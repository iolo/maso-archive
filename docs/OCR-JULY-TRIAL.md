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
| Faint, degraded, mottled-background or unusually styled text | Qwen candidate | Consider scan quality as well as content. Batch24 gray-background prose needed substantial Tesseract repair; its fixed prose sample scored Qwen0% versus Tesseract10% compact CER. One sample supports a trial, not a universal rule or paid-cost claim. |
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
Thin opcode/flag-table rows need particular caution: batch27 produced two Qwen
length-limit loops on stacked opcode rows. Preserve the complete table image,
stop repeating failed calls, and use a recorded Tesseract fallback for the affected
row or remaining homogeneous rows. Check every flag and opcode cell against the
scan; Tesseract also corrupts these symbols. This is a provisional exception, not
a reversal of the numeric-table starting choice or evidence of paid savings.
Batch28 extends the caution to a small ruled color table: Qwen repeated escaped
tabs until the output limit. Use the bounded Tesseract probe before committing
a group of ruled tables to Qwen, even when the values are simple. Preserve failed
responses and record any route change; the observed failure does not identify its
cause or prove Tesseract more economical after correction. Non-ruled BASIC DATA
and formula samples still favor Qwen in this checkpoint.
Batch29 exercised that probe rule: compiler identifiers/punctuation were badly
corrupted by Tesseract, so the compiler group used Qwen; two ruled numeric-output
tables used English Tesseract after a usable probe. Check every number regardless
of engine. Qwen won the fixed numeric sample too, so this route remains a cost
hypothesis, not an accuracy win. Compiler line counters, offsets and statements
need explicit row association; Qwen separated them despite legible characters.
Batch30 also shows that visually clear ruled headlines may yield blank or fragmented
Tesseract output while nearby body text remains usable. Check headline presence
as well as body coverage; never accept an empty headline as an empty source.
Source-read a short isolated failure, or use a bounded Qwen probe before routing
a new group with that style. The four fixed batch30 samples favor Qwen, including
ordinary news and the reused Tesseract table probe; usability remains a paid-cost
hypothesis rather than an accuracy ranking.
For repeated numeric/CHR$ expressions, check every printed term as well as row
coverage: batch20 Qwen shortened many repetitions while returning successful
responses. Use field counts as an audit, never as permission to invent missing
values. Preserve source anomalies and unresolved glyph encoding.
For aligned address/opcode/mnemonic columns, check row association explicitly.
Batch21 Qwen separated the columns into successive text blocks, while the fixed
Tesseract alternate preserved row order better. Consider the existing bounded
Tesseract probe for this layout; one crop does not establish a universal assembly
route. Also compare technical headings and circled labels literally: plausible
normalization can conceal source errors (batch21 changed printed1482 to1462).
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


## Kangaroo graphics and repeated character definitions, 2026-10-11

Batch20 completes 캥거루, PDF81–86/printed77–82. Its79 regions contain78 text
crops and one original screen; the advertisement on82 is excluded, and87 starts
the previously restored 운전 연습. The listing contains246 logical BASIC lines
and556 physical text/glyph rows. Two numeric DATA lines contain45 fields each;
35 character definitions contain12 hexadecimal fields each,420 in total. These
counts were checked after source transcription; no missing values were generated
from expected counts. Large sprite/title drawings use approximate printed-grid
rows with scan-linked markers, not exact byte or cell-spacing reconstruction.

Assignments were fixed before inference:4 Tesseract prose/byline crops and74
Qwen title/technical/code crops. Unlike batch19, graphic-bearing code remained
with Qwen. No repetition loop or process interruption occurred. Inspection found
that the left edge of the page83 right-column crops trimmed some leading numerals.
All seven were widened from427 to420/849 and rerun;67 unchanged Qwen results and
all4 Tesseract results were reused. The complete original OCR and original map
remain archived. Fixed evaluation crops were unchanged, and all81 completed Qwen
calls are included in accounting. This deliberate crop repair is not free reuse.

| Observation | Planned mixed route, including crop repair |
| --- | ---: |
| Original raw worker elapsed | 349.27s |
| Changed-crop rerun worker elapsed | 43.30s |
| Total measured raw worker elapsed | 392.56s |
| Tesseract recognition,4 calls | 1.02s |
| Qwen recognition,81 calls | 354.51s |
| Correction/source review/crop-repair/helper window | 739.79s |
| Raw overlap with correction | 371.43s |
| Corrected non-whitespace characters | 14,071 |
| Uncached, non-write correction input tokens | 76,443 |
| Cached correction input tokens | 2,871,936 |
| Correction output tokens | 22,452 |

Cache-write was zero. Local Qwen usage across both crop versions was53,453 tokens
(42,274 prompt;11,179 completion), separate from paid assistant usage and alternate
OCR. Raw elapsed is the sum of two measured worker runs, excluding the intervening
inspection/preparation gap. Correction includes that work and overlaps both raw
runs; do not add the elapsed columns. This mixed observation does not isolate a
causal engine cost. Its substantially larger listing and repeated-field review
also prevent a direct speed ranking against the shorter preceding article.

Successful Qwen responses omitted the430 tail and440–490, the960 tail and
970/1000/1010 even after widening, and the11012 tail plus11013. Source review
restored them. Many long CHR$ expressions lost repeated terms; source checks also
corrected numeric substitutions, format hashes and music-string truncation.
The raw model sometimes rendered printed sprites as emoji or invented ASCII
shapes. Those are replaced with explicit ⟦G⟧ markers linked to the original scan.

Source anomalies remain visible: the explanatory range870–1111 differs from
listing1110;100 lacks a visible comment token; some strings appear unclosed;
10210 contains a dot after HE0); and SRART remains printed in11009. Faint3/8,
O/0, music punctuation, graphic encoding and literal padding remain among55
review flags. No program execution, reconstructed sprite bytes, or human
acceptance is claimed.

| Preselected crop and primary | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p81r03 — introductory prose, Tesseract | 0.82% | 18.85% |
| p81r07 — variable definitions, Qwen | 0.00% | 36.47% |
| p82r07 — numeric DATA, Qwen | 0.42% | 35.42% |
| p85r09 — hexadecimal CHR$ expressions, Qwen | 0.00% | 42.61% |

[Comparison18](ocr-july-comparison-18.json) uses identical PNGs, with source-checked
references sealed before alternate OCR. References remain unblinded assistant
readings. The fixed sample set excludes graphic-marker crops and the main
omission cases; it cannot establish whole-article accuracy or paid savings.
Compact CER ignores whitespace and is not executable-code validation. The raw
quality gap supports continued Qwen trials on technical text, alongside explicit
checks for omitted repeated terms.

Export integrity, review/listing UTF-8 ranges, source line identities and a
byte-identical rebuild pass. July now has15 complete bodies and21 untouched,
no partial bodies and zero human acceptances. Cumulative coverage:78 source pages,
1,056 regions,995 text crops,61 images,1,479 BASIC lines,1,107 hex rows,
84 assembly rows and329 review flags. Next inspect SPC-1000 자동실행 테이프의 제작,
candidate88–93, and boundary94. Full issue restoration, consolidated decision
metrics and the reading room remain outstanding.


## SPC-1000 automatic tape article, 2026-10-11

Batch21 completes SPC-1000 자동실행 테이프의 제작, PDF88–92/printed84–88.
Page93 is the next section divider;94 starts 로고강좌. The104 mapped regions
contain99 text crops and five original diagrams/screens. Four small tables use
tab-separated cells. Listings contain5 numbered BASIC rows,13 hex rows with104
byte fields,13 assembly rows and2 before/after patch rows. These are source
transcriptions, not executed or certified binaries;21 flags await human review.

The preassigned route used20 Tesseract prose/caption crops and79 Qwen technical,
title and code crops. All completed without retry, fallback or changed crops.

| Observation | Planned mixed route |
| --- | ---: |
| Raw worker elapsed, including setup/render/export | 234.73s |
| Tesseract recognition,20 calls | 2.51s |
| Qwen recognition,79 calls | 205.35s |
| Correction/source review/helper window | 446.36s |
| Raw overlap with correction | 198.12s |
| Corrected non-whitespace characters | 6,062 |
| Uncached, non-write correction input tokens | 64,113 |
| Cached correction input tokens | 1,009,920 |
| Correction output tokens | 15,089 |

Cache-write was zero. Local Qwen usage was37,874 tokens (32,066 prompt;5,808
completion), separate from paid assistant usage and alternate evaluation. Correction
includes table/label review, assembly-column reconstruction, context recovery and
helper work. Recognition is nested within raw time, and raw overlaps correction;
do not sum these elapsed columns. This mixed run cannot isolate paid savings by
engine or establish a speed ranking across different article types.

Source comparison caught plausible normalization as well as ordinary errors.
The source heading prints `$1482`, while the body uses `$1462`; Qwen changed the
heading to1462. The printed `C1` mode value, figure7 metadata differing from the
procedure, `$H15C3`, repeated step9 and the `G0024` load instruction remain in the
restoration. In the latter case the diagram/summary instead use `G002A`. These
are source review issues, not permission to repair the historical instructions.

Qwen confused circled A/B/C/D with numbers and changed the intended A/B/D tape
selection. It split assembly address/opcode and mnemonic columns into separate
runs and misplaced annotation labels. The corrected draft restores row association
and labels; bracket geometry remains in the original crops. Hex139E zeros and
A8 were source-restored. Music O/0 and literal spacing remain reviewable.

| Preselected crop and primary | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p88r04 — clear prose, Tesseract | 1.28% | 0.00% |
| p89r05 — numeric table, Qwen | 0.00% | 38.89% |
| p91r08 — hex dump, Qwen | 0.63% | 11.25% |
| p91r10 — assembly columns, Qwen | 65.52% | 13.79% |

[Comparison19](ocr-july-comparison-19.json) keeps the four preselected identical
PNGs and seals references before alternate OCR. References remain unblinded
assistant readings. The assembly score is dominated by reading order, with
editorially linearized bracket labels also affecting comparison. Compact CER
ignores whitespace; it is neither layout fidelity nor executable-code validation.
This is useful counterevidence to a blanket Qwen-for-code assumption, while still
supporting its numeric-table/hex trial. No routing choice is retroactively changed.

Export integrity, text/review/listing UTF-8 ranges, source row identities and a
byte-identical rebuild pass. July now has16 complete bodies and20 untouched,
no partial bodies and zero human acceptances. Cumulative coverage:83 source pages,
1,160 regions,1,094 text crops,66 images,1,484 BASIC lines,1,120 hex rows,
97 assembly rows and350 review flags. Next inspect 로고강좌, candidate94–97,
and boundary98. Full issue restoration, consolidated decision metrics and the
reading room remain outstanding.


## Logo workspace, files and debugging, 2026-10-11

Batch22 completes 로고강좌, PDF94–97/printed90–93;98 begins 샤를의 법칙.
The80 regions contain77 text crops and three original graphic outputs. Five
unnumbered Logo procedures contain29 physical rows; three console/example blocks
add5 rows. Inline commands in explanatory prose are not included in these listing
counts. All source regions were compared;21 flags remain for mandatory human review.

The preassigned route used9 Tesseract ordinary-prose/byline/caption crops and68
Qwen technical prose, heading and code crops. The original worker exited143 after
46 Qwen successes. The process was confirmed terminal before recovery; all46
successful stages and all9 Tesseract texts/TSV/timers were reused. The unfinished
p96r11 request was archived and22 remaining crops completed. No crop or engine
assignment changed. The interruption cause and unfinished inference cost are unknown.

| Observation | Planned mixed route with recovery |
| --- | ---: |
| Raw elapsed, lower–upper bound | 181.71–245.05s |
| Completed Tesseract recognition,9 calls | 1.41s |
| Completed Qwen recognition,68 calls | 154.38s |
| Correction/source review/recovery/helper window | 308.71s |
| Raw overlap with correction, bounded | 149.38–212.72s |
| Corrected non-whitespace characters | 4,873 |
| Uncached, non-write correction input tokens | 32,045 |
| Cached correction input tokens | 1,545,088 |
| Correction output tokens | 8,641 |

Cache-write was zero. Completed local Qwen usage was31,357 tokens (27,388 prompt;
3,969 completion); unfinished-request usage is unknown, not zero. The lower raw
bound combines original start through last completed stage with the measured
resume; the upper bound includes the terminal-observation/recovery delay. Do not
add raw, recognition and correction columns. Export verification also includes a
final prose-wrap correction and a separate rebuild after the immutable-output
guard rejected overwriting the first draft; that draft remains archived. These
observations do not isolate an engine's paid correction cost.

The short procedures retained every printed row, including repeated SHAPE calls
and repeated forward/turn commands. Qwen added a closing quote to a Logo prefix
quote, split SPLITSCREEN, paraphrased 묶어서, and modernized several printed 화일
occurrences to 파일. Source review restored the literal wording. Printed PAKAGE,
ERAZE/ERASE, TRIANGE, GRAPICS/GRAHICS, PROGARM, HELCHT/HEICHT and U=138 remain
visible, with review notes rather than technical repair. Solid dots before some
printer commands remain scan-linked symbols; their executable meaning is unresolved.

| Preselected crop and primary | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p94r06 — ordinary prose, Tesseract | 0.00% | 14.29% |
| p95r04 — EDIT explanation, Qwen | 0.00% | 10.19% |
| p96r18 — dot-matrix SHAPE procedure, Qwen | 0.00% | 5.71% |
| p97r09 — typeset RECTANGLE procedure, Qwen | 0.00% | 0.85% |

[Comparison20](ocr-july-comparison-20.json) uses the fixed identical PNGs and
references sealed before alternate OCR. These are unblinded assistant readings,
not human gold or whole-article error rates. Tesseract is close on the typeset
procedure; the four samples do not cover the quote/paraphrase cases. Compact CER
ignores whitespace and does not certify Logo execution. Continue provisional
content routing while collecting paid-token/time observations.

Final export integrity, review/listing UTF-8 ranges, physical row counts and a
byte-identical rebuild pass. July now has17 complete article bodies and19 untouched,
no partial bodies and zero human acceptances. Cumulative coverage:87 source pages,
1,240 regions,1,171 text crops,69 images,1,484 BASIC lines,1,120 hex rows,
97 assembly rows,29 Logo procedure rows and371 review flags. Next inspect 샤를의 법칙,
candidate98–100, and boundary101. Full restoration, final metric consolidation
and the reading room remain outstanding.


## Charles's law and Hangul-bearing BASIC, 2026-10-11

Batch23 completes 샤를의 법칙, PDF98–100/printed94–96;101 begins CP/M 입문.
Its49 regions contain46 text crops and three preserved images: the flowchart,
line-number diagram and window diagram. The complete two-column BASIC listing
contains57 logical numbered lines and107 physical text rows. Every printed line
and wrapped continuation was checked;23 flags remain for mandatory human review.

The preassigned route used7 Tesseract ordinary-prose/byline/caption crops and39
Qwen scientific/technical prose, variable, heading and code crops. All completed
without interruption, retry, fallback or crop change. No omitted numbered BASIC
rows were observed in this run.

| Observation | Planned mixed route |
| --- | ---: |
| Raw worker elapsed, including setup/render/export | 136.66s |
| Tesseract recognition,7 calls | 0.90s |
| Qwen recognition,39 calls | 120.44s |
| Correction/source review/helper window | 292.59s |
| Raw overlap with correction | 89.35s |
| Corrected non-whitespace characters | 3,765 |
| Uncached, non-write correction input tokens | 19,588 |
| Cached correction input tokens | 1,296,128 |
| Correction output tokens | 8,777 |

Cache-write was zero. Local Qwen usage was19,780 tokens (16,416 prompt;3,364
completion), separate from paid assistant work and alternate evaluation. Recognition
is nested within raw time, which overlaps correction. The correction window
includes literal/row review and helper preparation; it cannot isolate a causal
engine cost or support a speed ranking against different content.

Qwen repeatedly changed HPLOT to HPLLOT/HPL0T, confused colons and semicolons,
and misread bitmap Hangul in display strings. Those readings were source-corrected.
The source's prose references to9010 and100, variable-legend XI/YI, 사용도 and
가로안 remain rather than being reconciled with the listing. A tiny visible mark
before the4040 comparison is retained as a period and flagged as possibly damaged
ink. Historical 읍 in two faint prompts, zero/O, and exact PRINT padding still need
human confirmation. No syntax repair, execution or byte-perfect claim is made.

| Preselected crop and primary | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p98r04 — introduction, Tesseract | 0.00% | 5.48% |
| p100r02 — variable definitions, Qwen | 2.30% | 5.75% |
| p100r06 — BASIC with Korean strings, Qwen | 3.51% | 32.46% |
| p100r13 — repeated graphics commands, Qwen | 5.76% | 21.58% |

[Comparison21](ocr-july-comparison-21.json) uses fixed identical PNGs and references
sealed before alternate OCR. References are unblinded assistant readings, not human
gold or whole-article error rates. The established Tesseract alternate configuration
uses `eng` for code and `kor+eng` for other text. Consequently the Korean-string
sample compares those configurations, not the best possible multilingual Tesseract
setup. Compact CER ignores whitespace and does not validate execution. The samples
support continued technical-text trials without establishing paid-token savings.

Export integrity, text/review/listing UTF-8 ranges, explicit line identities and a
byte-identical rebuild pass. July now has18 complete article bodies and18 untouched,
no partial bodies and zero human acceptances. Cumulative coverage:90 source pages,
1,289 regions,1,217 text crops,72 images,1,541 BASIC lines,1,120 hex rows,
97 assembly rows,29 Logo procedure rows and394 review flags. Next inspect CP/M 입문,
candidate101–118 and boundary119. Full restoration, final metric consolidation
and the reading room remain outstanding.


### July CP/M opening raw checkpoint, 2026-10-11

- Confirmed CP/M 입문 spans PDF101–113;114–118 are advertisements.
  First segment101–106 has142 mapped regions:139 text crops and3 preserved figures.
- Raw OCR complete using the preassigned routing rule:125 Qwen and14 Tesseract
  regions. Semantic correction, fixed-reference comparison and article export remain
  pending; the issue stays at18 complete article bodies and zero human acceptances.
- A process-name check missed the live original worker. A premature recovery
  archived one in-flight request; the original worker completed all recognition but
  export then lacked that request. Reconstructed its evidence from the preserved
  original request and response, retained both prior stage versions, and verified
  all125 stage hashes before re-export. No completed OCR inference was rerun.
- Exclude this batch's elapsed wall time from clean speed comparisons: the mistaken
  recovery, second server startup and evidence repair contaminated it. Private
  `batch-24/recovery-correction.json` supersedes the initial interruption diagnosis.
  Raw evidence-bundle manifest SHA-256: `a5da489e2352715ac82e8283effc65944a825b1bb969fbebd4400bf537f0da9a`.
- Next: source-based correction of101–106, then107–113 and full CP/M assembly.
  Final issue metrics and reading-room work remain outstanding.


### CP/M opening source-corrected — batch24, 2026-10-11

PDF101–106/printed97–102 is exported as the first segment of CP/M 입문.
The article continues through113;114–118 are advertisements. All142 mapped
regions are accounted for:139 text crops and3 original figures, including the
apparently blank startup screen. Three directory screens total36 physical rows;
the DUMP excerpt adds1 command,7 comment rows and3 assembly statements.
All47 rows were source-compared.33 review flags retain original inconsistencies,
command typography and the unfinished106→107 prose join.

Planned14 Tesseract/125 Qwen crops completed. Successful recognition sums are
Qwen234.81s and Tesseract1.87s; local Qwen usage46,426 tokens (40,514 prompt,
5,912 completion). The322.39s raw wall time is **excluded from clean performance
comparisons** because the process-monitoring mistake, competing model startup
and evidence repair contaminated it. Recognition timings are observations from
that same affected run, not clean speed measurements. The recovery server log
contains no completed recognition; all125 original responses were retained.

The correction/source/helper window is233.71s, with no raw overlap:35,291
uncached input,620,800 cached input and8,369 output tokens (including285
reasoning), zero cache-write tokens. This is observed mixed-route work, not
a causal estimate of either engine's correction cost. Reporting/evaluation are
separate, and the current report/commit tail carries into the next usage audit.

Tesseract failed the byline and several words in the mottled-background prose.
Qwen changed source 끄고 to 켜고, 화일 to 파일, 생략 to 생각, and inserted an
extra blank assembly-comment row; source comparison restored them. Printed
ATP/Tronstent/Progrom,64KK,$D606,Operaping,Loggin,Extention,AREN and FILF
remain flagged rather than technically repaired. RAM addresses are boundaries;
the linearized table preserves their band relationships. Commands have not been
executed, and exact typeset dots, spacing and return-marker bytes are not certified.

| Fixed sample | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p102r03 — gray-background OS prose | 0.00% | 10.00% |
| p102r26 — logical/physical device table | 0.00% | 82.56% |
| p105r10 — directory screen | 0.00% | 5.00% |
| p106r18 — assembly excerpt | 0.00% | 18.52% |

[Comparison22](ocr-july-comparison-22.json) uses identical PNGs and assistant
references sealed before alternate OCR. These are unblinded samples, not human
gold or whole-article accuracy. Compact CER ignores whitespace and cannot
certify command syntax or literal spacing. The routing heuristic now considers
mottled backgrounds even for ordinary prose; no automatic default has changed.

Export integrity, UTF-8 review/listing ranges and a byte-identical rebuild pass.
July has18 complete bodies,1 partial and17 untouched; human acceptance remains
zero. Cumulative coverage:96 source pages,1,431 regions,1,356 text crops,75
images,1,541 BASIC lines,1,120 hex rows,100 assembly rows,29 Logo rows and427
flags. Next restore107–113 and assemble all13 CP/M pages. Full-issue restoration,
final metrics and the reading room remain outstanding.


### CP/M conclusion and full article assembly — batch25, 2026-10-11

PDF107–113/printed103–109 completes CP/M 입문. Its203 mapped regions contain
199 text crops and4 preserved images: page-count formula, SAVE diagram, decorative
image and tab-stop diagram. The102 nonblank console rows include9 assembly
statements; inline typeset commands remain in prose.38 source-review flags cover
damaged characters, original technical anomalies and uncertain punctuation.

Preassigned13 Tesseract captions and186 Qwen technical/mottled-background crops
completed without retry or fallback. Raw407.91s includes rendering, verification,
startup and evidence export; recognition sums Qwen343.68s/Tesseract0.86s are nested
within it. Local Qwen usage68,540 tokens (60,273 prompt,8,267 completion) is separate
from paid assistant work and alternate evaluation. Correction/source/helper time
362.22s overlaps raw292.09s. Observed correction usage:20,537 uncached input,
1,570,688 cached input and11,104 output tokens (including1,482 reasoning), zero
cache-write. These mixed-content measurements do not isolate causal engine costs.

Qwen changed the CAT directory entry TEMP.$$$ to TEMP.COM, added a blank comment
row and dropped comment semicolons from the short PIP display. Source comparison
restored the extension and physical rows. Source108 has damaged character fragments
even outside our crop; these are explicitly marked rather than inferred as LOAD or
grammatical endings. Original bare ORG, unlabeled EQU15/20, unusual >A:PIP STAT
prompt, single-bar typeset command separators, leading AUTORUN stroke and DATCH
heading remain. The comma-like mark after DUMP in the CAT table remains provisional.
No command execution, syntax repair or exact-spacing certification is claimed.

| Fixed sample | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p108r12 — STAT console | 0.00% | 7.69% |
| p109r20 — gray-background PIP prose | 3.39% | 6.78% |
| p111r03 — assembly rows/comments | 0.00% | 4.46% |
| p113r02 — CAT directory rows | 3.05% | 16.79% |

[Comparison23](ocr-july-comparison-23.json) uses identical PNGs and references
sealed before alternate OCR. References are unblinded assistant readings, not human
gold. Typeset punctuation and the provisional comma-like mark affect these scores;
compact CER ignores whitespace and is not whole-article or executable-code accuracy.
The results support continued trials, not a proven paid-token saving.

The full101–113 article is assembled from immutable24/25 packages:345 regions,
338 text crops,7 figures,149 physical console/listing rows,12 assembly statements
and71 flags. The106→107 continuation is one reading block; its original terminal
newline remains between 이 and 름으로 to preserve segment bytes. Listing bytes are
exactly the concatenated source listings. All source/review UTF-8 ranges, complete
coverage, export integrity and byte-identical rebuild checks pass. Human acceptance
is pending. The assembler rejected an initial join assertion that omitted that
terminal newline; correcting the recipe required no source-package changes.

July now has19 complete article bodies, no partial bodies and17 untouched; zero
human acceptances. Cumulative coverage:103 source pages,1,634 regions,1,555 text
crops,79 images,1,541 BASIC lines,1,120 hex rows,109 assembly rows,29 Logo rows
and465 flags. Next inspect 기계어 강좌, candidate119–128 and boundary129.
Full-issue restoration, final metric consolidation and the reading room remain
outstanding. Batch24 timing exclusions remain in force.


### Z80 lesson opening — batch26, 2026-10-11

Restored PDF119–123/printed115–119 of the verified119–127 article.128 begins
the next article's title page, while its catalog reference points to body129.
This segment has104 regions:100 text crops,4 original images,50 assembly/example
rows and29 review flags. The50 rows comprise8 ADD/ADC examples,2 ORG directives
and40 addressed listing rows; the final853D row has no visible mnemonic.

Preassigned2 Tesseract byline/caption and98 Qwen technical crops completed without
retry or fallback. Raw262.40s includes setup/render/export; recognition sums
Qwen220.34s/Tesseract0.13s are nested. Local38,948 tokens comprise33,257 prompt
and5,691 completion. Correction/source/helper time329.46s overlaps raw183.76s;
18,826 uncached input,2,038,784 cached input and9,783 output tokens (including
1,981 reasoning), zero cache-write. Mixed-route observations do not isolate causal
engine correction costs; evaluation/reporting are separate.

Qwen merged ORG with the first addressed row, shifted LD A,41H and omitted
LD B,26D. All five source rows and column associations were restored. Every row
of both listings was checked, including all eight BIT operands. Original −95,
255/225,137/127 and +128/−128 contradictions remain, alongside source spellings,
missing parenthesis and blank853D mnemonic. No technical correction, execution or
byte-perfect claim is made. The arithmetic figures are linearized text with source
crops retained; drawn rules are omitted and arrow positioning is approximate.

| Fixed sample | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p120r01 — technical introduction | 1.23% | 12.35% |
| p120r17 — arithmetic layout | 33.33% | 3.33% |
| p122r19 — ADD operand examples | 0.00% | 5.56% |
| p123r19 — addressed assembly rows | 0.00% | 13.25% |

[Comparison24](ocr-july-comparison-24.json) uses identical PNGs and references
sealed before alternate OCR. The arithmetic score includes Qwen's added dashed
divider and arrow/label placement; it is not a pure digit-accuracy result. Samples
are unblinded assistant references, not human gold or whole-article accuracy. The
ORG/LD row failure occurred outside these fixed samples and remains material.

Export integrity, source-linked UTF-8 review/listing ranges and byte-identical
rebuild pass. July:19 complete bodies,1 partial,16 untouched; zero human acceptances.
Cumulative:108 source pages,1,738 regions,1,655 text crops,83 images,1,541 BASIC
lines,1,120 hex rows,159 assembly/example rows,29 Logo rows and494 flags. Next
124–127 and full lesson assembly; the123→124 prose join must account for intervening
listings. Full restoration, final metrics and reading room remain outstanding.


### Z80 lesson fully assembled — batch27, 2026-10-11

PDF124–127 completes the lesson begun in26:122 regions,119 text crops,3 images,
32 opcode rows with192 flag cells,12 truth-table data rows,4 logic-operation rows,
37 assembly/comment/directive rows and32 review flags. Both full opcode tables
remain as images beside their row transcriptions. Two damaged readings—the
INC(HL) result expression and one listing address digit—remain explicitly unresolved.
Original NFG,0011 register code, unusual operators, flag values and apparent opcode
mistakes are retained. Qwen separated the opening listing's mnemonic/address columns;
source review restored their association. No execution or byte-perfect claim.

Originally6 captions were assigned to Tesseract and113 text crops to Qwen.
Qwen p125r15 and p125r28 each repeated to the4096-token limit. After the second
failure, both failed crops and17 remaining unattempted opcode rows used Tesseract;
final25 Tesseract/94 Qwen crops.38 successes survived the first failure and50 were
reused on the final resume; no completed inference was rerun. Original routing,
failed responses, fallback changes and all local usage remain recorded separately.
Tesseract still required substantial table correction; the fallback bounded further
looping rather than establishing better table accuracy or lower paid cost.

Successful recognition: Qwen181.82s and Tesseract3.12s. Failed Qwen server compute
adds249.79s. Local42,668 tokens include both failed calls:29,802 prompt and12,866
completion. Exact raw process exit times were not instrumented;434.72–572.22s is
a broad bound, from measured recognition/failed compute to the full wall span,
whose upper bound includes recovery preparation. It is not a clean raw-speed sample.
Correction/source/helper work580.19s includes recovery preparation and overlaps that
wall span545.37s; do not add them. Paid correction observations:51,734 uncached input,
1,870,720 cached input,17,558 output including2,547 reasoning; zero cache-write.
Preparation, assembly, alternate evaluation and reporting are separate. Content,
source damage and recovery confound any causal engine-cost comparison.

| Fixed sample | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p124r01 — technical prose | 1.67% | 10.00% |
| p125r14 — ADD opcode row | 34.62% | 92.31% |
| p126r23 — ADC HL opcode row | 23.91% | 71.74% |
| p127r15 — OR assembly sample | 0.00% | 9.62% |

[Comparison25](ocr-july-comparison-25.json) uses the four preselected identical
PNGs and references sealed before alternate OCR. The rerouted ADC HL sample has
a bounded512-token Qwen alternate (completed normally); the different cap is
recorded. Table scores include flag/arrow typography and editorial slash separators
for stacked opcode lines, so they are not pure cell-value accuracy. References are
unblinded assistant readings, not human gold; none of these samples captures the
two primary length-limit failures. All failures remain part of the cost evidence.

Full119–127 assembly:226 regions,219 text crops,7 images,87 assembly/example rows
and61 flags. The123→124 prose join explicitly declares11 intervening listing blocks.
Source listing bytes, all review ranges, complete coverage, export integrity and
byte-identical rebuild pass. An initial export invocation lacked the src import
path; rerunning with the project path succeeded without changing source evidence.

July now has20 complete article bodies, no partial bodies and16 untouched; zero
human acceptances. Cumulative:112 source pages,1,860 regions,1,774 text crops,
86 images,1,541 BASIC lines,1,120 hex rows,196 assembly/example rows,29 Logo rows
and526 flags. Next inspect graphics title128/body129 and boundary137. Full issue
restoration, final metric consolidation and the reading room remain outstanding.


### Computer graphics — batch28, 2026-10-11

Restored the complete article PDF128–134/printed124–130.128 is the title page;
129 is the catalog's body reference.135–136 are advertisements and137 begins
Apple FORTRAN. The package has167 regions:158 text crops,9 original photographs/
illustrations/graphs,135 numbered BASIC lines in154 physical rows across8 listing
groups,45 DATA records containing270 printed fields, and37 review flags.

The initial route assigned10 clear captions/byline crops to Tesseract and148
technical/mottled-background crops to Qwen. Color-table p129r23 repeated escaped
tabs until4096 tokens. One same-crop Tesseract fallback and two remaining unattempted
ruled tables then switched the retained output to13 Tesseract/145 Qwen crops.
All24 completed first-attempt Qwen stages were reused without rerunning recognition.
This extends the ruled-table caution beyond batch27's opcode/flag rows. The failed
response, original route and changed assignments remain separately auditable.

Both worker lifespans were measured: raw505.01s is229.16s first attempt plus275.85s
resume, including failure/startup/render/export and excluding between-attempt
recovery preparation. Successful recognition is Qwen311.72s/Tesseract1.40s;
failed Qwen server compute123.76s is separate and nested within raw time.
Local58,306 tokens include the failed call:46,294 prompt and12,012 completion.
Correction/source/helper work611.12s overlaps measured raw attempts448.63s; do not
add the overlapping windows. Correction observations:33,307 uncached input,
2,410,496 cached input and18,964 output including4,007 reasoning; zero cache-write.
Mapping, alternate evaluation, export and reporting remain separate. These are
content/recovery-confounded observations, not causal per-engine correction costs.

Qwen silently omitted seven isolated continuation characters: I completing the
cube's line100 and six0 rows completing scores in the two DATA listings. Source
row checks restored them. In one dense DATA crop, Qwen separated line-number/DATA
labels from values and corrupted several scores and names. All45 records were
compared against their respective source pages. HPLOT/HPLLOT/HPL0T,1.5/15 and
Korean graph terms were also corrected. The larger dense-listing crops were fixed
during preflight before inference; no source crop was changed after recognition.

Source duplicate student17 and missing11,150/160 prose reference,220 versus200
bar-graph constant, abbreviated HPLOT replacement and missing closing quotation
remain as printed. Tiny apostrophe/period-like marks are retained provisionally
and flagged; no program execution, syntax repair or byte-perfect claim is made.
The second DATA listing ends after390 and jumps to450 END; absent400–440 rows
were not copied from the earlier program.

| Fixed sample | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p129r01 — introductory prose | 0.00% | 2.82% |
| p130r07 — frame BASIC | 1.72% | 13.79% |
| p131r15 — DATA rows310–350 | 4.51% | 58.65% |
| p134r10 — wrapped sine formula | 0.00% | 47.62% |

[Comparison26](ocr-july-comparison-26.json) uses preselected identical PNGs and
assistant references sealed before alternates. Compact CER ignores whitespace;
it does not certify physical-wrap preservation, whole-article accuracy or human
acceptance. The primary table failure and seven omitted characters occurred
outside these fixed samples and remain part of the evaluation and cost evidence.

All export, source-linked UTF-8 review/listing ranges, explicit printed-line counts,
complete coverage and byte-identical rebuild checks pass. July now has21 complete
article bodies, no partial bodies,15 untouched and zero human acceptances.
Cumulative:119 source pages,2,027 regions,1,932 text crops,95 images,1,676 BASIC
lines,1,120 hex rows,196 assembly/example rows,29 Logo rows and563 flags.
Next inspect Apple FORTRAN137 onward; its ending is unverified. Full-issue
restoration, final metrics and reading-room build remain outstanding.


### Apple FORTRAN — batch29, 2026-10-11

Restored PDF137–142/printed133–138 completely:123 regions,109 text crops,
14 original images,73 FORTRAN source rows and115 physical listing/menu/compiler
rows across13 groups. The two output tables contain80 numeric cells;31 review
flags remain.143 starts Information Radar, which continues through157.
158–159 are advertisements;160–162 Review Salon was already restored.

Two bounded English Tesseract preparation probes took0.629s total. The compiler
probe corrupted identifiers, digits and punctuation, so handwritten and compiler
listings used Qwen. The numeric-output probe retained usable row structure, so
those two tables used Tesseract with an explicit English override. Clear intro/
conclusion and captions also used Tesseract: final94Qwen/15Tesseract crops.
Probe crops differ from primary crops; their evidence and extra preparation cost
are retained separately. No engine assignment changed after primary inference.

The first worker exited143 (SIGTERM), with no recorded cause, after70 completed
Qwen crops. Those immutable stages were reused; one interrupted request was
archived and retried. No completed inference was repeated. Raw elapsed is bounded
232.60–355.95s, with a broad upper bound that includes interruption investigation;
exclude it from clean speed comparisons. Successful recognition was
Qwen200.65s/Tesseract1.51s. Completed Qwen responses account for38,558 local tokens
(33,510 prompt/5,048 completion), a lower bound: the interrupted response was not
captured. Its server log reports0.450s compute,207 evaluated prompt tokens and
8 generated tokens; this is not complete API prompt/cache accounting.

Correction/source/helper work took515.16s and includes interruption recovery.
Bounded raw overlap is215.62–338.97s; do not add overlapping stages. Observed paid
correction usage:53,873 uncached input,1,621,888 cached input and14,764 output
including1,819 reasoning; zero cache-write input. Mapping, probes, alternate
comparison, export and reporting remain separate. The compiler/handwriting work
and interruption prevent a causal claim about per-engine paid cost.

Qwen detached compiler line counters/offsets from statements and normalized
printed COLUMMN to COLUMN. Source checks restored both, along with handwritten
slashed-zero/I/slash readings. The source SYSIEM, CTRA-A, EXCUTE, SW=9 and the
intentional missing continuation marker in the error example remain unchanged.
Faint screen3 has an explicit unreadable fragment; its caption and several screen
glyphs remain provisional. Compiler source counters are indexed as unnumbered
printout evidence, not BASIC line numbers. All80 numeric cells were read from
the scan; output values were not reconstructed by executing or sorting the code.

| Fixed sample | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p137r06 — ordinary introductory prose | 0.00% | 2.65% |
| p140r04 — handwritten FORTRAN | 0.00% | 36.11% |
| p142r03 — compiler source/offsets | 11.60% | 23.70% |
| p142r09 — sorted numeric output | 2.53% | 10.13% |

[Comparison27](ocr-july-comparison-27.json) uses preselected identical crops and
unblinded assistant references sealed before alternates. Both Tesseract-primary
samples received bounded512-token Qwen alternates and completed normally.
Whitespace, handwritten glyph conventions and printed divider representation
limit CER interpretation. Qwen's compiler score also reflects character errors;
compact CER does not validate row associations or executable code. These samples
support better Qwen raw accuracy, not a demonstrated paid-cost advantage for the
chosen routing or either engine.

Complete coverage, source-linked UTF-8 review/listing ranges,73 source-row counts,
80 numeric-cell counts, export integrity and byte-identical rebuild all pass.
July now has22 complete bodies, no partial bodies,14 untouched and zero human
acceptances. Cumulative:125 unique source pages,2,150 regions,2,041 text crops,
109 images,1,676 BASIC lines,1,120 hex rows,196 assembly/example rows,29 Logo rows,
73 FORTRAN source rows and594 review flags. Next inspect Information Radar143–147
as an opening batch of its143–157 extent. Final issue metrics and reading-room
build remain outstanding.


### Information Radar domestic section — batch30, 2026-10-11

Restored PDF143–148/printed139–144, the complete domestic-news section of the
verified143–157 Information Radar article. It contains16 news items and one
additional robot-contest notice:152 regions,145 text crops,7 original images,
one six-row system-specification table with21 cells, and31 review flags.
Foreign news149–157 and full article assembly remain outstanding.

The preassigned route used108 Tesseract crops for clear news/headlines/notices and
37 Qwen crops for dense hardware/gate-array/course specifications plus the reversed
section heading. A bounded Tesseract probe preserved the specification table's
six row associations, though it lost column headings and damaged some labels.
The same unchanged PNG and its hash-checked result were reused as the primary
Tesseract evidence; no second call was made. No retries or fallbacks occurred.
The probe took0.205s during setup. It is included once in primary recognition,
excluded from raw-worker elapsed, and must not be added again as extra OCR cost.

Raw-worker time was128.97s. Recognition was Qwen87.35s/Tesseract15.28s, including
the reused0.205s table probe in the latter. Local Qwen usage14,901 tokens consists
of12,627 prompt and2,274 completion tokens. Correction/source/helper work418.06s
overlaps the raw worker109.52s. Paid correction observations:24,299 uncached input,
1,505,792 cached input and13,093 output including2,388 reasoning; zero cache-write.
Mapping, alternate evaluation, export and reporting remain separate. These are
mixed-content observations, not causal savings relative to FORTRAN or a second
correction of the same source.

Tesseract returned an empty organization heading and badly fragmented several
ruled headlines, Latin names and event labels. The selected table still needed
header/label restoration. Qwen corrupted a few Korean words and omitted a syllable
from a company name. All included passages were source-compared; internal column/
page continuations were explicitly joined, and the gate-array diagram was placed
with its text before the next news item. The table's12 specification cells,
6 row labels and3 headers were checked individually. The poster's duplicate
inquiry bullet is preserved twice, as printed.

Original8077, IIL/CDI, SAN/370, SNA/3780, 요성 and the isolated 사프로 spelling
remain. Unusual 컴퓨터을보급 and 부속 전구로 are provisional source readings
with human-review flags. Historical names, dates and telephone numbers were not
modernized or factually corrected. Graph/diagram/photo lettering remains in the
original images; the table and robot notice also have separate transcriptions.

| Fixed sample | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p143r08 — ordinary news prose | 0.00% | 14.63% |
| p144r16 — APC specifications | 0.00% | 20.99% |
| p146r09 — CMOS process parameters | 0.00% | 9.88% |
| p147r21 — ruled system table | 2.63% | 30.70% |

[Comparison28](ocr-july-comparison-28.json) uses preselected identical PNGs and
unblinded assistant references sealed before alternate recognition. Tesseract
uses kor+eng throughout; the two Tesseract-primary Qwen alternates have512-token
caps and completed normally. Compact CER ignores whitespace and reflects table
dash/column typography; it is not a pure numeric-cell score or proof of reading
order. The blank-headline failures are outside these fixed samples. Qwen wins
all four raw comparisons; the Tesseract choices remain experiments in total
restoration cost, not claims of better accuracy.

Export integrity, complete domestic coverage, explicit joins, all UTF-8 review
ranges, table-cell counts and byte-identical rebuild pass. July now has22 complete
bodies,1 partial body and13 untouched;14 bodies remain incomplete and none has
human acceptance. Cumulative:131 unique source pages,2,302 regions,2,186 text crops,
116 images and625 review flags. Code/hex/Logo/FORTRAN totals are unchanged.
Next inspect149–153 as a foreign-news batch, then the remainder through157 and
full Information Radar assembly. Final issue metrics/reading room remain pending.

### Information Radar foreign opening — batch31, 2026-10-11

Restored PDF149–153/printed145–149:156 text regions, no figures or tables,
13 complete news items and the opening of a GaAs SISFET item. Information Radar
remains partial: domestic143–148 is in batch30, and154–157 plus assembly remain.
The final153 fragment ends 순; preserve its mid-word join to154.

The planned39 Tesseract/117 Qwen route assigns ordinary collaboration, robot
standardization, export-control and UNIX news prose plus short labels to Tesseract;
technical specifications and boxed headlines go to Qwen. A bounded Tesseract
headline probe took0.119s and lost the1칩모뎀 wording. It was rejected before primary
recognition. Its crop differs slightly from the primary headline crop: it is
separate preparation evidence, not reused primary inference or a fifth fixed sample.

One worker exited143 after78 successful Qwen crops. All78 were hash-checked and
reused, with no routing change or successful crop repeated. The interrupted
p152r02 request is archived; its response/token usage was not captured. The
SIGTERM handler measured the first worker206.485s; the successful resumed worker
measured93.923s. Their sum300.408s includes render, startup and evidence handling,
but excludes recovery preparation between attempts. The cause of SIGTERM is
unknown. Successful recognition was Qwen259.357s/Tesseract5.069s; those calls
are nested within raw time. Local completed responses contain40,690 prompt and
7,260 completion tokens,47,950 total: a lower bound, not zero interrupted cost.

Correction/source review, recovery and helper work took692.44s and overlapped
232.21s of the measured raw attempts. Paid observations:70,124 uncached input,
2,768,128 cached input and20,299 output including2,370 reasoning; zero cache-write.
Preparation, export, evaluation and reporting are separate. The longer correction
window includes recovery and technical/source ambiguity checking; it cannot be
attributed causally to one engine or compared as a clean per-engine cost.

Qwen misread the boxed 핸드쉐이크 시퀀스 headline, several Korean syllables and
company names. Tesseract prose/labels needed source restoration of technical names
and ordinary words. Source review preserved original10계획,28ns초, repeated
프린터, TM 50C40, MES FDT/HEAT and contradictory component totals. No device
numbers or scientific statements were repaired from external knowledge. Faint
11 2 ms, the widely spaced11 mW digits,28편, PO-23A and printed 특정 remain
explicitly provisional. There are37 review flags; human proofreading is mandatory.

| Fixed sample | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p149r03 — ordinary news prose | 0.00% | 10.29% |
| p150r26 — boxed modem headline | 10.53% | 21.05% |
| p151r28 — CMOS identifiers | 0.00% | 17.02% |
| p153r26 — GaAs technical prose | 0.00% | 16.85% |

[Comparison29](ocr-july-comparison-29.json) uses preselected identical PNGs and
assistant references sealed before alternates, unblinded and not human gold.
Tesseract uses kor+eng throughout. The single Tesseract-primary sample's Qwen
alternate completed within its512-token cap. Compact CER ignores whitespace;
source ambiguities and prose joins require separate review. Qwen wins these raw
samples, but this does not establish a paid-token advantage for the mixed route.

Export integrity, all156 regional records, explicit news joins, UTF-8 review
ranges and byte-identical rebuild pass. July remains22 complete bodies,1 partial
and13 untouched, zero human accepted. Cumulative136 unique source pages,2,458
regions,2,342 text crops,116 images and662 review flags; code totals unchanged.
Next restore154–157 and assemble the full143–157 article. Final issue metrics
and the authorized post-restoration reading-room build remain outstanding.

### Information Radar completed — batch32 and assembly, 2026-10-11

Restored final PDF154–157/printed150–153:118 regions,117 text crops,one original
GaAs diagram and32 review flags. This completes the GaAs news from batch31 and
adds six complete items: Pascal, Apple IIc, HP laser printer, program generators,
microcomputer terminology and a Lisp machine. The full143–157 article is now
assembled from30–32:426 regions,418 text,8 original images,36 news items plus one
robot-contest notice,21 specification-table cells and100 review flags.

The preassigned route used52 Tesseract crops for ordinary Pascal/program-generator
prose, short headings and the diagram caption;65 Qwen crops for technical details,
product terminology and boxed headlines. No new preparation probes were needed.
One SIGTERM interrupted p157r14 after48 saved Qwen results. All48 were reused
unchanged; no successful inference was repeated, and routing did not change.
The two measured worker lifespans139.410s and42.354s total181.764s, excluding
recovery preparation. Successful recognition was Qwen142.279s/Tesseract8.934s,
nested within raw time. Local completed usage22,349 prompt plus3,834 completion
is26,183 tokens: a lower bound because the interrupted response is unavailable.

Correction/source checking, recovery and helper work took295.86s, overlapping
98.56s of raw attempts. Paid observations:27,734 uncached input,1,015,040 cached
input and8,494 output including1,110 reasoning; zero cache-write. The raw32 assistant window also contains initial source-reading and transcription
preparation before the correction window opened; include it when comparing total
restoration cost. Full assembly
was a separate75.92s window with9,232 uncached/723,328 cached input and1,612 output
including187 reasoning. These mixed-content observations do not measure causal
per-engine savings; the assembly window includes choosing the supported existing
assembly-index mode after an initial recipe validation rejection.

Qwen duplicated Korean syllables at two line breaks and confused the Apple IIc
heading, 응용, 워드스타 and several company/show-name spellings. Source reads
restore these while retaining printed onrmal off, Compag, 렘, the different
일렉트리/일렉트릭 spellings and the Pascal article's apparent 프로프로그램
repetition. Faint 휼레트/컴덱스/존속 readings remain provisional. Original claims
about Pascal read, ANSI's expansion and hardware capacities are transcribed,
not factually repaired. RomanⅡ, raised⁺ and the stacked½ are explicit typography
representations; no code was executed or inferred.

| Fixed sample | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p154r03 — GaAs technical prose | 1.35% | 16.22% |
| p154r16 — ordinary Pascal prose | 4.29% | 10.00% |
| p155r14 — Apple hardware specifications | 1.61% | 19.35% |
| p157r24 — Lisp hardware specifications | 1.30% | 2.60% |

[Comparison30](ocr-july-comparison-30.json) uses preselected identical PNGs with
unblinded assistant references sealed before alternates. Tesseract uses kor+eng;
the one Tesseract-primary Qwen alternate completed within512 tokens. Compact CER
ignores whitespace but counts superscript and Roman-numeral representation.
Qwen wins these four samples, while Tesseract is close on the Lisp passage.
This still does not establish which route minimizes paid correction cost.

The assembly preserves all three segment exports and their source bytes. Its
explicit153/154 join places 순 and 도가 높은 in one reading block, retaining
the immutable source newline. All review ranges,426 regional records,15-page
coverage and byte-identical rebuild pass. PDF157 has a complete final sentence
and article-end mark;158 is a publisher book advertisement, clarifying the
batch32 map's earlier generic phrase “another article.” Human acceptance remains
pending; no reading-room build was run at this checkpoint.

July now has23 complete bodies,13 untouched and no partial bodies, zero human
accepted. Cumulative140 unique source pages,2,576 regions,2,459 text crops,
117 images and694 review flags. Listing totals are unchanged. Next inspect
VISICALC candidate164–168; its exact extent is not yet verified. Final full-issue
metrics and the authorized reading-room build remain outstanding.

### VISICALC/VISIPLOT complete — batch33, 2026-10-11

Restored PDF164–168/printed160–164. The next page169 visibly starts 자료구조.
The five-page tutorial contains135 regions,122 text crops,13 source images,
116 physical command/annotation rows and35 review flags. Ten charts, the original
budget spreadsheet, a stacked equation and cursor-key diagram remain images;
commands, equation and budget values have separate source-linked transcription.

The planned route used29 Tesseract crops for introductory prose, titles/captions
and93 Qwen crops for commands, technical instructions, reversed installment title
and the dot-matrix table. A bounded English Tesseract table probe took0.333s and
badly corrupted labels and numeric values. It was rejected for primary OCR, but
the identical PNG/result was retained as its fixed comparison alternate after
hash verification. No second Tesseract table call was made. The probe is extra
setup recognition, excluded from primary recognition and raw-worker elapsed;
its reuse adds no evaluation inference cost.

Qwen transcribed all63 numeric values in the nine budget rows correctly against
the assistant's source reading. It returned them as a vertical list and omitted
spreadsheet coordinates, so correction restored row/column layout, row indices,
column letters and headers. Printed TOTAL, AVE and ENGEL figures were not
recalculated. A repeated-equals decoration is normalized to12 equals signs and
the title is presented textually; the screenshot remains the glyph/position source.
This is a63-cell observation from one unblinded assistant-reviewed table, not
human-certified accuracy or a general table benchmark.

One SIGTERM interrupted p166r11 after41 saved Qwen crops. All41 were reused
unchanged; no successful inference was repeated and no routing changed. The
measured worker attempts114.826s and94.441s total209.267s, excluding recovery
preparation. Successful recognition176.489s Qwen/3.141s Tesseract is nested in
raw elapsed. Local completed responses contain31,352 prompt plus4,183 completion
tokens,35,535 total; interrupted response usage is unknown, so this is a lower
bound. The rejected0.333s probe remains separate.

Correction/source review, recovery and helper work456.13s overlaps197.43s of raw.
Paid observations:23,657 uncached input,1,964,672 cached input and12,556 output
including2,764 reasoning; zero cache-write. Setup, export, evaluation and reporting
remain separate. Counts include mixed content and recovery work, so they do not
establish causal per-engine savings.

Qwen frequently confused circled R/S with circled digits or registered marks,
inserted zero into VISIPLOT, and changed 저장시키자 to 저장시켜라. These were
restored from source. Circled letters use Unicode enclosed forms; boxed cells
and arrows use editorial square brackets. The circled a/@-like glyph remainsⓐ
with an explicit identity flag. Physical command/annotation line breaks and
wrapping hyphens remain; this is not an executable command script.

Printed VISIPOLT, MATN/FOOD, the final I after its annotation, LIVE, SERLES5,
Scale0, the missing7 afterG and the Y/N question followed by1 remain uncorrected.
The faint sound word 뺑빼 and a formula-description digit remain provisional.
All ten charts retain original labels, colors as scanned, geometry and data;
none was reconstructed from computed values. Human review is mandatory.

| Fixed sample | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p164r08 — ordinary introductory prose | 0.00% | 5.00% |
| p164r23 — formula commands | 9.23% | 26.15% |
| p165r06 — complete dot-matrix table | 13.80% | 68.40% |
| p168r06 — mixed-language title commands | 5.26% | 15.79% |

[Comparison31](ocr-july-comparison-31.json) uses preselected identical PNGs.
Assistant references were sealed before new alternates; the earlier table probe
had already informed routing. Tesseract uses English for the table and kor+eng
for other samples, including commands. The one Tesseract-primary Qwen alternate
completed within512 tokens. Compact CER ignores whitespace but counts restored
coordinates and circled/boxed typography: the table's13.80% is not its numeric-
cell error rate. All four samples favor Qwen, without proving paid-token savings.

Export integrity, all135 regions,116 physical rows,63 source-checked numeric
cells, explicit column continuations, UTF-8 review ranges and byte-identical
rebuild pass. July now has24 complete bodies,12 untouched and no partials, zero
human accepted. Cumulative145 unique pages,2,711 regions,2,581 text crops,130
images and729 flags. This batch adds116 VISICALC command/annotation rows; earlier
BASIC, hex, assembly, Logo and FORTRAN counts remain unchanged. Next inspect
자료구조 candidate169–174, including its exact final boundary. Full-issue metric
consolidation and the authorized reading-room build remain pending.

### Data structures complete — batch34, 2026-10-12

Restored PDF169–174/printed165–170;175 starts UNIX. The complete article has
170 regions,148 text crops,22 source images and36 review flags. Six original
listing images accompany107 nonblank physical PL/I code/comment rows in ten
procedures: CREAT, INSERT, DELETE, ADDS, DELETES, ADDQ, DELETEQ, INIT, GETNODE
and RET. Sixteen memory/list diagrams retain their original addresses, arrows
and labels; they were not reconstructed as tables.

The route was fixed before inference:38 Tesseract crops for clear prose,
headings and captions,110 Qwen crops for technical prose, notation and code.
No route changed. One SIGTERM interrupted p172r30 after59 saved Qwen crops;
all59 were reused unchanged. A first resume stopped before new inference because
the interrupted stage still needed archival. Its4.793s startup cost and original
request are retained. The subsequent resume completed; no successful crop was
recognized twice. The measured worker lifespans147.223s,4.793s and114.089s sum
to266.105s, excluding preparation gaps. Successful recognition220.986s Qwen and
4.179s Tesseract is nested in raw elapsed. Completed local responses contain
35,098 prompt and5,527 completion tokens,40,625 total, a lower bound because
the interrupted request has no captured response usage.

Correction/source review, recovery and helper work took501.76s and overlapped
256.40s of the three raw worker lifespans. Paid observations:58,866 uncached
input,1,321,856 cached input and14,301 output including1,482 reasoning; zero
cache-write. Setup34 spans interrupted/status-only context and must not be read
as uninterrupted active preparation. Export, evaluation and reporting remain
separate. These mixed-content, unblinded observations do not isolate per-engine
paid-token savings.

Qwen's main code errors included punctuation, I/J, and a substantially corrupted
faint DELETEQ ending. Source review preserves printed CREAT, ADDS/DELETES,
missing declarations, R(I)=Y, PL/A and duplicated Korean prose. The faint
LINK(R+I))=X; reading, its plus-like glyph/parenthesis count, and several DELETEQ
glyphs remain explicitly provisional. Code was neither executed nor repaired.
Typeset inequalities use Unicode≤, while code retains physical comment wraps.
A large blank gap inside ADDQ is omitted from the text but preserved in its
image. The pool-routines frame precedes the joined left/right-column explanation
in reading order. Human review remains mandatory.

| Fixed sample | Qwen compact CER | Tesseract compact CER |
| --- | ---: | ---: |
| p169r07 — clear introductory prose | 0.00% | 1.23% |
| p170r24 — linked-list technical prose | 0.00% | 0.00% |
| p173r28 — PL/I ADDQ header/declaration | 1.59% | 44.44% |
| p173r32 — faint DELETEQ ending | 22.22% | 73.02% |

[Comparison32](ocr-july-comparison-32.json) uses preselected identical PNGs,
with assistant references sealed before alternates. Tesseract uses kor+eng for
prose and eng for code. The T-primary Qwen alternate completed within512 tokens.
The faint ending's reference is provisional, so its CER measures agreement with
that reading, not certified ground truth. This batch supports testing the content
routing rule further; the technical-prose tie cautions against categorical claims.

Export integrity, all170 regional records,107 listing rows in ten procedure
groups, explicit page/column joins, UTF-8 review ranges and byte-identical rebuild
pass. July now has25 complete bodies,11 untouched, no partials and zero human
accepted. Cumulative151 unique pages,2,881 regions,2,729 text crops,152 images
and765 flags. Earlier listing totals remain unchanged; this adds107 PL/I rows.
Next inspect UNIX candidate175–183 and verify the final boundary. Full-issue
metrics and the authorized reading-room build remain outstanding.
