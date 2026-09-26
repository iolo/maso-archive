"""Map CD3 RTF topics, native labels, ordered media, and CAB actions."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

from tools.inventory_cd3_sources import OUTPUT as INVENTORY, PROBE, RECORD, ROOT
from tools.map_cd1_topic import require
from tools.recover_cd1_text import json_bytes

OUTPUT = ROOT / "build/cd3-preservation/candidates.json"
SUMMARY = ROOT / "data/catalog/preservation/cd3-candidates.json"
PAGE = re.compile(rb"(?<!\\)\\page\n")
FOOTNOTE = re.compile(rb"\{\\up ([+!#$])\}\{\\footnote\\pard\\plain\{\\up \1\} ([^}]+)\}")
MEDIA = re.compile(rb"\\\{(?:bmc|ewl) ([^}]+)\\\}")
CAB_ACTION = re.compile(rb"!fc\(([^)]+)\)", re.I)
ISSUE = re.compile(rb"([0-9]{2})\\'b3\\'e2\s+([0-9]{1,2})\\'bf\\'f9\\'c8\\'a3", re.I)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def decode(raw):
    data = re.sub(rb"\\'([0-9a-fA-F]{2})", lambda m: bytes.fromhex(m[1].decode()), raw)
    return data.decode("cp949")


def spans(rtf):
    pages = list(PAGE.finditer(rtf))
    require(pages, "CD3 RTF has no topic boundaries")
    return [(0, pages[0].start())] + [(a.end(), b.start()) for a, b in zip(pages, pages[1:])] + [(pages[-1].end(), len(rtf))]


def checked(path, record):
    raw = path.read_bytes()
    require(len(raw) == record["bytes"] and digest(raw) == record["sha256"], f"Changed source: {path}")
    return raw


def build():
    reviewed = json.loads(RECORD.read_bytes())
    inventory_raw = checked(INVENTORY, reviewed["private_detail"])
    inventory = json.loads(inventory_raw)
    probe = {row["path"]: row for row in inventory["probe"]["main"]["files"]}
    disc = {row["path"]: row for row in inventory["extracted"]["files"]}
    rtf = checked(PROBE / "main/raw/MASO3.rtf", probe["MASO3.rtf"])
    media_names = {name.lower(): name for name in probe if name.lower().endswith(".bmp")}
    require(len(media_names) == sum(name.lower().endswith(".bmp") for name in probe), "Case-conflicting media names")
    disc_names = {name.lower(): name for name in disc}
    topics = []
    aliases = {}
    for ordinal, (start, end) in enumerate(spans(rtf), 1):
        raw = rtf[start:end]
        footnotes = {key: [] for key in "+!#$"}
        for match in FOOTNOTE.finditer(raw):
            footnotes[match[1].decode()].append(decode(match[2]))
        require(len(footnotes["$"]) <= 1 and len(footnotes["!"]) <= 1,
                f"Ambiguous CD3 title or native category: topic {ordinal}")
        for alias in footnotes["#"]:
            require(alias not in aliases, f"Duplicate CD3 context alias: {alias}")
            aliases[alias] = ordinal
        labels = sorted({f"{int(year):02d}{int(month):02d}"
                         for year, month in ISSUE.findall(raw[:2500]) if 1 <= int(month) <= 12})
        resources = []
        for match in MEDIA.finditer(raw):
            command = match[1].decode("ascii")
            name = command.split("!")[-1].strip()
            require(re.fullmatch(r"[A-Za-z0-9_.-]+", name), f"Unsafe media name: {name}")
            actual = media_names.get(name.lower())
            target_match = re.search(rb"\{\\v ([^}]+)\}", raw[match.end():match.end() + 45]) if name.lower() == "click.bmp" else None
            target_alias = target_match[1].decode("ascii") if target_match else None
            resources.append({"name": name, "source_name": actual,
                              "rtf_byte_offset": start + match.start(), "available": actual is not None,
                              "target_alias": target_alias})
        attachments = []
        for match in CAB_ACTION.finditer(raw):
            argument = match[1].decode("ascii")
            normalized = re.sub(r"/+", "/", argument.replace("\\", "/"))
            require(re.fullmatch(r"[A-Za-z0-9_./ -]+", normalized) and ".." not in normalized,
                    f"Unsafe CAB action: {argument}")
            actual = disc_names.get(normalized.lower())
            attachments.append({"action": argument, "path": actual,
                                "rtf_byte_offset": start + match.start(), "available": actual is not None})
        title = footnotes["$"][0] if footnotes["$"] else None
        role = "article_candidate" if title else "author_bio" if footnotes["!"] == ["Author"] else "auxiliary_topic" if footnotes["#"] else "document_tail"
        topic = {"identity": f"topic-{ordinal:04d}", "ordinal": ordinal,
                 "role": role, "title": title, "category": footnotes["!"][0] if footnotes["!"] else None,
                 "context_aliases": footnotes["#"], "browse_refs": footnotes["+"],
                 "native_issue_labels": labels, "group": labels[0] if len(labels) == 1 else "undated",
                 "rtf": {"byte_offset": start, "byte_length": end - start, "sha256": digest(raw)},
                 "media": resources, "cab_actions": attachments,
                 "initial_outcome": "pending" if title else "classified"}
        topics.append(topic)
    for topic in topics:
        for item in topic["media"]:
            alias = item["target_alias"]
            target = topics[aliases[alias] - 1] if alias in aliases else None
            if target and target["role"] == "auxiliary_topic" and len(target["media"]) == 1:
                item["target_topic"] = target["identity"]
                item["target_media"] = {key: target["media"][0][key]
                                        for key in ("name", "source_name", "available")}
            else:
                item["target_topic"] = None
                item["target_media"] = None
    require(sum(t["rtf"]["byte_length"] for t in topics) <= len(rtf), "RTF topic accounting failed")
    detail = {"schema_version": 1, "disc_id": "cd3", "source_inventory_sha256": digest(inventory_raw),
              "candidate_basis": "CD3 native RTF title footnotes, with byte spans bounded by HELPDECO page markers",
              "topics": topics}
    raw = json_bytes(detail)
    candidates = [t for t in topics if t["role"] == "article_candidate"]
    summary = {"schema_version": 1, "disc_id": "cd3", "source_inventory_sha256": digest(inventory_raw),
               "counts": {"rtf_topics": len(topics), "article_candidates": len(candidates),
                          "author_bios": sum(t["role"] == "author_bio" for t in topics),
                          "auxiliary_topics": sum(t["role"] == "auxiliary_topic" for t in topics),
                          "document_tails": sum(t["role"] == "document_tail" for t in topics),
                          "media_occurrences": sum(len(t["media"]) for t in topics),
                          "article_media_occurrences": sum(len(t["media"]) for t in candidates),
                          "missing_media_occurrences": sum(not m["available"] for t in topics for m in t["media"]),
                          "figure_links": sum(m["target_alias"] is not None for t in candidates for m in t["media"]),
                          "resolved_figures": sum(m["target_media"] is not None for t in candidates for m in t["media"]),
                          "missing_figure_sources": sum(m["target_media"] is not None and not m["target_media"]["available"] for t in candidates for m in t["media"]),
                          "cab_actions": sum(len(t["cab_actions"]) for t in topics),
                          "missing_cab_actions": sum(not a["available"] for t in topics for a in t["cab_actions"])},
               "native_groups": dict(sorted(Counter(t["group"] for t in candidates).items())),
               "private_detail": {"path": str(OUTPUT.relative_to(ROOT)), "bytes": len(raw), "sha256": digest(raw)},
               "limitations": ["CD-native labels are not paper-verified magazine issue identities.",
                               "Some candidates carry 1994 or 1996 labels, or no unique issue label.",
                               "Untitled auxiliary topics and unassigned bitmaps are retained separately."]}
    return summary, raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    summary, raw = build()
    if not args.write_record:
        require(json.loads(SUMMARY.read_bytes()) == summary, "Reviewed CD3 candidate record differs")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(raw)
    if args.write_record:
        SUMMARY.parent.mkdir(parents=True, exist_ok=True)
        SUMMARY.write_bytes(json_bytes(summary))
    print("CD3 candidates:", summary["counts"], summary["native_groups"])


if __name__ == "__main__":
    main()
