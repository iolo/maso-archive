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
| SPC-1000 음악기능과 명령어 | Qwen | Technical prose, table, formulas, BASIC and diagrams | Restored; printed47–51 / PDF51–55 |
| PIA 시리즈1 뮤직카드 — hardware segment | Tesseract | Hardware prose, circuit/pinout diagrams and construction photos | Hardware segment restored; printed180–183 / PDF184–187 |
| PIA 시리즈1 뮤직카드 — software instructions | Qwen | Commands, addresses, joystick controls and musical notation | Restored and assembled; PDF188–190 and upper191 |
| PIA 시리즈1 뮤직카드 — hex listing | Qwen | Dense addressed hexadecimal dump | Restored and assembled; lower PDF191 and PDF192–194 |
| Z-80 feature — opening and sections1–3 | Qwen | Low-contrast opening, signals/subscripts and diagrams | Segment restored; PDF21–26;27–38 deferred |

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
These different articles alone cannot establish causal engine savings.

Keep shared preparation, mapping, experiment development, alternate-engine
evaluation, exports and reporting visible. Report correction work separately,
plus the whole observed trial cost. Record retries and failed attempts too.
Compare input, cached input, cache-write input and output separately; normalize
by corrected characters, pages and listing lines only alongside their content
categories. Do not infer dollar savings from a simple token subtotal.

**Current goal,2026-10-11:** restore all remaining July article bodies, consolidate
metrics, then build the reading room for human review. This explicit request
supersedes the earlier reading-room hold; build it after the issue restoration.

## Provisional engine-selection heuristic

Recorded2026-10-11. Use Tesseract when its mistakes leave an easy-to-correct draft;
use Qwen when mistakes destroy structure or make individual characters expensive
to verify. This is a working hypothesis from the trial, not a demonstrated
paid-cost ranking or an automatic routing implementation.

| Content | Starting choice | Reason and evidence limit |
| --- | --- | --- |
| Clear, ordinary prose | Tesseract | Fast draft; context often makes errors easy to resolve. Qwen also reads prose better in our samples, so Tesseract is not a proven cost winner. |
| Numeric tables, formulas, dense technical notation | Qwen | Values, symbols and relationships are costly to reconstruct. The July frequency table supports this choice under the tested settings; other table layouts remain untested. |
| BASIC, assembly, hexadecimal listings | Qwen | Individual characters need careful checking. BASIC and four long-hex sample crops favor Qwen raw text; the full hex listing still required substantial byte checking. Paid savings and other assembly formats remain unproven. |
| Faint, degraded or unusually styled text | Qwen candidate | Try when Tesseract produces substantial garbage. This is a plausible fallback heuristic, not a settled July finding. |
| Diagrams and photographs | Preserve original image | Transcribe surrounding prose/captions separately. Diagram reconstruction is a distinct task. |

Choose by content, not page count. Mixed articles may use different engines for
homogeneous groups of mapped regions or coherent assembly segments, such as
Tesseract for an introduction and Qwen for a listing. Record the chosen primary
engine and scope before inference; current runs still use an explicitly selected
engine per checkpoint rather than automatic per-region routing.

When uncertain, inspect one representative Tesseract crop before committing the
rest of the segment. Switch if identifiers are repeatedly corrupted, table rows
are lost, reading order is mixed, or substantial text becomes unreadable fragments.
Ordinary spacing/wrapping problems alone do not justify switching. This bounded
probe is optional: do not routinely run both engines over the entire article.
Record all probes, fallbacks and retries, retain their raw evidence, and include
their elapsed cost. Correct the selected draft only once.

For planned comparisons, keep preselected assignments and samples fixed unless a
fallback is explicitly recorded. Seal the source-checked reference before alternate
OCR; do not retroactively choose the cleaner engine and call it the original
assignment. Keep diagnostic/evaluation costs separate from ordinary restoration.

Semantic correction and human review continue whichever engine is chosen. Judge
this heuristic by paid correction usage and total elapsed work across comparable
content categories, not raw CER alone. The music-card hex checkpoint supports the
raw-quality choice but also demonstrates its substantial remaining review cost.

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

## Technical article completed, 2026-10-10

Batch05 restores SPC-1000 음악기능과 명령어, printed47–51/PDF51–55,
with Qwen. Advertisement PDF50 and the next article beginning PDF56 are outside
the body. Its87 regions contain82 text crops and five original figures, including
a retained image of the frequency table. The searchable table has13 TSV rows
including its header, nine columns and96 numeric data cells. The merged-cell
register diagram and waveforms remain original images; their labels are not
claimed as searchable transcriptions. The SOUND TEST listing has43 numbered rows,
100–520. All regions have source evidence;18 review flags remain for human review.

Column/page continuations are joined explicitly. Corrections include 그림 misread
as 그룹/그럼, zeros misread as O, crop-boundary completions and musical symbols
collapsed into generic eighth notes. Source anomalies are preserved:216.63Hz in
prose,1474.98 in the table, PT/TP and repeated CT in a formula, B7 in an R7
discussion, SOUND register6 at210/410, and230 after a stated FT=240. These are
transcriptions, not repaired technical instructions or tested programs.

| Observation | Qwen SPC-1000 music |
| --- | ---: |
| Source pages | 5 |
| Raw stage, including render/startup/export | 301.99s |
| Recognition calls, contained in raw stage | 273.87s |
| Server startup/readiness, also contained in raw stage | 1.46s |
| Correction and recording window | 232.83s |
| Corrected non-whitespace characters | 8,189 |
| Observed uncached, non-write input tokens in correction window | 26,623 |
| Observed cached input tokens in correction window | 532,992 |
| Observed output tokens in correction window | 10,485 |
| Local Qwen tokens, separate from assistant usage | 44,891 |

Correction includes scan inspection, transcribing/rewrapping prose, explicit
assembly joins and review-record writing. It reuses the existing export helper;
no helper implementation is included. Cache-write tokens were zero. This longer,
denser article cannot be compared causally with the shorter games and reviews.
Startup is one new llama-server process per batch, reused for all crops and then
stopped. Startup measurements include model loading/readiness, with no controlled
cold filesystem-cache test. Per-crop recognition comparisons exclude startup.

Four samples were selected before primary inference and their references sealed
before alternate Tesseract calls. Both engines received exactly the same PNGs.

| Crop | Content | Qwen compact CER | Tesseract compact CER |
| --- | --- | ---: | ---: |
| p53r13 | Register explanation | 1.75% | 26.32% |
| p54r01 | Frequency table | 0.00% | 89.43% |
| p54r13 | BASIC lines250–390 | 1.08% | 5.91% |
| p55r17 | Envelope formula and prose | 0.00% | 11.11% |

The table is strong evidence for Qwen with these settings: all96 numeric cells
match the assistant's scan reading. Tesseract's current whole-table OEM1/PSM6,
kor+eng configuration loses much of this grid. This does not test row/cell
segmentation or other Tesseract settings. Compact CER ignores whitespace and cell
delimiters, so the separate TSV shape check matters; references are still
unblinded assistant readings, not independent human gold.

Shared costs remain visible. Mapping includes preliminary inspection of the next
music-card article. The raw-monitoring window contains13 assistant responses,
recorded separately from semantic correction and local model tokens. Evaluation
script authoring and export orchestration can fall between windows under the
completion-timestamp policy; those tokens remain in the cumulative unallocated
usage rather than being presented as zero-cost work. Conversation about startup
and the time/token tradeoff since the prior checkpoint is also carried forward
as between-window usage, not article correction time.

Native integrity, UTF-8 ranges, explicit listing numbers, complete region coverage,
table shape and byte-identical rebuild checks passed. July now has five complete
bodies across12 source pages:161 regions,152 text regions,nine original images,
207 logical BASIC lines and35 review flags. Thirty-seven TOC entries remain pending
restoration or heading classification. No reading-room rebuild or staging occurred.

## Music-card hardware segment completed, 2026-10-11

Batch06 restores the first four pages of PIA 시리즈1 뮤직카드 with Tesseract:
printed180–183/PDF184–187. The49 regions contain41 text crops and eight original
diagrams/photos. The boxed kit-sales advertisement on PDF185 is explicitly
excluded and masked before OCR. Diagram labels remain in source images; they are
not claimed as searchable transcriptions or included in accuracy samples.

This is a **partial article**, ending after the hardware construction instructions.
The software instructions, references and hexadecimal listings on PDF188–194
remain deferred. The package records all11 article pages, the four included pages,
the seven deferred pages and the need for full assembly. No listing lines are
claimed by this segment. Progress accounting now distinguishes complete articles
from partial bodies and checkpoint counts.

| Observation | Tesseract music-card hardware |
| --- | ---: |
| Source pages | 4 |
| Raw stage, including render/validation/export | 22.16s |
| Recognition calls, contained in raw stage | 8.06s |
| Correction and recording window | 128.80s |
| Corrected non-whitespace characters | 2,803 |
| Observed uncached, non-write input tokens in correction window | 10,395 |
| Observed cached input tokens in correction window | 481,152 |
| Observed output tokens in correction window | 4,874 |

Correction includes scan inspection, regional text, joins and review records;
the export helper was reused. Its date handling and partial-progress accounting
were adapted during setup, outside correction. Cache-write tokens were zero.
Tesseract's raw draft repeatedly confused IC with10 and replaced Korean words
with Latin fragments. Those errors were corrected against the scans. Printed
씨리즈, 실예 and schematic inconsistencies are retained, with seven review flags.

The four samples were selected before OCR and their Tesseract-derived references
sealed before alternate Qwen inference. Both engines received identical PNGs.

| Crop | Content | Qwen compact CER | Tesseract compact CER |
| --- | --- | ---: | ---: |
| p184r04 | Music-card capabilities | 0.00% | 4.92% |
| p186r05 | PSG explanation | 0.00% | 14.40% |
| p186r11 | Sound-control explanation | 0.55% | 2.76% |
| p187r05 | PIA pin-range explanation | 2.72% | 4.08% |

All four favor Qwen raw text, including references prepared from Tesseract drafts.
They remain unblinded assistant readings rather than independent human gold.
Alternate Qwen startup/inference is evaluation overhead, not part of the22.16s
Tesseract raw stage. This four-page illustrated segment contains much less text
than the five-page SPC article, so its lower correction totals do not establish
an engine cost advantage. Different content, crop sizes, context and retained
figures still confound article-level comparisons.

Native integrity, complete coverage of the included regions, UTF-8 ranges and
byte-identical rebuild checks passed. The exclusion mask and partial/deferred
coverage metadata were also checked. Across six checkpoints, July now has five
complete bodies and one partial body over16 source pages:210 regions,193 text
regions,17 original images,207 logical BASIC lines and42 review flags. Thirty-seven
TOC entries remain unfinished, including this partial body;36 are untouched.

The cumulative audit carries forward prior reporting/commit responses. Overnight
calendar gaps are not active work. The reporting window for this checkpoint also
spans a brief user interruption/resume and is labelled accordingly; raw OCR and
correction timings had already been closed and are unaffected. No reading-room
rebuild or staging occurred.

## Routing applied to software instructions, 2026-10-11

Batch07 applies the documented rule within the same music-card article: Qwen for
command-heavy software instructions after Tesseract for the hardware section.
The choice and four diagnostic samples were recorded before inference. It restores
printed184–186/PDF188–190 and the upper part of printed187/PDF191, including the
references. Its75 regions contain69 text crops and six original images. The menu
also has a searchable14-row, two-column transcription. Commands in prose are not
counted as executable listing rows.

**PDF191 is only partially restored.** The three hex columns below its references,
and PDF192–194, remain deferred. The article now covers PDF184–191, with184–190
fully restored for the article body. Both segments retain separate packages and
require assembly after the listing is restored. They still count as one partial
article, not two completed articles.

| Observation | Qwen software instructions |
| --- | ---: |
| Raw stage, including render/startup/export | 203.29s |
| Recognition calls, contained in raw stage | 181.05s |
| Server startup/readiness, also contained in raw stage | 1.26s |
| Correction and recording window | 178.32s |
| Corrected non-whitespace characters | 4,722 |
| Observed uncached, non-write input tokens in correction window | 29,044 |
| Observed cached input tokens in correction window | 316,160 |
| Observed output tokens in correction window | 6,422 |
| Local Qwen tokens, separate from assistant usage | 32,686 |

Correction includes scan inspection, transcription, explicit joins and review
records. Partial-page accounting/export helpers were adapted during setup, outside
correction. Cache-write tokens were zero; no raw inference retries occurred.
Shared preparation took337.73s, including mapping, seam checks, helper changes and
context recovery. The raw-monitoring window also contains helper/document reads
and preparation of the comparison script and continuation plan. Its assistant
usage is shared orchestration, not pure OCR or semantic correction. All these
costs remain visible in the usage audit.

Seventeen review flags preserve source anomalies and transcription limitations.
Qwen read the insertion key I as T and lost musical notation and some Korean
words. The corrected text retains the source's repeated SW(1), figure3 reference,
DEBUG heading 수립, RHYTH heading and Programm spelling. Complex triplet notation
uses explicitly marked editorial text substitutes linked to scans; boxed 이름 is
also marked as a placeholder, not literal command syntax. Japanese references and
faint beep spelling remain flagged. No musical program or hex bytes were tested.

The Qwen-based reference was sealed before alternate Tesseract inference on the
same four PNGs. No paid correction was repeated.

| Crop | Content | Qwen compact CER | Tesseract compact CER |
| --- | --- | ---: | ---: |
| p188r05 | Program memory addresses | 0.00% | 3.54% |
| p188r09 | Command menu | 0.00% | 58.87% |
| p190r07 | Volume instructions | 0.00% | 17.59% |
| p191r09 | Disk-load instructions | 1.65% | 16.53% |

The two Qwen differences in the final row are ASCII brackets versus the editorial
double brackets representing a printed box; they are not misrecognized Korean
letters. Scores retain the sealed reference without retrospective normalization.
Menu results use the fixed whole-crop Tesseract PSM6 configuration; separately
segmented rows/cells were not tested. References remain unblinded assistant
readings, not independent human gold.

These results support Qwen for this menu/notation category, while leaving the
paid-cost decision open. Software has4,722 corrected characters versus2,803 in the
hardware segment, and required more enlarged-image inspection. Lower output per
character but higher uncached input per character is a mixed observation; content,
context and transcription choices prevent a causal engine-cost comparison.
Long hex listings remain the next untested case. Keep the routing rule provisional.

Native integrity, UTF-8 ranges, complete included-region coverage, menu shape and
byte-identical rebuild checks passed. Checks also confirmed partial-page progress,
no overlap with deferred hex crops, reproducible masked crops and distinct block
IDs for later assembly. All seven package pins/exports remain valid. Totals are
five complete bodies and one partial body over20 represented source pages (19
fully restored for their selected article bodies):285 regions,262 text regions,
23 original images,207 logical BASIC lines and59 review flags.37 TOC entries remain
unfinished, including the partial music-card body;36 are untouched. Human review
and reading-room rebuilding remain pending; no reading-room build/staging occurred.

## Evidence and continuation

- [Issue progress and package pins](ocr-july-progress.json)
- [Four matched crop comparisons](ocr-july-comparison-01.json)
- [Six reverse-assignment crop comparisons](ocr-july-comparison-02.json)
- [Four technical/table crop comparisons](ocr-july-comparison-03.json)
- [Four hardware-prose crop comparisons](ocr-july-comparison-04.json)
- [Four software-instruction crop comparisons](ocr-july-comparison-05.json)
- [Assistant usage by work window, including shared overhead](ocr-july-usage.json)
- Private queue, maps, raw evidence, corrections and scripts:
  `private/pdf-restoration/12-1984-07-comparison/`
- Native packages: `build/pdf-restoration/12-1984-07-comparison-batch-01/editorial/`
  and `build/pdf-restoration/12-1984-07-comparison-batch-02/driving/`
- New packages: `build/pdf-restoration/12-1984-07-comparison-batch-03/review-salon/`
  and `build/pdf-restoration/12-1984-07-comparison-batch-04/sum15/`
- Technical article: `build/pdf-restoration/12-1984-07-comparison-batch-05/spc1000-music/`
- Partial hardware segment: `build/pdf-restoration/12-1984-07-comparison-batch-06/music-card-hardware/`

- Partial software segment: `build/pdf-restoration/12-1984-07-comparison-batch-07/music-card-software/`

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

Next: map the hexadecimal listing on lower PDF191 and PDF192–194. Qwen is the
provisional choice under the routing rule; fix detailed crops and samples before
inference. Preserve hardware06 and software07, then assemble the full article
after the listing is restored. Keep setup outside correction windows.
The cumulative usage audit now includes earlier reporting/commit responses through
the new cutoff; gaps remain visible and calendar spans are not active work time.
Preserve earlier packages and commit each checkpoint. Reading-room work remains
explicitly deferred.

## Long hex listing and full music-card assembly, 2026-10-11

Batch08 restores lower PDF191 and PDF192–194 with Qwen, selected before inference.
The75 code crops contain1,071 addressed rows and8,568 transcribed bytes. The
printed ranges4000–5727 and6000–6A4F remain separate; no bytes were invented for
the gap5728–5FFF. Two rows omitted by Qwen,47E8 and6590, were restored from scans.
Corrections also address8/B substitutions, erroneous zero cells and a row-boundary
error. Sixteen specific flags retain uncertain readings and source overprinting.
Every row was compared with its crop, but byte-perfect accuracy and execution are
unverified. Valid-looking byte substitutions can pass structural checks.

| Observation | Qwen hex segment |
| --- | ---: |
| Raw stage, including render/startup/export | 833.14s |
| Recognition calls, contained in raw stage | 807.55s |
| Server startup, contained in raw stage | 1.26s |
| Correction and recording window | 913.35s |
| Corrected non-whitespace characters | 22,491 |
| Observed uncached, non-write correction input tokens | 134,999 |
| Observed cached correction input tokens | 3,691,648 |
| Observed correction output tokens | 24,424 |

Cache-write tokens were zero. Qwen's59,727 local tokens (31,128 prompt and28,599
completion) are separate from assistant usage. There were75 fresh inferences,
no cache hits and no inference retries. The first row-detection map was rejected
and repaired before inference; its preparation cost is retained.

Correction began on completed pages while the final raw page was still running:
the windows overlap by about183 seconds. Do not add raw and correction durations
as serial elapsed. The650.57-second assistant raw-monitoring window also includes
shared-page assembler development/tests, queue classification and next-article
preflight; it is labelled shared work, not ordinary OCR or semantic correction.
Setup256.84s, export26.71s, evaluation22.48s and assembly104.57s remain separately
recorded, along with reporting and between-window usage. Assembly includes a
verification-call signature error corrected without repeating OCR or modifying
the exported source segments.

Four15-row crops, one from each page's second column, were fixed before inference.
The reference was sealed before alternate Tesseract OCR on identical PNGs.

| Crop | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p191r25 | 4.44% | 45.08% |
| p192r28 | 0.63% | 43.81% |
| p193r28 | 2.86% | 48.57% |
| p194r28 | 1.59% | 48.57% |
| Pooled60 rows /1,260 reference characters | 2.38% | 46.51% |

This supports Qwen as the starting choice for this kind of dense hex under the
fixed settings. It does not show that hex correction is cheap: scan comparison
still took over15 minutes. References are unblinded assistant readings from Qwen,
not independent human gold. CER ignores whitespace and is not a byte-error rate.
Tesseract used English OEM1/PSM6 without font-specific tuning or per-cell crops.
No second paid correction was performed, so paid savings remain unmeasured.

The full music-card article is now assembled from hardware06/Tesseract,
software07/Qwen and hex08/Qwen: PDF184–194,199 regions,14 original figures and40
source-linked review flags. Shared PDF191 is represented once, with disjoint
software and hex regions; the original deferred exclusion remains in the retained
software segment. The boxed advertisement on185 remains excluded. All original
segments and OCR provenance are retained. Assembly and native export integrity,
all review byte ranges,1,071-row listing identity and byte-identical rebuilds pass.
The shared-page implementation passed90 assembly/build/package tests.

July now has six complete bodies and30 remaining paginated body candidates,
covering23 distinct restored source pages:360 regions,337 text crops,23 figures,
207 logical BASIC lines and1,071 physical hex rows, with75 review flags. Six
unpaginated TOC parent headings are classified separately; all42 TOC entries remain
accounted for. Section-opener images remain source material, not separate article
bodies. Human acceptance is pending for every restored article.

Next is the Z-80 feature, candidate PDF21–38/printed17–34, routed provisionally to
Qwen for dense technical notation; detailed mapping and fixed samples precede OCR.
Reading-room construction follows full restoration and metric consolidation under
the active goal. No reading-room build was performed at this checkpoint.

## Z-80 opening and sections1–3, 2026-10-11

Batch09 uses Qwen for PDF21–26/printed17–22: title/introduction, address/data
buses, memory signals and input/output signals. The full feature extends through
PDF38; sections beginning with CPU control on27 remain deferred. The77 mapped
regions contain68 text crops and nine original diagrams with separate searchable
captions. Fourteen review flags retain source wording, small glyph ambiguity and
technical inconsistencies. No executable code or circuit behavior is certified.

Corrections include 핀 접속도 misread as 편집속도, 번지 misread as 변수,
입출력 misread as 입력력, dropped active-low bars and small numeric glyphs.
Visible overbars use combining U+0305 per letter; subscripts and superscripts use
Unicode. Bars are not inferred merely because a signal should be active-low.
For example, the source puts bars over RD, READ and WRITE but leaves WR unbarred
in one occurrence; that variation is retained. Printed S-RAM in a D-RAM density
argument,5비트,16비트 and the caption 비퍼 also remain, with review flags.

| Observation | Qwen Z-80 opening |
| --- | ---: |
| Raw stage, including render/startup/export | 247.89s |
| Recognition calls, contained in raw stage | 218.75s |
| Server startup, contained in raw stage | 1.26s |
| Correction and recording window | 295.99s |
| Corrected non-whitespace characters | 6,340 |
| Observed uncached, non-write correction input tokens | 25,450 |
| Observed cached correction input tokens | 1,552,256 |
| Observed correction output tokens | 10,118 |

Cache-write tokens were zero. Local Qwen38,645 tokens (32,763 prompt and5,882
completion) are separate from assistant usage. There were68 fresh inferences,
no cache hits and no retries. A prose seam with residual ink was moved into clear
whitespace before inference. Correction overlapped the raw engine run by181.49s;
do not add those durations as serial elapsed. Mapping/preflight, export19.43s,
evaluation50.05s and reporting are separately recorded. The assistant raw window
includes comparison-helper preparation; it is not identical to the raw-engine timer.

| Fixed crop | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p21r04 — low-contrast opening | 0.00% | 1.64% |
| p22r11 — address/subscript prose | 0.00% | 14.74% |
| p24r02 — memory control signals | 13.25% | 19.88% |
| p25r14 — input/output prose | 0.00% | 1.32% |

All22 Qwen compact edits in the memory-signal sample are20 missing overbar
codepoints plus two straight/curly quote differences. The base letters match when
those features are ignored; overbar omission still matters for this notation.
The primary scores retain all these features. CER is a codepoint measure, not a
grapheme-error rate. The fixed references are unblinded assistant readings sealed
before alternate OCR, not human gold. Tesseract used the same crops, kor+eng,
OEM1/PSM6 without font-specific tuning. No second paid correction was performed.

These samples support Qwen for the notation-heavy material, while the two ordinary
prose crops show a much smaller raw-quality difference. That is consistent with
content routing, but still does not demonstrate paid-token savings. Native export,
source-linked review byte ranges and byte-identical rebuild checks pass.

July now has six complete bodies, one partial body and29 untouched bodies
(30 bodies still unfinished). Across nine checkpoints:29 source pages,437 regions,
405 text crops,32 original figures,207 logical BASIC lines,1,071 physical hex rows
and89 review flags. Human acceptance remains pending. Next: map Z-80 PDF27–32,
then33–38 and full assembly. The reading room remains deferred until full issue
restoration and metric consolidation.
