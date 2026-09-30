# Local PDF restoration

Follow [PLAN-PDF.md](../PLAN-PDF.md) in checkpoint order and record each outcome
in [PROGRESS-PDF.md](../PROGRESS-PDF.md). The tools here do not authorize bulk OCR
before the pilot, contrasting samples, and staged reader pass their gates.

## Step 1: source inventory

Requires Python 3.11+ and Poppler `pdfinfo` / `pdftotext` on PATH. This checkpoint
uses no OCR engine or Python PDF dependency. The executed version is recorded
in the generated source manifest (initial run: Poppler 26.01.0).

Private inputs: the 21 `maso-pdf/maso-YYMM.pdf` files named by the plan, current
`TOC.md`, `data/identities/toc.json`, and the complete current `build/toc/`
snapshot. If the snapshot is missing, run `make import-toc` first. Historical
CD snapshot caches are not inputs to this pass.

```sh
make inventory-pdf
make test-pdf
# Independent rerun; never overwrite an existing checkpoint:
make inventory-pdf PDF_ARGS='--output private/pdf-restoration/inventory-repeat'
diff -qr private/pdf-restoration/inventory private/pdf-restoration/inventory-repeat
```

The default output is `private/pdf-restoration/inventory/`:

- `sources.json`: streaming SHA-256 and byte counts for original PDFs, tool
  versions, upstream snapshot hashes, per-page dimensions/rotation/MediaBox/
  CropBox and extractable-text presence. PDF indexes are zero-based, PDF page
  numbers one-based, boxes use PDF points and the unrotated bottom-left origin.
  Printed page numbers are never inferred from PDF indexes.
- `queue.jsonl`: every relevant TOC entry, including page-less leaves and
  headings, retaining its original identity, hierarchy, flags and candidate
  classification. Final eligibility and article location remain unresolved.
  An existing provisional article candidate ID is a reference, not a final
  decision or a new scan article ID.
- `evidence/`: raw Poppler page metadata and existing text layers. Text-layer
  presence says nothing about legibility or OCR success.
- `report.json`: reconciled source totals and counts by issue, hashed output
  references and explicit limits. The two 1995 sources have cover-only scope
  and no invented canonical TOC issue identity.

Inventory validates the full source set, expected plan totals, current TOC hash,
identity ledger, schema and all structured snapshot artifacts before publishing.
It rechecks source hashes after extraction and upstream hashes before the final
directory rename. A mismatch fails without installing a completed checkpoint;
review and document any evidenced input correction before changing the pinned
expectations. Existing outputs are never silently replaced. All source labels
remain unverified until visual inspection; step 1 does not map articles.

Ordinary tests use synthetic metadata and TOC records. Real scans, extracted
text, generated manifests and review images remain ignored under `private/`
or `build/`. Cover assets also remain in the existing ignored `covers/` folder.

## Step 2: cover evidence and installation

```sh
make prepare-pdf-covers
# Inspect candidates, then save the explicit private review.json described below.
make install-pdf-covers
```

Preparation saves the hashes of all existing covers before rendering page 1 of
each source with Poppler, a longest edge of 1,800 pixels and JPEG quality 92.
Poppler applies PDF rotation; the tool checks the resulting aspect ratio against
the source dimensions. Original sources and their metadata remain unchanged.
All 21 front covers were found on page 1 in the initial pass; no additional
lookup pages were required. Any future cover search must stay within the first
and last five pages of its PDF and preserve an unresolved outcome when exhausted.

`private/pdf-restoration/covers/candidates.json` pins each candidate, source,
source-page geometry and rendering settings. The explicit `review.json` is a
list with one record per source. A usable front-cover review has `source_id`,
`status: "verified-front-cover"`, `visible_issue_label` (`YYMM`), `date_evidence`
(visible text and region), `upright: true`, `proportions_checked: true`, and
`reviewed_artifact` (the candidate's exact path/hash/byte-count record). Record
condition, reviewed regions and date as well. Other outcomes are `uncertain`,
`damaged`, or `not-located`; these never install an image or assert an association.

Installation validates every review and source before writing. It uses exclusive
creation for missing `covers/masoYYMM.jpg` files and preserves existing covers
in any extension. Alternatives remain under `private/pdf-restoration/covers/`.
`ledger.json` records all 21 outcomes, existing hashes, new hashes and date
evidence. Verified cover dates identify the PDF issue label only; they do not
create TOC or CD identities. Reader presentation is checked later in step 9.

## Step 3: mapped article package

[The schema](../schemas/pdf-article.schema.json) and
[synthetic example](../examples/pdf-article.json) define version 1 of the
restoration package (separate from the reader contract version). Validate with:

```sh
PYTHONPATH=src python3 -m tools.pdf_restore.package \
  private/pdf-restoration/pilot/pilot-map.json
```

An article ID is `scan-` plus its existing TOC entry ID; correcting an OCR title
does not change it. Issue/TOC references and source hashes stay explicit. Source
PDF and TOC pin paths refer to repository inputs; generated OCR, correction,
figure and download paths refer to the package directory. All paths must be
relative and cannot contain traversal. The schema/validator checks structure;
later exporters must also verify referenced file bytes and TOC membership.

Each page records its zero-based PDF index, one-based PDF page, independently
observed printed number (or null), unrotated dimensions, MediaBox, CropBox and
rotation. Regions use `[left, top, right, bottom]` normalized to the full upright
page. The affine `pdf_to_upright_normalized` matrix maps unrotated PDF points
with bottom-left origin to those normalized coordinates. For `[a,b,c,d,e,f]`,
`u=a*x+c*y+e` and `v=b*x+d*y+f`; transforms account for nonzero MediaBox origins
and all four right-angle rotations. Full-page rendering uses MediaBox, not
CropBox. Pixel crops multiply normalized coordinates by the actual rendered
width/height; do not treat original PDF points as rendered pixels.

The `regions` array is reading order, including noncontiguous continuations.
Never sort it by PDF index. `excluded_regions` records shared-page advertising
or other excluded material; positive-area overlap with an eligible region is
rejected. Blocks and figures reference eligible region IDs, and mapping evidence
is separate from text review. Missing source pages are represented as explicit
gaps, not guessed source-page references. An unresolved or partial mapping does
not pass a complete-article gate.

Raw OCR text, positional data and settings have separate hashed references.
Corrected text blocks point back to source regions and correction evidence;
correction files, figures and downloads have their own pins. Keep literal code
whitespace. `availability` and `verification.status` are independent, with exact
reviewed region IDs, evidence and uncertainties. A mapped article awaiting OCR
remains `unresolved` / `unreviewed`. CD relationships require separate evidence.

The initial pilot is `scan-maso-1983-11-toc-0012`, mapped to PDF pages 30–31 /
printed pages 28–29. Nine ordered regions cover the section label, title, byline,
introduction, maze figure, two prose columns and two listing columns. The lower
book advertisement on PDF page 31 is excluded. The left listing's line 410
continues at the top of the right column, which ends at line 690 `RETURN`.
The visible listing starts at 110; this is recorded without inventing missing
earlier code. `mapping-review.json` pins the page evidence and documents the
opening/ending decision. No OCR or transcription accuracy is implied.

## Step 4: pinned local OCR

The initial runtime uses Ubuntu resolute amd64 packages, extracted into a private
directory without a system installation. Required host libraries are recorded
by `ldd` in `runtime.json`. On another platform, prepare a separately documented
runtime; do not silently replace the pinned engine or models.

```sh
mkdir -p private/pdf-restoration/ocr-runtime/debs
cd private/pdf-restoration/ocr-runtime/debs
apt-get download tesseract-ocr=5.5.0-1build1 libtesseract5=5.5.0-1build1 \
  libleptonica6=1.86.0-1 tesseract-ocr-kor=1:4.1.0-2build1 \
  tesseract-ocr-eng=1:4.1.0-2build1
cd ../../../..
PYTHONPATH=src python3 -m tools.pdf_restore.ocr setup
PYTHONPATH=src python3 -m tools.pdf_restore.ocr page \
  --package private/pdf-restoration/pilot/pilot-map.json --pdf-page 30 \
  --output private/pdf-restoration/pilot/ocr-page30
PYTHONPATH=src python3 -m tools.pdf_restore.ocr page \
  --package private/pdf-restoration/pilot/pilot-map.json --pdf-page 30 \
  --output private/pdf-restoration/pilot/ocr-page30-repeat --mode regions
```

Setup checks the five downloaded package SHA-256 values pinned in `ocr.py`
before extraction. Preserve those `.deb` files for offline rebuilds if the
distribution repository later removes the versions. `runtime.json` pins the
executable, libraries and both models. Korean model SHA-256 is
`6b85e11d9bbf07863b97b3523b1b112844c43e713df8b66418a081fd1060b3b2`;
English is `7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2`.
Engine version is Tesseract 5.5.0 / Leptonica 1.86.0, models package 4.1.0-2build1.
Repeated setup ignores only process-specific ASLR addresses in `ldd` output
when comparing runtime records, and preserves the original manifest bytes.

The page command is deliberately bounded to one mapped page. It verifies the
source/model hashes, renders to a 3,000-pixel longest edge, masks ineligible
areas, and compares eligible-page PSM 3 with ordered-region PSM 6. It keeps
figures as crops and does not OCR them in region mode. Prose uses `kor+eng`;
code regions use `eng`. Engine mode is 1, one OpenMP thread, preserved interword
spaces and a 300 DPI recognition hint (not a claim about physical scan DPI).
Excluded regions are whitened before either kind of OCR input is generated,
including shared-boundary pixels. Originals remain unchanged.

Each result retains raw TXT, TSV positions, settings, input crops and an evidence
manifest. TSV coordinates are relative to each OCR input; add `crop_pixels`'s
origin to locate them on the rendered page. Wall time is separately recorded in
`timing.json` and excluded from deterministic comparisons. Existing output
directories are refused rather than overwritten. The initial selected-region
rerun reproduced all 24 text/TSV/settings/stderr files exactly.

The initial comparison in `pilot/ocr-comparison.json` selects region PSM 6 for
explicit column order. Raw Korean recognition is poor and the decorative title
is empty. It requires substantial scan-supported correction; deterministic OCR
does not satisfy the useful-pilot gate or authorize bulk processing. No engine
search or third processing configuration was attempted.

## Step 5: reviewed article and portable preview

```sh
# One mapped page at a time; the pilot's remaining page contains two code regions.
PYTHONPATH=src python3 -m tools.pdf_restore.ocr page \
  --package private/pdf-restoration/pilot/pilot-map.json --pdf-page 31 \
  --output private/pdf-restoration/pilot/ocr-page31 --mode regions
# After saving scan-supported corrections and the pinned recipe:
make build-pdf-article
make check-pdf-article
make build-pdf-article PDF_OUTPUT=build/pdf-restoration/pilot-repeat
diff -qr build/pdf-restoration/pilot build/pdf-restoration/pilot-repeat
make test-pdf
```

The default recipe is `private/pdf-restoration/pilot/package-recipe.json`, and
the output is `build/pdf-restoration/pilot/`. Supply `PDF_RECIPE` and `PDF_OUTPUT`
for a later article. Outputs must remain under private/build locations; existing
directories are refused. A validated temporary export is renamed into place.
The build never runs OCR or overwrites reviewed corrections.

The private recipe pins the map, correction record, OCR evidence bundles and
runtime. It declares ordered blocks/figures, availability, verification scope
and gaps. `corrections.json` preserves a separate decision for every region,
with the reviewed scan hash, raw OCR hash, method and corrected blocks. Prose
print wraps may be joined with an explicit note. Code retains the transcribed
whitespace and physical wraps; uncertain characters or blank counts use `⟦…⟧`
and an accompanying explanation. Do not repair code from expected semantics.

The package schema now supports explicit `content_order`, `region_assets` and
hashed `review_records`. Maps produced in step 3 still validate. A readable
package must represent every mapped region, include every block/figure exactly
once in its order and expose every region image. The builder verifies source
and TOC membership, page geometry, map/OCR correspondence and all copied bytes.
This establishes structural coverage, not automatic transcription accuracy.

Open `build/pdf-restoration/pilot/index.html` directly, or serve the export
directory locally. The renderer reuses the existing reference HTML/CSS helpers
and emits static relative links with no JavaScript or external assets. Later
issue references can call the same renderer. It places figures in the declared
reading order, renders literal code in scrollable `pre` blocks and exposes
availability separately from review status.

The export contains:

- `article.json`, its portable preview and a complete hashed file manifest;
- `article.txt`, `listing.txt` and a deterministic `raw-ocr.zip` download;
- all nine eligible scan crops, raw regional TXT/TSV/settings, original
  corrections, map and runtime provenance;
- explicit per-block uncertainties and links to the source crops.

Full-page renders containing advertisements remain in private evidence and are
not copied into the preview or ZIP. Page-level OCR comparison evidence also
remains private; the package carries the selected regional outputs. Original
source PDF/TOC paths in metadata identify repository inputs rather than claiming
the full PDFs are included in the portable package. Original settings and
correction pins retain their provenance scopes; the private runtime/debs and
source PDFs are required to rerun OCR.

The pilot is `readable` / `sample-reviewed`: all prose, the figure, and every
printed code row were compared with their scans. Code is not character-perfect:
horizontal spacing remains unverified, line 550's quoted blank count is unknown,
and line 560 has an uncertain dot versus printing noise. These limits are shown
in the reading page and literal code. The useful-pilot result does not pass the
contrasting-sample, reader-integration or bulk-readiness gates.

## Step 6a: early-format contrast

The November sample is existing TOC entry `maso-1983-11-toc-0013`, 성냥개비
(printed title 성냥개비 게임). Its package is
`build/pdf-restoration/6a-matchsticks/`, with private inputs and review records
under `private/pdf-restoration/6a-matchsticks/`. PDF pages 32–34 / printed 30–32
contain 31 mapped regions: three-column prose, nine interspersed code blocks,
a photograph and two diagrams. All regions have review evidence. Availability
is `readable`, verification `sample-reviewed`; code spacing and three localized
character/count uncertainties remain explicit.

```sh
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/6a-matchsticks/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/6a-matchsticks-new
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/6a-matchsticks-new
diff -qr build/pdf-restoration/6a-matchsticks build/pdf-restoration/6a-matchsticks-new
```

Use a fresh output directory. The saved `6a-matchsticks-repeat/` export is
byte-identical. The renderer preserves blank-line paragraph boundaries within
prose blocks; literal code whitespace is unchanged. Blocks spanning column
breaks reference both source regions, while figures have explicit positions
in `content_order`. Figure 1 precedes the paragraph introducing the next page's
listing so that the introduction and listing remain adjacent.

`ownership.json` records the local classification separately from the original
queue: the scanned contents on PDF 10 identifies 취미생활 (`toc-0011`) as a
page-less group for eleven individually listed children. No parent body is
exported, and other children's article locations remain provisional. Do not
rewrite historical TOC data or count parent headings as restored articles.

`mapping-review.json`, `corrections.json`, `feature-results.json`,
`validation.json`, `browser-review.json` and `closeout.json` retain the sample's
extent, exact review coverage, synthetic edge-case results, browser checks and
remaining gaps. Source-derived artifacts remain ignored. Step 6a passes its
sample gate; January 1988 and August 1991 samples and reader integration remain
required before bulk work.

## Step 6b: January 1988, rotation and a shared page

Existing TOC entry `maso-1988-01-toc-0018`, 터보 파스칼에 한글을, is restored
in `build/pdf-restoration/6b-turbo-pascal/`. Private inputs and review records
are in `private/pdf-restoration/6b-turbo-pascal/`. The printed title includes
version 3.0; the original TOC identity remains unchanged.

PDF pages 94–95 visibly print 92–93 and carry rotation 270. Poppler renders
them upright at 2122×3000; all region coordinates and stored transforms use
the existing upright coordinate convention. Eleven regions cover the article,
including its complete BASIC listing and caption. Five prose continuations
cross columns or pages. The listing follows the continuous prose in the preview
so that a cross-page sentence is not interrupted.

The lower part of PDF 95 is a distinct, unlisted “1라인 모니터 프로그램” item.
Its flowchart, code and prose are excluded, along with the repeated running
header. Pixel checks verify that the excluded area is white in the eligible
OCR input. Full-page renders remain private and do not enter the export or ZIP.
There is no eligible article illustration in this sample.

```sh
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/6b-turbo-pascal/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/6b-turbo-pascal-new
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/6b-turbo-pascal-new
diff -qr build/pdf-restoration/6b-turbo-pascal build/pdf-restoration/6b-turbo-pascal-new
```

The sample is `readable` / `sample-reviewed`. All eleven regions were compared
with the scans, including the complete first prose column and every listing
row. A visibly blank phrase in the opening column is marked without inventing
words. Code spacing remains unverified; physical listing wraps and observed
inline Pascal punctuation are preserved. No historical code was executed.
The repeat export is byte-identical, and desktop/mobile and asset-hash checks
pass. The sample gate passes; step 6c and later reader/batch gates remain.

## Step 6c: August 1991, prose and inset quotations

Existing TOC entry `maso-1991-08-toc-0004`, 컬럼 마소쉘 : 베이직 언어로
돌아가자, is restored in `build/pdf-restoration/6c-basic-column/`. Private
mapping, OCR, corrections and review records are under
`private/pdf-restoration/6c-basic-column/`. PDF 84–86 contain fifteen regions
represented by twenty text blocks and one complete framed portrait. The first
two pages visibly print 98 and 99; PDF 86 has no visible folio and retains an
unknown printed page number.

The three-column prose includes an oversized opening character, eight text
continuations and two inset quotations. Both quotations are retained, including
their repetition of body text. The second quotation precedes the complete
adoption paragraph to avoid splitting its sentence. Drop-cap size, column/inset
placement and inline italics are normalized in reading text; source crops
preserve the original typography. The boxed recruitment notice below the
conclusion and repeated running headers are excluded.

```sh
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/6c-basic-column/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/6c-basic-column-new
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/6c-basic-column-new
diff -qr build/pdf-restoration/6c-basic-column build/pdf-restoration/6c-basic-column-new
```

The sample is `readable` / `sample-reviewed`. Every mapped region and printed
text row was compared with the scan, including complete prose column r07,
portrait r05 and quotations r04/r10. No code listing is present: the exporter
now omits `listing.txt` and its link for packages with no code blocks, while
retaining article text and raw OCR downloads. Packages containing code keep
their listing download. All 21 focused tests pass; the repeat export is
byte-identical and desktop/mobile text, image and download checks pass.
Step 6 is complete. Step 7's evidenced CD comparison and later reader/batch
gates remain; no CD relationship is asserted for this sample yet.

## Step 7: a separate, evidenced CD comparison

The August sample now has a reviewed correspondence to CD1 reference `9108098`.
Evidence includes the CD's issue/page label, the printed opening page, the author
and a substantial shared body passage. The original article packages retain
their existing metadata; the reviewed relationship lives in the comparison
sidecar for later integration.

Open `build/pdf-restoration/7-cd-comparison/comparison.md` for the report or
`comparison.json` for post-production. The comparison covers thirteen complete
text blocks on PDF 84–85 / printed 98–99 and the portrait. The debugging block
that crosses onto PDF 86 and later text remain outside the review. This is a
`sample-reviewed` correspondence, with `whole_cd_article_verified: false`.

Each comparison unit retains exact CD excerpts with paragraph-relative and
article-wide character ranges, the scan-supported reading with block/region
references, exact edit operations and a review decision. Offsets are zero-based,
end-exclusive Unicode character offsets, not byte offsets. CD spans are joined
without normalization. All 52 operations remain available, including paragraph
newlines and typography; they are not an error count. Three highlighted findings
record two CD omissions and one changed phrase, with scan-region evidence.

CD text, raw OCR and `corrections.json` remain distinct and unchanged. The package
also retains the two scan-only textual layout occurrences and the portrait's
disposition. The CD's sole image is a section icon, not that portrait. No source
is overwritten, no correction is automatically applied, and historical factual
claims or terminology are not independently repaired. Complete CD and correction
records are preserved as source snapshots without extending the comparison scope.

```sh
make compare-pdf-cd \
  PDF_COMPARISON_OUTPUT=build/pdf-restoration/7-cd-comparison-new
make check-pdf-comparison \
  PDF_COMPARISON_OUTPUT=build/pdf-restoration/7-cd-comparison-new
diff -qr build/pdf-restoration/7-cd-comparison build/pdf-restoration/7-cd-comparison-new
make test-pdf
```

The default recipe is
`private/pdf-restoration/7-cd-comparison/comparison-recipe.json`; override it with
`PDF_COMPARISON_RECIPE`. Use a fresh output path. The checked repeat export is
byte-identical. Tests reject title-only evidence, invalid offsets, unsupported
findings, incomplete dispositions, changed bytes and expanded page scope.
The export checker verifies its complete file inventory and hashes; it does not
establish transcription accuracy. Step 8 will integrate one scan pilot into a
separate reading-room export while preserving existing CD data and compatibility.

## Step 8: staged reading-room adapter

The pilot is now included in a separate version 3 data export at
`build/reading-room-pdf-pilot/data`. It is linked to its canonical November 1983
TOC entry and includes exact text/code, its figure, all nine scan regions, three
downloads, correction records and separate availability/review states. The
original portable package is copied intact under `data/source/pdf/<scan-id>/`.

```sh
make export-pdf-reader \
  PDF_READER_ARGS="--output build/reading-room-pdf-pilot-new/data"
PYTHONPATH=src python3 -m tools.reading_room.check \
  --data build/reading-room-pdf-pilot-new/data
diff -qr build/reading-room-pdf-pilot/data build/reading-room-pdf-pilot-new/data
```

The command defaults to the existing production data and pilot package. It
refuses existing outputs, validates in isolation and leaves its inputs intact.
The [static version 3 contract](READING-ROOM-STATIC-V3.md) documents identities,
path scopes, evidence fields and compatibility. Version 1/2 loading and existing
CD URLs remain supported; all 3,386 CD article summaries and original files are
preserved. No CD relationship is inferred for the pilot.

The complete repeat export is byte-identical. All 27 PDF tests, eight existing
web-export tests, six frontend tests and TypeScript checking pass. Step 8 proves
the data projection; scan-specific reader labels, review/evidence presentation
and browser acceptance are the next checkpoint, step 9.

## Step 9: read the pilot and its scan evidence

The existing application now supports scan-derived reading. The pilot's
availability and review scope are separate, remaining gaps stay visible, and
each body section links to its source regions. Selecting a region opens a
native-resolution image with contained scrolling and original-size/download
links. Other regions are not loaded automatically. Corrected prose, literal
code, figures, raw OCR and correction records remain separate.

```sh
make export-pdf-reader \
  PDF_READER_ARGS="--output build/reading-room-pdf-ui-new/data --covers covers"
READING_ROOM_OUTPUT=build/reading-room-pdf-ui-new READING_ROOM_BASE=/archive/ \
  npm --prefix web run build
READING_ROOM_OUTPUT=build/reading-room-pdf-ui-new READING_ROOM_BASE=/archive/ \
  npm --prefix web run preview -- --port 4178
```

The completed local site is `build/reading-room-pdf-ui/`; its preview is
`http://127.0.0.1:4178/archive/`. Open the pilot through November 1983's TOC,
metadata search or `#/articles/scan-maso-1983-11-toc-0012`. Region links append
`?region=r08`, for example. The standalone preview and original CD references
remain available. Production reader data is unchanged.

The staged site includes 27 covers, preserving owner images and all nineteen
newly installed PDF covers. Desktop/mobile, nested hosting, missing-state
fixtures, request isolation and CD regression routes pass. All 47 focused tests,
the production build and data integrity check pass. Browser review and closeout
are saved under `private/pdf-restoration/9-reader-ui/`; screenshots are under
`output/playwright/pdf-9/`. Step 10's batch/resume gate remains before bulk work.

## Step 10: bounded batch, resume and review preservation

`tools.pdf_restore.batch` runs regional OCR from mapped, existing TOC identities.
It does not locate articles, classify headings, transcribe corrections or assign
review status. Each named batch has a private request, an immutable `plan.json`,
an atomically saved `ledger.json`, and an independent content-addressed cache.
The qualification batch replays only the pilot, January 1988 and August 1991
samples: three articles, seven source pages, 35 regions (33 OCR jobs and two
figures). It does not expand the restoration queue.

Prepare a request before execution. Paths in its pins are repository-relative;
use `tools.pdf_restore.inventory.pin(ROOT, path)` to obtain hashes and sizes.
For example, a new mapped article's request has this structure:

```json
{
  "batch_id": "11-batch-01",
  "limits": {"articles": 2, "source_pages": 6, "lookup_pages": 20},
  "lookup_pages": [],
  "articles": [{
    "map": {"path": "private/pdf-restoration/11-batch-01/map.json",
            "sha256": "REPLACE_WITH_ACTUAL_SHA256", "bytes": 1234}
  }]
}
```

Use an optional `recipe` pin alongside `map` only for an already reviewed
package. Record inspected lookup pages as objects with `source_id` and one-based
`pdf_page`. Declare mapping targets and lookup limits in the checkpoint plan
before mapping. Record new mapping/review time and region counts as work happens;
historical sample mapping/review durations were not timed and must not be
inferred from OCR time. Keep unresolved mapping as an explicit separate outcome.
Two articles and six distinct source pages are the selected operating ceilings
for subsequent batches, with twenty lookup pages and one targeted retry per
failed region. The runner's absolute qualification limits remain three articles
and twelve pages; new requests should use the lower operating ceilings. Segment
long articles before OCR and close out the complete article separately.

Exact commands for the saved qualification batch are:

```sh
# Preparation refuses an existing state directory. Do this only once.
make prepare-pdf-batch
# Resume pending/interrupted tasks; verified successes are reused.
make resume-pdf-batch
# An optional deliberate checkpoint after four attempted regions:
make resume-pdf-batch PDF_BATCH_ARGS="--max-tasks 4"
# Publish evidence plus unchanged reviewed packages, into a fresh directory.
make export-pdf-batch
make check-pdf-batch
```

Defaults are `private/pdf-restoration/10-batch/request.json`, its sibling
`state/`, and `build/pdf-restoration/10-batch/`. Override `PDF_BATCH_REQUEST`,
`PDF_BATCH_STATE`, and `PDF_BATCH_OUTPUT` for a named batch or repeat export.
The cache defaults to `private/pdf-restoration/batch-cache`; set
`PDF_BATCH_ARGS="--cache <private-path>"` during preparation to choose another.
Resume/check exit with code 2 while any task is incomplete, including a deliberate
`--max-tasks` stop. Export can preserve partial outcomes but does not turn them
into readable articles. `make check-pdf-batch` requires completed OCR and a valid
export; inspect a partial export independently with:

```sh
PYTHONPATH=src python3 -m tools.pdf_restore.batch check \
  --output build/pdf-restoration/10-batch
```

A failed task is skipped on ordinary resumes while other regions continue.
After inspecting its saved `state/failures/<key>-<attempt>/` diagnostics, request
its sole targeted retry explicitly:

```sh
make resume-pdf-batch \
  PDF_BATCH_ARGS="--retry scan-EXISTING-TOC-ID/REGION-ID --reason 'record the bounded repair'"
```

A second failure remains deferred; further recovery requires a separately named
repair checkpoint. SIGINT/SIGTERM preserve an interrupted row. A killed process
may leave a `running` row and a dot-prefixed temporary directory; resume uses
only validated, atomically published cache directories. It recovers the row,
ignores incomplete temporary files and preserves successful regions. File locks
prevent concurrent runners from racing the same state or shared cache. Temporary
directories left by a hard kill can be inspected and cleaned up separately.

Each cache key includes the PDF hash, page geometry/rotation, that region's
coordinates and kind, page exclusions, pinned engine/model bytes and version,
renderer version/binary hash, Pillow version, processing implementation hashes,
and effective language/PSM/render configuration. Page exclusions invalidate all
regions on that page conservatively; an isolated region crop/configuration
change invalidates only that region. Notes and corrected reading text are not
OCR dependencies. A changed input or toolchain cannot silently alter an existing
plan: prepare a new request/state and reuse the same cache. Global configuration
uses `config`; per-article `region_config` maps region IDs to overrides, e.g.
`{"r01": {"psm": 7}}`. Only supported languages, PSM 3–13 and render scales
1000–6000 are accepted. Every cache hit rechecks hashes and complete inventories.

Exports contain a map and build-compatible `ocr-pageN/evidence.json` bundles for
each article, plus an outcome ledger and complete file manifest. Only eligible
region crops enter exports. TSV coordinates are relative to the crop; settings
record its page origin. Full-page scratch renders stay private. For new work,
review these bundles against scans, create a separate correction record and
package recipe as in step 5, then use `make build-pdf-article` and
`make check-pdf-article`. Never adopt new OCR as corrected text automatically.

When an existing recipe is supplied, batch export compares every crop, raw TXT
and TSV byte with the evidence used by that recipe. Only an exact match permits
a `reviewed/` rebuild from the original immutable recipe; its original OCR,
corrections, provenance and review limits remain intact. Otherwise the fresh
evidence is exported with `review_required: true` and no reviewed package.
Mapping changes require omitting the old recipe until the changed map is
reviewed. The original correction files remain available for post-production.

Qualification results, timings, synthetic failure ledgers, interruption and
invalidation evidence, and the bulk-readiness decision are saved under
`private/pdf-restoration/10-batch/`. Source-derived inputs and outputs stay
ignored. `make test-pdf` exercises batch behavior without real scans or an OCR
installation, including a killed child process and persistent failure/retry
limits. Review effort, rather than engine speed, determines batch sizing; an
OCR-complete outcome is never counted as restored or verified on that basis.

Step 10 is complete. All 35 real regions match the existing reviewed evidence;
the three reviewed packages and repeated batch exports are byte-identical.
The main export contains 345 files / 55,221,603 bytes. Successful regional work
totals 85.6 seconds, with 29.8 seconds in OCR; a complete-cache resume takes
about 0.6 seconds without new engine calls. These are replay measurements,
not new-article restoration estimates. All 37 focused PDF tests pass. The
full-repository check was stopped during an unrelated CD artifact audit and
is not claimed as passed. The saved bulk-readiness record admits the next
named November batch within the selected two-article/six-page ceilings.

## Step 11: November batches

`11-batch-01` restores existing entries `maso-1983-11-toc-0001` (opening
editorial) and `maso-1983-11-toc-0002` (minister interview). Open
`build/pdf-restoration/11-batch-01/index.html` or the local preview at
`http://127.0.0.1:4179/`. Both packages are readable/sample-reviewed and retain
separate raw OCR and `corrections.json` evidence. They contain no code listing.

The editorial occupies PDF13, with no visible printed folio. Its full printed
title is preserved separately from the shortened TOC label. The interview spans
PDF14–17 / printed12–15 and preserves mixed Korean/Hanja, three pull quotations,
two photographs and complete speaker/date/place metadata. Cross-column sentences
remain continuous. A localized syllable uncertainty and Hanja glyph-variant
limits are visible; period language and factual claims are not modernized.

The private inputs and records are under `private/pdf-restoration/11-batch-01/`.
The batch runner's immutable plan covers OCR; subsequent reviewed package recipes
live in its `editorial/` and `interview/` directories. The raw evidence export's
unreviewed status does not overwrite the later reviewed article outcomes.

```sh
# Existing state: resume/check without repeating successful OCR.
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-01/state
make check-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-01/state \
  PDF_BATCH_OUTPUT=build/pdf-restoration/11-batch-01-evidence

# Rebuild a reviewed article into a fresh directory; use interview for the other.
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-01/editorial/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-01-new/editorial
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-01-new/editorial

# Serve the completed two-article preview.
python3 -m http.server 4179 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-01
```

For a new bounded execution state, use `make prepare-pdf-batch` with
`PDF_BATCH_REQUEST=private/pdf-restoration/11-batch-01/request.json` and a fresh
`PDF_BATCH_STATE`; reuse the shared cache. Never overwrite an existing plan or
reviewed correction file to force a rerun.

All 37 focused PDF tests, two deterministic package rebuilds, complete asset
checks and desktop/mobile browser checks pass. Batch output totals 103 files /
20,530,372 bytes. The November issue ledger separately tracks four completed
articles, one group heading and 42 unresolved eligibility decisions among the
47 original TOC entries. This is a completed batch, not an issue closeout;
issue-wide staging and coverage reconciliation follow the remaining named batches.

### November batch 02

`11-batch-02` restores existing entries `maso-1983-11-toc-0014` (ENEMY SATELLITE,
PDF35 / printed33) and `maso-1983-11-toc-0015` (REVERSE, PDF36–37 / printed34–35).
Both are readable/sample-reviewed. Open `build/pdf-restoration/11-batch-02/index.html`
or the local preview at `http://127.0.0.1:4180/`.

The packages preserve three figures, all explanation text and downloadable BASIC
listings. ENEMY SATELLITE's dotted-leader annotations are separate reading text,
with their printed line associations recorded in `corrections.json`. Faint
operators and one prose uncertainty are marked. REVERSE's shared-page advertisement
is excluded. Printed code anomalies, prose/code discrepancies and physical listing
wraps remain intact. Exact spacing, border-star counts and glyph correspondence
remain unverified; these are transcription downloads, not tested executable code.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-02/state
make check-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-02/state \
  PDF_BATCH_OUTPUT=build/pdf-restoration/11-batch-02-evidence

# Rebuild into a fresh directory; use reverse for the other article.
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-02/enemy/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-02-new/enemy
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-02-new/enemy

python3 -m http.server 4180 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-02
```

Private mapping, transcriptions, corrections, validation and closeout records are
under `private/pdf-restoration/11-batch-02/`. The batch contains 125 files /
11,842,040 bytes. All 37 focused PDF tests, deterministic rebuilds, complete asset
checks and desktop/mobile browser checks pass. The November ledger now records
six restored articles, one group heading and 40 unresolved eligibility decisions;
the next checkpoint is `11-batch-03`, within the same two-article/six-page limits.

### November batch 03

`11-batch-03` restores `maso-1983-11-toc-0016` (원), PDF38–39 / printed36–37.
Open `build/pdf-restoration/11-batch-03/index.html` or `http://127.0.0.1:4181/`.
The article is readable/sample-reviewed, with both formulas, an illustration and
five independent captioned BASIC listings. Printed code wraps and discrepancies
are preserved; exact code spacing/glyphs and one prose reading remain unverified.

Its `corrections.json` includes selected `notable_corrections` examples alongside
the pinned raw/scan evidence and full reviewed blocks. A `listing_index` identifies
each listing's block, region and UTF-8 byte range in the combined `listing.txt`.
The byte range ends are exclusive and include blank-line separators. The download
contains five separate printed programs, not one executable program.

One crop edge was widened during review. The original `map.json`, `state/` and
`11-batch-03-evidence/` remain intact. Final recipes use `map-reviewed.json` and
evidence from `state-reviewed/`, which reused 22 regions and processed only r08.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-03/state-reviewed
make check-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-03/state-reviewed \
  PDF_BATCH_OUTPUT=build/pdf-restoration/11-batch-03-evidence-reviewed
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-03/circle/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-03-new/circle
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-03-new/circle
python3 -m http.server 4181 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-03
```

Output totals 104 files / 9,617,434 bytes. All 37 focused tests, deterministic
rebuild, asset checks and desktop/mobile checks pass. November now has seven
restored articles, one group heading and 39 unresolved eligibility decisions.
Next is `11-batch-04`: establish 잠수함's extent before admitting extraction;
split work into bounded checkpoints if it exceeds the six-source-page ceiling.

### November batch 04: partial 잠수함

`11-batch-04` restores the opening of `maso-1983-11-toc-0017` (잠수함),
PDF40–41 / printed38–39. The complete article occupies PDF40–47 / printed38–45;
the six continuation pages are observed but deferred. The package is explicitly
**partial/sample-reviewed**, with complete opening prose, three images and
listing lines 90–486. Open `build/pdf-restoration/11-batch-04/index.html` or
`http://127.0.0.1:4182/`.

The correction record retains selected OCR examples and listing byte ranges,
and adds `coverage` and `unresolved_graphics`. Fourteen editorial markers link
graphics-string occurrences to printed lines and pinned scan regions. Null
`encoded_bytes` and `character_count` mean unresolved; occurrence IDs are not
character codes. The partial listing preserves physical wraps and remaining
uncertainties and is not an executable reconstruction.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-04/state
make check-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-04/state \
  PDF_BATCH_OUTPUT=build/pdf-restoration/11-batch-04-evidence
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-04/submarine/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-04-new/submarine
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-04-new/submarine
python3 -m http.server 4182 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-04
```

The batch totals 62 files / 9,690,187 bytes. All 37 focused tests, deterministic
rebuild, asset checks and desktop/mobile checks pass. November has seven readable
articles, one partial article, one group heading and 38 unresolved eligibility
decisions. The partial article is not counted as a completed readable restoration.

PDF42 is physically upside down despite rotation metadata 0. The next checkpoint,
`11-orientation-repair`, must qualify explicit image correction while preserving
the source and its metadata, with one real page plus focused synthetic checks.
Its scope is saved in the private batch's `next-checkpoint.json`. After that repair
is committed, `11-batch-05` handles the six remaining pages within the existing
ceiling. A later aggregation checkpoint preserves one article identity and all
segment evidence while checking complete coverage; it performs no new extraction.

### Evidenced raster orientation correction

`11-orientation-repair` qualified PDF42 / printed40 with an explicit 180-degree
clockwise correction. The source PDF and its rotation metadata (0) remain
unchanged. The optional page field is separate from inventory geometry:

```json
"orientation_correction": {
  "clockwise_degrees": 180,
  "evidence": "The title, folio and listing are upside down in the source render."
}
```

Allowed corrections are 90, 180 and 270 degrees, with a nonblank observation.
Omit the field when no correction is needed. This additive schema change keeps
existing maps valid. `page_transform()` composes the source PDF rotation and
this correction; recompute `pdf_to_upright_normalized` when adding or changing
it. Map every region and exclusion against the corrected, upright image.
`width_pt`, `height_pt`, `MediaBox`, `CropBox` and `rotation` retain their original
inventory values, including for quarter-turn corrections that swap raster size.

Both OCR paths use a lossless pixel transpose after Poppler's metadata-aware
render and before exclusion masking and region cropping. Crop bounds and TSV
positions refer to that corrected image. The standalone `page.png` remains the
original Poppler render; `eligible-page.png` and region crops use the correction.
The batch runner keeps full page renders temporary and exports region evidence.

The pinned map, page evidence and regional OCR settings carry the correction.
Publication rejects missing or mismatched correction evidence, including page
evidence used for figures. Batch dependencies already include page geometry, so
changing a correction invalidates that page's tasks while unrelated pages can
reuse their cache. Changes to tool implementation also invalidate runtime pins:
older batch states cannot resume under this changed implementation. Keep those
states as historical evidence and prepare a fresh named state for new work.
Existing reviewed packages can still be checked or rebuilt from their recipes.

Qualification evidence is in `private/pdf-restoration/11-orientation-repair/`
and `build/pdf-restoration/11-orientation-repair-evidence/`. The four samples
check the title, first listing rows, last listing rows and folio, on one real
source page. Batch and standalone crops match pixel for pixel. Inspection
confirms upright title, folio40 and listing boundaries490–1817. Raw OCR still
contains errors and has not been promoted to reviewed transcription.

All 42 focused tests pass, covering composed rotations, invalid correction
records, exclusion masking, crops, selective cache invalidation and publication
provenance. Eight existing November packages pass integrity checks; the opening
segment rebuild remains byte-identical. No article availability or issue counts
changed in this repair.

The owner has authorized later manual correction of user-defined bitmap glyphs.
Continue with scan-linked markers and unresolved bytes/counts in `corrections.json`;
do not make decoding these glyphs a prerequisite for extraction. `11-batch-05`
will map and restore all six continuation pages, using r15+ IDs and the evidenced
correction on PDF42. The qualification windows are not a complete listing map.
Keep segment coverage partial until the separate eight-page assembly checkpoint.

### November batch 05: 잠수함 continuation

`11-batch-05` restores PDF42–47 / printed40–45 as a second segment of
`maso-1983-11-toc-0017`. The same article identity now has separate opening and
continuation packages. The continuation remains **partial/sample-reviewed**;
assembly is pending, with no further extraction required for these eight pages.
Open `build/pdf-restoration/11-batch-05/index.html` or
`http://127.0.0.1:4183/`.

The package contains 21 regions/blocks, including six repeated titles and fifteen
code blocks covering printed lines490–11360. Physical wraps and printed anomalies
remain visible. `corrections.json` supplies 20 selected correction examples,
15 listing byte ranges and 90 scan-linked unresolved graphics occurrences.
Null character codes/counts remain explicit; the owner will correct these later.

The new `glyph_definitions` index locates 38 printed character definitions by
declared code, printed line, scan pin and UTF-8 listing range. Repeated &H96, &H97
and &H87 definitions are preserved, including differing operands. These are
transcribed, unverified definitions, without inferred bitmap decoding or links
to graphics-marker byte identities. The listing is not an executable restoration.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-05/state-reviewed
make check-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-05/state-reviewed \
  PDF_BATCH_OUTPUT=build/pdf-restoration/11-batch-05-evidence-reviewed
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-05/submarine/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-05-new/submarine
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-05-new/submarine
python3 -m http.server 4183 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-05
```

The original map/state/export remain preserved. Crop review required one map
revision; `map-reviewed.json` and `state-reviewed/` contain the revised boundaries,
reusing six unchanged title tasks and regenerating fifteen code crops. No engine
failure or retry occurred. All 42 focused tests, deterministic rebuild, integrity
checks and desktop/mobile browser checks pass. Output totals 99 files /
24,031,393 bytes. All prior article packages remain unchanged.

November still has seven readable articles, one partial article, one group
heading and 38 unresolved eligibility decisions. Its ledger stores both segments
under the existing article and marks assembly pending. `11-submarine-assemble`
will combine them without new OCR: 35 regions, 38 blocks, three figures, seventeen
code ranges, 104 graphics occurrences and 38 definition entries. Assembly must
retain each segment's original map/OCR settings and review provenance, with
explicitly rebased scan references and listing offsets. Do not relabel historical
OCR as having been generated against a newly combined map. Full page coverage
may become readable while manual glyph corrections remain deferred and visible.

### Assemble reviewed segments without new OCR

`tools.pdf_restore.assemble` combines two to twelve disjoint, reviewed packages
for one source/TOC/article identity. The source inventory, original page geometry,
complete regional review, correction records and original OCR map/orientation
bindings must agree. Every segment must account for its included regions. The
explicit ordered page list must match exactly; overlapping pages, duplicate
identities and incomplete or unreviewed segments fail before publication.
Nested assemblies and comparison relationships require a separate adapter.

The default assembly recipe has these fields (the optional `index_mode` is described below):

```json
{
  "segments": [
    {"name": "opening", "manifest": {"path": "build/example-opening/manifest.json", "sha256": "<SHA-256>", "bytes": 123}},
    {"name": "continuation", "manifest": {"path": "build/example-continuation/manifest.json", "sha256": "<SHA-256>", "bytes": 456}}
  ],
  "expected_pdf_pages": [40, 41, 42, 43, 44, 45, 46, 47],
  "evidence": ["Evidence supporting complete article coverage and reading order."],
  "uncertainties": ["Remaining transcription and glyph limitations."],
  "resolved_notes": [
    {"segment": "opening", "note": "Exact superseded uncertainty from the original package.", "reason": "Evidence explaining why assembly resolves this note."}
  ]
}
```

Manifest paths are repository-relative pins. Segment names are unique lowercase
letters/digits/hyphens beginning with a letter. `resolved_notes` can be empty;
unlisted uncertainties remain visible. Original notes are retained unchanged
inside `segments/<name>/`, together with every original package file. The
combined `map.json` describes the union, while raw settings keep their original
map hashes. `assembly.json` and the saved recipe identify that distinction.

Reading order and literal code bytes are preserved. Combined `corrections.json`
rebases scans and UTF-8 listing/definition offsets, retains graphics occurrences
and records each source segment. The raw ZIP includes original OCR, positions,
settings, scans, maps, runtimes, provenance and corrections. `check-pdf-article`
also reconstructs the assembly from retained segments and compares its map,
correction indexes, article, downloads and rendered preview. It detects changed
projections even when the outer manifest has been rehashed. This is consistency
verification against pinned inputs, not cryptographic authorship verification.

```sh
make assemble-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-submarine-assemble/assembly-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-submarine-assemble-new/submarine
make check-pdf-article \
  PDF_OUTPUT=build/pdf-restoration/11-submarine-assemble-new/submarine
make test-pdf
python3 -m http.server 4184 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-submarine-assemble
```

The completed `11-submarine-assemble` checkpoint covers PDF40–47 / printed38–45:
35 regions, 38 blocks, 17 code blocks and three figures under the original article
identity. All 104 unresolved graphics markers and 38 printed glyph definitions
remain available for manual correction. Only four superseded scope/orientation
notes were resolved. The combined listing is the exact concatenation of the two
segment listings; original maps, OCR and segment packages remain unchanged.
No new PDF extraction, OCR, character decoding or historical program execution
was performed. The article is **readable/sample-reviewed**, with full page
coverage and explicit limits on character accuracy and executability.

The package has 164 files / 50,469,596 bytes, including retained segment exports.
All 48 focused tests pass, and a separate rebuild is byte-identical. The source,
TOC, inventory and all prior article files (647 pinned inputs) remain unchanged.
Desktop/mobile browser checks verify every block, all three figures, 39 asset
pins, listing/definition ranges and marker records. Actual index, download and
scan navigation passes; the downloaded listing matches the package bytes.
November now has eight readable, sample-reviewed articles, one group heading
and 38 unresolved eligibility decisions. The next checkpoint, `11-batch-06`,
establishes the extent of 체커 before bounded extraction; it does not reopen
잠수함's deferred bitmap correction.

### November batch 06: 체커

`11-batch-06` restores `maso-1983-11-toc-0018`, PDF48–51 / printed46–49.
The next article, AWARI, begins on PDF52 / printed50; that was the only outside
lookup page. The four-page package includes the illustrated opening, joined
three-column prose, five game/instruction screen images and the two-column BASIC
listing. The illustrated opening retains its overlaid title/introduction/credit
as one complete image; those text regions also have reading transcriptions.
Screens that continue across columns or pages retain their original boundaries.

There are 17 mapped regions, nine reading blocks, six figures and four code
blocks covering 73 numbered rows, 10–1880. The article is
**readable/sample-reviewed**. `corrections.json` records 17 selected OCR
corrections, four block ranges, 73 `listing_line_index` entries and twelve
`listing_anomalies`, each tied to a scan and UTF-8 listing range. The
`figure_sequence` records two board continuations. These indexes support later
manual review without inferring absent punctuation, repairing program logic or
executing the listing. Physical code wraps and printed anomalies remain visible;
exact spacing and ambiguous glyphs remain unverified.

Two crop revisions corrected header completeness, listing row boundaries and a
right margin. The original 17-task state and first revised state remain intact;
the first revision processed four regions and reused thirteen, then a six-pixel
split adjustment processed two and reused fifteen. Final evidence is in
`map-final.json`, `state-final/` and `11-batch-06-evidence-final/`. All three states
resume without changing their ledgers. No engine failures or retries occurred.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-06/state-final
make check-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-06/state-final \
  PDF_BATCH_OUTPUT=build/pdf-restoration/11-batch-06-evidence-final
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-06/checkers/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-06-new/checkers
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-06-new/checkers
python3 -m http.server 4185 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-06
```

The article package has 61 files / 16,320,406 bytes. A separate rebuild is
byte-identical, all 48 focused tests pass, and 815 pinned prior input files remain
unchanged. Package checks validate raw bytes, coverage, prose joining, image
order and all listing/correction ranges. No application or extraction code
changes were needed for this checkpoint.

Desktop/mobile checks verify all nine text blocks, all six figures, 21 asset
pins and the correction indexes. Actual index→article, listing-download and
scan navigation passes; downloaded bytes match. The batch wrapper totals
65 files / 16,338,741 bytes. Preview: `http://127.0.0.1:4185/`.
November now has nine readable/sample-reviewed articles, one group heading
and 37 unresolved eligibility decisions. Next is `11-batch-07`, AWARI; reuse its
observed PDF52 opening and verify its ending before bounded extraction.

### November batch 07: AWARI

`11-batch-07` restores `maso-1983-11-toc-0019`, PDF52–54 / printed50–52.
PDF55 opens the next TOC article and was the only outside lookup page. The
opening image was reused from batch06. The package includes ten reading blocks,
six figures and three code blocks covering 69 numbered rows, 5–999.

The example explanation continues from PDF52 to PDF54, across an illustrated
page. The reading block joins the split word and completes the explanation
before the illustration and three numbered gameplay panels. Regional transcripts
and both page references remain intact; `prose_joins` documents this placement.
The photo, board diagram, robot illustration and panels retain their source
order. `figure_sequence` records panel ranges ①–⑥, ⑦–⑫ and ⑬–⑯.

`corrections.json` retains 18 selected OCR corrections, three block ranges,
69 `listing_line_index` entries, twelve `listing_anomalies` and three
`text_review_items`. Printed spelling, unusual expressions, physical code wraps
and final prose counts remain as observed. Exact blank-string widths, ambiguous
glyphs and punctuation remain unverified. The package is
**readable/sample-reviewed**; no historical execution or semantic repair occurred.

An unsupported draft region kind was rejected during preparation, before OCR,
and corrected to `section-label`. Crop review processed four revised regions
and reused thirteen. A final photo-border adjustment processed one image and
reused sixteen regions, including all OCR results. The original, reviewed and
final maps/states/evidence exports are retained; all three completed states
resume without modifying their ledgers. There were no engine failures or retries.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-07/state-final
make check-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-07/state-final \
  PDF_BATCH_OUTPUT=build/pdf-restoration/11-batch-07-evidence-final
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-07/awari/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-07-new/awari
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-07-new/awari
python3 -m http.server 4186 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-07
```

The article package has 61 files / 13,893,668 bytes. A separate rebuild is
byte-identical, all 48 focused tests pass, and 880 pinned prior input files remain
unchanged. Package checks cover raw bytes, complete regional representation,
the prose join, figure order and all correction/listing offsets. No application
or extraction code changes were required.

Desktop/mobile checks verify all ten text blocks, all six figures, 21 asset
pins and the correction indexes. Actual index→article, listing-download and
scan navigation passes; downloaded bytes match. The batch wrapper totals
65 files / 13,912,077 bytes. Preview: `http://127.0.0.1:4186/`.
November now has ten readable/sample-reviewed articles, one group heading
and 36 unresolved eligibility decisions. Next is `11-batch-08`, 당신의 심장을
진단해 드립니다; reuse its observed PDF55 opening and verify the ending before
bounded extraction. Deferred submarine bitmap correction remains unchanged.

### November batch 08: 당신의 심장을 진단해 드립니다

`11-batch-08` restores `maso-1983-11-toc-0020`, PDF55–57 / printed53–55.
PDF58 opens the next article and was the only outside lookup. The opening image
was reused from batch07. The package contains thirteen reading blocks, one
illustration and eight code blocks covering 141 numbered rows, 10–1520.

The prose columns join at 고 + 형 지방, retaining both scan references and
regional transcripts. The illustration and its Microcomputing credit remain
available. Listing 780 continues across PDF56–57: `listing_line_index` retains
one global download range with two `segments`, each identifying its original
region, scan pin and UTF-8 range. Physical code wraps remain intact.

`corrections.json` includes 24 selected OCR corrections, eight block ranges,
141 line ranges, 25 listing anomalies and five prose review items. Original
spelling, duplicated wording, numeric references, age ranges and absent closing
quotes remain as printed. Exact whitespace, decorative asterisk counts,
ambiguous glyphs and punctuation remain unverified. The package is
**readable/sample-reviewed**; no historical execution or semantic repair occurred.

Crop revision processed five regions and reused ten. The original and reviewed
maps/states/evidence exports remain available; both states resume without
changing their ledgers. There were no engine failures or retries. Preparation
schema validation and an export blocked by the active OCR lock were resolved
before the completed export; neither was an OCR engine failure.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-08/state-reviewed
make check-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-08/state-reviewed \
  PDF_BATCH_OUTPUT=build/pdf-restoration/11-batch-08-evidence-reviewed
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-08/heart/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-08-new/heart
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-08-new/heart
python3 -m http.server 4187 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-08
```

The article package totals 68 files / 16,556,494 bytes; the wrapper/report totals
72 files / 16,576,347 bytes. A separate rebuild is byte-identical, all 48 focused
tests pass, and 945 pinned prior inputs remain unchanged. Desktop/mobile checks
verify all thirteen blocks, the illustration, 19 asset pins and correction
indexes. Actual article navigation, listing download and scan navigation pass;
downloaded bytes match. Preview: `http://127.0.0.1:4187/`.

November now has eleven readable/sample-reviewed articles, one group heading
and 35 unresolved eligibility decisions. Next is `11-batch-09`, the first bounded
segment of 도서관리 프로그램. Reuse its observed PDF58 opening; the TOC spacing
suggests a longer article, so preserve explicit deferred coverage within the
six-page limit. The ending is not yet verified. No application or extraction
code changes were needed; deferred submarine bitmap correction is unchanged.

### November batch 09: 도서관리 프로그램, segment 1

`11-batch-09` restores PDF58–63 / printed56–61 under `maso-1983-11-toc-0021`.
This is a **partial/sample-reviewed** article: the sentence continues on PDF64,
the only outside lookup, and the full ending remains unverified. The next TOC
entry does not establish the ending. The six-page checkpoint limit is unchanged.

The package contains 54 regions, 31 reading blocks and 15 figures: three
illustrations, nine menu examples, two tables and one flowchart, with twelve
caption pairs. There is no numbered code listing in this segment. Image interiors
remain available through full-resolution scan links. The reader illustration
overlaps a menu/caption; its rectangular crop preserves that overlap with an
explicit note instead of modifying the artwork.

`corrections.json` contains 27 selected OCR corrections, eleven text review
items, 31 UTF-8 text ranges and five prose joins. Original regional transcripts
and all contributing scan references remain available. The Catalog Enter prose
is placed after the intervening tables/flowchart, and the final sentence remains
unfinished with a visible continuation notice. Unusual printed wording and
ambiguous glyphs are retained for review.

Crop revisions processed seven tasks with 47 cache hits, then one figure with
53 cache hits. `state-reviewed/` was prepared but superseded without processing;
the original, final and final2 states all resume without changing their ledgers.
No engine failures or retries occurred. Final inputs use `map-final2.json` and
`state-final2/`.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-09/state-final2
make check-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-09/state-final2 \
  PDF_BATCH_OUTPUT=build/pdf-restoration/11-batch-09-evidence-final2
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-09/library-segment-01/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-09-new/library-segment-01
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-09-new/library-segment-01
python3 -m http.server 4188 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-09
```

The segment package totals 181 files / 30,192,570 bytes; the wrapper/report
totals 185 files / 30,234,337 bytes. A separate rebuild is byte-identical, all
48 focused tests pass, and 1,017 pinned prior files were preserved before the
intentional ledger update. Desktop/mobile checks verify all 31 blocks, 15 images,
57 asset pins, correction offsets and partial-coverage status. Actual article
navigation, text download and final scan navigation pass; downloaded bytes match.
Preview: `http://127.0.0.1:4188/`.

November now has eleven readable articles, one partial article, one group heading
and 34 unresolved eligibility decisions. Next is `11-batch-10`, segment 2 of the
same article starting at PDF64 / printed62. Preserve segment 1 and explicit
deferred coverage until the full extent is verified. No application or extraction
code changes were needed; deferred submarine bitmap correction is unchanged.

### November batch 10: 도서관리 프로그램, segment 2

`11-batch-10` restores PDF64–69 / printed62–67 under `maso-1983-11-toc-0021`.
The article remains **partial/sample-reviewed**. Segment 1 is preserved separately;
the two segments cover PDF58–69 without claiming complete coverage or assembly.
PDF70 is the sole outside lookup and continues the final SEARCH row.

There are 36 regions, thirty reading blocks, figure8 with its caption and ten
code blocks. The 342 numbered rows belong to three listings: CATALOG MASTER
has 66 rows (1–680), CATALOG ENTER has 244 (10–2440), and CATALOG SEARCH has
32 (10–320, last row incomplete). Printed gaps in numbering are not filled.

`corrections.json` uses `listing_id` together with `printed_line` to distinguish
repeated line numbers. Each of the 342 line entries points to its UTF-8 range
in `listing.txt`. ENTER190, 620, 950, 1870 and 2350 each have two source segments
within one global range. Thirty listing anomalies, eleven prose review items,
23 selected OCR corrections and thirty text ranges support manual review.
Physical code wraps and original spelling remain intact; exact whitespace,
decorative strings and ambiguous glyphs remain unverified. No execution or
semantic repair occurred.

Four prose joins retain regional transcripts and all scan references. The
opening continues segment 1's unfinished sentence. SEARCH320 ends at SE;
the following ARCH ON AUTHOR on PDF70 is recorded as deferred evidence.
The final enlarged-crop review corrected the draft table reference from 3 to 2;
the earlier builds remain in ignored review-draft directories.

Crop revisions processed fourteen prose regions, two code regions and one
wrapped heading, with 22/34/35 cache hits. Final inputs are `map-final3.json`
and `state-final3/`. All four completed states resume unchanged;
`state-reviewed/` was prepared only and superseded without processing.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-10/state-final3
make check-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-10/state-final3 \
  PDF_BATCH_OUTPUT=build/pdf-restoration/11-batch-10-evidence-final3
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-10/library-segment-02/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-10-new/library-segment-02
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-10-new/library-segment-02
python3 -m http.server 4189 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-10
```

The segment package totals 152 files / 31,321,476 bytes; the wrapper/report totals
156 files / 31,352,270 bytes. A separate final rebuild is byte-identical, all
48 focused tests pass, and 1,202 pinned prior files were preserved before the
intentional issue-ledger update. Desktop/mobile checks verify thirty blocks,
ten code containers, the figure, forty asset pins and all line ranges. Actual
article navigation, listing download and final scan navigation pass; downloaded
bytes match. Preview: `http://127.0.0.1:4189/`.

Issue counts remain eleven readable articles, one partial article, one group
heading and 34 unresolved eligibility decisions. Next is `11-batch-11`, segment 3
starting at PDF70 / printed68; retain SEARCH320's continuation provenance.
Ignore `tocs/` for now. No application or extraction code changes were needed;
deferred submarine bitmap correction remains unchanged.

### November batch 11: 도서관리 프로그램, segment 3

`11-batch-11` restores PDF70–75 / printed68–73 under `maso-1983-11-toc-0021`.
The article remains **partial/sample-reviewed**. Three separately preserved
segments cover PDF58–75; the full ending is still unverified. PDF76 is the sole
outside lookup and begins with BOOKSHELF200.

Eighteen regions produce fifteen code blocks and three listing captions, with
no figures. SEARCH contributes 350 visible numbered rows and a carried fragment
of 320; LIST contributes 42 rows, BORROW 95 and BOOKSHELF 19. This segment ends
SEARCH and includes complete LIST and BORROW listings, plus BOOKSHELF10–190.

`corrections.json` contains 507 local line ranges with listing identities and
occurrence identifiers. Its first entry marks the unnumbered SEARCH320 fragment
with `printed_line_visible: false`, linking the prior segment's manifest,
listing, byte range and scan provenance. The local transcript does not invent
a number. SEARCH1570 and BORROW740 each retain two current source segments.
Eighteen text ranges, fifteen code-block ranges, eleven selected OCR corrections,
33 listing anomalies and one caption review support manual post-production.

Printed numbering gaps, unusual SEARCH3445 and the caption spelling CATACOG
remain intact. The apparent SEARCH3190 continuation printed after 3200 stays
in physical order. Exact whitespace, decorative strings and ambiguous glyphs
remain unverified; no execution or semantic repair occurred.

All eighteen OCR tasks completed without crop revisions, engine failures or
retries. A no-op resume preserves the state ledger and raw evidence.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-11/state
make check-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-11/state \
  PDF_BATCH_OUTPUT=build/pdf-restoration/11-batch-11-evidence
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-11/library-segment-03/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-11-new/library-segment-03
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-11-new/library-segment-03
python3 -m http.server 4190 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-11
```

The segment package totals 83 files / 29,156,445 bytes; the wrapper/report totals
87 files / 29,175,443 bytes. A separate rebuild is byte-identical, all 48 focused
PDF tests pass, and 1,358 prior file pins were preserved before the intentional
issue-ledger update. Background desktop/mobile browser checks verify all blocks,
22 asset pins and 507 line ranges. Actual article navigation, listing download,
code scrolling and final scan navigation pass; downloaded bytes match.
Preview: `http://127.0.0.1:4190/`.

Issue counts remain eleven readable articles, one partial article, one group
heading and 34 unresolved eligibility decisions. Next is `11-batch-12`, segment 4
starting with BOOKSHELF200 at PDF76 / printed74. Ignore `tocs/` for now. Deferred
submarine bitmap correction is unchanged; no application or extraction code
changes were needed.

### November batch 12: 도서관리 프로그램, segment 4

`11-batch-12` restores PDF76–81 / printed74–79 under `maso-1983-11-toc-0021`.
The article remains **partial/sample-reviewed**. Four separately preserved
segments cover PDF58–81, twenty-four pages; the full ending is still unverified.
PDF82 is the sole outside lookup and continues SC SEQ LIST6 line240.

Twenty regions produce nineteen code blocks and one caption, with no figures.
The 309 visible numbered rows comprise BOOKSHELF200–1370 (118 rows), complete
SC SEQ LIST0–5 (28 rows each, 10–290), and LIST6's opening (23 rows, 10–240).
BOOKSHELF's opening remains in segment 3; LIST6's final included row is partial.

`corrections.json` records eight listing identities and 309 line ranges.
Two printed BOOKSHELF590 rows retain distinct occurrence and line IDs; 580 is
not invented. Missing90 in the SC SEQ programs is also preserved. BOOKSHELF950,
LIST2's110 and280, LIST3's220 and LIST6's40 each retain two source segments.
Twenty text ranges, nineteen code-block ranges, eighteen selected OCR corrections,
43 listing anomalies and one caption review support manual post-production.
Original DATA strings and printed misspellings remain intact, including the
caption's SEO versus code SEQ. Exact spaces and ambiguous glyphs remain unverified;
no execution or semantic repair occurred.

Two left crop margins were widened to retain clipped line-number digits. The
final run processed two tasks with eighteen cache hits. Both completed OCR states
resume unchanged; both evidence exports are retained. A final enlarged scan
check corrected the physical wrap of BOOKSHELF1310's opening parenthesis. Earlier
packages remain in ignored review-draft directories. Final inputs use
`map-final.json` and `state-final/`.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-12/state-final
make check-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-12/state-final \
  PDF_BATCH_OUTPUT=build/pdf-restoration/11-batch-12-evidence-final
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-12/library-segment-04/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-12-new/library-segment-04
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-12-new/library-segment-04
python3 -m http.server 4191 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-12
```

The segment package totals 91 files / 32,516,920 bytes; the wrapper/report totals
95 files / 32,537,804 bytes. A separate final rebuild is byte-identical, all 48
focused PDF tests pass, and 1,445 prior file pins were preserved before the
intentional issue-ledger update. Background desktop/mobile browser checks verify
all blocks, 24 asset pins and 309 line ranges. Actual article navigation, listing
download, code scrolling and final scan navigation pass; downloaded bytes match.
Preview: `http://127.0.0.1:4191/`.

Issue counts remain eleven readable articles, one partial article, one group
heading and 34 unresolved eligibility decisions. Next is `11-batch-13`, segment 5
at PDF82 / printed80, preserving the carried LIST6 line240 and verifying the
remaining article boundary locally. Ignore `tocs/` for now. Deferred submarine
bitmap correction is unchanged; no application or extraction code changes
were needed.

### November batch 13: 도서관리 프로그램, final segment

`11-batch-13` restores PDF82–83 / printed80–81 under `maso-1983-11-toc-0021`.
LIST9 DATA290 closes on PDF83, and the sole outside lookup, PDF84 / printed82,
visibly opens GUN MAN. The article's full extent is now verified as PDF58–83 /
printed56–81. Five separate segments cover these twenty-six pages without gaps
or overlaps. Availability remains **partial/sample-reviewed** pending assembly.

Seven code regions produce seven blocks, without figures or captions. There are
89 visible numbered rows: LIST6's250–290 and complete LIST7–9, 28 rows each.
The carried, unnumbered LIST6 line240 fragment makes ninety local line-index
entries. Its record pins segment 4's manifest, listing, corrections, exact byte
range and source segments. No local line number was inserted. LIST7's180 and
LIST8's130 each retain two current source regions.

`corrections.json` contains seven text ranges, seven code-block ranges, ninety
line ranges, six selected OCR corrections and twenty listing anomalies. LIST7
prints170 twice, with the second occurrence after180; occurrence and line IDs
preserve both. Missing190 and90 are not supplied. Original spelling, DATA strings
and physical wraps remain intact. Exact whitespace and ambiguous glyphs remain
unverified; no execution or semantic repair occurred.

The r01 bottom margin was widened around LIST6 DATA290's separate closing quote.
The final run processed one task with six cache hits. Both completed states
resume unchanged, and both evidence exports are retained. Final inputs use
`map-final.json` and `state-final/`.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-13/state-final
make check-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-13/state-final \
  PDF_BATCH_OUTPUT=build/pdf-restoration/11-batch-13-evidence-final
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-13/library-segment-05/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-13-new/library-segment-05
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-13-new/library-segment-05
python3 -m http.server 4192 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-13
```

The segment package totals 39 files / 11,313,954 bytes; the wrapper/report totals
43 files / 11,326,701 bytes. A separate rebuild is byte-identical, all 48 focused
PDF tests pass, and 1,540 prior file pins were preserved before the ledger update.
Background desktop/mobile checks verify all blocks, eleven asset pins and ninety
line ranges. Actual article navigation, listing download, code scrolling and
final scan navigation pass; downloaded bytes match.
Preview: `http://127.0.0.1:4192/`.

Next is `11-library-assemble`: combine the five saved segments without new OCR.
Namespace repeated region/block IDs, retain all text and listing correction
indexes, and resolve carried SEARCH320 and LIST6 line240 with explicit original
provenance. Superseded segment-coverage notes must be resolved while transcription
uncertainties remain visible. The saved plan expects 135 regions, 106 blocks,
51 code blocks and sixteen figures. GUN MAN follows as `11-batch-14` at PDF84 /
printed82. November counts remain eleven readable articles, one partial article,
one group heading and 34 unresolved eligibility decisions. Ignore `tocs/` for
now; deferred submarine bitmap work remains unchanged.

## Step 11 library assembly: regional and line correction indexes

`11-library-assemble` combines the five reviewed 도서관리 프로그램 segments,
PDF58–83 / printed56–81. PDF84 opens GUN MAN, as recorded in the prior boundary
review. The result is readable/sample-reviewed: 26 pages, 135 regions, 106 blocks,
51 code blocks and sixteen figures. No new source pages or OCR tasks are used.

For segments that reuse IDs and supply regional text and physical listing indexes,
add `"index_mode": "namespaced-v1"` to the assembly recipe. Default recipes retain
the original projection, so earlier assembled exports still validate unchanged.
Namespaced mode requires a text index covering every block and a line index that
partitions each segment's listing download. It rejects invalid identities, scans,
UTF-8 ranges, incomplete line coverage and inconsistent carried-line evidence.

The combined `corrections.json` provides:

- `identity_map`: original segment, kind and ID mapped to a unique combined ID.
  Region, block and figure references use these IDs; original OCR settings still
  refer to the immutable original maps.
- `text_index` and `text_review_items`: ranges in combined `article.txt`, computed
  from the actual UTF-8 reading order, including namespaced figure placeholders.
  Each retains its original `source_range` and `source_segment`.
- `listing_index`: code-block ranges in combined `listing.txt`. The download is
  the exact concatenation of original listing bytes, including physical wraps.
- `listing_line_index`: all 1,248 local physical line entries, with unique local
  row IDs, original occurrence IDs, source ranges and rebased regional scan spans.
  `logical_line_id` associates each entry with the combined numbered line.
- `logical_listing_line_index`: 1,246 numbered lines across sixteen programs.
  `source_parts` links the local entries. SEARCH320 and SC SEQ LIST6 line240 each
  have two parts. Joining these index ranges adds no printed number, removes no
  newline and repairs no code. Duplicate BOOKSHELF590 and LIST7 170 retain distinct
  occurrence IDs in printed order.
- 126 `listing_anomalies`, 24 prose/caption review items, nine local `prose_joins`,
  the figure sequence, image overlap notes and regional transcriptions.
  `resolved_continuations` records two verified code fragment links and one prose
  link. The prose retains its original reading blocks and block separator.
- `listing_groups` and `segment_continuations` preserve segment-scoped declarations;
  they do not claim newly inferred program completeness. Original continuation
  evidence is explicitly labelled as original. `segments[].original_metadata`
  retains numbering reviews, policies and any additional review metadata.

Each original package, including its complete corrections, remains byte-for-byte
under `segments/<name>/`. `segments[].original_corrections` links its portable pin.
Carried-line verification checks the prior manifest, listing and correction hashes,
exact prior byte range, scan spans, listing identity, number and adjacency. The
combined raw archive retains the original map/settings binding. The checker derives
all combined indexes again from the retained originals, catching index tampering
that only updates outer hashes. Historical notes remain scoped to their segments;
superseded scope notes are resolved only by exact original text and a recorded reason.

```sh
make assemble-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-library-assemble/assembly-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-library-assemble/library
make check-pdf-article \
  PDF_OUTPUT=build/pdf-restoration/11-library-assemble/library
make test-pdf
```

Use a fresh output directory for rebuilding. Assembly does not certify exact glyphs,
spacing or executable BASIC. November now has twelve readable/sample-reviewed
articles, one group heading and 34 unresolved eligibility decisions. Next is
`11-batch-14`, GUN MAN at PDF84 / printed82, with the existing six-page extraction
limit and boundary review before assigning its extent. `tocs/` remains out of scope.

## Step 11 batch 14: GUN MAN

`11-batch-14` restores the clearly identified GUN MAN page, PDF84 / printed82,
under `maso-1983-11-toc-0022`. It contains the platform/title, supplier credit,
callout, three introductory paragraphs, program explanation, original title
illustration and a framed BASIC listing ending at 2490 GOTO2000. PDF85 is an
uncaptioned photograph without explicit continuation text; its article ownership
remains unresolved and it is retained only as boundary evidence. PDF86 / printed84
opens MARK. The readable/sample-reviewed scope is the identified GUN MAN page;
it does not assert ownership of the neighboring photo.

Ten regions produce nine reading blocks and one figure. Platform/title crops
intentionally overlap the preserved illustration so their text is accessible
without erasing the original labels. The one code block contains fifty numbered
rows, 2000–2490, across 51 physical lines: 2430 wraps before `4, BF`. No line number
or physical continuation is invented. Nine regional text ranges, fifty line
ranges, two prose review items, nine selected OCR correction examples and 25 code
review notes remain in `corrections.json` with pinned scans and raw evidence.

Review notes cover SPRITE hex runs, I/1 and 0/O distinctions, faint horizontal
strokes, 2390's2809, 2400's `J NEXT`, 2450's `FORM-203` and 2480's `FORV-0`. These are
provisional scan readings, not syntax repairs. The explanation's printed `우측`
for 2140–2170 also remains unchanged. Exact glyphs, whitespace and executable
correctness remain unverified; sprite bytes were not inferred from expected shapes.

```sh
make resume-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-14/state-mapped
make check-pdf-article \
  PDF_OUTPUT=build/pdf-restoration/11-batch-14/gun-man
make test-pdf
python3 -m http.server 4194 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-14
```

One source page and two outside lookup pages were used. The completed state
resumes unchanged; ten crop tasks and nine text OCR outcomes completed with no
engine failures or retries. Raw evidence is retained in
`build/pdf-restoration/11-batch-14-evidence/`. The package contains 48 files /
7,567,902 bytes and has a byte-identical independent rebuild. All 51 focused PDF
tests pass; all 2,144 prior file pins matched before the intentional ledger update.
Desktop/mobile checks verify nine DOM blocks, one figure, fourteen asset pins,
all text and line ranges, literal listing downloads and horizontal code scrolling.
Preview: `http://127.0.0.1:4194/`.

November now has thirteen readable/sample-reviewed articles, one group heading
and 33 unresolved eligibility decisions. Only GUN MAN's entry changed. Next is
`11-batch-15`: map MARK from PDF86 / printed84, check the education heading's
eligibility without duplicating article content, and establish the ending within
the existing one-article/six-source-page ceiling. The neighboring photo remains
unassigned. `tocs/` and deferred submarine bitmap correction stay out of scope.

## Step 11 batch 15: MARK

`11-batch-15` restores 기능이 강화된 성적관리프로그램 MARK,
`maso-1983-11-toc-0024`, across PDF86–88 / printed84–86. The final listing ends
at 3560 END; PDF89 / printed87 opens 유효숫자를 18로. The parent 교육입문
(`maso-1983-11-toc-0023`) is a TOC grouping with no separately identified body
here. Its ownership decision is saved independently. The uncaptioned PDF85 photo
remains unassigned; neither the grouping nor MARK claims it.

Fifteen regions produce twelve reading blocks and one original flowchart. A
repeated running header is excluded. Two prose joins connect the opening columns
and a sentence continuing onto the next page around the diagram; original regional
transcriptions remain available. The flowchart and its caption retain separate
reading items, and its internal labels remain in the source image.

The BASIC download contains an inline `3560 END` example and the full 244-row
program, distinguished by `mark-inline-example` and `mark` listing identities.
Together they have 245 indexed rows and 249 physical lines. Rows 1705, 1715, 1725
and 1735 retain their physical wraps. Printed numbering gaps, MATHMATICS, music
strings and unusual operators are preserved without semantic repair. Exact spaces,
quotes and faint letter/digit distinctions remain unverified.

`corrections.json` retains twelve text ranges, four code-block ranges, all 245 line
ranges, 144 line review notes, four prose review items and thirteen selected OCR
correction examples. The output label at 3320 is explicitly marked
`⟦판독불확실:출력표시⟧`; `unresolved_text` links its exact UTF-8 range and scan,
with the original characters unresolved. This is an editorial marker, not source
code. No program execution or bitmap reconstruction was performed.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-15/state
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-15/mark
make test-pdf
python3 -m http.server 4195 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-15
```

The checkpoint uses three source pages and one outside lookup. Fifteen crop tasks
and fourteen text OCR outcomes completed with zero engine failures or retries;
code crops used scale 4000. The completed state resumes unchanged. Raw evidence is
saved under `build/pdf-restoration/11-batch-15-evidence/`. The package contains
68 files / 14,034,712 bytes and has a byte-identical independent rebuild. All 51
focused PDF tests pass, and all 2,196 prior pins matched before the ledger update.
Desktop/mobile checks cover the reading order, flowchart, nineteen asset pins,
all indexed ranges, marker visibility, literal downloads and code scrolling.
Preview: `http://127.0.0.1:4195/`.

November now has fourteen readable/sample-reviewed articles, two group headings
and 31 unresolved eligibility decisions. Only MARK and its education grouping
changed. Next is `11-batch-16`, 유효숫자를 18로 from PDF89 / printed87. Establish
its actual ending and split before exceeding six source pages; the next TOC start
is not proof of extent. Ignore `tocs/`; deferred submarine bitmap work is unchanged.

## Step 11 batch 16: 유효숫자를 18로

`11-batch-16` restores `maso-1983-11-toc-0025` across PDF89–91 / printed87–89.
PDF92 is a separate software submission notice. Another bounded lookup confirms
1차방정식 at PDF111 / printed109; the intervening pages were not assigned to this
article. The education parent remains a grouping, without a duplicate body.

Sixteen regions produce eleven reading blocks, three code blocks and three
original annotated frames. The three-column explanation has two sentence joins.
Original listing images retain every margin label and bracket, with separate
literal code and label transcriptions. The 86 numbered rows occupy 121 physical
lines, including 32 wrapped rows. Numbers, strings and operators split across
printed lines remain split. Line 10260's apparent SA$ stays as read; 10480 is
followed by 10500, and 10845 remains between 10840 and 10850. No missing number is
invented or historical program executed or repaired.

`corrections.json` contains eleven text indexes, three listing-block indexes,
86 line indexes, 49 line review notes, four prose review items and thirteen
selected OCR corrections. Its fourteen `margin_annotations` records include
exact label byte ranges in `article.txt`, associated listing-line IDs and pinned
bracket scans. Labels are explanatory text, not inserted BASIC comments. Exact
blank widths, repeated asterisks and faint glyphs remain manual-review work.

```sh
make resume-pdf-batch \
  PDF_BATCH_STATE=private/pdf-restoration/11-batch-16/state-reviewed
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-16/digits18/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-16-new/digits18
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-16-new/digits18
python3 -m http.server 4196 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-16
```

Final mapping uses `map-reviewed.json`; only a preliminary numbering note changed,
with all geometry retained. The final state reuses all sixteen cached crops and
thirteen text outcomes and resumes unchanged. There were no engine failures or
retries. Both evidence exports remain under `build/pdf-restoration/`, with suffixes
`11-batch-16-evidence` and `11-batch-16-evidence-reviewed`. Original raw OCR, scans
and positions remain unchanged; settings retain their corresponding map pins.

The package has 66 files / 24,285,466 bytes and a byte-identical independent rebuild.
All 51 PDF tests pass. The 2,452 preserved input pins matched before the ledger
update. Desktop/mobile checks cover all content, figures, twenty asset pins,
text/line and margin ranges, scrolling, actual downloads and scan links. The
private recipe's initial scope-note shadowing was corrected before the final
build and browser review; every final scope note is checked in the DOM. The
3,454-byte listing download matches exactly, and the final scan loads at 1686×3276.
Only favicon.ico returned 404. Preview: `http://127.0.0.1:4196/`.

November now records fifteen readable/sample-reviewed articles, two group
headings and 30 unresolved eligibility decisions. Next is `11-batch-17`,
1차방정식 from PDF111 / printed109, within the existing six-source-page ceiling.
This checkpoint does not close the issue or perform deferred bitmap correction.

## Step 11 batch 17: 1차방정식

`11-batch-17` restores `maso-1983-11-toc-0026` across PDF111–115 / printed109–113.
Its listing ends on PDF114, while figure3 continues through both columns of
PDF115. PDF116 is an unrelated advertisement. A handoff lookup confirms the next
article at PDF118 / printed116; PDF117 remains uninspected here.

The 31 regions yield 21 reading blocks, eight code blocks and six images. These
include the original equation, terminology table, problem-selection screen and
three consecutive output frames. The table also has fifteen accessible English/
Korean pairs. Output frames remain original images; their mathematical results
were not recalculated or mixed into source code.

There are 184 main-program rows and two separately identified inline 348 examples,
occupying 334 physical lines. All 113 wrapped rows retain their breaks. Lines 264
and 418 each have two scan-backed segments in `listing_line_index`; their byte
ranges cover the column continuation without adding a repeated number. The two
inline examples and main program have three independent `listing_id` values.
`mixed_inline_regions` retains the boundary between the examples' AND text and
Korean connecting prose. `table_rows` indexes all fifteen term pairs, preserving
the printed PERPENCULAR spelling. The correction record also holds 129 line notes,
five prose review items and fourteen selected OCR corrections. Exact spaces,
repeated equals, faint glyphs, line 144's 60 and line 384's U8 remain review items.
No program execution or semantic repair was performed.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-17/state-final
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-17/equation/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-17-new/equation
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-17-new/equation
python3 -m http.server 4197 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-17
```

Final mapping uses `map-final.json`. Two crop revisions widened four listing
regions to preserve complete edge rows; only those regions were reprocessed.
All 31 tasks and 25 text outcomes completed with no engine failures or retries.
Initial, reviewed and final evidence exports remain under `build/pdf-restoration/`
as `11-batch-17-evidence`, `11-batch-17-evidence-reviewed` and
`11-batch-17-evidence-final`. All completed states resume unchanged; unaffected
raw OCR, position and scan bytes match.

The 117-file package is 28,689,965 bytes and rebuilds identically. All 51 PDF tests
pass; the 2,824 preserved pins matched before the ledger update. Desktop/mobile
checks validate all content, six figures, 35 asset pins, text/line/table ranges,
column continuations and review notes. All eight code containers scroll without
page overflow. The actual 7,997-byte listing download matches, and the final scan
opens at 1129×3460. Only favicon.ico returned 404. Preview: `http://127.0.0.1:4197/`.

November now records sixteen readable/sample-reviewed articles, two group
headings and 29 unresolved eligibility decisions. Next is `11-batch-18`,
마이크로 컴퓨터 시스템입문 from PDF118 / printed116, within the six-page limit.
This is an article checkpoint, not issue closeout or deferred bitmap correction.

## November microcomputer systems checkpoint

`11-batch-18` restores `maso-1983-11-toc-0027`, 마이크로 컴퓨터 시스템입문,
across PDF118–120 / printed116–118. Its closing references and figure3 precede
the next article at PDF121. The existing TOC identity is retained. The six-chapter
outline announces a series; this article covers chapter1's definition, components
and history. It is `readable / sample-reviewed`, with explicit transcription limits.

Twenty-two regions produce fourteen reading blocks, one photograph and three
original diagrams. Three prose joins reconnect four column/page boundaries,
including 사/용자가 and 기능/(SUBROUTINE CALL). Figure3 follows the programming
explanation in reading order; original source geometry stays in the map. The
opening photograph includes the overlapping callout. Printed diagram labels,
historical dates, specifications, chip names and prices remain unchanged.

`corrections.json` preserves regional text, fourteen exact UTF-8 block ranges,
seven localized review items, five selected OCR correction examples and four
`reference_index` records. Each numbered reference has its transcription, exact
`article.txt` range and source scan. These are scan transcriptions, not externally
verified bibliography. Faint glyphs and punctuation remain manual review scope.
There is no code listing or `listing.txt` download for this article.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-18/state-final
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-18/micro-system/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-18-new/micro-system
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-18-new/micro-system
python3 -m http.server 4198 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-18
```

Initial OCR completed 22 crop tasks and eighteen text outcomes with no engine
failures or retries. Review widened r02 to include its whole callout and r08/r19
to retain edge glyphs; only those three tasks were reprocessed. Initial and final
maps/evidence exports remain saved. Both completed states resume unchanged, and
unaffected scan/OCR bytes match. The recipe uses `map-final.json` and final bundles.

The 86-file package is 16,240,666 bytes and rebuilds identically. All 51 PDF tests
pass; 3,237 preserved input pins matched before the ledger update. Desktop/mobile
checks validate all content, four images, 25 asset pins and text/reference ranges,
with no page overflow. The actual 9,106-byte article download matches, and the
final diagram scan opens at 2351×516. Only favicon.ico returned 404. Preview:
`http://127.0.0.1:4198/`.

November now records seventeen readable/sample-reviewed articles, two group
headings and 28 unresolved eligibility decisions. Next is `11-batch-19`,
영어학습용 프로그래밍 from PDF121 / printed119, displayed as 영어 학습용 프로그램.
Establish its ending within the six-source-page limit. This checkpoint does not
close the issue or perform deferred bitmap correction.

## November English-learning program checkpoint

`11-batch-19` restores `maso-1983-11-toc-0028`, 영어학습용 프로그래밍, across
PDF121–125 / printed119–123. The displayed title is 영어 학습용 프로그램.
The listing ends with 3000 END; PDF126 opens the separate Pascal article.
Availability is `readable`, verification `sample-reviewed`, with exact code
spacing, faint glyphs and executable correctness explicitly unverified.

Twenty-two regions produce eighteen reading blocks and two original figures:
the 8421 bitmap grid and an execution sample. The complete main listing has 201
numbered rows; a separate inline 730 example describes fifty questions instead of
the main program's twenty. Nine code blocks contain 238 physical lines, including
33 wrapped rows. The target 1210 in 1130 remains physically split as 1/210;
its bare 210 continuation is not indexed as a new statement. Similarly, a wrapped
`1 )` in a character definition belongs to its preceding statement.

`corrections.json` contains eighteen text ranges, nine code-block ranges, 202
numbered-row ranges, 124 line review notes, five prose review items and eleven
selected OCR correction examples. Twenty `data_index` records identify the
English exercises in 2500–2690; nine `glyph_definitions` records identify the
printed character codes and twelve transcribed row terms. Each has exact UTF-8
listing ranges and scans. These records support manual review without changing
printed choices such as form, grammar such as did you ate, music strings, missing
THEN or unusual assignments. No program execution or semantic repair was done.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-19/state
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-19/english/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-19-new/english
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-19-new/english
python3 -m http.server 4199 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-19
```

All 22 crop tasks and twenty text OCR outcomes completed without engine failures
or retries. Completed state resumes unchanged. The 93-file package is 28,560,616
bytes and rebuilds identically. All 51 PDF tests pass; 3,743 preserved input pins
matched before the ledger update. Validation covers all regions, original
geometry, raw archive bytes, prose joins and text/line/DATA/glyph intervals.
Browser acceptance caught missing visible scope notes in the private recipe;
the final package displays all six notes and validates them against corrections.

Desktop/mobile checks pass for all eighteen DOM blocks, two images, 26 asset
pins and the correction indexes. Eight long code containers scroll without page
overflow; the short inline example fits. The actual 9,929-byte listing download
matches and the final scan opens at 2228×2152. Only favicon.ico returned 404.
Preview: `http://127.0.0.1:4199/`.

November now has eighteen readable/sample-reviewed articles, two group headings
and 27 unresolved eligibility decisions. Next is `11-batch-20`, 파스칼 프로그램
1(연재) from PDF126 / printed124, within the six-source-page limit. Step 11 remains
active until every TOC entry is classified, each eligible article has an outcome,
and the standalone issue reference has been exported and inspected.

## November Pascal programming checkpoint

`11-batch-20` restores `maso-1983-11-toc-0029`, 파스칼 프로그램 1(연재), across
PDF126–131 / printed124–129. The displayed title is 파스칼 프로그래밍 1.
References end on PDF131; PDF132 opens the separate editor article. Availability
is `readable`, verification `sample-reviewed`, with exact glyphs, code spacing
and executable correctness explicitly unverified.

Eighty regions produce66 reading blocks and seven images: two facing-page cartoon
fragments and IF, REPEAT, WHILE, FOR and CASE syntax diagrams. Twenty independent
examples/templates contain134 physical code lines. Each has its own listing_id;
Fortran's two printed100 statement labels are distinguished from physical line
ordinals. Pascal and its BASIC/Fortran comparisons remain separate examples.

`corrections.json` contains66 text ranges,20 code-block ranges,134 line ranges,
22 line review notes, five prose review items and twelve selected OCR corrections.
Five formulae and six references have exact UTF-8 ranges and scans. Six prose
joins and one cross-column converter join preserve regional transcriptions.
Printed END;, Single roots is, WHILE-END, reversed comment braces, mathematical
operators and the value/scale explanation remain reviewable. No historical,
bibliographic or semantic correction and no program execution was performed.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-20/state-final
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-20/pascal/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-20-new/pascal
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-20-new/pascal
python3 -m http.server 4200 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-20
```

Both initial and final OCR states completed80 crops/73 text outcomes without
engine failures or retries and resume unchanged. Twenty-five tight crop edges
were widened in map-final.json. Only those tasks were reprocessed. Reused202
scan/OCR artifacts match;49 reused settings change only the package/map hash.
Original maps, crops, OCR and the final evidence export remain saved.

The310-file package is31,357,253 bytes and rebuilds identically. All51 PDF tests
pass;4,560 preserved input pins matched before ledger update. Validation covers
all regions, source geometry, raw archive bytes, joins and every correction range.
Desktop/mobile checks validate66 DOM blocks, seven images,84 asset pins and all
six visible scope notes. Eleven long code containers scroll without page overflow;
actual horizontal scrolling reaches390px. The actual3,382-byte listing download
matches and the final reference scan opens at897×666. Only favicon.ico returned404.
Preview: `http://127.0.0.1:4200/`.

November now records nineteen readable/sample-reviewed articles, two group
headings and26 unresolved eligibility decisions. Next is `11-batch-21`, 에디터를
만드는 법, observed PDF132 / printed130. Verify its extent from scans and split
before exceeding six source pages. Step11 still requires complete TOC accounting,
outcomes for every eligible article and the staged standalone issue reference.

## November editor article, first segment

`11-batch-21` restores segment 01 of `maso-1983-11-toc-0030`, 에디터를 만드는 법,
across PDF132–137 / printed130–135. Scans verify the full article through PDF140
/ printed138, ending with BASIC1300 above an advertisement. PDF141 opens MICRO
COMPUTER GRAPHIC. The segment is `partial / sample-reviewed`; the last three
pages and separate assembly remain required before complete-article status.

Forty-two regions produce 26 reading blocks, ten original diagrams/captions and
one code block. The prose covers the editor design, linked lists, storage pool
and commands through INSERT. The first 32 numbered BASIC rows (10–320) occupy
37 physical lines. Four wrapped rows retain their printed layout, including
180's G/OTO split. Remaining330–1300 appear on later source pages.

`corrections.json` records 26 text ranges, one code range, 32 numbered-row ranges,
18 line notes, twelve prose review points and ten selected OCR corrections.
Six prose joins retain regional text. Printed model names, Responce, inconsistent
figure references, &HZD and differing pointer-variable forms remain linked to
scans. Exact I/1 and O/0 glyphs, decorative symbol counts, string spaces and
executable correctness remain unverified. No semantic repair was performed.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-21/state-final
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-21/editor-segment-01/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-21-new/editor-segment-01
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-21-new/editor-segment-01
python3 -m http.server 4201 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-21
```

Both OCR states completed 42 crops / 32 text outcomes without failures or retries
and resume unchanged. Six edge corrections use map-final.json and final bundles.
Only those crops were reprocessed. Reused 126 scan/OCR artifacts match; 30 reused
settings change only the map/package hash. Original evidence remains saved.

The 149-file package is 30,971,394 bytes and rebuilds identically. All 51 PDF tests
pass; 6,748 preserved input pins matched before ledger update. Checks cover all
regions, geometry, raw archive bytes, joins and correction ranges. Desktop/mobile
checks pass for all blocks, ten images, 46 pins and visible partial/review scope.
The code scrolls without page overflow; actual horizontal scrolling reaches500px.
The actual 1,367-byte listing download matches and the final scan opens at869×495.
Only favicon.ico returned404. Preview: `http://127.0.0.1:4201/`.

November now has nineteen readable and one partial article, two group headings
and 25 unresolved eligibility decisions. Next is `11-batch-22`, editor segment02
at PDF138–140: remaining explanations, two diagrams and BASIC330–1300, with the
bottom advertisement excluded. Complete the separate assembly afterward, then
continue toward full November accounting and the staged issue reference.

## November editor article, second segment

`11-batch-22` restores PDF138–140 / printed136–138 under the same article identity
`maso-1983-11-toc-0030`. Twelve mapped regions produce eight reading blocks,
including four code blocks, and two original diagrams/captions. DELETE/OUTPUT
explanations and the closing accompany figures3-3/3-4 and BASIC330–1300. The
advertisement below1300 is excluded. PDF141 opens MICRO COMPUTER GRAPHIC.

The98 numbered BASIC rows span103 physical lines. Wrapped490/500/550/570 retain
split identifiers and strings. `corrections.json` includes eight text ranges,
four code ranges,98 line ranges,50 line notes,three prose review points and ten
selected OCR corrections. Two column joins retain regional text. TE in400 is
provisionally read and flagged; I/1, O/0, exact spaces, decorative symbol counts
and executable correctness remain unverified. No semantic repair was performed.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-22/state.json
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-22/editor-segment-02/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-22-new/editor-segment-02
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-22-new/editor-segment-02
python3 -m http.server 4202 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-22
```

All twelve OCR tasks / ten text outcomes completed without failures or retries;
the completed state resumes unchanged. The53-file package is13,190,987 bytes and
rebuilds byte-identically. All51 PDF tests pass; all7,808 preserved pins matched
before ledger update. Checks cover all regions, geometry, raw archives, reading
order, joins and correction ranges. Browser checks pass at1440×1000 and360×800:
eight blocks, two diagrams,16 asset pins, all review scope and correction ranges.
All four code blocks scroll without page overflow; actual scrolling reaches500px.
The3,410-byte listing download matches, and the final scan opens successfully.
Preview: `http://127.0.0.1:4202/`.

Both immutable editor segments are now ready for separate assembly. The article
remains partial until that checkpoint validates all nine pages together. November
counts remain nineteen readable, one partial, two headings and25 unresolved
eligibility decisions. Step11 continues through every entry and issue closeout.

## November editor article assembled

`11-editor-assemble` combines the two immutable editor segments under existing
identity `maso-1983-11-toc-0030`. Complete PDF132–140 / printed130–138 coverage is
now `readable / sample-reviewed`. No new OCR or source pages were processed.
The54 regions produce34 reading blocks, twelve original diagrams and five code
blocks. BASIC10–1300 has130 numbered rows over140 physical lines; eight wrapped
statements retain their original segment bytes.

Namespaced corrections retain34 text ranges,15 prose review points,130 local and
logical line ranges,68 line notes and eight prose joins. Four partial-scope notes
are explicitly resolved in the assembly. Both original packages, their maps,
settings and correction files remain byte-identical; unresolved glyph, spacing
and source-code concerns stay visible. No cross-segment fragment repair is needed.

```sh
make assemble-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-editor-assemble/assembly-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-editor-assemble-new/editor
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-editor-assemble-new/editor
python3 -m http.server 4203 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-editor-assemble
```

The213-file article is66,463,279 bytes and rebuilds byte-identically. All8,064
preserved pins,202 copied originals and188 raw archive members match. Validation
checks full page coverage, reading order and every projected range. Tooling is
unchanged; the immediately preceding batch22 run passed all51 PDF tests.

Browser checks pass at1440×1000 and360×800 for34 blocks, twelve diagrams,58 pins,
all correction ranges and visible scope. Superseded partial notes are absent
from the combined review panel and preserved in the originals. Five code blocks
scroll without page overflow; actual scrolling reaches500px. The4,777-byte listing
download matches and the rebased final scan opens at2204×1520. Desktop/mobile
screenshots were inspected. Preview: `http://127.0.0.1:4203/`.

November now has twenty readable/sample-reviewed articles, no partial articles,
two group headings and25 unresolved eligibility decisions. Next is11-batch-23,
MICRO COMPUTER GRAPHIC atPDF141 / printed139; establish its ending from scans.
The complete issue accounting and staged issue reference remain required.

## November MICRO COMPUTER GRAPHIC first segment

`11-batch-23` restores PDF141–146 / printed139–144 under existing TOC identity
`maso-1983-11-toc-0031`, with `partial / sample-reviewed` availability. Scans
verify the whole article through PDF149 / printed147. PDF150–151 are advertisements;
PDF152 starts 정보레이다. The final phrase 「더우기 직선을 」 continues on PDF147
as 「그리기 위해서」; the correction records retain that boundary for assembly.

All39 regions were inspected; eleven crops were refined with initial evidence
preserved. The26 reading blocks include five independent BASIC examples with36
numbered rows, alongside ten original diagrams, tables and graphics. Three
cross-column prose joins retain regional transcriptions. `corrections.json`
records26 text ranges, five listing ranges,36 line ranges,15 code notes, eleven
prose review points, four figure notes and ten selected OCR corrections. Printed
COLRS,14366, PRINT TAB punctuation, the R/T discrepancy and address/coordinate
claims remain scan-linked without semantic repair.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-23/state-final.json
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-23/graphic-segment-01/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-23-new/graphic-segment-01
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-23-new/graphic-segment-01
python3 -m http.server 4204 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-23
```

Initial/final OCR each completed39 tasks /29 text outcomes without failures;
completed states resume unchanged. The137-file article package is38,636,128 bytes
and rebuilds byte-identically. All51 PDF tests pass, all8,508 preserved input pins
match, and all region, geometry, archive and correction-range checks pass.

Browser checks pass at1440×1000 and360×800 for26 blocks, ten figures,43 pins and
correction ranges. Five code blocks scroll without page overflow; actual scrolling
reaches100px. The802-byte listing download matches, and the last source scan opens
at886×321. Desktop diagram/mobile code screenshots were inspected. Preview:
`http://127.0.0.1:4204/`.

November now has twenty readable articles, one partial article, two headings and
24 unresolved eligibility decisions. Next is11-batch-24 for PDF147–149, followed
by separate assembly. Full issue accounting and staged issue inspection remain.

## November MICRO COMPUTER GRAPHIC final segment

`11-batch-24` restores PDF147–149 / printed145–147 as the second immutable
`partial / sample-reviewed` segment of `maso-1983-11-toc-0031`. The opening prose
continues segment01; two column joins retain regional text. Figure6, three tables
and the closing graphic remain original images. All32 regions and two refined
code crops were inspected. Both OCR states complete32 tasks /27 text outcomes
without failures and resume unchanged.

The25 reading blocks include nine code blocks:52 numbered rows, seven unnumbered
commands and four printed ellipsis rows. Animation rows80/110 each retain three
physical lines; marginal Korean notes remain aligned with their printed rows.
Printed HPOLT,CONTOL,$0056/$00E6 and the absent150 row are preserved without repair.
Corrections include63 line ranges,26 line notes, eleven prose review points,
three figure notes and twelve selected OCR corrections.

Assembly now accepts explicit `row_kind: "unnumbered"` rows with a null printed
number, `printed_line_visible: false`, and a positive physical-line identity.
It keeps each as an independent logical row and rejects carried-line evidence
on these rows. Existing numbered continuation checks remain in force. This
supports immediate commands and printed ellipses without inventing line numbers.
Two focused regression tests and the full53-test PDF suite pass; a real projection
of both segments preserves all99 indexed rows and the cross-segment prose link.

```sh
make resume-pdf-batch PDF_BATCH_STATE=private/pdf-restoration/11-batch-24/state-final.json
make build-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-batch-24/graphic-segment-02/package-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-batch-24-new/graphic-segment-02
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-batch-24-new/graphic-segment-02
python3 -m http.server 4205 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-batch-24
```

The124-file package is17,919,256 bytes and rebuilds byte-identically; all9,157
preserved pins match. Browser checks pass at1440×1000 and360×800 for25 blocks,
five figures,36 pins and correction ranges. Six code blocks scroll on mobile
without page overflow. The1,640-byte listing download matches; the closing scan
opens at852×208. Preview: `http://127.0.0.1:4205/`.

Both segments cover all nine pages but the article remains partial until the
separate `11-graphic-assemble` checkpoint. Counts remain twenty readable, one
partial, two headings and24 unresolved eligibility decisions.

## November MICRO COMPUTER GRAPHIC assembled

`11-graphic-assemble` combines both immutable segments under TOC identity
`maso-1983-11-toc-0031`. Complete PDF141–149 / printed139–147 coverage is now
`readable / sample-reviewed`. No new OCR or source-page processing was required.
The71 regions produce51 reading blocks, fifteen figures/tables/graphics and
fourteen code blocks. All88 numbered rows, seven immediate commands and four
ellipsis rows are preserved over103 physical lines, including two wrapped rows.

Namespaced corrections retain99 local/logical row ranges,41 code notes,22 prose
review points and five regional prose joins. The sentence crossing segments is
explicitly linked. Four superseded scope notes are resolved; seven figure notes
remain available in original segment metadata and correction files. Original
packages, scans, maps and settings stay byte-identical. Glyph, spacing, gutter
shadow and printed-source concerns remain visible for manual correction.

```sh
make assemble-pdf-article \
  PDF_RECIPE=private/pdf-restoration/11-graphic-assemble/assembly-recipe.json \
  PDF_OUTPUT=build/pdf-restoration/11-graphic-assemble-new/graphic
make check-pdf-article PDF_OUTPUT=build/pdf-restoration/11-graphic-assemble-new/graphic
python3 -m http.server 4206 --bind 127.0.0.1 \
  --directory build/pdf-restoration/11-graphic-assemble
```

The272-file article package is85,028,522 bytes and rebuilds byte-identically.
All10,030 protected pins,261 copied source files and247 raw archive members match.
Validation checks full page order and every correction range. The unchanged
tooling uses batch24's immediately preceding successful53-test run.

Browser checks pass at1440×1000 and360×800 for51 blocks, fifteen figures,75 pins,
all correction ranges and visible review scope. Eleven code blocks scroll on
mobile without page overflow. The2,442-byte listing download matches; the rebased
last scan opens at852×208. Preview: `http://127.0.0.1:4206/`.

November now has twenty-one readable articles, no partial articles, two headings
and24 unresolved eligibility decisions. Next is11-batch-25 for 정보레이다 at
PDF152 / printed150. Full issue accounting and staged inspection remain required.

## Complete issue references and staged reader exports

After all eligible articles have outcomes and segmented articles are assembled,
`tools.pdf_restore.issue` validates the complete canonical TOC against the issue
ledger. It rejects omitted entries, duplicate/unlisted bodies, unresolved
eligibility, inconsistent outcome counts and invalid parent section anchors.
The standalone output copies every immutable article package, adds a47-entry
November TOC and creates reading pages using the existing preview renderer.
Reading pages link to the issue, previous/next article, downloads and original
scan evidence. Child section entries link to the one parent's heading anchor.

```sh
make export-pdf-issue PDF_ISSUE_ARGS="--base build/reading-room/data --ledger private/pdf-restoration/11-november/issue-progress.json --output build/pdf-restoration/11-closeout"
make export-pdf-issue-reader PDF_ISSUE_ARGS="--base build/reading-room/data --ledger private/pdf-restoration/11-november/issue-progress.json --output build/reading-room-pdf-november/data"
```

Both commands require fresh output directories. `accounting.json` and the
standalone manifest record separate article availability, verification, group
heading and section-reference counts. Every original package retains its own
manifest and correction evidence. The reader export copies the CD baseline once
and validates all added documents and unchanged CD files before publication.
See [the version3 contract](READING-ROOM-STATIC-V3.md#complete-scan-issues) for
section navigation, accounting fields and staged preview commands.
