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
  has three immutable natives: packages/design-a for 178–183/PDF180–185,
  packages/design-b for 184–189/PDF186–191 and packages/design-c for 190–195/PDF192–197.
  The new 69-file native matches an independent rebuild exactly. Combined coverage
  is 18 pages, 105 regions, 67 blocks and 38 original images. The article remains
  partial; its complete assembly is pending.

  The opening 178/PDF180 and final Z80 listing END 204/PDF206 establish physical
  span 180–206; independent cryptography opens 205/PDF207. The prose closing mark
  on 188 precedes patch tables and listings through 204. Current folios 190–195
  and outgoing 196/PDF198 were individually inspected. Nine physical pages 198–206
  remain deferred. PDF199–201 remain uninspected, unclassified and folio-unknown;
  None means uninspected, not unpaginated. Known deferred folios are 196 on 198 and
  200–204 on 202–206. No global folio offset or unchecked classification was inferred.

  Batch35 inspected 12 whole views: 179/180/191–198/206/207. Six mapped pages,
  six outside-map lookups and one canonical task; six pairs reused and six newly
  rendered. All 24 original and six revised exact crops were viewed before 12
  successful code tasks. OEM1/PSM6, one thread, 3000-pixel long edge and eng remain
  pinned. One source correction pass; zero recognition failures, retries or post-OCR
  crop repairs. All scans, crops, raw drafts, readings and serializers are retained.
  The initial explanatory word “unpaginated” for listing frames was corrected to
  “uncaptioned” before OCR; actual observed folios were already recorded correctly.

  Design-c retains 648 physical rows, 642 nonblank rows and twelve separate code
  blocks with twelve original frames. Each column has 54 physical rows, including
  blank and semicolon-only rows. There are no BASIC line numbers or new EQU
  fields in this segment. Indexes retain 66 label definitions, 527 instruction fields,
  519 operand fields, 135 branch/call operand fields and 1,138 physical columns.
  The 88 directive rows/values, 27 quoted strings, 26 quoted keyword candidates,
  157 hex fields, 12 local offsets and 55 comment expressions/442 parts are opaque.
  All UTF-8, regional, review, physical and lexical ranges reverse-project exactly.

  Printed LIGHT, OUPUT, ADDRESE, COMAND, S01900/S01990, CALL/SCALL, FTOV/FSTPV,
  FOBJ/FORJ, CMDKW-1/KWTO-1 and minus-exclamation offsets remain source candidates.
  No opcode, byte, address, target, encoding, arithmetic or syntax reconstruction.
  The page 189 DISPLAY quote physically continues into page 190's semicolon comment;
  both physical rows remain separate, without quote completion or executable joining.
  Quoted semicolon/colon punctuation in DEFM is a localized candidate and is excluded
  from comment-start classification. Twelve glyph occurrences retain source-linked
  uncertainty. The twelve listing frames have no invented figure captions.

  Prior design-b remains unchanged: two tables/58 rows/157 cells, 39 patch rows/
  117 opaque address-OLD-NEW fields, 138 physical rows/four BASIC labels/20 EQU
  fields, six shared captions/11 frame links and three unknown decorative bands.
  Keep these bands and all design-a table/diagram/caption metadata during assembly.
  The prior partial directory/manifest still pins design-a; the segments array pins
  all three natives. Aggregated coverage is not a combined article body.

  All 33,834 prior files and 26 implementation pins remain unchanged. The new
  preservation inventory contains 34,187 files. Native geometry, source/runtime,
  crop/settings/timing, all source indexes, prior ledger pins and independent rebuild
  checks pass. The unchanged 203-test baseline is reused without rerun.
  A fresh metadata-only revision corrects the inherited previous-restored printed-folio list to 178–189, matching twelve verified native pages. Initial metadata and audit are retained; native export, OCR and source readings are unchanged.
  Contest 0022 and technical 0019 remain non-owning headings on unpaginated PDF179;
  canonical titles, identities and parents are unchanged.

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

  Next: batch36, physical PDF198–203. Known folios are 196 on 198 and 200–201 on
  202–203; PDF199–201 must be individually inspected before assigning any folio or
  classification. Reuse preceding 197, opening 180/divider 179/ending 206/next 207;
  inspect outgoing 204. Preserve 195's final JP RUN1 and 196's semicolon/PRSHA boundary,
  all original frames, literal directive/quote/expression fields and native metadata.
  Nine physical pages and full article assembly remain. Human acceptance, full
  proofreading, source bytes, execution and historical claims remain unverified.
  No reader rebuild.
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
