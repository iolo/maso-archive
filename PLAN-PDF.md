# Step-by-step PDF restoration plan

Revised 2026-09-30. Status: **in progress; steps 1–10, 11-batch-01–31, 11-orientation-repair, 11-submarine-assemble, 11-library-assemble, 11-editor-assemble, 11-graphic-assemble, 11-radar-assemble, 11-mailing-assemble and 11-unix-assemble complete. UNIX 1(연재) is readable/sample-reviewed across PDF172–178 / printed170–176 with eleven cartoons, one version table,27 reading blocks and45 prose review notes. Both original segments, two provisional readings and exact regional byte partitions remain preserved. November has twenty-five readable articles, no partial articles, three headings and19 unresolved eligibility decisions. Next: 11-batch-32 maps 마이티용 순서배열 프로그램 from PDF179. Step 11 remains active through all November entries and issue closeout. 잠수함's manual bitmap correction remains deferred. Ignore `tocs/` for now as requested**.

Restore only articles listed in [TOC.md](TOC.md), extract available covers, and
integrate the results into the existing reading room. Use local OCR and preserve
useful results with explicit gaps. Follow the bounded checkpoint approach in
[PLAN-CD1.md](PLAN-CD1.md), [PLAN-CD2.md](PLAN-CD2.md),
[PLAN-CD3.md](PLAN-CD3.md), and [PLAN-reading-room.md](PLAN-reading-room.md).

## Working rules

- Work step by step. After every numbered checkpoint and named batch, append a dated entry to
  [PROGRESS-PDF.md](PROGRESS-PDF.md) recording inputs, completed work, outputs,
  validation, unresolved issues, and the next step. Record partial or blocked
  outcomes honestly before moving on. Also record each issue closeout. Steps
  11 and 12 are campaign milestones, not single execution checkpoints.
- Each executable checkpoint has one goal, fixed inputs, a work limit, a saved
  artifact, and an acceptance check. Split a checkpoint before expanding its
  scope. Mapping proceeds with the current article/batch, not across the archive
  before the pilot. The stall rule below does not replace these work limits.
- A partial checkpoint preserves useful outputs and an explicit exception. It
  permits independent work to continue but does not satisfy a failed prerequisite
  for bulk processing. Record the next bounded repair task when a gate fails.
- Avoid excessive investigation. Investigate only what is needed to deliver the
  current checkpoint; keep localized uncertainties visible and defer unrelated
  recovery work.
- **If a task remains stalled across three consecutive context windows, stop
  work and notify the owner.** Carry the stall count and blocker through context
  handoffs rather than restarting the count. Report the task, what was tried,
  the blocker, preserved partial outputs, and what would allow progress. Do not
  silently continue investigating beyond this limit.
- Preserve source PDFs and existing CD references. Keep scans, OCR, restored
  text, images, and generated references in ignored private/build locations.
- Article extraction is limited to existing TOC entries. Ignore advertising
  and other unlisted material for now, including advertising regions on pages
  shared with eligible articles. Cover extraction is explicitly included.
- Use scans as evidence for corrections. Preserve raw OCR, CD transcription,
  and scan-supported corrections separately. Reproducibility does not establish
  transcription accuracy or complete printed-issue coverage.

## Inspected starting point

The supplied `maso-pdf/` directory contains **21 PDFs, 6,615 PDF pages, and
2,664,455,314 bytes (2.48 GiB)**.

| Group | Supplied issues | Work in this pass |
| --- | --- | --- |
| Before CD coverage | 1983-11; 1984-02, 03, 05–10, 12; 1985-02, 03, 10, 11 | TOC-listed articles and covers |
| CD1 overlap | 1988-01; 1991-08, 09; 1992-12; 1993-03 | TOC-listed articles, covers, and evidenced CD comparisons |
| CD3 overlap | 1995-03, 07 | Covers only; no entries exist in the current TOC |

Twenty PDFs have no extractable text. September 1991 has only a short garbled
annotation mentioning `397~398`; its significance is unverified. Sample pages
show multi-column Korean, English, code, diagrams, advertisements, and PDF
rotation metadata. March 1995 PDF page 20 appears nearly blank. These are
planning observations, not a completed page or article inventory. Filenames are
provisional issue labels until checked against visible source evidence.

The current structured TOC snapshot matches `TOC.md`. For the 19 supplied issues
with TOCs it contains **839 entries and 684 provisional article candidates**;
November 1983 contains **47 entries and 35 candidates**. These are sizing inputs,
not final extraction totals. Page-less leaves and parent/child classifications
still require review; do not restrict eligibility to the existing candidate list.

## Checkpoint quality and batch limits

Keep availability and verification separate. Availability is `readable`,
`partial`, `image-only`, `failed`, or `unresolved`; verification is `unreviewed`,
`sample-reviewed`, or `fully-reviewed`, with the reviewed regions and remaining
uncertainties recorded. A failed OCR attempt does not mean an article is missing.
Only record missing source pages or articles when inspection supports that claim.

For the pilot and contrasting samples, inspect every mapped region for reading
order, omissions, unwanted material, and figure/caption placement. Compare all
pilot reading text with the scan, retaining uncertain characters as marked gaps.
For each contrasting sample, compare at least one complete prose column and one
code/figure region where present, recording the exact reviewed regions. A
readable result must preserve coherent prose order and expose available code and
figures without silent omissions; code that has not been checked character by
character remains explicitly unverified. This is not a requirement to execute
historical code or to proofread the whole archive.

For old user-defined bitmap characters, the owner has authorized manual
post-production correction (2026-09-28). Preserve uncertain occurrences as
explicit markers linked to printed lines and pinned scan regions in
`corrections.json`; leave unknown character codes/counts unresolved. Do not let
glyph decoding block the bounded extraction pass or invent replacement bytes.
Track pending manual glyph corrections separately from deferred page coverage.
Complete page coverage can be readable with these visible uncertainties;
segmented coverage remains partial until assembly. Neither status certifies
character-perfect or executable code.

Before bulk work, prove useful results on the pilot and contrasting samples,
including Korean prose, code, illustrations, and later layouts. An image-only or
unresolved result is valid accounting but does not prove the workflow works for
that case. If a required case fails, save it and complete a bounded repair or
replacement sample before passing the bulk gate. Subsequent issue reports must
separate usable results from exceptions rather than equating accounting with
successful restoration.

The initial qualification ceilings were **3 articles and 12 distinct source
pages per batch**. Step 10 passed the bulk-readiness gate and selected lower
operating ceilings of **2 articles and 6 distinct source pages per batch**,
whichever is reached first, to keep manual mapping and review bounded. Apply
these ceilings to all subsequent named batches. Historical manual review times
were not recorded; step 10 measures replay time and preserves workload counts
without inventing a restoration throughput estimate. Time new mapping and
review work prospectively.
For a longer article, use numbered page/region segments within the page ceiling,
then close out the assembled article separately. Never mark a segment as a
complete article. Each batch names its TOC IDs, source pages or mapping targets,
lookup-page limit, and outputs before execution. Cap location research at 20
inspected pages outside known article regions per batch; preserve unresolved
locations when that limit is reached. Permit one targeted OCR retry per failed
region in the batch; additional recovery becomes a separate deferred task.

## 1. Record sources and a provisional TOC queue

**Goal:** establish exactly which sources and TOC identities this pass may use.
**Input and limit:** metadata for all 21 PDFs and the existing TOC snapshot;
no article-boundary investigation.

- Record hashes, sizes, page counts, dimensions, rotation, and text-layer
  availability. Pin the TOC and structured snapshot hashes; reuse existing IDs.
- Save all 839 relevant TOC entries with their hierarchy and provisional
  classifications. Preserve page-less and ambiguous entries for later review.
  Resolve article versus heading decisions during local mapping, separately
  from the historical snapshot.
- Record the two 1995 PDFs as cover-only. Flag any source/TOC identity conflict
  for visual verification rather than inventing an association.

**Artifact/check:** a source manifest and provisional queue reconcile to 21 PDFs,
6,615 PDF pages, and the pinned TOC counts. Every queue record has an existing
TOC identity; uncertain classification remains explicit.

## 2. Account for available covers

**Goal:** recover usable front covers without replacing owner-supplied images.
**Input and limit:** the source manifest; inspect at most the first and last five
pages of each PDF for cover evidence. Defer unresolved cover searches.

- Verify visible issue dates. Record conflicts without attaching a cover to an
  unverified issue identity.
- Extract an embedded image where practical, otherwise render it upright with
  correct proportions. Record source hash, page index, dimensions, and settings.
- Add missing covers using `covers/masoYYMM`; preserve existing covers and keep
  alternatives separately. Record damaged, missing, or uncertain outcomes.

**Artifact/check:** a 21-source cover ledger plus available images. Inspect each
new cover for orientation, proportions, and date evidence; verify existing cover
bytes remain unchanged. Later reader integration checks their presentation.

## 3. Map one pilot and define its restoration record

**Goal:** establish an evidenced article extent and a reusable record format.
**Input and limit:** November 1983's “숨겨진 미로,” listed at printed page 28;
its opening was observed at PDF page 30. Map only this article, within the batch
page/lookup limits; segment it if needed.

- Verify its opening, ending, and continuations. A next TOC entry is not proof
  of an ending. Use scanned contents only to clarify existing entries.
- Record PDF page indexes and printed numbers separately, with an explicit
  index convention. Store ordered regions, coordinate units/origin, rotation
  transforms, and source dimensions; allow shared pages and continuations.
- Exclude advertisements and unlisted material. Keep ambiguous boundaries
  unresolved; do not guess a fixed page offset.
- Define the minimal article package: stable scan-derived ID distinct from CD
  IDs and independent of OCR titles, issue/TOC links, source hashes, region map,
  raw OCR paths/settings, corrected blocks, figures, downloads, and independent
  availability/review states. Keep correction evidence separate from raw OCR.

**Artifact/check:** one evidenced pilot map and a documented package schema with
synthetic examples. Verify numbering, rotated coordinates, shared-page exclusion,
and noncontiguous ordering with focused fixtures. If the pilot cannot be mapped,
record the blocker and select one named replacement before OCR work.

## 4. Establish local OCR on one pilot page

**Goal:** produce repeatable local OCR with positional evidence.
**Input and limit:** one mapped pilot page/region and the step 3 schema; one
baseline engine and at most two processing configurations.

- Set up Korean/English Tesseract, absent during initial inspection, with pinned
  engine/model versions and reproducible setup instructions. If installation is
  blocked, save the setup result as its own checkpoint before further work.
- Compare page and column/region processing where the page contains only eligible
  content; otherwise mask or crop excluded material before OCR. Retain raw text,
  positions, and settings. Record preprocessing only on derivatives.

**Artifact/check:** one OCR evidence bundle and repeatable commands. Re-run the
chosen configuration and compare text/positions, excluding declared volatile
metadata. Record quality limits and processing time; do not start an engine search.

## 5. Deliver the complete pilot package

**Goal:** make one article readable and traceable to its scan.
**Input and limit:** the mapped pilot and selected OCR configuration; one article,
using separate segment checkpoints if its extent exceeds the page ceiling.

- Produce ordered prose, literal code, captions, and figure crops. Preserve code
  whitespace and uncertain characters; store scan-supported corrections apart
  from raw OCR. Apply the pilot review requirement above.
- Export a minimal standalone article preview with downloads, scan-region
  evidence, and visible availability/review states. Keep this renderer reusable
  for later issue references rather than building a second reader application.

**Artifact/check:** one reviewed article package and preview. Check complete
mapped-region coverage, advertisement exclusion, figure/download links, and
unchanged raw OCR. Rebuild the package to verify stable IDs and content. A
partial result is retained, but the useful-pilot gate must pass before scaling.

## 6. Validate contrasting articles in separate checkpoints

**Goal:** establish that the package and processing rules handle observed variety.
**Input and limit:** the pilot workflow; execute and log each checkpoint below
separately, within the batch ceilings. Name the sample IDs before starting.

- **6a — Early-format contrast:** select at most two November articles that
  supplement the pilot with prose, code, illustrations, and a nested TOC case.
  Resolve whether parent entries group children without duplicating bodies.
- **6b — January 1988:** process one eligible article, checking page numbering,
  column order, rotation where present, figures, and code.
- **6c — August 1991:** process one eligible article with the same checks. Record
  unsupported layout features explicitly rather than silently dropping them.

**Artifact/check for each:** a sample package, exact review evidence, and a short
feature/result matrix. Apply the contrasting-sample review requirement above.
Test missing pages, continuations, and shared-page exclusions synthetically when
real samples do not exercise them. Preserve successful samples for the bulk pass.

## 7. Demonstrate one evidenced CD comparison

**Goal:** prove that scan-supported corrections and CD transcription remain distinct.
**Input and limit:** one successful overlap sample from step 6 and its existing
CD reference; one article association and up to two mapped pages of comparison.

- Require evidence for the association; title similarity alone is insufficient.
- Preserve OCR, CD text, differences, and scan-supported corrections separately.
  Record reviewed version relationships without treating a sample comparison
  as verification of the complete CD article.

**Artifact/check:** one comparison record whose decisions lead back to the scan;
no raw OCR or CD bytes change. If no sampled association can be supported, record
an explicit deferred comparison and expose no relationship. This does not block
independent scan reading. Leave September 1991's annotation until relevant to a
selected article, and defer March 1995's interior blank page entirely unless it
becomes relevant to cover identification.

## 8. Export one article through the reading-room adapter

**Goal:** validate the restoration package against the reader's actual data needs.
**Input and limit:** the pilot package and current reader data; one scan-derived
article in a separate staged export, retaining the existing CD records.

- Extend the static contract to version 3 with source/region references and
  availability/verification states. Retain version 1/2 support and existing URLs.
- Attach the article to its canonical issue/TOC identities. Include figures,
  downloads, scan evidence, and only supported version relationships.
- Validate paths, hashes, identities, and links before replacing any reader data.

**Artifact/check:** one staged export and focused adapter/compatibility tests.
Re-export it deterministically; verify existing CD IDs, links, and download bytes
remain intact. Correct package omissions here before bulk restoration.

## 9. Read the pilot in the existing application

**Goal:** demonstrate the complete issue → TOC → article → scan-evidence flow.
**Input and limit:** step 8's staged export; the pilot plus synthetic partial,
image-only, and unavailable cases, with representative existing CD routes.

- Render restored text, figures, downloads, scan regions at readable resolution,
  and distinct review states. Load article/page assets on demand.
- Include the pilot's metadata in search and available extracted covers in the
  existing cover presentation. Preserve standalone PDF and CD reference links.

**Artifact/check:** a working staged reader verified on desktop and mobile.
Check literal code rendering, evidence/download links, missing states, cover
fallbacks, search, CD navigation, and nested hosting. Confirm unrelated article
bodies are not fetched. Record browser results before advancing to bulk work.

## 10. Prove bounded batch and resume behavior

**Goal:** make the bulk procedure safe to repeat and interrupt.
**Input and limit:** at most three already prepared sample articles within the
12-page ceiling; use synthetic failures where needed, without expanding the queue.

- Define cache keys from source hash, region map, engine/model versions, and
  processing configuration. Preserve reviewed corrections across OCR reruns.
- Demonstrate interruption/resume, one isolated failure, and invalidation after
  a mapping/configuration change. Unaffected results must not be reprocessed.
- Measure mapping, OCR, review effort, and output size. Confirm or lower the
  initial batch ceilings, and document exact prepare/resume/export/check commands.

**Artifact/check:** a tested batch runner, durable outcome ledger, documented
limits, and a bulk-readiness record. Advance only after steps 5–6 demonstrate
useful results and steps 8–9 demonstrate a working reader. Record step 7's
comparison result or explicit deferral. A gate failure becomes a bounded repair
checkpoint, not a reason to process more issues speculatively.

## 11. Complete November 1983 through named batches

**Goal:** deliver the first complete issue accounting and usable issue reference.
**Input:** November's 47 TOC entries, existing samples, and the validated workflow.
**Size:** campaign milestone; each `11-batch-NN` is an independent checkpoint
within step 10's limits, followed by a separate `11-closeout` checkpoint.

- Map each batch immediately before extraction. Resolve headings, parent/child
  ownership, and page-less entries locally; retain decisions with evidence.
- Reuse successful samples. Save packages, review coverage, failures, retries,
  and unresolved boundaries after every batch. Avoid duplicate article bodies.
- For disjoint reviewed segments, assemble without new OCR. Retain original
  packages/maps/settings unchanged, validate complete ordered page coverage,
  rebase correction scan paths and listing byte ranges, and explicitly resolve
  superseded scope notes. Complete coverage can be readable/sample-reviewed
  while scan-linked bitmap markers remain pending the owner's manual correction.
- At closeout, generate a standalone issue reference with TOC navigation,
  downloads, scan evidence, and visible states using the existing preview tooling.

**Artifact/check per batch:** saved packages and reconciled batch outcomes, with
region/order checks and recorded text-review coverage. **Issue closeout:** all
47 entries have a classification and every eligible article has an outcome;
no unlisted article is added. Report readable/partial/image-only/failed/unresolved
counts separately, plus unresolved eligibility decisions. Export and inspect the
issue in the staged reader before moving to remaining issues.

## 12. Process remaining issues through the same bounded procedure

**Goal:** extend the proven workflow to the remaining 18 TOC-covered PDFs.
**Input and size:** one issue at a time chronologically; named checkpoints such as
`12-1984-02-batch-01` and `12-1984-02-closeout`, using the established ceilings.

- Reuse completed samples; map only the current batch. Preserve evidence and
  continue past isolated failures within the retry limit.
- An unsupported format becomes a separate bounded sample/repair checkpoint;
  do not expand a processing batch into an open-ended pipeline redesign.
- Reconcile each issue, produce its standalone reference/report, and validate
  its staged reader export before starting the next issue.
- Keep advertisements, unlisted material, and 1995 article bodies outside the
  extraction queue. Keep unresolved classification and source-label conflicts
  visible rather than inflating restoration totals.

**Artifact/check per batch and issue:** the same outputs/checks as step 11, with
an issue progress entry. **Milestone check:** all 839 TOC entries are accounted
for, subject to any evidenced input correction recorded in step 1; each eligible
article has an outcome and the two 1995 sources remain cover-only. Report actual
usable coverage separately from complete queue accounting.

## 13. Reconcile and install the complete reader export

**Goal:** make all delivered PDF results available alongside the existing archive.
**Input and limit:** completed issue packages/reports, cover ledger, and existing
CD references; aggregation only, with no new restoration or UI features.

- Reconcile manifests, source hashes, identities, TOC membership, outcome totals,
  review coverage, covers, and links across the 19 eligible issues.
- Build and validate a complete staged export; preserve standalone references
  and existing URLs before replacing reader data through the established flow.
- Confirm no 1995 article records were added. Check available 1995 covers through
  existing presentation without inventing canonical TOC or CD issue associations.

**Artifact/check:** a validated full export and coverage report distinguishing
usable results, unresolved eligibility, and restoration gaps. Existing CD links
and download bytes remain intact; repeated exports reproduce content.

## 14. Complete regression checks and handoff

**Goal:** deliver a usable, documented pass with honest limits.
**Input and limit:** the full export and accumulated checkpoint evidence;
final regression and documentation, not a new recovery campaign.

- Run the focused pipeline/adapter/reader checks introduced in earlier steps.
  Use synthetic fixtures in ordinary tests and keep real scans/OCR outside Git.
- Check representative desktop/mobile reading, literal code, scan evidence,
  downloads, cover fallbacks, metadata search, CD navigation, and nested hosting.
- Document preparation, resume, export, validation commands, required private
  inputs, output locations, and known limits. Update README and successor notes.
- Record final TOC accounting, eligible articles, availability/review totals,
  gaps, extracted covers, validation, and deferred tasks in PROGRESS-PDF.md.

**Completion:** the pilot/sample quality gates passed; every eligible article has
an explicit outcome; unresolved eligibility is separately reported; all usable
results and available covers appear in the reading room. Report restoration
coverage rather than claiming every article was recovered. Full proofreading,
cloud OCR, advertising restoration, TOC expansion, full-text search, ownership
features, and public deployment remain deferred.
