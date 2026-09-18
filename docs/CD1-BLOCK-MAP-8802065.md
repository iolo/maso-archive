# Pilot block map

Step 5c adds a semantic layer over the unchanged recovered paragraphs/runs.
Decisions are supported by the inspected source and remain pending original-viewer
review. This is one checksummed pilot, not an automatic classification scheme for
the whole collection.

## Reproduce

```sh
python3 -m tools.map_cd1_blocks
```

Requires `build/cd1-text/8802065/article.json` from step 5b. The command rejects a
different source hash, compares its output with the
[tracked summary](../data/catalog/block-maps/cd1-8802065.json), and writes
`blocks.json` and `provenance.json` under ignored `build/cd1-blocks/8802065/`.
`--write-record` deliberately regenerates that summary. Output files are replaced
individually; rerun after an interrupted write. No recovered text is rewritten.

The map contains source references and decisions, not copies of article text.
Block IDs encode the topic and inclusive paragraph range. Each member identifies
its paragraph, all owned run ordinals, and raw source span. Object references
retain the run position, filename, and RTF byte offset. Relationships reference
blocks without acquiring ownership of their content a second time.

## Result

**271 blocks cover all 323 paragraphs, 289 runs, and 21 objects**, preserving
source order. The run total includes 268 text runs and 21 object runs.

| Kind | Count | Evidence/interpretation |
| --- | --- | --- |
| Title | 2 | Introduction title and body title with navigation icon |
| Heading | 28 | Bold size/indent plus numbered labels: 3 level-one, 7 level-two, 18 level-three |
| Code/example | 17 | 12 isolated commands, one terminal transcript, four formatting-language examples |
| Caption | 13 | Twelve figure captions and one table caption |
| Figure | 8 | Caption-linked image content, including a rendered table |
| Table | 1 | Table-caption-linked image; no invented cells |
| Issue label / byline | 1 each | Visible opening metadata remains represented |
| Paragraph | 122 | Preserved paragraph fallback, without stronger semantic claims |
| Spacing | 77 | Blank/whitespace paragraphs outside grouped examples |
| Unresolved | 1 | WMF whose attachment cannot yet be established |

Heading parents use the observed three-level hierarchy. Caption links are explicit:
figure captions 4, 6, 8, and 10 point to code/examples, while the other captions
point to image content. Inline prose references such as a sentence mentioning
Figure 1 remain paragraphs rather than being mistaken for captions.

The mapper combines limited formatting rules with **explicit, source-reviewed
paragraph ranges** for the ambiguous cases. Each block records the evidence basis,
decision status, and review concerns. Code language labels are left unset for the
Markdown exporter rather than guessing a syntax-highlighter name.

## Cases that must survive rendering

- Body paragraphs **137–145**: the `mm` macro example. Its English text lines
  belong to the example rather than being separate prose paragraphs.
- **156–173**: the `tbl` example, with **ten inline WMF objects** interleaved
  with text. Its representation is `mixed_text_objects`; it is not text-only code.
  Internal blank paragraphs remain members of the same block.
- **174**: `bm54.wmf`, immediately after the example terminator and before the
  next caption. Keep it as an unresolved block until image/viewer evidence shows
  its relationship; do not attach it to either neighbor by guesswork.
- **182–202** and **212–217**: `pic` and `eqn` source examples, including original
  indentation, blank/space-only lines, and literal braces.
- **255–257**: command prompt, usage output, and final prompt form one transcript.
- **283**: the image for Table 1. Figure 7's rendered output is also table-related.
  Neither supplies recovered cell geometry; both require image inspection.

The title's icon is retained with a navigation-role candidate. Image-backed blocks
keep explicit inspection concerns. No semantic decision is marked viewer-verified.

## Validation and next task

Validation checks exact paragraph/run/object coverage, ordering, source spans,
caption targets, heading parents, and block text hashes. Projecting member
paragraphs back in order reproduces the original introduction/body byte-for-byte,
including whitespace; no source paragraph or object is duplicated or omitted.

All **47 tests** pass. Five new tests cover combined heading evidence, changed
source rejection, mixed example objects/internal blanks, omission/duplication/
relationship failures, and code-spacing changes. Private output is deterministic.

Next is **step 5d: private Markdown preview**. Pure text examples can be fenced
without changing their content. Mixed text/object examples need explicit resource
placeholders and review notes; Markdown image syntax inside a code fence will not
render those images. Preserve the structured mixed-content block and its ordered
object references for later richer rendering. Unknown attachments and unavailable
image resources must remain visible as unresolved, not silently flattened away.
