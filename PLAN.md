# Step-by-step implementation plan

Revised 2026-09-18. This is the active work queue. The previous detailed plan is
retained in [Design reference](docs/DESIGN-REFERENCE.md); it is not a requirement
to build every proposed component now.

## Goal and first milestone

The eventual goal remains a searchable archive for **1983-11–1990-12: 86 issues**.
We do not yet have all its source material. The first milestone uses only what
we already have: **one complete article recovered from CD1, linked to its TOC
record, and checked against the original Windows viewer**.

Full-text extraction/preparation is required regardless of whether an article is
ever published. Keep the recovered text and provenance private and reusable.
Possible future access for paper-issue/CD owners is a separate product decision;
eligibility rules and ownership/access verification are unresolved. They do not
block extraction, and no access mechanism is selected in this checkpoint.

Proceed from **one article → one issue → the catalog**. Use what each step
teaches us to specify the next. Missing scans do not block the first milestone.
Do not estimate or automate collection-wide extraction until we understand the
one-article path. “Complete” here means complete against the CD article; it does
not claim fidelity to printed pages we have not inspected.

## Already completed

- [x] Inspect all three discs and record their ISO hashes and format findings.
- [x] Establish the scope: 50 issues from 1983–1987 start with TOC metadata;
  the owner will arrange scans later. The 36 issues from 1988–1990 are candidates
  for CD1 enrichment.
- [x] Run the CD1 viewer in the owner's DOSBox-X environment.
- [x] Prove direct CD1 extraction: raw RTF, image resources, and three indexes
  are preserved privately with a checksummed manifest. Fidelity is unverified.
- [x] Import all 86 issues and 3,811 TOC entries with persistent identities,
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
| 5b — Next | Full text for that one article | Both identified topics produce ordered private text with provenance; headings, code, and tables are preserved or explicitly marked unsupported. No neighboring article is silently merged. |
| 6 | That article's image map | Referenced images are traced to extracted files and linked to the right text location. Each is renderable or listed as unsupported; absence of images is a valid documented result. |
| 7 | Viewer comparison record | Title, printed page, article boundaries, text, and available illustrations are compared with `MVIEWER2.EXE`; discrepancies are resolved or documented, and the sample is marked verified only if it passes. |

Steps 1–5a are complete. Steps 5b–7 remain pending, even though the extraction probe
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
1988–1990**. A discrepancy must be explained rather than forced to match a count.

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

## Exact scope of the next task: step 5b

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

## Later checkpoints — detail them when reached

These retain the intended outcome without pretending that unknown extraction
work is already specified. Break each checkpoint into numbered tasks before
starting it; none is a single “next task.”

| Checkpoint | Small tasks to schedule | Evidence needed to advance |
| --- | --- | --- |
| A second article | Choose one case that exercises a different feature, such as code or an image; repeat the verified path and address one new failure at a time. | The method works beyond the first sample. |
| Preservation readiness | Generate a durable inventory for CD1; reuse it for CD2 and CD3 separately; record an actual backup location and verify a restore when backup storage is available. | Source files are accounted for; backups are verified rather than assumed. Existing hashes/private probe manifests support the pilot but do not complete this checkpoint. |
| One issue | Choose an issue with usable CD content; enumerate TOC/CD matches; review ambiguities; recover its available articles in small batches; produce a coverage report. | Every TOC entry has a known status, including absent or unsupported content. Complete these preservation tasks before bulk processing. |
| Local catalog | Render one issue's TOC; add article metadata navigation; add title/author search; then enable all 86 imported issues. | Useful browsing/search works with missing content honestly labeled. A database or new framework is added only if required. |
| Publication-ready build | Specify public fields and asset decisions; implement the allowlisted export; test exclusion and withdrawal; prepare a site build and contact/access information. | The exact public artifact is reviewable. Local build completion does not mean deployment or publication approval. |
| Restricted reading access, if pursued | Define eligibility and permission evidence; evaluate paper/CD ownership verification and delivery options against the reading-room design. | An explicit access policy and reviewed technical design; no ownership-verification mechanism is assumed or required for private text recovery. |
| Expansion | Review one additional issue at a time; measure failure/review effort before choosing a larger batch; add supplied 1983–1987 scans through a separate sample-first path. | Quality and source traceability survive a larger collection. |

## Boundaries that remain in force

- ISO images, Windows files, extracted bodies, raw OCR, and full image resources
  remain private and outside Git/public-site assets. Keep tracked manifests and
  code separate from originals and generated content.
- Accuracy review and publication permission are separate. Covers, excerpts,
  and full articles need their own publication decisions; no automatic release
  follows from successful extraction or possession of a disc.
- Missing authors, pages, bodies, and covers remain missing. CD reformatted text
  is not a facsimile of the original magazine page.
- CD2/CD3 bulk extraction, OCR for later scans, summaries, entity enrichment,
  timelines, and full-text publication stay deferred until a concrete checkpoint
  requires them. They do not block the first verified article.

For existing implementation details, see [TOC import](docs/TOC-IMPORT.md),
[CD1 extraction](docs/CD1-EXTRACTION.md), and
[source inventory](docs/SOURCE-INVENTORY.md).
