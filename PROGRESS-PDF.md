# PDF restoration progress

Updated 2026-10-20. This file is the status index; detailed records live under
[`docs/progress/`](docs/progress/README.md), grouped by **magazine issue**, not
by the calendar month in which restoration work happened.

## Current status

December 1984 is in progress: ten readable articles, no partial articles,
two non-owning headings and 25 of 37 entries unresolved. BASIC speed is complete
over 102–109/PDF104–111, combining opening102–107 and ending108–109. Its238-file
assembly and both167/62-file metadata-only revisions reproduce byte-for-byte.
Every219original native file and every original correction value remains preserved.

The combined package retains60regions,109blocks,13images,230physical rows,
148numbered entries,82wraps,31quotes,ten DATAfields,146hex literals,18font units,
24graphic candidates/22markers,three tables/109cells/15blanks,137inline examples,
11figure-caption links,six listing-caption links andeight native prose joins.
Every source occurrence andnested marker/scan range is projected exactly. Original
source mistakes,glyph candidates,unknown widths andshort literals remain unchanged.

Separate explicit graphic/table/font tooling (4e77db4) passes187PDF tests andtwelve
focused tests. All16historical implementation pins andfour historical assembly
audits pass unchanged. The failed first real-source probe exposed a two-scan
uncertainty record;its original code/report andthe cross-scan regression/fix remain
preserved. Two verifier NameErrors andfresh fixes also remain;no export changed.
All20,161prior evidence files are unchanged;new preservation inventory:21,160files.
No new mapping,rendering,OCR orsource correction was needed for assembly.

Future selected-package/index/issue-closeout operations including BASIC speed must
use `tools.pdf_restore.graphic_literal_assembly.check` or its `installed()` context.
It also handles the older Crowded Speedway table/literal format. See the
[graphic/font format notes](docs/PDF-GRAPHIC-LITERAL-ASSEMBLY.md). Ordinary default
checking cannot certify these specialized correction indexes.

Next: batch20,establish the full extent/neighbors of CP/M(5)0012 fromobserved
110/PDF112,then restore atmost six mapped pages. Its end is not established;
next canonical perspective simulation131is only a lookup lead. Reuse/reinspect
pinned scans;review full extent before mapping andevery exact original/revised
crop before OCR. Human acceptance/full proofreading,source bytes andexecution
remain unverified. No reader/frontend work.

See the [December record](docs/progress/8412.md) and
[ledger](metadata/catalog/pdf-restoration/1984-12-progress.json). No reader rebuild.

October 1984 is complete under the canonical TOC JSON/assets scope: 35 readable,
assistant sample-reviewed articles and six non-owning headings account for all 41
entries, with no partial articles or unresolved eligibility. All 260 PDF pages are
classified: 205 contain selected article bodies and 55 are other material, including
18 pages of two unlisted features. The verified cover, selected packages and
independent byte-identical issue rebuild pass; all 30,737 prior evidence files remain
unchanged. The standalone index is `archive/pdf/1984-10/reference/issue.json`;
the report is `archive/pdf/1984-10/evidence/issue-closeout/report.json`.
Human acceptance/full proofreading, source bytes and execution remain unverified;
news/classified body transcription and the batch 35 preflight timing exception remain
explicit. The restoration closeout itself did not rebuild the reader.
Ten supplied eligible issues remain after October, including December now in progress.

October's volunteer reader was subsequently built at the owner's request. The
current `dist/reading-room/` contains 329 PDF articles across nine issues plus
3,386 CD records (3,715 total). Data preservation, tests, production compilation
and browser checks pass; the October release is saved. This was a local build,
with no deployment. See [the reader guide](docs/READING-ROOM.md).

September is also complete:37 readable articles/six headings, with its
[issue index](archive/pdf/1984-09/reference/issue.json) and
[report](archive/pdf/1984-09/evidence/14-1984-09-closeout/report.json) preserved.
See the [October record](docs/progress/8410.md), [OCR handoff](PLAN-OCR.md),
[PDF plan](PLAN-PDF.md) and [successor notes](docs/SUCCESSOR-NOTES.md).

| Issue | Body articles | Availability | Detailed progress |
| --- | ---: | --- | --- |
| 1983-11 | 35 | 35 readable | [8311](docs/progress/8311.md) |
| 1984-02 | 37 | 37 readable | [8402](docs/progress/8402.md) |
| 1984-03 | 38 | 37 readable, one terminal missing-source partial | [8403](docs/progress/8403.md) |
| 1984-05 | 36 | 36 readable | [8405](docs/progress/8405.md) |
| 1984-06 | 38 | 38 readable | [8406](docs/progress/8406.md) |
| 1984-07 | 36 | 36 readable | [8407](docs/progress/8407.md) |
| 1984-08 | 37 | 37 readable | [8408](docs/progress/8408.md) |
| 1984-09 | 37 | 37 readable; canonical TOC complete | [8409](docs/progress/8409.md) |
| 1984-10 | 35 | 35 readable; canonical TOC complete | [8410](docs/progress/8410.md) |
| 1984-12 | 10 | 10 readable; 0 partial; 2 non-owning headings; 25 TOC entries unresolved | [8412](docs/progress/8412.md) |

No April 1984 PDF was supplied. Completed accounting and usable coverage are
separate: March's absent printed pages 250–251 remain explicit.

## Cross-issue records

- [Foundations and contrasting pilots](docs/progress/foundation.md)
- [Catalog, scope, tooling and cost decisions](docs/progress/campaign.md)
- [OCR experiment progress](docs/progress/ocr-experiments.md)
- [Full experiment-history index](docs/history/README.md)

The reorganization preserves all **489 original sections**, their order within
each destination, evidence paths and measurements. Heading levels and relative
Markdown links were adjusted for the hierarchy. [Migration provenance and
section lookup](docs/progress/migration.json) map every old section to its new
location and record original/content hashes. No restoration output was changed.

## Updating progress

Append bounded checkpoint notes to `docs/progress/YYMM.md` for the issue being
restored. For a new issue, add a current-outcome summary and a checkpoint-records
section, then add it to the [directory index](docs/progress/README.md). Update
this status table and next step at issue milestones; do not append detailed
batch histories here. Keep measurements and package pins in their existing
machine-readable ledgers, and link them from the issue page.

Record cross-issue decisions in the appropriate shared file. Preserve historical
claims as dated observations; earlier “next” instructions are not a current queue.
A future cleanup must preserve the source records and update affected links.
