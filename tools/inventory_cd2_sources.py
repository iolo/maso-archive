"""Verify the CD2 ISO, extracted tree, decoder probe, and one native article candidate.

The full checksummed inventory stays private. The tracked record contains only
counts, fingerprints, and source locations; no recovered article body or media.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from tools.inventory_cd1_sources import (compare_trees, extract_inventory,
                                         fingerprint, iso_listing, tree_inventory)
from tools.map_cd1_topic import ROOT, require
from tools.recover_cd1_text import json_bytes

ISO = ROOT / "masocd-2.iso"
TREE = ROOT / "masocd-2"
PROBE = ROOT / "private/cd2-probe/raw"
OUTPUT = ROOT / "build/cd2-preservation/inventory.json"
RECORD = ROOT / "data/catalog/preservation/cd2-inventory.json"
EXPECTED_ISO = {"bytes": 197738496, "sha256": "fc7b3047b2c6cc2555500faf43dc0b73ff877c2f5b01acdb32041615d2f31a0e"}
DECODER_REVISION = "b9c187a20d83a3e738d8fe073eb924a8b7264c5c"
RTF = "MASO2.rtf"
CONTEXT = b"3H9UTZ3"
ACTION = b"!SrcCopy(9401163)"
REF = "940116300"
TITLE = "한글 TeX을 이용하려면"
PAGE = re.compile(rb"(?<!\\)\\page\n")
FOOTNOTE = re.compile(rb"\{\\up \$\}\{\\footnote\\pard\\plain\{\\up \$\} ([^}]+)\}")
MEDIA = re.compile(rb"\\\{(?:bmc|ewl) ([^}]+)\\\}")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def cd2_candidate(rtf, extracted, probe):
    indexes = {}
    for name in ("book.lst", "info.lst", "qnatip.lst"):
        raw = (PROBE / name).read_bytes()
        lines = raw.decode("cp949").splitlines()
        require(all("^" in line for line in lines), f"Invalid index line in {name}")
        indexes[name] = lines
    matches = [(name, number + 1, line) for name, lines in indexes.items()
               for number, line in enumerate(lines) if line.endswith("^" + REF)]
    require(len(matches) == 1 and matches[0][0] == "book.lst" and
            matches[0][2] == TITLE + "^" + REF, "Candidate index entry changed")
    pages = list(PAGE.finditer(rtf))
    require(pages, "No RTF topic boundaries")
    locations = [m.start() for m in re.finditer(re.escape(ACTION), rtf)]
    require(len(locations) == 1, "Candidate action is missing or ambiguous")
    position = locations[0]
    prior = max((m for m in pages if m.start() < position), key=lambda m: m.start())
    following = next(m for m in pages if m.start() > position)
    start, end = prior.end(), following.start()
    body = rtf[start:end]
    require(CONTEXT in body and body.count(CONTEXT) == 1, "Candidate context changed")
    # RTF hex escapes are the source's encoded Korean bytes, distinct from the
    # CP949 title in the CD-native index.
    title_footnotes = FOOTNOTE.findall(body)
    require(len(title_footnotes) == 1, "Candidate title footnote changed")
    encoded = re.sub(rb"\\'([0-9a-fA-F]{2})", lambda m: bytes.fromhex(m[1].decode()), title_footnotes[0])
    require(encoded.decode("cp949") == TITLE, "Index and article title disagree")
    require(b"94.\\{vfld21\\}1\\{vfld1\\}.  163p" in body, "Article's own page label changed")
    resources = []
    names = {row["path"] for row in probe["files"]}
    for m in MEDIA.finditer(body):
        command = m[1].decode("ascii")
        name = command.split("!")[-1].strip() if "!" in command else command.strip()
        require(re.fullmatch(r"[A-Za-z0-9_.]+", name), f"Unsafe media name: {name}")
        resources.append({"command": command, "name": name, "available": name in names,
                          "rtf_byte_offset": start + m.start()})
    source_files = [row for row in extracted["files"] if row["path"].startswith("DATA/SOURCE/9401163/")]
    require(source_files, "Candidate SOURCE attachment missing")
    return {"native_reference": REF, "native_context": CONTEXT.decode(),
            "index": {"file": "book.lst", "line": matches[0][1], "entry": matches[0][2]},
            "title_evidence": "CD-native index and matching RTF title footnote",
            "issue_evidence": "RTF label includes 94., unresolved dynamic fields, 1, and 163p; no independent paper issue metadata",
            "rtf": {"path": RTF, "byte_offset": start, "byte_length": end - start,
                    "sha256": sha(body), "boundary_basis": "adjacent HELPDECO \\page markers"},
            "action": ACTION.decode(), "source_attachment_files": source_files,
            "media_markers": resources,
            "unknowns": ["Print text and article boundaries are not paper-verified.",
                         "Source attachment membership is inferred from the native SrcCopy action and matching directory.",
                         "Media conversion and placement have not been validated in a browser."]}


def build():
    iso = fingerprint(ISO)
    require(iso == EXPECTED_ISO, "CD2 ISO differs from recorded source")
    listing, version = iso_listing(ISO)
    extracted = tree_inventory(TREE)
    with tempfile.TemporaryDirectory(prefix="maso-cd2-inventory-") as temporary:
        fresh = extract_inventory(ISO, listing, Path(temporary))
        compare_trees(fresh, extracted)
    probe = tree_inventory(PROBE)
    source = next(row for row in extracted["files"] if row["path"] == "DATA/MASO2.M12")
    rtf = (PROBE / RTF).read_bytes()
    require(source["bytes"] == 125394639 and rtf.startswith(b"{\\rtf1"), "CD2 decoder probe differs")
    candidate = cd2_candidate(rtf, extracted, probe)
    require(fingerprint(ISO) == iso, "ISO changed during inventory")
    detail = {"schema_version": 1, "disc_id": "cd2", "iso": {"path": ISO.name, **iso},
              "iso_entries": listing, "extracted": {"root": TREE.name, **extracted},
              "probe": {"root": "private/cd2-probe/raw", **probe}, "candidate": candidate,
              "decoder": {"repository": "https://github.com/joncampbell123/helpdeco",
                          "revision": DECODER_REVISION, "arguments": ["../../../masocd-2/DATA/MASO2.M12", "/g"]},
              "extraction": {"tool_version": version,
                             "command": ["7z", "x", "-y", "-bd", "-bb0", "-o<TEMP>/disc", "masocd-2.iso"]}}
    raw = json_bytes(detail)
    summary = {"schema_version": 1, "disc_id": "cd2", "scope": "source_map_and_candidate",
               "iso": detail["iso"], "container": {"path": source["path"], "bytes": source["bytes"], "sha256": source["sha256"]},
               "counts": {"disc_files": len(extracted["files"]), "disc_directories": len(extracted["directories"]),
                          "list_files": sum(row["path"].startswith("DATA/LIST/") for row in extracted["files"]),
                          "source_directories": sum(row.startswith("DATA/SOURCE/") for row in extracted["directories"]),
                          "probe_files": len(probe["files"]), "rtf_pages": len(list(PAGE.finditer(rtf))) + 1},
               "probe_extensions": dict(sorted(Counter(Path(row["path"]).suffix.lower() or "(none)"
                                                       for row in probe["files"]).items())),
               "candidate": {key: candidate[key] for key in ("native_reference", "native_context", "index", "title_evidence", "issue_evidence", "rtf", "action", "unknowns")},
               "candidate_attachment_paths": [row["path"] for row in candidate["source_attachment_files"]],
               "candidate_media": {"markers": len(candidate["media_markers"]),
                                   "available": sum(row["available"] for row in candidate["media_markers"]),
                                   "missing_names": sorted({row["name"] for row in candidate["media_markers"] if not row["available"]})},
               "viewer_entry_point": "BIN/MASO2.EXE on the disc; shortcut-only setup per owner",
               "validation": {"iso_hash_matches_recorded": True, "fresh_iso_extraction_matches_tree": True,
                              "cd1_decoder_emits_cd2_rtf": True, "index_title_matches_rtf": True,
                              "body_decoded": False, "viewer_compared": False},
               "private_detail": {"path": str(OUTPUT.relative_to(ROOT)), "bytes": len(raw), "sha256": sha(raw)}}
    return summary, raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    try:
        summary, raw = build()
        if not args.write_record:
            require(json.loads(RECORD.read_bytes()) == summary, "Reviewed CD2 inventory differs")
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(raw)
        if args.write_record:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_bytes(json_bytes(summary))
        print(f"CD2 source verified: {summary['counts']}; candidate {REF} mapped")
    except (OSError, ValueError, KeyError, StopIteration, subprocess.SubprocessError) as error:
        print(f"CD2 inventory failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
