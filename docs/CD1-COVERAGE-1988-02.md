# CD1 February 1988 coverage audit

Step **12a is complete**. The [machine-readable report](../data/catalog/issue-coverage/cd1-1988-02.json)
retains all **39 TOC entries**, in source order with persistent IDs and hierarchy,
and **five indexed CD references / 11 index occurrences**. All five reference
hashes resolve in the checksummed MVB context table. Two articles are prepared;
three indexed targets remain unprepared. No new article bodies were recovered.

| CD reference | TOC entry suffix | Title evidence | Relationship | Preparation |
| --- | --- | --- | --- | --- |
| `8802030` | `0031` | CD: `CP/M의 게리 킬달`; TOC includes the series prefix `유명한 프로그래머를 만났읍니다(5) : ` | New metadata match, with this specific prefix comparison | Unprepared |
| `8802065` | `0035` | CD: `유닉스란 무엇인가`; TOC adds `특집 : ` and `?` | Existing pilot match | Prepared; print review pending |
| `8802114` | `0021` | `스펠링 체커`, exact title | Existing second-article match | Prepared; print review pending |
| `8802180` | `0026` candidate | TOC: `터보 파스칼 한글 그래픽스 툴`; CD: `터보 파스칼 한글 그래픽 툴` | Unresolved title variant; no confirmed link | Unprepared |
| `8802184` | `0027` | `터보 C로 작성한 에디터`, exact title | New metadata match | Unprepared |

Each TOC ID begins `maso-1988-02-toc-`. All eleven CD occurrences explicitly
label February 1988. The new matches use issue labels and unique title evidence;
reference page suffixes are not used to decide matches. Authors, end pages, and
printed article boundaries are not established by this audit.

The TOC population comprises four section headings and 35 article candidates:
four supported matches, one unresolved candidate, and **30 article candidates
without an index match**. Including the four headings, 34 entries have no index
match. Two article candidates are prepared and 33 are unprepared. The report
retains every one, including news, reader material, and other unmatched entries.
It does not silently remove them from an issue catalog.

## What the report establishes

- The TOC import reproduces from its original source snapshot and persistent
  identity registry. February's complete source section also matches the live TOC.
- All three CP949 index files reproduce the imported entries and grouped
  references. Selection includes targets attributed by either an explicit issue
  label or a reference's inferred month, retaining all their occurrences and
  exposing conflicts. Reference suffixes alone cannot confirm a TOC match.
- Native context offsets are recorded from the checksummed MVB. A resolved hash
  is navigation evidence, not proof of printed page numbering or article boundaries.
- The existing combined package matches its reviewed hashes and passes standalone
  v1 validation: 39 TOC entries, two articles, four sections, and 30 runtime files.
  Prepared status comes from those validated articles, not an assumed extraction.
- The local preservation inventory matches its recorded checksum. This is the
  completed step 11a evidence; independent backup/restore is still pending.

The report covers February references **discovered in the three imported indexes**.
It does not establish that no additional February content exists among unindexed
native targets, linked topics, attachments, or physical magazine pages. A missing
index match means “not yet matched,” not “absent from the CD.” The graphics-tool
title difference needs further source evidence; neither spelling is corrected.
The two new relationships are audit metadata and have not been inserted into
the existing runtime packages. No publication decision follows from this report.

## Reproduce

```sh
make audit-cd1-issue
PYTHONPATH=src python3 -m tools.audit_cd1_issue --check
PYTHONPATH=src python3 -m unittest discover -s tests -p test_cd1_issue_coverage.py -v
```

The first command writes only the tracked metadata report; `--check` writes
nothing. The commands require the existing private sources/imports, combined
package, and local inventory. They do not invoke recovery or package builders.

The reviewed import uses TOC SHA-256
`7d4386d31559383e8ddf14ca60dcaa3464aef52cf4d3ac50ca5a993ab422e34e`.
When the working TOC differs, the audit reads that historical snapshot from
Git blob `e9db6b0e2889002a1159187bb6100d5f0d9f2d09` and verifies its SHA-256.
It also rejects any difference in February's current source section. Keep Git
history available when reproducing against an expanded working TOC.

## Next bounded tasks

**12a.1 — expanded TOC validation/import** can proceed while backup is pending.
The owner's unstaged additions cover 1991–1993; the current headings contain two
`93.10` sections and no `93.09`. Establish the intended issue from source evidence
before assigning identities or importing. Then extend the import period, preserve
existing IDs, and update source-snapshot handling/tests without rewriting the
provenance of already prepared articles. The additions are untouched by this audit.

**12b.1 — recover `8802030` only**, after step 11b: map its native and RTF topic
boundaries, identify all linked content and media, account for every source byte,
retain ordered structure/runs, and build a standalone package. Check title/byline
evidence and article boundary uncertainty without labeling it print-verified.
Combine it with the existing two articles only after standalone validation.

Later bounded batches can handle `8802184` and then `8802180`, retaining the latter's
unresolved TOC relationship until evidence supports a decision. Do not treat these
three targets as a complete printed issue. Step 12c must report unmatched TOC
entries and any subsequently discovered CD content explicitly. Backup/restore,
physical comparison, deferred media repair, CD2/CD3, and the UI retain their
separate scopes.
