# June 1984 OCR decision report

> Historical experiment report/protocol. Measurements and original conclusions
> below are retained. For future restoration, follow the owner's 2026-10-14
> [OCR policy](../PLAN-OCR.md): mapped Tesseract by default, Qwen as explicit
> assistance with layout/coverage review. This report does not queue a new trial.


**Recommendation: use Qwen3-VL as the preferred raw-OCR option for the next issue, retain the existing semantic correction and mandatory human review, and keep Tesseract available for fallback and selective comparisons.** The June evidence supports better raw transcription, especially code. It does not yet establish lower total project cost.

Configuration: local Qwen3-VL-8B-Instruct UD-Q4_K_XL through llama.cpp, 8,192-token context and deterministic OCR decoding; Tesseract comparisons use pinned OEM1/PSM6, one thread, usually `eng` for code and `kor+eng` for prose. Settings and exact source crops remain pinned in each comparison.

This is a consolidation of existing evidence, not a new benchmark. No pipeline default or acceptance state was changed. The issue contains 38 assembled article bodies across 216 source pages; all 45 contents entries are accounted for, including seven group headings. Human acceptance is still zero.

## Accuracy: raw OCR against the assistant reference

Lower character error rate (CER) is better. The primary table removes whitespace; rates are weighted by reference character count, not averaged across crops.

| Content | Crops | Reference characters | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: | ---: | ---: |
| Prose | 42 | 5,656 | 0.30% | 9.25% |
| Code | 48 | 12,384 | 2.86% | 33.09% |
| Tables / other text | 7 | 1,052 | 4.94% | 25.57% |
| Combined, excluding index | 97 | 19,092 | 2.22% | 25.61% |
| All CER crops, including index | 100 | 19,333 | 3.78% | 27.05% |

The 97 non-index crops contain 423 Qwen character edits versus 4,890 Tesseract edits: **91.35% fewer reference edits in this selected sample**. Qwen has lower compact CER on 95 of these crops; Tesseract is better on two. Those exceptions are the code crop `p106r17` (65.27% vs 45.42%) and other-text crop `p181r19` (59.68% vs 54.84%). Both engines can fail badly on individual regions.

Whitespace-normalized CER, which retains word separators, is **2.27% vs 23.75%** across the same 97 crops. This also favors Qwen, but neither metric checks original literal spacing exactly.

| Separate diagnostic | Qwen | Tesseract | Scope |
| --- | ---: | ---: | --- |
| Correct table cells | 311/312 | 260/312 | Two phoneme tables; eight ambiguous cells excluded |
| Exact numbered source rows | 99/108 | 0/108 | Five assembly crops; spaces inside quoted literals retained |

The English-only Tesseract sensitivity run improves the table result to 265/312 cells; the primary comparison uses 260/312. These cell and row scores are not pooled with CER. This stricter code-row metric was not recorded for the other June comparison batches.

The three advertisement-index crops have primary compact CER **127.80% vs 141.08%** because the reference replaces decorative dotted leaders with table separators. A separately labeled, post-hoc calculation removes the same four punctuation characters from both engines and the reference: **0.41% vs 122.82%**. It leaves Tesseract's spurious letters/digits and omitted rows intact. CER can exceed 100% because insertions count. Both the original and supplemental scores are retained; the supplemental result is not substituted into the combined total.

**Limit:** these are 102 purposively selected, single-run crops: 97 ordinary CER crops, three index crops and two cell-scored tables. References were fixed before Tesseract, but were assistant-corrected Qwen drafts and are unblinded. They are not independent human gold. Failed graphic crops and many other regions are not scored. Do not read 2.22% as the whole issue’s error rate, or subtract it from 100% to claim final transcription accuracy. Layout maps were reviewed before OCR; this does not validate unattended layout detection.

## Time and resources

| Same 102 primary crops | Qwen | Tesseract |
| --- | ---: | ---: |
| Sum of engine-call time | 206.12 s | 28.75 s |
| Median per crop | 1.63 s | 0.24 s |
| Sampled peak process-tree RSS | 10,452 MiB | 119 MiB |
| Sampled GPU allocation | 7,858 MiB | CPU workflow; no sampled GPU allocation |

**Qwen was 7.17× slower at raw recognition on these crops.** Its possible workflow advantage is less correction work, not faster OCR calls. That downstream advantage remains unmeasured. Timing excludes shared mapping/rendering, Qwen startup and later correction; no whole-issue Tesseract runtime was measured.

| June Qwen work | Measured value |
| --- | ---: |
| Retained successful OCR calls | 2,811 |
| Their summed inference time | 50.40 minutes |
| Mean retained inference per source page | 14.00 seconds |
| Sum of recorded raw-run segments | 66.45 minutes; incomplete |
| Retained-stage peak GPU / process-tree RSS | 7,988 / 10,502 MiB |

The run-segment total is a lower bound on recorded raw execution work, **not total project elapsed time**. Early runs and several aborted passes lack complete timers. Some timers include recovery and others cover recovery only. It includes rendering/startup/export where recorded, but excludes layout preparation, semantic correction, assembly, and human review. Do not add inference time to this total: they overlap. Per-page means hide substantial differences in content and region count.

Early checkpoints labeled monitored stage time as inference time (batches02–06), and batch01 called it preparation time. This consolidation consistently sums underlying `inference.seconds`; per-batch JSON records both timers and the original label. Token counts and call counts reconcile with every checkpoint.

RSS includes shared mappings and is not a physical RAM requirement. Peaks are sampled and may miss brief spikes. GPU allocation is not energy use; electricity and monetary compute costs were not measured.

## Tokens and retry overhead

| June local Qwen token accounting | Tokens |
| --- | ---: |
| Retained prompt/image tokens | 1,323,619 |
| Retained generated tokens | 261,927 |
| Retained total | 1,585,546 |
| Additional failed/superseded response tokens | 169,924 |
| Separately logged interrupted request | 231 |
| Observed total including retries/interruption | **1,755,701** |

Observed overhead is **10.73%** above retained OCR. The audit finds 3,041 distinct completion IDs and excludes 661 copied cached responses. Real reruns remain counted even when they used the same crop. The separately interrupted request has no retained completion response. These totals exclude the earlier three-page pilot and do not estimate unlogged work.

Five archived failed responses hit the output limit, across the information tables, design article and rebellion game. Crop revisions also caused superseded work; two process interruptions were documented. A normal stop did not guarantee completeness: source review still found omissions. Three rebellion-game regions required manual transcription, with some graphic literals still represented by explicit placeholders. Failure counts therefore do not measure total OCR defect incidence.

**Local tokens are not paid assistant tokens.** Tesseract uses no LLM tokens for OCR, but its semantic-correction cost is unknown. No defensible paid-token saving, dollar saving, cost per accepted page, or human-time reduction can be calculated from these logs.

## Should local Qwen also do automatic correction?

The earlier three-page development pilot is separate from the June sample:

| Workflow | Preparation time | Local tokens |
| --- | ---: | ---: |
| A: Tesseract | 8.86 s | 0 |
| B: Qwen raw OCR | 49.39 s | 17,138 |
| C: A + B + local Qwen correction | 125.58 s | 46,059 |

Relative to B, C increased preparation time by 2.54× and local tokens by 2.69×. Compact prose CER improved from 0.79% to 0.53%, and text on the figure page from 0.57% to 0.32%, while scored BASIC worsened from 0% to 0.13% (29 exact lines became 28). BASIC scoring excluded 41 uncertain lines, so this is a limited development result. C includes A+B dependencies; these are total preparation figures, not incremental correction alone. All times exclude startup, shared image preparation and human/capable-model work.

**Do not add local self-correction as a mandatory pass yet.** Its extra work and occasional regressions have not shown a clear downstream benefit. Use selective trials on difficult regions while preserving the raw reading.

## Decision and next measurement

| Decision | Evidence / condition |
| --- | --- |
| Prefer Qwen for the next raw-OCR trial | Large, consistent sampled error reduction; local compute is feasible on the current machine |
| Retain semantic correction and mandatory human review | Printed code, continuations, omissions and graphic glyphs still need judgment |
| Keep Tesseract as fallback and selective diagnostic | Far lower raw runtime/RSS; occasionally a better reading; no need to run both over every page |
| Continue layout-map and cache reuse | Preserve prior work; record actual retries separately |
| Defer a claim of improved sustainability | Paid correction tokens and active review time are still unknown |

For the next comparison, preselect a small balanced set of fresh prose, code, tables and graphic-heavy pages. Prepare both raw drafts on identical reviewed crops, then assign **one draft per page** to the correction/review workflow, balanced across content types. Keep the other draft hidden until review finishes to reduce familiarity bias. Record actual capable-model input/cached/output tokens, active mapping/correction/review minutes, retries, omissions and explicit human acceptance. Compare total effort per accepted page and errors after correction. Set the desired saving before inspecting the results; June supplies useful raw-OCR evidence, not that final decision metric.

The aggregate evidence is strong enough to continue Qwen as a partial alternative now. The next experiment should spend its measurement effort on correction and review cost, rather than accumulating more favorable raw-CER examples.

## Reproduce and inspect

[Machine-readable consolidation](ocr-experiments/ocr-june-metrics.json) contains input hashes, weighted counts, per-batch tokens/times, failure evidence and explicit nulls for unmeasured costs. [Original progress](ocr-experiments/ocr-june-progress.json), [issue accounting](ocr-experiments/ocr-june-accounting.json), [earlier A/B/C pilot](ocr-experiments/ocr-workflow-measurements.json), and [reading-room review guide](READING-ROOM.md) remain separate.

From the repository root, with the private June evidence present:

```sh
PYTHONPATH=src:. python3 -m tools.ocr_qwen.consolidate
PYTHONPATH=src:. python3 -m unittest discover -s tests -p test_ocr_consolidate.py
```

The consolidator is read-only with respect to OCR evidence. It pools existing edit counts, validates unique source-crop identity, deduplicates only identical completion IDs, keeps retry work, and never converts a missing measurement to zero.
