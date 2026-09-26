# CD2 extraction and private reference plan

Revised 2026-09-26. Status: **implemented**. The private complete pass and its
coverage report are described in [the CD2 reference guide](docs/CD2-READABLE-REFERENCE.md).
This is the source-specific work sequence used for `masocd-2.iso`.
CD1's usable reference and the 1983-11–1993-12 reading room are complete. See
[PLAN-CD1.md](PLAN-CD1.md), the [CD1 reference guide](docs/CD1-READABLE-REFERENCE.md),
and the [reading-room plan](PLAN-reading-room.md) for the results to build on.

## Goal and boundaries

Recover CD2's available article text, code, images, and source relationships into
a **private, reproducible, human-readable reference** for paper/OCR restoration.
The paper magazines are authoritative; CD text is a secondary transcription.
Preserve source bytes and uncertainty so paper-supported corrections can later be
recorded separately. A readable article with localized uncertainty is useful;
unresolved characters, article boundaries, and media must remain visible.

The broader archive target is **1983-11–1995-12 (146 monthly issues)**. CD2 paths
suggest 1994 material, but its actual issue and article coverage is unverified.
The supplied library TOC covers **122 issues through 1993-12**. Do not manufacture
1994 TOC entries, pages, authors, covers, or CD-to-TOC matches from filenames or
titles alone. CD-native issue/article navigation can stand on its own until
independent issue metadata is available.

The [reading-room PRD](PRD-reading-room.md) and current implementation target
**1983-11–1993-12**. This plan prepares CD2 data offline; adding 1994 to the SPA
requires a separate product-scope decision and a versioned adapter/input update.
Do not silently extend the current catalog or make SPA integration an extraction
acceptance gate. Keep original media, recovered bodies, and generated references
private. Publication and access policy remain separate decisions.

## Starting evidence and CD1 lessons

The [source inventory](docs/SOURCE-INVENTORY.md) records the supplied CD2 ISO as
197,738,496 bytes with SHA-256
`fc7b3047b2c6cc2555500faf43dc0b73ff877c2f5b01acdb32041615d2f31a0e`.
Initial inspection found `DATA/MASO2.M12` (125,394,639 bytes),
`BIN/MASO2.EXE`, `BIN/MASO2.INI`, `MV*12.DLL` libraries, and `DATA/SOURCE/`
and `DATA/LIST/` names suggesting 1994. Article-body decoding, native index
relationships, completeness, and viewer behavior have not been established.
The owner specifies Windows 95 for this disc. CD1's container/decoder behavior
is a useful hypothesis to test, not an assumed CD2 format guarantee.

CD1 delivered a portable private HTML reference with **1,080 text exports across
72 issues**, **3,125 listing downloads**, **4,979 viewable images**, **1,111
deferred images**, and eight explicitly blocked article-boundary cases. Its
historical strict v1 packages covered 995 articles; the final reference recovered
readable text from all 85 previously failed candidates, with localized markers in
33 articles. Reuse the successful source accounting, text/code/media handling,
reference exporter, and validation patterns where they fit CD2. The
[v1 content contract](docs/READING-ROOM-CONTENT-V1.md) remains a source of identity,
ordering, literal-text, and unavailable-media principles, not a prerequisite that
forces CD2 into CD1's strict RTF/font policies. Document any CD2-specific data
shape before building a consumer.

Prioritize complete readable text, code characters and whitespace, meaningful
emphasis, paragraph/section structure, captions, image placement, source
identities, and explicit gaps. Exact fonts, margins, alignment, and original-viewer
appearance are not acceptance gates. A viewer check may help settle a concrete
format ambiguity; it is not required for each article or for the final reference.
Do not guess uncertain bytes or code, discard unparsed source material, or mark
CD-derived text as paper-verified.

## Bounded work sequence

Work through these checkpoints in order, refining later checkpoints from the
evidence in the first. Record each candidate's outcome so the queue has a clear
stopping point. A failure in one article or image must not hide usable text in
another. Use the original ISO and preserve a checksummed source trail; lack of an
independent backup does not block read-only local extraction.

### 1. Source map and one candidate

**Input:** `masocd-2.iso`, its recorded hash, extracted tree, and initial source
inventory.

**Deliverable:** a reproducible CD2 file/container/index/media inventory and one
source-bound candidate for a text/code/image probe. Record native identifiers,
evidence for issue/title attribution, candidate article boundaries, viewer entry
point, and known unknowns. Distinguish articles from source-code attachments,
navigation records, and other disc content. Test whether CD1's decoder and
reference stages apply before reusing them.

**Check:** the ISO hash and inventories reproduce; every proposed issue/date or
article relationship points to inspected source evidence. If no article can yet
be identified, document the precise index/container question and make resolving
that question the next bounded task. Do not start a bulk extraction here.

### 2. One readable article

**Input:** the selected candidate and its recorded source locations.

**Deliverable:** private text and ordered blocks with source references, code
downloads where appropriate, image/attachment links, and explicit unavailable or
uncertain parts. Preserve original files. Use the simplest CD2-specific decoding
and export path that keeps text and whitespace honest; adapt CD1 code only where
compatibility is demonstrated.

**Check:** source bytes and extracted segments are accounted for, Korean text and
code render readably, paragraph and code spacing survive export, media positions
and links resolve or are marked unavailable, and a repeated build produces the
same files. Compare with the CD2 viewer only if a specific ambiguity requires it.
Print agreement remains unverified until paper evidence is reviewed.

### 3. One issue and a second case

**Input:** the proven article path and CD2's inspected index/issue records.

**Deliverable:** one browsable private issue slice and a second article chosen to
exercise a different source structure or failure mode. Show a CD-native article
list separately from any supplied library TOC. Record unmatched and blocked
items, missing metadata, and deferred media rather than filling gaps by inference.

**Check:** both cases build and validate independently; issue navigation, text,
listing downloads, image links, and unavailable states work in a local browser;
rebuilds agree. Revise the CD2 format notes and bulk-processing queue from the
observed exceptions.

### 4. Complete CD2 reference pass

**Input:** a reproducible candidate inventory and the tested extraction/export
path.

**Deliverable:** a portable private CD2 HTML/text/code/image reference and a
coverage report accounting for every discovered article candidate and associated
media resource.
Process by issue in resumable batches, retaining per-candidate success, partial,
failed, and blocked outcomes. Preserve raw evidence and prior review decisions;
keep localized uncertainty instead of discarding an otherwise usable article.

**Check:** all inventoried candidates have explicit outcomes; article and issue
links resolve or carry visible unavailable states; text, code whitespace,
downloads, and media are checked against exported records; a full rebuild agrees;
and representative Korean/code/image pages work in a browser. Report remaining
gaps and paper-review status without treating zero exceptions as the finish line.
Stop when the usable private reference and honest coverage report are delivered.

## Handoff and task records

Keep CD2-native identities and provenance distinct from CD1, even where a title
or asset resembles an existing record. If later requested, expose CD2 through a
versioned static reading-room adapter with explicit 1994 issue metadata and
compatibility checks; the SPA needs no runtime extraction, server, or database.
Do not alter the completed CD1 export or historical strict packages to accommodate
CD2. Paper/OCR comparison, verified corrections, and any public release remain
separate follow-up work.

For each implemented checkpoint, record the input, deliverable, validation,
limitations, and next task in [PROGRESS.md](PROGRESS.md); inspect the staged diff
and commit the scoped source/metadata changes. Keep ISO files and recovered
article bodies/assets out of Git. A request to continue CD1 or maintain the
existing reading room does not activate this CD2 queue.
