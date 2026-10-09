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
