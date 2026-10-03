# Successor notes — 2026-09-26 implementation wrap-up

**Current PDF continuation, 2026-10-03:** follow [PLAN-PDF.md](../PLAN-PDF.md)
and [PROGRESS-PDF.md](../PROGRESS-PDF.md) for the owner-authorized Tesseract plus
scan-based semantic review campaign. November1983 and February1984 are complete.
Data-only export/assembly/issue validation is implemented; no browser or reader
delivery is required. March batches01–09 and two article assemblies are complete.
Editorial13 and full feature14–37 are readable/sample-reviewed. The assembled
feature is `build/pdf-restoration/12-1984-03-feature`:24 pages,149 regions,
77 blocks,22 image panels and2,033 physical listing rows; all five original
packages remain unchanged under segments. Rebuild and85 PDF tests pass.
The full 추리력 테스트 게임40–46 is assembled at
`build/pdf-restoration/12-1984-03-reasoning`: 24 regions, 17 blocks, two images,
535 physical rows and 42 unresolved PET graphics markers. Both native segments
(batch06/reasoning/revised-final and batch07/reasoning) remain unchanged.
Batch07/hourglass restores complete 모래시계47–50: 18 regions, 13 blocks,
one image and 376 rows across five implementations. Batch08 completes paddle
construction51–53 (29 regions,18 blocks,eight numbered diagrams) and apple-counting
54–55 (11 regions,nine blocks,one photograph,80 BASIC rows). Both packages rebuild
identically; all text/listing/figure indexes and three prose joins pass.
Batch09/golf completes canonical 올 인원 (printed 홀 인 원)56–60:18 regions,
12 blocks,two images and360 physical BASIC rows (113 numbered,247 continuations).
Native review recipe is under `batch-09/golf/revised-final`; originals and two
once-repaired crops remain preserved. Code860 crosses59/60;1040 crosses columns.
Source table1770,PRINT CS,AP and uncertain650 period/1150 F/P remain literal.
Rebuild is byte-identical and85 earlier packages pass read-only preservation checks.
Page39 is a non-owning 취미생활 group heading. March has seven readable articles,
one group heading and36 unclassified entries; issue closeout remains pending.
Next follow `private/pdf-restoration/12-1984-03-batch-09/next-checkpoint.json`:
batch10 starts 팽이 놀이 at61, then candidate 사냥게임 at64 within two articles/
six source pages after verifying extents. Source61–62 already visually inspected.
Preserve PET line99/98 uncertainty, duplicate590, graphics markers and uncertain
small punctuation marks; do not repair historical code. The namespaced assembler
validates the legacy prose boundary and regional listing ranges without rewriting originals; see the assembly recipe
and validation evidence. Preserve all literal leading zeros, wraps, dump rows,
uncertainties and source/correction records. No new OCR engine/configuration.
The active owner goal is to complete all remaining March1984 content.
Earlier CD handoff details below are historical; they do not cancel this work.
No reviewer-model comparison has been performed. If the owner changes models,
record the selection and check a bounded prose/code/figure batch before making
claims about equivalent review quality or savings.

CD1, CD2, CD3 reference extraction and the combined reading room are complete.
The owner requested a documentation handoff and retention of the HELPDECO bug
record. No decoder migration, new recovery pass or public deployment is in
progress. Future work should follow a concrete owner request.

## Start here

- Main deliverable: `build/reading-room/`, served over HTTP. Run `cd web && npm run preview`
  and open the printed address. Read the [build/use guide](READING-ROOM.md).
- The combined catalog contains 3,386 candidates, 3,378 readable texts, 3,212
  UTF-8 listings, 5,497 library TOC entries and 9,990 group/media records.
  It exposes 122 library issues, 12 CD2 date groups and 18 CD3 native groups.
  Native date groups are not independently verified printed issues.
- The separate [CD1](CD1-READABLE-REFERENCE.md), [CD2](CD2-READABLE-REFERENCE.md)
  and [CD3](CD3-READABLE-REFERENCE.md) references remain under `build/`.
  CD2/CD3 reference shelves preserve supplemental texts and unassigned media;
  their 1,837 original attachment links are included in the reader.
- All four plans are implemented: [CD1](../PLAN-CD1.md), [CD2](../PLAN-CD2.md),
  [CD3](../PLAN-CD3.md), [reading room](../PLAN-reading-room.md).
  Original scope sections and [PROGRESS](../PROGRESS.md) retain checkpoint
  history; older statements about future UI/disc work are not current tasks.
- The original [reading-room PRD](../PRD-reading-room.md) predates the owner's
  explicit all-disc aggregation request. `PRD-local-web.md` is absent from this
  checkout. Do not infer requirements from the old handoff's mention of that file.

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
- Decide publication/access policy separately. No content has been deployed.

Keep source media and generated publisher content out of Git. Log substantive
work in PROGRESS and commit scoped changes; preserve unrelated owner edits.
