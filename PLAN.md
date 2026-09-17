# Implementation plan

Status: proposed implementation, based on repository and source inspection on 2026-09-18.
CD1 feasibility update: the owner has run the viewer in DOSBox-X, and a direct
extraction probe recovered RTF, images, and indexes. See
[CD1 extraction findings](docs/CD1-EXTRACTION.md). The TOC importer now accounts
for all 86 issues and 3,811 entries, with persistent IDs, schema validation,
candidate records, and a local search preview; see [TOC import](docs/TOC-IMPORT.md).
Durable disc inventory manifests, CD1 normalization/reconciliation, review,
and public-site implementation remain pending.

## Working rule: progress log and commits

For every implementation step:

1. Record the date, work performed, validation results, remaining limitations,
   and next action in `PROGRESS.md`. Log failed or blocked attempts as well;
   distinguish experiments from completed milestones.
2. Commit the step's changes together with its progress entry after the relevant
   checks. Use a descriptive commit message and inspect the staged diff first.
3. Keep original media, extracted publisher content, VM files, and private
   outputs out of commits. Record their paths and checksums where appropriate.

These rules apply to subsequent work throughout this plan. Each progress entry
is included in the commit it describes; it need not contain its own commit hash.

## Objective and scope

Build a Korean-language discovery archive for 월간 《마이크로소프트웨어》,
covering **1983-11 through 1990-12: 86 monthly issues**. Readers should be able
to find articles by title, author, date, and technology; follow related articles
over time; and identify the source and where the original can be consulted.

The [shared project discussion](https://chatgpt.com/share/6aac01d5-ad38-83ee-927a-cebca96649d4)
establishes the preservation, provenance, review, and publication principles.
This plan adopts the current, narrower date range in place of that discussion's
1983–1993 proposal. Its requirements are recorded here so execution does not
depend on continued availability of the temporary sharing link.

Deliver two complementary results:

- A reproducible local pipeline that preserves sources and produces traceable,
  reviewable issue and article records.
- A public-facing catalog built only from explicitly selected metadata,
  reviewed summaries, and approved visual assets.

Keep ISO images, extracted article bodies, OCR output, original software, and
VM disks in local preservation storage. Cover images, excerpts, and complete
articles have separate publication decisions. The public build must not infer
permission from an issue's age, a percentage threshold, or possession of its CD.
These are project publication rules, not a new legal assessment.

## What the existing materials establish

See [source inspection](docs/SOURCE-INVENTORY.md) for measurements and evidence.

| Input | Observed | Implementation consequence |
| --- | --- | --- |
| `TOC.md` | All 86 issue headings; 3,811 nested list entries | Import the entire catalog immediately; entries include sections and subtopics, not just articles. |
| CD1 | `MASOCD.MVB` directly decompiled to RTF, image resources, and indexes; introductory text declares 1988–1993 | Prioritize RTF normalization and matching of 1988–1990 records. |
| CD2 | `DATA/MASO2.M12`; source/listing paths dated 1994 | Preserve and probe its format; content enrichment is outside the initial date range unless inspection reveals earlier material. |
| CD3 | `MASO3.M14`, `LIST.M14`; attachment directories for all months of 1995 | Same preservation priority; defer bulk enrichment. |

The observed CD dates are **coverage clues, not completeness guarantees**.
We have not yet established whether the CDs reproduce entire issues, selected
articles, or reformatted text without all printed pages. No source for full
1983–1987 content has been confirmed. The owner will arrange scans later:
these **50 issues initially receive TOC metadata only**, while the **36 issues
from 1988–1990** are candidates for CD1 enrichment. Missing bodies, covers, or
authors must remain explicitly missing.

## Architecture and repository boundaries

Use a small Python pipeline, versioned JSON/JSONL records with JSON Schema
validation, and a rebuildable SQLite database for local querying and review.
Canonical reviewed records and correction history are authoritative; SQLite
and search indexes are derived outputs. Start with generated HTML and a small
TypeScript search interface. A hosted API, accounts, or graph database are not
needed for this catalog's initial size.

Proposed layout (to be created during implementation):

```text
TOC.md                         supplied transcription, retained as a source
PLAN.md
docs/                          extraction findings and operating instructions
schemas/                       versioned record contracts
src/maso_archive/               inventory, import, extract, reconcile, export
tests/fixtures/                 minimal synthetic parser/extraction fixtures
data/manifests/                 disc hashes, file inventories, run manifests
data/identities/                persistent import identities and retired IDs
data/catalog/                   reviewed issues, entries, articles, entities
data/overrides/                 explicit corrections and source-match decisions
data/public/                    generated allowlisted publication payload
web/                           static catalog and browser search
private/                       ignored extracted text, images, OCR, VM outputs
build/                         ignored intermediate files and generated site
```

The supplied ISO images can stay at their existing root paths. Add ignore rules
for them and private/generated directories before staging implementation work.
Do not move, modify, or commit the images. Build the site from `data/public/`
and approved assets only; never serve the repository root. Private processing
and public-site generation must be separate commands.

Each processing run records source hashes, tool versions, parameters, schema
version, outputs, and failures. Use input hashes and stage versions for caching;
support resuming a failed issue without rebuilding the collection. Preserve
previous review decisions when a parser or extraction tool changes.

## Data contracts

| Record | Essential fields and behavior |
| --- | --- |
| Issue | Stable ID such as `maso-1983-11`, year/month, original issue label, publication facts when known, holdings, source coverage, review status. Do not invent a day of publication or page count. |
| TOC entry | Stable ID, issue, parent entry, sibling order, indentation, raw text, source line range, entry kind (`section`, `article`, `subtopic`, `unknown`), parsed title/byline/page candidates. Every bullet survives import. |
| Article | Stable ID linked to TOC entry where possible, title, original byline, contributor relationships, section path, nullable printed start/end pages, source matches, summary and review states. |
| Source / asset | Disc ID and SHA-256, ISO path, container member or topic ID, extracted-file hash, content type, encoding, extraction run, relation to issue/article. |
| Page / locator | Printed page label, scan sequence if applicable, container topic ID, asset ID, mapping confidence. A CD topic is not automatically a scanned page. |
| Entity / contributor | Display label, aliases, type, provenance, reviewed relationships; distinguish people from corporate bylines and translators/editors. |
| Review / correction | Target field or match, previous and proposed values, evidence locator, decision, reviewer, timestamp. |
| Publication decision | Target record/asset, permitted fields/use, status, basis or permission reference, review date; independent of extraction and accuracy status. |

Store original text alongside normalized search text. Nullable fields mean
unknown, not zero or an inferred value. Track extraction method and verification
separately: a manually transcribed TOC is not automatically verified against print.
Provide field-level evidence for disagreements between the TOC and CD.

Article IDs must survive title corrections and new discoveries. Allocate IDs on
first import and retain a source-to-ID mapping; line numbers locate evidence but
must not be the sole permanent identity. New imports reconcile against this map
and flag ambiguous changes instead of silently assigning different identities.

## Milestone 1 — Preservation inventory and TOC import

TOC import, validation, persistent identities, article candidates, and the local
search preview are implemented. Generated unreviewed outputs are in `build/toc/`,
separate from the future reviewed catalog. Full machine-readable disc inventories
and actual backup verification remain outstanding.

1. Record all three ISO sizes, SHA-256 hashes, volume metadata, and complete
   directory inventories. Keep acquisition/ownership notes separate from the
   automatically observed metadata. Record backup locations and verification
   dates when backups are actually made.
2. Implement a deterministic importer for `## YY.MM` headings and nested bullets.
   Preserve original ordering, parent relationships, raw spelling, and source
   locations. Parse a final `= number` as a page candidate and `/ byline` only
   where the syntax is unambiguous. Preserve ambiguous text for review.
3. Retain sections, feature bundles, page-less children, and editorial matter.
   Do not assign a parent's page to all children as a verified start page, or
   turn every leaf into an article automatically.
4. Produce issue JSON, TOC-entry JSONL, article candidates, and a validation
   report covering dates, duplicates, missing pages, parse uncertainty, and
   suspicious hierarchy. Preserve apparent transcription errors until reviewed.
5. Build a preliminary metadata search export for local inspection. This work
   does not depend on legacy Windows or full-text access.

**Acceptance:** 86 unique issues, no gaps or extras in the target date range,
all 3,811 input bullets accounted for, exact raw-text traceability, deterministic
reimports, and explicit uncertainty rather than silently dropped entries.
Tests should cover nested sections, multiple contributors, slash-containing
titles, absent pages, repeated titles, and non-monotonic printed page order.

## Milestone 2 — CD1 extraction feasibility and coverage

1. Work on extracted copies of the containers. Pin a tested revision of an
   existing decoder before considering a custom parser.
2. Evaluate HELPDECO against `MASOCD.MVB`: internal directory, topic/context
   tables, text, formatting, image resources, links, and embedded files. Its
   documentation supports many MVB titles and internal-directory inspection
   of `.M??` files; this is a candidate, not proof that these CDs fully decode.
   See the [tool documentation](https://github.com/pmachapman/helpdeco/blob/master/README)
   and [64-bit cleanup](https://github.com/joncampbell123/helpdeco).
3. Test a few representative records before a complete export. Preserve raw
   bytes, inspect character-set declarations, and compare CP949/EUC-KR decoding
   with the original viewer. Handle other legacy encodings only where observed.
   Report undecodable sequences instead of replacing them silently.
4. Build a coverage matrix per target issue: TOC available, CD article records,
   body text, illustrations, cover, original-page reproduction, attachments,
   extraction failures, and unmatched records. Distinguish absent content from
   not-yet-inspected content.
5. Treat keys such as `8802065` and `SOURCE/P8801112` as candidate year/month/page
   identifiers. Confirm the interpretation against titles and viewer output
   before using them as deterministic joins.
6. Run only small format probes on CD2/CD3. Preserve their complete inventories;
   defer decoding later years unless needed to understand the shared format.

Prefer native text and images. If decoding is incomplete, inspect the failing
record structure and use the original viewer as the reference. Try viewer
copy/export/printing next, if supported. Use lossless captures and OCR for
image-only material or otherwise inaccessible records, recording that fidelity
and completeness may differ from the original print issue.

**Acceptance:** a written per-format capability report and a reproducible sample
export with readable Korean, correct article identity, and traceable image
associations, compared against the original application when available. Report
unsupported features explicitly. Time-box the initial decoder investigation to
two focused working days before deciding between adapter work and viewer export.

## Milestone 3 — Reconciliation and three-issue pilot

Use **1983-11, 1988-03, and 1990-12** as provisional pilot issues. The first
tests the metadata-only path; the latter two test early and late in-scope CD1
material. Confirm availability and replace a CD-backed pilot if necessary.
Three fully enriched issues require sufficient primary-source content; add a
third source-backed issue when it becomes available rather than pretending the
1983 issue is complete.

Match within an issue using confirmed source IDs, printed page, title, and
byline. Fuzzy matches are proposals for review, especially for feature bundles,
repeated series titles, or shared start pages. Keep unmatched CD topics and
unmatched TOC entries. A CD may omit editorial material or divide one printed
article into several topics.

Do not derive definitive article end pages from the next TOC entry. Preserve
unknown ends and record tentative ranges separately. Do not fabricate page
images from reformatted CD text.

Create a local review interface or generated review report showing source text
or image next to proposed metadata and match decisions. Store corrections as
overrides, so rerunning extraction cannot erase them.

For records with actual body content, produce short original Korean summaries
and proposed technology/entity tags. Retain source locators and processing
versions for each draft. A title-only description is not an article summary.
Review every summary before publication. Historical annotations need their own
evidence and must be distinguishable from what the article itself says.

If OCR is needed, benchmark candidate tools on a manually checked sample of
Korean prose, columns, mixed English/Korean, and code. Report character errors,
reading-order failures, and heading/page accuracy before choosing a tool. If a
hosted OCR or language model is chosen, explicitly select which source material
will be sent and establish a per-issue cost budget before bulk processing.

**Acceptance:** complete accounting for each pilot's TOC entries; all published
titles, bylines, and printed pages checked against available evidence; reviewed
source matches and summaries; documented missing content; repeatable runs.

## Milestone 4 — Searchable catalog and publication boundary

Build the catalog after the import schema and pilot review path are stable.

- Browse by year and issue; show the original TOC hierarchy and availability.
- Search titles, contributors, sections, reviewed summaries, and entity aliases.
  Filter by year, platform/technology, and whether article content was reviewed.
- Link each result to its issue, printed page when known, source description,
  review state, and verified external holdings/access links.
- Provide chronological result ordering and related-article links; a dedicated
  graph visualization is unnecessary for the MVP.
- Show approved covers where available and a clear typographic fallback where
  absent. Publish an archive policy and a configured correction/contact route.

Use Unicode normalization and explicit reviewed aliases for names such as
`애플 II` / `Apple II`. At this scale, start with browser-side substring/token
search over the public fields; benchmark Korean partial-word queries and short
technical names such as `C`, `6502`, and `CP/M` before adding a search service.
Keep exact/fuzzy matching behavior explainable and preserve punctuation in
displayed source text.

Make the publication exporter an allowlist: private body text, OCR, internal
paths, VM files, and unapproved images never enter HTML, JSON, search indexes,
source maps, or copied assets. Accuracy review and publication permission are
separate conditions. Cover availability alone does not trigger publication.
An issue-wide level must not override a more restrictive asset decision.

**Acceptance:** all 86 issues are discoverable; representative Korean/English
queries return expected records; keyboard and mobile browsing work; unsupported
content is honestly labeled; a build test rejects private/unapproved fields and
assets. Rebuilding after a withdrawal must remove the asset and search entries
from the deployed artifact, not merely hide its navigation link.

## Milestone 5 — Enrichment and sustainable operation

Expand reviewed enrichment to 12 source-backed issues (provisionally 1988), then
the remainder of 1988–1990. All 86 issues stay in the catalog during expansion.
The owner will arrange scans for 1983–1987 later; do not block the metadata
catalog on them. Before scanning a batch, agree on a capture profile using a
small sample: complete page order, covers and inserts, readable small text/code,
no clipped margins, and lossless masters with checksums. Keep printed page
numbers separate from scan sequence, record missing/blank pages, and preserve
masters before deskewing or other OCR preparation. Reuse the same source,
review, and publication contracts for these later scans. A complete TOC catalog
and a completely enriched archive are different completion measures.

Add verified library links and current access information with check dates.
Track rights/permission research and any asset-specific publication decisions.
Provide documented correction, withdrawal, rebuild, backup, and restore steps.
Validate a restore using preserved originals, canonical records, and run logs.

Later options: additional years, reviewed historical essays, richer entity
relationships, and permitted full-text access. Defer user accounts, comments,
semantic/vector search, translations, and runnable historical software.

## Windows setup and handoff

**Available setup: the owner has installed and run CD1 in DOSBox-X.** The local
Windows directory is `hwin31/`, configured by `hwin31.cfg`. The content remains
on the mounted ISO; setup installs the viewer/runtime and creates a shortcut.
The extracted `masocd-1/` directory is sufficient for host-side decoding. The
[Windows 3.1 installation guide](https://dosbox-x.com/wiki/Guide%3AInstalling-Windows-3.1x)
documents the environment setup. The available viewer can now verify typography, topic boundaries,
figures, article coverage, and any export facilities in the original viewer.

For reproducible viewer validation:

1. Use Korean Windows and working Korean fonts; keep a clean disk copy before
   installing CD software. Record emulator version and configuration.
2. Mount `masocd-1.iso` as a read-only CD with a consistent drive letter and run
   its installer. Confirm the application opens and Korean text is readable.
3. Check the issue/year selection, one 1988 and one 1990 article, an illustration,
   and a linked source-code attachment. Record the displayed title/page and
   whether text copying, export, or printing is available.
4. Retain the configured disk image, configuration, and local reference captures
   in private storage. Use a dedicated output exchange directory; keep the
   repository and unrelated host files outside guest write access.

For CD2 and CD3, prepare separate software installations in Korean Windows 95
when format validation reaches them. DOSBox-X also has a
[Windows 95 installation guide](https://dosbox-x.com/wiki/Guide%3AInstalling-Windows-95).
Use separate disk copies/configurations to avoid runtime conflicts. A working
QEMU or VirtualBox environment is also acceptable; no conversion is required
solely to standardize the emulator. The applications need no network for this
inspection workflow.

The owner has completed the initial Windows installation and viewer launch.
Automated control of that running viewer has not been established. It can now
serve as a visual reference while host-side normalization and catalog work
proceed independently.

## First implementation sequence

1. Add storage exclusions, preservation manifests, schemas, and the TOC importer.
2. Complete import validation and produce the first source-coverage report.
3. Probe CD1 extraction and compare selected output with Korean Windows 3.1.
4. Complete pilot reconciliation and the review/export workflow.
5. Build the static searchable catalog, then enrich a reviewed 12-issue batch.

The principal unknown is source recovery and completeness, not web development.
Estimate the bulk extraction/review workload after the pilot measures decoder
success, OCR needs, ambiguous matches, and review time per article. Metadata
work and Windows preparation can proceed independently without changing scope.
