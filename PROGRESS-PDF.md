# PDF restoration progress

Updated 2026-10-20. This file is the status index; detailed records live under
[`docs/progress/`](docs/progress/README.md), grouped by **magazine issue**, not
by the calendar month in which restoration work happened.

## Current status

December 1984 is in progress: nine readable articles, one partial article,
two non-owning headings and 25 of 37 entries unresolved. Both BASIC speed natives
now cover full 102–109/PDF104–111. The ending 108–109/PDF110–111 is restored;
the article remains partial pending an independent complete assembly.

The 57-file ending export and independent rebuild are byte-identical. It retains
15 regions, nine blocks, four original images, 14 regional text spans and 18 text
reviews. Lists 5/6 retain 201 physical rows, 123 numbered entries, 78 wraps,
25 quoted strings, ten literal DATA fields, 146 hex literals, 18 font definitions,
24 graphic candidates and 22 editorial markers. Every field, marker and clipped
physical source span has an independently checked UTF-8 occurrence.

Line 9100 continues from the left column to the right inside C/newline/HR$.
The &/newline/H8000 token stays split. Short &H8, &HC, &HD and &H0 spellings,
quoted borders, unknown blank widths, joined DATA glyphs and all candidates remain
literal or explicitly marked. No font decoding, key-layout inference, run-length
fill, opcode, arithmetic or execution reconstruction was performed.

All 15 exact original crops were inspected before 11 successful mapped Tesseract
tasks. Four pinned whole/review scans were reused; two mapped pages and two
outside-map lookups. No crop repair, recognition failure/retry or post-OCR crop
repair. Five supplemental source zooms support the one correction pass. All 19,908
prior evidence files remain unchanged; the new inventory contains 20,161 files.
The 175-test baseline and all 16 historical implementation pins are unchanged.

Next: basic-speed-assembly for complete 102–109. Preserve the opening's three
tables/109 cells/15 blanks and every ending graphic, font, hex, quote, DATA and
source-marker index. Existing table/literal tooling rejects the specialized graphic
category and does not project the new font/hex indexes; add an explicit compatible
projection without dropping metadata, rewriting source or changing prior pins.
No further mapping/OCR is needed. Crowded Speedway checks still require
`tools.pdf_restore.table_literal_assembly.check` or its `installed()` context.
Human acceptance/full proofreading, source bytes and execution remain unverified.
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
