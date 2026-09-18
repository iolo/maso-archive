# Structural fidelity and Markdown for the pilot

The owner correctly noted that plain text loses distinctions among code,
figures, headings, and other content blocks. Step 5b recovered the text layer
and observed formatting; it did not finish a faithful reading edition. Plain
text is a convenience export. Keep the original RTF and structured recovery,
and add semantic block decisions as a separate layer.

## Evidence from the actual article

Reviewed `build/cd1-text/8802065/article.json`, SHA-256
`d92a4231df2dce3d81bbf709e8191bde741397a77218cc5e61aaa6a130b0b1a1`.
Paragraph numbers below are one-based within body topic 149, not print paragraph
numbers. No publisher prose is reproduced here.

| Evidence | Observation | Implication |
| --- | --- | --- |
| Paragraphs 6, 11, 303 | Bold 12-point text, heading indent, Roman-numbered labels | Three first-level heading candidates |
| Paragraphs 12, 23, 52, 275, 304, 309, 314 | Bold 10-point text, heading indent | Seven second-level heading candidates |
| 18 paragraphs, including 26, 30, 224, 290 | Bold 9-point text, heading indent | Third-level heading candidates; validate numbering/context |
| Paragraphs 7, 182, 204, 207, 208 | Identical paragraph and Arial 9-point normal run formatting | Prose, code, captions, and objects cannot be distinguished by style alone |
| Paragraphs 182–202 | `.PS`–`.PE` example with indentation and internal blank lines | One code-block candidate spanning multiple RTF paragraphs |
| Paragraphs 212–217 | `.EQ`–`.EN` example | Preserve source code rather than automatically typesetting an equation |
| Paragraphs 180, 207–208, 210 | Figure captions introduce code, a rendered diagram, and more code | Caption relationships are not limited to image blocks |

The style collision was checked directly, including run-format equality. Prose
paragraph 7 spans RTF `[378665, 379785)`; the first code line (182) spans
`[460163, 460172)`. The complete example candidates span `[460163, 460684)`
and `[461953, 462154)`. Their boundaries are supported by syntax and context;
original-viewer confirmation is still pending.

The inventoried topics use direct formatting, without semantic style references
such as “Code” or “Heading 1”. Absence of table controls does not prove absence
of tabular content. Images and manual/viewer evidence may supply missing structure.

## Block model

Keep `article.json` as the recovered paragraph/run layer. A separate block map
should identify titles, headings/levels, prose, code/examples, captions, figures,
tables, or unresolved content. Each decision needs source topic/paragraph/run
references, byte spans, evidence, and a review/uncertainty status.

Every paragraph/run and object occurrence must be accounted for once in source
order. Preserve blank paragraphs and spaces inside examples. Caption/figure
relationships should reference blocks rather than duplicate content. Multiple
objects may compose one figure; a navigation icon needs its own role. Never
invent table cells or discard uncertain content to make the classification tidy.

## Markdown recommendation

Generate Markdown as a **derived reading/export format** from those decisions.
Retain RTF, structured recovery, and the block map as preservation sources;
Markdown does not reliably retain exact typography or complex layouts.

| Identified content | Markdown export |
| --- | --- |
| Titles/headings | Heading hierarchy |
| Prose | Paragraphs and supported inline emphasis |
| Code/examples | Fenced blocks preserving exact content and spaces; choose a safe fence length and only supported language labels |
| Figures | Ordered image references with captions; preserve composite relationships |
| Simple confirmed tables | Escaped Markdown tables |
| Complex/image-based tables or uncertain layout | Retained image/structured representation and an explicit review note |
| Unresolved resources | Explicit placeholders until image mapping supplies paths |

Escape prose syntax without changing code text or non-ASCII characters. Keep
navigation metadata out of reading text. A successful Markdown render does not
verify inferred structure: viewer comparison must also check heading hierarchy,
code boundaries, caption relationships, and tables/figures.

Next: **5c block identification**, **5d private Markdown preview**, then
**6 image mapping** and **7 viewer comparison**. The Markdown preview can be
regenerated with image paths after step 6; initial placeholders must be explicit.
