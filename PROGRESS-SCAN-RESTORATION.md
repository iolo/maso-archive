# Donated scan restoration progress

Updated 2026-11-15. Follow [PLAN-SCAN-RESTORATION.md](PLAN-SCAN-RESTORATION.md).

## Current status

**R00–R05 complete: five November 1984 articles have reproducible JSON/assets
packages in the project's schema.** All five are assistant sample-reviewed. The 24 cleaned source sets
are complete under [PROGRESS-SCANS.md](PROGRESS-SCANS.md). Their 6,070 JPEGs are
inputs, not restored articles.

The checked current TOC snapshot supplies 1,119 identities and 919 provisional
article candidates across these dates. Twenty-two dates add coverage beyond the
supplied PDFs; February and March 1984 are supplementary-source cases. Final
body counts and per-article availability remain undetermined.

The restoration target is presentation-independent structured data, with source
evidence and reproducible exports. The reading room is a sample presentation.
The existing `availability: readable` value records content availability;
`verification: sample-reviewed` records review level. Reproduction is established
separately by the complete package rebuild comparisons reported below. These
labels and the preserved exports retain their existing values.

| Checkpoint | Status | Next result |
| --- | --- | --- |
| R00 — scan input integration | Passed | 246 pinned JPEG inputs, forty TOC identities, shared OCR/native export and PDF regressions checked |
| R01 — November short prose pilot | Passed | Editorial on printed/source page 17; all 29 export files reproduce exactly |
| R02 — contrasting November layout | Passed for this sample | Two-page BASIC article; 79 listing rows, 36 table cells and 62 reproducible files |
| R03 — final Apple FORTRAN installment | Passed for this sample | Four pages; compiler/symbol/output contexts, 355 table cells and 231 reproducible files |
| R04 — contest commentary | Passed for this sample | Two pages; three continuation joins, 40 table cells and 45 reproducible files |
| R05 — final Basic Techniques installment | Passed | Three pages; six captioned code contexts, 58 numbered entries, 21 history cells and 118 reproducible files |
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

## R01 completed — 2026-11-14

Restored the complete one-page November editorial from the JPEG source using the
shared mapped Tesseract pipeline. Five raw OCR outcomes, six source regions,
three reading blocks and the original ending emblem are preserved. All pilot
reading text was compared with the scans; raw OCR misses in the orange heading
and deck were corrected visually. The 29-file JSON/assets package reproduces
byte for byte in a separate process without OCR. Native JPEG/cleanup hashes,
shared plans and the R00 implementation remain unchanged.

One reproducible article package is complete; the other 39 canonical identities await
disposition. This does not complete November or qualify listing/table handling.
See the [editorial result](metadata/catalog/scan-restoration/1984-11-editorial.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).

## R02 completed — 2026-11-15

Restored 비트 패턴 on printed/source pages 116–117. The shared mapped Tesseract
pipeline produced thirteen raw region outcomes. All fourteen eligible regions,
79 text-bearing listing rows, 41 numbered entries and 36 table cells were
source-compared. The 1090 cross-page wrap, quoted blanks, printed anomalies and
one unclear trailing comment mark remain explicit. No program was executed.

All 62 native JSON/assets files reproduce exactly in a separate process without
OCR. Fourteen crops match independent source pixels; six invalid range/cell/wrap
cases reject. Existing editorial evidence, cleanup records, implementation and
shared OCR/PDF plans remain unchanged; the existing 214 PDF plus three JPEG test
baseline is retained rather than rerun for this data-only batch.

Two reproducible article packages are complete; 38 canonical identities await
disposition. This sample establishes a small listing and two unruled reference
tables; complex tables, diagrams and captions still need case-specific review.
See the [Bit Pattern result](metadata/catalog/scan-restoration/1984-11-bit-pattern.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).

## R03 completed — 2026-11-15

Restored the final 애플 포트란 installment on printed/source 118–121. Fifty-five
raw OCR outcomes support 57 source-compared regions, fifty reading blocks and
two original figures. The export preserves nine code blocks/78 text-bearing
rows, 33 compiler rows, 27 symbol rows, 100 numeric-output cells and the literal
output caption. Eight field tables retain 355 cells, including 56 blanks.

All 231 selected files reproduce exactly in a fresh process. Source/caption/range
checks and ten rejection cases pass. A pre-OCR crop refinement and a later export
classification refinement are retained; no OCR was repeated. Explicit local
uncertainties remain in decorative marks, ellipses, reference glyphs and spacing.
Source claims, numerical output, execution, encoding and human acceptance remain
unverified. The original plots were not reconstructed.

Three reproducible article packages are complete; 37 identities await disposition.
See the [FORTRAN result](metadata/catalog/scan-restoration/1984-11-apple-fortran.json).
Next at this checkpoint: **R04**, locate the short 공모총평 candidate at reference 210 and verify its
extent before mapping. The pilot remains bounded; JPEG segment assembly and
whole-issue export integration remain pending before their first use.

## R04 completed — 2026-11-15

Restored 공모총평 / 성의와 자세 on visibly printed 210–211, with the separate
contest notice on 209 and SPC-CLOCK opening on 212 as boundaries. All ten mapped
regions, nine text outcomes, three continuation joins and two numbered lists
were source-compared. The entrant table retains four headers and nine rows:
40 indexed cells, including both distinct 헬리콥터 submissions. Historical
wording, unusual punctuation and the printed date/page reference remain intact.
A visible dot after the fourth entrant's name has a local uncertainty note.

A pre-OCR map refinement separates the final text line and emblem. One page
wrapper exited 143 before saving completion evidence; the cause is unknown.
The interrupted files are preserved, completed heading/title outputs reused,
and only the unconfirmed body task retried once successfully. Missing timings
are explicit; no complete OCR-duration total is claimed.

All 45 native files reproduce exactly in a fresh process. Ten pixel-exact crops,
all reading ranges/cells and eight rejected invalid cases pass. The prior three
packages/evidence, original masters, cleanup records, shared implementation and
OCR/PDF plans remain unchanged. Four reproducible article packages are complete;
36 canonical identities await disposition. This remains a pilot, with human
acceptance and original encoded bytes unverified.

See the [contest commentary result](metadata/catalog/scan-restoration/1984-11-contest-review.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R05**, locate the complete 기초 테크닉 코너 candidate at reference 122,
verify its ending and neighbors, then map a bounded batch. JPEG segment assembly
and whole-issue export integration remain pending before their first use.

## Restoration objective clarified — 2026-11-15

The owner clarified that restoration targets reproducible, presentation-independent
packages in the project's schema, with the web reading room as a sample
presentation. Earlier progress summaries used the availability label `readable`
as shorthand for completed work; that wording understated the deliverable.
Updated the project introduction, scan plan and scan progress terminology.
The four completed pilots already include structured JSON/assets, provenance,
corrections, source-linked ranges and exact fresh-process rebuild evidence.
Availability, review level and reproduction remain separate properties. This
documentation correction does not alter schema enums or preserved packages.

## R05 completed — 2026-11-15

The active goal now covers all November 1984 articles. Restored the complete
기초 테크닉 코너 final installment, —시작과 끝—, on actual folios 122–124.
The package preserves 25 structured blocks, six separate captioned listing
contexts, three SPC-1000 variant relationships, 64 text-bearing code rows,
two visual blank rows, 58 numbered entries and seven history rows/21 cells.
Two prose joins retain the column and closing-line continuations. Original
wording, punctuation and historical claims remain unchanged. Two quotation
blank-run counts and eight LO identifier glyph candidates remain explicit.

All 118 JSON/assets files match a fresh-process rebuild without OCR or a
presentation build. All 28 crops match source pixels; twelve invalid cases
reject. Twenty-seven OCR tasks completed in 13.812 summed engine seconds,
with no failed tasks or retries. One index-construction repair and two verifier
boundary repairs occurred before acceptance; the failed preflights are retained.
Two premature export commands rejected without output because the recipe had
not yet passed its index guard. Selected package text never changed after export.

Prior four packages/evidence, original scans, cleanup records, shared tools and
OCR/PDF plans remain exact. The unchanged PDF/JPEG regression baseline is reused
for this data-only checkpoint. Five reproducible article packages are complete;
35 canonical identities await disposition. Human acceptance, exact original
encoding/typesetting and execution remain unverified.

See [Basic Techniques result](metadata/catalog/scan-restoration/1984-11-basic-techniques.json).
Next: **R06**, inspect the original contents pages to classify apparent section
headings and establish feature ownership/location before the next article batch.
