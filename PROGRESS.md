# Progress

## 2026-09-18 — Source inspection and scope

- Read the shared project discussion and inspected `TOC.md` and all three ISOs.
- Confirmed 86 monthly TOC headings from 1983-11 through 1990-12 and 3,811 nested
  entries. Calculated ISO SHA-256 hashes and inspected disc directory listings.
- Recorded findings in `docs/SOURCE-INVENTORY.md`. The owner will arrange
  1983–1987 scans later; those 50 issues initially have TOC metadata only.
- Validation: no missing or duplicate issue headings in the working TOC.
- Limitation: inventory does not establish complete original-page coverage.

## 2026-09-18 — Implementation plan

- Created `PLAN.md` covering preservation, TOC import, CD extraction, data
  contracts, reconciliation, review, publication boundaries, and searchable UI.
- Planned CD1 enrichment for the 36 target issues from 1988–1990, with later
  scans handled through the same provenance and review workflow.
- Validation: checked local document links and confirmed scope against the TOC.
- Status: planning complete; catalog import and site implementation not started.

## 2026-09-18 — CD1 extraction feasibility

- The owner ran CD1 in DOSBox-X and supplied the extracted `masocd-1/` directory.
  Verified that setup installs the viewer/runtime and links to content on CD.
- Built HELPDECO at revision `b9c187a20d83a3e738d8fe073eb924a8b7264c5c`.
  The default build failed on legacy pointer assignments; a documented compiler
  compatibility flag allowed the probe build. An absolute input path printed
  usage; using a relative input path produced the extraction.
- Recovered 7,372 files, including a 74,157,536-byte RTF, image resources, and
  three Korean indexes. Preserved outputs, logs, and a checksummed manifest in
  `private/cd1-probe/`. Added Git exclusions for source media and private files.
- Confirmed the CD's declared coverage as 1988-01 through 1993-12. The indexes
  contain 1,038 distinct numeric references, including 360 for 1988–1990.
- Validation: readable Korean article samples; strict CP949 decoding of the
  indexes; successful decoding of one DIB and one BMP; output counts and local
  document links checked. Runtime log scan found no reported decoder errors.
- Limitations: mixed character/font handling requires an RTF parser; article
  matching, complete image validation, and viewer comparison remain pending.
  Compiler warnings remain. Reference/topic counts are not final article counts.
- Details: `docs/CD1-EXTRACTION.md`. This completes the feasibility experiment,
  not the entire extraction/reconciliation milestone.

## 2026-09-18 — Progress and commit workflow

- Added the standing rule to log each step here and commit its changes with the
  progress entry. Interpreted the request's “base url” as “base rule”; no website
  base URL was supplied or configured.
- Included the owner's existing README description and three TOC issue-heading
  corrections in the initial planning/probe commit, along with the new documents
  and storage exclusions.
- Validation: whitespace checks, document links, TOC date continuity, and staged
  file review; confirmed that extracted content and VM files are ignored.
- Next: implement the TOC importer and a small RTF normalization/topic-mapping
  pilot, then reconcile recovered CD1 articles with the TOC.

## 2026-09-18 — TOC importer and persistent identities

- Implemented `python3 -m maso_archive import-toc`, exposed through
  `make import-toc`, with JSON Schema validation and documented dependencies.
- Preserved every TOC bullet, hierarchy, original order, raw source line, and
  source checksum. Parsed title/byline/page candidates conservatively, retaining
  multiple page references and flagging incomplete or ambiguous fields.
- Added a versioned identity map in `data/identities/toc.json`. Insertions and
  moves preserve existing IDs; corrections, ambiguous duplicates, and removals
  use explicit decisions bound to the source checksum. Retired IDs are not
  reused, and rejected imports leave successful outputs and identities intact.
- Generated issue records, all TOC entries, article candidates, a validation and
  coverage report, local search metadata, and a checksummed run manifest under
  the ignored `build/toc/` directory. No source bodies or public-site assets are
  included. Recorded usage and correction procedures in `docs/TOC-IMPORT.md`.
- Result: 86 issues, 3,811 preserved entries, and 2,975 article candidates,
  including 199 possible feature bundles. The 2,068 review notices include nine
  empty bylines and 12 multiple-page references; notices are not import failures.
- Validation: all 15 tests passed with `make check`, including the real TOC,
  nested/synthetic edge cases, failure preservation, identity changes, and schema
  rejection. A second complete real-TOC import left all output and identity-map
  hashes unchanged. Documentation links and whitespace checks passed.
- Limitations: records remain unreviewed; article candidates include editorial
  matter and bundles. No end-page inference, normalized author identities,
  summaries, or CD article matching has been performed. Full durable disc
  inventories and backup verification are still outstanding in Milestone 1.
- Next: finish durable disc inventory manifests, then normalize and reconcile a
  small CD1 RTF/topic sample against the imported TOC records.

## 2026-09-18 — Plan revised into smaller tasks

- Replaced the broad milestone queue in `PLAN.md` with one bounded step per
  task, an explicit deliverable/completion check, and the existing log-and-commit
  rule. Preserved the earlier detail in `docs/DESIGN-REFERENCE.md`; the new plan
  takes precedence over its historical ordering and earlier “Next” entries here.
- Set the first milestone to one CD1 article linked to the TOC and verified
  against the original viewer, using sources already available. Missing scans
  are not a prerequisite. Separated index import, one metadata match, topic
  location, paragraph decoding, article text, images, and viewer comparison.
- Defined the immediate next task as importing the three extracted CD1 indexes
  with provenance and validation. Deferred RTF parsing and bulk matching from
  that task; no new extraction/import implementation was started in this revision.
- Retained completed work, the full 86-issue objective, the later-scan agreement,
  preservation/backup follow-up, and private/public data boundaries. Later issue,
  website, and expansion checkpoints will be decomposed when their inputs are known.
- Validation: checked local Markdown links and whitespace, matched completion
  statuses against prior progress, and confirmed the provisional sample's title
  and page occur in `TOC.md`. Documentation-only change; no code tests required.
- Next: **step 1 — CD1 reference-index importer**. Finish, validate, log, and
  commit that step before taking on the next numbered task.

## 2026-09-18 — Offline work checklist

- Added `docs/OFFLINE-TASKS.md` for the owner's parallel work: open the provisional
  CD1 article, record its boundaries and illustrations, and try copying a short
  text sample for comparison. Specified a private evidence folder and note format.
- Listed optional preservation of the working Windows environment, independent
  ISO backup verification, and information gathering for later scans. Missing
  future scans do not block the pilot; immediate index import needs no viewer
  evidence, while the eventual verification step does.
- Validation: checked local document links and confirmed that the proposed
  reference-evidence path is ignored by Git. No code changes or tests required.
- Next development task remains **step 1 — CD1 reference-index importer**.

## 2026-09-18 — Step 1 complete: CD1 reference-index importer

- Added `make import-cd1-index` and the corresponding CLI command. The importer
  verifies each of the three `.lst` files against the extraction manifest and
  decodes CP949 strictly. It reads no RTF, image, or article-body files.
- Preserved all 3,032 source lines with raw labels/targets, category paths,
  parent relationships, line numbers, byte spans, and input hashes. Retained
  category markers and terminators as records. Grouped references link to every
  original occurrence rather than losing repeated categories or title variants.
- Generated local entries, reference groups, validation report, and a checksummed
  run manifest in `build/cd1-index/`. Added JSON Schema validation and documented
  use and failure behavior in `docs/CD1-INDEX.md`.
- Result: 567 categories, 2,462 reference occurrences, and three terminators.
  The 1,080 distinct targets comprise 1,038 seven-digit references, 41 references
  with letter suffixes, and the `mscdmenu` navigation target. The historical
  baseline of 360 seven-digit references in 1988–1990 matches exactly.
- Review notices: nine padded category markers and three occurrences of
  `9311000`, whose page-like component is `000`. All were retained; no page zero
  or final article count was inferred. No input lines remain unparsed.
- Validation: eight new focused tests and the existing 15 tests all passed with
  `make check`. Tests cover the actual private sources plus synthetic malformed
  syntax, duplicate references, encoding/manifest rejection, byte provenance,
  deterministic output, and CLI operation with only indexes and their manifest.
  Reimporting the real files produced identical hashes for all four outputs;
  manifest hashes, documentation links, and whitespace checks passed.
- Limitations: reference dates are candidates based on native identifier syntax.
  No TOC matches, RTF topic mapping, body conversion, or viewer verification was
  performed. The first-article milestone remains incomplete.
- Next: **step 2 — one explicit CD-to-TOC metadata match**, starting with native
  reference `8802065`. Stop after that bounded task and its validation/log/commit.

## 2026-09-18 — Step 2 complete: one CD-to-TOC metadata match

- Recorded `8802065` → `maso-1988-02-toc-0035` in
  `data/catalog/source-matches/cd1-8802065.json`. The decision is supported by
  metadata only; existing TOC IDs, source labels, and import review states are
  unchanged. No collection-wide matching or RTF/body processing was performed.
- Preserved both CD occurrences: `column.lst` line 3 and `panecmds.lst` line 112,
  with their original labels, category paths, source hashes, and byte locations.
  The TOC evidence is the `88.02` heading at line 2451 and feature at line 2487.
- Exactly one entry in that issue matches after removing the explicitly recorded
  `특집 : ` prefix and final question mark. Both CD labels explicitly name 88.02.
  The TOC reports page 65; the CD target suffix `065` is consistent with it, but
  its reference-to-page interpretation remains unverified.
- The TOC has a single leaf feature entry with no byline or ending page. Whether
  the CD feature spans multiple topics or fully represents the print article is
  unresolved. Both CD occurrences come from the same disc, not independent sources.
- Added `tools/verify_cd1_match.py` to check this one record against actual input
  bytes, generated-output hashes, persistent identity, occurrence completeness,
  title/issue agreement, and the limits on page/content claims. Documented the
  decision and recheck command in `docs/CD1-MATCH-8802065.md`.
- Validation: the recorded match passed. Five deliberately invalid in-memory
  revisions were rejected: omitted occurrence, incorrect TOC identity, incorrect
  page, unsupported body-verification claim, and stale source hash. Documentation
  links and whitespace checks passed. Importer code and source files were unchanged.
- Next: **step 3 — map reference `8802065` to its raw topic/context records and
  byte locations**, before attempting paragraph decoding. The first-article
  milestone remains incomplete pending content recovery and viewer comparison.
