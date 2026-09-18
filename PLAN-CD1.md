# CD1 extraction and reading-room content plan

Revised 2026-09-18. This is the active work queue for extracting CD1 and organizing
its content for the reading room. The separate [reading-room PRD](PRD-reading-room.md)
owns the viewer's UI and application architecture. The previous broad archive
plan remains in [Design reference](docs/DESIGN-REFERENCE.md) as historical context.

## Goal and first milestone

This plan's goal is **reproducible CD1 content extraction and a static content
package that the reading room can consume**: issue/TOC metadata, article text and
semantic blocks, captions, converted media, source relationships, and explicit
coverage/review status. The first milestone remains **one complete article
recovered from CD1, linked to its TOC record, and checked against the original
Windows viewer**.

The archive target is **1983-11–1995-12: 146 monthly issues**, extended because
the owner holds the official CDs. The supplied TOC currently covers **86 issues
through 1990-12**; that source coverage is distinct from the expanded target.
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
one-article path. “Complete” here means complete against the CD article; it does
not claim fidelity to printed pages we have not inspected.

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
The exact versioned handoff schema is a later bounded step, informed by this pilot.

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
   the next unfinished step, unless the user explicitly requests a larger batch.
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

## First milestone: one verified article

| Step | Deliverable | Complete when |
| --- | --- | --- |
| 1 — Done | CD1 reference index | All three extracted `.lst` files are represented as structured records, retaining every occurrence, category path, title, source line, and original reference; counts and parse exceptions are reported. |
| 2 — Done | One explicit CD-to-TOC match | `8802065` is linked to `maso-1988-02-toc-0035` with both CD occurrences, title/issue evidence, and an explicitly conditional page comparison. |
| 3 — Done | Raw topic map for that article | Native context/hash evidence resolves `8802065` to body topic 149 and its linked introduction 148; byte locations and following boundaries are recorded, with completeness pending viewer review. |
| 4 — Done | One correctly decoded paragraph | The first body paragraph decodes strictly to 182 characters; byte provenance, font/encoding decisions, punctuation handling, and unsupported cases are recorded. |
| 5a — Done | RTF feature inventory for the mapped topics | All 149,579 bytes in introduction 148 and body 149 are accounted for; fonts, metadata groups, 21 object markers, and five HELPDECO literal-brace guards are located. |
| 5b — Done | Full text for that one article | Both mapped topics produce private ordered text and structured paragraphs/runs, with 21 object placeholders, all bytes accounted for, and the step 4 paragraph reproduced exactly. Image-contained text and viewer fidelity remain pending. |
| 5c — Done | Block identification for the pilot | 271 blocks cover all 323 paragraphs, 289 runs, and 21 objects; headings, examples, caption relationships, image-backed tables, and unresolved content retain evidence and source references. |
| 5d — Done | Private Markdown reading preview | Separate introduction/body previews represent all 271 blocks, preserving code whitespace, heading hierarchy, caption links, and ordered object placeholders, with source/output hashes and byte locations. |
| 6 — Next | That article's image map | Referenced images are traced to extracted files and linked to the right text location. Each is renderable or listed as unsupported; absence of images is a valid documented result. |
| 7 | Viewer comparison record | Title, printed page, article boundaries, text, and available illustrations are compared with `MVIEWER2.EXE`; discrepancies are resolved or documented, and the sample is marked verified only if it passes. |

Steps 1–5d are complete. Steps 6–7 remain pending, even though the extraction probe
already exposed some of their inputs. A decoded sample is not yet a verified article.
The milestone is complete only after step 7 passes; unsupported content that
prevents faithful recovery remains a blocker for that sample, not a hidden omission.

Selected pilot: **1988-02, “유닉스란 무엇인가?”, TOC page 65**, with CD reference
`8802065`. The [step 2 match](docs/CD1-MATCH-8802065.md) supports the metadata
relationship; the [step 3 topic map](docs/CD1-TOPIC-8802065.md) adds raw boundaries
and an explicit CD page-65 label. Content completeness remains unverified. If
the feature proves too complex for a first sample, document why and choose a simpler
article from step 1's inventory; do not force a one-topic-per-article assumption.

Step 7 uses the owner's working DOSBox-X setup. Automated viewer control has not
been established. If a direct comparison needs the owner's help, request a
specific comparison for this sample, not a new Windows installation. Keep the
step pending until the necessary evidence exists.

The owner can collect that evidence while development proceeds using the
[offline task checklist](docs/OFFLINE-TASKS.md). Viewer reference capture and
optional backup/scan preparation did not block index import and can continue
while topic mapping proceeds.

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
`python3 tools/verify_cd1_match.py`.

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
the original bytes. A successful decode is still pending viewer comparison in
step 7; do not mark the article complete. Keep image conversion and full-text
normalization outside this step, and log/commit the result before proceeding.

Result: `python3 -m tools.decode_cd1_paragraph` produces one private paragraph
and its raw-byte/provenance artifacts in `build/cd1-paragraph/8802065/`. The
sample is 182 characters and matches independent `iconv` CP949 decoding. The
RTF resets to default Arial without an explicit code page; CP949 is recorded as
a source-specific choice. See [the sample notes](docs/CD1-PARAGRAPH-8802065.md).
Viewer comparison remains pending. The limited sample does not exercise groups,
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
Image conversion and original-viewer comparison remain steps 6–7. Producing the
full text does not itself establish article completeness or display fidelity.

Result: `python3 -m tools.recover_cd1_text` writes separate introduction/body
text, structured paragraphs/runs with formatting/source spans, and provenance to
`build/cd1-text/8802065/`. All 268 text runs decode strictly; all 149,579 source
bytes are accounted for. The 4/319 introduction/body paragraphs retain blank lines,
and all 21 object placeholders stay in order. The step 4 sample matches exactly.
See [full-text recovery notes](docs/CD1-TEXT-8802065.md). Text inside image resources
is not transcribed, and viewer comparison/article completeness remain pending.

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
and reserve viewer-dependent decisions for review.

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
stable anchors. Layout, images, and viewer fidelity remain pending. See
[Markdown preview details](docs/CD1-MARKDOWN-8802065.md).

## Exact scope of the next task: step 6 — image map

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
The original viewer remains the fidelity reference for step 7. Its comparison
must cover semantic blocks, code boundaries, heading hierarchy, and caption/
figure/table relationships as well as text and images.

## Next checkpoints: organize and expand CD1 content

Step 6 remains the next implementation task, followed by step 7. The queue below
starts after the pilot comparison. Define exact inputs and checks when reached;
split issue/disc batches into smaller numbered tasks before starting them. A
single “continue” still means one bounded task.

| Step / checkpoint | Deliverable | Complete when |
| --- | --- | --- |
| 8 — Reading-room content contract | Define a versioned static-data schema using the pilot's metadata, blocks, and image map. | The contract represents issue/TOC/article/media identities, mixed content, captions, missing data, and review status; a sample validates without requiring a UI or backend. |
| 9 — One-article content package | Export the pilot and its issue/TOC context, reading blocks, Markdown preview, converted assets, and manifest into one private package. | All content and media references resolve or carry explicit unavailable status; source links/hashes and deterministic rebuilds are checked. The reading room can consume the documented files without parsing RTF. |
| 10 — Second-article check | Select a different structural case, repeat recovery, and export it through the same contract. | The new article preserves its source structure; unsupported cases are recorded and any schema change is explicit. Split new extraction problems into smaller tasks. |
| 11 — CD1 preservation readiness | Complete a durable CD1 source inventory; record a backup location and verify a restore when storage is available. | Source files are accounted for and backup/restore evidence exists before bulk processing. Existing probe hashes are retained but do not substitute for a verified backup. |
| 12 — One issue, in small tasks | First establish TOC/CD coverage; then recover a bounded article batch at a time; finally build the issue package and catalog/search records. | Every TOC entry and discovered CD article has an explicit match/availability/review status, with no guessed matches or silently omitted content. The static package validates end to end. |
| 13 — Remaining CD1 coverage, in small tasks | Repeat issue preparation and account for remaining native targets, linked topics, and media, including 1991–1993 content beyond the supplied TOC. | A CD1 coverage report distinguishes recovered, unsupported, missing, unmatched, and navigation-only content. Reproducible packages retain all known exceptions and review status; no unreviewed article is labeled verified. |

### Content contract requirements to carry into step 8

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
