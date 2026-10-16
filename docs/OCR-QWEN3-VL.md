# Qwen3-VL layout OCR

This opt-in local pipeline detects regions and reading order with Qwen3-VL,
then transcribes original-resolution crops. It produces unreviewed JSON, text,
figure crops, an overlay, raw requests/responses, runtime fingerprints and
resource measurements under `private/` or `build/`. It does not install article
packages or replace the existing pinned Tesseract restoration workflow.

## Run

Python dependencies are in `requirements.txt`. Use the already installed
`llama-server` from the same llama.cpp build as `llama-mtmd-cli`; no Python
Transformers runtime, remote inference or model download is used. By default the
CLI locates the single cached `Qwen3-VL-8B-Instruct-UD-Q4_K_XL.gguf` snapshot and
its `mmproj-BF16.gguf` under the standard Hugging Face cache.

```sh
python3 -m tools.ocr_qwen page \
  --image private/path/eligible-page.png \
  --output private/ocr-qwen3-vl/new-page

# A mapped article package: same 3000-pixel rendering, recorded orientation,
# boundary-safe exclusions and eligible-region mask as the current pipeline.
python3 -m tools.ocr_qwen page \
  --package private/path/package-plan.json --pdf-page 30 \
  --output private/ocr-qwen3-vl/new-pdf-page
```

All destinations must be fresh. Raster input is EXIF-oriented; `--rotation`
applies an additional clockwise right angle. Package input uses the package's
orientation and masks, and accepts no additional rotation. Standalone image
input uses the whole image: supply an eligible/masked image when scope matters.

Explicit local paths are supported:

```sh
python3 -m tools.ocr_qwen page \
  --server-binary ~/workspace/ai/llama.cpp/build/bin/llama-server \
  --model /path/Qwen3-VL-8B-Instruct-UD-Q4_K_XL.gguf \
  --mmproj /path/mmproj-BF16.gguf \
  --image private/path/page.png --output private/ocr-qwen3-vl/new-explicit-page
```

The owned server binds only to loopback, uses `--offline`, one slot, 99 GPU
layers, flash attention and an 8192-token context. Image encoding is capped at
4096 tokens; each transcription is capped at 4096 output tokens. The layout
request is capped at 3072 output tokens. Dense pages may need more context or
smaller regions: truncation, malformed JSON and invalid boxes fail visibly and
retain raw evidence. No silent retry, repair or acceptance of partial JSON.

OCR requests override the supplied interactive sampling preset with temperature
0, seed 42 and presence penalty 0, while retaining top-p .8, top-k 20 and min-p 0.
Greedy decoding reduces variation; disabling the presence penalty avoids
penalizing repeated printed code/text. This is not a comparison of sampling
presets. Reproducibility across builds/hardware is not guaranteed.

`--context`, `--image-tokens`, `--max-tokens`, `--gpu-layers`, and `--timeout`
are configurable. The model stays loaded across a benchmark. The server is
terminated when its owning command exits, including exceptions/interruptions.
`make ocr-qwen3-vl OCR_QWEN_ARGS='...'` wraps the page command.

## Outputs and limitations

`page/result.json` contains model-predicted region kind, normalized top-left
`bbox`, reading-order index, actual `crop_pixels`, text and asset name.
`bbox` is the original model prediction; text crops add 2% of page width and
0.5% of page height on each side, clamped to the image. Margins can admit
neighboring text, so inspect `layout-overlay.png` and crops. Figures retain the
predicted crop without padding. Tables use tabs/newlines; cell geometry and
figure-caption associations are not inferred or certified. Automatic boxes,
kinds and reading order need review, as does all transcription.

`layout.request.json` / `.response.json` and regional request/response pairs
retain prompts, image hashes, sampling settings, usage and native timings.
`manifest.json` pins page artifacts; `runtime/runtime.json` pins the executable,
GGUF and projector and records the launch command and load measurements.
`metrics.json` measures the running page pipeline. Failures retain
`failure.json` and any raw responses; they do not produce a completed result.
No model-generated confidence is presented as a calibrated accuracy estimate.

## Repeat the paired benchmark

The existing private OCR comparison contains three reviewed sample pages:
Korean prose with an inset, a photographed BASIC listing, and prose with diagrams
and captions. Adapt its pinned images and reviewed references once:

```sh
python3 -m tools.ocr_qwen prepare-trial \
  --output private/ocr-qwen3-vl/samples.json
python3 -m tools.ocr_qwen benchmark \
  --manifest private/ocr-qwen3-vl/samples.json \
  --output private/ocr-qwen3-vl/new-benchmark --repeats 2
make test-ocr-qwen3-vl
make test-pdf
```

`make benchmark-ocr-qwen3-vl OCR_QWEN_ARGS='...'` is equivalent. The current
pinned Tesseract runtime must already pass `verify_runtime()`; see
[PDF restoration](PDF-RESTORATION.md). Each page is run through:

1. Tesseract page mode: identical whole image, `kor+eng`, PSM 3, one thread.
2. Current Tesseract mapped-region mode: reviewed boxes, PSM 6, `eng` for code,
   `kor+eng` otherwise, one thread. Manual map creation cost is excluded.
3. Qwen: automatic layout plus regional transcription, no reference text or
   boxes in either prompt. The reference enters scoring only.

Inputs are the same pre-rendered 3000-pixel-long-edge PNGs. File/model hashes,
raw TSV/text, settings, all model responses, measured failures, per-run rows,
medians and peaks are retained. No historical cached timings are substituted.
Model load time is separate; rendering is excluded from all engine timings.
The first request has warm model weights, but there is no unreported inference
warm-up. Prompt reuse is disabled; OS file caches and GPU allocations remain warm.
The benchmark runs baselines first, then Qwen, sequentially. Two repeats reveal
only short-run variation, not confidence intervals or sustained throughput.

Resource measurements sample the Python process and children at a target 100 ms
interval, plus `nvidia-smi` overhead. CPU seconds and RSS are sampled estimates;
short-lived processes/peaks may be missed. RSS sums shared mappings and is not
physical-memory PSS. GPU memory is per matching process PID; unavailable/no
allocation is `null`, not zero. No energy, power, billing or human review time
is inferred from these measurements.

## Accuracy protocol

The reference is a prior scan-reviewed, assistant-corrected Tesseract draft,
subsequently crosschecked in the earlier trial. It is not an independent human
gold corpus. The three purposive pages are a diagnostic sample, not an archive
quality estimate. A reviewer familiar with the scans may favor the baseline's
segmentation or typography.

For prose/diagram pages, concatenate eligible reference regions in their recorded
order and predicted units in native engine order. Select predictions by geometry:
at least half their area overlaps one eligible reference box, or their center
lies in one. Do not reorder predictions using the reference. This excludes page
furniture but can include neighboring/diagram text from imprecise boxes. Report
Levenshtein CER with NFC/collapsed whitespace, CER with all whitespace removed,
and whitespace-token WER. Omission and ordering errors count; CER can exceed 100%.
Whitespace-free CER hides spacing/indentation errors and is never sufficient for
code acceptance.

For BASIC, deduplicate reference line numbers shared by overlapping crops.
Exclude entire reference lines containing unresolved `[BITMAP-*]`, `[BLANK-*]`
or `[ILLEGIBLE]` markers. Score the remaining numbered lines against the first
prediction with the same number, penalizing missing resolved lines. Report
missing/extra/duplicate numbers and exact resolved lines separately. This measures
known-line transcription, not whole-page order, unknown glyph recovery or correct
execution. Extra/uncertain lines are not folded into that CER.

A coarse layout diagnostic reports each reference's best predicted-box IoU and
counts IoU >= .5. Tesseract page units are lines; mapped units are supplied
regions; Qwen units are detected blocks. This is segmentation-sensitive and
**not a fair scalar layout ranking across those three granularities**. Inspect
the overlays alongside text/order errors. The photographed BASIC panel is a
reference figure containing code; a code detector need not classify it as a figure.

For additional images, provide a version-1 JSON manifest with a nonempty `samples`
array. Each sample has a unique filename-safe `id`, an `image` path (relative to
the manifest or absolute), its `sha256`, and ordered `reference` regions containing
`id`, `kind`, normalized `[x1,y1,x2,y2]` `bbox`, and `text`. Optional
`reference_source` pins the source annotation file. Keep transcriptions private.

## Runtime sources

- [Unsloth Qwen3-VL-8B-Instruct GGUF](https://huggingface.co/unsloth/Qwen3-VL-8B-Instruct-GGUF)
- [Installed llama.cpp API implementation at a8c9a4e7c](https://github.com/ggml-org/llama.cpp/blob/a8c9a4e7ccba890d6a2644a235492f836a7371c3/tools/server/server-common.cpp)

The installed parser requires the schema at
`response_format.json_schema.schema`. This was checked against source, since
its README's abbreviated `json_schema` example used a different shape.

## Measured comparison — 2026-10-09

Run: [sanitized measurements](ocr-experiments/ocr-qwen3-vl-benchmark.json); complete local evidence in
`private/ocr-qwen3-vl/benchmark-02/` (including its checked SHA-256 manifest).
All 18 runs completed successfully. Both repeats gave identical accuracy scores.

Hardware: Intel Core Ultra 9 275HX (24 logical CPUs), RTX 5080 Laptop GPU
(16,303 MiB), driver 595.99.02. Tesseract 5.5.0; llama.cpp build 11357
(`a8c9a4e7c`), cached Unsloth snapshot `b93a7ee713758252c555be4210c00540df954dc2`.

Lower error rates are better. CER includes collapsed whitespace; compact CER
removes all whitespace. BASIC rates apply only to 29 resolved numbered lines.

| Sample | Engine | Median seconds | CER | Compact CER | Peak RSS MiB | Peak GPU MiB |
|---|---|---:|---:|---:|---:|---:|
| Korean prose | Tesseract page | 4.90 | 27.57% | 4.99% | 253 | — |
| Korean prose | Tesseract mapped | 4.42 | 3.90% | 4.94% | 174 | — |
| Korean prose | Qwen automatic | 30.22 | 2.50% | 0.47% | 6355 | 8248 |
| BASIC | Tesseract page | 3.13 | 2.36% | 2.03% | 243 | — |
| BASIC | Tesseract mapped | 1.89 | 3.60% | 2.41% | 144 | — |
| BASIC | Qwen automatic | 24.91 | 1.13% | 1.27% | 6493 | 8248 |
| Diagrams + prose | Tesseract page | 2.81 | 38.36% | 10.06% | 241 | — |
| Diagrams + prose | Tesseract mapped | 2.69 | 6.08% | 7.39% | 158 | — |
| Diagrams + prose | Qwen automatic | 22.32 | 29.86% | 28.90% | 6512 | 8248 |

RSS/GPU columns are the maximum sampled across both repeats; GPU dash means no
matching allocation observed. Tesseract is CPU-only. The unusually high ordinary
CER for Tesseract page mode largely reflects Korean inter-character spacing: its
compact CER is much lower. Reporting both avoids hiding that difference.

Qwen was 6.8× slower than mapped Tesseract on prose, 13.2× on BASIC, and 8.3× on
the diagram page. Median sampled CPU seconds were 31.09 / 25.65 / 22.97 for Qwen
and 4.05 / 1.56 / 2.14 for mapped Tesseract, respectively. These are sampled CPU
usage totals, not CPU utilization percentages.

Qwen startup after runtime fingerprinting took 1.26 s with a warm OS file cache,
peaking at 5,367 MiB RSS and 7,562 MiB GPU allocation. This is not a cold-disk
launch measurement and excludes hashing/validation. Inference GPU allocation
reached 8,248 MiB (8.05 GiB). Process-tree RSS grew to 6,512 MiB over the six
page runs; this short run does not establish a long-running memory ceiling. The
GGUF is 4.795 GiB and projector 1.083 GiB (5.878 GiB combined). The pinned
Tesseract executable, two libraries and two language files total about 11.57 MiB,
excluding the rest of the system and downloaded package archives.

### What the scans show

- **Prose:** Qwen improved compact CER from 4.94% to 0.47% compared with mapped
  Tesseract. It detected three columns but merged the central inset with its
  surrounding column, so structural separation still needs review.
- **BASIC:** Qwen improved compact CER from 2.41% to 1.27%. It exactly matched
  27/29 resolved lines, versus 12/29 for mapped Tesseract and 17/29 for page
  Tesseract. All engines found all 70 line numbers; mapped Tesseract repeated
  line 860 because its source crops overlap. Forty-one unresolved glyph/blank
  lines were excluded from CER. No claim is made about their recovery or code
  executability.
- **Diagrams:** Qwen detected both figures (IoU >= .5), but omitted the entire
  middle prose column, split other paragraphs and clipped some figure labels.
  Its compact CER was 28.90%, versus 7.39% for mapped Tesseract. Matching a figure
  box by IoU does not guarantee a complete usable figure asset.

Visual checks used the retained original-resolution crops and overlays, including
`figures-qwen-1/layout-overlay.png`. This is an error diagnosis, not a completed
independent correction/review of all Qwen transcriptions.

**Decision:** retain mapped Tesseract as the default restoration pipeline. Use
Qwen as an opt-in draft/second reading for difficult prose or code, with explicit
layout and coverage review. This sample supports its recognition value but does
not support replacing reviewed region maps with its automatic layout output.

**User acceptance, 2026-10-14:** the maintainer accepted this conclusion as the
operating policy for future restoration. Mapped Tesseract remains the default;
Qwen assistance requires an explicit opt-in scope and layout/coverage review.
See the [current restoration guide](../PLAN-PDF.md#current-ocr-routing-guide).
The benchmark measurements and later trial results remain unchanged.

### Validation and preliminary attempts

Ten offline tests cover schema enforcement, truncation, raw evidence retention,
invalid geometry, failed runs, private destinations, file tampering, Unicode
scoring, native ordering, unresolved code lines and package exclusion masks.
The existing 117 PDF tests and 21 TOC tests also pass. No original restoration or source files
were modified. 
The retained `pilot/` and `benchmark-01/` runs are development evidence and are
excluded from the table. The first benchmark used the README-style schema
wrapper and correctly failed validation on four of six Qwen calls. The final
run uses the parser-compatible schema wrapper and a 4096-image-token cap rather
than the preliminary 2048-token cap. No failed runs were silently retried or
replaced in their original output directories.
