# CD1 Symbol-arrow recovery — checkpoint 18b

Article `9208198` now prepares with its nine Symbol arrows and 95 literal spaces
preserved. The source-bound adapter handles only the eight runs reviewed in
[18a](CD1-SYMBOL-REVIEW.md). The full article, standalone package and partial
August 1992 issue package validate under the unchanged v1 content contract.
Combined 17b coverage remains **988 articles across 72 issues, 92 failures and
eight blockers** until the separate 18c integration audit.

## Glyph and source policy

| Source byte | Unicode output | Count |
| --- | --- | ---: |
| `ac` | `←` U+2190 | 2 |
| `ad` | `↑` U+2191 | 1 |
| `ae` | `→` U+2192 | 6 |
| `20` | ordinary space U+0020 | 95 |

These **104 encoded bytes across eight runs** occur in body topic 2111. Topic
2110 supplies the introduction. The arrow mapping follows the
[pinned Adobe Symbol reference](../data/reference/adobe-symbol.txt), with SHA-256
`deb78ca840a429311939b9d165890873f71fb23ef223ceeb144a6c6d641a7e52`.
Its applicability to CD1 is the source-bound inference recorded in 18a; physical
magazine verification remains pending.

The reference offers two Unicode space alternatives. This policy retains literal
RTF spaces as U+0020, without converting them to nonbreaking spaces or reflowing
the annotation. In particular, the two-left-arrow run preserves **94 leading
spaces and one trailing space**. The Markdown preview represents those edge
spaces as numeric `&#32;` entities under the existing exporter. Markdown does
not promise original page layout; exact paragraph/run formatting remains in the
preservation data and ordered text remains in the structured package.

The new encoding name is `cd1_symbol_arrows_v1`. It is an explicit glyph adapter,
not a registered Python codec or a CP949 fallback. Original encoded bytes,
source spans, byte hashes and font formatting remain on every recovered run.
Only the eight approved runs, their paragraph text projections and corresponding
unsupported-run issues change. Neighboring source text and code remain exact.

The policy binds the article reference, both complete source-topic associations,
reviewed paragraph/run positions and original run evidence. The adapter rejects
other bytes, glyphs, articles, source changes and unrelated recovery errors.
The two conflicting Symbol articles (`9205400a`, `9205403`) remain deferred.

## Implementation and validation

The separate [glyph adapter](../tools/batch/symbol_arrows.py) first invokes the
frozen decoder, then applies only exact reviewed substitutions. Its independent
checker reconstructs bytes from the original RTF spans, checks each glyph against
the pinned reference, and requires inverse mapping to reproduce every byte.
Temporary Latin-1 transport is confined to that byte reconstruction; it is never
published as recovered article text. Complete source accounting, paragraph text
projections and unchanged run formatting are checked separately.

The isolated [article pipeline](../tools/batch/symbol_arrow_pipeline.py) preserves
the frozen stage sequence. Its process method adds the exact-job restriction,
records the glyph policy and invokes the adapter for article recovery. Auxiliary
recovery, semantics, media, Markdown and package construction retain their prior
behavior. Its identity binds the adapter, pipeline, frozen stages, 18a sample and
source policy. No shared decoder, policy, schema or historical record is changed.

The prepared article retains:

- **1,696 paragraphs, 535 blocks and two sections** from two source topics.
- **181,856 RTF bytes, 1,346 text runs and 24 object occurrences**.
- **15 available bitmaps**, each with source-equivalent pixels, and nine explicitly
  deferred WMF resources. Image repair remains separate.
- **22 runtime files**, including two Markdown previews. Both linked auxiliaries
  retain their separate recovery and prior dispositions.

Normal reruns reproduce the tracked sample record exactly. An isolated fresh
rebuild reproduces all 22 runtime files byte for byte, with identical source
checks and outcomes. All seven new policy/source/artifact tests pass, including
rejection of changed arrows, spaces, font labels, source evidence and policy
scope. **All 276 regression tests pass without skips**, including historical
source/package checks, Markdown, schema and nested base-URL validation.

An initial draft expected an `end_exclusive` field in a source association that
actually stores offset and length. The corrected adapter derives the endpoint;
the failed draft checkpoint remains private under its earlier implementation
identity. The successful record below binds the corrected implementation.

## Commands and handoff

```sh
make retry-cd1-symbol-arrows
make retry-cd1-symbol-arrows FONT_ARGS=--verify-fresh
```

`FONT_ARGS=--write-record` establishes the record. Normal runs require exact
equality; fresh verification builds under an isolated private directory.

The [sample summary](../data/catalog/batch-runs/cd1-symbol-arrow-sample.json)
records source counts, policy hash, durable checkpoints, packages and runtime
hashes. Detailed recovery and media remain under `build/cd1-symbol-arrow-sample/`.
Package `content/` directories are the static handoff, with paths relative to
the chosen base URL. Detailed source evidence stays outside the runtime package.

Checkpoint **18c** will carry this article and the validated 18a punctuation
sample (`9210202`) into combined issue packages. It must preserve all prior
outcomes, validate unchanged earlier content and independently audit both new
articles before updating coverage. The two Symbol font/context conflicts,
`9309201` and 37 existing-codec failures remain separate investigations.

Full text and media remain private. TOC matching, physical review, scans, image
repair, backup/restore, CD2/CD3, UI and publication/access remain separate work.
