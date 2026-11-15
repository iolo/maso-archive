# Donated scan restoration progress

Updated 2026-11-15. Follow [PLAN-SCAN-RESTORATION.md](PLAN-SCAN-RESTORATION.md).

## Current status

**R00–R21 checkpoints complete: ten November 1984 articles have complete reproducible
JSON/assets packages, including Feature I on actual 18–39, Feature II on 40–58,
개구리 on 66–69, 3차원 우주전쟁 on 70–74 and 미로II on 75–77. Both features retain their
immutable original segments.
아기펭귄 has two verified source segments covering all actual 78–85;
whole-article assembly remains pending, so this article stays partial.
Six section headings have source-backed non-owning classifications.**
All completed records are assistant sample-reviewed.
Twenty-three canonical identities await disposition. The 24 cleaned source sets
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
| R06 — contents ownership | Passed | Six non-owning headings; fourteen reproducible classification files and bounded feature location evidence |
| R07 — Feature I opening segment | Passed; whole article partial | Actual 18–23; 179 identical files, three tables, four code contexts and four original figures; 24–39 pending |
| R08 — Feature I middle segment b | Passed; whole article partial | Actual 24–29; 170 identical files, six code contexts, two binary examples and five original figures; 30–39 pending |
| R09 — Feature I middle segment c | Passed; whole article partial | Actual 30–35; 147 identical files, three code contexts, three tables, nineteen mathematical occurrences and six original figures; 36–39 and assembly pending |
| R10 — Feature I final segment d | Passed; whole article partial | Actual 36–39; 145 identical files, four monitor contexts, three byte tables and twelve original figures; all source pages covered, whole-feature assembly pending |
| R11 — complete Feature I assembly | Passed | Actual 18–39; 650 identical native files, all typed source indexes and the 29/30 sentence join; original four segments unchanged |
| R12 — Feature II opening segment a | Passed; whole article partial | Actual 40–45; 192 identical native files, two tables, three code contexts and three original structured diagrams; listing continues on 46 |
| R13 — Feature II middle segment b | Passed; whole article partial | Actual 46–51; 152 identical files, 185 numbered units, original keyboard screen and two typed flowcharts; listing/data group continues on 52 |
| R14 — Feature II listing segment c | Passed; whole article partial | Actual 52–57; 65 identical files, 692 numbered rows, 4,844 fields and typed data/routine groups |
| R15 — Feature II final source segment d | Passed; assembly pending at this checkpoint | Actual 58; 17 identical files, 116 numbered rows, 812 fields and fourteen routine groups |
| R16 — complete Feature II assembly | Passed | Actual 40–58; 435 identical files, unified programs/groups and typed diagram relationships; 232 shared tests pass |
| R17 — 개구리 | Passed | Actual 66–69; 78 identical files, one 284-unit BASIC program, 68 table cells and original screenshot relationships; twelve local uncertainties retained |
| R18 — 3차원 우주전쟁 | Passed | Actual 70–74; 70 identical files, one 403-unit BASIC program, thirty table cells, original editorial illustration and typed music/sprite DATA groups; 23 local uncertainties retained |
| R19 — 미로II | Passed | Actual 75–77; 70 identical files, 83 sparse BASIC units, 112 table cells, literal hex and coordinate DATA groups, and original screenshot relationships; eight local uncertainties retained |
| R20 — 아기펭귄 opening segment a | Passed; whole article partial | Actual 78–83; 133 identical files, 142 table cells, nine nested branches, 88 monitor rows/700 byte fields, 234 BASIC units and 61 scan-linked custom-glyph runs; 3240 continues on 84 |
| R21 — 아기펭귄 continuation segment b | Passed; assembly pending | Actual 84–85; 25 identical files, 280 physical rows, incoming 3240 fragment plus 222 printed statements, 48 maze fields and 90 graphic/run occurrences; original 5460 END retained |
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

## R06 completed — 2026-11-15

Inspected the original contents source 015 and retained six heading/child context
crops. 취미생활, 교육입문, 비지니스, 테크니컬, 공모입선작 and 정보모음 are
non-owning group headings. Canonical IDs, titles, parents and page references
remain exact; no duplicate article bodies were created. Source 065 independently
shows the 취미생활 divider and navigation list. Neither 015 nor 065 has a visible
printed folio, so their filenames are not promoted to observed folios.

All fourteen selected classification JSON/assets files reproduce in a separate
process. Six crop pixel checks and seven rejected ownership faults pass. A first
crop candidate with clipped heading tops is preserved with its input snapshot;
the selected revision widens those bounds. No OCR or article-body export ran.
Five earlier article packages/evidence, cleanup records, original sources and
shared tools/plans remain unchanged.

The lookup scope reached twenty outside views. Feature I opens on actual 18 as
애플 베이직에서 기계어로(2), with matching continuation probes on 30 and 36;
its ending is unverified. Feature II has a matching 기계어로 음악 구현 header on
actual 42; its opening/ending are unverified. The dense listing on source 054
has no ownership assigned from this probe. Five reproducible articles and six
non-owning headings are accounted for; 29 identities remain pending.

See [contents classification result](metadata/catalog/scan-restoration/1984-11-contents-classification.json).
Next: **R07**, verify the transition around sources 037–041, then restore a
bounded opening segment of feature I. JPEG segment assembly needs integration
before the first assembly; whole-issue export remains pending.

## R07 completed — 2026-11-15

Feature I, 애플 베이직에서 기계어로(2), opens on actual 18 and ends on 39.
Feature II, 기계어로 음악 구현, opens on 40 with the byline 탁연상; its ending
remains unverified. Restored only Feature I's opening segment, actual 18–23,
under its canonical article identity. Actual 24 begins a new paragraph and
listing 4; no word or numbered listing row splits at this segment boundary.
The article remains partial, with present pages 24–39 awaiting restoration.

The segment preserves 25 logical blocks, three tables/182 grid slots, ten actual
blank cells, three merged header continuations, four separate code contexts,
139 physical rows including two visual separators, 96 numbered entries and
581 assembler fields. Nine byte-continuation rows remain attached to their
numbered source entries. Four original figures retain 54 literal label
occurrences. Captions, prose joins, table cells, code fields and original assets
have source-linked ranges and associations independently of page presentation.
Printed decimal/hex/DATA/DFB differences, OF/OFF variants and diagram label
arrangements remain literal. Eleven dashed-run counts and two object-name
0/O glyph candidates remain explicit.

All 179 native files reproduce exactly in a fresh process without OCR or a
presentation build. Forty-four crop pixel checks and twelve rejected invalid
cases pass. Forty OCR tasks completed in 28.860 summed engine seconds, with
no failed tasks or retries. Enlarged review caught a clipped triangle apex;
the selected crop widens its top by eighteen rendered pixels. The original map,
bundle and mistaken early crop pass remain preserved. An explicit, pinned
recognition-map reuse path accepts figure-bound changes alone and retains all
original OCR/settings bytes. Both PDF and JPEG paths pass: 214 PDF regression
tests and six JPEG/reuse tests. One map-ID preflight, one gap-shape export
preflight and one verifier count repair are retained; selected export content
did not change after the successful build.

The five prior article packages/evidence, R06 classifications/evidence, original
sources, cleanup records and shared OCR/PDF plans remain exact. The shared
builder change and its implementation pins are recorded explicitly. November
now has five complete packages, one partial feature, six non-owning headings
and 28 unclassified identities. Human acceptance and execution remain unverified.

See the [Feature I segment result](metadata/catalog/scan-restoration/1984-11-apple-machine-language-a.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R08**, restore actual 24–29 as the next bounded Feature I segment and
check its 29/30 continuation. Integrate JPEG segment assembly before combining
the preserved segments; whole-issue export remains pending.

## R08 completed — 2026-11-15

Restored Feature I's next immutable segment, actual 24–29, under its existing
canonical identity. Listing 4 spans 24–25, listing 5 is complete on 26, and
listing 6 spans 27–28. Three independent annotated carry/monitor examples retain
their own instruction units and physical wraps. The source word joins across
25/26 and 26/27 and the paragraph joins across 28/29 are explicit. The sentence
ending on 29 with 사실 앞에서 즐겨썼던 continues on 30 with
흰색과 검은색 그래픽에서는; this remains a pending assembly join.

The package contains 27 logical blocks, six code contexts, 205 physical rows,
171 numbered assembler entries, eleven unnumbered instruction units, nine
byte-continuation rows, 1,260 assembler fields and 37 inline fields. Two binary
examples retain 34 source labels plus two explicitly absent header slots.
Five original figures preserve 133 literal label occurrences, observed flow
connectors, annotated shape data, sample shapes and 150 independent dot/bit
cells. Three listing captions and three observed figure captions retain their
associations. No figure or value was regenerated from expected machine behavior.
The diagram's repeated $0F label and the leading zero in its $FF row remain
literal, as do the prose/listing Scale difference, source addresses, references,
spelling and the two separate SKIP examples. Three object-name 0/O candidates
remain local and explicit.

All 170 native files reproduce exactly in a separate process without OCR or a
presentation build. All 44 crops match source pixels; fourteen invalid cases
reject. Thirty-nine OCR tasks completed in 28.316 summed engine seconds, with
no failures or retries. One pre-OCR map refinement widened tight text/figure
margins; the original candidate remains preserved. Enlarged review confirmed
the source spelling 부딧히게 before export. One verifier phrase guard was
repaired with its failed preflight retained; selected export content remained
unchanged after the first successful build.

The six earlier article/segment packages and their evidence, R06 classifications,
selected source masters, cleanup pins, shared implementation and OCR/PDF plans
remain exact. This data-only batch reuses R07's 220-test regression baseline.
November still has five complete articles, one partial feature, six non-owning
headings and 28 unclassified identities. Feature I now has source-checked
segments for twelve of its twenty-two pages; the remaining ten pages and
whole-article assembly are pending. Human acceptance, execution and original
encoded bytes remain unverified.

See the [Feature I segment b result](metadata/catalog/scan-restoration/1984-11-apple-machine-language-b.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R09**, restore actual 30–35, preserving the pending 29/30 sentence and
checking the 35/36 continuation. Then restore 36–39 and integrate JPEG segment
assembly before combining the immutable feature segments. Whole-issue export
and the remaining November identities stay in scope.

## R09 completed — 2026-11-15

Restored actual 30–35 as a third immutable Feature I segment under the existing
canonical identity. Listing 7 spans 32–33; listing 8 is complete on 34. The small
BASIC example remains independent. Logical continuations preserve split words
and the formula 40*AA across 32/33 without duplicating source text. The pending
29/30 sentence has both sides restored in separate packages; its assembly join
is still pending. Page 36 starts a new paragraph and continues the raster topic.
The rocket diagram on 35 awaits an explicit relationship to the original byte
table and decoding explanation on 36 after their restoration.

The package preserves 25 logical blocks, eight joins, three code contexts,
152 physical rows, 146 numbered entries, two byte continuations, 1,008 assembler
fields, 23 BASIC tokens and seven DFB literals. Three tables contain 197 grid
slots, distinguishing 23 actual blanks, four merged continuations, two shared
colour-label continuations and six ellipsis cells. Eight source annotations
retain the address diagram's labels and bracket contexts. Nineteen mathematical
occurrences preserve literal source characters and line breaks. Six original
figures retain 71 labels, 28 colour-symbol cells and 196 observed dot/blank cells.

The BASIC example's 1892 and line 44 remain as printed. The address table's 9340,
row 52's $3000, AA/A differences, formula double asterisk, 13736 versus
13896+21=13917, the 79-command claim and repeated 140 remain independent source
readings. The uncorrected colour example retains adjacent dots at the byte
boundary; the next example alternates. The rocket's 168 cells were reviewed
independently of the next page's byte table. Seven local uncertainties cover
an ellipsis count, damaged prose, a damaged decimal and four 0/O glyph
occurrences. No uncertain digits or damaged word were filled from expected
machine behavior or numerical results.

All 147 native files reproduce exactly in a separate process without OCR or a
presentation build. All 39 source crops match pixels, and sixteen invalid
structural cases reject. Thirty-three OCR tasks completed in 28.538 summed
engine seconds with no failures or retries. One pre-OCR map refinement and one
private prose-script quote repair are preserved. Both exports and the independent
verifier passed without preflight repairs. The seven earlier article/segment
packages and their evidence, contents classifications, source masters, cleanup
pins, shared implementation and OCR/PDF plans remain exact. This data-only
checkpoint reuses R07's 220-test regression baseline.

November still has five complete articles, one partial feature, six non-owning
headings and 28 unclassified identities. Feature I has checked segments for
eighteen of its twenty-two pages. Original encoded bytes/typesetting, execution
and human acceptance remain unverified.

See the [Feature I segment c result](metadata/catalog/scan-restoration/1984-11-apple-machine-language-c.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R10**, restore actual 36–39 and the rocket diagram/table relationship.
Then integrate JPEG segment assembly and combine the complete 18–39 feature,
including the pending 29/30 sentence join. Feature II, all remaining November
identities and whole-issue export remain in scope.

## R10 completed — 2026-11-15

Restored the final Feature I segment on actual 36–39 under the existing canonical
identity. The final paragraph and boxed 정보 end mark are source-compared;
Feature II begins independently on 40. A typed cross-segment relationship links
the original rocket diagram on 35 to the original decoding explanation and byte
table on 36. Their fifth-row difference remains literal. The four preserved
segments now cover all twenty-two source pages, but whole-feature assembly and
the pending 29/30 sentence join remain outstanding.

The final segment retains 25 logical blocks, five exact column joins, three byte
tables/72 source positions and four independent monitor contexts. Seventeen
instruction units span 22 physical rows, including two explanatory wraps and
three separate vertical ellipsis dots; 116 typed source fields retain command,
address, byte, return-token and explanation occurrences. The white monitor
example contains seven printed rows, and the shifted example's third address
is 2800. Neither gains an inferred row or address correction. The prose's
repeated 3번째 remains as printed. One open table glyph has explicit 0/C
candidates without a certified complete byte value.

Twelve original figures retain 236 label occurrences and 1,362 independently
observed large-dot, small-dot and empty cells. The rocket, paired symmetry,
white-shift and green-shift diagrams preserve distinct source patterns, byte
labels, captions and bracket/equality contexts. The last-byte diagram on 36
has no axis or high-bit text labels; wider source context confirms their
absence. No labels are borrowed from adjacent examples and no pattern is
regenerated from expected bytes, colour phase or motion.

Enlarged review caught a third ellipsis dot outside the initial monitor crop.
The initial map, raw OCR, crop and insufficient preflight remain preserved.
One targeted repair widens that crop and recognizes only the affected region;
the other 29 results and their original settings remain exact. The shared OCR
command now accepts an optional region selection, and the native builder accepts
disjoint evidence scopes while checking the selected regions against each
original recognition map. Source/page records, exclusions, roles, notes and
identities must still match. Duplicate/missing region assets reject. Both PDF
and JPEG paths pass: 214 PDF regression tests plus eleven image/reuse tests.
Neither `PLAN-OCR.md` nor `PLAN-PDF.md` changed.

All 145 native files match a separate-process rebuild exactly, without fresh OCR
or a presentation build. All 42 source crops match pixels and sixteen invalid
structural cases reject. Thirty initial OCR tasks plus one targeted repair
completed in 13.817 summed engine seconds, with no engine failures. Both exports
and the independent verifier passed without preflight repairs. The eight earlier
article/segment packages and private evidence, contents classifications, masters
and cleanup pins remain exact. Shared implementation changes are pinned
separately from the initial recognition implementation.

November remains at five complete articles, one partial feature, six non-owning
headings and 28 unclassified identities. Original encoded bytes/typesetting,
execution and human acceptance remain unverified.

See the [Feature I segment d result](metadata/catalog/scan-restoration/1984-11-apple-machine-language-d.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R11**, integrate and verify JPEG segment assembly, then combine actual
18–39 while retaining typed structures, source relationships, uncertainties and
the exact 29/30 sentence join. Continue Feature II and all remaining November
identities through issue closeout afterward.

## R11 completed — 2026-11-15

Selected the complete Feature I assembly on actual 18–39 under its existing
canonical identity. All four original segment packages remain byte-preserved
inside the assembly. The sentence ending on 29 joins the opening on 30 with
exactly one reviewed space, and both original region transcriptions remain
separately indexed. The rocket on 35 links explicitly to the independent
table/explanation on 36; the printed discrepancy is preserved.

The native package accounts for all 22 source views, 169 mapped regions,
142 original OCR outcomes, 101 logical blocks and 27 original figures. Its
projected indexes retain eleven tables/487 cells, seventeen code contexts,
518 physical rows, 441 logical units (413 numbered and 28 unnumbered), 2,849
assembler fields, 117 source literal tokens, 37 inline fields, 23 BASIC tokens,
116 monitor fields, nineteen mathematical occurrences, 494 figure labels and
all 24 local uncertainty occurrences. Twenty-three existing figure structures
and associations remain typed; the opening segment's four original figures
retain their source labels/assets and original content relationships. Forty-one
prose joins include the newly resolved cross-segment sentence join. There are
2,092 direct references to exact immutable correction records.

The shared assembler now accepts opt-in `structured-regions-v1` JPEG recipes,
with explicit source indices and pinned inventory. It namespaces local
identities, projects block/article/listing byte ranges, preserves blank spans,
and rejects unprojected indexes, overlapping text partitions and dangling
active references. Original boundary declarations and cross-segment source
relationships must match. Historical source IDs retain their original scope;
active indexes name assembled blocks/assets. The combined raw archive preserves
621 entries, including ten original recognition maps. Existing PDF assembly
recipes and projections remain compatible. Neither shared OCR/PDF plan changed.

All 650 native files compare byte for byte against a fresh-process rebuild with
the final reference/partition checks, without OCR or a presentation build.
The earlier 169 master-to-crop pixel checks are reused after rehashing masters
and proving copied crop bytes and source geometry unchanged. Sixteen invalid
projections reject, and 229 shared tests pass (214 PDF plus fifteen JPEG,
recognition-reuse and structured-assembly tests). One synthetic fixture's
reading-order origin and one reference gate's treatment of historical boundary
IDs required repairs; failed logs remain preserved. Both repeated exports and
the selected export passed. The nine earlier article/segment packages and their
private evidence, contents classifications, source masters and cleanup records
remain exact.

November now has six complete article packages, no partial article, six non-owning
headings and 28 unclassified identities. Local source uncertainty, original
encoded bytes/typesetting, execution and human acceptance remain separate from
the successful package reproduction.

See the [complete Feature I result](metadata/catalog/scan-restoration/1984-11-apple-machine-language.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R12**, locate Feature II's ending and restore its opening in a bounded
batch. Its observed title/byline begin on actual 40. Continue all remaining
November identities, source-image accounting, covers and whole-issue native
export/rebuild afterward.

## R12 completed — 2026-11-15

Restored the opening of Feature II, 기계어로 음악구현 by 탁연상, on actual
40–45 under its canonical identity. Boundary review locates the feature on
40–58: GOODMUSIC's explanation closes on 46, MINI ORGAN SPC-1000용 starts on
47, and its second listing ends at the stated A3E7 address on 58. Advertisements
and contest material follow. Interior 48–54 still awaits its own restoration
review; the located extent does not claim complete interior coverage.

The native segment retains 48 source regions, 42 logical blocks and three
explicit joins. Two tables preserve 156 header/data positions, genuine blanks,
the duplicated FREQ header, one absent header and five spanning octave labels.
Three code contexts retain 126 numbered source units, 146 physical/annotation
rows, 812 assembler/cycle fields, 322 physical BASIC tokens and 116 logical DATA
tokens. The number 27 split across two printed rows remains linked to both
original digit fragments. GOODMUSIC listing 2 owns both page-45 panels and keeps
an explicit continuation from row 104 to row 105 on 46.

All three original diagrams retain pixels and 98 label occurrences. Their typed
structures include the paired waveforms, eight pitch-phase bars and the
35-node/45-connector flowchart. Printed TIME increments, twelve mathematical
occurrences, g after h and the numerical chain 133.8=114($72) remain literal.
Four local uncertainty occurrences preserve a 13/B-looking table entry, an
object-filename 0/O glyph and two decorative string glyphs. Four bibliographic
references and the independent pull quote retain separate source relationships.

All 192 native files match a fresh-process rebuild byte for byte without OCR or
a presentation build. Forty-eight source crops match pixels; sixteen invalid
structural cases reject. All 45 mapped OCR tasks completed with zero engine
failures or retries. Display-text recognition misses were corrected directly
against source. One pre-OCR map refinement, one native-input helper repair for
repeated literals and two verifier bookkeeping repairs remain preserved with
their failed attempts. Both exports passed without repairs.

The ten earlier article/segment packages and their private evidence, contents
classifications, source masters and cleanup pins remain exact. The 229-test R11
baseline is reused after rehashing its evidence and proving shared implementation,
schemas, tests and both shared plans unchanged. Session cleanup ran in preview
mode only. November now has six complete packages, one partial feature, six
non-owning headings and 27 unclassified identities. Original encoded bytes,
typesetting, execution and human acceptance remain unverified.

See the [Feature II opening result](metadata/catalog/scan-restoration/1984-11-machine-music-a.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R13**, restore actual 46–51, preserving the outgoing GOODMUSIC program
identity and the MINI ORGAN section transition. Then continue 52–58 and assemble
the whole feature before completing the remaining November work.

## R13 completed — 2026-11-15

Restored Feature II actual 46–51 under the same canonical identity, preserving
the GOODMUSIC/MINI ORGAN section transition. GOODMUSIC listing 2 resumes at
row 105 and ends at 157 on 46; its preceding rows remain in segment a. The
independent execution-time excerpt stays a separate code context. MINI ORGAN's
prose ends with its original emblem on 49, while its attached diagrams and
listings remain part of the article. Listing 1 starts at 0000 on 51 and continues
at 0116 on 52, including the open TW character-definition group.

The segment retains 38 source regions, 33 logical blocks, two explicit joins,
185 numbered units and 189 physical/annotation rows. Its three code contexts
preserve 1,279 source fields, 322 DFB/DEFB literals and ten label-delimited data
groups without deriving bitmaps from expected characters. Ninety inline fields,
five mathematical occurrences, two numbered requirements, two bibliography
references, two independent pull quotes and the end emblem retain source ranges.
The printed MINT ORGAN, 8H before the wrapped 9000, 764·4468, row 129 3-C and
other source discrepancies remain literal.

Three original figures retain 168 label occurrences: a two-row keyboard screen,
the thirteen-node/seventeen-connector basic flowchart and the detailed flowchart
with 35 printed shapes, one connector-junction record and 58 observed main-flow,
routine-expansion and return-port relationships. Printed 321~319 and the separate
prose/diagram row-range differences remain unchanged. These structures describe
source relationships, not successful execution. Nine local glyph uncertainties
retain an initial D/0 address glyph, five 0/O name suffixes and three unresolved
composite screen-symbol groups; no modern keyboard bindings are inferred.

All 152 native files match a separate-process rebuild byte for byte, without
fresh OCR or a presentation build. Thirty-eight original-to-crop pixel checks
and sixteen invalid structural cases pass. All 35 OCR tasks completed with zero
engine failures or retries. One pre-OCR map refinement widened clipped/tight
prose and the closing emblem. An optional nearest-neighbor inspection enlargement
failed; exact keyboard crops were used and the failure note retained. Native
input generation, both exports and the independent verifier passed without repairs.

The eleven earlier article/segment packages and their private evidence, contents
classifications, original masters, cleanup records and shared plans remain exact.
The unchanged shared implementation reuses the rehashed 229-test R11 baseline.
Session cleanup ran in preview mode only. November counts remain six complete
packages, one partial feature, six non-owning headings and 27 unclassified
identities. Original encoding/typesetting, execution and human acceptance remain
unverified.

See the [Feature II segment b result](metadata/catalog/scan-restoration/1984-11-machine-music-b.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R14**, restore actual 52–57, including the listing 1 continuation and its
transition into listing 2. Final 58 and whole-feature assembly follow before
continuing the remaining November identities and issue closeout.

## R14 completed — 2026-11-15

Restored Feature II actual 52–57 as segment c under the same canonical identity.
MINI ORGAN listing 1 resumes at 0116 inside the TW character-definition group,
continues through the character and title/screen data, and ends at 0502 END on
55 with its printed address 9678 and blank object-byte field. The separately
captioned listing 2 starts below it at 0000 ORG 9FDAH. Its current final row is
0304 SOUND2: SUB A on 57; present source 58 resumes at 0305 and remains pending.

The native segment retains fourteen source regions, three logical blocks and
eleven panel joins. Two distinct program contexts preserve 692 numbered rows,
4,844 independently transcribed source fields and 1,440 DEFB literal occurrences.
Typed source groups retain 37 character-definition groups, sixteen title-data
groups, thirteen variable-definition groups, 52 routine groups and one listing
preamble. Group identities use listing and source-row occurrences; repeated data
and labels are not deduplicated. The incoming TW group and outgoing SOUND2
routine retain explicit continuation relationships. No character artwork or
object code is regenerated from these values.

All panels and the listing caption were compared against enlarged source crops.
The source RR: label at 0356 corrects an initial full-page AA: reading. Independent
fields retain 9A2H at listing 2 row 0045, 0FCH at 0059, (KEY),IY at 0061, 949H
at 0086, BIT 4,D at 0183, CBH/CBL at 0297/0298 and the visible KEY?1 operand at
0303. Ten local glyph uncertainties retain a D/0 initial address marker and nine
0/O label/operand alternatives, without resolving encoded names by program
expectation. Tabs represent field alignment, not recovered typesetting.

All 65 native files match an independent fresh-process rebuild byte for byte.
Fourteen source-to-crop pixel checks and eighteen invalid structural cases pass.
All fourteen mapped OCR tasks completed without engine failures or retries;
recognition errors were corrected from source. One pre-OCR refinement widened
five right-panel margins. One verifier ordering assumption failed and was repaired
to match uncertainty occurrences by region, row and field; its failed attempt is
retained. Native preparation and both exports passed without repairs.

The twelve earlier packages and their private evidence, contents classifications,
original masters, cleanup records and shared plans remain exact. The rehashed
229-test R11 baseline is reused for unchanged shared implementation, schemas and
tests. Session cleanup ran in preview mode only. November remains six complete
packages, one partial feature, six non-owning headings and 27 unclassified entries.
Original encoded bytes/typesetting, execution and human acceptance remain
unverified.

See the [Feature II segment c result](metadata/catalog/scan-restoration/1984-11-machine-music-c.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R15**, restore final actual 58, then assemble the complete 40–58 feature
with unified program/data-group identities and retained typed diagram references.
Continue the remaining November entries and whole-issue closeout afterward.

## R15 completed — 2026-11-15

Restored final Feature II actual 58 as segment d. MINI ORGAN listing 2 resumes
at 0305 inside SOUND2 and ends at the observed 0420 A3E7 C9 RET. The following
advertisement boundary reuses pinned R12 extent evidence. All nineteen source
pages on actual 40–58 are now covered in four separate immutable segments;
whole-feature assembly remains pending.

Two original listing panels form one logical code block with one explicit join.
The segment retains 116 numbered rows, 812 independently transcribed source
fields and fourteen typed routine groups. Incoming SOUND2 keeps its source
relationship to 0304 on 57. PLAY remains one routine across the panel boundary.
The printed KEY?3, KEY?2 and KEY?1 labels retain their visible question marks,
supporting the literal KEY?1 jump retained in segment c. No new caption, filename,
END directive, derived object bytes or execution claim is introduced.

All 17 native files match a fresh-process rebuild byte for byte. Both source
crops match original pixels, and fourteen invalid structural cases reject.
Both mapped OCR tasks completed without engine failures or retries. The source
map needed no refinement; native preparation, exports and verification passed.
The thirteen earlier packages and private evidence, source masters, contents
classifications and shared plans remain exact. The rehashed 229-test R11 baseline
is reused for unchanged shared implementation, schemas and tests. Session cleanup
ran in preview mode only.

November remains six complete article packages, one partial feature, six
non-owning headings and 27 unclassified entries. The complete Feature II package
must unify GOODMUSIC listing 2, both MINI ORGAN programs, split data/routine groups
and typed diagram relationships before its status changes. Original encoded
bytes/typesetting, execution and human acceptance remain unverified.

See the [Feature II final source result](metadata/catalog/scan-restoration/1984-11-machine-music-d.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R16**, assemble actual 40–58 with source/structure checks and an independent
native rebuild, then continue the remaining November entries and issue closeout.

## R16 completed — 2026-11-15

Assembled complete Feature II, 기계어로 음악구현 by 탁연상, on actual 40–58
from four immutable source segments. GOODMUSIC listing 2 now has one program
identity across 104/105, MINI ORGAN listing 1 across 0115/0116, and listing 2
across 0304/0305. The split TW character-definition group and SOUND2 routine
each retain one joined group and both original constituent records. The MINI
ORGAN source-example relationship now links its prose and three diagrams to both
complete original listings.

The complete native package retains nineteen source views, 102 original region
assets, 96 raw OCR outcomes, 76 logical blocks and six original figures. Its six
distinct code contexts preserve 1,143 physical rows, 1,119 logical units, 7,747
independent fields and 1,878 literal DATA/DFB/DEFB occurrences. Two tables retain
156 cells; 322 physical BASIC fields, 96 inline fields, seventeen mathematical
occurrences, 266 figure labels and all 23 local uncertainties remain indexed.
The logical DATA value 27 retains its separate printed 2/7 fragments. Printed
KEY? labels, 321~319, numerical discrepancies, blank fields and repeated data
remain literal. No instruction semantics resolve source glyphs or generate
replacement diagrams.

Added opt-in structured-programs-v1 assembly for explicit source-declared
program/group joins and scoped diagram component/label references. Program joins
require matching original outgoing/incoming records, consecutive rows and folios,
the previous-package manifest and adjacent code blocks. Original row identities
and source values remain stable; block/listing offsets project into unified
programs. Diagram axes, guides, phase bars, connectors, branch labels and null
junction labels retain typed source relationships. Existing structured-region
and PDF modes keep their earlier projection behavior.

All 435 native files match a separate-process rebuild byte for byte. All four
original segments are embedded exactly. The 102 earlier decoded-master pixel
proofs remain valid after rehashing masters/crops and comparing copied geometry
and bytes. Twenty-one invalid projections reject. All 232 regression tests pass:
214 PDF and eighteen JPEG/recognition/assembly tests, including three new program
assembly tests. Fourteen earlier packages and their private evidence, contents
classifications and shared plans remain exact, including the complete Feature I
package. No OCR or presentation build was needed.

Retained failed attempts document a missing projected block-owner reference,
an over-strict rejection of an unlabelled connector junction, and an independent
verifier assumption that every logical DATA token had a contiguous span. These
gates were repaired without changing historical source values. Both complete
exports passed on their first attempts. Session cleanup ran in preview mode only.

November now has seven complete article packages, no partial article, six
non-owning headings and 27 unclassified entries. Sample review and byte-for-byte
reproduction do not establish original encoding/typesetting, numerical/source
correctness, program execution or human acceptance.

See the [complete Feature II result](metadata/catalog/scan-restoration/1984-11-machine-music.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R17**, locate and restore 개구리 (catalog page candidate 66), checking
its actual title, ownership and ending in a bounded batch. Continue all remaining
November entries, source-image/covers accounting and whole-issue export/rebuild.

## R17 completed — 2026-11-15

Restored complete 개구리, credited to 편집부 for FC-100, on actual 66–69.
The preceding 취미생활 divider remains a non-owning section heading. The 정보
emblem closes the main prose, while the attached variable/program explanations
and listing continue through final 3830 RETURN. Actual 70 opens the separate
3차원 우주전쟁 article.

One original BASIC program retains 314 physical rows and 284 logical numbered
units across six panels. The music string at 2150 retains both printed fragments;
3380 DATA retains its continuation into the opposite column. The package indexes
473 literal DATA occurrences, including signed values, names, five ** delimiters
and END, plus 32 quoted logical strings. Source OBSCATLE, TE and the extra final
0 after PARK, 500 remain literal. No program was executed or corrected by expected
behavior.

Two explanatory tables retain thirteen variable definitions and twenty-one
program-range descriptions, with 68 cells and typed listing relationships. Five
prose paragraphs, the split 10/80 reference to line 1080, printed bonus formula
and original screenshot/status relationships remain independent of presentation.
Twelve local uncertainties cover music-string O/0 glyphs, three quoted blank-run
counts, status-string spacing, an extended range separator and one screenshot
digit. No caption or replacement screenshot was invented.

All 78 selected native files match a separate-process rebuild byte for byte.
All eighteen crops match the original decoded-master pixels, and seventeen
invalid structural cases reject. Seventeen mapped OCR tasks completed without
engine failures or retries; no source-map refinement was needed. A successful
initial export/rebuild is retained before refining the explicit prose-number
fragments and bonus-formula index in the selected revision. Neither revision
changes the recognized source text or original image assets.

All fifteen earlier packages and their private evidence, contents classifications,
source masters and shared plans remain exact. The unchanged implementation,
schemas, tests and frozen R16 logs support reuse of the 232-test baseline;
this data-only batch does not rerun those regressions. Session cleanup ran in
preview mode only. The batch freezes 208 private evidence files.

November now has eight complete article packages, no partial article, six
non-owning headings and 26 unclassified entries. Original encoding/typesetting,
source correctness, execution and human acceptance remain unverified.

See the [개구리 result](metadata/catalog/scan-restoration/1984-11-frog.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R18**, locate and restore 3차원 우주전쟁 (catalog page candidate 70),
verifying actual boundaries in a bounded batch. Continue all remaining November
identities, source-image/covers accounting and whole-issue native export/rebuild.

## R18 completed — 2026-11-15

Restored complete 3차원 우주전쟁, credited to 편집부 for MSX, on actual 70–74.
One original BASIC program runs from 1000 through final 5020 DATA above a separate
advertisement. No terminal END or RETURN is invented. Actual 75 opens 미로II.
The original frog artwork remains an editorial illustration where printed;
it is neither reassigned to the preceding article nor presented as a game screen.

The native package retains 418 physical rows and 403 logical numbered units
across ten panels. Split 20/70 and 197/0 jump targets and T/HEN keyword fragments
retain their source ranges; the music string at 3760 retains its physical wrap.
There are 118 DATA positions, including eight empty music slots, and 712 literal
source character pairs. Twenty-two four-row sprite DATA groups retain their
printed apostrophe separators and loader-source relationships. Groups 4320–4350
and 4770–4800 remain unified across page/panel boundaries. No sprites, music or
object bytes were generated.

Three prose paragraphs, fifteen program-range explanations with thirty cells,
the MSX/editorial credit and closing emblem retain source relationships. The
second range row's trailing ~, 2190's printed 117, 3040's = < symbol order and
both 2280/2290 SOUND 8, 0 occurrences remain literal. Twenty-three local
uncertainties retain music O/0 glyphs, source word spacing, two dot-like ink
marks, an overprinted coordinate glyph and status-string spacing.

All seventy native files match a separate-process rebuild byte for byte. All
sixteen original-to-crop pixel comparisons pass, and nineteen invalid structural
cases reject. One failed verifier attempt showed that text comparison alone
could not reject a displaced empty-slot anchor. The repaired gate requires its
exact source position; the successful native package and source readings did
not change. Both exports passed on their first attempts. Fifteen OCR tasks
completed without engine failures or retries, with no map refinement.

All sixteen earlier packages and their private evidence, classifications,
masters and shared plans remain exact. Rehashed unchanged implementation/schema/
test pins and frozen R16 logs support reuse of the 232-test baseline; those
regressions were not rerun for this data-only batch. Cleanup ran in preview mode
only. The batch freezes 210 private evidence files, including the failed gate
and an adjusted original-detail crop attempt.

November now has nine complete packages, no partial article, six non-owning
headings and 25 unclassified identities. Original encoding/typesetting, source
correctness, execution and human acceptance remain unverified.

See the [3차원 우주전쟁 result](metadata/catalog/scan-restoration/1984-11-space-fight.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R19**, locate and restore 미로II (catalog page candidate 75), checking
actual boundaries before mapping. Continue every remaining November identity,
source-image/covers accounting and checked whole-issue native export/rebuild.

## R19 completed — 2026-11-15

Restored complete 미로II on actual 75–77, credited to 김명준, 배재고2, for
애플 컴패티블. The observed title is represented as 미로Ⅱ while the canonical
contents identity remains unchanged. Actual 78 opens the separate 아기펭귄 article.

One original BASIC program retains 142 physical rows and 83 sparse numbered
units, from 5 through final 1200 DATA, across three panels. Two visual blank
separators remain physical rows. Continuations beginning with 38 and 4 belong to
555 and 580; neither becomes an invented numbered unit. The split INPUT variable
EE and physical source fragments retain exact ranges. No terminal END is added.

Two continued tables preserve nineteen independent variable definitions and
thirty-seven selective program explanations, with 112 cells. Array M and scalar
M retain separate definition identities; the explanation table does not acquire
invented descriptions for unmentioned source units. Nine source paragraphs,
the split CTRL-I reference, direction examples and the original screenshot's
seven labels retain typed relationships independently of presentation.

The two quoted hex readings retain 109 and 46 characters, including one final
unpaired source character in the first. Direct comparison with the original
scan supports retaining that odd length without padding, deletion or decoding.
Five coordinate DATA groups retain 170 numeric occurrences, 85 pairs, the
source-declared 5,0 endings and their explanation, loader and figure-label links.
Printed equality at 620 and < = symbol order at 690 remain literal. Eight local
uncertainties retain quoted whitespace, three O/0 identifier readings and faint
marks after 440. No program, shape rendering or screenshot reproduction ran.

All seventy native files match a separate-process rebuild byte for byte. All
sixteen source crops match original decoded-master pixels, and twenty-two
invalid structural cases reject. One pre-OCR map refinement enlarged four tight
edges; initial and refined evidence is retained. Fifteen OCR tasks completed
without engine failure or retry, with no later geometry change. Both exports
and the independent verification passed on their first attempts.

All seventeen earlier packages and private evidence, contents classifications,
source masters and shared plans remain exact. Rehashed unchanged implementation,
schema and test pins plus frozen R16 logs support reuse of the 232-test baseline;
those regressions were not rerun for this data-only batch. Cleanup ran in preview
mode only. The batch freezes 193 private evidence files.

November now has ten complete article packages, no partial article, six non-owning
headings and 24 unclassified identities. Original encoding/typesetting, source
correctness, execution and human acceptance remain unverified.

See the [미로II result](metadata/catalog/scan-restoration/1984-11-maze-ii.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R20**, locate and restore 아기펭귄 (catalog page candidate 78), checking
actual boundaries and retaining explicit continuation if more than six new source
views are needed. Continue every remaining November identity, source-image/covers
accounting and checked whole-issue native export/rebuild.

## R20 completed — 2026-11-15

Restored the opening segment of 아기펭귄 on actual 78–83, credited to
원성욱/김경헌 for SPC-1000. The observed title is 아기 펭귄. All eight article
pages were inspected to establish the actual 78–85 extent; actual 86 opens
컨닝. The article remains partial until 84–85 are restored and assembled.

Two explanatory tables preserve 28 variable definitions and 43 program-range
explanations, with 142 cells. The nine ON/GOTO key branches continue across the
79/80 page boundary. The 3670–3760 description continues from 80's left column
into its right column. Both description cells retain their separate physical
source fragments. Repeated SY definitions and independent O/zero forms in the
prose/table/listing remain literal. Future listing references point explicitly
to unrestored 84–85 rather than claiming complete segment coverage.

Three original listing identities remain separate. List 1 retains 26 address
rows and its four-byte final row. List 2 retains 62 address rows across two
panels, including every printed zero row. Together they preserve 700 byte-field
readings; faint source fields retain local alternatives and original-master
detail evidence. No binary, disassembly, music or shape rendering was generated.

List 3 BASIC retains 312 physical rows, including three visual blank separators,
and 234 numbered source units. Nine split tokens preserve physical fragments,
including 4920, THEN, GOSUB and -32. A numeric wrap beginning with 2 remains
part of 2850. Sixty-one distinct editorial custom-glyph run markers retain scan
links with null original bytes and counts. These markers identify source
occurrences and are not literal original code or evidence of executable bytes.
Eight title DATA groups retain their graphic strings, 32 numeric parameters
and pending loader relationships. Twelve information DATA strings retain their
source order and loader references.

The final 3240 ON CH GOTO fragment stays explicitly open: `, 3420` at the top of
84 continues it before numbered 3250. No terminal directive or complete logical
unit is invented at the segment boundary. The remaining source ends at 5460 END
on 85; that ending is location evidence, not a restored part of this segment.

The original penguin illustration remains one figure with two overlapping crops
and original source-coordinate placement. Its tagline, the original game screen,
status labels/values and the independent clock/conductor illustration retain
separate identities and relationships. Thirty-three local source uncertainties
cover faint byte glyphs, punctuation, stylized wording, screenshot labels,
O/zero readings and quoted whitespace, separately from the 61 graphic markers.

All 133 selected native files match a separate-process rebuild byte for byte.
All 34 source crops match decoded-master pixels; 28 invalid structural cases
reject. The first successful independent audit was followed by stronger source
placement and null glyph-byte/count probes; both audits passed and native files
remained unchanged. All eighteen earlier packages and private evidence,
classifications, masters, implementation and shared plans remain exact. The
unchanged pins and frozen R16 logs support reuse of the 232-test baseline;
those regressions were not rerun for this data-only segment.

One initial map validation rejected a segment suffix in the canonical article
ID; the canonical identity was restored before map creation/OCR. One pre-OCR
refinement widened three regions. Thirty OCR tasks then finished without engine
failure or retry and without later geometry changes. An OCR audit assumption
about the existing map-hash contract and one typed-branch lookup's omitted
source space were corrected before verification/native publication. The initial
failures and successful outcomes are retained. Both exports passed on their
first attempts. Cleanup ran in preview mode only. The batch freezes 362 private
evidence files.

November now has ten complete articles, one partial article, six non-owning
headings and 23 unclassified identities. Original encoding/typesetting, source
correctness, execution and human acceptance remain unverified.

See the [아기펭귄 segment result](metadata/catalog/scan-restoration/1984-11-baby-penguin-a.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R21**, restore actual 84–85, including the incoming 3240 fragment, then
assemble and independently rebuild the complete eight-page article. Verify
assembly support for this same-unit continuation and sparse BASIC numbering
before use. Continue all remaining November identities, covers/source accounting
and the checked whole-issue native export/rebuild.

## R21 completed — 2026-11-15

Restored actual 84–85 as continuation segment b of 아기펭귄. All eight observed
article pages, 78–85, now have source restoration in two immutable segments.
The article stays partial until whole-article assembly and its independent
native rebuild pass. Actual 86 opens the separate 컨닝 article.

The opening `, 3420` remains a numberless physical fragment of source 3240
ON CH GOTO from the previous segment. Its contextual logical identity, exact
previous-package manifest and preceding literal are preserved; no 3240 prefix
is inserted into this segment text. The next printed number is 3250. The
continuation retains 280 physical rows, one visual blank separator and 222
printed numbered statements, plus the incoming source fragment. Ten split
source tokens retain their physical fragments, including RETURN, GOSUB, MOD,
X0, IF, ELSE and the wrapped closing-message word. The original ending is
5460 END.

Ten maze DATA rows retain 48 unquoted graphic fields in original comma-field
order: nine five-field rows followed by a three-field row. Selected visual
heart/outline-block patterns have source links and no encoded character
assignments; the final row is neither padded nor reshaped. Eight GAME OVER
DATA groups retain sixteen physical graphic-string fragments, 32 numeric
parameters and their original shared loader across both 85 panels. Relationships
to the opening segment's title DATA, seventeen explanation rows and four
function-key dispatch targets are explicit. Ten original function-key
assignments retain their source expressions.

Ninety distinct custom-glyph/run occurrences retain editorial markers, pinned
scans and null original bytes/counts. Across both segments there are 151 such
occurrences. These markers are not literal original code or evidence of byte
equality. Eighteen local uncertainties retain quoted whitespace and O/zero
readings. The clearly printed R = II OR I at 4060 and FS = 3 at 5030 remain
literal source discrepancies; program behavior did not determine their readings.
No program, glyph, maze, music or bitmap output was executed or generated.

All 25 native files match a separate-process rebuild byte for byte. All four
source crops match decoded-master pixels; 25 invalid structural cases reject.
Both exports and verification passed on their first attempts. Four OCR tasks
completed without engine failure or retry. No map refinement or later geometry
change was needed. All nineteen earlier packages and their private evidence,
classifications, masters, implementation and shared plans remain exact. Rehashed
unchanged pins and frozen R16 logs support reuse of the 232-test baseline;
those regressions were not rerun for this data-only segment. Cleanup ran in
preview mode only. The batch freezes 89 private evidence files.

November counts remain ten complete articles, one partial article, six non-owning
headings and 23 unclassified identities. The ledger now records both 아기펭귄
segments with no pending source folios and an explicit pending 3240 assembly
join. Original encoding/typesetting, source correctness, execution and human
acceptance remain unverified.

See the [아기펭귄 continuation result](metadata/catalog/scan-restoration/1984-11-baby-penguin-b.json)
and [issue ledger](metadata/catalog/scan-restoration/1984-11-progress.json).
Next: **R22**, assemble and independently rebuild the complete eight-page
article. Preserve all original segment bytes/OCR provenance, combine only the
shared 3240 source unit, and retain sparse numbering, all source indexes,
continued cells, artwork placement and relationships. Validate or add narrowly
scoped assembly support with meaningful compatibility and negative tests before
use. Continue every remaining November identity, covers/source accounting and
the checked whole-issue native export/rebuild.

## R22 in progress — 2026-11-15

Qualified an explicit same-source-unit program join for the 83/84 boundary of
아기펭귄. A `logical_join` recipe declaration now validates the two original
source-unit identities, the incomplete outgoing unit, the numberless incoming
fragment, exact selected literals, the next printed number, source folios and
the previous manifest. Logical character coordinates and physical byte positions
are checked separately. The combined listing retains both physical lines;
only the logical source identity is joined. Sparse numbering is checked against
the segments' explicit observed numbers, and every nonblank physical row has one
logical owner. Original program links keep their consecutive-number contract.

Four new regression tests cover byte-identical synthetic native rebuilds,
seventeen invalid fragment/source cases, wrapped multibyte character coordinates
and rehashed outer logical-text tampering. All 214 PDF regressions and 22 JPEG,
recognition-map and assembly tests pass. Both actual source segments validate,
and the selected 3240 boundary qualifies with the expected 592 physical BASIC
rows and 456 distinct logical units across the article. This source-unit gate
does not certify the whole article projection.

The prospective checkpoint, original ledger snapshot, source/plan pins, regression
logs and boundary qualification are saved under
`archive/scans/1984-11/restoration/batch-22/`. An initial source-probe command
lacked the repository's required `PYTHONPATH=src:.`; it failed at import before
reading or writing source packages and passed after that environment correction.
Whole article export remains pending. The text/glyph indexes, continued table
cell spans, artwork placement and cross-segment data/loader/key relationships
still require explicit projection and independent verification. No complete
article package has been selected, and November counts remain ten complete,
one partial, six non-owning headings and 23 unclassified identities. Shared OCR
and PDF plans and original native packages remain unchanged.
