# PDF restoration progress

Updated 2026-10-20. This file is the status index; detailed records live under
[`docs/progress/`](docs/progress/README.md), grouped by **magazine issue**, not
by the calendar month in which restoration work happened.

## Current status

December 1984 is in progress: twelve readable articles, no partial articles,
two non-owning headings and 23 of 37 entries unresolved. Perspective simulation
is complete over19 observed pages131–149/PDF133–151 at
packages/perspective-complete-r01. Its393-file export and independent rebuild
match exactly. All384 native files are retained byte-identically:372 base files
from perspective-a,perspective-b-r01,perspective-c,perspective-d plus12 files from
the explicit perspective-reflection-revision. Human acceptance remains pending.

The full article retains105 regions,68 blocks,28 original frames,77 regional OCR
drafts,86 regional text spans and129 source review notes. All five original
correction metadata objects remain exact in native_metadata. The page134 repair
replaces its active region,block,crop,OCR andoccurrence indexes once atoriginal
reading order;one observed closing parenthesis is restored. Oldcroppedtext andthe
incorrect absence claim remain only as superseded archival evidence. No duplicate
page,section ormatrix counts. No new mapping,rendering,OCR orsource correction.

All source indexes survive:37 display/context ranges,28 matrices,104 observed
rows,351 literal cells,two printed ellipsis rows,16 fractions,466 math glyphs,
four equation labels,152 diagram/DATA labels,43 flow labels,24 flow references,
15 variable definitions,nine output rows and27 values. Source errors such as
reflection's two negative entries,identity translation,X₂ X₂ and219/2000 remain.
No mathematics,arithmetic,semantic orgraphic reconstruction. Earlier middle87
matrix cells andlisting143–148 source evidence remain immutable.

Code retains701 physical rows,696 nonblank units,601 numbered entries and2,958
tokens. AppleSoft andGBASIC stay independent. There are113 DATA fields in10
records,2,225 identifiers,1,002 numeric fragments,1,743 punctuation candidates,
86 comment glyphs,259 quote/comment glyphs,86 paired strings,68 reference clauses,
66 target fields and5,115 inline occurrences. All physical wraps,source gaps,
inserted2265/4045/4105,absent4140,POKE1913,2 and3840 NEX remain. No executable
flattening,firmware correction orcross-version repair. FinalGBASIC4290 END retained.

Known10.3 AppleSoft caption associates its143–144 continuation frames,and10.4
GBASIC caption associates149,from exact prior native bytes andscan provenance.
Both pending associations are resolved:19 caption/frame links,20 caption parts,
four listing-caption links andnine truly uncaptioned originals. One explicit
prose136→137 boundary retains source blocks andimage anchors;two listing links
connect1690→1700 and3770→3780 without changing physical bytes. Flow138→139 retains
observed B/A labels,with original geometry only. No caption orrevision remains pending.

The new opt-in implementation was committed separately as ef36c69 before export.
All203 PDF tests pass. The detailed audit verifies17,659 projected native rows and
19,901 nested UTF8 ranges. All29,444 prior files and23 prior implementation pins
are unchanged;three new perspective implementation pins bring the total to26.
New preservation inventory:30,256 files. All selected checks must now use
perspective_literal_assembly.check/installed(),which delegates cpm_literal_assembly
andgraphic_literal_assembly for older formats. The CP/M adapter isnot generic for
perspective math/source-revision indexes. No reader orfrontend work.

CP/M remains complete at packages/cpm5-complete-r01,observed110–129 plusunpaginated
upper PDF132 reference continuation;lower132 ad separate,no observed130. BASIC
speed102–109 retains opening102–107 andending108–109. Earlier native failures and
all superseded evidence remain preserved. Source bytes,full proofreading,execution
andmathematical correctness remain unverified.

Next:batch29,canonical MSX machine-code loader0014,TOC start150/byline박제현.
Provisional pages150–151/PDF152–153 must be verified against whole source pages
andneighbors before mapping;the next TOC article starts152. No globalfolio offset.
Recheck every exact original/revised crop before OCR. Keep literal physical code,
comments,quoted strings,hex/target fields andoriginal frames. Remain within two
articles,six mapped pages and20 outside-map lookups. No reader rebuild.

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
