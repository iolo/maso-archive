"""Verify CD3 reference coverage, source bindings, text, media, and links."""

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

from tools.build_cd3_reference import OUTPUT, check_links, load
from tools.build_cd2_reference import verify_package
from tools.inventory_cd3_sources import PROBE, ROOT, TREE
from tools.map_cd1_topic import require
from tools.map_cd3_candidates import digest, checked
from tools.recover_cd1_text import json_bytes

RECORD = ROOT / "data/catalog/preservation/cd3-readable-reference.json"


def verify():
    source, queue, probe_files, disc_files, rtf, queue_hash = load()
    manifest = verify_package(OUTPUT)
    require(manifest["source_queue_sha256"] == queue_hash, "Root source queue differs")
    catalog = json.loads((OUTPUT / "catalog.json").read_bytes())
    require(catalog["source_queue_sha256"] == queue_hash, "Catalog source queue differs")
    candidates = [t for t in queue["topics"] if t["role"] == "article_candidate"]
    source_by_id = {t["identity"]: t for t in candidates}
    rows = catalog["articles"]
    require(len(rows) == len(source_by_id) and {r["identity"] for r in rows} == set(source_by_id),
            "Article candidate coverage differs")
    require(Counter(r["status"] for r in rows) == catalog["outcomes"], "Outcome counts differ")
    groups = sorted({t["group"] for t in candidates})
    require(sorted(catalog["groups"]) == groups and
            sorted(p.name for p in (OUTPUT / "groups").iterdir()) == groups,
            "CD-native group coverage differs")
    for group in groups:
        package = OUTPUT / "groups" / group
        group_manifest = verify_package(package)
        require(group_manifest["source_queue_sha256"] == queue_hash, "Group queue differs")
        group_rows = json.loads((package / "articles.json").read_bytes())["articles"]
        require(group_rows == [r for r in rows if r["group"] == group], "Group article records differ")
        require(group_manifest["candidates"] == len(group_rows) and
                Counter(r["status"] for r in group_rows) == group_manifest["outcomes"],
                "Group coverage differs")
    media_count = 0
    attachment_count = 0
    for row in rows:
        topic = source_by_id[row["identity"]]
        require(row["group"] == topic["group"] and row["title"] == topic["title"],
                "Article identity or title differs")
        span = topic["rtf"]
        raw = rtf[span["byte_offset"]:span["byte_offset"] + span["byte_length"]]
        require(digest(raw) == span["sha256"], "RTF topic differs")
        article = OUTPUT / "groups" / row["group"] / "articles" / row["identity"]
        blocks = json.loads((article / "blocks.json").read_bytes())
        require(blocks["source"] == span and blocks["candidate"] == topic,
                "Article source blocks differ")
        page = (article / "index.html").read_text(encoding="utf-8")
        figure_targets = {m["target_topic"] for m in topic["media"] if m["target_topic"]}
        for link in topic["links"]:
            target_id = link["target_topic"]
            if target_id is None or target_id in figure_targets:
                continue
            target_topic = queue["topics"][int(target_id.split("-")[1]) - 1]
            if target_topic["role"] == "article_candidate":
                href = f"../../../../groups/{target_topic['group']}/articles/{target_id}/index.html"
            else:
                href = f"../../../../supplements/{target_id}/index.html"
            require(f'href="{href}"' in page, "Article linked topic omitted")
        text = (article / "article.txt").read_text(encoding="utf-8")
        if row["status"] == "failed":
            require("error" in blocks and not text, "Failed article has unaccounted text")
        else:
            expected = []
            occurrences = []
            media_index = 0
            for paragraph in blocks["paragraphs"]:
                for run in paragraph["runs"]:
                    if run["type"] == "media":
                        item = topic["media"][media_index]
                        media_index += 1
                        if item["target_alias"] and item["target_media"] is None:
                            expected.append(f"[figure:{item['target_alias']} · target unresolved]")
                        elif item["target_media"] is not None:
                            expected.append(f"[figure:{item['target_media']['name']}]")
                        else:
                            expected.append(f"[image:{run['resource']}]")
                        occurrences.append(run["resource"])
                    else:
                        expected.append(run["text"])
                if paragraph["terminated"]:
                    expected.append("\n")
            require(text == "".join(expected) and digest(text.encode()) == row["text_sha256"],
                    "Article text or whitespace differs")
            require(occurrences == [m["name"] for m in topic["media"]] and
                    row["media_occurrences"] == len(occurrences), "Article media order differs")
            require(row["figure_links"] == sum(m["target_alias"] is not None for m in topic["media"]) and
                    row["resolved_figures"] == sum(m["target_media"] is not None for m in topic["media"]),
                    "Figure associations differ")
            require(row["paragraphs"] == len(blocks["paragraphs"]) and
                    row["issue_records"] == len(blocks["issues"]), "Article block counts differ")
        media_count += row["media_occurrences"]
        require(len(row["attachments"]) <= len(topic["cab_actions"]), "Unexpected attachment")
        for attachment in row["attachments"]:
            path = attachment["source_path"]
            require(path in disc_files and path in source["cab_members"], "Uninventoried CAB")
            original = checked(TREE / path, disc_files[path])
            copied = (article / attachment["path"]).read_bytes()
            require(copied == original and attachment["sha256"] == digest(original),
                    "Attachment bytes differ")
            attachment_count += 1
    require(media_count == sum(len(t["media"]) for t in candidates), "Article media count differs")
    for group in groups:
        media = json.loads((OUTPUT / "groups" / group / "media.json").read_bytes())["resources"]
        for item in media:
            name = item["name"]
            require(name in probe_files, "Media source unlisted")
            original = checked(PROBE / "main/raw" / name, probe_files[name])
            require((OUTPUT / "groups" / group / "media" / name).read_bytes() == original,
                    "Media original differs")
            preview = OUTPUT / "groups" / group / "media" / (name + ".png")
            require(preview.exists() == (item["preview_sha256"] is not None),
                    "Media preview status differs")
            if preview.exists():
                require(digest(preview.read_bytes()) == item["preview_sha256"],
                        "Media preview differs")
    supplements = json.loads((OUTPUT / "supplements.json").read_bytes())["topics"]
    other = [t for t in queue["topics"] if t["role"] != "article_candidate"]
    require(len(supplements) == len(other) and
            {t["identity"] for t in supplements} == {t["identity"] for t in other},
            "Auxiliary topic coverage differs")
    require(Counter(t["status"] for t in supplements) == catalog["supplement_outcomes"],
            "Supplement outcomes differ")
    other_by_id = {t["identity"]: t for t in other}
    for record in supplements:
        topic = other_by_id[record["identity"]]
        require(record["rtf"] == topic["rtf"] and record["media"] == topic["media"],
                "Supplement source differs")
        directory = OUTPUT / "supplements" / topic["identity"]
        blocks = json.loads((directory / "blocks.json").read_bytes())
        require(blocks["source"] == topic["rtf"] and blocks["topic"] == topic,
                "Supplement blocks differ")
        text = (directory / "text.txt").read_text(encoding="utf-8")
        if record["status"] == "failed":
            require("error" in blocks and not text, "Failed supplement has unaccounted text")
        else:
            expected, occurrences = [], []
            for paragraph in blocks["paragraphs"]:
                for run in paragraph["runs"]:
                    if run["type"] == "media":
                        expected.append(f"[image:{run['resource']}]")
                        occurrences.append(run["resource"])
                    else:
                        expected.append(run["text"])
                if paragraph["terminated"]:
                    expected.append("\n")
            require(text == "".join(expected) and digest(text.encode()) == record["text_sha256"],
                    "Supplement text differs")
            require(occurrences == [m["name"] for m in topic["media"]] and
                    record["issue_records"] == len(blocks["issues"]),
                    "Supplement media or issue records differ")
    source_media = json.loads((OUTPUT / "media-sources.json").read_bytes())["resources"]
    require({m["name"] for m in source_media} ==
            {p for p in probe_files if p.lower().endswith(".bmp")},
            "Decoded media coverage differs")
    for item in source_media:
        original = checked(PROBE / "main/raw" / item["name"], probe_files[item["name"]])
        require((OUTPUT / "media-sources" / item["name"]).read_bytes() == original,
                "Decoded media original differs")
    used = {m["source_name"] for t in queue["topics"] for m in t["media"] if m["source_name"]}
    unassigned = json.loads((OUTPUT / "unassigned-media.json").read_bytes())["resources"]
    expected_unassigned = {p for p in probe_files if p.lower().endswith(".bmp")} - used
    require({m["name"] for m in unassigned} == expected_unassigned,
            "Unassigned media coverage differs")
    for item in unassigned:
        original = checked(PROBE / "main/raw" / item["name"], probe_files[item["name"]])
        require((OUTPUT / "unassigned-media" / item["name"]).read_bytes() == original,
                "Unassigned media original differs")
    check_links(OUTPUT)
    result = {"schema_version": 1, "disc_id": "cd3", "scope": "private_readable_reference",
              "source_queue_sha256": queue_hash,
              "output_manifest": {"path": str((OUTPUT / "manifest.json").relative_to(ROOT)),
                                  "sha256": digest((OUTPUT / "manifest.json").read_bytes())},
              "counts": {"article_candidates": len(rows), "groups": len(groups),
                         "success": catalog["outcomes"].get("success", 0),
                         "partial": catalog["outcomes"].get("partial", 0),
                         "failed": catalog["outcomes"].get("failed", 0),
                         "supplemental_topics": len(supplements),
                         "supplement_success": catalog["supplement_outcomes"].get("success", 0),
                         "supplement_partial": catalog["supplement_outcomes"].get("partial", 0),
                         "supplement_failed": catalog["supplement_outcomes"].get("failed", 0),
                         "source_media": len(source_media),
                         "unassigned_media": len(unassigned),
                         "article_media_occurrences": media_count,
                         "figure_links": sum(r["figure_links"] for r in rows),
                         "resolved_figures": sum(r["resolved_figures"] for r in rows),
                         "copied_cab_actions": attachment_count,
                         "output_files": len(manifest["files"])},
              "validation": {"all_candidate_outcomes_accounted": True,
                             "all_auxiliary_topics_classified": True,
                             "text_and_whitespace_match_blocks": True,
                             "media_and_cab_sources_match": True,
                             "all_html_links_resolve": True,
                             "output_files_match_manifest": True},
              "limits": ["CD3 labels and text have not been compared with paper magazines.",
                         "An original viewer comparison was not needed to resolve the mapped source relationships."]}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    try:
        result = verify()
        if args.write_record:
            RECORD.write_bytes(json_bytes(result))
        else:
            require(json.loads(RECORD.read_bytes()) == result, "Reviewed CD3 reference record differs")
        print("CD3 reference verified:", result["counts"])
    except (OSError, ValueError, KeyError, IndexError) as error:
        print(f"CD3 reference verification failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
