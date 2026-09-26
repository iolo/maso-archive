"""Verify the private CD2 reference against its source queue and output records."""

import argparse
from collections import Counter
import json
from pathlib import Path

from tools.build_cd2_reference import (ISSUES, OUTPUT, check_html_links, checked,
                                       digest, load, verify_package)
from tools.inventory_cd2_sources import ROOT, RECORD
from tools.map_cd1_topic import require
from tools.map_cd2_candidates import SUMMARY as QUEUE_RECORD
from tools.recover_cd1_text import json_bytes

RECORD_OUT = ROOT / "data/catalog/preservation/cd2-readable-reference.json"


def verify():
    queue, probe_files, disc_files, rtf = load()
    root = json.loads((OUTPUT / "manifest.json").read_bytes())
    coverage_raw = (OUTPUT / "coverage.json").read_bytes()
    coverage = json.loads(coverage_raw)
    require(root["disc_id"] == coverage["disc_id"] == "cd2" and
            root["coverage_sha256"] == digest(coverage_raw), "CD2 root/coverage identity differs")
    actual_root = {p.relative_to(OUTPUT).as_posix() for p in OUTPUT.rglob("*") if p.is_file() and
                   not p.relative_to(OUTPUT).parts[0] == "issues"}
    listed_root = {row["path"] for row in root["files"]} | {"manifest.json"}
    require(actual_root == listed_root, "CD2 root file inventory differs")
    for row in root["files"]:
        checked(OUTPUT / row["path"], row)
    candidates = {row["reference"]: row for row in queue["candidates"]}
    candidates.update({row["identity"]: row for row in queue["additional_article_candidates"]})
    require(coverage["candidate_count"] == len(candidates) == 1330, "CD2 candidate count differs")
    observed = {}
    media_statuses = Counter()
    media_occurrences = 0
    media_records = 0
    files_checked = len(root["files"])
    for issue in ISSUES:
        issue_path = OUTPUT / "issues" / issue
        manifest = verify_package(issue_path)
        files_checked += len(manifest["files"])
        report = next(row for row in coverage["issues"] if row["issue_group"] == issue)
        require(report["manifest_sha256"] == digest((issue_path / "manifest.json").read_bytes()) and
                report["candidates"] == manifest["candidates"] and
                report["outcomes"] == manifest["outcomes"], "CD2 issue coverage differs")
        articles = json.loads((issue_path / "articles.json").read_bytes())["articles"]
        resources = json.loads((issue_path / "media.json").read_bytes())["resources"]
        require(len(articles) == manifest["candidates"] and len(resources) == manifest["media_resources"],
                "CD2 issue article/media records differ")
        resource_by_name = {item["name"]: item for item in resources}
        require(len(resource_by_name) == len(resources), "Duplicate CD2 issue media")
        for name, item in resource_by_name.items():
            require(item["original_sha256"] == probe_files[name]["sha256"], "Media source fingerprint differs")
            require(digest((issue_path / "media" / name).read_bytes()) == item["original_sha256"],
                    "CD2 original media differs")
            preview = issue_path / "media" / f"{name}.png"
            require((preview.is_file() and digest(preview.read_bytes()) == item["preview_sha256"])
                    if item["preview_sha256"] else not preview.exists(), "CD2 media preview state differs")
            media_statuses[item["status"]] += 1
        for article in articles:
            identity = article["id"]
            require(identity in candidates and identity not in observed, "Duplicate/uninventoried CD2 article")
            candidate = candidates[identity]
            require(candidate["issue_group"] == issue and article["topic_ordinal"] == candidate["topic_ordinal"],
                    "CD2 article group/topic differs")
            span = candidate["rtf"]
            raw = rtf[span["byte_offset"]:span["byte_offset"]+span["byte_length"]]
            require(digest(raw) == span["sha256"], "CD2 article source span differs")
            source_media = [item["name"] for item in candidate["media"]]
            require(article["media_occurrences"] == len(source_media) and
                    article["resources"] == list(dict.fromkeys(source_media)),
                    "CD2 article/media source relationship differs")
            require(set(article["resources"]) <= set(resource_by_name), "CD2 article media not exported")
            media_occurrences += len(source_media)
            expected_actions = {(action["kind"], path) for action in candidate["actions"] for path in action["paths"]}
            actual_actions = {(attachment["kind"], attachment["source_path"]) for attachment in article["attachments"]}
            require(expected_actions == actual_actions, "CD2 source/list attachment mapping differs")
            article_dir = issue_path / "articles" / identity
            raw_text = (article_dir / "article.txt").read_bytes()
            require(digest(raw_text) == article["text_sha256"] and
                    len(raw_text.decode("utf-8")) == article["text_characters"],
                    "CD2 article text differs")
            for attachment in article["attachments"]:
                source = checked(ROOT / "masocd-2" / attachment["source_path"],
                                 disc_files[attachment["source_path"]])
                require(digest((article_dir / attachment["path"]).read_bytes()) ==
                        attachment["sha256"] == digest(source), "CD2 attachment differs")
                if attachment["kind"] == "ListView":
                    try:
                        text = source.decode("cp949")
                    except UnicodeDecodeError:
                        continue
                    converted = article_dir / "listings" / (Path(attachment["source_path"]).stem + ".txt")
                    require(converted.read_bytes() == text.encode("utf-8"), "CD2 listing characters/whitespace differ")
            observed[identity] = article
        media_records += len(resources)
        require(report["media_occurrences"] == manifest["media_occurrences"] and
                report["media_statuses"] == dict(sorted(Counter(item["status"] for item in resources).items())),
                "CD2 issue media coverage differs")
    require(set(observed) == set(candidates), "CD2 candidate outcomes incomplete")
    require(coverage["articles"] == [article for issue in ISSUES for article in
                                     json.loads((OUTPUT / "issues" / issue / "articles.json").read_bytes())["articles"]],
            "CD2 coverage article records differ")
    require(coverage["outcomes"] == dict(sorted(Counter(row["status"] for row in observed.values()).items())),
            "CD2 article outcome counts differ")
    require(coverage["media_occurrences"] == media_occurrences == 2661 and
            coverage["media_resource_records"] == media_records and
            coverage["media_statuses"] == dict(sorted(media_statuses.items())),
            "CD2 total media accounting differs")
    supplements = json.loads((OUTPUT / "supplements.json").read_bytes())["topics"]
    require(len(supplements) == coverage["untitled_topics"] == 58 and
            coverage["supplement_classes"] == dict(sorted(Counter(row["kind"] for row in supplements).items())),
            "CD2 untitled topic classification differs")
    for row in supplements:
        span = row["source"]
        require(digest(rtf[span["byte_offset"]:span["byte_offset"]+span["byte_length"]]) == span["sha256"],
                "CD2 supplement source span differs")
        require(digest((OUTPUT / "supplements" / f"{row['ordinal']}.txt").read_bytes()) == row["text_sha256"],
                "CD2 supplement text differs")
    unassigned = json.loads((OUTPUT / "unassigned-media.json").read_bytes())["resources"]
    article_media = {item["name"] for row in candidates.values() for item in row["media"]}
    all_probe_media = {name for name in probe_files if name.lower().endswith((".dib", ".wmf", ".bmp"))}
    require({row["name"] for row in unassigned} == all_probe_media - article_media and
            len(unassigned) == coverage["unassigned_media_resources"],
            "CD2 unassigned decoder media coverage differs")
    unassigned_statuses = Counter()
    for item in unassigned:
        name = item["name"]
        require(item["original_sha256"] == probe_files[name]["sha256"] and
                digest((OUTPUT / "unassigned-media" / name).read_bytes()) == item["original_sha256"],
                "CD2 unassigned original media differs")
        preview = OUTPUT / "unassigned-media" / f"{name}.png"
        require((preview.is_file() and digest(preview.read_bytes()) == item["preview_sha256"])
                if item["preview_sha256"] else not preview.exists(),
                "CD2 unassigned preview state differs")
        unassigned_statuses[item["status"]] += 1
    require(coverage["unassigned_media_statuses"] == dict(sorted(unassigned_statuses.items())),
            "CD2 unassigned media status count differs")
    check_html_links(OUTPUT)
    source_record = json.loads(RECORD.read_bytes())
    queue_record = json.loads(QUEUE_RECORD.read_bytes())
    return {"schema_version": 1, "disc_id": "cd2", "scope": "private_readable_reference",
            "iso_sha256": source_record["iso"]["sha256"],
            "candidate_map_sha256": queue_record["private_detail"]["sha256"],
            "output_manifest_sha256": digest((OUTPUT / "manifest.json").read_bytes()),
            "coverage_sha256": digest(coverage_raw), "candidate_count": len(observed),
            "outcomes": coverage["outcomes"], "media_occurrences": media_occurrences,
            "media_resource_records": media_records, "media_statuses": dict(sorted(media_statuses.items())),
            "unassigned_media_resources": len(unassigned),
            "unassigned_media_statuses": dict(sorted(unassigned_statuses.items())),
            "untitled_topic_classes": coverage["supplement_classes"],
            "output_files_verified": files_checked, "all_html_links_resolve": True,
            "paper_review": "pending"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.write_record:
        RECORD_OUT.parent.mkdir(parents=True, exist_ok=True)
        RECORD_OUT.write_bytes(json_bytes(result))
    else:
        require(json.loads(RECORD_OUT.read_bytes()) == result, "Reviewed CD2 reference record differs")
    print(result)


if __name__ == "__main__":
    main()
