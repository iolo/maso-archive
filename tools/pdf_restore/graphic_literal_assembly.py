"""Explicit assembly/check entrypoint for unverified graphic, font, hex and table source fields.

The adapter is installed only for the duration of the requested operation.
Historical projectors and native packages stay unchanged. Outputs retain the
opt-in in both original segment metadata and the combined correction format.
"""
import argparse
from contextlib import contextmanager
from pathlib import Path

from . import assemble as assembly
from .assembly_indexes import Segment
from .assembly_graphic_literals import project_graphic_literals
from . import table_literal_assembly as table_assembly
from .build import check_export

_BASE_PROJECT = table_assembly.project
FORMAT = 'graphic_table_source_fields_format'


def project(recipe, originals):
    flags = []
    for _, correction in originals:
        metadata = correction.get('manual_postproduction')
        flags.append(metadata.get(FORMAT) if isinstance(metadata, dict) else None)
    if not any(flag is not None for flag in flags):
        return _BASE_PROJECT(recipe, originals)
    if (any(flag != 'v1' for flag in flags) or
            recipe.get('index_mode') != 'wrapped-listing-v1' or
            recipe.get('prose_joins') or recipe.get('wrapped_listing_joins') or
            any('basic_source_fields_format' in c or
                (c.get('manual_postproduction') or {}).get('literal_source_fields_format') is not None or
                (c.get('manual_postproduction') or {}).get('literal_table_source_fields_format') is not None
                for _, c in originals)):
        raise ValueError('Graphic literals require uniform v1 wrapped segments without cross-segment joins')
    package, corrections = _BASE_PROJECT(recipe, originals)
    _, listing = assembly.text_bytes(package)
    offset = 0
    for spec, (source, correction) in zip(recipe['segments'], originals, strict=True):
        context = Segment(spec, source, correction, offset)
        project_graphic_literals(context, corrections, listing)
        offset += len(context.listing)
    return package, corrections


@contextmanager
def installed():
    """Temporarily enable exact projection during both export and offline check."""
    previous = assembly.project
    assembly.project = project
    try:
        yield
    finally:
        assembly.project = previous


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
    print(f"Graphic-literal assembly: {package['id']} / {package['availability']}")


if __name__ == '__main__':
    main()
