# CD2 native candidates and 9401 issue slice

Run `python3 -m tools.map_cd2_candidates` after the CD2 source inventory.
The private `build/cd2-preservation/candidates.json` maps native index rows to
RTF topics by the WinHelp context hash and records title, byte span, actions,
attachments, and ordered media. The compact tracked record is
`data/catalog/preservation/cd2-candidates.json`. Use `--write-record` only when
reviewing an intentional change to that source map.

The three CD-native indexes have 1,326 distinct references: 497 in `book.lst`,
572 in `info.lst`, and 257 in `qnatip.lst`. All resolve to unique RTF topics.
Four more titled topics occur without index entries and are retained as
additional candidates. The remaining 58 unindexed topics have no title footnote
and require separate navigation/content classification. The RTF has 1,388 topics
total. Exactly **69** indexed titles differ from their RTF
title footnotes; the map keeps both strings instead of selecting one silently.

The candidate set has 2,661 ordered media occurrences; all resource names are
present in the decoder probe. Of 174 native source/list actions, two have no
matching external path: `SrcCopy(9407196)` in `940719600` and
`SrcCopy(9409242)` in `940924400`. Their bodies remain candidates for recovery.
The 12 provisional CD-native groups contain 93, 92, 98, 110, 109, 119, 120,
126, 116, 114, 121, and 112 candidates from `9401` through `9412`. These
groups are based on native references or incomplete RTF labels; they do not
establish independently verified 1994 magazine issues.

Run `python3 -m tools.build_cd2_issue` to build the private portable
`build/cd2-issue-9401/` slice, then `--verify-existing` to check an identical
rebuild. Its CD-native list shows all 93 candidates in RTF order and marks 91
as pending. Two cases are currently readable:

| Native reference | Structure | Export |
| --- | --- | --- |
| `940116300` | Long article, 22 bitmap occurrences, `SrcCopy` ZIP | 207 paragraphs, UTF-8 text, source blocks, original/PNG images, ZIP |
| `940121800` | Article, two navigation bitmaps, `SrcCopy` and `ListView` | 146 paragraphs, UTF-8 text, CP949 listing preserved plus UTF-8 listing, two source ZIPs |

Both topics account for every RTF token, retain four unresolved dynamic fields,
and preserve article/code whitespace. The second article's UTF-8 text has SHA-256
`a3c8d1254f33377cbbabc49f8785649f87d120c0c93fad0b7866c2fb8837878d`.
Two repeated issue builds agreed on the manifest. Chromium navigation opened the
second article from the issue list; the listing preview showed its Korean header
and C code, both images loaded, and links to three original attachments, UTF-8
listing, text, and source blocks were present. The first article was checked in
the browser separately. The only observed browser console error was a favicon
404.

Next: process every candidate in resumable CD-native group batches. Preserve
per-candidate success, partial, failed, and blocked outcomes, and render clear
unavailable states for failed resources. Classify the 58 untitled RTF topics
before calling the complete CD2 coverage report finished. Paper review remains
pending.
