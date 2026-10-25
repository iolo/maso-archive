# maso-archive

An unofficial digital archive of the monthly magazine Microsoftware.

**CD1, CD2, CD3 restoration and the combined reading room are implemented.**
The private reader provides issue/date-group browsing, library TOCs, Korean
article text, code downloads, figures, original attachments and metadata search.
Paper magazines remain authoritative; CD transcription has not been verified
against print.

For PDF restoration, start with the short [OCR handoff](PLAN-OCR.md).
Mapped Tesseract is the default; Qwen is opt-in assistance for difficult prose or
code, with explicit layout and coverage review. The handoff links consolidated
findings, metrics, commands and preserved [experiment history](docs/history/README.md).

## What to keep

| Directory | Purpose | Preserve? |
| --- | --- | --- |
| `metadata/` | Tracked IDs, catalog records, decisions and provenance | Yes; commit to Git |
| `archive/` | Completed restorations, ongoing work, corrections, recipes, raw OCR, evidence and toolchains | Yes; back up separately |
| `work/` | Verified reproducible caches and temporary processing | Disposable after the task finishes |
| `dist/` | Assembled reading rooms | Replaceable from preserved inputs or release snapshots |

Keep original PDFs, ISOs, extracted source files, donated covers and TOCs too.
A completed article does **not** make its restoration evidence disposable.
`data`, `private`, `build` and `output` are compatibility links for older recipes.
Use the canonical directories above for new work. See [storage and recovery](docs/STORAGE.md)
for the issue layout, retention rules and reader restore command.

## Read the archive

The unified volunteer reader’s 2026-10-22 snapshot includes **11 completed PDF restorations**
(November 1983; February, March, May–October and December 1984; February 1985)
and **all three CDs**: 407 PDF article records plus 3,386 CD records, 3,793 total.
Known partial and unavailable states remain visible.

```sh
python3 -m http.server 4189 --bind 127.0.0.1 --directory dist/reading-room-volunteer
```

Open [the volunteer reading room](http://127.0.0.1:4189/#/review).
Filter by source, issue, personal review status, title or author. Open a PDF
article's scan comparison to review regions beside corrected text and original
OCR. **검토 메모** autosaves feedback locally; download the JSON and pass it to
the coordinator. Nothing is submitted automatically or marked officially accepted.
Browser data is specific to the host/port and should be exported before clearing it.

The prepared static app is `dist/reading-room/`. It uses relative
asset and data URLs and works with ordinary static servers, including Python's
`http.server` and `npx serve dist/reading-room -l 4189`; Vite is only
needed to build it. Rebuild the UI with
`make build-volunteer-reading-room`; validate its data with
`make check-volunteer-reading-room`. Reproduction, the pinned August adapters,
and private static hosting are described in the [reading-room guide](docs/READING-ROOM.md).
The [Cloudflare deployment guide](docs/DEPLOY-READING-ROOM.md) includes a resumable
uploader and a Worker for sharing the collection through an unlisted URL.
Earlier private previews and the CD-only baseline remain available below.

With the prepared private data, start the existing build:

```sh
cd web
npm run preview
```

Open the local address printed by Vite. The static site is in
`dist/reading-room-cd/`; it needs HTTP hosting for JSON requests, with no backend,
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

The export requires `archive/cd1/reference/`, `archive/cd2/reference/`,
`archive/cd3/reference/`, the pinned `archive/toc/current/` snapshot and CD1 reviewed issue
packages. It verifies the inputs and stages a checked replacement before
updating the reader. A Git checkout alone does not contain publisher sources or
finished private outputs. See the [reading-room guide](docs/READING-ROOM.md) for
input details, synthetic demo, development, routes and nested hosting.

Without private inputs:

```sh
cd web && npm ci && cd ..
make demo-reading-room
cd web && READING_ROOM_OUTPUT=dist/reading-room-demo npm run preview
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
The supplied library TOCs cover 122 issues through December 1993, with 5,299
entries after the owner’s manual corrections. The 152 navigation groups are
**not 152 distinct verified printed issues**: CD2/CD3 keep their own identities,
overlapping dates and CD3's
anomalous 1994/1996 labels and undated group. No later TOC associations were
invented. The combined media index has 9,990 group/resource records, including
unavailable states; CD2/CD3 supply 1,837 original attachment links.

The reader also includes 239 donated TOC pages as reduced images, including a
separate gallery for the 24 issue sets from 1994–1995. The original scans and OCR
stay private. [TOC comparison results](docs/TOC-RESTORATION.md#reviewed-donation-results--2026-09-30)
record 420 historical visual findings. The owner’s subsequent catalog corrections
are imported through the [reviewed identity migration](docs/TOC-IMPORT.md#owner-correction-migration--2026-10-01).

All three standalone references remain available:

| Reference | Private entry point | Reproduction and coverage |
| --- | --- | --- |
| CD1 | `archive/cd1/reference/index.html` | [CD1 guide](docs/CD1-READABLE-REFERENCE.md) |
| CD2 | `archive/cd2/reference/index.html` | [CD2 guide](docs/CD2-READABLE-REFERENCE.md) |
| CD3 | `archive/cd3/reference/index.html` | [CD3 guide](docs/CD3-READABLE-REFERENCE.md) |

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

PDF restoration is a separate JSON/assets campaign. November 1983; February,
March, May, June, July, August, September, October and December 1984; and February,
March and October 1985 are complete. March 1984 retains one missing-source terminal
partial; no April PDF was supplied. October 1985 accounts for all 39 canonical
entries: 35 readable, assistant sample-reviewed articles and four non-owning headings.
All 268 source pages are classified and the donated cover is verified. Its index is
`archive/pdf/1985-10/reference/issue.json`; the whole-issue report is
`archive/pdf/1985-10/evidence/issue-closeout/report.json`. All 9,031 files match the
independent rebuild, including 9,025 exact selected-package files; fresh 213 tests pass.
Human acceptance/full proofreading, source bytes/spacing/glyph counts, claims,
execution and independent backup recovery remain unverified. Volunteer body/glyph/
diagram-label work and the batch32/46 timing supplements remain explicit. No reader
rebuild followed this closeout. See the [PDF plan](PLAN-PDF.md),
[issue progress](docs/progress/README.md) and [successor handoff](docs/SUCCESSOR-NOTES.md).

November 1985 restoration is in progress: eighteen articles are readable and
independently reproducible. New Products on pages 100–101 now matches across
99 exported files, preserving two notices, three specification tables with all
50 cells, supplier credits and product photos. No current partial article or
assembly remains; 28 of 46 entries still need restoration or classification.
Next is the book review on page 102 and upper 103. The lower Back-Issue Guide
remains separate and pending. Cover and whole-issue accounting remain.
Conversation, progress logs and documents use English; original source text
retains its language. See [the November progress log](docs/progress/8511.md).

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
