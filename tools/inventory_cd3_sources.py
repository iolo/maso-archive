"""Check the CD3 ISO, extracted tree, both HELPDECO probes, and CAB members."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from tools.inventory_cd1_sources import (compare_trees, extract_inventory,
                                         fingerprint, iso_listing, safe_relative,
                                         tree_inventory)
from tools.map_cd1_topic import ROOT, require
from tools.recover_cd1_text import json_bytes

ISO = ROOT / "masocd-3.iso"
TREE = ROOT / "masocd-3"
PROBE = ROOT / "private/cd3-probe"
OUTPUT = ROOT / "build/cd3-preservation/inventory.json"
RECORD = ROOT / "data/catalog/preservation/cd3-inventory.json"
EXPECTED = {"bytes": 327081984, "sha256": "7c269df8479c72919863f27b68dceb6fe8b567a18f27eb9481655e15e4ae17d0"}
REVISION = "b9c187a20d83a3e738d8fe073eb924a8b7264c5c"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def cab_members(path):
    result = subprocess.run(["7z", "l", "-slt", str(path)], capture_output=True, timeout=120)
    require(result.returncode == 0, f"CAB listing failed: {path}")
    listing = result.stdout.decode("utf-8")
    require("Type = Cab\n" in listing and "----------\n" in listing, f"Not a CAB: {path}")
    members = []
    for block in listing.split("----------\n", 1)[1].strip().split("\n\n"):
        row = dict(line.split(" = ", 1) for line in block.splitlines() if " = " in line)
        name = row["Path"].replace("\\", "/")
        safe_relative(name)
        members.append({"path": name, "bytes": int(row["Size"])})
    require(len({m["path"] for m in members}) == len(members), f"Duplicate CAB member: {path}")
    return members


def build():
    iso = fingerprint(ISO)
    require(iso == EXPECTED, "CD3 ISO differs from recorded source")
    listing, version = iso_listing(ISO)
    extracted = tree_inventory(TREE)
    with tempfile.TemporaryDirectory(prefix="maso-cd3-inventory-") as temporary:
        fresh = extract_inventory(ISO, listing, Path(temporary))
        compare_trees(fresh, extracted)
    require(fingerprint(ISO) == iso, "CD3 ISO changed during inventory")
    main = tree_inventory(PROBE / "main/raw")
    baggage = tree_inventory(PROBE / "list/raw")
    files = {row["path"]: row for row in extracted["files"]}
    require((PROBE / "main/raw/MASO3.rtf").read_bytes().startswith(b"{\\rtf1"), "Main decoder RTF missing")
    require((PROBE / "list/raw/LIST.rtf").read_bytes().startswith(b"{\\rtf1"), "List decoder RTF missing")
    require("LIST1.TXT" in {r["path"] for r in baggage["files"]}, "LIST baggage missing")
    cabs = {}
    for path in sorted(p for p in files if p.lower().endswith(".cab")):
        cabs[path] = cab_members(TREE / path)
    detail = {"schema_version": 1, "disc_id": "cd3", "iso": {"path": ISO.name, **iso},
              "iso_entries": listing, "extracted": {"root": TREE.name, **extracted},
              "probe": {"main": {"root": "private/cd3-probe/main/raw", **main},
                        "list": {"root": "private/cd3-probe/list/raw", **baggage}},
              "cab_members": cabs,
              "decoder": {"repository": "https://github.com/joncampbell123/helpdeco",
                          "revision": REVISION, "arguments": {
                              "main": ["../../../../masocd-3/MASO3.M14", "/g"],
                              "list": ["../../../../masocd-3/LIST.M14", "/g"]}},
              "extraction": {"tool_version": version,
                             "command": ["7z", "x", "-y", "-bd", "-bb0", "-o<TEMP>/disc", ISO.name]},
              "validation": {"iso_hash_matches_recorded": True,
                             "fresh_iso_extraction_matches_tree": True,
                             "both_m14_decode_to_rtf": True,
                             "cab_members_listed_without_extraction": True}}
    raw = json_bytes(detail)
    summary = {"schema_version": 1, "disc_id": "cd3", "scope": "source_inventory",
               "iso": detail["iso"], "containers": {name: files[name] for name in ("MASO3.M14", "LIST.M14")},
               "counts": {"disc_files": len(extracted["files"]),
                          "disc_directories": len(extracted["directories"]),
                          "main_probe_files": len(main["files"]),
                          "list_probe_files": len(baggage["files"]),
                          "cab_files": len(cabs),
                          "cab_members": sum(map(len, cabs.values()))},
               "probe_extensions": dict(sorted(Counter(Path(r["path"]).suffix.lower()
                                                       for r in main["files"]).items())),
               "viewer_entry_point": "MASO3.EXE on disc; owner reports setup creates only a shortcut",
               "validation": detail["validation"],
               "private_detail": {"path": str(OUTPUT.relative_to(ROOT)), "bytes": len(raw), "sha256": digest(raw)}}
    return summary, raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    try:
        summary, raw = build()
        if not args.write_record:
            require(json.loads(RECORD.read_bytes()) == summary, "Reviewed CD3 inventory differs")
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(raw)
        if args.write_record:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_bytes(json_bytes(summary))
        print("CD3 source verified:", summary["counts"])
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f"CD3 inventory failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
