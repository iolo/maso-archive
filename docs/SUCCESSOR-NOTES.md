# Successor handoff — 2026-10-20

Storage: [what to preserve and where new work belongs](STORAGE.md). Historical paths remain available through compatibility links.

## Read first

1. [OCR handoff](../PLAN-OCR.md): accepted engine policy, essential findings,
   source/review rules, metrics and commands. Do not read all trial logs to resume.
2. [PDF plan](../PLAN-PDF.md): JSON/assets scope and remaining campaign gates.
   August, September and October are complete. October's 35 articles and 260-page
   ledger are recorded in [the October log](progress/8410.md). December 1984
   is now in progress; completed checkpoints and the next bounded task are in
   [the December log](progress/8412.md). Restoration alone does not authorize a
   reading-room rebuild.
3. [October closeout](../archive/pdf/1984-10/evidence/issue-closeout/report.json)
   and its source-page ledger at
   `archive/pdf/1984-10/restoration/issue-closeout/source-page-ledger.json`.
   The portable index is `archive/pdf/1984-10/reference/issue.json`; reproduce it
   using `archive/pdf/1984-10/restoration/issue-closeout/reproduction.json`.
   For an existing August assembly check, use its pinned adapters from
   `archive/pdf/1984-08/restoration/13-1984-08-closeout/reproduction.json`.

**Current OCR policy:** mapped Tesseract by default. Qwen is an opt-in draft or
second reading for difficult prose or code, with explicit layout/coverage review.
Do not restart completed comparisons or run both engines routinely. Historical
Qwen-first/adaptive assignments are superseded; measurements remain useful.

## Restoration state and boundaries

October accounts for all 41 TOC entries: 35 readable, assistant sample-reviewed
articles and six non-owning headings. All 260 PDF pages are classified and the
independent full issue rebuild is byte-identical. All 30,737 earlier evidence files
remain unchanged. Unlisted DOS TOOL KIT 41–43 and 통합 소프트웨어 241–255 are outside
canonical restoration scope. Human acceptance/full proofreading, source bytes and
execution remain unverified. News/classified body transcription is pending; many
program/numeric panels remain original images. Keep the batch 35 preflight timing
exception explicit: model confirmation of three revised crops followed OCR batch
launch, with per-region timing uninstrumented. Later source/crop/rebuild checks pass.

Completed JSON/assets issues are November 1983 and February, March, May, June,
July, August, September and October 1984. March retains its absent-source terminal
partial; no April PDF was supplied. Ten supplied eligible issues remain after
October.

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

Perspective evidence:restoration/batch-24/25/26 andevidence/batch-24/25/26.
Current native is packages/perspective-c,56 files;selected recipe is
restoration/batch-26/perspective-c/package-recipe.json. Its read-only verifier is
evidence/batch-26/verify.py;only a fresh explicit --report writes a report.
All ten regional readings,original/revisedmaps/crops/rawOCR andprior failures
remain preserved. No source orOCR restart is needed forassembly.

Keep all148 opening files and154 middle files immutable. The opening134 repair
must use fresh geometry/OCR/source/index paths andexplicitly supersede the clipped
reading;do notmutate packages/perspective-a. Batch25 runtime-path export failures
remain preserved;its selected middle recipe is package-recipe-r01.json.
AppleSoft ending143–144 connects prior1690 to1700 andends2760;GBASIC begins1000
onshared144 andcurrent148 ends3770. Final149 begins3780 andends4290 END.
The source caption10.3 frommiddle141 must associate withtwo current AppleSoft
originals atassembly,using pinned external bytes/scan provenance. Currentlocal10.4
heading already associates allfive GBASIC frames. Preserve source_code_connections,
caption_associations_pending andall numeric/symbol/comment/target/DATA indexes.

Crowded Speedway remains packages/crowded-speedway-complete-r01,including final
69F8/eight00source revision. Its pinned table/literal tooling39e5b61 remains
unchanged;the new graphic dispatcher supports that format forwhole selected audits.

Spin Ball remains packages/spin-ball-complete-r02. Literal-source tooling
c27c183and its [format notes](PDF-LITERAL-SOURCE-FIELDS.md) remain preserved.
Keep its five-field final7BE0revision,earlier four-field observation and7B28typing
repair explicit.

Diamond Field remains at packages/diamond-field-complete-r01 with its original
metadata revision. BASIC field tooling eba1e08 is documented in
[the format notes](PDF-BASIC-SOURCE-FIELDS.md). Use its evidence/diamond-field-assembly/
verify-r02.py historical audit; retain earlier failed attempts. NeighborPDF66 is
an unpaginated publisher ad; native58–64shorthand is not an observed folio64 or a
global-offset claim. Reader integration is separate; the owner subsequently
requested the October reader build.

Private PDFs, raw OCR, model files and completed exports are not in Git. Preserve
source hashes, canonical IDs/parents, original evidence and user edits. Verify a
process is live before waiting/resuming; reuse successful stages. Close out an
issue before starting another. Earlier checkpoint “next” statements are historical.

## Reader integration — 2026-10-19

At the owner's explicit request, `dist/reading-room/` now includes October's 35
articles: nine PDF issues (329 records) plus 3,386 CD records, 3,715 total. The
original October closeout/packages remain unchanged. See [the reading-room guide](READING-ROOM.md)
for reproduction and the verified `reading-room-2026-10-19-october` snapshot.
All 5,218 files from the 35 packages and 124,113 inherited reader files are preserved;
nine Python tests, 25 frontend tests, production build and browser checks pass. Q&A
correspondents remain beside their questions after a focused display correction.
This is a local build; no deployment occurred.

### Previous September integration — 2026-10-16

At the owner's explicit request, `dist/reading-room/` now includes September's
37 restored articles: eight PDF issues (294 records) plus 3,386 CD records,
3,680 total. The original September package and closeout remain preserved.
See the [reading-room guide](READING-ROOM.md) for the two recorded canonical-title
mappings, repeatable export inputs and named release recovery. This local build
was not deployed and does not authorize the next issue's reader integration.

## Where to look when needed

| Need | Reference |
| --- | --- |
| Engine accuracy, cost and limits | [OCR handoff evidence index](../PLAN-OCR.md#metrics-and-accounting) |
| Mapped-Qwen and optional A/B/C commands | [Workflow reference](OCR-WORKFLOW.md) |
| Article/assembly/batch/issue tooling | [PDF commands](PDF-RESTORATION.md#current-data-only-commands) |
| A specific old checkpoint or failure | [PDF issue logs](progress/README.md), [experiment history](history/README.md) |
| CD reader inputs, routes and private preview | [Reading-room guide](READING-ROOM.md), [README](../README.md) |

The [previous successor snapshot](history/SUCCESSOR-NOTES-2026-10-14.md) retains
all detailed earlier restoration notes. The disc constraints below remain useful;
old test counts and inventory sizes are historical observations, not new gates.

## Known decoder defect

Read [the HELPDECO underline bug record](CD3-HELPDECO-UNDERLINE-BUG.md) before
changing CD3 formatting. The pinned decoder mistakes a font character-set byte
for `DoubleUnderline`: Hangul `0x81` becomes RTF `\uldb`, even with the actual
underline flag off. The owner confirms normal, non-underlined rendering in the
Windows viewer. The record contains the font-stream hash, descriptor offsets,
counts, code references and reproduction command.

The implemented mitigation is **display-only** in `tools/cd3_display.py`, shared
by the CD3 HTML exporter and reading-room adapter. The decoder is unpatched,
no upstream issue was filed, and stored RTF/source flags retain its error.
Suppression also hides genuine underline; it does not alter literal text,
source evidence, bold/italic, code spacing or attachment bytes. Correcting the
font decoder and migrating the pinned probe is explicitly deferred.

## Owner priorities and retained exceptions

Paper magazines are authoritative. CD and library TOC data are separate
transcriptions. Preserve readable text, literal code, useful structure, images,
source provenance and visible uncertainty. Keep paper-supported corrections
separate. Do not guess uncertain characters or printed-issue associations.

CD1 has 1,080 texts across 72 body-bearing issues, including 33 with localized
gaps, plus eight unresolved article-boundary candidates. It retains 1,111
unviewable distinct images with original links. The historical 995 strict
packages/19b outcomes remain unchanged; the readable reference adds useful
text from all 85 earlier failures.

CD2 accounts for 1,330 candidates (220 success, 1,110 partial), and CD3 for 968
(792 success, 176 partial). Partial outcomes retain useful bodies with local
exceptions. CD3's anomalous date labels, missing images/CAB and unresolved figure
aliases remain explicit. Neither extraction completeness nor normal Windows
rendering establishes agreement with paper magazines.

The goal is useful reading and paper restoration with a clear stopping point.
Do not restart speculative recovery or cosmetic-formatting campaigns to clear
every exception. Existing viewer observations can diagnose concrete extraction
bugs; routine Windows setup or screenshot collection is not a prerequisite.

## Rebuild and verification

`make export-reading-room` validates the prepared references, builds static
version 2 data in a staging tree and replaces the existing data only after the
aggregate checker passes. CD1/demo version 1 documents and CD1 URLs remain
supported. See the guide for required private inputs; a Git checkout alone
cannot reproduce publisher content. `make demo-reading-room` supports UI work
without those inputs.

`make test-reading-room` runs the focused Python adapter tests, six Vitest
tests, TypeScript checks and a production build. `make check-reading-room`
verifies the prepared inventory, hashes, article memberships, literal text,
listings, attachments, media, search coverage and source manifests. The current
aggregate inventories 44,672 reference data files, about 3.43 GB before its root
manifest, plus optional covers (eight supplied samples bring it to 44,680).
Add covers as `covers/masoYYMM.jpg/png/webp`, then re-export/build; see
[the cover guide](READING-ROOM.md#add-or-replace-cover-images).
Use per-disc checks from the reference guides when changing those exporters;
avoid rerunning the whole historical suite for documentation-only changes.

Browser validation covered representative articles from each disc, linked CD3
figures and supplements, downloads, missing originals, undated navigation,
search, refresh and a 360px dark-mode layout. The underline follow-up checked
all current CD3 article/supplement pages and three rendered reader articles.
See PROGRESS for concrete cases and preserved-file checks.

## Future work, when requested

- Correct HELPDECO's font mapping, validate it against raw records and the viewer,
  version the new decoder/probe, regenerate dependent evidence and remove the
  blanket display workaround. Do not relabel the existing probe as corrected.
- Resolve a specific text, image, boundary or association problem when it helps
  actual paper/OCR comparison. Gary Kildall's interview (`8802030`) remains a
  useful starting example.
- Collect missing scans/covers and verified later TOCs. The library TOC currently
  ends at 1993-12; CD2/CD3 navigation does not manufacture later TOCs.
- Make and verify an independent backup of all disc sources, probes and private
  outputs. Earlier CD1 transfer archives are historical snapshots and do not
  include the completed CD2/CD3/SPA work. No independent backup is recorded.
- The owner reports that the volunteer reading-room deployment works; its
  access and future updates are separate from PDF restoration.

Keep source media and generated publisher content out of Git. Log substantive
work in PROGRESS and commit scoped changes; preserve unrelated owner edits.
