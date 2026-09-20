# CD1 ASCII font retry pass and current handoff — checkpoint 15b

This checkpoint processes the **27 remaining candidates** approved by 15a's
source-bound ASCII policy and carries forward its **six successful samples**.
All 33 eligible candidates receive durable subsequent outcomes. The other 53
font/decoding cases remain deferred. All 27 new attempts prepare successfully;
with six carried samples, current packages contain **977 articles across 72 issues**.
The consolidated source/package/media audit and complete resume pass, as do
all 236 regression tests. A second complete audit reproduces all 13 coverage
tables and the tracked summary exactly.

| Current candidate outcome | Count |
| --- | ---: |
| Prepared | 4 |
| Prepared with review exceptions | 973 |
| Failed, with retained evidence | 103 |
| Blocked on source-topic ownership | 8 |
| Total | 1,088 |

The remaining failures comprise 53 font/decoding cases, 35 unsupported RTF
constructs, 13 inherited-formatting cases, one unterminated paragraph and one
RTF document-envelope case. No new article failure was exposed by this pass.

## Preserved history and current issue packages

The 14b handoff is the baseline: 944 prepared articles across 72 issue packages,
136 failures and eight blockers. All historical 13d/14a/14b/15a reports and
packages remain intact. No decoder, font-policy or runtime-schema changes are
introduced by 15b.

For each issue, the composer verifies the prior package and adds only successful
font retries. It rejects duplicate article identities, wrong-issue content,
conflicting shared media and conflicting asset bytes. Article JSON, Markdown
previews and available media retain their exact bytes. Issue/catalog/media
indexes and manifests reflect the complete current article population.

Failed attempts retain source jobs, stage evidence and diagnostics. A failure does
not prevent unrelated articles from preparing. Failed issue composition remains
explicit and prevents the coverage audit from completing. Complete source text
remains private regardless of later publication decisions.

## Commands and recovery

```sh
make run-cd1-font-pass
make report-cd1-font-pass
```

Use the same converter/font environment as the validated 15a sample. The driver
binds that sample, the font audit, the historical 14b report, the unchanged font
runner and its own orchestration code. Resume verifies saved source identities,
checkpoints and packages; it carries the same six sample outcomes and retains
recorded failures without repeatedly attempting them.

Private artifacts live under `build/cd1-font-pass/`:

- `runs/<identity>/identity.json` binds the inputs and implementations.
- `outcomes/` points to the six existing 15a checkpoints or 27 new 15b checkpoints.
- `jobs/` and `evidence/` retain new outcomes and source/failure evidence.
- `issues/` records each of the 72 combined issue packages or a composition error.
- `status.json` shows progress; on resume its counters represent the verification
  cursor, while earlier durable outcomes remain present.
- `manifest.json` inventories every completed outcome and evidence file.
- `current-issues/issue-<issue-id>/<fingerprint>/content/` contains the current
  static handoff. Serve each `content/` directory beneath its chosen base URL;
  internal paths remain relative. Adjacent provenance stays separate.

Use one writer per output root. Run the coverage audit after execution or resume
has finished. A job persisted immediately before an interruption is recovered
even if its outcome pointer was not yet written.

## Coverage and fidelity checks

The audit verifies every new outcome, all 72 historical and all 72 current issue
packages, and every successful font retry's standalone package. It compares
current article JSON, previews and available media with the verified 14b payloads
and new standalone payloads byte for byte. It checks the exact article and media
populations, including unchanged issues.

Every successful retry must match the 15a source audit with only the approved
unsupported-to-ASCII substitutions. Existing text, formatting, source spans,
accounting and article boundaries remain exact. Auxiliary text/dispositions
retain the separate 14a policy. New source runs are independently checked against
RTF bytes; the 944 historical source audits and historical intermediate-stage
audits carry forward under their verified hashes and unchanged pipeline identity.
All referenced source media are checked again, including pixel comparisons for
available bitmap derivatives. Deferred images are retained for later repair.

Thirteen private coverage tables reconcile topics, contexts, index references and
occurrences, TOC entries, candidates, issues, media, source checks and remaining
exceptions. Font retry history is separate from the preserved 470-entry association
retry history. Failure/source paths retain their original evidence roots. Newly
exposed failures name the font-aware runner for later bounded follow-up; old
base-runner commands remain historical evidence.

The tracked [current coverage summary](../data/catalog/batch-runs/cd1-font-pass.json) locates all
current packages and private tables by checksum. `REPORT_ARGS=--write-record`
establishes the reviewed summary; a normal report run independently recalculates
the tables and requires exact equality with both cached table bytes and the
tracked record.

Current articles contain **380,996 paragraphs and 213,319 blocks**, with
**64,394,136 source RTF bytes and 353,753 text runs** accounted for. The 33 font
successes add 21,712 paragraphs beyond the historical 14b handoff.

All 6,165 referenced media resources are accounted for: **4,526 available, 811
deferred and 828 not packaged**. All **3,330 available bitmap derivatives** match
source dimensions and decoded RGBA pixels. No deferred-media repair is performed.

Coverage includes all 3,099 native topics, 2,103 contexts, 1,080 index references,
2,462 occurrences, 3,032 index rows and 5,497 TOC rows. **64 TOC entries** now link
to available content; **913 prepared articles lack reviewed TOC links** and remain
available through their native CD identities and issue catalogs.

Complete resume reproduces the 159-file execution manifest with SHA-256
`04375a76b766e4c3ebb76f1b04210d493788a78d9a12c7a2bb1074f033e64273`.
All **236 regression tests pass**, including six new checks for retry scope,
immutable history, combined article/media preservation and every current issue
package. Existing decoding, preservation, failure-isolation, resume and static
loading checks also pass.

TOC matching, the 53 deferred font cases, other RTF/ownership failures, semantic
and physical review, scans, image repair, backup/restore, CD2/CD3, reading-room UI
and access/publication decisions remain separate scopes. Successful extraction
does not establish complete printed-magazine coverage.
