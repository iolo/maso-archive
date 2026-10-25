# Successor handoff — 2026-10-25

Storage: [what to preserve and where new work belongs](STORAGE.md). Historical paths remain available through compatibility links.

## Current human-review reader

The owner's 2026-10-22 request integrates all completed restorations into
`dist/reading-room-volunteer/`: 11 PDF issues/407 articles plus all three CDs/3,386
records, 3,793 total. Open `http://127.0.0.1:4189/#/review`; export local review
notes before changing browser origin. The prior nine-issue reader and the complete
new release are preserved under `archive/releases/reading-room-2026-10-22-*`.
See [the reader guide](READING-ROOM.md) and
`archive/pdf/shared/evidence/reader-integration-2026-10-22/validation.json`.
This local build adds no human acceptance and performs no deployment. March and October 1985 are later data-only closeouts and are not included in this 11-issue reader snapshot.

## Active restoration

November 1985 remains in progress: thirteen readable, assistant sample-reviewed
articles, one partial article and 32 unresolved identities. Batch 19 restores
Lessons from Apple 0009 final pages 86–88 at
`archive/pdf/1985-11/packages/batch-19-r01/apple-lessons-b`. All body pages 80–88
now exist in two immutable segments; complete assembly remains pending. Canonical
title and parsed byline fields remain unchanged, with no person byline inferred.
Both final-segment exports match across 119 files. All 2,285 text ranges, 2,373
evidence pins, 30 images and 109 disjoint nonfigure pairs validate.
The final segment retains 27 blocks, three original page images, 264 physical
text rows, eighteen named literals, five wrapped literals, twenty technical claim
literals, two pullquotes and three continuation links. The incoming page 85→86
sentence is recorded for assembly. Printed wording, source claims, shortened book
title and name-glyph alternatives remain; no technical or historical repair.
All 30 exact crops were inspected before 27 pinned OCR tasks, and all raw drafts
were read before one source correction pass. No crop repairs or recognition retries.
All 17,479 prior files, eighteen inventories and 30 core pins remain unchanged.
The unchanged 213-test baseline is reused, not rerun. Current preservation contains
17,950 files. Next batch 20 assembles the complete article 80–88 without new OCR.
Diskette 0032 still needs a location search after its TOC 72 mismatch. Cover,
all 266 pages and whole-issue closeout remain. Conversation, logs and documentation
use English; original source text retains its language. No reader rebuild.
Reproduce with `archive/pdf/1985-11/restoration/batch-19/reproduction.json`.
Assembly must retain every native metadata category, the original timeline and
photographic legends. Link the page 85 tail to page 86 using exact source ranges.
Preserve the two segments' independent name candidates and quotation variants.
Existing batch 17 Hangul feature, batch 14 PLAY and batch 09 numerical-analysis
adapters remain required for their complete assemblies.
See [November log](progress/8511.md) and the issue ledger.

## Latest completed issue

October 1985 is complete under the canonical TOC JSON/assets scope. All 39 entries
are accounted for by 35 readable, assistant sample-reviewed articles and four
non-owning headings. No partial articles, unresolved eligibility or article assembly
remain. Canonical identities, titles, order and parent relationships are unchanged.

The standalone index is `archive/pdf/1985-10/reference/issue.json`; the validation
report is `archive/pdf/1985-10/evidence/issue-closeout/report.json`. All 9,031 issue
files match the independent rebuild, including all 9,025 selected-package files.
The packages retain 2,416 regions, 1,662 blocks and 404 figures. All
301,480 local UTF-8 excerpt ranges and 2,412 distinct images validate.
Ten private assembly formats preserve their native files, metadata and source uncertainties.
Reproduce/check with `archive/pdf/1985-10/restoration/issue-closeout/reproduction.json`.

All 268 source pages are accounted for: 224 contain selected bodies, with 231 page
assignments, and 44 are outside-body material. Those comprise 34 advertisements,
two contents pages, an issue-title page, an association notice, five unlisted HGR
feature pages (the last also a promotion), and the cover. Seven shared article
pages have 228 disjoint region pairs, including 115 nonfigure pairs. All 25 native
exclusion records remain exact. Null folios, including PDF229, remain null; no
page offset is inferred. Unlisted material and mixed-page ads remain outside
canonical transcription. No article identity was added.

The donated cover is verified: 480×611 RGB JPEG, 68,837 bytes, metadata stripped,
with an independently identical thumbnail rebuild. Fresh
`make test-pdf PYTHON=.venv/bin/python` passes all 213 tests. All 73,927 earlier
files, 68 prior checkpoint inventories, 30 core implementation pins and ten
private adapters remain unchanged. All earlier attempts and source evidence remain.

All 68 restoration/accounting checkpoints meet the two-task/six-mapped-page/
twenty-outside-lookup limits. The 52 OCR checkpoints retain 2,012 mapped Tesseract
tasks (495 English code and 1,517 Korean/English other regions), one recorded
source correction pass each and zero recognition retries. Three timing supplements
from batches 32 and 46 remain explicit: one masked figure was inspected after OCR,
an early raw-reading record was superseded before correction, and two original
figures were inspected after launch but before correction. Text crops were reviewed
before recognition; no stricter chronology is inferred.

Human acceptance/full proofreading, source encoded bytes/spacing/glyph counts,
historical or technical claims, execution and independent backup recovery remain
unverified. News/classified body transcription and custom glyph/diagram labels await
volunteers. No reader was rebuilt. No October 1985 restoration checkpoint remains;
other issues and collection-wide aggregation are separate work.

## Read first

1. [OCR handoff](../PLAN-OCR.md): accepted engine policy, essential findings,
   source/review rules, metrics and commands. Do not read all trial logs to resume.
2. [PDF plan](../PLAN-PDF.md): JSON/assets scope and remaining campaign gates.
   August, September, October and December are complete. October's 35 articles and 260-page
   ledger are recorded in [the October log](progress/8410.md). December 1984
   is complete; its final accounting and source limitations are in
   [the December log](progress/8412.md). Restoration alone does not authorize a
   reading-room rebuild.
3. [October 1985 closeout validation](../archive/pdf/1985-10/evidence/issue-closeout/report.json),
   its completion audit/record and source-page accounting. Reproduce the standalone
   `archive/pdf/1985-10/reference/issue.json` with
   `archive/pdf/1985-10/restoration/issue-closeout/reproduction.json` and its pinned
   ten-format dispatcher. All 68 checkpoints and batch32/46 timing supplements
   remain retained. No October 1985 restoration checkpoint remains.

**Current OCR policy:** mapped Tesseract by default. Qwen is an opt-in draft or
second reading for difficult prose or code, with explicit layout/coverage review.
Do not restart completed comparisons or run both engines routinely. Historical
Qwen-first/adaptive assignments are superseded; measurements remain useful.

## Restoration state and boundaries

October 1984 accounts for all 41 TOC entries: 35 readable, assistant sample-reviewed
articles and six non-owning headings. All 260 PDF pages are classified and the
independent full issue rebuild is byte-identical. All 30,737 earlier evidence files
remain unchanged. Unlisted DOS TOOL KIT 41–43 and 통합 소프트웨어 241–255 are outside
canonical restoration scope. Human acceptance/full proofreading, source bytes and
execution remain unverified. News/classified body transcription is pending; many
program/numeric panels remain original images. Keep the batch 35 preflight timing
exception explicit: model confirmation of three revised crops followed OCR batch
launch, with per-region timing uninstrumented. Later source/crop/rebuild checks pass.

Completed JSON/assets issues are November 1983 and February, March, May, June,
July, August, September, October and December 1984. March retains its absent-source terminal
partial; no April PDF was supplied. February, March and October 1985 are also complete. Further issues and collection-wide aggregation are separate work.

December 1984 is complete under the canonical TOC JSON/assets scope: 30 readable,
assistant sample-reviewed articles and seven non-owning headings account for all 37
entries, with no partial articles or unresolved eligibility. The standalone index is
`archive/pdf/1984-12/reference-r01/issue.json`; the completion report is
`archive/pdf/1984-12/evidence/issue-closeout/report.json`.
Information parent0031, 정보모음, remains a non-owning organizational group;
all canonical identities, titles, parents and six child relationships are unchanged.

Advertising index0036 is complete in packages/advertising-index:21 files match
the independent rebuild. Its actual body is the lower panel of240/PDF242;upper
independent magazine advertisement excluded. Canonical TOC255 remains unchanged.
Four regions/three blocks/one original panel retain24 rows/48 cells/two ordered column
parts/no invented headers and24 literal name/reference pairs. Three cover references
표3/표2/표4 remain printed references,not inferred folios. Original tree/rules/240folio
and24 leader-dot bands retained as pixels without encoded-count inference. Source
고려씨스템산업 and 우신기술서적 remain literal candidates. No reference targets verified.

Closing editorial0037 is complete in packages/closing-editorial:53 files match the
independent rebuild. Actual PDF258 follows yearly-index final255 and precedes independent
TIGER advertisementPDF259. Source title1년을 정리하며 remains separate from canonical
편집후기/256. The source page has no visible folio and is mapped null. Twelve regions/
11 blocks/one full original page retain nine independently signed notes and one left→middle
column word continuation. Nine signature Unicode candidates retain their own scans;
no full author identities or article-wide byline inferred. Six ellipsis bands retain
explicit editorial placeholders with unknown original glyph counts. Original old spelling,
학생방/청승맞게 candidates and Eye Shoping remain without grammar/encoding repair.

Both packages retain1,206 exact UTF-8 ranges;14 localized source candidates andsix
unknown-band occurrences remain source-linked. Six whole views/five reused renders/one
new render;two mapped pages/four outside lookups/two canonical tasks. All16 exact original
crops viewed before14 kor+eng tasks. All14 raws read before one direct source pass;
zero OCR failures,retries,engine changes or crop repairs. Successful index/signature
omissions handled through recorded source-direct fallback. Initial excluded-region schema
failure retained;fresh mapping revision fixes metadata only before any map/crop/OCR output.
Recorder authoring preflight removed stray descriptive draft characters before execution;
all drafts retained. Source readings/maps/crops/raws/packages unchanged by those repairs.
All44,629 prior files,every prior inventory and29 implementation pins pass;current
preservation inventory contains 44,948 files. Unchanged213-test baseline reused.

All 260 source pages are accounted: 227 contain selected article bodies and 33
are other material (one cover, 25 advertising/promotion pages, one contents page,
one issue title page, four group dividers and one unlisted publisher contest notice).
All 33 outside-body pages were inspected in bounded checkpoints. Six native-map
advertisement exclusions and the separate lower-PDF132 accounting annotation retain
seven mixed-page advertisement exclusions. The CP/M native maps and upper-only crops
are unchanged; source-map null folios on PDF132 and PDF258 remain null.

The donated cover takes priority. Its verified RGB JPEG thumbnail is 480×639 and
63,964 bytes, with metadata stripped; the private derivative rebuild is byte-identical.
The donated source remains unchanged and private. All 30 selected packages retain
1,836 regions, 1,291 blocks and 509 figures. Their 6,573 copied files are exact.
The selected standalone issue and independent rebuild match across all 6,579 files
(2,040,045,506 bytes each); 1,752 unique image hashes decode successfully. Original
exports remain preserved; the selected revision changes only ledger/manifest metadata.

Fresh `make test-pdf` passes all 213 tests. All 45,068 prior files, every prior inventory,
29 implementation pins and 1,645 pre-closeout ledger pins pass. The final preservation
inventory contains 71,430 stable files, excluding its own file and later ledger/audit
supplements. All maps, crops, raw drafts, corrections, immutable natives and failed
attempts remain preserved. All 51 source checkpoints and two accounting checkpoints
pass the recorded two-task/six-mapped-page/twenty-outside-lookup bounds.

Source errors, unknown glyphs and volunteer news/classified-body/diagram-label
transcription remain explicit. Batch01's initial exact crops were inspected after
recognition; full pages preceded mapping, revised crops preceded recognition, and all
selected regions were visually reviewed. This exception remains in the final report.
Human acceptance/full proofreading, source encoded bytes, historical/technical claims,
execution and backup recoverability remain unverified. No reader rebuild.

Classifieds0034 is complete223–225/PDF225–227 at packages/classifieds:35 files
match the independent rebuild. Nine regions/six searchable title/category/running
headings/three complete original pages retain three categories,eight ordered body-image
fragments and three item-to-contact continuations. Original opening photo/art,all offers,
contacts,prices,headers,footers and terminal mark remain. Body transcription is pending
volunteers under the accepted classifieds-image policy;no historical contact/price claims
or source item counts inferred. Source title letter spacing remains independent from
canonical 복덕방. No body pages or assembly are pending.

Q&A0035 is complete237–239/PDF239–241 at packages/qa:194 files match the independent
rebuild. Fifty-six regions/43 source-corrected blocks/13 original images retain five
questions and answers,ten code groups/17 physical rows,two machine-code tables/six rows/
12 cells/four headers/six opaque addresses/18 hex pairs and five prose continuations.
Seven original circuit/logic/truth-table diagrams retain six separately transcribed
caption links. Diagram/pin/node/truth-table label transcription is pending volunteers;
all original pixels,including page239 crease,remain. Five question submitters are not
an invented article byline. No body pages or assembly are pending.

The printed MACINE CODE header,two different byte groupings,0DEH,$17DE and $17DEH,
42 memory claim,1/65536 probability,7FF/FH physical wrap,74 LS 157/74LS157,power/pin
claims,Japanese reference/superscript candidates and *F000L remain literal. Sixteen
localized candidates retain exact downloads/ranges and original scans. No spelling,
opcode,byte,address,hardware,math,logic,encoding or bibliographic reconstruction.
Human acceptance/full proofreading,source bytes and execution remain unverified.

Eleven reused whole views/six mapped pages/five outside lookups/two canonical tasks.
All65 exact original crops inspected before49 pinned tasks:ten eng code/39 kor+eng.
All49 raws read before one direct source correction pass;zero OCR failures,retries,
engine switches or crop repairs. Successful OCR omissions retained with recorded
source-direct fallback. One serializer audit failed on an optional excerpt field before
writing corrections/recipes;fresh revision fixes only that audit. Both attempts retained;
source readings/maps/crops/raws unchanged. Both packages retain1,587 exact UTF-8 ranges.
All43,699 prior files,every prior inventory and29 implementation pins pass;current
preservation inventory contains 44,629 files. Unchanged213-test baseline reused.
No reader rebuild.

Information radar0033 is complete at packages/radar-complete-r01, covering
printed pages 155–163/PDF157–165. The 197-file package matches its independent rebuild
byte for byte. All 189 files from immutable radar-a domestic155–160 and radar-b
foreign161–163 remain exact, including their full correction metadata and stage scopes.
No radar body pages or assembly remain pending. The final TI story, contact address and
terminal mark precede independent book advertisementPDF166. Business dividerPDF167
and memory166/PDF168 remain separate; no global folio offset was inferred.

All 63 native category occurrences, 66 explicit source/category slices and 559 exact
UTF-8 ranges reverse-project correctly. The package retains 50 regions, 41 searchable
heading/title/credit blocks and nine complete original page images. Twenty-six news
reports plus one integrated reader notice retain 27 ordered item identities, 34 body
fragments, seven continuation joins and 26 adjacent story links. Reader23→foreign24
and the section-transition record retain the prior domestic manifest pin.

Five uncaptioned photos, one original four-panel SNA diagram and one terminal mark
remain as source images. Evolution of SNA Networks is its searchable embedded title,
not an invented caption. Body and diagram-label transcription is pending volunteers;
all original body, photo, rule, header, footer, notice, diagram and address pixels remain
readable. Searchable headings do not establish corrected body prose or technical claims.

Sixteen localized source candidates retain exact combined ranges and original scans:
한승컴퓨터/body한송컴퓨터, 벨엘상사, 센타/센터, 32비트, DPQ-280, 바이컴-Ⅱ,
입찰및, 찾읍니다, reader credit윤찬규, MC 68000, 석권 예상, 재고,
SNA발표 10주년, Networks and 인공 지능용. The reader credit is not an article byline.
Source spelling, spacing, encoded bytes and historical/technical claims remain unverified.
Assistant sample review is not human acceptance or full proofreading.

Assembly required no new mapping, rendering, OCR or source correction. Four exact stale
native-stage deferral/assembly notes were resolved only in active package status;
all original notes remain. All 787 evidence-pin occurrences resolve through declared
source roots to 135 retained files. All 43,280 prior files, every prior inventory and
29 implementation pins pass; the current preservation inventory contains 43,699 files.
The unchanged 213-test baseline is reused. No reader rebuild.

Canonical0030,the yearly
back-issue index,is complete241–255/PDF243–257 at packages/year-index-complete-r01.
The 179-file complete package matches its independent rebuild byte for byte. All171
files from immutable packages/year-index-a opening241–246,packages/year-index-b
middle247–252 and packages/year-index-c final253–255 remain exact. No body pages or
yearly-index assembly are pending. Source opening12권은 이런 내용들이었읍니다.,
subtitle과월호 활용을 위한 찾아보기,running과월호 목차 and final 통합 소프트웨어 2
bound the actual extent before independent editorialPDF258. Advertising index240/PDF242
remains separate despite its TOC reference255. No printed byline invented from TOC편집부.

The complete article retains15 reviewed source pages,51 regions,32 blocks and19 original
images. All123 native category occurrences and12,432 current-native UTF-8 range occurrences
reverse-project exactly. Full native metadata and original stage scopes survive. Six
external original-download heading/month occurrences retain their own ranges and pins;
they are independently checked and are not shifted as combined-download ranges.

Eighteen table parts retain396 rows,1,570 logical cell positions and71 header fields.
Final255 has three columns 월/제목/내용;the other17 tables have four. There are87
printed month fields,286 platforms,396 titles,396 summaries and405 blank slots. Month
fields are issue references,not folios. Sixty-eight local merges cover280 slots;nine
incoming groups retain31 empty slots. Ninety-four literal blank platform positions remain,
plus two covered blank platform positions. No unprinted label or platform column invented.
Eighteen section-heading associations remain separate from captions;all19 originals are
uncaptioned. Original gray grids,handwritten arrow/box,framed cover montage and integrated
back-issue sale note remain complete without graphic reconstruction.

Twenty-three localized source candidates retain exact combined ranges/original scans.
Source84.12,2실2방,SPC-100 0,디오리지이엠,로즈런너,올림차순,독도는 우리땅/지도,
마이크로 챌크,분산분석과 회귀분석외,서북 편란법,Searc-hing,마담 뚜,SP-1000,
신판 UFO,로미티이,칼창,시대적 변경,본선 논제,데이트 공유 and MAX-PRINT description
word order remain literal. One source-mark extent between 알람 and 등 uses an explicit
editorial placeholder with unknown glyph identities/count. Roman/Greek/dash/ellipsis/
bracket/center-dot/quote glyph approximations and original encoded spacing stay unverified.
Historical/technical/scientific claims,prices/stock claims,old spellings and opening's
partly overlapped 그간 candidate remain unverified. No semantic/title/platform/chronology/
grammar/math/hardware/encoding repair. Original pixels remain authoritative.

No new mapping,render,OCR or source correction was needed for assembly. Six exact stale
native-stage notes were resolved only in active package status;all original notes/metadata
remain copied. All12,634 evidence-pin occurrences resolve through declared source roots
to140 retained files. All42,048 prior files,every prior inventory and29 implementation
pins pass;yearly-index preservation inventory contains42,431 files. The unchanged213-test
baseline is reused. A read-only inspection missed the documented PYTHONPATH;the first
verifier omitted expected source_segment on top-level structure pins. Both failed attempts
remain;fresh verifier corrects only its expected metadata field. Packages/source readings
were unchanged. Human acceptance/full proofreading,source bytes,claims and execution remain
unverified. No reader rebuild.

Relocator232–233 remains complete at packages/relocator:83 files/six originals/
7,057 exact ranges/134 hex rows/1,072 opaque pairs/1,206 cells. All rows have eight
pairs,including F140. Four caption links/three caption parts/two uncaptioned frames,
source정주원/동북중3/FC-100,boxed keys/downarrows and J/P,F/147 wraps remain.
Biorhythm234–235 remains complete at packages/biorhythm:56 files/seven originals/
2,482 exact ranges/97 physical rows/67 BASIC labels/30 continuations. Incoming208
continues380;230 crosses pages. Two ampersand/four box-rule extents remain unknown;
two Hangul display clusters remain unverified. Source40 A+SIN,330-6.283184#,
510INT(.4...),W.G.CHA/1984/8/6 versusW.K.CHA/1984/8,HIGH RESORUTION and screen
FORCAST/NEM versuscodeFORECAST/INT remain independent. Lower235 ad stays excluded.
The batch44 root-ledger evidence path revision and both failed audit attempts remain;
native packages,source readings and raw OCR were unchanged.

SPC-CLOCK226–231 remains complete at packages/spc-clock:236 files match its rebuild,
with68 regions/48 blocks/15 originals/6,348 exact ranges. It retains224 physical code
rows,155 assembly ordinals/1,085 independent columns,nine EQU fields,47 actual BASIC
labels and the physical120 &HD/2 wrap. Missing90 and noEND remain; two unknown
semicolon bands/17 opaque music strings retain originals. D000/ORG0EA00H,ERR/ERC/
EPR/EROR,E8CFH/E8CFF,proseE8/BASIC EA,CURST2/CURS.2,N4EQU5 and source spelling/
grammar errors remain independent. Five diagrams/four tables36 cells/three prose joins/
seven caption parts/nine links survive. 메아리0026 remains non-owning without body pages.

Black-white219–222 remains complete at packages/black-white:137 files match its
independent rebuild;38 regions/20 blocks/eight originals/6,286 exact ranges survive.
Its one BASIC program retains234 physical rows/147 labels/87 continuations; numeric-only
0 and000*X remain wraps. Three prose tables retain33 rows/77 cells;six title glyphs,
12 screen labels and the original board remain. Forty-six decorative dash/ampersand
bands have unknown counts; nine quoted runs/six space runs/boxed cursor/C/↑↓→→ remain
unverified. SOUND13;9,NC(1000),SC1~15,720L prose/710M code,두려워하거나 and all
physical keyword/string/decimal wraps remain. Two screen BLACK/WHITE occurrence ranges
retain their fresh metadata revision; original correction/text/OCR remain unchanged.

64 Column214–218 remains complete at column64-complete-r01:144 files match its
independent rebuild; all135 original native files remain exact. All92 category
occurrences/16,415 UTF-8 ranges,520 physical rows,17 originals and the incoming290
DEFGquote association survive. Two unknown bands,music O/0/repeat counts/quoted spaces,
D000/ORG0E800H,1180H,LOP?? and070D/0D07 fields remain source uncertainties. No pages
or assembly are pending. Contest review213 remains complete at contest-review:30 files.

Cryptography205–211 remains complete at cryptography-complete-r01:323 files match
its independent rebuild. All217 original native files and193-file opening metadata
revision remain;all74 category occurrences/5,964 UTF-8 ranges reverse-project exactly.
Thirty unknown bands,source discrepancies716111947/71611947 and all original notes
remain explicit. Use design_literal_assembly.check/installed() for selected packages;
retain all29 implementation pins and213-test baseline. No reader rebuild.

Design(6), canonical 0020,
is now complete at packages/design-complete-r01, observed 178–204/PDF180–206.
The 449-file package matches its independent rebuild byte for byte. All 440 files
from five immutable natives remain exact: design-a 178–183, design-b 184–189,
design-c 190–195, design-d 196–201 and design-e 202–204. Keep every native.

The complete article retains 27 individually reviewed source pages, 141 regions,
85 blocks and 56 original images. No body pages or article assembly remain pending.
The independent opening 178/PDF180, final OTOP/END 204/PDF206 and next cryptography
205/PDF207 establish actual extent. No global folio offset was inferred. The lower
independent book advertisement on PDF181 and non-owning headings on PDF179 retain
their original exclusions/classifications. Canonical identities/titles/parents unchanged.

All 279 native segment/category occurrences and 29,792 UTF-8 range occurrences
reverse-project exactly. Full original correction metadata remains in native_metadata;
every additional native array is projected with an explicit category slice. Ten tables
retain 113 rows/358 cells/37 header fields, including 39 patch rows/117 opaque
address-OLD-NEW fields. Fifteen caption links retain ten printed captions; 41 original
frames remain uncaptioned. Shared-caption, diagram, spatial formula and prose
associations retain their original source occurrences and every image anchor.

Thirty-four listing groups retain 1,759 physical rows, including patch rows and only
four actual BASIC labels 10,20,30,40. Twenty EQU fields, 216 label candidates,
69 complete quoted fields, 44 quoted operands and 84 quote runs remain literal.
Thirteen quoted message fragments preserve trailing spaces and RECORD STRAT.
Twenty-two storage fields, one ORG, two symbolic storage operands and port/bit/hex/
local-offset fields are opaque. No opcode, byte, address, target, alias arithmetic,
encoding, hardware, syntax or graphic reconstruction. Source errors are independent.

Physical 189/190 DISPLAY comment continuation stays separate without quote completion.
Final END remains on its leading-semicolon physical row. Three decorative bands
retain unknown glyph counts. The MEMOF comment-tail candidate remains unverified;
no MEMORY completion or missing-glyph count was inferred. Root manual-review links
now use complete-listing ranges and retain their original native occurrences.
Human acceptance/full proofreading, source encoded bytes and execution remain unverified.

Adapter design_literal_assembly was committed separately as b4d4b8a before export.
All 213 PDF tests passed; all 29 implementation pins remain unchanged through assembly.
The 14 exact stale stage-note deferrals were resolved only in active package notes;
all original notes/review arrays/native files remain intact. External evidence paths
were not rewritten: 30,281 pin occurrences resolve to 328 retained source files using
the declared original review roots. No new mapping, render, OCR or source correction
was needed for assembly. Earlier mapping/serializer/test failures remain archived.

All 34,760 prior files remain unchanged. The new preservation inventory contains
35,682 files. Source/geometry, every native/category/range/asset, physical rows,
quoted/message/storage/END fields, complete output/rebuild and ledger checks pass.
The 213-test baseline is reused for this data-only export. The issue remains in
progress; design is one completed article within the original full-issue goal.

VisiCalc 172–175 remains complete at visicalc-limits:154 files, five menus/52 options/
129 fields, three ROUND claims and one manual source word ⟦faint source word⟧ pending.
Body/page coverage is complete; CALCULATE/CALCULATION and 351.6763/results351.68/352/350
remain independent. Memory 166–171 at memory-efficiency retains 182 files/190 cells/
15 blanks/99 byte fields/46 physical rows/45 entries, source 위해서/canonical 위하여,
Rea Only Memory, 76 BE:6 and output 149/prose 191. Mathematics 152–154 remains at
math-montecarlo-r01:104 files/output 3.136. Business unpaginated PDF167 retains
source 비지니스/canonical 비즈니스. MSX 150–151 at msx-loader retains 147 physical rows/
134 entries and 박재현/TOC박제현. Perspective 131–149 at perspective-complete-r01 retains
all 384 natives, 134 repair, two captions, 143–148 listings and 87 middle matrix cells;
keep perspective-a, perspective-b-r01, perspective-c, perspective-d. CP/M remains at
cpm5-complete-r01,110–129 plus unpaginated upper PDF132; lower 132 ad excluded, no 130.
BASIC speed102–109 retains opening 102–107/ending 108–109. Selected checks use
design_literal_assembly.check/installed(), delegating perspective_literal_assembly,
cpm_literal_assembly and graphic_literal_assembly. Preserve all 29 implementation pins.

December closeout is complete. Reproduce the selected JSON/assets issue using
`archive/pdf/1984-12/restoration/issue-closeout/reproduction-r03.json` and the pinned
private inputs. Read `evidence/issue-closeout/report.json`, the complete source-page
ledger and retained source uncertainties before volunteer correction. No further
December restoration checkpoint is queued. That is the historical December handoff; February 1985 has since completed. No --preview or
reader/browser/frontend rebuild was performed.

Complete design evidence: restoration/design-assembly and evidence/design-assembly.
Use assembly-recipe.json/reproduction.json and implementation.json's three exact
pins plus the original 26 pins. The selected complete package is design-complete-r01.
Read-only verify-assembly.py verifies the independent 449-file rebuild, every 440 native
file and all 279 category occurrences/29792 UTF-8 ranges. External source-root pin
resolution is in external-evidence.json and verify-external-evidence.py. Fresh explicit
--report only. Source/header/caption/table/patch/message/storage/physical/quote/error
categories and all five original correction objects are preserved without inference.

The root ledger's pending unknown-band/MEMOF links now point into the complete
listing and keep original_native_occurrence. Do not convert the final semicolon END
row into an executable directive or normalize printed source mistakes. No design
native, crop, reading, raw draft, failed adapter/test attempt or source evidence may
be removed after promotion. Cryptography,contest review,64Column,black-white,SPC-CLOCK,relocator andbiorhythm are complete;메아리 is non-owning. Yearly index and radar are complete in their selected full packages. Information0031 remains non-owning; classifieds and Q&A are complete. Advertising index and closing editorial are complete; whole-issue accounting, cover verification, independent rebuild and closeout are complete.

Crowded Speedway remains packages/crowded-speedway-complete-r01,including final
69F8/eight00source revision. Its pinned table/literal tooling39e5b61 remains
unchanged;the new graphic dispatcher supports that format forwhole selected audits.

Spin Ball remains packages/spin-ball-complete-r02. Literal-source tooling
c27c183and its [format notes](PDF-LITERAL-SOURCE-FIELDS.md) remain preserved.
Keep its five-field final7BE0revision,earlier four-field observation and7B28typing
repair explicit.

Diamond Field remains at packages/diamond-field-complete-r01 with its original
metadata revision. BASIC field tooling eba1e08 is documented in
[the format notes](PDF-BASIC-SOURCE-FIELDS.md). Use its evidence/diamond-field-assembly/
verify-r02.py historical audit; retain earlier failed attempts. NeighborPDF66 is
an unpaginated publisher ad; native58–64shorthand is not an observed folio64 or a
global-offset claim. Reader integration is separate; the owner subsequently
requested the October reader build.

Private PDFs, raw OCR, model files and completed exports are not in Git. Preserve
source hashes, canonical IDs/parents, original evidence and user edits. Verify a
process is live before waiting/resuming; reuse successful stages. Close out an
issue before starting another. Earlier checkpoint “next” statements are historical.

## Reader integration — 2026-10-19

At the owner's explicit request, `dist/reading-room/` now includes October's 35
articles: nine PDF issues (329 records) plus 3,386 CD records, 3,715 total. The
original October closeout/packages remain unchanged. See [the reading-room guide](READING-ROOM.md)
for reproduction and the verified `reading-room-2026-10-19-october` snapshot.
All 5,218 files from the 35 packages and 124,113 inherited reader files are preserved;
nine Python tests, 25 frontend tests, production build and browser checks pass. Q&A
correspondents remain beside their questions after a focused display correction.
This is a local build; no deployment occurred.

### Previous September integration — 2026-10-16

At the owner's explicit request, `dist/reading-room/` now includes September's
37 restored articles: eight PDF issues (294 records) plus 3,386 CD records,
3,680 total. The original September package and closeout remain preserved.
See the [reading-room guide](READING-ROOM.md) for the two recorded canonical-title
mappings, repeatable export inputs and named release recovery. This local build
was not deployed and does not authorize the next issue's reader integration.

## Where to look when needed

| Need | Reference |
| --- | --- |
| Engine accuracy, cost and limits | [OCR handoff evidence index](../PLAN-OCR.md#metrics-and-accounting) |
| Mapped-Qwen and optional A/B/C commands | [Workflow reference](OCR-WORKFLOW.md) |
| Article/assembly/batch/issue tooling | [PDF commands](PDF-RESTORATION.md#current-data-only-commands) |
| A specific old checkpoint or failure | [PDF issue logs](progress/README.md), [experiment history](history/README.md) |
| CD reader inputs, routes and private preview | [Reading-room guide](READING-ROOM.md), [README](../README.md) |

The [previous successor snapshot](history/SUCCESSOR-NOTES-2026-10-14.md) retains
all detailed earlier restoration notes. The disc constraints below remain useful;
old test counts and inventory sizes are historical observations, not new gates.

## Known decoder defect

Read [the HELPDECO underline bug record](CD3-HELPDECO-UNDERLINE-BUG.md) before
changing CD3 formatting. The pinned decoder mistakes a font character-set byte
for `DoubleUnderline`: Hangul `0x81` becomes RTF `\uldb`, even with the actual
underline flag off. The owner confirms normal, non-underlined rendering in the
Windows viewer. The record contains the font-stream hash, descriptor offsets,
counts, code references and reproduction command.

The implemented mitigation is **display-only** in `tools/cd3_display.py`, shared
by the CD3 HTML exporter and reading-room adapter. The decoder is unpatched,
no upstream issue was filed, and stored RTF/source flags retain its error.
Suppression also hides genuine underline; it does not alter literal text,
source evidence, bold/italic, code spacing or attachment bytes. Correcting the
font decoder and migrating the pinned probe is explicitly deferred.

## Owner priorities and retained exceptions

Paper magazines are authoritative. CD and library TOC data are separate
transcriptions. Preserve readable text, literal code, useful structure, images,
source provenance and visible uncertainty. Keep paper-supported corrections
separate. Do not guess uncertain characters or printed-issue associations.

CD1 has 1,080 texts across 72 body-bearing issues, including 33 with localized
gaps, plus eight unresolved article-boundary candidates. It retains 1,111
unviewable distinct images with original links. The historical 995 strict
packages/19b outcomes remain unchanged; the readable reference adds useful
text from all 85 earlier failures.

CD2 accounts for 1,330 candidates (220 success, 1,110 partial), and CD3 for 968
(792 success, 176 partial). Partial outcomes retain useful bodies with local
exceptions. CD3's anomalous date labels, missing images/CAB and unresolved figure
aliases remain explicit. Neither extraction completeness nor normal Windows
rendering establishes agreement with paper magazines.

The goal is useful reading and paper restoration with a clear stopping point.
Do not restart speculative recovery or cosmetic-formatting campaigns to clear
every exception. Existing viewer observations can diagnose concrete extraction
bugs; routine Windows setup or screenshot collection is not a prerequisite.

## Rebuild and verification

`make export-reading-room` validates the prepared references, builds static
version 2 data in a staging tree and replaces the existing data only after the
aggregate checker passes. CD1/demo version 1 documents and CD1 URLs remain
supported. See the guide for required private inputs; a Git checkout alone
cannot reproduce publisher content. `make demo-reading-room` supports UI work
without those inputs.

`make test-reading-room` runs the focused Python adapter tests, six Vitest
tests, TypeScript checks and a production build. `make check-reading-room`
verifies the prepared inventory, hashes, article memberships, literal text,
listings, attachments, media, search coverage and source manifests. The current
aggregate inventories 44,672 reference data files, about 3.43 GB before its root
manifest, plus optional covers (eight supplied samples bring it to 44,680).
Add covers as `covers/masoYYMM.jpg/png/webp`, then re-export/build; see
[the cover guide](READING-ROOM.md#add-or-replace-cover-images).
Use per-disc checks from the reference guides when changing those exporters;
avoid rerunning the whole historical suite for documentation-only changes.

Browser validation covered representative articles from each disc, linked CD3
figures and supplements, downloads, missing originals, undated navigation,
search, refresh and a 360px dark-mode layout. The underline follow-up checked
all current CD3 article/supplement pages and three rendered reader articles.
See PROGRESS for concrete cases and preserved-file checks.

## Future work, when requested

- Correct HELPDECO's font mapping, validate it against raw records and the viewer,
  version the new decoder/probe, regenerate dependent evidence and remove the
  blanket display workaround. Do not relabel the existing probe as corrected.
- Resolve a specific text, image, boundary or association problem when it helps
  actual paper/OCR comparison. Gary Kildall's interview (`8802030`) remains a
  useful starting example.
- Collect missing scans/covers and verified later TOCs. The library TOC currently
  ends at 1993-12; CD2/CD3 navigation does not manufacture later TOCs.
- Make and verify an independent backup of all disc sources, probes and private
  outputs. Earlier CD1 transfer archives are historical snapshots and do not
  include the completed CD2/CD3/SPA work. No independent backup is recorded.
- The owner reports that the volunteer reading-room deployment works; its
  access and future updates are separate from PDF restoration.

Keep source media and generated publisher content out of Git. Log substantive
work in PROGRESS and commit scoped changes; preserve unrelated owner edits.
