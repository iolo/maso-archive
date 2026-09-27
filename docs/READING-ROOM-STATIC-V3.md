# Static reader contract version 3

Version 3 adds a scan-derived article to the existing static data contract.
`web/src/data.ts` defines the reader types; `tools/reading_room/check.py` and
`tools/reading_room/scan.py` validate exported data against immutable packages.
This is the static web contract, distinct from the older content-bundle schema
in `schemas/reading-room-v1.schema.json`.

The loader accepts document versions 1, 2 and 3. An aggregate may contain all
three: only the catalog, search index, affected issue/media documents and new
scan article use version 3. Existing CD article documents and source assets
retain their exact bytes and URLs.

## Identities and states

A scan article's `reference` and `article_id` are its stable package ID, such as
`scan-maso-1983-11-toc-0012`. Its document is
`articles/scan-maso-1983-11-toc-0012.json`. Existing hash-route functions need no
new route syntax. `issue_id` and `tocEntryId` bind it to exactly one existing
canonical issue and TOC entry; the adapter appends the article ID without
removing any existing TOC associations.

Scan summaries and metadata-search items carry:

| Field | Meaning |
| --- | --- |
| `sourceKind: "scan"` | Distinguishes scan-derived material from legacy CD records |
| `availability` | `readable`, `partial`, `image-only`, `failed` or `unresolved` |
| `verification` | `unreviewed`, `sample-reviewed` or `fully-reviewed` |
| `status` | Same availability value for compatibility with summary consumers |
| `tocEntryId` | Canonical TOC identity, on the article summary |

Availability does not imply accuracy. The step 8 exporter currently accepts one
readable, reviewed pilot. Broader availability fixtures and their presentation
belong to step 9; bounded multi-article processing belongs to step 10.

## Article and evidence fields

The article document keeps the established `blocks`, `listings` and `media`
shape. Each projected text or figure block adds `regionIds` and either
`scanBlockId` or `scanFigureId`. Separate spacing blocks preserve the package's
exact `article.txt` separators without adding whitespace to literal code blocks.
The generated paragraph index records Unicode character offsets in that text;
separator positions lie between the recorded content spans.

The additional `scan` object contains:

- `packagePath` and `packageSha256`, pinning the copied original `article.json`.
- `source`, preserving the original PDF identity, SHA-256, size and repository
  input path. That path is provenance, not an exported full-PDF download.
- `coordinates`, `pages`, `regions` and `excludedRegions`: original PDF indices,
  independently observed printed numbers, transforms, crop geometry and exclusions.
  Each included region has its available scan asset pin.
- `availability`, full `verification` evidence/scope/uncertainties, and `gaps`.
- `contentOrder`, `figures`, `downloads`, `corrections` and `reviewRecords`.
- `relationships`, empty for this pre-CD pilot. The adapter rejects nonempty
  relationships until a comparison-backed relationship adapter is supplied;
  it never infers links from titles. Step 7's separate comparison remains intact.

`packagePath`, region-asset pins and download/correction/review pins are relative
to `data/source/`. Figure asset pins inside `scan.figures` retain the original
package-relative scope; resolve them beside `packagePath`. The PDF source path
retains repository-input scope. This distinction prevents accidental links to
unexported files.

The complete portable package is copied unchanged under
`data/source/pdf/<scan-id>/`, including its standalone preview, raw OCR,
corrections, region scans and manifests. The adapter's paragraph index is kept
separately under `data/source/pdf-adapter/<scan-id>/paragraphs.json`, so the
original package inventory still validates. Figure media use explicit source
paths; filenames need not follow CD media conventions.

## Staging and checks

```sh
make export-pdf-reader
PYTHONPATH=src python3 -m tools.reading_room.check \
  --data build/reading-room-pdf-pilot/data
```

The default inputs are `build/reading-room/data` and
`build/pdf-restoration/pilot`. The default output is a separate
`build/reading-room-pdf-pilot/data`. Override them with
`PDF_READER_ARGS="--base ... --package ... --output ..."`.
An existing output is refused. The exporter copies files independently, validates
in a temporary directory, then publishes the completed output. A failed export
leaves the baseline intact. It does not replace production reader data.

The version 3 manifest adds `baseManifestSha256` and `scanInputs`, pinning the
baseline and included scan package manifests. The checker verifies inventories,
file hashes, exact projection from the package, canonical TOC binding, paragraph
positions, region/download provenance and independent review states. Changing
projection data and merely recalculating the outer manifest cannot conceal a
mismatch with the copied scan package.

Step 8 validates this data adapter and version compatibility. Scan-specific UI
labels, review presentation, evidence navigation and desktop/mobile browser
acceptance are step 9; this staged data export is not yet a completed scan reader.
