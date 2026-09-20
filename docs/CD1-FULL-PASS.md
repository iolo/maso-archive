# CD1 first complete extraction pass — checkpoint 13d

The full pass consumes all **1,088 candidates in 72 issues** from the frozen 13a
inventory, using the pipeline validated in 13c. It records every candidate's
outcome, validates successful packages, and reconciles the entire source inventory
with prepared content and retained exceptions. This checkpoint does not require
resolving every source exception or comparing physical magazines.

## Recorded first-pass outcomes

| Outcome | Candidates |
| --- | ---: |
| Prepared | 4 |
| Prepared with review exceptions | 533 |
| Failed, with retained diagnostics | 543 |
| Blocked by source ownership | 8 |
| Total | 1,088 |

The **537 prepared articles** span all 72 issues. Every failure retains copied
stage evidence; the 551 failed/blocked candidates have explicit retry records.
The 15 articles validated in 13c carried forward entirely from compatible caches.

| Retained exception class | Candidates |
| --- | ---: |
| Unreviewed linked-content ownership | 470 |
| Font/decoding policy | 45 |
| Unsupported RTF construct | 20 |
| Unsupported inherited formatting | 6 |
| RTF document envelope | 1 |
| Unterminated paragraph | 1 |
| Source-topic ownership blocker | 8 |

The document-envelope case is the final candidate, `9312488`, whose source ends
with an unmatched closing brace. Its raw source and diagnostics remain available.
These are first-pass outcomes, not claims that the source content is unrecoverable.
The subsequent [14a review](CD1-ASSOCIATIONS.md) and
[14b retry pass](CD1-ASSOCIATION-PASS.md) address the linked-content class and
update availability while preserving this history. Ownership here means deciding
which article a linked native topic belongs to.

A complete resume verified all 1,088 records and 72 issue checkpoints and
reproduced the execution manifest byte for byte: SHA-256
`1c2cca1566ebaefd952eac7a878c148bf65e796ff60942ffd01429a15ec23907`.
Its 4,416 output records include all source-job records and 2,168 retained failure
evidence files. Original sources and the extraction pipeline remain unchanged. Two independent
complete coverage audits reproduce identical counts, issue records and all 11
coverage-table hashes.

## Coverage results

The packages contain **179,356 paragraphs and 96,399 blocks**. Independent
source reconstruction checks **30,038,307 RTF bytes and 167,611 text runs** across
915 article topics; three approved auxiliary topics are audited separately.
All **3,099 native topics, 2,103 contexts, 1,080 index references, 2,462 index
occurrences and 3,032 index rows** retain explicit dispositions.

All **5,497 TOC entries** are retained, including entries outside the observed CD1
months and section metadata. There are 66 confirmed metadata matches; **51 link
to prepared articles**, while the other 15 matched candidates remain unavailable.
**486 prepared articles have no confirmed TOC link** and remain accessible by
source identity in the private catalog. Ambiguous/title-mismatch cases are not
silently linked. Seven of nine unindexed candidates prepare; two fail. All eight
unattributed topics retain source evidence without invented article ownership.

All **6,165 referenced source media resources** pass their original manifest
checks. Prepared article packages use **2,174 available and 393 deferred** distinct
media resources; the remaining 3,598 are not packaged by this pass. Every one of
**1,479 available bitmap derivatives** matches its original decoded pixels.
Deferred vectors retain diagnostics and source links; they were not repaired.

The tracked [run summary](../data/catalog/batch-runs/cd1-full-pass.json) records
all 72 issue-package locations, counts, coverage-table hashes and verification
results. Full article text, previews, media and detailed coverage tables remain
under ignored private build directories.

**211 tests pass**, including actual-source interruption/resume, isolated decoder
failures, package/source regression, unavailable-state reconciliation, retained
failure evidence, metadata-only issue fallback and rejection of changed freshly
calculated coverage behind an otherwise valid cached report.

## Execution and recovery

```sh
make run-cd1-full-pass
make report-cd1-full-pass
```

The outer driver in `tools/batch/` does not change the extraction pipeline. Its
own implementation hash is recorded separately. The 13c gate requires an exact
pipeline identity match, so existing compatible sample stages remain reusable.
Original MVB/RTF/probe sources and the inventory are checked before work begins.
Image converters need the same environment used for sample validation.

Private execution evidence lives under
`build/cd1-batch/full-pass/<pipeline-identity>/`:

- `identity.json` records extraction identity, orchestration code and sample gate.
- `status.json` records durable job totals, completed issues and the current job.
- `jobs/<job-hash>.json` records each result, outcome, source evidence, successful
  stage references, retained failure evidence and subsequent retry arguments.
- `evidence/<job-hash>/` retains source-job metadata and copies failed-stage
  artifacts into checksum-addressable paths independent of temporary directories.
- `issues/<issue-id>.json` points to a validated issue package or records a
  composition failure. Issues without prepared bodies receive TOC-only packages.
- `manifest.json` is written after every candidate has an outcome and inventories
  all job, issue and failure-evidence files with hashes.

Interruptions leave already-recorded outcomes intact. Re-running the command
checks the original execution identity and verifies those job/package/evidence
hashes before resuming. During resume, `status.json` counters show the verification
cursor; existing job records and the completed manifest remain intact. A completed failed job remains a failed **first-pass**
outcome; the resume command does not repeatedly retry known source problems.
An interrupted in-flight job resumes through the underlying stage cache. Use only
one writer per output root. Source exceptions are retried in subsequent bounded
work with the arguments in their exception records, preserving first-pass history.

Each issue is composed from independently successful articles. The driver checks
that its article population exactly matches those successes. Metadata-only issue
packages retain unmatched TOC rows and make no claim of extracted bodies.
All output stays private; this command publishes nothing.

## Outcome meanings

| Outcome | Meaning |
| --- | --- |
| `prepared` | Source recovery and runtime package succeeded, with reviewed semantic decisions and no recorded deferred media/auxiliary rendering exception. Physical comparison still remains pending. |
| `prepared_with_review_exceptions` | A validated package exists, but generic semantic interpretation, media or auxiliary rendering needs review. |
| `blocked` | The input queue already identified a source ownership constraint. |
| `failed` | This pass attempted the candidate and retained a specific failure plus its source/stage evidence. No extracted-article claim is made. |

The last two outcomes are unavailable content in the catalog. They are never
counted as prepared because an intermediate text file happens to exist. Print
verification is a separate pending field for all preparations.

## Coverage and verification

The reporting command validates the entire execution manifest, every completed
job, all successful article packages and every issue package. It independently
reconstructs decoded text runs from RTF byte spans, checks complete topic byte
accounting and verifies available bitmap pixels against their source images.
Runtime article identities and TOC links must agree with the inventory.

The report produces private checksum-verified JSONL catalogs for:

- Every native topic, role, alias, source span and preparation/retention state.
- Every native context, index reference, index occurrence and other index row.
- Every current TOC entry, match evidence, available article link and unavailable
  matched candidate; unmatched metadata is retained.
- Every candidate, including unindexed identities, with explicit availability.
- Referenced source media, source integrity/absence, attempted conversion,
  runtime disposition and retained diagnostics.
- Per-issue packages and outcomes, successful source/run audits, the eight
  unattributed-topic records, and the failed/blocked retry queue.

`REPORT_ARGS=--write-record` records a reviewed summary in
`data/catalog/batch-runs/cd1-full-pass.json`. Normal reporting must reproduce that
record. The coverage directory itself is staged and hash-checked. Its manifest
and the execution manifest preserve reproducible first-pass evidence without
putting publisher text or images into Git.

The [sample report](CD1-BATCH-VALIDATION.md) and all earlier preparation records
remain historical checkpoints. Missing scans, physical comparison, image repair,
independent backup/restore, access/publication, CD2/CD3 and reading-room UI remain
separate work.

The subsequent [14a association checkpoint](CD1-ASSOCIATIONS.md) preserves the
111 linked auxiliaries and prepares six additional articles in separate sample
packages. Its results do not overwrite this first-pass history. The subsequent
[14b pass](CD1-ASSOCIATION-PASS.md) records all 464 remaining retries and combines
successful packages, bringing current availability to 944 articles across 72 issues.
