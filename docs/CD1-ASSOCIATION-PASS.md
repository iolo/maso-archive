# Complete association retry and current CD1 coverage — checkpoint 14b

Step 14b applies the validated separate-auxiliary policy to all **464 remaining
association candidates** and carries forward the **six successful 14a samples**.
All 470 first-pass association failures receive subsequent outcomes. New decoding,
formatting or structural failures retain their evidence and remain unavailable.

Execution is complete: 401 of the 464 new attempts prepare, and 63 retain failures.
Including the six carried sample articles, the retry class contributes 407
preparations, bringing current packages to 944 articles across 72 issues.
Complete resume reproduces the exact execution manifest, and the consolidated
source/package/media audit passes.

| Current candidate outcome | Count |
| --- | ---: |
| Prepared | 4 |
| Prepared with review exceptions | 940 |
| Failed, with retained diagnostics | 136 |
| Blocked on source-topic ownership | 8 |
| Total | 1,088 |

The 136 failures comprise 86 font/decoding cases, 35 unsupported RTF constructs,
13 inherited-formatting cases, one unterminated paragraph and one document-envelope
case. No association failure remains. These counts describe available CD content;
they do not establish complete printed-issue coverage.

## Preserved history and current packages

The original 13d record remains a historical first pass: 537 prepared articles,
543 failures and eight blockers. Of those failures, 470 belong to this retry
class; the other 73 failures and eight blockers retain their earlier outcomes.
The six 14a sample records and separate auxiliary recovery remain intact.

For each issue, current packages combine validated first-pass successes with
validated retry successes. The composer checks article/job uniqueness, source
identity, shared media records, asset bytes and every standalone package. Article
JSON remains identical to the standalone content. Failed articles cannot enter a
current issue merely because some intermediate text was recovered.

Each new combined issue package contains its complete current article population,
TOC/catalog availability, relative media references, Markdown previews and a
manifest. Original issue handoffs remain at their historical paths. No content is
published; all bodies, derivatives and detailed retry evidence remain private.

## Execution and resume

```sh
make run-cd1-association-pass
make report-cd1-association-pass
```

Use the same converter/font environment as 14a. The extraction pipeline and
auxiliary policy remain unchanged. The 14b orchestrator and report fingerprint
their own implementations separately. No per-article preparation scripts or
runtime schema changes are introduced.

Private artifacts live under `build/cd1-association-pass/`:

- `runs/<identity>/identity.json` binds the 13d, 14a sample and auxiliary-review
  records, validated pipeline identity and orchestration code.
- `outcomes/<job-hash>.json` within that run points to either an existing 14a
  checkpoint or a new 14b checkpoint, retaining each evidence root explicitly.
- `jobs/` and `evidence/` retain new results, source-job bindings, successful stage
  references, copied failure artifacts and bounded-retry arguments.
- `status.json` reports the recorded retry count and completed issue checkpoints.
  During resume its counters show the verification cursor; completed outcomes
  remain intact and known failures are not automatically retried.
- `issues/` records current issue package locations or an explicit composition
  failure. One failed article does not prevent unrelated successful articles
  from composing; unresolved composition failures prevent audit completion.
- `manifest.json` inventories every run outcome and its evidence after all 470
  candidates have subsequent outcomes.
- `current-issues/issue-<issue-id>/<fingerprint>/content/` contains the combined
  packages. Serve each `content/` directory beneath its chosen static base URL;
  package-internal paths remain relative, as in the existing reading-room contract.

Use one writer per output root. Resume verifies completed job/source/stage/package
hashes, carries forward the same six sample checkpoints, and checks composed issue
content. A durable job written immediately before interruption is recovered even
if its outcome pointer had not yet been written.

## Coverage and validation

The reporting command requires the completed execution manifest. It verifies all
470 subsequent outcomes and association boundaries, every current standalone and
combined issue package, successful retry source runs, auxiliary dispositions and
available bitmap pixels. The original 537 source audits carry forward from the
hash-verified 13d report under the unchanged source/pipeline identity.

Private coverage tables account for every native topic, context, index occurrence,
TOC row, candidate, referenced media resource and unattributed topic. Current
availability is explicit, while a separate retry-history table retains before/after
outcomes. Source/failure paths include their original evidence roots. Newly exposed
failures join the consolidated exception queue; they are never counted as extracted.
For newly exposed failures, the queue names the auxiliary-aware runner and the
need for a bounded source-policy change. The original base-runner retry command
is retained only as historical evidence, since it would repeat the old association
constraint. A later attempt must use a new private output root.

The tracked [current coverage summary](../data/catalog/batch-runs/cd1-association-pass.json) locates
all 72 current issue packages and the private tables by checksum. Establish a new
reviewed summary with `REPORT_ARGS=--write-record`; normal reporting independently
recalculates the tables and checks exact equality with both cached bytes and the
tracked record.

The 12 private coverage tables account for all 3,099 native topics, 2,103 contexts,
1,080 index references, 2,462 occurrences, 3,032 index rows, 5,497 TOC rows and 6,165
referenced media resources. Current articles contain 359,284 paragraphs and 202,527
blocks, with 61,491,911 RTF bytes and 330,177 text runs accounted for. Available
media total 4,312 resources; 771 remain deferred and 1,082 are not packaged.
All 3,171 available bitmap derivatives preserve source dimensions and RGBA pixels.

Only 62 TOC entries currently link to available content; 882 prepared articles
have no reviewed TOC link. This is a metadata-matching limitation: the articles
remain accessible by their native identities in the issue packages and catalog.

Complete resume reproduces the 1,652-file execution manifest with SHA-256
`6b8778e606b08503023e672c5b33d3d9c97bbb27250db4aba95a5a7d01c427b4`.
A second complete audit reproduces all 12 coverage tables and the tracked summary
exactly, including every issue package location, count and checksum.

All **223 regression tests pass**, including six new merge/reconciliation/artifact
checks. Targeted tests cover duplicate/wrong/unavailable articles, conflicting shared
media and asset paths, forbidden replacement of unrelated historical outcomes, provenance
path qualification and all completed issue packages. Existing decoder, preservation,
resume and static-loading regressions also pass.

Remaining failure classes and TOC matching are subsequent bounded work. Physical
comparison, missing scans, deferred image repair, backup/restore, CD2/CD3, access
and publication decisions, and reading-room UI remain separate scopes.
