# CD2 private readable reference

The private output is `build/cd2-reference/index.html`. It is a portable static
HTML/text/code/image reference built from the supplied CD2 ISO, extracted tree,
and the checksummed M12 decoder probe. All recovered bodies and media remain
under ignored `build/` and `private/` paths. The tracked metadata record is
`data/catalog/preservation/cd2-readable-reference.json`; it contains hashes and
counts, not article text.

## Reproduce and check

1. Prepare the private M12 decoder probe as described in
   [the source map](CD2-SOURCE-MAP.md). The pinned HELPDECO revision and command
   are recorded there.
2. Run `make inventory-cd2-sources` and `make map-cd2-candidates` to verify the
   ISO, extracted files, decoded resources, and native candidate queue.
3. Run `make build-cd2-reference`. Each CD-native group is an independent
   resumable batch. Use `make build-cd2-reference CD2_ARGS=--resume` to verify
   and reuse completed groups, or `CD2_ARGS=--verify-existing` to rebuild all
   groups and require byte-identical manifests.
4. Run `make check-cd2-reference`. It checks source and output hashes, all
   1,330 candidate identities and outcomes, article/media relationships, code
   listing bytes and whitespace, attachments, 58 supplemental topics, and every
   generated HTML link. The reviewed check covers 10,792 output files.

The reference is about 856 MiB on disk. It can be served by any local static
server; the pages use relative links and need no runtime extraction, database,
or application server. For local browsing, run
`python3 -m http.server 4178 --directory build/cd2-reference`. The completed source references remain separate; the
[reading room](READING-ROOM.md) now aggregates all three discs for browsing and search.

## Coverage

The CD-native indexes map 1,326 distinct references to unique RTF topics.
Four additional titled RTF topics lack index rows and remain separate article
candidates. The 12 provisional CD-native groups contain all 1,330 candidates.
Each has a readable article page, source-backed blocks, UTF-8 text where
recovery succeeded, ordered media positions, attachment links, and an explicit
outcome. The complete source queue, including both native index and RTF titles
where they differ, is in the private `build/cd2-preservation/candidates.json`.

| Result | Count | Meaning |
| --- | ---: | --- |
| Success | 220 | Readable export without a detected parser, media, or identity exception |
| Partial | 1,110 | Readable export with localized fields, undecodable bytes, title mismatch, missing action target, or deferred preview |
| Failed or blocked | 0 | No candidate body had to be discarded by this pass |
| Media occurrences | 2,661 | Every ordered article image marker has an associated record |
| Per-group media records | 2,139 | 2,008 direct bitmap previews, 130 flagged fallback previews, one deferred WMF preview |
| Unassigned decoder media | 284 | Originals and previews retained on a separate shelf; no article placement inferred |

The original media file is available even when its preview is deferred.
The 284 decoded image resources with no article RTF marker are available under
`unassigned-media/`, with source hashes and an explicit unassigned state.
`bm29.wmf` in `940434000` has an invalid header for the local converters and is
shown with an explicit unavailable-preview link to its original. Two source
copy actions, in `940719600` and `940924400`, have no matching external
attachment directory; their readable article bodies remain in the reference.
Sixty-nine native index titles differ from their RTF title footnotes, so both
strings remain in the source queue and the affected pages carry a review note.

Localized text records include 5,434 unresolved dynamic field occurrences in
1,073 articles, 639 undecodable byte runs in 102 articles, and 124 unsupported
RTF controls in 13 articles. The exporter puts visible markers into the text
instead of guessing characters. The `blocks.json` alongside each article gives
source byte fragments, media positions, and issue records. Original CD code
listings are preserved byte-for-byte; separate UTF-8 downloads retain their
decoded tabs, line breaks, and spaces. Ordered blocks retain bold and underline
marks where the CD RTF supplies them. ZIP/source attachments are copied from
the ISO tree without rewriting them.

The 58 remaining untitled RTF topics are inventoried outside the article count:
27 `MM` multimedia supplements, 26 link-list topics, four small untitled topics,
and one document tail. Their source spans and recovered supplemental text are
in `supplements.json` and `supplements/` under the private reference. These
classifications come from context names, links, and absence of article titles;
they do not assert printed-magazine relationships.

## Validation and limits

The complete reference built in CD-native group batches and then passed an
independent `--verify-existing` rebuild. `make check-cd2-reference` reconciles
all candidate and media counts with the source queue and verifies every
generated link, including the unassigned-media shelf. Chromium browser checks
covered the root index, the 9401 issue
list, Korean article text and 22 loaded images in `940116300`, the CP949 C
listing and three attachments in `940121800`, and the visible deferred-preview
state in `940434000`. The only observed console error was a missing favicon.

The CD is a secondary transcription. Paper text, issue identities, page labels,
article boundaries, and fallback-rendered WMF/DIB appearance have not been
checked against physical magazines or scans. Dynamic `vfld` fields interrupt
some labels and bylines. These remain visible as uncertainty markers. The
reading room now includes CD2 through its version 2 adapter, retaining native
groups separately from the library TOCs that end at 1993-12. Paper/OCR comparison, verified corrections, and publication policy are
separate follow-up work.
