# PDF progress directory

[Current status and next issue](../../PROGRESS-PDF.md) · [OCR handoff](../../PLAN-OCR.md)

Files use the magazine's `YYMM` issue code. Dates within each file identify when
restoration work occurred. Read the current outcome first; use old checkpoint
notes for targeted investigation, not as instructions to restart completed work.

| Issue | Records |
| --- | --- |
| November 1983 | [8311.md](8311.md) |
| February 1984 | [8402.md](8402.md) |
| March 1984 | [8403.md](8403.md) — absent-source partial remains explicit |
| May 1984 | [8405.md](8405.md) |
| June 1984 | [8406.md](8406.md) — early records plus links to later OCR history |
| July 1984 | [8407.md](8407.md) — completed ledger and existing detailed history |
| August 1984 | [8408.md](8408.md) |
| September 1984 | [8409.md](8409.md) — canonical TOC complete |
| October 1984 | [8410.md](8410.md) — canonical TOC complete |
| December 1984 | [8412.md](8412.md) — canonical TOC complete |
| February 1985 | [8502.md](8502.md) — canonical TOC complete |
| March 1985 | [8503.md](8503.md) — canonical TOC complete |
| October 1985 | [8510.md](8510.md) — canonical TOC complete |
| November 1985 | [8511.md](8511.md) — restoration pass complete; one unresolved entry |
| January 1988 | [8801.md](8801.md) — restoration pass complete; 36 readable articles, 14 non-owning headings and one unresolved survey entry; 8,360 JSON/assets files independently exact, 213 fresh tests |
| August 1991 | [9108.md](9108.md) — restoration pass complete; 28 readable articles, five non-owning headings, two section references; all383 pages accounted, 9,272 JSON/assets files independently exact, 213 fresh tests |

| September 1991 | [9109.md](9109.md) — active; twenty-three readable articles, no partial articles, four non-owning headings and two section references; actual assemblies/child anchors complete; source accounting344/406 records,62 outside pages pending, next twenty outside pages190–249; survey/application and B+ tree SAMPLE.C gaps, cover/export and closeout remain |

| Shared scope | Records |
| --- | --- |
| Inventory, covers, pilots, contracts and batch qualification | [foundation.md](foundation.md) |
| Catalog reconciliation, scope/tooling decisions and cost accounting | [campaign.md](campaign.md) |
| OCR benchmark/workflow setup | [ocr-experiments.md](ocr-experiments.md) |

Earlier January 1988/August 1991 samples are in foundations; their later whole-issue
closeouts are recorded separately above. Raw scans, OCR, correction files and generated packages
remain in their existing private locations.

## Maintenance

For new work, add brief dated checkpoints to the appropriate issue file and
maintain its current-outcome summary. Keep the root progress file as an index.
Use public/private machine-readable ledgers for complete metrics and pins;
avoid copying full ledgers into narrative logs. Current OCR policy, review
standards and JSON/assets scope remain in the linked handoff and PDF plan.
Artifact paths in backticks are repository-relative even in moved records.

[Migration map](migration.json) records the original Git revision/hash and every
moved section's source range, destination anchor, content hash and link rewrites.
The old log can be reconstructed exactly from that revision; the migrated record
bodies preserve all content except recorded heading-level/link adjustments.
Byte offsets describe the initial migration; use destination anchors for lookup
after updating summaries or appending new checkpoints. Keep migrated record
bodies and anchors intact; a later reorganization must update their locations.
Links to OCR JSON evidence were rebased when those files moved to
[`docs/ocr-experiments`](../ocr-experiments/README.md); the migration map records
the earlier snapshot.
