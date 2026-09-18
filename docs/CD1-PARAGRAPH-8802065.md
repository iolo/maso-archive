# CD1 pilot: one decoded paragraph

Step 4 recovers only the first prose paragraph under section I in the body of
“유닉스란 무엇인가?” (`8802065`). The source stays unchanged. Text and raw
bytes stay in ignored build output; the committed
[sample record](../data/catalog/paragraph-samples/cd1-8802065.json) contains
locations, hashes, encoding decisions, counts, and review status only.

## Reproduce and inspect locally

From the repository root:

```sh
python3 -m tools.decode_cd1_paragraph
```

The command checks the exact RTF snapshot, step 3 topic-map hash, sample span,
and recorded metadata before writing these local artifacts:

| File under `build/cd1-paragraph/8802065/` | Purpose |
| --- | --- |
| `paragraph.raw.rtf` | Exact source slice; a fragment, not a standalone RTF file |
| `paragraph.cp949` | Text bytes after RTF token handling, before Unicode decoding |
| `paragraph.txt` | UTF-8 paragraph followed by one LF |
| `provenance.json` | Source and output checksums, decisions, limitations |

`--write-record` regenerates the tracked metadata when deliberately reviewing a
change. Normal runs compare with that record. Validation failure writes no new
outputs; any old outputs remain attributable to their recorded source hashes.
Each artifact is replaced individually; after an interrupted write, rerun before
using the output set. The tool is a bounded sample decoder, not a general RTF CLI.

## Source and font decisions

- RTF span **`[378665, 379785)`**, zero-based and end-exclusive: **1,120 bytes**.
  It lies entirely inside mapped body ordinal 149 and starts immediately after
  a paragraph delimiter. It includes its own formatting prologue and terminal
  `\par `, without consuming the following paragraph's text.
- Prologue: `\pard\sl285\li395\ri395 \plain\fs18 `. Character state resets
  with `\plain`; the document's `\deff4` selects font 4, **Arial**, at 9 points.
  There are no font switches within the sample. Font declaration byte spans are
  included in the record.
- The header contains `\ansi` but no explicit `\ansicpg`, `\cpg`, or
  `\fcharset` declaration. Arial alone cannot determine these Korean bytes'
  encoding. **CP949 is an explicit source-specific interpretation**, supported
  by the known Korean sources and strict decoding of this sample. EUC-KR gives
  identical text here. This does not establish encoding or glyph mappings for
  every font elsewhere in the document.
- The default-font reset interpretation also matches pinned HELPDECO's
  `ChangeFont` implementation: after emitting `\plain`, it sets
  `CurrentFont.FontName=DefFont`. See
  [the decoder source](https://github.com/joncampbell123/helpdeco/blob/b9c187a20d83a3e738d8fe073eb924a8b7264c5c/helpdeco.c).

## Token handling and validation

The decoder recognizes the exact sample prologue and final paragraph control.
It collects `\'hh` byte escapes together with ASCII text before strict CP949
decoding, so a Korean two-byte character is not decoded one byte at a time.
Escaped braces/backslashes are supported as literal text and are never reparsed
as RTF commands. Groups and other controls cause an explicit failure.

Control-word delimiter spaces are syntax, while subsequent text spaces are
preserved, following [Microsoft's RTF syntax rules](https://learn.microsoft.com/en-us/previous-versions/office/developer/office2000/aa140284%28v%3Doffice.10%29).
Physical CR/LF bytes are omitted from the fragment's text stream; its terminating
paragraph control becomes one LF in the UTF-8 output. No Unicode normalization,
spelling correction, punctuation replacement, or whitespace collapsing is applied.

The result contains **182 characters: 128 Hangul syllables and 54 ASCII
characters**, corresponding to 310 CP949 bytes. The sample exercises Korean,
English abbreviations, parentheses, periods, and a question mark. It contains no
symbol-font glyphs or typographic special-character controls; those remain
unsupported. There are no replacement characters, and re-encoding to CP949
reproduces the tokenized bytes exactly.

Independent codec verification passed:

```sh
iconv -f CP949 -t UTF-8 build/cd1-paragraph/8802065/paragraph.cp949
```

That output matches `paragraph.txt` before its added terminal LF. Focused tests
also cover mixed Korean/ASCII, repeated spaces, escaped RTF syntax, incomplete
multibyte sequences, malformed byte escapes, and rejected controls/groups.
All 32 repository tests pass. These checks establish reproducibility and byte
handling; the original viewer comparison remains pending.

## Remaining scope

The tool rejects nested groups/destinations, hidden metadata, font changes,
symbol-font mapping, Unicode escapes, most special-character controls, tabs,
tables, images, embedded objects, and other paragraph prologues. It must not be
applied to the entire article by merely widening the byte span.

Because this paragraph does not exercise the rest of the RTF, step 5 is now
split: **5a inventories controls and fonts in the two mapped topics**, then
**5b recovers ordered full text**, preserving structure or explicitly reporting
unsupported content. Image conversion and viewer comparison remain later steps.
