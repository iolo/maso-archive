# PDF restoration progress

Updated 2026-10-20. This file is the status index; detailed records live under
[`docs/progress/`](docs/progress/README.md), grouped by **magazine issue**, not
by the calendar month in which restoration work happened.

## Current status

December 1984 is in progress: sixteen readable articles, one partial article,
five non-owning headings and 15 of 37 entries unresolved. Design(6), canonical 0020,
now has two immutable natives: packages/design-a for observed 178–183/PDF180–185 and
packages/design-b for observed 184–189/PDF186–191. The new 138-file native matches
its independent rebuild exactly. Combined coverage is 12 pages, 81 regions, 55 blocks
and 26 original images. The complete article assembly remains pending.

The independent opening 178/PDF180 and final Z80 listing END 204/PDF206 establish
physical span 180–206; cryptography opens 205/PDF207. Prose closes 188 with a publisher
mark, but patch tables and listings continue 189–204. All current mapped folios 184–189
and outgoing 190/PDF192 were inspected. Fifteen physical pages 192–206 remain deferred.
PDF193–201 remain unreviewed, unclassified and folio-unknown; None means uninspected,
not unpaginated. Known deferred folios are 190 on 192 and 200–204 on 202–206. No global
folio offset or unchecked interior classification was inferred.

This checkpoint inspected 12 whole views 179/180/185–192/206/207 before mapping:
six mapped pages, six outside-map lookups, one canonical task. Six full/review pairs
were reused and six newly rendered. All 42 original and 14 revised exact crops were
viewed before 29 successful mapped tasks, including five code crops. OEM1/PSM6,
one thread, 3000-pixel long edge, eng for code and kor+eng for prose remain pinned.
Each affected crop was widened once. One source correction pass; zero recognition
failures, retries or post-OCR repairs. Figure 8's printed (b) heading is retained as
separate prose from the widened code region. All stages and failed attempts retained.

Design-b retains 42 regions, 27 blocks, 13 originals, 34 regional ranges and 43 review
notes. Two tables preserve 58 rows/157 cells/eight header fields/one blank. The work-area
table has 17 rows/34 cells/16 definitions. The patch table retains 39 data rows, 117 opaque
address/OLD/NEW fields and five printed category headings. Unequal field lengths and
DB/D3/B/E/0/O values remain source candidates; no patch bytes or opcodes decoded.

Four listing groups retain 138 physical rows, 115 nonblank rows and four actual BASIC
labels 10,20,30,40. Patch addresses are not BASIC numbers. Twenty printed EQU definitions,
136 assembly columns, 384 tokens, 341 identifier occurrences and one unclosed quote are
indexed. Three unknown decorative bands remain explicit editorial markers; their English
labels are excluded from source tokens while printed semicolons are retained. The final
Tiny BASIC comment continues onto deferred 190; no quote completion or executable join.

Six prose joins, 15 expression/result claims, six explanation steps and four elevated
parenthesis marks preserve literal source occurrences. Diagrams retain 103 label rows/
173 fields. Six printed captions link 11 frames: figure 6 has four frames, figure 8 two,
figure 9 two. The Tiny listing and publisher mark have no invented captions. All 13
original images remain authoritative. FACTR/FACT, FSTVP/FSTPV/FTOV, 3FFH/listing 3FFFH,
Q equal/minus and circled/Greek/quartered-square glyphs remain uncertain candidates.
No syntax, hardware, byte, address, encoding, arithmetic or graphic reconstruction.

All 33,215 prior files and 26 implementation pins remain unchanged; the new preservation
inventory contains 33,834 files. The unchanged 203-test baseline is reused without
rerun. A fresh serializer fixes marker words leaking into two source tokens, reusing
all readings/blocks. Its first revision had an unmatched-parenthesis SyntaxError;
that attempt is retained. A verifier assumption that captions always followed bodies
was fixed for Table 1's caption above the table; the native was already correct.
Source/crop/settings/range/physical-row/patch-field/rebuild and preservation checks pass.

Contest0022 and technical0019 remain separate non-owning headings on unpaginated PDF179.
Their canonical children0023/24/25 and 0020/21 retain references213/214/219 and 178/205.
Canonical identities, titles and parents are unchanged.

VisiCalc 172–175 remains complete at visicalc-limits:154 files, five menus/52 options/
129 fields, three ROUND claims and one manual source word ⟦faint source word⟧ pending.
Body/page coverage is complete; CALCULATE/CALCULATION and 351.6763/results351.68/352/350
remain independent. Memory 166–171 at memory-efficiency retains 182 files/190 cells/
15 blanks/99 byte fields/46 physical rows/45 entries, source 위해서/canonical 위하여,
Rea Only Memory, 76 BE:6 and output 149/prose 191. Mathematics 152–154 remains at
math-montecarlo-r01:104 files/output 3.136. Business unpaginated PDF167 retains
source 비지니스/canonical 비즈니스. MSX 150–151 at msx-loader retains 147 physical rows/
134 entries and 박재현/TOC박제현. Perspective 131–149 at perspective-complete-r01 retains
all 384 natives, 134 repair, two captions, 143–148 listings and 87 middle matrix cells;
keep perspective-a, perspective-b-r01, perspective-c, perspective-d. CP/M remains at
cpm5-complete-r01,110–129 plus unpaginated upper PDF132; lower 132 ad excluded, no 130.
BASIC speed102–109 retains opening 102–107/ending 108–109. Selected checks use
perspective_literal_assembly.check/installed(), delegating cpm_literal_assembly and
graphic_literal_assembly. Preserve all 26 implementation pins.

Next: batch35, design assembly continuation on physical PDF192–197. Only 192 has an
already inspected 190 folio; verify every new page/folio before mapping. Reuse preceding 191,
opening 180/divider179/ending 206/next 207 and inspect outgoing 198. Preserve the physical
189/190 comment boundary, all source fields/indexes/shared captions/unknown bands and
native metadata. Fifteen physical pages and full assembly remain. Human acceptance,
full proofreading, source bytes, execution and historical claims remain unverified.
No reader rebuild.

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
