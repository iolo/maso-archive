"""Inventory CD1 sources and optionally test restoration from an independent ISO copy."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

from tools.map_cd1_topic import ROOT, require
from tools.recover_cd1_text import json_bytes

ISO = ROOT / "masocd-1.iso"
ISO_SHA256 = "dabd54e6a516ba9e3a2c348b8d1eebddd8bd45d8be3c81c84855102a269d9a17"
EXTRACTED = ROOT / "masocd-1"
PROBE = ROOT / "private/cd1-probe"
OUTPUT = ROOT / "build/cd1-preservation"
RECORD = ROOT / "data/catalog/preservation/cd1-inventory.json"
BACKUP_OUTPUT = ROOT / "private/preservation/cd1-backup-check.json"
BACKUP_RECORD = ROOT / "data/catalog/preservation/cd1-backup-check.json"


def safe_relative(value):
    path = PurePosixPath(value)
    require(value and not path.is_absolute() and "\\" not in value and
            all(p not in ("", ".", "..") for p in value.split("/")), f"Unsafe source path: {value!r}")
    return path


def fingerprint(path):
    require(path.is_file() and not path.is_symlink(), f"Not a regular source file: {path.name}")
    before = path.stat()
    checksum, size = hashlib.sha256(), 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(chunk)
            size += len(chunk)
    after = path.stat()
    require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) ==
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns) and size == after.st_size,
            f"Source changed while hashing: {path.name}")
    return {"bytes": size, "sha256": checksum.hexdigest()}


def tree_inventory(root):
    require(root.is_dir() and not root.is_symlink(), "Source root must be a real directory")
    files, directories = [], []
    for path in sorted(root.rglob("*"), key=lambda p: p.as_posix()):
        relative = path.relative_to(root).as_posix()
        safe_relative(relative)
        require(not path.is_symlink(), f"Symlink in source tree: {relative}")
        if path.is_dir():
            directories.append(relative)
        else:
            files.append({"path": relative, **fingerprint(path)})
    return {"files": files, "directories": directories}


def compare_trees(expected, actual):
    require(expected == actual, "Source tree differs in paths, directories, sizes, or hashes")


def checked_probe(root, tree):
    manifest = json.loads((root / "manifest.json").read_bytes())
    entries = manifest["files"]
    indexed = {entry["path"]: entry for entry in entries}
    require(len(indexed) == len(entries), "Duplicate probe manifest path")
    for name in indexed:
        safe_relative(name)
        require(name.startswith("raw/"), "Unexpected probe manifest path")
    actual = {entry["path"]: entry for entry in tree["files"]}
    require(set(actual) == set(indexed) | {"manifest.json", "build.log", "internal-directory.txt"},
            "Probe file inventory differs from manifest and supporting files")
    for name, expected in indexed.items():
        require(actual[name] == expected, f"Probe size/hash mismatch: {name}")
    return manifest


def run_7z(arguments):
    result = subprocess.run(["7z", *arguments], capture_output=True, timeout=120)
    require(result.returncode == 0, f"7z failed ({result.returncode}): {result.stderr.decode(errors='replace')[:500]}")
    return result.stdout.decode("utf-8", errors="strict")


def iso_listing(iso):
    listing = run_7z(["l", "-slt", str(iso)])
    require("----------\n" in listing, "Missing ISO listing entries")
    header, body = listing.split("----------\n", 1)
    require("Type = Iso\n" in header, "Source is not an ISO image")
    rows, paths = [], set()
    for block in body.strip().split("\n\n"):
        row = dict(line.split(" = ", 1) for line in block.splitlines() if " = " in line)
        safe_relative(row["Path"])
        require(row["Path"] not in paths and row["Folder"] in ("+", "-") and not row.get("Symbolic Link"), "Invalid/duplicate ISO entry")
        paths.add(row["Path"])
        rows.append({"path": row["Path"], "kind": "directory" if row["Folder"] == "+" else "file",
                     "bytes": None if row["Folder"] == "+" else int(row["Size"]), "recorded_modified": row.get("Modified")})
    return sorted(rows, key=lambda r: r["path"]), next(line.strip() for line in header.splitlines() if line.startswith("7-Zip "))


def extract_inventory(iso, listing, directory):
    target = directory / "disc"
    target.mkdir()
    run_7z(["x", "-y", "-bd", "-bb0", "-o" + str(target), str(iso)])
    result = tree_inventory(target)
    require([(r["path"], r["bytes"]) for r in result["files"]] ==
            [(r["path"], r["bytes"]) for r in listing if r["kind"] == "file"], "ISO extraction file coverage differs")
    require(result["directories"] == [r["path"] for r in listing if r["kind"] == "directory"], "ISO extraction directory coverage differs")
    return result


def build_inventory():
    iso = fingerprint(ISO)
    require(iso == {"bytes": 351090688, "sha256": ISO_SHA256}, "CD1 ISO differs from initial source fingerprint")
    listing, version = iso_listing(ISO)
    extracted = tree_inventory(EXTRACTED)
    with tempfile.TemporaryDirectory(prefix="maso-cd1-inventory-") as directory:
        fresh = extract_inventory(ISO, listing, Path(directory))
        compare_trees(fresh, extracted)
    require(fingerprint(ISO) == iso, "ISO changed during inventory")
    probe = tree_inventory(PROBE)
    manifest = checked_probe(PROBE, probe)
    mvb = next(r for r in extracted["files"] if r["path"] == "MASOCD.MVB")
    require(manifest["source"] == "masocd-1/MASOCD.MVB" and manifest["source_sha256"] == mvb["sha256"], "Probe source differs from ISO MVB")
    inventory = {"schema_version": 1, "disc_id": "cd1", "scope": "local_source_inventory",
                 "iso": {"path": "masocd-1.iso", **iso}, "iso_entries": listing,
                 "extracted": {"root": "masocd-1", **extracted}, "probe": {"root": "private/cd1-probe", **probe},
                 "extraction": {"tool_version": version, "command": ["7z", "x", "-y", "-bd", "-bb0", "-o<TEMP>/disc", "masocd-1.iso"]},
                 "decoder": {k: manifest[k] for k in ("decoder_repository", "decoder_revision", "build_command", "decoder_arguments")},
                 "validation": {"iso_matches_initial_hash": True, "all_iso_files_match_extracted_tree": True,
                                "probe_manifest_verified": True, "probe_source_matches_iso": True,
                                "independent_backup_assessed": False, "restore_from_backup_assessed": False}}
    raw = json_bytes(inventory)
    summary = {"schema_version": 1, "disc_id": "cd1", "scope": "local_source_inventory",
               "iso": inventory["iso"], "counts": {
                   "disc_files": len(extracted["files"]), "disc_directories": len(extracted["directories"]),
                   "disc_file_bytes": sum(r["bytes"] for r in extracted["files"]), "probe_manifest_files": len(manifest["files"]),
                   "probe_supporting_files": 3, "probe_files": len(probe["files"]),
                   "probe_bytes": sum(r["bytes"] for r in probe["files"])},
               "probe_extensions": dict(sorted(Counter(Path(r["path"]).suffix.lower() or "(none)" for r in probe["files"]).items())),
               "validation": inventory["validation"],
               "output": {"path": str((OUTPUT / "inventory.json").relative_to(ROOT)), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}}
    return summary, raw


def restore_backup(backup, inventory, independence_note, restore_parent=None):
    """Restore an ISO to a new temporary path and compare all extracted files.

    Storage independence is an owner assertion, not inferred from device IDs.
    This routine never writes to the backup or overwrites working source files.
    """
    backup = Path(backup).expanduser().resolve(strict=True)
    require(independence_note.strip(), "An independent-storage description is required")
    require(not backup.is_relative_to(ROOT) and not backup.samefile(ISO), "Backup must be outside the workspace and distinct from the working ISO")
    before = fingerprint(backup)
    expected = {k: inventory["iso"][k] for k in ("bytes", "sha256")}
    require(before == expected, "Backup ISO does not match the reviewed source")
    with tempfile.TemporaryDirectory(prefix="maso-cd1-restore-", dir=restore_parent) as directory:
        root = Path(directory)
        restored = root / "restored.iso"
        with backup.open("rb") as source, restored.open("xb") as target:
            shutil.copyfileobj(source, target, length=1024 * 1024)
        require(fingerprint(restored) == expected and fingerprint(backup) == before, "ISO changed or restore bytes differ")
        listing, version = iso_listing(restored)
        require(listing == inventory["iso_entries"], "Restored ISO listing differs")
        result = extract_inventory(restored, listing, root)
        compare_trees(result, {k: inventory["extracted"][k] for k in ("files", "directories")})
        return {"schema_version": 1, "disc_id": "cd1", "scope": "independent_iso_backup_restore",
                "checked_at_utc": datetime.now(timezone.utc).isoformat(), "backup_path": str(backup),
                "storage_independence": {"basis": "owner_supplied_description", "description": independence_note,
                                         "backup_device_id": backup.stat().st_dev, "workspace_device_id": ISO.stat().st_dev},
                "restored_iso": expected, "restored_files": len(result["files"]), "restored_directories": len(result["directories"]),
                "extraction_tool": version, "temporary_restore_removed": True,
                "verification": {"backup_iso_hash_matches": True, "restored_iso_hash_matches": True, "all_disc_files_match": True},
                "limitations": ["Physical storage independence is owner-described, not proved by device IDs.",
                                "This checks the original ISO backup; probe/repository backups require separate evidence."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    parser.add_argument("--backup-iso", type=Path)
    parser.add_argument("--independent-storage-note")
    args = parser.parse_args()
    try:
        require(bool(args.backup_iso) == bool(args.independent_storage_note), "Provide both --backup-iso and --independent-storage-note")
        summary, raw = build_inventory()
        if not args.write_record:
            require(json.loads(RECORD.read_bytes()) == summary, "Source inventory differs from reviewed record")
        OUTPUT.mkdir(parents=True, exist_ok=True)
        temporary = OUTPUT / "inventory.json.tmp"
        temporary.write_bytes(raw)
        temporary.replace(OUTPUT / "inventory.json")
        if args.write_record:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_bytes(json_bytes(summary))
        if args.backup_iso:
            evidence = restore_backup(args.backup_iso, json.loads(raw), args.independent_storage_note)
            evidence["inventory_sha256"] = summary["output"]["sha256"]
            encoded = json_bytes(evidence)
            BACKUP_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            BACKUP_OUTPUT.write_bytes(encoded)
            BACKUP_RECORD.write_bytes(json_bytes({"schema_version": 1, "disc_id": "cd1", "scope": evidence["scope"],
                "checked_at_utc": evidence["checked_at_utc"], "storage_independence_basis": "owner_supplied_description",
                "inventory_sha256": evidence["inventory_sha256"], "restored_iso": evidence["restored_iso"],
                "restored_files": evidence["restored_files"], "verification": evidence["verification"],
                "private_evidence": {"path": str(BACKUP_OUTPUT.relative_to(ROOT)), "bytes": len(encoded), "sha256": hashlib.sha256(encoded).hexdigest()}}))
            print("Backup ISO restored and all disc files verified; storage independence recorded from the supplied description.")
        else:
            print("Local CD1 source inventory verified. Independent backup/restore was not assessed by this run.")
        print(summary["counts"])
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f"CD1 preservation check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
