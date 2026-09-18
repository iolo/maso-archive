"""Read-only February 1988 coverage audit against reviewed source snapshots.

No recovery/build functions are called. Only metadata enters the tracked report.
The live TOC may grow; the imported snapshot remains independently checksummed.
"""

import argparse
from collections import Counter
import hashlib
import json
import sys

from maso_archive.cd1_index import INDEX_NAMES, group_references, parse_index
from maso_archive.reading_room_package import checked_file, file_record, load_package
from maso_archive.toc import assign_identities, finalize_entries, json_bytes, parse_toc
from tools.map_cd1_topic import ROOT, SOURCES, context_entries, context_hash, require
from tools.verify_cd1_match import checked_artifact, load
from tools.toc_snapshot import Snapshot

ISSUE = "maso-1988-02"
TOC_SHA = "7d4386d31559383e8ddf14ca60dcaa3464aef52cf4d3ac50ca5a993ab422e34e"
TOC_BLOB = "e9db6b0e2889002a1159187bb6100d5f0d9f2d09"
RECORD = ROOT / "data/catalog/issue-coverage/cd1-1988-02.json"
PACKAGE = "build/cd1-second-article/8802114/combined/content"
# Explicit comparisons apply only to these records, never as fuzzy match rules.
TITLE_COMPARISONS = {
    "8802065": ("특집 : 유닉스란 무엇인가?", "유닉스란 무엇인가", "record_specific_prefix_and_question_mark"),
    "8802030": ("유명한 프로그래머를 만났읍니다(5) : CP/M의 게리 킬달", "CP/M의 게리 킬달", "record_specific_series_prefix"),
    "8802180": ("터보 파스칼 한글 그래픽스 툴", "터보 파스칼 한글 그래픽 툴", "unresolved_title_variant"),
}


def issue_text(raw, heading="## 88.02"):
    lines = raw.decode("utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if line == heading]
    require(len(starts) == 1, "Issue heading missing or duplicated")
    start = starts[0]
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start:end]


def audit_issue(toc, entries, contexts, prepared, comparisons=None):
    """Account for both populations; absent index evidence never means absent CD text."""
    comparisons = TITLE_COMPARISONS if comparisons is None else comparisons
    toc = [row for row in toc if row["issue_id"] == ISSUE]
    require(len({row["id"] for row in toc}) == len(toc), "Duplicate TOC identities")
    require([row["order"] for row in toc] == sorted({row["order"] for row in toc}), "TOC source order changed")
    require(len({row["id"] for row in entries}) == len(entries), "Duplicate index identities")
    by_id = {row["id"]: row for row in entries}
    references = []
    for group in group_references(entries):
        occurrences = [by_id[key] for key in group["occurrence_ids"]]
        labels = sorted({row["display_issue"] for row in occurrences if row["display_issue"]})
        if group["issue_candidate"] != "1988-02" and "1988-02" not in labels:
            continue
        explicit_issue = all(row["display_issue"] == "1988-02" for row in occurrences)
        conflict = any(label != "1988-02" for label in labels) or group["issue_candidate"] not in (None, "1988-02")
        titles = group["title_variants"]
        rule = "exact_title"
        candidates = [row for row in toc if titles == [row["title_candidate"]] and row["kind_candidate"] != "section"]
        comparison = comparisons.get(group["reference"])
        if comparison and not candidates and titles == [comparison[1]]:
            candidates = [row for row in toc if row["title_candidate"] == comparison[0]]
            rule = comparison[2]
        status = "unmatched"
        if candidates:
            status = "supported_by_metadata" if len(candidates) == 1 and explicit_issue and not conflict and rule != "unresolved_title_variant" else "ambiguous"
        native = contexts.get(context_hash(group["reference"]))
        package = prepared.get(group["reference"])
        if package:
            require(status == "supported_by_metadata" and package["toc_entry_ids"] == [candidates[0]["id"]],
                    "Prepared article disagrees with metadata match")
        references.append({
            **group, "occurrences": occurrences,
            "attribution": {"display_issues": labels, "all_labels_agree": explicit_issue,
                            "reference_month_is_inferred": True, "conflict": conflict},
            "native_context": native,
            "native_status": "resolved_hash" if native else "not_found",
            "relationship": {"status": status, "basis": rule if candidates else "no_title_match",
                             "toc_candidate_ids": [row["id"] for row in candidates],
                             "origin": "existing_package" if package else "coverage_audit",
                             "page_suffix_used_to_match": False},
            "preparation_status": "prepared" if package else "unprepared",
            "prepared_article": package,
        })
    # A repeated title/native target must not silently become a one-to-one match.
    counts = Counter(key for row in references if row["relationship"]["status"] == "supported_by_metadata"
                     for key in row["relationship"]["toc_candidate_ids"])
    for row in references:
        relation = row["relationship"]
        if any(counts[key] > 1 for key in relation["toc_candidate_ids"]):
            require(row["prepared_article"] is None, "Conflicting reference for prepared article")
            relation["status"] = "ambiguous"
            relation["basis"] = "multiple_cd_references_for_one_toc_entry"
    rows = []
    for entry in toc:
        related = [r for r in references if entry["id"] in r["relationship"]["toc_candidate_ids"]]
        matched = [r["reference"] for r in related if r["relationship"]["status"] == "supported_by_metadata"]
        rows.append({"entry": entry, "matched_references": matched,
                     "candidate_references": [r["reference"] for r in related if r["reference"] not in matched],
                     "relationship_status": "matched" if matched else "ambiguous" if related else "not_index_matched",
                     "preparation_status": "not_applicable_section" if entry["kind_candidate"] == "section" else
                     "prepared" if any(r["prepared_article"] for r in related) else "unprepared"})
    require(set(prepared) <= {r["reference"] for r in references}, "Prepared reference missing from issue coverage")
    return {"toc_entries": rows, "cd_references": references, "counts": {
        "toc_entries": len(rows), "toc_sections": sum(r["entry"]["kind_candidate"] == "section" for r in rows),
        "toc_relationships": dict(sorted(Counter(r["relationship_status"] for r in rows).items())),
        "toc_preparation": dict(sorted(Counter(r["preparation_status"] for r in rows).items())),
        "cd_references": len(references), "cd_index_occurrences": sum(len(r["occurrences"]) for r in references),
        "cd_relationships": dict(sorted(Counter(r["relationship"]["status"] for r in references).items())),
        "cd_preparation": dict(sorted(Counter(r["preparation_status"] for r in references).items())),
    }}


def build_report():
    historical = Snapshot(ROOT)
    index_dir = ROOT / "build/cd1-index"
    toc_manifest = historical.artifact("manifest.json")
    index_manifest = load(index_dir / "manifest.json")
    require(toc_manifest["source"]["sha256"] == TOC_SHA, "Audit requires the reviewed TOC import snapshot")
    raw = (ROOT / "TOC.md").read_bytes()
    snapshot = historical.read("TOC.md")
    require(hashlib.sha256(snapshot).hexdigest() == TOC_SHA, "Archived TOC snapshot changed")
    require(issue_text(snapshot) == issue_text(raw), "Live February TOC differs; review before auditing")
    toc = historical.artifact("toc-entries.jsonl")
    issues, reconstructed, errors = parse_toc(snapshot.decode("utf-8"), "toc-sha256-" + TOC_SHA)
    registry = json.loads(historical.read("data/identities/toc.json"))
    assign_identities(reconstructed, registry, {}, errors)
    finalize_entries(reconstructed)
    require(not errors and reconstructed == toc, "TOC import does not reproduce from its source and identities")
    require([r for r in issues if r["id"] == ISSUE] ==
            [r for r in historical.artifact("issues.json") if r["id"] == ISSUE],
            "Issue import does not reproduce")
    entries = checked_artifact(index_dir, "entries.jsonl")
    reconstructed = []
    for name in INDEX_NAMES:
        source = next(r for r in index_manifest["sources"] if r["name"] == name)
        source_raw = checked_file(ROOT / "private/cd1-probe/raw", {**source, "path": name})
        reconstructed.extend(parse_index(name, source_raw)[0])
    require(entries == reconstructed, "Index import does not reproduce")
    require(group_references(entries) == checked_artifact(index_dir, "references.jsonl"), "Reference population differs")
    mvb_path = "masocd-1/MASOCD.MVB"
    mvb = checked_file(ROOT, {"path": mvb_path, "sha256": SOURCES[mvb_path]})
    contexts = context_entries(mvb)
    summary_path = "data/catalog/second-article-checks/cd1-8802114.json"
    summary = load(ROOT / summary_path)
    package_records = [r for r in summary["outputs"] if r["path"].startswith(PACKAGE + "/")]
    require(len(package_records) == summary["combined_runtime_files"], "Incomplete prepared package evidence")
    for record in package_records:
        checked_file(ROOT, record)
    bundle, _, package_counts = load_package(ROOT / PACKAGE)
    prepared = {a["source"]["reference"]: {key: a[key] for key in
                ("id", "toc_entry_ids", "content_status", "extraction_status", "print_verification")}
                for a in bundle["articles"] if a["issue_id"] == ISSUE}
    inventory_path = "data/catalog/preservation/cd1-inventory.json"
    inventory = load(ROOT / inventory_path)
    checked_file(ROOT, inventory["output"])
    report = audit_issue(toc, entries, contexts, prepared)
    return {"schema_version": 1, "disc_id": "cd1", "issue_id": ISSUE, "scope": "metadata_only_coverage",
            "inputs": {
                "toc_snapshot": {**toc_manifest["source"], "git_blob": TOC_BLOB},
                "toc_import_manifest": file_record("build/toc/manifest.json", historical.read("build/toc/manifest.json")),
                "cd_index_import_manifest": file_record("build/cd1-index/manifest.json", (index_dir / "manifest.json").read_bytes()),
                "mvb": file_record(mvb_path, mvb),
                "native_context_count": len(contexts),
                "prepared_package_summary": file_record(summary_path, (ROOT / summary_path).read_bytes()),
                "prepared_package_counts": package_counts,
                "inventory_summary": file_record(inventory_path, (ROOT / inventory_path).read_bytes()),
            }, **report,
            "limits": {"printed_issue_completeness": "unverified", "unindexed_native_targets": "not_attributed",
                       "new_article_bodies_recovered": 0, "runtime_packages_modified": False,
                       "publication_decision": "not_made", "independent_backup_verified": False},
            "next_batch": {"references": ["8802030"], "checkpoint": "12b.1",
                           "prerequisite": "11b independent backup and restore evidence",
                           "remaining_unprepared_index_targets": ["8802180", "8802184"]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare with tracked report without writing")
    args = parser.parse_args()
    try:
        report = build_report()
        raw = json_bytes(report)
        if args.check:
            require(RECORD.read_bytes() == raw, "Coverage report differs; review before replacing")
        else:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_bytes(raw)
    except (OSError, ValueError, KeyError) as exc:
        print(f"CD1 coverage audit failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report["counts"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
