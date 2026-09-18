"""Prepare a private, checksummed CD1 transfer archive; never claim an independent backup."""

import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

from tools.inventory_cd1_sources import fingerprint, safe_relative, tree_inventory
from tools.map_cd1_topic import ROOT, require
from tools.recover_cd1_text import json_bytes

OUTPUT = ROOT / "private/preservation/cd1-transfer"
INSTRUCTIONS = b"""CD1 preservation transfer set

This is a local transfer set, not independent-backup evidence.
Copy the archive and its .sha256 file to separate storage, then check:
  sha256sum -c <archive-name>.sha256
Extract only into a new empty directory. The archive contains the original ISO,
whole probe tree, build artifacts/inventories, and a Git bundle of committed refs.
MANIFEST.json records every payload file's SHA-256 and the repository commit.
The bundle does not contain uncommitted changes or ignored files outside this set.
Clone repository.bundle into a new checkout to recover repository history.
The extracted masocd-1 directory is omitted: it is reconstructable from the ISO.

After transfer, provide the independent archive/extracted ISO location and storage
description. The documented independent ISO restore check must still run, and
the other copied files must be checked against MANIFEST.json. A local verification
does not establish storage independence or complete PLAN-CD1 step 11b.
"""


def add_bytes(archive, name, raw):
    info = tarfile.TarInfo(name)
    info.size, info.mode = len(raw), 0o644
    archive.addfile(info, io.BytesIO(raw))


def write_archive(destination, files, directories, repository_commit):
    """files maps safe archive names to actual regular files, preserving exact bytes."""
    require(not ({"MANIFEST.json", "RESTORE.txt"} & set(files)), "Reserved transfer filename")
    require(len(set(directories)) == len(directories), "Duplicate transfer directory")
    require(not (set(files) & set(directories)), "File/directory collision")
    records = []
    for name, path in sorted(files.items()):
        safe_relative(name)
        records.append({"path": name, **fingerprint(path)})
    manifest = {"schema_version": 1, "disc_id": "cd1", "scope": "local_transfer_set",
                "repository_commit": repository_commit, "files": records,
                "directories": sorted(directories), "independent_backup_verified": False}
    with tarfile.open(destination, "w", format=tarfile.PAX_FORMAT) as archive:
        for name in sorted(directories):
            safe_relative(name)
            info = tarfile.TarInfo(name)
            info.type, info.mode = tarfile.DIRTYPE, 0o755
            archive.addfile(info)
        for record in records:
            path = files[record["path"]]
            info = tarfile.TarInfo(record["path"])
            info.size, info.mode = record["bytes"], 0o644
            with path.open("rb") as stream:
                archive.addfile(info, stream)
            require(fingerprint(path) == {k: record[k] for k in ("bytes", "sha256")},
                    f"Source changed during transfer: {record['path']}")
        add_bytes(archive, "MANIFEST.json", json_bytes(manifest))
        add_bytes(archive, "RESTORE.txt", INSTRUCTIONS)
    verify_archive(destination, manifest)
    return manifest


def verify_archive(path, expected):
    """Read every archived byte without extracting or following archive links."""
    with tarfile.open(path, "r:") as archive:
        members = archive.getmembers()
        names = [m.name for m in members]
        require(len(names) == len(set(names)), "Duplicate archive member")
        records = {r["path"]: r for r in expected["files"]}
        require(set(names) == set(records) | set(expected["directories"]) | {"MANIFEST.json", "RESTORE.txt"},
                "Archive coverage mismatch")
        for member in members:
            safe_relative(member.name)
            if member.name in expected["directories"]:
                require(member.isdir(), "Archive directory changed type")
                continue
            require(member.isfile(), "Archive payload is not a regular file")
            stream = archive.extractfile(member)
            if member.name in records:
                checksum, size = hashlib.sha256(), 0
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    checksum.update(chunk)
                    size += len(chunk)
                record = records[member.name]
                require(size == record["bytes"] and checksum.hexdigest() == record["sha256"],
                        f"Archive content mismatch: {member.name}")
            else:
                raw = json_bytes(expected) if member.name == "MANIFEST.json" else INSTRUCTIONS
                require(stream.read() == raw, "Transfer instructions/manifest mismatch")


def prepare():
    """Pin committed history; uncommitted work is explicitly outside this snapshot."""
    summary = json.loads((ROOT / "data/catalog/preservation/cd1-inventory.json").read_bytes())
    inventory_path = ROOT / summary["output"]["path"]
    require(fingerprint(inventory_path) == {k: summary["output"][k] for k in ("bytes", "sha256")},
            "Preservation inventory changed")
    inventory = json.loads(inventory_path.read_bytes())
    iso = ROOT / inventory["iso"]["path"]
    require(fingerprint(iso) == {k: inventory["iso"][k] for k in ("bytes", "sha256")}, "ISO changed")
    probe = tree_inventory(ROOT / "private/cd1-probe")
    require(probe == {k: inventory["probe"][k] for k in ("files", "directories")}, "Probe tree changed")
    build = tree_inventory(ROOT / "build")
    files = {"masocd-1.iso": iso}
    directories = {"private", "private/cd1-probe", "build"}
    for prefix, tree in (("private/cd1-probe", probe), ("build", build)):
        files.update({prefix + "/" + r["path"]: ROOT / prefix / r["path"] for r in tree["files"]})
        directories.update(prefix + "/" + name for name in tree["directories"])
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=OUTPUT) as temporary:
        stage = Path(temporary)
        bundle = stage / "repository.bundle"
        subprocess.run(["git", "bundle", "create", str(bundle), "--all", "HEAD"], cwd=ROOT, check=True, capture_output=True)
        subprocess.run(["git", "bundle", "verify", str(bundle)], cwd=ROOT, check=True, capture_output=True)
        files["repository.bundle"] = bundle
        archive = stage / "transfer.tar"
        manifest = write_archive(archive, files, sorted(directories), head)
        expected_sources = {"masocd-1.iso": {k: inventory["iso"][k] for k in ("bytes", "sha256")}}
        for prefix, tree in (("private/cd1-probe", probe), ("build", build)):
            expected_sources.update({prefix + "/" + r["path"]: {k: r[k] for k in ("bytes", "sha256")}
                                     for r in tree["files"]})
        require({r["path"]: {k: r[k] for k in ("bytes", "sha256")} for r in manifest["files"]
                 if r["path"] != "repository.bundle"} == expected_sources,
                "Sources changed since initial transfer inventory")
        require(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == head,
                "Repository HEAD changed during transfer preparation")
        details = fingerprint(archive)
        name = f"cd1-{head[:12]}-{details['sha256'][:12]}.tar"
        target = OUTPUT / name
        if target.exists():
            require(fingerprint(target) == details, "Existing transfer archive differs")
        else:
            archive.rename(target)
        (OUTPUT / (name + ".sha256")).write_text(f"{details['sha256']}  {name}\n", encoding="ascii")
        report = {"schema_version": 1, "scope": "local_transfer_set", "repository_commit": head,
                  "archive": {"path": str(target.relative_to(ROOT)), **details},
                  "payload_files": len(manifest["files"]), "payload_bytes": sum(r["bytes"] for r in manifest["files"]),
                  "archive_payload_verified": True, "git_bundle_verified": True,
                  "independent_backup_verified": False, "restore_from_independent_storage_verified": False}
        (OUTPUT / (name + ".json")).write_bytes(json_bytes(report))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        print(json.dumps(prepare(), ensure_ascii=False, indent=2))
    except (OSError, ValueError, tarfile.TarError, subprocess.CalledProcessError) as exc:
        print(f"CD1 transfer preparation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
