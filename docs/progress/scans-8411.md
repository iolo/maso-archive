# November 1984 — donated scan restoration

[Campaign plan](../../PLAN-SCAN-RESTORATION.md) · [Progress](../../PROGRESS-SCAN-RESTORATION.md)

## Current outcome

Forty canonical TOC identities are queued: five articles have reproducible
JSON/assets packages in the project's schema, and 35 await disposition.
All five packages are assistant sample-reviewed. Restoration preserves logical
structure, content/assets and source evidence independently of presentation;
the web reading room is a sample consumer. The existing `readable` availability
value is separate from the exact package rebuild checks recorded below.
The complete editorial `maso-1984-11-toc-0034` is
restored from printed/source page 17, between
an advertisement (16) and the separate Apple machine-language feature (18).
All three boundary views were inspected; no global filename/folio offset follows.

## R00 — JPEG input integration, 2026-11-14

Pinned all 246 November masters and preserved cleanup order and provenance.
Selected `archive/scans/1984-11/restoration/input-01/inventory-r02/` freezes the
TOC source, identity map and current snapshot inputs. Its forty-entry queue is
unclassified; no new article IDs or inferred bodies were created. The first
inventory is retained as an earlier input attempt.

The shared package validator, mapped Tesseract command and native JSON/assets
exporter accept version-2 JPEG maps with source indices, image hashes, native
pixels, reviewed reading positions and separately observed printed folios.
The existing engine, exclusions, region crops, correction and export flow are
reused. All 214 PDF tests and three new JPEG tests pass; the latest focused run
passes 23 tests. The initial missing-PYTHONPATH test invocation is recorded.
`PLAN-OCR.md`, `PLAN-PDF.md` and archived PDF/CD packages remain unchanged.

Real-source checks confirm July 1987's reordered 025–030 block and two damaged
extras, and decode February 1984's intact wide source 011. No July/February OCR
or article restoration ran. Synthetic checks cover all four orientations,
exclusion masking, coordinate round trips, source mutation and deterministic
native export. Source bytes are preserved.

Evidence: `archive/scans/1984-11/restoration/input-01/{checkpoint,source-checks,validation}.json`.
Tracked result: [1984-11-input.json](../../metadata/catalog/scan-restoration/1984-11-input.json).

R00 supports OCR and native article exports. JPEG segment assembly and whole-issue
export remain future integration tasks before those operations are needed.
Next: R01, one short editorial, one mapped page, two adjacent lookup pages already
inspected; preserve raw OCR, review every mapped region and rebuild the export.

## R01 — complete editorial pilot, 2026-11-14

Used the R00 input integration committed as `f74c4884`. One article, one mapped
source image and two previously inspected boundary lookups stay within the saved
batch scope. The initial OCR invocation selected the wrong source index (22
instead of 20) and was rejected before output or engine execution; its record is
retained. The correct invocation completed five Tesseract tasks in 3.117 engine
seconds, with zero failed regions, crop repairs, OCR retries or engine switches.

Compared all pilot reading text and six mapped regions with the full source and
exact exported crops in one source-correction pass. The orange heading/deck were
not recovered by raw OCR and were transcribed visually. Historical spelling and
source claims remain unchanged. Three reading blocks include twelve body
paragraphs. Five regional byte ranges and two joins preserve the left/right
column split inside 베이직 and the final line before the emblem. The original
emblem is an image with no invented caption or encoded-character interpretation.

The 29-file native at `archive/scans/1984-11/packages/editorial-r01/` is
assistant sample-reviewed and matches a separate fresh-process export exactly,
without rerunning OCR. All six crops match independent source pixels; all text
range bytes and reading joins validate. The original JPEG, cleanup metadata,
R00 implementation and shared OCR/PDF plans remain exact. A small external note
clarifies an overbroad pronoun-correction example in the free-text review notes;
no reading text or native package was changed.

Evidence and reproduction scripts are under
`archive/scans/1984-11/restoration/batch-01/`; the exact build/check commands and
file inventory are in `validation.json`. Raw OCR, maps, corrections, attempts and
original crops are preserved. Checkpoint elapsed time includes mapping, review,
exports and tool waits; active review time was not separately measured. A session
cleanup preview is saved; no broad deletion of other session work was applied.

Tracked result: [1984-11-editorial.json](../../metadata/catalog/scan-restoration/1984-11-editorial.json).
Issue ledger: [1984-11-progress.json](../../metadata/catalog/scan-restoration/1984-11-progress.json).
Human acceptance, character-perfect proofreading, source encoded bytes and
historical claims remain unverified. Listing/table handling, JPEG segment
assembly, whole-issue export and the remaining November identities are pending.
Next: R02; locate a bounded listing/table/figure example, with 비트 패턴 at canonical
reference 116 as a candidate, then record its exact source extent and batch scope.

## R02 — Bit Pattern, 2026-11-15

`maso-1984-11-toc-0014` has a complete, reproducible schema-based package from printed
116–117. Confirmed the visible folios, previous mathematics ending on 115 and
separate FORTRAN opening on 118. The lower-page 117 bookstore advertisement,
repeated running headers and folios are excluded. Two mapped images and two
boundary lookups stay inside the saved batch limit.

The existing mapped Tesseract pipeline processed thirteen text/code regions at
6000-pixel bounded scale, with 8.282 summed engine seconds. There were no failed
regions, OCR retries, crop repairs or engine switches. Its small listing font
produced many draft errors; one source-comparison pass covers all fourteen
eligible regions, including every text-bearing code row and table cell.

The native retains nine reading blocks, one original ending emblem, three source
listing panels, 79 physical rows and 41 numbered entries (1000–1400). Physical
wraps remain intact, including the continuation of 1090 at the top of 117.
Two unruled reference tables contain eighteen rows/thirty-six indexed cells;
row-local construction prevents repeated text from pointing to another cell.
The printed reversed range 1180~1120 and literal PROGRAMER, ADRESS, DELET and
THENWDELSE1390 remain unchanged. Quoted blanks and a 1220 unclear-tail marker have
source-linked ranges; original glyph/count and encoded bytes remain unverified.
No source code was repaired by syntax expectations or executed.

All 62 files in `archive/scans/1984-11/packages/bit-pattern-r01/` match a separate
fresh-process export without new OCR. Independent decoding/cropping proves all
fourteen source-region pixels; exact regional text, table cells, physical and
logical rows, quoted fields and the cross-page wrap validate. Six rejection
cases cover dropped rows, reused cells, wrong scans, lost continuation, altered
quoted blanks and wrong printed line numbers. Prior editorial evidence, source
masters, cleanup metadata, implementation and shared plans remain exact.
The unchanged 214-PDF/three-JPEG test baseline is retained for this data-only work.

Maps, raw OCR, correction/index records, original crops, listing-review scripts,
validation and the session-cleanup preview are preserved under
`archive/scans/1984-11/restoration/batch-02/`. No broad session deletion ran.
Elapsed time includes review, tool/conversation waits and interruption; active
review time was not separately measured.

Tracked result: [1984-11-bit-pattern.json](../../metadata/catalog/scan-restoration/1984-11-bit-pattern.json).
Native reproduction and validation commands are in the private `validation.json`.
The small ending emblem has no caption; complex illustrations, captions and ruled
tables are not certified by this sample. Human acceptance, character-perfect
proofreading and execution remain unverified. November is incomplete: two
reproducible article packages and 38 canonical identities awaiting disposition.

Next: R03, verify the actual ending and neighboring boundary of 애플 포트란
(`maso-1984-11-toc-0015`), whose opening is confirmed on printed/source 118.
Map at most six source views after that location check. JPEG segment assembly
and whole-issue export remain pending before they are required.

## R03 — final Apple FORTRAN installment, 2026-11-15

`maso-1984-11-toc-0015` has a complete, reproducible schema-based package from visibly
printed 118–121. The final-installment heading, closing text/emblem, Bit Pattern
ending on 117 and different article opening on 122 establish its scope. Four
mapped views and two outside lookups stay within the saved batch limit.

The pre-OCR crop review caught narrow wrapped-column bounds and a clipped S in
the subroutine form. The first map and two example crops are retained; the final
bounds were widened before recognition. All 55 Tesseract tasks finished in
17.333 summed engine seconds, with zero failed regions, OCR retries or engine
switches. All 57 eligible regions were compared with source in one review pass.

The native preserves fifty reading blocks, nine code blocks/78 text-bearing
rows, 33 compiler-index rows, 27 symbol rows and 100 literal numeric-output
cells. Eight field tables retain 90 rows/355 cells, including 56 blanks.
Compiler indices, offsets, labels and A continuation are distinct fields;
repeated RAD records remain separate. Twelve argument-mapping rows preserve
independent calling contexts. The output plot is a source crop with its literal
caption and an explicit shared numeric-table association; its coordinates and
asterisk counts were not inferred. The ending emblem remains uncaptioned.

Printed SUBROURINE, EP/EPS differences, Suroutine, repeated LOGICAL and I/IY/Y
references are retained. Decorative marks, ellipsis counts, faint relation
marks, slash/1 references and compiler-format blank counts have 27 local markers.
Numerical values and the compiler's 33-lines/0-errors report are historical print,
not new arithmetic or execution validation. Source encoding, exact typesetting
whitespace, program correctness and human acceptance remain unverified.

The first export inherited code-font OCR tags for numeric/symbol/output data.
That candidate and a reproducible input snapshot are retained. The selected
`archive/scans/1984-11/packages/apple-fortran-r02/` corrects only classification;
no source reading or OCR changed. All 231 selected files reproduce identically
in a fresh process. Ten rejection cases include collapsed RAD records, filled
blanks, altered output values, swapped compiler fields, caption IDs, lost prose,
wrong scans, missing uncertainty and the actual first classification candidate.
All 57 crops match separately decoded source pixels. Prior packages/evidence,
cleanup records, implementation and shared plans remain unchanged.

Private maps, OCR, source readings, corrections, attempts, candidate snapshot,
validators and cleanup preview are under `archive/scans/1984-11/restoration/batch-03/`.
Its evidence manifest pins every retained file; validation.json has reproduction
commands and limits. No broad session cleanup ran. Checkpoint wall time includes
mapping, review, tool/conversation waits and exports; active review time is not
separately measured. The unchanged PDF/JPEG test baseline is reused.

Tracked result: [1984-11-apple-fortran.json](../../metadata/catalog/scan-restoration/1984-11-apple-fortran.json).
November now has three reproducible article packages and 37 identities awaiting disposition.
Next: R04, locate and bound the 공모총평 candidate at canonical reference 210.

## R04 — contest commentary and entrants, 2026-11-15

`maso-1984-11-toc-0029`, 공모총평 / 성의와 자세, has a complete,
reproducible schema-based package from actual folios 210–211. Page 209 is the separate
contest notice; 212 opens SPC-CLOCK. Two mapped source images and two boundary
lookups stay within the saved scope. The top-right 편집부 credit is associated
with this article and read before its body.

Before OCR, the map review split the closing line from the emblem so that its
rectangular text crop contains only text. The first map and views are retained.
The page-210 wrapper exited 143 after producing draft files but before saving
the body completion record and timings. Its cause is unknown. The complete
heading/title outputs and settings were reused byte for byte; only the
unconfirmed body task was retried once from the same frozen crop. All interrupted
files and the explicit recovery manifest are retained. Measured durations cover
the successful retry and six page-211 tasks; a complete OCR total is unavailable.
The shared pipeline, runtime and map were not changed during recovery.

One source-comparison pass covers all ten regions and nine reading outcomes.
Six reading blocks retain the section heading, title, byline, complete body,
entrant-table heading and table. Three exact joins preserve 자신/의 at the page
break, 주석이/하나도 across columns and 계/속 at the closing line. Six submission
examples and three requirements have independent list indexes. The original
ending emblem remains an uncaptioned image.

All four headers and 36 data cells in the nine-entrant table are indexed to their
own text ranges. The two 헬리콥터 submissions remain separate by name/platform.
Printed 돐 forms, 테크니컬한. punctuation and the historical 84. 10월 / 212페이지
reference are retained. A visible dot after 황 종 태 is preserved with an explicit
punctuation-versus-incidental-mark uncertainty; no external name lookup ran.

All 45 files at `archive/scans/1984-11/packages/contest-review-r01/` match a
fresh-process export exactly. Independent source decoding verifies ten exact
crops. All regional reading bytes, the inserted column separator, table cells,
list items and joins validate. Eight invalid cases reject dropped entrants,
merged lists, lost word fragments, altered references, removed uncertainty,
invented captions, table-as-code classification and a wrong source hash.
The previous three packages/evidence, original masters, cleanup metadata,
implementation and shared OCR/PDF plans remain exact. The unchanged PDF/JPEG
test baseline is reused for this data-only checkpoint.

Private source readings, map, raw/partial OCR, recovery, correction/index records,
reproduction scripts, validation and cleanup preview are under
`archive/scans/1984-11/restoration/batch-04/`. Its evidence manifest pins every
retained batch file except itself. No broad session deletion ran. Checkpoint
wall time includes review, tool waits, recovery and export; active review time
was not separately measured. Original encoded bytes, exact typesetting
whitespace, historical claims, character-perfect certification and human
acceptance remain unverified.

Tracked result: [1984-11-contest-review.json](../../metadata/catalog/scan-restoration/1984-11-contest-review.json).
November now has four reproducible article packages and 36 canonical identities awaiting
disposition. Next: R05, verify the ending and neighbors of 기초 테크닉 코너
(`maso-1984-11-toc-0016`, reference 122) before mapping at most six source views.
JPEG segment assembly and whole-issue export still need integration before use.

## R05 — final Basic Techniques installment, 2026-11-15

The goal now covers every November article. `maso-1984-11-toc-0016`, 기초 테크닉
코너 / —시작과 끝—, is complete on actual folios 122–124, with 마지막회 and
끝내면서 confirming its final-installment scope. The preceding FORTRAN ending
on 121 and advertisement on 125 establish boundaries. Three mapped source images
and two boundary lookups remain within the checkpoint limit. Views 126/127 were
prepared during location work but not inspected or used to infer article extent.

All 27 mapped Tesseract tasks completed successfully in 13.812 summed engine
seconds. No OCR retry, map refinement or engine switch occurred. One source
comparison pass covers all 28 eligible regions, every text-bearing code row,
caption and history cell. Twenty-five schema-based blocks retain six independent
listing contexts. Their repeated numbers remain local to each example: 58
numbered entries, 64 text-bearing physical rows and two visible blank rows.
The quotation wraps and the wrapped zero under listing 1-1 line 70 remain
continuations. Six caption associations and three SPC-1000 variant associations
preserve source relationships. Seven history rows retain 21 indexed cells.

The prose joins preserve 위/치에 across columns and 성원/해준 before the final
emblem. Source 쉽상이다, 깨끗히, 스윗치/스위치, 지우고저, 게제, the history's
에니메이션 and comma/period date differences remain unchanged. The historical
Matt.2:5-7 attribution is retained without external correction. Two large
quotation blank runs have unknown counts; eight dot-matrix LO occurrences carry
local O/0 candidates. Other original bytes, spacing widths, historical claims,
execution and human acceptance remain unverified. The ending emblem is an
original image without interpreted text or caption.

An index guard caught substring LO matches inside COLOR before writing the
recipe. That failed generator and two rejected recipe-missing export invocations
are recorded; neither produced a native package. The independent verifier's
boundary list then needed newline/comma cases for actual standalone identifiers.
Both earlier verifiers are retained. These repairs changed index construction
or checking only; no source reading, OCR or selected export was replaced.

All 118 files at `archive/scans/1984-11/packages/basic-techniques-r01/` match a
fresh-process export from frozen reviewed inputs, without a presentation build.
All 28 source crops are pixel-exact. Complete regional ranges, six listing byte
partitions, physical/logical rows, captions, variant links, twelve quoted fields,
21 history cells and ten local uncertainty records validate. Twelve rejection
cases include context collapse, a fabricated wrapped-zero number, lost wraps,
wrong captions/variants, altered history cells, inferred blank counts, truncation,
invented emblem captions, wrong source pins and LO redirected inside COLOR.
The prior four packages/evidence, cleanup metadata, original scans, shared tools
and OCR/PDF plans remain exact. The existing PDF/JPEG test baseline is reused.

Raw OCR, source readings, maps, retained preflights, reproduction scripts,
validation and cleanup preview are preserved under
`archive/scans/1984-11/restoration/batch-05/`; its evidence manifest pins every
retained batch file except itself. No broad deletion ran. Checkpoint wall time
includes review, tool waits, verification and exports; active review time was
not separately measured.

Tracked result: [1984-11-basic-techniques.json](../../metadata/catalog/scan-restoration/1984-11-basic-techniques.json).
Five reproducible article packages are complete; 35 canonical identities await
disposition. Next: R06, inspect the original contents pages to classify apparent
section headings and establish feature ownership/location before further mapping.
JPEG segment assembly and whole-issue export remain pending before their use.
