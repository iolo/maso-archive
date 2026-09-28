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
