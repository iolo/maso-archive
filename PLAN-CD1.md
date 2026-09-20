# CD1 extraction and reading-room content plan

Revised 2026-09-20. This is the active work queue for extracting CD1 and organizing
its content for the reading room. The separate [reading-room PRD](PRD-reading-room.md)
owns the viewer's UI and application architecture. The previous broad archive
plan remains in [Design reference](docs/DESIGN-REFERENCE.md) as historical context.

## Goal and first milestone

This plan's goal is **reproducible CD1 content extraction and a static content
package that the reading room can consume**: issue/TOC metadata, article text and
semantic blocks, captions, converted media, source relationships, and explicit
coverage/review status. The first milestone is **one reproducible CD1 article
package, linked to its TOC record and usable by the reading room, with known
broken-media exceptions explicitly deferred**. Physical magazine pages are the
reference for later content verification. Original-viewer comparison is not a
required task; print verification does not block extraction or packaging.

**First preparation milestone completed in step 9:** the
[private pilot package](docs/CD1-PACKAGE-8802065.md) validates and rebuilds
identically, including explicit unavailable states for both deferred images.
Physical-magazine verification remains pending.

**Current milestone: the first complete CD1 extraction pass (steps 13a–13d).**
February's six prepared articles provide the regression baseline. Build a shared
batch pipeline, validate it on those articles and a bounded sample from other
issues, then process the remaining CD1 work queue with resumable issue checkpoints.
Completion means every discovered candidate has a recorded outcome, with available
content packaged and unresolved cases retained for follow-up. It does not mean
complete coverage of every printed issue or resolution of every damaged image.

The archive target is **1983-11–1995-12: 146 monthly issues**, extended because
the owner holds the official CDs. The supplied TOC now covers **122 issues
through 1993-12**; that source coverage is distinct from the expanded target.
CD1's observed index coverage is **1988–1993**, all within the new target. Prepare
its available content in controlled batches, preserving 1991–1993 source identities
without inventing entries in the supplied TOC. Additional issue/TOC metadata must
come from inspected CD records or later supplied sources.

CD2's apparent 1994 coverage and CD3's apparent 1995 coverage are handled separately
in [PLAN-CD2.md](PLAN-CD2.md) and [PLAN-CD3.md](PLAN-CD3.md). Those are deferred
source-specific queues, not additional tasks in this CD1 plan. Source coverage
and article completeness still require verification. Missing 1983–1987 scans
remain a separate future source task.

Full-text extraction/preparation is required regardless of whether an article is
ever published. Keep the recovered text and provenance private and reusable.
Possible future access for paper-issue/CD owners is a separate product decision;
eligibility rules and ownership/access verification are unresolved. They do not
block extraction, and no access mechanism is selected in this checkpoint.

Proceed from **one article → one reading-room content package → one issue → CD1**.
Use what each step teaches us to specify the next. Missing scans do not block
the first milestone.
Do not estimate or automate collection-wide extraction until we understand the
one-article path. Check extraction integrity against the preserved CD sources,
and record content accuracy against physical magazine pages separately. A valid
extraction/package is not a claim of print verification. Deferred image failures
remain visible in the coverage record rather than requiring immediate repair.

## Responsibility and handoff

| This plan produces | The reading-room PRD owns |
| --- | --- |
| Recovered text, semantic blocks, media derivatives, and provenance | Article/media display and reading typography |
| Stable issue/article/media identities, TOC order, and explicit relationships | Issue selection, navigation, routing, and responsive layouts |
| Pregenerated catalog/search data and content availability status | Client-side browsing/search interactions and missing-content presentation |
| Versioned static data files and validation reports | Vite/React/TypeScript SPA, components, themes, and application tests |

The handoff must work with the PRD's **static files and client-side SPA**, with no
runtime extraction, server, database, or backend requirement. Extraction tools
remain offline build tools. Viewer development can use the first sample package
without waiting for the entire CD to be processed.

Keep three layers distinct: preserved source/recovery evidence; structured reading
content with ordered blocks and media relationships; and derived reading exports
such as Markdown. Markdown remains useful for review, but mixed code/image content
must also be available as structured data so the viewer can represent it faithfully.
The [v1 content contract](docs/READING-ROOM-CONTENT-V1.md), completed in step 8,
defines this handoff using the pilot's inspected structures.

Packages stay private during preparation. Choosing publication content, deployment,
or an ownership/access policy belongs to separate work; extraction and packaging
continue independently of those decisions. Source-internal navigation, unresolved
attachments, and absent covers must remain explicit rather than becoming guessed
editorial relationships or synthetic assets.

## Already completed

- [x] Inspect all three discs and record their ISO hashes and format findings.
- [x] Establish initial source availability: 50 issues from 1983–1987 start with
  TOC metadata; the owner will arrange scans later. The supplied TOC also covers
  36 issues from 1988–1990 eligible for CD1 enrichment. The expanded archive target
  adds 60 monthly issues for 1991–1995; their TOC metadata is not yet imported.
- [x] Run the CD1 viewer in the owner's DOSBox-X environment.
- [x] Prove direct CD1 extraction: raw RTF, image resources, and three indexes
  are preserved privately with a checksummed manifest. Fidelity is unverified.
- [x] Import all 86 supplied TOC issues and 3,811 entries with persistent identities,
  article candidates, a local search-data preview, and validation tests.
- [x] Structure all 3,032 CD1 index lines and preserve their 2,462 reference
  occurrences, grouped into 1,080 native targets; see [CD1 index](docs/CD1-INDEX.md).

These are reusable results. Do not rewrite them just to follow the new sequence.
The 2,975 TOC article candidates and 1,038 CD index references are different
populations; neither is a verified count of complete articles.

## How each step works

1. Work on one numbered step at a time. A request to do the “next task” means
   the next unfinished, non-deferred step, unless the user explicitly requests
   a larger batch. Resume a deferred task when its evidence is available and
   it is scheduled, rather than blocking the active queue.
2. Before implementing, name the input, one main deliverable, and completion
   check. Avoid adding adjacent features to the same step.
3. If a step reveals another substantial unknown, split it into smaller steps
   here. Preserve the finding instead of silently expanding the work.
4. Validate the deliverable, log the result and limitations in
   [PROGRESS.md](PROGRESS.md), inspect the staged changes, and commit the step.
   Record failed experiments too. Use the existing identity map and preserve
   prior review decisions.
5. Report what is done and what comes next, then end that task. This does not
   require extra approval for routine edits, tests, or other work within the step.

## Pilot extraction status

| Step | Deliverable | Complete when |
| --- | --- | --- |
| 1 — Done | CD1 reference index | All three extracted `.lst` files are represented as structured records, retaining every occurrence, category path, title, source line, and original reference; counts and parse exceptions are reported. |
| 2 — Done | One explicit CD-to-TOC match | `8802065` is linked to `maso-1988-02-toc-0035` with both CD occurrences, title/issue evidence, and an explicitly conditional page comparison. |
| 3 — Done | Raw topic map for that article | Native context/hash evidence resolves `8802065` to body topic 149 and its linked introduction 148; byte locations and following boundaries are recorded, with completeness relative to print unverified. |
| 4 — Done | One correctly decoded paragraph | The first body paragraph decodes strictly to 182 characters; byte provenance, font/encoding decisions, punctuation handling, and unsupported cases are recorded. |
| 5a — Done | RTF feature inventory for the mapped topics | All 149,579 bytes in introduction 148 and body 149 are accounted for; fonts, metadata groups, 21 object markers, and five HELPDECO literal-brace guards are located. |
| 5b — Done | Full text for that one article | Both mapped topics produce private ordered text and structured paragraphs/runs, with 21 object placeholders, all bytes accounted for, and the step 4 paragraph reproduced exactly. Image-contained text and print verification remain pending. |
| 5c — Done | Block identification for the pilot | 271 blocks cover all 323 paragraphs, 289 runs, and 21 objects; headings, examples, caption relationships, image-backed tables, and unresolved content retain evidence and source references. |
| 5d — Done | Private Markdown reading preview | Separate introduction/body previews represent all 271 blocks, preserving code whitespace, heading hierarchy, caption links, and ordered object placeholders, with source/output hashes and byte locations. |
| 6 — Done | That article's image map | All 21 occurrences match the extraction manifest and have private derivatives; nine bitmap conversions preserve decoded pixels. Blank `bm54.wmf` and the equation's damaged symbols remain explicit review exceptions. |
| 7 — Deferred | Physical-magazine comparison record | When paper pages or scans/photos are available, compare title, author, page range, text, structure, figures, and captions. Record differences and deferred media; this is not a prerequisite for content preparation. |
| 8 — Done | Reading-room content contract v1 | Schema, relationship validator, synthetic example, and reproducible private pilot preserve ordered text/media, identities, captions, missing values, and independent extraction/print status. |
| 9 — Done | One-article content package | All 26 runtime files validate; 19 accepted images and two Markdown previews are included, two media exceptions stay unavailable, and package/provenance bytes reproduce exactly. |
| 10 — Done | Second-article schema check | `8802114` preserves unnumbered headings and three long Fixedsys/Pascal listings under unchanged v1; standalone and combined two-article packages validate and reproduce. |
| 11a — Done | Local CD1 preservation inventory | All 5,828 disc files and 375 directories match a fresh ISO extraction; all 7,374 probe manifest entries plus three supporting files are inventoried. |
| 11b — Deferred | Independent backup/restore verification | The owner confirmed no independent backup yet. Preserve the source set on separate storage and check a real restore when available; this does not block non-destructive extraction. |

Steps 1–6, 8–10, 11a, 12a, 12a.1, 12b.1–3, 12c, 12d, and 13a are complete.
Step 7 is deferred pending physical-magazine evidence; 11b awaits independent storage or an optical drive.
**Step 13b (shared extraction and packaging pipeline) is next.**
Backup/restore verification does not block extraction from the verified sources.
The first preparation milestone is complete: step 9's
article package validates, including explicit placeholders for deferred media.
Print comparison remains a separate pending status. No original-viewer screenshots
or side-by-side CD-viewer checks are required to advance.

Selected pilot: **1988-02, “유닉스란 무엇인가?”, TOC page 65**, with CD reference
`8802065`. The [step 2 match](docs/CD1-MATCH-8802065.md) supports the metadata
relationship; the [step 3 topic map](docs/CD1-TOPIC-8802065.md) adds raw boundaries
and an explicit CD page-65 label. Content completeness remains unverified. If
the feature proves too complex for a first sample, document why and choose a simpler
article from step 1's inventory; do not force a one-topic-per-article assumption.

The owner can prepare physical-magazine reference pages when convenient using
[the offline task checklist](docs/OFFLINE-TASKS.md). These are evidence for later
print comparison, not prerequisites for the content contract or sample package.
Keep original CD extraction records intact when print/CD differences are found.

## Step 1 completed: index import

**Inputs:** `private/cd1-probe/raw/column.lst`, `language.lst`, and `panecmds.lst`,
plus the existing extraction manifest.

**Output:** a reproducible local index and validation report under
`build/cd1-index/`, produced by a small importer with focused tests. Record source
hashes, encoding, hierarchy, and line locations. Keep all index occurrences;
provide a separate view grouped by reference without losing their categories.

**Checks:** strict decoding succeeds or failures are reported; every nonblank
source line is accounted for; repeated references across indexes stay traceable;
the same inputs give identical outputs. For the current files, check the earlier
observations of **1,038 distinct seven-digit references**, including **360 in
1988–1990**. All 1,038 now fall within the expanded 1983-11–1995-12 target; retain
the earlier-period count as source evidence. A discrepancy must be explained
rather than forced to match a count.

This step does not read the 74 MB RTF, convert images, match all articles, add
summaries, or build a UI. Preserve the original index files and keep generated
content local. Commit the importer/tests, any necessary documentation changes,
and its progress entry.

Result: `make import-cd1-index` produces these artifacts. All source lines are
accounted for; the numeric-reference baseline matches. The additional 41
letter-suffixed targets and one named navigation target are preserved separately.
See [usage and validation details](docs/CD1-INDEX.md).

## Step 2 completed: one metadata match

**Inputs:** the generated CD1 index, the existing TOC import, and their source
locations. Start with native reference `8802065`.

**Deliverable:** one explicit source-match record linking that CD reference's
occurrences to an existing TOC entry ID, accompanied by title, issue, and page
evidence and an explanation of any discrepancy. Keep source labels and the
original TOC identity unchanged.

**Check:** the proposed relationship is supported by the source metadata; any
ambiguity remains marked for review instead of being declared verified. This
matches metadata only: it does not establish that the complete body was recovered.

Do not add collection-wide matching, RTF decoding, image conversion, or a review
UI to this step. If the reference maps to a feature bundle rather than a single
article, record that relationship explicitly before deciding on a simpler pilot.

Result: [the match record](data/catalog/source-matches/cd1-8802065.json) links
reference `8802065` to `maso-1988-02-toc-0035`. The title and explicit issue labels
agree. Page 65 is reported by the TOC and is consistent with the reference suffix,
but is not independently verified by the CD index. The TOC has a single feature
entry; the number of CD topics remains unknown. Recheck with
`make restore-toc-snapshot` followed by
`PYTHONPATH=src python3 -m tools.verify_cd1_match`.

## Step 3 completed: raw topic map

**Inputs:** the accepted metadata match, preserved CD1 container/extraction
metadata, and raw RTF/project output as needed, all read-only.

**Deliverable:** a raw topic map for `8802065` with the source hashes, context or
link evidence resolving the native reference, and byte locations of relevant
topic records. Distinguish a feature introduction from article-body topics.

**Check:** the mapping is supported by context/link evidence, not just a title
string search. Identify the next-topic boundaries and document any uncertain
continuations. A feature may contain multiple topics; do not assume one-to-one
correspondence or silently merge adjacent articles.

Keep text normalization, image conversion, summaries, and bulk matching outside
this step. If resolving the context reveals a separate substantial problem,
record the finding and split the step before expanding implementation.

Result: [the topic map](data/catalog/topic-maps/cd1-8802065.json) resolves the
native reference by context hash to ordinal 149 (`2PES_R6`), linked to introduction
148 (`3M4UMD`). Native topic headers and raw RTF delimiters agree. A following
untitled separator and the next article, “스펠링 체커”, are explicitly excluded.
The CD body labels itself `88.2.  65p`; no general page-mapping rule is inferred.
Recheck with `python3 tools/map_cd1_topic.py`. See the
[evidence and remaining limits](docs/CD1-TOPIC-8802065.md).

## Step 4 completed: one decoded paragraph

**Inputs:** the pinned raw RTF, its font/header definitions, and step 3's body
range for ordinal 149. Keep source reads and any decoded sample private.

**Deliverable:** one decoded paragraph from the body, with its exact raw byte
span, font/encoding decisions, and a reproducible local conversion/check command.
Choose a small sample that exercises Korean and English; document any special
characters encountered and unsupported cases. Do not decode the whole article.

**Check:** strict decoding has no silent replacements; text characters and RTF
controls are distinguished, and the sample stays within the mapped body. Preserve
the original bytes. A successful decode does not establish agreement with print;
physical-page comparison is deferred in step 7. Keep image conversion and full-text
normalization outside this step, and log/commit the result before proceeding.

Result: `python3 -m tools.decode_cd1_paragraph` produces one private paragraph
and its raw-byte/provenance artifacts in `build/cd1-paragraph/8802065/`. The
sample is 182 characters and matches independent `iconv` CP949 decoding. The
RTF resets to default Arial without an explicit code page; CP949 is recorded as
a source-specific choice. See [the sample notes](docs/CD1-PARAGRAPH-8802065.md).
Print verification remains pending. The limited sample does not exercise groups,
font changes, tables, or symbol glyphs, so full-text recovery is split below.

## Step 5a completed: RTF feature inventory

**Inputs:** the pinned RTF header and step 3's separate introduction/body spans
(ordinals 148–149), plus step 4's supported/unsupported feature list.

**Deliverable:** a reproducible local inventory of RTF controls, referenced fonts,
group/destination types, and structural features within those two topics. Record
counts and byte locations for features needing support or review. Keep title,
footnote/navigation metadata, text, and object markers distinguishable.

**Check:** the tokenizer accounts for every byte inside each mapped span,
distinguishes escaped text from syntax, and reports unknown constructs without
discarding them. Record font/encoding uncertainty explicitly. This is inspection
only: do not decode full article text or convert images yet. Use the inventory
to specify the bounded step 5b implementation; split again if a substantial
unknown requires its own task.

Result: `python3 -m tools.inventory_cd1_rtf` accounts for both mapped spans and
records every token's byte location locally. The inventory distinguishes six
metadata footnotes, their markers, one hidden context link, and 21 object markers
from visible text. Arial and 굴림체 carry text; Times is selected only in an empty
introductory paragraph. Five literal-brace guards added by HELPDECO require
explicit handling. See [the inventory notes](docs/CD1-RTF-INVENTORY-8802065.md).

## Step 5b completed: private full-text recovery

**Inputs:** the pinned RTF, separate topic spans, step 5a's token/group/font/object
inventory, and step 4's verified paragraph bytes and decoded-output hash.

**Deliverable:** private ordered full text for introduction 148 and body 149,
plus structured paragraphs/runs retaining source spans and observed formatting.
Keep section headings and code-like text/spacing; do not rewrite spelling or
infer table semantics. Keep metadata footnotes and the hidden navigation target
separate from visible article text. Retain all 21 object markers in order with
explicit placeholders and byte provenance until step 6 handles their resources.

**Check:** every source token is represented as text, metadata, formatting,
object reference, or a documented unsupported construct. Decode strictly using
recorded font state; an undecodable run must retain its raw location and remain
flagged. Explicitly handle the five HELPDECO brace guards without inserting
spurious hyphens into example code. The original step 4 paragraph must reproduce
exactly. Preserve introduction/body separation and exclude neighboring topics.

Recover all available text now regardless of eventual publication/access policy.
Image conversion is step 6; physical-magazine comparison is deferred in step 7.
Producing the full text does not itself establish article completeness or display
fidelity.

Result: `python3 -m tools.recover_cd1_text` writes separate introduction/body
text, structured paragraphs/runs with formatting/source spans, and provenance to
`build/cd1-text/8802065/`. All 268 text runs decode strictly; all 149,579 source
bytes are accounted for. The 4/319 introduction/body paragraphs retain blank lines,
and all 21 object placeholders stay in order. The step 4 sample matches exactly.
See [full-text recovery notes](docs/CD1-TEXT-8802065.md). Text inside image resources
is not transcribed, and print verification/article completeness remain pending.

## Step 5c completed: block identification

**Inputs:** the private structured recovery, source RTF formatting, text/context,
object locations, and the [structural review](docs/CD1-BLOCK-STRUCTURE-8802065.md).
Plain-text exports are convenience files, not the final reading representation.

**Deliverable:** a separate block map referencing existing paragraphs/runs and
source spans. Identify title/heading candidates, prose, code/examples, captions,
figures, and possible tables, with evidence and review/uncertainty status. Keep
unresolved content intact. Use formatting together with numbering, code syntax,
caption labels, and context; style alone is demonstrably ambiguous in this pilot.

**Check:** account for every paragraph/run/object once in source order; preserve
code spaces and internal blank lines. Caption relationships may target code or
images, and composite figures may contain multiple objects. Do not infer cells
for a table without evidence. Keep the recovered paragraph/run data unchanged,
and retain source/layout uncertainty for later print comparison.

Result: `python3 -m tools.map_cd1_blocks` produces a separate, traceable block map
in `build/cd1-blocks/8802065/`. It identifies 28 headings, 17 code/example blocks,
and 13 caption relationships without changing the recovered paragraphs/runs.
The `tbl` example retains ten inline WMF objects as mixed content; the following
`bm54.wmf` remains unresolved. See [block-map details](docs/CD1-BLOCK-MAP-8802065.md).

## Step 5d completed: private Markdown preview

**Inputs:** the validated block map, unchanged paragraph/run recovery, and
caption/object relationships. No image conversion is required for this preview.

**Deliverable:** private Markdown for the separate introduction/body, with
provenance linking the export to source and block-map hashes.
Generate Markdown from the block map, preserving heading hierarchy, fenced code,
inline emphasis, and figure/caption relationships. Keep unresolved resources as
explicit placeholders until step 6. Emit tables only where cell structure is
supported; otherwise retain an image/structured fallback and a review marker.
For mixed text/object examples, preserve ordered placeholders and an explicit
limitation note; do not pretend Markdown image syntax renders inside code fences.
Keep `bm54.wmf` unresolved until its attachment is established.

**Check:** code content/spacing and object order survive export; prose Markdown
syntax is escaped without altering source text. Use fences long enough to avoid
collisions, and retain the three-level heading hierarchy and caption links.
No source block disappears from the export without an explicit representation.
Preserve RTF, paragraph/run JSON, and semantic decisions separately from this
reading format.

Result: `python3 -m tools.render_cd1_markdown` writes private `introduction.md`,
`body.md`, and `provenance.json` under `build/cd1-markdown/8802065/`. All 271 blocks
are represented, with 17 verbatim code fences, 28 hierarchical headings, 13
caption links, and 21 ordered object placeholders. An independent Markdown parser
reproduces each block's text, including code whitespace; spacing blocks retain
explicit comments and source whitespace. Inline HTML retains bold, underline, and
stable anchors. Original print layout, deferred images, and print verification
remain pending. See [Markdown preview details](docs/CD1-MARKDOWN-8802065.md).

## Step 6 completed: image map and conversion report

**Inputs:** the 21 ordered object references in the private text recovery,
their RTF locations, extracted BMP/DIB/WMF resources, and the extraction manifest.

**Deliverable:** a private image map connecting each occurrence to its source
resource and paragraph/run position, with source hashes, format/dimensions where
readable, and viewable derivatives or a specific unsupported/missing status.
Keep originals intact and derivatives outside Git. Distinguish a navigation icon
from editorial images where evidence supports that distinction; do not infer
that every resource is a separate illustration.

The owner suggested `convert` for Windows BMP/DIB → PNG and `inkscape` for WMF →
SVG. Both are available in the current environment (also `magick`). Use them as
the initial conversion path, record actual commands/versions, and inspect the
results; availability does not establish conversion fidelity. Pay particular
attention to the ten inline WMFs in the mixed example and unresolved `bm54.wmf`.

**Check:** account for all 21 occurrences, verify files against the extraction
manifest, and inspect rendered results for obvious conversion failures. Preserve
repeated/composite resources in their original order. Document unreadable assets
and fidelity uncertainties rather than silently omitting them. Do not perform
bulk extraction, OCR, publication, or access-verification implementation here.
Physical magazine pages are the content reference for deferred step 7. Technical
checks still verify CD bytes, decoded text, and conversion outputs. CD-only badges,
navigation, and reformatted layout need not match the printed page presentation.

Result: `python3 -m tools.map_cd1_images` writes private `images.json`,
`provenance.json`, `review.html`, nine PNG derivatives, twelve SVG derivatives,
and twelve PNG inspection previews under `build/cd1-images/8802065/`.
All 21 named resources match the source manifest; six distinct WMF names share
identical bytes, leaving 16 distinct source hashes. All nine bitmap conversions
preserve dimensions and decoded RGBA pixels. Two WMFs require review: `bm54.wmf`
produces a blank drawing; `bm55.wmf` loses mathematical Symbol glyphs in the
equation. Live SVG text also depends on local fonts. See
[image findings and reproduction](docs/CD1-IMAGES-8802065.md).

### Deferred media policy

At the owner's request, defer investigation/repair of broken conversions such as
`bm54.wmf` and `bm55.wmf`. Keep their originals, hashes, occurrence positions,
captions, failure observations, and conversion attempts in the
[deferred-media register](data/catalog/deferred-media/cd1-8802065.json). Revisit
them only in a later scheduled media-repair task; they are not current blockers.
Apply the same record-and-defer approach to further conversion failures.

Reading exports should use an unavailable-media placeholder at the original
position, retaining any caption. Suspect/blank derivatives may remain in the
private diagnostic review page but should not be presented as recovered article
images. Deferral changes work priority, not source evidence or fidelity status.

## Step 7 deferred: comparison with physical magazines

**Inputs, when available:** the physical February 1988 issue or legible scans/
photos with printed page numbers, plus the preserved CD1 topic/text/block records,
Markdown preview, image map, and deferred-media register. TOC page 65 is a starting
locator, not proof of the complete printed article's page range.

**Deliverable:** a print-comparison record identifying issue/edition, evidence
files and page ranges, reviewer observations, and the extent actually compared.
Cover title/author, article boundaries and continuations, text, code, headings,
figures, tables, and captions. Distinguish CD editorial/reformatting differences
from extraction errors. Preserve CD-derived text and document any proposed
print-based correction separately, with provenance.

**Check:** distinguish matches, differences, unobserved pages, and deferred media.
Partial scans establish only partial comparison. Keep print verification pending
until the relevant evidence has actually been examined; the existence of an
original magazine or official CD is not a verification result. Broken conversions
remain deferred. This task can resume when reference pages are available and
scheduled; it does not block steps 8–9 or later content preparation.

## Step 8 completed: reading-room content contract

**Inputs:** the recovered pilot metadata/text, semantic block map, image map,
deferred-media register, and static-data requirements in the reading-room PRD.

**Deliverable:** a versioned static-data contract and a validating pilot example
covering issue/TOC/article/media identities, ordered blocks and mixed content,
caption relationships, media placeholders, and source/verification status.
Keep preservation evidence separate from the viewer's required runtime data.

**Check:** represent the current pilot without losing source order or code
whitespace, inventing missing metadata, or treating broken media as usable assets.
Distinguish extraction checks from pending physical-magazine verification. The
contract must support a static client-side reading room without a backend or
runtime RTF parsing. No print capture or original-viewer comparison is required.
This step defines the contract; the full sample package is step 9.

Result: [contract v1](docs/READING-ROOM-CONTENT-V1.md) and its
[schema](schemas/reading-room-v1.schema.json) define catalog, issue, article,
media, and package-manifest documents. `make reading-room-example` regenerates
the private validating example and provenance sidecar. All 39 issue TOC entries
remain ordered, with only the established pilot match linked. Two sections,
271 blocks, 323 paragraphs, 289 runs, 21 media occurrences, and 13 caption
relationships preserve the recovered source. Nineteen media assets have verified
private bindings; two deferred resources have null display assets. No files are
copied into a deployable package yet. All 77 tests pass, including independent
source-run/projection checks and contract rejection cases. Print status is pending.

## Step 9 completed: one-article content package

**Inputs:** the validated v1 pilot example and provenance/asset bindings, existing
Markdown previews, image map, and deferred-media register.

**Deliverable:** one private package containing `manifest.json`, `catalog.json`,
`media.json`, separate issue/article documents, Markdown previews, and the 19
accepted media files, with a separate preservation/provenance record. Use the v1
contract's relative paths and configurable package base URL. Keep deferred media
at their original positions with unavailable status; do not copy suspect display
derivatives. Do not add UI, bulk extraction, or media repair to this step.

**Check:** validate every document and the assembled relationship graph, resolve
all required file references, verify actual bytes/hashes against the manifest and
source bindings, and reproduce the package deterministically. Preserve exact
article text/whitespace and both deferred placeholders. The reading room must be
able to load the documented files without RTF parsing. Print verification remains
pending independently. Passing these checks completes the first preparation
milestone; publication and access policy remain separate.

Result: `make reading-room-package` writes the private
`build/reading-room-packages/cd1-8802065/content/` handoff, with preservation
evidence in the adjacent `provenance.json`. The 26 runtime files comprise four
JSON documents, the manifest, two Markdown previews, and 19 accepted images.
The assembled documents equal the approved step 8 example; every copied asset
matches its source bytes. All 271 Markdown block contents remain byte-identical,
while outdated generated status notes are updated only in the package copies.
Standalone validation checks file hashes, inventory, schema/relationships,
caption anchors, and SVG dependencies without extraction inputs. All 88 tests
pass. See [package reproduction and handoff](docs/CD1-PACKAGE-8802065.md).

## Step 10 completed: second-article schema check

**Inputs:** checked CD1 MVB/RTF and extraction manifest, existing TOC/index
imports, the pilot's neighboring-topic evidence, and the validated first package.

**Deliverable:** recover and package a different structural case using the approved
v1 schema; validate it alone and together with the first article. Record any
unsupported source constructs or required schema changes explicitly.

**Result:** [스펠링 체커, reference 8802114](docs/CD1-SECOND-ARTICLE-8802114.md),
February 1988 page 114, matches TOC entry `maso-1988-02-toc-0021`. Its linked
introduction/body topics 151–152 contain 39 blocks, 485 paragraphs, 439 runs,
unnumbered headings, three long Pascal listings, and one bitmap title badge.
The first decoder probe rejected 417 Fixedsys runs. Header/byte inspection
supports an explicit strict-ASCII policy for font 15 in this source; the decoder's
original default remains unchanged. Listing boundaries and heading decisions
are checked against this article's formatting and context.

**Check:** no schema change was needed. `make check-second-article` produces
private standalone (8 files) and combined (30 files) packages. The combined
package preserves both article identities, 808 paragraphs, two established TOC
matches, and the original two deferred images. Every text projection and copied
asset is checked; all 95 tests pass, including first-pilot hash regressions and
seven new second-case tests. Repeated builds reproduce output hashes. Print
verification remains pending; source code was preserved without repair/execution.

## Step 11: local inventory complete; independent backup/restore pending

**Inputs:** the original CD1 ISO, extracted source directory, existing probe
manifest, and any available independently stored backup with its location record.

**Deliverable:** a durable CD1 source inventory and preservation-readiness report.
Verify original/extracted file coverage and checksums, identify the preservation
set, and record backup/restore evidence when a separate storage location is
available. Keep machine-specific storage locations private. Existing probe hashes
are useful evidence but do not establish that a backup can be restored.

**Check:** account for the source files and distinguish inventory validation from
actual backup/restore verification. If external storage evidence is unavailable,
complete the local inventory and record the remaining owner task explicitly;
do not claim independent backup/restore verification on that basis. Extraction
may continue by reading verified originals and writing separate generated outputs.
Do not repair media, implement the UI, or expand to CD2/CD3 in this step.

Result: split this checkpoint into **11a complete** and **11b deferred** after
the owner confirmed that no independent backup exists yet. The command
`make inventory-cd1-sources` verifies the original ISO hash, compares all 5,828 files and
375 directories with a fresh extraction, verifies all 7,374 probe-manifest files,
and inventories three supporting files. The private detailed inventory has a
tracked hash/summary; [readiness](data/catalog/preservation/cd1-readiness.json)
keeps independent restore verification pending, separately from permission to
continue non-destructive extraction. All 104 tests pass. The restore
command is implemented and tested with synthetic fixtures, but no real independent
backup or restore is claimed. See [preservation instructions](docs/CD1-PRESERVATION.md).

## Completed scope: step 12a — February 1988 coverage audit

**Inputs:** existing TOC/index imports, native CD reference metadata, the two
prepared February articles, and the verified local source inventory.

**Deliverable:** an issue coverage report retaining every TOC entry and every CD
reference attributed to February 1988, explicit existing/new metadata matches,
unmatched/ambiguous entries, and prepared versus unprepared content status.
Use source labels and evidence; do not infer matches solely from reference suffixes.

**Check:** account for the full issue metadata populations without treating CD
index presence as complete printed coverage. Preserve source order and identity;
do not silently collapse references or invent article bodies. This is read-only
source analysis and metadata preparation, with no new article-body recovery or
bulk extraction. Define subsequent bounded article batches from its findings;
those may proceed without completing the deferred backup/restore task.

Result: [coverage audit](docs/CD1-COVERAGE-1988-02.md) complete: 39 TOC entries,
five indexed CD targets / 11 occurrences, four supported metadata relationships
(two existing, two new), and one unresolved title variant. Two targets are
prepared and three are unprepared. Thirty article candidates and four section
headings have no index match; absence from the indexes is not absence from the CD.
The approved runtime schema and existing packages are unchanged.

## Completed scope: step 12a.1 — expanded TOC validation/import

**Inputs:** the owner's 1991–1993 TOC additions, the existing identity registry,
reviewed TOC snapshot, import checks, and article provenance records.

**Deliverable:** validate the corrected issue headings supplied by the owner,
then import the expanded period while preserving every existing identity.
Update snapshot handling and regression checks so historical article evidence
remains reproducible when the working TOC grows. Do not guess the missing month
or silently rewrite old source fingerprints. This metadata task may proceed
while step 11b is pending; no new article recovery is included.

Result: 122 consecutive issues through 1993-12, 5,497 entries, and 4,078 article
candidates imported. All 3,811 old identities are preserved; 1,686 were added.
The owner's September heading correction is accepted; only an empty trailing
bullet was removed. Historical TOC/identity/import inputs now have a separately
checksummed, reconstructable snapshot. Both article witnesses and the coverage
report reproduce without changing their reviewed hashes or runtime schema.
See [TOC import and historical snapshots](docs/TOC-IMPORT.md).

## Completed scope: step 12b.1 — `8802030`

Step 11b handoff preparation is complete: a checksummed **674 MB local transfer
archive** contains the ISO, full probe, prepared artifacts, and Git history through
`a0cf997`. See the [transfer instructions](docs/CD1-PRESERVATION.md#prepared-local-transfer-set)
and [receipt](data/catalog/preservation/cd1-transfer.json). All archived payloads
and the Git bundle were checked locally. This is ready for the owner to copy;
the owner confirms the local copy is the working `masocd-1.iso`, extracted from
the retained physical CD. No optical drive is available. Restore verification
remains deferred until independent storage or an optical drive is available.

**Execution boundary:** read the checksummed sources and write generated outputs
separately. Step 11b is a deferred preservation task, not a prerequisite for
article recovery. Source modification, deletion, or replacement is outside this
extraction workflow. Backup status does not establish legal ownership or
publication permission.

**Inputs:** the five-target February coverage report, original MVB, preserved RTF,
indexes, media, and the two validated existing packages.

**Deliverable:** map and recover only `8802030` (CP/M의 게리 킬달), account for
native/RTF boundaries and all linked topics/media, preserve ordered content, and
produce a validated standalone v1 package. Combine it with the two existing
articles only after standalone checks pass. Preserve boundary uncertainty and
pending print verification; do not claim complete printed-issue coverage.

Result: [Gary Kildall interview](docs/CD1-INTERVIEW-8802030.md) prepared.
Topics 145/146 contain 71,443 RTF bytes, 107 paragraphs, 85 runs, and one bitmap.
All 27 prompts and 40 answer paragraphs retain their ordered text and bold/plain
formatting. Turn associations remain in the private block map/provenance; v1
paragraph blocks preserve the reading representation without schema changes.
Standalone (8 files) and combined three-article (34 files) packages validate.
The older packages and historical coverage report remain unchanged. Three of
February's five indexed targets are prepared; `8802184` and `8802180` remain.
The owner's *Programmers at Work* attribution is recorded separately from the
CD editorial byline and remains unverified against the book.

## Completed scope: step 12b.2 — `8802184`

**Inputs:** the metadata match for `터보 C로 작성한 에디터`, the checksummed native
MVB and preserved RTF/media, and the validated three-article package.

**Deliverable:** map only this article's native/RTF boundaries and linked topics;
recover all available text and preserve code/listing whitespace, font decisions,
media, and captions. Inspect actual structures before extending decoder behavior;
retain unsupported content explicitly. Validate a standalone v1 package before
composing the next combined package, preserving all earlier article bytes.

**Check:** exact source-byte/run/paragraph accounting, supported TOC/title/page
metadata, media disposition, and reproducible standalone/combined validation.
Physical-print comparison remains pending. Do not infer full issue coverage or
start `8802180`, remaining issues, media repair, or reading-room UI work in this batch.

Result: [Turbo C editor article](docs/CD1-EDITOR-8802184.md) prepared. Topics
160/161 account for 62,315 RTF bytes, 1,206 paragraphs, 1,117 runs, and five media
occurrences. The 85 blocks retain the 1,121-line C listing, a two-line code example,
14 headings, and four caption relationships. A bounded decoder extension preserves
all 30 RTF tabs as literal tab characters with source-byte transformation records.
Code whitespace and source spelling remain unchanged in JSON and Markdown.

Five bitmap conversions preserve decoded pixels, including three diagrams. The
standalone package (12 files) validates before composition into a four-article
package (41 files). The shared title icon has one media identity; older article
documents, previews, assets, and deferred media records remain identical. Schema
v1 is unchanged. Four of February's five indexed targets are now prepared;
`8802180` remains. Physical comparison is pending, and the historical coverage
audit remains a record of its earlier two-article state.

## Completed scope: step 12b.3 — `8802180`

**Inputs:** the February coverage audit's remaining candidate,
`maso-1988-02-toc-0026`, checksummed MVB/RTF/index/media sources, and the validated
four-article package. The TOC title is `터보 파스칼 한글 그래픽스 툴`; the CD index
title is `터보 파스칼 한글 그래픽 툴`.

**Deliverable:** review that specific title variation using native/body metadata
and page evidence before deciding the TOC relationship. Preserve both source
labels and the comparison rationale; do not globally normalize titles or force
an ambiguous match. Map and recover only `8802180`, preserving actual code,
figures, captions, and any unsupported content with explicit records. Validate
a standalone v1 package before composing it with the four prepared articles.

**Check:** complete selected-topic byte/run/paragraph accounting, supported
metadata relationships, reproducible packages, and unchanged earlier article
outputs. Keep print verification pending and defer failed media conversions.
Do not start remaining issues, reading-room UI work, or complete issue coverage
claims. Step 12c will reconcile the five-target preparation status with the full
TOC and produce the final issue package/coverage handoff separately.

Result: [Turbo Pascal graphics article](docs/CD1-GRAPHICS-8802180.md) prepared.
The native, introduction, and body titles exactly match the TOC, and the body
confirms February 1988/page 180. The shorter CD index title remains in provenance;
the evidence supports this specific match without global title normalization.
Topics 157/158 account for 26,283 RTF bytes, 397 paragraphs, and 362 runs.

Three Pascal listings preserve 18/210/91 paragraphs. This article's font 15
explicitly uses CP949 for Korean literals. One string has a recorded possible
Johab interpretation; the alternative is not silently applied. Figure 3 retains
its separate text and image paragraphs within one v1 figure block. The Markdown
renderer now handles that structure without changing earlier output.

Five bitmap conversions preserve pixels. Inline `bm57.wmf`/`bm58.wmf` remain
deferred because their Symbol font is lost in conversion; source references and
private diagnostics are retained. The 12-file standalone and 48-file combined
five-article packages validate. All older article/media outputs remain identical,
including the earlier exceptions. All five indexed February targets are prepared,
with four deferred WMFs in the combined package; print completeness is unverified.

## Completed scope: step 12c — February 1988 issue handoff

**Inputs:** the historical coverage audit, all five preparation/package records,
the validated five-article package, reviewed match evidence (including `8802180`),
current and historical February TOC metadata, and deferred-media/text-review records.

**Deliverable:** reconcile every one of February's 39 TOC entries and five indexed
targets against the prepared packages. Produce a new current coverage record
without rewriting the historical audit, and a validated issue handoff under
`build/cd1-issues/1988-02/`, with package-relative catalog/search metadata and
explicit missing/unmatched/deferred states. Preserve all article, preview, media,
and review evidence from the validated inputs; record any metadata differences.

**Check:** five prepared references and their supported TOC links resolve exactly;
four section entries and 30 remaining article candidates are distinguished from
prepared articles. All package paths/hashes validate after relocation, including
four deferred WMFs and the pending string review. Rebuild deterministically and
document the configurable static base URL handoff. Keep print comparison pending.
Do not recover new topics, repair images, build the reading-room UI, or start other
issues/CDs in this task. This completes the first issue preparation checkpoint,
not the remaining CD1 coverage work in step 13.

Result: [February issue handoff](docs/CD1-ISSUE-1988-02.md) completed under
`build/cd1-issues/1988-02/`. All 48 runtime files are identical to the validated
five-article package. The exporter also checks each article, preview, asset, and
media record against its standalone package and preserves all five provenance
documents in separate private evidence.

The new [current coverage record](data/catalog/issue-coverage/cd1-1988-02-prepared.json)
accounts for 39 TOC entries: five prepared articles, 30 unmatched article
candidates, and four section entries. All five indexed references and 11 index
occurrences resolve. Current/historical February text and metadata agree; 39
entry source identifiers change only because the whole TOC document expanded.
The old audit remains unchanged, including its earlier ambiguous graphics-title
decision; the new record incorporates the later supporting evidence.

The package retains four deferred WMFs, the pending CP949/Johab text review,
unknown end pages, unavailable cover, and pending physical comparison. Catalog
search remains metadata-only. Rebuild, relocated validation, and HTTP retrieval
of every runtime file under two nested base URLs pass. No topic recovery, media
conversion, or schema changes were needed for this handoff.

## Completed scope: step 12d — February native coverage closeout

The owner explicitly requested **February 1988**, so this task precedes the
previously queued disc-wide inventory. Check native metadata for articles omitted
from the indexes, prepare any February bodies found, and reconcile the issue.

**Inputs:** the checked MVB/RTF, all three index imports, the current/historical
TOC, and the five-article step 12c handoff. **Completion check:** every observed
February native issue keyword and opening page label resolves to a prepared
article; all 39 TOC rows remain accounted for and runtime content validates.

Result: scanning all **3,099 native/RTF topics** found **six February bodies**.
All 1,088 dated article titles agree between native headers and RTF footnotes;
ten titled navigation topics and 2,001 untitled topics are accounted for. The
independent opening date/page scan gives the same six February bodies, bounded
by January topic 143 and March topic 164. Eleven context/header-offset differences
in other issues are recorded for later review; no February association differs.
This is a February coverage check, not completion of the disc-wide step 13a.

Recovered the unindexed [KEYBOARD LOCK](docs/CD1-KEYBOARD-8802162.md), reference
`8802162`, with exact native/introductory/TOC title, explicit issue/page 162, and
numeric-context/body-alias agreement. Its 303 paragraphs retain two listings,
three image-backed tables, a diagram, and five pixel-equivalent PNGs. No index
occurrence was invented; the indexes still contain five February references.

The [current handoff](docs/CD1-ISSUE-1988-02.md) at
`build/cd1-issues/1988-02-native/` contains **six articles / 56 runtime files** under
unchanged schema v1. All previous article, preview, asset, and review evidence
survives. The earlier five-article checkpoint and historical reports remain
reproducible. Current coverage is **six prepared, 29 unmatched article candidates,
and four sections**. All observed native February bodies are prepared; mislabeled
content elsewhere and printed-issue completeness remain unverified. Further
February content needs scans or another source; print review, four deferred WMFs,
and the existing text-decoding question remain recorded, non-blocking follow-up.

## Next milestone: first complete CD1 extraction pass

The owner approved moving from article-specific preparation to batch processing.
The current scripts demonstrate recovery, structure preservation, media conversion,
and packaging, but several still encode article-specific topic numbers, paragraph
ranges, and caption relationships. Extract reusable operations and rules into one
pipeline; keep reviewed exceptions as data. Existing preparation scripts and their
historical outputs remain reproducible regression references.

The February scan already observed **3,099 native/RTF topics**, including **1,088
dated article topics**. The index contains **1,080 distinct targets** and **2,462
reference occurrences**. These are different populations, not interchangeable
article totals. Reuse that evidence to build the processing queue, including
unindexed content, linked introductions, and unresolved identities.

### 13a — Completed: build the CD1 processing inventory

**Inputs:** checked MVB/RTF and probe manifest, native metadata scan from 12d,
all three index imports, current TOC through December 1993, six February article
preparations, and existing exception records.

**Deliverable:** a reproducible inventory and machine-readable processing queue
for CD1. Reconcile every native topic, context/index target, and index occurrence;
record supported issue attribution, article/topic relationships, TOC match evidence,
prepared status, and unresolved cases. Preserve suffixed and named references.
Retain stable source identities for unindexed topics; page suffixes alone cannot
establish identity or a TOC match. Record linked, navigation, separator, and
unattributed topics with evidence rather than dropping untitled topics.

Include the eleven observed context/header-offset differences as investigation
items. Resolve associations where native evidence supports them, and leave
ambiguous candidates explicitly blocked with their source locations. Missing TOC
matches do not prevent preparation of independently identified article bodies.
Group ready candidates by issue, with a separate queue for uncertain attribution.

**Completion check:** all source populations reconcile without silent omissions
or duplicate article jobs; February's six preparations resolve unchanged, including
unindexed KEYBOARD LOCK. Every candidate is either ready/already prepared or has a
specific unresolved dependency. Select a finite validation sample for 13c from
other issues, based on issue range and observed RTF/media variety. This checkpoint
produces metadata and the batch input contract; article recovery starts in 13b.

Result (2026-09-20): the [processing inventory](docs/CD1-PROCESSING-INVENTORY.md)
reconciles 3,099 topics, 2,103 contexts, 1,080 index targets, 2,462 occurrences,
and all 5,497 current TOC entries. It produces **1,088 dated article candidates
across 72 months: six already prepared, 1,074 ready for runner validation, and
eight blocked on adjacent content ownership**. Nine dated candidates are unindexed.
All six February identities, topic spans, and reviewed TOC matches are retained.

Native interval and alias evidence associates all 31 context/header-offset
differences, including eleven dated bodies. Three substantial unaliased topics
and five possible introductions remain explicit ownership cases. They block only
the affected jobs. The queue retains 883 linked introduction candidates, 114 linked
auxiliary topics, three application-resource topics, ten navigation topics, and
993 formatting-only separators. Ready status does not establish complete article
boundaries; the runner must inspect inherited RTF state and related links.

A frozen **nine-candidate sample** spans 1988–1993 and includes unindexed/suffixed
references, extra fonts, long listings, varied media, an interior context offset,
and a supplement with no numeric page label. `make inventory-cd1-processing`
rebuilds the metadata; the versioned manifest and standalone reader validate the
queue after relocation. No new article bodies or images were prepared in 13a.

### 13b — Next: build the shared extraction and packaging pipeline

**Inputs:** the 13a queue, existing extraction/conversion/validation components,
the approved v1 schema, and February's reviewed preparation evidence.

**Deliverable:** one runner that accepts article, issue, or whole-CD scope and
executes topic association, RTF inventory, text recovery, semantic mapping, media
conversion, Markdown preview, and package assembly as separately recorded stages.
Use shared rules for supported patterns and small source-bound exception records
for reviewed article-specific decisions. Encoding policies must follow inspected
font/run evidence; the February articles already demonstrate differing code-font
requirements. Preserve source paragraphs, runs, formatting, code whitespace,
objects, and source spans even when semantic classification is uncertain.

Separate extraction status from semantic review and print verification. Represent
uncertain structure explicitly where v1 supports it; otherwise retain the full
private intermediate and record why packaging is blocked. Unsupported controls
or undecodable spans must never disappear or be marked successfully recovered.
Failed images remain deferred at their source positions, with diagnostics and
source references. A single article/media failure must not abort unrelated jobs.

Write private intermediate content and packages independently of originals.
Validate staged output before replacing a successful artifact. Record input,
configuration, tool/pipeline version, and output hashes so retries and resume can
reuse only compatible results. Reuse validated media derivatives and compose
issue packages from independently prepared articles, without a chain of combined
packages that requires rebuilding all earlier articles for each addition.

**Completion check:** the runner processes the February baseline through shared
stages, preserves its content and recorded exceptions, and produces validated
packages. Identity, byte/run coverage, source-text projection, media relationships,
and package hashes are checked. Recovery from interruption, stale-cache rejection,
and isolated failure handling work. Keep v1 unless a demonstrated representation
gap requires a separately documented contract change. No new per-article script
is needed for each ordinary job.

### 13c — Validate batch operation beyond February

**Inputs:** the shared runner, all six February regression articles, and a fixed
sample of 6–10 additional candidates from at least three other issues. Use the
13a inventory to include early and late CD1 coverage and varied text/code/media
structures. Record the sample and expected review concerns before running it.

**Deliverable:** a regression and sample report covering extraction fidelity,
semantic decisions, successful conversions, deferred cases, and package loading.
Compare February article content, blocks, links, and accepted assets with its
reviewed outputs; record any justified packaging/provenance differences explicitly.
For the new sample, verify article boundaries and source accounting against the
preserved CD data. Compare bitmap pixels and retain vector conversion diagnostics.
Test interruption/resume, deterministic rebuilds, and nested static base URLs.

**Completion check:** no unexplained February content regressions or silent source
loss; supported sample jobs validate and exceptions retain their source evidence.
Resume and per-job failure isolation pass. A source-specific exception can remain
deferred when containment works; a general preservation or runner defect must be
fixed before expansion. Record the finite sample's outcome and proceed to 13d
once these checks pass. Physical-magazine review is independent of this gate.

### 13d — Run the first complete CD1 pass and reconcile results

**Inputs:** the full 13a queue, the validated runner, sample results, and recorded
exceptions. **Start condition:** 13c's preservation and batch-operation checks pass.

**Deliverable:** process all remaining ready candidates, issue by issue, with
resumable checkpoints and a consolidated run report. Carry successful sample
outputs forward when their fingerprints still match. Continue after isolated
article/media failures, retaining diagnostics and retry targets. Publish no content;
write private article/issue packages and catalog data with explicit availability.

**Completion check:** no candidate remains silently unattempted. Every job is
prepared, prepared with review exceptions, blocked by identified source/identity
constraints, or failed with retained evidence. Report those counts separately;
failed and blocked jobs are not counted as extracted. Every native topic and
index occurrence still maps to an accounted source record. Reconcile prepared
articles, TOC links, unmatched TOC entries, unindexed content, missing media, and
unattributed topics in the final CD1 coverage report. Validate all successful
packages and preserve a reproducible manifest of the run and its exception queue.
This completes the first pass; resolving individual exceptions becomes subsequent
bounded work and does not erase their recorded first-pass outcomes.

## Checkpoint status

Steps 12b.1–3, 12c, 12d, and 13a are complete. **13b is the next implementation task**;
13b–13d are planned, not yet implemented or run. A “continue” advances the next
unfinished checkpoint. During 13d, issue boundaries are resume/reporting points
within the full-CD pass, rather than requiring a separate plan or permission for
every article. Subdivide engineering work when needed while preserving this
milestone and its completion checks.

Steps 7 and 11b remain independently deferred and do not block extraction. Missing
scans, physical review, image repair, ownership/access decisions, CD2/CD3, and the
reading-room UI remain separate scopes. Full text is prepared privately regardless
of later publication decisions.

| Step / checkpoint | Deliverable | Complete when |
| --- | --- | --- |
| 8 — Done: reading-room content contract | Versioned static-data schema, validator, synthetic example, and private pilot example. | The contract represents issue/TOC/article/media identities, mixed content, captions, missing data, and review status; the pilot validates without a UI or backend. |
| 9 — Done: one-article content package | Private pilot runtime files, previews, accepted assets, manifest, and separate provenance. | All content and media references resolve or carry explicit unavailable status; source links/hashes and deterministic rebuilds are checked. The reading room can consume the documented files without parsing RTF. |
| 10 — Done: second-article check | Recovered and packaged `8802114`, including a combined two-article v1 package. | Long listings and unnumbered headings preserve source structure. Font 15 uses an explicit ASCII policy; the schema remains unchanged. |
| 11a — Done: local source inventory | Checksummed original, exact ISO/extracted-tree comparison, and complete probe coverage. | Every observed source file is accounted for and the inventory reproduces; this alone does not establish backup readiness. |
| 11b — Deferred: recovery-source verification | Transfer the prepared set to independent storage, or verify the physical CD when a drive is available. | A real independent ISO restore or fresh physical-CD read verifies all disc files; preserved probe/repository evidence is recorded separately from extraction progress. |
| 12a — Done: one-issue coverage audit | Read-only February 1988 TOC/CD coverage and matching report. | Every TOC entry and discovered CD reference has an explicit metadata relationship and preparation status, with no guessed matches or new body extraction. |
| 12a.1 — Done: expanded TOC validation/import | Review and import the 1991–1993 additions with stable IDs and explicit historical snapshots. | Issue attribution is supported, imports validate, existing article provenance stays reproducible, and regression checks pass. |
| 12b.1 — Done: Gary Kildall interview | Standalone and three-article packages preserving 27 interview turns. | Topics 145/146 and all source runs/media are accounted for, packages validate under unchanged v1, and previous article outputs remain identical. |
| 12b.2 — Done: Turbo C editor | Standalone and four-article packages preserving code tabs, diagrams, and shared media. | Topics 160/161 and all 1,206 paragraphs are accounted for; both code blocks project exactly, five bitmap conversions preserve pixels, and unchanged v1 packages validate. |
| 12b.3 — Done: Turbo Pascal graphics | Reviewed title match, standalone and five-article packages, deferred vectors and text-review record. | Topics 157/158, Korean Pascal strings, mixed figure paragraphs, and all media positions are preserved under unchanged v1. |
| 12c — Done: February issue handoff | Current coverage record and validated issue package/catalog metadata. | All 39 TOC entries and five indexed targets reconcile; 48 runtime files and all review evidence are preserved, with deterministic and relocated/base-URL checks passing. |
| 12d — Done: February native closeout | Six-article handoff, including unindexed KEYBOARD LOCK, and complete native February metadata accounting. | All six observed bodies are prepared; 29 unmatched candidates and four sections remain explicit; earlier content and exceptions survive under unchanged v1. |
| 13a — Done: processing inventory | Complete source accounting and a batch input queue, including unindexed content. | All native/index populations reconcile; ready and unresolved jobs are explicit; February preparations remain linked. |
| 13b — Next: shared pipeline | Reusable extraction, structure, conversion, and packaging stages with resume and exception records. | February runs through shared stages with preservation checks, isolated failures, and compatible-cache reuse. |
| 13c — Planned: batch validation | Six-article regression baseline plus a fixed sample from other issues. | Fidelity, deterministic builds, resume, failure containment, and static loading pass; unresolved source cases remain visible. |
| 13d — Planned: complete CD1 pass | All remaining ready candidates processed; private packages and consolidated coverage/exception reports. | Every job has an outcome; failed/blocked cases retain evidence and successful packages validate. |

### Content contract requirements implemented in step 8

- Reuse existing TOC identities and native CD references. Model article/topic/TOC
  relationships explicitly, including unmatched sources and multi-topic articles.
- Include issue dates, ordered TOC entries, source-supported titles/authors/pages,
  and cover availability. Missing values remain missing; CD index coverage is not
  evidence of complete printed-issue coverage.
- Preserve ordered blocks, code whitespace, inline emphasis, captions, and
  mixed text/media sequences. Expose unresolved content and table-image fallbacks
  so the viewer does not need to reverse-engineer the Markdown preview.
- Give media stable identities, package-relative paths, formats/dimensions where
  known, and conversion/availability status. Resource references must work beneath
  a configurable static base URL without leaking local filesystem paths.
- Provide small issue/article catalog records for navigation and client-side
  search. Document the searchable fields; keep their generation separate from
  the viewer's search interaction. Do not invent related/recommended articles.
- Retain traceability to source topics/spans and preservation manifests, while
  keeping detailed extraction ledgers out of the viewer's required runtime data.
  Validate schema versions, ordering, identities, references, and output hashes.
  Record physical-magazine comparison status independently of extraction checks;
  legacy `viewer_compared` flags describe historical evidence, not a workflow gate.

This plan ends with validated CD1 content packages and an honest coverage report.
UI implementation follows the reading-room PRD; publication, access policy, and
later scans need their own scope when pursued. CD2/CD3 extraction follows the
separate disc plans linked above.

## Boundaries that remain in force

- ISO images, Windows files, extracted bodies, raw OCR, and full image resources
  remain private and outside Git/public-site assets. Keep tracked manifests and
  code separate from originals and generated content.
- Accuracy review and publication permission are separate. Covers, excerpts,
  and full articles need their own publication decisions; no automatic release
  follows from successful extraction or possession of a disc.
- Missing authors, pages, bodies, and covers remain missing. CD reformatted text
  is not a facsimile of the original magazine page.
- UI implementation, CD2/CD3 extraction, OCR for later scans, summaries, entity
  enrichment, timelines, and publication/access implementation are outside this
  CD1 content plan. They do not block private content preparation.

For existing implementation details, see [TOC import](docs/TOC-IMPORT.md),
[CD1 extraction](docs/CD1-EXTRACTION.md), and
[source inventory](docs/SOURCE-INVENTORY.md).
