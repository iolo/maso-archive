# November 1984 — donated scan restoration

[Campaign plan](../../PLAN-SCAN-RESTORATION.md) · [Progress](../../PROGRESS-SCAN-RESTORATION.md)

## Current outcome

Forty canonical TOC identities are queued. No article is restored yet. The
editorial `maso-1984-11-toc-0034` is located on printed/source page 17, between
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
