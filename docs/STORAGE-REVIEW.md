# Storage sustainability review — 2026-10-16

The retention rule is unchanged: **preserve unfinished restoration and its
supporting evidence after completion too**. The directory name alone neither
makes a file disposable nor supplies a backup. Follow the
[successive-restoration procedure](STORAGE.md#successive-restoration).

## Scope and corrections

Reviewed all eight `PLAN-*.md` files, the three associated PRDs, current operator
guides, Make targets, and the 131 Python files under `tools/` and `src/`.
Historical manifests, raw OCR, source pins, corrections and archived scripts were
not rewritten. The 67 migrated metadata files still exactly match their original
Git versions; the two pinned CD1 tool sources also remain byte-identical.

| Finding | Correction |
| --- | --- |
| Cover/TOC plans still called retained derivatives rebuildable; other plans used old storage guidance | Added authoritative retention/current-location notes while preserving dated history |
| Four CD builders removed existing results, including after `--verify-existing` | Refuse existing destinations by default; compare actual file bytes without replacement; allow a fresh `--output` for revisions |
| CD finalizers rewrote preserved files during reruns | Accept identical bytes without writing; refuse differing files; verification refuses missing files rather than repairing them |
| Reader snapshots were tied to one hard-coded release, and reusing it did not compare against the current reader | Require explicit release names in the snapshot CLI, compare the current source, support selected-release restore, and recover interrupted snapshots only with matching inputs |
| Active PDF inventory/runtime reads still relied on old aliases | Prefer canonical inputs, with compatibility for unmigrated checkouts; test a new checkpoint without the old input aliases |
| Reader aggregation could rename a compatibility link as its destination | Canonicalize its output before the staged installation |
| The reader test target built into the serving directory | Send its frontend build to `work/validation/reading-room-ui/` |
| CD3 verification serialized the relocated physical path into an old provenance record comparison | Retain the reviewed logical path and verify that it resolves to the actual manifest |
| README still said September had not started | Record September's standalone completion and October as next; the reader still ends at August |

The CD publication changes preserve every earlier result on a mismatch. They do
not turn `archive/` into an immutable filesystem. Progress ledgers can still be
updated by their intended workflows; keep their versions through checkpoints
and independent backups. Do not run multiple writers against one destination.

## Verification performed

| Check | Result |
| --- | --- |
| Python syntax/import entry points | 131 files parsed; all 83 CLI `--help` commands passed |
| Preservation, migration and reader regression checks | 19 tests passed |
| PDF regression suite | 135 tests passed, including interruption/resume, source pins, package/issue validation and preservation |
| Existing September issue | Passed: 43 TOC entries, 37 readable articles, six headings |
| Storage compatibility | All 1,206 moves verified; no missing mapped destinations |
| Metadata and pinned CD1 sources | 67 original metadata files and both pinned tools unchanged |
| Source recovery from original ISOs | All three ISO hashes matched; every extracted file matched its preserved inventory |
| CD2 reference with temporarily recovered sources | Passed: 1,330 candidates, 10,792 output files |
| CD3 reference with temporarily recovered sources | Passed: 968 candidates, 11,346 output files |

The new tests cover actual-byte tampering with an unchanged manifest, extra
unlisted files, preservation of inodes/mtimes during verification, default
refusal by all four CD builders, finalization without writes, distinct reader
releases, interrupted snapshot recovery, and a fresh PDF batch/package using
canonical inputs without legacy aliases. OCR itself is synthetic in these
regression tests; no new recognition or article restoration was performed.

The ISO drill extracted into temporary directories only:

| Source | Verified files | Verified directories |
| --- | ---: | ---: |
| CD1 | 5,828 | 375 |
| CD2 | 1,956 | 102 |
| CD3 | 137 | 14 |

The CD2 checker received the temporary source root, and the CD3 checker received
the temporary extracted tree. Both results then exactly matched their existing
reviewed metadata records. Temporary extraction copies were removed after the
checks; no working source directory or preserved package was replaced.

The earlier full historical test run still has the recorded CD1 source/February
TOC limitations described in [STORAGE.md](STORAGE.md#migration-validation).
This review ran the focused checks above; it does not claim that the entire
historical suite is green. CLI help checks establish that entry points load,
not that every historical workflow can be replayed with current code.

## Recovery limits that remain

- **No independent external backup was established by this review.** The saved
  reader, archives and source ISOs are on the working disk. Keep an independent
  backup and test restoring it; same-disk recovery checks do not prove protection
  against disk loss.
- The `masocd-1/`, `masocd-2/` and `masocd-3/` extracted directories are absent.
  Ordinary source-dependent CD checks still require restoring those directories
  first. The temporary drill proves that the retained ISOs recover their exact
  inventoried contents; the absence was not caused by moving these directories.
- The old July reader integration intermediate is absent. Use the verified
  `reading-room-2026-10-16` release for recovery. The default August export recipe
  still needs that older base; it must not silently use a different reader.
- Four known frozen PDF scripts infer the repository root from their physical
  depth: May's `boundary-review.py`, July's `report-07-prepare.py`, September's
  `typing-segment-b/verify_listing.py` and `six-compatible/survey.py`. Restore an
  isolated original layout/code or supply a reviewed adapter before rerunning
  them. Their original bytes are retained. The survey also needs regenerated
  temporary page images.
- Historical OCR state can pin source code as well as models and input bytes.
  Use its original implementation to resume, or start a separately recorded
  attempt. Do not delete the old attempt or relax fingerprint checks.
- Browser review notes live outside this filesystem and need explicit export.

Machine-readable checks, the temporary-source recovery script and test output
are retained under `archive/migrations/storage-2026-10-16/crosscheck/`.
No additional article was integrated into the reader, and nothing was deployed,
staged or committed during this review.
