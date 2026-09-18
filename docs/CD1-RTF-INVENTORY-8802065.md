# Pilot RTF feature inventory

Step 5a inventories the introduction and body of `8802065` before full-text
conversion. Full-text preparation is required independently of publication;
future ownership/access verification does not block this work.

Run from the repository root:

```sh
python3 -m tools.inventory_cd1_rtf
```

The command validates the pinned RTF and topic-map hashes and compares the
generated summary with the [tracked metadata](../data/catalog/rtf-inventories/cd1-8802065.json).
It writes `summary.json` and a detailed `inventory.json` under ignored
`build/cd1-rtf-inventory/8802065/`. `--write-record` deliberately regenerates the
tracked summary. No body text is decoded or published. Outputs are individually
replaced; rerun after an interrupted write before using them together.

## Coverage and structure

| Feature | Introduction (148) | Body (149) |
| --- | --- | --- |
| Source bytes / accounted bytes | 1,310 / 1,310 | 148,269 / 148,269 |
| Paragraph controls, including blank paragraphs | 4 | 319 |
| Metadata footnotes | 1 context ID | 5: browse sequence, title, context ID, two keyword fields |
| Superscript metadata-marker groups | 2 | 10 |
| Hidden context-link groups | 0 | 1 |
| Embedded-object markers | 0 | 21 |
| Literal-brace guards inserted by HELPDECO | 0 | 5 |

Token spans are contiguous and cover every byte, including control delimiters,
physical newlines, group braces, and byte escapes. The detailed report records
every control occurrence/parameter, group extent/parent, selected font at each
token, and object-marker location. These counts describe RTF structure, not
article paragraph/heading counts after semantic interpretation.

The observed control words are `b`, `f`, `fs`, `footnote`, `keepn`, `li`, `par`,
`pard`, `plain`, `qr`, `ri`, `sa`, `sb`, `sl`, `ul`, `up`, and `v`. All groups and
controls in these spans are classified; unknown input in future runs is reported
or rejected, not silently discarded. The lexer retains unknown control words and
handles declared binary payloads opaquely; malformed escapes, binary lengths,
and group boundaries fail explicitly.

No table, tab, Unicode-escape, or explicit line-break controls were observed.
This does not mean the article lacks tables, equations, or code: they can occur
as formatted paragraphs or image resources. Paragraph spacing/indents, font size,
bold/underline, and original text spacing must survive the next step's structured
output, without guessing semantic headings or table layouts solely from counts.

## Fonts and metadata

Font 4 is Arial and font 5 is 굴림체; both carry visible text tokens. Font 6
(Times) is selected in an empty introductory paragraph before switching to
굴림체. No Symbol or Wingdings selection occurs in these two spans. The header
does not declare a code page or font charset. CP949 remains the source-specific
choice established by the paragraph sample, with strict run-level checks still
required for the rest of the text.

Font state is scoped to groups: a `plain` inside a footnote resets that group's
font, then the outer state is restored. The introductory topic ends in font 4;
the body inherits that state across the intervening topic delimiter. The tool
starts the introduction with unknown inherited state and confirms that its
visible text is preceded by an explicit font/reset. It does not silently assume
the font for an uninitialized run.

Metadata-marker and footnote groups must stay separate from visible prose. The
body's hidden context link is navigation to the introduction, not article text.
Detailed source positions allow these decisions to be checked without including
metadata strings in the recovered prose.

## Object markers and the brace-escape finding

The body has 13 `bmc` markers and eight `ewl mvbmp2, ViewerBmp2` markers:
one BMP, 12 WMFs, and eight DIB references. These are 21 occurrences, not a claim
of 21 editorial illustrations; one is the introduction/navigation icon, and
several resources may compose a single diagram. Resource existence, rendering,
and text relationships are step 6 work. Step 5b must preserve their order as
explicit placeholders instead of deleting the commands or exposing them as prose.

The first inventory pass flagged five `\-` symbols at bytes **461973, 461988,
462007, 462044, and 462088**. Every one immediately follows a literal `\{` in
example text. Inspection of pinned HELPDECO's `TopicDump` explains this pattern:
it inserts an invisible dash after a literal opening brace to prevent sample
text from being interpreted as a help-compiler command. See
[HELPDECO's emitter](https://github.com/joncampbell123/helpdeco/blob/b9c187a20d83a3e738d8fe073eb924a8b7264c5c/helpdeco.c#L3482).

Those five sequences are now explicitly classified as **literal-brace guards**.
They need recorded removal when recovering the original example text; treating
them as ordinary hyphens would corrupt it. Genuine object markers have unguarded
escaped braces and recognized command shapes. A lone `\-` remains a review
issue rather than receiving the same treatment automatically.

## Validation and next step

All 37 repository tests pass, including five new tests for contiguous byte
coverage, escaped syntax/binary data, scoped fonts and metadata, literal braces
versus objects, unknown/malformed constructs, and the actual private inventory.
The reviewed inventory has no unclassified constructs. That result establishes
lexical coverage only; it does not establish correct full-text decoding or
viewer fidelity.

Step 5b now has a concrete scope: recover both topics into private text and
structured paragraphs/runs; preserve spacing and observed formatting; separate
metadata; retain object placeholders; handle the five brace guards explicitly;
and reproduce the step 4 paragraph exactly. Full recovery and original-viewer
verification remain pending.
