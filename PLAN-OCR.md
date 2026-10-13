# Sustainable OCR and correction workflow

Updated: 2026-10-12. Owner: the archive maintainer; implementation and experiments
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

### July restoration complete, 2026-10-12

- Final advertising index262 restored:25 advertisers,27 associated page/cover
  references including three cover references;26 text crops,two original images,
  ten flags. Upper publisher advertisement excluded as a separate source item.
- Fixed25Q/1T after rejected0.103s row probe; normal completion,no retries/fallbacks.
  Raw28.709s;exact5,148 localtokens. Correction89.157s overlaps28.709s raw.
  Paid5,079 uncached/605,312 cached input;2,783 output includes425 reasoning.
- Comparison52:four Qwen wins;Tesseract blank on three rows under tested settings.
  Decorative leaders removed consistently before field-oriented CER; do not pool
  those scores with prior literal CER. Source reading also occurred in preparation.
- Export/rebuild/UTF-8/all25 row associations/27 references/three covers pass.
  All36 July bodies restored across54 checkpoints;zero partial or untouched.
  Human review remains pending. Full metrics consolidation and authorized reading
  room are the remaining goal deliverables; reporting/commit usage carries forward.

### July metrics and human-review preview completed, 2026-10-12

- All36 article bodies cover225 source pages;42 TOC entries reconcile as36 bodies
  and six group headings. All human acceptance remains pending.
- Consolidated206 ordinary crops: Qwen2.35% versus Tesseract22.56% compact CER;
  197 Qwen wins,four Tesseract wins,five ties. Four leader-normalized index crops
  stay separate.209 matched timed crops:805.51s versus41.42s (19.45× raw time).
- Native audit reconciles1,776,981 captured primary local tokens including failures
  and superseded work,plus24,246 alternate-evaluation tokens separately. Interrupted
  uncaptured generation remains unknown. Paid usage includes preparation,export,
  assembly,evaluation,reporting and between-window work; no causal savings claim.
- Decision and reproducible aggregator:docs/OCR-JULY-DECISION.md,
  docs/ocr-july-metrics.json,tools/ocr_qwen/consolidate_july.py. Continue the documented
  provisional routing rule; local GPU cost remains excluded from the decision.
- Complete preview:http://127.0.0.1:4188/archive/#/issues/maso-1984-07.
  Fresh output preserves all184 earlier scan articles and CD data. Full integrity,
  preservation,TOC accounting,production build,19 frontend and seven metric tests
  passed. Browser checked code,desktop/mobile source review,original OCR and final
  assembled-history region. Private screenshots and evidence retained.
- The interrupted delivery wait is excluded from active review windows using the
  last confirmed browser action; uninstrumented tail stays in between-window usage.
  Final audit has an explicit cutoff; the subsequent commit/report tail is excluded.
  Restoration,metrics and preview goal complete; next work awaits human review.

### August paired-cost pilot selected, 2026-10-12

- User approved choosing varied August articles for the proposed paired-cost pilot.
  Selected eight complete articles totaling28 source pages (16 planned restorations,
  56 page passes):editorial20,death-ski37–38,contest review237,basic technique65–68,
  VISICALC181–185,PIA196–199,BASIC command editor214–220,Q&A262–265.
- All selected layouts and adjacent boundaries visually checked before OCR. August
  selected PDF/printed pages match;do not reuse July's+4 offset. Contest review is
  one page;238 solicitation and239 RECALC are separate. Unrelated ads excluded.
- Frozen protocol:docs/OCR-AUGUST-PILOT.md; source/TOC/category/order pins:
  docs/ocr-august-pilot-selection.json. Balanced engine-first order,seed198408;
  first two pairs verify instrumentation before the remaining six.
- Local resources/time priced at zero. Paid usage split by uncached/cached/output,
  with shared preparation and experimental overhead separate. Source correction,
  human review,failed attempts and equal coverage remain required. No OCR or paid
  paired correction yet;no reading-room rebuild authorized for this pilot.
- Valid paired correction requires fresh contexts with no cross-arm answer reuse.
  Session rules require explicit authorization before subagent delegation; otherwise
  use separate fresh user-started correction sessions. Do not compare two sequential
  corrections in the existing conversation as independent measurements.

### August first-two raw pairs prepared, 2026-10-12

- Editorial p.20 and Death Ski pp.37–38 completed through both pure engines:
  four raw arms, 37 text crops per engine, no failed crops or retries. Both arms
  received identical crop bytes; 41 shared regions include four original figures.
- Added frozen-input paired runner and a passing failure-preservation test.
  Runtime/model pins match July. Raw worker times: editorial T 6.85s/Q 22.90s;
  game Q 43.27s/T 8.25s. Captured 24,770 local Qwen tokens have zero monetary cost.
- Prepared four separate correction packets with common instructions, source
  images, one assigned draft and immutable input manifests. No semantic correction
  or corrected export yet. Explicit delegation authorization remains pending;
  independent-session usage capture and equal-quality checks are still required.
- Progress and coordinator-only usage: docs/ocr-august-pilot-progress.json and
  docs/ocr-august-pilot-usage.json. Shared helper work overlapped local OCR and is
  not assigned causally to either engine. Audit cutoff excludes the later tail.
- First-two instrumentation gate remains unpassed; remaining six pairs not started.
  No paid-cost or accuracy verdict and no reading-room rebuild at this checkpoint.

### August independent corrections authorized; editorial pair sealed, 2026-10-12

- User explicitly authorized independent correction agents. Each case starts with
  a fresh context, the same instructions, inherited gpt-6-astra/high settings and
  one assigned draft. The second article's first correction is now running.
- Both editorial arms are sealed: 14 text regions and one figure each, unchanged
  assigned inputs, independently checked exports and byte-identical rebuilds.
  Native child-session usage is captured separately; no response-ID overlap with
  each other or the coordinator log was observed.
- Editorial T: 36,080 uncached / 346,240 cached input, 4,513 output tokens.
  Editorial Q: 32,005 uncached / 390,656 cached input, 4,228 output tokens.
  Reasoning is included in output; local resources still have zero monetary weight.
- All corrected text agrees ignoring whitespace; three spacing differences.
  Disagreements and the frozen source sample checked. One shared blurred-syllable
  reading remains for human review; only one independent arm originally flagged it.
  Original independent outputs remain unchanged; no character-perfect claim.
- Counts and break-even expression documented in docs/OCR-AUGUST-PILOT.md and
  docs/ocr-august-pilot-correction-usage.json. First-two gate still pending; no
  overall cost verdict, no six-pair expansion yet and no reading-room rebuild.

### August first-two measurement gate passed, 2026-10-12

- All four independent corrections sealed; native usage, common model/effort,
  immutable inputs, export integrity and byte-identical rebuilds verified.
- Game pair: 23 text regions, three figures, 80 physical / 68 logical code rows
  per arm. Five differing regions: two wording disagreements (one confirmed error
  per arm), one graphic approximation and two nonliteral placeholder differences.
  All disagreements and fixed source samples checked; human review still pending.
- Game T: 48,875 uncached / 750,336 cached input, 8,177 output tokens.
  Game Q: 64,062 uncached / 693,504 cached input, 7,538 output tokens.
  Worker-declared correction time was about 244s for each; timings are diagnostic.
- First-two gate passed with equal reviewable coverage and disclosed remaining
  errors. Continue the six frozen pairs with unchanged correction instructions.
  Cost depends on the rate vector; no overall winner or full-cohort conclusion.

### August contest pair complete; BASIC technique correction started, 2026-10-12

- Third pair sealed and compared: 17 text regions and one figure per arm, verified
  exports/rebuilds and immutable inputs. Six table columns, four rows and one empty
  cell preserved; 23/24 data cells agree ignoring whitespace. A blurred name remains
  unresolved. One Tesseract-route wording error recorded for human correction.
- Contest T: 33,297 uncached / 492,928 cached input, 4,785 output tokens, 147.78s
  worker-declared correction time. Q: 34,322 / 461,952 / 6,532 tokens, 197.06s.
  Common pricing condition documented; no general cost or accuracy winner.
- Fourth article pp.65–68 mapped into 79 regions, including 73 text crops, six
  source figures and ten separate listing/monitor groups. Both pure raw arms passed
  without failures (Q 59.93s, T 14.46s); first independent correction is running.
- Three paired comparisons complete, fourth in progress, four articles not started.
  All human acceptance remains pending; no reading-room rebuild.

### August fourth pair complete; VISICALC coverage recovery, 2026-10-12

- Eight independent corrections sealed; fourth pair source comparison complete.
  Both routes retain one confirmed fidelity error and an uncertain literal spacing.
- Fourth-pair token vectors and price break-even condition recorded in the pilot.
- VISICALC agent detected a missing shared crop line before export. Preserve its
  paid attempt, amend both input maps identically, rerun both raw arms, and restart
  both corrections with fresh contexts. Original artifacts stay immutable.
- Recovery overhead remains explicit; no zero-cost substitution for the unstarted
  arm and no reuse of paired corrections. Remaining three article pairs continue.
- Human acceptance pending throughout; reading room not rebuilt.

### August first six pairs compared; final two in correction, 2026-10-12

- All 16 matched raw arms are complete; 12 independent corrections are sealed.
  VISICALC recovery is complete, with its original abort and both raw reruns retained.
- VISICALC source review found eight wording/number errors and one punctuation
  omission in the Qwen-route correction; no confirmed T-route error in the checked
  regions. Hardware code agrees; one Q-route prose error remains for human review.
- Native token vectors and rate-dependent break-even conditions are documented.
  No raw-accuracy shortcut, full CER claim, or actual-currency total is inferred.
- Editor geometry v2 moves one shared crop seam before either raw arm ran;
  original frozen geometry is preserved and no correction attempt was discarded.
- Editor correction is running; Q&A packets are ready. Continue the frozen order
  and identical fresh-context instructions. Human acceptance pending; no reading room.

### August editor comparison complete; final Q&A pair underway, 2026-10-12

- Fourteen independent restorations sealed. Editor exports retain 151 text regions,
  six figures and 106 logical listing rows; one blank row explains the physical
  count difference. All disagreements and fixed samples source-checked.
- Both editor routes retain code/prose errors and unresolved faint glyphs/spaces.
  Lower Qwen total tokens coexist with more uncached input; pricing remains conditional.
- Q&A is the final planned pair. Consolidated reports are prepared with completion
  guards; human acceptance remains pending and no reading room has been rebuilt.

### August paired cost pilot complete, 2026-10-12

- Eight selected whole articles, 28 pages, 16 independent restorations complete;
  every export passed integrity and byte-identical rebuild checks. Both routes
  preserve 537 text regions and 30 original figures across the cohort.
- All paired disagreements and frozen source samples reviewed. Source-fidelity
  findings and uncertain glyphs remain recorded without altering sealed outputs.
  Human acceptance and later repair costs remain pending.
- Qwen matched totals: 730,994 uncached / 7,357,568 cached input / 72,314 output.
  Tesseract: 587,775 / 8,536,576 / 81,279. Reasoning is included in output.
- At hypothetical rates 1:0.1:4, Qwen correction is only 0.60% cheaper, with four
  articles favoring each route. The observed coverage-abort-inclusive Q route is
  4.17% higher. Actual rates are unknown; no currency bill or general savings claim.
- Matched raw worker time: Q 502.77s / T 115.41s. Correction worker time:
  Q 2,459.52s / T 2,393.35s. Local resources priced at zero; timing is diagnostic.
- docs/OCR-AUGUST-PILOT-RESULTS.md and the results JSON consolidate article-level
  metrics, rate sensitivity, recovery and shared experiment overhead. Keep the
  current selective-use policy provisional; no further double restoration begun.
- Reading room not rebuilt. Progress, usage and evidence pins recorded and committed.

### August user review: retain and improve adaptive routing, 2026-10-12

- User's tentative interpretation: Qwen's token-volume benefit is more useful for
  complex layouts/structured material/code; simpler articles show no practically
  decisive difference. Continue adaptive routing as the working policy.
- Use the user-supplied 10:1 uncached/cached input-price ratio. Output pricing is
  still unspecified; preserve the token vector and label output-rate assumptions.
- Documented region-level decisions, separate handling of diagram images and
  surrounding text, reuse of bounded probes, one selected correction pass, and
  explicit checks against normalization of printed spelling and code literals.
- Record future weighted usage and recovery during ordinary restoration. This
  update changes guidance only; the completed paired evidence remains sealed.

### Routing guide made discoverable for future sessions, 2026-10-12

- The current operational guide is now at the top of [PLAN-PDF.md](PLAN-PDF.md):
  engine choices, region-level routing, bounded probes/fallbacks, mandatory review,
  10:1 input-price weighting, evidence links and the reading-room hold.
- Historical May status and initial Tesseract setup are labeled explicitly so
  later sessions use current progress and routing instead of restarting old work.

### August ordinary restoration started, 2026-10-12

- User goal: restore all remaining August1984 articles. Separate production campaign
  `private/pdf-restoration/13-1984-08-adaptive/` accounts for43 canonical entries.
  Eight sealed pilot articles remain available for later production selection/repair;
  their residual errors and human acceptance are not silently cleared.
- Source inspection verifies logic IC feature21–29;30 is advertising,31 the
  non-owning hobby divider,32 begins 청소. First bounded batch restores21–26:
  139 regions,114 text crops,25 original figures and79 ordered blocks.
- Fixed39T75Q routing follows one0.323s representative T prose probe: technical
  identifiers failed beyond ordinary spacing. T handles short headings/captions;
  Q handles faint prose, formulas and tables. No full dual correction/evaluation.
- Ten crop edges repaired after enlarged source review: five T text crops,one Q
  text crop andfour figure crops. Initial run and all superseded outputs retained;
  unchanged crops reused. Original inverted-summary seam was fixed before inference.
- Nine searchable tables preserve34 data rows/100 cells. Two exact source subranges
  project the displaced page24 paragraph without dropping or repeating characters.
  Printed Booleen,reley,Direct Couple,23/24 repeated introduction,logic contradictions
  and missing/faint overbars remain literal or explicitly provisional.15 review flags.
- All139 crop geometries,76 Q request-image hashes/stop outcomes,regional/text/review
  byte ranges,table cells,source digest and independent byte-identical export rebuild
  pass. All16,790 prior pilot files unchanged. No runtime pipeline or frontend edits;
  no new unit-suite claim. JSON/assets only; reading room not rebuilt.
- Captured76 Q calls total39,792 local tokens and81.572s recognition,including the
  one replacement. T recognition3.894s plus rejected probe0.323s. Local money weight
  remains zero. Prospective paid windows include setup,recovery and export; no
  causal savings or human-time claim. See `docs/ocr-august-usage.json`.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-01/logic-ic/`.
  Evidence:`private/pdf-restoration/13-1984-08-adaptive/batch-01/validation.json`.
  Progress:`docs/ocr-august-progress.json`. Whole August and this article remain
  incomplete:one production partial,28 untouched bodies,eight sealed pilot bodies,
  one classified heading,five unclassified headings,zero human accepted.
- Next:ending27–29 and separate full logic IC assembly,then 청소32 onward.
  Preserve the user's unrelated `web/package.json` change outside commits.

### August logic IC feature complete, 2026-10-12

- Batch02 restores ending27–29:84 regions,65 text crops,19 original images,
  six searchable tables/26 rows/110 cells,50 ordered blocks and17 review flags.
  Fixed41Q24T assignments reuse the opening probe; no retries or repeated successful
  inference. Pre-OCR crop-margin revisions remain recorded.
- Original EX-OR values, table heading1, absent complement bars, final J-K row,
  malformed arithmetic and provisional heading6/8 retained. Clock arrows and
  Unicode bars/subscripts are reading aids; original pixels remain authoritative.
  Source29 T subsection precedes the counter, followed by7.7 caution prose.
- Separate full21–29 assembly preserves both native exports byte-for-byte:
  223 regions,179 text crops,44 original images,129 blocks,15 tables/60 rows/210 cells.
  All32 flags remain in original segment metadata; an explicit combined-byte audit
  indexes them without rewriting native corrections. First validation expected a
  nonexistent top-level flag field; that failed check and its recovery are recorded.
- Export integrity, all crop/source/request hashes, stop outcomes, regional character
  coverage, review ranges, native metadata and independent byte-identical rebuild
  pass. All16,790 sealed pilot files unchanged. Human acceptance remains pending.
- Batch02 Q capture:21,205 local tokens/41.129s across41 calls;T2.057s.
  Paid setup/correction/assembly/reporting windows remain separate and non-causal;
  local money weight zero, output pricing and human review time unknown.
- Full export:`build/pdf-restoration/13-1984-08-adaptive/logic-ic/`.
  Native ending:`build/pdf-restoration/13-1984-08-adaptive-batch-02/logic-ic-ending/`.
  Audit:`private/pdf-restoration/13-1984-08-adaptive/logic-ic-assembly-validation.json`.
  One production article complete,28 untouched bodies,eight sealed pilot bodies,
  one classified heading,five unclassified headings;zero human accepted.
- Whole August remains in progress. Next:verify and restore 청소32–36 and boundary37.
  JSON/assets only; no reading-room rebuild or runtime/frontend changes.

### August 청소 opening and hex dump, 2026-10-12

- Verified full32–36; BASIC ends910 in upper36, advertisement below excluded,
  and37 starts the next pilot title. Batch03 restores32–33:42 regions,41 text,
  one original screen,33 ordered blocks,208 hex rows/1664 bytes and13 review flags.
- T probe0.206s lost one proper noun/punctuation; later neighboring T prose has
  substantial Latin garbage. The successful probe is reused, all failed routing
  evidence retained, and the selected draft corrected directly from inspected scans.
  Do not extrapolate this initial sample to noticeably fainter neighboring crops.
  Actual new calls20T20Q,plus the one reused probe; no alternate full restoration.
- All18 Q hex crops source-compared.25 row corrections restore omitted/repeated
  cells and address glyphs. Initial final-column count67 was wrong:source ends6678
  with68 rows. Existing whitespace seams already contain every complete row;
  revised coverage records13/12/7 rows in the final three crops. No crop rerun.
- Printed 장진,패들값을기,CALL-151를 and prose4-shapes/12-shapes discrepancy
  retained. Structural address/byte counts validate coverage, never supply byte values;
  byte-perfect proofreading/execution remain unverified.211 unnumbered listing rows
  include two commands and the trailing monitor prompt.
- All42 crop/source/request hashes,20 Q stop outcomes,regional characters,text and
  listing byte ranges,source corrections,independent identical rebuild and16,790
  sealed pilot files pass. Human acceptance pending;JSON/assets only.
- Q12,755 local tokens/62.599s;T4.144s plus probe0.206s. Paid preparation/routing
  mistakes/correction/export/reporting windows separately recorded;no causal savings.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-03/sweeping-opening/`.
  Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-03/validation.json`.
  One complete production article,one partial,27 untouched,eight sealed pilot bodies,
  five unclassified headings;zero human accepted. Whole August remains in progress.
- Next:batch04 BASIC34–36,then separate full 청소 assembly.

### August 청소 BASIC34–36 native checkpoint, 2026-10-12

- Batch04 restores58 code crops,58 ordered blocks,332 physical rows and90 printed
  BASIC labels10–910. All six source columns and15 crop panels inspected. Lower36
  academy advertisement excluded; pre-OCR right margin widened before inference.
- Qwen alone handles faint structured code:58 completed calls,26,672 local tokens,
  65.233s recognition;no retries or alternate whole correction. Collapsed physical
  rows and mangled labels corrected from scans. Source wraps inside strings,
  identifiers and numeric DATA retained;no inferred executable reconstruction.
- Twenty source flags retain faint0/O,1/I,apostrophes/spaces,PLYER typo,concatenated
  BLOAD name,repeated FN F and faint dot after X. Character-perfect proofreading,
  source bytes and execution remain unverified;human acceptance pending.
- Crop/source/request hashes,all stop outcomes,regional character coverage,text and
  review UTF-8 ranges,332 physical/90 logical listing partitions and exact printed
  label indexes pass. Independent rebuild identical;16,790 pilot files unchanged.
  Validator row-kind schema mismatch and correction patch recovery retained;outputs
  unchanged during validation. No runtime/frontend/reading-room work.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-04/sweeping-basic/`.
  Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-04/validation.json`.
  One complete production article,one partial,27 untouched,eight sealed pilot bodies,
  five heading classifications remaining. Whole August remains in progress.
- Next:separate full 청소32–36 assembly from immutable batch03/batch04 exports.

### August full 청소32–36 complete, 2026-10-12

- Separate full assembly preserves both native exports exactly:100 regions,99 text
  crops,one original screenshot,91 blocks,543 physical listing rows and90 numbered
  BASIC entries. All208 hex rows/1664 candidate bytes and33 source flags retained.
- Existing wrapped-listing-v1 projects native within-segment wraps and unnumbered
  monitor/hex rows correctly. Initial namespaced mode rejected those native wraps
  before creating output;failure and mode recovery retained. No runtime code changes.
- All original metadata,native files,text/review/flag ranges,physical listing byte
  partition and logical label sequence pass. Listing equals exact native byte
  concatenation; independent assembly rebuild identical.16,790 pilot files unchanged.
- Export:`build/pdf-restoration/13-1984-08-adaptive/sweeping/`.
  Audit:`private/pdf-restoration/13-1984-08-adaptive/sweeping-assembly-validation.json`.
  Human acceptance,character-perfect proofreading,source bytes and execution pending.
- Two complete production articles,no partials,27 untouched,eight sealed pilot bodies,
  five heading classifications remaining. Whole August remains in progress.
- Next:죽음의 스키37–38 production selection/source repairs from sealed pilot evidence.
  JSON/assets only;reading room not rebuilt. Unrelated web edit remains outside commits.

### August 죽음의 스키 production reuse complete, 2026-10-12

- Selected existing Qwen pilot aug-02-A for dense MSX BASIC,then rechecked all26
  source crops,full37–38 and boundary39. Repaired one source wording normalization:
  수림→printed 수렵. Printed 올리면,SOUDN,Puah and loop-variable anomalies retained.
- Separate production export has26 regions,23 text crops,three original images,
  18 blocks,80 physical rows/68 numbered entries and11 source flags. Graphic title
  and borders remain image-backed editorial placeholders,not literal runnable strings.
  Both pilot arms and their residual-error comparison remain sealed and unchanged.
- No new OCR or local tokens. Source/crop/request hashes,reused raw text/settings/
  positions,all stop outcomes,text/review/flag ranges,exact physical/logical indexes
  and independent byte-identical rebuild pass. Listing bytes unchanged from selected
  pilot;22 other regional transcriptions identical.16,790 original pilot files intact.
- Export:`build/pdf-restoration/13-1984-08-adaptive/death-ski/`.
  Audit:`private/pdf-restoration/13-1984-08-adaptive/pilot-aug-02/validation.json`.
  Copied bundle's missing full-page path caused a retained validator lookup failure;
  audit now uses original separate source-pages files. No runtime code changes.
- Three complete production articles,27 untouched,seven pilot bodies still pending
  production selection,five heading classifications remaining. All eight pilot pairs
  preserved. Human acceptance remains pending;whole August in progress.
- Next:verify 이열치열39 against40–41,then restore prose and FC-100 BASIC separately.
  No reading-room rebuild;unrelated web change remains outside commits.

### August 이열치열39–40 complete, 2026-10-12

- Source40 confirms continuation390–820 and final820 END;41 starts 지능검사.
  Lower40 academy ad excluded.25 regions/22 blocks retain complete prose and97
  physical BASIC rows/73 printed labels100–820. All seven crop panels inspected.
- Mixed route:18Q dense code,sevenT prose/title crops including reused0.357s probe.
  Actual new T calls6. Probe mostly readable;neighbors had scattered Latin garbage,
  all corrected in one selected source pass. Q physical wraps repaired in two crops;
  literal message strings,missing closing quotes,code errors and8/B candidate retained.
  Eleven source flags;character-perfect/source-byte/execution verification pending.
- Initial worker failed sandbox local-socket creation after T recognition. Approved
  resume reused all seven T results and ran18Q;no successful inference repeated.
  Failed worker and recognition times retained separately. Export suffix/runtime-root
  configuration failures happened before output creation;recorded recovery changes
  export configuration only. Runtime pipeline unchanged.
- Source/crop/request hashes,18 stop outcomes,all regional characters,prose joins,
  text/review/flag ranges,97 physical/73 logical byte partitions and exact printed
  labels pass. Independent rebuild identical;16,790 sealed pilot files unchanged.
- Q7,583 local tokens/15.631s;T2.053s plus reused probe0.357s. Paid preparation,
  recovery,correction,export and reporting windows recorded;local money weight zero.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-05/heat/`.
  Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-05/validation.json`.
  Four complete production articles,26 untouched,seven pilots pending selection,
  five heading classifications remaining;zero human accepted. Whole August in progress.
- Next:verify 지능검사(IQ TEST)41–42 against43,then restore prose/FC-100 listing.
  JSON/assets only;no reading-room rebuild. Unrelated web edit remains outside commits.

### August 지능검사41–42 complete, 2026-10-12

- Full41–42 inspected;2250 CLS ends listing above bookstore ad;43 begins next title.
 32 regions/28 blocks preserve133 physical code rows:two independent level1 examples
 in4 rows,plus main1000–2250 in129 rows/126 visible numbered statements.128 numbered
 entries total. Canonical TOC title/byline unchanged;printed IQ TEST/김선일 retained.
- Fixed30Q body/formula/code and2T short title/byline;existing neighboring T degradation
 determines body route without another probe. Q15,235 local tokens/33.584s;T0.240s.
 No retries or duplicate successful inference. All eight source panels inspected.
- Pre-OCR42 margins widened to restore leading digits. Projection missed faint1970/
 2070 and split1980;source-inspected32-row right column and whitespace seams recorded.
 Initial/revised maps and crops preserved. No source characters inferred from numbering.
- Eleven flags retain glyph boxes,faint Hangul,source =<,branch1920,repeated2060 A=1,
 main2090 +X versus independent example-X,punctuation and literal prompt uncertainties.
 Q /69 restored to source +60;logical contradictions not repaired. No execution/byte claim.
- Source/crop/request hashes,30 stop outcomes,regional characters,all text/review ranges,
 explicit prose seams,133 physical/128 logical byte partitions and printed labels pass.
 Independent rebuild identical;16,790 sealed pilot files unchanged. Human pending.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-06/iq-test/`.
 Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-06/validation.json`.
 Five complete production articles,25 untouched,seven pilots pending production selection,
 five heading classifications remaining;whole August in progress. No reading-room rebuild.
- Next:위험천만한 달표면 착륙43–45.46 boundary verified;preserve MSX graphics as source
 images/unverified glyph candidates and printed physical listing without program repair.

### August 위험천만한 달표면 착륙43–45 complete, 2026-10-12

- Complete three-page article ends20040 DATA;46 begins 그래픽용 서브루틴.
 32 regions retain29 text crops,26 ordered blocks,three original images and140
 physical BASIC rows/136 numbered statements. All nine enlarged panels inspected.
- Mixed route27Q prose/code,2T title/byline;all29 calls completed without retries.
 One selected correction restores P from Q F and printed SOUDN from normalized
 SOUND. Printed =<,Scrool,missing second A$,address expressions and final100 remain.
- Thirty-two source flags and35 image-backed editorial markers preserve unresolved
 overprinted operators,repeated glyph counts,blank widths and MSX graphic strings.
 Original definition/title images are authoritative;markers are not literal code.
 Actual140 physical rows replace projection's missed short/graphic bands;initial
 maps/crops and repaired figure-edge evidence retained. No program repair.
- Source/crop/request hashes,27 stop outcomes,all source-character/text/flag ranges,
 physical/logical byte partitions and exact printed labels pass. Independent rebuild
 identical;nine prior production packages and16,790 sealed pilot files verified.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-07/lunar-lander/`.
 Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-07/validation.json`.
 Six complete production articles,24 untouched,seven pilots pending production
 selection,five heading classifications remaining;zero human accepted.
- Next:inspect full 그래픽용 서브루틴 extent from46 before bounded opening46–51.
 Whole August remains in progress. JSON/assets only;reading room unchanged.

### August 그래픽용 서브루틴46–50 complete, 2026-10-12

- Full46–56 inspected:article ends50;51–54 advertisements,55 education divider,
 56 next math article. Lower46 bookstore ad excluded. Complete five-page package
 retains90 regions/86 text crops,74 blocks,four original images and277 physical
 listing rows:213 assembly,42 hex including prompt,22 BASIC. Three independent
 BASIC tests retain20 numbered statements;41 hex rows retain328 candidate values.
- All25 original/nine revised panels inspected. Fifteen crop boundaries moved
 off faint character tails/semicolon fragments before inference. Initial schema
 failure/maps/crops retained;source counts replace projection misses/touching rows.
- Mixed route69 successfulQ,three length-loop failures and17T calls including
 three bounded fallbacks. Failed raw responses/request hashes/tokens preserved;
 successful crops never repeated. Clear46 prose probe produced Latin substitutions,
 so Q retained for body. One selected correction pairs flattened address/object/
 mnemonic columns and restores source lettering/values. Tabs are reading separators.
- Preserve printed F00H,F011H,1FFFH,duplicate SCREEN X,X,Y,byte/mnemonic differences,
 Test Program1 under list2,and50's physical44,1,18,738 continuation.29 source flags;
 no code execution,original encoded bytes or character-perfect proofreading claim.
- SuccessfulQ37,469 local tokens/85.975s;allQ40,179 including2,710 failed tokens.
 Failed server compute15.747s separate from unmeasured failed client wall duration.
 T1.805s plus0.316s probe;local monetary weight zero. All paid work windows retained.
- Export block-ID collision caught before output;unique region-based overrides fix
 configuration without modifying raw evidence. First address audit found two final
 O/0 label conversions;unpromoted export preserved,only F0C0/F0D0 labels repaired.
 Data values unchanged. All source/crop/request/UTF-8/prose/row indexes and exact
 rebuild pass;ten prior production packages/16,790 sealed pilot files unchanged.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-08/graphics-subroutines/`.
 Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-08/validation.json`.
 Source55 education divider classified non-owning with ten canonical children.
 Seven production articles complete,23 untouched,seven pilots pending selection,
 four heading classifications remaining;zero human accepted. August incomplete.
- Next:verify 수학을 통한 논리학습56–59 against next logo60,then restore full
 prose/math/listing. JSON/assets only;reading room and unrelated web edit unchanged.

### August 수학을 통한 논리학습56–59 complete, 2026-10-12

- Complete source56–59 inspected through logo60–61 boundary.83 regions retain
 79 text crops,61 ordered blocks and four original figures:prime sieve,two division
 diagrams and SWAP example. Five independent BASIC groups preserve140 physical
 rows/138 numbered statements;list2 line1210 spans three physical rows.
- All22 original crop panels and revised panel15 inspected. Two shared prose
 seams moved into white gaps before OCR;initial maps/crops retained. Source list3
 final crop has three code rows plus a nontext horizontal band,not four code rows.
- 61 successfulQ/18T tasks,no failures,retries or new probes. Prior same-font prose
 evidence informed routing. Q30,308 local tokens/59.234s;T1.340s. Local monetary
 weight zero;preparation,correction,export/recovery and reporting windows retained.
- Printed 솟수,3534,2767,G.C.M./Greatest Common Measure,PRINT dot and two faint
 comma candidates retained. Fractions/exponents are image-backed reading aids;
 eleven comment-dash markers defer exact glyph counts.29 DATA values retained.
 31 source flags;human proofreading,encoded source bytes and execution unverified.
- Two local correction-script syntax failures retained. Initial identical exports
 preserved before joining the sentence across figure3;regional readings unchanged.
 First validator overcounted dash markers13;source audit confirms11 and corrected
 only the validator expectation. No OCR repeated or raw evidence overwritten.
- Source/crop/request/stop checks,complete character coverage,UTF-8 review ranges,
 independent five-group label/physical/logical indexes and exact rebuild pass.
 Eleven prior production packages and16,790 sealed pilot files unchanged.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-09/math-logic/`.
 Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-09/validation.json`.
 Eight production articles complete,22 untouched,seven pilots awaiting selection,
 four heading classifications remaining;zero human accepted. August incomplete.
- Next:inspect complete 로고에로의 초대60 onward through BASIC65 boundary before
 mapping. JSON/assets only;reading room and unrelated web edit unchanged.

### August LOGO60–64 raw preparation complete, 2026-10-12

- Full60–65 inspected:printed 로고 강좌/연재4회 ends64 with references;
 canonical 로고에로의 초대 identity unchanged.101 text regions mapped across
 five pages,with35 command/output crops and182 unnumbered physical source rows.
- All28 original/ten revised panels inspected.16 crop geometries repaired before
 OCR;initial maps/crops and two failed whitespace-search attempts retained. One
 tightly typeset END/prose boundary has only a one-pixel gap,manually inspected.
- Cleaner prose warranted one bounded Tesseract probe:p63r02 retained every word
 with two punctuation errors.58T results include that unchanged reused probe;
 43Q crops cover code/formulas/inverse heading. No OCR failures or retries.
 Q22,753 local tokens/62.346s;T9.572s includes0.200s probe. Probe is not repeated
 or added twice to total recognition time. Local monetary weight zero.
- Raw crop/request hashes and43 stop outcomes pass. Evidence:
 `private/pdf-restoration/13-1984-08-adaptive/batch-10/raw-ocr-audit.json`.
 Source correction and production export remain pending;aggregate stays eight
 restored articles,22 untouched/seven pilots pending selection. Next:correct LOGO
 prose,commands,displayed results and source anomalies,then export/validate/commit.

### August LOGO60–64 production checkpoint complete, 2026-10-12

- Source correction/export is complete after the sealed raw checkpoint.101 text
 regions retain98 ordered blocks and35 command/output crops.182 unnumbered
 physical rows form34 independent groups and176 source lines;six printed wraps
 retain explicit physical parts without inventing executable joined code.
- Canonical TOC identity is 로고 강좌,maso-1984-08-toc-0011;unchanged. Source
 OTUPUT,BUTFIST,result5,단점,Programing and the open-parenthesis-shaped candidate
 in the PRINT example remain literal.30 unresolved entries retain source evidence.
 Human proofreading,source encoded bytes and program execution remain unverified.
- The bounded Tesseract probe retained words,but other prose crops required many
 Latin-letter substitutions to be corrected against the source. One source pass
 corrected the selected drafts;no whole-article second-engine correction or OCR
 rerun.43Q/58T results include one reused probe;recognition time unchanged.
- Source/crop/request/stop outcomes,complete regional character coverage,UTF-8
 review ranges,182 physical/176 source-line partitions and all six continuations
 pass. Native and independent rebuild are byte-identical.12 prior production
 packages and16,790 sealed pilot files unchanged. Human acceptance pending.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-10/logo-invitation/`.
 Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-10/validation.json`.
 Nine production articles complete,21 untouched,seven pilots awaiting selection,
 two headings classified/four remaining;zero human accepted. August incomplete.
- Next:source-check 기초 테크닉 코너/PASSWORD & LOGIN65–68 against English69,
 then reuse selected immutable aug-04 pilot in a separate production revision.
 JSON/assets only;reading room and unrelated web change remain untouched.

### August PASSWORD & LOGIN65–68 production selection complete, 2026-10-12

- Full65–69 boundary and all79 pilot regions rechecked:73 text crops and six
 original images retain71 ordered blocks. Source69 begins 영어 교육용 시스템.
 Canonical 기초 테크닉 코너 identity/byline/parent unchanged.
- Reuse immutable Qwen aug-04-A draft/raw/maps/runtime;one source-confirmed
 residual repair restores first PASWORD in p68r13. Other72 regional transcriptions
 and all listing bytes unchanged. No new OCR/local tokens,crop repairs or dual
 correction. Original paired pilot remains sealed with its known quality findings.
- Ten independent code groups retain119 physical rows/103 numbered statements,
 eight nonblank continuations,five blank rows,]LIST prompt and two monitor commands.
 Original incomplete PRINT"LOGIN,WELLCOME,PASS WORD,target220 and INKEY$(1)
 preserved.14 source flags retain literal/space uncertainties;no execution or
 encoded-byte certification. Mandatory human review remains pending.
- Source/crop/request/stop outcomes,exact reused raw/stage files,complete regional
 character coverage,UTF-8 review ranges,independent source-label counts and physical/
 logical/unnumbered partitions pass. Exact rebuild,13 prior production packages
 and16,790 sealed pilot files unchanged. Two validator assumptions corrected with
 initial scripts retained:pilot stages lack result.json;Counter requires row keys.
 No source or export changed during validator recovery.
- Export:`build/pdf-restoration/13-1984-08-adaptive/password-login/`.
 Audit:`private/pdf-restoration/13-1984-08-adaptive/pilot-aug-04/validation.json`.
 Ten production articles complete,21 untouched,six pilots awaiting selection,
 two headings classified/four remaining;zero human accepted. August incomplete.
- Next:inspect full English education article69 onward against CP/M90,then
 restore a bounded opening segment and retain remaining source scope for assembly.
 JSON/assets only;reading room and unrelated web edit remain untouched.

### August English education69–74 raw preparation complete, 2026-10-12

- Verified full English education article69–87 against22 source views69–90.
 Prose extends through76;LIST1 spans76–81,LIST2 spans81–84 andLIST3 spans84–87.
 Advertisements88/89 excluded;CP/M begins90. Opening69–74 maps six pages with
 16 outside-map lookups,within the bounded checkpoint limits.
- All27 original/14 revised panels inspected.24 distinct crop geometries repaired
 before recognition;initial maps/crops retained. A pre-export schema error used
 unsupported table kind;existing other-region table convention restored without OCR.
- 90 text crops routed78T/12Q;12 original images preserve the photograph and
 screens1–11. No probe,cache reuse,recognition failure or retry. Q8,367 local tokens
 and49.761s;T13.623s. Local monetary weight zero;timing is diagnostic only.
- Source/crop/map/request hashes,raw bundles,runtime pins and all12 stop outcomes
 pass;14 prior production package pins and16,790 sealed pilot files unchanged.
 One validator recovery restricts usage sums to scalar token counters;initial
 script retained. No source text or OCR changed during that recovery.
- Raw audit:`private/pdf-restoration/13-1984-08-adaptive/batch-11/raw-ocr-audit.json`.
 Source correction/export pending. Totals remain ten complete,zero partial,
 21 untouched,six pilots pending selection,two headings classified/four remaining;
 zero human accepted. English is not counted as restored from raw drafts.
- Next:source-correct69–74,especially the control-character table,Korean bitmap
 fragments and independent BASIC examples;then export/validate the opening.
 Restore remaining75–87 and assemble all69–87 separately. August incomplete.

### August English education69–74 production segment complete, 2026-10-12

- Corrected/exported90 selected mixed drafts across69–74 of verified full69–87.
 102 regions retain86 ordered blocks,12 original images and91 review ranges.
 Four regular joins and a split projection preserve five source boundaries;
 screen10's following paragraph remains after its original figure/caption.
- Three independent BASIC examples retain eight physical rows,three printed
 labels650/300/197 and five wraps. Broken Hangul fragments are explicit image-
 backed reading aids;hidden control characters and exact source bytes unverified.
 The ruled table retains15 rows/90 cells/16 blanks and three column groups.
- Printed PERFEDT/PERFECT,CIRL-A/CTRL-A,captionCTRL-K/headerCTRL-N,raised31,
 round mark beforeCALL and historical spellings retained.27 source uncertainties;
 original screens retain SYNTAX ERROR and overlapping Hangul/English output.
- Initial export omitted a review range crossing two projected blocks. Both
 unpromoted exports and original notes/validator/script retained;split only that
 note into two ranges. All regional transcription,raw OCR,crops and maps unchanged.
 No new inference or dual correction;12Q/78T recognition costs unchanged.
- Source/crop/request/stop checks,exact regional character coverage,UTF-8 review
 ranges,independent table/listing counts and source row associations pass. Exact
 rebuild,14 prior production packages and16,790 sealed pilot files unchanged.
 Export:`build/pdf-restoration/13-1984-08-adaptive-batch-11/english-education/`.
 Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-11/validation.json`.
- Ten production articles complete,one partial,20 untouched,six pilots awaiting
 selection,two headings classified/four remaining;zero human accepted. August
 incomplete. Source75–87 and full69–87 assembly remain mandatory.
- Next:reuse verified extent/views and map75–80 within six-page limit. Preserve
 prose ending/screens and LIST1 opening;81–87 follow in later natives. Outgoing
 74다음 문 fragment awaits source-confirmed75 join. JSON/assets only.

### August English education75–80 raw preparation complete, 2026-10-12

- Full69–87 extent reused from the pinned opening;75–81 full views reinspected.
 Six mapped75–80 pages and one outside-map lookup81. Prose ends76;LIST1 ends81,
 LIST2/3 continue81–87. Full69–87 assembly remains required.
- All32 original panels/six overlays and five original figures reviewed. No crop
 geometry repairs or probe. Screen13 has no visible printed caption;source prose
 identifies it without inventing caption text. Original map/crops retained.
- 123 text regions:28 initial Tesseract prose/headings/captions and95 Qwen code
 attempts. 93Q/30T final drafts;2 capped Qwen attempts preserved with
 same-crop bounded Tesseract fallbacks,zero successful-crop repeats/cache reuse.
 Q46,329 local tokens includes failures;successful recognition
 225.609s,failed server compute
 26.079s andT4.998s remain separate diagnostics.
 Local monetary weight zero;failed client wall duration remains unmeasured.
- Both capped generations looped on repeated bitmap divider glyphs. Later
 same-pattern crops should use the documented repeated-glyph Tesseract exception,
 retaining source images and correction-stage counts;no general cost winner inferred.
- Source/crop/map/request hashes,raw bundles,runtime pins,stop/fallback outcomes
 and continuous column coverage pass. 15 prior production packages and16,790
 sealed pilot files unchanged.542 projected ink bands are segmentation evidence,
 not a verified physical listing-row count;independent source count is pending.
- Raw audit:`private/pdf-restoration/13-1984-08-adaptive/batch-12/raw-ocr-audit.json`.
 No production export yet. Totals remain ten complete,one partial,20 untouched,
 six pilots pending selection,two headings classified/four remaining;zero human
 accepted. Human proofreading,source bytes and historical execution unverified.
- Next:correct75–80 prose and LIST1 physical rows,export/validate/commit the middle.
 Then restore81–87 and assemble all69–87. August incomplete;JSON/assets only.

### August English education75–80 production segment complete, 2026-10-12

- Corrected/exported123 selected mixed drafts across75–80 of full69–87.128 regions
 retain122 ordered blocks,five original images and123 text review ranges. Prose
 75원하/76는 joins;incoming75제로 awaits74다음 문 in full assembly.
- LIST1 retains553 ink-bearing physical rows,331 numbered statements and222 wraps
 in one program group. Source1463/2370 cross columns with four parts each.
 Indented2850/3003 targets and final argument digit2 remain continuations,not labels.
- Source correction caught two initial cuts bisecting a lone parenthesis/digit2.
 Four crops repaired/re-inferred once;all original raw evidence/maps and two capped
 Qwen attempts preserved. All32 original panels/four revised crops reviewed.
 Final direct ink-component check passes;542 projection bands were not row counts.
- Original93Q/30T selected results plus four Q crop repairs:97 successful Q
 inferences,2 failed Q attempts and30T calls. Q48,392 local tokens includes all
 failures;successful Q client recognition236.341s,T4.998s and failed Q server
 compute26.079s remain separate diagnostics. Local monetary weight zero.
- Source580,L-25,DR-shaped operator,incomplete RUN TEST.D,PERFECT filename and
 historical spellings retained.112 source flags include marked bitmap/glyph aids;
 hidden controls,exact source bytes,full proofreading and execution unverified.
 Screens12–15/photo retained;screen13 has no invented printed caption.
- Original optional component diagnostic lacked scipy;direct pixel method recovered
 without dependency installation. Validator figure-field lookup corrected with
 initial script retained;no source/export change. Stale worker console count6 is
 retained;four actual repair stages and authoritative JSON count4 verified.
- Source/crop/model request hashes,stop/fallback outcomes,exact character/UTF-8
 review ranges,independent physical/logical partitions and byte-identical rebuild
 pass.15 prior production packages and16,790 sealed pilot files unchanged.
 Export:`build/pdf-restoration/13-1984-08-adaptive-batch-12/english-education/`.
 Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-12/validation.json`.
- Totals remain ten complete,one partial English now69–80,20 untouched,six pilots
 pending selection,two headings classified/four remaining;zero human accepted.
- Next:map81–86 within six-page limit,then87 and full69–87 assembly. Reuse full
 extent and successful evidence;catch short glyph rows before OCR and use documented
 repeated-glyph exception. Whole August incomplete;JSON/assets only.

### August English education81–86 raw preparation complete, 2026-10-12

- Source-verified full69–87 extent reused;81–87 whole views reinspected. One article,
 six mapped81–86 pages and one outside-map lookup87. LIST1 ends81,LIST2 ends84,
 LIST3 continues through87;full69–87 assembly remains required.
- All37 original/nine revised panels,six original/three revised overlays and two
 wider source details inspected. Sensitive segmentation moved two cuts before OCR.
 24 distinct crops widened;12 narrowed again to exclude a listing frame. Original
 and intermediate maps/crops plus failed preflight diagnostic retained. Final
 eight-neighbor ink check passes156 boundaries;zero crossing components.
- 144 text regions:140 initial Qwen code attempts and four Tesseract calls(two
 clear labels/two repeated-bitmap-divider exceptions). Final139Q/5T drafts;
 One capped Qwen attempt retained with a bounded same-crop T fallback.
 No successful-crop repeats,probe or cache reuse. All recognition evidence sealed.
- Q66,289 local tokens includes failures;successful Q client recognition391.466s,
 T1.098s and failed Q server compute15.645s are separate diagnostics. Local
 monetary weight zero;failed client duration remains unmeasured. A capped crop
 repeated escaped spaces for a Hangul output label;no universal routing winner.
- Source/crop/map/request hashes,raw bundles,runtime pins,all stop/fallback outcomes
 and continuous column coverage pass.16 prior production packages and16,790
 sealed pilot files unchanged.821 projection bands are segmentation evidence,
 not certified physical-row counts;independent source correction remains pending.
- Preflight recovery excludes the frame without OCR. A relative-path pin helper
 failed after geometry update;resumed request/panel generation with absolute path.
 An empty raw work window contains bookkeeping only;no duplicate inference.
- Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-13/raw-ocr-audit.json`.
 No production export yet. English production coverage stays69–80. Totals remain
 ten complete,one partial,20 untouched,six pilots awaiting selection,two headings
 classified/four remaining;zero human accepted. August incomplete.
- Next:correct/export/validate81–86,then restore87 and assemble69–87. Preserve
 physical continuations32 across81/82,5020 across83/84 and130 across84 columns.
 Hidden control bytes,full proofreading and execution unverified;JSON/assets only.

### August English education81–86 production segment complete, 2026-10-12

- Corrected/exported144 selected drafts across81–86 of full69–87.144 regions retain144 ordered blocks,two listing titles and144 text review ranges;no figures.
- Three groups preserve827 ink-bearing physical rows,493 printed labels and334 wraps:LIST1 ending88/59/29,complete LIST2 370/200/170 andLIST3 opening369/234/135. All37 final panels source-reviewed;projection bands were not substituted for physical row counts.
- Source32 crosses81/82 with four parts,5020 crosses83/84 with four and130 crosses84 columns with two. Short0),3:,000,190 and2: fragments remain continuations,not fabricated labels. LIST3 ends this native at6126;87 begins6127.
- Historical spellings,HTA/PRI/PRIN/GOT truncations,580,L-25,265GOTO250,620GOTO3820 and uncertain punctuation retained.118 source flags preserve bitmap reading aids and uncertain glyphs. Clearer LIST3 text does not replace faint independent LIST1 source readings.
- No new recognition during correction/export.139 successful Q calls/five T calls plus one preserved capped Q attempt;66,289 local Q tokens include the failure. Local monetary weight zero;timings remain separate,noncausal diagnostics.
- Source/crop/model request hashes,stop/fallback outcomes,exact regional character/UTF-8 ranges,independent physical/logical partitions and byte-identical rebuild pass. All1,739 sealed raw files,16 prior production packages and16,790 pilot files unchanged.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-13/english-education/`. Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-13/validation.json`. Human acceptance,full proofreading,encoded bytes and execution remain unverified.
- Ten production articles complete,one partial English now69–86,20 untouched,six pilots pending selection,two headings classified/four remaining;zero human accepted. August incomplete.
- Next:restore87 and validate the ending,then separately assemble full69–87 from immutable native11–14. Join74다음 문/75제로;merge LIST1/LIST3 program indexes. JSON/assets only;no reading-room rebuild.

### August English education87 production ending complete, 2026-10-13

- Corrected/exported24 selected drafts on87,the source-confirmed LIST3 ending of full69–87.24 regions/blocks and24 review ranges retain144 ink-bearing physical rows,80 printed labels and64 wraps;no figures. Allsix original/three revised panels andtwo wider boundary details inspected.
- Fresh enlarged source reads firstlabel6129,superseding earlier provisional6127. Final10040RETURN ends the article;88 is unrelated advertising.7030 target600/0 remains a two-row continuation,not a new label.21 source flags preserve historical bitmap fragments,repeated separators and small trailing mark after6465.
- Preflight component assertion found a clipped10040 edge and6740 final pixels. Sequential orchestration mistakenly started recognition after that failure;worker explicitly stopped(exit130). Alloriginal maps/crops,three completed Q stages,two T drafts andinterrupted fourth request retained. Final12 right crops widened;one seam moved2063→2066.26 final boundaries pass withzero ink crossings.
- Resume reuses three unchanged successful Q stages exactly;19 new Q calls andtwo revised T calls complete the final22Q/twoT draft set. Actual known recognition:22 successful Q calls,four total T calls andone interrupted submitted Q request. Known Q usage10,622 tokens;interrupted response/token/compute data unavailable,explicitly unknown rather than zero. T total1.081s;local monetary weight zero.
- Source/crop/model hashes,original/final geometry,allselected stop outcomes,exact regional character/UTF-8 ranges,independent physical/logical partitions andbyte-identical rebuild pass.327 sealed raw/recovery files,17 prior production packages and16,790 pilot files unchanged. No new OCR during correction/export.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-14/english-education/`. Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-14/validation.json`. Human acceptance,full proofreading,source encoded bytes andhistorical execution unverified.
- Ten articles complete,one partial English withall69–87 native coverage,20 untouched,six pilots awaiting selection,two headings classified/four remaining;zero human accepted. English remains partial until separate fullassembly;August incomplete.
- Next:assemble full69–87 from immutable native11–14,join74다음 문/75제로 andmerge LIST1/LIST3 indexes. Then CP/M begins90,whose complete extent must be inspected before mapping. JSON/assets only;no reading-room rebuild.

### August full English education69–87 assembly complete, 2026-10-13

- FullEnglish69–87 assembled from exact validated native11–14 manifest pins.398 regions retain381 selected regional readings,375 ordered blocks,17 original images and382 review ranges. Fullarticle source coverage/readable availability verified;no missing/deferred pages.
- Six listing groups preserve1,532 ink-bearing physical rows,907 printed labels and625 wraps. Three independent examples remain separate;LIST1 merges76–81(641rows/390labels),LIST2 retains81–84(370/200),LIST3 merges84–87(513/314). Physical/listing bytes equal immutable native concatenation;all logical partitions andshort/cross-column/page continuations pass.
- One cross-native prose join preserves74다음 문/75제로 across originalscreen11 andits caption. Existing interrupted-wrapped adapter retains exact interruption order. Initial adjacent-only recipe failed beforeexport;recipe/failure retained,source andOCR unchanged.
- Structured source index retains control table15rows90cells16blankcells,three column groups andglobal UTF-8 cell/row ranges.278 original source flags andalloriginal native metadata remain unchanged. Source87 firstlabel6129 supersedes earlier provisional6127 explicitly;prior native metadata not rewritten.
- Four native packages copied byte-identically;source/canonical identity,coverage,allreview/table/listing ranges,independent exact rebuild,18 prior production packages,allfour raw inventories and16,790 sealed pilot files pass. No new OCR,mapping,frontend/browser orreading-room build duringassembly.
- Package:`build/pdf-restoration/13-1984-08-adaptive/english-education/`;source index:`build/pdf-restoration/13-1984-08-adaptive-english-source-index/source-index.json`;audit:`private/pdf-restoration/13-1984-08-adaptive/english-assembly-validation.json`. Human acceptance,fullproofreading,hidden controls,encoded bytes andhistorical execution remain unverified.
- Eleven production articles complete,zero partial,20 untouched,six pilots awaiting selection,two headings classified/four remaining;zero human accepted. August issue remains incomplete.
- Next:CP/M begins90. Inspect completeactual extent andfollowinggraphics title(canonical99) before boundedmapping;then adaptiveOCR,source correction/export/validation. Six-page/two-article and20outside-map limits remain;JSON/assets only.

### August CP/M90–95 raw preparation complete, 2026-10-13

- FullCP/M90–97 source extent verified from11 fresh90–100 whole views before mapping. Actual nextgraphics title98 differs fromcanonical99;identities unchanged. One article,six mapped90–95 pages,five outside-map lookups96–100. Ending96/97 andfullassembly remain.
- 163 regions retain154 text drafts,nine source images,27 code regions andfive structured tables. Clear prose/headings/captionsT;dense BASIC,command syntax andtable valuesQ. Source program/console/output examples stay separate. FullRESUME/ERASE images retain vertical omission marks;CALL example label retained separately.
- All42 original/31 revised panels andsix original/six final overlays inspected. Forty-nine original text crops repaired before recognition;three needed a second revision. Two full example images andone printed label added. Initial glyph splits,command/body andprogram/console boundaries repaired. Final616-boundary diagnostic haszero glyph crossings;four explicitly reviewed crossings are the shaded serial label background. Original/intermediate geometry,crops anddiagnostics retained. No recognition preceded finalgate.
- 63 successful Q calls and91T calls complete154 selected drafts;zero failures,retries,fallbacks,probe orcache reuse. Q28,988 local tokens(25,316prompt/3,672output),local monetary weightzero;recognition/preparation/recovery durations remain separate noncausal diagnostics.
- Source/crop/model/map/request hashes,allstop outcomes,runtime/raw bundles andfull extent pins pass. All19 prior production packages and16,790 sealed pilot files unchanged. Raw evidence sealed;physical listing rows andtable cells await independent source correction.
- Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-15/raw-ocr-audit.json`. No production export yet. Eleven articles complete,zero partial,20 untouched,six pilot selections pending,two headings classified/four remaining;zero human accepted. August incomplete.
- Next:correct/export/validate90–95,then restore96–97 andassemble90–97. Source spellings/errors,small glyphs,encoded bytes andhistorical execution remain unverified;JSON/assets only,no reading-room rebuild.

### August CP/M90–95 production opening complete, 2026-10-13

- Corrected/exported154 selected drafts across90–95 ofsource-verifiedfull90–97.163 regions retain147 ordered blocks,nine originalimages and154 textreviewranges. Seven sourceprose/listboundaries preserve90/91boot instructions,91갯/수,91/92display commands,92등/을 and95번/호.
- Twenty-six independent groups retain61 actualprogram/consolephysicalrows:19 printedlabels,four programwraps and38 unnumberedrows. Eight numberedprogram groups stay separate from18 command/consoleexamples. PRINT USING decimal2./45,format-string wrap andTRY/AGAIN remain physicalcontinuations. FullRESUME/ERASE sourceimages retain omitted-span dots without invented statements.
- Five original ruledtables retain26 data rows104cells/six semanticblankfields withglobal UTF-8 row/cell indexes. Bytecounts withparentheses remain inoneheadercolumn;HGR colors retain final4흑색 andblankothercolumnareas. Forty sourceflags retainLESE,TRL-13,CTR-C,APA,의위,표매팅,PRO3/PROG3,formatglyphs,returnarrows,sourceclaims andsmallglyph uncertainties.
- No new recognition duringcorrection/export:63 successfulQ/91T calls,zero failures/retries/fallbacks,28,988 localQtokens. First export's optionalunnumberedexampleindex includednumberedrows;unpromotedpackage/rebuild/originalbuilder preserved. Scopedprivatebuilderfix leaves61physical/19numbered indexes unchanged andprojects only38actualunnumberedrows into35 sourceexamples. Source text/listing/images unchanged. Initialvalidatorfigurefield lookupfailure retained;correctregion_ids check passes.
- Source/crop/model hashes,exactregional/table/listing/source-reference partitions,canonicalidentity andbyte-identical rebuild pass. All1,657 sealedraw/preflightfiles,19 priorproduction packages and16,790 pilotfiles unchanged. Humanacceptance,fullproofreading,sourcebytes andhistoricalexecution unverified.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-15/cpm-reviewed/`;sourceindex:`build/pdf-restoration/13-1984-08-adaptive-cpm-source-index-15/source-index.json`;audit:`private/pdf-restoration/13-1984-08-adaptive/batch-15/validation.json`.
- Eleven articles complete,onepartialCP/M90–95,19untouched,sixpilotselectionspending,twoheadingsclassified/fourremaining;zerohumanaccepted. Augustincomplete.
- Next:restoreCP/M96–97 frompinned full90–97extent,then separatelyassemble90–97 fromimmutable natives. Nextgraphicsactualtitle98 differsfromcanonical99;completeextentinspection stillrequired beforeitsmapping. JSON/assets only;no reading-roombuild.

### August CP/M96–97 production ending complete, 2026-10-13

- Ending96–97 uses the pinned full90–97 extent from native15;96/97 andnext actualgraphics title98 reinspected before mapping. One article,two mappedpages,one outside-map lookup. All11original/five revisedpanels andtwo original/two finaloverlays reviewed. Seven crops repaired before recognition;all168 finaledges pass withzero inkcrossings. Original geometry/crops/diagnostic retained.
- 42 regions retain41 orderedblocks and42 textreviewranges. One samepage columnjoin preserves필드의 개념이/희박하기. Eight independent numberedexamples andtwo command/session groups retain35 physicalrows,26 printedlabels,two wraps andseven unnumberedrows. AUTO100/110 displays remain prose;MERGE interaction remains independent. No new figures or tables.
- 24Q/18T calls complete all42 drafts withzero failures,retries,fallbacks,cache orprobes. Q13,895 localtokens(12,223prompt/1,672output);local monetaryweightzero. Preparation,recognition,correction/export andevaluation durations remain separate noncausal diagnostics. No furtherOCR during correction/export.
- Twenty sourceflags preserveX2/X2,unbalancedHPLOTdelimiter,MICRSOFTWARE,quotedmodes,I/1,semicolon/colon andspacing candidates,AppleSoft100/120/130/140 labels and10/20 prose references. Sourcecrop pixels/raw/model/map hashes,exactregional/listing/review partitions,canonicalidentity andbyte-identical rebuild pass. All20 priorproduction packages,allnative15 raw evidence and16,790 sealedpilot files unchanged.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-16/cpm/`;sourceindex:`build/pdf-restoration/13-1984-08-adaptive-cpm-source-index-16/source-index.json`;audit:`private/pdf-restoration/13-1984-08-adaptive/batch-16/validation.json`. Initialvalidatorlogical-row fieldlookupfailure retained;correctlisting_id check passes withoutsource/exportchanges. Humanacceptance,fullproofreading,encodedbytes andexecution unverified.
- Eleven articles complete,onepartialCP/M withall90–97 nativecoverage,19 untouched,six pilotselections pending,two headings classified/four remaining;zero humanaccepted. August remains incomplete.
- Next:separatefullCP/M90–97assembly from immutable natives15/16,then inspect fullgraphics extent starting actual98(canonical99). JSON/assets only;no reading-room rebuild.

### August full CP/M90–97 assembly complete, 2026-10-13

- Full CP/M90–97 assembled from exact validated opening15/ending16 manifest pins after endingcommit81b0108. All205 regions retain196 selectedreadings,188 orderedblocks,nine originalimages and196 textreviewranges. Fullsource coverage/readableavailability verified withno deferredpages. Eight nativeprose/listboundaries remain;no cross-native text/physicalrow join required.
- Thirty-six independent groups retain96 physicalrows:45 printedlabels,six numberedprogramwraps and45 unnumberedrows. Sixteen numberedprograms and20 command/console/sessionexamples remain separate. Standalone sourceindex projects42 unnumberedsourceexamples fromall45 actualrows,excluding every numberedprogramrow;three nativeexamplewraps preserved.
- Five ruledtables retain26 datarows104cells/six semanticblanks withglobal UTF-8 row/cell ranges. Both fullRESUME/ERASE images retaingraphicalomissiondots withoutfabricatedcode. All60 native sourceflags preserveoriginal words/errors,format glyphs,sourceclaims andquote/spacing/bitmap ambiguities. Both native metadata andhumanpending statuses unchanged.
- Every originalnativefile copiedbyte-identically. Fullcoverage/canonicalidentity,exactreview/table/listing/sourceexample partitions,independent byte-identical fullrebuild,all21 priorproduction packages,bothtwo raw inventories and16,790 sealedpilot files pass. No new mapping/OCR,pipeline/frontend/browser work orreading-room rebuild duringassembly.
- Package:`build/pdf-restoration/13-1984-08-adaptive/cpm/`;sourceindex:`build/pdf-restoration/13-1984-08-adaptive-cpm-source-index/source-index.json`;audit:`private/pdf-restoration/13-1984-08-adaptive/cpm-assembly-validation.json`. Humanacceptance,fullproofreading,sourceencodedbytes andhistoricalexecution remainunverified.
- Twelve productionarticles complete,zero partial,19 untouched,six pilotselections pending,two headings classified/four remaining;zero humanaccepted. August remains incomplete.
- Next:inspect fullgraphics extent beginningactual98(canonical99) andfollowingFortran title(canonical105) beforeboundedmapping. Then adaptiveOCR/sourcecorrection/export/validation andanyrequiredfullassembly. Six-page/two-article/20outside-map limits andJSON/assets scope remain.

### August graphics98–104 full source extent verified, 2026-10-13

- Allnine wholepage views98–106 actuallyinspected before mapping:98–100 reuse unchanged pinned sourceimages;101–106 arefresh. The graphics article starts98 withphoto/title/김홍진/마지막회 andends104 aftersection4다각형,finalthanks andendornament. Next애플 포트란 title/byline이준구 begins105. Canonicalgraphics page99 remainsunchanged.
- Nextnative17 maps98–103(sixpages),withthreeoutside-map lookups104–106. Ending104 andseparatefull98–104assembly required. Six fresh2829×4000source rasters prepared. Initial hardcoded2830-width assertion failed;failure retained andcorrectrequested4000-max/actualdimensions check passes withoutimagechanges. Mainpieprogram100line10–240 continues101line250–300;other examples remainindependent. Sourcecharts,tablecells,programphysicalwraps andallcodebitmaps mustbepreserved.
- Full extent/rasterpreparation evidence:`private/pdf-restoration/13-1984-08-adaptive/batch-17/{extent-inspection,source-raster-preparation}.json`. No mapping,recognition orproduction export yet. Twelvearticles complete,zero partial,19untouched,sixpilotselections/fourheadings andwholeAugustcloseoutremain. Next:mapcoherent regions,inspectallpanels/edges,repairbeforeadaptiveOCR,then sourcecorrection/export/validation. JSON/assets only;no reading-room rebuild.

### August graphics98–103 raw preparation complete, 2026-10-13

- Native17 maps sixpages98–103 of fullsource-verified98–104;threeoutside-map lookups104–106. Canonicalfirstpage99 unchanged. Ending104 andseparatefullassembly remain. 107regions retain86textdrafts and21originalimages. Nine independentprogram/patch groups use22code regions;onecompanyshipping table preserves its originalbitmap andseparatecellreading. Mainpieprogram100/101 stays onegroup.
- All29originalpanels,20revisedpanels andsixoriginal/sixfinaloverlays actuallyinspected. Thirty-seven originaltextcrops repaired before recognition. Sharedboundaries now preservecompleteprintedprose andcode rows;titlepage labels exclude decorative rules. Final344-boundary diagnostic haszero glyphcrossings;four explicitly reviewed crossings arethe shaded 마지막 회 background. Originalmaps/crops/diagnostic retained;noOCR preceded finalgate.
- 23successfulQ calls and63T calls complete all86selecteddrafts withzero failures,retries,fallbacks,cache reuse orprobes. Q14,583localtokens(11,791prompt/2,792output),localmonetaryweightzero. Preparation,recognition andevaluationdurations remain separate noncausaldiagnostics. Printedprogram errors andtable/codephysicalrows await independent sourcecorrection.
- Source/crop/model/map/requesthashes,allstopoutcomes,rawbundles,full extent andoriginalgeometrypins pass. All22priorproductionpackages,bothtwoCP/Mraw inventories and16,790sealedpilotfiles unchanged. Raw/preflight evidence sealed;no productionexport yet.
- Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-17/raw-ocr-audit.json`. Twelveproductionarticles complete,zero partial,19untouched,sixpilotselectionspending,twoheadingsclassified/fourremaining;zerohumanaccepted. Humanacceptance/fullproofreading,sourceencodedbytes andhistoricalexecution remainunverified. August incomplete.
- Next:correct/export/validate98–103,thenrestore104 andassemblefull98–104 fromimmutablenatives. JSON/assets only;no reading-room rebuild.

### August graphics98–103 production opening complete, 2026-10-13

- Corrected and exported all 86 selected drafts for pages 98–103 of the verified full article, 98–104. The opening retains 107 regions, 81 ordered blocks, 21 original images and 86 text review ranges. Four prose groups preserve five crop boundaries. One further column continuation, 훌륭한 모양의/바퀴가, is indexed across the intervening code and original image while keeping their source order.
- Nine independent numbered programs and patches retain 178 physical rows, 125 printed labels and 53 wraps. The pie program on 100–101 remains one group. Decimal, DATA and closing-parenthesis wraps are source rows, not new statements. The company table retains seven rows, 28 cells and no blank cells, with global UTF-8 indexes.
- Thirty-five source flags preserve incomplete line240+1, positive COS patch, missing X/parentheses, X2/NEXT dots, TC/TO and I/1 candidates, color3 erasure, table discrepancies and historical wording. Original bitmaps remain authoritative; human acceptance, full proofreading, encoded bytes and execution remain unverified.
- No further OCR during correction/export: 23Q/63T calls, zero failures/retries/fallbacks, 14,583 local Q tokens. Export initially stopped at imports because the command omitted the repository src path; the failure and original builder are retained. Correct PYTHONPATH succeeds without source, OCR or builder changes.
- Source/crop/raw hashes, every review/table/listing range, source-order continuation, canonical identity and byte-identical rebuild pass. All 852 sealed raw/preflight files, 22 prior production packages, both CP/M raw inventories and 16,790 pilot files remain unchanged.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-17/graphics/`; source index: `build/pdf-restoration/13-1984-08-adaptive-graphics-source-index-17/source-index.json`; audit: `private/pdf-restoration/13-1984-08-adaptive/batch-17/validation.json`.
- Twelve articles complete, one partial graphics article, 18 untouched bodies, six pilot selections pending, two headings classified/four remaining; zero human accepted. August is incomplete. Next: restore ending104, commit it, then assemble full98–104 from immutable natives17/18. JSON/assets only; no reading-room rebuild.

### August graphics104 production ending complete, 2026-10-13

- Restored all 21 selected drafts on page 104, the verified ending of the graphics article on 98–104. The ending retains 29 regions, 21 ordered blocks, eight original images and 21 text review ranges. Three prose continuations retain their original order around console/code illustrations; the final thanks and end ornament precede Fortran on 105.
- Five independent groups retain 26 physical rows: 19 printed labels, four program wraps and three unnumbered console rows. Bare 3/2 rows remain continuations of lines80/90. Printed line65 lacks FOR;140NEXT, prompt/bracket candidates, historical 갯수/번호 and source claims remain unchanged. Sixteen source flags retain uncertainties; human acceptance, full proofreading, source bytes and execution remain unverified.
- Page104/next105 and all eight original/two revised panels plus original/final overlays inspected. Five crop repairs preceded OCR; all84 final edges have zero ink crossings. Original geometry/crops retained. Seven Q calls and14T calls complete all21 drafts with zero failures/retries/fallbacks/cache/probes. Q2,482 local tokens(2,115prompt/367output); local monetary weight zero, timings separate diagnostics.
- Every crop/raw/model/map hash, text/review/listing range, source-order continuation and canonical identity passes, with an exact byte-identical rebuild. All248 sealed raw/preflight files,23 prior production packages, both CP/M and graphics-opening raw inventories, and16,790 pilot files unchanged.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-18/graphics/`; source index: `build/pdf-restoration/13-1984-08-adaptive-graphics-source-index-18/source-index.json`; audit: `private/pdf-restoration/13-1984-08-adaptive/batch-18/validation.json`.
- Twelve articles complete, one partial graphics article with all98–104 native coverage,18 untouched bodies,six pilot selections pending,two headings classified/four remaining;zero human accepted. August incomplete. Next: commit ending, then separately assemble full98–104 from immutable natives17/18. Fortran begins105 and needs complete extent inspection before mapping. JSON/assets only;no reading-room rebuild.

### August full graphics98–104 assembly complete, 2026-10-13

- Full graphics98–104 assembled from exact validated native17/18 pins after endingcommitfa3f056. The article retains136 regions,107 selected regional readings,102 ordered blocks,29 original images and107 text review ranges. Full readable coverage passes with no deferred/missing pages. Canonical page99 remains unchanged; actual title is98.
- Fourteen independent groups retain204 physical rows,144 printed labels,57 wraps andthree unnumbered console rows. Thirteen numbered programs/patches stay independent;the pie program100/101 remains one native group. Listing bytes equal exact native concatenation;all physical/logical partitions pass. Four native prose groups/five crop boundaries andfour prose frames around illustrations preserve source order.
- The shipping table retainsseven rows,28 cells andzero blanks with global UTF-8 indexes. All51 original source flags andevery native metadata/review status remain unchanged,including malformedline65 withoutFOR,incomplete240+1,prompt/glyph candidates,signs andsource claims. Human acceptance,full proofreading,encoded bytes andexecution remain unverified.
- Both original native packages copied byte-identically. Full coverage/canonical identity,every review/listing/table/prose range,independent exact rebuild,24 prior production packages,both graphics raw inventories and16,790 pilot files pass. No new mapping/OCR,pipeline/frontend/browser orreading-room work duringassembly.
- Package: `build/pdf-restoration/13-1984-08-adaptive/graphics/`; source index: `build/pdf-restoration/13-1984-08-adaptive-graphics-source-index/source-index.json`; audit: `private/pdf-restoration/13-1984-08-adaptive/graphics-assembly-validation.json`.
- Thirteen production articles complete,zero partial,18 untouched bodies,six pilot selections pending,two headings classified/four remaining;zero human accepted. August remains incomplete. Next: Apple Fortran begins105. Inspect complete source extent and following title before bounded mapping;reuse unchanged105/106 evidence. JSON/assets only;no reading-room rebuild.

### August Fortran105–110 raw preparation complete, 2026-10-13

- Full 애플 포트란 extent105–112 verified from ten whole-page views105–114 before mapping. Unchanged105/106 images reused;107–114 fresh. Following 자유 낙하운동/탁연상 begins113. Canonical Fortran title/byline/parent/page105 unchanged. Native19 maps105–110, with four outside-map lookups111–114; ending111–112 and full assembly remain.
- 178 regions preserve135 text drafts and43 original source images. Forty-seven code regions retain independent Fortran examples, file lists, prompts and compiler/output columns; compiler ordinals are not BASIC line labels. Two original tables have separate cell drafts. Prose/headings/captions start with Tesseract; code, diagram labels and structured content start with Qwen.
- All47 original/11 revised panels, six original/six final overlays and seven detailed boundary panels inspected. Twelve regions repaired before OCR, including one diagram image; complete paragraph endings, copyright rows and editor cursor retained. Final540-boundary diagnostic has zero glyph crossings and55 individually reviewed nontext crossings in diagram outlines, screen frames and one incidental scan dot. Original geometry/crops and diagnostic retained. An optional SciPy diagnostic import failure is preserved; existing NumPy/Pillow inspection completed the review without installing dependencies.
- 63 Q attempts yield61 successful drafts; two512-token length failures on FORMAT labels108 and END/cursor109 use recorded same-crop Tesseract fallbacks. All74 T calls complete, yielding135 selected drafts. No retries, probes or cache reuse. Failed responses and pre-fallback route plan retained. Q17,827 local tokens include15,042 prompt/2,785 output and all1,844 failed-attempt tokens; local monetary weight zero. Worker127.78 seconds is a separate noncausal timing diagnostic.
- Source/crop/model/map/request hashes, all stop outcomes, exact crop pixels and evidence bundles pass. Twenty-five prior production packages, all prior CP/M/graphics raw inventories and16,790 pilot files unchanged. Raw evidence sealed. No production export; physical rows, table cells and source correction remain pending.
- Audit: `private/pdf-restoration/13-1984-08-adaptive/batch-19/raw-ocr-audit.json`; crop gate: `preflight-acceptance.json` in the same directory. Thirteen production articles complete, zero partial,18 untouched bodies,six pilot selections pending,two headings classified/four remaining;zero human accepted. August incomplete.
- Next: correct/export/validate105–110, preserving literal statementlabel10, continuationA, compiler ordinals, printed syntax and historical claims. Then restore111–112 and assemble full105–112 from immutable natives. Human acceptance, full proofreading, source encoded bytes and historical execution remain unverified. JSON/assets only; no reading-room rebuild.

### August Fortran105–110 production opening complete, 2026-10-13

- Corrected and exported all 135 selected drafts for pages105–110 of the verified full article105–112. The opening retains178 regions,135 ordered blocks,43 original images and135 text review ranges. Seventeen instruction frames around printed screens retain separate objects in source order; no flattened prose or executable concatenation is inferred.
- Forty-seven regional code/screen groups retain121 physical rows and120 source-line examples. The complete program keeps Fortran statementlabel10 and continuationA in distinct source columns and physical rows. Compiler ordinals0–9 and offsets0/0/0/10/20/41/82/82/82/89 are independent of those labels. Ten compiler rows retain50 field cells and18 blank label/continuation fields; four symbol rows retain12 cells andone blank reference field. No BASIC numbering is invented.
- Both original tables retainnine rows,28 data cells andzero blank data cells. The arithmetic table's first printed header remains blank; the cursor guide has no invented header. Global UTF-8 row/cell indexes pass. Forty-three source figure associations andthree diagrams preserve label readings;11 arrow relations have exact source-text ranges.
- Fifty-six source flags retain STSTEM.APPLE,원시프로램,diagram commas/dots,cutoff prompts,unbalanced FORMAT quotes,partial example2 versuscomplete2.,damaged compiler PR)GRAM candidate,printed file-size/compile claims andLONG output label. Cursor/arrow/spacing glyphs are source-linked reading aids,not encoded-byte claims. Original bitmaps remain authoritative;human acceptance,full proofreading,source bytes andhistorical execution remain unverified.
- No additional OCR during correction/export:63 Q attempts/61 successes and74 T calls,including two recorded length-only fallbacks. All17,827 local Q tokens include failed attempts;local monetary weight zero. A correction flag initially targeted the preceding region; the failure/original script are retained and the flag now points to its actual source region. Initial diagram indexing used a single-line excerpt for a two-line label; failure/metadata/script retained,and the exact source newline now validates. Source OCR/transcription/images/export were unchanged by that index repair.
- Source/crop/raw/model pins,all review/listing/table/compiler/diagram ranges,canonical identity andan independent byte-identical rebuild pass. All1,433 sealed raw/preflight files,25 prior production packages,all prior CP/M/graphics raw inventories and16,790 pilot files remain unchanged.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-19/fortran/`; source index: `build/pdf-restoration/13-1984-08-adaptive-fortran-source-index-19/source-index.json`; audit: `private/pdf-restoration/13-1984-08-adaptive/batch-19/validation.json`.
- Thirteen production articles complete,one partial Fortran opening,17 untouched bodies,six pilot selections pending,two headings classified/four remaining;zero human accepted. August incomplete. Next: commit opening,restore111–112 using the pinned verified extent,then assemble full105–112 from immutable natives. Following article is 자유 낙하운동 on113. JSON/assets only;no reading-room rebuild.

### August Fortran111–112 raw preparation complete, 2026-10-13

- Reused the pinned full105–112 extent and actually reinspected111/112/following113. One article/two mapped pages/one outside-map lookup. Ending20 maps47 regions:36 text drafts and11 original images,including seven independent screen fragments andthree keyword/I/O/slot tables. Comment-rule fragments are ordered left-column then right-column before the keyword sidebar.
- All13 original/four revised enlarged panels,two original/two final overlays andone detailed boundary strip inspected. Five region crops repaired before OCR. Final144-edge diagnostic has zero glyph crossings;one inspected crossing is a short vertical table-rule extension. Original maps/crops/revisions and the pre-write import failure are retained.
- Eleven Q and25T calls completed36 drafts with zero inference failures,retries,cache hits or probes. Local Q6,910 tokens include6,036 prompt/874output;local monetary weight zero. Worker45.33 seconds remains a separate timing diagnostic. The Q I/O draft shifts row associations;one bounded same-crop T fallback remains required before correction,with original Q evidence/cost retained. No fallback has yet executed.
- Source/crop/map/request/runtime/model and stop-outcome audit passes. All26 prior production packages,prior CP/M/graphics/Fortran-opening raw inventories and16,790 pilot files remain unchanged. Native20 raw/preflight evidence sealed. No ending production export;source-corrected physical rows/table cells and export validation remain pending.
- Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-20/raw-ocr-audit.json`;gate:`preflight-acceptance.json` in the same directory. Thirteen production articles complete,one partial Fortran opening,17 untouched bodies,six pilot selections pending,two headings classified/four remaining;zero human accepted. August incomplete.
- Next: one bounded I/O-table fallback,correct all36 selected drafts,export/validate111–112 andcommit;then separately assemble full105–112 from immutable natives19/20. Following article is 자유 낙하운동113. Human acceptance,full proofreading,source bytes andhistorical execution remain unverified. JSON/assets only;no reading-room rebuild.

### August Fortran111–112 production ending complete, 2026-10-13

- Corrected all36 selected drafts and exported the verified ending111–112:47 regions,35 ordered blocks,11 original images and36 text review ranges. The comment rule joins from the left column to the top of the right column;seven instruction frames around independent screenshots retain source order.
- Seven console fragments retain ten unnumbered physical rows. Column-rule prose keeps eight ink rows/four semantic rules without inventing BASIC numbering. Three keyword/I/O/slot tables preserve35 data rows,118 cells andseven blanks;three independent keyword columns andeight slot groups retain five merged-slot continuation blanks andthe final blank purpose cell.
- Twenty-five source flags retain literal FORTMATTER,FOR-/MAT,TEST.CODE,9..12,IN#4,heading인트리식/body인트린식,슬로트 anduncertain header드/트,ditto/cursor glyph candidates andhistorical claims. Original bitmaps remain authoritative;human acceptance/full proofreading,source bytes andhistorical execution unverified.
- One bounded same-crop T fallback followed Q's shifted I/O associations. T also misses some rows;the selected T draft was corrected directly against the ten source rows,with no further inference ordual correction. All11Q/26T calls are counted;6,910 local Q tokens include the unselected Q attempt. Local monetary weight zero;45.33-second worker and0.37-second fallback are separate noncausal timing diagnostics. Original387-file andselected240-file raw inventories remain unchanged.
- Source/crop/model/map/raw hashes,all review/row/cell/column-rule ranges,blank-slot hierarchy,canonical identity andbyte-identical rebuild pass. All26 prior production packages,prior raw inventories and16,790 pilot files unchanged. Initial validation expected six I/O ditto cells rather than the five actually printed;original validator/failure retained,andonly its expected count changed. Source transcriptions/OCR/assets/export unchanged.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-20/fortran/`;source index:`build/pdf-restoration/13-1984-08-adaptive-fortran-source-index-20/source-index.json`;audit:`private/pdf-restoration/13-1984-08-adaptive/batch-20/validation.json`.
- Thirteen production articles complete,one partial Fortran withall105–112 native coverage,17 untouched bodies,six pilot selections pending,two headings classified/four remaining;zero human accepted. August incomplete. Next: commit ending,then separately assemble full105–112 from immutable natives19/20. Following 자유 낙하운동113 needs full extent inspection before mapping. JSON/assets only;no reading-room rebuild.

### August full Fortran105–112 assembly complete, 2026-10-13

- Full 애플 포트란105–112 assembled from exact validated natives19/20 after endingcommita6159b8. All225 regions,171 selected readings,170 ordered blocks,54 original images and171 text review ranges preserved. Full readable coverage has no missing/deferred pages. Canonical title/byline/parent/page105 unchanged;both native packages/original metadata copied byte-identically.
- Fifty-four regional groups retain131 physical rows and130 source-line examples. Only the complete FORMAT's two physical rows form one source example;independent screens/partial examples remain separate. Fortran statement10/continuationA andcompiler ordinals0–9/address offsets are distinct source columns. Ten compiler rows retain50 fields/18 blank label-continuation fields;four symbol rows retain12 fields/one blank numeric field.
- Five source tables retain44 rows,146 data cells,seven blank data cells andone printed blank header. Three independent keyword columns,eight slot groups/five blank merged-slot continuations andfour column rules/eight ink rows remain explicit. Twenty-four instruction frames around independent source objects andthe native comment-rule column join preserve source order. Fifty-three figure associations/three diagrams/11 arrows retain exact label ranges;the end ornament stays an original image.
- All81 source flags remain literal source-linked candidates,including STSTEM.APPLE,PR)GRAM,unbalanced FORMAT quotes,FORTMATTER,TEST.CODE,cutoff prompts,Intrinsic spelling differences andditto/header/cursor uncertainty. Human acceptance/full proofreading,original codepoints/encoded bytes andhistorical compilation/execution remain unverified.
- Full canonical/source coverage,171 review ranges,131-row/130-example partition,515 projected exact ranges,table headers/cells/blanks,compiler/Fortran fields anddiagram ranges pass. Independent full rebuild is byte-identical. All27 prior production packages,prior/selected raw inventories and16,790 pilot files unchanged. No new mapping/OCR,pipeline/frontend/browser orreading-room work duringassembly.
- Package:`build/pdf-restoration/13-1984-08-adaptive/fortran/`;source index:`build/pdf-restoration/13-1984-08-adaptive-fortran-source-index/source-index.json`;audit:`private/pdf-restoration/13-1984-08-adaptive/fortran-assembly-validation.json`.
- Fourteen production articles complete,zero partial,17 untouched bodies,six pilot selections pending,two headings classified/four remaining;zero human accepted. August remains incomplete. Next: inspect complete 자유 낙하운동 extentstarting113 andfollowing titlebefore bounded mapping,reusing unchanged113/114 source evidence. JSON/assets only;no reading-room rebuild.

### August freefall113–115 extent verified, 2026-10-13

- After full Fortran assemblycommitc980574,actually reinspected unchanged113/114 andfresh115/116 scans. Canonical 자유 낙하운동/탁연상/parent0009/page113 unchanged. Full source extent is113–115;following Z80 기계어 강좌/이세형 title is116. Four source views pinned;one article/three planned mapped pages/one outside-map lookup.
- Source113 retains physics prose/equations andscreen illustration;114 hasflow/window diagrams andusage/program explanation;115 hasvariable explanation/endornament andone complete two-column BASIC listing. Left-column3200 continuesright-column3210;final9910 precedesnexttitle116. Printed labels/wraps must be counted independently before correction/export;no execution orbyte verification inferred.
- No mapping/OCR orproduction export for native21 yet. Next: prepare4000rasters,coherent Tprose/Qformula-diagram-listing regions andsource crop review beforeOCR;then source correction/export/validation/commit. Fourteen complete production articles,17 untouched bodies,six pilot selections/four heading classifications andwholeAugust JSON/assets closeout remain. Humanacceptance/fullproofreading pending;no reading-room rebuild.

### August freefall113–115 raw preparation complete, 2026-10-13

- Native21 maps the verified full 자유 낙하운동/탁연상 article113–115, preserving canonical identity. Four pinned extent views and following Z80title116 retain one article/three mapped pages/one outside-map lookup. The map has82 regions,76 text drafts andsix original images;16 code regions belong toone complete BASICprogram across115's columns. Physical rows/printed labels/wraps remain pending independent source correction counts.
- All21 original/12 revised panels,three original/three final overlays,five final boundary panels andsix detailed source crops inspected. Twenty-eight distinct crops repaired before OCR. Final304-edge diagnostic haszero glyph crossings and18 source-reviewed nontext crossings inauthor underline,screen rules anddiagram connectors/brackets. Original map/crops/diagnostic retained. Snapshot inventory initially used relative paths against absolute ROOT;copied originals unchanged,andthe failure/recovery record retained before recognition.
- All29Q/47T calls complete76 drafts withzero failures,retries,cache hits orprobes. Q12,850 local tokens include10,279 prompt/2,571 output;local monetary weight zero. Worker103.68 seconds is a separate noncausal timing diagnostic. Q's gravity-diagram draft omits several source labels;one bounded same-crop Tfallback remains required before correction. No fallback has executed andno selected draft has yet been corrected.
- Source/crop/model/map/request/runtime pins,all stop outcomes andexact crop pixels pass. All28 prior production packages,prior CP/M/graphics/Fortran raw inventories,selected20 inventory and16,790 pilot files unchanged. Native21's757 raw/preflight files sealed. The preserved extent description accidentally says finalPOKE54,17;actual printed9910 isPOKE34,17. Original evidence stays immutable;source-review metadata must document the preparation-description correction.
- Audit:`private/pdf-restoration/13-1984-08-adaptive/batch-21/raw-ocr-audit.json`;crop gate:`preflight-acceptance.json`;pending fallback/source-review notes:`draft-inspection.json` in the same directory. No production export. Fourteen production articles complete,zero partial,17 untouched bodies,six pilot selections pending,two headings classified/four remaining;zero human accepted. August incomplete.
- Next:one bounded diagram-label fallback,correct all76 selected drafts,independently count one listing's physical rows/labels/wraps,export/validate full113–115 JSON/assets andcommit. Preserve formulas,diagram labels,source mistakes/glyph candidates andthe two physical prose joins. Human acceptance/full proofreading,source bytes andhistorical execution remain unverified. No reading-room rebuild.

### August freefall113–115 production complete, 2026-10-13

- Restored the complete verified 자유 낙하운동/탁연상 article113–115:82 regions,76 selected regional readings,74 ordered blocks,six original images and76 text-review ranges. Canonical title/byline/parent/page113 unchanged. Full readable coverage hasno missing/deferred pages andrequiresno assembly. Two no-space prose joins preserve조심해서 and표시한다.
- One complete BASICprogram across16 code regions retains117 physical rows,56 printed labels and61 wraps. Left48/right69 rows preserve3200→3210 source-column continuation. Physical3/2inPOKE230,32,A/$,K/N,PRIN/T,930'sfaintEND,8700'sbare1,9530'squotedV,DATA45split4/5 andcoordinate130split1/30 allretainexactphysical/logical associations. Twenty sourceDATA value candidates haveexplicitprovenance;no encoded-byte orexecutioncertification.
- Five figure associations andthree diagrams preservephysics/screen/formula labels,16 flow-label rows,three connectorarrows,one gravity arrow andwindow tickgroups/dividers. Three physics equations andthree formula/program variablepairs haveexact UTF-8 ranges. Diagramlabels,coordinate ticks,ellipsis andditto glyphs remain separatefromexecutableBASIC numbering;originalbitmaps authoritative.
- Fifty-one source flags retain historicalspellings/claims,sourceglyph/punctuation candidates,single/doublequote uncertainty,printed4.7versus4.9 andprose9 30versuslisting9530. Actualfinal9910 isPOKE34,17;the sealed preparationextent's54description error isdocumented without rewriting evidence. The private previous-newton region name islikewiseonlyan erroneous preparationlabel;sourceactuallysays샤를의법칙. Human acceptance/full proofreading,source bytes andhistoricalexecution remainunverified.
- One bounded same-crop Tfallback followedQ'somitted gravity labels. Talsomisseslabels;selectedTdraft corrected directlyfromsource,withnofurtherinference ordual correction. All29Q/48T calls counted;12,850localQ tokens includetheunselecteddiagramattempt. Local monetary weight zero;103.68-second worker and0.091-second fallback are separate noncausal timing diagnostics. Original757-file andselected491-file raw inventories unchanged.
- Canonical/fullcoverage,everyreview/listing/diagram/formula/prose range,sourcecrop/raw/model pins andindependentbyte-identical rebuild pass. All28 priorproductionpackages,prior CP/M/graphics/Fortran raw inventories,selected20inventory and16,790pilotfiles unchanged. No furtherOCR duringcorrection/export;no pipeline/frontend/browser work.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-21/freefall/`;sourceindex:`build/pdf-restoration/13-1984-08-adaptive-freefall-source-index-21/source-index.json`;audit:`private/pdf-restoration/13-1984-08-adaptive/batch-21/validation.json`.
- Fifteen productionarticles complete,zero partial,16 untouched bodies,six pilotselections pending,twoheadings classified/fourremaining;zerohumanaccepted. WholeAugust incomplete. Next:commitfreefall,theninspect completeZ80 기계어 강좌 extentbeginning116 andfollowingactualtitlebeforemapping,reusingpinned116view. Canonicalnexttitle128islookupaide,not extentproof. JSON/assets only;no reading-room rebuild.

### August Z80 lesson116–127 extent verified, 2026-10-13

- After completefreefallcommit4c83500,actually reinspectedunchanged116titleandfresh117–128whole-page scans. Full Z80 기계어 강좌/이세형 source extentis116–127;followingactual도형정의표의정복/김선호titleis128. All13views pinned;canonical 기계어 강좌 identity/byline/parent/page116unchanged. Native22planned116–121:onearticle/sixmappedpages/sevenoutside-maplookups122–128. Native23ending122–127andfullassemblyremain.
- Completeextentretainsstack/jump/call/returnprose,originalphotos/diagrams,condition/opcode tables andindependentSPC-1000examples/hex dumps. LIST3continues120→121;SPC-1000sortingLIST4spans125columns. CP/MsupportLIST5continues126left→righttop;separateCP/MversionsLIST1/2/3follow,withLIST3continuing126→127beforefullCP/MLIST4on127. Addresses/opcodes/labels/apostrophemarkers/dumpsarenotBASICnumbering;sourcecolumns/blankfields andliteral source mistakes require independent correction.
- Opening/endingnativeboundary121→122 splits프로/그램 withinoneword. Otherphysicalprose continuations117→118,118→119,119→120,120→121 and122→123 areexplicitlyrecorded. Printerphoto118/119 remains twooriginalpageassets;no image stitching ornew contentinferred. Final127DATA/DEFS declaration precedes128title,confirmingthefullendingbeforemapping.
- Extent:`private/pdf-restoration/13-1984-08-adaptive/batch-22/extent-inspection.json`. No native22mapping/OCR/exportyet. Next:4000rasters,coherentTprose/Qassembly-and-structuredregions,fullcrop review,thenOCR/sourcecorrection/export/validation. Fifteenproductionarticlescomplete,16untouchedbodies,sixpilot selections/fourheadingclassificationsandwholeAugustJSON/assetscloseoutremain. Humanacceptance/fullproofreading/sourcebytes/executionpending;no reading-room rebuild.

### August Z80 opening116–121 raw preparation complete, 2026-10-13

- Pages 116–121 now have 120 mapped regions: 108 text drafts, 12 source
  images, 34 code regions and one condition table. The full article extent remains
  116–127. Three SPC-1000 programs and their separate byte dumps retain assembly
  address/opcode/label/operand fields; physical row and cell counts await correction.
- Reviewed all 32 original panels, 22 revised panels, 12 images and six original
  and final overlays. Repaired 45 distinct crops before OCR; one leading glyph
  needed a second extension. All 432 final edges have zero glyph crossings.
  The remaining 24 ink crossings are inspected backgrounds or figure borders.
  Original and intermediate geometry, crops and diagnostics remain preserved.
- Two bounded Tesseract probes guided routing. The condition table retained all
  eight row associations and was reused. The assembly probe corrupted identifiers,
  so its initial route stayed Qwen. Qwen then shifted address/instruction pairs in
  p119r19; one bounded fallback reused the existing Tesseract probe without another
  inference. Correct only the selected draft once against the source.
- Actual calls: 38 Qwen and 71 Tesseract, including both probes and the unselected
  Qwen draft. Selected regions: 37 Qwen and 71 Tesseract. The worker made 69 new
  Tesseract calls; there were no length failures, retries or cache hits. Qwen used
  17,410 local tokens (15,178 prompt / 2,232 output). Local monetary weight is zero.
  Worker duration 111.591s, probe duration 0.319s and selection verification/copy
  duration are separate diagnostics; they establish no causal paid-cost winner.
- Source, crop, map, raw bundle, runtime/model and stop checks pass. All 29 prior
  production packages, native15–21 original raw inventories, native20–21 selected
  raw inventories and 16,790 pilot files remain unchanged. Original and selected
  native22 raw evidence are separately sealed. No production export exists yet.
- Evidence: `private/pdf-restoration/13-1984-08-adaptive/batch-22/raw-ocr-audit.json`,
  `selected-raw-preservation.json` and `raw-draft-inspection.json`. Next: source-correct
  the 108 selected drafts, count every assembly row and table cell, export/validate
  the opening, then restore 122–127 and assemble the article. Preserve the explicit
  121프로/122그램 word join. August remains 15 complete, zero partial, 16 untouched
  bodies, six pilot selections pending and four headings unclassified. Human
  acceptance, full proofreading, source bytes and execution remain unverified.
  Whole-issue JSON/assets closeout remains required; no reading-room rebuild.


### August Z80 opening116–121 production restored, 2026-10-13

- Restored opening116–121 of the verified full Z80 기계어 강좌/이세형 article116–127. All120 regions retain108 corrected selected drafts,98 ordered blocks,12 original images and108 source-review ranges. Canonical title/byline/parent/page116 unchanged. Coverage is explicitly partial:122–127 and separate full assembly remain.
- Thirty-four code regions retain117 unnumbered physical rows in27 source groups. Three SPC-1000 assembly examples preserve63 aligned rows,three separate byte dumps preserve19 rows,andthe jump-address example preserves6 rows. Structured indexes retain516 fields/67 blanks;ORG has separate blank address/opcode/label fields. Addresses,opcodes andapostrophe markers are not BASIC labels;zero numbered logical rows. LIST3 continues120→121 withgroup membership independentfromphysical export order.
- Condition table retainsone header/eight data rows,16 data cells/two header cells andzero blanks. Nine figure associations,two diagrams,11 flow nodes/12 flow arrows,six stack arrows andthree pseudocode rows have exact source ranges. Original printer photograph remains two page assets. Eight prose groups preserve10 physical boundaries;118프/119로그램 joins normally. Earlier assistant duplicate로 inference was rejected after direct native-crop inspection. Deferred121프로/122그램 join remains required at full assembly.
- Thirty-one source flags retain historical spellings,printed range/monitor claims,9021 opcode20DF apostrophe,uncertain LIST2operand-endingT glyphs and901DregisterB/E. No encoded-byte,assembly/execution orhuman-acceptance certification. Printed English ba-/ck andASC-/GET prose hyphens remain;source bitmaps authoritative.
- Source validation found17 incorrect row offsets in the initial private export helper because LIST3 crosses intervening inline examples. Initial export/rebuild/helper/corrections are preserved unchanged. The private native22 helper now walks code blocks in source order while retaining complete group membership. Fresh export/rebuild andall117 exact row ranges pass. Numeric usage-accumulator setup failure andsource-reading retraction are recorded separately. No pipeline/frontend/browser change ornew OCR duringcorrection/export.
- All38 original Qwen calls and71 Tesseract calls,includingtwo probes andthe unselected Qwen row-shift draft,are counted once. Selected37Q/71T reuseboth unchanged probes;bounded fallback madezero new inference calls. Qwen17,410local tokens include15,178prompt/2,232output. Local monetary weight zero;111.591s worker,0.319s probes and0.089s selection are separate noncausal diagnostics. T recognition total14.425s includesboth probes;probe time is not added twice.
- Source/crop/raw/runtime/model pins,all UTF-8 review/table/diagram/field ranges,canonical partial coverage andindependent byte-identical rebuild pass. Original1,085-file andselected691-file raw seals,29 priorproductionpackages,all priornative15–21 raw/selected inventories and16,790 pilot files unchanged. Human acceptance/full proofreading,sourcebytes andhistorical execution pending.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-22/z80/`;source index:`build/pdf-restoration/13-1984-08-adaptive-z80-source-index-22/source-index.json`;audit:`private/pdf-restoration/13-1984-08-adaptive/batch-22/validation.json`.
- August now has15 complete articles,one partial Z80,15 untouched bodies,six pilot selections pending,two headings classified/four unclassified andzero human accepted. Next:native23 ending122–127 from the pinned full extent,then full116–127 assembly. Whole-issue JSON/assets closeout remains required;no reading-room rebuild.

### August Z80 ending122–127 raw preparation complete, 2026-10-13

- Prepared the Z80 ending, pages 122–127 of the verified full article 116–127:
  188 regions, 175 raw text drafts, 13 original images, 107 code regions and three
  opcode tables across 29 text regions. All six ending views, the page 121 boundary
  and the following title on 128 were reinspected before mapping. Scope: one
  article, six mapped pages and two outside-map lookups.
- Inspected all 49 original panels, 13 images and six overlays. Changed 34 distinct
  regions before OCR. RETcc remarks became separate region p124r24; skewed source
  rows in p127r07/08 became one coherent 11-row crop. Four geometry revisions remain
  preserved. Several tiny edges needed follow-up. The final 700-edge diagnostic
  has zero source-reviewed glyph crossings and 217 inspected nontext crossings in
  backgrounds, rules, frames, connectors or scan artifacts. Final table checks
  include 44 distinct native edge strips across six panels. Original inventories
  and supplemental diagnostic/helper pins remain unchanged.
- Two audit setup recoveries are recorded. Inventory verification initially assumed
  a list instead of the actual path/hash mapping. The first successful audit then
  sealed its unfinished stdout log, whose hash changed after printing. The initial
  audit, seal and terminal log remain preserved; the final seal excludes audit
  stdout logs and passes fresh verification. Neither recovery changed source,
  crops or OCR output, and neither repeated inference.
- Two bounded Tesseract probes corrupted opcode flags/conditions and assembly
  identifiers, so both retained the Qwen route. Actual calls: 139 Qwen and 40
  Tesseract, including both unselected probes. Selected drafts: 137 Qwen and 38
  Tesseract. Two capped Qwen failures received bounded worker fallbacks; zero
  retries or cache hits. The CALLcc row repeated escaped newlines, and the dump
  ending repeated zero bytes. Both failed responses remain preserved.
- Qwen used 51,574 local tokens: 40,615 prompt and 10,959 output, including the two
  failures. Local monetary weight is zero. Worker duration 368.817s and probe
  duration 0.472s are separate, noncausal diagnostics. Paid uncached/cached input
  retains the 10:1 ratio; output rate remains unknown.
- Draft inspection found Qwen attaches LP1 to 9528 instead of printed 952B in
  p125r10. One bounded same-crop Tesseract fallback is required before selected
  correction and has not executed. Other values, duplicated flags, column order
  and blank byte-continuation fields need correction. The merged page 127 opening
  retains 11 visible instruction rows; final physical row and cell counts await
  independent source review. No draft is corrected and no ending export exists.
- Source/crop/map/request/runtime/model hashes, raw bundle pixels, stop outcomes,
  probes and preserved geometry pass. All 30 prior production packages, native
  15–22 original/selected raw inventories and 16,790 pilot files remain unchanged.
  The raw/preflight seal retains 1,975 files. Audit:
  `private/pdf-restoration/13-1984-08-adaptive/batch-23/raw-ocr-audit.json`.
  Pending selection: `raw-draft-inspection.json` in the same directory.
- August remains 15 complete articles, one partial Z80, 15 untouched bodies, six
  pilot selections pending, two headings classified/four unclassified and zero
  human accepted. Next: bounded fallback, source correction, ending export and
  validation, then commit and assemble full 116–127. Preserve the 121프로/122그램
  and 122위/123한 joins, uncertain opcode/subscript glyphs, printed errors and
  physical dump interruptions. Full proofreading, source bytes/execution and
  whole-issue JSON/assets closeout remain pending. No reading-room rebuild.


## 2026-10-13 — August Z80 ending122–127 production restored

- Restored the ending122–127 of Z80 기계어 강좌/이세형, canonical article0018
  beginning116. All188 regions retain175 once-corrected selected drafts,168 ordered
  blocks,13 original images and175 source-review ranges. Twelve incremental source
  correction parts preserve progress separately from immutable OCR. Full116–127
  assembly with opening22 remains required; the native ending is explicitly partial.
- The bounded same-crop Tesseract fallback for p125r10 preserves LP1 at printed952B,
  correcting the original Q draft's9528 association. Actual139Q/41T include two
  unselected T probes, two capped Q failures with worker fallbacks and this one new
  association fallback. Selected136Q/39T corrected once. No Q retry or dual correction.
  All51,574 local Q tokens include40,615 prompt/10,959 output and both failures.
  Local monetary weight zero; paid input retains1:0.1 uncached/cached ratio, output
  rate unknown. Worker368.817s, probes0.472s and selection0.220s are separate
  noncausal diagnostics. T recognition total8.320s includes probes/fallback once.
- 107 code regions retain405 unnumbered physical rows in17 source groups:
  345 aligned assembly rows,33 independent16-byte dump rows,21 displayed-output
  rows,two inline instructions andfour monitor commands. Structured indexes retain
  2,286 fields/432 blanks. Blank-address ORG, EQU, DEFM byte continuations andfour
  physically wrapped string fragments remain explicit. No BASIC logical numbering.
  Dumps remain at their original interruptions, independently of instruction bytes.
- Three opcode tables retain21 logical instruction rows/273 main cells,20 key
  rows/40 key cells,54 header cells and18 blank main remarks cells. Three unprinted
  CALLcc second timing fields remain absent. JR NZ operation/timing continuation
  p123r37 andRETcc remarks p124r24 remain associated with their owning rows.
  Literal POPqq opcode bullet,JP(HL) P←HL,CALLnn T-state7 andCALLcc trailing
  comma/no nn remain source candidates without instruction-semantic repair.
- Eleven figure associations andone sorting diagram retain15 boxed/terminal
  nodes,one JMP junction and18 directed connections. Physical arrowhead count is
  not certified. The diagram's B←5 andA↔H(HL), repeated sorted7/no8, prose
  figure4/caption5 andfaint code/dump glyphs remain literal or explicitly uncertain.
  Seventy-two flags retain source errors, string terminator candidates andprinted
  hyphens. Two prose joins retainfive boundaries, including122위/123한; two table
  companion joins retaintwo more. Deferred121프로/122그램 awaits fullassembly.
- The private validator initially used older preflight crop paths for revised
  regions. Failed validator anddiagnostic are preserved at export-validation-
  recovery-01. The corrected check uses sealed final selected crops/current map;
  all188 exported crop hashes andsource pixels match. No source/export mutation,
  inference repetition orpipeline change was needed for this recovery.
- Exact listing/field/table/header/diagram/review UTF-8 ranges,source coverage,
  canonical identity andindependent byte-identical rebuild pass. Original1,975-file
  andselected1,324-file raw seals,all30 prior production packages,priornative15–22
  raw inventories and16,790 pilot files remain unchanged. Human acceptance/full
  proofreading,source encoded bytes andhistorical execution remain unverified.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-23/z80/`; source index:
  `build/pdf-restoration/13-1984-08-adaptive-z80-source-index-23/source-index.json`;
  audit: `private/pdf-restoration/13-1984-08-adaptive/batch-23/validation.json`.
  August remains15 complete,one partial Z80,15 untouched bodies,six pilot
  selections pending,two classified/four unclassified headings andzero human
  accepted. Next: separate full116–127 assembly,then next source title128 after
  extent inspection. Whole-issue JSON/assets closeout remains; no reading-room rebuild.


## 2026-10-13 — Full August Z80 article116–127 assembled

- Assembled the exact validated opening22 andending23 after ending commit e83d753.
  Full116–127 coverage is readable under the JSON/assets scope:308 regions,283
  selected readings,265 ordered blocks,25 original images and283 review ranges.
  Canonical 기계어 강좌/이세형/parent0009/page116 remains unchanged.
- The single cross-native121프로/122그램 join uses an empty separator. Its exact
  interruptions remain: original flowchart,source-associated diagram labels,caption
  and122 runningheading. A private pinned adapter validates the two native package/
  source-index pins,diagram ownership andliteral same-article runningheading before
  accepting these interruption types. Wrong order andan unrelated heading are
  rejected. Shared pipeline files remain unchanged.
- All522 unnumbered physical code/output/monitor rows and44 source groups remain
  in native listing-byte order; no BASIC logical numbers orcross-native code merge
  are invented. Source indexes preserve2,802 structured fields/499 blanks.
  Four tables retain29 main rows/289 cells,20 key rows/40 key cells,56 header
  cells and18 blank main cells. Three unprinted CALLcc timing values remain absent.
  JR NZ andRETcc companion cells,physical dump interruptions andwrapped string
  fragments retain exact native/global ranges.
- Twenty figure associations andthree diagrams preserve original source assets
  andconnections. All103 native flags remain unchanged. Twelve native joins
  retain17 boundaries,includingtwo table companion joins;one cross-native boundary
  is added.8,312 exact source ranges project into combined downloads while retaining
  native coordinates. Human acceptance/full proofreading,encoded bytes andexecution
  remain unverified.
- Private validation initially treated the opening diagram's integer node count
  as the ending's node-object list. The failed helper anddiagnostic are preserved
  in z80-assembly-validation-recovery-01;schema-aware iteration passes without
  changing source/native/assembled bytes orrepeating OCR.
- Exact source coverage,review/table/header/key/diagram/field ranges andindependent
  byte-identical rebuild pass. Both native package trees/all original metadata,
  all31 prior production packages,priorraw/selected seals and16,790 pilot files
  remain unchanged. No new mapping,OCR,pipeline,frontend/browser orreader work.
- Export:`build/pdf-restoration/13-1984-08-adaptive/z80/`;source index:
  `build/pdf-restoration/13-1984-08-adaptive-z80-source-index/source-index.json`;
  audit:`private/pdf-restoration/13-1984-08-adaptive/z80-assembly-validation.json`.
  August now has16 complete articles,zero partial,15 untouched bodies,six pilot
  selections pending,two classified/four unclassified headings andzero human
  accepted. Next:source-verify fullactualextent of도형정의표의 정복/김선호
  beginning128 before mapping its opening. Whole-issue JSON/assets closeout remains.


## 2026-10-13 — August shape-table article extent verified

- Inspected all15 pinned whole-page views127–141 before mapping. 김선호’s
  도형정의표의 정복 occupies128–137, ending with section8 맺음말 and an
  article end mark. Separate 디버깅 룸 errata138, 복덕방 classifieds139–140
  and the lower advertisement140 are excluded. The next listed article’s actual
  title 일본 마이크로 컴퓨터의 현황 begins141. TOC spacing was not used as
  article extent proof.
- Next: map opening128–133 (six pages, nine outside-map lookups), inspect native
  crops, then recognize coherent prose and structured/code regions with adaptive
  routing and a bounded representative table probe. Ending134–137 and full
  assembly remain. No mapping, OCR or production export was added by this check.
- Evidence: `private/pdf-restoration/13-1984-08-adaptive/batch-24/extent-inspection.json`.
  August remains16 complete, zero partial,15 untouched bodies, six pilot selections
  pending, two classified/four unclassified headings and zero human accepted.
  Whole-issue JSON/assets closeout and full proofreading remain pending.


### August shape-table opening128–133 raw selection complete, 2026-10-13

- Prepared opening pages 128–133 of 김선호’s 도형정의표의 정복, whose
  verified full extent is 128–137. The map contains 132 regions: 112 selected
  text drafts and 20 original images. Eight structured tables occupy 26 text
  regions; three BASIC/monitor regions await source row indexing. The batch
  uses six mapped pages and nine outside-map lookups. Ending 134–137 and full
  assembly remain. This checkpoint records raw preparation, not restoration.
- Inspected all 35 original panels and six overlays, 29 first-revision panels,
  three second-revision panels, six final overlays and ten native boundary panels.
  Sixty-one distinct regions changed before OCR. Packed-byte bits remain with
  their vector labels; figure 14 keeps its complete merged 도형정의 label with
  six owning bytes. Both table captions, the SCALE heading and the pointer
  diagram’s final note are complete. Original maps, crops and both revisions
  remain preserved. Of 448 text edges, all 50 residual crossings are inspected
  borders, decorative rules or one scan speck; none crosses a glyph.
- A bounded Tesseract probe preserved five address/value rows but corrupted
  printed ?← placeholders, so structured regions retained Qwen. Original OCR
  completed 35 Qwen and 77 Tesseract drafts plus the unselected Tesseract probe,
  with no failures, retries or cache hits. All 112 drafts were read before selection.
  Empty or garbled headings, column-first table reading, missing vector labels
  and mixed-script BASIC identifiers triggered 13 bounded same-crop alternates:
  six Qwen and seven Tesseract calls. The six Qwen heading drafts and one
  Tesseract table segment were selected. Six other Tesseract alternates lost
  labels/values or were empty and remain unselected. No draft is corrected yet.
- Actual calls: 41 Qwen / 85 Tesseract; selected regions: 40 Qwen / 72 Tesseract.
  All 16,131 local Qwen tokens include 14,330 prompt and 1,801 output tokens,
  including unselected alternates. Tesseract recognition totals 16.379 seconds,
  counting the worker, probe and alternates once. Worker 84.315s, probe 0.071s,
  fallback 10.770s and selection 0.100s are separate, noncausal diagnostics.
  Local monetary weight is zero. Paid uncached/cached input retains 1:0.1;
  the output rate remains unknown.
- Source/crop/map/request/runtime/model/bundle pins and stop outcomes pass.
  The original 1,154-file and selected 823-file seals remain unchanged, along
  with all 32 prior production packages, native 15–23 raw/selected inventories
  and 16,790 pilot files. Selected drafts contain no empty regions, but still
  require source correction, table/diagram associations and literal code review.
  Preserve printed POKE 777 versus PEEK(767+I) and $30A(778) without semantic
  repair. Full proofreading, source encoded bytes and execution remain unverified.
- Evidence: `private/pdf-restoration/13-1984-08-adaptive/batch-24/selected-raw-audit.json`,
  `raw-ocr-audit.json` and `checkpoint-plan-selected.json` in that directory.
  No production opening export exists. August remains 16 complete articles,
  zero partial, 15 untouched bodies, six pilot selections pending, two classified
  and four unclassified headings, and zero human accepted. Next: correct, index,
  export and validate opening 128–133; then restore ending 134–137 and assemble
  the full article. Whole-issue JSON/assets closeout remains.


### August shape-table opening128–133 production restored, 2026-10-13

- Restored opening 128–133 of 김선호’s 도형정의표의 정복, whose verified
  full extent is 128–137. All 112 selected drafts were corrected once against
  source, with all 35 final source panels inspected. The JSON/assets export
  preserves 132 regions, 102 ordered blocks, 20 original images, 112 review
  ranges and 35 source uncertainty flags. Ending 134–137 and full assembly remain.
- Eight tables retain 85 logical rows, 311 logical field slots, 25 blank slots
  and 38 header slots. Logical fields include external byte labels and merged
  continuations; they do not assert independently printed boxes. Figure 6 keeps
  bit rows with their vector labels. Figure 14 preserves merged spans of 2/2/10
  bytes across its source crops. Exact ranges index 441 structured fields and
  side labels, including explicit empty slots.
- Three independent BASIC/monitor groups preserve 12 physical rows: ten printed
  BASIC labels, one DATA continuation and one unnumbered monitor command. Line 60’s
  visible PUKE candidate remains with O/U uncertainty. Table 1’s 777+I/$30A(778)
  and table 2’s 767+I/$300 refer to different examples; the earlier discrepancy
  interpretation is retracted without changing any source literal. Printed
  13-point prose versus seven visible points, the 10진수 heading versus 16진수
  prose, graphical glyph candidates and faint address spacing remain flagged.
- Eighteen figure associations, two unlabelled photos, five diagrams and two
  grids retain original assets. The two vector paths have eight/nine visible
  connections respectively; no missing terminal arrow is invented. Two pointer
  arrows and eight radial rotation labels are indexed. Eight native prose joins
  preserve ten boundaries and every interrupted figure, table, caption and heading.
- Exact UTF-8/table/header/label/listing ranges, source crop pixels and an
  independent byte-identical rebuild pass. All 32 prior production packages,
  original 1,154-file and selected 823-file seals, prior raw/selected inventories
  and 16,790 pilot files remain unchanged. The first prior-package audit lacked
  the immutable Z80 assembly’s existing private boundary adapter; its failed
  helper/diagnostic are preserved. Reusing that pinned adapter passes without
  source, package or shared pipeline changes.
- No new OCR was required for correction/export. The production ledger includes
  all 41 Qwen and 85 Tesseract calls from preparation, including unselected
  alternates; 40 Qwen/72 Tesseract regions were selected. All 16,131 local Qwen
  tokens (14,330 prompt/1,801 output) and 16.379 seconds of Tesseract recognition
  are counted once. Local monetary weight is zero; paid input retains 1:0.1
  uncached/cached weighting, output rate unknown. Time observations are noncausal.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-24/shape-table/`.
  Source index: `build/pdf-restoration/13-1984-08-adaptive-shape-table-source-index-24/source-index.json`.
  Evidence: `private/pdf-restoration/13-1984-08-adaptive/batch-24/validation.json`.
  August now has 16 complete articles, one partial shape-table article, 14 untouched
  bodies, six pilot selections pending, two classified/four unclassified headings
  and zero human accepted. Next: ending 134–137, then full 128–137 assembly.
  Whole-issue JSON/assets closeout, human acceptance/full proofreading, source
  encoded bytes and historical execution remain pending. No reading-room rebuild.


### August shape-table ending134–137 raw selection complete, 2026-10-13

- Prepared ending 134–137 of 김선호’s 도형정의표의 정복, whose full
  source-verified extent is 128–137. Four whole ending pages were reinspected;
  the original fifteen-page extent and eleven outside-map lookups were reused
  from exact pinned evidence. The batch preserves 113 regions, 99 selected text
  drafts and 14 original figure assets. Twenty-nine code regions cover eight
  independent BASIC programs and one monitor group; the color table occupies
  two text regions. Physical row/cell/diagram counts await source correction.
- All 30 original panels and four original overlays were inspected, followed
  by all 27 first-revision panels, two second-revision panels, four final overlays
  and three native boundary panels. Sixty-one distinct crops changed before OCR.
  Skewed program rows were regrouped without clipping; terminal words remain
  complete, and program 10’s source image retains its full frame and caption.
  All 396 text edges pass: 14 residual crossings are inspected rules, borders,
  an adjacent diagram circle/arrow or a pointer stem; none crosses a glyph.
- One bounded Tesseract color-table probe lost values, color names and row
  associations, so both structured regions retained Qwen. Original OCR completed
  39 Qwen and 60 Tesseract drafts, plus the unselected Tesseract probe. All 99
  drafts were read. Five empty headings and damaged command/address/method
  identifiers triggered 17 bounded Qwen alternates, one per unchanged crop.
  Fifteen were selected; two tiny grid-label alternates returned ILLEGIBLE and
  remain unselected. Their original drafts need direct correction from the scan.
  All calls stopped normally; no inference failures, retries or cache hits.
- Actual calls: 56 Qwen / 61 Tesseract; selected regions: 54 Qwen / 45 Tesseract.
  All 24,133 local Qwen tokens include 20,367 prompt and 3,766 output tokens,
  including both unselected label readings. Tesseract recognition totals
  10.503s, counting the probe once. Worker
  80.049s, alternate worker 51.828s
  and selection 0.082s are separate noncausal diagnostics.
  Local monetary weight is zero; paid uncached/cached input retains 1:0.1
  weighting and the output rate remains unknown.
- Exact source/crop/map/request/runtime/model/bundle pins and stop outcomes pass.
  Original 1,014-file and selected 857-file seals remain unchanged, alongside
  all 33 prior production packages, native 15–24 raw/selected inventories and
  16,790 pilot files. All 99 selected drafts are nonempty, but none is corrected
  yet. Printed BASIC mistakes, cassette/disk command punctuation and address
  contradictions still require source-linked literal review; no execution or
  source encoded-byte certification. The earlier opening address-context
  clarification remains unchanged.
- Evidence: `private/pdf-restoration/13-1984-08-adaptive/batch-25/selected-raw-audit.json`,
  `raw-ocr-audit.json` and `checkpoint-plan-selected.json` in that directory.
  No ending production export exists. August remains 16 complete articles,
  one partial shape-table article, 14 untouched bodies, six pilot selections
  pending, two classified/four unclassified headings and zero human accepted.
  Next: correct/index/export/validate ending 134–137, then assemble full 128–137.
  Whole-issue JSON/assets closeout remains; no reading-room rebuild.


### August shape-table ending134–137 production restored, 2026-10-13

- Restored ending 134–137 of 김선호’s 도형정의표의 정복. All 99 selected
  drafts were corrected once against source, with all 30 final source panels
  inspected. The JSON/assets export retains 113 regions, 93 ordered blocks,
  14 original images, 99 review ranges and 23 source uncertainty flags.
  Opening 128–133 remains immutable; separate full 128–137 assembly is next.
- Eight independent BASIC programs and one monitor group retain 144 physical
  rows: 123 printed BASIC labels, 20 continuations and one unnumbered row.
  Program 7’s absent labels 110/130 remain absent; program 8 is independent.
  DATA wraps, repeated PEEK calls, split SCALE value and XC row remain physical
  source rows. Printed 240.149, DATA separator ambiguity, XDARW diagram spelling,
  third flow heading’s left arrow, BLOAD comma and unmatched closing parenthesis
  remain literal. Faint O/0, I/1, 3/5 and monitor period/comma candidates are flagged.
- The color table retains three rows/twelve data fields and four header slots,
  including one blank merged continuation. It has three printed header boxes
  and twelve data boxes. Exact ranges index 34 structured fields/labels,
  18 inline command examples and 37 printed address fields. Ten displayed monitor
  values retain their original widths and the $600 A pointer label.
- All fourteen figure associations retain original assets. Three animation
  flows preserve eleven boxes and eleven directed connections; the monitor
  pointer adds one connection. Three grids preserve 18/5/8 patterned points
  and one separate filled reference point. Grid 20 retains three points in
  one cell rather than invented integer positions. The closing article mark
  remains a bitmap. Four prose joins preserve six boundaries and every original
  interrupted image, listing, caption and heading.
- Exact UTF-8/text/review/field/header/caption/listing ranges, source crop pixels
  and an independent byte-identical rebuild pass. All 33 prior production packages,
  original 1,014-file and selected 857-file seals, native 15–24 raw/selected
  inventories and 16,790 pilot files remain unchanged. An initialization helper
  failed before any correction because it mixed relative paths with absolute ROOT;
  its diagnostic is preserved. Resolving the path reused all thirty rendered
  panels without new OCR or a second correction. Shared pipeline is unchanged.
- No new OCR was required for correction/export. Accounting retains all 56 Qwen
  and 61 Tesseract calls from preparation, including the unselected table probe
  and two ILLEGIBLE grid-label alternates. Selected 54 Qwen/45 Tesseract drafts
  were corrected once. All 24,133 local Qwen tokens (20,367 prompt/3,766 output)
  and 10.503s of Tesseract recognition are counted once. Local monetary weight
  is zero; paid uncached/cached input remains 1:0.1, output rate unknown.
  Worker, probe, alternate, selection and correction time observations are noncausal.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-25/shape-table/`.
  Source index: `build/pdf-restoration/13-1984-08-adaptive-shape-table-source-index-25/source-index.json`.
  Evidence: `private/pdf-restoration/13-1984-08-adaptive/batch-25/validation.json`.
  August remains 16 complete articles, one partial awaiting shape-table assembly,
  14 untouched bodies, six pilot selections pending, two classified/four unclassified
  headings and zero human accepted. Next: full 128–137 assembly, then remaining
  articles and whole-issue JSON/assets closeout. Full proofreading, source encoded
  bytes and historical execution remain unverified. No reading-room rebuild.


### August full shape-table128–137 assembled, 2026-10-13

- Assembled 김선호’s 도형정의표의 정복, full pages 128–137, from the
  exact validated native 24/25 packages. Separate whole-page 133/134 inspection
  confirms ROT prose ends completely before the next program/DRAW subsection;
  no cross-native prose or listing join is added. Only the two segment-scope
  notes are resolved. Human review and all source uncertainties remain pending.
- Full JSON/assets export retains 245 regions, 211 source readings/review ranges,
  195 ordered blocks, 34 original images and 58 native source flags. Twelve
  independent listing groups preserve 156 physical rows, 133 numbered logical
  rows, 21 continuations and two unnumbered monitor rows. Listing bytes equal
  the native concatenation; printed mistakes, missing labels and glyph candidates
  are unchanged. All twelve native prose joins and sixteen boundaries remain.
- Nine tables retain 88 logical data rows, 323 data fields, 25 data blanks and
  42 header slots, including the color header’s blank merged continuation.
  The full source index preserves all 475 structured slots: 473 main fields
  and two side labels. All 2,146 exact native ranges are projected into the
  combined text/listing; original native index metadata remains inspectable.
- Thirty-two figure associations and two unlabelled photos retain their source
  assets. Nine diagrams preserve 31 directed relations; five grids preserve
  45 patterned points and one separate reference point. Distinct graph node
  identities prevent the repeated numeric labels from colliding. Eighteen
  ending inline examples, 37 address fields and the bitmap article-end mark
  retain exact source readings without invented geometry or Unicode substitutes.
- Independent full export/coverage/canonical/range checks and a byte-identical
  rebuild pass. All 34 prior production packages, native 15–25 raw/selected seals
  and 16,790 pilot files remain unchanged. No new OCR, mapping or rasterization;
  native inference costs are not counted again. Local compute/token monetary
  weight remains zero; paid uncached/cached input is 1:0.1, output rate unknown.
- Export: `build/pdf-restoration/13-1984-08-adaptive/shape-table/`.
  Source index: `build/pdf-restoration/13-1984-08-adaptive-shape-table-source-index/source-index.json`.
  Evidence: `private/pdf-restoration/13-1984-08-adaptive/shape-table-assembly-validation.json`.
  August now has 17 restored articles, zero partials, 14 untouched bodies,
  six pilot selections pending, two classified/four unclassified headings and
  zero human accepted. Next: verify the source extent of 읽을 거리 : 일본
  마이크로 컴퓨터의 현황, starting141, then restore bounded segments. Whole-issue
  JSON/assets closeout remains. No reading-room rebuild; full proofreading,
  source encoded bytes and historical execution remain unverified.


### August Japanese exhibition report141–145 extent verified, 2026-10-13

- Individually inspected all seventeen pinned whole-page views140–156.
  읽을 거리 : 일본 마이크로 컴퓨터의 현황 (canonical0020, 이홍철) occupies
  exactly141–145. The printed title omits the canonical 읽을 거리 prefix;
  canonical title/byline/parent are preserved. The editorial introduction names
  the Osaka exhibition and reporter. Page145 closes with an exhibition overview
  and complete final paragraph ending in ellipsis; no separate end mark or
  continuation instruction is visible.
- All intervening146–154 pages are separate advertisements, individually checked.
  Actual 정보 레이다 opens155 and continues156. Classified/ad140 is excluded.
  TOC spacing was not treated as extent proof. The revised batch covers five
  article pages with twelve outside-map lookups, within the six-page/twenty-lookup
  limits; the initial provisional141–146 mapping plan is superseded.
- The report has eight exhibition photographs (one each141/142/143, two144,
  three145), two separate pull quotes and vendor subsections. There are no code
  listings, structured tables or diagrams. Clear prose/headings/introduction/
  quotes start with Tesseract; crop-level failures may justify bounded fallback.
  Three-column order, the143/144 Epson continuation and144 Oki column continuation
  must be source-mapped explicitly. Preserve all original model names/spellings.
- Fifteen new whole-page renders and two unchanged reused views are retained.
  Initial rendering preceded the prospective preparation window and remains
  visible as between-window overhead. No mapping, native crop gate, recognition,
  correction or production export is claimed by this checkpoint.
- Evidence: `private/pdf-restoration/13-1984-08-adaptive/batch-26/extent-inspection.json`.
  Canonical/source/render pins pass. All existing production/raw/pilot records
  remain unchanged. August remains17 restored, zero partials,14 untouched bodies,
  six pilot selections pending, two classified/four unclassified headings and
  zero human accepted. Next: map/native-crop-check/recognize the complete141–145
  report. Whole-issue JSON/assets closeout remains; no reading-room rebuild.


### August Japanese exhibition report141–145 crop gate passed, 2026-10-13

- The complete141–145 Japanese microcomputer exhibition report now has52
  reviewed source regions:44 clear-text regions and eight preserved photographs,
  including two independent pull quotes. Tesseract is assigned to all44 text
  regions; no preparation probe or Qwen call was required.
- Five original overlays, all15 first revised panels, second-revision panel10,
  and all five final overlays were individually inspected. The original15
  panels are preserved without a claim of individual review. Twenty-one distinct
  regions were revised before OCR; the OFFICE PAK crop received a second edge
  adjustment. Both revision records and original crops remain preserved.
- All52 final crops match the pinned native source pixels. The176 text-edge
  checks report zero crossings. Canonical identity, three-column order, Epson
  and Oki continuations, original model spellings and the concluding ellipsis
  remain source-linked. Eight photograph assets will retain their source content.
- Crop gate: `private/pdf-restoration/13-1984-08-adaptive/batch-26/preflight-acceptance.json`.
  Recognition, source correction and export remain pending. August remains17
  restored, zero partials,14 untouched bodies, six pilot selections pending,
  two classified/four unclassified headings and zero human accepted.
- Next:44 Tesseract drafts, one source-based correction pass, complete141–145
  JSON/assets export and independent validation. No reading-room rebuild.


### August Japanese exhibition report141–145 restored, 2026-10-13

- Restored the complete141–145 Japanese microcomputer exhibition report,
  canonical0020, 이홍철. Its52 regions retain35 ordered text blocks, eight
  original photographs,44 regional text ranges and two independent pull quotes.
  Canonical title/byline/parent/page remain unchanged; the actual printed title
  is retained inside the body. No deferred article pages or separate assembly.
- All44 selected Tesseract drafts were read and corrected once against all15
  pinned source panels. Actual calls:44 Tesseract, zero Qwen, zero probes,
  failures, retries or alternates. No Qwen server/model startup. Recognition
  took12.160s and the raw worker took
  15.532s; these are separate local diagnostics,
  not measured human-time or monetary savings. Local monetary weight is zero;
  paid uncached/cached input retains1:0.1 weighting and output rate remains unknown.
- Six prose joins preserve nine adjacent column/page/paragraph boundaries.
  The141/142 terminal-word continuation remains explicitly linked around its
  independent pull quote and photograph, preserving the original object order.
  All eight unlabelled photographs remain exact source pixels with no invented
  captions. There are no listings, structured tables or diagrams in this report.
- Thirty-eight source-linked flags preserve historical wording/model names,
  printed specifications and glyph candidates. Sony’s overprinted model digit
  remains HB[4/7]5; brackets denote editorial alternatives, not printed characters.
  Native ending reads 건장한 소년들이었지만…; the earlier extent shorthand 착한
  is retained unchanged with an attached correction note. The verified141–145
  extent and complete concluding paragraph are unchanged by that clarification.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-26/japan-microcomputers`.
  Index: `build/pdf-restoration/13-1984-08-adaptive-japan-microcomputers-source-index-26/source-index.json`.
  Independent regional/review/flag byte ranges, source continuations, canonical
  identity, original crop pixels and byte-identical rebuild pass. All35 prior
  production packages, native15–25 raw/selected inventories,437 batch26 sealed
  files and16,790 pilot files remain unchanged. One raw-audit counter assertion
  was corrected in the validator; its original script/failure is preserved,
  and no recognition was repeated. Evidence: batch26 `validation.json`.
- August now has18 restored articles, zero partials,13 untouched bodies,
  six pilot selections pending, two classified/four unclassified headings and
  zero human accepted. Human review, full proofreading and source encoded bytes
  remain unverified. Next: source-verify the actual extent of 정보 레이다155,
  then bounded native restoration; do not infer extent from TOC spacing.
  Remaining bodies/pilots/headings and whole-issue JSON/assets closeout remain.
  No HTML/frontend/browser or reading-room rebuild.


### August radar155–160 raw selection ready, 2026-10-13

- Source-verified information radar155–165 from seventeen individually viewed
  whole-page scans154–170. Its final item ends165 before advertisement166;
  business divider167 and distinct 자료구조168–170 are excluded. Opening155–160
  uses six mapped pages/eleven outside-map lookups; ending161–165 and full
  assembly remain. Canonical0040 title/byline/parent/page are unchanged.
- Classified pageless 비즈니스0021 as a non-owning heading from divider167 and
  its three source child listings168/172/181. Printed 비지니스 spelling is retained
  as source evidence; canonical spelling/child identities remain unchanged.
  Separate 읽을거리141 listing does not change canonical0020 ownership.
- Opening68 regions retain59 selected text drafts, five original photographs
  and four original table images. All six original overlays, nineteen first
  revised panels, second revised panel18 and five changed final overlays were
  individually inspected; unchanged157 overlay is an exact reuse. Six distinct
  regions changed before inference; one received a second adjustment. Original
  and intermediate failed crop diagnostics remain preserved. Final236 boundary
  checks report zero crossings and all68 crops match native source pixels.
- One bounded Tesseract table probe lost headers/models/rows/value association,
  so four ruled specification tables and one contact list used Qwen. Clear text
  started with Tesseract. Five heading drafts lost whole lines/identifiers;
  one bounded Qwen heading probe preserved the missing lines and was reused,
  followed by one alternate for each of the other four affected headings.
  Selected49T/10Q drafts await source correction. Empty 나라밖 소식 section
  labelp160r05 will be source-read directly once; it is not an empty-source claim.
- Actual recognition:55T calls (54 worker plus one unselected table probe),
  tenQ calls (five worker plus five heading alternates, including the selected
  heading probe), zero inference failures/retries. All59 original/five alternate
  drafts were inspected. AllQ calls total7,080 input/1,072 output local tokens.
  T recognition took18.578s and Q recognition
  14.030s; worker/extra-startup/selection durations
  remain separate noncausal diagnostics. Local compute/token monetary weight
  is zero; paid uncached/cached input is1:0.1 with output rate unknown.
- Original675-file and selected416-file seals pass. All36 prior production
  packages, native15–26 raw/selected seals and16,790 pilot files are unchanged.
  A validator generator's overbroad numeric-substring assertion was corrected
  before audit; its failure is recorded and no inference repeated. Evidence:
  `private/pdf-restoration/13-1984-08-adaptive/batch-27/selected-raw-audit.json`.
- No source correction or production export is claimed. August remains18
  restored, zero partials,13 untouched bodies andsix pilot selections pending;
  headings nowthree classified/three unclassified, human accepted zero. Next:
  once-only selected-draft correction, source table/news/continuation indexes,
  validated opening155–160 JSON/assets export, then ending161–165/full assembly.
  Natural-language item160 continues163 around other news161–162; retain that
  ownership explicitly. Remaining articles/pilots/headings and issue closeout
  remain. No HTML/frontend/browser or reading-room rebuild.

### August radar correction resumed, 2026-10-13

- Individually inspected source-correction panels01–05 and corrected sixteen
  selected text drafts covering155–156 exactly once. The printed 금상사의,
  heading/body word order, historical spellings, technical claims and paragraph
  boundaries remain literal; twenty-two source-linked uncertainty records await
  human review. Photographs retain their source images without invented captions.
- Both raw inventories remain unchanged:675 original and416 selected files.
  Correction-region coverage, selected-draft provenance and all five panel pins
  pass. Evidence:
  `private/pdf-restoration/13-1984-08-adaptive/batch-27/correction-part01-validation.json`.
- Forty-three text regions remain. Resume at panel06/page157, reusing the saved
  first part. Complete correction, source table/news/continuation indexes and
  validated opening155–160 JSON/assets export; then restore161–165 and assemble
  the full radar. No new OCR or production export; restoration counts remain
  unchanged and human acceptance is pending. Reporting/commit usage carries
  into the next audit. No reading-room rebuild.

### August radar opening155–160 validated, 2026-10-13

- Completed all59 selected source corrections after nineteen individually viewed
  panels. The JSON/assets opening contains44 ordered text blocks, nine original
  images, three source captions and74 source-linked uncertainty records. Nine
  prose joins preserve fifteen adjacent boundaries. Human acceptance remains
  pending; this is a partial opening of verified full155–165.
- Fifteen news candidates retain fourteen complete domestic items and the first
  foreign item opening. Its natural-language discussion continues163 around five
  independent items161–162, without an invented cross-page word join. Four
  specification tables retain40 printed candidate rows/114 field slots/19 blanks;
  source geometry has38 ruled rows/108 logical slots/15 blanks, including two
  headers. Printer density/font multiline cells remain distinct from the ruled
  speed rows. Seven contact fields span eight printed lines. Original table
  bitmaps, spellings, apparent mistakes and historical claims remain authoritative.
- Recovered emptyOCR 나라밖 소식 directly from its scan. Native source confirms
  키콤 and 화콤코리아, superseding earlier extent shorthand without changing that
  evidence. One unsupported assistant duplication of 불구하고 was retracted;
  its initial proposal and recovery remain preserved. No new recognition calls.
- Complete regional/review/news/table/contact UTF-8 ranges, source crop pixels,
  coverage/ownership and existing news/reference projections pass. Independent
  rebuild is byte-identical. All36 prior packages, native15–27 raw/selected seals
  and16,790 pilot files remain unchanged. Production accounting includes all
  original55T/tenQ calls and8,152 local Q tokens once; local monetary weight zero.
  Paid uncached/cached input remains1:0.1, output rate and human effort unknown.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-27/radar`.
  Source index: `build/pdf-restoration/13-1984-08-adaptive-radar-source-index-27`.
  Validation: `private/pdf-restoration/13-1984-08-adaptive/batch-27/validation.json`.
- August now18 complete, one partial,12 untouched bodies, six pilot selections
  pending and three classified/three unclassified headings; human accepted zero.
  Native28 restores161–165 from the pinned extent, then a separate full radar
  assembly follows exact native27/28 pins. Remaining articles/pilots/headings and
  whole-issue JSON/assets closeout remain. No reading-room rebuild; reporting and
  commit usage after the audit cutoff carries into the next audit.


### August radar ending161–165 raw drafts validated, 2026-10-13

- Reused the pinned full 155–165 extent and seventeen whole-page scans;
  actually reinspected 161–166 before mapping. Ending161–165 has 53 regions:
  52 text regions and one original terminal ornament, nine new foreign reports
  numbered 16–24, natural-language item 15 continuation on 163 and item 23 across 164/165.
- Revised 32 distinct crops before inference; six received a second adjustment.
  Original/intermediate diagnostics and all source crops remain preserved.
  Fourteen final panels and five final overlays were individually inspected,
  with unchanged panels01/02 reused by exact hash. All 53 crops match native pixels.
  The 208-edge diagnostic has zero glyph crossings and two explicitly classified
  non-text scanner-band crossings near the top of 162, far above the heading.
- Reused batch 27 heading evidence: 42 clear-text Tesseract calls and ten Qwen
  calls for nine multilevel headings and one Hanja paragraph. Zero preparation
  probes, failures, retries or alternate calls. All 52 drafts read. Four repeated
  running headers have empty OCR and require direct source correction; no empty
  source is claimed. Technical values, spellings and paragraph joins remain pending.
- Qwen used 6,011 input/403 output local tokens; recognition took
  6.963s, Tesseract 19.528s.
  Worker/model-startup duration remains separate. Local monetary weight is zero;
  paid input ratio remains 1:0.1 and output rate/human effort remain unknown.
- Independent source/runtime/raw-bundle checks pass. The 557-file seal preserves
  all attempts and geometry. All 37 prior production packages, native 15–27 raw/
  selected seals and 16,790 pilot files remain unchanged. Evidence:
  `private/pdf-restoration/13-1984-08-adaptive/batch-28/raw-ocr-audit.json`.
- No new production export or completed article is claimed. August remains 18
  complete, one partial, 12 untouched bodies, six pilot selections pending and
  three classified/three unclassified headings; human accepted zero. Next:
  once-only correction of 52 selected texts, validated ending161–165 JSON/assets
  export and commit, then separate full radar155–165 assembly. Remaining August
  bodies/pilots/headings and issue closeout remain. No reading-room rebuild. Reporting and commit usage after the audit
  cutoff carries into the next audit.


### August radar ending161–165 validated, 2026-10-13

- Corrected all 52 selected ending drafts once from fourteen individually viewed
  source panels and an additional native crop. Four empty running headers were
  transcribed directly from their scans. Seventy source-linked uncertainty records
  preserve printed spellings, model discrepancies, Hanja and historical claims;
  human acceptance remains pending. No new recognition calls.
- Ending 161–165 JSON/assets contains 26 ordered text blocks and one original
  terminal ornament. Ten prose joins preserve 26 native boundaries, including
  the no-space 있었/는데 join across 164/165 around its explicit non-owning running header.
  That header remains separate; its physical position and interruption are pinned.
- Nine new foreign news entries 16–24 retain source ownership. The seven regions
  continuing natural-language item 15 on 163 are separately indexed, preserving
  its opening on 160 and intervening five reports on 161–162 without a fabricated headline
  or cross-segment word join. Final USA address and source endmark remain distinct.
- Independent regional/review/news/continuation UTF-8 ranges, source crop pixels,
  raw settings/hashes and existing news/reference projections pass. A separate
  rebuild is byte-identical. All 37 prior production packages, native 15–28 raw/
  selected seals and 16,790 pilot files remain unchanged. Actual 42T/tenQ calls and
  6,414 local Q tokens remain counted once; local monetary weight zero. Paid input
  ratio remains 1:0.1; output rate/human review effort unmeasured.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-28/radar`.
  Source index: `build/pdf-restoration/13-1984-08-adaptive-radar-source-index-28`.
  Validation: `private/pdf-restoration/13-1984-08-adaptive/batch-28/validation.json`.
- August remains 18 complete, one partial, 12 untouched bodies, six pilot selections
  pending and three classified/three unclassified headings; human accepted zero.
  Both radar natives now cover 155–165. Next is a separate full assembly from exact
  native 27/28 pins, followed by remaining August bodies/pilots/headings and whole-issue
  JSON/assets closeout. No reading-room rebuild; reporting/commit usage after the
  audit cutoff carries into the next audit.


### August full radar155–165 assembled, 2026-10-13

- Assembled full information radar155–165 from the exact native27/28
  packages. All24 news items have complete, disjoint source ownership:14 domestic
  and ten foreign. Item15 continues from160 to163 around five independent reports
  on161–162. Its full ownership is resolved in the assembled source index while
  the opening native's partial metadata remains unchanged.
- JSON/assets retains121 regions,111 regional readings/review ranges,70 ordered
  text blocks,ten original images,three source captions and144 source-linked
  uncertainty records. All19 native prose joins and41 boundaries remain intact,
  including the164/165 word continuation around its non-owning running header.
  Four tables preserve40 candidate rows/114 slots/19 blanks and38 ruled rows/
  108 logical slots/15 blanks, including two headers. Seven contact fields retain
  eight source lines. Human acceptance and full proofreading remain pending.
- All470 original segment files are copied exactly. The full source index
  preserves every native metadata key and projects788 exact UTF-8 ranges and801
  asset references. Independent coverage, ownership, table/contact/range checks
  and a byte-identical rebuild pass. All38 prior production packages, native15–28
  raw/selected seals and16,790 pilot files remain unchanged. No new OCR or mapping;
  native recognition costs are not counted again.
- Export: `build/pdf-restoration/13-1984-08-adaptive/radar`.
  Source index: `build/pdf-restoration/13-1984-08-adaptive-radar-source-index/source-index.json`.
  Evidence: `private/pdf-restoration/13-1984-08-adaptive/radar-assembly-validation.json`.
- August now has19 complete assistant restorations,zero partials,12 untouched
  bodies,six pilot selections pending,three classified/three unclassified headings
  and zero human accepted. Next: verify the source extent of 이근배's 자료구조,
  starting168, then restore it under adaptive routing. Remaining articles/pilots/
  headings and whole-issue JSON/assets closeout remain. No reading-room rebuild.
  Local compute/token monetary weight remains zero; paid input ratio is1:0.1,
  output rate/human effort unmeasured. Reporting/commit usage after the audit
  cutoff carries into the next audit.


### August tree article168–171 selected raw drafts validated, 2026-10-13

- Individually inspected six whole-page views167–172. 이근배's 자료구조
  occupies exactly168–171; the source has series4 and subtitle트리구조. Its final
  paragraph/figure11 and printed endmark close171. Business divider167 and new
  의료보험수가계산172 are excluded. Four views reused by exact hash; two fresh
  whole views and four native4000-pixel renders retained. Two outside-map lookups.
- Mapped63 regions:50 text crops and13 original image crops preserving eleven
  numbered figures in twelve parts plus the endmark. Figure5's lower(a)/(b) and
  upper(c)/(d) remain distinct source parts. Figure8's two15-row address/memory
  arrays retain original bitmaps; explicit structured correction of30 rows/60
  slots/eleven blank memory fields remains pending. No source code listing.
- Revised seven distinct crops before recognition, preserving original/intermediate
  geometry and diagnostics. All18 original panels, six changed final panels and
  four final overlays were individually inspected; twelve unchanged panels match
  original bytes. All63 crops match native pixels. The200-edge diagnostic has zero
  glyph crossings and eight classified non-text shaded-heading background cuts.
- Ran44Tesseract and six initialQwen calls; one bounded unchanged-cropQ alternate
  recovered the scrambled two-line genealogy sentence. All50 original drafts and
  the alternate were read. Selected43T/sevenQ drafts await once-only correction.
  No empty drafts, failures, retries or preparation probes; original failed-order
  T draft retained. Printed geneological, inline values and historical claims are
  source candidates, not silently modernized or mathematically certified.
- AllsevenQ calls used3,857 input/762 output local tokens,4,619 total, counted
  once. Q recognition took9.460s andTesseract
  10.008s; worker/startup/selection durations
  remain separate. Local monetary weight is zero; paid input ratio1:0.1 and
  output rate/human effort remain unmeasured.
- Independent runtime/raw-bundle/selected-provenance checks pass. Seals preserve
  678 original and317 selected/alternate files. All39 prior production packages,
  native15–28 raw/selected inventories and16,790 pilot files remain unchanged.
  Evidence: `private/pdf-restoration/13-1984-08-adaptive/batch-29/selected-raw-audit.json`.
- August remains19 complete assistant restorations,zero partials,12 untouched
  bodies,six pending pilot selections,three classified/three unclassified headings
  and zero human accepted. Next: source correction, diagram/formula/array indexes
  and complete168–171 JSON/assets export. Remaining articles/pilots/headings and
  issue closeout remain. No reading-room rebuild. Reporting/commit usage after
  the audit cutoff carries into the next audit.


### August complete tree article168–171 restored, 2026-10-13

- Restored the complete168–171 자료구조 article by 이근배, canonical0022.
  Source series4/subtitle트리구조 and canonical title/byline/business-parent/page
  remain intact. Its63 regions yield46 ordered text blocks,50 regional readings,
  twelve original figure parts covering eleven numbered figures and a terminal
  endmark. No deferred article pages or separate assembly.
- All50 selected drafts (43T/sevenQ) were corrected once against18 pinned source
  panels, with four persisted correction parts. No new recognition during correction
  or export. Actual recognition remains44T/sevenQ, including one bounded unchanged-
  crop genealogy alternate; the scrambled originalT draft and all raw evidence remain.
- Two15-row memory arrays retain30 data rows/60 field slots and eleven empty
  memory fields, plus two2-cell headers. Independent row/cell UTF-8 ranges preserve
  blank fields. Eleven searchable diagram graphs retain nodes, edges, binary link
  positions, level/subtree annotations and complete-tree indices. Variable-length
  and binary-node field layouts, ten figure9 null slots and five figure11 null slots
  remain source candidates beside authoritative bitmaps; no encoded bytes inferred.
- Three prose joins retain four column boundaries, including 디그/리 and 된/다.
  The displayed maximum-node formula stays independent with explicit incoming and
  outgoing prose. Both recursive definitions, eight formula/position examples and
  nineteen Unicode glyph ranges are indexed. Forty-six source flags retain literal
  geneological, seqen-tial, the omitted 빈 in the(c) clause, level1/l candidates,
  exponent/subscript typography and body0 versus diagram open-circle null readings.
  Source mathematical claims, encoded bytes and full proofreading remain unverified.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-29/tree`.
  Index: `build/pdf-restoration/13-1984-08-adaptive-tree-source-index-29/source-index.json`.
  Independent coverage, source pixels/raw hashes, exact regional/review/cell/flag
  ranges, figure associations, graph/null fields, canonical identity and byte-identical
  rebuild pass. All39 prior production packages, native15–29 raw/selected seals
  (including678 original/317 selectedbatch29 files) and16,790 pilot files remain
  unchanged. A validator-only qwen/qwen3-vl naming assertion was corrected; its
  failed script and recovery record remain. No source/export changes or OCR retries.
- August now has20 complete assistant restorations,zero partials,eleven untouched
  bodies,six pilot selections pending,three classified/three unclassified headings
  and zero human accepted. Forty production packages comprise29 natives,nine
  assemblies andtwo production selections. Next: source-verify actual full extent
  of 의료보험수가계산172 before mapping; then remaining bodies/pilots/headings
  and whole-issue standaloneJSON/assets closeout. No reading-room rebuild.
  Local compute/token monetary weight is zero; paid input ratio1:0.1,output rate
  and human effort remain unmeasured. Reporting/commit usage after the audit cutoff
  carries into the next audit.


### August medical-insurance opening172–177 selected raw drafts validated, 2026-10-13

- Verified the complete 의료보험수가계산 article by 컴퓨텍, canonical0023,
  occupies172–180. All twelve whole-page views171–182 were inspected: previous
  tree ending171 and new VISICALC181–182 are excluded. Two views reused by exact
  hash, ten fresh whole views and six native4000-pixel renders retained. Opening
  checkpoint172–177 has six outside-map lookups; ending178–180 remains deferred.
- Final mapping preserves56 regions:50 text crops and six original images,
  comprising flowchart1, complete report2 and four complete listing-page bitmaps.
  Twenty-four searchable BASIC chunks cover the complete first program174–177;
  two six-row control-key tables await exact cell indexes. Report caption173r02
  also appears inside authoritative bitmap173r03; retain that explicit association.
- All21 original panels, ten changed final panels and six final overlays were
  individually inspected; eleven unchanged panels match original bytes. Nineteen
  distinct original region IDs were affected before recognition; one superseded
  chunk176r07 was merged into176r06, retaining all original/intermediate crops.
  All56 final crops match native pixels. The200-edge diagnostic has zero glyph
  cuts and five non-text crossings: four shaded-series edges and one header rule.
- Two boundary-selector failures made no map/crop changes. A diagnostic inventory
  accidentally included its preceding inventory hash during retry setup; both
  preceding versions were reconstructed and hash-verified, and the current original
  inventory/source diagnostic remain intact. Recovery evidence is preserved.
- Ran23Tesseract/27Qwen original calls, then four bounded unchanged-crop alternates
  after all50 authoritative drafts were read. ThreeQ alternates recover lost
  numeric/control-key/action fields. OneT alternate retains a5022 continuation
  scaffold but damages identifiers/numbers and is unselected; correct that omitted
  row from the scan once. All four alternates were read. Selected20T/30Q drafts
  await correction. No empty drafts, runtime failures, retries or preparation probes.
  A preliminary file-glob check read auxiliary Tesseract files; the independent
  audit disproved its empty-draft finding before any dependent recognition.
- Actual recognition is24T/30Q, all counted once. All30Q calls used30,259 input
  and6,742 output local tokens,37,001 total. Q recognition took
  85.491s andTesseract
  5.274s; worker/startup/fallback/selection
  durations remain separate. Local monetary weight is zero; paid input ratio1:0.1,
  output rate and human effort remain unmeasured.
- Independent raw/runtime/bundle/selected-provenance checks pass. Seals preserve
  663 original and407 selected/alternate files. All40 prior production packages,
  native15–29 raw/selected inventories and16,790 pilot files remain unchanged.
  Evidence: `private/pdf-restoration/13-1984-08-adaptive/batch-30/selected-raw-audit.json`.
- August remains20 complete assistant restorations,zero partials,eleven untouched
  bodies,six pending pilot selections,three classified/three unclassified headings
  and zero human accepted. Next: source-correct/export/index opening172–177,
  restore ending178–180 and assemble full172–180. Programs2–4 are printed
  differences only; do not invent complete runnable listings. Remaining bodies,
  pilots,headings and standalone issue JSON/assets closeout remain. No reading-room
  rebuild. Reporting/commit usage after the audit cutoff carries into the next audit.


### August medical-insurance opening172–177 restored, 2026-10-13

- Restored opening172–177 of source-verified full172–180 의료보험수가계산,
  canonical0023/byline컴퓨텍/business parent0021. All56 mapped regions retain
  48 ordered text blocks,50 regional readings and six original images: flowchart1,
  complete report2 and four complete listing-page bitmaps. Ending178–180 and
  separate full assembly remain; the article is explicitly partial.
- All50 selected drafts (20T/30Q) were corrected once against21 pinned source
  panels in five saved parts. No new recognition during correction/export. Actual
  recognition remains24T/30Q, including three selectedQ control-key/value alternates
  and one unselectedT code alternate. The5022 continuation omitted by originalQ
  was transcribed directly from its scan. All663 original/407 selected evidence
  files and every alternative remain unchanged.
- The complete first BASIC listing174–177 retains24 text chunks and234 physical
  rows:169 numbered source candidates,61 nonblank wraps and four layout blanks.
  Two overlapping printed5120/5122 rows remain distinct flagged candidates; faint
  source7030 retains its overexposure warning. Final1756700 and1766520 are trailing
  operands of5175/6600, not additional numbered statements. Printed duplicate
  INPUTWA$, openquote15040, CALL868 versus-868, PRINTGOSUB and doublecolon remain.
  Quoted spaces/punctuation/Hangul and historical source bytes/execution unverified.
- Two six-row control-key tables retain30 exact field cells without invented
  headers. Two source prose joins preserve OFF(CTRL+R across full report173 and
  서브루/틴 across174 columns, with all interrupted headers/caption/image recorded.
  One searchable flowchart retains seven nodes/ten edges beside its authoritative
  bitmap. Four inline/contact/key examples and four Unicode glyph ranges are
  indexed. Forty-seven source flags retain printed spelling, code errors and
  ambiguous readings. Report tiny cells/ruled layout/footnote/dimensions remain
  preserved in the complete image; its caption also has an explicit text association.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-30/medical`.
  Index: `build/pdf-restoration/13-1984-08-adaptive-medical-source-index-30/source-index.json`.
  Independent canonical identity, coverage, source pixels/raw hashes, exact text/
  review/table/flag/listing ranges, wrap classification and byte-identical rebuild
  pass. All40 prior production packages,native15–30 raw/selected seals and16,790
  pilot files remain unchanged. No shared pipeline change or new OCR required.
- August now has20 complete assistant restorations,one partial medical article,
  ten untouched bodies,six pending pilot selections,three classified/three
  unclassified headings and zero human accepted. Forty-one production packages
  comprise30 natives,nine assemblies andtwo selections. Next: re-inspect/map/
  restore178–180, preserving printed difference-only programs2–4, then assemble
  full172–180. Remaining bodies/pilots/headings and standalone issue closeout
  remain. No reading-room rebuild. Local compute/token monetary weight is zero;
  paid input ratio1:0.1,output rate/human effort unmeasured. Reporting/commit usage
  after the audit cutoff carries into the next audit.


### August medical-insurance ending178–180 restored, 2026-10-13

- Restored ending178–180 of 의료보험수가계산, canonical0023/byline컴퓨텍,
  from five re-inspected pinned whole views177–181. Full172–180 extent proof from
  native30 is reused by exact hash. Three mapped pages/two outside-map lookups.
  Opening172–177 and ending178–180 now cover all source pages; separate assembly
  remains required, so the article is explicitly partial in production accounting.
- All34 regions retain26 ordered blocks,29 regional readings and five source
  images: four complete listing parts for programs2–4 and a terminal endmark.
  Three prose joins preserve 부/분,표/준 and명칭/을. Listing2's upper ending179
  precedes section3-3/listing3. Four caption associations include the shared label178.
- All17 original panels/eight changed final panels/three overlays were inspected;
  nine unchanged panels match original bytes. Two code pairs were merged and other
  cuts moved before OCR, preserving original/revised crops. All116 final boundary
  checks have zero glyph or non-text crossings. No preparation probes or failures.
- Ran15T/14Q original calls; all29 authoritative drafts read and selected without
  alternates, failures or retries. Corrected once against17 pinned source panels
  in three saved parts. No new OCR during correction/export. Q used17,074 input/
  3,776 output local tokens,20,850 total; recognition took
  52.221s Q/1.526s T.
  Worker/startup time remains separate; local monetary weight zero.
- Three complete-as-printed difference listings retain157 physical rows:114 numbered
  candidates,42 nonblank wraps and one layout blank. No full runnable replacements
  inferred. Twenty-six category DATA values retain explicit statement/value byte
  ranges and the printed KB=24/READ0..24 (25 iterations) discrepancy. Thirty-eight
  flags retain duplicate INPUT,179minusVAL, unclosed15040 quotes178/179 versus
  closed180, CTRL^C comments and period180, slash placement and0/O candidates.
  Quoted blank runs, source bytes/execution and full proofreading remain unverified.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-31/medical`.
  Index: `build/pdf-restoration/13-1984-08-adaptive-medical-source-index-31/source-index.json`.
  Independent coverage, source pixels/raw hashes, exact regional/review/flag/category/
  physical/logical ranges, canonical identity and byte-identical rebuild pass.
  All41 prior packages,native15–31 original/selected seals (417/204 files in31),
  and16,790 pilot files remain unchanged. No shared pipeline change.
- August remains20 complete articles,one partial medical,ten untouched bodies,six
  pending pilots,three classified/three unclassified headings and zero human accepted.
  Forty-two production packages comprise31 natives,nine assemblies andtwo selections.
  Next: separately assemble fullmedical172–180, then remaining bodies/pilots/headings
  and standalone issueJSON/assets closeout. No reading-room rebuild. Paid input
  ratio1:0.1; output rate/human effort unmeasured. Reporting/commit usage after
  the audit cutoff carries into the next audit.


### August full medical-insurance172–180 assembled, 2026-10-13

- Assembled full 의료보험수가계산172–180 from exact native30/31 packages.
  Canonical0023, byline컴퓨텍, business parent0021 and page172 are unchanged.
  All90 source regions retain74 ordered blocks,79 regional readings/review ranges,
  11 original images and85 source-linked uncertainty records. Five native prose
  joins remain intact; no cross-native prose or listing-row join was required.
- Four independent listings preserve391 physical rows:283 numbered candidates,
  103 nonblank wraps and five layout blanks. The first program is complete as
  printed; programs2–4 remain printed differences only. No runnable replacements
  are inferred. Both key tables retain12 rows/30 cells without invented headers;
  the flowchart retains seven nodes/ten edges beside its authoritative bitmap.
- The full source index preserves every native key and projects1,758 exact UTF-8
  ranges, including26 DATA value ranges, and1,461 source asset references. All26
  category values and the printed KB=24/25-read discrepancy remain explicit.
  Thirty inline examples/four Unicode candidates, all captions, terminal endmark,
  printed errors, quoted blank runs and source ambiguities are preserved.
- All345 original native files are copied byte-identically. Independent coverage,
  canonical identity, text/table/category/listing ranges and a byte-identical full
  rebuild pass. All42 prior production packages, native15–31 raw/selected seals
  and16,790 sealed pilot files remain unchanged. Human acceptance/full proofreading,
  original source encoding and historical execution remain unverified.
- Assembly initially stopped at the source-example guard. Separately committed
  adapter77f537a accepts explicitly unverified printed excerpts only in the opt-in
  source-reference mode; source ranges/scans remain checked and verification claims
  rejected. All132 PDF tests and42 prior-package preservation checks pass. Earlier
  recipes, rejected extra metadata field, unpromoted output and audit assumptions
  remain preserved. No new OCR, mapping or source rendering was required.
- Export: `build/pdf-restoration/13-1984-08-adaptive/medical`.
  Source index: `build/pdf-restoration/13-1984-08-adaptive-medical-source-index/source-index.json`.
  Evidence: `private/pdf-restoration/13-1984-08-adaptive/medical-assembly-validation.json`.
- August now has21 complete assistant restorations,zero partials,ten untouched
  bodies,six pending pilot selections,three classified/three unclassified headings
  and zero human accepted. Forty-three production packages comprise31 natives,
  ten assemblies andtwo selections. Next: audit VISICALC 활용181 sealedpilot aug-05
  coverage/residuals, verify its complete source extent, then create a separately
  validated production revision and restore any uncovered pages. All remaining
  bodies/pilots/headings and whole-issue JSON/assets closeout remain required.
  No reading-room rebuild. Local compute/token monetary weight zero; paid input
  ratio1:0.1,output rate/human effort unmeasured. Reporting/commit usage after the
  audit cutoff carries into the next audit.


### August VISICALC181–185 pilot promoted, 2026-10-13

- Promoted full VISICALC 활용181–185 from sealed Tesseract pilot aug-05-v2-B
  into a separate production revision. Canonical0024/title/byline삼보컴퓨터교육부,
  business parent0021 and page181 are unchanged. Opening181, terminal endmark185
  and next 메아리186 establish full extent. Unrelated bookstore ad181 excluded.
- Rechecked all91 corrected text regions in18 source panels, five original images,
  six whole-page views and nine supplementary views. Both pilot arms, the original
  crop-defect/recovery evidence and failed Qwen attempt remain sealed. All91
  selected transcriptions and full article.txt bytes are unchanged; no new OCR,
  crop repair or routine paired correction. The sampled pilot comparison's eight
  Qwen wording/number errors and one punctuation omission informed selection;
  it is not an exhaustive error-rate or engine-level accuracy claim.
- JSON/assets retains96 regions,85 ordered blocks,91 exact regional/review ranges,
  five original images and25 source flags. Five retained joins preserve six native
  boundaries, including split VISICALC and the physically wrapped commission
  example. Three worksheet captions,34 inline examples,six definition ranges and
  40 Unicode candidates have exact indexes. No numbered program listings inferred.
- Four physical tables have ten companion chunks and124 indexed candidate rows,
  896 grid slots and435 blanks. One header is printed; nine repeated axis headers
  are editorial and explicitly identified. Pipes, repeated rule strings, formula
  grouping and glyphs remain editorial source-reading projections. Source images
  are authoritative; blank values are not filled by arithmetic. Display-only
  +1.1degree rotations clarify worksheet row tilt; exported crops remain unchanged.
- Printed Discont Rate, FORTH, QUANITY, FRIGHT, COMMISION and VISCALC remain literal.
  The prose cashflow table and worksheet reverse second-year100/70 values; both
  remain. Printed0.01 NPV argument versus10% claim, E11 SUM target, two /F$ colons,
  malformed commission formula/raisedprime and invoice77523/378.58/42.88 retained.
  Original source encoding, exact glyphs/spacing and historical execution unverified;
  human acceptance/full proofreading remain pending.
- Independent canonical/coverage/pixel/raw/settings/index/caption/table checks and
  byte-identical rebuild pass. All472 copied immutable evidence files,43 prior
  production packages,native15–31 raw/selected seals and16,790 pilot files remain
  unchanged. Original pilot metadata/review notes are retained in the revision.
  No shared pipeline change; unchanged132-test PDF baseline reused.
- Export: `build/pdf-restoration/13-1984-08-adaptive/visicalc`.
  Source index: `build/pdf-restoration/13-1984-08-adaptive-visicalc-source-index/source-index.json`.
  Evidence: `private/pdf-restoration/13-1984-08-adaptive/pilot-aug-05/validation.json`.
- August now has22 complete assistant restorations,zero partials,ten untouched
  bodies,five pending pilot selections,three classified/three unclassified headings
  and zero human accepted. Forty-four production packages comprise31 natives,
  ten assemblies andthree selections. Next native32: verify 메아리186 source extent,
  then restore its disassembler prose/examples/machine-code checksum table. All
  remaining bodies/pilots/headings and standalone issue JSON/assets closeout remain.
  No reading-room rebuild. Local compute/token monetary weight zero; paid input
  ratio1:0.1,output rate/human effort unmeasured. Old pilot recognition/correction
  costs are not counted again. Reporting/commit after cutoff carries into next audit.


### August 메아리186–188 raw checkpoint validated, 2026-10-13

- Verified canonical0041 **메아리** occupies186–194, with three contributions:
  SPC-1000용 디스어셈블러186–188, 1차 방정식189–193, and 키보드판 길 잃은
  고양이194. Twelve whole pages186–197 were individually inspected. The first
  prose endmark186 does not terminate continued machine-code panels187–188.
  Page194's lower advertisement, the separate technical divider195 and PIA196–197
  are excluded. Canonical title/null byline/parent0036 remain intact; contribution
  bylines are source content. Nine outside-map lookups are recorded for native32.
- Fresh4000-pixel renders186–188 support41 regions:35 text crops and six images,
  including five whole dump panels and the prose endmark. Seventeen coherent
  searchable dump chunks cover276 printed address/byte/checksum rows; four other
  regions contain unnumbered assembly/monitor examples. Original images remain
  authoritative; source bytes and historical execution are unverified.
- Inspected17 original panels and six revised panels. Seven crop boundaries were
  adjusted; the first dump's two10-row crops were merged into one20-row crop
  because source tilt overlaps their rectangular vertical bounds. All original
  maps/crops/diagnostics remain. Every final crop matches native pixels and all140
  text boundaries pass with zero glyph or non-text crossings. All crop repairs preceded inference.
- Completed14Tesseract and21Qwen original calls without failed recognition,
  empty drafts,retries or preparation probes. All35 authoritative drafts were read.
  All276 addressed rows retain eight value slots and their printed checksum slot.
  Eight Tprose crops lost embedded addresses/commands/choice identifiers; one
  unchanged-crop Qalternate each recovers those fields. All eight alternate drafts
  were read and selected, preserving every original Tdraft. Selected6T/29Q
  readings await source correction. Actual calls14T/29Q, all counted once.
  Q still reads생각 for source생략 in186r15; ordinary wording and sparse hexO/0,
  B/8 candidates require source correction. Do not derive bytes from arithmetic,
  checksum or address continuity. No source text has yet been corrected.
- Local Qwen usage: 18,514 input + 9,094 output
  = 27,608 tokens. Q recognition took
  286.570s; Tesseract took
  3.340s. Worker startup/elapsed and
  preparation/review/reporting windows remain separate. Local monetary weight0,
  paid uncached:cached input ratio1:0.1; output rate and human active effort unknown.
- Original/selected raw bundle/runtime/source/crop audits and immutable seals pass.
  Seals preserve495 original and369 selected/alternate files. All44 existing
  production packages, native15–31 original/selected seals and16,790 pilot files
  remain unchanged. Evidence:
  `private/pdf-restoration/13-1984-08-adaptive/batch-32/selected-raw-audit.json`.
- This is a raw milestone: source correction, export and indexes are pending.
  August production remains22 complete,zero partial,ten untouched bodies,five
  pending pilot selections,three classified/three unclassified headings and zero
  human accepted. Next: correct/export186–188, restore189–194, then assemble the
  full department. All other bodies,pilots,headings and standalone issue JSON/assets
  closeout remain required. No reading-room rebuild.


### August 메아리 disassembler186–188 restored, 2026-10-13

- Restored 메아리 first contribution SPC-1000용 디스어셈블러186–188 from
  the saved selected29Q/6T readings, corrected once against source. Canonical0041
  title/null byline/parent0036 remain unchanged; 이정우 is contribution content.
  Full department186–194 extent proof and nine outside-map lookups reused by hash.
  Second/third contributions189–194 and separate full assembly remain required.
- Forty-one regions retain34 ordered text blocks,35 exact regional/review ranges
  and six original images: five dump panels and the prose endmark. One column
  join preserves 된다.먼저; four prose continuations remain interrupted by their
  printed displays. Left dump panel/chunks precede right panel/chunks on187/188.
- Seventeen dump chunks preserve276 data rows and one ADRS/+0..+7/SUM header.
  Exact article/listing ranges retain2,760 candidate data cells and ten header cells,
  original colons/spaces and panel/row associations. Four assembly/monitor displays
  add11 physical rows:288 total unnumbered listing rows in five source groups.
  No numbered program or runnable loader inferred; source images authoritative.
- Forty source flags and12 indexed examples preserve A262H versus AA8EH, CR1/CRI,
  A2AB/A2A8, D8/DB, BE/FE, 68/6B, 88/BB and other dot-font0/O,B/8 candidates.
  Printed A262H is not repaired from dump extent; checksum E9 is read from source,
  not calculated. Raw 생각 is corrected to visible 생략. Historical 키이/체크섬
  and printed command/prompt punctuation retained. Full proofreading, original
  encoded bytes, execution and human acceptance remain unverified.
- All29Q/14T actual calls (21originalQ/eight boundedQ alternates/14originalT)
  remain counted once; selected6T/29Q corrected once. No new OCR during correction,
  metadata finalization, export or validation. Local Q tokens18,514input/9,094output,
  27,608total; recognition286.570sQ/3.340sT. Local monetary weight zero; worker,
  selection and assistant wall-time windows remain separate noncausal diagnostics.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-32/echo`.
  Index: `build/pdf-restoration/13-1984-08-adaptive-echo-source-index-32/source-index.json`.
  Independent coverage, exact row/cell/listing/text/review ranges, original crop
  pixels/raw settings, canonical identity and byte-identical rebuild pass.
  All44 prior production packages,native15–32 original/selected seals and16,790
  pilot files remain unchanged; native32 retains495original/369selected files.
  No shared pipeline change; unchanged132-test PDF baseline reused.
- August now has22 complete assistant restorations,one partial 메아리,nine untouched
  bodies,five pending pilot selections,three classified/three unclassified headings
  and zero human accepted. Forty-five packages comprise32 natives,ten assemblies
  and three production selections. Native33 next:189–194, then full186–194 assembly.
  Other bodies,pilots,headings and standalone issueJSON/assets closeout remain.
  No reading-room rebuild. Paid input ratio1:0.1; output rate/human effort unknown.
  correction32 includes the intervening status/continuation handoff; elapsed window
  time is not active human effort. Reporting/commit after cutoff carries forward.


### August 메아리189–194 raw checkpoint validated, 2026-10-13

- Prepared remaining 메아리 contributions 1차 방정식189–193 and 키보드판 길
  잃은 고양이194. Seven pinned wholeviews189–195 were individually reinspected;
  exact full186–194 extent evidence from native32 reused. Earlier186–188 production
  export5071990 remains unchanged. One outside-map lookup195. Lower194book ad and
  separate195technical divider excluded; canonical0041/title/nullbyline/parent intact.
- Six fresh4000-pixel renders support51 regions:42 text and nine source images,
  comprising five BASIC page panels, one patch, one key table and two endmarks.
  Seventeen program chunks cover272 printed BASIC rows; the patch retains eight
  labels including3105 and physical address wraps. Table has four key/direction pairs.
  The prose endmark189 does not terminate the continued program through1933710RETURN.
- Reviewed all32 original panels,13 revised panels and both final header crops.
  Twenty-one distinct regions adjusted before inference; two header cuts adjusted
  a second time to exclude decorative rules. One tilted16-row pair190 merged into
  a32-row chunk. All51 crop pixels and168 final text edges pass with zero crossings.
  Two bootstrap/schema preparation failures and one raw-audit template failure are
  preserved with original/unpromoted crops/scripts. No inference restarted for recovery.
- Original21T/21Q calls completed without recognition failures,retries,empty drafts
  or probes. All42 authoritative drafts read. T189prose/194byline lose words/name;
  Q192r04 drops2790/2810 labels and shifts their strings; Q194table omits movement
  column. One alternate each: threeQprose/byline readings selected, two corruptT
  code/table alternates unselected. All five read and retained. Selected18T/24Q;
  actual23T/24Q counted once. Q189alternate introduces SPC-100 versus visible
  SPC-1000; source correction must retain this raw regression and restore the zero.
  Ordinary artificial tabs/wraps, openquotes, U8/U9 and patch -16/368 need source
  correction; no repeatedQ or whole-article dual correction performed.
- Local Q usage30,820input/4,735output,
  35,555total; recognition199.021sQ/
  6.143sT. Worker216.333s,
  alternate/selection durations remain separate noncausal diagnostics. Local compute
  and model tokens have monetary weight0; paid input ratio1:0.1, output rate and
  human active effort unmeasured. Recovery/preparation/review costs remain visible.
- Original/selected audits pass and seals retain713 original/356 selected and
  alternate files. All45 prior production packages,native15–32 raw/selected seals
  and16,790 pilot files unchanged. Evidence:
  `private/pdf-restoration/13-1984-08-adaptive/batch-33/selected-raw-audit.json`.
- Raw checkpoint only: once-only source correction, indexes and189–194 export
  pending, followed by full186–194 assembly. August production remains22 complete,
  one partial,nine untouched bodies,five pending pilots,three classified/three
  unclassified headings and zero human accepted;45 packages unchanged. All other
  bodies,pilots,headings and standalone issueJSON/assets closeout remain required.
  Full proofreading/source bytes/execution unverified. No reading-room rebuild.


### August 메아리 ending189–194 restored, 2026-10-13

- Restored remaining 메아리 contributions 1차 방정식189–193 and 키보드판 길
  잃은 고양이194 from selected24Q/18T drafts, compared once with all42 source
  text crops and nine original images. Canonical0041/title/nullbyline/parent0036
  unchanged; 백성아/강남구도곡동 and 구평모/면목중 remain contribution content.
  Full186–194 extent proof reused; lower194book ad and195technical divider excluded.
- Fifty-one regions retain40 ordered text blocks,42 exact regional/review ranges,
  five BASIC page panels,one patch,one key table and two endmarks. Two native prose
  joins preserve 많은 신경 and 만들어 보기. The189 prose endmark does not terminate
  the program, which continues through1933710RETURN. Full186–194 assembly remains.
- Seventeen program chunks preserve272 printed numbered/physical rows1000–3710.
  Restore source blank2780/2800PRINT and2790/2810label/string associations, omitted
  2950expression and3420semicolon. Artificial quoted newlines/tabs removed against
  source physical rows. Initial visual2410candidate rejected against full190panel;
  original2510 retained, with reconciliation saved before finalization.
- Patch retains eight printed labels1170/1190/3040/3105/3110/3120/3130/3140 in14
  physical rows,including1170quoted wrap and four -16/368 address wraps. Combined
  listing286physical rows/280numbered logical entries/two independent groups.
  Key table preserves one header/four data rows,ten cells total:eight data/two
  header,zero blanks; A→up,Z→down,right→right,left→left represented as explicit
  Unicode source candidates beside original bitmap,with exact row/cell ranges.
- Thirty-three source flags/eight indexed examples preserve open quotes,U9/U8,
  USE T TERMINATE,PRINT/quote adjacency,0/O,final2030INTERCEP/T/quote uncertainty,
  quoted padding,physical wraps and historical 키이. Source SPC-1000 finalzero
  restored while the raw selected alternate SPC-100 regression remains immutable.
  Full proofreading,human acceptance,original encoded bytes and execution unverified.
- Actual24Q/23T calls (21Q/21T original plus threeQ/twoT bounded alternates) remain
  counted once; selected24Q/18T corrected once. No new OCR during correction/export.
  Q local30,820input/4,735output/35,555total; recognition199.021sQ/6.143sT.
  Preparation failures/two unselected corrupt alternates/audit recovery retained.
  Local compute/tokens monetaryweight0; paidinput1:0.1,output rate/human effort unknown.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-33/echo-ending`.
  Index: `build/pdf-restoration/13-1984-08-adaptive-echo-source-index-33/source-index.json`.
  Independent canonical/coverage,exact text/review/table/physical/logical row ranges,
  crop pixels/raw settings/stop outcomes and byte-identical rebuild pass. All45
  prior production packages,native15–33 original/selected seals and16,790pilot files
  remain unchanged; native33 retains713original/356selected/alternate files.
  No shared pipeline change; unchanged132-test PDF baseline reused.
- August remains22 complete assistant restorations/one partial 메아리/nine untouched
  bodies/five pending pilots/three classified and three unclassified headings/zero
  human accepted. Forty-six packages comprise33 natives/ten assemblies/three selections.
  All186–194 source pages now covered in two immutable segments; fulldepartment
  assembly is next. Other bodies,pilots,headings and standaloneissueJSON/assets
  closeout remain required. No reading-room rebuild. Goal remains active.


### August full 메아리186–194 assembled, 2026-10-13

- Assembled full 메아리186–194 from exact native32 disassembler186–188 and
  native33 equation/keyboard-cat189–194 exports after ending commitfa701cd.
  All341 native files are copied byte-identically,including original corrections
  and all source metadata. Three distinct contribution titles/bylines remain
  source content; canonical0041/title/nullbyline/parent0036/page186 unchanged.
  Only two segment-scope gaps are resolved; no cross-native prose or listing join.
- Full JSON/assets export retains92 regions,77 regional readings/review ranges,
  74 ordered text blocks and15 original images. Three native prose joins and four
  source continuations interrupted by displays remain. Program prose endmark189
  remains separate from program ending193; keyboard-cat194 retains terminal mark.
  Five dump panels/five BASIC panels/patch/keytable/three endmarks preserved.
- Seven independent listing groups retain574 physical rows:288 unnumbered
  examples/dump rows,280 numbered rows and six wraps. Equation program272numbered
  rows1000–3710 and patch eightlabels/14physicalrows remain literal. Listing bytes
  exactly equal native concatenation; printed openquotes,U9/U8,3105 and -16/368
  wraps retained without executable joining,arithmetic/checksum or syntax repair.
- Full source index projects277 dump rows and2,770 cells into combinedarticle
  andlisting:276data rows/2,760datacells plus oneheader/tenheadercells. Exact figure,
  region,row andphysical-line associations remain. Key table preserves four data
  rows/eightdata cells,oneheader/twoheadercells,zero blanks and Unicode arrow
  reading candidates. All77 regional ranges,20 inline examples and73 sourceflags
  project exactly; original native metadata remains unchanged and inspectable.
- Independent fullcoverage/canonical/range/physical-logical partition checks and
  byte-identical full rebuild pass. All46 prior production packages,native15–33
  raw/selected seals and16,790pilot files remain unchanged. No new OCR,mapping,
  rasterization or sharedpipeline work during assembly; native recognition costs
  remain counted once. Unchanged132-test PDF baseline reused. Localcompute/tokens
  monetaryweight0; paidinput1:0.1,output rate and activehuman effort unknown.
- Export: `build/pdf-restoration/13-1984-08-adaptive/echo`.
  Source index: `build/pdf-restoration/13-1984-08-adaptive-echo-source-index/source-index.json`.
  Evidence: `private/pdf-restoration/13-1984-08-adaptive/echo-assembly-validation.json`.
  August now has23 complete assistant restorations,zero partials,nine untouched
  bodies,five pending pilots,three classified/three unclassified headings and
  zero human accepted. Forty-seven packages comprise33natives/11assemblies/three
  production selections. Next verify PIAseries2 sourceextent from196 and promote
  sealedaug-06 into a separate production revision;200 is only a boundary hint.
  Remaining bodies,pilots,headings and standaloneissueJSON/assetscloseout required.
  Full proofreading/sourceencodedbytes/execution remain unverified. No reading-room
  rebuild. Goal remains active.


### August PIA196–199 pilot promoted and two groups classified, 2026-10-13

- Promoted full PIA 시리즈2 미니네온사인의 제작196–199 into a separate
  mixed production revision from sealed aug-06-A Tesseract/aug-06-B Qwen pilots.
  Canonical0026/title/byline편집부/technical parent0025/page196 unchanged.
  Actual195–200 wholeviews verify opening196, three complete programs/references/
  terminal mark199 and distinct SPC-1000 article200. Lower197music-card kit ad,
  lower198design-school ad/photo and195divider excluded from the article body.
- All15 contact panels/63 original crops reviewed:56 selected text readings and
  seven source images.49 Tesseract prose/title/caption regions plus seven Qwen
  table/code/reference regions retain their original corrected transcriptions
  exactly. Confirmed unselectedQ p196r11거처 avoided using source-correctT거쳐.
  Both complete original correction histories, review notes and runtime
  fingerprints remain in production metadata. No new OCR, crop repair or routine
  wholearticle paired correction; original pilot recognition/correction costs
  remain counted once. Human acceptance/full proofreading pending.
- JSON/assets retains47 ordered blocks,56 exact regional/review ranges and seven
  original figures. Eight source prose joins preserve nine boundaries, including
  출력,3×6,2번째,다이오드,포트A and8개의. Eleven separate figure/table/program
  captions have source ranges; 그림2배선도 remains embedded in its source image.
  Two diagram records/ten node fields retain register boxes/LED arrangement;
  editorial A/B identifiers are separate from printed 주변기기 labels.
- Three independent complete BASIC groups retain40 physical rows/29 numbered
  logical entries/11 wraps:fig10 13physical/9labels,fig11 9/7,fig12 18/13.
  DATA digit splits25/4 and19/2, POKE address wraps -16/190 and -161/90, literal
  SOKDO prompts and program numbering remain unchanged without runnable joining,
  arithmetic, syntax repair, source-byte or execution certification.
- Three source tables retain10 candidate rows/52 exact cell slots/three merged
  blank followers. Two headers are printed; five bit groups cover7/6/5–3/2/1–0.
  C0C1/C0C3 control cells span both data columns; LED caption spans two rows.
  LED pattern10011010, circle/cross candidates and PA7–PA0 associations retained.
  Eight inline examples/two definitions/32 Unicode candidates and12 source flags
  retain NOT graphic approximations, printedpositive16192 versusnegative table/
  code addresses, 인용한 caption spelling, unmatched quotation and duplicate
  reference1/1. Original images remain authoritative for glyphs/spacing.
- Independent source/canonical/coverage/pixel/raw/settings/range/table/listing
  checks and byte-identical rebuild pass. All321 sealed copied evidence files,
  47 prior production packages,native15–33 raw/selected seals and16,790pilot files
  unchanged. Metadata preparation recovered from sparse original note logs;
  independent audit recovered from dictionary-Counter assertion. Both failures
  retained with zero repeated recognition.480 unpromoted export/rebuild files
  retain before-repair editorial diagram label metadata and remain separate.
  No shared pipeline change; unchanged132-test PDF baseline reused.
- Source195 divider also verifies canonical 테크니컬0025 and 공모입선작0031 as
  non-owning section headings with five technical/four contest children, no
  independent body. Canonical identities/pages/parents unchanged; 공모총평237
  remains canonical 정보모음 child0042. Source photograph/full divider retained
  in pinned classification evidence, without inventing an article package.
- Export: `build/pdf-restoration/13-1984-08-adaptive/pia`.
  Source index: `build/pdf-restoration/13-1984-08-adaptive-pia-source-index/source-index.json`.
  Evidence: `private/pdf-restoration/13-1984-08-adaptive/pilot-aug-06/validation.json`.
  August now has24 complete assistant restorations,zero partials,nine untouched
  bodies,four pending pilots,five classified/one unclassified heading and zero
  human accepted.48 packages comprise33natives/11assemblies/four selections.
  Next native34: verify SPC-1000 peripherals200 sourceextent before mapping;207
  is only a boundary hint. Printed200차경환 differs from canonical차정환; preserve
  both. Remaining bodies/pilots/정보모음 classification and standalonewholeissue
  JSON/assets closeout/requirementsaudit remain. No reading-room rebuild.
  Localcompute/tokens monetaryweight0; paidinput1:0.1,outputrate/activehuman effort
  unknown. Preparation window includes status/continuation gaps; elapsed time is
  not activehuman effort. Reporting/commit tail carries into the next audit.


### August SPC-1000 peripherals200–205 raw checkpoint validated, 2026-10-13

- Source extent for SPC-1000용 주변기기의 제작 is verified200–206 from ten
  individually inspected wholeviews199–208. Native34 covers200–205; ending206 and
  fullassembly remain required. Distinct207메타어셈블러 opens next article; no printed
  endmark detected206. Four outside-map lookups; left200MICRO-ROBOT ad excluded.
- Fresh4000-pixel renders support81 selected regions:69text/12original diagrams
  and table images. Twelve label/value companions and one address-bit example
  route Q; clear prose/titles/captions initially T. Canonical0027/title/차정환/parent0025
  retained. Displaytitle미니네온사인의제작 and printed차경환/EME연구실 recorded;
  enlarged source corrects historicalFME candidate without rewriting sealedPIA history.
- All41final crop panels/six final overlays inspected. Two pre-inference revisions
  preserve original84regions/42panels, merge three coherent prose splits and widen
  frames/edges; last shared202edge moved to blank native row658. All81crop pixels
  match native scans.276textedges have zero glyph crossings; five header-rule
  crossings explicitly classified nontext. Superseded original panels are preserved;
  no claim that all discarded panels were viewed. Zero OCR used for crop revisions.
- Original56T/13Q calls completed; all69drafts read. Damaged openingtitle/byline,
  Addressheading, CPU/address/port/bit associations receive one boundedQalternate
  each on13unchanged crops. All13read/selected; no failures,retries,empty drafts or
  probes. Selected43T/26Q from actual56T/26Q, countedonce. Original drafts retained.
  Q still regresses four번지 words to변수 and oneD5bit toD6; source correction pending.
- Tables retain raw scaffolds for4/16data rows,34pinpairs,eightoperationrows and
  threecontrolword groups; mergedconditions,active-lowbars,D3bitheader,EXT1labels,
  callout/circuit associations and printed technical contradictions need source
  correction/indexing. No semantic corrections or production export yet.
- LocalQ28,334input/4,809output/33,143total;
  recognition143.097sQ/26.949sT.
  Originalworker121.862s; fallback and selection durations
  remain separate diagnostics. Local compute/tokens monetaryweight0; paid input
  ratio1:0.1,outputrate/humanactiveeffort unmeasured. Preparation/review/recovery visible.
- Raw/selected audits pass; seals preserve987original/593selected/alternate
  files. All48prior production packages,native15–33raw/selected seals and16,790pilot
  files unchanged. Evidence:`private/pdf-restoration/13-1984-08-adaptive/batch-34/selected-raw-audit.json`.
- Production unchanged:24complete,zero partial,nine untouched bodies,four pending
  pilots,five classified/one unclassifiedheading and zerohumanaccepted. Next source
  correction/index/export200–205,206ending/fullassembly; remaining bodies/pilots/heading
  and standalonewholeissueJSON/assetscloseout required. No reading-room rebuild.


### August SPC-1000 peripherals opening200–205 restored, 2026-10-13

- Restored SPC-1000 peripherals opening200–205 from69 selected adaptive drafts,
  corrected once against source scans.81 regions retain61 ordered text blocks,
  twelve original images and69 exact regional/review ranges. Canonical0027/title/
  차정환/technical parent0025 remain unchanged; printed미니 네온사인의 제작 and
  차경환/EME연구실 remain source content. Seven prose joins preserve eight seams.
- Four tables preserve45 data rows/220 data cells,three header rows/16 header cells
  and seven merged blank followers. All34 external-bus pin/signal pairs,24 port-pin
  pairs,15 control-word states/eight bit positions, eight diagrams and their source
  labels are searchable with exact UTF-8 ranges. Twelve captions,18 literal examples,
  two definitions and31 flags retain original images as authoritative evidence.
- Restore sourceD3,D5 and four번지 readings from selectedQ regressions. Preserve
  printedMRIQ/SYS CLK/BUSAK,IPLK,4000~4FFF,9C00~DFFF,9000H~DFFFH,C003H,
  0~4/5addresses,34RESET andCS0/CS1/D6/D0 contradictions. Overbars/subscripts are
  editorial Unicode candidates; no hardware repair or source-byte certification.
- Actual56T/26Q calls and localQ28,334input/4,809output/33,143total remain counted
  once. Selected43T/26Q corrected once; no new OCR during correction/export. Local
  compute/tokens monetaryweight0; paidinput1:0.1,outputrate/humanactiveeffort unknown.
- Independent source/canonical/coverage/crop/raw/settings/range/table/circuit checks
  and byte-identical rebuild pass. A duplicate phrase initially attached one flag
  to an earlier joined region; fixed by its explicit regional position.592 files
  preserve both unpromoted exports and the before-fix metadata; all69 source readings
  unchanged. Audit-count assertions were reconciled to five total번지 occurrences
  (four repaired,one already correct); failed audit templates retained.987 original/
  593 selected evidence files,48 prior production packages,
  native15–34 seals and16,790 pilot files remain unchanged. Shared pipeline unchanged.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-34/spc-peripherals`.
  Source index: `build/pdf-restoration/13-1984-08-adaptive-spc-source-index-34/source-index.json`.
  Evidence: `private/pdf-restoration/13-1984-08-adaptive/batch-34/validation.json`.
  August now24 complete/one partial/eight untouched bodies/four pending pilots/
  five classified and one unclassified heading/zero human accepted.49 packages:
  34 natives/11 assemblies/four selections. Ending206 and full200–206 assembly are
  next; other bodies/pilots/heading and standaloneissueJSON/assets closeout remain.
  Human acceptance/full proofreading/source bytes/execution pending. No reading-room
  rebuild. Correction window includes earlier compaction/status/continuation gaps;
  elapsed is not active human effort. Reporting/commit tail enters the next audit.


### August SPC peripherals ending206 restored, 2026-10-13

- Restored SPC peripherals ending206 after immutable native34opening200–205.
  Fresh206wholeview/native render,all13crop panels/overlay and24regions inspected.
  Twenty selected source readings retain19 ordered blocks,four original images,
  twenty regional/review ranges andone column prose join. Full200–206 extent reused
  from ten pinned199–208 wholeviews; only206 freshly reinspected at this checkpoint.
- Two complete independent BASIC programs retain17 physical/numbered logical rows:
  eightlist1 rows10/15/20/25/30/35/40/45,ninelist2 rows10–90. Literal2↑A,missingTHEN
  in70IF andpossibleperiod after128 retained with source-linked glyph candidates.
  No program normalization or encoded-byte/execution certification.
- Figure8 retains40 componentpin/signal pairs,including35RESET versus printed205
  prose34RESET. Eight LEDpositions preservePA7–PA0,circle/circledcross states and
  binary00010101 example; original images authoritative. Seventeen literal examples,
 23 diagramlabel ranges and13flags retainC000/C001/C002/C003,0003/1003/2003aliases,
  5V,0~255/00..FF andprinted포트한/코볼 candidates without hardware or spelling repair.
- Initial4Q/16T plusseven boundedQalternates produce selected11Q/9T fromactual
  11Q/16T,all countedonce. LocalQ5,244input/1,182output/6,426total. Qalternate
  해당하나는데 regression correctedonce to source해당하는데; no correction/export OCR.
  Raw-audit nestedusage Counter failure retained andfixed by summing three scalar
  fields.231original/224selected evidence files remain sealed; no crop repairs,
  probes,recognition failures/retries or successfulQcrop reruns.
- Independent source/canonical/coverage,crop/raw/settings,text/review/program/pin/
  LEDranges andbyte-identical rebuild pass.49priorproductionpackages,native15–35
  seals and16,790pilot files unchanged. Sharedpipeline unchanged; JSON/assets only.
  Humanacceptance/fullproofreading/sourcebytes/execution pending. Localcompute/tokens
  monetaryweight0; paidinput1:0.1,outputrate/humanactiveeffort unknown.
- Export: `build/pdf-restoration/13-1984-08-adaptive-batch-35/spc-ending`.
  Index: `build/pdf-restoration/13-1984-08-adaptive-spc-source-index-35/source-index.json`.
  Evidence: `private/pdf-restoration/13-1984-08-adaptive/batch-35/validation.json`.
  August remains24complete/onepartial/eightuntouched/fourpendingpilots/fiveclassified
  andoneunclassifiedheading/zerohumanaccepted.50packages comprise35natives/
  11assemblies/fourselections. All200–206sourcepages now covered; separatefullassembly
  is next. Otherbodies/pilots/heading andstandaloneissueJSON/assetscloseout required.
  No reading-room rebuild. Reporting/commit/response tail carriesinto nextusageaudit.


### August full SPC peripherals200–206 assembled, 2026-10-13

- Assembled full SPC-1000용 주변기기의 제작200–206 from immutable native34
  opening200–205/native35ending206 after endingcommitc5c37c2. All389 native files
  copied byte-identically, including raw evidence, corrections and original source
  metadata. Canonical0027/title/차정환/parent0025/page200 unchanged; printed
  미니 네온사인의 제작/차경환/EME연구실 remain original article content.
- Full JSON/assets retains105regions,89 exact regional/review ranges,79 ordered
  textblocks and16images. Eight native prose joins/nine native boundaries remain;
  source205콘트롤 joins206포트에 directly across the explicit runningheader,
  pinout,labels andcaption. Private exact-pin adapter verifies their sourceownership
  andorder; ordinary figure/caption checks still apply. Negative source/order checks
  reject forged headings or reversed interruptions. Sharedpipeline unchanged.
- Combined sourceindex retains45 tabledata rows/220datacells,threeheader rows/
  16headercells andsevenmergedblankfollowers;34externalbuspins/40componentpins,
  24portpairs,15controlwordstates,eightLEDstates,ten diagrams/158labelranges,
  35inlineexamples,two definitions and44 sourceflags. Every global UTF-8 range
  matches its original native bytes,including joined rightregion andblankcells.
- Two complete independent BASIC groups preserve17physical/numberedlogicalrows
  (eight/nine). Listingbytes exactly equal native concatenation. Source2↑A,
  possibleperiodafter128,missingTHEN,printedaddress/pin/bit/count contradictions,
  MRIQ/SYS CLK/BUSAK,포트한 andeditorialbars/subscripts remain unaltered candidates.
  Fullproofreading/humanacceptance/sourceencodedbytes/historicalexecution unverified.
- Independent fullcoverage/canonical/ranges/assets andbyte-identical assembly
  rebuild pass; all50priorproductionpackages,native15–35raw/selectedseals and
  16,790pilotfiles unchanged. Independent sourceindex projector initially omitted
  namespacing bare region_id; failedvalidator retained andfixed without changing
  the assembled export or any source reading. No new OCR,mapping,rasterization,
  frontend/browser/reading-room work. Recognitioncosts remain countedonce;
  localcompute/tokens monetaryweight0,paidinput1:0.1,outputrate/humanactiveeffort unknown.
- Export: `build/pdf-restoration/13-1984-08-adaptive/spc-peripherals`.
  Index: `build/pdf-restoration/13-1984-08-adaptive-spc-source-index/source-index.json`.
  Evidence: `private/pdf-restoration/13-1984-08-adaptive/spc-assembly-validation.json`.
  August now25complete/zeropartial/eightuntouched/fourpendingpilots/fiveclassified
  andoneunclassifiedheading/zerohumanaccepted.51packages comprise35natives/
  12assemblies/fourselections. Next verify 메타어셈블러207 sourceextent;214is only
  a boundaryhint. Remaining articles/pilots/heading andstandalonewholeissueJSON/
  assetscloseout/requirementsaudit remain. No reading-roomrebuild. Reporting/commit
  tail carriesinto nextusageaudit. Goal remainsactive.


### August meta-assembler207–212 raw checkpoint validated, 2026-10-13

- Verified 메타어셈블러 extent207–213 from ten pinned206–215 wholeviews.
  Native36 covers207–212; ending213 and separate fullassembly remain required.
  Canonical0028/title/한상기/parent0025 retained; printed한상기/한국과학기술원
  anddisplaytitle메타어셈블러 preserved. Left207KoreaSCADA recruitment ad excluded.
- Six4000-pixel renders support108regions:98text and10original images, nine
  numberedfigures andoneuncaptioned16-bit diagram. Diagram/formula/field scopes
  initially25Q; prose/titles/captions73T. Figure9 is a17-row input-data template,
  not a complete program. Formula subscripts, bitpositions and blank headercells
  need source-linked correction/indexes; sourcebitmaps remain authoritative.
- All47original panels/sixoverlays and33revised panels/finaloverlays inspected.
  Forty-four distinct regions revised before inference; finalfigure6/caption
  boundaries repaired andthree crop floor/ceil rounding differences recovered.
  All108final crops match nativepixels;392textedges have zero glyphcrossings and
  seven classified nontext intersections. Original/revised/rounded crops retained.
  Schema/dependency/rounding preparation failures used zero OCR. Figure6/7 preserve
  captions within complete bitmaps andalso have separate captionreading records.
- All98original drafts read; fifteen T identifier/value failures receive one
  boundedQalternate each on unchanged crops. All15read/selected; actual73T/40Q,
  selected58T/40Q, countedonce. No recognitionfailures/retries/emptydrafts/probes.
  SelectedQ 끌격/명명어/목적으로/리스트инг regressions retained for once-only source
  correction. Ordinary prose spacing/wrapping and successfulQdrafts not rerun.
- LocalQ19,672input/2,941output/22,613total;
  recognition87.120sQ/33.249sT.
  Worker96.211s; alternate/selection andpreparation/
  evaluation/reporting durations separate noncausal diagnostics. Localcompute/tokens
  monetaryweight0; paidinputratio1:0.1,outputrate/humanactiveeffort unknown.
- Raw/selected audits pass; seals preserve1139original/797selected/
  alternatefiles. All51priorproductionpackages,native15–35seals and16,790pilotfiles
  unchanged. Evidence:`private/pdf-restoration/13-1984-08-adaptive/batch-36/selected-raw-audit.json`.
- Raw checkpoint only: correction/index/export207–212 pending, then213/fullassembly.
  Production remains25complete/zeropartial/eightuntouched/fourpendingpilots/five
  classified/oneunclassifiedheading/zerohumanaccepted;51packages unchanged.
  Remainingbodies/pilots/heading andstandaloneissueJSON/assetscloseout required.
  Fullproofreading/sourcebytes/execution unverified. No reading-room rebuild.


### August meta-assembler207–212 restored, 2026-10-13

- Restored 메타어셈블러 opening207–212 after raw checkpoint8b12edc.
  All98selected source readings correctedonce;108regions retain92orderedblocks,
  tenoriginalimages and98regional/reviewranges. Fiveprosejoins/sixboundaries
  preserve listcontinuations andsource적→응/어셈블→러이지/마이크→로 acrossheaders.
  Canonical0028/title/한상기/parent0025/page207 unchanged; printedbyline retained.
- Nine numberedfigures andoneuncaptioned16-bit diagram retain81labelranges,
  sevenclassificationedges,16bit/fieldpositions,ninedefinitions and28literalexamples.
  Headerexamplefigure8 retains3rows/9cells,sevenvalues/twoemptythirdcells.
  Figure6/7 completebitmaps includeincidentalcaptions withseparatecaptionrecords.
- Figure9 retains17schematictranscriptionrows/fourverticalthree-dotstacks,
  unnumbered andnot acomplete runnableprogram. Thirdheaderperiod retained as
  header./header candidate. Formula superscripts/subscripts, widthi/widthsubscripts,
  uppercaseM/lowercasem, VAX/11-780 versusVAX-11/780 and7/8 versus6/2/2 examples
  remain source-linked candidates. Enlarged211reading retains추어진 with주어진
  alternative; earlier sealed주어진 inspection remains an explicit historicalerratum.
- SelectedQ끌격/명명어/목적으로/리스트инг anddiagram적용형 correctedonce fromsource.
  Actual73T/40Q (25originalQ plus15boundedalternates) countedonce; selected58T/40Q.
  LocalQ19,672input/2,941output/22,613total. No correction/export OCR or successfulQ
  rerun. Raw1139/selected797sealedfiles remain unchanged. Allattempts/crop/schema/
  dependency/rounding recoveries retained; elapsed includes status/compaction gaps.
- Independent source/canonical/coverage,crop/raw/settings,text/review/formula/table/
  diagram/listingranges andbyte-identicalrebuild pass. Two shortsourceflag excerpts
  initially anchored earlier repeatedwords; unique-tail phrases repaired before
  promotion, preserving priorunpromotedexport/rebuild andall98source readings.
  All51priorproductionpackages,native15–36seals and16,790pilotfiles unchanged.
  Sharedpipeline unchanged; JSON/assets only. Humanacceptance/fullproofreading/
  sourceencodedbytes/historicalexecution unverified;29explicit sourceflags retained.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-36/meta-assembler`.
  Index:`build/pdf-restoration/13-1984-08-adaptive-meta-source-index-36/source-index.json`.
  Evidence:`private/pdf-restoration/13-1984-08-adaptive/batch-36/validation.json`.
  August now25complete/onepartial/sevenuntouched/fourpendingpilots/fiveclassified/
  oneunclassifiedheading/zerohumanaccepted.52packages comprise36natives/
  12assemblies/fourselections;all17historicalrawmilestones unchanged. Nextrestore
  ending213,then separatelyassemblefull207–213. Remainingbodies/pilots/heading and
  standalonewholeissueJSON/assetscloseout/requirementsaudit remain required.
  No reading-room rebuild. Reporting/commit/response tail carriesinto nextusageaudit.


### August meta-assembler ending213 restored, 2026-10-13

- Restored 메타어셈블러 ending213 from22 selected readings, corrected once against
  all23 individual source crops.23regions retain21orderedblocks andone original
  terminalmark. One native column continuation preserves all13asterisk directives;
  three references retain literal numbers, names, dates and physical word wraps.
- Actual15T/13Q includes7originalQ andsixboundedidentifier/value alternates;
  selected9T/13Q. All239original/227selectedsealed files unchanged. Qtokens
  5,542input/1,026output/6,568total; zero recognitionfailures/retries/probes and
  zero correction/export OCR. Two crop edges revised before inference; final88
  textedges have zero glyphcrossings/one nontext runningheaderrule intersection.
  Preparation syntax/dependency failures retained with zero inference cost.
- Enlarged source prints AISM/GEN in conclusion; extra I retained literally,
  superseding earlier sealed OCR-defect rationale without rewriting raw history.
  Health/GENTRATING,1–80행,colon-dot-colon syntax, smeared운용되는 and physical
  C-/ROSS,MICROCO-/MPUTERS,Uni-/versal and45/-66 wraps retain ten source flags.
  No external bibliographic normalization. Fullproofreading/humanacceptance/
  sourceencodedbytes/historicalexecution remain unverified.
- Independent sourcepixels/raw/settings,canonical/coverage,text/review/directive/
  reference ranges and byte-identical rebuild pass. All52prior productionpackages,
  native15–37raw/selected seals and16,790pilot files unchanged. Sharedpipeline
  unchanged; JSON/assets only. Localcompute/tokens monetaryweight0,paidinput1:0.1;
  outputrate andhumanactive effort unknown; reportingtail carriesinto nextaudit.
- Export:`build/pdf-restoration/13-1984-08-adaptive-batch-37/meta-ending`.
  Index:`build/pdf-restoration/13-1984-08-adaptive-meta-source-index-37/source-index.json`.
  Evidence:`private/pdf-restoration/13-1984-08-adaptive/batch-37/validation.json`.
  August remains25complete/onepartial/sevenuntouched/fourpendingpilots/fiveclassified/
  oneunclassifiedheading/zerohumanaccepted.53packages comprise37natives/12assemblies/
  fourselections;17historicalraw milestones unchanged. All207–213source pages now
  restored; separate full207–213assembly remains required before articlecompletion.
  Remainingbodies/pilots/heading and standalonewholeissueJSON/assets closeout/
  requirementsaudit remain required. No reading-room rebuild; goal remainsactive.


### August full meta-assembler207–213 assembled, 2026-10-13

- Assembled full 메타어셈블러207–213 from immutable native36 opening207–212
  andnative37 ending213 after endingcommit53b1159. All508 originalnative files
  copiedexactly, including rawOCR/corrections/source metadata/images. Canonical0028/
  title/한상기/parent0025/page207 unchanged; printedbyline/displaytitle retained.
- FullJSON/assets retains131regions,120 exact regional/review ranges,113ordered
  textblocks and11originalimages. Sixnativeprosejoins/sevenboundaries unchanged.
  Source212ends inputtemplate/caption;213starts newoutputparagraph. No crossnative
  prose orlistingjoin needed. Allnative metadata remains unchanged in segments.
- Combinedsourceindex retains81diagramlabelranges/ten source diagrams,16bitpositions,
  sevenclassificationedges,13definitions/56inlineexamples and39source flags. Header
  example retains3rows/9cells/twoblanks. Figure9 retains17schematicrows/fourvertical
  dotstacks; native group metadata explicitly retains incomplete/nonrunnable status.
  All13asterisk directives andthree references retain global UTF-8 ranges with
  printedAISM/GEN/Health/GENTRATING,colon-dot-colon/행 andphysical word/range wraps.
- Independent fullcoverage/canonical/source ranges, copiednativefiles andbyte-identical
  fullrebuild pass;53priorproductionpackages,native15–37raw/selectedseals and16,790
  pilotfiles unchanged. Independent validator initially expected source_complete in
  standardized assemblygroup; failedvalidator retained, now checks originalnative
  metadata andretains fullsourcegroups in combinedindex. No export/source changes
  or newOCR/mapping/rasterization/sharedpipeline/frontend/browser/reading-room work.
- Fullproofreading/humanacceptance/sourceencodedbytes/historicalexecution remain
  unverified. Original bitmaps remain authoritative for faintglyphs/formula/subscripts/
  headerperiod/historicalerrors. Recognition costs countedonce; assembly/evaluation/
  reporting separate elapsed diagnostics. Localcompute/tokens monetaryweight0;
  paidinput1:0.1,outputrate/humanactiveeffort unknown; reportingtail nextaudit.
- Export:`build/pdf-restoration/13-1984-08-adaptive/meta-assembler`.
  Index:`build/pdf-restoration/13-1984-08-adaptive-meta-source-index/source-index.json`.
  Evidence:`private/pdf-restoration/13-1984-08-adaptive/meta-assembly-validation.json`.
  August now26complete/zeropartial/sevenuntouched/fourpendingpilots/fiveclassified/
  oneunclassifiedheading/zerohumanaccepted.54packages comprise37natives/13assemblies/
  fourselections;all17historicalrawmilestones unchanged. Next source-verify actual
  extent of 마이크로 컴퓨터 설계강좌221 before mapping. Remainingbodies/pilots/heading
  andstandalonewholeissueJSON/assetscloseout/requirementsaudit remain required.
  Goal remainsactive; no reading-room rebuild.
