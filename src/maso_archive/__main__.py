"""Repository CLI; see docs/TOC-IMPORT.md and docs/CD1-INDEX.md."""

import argparse
from pathlib import Path
import sys

from .toc import ImportFailure, run_import
from .cd1_index import run_import as import_cd1_index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    toc = commands.add_parser("import-toc", help="Import the supplied Markdown TOC")
    toc.add_argument("--source", type=Path, default=Path("TOC.md"))
    toc.add_argument("--output", type=Path, default=Path("build/toc"))
    toc.add_argument("--identities", type=Path, default=Path("data/identities/toc.json"))
    toc.add_argument("--decisions", type=Path, help="Explicit ID reuse/deletion decisions")
    toc.add_argument("--start", default="1983-11")
    toc.add_argument("--end", default="1990-12")
    index = commands.add_parser("import-cd1-index", help="Import the three extracted CD1 indexes")
    index.add_argument("--source-dir", type=Path, default=Path("private/cd1-probe/raw"))
    index.add_argument("--manifest", type=Path, default=Path("private/cd1-probe/manifest.json"))
    index.add_argument("--output", type=Path, default=Path("build/cd1-index"))
    args = parser.parse_args()
    try:
        if args.command == "import-cd1-index":
            report = import_cd1_index(args.source_dir, args.manifest, args.output)
        else:
            report = run_import(
                args.source, args.output, args.identities,
                decisions_path=args.decisions, start=args.start, end=args.end,
            )
    except ImportFailure as exc:
        print(f"Import rejected: {exc}. See {args.output / 'failed-import-report.json'}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as exc:
        print(f"Import failed: {exc}", file=sys.stderr)
        return 1
    counts = report["counts"]
    if args.command == "import-cd1-index":
        print(
            f"Imported {counts['entries']} index entries from {counts['source_files']} files; "
            f"{counts['distinct_references']} distinct targets "
            f"({counts['numeric_references']} seven-digit references). "
            f"{counts['diagnostics']} review notices. Output: {args.output}"
        )
    else:
        print(
            f"Imported {counts['issues']} issues, {counts['entries']} TOC entries, "
            f"{counts['article_candidates']} article candidates. "
            f"{counts['diagnostics']} review notices. Output: {args.output}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
