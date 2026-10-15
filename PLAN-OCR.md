# OCR handoff

Updated 2026-10-16. Read this before future PDF restoration. This is the current
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

- August 1984 JSON/assets restoration is complete: 43 canonical TOC entries,
  37 readable, assistant sample-reviewed articles and six non-owning headings.
  Human acceptance remains pending. September 1984 is in progress; twenty-eight
  articles are readable, assistant sample-reviewed packages, including its
  editorial, IBM-PC feature introduction, first six hobby games, first
  educational article, complete typing article, complete math article and
  complete Logo lesson, menu-selection technique article and Z80 machine-language
  lesson, Apple Fortran article, CP/M installment, graph-structure lesson and
  system-development article and the complete eight-page **의료보험수가계산**
  article and the full nineteen-page **PIA 시리즈 SAM** article. The **비지니스**
  divider is non-owning. Medical-calculator segments are at
  `build/pdf-restoration/14-batch-26/medical-segment-a-v2/` and
  `build/pdf-restoration/14-batch-27/medical-segment-b-v2/`; their readable
  assembly is `build/pdf-restoration/14-batch-27/medical-complete-v2/`.
  Printed line 1230 has source damage, explicitly marked in the listing.
  The unlisted radar, advertising and book-notice pages through printed 156
  are classified separately; printed 157 is the non-owning **테크니컬** divider.
  **PIA 시리즈 SAM** is assembled at
  `build/pdf-restoration/14-batch-31/pia-complete-v1/` as `readable` /
  `sample-reviewed`, covering printed 158–176/PDF 160–178. Its four partial
  source packages retain the prose, short BASIC examples, and 39 original
  SAM/RECITER hex-panel images. Those image crops were checked for complete
  source coverage; their byte rows are not accepted as transcribed code.
  The next article visibly opens on printed 177/PDF 179 although its canonical
  TOC label says 176. Its three-page map and regional OCR now pass source and
  crop-provenance checks under
  `private/pdf-restoration/14-1984-09/batch-32/basic-recovery/`. Its checked
  three-page readable package is
  `build/pdf-restoration/14-batch-32/basic-recovery-v1/`, with five indexed
  best-read code/data panels and original crops. **모니터를 이용한 작표 도구**
  covers printed 180–183/PDF 182–185. Its checked readable package is
  `build/pdf-restoration/14-batch-33/monitor-plotter-v2/`; source-reviewed
  prose and two short BASIC examples are text, while the long BASIC listing
  remains three original code-panel images with row transcription pending.
  **SPC-1000 기계어 입력과 세이브 방법** occupies printed 184–185/PDF
  186–187. Its checked readable package is
  `build/pdf-restoration/14-batch-34/spc-machine-entry-v1/`; source-read
  prose and commands are text, while both hexadecimal tables remain original
  images with byte-level review pending. The separate unlisted
  **SPC-1000과 조이스틱** article occupies printed 186–189/PDF 188–191.
  The next canonical **마이크로 컴퓨터 설계 강좌** entry spans printed
  190–218/PDF 192–220. Its first six pages are source-read and exported as
  `build/pdf-restoration/14-batch-35/microcomputer-design-segment-a-v2/`, a
  checked `partial` / `sample-reviewed` package with 31 regions and twelve
  original diagram crops. The second six-page segment is also checked at
  `build/pdf-restoration/14-batch-36/microcomputer-design-segment-b-v1/`,
  with 33 regions, source-read prose and thirteen original figure/table
  crops. The third segment is checked at
  `build/pdf-restoration/14-batch-37/microcomputer-design-segment-c-v2/`,
  with 22 regions, source-read assembler explanation and eleven original
  figure/table/illustration/listing panels. The fourth segment is checked at
  `build/pdf-restoration/14-batch-38/microcomputer-design-segment-d-v1/`:
  twelve ordered original listing columns across printed 208–213, with no
  accepted byte text. The final printed 214–218 listing segment is checked at
  `build/pdf-restoration/14-batch-39/microcomputer-design-segment-e-v1/`;
  all five are assembled as a checked `readable` / `sample-reviewed` chapter
  at `build/pdf-restoration/14-batch-39/microcomputer-design-complete-v1/`.
  The printed-219 publisher software-contest notice is classified separately.
  **공모 총평** on printed 220–221 is a checked readable package at
  `build/pdf-restoration/14-batch-40/contest-review-v1/`; its results table
  remains an original image. Continue **애플 한글** and later TOC entries before
  closing September issue accounting. The first **애플 한글** partial covers
  printed 222–224 at
  `build/pdf-restoration/14-batch-41/apple-hangul-segment-a-v1/`; the remaining
  hex-listing pages still need source-image packages and assembly.
- Issue index: `build/pdf-restoration/13-1984-08-reference/issue.json`.
  Report: `build/pdf-restoration/13-1984-08-closeout/report.json`.
  [August ledger](docs/ocr-august-progress.json) is the machine-readable record.
- Existing August assemblies use pinned private boundary/review-range adapters.
  Validation/rebuild instructions and pins are in
  `private/pdf-restoration/13-1984-08-closeout/reproduction.json`.
  Seven review-range links were fixed in separate metadata revisions; all original
  packages, source readings, raw OCR and images remain preserved.
- Follow [PLAN-PDF.md](PLAN-PDF.md) for restoration scope and issue gates.
  Deliver JSON/assets; rebuild the reading room only when explicitly requested.
  Do not rerun completed trials or closeouts to begin a later issue.

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
  [results JSON](docs/ocr-august-pilot-results.json).
- Raw accuracy/resources: [initial benchmark](docs/OCR-QWEN3-VL.md),
  [June report](docs/OCR-JUNE-DECISION.md), [July report](docs/OCR-JULY-DECISION.md).
  CER/WER, table-cell scores and final acceptance measure different things.
- [August production usage](docs/ocr-august-usage.json): preparation, correction,
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

Reuse the pinned Tesseract runtime (OEM1/PSM6, one thread; `eng` for code and
`kor+eng` for other text). Default rendering is 3000 pixels on the long edge;
record any explicit scale change. Reuse the verified local Qwen/llama.cpp/GGUF
configuration when opting in; [runtime details](docs/OCR-QWEN3-VL.md#run) remain
in the technical reference. Neither an engine search nor a model download is
part of an ordinary restoration checkpoint.

```sh
# Normal mapped Tesseract OCR; the plan and page must already be reviewed.
PYTHONPATH=.:src python3 -m tools.pdf_restore.ocr page \
  --package private/path/map.json --pdf-page 30 \
  --output private/path/new-ocr-page30 --mode regions

# Explicit Qwen assistance on reviewed maps; no automatic layout pass.
PYTHONPATH=.:src python3 -m tools.ocr_qwen.mapped \
  --request private/path/request.json --output private/path/new-qwen-ocr
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
