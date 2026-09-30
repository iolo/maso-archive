# Donated TOC images

This workflow keeps `TOC.md` authoritative and read-only. OCR produces comparison
evidence, never catalog edits, IDs, search entries, or article associations. The
owner reviews reported differences and edits the source manually. A later source
edit may invalidate pinned catalog dependencies; migrating those dependencies is
separate work, not a side effect of preparing images.

## Private inputs and evidence

Original donations stay in ignored `tocs/`. The normalized filename is
`YYMM-NN.jpg`, with a two-digit sequence beginning at 01. Sequence is distinct from
a printed page number. Original bytes are preserved, including source metadata.
Do not serve the repository root or commit originals, crops, OCR output, or sites.

`private/toc-restoration/` holds the inventory, review decisions, reversible rename
journal, OCR cache, and reports. `build/toc-images/` holds prepared derivatives and
their private provenance manifest. Public reader records contain only derivative
paths, dimensions, sizes, hashes, ordering, and explicitly public coverage notes.

```sh
make inventory-tocs
make normalize-tocs                         # dry-run; saves/reuses inventory
make normalize-tocs TOC_ARGS='--apply'       # requires visual identity/order review
make normalize-tocs TOC_ARGS='--apply --rollback'
make ocr-tocs
make compare-tocs
make prepare-toc-images
```

An existing inventory is never silently replaced when it differs. After renaming,
use `TOC_ARGS='--inventory private/toc-restoration/current-inventory.json'` to save
a new inventory while retaining the original mapping for rollback. Apply and
rollback use the original inventory, reviews, and journal. Interrupted moves can
be resumed with the same command; changed bytes or occupied destinations fail
without overwriting them. Newly donated pages must not silently renumber reviewed
ones; mixed old and normalized names require explicit review first.

The review file `private/toc-restoration/reviews.json` contains `pages`, each keyed
by source `sha256`, with `date` (`YYMM`), `sequence`, `identityEvidence`, and
`orderEvidence`. These records document actual visual review; their presence is
not a substitute for doing that review. Optional `kind: "advertisement"` and a
`note` account for a non-TOC donation without serving it as a TOC. An optional
`publicNote` on a TOC page explains a gallery coverage gap to readers.

## OCR and comparison

OCR reuses the existing pinned local Korean/English Tesseract runtime and validates
its model/runtime hashes. No external service receives images. The default OCR
image fits within 3600 × 5400 pixels, independently of reader sizes. Raw text,
TSV word boxes/confidences, crop images, configuration, and source hashes remain
private. Cache keys include source content, recognition settings, and runtime.

```sh
make ocr-tocs TOC_ARGS='--dates 8311 8509 8802'
make ocr-tocs TOC_ARGS='--config private/toc-restoration/ocr-config.json'
```

Configuration is a JSON object keyed by normalized image name. Per-page values
can override `psm`, `bounds`, `rotation` (clockwise right angles), `languages`, and
`regions` (ordered normalized `[left, top, right, bottom]` rectangles). Whole-page
OCR can omit decorative headings and misorder columns; inspect and choose explicit
regions where needed. A low confidence result or an OCR omission is not evidence
that the catalog is wrong.

`ocr-index.json` points to the current per-page evidence. Reports live under
`private/toc-restoration/reports/<content-hash>/report.md` and `report.json`;
`reports/latest.json` identifies the latest report. Each catalog entry includes
source line, stable ID when the current import matches the source hash, verbatim
catalog text, candidate OCR text, and its image/region/pixel box. Complete OCR is
retained for spotting image-only entries and omissions. Similarity is a navigation
aid, not an acceptance decision. Hierarchy, ordering, contributors, and printed
pages still require visual comparison.

After comparison, each page's review may contain a `comparison` object with
`status`, `note`, `sourceSha256` (of `TOC.md`), and `evidenceSha256`. The note should
identify OCR errors, visible print/catalog differences, unreadable regions, and
coverage limitations. Changed catalog or OCR evidence marks that review stale.
Previous reports remain tied to their source version. Neither comparison nor OCR
has a catalog-write option.

## Reader integration

Preparation creates newly encoded RGB JPEGs: previews bounded by 480 × 720 at
quality 80, readable images bounded by 1600 × 2400 at quality 85. It applies EXIF
orientation, converts embedded profiles to sRGB, preserves proportions, never
upscales, and strips metadata. Cached derivatives are validated before reuse.
Staged replacement removes stale files and preserves the preceding usable output
on failure. The pilot's 12 portrait pages yielded 41–65 KB previews and 380–616 KB
readable images; a landscape pilot was 279 KB at 1600 × 1152.

Ordinary CLI reader export prepares images without OCR or renaming:

```sh
make export-reading-room READING_ROOM_ARGS='--output build/toc-reader-validation/data'
PYTHONPATH=src python3 -m tools.reading_room.check --data build/toc-reader-validation/data --require-thumbnails
```

Exporter options are `--tocs`, `--toc-images`, and `--toc-reviews`. Missing donation
directories produce an empty image collection. Existing datasets without the new
fields remain supported. The Python exporter APIs default to no TOC refresh;
callers opt in with `tocs=...`.

Canonical issue documents gain optional ordered `tocImages`. Other scans appear
in `toc-gallery.json`, linked from the bookshelf; this creates no catalog issues
or restoration groups. Native CD2/CD3 date groups do not acquire TOC scans merely
because their dates coincide. June 1991 retains its existing catalog and a clear
missing-scan message. Previews load lazily; larger images load when opened in a
keyboard-accessible dialog with page selection, zoom, and failure fallback.

PDF scan exports preserve existing TOC assets. `tools.reading_room.scan` also
accepts the three TOC options for an explicit refresh, allowing only TOC asset,
gallery, and `tocImages` field changes beyond its existing scan changes. The
checker validates hashes, actual encoding, dimensions, metadata, order, gallery
membership, and absence of stale TOC assets. Existing catalog checks stay enabled.

The synthetic `--demo` includes a two-page TOC and a later scan gallery without
opening private donations. Python tests cover source preservation, rename recovery,
OCR caching, comparison versioning, catalog isolation, image validation/removal,
and PDF export integration; frontend tests cover optional/missing collections and
on-demand image markup. Browser checks additionally exercise actual controls.

## Reviewed donation results — 2026-09-30

All 240 donated JPEGs have normalized names and reviewed dispositions. The 239
accepted TOC pages produce 478 derivatives; the remaining file is a preserved
July 1995 advertisement excluded from the viewer. Previews total 13,627,830 bytes
and readable images total 120,357,834 bytes. Two readable images slightly exceed
the 700 KB investigation threshold (December 1983 and June 1993); their density
justifies retaining the pilot quality settings. No original is served.

The private report selected by `private/toc-restoration/reports/latest.json`
contains 420 visual findings. Its coverage is 121 catalog issues with donated
images, one catalog-only issue (June 1991), and 24 image-only issue sets from
1994–1995. All 240 review records are tied to the original image, current OCR
evidence and unchanged `TOC.md` hashes. There are no pending page reviews.
Automatic entry labels such as `possible-difference` remain OCR navigation aids;
the page review notes and visual findings record the human-readable disposition.
The 420 findings are evidence for manual decisions, not 420 approved corrections.

Unresolved evidence remains explicit: damaged August 1984 text, obscured April
1986 graphics listings, clipped July 1992 page digits, and July 1995's donor-only
date and incomplete TOC coverage. Later image-only scans do not extend the catalog
or create article associations. The reader retains 152 navigation groups, 5,497
TOC entries and 3,386 articles, with a separate 24-set scan gallery.

Final validation includes 56 reader Python tests, 15 frontend tests, 58 PDF tests,
18 TOC/snapshot tests and TypeScript/production build. Full-issue PDF export also
preserves inherited TOC images, gallery records and derivative bytes. The private
`completion_audit.py` checks source and OCR pins, all reviewed findings, all four
prepared reader outputs, historical snapshot files, and the pre-integration reader
baseline. Run it from the repository root with
`PYTHONPATH=src:. python3 private/toc-restoration/completion_audit.py` when reviewing
these local results. It requires the private evidence and is not a public rebuild
dependency.
