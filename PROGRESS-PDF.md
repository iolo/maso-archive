# PDF restoration progress

Progress for [PLAN-PDF.md](PLAN-PDF.md). Record every PDF restoration step here,
including named batch checkpoints and issue closeouts during the bulk pass. Earlier CD and reading-room
history remains in [PROGRESS.md](PROGRESS.md).

### 2026-09-27 — Plan the supplied PDF restoration pass

- Inspected the 21 PDFs in `maso-pdf/`: 6,615 PDF pages and 2,664,455,314
  bytes. Checked metadata/text availability and representative rendered pages;
  this was planning inspection, not a completed article/page inventory.
- Saved the owner-reviewed sequence in `PLAN-PDF.md`: source/TOC inventory,
  covers, article mapping, one article, one issue, later-format validation,
  remaining issues, reader integration, and final validation.
- Restricted extraction to articles already listed in `TOC.md`. Advertising
  and unlisted material are excluded. March and July 1995 are cover-only
  because the current TOC ends in December 1993. Existing covers are preserved.
- Confirmed local OCR, usable results with visible gaps, and reading-room
  integration. Each step must update this log; the bulk pass also records each
  issue. If a task stalls across three consecutive context windows, stop and
  notify the owner with the blocker and preserved results.
- Validation: checked the TOC endpoint, existing cover filenames, and plan
  consistency with the source inventory and completed CD/reader workflows.
  Restoration implementation has not started; no OCR or source content changed.
- Next: step 1, checksummed source inventory and TOC-only extraction queue.

### 2026-09-27 — Revise checkpoint goals, limits, and sequencing

- Revised `PLAN-PDF.md` following the owner's requested review. The original
  sequence above is superseded; restoration implementation has not started.
- Gave each executable checkpoint a goal, fixed input/scope, saved artifact,
  and acceptance check. Replaced archive-wide advance mapping with mapping for
  the current pilot or batch. Separated OCR setup, pilot packaging, contrasting
  samples, CD comparison, reader export, and browser validation.
- Moved the article record definition and first working reader ahead of bulk
  processing. Added a batch/resume gate before the November and remaining-issue
  milestones, which now require separately logged batches and issue closeouts.
- Set initial ceilings of three articles and 12 distinct source pages per batch,
  with segmented long articles, bounded location research, and one targeted OCR
  retry per failed region. Calibrate ceilings downward from measured sample work.
- Defined separate availability and verification states, explicit pilot/sample
  review requirements, and useful-result gates. Complete queue accounting does
  not imply successful restoration. Deferred unrelated source anomalies.
- Validation: confirmed the existing structured snapshot matches `TOC.md` and
  counted 839 entries / 684 provisional article candidates across 19 supplied
  issues, including 47 entries / 35 candidates for November 1983. Reviewed step
  dependencies, partial-outcome handling, preserved scope, and document links.
  Changes are documentation only; no PDFs, OCR, reader data, or TOC were changed.
- Next: revised step 1, source manifest and provisional TOC queue.

### 2026-09-27 — Step 1: pin sources and the complete provisional queue

- Inputs: all 21 supplied PDFs, current `TOC.md` (SHA-256
  `15d932cf6a34f14981b07ff875d1b5be4f43a525063c303d2d99f54169987727`),
  current structured snapshot and existing identity ledger. Scope was metadata
  only; no article-boundary research or OCR was performed.
- Implemented `tools/pdf_restore/inventory.py`, `make inventory-pdf`, synthetic
  tests and `docs/PDF-RESTORATION.md`. It validates snapshot hashes, records each
  source hash/size and every page's dimensions, rotation, boxes and extractable
  text availability, then publishes the checkpoint only after reconciliation.
- Saved `private/pdf-restoration/inventory/{sources.json,queue.jsonl,report.json}`
  and raw Poppler evidence. Totals reconcile to 21 PDFs, 6,615 pages,
  2,664,455,314 bytes, 19 TOC-covered issues, 839 entries and 684 provisional
  article candidates. November retains all 47 entries / 35 candidates. The
  two 1995 sources remain cover-only without invented TOC identities.
- Every queue row preserves the existing TOC record, hierarchy and provisional
  classification; final article/heading decisions remain unresolved. Source
  labels remain filename-only pending visible date evidence. Twenty PDFs lack
  extractable text; September 1991's text layer is retained without interpreting
  the annotation. No printed-page offset is inferred.
- Validation: four synthetic tests pass, including rotated page metadata,
  missing metadata, text-page reconciliation, complete queue retention and
  snapshot tampering. A complete independent run in `inventory-repeat/` is
  byte-identical (`diff -qr`); source hashes were checked before and after
  extraction. Whitespace checks pass. Original PDF/TOC/CD/cover bytes unchanged.
- Outcome: complete. No stalls or blockers (stall count 0). Next: step 2,
  bounded front-cover inspection and a 21-source cover ledger.

### 2026-09-27 — Step 2: account for all front covers

- Inputs: the pinned 21-source inventory and eight existing owner-supplied
  covers. Inspected PDF page 1 only for each source, within the first/last-five
  page limit. Every front cover is present there; visible dates match all 21
  filename labels. No interior or trailing-page search was needed.
- Implemented `tools/pdf_restore/covers.py`, prepare/install make targets and
  four synthetic preservation/evidence tests. Rendered upright full-page JPEGs
  with Poppler 26.01.0, longest edge 1,800 pixels, quality 92. Rendering applies
  PDF rotation; dimensions and aspect ratios are checked against source geometry.
- Saved candidates, contact sheets, exact reviewed hashes, date-region evidence,
  condition notes and a 21-source ledger under `private/pdf-restoration/covers/`.
  The visible cover dates verify provisional PDF labels; no TOC/CD identities
  or article associations were invented. All covers are usable, with ordinary
  wear and specific clipping/crease damage retained in the review notes.
- Added 19 missing `covers/masoYYMM.jpg` images, including both 1995 covers.
  Preserved the existing November 1983 and December 1984 cover choices; their
  extracted alternatives remain private. All eight original cover hashes match
  the before ledger. No advertising/article extraction occurred.
- Validation: visually inspected all 21 full-cover tiles for date, orientation,
  proportions and condition; checked every installed image hash. Eight PDF
  tests pass, including conflicting dates, changed owner/candidate bytes,
  uncertain outcomes and preserving an existing image with another extension.
- Outcome: complete, 21 usable cover outcomes / 19 added / 2 alternatives.
  Reader presentation remains for step 9. Stall count 0. Next: step 3, map only
  November 1983's “숨겨진 미로” and define its restoration record.

### 2026-09-27 — Step 3: map “숨겨진 미로” and define the package

- Named the one-article mapping checkpoint in
  `private/pdf-restoration/pilot/mapping-plan.json` before rendering. Fixed input:
  `maso-1983-11-toc-0012`, observed opening PDF page 30 / printed 28. Limits:
  one article, 12 article pages, 20 outside lookup pages.
- Inspected PDF pages 29–32: two article pages and two outside lookup pages.
  Pages 33–34 were also rendered but not inspected or mapped. The pilot covers
  PDF pages 30–31 / printed 28–29, with nine ordered regions. Its prose/maze
  figure are followed by two listing columns; line 410 continues across columns
  and the final helper ends with line 690 RETURN. The prose conclusion, complete
  listing frame and separate book-advertisement panel support the ending;
  the next article alone was not used as proof.
- Saved `pilot-map.json` and `mapping-review.json`, including original source
  hash, separate printed/PDF numbering, explicit reading order, normalized
  upright coordinates, source dimensions and rotation transforms. Excluded the
  lower book advertisement on page 31. No continuations were observed. The
  listing starts at 110; earlier missing lines are not asserted.
- Added `schemas/pdf-article.schema.json`, a synthetic package example, the
  structural/geometry validator and documentation. Stable scan IDs derive from
  TOC identity, independently of OCR titles and CD IDs. Raw OCR, corrections,
  figures, downloads, scan/CD relationships and review evidence stay separate.
- Validation: six new synthetic fixtures cover all four rotations with nonzero
  origins, printed/PDF numbering, noncontiguous order, shared-page exclusions,
  missing-page outcomes, unsupported full-review claims and path traversal.
  All 14 focused PDF tests pass; the real pilot package validates.
- Outcome: mapping complete. Availability remains unresolved / verification
  unreviewed until OCR and text review. No bulk gate passed. Stall count 0.
  Next: step 4, pinned local Korean/English Tesseract on one pilot page with
  at most two configurations.

### 2026-09-27 — Step 4: local OCR evidence on pilot PDF page 30

- Tesseract was absent. Downloaded five pinned Ubuntu packages and extracted a
  private runtime under `private/pdf-restoration/ocr-runtime/`; no system
  installation was needed. Engine 5.5.0, Leptonica 1.86.0 and Korean/English
  model packages 4.1.0-2build1 are recorded with package, executable, library and
  model hashes. Setup instructions and host dependency evidence are preserved.
- Processed only mapped pilot PDF page 30 with two configurations: eligible
  page PSM 3 and ordered region PSM 6, `kor+eng`, OEM 1, one thread, 3,000-pixel
  longest-edge rendering. Saved TXT, positional TSV, settings, derivative crops
  and stderr under `pilot/ocr-page30/`. Selected region processing; figures stay
  as crops. Original PDFs, raw evidence and mapping are unchanged.
- Selected configuration preserves column order but does not produce reliable
  reading text unaided: many Korean characters are wrong, the decorative title
  is empty and the byline is incorrect. Page-level output also mixes figure
  noise into prose. Recorded these limits in `pilot/ocr-comparison.json`; no
  third configuration or engine search was attempted.
- Validation: repeated selected-region OCR in `pilot/ocr-page30-repeat/`;
  all 24 TXT/TSV/settings/stderr files match byte-for-byte. Only wall-clock
  timing is excluded. Initial OCR took 8.17 seconds total (4.01 page-level,
  4.16 across six text regions), excluding rendering/setup. A synthetic shared
  page check verifies excluded pixels cannot enter page or region OCR. All 15
  focused PDF tests pass; setup revalidation and whitespace checks pass.
- Fixed a setup-repeat false mismatch caused by changing ASLR load addresses
  in `ldd` output. Comparison now ignores only those volatile addresses and
  preserves the original runtime manifest and all raw OCR/settings hashes.
- Outcome: repeatable local OCR checkpoint complete, with explicit quality
  limits; the useful-pilot and bulk gates remain unpassed. Stall count 0.
  Next: step 5, OCR the pilot's two code regions, preserve raw outputs, compare
  all reading text to the scan, mark uncertain characters, and build the
  complete article package plus reusable standalone preview.

### 2026-09-27 — Step 5: deliver the reviewed “숨겨진 미로” pilot

- Named the checkpoint in `private/pdf-restoration/pilot/package-plan.json`
  before execution: one existing TOC article, two already mapped pages (PDF
  30–31 / printed 28–29), no outside lookup pages. Reused step 4's selected
  prose OCR and processed only page 31's two eligible code regions with the
  pinned Tesseract runtime, region PSM 6 / English model. Code OCR took 1.68
  seconds, excluding rendering; no OCR retries or engine search were needed.
- Visually compared all nine complete mapped regions: platform label, title,
  byline, introduction, maze figure, both prose columns and every printed row
  in both code columns. Saved 14 corrected blocks and separate per-region
  scan/raw hashes and correction decisions in `pilot/corrections.json`.
  Joined prose print wraps and the column continuation; retained physical code
  wraps and existing line-number gaps. The figure has no printed caption.
- Code remains explicitly imperfect: horizontal spacing is unverified, line
  550's quoted blank count is unknown, and line 560 has a possible dot versus
  printing noise before DID. Marked the latter two in the literal transcription
  with `⟦…⟧` and exposed the limits beside the code and in the article status.
  No code execution or semantic repair was performed. Raw OCR and scan bytes
  remain unchanged. Availability is **readable**, verification **sample-reviewed**,
  with full prose/region coverage and those code uncertainties recorded.
- Implemented a pinned recipe builder and portable preview renderer, reusing
  the existing reference HTML/CSS helpers. Added explicit mixed content order,
  region assets and hashed review records to the package schema while retaining
  step 3 map compatibility. Readable exports require complete mapped-region
  representation and reject changed input hashes, mismatched map/OCR evidence,
  missing scan assets and identities outside the TOC queue.
- Delivered `build/pdf-restoration/pilot/index.html` and `article.json`, all nine
  eligible scan crops, raw regional TXT/TSV/settings, original correction/map/
  runtime provenance, UTF-8 article and literal listing downloads, a deterministic
  raw-OCR ZIP, and a complete file manifest (44 files, about 9.35 MB). The lower
  book advertisement and full-page renders containing it are excluded from the
  export and ZIP. Source PDFs and the existing reader data were not modified.
- Validation: all 20 focused PDF tests pass. Five new synthetic tests exercise
  deterministic publication, literal whitespace/HTML escaping, mixed figure
  order, advertisement exclusion, raw-input tampering, missing regions, TOC/path
  rejection, broken links and asset integrity. An independent `pilot-repeat/`
  rebuild is byte-identical, including ZIP bytes and stable scan ID. All earlier
  and new OCR text/position/settings/image pins still match.
- Browser validation with the Playwright skill: desktop 1280×900 and mobile
  360×800; no page overflow, local horizontal code scrolling, decoded maze
  figure and code evidence image, exact DOM code text, and successful hashes
  for nine scan assets plus three downloads. An actual listing download is
  byte-identical to the export. Only the browser's unlinked favicon request
  returned 404. Screenshots are in `output/playwright/pdf-pilot/`; exact checks
  and the checkpoint outcome are pinned in `pilot/browser-review.json` and
  `pilot/package-closeout.json`. Rebuild/check commands are documented.
- Outcome: step 5 complete; useful-pilot gate passes with marked code
  uncertainties. Bulk gate remains unpassed pending contrasting samples and
  reader integration. Stall count 0. Next: step 6a, name at most two November
  contrast samples and resolve nested TOC ownership from local source evidence.

### 2026-09-27 — Step 6a: early-format contrast and nested TOC ownership

- Named one sample before execution in
  `private/pdf-restoration/6a-matchsticks/checkpoint-plan.json`: existing entry
  `maso-1983-11-toc-0013`, 성냥개비, printed title 성냥개비 게임. Mapped PDF
  32–34 / printed 30–32 with 31 regions. Used eight outside lookup pages
  (35 and 6–12), within the 20-page limit; no additional article bodies were
  processed. Completed prose, final listing and figure support the ending;
  the distinct next opening is corroborating evidence only.
- Scanned contents on PDF 10 establishes parent `toc-0011` 취미생활 as a
  page-less group for eleven individually paginated children. Saved this
  decision and child ownership in `ownership.json`, separately from the pinned
  historical queue. No aggregate parent article or duplicate body was created;
  other children's locations remain provisional.
- Reused pinned local Tesseract region PSM 6 for 28 text regions; three figures
  remain complete scan crops. OCR took 14.18 seconds excluding rendering and
  review, with zero retries. Raw Korean/code recognition required substantial
  scan-supported correction. All 121 image/text/position/settings pins checked
  unchanged after export; original PDF and TOC pins also passed.
- Compared all 31 regions for order, omissions, figures and exclusions, and
  all prose/code rows against the scans. The exact sample review includes both
  complete prose columns r05/r06, listing r08 and figures r04/r19/r31. Joined
  four split-word column continuations with both region references. Kept the
  page 33 introduction adjacent to page 34 lines 360/370; placed Figure 1
  immediately before that introduction. Repeated headers and lookup ads do
  not enter reading content. Printed prose inconsistencies remain unchanged.
- Delivered 30 text/code blocks and three figures in
  `build/pdf-restoration/6a-matchsticks/`: **readable / sample-reviewed**,
  31/31 mapped regions represented, 126 files totaling 15,194,201 bytes. Code
  uncertainties remain visible: horizontal/quoted spacing, the line number
  after 270 (280/290), a possible dot on line 430, and line 630's hyphen count.
  Diagram and game/strategy-table contents remain images with their captions.
  No program execution or semantic repair was performed.
- Fixed the reusable preview's rendering of multiple prose paragraphs within
  one block. Extended the synthetic export test to check paragraph separation,
  escaping and unchanged text downloads; all 20 focused PDF tests pass,
  including missing-page, noncontiguous-order, shared-ad and rotation fixtures.
  Export integrity checks pass and `6a-matchsticks-repeat/` is byte-identical.
- Playwright desktop 1280×900 and mobile 360×800 checks pass: correct mixed
  reading order, exact DOM text for all nine code blocks, paragraph separation,
  no page overflow, contained code scrolling, and hashes for 31 scan assets
  plus three downloads. All three figures decode after scrolling into view.
  Screenshots are in `output/playwright/pdf-6a/`. The only console error was
  the unlinked favicon 404. A premature lazy-image decode check was repeated
  after loading; no image bytes or production loading behavior were changed.
- Preserved the package during an interruption before browser completion;
  resumed browser validation without rerunning OCR. Saved feature/result
  matrix, validation, browser review and pinned closeout beside private inputs.
  Outcome: step 6a sample gate passes; bulk gate remains unpassed. Stall count
  0. Next: step 6b, name and restore one eligible January 1988 contrast sample.

### 2026-09-27 — Step 6b: January 1988 rotated/shared-page contrast

- Named existing entry `maso-1988-01-toc-0018`, 터보 파스칼에 한글을, before
  mapping in `private/pdf-restoration/6b-turbo-pascal/checkpoint-plan.json`.
  Inspected PDF 90–95: the article occupies PDF 94–95 / printed 92–93, with
  four outside lookup pages. Visible footers confirm January 1988. The printed
  title includes version 3.0 and byline 정내권; the existing TOC ID is retained.
- Mapped eleven regions across two pages, both with PDF rotation 270.
  Upright renders are 2122×3000; source geometry and explicit affine transforms
  validate. Followed five split-word continuations across columns/pages.
  The conclusion closes above a separator and a distinct unlisted “1라인
  모니터 프로그램” title. Excluded that item's flowchart, code and prose;
  the article itself has no eligible illustration. Decorative section icon
  and repeated running header are excluded separately.
- Reused the pinned Tesseract region configuration for all eleven text/code
  regions: 6.90 seconds of OCR, excluding rendering/review, zero retries.
  Compared every mapped region for order, omissions, upright orientation and
  unwanted content; compared all printed prose/caption/heading rows and the
  complete listing against the scans. Exact sample coverage includes full
  first prose column r04 and code r08. Saved corrected reading blocks and
  per-region scan/raw pins separately from immutable OCR.
- Delivered **readable / sample-reviewed**, eleven blocks representing all
  eleven regions, in `build/pdf-restoration/6b-turbo-pascal/`: 55 files totaling
  4,201,884 bytes. Placed the caption/listing after continuous prose to keep the
  cross-page sentence together. Marked the visibly blank opening phrase after
  보유하고 without guessing words. Code spacing remains unverified; physical
  wraps and printed inline MEM punctuation remain intact. No code execution,
  semantic repair or CD relationship assertion was performed.
- Validation: all 48 OCR image/text/position/settings pins still match; both
  builds verify source/TOC bytes and geometry. The excluded shared-page area
  has ink in the original and is wholly white in the eligible OCR input.
  Neither full-page renders nor neighboring reading content enter the export
  or ZIP. All 20 focused PDF tests pass, including rotation, shared-ad,
  noncontiguous-order and missing-page fixtures. Export integrity checks pass;
  `6b-turbo-pascal-repeat/` is byte-identical. No pipeline changes were needed.
- Playwright checks pass at desktop 1280×900 and mobile 360×800: literal code,
  complete declared reading order, visible source gap, no page overflow,
  contained code scrolling and all eleven scan-asset plus three download
  hashes. Screenshots are in `output/playwright/pdf-6b/`; only the unlinked
  favicon request returned 404. Saved mapping, correction, feature/result,
  validation, browser-review and pinned closeout records beside private inputs.
- Outcome: step 6b sample gate passes with the explicit source/code gaps.
  Bulk gate remains unpassed. Stall count 0. Next: step 6c, name and restore
  one eligible August 1991 article within the same bounded limits.

### 2026-09-27 — Step 6c: August 1991 prose, quotations and portrait

- Named existing entry `maso-1991-08-toc-0004`, 컬럼 마소쉘 : 베이직 언어로
  돌아가자, before execution in
  `private/pdf-restoration/6c-basic-column/checkpoint-plan.json`. The article
  occupies PDF 84–86, with visible printed folios 98 and 99 on the first two
  pages. PDF 86 has no visible folio; its printed page remains unknown.
  Eight outside lookup pages (98–101, 82–83 and 87–88) establish the offset
  and neighboring boundaries. No additional article bodies were processed.
- Mapped fifteen regions: section label, title, byline, two pull quotations,
  a framed portrait and three-column Korean prose. Compared every region for
  order, omissions, figure placement and unwanted material, and all printed
  text rows against the scans. Exact sample coverage includes complete prose
  column r07, portrait r05 and quotations r04/r10. Eight continuations retain
  all source references. The second quotation precedes the complete adoption
  paragraph rather than interrupting its sentence. Both quotations remain
  separate even where they repeat body text.
- Reused pinned local Tesseract PSM 6 for fourteen text regions, with zero
  retries: 16.57 seconds of OCR, excluding rendering and review. Corrected
  the opening drop-cap order and misread names/terms from scan evidence;
  historical terminology and factual claims remain as printed. All 63 raw
  image/text/position/settings pins still match. Source and TOC pins validate.
- Delivered **readable / sample-reviewed** in
  `build/pdf-restoration/6c-basic-column/`: twenty text blocks and one figure,
  all 15/15 regions represented, 67 files totaling 23,092,134 bytes. No code
  listing is present in this article. Drop-cap size, inset/column positioning
  and inline italic emphasis are explicitly normalized; original typography
  remains accessible in the scan crops. No independent second proofreading
  pass or CD relationship is claimed.
- Excluded the distinct boxed recruitment notice below the conclusion on
  PDF 86 and repeated running headers. Pixel checks find ink in the original
  notice and a wholly white area in eligible OCR input. Full-page renders
  remain private and are absent from the export and ZIP. All pages have
  rotation 0; actual upright dimensions are recorded in `validation.json`.
- Updated the reusable exporter to omit `listing.txt` and its download link
  when an article has no code blocks. Added a synthetic regression checking
  retained prose and figure content. All 21 focused PDF tests pass, including
  rotation, missing-page, noncontiguous-order and shared-page fixtures. Export
  integrity passes; `6c-basic-column-repeat/` is byte-identical.
- Playwright desktop 1280×900 and mobile 360×800 checks pass: declared reading
  order, exact DOM text for all twenty blocks, both quotations, decoded portrait,
  unknown-folio links, no page overflow, and hashes/sizes of fifteen scan assets
  plus two downloads. Screenshots are in `output/playwright/pdf-6c/`; the only
  console error was the unlinked favicon 404. Saved feature/result matrix,
  validation, browser review and pinned closeout beside private inputs.
- Outcome: step 6c sample gate passes, completing step 6. Bulk gate remains
  unpassed pending later checks and reader integration. Stall count 0.
  Next: step 7, one evidenced CD association and comparison using a successful
  overlap sample, limited to two mapped comparison pages.

### 2026-09-27 — Step 7: evidenced CD comparison

- Named the successful August sample `scan-maso-1991-08-toc-0004` and candidate
  CD1 reference `9108098` in
  `private/pdf-restoration/7-cd-comparison/checkpoint-plan.json`. Fixed scope:
  one association, PDF 84–85 / printed 98–99, zero new OCR. The debugging
  paragraph crossing into PDF 86 and all subsequent blocks are excluded from
  comparison. Preserved full source records without claiming those excluded
  portions were compared.
- Established a reviewed correspondence using the CD's native `91.8.  98p`
  label, observed printed opening, matching author 박현철 and a substantial
  identical body passage about the author's 1987 advocacy. The matching title
  is corroborating evidence only. Retained CD topic identities 1527/1528 and
  their original source provenance. Neither the existing scan package nor CD
  reference/reader metadata was rewritten to assert a relationship.
- Compared thirteen complete text blocks across twelve mapped regions and
  reviewed the portrait disposition. Recorded 52 exact character edit
  operations; these include whitespace, punctuation and layout differences,
  not 52 transcription-error claims. CD offsets identify original paragraphs
  and absolute Unicode character ranges; scan offsets identify corrected
  blocks with their region and correction-record references.
- The scan confirms two substantive omissions in the CD: the clause about
  discussing BASIC's current state in r09, and the multiple-index phrase in
  r12. A third explicit finding records r12's changed phrase ending. Retained
  scan spellings such as 비쥬얼, 데이타베이스 and 화일 beside differing CD
  spellings. No historical terminology, factual claim or original source text
  was automatically repaired.
- Recorded omitted author-role text and the separate repeated pull quotation.
  The CD contains the inset's underlying prose once, not a second quotation
  occurrence. Its only referenced image, `bm1137.bmp`, is a visually inspected
  32×25 section icon, not the framed portrait. The portrait and section-label
  dispositions concern this CD reference only; no archive-wide absence claim.
- Added `tools/pdf_restore/compare.py`, `make compare-pdf-cd` and
  `make check-pdf-comparison`. The exporter checks pinned inputs, substantial
  association evidence, page limits, paragraph offsets, complete in-scope block
  dispositions and figure references. It writes an independent comparison
  sidecar, never patches either source, and refuses existing output paths.
- Delivered `build/pdf-restoration/7-cd-comparison/`: `comparison.json` for
  post-production, `comparison.md` for reading, exact CD snapshots, unchanged
  scan corrections, selected scan/OCR evidence, mapping/runtime provenance and
  the reviewed recipe. There are 58 files totaling 8,169,355 bytes. Preserved
  private checkpoint, recipe, validation and pinned closeout records.
- Validation: all 24 focused PDF tests pass, including three comparison tests
  covering preservation, deterministic output, exact offsets, altered bytes,
  title-only evidence, unsupported anchors, invalid ranges, incomplete scope,
  page limits and unsupported findings. Repeat output is byte-identical.
  Checked 23 report links, all edit/span offsets, six original CD files against
  the existing reference manifest, and that manifest against its tracked pin.
  All 63 original OCR pins, the prior scan export manifest, source PDF and TOC
  still match. No OCR or CD bytes changed.
- Outcome: step 7 complete; correspondence is **sample-reviewed**, with
  `whole_cd_article_verified: false`. Bulk gate remains unpassed. Stall count
  0. Next: step 8, stage one pilot article through the reading-room version 3
  adapter while retaining version 1/2 support and existing CD records/URLs.

### 2026-09-27 — Step 8 started: staged reader adapter

- Committed the completed steps 1–7 as `d076c3e` after the owner requested
  per-step commits. Future checkpoints include a progress entry and commit.
- Fixed inputs before implementation: pilot `scan-maso-1983-11-toc-0012`
  and the existing combined reader data. Saved input manifest pins and scope
  under `private/pdf-restoration/8-reader-adapter/checkpoint-plan.json`.
- Scope is one scan article in `build/reading-room-pdf-pilot/data`, with a
  separate repeat export. Existing production data remains the baseline.
  Implementing contract version 3 and adapter validation; scan-specific UI
  presentation and browser acceptance remain step 9.
- Implemented the v3 projection and source/region/download pins. The pilot's
  projected text matches its existing UTF-8 download byte for byte; literal
  code blocks retain their own whitespace, with separators kept outside them.
  All 27 PDF tests, eight existing web-export tests and six frontend tests pass;
  TypeScript checking passes. Full combined-data export and repeat verification
  are in progress, preserving existing CD files and routes.

### 2026-09-27 — Step 8 complete: version 3 pilot adapter

- Added `tools/reading_room/scan.py` and `make export-pdf-reader`. It validates
  the baseline and reviewed pilot, stages independent file copies, binds the
  existing issue/TOC identities, checks the result and publishes only to a
  fresh output directory. Production reader data and scan inputs remain intact.
- Extended the static web contract and loader to version 3 while retaining
  version 1/2 documents and existing route identities. New scan records carry
  independent availability/review states, pinned source and region metadata,
  exact content order, figures, downloads, correction/review evidence and gaps.
  Documented path scopes in `docs/READING-ROOM-STATIC-V3.md`; original PDF paths
  are provenance rather than nonexistent full-PDF downloads.
- Copied the complete immutable pilot package under
  `data/source/pdf/scan-maso-1983-11-toc-0012/`. Kept generated reader paragraph
  positions outside that package so its original manifest remains valid.
  All fourteen text/code blocks retain exact text, including both literal
  listings; separate spacing blocks preserve the unchanged full-text download.
  Nine scan regions, one figure and three downloads retain their hashes.
- Delivered `build/reading-room-pdf-pilot/data`: 152 issue groups, 5,497 TOC
  entries, 3,387 article records and 3,379 text downloads, including the one
  added pilot. The export has 44,727 files totaling 3,453,577,239 bytes.
  All 3,386 original CD summaries and identities are unchanged. All 40,980
  original source files and all CD article documents remain byte-identical.
- Only four baseline documents change: catalog, search, November 1983 issue
  and its media index. The new manifest pins the baseline and scan manifests.
  All 44,676 other baseline files retain their paths, hashes and sizes. Only
  the pilot's TOC entry gains an article link; other TOC entries are unchanged.
  No CD relationship is inferred for this pre-CD pilot.
- Validation: 27 PDF tests, eight existing reader-export tests and six frontend
  tests pass; TypeScript checking passes. Synthetic version 1/2 baselines
  preserve CD bytes and yield deterministic version 3 exports. Rehashed edits
  to scan content, geometry, review state, download paths or package provenance
  are rejected. Changed inputs and unknown identities do not replace outputs.
- The complete real export and `build/reading-room-pdf-pilot-repeat/data` pass
  integrity checks and `diff -qr` reports identical trees. Original reader and
  pilot manifests still match their pre-execution pins. Saved validation and
  pinned closeout under `private/pdf-restoration/8-reader-adapter/`.
- Outcome: step 8 complete; bulk gate remains unpassed. Stall count 0.
  Next: step 9, scan-aware reading UI and desktop/mobile acceptance, including
  evidence/download routes, synthetic availability cases and existing CD routes.
  No step 9 browser or scan-specific display acceptance is claimed here.

### 2026-09-27 — Step 9 started: scan-aware reader

- Step 8 is committed as `1d38b23`. Fixed step 9 to its existing pilot,
  synthetic partial/image-only/unavailable cases and representative CD routes.
  Saved manifest/cover-ledger pins and browser acceptance scope under
  `private/pdf-restoration/9-reader-ui/`.
- Implementing separate availability/review presentation, region evidence
  navigation and source-aware labels in the existing application. Reusing the
  existing cover presentation for extracted covers; no new OCR or article
  restoration is included. Playwright desktop/mobile and nested-host checks
  will precede checkpoint completion and commit.
- The scan reader now shows availability and review independently, retains
  exact prose/code, and loads a region image only when selected. The real
  pilot's issue → TOC → article → r08 evidence flow passes at desktop and
  mobile widths under `/archive/`. All thirteen fetched region/download/
  correction assets match pinned hashes. Metadata search fetches no bodies;
  sampled CD1/CD2/CD3 routes and source links remain usable.
- Integrated available covers through the existing adapter: the staged reader
  now has 27 covers. An extracted cover decodes correctly, and an intentionally
  aborted image request shows the existing fallback. Finishing synthetic
  availability checks and final validation; production data remains unchanged.

### 2026-09-28 — Step 9 complete: scan reading and browser acceptance

- Added `ScanArticle.tsx` to the existing application. The pilot shows distinct
  availability/review states, visible remaining uncertainties, expandable review
  scope and correction links, exact prose/code, its figure, three downloads and
  the independent portable preview. The header retains the printed byline,
  including a role when the canonical TOC author omits it.
- Added article-local `?region=<id>` evidence navigation. Selected regions load
  at native resolution in a contained scrolling area, with original-size and
  download links, independent PDF/printed page numbers and a return-to-text link.
  The application never treats an unknown folio as an inferred printed number.
  Unselected region images are not fetched; the inline figure remains lazy.
- Updated shared shelf, issue, TOC and search labels to include scan reading
  without changing CD source labels or identities. Search contains the pilot's
  metadata and opens its existing canonical route. Available material is linked
  without inventing text or source downloads for missing-state fixtures.
- Added optional `--covers` support to the staged adapter, reusing the existing
  cover implementation. All nineteen installed PDF-cover pins match exported
  bytes; existing owner covers are preserved. The reader now presents 27 covers.
  An extracted cover renders with contained proportions; a deliberately aborted
  request and missing-cover fixtures exercise the fallback.
- Delivered the nested-base site in `build/reading-room-pdf-ui/`, served locally
  at `http://127.0.0.1:4178/archive/`. Its data has 44,746 files totaling
  3,466,427,386 bytes. All 44,412 source/article files from step 8 and all 3,387
  article summaries are unchanged. Only the catalog and nineteen issue cover
  records change, with nineteen added cover files and a new manifest. Original
  step 8, pilot and cover-ledger pins remain unchanged.
- Playwright desktop 1440×1000 and mobile 360×800 checks pass: issue → TOC →
  pilot → r08 evidence, mobile TOC navigation, visible review/gaps, exact prose
  and both code blocks, no page overflow and contained horizontal code/scan
  scrolling. Thirteen region/download/correction assets match browser-computed
  hashes and sizes. The independent preview opens successfully.
- Request checks find no article fetches on issue/TOC or fresh search pages,
  and only the pilot body on its routes. Initially only its inline figure is
  fetched; selecting r08 adds that region alone. The later explicit integrity
  audit fetches the other regions intentionally. Existing CD1 `8802184`, CD2
  `cd2-940109500` and CD3 `cd3-topic-0084` routes, downloads/reference links and
  mobile containment pass.
- Invented partial, image-only and failed fixtures run in a separate intercepted
  browser session without changing archive data. Partial text retains its marked
  gap and literal code; image-only material exposes its scan without a body or
  text download; failed recovery shows no broken source links and makes no
  missing-source claim. Unknown region and unresolved-state rendering also pass
  unit checks. Screenshots and snapshots are in `output/playwright/pdf-9/`.
- Validation: 28 PDF tests, eight existing web-export tests and eleven frontend
  tests pass. TypeScript/Vite production build and complete static data integrity
  check pass. No unexpected application console errors occurred; the aborted
  cover request is an intentional failure fixture. Saved validation, browser
  review and pinned closeout under `private/pdf-restoration/9-reader-ui/`.
- Outcome: step 9 complete; pilot remains **readable / sample-reviewed**, with
  its original code uncertainties. Bulk gate remains unpassed. Stall count 0.
  Next: step 10, a bounded batch of already prepared samples with synthetic
  failure and resume checks, within the three-article/twelve-page ceiling.

### 2026-09-28 — Step 10 started: bounded batch and resume

- Step 9 is committed as `99e342e`. Fixed this checkpoint to the prepared pilot,
  January 1988 and August 1991 samples: three existing TOC identities, seven
  source pages, no new location research. Saved the pinned request and scope
  in `private/pdf-restoration/10-batch/` before execution.
- Implementing region-level cache keys, durable outcomes and bounded retries.
  Existing reviewed corrections and raw OCR remain immutable; changed evidence
  must not inherit review automatically. Synthetic failures will exercise
  interruption, isolation and invalidation without expanding the queue.
- The real replay completed all 35 regions (33 OCR jobs and two figures) with
  no failures. Every crop, raw TXT and TSV matches the previous reviewed
  evidence. A SIGINT during a changed-region run left an interrupted ledger;
  resuming completed that region and reused the other 34 results. Separate
  crop and PSM changes each invalidate only one key and require review for
  the pilot, preserving the original corrections and all original cache entries.
- Synthetic checks pass for a killed process, failure isolation, one successful
  retry, a persistent failure stopped at the retry ceiling, corrupt cache/input
  rejection and preserved partial exports. Final repeat-export, effort and
  bulk-readiness records are in progress; no new article has been mapped.

### 2026-09-28 — Step 10 complete: bounded batch and resume gate

- Added `tools/pdf_restore/batch.py` and prepare/resume/export/check Makefile
  targets. Requests pin existing TOC maps, source/queue inputs and optional
  reviewed recipes. Preparation enforces article, distinct-page and lookup
  ceilings, source eligibility and geometry, and refuses existing state paths.
- Cache keys include source hash, region coordinates/kind, page geometry and
  exclusions, pinned engine/model bytes, renderer, Pillow, implementation and
  processing configuration. Completed entries have checked file inventories;
  changed inputs/tools cannot silently alter a prepared plan. Locks serialize
  runners, atomic ledgers preserve every outcome, and atomic cache publication
  prevents incomplete work from becoming a successful cache hit.
- Replayed only `maso-1983-11-toc-0012`, `maso-1988-01-toc-0018` and
  `maso-1991-08-toc-0004`: seven existing mapped pages, 35 regions, 33 OCR jobs
  and two figure crops. All complete without failures. Original crops, raw TXT
  and TSV match exactly. All three `reviewed/` rebuilds are byte-identical to
  the original packages; corrections and original review limits are unchanged.
- Delivered `build/pdf-restoration/10-batch/`: 345 files, 55,221,603 bytes,
  including build-compatible regional OCR bundles, unchanged reviewed packages,
  separate outcomes and a complete manifest. The repeat export is byte-identical.
  A no-op resume takes about 0.6 seconds, makes no engine calls and leaves its
  ledger unchanged. No full-page scratch render enters the export.
- A real SIGINT during diagnostic PSM processing records an interrupted task;
  resume finishes it and reuses the other 34 regions. Separate PSM and crop
  variants each change one cache key, preserving all 35 original cache entries
  including manifest timestamps. Both changed pilot outputs require review and
  omit a reviewed pilot export; their unchanged companion articles retain theirs.
  These are private diagnostic variants, not replacements or new restorations.
- Saved a durable synthetic failure/interruption ledger and partial export.
  The failed region does not prevent two other regions completing; its one
  targeted retry fails and a further retry is rejected. Partial raw output and
  diagnostics remain saved. Ordinary resumes never retry failures automatically.
- All 37 focused PDF tests pass, including nine new batch tests. Coverage
  includes actual child-process SIGKILL, interrupted and post-publication crash
  recovery, successful and exhausted retries, isolated map/config invalidation,
  source/model changes, bounds, locks, corrupt pins/cache, exact review reuse,
  changed-evidence review requirements, exclusions and partial exports.
  The broader `make check` was stopped during its first long-running, unrelated
  CD association artifact audit; no full-suite pass is claimed.
- Measured successful regional work totals 85.6 seconds, including 51.9 seconds
  rendering/cropping and 29.8 seconds in OCR; cache payload is 18,442,581 bytes.
  Mapping/review workload records retain 35 mapped/reviewed regions, 45 reading
  blocks, 111 code lines and fourteen historical lookup pages. This checkpoint
  adds no mapping or proofreading. Historical manual durations are unavailable,
  not zero; future batches must record them prospectively. The prior three-page
  matchstick sample alone needed 31 regions, reinforcing the manual review cost.
- Selected subsequent ceilings: **two articles / six distinct source pages**,
  twenty lookup pages and one targeted retry per failed region. Longer articles
  require segments and a separate article closeout. Documented exact commands,
  request format, failure recovery, review handoff and cache behavior in
  `docs/PDF-RESTORATION.md`.
- Rechecked the useful pilot, all three contrasting sample gates, step 7's
  limited CD correspondence, and steps 8–9's reader records and manifest pins.
  Their source packages, corrections and original reader input pins remain
  unchanged. Saved validation, effort, interruption, invalidation, synthetic
  outcomes and bulk-readiness records under `private/pdf-restoration/10-batch/`.
- Outcome: step 10 complete; **bulk gate passed for bounded named batches**.
  Original sample uncertainties remain visible; no additional article or issue
  coverage is claimed. Stall count 0. Next: `11-batch-01`, name the next November
  TOC identities and mapping targets before execution, within two articles/six
  pages. Reuse the pilot and matchstick sample in November issue accounting.

### 2026-09-28 — 11-batch-01 started: opening articles

- Step 10 is committed as `b7aea42`. Named existing November entries
  `maso-1983-11-toc-0001` (창간사) and `maso-1983-11-toc-0002` (장관 특별면담)
  before mapping. Candidate PDF positions are 13–17, with adjacent pages 12/18
  reserved for boundary lookup; positions and printed folios remain unverified
  until inspected. Saved source/queue/readiness pins and a mapping start time in
  `private/pdf-restoration/11-batch-01/checkpoint-plan.json`.
- Limits remain two articles, six source pages, twenty lookup pages and one
  targeted retry per failed region. Existing pilot and matchstick packages are
  retained for issue accounting; this batch adds no parent/group bodies.

### 2026-09-28 — 11-batch-01 complete: editorial and minister interview

- Restored the two named TOC entries, with five mapped source pages and two
  outside lookup pages. PDF13 contains the complete opening editorial; PDF14–17
  contain the complete interview at visible printed pages 12–15. PDF12 is an
  unrelated advertisement; PDF18 opens a distinct feature. Neither lookup page
  entered OCR or the article packages. No retry or scope expansion was needed.
- The editorial's full printed title includes “기술입국에”, which is absent
  from its shorter canonical TOC label. Preserved the printed reading title and
  original TOC identity separately. PDF13 has no visible folio: its observed
  printed page remains unknown, without promoting the TOC's page 11 to evidence.
  Preserved the publisher portrait, printed byline/role and publication date.
- The interview retains mixed Korean/Hanja, period spelling, speaker labels,
  interview date/place, both photographs and captions. Joined three evidenced
  cross-page/column continuations and preserved all three repeated pull quotes,
  relocating them to avoid breaking continuous sentences. Historical statistics
  and terminology remain as printed rather than being silently repaired.
- The bounded runner completed all 22 regions: nineteen OCR jobs and three
  figure crops, with zero failures/retries. A subsequent resume leaves the
  ledger unchanged. Raw TXT/TSV/settings remain separate from reviewed reading
  text. Saved per-region scan/raw pins and correction decisions in each article's
  `corrections.json`; no original OCR or earlier sample package was overwritten.
- Compared every mapped region and all printed text rows against the scans.
  Both articles are **readable / sample-reviewed**, not fully verified. The
  interview exposes one localized `실시/실지` uncertainty and states the limits
  of Unicode matching for historical Hanja glyph variants. Reflow, spacing and
  quotation placement normalizations remain explicit. The editorial's unknown
  folio is also visible in its scan links and review notes.
- Delivered `build/pdf-restoration/11-batch-01/`: 103 files, 20,530,372 bytes,
  with a two-article index, batch report, portable previews, text/raw-OCR
  downloads, 22 scan regions and separate correction records. There are 63 text
  blocks and three figures, with no invented code/listing download. Original
  unreviewed batch evidence is preserved in `11-batch-01-evidence/`; each
  reviewed article's repeat export is byte-identical in `11-batch-01-repeat/`.
- Validation: all 37 focused PDF tests pass; package/link/hash checks and exact
  regional-character accounting pass. Desktop 1440×1000 and mobile 360×800
  checks confirm all 63 DOM blocks, all three images, repeated quotes, readable
  Hanja, visible gaps and no horizontal page overflow. Twenty-eight browser
  assets match hashes/sizes. Actual index → interview → scan clicks succeed.
  Screenshots are in `output/playwright/pdf-11-batch-01/`. The only initial
  resource error was the local server's missing favicon; article assets pass.
- Recorded mapping elapsed time of 129.7 seconds and transcription/review
  elapsed time of 367.1 seconds, including inspection and artifact preparation.
  Rendering/cropping took 14.5 seconds and OCR 20.9 seconds. These are observed
  batch measurements, not a forecast of new-article throughput. Retained the
  two-article/six-page ceilings and twenty-page lookup/one-retry limits.
- Started a separate November issue ledger without changing the historical
  queue: 47 entries reconcile to four classified, readable/sample-reviewed
  articles (including the pilot and matchsticks), one evidenced group heading
  and 42 unresolved eligibility decisions. Those 42 are not counted as failed
  or missing articles. Saved a batch snapshot and the current issue ledger in
  `private/pdf-restoration/11-november/issue-progress.json`.
- Saved mapping, OCR, review timing, package validation, browser, issue snapshot
  and pinned closeout records under `private/pdf-restoration/11-batch-01/`.
  Local preview: `http://127.0.0.1:4179/`. Outcome: batch complete; November issue
  remains in progress. Stall count 0. Next: name `11-batch-02` within the same
  limits; issue-wide reader export/inspection remains the separate closeout.

### 2026-09-28 — 11-batch-02 started: two further game articles

- Batch 01 is committed as `b3da519`. Named `maso-1983-11-toc-0014`
  (ENEMY SATELLITE) and `maso-1983-11-toc-0015` (REVERSE), following the
  completed pilot and matchstick sample within the evidenced 취미생활 group.
  Saved the current issue ledger, input pins and mapping start time before
  inspecting candidate PDF35–37 and boundary lookup pages 34/38.
- Scope remains two articles, six source pages, twenty lookup pages and one
  targeted retry per failed region. Printed numbering and extent will be
  established locally; no parent body or new TOC entry will be introduced.
- Mapping confirmed three source pages: ENEMY SATELLITE at PDF35 / printed33,
  REVERSE at PDF36–37 / printed34–35. PDF34/38 were boundary lookups only.
  Explicitly excluded the unrelated academy advertisement below REVERSE.
- All 27 regions completed (24 OCR regions, three figures), with no retries.
  Reviewed every printed text row and figure; saved separate raw evidence,
  regional transcriptions and `corrections.json`. The reviewed packages contain
  37 blocks, including three code blocks and five separately preserved inline
  listing annotations. Faint operators and code spacing remain explicit limits.
- All 37 focused PDF tests pass. Both reviewed package rebuilds are byte-identical;
  package hashes, local links, literal listing downloads, raw OCR preservation
  and non-whitespace transcription accounting pass. Browser acceptance and
  November ledger reconciliation remain in progress.

### 2026-09-28 — 11-batch-02 complete: ENEMY SATELLITE and REVERSE

- Completed both named articles as **readable / sample-reviewed**, within the
  two-article/six-page ceilings. Used three mapped pages and two boundary lookup
  pages; no failed region, OCR retry or scope expansion. Their existing parent
  remains an evidenced group heading without an invented article body.
- ENEMY SATELLITE preserves its illustration, introduction, complete explanation
  and listing. Recovered a prose row omitted by OCR directly from the crop.
  Separated five dotted-leader annotations from BASIC, retaining their text and
  line associations in the reading package and correction evidence. Marked
  faint `=/−` operators and one localized prose reading uncertainty explicitly.
  Preserved the anomalous extra A, R and S characters and physical code wraps.
- REVERSE preserves its provider credit, award note, both figures/captions,
  complete explanation and two listing columns. Joined the evidenced continuations
  across columns/pages. Retained printed `A(R)>0`, `;:` and trailing colon forms,
  plus discrepancies between prose and code. Its lower-page advertisement is
  explicitly excluded. Exact code spacing, border-star counts and historical
  glyph correspondence remain unverified; neither program was repaired or run.
- Delivered `build/pdf-restoration/11-batch-02/`: 125 files, 11,842,040 bytes,
  including an index, report, two portable previews, three figures, 27 scan
  regions and separate text/listing/raw-OCR downloads and correction records.
  Original unreviewed evidence remains in `11-batch-02-evidence/`; deterministic
  reviewed rebuilds remain in `11-batch-02-repeat/`. No prior package changed.
- Validation: all 37 focused PDF tests pass. Both rebuilds are byte-identical;
  package/link/hash checks, raw preservation and complete transcription accounting
  pass. A no-op batch resume leaves its ledger unchanged. Browser checks at
  1440×1000 and 360×800 confirm all 37 DOM blocks, three images, visible review
  limits and no page overflow; code scrolls within its container. All 35 fetched
  assets match their pins. Actual index → article, listing download and scan
  clicks succeed; the downloaded listing matches the package byte for byte.
  Screenshots are in `output/playwright/pdf-11-batch-02/`.
- Browser setup initially raced server startup; navigation succeeded after the
  server started. A stalled sandboxed Playwright call succeeded after escalation.
  The only subsequent resource error was the local server's missing favicon;
  article assets pass. No full-repository check is claimed for this data-only
  batch; no application or extraction-tool code changed.
- Observed mapping elapsed time: 240.5 seconds. Transcription/review and correction
  preparation: 205.3 seconds. Cached processing totals: 10.4 seconds rendering/
  cropping and 11.5 seconds OCR. These are bounded batch observations, not proof
  of character-perfect code or a forecast of whole-issue throughput.
- Updated `private/pdf-restoration/11-november/issue-progress.json` and saved a
  pinned batch snapshot: 47 entries reconcile to six readable/sample-reviewed
  articles, one group heading and 40 unresolved eligibility decisions. Those 40
  are not failed or missing articles. Preserved all four prior article manifests.
- Saved mapping, OCR, timing, package/browser validation and closeout records
  under `private/pdf-restoration/11-batch-02/`. Preview:
  `http://127.0.0.1:4180/`. Outcome: batch complete; November issue in progress.
  Stall count 0. Next: name `11-batch-03` before mapping within the same limits;
  issue-wide reader staging and coverage reconciliation remain the later closeout.

### 2026-09-28 — 11-batch-03 started: 원

- Batch 02 is committed as `3aee759`. Named `maso-1983-11-toc-0016` (원)
  before mapping candidate PDF38–39, with boundary lookups PDF37/40. Saved the
  current issue ledger, input pins and mapping start time in the private batch.
- This batch admits one article within the two-article/six-page ceilings, with
  twenty lookup pages and one targeted retry per failed region. The next entry,
  잠수함, has a possible eight-page span from TOC candidates; its actual extent
  and a suitably bounded checkpoint will be determined separately. No article
  failure or missing pages are inferred from those candidates.
- Confirmed PDF38–39 / printed36–37 as the complete article, with PDF37/40
  serving only as boundary lookups. Mapped 23 regions: 22 text/code regions
  and one illustration. All OCR tasks completed without engine failure.
- Widened r08's right crop edge after review, preserving the initial map, state
  and evidence export. `map-reviewed.json`, `request-reviewed.json` and
  `state-reviewed/` are the final mapping inputs. Only r08 was reprocessed;
  the other 22 region payloads were reused byte for byte.
- Reviewed every printed row. Preserved three-column reading order, both formulas,
  repeated title, five listing captions and all physical code wraps. The new
  `corrections.json` includes 13 selected before/after OCR examples and verified
  byte ranges for five independent listings in `listing.txt`. Code precision
  limits and one prose uncertainty remain visible.
- All 37 focused tests, package/link/hash checks, raw preservation, transcription
  accounting, five listing ranges and the byte-identical rebuild pass. Browser
  acceptance and issue-ledger reconciliation are next.

### 2026-09-28 — 11-batch-03 complete: 원

- Restored the single named article as **readable / sample-reviewed**, using two
  source pages and two boundary lookups. All 23 regions are represented: three
  prose columns, both formulas, one illustration, both occurrences of the title,
  provider/platform text and five captioned BASIC listings. No TOC entry or
  parent body was invented; no neighboring article or advertisement was included.
- Preserved original map/state/evidence and the separate reviewed map revision.
  The r08 crop adjustment processed one changed region and reused the other 22
  payloads unchanged. No OCR engine retry or failed task was needed. Empty OCR
  results for both white-on-dark titles were recovered directly from the scans.
- `corrections.json` now includes 13 selected raw/reviewed excerpts with scan
  evidence, plus a `listing_index` giving each independent listing's caption,
  block/region identity and exact UTF-8 byte range in `listing.txt`. These examples
  supplement the full reviewed blocks; they are not an exhaustive edit diff.
  Five byte ranges were checked against the exported listing and browser fetch.
- Retained physical code wraps, including split `180`, `X1` and `Y1` tokens;
  the five listings are separate programs, not one executable file. Preserved
  prose `SQRT` versus printed code `SQR`, listing 4's endpoint `X0`, and spaced
  `> =` operators. Exact spacing and 0/O/1/I glyph correspondence remain
  unverified. One localized 여태/어태 prose uncertainty is visibly marked.
  No historical algorithm, prose claim or program was repaired or executed.
- Delivered `build/pdf-restoration/11-batch-03/`: 104 files, 9,617,434 bytes,
  including the batch index/report, portable article, 37 blocks, five code
  blocks, one figure, scan regions and separate correction/raw-OCR/text/listing
  artifacts. Final raw evidence is in `11-batch-03-evidence-reviewed/`; the
  initial evidence remains in `11-batch-03-evidence/`. The repeat reviewed export
  in `11-batch-03-repeat/` is byte-identical.
- All 37 focused PDF tests pass. Package hashes/links, original raw bytes,
  unaffected cached payloads, complete transcription accounting and listing
  ranges pass. A no-op resume leaves the reviewed ledger unchanged. Desktop
  1440×1000 and mobile 360×800 checks confirm exact text for all 37 DOM blocks,
  both formulas, image readiness, all five code blocks and no page overflow.
  All 27 fetched assets match their pins. Actual index → article, listing
  download and widened-scan clicks succeed. The downloaded listing is identical.
  Screenshots are in `output/playwright/pdf-11-batch-03/`; the only console
  resource error was the local server's missing favicon.
- Observed initial mapping: 67.2 seconds; transcription/review and correction
  preparation, including the crop adjustment: 271.4 seconds. Initial regional
  processing took 7.5 seconds rendering/cropping and 9.5 seconds OCR. The reviewed
  plan reused 22 cached regions and ran only r08; its cached timing totals are
  not additional full-batch processing. Measurements do not establish exact code
  transcription or predict whole-issue throughput.
- Reconciled all 47 November entries: seven restored/sample-reviewed articles,
  one group heading and 39 unresolved eligibility decisions. Preserved the six
  prior article manifests. Saved the updated issue ledger, batch snapshot,
  validation and pinned closeout records under the private batch directory.
- Updated the plan and workflow documentation; no application/extraction code
  changed. Preview: `http://127.0.0.1:4181/`. Batch complete; issue in progress;
  stall count 0. Next: `11-batch-04`, first establishing 잠수함's actual extent.
  If it exceeds six source pages, define bounded mapping/segment checkpoints
  before extraction, retaining one article identity and explicit partial coverage
  until assembly. Do not silently raise the source-page ceiling.

### 2026-09-28 — 11-batch-04 started: 잠수함 extent and admission

- Batch 03 is committed as `7ed61b5`. Named `maso-1983-11-toc-0017`
  (잠수함) and saved the current issue ledger, source/queue pins and start time.
  Its TOC candidates suggest printed38–45; this is not yet an observed extent.
- Boundary preflight is limited to candidate PDF39–48, within twenty lookup
  pages. Admit extraction only after checking the six-source-page ceiling.
  If larger, define bounded segment checkpoints with one article identity and
  explicit partial coverage before extraction. Keep the existing limits.
- Preflight confirms eight article pages, PDF40–47 / printed38–45; PDF39 ends
  원 and PDF48 starts 체커. No intervening advertisements. PDF42 / printed40
  renders upside down and requires a separate evidenced orientation correction.
- Before extraction, saved `extent-and-segments.json`: this checkpoint covers
  PDF40–41 only (introduction/images and listing90–486); the continuation covers
  PDF42–47 after orientation support is validated, followed by aggregation with
  no new extraction. Keep one TOC/article identity. The opening export will be
  explicitly partial, not counted as a complete readable article.
- The admitted two-page segment completed all 14 regions (eleven OCR regions,
  three figures), with zero engine failures/retries. Reviewed every included
  printed row and all figures. Saved separate raw OCR, transcription and
  `corrections.json`, with ten selected correction examples, two listing byte
  ranges and fourteen unresolved graphics-string occurrences linked to scans.
- Built the opening article as **partial / sample-reviewed**. Coverage records
  distinguish included PDF40–41 from deferred PDF42–47; no absent source pages
  are claimed. Graphic placeholders, uncertain music digits/case, code spacing
  and printed discrepancies remain explicit; no character codes were invented.
- All 37 focused tests and the byte-identical rebuild pass. Package/link/hash
  checks, all-region coverage, raw preservation, transcription accounting,
  two listing ranges and fourteen graphics occurrences pass. Browser checks
  and issue-ledger reconciliation remain in progress.

### 2026-09-28 — 11-batch-04 complete: 잠수함 opening segment

- Completed the bounded opening checkpoint; the article remains **partial /
  sample-reviewed**. Preflight inspected ten pages and confirmed the full article
  at PDF40–47 / printed38–45. Only PDF40–41 entered extraction; eight other pages
  were lookups. No source-page ceiling was raised and no additional TOC identity
  was introduced. The saved segment plan separates the two-page opening,
  six-page continuation and later aggregation without new extraction.
- Preserved all opening prose, the provider/award note, repeated title, naval
  illustration and two complete screen figures. Joined the evidenced column
  continuation. Included every printed code row from 90 through 486, retaining
  physical wraps and anomalous printed forms. The continuation begins at 490;
  its six observed pages are deferred, not missing from the source.
- `corrections.json` contains ten selected OCR correction examples, two verified
  UTF-8 listing ranges, explicit included/deferred coverage, and fourteen
  `unresolved_graphics` occurrences. Each graphics marker identifies its printed
  line and pinned scan region; encoded bytes and character counts remain null.
  The markers represent individual occurrences or whole strings as stated and
  do not imply that similar shapes share a character code.
- Kept the body/listing discrepancies, uncertain w/W and 6100/8100 readings,
  `=>` ordering, quote layout and code-spacing limits visible. No historical
  program or algorithm was repaired or executed. Code containing editorial
  graphics markers is explicitly described as an incomplete transcription.
- Delivered `build/pdf-restoration/11-batch-04/`: 62 files, 9,690,187 bytes,
  with index/report, partial article preview, 17 blocks (two code blocks), three
  figures, fourteen scan regions and correction/raw-OCR/text/listing artifacts.
  Original unreviewed evidence is in `11-batch-04-evidence/`; the reviewed repeat
  export in `11-batch-04-repeat/` is byte-identical.
- All 37 focused tests pass. Package/link/hash checks, raw preservation, complete
  included-region accounting, transcription accounting, listing ranges and
  graphics-marker references pass. A no-op resume leaves the ledger unchanged.
  Browser checks at 1440×1000 and 360×800 verify all 17 DOM blocks, three images,
  visible partial/deferred coverage and contained code scrolling. All 18 fetched
  assets match their pins. Actual index → article, listing download and scan
  clicks succeed; downloaded listing bytes match. Screenshots are under
  `output/playwright/pdf-11-batch-04/`. Only the local favicon request returned 404.
- Observed mapping/preflight preparation: 133.3 seconds. Opening transcription,
  review and correction preparation: 188.9 seconds. Rendering/cropping took
  7.1 seconds and OCR 6.2 seconds. No OCR failures/retries. These measurements
  exclude restoration of the deferred six pages and do not certify exact code.
- The November ledger now reconciles 47 entries to eight classified articles
  (seven readable, one partial), one group heading and 38 unresolved eligibility
  decisions. All eight have sample-review records limited to their stated
  coverage. Preserved all seven previous article manifests and source pins.
  Saved the updated ledger snapshot, validation and pinned closeout records.
- Preview: `http://127.0.0.1:4182/`. Checkpoint complete; article and issue still
  in progress; stall count 0. No application/extraction code changed here.
  Next is the separately bounded `11-orientation-repair`: qualify a 180-degree
  image correction for PDF42 without altering its source rotation metadata (0).
  Saved its one-real-page limit and acceptance criteria in `next-checkpoint.json`.
  Commit that repair before `11-batch-05` processes PDF42–47; reserve r15+ region
  identities and preserve this opening package until the assembly checkpoint.

### 2026-09-28 — 11-orientation-repair started

- Opening checkpoint is committed as `755edff`. Begin the saved one-real-page
  repair for PDF42, with synthetic checks for transforms, crops, masking, cache
  invalidation and provenance. Preserve source geometry and prior packages.
- Recorded the owner's authorization to defer old bitmap-character correction
  to manual post-production. Keep occurrence markers and scan evidence in
  `corrections.json`; pending glyph correction will not block extraction and is
  tracked separately from the six deferred continuation pages.
- Added optional evidenced clockwise orientation correction while retaining
  original inventory geometry. Both OCR paths transpose before masking/cropping;
  transforms, settings, image evidence and cache dependencies track it. Export
  rejects mismatched image/OCR orientation provenance.
- All 42 focused tests pass. Real qualification on PDF42 completed four sample
  crops with zero failures/retries; standalone and batch pixels match. Inspected
  upright repeated title, folio40 and listing boundaries490–1817. Raw OCR errors
  remain untouched and no reviewed continuation package is claimed.

### 2026-09-28 — 11-orientation-repair complete

- Implemented explicit page-level `orientation_correction`, accepting evidenced
  clockwise 90/180/270 corrections independently of immutable PDF rotation.
  Omission retains legacy behavior. PDF-to-upright transforms compose both
  rotations; masks and crop/TSV coordinates use corrected raster geometry.
  Both render paths use a pixel transpose without resampling.
- Correction records are pinned through maps, page evidence, OCR settings and
  batch dependencies. Publication checks image and OCR provenance. Synthetic
  checks prove all rotation compositions, invalid-input rejection, masking/crop
  behavior and selective invalidation with unchanged-page cache reuse.
- Qualified only PDF42 / printed40, within the one-real-page limit. Its source
  metadata remains rotation 0; the separate correction is 180. Four OCR samples
  completed without failures or retries: title, initial rows, final rows and
  folio. Visual review confirms the upright title and listing 490–1817. Batch and
  standalone crops match pixel for pixel. These are qualification windows, not
  the full continuation map or approved transcription. No bitmap codes inferred.
- Saved plan, preservation pins, map, runner state/cache, original and corrected
  render evidence, orientation review, validation and next-checkpoint records
  in `private/pdf-restoration/11-orientation-repair/`. Unreviewed batch output is
  in `build/pdf-restoration/11-orientation-repair-evidence/`.
- All 42 focused tests, export integrity and no-op resume pass. All eight prior
  November packages pass integrity checks; the opening package rebuild is
  byte-identical. Source, inventory, issue ledger and prior opening evidence
  remain unchanged. November still has seven readable articles, one partial,
  one group heading and 38 unresolved eligibility decisions.
- Updated the plan and workflow documentation with the owner's manual bitmap
  correction decision. Keep scan-linked occurrence markers in `corrections.json`
  and distinguish deferred glyph corrections from pending page coverage.
  Existing runner states retain their old implementation pins; new work uses
  fresh states. Checkpoint complete; stall count 0. Next: `11-batch-05`, restoring
  PDF42–47 within six pages, r15+ region IDs and the same article identity,
  followed by separate assembly without new extraction.

### 2026-09-28 — 11-batch-05 started: 잠수함 continuation

- Orientation repair is committed as `0387789`. Admitted the saved six-page
  continuation, PDF42–47 / printed40–45, under the existing article identity.
  Saved input pins, the issue-ledger snapshot and prior-package preservation
  pins before mapping. Use r15+ region IDs and the qualified correction on PDF42.
- Bitmap character decoding remains deferred to the owner's manual pass. Keep
  raw OCR, scan-linked markers, reviewed text and remaining uncertainties in
  separate correction evidence. The continuation stays partial until assembly.
- Initial OCR completed all 21 regions without engine failures. Crop review
  prompted one map revision: widen code margins and move three splits away from
  rows1000,5500,10160. Kept the initial map/state/export; a fresh state reused six
  title tasks and regenerated fifteen changed code crops. No engine retry used.
- Compared all included printed rows and boundaries. Saved 21 transcription
  blocks (15 code), 20 selected OCR correction examples, 90 unresolved graphics
  occurrences and an index of 38 printed character definitions. Preserved
  repeated &H96, &H97 and &H87 definitions and unusual printed forms.
- Built the continuation as partial/sample-reviewed. The opening remains in its
  original package; assembly is pending. Package, browser and ledger validation
  are in progress.

### 2026-09-28 — 11-batch-05 complete: 잠수함 continuation

- Completed PDF42–47 / printed40–45 within the six-source-page ceiling, with
  zero outside lookup pages. Retained the same article/TOC identity and used
  r15–r35; opening r01–r14 remain untouched. PDF42 has the qualified separate
  180-degree correction, with original rotation metadata 0 preserved.
- Preserved all included printed rows from 490 through 11360, including physical
  wraps, six repeated titles, character definitions and final screen strings.
  The package contains 21 blocks, 15 code blocks and 344 numbered rows. It remains
  **partial/sample-reviewed** until the opening and continuation are assembled.
  All eight source pages now have segment evidence; no missing page is claimed.
- `corrections.json` retains 20 selected OCR correction examples, 15 verified
  UTF-8 listing ranges and 90 unresolved graphics occurrences. Every marker links
  its printed line, region and pinned scan; encoded bytes and character counts
  remain null. Manual bitmap correction is deferred to the owner and does not
  block this extraction checkpoint.
- Added `glyph_definitions`: 38 printed definitions with declared code, printed
  line, scan pin and exact listing byte range. Preserved repeated &H96, &H97 and
  &H87 definitions, including the differing 129/127 operands. The index does not
  decode bitmaps or associate definitions with graphics markers. Retained the
  unusual printed comparisons, variable names, punctuation and quote layout;
  exact spacing, music strings and faint direction symbols remain unverified.
  No program execution or semantic repair was performed.
- One map revision widened code margins and moved three splits off printed
  rows. Initial 21-task evidence stays intact; the new state reused six title
  tasks and processed fifteen revised code regions. Both states resume without
  modifying their ledgers. No engine failures or retries occurred.
- Delivered `build/pdf-restoration/11-batch-05/`: 99 files, 24,031,393 bytes,
  including the index/report, continuation preview, 21 scan regions, raw OCR,
  correction record, text and listing. Original and revised unreviewed evidence
  remain in `11-batch-05-evidence/` and `11-batch-05-evidence-reviewed/`; the
  reviewed export in `11-batch-05-repeat/` is byte-identical.
- All 42 focused tests pass. Package/link/hash checks, raw preservation, exact
  regional transcription accounting, all 15 listing ranges, 90 graphics markers,
  38 definition ranges and orientation provenance pass. Prior eight article
  packages and original source/queue/TOC pins remain unchanged.
- Playwright checks at 1440×1000 and 360×800 pass: all 21 DOM blocks, visible partial
  scope, 25 fetched asset pins, all correction indexes and contained code scrolling.
  Actual index→article, listing download and scan clicks succeed; downloaded
  listing bytes match. Screenshots are under `output/playwright/pdf-11-batch-05/`.
  Only the local favicon returned 404. A stalled script invocation was cancelled
  before browser traffic and rerun successfully with the approved wrapper.
- Observed mapping took 67.0 seconds. Crop revision, transcription and correction
  preparation took 550.5 seconds, including the revised-crop processing wait.
  Initial render/crop and OCR timings were 15.0s/14.3s; the revised state's cached
  task timings are 25.6s/14.3s and include reused title tasks. These are local
  observations, not exact-code verification or whole-issue throughput estimates.
- November remains 47 entries: eight classified articles (seven readable, one
  partial), one group heading and 38 unresolved eligibility decisions. Added the
  continuation segment to the existing article record, preserving the opening
  directory/manifest and explicitly marking assembly pending. No new article
  or readable completion was counted. Saved ledger snapshot and pinned closeout.
- Preview: `http://127.0.0.1:4183/`. Checkpoint complete; stall count 0. No
  application/extraction code changed. Next: `11-submarine-assemble`, one article
  with no new source-page extraction or OCR. Preserve both segments' original
  maps/settings and review evidence; validate 35 regions, 38 blocks, three figures,
  17 listing ranges, 104 graphics occurrences and 38 definition entries under one
  article identity. Add bounded assembly support if needed instead of changing
  historical OCR provenance to claim a different map.

### 2026-09-28 — 11-submarine-assemble started

- Continuation checkpoint is committed as `eb59917`. Pinned both segment
  manifests/recipes, prior article packages, source inventory and issue ledger.
  The checkpoint permits one article, zero new source-page extraction and zero
  OCR tasks. Expected union: eight pages,35 regions,38 blocks and three figures.
- Add a separate assembly path because original OCR settings refer to distinct
  maps. Preserve the input packages byte for byte, validate their identity and
  disjoint coverage, then combine reading content and correction indexes.
  Manual bitmap correction remains deferred and visible.

### 2026-09-28 — 11-submarine-assemble complete

- Combined the reviewed opening and continuation under the existing
  `maso-1983-11-toc-0017` identity. The article now covers PDF40–47 / printed38–45:
  35 regions, 38 blocks, 17 code blocks and three figures. Availability is
  **readable/sample-reviewed**, with explicit character-accuracy limits.
  No new source pages were extracted and no OCR tasks were run.
- Added `tools.pdf_restore.assemble` and `make assemble-pdf-article`. The recipe
  pins ordered input manifests and expected pages. Assembly rejects mismatched
  identities, overlapping pages/regions, incomplete regional review, changed
  OCR provenance and incorrect listing/definition offsets before publication.
  The existing article checker independently reconstructs the combined map,
  correction indexes, downloads and preview from retained segments.
- Preserved every original package file under `segments/opening/` and
  `segments/continuation/`. Original maps, settings, raw OCR, scans and review
  records are unchanged. PDF42 retains its evidenced 180-degree image correction
  and original rotation metadata 0. The new union map is not substituted into
  historical OCR settings. All 647 pinned prior input files remain unchanged.
- The combined listing is exactly the original opening bytes followed by the
  original continuation bytes. `corrections.json` retains 30 selected correction
  examples, 17 listing ranges, 104 unresolved graphics occurrences and 38 printed
  glyph definitions. Scan paths and UTF-8 offsets are explicitly rebased with
  source-segment identities. Only four superseded scope/orientation notes are
  resolved; original notes remain in the preserved segment packages.
- Bitmap codes/counts remain unresolved, repeated definitions and printed
  anomalies remain intact, and the owner will perform later manual correction.
  Full page coverage does not mean character-perfect or executable code.
  No historical program execution, bitmap inference or semantic repair occurred.
- Delivered `build/pdf-restoration/11-submarine-assemble/`: 168 files,
  50,505,064 bytes including index/report and the article package. The article
  alone has 164 files / 50,469,596 bytes; retained original exports account for
  part of that size. A separate assembly rebuild is byte-identical.
- All 48 focused PDF tests pass, including six new assembly tests covering
  preservation, deterministic output, invalid coverage/identity/provenance,
  UTF-8 indexes and tampering even after outer-manifest rehashing. Source/TOC,
  package/link/hash, raw archive and correction-index checks pass.
- Playwright checks at 1440×1000 and 360×800 pass: 38 exact DOM blocks, three
  loaded figures, 39 fetched asset pins, every correction index and contained
  code scrolling. Actual index→article, listing-download and last-scan clicks
  succeed; downloaded listing bytes match. Inspected desktop, figure and mobile
  screenshots under `output/playwright/pdf-11-submarine-assemble/`. Local server
  binding required sandbox escalation; one stalled sandboxed script invocation
  was cancelled before traffic and passed on an escalated rerun.
- Updated November's ledger to eight readable/sample-reviewed articles, zero
  partial articles, one group heading and 38 unresolved eligibility decisions
  across 47 entries. The primary restoration now references the assembly;
  original segment records remain unchanged. Saved before/after snapshots,
  validation, browser acceptance, pinned closeout and next-checkpoint inputs.
- Checkpoint complete; stall count 0. Preview: `http://127.0.0.1:4184/`.
  Next: `11-batch-06`, establish 체커's boundaries from the observed PDF48 opening
  and TOC printed46 start, then restore within one article / six source pages.
  Its ending is not yet verified; allow at most six outside lookup pages and
  one targeted retry per failed region. Keep 잠수함's manual glyph work deferred.

### 2026-09-28 — 11-batch-06 started

- Assembly checkpoint is committed as `bb5b759`. Pinned source/TOC/inventory,
  runtime, issue ledger and previous exports before new work.
- Target: 체커 (`maso-1983-11-toc-0018`), with one article / six source pages,
  at most six outside lookup pages and one targeted retry per failed region.
  Inspect PDF48 onward and the next TOC boundary before determining the map;
  split the article if its observed extent exceeds the page ceiling.
- Preserve raw OCR and literal printed code, use scan-linked correction records,
  and keep unknown glyph bytes/counts explicit. Manual bitmap correction remains
  deferred; no historical program execution or semantic repair is planned.

- Boundary inspection confirms PDF48–51 / printed46–49; PDF52 starts AWARI.
  Mapped 17 regions: six figures and eleven text/code regions. Two crop revisions
  preserve the complete illustrated header and move listing splits into whitespace.
  Original, first-review and final maps/states/exports remain available; unchanged
  tasks were reused, with no engine failures or retry attempts.
- Prepared nine reading blocks, including one joined three-column body and four
  code blocks containing 73 numbered rows. `corrections.json` records 17 selected
  OCR corrections, four listing ranges, 73 per-line ranges and twelve printed
  anomalies. All six figures remain in source order, including the game boards
  that continue across printed page/column boundaries. Package validation and
  desktop/mobile browser review are in progress; issue counts are unchanged.

### 2026-09-28 — 11-batch-06 complete

- Restored 체커 (`maso-1983-11-toc-0018`) across PDF48–51 / printed46–49.
  PDF52 opens AWARI and was the only outside lookup page. Full article coverage
  fits the saved one-article/six-page limit; no segment assembly is required.
- Delivered **readable/sample-reviewed** content: 17 regions, nine blocks,
  four code blocks and six figures. Joined the three prose columns with explicit
  scan references, including the sentence crossing from the second to third
  column. Preserved the complete illustrated header, instruction screen and
  four gameplay columns in source order. Two boards continue across printed
  page/column boundaries; no rows were invented or images composited.
- The listing preserves 73 numbered rows, 10–1880, and physical wraps inside
  strings, expressions and numeric targets. `corrections.json` contains 17
  selected OCR correction examples, four block ranges, 73 `listing_line_index`
  entries and twelve `listing_anomalies`, with scan pins and UTF-8 byte offsets.
  `figure_sequence` records board continuations. Exact whitespace, ambiguous
  glyphs and faint punctuation remain unverified. No historical execution,
  syntax repair or program-logic repair was performed. No custom bitmap markers
  were identified in this listing; gameplay screens remain raster evidence.
- Retained original map/state/export and both crop revisions. The first revision
  completed the illustrated header, recovered a wrapped code row and adjusted
  right-column bounds: four regions processed, thirteen reused. The final split
  adjustment moved six pixels into whitespace: two processed, fifteen reused.
  Final inputs are `map-final.json` and `state-final/`. All three states resume
  without changing their ledgers; there were zero engine failures or retries.
- Exported `build/pdf-restoration/11-batch-06/`: 65 files / 16,338,741 bytes,
  including index/report and the article package (61 files / 16,320,406 bytes).
  The separate reviewed rebuild is byte-identical. Saved unreviewed evidence in
  the original, reviewed and final evidence exports, plus mapping/crop review,
  regional transcription, validation, ledger snapshots and pinned closeout.
- All 48 focused PDF tests pass. Package/link/hash checks, exact raw-byte
  preservation, complete regional coverage, joined prose, figure order, all
  listing/line/anomaly ranges and selected correction excerpts pass. All 815
  pinned prior input files remain unchanged, including the submarine assembly.
- Playwright checks at 1440×1000 and 360×800 pass: all nine DOM blocks match,
  all six figures load in order, all 21 fetched asset pins match, and code
  scrolling stays within its container. Actual index→article, listing download
  and final scan clicks pass; downloaded listing bytes match. Inspected prose
  and mobile screenshots under `output/playwright/pdf-11-batch-06/`. Only the
  local favicon returned 404. Local server/browser acceptance used approved
  sandbox escalation. No application or extraction code changes were required.
- Observed mapping took 76.2 seconds; crop review, transcription and correction
  preparation took 341.2 seconds, including revised-crop processing waits.
  Initial render/crop and OCR timings were 11.0s/6.5s. Final cached task timings
  were 16.3s/6.5s and include reused tasks; they are not a second full-pass cost
  or a claim of exact-code verification or whole-issue throughput.
- November now has nine readable/sample-reviewed articles, one group heading
  and 37 unresolved eligibility decisions across 47 entries. Only 체커's entry
  changed; prior restorations and deferred submarine bitmap work remain intact.
- Checkpoint complete; stall count 0. Preview: `http://127.0.0.1:4185/`.
  Next: `11-batch-07`, AWARI (`maso-1983-11-toc-0019`). Reuse the observed PDF52 /
  printed50 opening, verify the ending before mapping, and stay within one
  article, six source pages and six outside lookup pages. The next TOC item
  begins at printed53; its actual source boundary is not yet verified.

### 2026-09-28 — 11-batch-07 started

- 체커 is committed as `d94358b`. Pinned source/TOC/inventory, runtime,
  issue ledger and prior exports. Target: AWARI (`maso-1983-11-toc-0019`).
- Reuse the observed PDF52 / printed50 opening and verify the ending before
  mapping. Limits: one article, six source pages, six outside lookup pages and
  one targeted retry per failed region. Retain raw OCR, scan-linked corrections,
  figures and literal code with visible uncertainty; no historical execution
  or semantic repair. Update issue accounting only after validation.

- Confirmed PDF52–54 / printed50–52; PDF55 opens the next article and is the
  only outside lookup page. Mapped 17 regions, including six figures and three
  code regions. A preparation-time unsupported heading kind was rejected before
  OCR and corrected to `section-label`; the empty lock-only state is preserved.
- Crop review widened listing margins, added paragraph whitespace and trimmed
  the photograph's narrow lower border to exclude adjacent text. Original and
  revised maps/states/exports remain available; unchanged tasks were reused.
  Prepared ten blocks, 69 numbered code rows, 18 selected OCR corrections,
  three listing ranges, per-line offsets, twelve code review notes and three
  prose review notes. Joined the explanation across PDF52 and PDF54 with both
  source references intact. Validation is underway; issue counts are unchanged.

### 2026-09-28 — 11-batch-07 complete

- Restored AWARI (`maso-1983-11-toc-0019`) across PDF52–54 / printed50–52.
  PDF55 opens the next article and was the only outside lookup page. Complete
  coverage fits the saved one-article/six-page limit; no assembly is required.
- Delivered **readable/sample-reviewed** content: 17 regions, ten blocks,
  three code blocks and six figures. Joined the explanation across PDF52 and
  PDF54, retaining regional transcripts, both scan references and a documented
  `prose_joins` record. The photograph, board diagram, robot illustration and
  three numbered gameplay panels remain in source order. `figure_sequence`
  records panel ranges ①–⑥, ⑦–⑫ and ⑬–⑯.
- The listing preserves 69 numbered rows, 5–999, and physical code wraps.
  `corrections.json` contains 18 selected OCR corrections, three block ranges,
  69 `listing_line_index` entries, twelve `listing_anomalies` and three
  `text_review_items`, with scan pins and UTF-8 offsets. Printed spellings,
  unusual expressions and final prose counts remain as observed. Exact blank
  widths, ambiguous glyphs and punctuation remain unverified. No historical
  execution or semantic repair occurred. No custom bitmap markers were
  identified; gameplay screenshots remain raster evidence.
- Retained original and revised maps/states/evidence exports. The first crop
  revision processed four regions and reused thirteen. The final photograph
  border adjustment processed one figure and reused sixteen regions, including
  all OCR results. Final inputs are `map-final.json` and `state-final/`.
  All three completed states resume without changing their ledgers; there were
  zero engine failures or retries. The preparation-time region-kind rejection
  is separately recorded and its empty lock-only state is retained.
- Exported `build/pdf-restoration/11-batch-07/`: 65 files / 13,912,077 bytes,
  including the wrapper/report and article package (61 files / 13,893,668 bytes).
  A separate reviewed rebuild is byte-identical. Saved mapping/crop review,
  regional transcription, validation, ledger snapshots and pinned closeout.
- All 48 focused PDF tests pass. Package/link/hash checks, exact raw-byte
  preservation, complete regional coverage, joined prose, figure order and all
  correction/listing offsets pass. All 880 pinned prior input files remain
  unchanged, including prior restorations and the submarine assembly.
- Playwright checks at 1440×1000 and 360×800 pass: all ten DOM blocks match,
  all six figures load in order, all 21 fetched asset pins match, and code
  scrolling stays within its container. Actual index→article, listing download
  and final scan clicks pass; downloaded listing bytes match. Inspected prose
  and mobile screenshots under `output/playwright/pdf-11-batch-07/`. Only the
  local favicon returned 404. Local server/browser acceptance used approved
  sandbox escalation. No application or extraction code changes were required.
- Observed mapping took 134.0 seconds; crop review, transcription and correction
  preparation took 415.5 seconds, including processing waits. Initial
  render/crop and OCR timings were 8.96s/8.95s. Final cached task timings were
  13.37s/8.97s and include reused tasks; they are not a second full-pass cost
  or a claim of exact-code verification or whole-issue throughput.
- November now has ten readable/sample-reviewed articles, one group heading
  and 36 unresolved eligibility decisions across 47 entries. Only AWARI's
  entry changed; prior restorations and deferred bitmap work remain intact.
- Checkpoint complete; stall count 0. Preview: `http://127.0.0.1:4186/`.
  Next: `11-batch-08`, 당신의 심장을 진단해 드립니다
  (`maso-1983-11-toc-0020`). Reuse the observed PDF55 / printed53 opening, verify
  the ending before mapping, and stay within one article, six source pages and
  six outside lookup pages. The next TOC item begins at printed56; its actual
  source boundary is not yet verified.

### 2026-09-28 — 11-batch-08 started

- AWARI is committed as `8f3ab7e`. Target: 당신의 심장을 진단해 드립니다
  (`maso-1983-11-toc-0020`). Pin source, TOC, inventory, runtime, issue ledger
  and prior exports before mapping. Reuse the observed PDF55 / printed53
  opening and verify the ending from the scan.
- Limits: one article, six source pages, six outside lookup pages and one
  targeted retry per failed region. Preserve raw OCR, illustrations, literal
  code and scan-linked corrections. Record uncertainties without executing or
  repairing the historical program; reconcile issue counts after validation.

- Confirmed PDF55–57 / printed53–55; PDF58 opens the next article and was
  the only outside lookup. Mapped 15 regions, one illustration and eight code
  regions. Revised five crops to preserve code-number margins and complete
  wrapped rows; ten tasks were reused. All OCR tasks completed without failure.
- Prepared thirteen reading blocks and 141 numbered code rows, with 24 selected
  OCR corrections, eight block ranges, 141 line ranges, 25 listing anomalies
  and five prose review items. Line780 crosses PDF56–57 and retains both scan
  segments in its global byte range. Joined the two prose columns with both
  region references. Original wording and unverified code details remain visible.
- The separate rebuild is byte-identical; all 48 PDF tests and package checks
  pass. All 945 pinned prior files are unchanged. Browser acceptance is in
  progress; issue accounting is unchanged until those checks pass.

### 2026-09-28 — 11-batch-08 complete

- Restored 당신의 심장을 진단해 드립니다 (`maso-1983-11-toc-0020`) across
  PDF55–57 / printed53–55. PDF58 opens 도서관리 프로그램 and was the only
  outside lookup page. Complete coverage fits the saved one-article/six-page
  limit; no article assembly is required.
- Delivered **readable/sample-reviewed** content: 15 regions, thirteen blocks,
  eight code blocks and one illustration with its printed Microcomputing credit.
  Joined the prose columns at 고 + 형 지방 while retaining both scan references
  and regional transcripts. Repeated running titles, folios and decorative
  borders are excluded from the reading blocks.
- Preserved 141 numbered BASIC rows, 10–1520, and physical code wraps.
  `corrections.json` contains 24 selected OCR corrections, eight block ranges,
  141 `listing_line_index` entries, 25 `listing_anomalies` and five
  `text_review_items`. Line780 crosses PDF56–57; its global UTF-8 range contains
  two source segments, each with its own pinned scan and byte range. Verified
  all ranges and the complete continuation; no missing line numbers were invented.
- Retained duplicated Korean wording, original numeric references, unusual
  English spellings and printed age ranges. Missing closing quotes were not
  supplied. Exact whitespace, decorative asterisk counts, faint punctuation and
  ambiguous glyphs remain unverified. No custom bitmap markers were identified.
  No historical execution, semantic repair or factual modernization occurred.
- Revised five crops to widen the code-number margin and move split boundaries
  into whitespace, including the complete final row of 990. Five tasks processed,
  ten reused; both original and reviewed maps/states/evidence exports remain
  available. Final inputs are `map-reviewed.json` and `state-reviewed/`.
  Both states resume without modifying their ledgers; zero engine failures or
  retries. A draft page-schema rejection and a premature export rejected by the
  active OCR lock are recorded separately; both resolved before export.
- Exported `build/pdf-restoration/11-batch-08/`: 72 files / 16,576,347 bytes,
  including the wrapper/report and article package (68 files / 16,556,494 bytes).
  The separate rebuild is byte-identical. Saved regional transcription,
  correction evidence, crop review, validation, ledger snapshot and pinned closeout.
- All 48 focused PDF tests pass. Raw-byte preservation, regional coverage,
  source geometry, joined prose, image placement and all correction/listing
  offsets pass. All 945 pinned prior input files remain unchanged.
- Playwright checks at 1440×1000 and 360×800 pass: all thirteen DOM blocks match,
  the illustration loads, all 19 fetched asset pins match, and code scrolling
  stays within its container. Actual index→article, listing download and final
  scan clicks pass; downloaded bytes match. Inspected prose and mobile screenshots
  under `output/playwright/pdf-11-batch-08/`. Only the local favicon returned 404.
  Sandbox socket denial and npx DNS failure were resolved with approved
  escalation. No application or extraction code changes were required.
- Observed mapping took 91.7 seconds; crop review, transcription and correction
  preparation took 473.0 seconds, including processing waits and the server
  interruption. Initial render/crop and OCR timings were 10.46s/11.49s. Final
  cached timings were 12.86s/11.50s and include reused tasks; these are not a
  second full-pass cost or whole-issue throughput estimate.
- November now has eleven readable/sample-reviewed articles, one group heading
  and 35 unresolved eligibility decisions across 47 entries. Only this article's
  entry changed. Prior restorations and deferred submarine bitmap work remain intact.
- Checkpoint complete; stall count 0. Preview: `http://127.0.0.1:4187/`.
  Next: `11-batch-09`, the first bounded segment of 도서관리 프로그램
  (`maso-1983-11-toc-0021`). Reuse PDF58 / printed56, inspect local boundaries
  within one article, six source pages and six outside lookup pages, and record
  deferred coverage explicitly. The next TOC entry is GUN MAN at printed82;
  that spacing suggests segmentation but does not verify the actual ending.

### 2026-09-28 — 11-batch-09 started

- Heart article checkpoint is committed as `15b4f16`. Target: 도서관리 프로그램
  (`maso-1983-11-toc-0021`), first bounded segment. Pinned source, TOC, inventory,
  runtime, issue ledger and prior exports. Reuse PDF58 / printed56 opening.
- Limits: one article, six source pages, six outside lookup pages and one
  targeted retry per failed region. Verify local boundaries and record deferred
  or unresolved coverage explicitly; the next TOC item alone does not establish
  the article ending. Preserve raw OCR, illustrations, literal code and corrections.

- Confirmed six-page first segment: PDF58–63 / printed56–61. PDF64 continues
  the last sentence and is the only outside lookup. The full ending remains
  unverified. Mapped 54 regions, including 15 images: three illustrations, nine
  menu examples, two tables and one flowchart. No numbered code listing occurs
  in these six pages.
- All initial OCR tasks completed. Crop review recovered the complete instruction
  sentence, widened text/menu margins and trimmed adjacent letter fragments from
  the opening illustration. Original maps, state and OCR evidence are retained.
  Prose transcription, caption matching and continuation records are in progress.

### 2026-09-28 — 11-batch-09 complete

- Restored the first six pages of 도서관리 프로그램 (`maso-1983-11-toc-0021`),
  PDF58–63 / printed56–61, within the saved limit. PDF64 / printed62 is the
  only outside lookup and continues the final sentence. The full article ending
  remains unverified; the next TOC start does not establish coverage.
- Delivered **partial/sample-reviewed** content: 54 regions, 31 reading blocks
  and 15 figures (three illustrations, nine menus, two tables and one flowchart).
  Twelve captions remain paired with their figures. There is no numbered code
  listing in this segment. Menu, table and flowchart interiors remain images.
- `corrections.json` preserves 27 selected OCR corrections, eleven text review
  items, 31 UTF-8 `text_index` ranges and five prose joins, with regional text
  and scan references retained. The Catalog Enter prose follows the intervening
  tables and flowchart; this placement and the unfinished final sentence are
  documented. Original wording and ambiguous punctuation remain reviewable.
- The reader illustration intersects a menu and caption; its rectangular crop
  deliberately retains that source overlap, recorded in the corrections and
  visible gap notice. No artwork was erased or composited. No historical code
  execution, semantic repair or bitmap correction occurred.
- Crop revision recovered the complete instruction sentence and menu edges,
  retained illustration strokes and removed adjacent prose fragments from the
  opening illustration. Seven tasks processed with 47 cache hits, then one
  figure processed with 53 cache hits. The intermediate `state-reviewed/` was
  prepared only and superseded before processing. Final inputs are
  `map-final2.json` and `state-final2/`; all three completed states resume without
  ledger changes. Zero engine failures or retries.
- Exported `build/pdf-restoration/11-batch-09/`: 185 files / 30,234,337 bytes,
  including the wrapper/report and segment package (181 files / 30,192,570 bytes).
  The separate rebuild is byte-identical. Saved crop review, transcription,
  corrections, validation, issue ledger snapshot and pinned closeout.
- All 48 focused PDF tests pass. Raw bytes, regional coverage, source geometry,
  reading order, caption pairs and correction offsets pass. All 1,017 pinned
  prior files remained unchanged before the intentional issue-ledger update;
  every other TOC entry remains unchanged.
- Playwright checks at 1440×1000 and 360×800 pass: 31 DOM blocks, 15 loaded
  figures, 57 fetched asset pins, all text offsets and a visible partial-scope
  notice. No horizontal page overflow. Actual index→article, text download and
  final scan clicks pass; downloaded bytes match and the scan loads.
  Inspected table, flowchart and final-prose screenshots under
  `output/playwright/pdf-11-batch-09/`. The initial continuation screenshot was
  blank immediately after scrolling; a capture after two animation frames
  displays correctly. Both captures are retained. Only the favicon returned 404.
- Mapping took 126.7 seconds; crop review, transcription and correction preparation
  took 631.3 seconds, including processing waits. Initial render/crop and OCR
  timings were 21.69s/24.30s; final cached timings were 30.30s/24.36s, including
  reused tasks. These do not establish exact transcription or issue throughput.
- November now has eleven readable articles, one partial article, one group
  heading and 34 unresolved eligibility decisions across 47 entries. All twelve
  classified articles are sample-reviewed within their recorded limits.
  No application or extraction code changes were required; deferred submarine
  bitmap work remains intact. No issue closeout is claimed.
- Checkpoint complete; stall count 0. Preview: `http://127.0.0.1:4188/`.
  Next: `11-batch-10`, segment 2 of the same article, starting at PDF64 / printed62.
  Reuse the observed continuation image and preserve the prior segment within
  the same one-article, six-source-page and six-outside-lookup limits.

### 2026-09-28 — 11-batch-10 started

- Segment 1 is committed as `c389642`. Continue 도서관리 프로그램
  (`maso-1983-11-toc-0021`) with segment 2, starting at PDF64 / printed62.
  Reuse its observed opening and preserve the prior segment and continuation.
- Keep the one-article, six-source-page, six-outside-lookup limits and one
  targeted retry per failed region. The full article ending remains unverified.
  Ignore `tocs/` as requested; preserve the owner's existing `.gitignore` edit.

- Confirmed PDF64–69 / printed62–67 as the second six-page segment. PDF70 is
  the sole outside lookup and continues CATALOG SEARCH line320. Mapped 36
  regions: two pages of explanation, figure8 and ten code regions. The full
  article ending remains unverified.
- Built 30 reading blocks and one figure. CATALOG MASTER has 66 numbered rows,
  ENTER has 244, and the included SEARCH opening has 32 (342 total). Correction
  indexes distinguish each listing and retain five rows spanning source regions.
  Four prose joins retain the original regional transcripts.
- Crop review widened fourteen prose margins, two long code margins and one
  wrapped heading. All 36 tasks are complete with zero engine failures/retries.
  The byte-identical rebuild, 48 focused tests, byte ranges, source geometry and
  preservation of 1,202 pinned prior files pass. Browser acceptance is in progress;
  the issue ledger remains unchanged until it passes.

### 2026-09-28 — 11-batch-10 complete

- Restored 도서관리 프로그램 segment 2 (`maso-1983-11-toc-0021`), PDF64–69 /
  printed62–67. PDF70 / printed68 is the sole outside lookup and continues
  SEARCH320. The full article ending remains unverified. Both segments remain
  separate, preserving twelve pages of partial coverage; no assembly is claimed.
- Delivered **partial/sample-reviewed** content: 36 regions, 30 reading blocks,
  figure8 with its caption and ten code blocks. MASTER has 66 numbered rows
  (1–680), ENTER has 244 (10–2440), and SEARCH has 32 (10–320, final row partial).
  Physical code wraps, printed spelling and numbering remain intact. No code
  execution, semantic repair or manual bitmap correction occurred.
- `corrections.json` contains 23 selected OCR corrections, thirty listing
  anomalies, eleven prose review items, thirty text ranges, ten block ranges
  and 342 line ranges. `listing_id` distinguishes the three independently
  numbered programs. ENTER190, 620, 950, 1870 and 2350 each retain a single
  download range with source segments for both contributing regions.
- Four prose joins preserve original regional transcription and all scan links.
  The opening 한다. continues the prior segment's 기회를 제공. SEARCH320 ends
  at the printed SE; its observed PDF70 continuation is recorded but not imported.
  Exact spaces, decorative strings, faint punctuation and ambiguous glyphs
  remain unverified. A final enlarged-crop check corrected draft 표 3는 to 표 2는;
  the earlier build and repeat remain preserved as review drafts.
- Widened fourteen prose margins for page skew, two long code margins and one
  wrapped heading. Revision runs processed 14/2/1 tasks with 22/34/35 cache hits.
  Final inputs are `map-final3.json` and `state-final3/`. All four completed states
  resume without ledger changes; `state-reviewed/` was prepared only. Original,
  final and final3 evidence exports are saved; final2 has its retained state/cache.
  Zero engine failures or retries. An inventory-only page field was rejected
  during draft schema validation and removed before initial OCR preparation.
- Exported `build/pdf-restoration/11-batch-10/`: 156 files / 31,352,270 bytes,
  including the wrapper/report and segment package (152 files / 31,321,476 bytes).
  The separate final rebuild is byte-identical. All 48 focused PDF tests pass;
  geometry, raw bytes, regional representation, listing identities, prose joins
  and all text/code ranges validate. All 1,202 pinned prior files remained
  unchanged before the intentional issue-ledger update.
- Playwright checks at 1440×1000 and 360×800 pass: all thirty DOM blocks,
  ten code containers, the figure, forty asset pins and 342 line ranges.
  Horizontal code scrolling stays within the containers; the page does not
  overflow. Actual index→article, listing download and final scan clicks pass;
  downloaded bytes match and the scan loads. Inspected figure/prose and mobile
  code screenshots under `output/playwright/pdf-11-batch-10/`.
- Manual interaction changed a browser reference; a fresh navigation check
  passed. A private acceptance-script viewport reference was corrected and
  rerun. Local server socket denial and sandboxed npx DNS errors were resolved
  with approved escalation. Only the favicon returned 404; no application or
  extraction code changes were required.
- Mapping took 102.3 seconds. Initial draft review/build took 749.0 seconds;
  wall time after mapping through the corrected rebuild was 1,907.1 seconds,
  including earlier browser checks and approval/network waits. Initial
  render/crop and OCR times were 20.23s/29.75s; final cached times were
  23.01s/29.64s, including reused tasks. These are not active transcription-only
  timings, character-perfect verification or whole-issue throughput.
- November counts remain eleven readable articles, one partial article, one
  group heading and 34 unresolved eligibility decisions. Only the library
  article entry changed; its first segment record is unchanged. Deferred
  submarine bitmap work remains intact. `tocs/` and the owner's `.gitignore`
  edit were left alone. No issue closeout is claimed.
- Checkpoint complete; stall count 0. Preview: `http://127.0.0.1:4189/`.
  Next: `11-batch-11`, segment 3, starting at PDF70 / printed68. Preserve
  SEARCH320's carried row and the two prior segments within the same bounded
  limits. The next TOC start remains a hint, not article-extent evidence.

### 2026-09-28 — 11-batch-11 started

- Segment 2 is committed as `7ead10c`. Continue 도서관리 프로그램 with segment 3
  at PDF70 / printed68, beginning with the carried CATALOG SEARCH320 row.
  Pin current inputs and both prior segments; retain raw OCR and scan-linked
  corrections. Keep the one-article, six-source-page, six-outside-lookup limits
  and one targeted retry per failed region. Full article extent is unverified.
- Continue ignoring `tocs/` and preserve the owner's `.gitignore` edit.

- Segment 3 is built: eighteen regions, fifteen code blocks, three captions,
  506 numbered rows and one carried SEARCH320 fragment. The package retains
  eleven selected correction examples, 33 listing anomalies and one caption
  review. All 48 focused PDF tests pass; the separate rebuild is byte-identical
  and all 1,358 prior input pins remain unchanged. Browser acceptance is underway.

### 2026-09-28 — 11-batch-11 complete

- Restored 도서관리 프로그램 segment 3, PDF70–75 / printed68–73, under
  `maso-1983-11-toc-0021`. PDF76 was the sole outside lookup; BOOKSHELF200
  continues there. Six source pages remain within the checkpoint limit.
  Full article extent is unverified; GUN MAN's TOC start is only a hint.
- Eighteen regions produce eighteen reading blocks: fifteen code blocks and
  three listing captions, without figures. SEARCH has 350 visible numbered
  rows plus the carried 320 fragment, LIST has 42 rows, BORROW 95 and BOOKSHELF
  19. SEARCH ends here; LIST and BORROW are complete; BOOKSHELF is an opening.
- `corrections.json` indexes 507 local line ranges across four listing identities,
  506 with visible numbers. The first unnumbered fragment links the prior
  SEARCH320 manifest, download, byte range and scan provenance without inventing
  a local number. SEARCH1570 and BORROW740 each span two current regions.
  Eighteen text ranges and fifteen code-block ranges are verified.
- Retained eleven selected OCR corrections, 33 listing anomalies and one caption
  review. Printed SEARCH numbering gaps and 3445 remain intact. The apparent
  continuation of SEARCH3190 is printed after 3200 and stays in physical order.
  The caption's CATACOG spelling is preserved separately from code CATALOG.
  Exact whitespace, decorative symbol counts and ambiguous glyphs remain
  unverified; no code execution, semantic repair or character-perfect claim.
- All eighteen OCR tasks completed without engine failures, retries or crop
  revisions. Raw evidence and positions are preserved; resume leaves the ledger
  unchanged. Mapping took 73.3 seconds and review/build took 592.0 seconds,
  including processing waits. Render/crop and OCR took 17.35s/18.32s.
  These are not active transcription-only or whole-issue throughput measurements.
- Exported `build/pdf-restoration/11-batch-11/`: 87 files / 29,175,443 bytes,
  including the wrapper/report and segment package (83 files / 29,156,445 bytes).
  A separate rebuild is byte-identical. All 48 focused PDF tests pass; geometry,
  raw evidence, regional representation, identities and byte ranges validate.
  All 1,358 pinned prior files remained unchanged before the ledger update.
- Background Playwright checks pass at 1440×1000 and 360×800: eighteen DOM
  blocks, fifteen code containers, 22 asset pins and all 507 line ranges.
  Code scrolling works without page overflow. Actual index→article, listing
  download and final scan clicks pass; download bytes match and the scan loads.
  Inspected desktop SEARCH and mobile BOOKSHELF screenshots under
  `output/playwright/pdf-11-batch-11/`. Only favicon.ico returned 404.
- November counts remain eleven readable articles, one partial article, one
  group heading and 34 unresolved eligibility decisions. Only the library
  entry changed; both prior segment records remain identical. Its three separate
  segments cover PDF58–75 / printed56–73, eighteen pages, without assembly or
  a complete-article claim. Deferred submarine bitmap work remains intact.
  `tocs/` and the owner's `.gitignore` edit were left alone.
- Checkpoint complete; stall count 0. Preview: `http://127.0.0.1:4190/`.
  Next: `11-batch-12`, segment 4 at PDF76 / printed74, beginning with
  BOOKSHELF200. Reuse the observed opening and preserve all three segments.
  No application or extraction code changes were required; no issue closeout.

### 2026-09-28 — 11-batch-12 started

- Segment 3 is committed as `5473888`. Continue 도서관리 프로그램 segment 4
  from PDF76 / printed74 and BOOKSHELF200. Preserve all three earlier segments,
  raw OCR and scan-linked corrections. Retain the six-source-page ceiling,
  six outside lookups and one targeted retry per failed region. Verify the
  boundary locally; the next TOC start does not establish the article ending.
- Continue ignoring `tocs/` and preserve the owner's `.gitignore` edit.

- Segment 4 is built with twenty regions, nineteen code blocks and one caption.
  Its 309 numbered rows belong to BOOKSHELF and SC SEQ LIST0–6. Enlarged scans
  confirm duplicate BOOKSHELF590; both occurrences remain distinct. Five rows
  cross regions and LIST6's final240 continues outside this segment on PDF82.
- Widened the left margins of r02 and r20 to retain clipped line-number digits.
  The final OCR run processed two tasks and reused eighteen cached results.
  Both states and evidence exports remain preserved. The reviewed package has
  eighteen selected OCR corrections, 43 listing anomalies and one caption review.
  Browser acceptance and checkpoint reconciliation are underway.

### 2026-09-29 — 11-batch-12 complete

- Restored 도서관리 프로그램 segment 4, PDF76–81 / printed74–79, under
  `maso-1983-11-toc-0021`. Six included pages remain within the source ceiling;
  PDF82 is the sole outside lookup. SC SEQ LIST6's 240행 continues there.
  Full article extent remains unverified; the next TOC start is only a hint.
- Twenty regions produce twenty reading blocks: nineteen code blocks and one
  caption, without figures. The 309 visible numbered rows belong to eight
  programs: BOOKSHELF has 118 (200–1370), SC SEQ LIST0–5 each have 28 (10–290),
  and LIST6 has 23 (10–240, final row incomplete). BOOKSHELF ends here; its
  opening remains in segment 3. LIST0–5 are complete, and LIST6 is partial.
- `corrections.json` verifies twenty text ranges, nineteen code-block ranges
  and 309 line ranges. BOOKSHELF950, LIST2's 110 and 280, LIST3's 220 and LIST6's
  40 each retain two source segments. Both printed BOOKSHELF590 rows are kept
  with distinct occurrence/line IDs; 580 is absent. No SC SEQ listing's missing
  90 was invented. The final240 has explicit deferred continuation provenance.
- Retained eighteen selected OCR corrections, 43 listing anomalies and one
  caption review. Original spellings, DATA punctuation and the caption's SEO
  versus code SEQ remain separately visible. Exact spaces, strings, faint
  punctuation and glyphs remain unverified; no execution or semantic repair.
  A final enlarged scan check moved BOOKSHELF1310's opening parenthesis to its
  printed continuation row. The earlier package and repeat are preserved in
  ignored `11-batch-12-review-draft/` and `11-batch-12-repeat-review-draft/`.
- Widened two left crop margins, r02 and r20, to retain all line-number digits.
  Final inputs use `map-final.json` and `state-final/`. The revision processed
  two tasks with eighteen cache hits; both completed states resume unchanged.
  Both evidence exports remain saved. Zero engine failures or retries.
- Exported `build/pdf-restoration/11-batch-12/`: 95 files / 32,537,804 bytes,
  including wrapper/report and segment package (91 files / 32,516,920 bytes).
  The separate final rebuild is byte-identical. All 48 focused PDF tests pass;
  source geometry, raw evidence, regional coverage, identities and byte ranges
  validate. All 1,445 prior file pins remained unchanged before the ledger update.
- Background Playwright checks pass at 1440×1000 and 360×800: twenty DOM blocks,
  nineteen code containers, 24 asset pins and all 309 line ranges. Code scrolling
  works without page overflow. Actual index→article, final listing download and
  final scan clicks pass; downloaded bytes match and the scan loads. Inspected
  desktop BOOKSHELF and mobile DATA screenshots under
  `output/playwright/pdf-11-batch-12/`. Checks were repeated after the wrap fix;
  only favicon.ico returned 404. No application or extraction code changes.
- Mapping took 66.6 seconds. Initial draft review/build took 643.0 seconds;
  wall time after mapping through the corrected rebuild was 1,048.0 seconds,
  including earlier browser checks and waits. Initial render/crop and OCR times
  were 19.63s/19.84s; final cached totals were 25.02s/19.81s, including reused
  tasks. These are not active transcription-only or whole-issue throughput.
- November counts remain eleven readable articles, one partial article, one
  group heading and 34 unresolved eligibility decisions. Only the library
  entry changed; its three prior segment records remain identical. Four separate
  segments now cover PDF58–81 / printed56–79, twenty-four pages, without assembly
  or a complete-article claim. Deferred submarine bitmap work, `tocs/` and the
  owner's `.gitignore` edit remain untouched. No issue closeout is claimed.
- Checkpoint complete; stall count 0. Preview: `http://127.0.0.1:4191/`.
  Next: `11-batch-13`, segment 5 at PDF82 / printed80. Preserve LIST6's carried
  240 row with a link to this segment's exact bytes and scans, and verify the
  remaining article boundary within the same bounded limits.

### 2026-09-29 — 11-batch-13 started

- Segment 4 is committed as `7c03660`. Continue 도서관리 프로그램 segment 5
  from PDF82 / printed80, preserving the carried SC SEQ LIST6 line240 and its
  prior byte/scan references. Pin all four previous segments and inspect the
  article boundary locally. Retain the six-source-page, six-outside-lookup
  limits and one targeted retry per failed region.
- Continue ignoring `tocs/` and preserve the owner's `.gitignore` edit.

- Boundary verified: LIST9 DATA290 closes on PDF83 / printed81, and PDF84 /
  printed82 visibly opens GUN MAN. Only PDF82–83 are included; PDF84 is the sole
  outside lookup. All five segments now cover 26 contiguous pages, PDF58–83,
  while assembly remains pending.
- Built seven code regions with 89 visible numbered rows and the carried LIST6
  line240 fragment. Ninety line-index entries distinguish four listings and
  both printed LIST7 170 occurrences; the second follows180. Two rows cross
  current regions. Six selected OCR corrections and twenty listing anomalies
  retain source-linked review evidence. Widened r01's bottom margin for its
  closing quote; one task was reprocessed with six cache hits.

### 2026-09-29 — 11-batch-13 complete

- Restored 도서관리 프로그램 segment 5, PDF82–83 / printed80–81, under
  `maso-1983-11-toc-0021`. LIST9 DATA290 and its closing string end on PDF83;
  PDF84 / printed82 visibly opens GUN MAN. This verifies the article's full
  extent as PDF58–83 / printed56–81, twenty-six pages. Only two source pages
  and one outside lookup were needed; no following article content was extracted.
- Seven regions produce seven code blocks, with no figures or captions. The
  89 visible numbered rows comprise LIST6's final250–290 and complete LIST7–9
  (28 rows each). One unnumbered LIST6 line240 continuation makes ninety local
  line-index entries across four listing identities. It links the prior segment's
  manifest, listing, corrections, exact byte range and scan provenance without
  inventing a local number. LIST7's180 and LIST8's130 each span two regions.
- `corrections.json` retains seven text ranges, seven code-block ranges, ninety
  line ranges, six selected OCR correction examples and twenty listing anomalies.
  LIST7 prints170 twice: the second follows180 and precedes200. Both occurrence
  IDs are preserved; 190 is not invented. The programs' absent90 stays absent.
  Original spelling, DATA punctuation and physical wraps remain intact. Exact
  spaces and ambiguous glyphs remain unverified; no execution or semantic repair.
- Widened r01's bottom margin around LIST6 DATA290's separate closing quote.
  Final inputs are `map-final.json` and `state-final/`. One task was processed
  with six cache hits. Both completed states resume unchanged and both evidence
  exports remain saved. Zero engine failures or retries.
- Exported `build/pdf-restoration/11-batch-13/`: 43 files / 11,326,701 bytes,
  including wrapper/report and segment package (39 files / 11,313,954 bytes).
  The separate rebuild is byte-identical. All 48 focused PDF tests pass; geometry,
  raw evidence, regional coverage, identities, duplicate-number occurrences and
  byte ranges validate. The carried240 matches its prior pinned bytes. All five
  segments have disjoint contiguous page coverage, and all 1,540 prior file pins
  remained unchanged before the intentional ledger update.
- Background Playwright checks pass at 1440×1000 and 360×800: seven DOM/code
  blocks, eleven asset pins, all ninety line ranges, the prior-fragment link and
  verified-ending/assembly-pending status. Code scrolling works without page
  overflow. Actual index→article, listing download and final scan clicks pass;
  downloaded bytes match and the scan loads. Inspected desktop LIST7 and mobile
  carried-fragment screenshots under `output/playwright/pdf-11-batch-13/`.
  Only favicon.ico returned 404; no application or extraction code changes.
- Mapping took 69.0 seconds and review/build took 350.3 seconds, including
  processing waits. Initial render/crop and OCR times were 6.66s/6.64s; final
  cached totals were 6.65s/6.64s, including reused tasks. These are not active
  transcription-only timings or character-perfect verification.
- November counts remain eleven readable articles, one partial article, one
  group heading and 34 unresolved eligibility decisions. Only the library
  entry changed; its four earlier segment records remain identical. Availability
  remains partial because the primary package is only the final two-page segment
  and the complete article has not been assembled. Deferred submarine bitmap
  work, `tocs/` and the owner's `.gitignore` edit remain untouched.
- Checkpoint complete; stall count 0. Preview: `http://127.0.0.1:4192/`.
  Next: `11-library-assemble`, one article with zero new source pages or OCR tasks.
  Preserve all five packages, namespace repeated region/block IDs, and retain
  text/prose/listing/anomaly indexes and cross-segment continuations. The saved
  assembly plan expects 135 regions, 106 blocks, 51 code blocks and sixteen
  figures. Add bounded assembly support where required, with meaningful checks.
  After assembly, `11-batch-14` starts GUN MAN at PDF84 / printed82. No issue
  closeout is claimed.

### 2026-09-29 — 11-library-assemble started

- Final segment committed as `d7e7ebb`. Assemble the five preserved packages
  covering PDF58–83 / printed56–81 into one article. No new source pages, OCR
  tasks or outside lookups. Preserve original packages and all correction data;
  namespace repeated IDs and link the two carried code fragments explicitly.
- Validate complete coverage, deterministic export, correction offsets, raw bytes
  and desktop/mobile reading. Keep manual glyph review deferred, ignore `tocs/`,
  and preserve the owner's `.gitignore` edit. Update progress and commit.

### 2026-09-29 — 11-library-assemble complete

- Assembled 도서관리 프로그램 across PDF58–83 / printed56–81: all 26 pages,
  135 regions, 106 reading blocks, 51 code blocks and sixteen figures. The prior
  boundary review observes LIST9 DATA290 ending on PDF83 and GUN MAN opening on
  PDF84. No new source pages, OCR tasks or outside lookups were used.
- Added opt-in `namespaced-v1` assembly support. Repeated regional, block and
  figure IDs receive segment prefixes with an explicit original identity map.
  Every original package remains byte-identical under its own segment directory;
  the original OCR settings still bind to their original maps. Default assembly
  behavior remains compatible with the existing submarine export.
- Combined `corrections.json` retains 106 UTF-8 text ranges, 24 prose/caption
  review items, 51 code-block ranges, 1,248 local line entries, 126 anomaly notes,
  sixteen program identities, nine local prose joins, regional transcriptions,
  figure order and image overlap notes. Original numbering reviews, policies,
  continuation declarations and complete correction files remain available.
- A separate logical line index links those local entries into 1,246 numbered
  rows. SEARCH320 and SC SEQ LIST6 line240 each retain both physical fragments,
  exact original ranges and verified prior manifest/listing/correction/scan pins.
  The listing download is the exact concatenation of original bytes. No number,
  newline or character is invented or removed. Duplicate BOOKSHELF590 and LIST7
  170 retain distinct occurrences in printed order; missing numbers stay absent.
  The prose continuation is linked through its original reading blocks.
- Thirteen superseded scope notes have exact-text dispositions and reasons.
  Remaining notes are labelled by source segment. Availability is now
  readable/sample-reviewed; exact glyphs, whitespace, strings and executable
  correctness remain unverified. Deferred submarine bitmap work is untouched.
- All 51 focused PDF tests pass, including synthetic repeated IDs, Korean byte
  offsets, carried-line pin/range rejection, duplicate numbers, deterministic
  export and rehashed correction tampering. The full separate rebuild is
  byte-identical. All 1,583 preserved input pins matched before the intentional
  ledger update; all 546 original package files were copied unchanged. The raw
  archive's 512 entries match their original files. The submarine assembly still
  validates with the current checker.
- Background Playwright checks pass at 1440×1000 and 360×800: all 106 DOM blocks,
  sixteen images, 139 asset pins, text/line ranges and continuation associations.
  All 51 code containers scroll on mobile without page overflow. Actual wrapper
  link, listing download and final scan clicks pass; downloaded bytes match and
  the final scan loads. Inspected desktop figure and mobile continuation images
  under `output/playwright/pdf-11-library-assemble/`. Only favicon.ico returned404.
  The test browser is closed; preview remains at `http://127.0.0.1:4193/`.
- Exported `build/pdf-restoration/11-library-assemble/library/`: 557 files /
  204,044,508 bytes, including the five retained original packages. Wrapper,
  report and manifest are in its parent directory. Validation, browser evidence,
  ledger snapshots and the next checkpoint plan are saved privately.
- November now has twelve readable/sample-reviewed articles, zero partial
  articles, one group heading and 34 unresolved eligibility decisions. Only the
  library entry changed, preserving all five original segment records. This is
  an article checkpoint, not issue closeout. Stall count0. `tocs/` and the owner's
  `.gitignore` change remain untouched.
- Next: `11-batch-14`, GUN MAN at PDF84 / printed82. Reuse the observed opening
  scan, establish the ending before assigning coverage, and retain the existing
  one-article/six-source-page limit, six outside lookup pages and one engine retry
  per failed region. Update this log and commit that checkpoint separately.

### 2026-09-29 — 11-batch-14 started

- Library assembly committed as `6d0d63e`. Continue with GUN MAN under its
  existing TOC identity, from observed PDF84 / printed82. Retain the one-article,
  six-source-page ceiling and verify the following boundary before mapping.
- Preserve literal BASIC and scan-linked corrections, update the November ledger,
  validate the reader/downloads, and commit. Ignore `tocs/`; retain the owner's
  `.gitignore` change and deferred submarine bitmap review.

- Mapped the clearly identified GUN MAN page, PDF84 / printed82, with ten
  regions. PDF85 is an uncaptioned photograph whose attribution remains unresolved;
  it is retained only as boundary evidence. PDF86 opens MARK. Completed ten crop
  tasks and nine text OCR outcomes with zero engine failures or retries.
- Reviewed all included regions: nine text/code blocks and one original title
  illustration. Fifty numbered rows (2000–2490) occupy 51 physical code lines;
  2430 wraps once. Retained SPRITE hex strings, 25 line-specific review notes,
  two prose review items and nine selected OCR correction examples. Exact glyphs,
  spaces and program execution remain unverified. Rebuild and all 51 tests pass;
  2,144 prior pins match. Browser checks and ledger closeout are in progress.

### 2026-09-29 — 11-batch-14 complete

- Restored GUN MAN under `maso-1983-11-toc-0022`, PDF84 / printed82, as
  readable/sample-reviewed. The identified page contains its title illustration,
  HYCOM-800 label, supplier credit, instruction callout, introduction, program
  explanation and framed BASIC listing. Neighbor PDF85 is an uncaptioned photo
  without explicit continuation; its attribution remains unresolved and it is
  boundary evidence only. PDF86 / printed84 opens MARK. No photograph ownership
  or character-perfect coverage is inferred from the TOC interval.
- Ten regions yield nine reading blocks, one code block and one figure. The
  original title illustration retains its embedded platform/title labels and
  artist mark; overlapping text crops make the labels accessible without erasing
  pixels. The fifty numbered rows, 2000–2490, occupy 51 physical lines. Wrapped 2430
  remains one indexed row with both printed lines and an exact byte range.
- `corrections.json` retains nine text ranges, one code-block range, fifty line
  ranges, nine selected OCR correction examples, 25 listing review notes and two
  prose review items. Printed 2390's2809, 2400's J NEXT, 2450's FORM-203 and 2480's
  FORV-0 remain as read. Faint operators, I/1, 0/O and SPRITE hex runs are explicit
  manual-review items; no bitmap bytes are inferred or code executed/repaired.
  The explanation's 우측 for 2140–2170 remains distinct from other descriptions.
- Used one source page and two outside lookups. The final input is `map.json`;
  processing state is `state-mapped/`. Ten crop tasks and nine text OCR outcomes
  completed with zero engine failures or retries. The completed state resumes
  unchanged, and the separate evidence export remains saved. Raw source geometry,
  scan assets, OCR text, positions and original settings all validate.
- The package is 48 files / 7,567,902 bytes and rebuilds byte-identically. All 51
  focused PDF tests pass; all 2,144 preserved file pins matched before the intended
  ledger update. Text and listing ranges, selected correction excerpts, physical
  wrap preservation, source identity and all mapped-region coverage validate.
  No extraction or reader implementation changes were needed.
- Background Playwright checks pass at 1440×1000 and 360×800: nine DOM blocks,
  one figure, fourteen asset pins, all text/line ranges, visible photo-attribution
  limits and literal code. Actual wrapper→article, listing download and code-scan
  clicks pass; downloaded bytes match and the scan loads. Horizontal code scrolling
  works without page overflow. Inspected desktop illustration and mobile listing
  images under `output/playwright/pdf-11-batch-14/`. Only favicon.ico returned 404.
  Browser closed; preview remains at `http://127.0.0.1:4194/`.
- November now has thirteen readable/sample-reviewed articles, one group heading
  and 33 unresolved eligibility decisions. Only GUN MAN's entry changed. Original
  library segments/assembly, deferred submarine bitmap correction, `tocs/` and
  the owner's `.gitignore` change remain untouched. No issue closeout. Stall count 0.
- Mapping took 162.5 seconds; review/build/validation took 794.4 seconds,
  including tool waits. Render/crop and OCR processing took 4.21 and 4.10 seconds.
  These are wall timings, not character-perfect proofreading throughput. The
  wrapper/report export totals 52 files / 7,581,586 bytes.
- Private validation, timing, browser evidence, ledger snapshots and closeout
  records are saved. Next is `11-batch-15`: MARK at PDF86 / printed84, including
  the education-heading eligibility check. Reuse the observed opening image,
  establish its ending and split before exceeding six source pages; retain the
  six-lookup and one-engine-retry limits. Update progress and commit separately.

### 2026-09-29 — 11-batch-15 started

- GUN MAN committed as `62379bf`. Continue with MARK at PDF86 / printed84,
  under its existing TOC identity; verify the ending and reconcile the education
  heading without duplicating article content. Retain the one-article/six-source-
  page and six-outside-lookup limits.
- Preserve raw OCR, literal code, scans and correction indexes; validate the
  reader and downloads, update the ledger and commit. The neighboring PDF85 photo
  remains unassigned. Ignore `tocs/` and preserve the owner's `.gitignore` edit.

- Verified MARK on PDF86–88 / printed84–86, ending at 3560 END; PDF89 opens
  유효숫자를 18로. Saved the education-heading ownership decision separately.
  Fifteen regions include a flowchart; the repeated running header is excluded.
- Reviewed twelve reading blocks and two prose joins. The full program has 244
  numbered rows; the inline 3560 END example is indexed separately. Four rows
  wrap physically. The correction record retains 144 line review notes, four
  prose review items, thirteen selected OCR corrections and one explicit unknown
  output label on line 3320. Exact glyphs/spacing and execution remain unverified.
- Fifteen crop tasks and fourteen text OCR outcomes completed without engine
  failures or retries. The state resumes unchanged, the rebuild is byte-identical,
  all 51 PDF tests pass and 2,196 preserved input pins match. Browser checks and
  issue-ledger closeout are underway.

### 2026-09-29 — 11-batch-15 complete

- Restored 기능이 강화된 성적관리프로그램 MARK, `maso-1983-11-toc-0024`,
  across PDF86–88 / printed84–86 as readable/sample-reviewed. The listing ends
  at 3560 END; PDF89 / printed87 opens 유효숫자를 18로. Recorded 교육입문,
  `maso-1983-11-toc-0023`, as a grouping with no separate body identified here.
  The neighboring PDF85 photo remains unassigned; proximity is not ownership.
- Fifteen regions produce twelve reading blocks, four code blocks and one
  original flowchart. The repeated running header is excluded. Two prose joins
  preserve the opening column continuation and the sentence continuing onto
  the following page around the diagram. Original regional transcriptions,
  the flowchart and its separate caption remain available.
- The main program has 244 numbered rows; the prose's 3560 END example has its
  own listing identity. Together there are 245 indexed rows and 249 physical
  lines. Rows 1705, 1715, 1725 and 1735 retain their wraps. Printed numbering gaps,
  MATHMATICS, unusual operators and PLAY strings remain as transcribed, without
  semantic repair. Code was not executed; exact glyphs and spaces are unverified.
- `corrections.json` retains twelve text ranges, four code-block ranges, all
  245 line ranges, 144 line review notes, four prose review items and thirteen
  selected OCR corrections. The faint output label on 3320 is explicitly marked
  `⟦판독불확실:출력표시⟧`. Its exact UTF-8 range and scan are indexed under
  `unresolved_text`, with original characters left unknown. The marker is not
  source code. Other faint rows retain visible manual-review limits.
- Used three source pages and one outside lookup. Fifteen crop tasks and fourteen
  text OCR outcomes completed with zero engine failures or retries; the four code
  crops used scale 4000. Final inputs are `map.json` and `state/`. The completed
  state resumes unchanged and the separate raw-evidence export validates.
- The package has 68 files / 14,034,712 bytes and rebuilds byte-identically. All
  51 focused PDF tests pass. All 2,196 preserved input pins matched before the
  intentional ledger update. Raw OCR/settings, geometry, complete regional
  coverage, literal downloads, unique listing identities, numbering gaps, four
  wraps, correction excerpts, two prose joins and the uncertainty marker validate.
  No extraction or reader implementation changes were needed.
- Background Playwright checks pass at 1440×1000 and 360×800: twelve DOM blocks,
  one flowchart, nineteen asset pins and all text/line ranges. Actual wrapper
  navigation, listing download and final scan clicks pass; downloaded bytes match.
  Code scrolling works without page overflow, and the 3320 marker and review scope
  are present in the reader. Inspected desktop flowchart and mobile code images
  under `output/playwright/pdf-11-batch-15/`. Only favicon.ico returned 404.
  Preview remains at `http://127.0.0.1:4195/`.
- November now has fourteen readable/sample-reviewed articles, two group headings
  and 31 unresolved eligibility decisions. Only MARK and the education grouping
  changed. Prior packages, deferred submarine bitmap review, `tocs/` and the
  owner's `.gitignore` change remain untouched. No issue closeout. Stall count 0.
- Mapping took 122.6 seconds; review/build/validation took 1378.3 seconds,
  including tool waits. Cached render/crop and OCR totals were 16.05s and 11.49s.
  These are wall timings, not character-perfect proofreading throughput. The
  wrapper/report totals 72 files / 14,052,852 bytes. The background
  browser is closed; closeout, timing, validation and ledger snapshots are saved.
- Next: `11-batch-16`, 유효숫자를 18로 at PDF89 / printed87. Reuse the observed
  opening image, establish actual coverage and split before exceeding six source
  pages; do not infer extent from the next TOC entry. Retain the six-lookup and
  one-engine-retry limits, update progress and commit the checkpoint separately.

### 2026-09-29 — 11-batch-16 started

- MARK committed as `cdb2e4b`. Continue with 유효숫자를 18로 under
  `maso-1983-11-toc-0025`, beginning at observed PDF89 / printed87. Establish
  its actual ending; use a numbered segment if coverage exceeds six source pages.
- Preserve raw OCR, literal listings and scan-linked correction records. Retain
  the six outside lookup and one retry limits, update issue accounting, validate
  the export and browser, and commit. Ignore `tocs/`; preserve the owner's
  `.gitignore` change and deferred submarine bitmap correction.

- Verified the complete article on PDF89–91 / printed87–89. PDF92 is an
  unrelated submission notice; a separate handoff lookup confirms 1차방정식
  at PDF111 / printed109. Intervening pages are not assigned to this article.
- Sixteen regions preserve eleven reading blocks, three original annotated
  listing frames and three code blocks. The 86 numbered rows occupy 121 physical
  lines, including 32 wrapped rows. Fourteen margin labels have exact text ranges,
  listing associations and bracket scans in `corrections.json`.
- Corrected one preliminary map note after enlarged review: 10480 is present,
  followed by10500; 10490 is absent. Geometry is unchanged and the reviewed state
  reuses all cached results. Thirteen text OCR outcomes completed without failures
  or retries. The package rebuild is byte-identical, all 51 PDF tests pass and
  2,452 preserved input pins match. Browser checks and ledger closeout are underway.

### 2026-09-29 — 11-batch-16 complete

- Restored 유효숫자를 18로, `maso-1983-11-toc-0025`, across PDF89–91 /
  printed87–89 as readable/sample-reviewed. The program listing runs from 10000
  through 10850 GOTO10420. The described routines are present through 10845; PDF92
  is an unrelated software submission notice. A second outside lookup confirms
  the next selected article, 1차방정식, at PDF111 / printed109. The intervening
  pages were not inspected or assigned to this article based on the TOC gap.
- Sixteen regions yield eleven reading blocks, three code blocks and three
  original annotated listing frames. Three prose columns join at two sentence
  continuations. The original frames preserve the margin labels and brackets;
  their separate code and label transcriptions intentionally overlap the images.
- The listing contains 86 numbered rows and 121 physical lines, with 32 wrapped
  rows. Numbers, variables, operators and quoted strings that split across physical
  lines retain those breaks. Enlarged review confirms 10480 followed by 10500;
  no 10490 is invented. The additional 10845 row remains in printed order. Line 10260's
  second statement appears as SA$ and stays unchanged; no semantic repair or
  execution was performed. Exact spacing, repeated asterisks and faint glyphs
  remain unverified.
- `corrections.json` retains eleven text ranges, three code-block ranges, all 86
  line ranges, 49 line review notes, four prose review items and thirteen selected
  OCR correction examples. Fourteen margin annotations have exact UTF-8 text
  ranges, listing-line associations and original bracket scans. These explanatory
  labels remain separate from program code. The printed 10430 prose reference is
  preserved without reconciling it to a different program line.
- Three source pages and two outside lookups stay within the limits. Sixteen
  crop tasks and thirteen text OCR outcomes completed without failures or retries.
  A preliminary map note wrongly named the absent number; `map-reviewed.json`
  corrects only that note. Geometry stays identical and `state-reviewed/` reuses
  every cached result. Initial and reviewed evidence exports remain saved; raw
  OCR, positions and scan bytes match. The final state resumes unchanged.
- The package contains 66 files / 24,285,466 bytes and rebuilds byte-identically.
  All 51 focused PDF tests pass; all 2,452 preserved input pins matched before the
  intentional ledger update. Every mapped region, text/line range, wrap, selected
  correction, margin association, source transform and raw archive entry validates.
  No extraction or reader implementation changes were needed.
- Background Playwright checks pass at 1440×1000 and 360×800: eleven DOM blocks,
  three figures, twenty asset pins, all text/line ranges and fourteen margin-label
  ranges. The first review caught a private recipe variable shadowing the full
  scope notes; corrected it, rebuilt and checked every note in the final DOM.
  Actual wrapper navigation, listing download and final scan clicks pass. The
  3,454-byte download matches exactly; the final scan loads at 1686×3276. All three
  code containers scroll horizontally without page overflow. Inspected desktop
  annotated-frame and mobile-code screenshots under `output/playwright/pdf-11-batch-16/`.
  Only favicon.ico returned 404. Browser closed; preview remains at
  `http://127.0.0.1:4196/`.
- November now has fifteen readable/sample-reviewed articles, two group headings
  and 30 unresolved eligibility decisions. Only this article's entry changed.
  Prior packages, deferred submarine bitmap work, `tocs/` and the owner's
  `.gitignore` change remain untouched. No issue closeout; stall count 0.
- Mapping took 71.0 seconds; review/build/validation took 750.9 seconds, including
  tool waits. Cached render/crop and OCR totals were 19.52s and 9.54s. These wall
  timings do not measure character-perfect proofreading throughput. The wrapper,
  report and manifest total 70 files / 24,303,358 bytes. Closeout, validation, browser
  records, ledger snapshots and the next checkpoint plan are saved privately.
- Next: `11-batch-17`, 1차방정식 at observed PDF111 / printed109. Establish its
  ending and preserve its table, inline examples and full listing distinctly.
  Split before exceeding six source pages; retain six outside lookups and one
  engine retry per failed region. Update this log and commit separately.

### 2026-09-29 — 11-batch-17 started

- Previous checkpoint committed as `29f679b`. Continue with 1차방정식,
  `maso-1983-11-toc-0026`, from observed PDF111 / printed109. Establish the
  actual ending and use a numbered segment if it exceeds six source pages.
- Preserve the terminology table, prose, inline examples and full listing with
  distinct correction identities. Retain six outside lookups and one OCR retry
  per failed region; update the ledger, validate the preview and commit. Ignore
  `tocs/`, retain the owner's `.gitignore` edit and defer submarine bitmap work.

- Established five-page coverage, PDF111–115 / printed109–113. The listing ends
  on PDF114, while figure3 continues through both columns of PDF115. PDF116 is
  an advertisement; a separate handoff lookup confirms the next article at PDF118.
- Thirty-one regions preserve21 reading blocks, eight code blocks and six images.
  The main listing has 184 numbered rows plus two separately identified inline 348
  examples. The 186 indexed rows occupy 334 physical lines; 113 rows wrap, including
  cross-column264 and 418. Fifteen table pairs, five prose review items, 129 line
  review notes and fourteen selected corrections are recorded.
- Widened four listing crops during review; retained initial, reviewed and final
  maps/evidence. Only affected regions were reprocessed, with zero engine failures
  or retries. All 51 PDF tests pass, the rebuild is byte-identical and2,824 prior
  file pins match. Browser checks and issue accounting are in progress.

### 2026-09-29 — 11-batch-17 complete

- Restored 1차방정식, `maso-1983-11-toc-0026`, across PDF111–115 /
  printed109–113 as readable/sample-reviewed. The BASIC listing ends with
  436 RETURN on PDF114, but figure3's output continues through both columns
  of PDF115. PDF116 is an unrelated advertisement. A second outside lookup
  confirms 마이크로 컴퓨터 시스템입문 at PDF118 / printed116; PDF117 was
  not inspected or assigned to either article.
- Thirty-one regions yield 21 reading blocks, eight code blocks and six images:
  the displayed equation, terminology table, problem-selection screen and three
  consecutive output frames. Original output images preserve the printed numbers
  and mathematical results without recalculation or transcription as BASIC.
- The main program has 184 numbered rows, with two independently identified
  inline 348 examples. The 186 indexed rows occupy 334 physical code lines; 113 rows
  wrap. Lines 264 and 418 continue across columns, with exact ranges and both scan
  fragments in each line record. No line number or code character is inserted at
  the boundary. The inline examples' AND text is separated from Korean connecting
  prose while preserving the original mixed regions.
- `corrections.json` retains 21 text ranges, eight code-block ranges, 186 line
  ranges, 129 line review notes, five prose review items and fourteen selected OCR
  corrections. Fifteen `table_rows` records link English/Korean pairs to exact
  text ranges and the original table. Printed PERPENCULAR, line 144's 60,
  line 384's U8 and omitted quotes remain as read. Exact spaces, repeated equals,
  faint glyphs and executable correctness remain unverified; no semantic repair.
- Five source pages and two outside lookups stay within the limits. The initial
  31 crop tasks yielded 25 text OCR outcomes without engine failures or retries.
  Review widened the lower edges of r24/r25 and the side edges of r26/r27 to
  retain complete boundary rows. Two mapping revisions reprocessed only these
  four regions; unchanged OCR/scan bytes match. Initial, reviewed and final
  evidence exports remain saved. Final inputs use `map-final.json` and
  `state-final/`; all three completed states resume unchanged.
- The package contains 117 files / 28,689,965 bytes and rebuilds byte-identically.
  All 51 focused PDF tests pass; all 2,824 preserved input pins matched before the
  ledger update. Every region, source transform, raw archive entry, text/code
  range, table pair, mixed inline split and cross-column continuation validates.
  No extraction or reader implementation changes were needed.
- Background Playwright checks pass at 1440×1000 and 360×800: all 21 DOM blocks,
  six figures, 35 asset pins, 186 line ranges, fifteen table ranges and both column
  continuations. All eight code containers scroll without page overflow. Actual
  wrapper navigation, listing download and final scan clicks pass; the 7,997-byte
  download matches exactly and the last output scan loads at 1129×3460. Inspected
  desktop table and mobile continuation screenshots under
  `output/playwright/pdf-11-batch-17/`. All review notes are visible. Only
  favicon.ico returned 404. Browser closed; preview remains at
  `http://127.0.0.1:4197/`.
- November now has sixteen readable/sample-reviewed articles, two group headings
  and 29 unresolved eligibility decisions. Only this article's ledger entry changed.
  Earlier packages, deferred submarine bitmap work, `tocs/` and the owner's
  `.gitignore` change remain untouched. No issue closeout; stall count 0.
- Mapping took 116.3 seconds; review/build/validation took 1183.7 seconds including
  tool waits. Final cached render/crop and OCR totals were 33.17s and 16.19s. These
  timings do not establish character-perfect proofreading throughput. Wrapper,
  report and manifest total 121 files / 28,717,853 bytes. Closeout, validation,
  browser records, ledger snapshots and next-checkpoint inputs are saved privately.
- Next: `11-batch-18`, 마이크로 컴퓨터 시스템입문 at PDF118 / printed116.
  Establish its ending, preserve the opening photograph and column order, and
  split before exceeding six source pages. Retain six outside lookups and one
  engine retry per failed region; update this log and commit separately.

### 2026-09-29 — 11-batch-18 started

- Previous checkpoint committed as `54b3941`. Continue with 마이크로 컴퓨터
  시스템입문, `maso-1983-11-toc-0027`, from observed PDF118 / printed116.
  Verify the ending and preserve its opening photograph, prose order and diagrams.
- Retain the six-source-page, six-outside-lookup and one-engine-retry limits.
  Save scan-linked corrections, validate the package and browser, update the issue
  ledger and commit. Ignore `tocs/`; retain the owner's `.gitignore` edit and
  deferred submarine bitmap work.

### 2026-09-29 — 11-batch-18 transcription and package review

- Verified the complete article at PDF118–120 / printed116–118, ending with
  references and figure3. PDF121 opens the separate English-learning article.
  Mapped 22 regions: eighteen text regions and the opening photograph plus three
  diagrams. Four column/page boundaries become three joined prose blocks.
- Enlarged scan review corrected the chapter outline and publisher reading.
  Widened r02 to retain its overlapping callout, and r08/r19 to preserve edge
  glyphs. Kept initial evidence; only three crop tasks were reprocessed, with no
  engine failures or retries. Both completed OCR states resume unchanged.
- Built fourteen reading blocks with seven localized review notes and four
  scan-linked bibliography ranges in `corrections.json`. Historical dates,
  specifications, prices and printed names remain unchanged. No code listing.
- The 86-file package rebuilds byte-identically; all 51 PDF tests pass. All
  3,237 preserved input pins, raw OCR bytes, text/reference ranges, source
  geometry and prose joins validate. Browser acceptance and ledger closeout next.

### 2026-09-29 — 11-batch-18 complete

- Restored 마이크로 컴퓨터 시스템입문 under existing TOC identity
  `maso-1983-11-toc-0027`, PDF118–120 / printed116–118. Status is
  `readable / sample-reviewed`; exact-glyph accuracy remains limited. The six
  chapter titles are a series outline; this article contains chapter1 only.
- The opening photo includes its overlapping callout. All three diagrams retain
  original labels and geometry. Figure3 follows the programming explanation in
  reading order, before the resumed history; the source placement is preserved
  in the map. No historical facts, code or diagrams were rewritten or executed.
- `corrections.json` contains fourteen text ranges, seven localized review items,
  four numbered reference ranges and five selected OCR correction examples, all
  linked to scans. Regional transcription preserves the four original join
  boundaries. Printed chip dimensions, dates, transistor counts, model names,
  prices and bibliographic wording remain available for manual review.
- Three source pages and one outside lookup stay within the limits. Initial OCR
  completed 22 crop tasks and eighteen text outcomes without failures or retries.
  The final map reprocessed only r02/r08/r19. Both evidence exports remain saved;
  unchanged OCR and scan bytes match. Final recipe uses `map-final.json` and
  `state-final/`. A missing null caption field in the private recipe was fixed
  before successful export; no extraction or reader implementation change.
- The package has 86 files / 16,240,666 bytes and rebuilds byte-identically. All
  51 PDF tests pass. All 3,237 preserved input pins matched before the ledger
  update. Every region, raw archive entry, prose join, text/reference range and
  original page transform validates. No spurious `listing.txt` is generated.
- Background Playwright checks pass at 1440×1000 and 360×800: fourteen DOM blocks,
  four images, 25 asset pins, fourteen text ranges, seven review items and four
  bibliography ranges. No page overflow; all review notes visible. Actual wrapper
  navigation, article download and final diagram scan clicks pass. The downloaded
  9,106 bytes match exactly; the final scan loads at 2351×516. Desktop diagram and
  mobile prose screenshots were inspected under `output/playwright/pdf-11-batch-18/`.
  Only favicon.ico returned 404. Browser closed; preview remains at
  `http://127.0.0.1:4198/`.
- November now records seventeen readable/sample-reviewed articles, two group
  headings and 28 unresolved eligibility decisions. Only this article's ledger
  entry changed. Prior packages, deferred submarine bitmap work, `tocs/` and the
  owner's `.gitignore` edit remain untouched. No issue closeout; stall count 0.
- Mapping took 84.5 seconds; review/build/validation took 1185.3 seconds including
  tool waits. Final cached render/crop and OCR totals were 26.60s and 13.18s.
  These timings do not establish character-perfect proofreading throughput.
  Wrapper, report and manifest total 90 files / 16,262,268 bytes. Closeout,
  validation, browser records, ledger snapshots and next inputs are saved privately.
- Next: `11-batch-19`, 영어학습용 프로그래밍 at PDF121 / printed119. Its displayed
  heading is 영어 학습용 프로그램; retain the existing TOC identity. Verify its
  ending from scans and preserve any listing and figures. Keep the six-source-page,
  six-outside-lookup and one-engine-retry limits; update this log and commit.

### 2026-09-29 — 11-batch-19 started

- Continue toward full Step 11 completion from commit `4e2cd37`. Next is
  영어학습용 프로그래밍, existing `maso-1983-11-toc-0028`, opening at
  PDF121 / printed119. Establish its ending and preserve prose, listing and figures.
- Retain six source pages, six outside lookups and one engine retry per failed
  region. Preserve prior packages and source pins, scan-linked corrections and
  literal code. Deferred bitmap correction and `tocs/` remain outside this batch.

### 2026-09-29 — 11-batch-19 review and validation

- Confirmed complete coverage at PDF121–125 / printed119–123; PDF126 opens the
  Pascal article. Twenty-two regions preserve prose, two figures, the inline730
  example and all201 main numbered rows through3000 END.
- `corrections.json` has202 line ranges, twenty DATA-row records, nine character
  definitions,124 line review notes and five prose review items. Retain printed
  quirks such as WW=WW=2, missing THEN, form and the music-string discrepancy.
- Validation caught a wrapped `1 )` fragment incorrectly indexed as a new row;
  corrected the private indexing helper without changing the transcription.
  Bare target continuation210 within1130 is also retained as part of1130.
  Final count:201 main rows, one inline row,238 physical lines,33 wrapped rows.
- All51 PDF tests pass. The93-file package rebuilds identically;3,743 preserved
  pins, raw OCR, source geometry, all block/line/DATA/glyph ranges and prose joins
  validate. OCR completed22 tasks with20 text outcomes, no failures or retries.
  Browser acceptance and ledger closeout follow.
- Browser acceptance caught omitted visible review notes caused by a reused local
  variable in the private recipe helper. Renamed it, rebuilt and verified that
  package uncertainties/gaps equal all six correction scope notes. No shared
  reader change was needed; the final package is93 files /28,560,616 bytes.

### 2026-09-29 — 11-batch-19 complete

- Restored 영어학습용 프로그래밍 under existing TOC identity
  `maso-1983-11-toc-0028`, PDF121–125 / printed119–123. Displayed title is
  영어 학습용 프로그램. Status is `readable / sample-reviewed`; exact code
  glyphs, string spacing and executable correctness remain unverified.
- Eighteen reading blocks include nine code blocks: one independent inline730
  example and eight main listing regions. The 201 main rows plus one inline row
  occupy 238 physical lines, with 33 wrapped rows. Twenty DATA entries and nine
  DEF CHR$ definitions have exact listing ranges and scans. The original bitmap
  grid and execution example remain images, including the printed form choice.
- `corrections.json` retains eighteen text ranges, nine code-block ranges, 202
  numbered-row ranges, 124 line review notes, five prose review items and eleven
  selected OCR corrections. The source's missing THEN, unusual assignments,
  differing music strings, English grammar and physical word wraps are preserved.
  Neither BASIC execution nor manual submarine bitmap correction was performed.
- Five source pages and one outside lookup stay within the limits. All 22 crop
  tasks and twenty text OCR outcomes completed without engine failures or retries;
  the completed state resumes unchanged. A private request's incorrect option
  name was fixed before processing; its empty setup directory remains separate.
  No source geometry revision or shared extraction/reader change was needed.
- Final export: 93 files / 28,560,616 bytes, with an independent byte-identical
  rebuild. All 51 PDF tests pass. All 3,743 preserved input pins matched before
  the ledger update. Every source region, raw archive entry, prose join, text/code
  interval, DATA interval and twelve-term character definition validates.
- Background Playwright checks pass at 1440×1000 and 360×800: eighteen DOM blocks,
  two images, 26 asset pins, 202 row ranges, twenty DATA ranges and nine character
  definitions. All six review-scope notes are visible. Eight long code containers
  scroll without page overflow; the short inline example fits. Actual horizontal
  scrolling reaches 500px. The actual 9,929-byte listing download matches and the
  final scan opens at 2228×2152. Desktop bitmap and mobile DATA screenshots were
  inspected under `output/playwright/pdf-11-batch-19/`. Only favicon.ico returned
  404. Browser closed; preview remains at `http://127.0.0.1:4199/`.
- November now has eighteen readable/sample-reviewed articles, two group headings
  and 27 unresolved eligibility decisions. Only this article's ledger entry changed.
  Previous packages, `tocs/`, the owner's `.gitignore` edit and deferred bitmap
  correction remain untouched. Step 11 remains active; no issue closeout yet.
- Mapping took 106.1 seconds; review/build/validation took 3717.8 seconds including
  tool and approval waits. Cached render/crop and OCR totals were 30.53s and
  18.17s. These timings do not establish character-perfect proofreading throughput.
  Wrapper, report and manifest total 97 files / 28,582,755 bytes. Private helpers,
  closeout, validations, browser records, ledger snapshots and next inputs are saved.
- Next: `11-batch-20`, 파스칼 프로그램 1(연재), observed PDF126 / printed124.
  Verify the ending independently of the next TOC start, preserve examples and
  illustrations, and split before exceeding six source pages. Continue updating
  this log and committing each checkpoint through Step 11 issue closeout.

### 2026-09-29 — 11-batch-20 started

- Continue Step 11 from commit `69e5288` with 파스칼 프로그램 1(연재),
  `maso-1983-11-toc-0029`, opening at PDF126 / printed124. Verify its extent
  from scans, keeping the six-source-page and six-outside-lookup limits.
- Preserve the previous packages, source pins, printed examples and scan-linked
  corrections. Keep manual bitmap correction deferred and ignore `tocs/`.
  Update this log and commit this checkpoint before proceeding toward closeout.

- Confirmed the six-page article ends with references at PDF131 / printed129;
  PDF132 opens the separate editor article. All eighty regions and seven images
  have been compared with scans. Widened25 tight crop edges in a separate final
  map; original crops and OCR remain saved. Both OCR runs completed without
  engine failures. Final transcription has66 reading blocks,20 distinct code
  examples/templates and134 physical code lines, including two Fortran labels.
- Added six prose joins, one cross-column program join, five formula ranges and
  six reference ranges to corrections.json. Retained printed code, historical
  claims and mathematical typography; no execution or semantic repair. Initial
  build and independent rebuild succeeded. Package validation and background
  desktop/mobile reader acceptance follow before ledger update and commit.

### 2026-09-29 — 11-batch-20 complete

- Restored 파스칼 프로그램 1(연재), existing TOC identity
  `maso-1983-11-toc-0029`, across PDF126–131 / printed124–129. Display title is
  파스칼 프로그래밍 1. Availability is `readable`, verification `sample-reviewed`;
  exact code glyphs, spacing and executable correctness remain unverified.
- Eighty regions yield66 reading blocks and seven original images: two facing-page
  illustration fragments and five syntax diagrams. Twenty separately identified
  examples/templates contain134 physical code lines in Pascal, BASIC and Fortran.
  The two printed Fortran100 labels remain distinct from physical line ordinals.
- corrections.json retains66 text ranges,20 code-block ranges,134 line ranges,
  22 line notes, five prose notes, five formula ranges, six reference ranges and
  twelve selected OCR corrections. Six prose joins and the converter's column
  join retain original regional text. Only the read-/number joining hyphen is
  removed across a region boundary; physical code wraps remain visible.
- Printed END;, Single roots is, WHILE-END, reversed comment braces and the
  value/scale explanation remain visible with review notes. Mathematical glyphs
  and typeset formulae have readable Unicode transcriptions linked to scans.
  Source claims, reference details and program semantics were not repaired.
- Six source pages and one outside lookup satisfy checkpoint limits. Initial and
  final OCR states each completed80 crop tasks/73 text outcomes without engine
  failures or retries. Twenty-five edge revisions used a separate final map;
  only those tasks were reprocessed. Both completed states resume unchanged.
  Reused202 scan/OCR artifacts match;49 settings differ only in their map hash.
- The310-file package is31,357,253 bytes and rebuilds byte-identically. All51 PDF
  tests pass. All4,560 preserved input pins matched before ledger update. Source
  geometry, complete regional coverage, raw archive bytes, joins and every
  text/code/line/formula/reference range validate.
- Background browser checks pass at1440×1000 and360×800:66 DOM blocks, seven
  images,84 asset pins and all correction indexes. All six review scope notes
  appear. Eleven long code containers scroll without page overflow; actual
  converter scrolling reaches390px. Downloaded listing.txt matches3,382 bytes;
  the final reference scan opens at897×666. Desktop diagram and mobile code
  screenshots were inspected under output/playwright/pdf-11-batch-20/. Only
  favicon.ico returned404. Browser closed; preview is http://127.0.0.1:4200/.
- November now has nineteen readable/sample-reviewed articles, two group headings
  and26 unresolved eligibility decisions. Only0029 changed. Previous packages,
  tocs/, the owner's .gitignore edit and deferred bitmap correction remain intact.
  This completes the Pascal checkpoint, not Step11 or the issue closeout.
- Mapping took152.6s; review/build/validation took1210.2s including interrupted
  turn, tool and approval waits. Final cached render/crop and OCR totals are
  63.49s and32.90s; these are not character-perfect proofreading throughput.
  Wrapper/report/manifest total314 files /31,417,723 bytes. Helpers, correction
  evidence, validation, browser records and next inputs are saved privately.
- Next:11-batch-21, 에디터를 만드는 법, observed PDF132 / printed130. Establish
  its extent from scans and use disjoint numbered segments if longer than six
  pages. Continue through every November entry and the separate issue closeout.

### 2026-09-29 — 11-batch-21 started

- Continue Step 11 from commit `cdf2f7e` with 에디터를 만드는 법,
  `maso-1983-11-toc-0030`, opening at PDF132 / printed130. This checkpoint
  includes at most PDF132–137; inspect up to six outside pages to establish
  the article ending. Use a numbered partial segment if coverage exceeds six
  source pages, then assemble separately after the remaining segment is reviewed.
- Preserve prior packages, raw OCR, printed examples and source-linked corrections.
  Keep bitmap correction deferred and ignore `tocs/`. Update this log during work
  and commit each finished checkpoint before proceeding toward issue closeout.

- Scans establish the full article at PDF132–140 / printed130–138, ending at
  BASIC1300 above an advertisement. PDF141 opens MICRO COMPUTER GRAPHIC.
  This segment retains PDF132–137; three pages are deferred, not missing.
- All 42 mapped regions were inspected. Six crops were refined to retain diagram
  labels/edge glyphs and separate the first caption from following prose. Both
  OCR passes completed with no engine failures. The first segment has 26 reading
  blocks, ten diagrams and 32 BASIC rows (10–320) across 37 physical lines.
- corrections.json records six prose joins, 32 line ranges, 18 line notes,
  twelve prose review points and ten selected OCR corrections. Printed variable
  names, diagram references, decorative strings and G/OTO wrapping are preserved.
  Initial build and independent rebuild succeeded; validation and background
  desktop/mobile checks follow before the partial outcome is recorded and committed.

### 2026-09-29 — 11-batch-21 complete

- Restored editor segment 01 under existing identity `maso-1983-11-toc-0030`,
  에디터를 만드는 법, PDF132–137 / printed130–135. Availability remains
  `partial`, verification `sample-reviewed`. The full nine-page extent is verified;
  PDF138–140 are deferred to the next segment, followed by separate assembly.
- Forty-two regions yield 26 reading blocks and ten original diagrams/captions:
  figures 1–8 and 3-1/3-2. The prose covers design, linked lists, the storage pool
  and commands through INSERT. BASIC10–320 has 32 numbered rows across 37 physical
  lines. Rows30,160,180,190 wrap; G/OTO remains physically split in180.
- corrections.json retains 26 text ranges, one code-block range, 32 line ranges,
  18 line notes, twelve prose review points and ten selected OCR corrections.
  Six cross-column/page prose joins preserve their original regional text.
  Printed SPC-100, Responce, repeated figure4-(a), &HZD and differing variable
  references remain reviewable. No code execution or semantic repair was done.
  Exact glyphs, decorative symbol counts and string spaces remain unverified.
- Six source pages and four outside lookups satisfy checkpoint limits. Initial
  and final OCR states completed all 42 crops and 32 text outcomes without engine
  failures or retries. Six revised crops used a separate final map; only those
  tasks were reprocessed. Both states resume unchanged. Reused 126 scan/OCR files
  match; 30 settings differ only in the map/package hash.
- The 149-file segment package is 30,971,394 bytes and rebuilds byte-identically.
  All 51 PDF tests pass. All 6,748 preserved input pins matched before the ledger
  update. Source geometry, every mapped region, raw archive bytes, text and code
  ranges, physical line fragments and prose joins validate.
- Background browser checks pass at 1440×1000 and 360×800: 26 DOM blocks, ten
  images, 46 asset pins and all correction ranges. All six scope notes and partial
  status are visible. Long code scrolls without page overflow; actual scrolling
  reaches 500px. Downloaded listing.txt matches 1,367 bytes; the final prose scan
  opens at 869×495. Desktop buffer-diagram and mobile-code screenshots were
  inspected under output/playwright/pdf-11-batch-21/. Only favicon.ico returned
  404. Browser closed; preview remains http://127.0.0.1:4201/.
- November now has nineteen readable articles, one partial article, two group
  headings and 25 unresolved eligibility decisions. All twenty classified articles
  are sample-reviewed. Only0030 changed. Earlier packages, tocs/, the owner's
  .gitignore edit and deferred bitmap correction remain intact. No issue closeout.
- Mapping took 152.5s; review/build/validation took 1047.3s including tool/approval
  waits. Final cached render/crop and OCR totals are 46.96s and 29.65s. These do
  not establish character-perfect proofreading throughput. Wrapper/report/manifest
  total 153 files / 31,006,204 bytes. Helpers, validation, correction evidence,
  browser records, ledger snapshots and next inputs are saved privately.
- Next: 11-batch-22, editor segment 02, PDF138–140 / printed136–138. Preserve the
  DELETE/OUTPUT explanations and closing, diagrams3-3/3-4 and BASIC330–1300.
  Exclude the advertisement below the final listing. Assemble the article in a
  separate checkpoint, then continue the November queue and issue closeout.

### 2026-09-29 — 11-batch-22 started

- Continue Step 11 from `1153800` with editor segment 02, PDF138–140 /
  printed136–138, under existing TOC identity `maso-1983-11-toc-0030`.
  Reuse pinned boundary evidence; preserve DELETE/OUTPUT explanations, closing,
  diagrams3-3/3-4 and BASIC330–1300. Exclude the advertisement on PDF140.
- Preserve segment 01 and prior packages. Validate this segment and commit its
  checkpoint before separate article assembly. Keep bitmap correction deferred
  and ignore `tocs/` as requested.

- Mapped and inspected all twelve regions on the final three pages: six prose,
  two figures and four code crops. OCR completed all twelve tasks / ten text
  outcomes without failures. Figures3-3/3-4 and their captions are intact;
  running headings and the lower-page advertisement are excluded.
- Transcribed 98 numbered BASIC rows330–1300 across103 physical lines, preserving
  wraps in490/500/550/570. Two cross-column prose joins retain regional text.
  corrections.json includes98 line ranges,50 line notes,three prose review items
  and ten selected OCR corrections. The uncertain400 variable is provisionally
  TE; printed glyphs, spacing and source behavior remain manual review targets.
- The53-file segment package rebuilds byte-identically. All51 PDF tests pass,
  all7,808 preserved input pins match, and completed OCR resumes unchanged.
  Browser checks are underway before recording the partial outcome and commit.

### 2026-09-29 — 11-batch-22 complete

- Restored editor segment02, PDF138–140 / printed136–138, with DELETE/OUTPUT
  explanations, closing, figures3-3/3-4 and98 BASIC rows330–1300. All12 regions
  are represented in eight reading blocks and two original diagrams. Physical
  wraps and printed quirks remain visible and linked to correction evidence.
- The53-file package is13,190,987 bytes and rebuilds identically. All51 PDF tests
  pass. Checks validate source geometry, raw archive bytes, every region, two
  prose joins, eight text ranges, four listing ranges and98 numbered-row ranges.
  All7,808 preserved input pins matched before the ledger update. The completed
  OCR state resumes unchanged;12 crop tasks/10 text outcomes, no failures/retries.
- Background browser checks pass at1440×1000 and360×800 for all blocks, diagrams,
  16 asset pins, correction ranges and six scope notes. Four code blocks scroll
  without page overflow; actual scrolling reaches500px. The3,410-byte download
  matches. The final scan opens at2204×1520. The initial desktop screenshot
  preceded paint; a fresh settled screenshot and mobile screenshot were inspected.
  Only favicon.ico returned404. Browser closed; preview http://127.0.0.1:4202/.
- Both disjoint editor segments now cover all nine observed pages; availability
  remains partial/sample-reviewed until separate assembly. November counts stay
  nineteen readable, one partial, two headings and25 unresolved eligibility
  decisions. Only0030 changed; prior packages, tocs/, the owner's .gitignore edit
  and deferred bitmap correction remain intact. No issue closeout.
- Mapping took236.9s; review/build/validation647.2s including waits. Cached render/
  crop17.00s and OCR8.04s do not establish character-perfect proofreading speed.
  Wrapper/report/manifest total57 files /13,207,537 bytes. Private helpers,
  validation, browser records, ledger snapshots and next inputs are saved.
- Next:11-editor-assemble, using the two immutable segments without new OCR.
  Validate PDF132–140 and BASIC10–1300, resolve superseded partial-scope notes,
  and inspect the combined reader before continuing to MICRO COMPUTER GRAPHIC.

### 2026-09-29 — 11-editor-assemble started

- Assemble both immutable editor segments from `e6d5cd5` without new OCR.
  Require complete ordered PDF132–140 / printed130–138 coverage, twelve diagrams,
  BASIC10–1300 and all original evidence. Namespace local correction identities,
  rebase byte ranges, and explicitly resolve four superseded partial-scope notes.
- Preserve printed glyph ambiguities and physical wraps. Validate the combined
  article and desktop/mobile reader before marking0030 readable and committing.
  Continue afterward through the remaining November entries and issue closeout.

- Assembly and independent rebuild succeeded. Complete ordered nine-page
  coverage contains54 regions,34 reading blocks,12 diagrams and five code blocks.
  All130 numbered BASIC rows10–1300 span140 physical lines; eight wrapped rows
  retain exact segment bytes. No cross-segment fragments needed joining.
- All8,064 preserved pins and202 copied original files match. The213-file
  assembled package is66,463,279 bytes. Validation checks188 raw archive members,
  34 text ranges,15 prose review points,130 local/logical line ranges,68 line
  notes and eight prose joins. Four partial-scope notes are explicitly resolved;
  original segment records remain unchanged. No new OCR or source-page processing.
- Reused batch22's immediately preceding51-test pass because tooling is unchanged.
  Combined-reader browser checks follow before the ledger update and commit.

### 2026-09-30 — 11-editor-assemble complete

- Combined both immutable editor segments into one readable/sample-reviewed
  article, PDF132–140 / printed130–138, without new OCR. All54 regions,34 reading
  blocks,12 diagrams and130 numbered BASIC rows are retained in source order.
  The4,777-byte listing is the exact concatenation of the two originals.
- Validation confirms full ordered coverage, byte-identical rebuild,202 copied
  originals,188 raw archive members and8,064 preserved input pins. Every text,
  review and listing range validates. Four superseded scope notes are resolved;
  glyph/spacing/code concerns remain visible. All source packages remain intact.
  The unchanged tooling uses batch22's immediately preceding51-test pass.
- Desktop/mobile browser checks pass for all34 blocks,12 figures,58 pins and
  correction ranges. Five code blocks scroll without page overflow; actual
  scrolling reaches500px. Downloaded listing bytes match; the rebased final scan
  opens at2204×1520. Desktop diagram and mobile code screenshots were inspected.
  Only favicon.ico returned404. Browser closed; preview http://127.0.0.1:4203/.
- Article output totals213 files /66,463,279 bytes; wrapper/report/manifest totals
  217 files /66,508,349 bytes. Assembly/review/validation took289.8s including
  tool waits, with zero new OCR tasks. Private recipes, validation, browser
  records, original segments, ledger snapshots and next inputs are saved.
- November now has twenty readable/sample-reviewed articles, no partial articles,
  two group headings and25 unresolved eligibility decisions. Only0030 changed.
  Step11 remains active. Next:11-batch-23 maps MICRO COMPUTER GRAPHIC beginning
  atPDF141 / printed139; establish the ending locally before extraction.

### 2026-09-30 — 11-batch-23 started

- Continue from `762006e` with MICRO COMPUTER GRAPHIC, existing TOC identity0031,
  beginning atPDF141 / printed139. Inspect at mostPDF141–146 for this segment
  and six outside pages147–152 to establish the ending. Use disjoint numbered
  segments when the verified article exceeds six pages; assemble separately.
- Preserve all earlier packages, source diagrams/code and correction evidence.
  Keep bitmap correction deferred and ignore tocs/. Update progress during work
  and commit the completed checkpoint before advancing through the issue queue.

- Scans verify the complete article atPDF141–149 / printed139–147. The following
  PDF150–151 are full-page advertisements; PDF152 opens 정보레이다. Segment01
  includes141–146, with147–149 deferred. The final phrase 더우기 직선을 continues
  onPDF147 as 그리기 위해서; retain that explicit prose boundary for assembly.
- Initial map contains39 regions, including original address grids, graphics,
  small tables and five BASIC examples. Six included pages and six outside
  lookups satisfy the checkpoint limits. OCR has started; crop/content review,
  transcription, correction indexes and package/browser validation remain.
- Initial OCR completed39 crop tasks /29 text outcomes with no engine failures.
  Evidence export and local OCR bundles are saved. This is extraction progress,
  not a reviewed restoration outcome; the issue ledger is unchanged from the
  completed editor assembly. Detailed crop/transcription review is next.

- Reviewed all39 original crops and eleven refined crops. Expanded tight text
  edges and diagram borders using a separate final map; initial evidence remains
  intact. Both OCR states complete39 tasks /29 text outcomes without failures.
- Transcribed26 reading blocks, including five independent BASIC examples with
  36 numbered rows. Ten figure/table/graphic images retain original labels and
  captions. Three cross-column prose joins preserve regional text. The last
  prose fragment remains explicitly linked to the deferredPDF147 continuation.
- corrections.json records26 text ranges, five listing ranges,36 line ranges,
  15 code notes, eleven prose review points, four figure notes and ten selected
  OCR corrections. Printed COLRS,14366,PRINT TAB punctuation, R/T discrepancy
  and address/coordinate claims remain uncorrected and scan-linked.
- The137-file segment package is38,636,128 bytes and rebuilds byte-identically.
  All51 PDF tests pass; all8,508 preserved pins match. Completed OCR states resume
  unchanged. Browser checks are underway before recording the partial outcome.

### 2026-09-30 — 11-batch-23 complete

- MICRO COMPUTER GRAPHIC segment01 is partial/sample-reviewed across PDF141–146
  / printed139–144. The verified nine-page article continues through PDF149.
  Its39 regions contain26 reading blocks, ten original figures/tables/graphics
  and five independent BASIC examples with36 numbered rows. The final prose
  fragment and three cross-column joins have explicit correction records.
- Both initial/final OCR states complete39 tasks /29 text outcomes without
  failures and resume unchanged. Eleven revised crops were reprocessed while
  unchanged evidence stayed byte-identical. All51 PDF tests pass; all8,508
  preserved pins matched before updating the ledger. The137-file article package
  is38,636,128 bytes and rebuilds byte-identically. Every correction range,
  region, archive, geometry record and listing identity validates.
- Desktop/mobile browser checks pass at1440×1000 and360×800 for26 blocks, ten
  figures,43 pins and correction ranges. Five code blocks scroll without page
  overflow; actual scrolling reaches100px. The802-byte listing download matches;
  the final scan opens at886×321. Desktop diagram and mobile code screenshots
  were inspected. Final scan console has no errors. Browser closed; preview
  http://127.0.0.1:4204/.
- Wrapper/report/manifest total141 files /38,669,426 bytes. Mapping took162.2s;
  review/build/validation1208.4s including interruption and tool waits. Final
  cached render/crop71.948s and OCR17.423s do not certify proofreading speed.
  Private recipes, initial/final evidence, validation, browser records, ledger
  snapshots and next inputs are saved.
- November now has twenty readable, one partial, two headings and24 unresolved
  eligibility decisions. Only0031 changed; previous articles and deferred bitmap
  review remain intact. Next:11-batch-24 restores PDF147–149, links the incoming
  prose fragment, then assembles the article separately. Step11 remains active
  through complete November accounting and the staged issue export.

### 2026-09-30 — 11-batch-24 started

- Continue from `a363945` with MICRO COMPUTER GRAPHIC segment02, PDF147–149 /
  printed145–147. Preserve the first segment and link its outgoing prose to
  「그리기 위해서」. Map the final three pages immediately before extraction;
  retain the following advertisement/boundary evidence from batch23.
- Review printed HCOLOR, animation and memory-copy examples, including wraps,
  marginal annotations and original tables. Keep complete availability deferred
  until separate assembly validates all nine pages. Step11 remains active.

- All32 initial crops and two expanded code crops have been reviewed. Initial
  and final OCR each complete32 tasks /27 text outcomes without failures; only
  the two revised regions required new work. Raw evidence remains immutable.
- Restored25 reading blocks, five original figures/tables and nine code blocks.
  Corrections index52 numbered rows, seven unnumbered commands, four ellipsis
  rows, two wrapped numbered rows and the Korean marginal annotations. Printed
  HPOLT,CONTOL,$0056/$00E6 and the absent150 line remain visible and uncorrected.
- Assembly projection now accepts explicitly identified unnumbered physical rows
  without treating them as carried numbered statements. Two focused tests cover
  mixed numbered/unnumbered content, UTF-8 ranges and invalid continuation claims.
  All53 PDF tests pass. A real two-segment projection preserves99 indexed rows,
  all eleven unnumbered rows and the linked prose boundary.
- The124-file package is17,919,256 bytes and rebuilds byte-identically. All9,157
  preserved input pins match. Completed OCR states resume unchanged; every
  correction range, source geometry record, archive member and region validates.
  Browser review follows before recording the second segment and committing.

### 2026-09-30 — 11-batch-24 complete

- The final three-page segment is partial/sample-reviewed. Both immutable
  segments now cover PDF141–149 / printed139–147, awaiting separate assembly.
  Segment02 has25 reading blocks, five figures/tables, nine code blocks,52
  numbered rows and eleven unnumbered rows over67 physical lines.
- All53 PDF tests pass, including the new explicit unnumbered-row projection
  cases. Rebuild is byte-identical; all9,157 preserved pins and every region,
  archive, source geometry, correction range and prose join validate. Initial
  and final OCR states resume unchanged; two revised crops retain prior evidence.
- Desktop/mobile checks pass at1440×1000 and360×800 for25 blocks, five figures,
  36 pins and all correction ranges. Six code blocks need horizontal scrolling;
  actual animation-code scrolling reaches151px without page overflow. The1,640
  byte listing download matches; the closing scan opens at852×208. Desktop table
  and mobile code screenshots inspected. Only favicon.ico returned404. Browser
  closed; preview http://127.0.0.1:4205/.
- Article package:124 files /17,919,256 bytes. Wrapper/report/manifest:128 files /
  17,950,935 bytes. Recorded review/build/validation wall time1519.9s includes
  interruption and tool waits. The2.6s mapping-helper timing excludes earlier
  scan inspection; final cached render/crop33.787s and OCR16.360s are not human
  proofreading throughput. Recipes, review evidence, ledger and next plan saved.
- Counts remain twenty readable, one partial, two headings and24 unresolved
  eligibility decisions. Only0031 changed. Next:11-graphic-assemble validates
  the complete nine-page article, resolves superseded scope notes, and retains
  both original segments. Step11 still requires the remaining queue and closeout.

### 2026-09-30 — 11-graphic-assemble started

- Assemble the two immutable MICRO COMPUTER GRAPHIC segments from `04f286c`
  without new OCR. Require complete ordered PDF141–149 / printed139–147 coverage,
  fifteen figures/tables/graphics,88 numbered rows and eleven unnumbered rows.
- Preserve the five regional prose joins, link the sentence at the segment
  boundary, and resolve four superseded scope notes while retaining all source
  packages and correction evidence. Validate and browser-review before marking
  the article readable and proceeding to 정보레이다.

### 2026-09-30 — 11-graphic-assemble complete

- Complete MICRO COMPUTER GRAPHIC is readable/sample-reviewed across PDF141–149
  / printed139–147. The71 regions produce51 reading blocks, fifteen original
  figures/tables/graphics and fourteen code blocks. Both original packages remain
  immutable; the2,442-byte listing is their exact concatenation without new OCR.
- All88 numbered rows, seven unnumbered commands and four ellipsis rows validate
  over103 physical lines. Two numbered rows retain wraps. Namespaced corrections
  preserve99 local/logical row ranges,41 code notes,22 prose review points, five
  regional prose joins and the linked cross-segment sentence. Seven figure notes
  remain in original segment metadata. Four superseded scope notes are resolved.
- Rebuild is byte-identical; all10,030 protected pins,261 copied originals and247
  raw archive members match. Full ordered page coverage and every text/listing
  range validate. Tooling is unchanged since batch24's successful53-test run.
- Desktop/mobile checks pass at1440×1000 and360×800 for51 blocks, fifteen figures,
  75 pins and all correction ranges. Eleven code blocks scroll on mobile without
  page overflow; animation code reaches151px. Download bytes match; the rebased
  final scan opens at852×208. Desktop boundary/figure and mobile code screenshots
  were inspected. Only favicon.ico returned404. Browser closed; preview
  http://127.0.0.1:4206/.
- Article output totals272 files /85,028,522 bytes; wrapper/report/manifest totals
  276 files /85,085,822 bytes. Assembly/review/validation took221.1s including
  tool waits, with no new source-page processing. Recipes, validation, browser
  records, ledger snapshot and next inputs saved.
- November now has twenty-one readable/sample-reviewed articles, no partial
  articles, two headings and24 unresolved eligibility decisions. Only0031 changed.
  Next:11-batch-25 maps 뉴스모음 : 정보레이다 from PDF152 / printed150. Step11
  continues through all47 classifications, eligible outcomes and issue closeout.

### 2026-09-30 — 11-batch-25 started

- Continue from `6f51928` with 뉴스모음 : 정보레이다, existing TOC identity0032,
  beginning PDF152 / printed150. Inspect up to six included pages152–157 and
  local boundary lookups158–160 before deciding complete versus segmented scope.
- Preserve news subheadings and photographs under the existing TOC body owner;
  do not create extra unlisted articles. Keep prior packages and correction
  evidence intact, with the owner's bitmap post-production still deferred.

- Scans establish the news text at PDF152–158 / printed150–156. The first six
  pages are mapped as32 regions including ten photographs/illustrations; the
  final interview and Aram report on PDF158 are deferred to segment02. There
  is no sentence fragment at this segment boundary.
- PDF159 is an uncaptioned full-page photograph with no established association
  to the news body; its scan remains boundary evidence outside the package.
  PDF160 / printed158 opens VISICALC활용1. No new TOC article is introduced.
- Prepared32 OCR tasks within the six-source-page and three-lookup-page limits.
  Extraction is running; crop review, transcription, corrections and package
  validation remain before the issue ledger can record a restoration outcome.

- Initial OCR completed all32 tasks /22 text outcomes without failures. Saved
  the evidence export and local OCR bundles. This is extraction progress only;
  detailed crop/transcription review is next and the issue ledger remains at
  the completed graphics assembly (twenty-one readable articles).

- Inspected all32 initial crops and transcribed all22 text regions. Preserve
  ten original photos/illustrations, including the printed children-photo caption.
  Three joined prose blocks will retain five column/page-boundary transitions.
- Five initially uncertain passages have explicit scan-linked markers, including
  gutter-obscured words, a price and a name. Printed product specifications and
  historical claims are preserved rather than reconciled with modern knowledge.
- Seven tight/gutter-affected prose crops are being expanded and rendered at4000
  pixels for a second inspection. Initial map and evidence remain immutable.

- All seven revised crops are now inspected. The refined name reads 이범천;
  four unreadable passages remain explicitly marked. Corrections include32
  prose review points, two figure notes,22 selected OCR comparisons and all
  five column/page transitions in three joined blocks.
- The first segment builds as partial/sample-reviewed with17 reading blocks
  and ten original images. A second build is byte-identical; all53 PDF tests
  pass, all10,592 protected file pins match, and text/correction ranges and raw
  OCR preservation validate. Both OCR states resume unchanged. Browser review
  is next before recording the partial outcome and committing this checkpoint.

### 2026-09-30 — 11-batch-25 complete

- 정보레이다 segment01 is partial/sample-reviewed across PDF152–157 /
  printed150–155. Its32 regions produce17 reading blocks and ten original
  photographs/illustrations. Four unreadable passages remain explicit;32 prose
  review points and two figure notes retain manual correction scope. Five
  column/page joins are represented in three blocks with regional text preserved.
- All53 PDF tests pass. Rebuild is byte-identical, all10,592 protected pins match,
  all raw OCR and correction ranges validate, and both OCR states resume unchanged.
  Seven revised crops retain their original evidence; no source code is present.
- Desktop/mobile checks pass at1440×1000 and360×800 for17 blocks, ten figures and
  35 pins without page overflow. The22,147-byte text download matches; the final
  scan opens at1199×2216. Desktop photo/caption and mobile uncertain-price views
  inspected. Only favicon.ico returned404. Browser closed; preview
  http://127.0.0.1:4207/.
- Article package:108 files /60,029,184 bytes. Wrapper/report/manifest:112 files /
  60,055,995 bytes. Mapping117.5s; review/build/validation1104.8s includes tool
  waits and interruption. Final cached render/crop88.099s and OCR30.311s are not
  human proofreading throughput. Recipes, evidence, ledger and next plan saved.
- November now has twenty-one readable articles, one partial article, two
  headings and23 unresolved eligibility decisions. Only0032 changed. Next:
  11-batch-26 restores PDF158 / printed156, then separate news assembly. PDF159
  remains an uncaptioned boundary photo without established article association;
  PDF160 opens VISICALC활용1. Step11 remains active through issue closeout.

### 2026-09-30 — 11-batch-26 started

- Continue from `ce6d325` with the final news page PDF158 / printed156. Preserve
  the software-contest winner interview, portrait and Aram report under the
  existing0032 article. The first segment remains immutable. Both stories end
  on this page; separate assembly follows the final segment's validation.

- Reviewed all eight crops and transcribed seven text regions. Two joins produce
  five reading blocks; the original portrait is preserved. One faint word before
  자신감 remains explicitly marked; eleven scan-linked review points preserve
  names, period wording, program-title wrap, quantities and the historical contact.
- The final-page package builds byte-identically. All53 PDF tests pass; all11,110
  protected pins, raw OCR bytes, source geometry and text/correction ranges match.
  OCR completed eight tasks / seven text outcomes without failure and resumes
  unchanged. Desktop/mobile reader and download/scan checks follow.

### 2026-09-30 — 11-batch-26 complete

- The final news segment is partial/sample-reviewed at PDF158 / printed156,
  with eight regions, five reading blocks and the original interview portrait.
  Both segments cover the verified seven-page article and await separate assembly.
  Eleven text review notes retain one unreadable word and printed period wording;
  two regional joins preserve the interview and Aram reading order.
- All53 PDF tests pass. Rebuild is byte-identical; all11,110 protected file pins,
  raw OCR, source geometry, reading coverage and text ranges validate. OCR state
  resumes unchanged with eight completed tasks, seven text outcomes and no failures.
- Desktop/mobile checks pass at1440×1000 and360×800 for five blocks, one figure,
  eleven pins and correction ranges without page overflow. The3,997-byte text
  download matches; closing scan opens at1149×560. Initial desktop screenshot
  was blank; recaptured after viewport settled and visually inspected. Desktop
  portrait and mobile Aram views pass. Only favicon.ico returned404. Browser
  closed; preview http://127.0.0.1:4208/.
- Article package:39 files /8,774,675 bytes. Wrapper/report/manifest:43 files /
  8,788,261 bytes. Mapping36.6s; review/build/validation413.1s includes tool waits.
  Render/crop7.927s and OCR6.387s are processing timings, not human proofreading
  throughput. Recipes, review evidence, ledger snapshot and next plan saved.
- Counts remain twenty-one readable, one partial, two headings and23 unresolved
  eligibility decisions. Only0032 changed. Next:11-radar-assemble verifies all
  seven pages, eleven original images and five uncertainty markers without OCR.
  Step11 still requires the remaining queue and standalone issue closeout.

### 2026-09-30 — 11-radar-assemble started

- Assemble both immutable news segments from `2083b32` without new OCR. Require
  ordered PDF152–158 / printed150–156 coverage, eleven original images,22 blocks,
  43 text review points and all five unreadable passages. Preserve seven regional
  boundaries in five joins; no cross-segment sentence join is needed. Resolve
  superseded segment-scope notes while retaining original packages and metadata.

### 2026-09-30 — 11-radar-assemble complete

- Complete 정보레이다 is readable/sample-reviewed across PDF152–158 /
  printed150–156. Forty regions produce22 reading blocks and eleven original
  images. All43 text review points and five explicit unreadable passages remain
  scan-linked; five joins preserve seven regional boundaries. Two figure notes
  and five unresolved-text records also remain in original segment metadata.
- Both original packages are unchanged; no new OCR. Four superseded scope notes
  are resolved. PDF159's uncaptioned photograph remains boundary evidence with
  no established news association. The next article begins on PDF160.
- Rebuild is byte-identical; all11,302 protected pins,147 copied originals and135
  raw archive members match. Full ordered page coverage and every text/review
  range validate. Tooling is unchanged since batch26's successful53-test run.
- Desktop/mobile checks pass at1440×1000 and360×800 for22 blocks, eleven figures
  and43 pins without overflow. The26,266-byte text download matches; the rebased
  final scan opens at1149×560. Desktop portrait and mobile segment-boundary views
  inspected. Only favicon.ico returned404. Browser closed; complete preview
  http://127.0.0.1:4209/.
- Article output:157 files /103,067,505 bytes. Wrapper/report/manifest:161 files /
  103,101,384 bytes. Assembly/review/validation took226.0s including tool waits.
  Recipes, validation, browser records, ledger snapshot and next inputs saved.
- November now has twenty-two readable/sample-reviewed articles, no partial
  articles, two headings and23 unresolved eligibility decisions. Only0032 changed.
  Next:11-batch-27 maps VISICALC활용1 and checks the 비즈니스 parent heading locally.
  Step11 continues through the remaining entries and standalone issue closeout.

### 2026-09-30 — 11-batch-27 started

- Continue from `bddaca5` with VISICALC활용1 at PDF160 / printed158 and its
  unresolved 비즈니스 parent heading. Inspect the article boundary locally before
  extraction. Preserve printed spreadsheet commands, diagrams, screens and
  source wording; establish heading/body ownership without adding a TOC body.

- Scans establish complete PDF160–163 / printed158–161 coverage, ending above
  an unrelated typesetting advertisement. PDF164 opens 메일링 프로그램. Saved
  ownership evidence classifies the unpaginated 비즈니스 parent as a group heading.
- Mapped38 regions including eleven original diagrams/tables/screens and seven
  instruction regions. All extraction uses4000-pixel renders. Boxed cell locations
  and circled RETURN/space symbols need explicit transcription conventions;
  printed formula and instruction inconsistencies will remain scan-linked.

- All38 crops inspected, including eleven images and seven instruction regions.
  Transcribed27 text regions into25 blocks, with one prose join and one command
  join. Six command blocks preserve62 transcript rows (one blank separator),
  indexed individually with scan links.21 instruction notes,15 prose review
  points and six figure notes retain printed discrepancies and notation choices.
- No formula correction or execution. Cell boxes become brackets, circled key
  symbols stay Ⓡ/Ⓢ, and source ellipsis marks have explicit transcription notes.
  Printed E8×D7, four [E1]/DC locations and split label/title fragments remain.
- All53 PDF tests pass. Rebuild is byte-identical; all11,634 protected pins, raw
  OCR bytes, source geometry, region coverage and correction/listing ranges
  validate. The38 completed OCR tasks /27 text outcomes resume unchanged with
  no failures. Browser review follows before recording the article and heading.

### 2026-09-30 — 11-batch-27 complete

- VISICALC활용1 is readable/sample-reviewed across PDF160–163 / printed158–161.
  Its38 regions produce25 reading blocks, eleven original diagrams/tables/screens
  and six instruction blocks.62 unnumbered transcript rows include one blank
  separator;21 instruction notes,15 prose review points and six figure notes
  preserve source notation and discrepancies without formula repair or execution.
- Confirmed 비즈니스 as a group heading with no separate body, based on TOC
  hierarchy and independently titled/credited articles. The closing typesetting
  advertisement is excluded. Only0033 and0034 change in the issue ledger.
- All53 PDF tests pass. Rebuild is byte-identical; all11,634 protected pins,
  raw OCR, source geometry, region coverage and text/listing ranges validate.
  The38-task OCR state resumes unchanged with27 text outcomes and no failures.
- Desktop/mobile checks pass at1440×1000 and360×800 for25 blocks, eleven images,
  42 pins and every correction range. Five instruction blocks scroll on mobile;
  actual formula scrolling reaches180px without page overflow. The2,593-byte
  listing download matches; the final command scan opens at992×292. Desktop
  October screen and mobile formula views inspected. Only favicon.ico returned404.
  Browser closed; preview http://127.0.0.1:4210/.
- Article output:130 files /20,608,468 bytes. Wrapper/report/manifest:134 files /
  20,637,175 bytes. Mapping109.0s; review/build/validation574.2s includes tool waits.
  Render/crop25.914s and OCR12.697s are processing timings, not human proofreading
  throughput. Recipes, ownership evidence, validation, ledger and next plan saved.
- November now has twenty-three readable/sample-reviewed articles, no partial
  articles, three headings and21 unresolved eligibility decisions. Next:
  11-batch-28 maps 메일링 프로그램 at PDF164 / printed162. Step11 remains active
  through all47 classifications, eligible outcomes and standalone issue closeout.

### 2026-09-30 — 11-batch-28 started

- Continue from `7fcfe03` with 메일링 프로그램, TOC0035, beginning PDF164 /
  printed162. Inspect up to six included pages164–169 and boundary lookups
  170–172 before deciding segment coverage. Preserve printed BASIC source,
  wraps, original photographs and scan-linked correction scope without execution.

- Scans establish the complete article at PDF164–171 / printed162–169. The
  introduction ends on164; seven listing pages follow, ending at50260 on171.
  PDF172 opens UNIX1. This segment includes164–169;170–171 are deferred.
- Mapped eleven regions, including the opening photo and five full-page listing
  crops. Code renders use6000 pixels because the dot-matrix text becomes faint;
  introductory text/photo use4000. Preserve line4530 across167/168 and the
  outgoing7260 fragment across169/170 with explicit continuation evidence.

- All eleven crops inspected; five listing pages reviewed in fifteen overlapping
  enlarged slices. Nine reading blocks retain the opening photo, joined prose,
  and five code blocks.287 numbered BASIC lines cover349 physical rows, including
  the two-region4530 continuation;7260 remains explicitly outgoing to PDF170.
-68 listing notes, seven prose notes and one figure note preserve printed gaps,
  wraps and discrepancies. Twelve rows contain fifteen split-glyph markers and
  four unreadable markers. No program execution or semantic repair; raw OCR stays
  unchanged. Exact string spaces and decorative symbol counts remain reviewable.
- All53 PDF tests pass. Rebuild is byte-identical; all12,084 protected input pins,
  raw OCR archives, source geometry, region coverage and download/review ranges
  validate. Eleven OCR tasks /ten text outcomes resume unchanged without failures.
  Browser review follows before recording this partial article outcome.

### 2026-09-30 — 11-batch-28 complete

- 메일링 프로그램 segment01 is partial/sample-reviewed across PDF164–169 /
  printed162–167. Eleven regions produce nine blocks, one original photo and
  five code blocks.287 numbered BASIC lines cover349 physical rows. Line4530
  spans two scan regions; outgoing7260 is explicitly incomplete until PDF170.
-68 listing notes, seven prose notes and one figure note retain uncertainties.
  Twelve rows contain fifteen split-glyph and four unreadable markers. Printed
  GOSUB57010, DENAY/SAVEING, numbering gaps and the200 continuation remain;
  neither execution nor semantic repair was attempted.
- All53 PDF tests pass. Rebuild is byte-identical; all12,084 protected pins,
  raw OCR archive bytes, geometry and every text/listing range validate. Eleven
  tasks /ten text outcomes resume unchanged without failures or retries.
- Desktop/mobile checks pass at1440×1000 and360×800 for nine blocks, one photo,
  fifteen pins and all indexed ranges. All five code blocks scroll on mobile;
  actual scroll reaches180px without page overflow. The15,270-byte listing
  download matches, and the final scan opens at3289×4699. Desktop photo and mobile
  continuation views inspected. Only favicon.ico returned404. Browser closed;
  preview http://127.0.0.1:4211/.
- Article output:52 files /62,058,798 bytes. Wrapper/report/manifest:56 files /
  62,074,908 bytes. Mapping131.9s; review/build/validation1196.5s includes
  interruption, context recovery and tool waits. Processing:render/crop63.654s,
  OCR27.375s; these are not character-perfect proofreading throughput.
- Only0035 changed in the ledger. November now has23 readable articles, one
  partial article, three headings and20 unresolved eligibility decisions.
  Next11-batch-29 restores the final two pages170–171 with incoming7260, followed
  by a separate immutable assembly. Step11 and standalone issue closeout remain.

### 2026-09-30 — 11-batch-29 started

- Continue from `5bbac2d` with the final two mailing-program listing pages,
  PDF170–171 / printed168–169. Lookup scans confirm incoming7260 and final50260;
  PDF172 opens UNIX1. Map two full-page code crops at6000 pixels, excluding
  running titles. Preserve prior segment and continuation evidence for assembly.

- Both crops inspected in six overlapping enlarged slices. Two code blocks index
  100 newly numbered lines plus incoming7260, covering136 physical rows.47 review
  notes retain printed gaps, OPEN "P", CLOSE : END and faint control-code values.
  Eleven rows contain twenty split-glyph and one unreadable marker. The carried
  fragment pins the preceding segment's exact bytes, manifest and scan evidence.
- Rebuild is byte-identical; all12,293 protected input pins, raw archive members,
  geometry, every listing/text range and prior continuation references validate.
  Two OCR tasks/outcomes resume unchanged without failures. Generic tooling is
  unchanged since batch28's53-test pass. Browser checks precede segment closeout.

### 2026-09-30 — 11-batch-29 complete

- Final mailing-program segment is partial/sample-reviewed across PDF170–171 /
  printed168–169. Two code blocks index100 newly numbered lines plus incoming7260
  over136 physical rows.47 listing notes retain printed source quirks and gaps;
  eleven rows contain twenty split-glyph and one unreadable marker. Final50260
  and the following UNIX1 boundary are verified. No execution or semantic repair.
- Both immutable segments now cover all eight article pages; separate assembly
  remains. The incoming7260 row pins the first segment's manifest, listing,
  corrections and exact prior byte/scan ranges. Original packages remain intact.
- Rebuild is byte-identical; all12,293 protected pins, raw archives, source
  geometry and indexed ranges validate. Two OCR outcomes resume unchanged with
  no failures/retries. Tooling remains unchanged since batch28's53-test pass.
- Desktop/mobile checks pass at1440×1000 and360×800 for both code blocks, six
  pins and101 local line ranges. Both blocks scroll on mobile, including actual
  180px movement without page overflow. The7,191-byte download matches, and the
  final scan opens at3268×4675. Desktop ending and mobile incoming-fragment
  screenshots inspected. Only favicon.ico returned404. Browser closed;
  preview http://127.0.0.1:4212/.
- Article output:19 files /23,855,469 bytes. Wrapper/report/manifest:23 files /
  23,865,708 bytes. Mapping51.3s; review/build/validation636.8s includes tool waits.
  Render/crop24.464s; OCR9.479s. Saved segment manifests, correction metadata,
  validation, ledger snapshot and next assembly inputs.
- Counts remain23 readable articles, one partial article, three headings and20
  unresolved eligibility decisions. Next11-mailing-assemble must preserve387
  logical BASIC lines, all correction notes and both originals, then continue
  with UNIX from PDF172. Step11 issue accounting and standalone closeout remain.

### 2026-09-30 — 11-mailing-assemble started

- Assemble the two immutable mailing-program packages without new OCR. Verify
  PDF164–171 / printed162–169 in source order; preserve one original photo,
  eleven blocks,387 logical BASIC lines,115 listing notes and seven prose notes.
  Link incoming7260 to its exact prior fragment, retain4530's internal two-scan
  mapping and all forty uncertainty markers. Resolve four superseded scope notes.

- Complete eight-page assembly builds as readable/sample-reviewed. Thirteen
  regions produce eleven blocks, seven code blocks and one photo.387 logical
  lines span388 local records /485 physical rows. All115 listing notes, seven
  prose notes and forty uncertainty markers remain;23 unresolved-row records
  stay in original metadata. Four superseded scope notes are resolved.
- Rebuild is byte-identical; all12,395 protected pins,71 copied original files,
  57 raw archive members, full page order and every correction range validate.
  The7260 logical row joins two immutable source fragments;4530 retains its
  within-segment two-scan mapping. No new OCR or generic tooling changes.

### 2026-09-30 — 11-mailing-assemble complete

- Complete 메일링 프로그램 is readable/sample-reviewed across PDF164–171 /
  printed162–169. Thirteen regions produce eleven blocks, one original photo and
  seven BASIC code blocks.387 logical lines cover388 local records /485 physical
  rows.115 listing notes and seven prose notes preserve all printed uncertainties.
- Both original packages remain unchanged. Line7260 joins two immutable segment
  fragments;4530 retains its internal two-scan mapping. Four superseded scope
  notes are resolved.35 split-glyph and five unreadable markers remain visible;
  all23 unresolved-row records and the photo note stay in original metadata.
  No program execution, semantic repair or new OCR was performed.
- Rebuild is byte-identical; all12,395 protected pins,71 copied original files,
  57 raw archive members, full page coverage and every text/listing/review range
  validate. Generic tooling is unchanged since batch28's successful53-test run.
- Desktop/mobile checks pass at1440×1000 and360×800 for eleven blocks, one photo,
  seventeen pins and all387 logical line ranges. Seven code blocks scroll on
  mobile, with actual180px movement and no page overflow. The22,461-byte listing
  download matches; the rebased final scan opens at3268×4675. Desktop photo and
  mobile7260 boundary views inspected. Only favicon.ico returned404. Browser
  closed; complete preview http://127.0.0.1:4213/.
- Article output:82 files /129,466,289 bytes. Wrapper/report/manifest:86 files /
  129,486,219 bytes. Assembly/review/validation264.4s includes tool waits.
  Saved recipe, validation, browser evidence, ledger snapshot and next inputs.
- Only0035 changed. November now has24 readable/sample-reviewed articles, no
  partial articles, three headings and20 unresolved eligibility decisions.
  Next11-batch-30 maps UNIX 1(연재) at PDF172 / printed170. Step11 remains active
  through the remaining classifications, eligible outcomes and issue closeout.

### 2026-09-30 — 11-batch-30 started

- Continue from `f276a08` with UNIX 1(연재), TOC0036, starting PDF172 /
  printed170. Inspect local page boundaries through the next TOC start at
  printed177 before choosing coverage within the six-page batch ceiling.
  Preserve period terminology, diagrams and printed claims without factual repair.

- Boundary scans establish PDF172–178 / printed170–176 as the complete article;
  PDF179 starts 마이티용 순서배열 프로그램. This segment covers172–177, with final
  page178 and its table deferred. Mapped41 regions at4000 pixels, including ten
  original explanatory cartoons and their separately transcribed captions.
- Column/page joins require explicit tracing, especially PDF176's sentence
  interrupted by cartoons and the outgoing 점/점 continuation at177/178. Preserve
  source spelling, model names, period claims and small mathematical notation.

- All41 crops inspected; four clipped text/figure edges widened and reinspected.
  Original map/extraction remain intact. The repair reused37 cached regions and
  processed four changed crops without failures; the caption inr14 deliberately
  overlaps its separate transcription without erasing original image content.
- Six pages build with22 blocks, ten cartoons,31 regional transcriptions and five
  section joins spanning13 boundaries. Every regional byte maps to one reading
  block;30 prose notes preserve names, period claims, the small summation formula
  and two provisional readings. Final178/table and full assembly remain.

### 2026-09-30 — 11-batch-30 complete

- First UNIX segment is partial/sample-reviewed across PDF172–177 / printed170–175.
  Forty-one regions retain ten original cartoons,31 regional transcriptions and
  22 reading blocks. Five section joins span13 column/page boundaries; regional
  UTF-8 parts partition every transcribed byte exactly once. Final178/table remain.
- Thirty prose review notes retain period names, specifications, historical claims,
  Coporation, BBM, FOAMT and the small summation formula. Two provisional readings
  remain scan-linked: 사용시가 and the176/177 boundary 부작시켰을때. The widened
  general-purpose cartoon retains its caption alongside separate transcription.
- Initial41 tasks and repaired41-task state resume unchanged. Four repaired crops
  were reinspected;37 unchanged crops match the originals and were cache hits.
  All31 text OCR outcomes and original maps/extractions remain preserved; no
  failures/retries. Final cached render/crop44.925s and OCR33.946s include reused
  processing, not just repair runtime. No historical or semantic repair.
- Rebuild is byte-identical; all12,577 protected pins,135 raw archive members,
  source geometry, all text/review ranges and regional byte partitions validate.
  Generic tooling is unchanged since batch28's successful53-test run.
- Desktop/mobile checks pass at1440×1000 and360×800 for22 blocks, ten cartoons,
  44 asset/download pins and all30 review ranges. No page overflow. Downloaded
  article.txt matches22,170 bytes; final scan opens at796×3180. Desktop cartoon
  and mobile prose screenshots inspected. Only favicon.ico returned404. Browser
  closed; preview http://127.0.0.1:4214/.
- Article output:144 files /41,592,160 bytes. Wrapper/report/manifest:148 files /
  41,624,964 bytes. Mapping143.5s; review/build/validation1262.4s includes waits
  and interruption. Saved recipe, validation, ledger snapshot and next inputs.
- Only0036 changed. November has24 readable articles, one partial article, three
  headings and19 unresolved eligibility decisions. Next11-batch-31 restores
  PDF178 / printed176, preserves incoming 점/점 continuation and final table,
  then assembles the seven-page article. Step11 issue closeout remains pending.

### 2026-09-30 — 11-batch-31 started

- Continue from2e321a5 with final UNIX page PDF178 / printed176. The next page
  opens 마이티용 순서배열 프로그램, confirming the seven-page article boundary.
- Mapped eight regions: six text/caption regions and two original images (versions
  table and XENIX cartoon). Trace incoming 점/점, internal 판매하/게 and 소/유자
  joins. Preserve period licensing/version claims and original table cells.

- All eight crops inspected, including table cells and cartoon lettering; three
  tight crop edges widened and reinspected. Final extraction reused five cached
  regions and processed three changes with no failures. Initial evidence remains.
- Five reading blocks preserve all six regional transcriptions and both original
  images. Fifteen prose notes and two image notes retain printed spelling/claims.
  Incoming continuation pins prior manifest, article bytes, corrections and scan;
  two within-page joins preserve exact regional byte partitions.

### 2026-09-30 — 11-batch-31 complete

- Final UNIX page is partial/sample-reviewed at PDF178 / printed176. Eight
  regions retain six text/caption transcriptions, five reading blocks, the
  original six-row version table and XENIX cartoon. Fifteen prose notes and two
  figure notes retain printed spelling, version/licensing/pricing claims and
  table cells. No contemporary factual repair or inferred table data.
- Incoming 점/점 pins the first segment's manifest, exact article range,
  corrections and scan. Within-page 판매하/게 and 소/유자 joins retain exact
  regional byte partitions; the final sentence and next article boundary verify.
  Both immutable segments cover all seven pages; separate assembly remains.
- Three tight crop edges widened and reinspected. Five unchanged crops match
  originals and used cache; three changed tasks completed without failures.
  Initial and final eight-task states resume unchanged. Both maps/extractions
  remain preserved; six OCR text outcomes, no retries.
- Rebuild is byte-identical; all13,262 protected pins,27 raw archive members,
  geometry, regional partitions, text ranges and incoming evidence validate.
  Generic tooling remains unchanged since batch28's53-test pass.
- Desktop/mobile checks pass at1440×1000 and360×800 for five blocks, two images,
  eleven pins and15 review ranges, with no page overflow. The3,440-byte article
  download matches; final scan opens at806×2228. Desktop table and mobile
  licensing text screenshots inspected. Browser closed; preview4215.
- Browser launcher initially failed sandbox DNS. An early harness ran on the
  wrapper and got article.json404; that failure is preserved. Navigation rerun
  with approved access and all article checks passed. Favicon.ico404 also logged.
- Article output:36 files /7,034,843 bytes. Wrapper/report/manifest:40 files /
  7,048,721 bytes. Recorded mapping-script time0.3s excludes prior scan/planning;
  review/build/validation571.0s includes tool/approval waits. Final cached
  render/crop10.154s and OCR5.520s include reused work, not only repair runtime.
- Counts remain24 readable articles, one partial, three headings and19 unresolved
  eligibility decisions. Next11-unix-assemble must preserve27 blocks, twelve
  original images,45 prose notes, two provisional readings and both originals,
  then continue from PDF179. Step11 issue accounting and closeout remain.

### 2026-09-30 — 11-unix-assemble started

- Assemble two immutable UNIX segments without new OCR. All seven source pages
  PDF172–178 / printed170–176 build as readable/sample-reviewed with27 blocks,
  eleven cartoons and one version table. Retain45 prose notes, two provisional
  readings, the caption overlap and exact regional byte partitions.
- Incoming 점/점 links adjacent reading blocks; seven within-segment joins span
  fifteen boundaries. Four superseded partial-scope notes are resolved while
  both original packages and their correction metadata remain unchanged.

### 2026-09-30 — 11-unix-assemble complete

- Complete UNIX 1(연재) is readable/sample-reviewed across PDF172–178 / printed
  170–176. Forty-nine regions produce27 reading blocks, eleven original cartoons
  and one version table. All45 prose review notes remain; five figure notes and
  two provisional-reading records stay in original segment metadata.
- Both original packages remain unchanged. All37 regional transcriptions have
  exact byte partitions into reading blocks. Seven prose joins span15 boundaries;
  incoming 점/점 links adjacent blocks without rewriting their text. Original
  caption overlap remains explicit. Four superseded scope notes are resolved.
  No new OCR or historical/technical repair.
- Rebuild is byte-identical; all13,513 protected pins,180 copied original files,
  168 raw archive members, full page coverage and every text/review range verify.
  Generic tooling remains unchanged since batch28's successful53-test run.
- Desktop/mobile checks pass at1440×1000 and360×800 for27 blocks, twelve images,
  52 pins,45 prose review ranges and the linked continuation. No page overflow.
  The25,743-byte article download matches; rebased final scan opens at806×2228.
  Desktop table and mobile segment boundary screenshots inspected. Only
  favicon.ico returned404. Browser closed; complete preview http://127.0.0.1:4216/.
- Article output:190 files /72,835,968 bytes. Wrapper/report/manifest:194 files /
  72,875,502 bytes. Assembly/review/validation212.1s includes tool waits. Saved
  assembly recipe, validation, browser evidence, ledger snapshot and next inputs.
- Only0036 changed. November now has25 readable/sample-reviewed articles, no
  partial articles, three headings and19 unresolved eligibility decisions.
  Next11-batch-32 maps 마이티용 순서배열 프로그램 from PDF179 / printed177.
  Step11 remains active through remaining classifications, outcomes and closeout.

### 2026-09-30 — 11-batch-32 started

- Continue from0976743 with 마이티용 순서배열 프로그램, TOC0037. Local scans
  confirm two article pages PDF179–180 / printed177–178; PDF181 starts 프로그램
  제너레이터. Mapped19 regions including three BASIC listings, three sample
  outputs, the original photo and insertion-sort diagram.
- Preserve printed program2/3 caption/type discrepancies and all source code
  without execution. Trace first-column FLAG wrap and the 삽입법/이 끝난다.
  continuation across the second page's diagram/listing placement.

- All19 crops inspected, including every listing/output and both figures. Three
  clipped/tight edges widened and reinspected;16 unchanged tasks reused cache.
  Initial maps/extractions preserved; all19 tasks complete without failures.
- Complete article builds with14 reading blocks, six code/output blocks and two
  figures. Indexes distinguish89 numbered BASIC lines from26 sample-output rows
  across118 physical rows.28 listing notes, ten prose notes and two figure notes
  preserve type/caption mismatches, ELVIES, wraps and provisional punctuation.

### 2026-09-30 — 11-batch-32 complete

- Complete 마이티용 순서배열 프로그램 is readable/sample-reviewed across
  PDF179–180 / printed177–178. Nineteen regions produce14 blocks, six code/output
  blocks and two original figures. Three BASIC programs have89 numbered rows;
  three samples have26 unnumbered output rows,118 physical rows total.
- Twenty-eight listing notes, ten prose notes and two figure notes retain the
  program2/3 string/numeric caption mismatch, printed THEN/GOTO distinctions,
  ELVIES, wrapped ELSE lines, blank rows and a provisional comma-like mark after
  program1's260. Three prose joins retain column/page continuity. No execution
  or semantic repair; source wording and examples remain available for review.
- Three crop edges repaired and reinspected;16 unchanged regions match originals
  and used cache. Initial/final19-task states resume unchanged with17 text OCR
  outcomes and no failures/retries. An early export was correctly rejected by
  the live OCR lock; no artifact was created, and export succeeded after completion.
- Rebuild is byte-identical; all13,911 protected pins,71 raw archive members,
  geometry, text ranges and all115 indexed listing/output rows validate. Generic
  tooling remains unchanged since batch28's successful53-test run.
- Desktop/mobile checks pass at1440×1000 and360×800 for14 blocks, two images,
  23 pins and all115 row ranges. Four code/output blocks scroll on mobile; actual
  135px code scrolling verified with no page overflow. Article6,934-byte and
  listing2,190-byte downloads match. Final output scan opens at1157×610.
  Desktop diagram and mobile code/scroll screenshots inspected. Only favicon.ico
  returned404. Browser closed; preview http://127.0.0.1:4217/.
- Article output:81 files /16,232,361 bytes. Wrapper/report/manifest:85 files /
  16,253,628 bytes. Mapping76.9s; review/build/validation750.9s includes tool waits.
  Final cached render/crop40.132s and OCR11.322s include reused work, not only
  repair runtime. Saved recipe, validation, ledger snapshot and next inputs.
- Only0037 changed. November now has26 readable/sample-reviewed articles, no
  partial articles, three headings and18 unresolved eligibility decisions.
  Next11-batch-33 maps 프로그램 제너레이터 from PDF181 / printed179. Remaining
  classifications, article outcomes and standalone issue closeout keep step11 active.
