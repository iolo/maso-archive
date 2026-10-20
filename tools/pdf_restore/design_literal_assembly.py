"""Opt-in lossless projection of disjoint mixed design-article natives.

All native files/scalar metadata survive; every additional array is projected.
Printed BASIC labels, opaque assembly/data rows and comment-row END stay literal.
Other formats delegate to the existing perspective/CP-M/graphic dispatcher.
"""
import argparse
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path

from . import assemble as assembly
from . import cpm_literal_assembly as cpm
from . import perspective_literal_assembly as perspective
from .assembly_indexes import block_ranges
from .build import check_export

FORMAT = 'design-literal-v1'
START, END = cpm.START, cpm.END
RESERVED = {'records', 'blocks', 'normalizations', 'regional_transcription_sources',
            'caption_associations_pending'}


def validate_recipe(recipe):
    compatible = deepcopy(recipe)
    if compatible.get('index_mode') == FORMAT:
        compatible['index_mode'] = 'namespaced-v1'
        if recipe.get('prose_joins') or recipe.get('shared_pdf_pages'):
            raise ValueError('Design assembly requires disjoint immutable blocks/pages')
    return perspective.validate_recipe(compatible)


def _listing_ranges(package):
    result, cursor = {}, 0
    blocks = {b['id']: b for b in package['blocks']}
    for item in package['content_order']:
        if item['type'] == 'block' and blocks[item['id']]['kind'] == 'code':
            end = cursor + len(blocks[item['id']]['text'].encode())
            result[item['id']] = (cursor, end)
            cursor = end
    return result


def validate_native(source, correction, expected_pages):
    scope = correction.get('segment_scope', {})
    if (scope.get('boundary_pdf_span') != expected_pages or
            scope.get('current_pdf_pages') != [p['pdf_page'] for p in source['pages']]):
        raise ValueError('Native source scope differs from explicit article/page coverage')
    if correction.get('caption_associations_pending'):
        raise ValueError('Unresolved native caption association requires explicit review')
    article, listing = assembly.text_bytes(source)
    ranges = {'article.txt': block_ranges(source), 'listing.txt': _listing_ranges(source)}
    regional = {'article.txt': correction.get('regional_text_index', []),
                'listing.txt': correction.get('regional_listing_index', [])}
    assets = {r['region_id']: r['asset'] for r in source['region_assets']}

    def visit(value, download=None, block=None, region=None):
        if isinstance(value, list):
            for item in value:
                visit(item, download, block, region)
        elif isinstance(value, dict):
            if {'path', 'sha256', 'bytes'} <= value.keys():
                return
            download = value.get('download', download)
            block = value.get('block_id', block)
            region = value.get('region_id', region)
            if (region is not None and value.get('scan') is not None and
                    value['scan'] != assets.get(region)):
                raise ValueError('Source record scan differs from its own region')
            if START in value or END in value:
                start, end = value.get(START), value.get(END)
                data = {'article.txt': article, 'listing.txt': listing}.get(download)
                if (data is None or type(start) is not int or type(end) is not int or
                        not 0 <= start <= end <= len(data)):
                    raise ValueError('Invalid literal source range/download')
                try:
                    data[:start].decode(); text = data[start:end].decode()
                except UnicodeDecodeError as error:
                    raise ValueError('Source range splits UTF-8') from error
                if 'transcription_excerpt' in value and value['transcription_excerpt'] != text:
                    raise ValueError('Source excerpt differs from its exact occurrence')
                owners = [block] if block is not None else value.get('block_ids', [])
                if not owners or any(id not in ranges[download] for id in owners):
                    raise ValueError('Source range has no known owning block')
                lo = min(ranges[download][id][0] for id in owners)
                hi = max(ranges[download][id][1] for id in owners)
                if not lo <= start <= end <= hi:
                    raise ValueError('Source range outside its own block')
                if region is not None:
                    if not any(r['region_id'] == region and r['block_id'] in owners and
                               r[START] <= start <= end <= r[END] for r in regional[download]):
                        raise ValueError('Source range outside its own regional occurrence')
                if 'physical_line' in value and 'text' in value and text != value['text'] + '\n':
                    raise ValueError('Physical listing row differs from its literal bytes')
                if 'scans' in value and value['scans'] != [assets[r] for r in value['region_ids']]:
                    raise ValueError('Source block scans differ from its named regions')
            for item in value.values():
                visit(item, download, block, region)
    visit(correction)


def project(recipe, originals):
    if recipe.get('index_mode') != FORMAT:
        return perspective.project(recipe, originals)
    validate_recipe(recipe)
    for source, correction in originals:
        validate_native(source, correction, recipe['expected_pdf_pages'])
    if originals[-1][1]['segment_scope'].get('deferred_pdf_pages') != []:
        raise ValueError('Final native still defers source pages')
    package, combined = assembly.project_legacy(recipe, originals, check_listing_markers=False)
    for key in ('regions', 'blocks', 'figures'):
        if len({r['id'] for r in package[key]}) != len(package[key]):
            raise ValueError('Disjoint native source identifiers overlap')
    arrays = sorted({k for _, c in originals for k, v in c.items()
                     if isinstance(v, list) and k not in RESERVED})
    for key in arrays:
        combined[key] = []
    combined.update(literal_source_format=FORMAT, native_metadata=[], native_array_ranges=[],
                    regional_transcription_sources=[], original_caption_associations=[],
                    caption_associations_pending=[])
    combined_article, combined_listing = assembly.text_bytes(package)
    targets = block_ranges(package)
    listing_offset = physical_offset = 0
    for spec, (source, correction) in zip(recipe['segments'], originals, strict=True):
        article, listing = assembly.text_bytes(source)
        local = block_ranges(source)
        first = next(iter(local))
        article_offset = targets[first][0] - local[first][0]
        if any(targets[id] != (a + article_offset, z + article_offset)
               for id, (a, z) in local.items()):
            raise ValueError('Native article block bytes or positions changed')
        if combined_listing[listing_offset:listing_offset + len(listing)] != listing:
            raise ValueError('Native listing bytes changed')
        prefix = 'segments/' + spec['name']
        paths = {r['asset']['path'] for r in source['region_assets']}
        paths |= {r[k]['path'] for r in source['raw_ocr'] for k in ('text', 'positions', 'settings')}
        paths |= {'map.json', 'corrections.json', 'runtime.json', 'provenance.json', 'manifest.json'}
        combined['native_metadata'].append(dict(source_segment=spec['name'], directory=prefix,
                                                original=deepcopy(correction)))
        combined['regional_transcription_sources'].append(dict(source_segment=spec['name'],
            original_source_pins=deepcopy(correction.get('regional_transcription_sources', []))))
        combined['original_caption_associations'].append(dict(source_segment=spec['name'],
            original=deepcopy(correction.get('caption_associations_pending', []))))
        for key in arrays:
            rows = cpm.project_record(correction.get(key, []), article=article, listing=listing,
                article_offset=article_offset, listing_offset=listing_offset,
                prefix=prefix, local_paths=paths)
            start = len(combined[key])
            for row in rows:
                if isinstance(row, dict):
                    row['source_segment'] = spec['name']
                    if 'article_physical_line' in row:
                        row['article_physical_line'] += physical_offset
            combined[key].extend(rows)
            combined['native_array_ranges'].append(dict(source_segment=spec['name'], category=key,
                first_row=start, end_row_exclusive=len(combined[key])))
        listing_offset += len(listing)
        physical_offset += len(correction.get('listing_line_index', []))
    if listing_offset != len(combined_listing):
        raise ValueError('Combined listing has unexplained bytes')
    combined['coverage'].update(source_bytes='unverified', execution_verified=False,
        human_acceptance='pending', physical_source_rows=physical_offset)
    return package, combined


@contextmanager
def installed():
    with perspective.installed():
        previous = assembly.project, assembly.validate_recipe
        assembly.project, assembly.validate_recipe = project, validate_recipe
        try:
            yield
        finally:
            assembly.project, assembly.validate_recipe = previous


def assemble(recipe, output, root=assembly.ROOT):
    with installed():
        return assembly.assemble(recipe, output, root=root)


def check(output):
    with installed():
        return check_export(Path(output))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if not args.check and args.recipe is None:
        parser.error('--recipe is required')
    package = check(args.output) if args.check else assemble(args.recipe, args.output)
    print(f"Design literal assembly: {package['id']} / {package['availability']}")


if __name__ == '__main__':
    main()
