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

## September 1991 active, 2026-10-31

September 1991 restoration has twenty-three readable/sample-reviewed articles,
no partial articles, four non-owning group headings and two non-owning section references.
All 29 canonical TOC entries are classified; actual article assemblies and child anchors are
complete. Full issue accounting and closeout remain incomplete.

Batch69 directly reviews outside PDF 281,291,297–313,361: twenty advertisements with no visible
printed folios or additional canonical bodies. Retailer, antivirus, interface-converter,
Macintosh-book, music-card, training, monitor-filter and Korean software promotions remain outside
canonical ownership. 모아컴프라자 302–303 and the wholesale-market 304–305 retain paired-page context.
PC Line 312's sideways dealer/financing advertisement retains its source orientation. Commercial
course tables and anniversary prizes do not supply referenced source listings or application forms.
Ten new 3000px views and ten retained full-page views support direct review.

There are now 384 of 406 content records: 224 selected body pages and 160 reviewed outside
pages. Of 182 outside candidates, 22 remain pending. Cumulative outside categories are 156
advertisements, cover, contents, contents/colophon and one unlisted editorial. Every previous
page record, literal/null folio and source index reference remains exact, without a global folio offset.

The 23 selected articles retain 224 distinct body pages/224 assignments, with no shared page.
Forty-eight native contexts and eight exact mixed-page exclusions remain unchanged; the prior
nonfigure/exclusion disjointness audit stays pinned. The accounting JSON matches an independent
fresh-process rebuild. All 29 canonical entries/outcomes, 41,085 prior files, thirty core modules
and thirteen private adapters remain exact. Batch61's 213-test baseline is reused for data-only
work. No new article export, mapping, OCR, source correction or reader build.

Radar 0034 remains complete at radar-complete-r01: nineteen pages 89–95,98–109 and all 740 native
files remain exact in the 748-file assembly. Child 0041's final a-p089-topics anchor and typed
source/body-continuation contexts remain verified. Use pinned Batch61 radar_adapter and its
thirteen-adapter dispatcher. Community 0026's eleven available pages and child 0040's final
a-p387-topics anchor remain complete.

Complete original article recovery remains unverified. The community survey/application form
is unlocated in the bounded community span; source 405's 397~398 placeholder and folio jump
396→399 do not establish missing-content identity. Survey-prize material and giro forms 401–402
are not substitutes. B+ tree 0012's referenced 〈리스트 2〉SAMPLE.C remains unlocated in bounded
body 264–271/appendix 374–381/387–390. Those gap records and the seminar's related application-form
task remain unchanged; no issue-wide absence claim is made. Body prose, embedded screen/cover
lettering and earlier manual glyph tasks remain explicit volunteer work. Human acceptance,
full proofreading, source encoded bytes/exact spaces/glyph identities/counts, historical/technical/
contact/geographic claims, execution and independent backup recovery remain unverified.

Next: Batch70 reviews the next twenty outside pages: PDF 367–379,394–395,399,401–404.
Reuse pinned Batch62 accounting builder/ownership and Batch69 accounting, preserving earlier
records. Finish all 406 pages and final survey/application/SAMPLE.C gap dispositions, then cover,
standalone issue export, independent all-native/actual assembly rebuilds and closeout.
No reader rebuild.
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
