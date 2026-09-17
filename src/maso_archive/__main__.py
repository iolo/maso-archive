"""Repository CLI; see docs/TOC-IMPORT.md."""

import argparse
from pathlib import Path
import sys

from .toc import ImportFailure, run_import


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
    args = parser.parse_args()
    try:
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
    print(
        f"Imported {counts['issues']} issues, {counts['entries']} TOC entries, "
        f"{counts['article_candidates']} article candidates. "
        f"{counts['diagnostics']} review notices. Output: {args.output}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
