"""Build/check the private all-restored volunteer reader with August's pinned adapters.

August's standalone closeout used four narrowly scoped validation extensions.
Install those exact scripts before running the ordinary reader exporter/checker;
never bypass package validation or alter historical restoration artifacts.
"""
import argparse
import json
from pathlib import Path
from runpy import run_path

from tools.pdf_restore.inventory import ROOT, digest

ADAPTERS = (
    ('private/pdf-restoration/13-1984-08-adaptive/z80-boundary-adapter.py',
     '7473648ed4f33c8e881dc54569f0a7016e2f749e78bc8a221496e3bcb7adc365'),
    ('private/pdf-restoration/13-1984-08-adaptive/spc-boundary-adapter.py',
     'a696de884830e78a60fd8bb7f0179dfbe0d4dbbfd1278b53f97db48eb1370d96'),
    ('private/pdf-restoration/13-1984-08-adaptive/microcomputer-boundary-adapter.py',
     '75626f57bb395580ba793eade81d86266786b03c25a832a6797339d127d35fdc'),
    ('private/pdf-restoration/13-1984-08-closeout/review-range-adapter.py',
     '47ab44a5b69d0ed7a84228c57ad0e4c47f8ab40fa0614bafc9749f0076a5f436'),
)


def install_adapters(root=ROOT):
    # Verify the complete set before executing any private adapter.
    for relative, expected in ADAPTERS:
        path = root / relative
        if not path.is_file() or digest(path) != expected:
            raise ValueError(f'Missing or changed August closeout adapter: {relative}')
    for relative, _ in ADAPTERS:
        run_path(str(root / relative))['install']()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('export', 'check'))
    parser.add_argument('--base', type=Path, default=ROOT / 'dist/reading-room-routed-july-complete/data')
    parser.add_argument('--ledger', type=Path, default=ROOT / 'archive/pdf/1984-08/restoration/13-1984-08-closeout/export-ledger.json')
    parser.add_argument('--data', type=Path, default=ROOT / 'dist/reading-room/data')
    args = parser.parse_args()
    install_adapters()
    if args.action == 'export':
        from .scan_issue import stage_issue
        result = stage_issue(args.base, args.ledger, args.data)['counts']
    else:
        from .check import check
        result = check(args.data, require_thumbnails=True)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
