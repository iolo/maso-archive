# CD1 frozen-sample validation — checkpoint 13c

This checkpoint exercises the six February regression articles and the nine
additional candidates selected before extraction in the [13a inventory](CD1-PROCESSING-INVENTORY.md).
**13c is complete.** The sample spans ten issues and 1988–1993. It includes unindexed and suffixed
references, interior native context offsets, long code listings, extra fonts,
bitmap/vector media, and a supplement without a numeric opening page.

## Reproduce the validation

```sh
make validate-cd1-batch
make check
```

The validation command uses original checked sources, prepares all fifteen
articles, audits source bytes and bitmap pixels, rebuilds into an empty temporary
root, compares every stage's output hashes, checks compatible resume, and fetches
all issue-package files under two nested HTTP base URLs. It requires local image
converters and localhost server access. Ordinary execution compares the result
with the [reviewed record](../data/catalog/batch-runs/cd1-validation-sample.json);
`VALIDATION_ARGS=--write-record` records a deliberately reviewed new result.

The prepared packages remain under `build/cd1-batch/`, with article and issue
pointer files described in the [runner guide](CD1-BATCH-RUNNER.md). This location
allows compatible results to carry forward into the full-CD pass. Historical
February packages and the 13b record remain unchanged. Text, media, raw spans,
conversion diagnostics and auxiliary recoveries stay private.

## Sample results

| Source reference | Issue | Paragraphs | Blocks | Deferred media |
| --- | --- | ---: | ---: | ---: |
| `1KP6JK` | 1988-04 | 42 | 42 | 0 |
| `8901152` | 1989-01 | 286 | 136 | 28 |
| `9011288` | 1990-11 | 1,894 | 279 | 0 |
| `9105358` | 1991-05 | 224 | 183 | 0 |
| `9209394a` | 1992-09 | 78 | 26 | 0 |
| `9302402a` | 1993-02 | 10 | 10 | 0 |
| `9304310` | 1993-04 | 520 | 416 | 0 |
| `9311000` | 1993-11 | 514 | 514 | 0 |
| `9312167` | 1993-12 | 1,721 | 105 | 0 |

Including February, the packages contain **15 articles, 8,110 paragraphs, 2,388
blocks and 200 distinct media records: 168 available and 32 deferred**. February's
article JSON and Markdown bytes, media dispositions and accepted assets remain
identical to the reviewed baseline. Its four existing WMF exceptions remain
untouched. The 28 additional exceptions belong to the math-library article:
conversion does not retain its source Symbol font, so mathematical glyphs remain
suspect. Diagnostics and source locations are retained; no repair was attempted.

The unindexed article retains ID `cd1:article:native-0e6aae95` and exported source
alias `1KP6JK`. Suffixed references remain distinct. The supplement `9311000`
retains a null page number. Interior context offsets are preserved as source
locations, not mistaken for native header positions or different article starts.

## Changes established by source evidence

The initial 13b runner prepared three of the additional articles. The other six
stopped explicitly on extra font policies, first-line indentation or auxiliary
ownership. Their initial private report remains at
`build/cd1-sample-initial/run-report.json`.

- **Fixedsys encoding:** font 15 uses CP949 under the shared source policy. The
  inspected samples include Korean comments in this font, so blanket ASCII is
  insufficient. Every text run strictly round-trips its original bytes. Reviewed
  February font policies remain authoritative for those articles.
- **Additional fonts:** font 26 in `9105358` and font 95 in `9304310` contain only
  spaces. ASCII permission is bound to those exact source-topic hashes; it does
  not authorize arbitrary glyph interpretation elsewhere.
- **RTF formatting:** first-line indentation (`fi`), tab-stop positions (`tx`) and
  double underline (`uldb`) are retained in structured preservation data, including
  resets and inherited state. No width or missing glyph is guessed.
- **Structure:** contiguous Fixedsys runs retain preformatted layout, internal
  blank paragraphs and tabs. This is a layout decision; code/table/terminal
  semantics and language remain unverified. Supported numbered headings retain
  their levels; an apparent second-level heading without a first-level parent
  stays unresolved. The math-library sample exposed and tests now cover that
  missing-parent case. Recognized titles/bylines and all unclassified paragraphs
  retain their source runs and separate semantic-review status.

These decisions live in the shared pipeline and
[source-bound policy](../data/catalog/batch-profiles/cd1-shared-policy.json), rather
than new per-article scripts. The runtime schema remains v1.

## Auxiliary topics

Links from two articles target author biographies and a series navigation list.
They are recovered separately with exact source spans and token/run accounting:

| Native topic | Role | Paragraphs | Source media references |
| --- | --- | ---: | ---: |
| 30 | Author biography | 5 | 0 |
| 33 | Author biography | 5 | 1 |
| 132 | Series navigation | 11 | 7 |

The **21 auxiliary paragraphs** are additional to the article totals above. Their
raw RTF, recovery, links and dispositions are stored in association-stage evidence;
the source media hashes are checked. Auxiliary media rendering remains deferred.
The biographies and navigation list are not merged into article bodies, and the
series links do not recursively pull in other articles. Other unreviewed linked
content still requires ownership review.

## Checks and remaining scope

A fresh build reproduces all stage output hashes. Compatible resume reuses all
**328 stage calls**, and **524 HTTP file fetches** match beneath both nested URL
prefixes. Source reconstruction covers **992,844 RTF bytes and 7,431 text runs**
for the articles, with a separate audit of the auxiliary topics. All **95 available
bitmap resources** match decoded source pixels.

The validation independently reconstructs each decoded run from original RTF byte
spans and checks its codec, encoded hash and byte round trip. It also verifies
contiguous complete topic accounting, paragraph projections, source identities,
media occurrences, package manifests, bitmap pixel equivalence and conversion
diagnostics. The existing actual-source interruption/resume and decoder-failure
isolation tests remain part of the full suite. New tests cover the added controls,
resets, fixed-pitch grouping, missing heading parents, altered run bytes, ledger
gaps and the retained sample packages.

The sample does not establish complete printed-issue coverage or prove that every
remaining CD1 candidate is supported. Semantic/physical review and unresolved
media remain explicit. The next checkpoint, **13d**, attempts the complete queue
and records every prepared, blocked or failed outcome with retry evidence. Missing
scans, image repair, physical comparison, independent backup verification, CD2/CD3,
publication/access decisions and reading-room UI remain separate.
