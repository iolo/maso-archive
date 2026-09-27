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
