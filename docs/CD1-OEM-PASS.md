# CD1 exact-run OEM integration — checkpoint 19b

All five articles approved in [19a](CD1-CODEC-REVIEW.md) are integrated. Audited
coverage is **995 prepared articles across 72 issues**, with **85 failures and
eight blockers** retained out of 1,088 candidates. The two remaining approved
articles were processed; three validated samples were carried unchanged.

## Scope and source preservation

| Reference | Origin | Reviewed literal | Paragraphs | Blocks |
| --- | --- | --- | ---: | ---: |
| `8901200` | Carried 19a sample | Pascal frame edges/corners | 2,208 | 263 |
| `8902178` | New 19b preparation | Pascal frame edges/corners | 2,791 | 242 |
| `8903170` | New 19b preparation | Pascal frame edges/corners | 2,684 | 102 |
| `8911214` | Carried 19a sample | Assembly vertical borders | 1,421 | 315 |
| `9206396` | Carried 19a sample | printf horizontal marker | 138 | 56 |

The five complete articles contain **9,242 paragraphs, 978 blocks, 665,446 RTF
bytes and 8,234 text runs** across nine source topics. Their
existing policies authorize only **30 exact literal runs, 1,073 encoded bytes
and 37 box glyphs**. The decoder, reference mapping, policies and three samples
remain those verified in 19a. Korean text outside the reviewed literals keeps its
existing interpretation. Complete RTF recoveries are compared with the original
15a evidence, changing only those approved runs; independent checks reconstruct
their bytes and preserve source spans and formatting.

All five outcomes remain `prepared_with_review_exceptions`. Physical/semantic
review is pending, and `bm342.wmf` and `bm1829.wmf` retain deferred media records.
Successful extraction does not establish printed-issue completeness or resolve
publication/access permission.

## Combined handoff and validation

The isolated handoff is under `build/cd1-oem-pass/`. Each package's `content/`
directory is the static viewer input, with paths relative to the chosen base URL.
The earlier `build/cd1-symbol-pass/` handoff remains preserved.

The integration checks all prior/current issue packages, exact article/preview/
media bytes, complete source associations, auxiliary dispositions, original
candidate populations and bitmap pixels. The 990 earlier article source audits
are carried forward unchanged; all five added articles receive fresh source
checks. The three carried checks must also match their 19a sample record.

Coverage retains six separate retry histories: the five OEM articles, two Symbol
articles, six declaration-font retries, five ordinary-font retries, 33 ASCII-font
retries and 470 association retries. The 32 unresolved codec-review cases retain
their 19a decisions alongside previous error records; Symbol and declaration-font
annotations remain unchanged.

| Audited measure | Current 19b handoff |
| --- | ---: |
| Prepared articles | 995: 4 prepared, 991 with review exceptions |
| Paragraphs / blocks | 401,728 / 221,931 |
| Accounted RTF bytes / text runs | 66,290,955 / 372,146 |
| Source media | 6,165 |
| Available / deferred / not packaged media | 4,651 / 893 / 621 |
| Pixel-equivalent bitmaps | 3,453 |
| TOC entries linked to available content | 64 |
| Prepared articles without reviewed TOC links | 931 |

The 85 failures comprise 35 font/decoding cases, 35 unsupported RTF cases,
13 inherited-formatting cases, one unterminated paragraph and one document-envelope
case. Eight source-ownership blockers remain separate. The 35 font/decoding cases
include two cross-font characters, 30 mixed/ambiguous codec cases, two Symbol
font/context conflicts and `9309201`'s ambiguous declaration.

Execution produced an **81-file manifest**, SHA-256
`52765a24a05ee6f266b2acc1a3381a6f56de1c9ada81fa4b9acf7f8290931f78`.
The [tracked coverage record](../data/catalog/batch-runs/cd1-oem-pass.json) binds
all 17 coverage tables and has SHA-256
`a687459e798d89e5c5de22aedb0cda4885446e3d093dc2f0252f0e96b7344ec4`.
Complete resume reproduces the execution manifest exactly. A second full audit
reproduces **all 17 coverage tables and the tracked summary exactly**, including
the five source checks, every historical/current package and available bitmap
pixels. All seven new integration tests pass without skips, covering selection,
sample provenance, runtime inventories, preserved content and histories, deferred
decisions, inverse source bytes and literal Markdown spacing. All **298 regression
tests pass without skips**, including historical source/package preservation,
schema, Markdown, nested base-URL and TOC snapshot checks.

## Reproduction and next checkpoint

```sh
make run-cd1-oem-pass
make report-cd1-oem-pass
```

The first report uses `REPORT_ARGS=--write-record`; later reports must reproduce
the tracked record and generated coverage tables exactly. Execution resumes from
verified per-article outcomes and immutable sample pointers. Full text, media,
Markdown previews and detailed source evidence stay in ignored private outputs.

Next, **20a** examines the two characters split across font changes in `8901110`
and `9103202`. Any supported representation must preserve both source fragments
and formatting before isolated full-article samples and later integration. The
30 mixed/ambiguous codec cases, two Symbol conflicts, `9309201`, unsupported RTF,
inherited formatting and ownership blockers remain separate exception classes.
TOC matching, physical review, scans, image repair, backup/restore, CD2/CD3, UI and
publication/access remain separate work.
