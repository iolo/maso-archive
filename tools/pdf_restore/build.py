"""Assemble a reviewed scan article and portable preview from pinned private inputs."""
import argparse
from copy import deepcopy
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile

from .inventory import ROOT, digest, pin, write_json
from .package import validate_package
from .preview import render_preview


def safe_path(root, relative):
    path = PurePosixPath(relative)
    if not relative or path.is_absolute() or '..' in path.parts or '\\' in relative or ':' in relative:
        raise ValueError(f'Unsafe artifact path: {relative}')
    target = root / relative
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Artifact symlink escapes its input directory')
    return target


def checked(root, record):
    path = safe_path(root, record['path'])
    if pin(root, record['path']) != record:
        raise ValueError(f'Artifact hash/size differs: {record["path"]}')
    return path.read_bytes()


def copy_pin(source_root, stage, record, destination=None):
    raw = checked(source_root, record)
    destination = destination or record['path']
    path = safe_path(stage, destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != raw:
        raise ValueError(f'Conflicting artifact destination: {destination}')
    path.write_bytes(raw)
    return pin(stage, destination)


def package_pins(package):
    for row in package['raw_ocr']:
        for key in ('text', 'positions', 'settings'):
            yield row[key]
    for row in package['figures']:
        yield row['asset']
    for row in package.get('region_assets', []):
        yield row['asset']
    yield from package['downloads']
    yield from package['corrections']
    yield from package.get('review_records', [])


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                raise ValueError('Duplicate HTML anchor')
            self.ids.add(attrs['id'])
        self.links.extend(attrs[key] for key in ('href', 'src') if key in attrs)


def check_export(output):
    package = validate_package(json.loads((output / 'article.json').read_bytes()))
    for record in package_pins(package):
        checked(output, record)
    links = Links()
    links.feed((output / 'index.html').read_text())
    for href in links.links:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            raise ValueError('Standalone preview should not depend on external links')
        if url.path and not safe_path(output, unquote(url.path)).is_file():
            raise ValueError(f'Broken preview link: {href}')
        if not url.path and url.fragment not in links.ids:
            raise ValueError(f'Broken preview fragment: {href}')
    # A readable package must render every included item and retain literal code.
    for block in package['blocks']:
        if block['id'] not in links.ids:
            raise ValueError('Preview silently omits a reading block')
    manifest_path = output / 'manifest.json'
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_bytes())
        names = [row['path'] for row in manifest['files']]
        actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
        if len(names) != len(set(names)) or actual != set(names) | {'manifest.json'}:
            raise ValueError('Export file inventory differs from manifest')
        for record in manifest['files']:
            checked(output, record)
    return package


def build(recipe_path, output, root=ROOT):
    root, recipe_path, output = Path(root).resolve(), Path(recipe_path).resolve(), Path(output).resolve()
    if not any(output.is_relative_to(root / d) for d in ('build', 'private')):
        raise ValueError('Generated export must remain under build/ or private/')
    if output.exists():
        raise ValueError('Export already exists; rebuild into a separate output for comparison')
    base = recipe_path.parent
    recipe = json.loads(recipe_path.read_bytes())
    package = validate_package(json.loads(checked(base, recipe['map'])))
    checked(root, {key: package['source'][key] for key in ('path', 'sha256', 'bytes')})
    checked(root, package['toc_pin'])
    inventory = root / 'private/pdf-restoration/inventory'
    sources = json.loads((inventory / 'sources.json').read_bytes())
    source = next((s for s in sources['sources'] if s['id'] == package['source']['id']), None)
    if source is None or source['scope'] != 'toc-entries-and-cover':
        raise ValueError('Article source is not eligible for TOC restoration')
    if any(source[k] != package['source'][k] for k in ('sha256', 'path', 'bytes')):
        raise ValueError('Mapped source disagrees with source inventory')
    for page in package['pages']:
        original = source['pages'][page['pdf_index']]
        if any(page[k] != original[k] for k in ('pdf_page', 'width_pt', 'height_pt', 'rotation', 'MediaBox', 'CropBox')):
            raise ValueError('Mapped page geometry disagrees with source inventory')
    queue = [json.loads(line) for line in (inventory / 'queue.jsonl').read_bytes().splitlines()]
    if not any(q['toc_entry_id'] == package['toc_entry_id'] and q['issue_id'] == package['issue_id']
               and q['source_id'] == package['source']['id'] for q in queue):
        raise ValueError('Article is not an existing eligible TOC entry')
    corrections = json.loads(checked(base, recipe['corrections']))
    if corrections['article_id'] != package['id'] or corrections['map'] != recipe['map']:
        raise ValueError('Corrections belong to a different article or region map')
    regions = {r['id']: r for r in package['regions']}
    records = {r['id']: r for r in corrections['records']}
    if len(records) != len(corrections['records']) or set(records) != set(regions):
        raise ValueError('Require an explicit review outcome for every mapped region')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent, prefix='.pdf-export-') as temporary:
        stage = Path(temporary) / 'export'
        stage.mkdir()
        package = deepcopy(package)
        package['blocks'] = corrections['blocks']
        package['raw_ocr'], package['region_assets'] = [], []
        raw_regions = set()
        for bundle in recipe['ocr_bundles']:
            folder = safe_path(base, bundle['directory'])
            manifest = json.loads(checked(base, bundle['manifest']))
            page = next((p for p in package['pages'] if p['pdf_page'] == manifest['pdf_page']), None)
            if page is None or manifest.get('orientation_correction') != page.get('orientation_correction'):
                raise ValueError('OCR evidence orientation differs from mapped page')
            if manifest['source_sha256'] != package['source']['sha256'] or manifest['runtime'] != recipe['runtime']:
                raise ValueError('OCR source or runtime provenance differs')
            images = {r['path']: r for r in manifest['images']}
            for row in manifest['results']:
                ids = row['region_ids']
                if len(ids) != 1:  # Page-level comparison remains in private evidence.
                    continue
                id = ids[0]
                if id not in regions or id in raw_regions:
                    raise ValueError('Duplicate or unknown OCR region')
                settings = json.loads(checked(folder, row['settings']))
                page = next(p for p in package['pages'] if p['pdf_index'] == regions[id]['pdf_index'])
                if settings.get('orientation_correction') != page.get('orientation_correction'):
                    raise ValueError('OCR orientation correction differs from mapped page')
                if (settings['package']['sha256'] != recipe['map']['sha256'] or
                    settings['source_sha256'] != package['source']['sha256'] or
                    settings['pdf_index'] != regions[id]['pdf_index'] or
                    manifest['pdf_page'] != settings['pdf_page'] or settings['region_ids'] != ids):
                    raise ValueError('OCR was prepared for a different region map')
                raw_regions.add(id)
                exported = {'region_ids': ids}
                for key in ('text', 'positions', 'settings'):
                    exported[key] = copy_pin(folder, stage, row[key], f'{bundle["directory"]}/{row[key]["path"]}')
                package['raw_ocr'].append(exported)
            for id, region in regions.items():
                if region['pdf_index'] + 1 == manifest['pdf_page']:
                    asset = images.get(id + '.png')
                    if asset is None:
                        raise ValueError('Missing scan-region image')
                    record = copy_pin(folder, stage, asset, f'{bundle["directory"]}/{asset["path"]}')
                    if records[id]['scan'] != record:
                        raise ValueError('Reviewed scan differs from exported scan')
                    if records[id]['raw_ocr'] is not None:
                        checked(base, records[id]['raw_ocr'])
                        checked(stage, records[id]['raw_ocr'])
                    package['region_assets'].append({'region_id': id, 'asset': record})
        required_ocr = {id for id, region in regions.items() if region['kind'] != 'figure'}
        if raw_regions != required_ocr:
            raise ValueError('Missing raw OCR outcome for a mapped text region')
        assets = {r['region_id']: r['asset'] for r in package['region_assets']}
        package['figures'] = [dict(id=f['id'], region_ids=f['region_ids'], asset=assets[f['region_id']],
                                   caption=f['caption']) for f in recipe['figures']]
        package['content_order'] = recipe['content_order']
        package['availability'], package['verification'], package['gaps'] = (
            recipe['availability'], recipe['verification'], recipe['gaps'])
        for block in package['blocks']:
            expected = [f'corrections.json#{id}' for id in block['region_ids']]
            if block['correction_evidence'] != expected:
                raise ValueError('Reading block correction evidence is not tied to its scan regions')
        package['corrections'] = [copy_pin(base, stage, recipe['corrections'], 'corrections.json')]
        copy_pin(base, stage, recipe['map'], 'map.json')
        runtime = root / 'private/pdf-restoration/ocr-runtime'
        runtime_pin = copy_pin(runtime, stage, recipe['runtime'], 'runtime.json')
        write_json(stage / 'provenance.json', dict(recipe=pin(base, recipe_path.name),
                   inventory=pin(inventory, 'sources.json'), queue=pin(inventory, 'queue.jsonl'),
                   map=recipe['map'], corrections=recipe['corrections'], runtime=runtime_pin,
                   ocr_bundles=recipe['ocr_bundles'],
                   review_scope='See per-region review records; structural completeness is not transcription accuracy.'))
        package['review_records'] = [pin(stage, 'provenance.json')]
        ordered_blocks = {b['id']: b for b in package['blocks']}
        parts, code = [], []
        for item in package['content_order']:
            if item['type'] == 'block':
                block = ordered_blocks[item['id']]
                parts.append(block['text'])
                if block['kind'] == 'code':
                    code.append(block['text'])
            else:
                parts.append(f'[그림 {item["id"]}: 스캔 이미지 참조]')
        (stage / 'article.txt').write_text('\n\n'.join(parts) + '\n', encoding='utf-8')
        if code:
            (stage / 'listing.txt').write_text(''.join(code), encoding='utf-8')
        with zipfile.ZipFile(stage / 'raw-ocr.zip', 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            names = {record[key]['path'] for record in package['raw_ocr'] for key in ('text', 'positions', 'settings')}
            names |= {row['asset']['path'] for row in package['region_assets']} | {'runtime.json'}
            for name in sorted(names):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, (stage / name).read_bytes())
        download_names = ['article.txt'] + (['listing.txt'] if code else []) + ['raw-ocr.zip']
        package['downloads'] = [pin(stage, name) for name in download_names]
        validate_package(package)
        write_json(stage / 'article.json', package)
        html, css = render_preview(package)
        (stage / 'index.html').write_text(html, encoding='utf-8')
        (stage / 'style.css').write_text(css, encoding='utf-8')
        check_export(stage)
        write_json(stage / 'manifest.json', dict(article_id=package['id'], availability=package['availability'],
                   verification=package['verification']['status'], mapped_regions=len(regions),
                   represented_regions=len({id for b in package['blocks'] + package['figures'] for id in b['region_ids']}),
                   files=[pin(stage, p.relative_to(stage).as_posix()) for p in sorted(stage.rglob('*')) if p.is_file()]))
        # Recheck immutable review and map before publishing a completed export.
        checked(base, recipe['map'])
        checked(base, recipe['corrections'])
        stage.rename(output)
    return package


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        package = check_export(args.output)
    else:
        if args.recipe is None:
            parser.error('--recipe is required when building')
        package = build(args.recipe, args.output)
    print(f"{'Checked' if args.check else 'Built'} {package['id']}: {package['availability']} / {package['verification']['status']}")


if __name__ == '__main__':
    main()
