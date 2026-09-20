# CD1 non-Symbol font-declaration review — checkpoint 17a

This checkpoint audits seven remaining candidates with unreviewed non-Symbol
fonts. Six support source-bound policies; one remains deferred because a byte
sequence in a code listing is ambiguous. Five fixed samples prepare successfully.
The 16b combined handoff remains **982 articles across 72 issues** until the next
retry/reconciliation checkpoint integrates these standalone results.

## Decisions from complete source evidence

All **14 associated topics** reproduce their original 15a recovery under the old
policy. The audit inspects **799 unsupported runs**, including **258 non-ASCII
runs**. The six accepted candidates account for **703 runs**, including **222
non-ASCII runs**. Source topic hashes, positions, associations and the complete
source RTF hash bind each decision; font names alone do not authorize decoding.

| Reference | Font policy | Unsupported runs | Decision and evidence |
| --- | --- | ---: | --- |
| `8910172` | Tms Rmn (1): ASCII | 1 | Fourteen spaces following an illustration in a pointer-assignment listing. |
| `9010204` | fixedsys (64): CP949 | 205 | C listing, compiler notes and Korean comments agree in context. |
| `9107124` | FIXEDSYS (73): CP949 | 28 | C++ class listing with Korean private/public member annotations. |
| `9108302` | @굴림체 (72): ASCII | 1 | Opening parenthesis before `Lock`, paired with the following closing parenthesis. |
| `9304171` | Helvetica (7): CP949; Helv (0): ASCII | 99 | Korean outline-font introduction/body and one ASCII Helv run. |
| `9306300` | Helvetica (7): CP949 | 369 | Korean presentation/EMS/VGA text and listing context. |
| `9309201` | No approved policy | 96 | One ambiguous code-listing run prevents approval of the whole article. |

The accepted CP949 runs reproduce their bytes exactly and agree with the EUC-KR
repertoire. Competing CP1252, CP437 and Johab interpretations or failures remain
in private evidence, alongside decoded candidates, raw bytes and surrounding
paragraphs. ASCII spacing and punctuation retain exact bytes. The vertical-font
declaration is preserved; this is a text interpretation, not verification of
rotated glyph appearance or physical page layout.

The deferred article is a useful counterexample to trusting round-trips alone.
In topic 2888, paragraph 62, run 1, the byte sequence `a4 47 45 54` contains a
high byte before an apparent ASCII `GET` keyword. CP949 accepts the bytes and
round-trips, but consumes `47` (ASCII `G`) into an extended Hangul character.
EUC-KR rejects the sequence; single-byte interpretations preserve `GET` but leave
the preceding glyph unexplained. Context does not justify selecting or repairing
that glyph, dropping a byte, or reconstructing the listing.

Consequently, **all 96 unsupported runs in `9309201` remain retained**, including
otherwise plausible runs. Its complete original recovery is preserved unchanged,
and no policy or runtime package is generated for it. Independent source-byte
checks use Latin-1 solely as reversible byte transport, with explicit
`retained_bytes_not_decoded_text` status. Candidate interpretations are diagnostics,
not approved article text. The unresolved run, alternatives and neighboring
paragraphs remain recorded for a later bounded investigation.

## Fixed sample and preservation checks

The five samples are `8910172`, `9010204`, `9107124`, `9108302` and `9304171`,
covering all five newly reviewed declarations plus the mixed Helvetica/Helv case.
All five prepare with review exceptions. They preserve **2,159 paragraphs, 1,350
blocks, 380,446 RTF bytes, 1,842 text runs and 67 object occurrences**. Five
standalone and five partial sample issue packages validate under unchanged schema v1.

Only the reviewed unsupported runs, their paragraph text projections and their
corresponding issue records change. Existing text, formatting, whitespace, source
spans, accounting, metadata, article boundaries and object positions stay exact.
The 14a auxiliary dispositions and recovered text remain unchanged. There are
**65 distinct media resources: 56 available and nine deferred**; all 56 available
bitmaps preserve source pixels. Deferred conversions remain recorded for later
resolution. No semantic reclassification or font-layout fidelity is claimed.

Normal audit/sample reruns reproduce both tracked summaries exactly. An isolated
fresh rebuild reproduces **all 93 article runtime files byte for byte**, with
identical source checks and outcomes. **256 regression tests pass without skips**,
including eight new declaration-policy/artifact tests and the historical source,
package, media, schema, Markdown, resume and static base-URL checks.
The six accepted policies include
`9306300`, whose complete source decoding is audited but whose packaging is left
for 17b. That checkpoint will carry the five samples forward, attempt the remaining
supported candidate and reconcile combined coverage. `9309201`, four Symbol-font
cases and 37 existing-codec failures remain outside that retry scope.

## Commands and private evidence

```sh
make review-cd1-font-declarations
make retry-cd1-font-declaration-sample
make retry-cd1-font-declaration-sample FONT_ARGS=--verify-fresh
```

Use the converter/font environment pinned by 16b. `FONT_ARGS=--write-record`
establishes each record; normal reruns require exact equality. The fresh check
uses a separate temporary private root and compares every article runtime file,
source check and outcome with the recorded sample.

- [Audit summary](../data/catalog/batch-runs/cd1-font-declaration-review.json)
  explicitly separates accepted and deferred references. Private
  `build/cd1-font-declaration-review/stages/review/<hash>/` retains seven recovery
  records, all 799 run/context records and six source-bound policies.
- [Sample summary](../data/catalog/batch-runs/cd1-font-declaration-sample.json)
  binds the audit and runner. `build/cd1-font-declaration-sample/` retains stages,
  durable checkpoints, packages and conversion diagnostics.
- Each package's `content/` directory remains the static handoff. All runtime
  paths remain relative to the chosen base URL. Extraction evidence is separate
  from runtime content, and output guards protect all historical and audit roots.

Full text, previews, images and per-run evidence remain private. Original decoder,
shared policies, schema, reports and combined packages remain unchanged. Physical
comparison, TOC matching, scans, media repair, backup/restore, CD2/CD3, UI and
publication/access remain separate work.
