# CD1 font-declaration retry pass — checkpoint 17b

This checkpoint processes `9306300` under the exact-source policy reviewed in
[17a](CD1-FONT-DECLARATION-REVIEW.md), carries its five sample successes forward,
and reconciles combined CD1 availability against the immutable 16b handoffs.
Execution completes with all **72 issue packages prepared** and six successful
retries (five carried samples and one new attempt). The 80-file execution manifest
has SHA-256 `16cd2b493c2ce49488280c56b29fae7b9b9fe2709710b9f72aea0340d3e66003`.
Complete resume reproduces that manifest byte for byte. The source, package,
media and coverage audit passes with **988 prepared articles across 72 issues**.
A second complete audit reproduces all **15 coverage tables and the tracked
summary exactly**. **262 regression tests pass without skips**, including six new
scope, sample-gate, ambiguous-deferral, history and combined-package checks. The 16b report
remains the historical 982-article checkpoint.

## Current coverage

Of 1,088 candidates, **988 prepare** (four prepared and 984 prepared with review
exceptions), **92 fail**, and **eight remain blocked**. All six retries succeed;
no new failure occurs.

| Remaining exception category | Candidates |
| --- | ---: |
| Font/decoding policy | 42 |
| Unsupported RTF construct | 35 |
| Unsupported inherited formatting | 13 |
| Unterminated paragraph | 1 |
| RTF document envelope | 1 |
| Source-topic ownership blockers | 8 |

The 42 font/decoding cases comprise the ambiguous article retained by 17a, four
Symbol-font cases and 37 failures under existing codecs. The next bounded review
will examine the four Symbol-font cases; their ASCII-range byte values alone do
not establish glyph identities.

Current packages preserve **390,366 paragraphs, 219,994 blocks, 65,353,264 RTF
bytes and 362,186 text runs**. The six successes add 2,640 paragraphs beyond 16b;
`9306300` contributes 481 paragraphs. All 6,165 source media are accounted for:
**4,617 available, 882 deferred and 666 not packaged**. All **3,419 available
bitmap resources** preserve source pixels. Newly encountered deferred resources
remain recorded; no existing available media is lost.

All 3,099 native topics, 2,103 contexts, 1,080 index references, 2,462 index
occurrences, 3,032 index rows and 5,497 TOC entries reconcile. **64 TOC entries**
link to content; **924 prepared articles lack reviewed TOC links** and remain
available under native identities. These counts describe observed CD1 content;
printed-issue completeness and physical accuracy still require separate review.

## Scope and preservation

The pass accepts exactly six reviewed article/topic associations and their
explicit ASCII or CP949 mappings. Five distinct successful samples must match
both the pipeline and review record; only `9306300` may be newly attempted.
Any later-stage failure retains its evidence and does not count as prepared.

`9309201` remains outside the approved policy and retry population. Its ambiguous
source bytes and complete original recovery remain in the 17a evidence. The
current exception table carries that decision and a hash-bound reference to the
review record. Four Symbol-font cases and 37 failures under existing codecs also
remain outside this pass.

Each issue package combines the verified 16b package with successful standalone
retries. The audit validates every historical and current package, checks exact
preservation of article JSON, Markdown previews and available media, and verifies
article/media populations. All six successful recoveries must equal the original
15a recovery with only the substitutions reviewed in 17a. New text runs and topic
accounting are independently reconstructed from the original RTF. Auxiliary
content retains the reviewed 14a decisions.

The 982 historical source audits carry forward under checked hashes and the
unchanged pipeline. They are preserved evidence, rather than newly decoded
articles. Original media bytes and all available bitmap pixels are checked.
Broken conversions remain deferred with their diagnostics.

The report retains 15 private coverage tables, including four separate retry
histories: `retry_history` for the six declaration candidates,
`ordinary_font_retry_history` for the five 16a/16b candidates,
`font_retry_history` for the 33 ASCII candidates, and `association_retry_history`
for the 470 association candidates. Other exception instructions and annotations
survive; the ambiguous article receives its newer, explicit review decision.

## Commands and handoff

```sh
make run-cd1-font-declaration-pass
make report-cd1-font-declaration-pass
```

Use `REPORT_ARGS=--write-record` to establish the coverage record. Normal reporting
recomputes coverage, checks every generated table against cached bytes and requires
exact equality with the tracked summary. Execution resume verifies source jobs,
stage evidence and packages before reusing outcomes. The converter/font environment
is unchanged from 17a.

Execution records, source evidence and combined packages remain beneath
`build/cd1-font-declaration-pass/`. The manifest binds six outcome pointers, the
new job/evidence and 72 issue checkpoints. The five sample artifacts retain their
original 17a locations. Each combined package's `content/` directory is the static
reading-room handoff. Runtime paths remain relative to the chosen base URL;
extraction evidence stays outside runtime content.

The [tracked coverage summary](../data/catalog/batch-runs/cd1-font-declaration-pass.json)
records current package paths, dependencies, the execution manifest and hashes of
all 15 private coverage tables.

Full text, previews, media and detailed evidence remain private. TOC matching,
physical comparison, semantic review, scans, image repair, backup/restore,
CD2/CD3, UI and publication/access remain separate work.
