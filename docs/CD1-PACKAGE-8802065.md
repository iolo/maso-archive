# Pilot reading-room package

Step 9 completes the first CD1 preparation milestone: one private, reproducible
article package under the approved [v1 contract](READING-ROOM-CONTENT-V1.md).
The contract schema is unchanged. The package contains article `8802065`,
**유닉스란 무엇인가?**, and its February 1988 issue/TOC context.

## Build and verify

```sh
make reading-room-package
PYTHONPATH=src python3 -m tools.build_reading_room_package --verify build/reading-room-packages/cd1-8802065/content
```

Building requires the existing step 8 example/provenance, source metadata and
maps referenced by that provenance, accepted image derivatives, and step 5d
Markdown previews/provenance. Each input is checked against its recorded hash.
The exporter reads prepared artifacts; it does not rerun extraction or conversion.
If step 8 outputs are absent, regenerate them with `make reading-room-example`.

`--verify CONTENT_DIRECTORY` checks an existing package independently of those
private build inputs. It requires only the validator's code/dependencies and v1
schema. The directory can be relocated. Verification reads the manifest, validates
each document and the complete graph, checks actual file sizes/hashes and exact
inventory, and checks generated Markdown caption anchors and SVG dependencies.
It rejects unsafe paths, symlinks, missing/changed files, unexpected files, and
external/dangling SVG resource references. It is an integrity check, not proof of
authenticity, printed-page accuracy, or permission to publish.

The default build checks the generated result against the tracked
[metadata summary](../data/catalog/reading-room-packages/cd1-8802065.json).
An intentional reviewed input/export change can update that summary explicitly:

```sh
PYTHONPATH=src python3 -m tools.build_reading_room_package --write-record
```

Files are built in a sibling staging directory and validated before replacing
the previous generated package directory. A failed input or staging check leaves
the previous package intact. Successful replacement removes obsolete files.
The two directory renames are not a transaction across a machine crash; rerun
the deterministic build if interrupted. No source or earlier output is rewritten.

## Files and static handoff

```text
build/reading-room-packages/cd1-8802065/
  provenance.json                       private preservation evidence
  content/                              package base directory
    manifest.json
    catalog.json
    media.json
    issues/maso-1988-02.json
    articles/cd1/8802065.json
    previews/cd1/8802065/introduction.md
    previews/cd1/8802065/body.md
    media/cd1/                          9 PNGs and 10 SVGs
```

The **26 files** below `content/` are the complete static handoff, totaling
376,531 bytes for this reviewed build. The separate 181,480-byte provenance file
is not a required runtime document. All content and detailed evidence remain
under ignored `build/`; tracked files contain code, documentation, tests, and
metadata hashes only.

The reading-room client loads `manifest.json`, then obtains document paths by
kind/identity. The catalog supports navigation and metadata search, the issue
provides the ordered TOC, the article provides ordered structured content, and
the media index supplies assets or explicit unavailable states. No RTF parsing,
database, or backend is required. The package contains no UI implementation.

Set the package base URL to wherever **`content/`** is mounted, for example
`https://example.test/archive/data/`. Resolve every manifest, document, media,
and preview path against that directory, rather than the current SPA route or
article file's directory. The files contain no deployment origin. For example,
`articles/cd1/8802065.json` resolves below `/archive/data/`, just like `media/cd1/...`.
See the contract's base-URL example for client URL construction.

## Preserved content and exceptions

The assembled JSON round-trips to the approved step 8 example exactly: one issue,
39 TOC entries (one established article match), two sections, 271 blocks,
323 paragraphs, 289 runs, 21 media occurrences, and 13 caption relationships.
The section text projections match the recovered introduction/body text bytes,
including code indentation, trailing spaces, empty paragraphs, and object order.

All 19 accepted derivatives are copied byte-for-byte, preserving their recorded
hashes. The six differently named identical WMFs retain their separate identities
and files. `bm54.wmf` and `bm55.wmf` remain deferred in `media.json`, with null
display assets, original occurrences/caption relationships, and problem IDs.
Their suspect derivatives and diagnostic previews are absent from the package.
The client should display an unavailable-media placeholder at each occurrence.

The SVGs have no external image/style document dependencies. Four contain live
text with `font_substitution_possible`; their appearance still depends on installed
fonts. Package integrity does not certify conversion fidelity. Neither media
repair nor physical-magazine comparison was performed in this step.

The unknown cover and article ending page remain null. The starting page remains
65, supported by existing source metadata. Extraction status is checked, and
physical-magazine verification is pending. The other 38 TOC entries remain
unmatched, not declarations that their article bodies are absent from the CD.

## Markdown previews and provenance

Both package previews retain ordered source image placeholders, including the
ten WMFs embedded in the mixed code example. Use the structured article/media
documents to display images. Markdown remains a useful text review format rather
than the full mixed-content reading model.

The old step 5d files remain unchanged. Their generated notes said image conversion
and CD-viewer comparison were pending. Only those generated notes are updated in
the package copies: images now refer to the media index, print verification is
pending, and the title object's source-internal role remains unresolved. No
original-viewer comparison is required. The exporter uses the recorded content
byte ranges to protect every one of the 271 block contents; even matching words
inside article prose/code would be copied unchanged. Caption anchors still resolve.

The private package provenance records input fingerprints, the complete step 8
evidence, original asset bindings, adjusted preview content ranges and hashes,
and all runtime file hashes. Its nested `contract_evidence` describes the earlier
step 8 output, including that step's `assets_copied: false`; the package's own
validation records the completed copy. Preservation inputs, source spans,
local paths, and historical viewer flags remain outside the runtime documents.

## Completion check

Tests verify relocation/round-trip, every preview content range, exact accepted
asset bytes, deferred-media exclusion, unsafe/missing/corrupt files, document
identity mismatches, broken preview links, SVG dependencies, and preservation of
the prior output after a staging failure. Repeated builds must match the tracked
summary and all output bytes. These checks complete the **one-article preparation
milestone**; they do not establish issue-wide coverage or printed-page accuracy.

Next is step 10: choose a second article with a different source structure and
test the same contract, splitting newly discovered recovery problems into bounded
tasks. UI work, publication/access decisions, CD2/CD3, and deferred print/media
review retain their separate scopes.
