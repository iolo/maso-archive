# Step-by-step PDF restoration plan

Storage update, 2026-10-16: follow the [successive-issue workflow](docs/STORAGE.md#successive-restoration)
for new work. Keep unfinished batches, raw OCR, corrections, recipes and review
evidence under `archive/pdf/YYYY-MM/`; preserve them after issue closeout too.
Use a fresh destination for each revision. Older dated paths below remain valid
through compatibility links and do not change the retention policy.

## Current OCR routing guide

**User decision, 2026-10-14:** retain mapped Tesseract as the default restoration
pipeline. Use Qwen as an opt-in draft or second reading for difficult prose or
code, with explicit layout and coverage review.

Read the short [OCR handoff](PLAN-OCR.md) before a future batch. It consolidates
source review, bounded assistance, evidence preservation, commands, metrics and
accounting limits. It supersedes earlier Qwen-first/adaptive trial assignments.
The [experiment history index](docs/history/README.md) is for targeted lookup;
old checkpoint “next” statements are not a queue to resume.

**Do not rebuild the reading room until the user explicitly requests it.** PDF
restoration delivers JSON/assets. Existing rendering instructions and acceptance
records below are historical and do not authorize a new rebuild.

## February 1985 in progress, 2026-10-22

Batch01 restores 편집자 노트, canonical0009, on printed17/PDF19.
The selected JSON/assets package is
`archive/pdf/1985-02/packages/batch-01-r02/editorial`; all 25 files match its
independent rebuild. Five reviewed regions retain four blocks, 67 physical text
rows and the complete original page. All 394 exact UTF-8 ranges and five image
decodes pass; fresh `make test-pdf` passes 213 tests.

Batch02 completes Q&A, canonical0010, on printed18–21/PDF20–23. Its selected
package `archive/pdf/1985-02/packages/batch-02-r01/qa` matches all 266 files of
the independent rebuild. Nine questions retain 52 assembly ordinals, 12 BASIC
labels, 24 arithmetic cells and five explicit unknown bands. All 2,482 exact
UTF-8 ranges and 68 image decodes pass; unchanged 213-test baseline reused.

Batch03 completes 이 책을 처음 대하는 독자에게, canonical0011, on printed22–26/
PDF24–28. All 215 files at `archive/pdf/1985-02/packages/batch-03-r01/reader-guide`
match the independent rebuild. Fifty text blocks and six originals retain three
BASIC examples, two assembly listings, two dumps and two interactive-entry panels.
All 2,766 exact ranges, 56 image decodes, 50 code rows, 18 assembly ordinals,
11 BASIC labels and four caption links pass. Two unknown bands, four faint heading
candidates, literal command/byte discrepancies and duplicate MSX step③ remain explicit.
One crop repair preceded 50 OCR tasks; no failure/retry. The 213-test baseline is reused.

Batch04 completes 애독자 광장, canonical0012, on printed27–29/PDF29–31.
All 159 files at `archive/pdf/1985-02/packages/batch-04-r01/readers-plaza`
match its independent rebuild. Eight letters, eight signatures and three editorial
replies retain 348 physical text rows, eight numbered requests and eleven printed
references. All 1,966 exact ranges and 40 images pass. Six crop repairs preceded
37 tasks; no OCR failure/retry. Five ellipsis bands and localized source candidates
remain explicit. The unchanged 213-test baseline is reused.

Batch05 completes 베이직 강좌, canonical0026, source headline 세련된 INPUT,
on printed30–32/PDF32–34. All 171 files at
`archive/pdf/1985-02/packages/batch-05-r01/basic-input` match its independent
rebuild. All 3,078 exact ranges and 45 images pass. Two programs and four examples
retain 87 physical code rows/84 BASIC labels; two tables retain 76 nonblank cells,
eight blank slots and three printed range groups. Five captions retain their targets.
RETRUN, the physical1170/290 wrap and 13 unknown bands remain literal. The original
input diagram remains; independent label transcription is pending volunteers.
All 39 OCR tasks completed without failure/retry; the 213-test baseline is reused.

Batch06 completes 애플 tip : 언제나 가능한 진법 변환, canonical0027,
source headline 언제라도 가능한 진법변환, on PDF36–37. Opening folio34 is visible;
final folio is absent and mapped null. Lower independent book advertisement excluded.
All 117 files at `archive/pdf/1985-02/packages/batch-06-r02/apple-conversion` match
its independent rebuild. All 905 exact ranges, 992 evidence pins and 30 images pass.
Seven code/output rows, one temporary BASIC label, five ordered steps, six prose
step references, eleven RETURN occurrences and two word continuations survive.
Seventeen localized candidates retain NED20G/ED20G and literal arithmetic.
All 26 tasks completed without failure/retry; the unchanged 213-test baseline is reused.
A fresh metadata revision corrects one 2A occurrence link; all prior versions remain.

Batch07 completes SPC-1000 tip : BEEP, canonical0028, on printed36–37/PDF38–39.
The opening lower 컴퓨돌이 panel remains separately owned and excluded. All 105 files
at `archive/pdf/1985-02/packages/batch-07-r01/spc-beep` match its independent rebuild.
All 1,987 exact ranges, 2,069 evidence pins and 27 images pass. Two BASIC listings
retain 60 labels/63 code rows, 124 numeric DATA fields plus END and 62 note/duration
pairs. The note table retains 16 data cells/two row headers; six usage examples,
five boxed keys and three caption links remain. Seven unknown bands/marks and
19 source candidates remain explicit. All 23 tasks completed without failure/retry;
two crop repairs preceded OCR. Unchanged 213-test baseline reused.

Batch08 completes MSX-tip : 미니 모니터, canonical0029, on printed38–39/PDF40–41.
The final right relocation advertisement is excluded; left listing panel and folio
remain. All 88 files at `archive/pdf/1985-02/packages/batch-08-r01/msx-monitor` match
its independent rebuild. All 2,316 exact ranges, 2,384 evidence pins and 22 images pass.
The listing retains all 61 rows/labels1000–1600, 32 quoted fields, 35 literal fields
and 17 branch targets. Three command sections, one caption/four listing regions,
four connections and six physical wraps remain. Eight unknown bands/widths and
18 localized candidates remain explicit. All 19 tasks completed without failure/retry;
two crop repairs preceded OCR. Unchanged 213-test baseline reused.

Batch09 completes 모뎀, 그 속 이야기, canonical0031, on printed40–43/PDF42–45.
Parent0030, 마이크로컴퓨터의 새로운 물결, is non-owning; all four child identities
and relationships remain. All 214 files at
`archive/pdf/1985-02/packages/batch-09-r01/modem` match its independent rebuild.
All 1,934 exact ranges, 2,100 evidence pins and 56 images pass. Fifty blocks retain
290 physical rows, two original diagrams/two captions, two pull quotes, five chip
features, two credits, six connections and twelve physical wraps. Twenty-six source
candidates retain Oxcide/역활 and literal claims. Diagram-label transcription remains
pending volunteers. All 50 tasks completed without failure/retry; three crop repairs
preceded OCR. Unchanged 213-test baseline reused.

Batch10 completes 오캄의 칼날, canonical0032, on printed44–49/PDF46–51.
All 286 files at `archive/pdf/1985-02/packages/batch-10-r02/occam` match its
independent rebuild. All 4,778 exact ranges, 5,007 evidence pins and 76 images pass.
Sixty-seven blocks retain 436 physical rows, including 108 code rows in nine groups
and 96 source-line groups. Two listing captions/panels, one illustration, two pull
quotes, four operator-table rows/eight cells, eleven annotation wraps and ten prose
connections remain. Forty-two localized candidates retain Willam, SER Q and literal
identifier differences. One hyphen-band count and encoded whitespace remain unknown.
All 67 tasks completed without failure/retry; four crop repairs preceded OCR. A fresh
metadata revision adds logical row grouping without changing text. All versions remain.
Unchanged 213-test baseline reused.

Batch11 completes 80286, canonical0033, on printed50–55/PDF52–57.
All 243 files at `archive/pdf/1985-02/packages/batch-11-r01/i80286` match its
independent rebuild. All 3,193 exact ranges, 3,379 evidence pins and 64 images pass.
Fifty-seven blocks retain 463 physical rows, six complete pages, one uncaptioned
processor diagram, three pull quotes, three credits and six section headings.
Eleven page/column joins, five regional continuations, eighteen physical wraps,
112 technical-token occurrences and 131 numeric fields retain exact source links.
Forty-eight candidates preserve nultitasking, Zenix, Bus Instruction Unit and literal
source claims. One ellipsis-band count remains unknown; diagram labels pending volunteers.
All 57 tasks completed without failure/retry; four crop repairs preceded OCR.
Unchanged 213-test baseline reused. All prior work and source corrections remain.

Batch12 restores the opening six pages of 포쓰의 기초 이해, canonical0034,
printed56–61/PDF58–63. The full article is eight pages, printed56–63/PDF58–65;
its closing two pages and assembly remain pending. All 395 files at
`archive/pdf/1985-02/packages/batch-12-r01/forth-a` match the independent rebuild.
All 2,852 exact ranges, 3,206 evidence pins and 114 images pass. Ninety-one blocks
retain 393 physical rows, fifteen diagrams with captions, two tables with captions,
eighteen data cells/four headers/nine ordinals, two pull quotes and one source credit.
Eight continuations, twenty physical wraps and sixteen internal references retain
exact source links. Twenty-nine candidates preserve Intrepretive, 어드레드 and 아키스;
one caption dot-band count remains unknown. Diagram labels are pending volunteers.
All 114 original/thirteen revised crops were inspected before 91 tasks; all raws
read before one source pass. Zero OCR failure/retry; unchanged 213-test baseline.

Batch13 restores Forth's closing printed62–63/PDF64–65, excluding the independent
upper-right 컴퓨돌이 해답 panel. All 166 files at
`archive/pdf/1985-02/packages/batch-13-r01/forth-b` match the independent rebuild.
All 787 current exact ranges, the separate incoming prior-segment range, 922 evidence
pins and 44 images pass. Thirty-eight blocks retain 114 physical rows, two diagrams,
three captions, twelve table cells/six arrows, two compiler roles/four term lines,
three NEXT points and two pull quotes. Nineteen source candidates retain literal
wording and glyph approximations. All 44 original/two revised crops were inspected
before 38 tasks; all raws read before one source pass. Zero OCR failure/retry;
unchanged 213-test baseline reused. Original attempts and both natives remain.

Forth is now complete at `archive/pdf/1985-02/packages/forth-complete-r01`, covering
printed56–63/PDF58–65. All 569 files match the independent rebuild; all 561 native
files and both full correction records remain exact. Fifty segment/category slices
and 3,639 projected UTF-8 ranges reverse to their original occurrences. The package
retains 158 regions, 129 blocks, 507 physical rows, seventeen diagrams/twenty captions,
three tables/thirty cells/four headers, four pull quotes and the verified 네/스팅 join.
Six stale stage notes are resolved only in active status; original notes remain.
Forty-eight source candidates and one unknown caption dot count remain explicit.
No new mapping, render, OCR or source correction. Use the pinned private
`archive/pdf/1985-02/restoration/forth-assembly/forth_literal.py` checker/context;
see its `reproduction.json`. The unchanged 213-test baseline is reused, and three
negative adapter probes reject range drift, a changed incoming link and deferred coverage.

Batch14 restores the opening printed64–69/PDF66–71 of 산수 경주, canonical0036.
Its full extent is printed64–76/PDF66–78; seven following pages and assembly remain
pending. Parent0035 교육용 프로그램의 진수 is non-owning with four unchanged children.
All 339 files at `archive/pdf/1985-02/packages/batch-14-r01/math-race-a` match the
independent rebuild. All 6,572 exact ranges, 6,863 evidence pins and 96 images pass.
The 479 physical text rows include 114 code rows and 43 actual BASIC labels; three
tables retain 114 rows/228 cells without invented headers. Four screens, an illustration,
nine caption links, five prose connections and two listing joins remain source-linked.
Thirty-nine candidates retain AA operator ambiguity, +. code point, T/O glyph,
-16368 and historical wording. Outgoing line490 preserves 25 before next page's 0.
All 96 original/four revised crops were inspected before 78 tasks; all raws read before
one source pass. Zero OCR failure/retry; unchanged 213-test baseline reused. The original
three-child count is preserved as a metadata erratum; OCR-bound maps remain unchanged.

Batch15 restores the middle printed70–75/PDF72–77 of 산수 경주 at
`archive/pdf/1985-02/packages/batch-15-r01/math-race-b`. All 106 files match the
independent rebuild; 15,643 current UTF-8 ranges, two external native ranges,
15,759 current evidence pins and 40 images pass. Its 619 physical text rows include
593 BASIC rows and 22 dump rows. The incoming490 fragment, 180 new labels500–2290,
eleven panel boundaries/six BASIC joins, 145 quoted fields and 176 dump bytes remain
source-linked. Thirty localized candidates and 461 unknown encoded-whitespace bands
remain explicit. All 40 original/one revised crops preceded 19 tasks; all raws were
read before one source pass. No OCR failure/retry; unchanged 213-test baseline reused.

Batch16 restores final printed76/PDF78 at
`archive/pdf/1985-02/packages/batch-16-r01/math-race-c`. All 29 files match the
independent rebuild; 7,174 current UTF-8 ranges, two external native ranges,
7,199 current evidence pins and eight images pass. Four blocks retain the section
label and 143 dump rows/1,141 literal bytes. The incoming60A8/60B0 link, two column
boundaries, prior caption and five-byte final6520 row remain indexed. Twenty-two
localized glyph candidates remain explicit. All eight original/one revised crops
preceded four tasks; all raws were read before one source pass. No OCR failure/retry;
unchanged 213-test baseline reused. PDF79 is an independent contest advertisement.

산수 경주 is now complete at `archive/pdf/1985-02/packages/math-race-complete-r01`,
covering printed64–76/PDF66–78. All 483 files match the independent rebuild; all
474 native files and full correction metadata remain exact. Ninety-six category
slices and thirteen projected objects reverse to their native records across
29,389 original range occurrences. All 32,710 active ranges, 29,829 native evidence
pins and 144 image decodes pass. Complete indexes retain 223 BASIC labels/703 BASIC
rows, 165 dump rows/1,317 literal bytes, three tables/228 cells and ten captions.
Both cross-segment continuations and two external caption links are verified without
rewriting physical text. Ninety-one source candidates and 461 unknown whitespace
bands remain explicit. Six stale stage notes are resolved only in active status.
Use the pinned private `restoration/math-race-assembly/math_race_literal.py` checker
or its `installed()` context; see that directory's `reproduction.json`. Five negative
probes reject range, continuation, caption, cell and final-page coverage drift.
No new mapping, rendering, OCR or source correction; unchanged 213-test baseline reused.

Batch17 restores 디지털 논리 회로 opening78–83/PDF80–85 at
`archive/pdf/1985-02/packages/batch-17-r01/digital-logic-a`. All 311 files match its
independent rebuild; 5,474 exact ranges, 5,954 evidence pins and 99 images pass.
Five numbered tables/two additional truth tables retain 442 indexed nonblank fields;
eight gate groups retain 80 truth-data cells. Eleven arithmetic panels, six caption
links and seven original Karnaugh diagrams remain. Thirty-seven candidates preserve
source 디지탈, printed sentence/formula errors and literal truth values. Four encoded
ellipsis counts remain unknown; independent diagram labels pending volunteers.
All 99 original/21 revised crops preceded 68 tasks; all raws read before one source
pass. No OCR failure/retry; unchanged 213-test baseline reused. Original maps retain
the superseded source-title narrative, with an explicit metadata erratum.

Batch18 completes the ending84–85/
PDF86–87 at packages/batch-18-r01/digital-logic-b. All 128 files match its independent
rebuild; 1,224 current ranges, three external ranges, 1,344 evidence pins and 42 images
pass. Two truth tables retain 56 data cells; six design steps and four arithmetic
examples remain. Fourteen text/two image candidates preserve literal formula and
label discrepancies. All 42 original/one revised crops preceded 26 kor+eng tasks;
all raws read before one source pass. No OCR failure/retry; unchanged test baseline.
디지털 논리 회로 is now complete at packages/digital-logic-complete-r01, printed78–85/
PDF80–87. All 447 files match the independent rebuild; all 439 native files/full metadata
remain exact. Fifty-eight category slices/eight objects reverse to native records:
6,698 original range occurrences, 6,703 active ranges, 7,305 native evidence pins and
141 images pass. Nine table groups retain 507 indexed fields/89 blank slots; twelve
arithmetic panels, six design steps, six captions and both cross-segment associations
are verified. Fifty-one text/two image candidates and four unknown ellipsis counts
remain; independent diagram labels pending volunteers. Four original stage notes and
two ledger deferrals are preserved with explicit resolution records. Five negative
probes reject altered ranges/links/coverage. Use the pinned private digital-logic-assembly/
digital_logic_literal.py checker/context and reproduction.json; generic check alone
does not recognize this format. No new OCR/source correction; unchanged test baseline.

Batch19 restores PASCAL/MT+ opening86–91/PDF88–93 at
`archive/pdf/1985-02/packages/batch-19-r02/pascal-a`. All 512 files match its
independent rebuild; 7,374 exact ranges, 7,786 evidence pins and 134 images pass.
Its 123 blocks retain 444 transcript rows, including 159 code/output/example rows;
four vertical-dot extents have unknown original row counts. Lists1–5, three printed
outputs, five captions, CASE's page continuation and eight prose associations remain.
Fifty candidates preserve literal source errors; ten symbol/ellipsis extents and
486 encoded-space bands remain unknown. All 132 original/28 revised crops preceded
123 tasks (52 eng/71 kor+eng); all raws read before one source pass. No failure/retry.
A fresh metadata revision adds logical row coverage; text and both prior outputs
remain exact. Unchanged 213-test baseline reused; all 17,295 prior files verified.

Batch20 restores PASCAL/MT+ middle92–97/PDF94–99 at
`archive/pdf/1985-02/packages/batch-20-r01/pascal-b`. All 346 files match its
independent rebuild; 8,279 current UTF-8 ranges, one incoming native range,
8,615 evidence pins and 100 images pass. The 79 blocks retain 361 text rows,
including 213 code/output rows in 209 logical source lines. Lists6–9, five output
groups, eight captions, 33 directory entries/99 fields/three blank slots and 29
file/option items remain indexed. Linker/debugger continuations, the duplicated
Hanoi header and list9's separate main/module remain literal. Forty-three candidates,
one unknown ellipsis count and 686 unknown encoded-space bands remain explicit;
independent diagram labels are pending volunteers. All 100 crops preceded 79 tasks
(32 eng/47 kor+eng); all raws read before one source pass. No failure/retry/crop repair.
All 20,369 prior files verified; unchanged 213-test baseline reused.

Batch21 restores ending98–103/PDF100–105 at
`archive/pdf/1985-02/packages/batch-21-r01/pascal-c`. All 210 files match its
independent rebuild; 8,507 current ranges, two external native ranges, 8,813 pins
and 60 images pass. Its 270 text rows include 209 code/output rows in 207 logical
lines. Lists10–12 retain three captions and five listing connections. Assembly
indexes retain 63 rows/158 fields/94 blank fields/11 labels/four storage rows;
eleven constants and six array bounds remain literal. Thirty-three candidates
and 863 unknown encoded-space bands retain original scans. All 60 original/two
revised crops preceded 47 tasks (28 eng/19 kor+eng); all raws read before one pass.
No OCR failure/retry. Initial constant-index assertion failure is preserved;
metadata correction changed no text. All 21,734 prior files verified; unchanged
213-test baseline reused. Final independent contest excluded from article assets.

PASCAL/MT+ is complete at `archive/pdf/1985-02/packages/pascal-complete-r01`,
printed86–103/PDF88–105. All 1,077 files match its independent rebuild; all 1,068
native files/full metadata remain exact. All 120 category slices/sixteen objects
reverse to native records, retaining 24,160 original range occurrences. All 26,620
active ranges, 25,223 native evidence pins and 294 images pass. Complete indexes
retain 581 code/output rows in 575 logical groups, 87 listing groups, sixteen
captions and nine output groups. Lists1–12, directory/assembly fields, both native
boundary associations and the external3.3 reference pass. Four vertical-dot extents
retain unknown source-row counts. All126source candidates, eleven unknown symbol/
ellipsis extents and2035unknown space bands remain; diagram labels pending volunteers.
Six stale stage notes are resolved only in active status; full originals remain.
Seven negative probes reject range/link/field/coverage drift. Checker revisions and
their failed attempts are preserved; no source text or package revision was needed.
Use the pinned private `restoration/pascal-assembly/pascal_literal.py` checker/context
and reproduction.json. No new OCR/source correction; unchanged213-test baseline reused.
The independent lower-right contest on103/PDF105 remains excluded.

Batch22 completes CP/M 입문 at `archive/pdf/1985-02/packages/batch-22-r01/cpm`,
printed104–108/PDF106–110. Its actual extent is five pages; following PDF111 is an
independent advertisement, and PDF112 opens the software review. All 312 files match
the independent rebuild; 5,742 exact ranges, 6,004 evidence pins and 81 images pass.
The 361 non-table text rows include 90 code/output rows. Sixty-three assembly rows
retain 185 fields/four blanks, including two address-only rows. Eight dump rows retain
52 bytes; the two-page DPB table retains nine data rows/four headers/40 cells and all
59 cell lines. Five BASIC labels/two quoted fields, 31 numeric output fragments and
all source connections remain. Forty-six candidates, eight unknown dot bands and
265 unknown encoded-space bands remain. All 81 crops were reviewed before 74 tasks;
all raws read before one source pass. No OCR failures/retries/crop repairs. Initial
map/preflight assertion failures and a metadata-only quote-index revision are retained.
All 24,775 prior files verified; unchanged 213-test baseline reused.

Batch23 completes 소프트웨어 리뷰, source 삼보 컴퓨터의 TG-WRITER, at
`archive/pdf/1985-02/packages/batch-23-r01/tg-writer`, printed110–112/PDF112–114.
All 176 files match its independent rebuild; 1,661 exact UTF-8 ranges, 1,822 evidence
pins and 48 images pass. Forty blocks retain 169 non-table text rows, four feature
items, six summary fields, two formatting samples and two tables with 48 nonblank
cells/six blank cells. Four connections, eighteen physical wraps and fifteen heading
associations remain. Thirty-one candidates, two unknown ellipsis counts and one
margin-space band retain original scans; photograph labels pending volunteers.
All 48 original/one revised crops preceded 40 kor+eng tasks; all raws read before
one source pass. No OCR failures/retries; one paragraph-edge trim before recognition.
Literal command names, product claims, repeated wording, sample punctuation and
printed totals846/3,421 remain. All 26,010 prior files and 30 implementation pins
pass; unchanged 213-test baseline reused. Following PDF115 is a separate feature opener.

Batch24 completes the feature introduction, canonical0001, on printed113/PDF115 at
`archive/pdf/1985-02/packages/batch-24-r01/feature-intro`: all 38 files match the rebuild;
123 exact ranges, 153 evidence pins and nine images pass. Seven blocks retain sixteen
physical rows and four keyboard labels. Two photo-obscured spans and five source
candidates remain explicit. The opener owns its introduction; both child identities remain.
Speed text, canonical0002, is partial at `packages/batch-24-r01/speed-a`, covering
printed114–116,122–123/PDF116–118,124–125. All 325 files, 8,514 exact ranges, 8,940
pins and 85 images pass. Its 417 rows include 146 code rows in 145 logical groups;
136 assembly ordinals retain 658 fields/164 blanks/184 object bytes, six comments and
33 directives. Seven BASIC labels, two captions, five command guides, thirteen annotation
groups and five connections remain. Thirty candidates, one unknown leader band,
26 ornament approximations and 561 unknown space bands remain. Incomplete PEEK and
assembly94 operands,800E/1415 and1200/1600/2700 stay literal. Full extent is ten pages:
three prose pages plus122–128 listings, final128 upper only; intervening music excluded.
All 94 original/eight revised crops preceded84tasks; all raws read before one source pass.
No OCR failures/retries. All 26,714 prior files and30implementation pins pass; unchanged
213-test baseline reused. Batch25 below completes the remaining listing pages.

The 56-entry ledger records nineteen readable/sample-reviewed articles, no partial
articles, two non-owning headings and 35 unresolved entries.
Batch25 restores the remaining speed-text listings at
`archive/pdf/1985-02/packages/batch-25-r01/speed-b`, printed124–128/PDF126–130,
with final128 upper only. All 158 files match the independent rebuild; 15,805 current
UTF-8 ranges, five external native ranges, 16,277 evidence pins and 41 images pass.
The 410 physical text rows include355 code rows in353 logical groups. Assembly
ordinals137–432 retain1,459 fields/323 blanks/570 object bytes/eight storage directives;
the unnumbered byte row after425 remains separate. List2 retains57 BASIC labels and
its physical line50 string wrap. Eighteen annotation groups andfive native associations
retain caption122, page128, ordinal136→137 andincoming annotations/prose.
Twenty-six candidates,36 ornament approximations and1,279 unknown space bands remain.
Printed349–350/302–349, DF, BLT, WRITE,APPEND andbareNEXT remain literal.
All41 original/two revised crops preceded36 tasks(18eng/18kor+eng); allraws read before
one source pass. No OCR failures/retries. A verifier spacing assertion was corrected
in a fresh revision; both attempts remain, source text/packages unchanged.
All28,160 prior files and30 implementation pins pass; unchanged213-test baseline reused.
Batch25 restored all ten body pages across two natives; the complete assembly follows below.

스피드 텍스트 is complete at `packages/speed-text-complete-r02`. All 492 files match
its independent rebuild; all 483 native files and full metadata remain exact. The 78
category slices and ten object projections retain 24,319 original range occurrences;
26,904 active ranges, 25,217 native evidence pins and 126 images pass. Five external
associations resolve to exact complete-article ranges while their native records remain.
Complete indexes retain 827 text rows, 501 code rows in 498 logical groups, 432 assembly
ordinals, 754 object bytes, one unnumbered byte continuation, 64 BASIC labels, three
listing groups, three captions and 31 annotations. Final page 128 remains upper-only.
Fifty-six candidates, one leader band, 62 ornament approximations and 1,840 unknown
space bands remain. Four stage notes resolved only in active status; originals retained.
No new OCR or source correction. Eight negative probes reject range/link/ordinal/coverage
changes; unchanged 213-test baseline reused. Use the pinned private speed_text_literal
checker/context and reproduction.json. No speed-text body pages or assembly remain pending.

Batch 26 restores 배경 음악의 구현 opening at
`archive/pdf/1985-02/packages/batch-26-r01/music-a`: prose 117–121/PDF119–123 and
lower 128/PDF130. Its verified full extent is eleven noncontiguous pages through
printed 133/PDF135, ending 480 GOTO 400. Upper 128 remains separately owned speed text;
the final page's independent contest and advertisement are excluded.
All 383 files match an independent rebuild; 5,054 exact UTF-8 ranges, 5,510 evidence
pins and 101 images pass. The 348 text rows retain 73 code rows in 72 logical groups,
51 assembly ordinals 0000–0050, 200 fields/157 blanks/38 object bytes, 64 dump bytes
and nine patch-assembly rows. Four diagrams, three pull quotes, five captions, eight
installation steps, eight usage groups, twelve routine annotations and nine joins remain.
Thirty-one source candidates, three unknown bands and 286 unknown spacing bands remain;
printed command inconsistencies, repeated prose and historical ranges stay literal.
All 101 original/11 revised crops preceded 91 tasks (8 eng/83 kor+eng); all raws were read
before one source pass. No OCR failures/retries. All 29,813 prior files and 30
implementation pins pass; unchanged 213-test baseline reused. This is a partial article.

Batch 27 restores the ending music listings at
`archive/pdf/1985-02/packages/batch-27-r02/music-b`, printed129–133/PDF131–135.
All 103 files match an independent rebuild; 20,947 current UTF-8 ranges, 15 external
native ranges, 21,941 evidence pins and 28 images pass. The 450 text rows retain
446 code rows in 437 logical groups, 389 assembly ordinals0051–0439, 1,907 fields,
865 blanks, 673 object bytes and seven unnumbered byte continuations. Ordinal0390 is
present; the earlier possible-gap note remains preserved. List2 retains 48 labels,
two physical wraps, 17 PLAY strings with 251 characters, one caption and two credits.
Fifteen links retain the opening row0050, list1 caption, twelve routine annotations
and the list2 prose reference. The final page owns only the left and upper-right
listing panels; the independent contest and advertisement remain excluded.
Thirty-one source candidates, two unknown asterisk bands and 1,805 unknown spacing
bands remain. All 28 original/eight revised crops preceded 22 tasks (18 eng/4 kor+eng);
all raws were read before one source pass. No OCR failures or retries. A focused
source check corrected one manual byte-order error at0413 to220C16; both versions remain.
A code-group metadata revision excludes the caption; text and OCR are unchanged,
and the failed first export, rebuild and verifier remain preserved. All 31,330 prior
files and 30 implementation pins pass; the unchanged 213-test baseline is reused.
Batch27 restored all eleven body pages across two native packages; the complete assembly follows below.

배경 음악의 구현 is complete at
`archive/pdf/1985-02/packages/background-music-complete-r01`, covering eleven
noncontiguous pages117–121,128–133/PDF119–123,130–135. All 495 files match the
independent rebuild; all 486 native files and full correction metadata remain exact.
Eighty category slices and twelve object projections reverse to their native records
across 26,001 original UTF-8 range occurrences. All 29,010 active ranges, 27,451 native
evidence pins and 129 images pass. Complete indexes retain 798 text rows, 519 code rows
in 509 logical groups, 440 assembly ordinals0000–0439, 711 object bytes, seven unnumbered
byte continuations, 64 patch-dump bytes, nine patch-assembly rows, 48 BASIC labels,
two physical wraps and 17 PLAY strings/251 characters. Six captions, twelve routine
annotations and all fifteen cross-segment associations retain exact source occurrences.
Upper128 speed text, final133 contest and advertisement remain excluded. Sixty-two
source candidates, five unknown bands and 2,091 unknown spacing bands remain explicit.
Four stage notes are resolved only in active status; all original notes remain.
No new mapping, render, OCR or source correction. Nine negative probes reject altered
ranges, links, ordinals and page coverage. All 32,016 prior files and 30 implementation
pins pass; the unchanged 213-test baseline is reused. Use the pinned private
`restoration/background-music-assembly/background_music_literal.py` checker/context
and `reproduction.json`; the generic checker alone does not recognize this format.
After music assembly: 20 readable, no partial articles, two non-owning headings and 34 unresolved.

Batch28 completes the input-tools introduction, canonical0004, on printed134/PDF136
at `archive/pdf/1985-02/packages/batch-28-r01/input-intro`, and 페이퍼 홀더,
canonical0005, on printed135/PDF137 at
`archive/pdf/1985-02/packages/batch-28-r01/paper-holder`. All 22 introduction files
and 54 paper-holder files match their independent rebuilds. All 286 exact UTF-8
ranges, 345 evidence pins and 18 images pass. Fourteen blocks retain 40 physical rows,
the original photograph and diagram, four faint diagram labels, one caption and its
prose reference, the 입/력된 column join, ten physical wraps and three historical claims.
The introduction owns its prose/photo; all three child identities and relationships remain.
Nine localized glyph candidates and two Roman-II Unicode approximations remain explicit.
The original price5～6천원, availability statement and printed wording remain literal.
All 18 crops were inspected before 14 kor+eng tasks; all drafts were read before one
source correction pass. No OCR failure, retry or crop repair. All 33,029 prior files
and 30 implementation pins pass; the unchanged 213-test baseline is reused.
Current totals: 22 readable, no partial articles, two non-owning headings and 32 unresolved.

Batch29 restores ALE’s complete prose segment, canonical0006, on printed136–139/
PDF138–141 at `archive/pdf/1985-02/packages/batch-29-r01/ale-a`. All 223 files match
its independent rebuild; all 2,369 exact UTF-8 ranges, 2,545 evidence pins and 58 images
pass. Fifty-two blocks retain 272 physical rows, six examples/seven code rows, one
BASIC label, two tables/19 rows/38 cells, two captions and eight prose continuations.
Twelve listing annotations, five routine ranges, seven key notations, seven POKE
commands, two pull quotes and 56 physical wraps retain their source occurrences.
Twenty-nine glyph/wording candidates, seventeen Unicode approximations and twelve
unknown spacing bands remain explicit. Printed1006/L$3EF,37478($9266),PSII,FREFAC,
overlapping routine ranges, table arrows and split RETURN remain literal.
The full extent is eight noncontiguous pages: prose136–139 plus listing142–145.
Shared139/PDF141 owns only upper ALE prose; lower MLE and interveningPDF142–143
are excluded. All 58 original/five revised crops preceded52tasks (6eng/46kor+eng);
all drafts were read before one source pass. No OCR failure/retry. All 33,342 prior
files and 30 implementation pins pass; the unchanged 213-test baseline is reused.
Current totals: 22 readable, one partial article, two non-owning headings and 31 unresolved.

Batch30 restores the complete ALE listing on printed142–145/PDF144–147 at
`archive/pdf/1985-02/packages/batch-30-r01/ale-b`. All 53 files match its independent
rebuild; 31,617 current UTF-8 ranges, thirteen external native ranges, 32,586 evidence
pins and fourteen images pass. All 579 assembly ordinals retain 3,161 independent
fields, 892 blank fields, 1,007 printed object bytes, 375 comments, 136 labels and
49 ORG/EQU directives. Two unnumbered headers retain the source/object filenames;
the object-header dash count stays unknown. Seven column/page boundaries, one caption,
twelve prose ordinal references and one prose listing reference retain exact links.
The printed494 range remains open. Thirty-eight localized candidates, two isolated
ink marks and 2,971 unknown spacing bands retain originals. FFER stays in its printed
comment position without an inserted semicolon. All source spellings and numerical
claims remain independent, including prose1006 and the listing's1,007 object bytes.
All 22 original/nine revised crops were reviewed before ten tasks (8eng/2kor+eng);
all drafts were read before one source pass. No OCR failure/retry. Original half-column
crops and subsequent whole-column/margin repairs remain. A null-ledger-entry verifier
failure and its corrected script remain; no source/package changes were required.
All 34,248 prior files and 30 implementation pins pass; unchanged213-test baseline reused.
All eight ALE body pages now exist in two immutable natives; article assembly is pending.
Current totals: 22 readable, one partial article, two non-owning headings and 31 unresolved.

ALE is complete at `archive/pdf/1985-02/packages/ale-complete-r01`, covering eight
noncontiguous pages136–139,142–145/PDF138–141,144–147. All 285 files match the
independent rebuild; all 276 native files and full correction metadata remain exact.
Ninety-eight category slices and ten object projections reverse to native records
across 33,986 original UTF-8 range occurrences. All 37,850 active ranges, 35,131 native
evidence pins and 72 images pass. Complete indexes retain 855 text rows, 588 code rows
in 587 logical groups, 579 assembly ordinals, 3,161 fields, 892 blanks, 1,007 object bytes,
375 comments, 136 labels and 49 directives. Two listing headers, six examples, one
BASIC label, two tables/38 cells, three captions, twelve ordinal annotations, five
routine ranges, seven keys/seven POKE commands, two pull quotes and eight prose joins
remain. All thirteen cross-segment links resolve; printed494 remains open-ended.
Shared139/PDF141 owns only upper ALE prose; lower MLE and interveningPDF142–143
remain excluded. Sixty-seven candidates, one unknown dash band, two isolated ink marks,
eighteen Unicode approximations and 2,983 unknown spacing bands retain original scans.
Four stage notes resolve only in active status; original notes and all source claims,
including prose1006 versus listing1,007 bytes and unexplained FFER, remain untouched.
No new mapping, rendering, OCR or source correction. Nine negative probes reject altered
ranges, references, ordinals and ownership. All 34,529 prior files and 30 implementation
pins pass; unchanged213-test baseline reused. Use the pinned private
`restoration/ale-assembly/ale_literal.py` checker/context and `reproduction.json`;
the generic checker alone does not recognize this format.
Current totals: 23 readable, no partial articles, two non-owning headings and 31 unresolved.

Batch31 restores all MLE prose on printed139–141/PDF141–143 at
`archive/pdf/1985-02/packages/batch-31-r01/mle-a`. All 225 files match the independent
rebuild; 2,023 exact UTF-8 ranges, 2,228 evidence pins and 60 images pass. Fifty-two
blocks retain 221 serialized text rows, including ten code/menu rows in nine logical
groups. Five menu options, two tables/18 cells, eleven memory-diagram labels, four
examples, 39 key notations, four prose joins and 55 physical wraps retain source links.
Three listing references and three BASIC-label claims remain explicitly deferred.
The diagram retains its original geometry; label serialization order is editorial.
Shared139 owns lower MLE body and its separate section badge; upper ALE is excluded.

The full sixteen-page extent is verified: prosePDF141–143, then listingsPDF148–160.
List1 starts at the first visible ordinal4; no rows1–3 are invented. It ends at
49DB:60 1149 RTS on159, where list2 starts at BASIC100. List2 ends on160 at label460,
final physical row : GOTO 180. The separate contest and advertisements on160 are
excluded;161 is an independent advertisement and162 starts 정보교류/나라안 소식.
Thirteen listing pages and complete immutable article assembly remain pending.

Printed 게제, 압력, 30행, menu DISC versus heading DISK, memory addresses and command
fields remain literal. Twenty-three candidates, five unknown menu dot leaders, 24 Unicode
approximations and 37 unknown spacing bands retain originals. All 60 original/two revised
crops were reviewed before52 tasks (5eng/47kor+eng); all drafts were read before one
source pass. Two border trims preceded OCR; no failure/retry. All 35,122 prior files
and30 implementation pins pass; unchanged213-test baseline reused. Three mapped pages,
17 outside lookups and one canonical task respect the operating limits.
Current totals: 23 readable, one partial article, two non-owning headings and 30 unresolved.

Batch32 restores the first six MLE listing pages146–151/PDF148–153 at
`archive/pdf/1985-02/packages/batch-32-r01/mle-b`. All 79 files match the independent
rebuild; 32,867 current UTF-8 ranges, one external native range, 34,637 evidence pins
and22 images pass. The 543 printed ordinals4–546 retain 647 field-bearing physical rows,
2,837 independent fields, 1,692 blanks, 1,226 object bytes, 55 comment fragments,
129 labels and92 directives. No leading rows1–3 are invented. One object-file header,
89 unnumbered byte rows and15 text continuations form648 code rows/544 logical groups.
Thirteen quoted operands and17 DFB operands retain physical fragments and unknown
encoded spacing. Eleven column/page joins include ordinal498 acrossPDF152–153 and
ordinal510 acrossPDF153 columns. The caption and exact native prose reference are linked.

Printed NENUE/MENUE, BLT/BGE, PTADDR/PRTADR, CONTRO/L E, DFB $4/6 and $4/5 wraps,
quoted strings and independent object fields remain literal. Forty-three candidates,
five unknown dash bands, one isolated ink mark, three RomanII approximations and
2,519 unknown spacing bands retain originals. All22 crops were reviewed before16 tasks
(12eng/4kor+eng); all drafts were read before one source pass. No crop repair, OCR
failure or retry. All36,053 prior files and30 implementation pins pass; unchanged
213-test baseline reused. Six mapped pages, two outside lookups and one canonical task
respect the limits. Nine of sixteen MLE source pages now exist in two immutable natives.
Current totals: 23 readable, one partial article, two non-owning headings and 30 unresolved.

Batch33 restores MLE listing152–157/PDF154–159 at
`archive/pdf/1985-02/packages/batch-33-r01/mle-c`. All83 files match the independent
rebuild; 33,873 current UTF-8 ranges, four external native ranges, 35,254 evidence pins
and23 images pass. All603 assembly ordinals547–1149 retain2,916 independent fields,
1,305 blanks,1,269 object bytes,66 comments and81 labels. Eleven column/page joins
and incoming546/547 remain linked. Final49DB:60 1149 RTS ends list1 without an addedEND.

Lower-right159 begins separately captioned list2 MLE.START, BASIC100–300 in40 physical
rows/21 labels/19 wraps. Fourteen quoted strings,87 numeric fragments andthree branch
occurrences remain indexed. Numeric10:,6371),6373),6) and1798 fragments are continuations,
not new BASIC labels. The caption, two exact prose references and prior list1 caption
retain their original occurrences. PrintedHIMEM16368 versusCALL16384,opaqueD823G patch
string,L0/LO candidate,A$/L$ display strings and independent assembly fields stay literal.
Fifty-one localized candidates,one overprinted row1133,five Unicode approximations and
2,793 unknown spacing bands retain originals; no syntax,byte,address or arithmetic repair.

All23 crops were reviewed before17 tasks (13eng/4kor+eng); all drafts were read before
one source pass. No crop repair, OCR failure or retry. All36,427 prior files and30
implementation pins pass; unchanged213-test baseline reused. Six mapped pages, two
outside lookups and one canonical task respect the limits. Fifteen of sixteen MLE
source pages now exist in three immutable natives. Prior prose/listing natives unchanged.
Current totals: 23 readable, one partial article, two non-owning headings and 30 unresolved.

Batch34 restores final MLE listing158/PDF160 at
`archive/pdf/1985-02/packages/batch-34-r01/mle-d`. All24 files match the independent
rebuild; 1,378 current UTF-8 ranges, two external native ranges, 1,399 evidence pins
and six images pass. Sixteen BASIC labels310–460 retain33 physical rows/17 wraps,
eight quoted strings,64 numeric fragments andthree GOTO targets. Numeric12,3617),
16375),53,114 and115 fragments remain continuations, not new labels. The430/440
column join, incoming300/310 and exact prior list2 caption retain source occurrences.
Final460 : GOTO 180 establishes the body ending; no END is invented.

The original section badge andtwo framed listing panels remain separate; independent
contest and lower book advertisements are excluded. Following161 is an independent
advertisement. SourceL0/LO,A$/L$ display strings,BLOADED spelling andnumeric/string
wraps stay literal. Eleven source candidates,one RomanII approximation and162 unknown
spacing bands retain originals. Allsix crops were individually reviewed beforethree
tasks (2eng/1kor+eng); all drafts read before one source pass. No crop repair, OCR
failure or retry. All36,817 prior files and30 implementation pins pass; unchanged
213-test baseline reused. One mapped page,two outside lookups andone canonical task
respect the limits. All sixteen MLE pages now exist in four immutable natives;
complete article assembly remains pending, and earlier natives are unchanged.
Current totals: 23 readable, one partial article, two non-owning headings and 30 unresolved.

MLE is now complete at `archive/pdf/1985-02/packages/mle-complete-r02`.
All420 files match the independent rebuild; all411 files from four immutable natives
and their full metadata remain exact. The sixteen noncontiguous source pages are
prose139–141/PDF141–143 and listings146–158/PDF148–160. No body pages or article
assembly remain pending. Shared141 upperALE and160 contest/ads remain excluded;
intervening144–147 belongs to ALE.

All236 native category slices,21 object projections and70,141 projected UTF-8 ranges
reverse to original records;75,654 active ranges and111 images pass. Seven external
native associations resolve into complete article coordinates while their original
wrappers remain unchanged. Twenty-five listing connections preserve498/510 byte
continuations,546/547 and BASIC300/310 boundaries. Seven complete listing groups
retain1,334 physical code rows/1,193 logical lines within1,554 total text rows.

List1 retains1,146 ordinals4–1149,1,250 field-bearing physical rows,5,753 independent
fields/2,997 blanks,2,495 object bytes,89 byte continuations,15 text continuations,
13 quoted operands and17 DFB operands. No leading1–3 are invented; final49DB:60
1149 RTS stays literal. List2 retains37 BASIC labels100–460 in73 rows/36 wraps,
22 quoted strings andfinal460 : GOTO 180,without an addedEND. Three prose listing
references target complete captions. Printed210/410 claims link to exact BASIC rows;
printed30행 has no matching label and remains explicitly unmatched,never repaired to130.

The two tables/18 cells,11 diagram labels,5 menu options,39 key notations,four prose
joins andtwo pullquotes remain. 128 localized candidates,ten unknown decorative bands,
two ink marks,33 Unicode approximations and5,511 unknown spacing bands retain originals.
All source wording,opaque strings,byte/address discrepancies and errors remain literal.
Use the pinned private `mle_literal.check` / `mle_literal.installed` adapter and its
reproduction.json. All30 implementation pins remain unchanged;213-test baseline reused.
No new mapping,rendering,OCR orsource correction. Eight exact stale stage notes are
resolved only in active assembly notes; every original note remains in native metadata.
The failed first assembly expectation and first key-wrap verifier are preserved;
selectedr02 export/rebuild and revised verifier pass,including nine negative probes.
All36,940 prior files remain unchanged.
Current totals: 24 readable, no partial articles, two non-owning headings and30 unresolved.

Batch35 completes 나라안 소식0014 on printed160–165/PDF162–167 at
`archive/pdf/1985-02/packages/batch-35-r01/domestic-news`. All222 files match the
independent rebuild;3,552 exact UTF-8 ranges,3,749 evidence pins and64 images pass.
Fifty blocks retain328 physical prose/heading rows. Sixteen news items preserve
four column/page continuations,111 physical wraps andthree uncaptioned photographs.
Four tables retain24 rows,92 cells/16 headers and108 cell lines;13 cell wraps,two
spatial headers andfour merged training-table cells remain explicit. Forty serialized
table rows are not claimed as source physical rows. Four table contexts,two image
contexts andall sixteen heading/body associations validate.

정보 레이다0013 is a non-owning section heading. The rotated opening masthead and
running headers read 정보레이다; earlier lookup-only 정보교류 notes are preserved
with an explicit erratum. Canonical titles and sibling parent0008 relationships stay
unchanged;no duplicate body or invented hierarchy. Parent정보모음0008 remains unresolved.
PDF161 is an independent advertisement;168 starts 나라밖 소식 and169 continues it.
Foreign-news extent andrestoration remain pending.

Forty source candidates,two ink marks and24 Unicode approximations retain originals.
Printed5바이트씩15비트,수수강신청서,Jonus Ada,두격,awkward grammar andcontest totals
28작품/28명/58매/66대 remain literal. Photograph-label transcription,human acceptance,
full proofreading,source encoded bytes andhistorical/product claims remain unverified.
All64 original/two revised crops preceded50 kor+eng tasks;all drafts were read before
one source correction pass. Two table-edge expansions preceded recognition;no OCR
failure/retry. All37,808 prior files and30 implementation pins remain exact;unchanged
213-test baseline reused. The preservation inventory now contains38,717 files.
Current totals: 25 readable, no partial articles, three non-owning headings and28 unresolved.

Batch36 restores 나라밖 소식0015 opening166–171/PDF168–173 as partial at
`archive/pdf/1985-02/packages/batch-36-r01/foreign-news-a`. All234 files match its
independent rebuild;4,311 exact UTF-8 ranges,4,495 evidence pins and61 images pass.
Fifty-five blocks retain474 physical rows,13 complete news items andthe opening
IBM PC AT report. Nineteen numbered features,four bullets,nine subheadings,ten
internal connections and171 physical wraps remain source-linked. Outgoing 유력/한
continues onPDF174; native fragments remain separate for later assembly.

The verified full extent is166–174/PDF168–176. Final176 foreign text occupies the
whole left column andupper-right;the lower-right boxed 원고 모집 광고0016 is
separate andexcluded. PDF177 is an independent Silicon Valley Fever book advertisement.
Fifty-eight source candidates,two ink marks,one unknown ellipsis band and137 Unicode
approximations retain originals. Printed70/780nm,300/360KB,Rodert Wasserman,Wall Fargo,
Microcrompu-ter,Iomgega,Bern-onlli andsource errors remain literal. All61 original/
one revised crops preceded55 kor+eng tasks;all raws read before one source pass.
No OCR failures/retries. All38,717 prior files and30 implementation pins remain exact;
unchanged213-test baseline reused. Preservation inventory: 39,671 files.
Current totals: 25 readable, one partial article, three non-owning headings and27 unresolved.

Batch37 restores 나라밖 소식0015 ending172–174/PDF174–176 at
`archive/pdf/1985-02/packages/batch-37-r01/foreign-news-b`. All98 files match its
independent rebuild;1,793 current UTF-8 ranges,one incoming native range,1,877 evidence
pins and27 images pass. Twenty-one blocks retain190 physical rows,three complete
news items andthe AT report ending. Five internal connections,72 physical wraps,
incoming 유력/한 andthree PLD subheadings remain source-linked. Two original PLD
images retain separate links to the two caption lines. Final176 lower-right0016
notice is excluded from every selected asset;uncut source is preserved as evidence.

Allnine source pages166–174 now exist in two immutable natives;article availability
remains partial until complete assembly. Thirty-six localized candidates and16 Unicode
approximations retain originals,including 강행했거,자회사,파콜,롬/M과,Co-upled,
게이전트압이,버/터회로,1천83/1013,MIM/MMI,벽이라도고 andfinal체계화하는.
All27 original crops preceded21 kor+eng tasks;all drafts read before one source pass.
No OCR failure,retry orcrop repair. All39,671 prior files and30 implementation pins
remain exact;unchanged213-test baseline reused. Preservation inventory: 40,085 files.
Current totals remain25 readable,one partial article,three non-owning headings and27 unresolved.

나라밖 소식0015 is complete at `archive/pdf/1985-02/packages/foreign-news-complete-r01`,
printed166–174/PDF168–176. All340 files match the independent rebuild;all332 native
files andfull correction metadata remain exact. Forty-four category slices/nine objects
reverse to their native records,retaining6,104 projected UTF-8 ranges. All6,209 active
ranges,6,372 native evidence pins and88 images pass. Use the pinned private
`foreign_news_literal.check` / `foreign_news_literal.installed` adapter and reproduction.json.

Seventeen complete news items retain664 physical rows,19 numbered features,four bullets,
12 subheadings,two PLD image/caption associations and243 physical wraps. The AT report
retains its opening andending native associations;15 internal prose connections plus
유력/한 link the original fragments without rewriting them. Final176 lower-right
canonical0016 notice remains excluded. Ninety-four candidates,two ink marks,one unknown
ellipsis band and153 Unicode approximations retain source errors andliteral discrepancies.
Image-label transcription,human acceptance,full proofreading,source bytes andclaims
remain unverified. No body pages orarticle assembly remain pending.

Four exact native stage notes andtwo ledger deferrals are resolved only in active status;
all originals remain preserved. Six negative probes reject altered ranges,AT coverage,
caption targets,final notice inclusion anddeferred ending. No new mapping,rendering,OCR
orsource correction. All40,085 prior files and30 implementation pins remain unchanged;
213-test baseline reused. Preservation inventory: 40,791 files.
Current totals: 26 readable,no partial articles,three non-owning headings and27 unresolved.

Batch38 completes 원고 모집 광고0016 on the lower-right of174/PDF176 at
`archive/pdf/1985-02/packages/batch-38-r01/call-for-papers`. All17 files match its
independent rebuild;114 exact UTF-8 ranges,127 evidence pins andthree images pass.
Two blocks retain19 physical rows,four contact fields,three submission terms andsix
wraps. The complete notice frame is preserved;all selected regions are disjoint from
completed foreign news. Canonical TOC eligibility includes this notice despite its title.

Printed이시겠읍니까?,일류 필자로,접수일로 부터,address36-4,telephone783-2296
and10일 return wording remain literal. Four localized candidates retain source links;
contact validity,human acceptance,full proofreading andsource bytes remain unverified.
Allthree crops precededtwo kor+eng tasks;both drafts read before one source pass.
No OCR failure,retry orcrop repair. All40,791 prior files and30 implementation pins
remain exact;unchanged213-test baseline reused. Preservation inventory: 40,887 files.
Current totals: 27 readable,no partial articles,three non-owning headings and26 unresolved.

Batch39 completes 프린터 마스터0041 on printed176–181/PDF178–183 at
`archive/pdf/1985-02/packages/batch-39-r01/printer-master`. All166 files match the
independent rebuild;12,919 exact UTF-8 ranges,14,238 evidence pins and46 images pass.
Thirty-seven blocks retain540 non-table physical text rows,including468 code rows.
The listing preserves447 ordinals0000–0446,21 unnumbered object-byte continuations,
2,144 fields/1,132 blanks and773 literal object bytes. Two command tables retain26
merged cells/35 cell lines;table serialization is separate from physical source rows.
Six boxed keys,14 commands,15 physical wraps and17 listing boundaries remain indexed.

Final0446 E305 contains a semicolon,correcting the preliminary address-only observation;
original notes remain. No END is invented. Korean year/month glyphs in a DEFM string
remain independent of printed object bytes. Thirty-eight source candidates,two ink marks,
eleven unknown decorative bands,19 Unicode approximations and1,743 unknown space bands
retain original scans. Shared181 lower-right contest0023 remains excluded and pending.
All46 original/nine revised crops preceded37 tasks(18eng/19kor+eng);all drafts were
read before one source pass. No OCR failure/retry. Initial verifier schema-key failure
is preserved;the revised verifier passes without changing source/package data.
All40,887 prior files and30 implementation pins remain exact;213-test baseline reused.
Preservation inventory: 41,590 files. Human acceptance,full proofreading,source bytes,
spacing,execution andtechnical claims remain unverified. No reader rebuild.
Current totals: 28 readable,no partial articles,three non-owning headings and25 unresolved.

Batch40 completes 10진수를 2진수∼16진수까지로0023 on printed181/PDF183 at
`archive/pdf/1985-02/packages/batch-40-r01/decimal-conversion`. All34 files match its
independent rebuild;339 exact UTF-8 ranges,364 evidence pins andseven images pass.
Six blocks retain14 physical text rows,including one BASIC label1 across nine code rows.
Eight wraps,three quoted strings,15 statements andone branch target remain indexed;
the split409/6 constant andN/0(10)? prompt retain their original physical rows.
Eight source candidates include the ambiguous0/O/Q prompt glyph. Eight Unicode
approximations and67 unknown space bands retain scans. No syntax oraddress repair.

Heading0019 is non-owning: the same1-LINE 콘테스트 우수작 label appears above
allfour independently titled children on103/133/158/181. Allcanonical identities and
parent links remain;the otherthree contest bodies stay unresolved. The complete0023
panel is source-disjoint from completedprinter0041. Author박문길,platform애플컴패티블
andhistoricaladdress길음3동126-27 remain literal. Allseven crops preceded six tasks
(one eng/five kor+eng);all drafts were read before one source pass. No crop repair,
OCR failure orretry. All41,590 prior files and30 implementation pins remain exact;
unchanged213-test baseline reused. Preservation inventory: 41,757 files.
The active PDF184 heading is corrected to매월 소프트웨어 공모;the prior이달의
observation remains preserved. Human acceptance,full proofreading,source bytes,
spacing,execution andcontact validity remain unverified. No reader rebuild.
Current totals: 29 readable,no partial articles,four non-owning headings and23 unresolved.

Batch41 completes GR타입의 숫자 쓰기0020 on103/PDF105 and파노라마II0021
on133/PDF135 at `archive/pdf/1985-02/packages/batch-41-r01/gr-numbers` and
`archive/pdf/1985-02/packages/batch-41-r01/panorama-ii`. Each34-file package matches
its independent rebuild. GR passes479 exact UTF-8 ranges/504 evidence pins;panorama
passes174 ranges/199 pins. All14 image crops match their source pixels andexclude
completedPASCAL/music panels andthe lower bookshop advertisement.

GR retains12 physical code rows,one BASIC label1,eleven wraps,three quoted strings
andall50 digits in4/28/18-character physical fragments. Two quoted blank-space bands
retain explicit unknown counts;the W$ gap is visibly wider than Y$. B/$ andGOTO/1
wraps remain. Panorama retainsfive code rows,one label1,four wraps,IMOD/6,Y=Y/+K,
THEN's T/HEN split andcompactNEXTELSENEXT without syntax repair. Together the packages
retain27 physical text rows,32 lexical colon groups,21 source candidates,30 Unicode
approximations and80 unknown space bands. Authors,platforms andaddresses remain literal.

All14 original/one revised crops preceded12 tasks(two eng/ten kor+eng);all drafts
were read before one source pass. One GR byline trim;no OCR failure/retry.
All41,757 prior files and30 implementation pins remain exact;213-test baseline reused.
Preservation inventory: 42,052 files. Heading0019 andallfour childlinks remain unchanged.
Human acceptance,full proofreading,source bytes,spacing,execution andcontact validity
remain unverified. No reader rebuild.
Current totals: 31 readable,no partial articles,four non-owning headings and21 unresolved.

Batch42 completes 추종자0022 on printed158/PDF160 at
`archive/pdf/1985-02/packages/batch-42-r01/follower`. All 34 files match the
independent rebuild; 209 exact UTF-8 ranges, 234 evidence pins and seven source-pixel
crop comparisons pass. Its complete contest panel matches the existing MLE exclusion;
completed MLE and lower book advertisements remain outside its ownership.

Twelve physical text rows retain seven BASIC rows, one numeric label1, six wraps,
two quoted strings, thirteen lexical colon groups and the symbolic LABEL/GOTO C.
The quoted label closes on the next physical row; PEE/K and AM/OD99 wraps remain.
Square brackets in both CIRCLE groups, 6^6 carets, compact POKEM and all numeric
fields remain literal. Ten source candidates, eleven Unicode approximations and
one unknown encoded-space band retain scans. Author 정 지 윤, SPC-1000 and the
historical address remain as printed. No syntax, arithmetic or contact repair.

All seven crops were reviewed before six tasks (one eng/five kor+eng); all drafts
were read before one source pass. No crop repair, OCR failure or retry.
All 42,052 prior files and 30 implementation pins remain exact; the unchanged
213-test baseline is reused. Preservation inventory: 42,211 files.
All four 1-LINE contest children are now readable; heading0019 and canonical links
remain unchanged. Human acceptance, full proofreading, source bytes, spacing,
execution and contact validity remain unverified. No reader rebuild.
Current totals: 32 readable, no partial articles, four non-owning headings and 20 unresolved.

Batch43 completes 공모 총평0043, source headline 새학기 준비, on printed183/PDF185
at `archive/pdf/1985-02/packages/batch-43-r01/competition-review`. All 34 files match
its independent rebuild; 706 exact UTF-8 ranges, 780 evidence pins and eight image
crops pass. Two columns retain 59 prose rows and their continuation. Three other
text rows, seven paragraph segments, 57 physical row boundaries, three quoted titles
and seven historical award/software claims remain source-linked.

The winners table retains four headers and twenty data cells in six serialized
rows, with every repeated value linked to its own occurrence. Pipes are editorial
cell separators; the original table and full page remain available. Fifteen source
candidates include the contributor-name glyph 록 (raw OCR 목); six quote glyphs
remain Unicode approximations. Historical wording, names, award counts and claims
remain literal. The TOC credit 편집부 is not inserted as an unprinted body byline.

Parent0042 공모 입상 is now non-owning: source openings on PDF185,186,198 show its
three independently titled children under review, top-prize and prize section labels.
All canonical identities and three child links remain unchanged. The preceding
PDF184 monthly recruitment notice remains independently owned.

All eight crops were reviewed before six kor+eng tasks; all drafts were read before
one source pass. No crop repair, OCR failure or retry. Two preparation failures are
retained: unsupported map kind, then PNG-byte comparison corrected to decoded pixels.
Both stopped before OCR. All 42,211 prior files and 30 implementation pins remain
exact; the unchanged 213-test baseline is reused. Preservation inventory: 42,383 files.
Human acceptance, full proofreading, source bytes, spacing and historical claims
remain unverified. No reader rebuild.
Current totals: 33 readable, no partial articles, five non-owning headings and 18 unresolved.

Batch44 restores 전학년 성적 처리 프로그램0044 opening printed184–189/PDF186–191
at `archive/pdf/1985-02/packages/batch-44-r01/grades-a`, with partial availability.
The full twelve-page extent is verified as printed184–195/PDF186–197. Ending six
pages and separate article assembly remain pending. All 108 files match the independent
rebuild; 15,978 exact UTF-8 ranges, 16,065 evidence pins and 30 crop images pass.

Both BASIC listings are complete within this segment: 431 physical code rows retain
296 labels, 135 wraps, 177 quoted strings and 668 statement groups. Three same-label
column joins preserve2010 SN/UM,4310 PRIN/T#1 and8110 MI/D-1. Numeric-only rows and
0 THEN/1 ELSE prefixes remain continuations. Final9010 RETURN and2050 RESUME stay
literal. Two captions, the printed credit, seven requirements, nine claims, three
command examples and the introductory column continuation retain source links.

Seven unknown quoted-space bands and faint terminal punctuation at list2 line290
remain explicit editorial markers. Thirty-seven candidates retain FISRT, independent
prompt punctuation/dimensions, literal arithmetic, faint1020–1080 readings, historical
spelling and credit. Six Unicode approximations and 1,223 display-space bands do not
certify source bytes. Focused review removed an unsupported draft blank inside <=;
initial transcripts and all focused crops remain preserved. No syntax or claim repair.

Seven original images retain five whole pages and the two owned listing panels on
PDF189; its separate lower-right publisher advertisement is excluded. The compilation
paragraph ends 않는 onPDF191 and continues 다. on192. All 30 original/seven expanded
crops were reviewed before 23 tasks (11eng/12kor+eng); all raws preceded one source
pass. Zero OCR failures/retries. All 42,383 prior files and 30 implementation pins
remain exact; the unchanged 213-test baseline is reused. Preservation inventory:
42,909 files. Human acceptance, full proofreading, source bytes, spacing and execution
remain unverified. No reader rebuild.
Current totals: 33 readable, one partial article, five non-owning headings and 17 unresolved.

Batch45 restores 전학년 성적 처리 프로그램0044 ending printed190–195/PDF192–197
at `archive/pdf/1985-02/packages/batch-45-r01/grades-b`. All twelve body pages now
exist across immutable grades-a and grades-b; separate article assembly remains pending.
All 155 files match the independent rebuild. Checks pass for 6,981 current UTF-8 ranges,
82 exact opening-native references, 7,194 evidence pins and 42 crop images.

Five explanatory tables retain 67 logical rows, 134 cells and 157 cell fragments,
including the445–450 description continued onto192. Their 43 printed line references
retain 81 exact BASIC endpoint associations. The335 other physical text rows and89
table serialization rows preserve the sixteen compilation steps (⑩ absent), seven menu
options, ten command examples, six example groups and nine page/column continuations.
The incoming 않는/다. association links to the unchanged opening native.

Six whole pages and the captioned final printout remain as original images. Internal
printout label/data transcription is pending volunteers. Thirty-six source candidates
retain BASOCM.COM, the visually confirmed772085 (raw72085), ENGLI, DSKETTE, 횟수을,
and caption 출력된 전체 성적을 화면. Printed⑤⑥ placement, .BAS/.COM instructions,
filename punctuation and claims remain independent; no arithmetic or syntax repair.
One ellipsis-count uncertainty,110 Unicode approximations and1,994 display-space bands
remain explicit. Human acceptance, full proofreading, source bytes and execution unverified.

All42 original/one trimmed crops preceded35 kor+eng tasks; all drafts preceded one
source pass. Zero OCR failures/retries. An unsupported heading map kind failed before
output; the fresh map uses section-label. A missing-import verifier failure is retained;
its revision changes only the checker. All42,909 prior files and30 implementation pins
remain exact; the unchanged213-test baseline is reused. Preservation inventory:
43,568 files. No reader rebuild.
Current totals: 33 readable, one partial article, five non-owning headings and 17 unresolved.

전학년 성적 처리 프로그램0044 is complete at
`archive/pdf/1985-02/packages/grades-complete-r01`, printed184–195/PDF186–197.
All 272 files match the independent rebuild; all 263 native files and full correction
metadata remain exact. Ninety-four category slices and eleven object projections
reverse to native records across 22,959 original UTF-8 range occurrences. All 25,275
active ranges, 23,341 native evidence pins and 72 crop images pass.
The article retains 828 physical text rows plus 89 table serialization rows, two BASIC
listings with 431 physical rows/296 labels/135 wraps/177 quoted strings/668 statements,
five tables with 67 logical rows/134 cells/157 fragments, three captions and eleven
continuations. All 43 printed listing references retain their 81 endpoint associations;
these and the incoming 않는/다. join resolve into complete-article ranges while original
native references remain unchanged. Sixteen compilation steps still omit⑩; seven menu
options and the original placement of⑤⑥ remain literal. The independent lower-right
publisher notice on187/PDF189 remains excluded.
Seventy-three source candidates, eight unknown bands, one ellipsis-count uncertainty,
116 Unicode approximations and 3,217 unknown encoded-space bands remain explicit.
BASOCM.COM,772085,ENGLI,FISRT,DSKETTE and caption성적을 화면 retain their source forms.
Internal printout data/label transcription is pending volunteers. Four stage notes resolve
only in active status; all original notes, source discrepancies and uncertainties survive.
No new mapping, rendering, OCR or source correction. Eight negative probes reject altered
ranges, references, labels, captions, compilation numbering, ownership and deferred coverage.
All 43,568 prior files and 30 implementation pins pass; unchanged213-test baseline reused.
Use the pinned private `restoration/grades-assembly/grades_literal.py` checker/context
and `reproduction.json`; the generic checker alone does not recognize this format.
Current totals: 34 readable, no partial articles, five non-owning headings and 17 unresolved.

Batch46 restores 시간표 작성 프로그램0045 opening printed196–201/PDF198–203
at `archive/pdf/1985-02/packages/batch-46-r01/timetable-a`. Full extent is seven
pages196–202/PDF198–204; final202/PDF204 and complete assembly remain pending.
All 222 files match the independent rebuild. Checks pass for 10,948 exact UTF-8 ranges,
11,127 evidence pins and 60 crop images. The segment retains 384 physical text rows
plus76 table serialization rows, including262 BASIC physical rows,63 source-label
occurrences,56 distinct labels,199 physical wraps,168 quoted strings and456 lexical
colon groups. Seven repeated0 comment labels and two130 labels retain distinct source
occurrence IDs. All five internal listing joins80/140/230/320/390 remain exact;
final1007 continues onPDF204. List2 character-pattern data is deferred to that page.
Six tables retain74 logical rows,148 cells,150 cell fragments andfour brace groups.
Eighteen printed line references retain31 endpoints:159 and180 have no exact source
label;130 refers to two literal occurrences. No semantic target or repaired label inferred.
Fifteen boxed keys,seven menu options,five prose/table continuations andfour caption
links remain. Three output panels retain one shared caption; internal data/labels await
volunteer transcription. Source T22 duplication,159,S(7)/S(6),DEFCHR$,PROGRAMER,
SPESIAL,1984/9,period2122.,GOTO180 andmemory endpoint56C9 remain independent.
Twenty-six source candidates,37 visible editorial markers,115 Unicode approximations
and1,147 unknown encoded-space bands retain their scans. Human acceptance,full
proofreading,source bytes,spacing,claims andexecution remain unverified.
All60 original/six widened crops preceded51 OCR tasks (six eng/45 kor+eng); all drafts
preceded one source pass. No OCR failure/retry. A fresh text revision corrects one O/0
transcription error. Failed map-kind,metadata key-location andverifier particle checks
remain preserved; their revisions change preparation/checking only. All44,135 prior files
and30 implementation pins pass; unchanged213-test baseline reused. No reader rebuild.
Current totals: 34 readable, one partial article, five non-owning headings and16 unresolved.

Batch47 restores final printed202/PDF204 at
`archive/pdf/1985-02/packages/batch-47-r01/timetable-b`. All 34 files match its
independent rebuild; 3,397 current UTF-8 ranges, 3,419 evidence pins, four external
native-range occurrences (three unique) and seven crop images pass. Six blocks
retain 122 physical text rows: 69 BASIC rows and 50 dump rows plus badge/caption.
The incoming1007 fragment, 48 new labels1008–1055, 240 literal DATA fields and
50 dump addresses/400 byte fields through56D2 remain source-linked. Two external
associations retain the incoming1007 and inherited list1 caption; two internal
column joins and the list2 caption retain their exact targets. Nineteen custom-glyph
markers, 29 Unicode approximations, 469 unknown encoded-space bands and31 source
candidates remain explicit. The original prose endpoint56C9 is not changed to56D2.
All seven exact crops preceded six OCR tasks (four eng/two kor+eng); all drafts
preceded one source pass. No crop repair or OCR failure/retry. The original metadata
count of three unique native ranges is retained with an erratum distinguishing four
occurrences; package bytes are unchanged. All45,115 prior-file pins and30 implementation
pins pass; the unchanged213-test baseline is reused. All45,277 files in the new
preservation inventory remain exact. No reader rebuild.
All seven body pages now have verified native packages; complete assembly is pending.
Current totals: 34 readable, one partial article, five non-owning headings and16 unresolved.

시간표 작성 프로그램0045 is complete at
`archive/pdf/1985-02/packages/timetable-complete-r01`, printed196–202/PDF198–204.
All 265 files match the independent rebuild; all256 native files and full correction
metadata remain exact. Eighty-eight category slices and nine projected objects reverse
to their native records across14,345 projected UTF-8 ranges. All18,108 active ranges,
14,554 native evidence pins and67 images pass. The complete article retains506 physical
text rows plus76 serialized table rows,331 BASIC rows/111 label occurrences/104 distinct
labels/220 wraps,168 quoted strings,456 lexical colon groups,50 dump rows/400 byte fields,
six tables74 rows/148 cells/four brace groups,15 boxed keys andseven menu options.
Both incoming1007 andinherited list1 caption associations resolve into complete ranges;
original physical text andall four native-range wrapper occurrences remain exact.
Seven0 comments,two130 labels,missing159/180 andambiguous130 references remain explicit.
The source prose endpoint56C9 is independent ofthe final dump address56D2. Five captions,
five prose/table continuations,three output panels andall seven originals remain.
Fifty-seven source candidates,56 visible unknown markers,144 Unicode approximations and
1,616 unknown encoded-space bands remain; output-panel internal label/data transcription
is pending volunteers. Human acceptance,full proofreading,source bytes,spacing,claims and
execution remain unverified. Four stale stage notes resolve only in active status,with
originals retained. Eight negative probes reject range,link,label,caption,cell,byte and
coverage drift. All45,277 prior files and30 implementation pins pass; the new45,832-file
preservation inventory is exact. No new mapping,rendering,OCR orsource correction;
unchanged213-test baseline reused. Use the pinned private timetable-assembly/
timetable_literal.py checker/context and reproduction.json for rebuild andissue closeout.
Current totals: 35 readable, no partial articles, five non-owning headings and16 unresolved.

Batch48 completes 애플 클럭0047 on printed204–208/PDF206–210 at
`archive/pdf/1985-02/packages/batch-48-r01`. All 181 files match its independent
rebuild; 12,874 exact UTF-8 ranges, 13,015 evidence pins and 49 images pass.
Four BASIC programs and one POKE example retain 262 physical rows, 135 labels,
127 wraps, 58 quoted strings, 371 lexical statements and 49 DATA fields. List1
retains 30 dump rows/240 byte fields, including the literal dot in0318. Three
same-line joins preserve list3/1020, list4/145 and list5/150 across columns/pages.
The address table retains 16 logical rows, 62 cells, five header cells and two
cells spanning1002–1003. Six captions, three prose joins, two original circuit
diagrams and five complete pages retain their source associations. Printed
$2E0/$2E1, 34Hz/68Hz/1/64, prose14minutes versus POKE15, 로시시켜, TRU, MULTY,
leading-zero03 and 클럭장치 remain literal. Q/O/0 and D0/DO candidates remain
explicit. Two unknown space bands, one dot band and one faint terminal letter
remain visible; 38 source candidates, seven Unicode approximations and 2,335
unknown encoded-space bands retain their scans. Circuit-label transcription,
human acceptance, full proofreading, source bytes, claims and execution remain
unverified. All49 original/one widened crops preceded41 OCR tasks (12 eng/29 kor+eng);
all drafts preceded one source pass. No OCR failure/retry. Original transcripts
and the focused table/glyph revision remain preserved. All45,832 prior files and
30 implementation pins pass; the new46,627-file preservation inventory is exact.
The unchanged213-test baseline is reused. No reader rebuild.
Parent0046 테크닉의 극치 is non-owning, with both canonical children0047/0048
unchanged. The printed 테크니컬 banner does not replace the canonical title.
FollowingPDF211 is a separate publisher notice/ad; PDF212 starts0048, with
continuation213 reviewed only for ownership. No parent body or divider is invented.
Current totals: 36 readable, no partial articles, six non-owning headings and14 unresolved.

Batch49 restores the opening210–215/PDF212–217 of 마이크로 컴퓨터 설계 강좌0048,
chapter8 A/D변환기의 접속, at `archive/pdf/1985-02/packages/batch-49-r01`.
All286 files match the independent rebuild;3,970 exact UTF-8 ranges,4,249 evidence
pins and83 images pass. Full extent210–221/PDF212–223 was individually reviewed;
final221 contains concluding prose,parts table1 andlist3/output,followed by the
independent Z80 article222/PDF224. Ending216–221 andimmutable assembly remain pending.
The opening retains65 blocks/285 physical transcript rows,nine numbered diagrams,
one illustration andtwo original tables. Fifteen table rows retain79 populated cells,
14 headers,24 blanks andtwo spanning cells;multiline timing fields remain indexed.
Eleven caption links,ten prose connections,42 selected physical wraps,four numbered
steps andoutgoing변환 결과를 retain source associations. ICL7107,caption6 OBOB glyph
candidate,20V×1256,1/256,78mV,미분직선성,전환종료 andtiming8+2/μS/클럭주기 remain
literal. Thirty-one source candidates,87 Unicode/subscript approximations and1,179
unknown encoded-space bands retain scans. Diagram-label transcription,human acceptance,
full proofreading,source bytes,spacing,claims,circuit behavior andexecution remain unverified.
All83 original/two revised crops preceded65 kor+eng tasks;all drafts preceded one
source pass. No OCR failure/retry. The rejected map-ID attempt andinitial checker
assumption about absent listing.txt remain archived;only preparation/checker changed.
All46,627 prior files and30 implementation pins pass;47,815 files are now preserved.
The unchanged213-test baseline is reused. No reader rebuild.
Current totals: 36 readable, one partial article, six non-owning headings and13 unresolved.

Batch50 restores final216–221/PDF218–223 of 마이크로 컴퓨터 설계 강좌0048 at
`archive/pdf/1985-02/packages/batch-50-r01`. All275 files match the independent
rebuild;5,976 current exact UTF-8 ranges,one incoming native range,6,290 evidence
pins and77 images pass. The ending retains63 blocks/413 physical transcript rows,
seven numbered diagrams,parts-table original andsix complete pages. List1 retains
69 assembly rows/196 fields/80 blank fields/six EQU constants;lists2/3 retain16
BASIC labels,36 output rows/81 numeric fields,six prompt-response pairs anda final
unanswered prompt. Two independent parts lists retain27 rows/47 cells/seven blank
quantities. Eleven caption links,five prose connections,one listing continuation,
80 physical wraps,five complete overbar groups andthe incoming native boundary pass.
Duplicate③,28V versus figure2.8V,REF IF⁺,진압,음궤한,CMMR,DIT,ADC082-!,AF. and
missing THEN remain literal. Thirty-seven source candidates,one faint-glyph marker,
55 Unicode approximations and1,424 unknown encoded-space bands retain original scans.
All77 original/eight revised crops acrosssix repaired regions preceded63 OCR tasks
(8 eng/55 kor+eng);all drafts preceded one source pass. No OCR failures/retries.
All47,815 prior files and30 implementation pins pass;48,957 files are preserved.
The unchanged213-test baseline is reused. No reader rebuild. All twelve body pages
are now restored across two immutable natives;complete article assembly is pending.
Current totals: 36 readable, one partial article, six non-owning headings and13 unresolved.

마이크로 컴퓨터 설계 강좌0048 is complete at
`archive/pdf/1985-02/packages/design-complete-r01`, covering printed210–221/PDF212–223.
All 570 files match the independent rebuild; all 561 native files and full correction
records remain exact. Seventy-four category slices and ten objects reverse to their
original metadata across 9,946 projected UTF-8 ranges. All 10,431 active ranges,
10,540 native evidence pins and 160 images validate. The assembly retains 128 blocks,
698 physical transcript rows, sixteen numbered diagrams, one illustration, three
original table panels and twelve complete pages. Three tables/four independent lists
retain 42 logical rows, 126 cells, 15 headers, 31 blank slots and two spanning cells.
List1 retains 69 assembly rows/196 fields/80 blanks/six EQU constants; lists2/3 retain
16 BASIC labels, 36 output rows/81 numeric fields, six prompt-response pairs and one
unanswered prompt. Twenty-two captions, sixteen complete prose continuations, one
listing continuation, 122 physical wraps and five signal-overbar groups remain.
The incoming 변환 결과를/A 레지스터에서 boundary and opening list1 reference resolve
without rewriting text. Sixty-eight candidates, one faint-glyph marker, 142 Unicode
approximations and 2,603 unknown encoded-space bands retain scans. Four native stage
notes and one ledger deferral are resolved only in active status; originals remain.
Use the pinned private `restoration/design-assembly/adc_design_literal.py` checker
or its `installed()` context; see `reproduction.json`. Eight negative probes reject
range, boundary, caption, blank-slot, assembly-row, coverage and ending corruption.
All 48,957 prior files and 30 implementation pins pass; 50,120 files are preserved.
No new mapping, rendering, OCR or source correction; unchanged 213-test baseline reused.
Current totals: 37 readable, no partial articles, six non-owning headings and13 unresolved.

Batch51 completes 알려지지 않은 Z80 명령어0049, printed222–223/PDF224–225, at
`archive/pdf/1985-02/packages/batch-51-r01`. All 306 files match the independent
rebuild; 4,465 exact UTF-8 ranges, 4,736 evidence pins and81 images pass.
Six tables retain52 logical rows,273 nonblank cells,six blanks,33 headers,29 row
headers,four axes and57 source underline groups. Two assembly examples retain15
physical rows/printed ordinals,77 fields,28 blank fields,22 bytes andfour labels.
Six captions,three table references,one example association,four prose continuations
and37 physical wraps remain linked. Printed Ediwin,DFB,RLO,RR .C,BIT b C,
OUT (C),L under60,LD (nn),H,CPRI andD000 remain literal. Printed ranges andthe4–7
row group are not expanded. Thirty source candidates,two faded ED prose bands,
seven Unicode approximations and787 unknown encoded-space bands retain scans.
All81 original/eight revised crops acrossseven regions preceded72 OCR tasks
(2 eng/70 kor+eng);all drafts preceded one source pass. No OCR failures/retries.
All50,120 prior files and30 implementation pins pass; 51,351 files are preserved.
All table/example labels are transcribed; no diagram-label task remains for0049.
The unchanged213-test baseline is reused. No reader rebuild.
Current totals: 38 readable, no partial articles, six non-owning headings and12 unresolved.

Batch52 completes MAT 함수0050, printed224–227/PDF226–229, at
`archive/pdf/1985-02/packages/batch-52-r01`. All 293 files match the independent
rebuild; 5,909 exact UTF-8 ranges, 6,133 evidence pins and 86 images pass.
Twelve listing panels retain 142 BASIC rows/labels, 144 lexical statements, four
quoted strings, eight quote delimiters, ten branch targets and twelve DATA fields.
Three matrices retain 21 cells in nine rows, with original geometry alongside an
editorial text layout. Three equations retain twelve numeric fields, nine variables
and nine operators; six formulas and five output rows/six fields remain independent.
Twelve captions, fourteen prose references, three line references, seven continuations
and 36 physical wraps remain linked. Printed PUT1S, J=1, D(RB), X=RB, OUTOUT,
determinent, baseline B=AT, the beta glyph, raised marks after1530/1910 and list10
references remain literal. Thirty source candidates, 39 Unicode approximations and
1,094 unknown encoded-space bands retain scans. All matrix/listing labels are transcribed.
All 86 original crops and one widened caption preceded 66 OCR tasks (12 eng/54 kor+eng);
all drafts preceded one source pass. No OCR failures/retries. Six page views were reused.
All 51,351 prior files and 30 implementation pins pass; 52,539 files are preserved.
The unchanged 213-test baseline is reused. No reader rebuild.
Current totals: 39 readable, no partial articles, six non-owning headings and 11 unresolved.

Batch53 completes 그랜드 캐년0052, printed228–231/PDF230–233, at
`archive/pdf/1985-02/packages/batch-53-r01`. Parent 게임 모음0051 is non-owning;
all five child identities and relationships remain unchanged. Independent openings
on PDF230,234,238,246,251 support the parent classification; other children remain pending.
All 185 files match the independent rebuild; 20,028 exact UTF-8 ranges,
20,178 evidence pins and 53 images pass. Twenty-six BASIC labels in 28 physical
rows retain three quoted strings, six delimiters, 28 lexical statements, 96 DATA fields
and two wraps. The six-column dump retains 293 rows, 2,340 byte fields and every
address, including the final four-byte6920 row. Three command panels, two monitor
entry rows/nine bytes, eight screen labels/eight values and eleven boxed keys remain.
Two captions, six references, twelve listing joins, one prose column join and
53 physical prose wraps remain linked. Printed L$923, checksums4288/265976,
range28672–28761, 96 DATA fields, setupX/Z versus inplayA/Z and source spelling
remain independent; no byte, syntax, length or checksum repair. Thirty-two candidates,
two editorial mark descriptions, sixteen Unicode approximations, 2,834 unknown
encoded-space bands and three vertical gaps retain scans. All visible labels transcribed.
All 53 original/six revised crops preceded 41 OCR tasks (17 eng/24 kor+eng); all drafts
preceded one source pass. No OCR failures/retries. One metadata revision corrects the
left countdown3 occurrence link; all text and earlier versions remain unchanged.
All 52,539 prior files and 30 implementation pins pass; 53,332 files are preserved.
The unchanged 213-test baseline is reused. No reader rebuild.
Current totals: 40 readable, no partial articles, seven non-owning headings and 9 unresolved.

Batch54 completes 포도 귀신0053 (source 포도귀신), printed232–235/PDF234–237,
at `archive/pdf/1985-02/packages/batch-54-r01`. All 121 files match the independent
rebuild; 10,259 exact UTF-8 ranges, 10,365 evidence pins and 37 images pass.
Seven BASIC panels retain 185 labels in 256 physical rows, 71 wraps, eleven quoted
strings, 22 quote delimiters, 245 lexical statements, 216 DATA fields, 43 branch
targets and 1,972 lexical tokens. Exact label/token fragments cover all nonspace code.
Six listing joins include the same-line1110 and2210 continuations. Eleven program
range descriptions retain thirteen physical rows and the open-ended2800 range.
Four screen labels/values, four boxed keys, one description column join and29 prose
wraps remain linked. The listing and screen have no invented captions. Final lower
academy advertisement is excluded; eligible top, folio235 and private full-page evidence remain.
Source spelling, all-BASIC claim, percent variables,1090 raised mark, physical digit/
variable/string wraps and quoted spaces remain literal. Thirty-four candidates,
eight Unicode approximations and1,245 encoded-space bands (including15 quoted bands)
retain scans. All visible labels are transcribed; execution remains unverified.
All37 original/two revised crops preceded25 OCR tasks (7 eng/18 kor+eng); all drafts
preceded one source pass. No OCR failures/retries. Initial preparation's12-range count
is corrected explicitly to11 in the selected map, indexes and active record; originals remain.
All53,332 prior files and30 implementation pins pass; 53,867 files are preserved.
The unchanged213-test baseline is reused. No reader rebuild.
Current totals: 41 readable, no partial articles, seven non-owning headings and 8 unresolved.

Batch55 restores 소혹성 지대0054 opening printed236–241/PDF238–243 at
`archive/pdf/1985-02/packages/batch-55-r01` as a partial native. Its full eight-page
extent is printed236–243/PDF238–245; the final two pages and complete assembly remain pending.
All 218 files match the independent rebuild; 39,924 exact UTF-8 ranges,
40,110 evidence pins and68 image decodes pass. One BASIC panel retains39 labels/
physical rows1000–1380, ten quoted strings/20 delimiters,39 lexical statements,
five branches,218 lexical tokens and14 quoted-space bands. Twelve dump columns retain
612 rows/4,896 literal byte fields C100–D418 and eleven column/page connections.
Four command regions/five physical command rows, eight routine descriptions/ten
addresses, four boxed keys, five opaque screen fields, two captions/two references,
two regional continuations and45 physical prose wraps remain indexed.
Printed SC * 256, save bound &HD9FF, repeated load-heading wording, 갯수/리턴키이를,
byte discrepancies and all source spelling remain literal. Thirty-eight candidates,
seven editorial markers (including two unknown asterisk counts), twelve Unicode
approximations and5,463 encoded-space bands retain originals. Five low marks and
four raised marks remain independent of the indexed byte fields. Tiny painted labels
inside the original illustration remain pending volunteers; screen/listing labels are transcribed.
All59 original crops and ten replacement command/prose crops preceded47 OCR tasks
(17 eng/30 kor+eng); all drafts preceded one source pass. No OCR failures/retries or
coverage repairs. Four running-head crops omitted by the sheet predicate were inspected
separately before OCR. Metadata revisions correct the preparation's missingH in &HD9FF
and a narrative low-mark count; source text and every original version remain preserved.
All53,867 prior files and30 implementation pins pass; 54,788 files are preserved.
The unchanged213-test baseline is reused. No reader rebuild.
Current totals: 41 readable, one partial article, seven non-owning headings and 7 unresolved.

Batch56 restores 소혹성 지대0054 ending printed242–243/PDF244–245 at
`archive/pdf/1985-02/packages/batch-56-r01`. All 52 files match the independent
rebuild; 11,558 current exact UTF-8 ranges, three inherited native ranges,
11,614 current evidence pins and16 images pass. Five dump columns retain189 rows/
1,512 literal byte fields D420–DA00, with column lengths51/51/51/18/18 and eight final
zero fields. Four column connections, the exact incoming D418/D420 boundary and the
opening list2 caption remain linked to immutable batch55 evidence. Twenty-eight source
candidates, one editorial address-side mark atD600, one raised-separator Unicode
approximation atD938 and1,513 encoded-space bands retain originals. No byte, address,
command or length repair; printed save bound &HD9FF remains independent of finalDA00.
Final245 right LOGATOR contest and lower reader errata are excluded; the complete
eligible dump panel and folio243 remain, with full-page evidence preserved privately.
All16 original/two revised crops preceded nine OCR tasks (5 eng/4 kor+eng); all drafts
preceded one source pass. No OCR failures/retries. The first dump column's right margin
was widened and a blank folio crop moved up before OCR; both original attempts remain.
All54,788 prior files and30 implementation pins pass; 55,031 files are preserved.
The unchanged213-test baseline is reused. No reader rebuild.

All eight article pages236–243/PDF238–245 are now covered in two immutable natives;
complete article assembly remains pending. Together they retain931 physical text rows,
845 code rows,39 BASIC labels/rows, ten quoted strings/20 delimiters,39 statements,
five branches,218 lexical tokens,14 quoted-space bands,801 dump rows/6,408 literal
byte fields in17 columns, four command regions/five rows, eight routine descriptions/
ten addresses, five screen fields, four boxed keys, two captions plus the inherited
association, fifteen internal dump joins and the incoming boundary, two regional
continuations and45 prose wraps. Sixty-six source candidates, eight editorial markers,
thirteen Unicode approximations and6,976 encoded-space bands remain explicit.
Current totals: 41 readable, one partial article, seven non-owning headings and 7 unresolved.

소혹성 지대0054 is complete at `archive/pdf/1985-02/packages/asteroid-complete-r01`,
printed236–243/PDF238–245. All 279 files match the independent rebuild;
all270 native files and both full correction records remain exact. Eighty category
slices/twelve objects and51,482 projected ranges reverse to their native records.
All78,224 active exact ranges,51,724 native evidence pins and84 image decodes pass.
Complete indexes retain931 physical text rows,845 code rows,39 BASIC labels/rows,
ten quoted strings/20 delimiters,39 statements,five branches,218 lexical tokens,
14 quoted-space bands,801 dump rows/6,408 literal byte fields in17 columns,
four command regions/five rows,eight routine descriptions/ten addresses,five opaque
screen fields,four boxed keys,two captions/two references,16 dump connections,
two regional continuations and45 prose wraps. The exact D418/D420 boundary and
inherited list2 caption resolve without rewriting physical text. External evidence
retains its native namespace; separate complete indexes use article coordinates.
Sixty-six source candidates,eight editorial markers,thirteen Unicode approximations
and6,976 encoded-space bands remain explicit. SC * 256, &HD9FF versus finalDA00,
repeated load-heading wording and all byte/glyph/spelling discrepancies remain literal.
Final245 right LOGATOR contest and lower errata remain excluded; eligible panel/folio
and complete private source-page evidence remain. Tiny illustration labels are pending volunteers.
Six completed stage notes are resolved only in active metadata; originals remain.
The first verifier compared a code-row dictionary with its shorter logical reference;
a fresh revision checks their exact shared fields. The selected adapter also rejects
changed BASIC label metadata. Both original attempts remain; no source/output change.
All eight negative probes reject range,incoming,caption,label,byte or deferred-coverage drift.
All55,031 prior files and30 implementation pins pass; 55,617 files are preserved.
Use the pinned private `restoration/asteroid-assembly/asteroid_literal_r02.py`
checker/context and its `reproduction.json`; generic package check alone does not
recognize this format. No new mapping,render,OCR or source correction. The unchanged
213-test baseline is reused. No body pages or article assembly remain pending.
Current totals: 42 readable, no partial articles, seven non-owning headings and 7 unresolved.

Batch57 completes 부메랑 소년0055 (source 부메랑소년), printed244–248/PDF246–250,
at `archive/pdf/1985-02/packages/batch-57-r03`. All 136 files match the independent
rebuild; 19,587 exact UTF-8 ranges,19,711 evidence pins and43 image decodes pass.
Nine BASIC panels retain377 labels in435 physical rows,58 wraps,50 quoted strings/
96 delimiters (four source quotes remain unclosed),383 lexical statements,416 literal
hex DATA fields in13 sprite groups,24 branch targets and3,756 lexical tokens.
Nine PLAY strings/122 characters,one DRAW string,seven graphic-key bands4430–4490,
four wavy-glyph strings/twelve band markers,two boxed arrow keys,one printed program
range,eight listing connections and21 prose wraps retain exact associations.
Source REM END3810 remains independent of actual final4760. Split TX/STR$/MS/ME,
41/00 branch target,compact PUTSPRITE,PLAY0/O/5/S and all DATA/source discrepancies
remain literal. Graphic-key Latin/bracket readings are visual approximations; [ versusC,
V/W run counts and encoded MSX input remain unverified. No closing quotes were invented
for4460–4490. Wavy-glyph strings and low marks at2560/2700 retain originals and markers.
Forty-three candidates,14 editorial markers,nine Unicode approximations and2,836
source-approximation space bands (including46 quoted bands) remain explicit;
forty spaces inside editorial marker descriptions are indexed separately.
All43 original/nine replacement crops preceded28 OCR tasks (9 eng/19 kor+eng);
all drafts preceded one source pass. No OCR failures/retries. Eight regions were repaired
for clipped edges; the stage paragraph needed a second top-margin revision.
Source-credit preparation metadata now uses only the printed Korean publication name.
Fresh metadata revisions add six omitted Unicode occurrences and distinguish editorial
spaces; all source text,three exports,two rebuilds and original versions remain preserved.
The initial ledger script expected a new251 lookup; it already existed from batch53.
It stopped before writes; a fresh script retains that existing observation unchanged.
All55,617 prior files and30 implementation pins pass; 56,651 files are preserved.
The unchanged213-test baseline is reused. No body pages or assembly remain pending.
Current totals: 43 readable, no partial articles, seven non-owning headings and 6 unresolved.

Batch58 completes 양계장에서 아르바이트를0056, printed249–251/PDF251–253,
at `archive/pdf/1985-02/packages/batch-58-r01`. All 98 files match the independent
rebuild; 8,700 exact UTF-8 ranges, 8,787 evidence pins and29 image decodes pass.
Five BASIC panels retain185 labels in208 physical rows,23 wraps,43 quoted strings/
86 delimiters,212 lexical statements,54 DATA fields (six decimal headers and48 hex
fields),six bitmap groups,20 direct branch fragments,12 ON targets and1,405 lexical tokens.
Two PLAY strings/58 characters,six graphic bands,eight boxed keys/three graphic-input
associations,one printed1240 reference,four listing connections,the same-page
제한시/간내에 prose continuation and34 physical prose wraps retain exact associations.
Actual final2850 RETURN and following 복덕방 on254 establish the complete ending.
Missing2500,split THEN/100/32,G assignment,RETURN1720,PLAY0/O/6,DATA fields and
historical wording/claims remain literal. Two editorial markers preserve unknown counts
in the repetitive W-like1240 and c1280 bands. Four d-glyph rows2350–2410 retain visual
approximations with count/spacing/encoding uncertainties and original panels.
Thirty-eight source candidates,two editorial markers,seven Unicode approximations
and1,429 source-approximation space bands (including69 quoted bands) remain explicit;
six spaces inside editorial descriptions are indexed separately. Faint prose spelling
and collision consonants remain localized volunteer proofreading candidates.
All29 original/three replacement crops preceded20 OCR tasks (5 eng/15 kor+eng);
all drafts preceded one source pass. No OCR failures/retries. Three crop repairs improve
slanted listing margins and isolate1240. The first map preparation rejected unsupported
heading kind before map/crop writes; a fresh script uses section-label. Both scripts and
the failure summary remain preserved. All56,651 prior files and30 implementation pins
pass; 57,101 files are preserved. The unchanged213-test baseline is reused.
No body pages or assembly remain pending. Nine source views include three mapped pages
and six outside lookups; following258 has visible folio240, independent of TOC256.
Current totals: 44 readable, no partial articles, seven non-owning headings and 5 unresolved.

Batch59 completes 디버깅 룸0017 (source 디버깅룸), the independent lower panel
on printed243/PDF245, at `archive/pdf/1985-02/packages/batch-59-r03`.
All 45 files match the independent rebuild; 1,180 exact UTF-8 ranges,
1,220 evidence pins and12 image decodes pass. Five correction entries retain25 cells/
five headers,four printed correction pairs and the SEARCH diagram's four labels/two
blank slots. Eight Q&A rows retain94 numeric cells,two final blank cells,twelve headers
and23 grouping brackets. Row2's closing37] has no visible opening before26; no bracket
was added. CP/M format retains14 field names,27 hex fields,three ellipsis groups and
five underlined7a–7e fields. Earlier values were not invented. Four printed references,
two physical prose wraps and one caption association retain exact source links.
Sixteen candidates,seven Unicode approximations and263 unknown space bands remain.
Table pipes/semicolons/spacing are editorial serialization; subscript headers are flattened
and bracket shapes approximated,with original tables/panel preserved. Historical
corrections are transcribed here; they were not applied to other articles or issues.
All12 original crops preceded8 OCR tasks (2 eng/6 kor+eng); all drafts preceded one
source pass. No crop repairs,OCR failures or retries. Metadata revisions remove stray
draft-note fragments and use the actual printed caption. The OCR-bound map's exclusion
note incorrectly called LOGATOR canonical0050/already restored; active correction
metadata identifies it as an independent unlisted contest. Canonical0050 remains MAT 함수.
No source/OCR inputs changed. The first verifier omitted the caption's final newline
from its expectation; a fresh verifier checks the complete range. All three exports,
two rebuilds,original notes and failed/passed verifiers/validations remain preserved.
All57,101 prior files and30 implementation pins pass; 57,456 files are preserved.
The unchanged213-test baseline is reused. No body pages or assembly remain pending.
The shared-page observation now distinguishes selected0054 upper-left dump,selected0017
lower errata and unlisted upper-right LOGATOR; the previous observation is preserved.
Current totals: 45 readable, no partial articles, seven non-owning headings and 4 unresolved.

Batch60 completes 복덕방0018, printed252–255/PDF254–257, and 광고색인0024,
the lower panel of PDF258 with visible folio240 and canonical TOC256 unchanged.
Selected packages are `archive/pdf/1985-02/packages/batch-60-r01/classifieds` and
`archive/pdf/1985-02/packages/batch-60-r01/advertising-index`. All101 classifieds files
and25 index files match their independent rebuilds. Classifieds pass4,993 exact UTF-8
ranges,5,072 evidence pins and27 image decodes; the index passes508 ranges,550 pins
andfive image decodes. No body pages or assembly remain pending.

Classifieds retain83 bullet items (5 원함,32 바꾸기,46 물려주기),77 contact rows/
76 printed contact groups,79 phone fields,69 money expressions and15 location fields.
All254 physical rows,nine column/page connections andfour continuing items remain
source-linked. Three large photographic labels are transcribed. One apple-logo marker,
38 candidates,211 Unicode approximations and742 source-approximation space bands
plus one editorial-description space remain explicit. Stylized monitor /// versus III
and tiny photographic object-label transcription remain pending volunteers. Final contact
민 경 윤 corrects provisional map 민정훈 in active metadata; the OCR-bound map remains
unchanged. Printed product spellings,split model names,prices,phone numbers and source
claims remain literal; no current offers or contact validity were inferred.

The index retains24 rows/48 cells in two ordered columns without invented headers,
26 printed reference tokens (three cover references),24 leader-dot bands,original tree,
rules and240 folio. The independent upper 컴퓨터비전 advertisement is excluded.
Eight candidates,two source-space bands,24 editorial pipes and48 separator spaces
remain explicit. Printed 고려씨스템산업,벨엘상사 and이행전기 remain source candidates;
leader-dot counts and reference targets are unverified. No catalog correction.

All32 original/three replacement crops preceded26 kor+eng tasks; all drafts preceded
one source pass. No OCR failures/retries. Crop repairs recover the monitor label,final
오승택 contact row and outgoing 흑백 continuation. Index drafts omitted most rows;
all24 were recovered directly from the source without another OCR attempt.
All57,456 prior files and30 implementation pins pass; 58,006 files are preserved.
The unchanged213-test baseline is reused. Two canonical tasks,five mapped pages andtwo
outside lookups stay within the limits; six reused source views andone new259 view.
Current totals: 47 readable, no partial articles, seven non-owning headings and 2 unresolved.

Batch61 completes 컴퓨돌이0025 at `archive/pdf/1985-02/packages/batch-61-r01`.
Its two independent complete vignettes are 언제쯤 below BEEP on printed36/PDF38
and 해답 in the upper-right of Forth's ending on printed63/PDF65. Intervening technical
article pages remain outside this canonical comic's ownership. All44 files match the
independent rebuild;291 exact UTF-8 ranges,332 evidence pins and12 image decodes pass.
Eight blocks/four original art/panel figures retain22 physical rows (16 story rows),
eight quoted passages/three wrapped quotes,two art/text associations,two10년 hat labels,
three1/2/10-year duration fields and100/0-point score fields. No byline,artist or signature
was inferred. Literal 늘리지요,학생같으면,걸릴겁니다 and0점임 remain unchanged.
Sixteen candidates,21 Unicode approximations and59 unknown space bands retain stylized
logos,curly quotes,ellipsis and slanted exclamations. Active metadata corrects the
provisional map's final question mark to the source exclamation; OCR inputs remain exact.
All12 original/two hat-label replacements preceded8 kor+eng tasks; all drafts preceded
one source pass. No OCR failures/retries. The first map validation rejected2–3 pixels
of overlap between technical exclusions and comic borders before map/crop writes;
a fresh script narrowed the exclusions. Original script/failure summary remain.
All58,006 prior files and30 implementation pins pass; 58,228 files are preserved.
The unchanged213-test baseline is reused. No body pages or assembly remain pending.
Shared-page observations retain the prior records and separate restored comic/technical
owners on38/65. One canonical task,two mapped pages,five outside lookups; seven reused
full source views,no new render. All canonical article bodies are now readable/sample-reviewed.
Current totals: 48 readable, no partial articles, seven non-owning headings and 1 unresolved.

Next: resolve parent 정보모음0008 as heading-classification62.
Check its pageless canonical entry and every unchanged child link against selected
source/package evidence. Determine organizational/body ownership without inventing
another body,divider or hierarchy; audit all56 identities and classifications before
issue closeout. No new OCR is needed unless actual body evidence requires mapping.
Cover selection,full260-page accounting,standalone issue export/rebuild/report and
requirements audit remain pending. Human acceptance,full proofreading,source bytes,
spacing,stylized glyph encoding,historical claims and independent backup recovery
remain unverified. No reader rebuild.

## December 1984 closeout, 2026-10-20

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
December restoration checkpoint is queued. Nine supplied eligible issues remain;
February 1985 is next, and no next-issue work has started. No --preview or
reader/browser/frontend rebuild was performed.

See the [December record](docs/progress/8412.md) and
[ledger](metadata/catalog/pdf-restoration/1984-12-progress.json). No reader rebuild.

## October 1984 closeout, 2026-10-19

October 1984 is complete under the canonical TOC JSON/assets scope: 35 readable,
assistant sample-reviewed articles and six non-owning headings account for all 41
entries, with no partial articles or unresolved eligibility. All 260 PDF pages are
classified: 205 contain selected article bodies and 55 are other material, including
18 pages of two unlisted features. The verified cover, selected packages and
independent byte-identical issue rebuild pass; all 30,737 prior evidence files remain
unchanged. The standalone index is `archive/pdf/1984-10/reference/issue.json`;
the report is `archive/pdf/1984-10/evidence/issue-closeout/report.json`.
Human acceptance/full proofreading, source bytes and execution remain unverified;
news/classified body transcription and the batch 35 preflight timing exception remain
explicit. No reading-room rebuild. December 1984 is also complete;
nine supplied eligible issues remain, and no next-issue work has started.

See the [October record](docs/progress/8410.md) and [versioned ledger](metadata/catalog/pdf-restoration/1984-10-progress.json).
Unlisted DOS TOOL KIT41–43 and 통합 소프트웨어241–255 remain outside the canonical article set.

## September 1984 closeout, 2026-10-16

September is complete under the canonical-TOC JSON/assets scope: all 43 TOC
entries are accounted as 37 readable, assistant sample-reviewed articles and
six non-owning headings. The standalone index is
`archive/pdf/1984-09/reference/issue.json`; the report is
`archive/pdf/1984-09/evidence/14-1984-09-closeout/report.json`. All 268 PDF pages are
classified in `archive/pdf/1984-09/restoration/14-1984-09-closeout/source-page-ledger.json`:
226 have selected article bodies and 42 are other material, including the
separate unlisted four-page SPC-1000 joystick article. One source page is shared
by two disjoint articles. The 37 selected packages, verified cover, complete
issue and independent byte-identical rebuild pass. Information-radar story
headings are searchable, with complete news bodies in original images awaiting
volunteer transcription. Human acceptance/full proofreading, source bytes and
program execution remain unverified. October 1984 is next. No reading-room
rebuild occurred.

## August 1984 closeout, 2026-10-14

August is complete under the JSON/assets scope:37 readable, assistant
sample-reviewed articles and six non-owning headings account for all43 canonical
TOC entries. No partial bodies or unresolved eligibility remain. The standalone
index is `build/pdf-restoration/13-1984-08-reference/issue.json`; the report is
`build/pdf-restoration/13-1984-08-closeout/report.json`. All selected packages and
the complete issue reproduce exactly. Seven review-range links are corrected in
separate metadata revisions; original source readings, OCR, assets and packages
remain unchanged. Human acceptance/full proofreading, source bytes and program
execution remain unverified. September 1984 is now in progress; see
[its checkpoint log](docs/progress/8409.md). No reading-room rebuild.
See the current [progress record](PROGRESS-PDF.md) and [OCR plan](PLAN-OCR.md).

## Scope and historical May 1984 closeout

**Scope clarified 2026-10-02:** this plan converts eligible PDF content into
structured JSON and extracted image assets. Deliver article/issue identities,
ordered text/code/caption blocks, figures and covers, source/region provenance,
immutable raw OCR, `corrections.json`, and explicit availability/review outcomes.
Text/listing files may accompany the JSON for correction and reuse.

HTML previews, human-readable publication, reading-room adapters/integration,
browser/Playwright checks, frontend builds/tests, and reader installation belong
to a separate rendering task. They are not prerequisites at any checkpoint,
including issue closeout and final campaign completion. PDF page rasterization
and cropping for OCR, scan review, and image extraction remain in scope.

November 1983, February 1984, March 1984 and May 1984 are complete.
April has no supplied PDF, as confirmed by the owner. March retains one terminal
partial due to absent printed pages 250–251; all available content is restored.
March's completed package and report remain unchanged.

**May 1984 is complete under the JSON/assets scope.** All 42 canonical TOC
entries are accounted: 36 readable, sample-reviewed articles and six non-owning
headings. There are no partial, failed, image-only or unresolved outcomes, no
deferred source pages and no pending assemblies. Canonical IDs, titles and parents
are unchanged. Full proofreading, source encoded bytes and historical program
execution remain unverified; original errors and uncertain glyphs are preserved.

The standalone issue index is `build/pdf-restoration/12-1984-05-reference/issue.json`;
the report is `build/pdf-restoration/12-1984-05-closeout/report.json`. They cover
217 source pages, 1,964 regions, 1,353 blocks, 403 figures and 5,978 physical listing rows.
All 7,334 original article files are copied exactly.
The issue package has 7,340 files totaling 1,558,818,169 bytes. Canonical
accounting, source/page geometry, package/assets, correction evidence and an
independent byte-identical issue rebuild pass. The verified source cover and its
provenance accompany the report; the canonical thumbnail is retained in the issue.

Forty-three native checkpoints and seventeen assemblies preserve 42 immutable
May inputs. All 200 native/36 assembly manifests and prior OCR/unpromoted evidence
inventories remain unchanged. The separately committed radar news adapter `f8fa518`
passes 117 PDF tests; the closeout reuses that unchanged baseline. No new OCR,
HTML, frontend, browser or reader work was required. At that closeout, June 1984
was next and fifteen supplied eligible issues remained after May. These are
historical counts; use [PLAN-OCR.md](PLAN-OCR.md) for subsequent progress.

Evidence: `private/pdf-restoration/12-1984-05-closeout/validation.json` and
`completion-audit.json`. The pre-export cover-root validation failure is retained;
the corrected installed-cover path passes without changing any asset.

The checkpoint records below are historical evidence; the completion above
supersedes their earlier next-step and aggregate status statements.

The appendix source-candidate adapter is validated before full assembly. New opt-in
`wrapped-source-reference-v1` projects the natives' independent choice candidates
and explicit printed answer pairs without rewriting their verification fields.
115 PDF tests pass, including source-range/prose-join and false verification checks.
The real 20-page projection preserves 468 inline examples/160 answers, 58 listing
groups and all original metadata. All 197 native/34 historical assembly pins and
preserved unpromoted/OCR evidence inventories pass; the ledger is unchanged.
Tooling was committed separately as `bdf0d8c` before the full appendix export.
Evidence: `private/pdf-restoration/12-1984-05-appendix-source-adapter`.

Full appendix 230–249 assembly is complete after native41 `0db83cb` and separately
tested tooling `bdf0d8c`. Four immutable natives retain 313 regions, 196 combined
blocks, 107 original images, 206 regional spans and 456 text reviews. All four
printed answer keys retain 160 pairs; 468 inline examples, 89 Unicode candidates
and 66 table rows/460 cells/59 blanks are preserved. 436 physical listing rows
retain 421 numbered entries, three wraps and 12 unnumbered rows in 58 groups.
Middle12 merges its group across235/236 with fresh rows; adult30 prompt/choices
join with an explicit paragraph boundary. Nine native prose joins and all original
metadata remain unchanged. Independent full rebuild, exact indexes and197native/
34priorassembly pins pass; two unpromoted exports and40–41 OCR inventories retained.
115-test baseline reused. Full proofreading, source bytes and execution unverified.
Remaining after this assembly: radar restoration/classification and separate
issue closeout, advanced by native42 below. No new mapping/OCR, HTML or browser
work was required for the appendix assembly.
Export: `build/pdf-restoration/12-1984-05-appendix`.
Evidence: `private/pdf-restoration/12-1984-05-appendix-assemble`.

Native42 restores information radar89–94 of full source-verified89–96. All15fresh
88–99/249–251 scans and the contents image were reviewed before mapping; one
article/six mapped pages/nine outside-map lookups. 67 regions retain55 blocks,
six original images,61 regional spans,101 text reviews,29 Unicode candidates,
13 news items, two captions and six native prose boundaries. The award table
retains13 rows/65 cells/seven blank merged-label continuations. Printed DESING,
Compaq5½-inch claims, Insructions/dottleneck/VSLI/Fourrier and model/body
discrepancies remain literal candidates. All73 original/seven revised panels and
six images were viewed; four distinct crops widened once.71 actual OCR tasks,
zero failures/retries. Independent indexes/projections and byte-identical rebuild
pass;197 prior native/35 assembly pins and preserved evidence inventories unchanged.
Unchanged115-test baseline reused. Source bytes/full proofreading remain unverified.
Pageless information group0034 is classified non-owning from the source contents
and eight canonical children. Native43: restore radar95–96 and lower advertising
index250, excluding the upper publisher ad; then commit the ending and assemble
the full radar89–96. Separate whole-issue closeout remains required.
Export: `build/pdf-restoration/12-1984-05-batch-42/radar`.
Evidence: `private/pdf-restoration/12-1984-05-batch-42`.

Native43 completes radar95–96 and lower advertisingindex250 after native42
commit31355dd. Exact pinned15wholeviews/fullsourceextent were reused;95/96/250
were actually reinspected before mapping. Two articles/three mapped pages/12
outside-map lookups.28 regions retain23 blocks/two original images,26 regional
spans/52 text reviews and32 Unicode candidates. Six ending news reports preserve
three prose boundaries;30 advertiser entries retain60 cells in two source columns.
Coverreferences표2/표3/표4 and source spelling/unit/model/price discrepancies remain
literal candidates. Upper publisher ad250 excluded. All33 original panels/two
images viewed;28 actual tasks,zero failures/retries/repairs. Independent indexes,
projections and byte-identical rebuilds pass;198 prior native/35 assembly pins and
all preserved evidence inventories unchanged. Unchanged115-test baseline reused.
All42TOC identities now classified:36 articles/6groups;35readable/onepartialradar.
Next: separate fullradar89–96assembly from exact native42/43 pins, resolving only
extent/assembly scope notes; then wholeMay standaloneJSON/assets closeout and
requirements audit. No new mapping/OCR is needed for those remaining checkpoints.
Exports: `build/pdf-restoration/12-1984-05-batch-43/{radar,ads}`.
Evidence: `private/pdf-restoration/12-1984-05-batch-43`.

Accounting opening148–153 (native22) and ending154 (native23) retain52 regions,
41 ordered blocks,seven original images,45 native regional spans,41 source block
ranges and123 text review ranges. SectionsA–Z form one continuous PET/CBM BASIC
program:293 physical/numbered rows in29 codeblocks. Four native prose boundaries
retain 다음으로, 만일 누계까지, 대변합계 and 계정을. No crosssegment prose or
physical-row join is needed;1720 is followed by1730. Final2540RETURN andREADY154
precede non-owningdivider155 and next terminal article156.

Faint digits/variables/operators, PET graphics/run lengths, quoted spacing and
Hangul glyph sequences remain explicitly uncertain. Composed Korean candidates
inside markers are editorial reading aids;original bitmaps are authoritative.
Literal syntax/nonmonotonic2040/2030 and2541/2542/2530 labels,duplicate2582,
GOSIB2080,PRINT(Y1/100),THEN2229 and earlier malformed statements remain unchanged.
Row30B70/IFDC,row119D1/C1 andI5/I6 candidates need manual proofreading. No source
encoded-byte or execution certification;full proofreading remains deferred.

Native22 reviewednine148–156 lookups/six mapped pages;native23 reviewedfour
153–156 lookups/one mapped page. Both use three outside-map lookups. Native22
had54 executedtasks43 initial/11 repairs;native23 had13tasks9 initial/four repairs.
Each distinct region repaired once,zero failures/no OCR retry. All initial/revised
inspection panels,seven original images and supplementary source zooms reviewed.
Original maps/crops/raw OCR,positions/settings and attempts preserved.

Full assembly follows named native ending checkpoint0ef490d. All205 original
files are byte-identical;exact full rebuild, UTF-8 ranges and physical/logical
listing indexes pass. All175 prior native/30 assembly pins unchanged. Passing
unchanged100-test baseline reused. No new mapping,rendering,OCR,pipeline change,
HTML,frontend or browser work.

Terminal opening156–161 (native24) of verified156–180 retains58 regions,35
ordered blocks,11 original images,47 regional spans,85 text reviews andten
sourcecaption spans. Three independent unnumbered assembly listings retain52
physical rows;BDOS table retains39 rows/four cells,includingduplicate6/32.
Six prose groups preserve12 native boundaries. Eleven distinctregions repaired
once each;69 executedtasks58initial/11repair,zero failures/no OCRretry. All54
initial/11 revisedtextpanels,11 originalimages andone reviseddiagram reviewed.
Exact rebuild,UTF-8/table/listing indexes and175priornative/31assembly pins pass.
Unchanged100-test baseline reused. Literal asynchrnous,Receiver Transmission,
Equipemnt,wboote,ccp+806h andCALLBDOS hyphen retained;smallglyphs/bytes/execution
remain uncertain. Fullproofreading deferred. Remaining162–180 andfullassembly
required;wholeMay incomplete. Evidence:`private/pdf-restoration/12-1984-05-batch-24`.

Terminal middle162–167 (native25) retains51 regions,31 blocks,15 original images,
36 regional spans,67 text review ranges and15 caption spans. Six tables preserve
83 data rows/396 cells, including blank cells; three independent unnumbered
assembly listings preserve68 physical rows27/28/13 and zero numbered logical
entries. Four prose groups preserve five native boundaries. All48 initial/two
revised text panels,15 original images and two revised images reviewed. Three
distinct regions repaired once;54 tasks51 initial/three repair, zero failures or
OCR retries. Literal Received Date, Repuest, Trming, From DEC, boud, GS and printed
address discrepancies retained. Listing4's PC-3001 reading has unresolved3/8
ambiguity. Source bytes/execution unverified; full proofreading deferred.
Exact rebuild and all UTF-8/table/caption/listing indexes pass;176 prior native
and31 assembly pins unchanged. Passing unchanged100-test baseline reused. Both
terminal natives remain immutable; remaining168–180 and full assembly required.
Evidence: `private/pdf-restoration/12-1984-05-batch-25`.

Terminal middle168–173 (native26) retains59 regions,40 blocks,17 original images,
42 regional spans,67 text review ranges,16 source captions and two figure notes.
Six tables preserve45 data rows/100 cells; six independent assembly groups retain
132 unnumbered physical rows19/28/13/38/21/13. Two prose boundaries retain
루틴에서 and 에러가. Three address/formula examples are indexed. All52 initial/
nine revised text panels,17 original images and three revised images reviewed.
Ten distinct regions repaired once;69 tasks59 initial/ten repair, zero failures
or retries. Duplicate printed figure14/16 numbers, acept and GS-MIGHT header
retained; small glyphs/source bytes/execution unverified. Full proofreading deferred.
Exact rebuild and all text/cell/row/caption/listing indexes pass;177 prior native/
31 assembly pins unchanged. Unchanged100-test baseline reused. Terminal156–173
is available in three immutable natives;174–180 and separate assembly remain.
Evidence: `private/pdf-restoration/12-1984-05-batch-26`.

Terminal native27 pages174–179 is complete:20 regions,12 ordered blocks,
8 original images,12 regional spans,19 text review ranges,4 source captions,
2 command examples and1 figure note. Three unnumbered listing groups retain
241 physical rows:20 editor-screen rows,133 complete transmit-program rows and
88 receive-program rows continuing180. All29 original/5 revised text panels and
8 original images reviewed. One crop repaired once;21 tasks with zero failures
or OCR retries. Source COBY, figure20 reference, OR E, 8H+1H(129)BYTES and SEND R
comment beside G operand retained. Figure18 includes a narrow incidental screen
strip; complete flowchart and screen preserved separately. A first validation
attempt exposed per-group physical ordinals; its export remains saved, and
per-block ordinals now pass wrapped-index projection. No pipeline change.
Exact rebuild and all UTF-8/caption/row indexes pass;178 prior native/31 assembly
pins unchanged,100-test baseline reused. Four immutable terminal natives cover
156–179; native180 and separate full156–180 assembly remain. Full proofreading,
source encoding and execution remain unverified.
Evidence: `private/pdf-restoration/12-1984-05-batch-27`.

Terminal native28 ending180 is complete:3 regions,2 blocks,1 listing image,
2 regional spans,3 text review ranges,50 unnumbered physical rows and1 source
caption. All5 text panels and original image reviewed;3 tasks, zero failures,
no crop repairs or OCR retries. END RECEIVE and printed caption period retained.
Prior179/180 listing continues on a fresh physical row; no row join required.
Exact rebuild and all UTF-8/row/caption indexes pass;179 prior native/31 assembly
pins unchanged,100-test baseline reused. Five immutable segments now cover all
156–180; separate full assembly remains. Source bytes/execution and full
proofreading unverified. Evidence:`private/pdf-restoration/12-1984-05-batch-28`.

Terminal table adapter is validated separately before full assembly. New opt-in
`regional-table-listing-v1` permits explicitly indexed tab-separated table blocks
between continued prose. Exact row bytes, source scan identities, consecutive
row numbering, blank cells and complete table coverage are checked; prior modes
remain unchanged. The actual five-segment sample preserves191 regions,118 final
blocks,52 images,139 regional spans,241 review ranges and543 physical rows.
Two joins cross exactly11 reviewed objects. Original table indexes remain in
native metadata. All180 native/31 assembly pins and12 prior May assemblies pass;
103 PDF tests pass. No full assembly or new extraction in this tooling checkpoint.
Evidence: `private/pdf-restoration/12-1984-05-terminal-table-adapter`.

Terminal full156–180 assembly is complete after native ending17c02f2 and
separate table-adapterba2a2fc. It retains191 regions,118 ordered blocks,52 original
images,139 regional spans,120 source block ranges,241 review ranges,46 captions
and543 unnumbered physical listing rows. Fourteen assembly listings plus editor
screen form15 groups;receive listing14 spans178–180 with138 rows. Nineteen native
prose boundaries and two crosssegment joins across11 explicit objects preserved.
Searchable tables retain167 data rows/652 cells;native indexes are unchanged.
All653 original files are byte-identical, exact UTF-8/row indexes and independent
full rebuild pass. All180 prior native/31 assembly pins remain;103-test baseline
reused. A validation assertion initially expected one space in END RECEIVE;
it now checks the original five-space alignment. No output/source change.
Five scope gaps resolved;literal errors,glyph/encoding/execution uncertainty and
full-proofreading deferral remain explicit. No new mapping/rendering/OCR,HTML,
frontend or browser work. Evidence:`private/pdf-restoration/12-1984-05-terminal-assemble`.

Workshop native29 restores the complete lightpen article181–183:34 regions,
20 ordered blocks,seven construction diagrams/two listing panels,25 regional
spans,41 text review ranges,eight captions andseven indexed materials. Two
independent BASIC programs retain16 numbered physical/logical rows (4/12).
Five native prose boundaries preserve 응용기기,연결의 의미,연결부가 and+5V 전원이.
Quotedspacecounts,I/1/PBO/OV glyphs,sourceclaims andexecution remain unverified;
sourcePRINT juxtaposition andliteral 트라이겜/뚫려진 wording retained.
All26 original/one revised text panels,nine original/one revised images reviewed.
Two distinct crops repaired once;36tasks34initial/2repair,zero failures/retries.
Exact UTF-8/caption/material/listing indexes,wrapped projection andindependent
rebuild pass. All180 prior native/32 assembly pins preserved;13 May assemblies
revalidated. Passing103-test baseline reused. No pipeline/HTML/frontend/browser
changes. Source maps/crops/rawOCR/positions/settings/attempts remain pinned.
Evidence:`private/pdf-restoration/12-1984-05-batch-29`.

Native30 restores complete Apple 쾌속 DOS184–187 and 복덕방188:61 regions,
45 ordered blocks, four original images,57 regional spans,101 text review ranges
and two source captions. Seven prose groups preserve12 native boundaries.
Two independent unnumbered listings retain18 physical rows (16/2), with252
hex-token candidates. Sector table retains16 data rows/32 cells; classifieds
retain15 notices (two exchange, twelve sale, one wanted). Printed D9/I mismatch,
BAGIC-G,15만원 and the reinitialization instruction remain literal. Hex glyphs,
annotation alignment, prices/contacts, source bytes and execution remain unverified.
All71 original/37 revised text panels and four original images reviewed. Twenty-four
crops widened once;85 tasks61initial/24repair, zero failures or OCR retries.
Exact UTF-8/table/notice/hex/listing/caption indexes, wrapped projection and
independent rebuilds pass. All181 prior native/32 assembly pins preserved;
13 May assemblies revalidated and unchanged103-test baseline reused. Original
maps/crops/raw OCR/positions/settings/attempts retained. Full proofreading deferred.
Evidence: `private/pdf-restoration/12-1984-05-batch-30`.

Native31 completes 공모 총평 on pages 190–191 and restores the opening of
길 잃은 고양이 on pages 192–195, within its verified 192–197 extent. The two
packages retain 44 regions, 32 ordered blocks, eight original images, 36 regional
spans, 62 text review ranges and five captions. Four prose boundaries preserve
PONPOKO and 다양한; the printed wrapping hyphen before NPOKO is explicitly removed.
The winners table has eight data rows/48 cells; the direction table has four
rows/12 cells. The cat article has 23 program-guide rows and 13 variable definitions.
Its one continuous AppleSoft listing retains 129 physical rows: 85 numbered entries,
43 wraps and one ]LIST prompt. Line120 repeats destination170; only one line170
label is present. Quoted artwork, small glyphs and source bytes remain provisional;
printed wording and duplicate flowchart3240 are preserved. No code execution.

Fifteen fresh whole scans189–203 establish boundaries before mapping: six mapped
pages and nine outside-map lookups. All50 original/seven revised text panels and
eight original images reviewed. Three crops widened once;47 tasks44initial/3repair,
zero failures/retries. Exact UTF-8/table/cell/guide/variable/caption/listing indexes,
wrapped projection and independent byte-identical rebuilds pass. All183 prior
native/32 assembly pins unchanged;13 May assemblies revalidated. Passing unchanged
103-test baseline reused. Original maps/crops/raw OCR and provenance retained.
Full proofreading deferred. Cat196–197 is deferred, not missing; an ending native
checkpoint and separate assembly are required. Evidence:
`private/pdf-restoration/12-1984-05-batch-31`.

Native32 completes the cat ending196–197 and the function-key article198–201.
It retains60 regions,43 ordered blocks,12 original images,48 regional spans,
107 text review ranges,four captions andfive native prose boundaries.
Cat:286 physical rows,146 numbered entries,140 wraps;59 DATA statements retain
881 literal values. Line3080 crosses columns on196;197starts5130. These fresh
source readings supersede the native31 resume note's5080/5150 candidates;
historical native31 maps,metadata and saved notes remain unchanged.
Functionkeys:four independent groups,173 physical rows,three numbered entries,
170 unnumbered rows;1,308 hex-token candidates include1,280monitor readings.
Its default table has10rows/20cells includingblankKEY08;programguide has eight
address descriptions. LiteralFUNTION,FB69,0번/키이1 andsourcefigure references
remain unchanged; Unicode control/arrow markers do not certify source bytes.

Thirteen fresh191–203 scans were reviewed beforemapping,withsixmappedpages/seven
outside-maplookups. All72 original/50 revised text panels and12 original/seven
revised figures reviewed. Thirty-eight crops widened once;98tasks60initial/38repair,
zero failures/retries. Exactindexes,wrappedprojection and byte-identical rebuilds
pass;185 priornative/32assemblypins preserved and13Mayassemblies revalidated.
The unchanged103-test baseline is reused. Fullproofreading andcodeexecution remain
deferred. No pipeline,HTML,frontend orbrowser changes.
Evidence: `private/pdf-restoration/12-1984-05-batch-32`.

Native32ending iscommitted asd15789d. Separateopt-in referenceindex tooling
checkpoint passes106PDFtests,realcatprojection/byte-identicalsample rebuild and
all32historicalassemblychecks;187nativepins unchanged. It projects searchable
tablecells,programguide,variables andprompt into combinedUTF-8 ranges. Wholecat
assembly follows this namedtoolingcommit;sample doesnotpromoteledgeravailability.
Evidence: `private/pdf-restoration/12-1984-05-cat-reference-adapter`.

The full cat article on pages 192–197 is now readable/sample-reviewed. Its two
immutable segments retain 41 regions, 30 ordered blocks, 11 images, four captions,
30 regional spans and 47 text reviews. One AppleSoft program retains 415 physical
rows: 231 numbered entries, 183 wraps and one ]LIST prompt. Fifty-nine DATA
statements retain 881 literal values. Four direction-table rows/12 cells,
23 program-guide explanations and 13 variables have exact combined UTF-8 indexes.
No prose or physical-row join is needed between segments; 1090→1100 and 5120→5130
remain separate rows. Line 3080's column wrap on page 196 is retained.
Original files/metadata and 187 prior native/32 assembly pins are preserved;
the byte-identical rebuild and 106-test baseline pass. No new mapping, OCR, HTML
or browser work. Full proofreading, quoted artwork, source bytes and execution
remain unverified.
Full export: `build/pdf-restoration/12-1984-05-cat`.
Evidence: `private/pdf-restoration/12-1984-05-cat-assemble`.

Native33 restores the complete 너구리 article202–207: 47 regions,33 blocks,
11 original images,three captions,36 regional spans and156 text reviews.
Its CGBASIC listing has261 physical rows,172 numbered entries and89 wraps;
line880 crosses205/206. Independent hex data has124 rows/1,488 byte-value
candidates,plus16 save-example tokens. The direction table hasfive data rows
and a header/12 cells;12 guide rows,10 variable rows andseven commands are indexed.
Ninety-nine editorial graphic markers retain source references without inferring
original character bytes or run lengths. Printed errors and the prose2000-byte
claim remain unchanged;full proofreading andexecution are unverified.

Nine fresh201–209 scans proved the extent before mapping; six mapped pages and
three outside-map lookups. All54 original/five repaired text panels and11 images
were reviewed. Three distinct crops repaired once;50 tasks,zero failures/retries.
Exact indexes,wrapped projection andbyte-identical rebuild pass. All187 prior
native/33 assembly pins remain unchanged;14 May assemblies revalidate andthe
unchanged106-test baseline is reused. No pipeline or rendering changes.
Export: `build/pdf-restoration/12-1984-05-batch-33/raccoon`.
Evidence: `private/pdf-restoration/12-1984-05-batch-33`.

Native34 restores HAPPY-WORDS opening208–213 afterfresh full208–215 extent proof.
It retains55 regions,40 blocks,12 images,three captions,43 regional spans and76
text reviews. Complete LIST1 has410 physical rows/284 numbered entries/126 wraps;
1140 and2180 cross columns. Five keyboard-table rows/10 cells,54 guide fragments,
19 variable fragments andfive commands haveexact UTF-8 indexes. Music1900/1910
retains124 integer candidates;damaged1920/1930 and203 word candidates versus
printed200 claim remain explicit. Four editorial markers donot certify bytes.

Eleven fresh207–217 scans reviewed beforemapping;six mapped pages/five lookups.
All70 original/41 revised text panels and12 original/one revised image reviewed.
Nineteen crops repaired once;74 actual tasks,zero failures/retries. Exact indexes,
wrapped/reference projection andbyte-identical rebuild pass;188 priornative/33
assembly pins unchanged;14 May assemblies revalidated. Unchanged106-test baseline
reused. Native34 ispartial;ending214–215 andseparate assembly remain required.
Full proofreading,source glyphs/bytes andexecution unverified. JSON/assets only.
Export: `build/pdf-restoration/12-1984-05-batch-34/happy`.
Evidence: `private/pdf-restoration/12-1984-05-batch-34`.

Native35 completes HAPPY-WORDS ending 214–215 and 메아리 216–217: 22 regions,
14 ordered blocks, seven original images, 15 regional spans and 24 text reviews.
HAPPY LIST2/3 retain 128 unnumbered physical rows: two monitor prompts, 126 address
rows and 1,000 hex-token candidates (19 monitor, 981 shape-table). The complete
flowchart is preserved. 메아리's printed May patch retains 141 physical rows,
78 numbered entries and 63 wraps; 1110 and 1180 REM cross columns. Eight DATA
statements retain 228 integer candidates. The split headline retains both sources.
The original April program is not supplied or invented.

Nine fresh 213–221 scans established both extents before mapping; four mapped
pages and five outside-map lookups. All 28 original/three revised text panels,
seven images and one supplemental token inspection reviewed. One crop repaired
once; 23 actual tasks, zero failures/retries. Enlarged first label 5, hex 61B8's
final 52 and 63D0's 0D supersede preliminary readings; initial evidence retained.
Printed FILL NAME, RECODER, colon-only rows 1194–1196 and punctuation candidates
remain literal. Full proofreading, quoted spaces, source bytes and execution
remain unverified. Exact indexes, wrapped/reference/prompt projection and identical
rebuilds pass; all 189 prior native/33 assembly pins retained, 14 May assemblies
revalidated. Unchanged 106-test baseline reused. No pipeline or rendering changes.
Exports: `build/pdf-restoration/12-1984-05-batch-35/{happy,echo}`.
Evidence: `private/pdf-restoration/12-1984-05-batch-35`.

Native36 completes canonical 리뷰쌀롱220–224, including 카나리아II, DCM12-SL
and TM-103: 34 regions, 17 text blocks, five original images, one caption,
29 regional spans and 62 text review ranges. Three continuous prose groups retain
12 column/page boundaries. The specifications table has eight rows/16 cells,
including the explicit blank under its merged broadcast-frequency label.
Printed 알함브라/알함부라, 카나리아II/2, 칼러/컬러, model-name variants,
여유자작한, 농촌도 가도 and C-/ATALOG wrap remain literal. Historical technical
claims are not repaired; full proofreading and source encoded bytes unverified.
Twelve fresh219–230 scans proved extent before mapping: five mapped pages/seven
outside-map lookups. All38 original/six revised text panels and five images
reviewed. Three crops repaired once each;37 actual tasks, zero failures/retries.
Exact UTF-8/regional/table/cell/caption indexes, regional/reference projection and
identical rebuild pass;191 prior native/34 assembly pins preserved,15 May
assemblies revalidated. Unchanged112-test baseline reused. JSON/assets only.
Export: `build/pdf-restoration/12-1984-05-batch-36/review`.
Evidence: `private/pdf-restoration/12-1984-05-batch-36`.

Native37 completes Q&A225–229:49 regions,30 ordered blocks,12 original images,
eight captions,37 regional spans and76 text reviews. All eight question/answer
sections and seven printed listings remain. Separate list4 hex/disassembly
representations and figure1 hex table form nine literal groups.112 physical rows
retain48 numbered entries/64 unnumbered rows;45 hex rows retain166 candidates.
List6 continues170→180 across229 columns on fresh rows. List7 ends250 without
invented END/RETURN. Six prose groups retain seven native region boundaries.
Printed CGINT/CGINIT,커서나,메모리 경영,서브루틴은,28바이트 and11H alongside
11-byte prose retained. PATTERN caption has provisional8-like reading with explicit
3/8 uncertainty. Full proofreading,quoted spacing,source bytes/execution unverified.
Seven fresh224–230 scans proved complete extent before mapping:five mapped pages/
two outside-map lookups. All48 text panels/12 original images reviewed;49 actual
tasks,zero failures/retries,no crop repairs. Lower recruitment ad229 excluded by
verified crop bounds. Initial/final maps and OCR bundles remain byte-identical.
Two rejected pre-export map-bookkeeping attempts are retained in private evidence;
original map provenance was kept without new OCR or source changes.
Exact UTF-8/regional/caption/physical/logical/hex indexes,regional/reference and
wrapped listing projection and independent identical rebuild pass.192 prior native/
34 assembly pins retained;15 May assemblies revalidated. Unchanged112-test baseline
reused. JSON/assets only;no pipeline or rendering changes.
Export:`build/pdf-restoration/12-1984-05-batch-37/qa`.
Evidence:`private/pdf-restoration/12-1984-05-batch-37`.

Native38 restores the appendix opening230–235 after fresh continuous229–251
extent review proved the full230–249 article and independent neighboring content.
One article/six mapped pages/17 outside-map lookups. All60 text panels/22 original
images inspected;74 tasks,zero failures/retries,no crop repair. Initial/final maps
and OCR bundles are byte-identical.74 regions/51 blocks/52 regional spans retain
the introduction,40 elementary questions/key,middle1–11 and question12 opening.
111 physical/numbered code rows form15 independent groups; elementary question30
spans233 columns and question21 retains duplicate30/40 labels and source order.
Seven numeric DATA statements retain20 candidates; string DATA remains separately
indexed. Four answer-key rows/52 cells retain40 pairs and11 explicit blank cells.
One prose join retains middle question8 choice2's LEN/(Z$) boundary; physical
quoted-string wraps and20 circled Hangul glyph candidates retain uncertainty.
Printed C=A-C,=<,=>,missingTHEN and a provisional line60 dot remain literal.
Middle question12's new55/60 rows and choices on236 are deferred, with no physical
row join. Remaining236–249 require immutable segments and separate full assembly.
UTF-8/regional/table/blank-cell/physical/logical/DATA/glyph indexes, regional/reference
and wrapped projection and identical rebuild pass;193 prior native/34 assembly
pins unchanged,15 May assemblies revalidated. Unchanged112-test baseline reused.
An initial export with incomplete glyph metadata is preserved separately;
only the corrected `appendix-reviewed` export is promoted. Rejected bookkeeping
attempts and the refused overwrite are recorded. No source/map/OCR/tooling changes.
Export:`build/pdf-restoration/12-1984-05-batch-38/appendix-reviewed`.
Evidence:`private/pdf-restoration/12-1984-05-batch-38`.

Native exports: `build/pdf-restoration/12-1984-05-batch-{01–41}`.
Latest full export: `build/pdf-restoration/12-1984-05-appendix`.
Assembly evidence: `private/pdf-restoration/12-1984-05-appendix-assemble`.
Latest native export: `build/pdf-restoration/12-1984-05-batch-41/appendix-reviewed`.
Native evidence: `private/pdf-restoration/12-1984-05-batch-41`.
Assemblies: `build/pdf-restoration/12-1984-05-{feature,ai,fugitive,fishing,machine,logo,basictech,unix,medical,visicalc,database,accounting,terminal,cat,happy,appendix}`.
Ledger: `private/pdf-restoration/12-1984-05/issue-progress.json`.
Native35 ending is committed as `1e763f6`; its post-commit audit passes. Full
HAPPY-WORDS projection preflight reproduced a limitation of the existing adapter:
its legacy listing-marker counter rejects three retained code markers, while
the four immutable source marker records use exact regional excerpt ranges
instead of legacy glyph fields. One marker is in prose. No full export was created.

The opt-in `wrapped-literal-reference-v1` adapter now validates marker excerpts
against exact regional spans and matching unresolved records before projection.
It adds combined inline-example/hex-token/hex-row indexes without changing native
metadata or historical modes. All 112 PDF tests pass. Real HAPPY projection retains
538 physical rows, 1,000 hex candidates and four markers; repeated projection is
identical. All 191 native manifest pins and 33 historical assemblies pass their
preservation/compatibility checks. The issue ledger is unchanged. Evidence:
`private/pdf-restoration/12-1984-05-happy-reference-adapter`.
Tooling was committed separately as `89d5f4b` after native35 ending `1e763f6`.
Full HAPPY-WORDS 208–215 assembly is complete: 66 regions, 47 blocks, 16 images,
three captions, 50 regional spans and 85 text reviews. Its 538 physical rows retain
284 numbered entries, 126 wraps and 128 unnumbered rows across three listing groups.
Four markers, five inline examples, 126 hex rows/1,000 candidates, two prompts,
five table rows/10 cells, 54 guide fragments and 19 variables project exactly.
Two numeric DATA rows retain 124 candidates; 15 word-DATA rows/203 candidates remain
in original metadata. All original files/metadata and 191 native/33 prior assembly
pins are preserved. Fresh full rebuild is byte-identical. No new OCR or mapping;
112-test baseline reused. Source uncertainty and three native prose joins remain;
no physical row or prose join at 213/214. Only HAPPY availability is promoted.
Native39 restores appendix236–241, following immutable native38 opening230–235.
The ledger preserves both segments and available pages230–241; no full assembly
or readable promotion yet. Eight fresh235–242 scans and15 exact pinned native38
reviews preserve complete230–249 extent proof; six mapped pages/17 outside lookups.
All77 text panels/41 figures plus one repaired r105 crop actually reviewed.
One right-edge repair recovered both complete question22 choices.112 initial tasks
andone repair executed;111 cache hits,zero failures/retries. Initial maps/crops,
raw OCR/positions/settings and attempts preserved;111 unchanged final crops verified.
112 regions,67 blocks,71 regional spans and156 review ranges retain middle12 tail,
middle ending/key239 and high-school questions1–27/question28 prompt.148 physical/
numbered code rows form23 groups; q27,q36/37,q40 and high12 span fresh rows across
columns/pages. Five numeric DATA statements retain15 values; mixed DATA separately
indexed. Four prose joins and46 Unicode notation candidates retain uncertainty.
Middle duplicate16 labels,DIN,NEXT1I,FOR,missingTHEN,blank20/40 operands and blank
condition box stay literal. Middle forty-answer key plus truth table retain9 rows/
67 cells,11 blanks and40 separately indexed answers. Full proofreading,source
encoding and execution unverified; original bitmaps authoritative.
Exact UTF-8/regional/table/physical/logical/DATA/glyph indexes,regional/reference/
wrapped projections and independent byte-identical rebuild pass.194 prior native/
34 assembly pins plus earlier unpromoted export preserved;15 May assemblies
revalidated. Unchanged112-test baseline reused. No pipeline or rendering changes.
Export:`build/pdf-restoration/12-1984-05-batch-39/appendix`.
Evidence:`private/pdf-restoration/12-1984-05-batch-39`.
Do not rerun completed closeout or pre-promotion validator/finalizer.

Native 40 restores appendix pages 242–247, covering the high-school ending/answer
key and adult questions 1–29 plus question 30's prompt. The ledger preserves three
immutable segments covering 230–247; full assembly and readable promotion await
pages 248–249. Eight fresh 241–248 scans and 15 exact pinned native 38 reviews establish
complete 230–249 extent before mapping: one article, six mapped pages, 17 outside lookups.

The checkpoint retains 89 regions, 54 blocks, 31 original figures, 58 regional ranges
and 131 text reviews. All 67 initial text panels/31 figures and 10 revised text crops/
four revised figure crops were actually reviewed. Fourteen distinct regions were
repaired once each to recover INPUT A$, TO 20 endings, axis labels, clipped text,
question labels and the complete source caption. Initial evidence and both repair
generations remain separate; 75 unchanged final crops are byte-identical. There
were 103 actual tasks(89 initial/14 repaired), 164 cache hits and zero OCR failures/retries.

Its 136 physical program rows retain 122 numbered entries, 12 unnumbered rows and two
wrapped DATA rows across 15 independent groups. High 32's boxed 1–6 are ordinal labels,
not certified BASIC line numbers; INPUT A$ and eleven stack rows remain unnumbered.
Four prose joins, 144 inline examples, 40 printed high-school answers and 18 Unicode
notation candidates retain uncertainty. Seven tables preserve 31 rows/139 cells and
16 blanks. Source NEXT 1, duplicated 중중, 직접회로, blank operands and historical claims
remain literal; comparison-glyph, quote/spacing and geometry candidates stay uncertain.
Closer review confirms the comma after 97 in high 39 DATA; the earlier contrary
review note was withdrawn. Full proofreading, source bytes and execution are unverified.

Exact UTF-8/regional/table/cell/physical/logical/glyph indexes, regional/reference/
wrapped projections and an independent byte-identical rebuild pass. 195 prior native/
34 assembly pins plus the earlier unpromoted export are unchanged; 15 May assemblies
were revalidated. All three native 40 OCR evidence exports are inventory-pinned.
A rejected reused output path, completed-export diagnostic error and local generation-
metadata filename mix-up are recorded; authoritative exports were preserved and
metadata was recovered from their saved outcomes. The unchanged 112-test baseline
is reused; no pipeline or rendering changes.
Export:`build/pdf-restoration/12-1984-05-batch-40/appendix`.
Evidence:`private/pdf-restoration/12-1984-05-batch-40`.
Do not rerun completed closeout or pre-promotion validator/finalizer.

Native 41 restores the appendix ending on pages 248–249. All source pages
230–249 are now available across four immutable native segments; full assembly
and readable promotion remain. Four fresh 247–250 scans and 18 exact pinned prior
reviews establish complete extent before mapping: two mapped pages and 20 outside
proof pages. The advertisement below the final answer key on 249 is excluded.

This segment retains 38 regions, 25 blocks, 13 original figures, one caption,
25 regional spans and 58 text reviews. All 25 text panels and 13 figure crops
were actually reviewed. All 38 OCR tasks completed without failures, retries or
crop repairs; final map and OCR evidence are unchanged copies of the originals.
Its 41 physical program rows retain 40 numbered entries and one wrapped row across
six independent groups/eight code regions. Adult 33 and program 37(1) continue
with fresh physical rows; printed 40 wraps to THEN GOTO 99. One numeric DATA row
retains four values. No native prose or physical-row joins are needed.

The adult answer key preserves all 40 answers. Four source tables retain 22 rows,
202 cells and 21 blanks, including the ASCII table's printed omissions. Repeated
array-label rows retain explicit source roles in the corrected index. An initial
export with unsupported repeated header metadata remains separately pinned;
only `appendix-reviewed` is promoted. Text, listing bytes, maps and scans are
identical between exports. There are 73 inline examples and five Unicode notation
candidates. Blank operands, omission dots, binary choice 1000100 and historical
wording remain literal; full proofreading, encoded bytes and execution are unverified.

Exact regional/table/cell/physical/logical/DATA/glyph indexes, regional/reference/
wrapped projection and independent byte-identical rebuild pass. All 196 prior
native and 34 assembly manifest pins remain unchanged; two unpromoted native
exports and native 40/41 OCR evidence inventories are preserved. Fifteen May
assemblies were revalidated; the unchanged 112-test baseline is reused.
Export: `build/pdf-restoration/12-1984-05-batch-41/appendix-reviewed`.
Evidence: `private/pdf-restoration/12-1984-05-batch-41`.
Do not rerun completed native closeout or pre-promotion validation/finalizers.

Next: assemble the full appendix 230–249 from exact pinned native 38 reviewed,
39, 40 and 41 reviewed exports after native 41's commit/audit. Preserve all raw
files and metadata, merge the middle 12 listing across 235/236 without a row join,
and review the adult 30 prompt/choices boundary at 247/248. Validate complete
coverage, source/index projection and an independent full rebuild before readable
promotion. No new mapping/OCR is required. Information radar on 89, information-
group/advertising-index classifications and separate issue closeout remain.
Three unresolved TOC identities, one partial appendix and
separate issue closeout remain;whole May is incomplete.
Unlisted announcement189 remains excluded.
May closeout follows all remaining articles/classifications.
Stay within two-article/six-mapped-page/twenty-outside-map-lookup limits.

The following March checkpoint record preserves the completed work and its provenance.
March batches 01–44 and nineteen article assemblies are complete: the editorial on
printed13/PDF13 and full Hangul-computer feature on printed/PDF14–37 are readable,
sample-reviewed packages. The feature retains five immutable source segments,
149 regions,77 ordered blocks,22 image panels and2,033 physical listing rows.
Global correction/listing indexes, exact source copies, identical rebuild and
all85 PDF tests pass. Uncertain glyphs and proofreading limits remain explicit.
The complete 추리력 테스트 게임 on printed/PDF40–46 is assembled from two
immutable segments: 24 regions, 17 blocks, two images, 535 physical listing rows
and 42 unresolved PET graphics markers. Batch07 also restores the complete
모래시계 on47–50: 18 regions, 13 blocks, one image and 376 listing rows across
five implementations. Batch08 completes game-paddle construction on51–53
(29 regions,18 blocks,eight numbered diagrams) and the apple-counting game on54–55
(11 regions,nine blocks,one photograph,80 BASIC rows). Three prose joins and all
figure captions are source-reviewed. Batch09 completes 올 인원 (printed 홀 인 원)
on56–60:18 regions,12 blocks,two images and360 physical BASIC rows (113 numbered,
247 continuations). Two cross-boundary wraps and uncertain glyphs remain explicit.
Batch10 completes 팽이 놀이61–63:11 regions,eight blocks,one image and117 physical
listing rows. It also restores 사냥게임64–66 of verified64–69:37 regions,33 blocks,
two images and four short code groups. Both exports rebuild byte-identically;
86 earlier packages pass preservation checks. Two prose joins and source anomalies
remain documented. Batch11 completes hunting67–69 and assembles64–69 as readable:
45 regions,38 blocks,two images,195 physical listing rows across five code groups,
three prose joins and61 source-linked annotated code rows in native corrections.
The assembly preserves both original segments unchanged. Puzzle70–72 is partial:
12 regions,nine blocks,two images and67 program rows through3325;73 remains.
Native exports and the hunting assembly rebuild identically;88 earlier packages
pass preservation checks. Page39's 취미생활 is a non-owning group heading.
Batch12 completes puzzle73 and assembles70–73:13 regions,10 blocks,two images
and133 program rows. It also completes 매직 스퀘어74–76:12 regions,six blocks,
one original illustration and182 physical listing rows (86 numbered,96 wraps).
Three right-edge crops were widened once each; original/intermediate evidence
remains unchanged. Source anomalies and uncertain decorative counts remain explicit.
Fresh native/assembly rebuilds match;90 earlier packages pass preservation checks.
Batch13 completes 당신도 암산왕77–78 (14 regions,11 blocks,one illustration,
64 physical listing rows) and 불꽃 놀이79 (seven regions,five blocks,two photos,
33 physical listing rows). All21 tasks completed without repair/retry. Literal
arithmetic operators and uncertain punctuation remain explicitly flagged; both
exports rebuild identically and92 prior packages pass preservation checks.
교육입문81 is a second non-owning group heading; promotional80 is excluded.
Batch14 completes 베이직 강좌82–87:41 regions,24 blocks,five images,40 physical
conversion-listing rows and68 indexed example/output rows within prose/captions.
The searchable number-base table,eleven prose boundaries and four diagram captions
are checked. Two crop boundaries were repaired once each; source discrepancies
remain literal. Export rebuilds identically;94 prior packages pass preservation.
Batch15 completes 소프트웨어 복사 방지 기술88–91:42 regions,27 blocks,six images,
five indexed monitor commands,seven indexed bit rows and nine prose joins.
컴퓨터와 수92–93 is partial,with verified full extent92–99:18 regions,11 blocks,
two images,six indexed arithmetic rows and five prose joins. All60 tasks completed
without repair/retry; native exports rebuild identically and95 prior packages pass
preservation checks. Source discrepancies remain literal.
Batch16 completes 컴퓨터와 수94–99 and assembles92–99:107 regions,55 blocks,
36 original images and49 indexed example/table rows preserved in native corrections.
All89 tasks completed once without crop repair; eleven new column/page joins and
one cross-segment prose link are checked. Native and assembly rebuilds match;
97 prior native packages and four prior assemblies pass preservation checks.
Source mathematical errors and prose/diagram discrepancies remain literal.
Batch17 restores 마이크로 컴퓨터 시스템 입문100–105 of verified100–108:
59 regions,39 blocks,15 images,five indexed assembly examples,five prose boundaries
and nine numbered captions. One opening-photo boundary repaired once; originals
preserved. Exact rebuild and98 prior native/five assembly preservation checks pass.
Batch18 completes systems106–108 and assembles100–108:100 regions,65 blocks,
21 original images,29 physical assembly/output rows,17 indexed native examples
and15 prose boundaries. Both source segments remain immutable; captions1–15 and
source105/106 word split are checked. Tape109–111 restores49 regions,44 blocks,
four original images,
13 physical listing rows and10 indexed examples; complete extent109–112 verified.
Seven crop boundaries repaired once each. Native/assembly rebuilds match;99 earlier
native packages and five assemblies pass preservation checks.
Batch19 completes tape112 and assembles109–112:67 regions,58 blocks,seven images,
22 physical listing rows,20 indexed native examples and three prose boundaries.
Complete 자료 구조113–117 has43 regions,30 blocks,four images,137 physical Pascal/
PL-I/schematic rows in six groups,13 indexed examples,six prose boundaries and three
listing-column joins. One prose crop repaired once; historical syntax retained.
Native/assembly rebuilds match;101 prior native packages and six assemblies pass
preservation checks.
Batch20 completes 기계어 강좌118–123:41 regions,23 blocks,six original images,
23 physical listing rows across assembly/byte-dump/BASIC groups,11 indexed prose
examples and twelve prose boundaries. Two diagram edges widened once. Literal
CA/C5 discrepancy,0011 address ambiguity and BASIC apostrophe/wrap retained.
Exact rebuild and103 prior native/seven assembly preservation checks pass.
Batch21 restores 심층적 회귀분석134–139 of verified134–154:65 regions,
61 blocks,two images,101 physical listing/screen rows in eight groups,71 indexed
prose table/example rows and two prose boundaries. Tables preserve blank cells
and conflicting values; uncertain glyphs and mathematical notation remain explicit.
Two prose crop edges widened once; all original evidence retained. Exact rebuild
and104 prior native/seven assembly preservation checks pass.
Batch22 restores regression140–145:67 regions,51 blocks,eight original images,
170 physical rows in eleven code/screen groups,31 indexed table/example rows,
eight prose boundaries and six searchable plot captions. Literal source errors
and uncertain punctuation retained. Two prose crop repairs,one per region;exact
rebuild and105 prior native/seven assembly preservation checks pass.
Batch23 restores regression 146–151: 24 regions, 13 blocks, two original flowchart
panels, 558 physical listing rows in three groups, 73 indexed example/reference
rows, two prose boundaries and seven listing boundaries. One right-edge crop
repair retains HOME on line 3400. Literal errors and damaged glyphs remain explicit.
Exact rebuild and 106 prior native/seven assembly preservation checks pass.
Batch24 restores regression 152–154: seven regions, two blocks and 427 physical
listing rows. One left-edge crop repair recovers line-number digits. Full regression
134–154 is now assembled from four immutable segments: 21 pages, 163 regions,
127 blocks, 12 images and 1,256 listing rows. Exact native/assembly rebuilds and
107 prior package/seven prior assembly checks pass. A narrowly validated listing
block continuation adapter preserves the 4215/4220 boundary; all 88 PDF tests pass.
Batch25 restores VisiCalc155–160: 69 regions,39 blocks,23 original images,
18 captions,47 indexed command/key examples and seven prose boundaries. Six
regions widened once each; initial/intermediate evidence retained. Exact rebuild
and108 prior package/eight assembly checks pass; no tooling or engine changes.
Batch26 completes VisiCalc161–164 and assembles155–164 from two immutable
segments:99 regions,57 blocks,31 original images and69 indexed native command/key
examples. The ending has30 regions,18 blocks,eight images,seven captions and four
prose boundaries. Chart164 is upright after a lossless clockwise90 rotation; one
boundary repair recovers its leftmost labels. Exact native/assembly rebuilds and
109 prior package/eight prior assembly checks pass. No tooling or engine changes.
Batch27 restores 서북편란법165–170 of verified165–173:44 regions,28 blocks,
10 images,eight captions,five searchable tables,70 indexed example/reference rows,
69 physical BASIC rows and six prose boundaries. Eleven drawn-grid rows use explicit
source-linked unresolved markers. Two prose crop edges widened once; original
scans retained. Exact rebuild and110 prior package/nine assembly checks pass.
Batch28 completes northwest171–173 and assembles165–173:47 regions,29 blocks,
10 original images and275 physical BASIC rows;11 unresolved drawn-grid markers
preserved. Database174–176 of verified174–177 restores26 regions,16 blocks,
five images,67 indexed example rows and five prose boundaries. One syntax-crop
edge repaired once. Both natives/full assembly rebuild identically;111 prior
packages and nine prior assemblies validate unchanged.
Batch29 completes database177 and assembles174–177:31 regions,18 blocks,
six original images and93 indexed native example rows;seven prose boundaries.
Medical178–182 of verified178–185 restores46 regions,27 blocks,15 original
images,eleven linked headings and four prose boundaries. One database syntax-crop
repair;both natives and assembly rebuild identically.113 earlier native packages
and ten earlier assemblies validate unchanged.
Batch30 completes medical183–185 and assembles178–185:75 regions,39 blocks,
31 original images and18 linked headings. Five native prose boundaries and the
182/183effectlist continuation are reviewed; native segments remain immutable.
UPDATE186–188 of verified186–189 restores28 regions,21 blocks,five images and
32 indexed table rows. One uppercrop repair recovers187firstconditionline.
Printed table conflicts and syntax remain literal; exact rebuild and preservation
checks cover115 earlier native packages and eleven earlier assemblies.
Batch31 completes UPDATE189 and assembles186–189:30 regions,22 blocks,five
images,32 indexed native table rows and52 physical BASIC rows. The original
numbering,190wrap and sampletable conflicts remain unchanged. 세운상가190–194
of verified190–204 restores29 regions,15 blocks andfour original images.
Nine prose boundaries and the190/191split title are reviewed; no crop repair.
Exact rebuild and preservation checks cover117 earlier packages and12 assemblies.
Batch32 extends 세운상가 through195–200:45 regions,34 blocks,four original
images,ten indexed hardware-table rows and seven prose boundaries. Twenty-four
vendor entries retain source categories and cross-column/page continuations.
Two crop edges repaired once each; exact rebuild and preservation checks cover
119 earlier native packages and thirteen assemblies. Both segments remain immutable.
Batch33 completes 세운상가201–204 and assembles190–204:101 regions,69 blocks,
ten original images andten indexed hardware-table rows. Three immutable segments
retain21 native prose boundaries andtwo crosssegment reading links. 기계어테크닉
206–207 of verified206–209 has17 regions,13 blocks,one title artwork,five physical
assembly rows and33 indexed prose examples.205technicaldivider is non-owning.
No crop repair; exact rebuild and preservation checks cover120 earlier native
packages and thirteen assemblies.
Batch34 completes 기계어테크닉208–209 and assembles206–209:32 regions,
24 blocks,three images and40 physical assembly rows across three captioned listings.
Leading-zero line numbers remain literal;the assembler now accepts them with integer
indexes while preserving existing string indexes. All89 PDF tests pass.
Interface210–213ofverified210–217 has28 regions,13 blocks,seven images andeight
prose boundaries. Active-low overbars and the two-panel road spread are preserved.
No crop repairs;exact rebuild and preservation checks cover122 earlier native
packages and fourteen assemblies.
Batch35 completes interface214–217 and assembles210–217:58 regions,27 blocks,
12 images,eight linked captions and19 native prose boundaries. The213/214수도
reading link preserves native bytes;an adapter records the omitted opening field
in the earlier outgoing note using the reviewed incoming link. All90 PDFtests pass.
Shape218–219ofverified218–227 has18 regions,11 blocks,four images,a searchable
six-row vector table andthree prose boundaries.220–227andassemblyremain.
No crop repairs;exact rebuild and preservation checks cover124 earlier native
packages and fifteen assemblies. March has twenty-nine readable andone partial
article,four group headings and10 entries awaiting classification/restoration.
Batch36 restores shape220–225: 56 regions, 30 blocks, nine original images,
153 physical BASIC rows, 55 indexed examples and sixteen prose boundaries.
Page222's nonlinear prompt flow is source-linked; tables2/3 have searchable rows.
The error patch is separate from the main listing, which continues at226line1310.
Printed binary/address/capacity inconsistencies and missing operators remain literal.
No crop repairs or OCR changes; exact rebuild and preservation checks cover126
prior packages and sixteen assemblies. Counts remain29 readable/one partial,
four group headings and10 unclassified entries. Whole March remains incomplete.
Batch37 finishes shape226–227 and assembles218–227:83 regions,45 blocks,
15 images,389 physical listing rows and110 indexed native examples. Three immutable
segments retain source code,output,wraps andhistorical discrepancies; six obsolete
scope notes resolved. The225/226listing-block link preserves1300→1310.
A/D228–231ofverified228–241 has27 regions,14 blocks,seven images,four captions,
19 indexed examples andsix prose boundaries. Its source-backed narrative order is
228→231→230→232,with original folios andregions unchanged. Two crop repairs,
exact native/assembly rebuilds and127 prior native/sixteen assembly checks pass.
Batch38 restores A/D232–237: 50 regions,27 blocks,13 original images and captions,
38 indexed examples and ten prose boundaries. Printed formulas and claims stay
literal; table3 and diagram labels remain source images. Two diagram crops were
widened once each; initial evidence retained. Exact rebuild, indexes and129 prior
native/seventeen assembly checks pass. OCR settings remain unchanged.
Batch39 finishes A/D238–241 and assembles228–241: 113 regions,61 blocks,
29 source images,25 linked captions,24 physical assembly-listing rows and95 native
indexed examples. All three original segments remain exact; six scope notes resolve.
Contestresults243 is independently readable: six regions,four blocks,two column
joins and13 indexed examples. Both native packages and the full assembly rebuild
identically;130 prior natives and seventeen assemblies validate unchanged.
No crop repair or OCR retry; only canonical contest-title spacing changed in metadata.
Batch40 restores the word-processor article's surviving244–249:23 regions,
14 blocks,two original images,453 physical listing rows (220 numbered),55 indexed
examples and one prose/six listing boundaries. Printed250–251 are missing:
PDF250 bears252 and begins tunnelgame. The surviving listing ends within3190;
245describes routines through4150. This is a terminal source-gap partial outcome,
with all available pages restored and no invented continuation or program repair.
Canonical0034공모입선작 is a non-owning group supported by its two awarded children.
Exact rebuild and132 prior native/eighteen assembly checks pass;OCR unchanged.
Batch41 completes tunnelgamePDF250–252/printed252–254:13 regions,seven blocks,
two images,198 physical listing rows (97 numbered),34 indexed examples andtwo
prose boundaries. DebuggingroomPDF253/printed255:12 regions,nine blocks,two images,
25 physical listing rows in three correction groups,seven numbered labels andeight
indexed examples. Published corrections remain separate from earlier native articles;
PRINT graphicG870 retains an undecoded marker linked to its scan. Four one-time
crop repairs preserve initial evidence;OCR settings unchanged. Exact rebuilds,
all indexes and133 prior native/eighteen assembly preservation checks pass.
Batch42 completes Q&A PDF254–257/printed256–259 and the listed advertising index
on lower204. Forty regions,31 blocks,four original images,seven standalone BASIC
rows and78 indexed examples;five prose boundaries. Sixteen one-time crop repairs
preserve initial evidence. Inline code with its Korean prose tail remains in article
text. Exact rebuilds and135 prior native/eighteen assembly checks pass.
Batch43 reconciles canonical0040 정보 레이다 with source124–131, superseding the
earlier unlisted exclusion. Opening124–129 restored:50 regions,33 blocks,ten
original images,78 indexed examples andseven prose boundaries;no crop repairs.
Exact rebuild and137 prior native/eighteen assembly checks pass.
Batch44 completes news130–131 and assembles124–131:68 regions,48 blocks,ten
original images,139 indexed native examples,ten native prose boundaries andone
cross-segment continuation. Exact native/assembly rebuilds and138 prior native/
eighteen assembly checks pass. Canonical0038정보모음 is a non-owning group.
The March closeout is complete. All 44 canonical entries and 38 article outcomes
match the standalone export. Stale aggregate ledger counters were recomputed from
the authoritative entries. Printed pages 250–251 remain an explicit source gap.
See `private/pdf-restoration/12-1984-03-closeout/completion-audit.json` and
`validation.json`. The March objective is complete; May 1984 is the next supplied issue.
The revised requirements supersede rendering gates in older progress entries,
tool documentation, and saved successor notes; those records remain evidence of
work already performed, not authority to repeat rendering work.

## Historical completion record

The following records work completed under the earlier scope, including reader
work. Steps 8–9 below now specify the data contract and data acceptance gates;
reuse existing evidence rather than repeating completed extraction.

Revised 2026-10-02. Status: **steps 1–11 complete.** November 1983's
47 TOC entries are accounted for: 35 readable/sample-reviewed articles, five
group headings and seven section references. The standalone issue reference and
complete staged reader export passed integrity and desktop/mobile checks.
No partial, image-only, failed or unresolved article outcomes remain for this
issue; manual bitmap correction in 잠수함 and full proofreading remain deferred.
The **12-catalog-reconcile** checkpoint is complete: the owner's corrected TOC,
completed cover/TOC image integration and all 35 November articles coexist in a
validated staged reader. February batches 01–03 restored the complete editor's
note and three FC-100 feature segments covering printed18–30. The feature is now
assembled as readable/sample-reviewed, with every original segment and correction
record preserved. Batch04 restored 우주전쟁, printed32–35, and classified the
취미생활 divider. Batch05 restored FLIP-IT II, printed36–40, preserving all
listing wraps. Batch06 restored 구슬게임, printed41–43, including its character
definitions and duplicate printed line number. Batch07 restored 마이크로텍스트's
first six pages, printed44–49 / PDF51–46, through BASIC2080. Its complete extent
is verified at printed44–51. Batch08 restored the final two pages, printed50–51,
through3470. The complete eight-page article is now assembled and validated,
preserving both immutable segments, all correction records and physical wraps.
Batch09 restored 3차원 미로, printed52–53, and 드래곤, printed54–55, preserving
physical code wraps and explicit unknown strings/glyphs while excluding the
shared-page advertisement. Batch10 restored 최신예 폭격기32K, printed56–58,
and 천하무적 제공호, printed59, retaining literal DATA strings and historical
code anomalies. Batch11 restored the complete 루빅의 큐브 at printed60–64 /
PDF35–31, preserving462 numbered statements in502 physical rows, two diagrams
and three command tables. The following advertising/promotional pages are
excluded; 교육입문 is a verified group divider. Batch12 restored 독도는 우리땅,
printed70–75 / PDF25–20, including its page-spanning DATA statement, Korean
screen strings, map DATA and music strings. Batch13 restored 사용하는 사람의
입장에 서서, printed76–77 / PDF19–18, and APA프로그램의 활용법, printed78–81 /
PDF17–14. All26 guide items and15 independent command/listing examples are
preserved, with source-linked notes for hidden controls and literal anomalies.
Batch14 restored 파스칼 프로그래밍 마지막회, printed82–87. The source order
changes: its title is PDF13 and its continuation is PDF79–83; PDF12–7 are ads.
All six editor sections, file-format/P-machine discussion, nine independent
examples and four illustrations are preserved. Batch15 restored the first six
pages of 마이크로컴퓨터 시스템 입문, printed88–93 / PDF84–89. Its complete
extent is verified at printed88–96 / PDF84–92; 타임머신 starts97 / PDF93.
The first package preserves15 images,14 captions and an eight-row searchable
controller table. Batch16 restored final printed94–96 / PDF90–92, including
figures15–20, three references and ten overlined signal-name occurrences.
The complete nine-page article is now assembled and validated, preserving both
immutable segments and projecting every regional correction index. Batches17–19
restored 타임머신, 매개변수로 표현된 함수의 그래프, Q&A and 디버깅 룸.
Batches20–21 restored both 정보 레이다 subsections; the complete eight-page
article is now assembled and validated, preserving24 news-item identities,
image associations and all correction ranges. Batch22 restored 삼성SPC-500 at
printed122–124 / PDF118–120, including its final system diagram above an excluded
advertisement. All six tables/diagrams and the photograph retain original images;
the six captions and all prose are transcribed. Batch23 restored the first six
pages of 회계 관리 프로그램, printed125–130 / PDF121–126, including15 variable
definitions, three screen images, a flowchart and both halves of a photograph.
Its complete extent is verified at printed125–135 / PDF121–131. Batch24 restored
the final explanation and all four BASIC pages:246 numbered rows,35 margin labels
and four complete listing-panel images. Both segments retain180 review notes,
108 regional ranges,28 Unicode spans and65 unresolved readings or symbol/spacing
markers. The eleven-page accounting article is now assembled and validated with
all regional/Unicode and listing correction indexes projected together. February
has **37 readable articles and no partial articles**, all sample-reviewed,
six classified group headings and no unresolved entries. Batches25–29 restored
UNIX, VisiCalc 활용, 우수한 프로그래머가 되는 첩경 and dBASEII, and classified
테크니컬. Batches30–38 and their assemblies completed 로더란 무엇인가,
기계어 테크닉, the16-page 한글 워드프로세서의 설계2 and the eight-page
A/D,D/A의 이론과 실제1. All original segments and correction evidence remain
preserved. Batch39 restored the complete competition notice200/PDF196 and
second competition review201/PDF197, including all11 reviewed submissions.
Batch40 restored complete SNAKY GAME202–207/PDF198–203,including148 numbered
BASIC statements in282 physical rows,five images and two searchable tables.
Batch41 restored complete 지하괴물잡기208–212/PDF204–208,including216
numbered statements in242 physical rows and all18 character definitions.
Bitmap spans and unknown blank widths remain explicitly source-linked for
manual correction. Batch42 restored the dictionary opening213–218/PDF209–214,
with37 entries (last DEFDBL incomplete),68 machine labels,three images and a
searchable16-color table. Ending239/PDF235 and following advertisement240
are inspected;remaining continuity still awaits source review. Batch43 restored
219–224/PDF215–220,including57 definition fragments,73 machine labels and
11 independent examples. Twelve pages are now preserved in two immutable
segments;the DEFDBL boundary join is verified. Batch44 restored225–230/PDF221–226,
including47 entries,17 independent examples and three original table images.
Batch45 restored231–236/PDF227–232,including57 entries,19 independent
examples and the original REPT image. Twenty-four pages are now preserved in
four immutable segments;two TI$ HOME symbols remain source-linked markers.
Batch46 restored final237–239/PDF233–235,including six final commands,
five ASCII tables in six original panels and166 searchable data rows. All27
pages now have verified continuity;64 final table-glyph markers remain explicit.
The complete27-page dictionary is now assembled and validated:245 reading
blocks,14 original images,276 global regional ranges and73 uncertainty markers.
All five source packages remain byte-identical;DEFDBL's first boundary is joined.
The remaining 공모입선작 and 정보모음 entries are now verified non-owning
TOC groups. All43 entries reconcile as37 readable/sample-reviewed articles and
six group headings;no eligibility decisions remain. The **12-1984-02-reference**
checkpoint now packages all37 articles with their original JSON,assets and
correction records. Source/page checks,static links and a byte-identical rebuild
pass without browser use. **12-1984-02-closeout is complete**: separate combined
reading-room integration,preservation checks and desktop/mobile acceptance pass.
All37 February articles coexist with35 November articles and3,386 CD articles;
corrected TOC,145 cover assets and145 TOC scan sets remain intact. Manual bitmap
correction and full proofreading remain deferred. February1984 is complete within
the agreed restoration scope. Step12 remains open for the other17 eligible issues;
the next issue is March1984,with no extraction started yet.

## Objective

Restore only articles listed in [TOC.md](TOC.md) into JSON, extract image assets
and available covers, and preserve useful results with explicit gaps. Use local
OCR. Follow the bounded checkpoint approach in
[PLAN-CD1.md](PLAN-CD1.md), [PLAN-CD2.md](PLAN-CD2.md),
[PLAN-CD3.md](PLAN-CD3.md). Rendering and reading-room delivery are separate work
under [PLAN-reading-room.md](PLAN-reading-room.md), when requested.

## Working rules

- Work step by step. After every numbered checkpoint and named batch, append a dated entry to
  the relevant [issue progress file](docs/progress/README.md), recording inputs, completed work, outputs,
  validation, unresolved issues, and the next step. Record partial or blocked
  outcomes honestly before moving on. Also record each issue closeout. Steps
  11 and 12 are campaign milestones, not single execution checkpoints. Commit
  changes after each completed step or named checkpoint. Keep
  [PROGRESS-PDF.md](PROGRESS-PDF.md) as the current status index; update it at
  issue milestones rather than appending batch histories there.
- Each executable checkpoint has one goal, fixed inputs, a work limit, a saved
  artifact, and an acceptance check. Split a checkpoint before expanding its
  scope. Mapping proceeds with the current article/batch, not across the archive
  before the pilot. The stall rule below does not replace these work limits.
- A partial checkpoint preserves useful outputs and an explicit exception. It
  permits independent work to continue but does not satisfy a failed prerequisite
  for bulk processing. Record the next bounded repair task when a gate fails.
- Avoid excessive investigation. Investigate only what is needed to deliver the
  current checkpoint; keep localized uncertainties visible and defer unrelated
  recovery work.
- **If a task remains stalled across three consecutive context windows, stop
  work and notify the owner.** Carry the stall count and blocker through context
  handoffs rather than restarting the count. Report the task, what was tried,
  the blocker, preserved partial outputs, and what would allow progress. Do not
  silently continue investigating beyond this limit.
- Preserve source PDFs and existing CD references. Keep scans, OCR, restored
  text, images, and generated data packages in ignored private/build locations.
- Article extraction is limited to existing TOC entries. Ignore advertising
  and other unlisted material for now, including advertising regions on pages
  shared with eligible articles. Cover extraction is explicitly included.
- Use scans as evidence for corrections. Preserve raw OCR, CD transcription,
  and scan-supported corrections separately. Reproducibility does not establish
  transcription accuracy or complete printed-issue coverage.
- Validate data and source evidence directly. Do not generate HTML, launch a
  browser, rebuild a reader, or run frontend checks to accept PDF restoration.
  `readable` describes coherent extracted content, not successful UI rendering.

## Cover and TOC inputs and preservation

- `TOC.md`, including the owner's `bccb3e0` corrections, remains authoritative.
  OCR findings do not authorize further catalog edits. Preserve stable IDs with
  explicit decisions; keep old catalog snapshots and article packages unchanged.
- Follow [PLAN-covers.md](PLAN-covers.md): donated cover → verified PDF cover →
  placeholder. Reuse completed cover preparation and preserve its asset metadata
  and bounded derivatives rather than restoring deleted legacy JPEGs. Serving
  covers is outside this plan.
- Follow [PLAN-tocs.md](PLAN-tocs.md): preserve normalized originals and the
  existing reduced-image assets and viewer/gallery work without modifying them.
  TOC presentation is outside this plan. Completed scan comparison reports remain
  pinned historical evidence; a new catalog hash does not silently reapprove them.
- The corrected import contains 5,299 entries across 122 issues. The PDF queue
  now contains **828 entries and 686 provisional article candidates** across the
  same 19 eligible PDFs. These replace the original 839/684 sizing totals below.
  November's 47 entries and February's 43 entries are unchanged.
- Current PDF queue: `private/pdf-restoration/inventory-2026-10-01/queue.jsonl`.
  Its report pins the original source inventory and November completion ledger;
  `completed_outcome` preserves finished classifications and restoration states.
  Original inventory and step 11 closeout records remain historical artifacts.

## Inspected starting point

The supplied `maso-pdf/` directory contains **21 PDFs, 6,615 PDF pages, and
2,664,455,314 bytes (2.48 GiB)**.

| Group | Supplied issues | Work in this pass |
| --- | --- | --- |
| Before CD coverage | 1983-11; 1984-02, 03, 05–10, 12; 1985-02, 03, 10, 11 | TOC-listed articles and covers |
| CD1 overlap | 1988-01; 1991-08, 09; 1992-12; 1993-03 | TOC-listed articles, covers, and evidenced CD comparisons |
| CD3 overlap | 1995-03, 07 | Covers only; no entries exist in the current TOC |

Twenty PDFs have no extractable text. September 1991 has only a short garbled
annotation mentioning `397~398`; its significance is unverified. Sample pages
show multi-column Korean, English, code, diagrams, advertisements, and PDF
rotation metadata. March 1995 PDF page 20 appears nearly blank. These are
planning observations, not a completed page or article inventory. Filenames are
provisional issue labels until checked against visible source evidence.

The current structured TOC snapshot matches `TOC.md`. For the 19 supplied issues
with TOCs it contains **839 entries and 684 provisional article candidates**;
November 1983 contains **47 entries and 35 candidates**. These are sizing inputs,
not final extraction totals. Page-less leaves and parent/child classifications
still require review; do not restrict eligibility to the existing candidate list.

## Checkpoint quality and batch limits

Keep availability and verification separate. Availability is `readable`,
`partial`, `image-only`, `failed`, or `unresolved`; verification is `unreviewed`,
`sample-reviewed`, or `fully-reviewed`, with the reviewed regions and remaining
uncertainties recorded. A failed OCR attempt does not mean an article is missing.
Only record missing source pages or articles when inspection supports that claim.

For the pilot and contrasting samples, inspect every mapped region for reading
order, omissions, unwanted material, and figure/caption placement. Compare all
pilot reading text with the scan, retaining uncertain characters as marked gaps.
For each contrasting sample, compare at least one complete prose column and one
code/figure region where present, recording the exact reviewed regions. A
readable result must preserve coherent prose order and expose available code and
figures without silent omissions; code that has not been checked character by
character remains explicitly unverified. This is not a requirement to execute
historical code or to proofread the whole archive.

For old user-defined bitmap characters, the owner has authorized manual
post-production correction (2026-09-28). Preserve uncertain occurrences as
explicit markers linked to printed lines and pinned scan regions in
`corrections.json`; leave unknown character codes/counts unresolved. Do not let
glyph decoding block the bounded extraction pass or invent replacement bytes.
Track pending manual glyph corrections separately from deferred page coverage.
Complete page coverage can be readable with these visible uncertainties;
segmented coverage remains partial until assembly. Neither status certifies
character-perfect or executable code.

Before bulk work, prove useful results on the pilot and contrasting samples,
including Korean prose, code, illustrations, and later layouts. An image-only or
unresolved result is valid accounting but does not prove the workflow works for
that case. If a required case fails, save it and complete a bounded repair or
replacement sample before passing the bulk gate. Subsequent issue reports must
separate usable results from exceptions rather than equating accounting with
successful restoration.

The initial qualification ceilings were **3 articles and 12 distinct source
pages per batch**. Step 10 passed the bulk-readiness gate and selected lower
operating ceilings of **2 articles and 6 distinct source pages per batch**,
whichever is reached first, to keep manual mapping and review bounded. Apply
these ceilings to all subsequent named batches. Historical manual review times
were not recorded; step 10 measures replay time and preserves workload counts
without inventing a restoration throughput estimate. Time new mapping and
review work prospectively.
For a longer article, use numbered page/region segments within the page ceiling,
then close out the assembled article separately. Never mark a segment as a
complete article. Each batch names its TOC IDs, source pages or mapping targets,
lookup-page limit, and outputs before execution. Cap location research at 20
inspected pages outside known article regions per batch; preserve unresolved
locations when that limit is reached. Permit one targeted OCR retry per failed
region in the batch; additional recovery becomes a separate deferred task.

## 1. Record sources and a provisional TOC queue

**Goal:** establish exactly which sources and TOC identities this pass may use.
**Input and limit:** metadata for all 21 PDFs and the existing TOC snapshot;
no article-boundary investigation.

- Record hashes, sizes, page counts, dimensions, rotation, and text-layer
  availability. Pin the TOC and structured snapshot hashes; reuse existing IDs.
- Save all 839 relevant TOC entries with their hierarchy and provisional
  classifications. Preserve page-less and ambiguous entries for later review.
  Resolve article versus heading decisions during local mapping, separately
  from the historical snapshot.
- Record the two 1995 PDFs as cover-only. Flag any source/TOC identity conflict
  for visual verification rather than inventing an association.

**Artifact/check:** a source manifest and provisional queue reconcile to 21 PDFs,
6,615 PDF pages, and the pinned TOC counts. Every queue record has an existing
TOC identity; uncertain classification remains explicit.

## 2. Account for available covers

**Goal:** recover usable front covers without replacing owner-supplied images.
**Input and limit:** the source manifest; inspect at most the first and last five
pages of each PDF for cover evidence. Defer unresolved cover searches.

- Verify visible issue dates. Record conflicts without attaching a cover to an
  unverified issue identity.
- Extract an embedded image where practical, otherwise render it upright with
  correct proportions. Record source hash, page index, dimensions, and settings.
- Add missing covers using `covers/masoYYMM`; preserve existing covers and keep
  alternatives separately. Record damaged, missing, or uncertain outcomes.

**Artifact/check:** a 21-source cover ledger plus available images. Inspect each
new cover for orientation, proportions, and date evidence; verify existing cover
bytes remain unchanged. Presentation checks belong to the separate rendering task.

## 3. Map one pilot and define its restoration record

**Goal:** establish an evidenced article extent and a reusable record format.
**Input and limit:** November 1983's “숨겨진 미로,” listed at printed page 28;
its opening was observed at PDF page 30. Map only this article, within the batch
page/lookup limits; segment it if needed.

- Verify its opening, ending, and continuations. A next TOC entry is not proof
  of an ending. Use scanned contents only to clarify existing entries.
- Record PDF page indexes and printed numbers separately, with an explicit
  index convention. Store ordered regions, coordinate units/origin, rotation
  transforms, and source dimensions; allow shared pages and continuations.
- Exclude advertisements and unlisted material. Keep ambiguous boundaries
  unresolved; do not guess a fixed page offset.
- Define the minimal article package: stable scan-derived ID distinct from CD
  IDs and independent of OCR titles, issue/TOC links, source hashes, region map,
  raw OCR paths/settings, corrected blocks, figures, asset/file references, and
  independent availability/review states. Keep correction evidence separate from raw OCR.

**Artifact/check:** one evidenced pilot map and a documented package schema with
synthetic examples. Verify numbering, rotated coordinates, shared-page exclusion,
and noncontiguous ordering with focused fixtures. If the pilot cannot be mapped,
record the blocker and select one named replacement before OCR work.

## 4. Establish local OCR on one pilot page

This original setup milestone is historical. For a new restoration batch, apply
the [current routing guide](#current-ocr-routing-guide)
above using the already installed, verified engines.

**Goal:** produce repeatable local OCR with positional evidence.
**Input and limit:** one mapped pilot page/region and the step 3 schema; one
baseline engine and at most two processing configurations.

- Set up Korean/English Tesseract, absent during initial inspection, with pinned
  engine/model versions and reproducible setup instructions. If installation is
  blocked, save the setup result as its own checkpoint before further work.
- Compare page and column/region processing where the page contains only eligible
  content; otherwise mask or crop excluded material before OCR. Retain raw text,
  positions, and settings. Record preprocessing only on derivatives.

**Artifact/check:** one OCR evidence bundle and repeatable commands. Re-run the
chosen configuration and compare text/positions, excluding declared volatile
metadata. Record quality limits and processing time; do not start an engine search.

## 5. Deliver the complete pilot package

**Goal:** make one article readable and traceable to its scan.
**Input and limit:** the mapped pilot and selected OCR configuration; one article,
using separate segment checkpoints if its extent exceeds the page ceiling.

- Produce ordered prose, literal code, captions, and figure crops. Preserve code
  whitespace and uncertain characters; store scan-supported corrections apart
  from raw OCR. Apply the pilot review requirement above.
- Export article JSON, extracted images, correction records, and scan-region
  evidence with explicit availability/review states and a file/hash manifest.

**Artifact/check:** one reviewed JSON and asset package. Check complete
mapped-region coverage, advertisement exclusion, local asset references, and
unchanged raw OCR. Rebuild the package to verify stable IDs and content. A
partial result is retained, but the useful-pilot gate must pass before scaling.

## 6. Validate contrasting articles in separate checkpoints

**Goal:** establish that the package and processing rules handle observed variety.
**Input and limit:** the pilot workflow; execute and log each checkpoint below
separately, within the batch ceilings. Name the sample IDs before starting.

- **6a — Early-format contrast:** select at most two November articles that
  supplement the pilot with prose, code, illustrations, and a nested TOC case.
  Resolve whether parent entries group children without duplicating bodies.
- **6b — January 1988:** process one eligible article, checking page numbering,
  column order, rotation where present, figures, and code.
- **6c — August 1991:** process one eligible article with the same checks. Record
  unsupported layout features explicitly rather than silently dropping them.

**Artifact/check for each:** a sample package, exact review evidence, and a short
feature/result matrix. Apply the contrasting-sample review requirement above.
Test missing pages, continuations, and shared-page exclusions synthetically when
real samples do not exercise them. Preserve successful samples for the bulk pass.

## 7. Demonstrate one evidenced CD comparison

**Goal:** prove that scan-supported corrections and CD transcription remain distinct.
**Input and limit:** one successful overlap sample from step 6 and its existing
CD reference; one article association and up to two mapped pages of comparison.

- Require evidence for the association; title similarity alone is insufficient.
- Preserve OCR, CD text, differences, and scan-supported corrections separately.
  Record reviewed version relationships without treating a sample comparison
  as verification of the complete CD article.

**Artifact/check:** one comparison record whose decisions lead back to the scan;
no raw OCR or CD bytes change. If no sampled association can be supported, record
an explicit deferred comparison and expose no relationship. This does not block
independent PDF extraction. Leave September 1991's annotation until relevant to a
selected article, and defer March 1995's interior blank page entirely unless it
becomes relevant to cover identification.

## 8. Establish a portable JSON and asset export

**Goal:** deliver a reusable data package independent of any renderer.
**Input and limit:** the pilot package and documented restoration schema;
one scan-derived article, without changing existing CD records.

- Document the JSON contract for ordered blocks, source/region references,
  corrections, assets, and independent availability/verification states.
- Retain canonical issue/TOC identities, stable article/block IDs, and only
  evidenced version relationships. Existing compatibility fields may remain,
  but must not require HTML pages, reader routes, or a running application.
- Include a manifest of package files and hashes with resolvable local paths.

**Artifact/check:** one JSON and asset export with focused schema/reference
checks. Re-export deterministically and verify raw OCR, source evidence, and CD
bytes remain intact. Correct package omissions before bulk restoration.

## 9. Validate the pilot data and evidence

**Goal:** prove that article content and corrections can be consumed from files.
**Input and limit:** step 8's package; the pilot plus synthetic partial,
image-only, failed, and unresolved outcomes.

- Validate issue/TOC/article identities, block order, source-region coverage,
  asset paths/hashes/dimensions, correction targets and listing byte ranges.
- Verify literal code and whitespace survive JSON serialization and extraction.
  Inspect source/crop images directly for evidence and crop quality.
- Check that incomplete outcomes and review limits remain explicit, and that
  the package can be validated without HTML, CSS, reader data, or a browser.

**Artifact/check:** a saved data-validation report and focused fixtures covering
the above invariants. Retain the scan comparison/review evidence from steps 5–6;
passing structural checks does not establish transcription accuracy.

## 10. Prove bounded batch and resume behavior

**Goal:** make the bulk procedure safe to repeat and interrupt.
**Input and limit:** at most three already prepared sample articles within the
12-page ceiling; use synthetic failures where needed, without expanding the queue.

- Define cache keys from source hash, region map, engine/model versions, and
  processing configuration. Preserve reviewed corrections across OCR reruns.
- Demonstrate interruption/resume, one isolated failure, and invalidation after
  a mapping/configuration change. Unaffected results must not be reprocessed.
- Measure mapping, OCR, review effort, and output size. Confirm or lower the
  initial batch ceilings, and document exact prepare/resume/export/check commands.

**Artifact/check:** a tested batch runner, durable outcome ledger, documented
limits, and a bulk-readiness record. Advance only after steps 5–6 demonstrate
useful results and steps 8–9 demonstrate valid JSON and asset exports. Record
step 7's comparison result or explicit deferral. A gate failure becomes a bounded repair
checkpoint, not a reason to process more issues speculatively.

## 11. Complete November 1983 through named batches

**Goal:** deliver the first complete issue accounting and JSON issue index.
**Input:** November's 47 TOC entries, existing samples, and the validated workflow.
**Size:** campaign milestone; each `11-batch-NN` is an independent checkpoint
within step 10's limits, followed by a separate `11-closeout` checkpoint.

- Map each batch immediately before extraction. Resolve headings, parent/child
  ownership, and page-less entries locally; retain decisions with evidence.
- The opening feature is one article across PDF18–28. Its seven pageless TOC
  children are section references: preserve their TOC entries and link them to
  the final parent article and stable section/block IDs after assembly. Count
  these references separately from body-owning articles and group headings.
  PDF29 is excluded.
- Reuse successful samples. Save packages, review coverage, failures, retries,
  and unresolved boundaries after every batch. Avoid duplicate article bodies.
- For disjoint reviewed segments, assemble without new OCR. Retain original
  packages/maps/settings unchanged, validate complete ordered page coverage,
  rebase correction scan paths and listing byte ranges, and explicitly resolve
  superseded scope notes. Complete coverage can be readable/sample-reviewed
  while scan-linked bitmap markers remain pending the owner's manual correction.
- At closeout, generate a JSON issue index and report containing TOC accounting,
  package/asset references, source evidence, correction records, and outcome states.

**Artifact/check per batch:** saved packages and reconciled batch outcomes, with
region/order checks and recorded text-review coverage. Validate JSON, assets,
source links, correction byte ranges and reproducibility at this stage. These
data checks also apply at issue closeout; no HTML or browser acceptance is required.
**Issue closeout:** all
47 entries have a classification and every eligible article has an outcome;
no unlisted article is added. Report readable/partial/image-only/failed/unresolved
counts separately, plus unresolved eligibility decisions. Validate the JSON issue
index, package references and asset integrity before moving to remaining issues.

## 12. Process remaining issues through the same bounded procedure

**Goal:** extend the proven workflow to the other TOC-covered PDFs; 17 remain
after February 1984's completion.
**Input and size:** one issue at a time chronologically; named checkpoints such as
`12-1984-02-batch-01` and `12-1984-02-closeout`, using the established ceilings.

- Reuse completed samples; map only the current batch. Preserve evidence and
  continue past isolated failures within the retry limit.

### Historical February checkpoints

The notes below retain the completed February sequence under the earlier scope.
References to subsequent work describe the next action at that historical point;
they do not impose rendering or reader acceptance on remaining issues.

- February's PDF is not in printed reading order. Verified local mappings are
  PDF78→printed17, PDF77→18, PDF76→19 and PDF75→20; PDF79 instead contains
  printed83. Confirm each page locally, retain explicit reading order and never
  infer a global offset. The FC-100 feature starts on observed printed18 despite
  catalog17; preserve the discrepancy without editing the authoritative TOC.
- The feature's dense reference tables may remain original scan images during
  the bounded pass. State clearly which table contents are not transcribed;
  preserve full-resolution access and separate captions. Continue prose and code
  extraction without treating image-preserved tables as searchable text.
- The assembled FC-100 covers printed18–30 / PDF77–65 in descending local order.
  Both cross-segment prose joins, all correction ranges, original table/diagram
  images and unresolved transcription notes remain explicit. Reuse this complete
  package at issue closeout. PDF64's 취미생활 divider and PDF63's 우주전쟁 opening
  remain outside this article; verify each following page before extraction.
- An unsupported format becomes a separate bounded sample/repair checkpoint;
  do not expand a processing batch into an open-ended pipeline redesign.
- 마이크로텍스트 spans eight verified pages, exceeding one batch's ceiling.
  Preserve the first six-page segment and its seven prose/table joins, code270
  page continuation, literal technical anomalies and correction indexes. The
  remaining two pages were restored separately. The complete article now passes
  assembly and browser acceptance with opt-in `wrapped-listing-v1` support:
  338 logical/606 physical rows, partial anomaly ranges, DATA indexes and all
  original metadata are preserved. Synthetic tests cover wraps, source identities,
  UTF-8 ranges and tampered indexes; existing assembly modes remain unchanged.
  The following 3차원 미로 and 드래곤 are now restored from locally verified
  printed52–55 / PDF43–40. Their physical wraps, unknown strings and literal
  syntax anomalies remain explicit; the advertisement below 드래곤 is excluded.
  최신예 폭격기32K and 천하무적 제공호 are also complete at printed56–59 /
  PDF39–36. Retain their literal shape DATA punctuation, quoted spacing and
  historical address/direction anomalies for owner proofreading.
- 루빅의 큐브 is complete at printed60–64 / PDF35–31. Its following PDF30–27
  advertising/promotional pages are excluded and PDF26 is the 교육입문 divider
  (locally inferred position69, no visible folio). Preserve its literal code
  anomalies, numeric physical wraps and source-linked review notes.
- 독도는 우리땅 is complete at printed70–75 / PDF25–20. Retain its cross-page
  DATA190,28 literal DATA records,14 music strings, Korean Unicode reading text
  and source-linked anomalies. Original encoding, execution and playback remain
  unverified; the flowchart and screen image retain their internal labels as images.
- 사용하는 사람의 입장에 서서 and APA프로그램의 활용법 are complete at
  printed76–81 / PDF19–14. Preserve all26 guide items,15 separate APA examples,
  terminal input/output identities and hidden/inverse-control uncertainty. Do not
  interpret the combined example download as one executable BASIC program.
- 파스칼 프로그래밍 is complete at printed82–87 / PDF13 and79–83. Preserve
  the verified scan-order jump, all six editor sections, four illustrations and
  nine independent examples. The circled DEMO markers are editorial labels;
  retain deliberate inyeger and literal menu/technical wording without repair.
- 마이크로컴퓨터 시스템 입문 is complete at printed88–96 / PDF84–92.
  Preserve both original segments,21 images,20 captions, eight controller rows,
  three references,72 regional ranges and40 review notes. The explicit page93/94
  과/의 join retains the intervening figure/caption/table order. The tested
  opt-in `regional-prose-v1` assembly mode projects regional, table, Unicode,
  signal and reference ranges while keeping old assembly behavior unchanged.
- 타임머신 is complete at printed97–101 / PDF93–97. Preserve the72-line
  main calendar listing and three separate compatibility variants,84 logical/
  88 physical rows, two original images, five prose joins and34 review notes.
  The30 explicit U+2422 blank symbols are reading notation, not recovered spaces
  or original bytes. Retain literal Y3<>=0, the variant330 difference, physical
  PRINT wraps and prose variable-name discrepancies without inferred repairs.
- 매개변수로 표현된 함수의 그래프 is complete at printed102–104 /
  PDF98–100. Preserve67 logical/134 physical BASIC rows, including22 blank
  string rows, the cross-page400 continuation and the unnumbered55 target row.
  Two original screen photographs,34 review notes and the unresolved faint
  prose key name remain source-linked; quoted spacing/control bytes and graph
  execution remain unverified.
- Q&A is complete at printed105–107 / PDF101–103; 디버깅 룸 is complete
  on printed108/PDF104. Preserve eight indexed question/answer pairs, separate
  BASIC/disassembly examples, ten explicit assembly-row records and five prose
  joins. Six errata/enhancement entries index five independent BASIC patches
  and the source's incomplete prose corrections. Literal $300(786),80행,
  Y1),그리,/나머 and historical technical claims remain unmodified. Exact target
  articles/issues are unverified; never apply patches silently to prior exports.
- PDF105–106 are advertisements. 정보 레이다's domestic subsection is restored
  at printed111–116 / PDF107–112:15 indexed news items, eight photographs,
  one diagram, six prose joins and40 source-linked review notes. Preserve
  provisional 휩웨어 and literal quantities/spellings without inferred repair.
  The overseas subsection is restored at printed117–118 / PDF113–114: nine
  news items, three prose joins and26 review notes, retaining78%/73%, DRAM/DPAM,
  the prospective1983 date and1300MFLOPS. The complete eight-page extent is
  verified and both immutable segments are now assembled as readable/sample-reviewed.
  Validated news-index projection preserves all24 news identities, subsection
  membership, image associations,62 regional ranges,66 review notes and143
  Unicode spans. Independent stories and header regions partition the source;
  no new sentence join is needed. All71 PDF tests and deterministic rebuild pass.
  The page118 advertisement and following PDF115–116 notices are excluded.
  PDF117 is the 비즈니스 divider
  (no visible folio); 삼성SPC-500 opens at printed122/PDF118. These 정보모음
  entries occur physically before business; keep authoritative TOC order.
- 삼성SPC-500 is complete at printed122–124 / PDF118–120. The prose ends on123
  but the final system block diagram continues on124. Preserve all six numbered
  tables/diagrams, the computer photograph, six searchable captions and two column
  joins. Table cells, memory addresses and internal diagram labels remain original
  images rather than certified searchable text. Keep literal TV 표6, 비데오,
  키이, 8가지의 음계, Z-80A/Z80A and capacity claims. The124 bookstore
  advertisement is excluded; 회계 관리 프로그램 begins125/PDF121.
- 회계 관리 프로그램 spans printed125–135 / PDF121–131; UNIX begins136/PDF132.
  The first six pages are restored as a partial article with27 reading blocks,
  six original image crops, four captions and15 printed variable definitions.
  Preserve all eight prose joins,41 review notes,35 regional ranges and28 Unicode
  spans. Keep the provisional 역할난을, literal FI$/DI$/F1 and L3,K3,: notation,
  confirmed end-code999999, 지수승/지수성 and routine-name variants. Screen and
  flowchart labels remain imagery; blank flowchart nodes are not inferred.
  Final prose131 and BASIC listing132–135 are now restored:246 numbered/physical
  rows,35 separate margin labels (O/W repeated), an office photograph and four
  complete listing panels. Keep64 final-segment uncertainty markers,139 review
  notes and98 listing review spans. Tight W/AA/AB crop edges and1534's placement
  in the following region are documented; full panels retain exact source context.
  Each statement appears once in listing.txt. Literal THEN343, LB=0, KICOM and
  F1$/D1$ remain unchanged. Completed assembly projects both regional/Unicode
  indexes and listing rows/reviews through opt-in regional-listing-v1. Both source
  packages and previous mode behavior are preserved. All73 PDF tests, complete
  range validation and byte-identical rebuild pass; no new OCR or boundary join.
- UNIX spans printed136–142/PDF132–138; VisiCalc begins143/PDF139. The opening
  six-page segment has58 regions,37 reading blocks,13 original cartoons/diagrams
  and nine captions. Five join records connect eight boundaries;45 regional
  ranges,36 review notes and44 Unicode glyph spans are source-linked. Preserve
  historical 메인 머신, 쉘, 변수/module wording, ex/INed, MAKE/SCCS, DC/BC and
  pattern examples without modern correction. The last 살 continues as
  펴보기로 하자. on the final page. One r48 figure crop was widened once;
  original maps/OCR/export remain intact. Per-batch package checks pass without
  Playwright. Final page142 adds two cartoons and one caption. Completed seven-page
  assembly contains63 regions,38 reading blocks,15 images,10 captions and the
  explicit 살/펴보기로 join across the preserved machine-control cartoon.48
  regional ranges,43 review notes and46 Unicode spans validate in the combined
  download; both source packages and the deterministic rebuild are byte-identical.
- VisiCalc 활용 spans printed143–148/PDF139–144. Its complete package has34
  regions,21 reading blocks and seven original images. Five recorded joins
  connect six boundaries;27 regional ranges,48 review notes and177 Unicode
  spans validate against the complete text. Preserve source formula/command
  discrepancies without repair; document boxed cells, circled keys and fraction
  linearization as reading conventions. Spreadsheet cells remain imagery. All
  original assets, prior-file pins and deterministic rebuild pass without browser
  checks or generic pipeline changes. Next article begins149/PDF145.
- 우수한 프로그래머가 되는 첩경 spans printed149–154/PDF145–150. Its complete
  package contains54 regions,42 blocks,five images,four captions and three
  independent BASIC examples with25 rows. Preserve intentional IMPUT/grouping
  errors, Korean REM text and seven dotted placeholders; no execution or inferred
  omitted code. Two shared-page advertisements are excluded.49 regional ranges,
 44 text reviews,51 Unicode spans and13 listing reviews validate. Six joins
  connect seven boundaries; all prior pins and byte-identical rebuild pass.
  Next dBASEII article starts155/PDF151; no per-batch browser check is required.
- The dBASEII introductory article spans printed155–158/PDF151–154. Its complete
  package has42 regions,27 blocks,seven images and six captions. Five searchable
  tables retain19 data rows and both printed supply-quantity discrepancies.26
  table-row ranges,35 regional ranges,41 text reviews and48 Unicode spans pass
  validation. Four joins connect eight boundaries. Historical claims, exponents
  and field-name examples remain source readings. All prior pins and the
  byte-identical rebuild pass. PDF155 is the 테크니컬 group divider without
  visible folio; position159 is inferred, not printed. Loader begins160/PDF156.
- 로더란 무엇인가 spans printed160–166/PDF156–162. First six pages are a
  partial package with63 regions,46 blocks,10 original images and eight captions.
  Three independent POKE examples and the complete main PROGRAM LOADER listing
  retain120 physical rows:16 unnumbered,73 numbered and31 wrapped continuations.
  Keep printed code/address discrepancies and ten unresolved quoted-space/glyph
  markers for manual correction. Seven joins,53 regional ranges,53 text reviews,
  66 Unicode spans,23 listing reviews and seven memory-table rows validate.
  Final166/PDF162 contains remaining explanation,figure6,optional shape commands
  and footnotes; restore it next, then assemble all seven pages using the existing
  regional-listing-v1 projection. Preserve the printed interpreter6 reference
  despite its final-page definition5. No per-batch browser check is required.
  Final166 is now restored in a second immutable package:14 regions,12 blocks,
  figure6/caption,three optional commands in four physical rows and six footnotes.
  It adds24 text reviews,27 Unicode spans and one shape ta-/ble column join.
  Completed assembly adds validated unnumbered-row support alongside numbered
  wraps in the opt-in listing projector, without changing either source package.
  All seven pages now provide77 regions,58 blocks,11 images,124 code rows and
  five code groups.66 regional ranges,77 text reviews,93 Unicode spans and27
  listing reviews address complete downloads; source table/footnote indexes
  remain explicitly local.75 PDF tests,prior assembly checks and byte-identical
  rebuild pass. Next 케이-모니터1 begins167/PDF163.
- 케이-모니터1 spans printed167–171/PDF163–167. Its complete PC-8001 package
  has30 regions,21 reading blocks,nine original images and four captions. Preserve
  all85 numbered BASIC lines in86 physical rows,including700's G/OTO720 wrap.
  Three searchable tables provide22 data rows and three headers.21 regional
  ranges,46 text reviews,41 Unicode spans,22 listing reviews and five uncertainty
  markers validate. The r22 table-heading crop was widened once; initial evidence
  remains intact and29 other regions were reused. Flowchart/output-image overlap,
  literal d/m prose,table commas and source code quirks remain explicit. All prior
  pins and byte-identical rebuild pass. Next 기계어 테크닉 begins172/PDF168.
- 기계어 테크닉 연재1회 spans printed172–175/PDF168–171. Its complete
  package has48 regions,35 reading blocks,ten original panels and ten captions.
  Preserve28 ordinal6502 rows,18 ordinalZ80 rows and four numbered BASIC rows
  in three independent listing groups. Machine ordinals are not BASIC line
  numbers. Four memory tables provide19 indexed rows,including visibly blank
  C730 cells. Two prose joins cover three boundaries and retain intervening
  listing content once.38 regional ranges,50 text reviews,103 reading-glyph
  spans,15 listing reviews and two unresolved tiny marks validate. Printed
  byte/address/mnemonic discrepancies and7B/FB disagreement remain explicit
  for manual correction. No OCR retry or crop revision; all prior pins and a
  byte-identical rebuild pass. Next 한글워드프로세서의 설계2 begins176/PDF172;
  inspect its extent and restore at most six source pages per checkpoint.
- 한글워드프로세서의 설계2 spans printed176–191/PDF172–187:16 pages,
  including circuit panels189–191 after the prose conclusion188. Next A/D,D/A
  begins192. First six pages176–181 are a partial package:54 regions,27 blocks,
  eleven original figures and captions,a four-row clock table and two unnumbered
  Z80 example lines. Six joins cover16 column/page boundaries.43 regional ranges,
  59 text reviews,123 reading-glyph spans and eight complete signal-overbar ranges
  validate. Keep printed historical claims,units,wording and signal differences;
  no circuit or code execution certification. Existing regional/listing projector
  preflight and byte-identical rebuild pass. Continue182–187 next,then188–191
  and immutable assembly. All17 extent lookup images are saved for reuse.
- The middle six Hangul wordprocessor pages182–187 are now preserved in a
  second partial package:48 regions,24 blocks,13 figures and captions,two
  binary-counter tables,and five joins across11 column/page boundaries.
  35 regional ranges,40 text reviews,147 Unicode spans and six complete
  overline groups validate. One incomplete marginal mark remains explicit.
  A single r39 crop extension preserves its final2;47 other OCR regions were
  reused. Assembly now accepts fully overlined digits such as F̅8̅;77 PDF tests
  and a byte-identical rebuild pass. Restore final188–191 next,then assemble
  all16 pages with the two source-linked boundary joins. Twelve pages restored
  does not yet mean a complete article. No browser work in this checkpoint.
- Final Hangul pages188–191 are restored:16 regions,8 blocks,five original
  figures,three captions and two joins across three boundaries.11 regional
  ranges,25 reviews,29 Unicode spans and four overline groups validate. All
  sixteen source pages now exist in three immutable packages;next assemble
  using regional-listing-v1 and the two explicit boundary joins. No new OCR
  is needed for assembly;retain local table indexes and all original packages.
- The complete16-page Hangul wordprocessor assembly is readable/sample-reviewed:
  118 regions,57 blocks,29 figures and27 captions. Two boundary joins preserve
  intervening figures/captions;89 regional ranges,124 reviews,299 Unicode spans
  and18 signal groups validate against original and combined bytes. Three
  tables'9 row indexes remain explicitly source-local;global regional ranges
  locate those passages. Original packages and deterministic rebuild match.
  Next verify A/D,D/A의 이론과 실제1 from192/PDF188;no new restoration scope
  or per-batch browser work is implied by this completed assembly.
- A/D,D/A의 이론과 실제1 spans192–199/PDF188–195. First six pages are
  restored:47 regions,30 blocks,ten images/captions,three eight-row tables and
  three formula/example ranges. Four joins cover seven boundaries.37 regional
  ranges,45 reviews and54 Unicode spans validate. Preserve printed numeric
  discrepancies and the duplicate000 row;exclude the recruitment ad on193.
  Next restore198–199 and assemble without a new boundary join.
- Final converter pages198–199 are restored:16 regions,9 blocks,four original
  images,two captions and17 bipolar-code data rows plus header.12 regional
  ranges,28 reviews,29 Unicode spans and two uncertain marks validate. One
  r07 crop extension recovers clipped text;15 cached regions reused. All eight
  pages are ready for regional-prose-v1 assembly without a boundary join.
- The complete eight-page converter assembly is readable/sample-reviewed:
  63 regions,39 blocks,14 images and12 captions.49 regional ranges,73 reviews,
  83 Unicode spans and two tiny-mark uncertainties validate against original
  and combined bytes. Four tables'45 row indexes and three formula ranges stay
  source-local,with global regional ranges provided. All source packages and
  deterministic rebuild match. Next restore TOC-listed competition notice200
  and second competition review201 after verifying their extents.
- Competition notice200/PDF196 and second competition review201/PDF197 are
  complete:32 regions,29 blocks,one publisher-logo image,31 regional ranges,
  29 review notes and48 Unicode spans. Both column joins and all11 submissions
  validate. Historical rules,prizes,names and printed spelling errors remain
  source-linked. No retries or browser work;both fresh rebuilds match.
  Next verify SNAKY GAME from202/PDF198 within the six-page batch limit.
- SNAKY GAME202–207/PDF198–203 is complete:51 regions,42 blocks,five images,
  four captions and two searchable tables with28 indexed rows.148 numbered
  BASIC statements retain282 physical wraps/rows,seven uncertain blank-string
  widths and26 final DATA values.46 regional ranges,45 reviews,33 Unicode spans
  and29 listing reviews validate.13 one-time crop extensions preserve initial
  evidence and reuse38 unchanged regions;fresh rebuild matches. Next verify
  지하괴물잡기 from208/PDF204. No per-batch browser work is required.
- 지하괴물잡기208–212/PDF204–208 is complete:35 regions,29 blocks,five
  images including all four bitmap/photo listing panels.216 numbered statements
  retain242 physical rows;200:CLS is a V= continuation,not a duplicate number.
  64 graphic spans and26 unknown blank widths remain manual-correction markers.
  18 DEFCHR$ definitions retain216 printed hex values without inferred glyph
  mapping.30 regional ranges,123 reviews and116 listing reviews validate.
  Three one-time crop extensions reuse32 regions;fresh rebuild matches.
  Lower212 advertisement excluded. Next verify the dictionary from213/PDF209.
- Dictionary opening213–218/PDF209–214 is restored as a partial article:
  58 regions,48 blocks,three images,55 regional ranges,40 review notes and52
  Unicode spans.37 dictionary entries include the unfinished DEFDBL opening;
  seven column/page joins,68 boxed machine labels,16 color data rows plus header,
  six independent example/output groups and three formula ranges are indexed.
  Literal boxed O,W80,D$/A$,CHR$(47),duplicate 회색 and 열은파란색 remain
  unchanged. Two reverse-field symbols await manual correction. One CHR$ crop
  extension reuses57 unchanged regions;fresh rebuild matches. Ending239 and
  following advertisement240 are verified endpoints,not proof of uninspected
  intervening continuity. Next219–224,then provisional225–230,231–236,237–239,
  followed by source-preserving assembly. No per-batch browser work.
- Dictionary continuation219–224/PDF215–220 is restored:71 regions,62 blocks,
  one original HCOLOR-table image,70 regional ranges,43 review notes and32
  Unicode spans.57 definition fragments,73 machine labels,eight color rows
  plus header,19 command-guide rows,11 independent examples and three formula
  ranges validate. Eight internal joins and incoming DEFDBL 한/다. join are
  proved;following225 starts INT without another boundary join. Printed17
  digits,duplicate HCOLOR2,FRE OI,INKFY$,HTAB14행 and duplicated INST/DEL
  ending remain literal. Four blank widths and one small INPUT separator await
  manual correction. No crop/OCR revision;fresh rebuild matches. Twelve pages
  preserved across two segments;next225–230,then231–236 and237–239,then assembly.
- Dictionary continuation225–230/PDF221–226 is restored:64 regions,52 blocks,
  three original table images,61 regional ranges,47 review notes and30 Unicode
  spans.47 entries,48 machine labels,21 table/header rows,three parameter rows,
  19 literal POKE ranges,two key-notation ranges,17 independent examples and
  three formulas validate. Nine internal joins;no new external boundary join.
  Printed245,TRE(0),MAN,duplicate LOAD wording,NEXT15,line39/30,ABC(),
  POINT−1 1 and differing POKE addresses remain source-linked. PRINT USING
  hash counts checked;key-control bytes remain unverified. No OCR revisions;
  fresh rebuild matches. Eighteen pages preserved,next231–236 then237–239,
  followed by assembly and issue closeout. No per-batch browser work.
- Dictionary continuation231–236/PDF227–232 is restored:69 regions,63 blocks,
  one original REPT image,68 regional ranges,52 review notes and70 Unicode
  spans.57 entries,61 machine labels,19 independent examples,three formulas,
  three POKE ranges and six key notations validate. Five internal joins;no new
  external definition join. REPT24/8 cross-mark rows remain indexed beside
  the source image. Two TI$ HOME graphics are source-local correction markers;
  no control bytes inferred. Printed RNA(0),GAVE/GAME,SGN X=1,REM comma,
  DATA trailing period and historical claims remain literal. One READ crop
  extension restores the final sentence;68 cached regions reused. Fresh rebuild
  matches. Twenty-four pages preserved;next final237–239/code tables,then
  assembly and issue closeout. No per-batch browser or reader staging.
- Final dictionary237–239/PDF233–235 is restored:28 regions,21 blocks,six
  original table images,five captions,22 regional ranges,25 review notes and52
  Unicode spans. Six final definitions,seven machine labels,two independent
  examples and two WAIT formulas remain literal. Five tables contain166 data
  rows plus six physical headers,618 nonblank cell ranges and two blank cells.
  Table3 repeats96;table5 preserves161→255 and222→255;caption5 says16 and
  final prose says TAB.64 source-cell graphic markers defer uncertain ink
  symbols and position-dependent PET bitmaps without inferring their bytes.
  ASCII prose joins237 to239 across the intervening tables. Shared laser-book
  advertisement excluded;following240 advertising confirms the ending. All27
  pages now verified;fresh rebuild matches,no OCR retries. Next assemble five
  immutable segments with one DEFDBL join and all local correction indexes.
- The complete27-page dictionary is assembled from five immutable segments.
  290 regions yield245 blocks,14 images and five captions.276 regional ranges,
  207 review notes,236 Unicode spans and73 uncertainty markers are projected
  into article.txt;69 markers are graphic and four are blank-width text notes.
  Thirty original joins remain and DEFDBL 한/다. is joined once.203 definitions
  retain204 original fragments;257 labels,219 table/header rows,55 examples,
  14 formulas and all cell/key/POKE/guide indexes remain explicitly local in
  original corrections/metadata. Both source and combined ranges validate.
  Regional assembly now accepts explicit graphic markers with matching unresolved
  text evidence and rejects inferred bytes;existing glyph checks remain strict.
  All79 PDF tests and a fresh byte-identical rebuild pass;9,973 prior files and
  all five embedded packages are unchanged. No new OCR or browser work. All37
  articles are readable/sample-reviewed;two group-heading decisions and issue
  reconciliation,standalone reference/report and reader acceptance remain.
- Final heading classification is complete. 공모입선작0033 groups the two
  restored prize-winning games;정보모음0037 groups six distinct articles at
  printed17,105,108,111,200,201. Both canonical pageless section identities and
  child links remain unchanged;neither owns an additional body or invented
  standalone divider page. All43 canonical entries pass full ownership/accounting
  checks:37 readable/sample-reviewed articles,six groups,no unresolved eligibility.
  All37 article records and11,153 prior-file pins are unchanged. Next is issue
  closeout,with standalone reference/report and staged reader acceptance.
- Standalone reference checkpoint is complete at
  `build/pdf-restoration/12-1984-02-reference`. All37 immutable packages reconcile
  with43 TOC entries and six groups.6,817 copied package files,including62
  correction files across assembled/original segments,remain byte-identical.
  Source identity,page geometry and full-article coverage match the saved ledger.
  All4,346 local links,111 fragments and37 previous/next routes pass static checks;
  a fresh export reproduces all6,859 output files.11,157 prior-file pins remain
  unchanged. No new OCR,pipeline changes,reader staging or browser work.
  One validation-script retry normalized string/integer printed-page labels;
  no source content was changed. Reading-room integration/acceptance remains a
  separate closeout stage;static link checks do not claim browser acceptance.
- February issue closeout is complete. Combined reader
  `build/reading-room-pdf-february` preserves50,313 baseline files,all3,421 prior
  article records and all6,817 February package files. Only the four expected
  baseline catalog/search/February issue/media documents change.145 cover assets,
  149 covered issues and145 TOC scan sets/239 pages/478 derivatives are preserved.
  The inherited checklist's149 TOC-set count was corrected against PLAN-tocs.md;
  the baseline/data were unchanged. All37 rendered article routes,193 literal code
  blocks,1,711 region links and six group routes pass. Desktop/mobile,actual
  text/listing/scan downloads,correction access,TOC zoom,search,November/CD routes
  and nested hosting pass;79 PDF,56 reader and15 frontend tests plus production
  build pass. Completion evidence is in the matching private closeout directory
  and `build/pdf-restoration/12-1984-02-closeout`. No new OCR or pipeline changes.

### Requirements for remaining issues

- Reconcile each issue, produce its JSON index/report, and validate its article
  packages and extracted assets before starting the next issue.
- Keep advertisements, unlisted material, and 1995 article bodies outside the
  extraction queue. Keep unresolved classification and source-label conflicts
  visible rather than inflating restoration totals.

**Artifact/check per batch and issue:** the same outputs/checks as step 11, with
an issue progress entry. **Milestone check:** all 828 current TOC entries are accounted
for (839 in the initial snapshot; corrected by the owner after step 11); each eligible
article has an outcome and the two 1995 sources remain cover-only. Report actual
usable coverage separately from complete queue accounting.

## 13. Reconcile the complete JSON and asset collection

**Goal:** deliver a consistent collection ready for downstream use.
**Input and limit:** completed issue packages/reports, cover ledger, and existing
CD references; aggregation only, with no new restoration or UI features.

- Reconcile manifests, source hashes, identities, TOC membership, outcome totals,
  review coverage, covers, and links across the 19 eligible issues.
- Build an aggregate JSON index and file/hash manifest referencing completed
  issue indexes, article packages, corrections, and assets. Preserve existing
  packages and CD data; do not install or replace reading-room data.
- Confirm no 1995 article records were added. Account for available 1995 cover
  assets without inventing canonical TOC or CD issue associations.

**Artifact/check:** a validated JSON/asset collection and coverage report
distinguishing usable results, unresolved eligibility, and restoration gaps.
All local references resolve and hashes match; repeated exports reproduce content
apart from declared volatile metadata. Existing CD records and bytes remain intact.

## 14. Complete regression checks and handoff

**Goal:** deliver a usable, documented pass with honest limits.
**Input and limit:** the full export and accumulated checkpoint evidence;
final regression and documentation, not a new recovery campaign.

- Run the focused pipeline, schema, package and asset checks introduced above.
  Use synthetic fixtures in ordinary tests and keep real scans/OCR outside Git.
- Check representative literal code/whitespace, correction byte ranges, source
  evidence, image integrity and cover metadata directly from data and image files.
- Document preparation, resume, export, validation commands, required private
  inputs, output locations, and known limits. Update README and successor notes.
- Record final TOC accounting, eligible articles, availability/review totals,
  gaps, extracted covers, validation, and deferred tasks in PROGRESS-PDF.md.

**Completion:** the pilot/sample quality gates passed; every eligible article has
an explicit outcome; unresolved eligibility is separately reported; all usable
results and available image/cover assets are indexed in the validated JSON
collection with provenance and correction records. No renderer or reader is
required to complete this plan. Report restoration
coverage rather than claiming every article was recovered. Full proofreading,
cloud OCR, advertising restoration, TOC expansion, full-text search, ownership
features, and public deployment remain deferred. HTML rendering and reading-room
delivery are separate tasks consuming this data collection.

## Completed checkpoint: remove HTML dependencies from data delivery

Completed 2026-10-03. Article export, segment assembly, batch-reviewed export
and issue closeout now default to JSON/assets without HTML. Explicit `--preview`
retains optional historical rendering for separate use. All 82 PDF tests pass;
a JSON-only sample issue rebuilds identically, and all 72 completed November/
February article packages pass read-only preservation checks. March 1984's first
bounded Tesseract/restoration batch is now complete. The requirements below are retained
as the completed checkpoint's scope.

**Goal:** make the existing tools satisfy the clarified scope before March 1984.
**Input and limit:** existing build/assembly/batch/issue export and validation
code, plus synthetic fixtures and already completed package evidence. One bounded
compatibility checkpoint; no new OCR, article restoration, or renderer redesign.

- Separate JSON/asset validation from preview validation. Currently `build.py`
  requires `index.html` in `check_export`, `assemble.py` compares generated HTML,
  and `issue.py` generates a rendered issue reference. Check their callers too.
- Make PDF data delivery and issue closeout work without generating HTML/CSS or
  invoking reader/frontend tools. Preserve existing package schemas, stable IDs,
  raw OCR, corrections and assets; retain old rendered artifacts unchanged.
- Reuse focused fixtures to demonstrate export, assembly, resume and closeout
  with no HTML present. Document the data-only commands and successor checkpoint.

**Artifact/check:** focused passing data tests and a JSON/asset-only sample issue
index/report, with package preservation checks. Update PROGRESS and commit before
starting March extraction. The 2026-10-03 implementation completes these gates;
the earlier scope revision alone did not implement the tooling changes.
