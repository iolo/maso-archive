# CD1 interview: CP/M의 게리 킬달

Step **12b.1 is complete**. Reference `8802030` is recovered into a standalone v1
package and a combined three-article package. The approved schema is unchanged.
The [tracked preparation record](../data/catalog/article-preparations/cd1-8802030.json)
contains metadata, source locations, validation results, and output hashes; article
text, previews, and assets remain private under `build/cd1-articles/8802030/`.

## Source mapping and boundaries

| Source | Evidence |
| --- | --- |
| TOC | `maso-1988-02-toc-0031`, reported page 30; series prefix `유명한 프로그래머를 만났읍니다(5) : ` precedes the CD title. |
| CD index | Both occurrences explicitly label February 1988 and use the same title/reference. This specific prefix comparison is unique within the issue. |
| Native body | Context hash `0x0e6881f5`, topic 146, generated RTF alias `6SRE0ZE`. |
| Introduction | Topic 145, alias `3M4UJI`; the body's only hidden context link points here. |
| RTF spans | Introduction `[305158, 306658)`, body `[306664, 376607)`: 71,443 bytes, excluding the intervening page control. |
| Adjacent boundaries | Topics 144 and 147 are verified separators. Native browse links lead to previous body 143 and next body 149; their article text is excluded. |
| CD metadata | Native/introductory title agrees; body explicitly labels page 30 and credits `글/ 편집부`. End page remains unknown. |

Original MVB/RTF fingerprints, context records, topic links, RTF aliases, and every
token's disposition are checked. Both topics decode using the already established
font 4/5 CP949 policy, without unsupported runs or new decoder behavior. The
historical TOC snapshot is read explicitly; growing current imports do not rewrite
the evidence for this package.

## Interview structure

The two topics contain **107 paragraphs / 85 runs / one media occurrence**:
four introductory paragraphs and 103 body paragraphs. All 107 paragraphs have
corresponding ordered blocks: two titles, one issue label, one byline, 71 prose
paragraphs, and 32 spacing blocks.

The interview has **27 prompts and 40 answer paragraphs**. Prompts consistently
use bold 18-half-point text, left indent 215, and spacing-after 95; answers use
plain text and may span several paragraphs. Some prompts invite discussion without
ending in a question mark, so punctuation alone is not the identification rule.
The case-specific paragraph positions and formatting are checked during rebuild.

Prompts remain paragraph blocks with bold runs. No artificial section headings,
speaker names, or visible Q/A prefixes are inserted. The private block map gives
them `interview_question` / `interview_answer` subtypes and records each turn's
question and answer block IDs. These semantic associations remain in preservation
metadata: v1 does not have dedicated question/answer roles in its runtime schema.
The viewer can render the faithful ordered paragraphs immediately; a future
semantic interview UI would need an explicit contract extension.

The introduction calls Kildall the fourth programmer while the TOC series label
uses `(5)`. Both statements are retained without harmonizing their numbering.
Source wording, including apparent typos, is preserved rather than silently edited.

The owner identifies this as a translated interview from *Programmers at Work*.
That note is recorded as **owner-provided, not checked against the book**. A book
credit was not observed in the recovered CD text. The runtime byline remains the
CD's editorial credit; no book author/interviewer/translator attribution is inferred.
Neither book completeness nor physical-magazine accuracy has been verified.

## Media and package handoff

`bm42.bmp` is a small 32 × 25 bitmap beside the title, not a recovered interview
photograph. Its PNG has exactly the same decoded RGBA pixels as the original.
The object position and underline/bold marks remain in the runtime paragraph.
No additional figures were observed in these mapped CD topics; this makes no claim
about illustrations present in the printed magazine or the book.

| Output | Contents |
| --- | --- |
| `build/cd1-articles/8802030/single/content/` | Eight runtime files: one article, two sections, one PNG, two Markdown previews, issue/catalog/media/manifest documents. |
| `build/cd1-articles/8802030/combined/content/` | 34 runtime files: three articles, six sections, 417 blocks, 915 paragraphs, 23 media occurrences, and six previews. |
| `build/cd1-articles/8802030/body.txt` | Exact paragraph text projection for the interview body. |
| `build/cd1-articles/8802030/blocks.json` | Block evidence and 27 interview turns. |
| `build/cd1-articles/8802030/provenance.json` | Source records, native/RTF boundaries, metadata comparison, conversion evidence, turn associations, and preview byte ranges. |

Standalone validation completes before composition. The combined package retains
the two older articles and previews byte-for-byte. Their two deferred media assets
remain unavailable, with explicit records. All 39 February TOC entries remain in
source order; three now link to prepared articles and 36 remain unmatched in the
runtime package. The separate metadata audit supports another unprepared match
and one unresolved candidate; runtime preparation does not change that distinction.

The earlier two-article packages and historical coverage report are not overwritten.
This preparation record establishes the newer status: **three of February's five
indexed targets are prepared**. `8802184` and `8802180` remain unprepared, and many
TOC entries still have no CD-index match. Complete printed-issue coverage is not
claimed. Physical comparison and publication decisions remain pending.

## Reproduce and validate

```sh
make restore-toc-snapshot
make prepare-cd1-interview
PYTHONPATH=src python3 -m unittest discover -s tests -p test_cd1_interview.py -v
make check
```

The command requires the original private MVB/RTF/probe files, imported CD indexes,
historical TOC inputs, and the reviewed two-article package. ImageMagick converts
the bitmap. Rebuilds compare with the tracked record before replacing generated
outputs; `--write-record` is reserved for an explicitly reviewed new result.
The eight interview checks cover native boundaries, every source byte/run/mark,
multi-paragraph answers, changed formatting, pixel equality, protected preview
content, standalone relocation, combined-package preservation, and the separation
of owner-provided bibliography from CD metadata.

Subsequent checkpoint: [12b.2 — Turbo C editor](CD1-EDITOR-8802184.md) is now
complete, followed by [12b.3 — Turbo Pascal graphics](CD1-GRAPHICS-8802180.md).
The subsequent [12c issue handoff](CD1-ISSUE-1988-02.md) is complete;
see [PLAN-CD1](../PLAN-CD1.md) for the current task. Backup/restore
remains a separate deferred task and does not block content preparation.
