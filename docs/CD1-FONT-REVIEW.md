# CD1 font audit and ASCII-only retry sample — checkpoint 15a

The 14b exception queue contains 86 font/decoding failures. This checkpoint audits
all associated source topics and validates six fixed retries using additional
ordinary-font ASCII mappings. Original decoding code, shared policy, schema and
13d/14a/14b records remain unchanged. New results live in separate private roots.

## Complete source audit

The audit checks **163 topics**, including **13 topics beyond the 150 reached by
historical recovery**. Every retained recovery prefix matches the independent
source recovery exactly. All source bytes remain accounted for, including runs
that still cannot be interpreted. Retained bytes are reconstructed independently
from RTF spans before classification; Latin-1 is used only as a reversible byte
transport in this check, never as a decoding policy or published text.

| Classification of unsupported runs | Runs |
| --- | ---: |
| Reviewed ordinary-font ASCII | 3,667 |
| Unreviewed font or symbol glyph | 813 |
| Existing codec failure | 184 |
| Non-ASCII/control bytes in an additional ordinary font | 18 |
| Total | 4,682 |

**33 candidates** have only reviewed ASCII font failures across their complete
source associations; **53 remain deferred**. The run counts above are not article
counts: deferred articles can contain both safe ASCII runs and unresolved runs.

The reviewed declarations are Helv (0), Times New Roman (3), Courier New (13),
MS Sans Serif (26), COURIER NEW (46) and LinePrinter (48). Each added mapping is
restricted to ASCII printable characters and tab, tied to exact article topics
and source hashes. No global font mapping is changed. Symbol and unreviewed fonts
remain unsupported even when their byte values fall in the ASCII range. No
replacement characters, alternate-encoding fallback or guessed glyph mappings
are permitted. Ordinary font names alone do not authorize non-ASCII decoding.

## Fixed six-article sample

| CD reference | Selected concern |
| --- | --- |
| `8803110` | Courier New ASCII layout |
| `8804096` | Times New Roman space |
| `8910268` | Uppercase Courier New ASCII listing |
| `9012137` | Helv ASCII text |
| `9106274` | MS Sans Serif spaces |
| `9205208` | LinePrinter tab and Times New Roman |

All six prepare with review exceptions. They contain **2,927 paragraphs, 1,839
blocks, 548,953 source RTF bytes and 3,488 text runs**, with 50 object occurrences.
All 35 available bitmap derivatives preserve source pixels. Six WMF resources in
`8910268` remain deferred with conversion diagnostics; no image repair is attempted.

Six standalone packages and six partial sample issue packages validate under
unchanged schema v1. The retry checks the entire recovered topic against the
previous audit, allowing only the reviewed unsupported-to-ASCII replacements and
corresponding paragraph text/issue updates. Existing text, font formatting,
whitespace, source spans, accounting, metadata and article boundaries stay exact.
Auxiliary dispositions and recovered auxiliary text retain the 14a policy.

Font-family layout is retained as source evidence; this checkpoint does not add
semantic block-classification rules for the newly accepted fonts. Generic semantic
review and physical-magazine comparison remain pending.

The six successes add available standalone text beyond 14b's 944 articles. The
**72 combined current handoffs remain the 14b packages** until step 15b reconciles
these six samples with the remaining 27 eligible retries. The 53 deferred font
cases and other exception classes are not retried here.

Normal audit and sample reruns reproduce both tracked summaries. A fresh isolated
rebuild reproduces **all 84 article runtime files** byte for byte. **230 regression
tests pass**, including seven new checks for ASCII policy limits, symbol/control
rejection, unchanged source formatting, protected output roots, the full audit and
all sample packages. Existing source, schema, preservation, interruption/resume and
static-loading checks also pass.

## Commands and private evidence

```sh
make review-cd1-fonts
make retry-cd1-font-sample
make retry-cd1-font-sample FONT_ARGS=--verify-fresh
```

Use the same converter/font environment as 14b. `FONT_ARGS=--write-record`
establishes the reviewed audit or sample record; normal reruns require exact
record equality. The fresh check rebuilds all six articles in an isolated temporary
private directory and compares every runtime file against the recorded sample.

- [Font audit summary](../data/catalog/batch-runs/cd1-font-review.json) binds the
  current exception queue, original pipeline, audit implementation, fixed sample
  and source-bound policy. Private `build/cd1-font-review/stages/review/<hash>/`
  retains full source recovery, every undecoded run, per-job classifications and
  the policy. Reuse verifies the cache manifest and all recorded output hashes.
- [Sample summary](../data/catalog/batch-runs/cd1-font-sample.json) binds the font
  audit and retry implementation. `build/cd1-font-sample/` contains isolated
  stages, durable checkpoints, source checks, packages and conversion diagnostics.
- Each package's `content/` directory remains the static handoff. Serve it below
  the chosen base URL; internal catalog, article, preview and media paths remain
  relative. Detailed source evidence is adjacent to the runtime content.

The retry runner rejects output paths overlapping historical batch, association
or audit roots. Resume verifies recorded source jobs, stage manifests and packages.
The original generic retry command is historical evidence; broader font retries
must use the reviewed font extension in a new private root.

Full text, previews, images and per-run decoding evidence remain private. Deferred
byte sequences and symbol glyphs need their own bounded investigations. TOC matching,
physical comparison, scans, media repair, backup/restore, CD2/CD3, reading-room UI
and access/publication decisions remain separate work.
