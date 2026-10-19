"""Opt-in assembly of literal, unnumbered CP/M source transcripts and tables.

Original packages and correction metadata remain immutable. Every native array
is projected, including nested compiler ranges and zero-length table cells.
The adapter delegates all other formats to the existing graphic dispatcher.
"""
import argparse
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path

from . import assemble as assembly
from . import graphic_literal_assembly as graphic
from .assembly_indexes import block_ranges
from .build import check_export

FORMAT = 'cpm-literal-v1'
START, END = 'utf8_byte_start', 'utf8_byte_end_exclusive'
_VALIDATE = assembly.validate_recipe


def validate_recipe(recipe):
    compatible = deepcopy(recipe)
    if compatible.get('index_mode') == FORMAT:
        compatible['index_mode'] = 'namespaced-v1'
    return _VALIDATE(compatible)


def project_record(value, *, article, listing, article_offset, listing_offset,
                   prefix, local_paths, inherited_download=None):
    """Rebase exact occurrences recursively, retaining literal values and IDs."""
    if isinstance(value, list):
        return [project_record(v, article=article, listing=listing,
                    article_offset=article_offset, listing_offset=listing_offset,
                    prefix=prefix, local_paths=local_paths,
                    inherited_download=inherited_download) for v in value]
    if not isinstance(value, dict):
        return deepcopy(value)
    if {'path', 'sha256', 'bytes'} <= value.keys():
        return (assembly.rebase(value, prefix) if value['path'] in local_paths
                else deepcopy(value))
    download = value.get('download', inherited_download)
    result = {k: project_record(v, article=article, listing=listing,
                article_offset=article_offset, listing_offset=listing_offset,
                prefix=prefix, local_paths=local_paths,
                inherited_download=download) for k, v in value.items()}
    if START in value or END in value:
        if START not in value or END not in value or download not in ('article.txt', 'listing.txt'):
            raise ValueError('Literal range needs two endpoints and a known download')
        data = article if download == 'article.txt' else listing
        offset = article_offset if download == 'article.txt' else listing_offset
        start, end = value[START], value[END]
        if type(start) is not int or type(end) is not int or not 0 <= start <= end <= len(data):
            raise ValueError('Literal range outside source download')
        # Validate both endpoints, including a zero-length range inside a glyph.
        try:
            data[:start].decode('utf-8')
            text = data[start:end].decode('utf-8')
        except UnicodeDecodeError as error:
            raise ValueError('Literal range splits a UTF-8 glyph') from error
        if 'transcription_excerpt' in value and text != value['transcription_excerpt']:
            raise ValueError('Literal excerpt differs from its source occurrence')
        result.update({START: start + offset, END: end + offset})
    for key in ('table_utf8_byte_start', 'table_utf8_byte_end_exclusive'):
        if key in value:
            point = value[key]
            if type(point) is not int or not 0 <= point <= len(article):
                raise ValueError('Table position outside source article')
            article[:point].decode('utf-8')
            result[key] = point + article_offset
    return result


def project(recipe, originals):
    if recipe.get('index_mode') != FORMAT:
        return graphic.project(recipe, originals)
    validate_recipe(recipe)
    if recipe.get('prose_joins') or recipe.get('shared_pdf_pages'):
        raise ValueError('Literal CP/M assembly requires disjoint immutable native blocks')
    for source, correction in originals:
        if not isinstance(correction.get('segment_scope'), dict):
            raise ValueError('Literal CP/M source scope is required')
        if any(row.get('printed_line') is not None or row.get('printed_line_visible') is not False
               for row in correction.get('listing_line_index', [])):
            raise ValueError('Literal CP/M rows must not claim BASIC line numbers')
    package, combined = assembly.project_legacy(recipe, originals, check_listing_markers=False)
    # All identifiers in these disjoint native maps must already be unique.
    for key in ('regions', 'blocks', 'figures'):
        if len({r['id'] for r in package[key]}) != len(package[key]):
            raise ValueError('Literal CP/M native identifiers overlap')
    reserved = {'records', 'blocks', 'normalizations', 'regional_transcription_sources',
                'caption_associations_pending'}
    arrays = sorted({k for _, c in originals for k, v in c.items()
                     if isinstance(v, list) and k not in reserved})
    for key in arrays:
        combined[key] = []
    combined['literal_source_format'] = FORMAT
    combined['native_metadata'] = []
    combined['regional_transcription_sources'] = []
    combined['original_caption_associations'] = []
    combined['caption_associations_pending'] = []
    combined_article, combined_listing = assembly.text_bytes(package)
    combined_ranges = block_ranges(package)
    listing_offset = physical_offset = 0
    for spec, (source, correction) in zip(recipe['segments'], originals, strict=True):
        article, listing = assembly.text_bytes(source)
        local_ranges = block_ranges(source)
        first = next(iter(local_ranges))
        article_offset = combined_ranges[first][0] - local_ranges[first][0]
        if any(combined_ranges[id] != (a + article_offset, z + article_offset)
               for id, (a, z) in local_ranges.items()):
            raise ValueError('Literal source blocks changed during assembly')
        if combined_listing[listing_offset:listing_offset + len(listing)] != listing:
            raise ValueError('Literal source listing bytes changed')
        prefix = 'segments/' + spec['name']
        local_paths = {r['asset']['path'] for r in source['region_assets']}
        local_paths |= {r[k]['path'] for r in source['raw_ocr'] for k in ('text', 'positions', 'settings')}
        local_paths |= {'map.json', 'corrections.json', 'runtime.json', 'provenance.json', 'manifest.json'}
        combined['native_metadata'].append(dict(source_segment=spec['name'], directory=prefix,
            original=deepcopy(correction)))
        combined['regional_transcription_sources'].append(dict(source_segment=spec['name'],
            original_source_pins=deepcopy(correction.get('regional_transcription_sources', [])),
            note='Original external source-evidence pins; full corrected text retained in original metadata.'))
        combined['original_caption_associations'].append(dict(source_segment=spec['name'],
            original=deepcopy(correction.get('caption_associations_pending', []))))
        for key in arrays:
            rows = project_record(correction.get(key, []), article=article, listing=listing,
                article_offset=article_offset, listing_offset=listing_offset,
                prefix=prefix, local_paths=local_paths)
            for row in rows:
                if isinstance(row, dict):
                    row['source_segment'] = spec['name']
                    if 'article_physical_line' in row:
                        row['article_physical_line'] += physical_offset
            combined[key].extend(rows)
        listing_offset += len(listing)
        physical_offset += len(correction.get('listing_line_index', []))
    # Resolve only the already reviewed cross-native figure16 association.
    incoming = [c['segment_scope']['incoming_figure16'] for _, c in originals
                if 'incoming_figure16' in c['segment_scope']]
    if len(incoming) != 1:
        raise ValueError('One reviewed figure16 incoming caption association is required')
    association = incoming[0]
    owners = [(spec, source, correction) for spec, (source, correction)
              in zip(recipe['segments'], originals, strict=True)
              if association['opening_region'] in {r['id'] for r in source['regions']}]
    if len(owners) != 1 or owners[0][0]['manifest'] != association['opening_manifest']:
        raise ValueError('Figure16 opening association differs from its immutable native')
    caption = next(b for b in package['blocks'] if b['id'] == association['caption_block_id'])
    frames = association['future_combined_figure_ids']
    if frames != [association['opening_region'] + '-image', association['ending_region'] + '-image']:
        raise ValueError('Figure16 requires its two original source frames')
    ending = next(r for r in package['regions'] if r['id'] == association['ending_region'])
    outgoing = owners[0][2]['segment_scope'].get('outgoing_figure16', {})
    if outgoing.get('caption_on_pdf') != ending['pdf_index'] + 1:
        raise ValueError('Figure16 ending page differs from its reviewed boundary')
    for id in frames:
        figure = next(f for f in package['figures'] if f['id'] == id)
        if figure['caption'] not in (None, caption['text']):
            raise ValueError('Figure16 caption differs between original frames')
        figure['caption'] = caption['text']
    opening = frames[0]
    combined['caption_links'].append(dict(figure_id=opening, figure_region_id=opening,
        caption_block_id=caption['id'], caption_region_id=caption['region_ids'][0],
        internal_text_transcribed=True, association='Reviewed cross-native figure16 caption.'))
    ending_link = next(r for r in combined['listing_caption_links']
                       if r['listing_id'] == association['ending_region'])
    opening_link = deepcopy(ending_link)
    opening_link['caption_source_segment'] = opening_link.pop('source_segment')
    opening_link.update(listing_id=association['opening_region'],
        block_ids=[association['opening_region']], figure_ids=deepcopy(frames),
        assembly_derived=True,
        association='Observed ending caption also owns the original opening listing/frame.')
    combined['listing_caption_links'].append(opening_link)
    combined['resolved_caption_associations'] = [deepcopy(association)]
    combined['connected_listing_groups'] = [dict(listing_ids=[association['opening_region'],
        association['ending_region']], figure_ids=frames, caption_block_id=caption['id'],
        policy='Physical native rows/blocks preserved; no renumbering or inferred byte join.')]
    uncaptioned = combined.setdefault('uncaptioned_figure_index', [])
    known_uncaptioned = {r['figure_id'] for r in uncaptioned}
    for figure in package['figures']:
        if figure['caption'] is None and figure['id'] not in known_uncaptioned:
            uncaptioned.append(dict(figure_id=figure['id'], region_id=figure['region_ids'][0],
                scan=deepcopy(figure['asset']), caption=None,
                reason='No printed caption in original source; original native metadata retained.'))
    combined['coverage'].update(source_bytes='unverified', execution_verified=False)
    return package, combined


@contextmanager
def installed():
    with graphic.installed():
        previous_project, previous_validate = assembly.project, assembly.validate_recipe
        assembly.project, assembly.validate_recipe = project, validate_recipe
        try:
            yield
        finally:
            assembly.project, assembly.validate_recipe = previous_project, previous_validate


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
    if args.check:
        package = check(args.output)
    else:
        if args.recipe is None:
            parser.error('--recipe is required for assembly')
        package = assemble(args.recipe, args.output)
    print(f"CP/M literal assembly: {package['id']} / {package['availability']}")


if __name__ == '__main__':
    main()
