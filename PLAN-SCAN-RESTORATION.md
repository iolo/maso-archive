# Restore articles from the donated scans

Created 2026-11-14. This is the next campaign after [scan cleanup](PLAN-SCANS.md).
R00–R13 are complete; the active goal is to restore all November 1984 articles.
Track execution in
[PROGRESS-SCAN-RESTORATION.md](PROGRESS-SCAN-RESTORATION.md).

## Aim

Restore the cleaned scans as **reproducible, presentation-independent article and
issue packages in the project's own schema**. Preserve logical content order,
titles and identities, prose, code, table rows/cells, original figures, captions
and their associations, with source provenance, correction evidence and explicit
gaps or uncertainties. Searchable text and code downloads are derived outputs;
OCR is one stage of restoration. The web reading room is a sample presentation
of these packages, not the definition of a restored article.

Preserve source geometry as evidence while expressing article structure and
relationships independently of a particular page layout or reader. Rebuild the
selected JSON/assets package from pinned sources and reviewed inputs, without
fresh OCR or a reading-room build, and compare all output files exactly. This
establishes artifact reproducibility; source fidelity also requires the separate
coverage, structure, asset, range and review checks below.
Keep this a practical issue-by-issue job. A useful partial article with a clear
gap is better than getting stuck trying to reconstruct lost paper.

Use the existing [OCR policy](PLAN-OCR.md#accepted-policy),
[bounded review procedure](PLAN-OCR.md#source-review-and-bounded-assistance) and
[JSON/assets workflow](docs/PDF-RESTORATION.md#current-data-only-commands).
**`PLAN-OCR.md` is the shared operating guide for both PDF and JPEG sources.**
Use the same OCR pipeline already used under `PLAN-PDF.md`. This scan plan adds
source selection, image-input handling and issue scheduling; it does not replace
or fork the OCR procedure. Leave `PLAN-OCR.md` and `PLAN-PDF.md` unchanged and
available for future donated PDFs, including their existing PDF commands and
source/provenance conventions.
Keep the completed PDF and CD packages intact. The outstanding PDF collection
handoff remains separate; this plan adds a new source type and new issue coverage.

## Starting point

- `archive/scans/YYYY-MM/` contains 24 checked issue sets: 6,070 distinct JPEGs,
  6,066 proposed reading-order entries and four extras. The
  [cleanup progress](PROGRESS-SCANS.md) links every issue's findings.
- The [collection audit](metadata/catalog/scans/collection-audit.json) accounts
  for all 59 ZIPs and confirms source/master hashes. Cleanup reviewed contact
  sheets and selected larger views; it did not establish full printed pagination.
- The checked `archive/toc/current/` snapshot contains **1,119 canonical TOC
  identities and 919 provisional article candidates** for these 24 dates.
  These are planning counts, not 919 proven article bodies. Group headings,
  shared bodies, unlocated entries and other outcomes still need classification.
- **22 issue dates have no supplied PDF.** February and March 1984 already have
  completed PDF restoration passes; treat their JPEGs as supplementary sources,
  rather than automatically transcribing both issues again.

Keep `PLAN-SCANS.md` as the cleanup record and `PLAN-PDF.md` as the PDF campaign
record. This short plan owns the scan-specific work.

## 1. Connect JPEG sources to the existing pipeline

Reuse the existing OCR, mapping, correction, assembly and export machinery.
Some `tools/pdf_restore/` entry points currently assume a PDF path, PDF page
indices and PDF geometry. Connect the cleaned JPEGs at that input boundary,
replacing PDF rendering with image loading where needed. Direct JPEG integration
for mapped Tesseract and native article export passed R00. Structured JPEG
segment assembly passed R11 with complete Feature I and unchanged PDF behavior.
Whole-issue export remains to be integrated before its first JPEG use. Existing
PDF commands remain valid for PDF inputs.

Keep this input change small. Reuse the pinned OCR runtime, reviewed region maps,
recognition settings, evidence, correction and export procedures from
`PLAN-OCR.md`. Extend source records explicitly only where JPEG provenance or
geometry requires it, preserving existing PDF formats, checks and archived pins.
Do not require a PDF conversion or put invented PDF page numbers into image
records. Future PDF issues must still run through the existing PDF input path.

Each selected source view must identify:

| Field | Meaning |
| --- | --- |
| Source identity | Issue, relative JPEG path, SHA-256 and native pixel dimensions |
| Cleanup inputs | Pinned `manifest.json`, `review.json` and `page-list.csv` |
| Source filename number | The donated filename's number, when present |
| Reading order | Reviewed order, including explicit review overrides |
| Printed folio | Observed numeral or label; unset when unverified |
| View geometry | Original pixel bounds, orientation and any derived-view transform |
| Regions | Eligible text/code/table/figure regions, exclusions and reading sequence |

Use `page-list.csv` together with `review.json`; sorting filenames or using only
the extraction manifest loses July 1987's correction. New pagination or order
decisions belong in restoration overlays, leaving the hashed cleanup files intact.
A source path/hash is the stable anchor; a reading position is not a page identity.

Keep JPEG masters byte-preserved. Rotate, crop or deskew only derived views when
needed, recording the transform back to the original. Keep originals available
beside the processed view. Retain a foldout intact and map its panels explicitly;
one image can contain several printed pages. Do not force all issues into one
filename-to-folio offset or automatically split every wide image.

Check the JPEG input integration with a small upright page, a sideways view, an
intact foldout and the known July order correction. Check hash rejection, bounds,
coordinate round trips, duplicate order slots and source-to-crop correspondence.
These establish correct image input to the existing pipeline; they do not reopen
OCR engine qualification or start unrelated issues' article restoration. Run the
relevant existing PDF regression checks if shared code changes, including a PDF
input example, so both source paths remain usable.

## 2. Restore one straightforward pilot

Start with **November 1984**: 246 retained scans, four identified cover faces,
no internal filename gaps and no known gross ordering anomaly. It adds new
coverage without immediately taking on damaged-source puzzles. This is a pilot
choice, not a claim that every physical page is present.

Pin its current TOC identities and cleanup records. The first article candidate
is **편집자 노트**, `maso-1984-11-toc-0034`, with catalog page reference **17**.
Locate it visually and establish its actual extent and neighboring material
before mapping; the catalog reference does not establish `page-017.jpg` or its end.
If it exceeds the pilot bound or is unlocated, record that outcome and choose a
shorter located TOC article in the same issue.

Restore that one short prose article end to end: map, OCR, correct against the
scan, retain figures/captions where present, export JSON/assets and rebuild it
independently. Compare all pilot reading text and every mapped region with the
source. Then qualify a listing/table/figure example from the same issue in a
separate bounded checkpoint. Choose it after inspecting the actual layout;
candidate counts and TOC ordering alone do not establish its extent.

The scan-input pilot passes when the project's schema represents the article's
logical structure and relationships, source coverage is accounted for,
uncertainties remain explicit, assets and ranges point to the right occurrences,
and the complete JSON/assets package reproduces without fresh OCR or dependence
on a presentation build. Text readability alone does not pass this gate. This checks the new inputs
through the established workflow. It does not repeat the completed PDF OCR engine
experiments. A successful OCR command or an image-only exception alone does not
pass this gate.

## 3. Use the established bounded workflow

For each named batch, record its TOC IDs, selected sources, expected extent,
limits, outputs and next step before running OCR. Keep the existing limits:
**at most two articles and six distinct source-page views**, whichever comes
first, plus **at most twenty outside-scope lookup pages**. Count separately mapped
foldout panels as separate views and record the original image count as well.
Segment longer articles and assemble their preserved segments separately.

Use mapped, pinned **Tesseract** by default. Qwen remains opt-in assistance with
a recorded reason and region scope. Do not repeat an engine comparison for every
issue. Reuse successful OCR when input bytes, maps, settings and implementation
match. Preserve failed attempts; allow one targeted repair/retry per failed region
in a batch and defer further recovery as a named task.

Check reading order, omissions and figure associations against full pages, then
review the selected text against its regions. Pay special attention to Korean
columns, listing rows and wraps, identifiers, DATA/hex literals, table cells and
blanks, captions and cross-page joins. Preserve printed mistakes and uncertain
glyphs rather than repairing historical programs by expectation. Execution and
original encoded bytes require separate evidence.

Use canonical TOC identities, retaining received titles and observed source-title
differences separately. Classify headings and shared-body references without
duplicating article bodies. Restore eligible TOC-listed content and covers;
retain advertisements, forms and other unlisted scans in the source set without
automatically turning them into article transcriptions. Explicitly account for
TOC-listed indexes/notices rather than silently dropping them.

Availability (`readable`, `partial`, `image-only`, `failed`, `unresolved`) and
review status stay separate from reproduction results. `readable` is an existing
content-availability value, not the restoration objective or proof of a
reproducible package. Report completed schema-based packages and their rebuild
evidence as restoration progress, with availability, gaps and review level as
separate attributes. Assistant sample review is not human acceptance.
A failed OCR attempt is not a missing page; an unlocated article is not proof of
source absence. Record source-linked uncertainty and damage without inventing
replacement text or imagery.

## 4. Finish the pilot issue, then expand

Complete November 1984's issue accounting and checked export before starting
another issue's article restoration. Passing the pilot establishes the workflow;
it does not mean the whole pilot issue is already restored.

Next, do a small **supplementary-source check for March 1984**. Its existing
word-processor article is partial because printed **250–251** are absent from
the supplied PDF. Inspect whether those actual folios are present and legible in
the donated JPEGs. Matching filenames are insufficient. If usable, restore a new
source-linked supplement and assemble a new revision, preserving the original
PDF package and its historical missing-source outcome. Otherwise retain the gap.
February 1984 likewise needs targeted source comparison only where there is a
documented gap or improvement worth making.

Continue the remaining new issue dates chronologically from the
[cleanup index](PROGRESS-SCANS.md), skipping already completed scan work. Keep
these known cases in view:

| Case | Treatment |
| --- | --- |
| February 1984 and December 1985 wide scans | Inspect intact foldouts before interpreting filename gaps as missing pages |
| March 1984 | Keep uncertain late-page order explicit; bound any location research |
| June 1987 | Scans 191–192 exist despite the donor note; verify the needed content |
| July 1987 | Consume the corrected reading list; retain cut-out alternatives outside the primary sequence |
| January, March, April, August and December 1987 | Carry documented absent spans into affected article outcomes |
| December 1987 rear cover | Retain the visible torn corner; cosmetic reconstruction is separate work |

Do not reopen unrelated old PDF/CD articles merely because new scans exist.
Record source choices per article or segment, with explicit cross-source joins
when combining evidence. Keep canonical article IDs stable across source variants.

## Outputs and progress

Preserve the cleaned source files and their review records in place. Add work
alongside them, outside `pages/`, `covers/` and `extras/`:

```text
archive/scans/YYYY-MM/
  restoration/batch-NN/    maps, derived views, raw OCR, corrections, attempts
  packages/               checked immutable article and segment exports
  reference/              selected issue JSON/assets export
  evidence/               rebuild comparisons, accounting and handoff
metadata/catalog/scan-restoration/
                          small tracked queues, ledgers and result records
```

Use fresh package directories. Preserve source snapshots, runtime/implementation
pins, raw OCR and correction evidence; Git alone is not a backup of `archive/`.
Keep disposable rebuilds under `work/validation/` and reader outputs under `dist/`.
Reuse earlier validated checks when their inputs have not changed; there is no
need to rehash all 59 ZIPs or copy all previous restoration files in every batch.

Update the new restoration progress index at milestones, write short per-issue
batch records, and commit each completed bounded checkpoint and issue closeout.
Keep the cleanup progress as a completed source-preparation record. Time new work
prospectively and record real workload/retry counts without estimating historical
review time. If a task stalls across three consecutive context windows, preserve
the partial result and report the blocker, following the existing PDF work rule.

An issue closes when every canonical identity has an evidenced outcome, every
source image is accounted for as selected material/cover/insert/alternative/other
or an unresolved case, and ownership, continuity, assets, ranges and a fresh
selected-package rebuild check pass. Distinguish source images, mapped panels,
printed folios and eligible body pages in the totals. Include known gaps and a
reproduction/next-work handoff. After the queue is done, reconcile the collection.

HTML generation, reading-room integration, deployment, full human proofreading
and cosmetic page reconstruction are later tasks. This campaign delivers the
restored JSON/assets and faithful source evidence first.

## First executable checkpoints

| Checkpoint | Saved result | Acceptance |
| --- | --- | --- |
| R00 — scan input integration | Minimal JPEG input support, November input/TOC pins, focused checks | Same OCR pipeline accepts the scan views; existing PDF input and behavior remain compatible |
| R01 — short prose pilot | One located November article, raw OCR, corrections and checked package | Full pilot text/region review and independent identical rebuild |
| R02 — contrasting layout | Bounded November listing/table/figure sample and its evidence | Rows/cells/assets/continuations accounted for; any failed prerequisite repaired before scaling |
| R03 — Apple FORTRAN | Complete final installment, compiler/symbol/output fields and original plot | 231 identical native files, 355 indexed table cells, explicit source uncertainty |
| R04 — contest commentary | Complete two-page commentary, entrant table and recovery evidence | 45 identical files, 40 indexed cells, exact continuation joins and bounded OCR retry |
| R05 — Basic Techniques | Complete final installment, independent listings and history table | 118 identical files, six captioned contexts, 58 numbered entries and 21 history cells |
| R06 — source contents classification | Six non-owning headings and bounded feature probes | Fourteen identical files, six pixel-exact contexts, canonical relationships retained |
| R07 — Feature I opening segment | Actual 18–23; whole feature remains partial | 179 identical native files, three tables, four code contexts, four original figures; explicit continuation pending on 24–39 |
| R08 — Feature I middle segment b | Actual 24–29; whole feature remains partial | 170 identical native files, six code contexts, two binary examples, five original figures; pending sentence join onto 30 |
| R09 — Feature I middle segment c | Actual 30–35; whole feature remains partial | 147 identical native files, three code contexts, three tables, nineteen mathematical occurrences and six original figures; 36–39 and assembly pending |
| R10 — Feature I final segment d | Actual 36–39; whole feature remains partial | 145 identical native files, four monitor contexts, three byte tables and twelve original figures; all 22 source pages covered in separate segments, assembly pending |
| R11 — complete Feature I assembly | Actual 18–39; complete native article package | 650 identical files; typed source indexes, uncertainty and source links preserved; four original segments unchanged; 229 shared tests pass |
| R12 — Feature II opening segment | Actual 40–45; whole feature remains partial | 192 identical native files; two tables, three code contexts and three original diagrams with typed source relationships; listing continuation onto 46 explicit |
| R13 — Feature II middle segment b | Actual 46–51; whole feature remains partial | 152 identical native files; 185 numbered units, original screen and two flowcharts; GOODMUSIC final part and MINI ORGAN listing continuation retained |

Immediate next action: **R14**, restore Feature II actual 52–57 in at most six
mapped source views. MINI ORGAN listing 1 continues at 0116 on 52, including the
open TW character-definition group from 51. Inspect its transition into listing 2
on 55. The feature's located extent is 40–58; segments a/b now preserve 40–51.
Continue final 58 and whole-feature assembly afterward. Preserve one program
identity across listing/segment boundaries and all typed diagram references.
Preserve complete Feature I on 18–39 and its four original segments.
JPEG assembly is now integrated and checked; use the same source/structure and
fresh native rebuild gates for later long articles. Whole-issue export remains
to be checked before first use.
Then continue the remaining articles in bounded batches through issue closeout.
R01 delivered the editorial; R02 Bit
Pattern; R03 the complete four-page Apple FORTRAN installment with separate
compiler/output/symbol contexts and an original plotted figure; R04 the two-page
contest commentary and nine-entrant table; R05 the three-page final Basic
Techniques installment and its six code examples; R06 six source-backed group
classifications; R07 the opening six-page Feature I segment with typed table and
assembler fields, source-linked BASIC wraps and original figure labels; R08 the
next six-page segment with three independent assembler listings, annotated
monitor/carry examples and structured source diagrams; R09 the next six pages
with literal mathematical occurrences, colour/address tables, two complete
assembler listings, an independent BASIC example and observed dot grids. November remains
in progress. R10 preserves the final four pages, original monitor/table examples,
and source-linked dot-size/grid structure. One targeted text-crop repair added
optional region selection and disjoint evidence reuse to the shared PDF/JPEG
pipeline, with 225 regression tests and both shared plans unchanged.
R11 assembles complete Feature I with projected typed indexes, exact source
relationships and the 29/30 sentence join. All 650 native files reproduce;
229 shared tests pass. Whole-issue export remains to be checked before first use.
R12 restores Feature II's opening six pages with 156 header/data cell positions,
five spanning octave labels, 126 numbered code units, twelve mathematical
occurrences and three original diagrams. The flowchart records 35 observed nodes
and 45 connectors without execution-based repairs. All 192 native files reproduce
exactly; four local glyph uncertainties and the outgoing listing continuation
remain explicit. Shared implementation and both shared plans are unchanged.
R13 preserves the next six pages: GOODMUSIC's final 53 rows, its independent
timing excerpt, MINI ORGAN prose and three original figures, and the first 116
rows of its character-definition listing. Typed structures retain 1,279 source
fields, 322 data literals, ten label-delimited data groups and 168 figure labels.
The two flowcharts distinguish printed shapes, connector junctions and routine
expansions without execution claims. All 152 files reproduce; nine local glyph
uncertainties and the open program/data-group continuation remain explicit.
