# Sustainable OCR workflow experiment

See [PLAN-OCR.md](../PLAN-OCR.md) for the objective and human-review requirements.
This experiment prepares three alternatives from **identical reviewed crops**:
A: Tesseract; B: independent Qwen transcription; C: local Qwen correction proposals
using the image and both drafts. The final semantic correction and human acceptance
stages remain necessary. This is preparation for measuring end-to-end savings;
its reference scores do not establish savings by themselves.

## Prepare and resume

Use the existing private three-page manifest created by `prepare-trial` in the
[Qwen OCR guide](OCR-QWEN3-VL.md):

```sh
python3 -m tools.ocr_qwen workflow \
  --manifest private/ocr-qwen3-vl/samples.json \
  --output private/ocr-qwen3-vl/new-workflow

# Same inputs, code, models and inference settings:
python3 -m tools.ocr_qwen workflow \
  --manifest private/ocr-qwen3-vl/samples.json \
  --output private/ocr-qwen3-vl/new-workflow --resume

# An interrupted stage has no completed checkpoint. Explicitly retain/archive
# that partial attempt and retry it, reusing all completed stages:
python3 -m tools.ocr_qwen workflow \
  --manifest private/ocr-qwen3-vl/samples.json \
  --output private/ocr-qwen3-vl/new-workflow --resume --retry-incomplete

make test-ocr-qwen3-vl
```

Runtime options match the `page`/`benchmark` commands. Reviewed geometry and kind
are supplied, but reference transcriptions and their uncertainty labels never
enter inference. Qwen's initial OCR sees neither Tesseract nor the reference.
The same Qwen model then checks the two drafts against the image; that second
pass is not independent adjudication and can introduce errors.

Each successful stage has a hash manifest, raw evidence, measured resources and
result. Resume checks input, implementation, runtime/model hashes and parameters;
it rejects stale/tampered evidence. Completed stages never rerun during an unchanged
resume. Configuration changes require a fresh run. Cross-configuration cache reuse
is not yet implemented. Incomplete attempts are retained under `failed-attempts/`
only when an explicit retry is requested. A fully cached resume starts no server. A nonblocking per-run file lock prevents
a surviving worker and a resumed command from writing concurrently; wait on the
original command session before resuming after an interruption.

Local correction returns a complete proposed transcription and at most eight
uncertainty strings, each at most 160 characters. These limits bound an observed
failure in which the model repeated explanations until exhausting its context.
Notes may be inaccurate or incomplete; their absence is not evidence of correctness.

## Review artifacts

Each run contains:

- `pages/<sample>/page.png` and exact region crops, including original figures.
- `<sample>-review.md`: full-page coverage context and every region with A/B/C
  drafts. Figures remain original assets. Agreement regions remain in the packet.
- `<sample>-differences.json`: exact Unicode-offset differences for A/B and B/C,
  with separate exact/whitespace-normalized/whitespace-free agreement indicators.
- `stages/<sample>/<region>/<arm>/`: immutable drafts, prompts, raw responses,
  Tesseract TSV, local token counts and sampled resources.
- `report.json`: preparation-stage costs, accuracy proxies and disagreement counts.
  C's stage cost is incremental; its end-to-end preparation requires A+B+C.
- `review-ledger.json`: editable human review record, initially pending for all
  three arms and all regions. Resume preserves it.
- `review-status.json`: derived status, with no invented human time or paid-model
  token measurements.

The same page is shown in all arms, so reviewer familiarity can affect timings.
The side-by-side packet supports practical inspection, not a blinded study. Record
review order/familiarity in notes and counterbalance order in a later timed trial.
Keep references separate from actual review work; copying existing reference answers
would not measure correction effort. BASIC evaluation excludes unresolved glyph
lines as documented in the original benchmark.

## Record actual review

Review full-page coverage, every eligible region and figure/caption boundaries.
Inspect agreements as well as disagreements. For an arm's page record, set an
identified `reviewer`, `reviewer_type: "human"`, `page_coverage_checked: true`,
and a disposition for every region:

- `accepted`: source checked and draft retained as final text.
- `corrected`: source checked and a corrected final text retained.
- `figure-reviewed`: a figure crop and its association checked.
- `unresolved`: reading remains unresolved; describe it in `notes`.
- `pending`: not reviewed.

For accepted/corrected text, save the actual final transcription in a file within
the run and put its relative path in `final_text`. Set page `accepted: true` only
when all regions have an accepted disposition and coverage has been checked.
This ledger's acceptance is conservative: an unresolved region keeps the page
pending rather than promoting it. The checker validates the recorded claim; it
cannot verify the identity of whoever edits a local JSON file. It does not install
anything into the archive.

Record `active_review_seconds` only when actually timed (exclude pauses), plus
`review_passes` and `escalations` when known. The optional `capable_model_usage`
object requires `input_tokens`, `cached_input_tokens`, `output_tokens`, and a
`source` describing the actual runtime/usage record and token counting convention.
Leave unavailable values null. Do not estimate paid tokens from character counts,
local model tokens or this conversation's length.

```sh
python3 -m tools.ocr_qwen review-summary \
  --ledger private/ocr-qwen3-vl/new-workflow/review-ledger.json
```

The checker rejects missing prepared page/arm/region records, automatic acceptance,
text regions disguised as figures, missing final text files, and invalid recorded
usage/time. Actual savings remain unmeasured until comparable review records exist.

## First mapped-crop trial — 2026-10-09

Private run: `private/ocr-qwen3-vl/workflow-03/`. Public, transcription-free
[measurements](ocr-workflow-measurements.json) were generated with:

```sh
python3 -m tools.ocr_workflow_report \
  --run private/ocr-qwen3-vl/workflow-03 \
  --output docs/new-workflow-measurements.json
```

All 20 text regions and three figure regions are represented. Sixty stages
completed: 20 Tesseract calls, 20 independent Qwen OCR calls and 20 local
correction calls. Every reference, source image, crop hash and completed stage
manifest was checked. An unchanged resume reused all 60 stages, performed zero
inference, and started no additional server.

One serial preparation run per arm, using the same hardware/model as the original
benchmark. Preparation seconds exclude startup, shared crop preparation and final
review. C includes the complete A+B+correction dependency cost. Compact CER removes
all whitespace; BASIC scores only the 29 resolved numbered lines.

| Sample | Arm | Preparation seconds | Compact CER | Local prompt + output tokens |
|---|---|---:|---:|---:|
| prose | A-tesseract | 4.04 | 4.94% | 0 |
| prose | B-qwen | 19.23 | 0.79% | 6,471 |
| prose | C-local-correction | 53.78 | 0.53% | 17,797 |
| basic | A-tesseract | 1.63 | 2.41% | 0 |
| basic | B-qwen | 17.50 | 0.00% | 5,894 |
| basic | C-local-correction | 42.07 | 0.13% | 15,733 |
| figures | A-tesseract | 3.19 | 7.39% | 0 |
| figures | B-qwen | 12.66 | 0.57% | 4,773 |
| figures | C-local-correction | 29.72 | 0.32% | 12,529 |

These are local llama.cpp tokens, not paid-model tokens. B requires only its own
recognition stage, while C needs both initial drafts and the correction pass.
Across the three pages, B used 17,138 local tokens; C used 46,059 including B.
Human review time, capable-model tokens and accepted-page savings remain null.

Using reviewed geometry removed the earlier automatic-layout omission on the
diagram page. Qwen draft compact CER there was 0.57%, versus 28.90% in the earlier
automatic-layout trial. This is a different pipeline configuration, not a repeat
measurement of the earlier automatic detector.

The correction pass improved reference edit distance in four regions and worsened
it in three. It appended an extra character to a previously reference-matching
BASIC line and changed a previously matching heading; some regressions had no
uncertainty note. Thus disagreement/uncertainty flags help organize review but
cannot certify or automatically accept any text. The prose reference remained
slightly better matched overall after correction; BASIC became slightly worse.

For now, **B is the simplest promising partial alternative**: use local Qwen on
established crops as the draft for the existing semantic/human correction work.
C remains an optional proposal source whose extra effort must earn its place in
a timed review. No arm has received human acceptance in this experiment.

### Ready for review

- [Prose packet](../private/ocr-qwen3-vl/workflow-03/prose-review.md)
- [BASIC packet](../private/ocr-qwen3-vl/workflow-03/basic-review.md)
- [Diagrams/prose packet](../private/ocr-qwen3-vl/workflow-03/figures-review.md)
- [Human review ledger](../private/ocr-qwen3-vl/workflow-03/review-ledger.json)

All three packets include the full page, crops and all A/B/C drafts. The next
checkpoint is actual review with recorded active time and available capable-model
usage; that checkpoint is deliberately not marked complete by these scores.

### Development attempts and verification

`workflow-01` retains a rejected, truncated correction response caused by looping
explanations. Its replacement schema bounds uncertainty notes. `workflow-02`
completed, but an attempted resume overlapped a surviving worker after an
interruption; its timings are excluded. A per-run OS file lock now prevents
concurrent writers. Only the fresh serial `workflow-03` supplies this table.
These development attempts consumed additional local compute not included in
steady preparation costs; they are not hidden as successful ordinary runs.

24 OCR/workflow tests pass, covering reference isolation, truncation, raw evidence,
cache tampering, concurrent-run exclusion, review coverage, explicit human
acceptance and cost dependency accounting. The prepared ledger reports zero
accepted pages. No historical scan/transcription/package was modified.

## June 1984 practical adoption

The maintainer authorized the whole June issue using arm B as the raw draft for
assistant scan-based semantic correction and mandatory human review. This trial
runs alongside the measurement experiment; no human acceptance is inferred.
The issue queue and ledger are under `private/pdf-restoration/12-1984-06-qwen/`.

For inspected restoration maps, use the mapped adapter:

```sh
PYTHONPATH=src python3 -m tools.ocr_qwen.mapped \
  --request private/pdf-restoration/12-1984-06-qwen/batch-01-corrected/request.json \
  --output private/pdf-restoration/12-1984-06-qwen/batch-01-corrected/ocr
# Add --resume only for unchanged inputs/settings/implementation.
```

A request contains `batch_id`, optional `scale_to` (1000–6000; default3000), and
`articles: [{"map": {"path": "private/.../map.json", "sha256": "...", "bytes": 123}}]`.
Paths are repository-relative. At most three mapped articles and twelve distinct
source pages are allowed. The adapter validates source/TOC pins, orientations and
exclusions, retains every crop and original figure, and transcribes text regions
without automatic layout or a local correction pass. Inspect crops for clipping
as well as full-page coverage before accepting results. An unchanged completed
resume reuses immutable stages without starting a server. An incomplete failed
stage is retained and requires a fresh output; this adapter currently has no
`--retry-incomplete` option.

Each article directory contains an existing-format `evidence-bundles.json` and
per-page `evidence.json`, raw text, settings and positions JSON. Positions are
explicitly **region-level only** and include the native response; Qwen has not
provided word boxes. Export recipes specify `runtime_directory` relative to the
repository and the pinned `runtime-fingerprint.json`. Recipes omitting that field
continue to use the original Tesseract runtime directory. Export still requires
explicit scan-linked correction outcomes for every region. Record human acceptance
separately from the legacy `sample-reviewed` assistant review status.

Rollback requires selecting the retained Tesseract path and generating fresh raw
OCR/evidence for the same reviewed maps; previous OCR, maps and corrections are
never overwritten. No public reader installation is part of raw OCR execution.
