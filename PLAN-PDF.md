# Step-by-step PDF restoration plan

Storage update, 2026-10-16: follow the [successive-issue workflow](docs/STORAGE.md#successive-restoration)
for new work. Keep unfinished batches, raw OCR, corrections, recipes and review
evidence under `archive/pdf/YYYY-MM/`; preserve them after issue closeout too.
Use a fresh destination for each revision. Older dated paths below remain valid
through compatibility links and do not change the retention policy.

Session wrap-up, 2026-10-28: keep disposable comparison exports under
`work/validation/`, scratch renders under `work/tmp/`, and reader integration
stages under `work/reading-room/`. Retain comparison reports and unique restoration
evidence in `archive/`. After saving the checkpoint and finishing processing,
preview with `make clean-session`; delete with
`make clean-session CLEAN_ARGS=--apply`. See [cleanup scope and optional flags](docs/STORAGE.md#session-cleanup).

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

## March 1993 restoration, 2026-11-03

The full March 1993 issue goal is active. Batch 01 initializes all 52 canonical
TOC identities and verifies the 433-page source and pinned Tesseract runtime.
Column 0005, 컬럼 마소쉘 : 정보산업은 기간산업이다, is readable/sample-reviewed
on PDF 100–101, individually observed printed 98–99. Its 82 JSON/assets files
match two exports and a fresh-process rebuild. All twenty source crops, eighteen
selected OCR outcomes, 275 typed ranges and 173 reading rows validate. Four section
headings, original portrait/series artwork, independent pull quotation, separate
closing paragraph, four contributor rows and four continuation boundaries remain.
One paused/resumed source correction pass used eighteen initial recognitions plus
four changed-crop recognitions; fourteen unchanged raw/TSV results were reused,
with original execution provenance and zero unchanged-input retries. All crop/map
revisions and a copied declaration-year clarification are retained. Fresh 213 PDF
tests pass; all 13,097 December reference files and thirty core modules are exact.

Batch 02 preserves feature 0001 opening PDF 156–161 as an immutable partial native:
220 independently/fresh-process exact files, 59 exact crops, 51 selected outcomes,
655 valid typed ranges and 339 reading rows. Eight original images, two complete
tables/twenty data cells/six header fragments, 24 diagram-label rows, six caption
associations and eight internal continuations remain explicit. Source ending 172
is observed, without claiming unreviewed intervening continuity. Independent PCI
sidebar 161 interrupts main prose 160→162; their contexts remain separate. One
source pass used 51 initial recognitions plus one changed-heading recognition
before correction; fifty exact raw/TSV results retain original execution provenance,
with zero unchanged-input retries. All revisions remain retained; nine custom-data
mutations are rejected. All 13,179 earlier reference/package files remain exact.

Batch 03 preserves continuation 162–167 as native b: 196 independent/fresh-process
exact files, fifty exact crops, 46 selected outcomes, 757 valid ranges and 431
indexed text rows. Eleven headings, three complete diagrams, nine table cells/
three headers, 67 diagram-label rows, four numeric labels and eight continuation
boundaries retain source contexts. Both original incoming 160→162 native contexts
validate across sidebar 161. Lower 163 recruitment notice is excluded; first/second
sections end 163/167 with no prose joins into 164/168. Source title 164 adds 내부
without changing child 0003's canonical title. All twelve pages 156–167 are now
preserved across a/b. One source pass, 46 initial plus three changed-crop calls,
43 exact reused raw/TSV outcomes and zero unchanged-input retries. Nine invalid
custom-data cases are rejected; all 13,399 prior files and thirty core modules
remain exact. First two intrinsic section bodies are preserved; assembly is pending.

Batch 04 preserves final section 168–172 as native c: 201 independent/fresh-process
exact files, 54 exact crops, 46 selected outcomes, 912 ranges, eight original panels,
three charts/24 values, eighteen specification fields and two literal DOS fragments/
ten nonempty rows. One paused/resumed source pass; 46 initial plus three changed
recognitions, 43 exact reused raw/TSV outcomes, zero unchanged-input retries.
All seventeen body pages 156–172 are preserved across a/b/c; actual parent assembly
and final child anchors remain required. Printed chart 4.183 versus prose 4183,
chip/time-unit/ratio/cache claims and wording stay literal. Nine invalid custom-data
cases rejected; all 13,595 prior files and thirty core modules remain exact.

Batch 05 actually assembles the readable parent on 156–172: 626 exact files from
three independently regenerated natives/617 files and a fresh-process rebuild.
All 163 crops, 118 reading blocks, twenty original images, 143 outcomes, 2,324
projected metadata ranges and 4,484 current typed occurrences validate. Main 160→162
joins across independent PCI sidebar 161; two section boundaries and all source
blocks/listing bytes remain intact. Child 0002 is a final non-owning anchor 157/155.
Nine rehashed assembly/child cases rejected; no new OCR/source correction. All
13,796 prior files and thirty core modules remain exact; 213-test result retained.

Batch 06 finalizes children 0003/0004 as non-owning references at assembled
headings 164/168, printed 162/166. All three feature child anchors are final.
Five classification files reproduce exactly in independent/fresh-process exports;
ten parent-relative ranges and nine invalid ownership/anchor cases validate.
Source 164 adds 내부 beyond the canonical contents title; both forms remain.
The frozen parent pending-child notes have an external current disposition;
all 626 parent files and source-fidelity limits remain unchanged. No new OCR or
source correction; all 14,422 prior files and thirty core modules remain exact.

Batch 07 classifies group 0006 as non-owning and preserves copyright article 0007
opening 140–145/138–143 as a partial native: 239 independently/fresh-process exact
files, sixty exact crops, 57 outcomes, 1,037 native/group ranges and 653 reading rows.
Three original images, three independent pull quotations, fifteen headings, three
party rows/six labels, eleven citations, eleven command tokens, eight circled markers
and seventeen continuations remain explicit. One source pass used 57 initial plus
three pre-correction and one within-pass changed recognition; two title crops were
refined afterward with saved text unchanged. Total 63 calls, 55 exact final reused
outcomes with actual execution origins, zero unchanged-input retries. Nine invalid
custom-data cases rejected; all 14,427 prior files and thirty core modules exact.
Actual seven-page extent 140–146 observed; final 146 and actual assembly pending.

Batch 08 preserves final 146 as native b and actually assembles copyright article
0007 on 140–146/138–144: 291 exact files from two independently regenerated natives/
283 files and a fresh-process rebuild. All 69 crops, 66 outcomes, 1,218 projected
metadata ranges, 2,364 current typed occurrences and 775 rows validate. One direct
145→146 prose join retains both original contexts. Three independent quotations
stay separate; quotation 145 and main prose 146 retain differing wording. Eighteen
headings, three party rows, eleven citations/command tokens, eight circled markers
and nineteen internal continuations remain indexed. Final-page native b adds nine
initial calls, one source pass and zero retries after four pre-OCR crop changes.
Nine rehashed assembly and two ownership mutations are rejected; all 14,667 prior
files and thirty core modules remain exact. Prior fresh 213-test result retained.

Batch 09 verifies Macworld article 0008's actual eight-page body 174–181 and
preserves opening 174–179/printed 172–177 as a partial native: 165 independently/
fresh-process exact files, 49 exact crops, thirteen original images, 36 outcomes,
922 ranges and 496 physical rows. Six captions/eleven figure associations, six
CD-ROM cover panels, three presenters, four headings and seventeen reading
boundaries retain source contexts. All 36 drafts were read before one source pass;
zero retries or post-pass changes. Eleven pre-OCR events across nine original
regions remain in three maps. Printed software/grammar/bit-depth/age/price claims
stay literal. Nine invalid custom-data cases are rejected; all 15,002 prior files
and thirty core modules remain exact. Final 180–181 and actual assembly pending.

Batch 10 preserves final Macworld 180–181 and actually assembles all eight pages:
282 exact r02 files from two independently regenerated natives/274 files and a
fresh-process rebuild. All 75 crops, 61 outcomes, 1,542 metadata projections, 3,028
current ranges and 710 physical rows validate. One 179→180 prose join retains both
original contexts and nine intervening graphic items. Fourteen images, seven
caption blocks/twelve associations, six covers, three presenters, 21 courses,
six contacts/27 rows and four phone/fax occurrences retain source contexts.
Final native b adds 25 initial calls after one pre-OCR fax repair, one source pass
and zero retries/post-pass changes. R01's semantic audit caught caption block IDs
in figure.caption text fields; r02 resolves twelve current captions from verified
literal ranges. Only six root JSON files change; all native, article-text, asset
and raw-ZIP bytes remain exact. Nine rehashed assembly/two ownership mutations
are rejected; all 15,167 prior files and thirty core modules remain unchanged.

Batch 11 completes Nintendo article 0009 on PDF 182–184/printed 180–182:
142 independently/fresh-process exact files, 35 exact crops, 33 OCR outcomes,
521 typed ranges and 268 physical rows. Two headings, two three-point arguments,
fourteen contour-following reading rows, original illustration/category artwork,
independent pull quotation and closing acknowledgment remain explicit. Lower 184
book-year campaign is excluded. The same checkpoint preserves health article 0010
opening 188–190/printed 186–188 as a 117-file partial: 28 exact crops, 27 outcomes,
436 ranges, 289 rows and seven headings. Its full compound extent is 188–196:
main 188–193 by 오형태, then uncredited editorial stretching guide 194–196,
잠깐! 10분만 쉽시다. The opening editorial deck promises that guide; no author is
invented for it. Both independent quotations stay outside main prose joins.
All sixty drafts were read before one source pass; sixty initial calls, zero
retries or within-pass/post-pass changes. Thirteen pre-OCR events repair twelve
original regions. Nine rehashed native cases and two ownership cases are rejected;
all 15,840 prior files and thirty core modules remain exact. Prior fresh 213-test
result retained. Final health 191–196 and actual nine-page assembly remain next.

Batch 12 preserves final health PDF 191–196 as a 376-file native, then actually
assembles all nine pages 188–196/printed 186–194. The 501-file r02 assembly reproduces
from both independently regenerated natives/493 files and in a fresh process.
All 135 exact crops, 114 outcomes, 1,503 metadata projections, 2,892 current ranges/
2,792 native occurrences and 750 physical rows validate. Authored main 188–193 and
uncredited editorial guide 194–196 remain distinct; no 190→191 cross-native prose
merge. Four independent quotations, 36 headings, 27 numbered entries in ten guide
groups, twenty guide images and the final posture panel retain source contexts.
Final native adds 87 initial plus three pre-correction changed-input recognitions;
84 exact raw/TSV results retain original execution provenance. All ninety drafts
read before one source pass; zero unchanged-input retries or within-pass/post-pass
changes. Twenty-four pre-OCR repairs and three faint bottom-row extensions remain.
R01's semantic audit caught native IDs in figure-region and intervening-item
references. R02 fixes twenty guide and four boundary references; only six root JSON
files differ. Article text, raw ZIP, all 493 native files and assets remain exact.
Nine rehashed root cases and two ownership cases are rejected. All 16,099 prior
files and thirty core modules remain unchanged; prior fresh 213-test log retained.

Batch 13 completes canonical competition notice 0011 on PDF 134–135 as a
115-file native, reproduced independently and in a fresh process. Both source
folios remain null; original contents reference 132 is retained separately.
All 29 exact crops, 26 outcomes, 248 typed ranges and 39 source rows/fragments
validate. Two original full-page compositions and the award panel preserve the
graphic design; nine numbered sections, four ranked award rows/eight cells,
a separate common-award span, counts 1/2/4/4 and three contact rows remain indexed.
Issuer is not an invented byline. Canonical and printed spread-title forms differ
and remain separate. This explicitly TOC-listed publisher announcement is eligible;
it does not authorize unrelated advertising extraction.
Pageless category 0012, 원리구현, is now non-owning from contents 4 and the repeated
banner on 198. Its two evidence files reproduce independently/fresh-process; the
category crop is exact. All seven child links remain; no group body/folio or child
restoration is invented. All 26 drafts read before one source pass; ten pre-OCR
repairs, zero retries or within-pass/post-pass changes. Nine rehashed notice,
three group and two ownership mutations are rejected. All 17,477 prior files and
thirty core modules remain exact; prior fresh 213-test result retained.

Batch 14 verifies Huffman article 0013's full eleven-page extent, PDF 198–208,
and preserves opening 198–203/printed 196–201 as a 332-file partial native.
Independent and fresh-process exports match. All 96 crops, 76 OCR outcomes,
5,600 typed ranges and 536 indexed source rows/fragments validate. Twenty original
images retain ten diagrams, four printed tables, worked examples and an independent
Modified Huffman sidebar. Twelve table/array indexes preserve 1,189 cells; the
worked matrix adds 64 cells. Nine array occurrences keep explicit values, circled
annotations and ellipses; no omitted values are expanded. The AC table retains
43 printed rows, nine blank cells and fifteen dot separators. Seven prose boundaries
include main 201→203 across table page 202. Source bit-string, caption, formula and
array-label/count differences remain literal. All 76 drafts read before one source
pass; six pre-OCR margin changes, zero retries, one within-pass saved-caption
refinement and zero post-pass changes. Twelve rehashed native and two ownership
cases are rejected. All 17,594 prior files and thirty core modules remain exact;
prior fresh 213-test result retained. Final 204–208 and actual assembly remain pending.

Batch 15 preserves final Huffman PDF 204–208 as a 125-file native and actually
assembles the complete eleven-page article 198–208/printed 196–206. All 466 files
match an export consuming both independently regenerated natives/457 files and a
fresh-process rebuild. All 134 crops, 102 outcomes, 14,285 projected metadata ranges,
28,476 current range occurrences and 1,036 indexed source rows/fragments validate.
One 203→204 prose merge crosses diagrams 8–10 and preserves both original contexts.
Nine internal prose boundaries, independent table page 202 and the Modified Huffman
sidebar remain explicit. Thirty-two original images retain fourteen diagrams,
four printed tables, worked examples, a source photograph and seven code panels.
Twenty printed-caption associations contain literal display text; 1,189 table cells
and 64 matrix cells retain their exact source occurrences. Listing 1 preserves all
379 numbered rows, 53 blank numbered rows, 1,968 tokens, twelve functions, twenty
array declarations, four string literals and twelve comment rows, including eight
Korean rows. Printed number/colon columns and source defects remain; no code repair
or execution is claimed. Final native adds 26 initial recognitions, one source pass,
four pre-OCR margin events across two columns and zero retries or within/post-pass
changes. Metadata-only native r02 fixes one explanatory note; transcript/assets/raw
ZIP bytes remain exact. Twelve rehashed assembly, six native and two ownership cases
are rejected. All 17,926 prior files and thirty core modules remain exact; earlier
fresh 213-test result retained. Both immutable natives retain historical partial scopes.

Batch 16 verifies popup-window article 0014's actual eleven-page extent, PDF
210–220, and preserves opening 210–215/printed 208–213 as a 385-file partial native.
Independent and fresh-process exports match. All 103 crops, 91 outcomes, 6,079 typed
range occurrences and 604 nonempty reading rows validate. Twelve original images
retain table 1, three boxed examples, stack/heap fragments, an ending ornament and
three listing panels. Five captions use literal display text; other captions are
null. Ten table rows/twenty cells, nine style entries, eight field groups, eleven
API signatures and three illustrative fragments retain their source occurrences.
Six independent code contexts contain 326 physical rows. Listing 1's opening has
211 numbered rows, 26 blank numbered rows and six unnumbered wraps; duplicate 67
and absent 68 remain literal. Five prose boundaries and the heap comment 213→214
retain source contexts. All 91 drafts read before one source pass; nine English
code regions and 82 Korean/English text regions, one pre-OCR crop repair and zero
retries or within-pass/post-pass changes. Thirteen rehashed native and two ownership
cases are rejected. All 18,642 prior files and thirty core modules remain exact;
earlier fresh 213-test evidence retained. Later 216–220 and actual assembly pending.

Batch 17 preserves final popup-window PDF 216–220 as a 77-file native, then
actually assembles all eleven pages, 210–220. The 471-file assembly reproduces
from two independently regenerated natives/462 files and in a fresh process.
All 129 crops, 105 outcomes, 19,420 projected metadata ranges, 39,772 current range
occurrences and 1,400 nonempty reading rows validate. Eight code contexts retain
three boxed examples, stack/heap fragments and three numbered listings. All 974
numbered rows (345/431/198), 119 blank numbered rows and 37 physical wraps remain;
listing 1 retains duplicate 67 and absent 68. Twenty-four original images, fifteen
code panels, seven literal captions and twenty table cells retain their contexts.
Twenty explicit MVcur initializer values remain separate from MENUMAX 32; no
values are expanded. Listing 1's 211→212 boundary preserves native bytes without
a prose merge. Final native adds fourteen initial plus one within-pass changed-crop
recognition; thirteen exact raw/TSV outcomes retain original execution provenance.
One source pass, five pre-OCR margin repairs, one within-pass initializer repair,
zero unchanged-input retries or post-pass changes. Native r02 fixes seven function
occurrence roles; four JSON files change, all transcript/assets/raw-ZIP bytes exact.
Twelve rehashed root, six native and two ownership cases are rejected. All 19,027
prior files and thirty core modules remain exact; earlier fresh 213-test log retained.
Original native partial scopes remain historical. Main prose ends 214, listings end
216/219/220; lower 220 publisher notice is excluded and folio 220 remains null.

Batch 18 verifies puzzle-game article 0015's actual fifteen-page extent, PDF
222–236, and preserves opening 222–227/printed 220–225 as a 261-file partial native.
Independent and fresh-process exports match. All 78 exact crops, 58 outcomes,
5,768 typed range occurrences and 546 nonempty reading rows validate. Twenty
original images retain three diagrams, fourteen code panels, category/series art
and ending ornament. Four printed captions use literal text; sixteen are null.
Twelve grid cells, 42 diagram labels, 49 explicit initializer pairs/98 cells,
nine struct contexts/47 field groups and eleven function occurrences retain their
own source ranges. Nine independent code contexts contain 316 physical rows;
listing 1 preserves 187 four-digit number/colon rows, seven blank numbered rows
and one physical string wrap at 175. Printed defects and PCX example/listing
variants remain literal; no code repair or execution. All 58 drafts read before
one source pass; fourteen English code regions, 44 Korean/English regions,
seven pre-OCR margin events across five regions and zero retries or within/post-pass
source changes. Metadata r02 removes a Korean identifier from the comment index;
four JSON files differ, all transcript/assets/raw-ZIP bytes exact. Fifteen rehashed
native and two ownership cases are rejected. All 19,652 prior files and thirty
core modules remain exact; earlier fresh 213-test evidence retained. Main prose
ends 226; listing 1 ends 236 at 1415 before independent advertising. Pages 237/238
confirm the boundary; prepared 239 was not reviewed. Later 228–236 and actual
fifteen-page assembly remain required.

Batch 19 preserves puzzle-game listing 1 on PDF 228–233/printed 226–231 as a
69-file middle native. Independent and fresh-process exports match. All 24 exact
crops, twelve outcomes, 17,555 typed range occurrences and 913 physical rows
validate. All 883 numbered rows 0188–1070 retain their four-digit number/colon
columns, 21 blank numbered rows and thirty unnumbered physical continuations.
Twelve original panels have null captions. Forty-one function headers, table[4]
and KJS[8]'s twelve explicit values, two union fields, eight case labels and 31
macro-glyph occurrences retain their own source contexts. The wrapped string 0287,
blank payloads 1017/1031 followed by getimage wraps, numbered 0620/0621 fragments,
PLT/PUT and X/N candidates, RED::BLUE, divisior and message variants stay literal;
no code repair or execution. Both original native contexts at 0187→0188 validate
without claiming an actual assembly. All twelve initial English drafts read before
one source pass; two pre-OCR margin events on one region and zero retries or
within/post-pass source changes. Fifteen rehashed native and two ownership cases
are rejected. All 20,174 prior files and thirty core modules remain exact; earlier
fresh 213-test evidence retained. Opening and middle now preserve 222–233 across
two natives/330 files; actual fifteen-page assembly and final 234–236 remain pending.

Batch 20 preserves final puzzle-game PDF 234–236 as a 39-file native, then
actually assembles the full fifteen-page article, 222–236. The 378-file assembly
reproduces from three independently regenerated natives/369 files and in a fresh
process. All 114 exact crops, 76 outcomes, 29,757 metadata projections, 60,940 current
range occurrences/60,832 source occurrences and 1,816 reading rows validate.
Nine code contexts retain eight illustrative fragments and listing 1. All 1,415
numbered rows preserve four-digit number/colon columns, 37 blank numbered rows and
43 physical wraps; original 0187→0188 and 1070→1071 contexts remain without prose
merges. Thirty-eight original images retain three diagrams, 32 code panels,
category/series artwork and ending ornament; four captions are literal text,
34 are null. Twelve grid cells, 42 diagram labels, 49 explicit pairs/98 cells and
twelve table/KJS values remain indexed. All 59 function occurrences, 16 key cases,
eight sound cases and source variants retain their contexts. Two wrapped strings
and 115 complete quoted occurrences remain literal; no code repair or execution.
Final native adds six initial English calls, one source pass and zero crop changes,
retries or within/post-pass changes. Twelve rehashed root, six native and two
ownership cases reject. All 20,243 prior files and thirty core modules remain
exact; earlier fresh 213-test evidence retained. Main prose ends 226; listing ends
236 at 1415 above an excluded book advertisement. Folios 220–234 are individually
observed across the article; 237 is advertising and 238 opens the distinct Turbo C
article. Original native partial/deferred scopes remain historical.

Batch 21 verifies Turbo C article 0016's actual ten-page extent, PDF 238–247,
and preserves opening 238–243/printed 236–241 as a 327-file partial native.
Independent and fresh-process exports match. All 93 exact crops, 75 OCR outcomes,
3,062 typed range occurrences and 492 nonempty reading rows validate. Eighteen
original images retain five memory diagrams, eleven code panels, the linker table
and category artwork; five captions are literal text and thirteen are null.
The linker map retains nine rows/45 cells/five headers; 84 diagram labels retain
individual occurrences. Ten independent code contexts preserve 58 physical rows,
559 tokens, eight commands, eighteen instruction rows, thirteen registers, eight
flags and 128 explicit dump-byte occurrences. Loaded DEBUG 242→243 remains separate
from copied-file DEBUG 243. Nine prose boundaries, one code boundary and the separate
sidebar's formula/four points retain source contexts. All 75 drafts were read before
one source pass: eleven English code regions, 64 Korean/English regions, zero retries
or within/post-pass source changes. Initial schema error and pre-OCR margin/map
revisions remain retained. Source wording, historical claims, addresses and segment
differences stay literal; no code repair or execution. Fifteen rehashed native and
two ownership cases reject. All 20,660 prior files and thirty core modules remain
exact; earlier fresh 213-test evidence retained. Final 247 closes above excluded
book advertising; 248–249 are advertisements and 250 opens the distinct Unix article.
Final 244–247 and actual ten-page assembly remain required.

Batch 22 preserves final Turbo C PDF 244–247 as a 196-file native, then actually
assembles the complete ten-page article 238–247/printed 236–245. All 532 files match
an export consuming two independently regenerated natives/523 files and a fresh-process
rebuild. All 151 exact crops, 118 outcomes, 4,916 metadata projections, 9,738 current
range occurrences/9,598 source occurrences and 763 reading rows validate. Thirty-three
original images retain six memory diagrams, twenty-two code panels, three tables,
category art and ending ornament; nine captions are literal text and 24 are null.
Three tables retain 93 cells/twelve headers; 93 diagram labels, the independent
sidebar's formula/four points and thirteen prose boundaries retain source contexts.
Twenty-one independent code contexts preserve 145 physical rows, 1,063 tokens,
twenty comment/header rows, six quoted literals, 29 indexed instruction rows,
ten commands, thirteen registers, eight flags and 128 explicit dump-byte occurrences.
PSP structure retains seven fields; two C listings preserve their printed forms.
No cross-native prose merge, source repair or code execution. Final native adds
43 initial recognitions, eleven English and 32 Korean/English, after all drafts
were read before one source pass. Zero retries or within/post-pass changes; pre-OCR
map/crop revisions and two helper failures remain retained. Printed 52/512,
setargv/serargv, wording, addresses and opcode differences stay literal. Twelve
rehashed root, six native and two ownership cases reject. All 20,987 prior files
and thirty core modules remain exact; earlier fresh 213-test evidence retained.
Final 247 closes above excluded book advertising; 250 is the distinct Unix opener.
Original native partial scopes remain historical.

Batch 23 verifies Unix article 0017's actual nine-page body, PDF 250–258,
and preserves opening 250–255/printed 248–253 as a 421-file partial native.
Independent and fresh-process exports match. All 130 exact crops, 94 OCR outcomes,
3,189 typed range occurrences and 454 nonempty reading rows validate. Thirty-six
original images retain 29 code panels, two tables, three diagrams, key flow and
category/series artwork; six captions are literal text and thirty are null.
Two tables preserve 37 explicit cells/eight header fragments; fifty diagram labels
retain separate occurrences. Twenty-eight independent code contexts preserve
148 physical rows, 43 numbered Listing 1 rows, three blank numbered rows, 957 tokens,
36 comment rows, four quoted literals, four commands and ten printed output pairs.
Eight structures retain 38 field groups; nine API prototypes, 22 includes and nine
conditions remain literal. Split ipc_perm keeps seven fields; union semun retains
only two current fields and continues on 256. Five prose boundaries and one code
boundary retain source contexts. All 94 drafts were read before one source pass:
29 English and 65 Korean/English regions, zero retries or within/post-pass changes.
Seventy-two pre-OCR crop events and the failed pre-recognition launch remain retained.
Metadata r02 clarifies the table-2 header note; only four JSON files differ from
retained r01. All source text, images and raw ZIP bytes remain exact. Source spelling,
header/pointer differences and filename candidates remain; no code repair or execution.
Seventeen rehashed native and two ownership mutations reject. All 21,715 prior files
and thirty core modules remain exact; prior fresh 213-test evidence is retained.
Final 258 closes above excluded publisher advertising; 259 is an advertisement,
260 the distinct DOS opener. Final 256–258 and actual nine-page assembly remain required.

Batch 24 preserves final Unix PDF 256–258 as a 181-file native, then actually
assembles the complete nine-page article 250–258/printed 248–256. All 611 files match
an export consuming two independently regenerated natives/602 files and a fresh-process
rebuild. All 185 exact crops, 133 outcomes, 5,421 metadata projections, 10,759 current
range occurrences/10,583 source occurrences and 658 reading rows validate. Fifty-two
original images retain 43 code-panel associations, two tables, four diagrams, key flow,
category/series artwork and ending ornament; eight captions are literal text and 44 null.
Two tables preserve 37 cells/eight headers, and 55 diagram/flow labels retain separate
occurrences. Forty independent code contexts preserve 282 physical rows, 151 numbered
rows across Listings 1/2, seventeen blank numbered rows, 1,734 tokens, 51 comment rows,
fourteen quoted literals, nine commands and twelve printed output rows. Thirteen API
prototypes, 31 includes, fourteen conditions and five function-definition candidates
remain literal. Complete union semun metadata links two fields on 255 to the array
field/closing brace on 256. Main prose 256→258 crosses independent Listing 2 on 257;
seven prose and three code boundaries retain source contexts. No cross-native prose
merge, source repair or execution. Final native adds 39 initial recognitions, fourteen
English and 25 Korean/English, after all drafts were read before one source pass.
Zero retries or within/post-pass changes; 39 pre-OCR crop events and helper/audit failures
remain retained. IPC_GETALL/IPC_SETALL, shm_nattach/shm_cnattach, spaced operators,
broken-bar candidates and printed Hello,World output stay literal. Twelve rehashed
root, eight native and two ownership mutations reject. All 22,557 prior files and
thirty core modules remain exact; prior fresh 213-test evidence retained. Final 258
closes above excluded publisher advertising; 259 is an advertisement, 260 the distinct
DOS opener. Original native partial scopes remain historical.

Batch 25 verifies DOS article 0018's actual thirteen-page body, PDF 260–272,
and preserves opening 260–265/printed 258–263 as a 307-file partial native.
Independent and fresh-process exports match. All 82 exact crops, 72 OCR outcomes,
3,201 typed range occurrences and 495 nonempty reading rows validate. Ten original
images retain portrait/category artwork, three listing panels, two tables and three
formulas; five captions are literal text and five null. Three independent assembly
procedures preserve 131 physical rows, 119 numbered rows, 28 blank numbered rows,
twelve unnumbered comment wraps, 438 tokens, 64 comment rows, 76 instruction rows,
84 register occurrences, 21 immediate occurrences, nine memory operands and eighteen
branches/calls. Table 1 retains fourteen explicit cells/three headers and four blank
positions; table 2 retains two input and one output register assignment. Three formulas,
eight version-value pairs, four printed calculations and twelve prose boundaries
retain source contexts. Canonical title and null byline stay unchanged; source credit
is separate. All 72 drafts were read before one source pass: three English and 69
Korean/English regions, zero retries or within/post-pass source changes. Eighty-three
pre-OCR crop events remain retained. Metadata r02 records intervening table/listing
panels on 261→262 and 264→265; only four JSON files differ from retained r01. All
source text, assets and raw ZIP bytes remain exact. Source spelling, offset/version
claims, comment differences and glyph candidates remain; no code repair or execution.
Seventeen rehashed native and two ownership mutations reject. All 23,349 prior files
and thirty core modules remain exact; prior fresh 213-test evidence retained. Main
prose ends 268; Listing 5 ends at 516 END Entry on 272 before independent book-year
filler. Pages 273–275 are advertisements, 276 the distinct vector-font opener.
Final 266–272 and actual thirteen-page assembly remain required.

Batch 26 preserves DOS continuation PDF 266–271/printed 264–269 as a
199-file immutable native. Independent and fresh-process exports match. All 61
crops, 43 outcomes, 8,707 typed range occurrences and 659 reading rows validate.
Eighteen original images retain three structure tables, the STACKS formula,
screenshot, build commands, ending ornament and code panels. Six captions contain
literal display text; twelve are null. Tables preserve 54 explicit cells/nine
headers and eleven enumeration labels, including within-cell wraps. Printed
9×128=1,052 remains literal. Independent Listing 4 preserves 81 numbered rows and
nine unnumbered comment wraps; Listing 5 DOSINFO.ASM preserves rows 001–410.
Four commands form two separate contexts. The current 504 physical code/command
rows include 100 blank numbered rows, 1,876 tokens, 228 comment rows, 293
instructions, 271 register occurrences, 102 immediates, 23 memory operands and
72 branch/call occurrences. Seven decorative rule counts remain explicit unresolved
markers linked to original images. Colon-shaped MASM punctuation, boxed return-key
candidates, MODEL without a visible leading dot and source spelling remain;
no code repair or execution. Five prose boundaries retain the 267→268 continuation
across independent Listing 4 and screenshot; prose ends 268 with a separate tail
and ornament. Eight code-panel boundaries retain the two independent listings.
All 43 drafts were read before one source pass: twelve English and 31 Korean/English
regions, thirty pre-OCR crop events and zero retries or within/post-pass changes.
Seventeen rehashed native and two ownership cases reject. An initial audit lookup
matched the S enumeration inside IFS; its validator was corrected without package
changes. All 23,963 prior files and thirty core modules remain exact; earlier fresh
213-test evidence is retained. DOS coverage now spans 260–271 in separate natives
a/b, 307+199=506 files. The primary directory/manifest still identifies opening a.
Final 272 and actual thirteen-page assembly remain required.

Batch 27 preserves final DOS page 272 as a 19-file native and actually
assembles the complete thirteen-page article on PDF 260–272/printed 258–270.
All 534 assembly files match an export consuming three independently regenerated
natives totaling 525 files and a fresh-process rebuild. All 147 exact crops,
117 outcomes, 13,673 metadata projections, 27,998 current range occurrences/
27,864 source occurrences and 1,260 reading rows validate. All original native
blocks, text, metadata and assets remain unchanged. Thirty original images retain
seventeen code/command panels, five table/interface compositions, four formulas,
portrait/category artwork, screenshot and ending ornament. Eleven captions contain
literal text; nineteen are null. Four regular tables retain 68 explicit cells and
twelve headers; the separate call interface retains two inputs and one output.
Seven independent code contexts preserve 741 physical rows: 716 numbered rows
across five listings, 21 unnumbered comment wraps and four build commands. There
are 148 blank numbered rows, 2,708 tokens, 340 comment rows, 443 instructions,
434 register occurrences, 149 immediates, 42 memory operands, 103 branch/call
occurrences and 25 quoted occurrences. Listing 5 DOSINFO.ASM is complete as printed
at 001–516. Root metadata links b410→c411, preserves native row IDs/ordinals and
adds cumulative current ordinals; GetStacks 390–470 is complete while both native
partial/tail records remain historical. Independent Listing 4 GetStacks stays separate.
Seventeen prose boundaries, nine within-native code boundaries and one cross-native
Listing 5 boundary retain source contexts. Main prose ends 268; final 516 END Entry
on 272 precedes excluded book-year filler. No prose merges or code repair/execution.
Final native adds two initial English drafts, both read before one source pass;
zero crop changes, retries or within/post-pass changes. Two new decorative rule
markers bring the unresolved dash-count total to nine. Printed wording, arithmetic,
MASM punctuation and glyph/space/byte candidates remain. Twelve rehashed assembly,
eight native, two ownership and three adapter-guard cases reject. All 24,162 prior
files and thirty core modules remain exact; earlier fresh 213-test evidence retained.

Batch 28 verifies vector-font article 0019's eleven-page body, PDF 276–286/
printed 274–284, and preserves opening 276–281 as a 346-file partial native.
Independent and fresh-process exports match. All 94 exact crops, 81 OCR outcomes,
2,073 typed range occurrences and 430 nonempty reading rows validate. Thirteen
original images retain category/group/series artwork, two tables and figures 1–8;
ten captions contain literal text and three are null. Table 1 has thirteen rows/
39 cells/three headers; table 2 has fourteen rows/28 cells/two headers. Physical
cell wraps remain explicit, including INSERT/CURVE in one menu cell. Cases 7/8
have distinct straight/curve wording; final source readings supersede the earlier
preliminary duplicate-case observation. Figure 3's matrix retains thirty displayed
rows 0–25/96–99, 294 explicit data cells, ten headers, six blank x4/y4 cells in rows
10/19/22 and two dotted separators. Omitted 26–95 values are never expanded.
Three independent code contexts retain ten physical rows, 93 tokens, four comments,
eight struct members in four field groups, two 100-element arrays and four
assignments. Seventy-eight diagram labels retain figure/phase contexts. Nine prose
boundaries, independent editorial/series contexts and outgoing 281→282 remain.
All 81 initial drafts were read before one paused/resumed source pass. Sixty-five
pre-OCR crop events and one within-pass figure-only table-frame extension remain;
all 81 raw/TSV outcomes are exact with actual r04 execution origins. Zero text-crop
changes, new recognitions, retries or post-pass changes. Source 고정난, 에니메이션,
drawploy, 곡선와, repeated wording and missing counter parenthesis remain literal.
Pcx/Pex, glyphs, spacing, encoded bytes and exact dot counts remain unverified.
Twenty rehashed native and two ownership mutations reject. All 24,715 prior files
and thirty core modules remain exact; earlier fresh 213-test evidence retained.

Batch 29 preserves vector-font final PDF 282–286 as a 228-file native and
actually assembles the complete eleven-page article, 276–286/printed 274–284.
All 583 assembly files match an export consuming two independently regenerated
natives totaling 574 files and a fresh-process rebuild. All 163 exact crops,
131 outcomes, 11,953 native metadata projections, 23,790 current range occurrences/
23,644 source occurrences and 940 reading rows validate. Every projected source
field retains its native context; original metadata/assets stay exact. One
281→282 prose merge joins 있어야 while retaining all seven intervening Table 2/
Figure 8 items. Thirteen internal prose boundaries and six code-panel boundaries
remain. Main prose ends 283; seven independent listings end at listing 7 row 21
on 286, before excluded book advertising. Ten code contexts preserve 385 physical
rows: ten opening fragment rows and 375 numbered rows across seven listings
69/80/69/37/40/59/21. Six numbered blanks, seven missing row-13 colons and eight
unresolved wavy rules remain. All 3,899 tokens, 67 comments, 130 lexical API names,
29 control names, 217 member accesses and 33 numbered wrap groups retain source
occurrences. Three printed functions are complete; no code repair or execution.
Thirty-two original images have 22 literal captions and ten null captions. Four
tables retain 83 cells/five headers; Figure 3's separate matrix keeps 294 cells/
ten headers/six blanks/two dotted separators. All 108 diagram-label occurrences
retain figure/phase contexts. Final native adds fifty initial recognitions, all
drafts read before one paused/resumed source pass. Twenty pre-OCR crop events;
zero retries or within/post-pass changes. The initial map schema rejection occurred
before recognition; the diagnostic and corrected revisions remain retained.
Source caption/prose differences, duplicate mouse_off() calls, pro!=1, spelling,
operator/glyph candidates and unresolved rule/dot counts stay literal. Sixteen
rehashed assembly, twelve native, two ownership and three adapter-guard cases
reject. All 25,061 prior files and thirty core modules remain exact; earlier fresh
213-test evidence retained.

Batch 30 classifies pageless library heading 0020 as non-owning and preserves
menu-library article 0021 opening PDF 292–297/printed 290–295 as a 363-file partial.
Independent and fresh-process exports match. All 96 exact crops, 86 selected OCR
outcomes, 2,498 typed ranges and 490 nonempty reading rows validate. Ten original
images retain category/chronology artwork, two box screens, two header panels,
the annotated C example and three menu illustrations; eight captions contain
literal source text and two are null. Three code contexts preserve 130 physical
rows, 573 tokens, 45 comment rows, two string/character literals, fourteen defines,
ten prototypes, nine FILE members, four printed example functions, twelve unresolved
decorative rule counts and four omission-dot rows. Two independent sidebars, three
reference contexts, nine chronology entries/eleven rows, seven printed errata
relationships, nineteen lexical diagram labels and four formula relationships
remain source-local. Ten prose boundaries retain their independent contexts.
All 86 initial drafts plus one changed-crop draft were read before one source pass.
Forty-nine pre-OCR crop events and one pre-correction paragraph extension remain
retained: 87 actual recognitions, 85 exact raw/TSV reuses with original execution
provenance, zero unchanged-input retries or within/post-pass changes. Source code
and wording defects stay literal; no repair, compilation or execution. Twenty
rehashed native, three group and two ownership mutations reject. The two group
files reproduce independently/fresh-process with all four canonical child links.
All 25,872 prior files and thirty core modules remain exact; the earlier fresh
213-test evidence is retained. Actual article extent 292–304 is individually
reviewed: main prose ends 300 and four numbered listings end at XmTEST.C row 108
on 304, before excluded book advertising. Final 298–304 and actual assembly remain.

Batch 31 preserves menu-library continuation PDF 298–303/printed 296–301 as a
221-file immutable native. Independent and fresh-process exports match. All 65 exact
crops, 49 selected outcomes, 12,932 typed ranges and 835 nonempty reading rows validate.
Sixteen original images preserve three array examples, a menu diagram, two screenshots,
the closing ornament and all numbered listing panels. Fourteen caption associations
use literal text; two are null. Seven code contexts retain 639 physical rows: 105
unnumbered example rows and 534 numbered rows across listings 1–4, with lengths
124/24/352/34. Forty-four numbered blanks, eight omission-dot rows, 4,193 tokens,
261 comment rows, 92 literals and ten complete printed functions remain indexed.
Seventy-six unresolved graphic/rule spans retain original panels; no box-drawing
bytes or decorative counts are inferred. Five arrays retain 69 explicit literals.
Four prose and five code boundaries retain source contexts. Main prose ends 300;
listing 4 continues from row 34 on 303 to final rows 35–108 on 304. All 49 initial
and one changed-crop drafts were read before one source pass: 33 pre-OCR events,
one pre-correction number-column extension, fifty actual recognitions, 48 exact
raw/TSV reuses with original execution provenance and zero unchanged-input retries
or within/post-pass changes. Metadata r02 restores fourteen cross-crop comment rows;
only four root JSON files differ, with transcript/assets/raw ZIP bytes exact.
Twenty rehashed native and two ownership mutations reject. All 26,237 prior files
and thirty core modules remain exact; the earlier fresh 213-test evidence is retained.
Opening a and continuation b preserve twelve pages in 363+221=584 files. Final 304
and actual thirteen-page assembly remain required; the primary manifest still
identifies opening a. Historical code and claims are not repaired or executed.

Batch 32 preserves menu-library final PDF 304 as a nineteen-file native and
actually assembles the complete thirteen-page article, 292–304/printed 290–302.
All 612 assembly files match an export consuming three independently regenerated
natives totaling 603 files and a fresh-process rebuild. All 165 exact crops,
137 outcomes, 17,039 native metadata projections, 35,799 current range occurrences/
35,645 source occurrences and 1,399 reading rows validate. Every projected field
retains its native context; original text, metadata and assets remain exact. One
297→298 prose merge joins 문자 and 열; listing 4's 34→35 boundary completes main
through row 108 without changing code bytes. Main prose ends 300, separate from
two screenshots and four numbered listings. Ten code contexts preserve 843
physical/logical rows, including 608 numbered rows across listings 124/24/352/108
and 51 numbered blanks. All 5,311 tokens, 327 comment rows and 125 string/character
literals remain indexed. Fifteen printed function contexts include eleven complete
numbered-listing functions and four example functions with source defects retained.
Six array contexts keep 96 explicit string literals and 36 numeric values; item2's
complete initializer retains both original fragments. Example 4 remains its printed
fragment. Twenty-eight original images have 22 literal caption associations and six
null captions. Seven errata relationships, two independent sidebars, chronology,
references and source claims remain separate. Seventy-nine graphic/rule spans plus
twelve independent header-rule counts stay unresolved. Final native adds two initial
English recognitions, both drafts read before one source pass, zero retries or crop/
within/post-pass changes. Sixteen rehashed assembly, twelve native, two ownership
and three adapter-guard cases reject. All 26,679 prior files and thirty core modules
remain exact; the earlier fresh 213-test evidence is retained. No code repair,
compilation, execution or reader rebuild.

Batch 33 verifies Class(Y) article 0022's actual eleven-page extent, PDF 318–328,
and preserves opening 318–323/printed 316–321 as a 367-file partial native.
Independent and fresh-process exports match. All 100 exact crops, 86 OCR outcomes,
2,496 typed range occurrences and 458 nonempty source rows validate. Fourteen
original images preserve category artwork, code panels and two diagrams; two
captions contain literal source text and twelve remain null. Eight separate code
contexts retain 117 physical/114 logical rows, eighteen blanks, three wraps,
642 tokens, five comments, six string literals, three includes, two class declarations
and thirteen printed function bodies. Repeated constructor/inheritance examples
retain their own source occurrences. Figure 1 has eight menu labels; Figure 2 has
five class compartments, ten instance variables, 24 methods, fifteen field headings,
two explicitly empty instance fields, two stars and four directed connectors.
All 62 diagram labels, three menu definitions, ten prose boundaries and three code
boundaries remain indexed. Canonical Class(Y) and printed Class(y) remain separate;
byline 임지열, parent 0020 and contents reference 316 are unchanged. Main prose ends
325; six numbered listings end at MENUDEMO.PRG row 66 on 328 above book advertising.
All 86 initial drafts were read before one continuing source pass: eleven pre-OCR
crop repairs, one notation-kind clarification, zero retries or within/post-pass
changes. Printed filename differences, wording, technical claims and unresolved
constructor punctuation remain literal. Twenty-two rehashed native and two ownership
mutations reject. All 27,310 prior files and thirty core modules remain exact;
the earlier fresh 213-test evidence is retained. Final 324–328 and actual assembly
remain required. No code repair, compilation, execution or reader rebuild.

Batch 34 preserves Class(Y) final PDF 324–328 as a 176-file native and actually
assembles the complete eleven-page article, 318–328/printed 316–326. All 552 assembly
files match an export consuming two independently regenerated natives totaling
543 files and a fresh-process rebuild. All 150 exact crops, 125 outcomes, 9,806
native metadata projections, 19,507 current typed ranges/19,362 source occurrences
and 949 source reading rows validate. Every projected field retains its native
context; original text, code, metadata and assets remain exact. One 323 Pu→324
llDnMenu prose join retains both original regions. Main ends 325 with a separate
ornament; six numbered listings end at MENUDEMO.PRG row 66 on 328 above excluded
book advertising. Fourteen code contexts preserve 463 physical/460 logical rows,
including 346 visible numbered rows, 72 numbered blanks, eighteen unnumbered blanks
and twelve wrap groups. Listing 6 jumps from printed 41 to 43; no row 42 or missing
content is invented. All 2,272 tokens, 62 comment rows, 33 string literals, 52 printed
function contexts and seven class declarations remain indexed. Two damaged keyword
glyphs remain explicitly unresolved. Five menu initializers retain fourteen labels
and their callback/submenu occurrences. Twenty-five original images have eight
literal captions and seventeen null captions. All 62 diagram labels, three menu
definitions, thirteen internal prose/seven code boundaries and source claims remain
separate. Final native adds 39 initial recognitions, all drafts fully read before
one continuing source pass. Four pre-OCR crop repairs; zero retries or within/post-pass
changes. Seventeen rehashed native, sixteen rehashed assembly, three adapter and two
ownership cases reject. All 27,677 prior files and thirty core modules remain exact;
the earlier fresh 213-test evidence is retained. No code repair, compilation,
execution or reader rebuild.

Batch 35 verifies Halla Pro(2) article 0023's actual twelve-page extent, PDF
330–341, and preserves opening 330–335/printed 328–333 as a 790-file partial native.
Independent and fresh-process exports match. All 211 exact crops, 190 OCR outcomes,
2,544 typed range occurrences and 484 nonempty source reading rows validate. Four
original tables retain 49 data cells, two blank cells, eleven headers and four
literal captions. Table 2 keeps five multiline groups; table 3 keeps eight nodes
and five arrows in three separate priority chains. Table 4 reads 내정 자형.
Twenty-one original images have four literal captions and seventeen null captions.
Directory-tree parts and project diagrams retain 49 searchable labels and fourteen
library/description pairs. Seven procedure groups preserve 33 entries; seven command
occurrences and twelve header filenames remain indexed. The annotated HELLOHAN.C
example has thirteen physical rows/four blanks and four separate callouts. DOS
output adds ten rows/two blanks: 23 total rows, 153 tokens, one comment and two
quoted literals. Four colon-like statement endings remain explicit colon/semicolon
uncertainties without syntax repair. Six prose and two procedure boundaries retain
their original contexts; outgoing 335→336 remains deferred across tables 2–4.
All 190 initial drafts were fully read before one continuing source pass. Fifteen
pre-OCR crop repair/repartition events across three retained maps; zero retries or
within/post-pass changes. Printed wording, filename differences, damaged glyphs,
dot counts and control-byte candidates remain literal or explicitly uncertain.
Thirty rehashed native cases and two ownership cases reject. All 28,405 prior files
and thirty core modules remain exact; earlier fresh 213-test evidence is retained.
Final 336–341 and actual twelve-page assembly remain required. No code repair,
compilation, execution or reader rebuild.

Batch 36 preserves Halla Pro(2) final PDF 336–341 as a 949-file native and actually
assembles the complete twelve-page article, 330–341/printed 328–339. All 1,748 files
match an export consuming two independently regenerated natives totaling 1,739 files
and a fresh-process rebuild. All 464 exact crops, 419 outcomes, 5,562 native metadata
projections, 10,732 current typed ranges/10,286 source occurrences and 1,001 indexed
reading rows/fragments validate. One 335→336 prose join retains both original source
contexts and all 38 intervening table 2–4 caption/image/header/cell items, with one
declared display space. Ten tables retain 133 data cells, two blank cells, 29 printed
headers and one blank header. Thirteen code/output contexts retain 63 physical/
59 logical rows, thirteen blanks, four wraps, 454 tokens, one comment, eighteen
quoted literals and seven include rows. Four opening callouts and nine final
code annotations remain separate from code bytes. Forty-five original images have
nineteen literal captions and 26 null captions. Five complete screen images retain
64 selected GUI label candidates and five source creator/ID associations. Miniature
GUI text/data remains source-image dependent; no complete GUI transcription,
numerical dataset or original software behavior is claimed. Fifteen internal prose
and two procedure boundaries remain; final 341's next-month paragraph/MS ornament
stays above excluded publisher advertising. Final native adds 229 initial calls,
all drafts fully read before one continuing source pass. Seventy-eight pre-OCR crop
events, one saved punctuation refinement during the pass, zero retries or within/
post-pass crop/OCR changes. Printed FIXRESMDOE, wording, filename/coordinate
differences and colon/semicolon candidates remain literal or explicitly uncertain.
Twenty native, fourteen assembly, three self-consistent adapter faults and two
ownership cases reject. All 29,195 prior files and thirty core modules remain exact;
the earlier fresh 213-test evidence is retained. Both natives remain immutable with
historical partial scopes. No code repair, compilation, execution or reader rebuild.

Batch 37 completes CMDLN article 0024 on PDF 344–348/individually observed printed
342–346. All 379 selected r02 files match independent and fresh-process exports.
All 103 exact crops, 89 outcomes, 6,020 typed ranges and 434 indexed nonempty reading
rows/fragments validate. Twenty-one code/output contexts retain 260 physical rows,
225 nonblank physical rows, 217 logical source rows, 35 display-gap blanks and six
physical wraps. Both listings retain their literal printed number columns, 0–70
and 1–85: 156 numbered rows. Listing downloads preserve those columns; original
program-file recovery is unverified. All 2,104 tokens, 58 quoted C/C++ literals,
four comments, three includes, seven printed function bodies, eight API signatures,
ten explicit command/usage occurrences and 32 filename references retain source
contexts. Four independent printed-output contexts and two separate Korean callouts
remain; the first option result continues lower-left to upper-right on 348. Fourteen
original images have four literal captions and ten null captions. Five prose
boundaries retain source blocks; final 348's closing paragraph/MS ornament precedes
independent book advertisement 349 and the distinct Windows-tools opener 350.
All 89 initial drafts were read before one continuing source pass. Thirty-five
pre-OCR crop events across three maps, zero retries or within/post-pass changes.
Direct pale-color review repaired annotation ascenders missed by threshold-130
checks. All 87 source-local candidates remain explicit, including colon/semicolon
readings, missing connective wording, `*option`/`*options` differences, besure, an extra
percent-like command mark and the figure's BORLANDC path candidate. No syntax repair,
compilation or execution. R01's broad command matcher is retained; metadata-only r02
selects ten explicit occurrences and logical wrap groups. Only four root metadata
files differ; all article/listing/raw-ZIP/asset/OCR bytes remain exact. Thirty-two
rehashed native cases pass generic integrity and fail the independent source audit;
two canonical ownership cases also reject. All 31,892 prior files and thirty core
modules remain exact; earlier fresh 213-test evidence retained. Full proofreading,
human acceptance, exact glyphs/spacing/encoded bytes, historical claims and software
behavior remain unverified. No reader rebuild.

Batch 38 classifies pageless group 0025 활용 as non-owning and preserves OOP article
0026 opening PDF 306–311/printed 304–309 as a partial native. Its 325 files and three
classification files reproduce independently and in fresh processes. All 88 crops,
76 OCR outcomes, 1,613 typed ranges and 691 nonempty source rows validate. Twelve
original images have null captions. Three code examples retain sixteen physical
rows, fourteen nonblank rows, two blank gaps, 127 tokens, six printed result comments,
seven calls and one MakeBlock function. Literal `2x`, `block:x(2)`, Makeblock case and
the final unanswered `? block1:eval` remain unchanged. Five descriptive templates
across six prose regions retain twenty rows, fourteen parameter placeholders and
four independent private/exported member occurrences. Templates are not executable
programs. Fourteen prose boundaries, one constructor-template boundary and outgoing
311→312 retain their source contexts. Quoted anecdote/bibliography, monthly-disk
unavailability notice, eleven listing mentions, two filenames and seventeen version
occurrences remain literal. OCR missed the second heading row on 309; it was restored
from the unchanged scan without another recognition. All 76 drafts were read before
one continuing source pass; 27 pre-OCR crop events, zero retries or within/post-pass
changes. All 36 source-local candidates remain explicit. Thirty-six rehashed native,
six group and two canonical ownership faults reject. All 32,650 prior files and
thirty core modules remain exact; earlier fresh 213-test evidence retained.
The actual twelve-page extent is 306–317/printed 304–315; main prose ends 313 and
four numbered listings continue through 317. Final printed line 266 `중략` is preserved
as an observed omission. Final 312–317 had extent/layout review only; their source
correction and actual twelve-page assembly remain required. No omitted program
content, source encoded bytes, software functionality or execution is inferred.
Group evidence retains contents 5 and category 306 crops plus repeated banner 350;
all five child identities remain unchanged. No group body/byline/folio or Windows-tools
restoration is invented. Full proofreading and human acceptance remain pending.
No reader rebuild.

Batch 39 restores final OOP PDF 312–317 and actually assembles all twelve pages
306–317/individually observed printed 304–315. The 537-file root reproduces from both
independently regenerated natives/528 files and in a fresh process. All 150 crops,
120 outcomes, 12,846 metadata projections, 25,588 current typed ranges/25,452 source
occurrences and 1,366 indexed source rows validate. One 311→312 prose join retains
two intervening category items and both original contexts. Main prose ends 313
with a separate MS ornament; four numbered listings continue through 317.
All 505 numbered rows remain: OBJECT.CH 1–26, OOPDEMO.PRG 1–96, OBJECT.PRG 1–117
and PICKLIST.PRG 1–266. Listing downloads preserve number columns and 86 numbered
blanks. Nine code contexts retain 524 physical rows, 435 nonblank rows and three
unnumbered display gaps. The final native records 374 logical listing groups and
47 wraps; the opening examples retain fourteen nonblank rows separately. All 4,573
code tokens, 88 quoted-literal candidates, 130 comments including seventeen Korean
rows, seven includes, 23 macros and eleven printed function bodies retain source
occurrences. Deonstration/Pseduo spelling, identifier case, unquoted color tokens,
string-continuation defect, missing-semicolon candidates and PickList2 remain literal.
Five descriptive templates retain twenty rows, fourteen parameter placeholders,
four private/exported occurrences and their split-constructor boundary. Thirty
original images have four literal captions and 26 null captions. Twenty internal
prose boundaries, eight code continuations, quoted anecdote/bibliography, monthly-disk
unavailability notice, OCR-missed heading row, eleven resolved listing references
and all 257 source-local candidates remain explicit. Final listing 4 row 266 `중략`
is a printed omission after EOF 264 and blank 265. No omitted program content is
reconstructed; article completeness as printed does not certify software recovery.
Final native adds 44 initial plus one pre-correction changed-crop recognition;
43 raw/TSV outcomes are reused exactly with their actual execution origins. All
45 drafts read before one continuing source pass; six pre-OCR crop events, zero
unchanged-input retries or within/post-pass changes. Direct review found whole
letters beyond a zero-crossing crop; one widening restores comment 176's final
word string. The initial map-helper schema error remains retained. Twenty rehashed
native faults, twenty assembly faults, three self-consistent projection faults and
two ownership faults reject. All 32,978 prior files and thirty core modules remain
exact; earlier fresh 213-test evidence retained. Full proofreading, human acceptance,
exact glyphs/spacing/encoded bytes, historical claims, original software recovery
and execution remain unverified. No reader rebuild.

Batch 40 verifies Windows-tools article 0027's actual seven-page extent, PDF
350–356/individually observed printed 348–354, and preserves opening 350–355 as a
474-file partial native. Selected r02 reproduces independently and in a fresh process.
All 130 exact crops, 112 outcomes, 1,957 typed ranges and 660 nonempty source rows
validate. Eighteen original images have eight literal captions and ten null captions.
Five application heading/icon pairs and six screenshots retain searchable selected
labels; miniature configuration, list, body and control data are not fully recovered.
Diagram 1 retains twelve label regions/thirteen physical text rows, six nodes and
five directed arrows. Its bottom-right node reads 클라이언트 프로그램 despite the
historical crop ID final-packager. Table 1 retains 39 rows, 117 cells, 95 nonblank
cells, 22 blank merged-resource cells, three headers and seventeen resource groups.
Repeated DeleteObject cells link to distinct source occurrences; blanks remain empty
with explicit image, column and group associations. Printed CreateCommpatibleDC,
SetWindowHook, GlobalFreeAtom, UnhookWindowsHook and Executer stay literal.
Four numbered recovery steps, 38 filename references, sixty menu references, seven
version occurrences, fourteen prose boundaries and 36 source-local candidates retain
their contexts. The editorial attribution is separate from 김강훈's byline; the opening
drop cap is folded once. All 112 drafts were read before one continuing source pass;
112 initial recognitions, zero retries or within/post-pass changes. Four maps retain
69 pre-OCR crop events. Zero nonfigure overlaps; thirteen threshold-130 crossings are
directly color-reviewed non-text backgrounds, frames, arrows or grid. An initial
duplicate-order helper assertion is retained. Metadata-only r02 fixes three proposed
future joins inside words; four root metadata files change, while article text,
images, raw OCR/settings and ZIP bytes remain exact. Both 474-file revisions remain.
Thirty rehashed native faults and two ownership faults reject. All 33,718 prior files
and thirty core modules remain exact; earlier fresh 213-test evidence is retained.
Final 356 and actual seven-page assembly remain required. Outgoing 355 ends 동 and
356 begins 적으로 across the intervening table; the future join has no added space.
Final 356's lower independent book advertisement is outside the article. Full
proofreading, human acceptance, exact glyphs/spacing/encoded bytes, historical claims,
software/configuration recovery and execution remain unverified. No reader rebuild.

Batch 41 restores final Windows-tools PDF 356 and actually assembles all seven pages
350–356/individually observed printed 348–354. The 544-file root reproduces from
both independently regenerated immutable natives/536 files and in a fresh process.
All 145 crops, 125 outcomes, 2,118 metadata projections, 4,108 current typed ranges/
3,984 source occurrences and 706 nonempty source rows validate. One 355→356 prose
join forms 동적으로 with no added space, retaining ten intervening table/category
items and both original contexts. Twenty original images have eight literal captions
and twelve null captions. Six screenshots preserve selected searchable labels with
explicit miniature configuration/list/body/control limits; five application icons
and their headings remain. Table 1 retains 39 rows, 117 cells, 95 nonblank cells,
22 blank merged-resource cells, three headers and seventeen resource groups. Repeated
DeleteObject cells retain distinct source occurrences. Diagram 1 preserves twelve
label regions/thirteen physical rows, six nodes and five directed arrows; its final
node reads 클라이언트 프로그램. All table/cell/group/screen/application/diagram/node/
edge/option/hotkey/procedure identifiers and references are namespaced. Four recovery
steps, six option entries, three physical hotkey occurrences, sixteen internal prose
boundaries and 46 source-local candidates remain. Printed Executer, RepaintScreen,
CreateCommpatibleDC, SetWindowHook, GlobalFreeAtom and UnhookWindowsHook are literal.
The editorial attribution is separate from 김강훈's byline; the opening drop cap is
folded once. Final 356 ends the stress.ini paragraph with a separate MS ornament;
the lower independent book advertisement is excluded. Final native adds thirteen
initial recognitions after two pre-OCR margin events. All thirteen drafts read before
one source pass; zero retries or within/post-pass changes. Direct color review and
exact crop checks pass. Opening natives, both 474-file revisions, all maps and original
OCR/corrections remain unchanged. Fifteen rehashed native faults, eighteen assembly
faults, five self-consistent projection namespace/occurrence faults and two ownership
faults reject. Failed audit-helper assumptions remain retained; source content was
unchanged. All 34,666 prior files and thirty core modules remain exact; earlier fresh
213-test evidence retained. Full proofreading, human acceptance, exact glyphs/spacing/
encoded bytes, historical claims, software/configuration recovery and execution remain
unverified. Selected GUI labels do not certify complete miniature data recovery.
No reader rebuild.

Batch 42 verifies and restores complete public-software article 0028 on PDF
358–362/individually observed printed 356–360. All 396 files reproduce independently
and in a fresh process. The canonical title uses 4가지 and byline 편집부; source title
네 가지 and credits 김영숙, 신동수 기자 remain separately indexed. All 106 exact crops,
94 outcomes, 1,980 typed ranges and 567 nonempty source rows validate. Four distinct
components cover 길 1.1, 모든글, 윈도우즈 스캔 100 and Whoop It Up!, with explicit
body extents and floating figure associations. Twelve original images have seven
literal captions and five null captions. Two menu tables retain eighteen and 42
data rows, 180 cells, 98 nonblank cells, 82 blank merged-menu/shortcut cells, eleven
main-menu groups and eight printed unsupported-menu asterisks. Repeated F8 shortcuts
retain independent source offsets. Leading dashes, Casecade and the diagonal mark
before Save As remain literal. The original special-character chart preserves thirteen
numeric row labels, ten numeric column labels and 130 opaque graphic positions.
Each position retains its original image/slot and axis sources; Unicode transcription
and encoded byte value remain null. No glyph assignment, blank/ink interpretation,
axis-derived code arithmetic or font reconstruction is claimed. Four screenshots
retain selected searchable labels with explicit miniature console/menu/list/document/
configuration/control limits. Two OCR omissions, the large scan-100 heading and a
miniature menu row, are restored directly from unchanged source crops. Printed
heading/caption 93 and body 100 remain separate. Five speaker setup steps, 25 filename
occurrences, fifteen scan-name occurrences, eight version occurrences, twelve prose
boundaries, two historical contacts and 57 source-local candidates remain indexed.
Printed `$m`, unusual font filenames, 8×4×4, 1088KB, Dirver, 직업 and 동우회 stay
literal. All 94 drafts read before one continuing source pass; 94 initial recognitions,
zero retries or within-pass crop/OCR changes. Four maps retain forty pre-OCR crop
events. Direct color review repairs clipped prose, final table row, menu ascenders
and leading dashes; ten remaining threshold-130 crossings are non-text table/control/
background/frame ink. All text crops are disjoint. One within-pass saved-text correction
refines the initial font-menu reading to 하얀글; both readings and detail evidence remain.
No post-pass change. Final 362 ends with archive filenames/MS ornament; 363 is advertising
and 364 opens distinct debugger article 0029. Thirty-two rehashed native faults and
two ownership faults reject. All 35,272 prior files and thirty core modules remain
exact; earlier fresh 213-test evidence retained. Full proofreading, human acceptance,
exact glyphs/spacing/encoded bytes, historical claims, original software/configuration
recovery and execution remain unverified. No reader rebuild.

Current totals: twenty-one readable/sample-reviewed articles, no partials, four non-owning
groups, three section references and 24 unresolved identities among 52. Twenty-one
current body-owner packages contain 10,382 exact files; thirteen classification evidence
files remain separate. Original natives and superseded revisions remain unchanged.

Next: Batch 43 verifies debugger/disassembler article 0029 from its known PDF 364
opener/reference 362. Establish actual continuity and ending, then map up to six
confirmed opening pages, provisionally 364–369. Reuse retained 364–368 renders; their
context/layout review does not claim restoration. Preserve canonical title/byline
장근재 and the source affiliation 순천향대 병원 separately. Keep debugger command
tables, printed command/code fragments, original figures and historical claims literal;
do not repair or execute source syntax, bytes or addresses. Public-software 0028 is
final. The ceilings remain two canonical tasks, six mapped pages and twenty outside
lookups. No reader rebuild.

Remaining bodies, 433-page accounting, cover and issue closeout are required. See
[March progress](docs/progress/9303.md) and the
[ledger](metadata/catalog/pdf-restoration/1993-03-progress.json).

## December 1992 closeout, 2026-11-01

The canonical TOC JSON/assets pass is complete with explicit coverage gaps. All 45
identities and 446 source pages are accounted: thirty readable/sample-reviewed
articles, two partials, seven groups, three section references and three unresolved
identities. The standalone collection at `archive/pdf/1992-12/reference/` contains
13,097 independently exact files. All 59 natives and fourteen actual assemblies
regenerate exactly; fresh 213 PDF tests pass. Five final gap/reference outcomes remain
reported without claiming full original article recovery. See the Batch 72 closeout
below, [December record](docs/progress/9212.md) and private handoff/reproduction evidence.
Full proofreading, human acceptance and volunteer glyph work remain deferred. No reader
rebuild. Historical checkpoint notes below retain their original states.

The two independent JSON/assets exports contain 94 exact files. All 23 native
crops match source render pixels; all 21 mapped Tesseract drafts were read and
source-corrected once, with zero OCR retries. Four section headings, two original
images, two independent pull quotations, a separately attributed closing quotation
and six continuation boundaries are retained. A pre-OCR crop revision is preserved;
the old araea product-name glyph remains an explicit source-linked approximation.
The checkpoint uses one canonical task, three mapped pages and seventeen outside
lookups. Prior September reference files and thirty core modules remain exact.

The feature native contains 207 independently exact files, 54 exact source crops,
48 OCR outcomes and eleven continuation boundaries. The original opening artwork,
three diagrams/charts, two formula panels and literal POINT code remain intact.
One source correction pass, no OCR retries; pre-OCR crop repairs, a failed helper
and one saved-transcript refinement remain explicit. The final summary/closing
mark/references are observed on PDF 183, followed by advertisements; this does not
prove unreviewed intervening continuity. Child 0002–0004 remain unresolved.

Batch 03 completes continuation PDF 162–167/printed 152–157 as native b. The first
intrinsic section is now preserved across twelve feature pages in natives a/b;
whole-feature availability remains partial. The selected second export revision has
341 independently exact files, 92 exact source crops, 80 OCR outcomes, nine glossary
entries, nine diagram captions, four code fragments and ten internal boundaries.
Both original download/scan contexts for the incoming 161→162 join validate.
Pre-OCR map revisions, one failed helper, one bracket-output refinement and one
metadata-only export revision remain preserved. One source correction pass; no
OCR retry. Child 0002–0004 remain unresolved pending actual assembly/final anchors.

Batch 04 preserves part 2 opening PDF 168–173/printed 158–163 as native c:
326 independently exact files, 86 exact source crops, 77 OCR outcomes, 72 blocks
and nine original images. Fourteen code fragments retain 61 nonempty rows,
46 colon candidates and three ellipsis rows; seven caption associations and five
column joins validate. One source pass, no recognition retry. A terminal render
interruption before recognition is retained. The feature now spans eighteen
preserved pages across a/b/c. PDF 168 starts a new section without an incoming
prose join; 173→174 continues mid-word 속+성. No child classification is advanced.

Batch 05 adds PDF 174–179/printed 164–169 as native d: 443 independently exact
files, 116 exact crops and 106 OCR outcomes. Four complete tables retain 34 rows
and 285 cells, including the twelve-method/fourteen-criterion matrix; eight internal
joins, four code fragments/34 rows and all 1,880 current typed ranges validate.
Both native contexts of the incoming 속+성 join remain explicit. Part 2 ends 175;
part 3 starts 176 independently. One source pass, no recognition retry; four pre-OCR
crop repairs and a failed preflight helper retained. Coverage is now 156–179 across
a/b/c/d; the first two intrinsic section bodies are preserved, with no child
classification or completed assembly claim.

Batch 06 completes final PDF 180–183/printed 170–173 as native e: 198 independently
exact files, 55 exact crops and 45 OCR outcomes. Three lists/eleven step entries,
four references, six captions and eight internal boundaries validate; both original
incoming native contexts remain explicit. The conclusion, closing ornament,
bibliography and photograph end on 183; 184–185 are advertisements. One source
pass, no recognition retry or crop revision. All 28 feature body pages, 156–183,
are preserved across five immutable natives. Availability remains partial until
actual assembly; child 0002–0004 remain unresolved.

Batch 07 delivers the actual readable parent assembly and child 0002's final
non-owning anchor on PDF 157/printed 147. All 1,524 assembled files reproduce from
five independently regenerated natives; 403 exact crops, 356 OCR settings, 4,746
projected metadata ranges, 9,156 current typed occurrences and three cross-native
joins validate. The deterministic second revision passes fresh-process checks;
the first metadata-order revision and failed helpers remain preserved, with unchanged
article/listing/map bytes. All 213 PDF tests pass; nine rehashed assembly/child
mutations are rejected. No new OCR or source correction; thirty core modules unchanged.

Batch 08 resolves children 0003/0004 at final anchors on PDF 168/176, printed 158/166.
All three child references are final and own no duplicate bodies. Canonical, contents,
opening-outline and body title forms remain separate; the third title's OOP/conjunction
variants are preserved. Five classification sidecars reproduce exactly in fresh processes;
ten parent-relative ranges and nine invalid ownership/anchor cases validate. The parent's
frozen pending-child notes are resolved by an external current disposition, with all
1,524 parent files and source-fidelity limits unchanged. No new OCR/source correction.

Batch 09 completes article 0007, 이영식의 PC 이야기 : 미국 대통령 선거와 컴퓨터,
on PDF 148–152/printed 138–142, and classifies 읽을거리 group 0006 as non-owning.
All 170 article files and one classification sidecar reproduce independently and in
fresh processes. All 45 exact crops, 39 OCR settings, 751 typed ranges, 554 reading
rows, six headings and sixteen boundaries validate. Three independent pull quotations
and a separate attributed closing quotation remain distinct. One source pass, no OCR
retry or crop repair; printed dates, numbers, wording and claims remain literal.

Batch 10 preserves the look-and-feel article 0008 opening on PDF 186–191/printed
176–181 as an immutable partial native. All 306 files reproduce independently and
in a fresh process; 76 exact crops, 74 selected OCR outcomes and 1,845 typed ranges
validate. Its table retains 29 data rows/203 cells plus seven headers: 46 blank
positions, 98 circle candidates, one partial-circle marker and two faint name spans.
Two five-entry lists and fifteen prose boundaries remain explicit. One source pass
was paused for one wider prose crop; 74 initial recognitions plus one changed-crop
recognition, 73 unchanged raw/TSV results reused, zero unchanged-input retries.
Fourteen row crops were repaired before OCR. A failed statistics preflight is retained;
source text/cells were unchanged. Source title/credits, amounts and citations stay literal.

Batch 11 preserves continuation 192–197/printed 182–187 as immutable native b:
340 independently exact files, 86 exact crops, 82 OCR outcomes, 559 reading rows
and 970 typed ranges. Four original panels retain ten window diagrams and a separate
case chart; eleven captions, sixteen claim occurrences and thirteen prose boundaries
validate. Two right-column advertisements are excluded. All raws were read before
one source pass; no retries. Two pre-OCR map revisions repaired ten distinct crops
in eleven events. Repeated B1 labels and source spelling variants remain literal.
All source body pages 186–198 now have direct ownership/continuity review;
186–197 are preserved across natives a/b. Availability stays partial.

Batch 12 preserves final PDF 198/printed 188 above its lower advertisement: 25 exact files,
five crops, four outcomes, 56 rows and 82 ranges. All thirteen look-and-feel body
pages 186–198 are preserved across a/b/c; actual assembly remains required.
The same batch preserves article 0009 opening 200–204/printed 190–194: 266 exact files,
66 crops, 64 outcomes, 571 rows, 890 ranges and two original images. Its actual
ending 205/195 is observed; final 205 remains deferred. All 68 raws read before one
source pass, zero retries; 55 law crops repaired before OCR, two schema preflight
failures retained. Canonical title/byline/parent and literal source variants stay intact.

Batch 13 delivers the complete readable look-and-feel assembly on 186–198:
679 exact files from three independently regenerated natives/671 files. All 2,897
projected metadata ranges, including 92 blank anchors, and 5,632 current typed
occurrences validate. Both cross-native joins, all table/claim/figure indexes and
native-a original execution provenance remain explicit. Nine invalid cases are
rejected, including a rehashed root blank-anchor edit. No new assembly OCR/source pass.
The same batch preserves final 205 of article 0009:49 exact files, 11 crops, ten initial
outcomes, 116 rows and 167 ranges. All six body pages 200–205 now preserved across a/b;
actual assembly remains required. One source pass, zero retries/crop repairs.

Batch 14 completes the actual readable article 0009 assembly on PDF 200–205:
323 exact files from two regenerated natives/315 files. All 1,057 projected metadata
ranges, 2,045 current ranges, 77 crops and 74 outcomes validate. Its cross-native
join, two independent quotations, source title forms and original images remain
explicit. Group 0010 is non-owning: original contents 4/5 and the repeated section
label above child 0011 on 208 support the decision. Four classification files
reproduce exactly; all ten child identities/parents/body states remain unchanged.
Twelve invalid source/recipe/root/ownership cases are rejected. No new OCR/source pass.

Batch 15 preserves GUI-library child 0011 opening 208–213/printed 198–203:
253 independently/fresh-process exact files, 64 exact crops, 48 blocks, four original
images, 60 selected OCR outcomes and 2,907 typed ranges. All 580 physical code rows,
328 printed numbered rows, 20 numbered blanks, four unnumbered wraps and ten numbered
conditions validate. Printed labels remain separate from C text; source defects and
incomplete/abbreviated fragments stay literal. One source pass; 60 initial plus one
changed-crop recognition, 59 exact raw/TSV outcomes reused with original execution
provenance, zero unchanged-input retries. Three pre-OCR crop repairs, one added panel
heading, one within-pass margin repair and a failed export helper remain preserved.

Batch 16 preserves final 214/printed 204 as an 18-file native: 138 labels, 147 physical
rows, 13 numbered blanks, nine unnumbered wraps and complete original cartoon. Both
raw eng drafts read before one source pass; two initial recognitions, no retries or
crop repairs. The actual complete seven-page assembly contains 280 independently/
fresh-process exact files from two regenerated natives/271 files. All 3,633 projected
ranges, 8,156 current occurrences, 67 crops, 62 selected outcomes and three ZIPs validate.
All 727 physical code rows, 466 numbered rows, 33 numbered blanks and 13 unnumbered
wraps remain explicit. Listing 4 spans 001–331 without a cross-native text merge;
listing bytes equal native concatenation. The abbreviated 212/full 214 functions are
linked as distinct source occurrences. Listing 2 remains its printed fragment.
Ten invalid native/recipe/rehashed-root cases are rejected. No assembly OCR/source pass.

Batch 17 completes child 0012, 필기 문자 인식 시스템의 구현(3) : 필기 알파벳 대문자 인식,
on PDF 216–221/individually read printed 206–211: 241 independently/fresh-process exact
files, 64 exact crops, 48 blocks and eight original images. Three tables retain 148
data cells plus 15 headers and two blanks. Fifty opaque graphic markers retain
source contexts: 45 in tables and five inline.
Six listings retain 319 physical rows, 224 normal numbered rows, 26 numbered blanks,
19 unnumbered wraps and a displaced inline 15: candidate. All 2,446 current typed
ranges and 18 private source ranges validate; eight altered custom-data cases are
rejected. All 56 raws read before one source pass; no retries. Thirteen crop repairs,
one split region and a failed schema preflight are retained. Literal reference conflicts,
printed ellipsis and unrecovered automaton/global.h references remain explicit.

Batch 18 preserves article 0013 opening PDF 222–227/printed 212–217 as a partial
native: 238 independent/fresh-process exact files, 70 exact crops, 46 blocks and
17 original images. Nine diagrams and seven formula panels retain literal source
geometry; 15 variable and 17 function entries retain descriptive annotations and
continuations. All 1,034 current ranges, four private ranges and eight rejection
cases pass. Numbered Listing 1 starts 001–010, including three blanks. All 53 raws
read before one source pass; zero retries. Five pre-OCR edge repairs and a schema
failure remain retained. Direct source credit is 이정윤; the previous forward-note
reading 이정운 is superseded. Canonical title/byline/order/parent remain unchanged.

Batch 19 preserves final 228–230/218–220 as a 57-file native, then actually assembles
all nine pages 222–230: 304 independent/fresh-process exact files from two regenerated
natives/295 files. All 3,469 projected ranges, 7,646 current typed occurrences,
82 source crops, 65 settings and three ZIPs validate. Five complete printed listings
retain 349 numbered rows, 57 numbered blanks and nine physical wraps; 444 physical
code/catalogue rows include the descriptive interfaces. All original diagrams,
formulas, catalogue indexes and literal defects retain current/native contexts.
No cross-native text merge; code bytes equal native concatenation. Original encoded
program/header/picture recovery and execution remain unverified. Eleven invalid
native/recipe/rehashed-root cases rejected. Twelve raws read before one source pass,
zero retries; four pre-OCR edge repairs retained. No new assembly OCR/source pass.

Batch 20 preserves Turbo C article 0014 opening 232–237/printed 222–227:
330 independent/fresh-process exact files, 81 exact crops, 71 blocks and the original
five-episode series panel. Five process stages, eleven compiler/linker items, seven
hidden-bug items and eleven headings retain source contexts. Three code regions
retain 53 physical rows; Listing 1 remains its complete printed fragment without
a closing brace, and the second read example lacks a semicolon. Ten escaped-sequence
occurrences retain differing n/r order. All 1,113 current ranges, four private ranges,
80 settings and ten rejection cases pass. All eighty raws read before one literal
source pass; zero retries. Eight pre-OCR edge repairs and an import-only export
failure retained. Actual ten-page extent 232–241 directly reviewed; availability partial.

Batch 21 preserves final 238–241 as an 87-file native, then actually assembles all ten
pages 232–241: 426 independent/fresh-process exact files from two regenerated natives/
417 files. All 5,648 projected ranges, 12,477 current typed occurrences, 102 exact crops,
99 settings and three ZIPs validate. One closing-prose join retains 컴퓨터 언 / 어는;
code bytes equal native concatenation. Complete Listing 2 retains 616 printed row
occurrences, fifteen numbered blanks and 23 physical wraps, including literal 399→300
and 500→101 restarts. Both start_screen occurrences stay distinct; printed fragment
brace/read semicolon defects and escaped n/r order remain. Seven printed reference
rows and original closing mark/panel retained; lower 241 PCSHELL tip excluded.
Nineteen raws read before one source pass, zero retries/crop repairs; schema failure
retained. Fourteen invalid native/recipe/rehashed-root cases rejected. No new assembly OCR/pass.

Batch 22 preserves article 0015 opening 242–247/printed 232–237 as an immutable
partial native: 454 independent/fresh-process exact files, 118 exact crops, 94 blocks,
nine original images and 109 OCR outcomes. Actual eleven-page body 242–252 is directly
reviewed; prose closes 249, but four printed listings continue through 252 above a
separate lower advertisement. The palette retains 51 searchable labels; Table 2 has
35 data cells/five headers, negative zero and 21 parenthesized color values. Twenty-nine
descriptive declarations retain 31 physical rows and two wraps. All 1,288 current
ranges, four private ranges and 109 source-local transcript pins validate. Screen
caption order 2/1/3/4, independent mathematical sidebar, literal formula/claims and
printed declaration defects remain. One faint operator stays explicitly unresolved
at U+E100; no C++ operator inferred. All raws read before one literal source pass;
80 kor+eng/29 eng, zero retries, 43 pre-OCR crop repairs. Ten altered-data cases rejected.

Batch 23 restores final 248–252 as a 194-file native and actually assembles the full
article 242–252: 657 independent/fresh-process exact files from two regenerated natives/
648 files. All 165 exact crops, 155 settings, 5,372 projected ranges, 10,644 current typed
occurrences/636 empty anchors and 10,470 native-source links validate. One main-prose
join retains 의미있 / 는 조도를 구할 수 있다. with ten explicit intervening items;
the complete independent sidebar stays separate. Four printed listings retain
42/158/158/40 labels, 78 empty program rows including three graphic dividers, 21 wraps
and 419 physical listing rows. Forty descriptive entries retain 45 physical rows.
Three source spans remain explicitly unresolved: opening operator U+E100, Listing 2
operator U+E101 and Listing 3 panel-edge-obscured tail U+E102. Printed colorcontroler,
missing row 137 semicolon, signature/dot defects and literal Listing 3 claim remain.
All 46 raws read before one source pass; 22 eng/24 kor+eng, zero retries, six pre-OCR
repairs. Schema failure retained; seventeen invalid cases rejected, ten rehashed roots.

Batch 24 verifies Fractint article 0016's fourteen-page body 254–267/printed 244–257
and preserves opening 254–259 as a partial native: 250 independent/fresh-process exact
files, 67 exact crops, 47 blocks, nine original images and 58 selected OCR outcomes.
All 794 current ranges, four private ranges and 58 source-local transcript pins pass.
Embedded 26-row Stone Soup parable, three-episode panel/current third, seven fractal
images, first source menu screen/eight captions, printed 1026 versus 10²⁶ erratum and
five option headers/seven syntax rows remain. Twelve technical claims, fourteen file
and thirteen hotkey occurrences retain source contexts. All 58 initial drafts read;
one clipped margin widened, recognized and read before the single correction pass.
57 unchanged raw/TSV outcomes reused with original execution pins; 59 actual calls,
zero unchanged-input retries. Thirteen pre-OCR crop events/twelve distinct repairs,
one split addition and one post-OCR/pre-pass margin repair remain archived. Ten
altered-data cases rejected; eleven boundaries retain sixteen intervening contexts.

Batch 25 preserves Fractint continuation 260–265/printed 250–255 as native b:
346 independent/fresh-process exact files, 88 exact crops, 74 blocks, five original
menu screens and 83 OCR outcomes. All 1,033 current ranges, seven adjacent-native
ranges and 83 source-local transcript pins validate. Twelve assignment headers,
two command rows, four printer-resolution entries/five physical rows, nine hotkey
and five drawing-option descriptions, two exponent partitions and nine boundaries
with eight intervening contexts remain source-linked. Printed Mamimum, Retrive,
maxi/teer, expen-/ded memory, filename/model/case variants and numeric claims stay
literal. All raws read before one source pass; 14 eng/69 kor+eng, zero retries,
two pre-OCR edge refinements. Fourteen altered-data cases rejected. Opening 58 original
execution records/57 reused outcomes revalidated; prior files/core/source exact.
Direct incoming reading is 259 옵션을 / 260 써 줄 필요가 없다.; this supersedes the
earlier prospective 쓸 handoff without rewriting native-a bytes or historical evidence.
Natives a/b preserve twelve pages 254–265; availability remains partial.

Batch 26 preserves final Fractint 266–267 as a 126-file native, then actually
assembles the complete fourteen-page article 254–267: 731 independent/fresh-process
exact files from three regenerated natives/722 files. All 185 exact crops, 170 OCR
outcomes, 2,228 projected metadata ranges, 4,372 current ranges, 4,202 source links,
sixteen private ranges and 170 source-local transcript pins validate. One FPU prose
join retains 옵션을 / 써 줄 필요가 없다.; 265→266 remains separate paragraphs.
Seventeen complete option headers, all original images/menus/series/parable and
closing M mark remain. Final examples retain fifteen code rows and five formula
annotations; nine comment glyphs retain explicit colon/semicolon candidates.
Literal figure references 9/12 remain label mismatches, with null confirmed targets
and unconfirmed semantic candidates after complete body review; no panels invented.
All 29 final raws read before one source pass; zero retries, three pre-OCR margin
repairs. First assembly metadata aliasing failure retained; fresh r02 changes only
three JSON files, with article/listing/native bytes unchanged. Twenty invalid cases
rejected, including thirteen rehashed roots. All prior source/core/evidence exact.

Batch 27 verifies Tetris article 0017's actual eight-page body 272–279/printed
262–269 and preserves opening 272–277 as a six-page partial: 329 independently and
fresh-process exact files, 83 exact crops, 69 blocks, four original images and 79 OCR
outcomes. Nine member descriptions, six examples, three diagrams with searchable
lettering and the closing M remain. Complete Listings 1/2 and partial Listing 3 retain
191 printed labels, 38 numbered blanks and 252 physical code rows. Three panel-border
comment tails and two string blank-width candidates remain explicitly uncertain.
All 3,064 typed ranges/162 empty occurrences, six private ranges and 79 source-local
pins validate; nine joins/ten boundaries retain 23 intervening source contexts.
All raws read before one literal source pass; 12 eng/67 kor+eng, zero retries, one
pre-OCR label-margin repair. Source is_sts, missing example return type and aligned
annotation wraps remain literal. Fifteen altered-data cases rejected; failed preparation
and two verifier revisions retained without source/package changes.

Batch 28 preserves final Tetris 278–279 as a 41-file native, then actually assembles
all eight pages 272–279: 379 independently/fresh-process exact files from two
regenerated natives with 370 files. All 91 source crops, 87 settings, 6,527 projected
ranges, 13,252 current ranges/820 empty occurrences, 13,165 source links, thirteen
private ranges and 87 source-local pins validate. Five complete listings retain
506 labels, 100 numbered blanks and 567 physical code rows. Nine member descriptions,
six examples, 22 function definitions/three inline definitions, three diagrams with
searchable lettering and the closing M remain. Code bytes equal native concatenation;
Listing 3 rows 19/20 span the native boundary without a logical code-line merge.
Four border-obscured tails remain explicit, including the new program tail U+E103.
Original blank-string widths, glyphs/spaces/encoded bytes and execution are unverified.
All eight final raws read before one literal source pass; six eng/two kor+eng, zero
retries/crop repairs. Failed helper/import and pin-path verifier checks retained;
fresh revisions pass without source/OCR changes. Twenty invalid cases rejected,
including thirteen consistently rehashed roots. Earlier files and core remain exact.

Batch 29 preserves year-in-review feature 0019's confirmed opening on PDF 299 as
a partial package: 33 independently/fresh-process exact files, seven exact crops,
six text blocks and the original full-page composition. All six kor+eng raw drafts
were read before one literal source pass; zero retries or crop repairs. Two introductory
paragraphs, title/credit/outline forms, eighteen physical reading rows including one
blank separator, 48 current typed ranges and two private boundary ranges validate.
Twelve consistently rehashed false ownership/folio/extent/completion/absence/recovery/
glyph claims are rejected. Earlier packages, source, reference files and core stay exact.

Source evidence supersedes the prior provisional handoff: PDF 299 has no visible
printed folio; 289 is its canonical contents reference. Physical 300–305 print 325–330
and contain unrelated shell listings. Page 306 is advertising; 307–317 contain the
separate vaccine-toolkit article. Only opener 299 is confirmed feature content in
this bounded review. Its continuation, intrinsic section bodies and ending remain
unlocated. No 299–304 extent, missing-page count or source-wide absence is inferred.
Children 0020/0021 remain unresolved; the opening outline is not a final body anchor.

Batch 30 reviews twenty additional outside pages, 290–297 and 318–329: twelve
full advertisements and eight vaccine-toolkit pages with locally read folios 343–350.
No feature 0019 continuation was found in that bounded range. The combined forty-page
source index for 290–329 and external pending disposition reproduce as three exact
files independently and in a fresh process. Forty source images/pins, all current
observation/layout pins and eight invalid disposition cases validate. No mapping,
OCR, source pass, article-package change or other canonical classification is added.
The immutable opening and original gap metadata remain exact. Its body location,
ending and children 0020/0021 are still pending; no missing-page count, source-wide
absence or complete feature recovery is inferred.

Batch 31 preserves vaccine-toolkit article 0024 opening PDF 307–312/individually
read printed 332–337 as a partial native: 302 independently/fresh-process exact files,
83 exact crops, 59 text blocks and thirteen original images. All seventy complete
raws were read before one literal source pass; four eng/66 kor+eng, zero retries or
within-pass crop repairs. One schema preflight failure, 26 pre-OCR edge refinements
and an export metadata helper failure remain retained. Fresh helper/input copies
repair the continuation pairing with unchanged map/crop/raw/TSV/settings bytes.

Three classification trees retain 39 source-linked nodes; two hierarchical analysis
outlines retain 29 entries. Twelve improvements, eight limitations and ten construction
steps retain thirty numbered entries and all continued fragments. Five diagrams
retain thirty searchable labels; portrait, source title/credit forms and two original
assembler panels remain intact. Four boxed return-key graphics stay explicit markers,
without inferred control bytes. Literal ASH filename, MASM colons, physical filename/
procedure wraps, historical claims and source terminology remain unchanged.
All 1,067 current ranges/eleven blank occurrences, two private boundary ranges, seventy
transcript pins, 453 reading rows and six code rows validate. Eighteen rehashed invalid
cases are rejected; earlier packages/evidence/source/reference/core remain exact.

Batch 32 preserves continuation PDF 313–318/individually read printed 338–343
as native b: 328 independently/fresh-process exact files, 88 exact crops, 77 blocks
and eleven original images. All 77 complete drafts were read before one source pass;
seven eng/seventy kor+eng, zero retries or within-pass crop repairs. Eleven distinct
pre-OCR edge repairs/twelve events and inherited map-note correction are retained.

Nineteen detailed procedure descriptions retain 308 physical parts, eighteen procedure
continuations and one main-prose continuation across intervening diagrams. Fifteen
result rows/thirty cells, eight byte-layout diagrams/64 fields, an opaque wavy omission
and sixteen printed dump offsets/256 hex-token candidates remain source-linked.
All 2,235 current typed ranges/seven blank occurrences, 532 reading rows and 26 physical
code/data/dump rows validate. Incoming 312 프 / 313 로시져는 retains both native contexts.
Both FFFFh values have four F letters. Source 92h prose/diagram agree on four registers
with CS/SS adjusted by 10h; earlier prospective conflict wording is superseded.
PPSur remains the u-shaped identifier candidate with PPStr alternative. Source wording,
register/error omissions, 주 000 and physical wraps stay literal; no byte recovery claim.
Initial helper compilation failure and a metadata-only export revision are retained;
509 copied execution inputs and article/listing bytes remain exact. Twenty-one rehashed
semantic mutations are rejected. Earlier packages/evidence/core/reference remain exact.

Batch 33 preserves PDF 319–324/individually read printed 344–349 as native c:
324 independently/fresh-process exact files, 90 exact crops, 75 blocks and fifteen
original images. All 75 complete drafts read before one source pass; 32 eng/43 kor+eng,
zero retries or within-pass repairs. Eight pre-OCR edge repairs remain retained.

All 5,643 current typed ranges/435 blank occurrences, four private boundary ranges,
688 reading rows and 523 code/data/dump rows validate. Printed Listings 2/3/4 retain
412 labels and all 61 numbered blanks; unnumbered Listing 1 has 29 rows/nineteen EXTRN
declarations. Three prose continuations and five code continuation associations retain
source contexts. Three dump panels preserve 832 visible tokens plus three concatenated
jump-pair candidates, explicit omission, partial rows and original annotations.
Eight opaque banner runs and the literal 12Ah* candidate remain unverified glyphs.
Listings 2/3/4 captions and program banners remain conflicting source occurrences.
The original prose closing M and boxed historical user notice remain separate.
A fresh metadata-only revision fixes numbered-row flags while preserving 505 original
execution inputs and all article/listing bytes. Twenty-four rehashed invalid cases are
rejected. All prior packages/evidence/core/source/reference remain exact.

Batch 34 preserves final 325/printed 350 as a 36-file native, then actually assembles
all nineteen vaccine-toolkit pages 307–325: 999 independently/fresh-process exact files
from four regenerated natives/990 files. All 270 exact source crops, 228 OCR settings,
206 blocks, 42 original images and five ZIP CRCs validate. Final six complete raws read
before one literal source pass; five eng/one kor+eng, zero retries. Two pre-OCR crops
repaired in four retained events. No assembly OCR/source pass or core changes.

All 10,109 projected native metadata ranges, 22,641 current ranges/1,640 empty
occurrences and 22,387 native source links validate. Eleven literal prose joins retain
source wraps; code bytes equal native concatenation. Five complete printed listings
retain 571 labels/88 numbered blanks, plus unnumbered Listing 1/nineteen EXTRN
declarations. Final inset labels 121–131 follow main 120; blank 103→104 remains
separate physical rows. Four caption/banner conflicts, unknown dump/layout omissions,
partial dump rows, identifier/star candidates and independent historical notice remain
explicit. Four return-key and ten banner markers retain fourteen scoped meanings,
including overlapping PUA code points in a/c. Original native bytes are unchanged.

Original a/b/c execution-map/crop/raw/TSV/settings inputs revalidate through 494/509/505
copied files. One audit helper import failure is retained; fresh audit_r02 fixes helper
lookup only. Twenty-nine invalid cases are rejected, including twenty-two consistently
rehashed roots through guarded assembly checks. All 35,119 prior December files,
6,795 prior selected files, ten classification files, 9,332 September reference files
and thirty core/source/runtime/TOC/queue pins remain exact. Unchanged 213-test baseline
reused with complete current audits; no generic custom-metadata validation claim.

Batch 35 reviews twenty further complete views, physical 280–289 and 330–339:
all full advertisements, with no confirmed visible magazine folios. Neither UNIX
opening appears in these twenty pages. Ten exact source views reused and ten new
3000px renders retained; no mapping, OCR, source pass or package change. Promotional
newspaper clipping on 339 remains part of an advertisement, not a magazine article.

The combined non-owning source index now covers sixty physical pages 280–339.
Three index/disposition files reproduce independently and in a fresh process; all
sixty source images/pins, twenty current source/layout observations and sixteen
private altered-data cases validate. UNIX 0022/0023 retain unresolved classification,
null ownership/restoration and pending opening/extent locations. The prior shell
continuation on 300–305 does not establish either independent opening or complete
extent. No missing-page count, final unavailable outcome or source-wide absence
inferred. All earlier packages, feature 0019 partial/children, classification outcomes,
6,840 selected files, ten classifications, 9,332 September reference files and thirty
core/source/runtime/TOC/queue pins remain exact. Unchanged 213-test baseline reused;
private search checks do not claim generic schema or full-source coverage.

Batch 36 preserves utility article 0026 opening PDF 361–366/individually read
printed 386–391 as a 427-file immutable partial native. Its actual eleven-page body
361–371 is directly reviewed: prose closes 366, but four printed listings continue
through DEFINE.H label 76 on 371 above an independent advertisement. Full-page
advertisements 360/372 and independent Norton opening 373/398 bound the article.
Group 활용 0025 is non-owning from original contents/body anchors; child 0027 stays
unresolved. One classification record with ten source pins reproduces independently
and in a fresh process, separately from the article files.

All 112 exact crops, 102 settings, 3,038 typed ranges/17 blank occurrences, 696 reading
rows and 154 code/data/dump rows validate. Ten original figures retain the memory
diagram's 21 labels, a nine-row/four-column table and seven console rows. Figure 4
retains thirty displayed offset rows/480 hex candidates, separately read ASCII,
nine scoped opaque runs, four annotations and an unknown dotted omission. No unseen
bytes, missing-row count or decoded program is inferred. Example 1 preserves its
3/1/3 rows; Example 2 preserves thirteen fields/descriptions and punctuation candidates.
Eight function descriptions, eight usage options/sixteen cells, four examples/eight
cells and thirteen prose continuations remain source-linked.

All 102 complete drafts read before one literal source pass; 26 eng/76 kor+eng,
zero retries or within-pass crop changes. Sixty-two distinct pre-OCR crop repairs
in seventy events, initial map schema failure and within-pass punctuation refinement
remain preserved. Printed defalut, absent final function brace, colon-shaped C
punctuation, two dot-pair :: candidate/|| alternative, physical wraps and shell
placeholder-count differences stay literal. Editorial material, attributed quotation,
historical warning and prose-closing mark remain separate. Exact glyphs/spaces/bytes,
source claims, original programs and execution remain unverified.

Three native exports match; all PNG decodes/ZIP CRCs and twenty-eight private invalid
cases pass: twenty-two rehashed native edits plus six group edits rejected. These
are frozen source-specific checks, not generic custom-schema validation. A metadata-only
revision fixes the final label 076→76, preserving 659 copied execution inputs and
article/listing bytes. A verifier runtime-base error is retained with its repaired
helper. All 36,400 prior December files, 6,840 former selected files, ten former
classifications, 9,332 September files and thirty core/source/runtime/TOC/queue pins
remain exact. Unchanged 213-test baseline reused; no core or reader changes.

Batch 37 restores final utility pages 367–371/individually read 392–396 and actually
assembles the complete eleven-page article 361–371. All 621 files match independent
and fresh-process exports from two regenerated immutable natives/612 embedded files.
The final five-page native has 185 exact files. Thirteen literal prose joins retain
intervening panels and physical source wraps; no prose join across 366→367 or physical
code-line merge. All code bytes equal native concatenation. Original native scope
notes remain historical, with an explicit current complete-assembly disposition.

All 165 exact crops, 143 settings (63 eng/80 kor+eng), 9,434 projected native ranges,
19,178 current typed ranges/440 blank occurrences and 18,985 native source links validate.
All 22 original images, 165 PNG decodes and three ZIP CRCs pass. Four complete printed
listings retain 708 labels, 29 numbered blanks, seven unnumbered wraps and 715 listing
rows. The full source index retains 1,415 reading rows and 869 code/data/dump rows.
Eighteen definitions, sixteen prototypes, nineteen macros and fourteen full-header
fields remain source-linked. Caption/prototype filename forms stay separate.

All 41 complete final-page raws read before one literal source pass; 37 eng/four kor+eng,
zero retries or within-pass crop changes. Thirty pre-OCR repairs retain first-map crops
and reuse 23 unchanged crops. The unreliable pixel-only number-band probe is preserved
as geometry evidence, not recognition. Twenty later graphic/string-divider runs and
nine earlier ASCII runs retain 29 scoped markers without inferred widths/bytes.
Literal defalut, ::/|| alternatives, caret-shaped ^= candidates, physical wraps,
quote/punctuation/blank-width candidates and spelling/claims remain. Full listing's
brace does not repair the inline fragment; header's extra path field does not backfill
Example 2. Earlier tables/dump/quotation/historical warning stay intact.

Thirty-one consistently rehashed root/recipe/native mutations are rejected through
frozen source projection and guarded assembly checks; no generic custom-schema claim.
All 39,177 prior December files, 7,267 former selected files/fifteen roots, eleven
classifications, 9,332 September files and thirty core/source/runtime/TOC/queue pins
remain exact. Unchanged 213-test baseline reused. No new assembly OCR/source pass or
core/reader changes; exact glyphs/spaces/encoded files, technical/historical truth,
execution, human acceptance and full proofreading remain unverified.

Batch 38 completes Norton Desktop article 0027 on PDF 373–376/individually read
398–401, credit 탁연상. All 202 selected JSON/assets files reproduce independently
and in a fresh process. All 53 exact crops, 47 kor+eng OCR settings, 34 blocks,
351 reading rows and 654 typed ranges validate. Five complete screenshots and the
separate closing M remain; seven headings, eight prose groups and thirteen continuation
boundaries preserve physical wraps. Full advertisement 372 and independent frame-grabber
opening 377 bound the four-page body, including the final two figures below the conclusion.

Five external Figure 1 annotations and selected Figure 5 chart labels retain direct
source contexts: two titles, four categories and two legend candidates. Tiny UI/file
names, chart numerals/axis/summary values and units are not exhaustively transcribed;
original pixels remain authoritative. Fifteen utility catalogue entries, three calculator
subtypes, four numbered group improvements, Quick Access note, three unrecovered prose
filename references, seven historical claims and twelve source variants remain explicit.
No original software/data/file recovery, chart dataset or current security advice claimed.

All 47 complete raws read before one literal source pass; zero OCR retries or within-pass
crop changes. Eleven pre-OCR crop repairs retain the initial map/crops and reuse 42 crops
exactly. Empty/failed tiny-label drafts remain preserved. A fresh metadata revision fixes
repeated-word continuation-tail pointers; all 258 execution input files and article bytes
remain exact. First export/helper retained. Seventeen consistently rehashed custom-data
edits pass generic exports but fail the frozen private source audit; no generic custom
schema claim. All 40,530 prior December files, 7,461 former selected files, eleven
classifications, 9,332 September files and thirty core/source/runtime/TOC/queue pins remain
exact. Unchanged 213-test baseline reused; no core or reader changes.

Batch 39 preserves frame-grabber article 0029 opening PDF 377–382/locally read
402–407 as a 361-file immutable partial native and classifies hardware group 0028
as non-owning. All twenty body pages 377–396/402–421 are directly reviewed: prose
closes 390, but three listings continue through END 118 on 396 above a separate
subscription notice. Independent laser-printer article opens 397; its source credit
김현숙 기자 stays separate from canonical 편집부, with child 0030 still unresolved.
Remaining fourteen frame-grabber pages and actual twenty-page assembly are required.

Three native exports and three one-file group exports match, including fresh processes.
All 95 exact source crops, 86 kor+eng settings, 78 blocks, nine original images,
874 reading/search rows and 3,150 typed ranges/14 empty occurrences validate.
Nine tables retain 346 data cells/43 headers: five printed blank parts cells and two
separate editorial blank slots within a dotted-omission row. Seven pinouts retain
110 printed label/number pairs; twelve circuit component blocks plus four gate
reference forms, six main headings, six prose groups/eight joins and thirteen source
variants remain explicit. Ninety-three editorial graphic markers do not assign original
glyph counts, missing rows, valid logic, a netlist or a numeric timing series.

All 86 complete raws read before one source pass; zero retries or within-pass crop
changes. Twenty-six pre-OCR crop repairs/two added details retain initial 93 crops;
67 initial crops and 94 final-revision copies are exact. Nine source-only enlarged
circuit details support literal candidates. Failed padded-filename pin comparison,
first copy, all maps/crops/raws and in-pass typing/layout refinements remain retained.
Twenty private altered-data cases pass their rejection checks: fourteen consistently
rehashed natives pass generic export checks but fail frozen source audit; six group
edits fail classification checks. All 41,739 prior December files, 7,663 former selected
files, eleven earlier classifications, 9,332 September files and thirty core/source/
runtime/TOC/queue pins stay exact. Unchanged 213-test baseline reused; no core changes.

Batch 40 preserves frame-grabber continuation PDF 383–388/individually read folios
408–413 as a 460-file immutable native b. Three independent/fresh-process exports
match. All 121 exact source crops, 110 settings (14 eng/96 kor+eng), 101 blocks,
eleven original panels, 664 reading/search rows and 2,509 typed ranges/36 empty
occurrences validate, including three private adjacent-native ranges. Natives a/b
now preserve twelve pages 377–388; remaining 389–396 and actual assembly are required.

Twelve regional table panels retain 324 data cells and 44 headers, including eighteen
unfilled device/merged-bit layout slots without carried-forward values. The memory
pinout retains 28 label/number pairs; slot tables retain 62 pin/name/use-mark entries.
O/X remain glyph candidates with unverified O/zero encoded identity. Two comparator
blocks and eight passive candidates retain LM219, R?, 0.1uF and stacked 1/1 forms.
The complete original circuit remains authoritative; no pin-11 assignment or netlist
is validated. Six flow steps, thirty editorial graphic markers, fifteen main headings,
two independent asides, 21 source variants and nine prose joins remain explicit.

Fourteen code/example regions retain 29 physical example rows plus six separately
indexed marginal flow-step labels and fifteen colon-shaped terminal candidates.
Literal 32×124, SD?, Comparater, ClocK/CLeaR, OWS, IRQ9, out_.data, midline-dash
identifiers, read_data1() and printed ②와 ③ remain candidates. Source code, arithmetic,
models and references are not repaired. Original electronic/software files, encoded
glyph/space identities, technical validity and execution remain unverified.

All 110 complete raws read before one literal source pass; zero retries or within-pass
crop changes. Twenty-five pre-OCR repair events across 22 distinct crops/three added
details retain the initial map/crops and reuse 96 initial/117 preceding crops exactly.
Nine 3x original-pixel details were directly reviewed without recognition. First export
retained; a fresh metadata revision separates flow labels from physical code rows.
All 708 execution inputs and article/listing bytes remain exact; four exported JSON
files change. Eighteen consistently rehashed custom-data edits pass generic exports
but fail the frozen private audit; no generic custom-schema enforcement claim.
All 43,097 prior December files, 8,024 former selected files, twelve classifications,
9,332 September reference files and thirty core/source/runtime/TOC/queue pins remain
exact. Unchanged 213-test baseline reused; no core changes.

Batch 41 preserves frame-grabber continuation PDF 389–394/individually read folios
414–419 as a 254-file immutable native c. Three independent/fresh-process exports
match. All 65 exact source crops, sixty settings (25 eng/35 kor+eng), 55 blocks,
five original panels, 949 reading rows and 6,749 typed ranges/668 repeated empty-anchor
occurrences validate, including three private adjacent-native ranges. Natives a/b/c
now preserve eighteen pages 377–394; final 395–396 and actual assembly remain required.

Twenty-five code crops retain all 712 printed labels and physical rows: complete
Listing 1 header 01–44 and current Listing 2 C001–668. Ninety-three numbered blanks,
no unnumbered wraps, 23 fragment continuations and 423 punctuation candidates validate.
Nineteen scoped markers preserve thirteen divider runs, one char-literal middle glyph,
one exclamation-like string run and four rectangle rows without original counts/bytes.
Eleven function definitions include ten complete printed bodies and partial col_6;
fourteen prototypes, 38 header/five C macros, six includes and twenty variants remain.
Colon/dot-pair/caret/1-l/II-ll-11 candidates, filenames and printed defects stay literal.

The complete construction inset spans two original gray panels, with seven priced
parts entries plus a separate budget claim, seven numbered steps and six tips. Five
main improvements, six references, source contact and closing M remain separate.
Five prose joins retain physical wraps. Incoming 388 몇 가지 / 389 영상처리를 해보는 일만이
남아 있다. retains both native downloads/scans and the intervening lower flow drawing.
Current C668 continues as numbered C669 on 395; no physical code-line merge or inferred
valid code. Prose M on 390 does not end the article; final C/ASM listings remain.

All sixty complete raws read before one literal source pass; zero retries or within-pass
crop changes. Ten pre-OCR margin repairs retain the initial map/crops and reuse 55 crops
exactly. Five 3x original-pixel details reviewed without recognition. Initial assistant
notes counted eight costs; the actual transcript/first export already had seven priced
entries. A fresh metadata disposition corrects current wording while retaining those
notes and the first export. All 398 execution inputs and article/listing bytes remain
exact; four exported JSON files change. Twenty consistently rehashed custom-data edits
pass generic exports but fail the frozen private audit; no generic custom-schema claim.
All 46,032 prior December files, 8,484 former selected files, twelve classifications,
9,332 September reference files and thirty core/source/runtime/TOC/queue pins remain
exact. Unchanged 213-test baseline reused; no core changes.

Batch 42 restores final PDF 395–396/individually read folios 420–421 as a 53-file
immutable native d, then actually assembles the complete twenty-page frame-grabber
article 377–396/402–421. Article 0029 is now readable/sample-reviewed. Three complete
1,137-file exports match, consuming all 1,128 independently regenerated native files.
Historical natives and their scope notes remain unchanged, with an explicit current
complete-assembly disposition. Canonical identity/title/parent/reference remain exact.

All 292 original source crops, 267 OCR outcomes/settings, 243 blocks, 25 figures and
2,761 reading rows validate. All 14,753 projected native ranges and 29,916 current typed
ranges pass; 1,956 repeated empty-anchor occurrences are separate from printed blanks.
Two actual prose joins 382→383 and 388→389 retain physical wraps and intervening panels.
C668/C669 remain separate numbered physical rows. All 292 PNGs and five ZIP CRCs pass.

Three printed listings retain 985 labels/physical rows: header 44, C 823 and ASM 118,
ending END above the independent lower-396 subscription notice. All 129 numbered blanks,
zero unnumbered wraps and 32 fragment continuations remain. Earlier 29 inline code rows
and six marginal flow labels stay separate. Fifteen C function candidates include the
complete cross-native col_6 body; two ASM PROC/ENDP pairs remain. VERT_SYNC2 is a comment
reference; no unprinted routine or valid-code repair is supplied.

Complete custom projection retains 21 table panels/757 cells including headers, 138
pinout pairs, 62 slot entries, circuit/passive/flow candidates, 123 graphic markers,
24 opaque runs with unknown original counts/bytes, 536 punctuation candidates, fifteen
inline terminal candidates and seventy source variants. Seven priced entries and the
retained eight-to-seven assistant-note disposition, seven construction steps, six tips,
five improvements, six references and contact remain separate. Printed defects and
glyph/filename/claim differences remain literal; original files and execution unverified.

All eleven final complete raws read before one literal pass: ten eng/one kor+eng,
zero retries or within-pass crop changes. One pre-OCR lower-margin repair retains the
initial map/crops and ten exact crop copies. Four 3x original-pixel details reviewed
without recognition. Native d preserves 273 labels/36 numbered blanks, five opaque runs
and 113 punctuation candidates. OCR-omitted directives/blank labels restored from scans.

Twenty-five consistently rehashed root/recipe/native edits fail the frozen private
projection/check_assembly; no generic custom-schema claim. All 47,685 prior December
files, 8,738 former selected files, twelve classifications, 9,332 September reference
files and thirty core/source/runtime/TOC/queue pins remain exact. Unchanged 213-test
baseline reused; no core changes or new assembly OCR/source pass.

Batch 43 completes laser-printer article 0030 on PDF 397–402/individually read folios
422–427. The source byline 글. 김현숙 기자 remains separate from canonical credit 편집부;
title/kicker differences also remain explicit. The upper-402 conclusion/M ends the body,
above an independent lower advertisement. Previous 396 ends the frame-grabber; following
403 opens the timetable article, continued 404–405. Other identities remain unchanged.

Three 423-file exports match, including a fresh-process rebuild. All 106 exact source
crops, 103 pinned kor+eng outcomes, 88 blocks, three figures, 498 reading rows and 1,104
typed ranges validate. Eleven empty-anchor occurrences retain blank separator contexts.
Thirteen joined groups retain fifteen fragment boundaries: fourteen prose and one list
continuation. Main prose 399→401 passes around all nineteen independent sidebar regions
on 400. All 106 PNG decodes and one ZIP CRC pass; no source code or original-file recovery.

Thirty-two status/error-message entries retain 36 physical rows and seventeen description
groups. Four wrapped messages, PF/PE headings, OVERFLAW, Q/O candidate in QVERFLAW,
MALFUCTION and REMENBER remain literal. Thirteen uncoded symptom sections and five blank-
output bullets retain their printed claims. Missing codes or technically valid descriptions
are not supplied. Old araea, Selt/Self, 흔적/혼적 and button glyphs remain source candidates.

Complete original Figure 1 retains four photographic components and an optical diagram,
with eleven indexed external labels. Printed mirorr/lense remain distinct from body mirror.
The rotated drum detail retains unknown glyph identities/counts/bytes, without invented
readable words. Tiny photographic product-label writing is not exhaustively transcribed.
The independent principle sidebar retains its 동진전산(kts146) 끝. credit; the main electrical
precaution remains historical source text with no present technical or safety certification.

All 103 complete raws read in three untruncated outputs before one literal source pass;
zero retries or within-pass crop changes. All 106 initial crops reviewed on 29 sheets.
Thirty-six pre-OCR events in 35 distinct regions were reviewed on nine repair sheets plus
one final crop. Seventy-one initial and 105 preceding crops remain exact. Four enlarged
source-only details were reviewed without recognition. All maps, crops, raws and corrections
remain archived. Technical claims and source spelling/physical wraps remain unrepaired.

Twenty consistently rehashed custom-data edits pass generic exports but fail the frozen
private audit; no generic custom-schema claim. All 49,105 prior December files, 8,800
former selected files, twelve classifications, 9,332 September files and thirty core/source/
runtime/TOC/queue pins remain exact. Unchanged 213-test baseline reused; no core changes.

Batch 44 classifies information-sharing heading 0031, 정보나눔터, as non-owning,
and preserves timetable article 0032 opening PDF 403–408/printed 428–433. Fourteen whole
views verify the actual nine-page body 403–411/428–436. Final Listing 1 GLOBAL.BAS,
conclusion/M, contact and disk notice occur on 411 above an independent advertisement;
412 is a full advertisement and 413 opens the technical section. Final 409–411 and
actual assembly remain required. Canonical identity, credit 정보문 and parent stay intact;
source affiliation 장항고등학교 교사, editorial deck and section introduction stay separate.

Three 304-file opening exports match, including a fresh-process rebuild. All 77 source
crops, 73 pinned kor+eng outcomes, 58 blocks, four original screens, 655 reading rows and
1,159 typed ranges validate. Twenty-nine empty anchors retain blank separator contexts.
Twelve joined groups/fifteen boundaries retain physical wraps and explicit intervening
screen/heading contexts. Two control tables retain 32 rows/64 cells; two four-row numerical
examples retain eighteen label/value pairs/36 cells without arithmetic repair. Table tabs
are presentation separators, with no original encoded-spacing claim.

Four original screens and separate captions remain intact; tiny embedded lettering is
not exhaustively transcribed. The independent Visual Basic sidebar, 61 button occurrences,
eight printed-file reference occurrences and ten source variants retain explicit contexts.
The file-reference index is not an original-file inventory. Old araea, PR/PRJ, 붙히고,
identifier wraps and word/glyph candidates remain source-linked; no valid program or
original executable/source/forms/data/disk recovery or execution is inferred.

All 73 complete raw drafts read in three untruncated outputs before one literal source
pass, zero retries or within-pass crop changes. All 77 initial crops reviewed on 22 sheets;
eleven pre-OCR repairs reviewed on three sheets, with 66 initial crops reused exactly.
Five source-only enlarged details reviewed without recognition. Two initial schema
preflight failures and two export-helper failures remain archived; all recognition and
reviewed-text bytes remain exact across export revisions. No separate source-pass-start
timestamp was saved; the method and raw-reading/end timestamps are retained.

Original contents 5, repeated information-sharing headers and independent opening 403
support group 0031. Eight source anchors and all seven canonical children/order/parents
remain explicit. Three one-file classification exports match; seven invalid edits fail
the private guard. No duplicate body, divider, package, download or nested hierarchy added.
Eighteen consistently rehashed native-metadata edits pass generic exports and fail the
frozen private audit; no generic custom-schema claim. All 50,620 prior December files,
9,223 former selected files/eighteen roots, twelve classifications, 9,332 September files
and thirty core/source/runtime/TOC/queue pins remain exact. Unchanged 213-test baseline reused.

Batch 45 preserves final timetable pages 409–411/printed 434–436 as a 172-file native,
then actually assembles complete article 0032 on PDF 403–411/individually read 428–436.
Three 485-file assemblies match, including a fresh-process build, from two independently
regenerated immutable natives/476 files. Both native metadata and bytes remain exact;
earlier partial-scope notes now have an explicit complete-assembly disposition.

All 120 source crops, 113 OCR outcomes, 90 blocks, seven original panels, 1,012 reading
rows, 1,928 projected native ranges and 3,861 current typed ranges validate. There are
138 repeated empty-anchor occurrences and 3,769 current/native projection pairs. One
literal 408→409 prose join retains 노란색으로 / 변한다. with both original source contexts.
All physical wraps, eighteen internal groups and 22 fragment boundaries remain explicit.
All 120 PNG decodes and three ZIP CRCs pass; no new assembly OCR or source correction.

The complete two-column printed GLOBAL.BAS listing retains 67 physical code/blank rows,
nine blank contexts and 26 printed declaration rows, without printed line numbers or
unnumbered wraps. Code bytes equal the final native. Printed techer/TECHER spellings,
unuseable, nl/t123/week1 and other 1/l candidates remain literal. The small 덤/멤 comment
and DIVISISU/DIVSISU/DIMSISU form-filename alternatives remain unresolved source candidates.
No valid-code repair, unprinted implementation or original encoded file recovery is inferred.

Two control tables retain 32 rows/64 cells; two numerical examples retain eighteen pairs/
36 cells. The worked example has four rows/twelve cells; four file catalogues retain
nineteen entries. The independent Visual Basic sidebar, four screens, command contexts,
twenty source variants, conclusion/M, historical contact and disk-availability notice remain
separate. Listing and notice original panels intentionally overlap searchable text. Tiny
screen lettering is not exhaustively transcribed. The independent lower-411 advertisement
is excluded; 412 is a full advertisement and 413 opens the technical section.

All forty final-segment complete raws read in two untruncated outputs before one literal
source pass: two eng code/38 kor+eng other regions, zero retries or within-pass crop changes.
All 43 initial crops reviewed on twelve sheets; four pre-OCR repairs reviewed on one sheet,
39 initial crops reused exactly. Five source-only enlarged details reviewed without OCR.
An audit-helper archive-count preflight failure is retained and corrected; no delivery bytes
changed. The native also matches a separate fresh-process build.

Twenty-five consistently rehashed root/recipe/native edits fail the frozen private
projection/check_assembly; no generic custom-schema claim. All 52,609 prior December
files, 9,527 former selected files/nineteen roots, thirteen classifications, 9,332 September
files and thirty core/source/runtime/TOC/queue pins remain exact. Unchanged 213-test baseline
reused; only 0032 advances. Information-sharing heading 0031 and other child states stay intact.

Batch 46 completes article 0034, @Get...Read입력을 메뉴로 하자, on PDF 413–414/
individually read folios 438–439, and classifies technical heading 0033 as non-owning.
The source title/byline 최익성 stay separate from the heading/editorial invitation.
Heading reference 438, article null reference, both canonical parents 0031 and all
identities/order remain unchanged. Five technical tips remain canonical siblings;
no children are invented under 0033 and no duplicate body/package/download is assigned.

Three 58-file article exports match, including a fresh-process build. All thirteen
exact article crops, twelve outcomes, nine blocks, one original table panel, 108 reading
rows and 251 typed ranges/five empty anchors validate. Three prose joins preserve physical
rows, including the 413→414 disk-notice continuation. Upper-middle 414 ends 장점이 있다.
before independent MODECON and monitor-tip bodies; 415 opens an independent Clipper article.
No closing M mark is invented. Two inline code examples retain seventeen physical rows,
including a three-row annotated assignment and two colon-shaped omission marks. Printed
! =, & &, CHR without dollar sign, Korean placeholders, arrows and physical wraps remain
literal. No valid-code repair or unprinted implementation is supplied.

The code/name table retains two headers, five pairs/twelve readable cells and two opaque
lower vertical-dot-run contexts. U+E601/U+E602 each represents an unknown original glyph
count/encoding; original table pixels remain authoritative. Presentation tabs and code
spacing are scan-based approximations. Eleven source variants include 실지 못하지만,
READ을, operator/arrow and punctuation candidates. The source explicitly says the full
program listing is not printed and refers source/executable to this month's disk. Those
files and disk remain unrecovered; both printed inline examples are retained. No missing-
page, issue-wide absence, original encoded-file, execution or technical-truth claim.

Three one-file heading classifications match, including a fresh process. Five source
anchors, original heading/logo/editorial panel, two context transcriptions, nine physical
context rows/ranges and three exact crops validate. The eight-line historical editorial
invitation remains private classification context, separate from article 0034's body.
Nine ownership/reference/reparenting/preface edits fail the frozen private guard.

All fourteen complete raw drafts read in one untruncated output before one literal source
pass: two eng/twelve kor+eng, zero retries or within-pass changes. Sixteen initial exact
crops reviewed on five sheets; one pre-OCR table-margin repair directly reviewed and fifteen
initial crops reused exactly. Three enlarged source-only details reviewed without OCR.
A classification-helper type-assertion failure is retained and fixed before any classification
export; canonical integer 438 is unchanged. Inherited execution-map timetable/screen template
wording is explicitly corrected in article metadata; recognition provenance remains exact.

Twenty-two consistently rehashed article-metadata edits pass generic exports and fail the
frozen private audit; no generic custom-schema claim. All 53,718 prior December files,
9,708 former selected files/nineteen roots, thirteen former classifications, 9,332 September
files and thirty core/source/runtime/TOC/queue pins remain exact. Unchanged 213-test baseline
reused. Only 0033/0034 advance; all other child states remain unchanged.

Batch 47 completes independent MODECON article 0035 and monitor-performance tip 0043
on shared PDF 414/individually read folio 439. Three 41-file MODECON exports and three
45-file monitor exports match, including fresh-process builds. The eight/ten source crops,
eight/nine OCR outcomes, six/eight blocks, 25/47 reading rows and 67/105 typed ranges
validate. All eighteen PNG decodes and two ZIP CRCs pass. Eighty cross-body crop pairs
are disjoint, and every eligible region is disjoint from its exclusions. Completed upper-
page Get/READ article 0034 remains separate; 413 and 415 are independent neighboring bodies.

MODECON source title MODE CON을 이용한 쾌적한 도스 화면보기 differs from the canonical
MODE CON으로 쾌적한 도스 화면보기. Both remain explicit; credit 원치호, parent 0031,
null reference and order stay unchanged. One opening group retains three column fragments
and two boundaries. The single unnumbered command row retains MODE CON: LINES=50.
Forward slashes, typographic spaces and the physical SYS wrap in DEVICE = C : /DOS/ANSI.
SYS stay literal. Four file occurrences, four values (50, 40, 50, 42), five variants and
the directory/text-size claims remain source-linked. No valid DOS syntax repair, original
encoded commands/files, execution or technical-truth certification.

Uncertain-kind 0043 resolves to an independent article body from its own contents title,
gray panel, bullet-title, introduction, six numbered items and actual ending. No byline is
observed or supplied; parent 0031/null reference/order stay intact. It is not nested under
MODECON or heading 0033. The complete original panel intentionally overlaps only its own
searchable text. All six two-row numbered headings and six paragraph-gap anchors remain.
Step 4's middle-to-right continuation preserves selected / 하는 것이 좋다. contexts without
merging physical rows. Printed 추위서, fliker, 낀듯, the circular bullet approximation and
fragmentary 얘기./모니터. endings remain literal. Four variants and historical display,
selection and eye-health claims retain their uncertainty; no current advice certification.

The original shared inventory omitted uncertain-kind 0043, so its first export was rejected.
A narrowly scoped private eligibility adapter now accepts only that frozen canonical
identity/source/TOC/geometry/map and the issue queue's source-backed independent-body
decision. Six altered identity/source/map cases are rejected. The generic core and shared
inventory remain unchanged. Successful MODECON output was reused exactly. The failed export
and a dependent audit launched before checking its success remain archived; the latter
failed on the missing monitor output and passes after export completion. No new OCR or
source correction was used for either repair. Thirteen assembly adapters remain required;
the Batch 47 eligibility adapter is additionally needed when rebuilding monitor 0043.

All seventeen complete raw drafts read in one untruncated output before one literal source
pass: one eng/sixteen kor+eng, zero retries or crop changes. All eighteen exact initial
crops reviewed on five sheets; no pre-OCR repairs. Three enlarged source-only details
reviewed without recognition. Thirty consistently rehashed custom-metadata edits pass
generic exports and fail the frozen private audit; no generic custom-schema claim.
All 53,984 prior December files, 9,766 former selected files/twenty roots, fourteen
classifications, 9,332 September files and thirty core/source/runtime/TOC/queue pins remain
exact. Unchanged 213-test baseline reused; only 0035/0043 advance.

Batch 48 completes Clipper/ACHOICE article 0036 on PDF 415–416/individually read
folios 440–441. Source title and credit 신준현, canonical parent 0031, null reference and
order remain unchanged. The final prose ends upper-middle/right 416 with 기사에서 인용한
것이다. Independent printer 0044 title/byline/body/M and the lower Excel gray tip are
excluded; 417 is a full advertisement. No closing M is inferred for Clipper.

Three 76-file exports match, including a fresh-process build. All nineteen exact source
crops, sixteen outcomes, eleven blocks, three original listing panels, 177 reading rows and
861 typed ranges/56 empty-anchor occurrences validate. Two joined prose groups retain five
boundaries. The 415→416 continuation passes around all nine intervening listing regions;
physical source order and wraps remain explicit. Eligible regions are disjoint from every
exclusion. Original panels intentionally overlap only their own searchable labels/code.
All nineteen PNG decodes and one ZIP CRC pass.

The three printed listings retain EASYPUT.PRG, function PUTDATA and function JBOX:
44/45/39 physical code rows, 128 total, eleven blank contexts and no printed line numbers.
All 125 logical row contexts cover these rows exactly. Two aligned comment groups retain
three/two physical rows without merging; eleven comment rows remain explicit. Twelve array
values, three printed calls and six CHR value pairs retain source ranges. The composite
listing download has three separately indexed fragments; it does not certify a combined
executable program or recover original encoded files.

Printed colon-separated assignments, USEARRARY comment spelling, SELLE, sdata2/z case,
SET COLOR TO /W, bare RETURN rows and all CHR(212) values remain unrepaired. Twelve variants
retain byline and 1/I/l/HO/H0 candidates. Six decorative dash-run markers and one prose
omission-dot marker have unknown original glyph counts/encoded bytes. Two whitespace ink
contexts in listing 1 have unknown glyph identity/count/code membership; original pixels
remain authoritative. Indentation, alignment, quotes and typography are scan approximations.
Four prose list references retain two apparent panel-number mismatches without repairing
the printed numbers. The final JBOX prior-article attribution stays literal; the cited article
and unprinted implementation are not identified or recovered. No syntax, logic or technical
repair, original program/data/disk recovery or execution is inferred.

All sixteen complete raw drafts read in one untruncated output before one literal source
pass: three eng/thirteen kor+eng, zero retries or within-pass changes. Nineteen initial
crops reviewed on six sheets; one pre-OCR clipped left prose margin widened and directly
reviewed, eighteen initial crops exact. All three code crops also viewed at original
resolution. Seven enlarged source-only details reviewed without recognition. No export/
helper failures in this checkpoint. Twenty-seven consistently rehashed custom-metadata
edits pass generic exports and fail the frozen private audit; no generic custom-schema claim.
All 54,278 prior December files, 9,852 former selected files/twenty-two roots, fourteen
classifications, 9,332 September files and thirty core/source/runtime/TOC/queue pins remain
exact. Unchanged 213-test baseline reused; only 0036 advances.

Batch 49 completes independent printer-eject article 0044 on PDF 416/individually read
folio 441, credited 박상희. Source title, canonical parent 0031, null reference and order
remain unchanged. The original closing M follows the final commands above the separate
Excel tip. Completed Clipper listing 3/prose are excluded; 415 is Clipper and 417 a full
advertisement. No other body state advances.

Three 42-file exports match, including a fresh-process build. All nine source crops,
eight outcomes, eight blocks, one original closing ornament, 48 reading rows and 177 typed
ranges/six empty-anchor occurrences validate. Every eligible region is disjoint from its
exclusions. All nine PNG decodes and one ZIP CRC pass. Independent paragraphs stay separate;
no prose join is invented between columns.

Two code fragments retain ten printed text rows and two layout-gap anchors, twelve row
contexts total. Nine logical command units cover the printed rows exactly; RCX and its
following 000B remain separate physical rows. Both E 0100 addresses and all eleven printed
two-digit hex tokens stay literal. The source's 11-byte claim is not proof of resulting
file size or executable bytes. No address repair, assembly, execution or output program
creation. The composite listing is not an original script/batch/program file, and original
encoded blank-line count and vertical leading remain unknown.

Five filename occurrences, seven port occurrences, two physical word/filename wraps and
eight variants remain source-linked. DEBUG〈FOF.SCR uses U+3008 as a source-angle candidate,
with ASCII< recorded separately. Printed 쉽/십, 짜증스럽지 않다, 000B/0008 and 1/I/0/O
candidates remain explicit. The original M stays graphic pixels, without an encoded-character
claim. Historical printer/MODE behavior and source glyphs remain unverified.

The first export was rejected because the shared inventory lacks canonical 0044. Direct
inspection now proves that inventory uses an older TOC snapshot: 42 issue entries versus
the issue queue's 45, with different source hashes; 0043–0046 are absent from the legacy
snapshot. This supersedes Batch 47's unproven explanation that uncertain kind caused the
monitor omission. Monitor 0043 gets only a current provenance-disposition pointer; its body,
availability, package and adapter bytes stay exact. The scope amendment records this as
the second canonical task, with no new source page or OCR.

A narrowly scoped guard validates only frozen canonical 0044/source/TOC/geometry/map and
the current issue queue. Six altered identity/source/map cases are rejected. The generic
core and legacy inventory remain unchanged; the failed export remains archived. Thirteen
assembly adapters and the separate monitor/printer eligibility guards are needed for the
relevant builds. Twenty-two consistently rehashed custom-metadata edits pass generic
exports and fail the frozen private audit; no generic custom-schema claim.

All eight complete raw drafts read in one untruncated output before one literal source
pass: two eng/six kor+eng. Nine exact initial crops reviewed on three sheets; three enlarged
source-only details viewed. Zero repairs, retries or within-pass crop changes. All
54,582 prior December files, 9,928 former selected files/twenty-three roots, fourteen
classifications, 9,332 September files and thirty core/source/runtime/TOC/queue pins remain
exact. Unchanged 213-test baseline reused. Current totals: twenty-three readable/sample-
reviewed articles, one partial, six groups, three section references and twelve unresolved
identities. Twenty-four roots contain 9,970 selected files; fourteen classifications are separate.

Batch 50 classifies information-radar heading 0045 as non-owning and preserves compound
child 0046 opening PDF 112–116/individually read folios 102–106 as immutable partial native a.
The original unfoliated divider on 111 is separate classification context: its full artwork,
title and local catalogue are retained. Canonical compound title, parent 0045, null page
references and order remain unchanged; intrinsic news and branch labels are not new
canonical children.

Observed anchors are domestic news 112–123, overseas opening 124/final 133, software
134–137, books 138–139 and prices 140–141, followed by independent quiz 142. Intervening
continuity beyond the first native remains unverified. The December-events sidebar on
123 requires later ownership review. All five divider references conflict with observed
opening folios: printed 128/130/102/114/124 versus observed 102/114/124/128/130. Both sets
remain explicit and unrepaired. The books running label 정보나눔터 is a source variant;
it does not change the canonical hierarchy.

Three 208-file native exports match, including a fresh process. All 56 body source crops,
48 outcomes, 22 blocks, eight original panels/photographs, 695 reading rows and 1,039 typed
ranges/33 empty anchors validate. Three complete main news items and an independent
two-page interview remain distinct. Six interview questions include one spanning columns;
four prose groups retain 26 continuation boundaries and their intervening material. Six
captions, two rotated photo-credit candidates, eleven source variants and 155 literal
numeric occurrences retain source contexts. The native ends a complete workstation item;
117 starts new news, without an inferred incoming prose join.

One group classification record and its original divider PNG, two files total, reproduce
independently and in a fresh process. Two searchable context regions/seven rows retain
the local catalogue and five conflicts. The heading owns no duplicate article body,
article package or text download. All three divider source crops match original pixels.

All fifty complete raw drafts were read in one untruncated output before one literal
source pass: two divider texts and 48 body texts, all kor+eng. All 59 initial crops on
17 sheets and sixteen changed crops on four sheets were directly reviewed before OCR;
43 initial crops remain exact. Five enlarged source-only details were reviewed without
recognition. Zero retries or within-pass map changes. Printed Ristricted, 워스테이션,
높히고, 메임 프레임 and 선워스테이션 remain literal. SPECfp92 uses baseline fp as a
typography approximation; original pixels remain authoritative. Reporter/photo credits,
product claims, prices and predictions are source occurrences, with no technical-truth,
original-file, execution or original encoded-glyph/spacing claim.

Eligibility was checked before the first export against the current issue queue and a
guard scoped to the frozen first-native map. The core and legacy inventory stay exact.
Six altered identity/source/map cases and six actual group-audit cases are rejected.
Twenty consistently rehashed custom-metadata edits pass generic exports and fail the
private frozen source audit; no generic custom-schema enforcement claim. One failed
validation helper used an unchanged page index in its negative case; a fresh helper
uses an actual changed index. Failure and completed evidence are retained, without
new OCR or source correction.

All 54,760 prior December files, 9,970 former selected files/24 roots, fourteen
classification files, 9,332 September files and thirty core/source/runtime/TOC/queue pins
remain exact. The unchanged 213-test baseline is reused. Current totals: twenty-three
readable/sample-reviewed articles, two partials, seven groups, three section references
and ten unresolved identities. Twenty-five selected roots contain 10,178 files; sixteen
classification files are separate, including the new group record and divider image.

Batch 51 preserves compound information-radar entry 0046 continuation PDF 117–122,
individually read folios 107–112, as immutable native b. Canonical compound title,
parent 0045, null reference and other identities remain unchanged. Prior 116 ends a
complete item; 117 starts independent Hitel news, with no incoming prose join.

Eleven intrinsic news items retain ten complete items and the opening of the floptical
item, which continues on 123. Site-license, Geulbak/integrated software, Windows workgroup,
notebook, optical disk, multimedia, NAL and sound/video items retain their separate flows.
The video-interface item ends on 122, correcting an early progress note that suggested
two outgoing items. Only the floptical item continues; its final sentence on 122 precedes
a new paragraph on 123. No physical word merge is inferred at this native boundary.

Three selected 312-file exports match, including a fresh process. All 82 source crops,
74 outcomes, 43 blocks, eight original images, 760 reading rows and 1,227 typed ranges/
26 empty anchors validate. Eleven prose groups retain 31 column/page boundaries and
their intervening material. Eight captions, one rotated photographer credit, eight
historical contact blocks, fifteen variants, 182 literal numeric occurrences and two
file references retain source contexts. Original image lettering is not exhaustively
transcribed. Prior native a's 208 files regenerate exactly through the new guard's
unchanged-map delegation.

All 74 complete raw drafts were read in one untruncated output before one literal source
pass, all kor+eng. All 83 initial crops on 23 sheets and seven changed selected crops on
two sheets were directly reviewed before recognition. Eight pre-OCR revision events
include seven changed crops and one removed fragment that cut through a paragraph;
75 unchanged crops remain exact. Six enlarged/rotated source-only details were viewed.
Zero retries or within-pass map changes. The initial map's nine/eight-complete item-count
note is superseded by the explicit eleven/ten-complete enumeration.

Title 틀미름이/body 틀마름이, old-araea ᄒᆞᆫ글 approximation, source spelling/particles,
Greek-mu typography, identifier/model wraps and MIDI module price 2만9천원 remain literal.
Historical political/legal claims, product details, comparisons, prices, forecasts and
contacts are source occurrences; their truth and current applicability are unverified.
No original encoded glyph/spacing, file recovery, execution, human acceptance or full
proofreading claim.

The first helper stopped because a variant lookup omitted a physical word wrap. A fresh
helper reused the unchanged map/raws/corrected text. Audit then found that the filename
index omitted .ntx because a Korean particle followed it. A metadata-only correction/
recipe/export revision adds its exact source range. Article bytes, all crops/raws/TSVs/
settings/runtime/map/ZIP and 308 of 312 files remain exact; four metadata files differ.
Both failed attempts and the initial export remain retained. No new OCR or source pass.
Twenty-one consistently rehashed metadata edits pass generic exports and fail the private
frozen source audit; six altered eligibility cases are rejected. The core and legacy
inventory stay unchanged. The unchanged 213-test baseline is reused.

All 55,557 prior December files, 10,178 former selected files/25 roots, sixteen
classification files, 9,332 September files and thirty core/source/runtime/TOC/queue pins
remain exact. Current totals stay twenty-three readable/sample-reviewed articles, two
partials, seven groups, three section references and ten unresolved identities. Twenty-six
selected roots contain 10,490 files; sixteen classification files remain separate.
Compound natives a/b preserve eleven pages 112–122 and 520 files; availability stays partial.

Batch 52 preserves compound information-radar entry 0046 continuation PDF 123–128,
individually read folios 113–118, as immutable native c. Domestic news ends on 123;
the explicit overseas-network heading starts on 124. Thirteen main news flows retain
eleven complete items wholly within this native, the incoming floptical tail and the
outgoing printer opening. Canonical compound title, parent 0045, null reference and
all other identities remain unchanged.

The December-events panel on 123 belongs to the domestic-news branch as an ancillary
sidebar. Its embedded placement before the overseas heading supports that decision.
The closing M separates the product-news flow; the notice remains distinct from HDD
prose. Preserve the complete original panel and searchable heading, bullet, body,
dates and historical organizer contacts. No new canonical child or current invitation.

Three 323-file exports match, including a fresh process. All 84 source crops, 77 OCR
outcomes, 44 blocks, seven original images, 775 reading rows and 1,304 typed ranges/
34 empty anchors validate. Thirteen prose groups retain 33 column/page boundaries
and their intervening material. Five captions, three reporter credits, five historical
contact blocks, three embedded vendor-contact contexts, seventeen variants and 239
literal numeric occurrences remain source-linked. Earlier natives a/b regenerate
exactly through the new guard's delegation: 208 and 312 files respectively.

All 84 initial crops on 25 sheets and seven repaired crops on two sheets were directly
reviewed before recognition; 77 unchanged crops remain exact. All 77 complete raw
drafts were read in one untruncated output before one literal source pass, all kor+eng.
Seven pre-OCR edge repairs are retained in a fresh map revision. Zero OCR retries or
within-pass crop changes. The unchanged 213-test baseline is reused.

Literal 1.44KB, the wrapped 19/.2GB claim, model I/1 candidates, spelling differences,
prices, release forecasts and physical identifier wraps remain source occurrences.
Their technical or historical truth, current applicability and original encoded bytes
are unverified. Tiny embedded image lettering and screenshot BASIC code are not
exhaustively transcribed. No original file recovery, execution, human acceptance or
full proofreading claim.

The incoming 122→123 continuation starts a new paragraph after a complete sentence;
no physical word merge is inferred. Outgoing 128 ends 애플 and 129 begins 토크,
continuing one word. Both fragments and source contexts remain explicit; actual
cross-native assembly is still required. Twenty-five consistently rehashed metadata
edits pass generic exports and fail the frozen private source audit; six altered
eligibility cases are rejected. No generic custom-schema enforcement claim.

All 56,952 prior December files, 10,490 former selected files/26 roots, sixteen
classification files, 9,332 September files and thirty core/source/runtime/TOC/queue
pins remain exact. Totals stay twenty-three readable/sample-reviewed articles, two
partials, seven groups, three section references and ten unresolved identities.
Twenty-seven selected roots contain 10,813 files; sixteen classification files remain
separate. Natives a/b/c preserve seventeen pages 112–128 and 843 files; the compound
entry stays partial.

Batch 53 preserves compound information-radar entry 0046 continuation PDF 129–134,
individually read folios 119–124, as immutable native d. Sixteen main text items retain
fourteen complete items wholly within this native, the incoming printer tail and the
outgoing Han-geul Baram opening. Overseas-network continuity on 124–133 is now directly
source-reviewed across current and prior checkpoints; actual assembly remains pending.
Canonical compound title, parent 0045, null reference and other identities are unchanged.

Page 133 closes the overseas branch with an editorial roundup of six products. The full
original tinted panel, two separately cropped screenshots, captions and closing ornament
remain intact. Page 134 opens software reviews. Three screenshots belong to Han-geul
Baram; the fourth anticipates the independent review on 135. Its selected 반질고리
title/caption candidate remains uncertain, with 반짇고리/반지고리 alternatives linked to
enlarged source views. Initial shorthand is retained in the first ownership/review records;
a fresh revision supersedes the candidate wording without changing figure ownership.
No new canonical child or restored page-135 body is inferred.

Three 369-file exports match, including a fresh process. All 100 source crops, 87 OCR
outcomes, 62 blocks, thirteen original images, 714 reading rows and 1,304 typed ranges/
29 empty anchors validate. Twelve prose groups retain 25 column/page boundaries and
their intervening material. Eleven captions, fifteen historical contact blocks across
sixteen regions, one contact split across columns, twenty variants, 269 literal numeric
occurrences and two printed file-format references remain source-linked. Earlier natives
a/b/c regenerate exactly through the new guard: 208, 312 and 323 files respectively.

All 100 initial crops on 28 sheets and seventeen repaired crops on five sheets were
directly reviewed before recognition; 83 unchanged crops remain exact. All 87 complete
raw drafts were read in one untruncated output before one literal source pass, all kor+eng.
Four enlarged source-only details were viewed without further OCR. Seventeen pre-OCR
edge repairs are retained in a fresh map revision. Zero OCR retries or within-pass map
changes. The unchanged 213-test baseline is reused.

Literal Canon price 295 dollars, magenda, mata, fliker, the wrapped 167/000,000-colour
claim, 280∼1400시간, 88bit, 4MB/26KB and Microsoft QEMM386 attribution remain source
occurrences. Physical model/unit/identifier wraps and Latin/Roman I/1 candidates remain
explicit. Technical or historical truth, current applicability, original encoded glyphs/
bytes/spacing and file recovery remain unverified. Embedded menus and image lettering
are not exhaustively transcribed. No execution, human acceptance or full proofreading claim.

Incoming 128 ends 애플 and 129 begins 토크, continuing one word with both native
contexts validated. Outgoing 134 ends 규격을 and 135 begins 지원하여 in the same
Baram prose. Actual cross-native assembly remains required. Twenty-eight consistently
rehashed metadata edits pass generic exports and fail the frozen private source audit;
six altered eligibility cases are rejected. No generic custom-schema enforcement claim.

All 58,045 prior December files, 10,813 former selected files/27 roots, sixteen
classification files, 9,332 September files and thirty core/source/runtime/TOC/queue pins
remain exact. Totals stay twenty-three readable/sample-reviewed articles, two partials,
seven groups, three section references and ten unresolved identities. Twenty-eight selected
roots contain 11,182 files; sixteen classification files remain separate. Natives a/b/c/d
preserve twenty-three pages 112–134 and 1,212 files; the compound entry stays partial.

Batch 54 preserves compound information-radar entry 0046 continuation PDF 135–140,
individually read folios 125–130, as immutable native e. The sixteen main items include
fourteen complete current bodies, the incoming Han-geul Baram ending and the outgoing
price branch. Five public-software reviews, seven descriptive book notices and a separate
six-entry book-shelf table retain their own titles, prose, images and records. These are
intrinsic items within the unchanged canonical compound, not new canonical children.

Three 469-file exports match, including a fresh process. All 131 exact source crops,
110 OCR outcomes, 62 blocks, 21 original figures, 588 reading rows and 1,201 typed ranges/
seventeen empty anchors validate. Two ranges explicitly use immutable native-d download
and scan contexts. Fifteen prose groups preserve 31 column/page boundaries. Six captions,
two historical contacts, seven book covers/bibliographies, eighteen shelf cells/three
headers, fourteen price quotes, five printed file/upload records, twelve ring-review
modules, 24 variants and 132 literal numeric occurrences remain source-linked.

All 131 initial crops on 36 sheets, 32 changed crops on eight sheets and fifteen further
pre-OCR refinements on four sheets were directly reviewed before recognition. The 47
revision events affect 32 distinct crops; 99 initial crops remain exact. All 110 complete
kor+eng raw drafts were read in one untruncated output before one literal source pass.
Seven enlarged source-only details were reviewed without OCR. Zero OCR retries or
within-pass map changes. The initial audit helper expected an incorrect numeric count;
its failed log is retained and the helper now checks the actual 132 occurrences. Package
bytes are unchanged. The unchanged 213-test baseline is reused.

Baram's 134→135 prose continuation and the ring review's anticipatory page-134 screenshot
retain explicit prior-native contexts. The latter is not duplicated in native e.
Blue Pencil's 136→137 word split remains 윈도/우. Software ends on 137; the books branch
on 138–139 is independent. Page 140 ends with a complete sentence; page 141 continues
the price branch with charts, without a physical prose join. Actual assembly is pending.

The selected 반질고리 title/body/caption candidate remains uncertain, with 반짇고리/
반지고리 alternatives. Old Hangul ᄒᆞᆫ글 is a Unicode approximation with explicit
alternatives; the book-author candidate 김현수 retains 김헌수 as an alternative.
Literal 열러, the repeated 결과를, 부문, publisher spelling 영중 and the six-month/July
wording remain unrepaired. Table pipes approximate printed rules. Original panels,
the shelf table and the public-software bubble intentionally overlap searchable text.
Embedded image lettering is not exhaustively transcribed. Prices, health/fortune and
technical claims, original encoded glyphs/bytes/spacing, program recovery, execution,
human acceptance and full proofreading remain unverified.

The enlarged page-140 source clearly reads 210MB at 42만원 ±1만원, matching the
page-141 chart's 42. The initial “24” reading and conflict note were preliminary visual
errors; they remain retained and are explicitly superseded before OCR. No source price
conflict is established. The five filename/size/upload records are historical metadata;
their program archives have not been recovered.

Thirty-two consistently rehashed custom-metadata edits pass generic exports and fail the
frozen private audit; six altered eligibility cases are rejected. No generic custom-schema
enforcement claim. The new guard delegates unchanged natives a/b/c/d, whose 208, 312,
323 and 369 files regenerate exactly. All 59,309 prior December files, 11,182 former
selected files/28 roots, sixteen classification files, 9,332 September files and thirty
core/source/runtime/TOC/queue pins remain exact.

Totals stay twenty-three readable/sample-reviewed articles, two partials, seven groups,
three section references and ten unresolved identities. Twenty-nine selected roots now
contain 11,651 files; sixteen classification files remain separate. Five compound natives
preserve twenty-nine pages 112–140 and 1,681 files. The compound remains partial.

Batch 55 restores final compound information-radar page PDF 141, individually read
folio 131, as immutable native f. Three original charts retain all headings, units, axes,
dates, series labels and parenthesized point labels. Page 140's prose ends completely;
141 continues the price branch without a physical prose join. The independent reader
quiz on 142/printed 132 establishes the compound ending at 141. Canonical title,
parent 0045, null reference and other identities remain unchanged.

Three 279-file exports match, including a fresh process. All seventy exact source crops,
67 OCR outcomes/blocks, three original figures, 96 reading rows and 630 typed ranges
validate. Fifteen ranges explicitly use immutable native-e download/scan contexts.
Thirteen series retain 32 vertical-axis ticks, nine date labels, 36 physical point labels
and 37 printed observations. Two February observations are explicitly absent. The single
mouse-chart July “4.5” label supports both sensor-mouse and trackball observations;
both refer to the same physical source occurrence, without duplicating the label.

The 120MB and 60MB disk series start in July without February points. Missing data is
neither zero-filled nor interpolated. Thirteen November endpoint values agree with
page 140's central quotes after explicit unit conversion; literal quotes and qualifiers
remain intact. Page 140's 240MB quote has no corresponding series in the chart, and
none is invented. Source prices and drawn line/point positions remain unmodified.

All seventy initial crops on eighteen sheets and thirteen changed crops on four sheets
were directly reviewed before recognition; 57 initial crops remain exact. All 67 complete
kor+eng drafts were read in one untruncated output before one literal source pass.
Four enlarged source-only details were reviewed without OCR. Thirteen pre-OCR repairs,
zero OCR retries and zero within-pass map changes. Literal decimals 7.5, 5.5, 9.5, 4.5
and 1.2 remain explicit. A tiny ink stroke above the modem chart's July “18” remains in
the original crop without certification as encoded punctuation or numeric data.

Axis tick strokes are graphical marks, not minus signs. Unicode bullets, parentheses
and spacing approximate print; no year is printed on the chart date labels. Source price
accuracy, plot geometry accuracy, historical/current market truth, original encoded
glyphs/bytes, program recovery, execution, human acceptance and full proofreading remain
unverified. The unchanged 213-test baseline is reused.

Thirty-two consistently rehashed custom-metadata edits pass generic exports and fail
the frozen private audit; six altered eligibility cases are rejected. No generic custom-
schema enforcement claim. The new guard delegates unchanged natives a/b/c/d/e, whose
208, 312, 323, 369 and 469 files regenerate exactly. All 61,023 prior December files,
11,651 former selected files/29 roots, sixteen classification files, 9,332 September
files and thirty core/source/runtime/TOC/queue pins remain exact.

All thirty compound body pages 112–141 are now preserved across six immutable natives,
totalling 1,960 files. Actual assembly remains required, so availability stays partial.
Issue totals remain twenty-three readable/sample-reviewed articles, two partials, seven
groups, three section references and ten unresolved identities. Thirty selected roots
contain 11,930 files; sixteen classification files remain separate.

Next: actually assemble compound 0046 on 112–141 from the six independently regenerated
native recipes. Resolve only source-backed cross-native prose joins and figure contexts;
carry every original asset, literal claim, physical wrap, glyph candidate and custom index.
Native e has two D-relative ranges; native f has fifteen E-relative ranges. Preserve these
named contexts when projecting all root/native ranges. Ring's page-134 anticipatory
figure belongs to its page-135 review; Baram continues across 134→135. Prices 140→141
require no prose join. Verify coherent reading order and a fresh standalone compound
rebuild before advancing availability. No new mapping or OCR is needed. Twenty prior
adapters plus the native-f guard apply to relevant builds. Keep at most two canonical
tasks/six mapped/twenty outside pages. Other bodies/assemblies, year-feature/UNIX locations,
all 446-page accounting, cover, standalone issue export/rebuild and closeout remain
required. Full December goal active. No reader rebuild.
See [December progress](docs/progress/9212.md) and
[ledger](metadata/catalog/pdf-restoration/1992-12-progress.json).

Batch 56 completes the actual compound information-radar assembly on PDF 112–141,
individually verified printed 102–131. Three 1,968-file assemblies match byte for byte,
including a fresh process, from six independently regenerated immutable natives with
1,960 unchanged files. No new mapping, recognition or source correction. Seventeen
outside whole pages and six exact boundary crops were directly reviewed.

All 523 source-exact crops, 463 selected OCR outcomes, 297 assembled blocks from 300
source blocks, sixty original figures and 3,628 physical reading rows validate. All
6,705 projected metadata ranges, seventeen foreign-context ranges, 13,555 current
typed occurrences, 278 repeated empty-anchor occurrences and 13,258 current/native
projection pairs validate. Original metadata stays in its native context; projected
prior-native D/E ranges use the actual source downloads and scans.

Three source-backed prose joins preserve the new paragraph at 122→123, physical
애플/토크 rows at 128→129 and Baram at 134→135, including intervening captions and
figures. The 116→117 items remain independent; prices 140→141 need no prose join.
Five complete branches and 56 complete main intrinsic items retain source fragments.
The independent interview and ancillary events notice remain separate. No canonical
children are invented. Ring's page-134 anticipatory illustration belongs to its
page-135 review; 반질고리 remains a candidate with 반짇고리/반지고리 alternatives.

Seven book notices, six shelf rows/eighteen cells/three headers, five software-file
records, twelve ring modules, fourteen price quotes and all original art, captions,
credits, historical contacts, literal claims and glyph candidates remain preserved.
Three charts retain thirteen series, 36 physical point labels and 37 observations.
Two February observations stay missing; one July 4.5 mouse label supports two
observations. No interpolation, zero filling or invented 240MB series.

The first assembly differed only in JSON key order from an unordered metadata
dictionary. Both complete first exports remain retained; deterministic adapter r02
changes metadata ordering only. An interrupted slow audit and a corrected helper
field-name failure are preserved, without changes to source or native delivery bytes.
Twenty-six consistently rehashed root/recipe/native edits and six altered eligibility
maps are rejected by frozen private guards; no generic custom-schema claim. All six
unchanged native maps delegate to their existing guards.

All 61,949 prior December files, 11,930 former selected files/thirty roots, sixteen
classification files, 9,332 September files and thirty core/source/runtime/TOC/queue
pins remain exact. The unchanged 213-test baseline is reused. Source encoded bytes,
original program/file recovery, execution, technical/historical truth, human acceptance
and full proofreading remain unverified.

Only compound 0046 advances to readable/sample-reviewed. Totals are twenty-four
readable, one partial, seven group headings, three section references and ten unresolved
identities among 45. Twenty-five selected roots contain 11,938 files; sixteen
classification files remain separate. All six immutable natives remain retained.

Next: verify and restore reader quiz 0039 and next-issue contents notice 0040. Quiz
opening 142/printed 132 is observed; confirm its full extent and all panels. PDF 144
is only a candidate for the contents notice, not a verified global offset. Review
actual folios, endings, adjacent titles and ownership before mapping. Keep at most
two canonical tasks, six mapped pages and twenty outside lookup pages. Year-feature
continuation/child references, UNIX locations, remaining reader-section bodies,
all 446-page accounting, cover, standalone issue export/rebuild and closeout remain
required. Full December goal active. No reader rebuild.

Batch 57 completes reader quiz 0039 on PDF 142–143/individually read 132–133 and
January contents notice 0040 on PDF 144–145/134–135. Original contents 4/5, prior
radar ending 141, all four body pages and following independent C-book advertisement
146 were directly reviewed. Canonical identities, titles, order, parents and references
132/134 remain unchanged. Neither body has an observed byline.

Three 214-file quiz exports and three 171-file notice exports match byte for byte,
including a fresh process. All 108 source-exact crops, 87 selected OCR outcomes,
86 blocks, 21 original figures, 290 physical reading rows and 1,036 typed ranges
validate, including one blank paragraph anchor. All images decode; both ZIP CRCs pass.

The quiz retains its invitation, cartoon/title, sixteen prize captions and original
art, current question, previous JPEG answer, four entry sections, sixteen winner
groups and closing submission notice. All 87 advertised prize counts and 87 physical
historical name/locality rows are separately indexed. Two outlined graphic blanks
remain two Unicode squares; no current answer is supplied. JPEG belongs only to the
previous month. The monthly deadline is printed as 20. Names, addresses and contacts
remain historical source candidates, with no identity/current-location verification.

Caption/winner-heading variants, old-araea ᄒᆞᆫ글 with 훈글/흔글/한글 alternatives,
printed 컴퓨러/셈틀책꽂이 and faint name candidates remain source-linked. Literal
소울 is retained without geographic repair. Tiny lettering in prize artwork remains
in original images without encoded transcription certification. No prizes or software
are recovered, contacts verified or submissions sent.

The notice retains twelve editorial previews and two independent promotional notices.
Source title 1월호 주요 목차 and canonical ending 안내 remain separate. The IPC
paragraph crosses 144→145 with literal physical 본/것을 rows and an intervening
independent library-bank panel. Printed Inter Process Communicaion remains without
English spelling repair. Boxed series 1/5, 150, 512×512, 256, 1MB, version strings,
library-bank notice and 마소지기 2.0 special-gift panel remain source-linked. No new
canonical children, actual January publication, award history or software recovery inferred.

All 108 initial crops on 29 sheets were reviewed before recognition. Eighteen pre-OCR
edge-change events affect fourteen distinct crops; all changed crops on five sheets
were reviewed, and 95 selected crops still equal initial crops. All 87 complete raw
drafts were read in one untruncated output before one literal source pass. Seven empty
colored-heading drafts were corrected from scans without retry. Eight enlarged
source-only details were viewed without OCR. Zero retries or within-pass map changes.

Twenty-six consistently rehashed custom-metadata edits pass generic export integrity
and fail frozen private source/index audits; no generic custom-schema claim. All
67,948 prior December files, 11,938 former selected files/25 roots, sixteen classification
files, 9,332 September files and thirty core/source/runtime/TOC/queue pins remain exact.
The unchanged 213-test baseline is reused. Source glyphs/spacing/encoded bytes,
technical/historical truth, original files, execution, human acceptance and full
proofreading remain unverified.

Only 0039/0040 advance. Totals are twenty-six readable/sample-reviewed articles, one
partial, seven group headings, three section references and eight unresolved identities
among 45. Twenty-seven selected roots contain 12,323 files; sixteen classification
files remain separate. The full December goal remains active.

Next: locate and verify reader Q&A 0037 using source folios, adjacent titles, opening,
extent and ending before mapping at most six confirmed body pages. PDF 419 is a
candidate from the canonical reference 444, not a verified location or global offset.
Segment any longer body and assemble separately. Reader voices and other unresolved
identities do not advance from proximity alone. Year-feature continuation/child references,
UNIX locations, remaining reader bodies, all 446-page accounting, cover, standalone
issue export/rebuild and closeout remain required. No reader rebuild.

Batch 58 completes canonical Q&A 0037, 물어보세요, on PDF 419–424 with individually
read printed folios 444–449. Twelve whole pages establish the body, prior advertisements,
contents identity and independent reader-voices opening on 425/450. Canonical identity,
null parent and reference 444 stay unchanged; reader credits are contributors, not an
invented article byline. No assembly remains for this six-page body.

Three 387-file JSON/assets exports match byte for byte, including a fresh process.
All 99 source-exact crops, 93 selected OCR outcomes, 77 blocks, six original figures,
613 physical reading rows and 1,107 typed ranges validate. Two intrinsic sections retain
fourteen question/answer exchanges and their fourteen credits. Twenty-eight graphic Q/A
markers stay outside prose rows. Three ancillary editorial notices remain distinct.
Thirteen prose joins preserve sixteen boundaries, four across pages, with physical
wraps, intervening FDD panel and coherent per-exchange order explicitly indexed.

Four MNP command entries retain their literal candidates, each relevant token with one
ASCII backslash. The configuration fragment has exactly two rows, [386 Enh] and
EMMEXCLUDE=A000-CFFF. Two slanted separator occurrences retain independent glyph
candidates and alternatives. Seventeen source variants and 86 numeric occurrences remain
source-linked. Printed Interace, SYSTEM. INI, spelling variants and technical claims
are preserved without repair, original encoded-byte certification or execution.

Fourteen pre-OCR edge-change events affect eleven distinct crops; 88 selected crops
still equal initial crops. All 99 initial crops and every changed full crop were viewed
before recognition. Clipped contact-sheet display tiles remain retained and were
superseded by individual full-crop review. All 93 complete raw drafts were read before
one literal source pass. Eight source-only enlargements were viewed without OCR.
Zero retries or within-pass map changes. Prospective stage wall times include tool
latency and orchestration; they do not measure isolated manual throughput.

Twenty-six consistently rehashed custom-metadata edits pass generic integrity and fail
frozen private source/index audits; no generic custom-schema claim. All 69,294 prior
December files, 12,323 former selected files across 27 roots, sixteen classifications,
9,332 September files and thirty core/source/runtime/TOC/queue pins remain exact.
The unchanged 213-test baseline is reused. Original files, encoded glyphs/spacing,
technical/historical truth, execution, human acceptance and full proofreading remain
unverified.

Only 0037 advances. Totals: twenty-seven readable/sample-reviewed articles, one partial,
seven group headings, three section references and seven unresolved identities among 45.
Twenty-eight selected roots contain 12,710 files; sixteen classifications remain separate.
The full December objective remains active.

Next checkpoint 59 verifies reader voices 0038 from its observed PDF 425/printed 450
opening. Confirm actual ending, letter continuations, signatures, adjacent titles and
advertisement boundaries before mapping at most six pages. Candidate 425–430 is not a
verified extent; segment any longer body and assemble separately. Keep at most two
canonical tasks and twenty outside lookup pages. Year-feature continuation/child
references, UNIX locations, remaining reader bodies, all 446-page accounting, cover,
standalone issue export/rebuild and closeout remain required. No reader rebuild.

Batch 59 completes canonical reader voices 0038, 독자의소리, on PDF 425–426,
individually read printed 450–451. Twelve whole views establish the independent Q&A
ending on 424, both body pages and following advertisements 427–432. Publisher price
notice 433 is independent and does not classify the canonical bulletin. Source title
독자의 소리 and canonical spelling remain separate; null parent/reference 450 unchanged.
Four intrinsic signed letters create no canonical children or article byline.

Three 93-file JSON/assets exports match byte for byte, including a fresh process.
All 22 source-exact crops, 21 OCR outcomes, fourteen blocks, one original photograph
and 482 typed ranges validate. Four letters retain headings, complete bodies and
four historical name/locality credits. The 322 nonempty physical rows remain distinct
from twenty reading-notation paragraph separators/empty anchors. Four prose groups
retain seven continuation boundaries, one across pages, without merging physical rows.
Closing M remains separate graphic notation; the photograph has no invented caption.

Eight source variants, 25 numeric occurrences, ten historical claim occurrences and
four company-name candidates retain their original contexts. Printed 드라이버, 네트웍,
범이산업, 한솔, 구자록, versions 3.3/5.0/6.0, memory values 640/736, October 15 and
current 23/next 24 exhibition references remain literal. Enlarged 김지원 supersedes
the prospective whole-page 김지현 note; identities remain unverified. Quotation glyphs
are Unicode candidates. Compatibility, royalties, capacity and future-release claims
remain historical reader opinions, without technical or historical certification.

Eight pre-OCR edge changes affect seven distinct crops; fifteen selected crops still
equal initial crops. All 22 initial crops on eleven sheets and every changed full crop
were reviewed before recognition. All 21 complete raw drafts were read in one untruncated
output before one literal source pass. Four source-only enlargements were viewed
without OCR. Zero retries or within-pass changes. A pending layout view was completed
after polling the original render process. The first audit helper wrongly expected
a code listing; revised audit verifies its absence. Earlier helper/evidence retained,
with source/export bytes unchanged. Prospective wall times include tool/orchestration
latency and do not measure isolated manual throughput.

Twenty-four consistently rehashed custom-metadata edits pass generic integrity and
fail frozen private source/index audits; no generic custom-schema claim. All 70,692
prior December files, 12,710 former selected files across 28 roots, sixteen classifications,
9,332 September files and thirty core/source/runtime/TOC/queue pins remain exact.
The unchanged 213-test baseline is reused. Original glyphs/spacing/encoded bytes,
software/files, execution, technical/historical truth, identities, human acceptance
and full proofreading remain unverified.

Only 0038 advances. Totals: twenty-eight readable/sample-reviewed articles, one partial,
seven group headings, three section references and six unresolved identities among 45.
Twenty-nine selected roots contain 12,803 files; sixteen classifications remain separate.
The full December objective remains active.

Next checkpoint 60 locates and verifies bulletin 0041 and Ctrl-Break 0042. References
462/463 and candidate PDF 437/438 do not establish locations or a global folio offset.
Confirm actual titles, folios, extent, endings and ownership before mapping at most six
pages/two canonical tasks. Outside lookup limit remains twenty pages. Year-feature
continuation/child references, UNIX locations, remaining reader bodies, all 446-page
accounting, cover, standalone issue export/rebuild and closeout remain required.
No reader rebuild.

Batch 60 completes bulletin 0041, 게시판, on PDF 437/individually read printed 462,
and Ctrl-Break 0042 on PDF 438/463. Ten whole views establish both independent bodies,
prior subscription advertising 436, following afterword/advertisement index 439/464
and landscape reader-card sides 440/441. Canonical identities, null parents and references
remain unchanged. Intrinsic notices/satire create no canonical children or page bylines.

Three exports per package match byte for byte, including a fresh process: 136 bulletin
files and 62 Ctrl-Break files. All 52 source-exact crops, 43 selected OCR outcomes/blocks,
nine original figures, 111 physical rows and 437 typed ranges validate. The bulletin
retains five disk groups/nine entries advertising seven diskettes, eight literal program
tokens and seven separator candidates. No disks, original programs or file bytes recovered.
Its fee table has nine positions/eight nonempty cells/one visually blank image anchor,
with original table, purchase text, disk icon, historical phone and street map intact.
Thirteen embedded map-label candidates remain qualified; exit-number glyph unresolved.
The JPEG erratum retains six LENA.OUT/LENA_F.CON occurrences and both correction
directions, including printed CON. Prior November images are not verified or modified.

Ctrl-Break retains four satire items and a separate seven-row contribution invitation.
The communications cartoon keeps ten club candidates and its handwritten caption.
The poem has 27 physical rows, separate source attribution and 이경일/ikilee credit;
this is not a page byline or verified identity. Printed 컴바이러스 and 혓바닥 stay literal.
The humorous program preserves seventeen rows, five prose rules and three physical
wraps in article/listing contexts. Uppercase DO, Korean include/prose, approximate
indentation and missing C punctuation remain without repair or execution. Its listing
ends at the closing brace without an added newline. Original doctor/computer joke,
arrow, poem art and angled invitation remain intact, including final Ctrl-break case.

All 52 initial crops on eighteen sheets and one changed full title crop were reviewed
before recognition; 51 selected crops remain initial-exact. A terminal Poppler interruption
occurred before any Ctrl-Break recognition. All 31 completed bulletin outcomes were
reused unchanged; twelve Ctrl-Break outcomes were recognized once in a fresh destination.
All 43 complete raw drafts were read in one untruncated output before one source pass.
Eight source-only enlarged/rotated details were viewed without OCR. One empty fee-cell
draft and the invitation's running-footer-only draft were corrected directly from scans.
Zero recognition retries or within-pass crop changes. An audit-helper assumption about
an extra listing newline was corrected; source/export bytes stayed unchanged. Earlier
helper, interrupted render and logs remain retained. Prospective stage walls include
interruption/orchestration latency; successful engine time is separate, not manual throughput.

Thirty-two consistently rehashed custom-metadata edits pass generic integrity and fail
frozen private source/index audits; no generic custom-schema claim. All 71,118 prior
December files, 12,803 former selected files across 29 roots, sixteen classifications,
9,332 September files and thirty core/source/runtime/TOC/queue pins remain exact.
The unchanged 213-test baseline is reused. Original glyphs/spacing/encoded bytes,
technical/historical truth, names/contacts, source disks/files, execution, human acceptance
and full proofreading remain unverified.

Only 0041/0042 advance. Totals: thirty readable/sample-reviewed articles, one partial,
seven group headings, three section references and four unresolved identities among 45.
Thirty-one selected roots contain 13,001 files; sixteen classifications remain separate.
All reader-section canonical bodies are now readable. The full December objective remains active.

Next checkpoint 61 begins systematic 446-page accounting with direct review of physical
pages 1–20 and bounded location research for year-feature 0019 and UNIX terminal-control
0022. Preserve source kinds and actual folios in a pinned index; reconcile prior reviewed
body/search evidence without treating render existence as visual review. No full-source
absence claim before complete accounting. Children 0020/0021 and UNIX 0023 do not advance
in this two-task checkpoint. Known shell-listing fragments 300–305 alone do not establish
opening/ownership/extent. Keep at most twenty outside pages and six mapped pages.
Remaining bodies/assemblies or explicit source gaps, all 446-page accounting, cover,
standalone issue export/rebuild and closeout remain required. No reader rebuild.

Batch 61 begins systematic source-page accounting and bounded location research for
year-feature 0019 and UNIX terminal-control 0022. Twenty whole pages, physical 1–20,
were directly reviewed: one cover, two contents pages and seventeen advertisements.
Cover promotion and contents references do not establish target body locations.
No mapped pages, recognition calls, retries or source correction passes occurred.
All 45 canonical entries remain unchanged: thirty readable/sample-reviewed, one
partial, seven group headings, three section references and four unresolved.

The provisional four-file accounting sidecar is
`archive/pdf/1992-12/restoration/batch-61/accounting-r01/`. All 446 physical slots are
represented: 345 have a primary classification and 101 remain explicitly pending.
Three exports match byte for byte, including a fresh process. Sixty retained review
records pair 328 prior whole-page reviews with pinned source renders; twenty-two
explicit review/render/archive bridges preserve the evidence where original review
records did not themselves contain image pins. Eighty-seven prior nonbody decisions
retain their original source-evidence pointers. The current twenty views include
three rechecks and add seventeen newly classified pages. Source audit decodes all
forty current native/layout images and validates every prior evidence pointer.

The ledger retains 238 selected body pages across 31 maps, with 31 map-local excluded
region records across fourteen mixed body pages. These are contextual records, not
31 unique advertisements. The unassigned shell-listing fragment on 300–305 retains
its uncertain ownership. Pending pages are 21–79, 81–89, 91–93, 95–97, 105–106,
340–359 and 442–446. No folio offset, missing-page count, full accounting, source-wide
absence, new canonical ownership or verified cover-asset replacement is inferred.

Twenty consistently rehashed private accounting mutations are rejected by the private
audit; this does not assert generic article-schema enforcement. All 71,822 prior
December files, 13,001 selected article files/31 roots, sixteen classifications,
9,332 September reference files and thirty core/source/runtime/TOC/queue pins remain
exact. The unchanged 213-test baseline is reused. Four accounting sidecar files do
not increase the selected article-file count. Stage wall times include preservation,
rendering, reconciliation and orchestration; they are not manual-review throughput.

Next checkpoint 62 reviews physical pages 21–40 for the same two location tasks,
within the 2 canonical task/6 mapped page/20 outside page limits. Year-feature 0019
remains partial at opener 299; its ending and child references 0020/0021 remain
unresolved. UNIX 0022/0023 remain unresolved; this checkpoint does not advance 0023.
Remaining bodies/assemblies or explicit source gaps, all 446-page accounting, cover
verification, standalone JSON/assets issue export/rebuild and closeout are required.
Full December objective remains active. No reader rebuild.

Evidence: `archive/pdf/1992-12/restoration/batch-61/validation.json`,
`source-audit.json`, `negative-checks.json`, `reproduction.json`,
`fresh-process-reproduction.json`, `prior-review-index-r02.json`,
`prior-classification-decisions.json`, `source-boundaries.json` and
`prospective-timings.json`; the canonical ledger records checkpoint 62.

Batch 62 directly reviews physical pages 21–40 for year-feature continuation 0019
and UNIX terminal-control 0022. All twenty pages are full advertisements: graphics
cards, printers, computers, processors, floppy disks, video/audio cards and software.
UNIX, GUI, DOS SHELL and image-grabber product mentions remain advertising context;
neither target body is observed. No magazine folio is visible on these pages;
specifications, prices, certification numbers and screenshot dates are not folios.
No mapping, recognition, retry or source correction pass occurs.

The fresh four-file sidecar at
`archive/pdf/1992-12/restoration/batch-62/accounting-r01/` represents all 446 slots:
365 classified and 81 explicitly pending. Three exports match byte for byte,
including a fresh process. The twenty additions replace only prior pending rows;
all other 426 page rows remain unchanged. The prior source-accounting audit is
reexecuted against original pinned review, render and ownership inputs, retaining
its twenty-two explicit review/render bridges. All forty current native/layout
images decode. Coverage still includes 238 selected body pages/31 maps and 31
map-local exclusion records across fourteen mixed body pages. The unassigned
shell-listing fragment on 300–305 remains unassigned. Pending pages are 41–79,
81–89, 91–93, 95–97, 105–106, 340–359 and 442–446.

Twenty consistently rehashed private accounting mutations are rejected by the
private source audit; no generic article-schema claim. All 71,910 prior December
files, 13,001 selected article files/31 roots, sixteen classifications, 9,332 September
files and thirty core/source/runtime/TOC/queue pins remain exact. The unchanged
213-test baseline is reused. An inherited narrative count in the first completion
report is corrected in `completion-audit-r02.json`; the original report is retained.
Source ledger, validation and canonical entries were correct and remain unchanged.
Prospective stage wall times include preservation, rendering and orchestration;
they do not measure isolated manual review or restoration throughput.

All 45 canonical entries remain unchanged: thirty readable/sample-reviewed, one
partial, seven groups, three section references and four unresolved. Next checkpoint
63 reviews physical pages 41–60 for the same two location tasks, within 2/6/20 limits.
Year-feature 0019 remains partial at opener 299; its ending and child references
0020/0021 remain unresolved. UNIX 0022/0023 remain unresolved. No full-source absence,
missing-page count, new ownership, full accounting or cover-asset verification is
claimed. Remaining bodies/assemblies or explicit source gaps, all 446-page accounting,
cover verification, standalone JSON/assets issue export/rebuild and closeout remain
required. Full December objective active. No reader rebuild.

Evidence: `archive/pdf/1992-12/restoration/batch-62/validation.json`,
`source-reviewed.json`, `source-audit.json`, `negative-checks.json`,
`reproduction.json`, `fresh-process-reproduction.json`, `source-boundaries.json`,
`prospective-timings.json` and `completion-audit-r02.json`. Session evidence:
`archive/pdf/1992-12/evidence/session-2026-11-01-43/`.

Batch 63 directly reviews physical pages 41–60 for year-feature continuation 0019
and UNIX terminal-control 0022. All twenty pages are full advertisements, including
a computer seller's ski-school promotion. Product mentions of UNIX, GUI, Look & Feel,
VAX and terminal-server functions do not identify canonical article bodies. The
large 289 on a computer/printer advertisement is a price; ski-event dates and product
specifications are not magazine folios. No visible magazine folio is observed on
these pages. Neither target body is found within this bounded review; no mapping,
recognition, retry or source correction pass occurs.

The four-file sidecar at
`archive/pdf/1992-12/restoration/batch-63/accounting-r01/` represents all 446 slots:
385 classified and 61 explicitly pending. Three exports match byte for byte,
including a fresh process. Only twenty prior pending rows change; the other 426
page rows remain unchanged. Prior accounting audits are reexecuted through original
pinned review, render and ownership inputs, retaining the twenty-two explicit
review/render bridges. All forty current native/layout images decode. The ledger
retains 238 selected body pages/31 maps and 31 map-local exclusion records across
fourteen mixed body pages. The shell-listing fragment on 300–305 remains unassigned.
Pending pages are 61–79, 81–89, 91–93, 95–97, 105–106, 340–359 and 442–446.

Twenty consistently rehashed private accounting mutations are rejected by the
private source audit; no generic article-schema claim. All 71,994 prior December
files, 13,001 selected article files/31 roots, sixteen classifications, 9,332 September
files and thirty core/source/runtime/TOC/queue pins remain exact. The unchanged
213-test baseline is reused. Prospective stage wall times include preservation,
rendering, recursive evidence checks and orchestration; they do not measure isolated
manual review or restoration throughput.

All 45 canonical entries remain unchanged: thirty readable/sample-reviewed, one
partial, seven groups, three section references and four unresolved. Next checkpoint
64 reviews the next twenty pending pages, physical 61–79 and 81, within 2/6/20 limits;
already classified page 80 is skipped. Year-feature 0019 remains partial at opener
299, with ending and children 0020/0021 unresolved; UNIX 0022/0023 remain unresolved.
No source-wide absence, missing-page count, new ownership, complete accounting or
cover-asset verification is claimed. Remaining bodies/assemblies or explicit source
gaps, all 446-page accounting, cover verification, standalone JSON/assets issue
export/rebuild and closeout remain required. Full December objective active.
No reader rebuild.

Evidence: `archive/pdf/1992-12/restoration/batch-63/validation.json`,
`source-reviewed.json`, `source-audit.json`, `negative-checks.json`,
`reproduction.json`, `fresh-process-reproduction.json`, `source-boundaries.json`,
`prospective-timings.json` and `completion-audit.json`. Session evidence:
`archive/pdf/1992-12/evidence/session-2026-11-01-44/`.

Batch 64 directly reviews the next twenty pending physical pages, 61–79 and 81,
for year-feature continuation 0019 and UNIX terminal-control 0022. All are full
advertisements, including landscape Multiuser DOS and plotter promotions and the
four-page SOFTBANK software-price/dealer catalogue. UNIX compatibility, networking,
compiler merchandise and JPEG-compression descriptions remain advertising context.
Neither target body is observed. No visible magazine folio is found; performance
counters, prices, specifications and dealer addresses are not folios. Original
landscape compositions are retained. No mapping, recognition, retry or source
correction pass occurs; already classified page 80 is not newly reviewed.

The fresh four-file sidecar at
`archive/pdf/1992-12/restoration/batch-64/accounting-r01/` represents all 446 slots:
405 classified and 41 explicitly pending. Three exports match byte for byte,
including a fresh process. The twenty additions change only prior pending rows;
all other 426 page rows remain unchanged. Prior source-accounting audits are
reexecuted through original pinned review, render and ownership inputs, retaining
the twenty-two explicit review/render bridges. All forty current native/layout
images decode. The ledger still has 238 selected body pages/31 maps and 31 map-local
exclusion records across fourteen mixed body pages; the shell-listing fragment on
300–305 remains unassigned. Pending pages are 82–89, 91–93, 95–97, 105–106,
340–359 and 442–446.

Twenty consistently rehashed private accounting mutations are rejected by the
private source audit; no generic article-schema claim. All 72,076 prior December
files, 13,001 selected article files/31 roots, sixteen classifications, 9,332 September
files and thirty core/source/runtime/TOC/queue pins remain exact. The unchanged
213-test baseline is reused. Four accounting files do not increase the selected
article-file count. Stage wall times include preservation, rendering, recursive
evidence checks and orchestration, not isolated manual-review throughput.

All 45 canonical entries remain unchanged: thirty readable/sample-reviewed, one
partial, seven groups, three section references and four unresolved. Next checkpoint
65 reviews pending pages 82–89, 91–93, 95–97, 105–106 and 340–343 for the same two
location tasks, within 2/6/20 limits. Map eligible body only after confirming its
identity. Year-feature 0019 remains partial at opener 299, with ending/children
0020/0021 unresolved; UNIX 0022/0023 remain unresolved. No source-wide absence,
missing-page count, new ownership, complete accounting or cover verification is
claimed. Remaining bodies/assemblies or explicit source gaps, all 446-page accounting,
cover verification, standalone JSON/assets issue export/rebuild and closeout remain
required. Full December objective active. No reader rebuild.

Evidence: `archive/pdf/1992-12/restoration/batch-64/validation.json`,
`source-reviewed.json`, `source-audit.json`, `negative-checks.json`,
`reproduction.json`, `fresh-process-reproduction.json`, `source-boundaries.json`,
`prospective-timings.json` and `completion-audit.json`. Session evidence:
`archive/pdf/1992-12/evidence/session-2026-11-01-45/`.

Batch 65 directly reviews twenty pending pages: 82–89, 91–93, 95–97, 105–106
and 340–343, for year-feature continuation 0019 and UNIX terminal-control 0022.
Nineteen are full advertisements. Physical 105 is an independent unlisted
편집자 노트, 응용 소프트웨어 개발로 승부를 걸자, with actual visible magazine folio 95.
Its original whole-page image and classification remain outside the forty-five
canonical identities; editorial body transcription is outside this checkpoint.
No new identity or canonical ownership is inferred. The printer advertisement on
89 includes a writer's portrait/quotation; newspaper clippings on 340 remain inside
a program-development-tool advertisement. The Sora1.5 graphical DOS-shell promotion
on 341 is advertising, not the human-shell or terminal-control article. Neither
target body is observed. No mapping, recognition, retry or source correction occurs.

The four-file sidecar at
`archive/pdf/1992-12/restoration/batch-65/accounting-r01/` represents all 446 slots:
425 classified and 21 explicitly pending. Three exports match byte for byte,
including a fresh process. Only twenty prior pending rows change; all other 426
page rows remain unchanged. Prior accounting audits are reexecuted through original
pinned review/render/ownership inputs, retaining twenty-two explicit review/render
bridges. All forty current native/layout images decode. Current source classes
include 171 full advertising pages and one unlisted editorial; 238 selected body
pages/31 maps and 31 map-local exclusion records across fourteen mixed body pages
remain unchanged. The shell-listing fragment on 300–305 remains unassigned.
Pending pages are 344–359 and 442–446. Actual folio 95 is read directly; no global
offset, newspaper date or promotional number is substituted for a magazine folio.

Twenty consistently rehashed private accounting mutations are rejected by the
private source audit, including loss of the editorial's actual folio. No generic
article-schema claim. All 72,158 prior December files, 13,001 selected
article files/31 roots, sixteen classifications, 9,332 September files and thirty
core/source/runtime/TOC/queue pins remain exact. The unchanged 213-test baseline
is reused. Four accounting files do not increase the selected article-file count.
Stage wall times include preservation, rendering, evidence checks and orchestration;
they do not measure isolated manual-review or restoration throughput.

All 45 canonical entries remain unchanged: thirty readable/sample-reviewed, one
partial, seven groups, three section references and four unresolved. Next checkpoint
66 reviews physical 344–359 and 442–445 for the same two location tasks within 2/6/20
limits. Physical 446 remains pending beyond that twenty-page checkpoint. Year-feature
0019 remains partial at opener 299, with ending/children 0020/0021 unresolved;
UNIX 0022/0023 remain unresolved. No source-wide absence, missing-page count, new
ownership, complete accounting or cover verification is claimed. Remaining bodies/
assemblies or explicit source gaps, all 446-page accounting, cover verification,
standalone JSON/assets issue export/rebuild and closeout remain required.
Full December objective active. No reader rebuild.

Evidence: `archive/pdf/1992-12/restoration/batch-65/validation.json`,
`source-reviewed.json`, `source-audit.json`, `negative-checks.json`,
`reproduction.json`, `fresh-process-reproduction.json`, `source-boundaries.json`,
`prospective-timings.json` and `completion-audit.json`. Session evidence:
`archive/pdf/1992-12/evidence/session-2026-11-01-46/`.

Batch 66 directly reviews physical 344–359 and 442–445 for existing location
tasks year-feature continuation 0019 and UNIX terminal-control 0022. Eighteen pages
are full advertisements. Landscape 442–443 are the two sides of a subscription/
remittance form, retained as their own class, separate from reader cards 440–441.
Blank fields and historical payment/subscription information remain original image
context. Product-history years on 347, the UNIX course panel on 353 and software/
music demonstrations on 355–358 are advertising; neither target body is observed.
No mapping, OCR, retry, source correction or canonical entry advance occurs.

The four-file sidecar at
`archive/pdf/1992-12/restoration/batch-66/accounting-r01/` represents all 446 slots:
445 classified and only physical 446 pending. Three exports match byte for byte,
including a fresh process. Only twenty prior pending rows change; all other 426
page rows remain unchanged. The prior accounting source-audit chain is reexecuted
through original pinned review/render/ownership inputs, including twenty-two explicit
review/render bridges. All forty current native/layout images decode. The ledger
contains 189 full advertising pages and two subscription/remittance-form sides.
Its 238 selected body pages/31 maps and 31 map-local exclusion records across fourteen
mixed body pages are unchanged, as are editorial 105/95 and the unassigned shell
listing fragment on 300–305. Form/giro identifiers and advertising years are not
magazine folios; no visible magazine folio is observed on these twenty pages.

Twenty consistently rehashed private accounting mutations are rejected, including
substitution of a form identifier for a magazine folio. All
72,240 prior December files, 13,001 selected article files/31 roots,
sixteen classifications, 9,332 September files and thirty core/source/runtime/TOC/queue
pins remain exact. The unchanged 213-test baseline is reused. The four accounting
files do not increase the selected article-file count. Prospective stage wall times
include preservation, rendering and orchestration; they do not measure isolated
manual-review or restoration throughput.

All 45 canonical entries remain unchanged: thirty readable/sample-reviewed, one
partial, seven groups, three section references and four unresolved. Next checkpoint
67 reviews the final pending page 446 and rechecks contents 4–5, year-feature opener
299, shell-fragment boundaries 300/305 and advertisement 306 for the same two tasks:
seven outside pages within 2/6/20 limits, with no preassigned mapped pages. Six views
are rechecks, not six newly classified pages. Existing owners and mixed contexts
must remain intact. Children 0020/0021 and UNIX 0023 are not advanced in this scope.
Full primary classification alone will not prove source-wide absence, a missing-page
count or complete mixed-component/ownership accounting. Remaining year/UNIX bodies/
assemblies or explicit source gaps, final accounting, cover verification, standalone
JSON/assets issue export/rebuild and closeout remain required. Full December
objective active. No reader rebuild.

Evidence: `archive/pdf/1992-12/restoration/batch-66/validation.json`,
`source-reviewed.json`, `source-audit.json`, `negative-checks.json`,
`reproduction.json`, `fresh-process-reproduction.json`, `source-boundaries.json`,
`prospective-timings.json` and `completion-audit.json`. Session evidence:
`archive/pdf/1992-12/evidence/session-2026-11-01-47/`.

Batch 67 directly reviews seven physical pages: contents 4–5, existing year-feature
opener 299, shell-fragment boundaries 300/305, advertisement 306 and final pending
page 446. The latter is a narrow cover-wrap fragment: the spine, part of the front
panel and part of an advertising panel. December 1992 is visible, while front-panel
text is clipped at the scan edge. It is retained as `cover-wraparound-fragment`,
not certified as a complete usable cover asset. No visible magazine folio on 446.

The contents references remain 289 for the year feature and 306/314 for the two
UNIX articles. They are references, not physical-page assignments. Existing year
opener 299 retains its selected ownership, domestic/overseas outline, introduction
and credit; no continuation, intrinsic child-body anchor or ending is established.
Shell page 300/printed 325 starts mid-program at label 0221; 305/330 ends the visible
listing at 1064/blank 1065 above an office-relocation advertisement. No independent
UNIX opening is established. Physical 306 is a removable-HDD advertisement. No new
target body, mapping, OCR, retry, source correction or canonical entry advance.

The four-file sidecar at
`archive/pdf/1992-12/restoration/batch-67/accounting-r01/` classifies all 446 physical
pages, with none pending. Only final row 446 changes; all prior 445 rows, owners,
folios and recorded mixed components remain unchanged. Six rechecks are recorded
separately and do not add six new primary classifications. Three exports match byte
for byte, including a fresh process. All fourteen current source/layout images
decode, and a fresh PDF render of 446 matches the retained native pixels exactly.
The source-audit chain is reexecuted through original pinned review/render/ownership
inputs, retaining twenty-two explicit review/render bridges. The ledger still
contains 238 selected body pages/31 maps and 31 map-local exclusion records across
fourteen selected-body pages. Primary classification is complete; complete mixed-
component/ownership accounting and source-wide target dispositions remain pending.

Twenty consistently rehashed private accounting mutations are rejected, including
cover/date misclassification, altered existing ownership and counting rechecks as
new pages. An inline verifier-adaptation parse failure before any verifier write is
retained with its exact failed-line extract; the exports and source review were
unaffected. All 72,322 prior December files, 13,001 selected article
files/31 roots, sixteen classifications, 9,332 September files and thirty core/source/
runtime/TOC/queue pins remain exact. The unchanged 213-test baseline is reused.
Accounting files do not increase the selected article-file count. Prospective stage
walls include preservation/rendering/orchestration, not isolated manual throughput.

All 45 canonical entries remain unchanged: thirty readable/sample-reviewed, one
partial, seven groups, three section references and four unresolved. Next checkpoint
68 directly audits seventeen mixed contexts for the same two tasks 0019/0022:
selected-body pages 195, 197, 198, 221, 230, 241, 252, 371, 396, 402, 411, 413,
414 and 416, plus shell/ad 305, afterword/advertisement-index 439 and cover fragment
446. Zero newly primary-classified pages are expected; existing article bytes and
owners must remain intact. This remains within 2/6/20 limits, with no preassigned
mapped pages. Children 0020/0021 and UNIX 0023 are outside this two-task scope.
Complete primary classification alone proves neither source-wide absence nor a
missing-page count. Remaining year/UNIX bodies/assemblies or evidence-backed source
gaps, final mixed-component/ownership accounting, cover verification, standalone
JSON/assets issue export/rebuild and closeout remain required. Full December
objective active. No reader rebuild.

Evidence: `archive/pdf/1992-12/restoration/batch-67/validation.json`,
`source-reviewed.json`, `source-audit.json`, `negative-checks.json`,
`reproduction.json`, `fresh-process-reproduction.json`, `source-boundaries.json`,
`prospective-timings.json`, `helper-failure-r01.json` and `completion-audit.json`.
Session evidence: `archive/pdf/1992-12/evidence/session-2026-11-01-48/`.

Batch 68 directly reviews seventeen mixed whole pages for the two existing tasks
0019/0022: 195, 197, 198, 221, 230, 241, 252, 305, 371, 396, 402, 411, 413,
414, 416, 439 and 446. Their 37 semantic component occurrences retain selected
article bodies, independent advertisements/promotions/notices, unlisted PCSHELL
and Excel tips, non-owning technical preface 0033, separately owned technical tips,
the unassigned shell listing, afterword/advertisement index and cover-wrap panels.
All 31 map-local exclusion records across fourteen selected-body pages remain exact.
They are owner-relative contexts with overlaps, not thirty-one independent ads.
No new year-feature continuation/ending or attributable terminal-control body is
identified. No mapped pages, recognition, retry or source correction occurs.

The four-file sidecar at
`archive/pdf/1992-12/restoration/batch-68/accounting-r01/` retains all 446 primary
page rows unchanged and adds the semantic mixed-context inventory, a complete
source-page location-evidence index and two final PDF-pass location dispositions.
Three exports match byte for byte, including a fresh process. All 446 source-image
pins and classification-evidence pointers are rechecked, together with 31 selected
maps; the prior source-audit chain executes through the original review/render/
ownership evidence. All thirty-four current native/layout images decode.
Current whole views are seventeen rechecks, not seventeen new primary pages.

Year-feature 0019 remains its existing partial opening on 299; the continuation,
actual ending and intrinsic child-body anchors remain unlocated. Terminal-control
0022 remains an unidentified body. These two location searches are final for the
supplied PDF pass, with external dispositions superseding active search instructions
in frozen historical records. The existing partial package and canonical entries
are unchanged. Resume these searches only with new source, independent attribution
evidence or a specifically contradicted classification. Unassigned shell fragment
300–305 is retained without certifying its canonical attribution. The result does
not prove original source omission, a missing-page count or universal source-wide
absence, and does not turn an unresolved identity into a recovered article.

Twenty consistently rehashed private mutations are rejected, including lost source
rows, altered ownership/exclusions, PCSHELL misattribution, false original omission
and advancing children outside scope. All 72,380 prior December files,
13,001 selected article files/31 roots, sixteen classification files, 9,332 September
files and thirty core/source/runtime/TOC/queue pins remain exact. The unchanged
213-test baseline is reused. Four sidecar files do not increase selected article
file counts. Prospective stage walls include preservation, render reuse and evidence
reconciliation/orchestration; no isolated manual-throughput claim.

All 45 canonical entries remain unchanged: thirty readable/sample-reviewed, one
partial, seven groups, three section references and four unresolved. The two current
location gaps are finalized; children 0020/0021 and shell 0023 remain pending their
own outcomes. Next checkpoint 69 handles only the two child-reference dispositions,
with direct contents 5/opener 299 rechecks and no preassigned mapped pages, within
2/6/20 limits. Complete recorded mixed-context inventory and reconciled source-page
evidence do not certify final shell ownership, full original-issue recovery or issue
closeout. Remaining child/shell outcomes, integrated final ownership/gap accounting,
usable cover verification, standalone JSON/assets issue export/rebuild and closeout
remain required. Full December objective active. No reader rebuild.

Evidence: `archive/pdf/1992-12/restoration/batch-68/validation.json`,
`source-reviewed.json`, `source-audit.json`, `negative-checks.json`,
`reproduction.json`, `fresh-process-reproduction.json`, `source-boundaries.json`,
`prospective-timings.json` and `completion-audit.json`. Session evidence:
`archive/pdf/1992-12/evidence/session-2026-11-01-49/`.

Batch 69 directly rechecks contents page 5 and parent year-feature opener 299 for
child identities 0020/0021. The domestic/overseas items are contents and opening
outline references, not recovered intrinsic section-body anchors. Their preserved
source forms, including Roman I/II versus canonical numbered titles, remain separate.
Contents reference 289 is not a directly observed magazine folio. No new mapping,
OCR, retry, source correction, duplicate body or canonical availability/classification
change occurs. The original parent partial package and its frozen metadata remain
exact; current external dispositions finalize these dependent reference searches.

The four-file sidecar at
`archive/pdf/1992-12/restoration/batch-69/gap-r01/` contains cumulative final PDF-pass
gap dispositions, two explicit child-reference evidence records, the exact prior
disposition copy and a manifest. Three exports match byte for byte, including a
fresh process. Both complete outline-text ranges resolve into the original pinned
parent article; review references resolve into the two current whole-page observations.
Prior location-index pointers now have explicit pinned JSON contexts in the cumulative
export. The two original-content location-gap records remain byte-equivalent as JSON
values. The complete prior 446-page/mixed-context source-audit chain is reexecuted;
all four current native/layout images decode.

There are four final tasks for this supplied PDF pass: original-content location
gaps 0019/0022 and related child-reference gaps 0020/0021. This is not four missing
independent articles. Year-feature 0019 retains its opener only; terminal-control
0022 has no independently identified body; neither child gains a body/anchor or
new ownership. Missing original extent, original omission, exact attribution and
missing-page count remain unverified. No universal source-wide absence claimed.
The source-supported child outcome is final until new continuation/body evidence
or an independently evidenced intrinsic section anchor becomes available.

Twenty private mutations with consistently rehashed manifests and companion pins
are rejected, including outline-to-body promotion, duplicate ownership, changed
source numbering, altered text ranges and counting children as independent original
content gaps. All 72,456 prior December files, 13,001 selected article
files/31 roots, sixteen classification files, 9,332 September files and thirty
core/source/runtime/TOC/queue pins remain exact. The unchanged 213-test baseline is
reused. Gap/reference files do not increase selected article-file counts. Prospective
stage walls include preservation, render reuse, range checks and orchestration;
no isolated manual-throughput claim.

All 45 canonical entries remain unchanged: thirty readable/sample-reviewed, one
partial, seven groups, three section references and four unresolved. Only canonical
0023 remains pending its own gap/recovery outcome. Next checkpoint 70 uses one
canonical task and eight proposed outside views: contents 5, all six unassigned
shell-listing pages 300–305 and advertisement boundary 306. Confirm attribution and
usable fragment scope before mapping at most six eligible pages. The mid-program
start and code-fragment ending do not establish a complete original article/program.
No preassigned mapped pages. Final integrated ownership/gap accounting, usable cover
verification, standalone JSON/assets issue export/rebuild and closeout remain required.
Full December objective active. No reader rebuild.

Evidence: `archive/pdf/1992-12/restoration/batch-69/validation.json`,
`source-reviewed.json`, `source-audit.json`, `negative-checks.json`,
`reproduction.json`, `fresh-process-reproduction.json`, `source-boundaries.json`,
`prospective-timings.json` and `completion-audit.json`. Session evidence:
`archive/pdf/1992-12/evidence/session-2026-11-01-50/`.

Batch 70 attributes and restores the surviving human-shell listing on physical
300–305, individually read printed 325–330, as a partial native for canonical 0023,
유닉스 쉘을 만들자(마지막회) : 휴먼쉘의 고급 기능. Contents 5 and advertisement
boundary 306 are the two outside views. Named local CD1 reference 9212314 and six
matching declaration occurrences on bounded pages 300/305 support attribution;
all six pages are reviewed for continuity. This comparison covers one article and
two physical pages, without inserting unseen CD text or certifying the whole CD
reference against print. Canonical title, parent, credit, order and reference remain
unchanged; independent PDF opening/title/byline and complete original extent remain
unlocated.

The selected native is
`archive/pdf/1992-12/packages/batch-70-r01/human-shell/`: 63 exact files across selected,
independent and fresh-process exports. All eighteen crops match source pixels,
including six complete original listing panels beside twelve searchable columns.
Twelve initial eng drafts were read completely before one literal source correction
pass; no OCR retry or within-pass crop change. The native preserves 845 printed labels
0221–1065, 852 physical rows, 142 numbered blanks, seven unnumbered wraps/carries,
39 visible signature occurrences, eleven column/page boundaries and 3,656 local
byte ranges. Printed margin numbers remain separate from code. Source defects,
identifier/operator/glyph/spacing candidates and physically split strings stay literal;
original source files/bytes, compilation and execution are unverified.

A metadata-only map revision before OCR corrects the final-label observation without
changing crop pixels: 1065 is a closing brace, superseding the earlier blank reading.
The source-pass candidate at 0577 is GolBaengLee_Command, superseding the prospective
GolBeangLee observation. Original maps, raw drafts, source observations, failed export,
audit and verification helpers remain preserved. Twenty semantic mutations with
consistently rehashed article/manifest pins pass generic structural checks and fail
the private source audit, including false full-body, original-byte, execution and CD
verification claims. All 72,502 prior December files, 13,001 prior selected files,
sixteen classification files, 9,332 September files, thirty core modules and fifteen
local CD reference files remain exact. The unchanged 213-test baseline is reused.
Prospective stage walls include preparation, draft reading, source review and retained
helper failures; no isolated manual-throughput claim.

Three four-file cumulative accounting exports also match, including a fresh process:
`archive/pdf/1992-12/restoration/batch-70/shell-outcome-r01/`. All 446 source pages now
have integrated material/ownership outcomes: 244 selected body pages across 32 maps,
32 map-local exclusions across fifteen mixed selected-body pages, and no pending
primary page. Only six previously unassigned listing rows gain ownership; the other
440 primary rows and all four prior gap target values remain exact. Historical
location indexes stay pinned, with explicit supersession for shell pages 300–305.
All five PDF-pass gap tasks are final: three original-content gaps (partial year
feature 0019, unidentified terminal-control 0022 and partial shell 0023) plus two
related child-reference gaps 0020/0021. These are not five missing independent
articles. No source-wide absence, original omission or missing-page count inferred.

Current totals are thirty readable/sample-reviewed articles, two partials, seven
non-owning groups, three section references and three unresolved identities among
45. Thirty-two selected roots contain 13,064 files; sixteen classifications remain
separate. The shell fragment is complete within its surviving six pages, but starts
mid-program and supplies no independent article opening or proof of complete original
ending. Canonical availability remains partial. Source material/ownership accounting
is complete; complete original article recovery is not verified. Next checkpoint 71
verifies usable cover evidence and final issue integration, then produces and reproduces
the standalone JSON/assets collection before closeout. Candidate source cover views
are 1 and 446; the latter is only a narrow wraparound fragment. Full December goal
active. No reader rebuild.

Evidence: `archive/pdf/1992-12/restoration/batch-70/validation.json`,
`source-reviewed-r02.json`, `source-reading-decisions.json`, `source-audit.json`,
`negative-checks.json`, `reproduction.json`, `fresh-process-reproduction.json`,
`shell-outcome-reproduction.json`, `shell-outcome-audit.json`, `source-boundaries.json`,
`prospective-timings.json` and `completion-audit.json`. Session evidence:
`archive/pdf/1992-12/evidence/session-2026-11-01-51/`.

Batch 71 verifies the usable December 1992 cover and reconciles final delivery
inputs. The donated original `covers/9212.jpg` has a full upright front composition,
visible 92/12/December and the 1992년12월1일 imprint. Its red masthead and Christmas-tree
artwork match complete PDF front cover 1. Physical 446 is a narrow outer-wrap scan
with spine, partial front and cropped advertising; its clipped right edge makes it
unsuitable as a complete front-cover asset. Both whole PDF views and the donated
cover/thumbnail were directly inspected. Zero canonical tasks, zero mapped pages,
two outside PDF pages, no OCR or source correction.

Donated-first priority selects the original photograph without modifying it or the
global cover derivative set. The three-file cover package at
`archive/pdf/1992-12/restoration/batch-71/cover-r01/` contains a 466 × 640 RGB JPEG,
private provenance and manifest. Selected, independent and fresh-process exports
match byte for byte. The proportional, never-upscaled thumbnail follows the existing
480 × 640 bounds, EXIF orientation, quality-80/LANCZOS and metadata-stripping policy.
Only the bounded derivative is intended for issue delivery; the original stays private.
Eight consistently rehashed private checks reject source-priority, date, orientation,
composition, wrap-fragment and thumbnail-dimension errors. The first integration
helper's underscore-versus-hyphen classification mismatch is retained; the corrected
helper uses the existing canonical values, with no data/schema change.

All 72,827 prior December files, 13,064 selected article files across 32 roots,
sixteen classification files, 9,332 September reference files, thirty core modules,
source/runtime/TOC/queue pins, donated original and prior global cover artifacts remain
exact. The unchanged 213-test baseline is reused. The delivery-input report reconciles
all 45 canonical identities, thirty readable articles, two partials, seven groups,
three section references and three unresolved identities. All 446 source pages and
five final PDF-pass gap outcomes remain accounted: three original-content gaps plus
two related references. No body ownership or canonical outcome changes. Current cover
provenance supersedes historical pending-cover flags without mutating those records.
Complete original article recovery remains unverified.

Next checkpoint 72 produces the portable standalone JSON/assets issue collection,
independently regenerates selected natives/assemblies, checks local asset/correction
references, runs fresh focused regressions and audits every issue-closeout requirement.
The issue is not closed yet. Human acceptance/full proofreading, original program bytes
and execution remain unverified. Full December goal active. No reader rebuild.

Evidence: `archive/pdf/1992-12/restoration/batch-71/validation.json`,
`source-reviewed.json`, `source-audit.json`, `negative-checks-r02.json`,
`reproduction.json`, `cover-recipe.json`, `issue-integration.json`,
`prospective-timings.json` and `completion-audit.json`. Session evidence:
`archive/pdf/1992-12/evidence/session-2026-11-01-52/`.

Batch 72 completes the December 1992 canonical TOC JSON/assets restoration pass
under steps 8, 9, 11, 12 and the single-issue handoff checks of step 14. All 45
identities have explicit outcomes: thirty readable/sample-reviewed articles, two
partial articles, seven non-owning group headings, three anchored section references
and three unresolved identities. Canonical titles, order, bylines, parents and original
contents references remain exact. All 446 physical pages have material/ownership
accounting. The 247 selected owner assignments cover 244 distinct body pages across
32 maps; 32 map-local exclusions cover fifteen mixed selected-body pages. Shared
pages 414 and 416 retain separate region ownership.

The standalone collection is `archive/pdf/1992-12/reference/`: 13,097 files, including
all 13,064 immutable selected article files, the 45-row TOC/accounting, sixteen exact
classification files, donated-cover thumbnail/provenance, page/mixed/gap/ownership
reports, active reading-field indexes and resource-context bindings. It requires no
renderer or browser. All 59 single-map natives regenerate exactly from frozen recipes;
all fourteen actual assemblies consume regenerated natives through the unchanged
private adapters. A separate fresh-process issue export consumes those regenerated
bodies and independently rebuilt cover/accounting/gap/delivery evidence. Every one
of the 13,097 files matches byte for byte.

All 3,365 native source crops match retained render pixels; 3,023 selected body OCR
settings retain their exact original execution maps, including unchanged-result reuse.
All 333,116 typed UTF-8 range occurrences validate in 73 current/native contexts,
including 14,070 empty anchors and 160,291 native projection pairs. Joined prose is
independently reconstructed from native texts; assembled listings equal native listing
concatenation. Every published block correction fragment, three final child anchors,
two dependent outline references and 247 current owner-map pointers resolve locally.
The collection includes 32 active reading-index entries with 772 field pointers and
23,479 original-repository-to-bundled aliases. Exact historical child-evidence bytes
are co-located with their cumulative gap report. Retained private PDF/donor/TOC/runtime/
recipe/review/helper/CD fingerprints are explicitly distinguished from consumer paths.

All 3,356 distinct published images fully decode. Every one of 22,692 members in
73 distinct ZIPs has a safe relative path, valid CRC and exact bundled-file bytes.
No HTML/frontend artifact, original PDF or donated original is bundled. The verified
466 × 640 cover follows donated-first priority; source 446 remains only a clipped
wraparound fragment. Fresh 213 PDF tests pass. Sixteen fresh canonical-accounting
model fixtures have consistent input manifests and reject invalid identity/ownership/
anchor/partial/gap claims; the twenty shell and eight cover rehashed semantic checks
remain preserved. The actual validation scopes are separate and recorded.

All 71 earlier checkpoints satisfy the 2-task/6-mapped-page/20-outside-page ceilings.
Historical records reconcile 3,030 recognition calls: 3,023 selected body outcomes,
four non-owning heading-context outcomes and three changed-crop calls. There are
55 recorded source correction passes and zero unchanged-input recognition retries.
These are retained assistant workflow attestations, not independent observation of
mental reading, manual throughput or human proofreading. All 72,872 prior December
files, 13,064 selected article files, sixteen classifications, 9,332 September reference
files, thirty core modules, sixteen private adapters, fifteen touched CD reference
files, donated/global cover inputs and source/runtime/TOC/queue pins remain exact.
Failed and unique helper/source revisions remain archived.

Five PDF-pass gap outcomes remain explicit: original-content gaps for partial year
feature 0019, unidentified terminal-control 0022 and partial human-shell 0023, plus
related child-reference gaps 0020/0021. Year feature 0019 has only its opener on 299;
shell 0023 preserves the continuous listing fragment on 300–305 without an independent
opening, prose/listing start or certified complete original extent. The two children
have outline references without intrinsic body anchors. These are not five independent
missing articles. No source-wide absence, original omission or missing-page count is
inferred. Complete original article recovery, original program files/bytes, exact
source glyphs/spaces, historical/technical truth and execution remain unverified.
Human acceptance/full proofreading and volunteer glyph/bitmap work remain deferred.
Other issues and collection-wide aggregation are separate work. No reader rebuild.

Validation and reproduction evidence is retained in
`archive/pdf/1992-12/restoration/issue-closeout-01/` and
`archive/pdf/1992-12/evidence/issue-closeout-01/`. `handoff-r02.json` documents private
inputs, fresh output/resume/build/export/check commands and limits. Use a fresh
output for every revision; retain originals and unique evidence. The final save,
cleanup and commit checks are recorded in `verified-after-cleanup.json` and
`completion-audit.json` in the evidence directory.

## September 1991 closeout, 2026-10-31

September 1991 is complete as a canonical TOC JSON/assets restoration pass:
29 identities account for 23 readable/sample-reviewed articles, four non-owning group
headings and two non-owning section references, with no partial or unresolved entries.
All main/available bodies, actual article assemblies and final child anchors are complete.
Canonical titles, order, parents and original contents references remain unchanged.

Complete original article recovery remains unverified. Final dispositions retain two
unrecovered original-content gaps: B+tree's referenced 〈리스트 2〉 SAMPLE.C and the
community questionnaire. The seminar's application form inside that questionnaire is
one related unrecovered reference, with null physical target. These search/disposition
tasks are final for this PDF pass. Source 405's literal 397~398 placeholder and folio jump
396→399 do not identify unavailable content or verify a missing-page count. Subscription/
giro forms, quiz prize material, disk catalogue and source distribution claims are not
recovered forms or program bytes. No issue-wide absence or reconstructed-content claim.
All original package/ledger gap and reference metadata remains exact; final current
dispositions are separate and explicitly linked to the preserved evidence.

Index: `archive/pdf/1991-09/reference/issue.json`; outcomes and limits:
`archive/pdf/1991-09/reference/accounting.json`, `coverage-gaps.json` and
`final-gap-dispositions.json`. All 9,332 standalone files match the independent second
export byte for byte. All 48 single-map natives were regenerated from frozen recipes;
all thirteen actual assemblies consumed regenerated natives through the original thirteen
private adapters. The 23 selected packages contain 9,318 exact files. Two active radar/
community reading companions retain 73 exact source-index fields with explicit article
asset/download contexts, 117 body fragments, 48 continuation links and one cross-native
link. Complete eligible original images for all thirty companion body pages remain exact.

All 406 physical source pages have content records: 224 selected body pages/224 assignments
and 182 directly reviewed outside pages, zero pending/shared pages and eight mixed exclusions.
All ten accounting checkpoints, both disposition exports, cover/provenance and the independent
ownership audit reproduce exactly. Every selected/native exclusion is audited; nonfigure
regions are disjoint and any overlapping original figure pixels retain their white masks.
Literal/null folios, the unlisted editorial and all bounded outside observations remain unchanged.
Complete physical-page accounting is separate from recovery of unavailable original content.

The audit validates 2,534 regions, 1,731 blocks, 446 figures and 277,483 typed byte-range
occurrences across 61 root/native contexts, including 38 exact source-local metadata payloads
and 87,979 current/native projection pairs. Every native crop matches the retained render pixels.
All 2,535 published image files/2,458 distinct images fully decode; all 61 distinct ZIP assets
pass CRC checks. All 2,088 settings retain mapped Tesseract OEM1/PSM6/thread1/3000px/300DPI hint/
interword spaces: 189 eng code regions and 1,899 kor+eng other regions. Declared local resources,
3,834 correction-evidence fragments, both child anchors and detailed gap contexts resolve.

All 73 earlier checkpoints satisfy two canonical tasks/six newly mapped pages/twenty outside
lookups. Their 48 OCR checkpoints retain one source-correction pass each: 2,088 initial plus
five changed-crop recognitions, 2,093 actual invocations, zero unchanged-input retries.
Batches03/05/16/25 each repair one crop before correction; Batch29's repair resumes the same
paused pass. Batch07's nine-value/absent-slot correction adds no OCR. Batch19's supplemental
outside page 243 is conservatively counted; Batch16's recorded retry means its changed input.
Raw-before-pass attestations and completion-only timing limits remain explicit. All failed
helpers/logs, refinements and source/metadata revisions are retained without source changes.

The donated cover supplies a 466 × 640 RGB JPEG thumbnail, 62,344 bytes, independently
reproduced with exact provenance. Metadata is stripped and full framing/worn edges/aspect ratio
are preserved without crop or upscale. The original donor and verified PDF alternatives remain
private and unchanged; the donor is not bundled.

Fresh `make test-pdf PYTHON=.venv/bin/python` passes all 213 tests. Twenty-two invalid canonical,
ownership/outcome/anchor/accounting/gap/portable-path mutations are rejected. All 41,297 prior
issue files, 336 cover inputs, 9,272 initial prior-reference files, thirty core modules, thirteen
private adapters and the cover helper remain exact. All 110 original inventory files are
preserved; 1,701,187 historical issue-file pin occurrences have zero mismatches.

Validation: `archive/pdf/1991-09/evidence/issue-closeout-01/report.json`.
Reproduction/private-input commands:
`archive/pdf/1991-09/restoration/issue-closeout-01/reproduction.json`.
The final requirement-by-requirement completion audit and saved-state checks accompany the
closeout. No further September checkpoint is scheduled; other issues and collection aggregation
are separate work. No new OCR, source correction, reader/HTML/browser/frontend build or deployment.
Human acceptance/full proofreading, original encoded bytes/exact spaces/glyph identities/counts,
historical/technical/contact/geographic claims, program execution and independent backup recovery
remain unverified. Body prose, embedded lettering and glyph/diagram-label tasks remain explicit
volunteer work, with complete original image evidence retained.

See [September progress](docs/progress/9109.md) and
[ledger](metadata/catalog/pdf-restoration/1991-09-progress.json).

## August 1991 closeout, 2026-10-30

August 1991 is complete as a canonical TOC JSON/assets restoration pass:
35 identities account for 28 readable/sample-reviewed articles, five non-owning
headings and two non-owning section references, with no partial or unresolved entries.
All canonical bodies, actual assemblies and child anchors are complete. Unlisted
material remains outside the article queue; canonical titles, order and parents are unchanged.

Index: `archive/pdf/1991-08/reference/issue.json`; outcomes and coverage limits:
`archive/pdf/1991-08/reference/accounting.json` and `coverage-gaps.json` in that directory.
All 9,272 standalone files match the independent second export byte for byte.
All 48 single-map natives were regenerated from frozen recipes; all sixteen actual
assemblies consumed regenerated natives. The 28 selected packages contain 9,201 exact
files. Four original private adapters and BASIC0004's legacy old-TOC/current-identity
guard remain pinned. Both active news/community reading indexes are included with
explicit article-relative asset/download contexts; their original provenance stays private.

All 383 source pages have content records: 211 selected body pages/211 assignments
and 172 directly reviewed outside pages, zero pending/shared pages and 21 mixed exclusions.
All nine accounting checkpoints and the independent ownership audit reproduce exactly.
Every selected/native exclusion is audited; nonfigure regions are disjoint from exclusions,
and overlapping original figure pixels retain the original white masks. Literal/null
folios, the unlisted editorial and all outside observations remain unchanged.

The audit validates 2,460 regions, 1,836 blocks, 392 figures and 271,538 typed range
occurrences across 64 root/native contexts, including 36 exact source-local metadata
payloads. Companion indexes retain 1,235 current/native range pairs, complete eligible
original images for 36 body pages and all column/page continuation links. Every native
crop matches the original retained render pixels. All 2,436 distinct published images,
including cover and original CD bitmap/derivative, fully decode; all 64 distinct ZIP
assets pass CRC checks. All 2,068 OCR settings retain OEM1/PSM6/thread1/3000px/300DPI
hint/interword spaces: 150 eng code regions and 1,918 kor+eng other regions.

All 73 earlier checkpoints satisfy two canonical tasks/six newly mapped pages/twenty
outside lookups. Their 46 new OCR checkpoints retain one source correction pass each:
2,054 initial plus six changed-crop recognitions, 2,060 new invocations, zero unchanged-input
retries. Fourteen retained legacy pilot settings are separate. Batch05's three repairs
and Batch13's one preceded correction; Batch08's two occurred within its one paused/resumed
pass. Batch38's narrative supplement and Batch43's formal-link repair remain explicit.
The original failed checks/helpers and all source/metadata revisions are retained.

The donated cover supplies a 466×640 RGB JPEG thumbnail, 65,291 bytes, independently
reproduced with exact provenance. Source metadata is stripped; aspect ratio and full
framing are preserved without cropping or upscaling. Donor and PDF alternatives remain
private and unchanged; the donor is not bundled. The existing BASIC/CD1 correspondence
sidecar is included: 58 exact files, bounded to PDF84–85 and thirteen complete text blocks.
Its whole CD article remains unverified; neither CD nor scan data was edited.

Fresh `make test-pdf PYTHON=.venv/bin/python` passes all 213 tests. Fourteen invalid
canonical/ownership/outcome/child-anchor/page-accounting mutations are rejected. All
40,445 prior issue files, 176 initial shared files, 336 cover input/evidence files,
156 earlier inventory files, thirty core modules and four private adapters remain exact.
Two documented historical open-log fingerprints retain their selected closed-log revisions.

Validation: `archive/pdf/1991-08/evidence/issue-closeout-01/report.json`.
Reproduction and private-input commands:
`archive/pdf/1991-08/restoration/issue-closeout-01/reproduction.json`.
The final completion audit and saved-state checks accompany the closeout. No further
August checkpoint is scheduled. Other issues and collection aggregation are separate work.
No new OCR, source correction, reader/HTML/browser/frontend build or deployment.
Human acceptance, full proofreading, source encoded bytes/spacing/glyph identities/counts,
historical or technical claims, execution and independent backup recovery remain unverified.
Body prose, embedded lettering/handwriting and glyph/diagram-label work remain explicit
volunteer tasks, with complete original image evidence retained.

See [August progress](docs/progress/9108.md) and
[ledger](metadata/catalog/pdf-restoration/1991-08-progress.json).

## January 1988 closeout, 2026-10-28

January 1988 is complete as a canonical TOC JSON/assets restoration pass:
51 identities account for 36 readable/sample-reviewed articles, 14 non-owning
headings and one explicit unresolved survey eligibility/location gap. There are
no partial articles or pending body-page assemblies among the classified articles.
Survey 0032 retains its original contents reference 175 and null body ownership.
The PDF22–23 awards spread is preserved as bounded context, without substituting
it for a questionnaire or claiming source-wide absence. Complete accounting does
not mean every listed article was recovered; PLAN-PDF reports unresolved
eligibility separately from classified article outcomes.

Index: `archive/pdf/1988-01/reference/issue.json`; outcomes and gap report:
`archive/pdf/1988-01/reference/accounting.json`. All 8,360 issue files match the
independent second export byte for byte. All 50 single-map native inputs were
regenerated from frozen recipes, then all nine assemblies consumed those regenerated
natives. The 36 selected packages contain 8,350 exact files. Seven private assembly
adapters and the separate legacy old-TOC/current-identity guard remain pinned;
all original/native metadata, historical scope notes and failed attempts are retained.
Nine invalid ownership/outcome/gap mutations were rejected.

The audit validates 2,329 regions, 1,647 blocks, 490 figure records and 573,137
typed byte ranges across 59 native/assembled contexts. All 2,320 distinct package
images decode, and all 2,329 native crops exactly match the retained source-render
pixels with their original orientation and exclusion masks. All 1,839 published
OCR settings retain OEM1/PSM6/thread1/3000px/300DPI hint/interword spaces:
330 eng code regions and 1,509 kor+eng other regions.

All 65 earlier checkpoints satisfy two canonical tasks/six mapped pages/twenty
outside lookups. Their 47 OCR checkpoints retain one source correction pass each.
Actual January recognition invocations were 1,828 initial plus nine changed-input
repairs, 1,837 total, with zero unchanged-input retries. Batch02's one repair
preceded source correction; Batch40's five-plus-three repairs resumed the same
paused pass after crop review and raw reading. Batch01's raw-reading order is an
explicit method attestation without a separate raw-reading timestamp. The current
1,839 settings include 11 retained legacy pilot regions; these are distinct counts.

All 242 pages have content records: 188 selected body pages/190 assignments and
54 reviewed outside pages. Outside material includes 45 advertisements, cover,
contents/colophon, unlisted New Year editorial, two awards pages, events calendar,
public-software catalogue, subscription/distribution and mixed page240. The static
ownership audit covers 33 selected and 12 native exclusions. Shared pages100/167
have 336 region pairs, including 240 disjoint nonfigure pairs; only one identical
small folio image overlaps. Literal/null folios and unlisted neighboring areas stay
unchanged. These are frozen source reviews and independently rebuilt geometry,
without a new full-body proofreading claim.

The dated donated cover supplies a 480×605 RGB JPEG thumbnail, 47,370 bytes,
with metadata stripped and aspect ratio preserved without cropping or upscaling.
Its independent transformation and provenance JSON are exact; the full donated
original and PDF alternative remain unchanged and private. The donor is not bundled.
Fresh `make test-pdf PYTHON=.venv/bin/python` passes all 213 tests. All 49,645 prior
issue files, 65 earlier inventories, 134 pilot files, 30 core pins and eight private
adapters remain exact. Every source/crop/raw/settings/transcript/correction/native
segment/helper revision/export/rebuild is retained.

Validation: `archive/pdf/1988-01/evidence/issue-closeout-01/report.json`.
Reproduction: `archive/pdf/1988-01/restoration/issue-closeout-01/reproduction.json`.
The completion audit and final preservation inventory accompany the closeout.
No further January restoration checkpoint is scheduled. No reader rebuild,
HTML/browser/frontend work, deployment or other-issue restoration was performed.
Human acceptance, full proofreading, original encoded bytes, exact spacing/glyph
identities and counts, historical/technical claims, program execution and independent
backup recovery remain unverified. Former0023/original105 history, postal samples,
scanner glyphs and two graph panels retain their recorded manual-review limits.

## November 1985 closeout, 2026-10-26

November 1985 is complete as a canonical TOC JSON/assets restoration pass:
46 identities account for 39 readable/sample-reviewed articles, six non-owning
headings and one explicitly unresolved Software Contest eligibility/location gap.
There are no partial articles or pending assemblies among the classified articles.
Software Contest 0035 retains contents reference 176, which conflicts with the
independently titled diskette offer on source 176. No unrelated notice or article
is substituted, and no full-source absence is claimed. This is documented coverage,
not a claim that every listed article was recovered. PLAN-PDF permits separately
reported unresolved eligibility in a completed usable restoration pass.
Index: `archive/pdf/1985-11/reference/issue.json`; coverage and gap report:
`archive/pdf/1985-11/reference/accounting.json`. The collection has 9,644 files;
all are byte-identical to a second export built from independently regenerated
packages. All 39 packages were rebuilt from their frozen recipes: 9,638 exact
files, including ten immutable assembly formats. Private adapters add format
dispatch and explicit unresolved accounting without changing thirty core files.
Seven invalid ownership/outcome mutations were rejected by the accounting check.
All 2,630 regions, 2,123 blocks and 483 figures validate;
556,020 local UTF8 excerpt records in their proper projected/native contexts and
2,562 distinct decoded images pass. All 2,147 mapped OCR settings retain pinned
Tesseract OEM1/PSM6/thread1/3000px/300DPI hint/interword spaces: 365 eng code and
1,782 kor+eng other regions. All 66 earlier checkpoints satisfy two canonical
tasks/six mapped pages/twenty outside lookups; 51 OCR checkpoints retain one source
correction pass each and zero recognition retries. No new closeout OCR or correction.
All 266 source pages are accounted: 224 selected body pages/233 assignments and
42 outside-body pages. Thirty mixed exclusions and nine shared pages/368 disjoint
cross-owner nonfigure pairs remain exact. Outside-body material is 35 advertisements,
one cover, one issue-title, one unlisted slogan-winners notice and four SMALL HCOPY
pages on 206-209. Contents, lower36 bulletin/photo and colophon stay separate.
The page36 review-note correction is explicit; original package boundaries and
historical parent/pending-owner notes remain unchanged as provenance. Folios and
all provisional source observations remain literal, with no global offset.
The dated donor cover is the source of a validated 474 by 640 RGB JPEG thumbnail,
67,034 bytes, independently rebuilt exactly. EXIF and other source metadata are stripped;
aspect ratio is preserved without upscaling or cropping. The donated original is
unchanged and private; it is not bundled. PDF source/candidate alternatives remain.
Fresh `make test-pdf PYTHON=.venv/bin/python` passes all 213 tests. All 53,996 prior
issue files, 66 earlier inventories, ten adapters and thirty core pins remain exact.
Batch54's original recorder-log inventory exception remains historical; its selected
stable revision02 has literal pins. All source attempts, maps, crops, raw drafts,
settings, corrections, failed checks, native segments and prior rebuilds remain.
Validation: `archive/pdf/1985-11/evidence/issue-closeout-01/report.json`.
Reproduction: `archive/pdf/1985-11/restoration/issue-closeout-01/reproduction.json`.
Completion audit and final-state checks accompany the closeout evidence.
No HTML/browser/frontend/reader rebuild, deployment or other-issue work. Responses,
progress logs and documentation use English; original source retains its language.
Human acceptance, full proofreading, original encoded text bytes, exact spacing,
glyph identities, historical/technical claims, execution and independent backup
recovery remain unverified. Original errors and scan-linked uncertainties remain
literal. No further November restoration checkpoint is scheduled.

## October 1985 closeout, 2026-10-25

October 1985 is complete under the canonical TOC JSON/assets scope. All 39 entries
are accounted for by 35 readable, assistant sample-reviewed articles and four
non-owning headings. No partial articles, unresolved eligibility or article assembly
remain. Canonical identities, titles, order and parent relationships are unchanged.

The standalone index is `archive/pdf/1985-10/reference/issue.json`; the validation
report is `archive/pdf/1985-10/evidence/issue-closeout/report.json`. All 9,031 issue
files match the independent rebuild, including all 9,025 selected-package files.
The packages retain 2,416 regions, 1, 662 blocks and 404 figures. All
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

Details: [October log](docs/progress/8510.md) and
[ledger](metadata/catalog/pdf-restoration/1985-10-progress.json).

## March 1985 closeout, 2026-10-23

March 1985 is complete under the canonical TOC JSON/assets scope. All 48 entries
are accounted for by 39 readable, assistant sample-reviewed articles and nine
non-owning headings. No partial articles, unresolved eligibility or article assembly
remain. Canonical identities, titles, order and parent relationships are unchanged.

The standalone index is `archive/pdf/1985-03/reference/issue.json`. The whole-issue
validation report is `archive/pdf/1985-03/evidence/issue-closeout/report.json`; the
completion record and requirement audit are in the same directory. All 9,588 issue
files match the independent rebuild, including 9,582 exact selected-package files.
The 39 packages retain 2,743 regions, 2,069 blocks and 674 original figures; all
385,683 local UTF-8 excerpt ranges and 2,715 distinct images validate. All 14 private
assembly formats retain their native files, full metadata and source uncertainties.
Reproduce/check using `archive/pdf/1985-03/restoration/issue-closeout/reproduction.json`.

All 244 source pages are classified: 217 contain selected article bodies and 27 are
outside-body material (22 advertisements/promotions, two unlisted reference charts,
one contents page, one cover and one publisher notice). Seven pages have two owners;
all 162 pairs of non-figure regions are disjoint. Four small overlapping image pairs
contain only common printed folios. All 28 native exclusion records remain exact.
PDF208's printed folio stays null. Unlisted charts10–11 and notice147 remain private
source images outside canonical transcription; no new article identities were added.

The donated cover thumbnail is verified: RGB JPEG, 477×640, 60,112 bytes, metadata
stripped, with an independently identical private rebuild. The donated original and
existing derivative remain unchanged. Fresh `make test-pdf PYTHON=.venv/bin/python`
passes all 213 tests. All 61,311 earlier files, 75 prior checkpoint inventories,
30 core implementation pins and 14 private adapters remain unchanged. Every prior
attempt, crop, raw OCR, correction, recipe, native and failed revision is retained.

All 75 restoration/accounting checkpoints meet the two-task/six-mapped-page/
twenty-outside-lookup limits. The 53 OCR checkpoints retain 2,069 pinned Tesseract
tasks and one recorded source correction pass each. Batch52's four replacement
crops were observed after OCR launch; that explicit timing exception and later
source checks remain in the final audit. The two accounting verifier failures
and all earlier failed attempts remain preserved.

Human acceptance/full proofreading, source encoded bytes/spacing/glyph counts,
historical/technical claims, code execution and independent backup recovery remain
unverified. News/classified-body transcription and custom glyph/diagram labels await
volunteers. No reader was rebuilt. March has no remaining restoration checkpoint.
Any next-issue work is separate; the next supplied eligible campaign issue is
October 1985, and none of its restoration is included in this closeout.

Details: [March log](docs/progress/8503.md) and
[ledger](metadata/catalog/pdf-restoration/1985-03-progress.json).

## February 1985 closeout, 2026-10-22

February 1985 is complete under the canonical TOC JSON/assets scope: all 56
entries are accounted for by 48 readable, assistant sample-reviewed articles and
eight non-owning headings. No partial articles or unresolved eligibility remain.
All 260 PDF pages are classified: 232 contain selected article bodies and 28 are
outside-body material. Ten pages have two canonical owners; their 284 pairs of
mapped non-figure regions are disjoint. The donated cover thumbnail is verified.

The standalone index is `archive/pdf/1985-02/reference/issue.json`; the final report
is `archive/pdf/1985-02/evidence/issue-closeout/report.json`. All 10,601 issue files
match the independent rebuild, including 10,595 exact selected-package files.
All 213 freshly rerun PDF tests pass. Reproduce/check the export using
`archive/pdf/1985-02/restoration/issue-closeout/reproduction-r02.json` and the pinned
dispatcher for the 13 private assembly adapters. All 58,348 earlier
files and 30 core implementation pins remain unchanged. Checkpoint details and
source limitations remain in [the February log](docs/progress/8502.md), the ledger
and retained private evidence.

Human acceptance and full proofreading remain pending. Source bytes, exact encoded
spacing, historical claims, code execution and independent backup recovery remain
unverified. Glyph/diagram-label volunteer work and source errors remain explicit.
Unlisted panels and advertisements remain outside canonical-body transcription;
the index's visible-folio 240/TOC 256 conflict is preserved. No reader was rebuilt.
February has no remaining restoration checkpoint. March 1985 is the next campaign
issue; no work on it is included in this closeout.

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
spans/52 text reviews and 32 Unicode candidates. Six ending news reports preserve
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
and 31 assembly pins unchanged. Passing unchanged100-test baseline reused. Both
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
All 71 original/37 revised text panels and four original images reviewed. Twenty-four
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
45 regions, 38 blocks,two images,195 physical listing rows across five code groups,
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
the agreed restoration scope. Step 12 remains open for the other17 eligible issues;
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
2, 664,455,314 bytes (2.48 GiB)**.

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
  membership, image associations,62 regional ranges, 66 review notes and143
  Unicode spans. Independent stories and header regions partition the source;
  no new sentence join is needed. All 71 PDF tests and deterministic rebuild pass.
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
  retain120 physical rows:16 unnumbered,73 numbered and 31 wrapped continuations.
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
  one original HCOLOR-table image,70 regional ranges,43 review notes and 32
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


## November 1985 closeout, 2026-10-26

Completed the canonical TOC JSON/assets pass under steps 8, 9, 11, 12 and the
single-issue handoff checks of step 14. All 46 identities are accounted: 39 complete
readable/sample-reviewed articles, six non-owning headings and one separately
reported unresolved Software Contest eligibility/location gap. The completion
rule explicitly permits this reported gap; no other article replaces it. The
9,644-file standalone collection and all 9,638 regenerated package files are
independently exact; fresh 213 tests and direct range/image/source checks pass.
All 266 pages, thirty mixed exclusions and the donated-cover thumbnail validate.
See the November log, private closeout report and reproduction record. Collection
aggregation, other issues, full proofreading and reader delivery remain separate.
