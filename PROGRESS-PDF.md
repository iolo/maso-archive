# PDF restoration progress

Updated 2026-10-20. This file is the status index; detailed records live under
[`docs/progress/`](docs/progress/README.md), grouped by **magazine issue**, not
by the calendar month in which restoration work happened.

## Current status

December 1984 is in progress: eleven readable articles, one partial perspective
simulation article, two non-owning headings and 23 of 37 entries unresolved.
The perspective article spans 19 observed pages131–149, PDF133–151. Its narrative
closing mark on140 is followed by AppleSoft141–144 and GBASIC144–149; the last
listing ends4290 END on149. The opening title/cube/byline 고일두 is onright131;
the left office-move advertisement is separate. No global folio offset is inferred.

Opening131–136 is restored at packages/perspective-a. The native and independent
rebuild reproduce all148 files exactly:40 regions,33 blocks,seven original drawings,
39 regional text spans,six source joins and16 unnumbered MOVE/DRAW physical rows.
Sixty-four code tokens retain subscripts as Unicode visual candidates. No numbered
BASIC entries are inferred. Printed137–149 and the complete article assembly remain.

The mathematical indexes retain26 display/context spans,20 matrices,74 matrix rows,
264 literal cells,15 fractions,296 math glyphs,four equation labels and959 inline
occurrences. Diagram indexes retain101 observed label tokens and seven captions
across six captioned frames. One original frame carries separate6.1/6.2 captions;
the opening cube has no observed caption. Original two-dimensional layouts survive
in all40 region images. Textual brackets,spacing,slash fractions and label order are
editorial representations;mathematical correctness and source bytes are unverified.

Source anomalies remain:219/2000=0.1395,the three-component scaling input vector,
the first reflection matrix's two negative entries,the symbolic view matrix's final0
and clipping prose's ad remainder. General matrix g/q,perspective γ/r,looped ℓ/l,
subscript t/i,decimal/coordinate punctuation and other faded glyphs remain explicit
visual candidates. No arithmetic,formula,semantic or graphic reconstruction.

All23 whole/review pairs and40 original/23 revised crops were inspected before33
successful mapped Tesseract tasks. Six mapped pages,17 outside-map lookups,20 new
renders andthree original render reuses. No recognition failures/retries orpost-OCR
crop repairs. The failed advertisement-map metadata attempt and initial display-line
index selector remain preserved;fresh scripts reuse completed source review/readings.
All27,541 prior files and20 historical plus3 CP/M implementation pins are unchanged.
New preservation inventory:28,226 files. All193 PDF tests pass. No shared tooling changes.

CP/M(5) remains complete at packages/cpm5-complete-r01:all21 PDF112–132 pages,
observed110–129 plus an unpaginated upper reference continuation;lower132 ad separate,
no observed130. Its904-file assembly retains all895 native files and every specialized
index/metadata field. BASIC speed102–109 remains complete from opening102–107 and
ending108–109. All selected-package/issue checks must use cpm_literal_assembly.check
or its installed() context,which installs/delegates graphic_literal_assembly for older
formats. The CP/M-specific adapter is not a generic perspective-formula adapter.

Next: batch25,perspective137–142,PDF139–144. This includes clipping/composite
transforms,flowchart,variables,usage,data/output examples and the first two AppleSoft
listing pages. Recheck the full extent/neighbors and every exact crop beforeOCR;
preserve all native formula/matrix/cell/fraction/glyph/equation/diagram/captionpart/
physical/code/review indexes and metadata for later assembly. Keep checkpoints within
two articles,six mapped pages and20 outside-map lookups. Human acceptance,full
proofreading,original encoded bytes,execution and mathematics remain unverified.
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
