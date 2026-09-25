# CD2 pilot article: 940116300

Build with `python3 -m tools.build_cd2_pilot`. The output is the private portable
`build/cd2-reference-pilot/` directory. Run with `--verify-existing` to check
that a repeat build has the same file inventory and SHA-256 values. The tool
requires the checksummed source inventory produced by
`python3 -m tools.inventory_cd2_sources`.

The pilot is `한글 TeX을 이용하려면`, native index reference `940116300`. Its
77,248-byte RTF topic is identified by the index title, RTF title footnote,
context `3H9UTZ3`, and `SrcCopy(9401163)` action. The builder tokenizes every
byte of that topic, skips the explicitly recognized metadata and hidden action,
decodes visible text as CP949, and preserves paragraph, line, tab, bold, and
ordered image runs in `blocks.json`. `article.txt` is UTF-8 and has 207
paragraphs. Four dynamic `vfld` occurrences in the printed label and byline
remain visible as `⟦field:…⟧` with issue records. No paper correction is implied.

The source ZIP is copied byte-for-byte from
`DATA/SOURCE/9401163/TEX.ZIP`. All 22 referenced bitmap resources are retained
as original files and rendered as PNGs next to their article positions. The
builder checks each original against the source inventory and verifies PNG pixel
equality. Text, source blocks, attachment, and image links are relative and work
under a local static server.

Validation on 2026-09-26: two consecutive builds had the same manifest and
text SHA-256 `59c20be8a67421ec9251d267ddf2db90884c1561e5932f76c166c9f1c2189ec4`.
In Chromium via Playwright, the Korean article heading and text rendered, and
all 22 image elements had positive natural width. The ZIP and original image
links point to files included in the manifest. Browser console output contained
only a missing favicon request.

The `94.` / `1` / `163p` label is interrupted by unresolved dynamic fields.
It is not a verified magazine issue or page citation. The RTF topic boundaries
are decoder boundaries, and print agreement is pending paper review. The pilot
does not establish that all CD2 topics share this structure. Next: inspect the
CD-native issue index, choose a second case with a different attachment or
media pattern, and build one browsable issue slice before a complete pass.
