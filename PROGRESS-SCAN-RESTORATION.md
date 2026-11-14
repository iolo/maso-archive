# Donated scan restoration progress

Updated 2026-11-14. Follow [PLAN-SCAN-RESTORATION.md](PLAN-SCAN-RESTORATION.md).

## Current status

**R00 complete; the November 1984 editorial is located and ready for OCR.** The 24 cleaned source sets
are complete under [PROGRESS-SCANS.md](PROGRESS-SCANS.md). Their 6,070 JPEGs are
inputs, not restored articles.

The checked current TOC snapshot supplies 1,119 identities and 919 provisional
article candidates across these dates. Twenty-two dates add coverage beyond the
supplied PDFs; February and March 1984 are supplementary-source cases. Final
body counts and per-article availability remain undetermined.

| Checkpoint | Status | Next result |
| --- | --- | --- |
| R00 — scan input integration | Passed | 246 pinned JPEG inputs, forty TOC identities, shared OCR/native export and PDF regressions checked |
| R01 — November short prose pilot | Located; OCR pending | Editorial `maso-1984-11-toc-0034` is complete on printed/source page 17 |
| R02 — contrasting November layout | Not started | Qualify listing/table/figure handling before scaling |
| November 1984 issue closeout | Not started | All forty canonical TOC identities accounted for, with checked JSON/assets |

## Planning checkpoint — 2026-11-14

Reviewed the completed cleanup index/audit, current TOC snapshot and existing
PDF/OCR contracts. Verified the TOC snapshot's output hashes against its manifest
and its source/identity pins. Confirmed the existing OCR input path renders PDFs
and the article map schema requires PDF indices and geometry; direct scan input
needs implementation rather than a renamed PDF recipe.

Saved a separate scan restoration plan, preserving the completed cleanup and
PDF campaign records. Chose November 1984 for the first pilot and identified a
later targeted March 1984 check for the PDF's absent printed folios 250–251.
No OCR, source-image transformation, restoration export or reader rebuild ran.

The owner clarified that the same `PLAN-OCR.md` pipeline applies to these scans
and that it must remain reusable under `PLAN-PDF.md` for future PDF donations.
Updated this scan plan to limit new implementation to JPEG input integration and
necessary source metadata. Neither shared plan was edited. Existing OCR policy,
runtime, review procedure and PDF input support remain the baseline; this is not
a separate OCR pipeline or a new engine-selection exercise.

## R00 completed — 2026-11-14

The existing mapped Tesseract and native article exporter now accept explicit
version-2 JPEG source maps. PDF version-1 behavior is preserved: all 214 existing
PDF tests passed, plus three new JPEG tests (including four orientations).
Reviewed July order overrides and a real February foldout also pass source checks.
Selected November inventory `input-01/inventory-r02` freezes all forty canonical
identities and TOC inputs. No OCR ran. Initial inventory/test invocation details
are retained in the R00 evidence.

See [November progress](docs/progress/scans-8411.md) and the
[input result](metadata/catalog/scan-restoration/1984-11-input.json).
Segment assembly and whole-issue export still need JPEG integration before use;
R00 establishes the shared OCR/native-article path, not a completed issue workflow.

Next: **R01**, the one-page November editorial. Keep batch history in its issue
record and leave the completed cleanup index unchanged.
