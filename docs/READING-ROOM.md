# Reading room

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

The 5,497 library TOC entries still cover 1983-11–1993-12. CD2/CD3 groups have
no invented TOC links. CD3 includes anomalous 1994/1996 labels and an undated
group; overlapping labels remain separate by disc. These 152 navigation groups
are not a claim of 152 distinct printed issues.

## Build the local archive

From the repository root, with the private `build/cd1-reference/`,
`build/cd2-reference/`, `build/cd3-reference/`, `build/toc/`, and CD1 reviewed
issue packages present:

```sh
cd web && npm ci && cd ..
make export-reading-room
make check-reading-room
make build-reading-room
cd web && npm run preview
```

Open the local preview address shown by Vite. The complete static site is in
`build/reading-room/`: `index.html`, hashed frontend assets and the prebuilt
`data/` tree. It needs ordinary static file hosting, with no application server
or API. A direct `file://` browser opening is not supported by the SPA because
browsers restrict local JSON fetches. The older
`build/cd1-reference/index.html` remains the direct-file reader.

The export refuses a TOC snapshot that does not match the completed reference's
input hashes, and verifies CD2/CD3 file inventories and hashes before copying.
It builds and checks a staging tree before replacing reading-room data, so
missing or changed inputs leave the previous data usable. It does not change
the references, extraction records or publisher sources.
The generated data and source assets stay under ignored `build/` and
must be handled as private content. A checkout without those folders can still
build and test the synthetic demo:

```sh
cd web && npm ci && cd ..
make demo-reading-room
cd web && READING_ROOM_OUTPUT=build/reading-room-demo npm run preview
```

The demo deliberately uses invented article titles, code and a simple SVG. Its
prepared, recovered, gap, blocked and unmatched cases exercise the same reader.
It lives under `build/reading-room-demo/`, separate from the real archive.

For development, run `npm run dev` in `web/` after exporting data. Vite serves
the selected build data through its local development middleware. Set
`READING_ROOM_OUTPUT=build/reading-room-demo` to develop against the demo.

## Add or replace cover images

Put optional images in the private `covers/` directory at the repository root.
Use one file per month, named **`masoYYMM.jpg`**, `.jpeg`, `.png` or `.webp`:

```text
covers/maso8311.jpg  → November 1983
covers/maso9001.png  → January 1990
covers/maso9509.png  → September 1995
```

For this archive, `YY` means `19YY`. Both the bookshelf and issue overview show
available covers. Missing covers keep a placeholder; small or lower-quality
images are accepted. Images retain their original bytes and proportions, with
no cropping or upscaling of the source file. Replace a file later with a better
copy under the same name, or remove it to return to the placeholder.

After adding, replacing or removing covers:

```sh
make export-reading-room
make check-reading-room
make build-reading-room
```

Refresh the browser. Covers are copied into `build/reading-room/data/covers/`,
included in the file/hash manifest and listed under `coverInputs`; `counts.covers`
counts navigation groups with an assigned cover. A failed image load also shows
the missing-cover placeholder. The current sample set contains eight images.
Keep only one supported image per date; duplicate dates, malformed image names
or corrupt files produce an export error. A missing `covers/` folder is fine.
Images outside an export's date range are not assigned.

To use another source folder, pass
`make export-reading-room READING_ROOM_ARGS="--covers /path/to/covers"`.
The synthetic demo does not consume private covers. `covers/` and generated
outputs are excluded from Git.

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

Deploy the **contents** of `build/reading-room/` at `/archive/` (or choose a
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
`build/reading-room-pdf-pilot/data`, retaining the complete CD baseline. The
loader accepts version 3. The scan-specific UI described in
[PDF restoration](PDF-RESTORATION.md) passes desktop/mobile checks in
`build/reading-room-pdf-ui/`, including scan evidence, review states and extracted
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
inventoried files and approximately 3.43 GB before its root manifest; the eight
sample covers bring the file inventory to 44,680.

For the earlier CD1-only export, run
`PYTHONPATH=src python3 -m tools.reading_room.export --output build/reading-room-cd1/data`.
The default `make export-reading-room` aggregates all discs; custom paths can
be passed with `READING_ROOM_ARGS`. The historical strict package schema is
unchanged.

For CD1, the adapter projects the existing `catalog.json`, per-article `reference.json`,
text/listing files and media from `build/cd1-reference/`. It reads the pinned TOC
snapshot and reviewed links from existing issue packages. Issue TOCs and CD article
lists remain separate; an unmatched TOC entry does not imply absent CD content.
Article IDs, paragraph order, literal runs, code whitespace, gap markers and
download bytes are retained. Source/reference records remain available through
article links. Media has separate issue/resource identities and original links.

The CD1 portion contains 5,497 TOC entries, 3,125 listing downloads and
6,783 issue-specific media records. Those media records represent 6,090 distinct
referenced images: 4,979 viewable derivatives and 1,111 deferred originals.
Eight candidate articles still have unresolved boundaries; 33 other references
have localized marked text gaps. Optional owner-supplied covers are supported;
issues without one show a plain placeholder. Search covers metadata, not full article text.
The aside shows more articles from the same issue and source links; it does not
claim editorial recommendations. The reader does not perform OCR, article
correction, new extraction or paper verification.

## Checks

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
