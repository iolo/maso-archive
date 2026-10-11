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
| Musical note/rest glyph bands | Preserve original image with labeled editorial description | Batch13 Qwen repeated symbols until the response limit. Separate numeric rows for OCR; symbol names are descriptions, not a literal transcription or a tested Tesseract result. |

Choose by content, not page count. Mixed articles may use different engines for
homogeneous groups of mapped regions or coherent assembly segments, such as
Tesseract for an introduction and Qwen for a listing. Record the chosen primary
engine and scope before inference; current runs still use an explicitly selected
engine per checkpoint or a recorded per-region assignment list. Batch15 uses
such a preassigned mixed list; there is still no automatic content classifier.

When uncertain, inspect one representative Tesseract crop before committing the
rest of the segment. Switch if identifiers are repeatedly corrupted, table rows
are lost, reading order is mixed, or substantial text becomes unreadable fragments.
Ordinary spacing/wrapping problems alone do not justify switching. This bounded
probe is optional: do not routinely run both engines over the entire article.
Record all probes, fallbacks and retries, retain their raw evidence, and include
their elapsed cost. Correct the selected draft only once. Check crop coverage against
visible source rows even when the engine reports success: batch14 returned just a
continuation line while silently omitting nine numbered lines below it. For mixed
code/graphics, keep explicit scan-linked graphic placeholders; a bounded Tesseract
fallback can end a Qwen repetition loop without establishing glyph accuracy.
Batch19 also tested preassigning glyph-heavy BASIC crops to Tesseract. It avoided
retries in that run but badly corrupted adjacent code, requiring extensive manual
repair. Treat that exception as unproven: prefer separating graphic bands from
ordinary code where layout permits, and do not route code to Tesseract solely
because it contains a few graphic characters. Keep the same scan-linked markers
and bounded fallback policy for unresolved glyphs.
Reuse successful evidence only with unchanged source/crops and verified hashes,
and label mixed-engine provenance explicitly.

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


## Z-80 CPU control and interrupts, 2026-10-11

Batch10 restores PDF27–32/printed23–28 with Qwen:82 regions,75 text crops,
seven original diagrams and16 source-linked review flags. Sections4–5 include
RESET/WAIT/HALT timing, interrupt modes, vector bytes and daisy-chain priority.
The last summary point continues on33; the article remains partial pending33–38
and full assembly. Printed “25 MHz” beside “400 ns,” “M1” in a mode1 description,
“원쪽,” and a faint candidate “Retum” remain visible in the review record rather
than being silently repaired. Human acceptance is pending.

| Observation | Qwen CPU control / interrupts |
| --- | ---: |
| Raw stage including render/startup/export | 313.01s |
| Recognition calls, contained in raw stage | 281.76s |
| Correction and recording window | 491.75s |
| Corrected non-whitespace characters | 8,731 |
| Observed uncached, non-write correction input tokens | 208,143 |
| Observed cached correction input tokens | 2,287,744 |
| Observed correction output tokens | 13,186 |

Cache-write tokens were zero. Local Qwen46,025 tokens (38,192 prompt/7,833
completion) are separate. All75 inferences were fresh; no retries. Correction
includes exact source edits, joins and flags and overlaps raw inference by223.32s.
The raw-monitoring assistant window also includes development of the exact-edit
helper. These observed token counts include session/context overhead; they are
not a normalized OCR correction cost or evidence of paid-token savings. Export
completed before an interruption; its end is reconstructed from the completed
export-results file timestamp. The inactive gap is excluded from active windows.

| Fixed crop | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p27r02 — CPU control signals | 15.31% | 23.47% |
| p29r08 — interrupt introduction | 4.38% | 12.41% |
| p31r01 — IM2 peripheral/vector prose | 0.00% | 13.79% |
| p32r06 — EI/DI control prose | 0.56% | 11.86% |

Qwen's15 and6 edits in the first two samples are entirely missing U+0305 overbar
codepoints; the base text matches. Primary CER retains those meaningful notation
errors. The fourth crop has one corrected Korean character. References were sealed
before alternate OCR and are unblinded assistant readings, not independent human
gold. Tesseract used identical PNGs, kor+eng/OEM1/PSM6; no font tuning or second
paid correction. This favors Qwen raw accuracy in these samples while leaving the
paid-token/time tradeoff unresolved.

Native export integrity, UTF-8 review ranges and byte-identical rebuild pass.
Across ten checkpoints:35 source pages,519 regions,480 text crops,39 figures,
207 logical BASIC lines,1,071 physical hex rows and105 flags. Six bodies are
complete, one partial and29 untouched (30 unfinished). Next: Z-80 PDF33–38 and
full assembly. Reading room follows full issue restoration and metric consolidation.


## Z-80 final segment and complete assembly, 2026-10-11

Batch11/Qwen restores PDF33–38/printed29–34:67 text crops, nine numbered diagrams
and one editorial illustration across77 regions, with16 source-linked flags.
The text completes the interrupt summary, bus control, power/clock specifications,
example circuits and conclusion. Exact source corrections include 인터넷→인터럽트,
생각하겠다→생략하겠다, omitted signal overbars and wrapping. Printed 그림G/그림H,
CPM, OP 코드 패치 and historical electrical claims remain as printed. A small
repeated 핀/편 vowel candidate is explicitly flagged for human confirmation.

| Observation | Qwen final Z-80 segment |
| --- | ---: |
| Raw stage including render/startup/export | 160.07s |
| Recognition calls, contained in raw stage | 132.76s |
| Correction and recording window | 225.33s |
| Corrected non-whitespace characters | 5,862 |
| Observed uncached, non-write correction input tokens | 19,574 |
| Observed cached correction input tokens | 748,544 |
| Observed correction output tokens | 6,660 |

Cache-write tokens were zero. Local Qwen34,093 tokens (28,612 prompt/5,481
completion) remain separate. All67 inferences were fresh, with no retries. One
crop seam was rejected and moved to clear whitespace before inference. Correction
overlapped raw inference by100.93s. The raw-monitoring window includes comparison
helper preparation/API inspection; evaluation includes assembly-helper preparation.
Native export21.05s and assembly44.95s are separately recorded assistant windows.
These windows include tool waits and verification, not just computation.

| Fixed crop | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p33r09 — bus-control signals | 10.56% | 24.65% |
| p34r02 — power/clock specification prose | 0.00% | 24.14% |
| p36r01 — memory/address subscripts | 0.00% | 12.96% |
| p38r05 — refresh-register prose | 0.00% | 8.09% |

All15 Qwen edits in p33r09 are omitted U+0305 overbar codepoints; base text matches.
The other three match the assistant reference after whitespace removal. Source
errors such as CPM are preserved, so these scores measure transcription fidelity,
not technical correctness. References were sealed before Tesseract and remain
unblinded assistant readings, not human gold. Identical crops, kor+eng/OEM1/PSM6,
no font-specific tuning or repeated paid correction. The samples continue to favor
Qwen raw accuracy, without establishing a causal paid-token advantage.

The full Z-80 article is assembled from immutable09–11 across all18 pages21–38:
236 regions,26 original images (diagrams1–25 plus an illustration),46 review flags.
An explicit source-checked join completes the PDF32/33 summary sentence across
intervening diagrams14–16/captions. Original segment-level coverage flags remain
historical evidence; assembly coverage is complete. Native and assembled export
integrity, every projected review byte range and byte-identical rebuilds pass.
No source program or circuit is certified correct; human acceptance remains pending.

July now has seven complete bodies and29 untouched bodies, with no partial body.
Across11 checkpoints:41 distinct source pages,596 regions,547 text crops,49 figures,
207 logical BASIC lines,1,071 physical hex rows and121 flags. The next candidate
is 애플음의 정복, PDF42–50/printed38–46; confirm the actual body/advertisement
boundaries and content before mapping. Reading room follows full issue restoration
and metric consolidation.


## Apple sound opening and interruption recovery, 2026-10-11

Source inspection establishes the article extent as PDF42–49/printed38–45;
PDF50 is an advertisement. Batch12/Qwen restores42–45:49 regions,44 text crops,
five original images, seven BASIC lines and58 addressed assembly rows in program
tables1–5. Twelve source-linked flags preserve printed CALL-1511, an extra closing
parenthesis, the S-like address prefix, uncertain punctuation and a margin mark.
Circled two-digit flowchart steps are explicitly linearized as parenthesized numbers.
The last paragraph continues onto46; full article assembly remains pending.

| Observation | Qwen Apple sound opening |
| --- | ---: |
| Combined raw-stage elapsed | Exact value unknown;161.77–283.81s bounds |
| Completed recognition calls | 132.66s; incomplete call excluded |
| Correction, recovery and recording window | 351.17s |
| Corrected non-whitespace characters | 3,601 |
| Observed uncached, non-write correction input tokens | 21,392 |
| Observed cached correction input tokens | 1,797,504 |
| Observed correction output tokens | 8,913 |

The first worker exited143 after30 completed crops and one incomplete request;
no live worker remained. Cause and exact stop time are unknown. Its output is
preserved separately. A fresh recovery directory reused only hash-verified complete
stages and finished14 remaining crops in56.13s, with no completed inference rerun.
The lower raw bound uses the last completed stage timestamp; the upper uses terminal
observation, each plus measured resume duration. Observation delay is included in
the upper bound, recovery preparation excluded. Public `raw_run_seconds` is null
rather than presenting either bound as an exact measurement. Interrupted inference
time and local tokens are unknown; the recorded22,498 local tokens (18,805 prompt,
3,693 completion) cover successful calls only. Assistant cache-write tokens were zero.

Correction time includes failure inspection, recovery, waits, source proofreading
and artifact writing; raw work overlapped it, but the exact overlap is unknown.
Comparison-helper preparation is separately visible in the raw assistant window.
A code crop boundary was adjusted before inference to avoid splitting address031C.
These measurements remain observations, not isolated engine correction costs.

| Fixed crop | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p43r02 — introduction prose | 0.00% | 3.59% |
| p43r13 — BASIC/ROM prose | 0.00% | 4.76% |
| p43r18 — bell disassembly | 4.23% | 40.85% |
| p45r07 — music disassembly | 8.04% | 25.00% |

Qwen still required correction of hexadecimal0/O and operand $/# glyphs; its raw
code was not perfect. The larger differences on code than prose support the
provisional content rule without proving paid-token savings. References were sealed
before alternate OCR, are Qwen-derived and unblinded, and are not human gold.
Tesseract used identical PNGs, eng for code and kor+eng for prose, OEM1/PSM6,
without font-specific tuning. No second paid correction was performed.

Native export integrity, source-linked UTF-8 review ranges, printed BASIC line
numbers,58 source-address identities and byte-identical rebuild pass. None of these
checks certifies executable behavior. July has seven complete bodies, one partial
and28 untouched (29 unfinished). Across12 checkpoints:45 source pages,645 regions,
591 text crops,54 figures,214 logical BASIC lines,1,071 physical hex rows,
58 assembly rows and133 flags. Next restore46–49, including the music-note table,
then assemble the article. Full-issue metric consolidation and reading room follow
completion of the remaining bodies; human review remains mandatory.


## Apple sound conclusion and complete assembly, 2026-10-11

Batch13 restores PDF46–49:67 regions,65 text crops, two original images,
90 logical BASIC lines,26 assembly rows and20 review flags. The music table
contains72 checked numeric values. Its24 note/rest symbols remain in a source
image; names in the caption are explicitly editorial descriptions. Printed
anomalies such as duplicate line50, `POKE 6.K`, `MI PA SOL` and `SVAE` remain
flagged rather than repaired. Uncertain `94.RR` and `100 DATA 0.0` retain scan links.

| Observation | Qwen Apple sound conclusion |
| --- | ---: |
| Raw elapsed, both attempts | 487.29s |
| Successful recognition, including repeated crops | 309.52s |
| Failed call server compute, separate timer basis | 123.20s |
| Correction/recovery/recording window | 738.71s |
| Corrected non-whitespace characters | 6,742 |
| Uncached, non-write correction input tokens | 34,096 |
| Cached correction input tokens | 4,158,848 |
| Correction output tokens | 17,370 |

The first attempt completed22 crops, then the music-symbol band repeated until
its4,096-token response limit. All failure evidence is retained. That band was
rerouted to an original image. The changed map required a fresh65-crop run;
22 successful raw crops were therefore repeated, with no duplicate paid correction.
Combined local usage is53,376 tokens (40,658 prompt;12,718 completion), including
the failed response. Final-attempt-only usage is38,357 tokens and recognition247.00s.
The raw sum includes both startups and failure, but excludes rerouting between
attempts. Failed server compute is not added to the client recognition timer.
Raw work overlaps the correction window by419.66s; those times must not be summed
as sequential elapsed. Correction includes recovery work; cache-write tokens zero.

| Fixed crop | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p46r06 — BASIC bird-sound DATA | 1.15% | 2.87% |
| p47r02 — numeric pitch table | 0.00% | 80.00% |
| p47r12 — assembly | 1.16% | 29.07% |
| p49r08 — pointer prose | 0.99% | 12.32% |

References were sealed before alternate inference, remain Qwen-derived/unblinded,
and are not human gold. Identical PNGs used Tesseract OEM1/PSM6, eng for code and
kor+eng otherwise. Row-specific segmentation could improve the table baseline;
80% is not a general table estimate. Compact CER ignores whitespace/delimiters
and excludes editorial glyph descriptions. These samples support the provisional
raw-quality rule but establish neither paid savings nor whole-article accuracy.

Full Apple sound assembly now covers42–49:116 regions, seven image assets,
18 listing groups,97 logical BASIC lines,84 assembly rows,222 physical listing
rows and32 review flags. The45/46 sentence is explicitly joined. Assembly exposed
a private export-helper metadata mismatch for wrapped rows; corrected metadata
and rebuilt batch13 preserve the exact article/listing text. The original
pre-fix output remains available locally. Final segment and assembly integrity,
UTF-8 review ranges, source listing bytes and byte-identical rebuilds pass.
Assembly diagnosis/re-export is in reporting overhead, not correction usage.
No program execution or human acceptance is claimed.

July now has eight complete bodies, zero partial and28 untouched. Across13
checkpoints:49 source pages,712 regions,656 text crops,56 images,304 logical BASIC
lines,1,071 hex rows,84 assembly rows and153 flags. Six unpaginated headings remain
separate. Next inspect 컴퓨터반란군 진압대, candidate PDF56–58, before confirming
its route. Full-issue metric consolidation and reading room follow restoration.


## FC-100 rebellion game and mixed fallback, 2026-10-11

Batch14 restores the complete 컴퓨터반란군 진압대 article, PDF56–58/printed52–54.
It has50 mapped regions,49 text crops, one original screen image,170 numbered BASIC
lines across195 physical listing rows,112 hexadecimal DATA values and21 review
flags. Source59 starts the next article. Introduction, variables, explanation and
listing follow their actual cross-column reading order.

Qwen was assigned before inference because code dominates the article. After44
successful crops, p58r08 repeated graphic brackets until the4,096-token limit.
The failed request/response remain intact. Recovery copied44 verified Qwen stages
without repeating inference, completed four remaining Qwen crops, and used
Tesseract eng/OEM1/PSM6 on the failed crop. The mixed evidence retains each engine's
native response/settings and original scan. No second paid correction occurred.
The Tesseract fallback ended the loop; it did not reliably decode graphic literals.

`⟦G⟧` explicitly marks an unresolved FC-100 graphic run in eight source-linked
regions. It is editorial notation, not a program token or a promise of exact glyph
count/byte encoding. Readable numeric labels, English strings and the printed
credit “Programer : Jang Chang Soo.” are preserved. Line4010's missing T, several
absent closing quotes, the missing separator before NEXT in2190, and ambiguous
quote punctuation in8070 remain flagged. Wider source-column checks distinguish
printed omissions from crop clipping. Programs have not been executed or repaired.

A separate successful Qwen response for p58r11 contained only the first physical
continuation line, omitting all nine numbered lines9010–10040. Source proofreading
restored those rows. Thus completion status and fast inference do not establish
coverage. This omission was outside the four preselected comparison crops and is
reported separately rather than concealed by their favorable scores.

| Observation | Qwen primary, one Tesseract fallback |
| --- | ---: |
| Raw elapsed, first attempt plus recovery | 328.45s |
| Successful unique Qwen recognition | 182.24s |
| Failed Qwen server compute, separate timer basis | 125.43s |
| Tesseract fallback recognition | 0.15s |
| Correction/recovery/helper/recording window | 490.10s |
| Corrected non-whitespace characters, including editorial markers | 5,993 |
| Uncached, non-write correction input tokens | 56,553 |
| Cached correction input tokens | 2,055,424 |
| Correction output tokens | 14,224 |

Local Qwen usage33,544 tokens includes the failed response (24,269 prompt;
9,275 completion). Cache copies are counted once. The raw sum covers startup,
inference/failure and evidence export, excluding preparation between attempts.
Recognition and raw timers overlap and must not be added. Failed server compute
has a different measurement basis. Raw/correction overlap is292.12s. The correction
window includes mixed-recovery helper implementation and source coverage repair;
it is not isolated engine correction cost. Assistant cache-write tokens were zero.

| Fixed crop | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p56r04 — introduction | 0.00% | 10.34% |
| p57r16 — coordinate-check BASIC | 0.37% | 24.34% |
| p58r03 — key-check BASIC | 1.58% | 35.57% |
| p58r12 — hexadecimal DATA | 0.00% | 20.69% |

All four crops used identical PNGs and source-checked references sealed before
alternate inference. They exclude graphic placeholders and the omitted-row crop.
References remain unblinded assistant readings, not independent human gold;
compact CER is not a whole-article, layout, executable-code or paid-savings score.

Native export integrity, source-linked review byte ranges, explicit printed line
identities, listing byte coverage and byte-identical rebuild pass. July now has
nine complete bodies and27 untouched, with no partial bodies and zero human
acceptances. Cumulative checkpoints cover52 source pages,762 regions,705 text
crops,57 images,474 BASIC lines,1,071 hex rows,84 assembly rows and174 flags.
Next inspect 육감개발 2주 완성, candidate PDF59–61; choose its route after checking
remaining pages. Full issue restoration, consolidated metrics and the reading-room
preview remain outstanding.


## Sixth-sense game with planned content routing, 2026-10-11

Batch15 restores complete 육감개발 2주 완성, PDF59–61/printed55–57. The article
has30 text regions,97 logical/physical BASIC rows and11 source-linked review flags.
PDF62 begins the next article. Prose continues59 left/right into60; variables and
explanation precede the listing on60–61. One code-crop seam was moved before OCR
to avoid cutting line360; all final physical rows were inspected.

Assignments were fixed before inference:10 clear prose/byline regions to Tesseract,
20 title/variable/explanation/code regions to Qwen. This is a planned mixed route,
not an opportunistic choice of the cleaner draft. Both engines retain native
settings and responses with identical source-map provenance. No retry or fallback
was needed. Source PROGARM spelling, historical Korean wording, probability claims
and algorithm statements remain unchanged; no program execution is claimed.

Two successful Qwen responses were incomplete: p60r12 omitted the tail of150,
and p61r04 omitted the tail of710 plus all nine rows720–800. Those were restored
from source. The complete97-row count checks physical content, not just returned
status or apparently well-formed text. The omissions are outside the four fixed
comparison crops and remain explicitly reported.

| Observation | Planned mixed route |
| --- | ---: |
| Raw elapsed, including render/startup/export | 72.36s |
| Tesseract recognition,10 regions | 2.96s |
| Qwen recognition,20 regions | 57.03s |
| Correction/coverage checking/recording window | 176.10s |
| Corrected non-whitespace characters | 3,028 |
| Uncached, non-write correction input tokens | 17,475 |
| Cached correction input tokens | 681,472 |
| Correction output tokens | 5,479 |

Qwen raw usage11,623 tokens (10,155 prompt;1,468 completion) is separate from paid
assistant usage. Cache-write tokens were zero. Raw work overlaps correction by
37.87s; do not add these windows as sequential elapsed. Preparation includes the
private mixed-run helper; comparison-helper preparation is in the raw assistant
window. Correction usage covers both engines together and cannot establish their
individual causal cost or a saving versus running this article with one engine.

| Preselected crop and primary | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p59r03 — introductory prose, Tesseract | 0.60% | 6.55% |
| p59r07 — strategy prose, Tesseract | 1.40% | 2.10% |
| p60r14 — BASIC instructions, Qwen | 0.00% | 2.86% |
| p61r03 — BASIC prediction logic, Qwen | 0.00% | 6.11% |

Each alternate ran only after the primary draft's source-checked reference was
sealed. References are unblinded assistant readings, not human gold. Tesseract
used kor+eng for prose and eng for code, OEM1/PSM6; identical PNGs were compared.
These clean code samples show a smaller gap than the preceding graphic-heavy game.
They support continued content-specific testing, not a blanket paid-cost ranking.
Compact CER excludes whitespace and is not a whole-article accuracy estimate.

Export integrity, review UTF-8 ranges, explicit printed row identities and
byte-identical rebuild pass. July now has10 complete bodies and26 untouched,
with no partial bodies and zero human acceptances. Cumulative coverage:55 source
pages,792 regions,735 text crops,57 images,571 BASIC lines,1,071 hex rows,
84 assembly rows and185 flags. Next inspect 디오디지이엠, candidate PDF62–67.
Full restoration, consolidated metrics and the reading room remain outstanding.


## Dodgem game with interruption recovery, 2026-10-11

Batch16 completes 디오디지이엠, PDF62–67/printed58–63:39 text regions,
307 logical/physical BASIC rows and19 source-linked review flags. The boxed
advertisement on63 is excluded; PDF68 begins the already-restored 합이15 article.
Assignments were fixed before OCR:5 clear prose/byline crops to Tesseract,
34 headline/code crops to Qwen. Both engines retain native evidence.

The raw process terminated with exit143 after29 completed Qwen calls; its cause
is unknown. All29 stages passed their hash checks and were reused, as were all5
Tesseract outputs. The interrupted p67r03 request remains preserved separately;
five remaining Qwen calls completed in the resumed run. No completed inference
was repeated. The original Tesseract timers existed only in process memory and
were lost; they remain null. Future mixed runs should persist each timer as soon
as its crop finishes.

| Observation | Planned mixed route |
| --- | ---: |
| Raw elapsed bounds, original attempt plus resume | 196.14–405.53s |
| Measured resume, including startup/evidence export | 31.23s |
| Completed Qwen recognition,34 regions | 167.84s |
| Tesseract recognition,5 reused regions | Unknown |
| Correction/recovery window | 458.21s |
| Corrected non-whitespace characters | 6,593 |
| Uncached, non-write correction input tokens | 80,418 |
| Cached correction input tokens | 1,922,560 |
| Correction output tokens | 12,735 |

The raw bounds use original start to last completed stage / terminal observation,
plus measured resume. The upper bound includes observation delay; exact interrupted
inference time and tokens are unavailable. The correction window also includes
recovery/helper preparation and possible interruption delay, so it is not pure
proofreading time or a clean speed comparison. Raw execution overlaps correction;
do not add those windows as sequential time. Paid usage covers the mixed workflow
jointly. Cache-write tokens were zero. Completed Qwen calls used31,824 local tokens
(27,262 prompt;4,562 completion); this excludes unknown interrupted-call usage and
is separate from paid assistant usage. No per-engine paid savings are established.

Two successful Qwen responses silently omitted content: p62r07 lost the end of1060
and all1070; p66r03 lost the end of2950 and all2960–3040. All ten whole rows and two
partial tails were restored from the scan. Every printed row was checked against
source, including the printed absence of3950. Source F$/F, P(J,1), missing closing
quotes, PICES/DIGITA/AVOBE/OBLECT/NOR THERN/FORFET/RESOGN remain unchanged.
Ambiguous L0/LO and BO/B0 glyphs and literal padding carry review flags; the
listing has not been executed or repaired for runtime behavior.

| Preselected crop and primary | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p62r03 — introductory prose, Tesseract | 0.00% | 8.40% |
| p64r03 — BASIC neighbor checks, Qwen | 0.00% | 3.16% |
| p65r05 — BASIC movement logic, Qwen | 0.00% | 3.41% |
| p67r02 — BASIC compass instructions, Qwen | 0.00% | 10.27% |

[Comparison14](ocr-july-comparison-14.json) uses identical PNGs and references
sealed before alternate OCR. References are unblinded assistant source readings,
not independent human gold. Compact CER ignores whitespace, including code
literal padding. These samples exclude the omitted crops and cannot establish
whole-article accuracy. Their favorable Qwen scores support continued testing of
the provisional rule alongside explicit coverage checks.

Export integrity, source-linked review ranges, all307 line identities and
byte-identical rebuild pass. July now has11 complete bodies, no partial bodies,
and25 untouched; all human acceptances remain pending. Cumulative coverage:
61 source pages,831 regions,774 text crops,57 images,878 BASIC lines,
1,071 hex rows,84 assembly rows and204 flags. Next inspect 위기일발,
candidate PDF70–72, with page73 checked for the boundary. Full issue restoration,
metric consolidation and the reading room remain outstanding.


## Faint Apple listing and decimal DATA, 2026-10-11

Batch17 completes 위기일발, PDF70–72/printed66–68. The article contains45 regions:
44 text crops and1 retained opening image. Its listing has127 logical BASIC lines
across231 physical rows, including line660 continuing from71 to72. Page73 starts
화성인 디거. All line identities and physical continuations were checked against
the source; the exported listing retains the printed wraps.

The route was fixed before OCR:5 clear introductory prose/byline crops to Tesseract;
39 title, technical explanation, variable-definition and faint code/DATA crops to
Qwen. Recognition timers are now saved immediately after each crop, so a later
interruption will not erase completed timings. This run needed no retries or
fallback. The two engines retain their native evidence, settings and source map.

| Observation | Planned mixed route |
| --- | ---: |
| Raw elapsed, including render/startup/export | 190.48s |
| Tesseract recognition,5 regions | 1.33s |
| Qwen recognition,39 regions | 168.12s |
| Correction/source review/helper window | 396.10s |
| Corrected non-whitespace characters | 5,633 |
| Uncached, non-write correction input tokens | 32,098 |
| Cached correction input tokens | 1,465,600 |
| Correction output tokens | 10,149 |

Raw execution overlaps correction by176.30s; these times must not be added as
sequential elapsed. Correction includes source DATA inspection, wrapped-row
tracking, prose/list joining and helper adaptation, not just proofreading.
Cache-write tokens were zero. Local Qwen usage was23,275 tokens (18,341 prompt;
4,934 completion), separate from paid assistant usage. The shared correction
window cannot establish which engine caused a given paid cost or a saving.

Qwen omitted a single-character continuation completing the final11 in DATA1130;
source review restored it. It also inserted a duplicate parenthesis around a wrap
and read the printed31779 address as31979. Those OCR errors were corrected.
Apparent source anomalies remain: the explanation says DATA starts1230 although
the listing starts1130; the variable list includes KT/V.M; faint separators and
GOTC require human review. The24 DATA lines retain379 literal comma-separated
fields, including trailing21- in1140 and decimal-like1.2 in1360. This is a
transcription audit, not a validated executable or reconstructed binary.

| Preselected crop and primary | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p70r04 — clear opening prose, Tesseract | 0.00% | 2.06% |
| p71r05 — variable definitions, Qwen | 0.00% | 21.43% |
| p71r12 — faint wrapped BASIC, Qwen | 0.00% | 67.38% |
| p72r13 — decimal DATA, Qwen | 0.00% | 14.41% |

[Comparison15](ocr-july-comparison-15.json) uses identical PNGs and references
sealed before alternate OCR. The faint BASIC sample shows a much larger raw gap
than the clear prose, consistent with continuing this content route. References
remain unblinded assistant readings, including flagged source ambiguities. The
sample excludes the omitted1130 continuation. Compact CER ignores whitespace,
so these scores are neither whole-article accuracy nor proof of paid-token savings.

Export integrity, UTF-8 review ranges, continuation coverage and byte-identical
rebuild pass. July now has12 complete bodies and24 untouched, with no partial
bodies and zero human acceptances. Cumulative coverage:64 source pages,876 regions,
818 text crops,58 images,1,005 BASIC lines,1,071 hex rows,84 assembly rows and224
flags. Next inspect the remainder of 화성인 디거, candidate73–77, with78 checked
for the boundary. Full restoration, consolidated metrics and reading room remain.


## Digger BASIC and hexadecimal listing, 2026-10-11

Batch18 completes 화성인 디거, PDF73–77/printed69–73. Its58 regions contain57
text crops and1 retained opening artwork; the separate advertisement on77 is
excluded. Page78 begins 보트 탐험. The listing has141 logical BASIC lines across
383 physical BASIC rows,2 monitor-command rows and36 hex rows containing288 byte
fields. Physical counts retain code continuations and an explicit blank literal
wrap, while vertical gaps between separate BASIC lines are normalized. Decimal
DATA40 has21 fields; long melody strings were compared with their printed rows.

Assignments were recorded before OCR:7 clear prose/byline crops to Tesseract;
50 titles, keyboard-symbol text, technical explanations, BASIC and hex crops to
Qwen. Both engines retain native evidence. Boxed arrow keys are represented as
[←]/[→] in searchable prose, with that editorial notation explicitly flagged.

Two processes terminated with exit143. The cause remains unknown; llama-server
logs show cancelled active requests, not a diagnosed model failure. After each
terminal status was verified, completed stages were checked and reused:5 on the
first resume,9 on the final resume. All7 Tesseract outputs and their immediately
persisted timers survived. Two interrupted requests remain archived separately.
The final attached-terminal run completed41 remaining Qwen calls. No completed
inference was repeated, and the transport change alone does not establish a cause.

| Observation | Planned mixed route |
| --- | ---: |
| Raw elapsed bounds across three attempts | 285.22–489.62s |
| Measured final resume, including startup/export | 228.38s |
| Completed Tesseract recognition,7 regions | 1.68s |
| Completed Qwen recognition,50 regions | 252.73s |
| Correction/recovery/source review/helper window | 855.57s |
| Corrected non-whitespace characters | 8,650 |
| Uncached, non-write correction input tokens | 59,909 |
| Cached correction input tokens | 3,865,856 |
| Correction output tokens | 21,970 |

The lower raw bound sums the original start through its last completed crop,
the first resume's ready-runtime timestamp through its last completed crop, and
the measured final resume. The upper bound also includes observation/recovery
gaps. Exact interrupted-call time and tokens are unknown. Completed local Qwen
usage was34,133 tokens (26,597 prompt;7,536 completion), excluding those unknown
interrupted costs and separate from paid assistant usage. Cache-write was zero.
Raw work overlaps correction, whose window includes both recovery helpers and
source review. These interruption-affected times cannot rank engine speed or
isolate causal paid savings.

A successful Qwen response returned only the opening continuation of p76r02,
omitting all five BASIC lines760–800. Another omitted the wrapped0 completing940.
Both were restored from the scan. Source line700 has a white damaged band: its
unreadable span is explicitly marked [ILLEGIBLE], not reconstructed from neighboring
logic. Original998 numbering, COMMING spelling, damaged punctuation and uncertain
literal padding remain flagged. The printed monitor range ends401F while the dump
continues through411F; both are retained. Hex review corrected addresses and bytes,
including an extra raw byte in40B0; faint readings remain provisional. No executable
or binary certification is claimed.

| Preselected crop and primary | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p73r04 — introductory prose, Tesseract | 0.00% | 10.20% |
| p74r07 — BASIC decimal DATA/music routine, Qwen | 0.00% | 23.53% |
| p75r09 — BASIC enemy movement, Qwen | 0.00% | 13.86% |
| p77r05 — faint hexadecimal rows, Qwen | 3.17% | 93.65% |

[Comparison16](ocr-july-comparison-16.json) uses identical PNGs, with references
sealed before alternate OCR. The source readings are unblinded and include flagged
ambiguities, not independent human gold. Fixed samples exclude damaged700 and the
silent five-line omission. Compact CER ignores whitespace. The raw gap supports
continued Qwen trials on faint technical listings, while these samples cannot
establish whole-article accuracy or paid-token savings.

Export integrity, all listing/review ranges, explicit row identities and
byte-identical rebuild pass. July now has13 complete bodies and23 untouched,
with no partial bodies and zero human acceptances. Cumulative coverage:69 source
pages,934 regions,875 text crops,59 images,1,146 BASIC lines,1,107 hex rows,
84 assembly rows and250 review flags. Next inspect79–81 to complete the extent
check for 보트 탐험, whose opening78 is confirmed. Full issue restoration,
consolidated metrics and the reading room remain outstanding.


## Boat exploration and the graphic-code exception, 2026-10-11

Batch19 completes 보트 탐험, PDF78–80/printed74–76:43 regions,42 text crops and
one original screen image. The advertisement on80 is excluded;81 begins 캥거루.
The listing contains87 logical BASIC lines across166 physical rows, including
wrapped graphic strings. Seven hexadecimal DATA lines have84 fields in total.
There are24 source-linked review flags; human acceptance remains pending.

Before inference,17 crops were assigned to Tesseract (clear prose/byline plus
14 graphic-heavy BASIC crops),25 to Qwen (titles, technical notes, ordinary code
and DATA). Code Tesseract calls used eng; prose used kor+eng. This graphic-code
exception was intended to avoid the repetition seen in earlier Qwen runs. It
completed without retries, but Tesseract severely corrupted adjacent BASIC.
Source correction repaired those statements. This does not establish an efficient
exception, and the heuristic now records that counter-evidence.

| Observation | Planned mixed route |
| --- | ---: |
| Raw elapsed, including rendering/startup/export | 87.10s |
| Tesseract recognition,17 regions | 2.53s |
| Qwen recognition,25 regions | 68.58s |
| Correction/source review/helper window | 270.59s |
| Raw overlap with correction | 74.23s |
| Corrected non-whitespace characters | 4,707 |
| Uncached, non-write correction input tokens | 32,192 |
| Cached correction input tokens | 570,624 |
| Correction output tokens | 8,876 |

Cache-write was zero. Completed local Qwen usage was13,237 tokens (11,006 prompt;
2,231 completion), separate from paid assistant usage. Elapsed windows include
source checking, helper work and tool waits; overlapping raw time must not be
added again. Mixed correction cannot attribute paid usage causally to either
engine. Character counts include editorial markers and do not measure encoded
program size.

Qwen omitted the numbered comment framework0–4, flattened3110–3130 into a single
row and misread1540/1550 as1548/1558,50 as58, and10 as18. These were restored from
the source. Each ⟦G⟧ denotes a graphic glyph or run whose exact characters/bytes
remain unresolved, with the original crop preserved. One faint character in the
line2200 sound string is marked [ILLEGIBLE]. Source STAT and DANGAR spellings,
faint3/8 readings, music punctuation and uncertain padding remain flagged. No
execution or byte-faithful glyph reconstruction is claimed.

| Preselected crop and primary | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p78r04 — introductory prose, Tesseract | 0.00% | 7.69% |
| p78r09 — variable definitions, Qwen | 0.00% | 9.89% |
| p79r17 — hexadecimal DATA, Qwen | 0.00% | 34.09% |
| p79r07 — ordinary BASIC, Qwen | 0.00% | 31.07% |

[Comparison17](ocr-july-comparison-17.json) uses identical PNGs and references
sealed before alternate OCR. References are unblinded assistant readings, not
independent human gold. Samples deliberately exclude graphic markers and do not
include the omitted header or faint final-page errors. Compact CER ignores
whitespace; zero on these crops is not whole-article accuracy. The samples favor
Qwen for ordinary code but do not test the graphic-heavy routing exception or
prove paid-token savings.

Export integrity, listing/review byte ranges, explicit row identities and a
byte-identical rebuild pass. July now has14 complete bodies and22 untouched,
with no partial bodies and zero human acceptances. Cumulative coverage:72 source
pages,977 regions,917 text crops,60 images,1,233 BASIC lines,1,107 hex rows,
84 assembly rows and274 review flags. Next inspect 캥거루, candidate81–86;
87 is the previously restored 운전 연습. Full issue restoration, consolidated
metrics and the reading room remain outstanding.
