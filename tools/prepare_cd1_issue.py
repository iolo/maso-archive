"""Step 12c: reconcile February coverage and relocate five prepared articles.

Reads existing metadata/packages; never recovers topics or converts images.
"""

import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

from jsonschema.exceptions import ValidationError

from maso_archive.reading_room import SCHEMA_PATH
from maso_archive.reading_room_package import checked_file, file_record, load_package
from maso_archive.toc import assign_identities, finalize_entries, parse_toc
from tools import audit_cd1_issue as audit
from tools.build_reading_room_package import write_package
from tools.map_cd1_topic import ROOT, context_hash, require
from tools.recover_cd1_text import json_bytes
from tools.toc_snapshot import Snapshot
from tools.verify_cd1_match import checked_artifact

ISSUE = audit.ISSUE
OUTPUT = ROOT / "build/cd1-issues/1988-02"
RECORD = ROOT / "data/catalog/issue-packages/cd1-1988-02.json"
COVERAGE = ROOT / "data/catalog/issue-coverage/cd1-1988-02-prepared.json"
PREVIOUS = ROOT / "build/cd1-articles/8802180/combined/content"
PREPARATIONS = [
    ("8802065", "data/catalog/reading-room-packages/cd1-8802065.json", "build/reading-room-packages/cd1-8802065"),
    ("8802114", "data/catalog/second-article-checks/cd1-8802114.json", "build/cd1-second-article/8802114"),
    *[(ref, f"data/catalog/article-preparations/cd1-{ref}.json", f"build/cd1-articles/{ref}")
      for ref in ("8802030", "8802184", "8802180")],
]


def compare_toc(historical, current):
    """Allow the expanded document's source ID, but no unnoticed issue drift."""
    old = [e for e in historical if e["issue_id"] == ISSUE]
    new = [e for e in current if e["issue_id"] == ISSUE]
    require([e["id"] for e in old] == [e["id"] for e in new], "February TOC identities/order changed")
    changes = []
    for before, after in zip(old, new):
        a, b = deepcopy(before), deepcopy(after)
        source_a, source_b = a["source"].pop("id"), b["source"].pop("id")
        require(a == b, f"February TOC metadata changed: {before['id']}")
        if source_a != source_b:
            changes.append({"toc_entry_id": before["id"], "field": "source.id", "before": source_a, "after": source_b})
    return changes


def check_reviews(bundle, deferred, text_reviews):
    """Every deferred runtime ID needs an unresolved record; text reviews need a paragraph."""
    problems = {p["id"]: p for record in deferred for p in record["issues"]}
    require(len(problems) == sum(len(r["issues"]) for r in deferred), "Duplicate deferred issue ID")
    referenced = set()
    for media in bundle["media"]["items"]:
        if media["status"] != "deferred":
            continue
        require(media["asset"] is None, "Deferred asset unexpectedly available")
        for key in media["problem_ids"]:
            require(key in problems, "Deferred media lacks a review record")
            problem = problems[key]
            require(problem["resource"] == media["source"]["resource"] and
                    problem["status"] == "deferred" and not problem["resolved"], "Deferred media disposition changed")
            referenced.add(key)
    require(referenced == set(problems), "Unreferenced deferred review record")
    require(len(text_reviews) == 1 and text_reviews[0]["id"] == "cd1-8802180-text-001",
            "Pending text review record missing or duplicated")
    paragraphs = {p["id"]: p for a in bundle["articles"] for s in a["sections"] for b in s["blocks"] for p in b["paragraphs"]}
    for review in text_reviews:
        identifier = f"cd1-8802180:T{review['topic_ordinal']}:P{review['paragraph_ordinal']:03d}"
        require(identifier in paragraphs and not review["corrected"] and
                review["status"] == "pending_physical_comparison" and not review["alternative_decoding"]["applied"],
                "Text review target/status changed")
        text = "".join(r["text"] for r in paragraphs[identifier]["runs"] if r["type"] == "text")
        character = chr(int(review["decoded_codepoint"][2:], 16))
        require(text.count(character) == review["occurrences"] and
                character.encode("cp949").hex() == review["encoded_pair_hex"], "Reviewed source string changed")


def build_handoff():
    inputs = {}

    def read(path, expected=None):
        path = Path(path)
        relative = path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()
        raw = checked_file(ROOT, {**(expected or {}), "path": relative})
        inputs[relative] = file_record(relative, raw)
        return raw

    historical = json.loads(read(audit.RECORD))
    require(historical == audit.build_report(), "Historical coverage no longer reproduces")
    snapshot = Snapshot(ROOT)
    old_toc = snapshot.artifact("toc-entries.jsonl")
    manifest = json.loads(read("build/toc/manifest.json"))
    current_raw = read("TOC.md", manifest["source"])
    registry_raw = read("data/identities/toc.json", {"sha256": manifest["identities_sha256"]})
    current = checked_artifact(ROOT / "build/toc", "toc-entries.jsonl")
    current_issues = checked_artifact(ROOT / "build/toc", "issues.json")
    for name in ("toc-entries.jsonl", "issues.json"):
        read("build/toc/" + name, manifest["outputs"][name])
    issues, reconstructed, errors = parse_toc(current_raw.decode(), "toc-sha256-" + manifest["source"]["sha256"])
    assign_identities(reconstructed, json.loads(registry_raw), {}, errors)
    finalize_entries(reconstructed)
    require(not errors and reconstructed == current and
            [i for i in issues if i["id"] == ISSUE] == [i for i in current_issues if i["id"] == ISSUE],
            "Current February TOC import does not reproduce")
    require(audit.issue_text(current_raw) == audit.issue_text(snapshot.read("TOC.md")), "February TOC source changed")
    differences = compare_toc(old_toc, current)
    summaries, evidence, singles = {}, {}, {}
    for reference, record_path, base in PREPARATIONS:
        summary = json.loads(read(record_path))
        require(summary["article_id"] == "cd1:article:" + reference, "Preparation identity changed")
        content = base + ("/content" if reference == "8802065" else "/single/content")
        records = [{**r, "path": content + "/" + r["path"]} for r in summary["outputs"]] if reference == "8802065" else summary["outputs"]
        selected = {r["path"][len(content) + 1:]: read(r["path"], r) for r in records if r["path"].startswith(content + "/")}
        bundle, _, counts = load_package(ROOT / content)
        expected_count = summary["counts"]["files"] if reference == "8802065" else summary["single_runtime_files"]
        require(len(selected) == counts["files"] == expected_count and len(bundle["articles"]) == 1,
                "Incomplete standalone preparation")
        provenance = summary["provenance"] if reference == "8802065" else next(r for r in records if r["path"] == base + "/provenance.json")
        evidence[reference] = json.loads(read(provenance["path"], provenance))
        summaries[reference], singles[reference] = summary, (bundle, selected)
    previous_prefix = PREVIOUS.relative_to(ROOT).as_posix() + "/"
    runtime = {r["path"][len(previous_prefix):]: read(r["path"], r) for r in summaries["8802180"]["outputs"]
               if r["path"].startswith(previous_prefix)}
    bundle, _, counts = load_package(PREVIOUS)
    require(len(runtime) == counts["files"] == summaries["8802180"]["combined_runtime_files"], "Incomplete combined preparation")
    require({a["source"]["reference"] for a in bundle["articles"]} == set(summaries), "Prepared reference population changed")
    for reference, (single, files) in singles.items():
        for path, raw in files.items():
            if path.startswith(("articles/", "previews/", "media/")):
                require(runtime.get(path) == raw, f"Prepared content changed: {path}")
        media_by_id = {m["id"]: m for m in bundle["media"]["items"]}
        require(all(media_by_id.get(m["id"]) == m for m in single["media"]["items"]), "Prepared media metadata changed")
    # This match was ambiguous in 12a; require the subsequent native/body evidence.
    match = summaries["8802180"]["title_comparison"]
    require(match == evidence["8802180"]["title_comparison"] and match["decision"] == "matched" and
            match["toc_title"] == match["native_and_body_title"] == audit.TITLE_COMPARISONS["8802180"][0] and
            match["index_title"] == audit.TITLE_COMPARISONS["8802180"][1], "Graphics title evidence changed")
    comparisons = dict(audit.TITLE_COMPARISONS)
    comparisons["8802180"] = (*comparisons["8802180"][:2], "reviewed_native_body_title_and_page_agreement")
    prepared = {a["source"]["reference"]: {k: a[k] for k in
                ("id", "toc_entry_ids", "content_status", "extraction_status", "print_verification")} for a in bundle["articles"]}
    contexts = {context_hash(r["reference"]): r["native_context"] for r in historical["cd_references"]}
    entries = checked_artifact(ROOT / "build/cd1-index", "entries.jsonl")
    read("build/cd1-index/manifest.json")
    coverage = audit.audit_issue(current, entries, contexts, prepared, comparisons)
    require(coverage["counts"]["cd_preparation"] == {"prepared": 5} and coverage["counts"]["toc_preparation"] ==
            {"not_applicable_section": 4, "prepared": 5, "unprepared": 30}, "Unexpected February coverage population")
    require(len(bundle["issues"]) == 1 and bundle["issues"][0]["id"] == ISSUE, "Unexpected issue package")
    issue = bundle["issues"][0]
    imported_issue = next(i for i in current_issues if i["id"] == ISSUE)
    require((issue["year"], issue["month"], issue["label"]) ==
            (imported_issue["year"], imported_issue["month"], imported_issue["original_label"]), "Issue heading metadata changed")
    require(len(issue["toc"]) == len(coverage["toc_entries"]), "Runtime TOC population changed")
    for row, runtime_entry in zip(coverage["toc_entries"], issue["toc"]):
        entry = row["entry"]
        expected = {"id": entry["id"], "parent_id": entry["parent_id"], "kind": entry["kind_candidate"],
                    "title": entry["title_candidate"], "byline": entry["byline_candidate"],
                    "pages": {"start": entry["start_page_candidate"], "end": entry["end_page_candidate"]},
                    "article_ids": [prepared[r]["id"] for r in row["matched_references"]],
                    "link_status": "matched" if row["matched_references"] else "unmatched"}
        require(runtime_entry == expected, "Current TOC and runtime metadata disagree")
        row["content_availability"] = "not_applicable_section" if entry["kind_candidate"] == "section" else (
            "prepared" if row["matched_references"] else "not_prepared_no_index_match")
    deferred = [json.loads(read(f"data/catalog/deferred-media/cd1-{reference}.json")) for reference in ("8802065", "8802180")]
    for record in deferred:
        for problem in record["issues"]:
            read(problem["source"]["path"], problem["source"])
    text_reviews = summaries["8802180"]["text_reviews"]
    require(text_reviews == evidence["8802180"]["text_reviews"], "Text review evidence changed")
    check_reviews(bundle, deferred, text_reviews)
    require(all(a["print_verification"]["status"] == "pending" and a["pages"]["end"] is None for a in bundle["articles"]),
            "Print review status needs explicit reconciliation")
    schema = file_record(SCHEMA_PATH.relative_to(ROOT).as_posix(), read(SCHEMA_PATH))
    coverage = {"schema_version": 1, "disc_id": "cd1", "issue_id": ISSUE, "checkpoint": "12c",
                "scope": "prepared_indexed_articles_and_complete_TOC_accounting",
                "historical_audit": inputs[audit.RECORD.relative_to(ROOT).as_posix()],
                "metadata_comparison": {"historical_source": historical["inputs"]["toc_snapshot"],
                                        "current_source": inputs["TOC.md"], "entry_differences": differences,
                                        "runtime_metadata_changes": [], "issue_text_identical": True},
                **coverage, "review_records": {"deferred_media": deferred, "text_reviews": text_reviews},
                "limits": {"printed_issue_completeness": "unverified", "unindexed_native_targets": "not_attributed",
                           "cover": "unavailable", "new_topics_recovered": 0, "new_media_conversions": 0,
                           "publication_decision": "not_made", "independent_backup_verified": False},
                "runtime_counts": counts, "catalog_search_fields": bundle["catalog"]["search_fields"]}
    outputs = [file_record(p, raw) for p, raw in sorted(runtime.items())]
    provenance = {"schema_version": 1, "issue_id": ISSUE, "schema": schema, "inputs": inputs,
                  "coverage": coverage, "article_evidence": evidence, "runtime_root": "content", "outputs": outputs,
                  "handoff": {"base_url": "deployment_supplied_directory_URL_ending_in_slash",
                              "entrypoint": "manifest.json", "path_resolution": "all_paths_relative_to_package_base",
                              "search": "metadata_only; title/byline/issue_id; no_full_text_index"},
                  "validation": {"runtime_bytes_identical_to_predecessor": True, "all_five_standalones_checked": True,
                                 "current_and_historical_TOC_reconciled": True, "schema_changed": False}}
    files = {**{"content/" + p: raw for p, raw in runtime.items()}, "provenance.json": json_bytes(provenance)}
    record = {"schema_version": 1, "issue_id": ISSUE, "package_root": (OUTPUT / "content").relative_to(ROOT).as_posix(),
              "schema": schema, "coverage": file_record(COVERAGE.relative_to(ROOT).as_posix(), json_bytes(coverage)),
              "counts": counts, "coverage_counts": coverage["counts"], "deferred_media": 4, "text_reviews": len(text_reviews),
              "predecessor": PREVIOUS.relative_to(ROOT).as_posix(), "outputs": outputs,
              "provenance": file_record((OUTPUT / "provenance.json").relative_to(ROOT).as_posix(), files["provenance.json"]),
              "validation": provenance["validation"]}
    return record, coverage, files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    try:
        record, coverage, files = build_handoff()
        if not args.write_record:
            require(record == json.loads(RECORD.read_bytes()), "Issue handoff differs from reviewed record")
            require(coverage == json.loads(COVERAGE.read_bytes()), "Prepared coverage differs from reviewed record")
        write_package(OUTPUT, files)
        if args.write_record:
            for path, value in ((RECORD, record), (COVERAGE, coverage)):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(json_bytes(value))
        print(f"February issue handoff prepared: {record['counts']}; coverage={coverage['counts']}")
    except (OSError, ValueError, KeyError, StopIteration, ValidationError) as exc:
        print(f"Issue handoff failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
