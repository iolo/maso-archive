"""Private TOC restoration commands; catalog files are always read-only."""
import argparse
import json
from pathlib import Path

from tools.reading_room.export import read
from .inventory import PRIVATE, SOURCES, inventory, normalize, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['inventory', 'normalize', 'ocr', 'compare', 'prepare'])
    parser.add_argument('--sources', type=Path, default=SOURCES)
    parser.add_argument('--inventory', type=Path, default=PRIVATE / 'inventory.json')
    parser.add_argument('--reviews', type=Path, default=PRIVATE / 'reviews.json')
    parser.add_argument('--journal', type=Path, default=PRIVATE / 'rename-journal.json')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--dates', nargs='*', help='Limit OCR to selected YYMM dates')
    parser.add_argument('--config', type=Path, help='Per-image OCR config keyed by normalized image name')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--rollback', action='store_true')
    args = parser.parse_args()
    if (args.apply or args.rollback) and args.action != 'normalize':
        parser.error('--apply/--rollback are only for normalize')
    if args.action == 'inventory' or (args.action == 'normalize' and not args.apply):
        result = inventory(args.sources)
        if args.inventory.exists() and read(args.inventory) != result:
            parser.error('Inventory already exists and differs; choose a new --inventory to preserve the rename mapping')
        save(args.inventory, result)
        print(json.dumps({k:v for k,v in result.items() if k != 'records'}))
    elif args.action == 'normalize':
        print(json.dumps(normalize(args.inventory, args.reviews, args.journal, args.rollback)))
    elif args.action == 'prepare':
        from tools.reading_room.tocs import prepare, DEFAULT_OUTPUT
        result = prepare(args.sources, args.output or DEFAULT_OUTPUT, args.reviews)
        print(json.dumps(dict(pages=len(result['records']))))
    elif args.action == 'ocr':
        from .ocr import ocr_page
        manifest = inventory(args.sources)
        if manifest['errors']:
            raise ValueError('Invalid OCR inputs')
        output = args.output or PRIVATE / 'ocr'
        index_path = output.parent / 'ocr-index.json'
        existing = read(index_path)['pages'] if index_path.exists() else []
        live = {r['new']:r['sha256'] for r in manifest['records']}
        rows = {r['name']:r for r in existing if live.get(r['name']) == r['sha256']}
        config = read(args.config) if args.config else {}
        for row in manifest['records']:
            if args.dates and row['date'] not in args.dates:
                continue
            _, destination = ocr_page(row, args.sources, output, config.get(row['new']))
            rows[row['new']] = dict(name=row['new'], date=row['date'], sequence=row['sequence'],
                                   sha256=row['sha256'], evidence=str(destination / 'evidence.json'))
            save(index_path, dict(pages=sorted(rows.values(), key=lambda r:r['name'])))
            print(row['new'], flush=True)
    elif args.action == 'compare':
        from .compare import compare
        print(compare(output=args.output or PRIVATE / 'reports', reviews_path=args.reviews))


if __name__ == '__main__':
    main()
