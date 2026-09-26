# CD3 source map and native candidate queue

The supplied `masocd-3.iso` is 327,081,984 bytes with SHA-256
`7c269df8479c72919863f27b68dceb6fe8b567a18f27eb9481655e15e4ae17d0`.
Run `make inventory-cd3-sources` to verify its hash, all 137 extracted files
against a fresh ISO extraction, both decoded M14 probes, and the 2,130 members
listed inside 105 CAB archives. The full checksummed inventory remains private
at `build/cd3-preservation/inventory.json`; the tracked summary contains no
publisher article text. The source ISO and extracted tree are never rewritten.

The pinned HELPDECO revision
`b9c187a20d83a3e738d8fe073eb924a8b7264c5c` used for CD1/CD2 also decodes
CD3's M14 containers. The existing local binary was built with
`make helpdeco CFLAGS='-g3 -O0 -Wno-error=incompatible-pointer-types'`.
From empty `private/cd3-probe/main/raw` and `private/cd3-probe/list/raw`
directories, run it with `../../../../masocd-3/MASO3.M14 /g` and
`../../../../masocd-3/LIST.M14 /g`, respectively. Relative input paths matter:
HELPDECO treats a leading slash as an option. Retain the decoder logs beside
the probes. The main M14 yields a 25,222,941-byte RTF and 1,570 BMPs; LIST.M14
yields one small RTF and a 161-byte `LIST1.TXT` baggage file. LIST.M14 is not
the article index. The owner's setup observation is that it installs no
software and only creates a shortcut to the viewer on the CD.

Known decoder limitation: [HELPDECO's font reader interprets CD3's Hangul
character-set byte as double underline](CD3-HELPDECO-UNDERLINE-BUG.md).
The pinned probe therefore contains bogus `\uldb` formatting. The reading display
suppresses CD3 underlining; the decoder and checksummed probe remain unchanged.
Use the bug record for byte-level evidence and the deferred correction path.

Run `make map-cd3-candidates` to reproduce
`build/cd3-preservation/candidates.json` from the checksummed source inventory.
The main RTF has 2,336 page-delimited topics. Native title footnotes identify
967 article candidates. A further 1995-06 body, `topic-0859`, lacks a title
footnote and context alias but carries a native issue/page label and the same
article structure as its neighbors. Its visible lead phrase is retained as a
provisional display title, giving **968** source-bound candidates. The other
topics are 12 author bios, 1,355 auxiliary topics, and one document tail. A
title footnote or reviewed body structure is evidence of a CD candidate, not
proof of a paper article boundary. The CD's own date labels form 18 groups: 12 apparent
1995 months, four 1994 months, one 1996 label, and an undated group. Two
candidates have multiple month labels and five have none; all seven remain
undated. These labels are not verified printed-issue identities, and CD3 cannot
be described as an exclusively 1995 source.

The RTF has 2,384 ordered image markers. Most article `Click.bmp` markers are
viewer controls linked by context alias to separate figure topics. The map
resolves 969 of 971 figure links to single-image topics; two target aliases
(`CKX.TC`) are unresolved in HELPDECO's own log. Eight resolved figure topics
refer to BMPs absent from the decoded probe. Across all topics, 253 image
occurrences refer to missing decoded sources. These remain explicit gaps. An
additional 511 decoded BMPs have no RTF marker and remain unassigned. Do not
infer their article placement from similar names.

Article actions also link to 115 text-only sidebars, all 12 author bios, and
other articles. The candidate queue records each action's source offset and
target topic. The reference exports every supplemental topic as a readable page
or explicit media record; the text boxes remain linked from their source
articles. Three longer auxiliary texts have no article link and remain
discoverable on the supplemental-topic shelf. All 1,570 decoded BMP originals
are retained in a global media shelf.

The RTF contains 80 `fc(Files\\...cab)` actions. Seventy-nine resolve to
byte-identical CAB files in the ISO tree. `Files\\9504\\Grid.cab` in
`topic-0104` is missing; its article body is still readable. CAB member names
and sizes are recorded without treating files inside an attachment as articles.
The source map keeps both the article marker and its resolved figure identity,
so the reference can place the actual figure beside the article caption rather
than showing only the viewer's Click icon.

The first readable case was `topic-0036` (`FLI, FLC 파일 분석`), a 1994-labeled
topic with inline C and assembly spacing. The second structural case was
`topic-0037` (`애니메이션 플레이어 제작`), which links a viewer icon to the separate
313×132 `T01311.BMP` figure. The source map and these cases establish the
export path; neither establishes agreement with the printed magazines.
