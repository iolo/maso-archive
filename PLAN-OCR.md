# OCR handoff

Storage: [what to preserve and where new work belongs](docs/STORAGE.md). Historical paths remain available through compatibility links.

Updated 2026-10-20. Read this before future PDF restoration. This is the current
operating guide; experiment history is reference material, not a task queue.

## Accepted policy

**Mapped Tesseract is the default restoration pipeline.** Use Qwen as an opt-in
draft or second reading for difficult prose or code, with explicit layout and
coverage review. The owner accepted this policy on 2026-10-14. It supersedes the
June Qwen-first trial and July/August content-based starting assignments.

Use reviewed region maps with either engine. A content category alone does not
select Qwen. Automatic Qwen layout and local self-correction are optional
experiments, not production defaults. Ordinary restoration does not require
paired OCR or a new engine comparison.

## Current restoration state

- December 1984 is in progress: eleven readable articles, one partial perspective
  simulation article, two non-owning headings and 23 of 37 entries unresolved.
  Perspective has complete source coverage over131–149/PDF133–151 in four immutable
  base natives: packages/perspective-a, packages/perspective-b-r01,
  packages/perspective-c and packages/perspective-d. Their105 regions,68 blocks and
  28 original images remain unchanged. Full article assembly is still required.

  The opening134/PDF136 reflection-region repair is now verified at
  packages/perspective-reflection-revision. Its12-file native and independent rebuild
  match exactly. The old crop atx=.949 was retained byte-identically;the revised
  right edge x=.970 includes the printed closing parenthesis after−1. Both exact
  crops were inspected before one fresh kor+eng OEM1/PSM6/one-thread/3000-long-edge
  task. No recognition failure,retry orpost-OCR repair. All21 full/review pairs132–152
  were reused and inspected:one mapped page,20 outside-map lookups.

  One source-direct correction pass adds only that observed parenthesis to the
  active block text. All other candidate bytes remain identical. The three matrices,
  12 rows,48 cells,three display ranges,11 math glyphs and64 inline occurrences
  remain source-linked;the first matrix still has two negative diagonal entries.
  Source a,e,f is unchanged. No mathematical,arithmetic orsemantic repair. A separate
  restored-glyph index locates the newly recovered parenthesis exactly.

  The old opening package,crop,rawOCR,reading,indexes andincorrect missing-parenthesis
  claim remain immutable superseded evidence. The verified revision must replace
  only p134-right-middle's active region,block andoccurrence indexes during assembly,
  with old evidence retained. It adds no page,section orduplicate matrix counts.
  The ledger now records verified-native-awaiting-assembly-application,with pinned
  source_revision andnative_revisions. Do not append the repaired section asnewcontent.

  Earlier143–148 at perspective-c retains406 physical rows,378 numbered entries,
  49 DATA fields and65 target fields. Final149 at perspective-d retains53 rows,
  inserted4045/4105,absent4140,literal3840 NEX andfinal4290 END. Middle137–142 at
  perspective-b-r01 retains87 matrix cells,two ellipsis rows,43 flow labels,24 source
  references,15 variable definitions,64 DATA fields and27 output values. Active
  four-native totals include701 physical rows and601 numbered entries. Preserve all
  math,flow,prosejoin,DATA/output,physical/logical,quote/comment/numeric/symbol/target
  andcaption metadata. AppleSoft andGBASIC remain independent source versions.

  All29,330 prior files and23 implementation pins remain unchanged. The new
  preservation inventory has29,444 files. The unchanged193-test baseline frombatch24
  is reused without rerunning tests. No shared tooling orreader changes.
  CP/M remains complete at packages/cpm5-complete-r01,observed110–129 plusunpaginated
  upper PDF132 reference continuation;lower132 ad separate,no observed130. BASIC
  speed102–109 retains opening102–107 andending108–109. All selected checks use
  cpm_literal_assembly.check/installed(),which delegates graphic_literal_assembly.
  The CP/M adapter isnot generic forperspective math/source-revision indexes.

  Next:compatible full perspective assembly fromfour base natives plusverified
  region revision. Preserve all372 base files and12 revision files exactly;apply
  replacement once atoriginal reading order. Resolve known10.3 AppleSoft caption
  association for143–144 frames and10.4 GBASIC association for149,using pinned
  external source ranges. Preserve every native field/array/metadata andoriginal
  frame. Connect prose136→137,flow138→139 andlistings1690→1700/3770→3780 without
  flattening physical bytes. Implement/verify compatible assembly before promotion;
  independent full rebuild andissue accounting/preservation audit remain mandatory.
  Human acceptance,full proofreading,source bytes,execution andmathematics remain
  unverified. No reader rebuild.
  See the [December record](docs/progress/8412.md) and
  [ledger](metadata/catalog/pdf-restoration/1984-12-progress.json).
- October 1984 is complete under the canonical TOC JSON/assets scope: 35 readable,
  assistant sample-reviewed articles and six non-owning headings account for all 41
  entries, with no partial articles or unresolved eligibility. All 260 PDF pages are
  classified: 205 contain selected article bodies and 55 are other material, including
  18 pages of two unlisted features. The verified cover, selected packages and
  independent byte-identical issue rebuild pass; all 30,737 prior evidence files remain
  unchanged. The standalone index is `archive/pdf/1984-10/reference/issue.json`;
  the report is `archive/pdf/1984-10/evidence/issue-closeout/report.json`.
  Human acceptance/full proofreading, source bytes and execution remain unverified;
  news/classified body transcription and the batch 35 preflight timing exception remain
  explicit. No reading-room rebuild at restoration closeout. Ten supplied eligible
  issues remain after October, including December now in progress.
  Continue from the [October record](docs/progress/8410.md) and
  [versioned ledger](metadata/catalog/pdf-restoration/1984-10-progress.json).
  The owner subsequently requested the October volunteer reader build, now
  completed locally; see [the reader guide](docs/READING-ROOM.md).
- August 1984 is complete at `archive/pdf/1984-08/reference/issue.json`;
  its report is `archive/pdf/1984-08/evidence/13-1984-08-closeout/report.json` and its
  machine-readable [ledger](docs/ocr-experiments/ocr-august-progress.json) remains preserved.
- September 1984 is complete under the canonical-TOC JSON/assets scope: 37
  readable, assistant sample-reviewed articles and six non-owning headings.
  The [issue index](archive/pdf/1984-09/reference/issue.json),
  [closeout report](archive/pdf/1984-09/evidence/14-1984-09-closeout/report.json) and
  source-page ledger classify all 268 PDF pages. The information-radar body
  prose, many code panels and classifieds remain readable original images with
  volunteer transcription pending. The separate unlisted SPC-1000 joystick
  article is classified outside the canonical article set. October 1984 is also
  complete; December 1984 is next, with ten supplied eligible issues remaining.
- Existing August assemblies use pinned private boundary/review adapters.
  Instructions and pins are in
  `archive/pdf/1984-08/restoration/13-1984-08-closeout/reproduction.json`.
  Follow [PLAN-PDF.md](PLAN-PDF.md) for restoration scope. Deliver JSON/assets;
  rebuild the reading room only when explicitly requested.

## Source review and bounded assistance

Keep ordinary checkpoints within **two articles, six distinct source pages and
twenty outside-map lookup pages**, as defined in
[the PDF batch limits](PLAN-PDF.md#checkpoint-quality-and-batch-limits).
Segment longer articles and assemble their immutable outputs separately. Tool
ceilings of three articles/twelve pages do not expand the operating limits.

1. Verify the canonical identity, source hash, actual start/end and adjacent pages.
   Map only the current bounded checkpoint. Review crop coverage and reading order
   against full pages; printed page numbers are not a global PDF offset.
2. Run mapped Tesseract, reusing successful evidence on unchanged inputs. Record
   settings, source/crop hashes and stage provenance. If Qwen is warranted, record
   the reason and exact region scope before inference; use one bounded probe only
   when it can change that choice.
3. Check every eligible region and page coverage, including engine agreements.
   Preserve diagrams/screens as original images and review captions/labels and
   associations separately. Check code rows, table cells, identifiers, literals,
   physical wraps and continuation boundaries explicitly. Successful OCR can omit
   content; model agreement or plausible code does not establish fidelity.
4. Correct the selected draft once against scans. Preserve historical spelling,
   printed mistakes and uncertain glyphs. Do not repair a program using expected
   syntax, opcode semantics or execution. Keep source-linked uncertainty records;
   Unicode approximations do not certify original encoded bytes.
5. On failure, looping, truncation, lost rows or damaged reading order, retain the
   attempt and use a recorded bounded fallback or crop repair. Ordinary spacing
   differences alone do not justify switching engines. Ruled tables, aligned
   assembly columns and repetitive decorative/graphic bands need particular care
   with either engine; do not repeatedly retry an unchanged failing crop.
6. Export and validate source/asset pins, every text/review range within its named
   region, physical/logical listing indexes, complete ordered coverage and an
   independent rebuild. Repeated text must link to the correct source occurrence.
   Keep immutable natives and corrections when assembling segments.
7. Record availability and review separately. Assistant `sample-reviewed` is not
   human acceptance. Preserve original evidence and failed attempts, update the
   issue ledger, and commit a bounded checkpoint. Resolve issue accounting and
   closeout before moving to the next issue.

After an interruption, verify whether the original process is still running and
resume it by its live handle. A lock or state file alone is not proof of a live
worker. Reuse verified stages rather than restarting successful recognition.

## What the experiments established

| Evidence | Useful finding | Limit |
| --- | --- | --- |
| Three-page layout benchmark | Qwen improved sampled prose/BASIC recognition; automatic layout omitted a whole prose column on the diagram page | Diagnostic sample; not independent human gold or whole-issue accuracy |
| Mapped A/B/C workflow | Reviewed crops improve Qwen coverage; a local correction pass both improved and regressed readings | No demonstrated human-time saving; local self-correction is not mandatory |
| June and July sampled crops | Qwen often had lower raw CER; Tesseract was substantially faster at raw recognition | Selected, unblinded assistant references; different material does not isolate paid correction cost |
| August eight matched articles | No convincing general paid-cost advantage for either route; uncached/cached/output rates and recovery change the ranking | Reviewable drafts with different residual errors; human repair remains unpriced |

The operating decision balances useful source correction with sustainable work.
It is not a claim that Tesseract always has the lowest raw error rate or that
Qwen has no value. No further benchmark is queued. A future experiment needs a
specific unresolved decision and a bounded design; preserve the existing results.

## Metrics and accounting

- [August comparison report](docs/OCR-AUGUST-PILOT-RESULTS.md): paired correction
  tokens, runtime, observed source errors and price sensitivity. Full vectors:
  [results JSON](docs/ocr-experiments/ocr-august-pilot-results.json).
- Raw accuracy/resources: [initial benchmark](docs/OCR-QWEN3-VL.md),
  [June report](docs/OCR-JUNE-DECISION.md), [July report](docs/OCR-JULY-DECISION.md).
  CER/WER, table-cell scores and final acceptance measure different things.
- [August production usage](docs/ocr-experiments/ocr-august-usage.json): preparation, correction,
  export, evaluation/recovery and reporting windows, plus between-window usage.
  Local inference calls/retries/routes are in the August progress ledger.
- Separate paid uncached input, cached input and output. Reasoning is included in
  output; do not count it twice. Working input-price ratio is 1:0.1; output rate
  is unknown. Use `uncached + 0.1*cached + r*output` only with `r` explicit.
- Local CPU/GPU/runtime/model tokens have zero monetary weight by owner choice.
  Elapsed time includes tool waits, gaps and interruptions; it is not active
  human effort. Monetary cost and active human review time remain unmeasured.
  Goal-level token counters and response audits have different scopes; do not
  combine them or infer billing from either. Reused work is not charged again.

## Commands and references

Run from the repository root with `PYTHONPATH=.:src`. Use fresh destinations;
private inputs and existing runtime/model fingerprints are required.
Follow the [successive-issue workflow](docs/STORAGE.md#successive-restoration):
new batch/revision directories are retained immediately, including unsuccessful
attempts; do not derive new issue paths from the historical migration lookup.

Reuse the pinned Tesseract runtime (OEM1/PSM6, one thread; `eng` for code and
`kor+eng` for other text). Default rendering is 3000 pixels on the long edge;
record any explicit scale change. Reuse the verified local Qwen/llama.cpp/GGUF
configuration when opting in; [runtime details](docs/OCR-QWEN3-VL.md#run) remain
in the technical reference. Neither an engine search nor a model download is
part of an ordinary restoration checkpoint.

```sh
# Normal mapped Tesseract OCR; the plan and page must already be reviewed.
PYTHONPATH=.:src python3 -m tools.pdf_restore.ocr page \
  --package archive/pdf/YYYY-MM/restoration/batch-NN/map.json --pdf-page 30 \
  --output archive/pdf/YYYY-MM/restoration/batch-NN/new-ocr-page30 --mode regions

# Explicit Qwen assistance on reviewed maps; no automatic layout pass.
PYTHONPATH=.:src python3 -m tools.ocr_qwen.mapped \
  --request archive/pdf/YYYY-MM/restoration/batch-NN/request.json --output archive/pdf/YYYY-MM/restoration/batch-NN/new-qwen-ocr
# Add --resume only for unchanged inputs/settings/implementation.
```

The mapped-Qwen request schema and distinct resume/retry rules are in
[the workflow reference](docs/OCR-WORKFLOW.md#mapped-qwen-assistance).
[PDF tooling](docs/PDF-RESTORATION.md#current-data-only-commands) documents article,
assembly, batch and issue export/check commands. For code changes, use focused
checks such as `make test-pdf` and `make test-ocr-qwen3-vl`; documentation-only
cleanup does not require inference, a PDF rebuild or frontend tests.

## History and optional research

The [history index](docs/history/README.md) links frozen plan/checkpoint narratives.
Read a relevant record only when investigating a specific result, failure or
legacy artifact. Older “next” instructions and engine recommendations are not
current authorization. Human A/B/C review measurements remain pending; that is
an optional research follow-up, not an instruction to restart the experiment.

## Maintaining this handoff

Update the policy, current issue state and essential references here. Keep
per-region/per-checkpoint detail in the issue's machine-readable ledger and
private evidence. If a new experiment is requested, give it a bounded protocol
and a separate dated record linked from the history index. Keep the snapshots
frozen; do not grow this handoff back into a chronological experiment log.
