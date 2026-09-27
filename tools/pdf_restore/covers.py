"""Prepare bounded cover evidence; install only explicitly reviewed front covers."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

from PIL import Image

from .inventory import ROOT, digest, pin, write_json

DEFAULT = ROOT / 'private/pdf-restoration/covers'


def existing_covers(root):
    return [pin(root, path.relative_to(root).as_posix()) for path in sorted((root / 'covers').glob('*'))
            if path.is_file()]


def render(root, source, page, target, size=1800):
    if not 1 <= page <= source['page_count']:
        raise ValueError('PDF page out of range')
    if digest(root / source['path']) != source['sha256']:
        raise ValueError('PDF source hash changed')
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-singlefile',
                    '-scale-to', str(size), '-jpeg', '-jpegopt', 'quality=92',
                    str(root / source['path']), str(target.with_suffix(''))], check=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with Image.open(target) as picture:
        width, height = picture.size
        picture.verify()
    page_metadata = source['pages'][page - 1]
    source_width, source_height = page_metadata['width_pt'], page_metadata['height_pt']
    if page_metadata['rotation'] in (90, 270):
        source_width, source_height = source_height, source_width
    if abs(width / height - source_width / source_height) > 0.002:
        raise ValueError('Rendered cover proportions differ from rotated PDF dimensions')
    return dict(pdf_index=page - 1, pdf_page=page, width=width, height=height,
                source_page_metadata=page_metadata,
                settings={'renderer': 'pdftoppm', 'scale_to': size, 'format': 'jpeg', 'quality': 92,
                          'rotation': 'PDF metadata applied by Poppler', 'crop': 'full page'},
                artifact=pin(target.parent, target.name))


def prepare(root=ROOT, output=DEFAULT):
    if output.exists():
        raise ValueError('Cover checkpoint already exists')
    inventory = root / 'private/pdf-restoration/inventory/sources.json'
    sources = json.loads(inventory.read_bytes())['sources']
    output.mkdir(parents=True)
    write_json(output / 'existing-before.json', existing_covers(root))
    records = []
    for source in sources:
        target = output / 'candidates' / f'{source["id"]}-page-001.jpg'
        record = render(root, source, 1, target)
        record['artifact'] = pin(output, target.relative_to(output).as_posix())
        records.append(dict(source_id=source['id'], source_sha256=source['sha256'],
                            filename_issue_label=source['filename_issue_label'], candidate=record,
                            inspected_pdf_pages=[1], status='awaiting-visual-review'))
    version = subprocess.run(['pdftoppm', '-v'], capture_output=True, check=True)
    write_json(output / 'candidates.json', dict(renderer_version=(version.stdout + version.stderr).decode().splitlines()[0],
                                               inventory=pin(root, inventory.relative_to(root).as_posix()),
                                               records=records))


def install(root=ROOT, output=DEFAULT):
    """Review is a private, explicit evidence record, never inferred from names."""
    if (output / 'ledger.json').exists():
        raise ValueError('Cover ledger already installed')
    prepared = json.loads((output / 'candidates.json').read_bytes())
    inventory = prepared['inventory']
    if pin(root, inventory['path']) != inventory:
        raise ValueError('Source inventory changed')
    sources = {s['id']: s for s in json.loads((root / inventory['path']).read_bytes())['sources']}
    before = json.loads((output / 'existing-before.json').read_bytes())
    for record in before:
        if pin(root, record['path']) != record:
            raise ValueError('An existing cover changed')
    reviews = json.loads((output / 'review.json').read_bytes())
    if len(reviews) != len(prepared['records']) or {r['source_id'] for r in reviews} != set(sources):
        raise ValueError('Require one review outcome per source')
    by_id = {r['source_id']: r for r in reviews}
    ledger = []
    planned = []
    for record in prepared['records']:
        source = sources[record['source_id']]
        if digest(root / source['path']) != source['sha256']:
            raise ValueError('PDF source changed')
        review = by_id[record['source_id']]
        if review['status'] not in ('verified-front-cover', 'uncertain', 'damaged', 'not-located'):
            raise ValueError('Unknown cover review status')
        row = {**record, 'review': review, 'installed': None}
        if review['status'] == 'verified-front-cover':
            if (review['visible_issue_label'] != source['filename_issue_label'] or
                    not review['date_evidence'] or not review['upright'] or not review['proportions_checked']):
                raise ValueError('Cover date/orientation/proportion gate failed')
            candidate = record['candidate']
            artifact = candidate['artifact']
            if review['reviewed_artifact'] != artifact:
                raise ValueError('Review does not identify the prepared cover bytes')
            if pin(output, artifact['path']) != artifact:
                raise ValueError('Reviewed cover bytes changed')
            matches = list((root / 'covers').glob(f'maso{review["visible_issue_label"]}.*'))
            if matches:
                row['disposition'] = 'existing-preserved; alternative-retained'
                row['existing'] = [pin(root, p.relative_to(root).as_posix()) for p in sorted(matches)]
            else:
                relative = f'covers/maso{review["visible_issue_label"]}.jpg'
                row['disposition'] = 'add-missing-cover'
                row['installed'] = {**artifact, 'path': relative}
                planned.append((output / artifact['path'], root / relative))
        else:
            row['disposition'] = 'deferred-no-association'
        ledger.append(row)
    # Validate all reviews before installing any image; exclusive creation preserves owner bytes.
    for source, destination in planned:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with source.open('rb') as stream, destination.open('xb') as target:
            shutil.copyfileobj(stream, target)
    for record in before:
        if pin(root, record['path']) != record:
            raise ValueError('An existing cover changed during installation')
    write_json(output / 'ledger.json', dict(checkpoint='2', sources=len(ledger),
               renderer_version=prepared['renderer_version'],
               existing_preserved=before, review=pin(output, 'review.json'), records=ledger))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'install'])
    args = parser.parse_args()
    (prepare if args.action == 'prepare' else install)()


if __name__ == '__main__':
    main()
