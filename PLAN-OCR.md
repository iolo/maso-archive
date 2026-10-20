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

- December 1984 is in progress: sixteen readable articles, one partial article,
  five non-owning headings and 15 of 37 entries unresolved. Design(6), canonical 0020,
  has five immutable natives: packages/design-a for 178–183, packages/design-b for
  184–189, packages/design-c for 190–195, packages/design-d for 196–201 and
  packages/design-e for 202–204/PDF204–206. The new 39-file closing native matches
  its independent rebuild exactly. Combined coverage is all 27 pages/PDF180–206,
  141 regions, 85 blocks and 56 original images. No source body pages remain deferred;
  the complete article assembly is pending, so canonical availability remains partial.

  The independently reviewed opening is 178/PDF180, final OTOP/END is on 204/PDF206,
  and independent cryptography opens 205/PDF207. All 27 physical article pages have
  individual whole-view evidence. No global folio offset was inferred. Batch37
  reinspected seven whole views: 179/180/203–207. Three mapped pages, four outside-map
  lookups, one canonical task; all seven full/review pairs reused with pinned identity.
  All twelve exact original crops were inspected before six successful English code
  OCR tasks. Margins were complete, including gutter beyond the LOAD1 comment frame;
  no crop repair. OEM1/PSM6, one thread and 3000-pixel long edge remain pinned.
  One source correction pass; zero failures, retries or post-OCR repairs.

  Design-e retains 325 physical rows/322 nonblank rows, six code blocks and six
  uncaptioned original frames. Five columns have 54 physical rows; the final column
  has 55. Indexes retain 61 labels, 61 opaque directive rows/values, 13 complete quoted
  message fields/fragments, 22 labeled storage fields, one ORG and two symbolic
  storage operands. The 18 port operands, five bit operands, 86 hex fields and 15 local
  offsets remain opaque. Quoted trailing spaces, RECORD STRAT, MESS6, INBUF+110 and
  OTOP are literal candidates without decoded bytes or arithmetic/alias reconstruction.

  The final END appears on a physical row beginning with a semicolon. That complete
  row is retained as a comment candidate and END has a separate source occurrence
  index; no executable directive was supplied. The LOAD1 comment visibly ends in the
  candidate MEMOF near the source frame edge. Its tail glyph/completeness remains
  unverified; the original includes gutter proving this is not an OCR crop omission.
  No MEMORY completion or missing-glyph count was inferred. The localized tail is
  pinned for possible manual review. Incoming 201 LD A,3FH to 202 CALL PUT and the
  independent next-article boundary remain explicit physical source associations.
  No opcode, byte, address, target, encoding, syntax or hardware repair.

  All preceding natives retain every table, diagram, shared caption, physical row,
  quote run, opaque field and unknown band. Design-b retains 39 patch rows/117 fields,
  138 physical rows/four BASIC labels/20 EQU fields, six captions/11 frame links and
  three unknown bands. Design-c and design-d retain their 648 rows each, complete
  quoted operands and source errors. The partial entry still primarily pins design-a;
  segments pins all five. Combined coverage is not a combined article body.

  All 34,538 prior files and 26 implementation pins remain unchanged. The new
  preservation inventory contains 34,733 files. Source/runtime, geometry, crop/settings/
  timing, exact UTF-8/review/physical/lexical/message/storage/END indexes, prior ledger
  pins and independent rebuild checks pass. The unchanged 203-test baseline is reused
  without rerun. All scans, raw drafts, crops, one-pass readings, recipes and review
  artifacts are retained. No failed attempt or OCR/correction rerun in this checkpoint.
  Contest 0022 and technical 0019 remain non-owning headings on unpaginated PDF179;
  canonical identities, titles and parents are unchanged.

  VisiCalc 172–175 remains complete at visicalc-limits:154 files, five menus/52 options/
  129 fields, three ROUND claims and one manual source word ⟦faint source word⟧ pending.
  Body/page coverage is complete; CALCULATE/CALCULATION and 351.6763/results351.68/352/350
  remain independent. Memory 166–171 at memory-efficiency retains 182 files/190 cells/
  15 blanks/99 byte fields/46 physical rows/45 entries, source 위해서/canonical 위하여,
  Rea Only Memory, 76 BE:6 and output 149/prose 191. Mathematics 152–154 remains at
  math-montecarlo-r01:104 files/output 3.136. Business unpaginated PDF167 retains
  source 비지니스/canonical 비즈니스. MSX 150–151 at msx-loader retains 147 physical rows/
  134 entries and 박재현/TOC박제현. Perspective 131–149 at perspective-complete-r01 retains
  all 384 natives, 134 repair, two captions, 143–148 listings and 87 middle matrix cells;
  keep perspective-a, perspective-b-r01, perspective-c, perspective-d. CP/M remains at
  cpm5-complete-r01,110–129 plus unpaginated upper PDF132; lower 132 ad excluded, no 130.
  BASIC speed102–109 retains opening 102–107/ending 108–109. Selected checks use
  perspective_literal_assembly.check/installed(), delegating cpm_literal_assembly and
  graphic_literal_assembly. Preserve all 26 implementation pins.

  Assembly tooling is now tested in tools.pdf_restore.design_literal_assembly using
  mode design-literal-v1. All 213 PDF tests pass, including ten focused regressions.
  The five-native probe preserves all 440 files, 279 segment/category occurrences,
  29,792 UTF-8 ranges and 1,759 physical listing rows. Source metadata, four BASIC
  labels, the leading-semicolon END row and MEMOF uncertainty remain exact. Preserve
  the three new implementation.json pins as well as the 26 prior pins. The initial
  parent-scan validation gap and two test fixture/assertion failures are retained;
  all were resolved before the passing probe/full suite. No OCR, source correction,
  readable assembly export or canonical availability promotion occurred in this phase.
  Use design_literal_assembly.check/installed() for the new and earlier formats.

  Next: design-assembly. Use the tested design-literal-v1 adapter to create the
  production recipe with explicit stage-note resolutions, then assemble observed
  178–204 from the exact five immutable inputs;
  retain all assets, native bytes, range projections, tables, opaque patch fields,
  prose/spatial/diagram/caption associations, physical listing groups, quoted runs,
  message/storage/ORG fields, MEMOF uncertainty and the leading-semicolon END row.
  No new mapped source pages or OCR are queued. Promote canonical 0020 only after
  the complete package and independent rebuild pass. Human acceptance, full proofreading,
  source bytes, execution and historical claims remain unverified. No reader rebuild.
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
