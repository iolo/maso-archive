"""Map every CD-native CD2 index reference to a checksummed RTF topic."""

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

from tools.inventory_cd2_sources import PROBE, ROOT, RECORD
from tools.map_cd1_topic import context_hash, require
from tools.recover_cd1_text import json_bytes

OUTPUT = ROOT / "build/cd2-preservation/candidates.json"
SUMMARY = ROOT / "data/catalog/preservation/cd2-candidates.json"
PAGE = re.compile(rb"(?<!\\)\\page\n")
CONTEXT = re.compile(rb"\{\\up #\}\{\\footnote\\pard\\plain\{\\up #\} ([^}]+)\}")
TITLE = re.compile(rb"\{\\up \$\}\{\\footnote\\pard\\plain\{\\up \$\} ([^}]+)\}")
ACTION = re.compile(rb"\{\\v !?(SrcCopy|ListView)\(([0-9]+)\)\}")
MEDIA = re.compile(rb"\\\{(?:bmc|ewl) ([^}]+)\\\}")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def decode_footnote(raw):
    data = re.sub(rb"\\'([0-9a-fA-F]{2})", lambda m: bytes.fromhex(m[1].decode()), raw)
    return data.decode("cp949")


def topic_spans(rtf):
    pages = list(PAGE.finditer(rtf))
    require(pages, "No RTF pages")
    return [(0, pages[0].start())] + [(a.end(), b.start()) for a, b in zip(pages, pages[1:])] + [(pages[-1].end(), len(rtf))]


def build():
    reviewed = json.loads(RECORD.read_bytes())
    detail_raw = (ROOT / reviewed["private_detail"]["path"]).read_bytes()
    require(digest(detail_raw) == reviewed["private_detail"]["sha256"], "Source inventory changed")
    detail = json.loads(detail_raw)
    rtf = (PROBE / "MASO2.rtf").read_bytes()
    expected = next(row for row in detail["probe"]["files"] if row["path"] == "MASO2.rtf")
    require(digest(rtf) == expected["sha256"], "RTF differs from source inventory")
    media_files = {row["path"] for row in detail["probe"]["files"]}
    disc_files = {row["path"] for row in detail["extracted"]["files"]}
    contexts = {}
    topics = []
    for ordinal, (start, end) in enumerate(topic_spans(rtf), 1):
        raw = rtf[start:end]
        aliases = [m[1].decode("ascii") for m in CONTEXT.finditer(raw)]
        names = [decode_footnote(m[1]) for m in TITLE.finditer(raw)]
        topic = {"ordinal": ordinal, "rtf": {"byte_offset": start, "byte_length": end-start,
                                               "sha256": digest(raw)},
                 "context_aliases": aliases, "title_footnotes": names}
        for alias in aliases:
            value = context_hash(alias)
            require(value not in contexts, "Duplicate CD2 context hash")
            contexts[value] = topic
        topics.append(topic)
    rows = []
    seen_refs = set()
    for index in ("book.lst", "info.lst", "qnatip.lst"):
        source = (PROBE / index).read_bytes()
        indexed = next(row for row in detail["probe"]["files"] if row["path"] == index)
        require(digest(source) == indexed["sha256"], f"Changed native index: {index}")
        for line, entry in enumerate(source.decode("cp949").splitlines(), 1):
            require(entry.count("^") == 1, f"Unparsed {index}:{line}")
            index_title, ref = entry.split("^", 1)
            require(re.fullmatch(r"[0-9]{9}", ref) and ref not in seen_refs,
                    f"Invalid or duplicate native reference: {ref}")
            seen_refs.add(ref)
            topic = contexts.get(context_hash(ref))
            require(topic is not None and len(topic["title_footnotes"]) == 1,
                    f"Index reference does not resolve uniquely: {ref}")
            span = topic["rtf"]
            raw = rtf[span["byte_offset"]:span["byte_offset"]+span["byte_length"]]
            actions = [{"kind": m[1].decode(), "argument": m[2].decode(),
                        "rtf_byte_offset": span["byte_offset"]+m.start()} for m in ACTION.finditer(raw)]
            attachments = []
            for action in actions:
                if action["kind"] == "SrcCopy":
                    paths = sorted(path for path in disc_files if path.startswith("DATA/SOURCE/"+action["argument"]+"/"))
                else:
                    target = "DATA/LIST/"+action["argument"]+".TXT"
                    paths = [target] if target in disc_files else []
                attachments.append({**action, "paths": paths, "available": bool(paths)})
            media = []
            for m in MEDIA.finditer(raw):
                command = m[1].decode("ascii")
                resource = command.split("!")[-1].strip() if "!" in command else command.strip()
                require(re.fullmatch(r"[A-Za-z0-9_.]+", resource), f"Unsafe CD2 media name: {resource}")
                media.append({"name": resource, "rtf_byte_offset": span["byte_offset"]+m.start(),
                              "available": resource in media_files})
            rows.append({"reference": ref, "index": index, "index_line": line,
                         "index_title": index_title,
                         "rtf_title": topic["title_footnotes"][0],
                         "title_agrees": index_title == topic["title_footnotes"][0],
                         "issue_group": ref[:4], "context_aliases": topic["context_aliases"],
                         "topic_ordinal": topic["ordinal"], "rtf": span,
                         "actions": attachments, "media": media,
                         "initial_outcome": "pending"})
    require(len(rows) == len(seen_refs), "Candidate count mismatch")
    mapped = {row["topic_ordinal"] for row in rows}
    unindexed = [topic for topic in topics if topic["ordinal"] not in mapped]
    additional = []
    for topic in unindexed:
        if not topic["title_footnotes"]:
            continue
        require(len(topic["title_footnotes"]) == 1, "Ambiguous unindexed title")
        span = topic["rtf"]
        head = rtf[span["byte_offset"]:span["byte_offset"]+min(span["byte_length"], 700)]
        label = re.search(rb"94\.\\\{vfld21\\\}([0-9]{1,2})\\\{vfld(?:[0-9]*)\\\}\.\s+[0-9]+p", head)
        issue_group = "94" + f"{int(label[1]):02d}" if label else None
        topic_raw = rtf[span["byte_offset"]:span["byte_offset"]+span["byte_length"]]
        extra_actions = []
        for m in ACTION.finditer(topic_raw):
            kind, argument = m[1].decode(), m[2].decode()
            if kind == "SrcCopy":
                paths = sorted(path for path in disc_files if path.startswith("DATA/SOURCE/"+argument+"/"))
            else:
                target = "DATA/LIST/"+argument+".TXT"
                paths = [target] if target in disc_files else []
            extra_actions.append({"kind": kind, "argument": argument, "paths": paths,
                                  "available": bool(paths), "rtf_byte_offset": span["byte_offset"]+m.start()})
        extra_media = []
        for m in MEDIA.finditer(topic_raw):
            command = m[1].decode("ascii")
            resource = command.split("!")[-1].strip() if "!" in command else command.strip()
            require(re.fullmatch(r"[A-Za-z0-9_.]+", resource), "Unsafe unindexed media name")
            extra_media.append({"name": resource, "rtf_byte_offset": span["byte_offset"]+m.start(),
                                "available": resource in media_files})
        additional.append({"identity": f"unindexed-topic-{topic['ordinal']}",
                           "title": topic["title_footnotes"][0], "topic_ordinal": topic["ordinal"],
                           "context_aliases": topic["context_aliases"], "rtf": span,
                           "issue_group": issue_group,
                           "issue_evidence": "RTF printed label with unresolved dynamic fields" if label else "none",
                           "actions": extra_actions, "media": extra_media,
                           "initial_outcome": "pending"})
    by_issue = Counter(row["issue_group"] for row in rows)
    by_issue.update(row["issue_group"] for row in additional if row["issue_group"])
    detail_out = {"schema_version": 1, "disc_id": "cd2", "source_inventory_sha256": digest(detail_raw),
                  "candidate_basis": "CD-native index entries resolved by WinHelp context hash to unique RTF topics",
                  "candidates": sorted(rows, key=lambda row: (row["issue_group"], row["topic_ordinal"])),
                  "additional_article_candidates": additional,
                  "unindexed_topics": unindexed}
    raw_out = json_bytes(detail_out)
    all_candidates = rows + additional
    summary = {"schema_version": 1, "disc_id": "cd2", "source_inventory_sha256": digest(detail_raw),
               "counts": {"candidates": len(rows)+len(additional), "indexed_candidates": len(rows),
                          "unindexed_title_candidates": len(additional), "indexed_topics": len(mapped),
                          "rtf_topics": len(topics), "unindexed_topics": len(topics)-len(mapped),
                          "title_differences": sum(not row["title_agrees"] for row in rows),
                          "media_occurrences": sum(len(row["media"]) for row in all_candidates),
                          "unavailable_media_occurrences": sum(not m["available"] for row in all_candidates for m in row["media"]),
                          "actions": sum(len(row["actions"]) for row in all_candidates),
                          "unavailable_actions": sum(not action["available"] for row in all_candidates for action in row["actions"])},
               "index_counts": dict(Counter(row["index"] for row in rows)),
               "issue_groups": dict(sorted(by_issue.items())),
               "private_detail": {"path": str(OUTPUT.relative_to(ROOT)), "bytes": len(raw_out),
                                  "sha256": digest(raw_out)},
               "limitations": ["Index entries are CD-native candidates, not paper-verified article or issue records.",
                               "Unindexed RTF topics need separate classification.",
                               "Title differences retain both native index and RTF strings."]}
    return summary, raw_out


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    summary, raw = build()
    if not args.write_record:
        require(json.loads(SUMMARY.read_bytes()) == summary, "Candidate record differs")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(raw)
    if args.write_record:
        SUMMARY.parent.mkdir(parents=True, exist_ok=True)
        SUMMARY.write_bytes(json_bytes(summary))
    print(summary["counts"], summary["issue_groups"])


if __name__ == "__main__":
    main()
