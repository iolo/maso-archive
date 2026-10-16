# OCR workflow reference

Storage: [what to preserve and where new work belongs](STORAGE.md). Historical paths remain available through compatibility links.

The [OCR handoff](../PLAN-OCR.md) defines current policy: mapped Tesseract is the
default; Qwen is explicit assistance. The A/B/C workflow below is an optional
measurement experiment, not a required restoration pass. Its original nine
page/arm human review records remain pending. No new experiment is queued.
The public JSON measurements and checkpoint ledgers are indexed in
[OCR experiment data](ocr-experiments/README.md).

## Mapped Qwen assistance

For reviewed restoration maps, use the existing mapped adapter:

```sh
PYTHONPATH=.:src python3 -m tools.ocr_qwen.mapped \
  --request archive/pdf/YYYY-MM/restoration/batch-NN/request.json --output archive/pdf/YYYY-MM/restoration/batch-NN/new-qwen-ocr
# Add --resume only for unchanged inputs/settings/implementation.
```

A request contains `batch_id`, optional `scale_to` (1000–6000; default 3000),
and `articles: [{"map": {"path": "archive/evidence/.../map.json", "sha256": "...", "bytes": 123}}]`.
Paths are repository-relative. The adapter ceiling is three articles/twelve source
pages; use the tighter current restoration checkpoint limits when applicable.
It uses reviewed crops, not automatic layout or a local correction pass.

Inspect complete pages and crops for omissions/clipping. Output includes original
figures, native responses, raw text/settings and region-level positions; these
are not word boxes. Export requires explicit source-linked corrections. Recipes
record `runtime_directory` and `runtime-fingerprint.json`; never substitute an
engine's runtime provenance for another's.

An unchanged completed resume reuses stages without starting a server. A failed
incomplete stage remains preserved and needs a fresh output; this mapped adapter
has no `--retry-incomplete` option. That option belongs to the separate A/B/C
workflow below. Confirm the original process has stopped before resuming.

## Optional A/B/C review experiment

All three arms use identical reviewed crops: A is Tesseract, B is an independent
Qwen reading, C proposes local corrections from both drafts and the scan. Keep
references out of candidate prompts. C is not independent adjudication and can
regress a correct reading. Source inspection and human acceptance remain separate.

## Prepare and resume

Use the existing private three-page manifest created by `prepare-trial` in the
[Qwen OCR guide](OCR-QWEN3-VL.md):

```sh
python3 -m tools.ocr_qwen workflow \
  --manifest archive/experiments/ocr-qwen3-vl/samples.json \
  --output archive/experiments/ocr-qwen3-vl/new-workflow

# Same inputs, code, models and inference settings:
python3 -m tools.ocr_qwen workflow \
  --manifest archive/experiments/ocr-qwen3-vl/samples.json \
  --output archive/experiments/ocr-qwen3-vl/new-workflow --resume

# An interrupted stage has no completed checkpoint. Explicitly retain/archive
# that partial attempt and retry it, reusing all completed stages:
python3 -m tools.ocr_qwen workflow \
  --manifest archive/experiments/ocr-qwen3-vl/samples.json \
  --output archive/experiments/ocr-qwen3-vl/new-workflow --resume --retry-incomplete

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
  --ledger archive/experiments/ocr-qwen3-vl/new-workflow/review-ledger.json
```

The checker rejects missing prepared page/arm/region records, automatic acceptance,
text regions disguised as figures, missing final text files, and invalid recorded
usage/time. Actual savings remain unmeasured until comparable review records exist.

## Existing results and evidence

The serial run `archive/experiments/ocr-qwen3-vl/workflow-03/` completed 60 verified stages;
an unchanged resume made no new inference or server startup. Its source-linked
review packets and `review-ledger.json` remain available there. All nine human
page/arm records remain unaccepted.

[Measurements](ocr-experiments/ocr-workflow-measurements.json) retain the sample-level scores,
local resource costs, regressions and missing human/paid measurements.
[June's consolidation](OCR-JUNE-DECISION.md#should-local-qwen-also-do-automatic-correction)
explains why local self-correction is not mandatory.
The [full development/adoption log](history/OCR-WORKFLOW-2026-10-14.md)
preserves the first-run tables, failed attempts and subsequent issue checkpoints.
