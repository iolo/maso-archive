"""Assemble disjoint reviewed page segments without regenerating OCR or its provenance."""
import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
import tempfile
import zipfile

from .build import checked, check_export, copy_pin, safe_path, validate_source
from .inventory import ROOT, pin, write_json
from .package import validate_package
from .preview import render_preview


def text_bytes(package):
    blocks = {b['id']: b for b in package['blocks']}
    parts, code = [], []
    for item in package['content_order']:
        if item['type'] == 'figure':
            parts.append(f'[그림 {item["id"]}: 스캔 이미지 참조]')
        else:
            block = blocks[item['id']]
            parts.append(block['text'])
            if block['kind'] == 'code':
                code.append(block['text'])
    return ('\n\n'.join(parts) + '\n').encode(), ''.join(code).encode()


def validate_recipe(recipe):
    if set(recipe) != {'segments', 'expected_pdf_pages', 'evidence', 'uncertainties', 'resolved_notes'}:
        raise ValueError('Unknown or missing assembly recipe field')
    segments = recipe['segments']
    if not 2 <= len(segments) <= 12:
        raise ValueError('Assembly requires two to twelve segments')
    names = []
    for row in segments:
        if set(row) != {'name', 'manifest'} or not re.fullmatch(r'[a-z][a-z0-9-]*', row['name']):
            raise ValueError('Invalid segment name or manifest')
        names.append(row['name'])
    if len(set(names)) != len(names):
        raise ValueError('Duplicate segment name')
    pages = recipe['expected_pdf_pages']
    if not pages or any(type(n) is not int or n < 1 for n in pages) or len(set(pages)) != len(pages):
        raise ValueError('Expected page coverage must be explicit and unique')
    for key in ('evidence', 'uncertainties'):
        if not isinstance(recipe[key], list) or any(not isinstance(v, str) or not v.strip() for v in recipe[key]):
            raise ValueError('Assembly review notes must be nonblank strings')
    if not recipe['evidence']:
        raise ValueError('Assembly requires coverage review evidence')
    seen = set()
    for row in recipe['resolved_notes']:
        if (set(row) != {'segment', 'note', 'reason'} or row['segment'] not in names or
            any(not isinstance(v, str) or not v.strip() for v in row.values())):
            raise ValueError('Resolved notes require a known segment, exact note and reason')
        key = (row['segment'], row['note'])
        if key in seen:
            raise ValueError('Duplicate resolved note')
        seen.add(key)


def rebase(record, prefix):
    return {**record, 'path': f'{prefix}/{record["path"]}'}


def read_segment(folder, manifest):
    """Validate an immutable single-map package, including OCR's original map binding."""
    checked(folder, {**manifest, 'path': 'manifest.json'})
    if (folder / 'assembly.json').exists():
        raise ValueError('Nested assemblies are not supported; name original segments')
    package = check_export(folder)
    if package['availability'] not in ('partial', 'readable') or package['verification']['status'] == 'unreviewed':
        raise ValueError('Assembly requires reviewed segments')
    validate_package({**package, 'availability': 'readable'})  # Every included region must be represented.
    if package['relationships']:
        raise ValueError('Comparison relationships require a separate assembly adapter')
    regions = {r['id']: r for r in package['regions']}
    if set(package['verification']['reviewed_region_ids']) != set(regions):
        raise ValueError('Segment review must cover all included regions')
    provenance = json.loads((folder / 'provenance.json').read_bytes())
    mapped = validate_package(json.loads(checked(folder, {**provenance['map'], 'path': 'map.json'})))
    corrections = json.loads(checked(folder, {**provenance['corrections'], 'path': 'corrections.json'}))
    for key in ('id', 'issue_id', 'toc_entry_id', 'source', 'toc_pin', 'pages', 'regions', 'excluded_regions', 'mapping'):
        if package[key] != mapped[key]:
            raise ValueError('Segment differs from its original map')
    if (corrections['article_id'] != package['id'] or corrections['map'] != provenance['map'] or
        corrections['blocks'] != package['blocks']):
        raise ValueError('Segment differs from its original correction review')
    records = {r['id']: r for r in corrections['records']}
    if len(records) != len(corrections['records']) or set(records) != set(regions):
        raise ValueError('Segment correction records must cover every region exactly once')
    assets = {r['region_id']: r['asset'] for r in package['region_assets']}
    for id, row in records.items():
        if row['scan'] != assets[id]:
            raise ValueError('Segment review scan differs from region asset')
    pages = {p['pdf_index']: p for p in package['pages']}
    raw_ids = set()
    for row in package['raw_ocr']:
        ids = row['region_ids']
        if len(ids) != 1 or ids[0] not in regions or ids[0] in raw_ids:
            raise ValueError('Invalid segment OCR region')
        id = ids[0]
        settings = json.loads(checked(folder, row['settings']))
        page = pages[regions[id]['pdf_index']]
        if (settings['package']['sha256'] != provenance['map']['sha256'] or
            settings['source_sha256'] != package['source']['sha256'] or
            settings['pdf_index'] != page['pdf_index'] or settings['pdf_page'] != page['pdf_page'] or
            settings['region_ids'] != ids or settings.get('orientation_correction') != page.get('orientation_correction') or
            records[id]['raw_ocr'] != row['text']):
            raise ValueError('Segment OCR provenance differs from original map/review')
        raw_ids.add(id)
    if raw_ids != {id for id, row in regions.items() if row['kind'] != 'figure'}:
        raise ValueError('Segment lacks complete regional OCR evidence')
    article, listing = text_bytes(package)
    if (folder / 'article.txt').read_bytes() != article or (listing and (folder / 'listing.txt').read_bytes() != listing):
        raise ValueError('Segment text/listing differs from reading order')
    return package, corrections


def project(recipe, segments):
    """Derive combined content and correction indexes; never modify original evidence."""
    validate_recipe(recipe)
    first = segments[0][0]
    package = deepcopy(first)
    arrays = ('pages', 'regions', 'excluded_regions', 'blocks', 'figures', 'content_order', 'raw_ocr', 'region_assets')
    for key in arrays:
        package[key] = []
    package.update(downloads=[], corrections=[], review_records=[], gaps=[])
    package['mapping'] = dict(status='mapped', evidence=recipe['evidence'], uncertainties=[])
    records, listing_index, graphics, definitions, segment_records = [], [], [], [], []
    retained_notes, all_pages, offset = [], [], 0
    for spec, (source, correction) in zip(recipe['segments'], segments, strict=True):
        name, prefix = spec['name'], 'segments/' + spec['name']
        if any(source[k] != first[k] for k in ('id', 'issue_id', 'toc_entry_id', 'source', 'toc_pin', 'title', 'coordinates')):
            raise ValueError('Segments have different article/source/TOC identities')
        notes = source['gaps'] + source['verification']['uncertainties'] + source['mapping']['uncertainties']
        notes += [note for block in source['blocks'] for note in block['uncertainties']]
        resolved = {row['note'] for row in recipe['resolved_notes'] if row['segment'] == name}
        if not resolved <= set(notes):
            raise ValueError('Resolved note is not an exact original uncertainty')
        keep = lambda values: [v for v in values if v not in resolved]
        retained_notes.extend(keep(notes))
        all_pages.extend(p['pdf_page'] for p in source['pages'])
        for key in ('pages', 'regions', 'excluded_regions', 'content_order'):
            package[key].extend(deepcopy(source[key]))
        for block in source['blocks']:
            package['blocks'].append({**deepcopy(block), 'uncertainties': keep(block['uncertainties'])})
        package['figures'].extend({**deepcopy(f), 'asset': rebase(f['asset'], prefix)} for f in source['figures'])
        package['region_assets'].extend({**r, 'asset': rebase(r['asset'], prefix)} for r in source['region_assets'])
        package['raw_ocr'].extend({**r, **{k: rebase(r[k], prefix) for k in ('text', 'positions', 'settings')}}
                                  for r in source['raw_ocr'])
        for row in correction['records']:
            records.append({**deepcopy(row), 'scan': rebase(row['scan'], prefix),
                            'raw_ocr': rebase(row['raw_ocr'], prefix) if row['raw_ocr'] else None,
                            'source_segment': name})
        _, source_listing = text_bytes(source)
        source_blocks = {b['id']: b for b in source['blocks']}
        supplied = correction.get('listing_index')
        supplied_by_id = {r['block_id']: r for r in supplied or []}
        code_ids = [r['id'] for r in source['content_order'] if r['type'] == 'block' and source_blocks[r['id']]['kind'] == 'code']
        if supplied is not None and (len(supplied_by_id) != len(supplied) or set(supplied_by_id) != set(code_ids)):
            raise ValueError('Segment listing index does not cover its code blocks')
        local_offset = 0
        for id in code_ids:
            block = source_blocks[id]
            end = local_offset + len(block['text'].encode())
            row = supplied_by_id.get(id, {'block_id': id, 'region_ids': block['region_ids']})
            if supplied is not None and (row['utf8_byte_start'] != local_offset or row['utf8_byte_end_exclusive'] != end):
                raise ValueError('Segment listing byte range differs from code block')
            listing_index.append({**deepcopy(row), 'download': 'listing.txt', 'source_segment': name,
                                  'utf8_byte_start': offset + local_offset, 'utf8_byte_end_exclusive': offset + end})
            local_offset = end
        assets = {r['region_id']: r['asset'] for r in source['region_assets']}
        for key, destination in (('unresolved_graphics', graphics), ('glyph_definitions', definitions)):
            for row in correction.get(key, []):
                if row['region_id'] not in assets or row['scan'] != assets[row['region_id']]:
                    raise ValueError('Correction index scan differs from mapped region')
                region_text = ''.join(b['text'] for b in source['blocks'] if row['region_id'] in b['region_ids'])
                revised = {**deepcopy(row), 'scan': rebase(row['scan'], prefix), 'source_segment': name}
                if key == 'unresolved_graphics':
                    if not row['marker'] or region_text.count(row['marker']) != 1:
                        raise ValueError('Graphics marker differs from its reviewed region')
                else:
                    start, end = row['utf8_byte_start'], row['utf8_byte_end_exclusive']
                    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(source_listing):
                        raise ValueError('Definition byte range outside listing')
                    span = source_listing[start:end].decode('utf-8')
                    if span not in region_text or not span.startswith(f"{row['printed_line']} DEF CHR$({row['printed_code']})="):
                        raise ValueError('Definition range differs from its reviewed region')
                    revised.update(download='listing.txt', utf8_byte_start=offset + start, utf8_byte_end_exclusive=offset + end)
                destination.append(revised)
        segment_records.append(dict(name=name, directory=prefix, original_coverage=correction.get('coverage'),
                                    manual_postproduction=correction.get('manual_postproduction')))
        offset += len(source_listing)
    if all_pages != recipe['expected_pdf_pages'] or len(set(all_pages)) != len(all_pages):
        raise ValueError('Segments overlap or differ from expected ordered page coverage')
    if len({r['id'] for r in records}) != len(records):
        raise ValueError('Duplicate correction identity across segments')
    if len({r['id'] for r in graphics}) != len(graphics) or len({r['marker'] for r in graphics}) != len(graphics):
        raise ValueError('Duplicate graphics occurrence identity across segments')
    if Counter(re.findall(r'⟦G[^⟧]*⟧', text_bytes(package)[1].decode())) != Counter(r['marker'] for r in graphics):
        raise ValueError('Graphics occurrence index does not match combined listing')
    package['gaps'] = list(dict.fromkeys(recipe['uncertainties'] + retained_notes))
    package['availability'] = 'readable'
    package['verification'] = dict(status='sample-reviewed', reviewed_region_ids=[r['id'] for r in package['regions']],
                                   evidence=recipe['evidence'], uncertainties=package['gaps'])
    validate_package(package)
    corrections = dict(article_id=package['id'], policy='Assembly of immutable reviewed segments; no new OCR or character-code inference.',
                       records=records, blocks=package['blocks'], segments=segment_records, resolved_notes=recipe['resolved_notes'],
                       normalizations=package['gaps'], listing_index=listing_index, unresolved_graphics=graphics,
                       glyph_definitions=definitions, coverage=dict(article_pdf_pages=all_pages, included_pdf_pages=all_pages,
                       included_printed_pages=[p['printed_page'] for p in package['pages']], deferred_pdf_pages=[],
                       complete_article=True, assembly_pending=False, source_pages_missing=False), character_perfect_code=False)
    return package, corrections


def map_projection(package):
    mapped = deepcopy(package)
    for key in ('blocks', 'figures', 'content_order', 'raw_ocr', 'region_assets', 'downloads', 'corrections', 'review_records'):
        mapped[key] = []
    mapped['availability'] = 'unresolved'
    mapped['verification'] = dict(status='unreviewed', reviewed_region_ids=[], evidence=[], uncertainties=[])
    return validate_package(mapped)


def assembly_record(folder, recipe):
    rows = []
    for spec in recipe['segments']:
        prefix = 'segments/' + spec['name']
        rows.append(dict(name=spec['name'], manifest=pin(folder, prefix + '/manifest.json'),
                         map=pin(folder, prefix + '/map.json'), corrections=pin(folder, prefix + '/corrections.json')))
    return dict(version=1, recipe=pin(folder, 'assembly-recipe.json'), segments=rows)


def raw_names(package, recipe):
    names = {r[k]['path'] for r in package['raw_ocr'] for k in ('text', 'positions', 'settings')}
    names |= {r['asset']['path'] for r in package['region_assets']}
    names |= {f'segments/{s["name"]}/{name}' for s in recipe['segments']
              for name in ('map.json', 'runtime.json', 'provenance.json', 'corrections.json')}
    return sorted(names)


def check_assembly(folder, package):
    """Offline verification against retained segments, even if outer files were rehashed."""
    recipe = json.loads((folder / 'assembly-recipe.json').read_bytes())
    validate_recipe(recipe)
    segments = [read_segment(safe_path(folder, 'segments/' + row['name']), row['manifest']) for row in recipe['segments']]
    expected, corrections = project(recipe, segments)
    if json.loads((folder / 'map.json').read_bytes()) != map_projection(expected):
        raise ValueError('Assembly map differs from original segments')
    corrections['map'] = pin(folder, 'map.json')
    if json.loads((folder / 'corrections.json').read_bytes()) != corrections:
        raise ValueError('Assembly correction projection differs from original segments')
    if json.loads((folder / 'assembly.json').read_bytes()) != assembly_record(folder, recipe):
        raise ValueError('Assembly provenance differs from retained inputs')
    expected['corrections'] = [pin(folder, 'corrections.json')]
    expected['review_records'] = [pin(folder, 'assembly.json')]
    article, listing = text_bytes(expected)
    for name, value in [('article.txt', article)] + ([('listing.txt', listing)] if listing else []):
        if (folder / name).read_bytes() != value:
            raise ValueError('Assembly reading download differs from original segments')
    with zipfile.ZipFile(folder / 'raw-ocr.zip') as archive:
        if archive.namelist() != raw_names(expected, recipe) or any(
                archive.read(name) != safe_path(folder, name).read_bytes() for name in archive.namelist()):
            raise ValueError('Assembly raw archive differs from original segment bytes')
    expected['downloads'] = [pin(folder, name) for name in ['article.txt'] + (['listing.txt'] if listing else []) + ['raw-ocr.zip']]
    if package != expected:
        raise ValueError('Assembly article projection differs from original segments')
    html, css = render_preview(expected)
    if (folder / 'index.html').read_text() != html or (folder / 'style.css').read_text() != css:
        raise ValueError('Assembly preview differs from reading projection')


def assemble(recipe_path, output, root=ROOT):
    root, recipe_path, output = (Path(p).resolve() for p in (root, recipe_path, output))
    if not any(output.is_relative_to(root / d) for d in ('build', 'private')) or output.exists():
        raise ValueError('Use a fresh assembly output under build/ or private/')
    recipe_pin = pin(recipe_path.parent, recipe_path.name)
    recipe = json.loads(checked(recipe_path.parent, recipe_pin))
    validate_recipe(recipe)
    folders, segments = [], []
    for spec in recipe['segments']:
        checked(root, spec['manifest'])
        folder = safe_path(root, spec['manifest']['path']).parent
        if output.is_relative_to(folder) or folder.is_relative_to(output):
            raise ValueError('Assembly output overlaps a segment input')
        segments.append(read_segment(folder, spec['manifest']))
        folders.append(folder)
    package, corrections = project(recipe, segments)
    validate_source(package, root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent, prefix='.pdf-assembly-') as temporary:
        stage = Path(temporary) / 'export'
        stage.mkdir()
        for spec, folder in zip(recipe['segments'], folders, strict=True):
            manifest = json.loads(checked(root, spec['manifest']))
            prefix = 'segments/' + spec['name']
            for record in manifest['files'] + [pin(folder, 'manifest.json')]:
                copy_pin(folder, stage, record, prefix + '/' + record['path'])
        copy_pin(recipe_path.parent, stage, recipe_pin, 'assembly-recipe.json')
        write_json(stage / 'map.json', map_projection(package))
        corrections['map'] = pin(stage, 'map.json')
        write_json(stage / 'corrections.json', corrections)
        write_json(stage / 'assembly.json', assembly_record(stage, recipe))
        package['corrections'] = [pin(stage, 'corrections.json')]
        package['review_records'] = [pin(stage, 'assembly.json')]
        article, listing = text_bytes(package)
        (stage / 'article.txt').write_bytes(article)
        if listing:
            (stage / 'listing.txt').write_bytes(listing)
        with zipfile.ZipFile(stage / 'raw-ocr.zip', 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for name in raw_names(package, recipe):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type, info.external_attr = zipfile.ZIP_DEFLATED, 0o644 << 16
                archive.writestr(info, safe_path(stage, name).read_bytes())
        package['downloads'] = [pin(stage, name) for name in ['article.txt'] + (['listing.txt'] if listing else []) + ['raw-ocr.zip']]
        validate_package(package)
        write_json(stage / 'article.json', package)
        html, css = render_preview(package)
        (stage / 'index.html').write_text(html)
        (stage / 'style.css').write_text(css)
        write_json(stage / 'manifest.json', dict(article_id=package['id'], availability=package['availability'],
                   verification=package['verification']['status'], files=[pin(stage, p.relative_to(stage).as_posix())
                   for p in sorted(stage.rglob('*')) if p.is_file()]))
        check_export(stage)
        checked(recipe_path.parent, recipe_pin)
        for spec, folder in zip(recipe['segments'], folders, strict=True):
            read_segment(folder, spec['manifest'])
        stage.rename(output)
    return package


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    package = assemble(args.recipe, args.output)
    print(f'Assembled {package["id"]}: {len(package["pages"])} pages / {package["availability"]}')


if __name__ == '__main__':
    main()
