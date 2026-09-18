# Reading-room content contract v1

Step 8 defines the static data consumed by the [reading room](../PRD-reading-room.md).
The [JSON Schema](../schemas/reading-room-v1.schema.json) defines field shapes;
[the validator](../src/maso_archive/reading_room.py) enforces relationships and
ordering. Both are normative. The [synthetic example](../examples/reading-room-v1.json)
is safe to track and exercises mixed content without publisher article text.
The real pilot remains under ignored `build/reading-room-contract/8802065/`.

This step produces a validating contract example, not a deployable package.
Step 9's [completed pilot package](CD1-PACKAGE-8802065.md) splits the runtime
documents, copies accepted assets, includes Markdown previews, and checks the
resulting package's files and hashes. No viewer, backend,
runtime RTF parser, or access-verification service is needed to consume v1.

## Documents and versioning

Every runtime document has `schema_version: 1` and a `kind` discriminator.
All declared fields are required; unknown fields and unknown versions fail
validation. Nullable fields use JSON `null`, never fabricated values or empty
strings. Arrays retain source order unless a more specific rule below applies.
Strings are Unicode; serialized files are UTF-8. The producer must explicitly
revise the version and migration rules for incompatible additions, including
new block types. Consumers must report unsupported versions instead of dropping
unrecognized content. v1 covers the inspected CD1 structures; it is not a claim
that every CD2/CD3 or future scan format has already been modeled.

| Document kind / schema definition | Purpose | Package location |
| --- | --- | --- |
| `package_manifest` | Document identity-to-file mapping, byte counts, SHA-256 hashes, optional previews | `manifest.json` |
| `catalog` | Small issue/article metadata projections for browsing and search | `catalog.json` |
| `issue` | Date, label, cover reference, ordered TOC tree | `issues/*.json` |
| `article` | Metadata, source identity, ordered sections/blocks/runs, captions, verification | `articles/*.json` |
| `media_index` | Resource identities, usable assets or explicit unavailable states | `media.json` |

The schema root is the development `contract_example` envelope: one catalog,
arrays of issues/articles, and one media index. Each runtime document also
validates independently against its named `$defs` definition. `validate_bundle`
additionally checks the complete graph, including catalog consistency. The
example envelope is not another required runtime file.

`manifest.json` lists every runtime document exactly once as
`{kind, id, path, bytes, sha256}`. Catalog/media singleton IDs are `null`; issue
and article IDs match the document. Consumers look up file paths in this index,
rather than deriving filenames from titles or IDs. Preview records identify
`article_id`, `section_id`, `path`, `bytes`, and `sha256`; each section may have
at most one Markdown preview under `previews/*.md`. An empty preview list is
valid. Media file hashes and paths live in `media.json`. The manifest does not
hash itself. `validate_manifest(manifest, bundle)` checks inventory, paths,
and preview ownership; the package validator additionally verifies actual file bytes.

## Identities and source relationships

Identifiers are opaque strings to consumers. Do not use a title, page number,
array offset, display filename, or file hash as an article identity.

| Entity | CD1 pilot identity / rule |
| --- | --- |
| Issue | `maso-1988-02`, matching the issue's year/month |
| TOC entry | Existing persistent identity, e.g. `maso-1988-02-toc-0035` |
| Article | `cd1:article:8802065`, anchored to the disc's native reference |
| Section | `cd1:topic:148` and `cd1:topic:149`, retaining recovered topic identity |
| Block | Existing block-map identity, e.g. `cd1-8802065:T149:P156-173` |
| Paragraph | `cd1-8802065:T149:P174` |
| Media resource | `cd1:media:bm54.wmf`, anchored to the disc and resource name |
| Media occurrence | Existing paragraph/run identity, e.g. `cd1-8802065:T149:P174:R1` |

Identity definitions must be unique within the bundle; references reuse them.
The catalog repeats metadata projections, not independent entity definitions.
Six differently named pilot WMFs have identical bytes: preserve all six media
identities and their occurrence positions. Hash equality does not establish
editorial identity. Rebuilding unchanged inputs must preserve identities. Changes
to source segmentation need an explicit migration; never silently renumber links.

An article has `source: {disc_id, reference}` and zero or more `toc_entry_ids`.
One native disc/reference pair defines one article record. Multiple sections
allow introduction, body, continuation, and unknown roles. `issue_id: null`
and empty TOC links preserve a source whose issue/match is not established.
An article may link to multiple TOC entries, and an entry may link to multiple
articles; both directions must agree in TOC traversal order. Cross-issue TOC
links are rejected. Source-internal navigation is not an inferred related-article
or recommendation relationship.

## Issue metadata and catalog

Issue TOCs are flat arrays in depth-first source order with explicit `parent_id`
references. Parents must precede their children; closed branches cannot reopen.
Do not page-sort entries. TOC `kind` retains the imported candidate classification;
it does not certify that each entry is a distinct complete article.

`toc_status` is `available`, `partial`, or `missing`; `missing` requires an empty
array. Availability describes the metadata supplied, not complete CD or printed
issue coverage. Each entry has a title, nullable byline, nullable start/end pages,
`article_ids`, and `link_status`. `matched` requires links; `unmatched` has none.
An unmatched TOC entry does not prove the CD lacks its body. If an article is
known but not prepared, its record can explicitly use `not_prepared`.

Article titles/bylines are display strings backed by source evidence. A byline
is not necessarily a person's normalized name. Preserve the pilot's editorial
byline rather than guessing contributors. End pages remain unknown unless
supported; an end page requires a known start and cannot precede it. Unknown
covers use `cover_media_id: null`; a known cover resource can instead reference
a media entry with an unavailable status.

The catalog is the exact ordered projection generated by `catalog_for`:
issue ID/date/label/TOC status/cover and article ID/issue/title/byline/pages/content
status. `search_fields` is exactly `title`, `byline`, `issue_id`. Null bylines
contribute no search text. Search interaction and normalization belong to the
client; v1 has no full-text index or invented recommendations. Unmatched TOC
titles remain available in issue documents, not synthetic catalog articles.

## Ordered content and rendering semantics

An article contains ordered sections, then ordered blocks, paragraphs, and runs.
All blocks retain at least one paragraph, including empty source paragraphs.
A paragraph with no runs is an empty line. Text runs carry literal `text` and
`marks` (`bold`, `underline`, or neither); media runs carry `media_id`, a unique
`occurrence_id`, and marks. Inline strings contain no CR or LF: each paragraph
boundary contributes **one LF, including the last paragraph**. Do not trim,
normalize Unicode, collapse spaces, remove empty paragraphs, or reorder runs.

| Block type | Required interpretation |
| --- | --- |
| `title`, `issue_label`, `byline`, `paragraph` | Source-supported text/media in flow order |
| `heading` | Level 1–3 and explicit parent; hierarchy cannot skip a level |
| `code` | Preformatted paragraphs and inline media; preserve indentation, blank lines, trailing spaces |
| `caption` | Text at its source position, with explicit `caption_for` relationship |
| `figure`, `table` | Image-backed content; at least one media occurrence, with text if present |
| `spacing` | Empty/whitespace-only paragraphs, without media |
| `unresolved` | Preserved content whose semantic interpretation remains unresolved |

`layout` is `preformatted` for code, `spacing` for spacing, otherwise `flow`.
Every block identifies its preceding enclosing heading through
`parent_heading_id`, or `null`. Heading scope resets at each section boundary.
`interpretation: source_supported` means the current source/block evidence
supports the classification; it is not print verification. An unresolved block
must use `interpretation: unresolved`.

The mixed code example contains ten WMF occurrences among text runs. A client
can render runs in a whitespace-preserving container with inline image elements
and explicit paragraph breaks. A Markdown image string inside a fenced code
block would not provide that behavior. Render literal text as text nodes:
`<tag>`, ampersands, and Markdown punctuation are source characters, not HTML or
Markdown instructions. Apply marks separately; do not parse run text as markup.

`caption_for` links caption blocks to code, figure, table, or unresolved blocks
within the article. Every caption must be linked. Keep captions in their original
position; the relationship does not authorize duplicating or moving them.
The v1 table fallback is an image, with no invented rows/cells or OCR text.
Font IDs/sizes and detailed RTF geometry remain in preservation evidence;
bold/underline, semantic hierarchy, paragraph boundaries, and mixed runs are the
runtime reading model. It is not a facsimile of CD or printed page layout.

## Media, paths, and configurable base URL

Every referenced resource appears in the media index, including unavailable
resources. `available` requires an `asset` and a null reason. `deferred`, `missing`,
and `unsupported` require `asset: null` and a nonempty reason. Deferred media
also require `problem_ids` pointing to preserved problem records. A consumer
must retain an unavailable-media placeholder at each occurrence and preserve
associated captions. Do not render a suspect derivative through a fallback path.

Assets specify package-relative `path`, MIME type, bytes, SHA-256, and positive
dimensions with explicit units (`px`, `mm`, `cm`, `in`, or `pt`). Supported display
formats are PNG, SVG, JPEG, and WebP. Paths and MIME extensions must agree.
Media paths start with `media/`; all package paths use safe ASCII segments,
without absolute paths, dot segments, escapes, queries, fragments, or backslashes.
Multiple identities may share an asset path only if all asset metadata agrees.
`rendering_notes` carries limitations such as `font_substitution_possible`.
An available derivative is usable for preparation, not proof of image fidelity.

The deployment supplies a **package base URL**, e.g.
`https://example.test/archive/data/`. Every manifest/asset/preview path resolves
against that directory, never against the current SPA route or article file.
For a configured absolute or site-relative directory URL without query/fragment:

```js
const root = new URL(baseURL.endsWith('/') ? baseURL : baseURL + '/', document.baseURI);
const assetURL = new URL(asset.path, root);
```

Thus `media/cd1/bm41.bmp.png` works under `/archive/data/` as well as `/data/`.
The data contains no machine-local paths or hard-coded deployment origin.
The client uses a media item's `source.resource` for a factual placeholder label
if needed; it must not invent a description of unseen image content. Loading a
prepared SVG as an image does not require treating its contents as article HTML.

## Extraction, print verification, and provenance

Article `content_status` is `available`, `not_prepared`, or `unavailable`.
Available content must have sections. The latter two have empty sections and
relationships and `extraction_status: unchecked`. `extraction_status: checked`
means the export passed the recorded source-integrity/projection checks.
These fields do not grant publication permission or establish print accuracy.

`print_verification` is independent: `pending` has a null report and no compared
pages. `partial`, `matched`, and `differences` require a report ID and a nonempty,
unique, sorted list of actually compared printed pages. The report records the
issue/edition, source scans/photos, reviewer, comparison extent, and observations.
Only examined evidence can justify these statuses; schema validity alone cannot.
In particular, `matched` must not be used to imply full comparison from partial
pages. Corrections based on print evidence retain the CD-derived version and
separate provenance. Original CD-viewer comparisons are not required.

Runtime source identifiers and problem/report IDs connect to preservation records.
The private `provenance.json` sidecar carries input hashes, schema hash, metadata
evidence, paragraph source spans/run ordinals, block-map reference, and asset
bindings to local derivative files. The pinned recovery/map files retain exact
run byte spans and RTF styles. These details are not required for client rendering.
Legacy `viewer_compared`/`converted_pending_viewer` fields stay in historical
source records; runtime availability and print status have their own semantics.

## Pilot result and reproduction

The pilot is article `8802065`, **유닉스란 무엇인가?**, linked to the February 1988
TOC. Its contract example contains:

- One issue with all **39** imported TOC entries in original tree order; only
  the established pilot match is linked. The other 38 remain unmatched.
- One article with two sections, **271 blocks, 323 paragraphs, and 289 runs**
  (268 text runs and 21 media occurrences), plus 13 caption relationships.
- **21** named media resources: 19 available derivatives (nine PNGs, ten SVGs),
  and `bm54.wmf`/`bm55.wmf` deferred with null assets and recorded problem IDs.
- Unknown cover and ending page, source-supported starting page 65,
  extraction checked, and physical-magazine verification pending.

The exporter reconstructs each source paragraph and each block's checksummed
text, representing media as its original `[object:filename]` placeholder for
comparison only. Independent tests compare every text run, mark, and paragraph
against recovery data and the saved introduction/body text. This proves source
text/order preservation; it cannot establish print completeness or image fidelity.

With the existing private recovery, TOC import, block map, image map, and deferred
register present, run:

```sh
make reading-room-example
make check
```

The exporter validates pinned inputs and accepted derivative hashes, checks the
reviewed [metadata summary](../data/catalog/reading-room-examples/cd1-8802065.json),
and writes `pilot.example.json` plus `provenance.json` under
`build/reading-room-contract/8802065/`. It neither copies media nor changes the
existing recovery outputs. Output bytes and hashes reproduce on repeated builds;
no timestamps are injected. After an intentional reviewed contract/input change,
refresh the tracked summary explicitly with:

```sh
PYTHONPATH=src python3 -m tools.build_reading_room_example --write-record
```

Public contract tests use only synthetic content; private pilot tests skip when
its private source artifacts are absent. The synthetic fixture's asset sizes and
zero hashes are illustrative and have no corresponding image files: it validates
the logical contract, not package filesystem integrity.

Step 9 took this validated example and private asset bindings as inputs, wrote
the documented runtime files and previews, copied only the 19 accepted assets,
and created an actual manifest. Its completion checks resolve every reference,
verify all file hashes, preserve deferred placeholders, and reproduce the package
without requiring RTF parsing in the reading room. All package content stays
private; the first preparation milestone is complete. See the
[package report](CD1-PACKAGE-8802065.md) for reproduction and remaining limitations.
