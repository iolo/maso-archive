# Donated scan restoration progress

Updated 2026-11-15. Follow [PLAN-SCAN-RESTORATION.md](PLAN-SCAN-RESTORATION.md).

## Current status

**R00–R13 complete: six November 1984 articles have complete reproducible
JSON/assets packages, including the complete Feature I on actual 18–39.
Feature II has two reproducible segments covering 40–51 and remains partial.
Feature I's four original segments remain unchanged. Six section headings have source-backed non-owning
classifications.**
All completed records are assistant sample-reviewed.
Twenty-seven canonical identities await disposition. The 24 cleaned source sets
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
