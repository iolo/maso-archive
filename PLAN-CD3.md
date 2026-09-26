# CD3 extraction and private reference plan

Revised 2026-09-26. Status: **implemented**. The private complete pass and its
coverage report are described in [the CD3 reference guide](docs/CD3-READABLE-REFERENCE.md).
This is the source-specific work sequence used for the owner's official
`masocd-3.iso`. CD1 and CD2 already have usable private
references; see [PLAN-CD1.md](PLAN-CD1.md), [PLAN-CD2.md](PLAN-CD2.md), and their
[CD1](docs/CD1-READABLE-REFERENCE.md) and
[CD2](docs/CD2-READABLE-REFERENCE.md) reference guides for the implemented paths.

## Goal and boundaries

Recover CD3's available article text, code, images, and source relationships into
a **private, reproducible, human-readable reference** for paper/OCR restoration.
The paper magazines are authoritative; CD text is a secondary transcription.
Preserve source bytes, native identities, and uncertainty so later paper-supported
corrections remain distinguishable from the CD extraction. A readable article
with localized gaps is useful; unresolved boundaries and media stay visible.

The broader archive target is **1983-11–1995-12 (146 monthly issues)**. CD3 paths
suggest 1995 material, but its actual issue/article coverage and completeness
are unverified. The supplied library TOC covers **122 issues through 1993-12**.
Do not manufacture 1995 TOC entries, authors, pages, covers, or CD-to-TOC matches
from filenames, titles, or timestamps. CD-native navigation can stand on its own
until independent issue metadata is available.

The [reading-room PRD](PRD-reading-room.md) and implemented SPA cover
**1983-11–1993-12**. This plan prepares CD3 data offline. Adding 1995 to the SPA
requires a separate product-scope decision and a versioned static adapter/input
update; SPA integration is not an extraction acceptance gate. Keep the ISO,
recovered bodies, media, and generated reference private. Publication and access
policy remain separate decisions.

## Starting evidence and lessons from CD1 and CD2

The [source inventory](docs/SOURCE-INVENTORY.md) records `masocd-3.iso` as
327,081,984 bytes with SHA-256
`7c269df8479c72919863f27b68dceb6fe8b567a18f27eb9481655e15e4ae17d0`.
Initial inspection found `MASO3.M14` (299,619,070 bytes), `LIST.M14` (10,067
bytes), `MASO3.EXE`, `MASO3.CNT`, `MV*14N.DLL` viewer libraries, and 105 `.CAB`
files. `FILES/9501` through `FILES/9512` suggest 1995 attachments, not verified
magazine issues or article bodies. At planning time the main M14 had not been
decoded; both containers now have checked HELPDECO probes. The owner
reports that CD3 setup installs no software: it only creates a shortcut to the
viewer on the CD. Windows 95 was the intended viewer environment, not an
extraction prerequisite. The ISO and file timestamps conflict and do not
establish publication dates.

The inspected containers share an initial signature, and CD2's M12 accepted the
pinned HELPDECO decoder used for CD1. Test M14 compatibility and the role of
`LIST.M14` separately; neither a shared signature nor an executable family
proves the same indexes, topic boundaries, encoding, or media behavior. Record
the decoder version and command if one works. Preserve an undecoded source path
and a precise format question if it does not.

CD1's completed reference shows why useful text/code/image exports and explicit
blockers matter more than cosmetic RTF fidelity. CD2's completed pass shows the
need to inventory index and unindexed topics separately, retain conflicting
titles and unresolved fields, account for ordered and unassigned media, and let
missing attachments or previews coexist with a readable body. Reuse their
checksummed inventories, source accounting, resumable batches, portable exporter,
and validation patterns only where CD3 evidence supports them. The
[v1 content contract](docs/READING-ROOM-CONTENT-V1.md) supplies identity,
ordering, literal-text, and unavailable-media principles; it does not require
CD3 to satisfy CD1's strict RTF/font package policy or CD2's data shape.

Prioritize complete readable text, code characters and whitespace, meaningful
emphasis, paragraph/section structure, captions, image placement, source
identities, and explicit gaps. Exact fonts, margins, alignment, and original-viewer
appearance are not acceptance gates. Use a viewer check when it can resolve a
specific source ambiguity; it is not required for every article. Do not guess
uncertain bytes, discard unparsed content, or mark CD text as paper-verified.

## Bounded work sequence and outcome

The checkpoints below were completed in order, refining later work from the
source evidence. The result is a private reference for all 968 discovered CD3
article candidates, with 792 success and 176 partial outcomes, plus explicit
auxiliary-topic and media accounting. See [the source map](docs/CD3-SOURCE-MAP.md)
for format evidence. A failure in one article or image did not hide usable text
in another. The checksummed source trail did not require an independent backup
to perform read-only local extraction.

### 1. Source map and one candidate — done

**Input:** the original `masocd-3.iso`, recorded hash, and source inventory.

**Deliverable:** a reproducible ISO/extracted-file inventory and a bounded
container/index/media map for both M14 files and relevant CAB contents. Identify
the viewer entry point, native navigation or article identifiers, candidate
boundaries, and evidence for any issue/title attribution. Distinguish article
content from downloadable attachments, code listings, navigation records, and
other disc resources. Select one source-bound candidate for a text/code/image
probe. Test CD1/CD2 decoder compatibility before adapting their tools.

**Check:** source hashes and inventories reproduce; each proposed relationship
points to inspected bytes or records. Record unsupported decoder output and
unmapped files explicitly. If no article can be identified, document the exact
index/container question and make resolving it the next bounded task. Do not
start bulk extraction here.

### 2. One readable article — done

**Input:** the selected candidate and its recorded source locations.

**Deliverable:** a private portable article with UTF-8 text, ordered blocks and
source references, separate code/listing downloads where appropriate, original
and viewable media where possible, attachment links, and explicit unknown or
unavailable parts. Keep original files byte-for-byte. Implement the smallest
CD3-specific decoding/export path that preserves text and whitespace honestly.

**Check:** account for the selected source span and extracted segments; verify
Korean text, code spacing, media order, link targets or unavailable states, and
repeatable output hashes. If source records leave a concrete boundary or
rendering ambiguity, compare with the original disc viewer. Print agreement
remains unverified until paper review.

### 3. One native group and a second case — done

**Input:** the proven article path and inspected CD-native navigation records.

**Deliverable:** one browsable private native group or issue slice plus a second
article chosen to exercise a different structure or failure mode. Show its
CD-native list without implying a match to the missing 1995 library TOC. Record
unindexed content, title conflicts, unmatched attachments, unassigned media,
blocked boundaries, and missing metadata as applicable. Revise the candidate
queue and format notes from these cases.

**Check:** both cases build and validate independently; local navigation, text,
listing downloads, media links, and unavailable states work in a browser; a
rebuild agrees. The candidate inventory states what remains outside the group.

### 4. Complete CD3 reference pass — done

**Input:** a reproducible inventory of discovered article candidates and other
content, plus the tested extraction/export path.

**Deliverable:** a portable private CD3 HTML/text/code/image reference and a
coverage report accounting for every discovered candidate, associated media,
attachments, and non-article topics. Process by CD-native group in resumable
batches. Retain per-candidate success, partial, failed, and blocked outcomes,
source evidence, and review decisions. Keep localized uncertainty instead of
discarding otherwise usable articles. Do not infer printed-issue completeness
from a complete CD candidate queue.

**Check:** every inventoried item has an explicit outcome or classification;
article/group links resolve or show unavailable states; text, code whitespace,
downloads, and media agree with exported records; full rebuilds reproduce the
output; and representative Korean, code, image, and exception pages work in a
browser. Report remaining gaps and paper-review status. Stop when the usable
private reference and honest coverage report are delivered, even if exceptions
remain.

## Handoff and task records

Keep CD3-native identities and provenance distinct from CD1/CD2, even where
titles or assets resemble earlier records. If later requested, expose CD3 through
a versioned static reading-room adapter with supported 1995 issue metadata and
compatibility checks. Do not alter the completed CD1/CD2 references or historical
strict packages to accommodate CD3. Paper/OCR comparison, verified corrections,
and any public release are separate follow-up work.

The implemented checkpoint records in [PROGRESS.md](PROGRESS.md) retain their
inputs, deliverables, validation, limits, and handoffs. Keep the ISO and
recovered article bodies/assets out of Git. A request to continue CD1/CD2 or
maintain the existing reading room does not reopen the CD3 extraction queue.
