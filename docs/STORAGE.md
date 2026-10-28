# Storage and preservation

The deciding question is **whether losing a file would lose restoration work or
our ability to explain and reproduce it**, even while an issue is unfinished.
Completion does not make the supporting evidence disposable.

| Location | Contents | Retention |
| --- | --- | --- |
| `metadata/` | Stable IDs, catalog/provenance records, manual decisions, reference tables and storage map | Keep in Git |
| `archive/` | Completed packages **and ongoing restoration**, corrections, mappings, recipes, raw OCR, failed attempts, review evidence and pinned toolchains | Preserve and back up outside Git |
| `work/` | Temporary processing and caches with a verified reconstruction path | May discard after the task finishes; never the sole copy of work |
| `dist/` | Generated readers and optional deployment snapshots under `dist/releases/` | Disposable; no archival retention required |

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
      evidence/            comparison reports and unique validation evidence
    shared/                inventories and work shared across issues
  cd1/                     extraction, reference, packages and evidence
  cd2/
  cd3/
  toc/                     current catalog, restoration and image derivatives
  covers/                  cover inventories and retained derivatives
  toolchains/ocr/           exact OCR runtime used by restoration recipes
  experiments/             retained OCR experiments
  operations/              private deployment state and credentials
  migrations/              move journal, original code snapshot and checks
  legacy-paths/            compatibility links and older-script destinations
work/
  cache/toc-snapshots/      historical catalogs reproducible from Git blobs
  validation/              disposable validation outputs
  reading-room/            disposable reader integration stages
  tmp/                     disposable scratch work
dist/                      assembled readers
  releases/                optional, disposable deployment snapshots and receipts
  reading-room-volunteer/  volunteer reader, when generated
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
Use the explicit session cleanup below for disposable outputs.

For an independent rebuild, compare the disposable `work/validation/` output with
the selected archive package and retain the comparison report and hashes under
`evidence/`. A byte-identical rebuild copy needs no separate permanent retention.
Keep any unique failure, correction or review evidence before cleaning its scratch
location. A directory named `evidence` or a file described as a cache does not by
itself establish what needs preservation.

## Session cleanup

After saving the restoration checkpoint and finishing its processing jobs:

```sh
make clean-session                         # Preview; changes nothing
make clean-session CLEAN_ARGS=--apply      # Remove the listed temporary outputs
```

The default locations are `work/tmp/`, `work/validation/` and `work/reading-room/`.
Other `work/` locations are left alone. Optional flags broaden the selection:

```sh
# Preview reader builds/releases and the reproducible TOC cache as well:
make clean-session CLEAN_ARGS="--include-dist --include-caches"
# Remove the same selection:
make clean-session CLEAN_ARGS="--apply --include-dist --include-caches"
```

`--include-dist` adds generated contents of `dist/`, including `dist/releases/`,
while keeping `dist/README.md`. `--include-caches` adds only
`work/cache/toc-snapshots/`; recreate it with `make restore-toc-snapshot` or the
appropriate historical snapshot descriptor. Deleting readers does not implement
the missing full reader rebuild described below.

The command does not inspect or delete `archive/`, `metadata/`, original sources,
compatibility aliases or installed toolchains. It rejects selected paths with
symlinked parents, Git-tracked files, mount points or special files before any
deletion. Links inside temporary directories are unlinked without following
their targets. Space figures are estimates; hard links or filesystem sharing
can affect the actual space reclaimed. Cleanup runs only when explicitly called;
there is no automatic deletion after a failed or interrupted restoration.
The command does not discover temporary copies misplaced inside `archive/`;
those need a separate review of their contents and dependencies. Its default
scope keeps existing readers and TOC caches available between sessions.

### Shared evidence cleanup — 2026-10-28

The owner's cleanup removed the generated reader integration `stages/` tree
from `archive/pdf/shared/evidence/reader-integration-2026-10-22/`. Its reports,
scripts and browser observations remain. New reader stages belong under
`work/reading-room/`, with the default `work/reading-room/volunteer-stages/`.

Six repeat exports (`pilot-repeat`, `6a-matchsticks-repeat`,
`6b-turbo-pascal-repeat`, `6c-basic-column-repeat`, `7-cd-comparison-repeat` and
`10-batch-repeat`) were checked file by file with SHA-256 against their selected
copies in `archive/pdf/shared/packages/` before deletion. Those packages retain
all of the duplicate content. Their historical `build/pdf-restoration/` aliases
now point to disposable `work/validation/pdf-shared/` destinations so a later
verification export stays outside the archive. Missing repeats are expected.
Earlier correction/configuration variants and other unique evidence remain.
The cleanup receipt is `metadata/catalog/storage-cleanup-2026-10-28.json`.

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
   under `work/validation/YYYY-MM/`, validate it, retain its report and hashes
   under the issue's `evidence/`, and record the selected package in the ledger.
   Close an issue into a fresh `reference/` (or a named revision if it exists).
   Never replace a completed package in place or edit its manifest to hide a
   provenance change. Small mutable progress ledgers still need Git checkpoints
   or versioned backups; placing them in `archive/` alone does not version them.
5. Keep all selected packages, recipes, corrections, raw OCR, reviews, source
   mappings, runtime fingerprints and required assets after closeout. Record the
   code revision and exact commands. Copy the local archive and original inputs
   to independent backup storage, then verify a restore before calling that
   checkpoint recoverable. Git commits alone do not back up these ignored files.
6. After saving the session checkpoint and finishing its jobs, follow
   [session cleanup](#session-cleanup). Remove disposable scratch, validation and
   reader-stage outputs; keep the selected restoration inputs and results.

The current PDF package/issue exporters refuse an existing destination. The CD2
pilot/issue and CD2/CD3 reference builders now do too. For CD reference groups,
`--resume` checks completed packages before reusing them; `--verify-existing`
compares reconstructed file bytes without changing existing files. A different
result requires a fresh `--output`, for example `archive/cd2/evidence/reference-r02`.
Finalization adds missing files during an ordinary/resumed build, accepts
identical existing bytes, and refuses changes to existing files. Verification
does not repair missing files. Run only one writer for a given batch/output.

Reader integration is a separate task requiring an explicit request. A named
deployment snapshot under `dist/releases/` is optional. `work/` may contain disposable
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

## Reading-room deployment outputs

Reading-room builds and release snapshots are generated web deployment artifacts.
They belong in `dist/`, with optional named snapshots and their JSON hash receipts
under `dist/releases/`. They are not part of the restoration archive and require
no permanent preservation. `work/` remains for temporary processing and caches.
Keep canonical source material, restoration packages, metadata, corrections,
required assets, recipes and validation evidence in their preserved locations.

The owner deleted the former `archive/releases/` copies; local reader outputs
are also absent.
The empty old directory was removed when the release location changed. No release
payloads were moved or regenerated. Historical catalogs, receipts and frozen
reproduction records retain their original paths and hashes as evidence; an old
release path in those records does not imply that the generated files still exist.

### Current build limitation

The current volunteer exporter is incremental: its default base is
`dist/releases/reading-room-2026-10-22-before-all-restorations/data`, to which it
adds December 1984 and February 1985. That base is currently absent. Changing its
location does not implement a full rebuild. Rebuilding the complete reader from
preserved CD/PDF packages and metadata without any previous release remains to
be implemented and verified. The dependency on generated snapshots is a build
limitation, not an archival retention requirement. Restoration can continue
without any reading-room build or release snapshot.

The last assembled volunteer reader (2026-10-22) contained 11 completed PDF
restorations and all three CDs. Later restoration closeouts remain separate
until explicitly integrated. See [the reader guide](READING-ROOM.md).

### Optional deployment snapshots

For an available, validated reader, these commands create an independent copy
under `dist/releases/` and copy it back to a fresh serving directory:

```sh
python3 -m tools.storage_layout snapshot-reader --source dist/reading-room-volunteer --release reading-room-YYYY-MM-DD-r01
python3 -m tools.storage_layout restore-reader dist/recovery-check --release reading-room-YYYY-MM-DD-r01
```

The snapshot command refuses differing bytes under an existing name. Copying a
snapshot back verifies its receipt and refuses an existing output. Source and
serving directories must be outside `dist/releases/` to avoid overlapping copies.
If keeping a snapshot for convenience, keep its matching receipt with it; both
are disposable deployment outputs.

`make restore-volunteer-reading-room` selects the optional
`reading-room-2026-10-22-all-restorations` snapshot. It works only while that
snapshot and receipt exist in `dist/releases/`. The lower-level restore command
without `--release` still selects the original `reading-room-2026-10-16` name,
not whichever directory happens to be newest. Neither command rebuilds a reader
from restoration packages. `make build-volunteer-reading-room` builds the UI;
it does not regenerate the reader data.

Back up `archive/` and original sources separately; repository commits cover
`metadata/`, code and documentation only. Browser review notes live in browser
storage and must be exported separately.

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
