# Sustainable OCR and correction workflow

Updated: 2026-10-11. Owner: the archive maintainer; implementation and experiments
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

### Puzzle checkpoint and education divider, 2026-10-09

- Batch16 completes 별로 재미없는 프로그램96–98:36 text regions,four original
  images,168 physical code rows/147 statements across Apple and FC-100/SPC-1000
  versions. Restored omitted1050 continuation and removed inferred closing quotes;
  retained apparent source defects, physical wraps and six human-review notes.
- Raw preparation53.15s; inference38.84s;21,261 local tokens; sampled GPU7,800MiB /
  RSS4,763MiB. Fixed ending prose compact CER0.47% versus11.32% Tesseract;
  FC/SPC sample1.08% versus24.55%. Same crops and reference fixed before Tesseract;
  assistant-derived diagnostics, not independent human gold or total work speed.
-36 cache hits/zero new calls; export/rebuild identical; all raw stages/stop reasons,
  text/review/listing byte ranges and printed statement labels checked.
-99 classified as non-owning 교육입문 divider with six existing child entries.
  June totals74 article source pages,14 complete assistant-reviewed articles,
  two non-owning headings,zero human accepted. Reading room still twelve articles;
  address book and puzzle ready for next refresh. Continue Z80 tutorial100–107.

### Z80 tutorial checkpoint and reader refresh, 2026-10-09

- Batch17 completes Z80 기계어 강좌100–107:100 text regions,17 original images,
  78 physical assembly/inline code rows and eight unresolved source readings.
  Opcode matrices104,exchange table105 and diagram labels remain image-only;
  all article content is present for reading, but those cells are not text exports.
- Reconstructed assembly address/byte/instruction row associations lost by Qwen,
  corrected faint digits and Korean misreadings, joined cross-column prose.
  Preserved apparent source defects and flagged0643/0843 discrepancy rather than
  repairing code. No assembler execution or byte validation claimed.
- Raw preparation162.93s; inference95.68s;49,749 local tokens; sampled GPU7,794MiB /
  RSS8,818MiB. Reader staging overlapped this run: preparation time is not a
  controlled speed comparison. Fixed prose compact CER0% versus12.22% Tesseract;
  final assembly crop0% versus32.58%. On faint listing1 main crop Qwen lost row
  order:65.27% versus45.42% Tesseract, an important counterexample. Both required
  substantial correction; no independent human gold and literal blanks unscored.
-100 cache hits/zero new calls; native export/rebuild identical; raw stop reasons,
  article/review/listing byte coverage verified. June totals82 article source pages,
  15 complete assistant-reviewed articles,two non-owning headings,zero human accepted.
- Fresh grouped reader `build/reading-room-qwen-june-through-puzzle` adds address
  book and puzzle to the prior12 articles.14 are now available at port4187; reload
  the tab. Dataset/source pins, unchanged prior collection and production build
  checked; browser source/correction view verified, screenshot inspected. Z80 is
  ready for a later grouped refresh. Continue LOGO starting108 and remaining queue.

### LOGO checkpoint and TOC reconciliation, 2026-10-09

- Batch18 completes LOGO108–112:75 text regions,11 original images,83 physical
  code rows in16 groups,10 unresolved readings. Preserved source COUNTDOWOWN,
  LEGNTH, missing END and prose spelling mistakes; no executable repair.
- Raw preparation80.33s; inference40.06s;26,959 local tokens; sampled GPU7,788MiB /
  RSS5,468MiB. Fixed definition compact CER1.28% versus12.82% Tesseract;
  TREE0% versus3.13%; FLUFF0% versus3.70%. Assistant-derived unblinded reference,
  not independent human gold; literal blanks unscored, total human effort unknown.
-75 cache hits/zero new calls; export/rebuild and text/review/listing byte ranges
  verified. June totals87 article source pages,16 complete assistant-reviewed
  articles,two classified non-owning headings,zero human accepted.
- Reconciled historical44-entry restoration queue with canonical45-entry TOC:
  added pending 읽을거리 heading0045; corrected0035 title and parent projection.
  Original queue retained, current queue and reconciliation evidence separately pinned.
  Final closeout must account for all45 entries. Reader remains14 articles pending
  next grouped refresh. Continue graphics animation113 onward.

### Graphics animation checkpoint, 2026-10-09

- Batch19 completes 기초 테크닉 코너113–116:46 text regions,120 physical code
  rows,92 numbered statements across eight printed BASIC listings plus inline
  examples. Commercial advertisement116 excluded. Six source issues flagged,
  including inconsistent monitor direction, mismatched explanation numbers and
  duplicated star program inside list4-1. No program repairs or execution.
- Raw preparation82.72s; inference57.98s;28,596 local tokens; sampled GPU7,808MiB /
  RSS5,907MiB. Lookahead rendering overlapped preparation; not controlled speed.
  Fixed prose compact CER0% versus1.79% Tesseract; windmill0.95% versus12.38%;
  final27-row listing0% versus7.01%. Assistant-derived diagnostics only, literal
  blanks unscored and human effort unknown.
-46 cache hits/zero new calls; export/rebuild and UTF-8 article/review/listing ranges
  verified, including duplicate numbered rows. Totals91 article source pages,
  17 complete assistant-reviewed articles,two non-owning headings,zero accepted.
  Continue graphics117–123 and all remaining issue entries.

### Computer graphics checkpoint, 2026-10-09

- Batch20 completes 컴퓨터 그래픽과 친구가 되자117–123:81 text regions,seven
  images,two text tables,172 physical code rows,139 numbered statements and ten
  unresolved items. Preserved differing table/DATA values and printed wording;
  blank CTRL-G strings are visible transcription, not recovered control bytes.
- Corrected clipped final code crop before the final run; retained aborted raw
  evidence separately (32 completed calls,30.30s additional inference). Final run:
  preparation141.85s,inference87.34s,42,806 local tokens,GPU7,802MiB/RSS7,881MiB.
  Lookahead rendering overlapped; these are not total-work or controlled speed figures.
- Fixed prose/table/game crop compact CER0% each, versus3.80%,13.42%,21.56%
  Tesseract. Unblinded assistant-derived references; literal blanks unscored.
-81 cache hits/zero new calls; native rebuild, article/review UTF-8 ranges and
  physical/logical listing coverage verified. Totals98 article source pages,
  18 complete assistant-reviewed articles,two non-owning headings,zero accepted.
  Next BASIC speed124–125 and educational program126 onward; full issue ongoing.

### BASIC speed checkpoint, 2026-10-09

- Batch21 completes 베이직 프로그램 처리속도 증진법124–125:40 text regions,
  two images,52 physical annotated code/monitor rows in nine groups,five unresolved
  items. Joined spread title and cross-column prose. Preserved damaged assignment,
  printed comma syntax and historical claims; no executable repair or byte validation.
- Raw preparation36.77s; inference24.00s;15,324 local tokens; sampled GPU7,808MiB /
  RSS3,747MiB. Reader staging overlapped; not controlled speed. Fixed mixed dump
  compact CER11.22% versus77.55% Tesseract; prose1.25% versus10.00%. Unblinded
  scan-corrected reference, literal blanks unscored, human effort unknown.
-40 cache hits/zero new calls; native rebuild and UTF-8 ranges/listing coverage
  verified. Totals100 source pages,19 complete assistant-reviewed articles,
  two non-owning headings,zero human accepted. Educational program126–129 next.

### Heat and Work checkpoint, 2026-10-09

- Batch22 completes educational program126–129:55 text regions,five images,
  154 physical code rows,56 numbered statements and eight unresolved items.
  Preserved source title 열과 일 versus canonical TOC 열과 알, split Hangul
  glyph candidate, formula and original DATA rows. Diagrams remain source images.
- Raw preparation91.49s; inference55.55s;26,507 local tokens; sampled GPU7,800MiB /
  RSS5,462MiB. Fixed prose compact CER0% versus1.67% Tesseract; Korean listing
  1.46% versus19.90%; DATA/drawing block0% versus12.56%. Unblinded assistant
  reference, literal blanks unscored; no end-to-end speed or human-effort claim.
-55 cache hits/zero new calls; native rebuild and UTF-8 ranges/listing coverage
  verified. Totals104 source pages,20 complete assistant-reviewed articles,
  two non-owning headings,zero human accepted. Information radar131–140 next.
- Grouped reader refreshed to18 articles through graphics117–123. All prior146
  scan articles and CD files preserved; integrity/build checks passed. Browser
  checked graphics article tables and side-by-side final code region123; screenshot
  retained privately. BASIC speed and Heat and Work await the next grouped refresh.

### Information Radar checkpoint, 2026-10-10

- Batch23 completes 정보레이다131–140:171 text regions,four photographs,two
  transcribed tables and ten unresolved items. Source geography, IMB spelling,
  reversed price range, inconsistent forecast and hardware units remain printed.
- Full fee-table inference failed by repeating tabs to4096 output tokens. A row
  retry also failed at4096 tokens. Both responses and preceding successful calls
  remain private; final cell-level segmentation succeeded. The two failed runs
  additionally used125 completed calls/111.98s inference plus the failed calls;
  a padding adjustment stopped another attempt before any completed inference.
  Final-run figures below exclude those costs and cannot represent total effort.
- Final raw preparation238.47s; inference188.04s;102,320 local tokens; sampled
  GPU7,838MiB/RSS10,502MiB. Two originally selected prose crops have compact
  CER0%/1.75%, versus2.07%/11.40% Tesseract. Revised fee-header crop0% versus
  74.36% is a post-failure diagnostic, not the originally selected full-table test.
  All references remain assistant-derived, unblinded and whitespace-insensitive.
-171 cache hits/zero new calls; export/rebuild and UTF-8 review ranges verified.
  Totals114 source pages,21 complete assistant-reviewed articles,zero accepted.
  Business divider141 classified as the third non-owning heading; four canonical
  children retained. UNIX142–148 raw OCR complete; VISISUM149–154 running.

### UNIX checkpoint, 2026-10-10

- Batch24 completes UNIX142–148:120 text regions,eight original diagrams and
  illustrations,six unresolved readings. Cross-page prose joins restored; printed
  CALENDER, 패워드 and historical technical descriptions retained. Annotated
  command-screen diagrams remain images; no current-system commands executed.
- Raw preparation111.62s; inference84.89s;50,200 local tokens; sampled GPU7,800MiB /
  RSS8,971MiB. Fixed mail prose/list/MAKE prose compact CER0%/1.22%/0%, versus
  1.67%/19.51%/4.55% Tesseract. Unblinded assistant-derived diagnostic references,
  not independent human gold; human effort and paid-token usage unmeasured.
-120 cache hits/zero new calls; export/rebuild and UTF-8 review ranges verified.
  Totals121 source pages,22 complete assistant-reviewed articles,three non-owning
  headings,zero human accepted. VISISUM raw OCR complete; semantic review next.

### VISISUM checkpoint, 2026-10-10

- Batch25 completes VISISUM149–154:72 text regions,12 original images,172
  physical code rows,144 numbered statements and nine unresolved items. Restored
  omitted dash strings and a wrapped arithmetic continuation; preserved printed
  incorrect sum, ENVIROMENT and ERROR IN FILE FOT. Staffing table order manually
  reconstructed with all empty cells; matrix examples remain images.
- Raw preparation81.55s; inference59.38s;34,774 local tokens; sampled GPU7,834MiB /
  RSS6,747MiB. Fixed prose/code/code compact CER0%/0%/2.65%, versus4.62%/56.67%/
  26.49% Tesseract. Assistant-derived unblinded references; literal spaces ignored
  by compact CER, faint0/O readings remain candidates. Not an end-to-end measure.
-72 cache hits/zero new calls; native rebuild, UTF-8 ranges and complete listing
  coverage verified. Totals127 source pages,23 complete assistant-reviewed articles,
  three non-owning headings,zero human accepted. Medical-insurance155–161 next.
- Grouped reader now22 articles through UNIX. Prior scan/CD files preserved;
  integrity and production build passed. Browser checked Information Radar article
  and side-by-side fee-table region; screenshot viewed. Full browser reload needed
  to discard the previous in-memory catalog. VISISUM awaits next grouped refresh.

### Medical-insurance program checkpoint, 2026-10-10

- Batch26 completes 의료보험 수가계산155–161:118 text regions,two images,
  five listing groups,223 physical rows,168 numbered statements and11 unresolved
  items. Kept the four printed variations separate with their explicitly omitted
  shared continuations. Boxed arrows transcribed as bracketed arrows; inconsistent
  variable descriptions and printed identifiers preserved. No program execution.
- Corrected one boundary crossing a Korean string. Two changed crops re-inferred;
  116 other stages reused after exact image/runtime verification. Initial118-call
  pass153.75s plus recovery27.28s gives181.03s raw preparation. Final-stage inference
  122.49s excludes4.95s in the two superseded responses; no failed inference calls.
  Final stages66,083 local tokens; sampled GPU7,798MiB/RSS10,339MiB.
- Fixed prose/code/code compact CER0%/0.69%/0%, versus5.88%/22.76%/15.53%
  Tesseract. Samples unchanged by boundary repair. Unblinded assistant references,
  whitespace-insensitive metrics; no independent human accuracy or effort claim.
-118 cache hits/zero new calls on final resume; export/rebuild, UTF-8 indexes and
  complete listing coverage verified. Totals134 source pages,24 complete assistant-
  reviewed articles,three non-owning headings,zero human accepted. VISICALC next.

### VISICALC checkpoint, 2026-10-10

- Batch27 completes VISICALC 활용162–169:130 text regions,three output images,
  three BASIC listings,454 physical rows,346 numbered statements,14 review flags.
  Restored keyboard symbols, physical wraps, WDTH and scan-counted asterisks.
  Faint Korean dealer names remain candidates; printed RETUF, missing assignment,
  inconsistent formula labels and RETURN-before-NEXT retained without repair.
- Widened one prose crop that omitted wrapped-line 하. Initial130-call run plus
  one corrected inference took174.52s;129 unchanged stages reused only after exact
  image/runtime verification. Final-stage inference115.73s excludes superseded crop;
  final65,892 local tokens,sampled GPU7,822MiB/RSS10,083MiB. No failed inference.
- Fixed prose/BASIC/Hangul-DATA compact CER0%/5.52%/5.98%, versus13.85%/31.03%/
  55.56% Tesseract. Korean DATA uses kor+eng, chosen before Tesseract output.
  Unblinded assistant references; faint names and ignored literal whitespace limit
  these diagnostics. No independent human or end-to-end productivity claim.
-130 cache hits/zero new calls; rebuild, UTF-8 indexes and listing coverage passed.
  Totals142 source pages,25 complete assistant-reviewed articles,four non-owning
  headings,zero human accepted. Technical divider171 classified, children retained.
  Next: design tutorial172–181 and grouped reader refresh, then remaining issue.

### Microcomputer design checkpoint, 2026-10-10

- Batch28 completes 마이크로 컴퓨터 설계 강좌172–181:114 text regions,
  sixteen images,eleven review flags. Schematics and main pin/parts tables remain
  source images. Restored cross-column sentences, active-low overbars and the small
  address/data table; retained printed SPEP/SETP and unusual technical wording.
- One paragraph failed with4096 repeated U+2060 escape tokens. Its response is
  preserved. Splitting it into three crops succeeded;103 completed stages reused
  after exact image/runtime checks. The barred WR/RD line still required scan
  correction. Final114-stage inference103.05s;55,976 successful local tokens plus
  4,674 failed-call tokens. Failed server prompt+generation38.71s. Recovery wall
  time36.85s is **only the recovery pass**; initial aborted wall time is unavailable.
  Sampled successful-stage peaks GPU7,794MiB/RSS8,947MiB.
- Fixed prose/prose/table compact CER0%/0%/59.68%, versus4.92%/30.67%/54.84%
  Tesseract. Table score includes annotation reading-order differences and is not
  a pure glyph metric. References remain unblinded assistant transcriptions;
  no human accuracy or end-to-end productivity claim.
-114 cache hits/zero new calls; export/rebuild and UTF-8 indexes verified. Totals
  152 source pages,26 complete assistant-reviewed articles,four non-owning headings,
  zero human accepted. Grouped preview refresh underway. Scan inspection establishes
  relocator182–185 and classifieds186; earlier estimated188 is not the actual body.

### Reading-room refresh through design, 2026-10-10

- Local preview4187 now contains26 June articles, adding VISISUM, medical insurance,
  VISICALC and computer design to the previous22. Dataset integrity, package pins,
  unchanged previous scan/CD files and production build passed. Browser reloaded;
  checked26-article navigation, VISICALC Korean DATA side-by-side and design WR/RD
  overbars/review flags. Both screenshots were visually inspected.
- Fixed staging helper `stage-group28.py`; output `build/reading-room-qwen-june-through-design`.
  Manifest `6f8b3c282125f98fe239072d5112dfdb616dc0d502c8d9c51cedfb4702e28ce6`.
  Previous previews retained; no publication or human acceptance inferred.

### Relocator checkpoint, 2026-10-10

- Batch29 completes 리로케이터 프로그램182–185:54 text regions,two diagrams,
  six listing groups,366 physical rows and297 numbered assembler source rows
  (0000–0296). Repaired OCR column ordering and repeated hex-byte omissions;
  retained printed addresses, D000, RELOCATER, STOP and historical assembler result.
  Nine explicit review flags; no execution/reassembly or original-byte claim.
- Raw preparation124.67s; inference105.58s;38,716 local tokens; sampled GPU7,988MiB /
  RSS7,367MiB. No failed inference. Fixed prose/example/assembly compact CER all0%,
  versus4.69%/1.67%/64.77% Tesseract. These are unblinded assistant-reference
  diagnostics; table/column order and whitespace normalization limit interpretation.
-54 cache hits/zero new calls; rebuild, explicit source-row coverage and UTF-8
  indexes passed. Private export helper now accepts explicit block-ID overrides,
  keeping raw maps immutable when informal region notes repeat across pages.
  Totals156 source pages,27 complete assistant-reviewed articles,four non-owning
  headings,zero human accepted. Reader has26 articles; relocator awaits next refresh.

### Classifieds and contest review, 2026-10-10

- Batch30 completes 복덕방 on actual page186 (TOC estimate188):28 text regions,
  three review flags. Historical prices, contact details and printed BAGIC-G retained.
  Moved a shared crop edge four normalized pixels to avoid touching 령; reran two
  crops and reused26 after exact image/runtime checks. Original evidence retained.
  Combined original+recovery wall36.21s; final-stage inference16.36s excludes the
  superseded two crops.10,825 final local tokens; GPU7,758MiB/RSS3,023MiB.
- Batch31 completes 공모총평190–191:40 text regions, six review flags. Rejoined
  spread title and column continuations; six award rows plus header as TSV.
  Retained printed machine-name discrepancies and unusual wording. Raw50.62s,
  inference32.09s,18,962 local tokens,GPU7,792MiB/RSS4,313MiB. No failed calls.
- Three fixed samples per article: compact CER all0% Qwen; Tesseract4.05%/6.94%/
  18.67% for classifieds and3.62%/6.67%/37.50% for contest review. The table sample
  is a single row; these unblinded assistant-reference results are not human gold.
- Both exports and byte-identical rebuilds passed; UTF-8 source indexes verified;
  resume28+40 cache hits,zero new calls. Totals159 source pages,29 complete
  assistant-reviewed articles,four non-owning headings,zero human accepted.
  Reader remains26 articles pending next grouped refresh. Next: graphic editor192–198.

### Graphic editor checkpoint, 2026-10-10

- Batch32 completes 그래픽 에디터192–198:163 text regions,four source images,
  seven listing groups,152 physical listing rows,141 numbered rows,twelve review
  flags. Five inline examples, eight-row hex routine and complete BASIC are kept
  separate. Restored PRINT USING hash counts, O/0 candidates and physical wraps;
  retained printed SHTFT and apparent original program anomalies. No execution.
- Initial process ended with SIGTERM143 after140 completed stages. Cause unknown;
  incomplete region request/server log retained. Recovery reused140 exact-image/
  runtime stages and ran23 remaining calls. Recovery73.34s is **not total raw wall
  time**; initial wall time is unavailable. Final-stage inference130.50s,75,353
  local tokens plus231 tokens logged for the interrupted response,0.19s server
  prompt+generation for that request. GPU7,802MiB/RSS9,115MiB sampled.
- Fixed prose/hex/BASIC compact CER0%/5%/0.37% Qwen versus2.78%/47.50%/43.45%
  Tesseract. Unblinded assistant-reference diagnostics; whitespace and original
  encoding are not verified.163 cache hits/zero new calls; export,rebuild,source
  row coverage and UTF-8 indexes passed. Totals166 source pages,30 complete
  assistant-reviewed articles,four non-owning headings,zero human accepted.
- Grouped reader refresh through graphic editor is building. Next article is
  한글 소트199–204; figures and crop edges checked before inference.

### Hangul sort and reader refresh, 2026-10-10

- Batch33 completes 한글 소트199–204:99 text regions,nine source images,
  three listing groups,133 physical rows,127 numbered rows,eleven review flags.
  Preserved printed DATA space marks as visible U+2423 candidates, jamo, physical
  wraps and original inconsistencies. Counted rule lengths and checked literal
  padding against scans; original encoding and executable correctness unverified.
- Raw122.38s,inference94.58s,54,870 local tokens; GPU7,800MiB/RSS9,750MiB sampled.
  No failed calls. Fixed prose/DATA/BASIC compact CER0%/5.90%/1.22% versus
  Tesseract4.35%/16.24%/37.80%. Code baseline uses eng, including the Korean-literal
  sample; this limits comparison. Unblinded assistant reference, not human gold.
-99 cache hits/zero new calls; export,rebuild,source-row coverage and UTF-8 checks
  passed. Totals172 source pages,31 complete assistant-reviewed articles,four
  non-owning headings,zero human accepted. Next: computer rebellion205–209.
- Grouped reader now contains30 complete articles through graphic editor at4187.
  Fresh staging preserved prior files and scanInputs; full integrity and production
  build passed. Browser issue count, BASIC scan/correction and contest table row
  checked, screenshots viewed. Hangul sort awaits the next grouped refresh.

### Computer rebellion checkpoint, 2026-10-10

- Batch34 assembles 당신은 컴퓨터 반란 진압대205–209:108 successful Qwen regions,
  three explicitly assistant-manual regions and one illustration. Listing200
  numbered rows/334 physical rows; fifteen review flags. The title literals
 7020–7120 remain editorial placeholders with scans, not character-transcribed
  program text. Box glyphs and header rule counts are visual candidates only.
- Two4096-token repetition failures (asterisk border, box rules) retained. Manual
  source fallback is separately labeled, never fabricated as raw Qwen output.
  Also repaired raw omissions after a normal stop, line-number errors, repeated
  hex DATA and O/0 readings. Printed anomalies retained; no program execution.
- Combined original+two recovery wall220.38s; final108-stage inference80.39s plus
 77.66s failed server prompt/generation.42,995 successful tokens +9,900 failed =
 52,895 local tokens. GPU7,794MiB/RSS4,526MiB sampled from successful stages;
  these are not a measurement of manual work or failed-request resource peaks.
- Fixed prose/BASIC/DATA compact CER0%/2.80%/1.18% versus9.21%/25.23%/28.24%.
  BASIC crop narrowed after header failure. These three unblinded samples exclude
  the graphical failures and manual fallback, so cannot represent whole-article
  accuracy.108 cache hits/zero new calls; export/rebuild, UTF-8 and explicit
  source-row checks passed. Totals177 pages,32 assembled assistant-reviewed
  articles,four non-owning headings,zero human accepted. Reader remains30 articles.
- Next: horse-blocking game210–213, already through raw OCR and scan inspection.

### Horse-blocking game checkpoint, 2026-10-10

- Batch35 completes 말 움직여 막기 게임210–213:92 text regions,three gameplay
  images,one BASIC listing,339 physical rows/211 numbered rows,thirteen flags.
  Restored missing DATA160 continuation, assignment710 tail, printed wraps,
  I/1/O/0 and punctuation. Preserved source PLESE, CONGRATURTIONS, SHIF and
  doubtful comma/dot marks. Literal padding remains uncertain; no execution.
- Raw98.24s,inference78.38s,41,308 local tokens,GPU7,760MiB/RSS7,459MiB sampled.
  No failed calls. Fixed prose/header/BASIC compact CER0%/2.47%/0.56% versus
  Tesseract10.81%/62.96%/35.56%; unblinded assistant-reference diagnostics,
  whitespace ignored and no claim of full-article or human-gold accuracy.
-92 cache hits/zero new calls; export/rebuild, UTF-8 and explicit printed-row
  coverage passed. Totals181 pages,33 complete assistant-reviewed articles,
  four non-owning headings,zero human accepted. Reader remains30 articles.
  Next: 메아리214–216 (two contributions), then Q&A219–221. Pages217–218
  are advertisements; page221 continues Q&A, not a reading-section divider.

### Readers letters checkpoint, 2026-10-10

- Batch36 completes 메아리214–216, including SERPENT-alpha corrections and the
  Apple lowercase technique:54 text regions,one memory diagram,four listing
  groups,16 physical rows,nine numbered rows,eight review flags. Joined split
  prose and CTRL-R across columns. Preserved historical advice, spellings and
  repeated SCRN$ coordinates; filled-square literal is a Unicode visual candidate.
- Raw53.24s,inference37.88s,24,348 local tokens,GPU7,806MiB/RSS5,161MiB sampled.
  No failed calls. Fixed prose/condition/BASIC compact CER0%/2.53%/0% versus
 11.63%/11.39%/19.44%; unblinded assistant reference, no human-gold claim.
-54 cache hits/zero new calls; export/rebuild, UTF-8 and listing row checks passed.
  Totals184 source pages,34 complete assistant-reviewed articles,four non-owning
  headings,zero human accepted. Grouped preview through letters is staging.
  Next: Q&A219–221; history222–244; appendix245–249; ad index250.

### Q&A checkpoint, 2026-10-10

- Batch37 completes Q&A219–221:61 text regions,one illustration,14 separate
  listing groups,37 physical rows/18 numbered rows,eleven human-review flags.
  Scan corrections include MERGE brackets, Korean words and superscript math;
  printed TETS, 00A0H, hex-address gap, LIST letter O and a dubious leading dot
  remain visible for review. Historical technical claims were not repaired.
- Raw64.21s,inference46.70s,27,510 local tokens,GPU7,802MiB/RSS5,668MiB sampled.
  No failed calls. Fixed prose/hex/BASIC compact CER0%/0%/0% versus Tesseract
  7.45%/88.13%/26.67%. Unblinded assistant reference; not human-gold accuracy.
-61 cache hits/zero new calls; export/rebuild, UTF-8 and explicit source-row checks
  passed. Totals187 source pages,35 complete assistant-reviewed articles,four
  non-owning headings,zero human accepted. History222–244 is next in two batches,
  followed by appendix245–249,ad index250 and remaining heading classifications.

### Grouped reading preview through letters, 2026-10-10

- Staged four newly complete packages into a fresh grouped reader:34 June articles.
  All prior146 scan articles, CD content and previous scanInputs preserved. Full
  dataset integrity, projection/source pins and unchanged prior bytes passed.
- Production build passed. A full browser reload confirmed34 articles; source
  review checked the rebellion title-graphic placeholders and letters SCRN$ code,
  including human-pending banners, scans and correction notes. Screenshots viewed.
  Local preview remains at port4187; original phoneme preview4186 preserved.
- New manifest8d1f93b99103efc869d7c229b4b72e41c8d2a2341785d84ec627c7664a806aac.
  No frontend changes; the user's homepage edit remains untouched and uncommitted.
  Q&A is complete but awaits the next grouped/final reader; history OCR underway.

### History opening checkpoint, 2026-10-10

- Batch38 restores history222–233 as a partial package:167 text regions,eleven
  original images (including the star-rating comparison),25 explicit prose/title
  joins,eight review flags. Sidebars and interview continuations retain reading
  order around images. Printed claims/names remain unmodernized.
- Raw225.16s,inference160.33s,93,238 local tokens,GPU7,802MiB/RSS10,343MiB sampled.
  No failed calls. Three fixed prose samples compact CER0%/0%/0% versus9.09%/
  11.90%/12.26%; unblinded assistant reference, not human-gold evidence.
-167 cache hits/zero new calls; export/rebuild and UTF-8 ranges passed.
  Totals199 source pages,35 complete articles plus one partial,four non-owning
  headings,zero human accepted. History ending234–244 is running; assembly will
  join the preserved segments before staging. Reader remains34 articles.

### Complete history checkpoint, 2026-10-10

- Batch39 adds234–244:158 text regions,six images,22 explicit joins,ten flags.
  Raw213.15s,inference164.17s,86,805 local tokens,GPU7,794MiB/RSS10,276MiB.
  Three fixed prose compact CER0%/0.78%/0.51% versus Tesseract9.33%/35.94%/
  15.15%; unblinded assistant-reference diagnostics, not human-gold accuracy.
- Joined preserved opening/ending into complete history222–244:342 regions,
  325 text regions,seventeen images,eighteen flags. Osborne prose and boxed
  company profiles retain continuous reading order; cross-page 달/러 joined.
  Full coverage,pins,UTF-8 ranges and byte-identical rebuild passed;158 cache
  hits and zero new calls for batch39. Historical claims were not modernized.
- Totals210 source pages,36 complete assistant-reviewed articles,no partials,
  four non-owning headings,zero human accepted. Appendix and index raw OCR
  finished; final corrections, heading classification and whole reader remain.

### Appendix and index checkpoint, 2026-10-10

- Batch40 completes contest problems245–249:124 text regions,twelve diagrams,
  three continuation joins,fifteen review flags. Four divisions, tables and
  formulas retain source wording; printed duplicated editor P command is flagged.
  Raw95.00s,inference71.00s,47,005 local tokens,GPU7,806MiB/RSS8,311MiB sampled.
  Fixed prose/name-table/command-table compact CER0%/0%/6.11% versus Tesseract
  4%/4.88%/54.15%; unblinded assistant-reference diagnostics, not human gold.
- Batch41 completes advertisement index250:31 company/page pairs,four text
  regions,one decorative image,four flags. Dotted leaders become TSV separators.
  Raw12.20s,inference4.80s,2,380 local tokens,GPU7,788MiB/RSS1,747MiB sampled.
  Primary character scores are dominated by decorative leaders. A separately
  labeled post-hoc diagnostic strips the same four punctuation characters from
  both outputs/reference: Qwen0%/1.85%/0% versus155.17%/164.81%/90.70%.
  Tesseract hallucinated letters/digits and omitted rows remain penalized; this is
  not a general OCR ranking or a human-gold/whole-index accuracy claim.
-128 cache hits,zero new calls; both native exports,rebuilds,coverage and UTF-8
  ranges passed. Totals216 source pages,38 complete articles,no partials,zero
  human accepted. Three remaining non-owning TOC headings and final preview next.

### Whole-issue accounting, 2026-10-10

- All45 canonical contents entries are accounted for:38 readable article bodies,
  seven non-owning headings,no missing/partial/failed bodies. All38 remain
  assistant sample-reviewed and human-pending; readable is not character-perfect.
- Original contents PDF17 and source spreads confirm 공모입선작, 읽을 거리 and
  정보모음 are group headings. Preserved canonical titles/parents and the known
  복덕방 TOC188 versus actual186 discrepancy. Advertisements and unlisted notices
  are outside the canonical-article restoration scope.
- Private whole-issue-ledger.json pins every completed package. Public accounting
  is docs/ocr-june-accounting.json. Final reader stages from the unchanged
  pre-June collection into a fresh directory, preserving earlier previews.

### Complete June reading room, 2026-10-10

- Fresh complete reader staged at build/reading-room-qwen-june-complete: all38
  article bodies,216 source pages,seven group headings,all45 TOC entries resolved.
  Native packages contain3,082 regions and325 explicit unresolved-text flags;
  flags are review aids, not an exhaustive error count. Human acceptances remain0.
- Full dataset integrity, package/projection pins, prior collection byte preservation,
  complete TOC accounting and production build passed. Earlier preview folders
  and the phoneme reader remain unchanged. Final data manifest:
  551f16c995adf82bbd366e69167e022bf3363b98199e60e60439e3788fef8b7a.
- Browser reload verified38 articles and coverage status. Checked the joined
  history and its342-region source review, plus appendix tables and duplicated-P
  source flag. Screenshots captured and viewed; human-pending notices preserved.
  Local review URL: http://127.0.0.1:4187/archive/#/issues/maso-1984-06.
- All requested article restoration and preview preparation are complete. Next is
  mandatory human review/correction. Some graphic literals remain placeholders;
  no claim of character-perfect text, executable code or measured paid-token/time
  savings. No frontend change; user's homepage edit remains uncommitted.


### Consolidated decision metrics, 2026-10-10

- Added docs/OCR-JUNE-DECISION.md and reproducible docs/ocr-june-metrics.json.
  Aggregated 38 comparison files: 102 matched crops, with 97 ordinary CER crops,
  three decorative-index crops and two separately cell-scored tables. Weighted
  compact CER on the 97 non-index crops is 2.22% Qwen versus 25.61% Tesseract;
  including index, 3.78% versus 27.05%. References remain unblinded assistant drafts.
- Matched engine time is 206.12s versus 28.75s: Qwen is 7.17 times slower in raw
  recognition. Retained June inference totals 50.40 minutes, not full project time.
  Summed raw-run segments cover 66.45 minutes but have explicit timing gaps.
- Retained OCR used 1,585,546 local tokens. Auditing 3,041 distinct completion IDs,
  ignoring 661 copied cached responses, plus one separately logged interrupted
  request yields 1,755,701 observed tokens: 10.73% additional work. Five archived
  failed responses hit the output limit; ordinary-stop omissions remain possible.
- Recommended next trial: Qwen raw OCR with current semantic correction and
  mandatory human review; Tesseract fallback/selective comparisons. Local Qwen
  self-correction remains optional given extra compute and observed regressions.
  No pipeline defaults changed. Paid assistant tokens, human active review time,
  energy and cost per accepted page remain unmeasured; no savings claim.
- Consolidator tests cover weighted rates, empty/mismatched denominators, true
  reruns versus cache copies, and token reconciliation. Existing OCR evidence and
  the user's homepage edit are preserved.
- Validation: five focused aggregation tests passed; regenerated JSON and report
  match byte-for-byte. Retained calls/tokens reconcile with all 41 checkpoints.
  Early monitored-stage timing labels are explicitly distinguished from underlying
  inference timers; original checkpoint evidence was not rewritten.

### July content/cost trial started, 2026-10-10

- Maintainer selected July1984 for a second issue trial focused on paid assistant
  tokens versus elapsed work, with local GPU cost excluded from the decision.
  [Trial plan and first measurements](docs/OCR-JULY-TRIAL.md) use opposite primary
  assignments within content categories before drawing routing conclusions.
- Restored editorial printed16/PDF20 with Qwen and 운전 연습 printed83/PDF87 with
  Tesseract: two complete bodies,19 regions,57 numbered BASIC lines, six review
  flags. Native integrity, source coverage, UTF-8 ranges and identical rebuilds
  passed. Printed unclosed code strings retained; no execution or syntax repair.
- Both trial engines use4,000-pixel renders. Existing Tesseract default remains
  3,000. Four preselected matched-PNG diagnostics favor Qwen, including three
  references fixed from Tesseract drafts before alternate Qwen inference.
- Added response-deduplicated assistant usage accounting with separate cached,
  uncached, cache-write and output categories, explicit work windows, unknowns,
  and visible between-window overhead. First correction windows46.65s/70.89s are
  observational; Tesseract's window includes one export-helper setup response.
  No engine cost ranking follows from these different articles.
- Current42-entry queue: two restored bodies,40 entries pending restoration or
  heading classification. Next pair: 리뷰 살롱 with Tesseract; 합이15 with Qwen.
  Inspect complete boundaries and content before their OCR assignments begin.
- **User instruction: do not rebuild/restage the reading room until explicitly
  requested.** No reading-room action performed. Continue native restoration,
  evaluation, progress records and commits. User's homepage edit remains separate.
- Validation:16 focused tests pass across usage, Tesseract crop/settings behavior,
  native exports and the mapped Qwen adapter. Raw inference and full-stage timers
  are separate; shared setup/evaluation costs remain in the trial audit.

### July reverse assignments completed, 2026-10-10

- Batch03 restores 리뷰 살롱, printed156–158/PDF160–162, with Tesseract:
  seven book reviews,36 text regions,two original image strips,six review flags.
  Printed159/PDF163 is the following business-section opener, outside this body.
  Raw19.74s; recognition9.40s; correction/recording window117.92s.
- Batch04 restores 합이15, printed64–65/PDF68–69, with Qwen:17 text regions,
  three grids,107 numbered BASIC lines,five flags. Raw73.37s; recognition63.03s;
  13,683 local tokens; correction/recording window72.32s. Restored an invented
  wrap at48; retained printed ALTERNATLEY, UN FILLED and the<> operator at920.
- Both native packages pass coverage, integrity, UTF-8 ranges, explicit listing
  row accounting and byte-identical rebuild checks. No code execution or repair.
  Totals:four complete bodies,seven source pages,74 regions,164 logical listing
  lines,17 flags;38 TOC entries remain pending restoration/heading classification.
- Six preselected identical-crop comparisons favor Qwen raw text. Three references
  originate from Tesseract drafts and were sealed before alternate Qwen inference.
  Counts and timing remain observational; zero compact CER hides whitespace/wrap
  differences and is not a full-code fidelity claim.
- Usage audit includes previous reporting/commit tail and current shared overhead.
  New correction windows reuse the helper and contain no implementation work.
  Qwen code required fewer edits, but increased uncached image/context input means
  no paid-cost winner yet. See docs/OCR-JULY-TRIAL.md and cumulative JSON evidence.
- Next:inspect technical/table candidates SPC-1000 음악기능과 명령어 and PIA
  시리즈1 뮤직카드 before choosing their engines. Reading-room rebuild/staging
  remains prohibited until explicitly requested; none performed this checkpoint.

### July technical article completed, 2026-10-10

- Batch05 restores SPC-1000 음악기능과 명령어 with Qwen, printed47–51/PDF51–55:
  87 regions,82 text crops,five original figures,43 numbered BASIC lines and18
  source-linked review flags. Frequency table has13 TSV rows,nine columns and96
  checked numeric cells; original image retained alongside searchable text.
- Raw stage301.99s, including273.87s recognition and1.46s server startup/readiness.
  Correction/recording232.83s;44,891 local tokens. Observed correction usage:
  26,623 uncached input,532,992 cached input,10,485 output; zero cache-write tokens.
  Shared mapping, monitoring, evaluation and between-window costs remain separate.
- Four preselected identical-PNG comparisons again favor Qwen. Table compact CER
  Qwen0.00%,Tesseract89.43% under the fixed whole-table PSM6 configuration; no
  alternative row/cell segmentation tested. References remain assistant-derived.
  Source formula/register inconsistencies preserved, not technically repaired.
- Native integrity, UTF-8 ranges, explicit listing numbers, region coverage,
  table shape and byte-identical rebuild checks passed. Five complete July bodies,
  12 source pages,161 regions,207 logical BASIC lines,35 review flags;37 TOC entries
  remain pending restoration/heading classification. Human acceptance pending.
- Next: detailed mapping of PIA 시리즈1 뮤직카드, provisionally PDF184–194 after
  contact-sheet boundary inspection. Eleven-page body includes embedded advertising
  and long hexadecimal listings; engine/sample assignment remains pending mapping.
- Reading room was not rebuilt or restaged. Preserve user's homepage edit.
  Final reporting/commit tail is carried into the following cumulative usage audit.

### July music-card hardware segment completed, 2026-10-11

- Batch06 restores PIA 시리즈1 뮤직카드 hardware/construction section with
  Tesseract: printed180–183/PDF184–187,49 regions,41 text crops,eight original
  diagrams/photos and seven review flags. Boxed advertisement on185 excluded.
- This is a partial body: software instructions, references and hexadecimal
  listings PDF188–194 remain deferred. Full article assembly is still required.
  Accounting distinguishes five complete articles,one partial article and six
  checkpoints; partial segments do not increase completed-article counts.
- Raw22.16s; recognition8.06s; correction/recording128.80s for2,803 non-whitespace
  characters. Correction usage:10,395 uncached input,481,152 cached input,4,874
  output tokens; zero cache-write. Setup/helper adaptations remain outside the
  correction window. No raw inference retries; preparation schema error corrected
  before the pinned OCR map was run.
- Four preselected identical-PNG prose samples favor Qwen, using references sealed
  from Tesseract-based correction before alternate Qwen inference. Evaluation cost
  remains separate; no causal article-level paid-cost ranking follows.
- Native integrity, included-region coverage, UTF-8 ranges, advertisement mask,
  deferred-page metadata and byte-identical rebuild checks passed. Totals across
  restored segments:16 source pages,210 regions,193 text regions,17 original
  images,207 logical BASIC lines,42 review flags.37 TOC entries unfinished,
  including the partial body;36 untouched. Human acceptance remains pending.
- Next:map PDF188–194,assign engine/samples,restore remaining music-card content
  and assemble with batch06. Reading room unchanged; user's homepage edit retained.
  Reporting elapsed includes a brief interruption/resume, explicitly labelled;
  raw/correction timers were already closed. Carry final commit tail into next audit.

### Provisional content routing documented, 2026-10-11

- Added [engine-selection guidance](docs/OCR-JULY-TRIAL.md#provisional-engine-selection-heuristic)
  and linked it from the OCR workflow: Tesseract for clear prose, Qwen for costly
  character/structure errors, and original images for diagrams/photos.
- Recorded bounded probes, explicit primary/fallback assignments, retained attempt
  costs and one semantic correction per passage. BASIC evidence is promising;
  long hexadecimal listings remain untested. No causal paid-cost winner claimed.
- Documentation only; no automatic routing, pipeline default or reading-room change.

### July software instructions restored with routing rule, 2026-10-11

- Batch07 selects Qwen before inference for commands, addresses and notation,
  following Tesseract hardware06 in the same article. Restored PDF188–190 and upper
  PDF191:75 regions,69 text crops,six original images and17 review flags.
- PDF191 remains partial. Lower191 and192–194 hex listings are next; Qwen is the
  provisional choice, with detailed mapping/samples still required. Preserve both
  existing segments and assemble only after the listing is restored.
- Raw203.29s including181.05s recognition and1.26s startup; correction178.32s for
  4,722 non-whitespace characters. Correction usage:29,044 uncached input,
  316,160 cached input,6,422 output tokens; zero cache-write. Local Qwen32,686
  tokens separately recorded. Shared setup337.73s and monitoring/evaluation/report
  work remain visible; raw-window helper preparation is not correction cost.
- Four fixed samples favor Qwen; menu compact CER0.00% versus58.87% for fixed
  whole-crop Tesseract PSM6. Disk-load Qwen1.65% reflects two editorial bracket
  differences. References sealed before alternate OCR; no repeated paid correction.
  Paid-cost evidence remains observational and mixed, not a proven routing win.
- Retained source anomalies; explicitly marked triplet-notation substitutes and
  boxed placeholder, with scan links. No program repair or execution claims.
- Integrity, UTF-8 ranges, coverage,14-row menu, partial-page accounting, deferred
  hex exclusion and byte-identical rebuild checks passed. All seven exports valid.
  Five complete bodies,one partial;20 represented pages (19 complete for selected
  article bodies),285 regions,262 text regions,23 images,207 logical BASIC lines,
  59 review flags.37 entries unfinished,36 untouched; human acceptance pending.
- Reading room unchanged; user homepage edit retained. Carry this reporting/commit
  tail into the next cumulative token audit.

### Full July restoration goal activated, 2026-10-11

- Restore every remaining article body, consolidate time/paid-token metrics, then
  build and verify a reading-room preview for mandatory human review. The explicit
  goal authorizes that final build after restoration; earlier hold is superseded.
- Keep the routing rule provisional, immutable raw evidence and source-linked
  correction records. Classify six unpaginated TOC parent headings separately;
  all42 catalog entries remain accounted for, with36 paginated body candidates.
- Current work: music-card hex listing and full assembly. Then continue through
  remaining bodies in source order, inspecting actual boundaries and advertisements.

### July hex listing and music-card assembly completed, 2026-10-11

- Batch08/Qwen restores lower191 and192–194:75 crops,1,071 addressed hex rows,
  8,568 bytes,16 source-linked flags. Two omitted rows restored from source;
  printed5728–5FFF gap retained. Byte accuracy and execution remain unverified.
- Raw833.14s, recognition807.55s, startup1.26s; correction/recording913.35s.
  Correction usage:134,999 uncached input,3,691,648 cached input,24,424 output;
  zero cache-write. Local Qwen59,727 tokens separately recorded. Raw and correction
  overlap by about183s; shared assembler development during raw monitoring is
  explicitly labelled. Preparation rejection and assembly verification-call error
  retained in costs; no inference retries or duplicate paid correction.
- Four preselected identical-PNG hex samples: pooled compact CER2.38% Qwen versus
  46.51% Tesseract. Supports provisional raw-quality routing, not paid-cost savings
  or human-gold/byte-perfect accuracy; substantial source-checking work remains.
- Full music-card assembly combines immutable batches06–08 across PDF184–194:
  199 regions,14 figures,40 flags. Explicit shared-page geometry/exclusion handling
  preserves both parts of191 and original source exclusions. Ninety targeted tests
  passed; export integrity, all review byte ranges and byte-identical rebuilds pass.
- July:6 complete bodies,30 remaining;6 unpaginated parent headings separately
  classified, all42 TOC entries accounted for.23 source pages,360 regions,
  337 text crops,23 figures,207 BASIC lines,1,071 hex rows,75 flags. Human review
  pending. Reading room awaits full restoration and metric consolidation.
- Next: Z-80 feature, candidatePDF21–38, Qwen for dense technical notation;
  detailed mapping and preselected samples still required. User homepage edit
  retained. Carry reporting/commit tail into the next cumulative usage audit.

### July Z-80 opening restored, 2026-10-11

- Batch09/Qwen restores PDF21–26/printed17–22, opening and sections1–3:
  77 regions,68 text crops,nine original diagrams,14 source-linked flags.
  Remaining27–38 and full Z-80 assembly are still pending.
- Restored visible overbars, subscripts and cross-column/page prose joins. Retained
  printed S-RAM/5비트/16비트 inconsistencies and caption 비퍼; faint last subscript
  in A₀~A₆ remains a candidate for human confirmation. No technical repair/testing.
- Raw247.89s, recognition218.75s,startup1.26s; correction295.99s for6,340 characters.
  Correction tokens:25,450 uncached input,1,552,256 cached input,10,118 output;
  zero cache-write. Local Qwen38,645 tokens separate. Raw/correction overlap181.49s;
  preserve separate engine and assistant clocks. No inference retries.
- Four fixed crops favor Qwen raw text, with small margins on ordinary prose.
  Memory-signal Qwen13.25% CER comprises20 dropped overbars and two quote-style
  differences; base letters match. References sealed before alternate Tesseract;
  no repeated paid correction, human-gold or paid-savings claim.
- Integrity, correction byte ranges and byte-identical rebuild passed. July totals:
  6 complete bodies,1 partial,29 untouched;29 source pages,437 regions,405 text,
  32 figures,207 BASIC lines,1,071 hex rows,89 flags. Human review pending.
- Next: map Z-80 CPU control/interrupt material27–32, then33–38 and assemble.
  Reading room after full restoration/metrics. Homepage edit remains untouched;
  carry final reporting/commit tail into next cumulative usage audit.


### July Z-80 CPU control and interrupts restored, 2026-10-11

- Batch10/Qwen restores PDF27–32:82 regions,75 text crops,7 figures,16 flags.
  Source inconsistencies and uncertain small glyphs remain explicit for review.
  The final summary point continues on33; full article assembly is still pending.
- Raw313.01s, recognition281.76s; correction491.75s for8,731 characters.
  Correction tokens:208,143 uncached input,2,287,744 cached input,13,186 output;
  zero cache-write. Local46,025 tokens separate. Raw/correction overlap223.32s.
  Exact-edit helper preparation and interruption timing limits are documented.
- Four fixed raw comparisons favor Qwen; first two Qwen errors are entirely
  missing overbars. No independent human gold, duplicate paid correction or
  causal paid-savings claim. Integrity, review ranges and rebuild checks pass.
- July:6 complete bodies,1 partial,29 untouched;35 source pages,519 regions,
  480 text crops,39 figures,207 BASIC lines,1,071 hex rows,105 flags. Human review
  pending. Next:33–38, then assemble Z-80. Reading room after full issue/metrics.
  User homepage edit preserved; final reporting/commit usage carries forward.


### July Z-80 complete article assembled, 2026-10-11

- Batch11/Qwen restores final33–38:77 regions,67 text crops,10 original images,
  16 flags. Historical printed anomalies retained with source-linked review notes.
- Raw160.07s, recognition132.76s; correction225.33s for5,862 characters.
  Correction usage19,574 uncached input,748,544 cached input,6,660 output;
  zero cache-write. Local34,093 tokens separate. Raw/correction overlap100.93s.
  One crop seam adjusted before inference;67 fresh inferences, no retries.
- Fixed four-sample comparison favors Qwen; its only errors are15 omitted overbars
  in one crop. Human-gold and causal paid-savings claims remain unsupported.
- Full Z-80 assembly combines09–11 across21–38:236 regions,26 images,46 flags.
  Explicit interrupted prose join completes the32/33 summary. Native and assembled
  export integrity, all source-linked UTF-8 review ranges and reproducible rebuilds
  pass. Original segments unchanged; mandatory human review remains pending.
- July:7 complete bodies,29 untouched;41 pages,596 regions,547 text crops,
  49 figures,207 BASIC lines,1,071 hex rows,121 flags. Next inspect Apple sound
  article candidate42–50, then map with provisional routing. Reading room after
  full issue restoration/metrics. User homepage change left untouched.


### July Apple sound opening restored, 2026-10-11

- Source extent42–49 confirmed;50 is advertisement. Batch12/Qwen restores42–45:
  49 regions,44 text crops,5 images,7 BASIC lines,58 assembly rows,12 flags.
  Preserve source anomalies, explicit circled-step linearization and margin mark.
- Worker exit143 after30 completed crops and one incomplete request; cause unknown.
  Original output preserved, verified30 crops reused, remaining14 completed in56.13s.
  Combined raw elapsed is bounded161.77–283.81s, exact value null. Successful
  recognition132.66s and local22,498 tokens exclude incomplete inference cost.
- Correction/recovery351.17s;21,392 uncached input,1,797,504 cached input,
  8,913 output tokens, zero cache-write. No exact overlap or pure correction claim.
- Four fixed comparisons favor Qwen, with larger gaps on assembly than prose;
  $/# and0/O errors still require source review. No human-gold or causal savings claim.
- Native integrity, UTF-8 review ranges, row/address audit and reproducible rebuild
  pass. July:7 complete,1 partial,28 untouched;45 pages,645 regions,591 text,
  54 figures,214 BASIC lines,1,071 hex rows,58 assembly rows,133 flags.
- Next:46–49, then full Apple sound assembly. Full reading room remains scheduled
  after issue restoration and metric consolidation. User homepage change preserved.


### July Apple sound complete, 2026-10-11

- Batch13 restores46–49:67 regions,65 text crops,2 images,90 BASIC lines,
  26 assembly rows,72 numeric table values and20 flags. Original musical symbols
  retained with labeled editorial descriptions; routing guidance updated.
- Qwen symbol repetition hit4,096 tokens. Failure and both raw attempts retained;
  changed map caused22 repeated crops. Raw487.29s; successful recognition309.52s;
  failed server compute123.20s has a separate timer basis. Local53,376 tokens
  include failure/repetition. No duplicate paid semantic correction.
- Correction/recovery738.71s;34,096 uncached input,4,158,848 cached input,
  17,370 output tokens. Raw overlap419.66s. Four fixed comparisons favor Qwen,
  but references are unblinded and paid savings remain unproven.
- Full42–49 assembly passes integrity, review ranges, exact source listing bytes
  and byte-identical rebuild. Private wrapped-row metadata fixed during reporting;
  article/listing bytes preserved. Full article:116 regions,7 images,32 flags,
  97 logical BASIC lines and84 assembly rows. Human review pending.
- July:8 complete bodies,28 untouched;49 pages,712 regions,656 text crops,
  56 images,304 BASIC lines,1,071 hex rows,84 assembly rows,153 flags.
  Next inspect candidate56–58. Reading room after full restoration/metrics.
  User homepage edit remains untouched; final reporting/commit usage carries forward.


### July FC-100 rebellion game restored, 2026-10-11

- Batch14 restores complete PDF56–58:50 regions,49 text crops,1 image,
  170 numbered BASIC lines/195 physical rows,112 hex DATA values and21 flags.
  Source spelling/errors retained; graphics use explicit scan-linked ⟦G⟧ markers.
- Qwen bracket repetition reached4,096 tokens after44 completed crops. Preserved
  failed evidence; reused44 verified stages, inferred4 remaining, used Tesseract
  for1 crop. No repeated successful inference or duplicate paid correction.
- Raw328.45s; successful Qwen182.24s; fallback0.15s. Failed server compute125.43s
  is a separate basis. Local33,544 tokens include failure. A successful Qwen crop
  silently omitted9 numbered rows; all restored by source review and flagged.
- Correction/recovery/helper work490.10s;56,553 uncached input,2,055,424 cached
  input,14,224 output tokens, zero cache-write. Raw overlap292.12s.
- Four fixed samples favor Qwen; they exclude graphic placeholders and the omitted
  crop. No human-gold, whole-article accuracy or paid-savings claim. Coverage-check
  guidance added to routing rule. Export/review ranges/reproducible rebuild pass.
- July:9 complete,27 untouched;52 source pages,762 regions,705 text crops,
  57 images,474 BASIC lines,1,071 hex rows,84 assembly rows,174 flags.
  Next inspect59–61. Full restoration, metric consolidation and reading room remain.
  Homepage edit untouched; final reporting/commit usage carries into next audit.


### July sixth-sense game restored with planned mixed routing, 2026-10-11

- Batch15 completes PDF59–61:30 text regions,97 BASIC lines,11 review flags.
  Preassigned10 Tesseract prose/byline crops and20 Qwen title/definitions/code crops;
  native evidence for both engines retained. No retries or fallback.
- Raw72.36s; recognition Tesseract2.96s/Qwen57.03s. Correction/coverage checks176.10s,
  overlap37.87s. Usage17,475 uncached input,681,472 cached input,5,479 output,
  zero cache-write. Local Qwen11,623 tokens separate; no per-engine paid attribution.
- Two Qwen responses silently omitted tails of150/710 and full720–800 rows;
  restored from source. PROGARM and printed wording retained. All97 rows checked.
- Four fixed comparisons favor Qwen; clean-code gaps smaller than prior graphic
  game. No independent gold, whole-article score or causal savings claim.
  Export integrity, review ranges and byte-identical rebuild pass.
- July:10 complete,26 untouched;55 pages,792 regions,735 text crops,57 images,
  571 BASIC lines,1,071 hex rows,84 assembly rows,185 flags. Human review pending.
  Next inspect62–67. Full restoration/metrics/reading room remain outstanding.
  Homepage edit untouched; final reporting/commit usage carries into next audit.


### July Dodgem game restored after interruption, 2026-10-11

- Batch16 completes PDF62–67/printed58–63:39 text regions,307 BASIC rows,
  19 review flags. Planned5 Tesseract prose/byline and34 Qwen headline/code crops;
  PDF63 advertisement excluded. Original spelling/program anomalies retained.
- Raw process ended143 after29 Qwen crops; preserved interrupted request and reused
  all completed Qwen and5 Tesseract results. Five remaining Qwen calls completed.
  Raw elapsed bounded196.14–405.53s; resume31.23s; completed Qwen recognition167.84s.
  Original Tesseract timers and interrupted Qwen duration/tokens unavailable, not zero.
- Correction/recovery window458.21s includes helper work and interruption delay;
  not pure proofreading time.80,418 uncached input,1,922,560 cached input,12,735
  output tokens. Local31,824 completed-call tokens separate; no causal savings claim.
- Source check restored ten whole omitted lines and two partial tails from successful
  Qwen responses. All307 source line identities checked. Four fixed comparison crops
  favor Qwen but exclude those omissions; no whole-article accuracy claim.
- Export integrity, review ranges and byte-identical rebuild pass. July:11 complete,
  25 untouched;61 pages,831 regions,774 text crops,57 images,878 BASIC rows,
  1,071 hex rows,84 assembly rows,204 flags. Human review pending.
- Next inspect 위기일발, candidate70–72. Persist recognition timers per crop in
  subsequent mixed runs. Full issue/metrics/reading room remain; homepage edit
  untouched. Final report/commit usage carries into the next audit.


### July 위기일발 restored, 2026-10-11

- Batch17 completes PDF70–72/printed66–68:45 regions,44 text crops,1 opening
  image,127 logical BASIC lines/231 physical rows and20 review flags.
  Planned5 Tesseract prose/byline and39 Qwen technical/title/code crops.
- Raw190.48s; recognition Qwen168.12s/Tesseract1.33s. Per-crop timers now
  persisted immediately; no retry or fallback. Local23,275 completed-call tokens.
- Correction/source DATA audit/helper window396.10s;32,098 uncached input,
  1,465,600 cached input,10,149 output tokens. Raw overlap176.30s; shared paid
  window cannot attribute causal cost to either engine. Cache-write zero.
- All127 line identities and231 physical rows checked, including cross-page660.
  Qwen omitted a one-character1130 continuation; restored.24 DATA lines contain
  379 literal comma-separated fields; source21- and1.2 retained with flags.
  Faint punctuation/source anomalies remain reviewable; no execution.
- Four fixed crops favor Qwen, most strongly on faint BASIC (0% vs67.38% compact
  CER). Unblinded references and fixed sample selection do not prove whole-article
  accuracy or paid savings. Export/review ranges/byte-identical rebuild pass.
- July:12 complete,24 untouched;64 pages,876 regions,818 text crops,58 images,
  1,005 BASIC lines,1,071 hex rows,84 assembly rows,224 flags. Human review pending.
  Next inspect remaining 화성인 디거73–77 and boundary78. Full issue/metrics/
  reading room remain outstanding. Homepage edit preserved; final usage carries forward.


### July 화성인 디거 restored, 2026-10-11

- Batch18 completes PDF73–77:58 regions,57 text crops,1 opening artwork,
  141 BASIC lines/383 physical BASIC rows,36 hex rows/288 byte fields,
  2 monitor-command rows and26 review flags. Page77 advertisement excluded.
  Planned7 Tesseract clear prose/byline and50 Qwen technical/code crops.
- Two raw processes ended143, cause unknown. Preserved both incomplete requests;
  reused5 then9 completed Qwen stages and all7 Tesseract outputs/timers.
  Final resume completed41 remaining calls. No completed inference repeated.
- Raw bounded285.22–489.62s; final resume228.38s. Completed recognition Qwen252.73s,
  Tesseract1.68s. Local34,133 completed-call tokens; interrupted costs unknown.
- Correction/recovery/source review/helper window855.57s;59,909 uncached input,
  3,865,856 cached input,21,970 output tokens. Cache-write zero. Raw overlaps;
  this interruption-affected observation does not isolate engine cost or savings.
- Source700 has an explicit unreadable span, not inferred code. Qwen omitted760–800
  and a wrapped0; source-restored. Hex digit/address errors corrected with faint-byte
  flags. Source typos, monitor401F/end411F mismatch and padding uncertainty retained.
- Four fixed crops favor Qwen, including hex3.17% vs93.65% compact CER. References
  remain unblinded and omit the silent-omission/damaged700 cases. Export integrity,
  listing/review ranges and byte-identical rebuild pass; no execution/human acceptance.
- July:13 complete,23 untouched;69 pages,934 regions,875 text crops,59 images,
  1,146 BASIC lines,1,107 hex rows,84 assembly rows,250 flags. Next inspect79–81
  for 보트 탐험 (start78 confirmed). Full issue/metrics/reading room remain.
  Homepage edit preserved; final report/commit usage carries forward.


### July 보트 탐험 restored, 2026-10-11

- Batch19 completes78–80:43 regions,42 text crops,1 screen image,87 logical
  BASIC lines/166 physical rows,7 DATA lines/84 hexadecimal fields and24 flags.
- Planned17 Tesseract/25 Qwen crops; no retry. Graphic-heavy BASIC preassigned to
  Tesseract to avoid prior symbol repetition, but adjacent code needed extensive
  source repair. Exception remains unproven and is qualified in the routing rule.
- Raw87.10s; recognition Qwen68.58s/Tesseract2.53s. Correction/helper window270.59s,
  overlapping raw by74.23s.32,192 uncached input,570,624 cached input,8,876 output
  tokens; cache-write zero. Local13,237 Qwen tokens separate; no causal savings claim.
- Source graphic strings retain explicit scan-linked ⟦G⟧ markers; exact bytes and
  literal padding unresolved. Faint2200 character marked unreadable. Qwen's omitted
  numbered header and final-page number errors corrected; original typos retained.
- Four fixed samples favor Qwen, but exclude graphic-marker regions and main
  omission cases. Unblinded CER cannot rank whole-article accuracy or paid cost.
  Export/review ranges and byte-identical rebuild pass; mandatory human review pending.
- July:14 complete,22 untouched;72 pages,977 regions,917 text crops,60 images,
  1,233 BASIC lines,1,107 hex rows,84 assembly rows,274 flags. Next inspect 캥거루
  candidate81–86 and boundary87. Full issue/metrics/reading room remain outstanding.
  Homepage edit preserved; final report/commit usage carries forward.


### July 캥거루 restored, 2026-10-11

- Batch20 completes81–86:79 regions,78 text crops,1 screen,246 BASIC lines/556
  physical text/glyph rows,90 numeric DATA fields,420 CHR$ hex fields,55 flags.
- Planned4 Tesseract/74 Qwen crops. Seven page83 right-column crops widened after
  detecting trimmed numerals; original evidence archived and only those7 rerun.
  Reused67 Qwen/4 Tesseract results; no repetition loop or process interruption.
- Worker elapsed349.27s+43.30s=392.56s; all81 Qwen calls354.51s and4 Tesseract
  calls1.02s. Local53,453 tokens across both crop versions. No discarded attempt cost.
- Correction/source/crop-repair/helper window739.79s overlaps raw371.43s.76,443
  uncached input,2,871,936 cached input,22,452 output tokens; zero cache-write.
  Mixed observation and larger listing cannot establish causal engine savings.
- Source checks restored omitted BASIC lines and repeated CHR$ terms. Graphic
  literals remain scan-linked markers; original spelling, apparent syntax defects,
  faint numeric readings and exact padding require human review. No execution.
- Four fixed samples favor Qwen, but exclude major omissions/graphic cases.
  Export integrity, listing/review byte ranges and byte-identical rebuild pass.
- July:15 complete,21 untouched;78 pages,1,056 regions,995 text crops,61 images,
  1,479 BASIC lines,1,107 hex rows,84 assembly rows,329 flags. Next inspect automatic
  SPC-1000 tape article88–93/boundary94. Full issue/metrics/reading room remain.
  Homepage edit preserved; final report/commit usage carries forward.


### July SPC-1000 automatic tape article restored, 2026-10-11

- Batch21 completes88–92:104 regions,99 text crops,5 diagrams/screens,5 BASIC
  rows,13 hex rows/104 fields,13 assembly rows,2 patch rows and21 review flags.
  Page93 is a section divider;94 starts 로고강좌.
- Planned20 Tesseract/79 Qwen crops; no retry, fallback or crop change. Raw234.73s;
  recognition Qwen205.35s/Tesseract2.51s. Local37,874 tokens counted separately.
- Correction/helper window446.36s overlaps raw198.12s.64,113 uncached input,
  1,009,920 cached input and15,089 output tokens; zero cache-write. No causal
  per-engine paid savings estimate.
- Restored assembly row association and circled tape labels; original1482 heading,
  C1 mode, figure metadata, repeated step9 and G0024 load instruction retained.
  Source anomalies and exact literals remain human-review items; no execution.
- Fixed samples split: Tesseract better on prose/assembly order; Qwen better on
  numeric table/hex. Routing guidance now calls out assembly column checks and
  plausible normalization. Unblinded sample CER does not rank whole articles.
- Export integrity, review/listing byte ranges and byte-identical rebuild pass.
  July:16 complete,20 untouched;83 pages,1,160 regions,1,094 text crops,66 images,
  1,484 BASIC lines,1,120 hex rows,97 assembly rows,350 flags. Next inspect94–98.
  Full issue restoration, final decision metrics and reading room remain outstanding.
  Homepage edit preserved; final report/commit usage carries forward.


### July 로고강좌 restored, 2026-10-11

- Batch22 completes94–97:80 regions,77 text crops,3 original graphics,29 Logo
  procedure rows plus5 console/command rows and21 review flags.98 is next article.
- Planned9 Tesseract/68 Qwen crops. Exit143 after46 Qwen successes; verified terminal
  before resuming22 crops. All9 Tesseract outputs/timers and completed Qwen stages
  reused. Interrupted request archived; unfinished duration/tokens remain unknown.
- Raw bounded181.71–245.05s; completed recognition Qwen154.38s/Tesseract1.41s.
  Local31,357 completed tokens. Correction/recovery/helper window308.71s overlaps
  raw149.38–212.72s.32,045 uncached input,1,545,088 cached input,8,641 output;
  zero cache-write. Final wrap correction/export rebuild recorded separately.
- Original Logo spellings/values retained; Qwen's added closing quote, identifier
  splitting, paraphrase and modernized Korean wording source-corrected. No execution.
- Four fixed samples favor Qwen, with Tesseract close on typeset code. Unblinded
  samples cannot establish whole-article accuracy or causal paid-token savings.
- Final export integrity, source row counts, review/listing ranges and byte-identical
  rebuild pass. July:17 complete,19 untouched;87 pages,1,240 regions,1,171 text
  crops,69 images,1,484 BASIC lines,1,120 hex rows,97 assembly rows,29 Logo rows,
  371 flags. Next inspect98–101. Full issue/metrics/reading room remain outstanding.
  Homepage edit preserved; final report/commit usage carries forward.


### July 샤를의 법칙 restored, 2026-10-11

- Batch23 completes98–100:49 regions,46 text crops,3 diagrams,57 BASIC lines/
  107 physical rows and23 review flags.101 begins CP/M 입문.
- Planned7 Tesseract/39 Qwen crops; no retry, fallback, crop change or missing
  numbered rows observed. Raw136.66s; recognition Qwen120.44s/Tesseract0.90s.
  Local19,780 tokens separate from paid assistant usage.
- Correction/source/helper window292.59s overlaps raw89.35s.19,588 uncached input,
  1,296,128 cached input and8,777 output tokens; zero cache-write. No causal savings.
- Source HPLOT/colons/Hangul restored. Printed prose/legend inconsistencies retained;
  faint4040 mark, historical prompt spelling, zero/O and exact padding remain flagged.
  No executable or byte-perfect claim; mandatory human review pending.
- Four fixed samples favor Qwen. Tesseract uses eng on code, limiting interpretation
  of the Korean-string sample. Unblinded CER is not a whole-article accuracy score.
- Export integrity, explicit line identities, review/listing byte ranges and
  byte-identical rebuild pass. July:18 complete,18 untouched;90 pages,1,289 regions,
  1,217 text crops,72 images,1,541 BASIC lines,1,120 hex rows,97 assembly rows,
  29 Logo rows,394 flags. Next inspect CP/M101–119. Full goal remains unfinished.
  Homepage edit preserved; final report/commit usage carries forward.


### July CP/M opening raw checkpoint, 2026-10-11

- Confirmed CP/M 입문 spans PDF101–113;114–118 are advertisements.
  First segment101–106 has142 mapped regions:139 text crops and3 preserved figures.
- Raw OCR complete using the preassigned routing rule:125 Qwen and14 Tesseract
  regions. Semantic correction, fixed-reference comparison and article export remain
  pending; the issue stays at18 complete article bodies and zero human acceptances.
- A process-name check missed the live original worker. A premature recovery
  archived one in-flight request; the original worker completed all recognition but
  export then lacked that request. Reconstructed its evidence from the preserved
  original request and response, retained both prior stage versions, and verified
  all125 stage hashes before re-export. No completed OCR inference was rerun.
- Exclude this batch's elapsed wall time from clean speed comparisons: the mistaken
  recovery, second server startup and evidence repair contaminated it. Private
  `batch-24/recovery-correction.json` supersedes the initial interruption diagnosis.
  Raw evidence-bundle manifest SHA-256: `a5da489e2352715ac82e8283effc65944a825b1bb969fbebd4400bf537f0da9a`.
- Next: source-based correction of101–106, then107–113 and full CP/M assembly.
  Final issue metrics and reading-room work remain outstanding.


### July CP/M opening corrected, 2026-10-11

- Batch24 exports101–106 of the verified101–113 article:142 regions,139 text,
  3 figures,47 console/comment/assembly rows including3 assembly statements,33 flags.
- Fixed14 Tesseract/125 Qwen route; all four comparison22 samples favor Qwen.
  Mottled-background prose is now an explicit routing consideration. Source
  power-off wording, historical vocabulary and physical comment rows restored.
  Original technical anomalies retained, mandatory human review pending.
- Raw wall time excluded after mistaken recovery and evidence repair. Recognition
  Qwen234.81s/Tesseract1.87s and46,426 local tokens retained as affected-run
  observations. Correction233.71s;35,291 uncached/620,800 cached input and8,369
  output tokens. No causal paid savings or clean speed claim.
- Export/review/listing integrity and byte-identical rebuild pass. July18 complete,
  1 partial,17 untouched;96 pages,1,431 regions,1,356 text,75 figures,427 flags.
  Next107–113 and CP/M assembly; full restoration/metrics/reading room outstanding.
  Homepage edit preserved; final report/commit usage carries forward.


### July CP/M fully assembled, 2026-10-11

- Batch25 completes107–113:203 regions,199 text crops,4 images,102 console rows
  including9 assembly statements and38 flags.13 Tesseract/186 Qwen crops; no retry.
- Raw407.91s; recognition Qwen343.68s/Tesseract0.86s;68,540 local tokens.
  Correction362.22s overlaps292.09s;20,537 uncached/1,570,688 cached input and
  11,104 output tokens. Separate assembly/evaluation/reporting; no causal savings.
- Qwen TEMP.COM restored to source TEMP.$$$; extra/omitted comment rows/markers
  corrected. Damaged source fragments explicitly marked, original command anomalies
  retained. Four comparison23 samples favor Qwen; unblinded references remain limited.
- Full101–113 CP/M assembly:345 regions,7 figures,149 physical listing rows,
  12 assembly statements,71 flags. Immutable source bytes/review ranges and
  byte-identical rebuild pass.106/107 joins in one block with original newline retained.
- July19 complete,17 untouched, no partial bodies, zero human acceptances;103 pages,
  1,634 regions,1,555 text crops,79 images and465 flags. Next inspect119–129.
  Full restoration/metrics/reading room remain outstanding; homepage edit preserved.
  Batch24 timing exclusions persist; final reporting/commit usage carries forward.


### July Z80 lesson opening restored, 2026-10-11

- Batch26 covers119–123 of verified119–127;128 next article title,129 body.
  104 regions,100 text,4 figures,50 assembly/example rows,29 flags.
- Planned2 Tesseract/98 Qwen crops, no retry. Raw262.40s; recognition220.34s/0.13s;
  38,948 local tokens. Correction329.46s overlaps183.76s;18,826 uncached input,
  2,038,784 cached input and9,783 output tokens. No causal paid savings claim.
- Qwen ORG/address alignment failure and lost LD B,26D source-corrected. Printed
  arithmetic contradictions, missing parenthesis and blank final mnemonic retained.
  Comparison24 split: Qwen prose/assembly, Tesseract arithmetic layout; divider/arrow
  representation affects CER. Mandatory human review pending.
- Export/review/listing ranges and byte-identical rebuild pass. July19 complete,
  1 partial,16 untouched;108 pages,1,738 regions,1,655 text,83 images,494 flags.
  Next124–127 and full lesson assembly. Full goal unfinished; homepage edit preserved.
  Final report/commit usage carries forward.


### July Z80 lesson fully assembled, 2026-10-11

- Batch27 completes124–127:122 regions,3 images,32 opcode rows,37 listing rows,
  32 flags. Both complete opcode tables retained beside transcriptions; damaged
  result expression/address digit unresolved, original errors preserved.
- Two Qwen4096-token loops led to two Tesseract fallbacks and17 unattempted opcode
  rows rerouted. Final25 Tesseract/94 Qwen; no completed inference repeated.
  Recognition181.82s/3.12s plus249.79s failed server compute;42,668 local tokens
  include failures. Raw434.72–572.22s broad bound includes recovery preparation
  in its upper bound; exclude from clean speed comparisons.
- Correction580.19s with545.37s raw-wall overlap;51,734 uncached/1,870,720 cached
  input and17,558 output tokens. Four comparison25 samples favor Qwen; table CER
  is typography-sensitive, ADC HL alternate has512-token cap. No causal savings.
- Full119–127 assembly226 regions,7 images,87 assembly/example rows and61 flags.
  Immutable source listing bytes, review ranges and byte-identical rebuild pass.
- July20 complete,16 untouched, no partials;112 pages,1,860 regions,1,774 text,
  86 images,526 flags, zero human acceptances. Next inspect graphics128 onward.
  Full restoration/final metrics/reading room outstanding; homepage edit preserved.
  Final reporting/commit usage carries forward.


### July computer graphics complete, 2026-10-11

- Full128–134 restored;135–136 advertisements,137 Apple FORTRAN.167 regions,
  9 images,135 BASIC lines/154 physical rows,45 DATA records and37 flags.
- Color-table Qwen escaped-tab loop reached4096 tokens. One fallback plus two
  unattempted ruled tables rerouted: final13 Tesseract/145 Qwen.24 completed Qwen
  stages reused; no completed inference repeated. Ruled tables now merit a bounded
  Tesseract probe before committing the group to Qwen.
- Raw505.01s includes both measured attempts; successful recognition311.72s/1.40s,
  failed server compute123.76s,58,306 local tokens including failure. Correction
  611.12s overlaps448.63s;33,307 uncached/2,410,496 cached input and18,964 output.
  Helper/recovery and content differences confound causal paid-cost comparisons.
- Seven isolated I/0 continuations, DATA column associations/values, HPLOT and
  decimal errors source-corrected. Original numbering, prose/code discrepancies
  and provisional punctuation retained. Four comparison26 samples favor Qwen;
  their unblinded CER excludes the primary table failure and omitted continuations.
- Complete export, review/listing ranges,135 numbered-line counts and byte-identical
  rebuild pass. July21 complete,15 untouched, no partials;119 pages,2,027 regions,
  1,932 text,95 images,563 flags, zero human acceptances. Next Apple FORTRAN137.
  Final issue metrics/reading room outstanding; homepage edit preserved. Final
  reporting/commit usage carries forward.


### July Apple FORTRAN complete, 2026-10-11

- Full137–142 restored:123 regions,109 text crops,14 images,73 FORTRAN source
  rows/115 physical listing rows,80 numeric cells and31 flags. Next Information
  Radar143–157; inspect opening143–147. Review Salon160–162 already restored.
- Two bounded Tesseract probes0.629s informed unchanged94Qwen/15Tesseract route:
  Qwen handwritten/compiler code, English Tesseract numeric output. All numbers
  source-checked; no inferred sorting/execution. Source COLUMMN and original
  technical/typographical errors retained; faint screen3 explicitly unresolved.
- Exit143 interrupted one request after70 complete Qwen crops; reused all70,
  no completed inference repeated. Raw232.60–355.95s broad bound, not a clean
  speed sample. Recognition200.65s/1.51s;38,558 local completed-response tokens
  are a lower bound because interrupted response usage was not captured.
- Correction515.16s overlaps215.62–338.97s of bounded raw time;53,873 uncached/
  1,621,888 cached input and14,764 output. Recovery/helper/content confounding
  remains. Four comparison27 crops favor Qwen; no causal paid-cost conclusion.
- Export/review/listing integrity, explicit row/cell counts and byte-identical
  rebuild pass. July22 complete,14 untouched,no partials,zero human acceptances;
  125 unique pages,2,150 regions,2,041 text,109 images,594 flags. Final issue
  metrics/reading room outstanding; homepage edit preserved. Final report/commit
  usage carries forward.


### July Information Radar domestic section restored, 2026-10-11

- Batch30 restores143–148/printed139–144 of verified143–157:152 regions,
  145 text,7 images,16 news items plus1 notice,21 table cells and31 flags.
  Internal column/page continuations joined; duplicate notice bullet retained.
- Planned108 Tesseract/37 Qwen crops; table probe reused as primary after hash
  check, no duplicate inference/retry/fallback. Raw worker128.97s; recognition
  87.35s/15.28s, latter includes0.205s probe incurred during setup.14,901 local
  Qwen tokens. Probe cost counted once, not added again to primary recognition.
- Correction418.06s overlaps109.52s;24,299 uncached/1,505,792 cached input and
  13,093 output. Content and helper work confound per-engine paid-cost claims.
  All four comparison28 samples favor Qwen; Tesseract clear-news/table routes
  remain cost experiments. Blank/fragmented ruled headings were source-restored.
- Export/review ranges, table counts, domestic coverage and byte-identical rebuild
  pass. July22 complete,1 partial,13 untouched;131 unique pages,2,302 regions,
  2,186 text,116 images,625 flags,zero human acceptances. Next foreign news149–157,
  candidate149–153 first, then full article assembly. Issue metrics/reading room
  remain outstanding. Homepage edit preserved; final report/commit usage carries.

### July Information Radar foreign opening restored, 2026-10-11

- Batch31 restores149–153/printed145–149:156 text regions,13 complete news items
  and one partial GaAs SISFET item,37 review flags. No figures or tables. Restore
 154–157 next, then assemble143–157; source153 ends mid-word at 순.
- Planned39 Tesseract/117 Qwen. Rejected Tesseract headline probe0.119s is extra
  preparation cost. SIGTERM after78 saved Qwen crops; all reused unchanged, no
  duplicated successful inference or route change. Both worker lifespans measured:
  raw300.41s; successful recognition259.36s Qwen/5.07s Tesseract. Local47,950
  completed-response tokens are a lower bound; interrupted request usage unknown.
- Correction/source/recovery/helper work692.44s overlaps232.21s of raw. Paid
  observations70,124 uncached/2,768,128 cached input and20,299 output; no causal
  per-engine attribution. Four comparison29 crops favor Qwen; boxed headline
  still required two source corrections. Faint decimal points and original
  chip-number/quantity contradictions remain flagged, without factual repair.
- Export integrity, full regional coverage, explicit joins, UTF-8 review ranges
  and byte-identical rebuild pass. July22 complete,1 partial,13 untouched;
  136 unique pages,2,458 regions,2,342 text,116 images,662 flags. Human acceptance
  remains pending. Reading-room build awaits full restoration and metrics;
  preexisting homepage edit preserved. Final reporting/commit usage carries.

### July Information Radar complete, 2026-10-11

- Batch32 restores154–157:118 regions,117 text,one diagram,32 flags; six new news
  items and the GaAs conclusion. Full143–157 assembled from30–32:426 regions,
  418 text,8 images,36 news items plus one notice,21 table cells and100 flags.
- Planned52 Tesseract/65 Qwen. SIGTERM after48 saved Qwen crops; all reused,
  no successful crop repeated or route changed. Measured raw attempts181.76s,
  Qwen recognition142.28s/Tesseract8.93s. Local26,183 completed-response tokens
  are a lower bound; interrupted request usage remains unknown.
- Correction295.86s overlaps98.56s of raw;27,734 uncached/1,015,040 cached input
  and8,494 output. Assembly75.92s separately recorded. Four comparison30 samples
  favor Qwen, with Lisp specs close; typography affects CER. No causal cost claim.
- Original onrmal, Compag, inconsistent product names, source duplication and
  technical claims retained. Export/review ranges, full coverage,153/154 join
  and byte-identical assembly rebuild pass.158 is a publisher book advertisement.
- July23 complete,13 untouched,no partial bodies;140 unique source pages,
  2,576 regions,2,459 text,117 images,694 flags,zero human acceptances. Next
  VISICALC candidate164–168, extent still to verify. Final issue metrics and
  reading-room build remain pending; homepage edit preserved. Usage tail carries.

### July VISICALC/VISIPLOT complete, 2026-10-11

- Full164–168 restored;169 starts data structures.135 regions,122 text,13 images,
  116 physical command/annotation rows,63 numeric table cells and35 review flags.
  Ten charts, spreadsheet, equation and cursor-key diagram preserved as images.
- Planned29 Tesseract/93 Qwen. English T table probe0.333s badly corrupted dot-
  matrix text and values, so Q selected. Probe reused only as the fixed alternate,
  with no second table T call. Q table values all63 match the source, but row/
  column coordinates and reading layout needed restoration.
- One SIGTERM after41 saved Qwen crops; all reused, no route change or successful
  crop repeated. Measured raw209.27s; successful recognition176.49s Q/3.14s T.
  Local35,535 completed-response tokens are a lower bound; interrupted cost unknown.
- Correction456.13s overlaps197.43s;23,657 uncached/1,964,672 cached input and
  12,556 output. Four comparison31 samples favor Qwen, with typography/coordinates
  affecting CER. No causal paid-cost claim. Commands remain unexecuted; original
  VISIPOLT, MATN/FOOD, LIVE and SERLES5 retained beside glyph/word review flags.
- Export,116 row counts,63 cells, complete coverage, UTF-8 ranges and byte-identical
  rebuild pass. July24 complete,12 untouched,no partials;145 unique source pages,
  2,711 regions,2,581 text,130 images,729 flags,zero human acceptance. Next data
  structures candidate169–174, final boundary still to inspect. Final metrics/
  reading room pending; homepage edit preserved and reporting usage tail carries.

### July data structures complete, 2026-10-12

- Full169–174/printed165–170 restored;175 starts UNIX.170regions148text22images,
  107 physical PL/I code/comment rows in10 procedures,36 review flags.16 diagrams
  and6 listing images preserve source geometry; code remains unexecuted.
- Planned38 Tesseract/110 Qwen. SIGTERM after59 saved Qwen crops; all reused.
  First resume stopped before new inference pending interrupted-stage archival;
  its4.793s startup is included. Three worker lifespans total266.105s, with no
  repeated successful inference or route change. Local40,625 completed tokens
  are a lower bound; interrupted response usage unknown.
- Correction501.76s overlaps256.40s of raw;58,866 uncached/1,321,856 cached input,
  14,301 output. Setup spans interrupted/status-only context, not clean active
  preparation. Four comparison32 samples: Qwen wins introduction and code;
  technical prose tie0%. Faint code reference provisional; no causal cost claim.
- Source CREAT, ADDS/DELETES, R(I)=Y, PL/A, missing declarations and duplicate
  prose retained. Faint LINK(R+I)) and DELETEQ glyphs flagged for human review.
- Full coverage,107 listing rows, UTF-8 review ranges and byte-identical rebuild
  pass. July25 complete,11 untouched,no partials;151 unique pages,2,881 regions,
  2,729 text,152 images,765 flags,zero human accepted. Next UNIX175–183 candidate,
  final boundary still to inspect. Full metrics/reading room pending; preexisting
  homepage edit preserved and final reporting/commit usage carries.

### July UNIX complete, 2026-10-12

- Final installment175–181/printed171–177 restored;182ad/183divider excluded.
  187regions178text9images,76 outline entries in77rows,7model/memorypairs36flags.
- Fixed80 Tesseract/98 Qwen. Initial pass completed; five page177 crops widened
  after clipped leading Hangul discovered.93 unchanged Q/80T reused; original
  maps/OCR and revised evidence retained. No failure or route change. Both raw
  passes225.644s; all103 local Q calls32,334tokens fully accounted.
- Correction496.41s overlaps189.18s raw;32,918 uncached/2,407,936 cached input,
  13,224 output. Export includes archived pre-evaluation reading-order revision.
  Four comparison33 samples favor Qwen; no causal paid-token savings claim.
- Source Entory, CEC, 비전, 유동소숫정 and technical claims retained; glyph
  ambiguities flagged. Table values/labels source-checked, no commands executed.
- Coverage, outline/table rows, UTF-8 review ranges and byte-identical rebuild
  pass. July26complete,10untouched,no partials;158unique pages,3,068regions,
  2,907text161images801flags,zero human accepted. Next hardware195–206candidate,
  exact extent unverified. Full metrics/reading room pending; preexisting homepage
  edit preserved. Final reporting/commit usage carries into the next audit.

### July hardware OCR recovery, 2026-10-12

- Verified tutorial extent: PDF195–206/printed191–202;207 starts the next article.
  Batch36 covers195–200:155 regions,140 text crops and15 retained source images.
- Kept the preassigned routing:32 Tesseract crops and108 Qwen crops. Initial
  worker exited143 during model loading, after all32 Tesseract crops completed.
  Resume reused those results; no completed inference repeated, no Qwen request
  interrupted. Raw evidence and recovery accounting remain private.
- Both measured worker lifespans total205.984s, excluding the recovery
  gap. Successful recognition: Qwen169.118s,
  Tesseract3.308s. Local Qwen usage:34,774 tokens
  (29,885 prompt/4,889 completion). These are raw-stage observations only.
- Hashes, request-image identity and exact140-text/15-image coverage pass. The
  READ-table heading/right edge is cut in the printed source, confirmed against
  its parent figure; no crop repair or inferred missing columns were introduced.
- Semantic correction, fixed-reference comparison, export and human review remain
  pending. Completed-body totals stay26/36; this raw checkpoint is not a restored
  article. Next correct195–200, then restore201–206 and assemble the tutorial.
  Paid usage carries into the next full audit; idle time is excluded from the
  interrupted correction window. Reading-room build remains deferred.

### July hardware opening reviewed, 2026-10-12

- Restored PDF195–200/printed191–196 as a partial checkpoint: 155 regions,
  140 text crops, 15 images, five KEY routine rows, three tables with 20 data
  rows/200 cells and 37 review flags. Full195–206 extent verified;201–206 remains.
- Fixed32T/108Q routing retained. Both raw workers total205.984s; Qwen169.118s
  and Tesseract3.308s successful recognition. All32T reused after startup-only
  interruption, no completed inference repeated. Local34,774 tokens are exact.
- Two correction windows total599.63s, overlapping raw by10.28s; interrupted
  window closes at last observed prior-session event and excludes the idle gap.
  Observed94,080 uncached/1,570,944 cached input and17,228 output tokens. These
  include source review/helper work and do not isolate engine-specific savings.
- Comparison34 favors Qwen on four compact-CER samples, but its table alternate
  silently returns8/10 rows and13/14 columns. Tesseract also badly damages that
  grid. Neither table output is safe without source structure/cell review.
- Retained printed keyboand/keyboud,6진, repeated captions, missing assembler
  punctuation and clipped READ-table edge; uncertain subscripts/cells flagged.
  Export coverage, UTF-8 ranges, five listing rows and byte-identical rebuild pass.
- July:26 complete,1 partial,9 untouched;164 unique pages,3,223 regions,
  3,047 text crops,176 images,838 flags,zero human acceptance. Next restore the
  monitor/listing pages201–206 and assemble the full tutorial. Full-issue metrics
  and reading room remain pending; final reporting/commit usage carries forward.

### July hardware tutorial complete, 2026-10-12

- Restored201–206 and assembled full195–206/printed191–202. Batch37 adds207
  regions,199 text crops,8 images,286 numbered monitor rows,2 LOOP rows,
  37 table rows/74 cells including one blank, and50 review flags.
- Full tutorial:362 regions,339 text crops,23 original images,293 physical listing
  rows (5 KEY +2 LOOP +286 monitor),57 table rows/274 cells and87 flags. Monitor
  pages appear in logical order205,206,203,204 with original provenance retained.
- Fixed29T/170Q, one complete raw run458.051s; Qwen422.771s/Tesseract2.731s
  recognition. Local64,169 tokens exact; no interruption, retry or fallback.
- Correction861.88s overlaps428.26s raw. Observed66,986 uncached/4,095,488 cached
  input and21,482 output tokens, including9,421 reasoning; zero cache-write.
  Source field/row reconstruction and helper work included; assembly separate.
- Comparison35: ordinary prose ties at0%; Qwen wins memory rows and both code
  samples. Native-column references avoid penalizing the export's STAT-first
  layout. Tiny206 code needed address/label/comment restoration despite low CER
  on its selected crop; printed/source uncertainties remain review items.
- Original program ends at the first PROM64 statement286. All printed rows are
  restored, but no executable or complete-program claim is made. CTINT, CASETTE,
  memory-map differences and provisional CHARACTER0BIT/row118 readings retained.
- Coverage, all1–286 numbers,293 listing rows, review ranges, immutable segments
  and byte-identical assembly rebuild pass. July27 complete,9 untouched,no partials;
  170 unique pages,3,430 regions,3,246 text crops,184 images,888 flags,zero human
  acceptance. Next contest commentary207–208candidate; ending still to inspect.
  Final full-issue metrics/reading room pending; reporting/commit usage carries.

### July contest commentary complete, 2026-10-12

- Full commentary207/printed203 restored.208 independent submission notice and
  209 Yut article visually verified; excluded from commentary.36text crops13flags.
- Fixed28T/8Q, single raw29.036s, no retry/fallback. Qwen15.027s/Tesseract3.827s
  recognition nested in raw;2,957local tokens exact (2,569prompt/388completion).
- Correction116.263s overlaps18.317s raw. Observed13,657uncached/266,624cached
  input and3,501output incl354reasoning, zero cache-write; no per-engine savings
  attribution. One-page prose complexity differs from prior monitor listings.
- Comparison36 favorsQ on all4 fixed samples. T ordinary prose produced Latin
  fragments; Q still misread2 윷 characters. Probe one representative T crop for
  a new prose style rather than trusting appearance alone; route stays provisional.
- Original 컬럼버스, 규면/규민 discrepancy and historical wording retained. Source
  coverage, explicit three-column joins, UTF-8 ranges and byte-identical rebuild
  pass. July28complete/8untouched/no partials,171pages3466regions3282text184images
  901flags, zero human acceptance. Next Yut209–214candidate; ending unverified.
  Full metrics/reading room pending; final reporting/commit usage carries forward.

### July 윷놀이 opening restored, 2026-10-12

- Full209–214/printed205–210 verified;215 starts 사과도둑. Partial209–211 now
  restored:65regions61text4images29flags,40 address-description rows80cells,
  82hex rows651byte fields plus one monitor command. Flowchart preserved intact.
- Representative T prose probe0.235s produced Latin fragments; fixed5T/56Q before
  main OCR. Rejected probe reused only for fixed comparison, counted once.
- Terminal143 after16 savedQ crops; all5T and16Q reused unchanged. Interrupted
  p209r22 request preserved, response usage unknown. Two worker lifespans172.563s;
  successful recognition149.850sQ/0.374sT;local20,544tokens completed lower bound.
- Correction347.317s overlaps156.943s raw;33,996uncached/1,408,000cached input and
  10,168output incl1,258reasoning, zero cache-write. Includes recovery/helper work.
- Comparison37 favorsQ on4fixed crops, but 윷/byte glyph errors and an extra0A30
  byte field required source repair. Original $800~$100,$1000 and message spacing
  retained. Coverage,83listing rows,UTF-8 ranges and byte-identical rebuild pass.
- July28complete,1partial,7untouched;174pages3531regions3343text188images930flags,
  zero human accepted. Next remaining hex212–214, then assemble209–214. Final
  metrics/reading room pending; reporting/commit usage carries to next audit.

### July 윷놀이 complete, 2026-10-12

- Restored remaining212–214 and assembled full209–214/printed205–210. Batch40:
  136regions127text9images49flags,750 visible hex rows5993fieldslots;5991values
  transcribed,2[ILLEGIBLE]. Original1CC0/1F60 rows absent,1CB8 physically clipped.
- Full article201regions188text13images78flags,40address rows80cells,
  833listing rows(1command+832hex),6644fieldslots6642transcribed2unreadable;
  16absent source bytes never invented. Complete source restoration does not mean
  complete executable program. Small ambiguous readings remain provisional.
- All127crops Qwen, one uninterrupted raw666.379s;recognition640.520s nested;
  exact53,547local tokens(33,431prompt/20,116completion), no retries/fallbacks.
- Correction1062.358s overlaps640.973s raw.72,635uncached/6,249,088cached input,
  30,162output incl4,690reasoning, zero cache-write; includes literal source
  transcription, doubtful-field/assistant-draft rechecks and helper preparation.
- Comparison38 Qwins4hex samples, but successful raw responses contain omitted,
  shifted and extra fields plus address/glyph errors. No causal paid-savings claim.
  Coverage, source gaps, listing/review ranges and byte-identical assembly pass.
- July29complete,7untouched,no partials;177pages3667regions3470text197images979flags,
  zero human accepted. Next 사과도둑215–224candidate;215startverified,ending not yet.
  Final metrics/reading room pending; final reporting/commit usage carries forward.

### July 사과도둑 opening restored, 2026-10-12

- Verified the full article at PDF215–224, printed211–220;225 starts 탁구.
  Restored215–217:96 regions,92 text crops,4 source images,32 review flags.
  Includes33 variable entries,40 program-range entries and27 BASIC lines across
  60 physical rows. Line270 continues on218; the full article remains partial.
- Source YB/YB,US,933/930 and Aplle retained. Faint PLAY150/Sohool and literal
  spacing remain provisional. Custom graphics use explicit scan-linked markers;
  character encoding and execution are unverified. Human review remains pending.
- Initial7T/85Q after a rejected0.270s prose probe. After a confirmed SIGTERM,
  reused61Q and7T successes. Qwen then repeated header asterisks to4096 tokens;
  one Tesseract fallback plus two unattempted header strips routed to Tesseract.
  Final10T/82Q; remaining short-code crops completed with512-token caps.
- Three raw worker lifespans325.483s, including125.955s failed model compute.
  Local34,263-token lower bound includes4,435 failed tokens; interrupted response
  usage is unknown. No completed inference was repeated.
- Correction582.581s overlaps315.663s raw, includes recovery/helper work and
  assistant draft rechecks. Paid48,143 uncached /2,385,408 cached input,
  17,236 output including2,996 reasoning; no per-engine paid-savings claim.
- Four comparison39 samples favor Qwen, but exclude the failed decorative header
  from accuracy scoring. Its cost remains included. Export, byte-identical
  rebuild, listing coverage and UTF-8 review ranges pass.
- July29 complete,1 partial,6 untouched;180 pages,3763 regions,3562 text crops,
  201 images,1011 flags. Next218–224, then assemble215–224. Final metrics and
  reading room remain pending; final report/commit usage carries to next audit.

### July 사과도둑 middle listing restored, 2026-10-12

- Restored PDF218–220:92 regions,86 text crops,6 full column images,70 flags.
  All386 physical rows checked:132 numbered rows280–1590 plus two initial
  continuations of270.63 editorial graphic markers preserve source-row links;
  one faded source span remains [ILLEGIBLE]. No inferred glyph bytes or repair.
- One uninterrupted raw worker297.048s, final85Q/1T. An apple-art crop repeated
  spade symbols until the512-token cap; same-crop T fallback cost retained.
  Failed model compute15.226s; exact38,778 local tokens include891 failed tokens.
- Four successful Qwen responses silently omitted statement text near graphic
  literals. Restored against source. Original IF/ELSE anomalies,R.1 and codeL
  versus proseJ retained. Assistant first-draft370/870 confusion was source-rechecked.
- Correction740.656s overlaps256.709s raw; includes literal source transcription,
  graphical placeholders, enlarged rechecks and helper/index preparation.
  Paid73,589 uncached /3,973,760 cached input;20,854 output includes6,604 reasoning.
  No causal per-engine paid savings claim.
- Comparison40 favors Qwen on four plain-code samples. Two sample IDs were revised
  during source review to exclude graphic markers, before reference sealing and
  alternate scores; this set was not wholly preselected before primary OCR.
- Export integrity, byte-identical rebuild, listing coverage and UTF-8 ranges pass.
  July29 complete,1 partial,6 untouched;183 pages,3855 regions,3648 text crops,
  207 images,1081 flags. Next221–224, then full215–224 assembly with explicit
 270/1590 continuation links. Final metrics/reading room remain pending.

### July 사과도둑 complete, 2026-10-12

- Restored221–224 and assembled full215–224:305 regions,287 text crops,18 images,
  165 flags,358 numbered BASIC lines and940 representation rows. Four continuous
  wall bands are whole-band markers, not a claim of exact printed graphic rows.
- DATA2620–3570:96 rows,1,152 fields,three partial unreadable digits retained.
  Source anomalies and uncertain music/whitespace/glyph encoding remain flagged.
- Batch43 raw409.224s,105Q/4T, including two512-token graphic failures and same-crop
  fallbacks. Failed compute30.172s; exact50,111 local tokens. Original saved session
  remained live; no interruption/restart despite misleading sandbox-only ps.
- Correction920.636s overlaps392.234s raw and includes helper/export/comparison
  work. Paid140,700 uncached /3,864,448 cached input;28,213 output including3,076
  reasoning. Four exploratory comparison41 crops favor Qwen; no paid-savings claim.
- Added explicit, validated cross-segment wrapped-line joins for270/1590.
  All segment pins and listing bytes preserved. Export/rebuild/UTF-8 checks and
  76 assembly tests pass. Assembly163.401s measured separately.
- July30 complete,0 partial,6 untouched;187 pages,3972 regions,3757 text crops,
  215 images,1144 flags. Next Table Tennis225: verify end before mapping.
  Final metrics and reading room still follow restoration. Human review pending.

### July Table Tennis complete, 2026-10-12

- Restored the complete article on PDF225–228: 100 regions, 94 text crops,
  six original images, 38 review flags, 20 variable entries and 27 outline entries.
  Listing has 143 numbered BASIC lines and 302 representation rows; 72 graphic
  placeholders preserve source links without claiming executable glyph encoding.
- Initial 24T/70Q became 25T/69Q after one 512-token graphic repetition failure.
  Raw worker 235.598s, including failed compute 15.170s; exact 30,460 local tokens
  include 963 failed tokens. Accepted 0.245s prose probe reused once in T recognition,
  outside raw worker lifespan. No interrupted requests or successful reruns.
- Two successful Qwen responses silently omitted plain IF suffixes; source-restored.
  Source DATA has 553 visible numeric tokens but 552 comma fields: one missing comma
  retained. Provisional faded values, original syntax and music strings remain flagged.
- Correction 868.011s overlaps raw by 222.939s and includes source rechecks, a cleared
  margin concern, status/context recovery and helper preparation. Paid 91,868 uncached
  /6,104,704 cached input; 24,181 output includes 3,716 reasoning. Export and evaluation
  separately measured. No causal paid-cost saving claim.
- Comparison42 favors Qwen on four samples. Three were preselected; one code sample
  was changed after source review to exclude graphic placeholders, before reference
  sealing/alternates. Unblinded assistant references are not human gold.
- Export integrity, byte-identical rebuild, listing coverage and UTF-8 review ranges
  pass. July31 complete, five untouched; human review pending. Next cashbook starts229;
  ending237 remains a candidate to verify. Final metrics and reading room pending.

### July Cashbook opening restored, 2026-10-12

- Verified full article PDF229–237;238 starts the classified section. Restored229–232:
  116 regions,114 text crops,two original columns,27 flags. Complete instructions,
  30 variable entries,23 program ranges,two special notes,five error cases and five
  search formats. Opening listing has30 numbered lines1–210 across40 physical rows.
- T prose probe produced Latin substitutions and was rejected. Fixed16T/98Q:
  titles/two repetitive asterisk headers use T; prose,outlines and plain BASIC use Q.
  Original session returned terminal143 before resume. Reused26 Q stages and16 T;
  two date-format crops repaired and repeated with original evidence/cost retained.
- Two measured worker lifespans276.996s,excluding recovery gap. Completed-response
  local43,215-token lower bound includes two superseded crop responses; interrupted
  p230r15 usage unknown. Probe counted once as preparation/reused only as alternate.
- Correction637.291s overlaps raw by267.215s; includes source inspection, explicit
  draft edits/joins,crop repair,recovery and helper preparation. Paid74,414 uncached
  /3,771,392 cached input;16,905 output includes6,376 reasoning. No per-engine paid
  savings claim. Export/evaluation separately measured.
- Four unchanged comparison43 samples favor Qwen. Split-Hangul BASIC is4.41% versus
  T47.06% compact CER; reference is unblinded assistant source reading, not human gold.
  Printed jamo breaks,awkward source wording/ranges and missing-looking delimiter
  remain flagged; no execution or historical encoding certification.
- Export/rebuild/UTF-8/listing checks pass. July31 complete,one partial,four untouched.
  Next233–237 listing,then assemble229–237. Final metrics and reading room pending;
  all human acceptance remains pending and final reporting usage carries forward.

### July Cashbook complete, 2026-10-12

- Restored remaining233–237 and assembled full229–237:253 regions,241 text crops,
  12 original columns,75 flags;399 numbered BASIC lines across611 physical rows.
  Both immutable segments and literal physical wraps are preserved. One partial
  Hangul glyph remains unreadable; human proofreading and encoding review pending.
- Batch46 initially117Q/10T; a dotted prompt hit512 tokens and used Tesseract,
  final116Q/11T. Terminal143 confirmed before resume;34 Q stages and10 T crops
  reused. Raw two-lifespan341.445s;48,489 captured local tokens is a lower bound,
  including839 failed tokens. Interrupted request usage unknown.
- Correction730.481s overlaps313.260s raw. Paid107,664 uncached/3,206,400 cached
  input and23,864 output (including5,528 reasoning). Source inspection, draft
  edits, status recovery and helper preparation included; export/evaluation/
  assembly separate. No causal paid-token saving claim.
- Qwen wins four preselected comparison44 samples, but source review corrected
  omissions, punctuation and a reversed negative sentence. Add dotted prompt
  runs to repetition-risk routing; retain bounded fallback and source review.
- Export/rebuild/UTF-8/listing concatenation/source-pin checks pass. July32 complete,
  zero partial,four untouched. Next classified238–239 boundary verification, then
  Q&A,industry history and advertising index. Final metrics/reading room pending.
  Reporting/commit usage after the audit cutoff carries forward.

### July classified section restored, 2026-10-12

- Complete238–239:51 regions,50 text crops,one photo,19 flags;46 advertisements,
  35sale/11exchange,44phone/two postal contacts. Cross-page listing explicitly
  joined; four prices remain with their source advertisement.240 starts Q&A.
- Fixed47Q/3T after rejected0.326s T probe. Terminal143 confirmed;12Q/3T reused.
  Fourteen shared boundaries repaired across19 crops; only two completed crops
  repeated, original evidence/cost retained. No fallback; interrupted usage unknown.
- Raw149.538s; local21,539-token lower bound includes two superseded responses.
  Correction368.579s overlaps140.661s. Paid44,019 uncached/2,361,600 cached input;
  10,061 output includes2,998 reasoning. Source checks/repair/recovery/helper work
  included; export/evaluation separate. No causal paid-token saving claim.
- Qwen wins four comparison45 samples. IDs preselected; two images changed during
  source repair before seal/alternates. Names/model spelling/source anomalies
  still need human review. All phone strings and two postal contacts source-checked.
- Export/rebuild/UTF-8/cross-page checks pass. July33 complete,zero partial,three
  untouched. Next Q&A240 onward,industry history and advertising index; full metrics
  and reading room afterward. Final reporting/commit usage carries forward.

### July Q&A restored, 2026-10-12

- Complete240–242:78 regions,69 text crops,nine images,31 flags;five Q&A pairs,
  seven BASIC panels/72 numbered lines plus three template rows. Column/page
  continuations joined;243 starts industry history.
- Fixed56Q/13T after rejected0.206s Tprose probe. Both workers completed normally.
  One code crop per engine widened after first pass;55Q/12T reused and original
  costs retained. Raw164.828s;exact24,665 local Q tokens includes one superseded crop.
- Correction496.203s overlaps155.260s raw;42,504 uncached/2,421,504 cached paid input,
  13,845 output including5,136 reasoning. Source checks/repair/helper work included;
  export/evaluation separate. No causal paid-token savings claim.
- Qwins four unchanged preselected comparison46 samples. Corrected an extra DATA
  value and command names; kept printed label mismatch,technical claims/formulas,
  source anomalies and provisional literal glyphs. No code execution claim.
- Export/rebuild/UTF-8/joins/listing checks pass. July34 complete,zero partial,two
  untouched. Next history243 extent verification,then advertising index; final
  metrics/reading room afterward. Reporting/commit usage carries forward.

### July industry-history opening restored, 2026-10-12

- Verified full article243–261,ending mark261;262advertising index. Restored243–248:
  132text/four images,24flags,eight joins and two separate boxed sidebars.
- Fixed124Q/8T after rejected0.162s prose probe; normal completion,no retries.
  Raw332.609s;exact50,999localtokens. Correction398.599s overlaps332.609s.
  Paid70,982uncached/1,474,304cached input;13,383output includes2,502reasoning.
- Comparison47: Qwen wins three,Tesseract one. Keep the counterexample; no causal
  paid-token claim. Export/rebuild/UTF-8/continuation checks pass,human review pending.
- July34complete,onepartial,oneuntouched. Continue history249–261 and adindex262;
  assemble history,consolidate metrics,then build the authorized reading room.

### July Atari-history section restored, 2026-10-12

- Restored249–252:103text/four images,29flags,seven joins.253 starts Commodore.
  History243–252 now restored;253–261 and final assembly remain.
- Fixed97Q/6T after rejected0.177s prose probe. Original completed normally;
  eight left-clipped Q crops widened,89Q/6T reused. Revised run also exit0.
- Raw283.277s,exact41,193localtokens includes eight superseded responses.
  Correction432.584s overlaps283.277s. Paid58,480uncached/2,328,192cached input;
  13,154output includes2,867reasoning. No causal paid-token saving claim.
- Comparison48: three Qwen wins,one tie; four original sample images unchanged.
  Export/rebuild/UTF-8/joins pass.34complete,onepartial,oneuntouched,50checkpoints.
- Continue253–261/adindex262,assemble history,consolidate metrics,build reading room.
  Check both side edges against sloping source columns before further raw runs.

### July Commodore-history section restored, 2026-10-12

- Restored253–255:66 text crops,three original images,21 flags,three narrative
  joins; both profit charts retained with labels and ten numeric entries.
- Fixed64Q/2T after rejected0.177s prose probe; normal completion without retries,
  fallbacks or crop repairs. Raw166.579s;exact25,264 local Qwen tokens.
- Correction196.734s overlaps166.579s raw. Paid22,062 uncached/619,136 cached input;
  6,796 output includes777 reasoning. Substantial source reading was in preparation,
  so this shorter correction window alone does not demonstrate reduced effort.
- Comparison49:three Qwen wins,one tie. Original typesetting anomaly and financial
  discrepancy preserved for human review. Export/rebuild/UTF-8/12 targeted checks pass.
- History243–255 restored;256–261 remain,then adindex262 and assembly. July remains
  34 complete,one partial,one untouched across51 checkpoints. Metrics and authorized
  reading room follow restoration; reporting/commit usage carries forward.

### July Coleco-history section restored, 2026-10-12

- Restored256–258:69 text crops,three images,25 flags,five narrative joins.
  Full history243–258 restored;259–261 and assembly remain.
- Fixed65Q/4T after rejected0.199s name/prose probe. Widened margins during
  preflight; primary completed normally without retries/fallbacks/crop repairs.
  Two T headings were blank and transcribed directly from source.
- Raw179.174s;exact26,827 localtokens. Correction213.797s overlaps179.174s raw.
  Paid10,703 uncached/872,192 cached input;7,448 output includes1,154 reasoning.
  Source reading also occurred in preparation and final glyph rechecking in export;
  correction alone is not total effort. Original spelling variants preserved.
- Comparison50:four Qwen wins; unblinded assistant references,not human gold.
  Final export/rebuild/UTF-8/15 targeted checks pass. Human review remains pending.
- July34 complete,one partial,one untouched across52 checkpoints. Next Microsoft
  ending259–261,adindex262,assembly,full metrics and authorized reading room.

### July industry history completed and assembled, 2026-10-12

- Restored Microsoft ending259–261:71 text crops,three images,24 flags,five
  joins,nine Q&A pairs. Eight historical Korean endings preserved after enlarged
  source checks; Qwen had normalized some. Tesseract title blank,source-transcribed.
- Fixed70Q/1T after rejected0.186s probe; normal completion,no retries/fallbacks.
  Raw172.544s;exact27,200 localtokens. Correction283.016s overlaps172.544s raw.
  Paid14,656 uncached/1,555,072 cached input;8,569 output includes1,909 reasoning.
  Significant source reading also occurred in preparation; no causal savings claim.
- Comparison51:three Qwen wins,one tie. Export/rebuild/UTF-8/nine-pair/eight-ending
  and13 continuation/name checks pass; human review remains pending.
- Assembled full243–261 from five immutable segments:458 regions,441 text crops,
  17 original images,123 review flags. Complete extent,all review ranges and
  byte-identical rebuild verified; no new OCR or source corrections in assembly.
- July35 complete,zero partial,one untouched across53 checkpoints. Only advertising
  index262 remains before consolidated metrics and the authorized reading room.
