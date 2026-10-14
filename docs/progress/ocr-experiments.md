# OCR experiment progress

[All issues](README.md) · [Current OCR handoff](../../PLAN-OCR.md)

This preserves the original PDF progress entries for the OCR benchmark and
A/B/C sustainability workflow. Consolidated findings and commands are in the
handoff; detailed experiment narratives are indexed in [history](../history/README.md).
These entries do not authorize restarting the experiments.

## Checkpoint records

### 2026-10-09 — opt-in Qwen3-VL OCR pipeline and paired benchmark

- Added `tools.ocr_qwen`: owned offline llama.cpp server, schema-constrained
  layout detection, original-resolution crop transcription, raw response/prompt
  retention, figure assets, overlay, source/runtime hashes and sampled CPU/RSS/GPU
  metrics. Package inputs reuse the existing orientation/exclusion rules.
  Outputs remain unreviewed and private; the Tesseract pipeline remains default.
- Reused the existing three-page private OCR comparison and its assistant-reviewed
  scan references. Fresh `benchmark-02/` contains two uncached repeats each of
  Tesseract PSM 3, mapped Tesseract PSM 6 and automatic Qwen (18 successful runs).
  All 433 artifact pins and unchanged source/reference/implementation hashes
  verified. Preliminary attempts are retained separately, with their failures.
- Qwen median page times: prose 30.22 s, BASIC 24.91 s, figures 22.32 s, versus
  mapped Tesseract 4.42 / 1.89 / 2.69 s. Peak sampled Qwen GPU memory 8,248 MiB;
  process-tree RSS 6,512 MiB. Warm-cache model startup 1.26 s, separately measured.
- Compact CER (all whitespace removed): Qwen .47% / 1.27% / 28.90%, mapped
  Tesseract 4.94% / 2.41% / 7.39%. BASIC measures 29 resolved numbered lines,
  excluding 41 unknown-glyph/blank lines, not full-page accuracy. Qwen omitted
  the diagram page's middle column and merged the prose inset. Automatic layout
  is not reliable enough to replace reviewed region maps on this evidence.
- `docs/OCR-QWEN3-VL.md` documents commands, methodology, limitations and measured
  results; `docs/ocr-qwen3-vl-benchmark.json` retains sanitized measurements.
  Original transcriptions, images and raw responses remain under ignored private
  directories. No historical restoration package or source was modified.
- Validation: 10 new OCR tests, 117 existing PDF tests and 21 TOC tests passed;
  compile check and `git diff --check` passed. Both inference repeats produced
  identical accuracy metrics. No bulk archive conversion or reader installation.

### 2026-10-09 — sustainability plan and local draft/correction arms

- Saved `PLAN-OCR.md` with the clarified objective: sustainable human-reviewed
  restoration, preserving useful semantic correction while reducing repeated
  work and capable-model token use. Qwen is a partial alternative, not a full
  pipeline replacement. Human acceptance remains mandatory.
- Added a resumable three-arm workflow on identical reviewed crops: A Tesseract,
  B independent Qwen OCR, C Qwen correction proposals using the scan and A/B
  drafts. Reference text is reserved for scoring. Scripts build complete review
  packets/differences and an explicit human ledger; no agreements auto-accept.
- Final serial trial `private/ocr-qwen3-vl/workflow-03/`: 20 text regions, three
  figure regions, 60 completed stages. All stage/raw response/crop/source/reference
  hashes verified. Unchanged resume reused all 60 stages with zero new inference
  and no additional server start. All nine page/arm reviews remain pending.
- B compact CER: prose .79%, BASIC 0% on 29 resolved lines, figures/prose .57%.
  C: .53%, .13%, .32%. Correction improved four regions but regressed three
  against the prior assistant-reviewed references; it is not always beneficial.
  B preparation consumed 17,138 local tokens; full C consumed 46,059 including
  both drafts. Human review time and capable-model tokens remain unmeasured.
- Preserved development attempts: `workflow-01` failed on looping explanation;
  uncertainty notes now have schema length/count limits. `workflow-02` overlapped
  an attempted resume after interruption; its timings are excluded. A tested
  per-run OS file lock prevents overlapping workers; final measurements use only
  fresh serial `workflow-03`.
- `docs/OCR-WORKFLOW.md` documents CLI, actual review recording, results and links
  to the three private review packets. `docs/ocr-workflow-measurements.json`
  contains only sanitized measurements. `tools.ocr_workflow_report` computes
  dependency-inclusive costs and region regressions without inventing savings.
- Validation: 24 OCR/workflow tests pass, including reference isolation, cache
  tampering, concurrent writers, explicit human acceptance, coverage preservation
  and correction-cost accounting. No prior restoration/source/package edits.


[Back to progress index](README.md)
