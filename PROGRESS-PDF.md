# PDF restoration progress

Updated 2026-10-20. This file is the status index; detailed records live under
[`docs/progress/`](docs/progress/README.md), grouped by **magazine issue**, not
by the calendar month in which restoration work happened.

## Current status

December 1984 is in progress: eleven readable articles, one partial perspective
simulation article, two non-owning headings and 23 of 37 entries unresolved.
Perspective spans 19 observed pages 131–149, PDF133–151. Three immutable natives
cover131–148: packages/perspective-a, packages/perspective-b-r01 and
packages/perspective-c. They retain103 regions,67 blocks and27 original images.
Final GBASIC149, the explicit opening134 repair and full assembly remain.

The new listing143–148 native and independent rebuild reproduce all56 files
exactly. Its17 regions retain three blocks,seven original listing frames andten
regional text spans. Two right edges were widened once before OCR;all17 original
andtwo revised exact crops were inspected. Ten tasks succeeded with no failure,
retry or post-OCR crop repair. All22 whole/review pairs were reused and inspected;
six mapped pages and16 outside-map lookups. One source-direct correction pass.

The listing indexes retain406 physical rows,404 nonblank units and378 observed
numbered entries:100 AppleSoft1700–2760 and278 GBASIC1000–3770. AppleSoft inserted
2265, printed gaps andtwo blank rows remain. Target233/newline0 andall other
physical wraps are indexed without executable flattening. The source versions
remain independent:four AppleSoft DATA records retain40 fields;two GBASIC setup
records retainnine fields. Printed POKE1913,2 andsource glyph/spacing candidates
are not repaired from expected syntax,firmware orcross-version agreement.

Exact source indexes retain1,591 tokens,1,378 identifiers,897 numeric fragments,
1,537 punctuation candidates,74 comment glyphs,two uncertain decorative dash runs,
165 quote/comment glyphs,45 paired strings,55 reference clauses,65 target fields
and2,276 inline occurrences. Five GBASIC frames share observedlocal10.4 heading.
Two current AppleSoft frames have no locally printed caption;prior10.3 heading
is pinned with exact external source bytes for association atcompleteassembly.
The ledger carries this pending association andboth source-code connections.

Earlier middle137–142 retains87 matrix cells,two printed ellipsis rows,43 flowchart
labels,24 printed references,15 variable definitions,64 DATA fields and27 output
values. All math,diagram,flow,prosejoin,physical/logical listing andcaption metadata
must survive assembly. The CP/M adapter is not a generic perspective adapter.

Opening134 reflection paragraph has a closing parenthesis beyond the old crop
edge. The old native andits incorrect missing-parenthesis statement remain as
superseded evidence. A separate bounded crop/OCR/correction/index revision is
required before full assembly;see restoration/batch-25/opening-defect-followup.json
andthe ledger's required_native_revisions. No silent overwrite ofold evidence.

All28,907 prior files and23 implementation pins remain unchanged. The new
preservation inventory has29,209 files. The unchanged193-test baseline frombatch24
is reused without rerunning tests;no shared tooling changes orreader rebuild.
CP/M remains complete at packages/cpm5-complete-r01,observed110–129 plusunpaginated
upper PDF132 reference continuation;lower132 ad separate,no observed130. BASIC
speed102–109 retains opening102–107 andending108–109. All selected checks use
cpm_literal_assembly.check/installed(),which delegates graphic_literal_assembly.

Next:batch27,final GBASIC149/PDF151 through4290 END. Recheck full19-page extent
andneighbors PDF132/152:21 views,20 outside the one mapped page;do notadd153.
Then perform the separate opening134 source revision andcompatible full assembly,
resolving known10.3 caption association andpreserving every native field/array and
original frame. Human acceptance,full proofreading,source bytes,execution and
mathematics remain unverified. No reader rebuild.

See the [December record](docs/progress/8412.md) and
[ledger](metadata/catalog/pdf-restoration/1984-12-progress.json). No reader rebuild.

October 1984 is complete under the canonical TOC JSON/assets scope: 35 readable,
assistant sample-reviewed articles and six non-owning headings account for all 41
entries, with no partial articles or unresolved eligibility. All 260 PDF pages are
classified: 205 contain selected article bodies and 55 are other material, including
18 pages of two unlisted features. The verified cover, selected packages and
independent byte-identical issue rebuild pass; all 30,737 prior evidence files remain
unchanged. The standalone index is `archive/pdf/1984-10/reference/issue.json`;
the report is `archive/pdf/1984-10/evidence/issue-closeout/report.json`.
Human acceptance/full proofreading, source bytes and execution remain unverified;
news/classified body transcription and the batch 35 preflight timing exception remain
explicit. The restoration closeout itself did not rebuild the reader.
Ten supplied eligible issues remain after October, including December now in progress.

October's volunteer reader was subsequently built at the owner's request. The
current `dist/reading-room/` contains 329 PDF articles across nine issues plus
3,386 CD records (3,715 total). Data preservation, tests, production compilation
and browser checks pass; the October release is saved. This was a local build,
with no deployment. See [the reader guide](docs/READING-ROOM.md).

September is also complete:37 readable articles/six headings, with its
[issue index](archive/pdf/1984-09/reference/issue.json) and
[report](archive/pdf/1984-09/evidence/14-1984-09-closeout/report.json) preserved.
See the [October record](docs/progress/8410.md), [OCR handoff](PLAN-OCR.md),
[PDF plan](PLAN-PDF.md) and [successor notes](docs/SUCCESSOR-NOTES.md).

| Issue | Body articles | Availability | Detailed progress |
| --- | ---: | --- | --- |
| 1983-11 | 35 | 35 readable | [8311](docs/progress/8311.md) |
| 1984-02 | 37 | 37 readable | [8402](docs/progress/8402.md) |
| 1984-03 | 38 | 37 readable, one terminal missing-source partial | [8403](docs/progress/8403.md) |
| 1984-05 | 36 | 36 readable | [8405](docs/progress/8405.md) |
| 1984-06 | 38 | 38 readable | [8406](docs/progress/8406.md) |
| 1984-07 | 36 | 36 readable | [8407](docs/progress/8407.md) |
| 1984-08 | 37 | 37 readable | [8408](docs/progress/8408.md) |
| 1984-09 | 37 | 37 readable; canonical TOC complete | [8409](docs/progress/8409.md) |
| 1984-10 | 35 | 35 readable; canonical TOC complete | [8410](docs/progress/8410.md) |
| 1984-12 | 10 | 10 readable; 0 partial; 2 non-owning headings; 25 TOC entries unresolved | [8412](docs/progress/8412.md) |

No April 1984 PDF was supplied. Completed accounting and usable coverage are
separate: March's absent printed pages 250–251 remain explicit.

## Cross-issue records

- [Foundations and contrasting pilots](docs/progress/foundation.md)
- [Catalog, scope, tooling and cost decisions](docs/progress/campaign.md)
- [OCR experiment progress](docs/progress/ocr-experiments.md)
- [Full experiment-history index](docs/history/README.md)

The reorganization preserves all **489 original sections**, their order within
each destination, evidence paths and measurements. Heading levels and relative
Markdown links were adjusted for the hierarchy. [Migration provenance and
section lookup](docs/progress/migration.json) map every old section to its new
location and record original/content hashes. No restoration output was changed.

## Updating progress

Append bounded checkpoint notes to `docs/progress/YYMM.md` for the issue being
restored. For a new issue, add a current-outcome summary and a checkpoint-records
section, then add it to the [directory index](docs/progress/README.md). Update
this status table and next step at issue milestones; do not append detailed
batch histories here. Keep measurements and package pins in their existing
machine-readable ledgers, and link them from the issue page.

Record cross-issue decisions in the appropriate shared file. Preserve historical
claims as dated observations; earlier “next” instructions are not a current queue.
A future cleanup must preserve the source records and update affected links.
