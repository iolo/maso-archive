# TOC restoration plan

Status: complete. Catalog records remain unchanged. See the implementation
checkpoint and final completion audit below for verified results and limitations.

Implement [PRD-tocs.md](PRD-tocs.md) by normalizing the donated TOC filenames,
comparing their printed contents with `TOC.md`, and displaying reduced images
in the reading room. Preserve the donated image bytes and keep originals outside
Git and every served directory. OCR and visual review may read originals locally;
the PRD's restriction on direct use is interpreted as prohibiting their delivery
to the webapp.

## Source authority and manual corrections

`TOC.md` was manually created from Korean National Library records and is the
authoritative catalog. It takes priority over OCR text from the donated images.
It is shared across restoration tasks and must remain byte-for-byte unchanged
by this workflow. This user clarification supersedes the PRD instruction to
update `TOC.md` when differences are found.

Report mismatches to the user with the existing text, OCR text, visual evidence,
and precise locations. The user will decide and make corrections manually.
Even a visually confirmed difference does not authorize an automated edit,
addition, deletion, or reordering in `TOC.md`. Do not substitute OCR text into
generated catalog records, search metadata, or article associations either.
Image preparation and mismatch reporting can finish without waiting for edits.

## Inspected starting point

- `tocs/` contains 240 JPEGs in 145 issue directories from November 1983 through
  December 1995. The directory totals 1,211,748,437 bytes and contains no
  non-image files.
  There are 55 single-page, 85 two-page, and five three-page sets. June 1991 is
  missing. These are file inventory results; page contents have not been reviewed.
- Names currently resemble `8311/Page008.jpg` and `9512/Comm005.jpg`. The first
  sampled images are approximately 4,700 × 6,900 pixels. Filename numbers are
  evidence of source order, not verified printed page numbers.
- `/tocs/`, `/build/`, and `/private/` are already ignored; no TOC images are
  tracked. Preserve the existing working-tree changes, including the completed
  cover work and the user's `.gitignore` edits.
- The documented current TOC import has 122 issues and 5,497 entries through
  December 1993. All 24 later issue directories are present among the donations.
  Retain the existing June 1991 transcription and mark it as lacking donated
  scan verification.
- `src/maso_archive/toc.py` supports stable identities and explicit correction
  decisions. Changed text, removals, and ambiguous duplicates need decisions
  tied to the updated source hash; see [TOC import](docs/TOC-IMPORT.md).
- `tools/reading_room/export.py` requires TOC hashes and issue counts to match
  the CD1 reference manifest. Reimporting a corrected `TOC.md` alone will break
  the existing export. Reviewed article links also come from prepared packages.
- Historical CD1 witnesses have a separate snapshot mechanism in
  `tools/toc_snapshot.py`. Preserve those records and their provenance.
- Pillow and a private pinned Korean/English Tesseract runtime already exist.
  Reuse their image and OCR infrastructure where practical; the PDF package
  contract itself is not appropriate for loose donated JPEGs.
- The frontend displays structured TOCs but has no TOC image collection.
  The CD1, aggregate, and PDF scan export paths all need integration checks.

## Proposed conventions

These are implementation defaults where the PRD leaves a choice open.

- Flatten accepted images to `tocs/YYMM-NN.jpg`. Use a two-digit sequence starting
  at `01` for every issue, including single-page TOCs. Record any verified printed
  page number separately, avoiding confusion between scan and printed numbering.
- Establish order from the existing numeric suffixes, then verify visually for
  each issue. Do not guess issue identity or order when evidence conflicts.
  An undated page may retain its donor-supplied issue label for reversible
  filename normalization when no evidence conflicts. Record that provenance
  privately and disclose the unverified date in the viewer/report; the filename
  does not establish a verified publication date. Conflicting labels or uncertain
  path mappings still prevent normalization completion.
- Keep inventories, rename journals, OCR output, crops, and detailed image
  provenance under ignored `private/toc-restoration/`. Store rebuildable image
  derivatives under ignored `build/toc-images/`.
- Keep a readable mismatch report alongside private OCR evidence and summarize
  its findings to the user. This task does not change `TOC.md`, identity decisions,
  the identity map, or catalog associations. Never commit originals, OCR crops,
  or generated reader assets.
- Produce a small preview bounded by 480 × 720 pixels and a readable view bounded
  by 1600 × 2400 pixels, initially JPEG quality 80 and 85 respectively. Apply
  EXIF orientation, preserve proportions, never upscale, convert consistently to
  RGB, and remove source metadata. Validate legibility in the pilot before
  fixing these settings. Both outputs must be newly encoded derivatives.
- Add an optional ordered `tocImages` collection to issue documents, with
  derivative paths, dimensions, hashes, sequence, and optional printed page.
  Detailed source paths and OCR evidence stay private. Existing catalogs without
  this field continue to load.

## Implementation sequence

### 1. Inventory and normalize source names

- Add a dedicated module such as `tools/toc_restore/` for inventory, normalization,
  OCR comparison, and mismatch reporting. Keep reader asset attachment in
  `tools/reading_room/tocs.py`.
- Inventory every source path, issue, proposed sequence, format, dimensions, byte
  size, and SHA-256. Decode every JPEG to detect corruption. Report missing dates,
  duplicates, invalid issue names, ambiguous ordering, and non-image files.
- Generate a rename manifest before applying it. Verify issue labels and page
  order against the scans; retain uncertain cases for review. Exclude any future
  filesystem metadata files from image processing.
- Apply the checked mapping without overwrites. Use temporary names and a journal
  so collisions, interrupted renames, rollback, and reruns are handled safely.
  Recheck source hashes before each move and verify the final hash multiset.
  Renaming must not rotate, recompress, or otherwise modify source bytes.
- Preserve unrelated files and record old and new paths. Already normalized files
  should be recognized; new donations should not renumber existing pages silently.

Exit condition: every valid donated JPEG has an unambiguous normalized name,
with identical bytes and a reversible path mapping. Unresolved path mappings,
conflicting issue evidence, or corrupt inputs are explicitly reported and prevent
declaring normalization complete. Retained donor-only dates remain visibly
unverified even after filename normalization.

### 2. Pilot OCR and image reduction

- Select representative single-, double-, and triple-page TOCs, early and late
  layouts, dense columns, small Korean text, and mixed Korean/English titles.
- Verify the existing local OCR runtime and model hashes. Reuse its pinned
  execution helpers or extract a small shared helper without changing the PDF
  restoration behavior. Do not upload donated images to an external OCR service.
- OCR at a resolution suitable for recognition, independently of web derivative
  sizes. Correct orientation and use explicit column regions where whole-page
  recognition loses reading order. Preserve raw text, bounding boxes, confidence,
  source hashes, crop coordinates, and OCR settings in private evidence.
- Generate both derivative sizes. Inspect dense Korean text at desktop and mobile
  sizes, measure byte sizes, and select the smallest settings that remain useful
  for reading. An initial investigation threshold is 150 KB per preview and
  700 KB per readable page; record justified exceptions rather than damaging text.
- Cache by input hash and transform/OCR configuration so reruns skip unchanged
  work and replacing an image invalidates the affected results.

Exit condition: documented OCR/layout settings and derivative settings work on
the representative sample, with remaining recognition limitations understood.

### 3. Compare all donated TOCs and report mismatches

- Process all pages and merge them in verified issue order. Compare title,
  contributor, printed page, hierarchy, and ordering against the existing TOC.
  Normalize whitespace and Unicode only for comparison; preserve verbatim source
  text in the report and distinguish formatting differences from content differences.
- Produce an issue-by-issue report of matches, differing fields, image-only or
  catalog-only entries, and unresolved text. Include issue/date, stable entry ID
  and `TOC.md` line when available, normalized image name and region, existing
  catalog text, OCR text, and a visual-review note. OCR omission is not evidence
  that an existing entry is wrong.
- Review every page against the transcription, including apparent matches, to
  catch omissions. Distinguish OCR errors, visible differences between the printed
  TOC and library-derived catalog, and unreadable evidence. A visible difference
  remains a report item, not an instruction to replace the catalog text.
- Report the 24 later issue sets as images without corresponding `TOC.md` issues.
  Keep their OCR evidence separate; do not append headings or entries, extend the
  import period, allocate catalog IDs, or invent article associations.
- Deliver the report location and a concise mismatch summary to the user. Keep
  all differing readings available for manual review, including uncertain cases.
- Record the `TOC.md` hash used for comparison and verify it remains unchanged.
  If the user edits it during processing, retain the old report as tied to that
  version and regenerate comparisons against the new version without overwriting
  the user's edits. No comparison command should have a catalog-write mode.

Exit condition: every donated page has a comparison disposition, mismatches and
coverage gaps have been reported to the user, and this workflow has made no
changes to `TOC.md` or its derived catalog metadata.

### 4. Preserve catalog dependencies during image integration

- Keep the current imported TOC, identity map, reference manifests, historical
  snapshots, article bytes, and reviewed associations unchanged. Retain the
  exporter's existing TOC hash and count checks.
- Continue building structured TOC navigation and search from the authoritative
  catalog. OCR is comparison evidence only and must not override display metadata.
- Attach scans to existing canonical printed issues when their identity is
  verified. Preserve separate CD2/CD3 native groups, anomalous labels, and undated
  data; coincident dates alone do not establish an association.
- Make scans without a canonical catalog issue, including the later 24 issue
  sets, accessible through a separate date-labeled TOC scan gallery. This gallery
  describes available images only; it does not create catalog issues, OCR-derived
  TOC entries, article links, or additional restoration groups.
- If the user later edits `TOC.md`, report any resulting stale import or pinned
  dependency explicitly. Do not bypass validation or automatically reimport it
  as a side effect of image preparation. Catalog migration is separate follow-up
  work after the user's manual edits, when requested.

Exit condition: current and historical catalog checks still pass, catalog group
counts and routes remain unchanged, and scans can be displayed independently of
the user's correction decisions.

### 5. Attach reduced images and implement the issue view

- Generate and validate derivatives in a staging directory, then replace the
  prepared set. Record source/derivative hashes, transform settings, dimensions,
  byte sizes, and encoder versions in a private manifest. Reject source/output
  overlap and path escapes; never use original-byte copying as an optimization.
- Attach ordered derivative records to existing canonical issue documents and
  the separate scan gallery through shared reader export logic. Copy only
  validated derivatives into `data/tocs/`, using
  content-sensitive filenames. Remove stale assets and references on replacement
  or removal. Failure must preserve the previous usable reader output.
- Add a labeled TOC scan section to the existing issue overview: ordered lazy
  previews opening an accessible readable view with page selection and zoom.
  Load the larger derivative on demand, reserve image dimensions, and support
  keyboard navigation, descriptive Korean alt text, and narrow screens.
- Keep the structured TOC available alongside the scans. Missing or failed images
  must not prevent reading catalog text. Show a clear missing-scan state for June
  1991; distinguish unavailable scans from unresolved transcription.
- Support absent donation directories and old datasets. Add synthetic demo pages
  without private material. Integrate CD1-only, aggregate, and PDF scan exports;
  define scan-refresh allowances narrowly so unrelated baseline data stays checked.
- Extend `tools/reading_room/check.py` to validate order, references, hashes,
  actual encoding, dimensions, metadata stripping, asset inventories, and the
  absence of donated originals or stale TOC assets in served output.

Exit condition: every accepted scan has both derivatives and appears on its
existing canonical issue page or in the scan gallery; browser requests use only
reduced assets.

### 6. Validate and document the completed workflow

- Add focused synthetic tests for rename collisions/recovery/idempotence, source
  preservation, multipage ordering, OCR caching, comparison and report locations.
  Verify mismatches never modify `TOC.md`, identities, associations, or catalog
  metadata, and user edits invalidate comparisons against the previous hash.
- Test unchanged catalog and historical inputs, retained dependency checks,
  native groups that remain separate, and later scans displayed without creating
  catalog entries or populating catalog search from OCR.
- Test derivative bounds, metadata removal, replacements/removals, missing and
  corrupt sources, staged failure, and all reader export paths. Frontend tests
  should cover page selection, keyboard access, missing images, and old datasets.
- Run focused tests, the existing TOC and snapshot tests, `make test-reading-room`,
  and relevant PDF scan tests. With prepared private data, export to a separate
  validation output first, run its checker, then build and check the active reader.
  Verify historical witnesses against their preserved snapshots.
- Inspect desktop/mobile layouts and nested-base hosting in a real browser.
  Confirm preview versus readable-image requests, readable Korean text, bounded
  network sizes, preserved article routes, and correct multi-page order.
- Update `docs/TOC-IMPORT.md`, `docs/READING-ROOM.md`, `README.md`, and `PROGRESS.md`
  with commands, filename conventions, source authority, manual correction rules,
  OCR/review limitations, scan coverage, and regeneration steps. Record actual
  results in this plan.

Commands are `make inventory-tocs`, `make normalize-tocs` with dry-run
as the default and explicit apply mode, `make ocr-tocs`, `make compare-tocs`, and
`make prepare-toc-images`. All five targets are implemented. Ordinary reader
export should reuse the prepared
reviewed catalog and generate derivatives without rerunning OCR or renaming inputs.

## Completion criteria

The work is complete when all 240 current JPEGs are accounted for with normalized
names and unchanged hashes; all donated pages have a reviewed disposition,
including the advertisement excluded from the 239 accepted TOC images;
all accepted TOC pages have been compared and reviewed;
mismatches have been reported to the user for manual correction; reduced images
work in the reader; and both current and historical validation pass. This workflow
must leave `TOC.md`, catalog identities, and article associations unchanged.
Any unreadable text remains explicitly unresolved rather than silently accepted.
The missing June 1991 donation does not block preserving its existing catalog entry.

Before any commit, inspect the file list and confirm that no donated images,
private OCR evidence, or generated sites are included. This task does not publish
the archive, restore article bodies, or change the cover workflow.

## Implementation checkpoint — 2026-09-30

- Added `tools/toc_restore/` inventory, journaled normalization/rollback, pinned
  local OCR caching, and versioned read-only mismatch reports; all five proposed
  Make targets now exist. Added image preparation, canonical issue attachment,
  separate gallery, checker integration, and CD1/aggregate/PDF refresh paths.
- Added a lazy-preview reader with an on-demand readable dialog, page selection,
  keyboard controls, zoom, failure messages, optional-field compatibility, and
  synthetic demo images. Workflow details are in `docs/TOC-RESTORATION.md`.
- Real inventory verifies 240 JPEGs, 145 issue sets, no duplicate hashes/corrupt
  JPEGs, and missing June 1991. All 20 contact sheets were visually inspected for
  issue labels/order; these reviews explicitly do not claim completed catalog
  comparison. Original mapping and baseline catalog hashes are saved privately.
- Visual inventory found `9507/Page002.jpg` is an advertisement, not a TOC.
  Preserve and normalize it, but exclude it from the TOC viewer. The other July
  image is an opening contents/feature page; later listings appear absent. Its
  date is donor-supplied, not independently printed in the available images.
  Record this uncertainty and incomplete coverage in the gallery/report.
- A 12-page portrait pilot produced 41–65 KB previews and 380–616 KB readable
  images. The landscape April 1986 pilot is readable at 1600 × 1152 (279 KB).
  That source has obscured text, which must remain unresolved. Whole-page OCR
  misses some colored headings; region experiments and raw evidence are retained.
- Initial validation passed 50 reader Python tests, 58 PDF tests, 15 frontend
  tests, and TypeScript/build. Initial browser checks under `/archive/` confirmed
  larger images load on opening,
  keyboard page navigation, Escape/focus restoration, and no page overflow at
  390 px. Subsequent integration and real-data/browser results are recorded below.
- Full OCR now covers all 240 files. All 240 originals have normalized filenames;
  an independent check confirmed every original SHA-256 and the exact file list.
  The private journal retains the original mapping for rollback. Full preparation
  produced 239 accepted pages and 478 derivatives, with the advertisement excluded.
- Separate aggregate, CD1-only, and PDF scan exports and their checkers pass.
  Catalog baseline hashes remain unchanged. The reader suite has passed 54 Python
  tests; the 14 focused TOC tests also pass after adding catalog/OCR review
  invalidation checks. Detailed visual comparison covers every donated catalog
  page through December 1993; all 240 files have reviewed dispositions, with
  420 findings. Damaged August 1984 text, the blacked-out
  April 1986 graphics listings, and July 1992's clipped page digits remain unresolved. Findings include missing
  entries, displaced page numbers, split titles, and February 1987's conflicting
  printed masthead year (1986) versus publication line (1987). Later findings
  include September 1988's shifted page assignments, September 1989's omitted
  SPSS Q&A entry and displaced contributor, and November 1989's displaced pages.
  The 1990 comparisons add merged/split titles, contributor differences, July
  and August's swapped page assignments, and October's missing readers-section page.
  The 1991 comparisons add March's conflicting colophon date, November's omitted
  news section, December's omitted competition notice, and title/byline differences.
  June 1991 remains a catalog-only coverage gap because no scan was donated.
  The 1992 comparisons add January's four omitted articles, May's missing news
  page and AUTOEXEC.BAT spelling, July/August contributor differences, and
  December's displaced feature page (289 versus 298), hierarchy differences,
  omitted news sidebar and missing printer troubleshooting item.
  The 1993 comparisons add installment/title/byline differences, an omitted
  readers-section entry, hierarchy differences, and split utility titles.
  The 24 later issue sets were reviewed as image-only evidence; their dates,
  continuation order and coverage are recorded without adding catalog entries.
  July 1995 remains explicitly unresolved because its date is donor-supplied and
  later contents appear absent. The advertisement has its own excluded disposition.
  The current versioned private report is selected by
  `private/toc-restoration/reports/latest.json`; no donated pages remain pending.
  All 240 reviews are pinned to source images, OCR evidence and `TOC.md`.
- Active reader export, strict checker and production build pass. Preservation
  checks account for all 44,818 prior data files with no unrelated changes; the
  479 new files are 478 derivatives and the gallery document. Real browser checks
  at 390 × 844 and 1440 × 1000 verify readable Korean zoom, contained scrolling,
  on-demand requests, Escape/focus, failed-image fallback, missing June 1991,
  July 1995 uncertainty, three-page selection and a preserved article route.
  Both nested `/archive/` and active root hosting load reduced assets correctly.
- Final validation passes 56 reader Python tests (including full-issue PDF export
  preservation of inherited TOC images), 15 frontend tests, 58 PDF tests and
  18 TOC/snapshot tests, plus TypeScript and production build. Both historical
  article witnesses and the February coverage record reproduce exactly.
- Final completion audit passes: all 240 source hashes and review pins, all 420
  rendered findings, the pinned OCR runtime, 478 validated derivatives, four
  strict reader checks, eight historical snapshot files and all 44,818 prior
  reader files. Removing only the intended TOC presentation additions reproduces
  the saved reader baseline; its only 479 new files are the derivatives and gallery.
  The source-replacement test also verifies EXIF orientation, no upscaling, RGB
  conversion, metadata removal and deletion of the prior derivatives.
- Delivered the private mismatch report selected by `reports/latest.json`
  (version `bb5cd0a4d210d66a52f4a3e188329b93a4070c923a9e1f0f9d187bc4bdcf7cbe`).
  No page reviews remain pending or stale. Unreadable evidence and July 1995's
  uncertain date/coverage remain explicit report dispositions, not corrections.
  Detailed independent results are in `private/toc-restoration/completion-audit.json`.
  No catalog edits, commits or publication were performed.
