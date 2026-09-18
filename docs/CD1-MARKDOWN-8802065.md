# Pilot Markdown reading preview

Step 5d derives a private reading format from the reviewed block map and unchanged
paragraph/run recovery. It is not the preservation format or a verified facsimile.

## Reproduce and read

```sh
python3 -m tools.render_cd1_markdown
```

Requires `build/cd1-text/8802065/article.json` and
`build/cd1-blocks/8802065/blocks.json` from steps 5b–5c. Input hashes must match the
reviewed recovery and block-map summary. The command compares generated metadata
with the [tracked preview summary](../data/catalog/markdown-previews/cd1-8802065.json).
`--write-record` deliberately regenerates that summary after a reviewed change.

Open these local, ignored files in a Markdown viewer supporting inline HTML:

- `build/cd1-markdown/8802065/introduction.md`
- `build/cd1-markdown/8802065/body.md`

The adjacent `provenance.json` records both input hashes, Markdown output hashes,
rendering policy, and each block's UTF-8 byte range. Its content ranges exclude
generated anchors, review notes, and caption-navigation links, enabling independent
comparison with source blocks. Every block retains its source projection hash and
ordered object references. The tracked summary contains metadata only; article
text, generated Markdown, and detailed provenance remain outside Git.

Outputs are deterministic and replaced individually. If interrupted during writing,
rerun the command to regenerate the complete set. Source files are never rewritten.

## Representation decisions

- All **271 blocks / 323 paragraphs / 289 runs** remain represented in source order.
  Each block has a stable anchor derived from its topic and paragraph range.
- Each topic title uses H1. The **28 headings** map the three source levels to
  H2/H3/H4, with counts 3/7/18. Introduction and body remain separate documents.
- **17 code/example blocks** use unlabeled backtick fences longer than every
  backtick sequence in their content. Text, indentation, trailing spaces, and
  internal blank lines are copied verbatim from the source paragraph projection.
- Source punctuation is escaped so prose cannot accidentally become Markdown
  headings, lists, links, images, or HTML. Boundary spaces use character entities
  to avoid Markdown trimming or interpreting them as indentation/hard breaks.
- Inline `<strong>` and `<u>` retain bold/underline across Korean/Latin font-run
  boundaries. This avoids emphasis-delimiter ambiguity and supplies underline,
  which has no standard Markdown delimiter. Renderers disabling inline HTML may
  omit styling and anchor navigation. Font selection and point sizes stay in the
  preservation data; the preview does not reproduce them.
- **13 caption links** point to the mapped code/figure/table anchors. Captions and
  content remain in source order rather than being moved next to guessed images.
- **21 object placeholders** keep resource names and order. Review notes identify
  unavailable images, the possible title navigation icon, image-backed table
  content without reconstructed cells, and the unresolved `bm54.wmf` attachment.
- The `tbl` example retains **ten inline WMF placeholders inside its code fence**
  with an explicit mixed-content note. It is not presented as fully recovered
  text-only code, and Markdown image syntax is not inserted into fences.
- **77 spacing blocks** keep their original whitespace after source-spacing
  comments. Markdown may collapse their visual spacing; the comments and block
  provenance make that limitation explicit. This is not original page layout.

## Validation and remaining work

All **55 tests** pass, including eight new tests for escaping and inline styles,
fence collisions, changed input hashes, missing/inconsistent content, deterministic
output, code whitespace, object order, caption links, and unresolved-resource notes.

The optional `markdown-it-py` package was available for independent CommonMark
rendering checks. Those tests verify every non-spacing block's rendered text
against the unchanged recovery, check spacing projections directly, and parse
the complete documents to verify 17 fences, heading counts, 271 anchors, and 13
working caption targets. They skip explicitly when that package is unavailable;
the exporter itself uses only the standard library and existing project tools.

The first parser check caught trailing spaces lost in two prose paragraphs.
Boundary-space escaping fixed both; all block comparisons now pass. Reading
prose in a browser still uses normal HTML whitespace layout, not RTF geometry.
Rerunning the exporter reproduces all output bytes, and generated content is
confirmed ignored by Git.

Next is **step 6: image mapping and viewable derivatives**, starting with the
owner's `convert` BMP/DIB → PNG and `inkscape` WMF → SVG suggestions. This step
has not converted images, inferred table cells, or resolved the unknown attachment.
Original-viewer comparison remains step 7; the first milestone is still pending.
