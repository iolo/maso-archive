# Reading room

Storage: [what to preserve and where new work belongs](STORAGE.md). Historical paths remain available through compatibility links.

## Unified volunteer reading room — October 19, 2026

The current combined release is `dist/reading-room/`. It includes all nine
completed PDF issues through October 1984 and the CD1/CD2/CD3 collection.
For hosting through a secret share URL, see
[Deploy to Cloudflare R2 and Workers](DEPLOY-READING-ROOM.md).

| PDF issue | Article records |
| --- | ---: |
| 1983-11 | 35 |
| 1984-02 | 37 |
| 1984-03 | 38 |
| 1984-05 | 36 |
| 1984-06 | 38 |
| 1984-07 | 36 |
| 1984-08 | 37 |
| 1984-09 | 37 |
| 1984-10 | 35 |
| PDF total | 329 |
| CD1 / CD2 / CD3 total | 3,386 |

There are **3,715 article records**, 3,707 text downloads and 3,423 code listings
across 152 navigation records. Empty library TOCs and native CD date groups keep
their original identities; these are not 152 distinct printed issues. Known partial
and unavailable states remain visible. This integration adds no human acceptance.

```sh
python3 -m http.server 4189 --bind 127.0.0.1 --directory dist/reading-room
```

Open <http://127.0.0.1:4189/#/review?issue=maso-1984-10> for October's volunteer
queue, or <http://127.0.0.1:4189/#/issues/maso-1984-10> for its contents.
The shelf is at `#/`. Queue filters persist in the URL; lists load 60 entries
at a time. PDF articles retain scan comparisons, original OCR, code, figures and
correction evidence; CD articles retain text, code and original attachments.

Open **검토 메모** above an article or scan region. Name is optional; choose
**검토 중**, **수정 제안**, or **대조 완료**, and describe the location, current
text, proposed correction and evidence. Notes autosave in this browser's local
storage. Blocked/full storage gives feedback; an individual memo can still be
exported. Regional notes stay with their region and do not mark a whole article
checked. Current-text correction proposals take priority in the queue.

**내 검토 기록 내려받기** exports saved notes as UTF-8 JSON for delivery to the
coordinator through your usual channel. There is no submission server, shared
queue, account, assignment or automatic official approval. Notes belong to this
browser and origin, including port: export before moving hosts or clearing storage.
The app does not import notes. Text/package fingerprints identify stale notes;
old-text notes do not count toward current personal progress.

### Reproduce and validate

The October export uses the preserved September reader at
`archive/releases/reading-room-2026-10-16-september/data/` and integration ledger
`archive/pdf/1984-10/evidence/reader-integration-2026-10-19/export-ledger.json`.
All 35 inputs come from October's standalone package. No canonical title mappings
were required. All 5,218 original package files copy exactly. All 124,113 inherited
files outside the catalog/search/manifest and October issue/media indexes remain
unchanged. The original October closeout, OCR and corrections are preserved.
August's four hash-pinned validation adapters remain required by the checker.

Use a fresh output consistently:

```sh
make export-volunteer-reading-room VOLUNTEER_OUTPUT=dist/reading-room-volunteer-rebuild
make check-volunteer-reading-room VOLUNTEER_OUTPUT=dist/reading-room-volunteer-rebuild
make build-volunteer-reading-room VOLUNTEER_OUTPUT=dist/reading-room-volunteer-rebuild
make preview-volunteer-reading-room VOLUNTEER_OUTPUT=dist/reading-room-volunteer-rebuild VOLUNTEER_PORT=4190
```

The verified snapshot is `archive/releases/reading-room-2026-10-19-october/`, with
its sibling SHA-256 receipt. `make restore-volunteer-reading-room` selects it by
default and refuses an existing output. Set `VOLUNTEER_OUTPUT=dist/recovered-reader`
to restore alongside the current build. The September release and previous local
reader at `dist/reading-room-before-october-2026-10-19/` remain preserved.
To reproduce September, use its saved August base and integration ledger recorded
under `archive/pdf/1984-09/evidence/reader-integration-2026-10-16/`; select its
saved release with `VOLUNTEER_RELEASE=reading-room-2026-10-16-september`.

`VOLUNTEER_BASE` defaults to `./`: serve the entire output directory with an
ordinary static HTTP server, at its root or inside a subdirectory. Data/assets
resolve relative to `index.html`; hash navigation needs no rewrite or SPA fallback.
`make preview-volunteer-reading-room` is optional. For an intentional absolute
base, the static host must serve the output at that URL prefix.

October's 41 TOC entries resolve to 35 readable, sample-reviewed articles and six
non-owning headings. Human proofreading, news/classified body transcription,
source bytes and historical execution remain unverified. The restoration's batch
35 preflight timing exception remains in its original records.

Browser review caught and corrected an author-display bug: correspondent bylines
in an article without a canonical author now stay beside their questions, rather
than using the first correspondent as the author and hiding the others. Canonical
authors still retain their printed role when a matching byline is available.
Article records, original text and source packages are unchanged.

The full data checker, prior-file preservation checks, nine focused Python tests,
25 frontend tests, TypeScript and production compilation pass. Browser checks
cover October's contents, Q&A correspondents, original scan/corrected-text review,
actual text/code/image downloads, the volunteer queue and mobile layout.
Evidence, implementation pins and logs are preserved under
`archive/pdf/1984-10/evidence/reader-integration-2026-10-19/`.
Data manifest SHA-256: `d22f323dfd07d258158af0d50db863266dcce0652da2a2328827c5988f5f6d0f`.

The reader is prepared locally; this update did not deploy it.

The historical previews below describe earlier datasets and remain intact.

## Complete July routed-OCR review preview

The [July review preview](http://127.0.0.1:4188/archive/#/issues/maso-1984-07)
contains all **36 articles across 225 source pages**, including complete code
listings, the 19-page industry history and advertising index. All 42 contents
entries are accounted for: 36 readable articles and six group headings. Every
article remains pending human acceptance.

Choose **원문과 나란히 검토하기 →**, then **쪽 / 영역** to compare a corrected
region with its scan. Original OCR, correction notes and uncertainties remain
available. Copy a region URL when reporting a correction. This is a read-only
preview; opening an article does not approve it.

The fresh output is `dist/reading-room-routed-july-complete`, staged with
`tools.reading_room.scan_issue` from `dist/reading-room-qwen-june-complete/data`
and `archive/pdf/1984-07/restoration/12-1984-07-comparison/whole-issue-ledger.json`.
It preserves all 184 earlier scan articles and the CD collection, for 220 scan
articles total. The data manifest SHA-256 is
`b5b05a2968da1bc75b6c88622d284d55a7bd49b4e3ffce2d295d4e341c05357c`.

```sh
cd web
READING_ROOM_OUTPUT=dist/reading-room-routed-july-complete READING_ROOM_BASE=/archive/ npm run preview -- --port 4188 --strictPort
```

Full dataset integrity, prior-file preservation, TOC accounting and production
build passed. All 19 frontend tests and seven metric tests passed. Browser checks
covered the 36-article contents page, code article, region navigation, original
OCR disclosure, loaded scans, mobile layout without page overflow, and the final
region of the assembled history. No browser errors were observed in the resumed
review session. Private results and screenshots remain ignored by Git.

See [July accounting](ocr-experiments/ocr-july-accounting.json), [progress](ocr-experiments/ocr-july-progress.json)
and the [OCR decision report](OCR-JULY-DECISION.md). June's separate preview remains
unchanged. Human review, uncertain glyph resolution and code execution validation
remain distinct from this completed restoration-and-preview delivery.

## Complete June Qwen review preview

The [complete private June reader](http://127.0.0.1:4187/archive/#/issues/maso-1984-06)
contains all 38 article bodies across 216 source pages, including the complete
23-page computer-industry history, contest appendix and advertisement index.
All 45 contents entries are accounted for: 38 articles and seven group headings.
Human acceptance remains pending for every article. Refresh an already-open
browser tab to load the complete collection.

Choose **원문과 나란히 검토하기 →** from an article. **쪽 / 영역** and the
previous/next links move between scans. The view shows corrected text beside the
source, with zoom, correction notes, uncertainties and expandable original OCR.
On mobile, the scan sits above the text. Article tables retain empty cells and
scroll horizontally. Copy a region's URL when reporting a correction. The preview
is read-only; browsing does not save an approval or edit.

Graphic-character placeholders in the rebellion game, faint punctuation and
printed technical errors remain flagged. Readable does not mean character-perfect
or executable. The packages retain 325 explicit unresolved-text flags; that is a
review aid, not an exhaustive count of errors.

To restart the complete build:

```sh
cd web
READING_ROOM_OUTPUT=dist/reading-room-qwen-june-complete READING_ROOM_BASE=/archive/ npm run preview -- --port 4187 --strictPort
```

The final staging uses `tools.reading_room.scan_issue` with the private
`archive/pdf/1984-06/restoration/12-1984-06-qwen/whole-issue-ledger.json`, starting from
`dist/reading-room-restored/data` in a fresh output. The checked result is
`archive/pdf/1984-06/restoration/12-1984-06-qwen/reader-complete-result.json`.
Complete data manifest SHA-256:
`551f16c995adf82bbd366e69167e022bf3363b98199e60e60439e3788fef8b7a`.
Use a fresh output for any further staging; each package and ledger is pinned.

This preview preserves the previous 146 scan articles and CD collection. Earlier
June preview directories and the one-article phoneme preview at port4186 remain
unchanged. Data and screenshots remain ignored by Git. [Progress](ocr-experiments/ocr-june-progress.json)
and [whole-issue accounting](ocr-experiments/ocr-june-accounting.json) record package pins and
validation. Full dataset integrity, prior-file preservation, complete TOC
accounting and the production build passed. Browser checks cover the 38-article
issue page, assembled history, appendix tables and source/correction views with
human-pending notices and retained source ambiguities. No frontend code changed.

## Review completed PDF issues

`dist/reading-room-restored/` combines the original CD collection with all
four completed PDF issues: November 1983 (35 articles), February 1984 (37),
March 1984 (38) and May 1984 (36). The 146 scan-derived articles retain their
original text, code, figures, region evidence and independent review states.
March's word-processor article is partial because source pages 250–251 are
absent. The other 145 scan-derived articles are readable; all are sample-reviewed.

```sh
cd web
READING_ROOM_OUTPUT=dist/reading-room-restored READING_ROOM_BASE=/archive/ npm run preview -- --port 4184 --strictPort
```

Open `http://127.0.0.1:4184/archive/`. Issue routes are
`#/issues/maso-1983-11`, `#/issues/maso-1984-02`, `#/issues/maso-1984-03` and
`#/issues/maso-1984-05`. Select an article from its TOC or reading list. Each
article provides text/listing downloads and links to its original scan regions.
“복원 기록” opens the preserved JSON record; data-only restorations do not
require or advertise a separate HTML preview.

To reproduce from the existing validated February reader and completed ledgers,
use fresh output directories (the exporter refuses existing data outputs):

```sh
PYTHONPATH=.:src python3 -m tools.reading_room.scan_issue --base dist/reading-room-pdf-february/data --ledger archive/pdf/1984-03/restoration/12-1984-03/issue-progress.json --output dist/reading-room-restored-march/data
PYTHONPATH=.:src python3 -m tools.reading_room.scan_issue --base dist/reading-room-restored-march/data --ledger archive/pdf/1984-05/restoration/12-1984-05/issue-progress.json --output dist/reading-room-restored/data
cd web
READING_ROOM_OUTPUT=dist/reading-room-restored READING_ROOM_BASE=/archive/ npm run build
```

The exporter validates both complete datasets and preserves existing CD and
previously staged issue bytes. Source packages, restoration ledgers and the older
reader builds remain unchanged. These generated reader assets are private and
ignored by Git. June's separate ongoing trial is described above.

## CD baseline

The static reading room combines the completed **CD1, CD2 and CD3** references.
It contains **3,378 readable texts from 3,386 candidates**, with browsing,
metadata search, figures, source downloads and explicit review states.
CD text is a secondary transcription pending comparison with paper magazines.

| Source | Issue/date groups | Candidates | Readable texts | UTF-8 listings |
| --- | ---: | ---: | ---: | ---: |
| CD1 | 122 library issues | 1,088 | 1,080 | 3,125 |
| CD2 | 12 native date groups | 1,330 | 1,330 | 87 |
| CD3 | 18 native groups | 968 | 968 | 0 (code stays in article text) |
| Combined | 152 | 3,386 | 3,378 | 3,212 |

The 5,299 library TOC entries still cover 1983-11–1993-12. CD2/CD3 groups have
no invented TOC links. CD3 includes anomalous 1994/1996 labels and an undated
group; overlapping labels remain separate by disc. These 152 navigation groups
are not a claim of 152 distinct printed issues.

## Build the local archive

From the repository root, with the private `archive/cd1/reference/`,
`archive/cd2/reference/`, `archive/cd3/reference/`, `archive/toc/current/`, and CD1 reviewed
issue packages present:

```sh
cd web && npm ci && cd ..
make export-reading-room
make check-reading-room
make build-reading-room
cd web && npm run preview
```

Open the local preview address shown by Vite. The complete static site is in
`dist/reading-room-cd/`: `index.html`, hashed frontend assets and the prebuilt
`data/` tree. It needs ordinary static file hosting, with no application server
or API. A direct `file://` browser opening is not supported by the SPA because
browsers restrict local JSON fetches. The older
`archive/cd1/reference/index.html` remains the direct-file reader.

The export refuses a TOC snapshot that does not match the completed reference's
input hashes, and verifies CD2/CD3 file inventories and hashes before copying.
It builds and checks a staging tree before replacing reading-room data, so
missing or changed inputs leave the previous data usable. It does not change
the references, extraction records or publisher sources.
The generated reader data and source assets stay under ignored `dist/` and
must be handled as private content. A checkout without those folders can still
build and test the synthetic demo:

```sh
cd web && npm ci && cd ..
make demo-reading-room
cd web && READING_ROOM_OUTPUT=dist/reading-room-demo npm run preview
```

The demo deliberately uses invented article titles, code and a simple SVG. Its
prepared, recovered, gap, blocked and unmatched cases exercise the same reader.
It lives under `dist/reading-room-demo/`, separate from the real archive.

For development, run `npm run dev` in `web/` after exporting data. Vite serves
the selected build data through its local development middleware. Set
`READING_ROOM_OUTPUT=dist/reading-room-demo` to develop against the demo.

## Add or replace cover images

Put donated JPEGs in the private `covers/` directory as **`YYMM.jpg`**:

```text
covers/8311.jpg  → November 1983
covers/9001.jpg  → January 1990
covers/9509.jpg  → September 1995
```

`YY` means `19YY`; months must be 01–12. Exports select donated images first,
then verified front-cover candidates from `archive/pdf/shared/restoration/covers/`,
then the existing placeholder. PDF eligibility requires the pinned review,
visible date, and candidate hash; `masoYYMM.*` filenames alone are ignored.
PDF preparation and visual review remain a separate workflow. A corrupt donation
fails the export instead of silently selecting a PDF image. Missing source
folders are supported. June 1991 currently has neither source.

Every selected image is decoded and re-encoded as an RGB JPEG at quality 80,
within 480 × 640 pixels, preserving proportions without cropping or upscaling.
EXIF orientation is applied, embedded color profiles are converted to sRGB,
and source metadata is stripped. Donated originals stay unchanged and must
never be committed or served. Private manifests and rebuildable thumbnails
live under ignored `archive/covers/derivatives/`; only derivatives are copied into
`dist/reading-room-cd/data/covers/`. Content-sensitive filenames change when source
bytes or transform settings change.

After adding, replacing or removing a donation:

```sh
make prepare-cover-thumbnails  # Optional: export also prepares all supplied dates.
make export-reading-room
make check-reading-room
make build-reading-room
```

Preparation validates a staged derivative set before replacing the previous one.
CD1 and aggregate exports likewise validate staged readers before replacement.
An export refresh clears obsolete cover assignments and removes stale assets;
a frontend build alone does not refresh data. Dates outside the catalog are
prepared but do not create issues. `coverInputs` describes only public derivatives;
`counts.covers` counts assigned navigation groups and `counts.coverAssets` counts
unique images. Failed image loads retain the placeholder.

Custom export paths use `READING_ROOM_ARGS`, for example
`make export-reading-room READING_ROOM_ARGS="--covers /path/to/covers"`.
Use `--pdf-cover-checkpoint` and `--cover-thumbnails` for alternative private
checkpoint/cache directories. An absent checkpoint disables PDF fallback.
The preparation command uses `COVER_ARGS` and calls its cache option `--thumbnails`.
The synthetic demo never consumes private sources.

Scan staging accepts `--covers` to refresh baseline covers using this same
priority and validation. With no cover refresh requested, it preserves the
baseline, including legacy covers; that copy is not a completed cover migration.
The checker enforces derivative rules for `coverPolicy: thumbnail-v1` outputs;
`--require-thumbnails` additionally rejects unmigrated baselines. Baseline integrity
checks remain available without that option.

After reader checks and browser inspection pass, retire paired legacy JPEGs:

```sh
make cleanup-legacy-covers                    # Writes archive/covers/evidence/cover-cleanup.json; no deletion.
make cleanup-legacy-covers COVER_ARGS=--apply  # Applies the existing report after revalidation.
```

Cleanup requires exact `masoYYMM.jpg` → `YYMM.jpg` pairing, current source and
thumbnail hashes, and a validated reader using the donation for matching dates.
A date outside the reader catalog may use its validated prepared thumbnail.
Changed files or validation evidence invalidate the report. Reapplying the same
report is safe; completed deletions are logged in ignored
`archive/covers/evidence/cover-cleanup.<report-hash>.applied.json`. Unpaired legacy JPEGs, legacy
`.png`, `.jpeg` and `.webp` variants, donated originals, PDF candidates and review records are
preserved. Ordinary preparation, export and checking never delete source files.

For CD2/CD3, matching uses the group's displayed year/month. The same date cover
can illustrate multiple distinct native groups; it does not verify their printed
issue identity or create TOC associations. Undated groups stay without a cover.

## Deployment base and routes

The default build assumes the site is served from `/`. For a nested directory,
set the same base while building and serving, for example:

```sh
cd web
READING_ROOM_BASE=/archive/ npm run build
```

Deploy the **contents** of `dist/reading-room-cd/` at `/archive/` (or choose a
different `READING_ROOM_OUTPUT` directory). The data URL is resolved against
that base. Hash routes (`#/issues/...`, `#/articles/...`) work on static hosts
without a route rewrite. Downloads and images use package-relative data URLs.
Opening an article fetches its issue and article documents; it does not fetch
other article bodies. Search loads its metadata index only when opened.

The app uses the default neutral shadcn/ui palette, including its button
component, with a System/Light/Dark control. System is the initial setting;
an explicit choice persists in local storage. The header is fixed; TOC and
context panels adapt to mobile. Keyboard users can skip to the main content.

## Data and known limits

The aggregate uses static data version 2. The reader also accepts version 1
CD1/demo documents, preserving existing CD1 URLs. CD2/CD3 article IDs are
disc-qualified (for example `cd3:article:topic-0037`), documents use names such
as `articles/cd3-topic-0037.json`, and native groups use `cd3-9501`. Explicit
paths locate media and source blocks without imposing CD1's folder layout.
The manifest pins all three input manifests and inventories every output file,
including the complete copied CD2/CD3 references under `data/source/`.

A separate [version 3 scan pilot](READING-ROOM-STATIC-V3.md) is staged under
`dist/reading-room-pdf-pilot/data`, retaining the complete CD baseline. The
loader accepts version 3. The scan-specific UI described in
[PDF restoration](PDF-RESTORATION.md) passes desktop/mobile checks in
`dist/reading-room-pdf-ui/`, including scan evidence, review states and extracted
covers. The production aggregate above remains unchanged.

CD2 retains 220 success and 1,110 partial outcomes; CD3 retains 792 success and
176 partial outcomes. Partial status can mean text, media, attachment or metadata
uncertainty. It does not imply the body is missing. The adapter preserves
paragraph termination, whitespace, emphasis and source figure markers. CD3
blanket underlining comes from a [HELPDECO font-decoding bug](CD3-HELPDECO-UNDERLINE-BUG.md)
and is suppressed in the reading display. The decoder is unpatched; its generated
flags remain in source blocks, and text/download bytes are unchanged. This
workaround also suppresses genuine CD3 underline. CD3
Click icons resolve to their recovered figure targets; missing originals have
an unavailable state without a broken download link. Native source links open
the portable references for sidebars, author biographies and related topics.
The bookshelf also links the full references, supplemental and unassigned-media
shelves. These auxiliary topics remain outside the article/search counts.

The combined media index has 9,990 group/resource records: 6,783 from CD1,
2,139 from CD2, and 1,068 from CD3 (1,039 copied media records plus 29 explicit
missing-source records). This is not a distinct-image count. CD2/CD3 contribute
1,758 and 79 original attachment links respectively. Original bytes, including
CAB/source files, stay unchanged. The reference-only data tree contains 44,672
inventoried files and approximately 3.43 GB before its root manifest and covers.
The cover contribution depends on the supplied dates; inspect the current manifest
for exact file and cover counts.

For the earlier CD1-only export, run
`PYTHONPATH=src python3 -m tools.reading_room.export --output dist/reading-room-cd1/data`.
The default `make export-reading-room` aggregates all discs; custom paths can
be passed with `READING_ROOM_ARGS`. The historical strict package schema is
unchanged.

For CD1, the adapter projects the existing `catalog.json`, per-article `reference.json`,
text/listing files and media from `archive/cd1/reference/`. It reads the pinned TOC
snapshot or an explicitly validated owner correction migration, plus reviewed
links from existing issue packages. The adapter replays migration decisions and
preserves historical article records; it does not rewrite their source hashes.
Issue TOCs and CD article lists remain separate; an unmatched TOC entry does not
imply absent CD content.
Article IDs, paragraph order, literal runs, code whitespace, gap markers and
download bytes are retained. Source/reference records remain available through
article links. Media has separate issue/resource identities and original links.

The CD1 portion contains 5,299 TOC entries, 3,125 listing downloads and
6,783 issue-specific media records. Those media records represent 6,090 distinct
referenced images: 4,979 viewable derivatives and 1,111 deferred originals.
Eight candidate articles still have unresolved boundaries; 33 other references
have localized marked text gaps. Optional owner-supplied covers are supported;
issues without one show a plain placeholder. Search covers metadata, not full article text.
The aside shows more articles from the same issue and source links; it does not
claim editorial recommendations. The reader does not perform OCR, article
correction, new extraction or paper verification.

## Checks

Donated TOC scans use the separate [TOC image workflow](TOC-RESTORATION.md).
Canonical issues show ordered reduced images; scans outside the catalog appear
in a date-labeled gallery. OCR comparison remains private and never replaces
catalog text. The new export options are `--tocs`, `--toc-images`, and
`--toc-reviews`; missing donation directories and older datasets remain supported.

```sh
make test-reading-room
make check-reading-room
```

The focused target runs Python adapter tests, Vitest and a TypeScript/production
build. `check-reading-room` independently verifies the complete generated file
inventory, hashes, counts and TOC/article links. Browser checks use the
[Playwright CLI skill](https://playwright.dev/) against Vite preview to inspect
real issue/article/media/search flows, mobile layout and the static build.

The real build is large because it ships original and converted media files;
the browser loads only selected documents and images. Do not deploy or publish
the private content without a separate decision about access and rights.

## Build cleanup — October 14, 2026

Twenty obsolete preview/test directories were retired, reclaiming about **108 GiB**.
`build/` decreased from approximately 251 GiB to **143 GiB**. The removed groups
were nine incremental June previews (the completed June reader remains), the
repeated PDF pilot, three TOC validation readers, three cover-reader trials,
three demo/nested builds, and the fallback cover-thumbnail cache.

The current volunteer reader, July rebuild baseline, completed issue readers,
CD references, canonical TOCs, prepared CD packages, and PDF restoration outputs
remain in place. Other historical outputs with unresolved dependencies were
kept. This was a conservative cleanup, not a claim that every remaining build
is necessary to serve the site.

The private cleanup record is `archive/migrations/build-cleanup/2026-10-14/report.json`.
It lists every removed directory, byte totals, retained-file hashes and snapshot
hashes. All 886,430 removed regular files were hashed; unique bytes were copied
and checked, and identical retained copies were verified before deletion.
Compressed inventories preserve file locations, modes, timestamps and symlinks.
The archive (unique files plus indexes and logs) occupies about **246 MiB**.

To restore one historical preview at its original path:

```sh
python3 -m tools.storage_layout restore-retired reading-room-qwen-june-through-car
```

Restoration refuses an existing destination or changed source bytes. It requires
free space for the full restored copy. Historical staging scripts or old preview
URLs that refer to removed directories require restoration first. The synthetic
demo can instead be regenerated with `make demo-reading-room`.

**The compact archive is not an independent backup.** Duplicate bytes are read
from retained `reading-room`, `reading-room-pdf-pilot`,
`reading-room-qwen-june-complete`, `reading-room-routed-july-complete`, and
`reading-room-volunteer` data trees; exact source paths are in the inventories.
Keep those files unchanged along with the cleanup archive if exact historical
restoration is required. Both the archive and generated readers are Git-ignored.

Post-cleanup validation passed: the complete volunteer reader still has all
3,643 article records; the July baseline passes its full integrity check; all
37 August input packages validate; and eight retained manifests are unchanged.
Four cleanup tests covered lossless file/symlink restoration and rejection of
changed candidates, restore sources, and snapshot inventories. The logs and
validation records are beside the cleanup report.
