# CD1 readable text, code and image reference

Open **`build/cd1-reference/index.html`** directly in a browser. The folder is a
portable private reference for human reading and comparison with paper scans/OCR.
It needs no server, framework, database or internet connection. Copy the whole
folder to move it; all links are relative. It currently occupies about 1.07 GB.

CD1 is also included in the completed [combined CD1/CD2/CD3 reading room](READING-ROOM.md).
This guide describes the independently preserved CD1 reference and its counts.

## What is available

| Content | Count |
| --- | ---: |
| Issues in the library TOC | 122 |
| Issues with CD1 articles | 72 |
| CD1 article candidates accounted for | 1,088 |
| Articles with text exports | 1,080 |
| Text exports without decoding-gap markers | 1,047 |
| References with localized text gaps | 33 |
| Candidates blocked by unresolved article boundaries | 8 |
| Listing / preformatted-text downloads | 3,125 |
| Paragraphs represented | 458,678 |
| Image occurrences | 7,738 |
| Distinct referenced images | 6,090 |
| Images with viewable derivatives | 4,979 |
| Deferred images with original-file links | 1,111 |

The 995 previously prepared articles retain their text and meaningful marks.
All 85 previously failed candidates now have reference text: **52 without marked
text gaps, 33 with explicit gaps**. This includes `를` in `8901110` and `！` in
`9103202`; ordinary font changes no longer split their encoded characters.

These counts describe availability of CD reference material. They do not certify
agreement with the printed magazines or replace the historical 19b package results.
The eight blocked candidates have review pages, with no guessed article boundaries.

## Reading and comparing

Each issue lists its **CD articles separately from the library TOC**. Different
transcribed titles or missing reviewed TOC links do not hide article text. Existing
reviewed links are retained; uncertain matches are not invented. The 50 earlier
issues without CD1 bodies have TOC pages and explicit missing-source notices.

Each available article provides:

- `index.html`: readable text, preformatted listings and images near their source
  content, with source/review notes available separately.
- `article.txt`: UTF-8 text for searching, diffing or comparison with OCR. Tabs,
  code spacing and logical line breaks remain intact. `[image:filename]` marks
  an image occurrence; text within images has not been automatically transcribed.
- `listings/001.txt`, etc.: individual preformatted blocks without HTML or Markdown
  escaping. These include code candidates, fixed-width tables and terminal output;
  the exporter does not infer language or repair programs.
- `paragraphs.json`: stable paragraph IDs, character offsets, line ranges and
  image references in the text export. Offsets count Unicode characters, not bytes.
- `reference.json`: source associations, text blocks and review evidence.

Each image page offers the available PNG/SVG derivative and its original CD file.
Code embedded in an image can be inspected or OCRed from those files. Deferred
WMFs remain explicitly unavailable for inline viewing; their originals are retained.
Nine DIBs rejected by Pillow were decoded by ImageMagick and have conversion notes.
No WMF repair investigation was added.

For the newly recovered articles, ordinary fonts, colors, margins and alignment
are normalized. RTF line/tab/cell/row controls retain readable boundaries; tables
may appear as tab-separated text. Remaining undecodable bytes appear as
`⟦bytes:…⟧`, and ambiguous Symbol text appears as `⟦symbol font …⟧`.
There are **371 localized gap records** across 33 articles. These markers are
review annotations and must not be mistaken for source-code characters.

CD text is a secondary transcription. Compare differences against the paper or
scan; do not automatically overwrite OCR with CD text. Human editing errors and
omissions can exist in either source. Paper verification remains pending throughout.

## Rebuild and checks

```sh
make export-cd1-reference
make check-cd1-reference
PYTHONPATH=src python3 -m unittest discover -s tests -p test_cd1_reference.py -v
```

The initial build uses `REFERENCE_ARGS=--write-record`. Later runs build in isolation
and verify identical output against the existing export. To retain an old export
while changing the exporter, use a new path such as
`REFERENCE_ARGS="--output build/cd1-reference-v2"`.
The [tracked summary](../data/catalog/batch-runs/cd1-readable-reference.json)
contains counts and source/output hashes; text and images remain in ignored build
output. The 19b packages, decoder and previous audit records remain unchanged.

Validation: all **12 focused tests pass without skips**. The complete export check
verifies **26,828 files, 7,994 HTML pages and 81,086 local links**, and checks all
1,080 article text exports, paragraph positions and 3,125 listing downloads against
the reference blocks and generated HTML. A complete rebuild reproduces the manifest
and every output file exactly. Chrome checks using direct `file:` URLs confirm
issue/article navigation, readable Korean text, the recovered fullwidth character,
text links and image pages. The Turbo C listing has identical **30,624 characters
and 30 tabs** in its HTML code block and opened text file; code uses preformatted
spacing. A source diagram renders at its 467×258 dimensions with its original-file
link. These checks validate usability, not agreement with paper.

This finishes the usable CD1 reference deliverable with visible exceptions.
Paper/OCR restoration, scans, uncertain characters, unresolved ownership and deferred
images remain follow-up work driven by actual restoration needs. The richer reading
room SPA and CD2/CD3 have separate scopes.
