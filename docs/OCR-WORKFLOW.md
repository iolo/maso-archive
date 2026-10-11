# Sustainable OCR workflow experiment

See [PLAN-OCR.md](../PLAN-OCR.md) for the objective and human-review requirements.
This experiment prepares three alternatives from **identical reviewed crops**:
A: Tesseract; B: independent Qwen transcription; C: local Qwen correction proposals
using the image and both drafts. The final semantic correction and human acceptance
stages remain necessary. This is preparation for measuring end-to-end savings;
its reference scores do not establish savings by themselves.

## Prepare and resume

Use the existing private three-page manifest created by `prepare-trial` in the
[Qwen OCR guide](OCR-QWEN3-VL.md):

```sh
python3 -m tools.ocr_qwen workflow \
  --manifest private/ocr-qwen3-vl/samples.json \
  --output private/ocr-qwen3-vl/new-workflow

# Same inputs, code, models and inference settings:
python3 -m tools.ocr_qwen workflow \
  --manifest private/ocr-qwen3-vl/samples.json \
  --output private/ocr-qwen3-vl/new-workflow --resume

# An interrupted stage has no completed checkpoint. Explicitly retain/archive
# that partial attempt and retry it, reusing all completed stages:
python3 -m tools.ocr_qwen workflow \
  --manifest private/ocr-qwen3-vl/samples.json \
  --output private/ocr-qwen3-vl/new-workflow --resume --retry-incomplete

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
  --ledger private/ocr-qwen3-vl/new-workflow/review-ledger.json
```

The checker rejects missing prepared page/arm/region records, automatic acceptance,
text regions disguised as figures, missing final text files, and invalid recorded
usage/time. Actual savings remain unmeasured until comparable review records exist.

## First mapped-crop trial — 2026-10-09

Private run: `private/ocr-qwen3-vl/workflow-03/`. Public, transcription-free
[measurements](ocr-workflow-measurements.json) were generated with:

```sh
python3 -m tools.ocr_workflow_report \
  --run private/ocr-qwen3-vl/workflow-03 \
  --output docs/new-workflow-measurements.json
```

All 20 text regions and three figure regions are represented. Sixty stages
completed: 20 Tesseract calls, 20 independent Qwen OCR calls and 20 local
correction calls. Every reference, source image, crop hash and completed stage
manifest was checked. An unchanged resume reused all 60 stages, performed zero
inference, and started no additional server.

One serial preparation run per arm, using the same hardware/model as the original
benchmark. Preparation seconds exclude startup, shared crop preparation and final
review. C includes the complete A+B+correction dependency cost. Compact CER removes
all whitespace; BASIC scores only the 29 resolved numbered lines.

| Sample | Arm | Preparation seconds | Compact CER | Local prompt + output tokens |
|---|---|---:|---:|---:|
| prose | A-tesseract | 4.04 | 4.94% | 0 |
| prose | B-qwen | 19.23 | 0.79% | 6,471 |
| prose | C-local-correction | 53.78 | 0.53% | 17,797 |
| basic | A-tesseract | 1.63 | 2.41% | 0 |
| basic | B-qwen | 17.50 | 0.00% | 5,894 |
| basic | C-local-correction | 42.07 | 0.13% | 15,733 |
| figures | A-tesseract | 3.19 | 7.39% | 0 |
| figures | B-qwen | 12.66 | 0.57% | 4,773 |
| figures | C-local-correction | 29.72 | 0.32% | 12,529 |

These are local llama.cpp tokens, not paid-model tokens. B requires only its own
recognition stage, while C needs both initial drafts and the correction pass.
Across the three pages, B used 17,138 local tokens; C used 46,059 including B.
Human review time, capable-model tokens and accepted-page savings remain null.

Using reviewed geometry removed the earlier automatic-layout omission on the
diagram page. Qwen draft compact CER there was 0.57%, versus 28.90% in the earlier
automatic-layout trial. This is a different pipeline configuration, not a repeat
measurement of the earlier automatic detector.

The correction pass improved reference edit distance in four regions and worsened
it in three. It appended an extra character to a previously reference-matching
BASIC line and changed a previously matching heading; some regressions had no
uncertainty note. Thus disagreement/uncertainty flags help organize review but
cannot certify or automatically accept any text. The prose reference remained
slightly better matched overall after correction; BASIC became slightly worse.

For now, **B is the simplest promising partial alternative**: use local Qwen on
established crops as the draft for the existing semantic/human correction work.
C remains an optional proposal source whose extra effort must earn its place in
a timed review. No arm has received human acceptance in this experiment.

### Ready for review

- [Prose packet](../private/ocr-qwen3-vl/workflow-03/prose-review.md)
- [BASIC packet](../private/ocr-qwen3-vl/workflow-03/basic-review.md)
- [Diagrams/prose packet](../private/ocr-qwen3-vl/workflow-03/figures-review.md)
- [Human review ledger](../private/ocr-qwen3-vl/workflow-03/review-ledger.json)

All three packets include the full page, crops and all A/B/C drafts. The next
checkpoint is actual review with recorded active time and available capable-model
usage; that checkpoint is deliberately not marked complete by these scores.

### Development attempts and verification

`workflow-01` retains a rejected, truncated correction response caused by looping
explanations. Its replacement schema bounds uncertainty notes. `workflow-02`
completed, but an attempted resume overlapped a surviving worker after an
interruption; its timings are excluded. A per-run OS file lock now prevents
concurrent writers. Only the fresh serial `workflow-03` supplies this table.
These development attempts consumed additional local compute not included in
steady preparation costs; they are not hidden as successful ordinary runs.

24 OCR/workflow tests pass, covering reference isolation, truncation, raw evidence,
cache tampering, concurrent-run exclusion, review coverage, explicit human
acceptance and cost dependency accounting. The prepared ledger reports zero
accepted pages. No historical scan/transcription/package was modified.

## June 1984 practical adoption

The maintainer authorized the whole June issue using arm B as the raw draft for
assistant scan-based semantic correction and mandatory human review. This trial
runs alongside the measurement experiment; no human acceptance is inferred.
The issue queue and ledger are under `private/pdf-restoration/12-1984-06-qwen/`.

For inspected restoration maps, use the mapped adapter:

```sh
PYTHONPATH=src python3 -m tools.ocr_qwen.mapped \
  --request private/pdf-restoration/12-1984-06-qwen/batch-01-corrected/request.json \
  --output private/pdf-restoration/12-1984-06-qwen/batch-01-corrected/ocr
# Add --resume only for unchanged inputs/settings/implementation.
```

A request contains `batch_id`, optional `scale_to` (1000–6000; default3000), and
`articles: [{"map": {"path": "private/.../map.json", "sha256": "...", "bytes": 123}}]`.
Paths are repository-relative. At most three mapped articles and twelve distinct
source pages are allowed. The adapter validates source/TOC pins, orientations and
exclusions, retains every crop and original figure, and transcribes text regions
without automatic layout or a local correction pass. Inspect crops for clipping
as well as full-page coverage before accepting results. An unchanged completed
resume reuses immutable stages without starting a server. An incomplete failed
stage is retained and requires a fresh output; this adapter currently has no
`--retry-incomplete` option.

Each article directory contains an existing-format `evidence-bundles.json` and
per-page `evidence.json`, raw text, settings and positions JSON. Positions are
explicitly **region-level only** and include the native response; Qwen has not
provided word boxes. Export recipes specify `runtime_directory` relative to the
repository and the pinned `runtime-fingerprint.json`. Recipes omitting that field
continue to use the original Tesseract runtime directory. Export still requires
explicit scan-linked correction outcomes for every region. Record human acceptance
separately from the legacy `sample-reviewed` assistant review status.

Rollback requires selecting the retained Tesseract path and generating fresh raw
OCR/evidence for the same reviewed maps; previous OCR, maps and corrections are
never overwritten. No public reader installation is part of raw OCR execution.

### June checkpoint01 result

Pages19–22 now have23Qwen text results, one preserved original figure, assistant
scan-based correction records and three validated data packages. The editorial
and parent overview have complete extents; the technical child includes only22.
All three packages rebuild byte-identically. Cache-only resume reused23 stages
with zero new calls or additional server starts. Whole June remains in progress.

Successful recognition used58.72s and27,287local tokens, excluding rendering,
startup and review; sampled peak GPU was7,842MiB. An initial crop-mapping attempt
is retained and adds58.63s/27,309tokens. This is a practical checkpoint, not a
controlled accuracy/savings measurement. Human time and capable-model usage are
unmeasured. [Sanitized checkpoint/pins](ocr-june-progress.json) includes both runs.

Private review packets include all regions, including agreements:

- [Editorial19](../private/pdf-restoration/12-1984-06-qwen/batch-01-corrected/ocr/scan-maso-1984-06-toc-0038/review.md)
- [Feature overview20–21](../private/pdf-restoration/12-1984-06-qwen/batch-01-corrected/ocr/scan-maso-1984-06-toc-0001/review.md)
- [Technical opening22](../private/pdf-restoration/12-1984-06-qwen/batch-01-corrected/ocr/scan-maso-1984-06-toc-0002/review.md)
- [Human review ledger](../private/pdf-restoration/12-1984-06-qwen/batch-01-corrected/human-review-ledger.json)

All human acceptance is pending. Qwen sometimes modernized historical endings,
smoothed a printed duplicate or substituted more plausible wording; correction
records preserve the scan reading. Those findings support retaining semantic
review against the original image even when raw OCR reads fluently.

### June33–38: more difficult tables and photographed code

The next six-page checkpoint is assistant-reviewed and exported, with64 phoneme
rows,11 timing rows,39 sample-code rows and11 retained images. Small glyphs still
require human decisions. [Private review entry](../private/pdf-restoration/12-1984-06-qwen/REVIEW-PHONEME.md)
links source crops, raw drafts, corrections and the human ledger. Full article
extent33–47 is verified;39–47 remain queued.

Five identical PNG crops were tested with the existing pinned Tesseract setup
(OEM1/PSM6, kor+eng for prose/tables and eng for code), following Qwen inference.
The references are assistant scan-corrected Qwen-derived readings prepared before
seeing Tesseract output. This is a selected, unblinded diagnostic, not independent
human gold or representative whole-issue accuracy.

| Diagnostic | Qwen | Tesseract |
| --- | ---: | ---: |
| Two prose crops: compact CER,611 reference characters | 0.16% | 14.08% |
| Faint code crop: compact CER,321 reference characters | 0.62% | 42.68% |
| Phoneme table cells,8 uncertain cells excluded | 311/312 | 260/312 |
| Five crops, raw engine seconds | 18.65 | 2.27 |

Compact CER removes whitespace after NFC normalization. Cell comparison retains
row order and uses five cells per row without inferred code repair. Qwen's sole
scored cell difference is dash typography (em dash versus reference minus), not
an established substantive error. An additional
eng-only Tesseract table run scores265/312; its Korean example cells still count.
[Full measurements and limits](ocr-june-batch04-comparison.json) include per-crop
results, settings, image pins and sampled resources.

Tesseract is faster at recognition on these crops. Qwen's cleaner drafts suggest
less downstream correction work, but that effort and paid-token savings remain
unmeasured. Corrected six-page Qwen preparation took89.95s including render/startup;
69.03s was regional inference. An initial table-boundary attempt adds90.19s and is
retained in [checkpoint accounting](ocr-june-progress.json). New geometry requires
native-size boundary inspection; readable model output alone is not proof of a
complete crop. No automatic acceptance or publication occurred.

## June continuation39–44: code-focused diagnostic

Batch05 restores23 text regions and8 original images, including14 paired table
rows and255 numbered main-program rows. The source program is separate from the
short sample on38. Closing prose/references are covered;45–47 and full article
assembly remain pending. The [review entry](../private/pdf-restoration/12-1984-06-qwen/REVIEW-PHONEME.md)
links both preserved packages and their human ledgers.

Four crops were selected before inference: one prose and three code crops.
Assistant source-corrected references were pinned before Tesseract inspection.
The same PNG files and existing engine settings were used, with eng for code
and kor+eng for prose. These are unblinded diagnostics, not independent human gold.

| Diagnostic | Qwen | Tesseract |
| --- | ---: | ---: |
| Prose compact CER,161 reference characters | 1.86% | 11.80% |
| Code compact CER,843 reference characters | 0.12% | 47.81% |
| Exact numbered code rows,quoted spaces retained | 56/58 | 0/58 |
| Four crops,raw engine seconds | 11.35 | 1.24 |

Prose includes one provisional damaged-glyph reading. Compact CER ignores all
whitespace, which can hide errors inside code literals. The additional row check
preserves spaces inside single quotes while ignoring alignment elsewhere; it
requires one exact printed line-number match. This strict score measures source
transcription, not executable correctness. No assembly or execution was performed.
[Measurements](ocr-june-batch05-comparison.json) retain sample hashes and resources.

Source checking found an invented comment marker on ORG, an EOPEN misreading,
quoted-character errors and shortened banners. Printed source misspellings and
truncated comments were retained. Six unresolved readings remain for human review.
Qwen preparation took99.38s, including57.06s of regional inference; it used29,727
local tokens and sampled peak GPU7,838MiB/RSS6,450MiB. Cache resume reused all23
stages; the export rebuild is byte-identical. Human-time and paid-token savings
remain unmeasured. Continue selected comparisons by content type over subsequent
checkpoints without treating these diagnostics as automatic acceptance.

## June ending45–47 and complete article review

Batch06 completes the phoneme article with11 text regions,3 images,109 numbered
program rows and64 symbols. The assembled33–47 package has74 text regions and
22 images. Its39-row sample and364-row main program are distinct. Native table
indexes retain156 rows including headers; their projected text is checked exact.
Nineteen source readings remain unresolved and all96 regions await human review.

Two code crops were selected before inference and their assistant source references
fixed before Tesseract. [Measurements](ocr-june-batch06-comparison.json):

| Diagnostic | Qwen | Tesseract |
| --- | ---: | ---: |
| Compact CER,716 reference characters | 0.98% | 41.76% |
| Exact numbered rows,quoted spaces retained | 43/50 | 0/50 |
| Two crops,raw engine seconds | 7.74 | 0.70 |

The symbol table is not scored. FILENM punctuation remains a candidate reading.
Outside these samples, Qwen substituted Chinese characters for $$$; source review
also repaired quote marks, banner counts and literal indentation. Printed cut-off
strings remain cut off, and blank error-summary fields remain blank. The reference
is unblinded and Qwen-derived, not independent human gold. These small diagnostics
support continued evaluation, not a whole-issue accuracy or downstream savings claim.

Batch preparation took68.42s including rendering/startup/export; regional inference
40.16s and19,254 local tokens, sampled GPU7,940MiB/RSS4,720MiB. Native and assembled
rebuilds match byte-for-byte; resume used11 cached stages with no new inference.

The [reading-room preview](READING-ROOM.md) now supports human review without
reading JSON: whole article and tables, scan/correction comparison, region controls,
zoom, raw OCR and source notes. It remains read-only and does not convert viewing
into acceptance. Use the region URL when reporting a correction. Human review
and paid-model effort remain unmeasured; continue the matched-crop protocol.

## Complete June issue experiment

See the [consolidated decision report](OCR-JUNE-DECISION.md) for weighted accuracy, matched-crop runtime, local token/retry accounting, resource peaks and the remaining sustainability measurements.

All 38 canonical article bodies are now assembled across 216 source pages, with
seven non-owning headings accounting for all 45 contents entries. The
[coverage ledger](ocr-june-accounting.json) separates availability from review:
all 38 are readable and assistant sample-reviewed, with zero human acceptances.
The packages contain 3,082 mapped regions and 325 explicit unresolved-text flags;
these flags are review aids, not an exhaustive error count.

The experiment supports Qwen as a useful raw-OCR option before semantic correction,
particularly for Korean prose and ordinary printed source code. It does not yet
establish savings in paid tokens or human review time. Region mapping, continuation
assembly and scan comparison still require work; graphic characters and dense
or faint tables remain difficult. Repetition loops, interrupted runs and manual
fallbacks are recorded in their checkpoints. Some rebellion-game graphic literals
remain explicit scan-linked placeholders. No program is certified executable.

The final appendix comparison covers prose, a name/address table and editor
commands: compact CER 0%/0%/6.11% for Qwen versus 4%/4.88%/54.15% for Tesseract.
[Index scores](ocr-june-batch41-comparison.json) separately retain a post-hoc
leader-normalized diagnostic because dotted leaders distort edit distance. All
comparisons use assistant scan-corrected Qwen-derived references, fixed before
Tesseract but unblinded; none is independent human gold or a whole-issue accuracy
estimate. [Progress](ocr-june-progress.json) records individual timing, resources,
failures, cached resumes and package hashes rather than extrapolating savings.

The [complete reading-room preview](READING-ROOM.md) is the next stage: review
whole articles and source-linked regions, return corrections with their region
URLs, then record explicit human decisions. Merely opening a page does not accept
it. Keep the current correction workflow and use this issue to measure the work
remaining after local OCR.


## July content and cost trial

The maintainer selected July1984 for the next trial. See [the trial plan and
measurements](OCR-JULY-TRIAL.md) for opposite engine assignments across content
categories, actual assistant usage accounting, and matched raw-OCR samples.
Twenty-two complete July article bodies are recorded in
[July progress](ocr-july-progress.json), including the fully assembled CP/M and
Z80 lessons, computer graphics and Apple FORTRAN. Fourteen bodies remain incomplete, including the partly restored Information Radar;
six unpaginated TOC parent headings are tracked separately. All human acceptances
remain pending.

The [provisional engine-selection heuristic](OCR-JULY-TRIAL.md#provisional-engine-selection-heuristic)
starts with Tesseract for clear prose, Qwen for tables/technical notation/listings,
and original images for diagrams and musical-symbol bands. It includes bounded probes, explicit fallback
accounting and evidence limitations. The graphic-heavy code exception tested in
batch19 required extensive Tesseract repairs and remains unproven. Batch20 also
requires checking every repeated numeric/CHR$ term for silent Qwen omissions. Batch21
adds mixed evidence: Tesseract wins the sampled clear prose and assembly row order;
Qwen wins the numeric table and hex dump. Check column association and plausible
source normalization before trusting technical output. Batch22 retained all short Logo
procedure rows, but prefix quotes and historical wording still required source checks.
Batch23 retained57 BASIC lines but needed HPLOT, punctuation and bitmap Hangul
corrections. Its English-only Tesseract code alternate limits conclusions about
Korean strings. Batch24 adds scan-quality evidence: mottled-background ordinary
prose needed substantial Tesseract repair, while all four fixed samples favored
Qwen. Qwen still reversed a power-off instruction and modernized historical wording.
Its raw run was contaminated by erroneous recovery and competing model startup;
exclude its elapsed time from clean speed comparisons. Batch25 completed without
retry and again favored Qwen in four samples, but needed TEMP.$$$ and comment-row
repairs. Source comparison must check file extensions, row boundaries and original
command punctuation. Batch26 adds an ORG/address-row merge that lost an LD operand
row; count directives separately from addressed rows. Its fixed arithmetic-layout
sample favored Tesseract, but divider/arrow representation affects CER. CP/M101–113
and Z80 lesson119–127 are fully assembled. Batch27 produced two Qwen length-limit
loops on thin stacked opcode rows. Preserve original table images and use a
recorded bounded Tesseract fallback for affected/remaining homogeneous rows;
check every cell, since Tesseract also corrupts flag/opcode symbols. Both failed
costs and changed assignments remain in the audit. Table CER is typography-sensitive;
this exception does not establish a paid-cost advantage. Batch28 color-table
output also repeated escaped tabs to the cap, so use a bounded Tesseract probe
before committing other ruled-table groups to Qwen. Preserve all failed costs.
For BASIC, check isolated continuation characters: batch28 omitted one I and six
0 rows, and separated a DATA listing into label/value columns while changing
scores. Audit every row/field; do not reconstruct source anomalies from expected
program behavior. Full graphics128–134 is restored with135 BASIC lines.
Batch29 uses bounded Tesseract probes to distinguish compiler printouts from
numeric-output tables: Qwen for compiler/handwriting, English Tesseract for two
numeric tables, with every cell source-checked. Qwen still won the fixed numeric
sample, so usable row structure is not evidence of better accuracy or paid cost.
Check compiler line counters/offsets against statements, and retain misspellings
such as source COLUMMN even when Qwen silently normalizes them. Full Apple
FORTRAN137–142 is restored with73 source rows; no program execution. Batch30
restores Information Radar domestic news143–148. Its Tesseract table probe was
reused as primary after matching the exact crop hash; count that recognition once.
Visually clear ruled headlines sometimes returned blank/fragmented Tesseract text;
check heading coverage separately and restore isolated failures from the source.
All four fixed samples favor Qwen, including ordinary news and the selected table.
That does not establish causal paid savings for either engine. Batch31 restores
foreign149–153 with39 Tesseract/117 Qwen crops. A rejected bounded Tesseract
headline probe informed Qwen routing; its distinct crop is extra preparation cost,
not reused primary evidence. Qwen still misread two headline words, although it
won all four fixed samples. Preserve conflicting chip numbers, source totals and
faint decimal uncertainty without technical repair. A SIGTERM after78 Qwen
successes resumed with exact evidence reuse; both worker lifespans are measured,
but interrupted response tokens remain unknown. Batch32 completes154–157 with
52 Tesseract/65 Qwen crops and another48-success cache reuse after SIGTERM.
Check repeated syllables at crop line breaks and keep printed errors such as
onrmal and Compag. Unicode superscripts/Roman numerals affect compact CER; the
four fixed samples favor Qwen, with Tesseract close on Lisp specs. Full Information
Radar143–157 is assembled with426 regions and8 images. Source153/154 wraps and
all review anchors are preserved;158 is a publisher advertisement.
VISICALC164–168 is now complete in33. Its English Tesseract dot-matrix table
probe was badly corrupted, so Qwen was selected; the unchanged probe was reused
only as an alternate comparison, counted once as setup cost. Qwen got all63
numeric values but omitted coordinates and linearized the table, so numeric
accuracy does not establish layout completeness. Restore circled keys/boxed
cells against scans and preserve printed LIVE/SERLES5/MATN anomalies rather
than repairing commands.116 physical command/annotation rows remain unexecuted.
Data structures169–174 is complete in34, with38 Tesseract/110 Qwen crops,
107 PL/I rows and22 source images. Preserve printed procedure names, duplicate
prose and apparent code errors; faint DELETEQ and ADDQ punctuation need explicit
human review flags. The four fixed samples favor Qwen on introductory prose and
both code crops, but technical prose ties at0% compact CER. A failed recovery
startup is included in raw time; archive incomplete requests before resuming,
reuse successful stages and retain all attempt costs. UNIX175–181 is complete in35;182ad/183divider are outside the article. Its
80T/98Q route completed, then five clipped page177 body crops were widened and
rerun. Preserve original and revised maps/OCR and count all103 Q calls; reusing
unchanged evidence avoids duplicate recognition. Qwen wins all four fixed samples
(outline, plain prose, technical prose, memory rows), with all seven memory pairs
matching assistant source reading. Preserve printed Entory/CEC/비전 and other
source anomalies; retain original diagrams and small-glyph review flags. Next
inspect hardware195–206 and verify its boundary. This is guidance for choosing new checkpoints;
explicit mixed-region assignments are recorded, while no automatic classifier or
pipeline default has changed. The2026-10-11 full-issue
goal now authorizes a reading-room build after restoration and metric consolidation.

### Assembly across a shared source page

When an article segment ends halfway down a page, a later segment may restore the
remaining regions. Declare that page in the assembly recipe's `shared_pdf_pages`
and supply `resolved_exclusions` (an empty list when no exclusion is resolved).
Page metadata and orientation must match; included regions from different segments
must not overlap. Undeclared shared pages continue to be rejected.

A deferred exclusion may be removed from the combined map only through an explicit
record with `segment`, `region_id`, `restored_by` and `reason`. The restoring
segment's regions on that page must lie inside the original exclusion. This checks
geometry and provenance; the recipe's source-inspection evidence must still justify
complete content coverage. Original segment maps, exclusions, OCR and corrections
remain immutable in the assembly. Shared-page checks run again during export
verification, including when the assembled artifacts have been rehashed.

### Repetitive logic-table evidence from July hardware

Hardware checkpoint36 restores195–200 with the fixed32T/108Q route;201–206 and
full assembly remain pending. Comparison34's4532 truth table is a counterexample
to treating either successful OCR completion or lower CER as structural accuracy.
Qwen stopped normally with only8/10 data rows and13/14 columns; Tesseract also
badly corrupted the grid. Check source row/column counts, headers and each cell,
retain the original image, and flag unclear or clipped source material. Do not
infer missing values from electrical logic. This evidence does not establish
which engine minimizes total correction cost for such tables.

The initial worker stopped during model loading after32 completed Tesseract crops.
Reuse those outputs; count both startup lifespans, exclude the recovery gap, and
record exact local token totals when no inference request was interrupted. Keep
split correction windows separate and disclose any approximate interruption
boundary. The five-row KEY routine remains literal and unexecuted; printed syntax
errors, duplicated captions and source spelling are review items, not automatic
repair targets.

### Printed listing order and diagnostic fields

July hardware37 supplies another routing comparison: clear introductory prose ties
at0% compact CER, while Qwen wins the memory-map and two code samples. Its small
206 listing still loses fields and confuses labels outside the selected sample.
Keep every printed row number, address, object field, diagnostic status and comment
in the source audit; an apparently complete OCR response or favorable sample score
does not establish complete listing fidelity.

For the assembled195–206 tutorial, preserve the physical source provenance while
ordering monitor rows1–286 across205,206,203,204. The indexed export moves STAT
numbers first; use a separately sealed native-column reference for OCR comparison
so editorial reordering does not inflate either engine's errors. Retain source
A/V/U statuses, repeated zero fields and inconsistent addresses. Do not regenerate
object bytes or append code where the original ends at a partial routine. The
complete article and incomplete original program are distinct recorded facts.

July batch38 restores the complete contest commentary207/printed203;208 is a
separate submission notice and209 starts 윷놀이. Fixed28T/8Q routing completed
without retries:36 text regions,13 review flags, no code/tables/images. Export,
source coverage, UTF-8 review ranges and byte-identical rebuild pass. Human review
is pending. Source 컬럼버스 and 규면/규민 name discrepancy remain explicit.

Visually clear Korean prose can still produce Latin fragments in Tesseract.
Comparison36 favors Qwen on all four fixed samples, but Qwen also misreads two
윷 glyphs in its prose alternate. Use the bounded representative T probe before
routing a new prose style from appearance alone; preserve/reuse the probe and
count its cost. This is raw-quality counter-evidence, not proven paid savings.
July28/36 bodies complete; next inspect 윷놀이209–214candidate. Reading room
remains scheduled after all restoration and consolidated metrics.

July batch39 restores 윷놀이209–211 as a partial checkpoint of verified209–214;
215 begins 사과도둑.65 regions,61 text crops,4 original images and29 flags cover
all prose,40 address-description rows,82 hex rows/651byte fields and one monitor
command. The complete flowchart remains an image. Source/export coverage,
listing byte ranges and byte-identical rebuild pass; human acceptance pending.

A0.235s Tesseract prose probe produced Latin fragments, informing fixed5T/56Q.
The rejected probe is retained and reused only in comparison37, without another
call. After one terminal143,16 Qwen successes and all5 Tesseract results were
reused. Interrupted request usage is unknown, so completed local tokens are a
lower bound. Four samples favorQwen, but repeated 윷 and O/0/B/8 errors plus one
extra hex field still required source review. Field counts are audit checks, not
permission to infer values or certify execution. Continue212–214, then assemble.

July batch40 completes 윷놀이212–214 and assembles full209–214. All127 hex crops
used Qwen without interruption/retry. Nine original columns contain750 visible
rows; source lacks1CC0/1F60 and clips1CB8. Preserve two unreadable byte markers,
six provisional clipped fields and16 absent source bytes. Do not infer missing
rows from the address sequence. The full article has832 hex rows plus one command,
13images78flags, with40 address-description rows. Human acceptance remains pending.

Successful model responses can omit/shift repeated fields or add ninth fields
without losing row count. Audit every visible field against the source, including
addresses and B/8/O/0; keep uncertain readings explicit. Four fixed comparison38
samples favorQwen, but substantial source review remains. Raw666.379s and correction
1062.358s overlap640.973s; they are not additive or a causal paid-cost comparison.

Full export/assembly integrity, source gaps, review/listing ranges, immutable
segments and byte-identical rebuild pass. July29/36 bodies complete, no partials;
next inspect 사과도둑215–224candidate. Consolidated metrics and reading room follow
completion of the remaining seven bodies.

### July batch41: decorative headers are a separate routing case

Apple Thief215–217 demonstrates another repeated-symbol failure: a short BASIC
comment header made Qwen repeat asterisks to4096 tokens. Preserve the failed
response and its cost. Use a bounded Tesseract fallback for that strip, and
record any reassignment of adjacent unattempted decorative strips. Keep the
original header image for exact geometry. This does not justify routing ordinary
BASIC to Tesseract: all four fixed batch41 samples favored Qwen.

After the failure, the remaining short code crops completed under512-token caps;
this is one observed successful bound for those small crops, not a general limit
for longer listings. Preserve successful native requests with their original
4096 setting when resuming; do not overwrite cached evidence or repeat completed
calls. A prior SIGTERM and the header length failure are separate terminal events.
Three worker lifespans, all failed tokens, and unknown interrupted usage are
recorded independently from assistant correction and its raw-stage overlap.

Source graphics remain images with explicit editorial placeholders. Literal
YB/YB,US,933/930 and Aplle discrepancies are preserved. Line270 ends mid-token at
this checkpoint and continues on218; complete assembly must retain that boundary.
All human acceptance remains pending. Reading-room generation waits for the full
issue restoration and consolidated metrics.

### July batch42: graphic literals can silently truncate successful code OCR

Keep the bounded-output rule, but do not equate a successful response with full
coverage. In batch42, four successful Qwen strips omitted statement text after
or near graphic literals. One other graphic strip reached512 tokens while
repeating spade symbols and used a same-crop Tesseract fallback. Its15.226s failed
compute and891 tokens remain included in the297.048s raw run and38,778-token total.

Compare every printed physical row with the draft, including graphics-only rows,
quote-only continuations and isolated source fragments. Use explicit scan-linked
markers for custom characters, retain full original columns, and leave physically
damaged text unreadable instead of borrowing from similar routines. Original
IF/ELSE anomalies and R.1 are source content, not invitations to repair code.

For evaluation, exclude editorial marker spellings from literal CER comparisons.
If sample selection changes after primary OCR because a crop contains such
markers, record the original and revised IDs and the timing of that decision.
Batch42 replaced two IDs before sealing references and running alternate OCR;
it must not be described as a wholly preselected four-sample experiment.

The standalone middle segment begins with two unnumbered physical continuations
of270 and ends inside1590. Its boundary audit pins the opening segment. Full
assembly must verify and explicitly link those boundaries while preserving all
physical rows, source pins and review ranges; independent exports alone do not
prove complete article assembly.

### Explicit wrapped listing boundaries

`wrapped-listing-v1` assembly recipes may declare `wrapped_listing_joins` with a
left segment/local logical-line ID/exact ending and a right segment/ordered
local physical-line IDs/exact opening. The join must cover every leading
unnumbered row of the immediately next segment, be byte-adjacent, and stay in
the same listing. Partial, reordered, mismatched or nonadjacent evidence fails.
Only combined indexes gain continuation links; text bytes, source ranges, scan
pins and immutable segment corrections remain unchanged. Cross-segment DATA
numeric indexes are rejected pending a dedicated literal-value review.

Keep wall-art band representation counts distinct from printed row counts.
For process recovery, poll the saved tool session: sandbox-only `ps` may hide a
live host worker. Do not start a replacement based on that limited view.
