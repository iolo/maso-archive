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
