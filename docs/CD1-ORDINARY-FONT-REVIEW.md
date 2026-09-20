# CD1 ordinary-font non-ASCII review — checkpoint 16a

Five of the 53 remaining font/decoding failures contain non-ASCII runs in fonts
whose ASCII use was reviewed in 15a. This checkpoint reviews their complete source
associations and validates four fixed sample packages. The current 15b combined
handoff remains **977 articles across 72 issues**; sample successes will enter
combined coverage in 16b.

## Evidence and policy

All **ten source topics** reproduce their original 15a recovery exactly under the
old policy. The new policy recovers **3,425 previously unsupported runs**, comprising
3,407 ASCII runs and **18 non-ASCII runs**. All existing decoded text stays exact.

| Reference | Font | Non-ASCII runs | Context supporting the interpretation |
| --- | --- | ---: | --- |
| `8905226` | Courier New (13) | 8 | Contiguous assembly string rows form a box with corners, junctions and borders. |
| `9201260` | MS Sans Serif (26) | 4 | Korean spline prose/captions agree with adjacent Korean headings and figure positions. |
| `9202208` | Helv (0) | 1 | Korean SMM prose agrees with the preceding mixed-font library heading. |
| `9203182` | Courier New (13) | 4 | Korean comments and banner text fit the C listing and embedded-object positions. |
| `9207134` | MS Sans Serif (26) | 1 | A Korean listing caption names the `isAT` function in the following listing. |

Strict CP949 decoding and re-encoding preserve every source byte. EUC-KR produces
the same interpretation and bytes for these runs; no CP949 extension characters
are needed. The audit reconstructs encoded bytes independently from the RTF spans,
checks complete topic accounting, and retains competing CP1252, CP437 and Johab
interpretations (or strict decoding failures) alongside surrounding paragraphs.
The coherent Korean text and box geometry support the selected interpretation;
a font name or successful round-trip by itself would not justify it.

The policy is limited to these **five exact source associations and three explicit
font IDs**. The source RTF hash and each topic's hash, offsets and length remain
bound to the policy. No global font mapping is changed. Previously decoded runs,
whitespace, formatting, source spans, metadata, article boundaries and object
positions remain identical. Only reviewed unsupported runs, their paragraph text
projections and their corresponding issue records change. Unrelated errors cannot
be cleared. There is no replacement character, heuristic fallback or symbol-font
mapping. Physical-magazine comparison remains pending.

## Four fixed sample articles

The sample contains `8905226`, `9201260`, `9202208` and `9203182`, covering all
three fonts and both Korean text and box drawing. All four prepare with review
exceptions. They preserve **6,181 paragraphs, 4,654 blocks, 401,251 RTF bytes,
5,708 text runs and 106 object occurrences**. Four standalone packages and four
partial sample issue packages validate under unchanged schema v1. Reviewed 14a
auxiliary dispositions and recovered auxiliary text are unchanged.

The packages account for **106 media references: 44 available and 62 deferred**.
All **40 available bitmap resources preserve source pixels**. Deferred conversion
failures remain recorded; this checkpoint does not repair images. Source font
formatting and code whitespace are preserved, while semantic classification and
physical layout still carry the existing review limitations.

Normal audit and sample reruns reproduce their tracked summaries. An isolated
fresh rebuild reproduces **all 72 article runtime files byte for byte**, together
with identical source checks and outcomes. **243 regression tests pass**, including
seven new scope, malformed-byte/control rejection, preservation, protected-output
and artifact checks. Historical source, package, schema, Markdown, resume and
static base-URL checks also pass.

`9207134` has a complete source decoding audit but has **not** been packaged here.
Step 16b will process that remaining candidate, carry the four samples forward,
compose combined issue packages and audit current coverage. The other 48 font
cases, other extraction exception classes and TOC matching are separate work.

## Commands and private evidence

```sh
make review-cd1-ordinary-fonts
make retry-cd1-ordinary-font-sample
make retry-cd1-ordinary-font-sample FONT_ARGS=--verify-fresh
```

Use the same converter/font environment as 15b. `FONT_ARGS=--write-record`
establishes the audit or sample record; normal reruns require exact equality.

- [Audit summary](../data/catalog/batch-runs/cd1-ordinary-font-review.json) binds
  the 15b coverage record, original 15a audit, implementation and fixed sample.
  `build/cd1-ordinary-font-review/stages/review/<hash>/` retains the source-bound
  policy, five complete recoveries and private per-run/context/alternative evidence.
- [Sample summary](../data/catalog/batch-runs/cd1-ordinary-font-sample.json) binds
  the review and retry implementation. `build/cd1-ordinary-font-sample/` retains
  independent stages, durable outcomes, conversion diagnostics and runtime packages.
- Each package's `content/` directory remains the static handoff. Catalog, article,
  preview and media paths remain relative to the configured base URL. Detailed
  source evidence is separate from runtime content.

The new runner rejects output roots overlapping historical batch, association,
font and review roots. Historical decoder code, shared policies, schema, reports
and handoffs remain unchanged. Full text, previews, images and contextual evidence
stay private. Publication/access, UI, scans, physical review, backup/restore,
deferred media repair and CD2/CD3 remain separately scoped.
