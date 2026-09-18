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
