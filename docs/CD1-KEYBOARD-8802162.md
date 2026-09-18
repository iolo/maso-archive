# KEYBOARD LOCK: the unindexed February article

Step **12d** recovered a sixth February 1988 article that all three CD indexes
omit. Native topic **155** is “KEYBOARD LOCK”; its linked introduction is topic
**154**. The TOC has the exact title at page **162**, entry
`maso-1988-02-toc-0023`. The body explicitly says `88.2.  162p` and its issue keyword
says February 1988. Its numeric reference candidate `8802162` and exported alias
`1KN6JI` resolve to the same native context hash, `0x0e68416d`, and topic offset
`2131408`. Identity is supported by these combined observations, not a page suffix
alone. The preparation retains an empty index-occurrence list.

The introduction alias is `3M4LMA`. Native links, both context entries, the blank
neighbor topics 153/156, and browse neighbors 152/158 constrain the article bounds.
The two RTF spans total **53,683 bytes**. The source hashes, byte accounting,
metadata match, block map, conversion evidence, and Markdown content ranges are
retained in private provenance. The tracked
[preparation record](../data/catalog/article-preparations/cd1-8802162.json)
contains metadata and output hashes only.

## Preserved structure

The article contains **303 paragraphs, 315 runs, and 95 blocks**. Fonts 4/5 use
CP949; Fixedsys font 15 uses the checked ASCII policy. Ten headings follow the
source's bold size hierarchy; line-range subheadings retain their full text.
The editorial byline is preserved as written; program comments are not substituted
for the article byline. End page and physical verification remain unknown/pending.

| Source content | Representation |
| --- | --- |
| LOCK.BAS, body paragraphs 86–122 | 37 source paragraphs in a verbatim code block. |
| LOCK.ASM, body paragraphs 126–298 | 173 source paragraphs, preserving indentation and blank lines. |
| Three numbered tables | Image-backed table blocks; cells are not reconstructed. |
| Attribute-byte diagram | Figure block linked to its numbered caption. |
| Six captions | Explicit links to three tables, the diagram, and both listings. |
| Title bitmap | Preserved in its original mixed media/text position. |

All five resources (`bm56.bmp`, `88021631.dib`, `88021642.dib`, `p8021641.dib`,
`88021653.dib`) convert to PNG with matching dimensions and decoded RGBA pixels.
Trailing spaces after image objects remain in the structured content. No archived
program was executed, compiled, repaired, or silently corrected.

## Reproduce

```sh
make prepare-cd1-keyboard
make close-cd1-february
PYTHONPATH=src python3 -m tools.build_reading_room_package --verify build/cd1-issues/1988-02-native/content
```

Preparation requires the preserved private sources, historical TOC snapshot,
index import, and preceding graphics five-article package. It creates a **12-file
standalone** and **56-file six-article** package under `build/cd1-articles/8802162/`.
Standalone validation precedes composition; all older article, preview, media
bytes, and media metadata remain identical. The subsequent
[issue handoff](CD1-ISSUE-1988-02.md) adds complete February native-metadata coverage
and preserves the older indexed checkpoint separately. The approved v1 schema
is unchanged, and all extracted content remains private.
