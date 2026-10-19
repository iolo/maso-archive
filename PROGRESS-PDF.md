# PDF restoration progress

Updated 2026-10-20. This file is the status index; detailed records live under
[`docs/progress/`](docs/progress/README.md), grouped by **magazine issue**, not
by the calendar month in which restoration work happened.

## Current status

December 1984 is in progress: nine readable articles, one partial article,
two non-owning headings and 25 of 37 entries unresolved. BASIC speed0011 is
restored over 102–107/PDF104–109 of its verified full102–109/PDF104–111. The
following CP/M(5) starts110/PDF112; the education divider precedes102 atPDF103.
Canonical identities, titles and parent links remain unchanged.

The162-file native export and independent rebuild are byte-identical. It retains
45regions,100blocks,nine original images,108regional text spans,138text reviews,
30text notes andeight prose joins. Four listings retain29physical rows,25numbered
entries,four wraps,six quoted strings andnine source notes. Three tables retain
15data rows,16including headers,109cells and15blanks. Nine figure-caption links,
four listing-caption links and131inline examples have exact source occurrences.

All45original andthree revised exact crops were inspected before36successful
mapped Tesseract tasks. Three clipped edges were widened once each before OCR;
no recognition failure/retry or post-OCR repair. Twelve whole pages were reviewed,
with six outside-map lookups;four pinned renders reused,eight newly rendered.
Thekeymatrix OCR drafts are poor/empty;every table cell was transcribed directly
from scans. All19,252prior evidence files are unchanged;new inventory:19,908files.
Shared175-test baseline andall16historical implementation pins remain unchanged.

Source8008Akey infigure3 differs from8001inprose/figure4;BEE differs fromBEEP;
parenthetical&H0FFFF differs from&H0FFF. All remain literal. Blank key boxes,
uncertain matrix glyphs,physical COUNT/STOP/quoted-string wraps,inline FOR wrap
andUnicode return/arrow approximations remain explicit. No encoding,hardware,
arithmetic,syntax,opcode or execution reconstruction. The first verifier's wrong
file-count assumption andfresh fix are retained;source/export bytes are unchanged.

Next: batch19,restore ending108–109with lists5/6,then independently assemble the
full102–109article. Reuse/reinspect pinned whole scans before mapping andevery
exact original/revised crop before OCR. Future selected-package/issue-closeout
checks including complete Crowded Speedway88–97(final69F8) must use the explicit
`tools.pdf_restore.table_literal_assembly.check` or `installed()` context.
Human acceptance/full proofreading,source bytes andexecution remain unverified.
No reader/frontend work.

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
| 1984-12 | 10 | 9 readable; 1 partial; 2 non-owning headings; 25 TOC entries unresolved | [8412](docs/progress/8412.md) |

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
