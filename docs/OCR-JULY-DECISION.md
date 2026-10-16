# July OCR routing decision

> Historical experiment report/protocol. Measurements and original conclusions
> below are retained. For future restoration, follow the owner's 2026-10-14
> [OCR policy](../PLAN-OCR.md): mapped Tesseract by default, Qwen as explicit
> assistance with layout/coverage review. This report does not queue a new trial.


Continue the provisional content-routing rule. July supports Qwen's raw accuracy
advantage, but does **not** establish that it saves paid correction tokens or total
time. Tesseract remains useful for cheap drafts and bounded probes; Qwen is a
strong starting choice for code, structured values and difficult Korean text.
Semantic correction and human review remain mandatory.

All **36 article bodies across 225 source pages** are restored, including complete
assemblies: 54 checkpoints, 42 contents entries (six group headings), 4,940 regions
and 262 figures. All human acceptance remains pending. The workflow used 11 Qwen,
three Tesseract and 40 mixed checkpoints; these differently sized, deliberately
selected groups are not a controlled engine-cost comparison.

## Raw accuracy

Compact character error rate removes whitespace and divides total edits by total
reference characters. It does not measure layout, executable code or final human
acceptance. These are purposive crops with unblinded assistant references, not
independent human gold or a random whole-issue sample.

| Content | Crops | Reference characters | Qwen CER | Tesseract CER |
| --- | ---: | ---: | ---: | ---: |
| Prose | 85 | 8,664 | 1.24% | 9.83% |
| Code | 78 | 11,437 | 2.53% | 26.20% |
| Other structured content | 42 | 3,745 | 4.38% | 40.93% |
| Title | 1 | 7 | 0.00% | 14.29% |
| Combined | 206 | 23,853 | **2.35%** | **22.56%** |

Qwen won 197 crops, Tesseract four, with five ties. Retained counterexamples are
batch21 p88r04/p91r10, batch26 p120r17 and batch49 p247r08. The four advertising
index rows use decorative-leader normalization and remain separate: 38 characters,
Qwen 0%, Tesseract 71.05%. Three Tesseract index rows were blank under the tested
settings. These findings do not cover every Tesseract mode or Qwen prompt.

June independently showed 2.22% versus 25.61% on 97 ordinary crops. The direction
agrees; different content, crops and routing prevent treating the month-to-month
change as improvement or regression. Neither trial measures a final corrected
error rate. Source-linked ambiguities, spacing and printed errors still require
human judgment.

## Time and local work

On **209 timed matched crops**, Qwen took **805.51s** and Tesseract **41.42s**:
**19.45×** the raw recognition time. Medians were 3.24s and 0.179s. Batch16 p62r03
has no Tesseract timer, so both sides of that pair are excluded. Crop times exclude
model loading, rendering and correction. June's 7.17× ratio came from a different
cohort; it is not a fixed engine multiplier.

Whole-worker timers include setup/loading, rendering and output work. July has
47 exact recorded batches totaling **192.21 minutes**, plus six bounded batches
totaling **24.87–39.20 minutes**. Batch24's **5.37 minutes** are separately retained
as contaminated by competing-model startup. These are observed worker intervals,
not a clean whole-project benchmark. At least **53.78 minutes** of recorded raw
work overlaps correction windows. Do not add raw time to correction time.

The native-response audit reconciles **3,939 unique primary Qwen responses** and
**1,776,981 captured local tokens**, including 11 length-limited responses and
superseded work; 275 copied response files are excluded. Interrupted generation
without a response remains unknown, making the aggregate a lower bound. An additional **24,246 tokens across 36 captured alternate Qwen calls** are
recorded separately as evaluation. These are local tokens, not paid assistant tokens. Local
GPU expense is excluded from the decision as requested.

## Paid work and interpretation

The restoration audit cutoff is **2026-10-11 20:24:41 UTC**. Across the full observed
span, including between-window work, it records:

| Token class | Observed tokens |
| --- | ---: |
| Uncached input | 5,761,609 |
| Cached input | 253,555,328 |
| Output | 1,400,029 |
| Reasoning, already included in output | 326,855 |

The named windows total **12.66 hours**, including waits and helper work. Windows
labeled correction account for **6.59 hours**, 2,549,361 uncached input, 104,042,240
cached input and 694,930 output tokens. Evaluation-labeled windows account for
0.64 hours, 167,630 uncached input and 64,129 output tokens. Mapping/preparation,
export, assembly, reporting and accounting remain in the full totals, with exact
stage breakdowns in the machine-readable report. Source reading also occurred in
preparation, so correction-only totals understate that effort.

Between-window usage is retained: 748,046 uncached input, 39,313,536 cached input
and 140,893 output tokens. The 41.12-hour calendar span includes idle gaps and is
not working time. Windows with no observed response are unknown, not free. Usage
is attributed by response completion timestamp; it is not an invoice. Consolidation
and reading-room delivery after this cutoff are tracked separately in the final
usage audit, not silently attributed to restoration.

No second paid correction was performed on the same passage under the alternate
engine. Content difficulty, source checking, layout repair, caching, retries and
workflow changes therefore confound engine comparisons. June has no comparable
paid usage audit. We can say Qwen often supplies a much better draft and Tesseract
recognizes text much faster; we cannot yet quantify the paid-token exchange rate
between them. A dollar estimate would additionally require the actual applicable
cached/uncached/output rates.

The final delivery audit through **2026-10-11 22:15:23 UTC** records **5,885,171
uncached input**, **259,030,400 cached input** and **1,430,979 output** tokens;
330,911 reasoning tokens are already included in output. Named windows total
12.92 hours. Consolidation adds a 6.45-minute window, reading-room delivery 8.42
minutes and final accounting 0.47 minutes. Their observed uncached/output tokens
are respectively 57,176/14,292, 40,851/11,439 and 2,242/608; cached input and
between-window overhead remain in the machine-readable audit. The interrupted
browser wait is outside active review windows, whose first segment ends at the
last confirmed completed browser action. The final commit/report tail after this
cutoff is excluded. These delivery costs are separate from the frozen restoration
figures above.

## Practical rule

Follow the [documented routing heuristic](OCR-JULY-TRIAL.md#provisional-engine-selection-heuristic):
probe a representative simple prose crop when uncertain; retain Tesseract if its
draft is easy to correct, and switch when identifiers, values or reading order
break down. Favor Qwen for code and structured content, but bound generation and
retain failure costs. Separate graphics or repetitive decorative glyph bands
from ordinary text. Preserve scan coverage checks even when OCR reports success.

Routing is a useful working policy, not a proven cost optimum. More restoration
alone will not resolve the causal cost question: a future bounded, matched
correction experiment would be needed, if that evidence is worth its extra cost.

Reproduce with `PYTHONPATH=src:. python3 -m tools.ocr_qwen.consolidate_july`.
[Metrics and evidence pins](ocr-experiments/ocr-july-metrics.json), [usage audit](ocr-experiments/ocr-july-usage.json),
[progress](ocr-experiments/ocr-july-progress.json), and [June context](OCR-JUNE-DECISION.md) retain
the evidence and limitations. Raw transcriptions and native responses remain private.
