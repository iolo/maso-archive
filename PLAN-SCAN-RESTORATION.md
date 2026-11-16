# Restore articles from the donated scans

Created 2026-11-14. This is the next campaign after [scan cleanup](PLAN-SCANS.md).
R00–R47 are complete. The owner resumed the whole-November restoration goal.
R48 is next: establish SPC-CLOCK from its catalog opener 212 and source evidence.
Track execution in
[PROGRESS-SCAN-RESTORATION.md](PROGRESS-SCAN-RESTORATION.md).

## Aim

Restore the cleaned scans as **reproducible, presentation-independent article and
issue packages in the project's own schema**. Preserve logical content order,
titles and identities, prose, code, table rows/cells, original figures, captions
and their associations, with source provenance, correction evidence and explicit
gaps or uncertainties. Searchable text and code downloads are derived outputs;
OCR is one stage of restoration. The web reading room is a sample presentation
of these packages, not the definition of a restored article.

Preserve source geometry as evidence while expressing article structure and
relationships independently of a particular page layout or reader. Rebuild the
selected JSON/assets package from pinned sources and reviewed inputs, without
fresh OCR or a reading-room build, and compare all output files exactly. This
establishes artifact reproducibility; source fidelity also requires the separate
coverage, structure, asset, range and review checks below.
Keep this a practical issue-by-issue job. A useful partial article with a clear
gap is better than getting stuck trying to reconstruct lost paper.

Use the existing [OCR policy](PLAN-OCR.md#accepted-policy),
[bounded review procedure](PLAN-OCR.md#source-review-and-bounded-assistance) and
[JSON/assets workflow](docs/PDF-RESTORATION.md#current-data-only-commands).
**`PLAN-OCR.md` is the shared operating guide for both PDF and JPEG sources.**
Use the same OCR pipeline already used under `PLAN-PDF.md`. This scan plan adds
source selection, image-input handling and issue scheduling; it does not replace
or fork the OCR procedure. Leave `PLAN-OCR.md` and `PLAN-PDF.md` unchanged and
available for future donated PDFs, including their existing PDF commands and
source/provenance conventions.
Keep the completed PDF and CD packages intact. The outstanding PDF collection
handoff remains separate; this plan adds a new source type and new issue coverage.

## Starting point

- `archive/scans/YYYY-MM/` contains 24 checked issue sets: 6,070 distinct JPEGs,
  6,066 proposed reading-order entries and four extras. The
  [cleanup progress](PROGRESS-SCANS.md) links every issue's findings.
- The [collection audit](metadata/catalog/scans/collection-audit.json) accounts
  for all 59 ZIPs and confirms source/master hashes. Cleanup reviewed contact
  sheets and selected larger views; it did not establish full printed pagination.
- The checked `archive/toc/current/` snapshot contains **1,119 canonical TOC
  identities and 919 provisional article candidates** for these 24 dates.
  These are planning counts, not 919 proven article bodies. Group headings,
  shared bodies, unlocated entries and other outcomes still need classification.
- **22 issue dates have no supplied PDF.** February and March 1984 already have
  completed PDF restoration passes; treat their JPEGs as supplementary sources,
  rather than automatically transcribing both issues again.

Keep `PLAN-SCANS.md` as the cleanup record and `PLAN-PDF.md` as the PDF campaign
record. This short plan owns the scan-specific work.

## 1. Connect JPEG sources to the existing pipeline

Reuse the existing OCR, mapping, correction, assembly and export machinery.
Some `tools/pdf_restore/` entry points currently assume a PDF path, PDF page
indices and PDF geometry. Connect the cleaned JPEGs at that input boundary,
replacing PDF rendering with image loading where needed. Direct JPEG integration
for mapped Tesseract and native article export passed R00. Structured JPEG
segment assembly passed R11 with complete Feature I and unchanged PDF behavior.
Whole-issue export remains to be integrated before its first JPEG use. Existing
PDF commands remain valid for PDF inputs.

Keep this input change small. Reuse the pinned OCR runtime, reviewed region maps,
recognition settings, evidence, correction and export procedures from
`PLAN-OCR.md`. Extend source records explicitly only where JPEG provenance or
geometry requires it, preserving existing PDF formats, checks and archived pins.
Do not require a PDF conversion or put invented PDF page numbers into image
records. Future PDF issues must still run through the existing PDF input path.

Each selected source view must identify:

| Field | Meaning |
| --- | --- |
| Source identity | Issue, relative JPEG path, SHA-256 and native pixel dimensions |
| Cleanup inputs | Pinned `manifest.json`, `review.json` and `page-list.csv` |
| Source filename number | The donated filename's number, when present |
| Reading order | Reviewed order, including explicit review overrides |
| Printed folio | Observed numeral or label; unset when unverified |
| View geometry | Original pixel bounds, orientation and any derived-view transform |
| Regions | Eligible text/code/table/figure regions, exclusions and reading sequence |

Use `page-list.csv` together with `review.json`; sorting filenames or using only
the extraction manifest loses July 1987's correction. New pagination or order
decisions belong in restoration overlays, leaving the hashed cleanup files intact.
A source path/hash is the stable anchor; a reading position is not a page identity.

Keep JPEG masters byte-preserved. Rotate, crop or deskew only derived views when
needed, recording the transform back to the original. Keep originals available
beside the processed view. Retain a foldout intact and map its panels explicitly;
one image can contain several printed pages. Do not force all issues into one
filename-to-folio offset or automatically split every wide image.

Check the JPEG input integration with a small upright page, a sideways view, an
intact foldout and the known July order correction. Check hash rejection, bounds,
coordinate round trips, duplicate order slots and source-to-crop correspondence.
These establish correct image input to the existing pipeline; they do not reopen
OCR engine qualification or start unrelated issues' article restoration. Run the
relevant existing PDF regression checks if shared code changes, including a PDF
input example, so both source paths remain usable.

## 2. Restore one straightforward pilot

Start with **November 1984**: 246 retained scans, four identified cover faces,
no internal filename gaps and no known gross ordering anomaly. It adds new
coverage without immediately taking on damaged-source puzzles. This is a pilot
choice, not a claim that every physical page is present.

Pin its current TOC identities and cleanup records. The first article candidate
is **편집자 노트**, `maso-1984-11-toc-0034`, with catalog page reference **17**.
Locate it visually and establish its actual extent and neighboring material
before mapping; the catalog reference does not establish `page-017.jpg` or its end.
If it exceeds the pilot bound or is unlocated, record that outcome and choose a
shorter located TOC article in the same issue.

Restore that one short prose article end to end: map, OCR, correct against the
scan, retain figures/captions where present, export JSON/assets and rebuild it
independently. Compare all pilot reading text and every mapped region with the
source. Then qualify a listing/table/figure example from the same issue in a
separate bounded checkpoint. Choose it after inspecting the actual layout;
candidate counts and TOC ordering alone do not establish its extent.

The scan-input pilot passes when the project's schema represents the article's
logical structure and relationships, source coverage is accounted for,
uncertainties remain explicit, assets and ranges point to the right occurrences,
and the complete JSON/assets package reproduces without fresh OCR or dependence
on a presentation build. Text readability alone does not pass this gate. This checks the new inputs
through the established workflow. It does not repeat the completed PDF OCR engine
experiments. A successful OCR command or an image-only exception alone does not
pass this gate.

## 3. Use the established bounded workflow

For each named batch, record its TOC IDs, selected sources, expected extent,
limits, outputs and next step before running OCR. Keep the existing limits:
**at most two articles and six distinct source-page views**, whichever comes
first, plus **at most twenty outside-scope lookup pages**. Count separately mapped
foldout panels as separate views and record the original image count as well.
Segment longer articles and assemble their preserved segments separately.

Use mapped, pinned **Tesseract** by default. Qwen remains opt-in assistance with
a recorded reason and region scope. Do not repeat an engine comparison for every
issue. Reuse successful OCR when input bytes, maps, settings and implementation
match. Preserve failed attempts; allow one targeted repair/retry per failed region
in a batch and defer further recovery as a named task.

Check reading order, omissions and figure associations against full pages, then
review the selected text against its regions. Pay special attention to Korean
columns, listing rows and wraps, identifiers, DATA/hex literals, table cells and
blanks, captions and cross-page joins. Preserve printed mistakes and uncertain
glyphs rather than repairing historical programs by expectation. Execution and
original encoded bytes require separate evidence.

Use canonical TOC identities, retaining received titles and observed source-title
differences separately. Classify headings and shared-body references without
duplicating article bodies. Restore eligible TOC-listed content and covers;
retain advertisements, forms and other unlisted scans in the source set without
automatically turning them into article transcriptions. Explicitly account for
TOC-listed indexes/notices rather than silently dropping them.

Availability (`readable`, `partial`, `image-only`, `failed`, `unresolved`) and
review status stay separate from reproduction results. `readable` is an existing
content-availability value, not the restoration objective or proof of a
reproducible package. Report completed schema-based packages and their rebuild
evidence as restoration progress, with availability, gaps and review level as
separate attributes. Assistant sample review is not human acceptance.
A failed OCR attempt is not a missing page; an unlocated article is not proof of
source absence. Record source-linked uncertainty and damage without inventing
replacement text or imagery.

## 4. Finish the pilot issue, then expand

Complete November 1984's issue accounting and checked export before starting
another issue's article restoration. Passing the pilot establishes the workflow;
it does not mean the whole pilot issue is already restored.

Next, do a small **supplementary-source check for March 1984**. Its existing
word-processor article is partial because printed **250–251** are absent from
the supplied PDF. Inspect whether those actual folios are present and legible in
the donated JPEGs. Matching filenames are insufficient. If usable, restore a new
source-linked supplement and assemble a new revision, preserving the original
PDF package and its historical missing-source outcome. Otherwise retain the gap.
February 1984 likewise needs targeted source comparison only where there is a
documented gap or improvement worth making.

Continue the remaining new issue dates chronologically from the
[cleanup index](PROGRESS-SCANS.md), skipping already completed scan work. Keep
these known cases in view:

| Case | Treatment |
| --- | --- |
| February 1984 and December 1985 wide scans | Inspect intact foldouts before interpreting filename gaps as missing pages |
| March 1984 | Keep uncertain late-page order explicit; bound any location research |
| June 1987 | Scans 191–192 exist despite the donor note; verify the needed content |
| July 1987 | Consume the corrected reading list; retain cut-out alternatives outside the primary sequence |
| January, March, April, August and December 1987 | Carry documented absent spans into affected article outcomes |
| December 1987 rear cover | Retain the visible torn corner; cosmetic reconstruction is separate work |

Do not reopen unrelated old PDF/CD articles merely because new scans exist.
Record source choices per article or segment, with explicit cross-source joins
when combining evidence. Keep canonical article IDs stable across source variants.

## Outputs and progress

Preserve the cleaned source files and their review records in place. Add work
alongside them, outside `pages/`, `covers/` and `extras/`:

```text
archive/scans/YYYY-MM/
  restoration/batch-NN/    maps, derived views, raw OCR, corrections, attempts
  packages/               checked immutable article and segment exports
  reference/              selected issue JSON/assets export
  evidence/               rebuild comparisons, accounting and handoff
metadata/catalog/scan-restoration/
                          small tracked queues, ledgers and result records
```

Use fresh package directories. Preserve source snapshots, runtime/implementation
pins, raw OCR and correction evidence; Git alone is not a backup of `archive/`.
Keep disposable rebuilds under `work/validation/` and reader outputs under `dist/`.
Reuse earlier validated checks when their inputs have not changed; there is no
need to rehash all 59 ZIPs or copy all previous restoration files in every batch.

Update the new restoration progress index at milestones, write short per-issue
batch records, and commit each completed bounded checkpoint and issue closeout.
Keep the cleanup progress as a completed source-preparation record. Time new work
prospectively and record real workload/retry counts without estimating historical
review time. If a task stalls across three consecutive context windows, preserve
the partial result and report the blocker, following the existing PDF work rule.

An issue closes when every canonical identity has an evidenced outcome, every
source image is accounted for as selected material/cover/insert/alternative/other
or an unresolved case, and ownership, continuity, assets, ranges and a fresh
selected-package rebuild check pass. Distinguish source images, mapped panels,
printed folios and eligible body pages in the totals. Include known gaps and a
reproduction/next-work handoff. After the queue is done, reconcile the collection.

HTML generation, reading-room integration, deployment, full human proofreading
and cosmetic page reconstruction are later tasks. This campaign delivers the
restored JSON/assets and faithful source evidence first.

## First executable checkpoints

| Checkpoint | Saved result | Acceptance |
| --- | --- | --- |
| R00 — scan input integration | Minimal JPEG input support, November input/TOC pins, focused checks | Same OCR pipeline accepts the scan views; existing PDF input and behavior remain compatible |
| R01 — short prose pilot | One located November article, raw OCR, corrections and checked package | Full pilot text/region review and independent identical rebuild |
| R02 — contrasting layout | Bounded November listing/table/figure sample and its evidence | Rows/cells/assets/continuations accounted for; any failed prerequisite repaired before scaling |
| R03 — Apple FORTRAN | Complete final installment, compiler/symbol/output fields and original plot | 231 identical native files, 355 indexed table cells, explicit source uncertainty |
| R04 — contest commentary | Complete two-page commentary, entrant table and recovery evidence | 45 identical files, 40 indexed cells, exact continuation joins and bounded OCR retry |
| R05 — Basic Techniques | Complete final installment, independent listings and history table | 118 identical files, six captioned contexts, 58 numbered entries and 21 history cells |
| R06 — source contents classification | Six non-owning headings and bounded feature probes | Fourteen identical files, six pixel-exact contexts, canonical relationships retained |
| R07 — Feature I opening segment | Actual 18–23; whole feature remains partial | 179 identical native files, three tables, four code contexts, four original figures; explicit continuation pending on 24–39 |
| R08 — Feature I middle segment b | Actual 24–29; whole feature remains partial | 170 identical native files, six code contexts, two binary examples, five original figures; pending sentence join onto 30 |
| R09 — Feature I middle segment c | Actual 30–35; whole feature remains partial | 147 identical native files, three code contexts, three tables, nineteen mathematical occurrences and six original figures; 36–39 and assembly pending |
| R10 — Feature I final segment d | Actual 36–39; whole feature remains partial | 145 identical native files, four monitor contexts, three byte tables and twelve original figures; all 22 source pages covered in separate segments, assembly pending |
| R11 — complete Feature I assembly | Actual 18–39; complete native article package | 650 identical files; typed source indexes, uncertainty and source links preserved; four original segments unchanged; 229 shared tests pass |
| R12 — Feature II opening segment | Actual 40–45; whole feature remains partial | 192 identical native files; two tables, three code contexts and three original diagrams with typed source relationships; listing continuation onto 46 explicit |
| R13 — Feature II middle segment b | Actual 46–51; whole feature remains partial | 152 identical native files; 185 numbered units, original screen and two flowcharts; GOODMUSIC final part and MINI ORGAN listing continuation retained |
| R14 — Feature II listing segment c | Actual 52–57; whole feature remains partial | 65 identical native files; 692 numbered rows, 4,844 independent source fields and typed data/routine groups; listing 1 ends and listing 2 begins on 55 |
| R15 — Feature II final source segment d | Actual 58; all source pages covered, whole assembly pending | 17 identical native files; 116 numbered rows, 812 independent fields, fourteen typed routine groups and final A3E7 RET source evidence |
| R16 — complete Feature II assembly | Actual 40–58; complete native article package | 435 identical native files; three program joins, TW/SOUND2 group joins, 1,143 physical rows, 7,747 fields and six original typed diagrams; 232 regression tests pass |
| R17 — 개구리 | Actual 66–69; complete native article package | 78 identical native files; 314 physical rows/284 logical units, 473 DATA tokens, 68 explanatory table cells and original screenshot relationships; twelve local uncertainties retained |
| R18 — 3차원 우주전쟁 | Actual 70–74; complete native article package | 70 identical native files; 418 physical rows/403 logical units, 118 DATA positions including eight blanks, 22 sprite-data groups and thirty explanatory cells; original editorial illustration retained |
| R19 — 미로II | Actual 75–77; complete native article package | 70 identical native files; 142 physical rows/83 sparse logical units, 112 explanatory cells, literal 109/46-character hex strings and five coordinate DATA groups; original screenshot relationships and eight local uncertainties retained |
| R20 — 아기펭귄 opening segment a | Actual 78–83; whole article remains partial | 133 identical native files; 28 variable definitions, 43 explanations, nine nested branches, two continued cells, three listing contexts and 61 scan-linked custom-glyph runs; 3240 remains open onto 84 |
| R21 — 아기펭귄 continuation segment b | Actual 84–85; all source pages restored, assembly pending | 25 identical native files; 280 physical rows, 222 printed statements plus incoming 3240 fragment, 48 maze fields, eight GAME OVER groups, ten key assignments and 90 graphic/run occurrences; original 5460 END retained |
| R22 — complete 아기펭귄 assembly | Actual 78–85; complete native article package | 167 identical native files; 456 logical BASIC units from 592 physical rows, both monitor contexts, 142 table cells, 151 graphic/run records, overlapping artwork placement and 22 resolved source relationships; 239 regression tests pass |
| R23 — 컨닝 | Actual 86–89; complete native article package | 75 identical native files; 223 numbered units / 253 physical rows, 76 table cells, 223 DATA tokens including split 14, original screen/closing emblem, five uncertain key-label occurrences and literal source anomalies retained |
| R24 — 배고픈 거미 | Actual 90–92; complete native article package | 59 identical native files; 226 numbered units / 253 physical rows, 36 table cells, six sprite DATA groups / 192 hex fields, 22 web-coordinate pairs, nine fruit triples, cross-page 1270 and original DRAW/PLAY fragments; 21 local uncertainties retained |
| R25 — 로즈런너 opening segment a | Actual 93–98; whole article remains partial | 101 identical native files; independent setup, complete BASIC 1000–5410 / 463 physical rows, monitor 0C00–0C60 / 99 byte fields, twelve paragraphs, 24 variable fields, 140 drawing commands, original screenshots/captions and explicit 99–101 continuation |
| R26 — 로즈런너 continuation segment b | Actual 99–101; all source pages restored, assembly pending | 33 identical native files; 324 monitor rows, 721 byte fields, 95 blank operands, fourteen repeated BRK/??? runs, original INA/E8 and final 0F33 FF ??? retained; four local glyph alternatives |
| R27 — complete 로즈런너 assembly | Actual 93–101; complete native article package | 143 identical native files; three contexts, 831 physical rows / 810 logical units, 820 monitor byte fields, source alternatives and prior-address relationship; 242 shared regressions pass |
| R28 — 깡통이 통-통-통 | Actual 102–104; complete native article package | 72 identical native files; 119 BASIC rows, 75 table cells including a continued definition, eight paired grids / 1,536 observed cells, sixteen DATA groups / 192 fields, original illustration/screen/emblem and explicit prose/listing mismatch; four local uncertainties |
| R29 — 수학을 통한 논리학습 | Actual 110–115; complete native article package | 211 identical native files; 76 mathematical trees, forty exercise items, four independent listings / 240 logical units / 245 physical rows, 96 explanation cells and two original area diagrams; 37 invalid structural cases rejected |
| R30 — 리스즈트 opening segment a | Actual 140–145; whole article remains partial | 216 identical native files; five usage steps, nine properties, 27 numbered formatter groups / 67 physical rows, original memory layout / eight slots and flowchart / seventeen nodes / 27 connectors; 146–153 and assembly pending |
| R31 — 리스즈트 middle segment b | Actual 146–151; whole article remains partial | 153 identical native files; 102 LISZTER groups / 480 physical rows, nine bracketed continuations, 107 DATA strings, twelve report pages and typed source relationships; group 111, 152–153 and assembly pending |
| R32 — 리스즈트 final source segment c | Actual 152–153; all source pages covered, assembly pending | 47 identical native files; 59 groups / 96 physical rows, thirty variable definitions with two qualifiers, three loop pairs, original control-display alternatives/report/illustration; 49 invalid cases rejected |
| R33 — complete 리스즈트 assembly | Actual 140–153; complete native article package | 425 identical files; 187 logical groups / 643 physical rows, separate MAKE LISZT/LISZTER contexts, same-group 111 join and every original source structure; 45 invalid cases rejected and 246 fresh regressions |
| R34 — 전산개발 시스템 연구 | Actual 154–159; complete native article package | 212 identical files; five layouts / 52 fields / twenty ruler bands, 111 cells / 59 blanks, two flow graphs, three screens / nineteen UI fields and original evaluation report; 54 invalid cases rejected |
| R35 — 의료보험 수가계산 opening segment a | Actual 160–165; whole article remains partial | 92 identical files; 52 retrospective entries, 120 report cells, 131 logical program units / 194 physical rows, 29 DATA strings and original illustrations/captions; 53 invalid cases rejected |
| R36 — 의료보험 수가계산 final segment b | Actual 166–168; all source pages restored, assembly pending | 21 identical files; 141 logical units / 189 physical rows, 68 numeric DATA fields, fourteen department strings, ten classification labels and original prose-number disagreement; 47 invalid cases rejected |
| R37 — complete 의료보험 수가계산 assembly | Actual 160–168; complete native article package | 122 identical files; 272 logical units / 383 physical rows, 52 retrospective entries, 120 report cells, explicit 21010/21520 boundary and all source relationships/alternatives; 44 invalid cases rejected and 248 fresh regressions |
| R38 — 어음 거래 관리 | Actual 169–173; complete native article package | 148 identical files; four independent programs, 303 logical units / 628 physical rows, 55 reference rows / 110 cells and 97 local alternatives; 53 invalid cases rejected and 249 fresh regressions |
| R39 — ISAM | Actual 174–179; complete native article package | 178 identical files; two printed listing contexts, 116 logical units / 132 physical rows, typed linked-record/memory-disk structures, 149 cells / 15 blanks and eleven connectors; 53 invalid cases rejected; unchanged 249-test baseline reused |
| R40 — 비지캘크 한계의 극복 | Actual 180–184; complete native article package | 212 identical files; eighteen grids / 615 cells / 45 blanks / thirty formulas, eleven command sequences and typed aggregation/transfer relationships; 63 pixel checks and 58 invalid cases; unchanged 249-test baseline reused |
| R41 — 텍스트 화일이란? opening | Actual 185–190 of observed 185–195; complete native opening segment | 286 identical files; four typed diagrams, 49 record-strip slots, six blank hierarchy slots, eight connectors, eleven command-format groups / 23 logical commands; 74 pixel checks and 49 invalid cases; unchanged 249-test baseline reused |
| R42 — 텍스트 화일이란? final segment | Actual 191–195; complete native final segment, article assembly pending | 161 identical files; comparison table / 54 cells, paired record diagrams, one program / 227 numbered units / 281 physical rows / fourteen source sections, three DATA strings, eight printed map rows / 64 hex tokens and six logical command formats; 41 pixel checks and 68 invalid cases; unchanged 249-test baseline reused |
| R43 — complete 텍스트 화일이란? assembly | Actual 185–195; complete native article package | 456 identical files including 447 exact embedded segment files; source graphs, commands, mixed coordinate owners and fifteen reviewed prose/listing references; 115 pixel checks, 55 invalid cases and 253 fresh regressions |
| R44 — EPROM programmer opening segment a | Actual 198–201 of observed 198–205; whole article remains partial | 152 identical native files; 28 unnumbered pin terminals, 177 table/grid cells, seven cross-section nodes, eight block connections, twelve timing rows / fourteen connectors and source POKE example; 40 pixel checks and 69 invalid cases; unchanged 253-test baseline reused |
| R45 — EPROM programmer final segment b | Actual 202–205; all source folios restored, article assembly pending | 119 identical native files; three flowcharts / 30 nodes / 30 edges, circuit / 243 printed fields / 65 wire groups, one program / 43 units / 46 physical rows and five bibliography entries; 28 pixel checks and 81 invalid cases; unchanged 253-test baseline reused |
| R46 — complete EPROM programmer assembly | Actual 198–205; complete native article package | 280 identical files including 271 exact embedded segment files; scoped flow/circuit structures, separate command/program contexts, source-owned paragraph continuation and caption qualification; 68 pixel checks, 89 invalid cases and 258 fresh regressions |
| R47 — MAX-PRINT | Actual 206–208; complete native article package | 87 identical files; one Z80 listing / 212 source rows / 278 printed object bytes, two captioned BASIC examples plus an unassigned panel / 36 rows, ten table cells and typed byte/color diagram; 21 pixel checks, 84 invalid cases; unchanged 258-test baseline reused |

Immediate next action: **R48**, establish **SPC-CLOCK**,
`maso-1984-11-toc-0030`, from its catalog opener **212** and adjacent source
material. Confirm actual full extent, observed title/byline, body ownership and
program/table/figure structures before mapping. Keep at most two identities,
six new mapped source views and twenty outside lookup views; segment if needed
and assemble separately. Do not infer its end from the next catalog entry.

Preserve complete **MAX-PRINT**, `maso-1984-11-toc-0027`, on **206–208** as
`max-print-r01`, observed subtitle **텍스트화면과 그래픽화면의 장점만 보완** and
byline **SPC-1000 / 황 건 순**. All **87 native files** reproduce byte for byte.
Its one Z80 listing retains **212 physical rows**, repeated comment addresses,
**1,272 assembler fields**, **278 independently printed object bytes** and nineteen
source-symbol bindings. Keep the two captioned BASIC examples and uncaptioned
middle **250–300** panel as three distinct contexts, totaling **36 rows**. The
middle panel's owner remains unset; do not join it by row-number or syntax
plausibility. Three printed listing captions keep their actual frame owners.
The color table retains ten cells. The source byte/color diagram retains its
hatching, blank slots, horizontal/vertical elisions, four two-bit cells and legend;
printed **191** remains unchanged. All **21 pixel checks** and **84 damage cases**
pass. The unchanged **258-test R46 baseline** is rehashed and reused, not freshly
rerun. Keep all twelve local uncertainties, including source address/byte glyph
candidates, and the original wording; no execution or encoded-byte claim is made.

Preserve complete **198–205** of **애플 EPROM 프로그래머의 제작** as `eprom-r01`,
with immutable `eprom-a-r03` and `eprom-b-r02`. All **280 native files** reproduce
byte for byte, including **271 exact embedded segment files**. Scoped flow/circuit
identities and mixed coordinate owners remain explicit. The opening POKE command
and final program retain separate contexts and exact source bytes. The **더 / 욱**
logical paragraph continuation across 201/204 retains both frozen source blocks
and intervening figures. Printed figure 4 is qualified by its actual caption;
reference 5 and the uncaptioned circuit remain unresolved. All **68 pixel checks**,
**89 damage cases**, **11,101 coordinate comparisons** and **258 fresh regressions**
passed. The opt-in `regional-literals-v4` assembly contract retains older behavior.

Preserve final `eprom-b-r02` on **202–205**, including the clockwise source views
on 202/203, three flowcharts and R/W connector pairs, 51 circuit components/symbols,
243 printed fields, 175 endpoints and 65 source wire groups. Host and EPROM address
labels remain distinct. Keep bus elisions, unnumbered terminals, the unvalued LED
resistor and unmarked CE/D1 crossing qualified; do not complete them from external
pinouts. Retain 43 program units / 46 physical rows, three wraps, eight quoted
strings, five named REM sections, code token fragments and all five bibliography
entries. Source indentation and two blank display bands are metadata, without
original-byte claims. Preserve fourteen local uncertainties and original technical
wording. Figure 4 is observed; the circuit has no printed caption. Reference 5
remains unresolved, rather than receiving an invented caption.

Preserve immutable `eprom-a-r03` on **198–201**, observed title
**애플용 EPROM 프로그래머의 제작**, with bylines **이 우 빈** and **이 용 훈**.
Its 152 native files reproduce exactly. Keep the 28 unnumbered terminal labels
with three overbars and physical sides/rows, register header hierarchy and bit
groups, spanning A-port field and bracketed B bits 3/4, cross-section pointers,
block graph and timing arrows/loop. The two source **그림 3** captions, **RGM**,
prose **CS** beside pinout **CE**, original wording and nineteen local uncertainties
remain explicit. The 201 prose ends **더** and continues on 204 after the two
full-page diagrams; do not infer missing text from that layout. Reference
**그림 4, 5** requires the qualification above. No original device
operation, exact encoded bytes or full human proofreading is claimed.

Preserve complete **텍스트 화일이란?**, `maso-1984-11-toc-0024`, on **185–195**,
credited to **편 집 부** under **애플 컴패티블**, as `text-file-r03` and its
immutable `text-file-a-r02` and `text-file-b-r02` segments. All 456 native files
reproduce byte for byte, including 447 exact embedded segment files. Fifteen
reviewed prose/listing references retain their source evidence; the frozen marker
capturing “리스팅 3” within “리스팅 3190에서 3220” remains unchanged, with an
explicit containing context and checked 3190–3220 source-unit targets.
Final 191–195 retains table1's 54 cells, blank header, row group and footnotes;
the paired blocked/delimited record diagrams; and one printed program with
227 numbered units, 281 physical rows, fourteen REM-labeled sections, three DATA
strings and eight quoted map rows / 64 hex tokens. Keep the three cross-column
statements, split identifiers/destination digits, thirteen-selection/twelve-target
menu discrepancy, missing semicolons, FILENAMQ and SILICON VALLY. The selected
30-space BLANK$ literal follows source REM30; its original byte count and physical
allocation remain unverified, with the selected 15/15 allocation explicitly
editorial. Keep rule/quoted spacing and glyph alternatives without repair.
Preserve opening `text-file-a-r02` on 185–190:
the original slanted opener/photo/four diagrams, hierarchy/analogy arrows,
six blank file slots with second-slot hatching, 49 visual record slots with
stacked C-over-R labels and literal zero-like glyphs, eleven source command
formats and their physical wraps/alternative branches. Keep FILEANAME,
TEXT.SEQ, POSIT-TION, incomplete punctuation, original technical wording and
local glyph/handwriting alternatives. These are source structures without
recovered-byte or execution claims. The complete assembly preserves both source
segments and all 165 local uncertainties without fresh OCR.
Preserve complete 비지캘크 한계의 극복
on actual 180–184: eighteen grids, 615 source cells including 45 blanks and thirty
formulas, printed labels, separator bands, six boxed inputs, six block-range
rectangles, eleven command sequences and their formula/file/state relationships.
Keep source373/A2/Visi-um/circled1 discrepancies, difference values, final
C18/D18=32/52 and local glyph candidates. Circled return marks and plain R remain
distinct source displays; no missing filename return, recomputation or replay.
The selected r02 corrects an assistant review-note error: E5=218 agrees with the
printed inputs. All 615 source cells and article text are unchanged from r01;
the first package and evidence remain frozen. All 212 native files reproduce
exactly; 63 pixel checks, 58 negative cases, 38 earlier selected packages/evidence
and frozen r01 preservation pass. Shared implementation and operating
plans remain unchanged; the 249-test baseline/logs are rehashed and reused.
Preserve complete ISAM
on actual 174–179, its two separate printed listing contexts and exact source
1~630 replacement relationship, original diagram records/header groups/blank
slots/ellipsis bands/link paths, five operations/fifteen steps, seven variable
definitions and 28 algorithm references. Keep original PART$/PART, average40,
PRINT IE at listing1/914, repeated NEXT statements, Division reminder and local
letter/number alternatives. The repeated student name is 강부옹 in both tables;
earlier misread candidates remain preserved. Its 178 native files reproduce
exactly, all 46 pixel crops and 53 negative cases pass, and 37 earlier selected
packages/evidence remain exact. No shared implementation changed; the R38
249-test baseline/logs are rehashed and reused, not freshly rerun. Preserve complete
어음 거래 관리 on actual 169–173, including separate MENU/LIST1/LIST2/LIST3
contexts, repeated source numbers/routines, the same2000 column continuation,
record/control definitions, original prose/load-name/punctuation discrepancies
and 97 local glyph/blank-count/zero-O alternatives. Its 148 native files reproduce
exactly; all 34 pixel checks, 53 invalid cases and fresh 214 PDF / 35 JPEG tests
pass. Two disjoint crop repairs retain all original recognition. Optional exact
note dispositions qualify only annotations outside a reused bundle's scope;
selected notes, geometry and source metadata retain strict matching.
Preserve complete
의료보험 수가계산 on actual 160–168 and both immutable segments. Its 122 native
files reproduce exactly; all 26 pixel crops, 44 negative cases and fresh
214 PDF / 34 JPEG-recognition-assembly tests pass. The opt-in observed numbered
join preserves spaced BASIC numbers and physical wraps without inferred missing
instructions. Keep all 52 retrospective entries, 120 report cells/metadata,
272 logical units / 383 physical rows, DATA and source relationships, original
22000 and 22530/22532 prose disagreements, and 34 local alternatives. Original
encoded bytes and execution remain unverified. Shared OCR/PDF plans are unchanged.
Preserve complete 전산개발 시스템 연구
on actual 154–159, including all original layouts/ruler bands/blank fields,
seven-column I/O grids and their unusual value placement, two flow graphs,
report/screen examples, evaluation cells and local alternatives. Its 212 native
files reproduce exactly; all sixty crops and 54 invalid structural cases pass.
No shared code changed; the unchanged 246-test R33 baseline was rehashed and
reused, not freshly rerun. Preserve complete
리스즈트 on actual 140–153 and its three immutable source segments. The qualified
opt-in `structured-formatted-v1` mode retains multiple code blocks per program,
original formatter annotations and a same-number logical fragment join. Its
independent 425-file rebuild, all-source-record audit, 101 pixel checks and fresh
214 PDF / 32 JPEG-recognition-assembly tests pass. Keep both program identities,
107 DATA strings, original diagrams, definitions/qualifiers, three control-display
alternatives and both source reports; the 187 logical / 643 physical row counts
are source observations, not execution or recovered-byte claims.
Preserve source formatter output without inventing control bytes or executable REM/colon
tokens or normalizing printed anomalies. Preserve complete 수학을 통한 논리학습 on actual 110–115,
including fraction/root grouping, long-division notation, repeated exercise terms,
four independent source programs and local uncertainty. Preserve complete
깡통이 통-통-통 on actual 102–104, including the cross-column explanation cell,
independent paired-grid observations, all DATA occurrences and original prose/
listing mismatch. Preserve complete 로즈런너 on actual 93–101, its three source
contexts and all immutable segments/evidence. The explicit address join and v2
coordinate projection are qualified; frozen v1 packages remain reproducible.
Preserve complete 배고픈 거미 on actual 90–92,
including the numberless incoming 1270 fragment, selective 2470 explanation,
original sprite groups, numeric groups, macro strings and local uncertainty.
Preserve complete 컨닝 on actual 86–89,
complete 아기펭귄 on 78–85 and both immutable segments, including the same-unit
3240 join, all uncertain graphic runs, continued cells and original source relationships. Original segment
exports, frozen evidence and OCR map/settings bindings must remain exact.
November now has twenty-five complete article packages, no partial articles, six non-owning
headings and nine unclassified entries. Complete Feature II on 40–58 retains three
unified program identities,
both split source groups and all original diagram relationships.
Preserve complete Feature I on 18–39 and its four original segments.
JPEG assembly is now integrated and checked; use the same source/structure and
fresh native rebuild gates for later long articles. Whole-issue export remains
to be checked before first use.
Then continue the remaining articles in bounded batches through issue closeout.
R01 delivered the editorial; R02 Bit
Pattern; R03 the complete four-page Apple FORTRAN installment with separate
compiler/output/symbol contexts and an original plotted figure; R04 the two-page
contest commentary and nine-entrant table; R05 the three-page final Basic
Techniques installment and its six code examples; R06 six source-backed group
classifications; R07 the opening six-page Feature I segment with typed table and
assembler fields, source-linked BASIC wraps and original figure labels; R08 the
next six-page segment with three independent assembler listings, annotated
monitor/carry examples and structured source diagrams; R09 the next six pages
with literal mathematical occurrences, colour/address tables, two complete
assembler listings, an independent BASIC example and observed dot grids. November remains
in progress. R10 preserves the final four pages, original monitor/table examples,
and source-linked dot-size/grid structure. One targeted text-crop repair added
optional region selection and disjoint evidence reuse to the shared PDF/JPEG
pipeline, with 225 regression tests and both shared plans unchanged.
R11 assembles complete Feature I with projected typed indexes, exact source
relationships and the 29/30 sentence join. All 650 native files reproduce;
229 shared tests pass. Whole-issue export remains to be checked before first use.
R12 restores Feature II's opening six pages with 156 header/data cell positions,
five spanning octave labels, 126 numbered code units, twelve mathematical
occurrences and three original diagrams. The flowchart records 35 observed nodes
and 45 connectors without execution-based repairs. All 192 native files reproduce
exactly; four local glyph uncertainties and the outgoing listing continuation
remain explicit. Shared implementation and both shared plans are unchanged.
R13 preserves the next six pages: GOODMUSIC's final 53 rows, its independent
timing excerpt, MINI ORGAN prose and three original figures, and the first 116
rows of its character-definition listing. Typed structures retain 1,279 source
fields, 322 data literals, ten label-delimited data groups and 168 figure labels.
The two flowcharts distinguish printed shapes, connector junctions and routine
expansions without execution claims. All 152 files reproduce; nine local glyph
uncertainties and the open program/data-group continuation remain explicit.

R27 completes 로즈런너, actual 93–101, by joining the original monitor address
boundary explicitly while keeping setup, BASIC and monitor contexts distinct.
The v2 source-index projection handles the new coordinate/graphic/caption forms;
frozen v1 assemblies retain their original conventions. All 143 native files
rebuild exactly, all 32 source crops pass pixel checks, all 25 earlier packages
still validate with exact bytes/evidence, and 242 shared regressions pass.
At R27, November had 14 complete articles, no partial articles, six non-owning
headings and 20 identities awaiting disposition. R28 then completed 깡통이 통-통-통
on actual 102–104; current counts and next work are listed above. The remaining issue scope includes every
unresolved identity, covers/source-image accounting and a checked whole-issue
native export/rebuild; the reading room remains a sample presentation.
