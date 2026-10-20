# PDF restoration progress

Updated 2026-10-20. This file is the status index; detailed records live under
[`docs/progress/`](docs/progress/README.md), grouped by **magazine issue**, not
by the calendar month in which restoration work happened.

## Current status

December 1984 is in progress: thirteen readable articles, no partial articles,
two non-owning headings and 22 of 37 entries unresolved. The MSX machine-code
loader0014 is now complete over observed150–151/PDF152–153 at packages/msx-loader.
Its53-file native and independent rebuild match exactly. The article starts with
its own title after perspective149 andends8070 RESUME1150 before mathematics152.
All five whole views151–155 were inspected;no globalfolio offset was assumed.

The MSX native retains14 regions,eight blocks,four uncaptioned original images
(three boxed listing frames andthe publisher closing mark),ten regional spans
and16 source review notes. All14 original andone revised exact crop were inspected
before ten successful OCR tasks. One closing-prose crop was widened below its
last baseline before OCR. OEM1/PSM6,one thread,3000-long-edge,eng code/kor+eng prose
remain pinned. No recognition failure,retry orpost-OCR repair. Four full/review
pairs were reused andone new source page rendered;two mapped pages,three outside
lookups. One source-direct correction pass;all raw drafts/maps/crops retained.

The continuous listing retains147 physical rows and134 actual numbered entries,
including1045/1055/1065/1075/4015/5091. Printed3180/3190 after3150 andthe4090→4120
gap remain;no3160/3170/4100/4110 were supplied. All physical wraps remain,including
C/M$,S/TART,L/AST,quotedzero,MS/X,3/2),ERROR/newline100,EL/SE andquoted i/n line.
Source6030 >= and6530 > stay independent. No syntax,firmware,hex,arithmetic or
encoding repair,executable flattening orsemantic reconstruction.

Indexes retain763 tokens,368 identifiers,221 numeric fragments,1,265 punctuation
candidates,43 leading comment glyphs,21 decorative runs,123 quote/comment glyphs,
39 paired strings,34 reference clauses/target fields,44 function tokens and685
inline occurrences. Four command headings D/S/G/@,six literal hex examples and
four quoted character bounds are indexed without decoding. Prose • is retained
as a dot/bullet candidate independently ofcode4190's quoted period. Decorative
run widths,quotedspaces/dots,apostrophes,@,Q/O,0/O and1/I remain uncertain.

The source credit reads 박 재 현 / 박재현 candidate on151;the TOC names박제현.
Both are retained independently in source_byline_index andthe ledger. Canonical
identity,title,parent andTOC metadata remain unchanged. No printed frame captions
were observed;none were invented from article title orprogram comments.

All30,256 prior files and26 implementation pins remain unchanged. The new
preservation inventory has30,501 files. The unchanged203-test baseline is reused
without rerunning tests. A fresh index revision adds brackets/@/!/caret/backslash
coverage andthe prose stopmark range without changing source readings/other
indexes. Initial correction/recipe/stat files remain. An initial ledger finalizer
failed onan absent evidence list;its script/record/snapshot remain. The fresh
finalizer initializes only that list and reuses completed schema/reproduction.
No source,OCR orexport restart. No shared tooling orreader work.

Perspective131–149 remains complete at packages/perspective-complete-r01:393 files,
all384 natives exact,one134 repair andboth10.3/10.4 captions resolved. Immutable
perspective-a,perspective-b-r01,perspective-c,perspective-d andreflectionrevision
retain all math/code metadata,including87 middle matrix cells and143–148 listings.
CP/M remains complete at packages/cpm5-complete-r01,observed110–129 plusunpaginated
upper PDF132 reference continuation;lower132 ad separate,no observed130. BASIC
speed102–109 retains opening102–107 andending108–109. All selected checks use
perspective_literal_assembly.check/installed(),which delegates cpm_literal_assembly
andgraphic_literal_assembly for older formats. Preserve all26 implementation pins.

Next:batch30,canonical mathematics/logical learning(5)0015,start152. The title,
editorial credit andseries5 are observed onPDF154;PDF155/153 continues it. Verify
the complete extent andneighbors beforemapping. A provisional PDF153–170 lookup
window andsix-page opening152–157/PDF154–159 stay within the limits;these are
candidates,not an inferred globaloffset orverified end. Keep atmostsix mapped
pages/two articles/20 outside-map lookups. Retain all mathematical source errors,
formulas,fractions,diagrams,tables andcode without arithmetic reconstruction.
Human acceptance,full proofreading,source bytes andexecution remain unverified.
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
