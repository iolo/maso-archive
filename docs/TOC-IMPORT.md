# TOC importer

The importer preserves every source bullet, proposes metadata fields, and
reports uncertainty. Its outputs are **unreviewed local working data**, not an
approved public catalog. It does not modify `TOC.md` or read extracted CD bodies.

## Run

From the repository root, use Python 3.11 or later with the dependency in
`requirements.txt` installed. A virtual environment is optional:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
make import-toc PYTHON=.venv/bin/python
make check PYTHON=.venv/bin/python
```

With a suitable existing Python environment:

```sh
make import-toc
make check
```

Equivalent CLI with explicit locations:

```sh
PYTHONPATH=src python3 -m maso_archive import-toc \
  --source TOC.md \
  --output build/toc \
  --identities data/identities/toc.json
```

The default expected period is November 1983–December 1990. For a separate test
collection use `--start YYYY-MM --end YYYY-MM`, and separate output and identity
paths. The importer interprets two-digit issue years as 1900–1999. Missing,
duplicate, out-of-scope, empty, or out-of-order issues reject the import.
Unsupported nonblank Markdown lines also reject it; source text is never silently
dropped. Blank lines are preserved indirectly by source line locations/hash,
rather than represented as catalog entries.

## Outputs and preservation

| Path | Purpose |
| --- | --- |
| `build/toc/issues.json` | Issue records with original labels, provenance, and coverage state. |
| `build/toc/toc-entries.jsonl` | All nested entries, exact raw text/lines, field candidates, IDs, and review flags. |
| `build/toc/article-candidates.jsonl` | Provisional articles and feature bundles, linked to their TOC entries. |
| `build/toc/validation-report.json` | Counts, per-issue coverage, and diagnostics tied to entry IDs/source lines. |
| `build/toc/local-search.json` | Searchable metadata preview for every entry, including sections and page-less subtopics. |
| `build/toc/manifest.json` | Source, schema, identity-map, and output hashes; importer/Python/dependency versions and scope. |
| `data/identities/toc.json` | Durable, version-controlled ID allocator and active/retired entry mapping. |

`build/` is disposable and ignored by Git. **Keep the identity map**: it allows
rebuilding outputs without renumbering records. Restore it from Git if lost.
Generated records must not be edited as a review workflow; later reviewed
catalog records and field corrections belong in separate versioned data.

All issue/entry/candidate/search records, the successful validation report, and
the identity map are validated against `schemas/toc-import.schema.json` before
successful outputs are replaced. The importer also checks relationship targets
and ID allocation invariants. Files are replaced atomically one at a time after
validation; this is not a multi-file database transaction. The manifest's hashes
allow an interrupted/inconsistent output set to be detected and rebuilt.

Reimporting the same source with the same identity map, code, schema, and runtime
produces byte-identical files. No wall-clock timestamp is injected into generated
records. Dates of completed work are recorded in `PROGRESS.md`; bump the importer
version when its output semantics change.

Validation/identity failures exit nonzero, write `failed-import-report.json`,
and leave the previous successful output set and identity map untouched. A
successful rerun removes the obsolete failure report. Filesystem failures are
reported on stderr and may require rerunning to finish a partially written set.

## Parsing and interpretation

- Two-space nesting defines the normal hierarchy. Suspicious indentation is
  retained and flagged, with the nearest lower-indentation entry as its proposed
  parent. Original global order, sibling order, indentation, and source line are
  stored independently of printed page numbers.
- A trailing `= number` is a page candidate. Comma/space-separated page lists
  remain a list, with a null start page. Unrecognized page syntax is retained
  verbatim and flagged. No end pages or page inheritance are inferred.
- A single spaced slash separates a title/byline candidate. Embedded slashes in
  `CP/M` and `S/W` survive unchanged. Multiple spaced slashes are ambiguous and
  are retained in the title for review. Semicolon-separated byline parts remain
  literal contributor candidates; no person/organization/role normalization is
  attempted. Even a syntactically valid byline requires verification.
- A parent without a page/byline is a section candidate. A parent with those
  fields is a possible bundle/article. Leaf entries with a page marker or byline
  become article candidates, which can include notices, comics, and editorial
  matter. A page-less leaf is not automatically counted as an article.
- The local search preview normalizes Unicode to NFC and case-folds the title,
  byline, and issue date. Display text retains the original spelling. No aliases,
  summaries, inferred authors, or CD source matches are invented.

Candidate classification and review notices are not judgments that the TOC is
wrong. Sections legitimately lack pages, and magazines often list articles in
an order different from their printed page sequence.

## Stable identities and explicit decisions

IDs such as `maso-1988-01-toc-0001` are allocated once. The corresponding article
candidate uses `maso-1988-01-article-0001`. New insertions receive the next unused
serial in that issue; they do not renumber following entries. Source line numbers
are evidence locations, not permanent identities.

Unchanged unique raw text within an issue reuses its ID even when moved. Repeated
identical entries reuse occurrence order only when the entire issue's sequence
and hierarchy are unchanged. Changed text, ambiguous duplicates, and removals
require explicit decisions rather than fuzzy or positional guesses.

For a title correction, first run the importer to get its failure report. Write
a versioned decision file, for example `data/overrides/toc-correction.json`, with
the SHA-256 of the **updated** `TOC.md`:

```json
{
  "source_sha256": "REPLACE_WITH_64_CHARACTER_SHA256",
  "assignments": {"42": "maso-1988-01-toc-0001"},
  "removed_ids": [],
  "new_lines": []
}
```

The example assigns the entry on source line 42 its existing identity. Run:

```sh
sha256sum TOC.md
PYTHONPATH=src python3 -m maso_archive import-toc \
  --decisions data/overrides/toc-correction.json
```

Use `removed_ids` to acknowledge deletions; retired IDs are never reused. When
adding an intentionally identical duplicate, explicitly assign the old ID to its
correct line and list the new entry's line in `new_lines`. Ordinary unique new
entries do not require decisions. Decisions for another source hash are rejected.
Commit the correction/decision file, updated identity map, and progress entry
together. Subsequent unchanged imports do not need the decisions file.

## Initial results and checks

The supplied TOC imports as 86 issues and 3,811 entries, with 2,975 article
candidates. Of those, 199 are possible bundles rather than clear leaf articles.
There are 409 section candidates, 418 subtopics, and nine other unknown entries.
These categories preserve the original list; they are not a final article census.

The report contains 2,068 notices: 1,118 absent page markers, 12 multiple-page
references, nine empty bylines, 301 decreases in page order, 199 possible bundles,
427 uncertain entry kinds, and two repeated-title groups. The earlier inspection's
1,129 entries without a final single-number marker used a different textual
counting rule; the report now distinguishes absent markers and page lists.

Tests cover hierarchy and raw-line fidelity, multiple contributors, embedded and
ambiguous slashes, missing/multiple/unsupported pages, page ordering, stable IDs
across insertions and corrections, explicit duplicate/deletion decisions, retired
IDs, stale decisions, missing/corrupt registries, rejected input preservation,
schema enforcement, deterministic output, and complete import of the real TOC.

Next work: complete durable disc inventory manifests, then normalize a CD1 RTF
sample and reconcile its topics with these candidate records. This importer does
not complete every item in Milestone 1 or replace human review.
