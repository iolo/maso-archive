# PDF restoration progress

Updated 2026-10-20. This file is the status index; detailed records live under
[`docs/progress/`](docs/progress/README.md), grouped by **magazine issue**, not
by the calendar month in which restoration work happened.

## Current status

December 1984 is in progress: eleven readable articles, no partial articles,
two non-owning headings and 24 of 37 entries unresolved. CP/M(5) is complete under
the JSON/assets scope at packages/cpm5-complete-r01. All 21 source pages PDF112–132
are included: observed 110–129 plus an unpaginated upper reference continuation.
The lower PDF132 advertisement is separate; no folio 130 was observed.

The complete article, export probe and independent rebuild reproduce all 904 files
exactly. All 895 files from the four native packages remain byte-identical. The
assembly retains 271 regions, 195 blocks, 75 original images and 820 unnumbered
physical rows. Every native correction field survives in original metadata; every
native array category is projected. All 13,674 range occurrences, including 79
zero-width occurrences, preserve their source bytes and positions within the
combined article/listing coordinate systems. Native source text stays unchanged.

The complete indexes retain 390 table cells with one blank CPI counterpart,
183 compiler data cells with 39 blanks, four original-graphic cells, 36 diagram
labels, 12 table categories and 70 arrow/ditto occurrences. Figure 16's opening115
frame shares the observed ending116 caption; the new link is explicitly assembly-
derived. Figure34/37/48 ownership remains intact. There are 66 figure-caption links,
61 listing-caption links and nine uncaptioned originals. Labels are not synthetic
captions or recreated drawings. No semantic, opcode, arithmetic, encoding or graphic
reconstruction; printed mistakes and visual candidates remain unverified.

The opt-in adapter was committed as61ce1ce. All 193 PDF tests pass, including six
focused regressions. The first real-source probe caught a derived caption link
classified as a native row; its prototype and failure remain. The corrected probe
passes every native category and metadata comparison. All 24,797 prior files and
20 historical implementation pins are unchanged. New preservation inventory:
27,541 files. No new OCR, source correction, mapping, rendering, crop or reader work.

Use `tools.pdf_restore.cpm_literal_assembly.check` or its `installed()` context for
all selected-package and issue checks. It installs/delegates the existing
`graphic_literal_assembly` dispatcher for BASIC speed, Crowded Speedway and other
older formats. Three new adapter/test/document pins are separate from the 20
unchanged historical pins. See docs/PDF-CPM-LITERAL-ASSEMBLY.md for the format.
BASIC speed 102–109 remains complete from opening102–107 and ending108–109.
Human acceptance, full proofreading, original encoded bytes and execution remain
unverified. No reader rebuild.

Next: batch24, canonical0013 perspective simulation. Its opening on PDF133 visibly
shows131 with the title/cube/byline onright; the left advertisement is separate.
Verify its actual full extent and neighbors before mapping a bounded opening.
Provisional candidates PDF133–138 do not establish a global folio offset or ending.
Keep each checkpoint within two articles, six mapped pages and20 outside-map lookups.

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
