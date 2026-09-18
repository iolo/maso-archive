"""Verify the single pilot metadata-match record against its source snapshots.

This is an evidence checker, not a matching engine. Run the two existing import
commands first. No RTF, images, or article bodies are read, and no files are written.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from tools.toc_snapshot import Snapshot

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECORD = ROOT / "data/catalog/source-matches/cd1-8802065.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def checked_artifact(directory, name):
    manifest = load(directory / "manifest.json")
    raw = (directory / name).read_bytes()
    expected = manifest["outputs"][name]
    require(len(raw) == expected["bytes"] and hashlib.sha256(raw).hexdigest() == expected["sha256"],
            f"Stale or modified import output: {directory.name}/{name}")
    return json.loads(raw) if name.endswith(".json") else [json.loads(line) for line in raw.splitlines()]


def verify(record):
    require(record["schema_version"] == 1 and record["cd_reference"] == "8802065", "Not the selected pilot record")
    require(record["scope"] == "metadata_only" and record["decision"] == "supported_by_metadata", "Unexpected decision scope")
    require(record["verification"] == {
        "printed_original_checked": False, "cd_page_mapping_verified": False,
        "rtf_topics_mapped": False, "body_complete": False, "images_verified": False, "viewer_compared": False,
    }, "This metadata-only check cannot verify content")
    require(record["publication_decision"] == "not_made", "This step makes no publication decision")
    evidence = record["evidence"]
    require(evidence["toc"]["path"] == "TOC.md", "Unexpected TOC source")
    require(evidence["cd_index_directory"] == "private/cd1-probe/raw", "Unexpected CD index directory")
    snapshot = Snapshot(ROOT)
    toc_raw = snapshot.read("TOC.md")
    require(hashlib.sha256(toc_raw).hexdigest() == evidence["toc"]["sha256"], "TOC snapshot is stale")
    toc_lines = toc_raw.decode("utf-8").splitlines()
    toc_entries = snapshot.artifact("toc-entries.jsonl")
    selected = [entry for entry in toc_entries if entry["id"] == record["toc_entry_id"]]
    require(len(selected) == 1, "TOC entry ID is missing or ambiguous")
    toc = selected[0]
    require(toc["issue_id"] == record["issue_id"], "Issue mismatch")
    require(evidence["toc"]["entry"] == {key: toc[key] for key in evidence["toc"]["entry"]}, "TOC entry evidence changed")
    registry = json.loads(snapshot.read("data/identities/toc.json"))
    require([entry for entry in registry["entries"] if entry["id"] == toc["id"]] == [
        {key: toc[key] for key in ("id", "issue_id", "raw_text", "depth")}
    ], "Persistent TOC identity changed")
    issues = snapshot.artifact("issues.json")
    heading = evidence["toc"]["issue_heading"]
    require([issue["source"] for issue in issues if issue["id"] == toc["issue_id"]] == [heading], "Issue heading changed")
    for locator in [heading, toc["source"]]:
        require(locator["id"] == f"toc-sha256-{evidence['toc']['sha256']}", "TOC provenance hash mismatch")
        require(toc_lines[locator["line_start"] - 1] == locator["raw_line"], "TOC source line mismatch")

    cd_entries = checked_artifact(ROOT / "build/cd1-index", "entries.jsonl")
    references = checked_artifact(ROOT / "build/cd1-index", "references.jsonl")
    groups = [group for group in references if group["reference"] == record["cd_reference"]]
    require(len(groups) == 1, "CD reference missing or ambiguous")
    occurrences = evidence["cd_occurrences"]
    occurrence_ids = [row["id"] for row in occurrences]
    require(occurrence_ids == groups[0]["occurrence_ids"] and len(set(occurrence_ids)) == 2,
            "The record must include both original CD occurrences")
    cd_by_id = {entry["id"]: entry for entry in cd_entries}
    for row in occurrences:
        require(row == {key: cd_by_id[row["id"]][key] for key in row}, "CD occurrence evidence changed")
        source = row["source"]
        require(source["name"] in ("column.lst", "panecmds.lst"), "Unexpected pilot index file")
        raw = (ROOT / evidence["cd_index_directory"] / source["name"]).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == source["sha256"], "CD index snapshot is stale")
        span = raw[source["byte_offset"]:source["byte_offset"] + source["byte_length"]]
        require(span.rstrip(b"\r\n").decode("cp949") == row["raw_line"], "CD source byte span mismatch")
        require(raw.decode("cp949").splitlines()[source["line"] - 1] == row["raw_line"], "CD source line mismatch")
        require(row["reference"] == record["cd_reference"], "CD target mismatch")

    comparison = record["comparison"]
    title = comparison["title"]
    require(title["toc_prefix_removed"] == "특집 : " and title["toc_suffix_removed"] == "?"
            and title["application"] == "this_record_only", "Unexpected title comparison")
    normalized = toc["title_candidate"].removeprefix(title["toc_prefix_removed"]).removesuffix(title["toc_suffix_removed"])
    require(normalized == title["compared_title"] and all(row["title"] == normalized for row in occurrences), "Title mismatch")
    matches = [entry["id"] for entry in toc_entries if entry["issue_id"] == toc["issue_id"]
               and entry["title_candidate"].removeprefix(title["toc_prefix_removed"]).removesuffix(title["toc_suffix_removed"]) == normalized]
    require(matches == comparison["uniqueness"]["matching_toc_entry_ids"] == [toc["id"]], "Match is not unique within the issue")
    require(comparison["issue"] == {"toc_issue": "1988-02", "cd_display_issue": "1988-02", "agreement": "explicit_labels"}
            and toc["issue_id"] == "maso-1988-02" and all(row["display_issue"] == "1988-02" for row in occurrences), "Issue evidence mismatch")
    require(comparison["page"] == {
        "toc_reported_page": toc["start_page_candidate"], "reference_suffix": record["cd_reference"][-3:],
        "page_candidate_from_reference": int(record["cd_reference"][-3:]),
        "standalone_cd_page_label_observed": False, "agreement": "conditional_on_unverified_reference_format",
    } and toc["start_page_candidate"] == 65, "Page claim must remain conditional on the reference format")
    require(comparison["structure"] == {"toc_is_leaf": True, "toc_has_feature_label": True, "cd_topic_cardinality": "unverified"}
            and not any(entry["parent_id"] == toc["id"] for entry in toc_entries), "Feature structure needs review")
    require(comparison["author"] == {"toc_byline": None, "cd_index_byline": "not_provided", "comparison": "not_possible"}
            and toc["byline_candidate"] is None, "No author comparison is supported")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, default=DEFAULT_RECORD)
    args = parser.parse_args()
    try:
        record = load(args.record)
        verify(record)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(f"Pilot match check failed: {exc}", file=sys.stderr)
        return 1
    print(f"Metadata evidence checked: {record['cd_reference']} -> {record['toc_entry_id']}; 2 CD occurrences. Content remains unverified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
