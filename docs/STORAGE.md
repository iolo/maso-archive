# Storage and preservation

The deciding question is **whether losing a file would lose restoration work or
our ability to explain and reproduce it**, even while an issue is unfinished.
Completion does not make the supporting evidence disposable.

| Location | Contents | Retention |
| --- | --- | --- |
| `metadata/` | Stable IDs, catalog/provenance records, manual decisions, reference tables and storage map | Keep in Git |
| `archive/` | Completed packages **and ongoing restoration**, corrections, mappings, recipes, raw OCR, failed attempts, review evidence, pinned toolchains and saved releases | Preserve and back up outside Git |
| `work/` | Temporary processing and caches with a verified reconstruction path | May discard after the task finishes; never the sole copy of work |
| `dist/` | Assembled readers for serving and deployment | May replace from preserved inputs or a verified release snapshot |

`archive/` means local preserved material; it does not mean published or human
accepted. Keep original `maso-pdf/`, `masocd-*.iso`, extracted disc directories,
`covers/`, `tocs/`, and any other irreplaceable source material as well. This
migration leaves those source locations unchanged. Git does not contain them.

## Issue layout

```text
metadata/
  identities/              stable article and TOC IDs
  catalog/                 provenance and restoration records
  overrides/               reviewed decisions
  reference/               licensed decoding/reference tables
  storage-layout.json      exact old-to-new path map
archive/
  pdf/
    1984-09/
      reference/           completed standalone issue package
      packages/            retained article/batch packages
      restoration/         ongoing work, recipes, raw OCR and corrections
      evidence/            retained rebuilds and validation evidence
    shared/                inventories and work shared across issues
  cd1/                     extraction, reference, packages and evidence
  cd2/
  cd3/
  toc/                     current catalog, restoration and image derivatives
  covers/                  cover inventories and retained derivatives
  toolchains/ocr/           exact OCR runtime used by restoration recipes
  experiments/             retained OCR experiments
  releases/                independently copied reading-room releases
  operations/              private deployment state and credentials
  migrations/              move journal, original code snapshot and checks
  legacy-paths/            compatibility links and older-script destinations
work/
  cache/toc-snapshots/      historical catalogs reproducible from Git blobs
  validation/              disposable validation outputs
  tmp/                     disposable scratch work
dist/                      assembled readers
  reading-room/            current volunteer reader
  reading-room-cd/         CD-only reader, when regenerated
```

For a new issue, use `archive/pdf/YYYY-MM/restoration/batch-NN/` during work,
`packages/` for checked article/batch exports, `reference/` for the final issue,
and `evidence/` for closeout reports and comparison evidence. Keep each exported
package self-contained: do not add notes inside a hash-manifested package.

Keep raw OCR, source-region mappings, corrections, review decisions, recipes,
runtime fingerprints, failure records and required crops alongside that issue.
OCR called a “cache” can be provenance; a model rerun need not reproduce the
same output. Existing OCR caches, trials, screenshots and uncertain material
were therefore retained. Only the historical TOC cache, which reconstructs
from recorded Git blobs and checks every hash, moved to `work/`.

An output belongs in `work/` only if all inputs and instructions are preserved,
regeneration has been checked, and no correction, review or provenance relies on
that copy. Otherwise put it in `archive/`. Do not delete issue work after export.
There is no automatic cleanup command.

## Successive restoration

Use this sequence for October 1984 and subsequent issues:

1. Read `PLAN-OCR.md` and the latest issue ledger. Verify the source PDF,
   canonical TOC identities and pinned runtime before starting a batch.
2. Create `archive/pdf/YYYY-MM/restoration/batch-NN/` for requests, reviewed
   maps, corrections, OCR state and raw results. Give changed inputs or a new
   attempt a new directory; retain the previous attempt and its failure record.
   The migration lookup describes old paths only; it is not a new-issue allocator.
3. Resume unchanged work with the tool's explicit resume action. Preserve its
   state and source hashes. A changed tool/runtime fingerprint calls for a new
   recorded attempt or the original pinned implementation, not weaker checks.
4. Export to a fresh `packages/batch-NN-r01/`. Build an independent comparison
   under `evidence/`, validate it, and record the selected package in the ledger.
   Close an issue into a fresh `reference/` (or a named revision if it exists).
   Never replace a completed package in place or edit its manifest to hide a
   provenance change. Small mutable progress ledgers still need Git checkpoints
   or versioned backups; placing them in `archive/` alone does not version them.
5. Keep all selected packages, recipes, corrections, raw OCR, reviews, source
   mappings, runtime fingerprints and required assets after closeout. Record the
   code revision and exact commands. Copy the local archive and original inputs
   to independent backup storage, then verify a restore before calling that
   checkpoint recoverable. Git commits alone do not back up these ignored files.

The current PDF package/issue exporters refuse an existing destination. The CD2
pilot/issue and CD2/CD3 reference builders now do too. For CD reference groups,
`--resume` checks completed packages before reusing them; `--verify-existing`
compares reconstructed file bytes without changing existing files. A different
result requires a fresh `--output`, for example `archive/cd2/evidence/reference-r02`.
Finalization adds missing files during an ordinary/resumed build, accepts
identical existing bytes, and refuses changes to existing files. Verification
does not repair missing files. Run only one writer for a given batch/output.

Reader integration is a separate task requiring an explicit request. Save a
named release before replacing a reader. `work/` may contain disposable
validation outputs, but should never hold the only OCR result, correction or
review decision needed to continue the next checkpoint.

## Old paths and migration

On 2026-10-16, `data/` moved to `metadata/`. Local `private/`, `build/` and
`output/` contents moved to the locations in `metadata/storage-layout.json`.
Original subtrees were renamed on the same filesystem, preserving their files,
bytes and inode identities. The move journal is under
`archive/migrations/storage-2026-10-16/`.

The four old root names remain as symlinks. Old manifests, recipes and reports
keep their recorded paths and hashes. Compatibility links under
`archive/legacy-paths/` connect them to canonical locations. New files created by
older scripts through those paths also remain in preserved storage. They are
not duplicate copies; **deleting through a compatibility link deletes the real
file**. Keep the links and use the canonical layout for new work.

```sh
make check-storage
python3 -m tools.storage_layout lookup build/pdf-restoration/14-1984-09-reference
```

`check-storage` checks required preserved paths and alias destinations. Missing
regenerable work or dist outputs are reported separately. It is a layout check;
package and reader checkers remain responsible for content validation.

After a fresh checkout, restore `archive/` and original inputs from backup,
then run `make init-storage`. This recreates old-path links from the tracked map.
It does not download or invent missing restoration material. Recreate the TOC
cache with `make restore-toc-snapshot` (other historical snapshot descriptors can
be supplied with `--record`).

Frozen experiments can pin the implementation's hashes as well as their inputs.
For an exact historical rerun, use the Git revision in `storage-layout.json` and
the preserved inputs. The original tracked source is also saved as
`archive/migrations/storage-2026-10-16/tracked-before.tar`.
Current OCR/reader entry points use canonical defaults; older CD commands use
the compatibility paths. Code changes do not rewrite or relax historical hash
checks. Some preserved one-off scripts infer the repository root from their
physical directory depth; those need the original layout or an explicit path
adapter when rerun. Their source bytes are retained unchanged.

Known depth-dependent examples are May's `boundary-review.py`, July's
`report-07-prepare.py`, and September's `typing-segment-b/verify_listing.py` and
`six-compatible/survey.py`. Compatibility symlinks cannot correct
`Path(__file__).resolve().parents[N]`: it sees the new physical depth. Do not
execute these frozen scripts blindly in the relocated tree. Use an isolated
copy of their original layout/code, or a separately reviewed adapter with the
original script's hash checked. The survey also needs its temporary page images
recreated. These historical scripts are not the workflow for a new issue.

For the earlier compact preview archive, use
`python3 -m tools.storage_layout restore-retired SNAPSHOT_NAME`. This invokes
only the original hash-checked restore function with its repository root adapted;
it retains the original source/snapshot checks and overwrite refusal. Restore
the volunteer reader first if a retired snapshot depends on it.

## Restore the reading room

The pre-migration volunteer reader is retained independently at
`archive/releases/reading-room-2026-10-16/`. Its sibling JSON file lists every
file's size and SHA-256. The release contains the existing seven PDF issues and
three CDs; this reorganization does not integrate another issue or deploy it.

The older July reader intermediate was already missing before migration. Keep
this release so the existing reader can be recovered without that intermediate.
The copy uses independent files, not hard links to the mutable reader.

```sh
# Restore after dist/reading-room has been removed (refuses existing output).
make restore-volunteer-reading-room
# Or restore beside the current reader:
make restore-volunteer-reading-room VOLUNTEER_OUTPUT=dist/reading-room-restored
make check-volunteer-reading-room
python3 -m http.server 4189 --bind 127.0.0.1 --directory dist/reading-room
```

Restore verifies every copied file before installing the destination. UI-only
rebuilds still use `make build-volunteer-reading-room`. Later releases use
distinct names and can be restored separately:

```sh
# Run only after an explicitly requested reader build has passed validation.
python3 -m tools.storage_layout snapshot-reader --release reading-room-YYYY-MM-DD-r01
python3 -m tools.storage_layout restore-reader dist/recovery-check --release reading-room-YYYY-MM-DD-r01
```

Replace the example release name with the actual date/revision. Snapshot accepts
`--source dist/another-reader` when needed. Reusing a release name checks both the
saved copy and current source against the receipt; a changed reader requires a
new name. Interrupted copies can resume only with matching source bytes.
Preserve each release's sibling JSON receipt. The restore command without
`--release` deliberately selects the original `reading-room-2026-10-16` release,
not whichever directory happens to be newest.

The old July integration input is absent, so the default volunteer **export**
cannot currently reconstruct the assembled reader from that intermediate.
Restore the saved release for recovery. Its data can be an explicitly selected
base for future integration after that task's review; do not silently substitute
it into the old August-only export recipe.

The retained release and migration journal are on this same disk. They protect
against accidental rebuilding, not disk failure. Preserve `archive/` and
original sources in a separate backup; repository commits cover `metadata/`,
code and documentation only. Browser review notes must still be exported from
the reading room: they live in browser storage, outside these directories.

## Migration validation

All 1,206 mapped moves and all 67 original metadata file hashes were verified.
The independent reader copy contains 119,311 files, checked against the source
with SHA-256. The current reader, September issue and pinned OCR runtime pass
validation. Focused Python runs cover 287 tests (three skipped); 24 frontend tests
and a build to `work/validation/storage-ui` pass.

The broad historical suite still has pre-existing CD1 extracted-source and
February TOC discrepancies. Migration-related failures were fixed and rechecked
in focused runs. Details and original test output are retained in
`archive/migrations/storage-2026-10-16/validation.json` and its sibling logs.

The subsequent [plans and tools review](STORAGE-REVIEW.md) also tests successive
issues, overwrite refusal, named releases and recovery from the original ISOs.
