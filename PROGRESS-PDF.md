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
