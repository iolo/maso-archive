# July 1984: OCR choice by restoration cost

July is the next practical trial after [June](OCR-JUNE-DECISION.md). The decision
is whether an engine reduces paid assistant work enough to justify its additional
elapsed time, for each kind of content. Local GPU resource use is not a decision
criterion. The existing semantic correction and human review process continues.

## Trial plan

Restore the issue incrementally, preserving raw OCR and recording checkpoints.
Use one primary engine for each article or assembly segment. Before OCR, record
its content category, engine, crop map, and any comparison samples. Start with
these opposite assignments, then extend the sample to dense technical prose,
tables, mixed layouts, and longer listings:

| Article | Primary engine | Role | Status |
| --- | --- | --- | --- |
| 편집자 노트 | Qwen | Prose | Restored; printed16 / PDF20 |
| 운전 연습 | Tesseract | BASIC with introductory prose | Restored; printed83 / PDF87 |
| 리뷰 살롱 | Tesseract | Seven book reviews | Restored; printed156–158 / PDF160–162 |
| 합이 15 | Qwen | BASIC with introductory prose and grids | Restored; printed64–65 / PDF68–69 |

Both engines use 4,000-pixel page renders in this trial. Tesseract retains its
pinned runtime, OEM1/PSM6 and one thread, with English for code and Korean+English
for other text. Qwen retains the deterministic June raw-transcription settings.
Tesseract's general default remains3,000 pixels; the trial opts in to4,000.

Use the alternate engine only on the preselected diagnostic crops or when the
primary result needs a documented fallback. Fix the assistant transcription
before obtaining the alternate draft. Do not pay to correct the same passage
twice: the second reading would benefit from remembering the first. Raw OCR
comparisons can be paired; paid correction comparisons here are observational
across different material, with content, length, context and setup confounders.
These four different articles alone cannot establish causal engine savings.

Keep shared preparation, mapping, experiment development, alternate-engine
evaluation, exports and reporting visible. Report correction work separately,
plus the whole observed trial cost. Record retries and failed attempts too.
Compare input, cached input, cache-write input and output separately; normalize
by corrected characters, pages and listing lines only alongside their content
categories. Do not infer dollar savings from a simple token subtotal.

**Reading room: do not rebuild or restage until the user explicitly requests it.**
Native restoration packages and progress records can continue independently.

## First checkpoint, 2026-10-10

Two complete article packages contain19 regions:17 text regions and two original
illustrations. The game has57 numbered BASIC lines and60 physical listing rows.
Six source-linked review flags retain ambiguous spelling/punctuation and printed
unclosed strings. Both packages pass integrity, UTF-8 range, coverage and
byte-identical rebuild checks. No reading-room build or staging was performed.

The scan has a four-page offset on inspected pages. Printed16 is PDF20; printed83
is PDF87. The queue's other offsets remain candidates until visually confirmed.
There are42 canonical TOC entries, two restored bodies and40 entries still pending
restoration or heading classification. Human acceptance remains pending.

| Observation | Qwen editorial | Tesseract game |
| --- | ---: | ---: |
| Raw stage, including render/startup/export | 40.40s | 5.36s |
| Recognition calls, contained in raw stage | 27.17s | 2.07s |
| Correction and recording window | 46.65s | 70.89s |
| Corrected non-whitespace characters | 1,118 | 1,390 |
| Observed uncached, non-write input tokens in correction window | 4,102 | 7,357 |
| Observed cached input tokens in correction window | 199,296 | 213,504 |
| Observed output tokens in correction window | 1,515 | 2,883 |

These are different articles, not a speed or cost ratio. Correction windows include
tool orchestration and writing correction records. The Tesseract window also
contains the response that first adapted the export helper; that mixed response
cannot be split reliably into correction versus setup tokens. Cache-write tokens
were zero in both windows. Qwen's6,141 local tokens are separate from all assistant
usage. Subsequent checkpoints should avoid mixed-purpose responses across timing
boundaries. Short shell-only setup windows do not measure their authoring cost.

The four fixed raw-OCR comparisons use identical PNGs and both directions of
reference preparation: the editorial reference came from a Qwen draft; the game
references came from a Tesseract draft. All are unblinded assistant scan readings.

| Crop | Content | Qwen compact CER | Tesseract compact CER |
| --- | --- | ---: | ---: |
| p20r03 | Editorial prose | 0.00% | 6.67% |
| p87r04 | Game prose | 0.91% | 6.39% |
| p87r06 | BASIC lines100–270 | 0.00% | 7.33% |
| p87r08 | BASIC lines400–490 | 0.00% | 12.66% |

Compact CER ignores whitespace, including string-literal spaces. These are
supporting diagnostics, not independent human-gold accuracy or execution tests.
Qwen again gives cleaner drafts on this small sample; the paid-work decision
awaits the reverse assignments and additional content categories.

## Reverse assignments completed, 2026-10-10

The second pair adds five source pages,55 regions, two original image strips and
107 numbered BASIC lines. All seven book reviews retain their publishing details.
The game retains its three grids, printed misspellings and the apparent logic
error at line920. Qwen's invented wrap within line48 was restored to one printed
row. Eleven review flags cover source wording and uncertain glyphs/literal spaces.
Both packages pass full coverage, integrity, UTF-8 range and byte-identical rebuild
checks. The listing has107 physical rows and107 distinct printed line numbers.

July now has four complete article bodies over seven source pages:74 regions,
70 text regions, four original images,164 logical BASIC lines and17 review flags.
Thirty-eight TOC entries remain pending restoration or heading classification.
The reading room has not been rebuilt or restaged.

| Observation | Tesseract book reviews | Qwen sum15 game |
| --- | ---: | ---: |
| Source pages | 3 | 2 |
| Raw stage, including render/startup/export | 19.74s | 73.37s |
| Recognition calls, contained in raw stage | 9.40s | 63.03s |
| Correction and recording window | 117.92s | 72.32s |
| Corrected non-whitespace characters | 3,607 | 2,244 |
| Observed uncached, non-write input tokens in correction window | 7,304 | 12,665 |
| Observed cached input tokens in correction window | 345,472 | 182,144 |
| Observed output tokens in correction window | 4,779 | 2,567 |

Neither new correction window includes export-helper development. Both include
scan inspection and writing correction/review records. Cache-write tokens were
zero. Qwen's13,683 local tokens are separate from assistant usage.

The Qwen game contains107 listing lines versus57 in the earlier Tesseract game,
yet its correction window is similar in duration (72.32s versus70.89s) and uses
slightly fewer output tokens (2,567 versus2,883). Its uncached input is higher
(12,665 versus7,357), including the enlarged scans inspected in that response.
This supports fewer transcription edits, but does not establish a paid-cost win.
The games differ in listing length, prose proportion, layout and print quality;
the earlier Tesseract window also included one setup response.

Six further raw-OCR samples were fixed before primary inference. Transcriptions
were sealed before alternate-engine inference; Tesseract-derived references
supply the three book-review samples, Qwen-derived references the game samples.

| Crop | Content | Qwen compact CER | Tesseract compact CER |
| --- | --- | ---: | ---: |
| p160r04 | Book-review prose | 0.00% | 5.92% |
| p161r09 | Book-review prose | 0.34% | 4.42% |
| p162r11 | Book-review prose | 0.51% | 9.14% |
| p68r03 | Game instructions | 0.00% | 13.16% |
| p68r09 | BASIC lines35–53 | 0.00% | 3.04% |
| p69r03 | BASIC lines400–520 | 0.00% | 9.05% |

These six samples again favor Qwen's raw text. Zero compact CER does not imply
faithful line wrapping: it deliberately ignores the invented wrap in line48.
The references remain unblinded assistant readings. Continue with technical
tables and mixed layouts before adopting a routing rule.

## Evidence and continuation

- [Issue progress and package pins](ocr-july-progress.json)
- [Four matched crop comparisons](ocr-july-comparison-01.json)
- [Six reverse-assignment crop comparisons](ocr-july-comparison-02.json)
- [Assistant usage by work window, including shared overhead](ocr-july-usage.json)
- Private queue, maps, raw evidence, corrections and scripts:
  `private/pdf-restoration/12-1984-07-comparison/`
- Native packages: `build/pdf-restoration/12-1984-07-comparison-batch-01/editorial/`
  and `build/pdf-restoration/12-1984-07-comparison-batch-02/driving/`
- New packages: `build/pdf-restoration/12-1984-07-comparison-batch-03/review-salon/`
  and `build/pdf-restoration/12-1984-07-comparison-batch-04/sum15/`

The usage audit reads only local `token_usage_record` rows, deduplicates response
IDs, rejects overlapping windows, and preserves unknown fields as null. Cached
input and reasoning output are subsets, not additional tokens. Usage observations
are not a bill; this distinction is also documented in
[OpenAI's usage guidance](https://developers.openai.com/api/docs/guides/agents-api/observability).
Completion timestamps determine window attribution, including boundary-straddling
responses. Between-window usage stays visible as unattributed overhead. The first
response's duration predates the first usage timestamp; final reporting/commit
work after the saved cutoff must be included in a later audit.

Re-audit explicit completed windows without exporting conversation text:

```sh
PYTHONPATH=src:. python3 -m tools.pdf_restore.usage \
  --session-log /path/to/current-rollout.jsonl \
  --windows private/pdf-restoration/12-1984-07-comparison/work-windows.json \
  --output /tmp/july-usage.json
```

Next: inspect technical/table candidates such as SPC-1000 음악기능과 명령어 and
PIA 시리즈1 뮤직카드, then assign engines before their inference. These candidates
are not yet mapped or assigned. Keep mapping and setup outside correction windows.
The cumulative usage audit now includes earlier reporting/commit responses through
the new cutoff; gaps remain visible and calendar spans are not active work time.
Preserve earlier packages and commit each checkpoint. Reading-room work remains
explicitly deferred.
