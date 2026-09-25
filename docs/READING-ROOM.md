# Reading room

The static reading room is generated from the completed private CD1 reference.
The reader covers 122 issues (1983-11–1993-12), including the 50 issues with
library TOCs but no CD1 body. It renders 1,080 article texts from 1,088
candidate records. CD text is a secondary transcription pending comparison with
paper magazines.

## Build the local archive

From the repository root, with the private `build/cd1-reference/` and
`build/toc/` folders present:

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
input hashes. It does not change the reference, extraction records or publisher
sources. The generated data and source assets stay under ignored `build/` and
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

The adapter projects the existing `catalog.json`, per-article `reference.json`,
text/listing files and media from `build/cd1-reference/`. It reads the pinned TOC
snapshot and reviewed links from existing issue packages. Issue TOCs and CD article
lists remain separate; an unmatched TOC entry does not imply absent CD content.
Article IDs, paragraph order, literal runs, code whitespace, gap markers and
download bytes are retained. Source/reference records remain available through
article links. Media has separate issue/resource identities and original links.

The current export contains 5,497 TOC entries, 3,125 listing downloads and
6,783 issue-specific media records. Those media records represent 6,090 distinct
referenced images: 4,979 viewable derivatives and 1,111 deferred originals.
Eight candidate articles still have unresolved boundaries; 33 other references
have localized marked text gaps. Cover scans are absent, so issue pages show a
plain missing-cover placeholder. Search covers metadata, not full article text.
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
