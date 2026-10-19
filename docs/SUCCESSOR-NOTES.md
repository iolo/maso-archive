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

December 1984 is in progress: ten readable articles, one partial CP/M(5)
article, two non-owning headings and 24 of 37 entries unresolved. CP/M natives now
cover 110–121/PDF112–123. Its full source remains PDF112–132: observed 110–129 plus
an unpaginated upper reference-table continuation. The lower advertisement on
PDF132 is separate; no folio 130 was observed.

The new 116–121 native and independent rebuild reproduce all 255 files exactly.
It retains 78 regions, 53 blocks, 22 original images, 273 unnumbered physical rows,
270 nonblank transcript units and 1,448 tokens. All 113 ED line-label occurrences,
41 editor commands, five quoted source candidates and 36 quote/prime glyphs retain
exact source ranges. ED labels are preserved with duplicates and descending values.
Fifty-one dump rows retain 726 literal fields and 48 printed ASCII columns without
byte decoding, address arithmetic or opcode repair. Eighteen code markers and five
unknown prose $-run widths remain explicit. Source mistakes and glyph candidates
are unverified; no historical execution or encoded-byte claim.

All 56 regional text spans, 106 text reviews, 50 notes, 292 inline examples, 22 figure-
caption links, 21 listing-caption links and two prose joins pass independent checks.
Figure 34 preserves both original frames in one 31-row transcript; its caption owns
both images. Figure 16's caption on 116 retains the incoming 115 frame association
for full assembly. Source prose joins retain118left/right있/는 and119/120모드/로.

All 24 pinned whole-page views and 78 original/seven revised crops were inspected
before 56 successful mapped tasks. Six mapped pages and 18 outside-map lookups;
no new rendering, recognition failure/retry or post-OCR crop repair. The geometry
script produced the map and seven crops, then failed its final metadata pin lookup
on an old segment path. Its script, failure and fresh metadata record remain;
no second geometry repair or OCR retry. All 22,490 prior files and 20 implementation
pins are unchanged. New preservation inventory: 23,510 files. The unchanged 187-test
PDF baseline is reused; no shared tooling or reader work.

Both CP/M natives retain 178 regions, 134 blocks, 46 images and 489 physical rows.
Later 122–129, unpaginated PDF132 and complete assembly remain. Preserve every
transcript, editor-label/command, quote, hex/address/ASCII, marker, table, review and
caption index in a compatible future projection. BASIC speed 102–109 remains
complete from opening 102–107 and ending 108–109. All selected-package checks must
use `tools.pdf_restore.graphic_literal_assembly.check` or its `installed()` context,
which also handles Crowded Speedway.

Next: batch22, CP/M middle122–127/PDF124–129. Reinspect pinned source and neighbor
scans and every exact original/revised crop before OCR. Human acceptance, full
proofreading, source encoded bytes and execution remain unverified. No reader work.

CP/M natives: packages/batch-20-r01/cpm5-a and packages/batch-21-r01/cpm5-b.
Reproduction/schema/source evidence: restoration/batch-20 and restoration/batch-21.
Middle read-only audit: evidence/batch-21/verify.py. Its 255 files reproduce exactly;
all 23,510 preservation inventory files pass. Keep the seven-crop metadata pin
failure and fresh record. Earlier batch20 index-classifier and inventory open-log
exceptions remain preserved. All 20 historical implementation files stay pinned.
Full assembly must preserve every new editor/quote/ASCII/source-candidate index.

BASIC speed remains packages/basic-speed-complete-r01 with immutable batch18/19
originals and basic-speed-index-r01/{opening,ending} revisions. Its selected audit
is evidence/basic-speed-assembly/verify-r03.py; earlier failures remain preserved.

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
