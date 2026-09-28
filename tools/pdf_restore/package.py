"""Scan package identities, coordinate transforms and structural evidence checks."""
import argparse
import json
import math
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / 'schemas/pdf-article.schema.json'


def scan_id(toc_entry_id):
    return 'scan-' + toc_entry_id


def orientation_degrees(page):
    """Explicit clockwise raster correction; absence preserves legacy geometry."""
    correction = page.get('orientation_correction')
    if correction is None and 'orientation_correction' not in page:
        return 0
    if (not isinstance(correction, dict) or
        set(correction) != {'clockwise_degrees', 'evidence'} or
        type(correction['clockwise_degrees']) is not int or
        correction['clockwise_degrees'] not in (90, 180, 270) or
        not isinstance(correction['evidence'], str) or not correction['evidence'].strip()):
        raise ValueError('Invalid evidenced orientation correction')
    return correction['clockwise_degrees']


def page_transform(page):
    """Affine PDF bottom-left points -> upright normalized top-left coordinates.

    [a,b,c,d,e,f] means u=a*x+c*y+e; v=b*x+d*y+f. Use MediaBox because
    page rendering uses the full page (no Poppler -cropbox option). Compose
    immutable PDF rotation with the optional clockwise raster correction.
    """
    x0, y0, x1, y1 = page['MediaBox']
    width, height = x1 - x0, y1 - y0
    if width <= 0 or height <= 0:
        raise ValueError('Invalid source MediaBox')
    matrices = {0: [1, 0, 0, -1, -x0, y1], 90: [0, 1, 1, 0, -y0, -x0],
                180: [-1, 0, 0, 1, x1, -y0], 270: [0, -1, -1, 0, y1, x1]}
    if page['rotation'] not in matrices:
        raise ValueError('Unsupported page rotation')
    rotation = (page['rotation'] + orientation_degrees(page)) % 360
    if rotation in (90, 270):
        width, height = height, width
    a, b, c, d, e, f = matrices[rotation]
    return [a / width, b / height, c / width, d / height, e / width, f / height]


def overlaps(a, b):
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])


def validate_package(package):
    Draft202012Validator(json.loads(SCHEMA.read_bytes())).validate(package)
    if package['id'] != scan_id(package['toc_entry_id']):
        raise ValueError('Scan identity must derive from existing TOC identity')
    if not package['toc_entry_id'].startswith(package['issue_id'] + '-toc-'):
        raise ValueError('TOC identity belongs to another issue')
    pages = {p['pdf_index']: p for p in package['pages']}
    if len(pages) != len(package['pages']):
        raise ValueError('Duplicate source page')
    for page in pages.values():
        if page['pdf_page'] != page['pdf_index'] + 1:
            raise ValueError('PDF numbering disagrees with zero-based index')
        if any(not math.isclose(a, b, abs_tol=1e-12) for a, b in
               zip(page['pdf_to_upright_normalized'], page_transform(page))):
            raise ValueError('Rotation transform does not match source geometry')
    ids = set()
    for region in package['regions'] + package['excluded_regions']:
        if region['id'] in ids:
            raise ValueError('Duplicate region identity')
        ids.add(region['id'])
        if region['pdf_index'] not in pages:
            raise ValueError('Region refers to an unmapped page')
        x0, y0, x1, y1 = region['bbox']
        if not all(math.isfinite(v) for v in region['bbox']) or not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
            raise ValueError('Region bounds must be positive normalized upright coordinates')
    for region in package['regions']:
        for excluded in package['excluded_regions']:
            if region['pdf_index'] == excluded['pdf_index'] and overlaps(region['bbox'], excluded['bbox']):
                raise ValueError('Article region overlaps excluded material')
    included = {r['id'] for r in package['regions']}
    if package['mapping']['status'] == 'mapped' and not included:
        raise ValueError('Mapped article requires source regions')
    for block in package['blocks'] + package['figures']:
        if not set(block['region_ids']) <= included or not block['region_ids']:
            raise ValueError('Block/figure lacks eligible scan evidence')
    block_ids = [b['id'] for b in package['blocks']]
    figure_ids = [f['id'] for f in package['figures']]
    if len(set(block_ids + figure_ids)) != len(block_ids + figure_ids):
        raise ValueError('Duplicate content identity')
    expected_order = {('block', id) for id in block_ids} | {('figure', id) for id in figure_ids}
    if 'content_order' in package:
        order = [(item['type'], item['id']) for item in package['content_order']]
        if len(order) != len(set(order)) or set(order) != expected_order:
            raise ValueError('Content order must include every block and figure exactly once')
    if 'region_assets' in package:
        asset_ids = [item['region_id'] for item in package['region_assets']]
        if len(asset_ids) != len(set(asset_ids)) or not set(asset_ids) <= included:
            raise ValueError('Invalid or duplicate region asset')
    if package['availability'] == 'readable':
        represented = {id for b in package['blocks'] + package['figures'] for id in b['region_ids']}
        if package['mapping']['status'] != 'mapped' or represented != included:
            raise ValueError('Readable package must represent every mapped region')
        if 'content_order' not in package:
            raise ValueError('Readable package requires explicit content order')
        if {r['region_id'] for r in package.get('region_assets', [])} != included:
            raise ValueError('Readable package requires every scan-region asset')
    if not set(package['verification']['reviewed_region_ids']) <= included:
        raise ValueError('Review refers to unknown or excluded regions')
    if package['verification']['status'] == 'fully-reviewed':
        if set(package['verification']['reviewed_region_ids']) != included:
            raise ValueError('Full review must cover all mapped regions')
    def walk(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == 'path' and isinstance(item, str):
                    path = PurePosixPath(item)
                    if path.is_absolute() or '..' in path.parts or '\\' in item or ':' in item:
                        raise ValueError('Artifact paths must be safe package-relative paths')
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
    walk(package)
    return package


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path)
    args = parser.parse_args()
    result = validate_package(json.loads(args.package.read_bytes()))
    print(f"Validated {result['id']}: {len(result['regions'])} regions, {result['availability']}")


if __name__ == '__main__':
    main()
