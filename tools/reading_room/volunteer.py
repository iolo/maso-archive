"""Build/check the volunteer reader with all completed PDF restorations.

August's standalone closeout used four narrowly scoped validation extensions.
Install those exact scripts before running the ordinary reader exporter/checker;
never bypass package validation or alter historical restoration artifacts.
"""
import argparse
from contextlib import contextmanager
import importlib.util
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

FEBRUARY_DISPATCHER = (
    'archive/pdf/1985-02/restoration/heading-classification-62/assembly_dispatch.py',
    '2ef8160b2777886c58e865519121687640604331a8c2ba783f8472f4904deb0e',
)
DEFAULT_BASE = 'archive/releases/reading-room-2026-10-22-before-all-restorations/data'
DEFAULT_LEDGERS = (
    'archive/pdf/1984-12/reference-r01/ledger.json',
    'archive/pdf/1985-02/reference/ledger.json',
)
DEFAULT_STAGES = 'archive/pdf/shared/evidence/reader-integration-2026-10-22/stages'


def load_february_dispatcher(root=ROOT):
    relative, expected = FEBRUARY_DISPATCHER
    path = root / relative
    if not path.is_file() or digest(path) != expected:
        raise ValueError(f'Missing or changed February dispatcher: {relative}')
    spec = importlib.util.spec_from_file_location('volunteer_february_assembly', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # Dispatcher verifies all thirteen adapter pins.
    return module


@contextmanager
def installed_adapters():
    from tools.pdf_restore import assemble, design_literal_assembly
    # Import while core functions are unchanged: private projectors retain their
    # original native-validation bindings. Route only their declared formats.
    february = load_february_dispatcher()
    with design_literal_assembly.installed():
        install_adapters()
        common_project, common_validate = assemble.project, assemble.validate_recipe
        try:
            def project(recipe, segments):
                module = february.MODULES.get(recipe.get('index_mode'))
                return module.project(recipe, segments) if module else common_project(recipe, segments)

            def validate(recipe):
                module = february.MODULES.get(recipe.get('index_mode'))
                return module.validate_recipe(recipe) if module else common_validate(recipe)

            assemble.project, assemble.validate_recipe = project, validate
            yield
        finally:
            assemble.project, assemble.validate_recipe = common_project, common_validate


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
    parser.add_argument('--base', type=Path, default=ROOT / DEFAULT_BASE)
    parser.add_argument('--ledger', type=Path, action='append', help='Issue ledger; repeat in staging order')
    parser.add_argument('--stages', type=Path, default=ROOT / DEFAULT_STAGES)
    parser.add_argument('--data', type=Path, default=ROOT / 'dist/reading-room-volunteer/data')
    args = parser.parse_args()
    with installed_adapters():
        if args.action == 'export':
            from .scan_issue import stage_issue
            ledgers = args.ledger or [ROOT / p for p in DEFAULT_LEDGERS]
            destinations = [args.stages / f'stage-{i + 1:02}/data' for i in range(len(ledgers) - 1)] + [args.data]
            if any(p.exists() for p in destinations):
                raise ValueError('Use fresh reader and intermediate outputs')
            base = args.base
            for ledger, destination in zip(ledgers, destinations, strict=True):
                print(f'Staging {ledger} into {destination}', flush=True)
                result = stage_issue(base, ledger, destination)['counts']
                base = destination
        else:
            from .check import check
            result = check(args.data, require_thumbnails=True)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
