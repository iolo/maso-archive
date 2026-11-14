# November 1984 — donated scan restoration

[Campaign plan](../../PLAN-SCAN-RESTORATION.md) · [Progress](../../PROGRESS-SCAN-RESTORATION.md)

## Current outcome

Forty canonical TOC identities are queued: two readable/sample-reviewed articles
and 38 awaiting disposition. The complete editorial `maso-1984-11-toc-0034` is
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
readable/sample-reviewed and matches a separate fresh-process export exactly,
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

`maso-1984-11-toc-0014` is complete and readable/sample-reviewed from printed
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
proofreading and execution remain unverified. November is incomplete: two readable
articles and 38 canonical identities awaiting disposition.

Next: R03, verify the actual ending and neighboring boundary of 애플 포트란
(`maso-1984-11-toc-0015`), whose opening is confirmed on printed/source 118.
Map at most six source views after that location check. JPEG segment assembly
and whole-issue export remain pending before they are required.
