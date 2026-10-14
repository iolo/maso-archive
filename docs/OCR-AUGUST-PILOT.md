# August 1984 paired restoration cost pilot

> Historical experiment report/protocol. Measurements and original conclusions
> below are retained. For future restoration, follow the owner's 2026-10-14
> [OCR policy](../PLAN-OCR.md): mapped Tesseract by default, Qwen as explicit
> assistance with layout/coverage review. This report does not queue a new trial.


Status: complete for the eight selected article pairs: 16 independent restorations
sealed, source-compared and export/rebuild verified. Human acceptance is pending.
The [consolidated cost report](OCR-AUGUST-PILOT-RESULTS.md) contains the decision,
article-level token/time tables, price sensitivity, quality findings and overhead.
Selection and order were frozen before viewing either engine's output.
This pilot follows the user's October 12 request
to compare paid restoration cost with local CPU, GPU and runtime priced at zero.

The [setup usage audit](ocr-august-pilot-setup-usage.json) records selection and
protocol work through2026-10-12 00:40:48 UTC:39,461 uncached input,1,848,320 cached
input and10,510 output tokens (3,350 reasoning tokens already included in output).
This is shared experimental overhead, not either route's correction cost. The
subsequent validation,commit and report tail is outside that cutoff.

## Selected articles

Each selected article will be restored in full through both routes: **eight
articles, 28 distinct source pages, 16 restorations and 56 page passes**. This is
a purposive sample of different layouts, not a random sample of the entire issue.

| Pair | Article | Printed / PDF pages | Why included |
| --- | --- | --- | --- |
| 01 | 편집자 노트 | 20 | Short ordinary Korean prose; inexpensive instrumentation check |
| 02 | 죽음의 스키 | 37–38 | Short BASIC game, introductory prose and graphic/symbol rows |
| 03 | 공모총평 | 237 | Prose plus a small results table; second short prose case |
| 04 | 기초 테크닉 코너 | 65–68 | Several short BASIC listings, explanations and flowcharts |
| 05 | VISICALC 활용 | 181–185 | Spreadsheet formulas, numeric tables, commands and screen images |
| 06 | PIA 시리즈2 미니네온사인의 제작 | 196–199 | Circuit diagrams, register/bit tables and short code examples |
| 07 | 베이직 코맨드 에디터 | 214–220 | Longer BASIC listing, assembly/hex examples and command strings |
| 08 | Q&A | 262–265 | Mixed question/answer prose, assembly snippets and addressed byte tables |

For these pages **PDF page equals printed page**; July's +4 offset does not apply.
Starts, ends and adjacent pages were visually inspected. The contest review ends
on237;238 is a separate call for submissions and239 starts RECALC despite its
TOC start-page candidate of240. Unrelated advertisements on181,197–198 and220
must be explicitly excluded from both crop maps. Q&A ends265;266 is ad/index.
Figures, diagrams and screen images remain source images in both restorations;
the shared map will define exactly which surrounding text and table fields need
transcription before OCR. Graphic-glyph policy must be identical across routes.

The [selection manifest](ocr-august-pilot-selection.json) pins the source PDF,
canonical contents, page sets, categories and balanced processing order. The first
two pairs check instrumentation on prose and code. Engine-first order is randomized
within that two-pair block and within the remaining six, with seed198408 and four
first assignments per engine overall. Article order is fixed as above, not random.
Private contact sheets and boundary evidence are retained under
`private/pdf-restoration/13-1984-08-cost-pilot`.

## What the experiment measures

The main comparison is **paid assistant cost to produce a source-checked,
reviewable restoration of the same article**. Local model tokens, CPU/GPU use and
local elapsed time have zero monetary weight. Timings are still recorded as
diagnostics. Human review is mandatory, recorded separately and has no invented
hourly rate. Neither low raw CER nor a readable export constitutes human acceptance.

Measure each route from its frozen draft through semantic correction, source-image
inspection, necessary crop repairs/retries, assembly, validation and export. Keep
correction-only cost as a secondary breakdown. Shared layout preparation is charged
once in the experiment ledger, shown separately and added equally when presenting
comparable deployment scenarios. Do not charge one route all coordinator work.

Publish two different totals: (1) the observed expense of conducting both routes,
including comparison/reporting overhead, and (2) the scenario cost of choosing just
one route for these articles, with shared preparation counted once. The doubled
experiment's bill is not the production cost of either engine.

## Independence and consistent work

Each article/engine correction requires a **fresh context**, with the same model,
reasoning setting, instructions, tool access and output schema. It receives only
the source images, shared structural map and assigned raw draft. It must not read
the other route's raw or corrected text, notes, flags, token totals or decisions.
No reuse of a paid corrected transcription across routes. Source-only layout
preparation must not contain a hidden corrected answer key.

Use separate work directories and seal each result before paired comparison. The
coordinator may inspect both results only after both corrections finish. Do not
feed its post-comparison findings back into one correction and continue calling
that pass independent. Any second repair pass is a separate reported stage.
Fresh context removes cross-route conversational memory; it does not guarantee
identical cache state, stochastic behavior or true engine blinding. Avoid explicit
engine labels in correction instructions where practical, but do not claim that
draft style cannot reveal the engine.

The user explicitly authorized independent correction agents on October 12,
after this session's delegation rule initially blocked that step. Each agent uses
`fork_turns=none`, common instructions and inherited model/settings. Native session
metadata confirms `gpt-6-astra` with `high` effort for the launched cases. Do not
substitute two sequential corrections in the coordinator's shared conversation.

## Frozen OCR and review policy

- Use the same source pages, initial region map, render scale and crop bytes for
  both engines. Pin the current July-tested Qwen and Tesseract configurations and
  runtime/model identities before inference; do not tune against pilot answers.
- Tesseract uses the established code/prose language selection. Qwen uses the
  established deterministic transcription configuration. Record exact parameters,
  not only engine names. Common configuration reuse is distinct from answer reuse.
- Use one named primary engine throughout each arm. Bound looping/truncated calls;
  retain all attempts. Engine-specific crop repairs and reruns are allowed with
  their paid handling cost and provenance. Shared coverage defects found later
  require an explicit protocol deviation and comparable treatment of both arms.
- Do not silently fall back to the other engine in a pure-engine comparison.
  Record unresolved failures and any separately reported mixed-engine rescue.
- Correct spelling only against visible source, preserve printed technical errors
  with notes, check code literals/line numbers and table associations, and flag
  uncertain glyphs. Preserve coverage and source links. Both routes use the same
  existing restoration standard, without a target token budget or pressure to win.
- No reading-room rebuild is part of this pilot unless the user requests it.

## Usage, price and time accounting

Use per-run response records from each independent correction session. Deduplicate
response IDs; retain retries and failed attempts. Verify that child/session usage
is actually captured rather than assuming the coordinator log includes it. Record
session IDs, model/configuration, start/end timestamps and artifact pins privately.
Publish counts and pins, never conversation text or restored private content.

Record uncached input, cached input, cache-write input if applicable, output and
reasoning separately. Reasoning is a subset of output and must not be added again.
Capture source-image input and tool-result input through observed usage; missing
records are unknown, not zero. Use the same rate vector for both arms:

`cost = uncached_input * rate_uncached + cached_input * rate_cached + cache_write_input * rate_write + output * rate_output`

Use the actual applicable billing categories; the expression assumes each category
is disjoint. Record rates and units before producing currency totals. Until then,
publish the token vector and break-even pricing conditions. Also retain a sensitivity
view for cache effects instead of pretending fresh contexts guarantee equal caching.

Work windows include tool waits and helper work. Record raw worker and correction
intervals separately, including setup/model loading and retries, and subtract overlap
when forming elapsed unions. Never add nested recognition time to worker time. Keep
idle pauses, shared setup, comparison and final reporting separate. Record an audit
cutoff; final report/commit tails must be visible as excluded or included later.

## Measurement check and interpretation

After the first two pairs, verify separate session usage, complete source coverage,
reconciled token categories, isolated artifacts and comparable outputs. This is an
instrumentation check, not a stopping decision based on which engine looks cheaper.
If valid, continue the remaining six. If the protocol needs a material correction,
version it and disclose/re-run affected pairs rather than pooling incompatible runs.

Report article-level paired cost differences and ratios, median paired difference,
the total cost of each route across all eight articles, and descriptive content
breakdowns. Small strata of one article cannot establish a general routing rule.
Do not count crops as independent article replicates. More pages alone do not remove
single-run variability; consider a matched repeat only if an important decision is
close enough that the repeat is worth its paid cost.

After both passes are sealed, review disagreements against source and inspect a
fixed source-based sample that includes agreements. Agreement is not proof of
correctness. Human review should use neutral A/B labels and identical checks.
Report remaining errors, omissions and human repair separately, without declaring
either arm cheaper by tolerating poorer coverage or quality. Results remain
provisional until that quality comparison is completed.

Expansion to the whole August issue is a later decision. The pilot commits to eight
selected article pairs, not an automatic full-issue double restoration.

## First-two raw checkpoint, 2026-10-12

The editorial and game article now have four completed raw arms, with no failed
crops or retries. Their shared maps contain 41 regions: 37 text crops and four
source figures. Both engines received byte-identical PNG crops; Qwen's serialized
request image hashes also match. Source-only seam adjustments were completed
before inference and are recorded as shared preparation.

| Article | Engine | Worker seconds | Recognition seconds | Local model tokens |
| --- | --- | ---: | ---: | ---: |
| Editorial, p.20 | Tesseract | 6.85 | 3.34 | — |
| Editorial, p.20 | Qwen | 22.90 | 15.21 | 8,192 |
| Death Ski, pp.37–38 | Qwen | 43.27 | 35.28 | 16,578 |
| Death Ski, pp.37–38 | Tesseract | 8.25 | 4.74 | — |

Worker time includes runtime verification, crop copying and evidence export, plus
model startup for Qwen. Recognition time is a subset, not additional elapsed time.
Shared rendering/mapping is excluded. These are raw-stage diagnostics: all local
resources and 24,770 local model tokens have zero monetary weight in this study.
They do not yet answer the paid-cost question.

The frozen Qwen binary/model/projector hashes match the July-tested runtime.
Requests use temperature 0, seed 42, an 8,192-token context and 4,096 image tokens;
the ordinary output limit is 2,048 tokens, with a predeclared 512-token limit for
the graphic-character band on p.38. Tesseract uses OEM 1, PSM 6, one thread,
`eng` for code and `kor+eng` otherwise. Full configuration and input pins remain
with the private raw evidence. Each crop receives one bounded primary attempt;
failed native output is retained without fallback. The failure-preservation test
passes, including continued processing and refusal to overwrite an existing run.

Four separate correction packets were prepared in the frozen execution order,
with common instructions, source images, structural templates and one assigned
draft each. All were initially unstarted; following explicit authorization, the
independent correction stage below began. The first-two instrumentation gate has
now passed; the other six articles follow next. No reading-room rebuild
was performed.

The [progress manifest](ocr-august-pilot-progress.json) records artifact pins and
completion state. The [coordinator usage audit](ocr-august-pilot-usage.json) records
shared setup, preparation and orchestration through its explicit cutoff, including
between-window overhead. Independent correction-session usage is reported separately.
Coordinator helper work overlapped raw runs, so those paid tokens are shared
experimental overhead, not attributed to whichever local engine was running.
The subsequent validation, commit and delivery tail remains outside that cutoff.

## First independent pair, 2026-10-12

Both editorial restorations are sealed. Their exports contain all 14 text regions
and one original figure; export integrity and byte-identical rebuild were checked
independently by the coordinator. Input manifests confirm that neither correction
changed its assigned draft, source images, map or common instructions.

| Editorial route | Uncached input | Cached input | Output | Worker-declared seconds |
| --- | ---: | ---: | ---: | ---: |
| Tesseract | 36,080 | 346,240 | 4,513 | 129.95 |
| Qwen | 32,005 | 390,656 | 4,228 | 125.69 |

Cache-write input is zero in these observed records. Output already includes 391
and 656 reasoning tokens respectively. Usage covers each fresh session from its
creation through the coordinator observing completion, including instructions,
source inspection, correction, export checks and final reply. Worker-declared
time excludes initial instruction loading and final reply; the longer audit window
also includes observation delay and is not active correction time. The native
response IDs are distinct across the two sessions and absent from the coordinator
log. The [independent usage audit](ocr-august-pilot-correction-usage.json) retains
counts, model/settings, artifact pins and timing scopes without conversation text.

All 14 corrected regions agree after removing whitespace. Three differ in spacing.
The coordinator checked those disagreements plus the predeclared title/opening/
middle/ending sample against source, finding no confirmed character error in the
checked regions. One additional blurred syllable has the same reading in both
versions; only the Tesseract arm flagged it. A shared human-review flag records
that ambiguity without modifying either sealed result. This check establishes
comparable reviewable coverage, not character-perfect text or human acceptance.

This single prose pair is not an engine decision. Qwen used 4,075 fewer uncached
input and 285 fewer output tokens, but 44,416 more cached input tokens. Under the
common rate vector above, its correction cost is lower exactly when
`44,416 * rate_cached < 4,075 * rate_uncached + 285 * rate_output`.
No billing rates or currency total are assumed. Shared preparation and comparison
remain separate overhead; the remaining cohort is still required.

## First-two measurement gate passed, 2026-10-12

The game pair also has complete, independently verified exports: 23 text regions,
three original figures, 80 physical and 68 logical listing rows in each version.
All four correction sessions used the same model/effort, have separate reconciled
usage and unchanged assigned inputs, and passed export/rebuild checks. Every
corrected-text disagreement and the fixed source samples were inspected. The
remaining six pairs may proceed under the unchanged protocol.

| Game route | Uncached input | Cached input | Output | Worker-declared seconds |
| --- | ---: | ---: | ---: | ---: |
| Tesseract | 48,875 | 750,336 | 8,177 | 243.91 |
| Qwen | 64,062 | 693,504 | 7,538 | 243.72 |

Cache-write input remains zero. Output includes 1,285 Tesseract-route and 1,703
Qwen-route reasoning tokens. Qwen's game correction uses 15,187 more uncached
input, 56,832 fewer cached input and 639 fewer output tokens. It costs less only
when `56,832 * rate_cached + 639 * rate_output > 15,187 * rate_uncached`.
Across both articles together, the corresponding condition is
`12,416 * rate_cached + 924 * rate_output > 11,112 * rate_uncached`.
No actual billing rates have been supplied, and two single runs cannot establish
a general routing rule.

The game versions agree exactly in 18 of 23 text regions. Of the five differences,
two are wording disagreements: source inspection confirms one retained wording
error in each arm. The other three concern explicitly flagged Unicode graphic
approximations or nonliteral placeholders whose original images are preserved.
These placeholder differences are not counted as ordinary OCR character errors.
The fixed sample found no additional confirmed character errors. The sealed
independent outputs remain unchanged; source-linked findings are available for
human correction. Neither version is claimed to be runnable or character-perfect.

The private gate record and paired source-review records are pinned in the public
progress manifest. Human acceptance remains pending for both articles. Passing
this gate establishes usable instrumentation and comparable reviewable coverage;
it does not declare an accuracy or cost winner.

## Contest review pair completed; BASIC article underway, 2026-10-12

The contest review has 17 text regions and one figure in each verified export.
Both routes preserve all six table columns, four data rows and the printed empty
cell. TSV and Markdown formats differ, but 23 of 24 data cells agree after ignoring
whitespace. The remaining cell contains a blurred personal name: both readings are
retained for human confirmation. The Qwen arm explicitly flagged it; the Tesseract
arm did not. Source inspection also found one wording error in the Tesseract arm.
All five differing regions and the fixed source sample were inspected. Neither
sealed output was changed after comparison.

| Contest-review route | Uncached input | Cached input | Output | Worker-declared seconds |
| --- | ---: | ---: | ---: | ---: |
| Tesseract | 33,297 | 492,928 | 4,785 | 147.78 |
| Qwen | 34,322 | 461,952 | 6,532 | 197.06 |

Cache-write input is zero; output includes 533 and 1,282 reasoning tokens
respectively. Qwen costs less for this pair only when
`30,976 * rate_cached > 1,025 * rate_uncached + 1,747 * rate_output`.
This is another single-run observation with disclosed residual quality differences,
not a general cost conclusion. Raw worker time was 7.59s for Tesseract and 26.13s
for Qwen; it has zero monetary weight.

The next article, BASIC technique / PASSWORD & LOGIN (pp.65–68), has 79 shared
regions: 73 text crops and six source figures. Its ten code/monitor examples have
separate structural groups, preserving listing boundaries and wrapped rows. Both
raw arms completed without failures: Qwen 59.93s, Tesseract 14.46s worker time.
Correction packets use the unchanged common instructions; the first is running.
Its results and costs remain unknown until sealed. No reading-room rebuild.

## Fourth pair and VISICALC coverage amendment, 2026-10-12

BASIC technique has 73 text regions, six original figures and ten separate code
examples. Both exports passed integrity checks and byte-identical rebuilds. All
10 differing regions and the fixed sample (including every code example) were
source-checked. One source-fidelity error per route remains: the Qwen correction
normalized a printed prose typo; the Tesseract correction normalized a printed
code-string spelling. One literal-space count is unresolved. Human review remains
pending, and sealed outputs have not been repaired using paired findings.

| BASIC technique correction | Uncached input | Cached input | Output |
| --- | ---: | ---: | ---: |
| Qwen | 103,249 | 1,194,240 | 8,614 |
| Tesseract | 78,521 | 1,546,496 | 11,931 |

Qwen costs less for this pair iff `352256*c + 3317*o > 24728*u`, where
`u`, `c`, and `o` are common per-token uncached-input, cached-input and output rates.
No billing rates or currency totals are assumed.

**Protocol amendment for aug-05 only:** the first independent VISICALC agent
found an omitted physical line above region p185r15. Its original shared crop
started at y=1112; version 2 starts at y=1080 (1132×1600 reference coordinates).
All other crop bytes are unchanged. All five page overlays were checked again.
Original raw artifacts and the aborted correction are preserved. The other
original correction had not started. Both complete raw arms are rerun with the
same settings and engine order, followed by two new fresh-context corrections.
No corrected text is reused. This amendment changes coverage, not review standards.

The initial Qwen raw pass also reached its output limit at p182r21; its failed
response and 2,701 local tokens remain recorded. The initial aborted correction
used 47,297 uncached / 301,056 cached input and 1,686 output tokens. These are real
paid recovery costs, reported separately from matched version-2 correction and
included in a recovery-cost sensitivity view. An unstarted arm is not a completed
zero-cost restoration. Local rerun resources remain priced at zero. The private
`aug-05-v2/protocol-deviation.json` pins the defect and recovery policy.

## Fifth and sixth pairs completed, 2026-10-12

VISICALC version 2 has 91 text regions and five source figures per arm. Both
exports include the recovered first line and passed integrity/rebuild checks.
All 47 differing regions and the fixed sample were source-checked: 52 regions
in total, including all ten worksheet/table companions. The Qwen-based correction
retains eight confirmed wording/number errors and one punctuation omission in
those regions; the Tesseract-based correction has none confirmed there. Several
Qwen-route errors normalize printed spellings, and one changes a worksheet ZIP
code. These are sampled fidelity findings, not full CER or a raw-OCR ranking.
Original worksheet images and unresolved punctuation remain available for human
review. Both sealed corrections remain unchanged.

The hardware article has 56 text regions, seven original figures and three BASIC
listings. Both versions preserve all 40 physical / 29 numbered listing rows,
including wrapped numbers and addresses. All 15 differing regions and the fixed
sample were checked (21 regions total). One Korean wording error was confirmed
in the Qwen-based correction. Other differences concern table markup, whitespace
and explicit approximations of circuit symbols. Source diagrams and tables remain
available; human acceptance is pending.

| Article / route | Uncached input | Cached input | Output | Correction worker seconds |
| --- | ---: | ---: | ---: | ---: |
| VISICALC / Qwen | 113,749 | 882,048 | 10,183 | 404.04 |
| VISICALC / Tesseract | 101,602 | 994,048 | 10,666 | 300.46 |
| Hardware / Qwen | 73,471 | 739,072 | 8,513 | 241.64 |
| Hardware / Tesseract | 67,797 | 753,280 | 8,948 | 248.01 |

Output includes reasoning; cache-write input is zero. Under common per-token
rates `u,c,o`, Qwen's matched correction costs less for VISICALC exactly when
`112000*c + 483*o > 12147*u`, and for hardware when
`14208*c + 435*o > 5674*u`. The VISICALC aborted correction remains additional
recovery cost, separate from these matched version-2 numbers.

All eight matched raw pairs are now complete. A second geometry amendment affects
only the long editor article: additional source inspection after its first map
freeze, before any inference, moved the shared boundary between p218r18/r19 from
1001.2 to 1003.2 reference pixels to a verified blank raster row. The original map
is preserved and was never used for raw or corrected output. Both actual routes
use `aug-07-v2`; region count, content and correction standards are unchanged.
This pre-inference amendment incurred no aborted correction. The private
`aug-07-v2/protocol-deviation.json` records it.

## Seventh pair completed; Q&A underway, 2026-10-12

The editor has 151 text regions, six figures and 106 logical listing rows per
verified export. Its 292 versus 293 physical-row count differs by one blank row;
a continuation assigned to adjacent crop IDs differently appears exactly once in
both assembled listings. All 76 differing regions plus the fixed sample were
source-checked, 81 regions total. Checks found four wording/number/code-token
errors and two punctuation errors in the Tesseract correction, and two code-token
errors in the Qwen correction. Faint glyphs and literal spaces remain uncertain.
These are checked-region observations, not full CER or runnable-code certification.

| Editor correction | Uncached input | Cached input | Output | Worker seconds |
| --- | ---: | ---: | ---: | ---: |
| Tesseract | 127,514 | 2,528,896 | 19,640 | 561.03 |
| Qwen | 220,265 | 1,897,728 | 15,403 | 533.72 |

Qwen's matched correction is cheaper only when
`631168*c + 4237*o > 92751*u`. Its lower total-token count is not sufficient to
settle monetary cost, because it consumed more uncached input. The native audit
includes the full sessions, including metadata-only progress communication.
Fourteen independent restorations are sealed; the final Q&A pair is underway.

## Pilot complete: all eight pairs compared, 2026-10-12

Q&A exports contain 112 text regions, one figure and 72 physical listing rows each.
All 33 disagreements and the frozen sample were checked against source, 46 regions
in total, including all eight assembly examples and the BASIC groups. Ten wording
errors were confirmed in the Qwen correction (nine historical spelling changes
and one verb error); the Tesseract correction has three wording errors and two
omitted punctuation marks in checked regions. Uncertain punctuation/handwriting
remains flagged. Printed assembly inconsistencies are preserved by both versions.

| Q&A correction | Uncached input | Cached input | Output | Worker seconds |
| --- | ---: | ---: | ---: | ---: |
| Tesseract | 94,089 | 1,124,352 | 12,619 | 375.94 |
| Qwen | 89,871 | 1,098,368 | 11,303 | 333.66 |

This Qwen correction uses fewer tokens in every captured category, but unequal
residual quality prevents treating that as a measured saving to identical accepted
text. Human review and any paid repair pass are still pending for all eight pairs.

Across the matched cohort Qwen uses 143,219 more uncached input, 1,179,008 fewer
cached input and 8,965 fewer output tokens. Its cost is lower when
`1179008*c + 8965*o > 143219*u`. At illustrative rates `u:c:o = 1:0.1:4`, the
matched total is only 0.60% lower for Qwen; four articles favor each route, and the
median article ratio is 1.005. Adding the observed coverage-abort cost makes the
Qwen route 4.17% higher under that same hypothetical rate vector. Neither figure
is an actual bill or an estimate of inherent engine recovery risk.

The [results report](OCR-AUGUST-PILOT-RESULTS.md) and
[machine-readable results](ocr-august-pilot-results.json) consolidate all eight
articles, matched/recovery cost, raw/correction time, source fidelity and shared
experimental overhead. Sixteen matched raw arms plus two original coverage-recovery
arms were executed. No automatic whole-issue expansion or reading-room build was
performed. The existing content-routing heuristic remains provisional; this trial
does not establish a generally cheaper engine or a validated cost router.
