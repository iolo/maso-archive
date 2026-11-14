"""Pinned JPEG input for the existing mapped OCR and article export workflow."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath

from PIL import Image

from .inventory import ROOT, pin, write_json
from .package import image_transform


def checked_path(root, record):
    name = record['path']
    relative = PurePosixPath(name)
    if not name or relative.is_absolute() or '..' in relative.parts or '\\' in name or ':' in name:
        raise ValueError('Unsafe image-source path')
    path = root / name
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Image-source path escapes root')
    if pin(root, name) != {k: record[k] for k in ('path', 'sha256', 'bytes')}:
        raise ValueError(f'Image-source hash/size differs: {name}')
    return path


def load_image(page, root=ROOT):
    """Decode the exact hashed bytes, without modifying the JPEG master."""
    path = checked_path(root, page['image'])
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != page['image']['sha256']:
        raise ValueError('Image source changed while reading')
    with Image.open(io.BytesIO(raw)) as image:
        if image.format != 'JPEG' or list(image.size) != [page['width_px'], page['height_px']]:
            raise ValueError('JPEG dimensions/format differ from source record')
        image.load()
        return image.convert('RGB')


def validate_image_set(package, source, root=ROOT):
    descriptor = json.loads(checked_path(root, package['source']).read_bytes())
    if descriptor['kind'] != 'jpeg-set' or descriptor['issue_id'] != package['issue_id']:
        raise ValueError('Wrong JPEG source set')
    for record in descriptor['cleanup'].values():
        checked_path(root, record)
    for record in descriptor.get('toc_inputs', []):
        checked_path(root, record)
    if source['pages'] != descriptor['pages']:
        raise ValueError('JPEG inventory differs from pinned source set')
    pages = {p['source_index']: p for p in descriptor['pages']}
    keys = ('source_index', 'image', 'width_px', 'height_px', 'reading_order', 'source_filename_number')
    for page in package['pages']:
        original = pages.get(page['source_index'])
        if original is None or any(page[k] != original[k] for k in keys):
            raise ValueError('Mapped image geometry/provenance differs from source inventory')
        checked_path(root, page['image'])
    return descriptor


def prepare(issue, output, root=ROOT):
    """Freeze cleanup metadata and a canonical queue; do not map/OCR articles."""
    if len(issue) != 7 or not issue[:4].isdigit() or issue[4] != '-' or not issue[5:].isdigit():
        raise ValueError('Expected YYYY-MM issue')
    output = output.resolve()
    if not output.is_relative_to((root / 'archive/scans').resolve()) or output.exists():
        raise ValueError('Choose a fresh inventory under archive/scans/')
    folder = root / 'archive/scans' / issue
    manifest = json.loads((folder / 'manifest.json').read_bytes())
    review = json.loads((folder / 'review.json').read_bytes())
    cleanup = {name: pin(root, f'archive/scans/{issue}/{name}')
               for name in ('manifest.json', 'review.json', 'page-list.csv')}
    if review['manifestSha256'] != cleanup['manifest.json']['sha256']:
        raise ValueError('Cleanup review refers to another manifest')
    images = {i['path']: i for i in manifest['images']}
    with (folder / 'page-list.csv').open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != len(images) or {r['working_file'] for r in rows} != set(images):
        raise ValueError('Cleanup page list does not cover every master')
    printed = {r['path']: r['printedPage'] for r in review['printedPageSamples']}
    orders = {r['path']: r['readingOrder'] for r in review.get('readingOrderOverrides', [])}
    by_path = {r['working_file']: r for r in rows}
    pages = []
    for index, (name, image) in enumerate(images.items()):
        row = by_path[name]
        order = orders.get(name, image['readingOrder'])
        if (row['sha256'] != image['sha256'] or row['reading_order'] != str(order or '')
                or row['verified_printed_page'] != str(printed.get(name, ''))):
            raise ValueError('Cleanup page list disagrees with reviewed order/folio')
        record = dict(path=f'archive/scans/{issue}/{name}', sha256=image['sha256'], bytes=image['bytes'])
        checked_path(root, record)
        page = dict(source_index=index, image=record, width_px=image['dimensions'][0],
                    height_px=image['dimensions'][1], reading_order=order,
                    source_filename_number=image['sourceFilenameNumber'],
                    printed_page=str(printed[name]) if name in printed else None)
        page['image_to_upright_normalized'] = image_transform(page)
        pages.append(page)
    if sorted(p['reading_order'] for p in pages if p['reading_order'] is not None) != list(
            range(1, manifest['summary']['orderedImages'] + 1)):
        raise ValueError('Reviewed order repeats or loses a slot')
    toc = root / 'archive/toc/current'
    toc_manifest = json.loads((toc / 'manifest.json').read_bytes())
    for name, record in toc_manifest['outputs'].items():
        checked_path(root, dict(path=f'archive/toc/current/{name}', **record))
    if pin(root, 'TOC.md')['sha256'] != toc_manifest['source']['sha256']:
        raise ValueError('TOC source differs from current snapshot')
    if pin(root, 'metadata/identities/toc.json')['sha256'] != toc_manifest['identities_sha256']:
        raise ValueError('Canonical identity map differs from current snapshot')
    entries = [json.loads(line) for line in (toc / 'toc-entries.jsonl').read_bytes().splitlines()]
    entries = [e for e in entries if e['issue_id'] == f'maso-{issue}']
    if not entries:
        raise ValueError('Issue has no existing canonical TOC identities')
    output.mkdir(parents=True)
    snapshots = [('TOC.md', 'TOC.md'), ('metadata/identities/toc.json', 'identities.json'),
                 ('archive/toc/current/manifest.json', 'manifest.json'),
                 ('archive/toc/current/toc-entries.jsonl', 'toc-entries.jsonl')]
    (output / 'toc').mkdir()
    for original, name in snapshots:
        (output / 'toc' / name).write_bytes((root / original).read_bytes())
    descriptor = dict(schema_version=1, kind='jpeg-set', issue_id=f'maso-{issue}', cleanup=cleanup,
                      toc_inputs=[pin(root, (output / 'toc' / name).relative_to(root).as_posix())
                                  for _, name in snapshots],
                      pages=pages)
    write_json(output / 'source-set.json', descriptor)
    source = dict(id=f'jpeg-{issue}', kind='jpeg-set', **pin(root, (output / 'source-set.json').relative_to(root).as_posix()))
    write_json(output / 'sources.json', dict(sources=[dict(source, scope='toc-entries-and-cover', pages=pages)]))
    queue = [dict(toc_entry_id=e['id'], issue_id=e['issue_id'], source_id=source['id'],
                  title=e['title_candidate'], canonical_entry=e, status='unclassified') for e in entries]
    (output / 'queue.jsonl').write_text(''.join(json.dumps(e, ensure_ascii=False) + '\n' for e in queue), encoding='utf-8')
    return dict(issue=issue, sourceImages=len(pages), tocIdentities=len(queue), source=source)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--issue', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.issue, args.output), indent=2))


if __name__ == '__main__':
    main()
