# CD1 February 1988 coverage audit

Step **12a is complete**. This document records the original two-article audit
snapshot. The [step 12c issue handoff](CD1-ISSUE-1988-02.md) now supplies a separate
current report with all five indexed targets prepared. The original [machine-readable report](../data/catalog/issue-coverage/cd1-1988-02.json)
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
make restore-toc-snapshot
make audit-cd1-issue
PYTHONPATH=src python3 -m tools.audit_cd1_issue --check
PYTHONPATH=src python3 -m unittest discover -s tests -p test_cd1_issue_coverage.py -v
```

The restore command prepares the separate historical TOC cache; the audit
command writes only the tracked metadata report. Its `--check` mode writes
nothing. The commands require the existing private sources/imports, combined
package, and local inventory. They do not invoke recovery or package builders.

The reviewed import uses TOC SHA-256
`7d4386d31559383e8ddf14ca60dcaa3464aef52cf4d3ac50ca5a993ab422e34e`.
The audit reads the separate, hash-verified historical cache restored from
Git blob `e9db6b0e2889002a1159187bb6100d5f0d9f2d09` and the recorded import inputs.
It also rejects any difference in February's current source section. Keep Git
history available when reproducing against an expanded working TOC.

## Next bounded tasks

**12a.1 — expanded TOC validation/import is complete.** The owner corrected the
September 1993 heading. The 1991–1993 additions are now imported with all earlier
IDs preserved. Historical article and coverage provenance is unchanged; see
[TOC snapshot handling](TOC-IMPORT.md#current-results-and-historical-snapshots).

**12b.1–3 and 12c are complete.** The [issue handoff](CD1-ISSUE-1988-02.md)
preserves all five prepared articles and reconciles their newer evidence with
every February TOC entry. The next bounded task is **13a**, a metadata inventory
of remaining CD1 coverage. Backup/restore, physical comparison, deferred media
repair, CD2/CD3, and the UI retain their separate scopes.

The report's recorded `next_batch.prerequisite` preserves the earlier planning
decision. The current [CD1 plan](../PLAN-CD1.md) supersedes that backup gate;
source coverage findings and prepared-article evidence are unchanged.
