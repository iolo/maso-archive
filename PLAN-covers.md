# Cover restoration implementation plan

Prepared 2026-09-30 from [PRD-covers.md](PRD-covers.md) and inspection of the
existing reading-room exporter. Status: **implemented and validated 2026-09-30**.
Includes the subsequent requirement that donated covers take priority over
covers restored from scanned PDFs.

## Outcome and boundaries

Generate small thumbnails from donated `covers/YYMM.jpg` images and display
them on the existing bookshelf and issue pages. Keep donated originals private,
unchanged, excluded from Git and outside every served output. Delete a legacy
`covers/masoYYMM.jpg` only after its donated replacement has a validated thumbnail
and the reader integration has passed validation.

Select one cover per date in this order:

1. Donated `covers/YYMM.jpg`.
2. A verified front cover restored from a scanned PDF, when no donated cover exists.
3. The existing placeholder when neither source is available.

Generate a bounded thumbnail from either selected source. A PDF cover must never
replace a donated cover, regardless of image dimensions, timestamps or export
order. A corrupt donated input is an error, not permission to silently select a PDF.

Ignore unverified old low-quality covers. A `masoYYMM.*` filename alone does not
establish PDF provenance: identify eligible PDF covers through the existing
private PDF cover review/checkpoint records and verify the selected artifact's
hash and reviewed date. Limit deletion to the explicitly named `.jpg` files;
preserve legacy `.png`, `.jpeg` and `.webp` files on disk, along with private PDF
review records and candidate artifacts needed for fallback.

This work does not add issues, change article/TOC associations, restore missing
covers, alter the PDF extraction workflow, or deploy the archive.

## Inspected starting point

- `covers/` contains 145 donated JPEGs totaling 1,258,032,347 bytes, covering
  November 1983–December 1995 except June 1991 (`9106.jpg`).
- There are 27 legacy covers: 20 JPEGs and seven PNGs. Every legacy cover currently
  has a corresponding donated JPEG.
- `/covers/`, `/build/` and `/private/` are already ignored. No cover files are
  tracked. Preserve the existing user changes to `.gitignore`.
- `tools/reading_room/covers.py` currently accepts only `masoYYMM` filenames and
  copies their original bytes into the reader. Donated filenames currently cause
  an export error; adding filename support alone would expose full-size images.
- The shared `attach_covers()` adapter is used by the CD1 exporter, combined
  CD1/CD2/CD3 exporter, and PDF scan reader staging.
- `IssueCover` in `web/src/App.tsx` already supports dimensions, bookshelf lazy
  loading, issue-page display, and a failed/missing-image placeholder.
- Pillow is already a dependency. The existing aggregate exporter checks a
  staging directory before replacing the reader's data directory.
- PDF scan staging copies its baseline and enforces unchanged baseline files.
  Cover refresh must account explicitly for replaced/removed cover assets and
  changed issue documents, while preserving article and source-file checks.
- Vite preserves its output directory (`emptyOutDir: false`), so a frontend build
  alone cannot remove stale exported covers.

## Proposed thumbnail contract

These settings are implementation defaults, not additional PRD requirements:

| Property | Decision |
| --- | --- |
| Input | Donated `YYMM.jpg`, then verified PDF cover artifacts by reviewed date; `YY` maps to `19YY`, month must be 01–12 |
| Output | One JPEG thumbnail per supplied date, with a distinct derivative filename |
| Size | Fit within 480 × 640 pixels, preserving aspect ratio; never upscale or crop |
| Encoding | RGB, JPEG quality 80, optimized encoding |
| Orientation | Apply EXIF orientation before resizing |
| Metadata | Do not copy EXIF, comments, embedded thumbnails, or other source metadata |
| Storage | Rebuildable derivatives and source/transform records under ignored `build/cover-thumbnails/` |
| Reader assets | Copy only validated derivatives into `data/covers/` |
| Missing input | Try the verified PDF fallback when the donated cover is absent, then the placeholder; missing source directories remain supported |

Use Pillow's high-quality downsampling and handle color profiles consistently
when converting to RGB. Fully decode images before accepting them. Report corrupt
JPEGs, invalid dates, mismatched formats and ambiguous duplicates within a source
tier clearly. A donated cover and a verified PDF cover for the same date are
expected alternatives, not a duplicate-input error. Ignore unverified legacy
files before attempting to decode them.

Record source kind, reviewed PDF evidence where applicable, source hashes,
derivative hashes, dimensions, byte sizes, transform settings and relevant encoder
versions in the private derivative manifest.
Use content-sensitive derivative names so replacing a source does not leave the
browser displaying an older thumbnail at the same URL. Regenerate derivatives
when source bytes or transform settings change.

## Implementation sequence

### 1. Build the thumbnail preparation path

- Extend `tools/reading_room/covers.py` with source discovery, image transformation
  and derivative validation, separating those operations from issue attachment.
- Read verified PDF cover candidates from the existing private cover checkpoint;
  make its location configurable and allow it to be absent. Resolve source
  priority by date before generating thumbnails; do not infer provenance from
  installed legacy filenames or accept unreviewed PDF page renders.
- Provide `make prepare-cover-thumbnails` to prepare all valid donated inputs,
  including dates absent from the current reader catalog. Let normal exports
  invoke the same preparation logic so users do not need a separate manual step.
- Prepare outputs in a staging directory, validate the completed manifest and
  images, then replace the generated derivative set. A failed run must preserve
  the previous usable set and leave every source file untouched.
- Keep source and output paths distinct, reject unsafe path/symlink escapes,
  and never use a direct-copy shortcut for donated originals, even small ones.
- Report supplied dates, selected source kinds, successful thumbnails, invalid
  inputs and total output bytes. June 1991 is a donated-input gap; use a verified
  PDF cover if available, otherwise report a coverage gap without failing export.

### 2. Integrate derivatives with every reader export

- Change `attach_covers()` to attach only generated thumbnails, retaining the
  existing `cover: {path, width, height, sha256}` frontend contract.
- Apply the same donated-first selection in every export. Refreshing a scan
  reader must not downgrade a donated thumbnail to a PDF-derived thumbnail.
- Reset prior cover assignments when refreshing covers; remove obsolete cover
  assets from the staged reader tree so legacy files cannot remain served.
  Ensure issue documents and the catalog agree, including issues that lose a cover.
- Update `coverInputs`, file hashes and counts to describe generated assets.
  Keep detailed source records private and avoid browser links to donated inputs.
- Preserve date-based matching for CD1/CD2/CD3: multiple native groups can share
  a thumbnail, undated groups remain uncovered, and counts distinguish unique
  thumbnails from groups with assigned covers. Do not invent missing issues.
- Update scan staging's permitted cover changes narrowly, including removed
  assets and cleared cover assignments. Keep unrelated baseline files protected.
  With no cover refresh requested, retain its existing baseline-copy behavior.
- Separate validation of existing baseline integrity from the strict derivative
  checks for refreshed outputs. Scan staging must be able to validate a legacy
  baseline before replacing its covers. A no-refresh copy may retain legacy
  covers but must not be reported as a completed cover migration.
- Preserve `--covers` as the donated-source directory option and update its help
  text. Keep the synthetic demo independent of private files.
- Reuse the existing `IssueCover` component unless visual verification reveals
  a concrete rendering problem; no UI redesign or data schema bump is expected.

### 3. Validate the output, then clean up legacy JPEGs

- Extend `tools/reading_room/check.py` to decode cover derivatives and verify
  actual format, dimensions, bounds, metadata policy, hashes, and catalog/issue
  consistency in refreshed outputs. Ensure their cover inventory contains only
  referenced derivatives and no stale legacy assets.
- Add a cleanup command with a dry-run report and an explicit apply mode.
  Ordinary preparation/export/check commands must never delete source files.
- Produce the cleanup candidate list by exact `masoYYMM.jpg` → `YYMM.jpg` pairing.
  Require successful reader validation and a checked thumbnail for each candidate;
  a date outside the reader catalog can use its prepared, validated derivative.
- Before deletion, recheck the source and derivative hashes and the legacy file
  identity against the cleanup report. Reject stale reports or changed files.
  Record completed deletions in an ignored local log and make reruns safe.
- Apply cleanup as the last migration step. The present expected result is
  deletion of 20 legacy JPEGs, preservation of seven legacy PNGs, and no change
  to any of the 145 donated JPEGs. Recompute these counts at execution time.

### 4. Document and verify the complete workflow

- Update `README.md` and the cover section of `docs/READING-ROOM.md` with donated
  filenames, derivative limits, regeneration, missing-cover behavior and cleanup.
  Remove the obsolete instructions promising original-byte copying and the stale
  eight-cover sample count.
- Document the donated → verified PDF → placeholder priority. PDF cover
  preparation/review remains a separate workflow; this path consumes its verified
  artifacts as fallback and does not change PDF extraction or review gates.
- Record implementation and validation results in `PROGRESS.md`, then update
  this plan's status. Commit only code, documentation and synthetic fixtures.

## Validation and acceptance

Add focused synthetic tests in `tests/test_reading_room_web_export.py` and, if
needed, a dedicated cover test module. Cover the behavior that matters:

- Correct date parsing, unverified legacy-file exclusion, corrupt inputs, missing
  source directories, and source/output path separation.
- Donated/PDF collisions select donated covers without duplicate errors, regardless
  of dimensions, timestamps or export order. PDF-only dates use bounded PDF
  thumbnails; dates with neither source use placeholders. Invalid donated images
  fail rather than silently falling back; unverified PDF candidates are excluded.
- Real downsampling, preserved proportions, orientation handling, bounded output,
  stripped metadata, unchanged source hashes, and no source-byte copying.
- One derivative shared across matching groups; missing and undated placeholders.
- Source replacement/removal refreshes filenames, assignments and manifests and
  removes stale output. Failure leaves prior validated output usable.
- Adding a donation replaces the PDF thumbnail; removing it selects an available
  verified PDF fallback. Cleanup of installed legacy JPEGs preserves private PDF
  candidate artifacts so this fallback remains possible.
- All three export paths consume derivatives, including scan baseline refresh
  from legacy-format covers without changing unrelated CD data. No-refresh scan
  staging preserves its baseline without claiming derivative compliance.
- Cleanup preserves unpaired files, non-JPEG legacy files and donated originals;
  invalid/stale replacement evidence prevents deletion; repeated application is safe.

Run the focused Python tests, relevant PDF scan integration tests, and
`make test-reading-room`. With private data, prepare all donated thumbnails and
run `make export-reading-room`, `make check-reading-room`, and
`make build-reading-room` before cleanup. Verify the scan reader in a separate
output when exercising its integration.

Inspect the bookshelf and issue view in a real browser at desktop and mobile
sizes, including a donated cover replacing a PDF cover, a PDF-only cover, a
missing-cover placeholder, a failed image load, and nested-base hosting. Confirm
cover requests load only bounded derivatives.
Measure generated dimensions and total bytes; aim for roughly 100 KB or less
per cover on average and investigate outliers before adjusting quality.

The work is complete when every valid donated input has a thumbnail, every
matching reader group uses that thumbnail in preference to a PDF cover, groups
without donations use verified PDF thumbnails where available, no donated original
or stale legacy cover is present in refreshed served cover outputs, the reader checks pass,
eligible legacy JPEGs are removed, and donated source hashes remain unchanged.
Verify `git status` and the staged file list contain no donated images or
generated private artifacts.


## Execution results — 2026-09-30

- Prepared all 145 donations: 9,541,138 bytes total, about 65.8 KB per cover.
  Every derivative is RGB JPEG, within 480 × 640, with source metadata removed.
  The largest is February 1993 at 112,833 bytes (480 × 609); visual inspection
  confirmed its detailed textured artwork explains the size. Quality remains 80.
- The aggregate retains 152 groups and 3,386 articles, with 149 assigned groups
  sharing 145 thumbnails. June 1991 remains a documented missing-source gap.
- `make prepare-cover-thumbnails`, `make export-reading-room`,
  `make check-reading-room`, and `make build-reading-room` passed. Separate
  CD1-only and scan refresh outputs passed; the latter retained CD source bytes
  while adding the existing reviewed pilot (3,387 total articles).
- `make test-reading-room` passed 40 Python tests, 13 Vitest tests, TypeScript
  checking and the production build. All 58 PDF tests passed. Synthetic coverage
  includes failed/stale cleanup, atomic export failure, legacy scan migration,
  missing sources, PDF review/hash gates, priority and replacement/removal.
- Chromium checks passed at 1440 × 1000 and 390 × 844: bookshelf, issue view,
  missing/failed-image placeholders, PDF fallback at `/archive/`, and a donation
  replacing that PDF thumbnail with a new URL. Requests used bounded derivatives;
  screenshots are private under `output/playwright/covers-*.png`.
- Applied the validated cleanup report and verified safe reapplication: exactly
  20 legacy JPEGs removed; all 145 donations, seven legacy PNGs, and PDF checkpoint
  files retain their pre-migration hashes. Private evidence is in
  `build/cover-migration-before.json`, `build/cover-migration-result.json`,
  `build/cover-cleanup.json` and its applied log.
- Updated README and the reading-room guide. No donor images or generated private
  artifacts are tracked or staged. Existing user edits to `.gitignore` were preserved.
- Post-cleanup strict checks passed for all four refreshed reader outputs; the
  retained checkpoint independently regenerates 21 verified PDF thumbnails.
