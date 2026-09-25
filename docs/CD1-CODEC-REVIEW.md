# CD1 existing-codec review — checkpoint 19a

All **37 remaining existing-codec failure articles** are reviewed across **70
source topics, 185 unsupported runs and 10,504 encoded bytes**. Five articles
support policies limited to exact DOS box-drawing literals. Three fixed samples
prepare successfully. Two articles need a representation for multibyte characters
split across fonts; 30 retain mixed or ambiguous source bytes.

Combined 18c coverage remains **990 prepared articles across 72 issues, 90
failures and eight blockers** until the separate 19b integration audit. This
checkpoint does not claim that the remaining source anomalies are repaired.

## Findings and decisions

The original failure is CP949 decoding in 184 runs: 164 illegal multibyte
sequences and 20 incomplete sequences. One additional run in `8807052` uses an
unsupported Courier New font and contains two spaces. That article's separate
CP949 failure still prevents preparation; no partial repair is published.

| Declared font | Unsupported runs | Existing codec |
| --- | ---: | --- |
| Arial (4) | 116 | CP949 |
| Fixedsys (15) | 50 | CP949 |
| 굴림체 (5) | 18 | CP949 |
| Courier New (13) | 1 | Unapproved in this article |

| Article decision | Articles | Runs |
| --- | ---: | ---: |
| Exact OEM literal policy supported | 5 | 30 |
| Cross-font character representation deferred | 2 | 4 |
| Mixed or ambiguous source retained | 30 | 151, including the additional font run |

Every original full recovery reproduces exactly under the unchanged decoder.
Independent retained-byte checks account for each complete topic and reconstruct
every encoded run from RTF. They explicitly use byte transport without approving
glyphs. Private evidence includes each original run, source spans/hashes, active
codec, font/formatting, surrounding paragraphs, strict decoding error interval
and competing CP949, EUC-KR, CP437 and CP1252 attempts. A candidate decoding that
round-trips is never sufficient to approve it.

### Exact DOS literal policies

| Reference | Reviewed source role | Runs | Validation sample |
| --- | --- | ---: | --- |
| `8901200` | Pascal frame edges and corners | 8 | Prepared |
| `8902178` | Pascal frame edges and corners | 8 | Policy only; retry in 19b |
| `8903170` | Pascal frame edges and corners | 8 | Policy only; retry in 19b |
| `8911214` | Assembly string borders | 5 | Prepared |
| `9206396` | Horizontal marker in a printf literal | 1 | Prepared |

The Pascal calls place horizontal glyphs along the two y boundaries, vertical
glyphs along the two x boundaries, and individual corner glyphs at the matching
coordinates. The assembly strings place a vertical border at both ends. The
printf literal contains three repeated horizontal-line bytes beside `<`.
These specific programming roles support the glyph interpretations.

The [Microsoft CP437 mapping hosted by Unicode](https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/PC/CP437.TXT)
maps the seven reviewed bytes to `│ ║ ┐ └ ─ ┘ ┌`. A
[pinned copy](../data/reference/microsoft-cp437.txt), retrieved 2026-09-25, has
SHA-256 `6bad4dabcdf5940227c7d81fab130dcb18a77850b5d79de28b5dc4e047b0aaac`.
The [Unicode distribution license](../data/reference/unicode-license-v3.txt) is
included unchanged. All 256 reference entries match Python's CP437 mapping.
The upstream DOS EOF marker is retained in the file and ignored only by the table
parser. Git attributes preserve both reference files byte for byte.

Applying that mapping is a source-bound inference from literal bytes and code
context. It does not establish the original code page for the whole article or
constitute physical-magazine verification. Alternative mappings can round-trip
the same bytes while yielding different glyphs. Ordinary Korean text continues
to use its existing codec.

The five policies cover **30 runs, 1,073 encoded bytes and 37 box glyphs**. Each
binds the article, complete source-topic associations, paragraph/run positions
and original run evidence. Only ASCII plus the reviewed box-byte subset is
accepted, with additional checks for each literal's structure and glyph counts.
Unreviewed articles, controls, fonts, literals and already decoded text are rejected.

### Deferred split characters and ambiguous bytes

`8901110` splits the bytes of the Hangul syllable `를` between Arial and Fixedsys.
`9103202` splits the bytes of the fullwidth exclamation mark `！` between the same
fonts. Joining each adjacent pair yields strict CP949 text that also reproduces
the EUC-KR bytes. Both original run formats are retained. Joining runs would lose
the font boundary; assigning the whole character to either run would introduce
a formatting decision. These two cases therefore remain a separate representation
task, with candidate text and the exact boundary recorded privately.

The other 30 articles retain every unsupported run and its original issue. Some
contain plausible DOS bytes alongside Korean bytes in the same run, or isolated
high bytes in prose/comments. A whole-run CP437 fallback would reinterpret Korean
text; deleting, replacing or completing bytes would alter the source. No such
fallback or repair is introduced. Per-article decisions and competing interpretations
are recorded in the private review's `jobs.json`, `runs.json` and `boundaries.json`.

## Sample validation and preservation

The three samples preserve **3,767 paragraphs, 634 blocks, 332,886 RTF bytes,
3,209 text runs and 27 object occurrences**. Only **14 approved runs** change,
containing 609 encoded bytes and 21 box glyphs. Original bytes, source spans,
hashes and font/paragraph formatting remain exact. Neighboring text and existing
code errors are preserved. Each new run declares its actual `cp437` encoding.

The [isolated adapter](../tools/batch/oem_runs.py) invokes the unchanged decoder
first, then substitutes only approved runs. The independent checker reconstructs
RTF spans, requires inverse bytes, verifies reference glyphs and checks the exact
policy positions and formatting. The separate article pipeline retains the frozen
stage sequence; only its exact-job restriction, recorded run policy and article
recovery call differ. Auxiliary recovery, semantics, media, Markdown and package
construction retain their earlier behavior. No shared policy or schema changes.

All standalone and partial-issue packages validate. All 24 distinct available
bitmap resources preserve source pixels. The 27 occurrences refer to 25 distinct
resources; `bm1829.wmf` remains explicitly deferred. Detailed media evidence and
all auxiliary dispositions remain preserved separately.

Normal audit/sample reruns reproduce both tracked records exactly. An isolated
fresh rebuild reproduces **all 46 runtime files byte for byte**, with identical
source checks and outcomes. All nine new policy/reference/artifact tests pass,
including literal spacing in Markdown and rejection of altered glyphs, source
evidence, formatting and scope. All **291 regression tests pass without skips**,
including historical source, package, Markdown, schema and base-URL checks.

## Commands and next checkpoint

```sh
make review-cd1-codecs
make retry-cd1-oem-sample
make retry-cd1-oem-sample FONT_ARGS=--verify-fresh
```

`FONT_ARGS=--write-record` establishes the records. Normal reruns require exact
equality; fresh verification uses an isolated private build directory.

- [Review summary](../data/catalog/batch-runs/cd1-codec-review.json) binds the 18c
  coverage, original review, reference files and all private audit outputs under
  `build/cd1-codec-review/`.
- [Sample summary](../data/catalog/batch-runs/cd1-oem-sample.json) records the three
  outcomes, independent source checks, runtime hashes and checkpoints under
  `build/cd1-oem-sample/`.

Checkpoint **19b** will retry `8902178` and `8903170`, carry the three validated
samples, and audit combined coverage against 18c. The two cross-font characters,
30 ambiguous-source articles, two Symbol conflicts and `9309201` remain separate.

Full text, previews, media and detailed source evidence stay private. Package
`content/` directories remain the static handoff, with paths relative to the
chosen base URL. Physical review, TOC matching, scans, image repair, backup/restore,
CD2/CD3, UI and publication/access remain separate work.
