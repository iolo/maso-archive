# Sustainable OCR and correction workflow

Updated: 2026-10-09. Owner: the archive maintainer; implementation and experiments
assisted by Codex. This is a hobby project's sustainability experiment, not a
replacement mandate or an unattended restoration project.

## Objective

Reduce the maintainer's time, attention and paid-model token consumption per
accepted page while retaining the current useful semantic correction work.
Human review and correction remain mandatory. Small differences in raw OCR error
rate matter less than the total work required to reach an accepted artifact.
Qwen3-VL is one partial alternative among several to evaluate.

## Principles

- Keep raw scans, draft OCR, proposed corrections, uncertainties and human decisions
  separately, with stable page/region identifiers and input/model/prompt hashes.
- Never treat model agreement, confidence or a good CER as human acceptance.
  Review every eligible region and page-level coverage, including agreements.
- Use local compute for repeatable recognition and routine first-pass proposals;
  retain capable-model reasoning for difficult readings, context and structure.
- Put deterministic work in scripts: cropping, draft alignment, differences,
  coverage checks, review packet assembly, token accounting and package validation.
- Reuse valid cached work and recorded decisions. Resume interruptions without
  restarting completed regions; never silently replace prior evidence.
- Do not infer paid-token savings or human-time savings from OCR accuracy, output
  length or model speed. Unmeasured fields remain null.

## Baseline and candidate workflows

Use the same scans, reviewed region maps, acceptance criteria and final review
requirements for all arms. Existing references are for offline evaluation only;
no reviewed transcription may enter a candidate prompt.

| Arm | Draft preparation | Correction and acceptance |
|---|---|---|
| A | Existing Tesseract on reviewed crops | Current semantic correction plus human review |
| B | Qwen3-VL on the identical reviewed crops | Same semantic correction plus human review |
| C | Tesseract and independent Qwen readings; local Qwen proposes corrections from both drafts and the scan | Same semantic correction where needed, plus human review |

“Independent” here means the Qwen OCR call sees no Tesseract draft. The subsequent
correction model is the same Qwen model and is not an independent adjudicator.
Automatic Qwen layout remains an optional exploratory input; it is not required
for these arms. Reusing reviewed maps isolates recognition/correction value from
layout errors and preserves prior work.

## Measurements

Primary end-to-end measures, per accepted page and per arm:

- Human active review/correction seconds, number of review passes and unresolved
  readings; pause time excluded and measurement method recorded.
- Actual capable-model input/cached-input/output tokens and escalation count,
  when available from the runtime or supplied usage records.
- Final coverage and acceptance outcome under the same human review standard.

Preparation measures and diagnostic proxies:

- Local model tokens, elapsed time, CPU/RSS/GPU estimates, cache hits and failures.
- Disagreement regions/spans, exact versus whitespace-only differences, and
  residual edit distance to the existing reference. These are workload indicators,
  not measured human effort or capable-model token savings.
- Explicit omissions, invented text, unintended code/spelling normalization,
  unresolved glyphs and corrections that regress a previously correct reading.

Retain the prior three-page diagnostic set initially: Korean prose/inset, BASIC
with bitmap glyphs, and prose/figures. Its assistant-reviewed references are not an
independent human gold corpus. Later add fresh pages across issues and layouts;
separate prompt development pages from held-out evaluation. Counterbalance arm
review order and record reviewer familiarity. A single reviewer seeing the same
page repeatedly creates a learning effect; do not claim a controlled trial.

## Execution checkpoints

1. **Completed: initial OCR feasibility.** Local llama.cpp/GGUF pipeline and
   paired benchmark exist; see `docs/OCR-QWEN3-VL.md`. Qwen's recognition is
   promising; automatic layout has omissions. The old replacement-oriented
   conclusion does not answer this plan's sustainability objective.
2. **Completed: controlled local preparation.** Implement all three draft arms on
   reviewed crops; local first correction, reusable per-region checkpoints,
   source-linked differences and complete review packets. Run the three-page
   diagnostic set and compare remaining errors and resource/local-token costs.
3. **Ready for human review: actual review measurement.** Prepare explicit, initially unreviewed
   review records for A/B/C. The maintainer reviews complete page coverage and
   regions. Record actual capable-model usage when available. Do not mark this
   checkpoint complete using automated scoring or assistant review alone.
4. **Then: selective assistance.** Use disagreements and uncertainty to prioritize
   capable-model assistance, while retaining human coverage checks for every
   region. Compare full-context versus bounded evidence packets without losing
   source fidelity. Do not automatically accept unflagged regions.
5. **Then: broaden and choose partial adoption.** Evaluate held-out prose, code,
   tables, difficult scans and continuations. Adopt useful stages independently;
   keep engine selection reversible. Compare other local tools/models if warranted.

## Deliverables and completion criteria

- Reproducible CLI, tests and documentation; private raw artifacts and transcripts.
- Readable review packets with original page/crops and A/B/C drafts/differences.
- A machine-readable cost/quality report that separates measured local costs,
  diagnostic proxies and pending human/capable-model measurements.
- A review ledger requiring explicit human page coverage, per-region disposition,
  unresolved-reading records and human acceptance. No automatic archive promotion.
- An evidence-based recommendation after actual review: which stages to keep,
  route or drop. No arbitrary token-savings target before establishing a baseline.

## Current execution record

- Checkpoint 2 completed on the existing three private sample pages. The serial
  `private/ocr-qwen3-vl/workflow-03/` run contains 60 completed, verified stages,
  complete A/B/C packets and an explicitly pending human review ledger.
- Reviewed-crop Qwen drafts had compact CER .79% (prose), 0% (29 resolved BASIC
  lines only), and .57% (diagram-page prose). Local correction improved four
  regions but regressed three relative to existing references. Its full A+B+C
  preparation used 46,059 local tokens versus B's 17,138. These are not paid-model
  tokens, and no human-time or paid-token savings have yet been measured.
- An unchanged resume reused all 60 stages, computed zero new stages, and started
  no extra server. Per-run file locks now prevent overlapping resumed workers.
- [Workflow guide and results](docs/OCR-WORKFLOW.md) links the three review packets
  and ledger. [Sanitized measurements](docs/ocr-workflow-measurements.json) retain
  costs, reference diagnostics, regressions and pending review status.
- Checkpoint 3 requires actual human review and usage records. All nine page/arm
  records remain unaccepted; neither assistant scoring nor model agreement marks
  this checkpoint complete. No archive promotion.

## Authorized June 1984 issue trial

The maintainer authorized applying Qwen3-VL to the entire next issue, 1984.06,
with rollback available. Use **reviewed maps → Qwen raw OCR → assistant semantic
correction against scans → mandatory human review**. The three-arm experiment's
pending human measurements do not block this explicitly authorized practical trial.
Do not run the local Qwen correction arm by default. Tesseract remains available
for selected cross-checks and rollback using the same maps.

Process the issue in the existing bounded restoration checkpoints (up to three
articles and twelve source pages), preserving source-linked evidence, continuation
and queue accounting. Whole-issue scope does not mean unchecked automatic layout.
Keep drafts and corrections private, record progress after each checkpoint and
commit code/documentation. Do not count a partial opening as a complete article.

- Source: `maso-pdf/maso-8406.pdf`, 256 PDF pages, 44 canonical TOC entries.
- Private campaign: `private/pdf-restoration/12-1984-06-qwen/`, with queue and
  issue progress ledger. All human acceptance remains pending.
- First checkpoint: editorial19, feature overview20–21, technical child opening22.
  Initial crop inspection found an erroneous blank-margin crop and clipped glyphs
  on21; retain that run and use separately corrected maps/evidence.
- Completed checkpoint: `batch-01-corrected` has 23 raw text regions and one
  original figure, assistant source corrections and three validated exports.
  Editorial and overview have complete extents; the technical article is partial.
  All three exports rebuild byte-identically. Resume reused23 stages with no
  new inference/server. Human acceptance is pending for all three.
- [June checkpoint record](docs/ocr-june-progress.json) pins the private packages
  and records measured preparation resources, retained failed-map attempt costs
  and unmeasured human/paid-token fields. Next map technical continuation23–32
  in bounded checkpoints, preserving the opening22 package.
- Whole June issue remains in progress. Existing Tesseract evidence, prior issues,
  canonical TOC and reader publication are unchanged.

### Continuation checkpoint, 2026-10-09

- Completed native `batch-02` (23–27) and `batch-03` (28–32): 55 raw text
  regions and 19 original diagram crops, followed by assistant scan corrections.
- Assembled the full first technical child22–32 with the immutable opening22.
  It contains63 text regions,20 figures, and137 numbered Z80 rows plus `LIST`.
  Omitted prose, circled-letter readings and displaced code operands/comments
  were corrected from scans. Two sound-vowel readings remain human-review items.
- All55 stages verified; cache resumes made zero new calls. Two native exports
  and the assembly rebuild byte-identically;343 prior checkpoint files unchanged.
  Validation:119 PDF tests and25 OCR tests pass.
- Continuation inference:126.89s,44,367 prompt +9,807 output local tokens;
  sampled GPU peak7,862MiB and process-tree RSS peak6,037MiB. Rendering,
  startup and review are excluded. Human-time and paid-token savings unmeasured.
- Private review entry: `private/pdf-restoration/12-1984-06-qwen/REVIEW-SPEECH.md`.
  Complete export: `build/pdf-restoration/12-1984-06-qwen-speech-complete/`.
- Issue total:14 source pages,3 assistant-reviewed complete articles,0 partial,
  0 human-accepted. Next: inspect/map the second technical child beginning33,
  then continue the remaining June queue. Whole-issue completion is still pending.

### Further test checkpoint, 2026-10-09

- Restored second technical child opening33–38 in `batch-04-corrected`; full
  extent33–47 verified visually. Includes40 text regions,11 retained images,
  64 phoneme rows,11 timing rows and39 source-code rows. Continuation39–47 pending.
- Native table inspection caught a split through one row; retained the first
  40-call attempt and reran corrected maps. Both attempts are included in costs.
  Corrected preparation took89.95s including rendering/startup; inference69.03s,
  32,258local tokens, sampled peak GPU7,858MiB/RSS6,654MiB.
- Five identical-crop tests show cleaner Qwen drafts but faster Tesseract raw
  recognition (18.65s versus2.27s). Prose compact CER0.16%/14.08%, faint listing
  0.62%/42.68%; table cells311/312 versus260/312. Eight ambiguous cells excluded.
  Eng-only Tesseract table sensitivity gives265/312. References are assistant
  scan-corrected Qwen-derived readings, not blinded independent human gold.
- Export integrity,77 table-row ranges covering397 cells,39 listing rows, byte-identical rebuild,
  40 cache hits with no new inference, and682 unchanged prior files verified.
  No runtime code changes; existing144-test result is not a new test run.
- Review: `private/pdf-restoration/12-1984-06-qwen/REVIEW-PHONEME.md`.
  [Matched measurements](docs/ocr-june-batch04-comparison.json) record limits.
  Issue total20pages,3 complete/1 partial assistant-reviewed articles; all human
  acceptance pending. Next checkpoint39–44, then45–47 and full assembly.

### Continued evaluation checkpoint, 2026-10-09

- Restored39–44 in `batch-05`:23 text regions,8 original images,14 paired
  word-table rows and255 numbered main-program rows. Main listing numbering is
  separate from the sample on38. Remaining45–47 and full assembly are pending.
- Preflight repaired three listing crop boundaries before inference. One raw run:
  99.38s preparation,57.06s regional inference,29,727 local tokens, sampled peak
  GPU7,838MiB/RSS6,450MiB. No inference failures, truncation or reruns.
- Four preselected matched crops continue the diagnostic: code compact CER0.12%
  versus47.81%; prose1.86% versus11.80%. References are assistant source readings,
  not human gold; prose includes a provisional damaged-glyph reading. A separate
  code-row check preserves quoted spaces, which compact CER would ignore.
- Keep selected matched-crop evaluation through subsequent checkpoints. Report
  prose, code and tables separately; retain the existing model/prompt/Tesseract
  settings, fix sample selection and references before viewing Tesseract, and
  record source uncertainty. Do not infer human-time or paid-token savings.
- Native export rebuild is byte-identical;23 cache hits made zero new calls;
  1,722 prior files, including existing exports and human ledgers, are unchanged.
  No pipeline code changed, so the prior144-test result is not a new test run.
- Issue total26 pages,3 complete/1 partial assistant-reviewed articles,0 human
  accepted. [Measurements](docs/ocr-june-batch05-comparison.json) retain limits.

### Complete phoneme article and human-review preview, 2026-10-09

- Finished batch06 pages45–47:11 text regions,3 retained images,109 main-program
  rows and64 symbols. Corrected quoted literals, banner counts and $$$/Chinese
  confusion against the scan; retained source-cut strings and blank error fields.
  Three new candidate readings await human review.
- Raw preparation68.42s; regional inference40.16s;19,254 local tokens; sampled
  GPU7,940MiB/RSS4,720MiB. All11 stages reused on resume with zero new calls.
- Two preselected code crops: compact CER0.98% Qwen versus41.76% Tesseract;
  literal-sensitive row matches43/50 versus0/50. Raw recognition7.74s versus0.70s.
  [Measurements](docs/ocr-june-batch06-comparison.json) preserve source uncertainty
  and the unblinded assistant-reference limitation; downstream savings unmeasured.
- Assembled33–47:74 text regions,22 images,403 numbered rows in two distinct
  programs,156 native table rows including headers and19 unresolved entries.
  Native and assembled rebuilds are byte-identical; all source/projected listing
  and review ranges verified. Native table indexes and projected text are exact.
- Built the requested [reading-room preview](docs/READING-ROOM.md): whole article,
  side-by-side scan/correction, region navigation, zoom, raw OCR and review notes.
  Preserved previous reader provenance while staging this one complete June article.
  Validation:19 frontend tests,5 PDF-reader tests, production build, dataset
  integrity, desktop/mobile/dark-mode browser checks. This is a read-only preview.
- Issue total29 pages,4 assistant-reviewed complete articles,0 partial,0 human
  accepted. All96 phoneme regions remain pending. Review this article before
  continuing the next June TOC entries around51–52; keep selected evaluation.

### Remaining June issue authorized, 2026-10-09

- User requested restoration of all remaining June articles. Continue bounded,
  immediately inspected maps with Qwen raw OCR and assistant source correction;
  retain selected matched-crop evaluation, immutable evidence and mandatory human
  acceptance. Commit completed checkpoints. Refresh the private reader after
  groups of articles to avoid copying the existing collection for every native.
- Batch07 completes 시계공부52–56:22 text regions,6 original images,231 physical
  BASIC rows /194 numbered statements. Explicit order follows55-left opening,
  56-left,55-left ending,55-right and56-right; all original panels remain.
  Seven candidate readings remain. 취미생활51 is a non-owning section divider.
- Dense BASIC has more raw errors than the previous assembly sample: selected
  code compact CER2.85% Qwen versus33.23% Tesseract; prose0% versus4.10%.
  References remain unblinded assistant candidates, not human gold. No claim
  of whole-article accuracy or correction-time savings. Both samples fixed first.
- Preparation89.45s; regional inference70.66s;26,908 local tokens; sampled GPU
  7,836MiB/RSS5,882MiB.22 cached stages,zero new calls; native rebuild byte-identical,
  text/review/listing byte ranges checked. No runtime code or new unit-test claim.
- June now34 article source pages,5 complete articles,one classified group,0 human
  accepted. Next maze game57–59, then the remaining queue and whole-issue closeout.

### Maze game checkpoint, 2026-10-09

- Completed maze57–59:19 text regions,5 original images,191 physical rows and
  106 numbered BASIC statements. The3100 continuation across59 columns is linked;
  advertisement below59 is excluded. Five source candidates remain pending.
- Qwen preparation57.90s; inference43.60s;19,583 local tokens; sampled GPU7,822MiB /
  RSS4,572MiB.19 cached stages/zero calls. Selected prose compact CER0.69% versus
  6.90%; code0% versus41.63%. Quoted spacing and unscored source anomalies still
  need review; these assistant references are not independent human gold.
- Replaced the private export helper's numeric-prefix heuristic with explicit
  source line labels. Wrapped numeric operands are not new BASIC statements.
  Clock's corrected count is194 statements (not195); original exports retained,
  text/listing bytes unchanged, fresh indexed exports reproduce exactly. No OCR
  rerun. Use clock-study-indexed and maze-game-indexed packages going forward.
- June totals37 article source pages,6 complete articles,one non-owning heading,
  zero human accepted. Continue space animation60–63, then remaining June queue.

### Space and orchard checkpoints, 2026-10-09

- Batch09 completes 우주 유영60–63:26 text regions,9 original images,109 physical
  code rows/106 numbered statements in two separate listings. Restored a missing
  repeated E0 in1820 and four nonzero bytes replaced by zeros in1920; preserved
  source defects in the short example and marked six candidate readings.
- Preparation75.62s; inference57.13s;24,014 local tokens; sampled GPU7,820MiB /
  RSS5,263MiB. Selected DATA compact CER0.45% versus23.48% Tesseract.26 cached
  stages/zero calls. Original diagrams retain their embedded cell labels as images.
- Batch10 completes 과수원64–65:10 text regions,3 original images,69 physical
  rows/59 statements. Restored a missing520 tail and all530 even though Qwen
  returned a normal stop; corrected hex zero/O readings and physical wraps.
  Three source candidates remain, including quoted spaces and a color glyph.
- Preparation37.11s; inference25.17s;12,369 local tokens; sampled GPU7,822MiB /
  RSS3,428MiB. Fixed PATTERN/ending sample compact CER7.94% versus34.71%; omissions
  are included in this score.10 cached stages/zero calls. Normal completion is
  not evidence of complete transcription; printed line labels are checked directly.
- Both native exports reproduce byte-for-byte; integrity, text/review UTF-8 ranges,
  listing byte coverage and all36 raw stop reasons checked. Comparisons remain
  unblinded assistant-reference diagnostics, not independent human gold.
- June totals43 article source pages,8 complete articles,one non-owning heading,
  zero human accepted. Continue SPC-1000 automatic tape66–69 and remaining queue.

### SPC tape article and grouped reader, 2026-10-09

- Batch11 completes SPC-1000 자동실행 테이프66–69:47 text regions,8 original
  figures,30 physical code rows/22 numbered statements across five separate
  examples. Joined four cross-column/page prose continuations and restored source
  punctuation. Five address-table pairs checked; custom character chart retained
  as an image. Four original address/glyph candidates remain unresolved.
- Preparation78.45s; inference59.62s;30,793 local tokens; sampled GPU7,826MiB /
  RSS6,301MiB. Selected prose compact CER0.61% versus3.67%; reference fixed before
  Tesseract, assistant-derived and unblinded.47 cached stages/zero calls. Native
  export/rebuild identical; all text/review/listing ranges and raw stages checked.
- Expanded reader now includes the eight complete articles through orchard,
  preserving all previous146 scan articles and CDs. One grouped independent copy
  avoids seven collection copies; complete inventory/projection checks passed.
  Production build and desktop source/correction browser checks passed; no UI code
  changed. See docs/READING-ROOM.md for port4187 and source-review links. SPC awaits
  next grouped refresh; human acceptance remains pending for every June article.
- June totals47 article source pages,9 complete articles,one non-owning heading.
  Continue Apple automatic tape70–75, then all remaining eligible June articles.

### Apple tape checkpoint, 2026-10-09

- Batch12 completes 자동실행 베이직 프로그램 제작법70–75:68 text regions,
  13 original images,71 physical code rows. Three BASIC statements are indexed as
  numbered lines; disassembly addresses, monitor prompts and hex rows are separate
  unnumbered source rows. Flowchart text follows source steps; original geometry
  remains available. Eight source/glyph candidates remain pending human review.
- All57 program bytes match independently between the printed64-byte memory dump
  and28-instruction disassembly. Seven trailing zero bytes retained. Printed0307
  operand$E0 contradicts byteB0; preserved rather than regenerated. Other printed
  address, length and BSAVE discrepancies also remain explicit review items.
- Preparation109.67s; inference84.68s;43,749 local tokens; sampled GPU7,844MiB /
  RSS8,223MiB. Fixed hex-dump sample compact CER0% versus55.95% Tesseract against
  assistant reference. This is one selected crop, not an execution/accuracy claim.
  RSS was higher over this68-call batch; bounded process lifetimes remain useful.
-68 cached stages/zero calls; native export and rebuild byte-identical, all source
  ranges checked. Enlarged recheck preserved source typo 베이지 rather than an
  inferred correction. Promote apple-auto-tape-source-checked; first export retained.
- June totals53 article source pages,10 complete articles,one non-owning heading,
  zero human accepted. Reader currently covers the first eight; continue numbers
  game76–78 with distinct Korean/English listings, then the rest of the issue.

### Bilingual numbers game checkpoint, 2026-10-09

- Batch13 completes 숫자 따오기76–78:19 text regions,6 original images,
  301 physical code rows/176 numbered statements across separate Korean and
  English BASIC listings. Restored omitted banner strings and numbered English
  statements1010/1020 and3002/3005 that raw OCR merged. Korean3021 spans columns;
  prompt rows stay unnumbered. Printed variable inconsistencies remain unchanged.
- Preparation67.66s; inference52.26s;20,706 local tokens; sampled GPU7,824MiB /
  RSS4,758MiB. Fixed Korean ending compact CER2.08% versus36.98% Tesseract
  kor+eng; English ending1.64% versus16.78% Tesseract eng. Both use identical
  crop inputs and assistant references fixed before comparison, not human gold.
- Eight unresolved glyph/spacing/source-code notes; mandatory human review and
  execution remain pending.19 cache hits/zero calls; export and rebuild identical,
  source/text/review/listing ranges and all raw stop reasons checked.
- June totals56 article source pages,11 complete articles,one non-owning heading,
  zero human accepted. Continue car race79–83 and remaining eligible articles.

### Car race checkpoint, 2026-10-09

- Batch14 completes 자동차 레이스79–83:50 text regions,11 original images,
  243 physical code rows/106 BASIC statements, three inline examples and two
  disassemblies. Source83 bookstore advertisement excluded. Diagrams retain their
  original geometry and embedded labels as images. Nine review items remain.
- Restored omitted320 tail/330–360,850 continuation, repeated character-definition
  terms and misread zeros/targets. All12 definitions now contain the12 printed
  byte terms. Independently transcribed39-byte scroll and24-byte attribute DATA
  exactly match printed disassemblies; zero terminators retained. No execution.
- Custom screen characters inside literals use explicit editorial ⟦...⟧ markers;
  their exact bytes/cell counts and some literal spacing require human review.
  This complete article reading edition is not an executable reconstruction.
- Preparation88.27s; inference65.81s;31,707 local tokens; sampled GPU7,804MiB /
  RSS6,422MiB. Selected DATA compact CER2.15% versus39.27%; disassembly1.45%
  versus47.69% Tesseract. Assistant reference fixed before comparison; not human
  gold or an end-to-end speed claim. Repeated-byte omissions are a notable limit.
-50 cache hits/zero calls; all raw stages and stop reasons checked, native export
  and rebuild identical, source/text/review/listing byte ranges verified.
- June totals61 article source pages,12 complete articles,one non-owning heading,
  zero human accepted. Continue 한글 전화번호부와 주소록84 onward and remaining queue.

### Reading room refresh through car race, 2026-10-09

- Grouped staging adds four pinned packages to the prior eight-article preview;
  twelve June articles now available at the existing port4187 review URL. Reload
  an open tab to clear its in-memory collection. Original previews remain intact.
- Fresh output `build/reading-room-qwen-june-through-car` passes complete dataset
  inventory and projection checks, preservation of the prior collection and source
  package pins, TypeScript/production build, and desktop browser navigation and
  side-by-side car-code review. Human-pending state and graphic markers visible.
- Next article extent checked: telephone/address84–93;94/95 advertisements excluded.
  Batch15 mapped111 regions and completed88 raw calls; semantic checking underway.
  Do not count this article as reviewed or include it in the current preview yet.

### Telephone/address book checkpoint, 2026-10-09

- Batch15 completes 한글 전화번호부와 주소록84–93:88 text regions,23 original
  images,416 physical listing rows/180 numbered statements across two listings.
  Six table sections now preserve row associations as TSV. Flowcharts and screen
  labels remain image-only;88 advertisement and94/95 advertisements excluded.
- Corrected punctuation, duplicated wrap glyphs, digits, banner runs and Korean
  misreadings against scans. Preserved printed Roman-keyboard Hangul strings and
  source inconsistencies;14 explicit review notes remain. No execution or claim
  of exact literal spacing. Human acceptance remains pending.
- Raw preparation172.82s; inference135.61s;62,255 local tokens; sampled GPU7,828MiB /
  RSS9,194MiB. Fixed table sample compact CER0.26% versus9.87% Tesseract; maker
  listing1.80% versus15.27%; final listing3.08% versus56.92%. Same crops, assistant
  reference fixed before Tesseract; unblinded, not human gold. Whitespace ignored
  by these diagnostics, including literal blanks. Human effort/tokens unmeasured.
-88 cache hits/zero new calls; all raw stages stopped normally. Export/rebuild
  identical; source/text/review/listing byte ranges and printed line numbers checked.
- June totals71 article source pages,13 complete assistant-reviewed articles,
  one non-owning heading,zero human accepted. Current reading room still includes
  twelve articles; address book is ready for the next grouped refresh.
- Continue 별로 재미없는 프로그램 starting96 and the remaining issue queue.
