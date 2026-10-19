# PDF restoration progress

Updated 2026-10-20. This file is the status index; detailed records live under
[`docs/progress/`](docs/progress/README.md), grouped by **magazine issue**, not
by the calendar month in which restoration work happened.

## Current status

December 1984 is in progress: ten readable articles, one partial CP/M(5)
article, two non-owning headings and 24 of 37 entries unresolved. CP/M opening
110–115/PDF112–117 is restored. Its full source spans PDF112–132: observed
folios 110–129 plus an unpaginated final reference-table continuation. The lower
bookshop advertisement on that scan is separate. No folio 130 was observed.

The 337-file opening package and independent rebuild are byte-identical. It retains
100 regions, 81 blocks, 24 original images, 216 unnumbered physical transcript rows,
213 transcript units, 1,295 literal tokens, 77 dump rows, 816 literal fields and
48 printed ASCII columns. One FDOS table retains 24 cells. Exact source indexes
cover 83 regional text spans, 138 text reviews, 55 notes, 377 inline examples,
22 figure-caption links, 21 listing-caption links and two prose joins. Four visible
quote marks, 11 code unknown markers and nine prose unknown markers remain explicit.
Source mistakes, faint glyphs and binding-hidden text remain candidates; no opcode,
ASCII, arithmetic or program reconstruction. Figure 16 starts on 115 and continues
on 116, where its caption appears. Hexadecimal addresses are source labels.

All 24 whole-page views, 100 original crops and 25 once-revised crops were inspected
before 76 successful mapped Tesseract tasks. Six mapped pages and 18 outside-map
lookups; 20 new renders and four reused renders. No recognition failure, retry or
post-OCR crop repair. The initial index classifier confused a NEXT PC response with
a dump; its failed script and fresh fix remain. The first inventory pinned its
still-open finalizer log. That inventory, terminal log, exception and fresh selected
22,490-file inventory remain. All 21,160 prior files and 20 implementation pins are
unchanged. The existing 187-test PDF baseline is reused; no shared tooling changed.

BASIC speed 102–109 remains complete from opening 102–107 and ending 108–109.
Selected-package/index/issue-closeout checks must use
`tools.pdf_restore.graphic_literal_assembly.check` or its `installed()` context;
it also handles Crowded Speedway. Preserve every CP/M transcript, field, ASCII,
marker, table, review and caption index in a future compatible full assembly.

Next: batch21, CP/M middle116–121/PDF118–123. Reinspect pinned full-source and
neighbor scans and every exact original/revised crop before OCR. Later122–129,
unpaginated PDF132 and complete assembly remain. Human acceptance, full
proofreading, source encoded bytes and execution remain unverified. No reader work.

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
