# November 1984 — donated scan restoration

[Campaign plan](../../PLAN-SCAN-RESTORATION.md) · [Progress](../../PROGRESS-SCAN-RESTORATION.md)

## Current outcome

Forty canonical TOC identities are queued: one readable/sample-reviewed article
and 39 awaiting disposition. The complete editorial `maso-1984-11-toc-0034` is
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
