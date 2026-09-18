# CD1 source inventory and preservation readiness

Step **11a is complete**: the local original and extracted source sets are fully
inventoried and checked. Step **11b remains pending**: the owner confirmed that
there is no independent backup yet. No restore from independent storage has
occurred, and CD1 is **not ready for bulk processing** on that basis.

The [readiness record](../data/catalog/preservation/cd1-readiness.json) keeps that
distinction explicit. The [inventory summary](../data/catalog/preservation/cd1-inventory.json)
pins the detailed private inventory by byte count and SHA-256.

## Verified local sources

| Source set | Files | Bytes | Check |
| --- | ---: | ---: | --- |
| `masocd-1.iso` | 1 | 351,090,688 | Matches the initial whole-image SHA-256 |
| `masocd-1/` | 5,828 | 343,516,641 | Every path, size, and hash matches a fresh ISO extraction |
| `private/cd1-probe/raw/` | 7,374 | 270,966,330 | Every entry matches the existing probe manifest |
| Probe supporting files | 3 | 1,412,236 | Newly inventoried manifest, build log, and internal-directory listing |

The disc also contains **375 directories**, all accounted for, including empty
directories. The 7,374 probe entries comprise 7,372 decoder outputs and two process
logs. With supporting files, the probe tree has **7,377 files / 272,378,566 bytes**.
There are no unaccounted files in either inspected tree, no symlinks, and no
content mismatches. The MVB inside the ISO matches the probe's recorded input hash.

CD1 image SHA-256:

```text
dabd54e6a516ba9e3a2c348b8d1eebddd8bd45d8be3c81c84855102a269d9a17
```

The detailed inventory lives at `build/cd1-preservation/inventory.json` and records
all file paths, sizes, hashes, directory coverage, observed ISO modification
timestamps, extraction command/tool version, and the probe's decoder repository,
revision, build command, and arguments. Paths are relative to the workspace.
Source timestamps are observations, not publication-date evidence.

The inventory covers source preservation, not article completeness, correct
font rendering, usable code listings, or agreement with physical magazines.
Those remain separate checks. The two known broken media conversions retain
their existing deferred status.

## Reproduce the inventory

```sh
make inventory-cd1-sources
```

Requires the three local source paths above, Python, and `7z`. The command:

1. Checks the ISO against its initial size/hash and inspects its directory listing.
2. Hashes the existing extracted tree and independently extracts the ISO into a
   fresh temporary directory using 7-Zip.
3. Checks exact file and directory coverage, sizes, and hashes between the two
   trees, then removes the temporary extraction. Source files are read only.
4. Verifies every probe manifest entry and records all three supporting files.
5. Checks the result against the reviewed metadata summary and writes the detailed
   inventory under ignored `build/`.

The temporary extraction needs about 344 MB of free space. Repeated runs produce
identical inventory bytes; no local absolute paths, current timestamps, or
temporary directory names enter the inventory. A source change fails before the
successful inventory is replaced. Refreshing the reviewed summary is explicit:

```sh
python3 -m tools.inventory_cd1_sources --write-record
```

The initial implementation found a path-order comparison mismatch because Python
path-component ordering differs from full relative-string ordering. Consistent
relative-string ordering fixed that check; a regression test covers the case.
It was not a source-file discrepancy.

## Preservation set to keep on separate storage

The backup should retain these together, preserving their relative names:

- **Original `masocd-1.iso`**: the authoritative supplied disc image, including
  viewer files and source-code attachments. Keep its known hash alongside it.
- **Entire `private/cd1-probe/` tree**: raw recovery, image resources, indexes,
  manifest, and logs. This preserves the historical decoder result and evidence,
  even if a later decoder/toolchain behaves differently.
- **Detailed `build/cd1-preservation/inventory.json` and its tracked summary**:
  the reference for subsequent file-by-file checks.
- **Repository history and canonical metadata**, including identity registries,
  reviewed mappings, plans, and progress. A working checkout alone is not proof
  of an independent repository backup. Include newly supplied metadata files
  in the owner's backup even before their import is scheduled.
- **Prepared private recovery/package artifacts and toolchain evidence** when
  practical. Preserve the HELPDECO revision/build record and conversion versions;
  do not rely on a temporary tool checkout as the only retained copy.

The ISO plus entire probe tree totals **623,469,254 bytes**, excluding repository,
inventory, and prepared artifacts. The extracted `masocd-1/` tree can be restored
from the checked ISO; retaining it as well brings the three inspected source
sets to **966,985,895 bytes**. Those totals describe logical file bytes, not storage
allocation or deduplicated backup size.

Choose a separate drive or other independent storage and record its location
privately. A second path, filesystem device ID, or copy on the same physical disk
does not by itself establish independence. This step has not copied sources to
another storage location.

## Prepared local transfer set

The [transfer record](../data/catalog/preservation/cd1-transfer.json) identifies
a **673,433,600-byte archive** ready to copy to separate storage:

```text
private/preservation/cd1-transfer/cd1-a0cf99712270-a18c40ba44c5.tar
private/preservation/cd1-transfer/cd1-a0cf99712270-a18c40ba44c5.tar.sha256
```

It contains 7,581 payload files: the original ISO, the complete probe tree, all
current `build/` artifacts (including inventories and historical TOC inputs), and
a self-contained Git bundle through commit `a0cf9971227092f0d372591db1d0a723a266fbb1`.
`MANIFEST.json` lists every payload file's size/hash and the directory inventory;
`RESTORE.txt` explains the transfer and restore steps. The reconstructable
`masocd-1/` directory is omitted. Uncommitted repository changes and ignored files
outside these named source sets are not included. The transfer preparation tool
itself was committed after this content snapshot; rerun it for a later snapshot.

```sh
make prepare-cd1-transfer
```

The command verifies the ISO/probe against the preserved inventory, includes
committed Git refs/history, and hashes every archived payload without extracting
it. It writes only beneath ignored `private/preservation/cd1-transfer/`. Archive
names include their repository commit and content hash, so a later set does not
replace an earlier one. Each set has a `.sha256` sidecar and private JSON receipt.
It never updates backup readiness or writes to external storage.

Copy the archive and checksum sidecar together. On the **separate storage**, run:

```sh
sha256sum -c cd1-a0cf99712270-a18c40ba44c5.tar.sha256
```

Extract into a new empty directory. The ISO will be at its root; retain the probe
tree, build artifacts, and Git bundle alongside it. To restore repository history,
clone `repository.bundle` into a new checkout. The prepared bundle was also
cloned locally and passed `git fsck --full`; its historical TOC blob is intact.
Those local checks do not establish independent storage or complete step 11b.
Provide the independent location/storage description for the restore check below.
The physical CD is also an independent recovery source: once its drive is
accessible, a fresh read can be compared against the preserved ISO/disc inventory.
Possession of the disc is recorded separately from successful read/restore evidence.

## Restore check when the backup exists

After creating an independent ISO copy, supply its real path and a factual
description of the storage location. For example, replacing the placeholders:

```sh
python3 -m tools.inventory_cd1_sources \
  --backup-iso /path/on/separate-storage/masocd-1.iso \
  --independent-storage-note 'Owner description of the separate backup storage'
```

The command first verifies the local inventory. It rejects the working ISO,
workspace-local copies, and hard links to the working image. It hashes the backup,
copies it to a newly created temporary restore file, hashes that restored image,
extracts it, and checks all 5,828 files and 375 directories against the inventory.
It checks that the backup did not change during copying and removes the temporary
restore. It needs roughly 695 MB of temporary space. It does not overwrite the
backup or any working source.

Only a successful restore writes:

- `private/preservation/cd1-backup-check.json`: actual backup path, supplied
  independence description, device observations, timestamp, and verification.
- `data/catalog/preservation/cd1-backup-check.json`: a sanitized evidence summary
  and hash of the private report, without machine-specific location details.

Storage independence is explicitly **owner-described**; the tool does not infer
physical independence from device IDs. The ISO restore check does not certify
that the probe tree, repository, or prepared artifacts were also backed up.
Verify those copied preservation files against their inventories/snapshots too.
After reviewing actual evidence, update readiness, PLAN-CD1, and PROGRESS and
commit the metadata. The command does not automatically mark the preservation checkpoint
complete. A failed check leaves prior successful backup evidence untouched;
an old success is historical evidence, not proof of the latest attempt.

## Status and validation

Nine new tests cover modified/missing/extra files, empty directories, unsafe
archive paths, symlinks, probe manifest coverage, tool failure, rejection of the
working image or corrupt backups, temporary-restore cleanup, and restored-tree
mismatches. Restore mechanics use explicitly synthetic fixtures and do not count
as a real backup test. The actual-source test verifies the complete local CD1 set.

The owner confirms the local copy is the working `masocd-1.iso`, extracted from
the retained original physical CD. No optical drive is currently available.
Step 11b is deferred until independent storage or an optical drive is available; probe/repository preservation remains a separate part of that checkpoint. The
[February 1988 issue handoff](CD1-ISSUE-1988-02.md) and expanded TOC import are complete.
The next task is **13a: build the CD1 processing inventory for the batch pipeline**.
All six observed native February articles are prepared. Shared-pipeline validation
will precede a resumable run across the remaining CD1 queue. Backup/restore
verification remains deferred and does not block extraction that reads verified originals and writes separate
outputs. These checks concern file integrity and recoverability, not legal
ownership or publication permission.
