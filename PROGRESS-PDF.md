# PDF restoration progress

Updated 2026-10-20. This file is the status index; detailed records live under
[`docs/progress/`](docs/progress/README.md), grouped by **magazine issue**, not
by the calendar month in which restoration work happened.

## Current status

December 1984 is in progress: ten readable articles, one partial CP/M(5)
article, two non-owning headings and 24 of 37 entries unresolved. Four immutable
CP/M natives now cover all 21 source pages, PDF112–132: observed 110–129 plus an
unpaginated upper reference-table continuation. The lower advertisement on PDF132
is separate; no folio 130 was observed. Complete article assembly remains pending.

The new ending native and independent rebuild reproduce all 63 files exactly.
Its 21 regions, 14 blocks and 10 original images retain 27 unnumbered physical rows,
25 nonblank units and 129 tokens. Fifteen compiler rows retain 45 exact cells,
including two blank object fields; object strings remain opaque source candidates.
No byte decoding, padding, opcode repair, arithmetic or execution reconstruction.

Four reference-table halves retain 118 data rows, 122 rows including headers,
366 cells, 12 category labels and 70 arrow/ditto occurrences. The CPI counterpart
is visibly blank and stays empty. Four graphic cells link to original rotation
diagrams and 36 separately indexed visible labels. Their labels are transcriptions,
not printed captions or recreated drawings. Eight table/diagram images have no
observed caption. Source mistakes, unknown glyphs, ditto marks and cell wraps remain
explicit; no manual-based instruction correction or graphic-pattern reconstruction.

All 15 regional text spans, 31 text reviews, 16 notes, 775 inline examples, two
figure-caption links, two listing-caption links and one error-list column join pass.
All 23 pinned whole-page views and 21 original/nine revised crops were inspected
before 11 successful tasks. Three mapped pages and 20 outside-map lookups; no new
rendering, recognition failure/retry or post-OCR crop repair. All 24,469 prior files
and 20 implementation pins are unchanged. New preservation inventory: 24,797 files.
The unchanged 187-test PDF baseline is reused; no shared tooling or reader work.

The four natives retain 271 regions, 195 blocks, 75 original images and 820 physical
rows. All source is available; a compatible full assembly is required. Preserve every
native transcript, editor, quote, compiler, hex/address/ASCII, table/cell/row/category,
graphic-cell/diagram-label/symbol, marker, review and caption index, including exact
zero-length blanks and original metadata. Preserve all existing multi-frame captions,
including figures 16, 34, 37 and 48. No source rewrites or index-category dropping.

Next: cpm5-assembly, using all four immutable natives. Add a compatible adapter if
needed while keeping all 20 historical implementation files unchanged. Independently
rebuild and verify the complete article, source coverage and canonical accounting.
BASIC speed 102–109 remains complete from opening 102–107 and ending 108–109.
All selected-package checks must use `tools.pdf_restore.graphic_literal_assembly.check`
or its `installed()` context, which also handles Crowded Speedway. Human acceptance,
full proofreading, source encoded bytes and historical execution remain unverified.
No reader rebuild.

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
