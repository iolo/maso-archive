# CD1 Symbol-font review — checkpoint 18a

All four remaining Symbol-font candidates are reviewed across **six source topics,
15 unsupported runs and 125 encoded bytes**. One article supports an exact-source
ASCII policy and prepares as a standalone sample. Two articles retain conflicting
font/context evidence; one retains supported arrow candidates pending a reversible
Symbol decoder. Current combined 17b coverage remains **988 articles across 72
issues, 92 failures and eight blockers** until a later integration audit.

## Evidence and decisions

The RTF declares font 2 as `Symbol` (with a `froman` family classification). All
six topics reproduce the original 15a recoveries under the unchanged policy.
Each original text run is independently checked against its RTF byte spans.

[Microsoft describes Symbol](https://learn.microsoft.com/en-us/typography/font-list/symbol)
as a font with Greek letters, numerals, punctuation and mathematical symbols.
The [Unicode-hosted Adobe Symbol mapping](https://www.unicode.org/Public/MAPPINGS/VENDORS/ADOBE/symbol.txt)
provides the reference byte-to-Unicode candidates used here. A
[complete pinned copy](../data/reference/adobe-symbol.txt), including its original
redistribution notice, has SHA-256
`deb78ca840a429311939b9d165890873f71fb23ef223ceeb144a6c6d641a7e52`.
Applying this reference to CD1 is a source-bound inference supported by the exact
font declaration and context, not a claim of physical glyph verification.

| Reference | Runs | Decision |
| --- | ---: | --- |
| `9205400a` | 2 | Deferred font/context conflict: apparent BASIC keywords map to Greek capitals under Symbol. |
| `9205403` | 1 | Deferred font/context conflict: an apparent Pascal identifier suffix maps to Greek kappa. |
| `9208198` | 8 | Deferred implementation: directional-arrow candidates agree with annotation context but require a Symbol decoder. |
| `9210202` | 4 | Accepted exact-source ASCII policy for digits 1/2/3, comma and semicolon only. |

ASCII-range bytes alone do not authorize ASCII text. In the first two articles,
context suggests program text while the declared font suggests different glyphs.
Neither interpretation is silently selected. Whole original recoveries remain
unchanged; neighboring text, competing candidates and raw bytes are recorded
privately for later review.

For `9208198`, the reference maps bytes `ac`, `ad` and `ae` to left, up and right
arrows. Its eight runs contain nine arrow glyph candidates and 95 literal space
bytes. The mapping offers both ordinary and nonbreaking Unicode interpretations
for a space glyph; both remain in the evidence. The current recovery function
accepts only ASCII/CP949 codecs, and its independent checker requires decoded
text to encode back to the exact original bytes. Using CP949 for these single-byte
arrows would not meet that requirement. This is an implementation limitation,
separate from the two code/font ambiguities. No runtime glyph mapping is approved
for this article in 18a.

The accepted four runs contain nine bytes, drawn only from `2c 31 32 33 3b`.
Their Symbol and ASCII mappings agree, and the listing context supports them.
The policy is bound to `9210202` and its exact source topics. It does not authorize
Symbol letters, spaces, arbitrary punctuation or another article. Font 2 and all
other formatting remain in the recovered output. Existing code mistakes also
remain: this review does not insert missing operators or otherwise repair listings.

## Sample and preservation checks

`9210202` prepares with review exceptions. Its standalone and partial issue
packages validate under unchanged schema v1. They preserve **424 paragraphs,
424 blocks, 90,389 RTF bytes, 380 text runs and three object occurrences**.
All three media resources are available bitmaps with pixels identical to their
sources. The article has **10 runtime files**.

Only the four approved runs, their paragraph text projections and corresponding
unsupported-run issues change. Source spans, byte hashes, metadata, formatting,
article boundaries and object positions remain exact. Auxiliary dispositions
retain the 14a policy. The 11 deferred runs remain unsupported in their original
recoveries; byte accounting uses explicit `retained_bytes_not_decoded_text`
transport checks without claiming decoded glyphs.

Normal audit/sample reruns reproduce both records exactly. An isolated fresh
rebuild reproduces **all 10 runtime files byte for byte**, with identical source
checks and outcomes. **269 regression tests pass without skips**, including seven
new reference-mapping, policy-boundary, source-preservation, deferred-byte and
artifact checks, plus all historical source/package/schema/Markdown/base-URL tests.

## Commands and evidence

```sh
make review-cd1-symbols
make retry-cd1-symbol-sample
make retry-cd1-symbol-sample FONT_ARGS=--verify-fresh
```

`FONT_ARGS=--write-record` establishes each record; normal reruns require exact
equality. The fresh check uses an isolated private output root and compares every
article runtime file, source check and outcome.

- [Audit summary](../data/catalog/batch-runs/cd1-symbol-review.json) binds the 17b
  handoff, original 15a review and pinned mapping. Private `build/cd1-symbol-review/`
  retains all four recoveries, 15 run/context records and the one accepted policy.
- [Sample summary](../data/catalog/batch-runs/cd1-symbol-sample.json) records source
  checks, packages, runtime hashes and durable checkpoints under
  `build/cd1-symbol-sample/`.
- Package `content/` directories remain the static handoff; runtime paths are
  relative to the chosen base URL. Detailed extraction evidence stays separate.

The next bounded checkpoint will implement and validate a reversible, source-bound
arrow mapping for `9208198` in isolated code while preserving frozen history. It
must explicitly handle source spaces, reject unreviewed glyphs and validate byte
accounting, formatting, Markdown, packaging and a fresh rebuild before integration.
The accepted punctuation sample can then be carried forward in a separate combined
coverage pass. The two font/context conflicts, `9309201` and 37 existing-codec
failures remain separate investigations.

Full text, images and detailed source evidence remain private. Original decoder,
shared policies, schema and historical records are unchanged. Physical comparison,
TOC matching, scans, image repair, backup/restore, CD2/CD3, UI and publication/access
remain separate work.
