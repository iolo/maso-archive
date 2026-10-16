# August 1984 paired OCR cost results

> Historical experiment report/protocol. Measurements and original conclusions
> below are retained. For future restoration, follow the owner's 2026-10-14
> [OCR policy](../PLAN-OCR.md): mapped Tesseract by default, Qwen as explicit
> assistance with layout/coverage review. This report does not queue a new trial.


**Finding: this pilot does not show a convincing paid-cost advantage for either OCR route.** Qwen reduced cached input and output, but increased uncached input. Which route costs less depends on the applicable rates.

At the hypothetical rate ratio uncached:cached:output = 1:0.1:4, Qwen is **0.60% cheaper** across the eight matched corrections, wins four articles out of eight, and has a median article ratio of 1.005. Including the observed aborted correction makes its route **4.17% more expensive**. The abort arose from a shared crop defect, so that recovery result is an operational accounting fact, not proof that Qwen intrinsically causes more recovery.

If cached input is priced the same as uncached input, Qwen is about 11.3% cheaper in the displayed scenarios. If cached input is free, Tesseract is cheaper in all displayed scenarios. These are sensitivity calculations, not actual provider prices.

**Decision:** continue selective use of Qwen where its raw draft is useful. The current content-routing rule remains provisional; this trial establishes no general paid-token saving. A repeat should target a specific close decision after the actual rate vector is known; this pilot does not justify doubling the rest of August automatically.

**User review, 2026-10-12:** keep and improve adaptive routing. The user's tentative
interpretation is that complex layouts, structured material and source code benefit
more from Qwen, while the differences for simpler material are not practically
decisive. Use the user-supplied **10:1 uncached-to-cached input price ratio** as the
working cost assumption. The output price is still unspecified; the `1:0.1:4`
example below remains illustrative, not a confirmed complete billing rate.

The token-volume observation is supported by the two cited examples: Qwen used
9.1% fewer total correction tokens for VISICALC and 20.3% fewer for the editor.
However, with the illustrative output rate of 4, their weighted cost changes are
respectively −0.40% and +2.76%. Thus complexity is a useful routing hypothesis,
while uncached/cached/output usage must remain separate when evaluating savings.
For the whole matched cohort with `u=1,c=0.1`, Qwen is cheaper when the output
rate exceeds approximately `2.824` times the uncached-input rate, before recovery
or later repair costs. These observations do not validate a universal content rule.

Apply the [updated routing guidance](OCR-JULY-TRIAL.md#august-review-refinement-2026-10-12)
to future ordinary restoration: route coherent regions by draft usability, correct
the selected draft once, and collect weighted usage without routinely doubling
articles. This decision does not change the sealed pilot results or mark human
acceptance complete.

Eight articles (28 distinct pages) were restored independently through both routes: 16 verified exports. Local CPU/GPU/runtime and local model tokens have zero monetary weight. All human acceptance remains pending. No reading room was rebuilt.

This measures cost to reach independently source-checked, reviewable drafts. Residual errors differ, and a later human repair pass has not been priced. It does not establish equal-cost production of identically error-free text.

## Paid correction tokens

| Article | T uncached | Q uncached | T cached | Q cached | T output | Q output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 편집자 노트 | 36,080 | 32,005 | 346,240 | 390,656 | 4,513 | 4,228 |
| 죽음의 스키 | 48,875 | 64,062 | 750,336 | 693,504 | 8,177 | 7,538 |
| 공모총평 | 33,297 | 34,322 | 492,928 | 461,952 | 4,785 | 6,532 |
| 기초 테크닉 코너 | 78,521 | 103,249 | 1,546,496 | 1,194,240 | 11,931 | 8,614 |
| VISICALC 활용 | 101,602 | 113,749 | 994,048 | 882,048 | 10,666 | 10,183 |
| PIA 시리즈2 미니네온사인의 제작 | 67,797 | 73,471 | 753,280 | 739,072 | 8,948 | 8,513 |
| 베이직 코맨드 에디터 | 127,514 | 220,265 | 2,528,896 | 1,897,728 | 19,640 | 15,403 |
| Q&A | 94,089 | 89,871 | 1,124,352 | 1,098,368 | 12,619 | 11,303 |
| **Total** | **587,775** | **730,994** | **8,536,576** | **7,357,568** | **81,279** | **72,314** |

Counts come from deduplicated native response usage, with source-image/tool input included. All 16 independent sessions used the same inherited model and reasoning setting. Cache-write input was zero. Reasoning is included in output, never added again. No actual billing rates were supplied, so these are not dollar amounts or a claim about subscription charges.

## Price sensitivity

Use the same per-token rates for both routes: `C = u*uncached + c*cached + o*output`. The following rates are hypothetical ratios with `u=1`; they are not current model prices. A ratio below 1 favors Qwen. At `c=1`, all captured input is priced as uncached, a useful cache sensitivity check.

| Cached rate c | Output rate o | Q/T total cost | Median article Q/T | Median paired difference | Q cheaper articles |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1 | 1.2007 | 1.0883 | 8,451.5 | 2/8 |
| 0 | 4 | 1.1176 | 1.0808 | 9,114.0 | 2/8 |
| 0 | 8 | 1.0578 | 1.0300 | 5,238.5 | 3/8 |
| 0.1 | 1 | 1.0107 | 1.0016 | 272.8 | 3/8 |
| 0.1 | 4 | 0.9940 | 1.0050 | 869.9 | 4/8 |
| 0.1 | 8 | 0.9778 | 0.9909 | -2,415.2 | 5/8 |
| 1 | 1 | 0.8865 | 0.9473 | -36,901.0 | 7/8 |
| 1 | 4 | 0.8866 | 0.9524 | -39,833.5 | 7/8 |
| 1 | 8 | 0.8867 | 0.9575 | -43,743.5 | 7/8 |

Exact whole-cohort difference, Q minus T: `+143,219*u -1,179,008*c -8,965*o`. Qwen is cheaper when this expression is negative. Per-article vectors, differences and scenario ratios are in [the machine-readable results](ocr-experiments/ocr-august-pilot-results.json).

The 16 sealed corrections are the matched comparison. VISICALC had one aborted Qwen-route correction after a shared crop defect was found; it used 47,297 uncached input, 301,056 cached input and 1,686 output tokens. Both raw routes were rerun on an identically amended map, followed by two fresh corrections. The original Tesseract correction had never started. Add that paid abort for an observed recovery-inclusive view; it is not an intrinsic Qwen failure penalty. Both views are in the results JSON.

## Article comparison at the illustrative 1:0.1:4 rates

Normalized cost units; negative percentage means Qwen is cheaper. Human repair remains unpriced.

| Article | T cost units | Q cost units | Q versus T |
| --- | ---: | ---: | ---: |
| 편집자 노트 | 88,756.0 | 87,982.6 | -0.87% |
| 죽음의 스키 | 156,616.6 | 163,564.4 | +4.44% |
| 공모총평 | 101,729.8 | 106,645.2 | +4.83% |
| 기초 테크닉 코너 | 280,894.6 | 257,129.0 | -8.46% |
| VISICALC 활용 | 243,670.8 | 242,685.8 | -0.40% |
| PIA 시리즈2 미니네온사인의 제작 | 178,917.0 | 181,430.2 | +1.40% |
| 베이직 코맨드 에디터 | 458,963.6 | 471,649.8 | +2.76% |
| Q&A | 257,000.2 | 244,919.8 | -4.70% |

The Q&A correction is lower in every captured token category, but also has more observed source-spelling errors. The BASIC tutorial favors Qwen in this scenario while the long editor favors Tesseract. Neither contrast establishes a general code/prose cost rule.

## Time diagnostics

These durations have no monetary weight. Raw worker time includes runtime checks, model startup, recognition and export; recognition is nested within it. Correction worker time excludes initial instruction loading and the final reply, while the paid usage audit includes the complete session. Sums below are sequential workload durations, not elapsed calendar completion time.

| Article | T raw seconds | Q raw seconds | T correction seconds | Q correction seconds |
| --- | ---: | ---: | ---: | ---: |
| 편집자 노트 | 6.85 | 22.90 | 129.95 | 125.69 |
| 죽음의 스키 | 8.25 | 43.27 | 243.91 | 243.72 |
| 공모총평 | 7.59 | 26.13 | 147.78 | 197.06 |
| 기초 테크닉 코너 | 14.46 | 59.93 | 386.27 | 379.98 |
| VISICALC 활용 | 19.43 | 94.14 | 300.46 | 404.04 |
| PIA 시리즈2 미니네온사인의 제작 | 12.43 | 51.00 | 248.01 | 241.64 |
| 베이직 코맨드 에디터 | 27.04 | 129.53 | 561.03 | 533.72 |
| Q&A | 19.36 | 75.87 | 375.94 | 333.66 |
| **Total** | **115.41** | **502.77** | **2393.35** | **2459.52** |

The two discarded-coverage raw arms add 113.96 local worker seconds, and the aborted correction adds 60.41 worker seconds. Their evidence and cost remain retained. No cross-engine OCR fallback was used. The Qwen VISICALC worksheet crop hit its bounded output limit in both map versions; failed native output was retained for source-based correction.

## Source fidelity and remaining human work

The coordinator inspected every corrected-text disagreement and each frozen source sample, including agreements. Each independent correction was instructed to check every assigned region. Counts below are confirmed wording/number occurrences in the coordinator-checked regions, not full character error rates. A zero means no confirmed error in those checks, not a perfect article.

| Article | Regions checked | T wording/number errors | Q wording/number errors |
| --- | ---: | ---: | ---: |
| 편집자 노트 | 7 | 0 | 0 |
| 죽음의 스키 | 9 | 1 | 1 |
| 공모총평 | 8 | 1 | 0 |
| 기초 테크닉 코너 | 20 | 1 | 1 |
| VISICALC 활용 | 52 | 0 | 8 |
| PIA 시리즈2 미니네온사인의 제작 | 21 | 0 | 1 |
| 베이직 코맨드 에디터 | 81 | 4 | 2 |
| Q&A | 46 | 3 | 10 |

Additional confirmed punctuation errors in checked regions: VISICALC 활용: T 0, Q 1; 베이직 코맨드 에디터: T 2, Q 0; Q&A: T 2, Q 0.

Original images, source-linked uncertainty notes and sealed independent exports are retained privately. Observed errors have not been silently repaired using the other route. Formatting, graphic approximations, punctuation and uncertain glyphs require their own review; see the pinned private quality records.

## Shared overhead and experiment cost

The experiment also required common source mapping, instrumentation, agent coordination, paired comparison and reporting. That paid work is audited separately. OCR control overlapped other shared work, so it has no clean causal per-engine allocation. The independent correction comparison is better identified than the complete production cost.

| Scope | Uncached input | Cached input | Output |
| --- | ---: | ---: | ---: |
| Shared coordinator | 758,031 | 36,371,328 | 187,664 |
| Observed doubled experiment, including recovery | 2,124,097 | 52,566,528 | 342,943 |

Coordinator cutoff: **2026-10-12T03:34:25.927848+00:00**. The subsequent commit/delivery tail is excluded. The initial selection/setup audit is a subset of coordinator usage and must not be added again. Child response IDs are reconciled separately and do not overlap the coordinator's responses.

A single-route scenario is `C_Q = S + Q correction` or `C_T = S + T correction`, for the same shared preparation charge S. S cancels in the absolute difference, but reduces percentage savings. We cannot extract an actual production-only S from this trial because preparation and experiment-specific work overlap. Charging the entire experiment to both routes would be misleading.

## Scope and reproducibility

The sample covers short prose, a game listing, a contest table, BASIC tutorials, spreadsheets, hardware, a long editor listing and mixed Q&A. It is purposive, with one run per route and four first assignments per engine. Fresh contexts avoid answer reuse; they do not guarantee equal cache state or deterministic assistant behavior. No content category has enough independent articles here for a validated cost router.

Both routes used the same pinned source crop bytes and July-tested runtime settings. The VISICALC shared-coverage recovery and editor pre-inference seam amendment are documented in the [protocol and progress history](OCR-AUGUST-PILOT.md). All exports passed integrity checks and byte-identical rebuilds; input manifests and usage categories reconciled.

Evidence: [selection](ocr-experiments/ocr-august-pilot-selection.json), [progress](ocr-experiments/ocr-august-pilot-progress.json), [independent usage](ocr-experiments/ocr-august-pilot-correction-usage.json), [coordinator usage](ocr-experiments/ocr-august-pilot-usage.json), [consolidated results](ocr-experiments/ocr-august-pilot-results.json).
