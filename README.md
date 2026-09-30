# maso-archive

월간 마이크로소프트웨어의 비공식 디지털 아카이브.

**CD1, CD2, CD3 restoration and the combined reading room are implemented.**
The private reader provides issue/date-group browsing, library TOCs, Korean
article text, code downloads, figures, original attachments and metadata search.
Paper magazines remain authoritative; CD transcription has not been verified
against print.

## Read the archive

With the prepared private data, start the existing build:

```sh
cd web
npm run preview
```

Open the local address printed by Vite. The static site is in
`build/reading-room/`; it needs HTTP hosting for JSON requests, with no backend,
database or runtime extraction. It is not a direct `file://` application.

To regenerate it from the completed private references, use Python 3.11+ with
`requirements.txt` installed and Node.js 20.19+ (20.x) or 22.12+:

```sh
cd web && npm ci && cd ..
make export-reading-room
make check-reading-room
make build-reading-room
cd web && npm run preview
```

The export requires `build/cd1-reference/`, `build/cd2-reference/`,
`build/cd3-reference/`, the pinned `build/toc/` snapshot and CD1 reviewed issue
packages. It verifies the inputs and stages a checked replacement before
updating the reader. A Git checkout alone does not contain publisher sources or
finished private outputs. See the [reading-room guide](docs/READING-ROOM.md) for
input details, synthetic demo, development, routes and nested hosting.

Without private inputs:

```sh
cd web && npm ci && cd ..
make demo-reading-room
cd web && READING_ROOM_OUTPUT=build/reading-room-demo npm run preview
```

Donated covers go in private `covers/` as `YYMM.jpg` (for example `8311.jpg`).
Exports generate JPEG thumbnails bounded by 480 × 640 pixels for the bookshelf
and issue page. Donated images take priority over verified PDF covers, then
placeholders. Originals stay unchanged and must never be committed or served.
See [adding covers and retiring legacy JPEGs](docs/READING-ROOM.md#add-or-replace-cover-images).

## Delivered coverage

| Source | Navigation groups | Candidates | Readable texts | UTF-8 listings |
| --- | ---: | ---: | ---: | ---: |
| CD1 | 122 library issues, 72 with CD1 bodies | 1,088 | 1,080 | 3,125 |
| CD2 | 12 native date groups | 1,330 | 1,330 | 87 |
| CD3 | 18 native groups | 968 | 968 | Inline code stays in article text |
| Combined | 152 | 3,386 | 3,378 | 3,212 |

The archive target is November 1983–December 1995 (146 monthly issues).
The supplied library TOCs cover 122 issues through December 1993, with 5,497
entries. The 152 navigation groups are **not 152 distinct verified printed
issues**: CD2/CD3 keep their own identities, overlapping dates and CD3's
anomalous 1994/1996 labels and undated group. No later TOC associations were
invented. The combined media index has 9,990 group/resource records, including
unavailable states; CD2/CD3 supply 1,837 original attachment links.

The reader also includes 239 donated TOC pages as reduced images, including a
separate gallery for the 24 issue sets from 1994–1995. The original scans and OCR
stay private. [TOC comparison results](docs/TOC-RESTORATION.md#reviewed-donation-results--2026-09-30)
record 420 visual findings for manual review; the library catalog remains unchanged.

All three standalone references remain available:

| Reference | Private entry point | Reproduction and coverage |
| --- | --- | --- |
| CD1 | `build/cd1-reference/index.html` | [CD1 guide](docs/CD1-READABLE-REFERENCE.md) |
| CD2 | `build/cd2-reference/index.html` | [CD2 guide](docs/CD2-READABLE-REFERENCE.md) |
| CD3 | `build/cd3-reference/index.html` | [CD3 guide](docs/CD3-READABLE-REFERENCE.md) |

The reading room includes all three discs. Its CD2/CD3 source links also expose
supplemental texts, biographies and unassigned-media shelves, outside the article
counts. CD1's historical strict packages and earlier retry results remain intact.

## Known limits

- CD1 retains eight unresolved article boundaries, 33 texts with localized gaps,
  and 1,111 deferred distinct images with original links.
- CD2 has 220 success and 1,110 partial outcomes; CD3 has 792 success and 176
  partial outcomes. Partial can mean a text, media, attachment or metadata
  exception; readable bodies are retained.
- **HELPDECO misreads CD3's font character-set byte as double underline.** The
  current display workaround removes CD3 underlining in the reader and standalone
  pages. The decoder is unpatched; generated RTF/source flags retain the defect,
  and genuine underline is also suppressed. See the
  [bug record and deferred correction](docs/CD3-HELPDECO-UNDERLINE-BUG.md).
- Complete cover coverage, print verification, corrected transcriptions, further TOC matching,
  independent backup/restore verification and publication remain future work.
  Search covers metadata, not full article text.

The completed implementation is a private reading/restoration reference. Original
ISOs, decoder probes, recovered bodies/assets, generated sites and browser
artifacts are excluded from Git. No public deployment was performed.

## Validation and handoff

```sh
make test-reading-room    # Python adapter tests, Vitest, TypeScript and build
make check-reading-room   # Prepared private data: inventory, hashes and links
```

Per-disc checks are `make check-cd1-reference`, `make check-cd2-reference` and
`make check-cd3-reference`; prerequisites and rebuild commands are in their guides.
`make check` runs the broader historical Python suite when relevant to a change.
Focused tests and real-browser checks cover article/media navigation, search,
downloads, missing states and mobile reading. Checks establish extraction
consistency and usability, not agreement with print.

- [Current successor handoff and deferred work](docs/SUCCESSOR-NOTES.md)
- Completed plans: [CD1](PLAN-CD1.md), [CD2](PLAN-CD2.md), [CD3](PLAN-CD3.md),
  [reading room](PLAN-reading-room.md)
- [Chronological implementation and validation record](PROGRESS.md)
- Source maps: [initial inspection](docs/SOURCE-INVENTORY.md),
  [CD1 extraction](docs/CD1-EXTRACTION.md), [CD2](docs/CD2-SOURCE-MAP.md),
  [CD3](docs/CD3-SOURCE-MAP.md)
- [Optional physical-magazine and backup tasks](docs/OFFLINE-TASKS.md)
- Historical foundations: [TOC import](docs/TOC-IMPORT.md),
  [donated TOC images and read-only OCR comparison](docs/TOC-RESTORATION.md),
  [strict v1 package contract](docs/READING-ROOM-CONTENT-V1.md),
  [CD1 19b checkpoint](docs/CD1-OEM-PASS.md),
  [original reading-room PRD](PRD-reading-room.md),
  [design reference](docs/DESIGN-REFERENCE.md)
