# CD1 graphics article: 터보 파스칼 한글 그래픽스 툴

Step **12b.3 is complete**. Reference `8802180` has a standalone v1 package and
a combined five-article package. The schema is unchanged. The
[preparation record](../data/catalog/article-preparations/cd1-8802180.json)
contains metadata, source locations, output hashes, and the remaining text-review
question. Article text, images, and conversion diagnostics remain private under
`build/cd1-articles/8802180/`.

## Match and source boundaries

The earlier coverage audit left this reference as a candidate because both CD
index occurrences use `터보 파스칼 한글 그래픽 툴`, while the TOC uses
`터보 파스칼 한글 그래픽스 툴`. Inspection now establishes that the **native title,
introduction title, and body title exactly match the TOC**. The body explicitly
reports February 1988, page 180; both indexes agree on issue and reference.
This supports the unique match to `maso-1988-02-toc-0026`. Both spellings remain
in provenance; no global title normalization or TOC edit was made.

| Evidence | Observed value |
| --- | --- |
| Index locations | `column.lst` line 423; `language.lst` line 600. |
| Introduction | Topic 157, alias `3M4LOI`, RTF bytes `[607600, 608710)`. |
| Body | Topic 158, alias `1KN6LQ`, context hash `0x0e6841cb`, RTF bytes `[608716, 633889)`. |
| Boundaries | Separators 156/159; native browse links to bodies 155/161; only hidden body link points to introduction 157. |
| Metadata | Byline `글/ 신상돈`; start page 180; end page unknown; print comparison pending. |

The two selected spans total **26,283 bytes**. Original source fingerprints,
native offsets, aliases, links, and all selected RTF token dispositions are
checked. Neighboring article text is excluded. Historical TOC inputs and earlier
packages remain reproducible independently of expanded current imports.

## Listings, figures, and decoding review

The recovery contains **397 paragraphs / 362 runs / seven media occurrences**,
organized into **80 blocks**: two titles, one issue label, one byline, eight
headings, 27 prose paragraphs, 27 spacing blocks, five code blocks, six captions,
and three figures.

Three Pascal listings preserve **18, 210, and 91 paragraphs**, including blank
lines and trailing spaces. The other two code blocks preserve an isolated address
formula and a procedure call. The first listing ends with the source's `end`
without adding a period. No listing is compiled or corrected.

Fonts 4/5 use CP949. Unlike earlier articles, font 15 contains Korean string
literals: seven runs fail the earlier ASCII policy. This article explicitly
uses strict CP949 for font 15 and verifies byte round-trips. Earlier articles'
font policies remain unchanged. No decoder extension was needed.

One string remains a **possible mixed-encoding case**, recorded as
`cd1-8802180-text-001`: topic 158, paragraph 320, source span `[629837, 629885)`.
Its two `88 74` byte pairs decode to `늯` (U+B2AF) in CP949 and `값` (U+AC12)
in Johab. The latter also occurs in the figure's separate text header and is a
plausible intended label. The alternative is recorded but **not applied**;
round-tripping alone cannot establish intended glyphs. Original bytes, the
chosen decoding, and a preview review note remain available for later comparison.

Figure 3 consists of a text header and a bitmap in separate source paragraphs
293–294. They remain one figure block in that order, linked from caption 291.
The Markdown renderer now supports multiple paragraphs within a figure; existing
single-paragraph output remains byte-identical. Six caption relationships cover
the three figures and three listings. Image-contained text is not transcribed.

## Media and package handoff

Five BMP/DIB resources convert to PNG with identical decoded RGBA pixels:
`bm39.bmp` (9 × 9), `bm41.bmp` (59 × 25), `p8021811.dib` (309 × 285),
`p8021812.dib` (438 × 126), and `82181_3.dib` (302 × 242). The three figures were
visually inspected; this does not verify them against paper.

Inline `bm57.wmf` and `bm58.wmf` convert with a missing Symbol-font warning.
They are **deferred**, with null runtime assets and explicit problem IDs in the
[deferred-media record](../data/catalog/deferred-media/cd1-8802180.json). Their
positions inside paragraph 12 and caption 14 remain intact. Source hashes and
private SVG/PNG diagnostics are retained; no repair or replacement text was
attempted. The two resources have identical bytes but retain their source IDs.

| Output | Contents |
| --- | --- |
| `build/cd1-articles/8802180/single/content/` | 12 runtime files: one article, five PNGs, seven media records, and two previews. |
| `build/cd1-articles/8802180/combined/content/` | 48 runtime files: five articles, ten sections, 582 blocks, 2,518 paragraphs, 33 media records, 35 media occurrences, and ten previews. |
| `build/cd1-articles/8802180/provenance.json` | Source and title evidence, font policy, text-review question, conversion diagnostics, and protected preview ranges. |
| `build/cd1-articles/8802180/deferred-media/` | Diagnostic derivatives excluded from runtime packages. |

Standalone validation precedes composition. The shared `bm39.bmp` record and
asset are checked against the predecessor and stored once. Every earlier article,
preview, media record, and asset remains identical. The combined package now has
four deferred WMFs, including the two earlier exceptions.

All five indexed February targets are prepared. Of 39 TOC entries, five now link
to articles; 34 remain unmatched in the runtime package, including four section
entries. This does not establish complete printed-issue coverage. The historical
coverage audit retains its original candidate decision; the new preparation
record supplies the additional evidence for the match.

## Reproduce

```sh
make restore-toc-snapshot
make prepare-cd1-graphics
PYTHONPATH=src python3 -m unittest discover -s tests -p test_cd1_graphics.py -v
make check
```

Requires private MVB/RTF/probe sources, imported indexes, historical TOC inputs,
the reviewed four-article package, ImageMagick, and Inkscape. Normal rebuilds
compare with both tracked preparation and deferred-media records before replacing
generated outputs. Next: **12c**, reconcile issue coverage and produce the
February issue handoff from these five prepared articles.
