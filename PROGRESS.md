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

## 2026-09-18 — Step 3 complete: pilot raw topic/context map

- Resolved native reference `8802065` through hash `0x0e688271` in the MVB
  `|CONTEXT` table to topic ordinal 149, represented by generated RTF alias
  `2PES_R6`. The native topic title is “유닉스란 무엇인가?”. This relationship
  is supported by context records, not just matching title text.
- Recorded the separate linked introduction (ordinal 148, `3M4UMD`) and body
  as the provisional recovery scope. Preserved native logical addresses, physical
  MVB header/context locations, exact raw RTF byte spans, and input/slice hashes
  in `data/catalog/topic-maps/cd1-8802065.json`. No article body is committed.
- Identified a nine-byte untitled RTF separator (native ordinal 150), followed
  by the introduction and body of “스펠링 체커” (151–152). The pilot's native
  browse-forward pointer reaches that neighboring body; it is not evidence of
  feature continuation. All three following topics are explicitly excluded.
- Located the explicit CD body label `88.2.  65p` at RTF byte 378317, supporting
  page 65 for this pilot without establishing a collection-wide suffix rule.
  Preserved the step 2 match unchanged as its historical metadata-only decision.
- Added `tools/map_cd1_topic.py`, a bounded stdlib generator/verifier requiring
  the exact preserved MVB/RTF hashes. It checks native links against RTF topic
  ordinals/context hashes and rejects unsupported source/layout changes. It
  requires no temporary HELPDECO installation. Documented usage and format
  evidence in `docs/CD1-TOPIC-8802065.md`.
- Format investigation found that HELPDECO's implementation uses a 16,384-wide
  logical TOPICPOS stride for this uncompressed MVB's 4,096-byte physical blocks;
  using the general prose's uncompressed-size formula would mislocate records.
  Native block headers and logical address gaps are handled separately.
- Validation: all 27 tests passed with `make check`, including four focused
  tests for context hashing, cross-block reads/truncation, unsupported layouts,
  and reproduction of the map from actual private sources. The map's default
  read-only verification and the existing step 2 metadata checker both passed.
- Limitations: intro/body roles and article completeness await original viewer
  comparison; other viewer navigation or decoder omissions have not been ruled
  out. Only title/page metadata was decoded, not an article paragraph. Image
  handling, body normalization, and collection-wide mapping remain deferred.
- Investigated the owner's JOHAB observation before committing. On the three
  preserved `.lst` snapshots, strict Python JOHAB and `iconv -f JOHAB -t UTF-8`
  both fail: `column.lst` at byte 74, `language.lst` at byte 7, `panecmds.lst` at
  byte 0. All three decode strictly as EUC-KR identically to CP949, with readable
  Korean labels. Recorded the failed conversion evidence in `docs/CD1-INDEX.md`;
  retained the existing importer encoding. RTF font encodings remain a separate
  step 4 investigation.
- Next: **step 4 — decode one paragraph inside the mapped body**, preserving
  raw bytes and recording font/encoding decisions. The milestone is incomplete.

## 2026-09-18 — Step 4 complete: one strictly decoded body paragraph

- Selected the first prose paragraph under section I within body ordinal 149:
  raw RTF bytes `[378665, 379785)`, including its formatting reset and ending
  paragraph control. No introduction or neighboring article text is included.
- Added `python3 -m tools.decode_cd1_paragraph`, with exact RTF/topic-map/sample
  hash checks. It preserves the raw slice and writes tokenized CP949 bytes,
  UTF-8 text, and provenance to ignored `build/cd1-paragraph/8802065/`.
  Only the metadata record in `data/catalog/paragraph-samples/` is committed.
- Result: 182 text characters (128 Hangul syllables, 54 ASCII), 310 CP949 bytes,
  no replacement characters. Korean, English, parentheses, periods, question
  mark, and original spacing are preserved. No spelling or Unicode normalization
  is applied. The output adds one LF for the terminal paragraph control.
- Font evidence: the sample's `plain` reset selects document default font 4,
  Arial, at 9 points. There are no font changes inside the sample. The RTF header
  lacks explicit code-page/font-charset declarations, so CP949 is a documented
  source-specific interpretation rather than an inference from Arial. Strict
  EUC-KR produces identical text for this paragraph.
- The bounded decoder rejects unsupported controls/groups instead of dropping
  them. It tokenizes byte escapes before decoding, preserves escaped literal
  RTF syntax, and requires exact CP949 round-trip equality. Hidden destinations,
  font switches, symbol glyphs, Unicode escapes, tables, and images remain outside
  its supported subset. No full article conversion was attempted.
- Validation: all 32 tests passed with `make check`, including five new tests
  covering mixed Korean/ASCII and spacing, escaped syntax, malformed/incomplete
  bytes, unsupported controls/groups, and the real private sample's provenance.
  Independent `iconv -f CP949 -t UTF-8` output exactly matches the decoded text
  before its terminal LF; all generated artifact hashes match the record. A
  rerun reproduced all four artifacts byte-for-byte; local documentation links
  and Git exclusion of the decoded output were checked.
- Documented the result in `docs/CD1-PARAGRAPH-8802065.md`. Updated the plan to
  split full-text recovery into **5a — control/font/structure inventory** and
  **5b — ordered full-text recovery**, because this sample alone does not exercise
  the remaining RTF features. Step 5a is the next bounded task.
- Limitations: original viewer glyph/text comparison and article completeness
  remain unverified. The first milestone is not complete.

## 2026-09-18 — Step 5a complete: RTF feature inventory

- Recorded the owner's clarification: full-text extraction/preparation is
  required independently of publication. Possible future access for paper/CD
  owners remains a separate product decision; eligibility and verification are
  unresolved and do not block private recovery. Added that boundary to PLAN.md.
- Added `python3 -m tools.inventory_cd1_rtf`, a byte-preserving lexical inventory
  for introduction 148 and body 149. All 149,579 source bytes are accounted for.
  Detailed token/control/group/font locations stay under ignored
  `build/cd1-rtf-inventory/8802065/`; a compact metadata record is tracked in
  `data/catalog/rtf-inventories/cd1-8802065.json`. No full body text was decoded.
- Classified six metadata footnotes, twelve marker groups, one hidden context
  link, and 21 embedded-object markers. The introduction/body contain 4/319
  paragraph controls, including empty paragraphs. No explicit table, tab, or
  Unicode controls were observed; table/code semantics cannot be inferred from
  that absence, particularly where content is represented by image resources.
- Traced visible text to Arial and 굴림체, with Times selected only for an empty
  introductory paragraph. Group-scoped font resets/restoration and inter-topic
  inheritance are represented. Explicit code-page/font-charset declarations
  remain absent; strict full-text decoding and viewer glyph checks are pending.
- Initial inventory reported five unsupported `\-` symbols in example text.
  Pinned HELPDECO source confirms that its emitter inserts this sequence after
  literal opening braces to prevent sample code from becoming help commands.
  Recorded all five byte positions as literal-brace guards; no unclassified
  constructs remain. Full-text recovery must remove these guards explicitly
  with provenance instead of inserting hyphens or deleting example braces.
- Validation: all 37 tests passed with `make check`, including five new tests
  for byte coverage/binary payloads, scoped font restoration/metadata, object
  versus literal-brace handling, unknown/malformed syntax, and the private-source
  inventory. Reruns reproduced both outputs byte-for-byte; independently joining
  all token spans reproduced both source-slice hashes. Documentation links and
  Git exclusion of the detailed inventory passed. No image conversion, bulk
  extraction, access control, or UI changes
  were performed. The owner's pre-existing untracked `PRD-reading-room.md` was
  read for context and left unchanged and outside this commit.
- Next: **step 5b — recover the complete available text of the two mapped topics
  privately**, preserving structure/provenance and all 21 object placeholders.
  Full-text fidelity and article completeness still require subsequent review.

## 2026-09-18 — Step 5b complete: private full available topic text

- Added `python3 -m tools.recover_cd1_text`. It validates the pinned sources and
  reviewed inventory/sample, then writes separate `introduction.txt`, `body.txt`,
  structured `article.json`, and `provenance.json` under ignored
  `build/cd1-text/8802065/`. Only metadata/hashes are committed in
  `data/catalog/text-recoveries/cd1-8802065.json`.
- Recovered all 268 available text runs using strict CP949, with exact byte
  round trips and zero undecoded runs/replacement characters. Preserved all 4
  introduction and 319 body paragraphs, including blank paragraphs and code-like
  line spacing. Text output has 192/27,686 characters respectively, including
  line endings and generated object placeholders.
- Preserved observed paragraph/run formatting and raw source spans. Kept
  footnote/navigation metadata separate from visible prose without leaking its
  font resets. All 21 object placeholders remain in source order with resource
  names and paragraph/run locations; no image-contained text was transcribed.
- Recorded removal of the five HELPDECO literal-brace guards; example braces
  survive without added hyphens. No spelling corrections, Unicode normalization,
  whitespace collapsing, or inferred table/heading semantics were applied.
- Every one of the 40,351 tokens / 149,579 source bytes has a contiguous ledger
  entry describing its treatment. Undecodable runs would preserve their raw bytes,
  location, and issue placeholder; unreviewed visible controls are rejected.
- Validation: all 42 tests passed with `make check`, including five new tests for
  metadata/font isolation, paragraph formatting/spacing, escapes and objects,
  explicit decoding failures, and private-source recovery. The original step 4
  paragraph matches exactly. An independent source-span scanner and `iconv`
  conversion matched all 268 decoded runs; both ledgers cover their full spans.
  All four generated artifacts reproduced byte-for-byte on rerun.
- Documented the result in `docs/CD1-TEXT-8802065.md` and marked step 5b complete
  in PLAN.md. Private full-text preparation is independent of publication/access
  decisions; no ownership verification or reader UI was added.
- Next: **step 6 — map the 21 object occurrences to their extracted image
  resources and viewable derivatives or explicit unsupported statuses**. Viewer
  comparison and article completeness remain pending; text in images is outside
  the recovered text layer. The first milestone is not complete.

## 2026-09-18 — Structural-fidelity review and Markdown plan

- Investigated the owner's concern that plain text flattens code, figures,
  sections, and other blocks. Clarified that step 5b recovered the text layer and
  formatting evidence, not a finished reading edition. Raw RTF and structured
  paragraph/run output remain preserved and unchanged.
- Found three bold 12-point, seven bold 10-point, and eighteen bold 9-point
  heading candidates. Direct comparison also proved that prose, code, captions,
  and image-marker paragraphs can have identical paragraph/run formatting.
  Style alone therefore cannot identify all block types reliably.
- Located code examples at body paragraphs 182–202 (`.PS`–`.PE`) and 212–217
  (`.EQ`–`.EN`), preserving their source ranges and internal blank lines. Figure
  captions can label code examples as well as rendered images; an automatic
  caption-to-next-image rule would misrepresent this article.
- Recommended Markdown as a derived reading/export format in response to the
  owner's question. Keep preservation data and semantic decisions separately;
  use heading hierarchy, fenced code, captions/images, and supported simple
  tables, with explicit unresolved/complex-layout handling.
- Added `docs/CD1-BLOCK-STRUCTURE-8802065.md` and revised PLAN.md: next is
  **5c — block identification**, followed by **5d — private Markdown preview**,
  then image mapping and viewer comparison. Structural decisions need evidence,
  source references, and uncertainty; no speculative classifications were applied
  to the recovered article in this review.
- Validation: checked the actual private article hash, asserted identical styles
  across representative prose/code/caption/object paragraphs, confirmed both
  code-boundary pairs and heading candidate counts. This is a documentation/plan
  change; recovery code and generated article content were not modified.

## 2026-09-18 — Step 5c complete: semantic block map

- Added `python3 -m tools.map_cd1_blocks`, scoped to the checksummed pilot
  recovery. It combines numbered-label/format evidence with explicit reviewed
  paragraph ranges for code, captions, figures, and opening metadata. It does
  not claim to classify arbitrary articles automatically.
- Produced 271 blocks covering all 323 paragraphs, 289 runs, and 21 objects.
  Identified 28 headings with three-level parent relationships, 17 code/example
  blocks, and 13 explicit caption links. Retained fallback paragraphs and spacing
  blocks. All decisions remain source-supported candidates pending viewer review.
- Preserved four formatting-language examples, twelve isolated commands, and
  one terminal transcript. Internal blank paragraphs and indentation remain
  inside their example blocks. Figure captions can link to code or images.
- Found ten inline WMF objects within the `tbl` example (paragraphs 156–173),
  recorded as mixed text/object content. Kept the following `bm54.wmf` (174)
  unresolved until image inspection. The table image and rendered-table figure
  retain explicit cell-reconstruction limitations; no cell geometry was invented.
- Generated private `blocks.json`/`provenance.json` under
  `build/cd1-blocks/8802065/`, with a tracked metadata summary in
  `data/catalog/block-maps/cd1-8802065.json`. Original paragraph/run recovery is
  unchanged. Each block has source membership, byte spans, evidence, review
  concerns, and a hash of its exact content projection.
- Validation: all 47 tests passed with `make check`, including five new tests
  covering heading evidence, changed-source rejection, mixed-content examples,
  omission/duplication/invalid-link rejection, and code-spacing changes. Exact
  ordered coverage checks include every paragraph, run, and object occurrence.
  Independent projection from block member runs reproduced both text files
  byte-for-byte. Both map artifacts reproduced identically on rerun; the original
  recovery hash, documentation links, and Git exclusion checks passed.
- Recorded the owner's conversion guidance for step 6: BMP/DIB → PNG using
  `convert`, WMF → SVG using `inkscape`. Both commands (and `magick`) are present.
  No images were converted in this step; actual rendering/fidelity checks remain.
- Next: **step 5d — private Markdown preview** from the block map. Preserve mixed
  example placeholders and unresolved attachments explicitly; retain structured
  preservation data. Viewer verification and the first milestone remain pending.

## 2026-09-18 — Step 5d complete: private Markdown preview

- Added `python3 -m tools.render_cd1_markdown`, consuming the checksummed recovery
  and reviewed block map without changing either. Generated separate private
  `introduction.md`/`body.md` and `provenance.json` under
  `build/cd1-markdown/8802065/`; tracked only the renderer, tests, documentation,
  and metadata summary in `data/catalog/markdown-previews/cd1-8802065.json`.
- Represented all 271 blocks, 323 paragraphs, 289 runs, and 21 object occurrences
  in order. Kept 28 headings in three levels below topic titles, 17 verbatim
  code/example fences, and 13 caption links to stable content anchors. Preserved
  source spacing with explicit comments; Markdown does not reproduce RTF layout.
- Escaped prose syntax and retained bold/underline through inline HTML. Fences
  exceed any embedded backtick sequence. Provenance maps every block to UTF-8
  output/content byte ranges and records input/output hashes and source content
  hashes; preservation inputs remain separate from the reading representation.
- Kept the ten inline WMFs in the `tbl` example as ordered placeholders with a
  mixed-content limitation note. Retained `bm54.wmf` as an unresolved attachment,
  image-backed table limitations, and the title icon's uncertain role. No images
  were converted and no resource was silently discarded.
- Initial independent rendering checks exposed Markdown trimming trailing spaces
  from two prose paragraphs. Boundary-space entities fixed the loss; comparisons
  now retain every block's text and all code whitespace. The first build also
  rejected the assumed short topic-role names; the renderer now explicitly maps
  the recovery's `linked_introduction` / `reference_target_body` roles.
- Validation: `make check` passed all 55 tests, including eight new Markdown
  tests. Available `markdown-it-py` independently rendered every content block
  and the complete documents, checking text, fence/heading counts, 271 unique
  anchors, and 13 valid caption targets. Renderer checks skip explicitly where
  that optional test package is unavailable. Deterministic regeneration, input
  hashes, and Git exclusion checks passed; generated content stays private.
- Next: **step 6 — image map and viewable derivatives**. Original-viewer comparison
  is still pending in step 7; this preview does not complete the first milestone.

## 2026-09-18 — Refocus plan on CD1 content preparation

- Read the owner's separate `PRD-reading-room.md` and included it unchanged as
  the viewer/UI reference. Revised PLAN.md around CD1 extraction and organizing
  static content for that reading room; linked both documents from README.md.
- Defined the handoff as pregenerated issue/TOC/article/media data, ordered
  semantic blocks, Markdown previews, converted assets, provenance, and explicit
  coverage/review status. The PRD owns the client-side SPA and UI; the extraction
  plan adds no runtime server, database, or backend requirement.
- Kept step 6 image mapping and step 7 original-viewer comparison next. Added
  subsequent checkpoints for a versioned content contract, one-article package,
  a second structural sample, preservation readiness, one issue, and remaining
  CD1 coverage in bounded tasks. Exact schemas and batch sizes remain to be
  specified from evidence when those steps are reached.
- Distinguished CD1's observed 1988–1993 source coverage from the archive's
  initial 1983-11–1990-12 selection. Later CD1 extraction preserves sources
  outside that selection without inventing TOC records or changing archive scope.
- Removed UI, publication, and access implementation from this plan's future
  queue. Kept full-text preparation independent of publication and eligibility
  decisions; CD2/CD3 and later scans belong to separate future scopes.
- Validation: checked local documentation links and the staged diff; confirmed
  the supplied PRD is byte-for-byte unchanged. Documentation-only revision; no
  extraction output or code changed, so no test rerun was needed. The initial
  combined edit was rejected on a mismatched context line and reapplied in smaller
  patches. Git's whitespace check reports the supplied PRD's existing final blank
  line; retained it to preserve the owner's file and checked its other whitespace
  separately. Next implementation task remains **step 6**.

## 2026-09-18 — Extend archive target and separate disc plans

- Extended the archive target to **1983-11–1995-12: 146 monthly issues**, based
  on the owner's official CD holdings. The existing TOC remains a source for
  86 issues through 1990-12; the additional 60 months require source-supported
  metadata, not invented TOC entries or presumed complete CD coverage.
- Renamed `PLAN.md` to `PLAN-CD1.md` and updated active documentation links.
  Added deferred `PLAN-CD2.md` and `PLAN-CD3.md`, each with its own source/format
  inspection task and subsequent sample-first checkpoints. Their apparent 1994
  and 1995 coverage and decoder compatibility still need verification. CD1's
  active task remains **step 6 — image mapping and conversion**.
- Updated README.md with the expanded scope and three plans. Marked the old
  design reference's 86-issue scope as historical; retained historical progress
  entries as written. Documented that the TOC importer's default expected range
  describes the supplied file and therefore still ends at 1990-12.
- Updated CD1 index importer 0.2.0 to classify target-period candidates through
  1995-12 and record the target range in generated reports/manifests. All 1,038
  numeric references are now in range; the historical 360 references for
  1988–1990 remain independently checked. Original index occurrences, native
  references, TOC identities, recovered article content, and the reading-room
  PRD are unchanged.
- Validation: all **56 tests** passed with `make check`, including a new test for
  inclusive period boundaries, later years, invalid months, and named references.
  Regenerated the private CD1 index and rechecked the pilot metadata match.
  Verified documentation links, absence of stale active `PLAN.md` references,
  source-period/target-period distinction, and staged whitespace/diff checks.
  No CD2/CD3 extraction was started.

## 2026-09-18 — CD1 step 6 complete: image map and conversion report

- Added `python3 -m tools.map_cd1_images`, verifying the pilot's article/block
  hashes and every image against the extraction manifest before conversion.
  Mapped all 21 occurrences to topic, paragraph, run, block, caption relationships,
  source filename/hash, and private derivatives. There are 21 names but 16 distinct
  source hashes; six pointing-hand WMFs are byte-identical and retain all positions.
- Followed the owner's conversion suggestions: ImageMagick `convert` produced
  nine PNGs from one BMP and eight DIB-named BMP files; Inkscape produced twelve
  SVGs from WMFs. Added twelve white-background PNG inspection renders at 384 dpi.
  Recorded tool versions, commands/logs, dimensions, source/output hashes, and
  font resolution. Pillow independently checks decoded RGBA pixels and is now an
  explicit dependency. All nine bitmap conversions preserve dimensions/pixels.
- Generated `images.json`, `provenance.json`, and an ordered `review.html` under
  ignored `build/cd1-images/8802065/`. Only a compact metadata summary is tracked
  in `data/catalog/image-maps/cd1-8802065.json`; originals and media stay private.
  Prior recovery, semantic blocks, and Markdown previews remain unchanged.
- Inspected private raster/vector contact sheets. The title contains a section
  badge whose navigation behavior remains unverified. Inline WMFs contain six
  pointing hands and four overlined numerals. Table images remain images; no
  OCR, cell geometry, or transcription was invented.
- Found two explicit exceptions: `bm54.wmf` yields an SVG with no drawing
  elements and an entirely white preview; its intended content/attachment remains
  unresolved. Figure 11's `bm55.wmf` loses Symbol-font mathematical glyphs, showing
  incorrect summation/infinity characters. A `wmf2svg --inline` fallback produced
  invalid encoding and replacement glyphs, so it was not adopted. Font lookup
  also substitutes Liberation Serif for Times New Roman in text-bearing SVGs.
- Recorded 19 resources as `converted_pending_viewer` and two as `needs_review`.
  No image is fidelity-verified. Added targeted original-viewer comparison items
  to the offline checklist and detailed step 7's scope in PLAN-CD1.md. The blank
  object and damaged equation must be addressed before the sample can pass.
- Validation: all **63 tests** passed, including seven new image tests covering
  manifest integrity, missing/unsafe inputs, converter failure, empty SVG content,
  exact occurrence order, duplicate-resource preservation, source/output hashes,
  pixel equivalence, and review flags. Full conversion reruns reproduced identical
  outputs; final PNGs match the visually inspected probe images pixel-for-pixel.
  Documentation links, Git exclusions, and whitespace checks passed.
- Next: **step 7 — original-viewer comparison**. The first milestone remains
  pending; no reading-room packaging, bulk recovery, or CD2/CD3 work was started.

## 2026-09-18 — Defer broken-media repair at the owner's request

- Changed the current priority: record broken conversions and continue content
  preparation without investigating their repair now. This supersedes step 6's
  earlier requirement to resolve the blank object/equation before proceeding.
- Added `data/catalog/deferred-media/cd1-8802065.json` for `bm54.wmf` and
  `bm55.wmf`, preserving source hashes, exact occurrences, block/caption links,
  observed problems, and references to recorded conversion attempts. Both are
  unresolved, explicitly deferred, and nonblocking for current progress.
- Updated PLAN-CD1.md and the image findings: step 7 can accept the usable
  article content with deferred media recorded, then proceed to packaging and
  later extraction. Full image fidelity stays unverified. Missing evidence for
  other comparison checks still needs to be collected; no comparison is claimed
  to have happened in this revision.
- Future reading exports retain unavailable-media placeholders and captions at
  the original positions instead of presenting suspect derivatives as recovered
  images. Originals and existing private diagnostic outputs remain preserved.
  Changed the two problem-image captures in the offline checklist to optional
  later work. Further conversion failures should use the same record-and-defer
  approach rather than trigger immediate investigation.
- Validation: checked the deferred records against the existing image map and
  source hashes/occurrences, verified local documentation links and the staged
  diff. No code, recovery, or generated media changed; no conversion or test
  suite rerun was needed. Next task remains **step 7**, with these exceptions
  excluded from its required repair work.

## 2026-09-18 — Use physical magazines for content verification

- Removed original CD1 viewer comparison as a required task at the owner's
  request. Physical magazine pages, or legible scans/photos of them, are now
  the reference for content accuracy. Technical extraction checks still compare
  decoded content and converted media with preserved CD sources.
- Replaced step 7 with a deferred physical-magazine comparison: record the issue,
  edition/page evidence, extent compared, and metadata/text/structure/media
  differences. Preserve CD-derived text and document any print-based correction
  separately; a difference may originate in the CD edition, not extraction.
- Made **step 8 — reading-room content contract** the next active task. The
  preparation milestone now ends with step 9's reproducible sample package;
  pending print verification and registered broken-media exceptions do not block
  content preparation. No physical-page comparison has yet been claimed complete.
- Rewrote the offline checklist around locating the February 1988 printed
  article, establishing its actual page range, and keeping scans/photos with
  provenance when convenient. Removed required viewer screenshots, copy/export
  experiments, and navigation-behavior checks. Partial pages support only partial
  comparison; no full scan set is required before development continues.
- Updated image documentation to explain that existing `converted_pending_viewer`
  and false `viewer_compared` fields are historical conversion metadata, not
  current workflow requirements. Kept those checksummed artifacts and the deferred
  image records unchanged; the upcoming contract will distinguish extraction
  integrity from physical-magazine verification.
- Validation: checked documentation links, the revised active/deferred step
  sequence, and the staged diff. This changes planning and offline guidance only;
  no code, extraction output, or media changed, so no test rerun was needed.

## 2026-09-18 — CD1 step 8 complete: reading-room content contract v1

- Added a versioned JSON Schema and documented static catalog, issue, article,
  media, and package-manifest documents. Stable identities reuse native CD
  references and existing TOC/block/occurrence IDs. Explicit manifest lookups and
  package-relative paths support a configurable base URL without local paths.
- Defined ordered sections, blocks, paragraphs, and text/media runs, preserving
  bold/underline, code indentation, empty paragraphs, trailing spaces, inline
  images, heading hierarchy, and caption relationships. Image-backed tables and
  unresolved blocks remain explicit; Markdown is a derived preview rather than
  the required runtime representation of mixed code/media content.
- Added a synthetic public fixture and a deterministic private pilot exporter,
  invoked with `make reading-room-example`. The pilot contains all 39 February
  1988 TOC entries, with one established match and 38 unmatched entries, plus
  two sections, 271 blocks, 323 paragraphs, 289 runs, 21 media occurrences, and
  13 caption relationships. Unknown cover/end page and original TOC order remain.
- The 19 accepted media derivatives have checked hashes and planned package
  paths. Deferred `bm54.wmf` and `bm55.wmf` retain occurrence/caption links and
  problem IDs, with null display assets. Suspect derivatives are not exposed as
  article images. No repair, asset copying, or full package build occurred here.
- Separated source extraction checks from pending physical-magazine verification.
  Runtime data contains source identities and statuses; a private provenance
  sidecar holds input/schema hashes, source spans, metadata evidence, and local
  asset bindings. Publisher text and all generated outputs stay ignored/private;
  only the schema, code, synthetic example, and metadata summary are tracked.
- Validation: all **77 tests passed**, including 14 contract tests for exact
  source-run/text/format preservation, repeatable output, independent document
  schemas, many-to-many TOC links, mixed media, unavailable placeholders,
  manifest inventory/preview ownership, unsafe paths, duplicate/dangling
  identities, stale catalog projections, and independent print-review metadata.
  Two command-line rebuilds reproduced the recorded output hashes; documentation
  links, generated-output exclusions, and staged whitespace checks passed.
- Updated PLAN-CD1.md: **step 9 — one-article content package** is next, with
  explicit file/hash/reference and deterministic-rebuild checks. The first
  preparation milestone remains pending until that package passes. Deferred
  physical-magazine comparison, UI work, and CD2/CD3 extraction remain separate.

## 2026-09-18 — CD1 step 9 complete: private one-article package

- Assembled the approved v1 contract example into
  `build/reading-room-packages/cd1-8802065/content/`: catalog, issue, article,
  media index, manifest, two Markdown previews, and 19 accepted images. The
  **26 runtime files** total 376,531 bytes; separate private provenance records
  source/input fingerprints, asset bindings, preview content ranges, and hashes.
  The approved schema and existing source/recovery outputs remain unchanged.
- Added `make reading-room-package` and standalone `--verify CONTENT_DIRECTORY`.
  The latter needs only package files, validator code/dependencies, and the schema;
  it does not read extraction inputs. Validation checks individual schemas, the
  complete relationship graph, manifest identities, actual hashes/sizes, exact
  file inventory, generated caption anchors, and SVG resource dependencies.
- Preserved all 39 TOC entries, two sections, 271 blocks, 323 paragraphs, 289 runs,
  21 media occurrences, and 13 caption relationships. Package JSON round-trips
  exactly to the approved example; source text projections match recovered
  introduction/body bytes. Unknown cover/end page and 38 unmatched TOC entries
  remain explicit. Print verification remains pending.
- Copied nine PNGs and ten SVGs byte-for-byte. Deferred `bm54.wmf`/`bm55.wmf`
  retain null display assets, occurrences/captions, and problem IDs. Suspect
  derivatives and diagnostic previews are absent. Four SVGs retain recorded
  font-substitution concerns; package integrity does not establish image fidelity.
- Adapted generated Markdown notes to the current media/physical-magazine status
  only in package copies. All 271 protected block-content ranges are unchanged,
  including code whitespace and mixed image placeholders; caption links resolve.
  Original step 5d previews and their checksummed provenance remain intact.
- Builds validate a staging directory before replacing the generated package.
  Failed staging leaves the previous result intact; successful rebuilds remove
  stale files. Added a tracked metadata-only summary, reproduction/handoff docs,
  and 11 package tests. All publisher content remains ignored/private.
- Validation: all **88 tests passed**. Two command-line rebuilds reproduced the
  reviewed hashes; standalone validation and relocated-package tests passed.
  A temporary localhost static server served all 26 files beneath `/archive/data/`,
  with each response matching its recorded bytes/hash. Missing/corrupt files,
  unexpected derivatives, unsafe paths, symlinks, mislabeled documents, broken
  caption anchors, and external/dangling SVG resources are rejected. Documentation
  links, Git exclusions, and staged whitespace checks passed.
- The **first CD1 preparation milestone is complete**. PLAN-CD1.md now advances
  to **step 10 — second-article check**. Deferred physical-magazine comparison,
  media repair, UI implementation, publication/access policy, and CD2/CD3 remain
  separate; none is claimed complete by this package.

## 2026-09-18 — CD1 step 10 complete: second article verifies schema v1

- Selected **스펠링 체커**, CD reference `8802114`, February 1988 page 114.
  Three index occurrences agree with one exact TOC title under the utility
  section (`maso-1988-02-toc-0021`). Native context/hash and RTF aliases confirm
  introduction/body topics 151–152, the hidden introduction link, and the following
  separator/browse boundary. The CD page label independently agrees with the TOC.
- Inspected a different structure: unnumbered headings, one usage command,
  three captioned Pascal listings, and one bitmap title badge. The first decoder
  probe rejected 417 font-15 runs; the header identifies Fixedsys and all 12,608
  encoded bytes are ASCII. Added an opt-in strict-ASCII font policy, retaining
  the original decoder default and explicit failures for other fonts/non-ASCII
  Fixedsys data. No source spelling or code errors were repaired or executed.
- Recovered all 27,624 source bytes with contiguous accounting: 485 paragraphs,
  439 runs, and 34 decompiler brace guards handled explicitly. Mapped 39 blocks,
  including three listing ranges of 317/36/96 paragraphs and three caption links.
  Unnumbered headings use inspected formatting/context; the original pilot's
  numbered-heading decisions remain unchanged.
- Converted `bm40.bmp` to a 32 × 25 PNG with identical decoded RGBA pixels and
  visually inspected the title badge. Its navigation behavior remains unresolved.
  Reused Markdown rendering with article-specific labels/anchors, preserving
  original first-pilot output hashes and every new block's content bytes.
- Added `make check-second-article`. It creates private recovery, inventory,
  block map, text projections, provenance, an 8-file standalone package, and a
  30-file combined package under `build/cd1-second-article/8802114/`. The combined
  package has two articles, four sections, 310 blocks, 808 paragraphs, 22 media
  occurrences, 20 accepted assets, and four previews. Two TOC entries are matched;
  37 remain unmatched. The original two deferred media remain unavailable.
- **No schema change was needed.** Long preformatted blocks, unnumbered headings,
  listing captions, media occurrences, shared issue metadata, and stable IDs all
  fit v1. The approved schema hash remains unchanged. This verifies the two
  inspected cases; it does not establish support for all remaining CD structures.
- Validation: all **95 tests passed**, including seven new tests for opt-in
  decoding/failures, native boundaries/accounting, every source run/mark, long
  listing ranges, heading classification, bitmap pixels, preview content, and
  relocated standalone/combined packages. Two command-line rebuilds reproduced
  all reviewed hashes; standalone package verification passed. First-pilot
  recovery, Markdown, contract, and package regressions remain byte-identical.
  Documentation links, generated-output exclusions, and staged whitespace checks
  passed. The initial synthetic font-policy test had an unescaped RTF brace;
  correcting that fixture produced the intended literal-brace preservation check.
- Updated PLAN-CD1.md and offline guidance: **step 11 — CD1 preservation
  readiness** is next, with separate inventory and backup/restore evidence.
  Physical-magazine verification stays pending. Publisher content remains private;
  only code, tests, documentation, and the metadata summary are tracked.

## 2026-09-18 — CD1 step 11a complete; independent backup/restore pending

- Rechecked the 351,090,688-byte original CD1 ISO against its initial SHA-256.
  Compared a fresh temporary ISO extraction with `masocd-1/`: all **5,828 files**
  (343,516,641 bytes) and **375 directories** match, with no missing/extra files,
  symlinks, or content differences. The MVB hash matches the preserved probe's
  source fingerprint. Source files were not modified.
- Verified all **7,374 probe-manifest entries** (7,372 decoder outputs plus two
  process logs), and inventoried the manifest, build log, and internal-directory
  listing. The complete probe tree is **7,377 files / 272,378,566 bytes**.
  Detailed file/directory records remain private in
  `build/cd1-preservation/inventory.json`; a tracked metadata summary pins its
  3,111,986 bytes and SHA-256. Observed source timestamps and tool/decoder evidence
  are retained without treating them as publication dates.
- Added `make inventory-cd1-sources` and an optional independent-ISO restore check.
  The latter requires a supplied backup location/storage description, creates a
  fresh temporary restore, verifies the copied ISO and every extracted disc file,
  and records actual evidence privately with a sanitized tracked summary. It
  rejects the working image/workspace-local copies, corrupt input, unsafe paths,
  and restored-tree differences. Device IDs do not prove physical independence.
- The first inventory attempt exposed a path-ordering comparison mismatch between
  component-sorted paths and relative strings. Using consistent relative-string
  ordering fixed it; a regression test covers the case. No source discrepancy
  was found after full hash comparison.
- The owner explicitly confirmed **no independent backup yet**. No real backup
  copy or independent restore test was performed. Recorded step **11a complete**
  and **11b deferred**, with `ready_for_bulk_processing: false` in the readiness
  record. Synthetic restore tests validate mechanics only, not actual preservation.
- Documented the preservation set: original ISO, whole probe tree, inventory,
  repository/canonical metadata, and prepared private artifacts/toolchain evidence.
  ISO plus probe is 623,469,254 bytes; including the reconstructable disc tree is
  966,985,895 bytes. Machine-specific backup locations stay private when supplied.
- Validation: all **104 tests passed**, including nine new inventory/restore
  tests covering tampering, missing/extra files, empty directories, manifest
  coverage, symlinks, unsafe archive paths, tool failure, working-copy rejection,
  temporary cleanup, and restoration mismatch. Two command-line inventories
  reproduced the reviewed output hash. Documentation links, Git exclusions, and
  staged whitespace checks passed.
- Next non-deferred task: **12a — read-only February 1988 TOC/CD coverage audit**.
  Split issue work into coverage first and later bounded article batches. Those
  batches and bulk processing remain gated on step 11b's real preservation
  evidence. Print comparison, media repair, CD2/CD3, and UI work remain separate.

## 2026-09-18 — CD1 step 12a: February 1988 coverage audit complete

- Added `make audit-cd1-issue` and a read-only `--check` mode. The tracked
  metadata report retains all **39 TOC entries** in source order, with persistent
  IDs, hierarchy, original source locators, and explicit relationship/preparation
  status. It includes all **five indexed CD references / 11 occurrences**
  attributed to February 1988 by the three indexes.
- Reproduced the TOC entries from the reviewed source snapshot and identity
  registry, and all CD index entries/groups from the checksummed CP949 originals.
  All five target hashes resolve in the original MVB context table; their native
  offsets are retained. Context resolution does not establish article boundaries,
  printed page numbers, or complete printed-issue coverage.
- Retained two existing matches (`8802065`, `8802114`), added two supported
  metadata relationships (`8802030`, `8802184`), and recorded `8802180` as an
  unresolved candidate: TOC `그래픽스 툴` versus CD `그래픽 툴`. The interview
  comparison removes its specific series prefix; no general fuzzy-title rule or
  page-suffix-only matching was introduced. New matches remain audit metadata.
- The TOC has four section headings and 35 article candidates. Four candidates
  are matched, one is unresolved, and **30 article candidates have no index
  match**. The latter status does not assert that their bodies are absent from
  the CD. Unindexed native targets and physical print completeness remain outside
  this audit's established coverage.
- Verified the existing combined package against its tracked hashes and v1
  standalone validator: two prepared articles, four sections, 39 TOC entries,
  and 30 runtime files. Three indexed targets remain unprepared. No new article
  recovery, runtime package/schema changes, image repair, or publication occurred.
  Local inventory evidence still verifies; independent backup/restore is pending.
- The owner's working `TOC.md` now appends 1991–1993 entries. Its reviewed prefix,
  including February 1988, is byte-identical. The audit verifies the historical
  SHA-256 using the preserved Git blob and additionally compares the live issue
  section; it does not overwrite/reimport the expanded TOC. Those user changes
  remain unstaged and outside this commit.
- Validation: all **nine new coverage tests pass** with the expanded working TOC;
  repeated report checks reproduce identical metadata. Tests exercise duplicate
  titles/references, missing index evidence, issue-label/reference conflicts,
  named targets, unresolved variants, prepared identity mismatches, and source
  order/snapshot checks. Documentation links and whitespace checks pass.
- The working-tree full suite reports one failure and two errors caused by the
  expanded TOC: changed second-article provenance, the pilot's old source hash,
  and the original TOC importer range/validation. In a temporary copy using the
  reviewed TOC snapshot, **all 113 tests pass**. The first temporary harness used
  symlinked source directories, which the existing validators correctly rejected;
  rerunning with real file copies passed. No user source was replaced to run tests.
- Updated PLAN-CD1.md and offline guidance. Next is **12a.1: validate/import the
  expanded TOC**, resolving duplicate `93.10` / missing `93.09` headings from
  source evidence and preserving historical provenance when imports grow. The
  first later article batch is **12b.1: `8802030` only**, explicitly gated on
  step 11b's independent backup/restore evidence. Subsequent targets `8802184`
  and `8802180`, print comparison, and remaining CD1 coverage stay separate.

## 2026-09-18 — CD1 step 12a.1: expanded TOC import and historical provenance

- Accepted the owner's corrected September 1993 heading. The source now has
  **122 consecutive, unique issues from 1983-11 through 1993-12**. Removed one
  empty trailing `-` formatting artifact; all substantive supplied text is
  retained. The corrected expanded TOC is committed with its identity map.
- Updated the importer/CLI default end month to `1993-12`. Imported **5,497 TOC
  entries and 4,078 article candidates**, with no validation/identity errors.
  The archive target still ends in 1995-12; no unsupported 1994–1995 TOC entries
  were invented. Source SHA-256 is
  `15d932cf6a34f14981b07ff875d1b5be4f43a525063c303d2d99f54169987727`.
- Preserved all **3,811 existing identities**, their issue allocators, and all
  earlier entry fields except the source-wide fingerprint. Added **1,686 new
  identities**; none were retired. All 3,608 review notices are retained,
  including seven suspicious indentation cases in the additions. Candidate
  counts are not a verified article census or publication approval.
- Added a tracked expansion record containing source/output hashes, counts,
  and migration checks. Current output remains in ignored `build/toc/`; the
  durable identity registry is versioned. Repeated imports preserve every output
  byte and identity allocation.
- Added an explicit historical TOC snapshot descriptor and
  `make restore-toc-snapshot`. Source and identity blobs from Git reconstruct the
  old import in a separate ignored cache; every output is checked against its
  reviewed hash. The recorded old manifest is retained verbatim, including its
  historical runtime versions. Restoration does not overwrite current inputs;
  missing/corrupt historical data cannot silently fall back to the current TOC.
- Updated the pilot match checker, contract/package builders, second-article
  checker, and February coverage audit to read those historical inputs explicitly.
  Their original logical paths and fingerprints retain their historical meaning.
  **No prepared article, provenance file, package summary, coverage report, or
  approved runtime schema was rewritten.** The coverage audit still verifies
  that February's current source section agrees with the historical snapshot.
- Validation: **all 116 tests pass in the expanded working tree**. Three new
  tests cover snapshot restoration, corruption/missing-cache rejection, current
  input isolation, complete identity/field preservation, and deterministic expanded
  reimports. The first full run found one remaining package-builder dependency
  on the live manifest; moving that historical read to the snapshot resolved it.
  The final snapshot test also runs from Git inputs without requiring a preexisting
  cache. Command-line import, historical restore, pilot match verification, and
  coverage reproduction passed; documentation links and whitespace checks passed.
- Marked step **12a.1 complete**. Next article task **12b.1: `8802030` only** is
  fully scoped in PLAN-CD1.md and remains gated on step 11b's real independent
  backup/restore evidence. Physical comparison, unresolved title/media cases,
  later article batches, CD2/CD3, and the reading-room UI remain separate.

## 2026-09-18 — CD1 preservation handoff prepared; recovery sources clarified

- Continued the pending preservation checkpoint by preparing a portable local
  transfer archive. It contains the original ISO, entire probe tree, current build
  artifacts/inventories/historical TOC cache, and committed Git refs/history through
  `a0cf9971227092f0d372591db1d0a723a266fbb1`. The reconstructable extracted disc
  tree is omitted. Uncommitted files and ignored material outside the named source
  sets are explicitly outside this snapshot; the new transfer tool is committed
  after the captured content revision.
- The private archive is **673,433,600 bytes**, with **7,581 payload files** totaling
  666,343,528 bytes. SHA-256:
  `a18c40ba44c5be68316d60ccdd2210e236ff290b7d5b51149b972602151bed3a`.
  A `.sha256` sidecar and private receipt sit alongside it; the tracked transfer
  receipt records its relative path/hash. `MANIFEST.json` retains all payload
  hashes and directories, and `RESTORE.txt` provides recovery instructions.
- Added `make prepare-cd1-transfer`. It first checks the ISO/probe against the
  preserved inventory, stages a Git bundle, writes a fresh private archive, and
  verifies every archived payload byte without extracting. Source changes,
  unsafe paths, links, duplicate members, missing files, and corrupt content are
  rejected. Names include commit/content hashes so newer sets retain older ones.
- Verified the real archive and Git bundle. Cloned the archived bundle into a
  temporary mirror, ran `git fsck --full`, checked the captured HEAD, and verified
  the historical TOC blob. These checks were local; no independent copy or
  physical-disc read was performed, and readiness remains false.
- The owner clarified that a **local copy and physical CD are available**.
  Updated readiness from unavailable to unverified, recording the physical CD as
  an owner-reported independent recovery source. Its readability has not been
  tested here. No optical drive is visible in the machine's block-device listing;
  the local copy's accessible path and storage independence remain unspecified.
  Requested a copy/device location to perform the next verification.
- Validation: **all 120 tests pass**, including four new transfer tests for exact
  round trips, deterministic bytes, source preservation, payload/manifest
  corruption, missing/duplicate members, unsafe paths, and archive/source links.
  Documentation links, private-output exclusions, and whitespace checks pass.
- Updated PLAN-CD1, preservation/offline guidance, and the readiness record.
  The transfer set is ready to copy. Step 11b still needs accessible recovery-source
  and preservation evidence before article task 12b.1 (`8802030`) begins. No new
  article text, media conversion, publication, or external-storage write occurred.

### Owner clarification: working image and retained physical CD

- The reported local copy is the existing `masocd-1.iso`, extracted from the
  owner's retained physical CD. It is not an additional independent digital copy.
  The owner confirms no optical drive is currently available.
- The source location question is resolved. Recorded the physical original and
  unavailable drive explicitly; step 11b remains deferred until independent
  storage or an optical drive is available. The prepared local transfer archive
  remains verified and ready to copy. No independent restore test or further
  article recovery was performed.

## 2026-09-18 — Separate preservation verification from extraction progress

- Corrected the overly strict backup prerequisite after clarifying its purpose
  with the owner. Step 11b concerns recoverability and file integrity; it does
  not verify legal ownership or publication rights. It remains deferred without
  blocking extraction that reads checksummed originals and writes separate outputs.
- Updated PLAN-CD1, current guidance, and readiness metadata. Replaced the
  ambiguous bulk-readiness flag with separate independent-restore verification,
  extraction-permission, and backup-blocking fields. No backup or physical-CD
  read is newly claimed, and no extraction source has been modified.
- Kept the reviewed February coverage report byte-identical. Its historical
  next-batch prerequisite is explicitly superseded by the current plan; coverage
  findings and prepared-article provenance are unchanged.
- Next is **12b.1: `8802030` (CP/M의 게리 킬달)**. Then prepare the other February
  targets, assemble the issue package with explicit missing/unmatched content,
  and expand across CD1. The pilot/tooling phase is largely complete, but only
  two articles are packaged so far; the final numbered stages still contain
  substantial content-recovery work. CD2/CD3 and the reading-room UI remain separate.
- Validation: checked readiness JSON, documentation links, remaining gate wording,
  and whitespace. No code, schema, or article output changed; tests were not rerun
  for this planning/metadata correction.

## 2026-09-18 — CD1 step 12b.1: Gary Kildall interview prepared

- Mapped reference **`8802030` / CP/M의 게리 킬달** to native body topic 146
  (hash `0x0e6881f5`, alias `6SRE0ZE`) and linked introduction 145 (`3M4UJI`).
  Both CD index occurrences agree with February 1988 and the specific TOC series
  prefix comparison for `maso-1988-02-toc-0031`. The CD explicitly reports page
  30 and credits `글/ 편집부`; end page and print comparison remain unknown/pending.
- Verified both RTF aliases against native context offsets, the introduction
  link, adjacent separators 144/147, and previous/next browse boundaries. The
  two selected spans total **71,443 bytes**. An initial adjacent-topic probe hit
  unsupported `tab` controls in the preceding article; its text was excluded
  from this bounded task. The actual interview topics need no decoder extension.
- Recovered **107 paragraphs / 85 runs / one media occurrence**, with strict
  font 4/5 CP949 decoding and complete byte/token accounting. Every paragraph,
  run, mark, and spacing block survives projection into the unchanged v1 contract.
- Identified **27 interview prompts and 40 answer paragraphs** using reviewed
  positions, bold/plain runs, indentation, spacing, and source order. Prompts
  remain bold paragraph blocks; no artificial headings or visible speaker labels
  were introduced. Private block/provenance metadata preserves explicit turn
  associations and interview-question/answer subtypes. Dedicated runtime Q/A
  roles would require a future contract extension; they are not claimed here.
- Converted the 32 × 25 title-linked `bm42.bmp` to PNG and confirmed decoded
  RGBA equality. The small marker is not an interview photograph. Source object
  position and emphasis remain intact; no other media occurs in these topics.
- Preserved the owner's *Programmers at Work* attribution as an owner-provided
  bibliographic note, unverified against the book. No book credit was observed
  in the recovered text; the CD's editorial byline remains unchanged. The TOC
  series label `(5)` and introduction's fourth-programmer wording are retained
  without harmonization. No book/print completeness or publication rights are
  inferred, and publisher text/assets stay in ignored build output.
- Added `make prepare-cd1-interview`, an **8-file standalone package**, and a
  **34-file combined three-article package** under `build/cd1-articles/8802030/`.
  Standalone validation precedes composition. The combined package has six
  sections, 417 blocks, 915 paragraphs, 23 media occurrences, and six previews.
  All 39 TOC entries remain; three link to prepared articles. Earlier article
  documents/previews remain byte-identical, including both deferred media states.
- Reused the second-article assembler and parameterized its section projection
  with defaults preserving the earlier result. No schema or general decoder
  changes were needed. The historical two-article package and coverage report
  remain unchanged; the new preparation summary records the newer status.
- Validation: **all 128 tests pass**, including eight new interview checks for
  native boundaries, complete byte accounting, every run/mark, multi-paragraph
  answers, rejected style drift, bitmap pixels, preview content ranges, relocated
  standalone/combined packages, old article preservation, and attribution limits.
  A second command-line build reproduced the reviewed record. Documentation links,
  private-output exclusions, and whitespace checks pass.
- Updated PLAN-CD1 and current guidance: **12b.1 complete; 12b.2 (`8802184`,
  터보 C로 작성한 에디터) is next**. Three of February's five indexed targets are
  prepared; `8802184` and `8802180` remain. Backup/restore and physical comparison
  remain independently deferred and do not block extraction.

## 2026-09-18 — CD1 step 12b.2: Turbo C editor prepared

- Mapped **`8802184` / 터보 C로 작성한 에디터** to body topic 161 (`1KN6LK`,
  hash `0x0e6841c5`) and introduction 160 (`3M4LOC`). Native context offsets,
  the introduction link, adjacent separators 159/162, and browse boundaries
  agree. The selected RTF spans total **62,315 bytes**. Both index occurrences
  match TOC entry `maso-1988-02-toc-0027`, February 1988, and page 184. The CD
  credits `글/ 우원식`; end page and physical comparison remain unknown/pending.
- Recovered **1,206 paragraphs / 1,117 runs / five media occurrences** with
  strict CP949 for fonts 4/5 and ASCII for explicitly identified Fixedsys font 15.
  Every source byte is accounted for; no unsupported runs remain.
- Added explicit RTF `\tab` support: all **30 tabs** survive as U+0009 with
  source spans and transformation records. They are not expanded to spaces.
  Parameterized tabs and unsupported controls still fail. The existing 175
  HELPDECO brace-guard removals remain separately recorded.
- Mapped **85 blocks**, including a **1,121-line C listing**, a two-line example
  in the prose font, 14 headings, three figures, and four caption relationships.
  Code text, blank lines, tabs, and apparent source spelling errors remain exact
  in JSON and Markdown. Closing-heading placement is explicitly an interpretation
  pending physical review. No historical program was compiled or executed.
- Converted all five bitmaps to PNG with identical decoded RGBA pixels and
  visually inspected the three diagrams. The shared `bm40.bmp` icon keeps its
  existing identity and bytes; it appears once in the combined media index.
  No deferred WMF repair was attempted, and their existing records remain intact.
- Added `make prepare-cd1-editor`, a **12-file standalone package**, and a
  **41-file combined four-article package** under `build/cd1-articles/8802184/`.
  Standalone validation precedes composition. The combined package has eight
  sections, 502 blocks, 2,121 paragraphs, 27 media records, 28 media occurrences,
  and eight previews. All previous article documents, previews, media records,
  and image assets remain identical. Schema v1 is unchanged.
- Validation: **138 tests pass**, including eight editor integration checks and
  two tab-decoder checks. Coverage includes complete byte accounting, every run
  and mark, exact fenced code, tab transformations, heading/caption relationships,
  rejected evidence drift, bitmap pixels, relocated packages, and shared media.
  Earlier recovery/package records still reproduce under the extended decoder.
  A second command-line build reproduced the reviewed record. Local documentation
  links, readiness JSON, private-output exclusions, and whitespace checks pass.
- Updated current guidance: **12b.2 complete; 12b.3 (`8802180`) is next**, starting
  with its TOC/CD title variation. Four of February's five indexed targets are
  prepared; 35 of 39 TOC entries remain unmatched in the runtime package.
  Historical packages and the earlier coverage audit stay unchanged. Publisher
  text and assets remain ignored private output; print comparison, backup/restore,
  and publication decisions remain separate from this extraction checkpoint.

## 2026-09-18 — CD1 step 12b.3: Turbo Pascal graphics prepared

- Resolved the metadata candidate **`8802180`** using new source evidence:
  the native, introduction, and body titles exactly match TOC entry
  `maso-1988-02-toc-0026` (`터보 파스칼 한글 그래픽스 툴`). Both CD index occurrences
  retain the shorter `그래픽` spelling. The body confirms February 1988/page 180
  and byline `글/ 신상돈`. No global title normalization or TOC edit was made.
- Verified native body 158 (`1KN6LQ`, hash `0x0e6841cb`), introduction 157
  (`3M4LOI`), separators 156/159, and browse boundaries. Recovered all selected
  **26,283 RTF bytes**, producing **397 paragraphs / 362 runs / seven media
  occurrences** with complete token accounting.
- Preserved **80 blocks**, including three Pascal listings of **18/210/91
  paragraphs**, an isolated formula and call, eight headings, six captions, and
  three figures. Code whitespace, source punctuation, blank lines, and all
  inline media positions remain intact. No program was compiled or corrected.
- Seven font-15 runs contain non-ASCII strings. The article explicitly uses
  strict CP949 for that font; prior articles keep their ASCII policies. One demo
  string remains a possible mixed-encoding case: two `88 74` pairs decode as
  `늯` in CP949 and `값` in Johab. Recorded both interpretations, exact source
  span and pending status; the alternative is not applied. A generated preview
  note points out the review question without altering source content.
- Kept figure 3's text header and bitmap as two ordered paragraphs in one figure
  block. Extended Markdown rendering for multi-paragraph figures; v1 already
  supports the structure. Historical article/previews still reproduce exactly.
- Converted five bitmaps with identical RGBA pixels and visually inspected the
  three figures. Deferred inline `bm57.wmf` and `bm58.wmf` after conversion lost
  their Symbol font. Tracked their source hashes, positions, problem IDs, and
  null runtime assets; retained diagnostic SVG/PNG files privately. No repair
  was attempted. Identical source bytes retain the two distinct resource IDs.
- Added `make prepare-cd1-graphics`, a **12-file standalone** package, and a
  **48-file combined five-article** package under `build/cd1-articles/8802180/`.
  Standalone validation precedes composition. The combined package has ten
  sections, 582 blocks, 2,518 paragraphs, 33 media records, 35 occurrences, and
  ten previews. Its shared icon and every prior article/media output remain
  identical. Four WMFs are now explicitly deferred across the five articles.
- Validation: **148 tests passed**, including ten new graphics checks covering
  byte/run preservation, native boundaries, Korean strings and review evidence,
  exact listings, mixed figures, captions, rejected evidence drift, bitmap pixels,
  deferred-asset exclusion, title matching, relocation, and predecessor preservation.
  After recording the unapplied Johab alternative, all ten graphics checks passed
  again. A normal command-line rebuild reproduced both tracked records. Local
  documentation links, readiness JSON, private-output exclusions, and whitespace
  checks also pass.
- Updated PLAN-CD1/current guidance: **12b.3 complete; 12c is next**, to reconcile
  coverage and build the February issue handoff. All five indexed targets are
  prepared; 34 of 39 runtime TOC entries remain unmatched (four sections and
  30 other article candidates). Historical coverage records stay unchanged.
  This does not establish complete print coverage; physical comparison and
  independent backup/restore remain separately deferred.

## 2026-09-18 — CD1 step 12c: February issue handoff completed

- Added `make prepare-cd1-issue` and the private handoff at
  `build/cd1-issues/1988-02/`. All **48 runtime files / 1,291,810 bytes** remain
  identical to the validated five-article predecessor. Each article, preview,
  asset, and media record is also checked against its standalone package.
  All five article provenance documents are preserved in separate handoff evidence.
- Revalidated the original two-article coverage audit without rewriting it.
  Added a new current report accounting for **39 TOC entries, five indexed
  references, and 11 index occurrences**: five prepared articles, 30 unmatched
  article candidates, and four section entries where preparation is not applicable.
  Unindexed native content remains unattributed; no absence or print-completeness
  claim is inferred from an index gap.
- Reproduced the current TOC entry import from the checked source and identity
  registry and compared February with the historical snapshot. February's source
  text, identities, order, hierarchy, titles, and pages agree. Recorded the **39
  changed entry source IDs** caused by the expanded whole-document fingerprint;
  no runtime metadata changed. Unrelated pre-1988 scan-availability annotations
  are outside this February comparison.
- Incorporated `8802180`'s later native/body-title and page evidence into the new
  coverage record. The historical audit keeps its original ambiguous decision.
  No global title normalization or reference-page-suffix matching was introduced.
- Preserved four deferred WMFs and the pending CP949/Johab string question,
  including exact source references, problem IDs, and the unapplied alternative.
  Checked that deferred runtime IDs resolve to unresolved records and that the
  text-review target still contains the preserved characters. Cover availability,
  end pages, and physical verification remain unknown/pending as before.
- The unchanged v1 handoff contains five articles, ten sections, 582 blocks,
  2,518 paragraphs, 33 media records, 29 assets, 35 media occurrences, and ten
  previews. Catalog search remains metadata-only (`title`, `byline`, `issue_id`).
  Documented the configurable package base URL and manifest-based path lookup.
  This step recovered no new topics and converted or repaired no images.
- Validation: **156 tests passed**, including eight new handoff checks for TOC
  drift, complete population accounting, historical/new evidence separation,
  every runtime byte, all five provenance documents, missing/resolved review
  records, failed-staging preservation, and relocated static loading. All 48 files
  were fetched with exact hash checks under two nested HTTP base URLs. The eight
  handoff checks passed again after strengthening missing-text-review validation.
  A normal command-line rebuild reproduced both reviewed records. Documentation
  links, readiness JSON, private-output exclusions, and whitespace checks pass.
- Updated current guidance: **12c complete; 13a is next**, a CD1 metadata inventory
  to account for remaining references/issues and select the next bounded issue
  task. The first issue preparation checkpoint is complete; remaining CD1 coverage
  is still ahead. Physical comparison and independent recovery verification remain
  separate deferred tasks; CD2/CD3 and reading-room UI remain separately planned.

## 2026-09-18 — CD1 step 12d: February native coverage closed out

- Followed the owner's explicit request to focus on February 1988 before the
  previously queued step 13a. Reviewed every one of the **3,099 native/RTF topics**
  for native titles and issue-keyword metadata. Accounted for 1,088 dated article
  topics, ten titled navigation topics, and 2,001 untitled topics. Native and RTF
  article titles agree. Issue keywords and an independent opening date/page scan
  both identify **six February bodies**, bounded by January/March browse neighbors.
- Discovered **KEYBOARD LOCK**, page 162, omitted from all three indexes. Matched
  TOC `maso-1988-02-toc-0023` using exact title, explicit issue/page, native context
  `0x0e68416d`, exported alias `1KN6JI`, and linked introduction `3M4LMA`. Retained
  zero index occurrences. The five indexed references and 11 occurrences remain
  distinct from the six native/prepared articles; prior reports are unchanged.
- Added `make prepare-cd1-keyboard`: recovered topics 154/155 and all **53,683 source
  bytes, 303 paragraphs, 315 runs, and 95 blocks**. Preserved 37-paragraph BASIC and
  173-paragraph assembly listings without execution or correction, ten headings,
  six caption relationships, three image-backed tables, and one diagram. Five
  bitmap resources convert to PNG with identical decoded pixels. Table cells are
  explicitly unreconstructed; code whitespace and image-adjacent spaces survive.
- Added `make close-cd1-february` and the current private handoff at
  `build/cd1-issues/1988-02-native/`: **56 runtime files / 1,484,924 bytes**, six
  articles, twelve sections, 677 blocks, 2,821 paragraphs, 38 media records,
  34 assets, 40 media occurrences, and twelve previews. The approved v1 schema is
  unchanged. All earlier article/preview/asset bytes and media records survive;
  all six article provenance documents and the complete metadata inventory remain
  in private handoff evidence. The historical five-article handoff still reproduces.
- Current coverage accounts for **six prepared articles, 29 unmatched article
  candidates, and four section entries**. All observed native February bodies are
  prepared. Absence of mislabeled content elsewhere and printed completeness are
  not proven; scans or another source can address the remaining candidates.
  Eleven other-issue context/header-offset differences discovered during the scan
  are recorded for later review, without expanding into their extraction/repair.
- Preserved all four deferred WMFs, the existing CP949/Johab string question,
  missing cover/end pages, and pending physical comparison. Independent recovery
  remains deferred and non-blocking. No publication or UI work was performed.
- Validation: **167 tests passed**, including eleven new checks for native/index
  population accounting, rejected issue-keyword drift, complete byte/run/mark
  preservation, exact listings, table/caption structure, bitmap pixels, prior
  content preservation, relocation, and failed-staging recovery. All 56 runtime
  files were fetched and hash-checked under two nested HTTP base URLs. After
  strengthening the unchanged-issue-metadata guard, all five closeout checks passed
  again. Both normal build commands reproduced the reviewed records. Local
  documentation links, readiness JSON, private-output exclusions, and whitespace
  checks pass. Updated the plan, current handoff documentation, and owner task list;
  step 13a remains a separate future task.

## 2026-09-18 — Revised step 13 for the first complete CD1 extraction pass

- Applied the owner's approval to move from article-specific preparation toward
  a shared batch pipeline. Revised PLAN-CD1 around four checkpoints: **13a processing
  inventory → 13b shared extraction/packaging pipeline → 13c regression and sample
  validation → 13d resumable full-CD1 pass**. Step 13a remains the next implementation
  task; this change implements the plan revision, not the pipeline or batch run.
- Made native-topic accounting, unindexed articles, linked introductions, stable
  identities, and unresolved context relationships part of the processing queue.
  The existing 3,099-topic scan and six February preparations are reusable inputs;
  native article-topic and index-reference populations remain distinct.
- Specified reusable stages with source-bound exception data, complete byte/run
  preservation, explicit uncertain structures, deferred media, compatible cache
  reuse, staged package validation, interruption recovery, and per-job failure
  isolation. Issue packages will compose independent article outputs.
- Defined the expansion check: preserve all six February articles and validate a
  fixed sample of 6–10 candidates across at least three other issues. Full-disc
  processing starts after fidelity and batch-operation checks pass. Source-specific
  exceptions can remain recorded; general preservation defects require correction.
- Defined full-pass completion as accounting for every candidate's outcome, with
  validated successful packages and explicit failed/blocked cases. Issue boundaries
  serve as resume/reporting points within the pass. Missing scans, physical review,
  independent backup, deferred repairs, access/publication, CD2/CD3, and UI work
  retain their separate scopes.
- Updated README, current coverage/handoff/preservation guidance, the offline task
  list, and readiness next-scope text. Historical extraction records and outputs
  remain unchanged; the owner's existing PRD-reading-room edits are left untouched.
- Validation: local documentation links, the new milestone anchor, unique checkpoint
  headings, readiness JSON, and whitespace checks pass. Only `allowed_next_scope`
  changed in the readiness record. No runtime code changed, so extraction tests
  were not rerun.

## 2026-09-20 — CD1 step 13a: processing inventory completed

- Added `make inventory-cd1-processing`, the private metadata artifacts under
  `build/cd1-processing-inventory/`, and a tracked inventory record. Reused the
  February native scan, checked original MVB/RTF hashes, reproduced all three
  index imports/grouping and current TOC entries, and verified February's runtime
  files and source-topic evidence. No new article text or media was prepared.
- Accounted for **3,099 topics, 2,103 contexts, 3,032 index entries, 1,080 distinct
  index targets, 2,462 reference occurrences, and 5,497 TOC entries**. All index
  targets resolve to native/exported aliases: 1,079 dated bodies and one navigation
  topic. All 41 suffixed references remain distinct. Nine dated candidates are
  unindexed, including already-prepared KEYBOARD LOCK; no numeric reference was
  invented from a page label.
- Built **1,088 article-candidate jobs across 72 months**: six already prepared,
  **1,074 ready for runner validation**, and **eight blocked on ownership**. Ready
  is a metadata state, not a claim of successful extraction or complete boundaries.
  The eight blockers preserve three substantial unaliased topics following bodies
  and five possible introductions without the expected direct link. Their content
  is not discarded or merged solely from adjacency.
- Classified the other sources as 883 linked introduction candidates, 993
  formatting-only separators, 114 linked auxiliary topics, three application
  resource topics, and ten navigation topics. Retained all aliases, incoming and
  outgoing links, native locations, and RTF spans/hashes. All 31 context/header
  differences (eleven dated bodies) lie inside the corresponding ordered native
  topic intervals; association evidence is recorded without treating those offsets
  as article-header addresses. Actual recovery boundaries remain a runner check.
- Preserved the six prepared identities, TOC links, exact source spans, extraction
  status, and pending physical comparison. Conservative new TOC matching requires
  exact titles, explicit issues, and observed pages: 66 entries matched, 185 need
  review, 2,780 have no exact-title match, 1,909 are outside observed CD1 months,
  and 557 are sections. Unmatched TOC metadata does not block body preparation.
- Froze a **nine-candidate validation sample spanning 1988–1993**, including
  unindexed/suffixed references, additional fonts, long code-bearing topics,
  bitmap/vector variety, interior context offsets, and a supplement without a
  numeric page label. Selection uses lexical hints only; complete RTF/semantic
  inspection is still required in the shared pipeline.
- Documented the versioned batch input contract and added a standalone inventory
  reader. It checks hashes, unique ownership, complete source populations, job
  states, context intervals, links, and TOC/job relationships after relocation.
  Staging validates before replacement; failed validation preserves the previous
  inventory. Normal builds must reproduce the reviewed record.
- Updated PLAN-CD1 and current guidance: **13a complete; 13b, the shared extraction
  and packaging runner, is next**. Full-disc processing follows 13c validation.
  Historical extraction records and packages remain unchanged; physical review,
  deferred repairs, backup/restore, CD2/CD3, access/publication, and UI remain
  separate. The owner's PRD-reading-room edits remain untouched.
- Validation: **179 tests passed**, including twelve new inventory checks covering
  complete populations, unindexed/suffixed identities, context bounds, explicit
  page matching, retained ownership blockers, February evidence, fixed sample,
  rejection of missing/duplicate/falsely-ready jobs, relocation, and failed staging.
  The initial restricted run blocked two localhost HTTP tests and changed Inkscape
  diagnostics used by a historical reproducibility assertion; an authorized
  unrestricted `make check` passed the full suite without source/record changes.
  Normal inventory rebuild and standalone verification pass, as do documentation
  links, metadata totals, private-output exclusions, readiness JSON, and whitespace.

### 2026-09-20 — Step 13b: shared CD1 batch runner and February regression

- Implemented one article/issue/whole-disc runner with seven recorded stages:
  association, RTF inventory, recovery, semantic mapping, media, Markdown, and
  package assembly. `make batch-cd1 BATCH_ARGS="--issue 1988-02"` prepares the
  February baseline; article selectors accept source references and stable IDs.
  Actual-source work in this checkpoint covered only February's six articles.
- Rechecked queue inputs and original MVB/RTF/probe hashes; preserved raw selected
  topic evidence and native/context/TOC links. Added scoped inherited formatting
  snapshots across RTF pages, including group restoration and opaque binary data.
  Unsupported inherited/visible controls, unknown codecs, undecoded spans and
  unresolved external content ownership cannot silently become successful text.
- Exported **168 source-bound exceptional block decisions** from the six reviewed
  maps into metadata-only profiles. Ordinary paragraph/spacing blocks use shared
  rules; font policies preserve February's different Fixedsys requirements.
  Recovery reads the original RTF again, retaining byte accounting, paragraphs,
  runs, formatting, objects and source spans. Unreviewed generic semantics remain
  explicit; broader font/structure evidence belongs to the frozen 13c sample.
- Added immutable stage generations, staged validation, atomic successful-output
  publication, compatible-cache checks, corruption quarantine, retained failure
  evidence, and per-article failure isolation. Fingerprints include source/config,
  upstream output hashes, schema/profile/code, runtime/converter versions and
  installed font-file hashes. Media checkpoints are shared; reviewed derivatives
  and known deferred cases are reused without retrying broken WMFs.
- Composed the February issue from independent article packages. **All six article
  JSON documents and all twelve Markdown previews match the baseline byte for
  byte; media records and accepted assets are unchanged.** The resulting v1
  package contains **56 runtime files, 6 articles, 12 sections, 677 blocks, 2,821
  paragraphs, 38 media records, 34 available assets, and 40 occurrences**. Four
  WMFs remain deferred. Existing coverage, the graphics decoding ambiguity, and
  Gary Kildall bibliographic context remain in private provenance. Combined
  catalog/media/manifest ordering reflects independent composition; source order
  and historical artifacts remain unchanged.
- Recorded the validated output in `data/catalog/batch-runs/cd1-february.json`.
  A second full February run verified and reused **all 83 stage calls** from cache.
  All 58 recorded issue-stage files (runtime, provenance and checkpoint) pass
  checksum verification. Publisher text/media/intermediates remain ignored under
  private/build paths; only tools, tests, metadata and documentation are tracked.
- Added **15 tests**, including actual-source interruption after one recovered
  topic, retained partial evidence, successful resume, isolated decoder failure
  followed by a successful article, independent issue composition, exact baseline
  regression, source-bound decision drift, unknown fonts/controls, binary/group
  inheritance, stale/corrupt caches, failed staging and symlink rejection.
  **194 tests passed** in the unrestricted full suite. The restricted attempt hit
  the previously observed two localhost socket restrictions and one historical
  Inkscape-diagnostics mismatch; unrestricted verification passed without changing
  historical records. The final runner-specific suite also passes (15 tests), as
  do profile reproduction, documentation links, private-output exclusions and
  `git diff --check`.
- Updated PLAN-CD1, current guidance and readiness metadata: **13b complete;
  13c is next**, using the already frozen nine candidates beyond February. Full
  CD1 extraction follows that checkpoint. Physical comparison, missing scans,
  deferred image repair, independent backup/restore, access/publication, CD2/CD3
  and reading-room UI remain separate. The owner's concurrent changes to
  `PRD-reading-room.md` were left untouched and excluded from this commit.

### 2026-09-20 — Step 13c: frozen sample, preservation audit and batch validation

- Ran the nine candidates frozen in 13a, together with all six February regression
  articles. The first sample-only attempt prepared **three of nine**; six stopped
  explicitly on missing font policies, an unsupported `fi` control, or auxiliary
  topic ownership. Its report remains in `build/cd1-sample-initial/`. The first
  expanded attempt prepared **14 of 15** and exposed an automatic heading rule
  assigning level two without a level-one parent. Retained that attempt report,
  fixed the shared rule, and added a regression test; no missing heading was
  invented to force the package to validate.
- Added source-bound shared policy: CP949 for inspected Fixedsys runs (including
  Korean comments), with February's reviewed policies preserved. Additional font
  26 in `9105358` and font 95 in `9304310` contain only spaces; their ASCII policies
  are bound to exact article-topic hashes. Unknown fonts still fail with encoded
  source evidence. Preserved first-line indentation, tab-stop positions, double
  underline, resets and inherited state in structured RTF recovery.
- Added conservative common structure rules for explicit titles/bylines, supported
  numbered headings, and contiguous Fixedsys passages. Preformatted candidates
  retain code whitespace, internal blank paragraphs and tabs; language and
  code/table/terminal interpretation remain unverified. Unclassified paragraphs
  and missing-parent heading cases remain explicit. No per-article preparation
  scripts or runtime schema changes were introduced.
- Inspected links to **two author biographies and one series navigation topic**.
  Recovered their **21 paragraphs** separately with raw RTF, source/run accounting,
  source links and dispositions. Verified all eight auxiliary media references;
  their rendering remains deferred. These topics are not merged into the article
  body or followed recursively into other articles. Other unreviewed linked
  content still requires an ownership decision.
- **All 15 articles now prepare across ten issues:** **8,110 paragraphs, 2,388
  blocks, 213 media occurrences and 200 distinct media records**. Nine new articles
  contribute 5,289 paragraphs. Preserved the unindexed native identity/source
  alias, both suffixed identities, interior context offsets and the supplement's
  null page number. February's article JSON/Markdown bytes, media records and
  accepted assets remain unchanged; its historical artifacts/13b record survive.
- Independently reconstructed **7,431 text runs from 992,844 original RTF bytes**,
  checking codec round trips and encoded hashes, complete contiguous topic byte
  accounting, paragraph projections, boundaries and identities. Audited auxiliary
  recovery separately. All **95 available bitmap resources** match decoded source
  pixels. Of the 200 article media records, **168 are available and 32 deferred**:
  February's four existing exceptions plus 28 math-library vectors whose Symbol
  font/glyphs are suspect after conversion. Kept diagnostics and source positions;
  no broken-image repair was attempted.
- Added `make validate-cd1-batch`. A fresh run in an empty temporary root reproduced
  **every recorded stage output hash**, including conversion diagnostics and
  preservation intermediates. Compatible resume reused **all 328 stage calls**.
  All **524 HTTP file fetches** beneath `/archive/cd1/sample/` and
  `/reader/data/magazines/cd1/` matched the composed package files. This verifies
  the current sample's source preparation and static loading, not print fidelity
  or universal support for all remaining disc constructs.
- Recorded the frozen selection, per-article/topic counts, source hashes, media
  dispositions/diagnostics, issue package locations and validation results in
  `data/catalog/batch-runs/cd1-validation-sample.json`. Full text, images, source
  spans and auxiliary recovery remain private under `build/`; tracked material
  contains tools, tests, policy/validation metadata and documentation.
- **202 tests pass**, including eight new checks covering formatting/reset rules,
  fixed-pitch preservation, heading-parent constraints, independent run-byte
  reconstruction, ledger gaps, frozen identities, auxiliary accounting and all
  retained issue/media artifacts. Existing actual-source interruption/resume,
  failure isolation and February regressions pass. The finite validation command,
  full suite, tracked/private report comparison, local documentation links and
  whitespace checks all pass. Validation ran with the converter and localhost
  access required by these checks.
- Updated PLAN-CD1 and current guidance: **13c complete; 13d, the first full CD1
  pass, is next**. Every remaining candidate will receive a prepared, blocked or
  failed outcome with evidence. Semantic/physical review, missing scans, deferred
  image repair, independent backup/restore, access/publication, CD2/CD3 and UI remain
  separate. The owner's concurrent `PRD-reading-room.md` edits remain untouched
  and are excluded from this commit.

### 2026-09-20 — Step 13d started: durable full-queue execution

- Started all 1,088 candidates across 72 issues using the exact extraction identity
  validated in 13c. The new outer driver records its own code hash separately,
  checks the sample gate, and leaves compatible extraction/media caches reusable.
- Added durable per-job outcomes, source evidence, successful-stage references,
  copied failure-stage evidence, retry arguments, progress totals, and issue
  checkpoints. Resume verifies completed records and keeps original first-pass
  failures rather than automatically retrying them. Issues without successful
  articles can receive valid metadata-only TOC packages.
- The execution process is live; final counts, full source/TOC/media reconciliation,
  all-package verification and the final commit remain pending. Original media,
  historical records and the owner's PRD edits are unchanged. No content is
  published and no broken images are repaired.
- Added the coverage/report builder and targeted tests for explicit unavailable
  states, omission/duplication rejection, TOC-link consistency, retained failure
  evidence and metadata-only issue packages. Seven targeted checks pass; the
  full-pass artifact test waits for the completed run. Full-suite validation and
  the requirement-by-requirement completion audit follow execution.

### 2026-09-20 — Step 13d completed: first complete CD1 pass and reconciliation

- Executed the complete frozen queue, issue by issue, using the unchanged 13c
  extraction identity: **1,088 candidates in 72 issues**. Outcomes are **four
  prepared**, **533 prepared with review exceptions**, **543 failed**, and **eight
  blocked**. No candidate is silently unattempted, and failed/blocked cases are
  never counted as extracted. All 15 prior sample articles reuse compatible stages.
- Validated **537 standalone article packages and all 72 combined issue packages**,
  including exact article populations and unchanged standalone content. The
  packages contain **179,356 paragraphs and 96,399 blocks**. Independently checked
  **30,038,307 original RTF bytes and 167,611 text runs** across 915 article topics;
  audited the three recovered auxiliary topics separately.
- Reconciled **3,099 native topics, 2,103 contexts, 1,080 index references, 2,462
  index occurrences, 3,032 index rows and all 5,497 TOC entries**. Of 66 confirmed
  TOC metadata matches, 51 now link to prepared articles and 15 remain unavailable.
  Another 486 prepared articles retain source identities without guessed TOC
  links. Seven of nine unindexed candidates prepare; two fail. All eight
  unattributed topics retain source evidence and explicit unresolved ownership.
- Verified every one of **6,165 referenced source media resources**. Runtime
  disposition is **2,174 available, 393 deferred and 3,598 not packaged**. All
  **1,479 available bitmap derivatives** preserve decoded source pixels. Retained
  vector diagnostics and original resources without attempting image repair.
- Retained source-job records for all candidates and **2,168 copied failure
  evidence files** for all 543 failures. The consolidated retry queue includes
  all 551 failed/blocked candidates. Failure classes are 470 unreviewed linked
  content, 45 font/decoding policies, 20 unsupported RTF constructs, six inherited
  formatting cases, one unterminated paragraph and the final article's unmatched
  closing brace. Eight queue blockers concern source-topic ownership.
- Completed a real full resume: all 1,088 outcomes and 72 issue checkpoints
  reproduce the original 4,416-output execution manifest byte for byte, SHA-256
  `1c2cca1566ebaefd952eac7a878c148bf65e796ff60942ffd01429a15ec23907`.
  Known failures remain stable first-pass outcomes rather than being retried by
  resume. Earlier preparation records, original sources and schema v1 remain intact.
- Added `make run-cd1-full-pass`, `make report-cd1-full-pass`, the tracked
  `data/catalog/batch-runs/cd1-full-pass.json` summary and 11 private coverage
  tables. Reporting validates every source/package/evidence population and
  compares newly generated coverage bytes with cached output. Tools and metadata
  are tracked; article text, images, previews and detailed recovery stay private.
- Repeated the complete source/package/media audit independently. Both runs
  produced identical counts, issue records and byte hashes for all 11 coverage
  tables. The final reporter identity and every coverage output hash verify;
  the execution manifest remains unchanged. The second audit includes the
  strengthened freshly-generated-versus-cached coverage check.
- **211 tests pass**, including nine first-pass checks and the existing actual-source
  interruption/resume, failure containment, February regression and static loading
  tests. Local documentation links, metadata JSON and whitespace checks pass.
- Updated PLAN-CD1, README, preservation readiness and current checkpoint guidance:
  **13a–13d are complete**. Subsequent bounded work should begin with linked-content
  ownership and explicit TOC review; recorded first-pass failures remain history.
  This does not establish complete printed coverage. Physical comparison, scans,
  deferred image repair, independent backup/restore, access/publication, CD2/CD3
  and reading-room UI remain separate. The owner's PRD edits are unchanged and
  excluded from the commit.

### 2026-09-20 — Step 14a started: linked auxiliary recovery and bounded retry validation

- Audited all 470 first-pass linked-content failures: their 587 blocking links
  target exactly 111 unowned auxiliary topics, including 31 leaf topics and 80
  topics with outgoing links. All 308 outgoing links remain source references.
- Added a separate auxiliary audit/policy and an extension of the existing runner
  with its own identity and output root. Original root-level pipeline code, shared
  policy and first-pass packages remain unchanged. Two unsupported auxiliary
  formatting cases retain raw RTF and state evidence.
- Fixed the six-article sample before execution: `9308449`, `9103252`, `9010234`,
  `9201335`, `9008224`, and `9004200`. These cover leaf, series, mixed, shared and
  both deferred auxiliary cases. PLAN-CD1 now distinguishes this validation step
  from 14b's remaining 464 retries and combined availability reconciliation.

### 2026-09-20 — Step 14a completed: auxiliary policy and six successful retries

- Accounted for every one of the 470 association failures, 587 blocking links and
  111 auxiliary destinations. The source-bound policy requires an unowned,
  undated auxiliary with a resolved native context, an alias and consistent
  incoming links. Other/ambiguous destinations remain blocked. Auxiliary links
  stay separate from article bodies; no recursive article import is performed.
- Recovered **109 auxiliary topics**, comprising **774 paragraphs, 85,274 source
  RTF bytes and 1,176 text runs**, with independent byte accounting and codec
  round-trip verification. Topics 18 and 19 remain deferred with exact raw RTF,
  native metadata and inherited-formatting state. Preserved all 308 outgoing links
  and verified 28 distinct media resources in recovered auxiliaries; their
  rendering remains deferred.
- All **six fixed article retries prepare with review exceptions**: **791
  paragraphs, 284 blocks, 128,520 audited RTF bytes and 718 text runs** across ten
  article topics. Auxiliary paragraphs are not merged into article bodies, and
  auxiliary recovery matches the separate audit, including both deferred cases.
  All ten available bitmap resources preserve original decoded pixels.
- Validated six standalone and six partial sample issue packages. These add six
  prepared articles beyond the historical 537. Sample issue packages do not
  replace the complete first-pass handoffs. First-pass outcomes and all original
  sources remain unchanged; article/auxiliary semantic and physical review remain
  pending. No publisher content is committed or published, and no media is repaired.
- Added `make review-cd1-associations` and `make retry-cd1-association-sample`, with
  separate tracked audit/sample summaries and private source/package/checkpoint
  artifacts. Both normal commands reproduce their records exactly. The extension
  fingerprints its reviewed policy, implementation and checkpoint helper, and
  refuses output inside the original first-pass root. A fresh dependency-identified
  rebuild reproduces **all 57 article runtime files** byte for byte; final resume
  and the six focused regression/artifact checks pass.
- **217 full-suite tests pass**, covering existing source/package/HTTP regressions
  and six new ownership, source-integrity, deferred-recovery, output-isolation and
  actual-artifact checks. Documentation links, JSON metadata, original pipeline
  preservation and whitespace checks also pass.
- PLAN-CD1 now records **14a complete; 14b next**: retry the remaining 464 members
  of this exception class, retain any newly exposed decoder/formatting failures,
  carry the six sample results forward, and reconcile combined packages/current
  availability without rewriting 13d history. Other exception classes and TOC
  review remain separate bounded work. The owner's `PRD-reading-room.md` changes
  and new `PRD-local-web.md` remain outside this commit.
