# Restore articles from the donated scans

Created 2026-11-14. This is the next campaign after [scan cleanup](PLAN-SCANS.md).
Execution has not started. Track it in
[PROGRESS-SCAN-RESTORATION.md](PROGRESS-SCAN-RESTORATION.md).

## Aim

Turn the cleaned scans into readable article JSON, searchable text, code downloads
and original figures, with enough source evidence to revisit a correction.
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
has not been implemented or tested yet; existing PDF commands remain valid for
PDF inputs and are not yet ready-to-run scan commands.

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

The scan-input pilot passes when text order is usable, source coverage is accounted for,
uncertainties remain visible, assets and ranges point to the right occurrences,
and the saved package reproduces without fresh OCR. This checks the new inputs
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
review status stay separate. Assistant sample review is not human acceptance.
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

Immediate next action: **R00**, followed by locating the November editorial.
No scan OCR or restoration package has been produced under this plan yet.
