# CD1 Symbol integration — checkpoint 18c

This checkpoint carries the invariant-punctuation article `9210202` from
[18a](CD1-SYMBOL-REVIEW.md) and the reversible-arrow article `9208198` from
[18b](CD1-SYMBOL-ARROWS.md) into combined CD1 issue handoffs. It performs no new
article extraction. Both sample checkpoints retain their distinct decoding
identities, original locations and complete source evidence.

Execution prepares **all 72 issue handoffs**. Seventy copy the verified 17b
runtime content byte for byte; August and October 1992 merge their respective
sample article. Complete resume reproduces the **74-file execution manifest**
exactly, with SHA-256
`6699c36150411a3c43b05b5be59885a4560e216210a53e7903d364a48e97b8ca`.
The independent source, package, media and coverage audit passes with **990
prepared articles across 72 issues**. A second complete audit reproduces all
**16 coverage tables and the tracked summary exactly**. **282 regression tests
pass without skips**, including six new integration checks and the historical
source/package/schema/Markdown/base-URL tests. The 17b report remains the
historical 988-article checkpoint.

## Current coverage

All **1,088 candidates** reconcile: **990 prepared** (four prepared and 986 with
review exceptions), **90 failed** and **eight blocked**. The two validated samples
are the only availability changes. No new extraction attempt or failure occurs.

| Remaining exception category | Candidates |
| --- | ---: |
| Font/decoding policy | 40 |
| Unsupported RTF construct | 35 |
| Unsupported inherited formatting | 13 |
| Unterminated paragraph | 1 |
| RTF document envelope | 1 |
| Source-topic ownership blockers | 8 |

The 40 font/decoding cases comprise two Symbol font/context conflicts, the
ambiguous `9309201` case and 37 failures under existing codecs. The next bounded
checkpoint, 19a, will review the retained byte evidence for those 37 cases and
select a small validation sample only where reversible recovery is supported.

Current packages preserve **392,486 paragraphs, 220,953 blocks, 65,625,509 RTF
bytes and 363,912 text runs**. The two samples add 2,120 paragraphs, 959 blocks,
272,245 RTF bytes and 1,726 text runs. All **6,165 source media** reconcile:
**4,630 available, 891 deferred and 644 not packaged**. All **3,432 available
bitmap resources** have source-equivalent pixels. Media counts are deduplicated
across articles; shared resources are counted once.

All **3,099 native topics, 2,103 contexts, 1,080 index references, 2,462 index
occurrences, 3,032 index rows and 5,497 TOC entries** reconcile. The 64 available
TOC entries remain unchanged; **926 prepared articles lack reviewed TOC links**
and retain native CD identities. These figures describe the observed CD content,
not complete printed-issue coverage or physical verification.

## Scope and preservation

Only the two reviewed font failures are eligible for integration. Each sample
must match its own pipeline, the pinned 18a review, exact source job, successful
checkpoint and complete runtime inventory. The arrow sample must also match its
glyph-policy hash. Any altered byte, missing/extra runtime file, changed topic
association or unreviewed candidate prevents reuse.

Both recoveries are compared with their complete original recoveries, allowing
only the substitutions approved in 18a/18b. The ordinary byte checker validates
the punctuation article; the source-bound arrow checker validates the arrow
article. Every new topic must reproduce its sample's independent source checks.
Arrow counts, literal spaces, original bytes and formatting remain preserved.
Linked auxiliaries retain their separate text and earlier dispositions.

The coverage audit independently loads and validates all 72 prior and all 72
current packages. It compares every article payload, Markdown preview and
available media file, rejects missing/extra articles or media, and checks all
source media plus available bitmap pixels. The 988 earlier source audits carry
forward under their checked historical records. They are preserved evidence,
not newly extracted articles.

The two Symbol conflicts, `9205400a` and `9205403`, retain their original failed
outcomes and gain explicit references to the 18a font/context decisions. The
ambiguous `9309201` decision and all other unresolved exceptions remain intact.
Existing code text is not repaired. Deferred images remain deferred.

The 16 private coverage tables retain five separate retry histories: this checkpoint's two Symbol
samples, six declaration candidates, five ordinary-font candidates, 33 ASCII
candidates and 470 association candidates. Historical records and packages are
never overwritten. The frozen decoder, shared policies and schema are unchanged.

## Commands and handoff

```sh
make run-cd1-symbol-pass
make report-cd1-symbol-pass
```

Use `REPORT_ARGS=--write-record` to establish the coverage record. Normal
reporting recomputes the audit and requires exact equality with every cached
coverage table and the tracked summary. Execution resume rechecks both samples
and verifies issue checkpoint bytes before reuse.

The [coverage summary](../data/catalog/batch-runs/cd1-symbol-pass.json) records
current package paths, source populations, exceptions, sample dependencies and
private coverage-table hashes. Execution records and combined packages live
beneath `build/cd1-symbol-pass/`. Each package's `content/` directory is the static
reading-room handoff, with paths relative to the chosen base URL. Detailed source
evidence stays outside runtime content.

Full text, media and detailed evidence remain private. Physical comparison, TOC
matching, semantic review, scans, image repair, backup/restore, CD2/CD3, UI and
publication/access remain separate work.
