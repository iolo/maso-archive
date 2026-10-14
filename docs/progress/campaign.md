# Campaign-wide PDF progress

[All issues](README.md) · [Current status](../../PROGRESS-PDF.md)

Catalog reconciliation, scope/tooling decisions, cost audits and earlier handoff
notes span issues and are kept here rather than assigned to a single month.
These are historical records; current policy and next issue are in the index.

## Checkpoint records

### Current handoff — 2026-10-14

August JSON/assets restoration is complete: 37 readable, assistant sample-reviewed
articles and six non-owning headings account for all 43 canonical TOC entries.
September 1984 is next and has not started. Human acceptance/full proofreading
remain pending. No reading-room rebuild is queued.

Start with [the short OCR handoff](../../PLAN-OCR.md) and
[successor notes](../SUCCESSOR-NOTES.md). The accepted policy is mapped Tesseract
by default, with opt-in Qwen assistance and explicit layout/coverage review.
[August progress](../ocr-august-progress.json) and
`build/pdf-restoration/13-1984-08-closeout/report.json` hold the completed outcome.

The detailed records below are historical evidence. Read a specific checkpoint
when needed; earlier engine recommendations, test counts and “next” statements
are not current operating instructions. OCR experiment narratives are indexed
in [history](../history/README.md).


### 2026-10-01 — 12-catalog-reconcile started

- Authorized prerequisite before February extraction: reconcile the owner's
  committed TOC corrections (`bccb3e0`), preserve stable identities and prior
  article evidence, and retain the completed cover/TOC image integration.
- Preserved the previous 5,497-entry TOC as a reproducible historical snapshot.
  An isolated import probe rejected 956 unresolved old identities without
  changing the current catalog. Reviewed spelling/byline/page corrections,
  category splits and combined entries through explicit identity decisions.
- Corrected import now has 122 issues, 5,299 entries and 4,170 provisional article
  candidates. November's 47 and February's 43 entries are unchanged. Reader
  dependency migration, PDF queue refresh and validation remain in progress.

### 2026-10-01 — 12-catalog-reconcile complete

- Imported the owner's corrected `TOC.md` without editing it: 122 issues,
  **5,299 entries and 4,170 provisional article candidates**. Explicit decisions
  preserve 5,032 IDs, allocate 267 new IDs and retire 465 IDs without reuse.
  Retirements record successors for merged entries; the two omitted entries
  without successors had no reader links. All prior reading links carry forward.
- Preserved the previous expanded catalog as a reproducible Git-backed snapshot.
  The reader requires pinned migration inputs and exact import replay before
  combining corrected metadata with historical CD1 packages. A real standalone
  CD1 rebuild reproduces all 26,827 content files; only its exporter provenance
  changes. Existing article identities, bodies and historical evidence stay intact.
- Refreshed the PDF queue at
  `private/pdf-restoration/inventory-2026-10-01/queue.jsonl`: **828 entries and
  686 provisional article candidates** across the same 19 eligible PDFs.
  Original PDF/evidence hashes validate; each completed November entry retains
  its original outcome. November's 47 and February's 43 catalog entries are
  unchanged. No new OCR, extraction or source-page mapping in this checkpoint.
- Exported `build/reading-room-catalog-reconciled/data`, then staged all 35
  November articles in `build/reading-room-pdf-reconciled`. The combined reader
  has **3,421 articles**, 3,413 texts, 3,237 listings and 10,177 media records.
  Final data manifest SHA-256:
  `e7f5d928ea5b37bfb0f5971a9993cd37c342097142bb132919f160839157e486`.
- Retained the completed cover/TOC work: 145 donated cover derivatives assigned
  to 149 groups, 239 TOC pages with 478 derivatives and 24 later image galleries.
  Cover priority remains donated → verified PDF → placeholder. Original scans
  stay private; historical TOC comparison findings are not silently reapproved.
- Preservation checks pass for all 3,386 CD article records, all 35 original
  November packages (4,915 content files plus 35 manifests), the step 11 ledger,
  and both contrasting sample packages. Separate staged outputs leave prior
  exports unchanged. Deferred manual bitmap corrections remain available in
  the original `corrections.json` records.
- Validation passed: 21 TOC/migration/snapshot tests, 59 PDF tests, 56 reader
  tests, 15 frontend tests, TypeScript and production build. The final combined
  export passes the complete file-hash and reader integrity checks.
- Desktop 1440×1000/mobile 390×844 browser checks pass for donated covers,
  lazy TOC loading, page selection, zoom, Escape/focus restoration, November
  section navigation, February metadata, corrected titles/search and CD1/2/3
  article routes. Actual 43,508-byte article and 3,512-byte listing downloads
  match originals. No mobile page overflow or console errors/warnings;
  screenshots inspected and test browser closed.
- Tracked checkpoint receipt: `data/catalog/toc-imports/2026-10-01.json`.
  Private audit and validation evidence:
  `private/pdf-restoration/12-catalog-reconcile/completion-audit.json`.
  Browser evidence: `output/playwright/pdf-catalog-reconcile`.
- Next is **12-1984-02-batch-01**: select and map the first bounded February
  batch using the refreshed queue. Use the reconciled reader baseline for later
  staging. Step 12 remains open; final aggregate installation remains step 13.

### 2026-10-01 — restoration cost audit requested

- Paused further restoration for a measured/estimated cost breakdown. See
  `docs/PDF-COST-AUDIT.md`; private aggregate evidence is under
  `private/pdf-restoration/cost-audit-2026-10-01`. No pipeline changes made for
  the audit. Current accounting assembly remains pending closeout:73 PDF tests,
  immutable rebuild,4,438 prior pins and desktop/mobile browser checks passed.
- Completed February sample:24 batches and four assemblies,10h34m elapsed
  including waits. Initial and revised render/OCR task execution totals20m36s.
  There were53 revised-region reruns plus five new regions, no task failures.
  Token accounting separates cached input, uncached input and output; finer
  activity attribution is explicitly approximate. Restoration has not resumed.

### 2026-10-02 — Completed-issue cost statistics

- Updated `docs/PDF-COST-AUDIT.md` using4,443 deduplicated response-usage records
  through February goal completion. Reproduced the previous audit's exact token
  totals and first24 batches' task-processing seconds. No new restoration,
  pipeline changes or browser work. February goal remains complete;March unstarted.
- November step11's observed window is57.81 calendar hours for35 delivered
  articles,with7,685,683 uncached input and1,375,890 output tokens plus313,575,808
  cached input. It excludes earlier setup and two reused pilot articles.
- February's complete observed window is25.44 calendar hours for37 articles:
  6,107,250 uncached input,1,313,296 output and230,869,632 cached input tokens.
  Average41.25 calendar minutes and200,555 uncached-plus-output tokens/article.
  Calendar spans include idle/approval waits;active labor is not measured.
- The earlier6,609,803-token/20h38m goal counter starts after batches01–03 and
  feature assembly. Documented its different scope and accounting;it must not
  be substituted for the full issue's input/output usage or monetary billing.
- All59 February checkpoint windows reconcile without overlap:46 restoration
  batches,ten assemblies,classification,reference and reader closeout. Direct
  article checkpoint mean25.03min,median15.60min;shared two-article batch splits
  are estimates. Full37-article CSV,issue-window CSV and detailed JSON are saved
  under `build/pdf-restoration/cost-audit-2026-10-02`,with private reproduction code.
- Rendering/OCR task ledgers total31m54s across1,706 initial and80 subsequent
  executions,excluding cache hits. These nested durations are not additive to
  checkpoint clocks. Linear20/150-issue illustrations explicitly retain February's
  workload and idle pattern;they are scenarios,not forecasts or active-hour bills.

### 2026-10-02 — Clarify PDF scope: JSON and extracted assets

- Revised PLAN-PDF.md to match the owner's explicit goal: structured article and
  issue JSON plus extracted images/assets, source/region evidence, immutable raw
  OCR, corrections.json and separate availability/review outcomes. PDF page
  rasterization and cropping for OCR/source review remain in scope.
- Removed HTML previews, reader adapters/integration, browser/Playwright checks,
  frontend tests/builds and reader installation from every future acceptance gate,
  including issue closeout and campaign completion. Steps 8–9 now validate the
  portable data contract; steps 13–14 reconcile and hand off JSON/assets.
- Preserved historical completion records and outputs. November and February
  remain complete; 17 eligible issues remain. Cover/TOC plans and owner catalog
  corrections remain authoritative; their existing presentation work is preserved.
  Updated the restoration guide to distinguish historical commands from current
  scope. Earlier notes about step 13 reader installation are superseded.
- Inspected existing tooling and recorded a bounded follow-up before March:
  remove HTML requirements from build/assembly validation and issue export,
  including dependent callers, while preserving package data and correction
  evidence. This revision does not implement that change or alter the pipeline.
- Validation: reviewed the revised scope and future gates; `git diff --check`
  passes. Documentation only; no OCR, package regeneration, browser work or test
  suite run. Next: the data-only tooling checkpoint, then March extraction.

### 2026-10-03 — Resume Tesseract restoration; complete data-only tooling

- Owner resumed the remaining issues with the validated Tesseract and semantic
  review pipeline. March 1984 remains the next issue; OCR experiments are outside
  this continuation. No engine, runtime, model or review-standard change.
- Article export/check and segment assembly now work without HTML; optional
  historical previews require explicit selection. Batch-reviewed export inherits
  the data-only behavior while retaining interruption, cache and retry rules.
- Issue closeout now delivers an issue JSON index, retained ledger/TOC,
  accounting, article packages, cover and a file/hash manifest. Its offline
  checker reconciles identity, ownership, review/availability counts and assets.
  No browser, reader staging or frontend build is part of acceptance.
- All 82 PDF tests pass, including renderer-free export/assembly/issue checks,
  interrupted batch resume and data tampering checks. A synthetic JSON-only
  issue rebuilds byte-identically. All 72 completed November/February packages
  pass read-only checks of their original manifests and retained files.
- Evidence: private/pdf-restoration/data-only-checkpoint/validation.json and
  sample-issue/issue.json. Existing packages and historical HTML remain intact.
  Updated PLAN-PDF.md and the restoration guide. Next: map and restore March's
  first bounded batch using Tesseract and source review.


[Back to progress index](README.md)
