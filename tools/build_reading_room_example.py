"""Build the private v1 contract witness; asset packaging belongs to step 9."""

import argparse
import json
from pathlib import Path
import re
import sys

from jsonschema.exceptions import ValidationError

from maso_archive.reading_room import SCHEMA_PATH, catalog_for, project_section, validate_bundle
from tools import map_cd1_blocks as block_tools
from tools import verify_cd1_match as match_tools
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import ROOT, require
from tools.recover_cd1_text import json_bytes, topic_text
from tools.toc_snapshot import Snapshot, read_input

OUTPUT = ROOT / "build/reading-room-contract/8802065"
RECORD = ROOT / "data/catalog/reading-room-examples/cd1-8802065.json"
ARTICLE_ID = "cd1:article:8802065"


def media_id(name):
    return "cd1:media:" + name


def dimensions(resource):
    if "png_pixels" in resource:
        return {"width": resource["png_pixels"]["width"], "height": resource["png_pixels"]["height"], "unit": "px"}
    parsed = [re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)(px|mm|cm|in|pt)", resource["svg"][axis]) for axis in ("width", "height")]
    require(all(parsed) and parsed[0][2] == parsed[1][2], "Unsupported SVG dimensions")
    return {"width": float(parsed[0][1]), "height": float(parsed[1][1]), "unit": parsed[0][2]}


def build_example():
    inputs = {}

    def read(path, expected=None):
        path = ROOT / path
        raw = read_input(ROOT, path)
        require(expected is None or digest(raw) == expected, f"Changed input: {path.relative_to(ROOT)}")
        inputs[str(path.relative_to(ROOT))] = {"bytes": len(raw), "sha256": digest(raw)}
        return json.loads(raw)

    recovered = read(block_tools.SOURCE, block_tools.SOURCE_SHA256)
    block_record = read(block_tools.RECORD)
    block_map = read(block_tools.OUTPUT / "blocks.json", block_record["output"]["sha256"])
    block_tools.validate_map(recovered, block_map)
    image_record = read("data/catalog/image-maps/cd1-8802065.json")
    image_output = next(o for o in image_record["outputs"] if o["path"].endswith("images.json"))
    images = read(image_output["path"], image_output["sha256"])
    for source in images["sources"]:
        read(source["path"], source["sha256"])
    deferred = read("data/catalog/deferred-media/cd1-8802065.json")
    require(deferred["image_map"]["sha256"] == image_output["sha256"], "Stale deferred-media decisions")
    match = read("data/catalog/source-matches/cd1-8802065.json")
    match_tools.verify(match)
    for path in ("build/toc/manifest.json", "data/identities/toc.json"):
        read(path)
    snapshot = Snapshot(ROOT)
    toc_issues = snapshot.artifact("issues.json")
    toc_entries = snapshot.artifact("toc-entries.jsonl")
    for name in ("issues.json", "toc-entries.jsonl"):
        raw = snapshot.read("build/toc/" + name)
        inputs["build/toc/" + name] = {"bytes": len(raw), "sha256": digest(raw)}
    issue_source = next(i for i in toc_issues if i["id"] == match["issue_id"])
    selected_toc = [e for e in toc_entries if e["issue_id"] == issue_source["id"]]
    issue = {"schema_version": 1, "kind": "issue", "id": issue_source["id"],
             "year": issue_source["year"], "month": issue_source["month"], "label": issue_source["original_label"],
             "toc_status": "available", "cover_media_id": None,
             "toc": [{"id": e["id"], "parent_id": e["parent_id"], "kind": e["kind_candidate"],
                      "title": e["title_candidate"], "byline": e["byline_candidate"],
                      "pages": {"start": e["start_page_candidate"], "end": e["end_page_candidate"]},
                      "article_ids": [ARTICLE_ID] if e["id"] == match["toc_entry_id"] else [],
                      "link_status": "matched" if e["id"] == match["toc_entry_id"] else "unmatched"} for e in selected_toc]}
    resources = {r["resource"]: r for r in images["resources"]}
    deferred_by_name = {i["resource"]: i for i in deferred["issues"]}
    require(len(deferred_by_name) == len(deferred["issues"]), "Duplicate deferred resource")
    require(set(deferred_by_name) <= set(resources), "Unknown deferred resource")
    media, bindings = [], []
    for name, resource in resources.items():
        item = {"id": media_id(name), "source": {"disc_id": "cd1", "resource": name},
                "status": "available", "asset": None, "reason": None, "problem_ids": [], "rendering_notes": []}
        if name in deferred_by_name:
            decision = deferred_by_name[name]
            require(decision["status"] == "deferred" and not decision["resolved"], "Unexpected media disposition")
            require(decision["source"] == resource["source"], "Deferred resource source differs")
            require(decision["occurrences"] == [o for o in images["occurrences"] if o["resource"] == name], "Deferred occurrence evidence differs")
            item.update(status="deferred", reason="conversion_deferred", problem_ids=[decision["id"]])
        else:
            require(resource["status"] == "converted_pending_viewer", "Unreviewed media requires a disposition")
            derivative = next(d for d in resource["derivatives"] if d["role"] in ("converted_png", "converted_svg"))
            path = ROOT / "build/cd1-images/8802065" / derivative["path"]
            raw = path.read_bytes()
            require(digest(raw) == derivative["sha256"] and len(raw) == derivative["bytes"], "Changed media derivative")
            asset = {"path": "media/cd1/" + path.name, "mime_type": "image/png" if path.suffix == ".png" else "image/svg+xml",
                     "bytes": len(raw), "sha256": digest(raw), "dimensions": dimensions(resource)}
            item["asset"] = asset
            if "live_svg_text_depends_on_available_fonts" in resource["concerns"]:
                item["rendering_notes"] = ["font_substitution_possible"]
            bindings.append({"media_id": item["id"], "package_path": asset["path"],
                             "source_path": str(path.relative_to(ROOT)), "sha256": digest(raw), "bytes": len(raw)})
        media.append(item)
    sections = []
    paragraph_provenance = []
    occurrences = []
    for topic in recovered["topics"]:
        section = {"id": f"cd1:topic:{topic['ordinal']}",
                   "role": {"linked_introduction": "introduction", "reference_target_body": "body"}[topic["role"]], "blocks": []}
        for source_block in block_map["blocks"]:
            if source_block["topic_ordinal"] != topic["ordinal"]:
                continue
            paragraphs = []
            for member in source_block["members"]:
                source = topic["paragraphs"][member["paragraph_ordinal"] - 1]
                identifier = f"cd1-8802065:T{topic['ordinal']}:P{source['ordinal']:03d}"
                paragraph = {"id": identifier, "runs": []}
                require(source["text"] == "".join(r["text"] for r in source["runs"]), "Inconsistent source runs")
                for n, run in enumerate(source["runs"], 1):
                    marks = [label for key, label in (("b", "bold"), ("ul", "underline")) if run["format"][key]]
                    if run["kind"] == "text":
                        paragraph["runs"].append({"type": "text", "text": run["text"], "marks": marks})
                    else:
                        require(run["kind"] == "object", "Unsupported source run")
                        occurrence_id = identifier + f":R{n}"
                        paragraph["runs"].append({"type": "media", "media_id": media_id(run["object"]["resource"]),
                                                  "occurrence_id": occurrence_id, "marks": marks})
                        occurrences.append(occurrence_id)
                paragraphs.append(paragraph)
                paragraph_provenance.append({"paragraph_id": identifier, "topic_ordinal": topic["ordinal"],
                                             "paragraph_ordinal": source["ordinal"], "source_span": source["source_span"],
                                             "run_ordinals": member["run_ordinals"]})
            kind = source_block["kind"]
            section["blocks"].append({"id": source_block["id"], "type": kind,
                                      "layout": "preformatted" if kind == "code" else "spacing" if kind == "spacing" else "flow",
                                      "heading_level": source_block.get("heading_level"),
                                      "parent_heading_id": source_block["parent_heading_id"],
                                      "interpretation": "unresolved" if kind == "unresolved" else "source_supported",
                                      "paragraphs": paragraphs})
        sections.append(section)
    require(occurrences == [o["id"] for o in images["occurrences"]], "Object order differs from image map")
    matched_toc = next(e for e in selected_toc if e["id"] == match["toc_entry_id"])
    article = {"schema_version": 1, "kind": "article", "id": ARTICLE_ID, "issue_id": issue["id"],
               "title": recovered["topics"][0]["paragraphs"][1]["text"],
               "byline": recovered["topics"][1]["paragraphs"][3]["text"],
               "pages": {"start": matched_toc["start_page_candidate"], "end": None},
               "source": {"disc_id": "cd1", "reference": "8802065"}, "toc_entry_ids": [matched_toc["id"]],
               "content_status": "available", "extraction_status": "checked",
               "print_verification": {"status": "pending", "report_id": None, "pages_compared": []},
               "sections": sections, "relationships": [{"type": "caption_for", "from_block": r["from_block"], "to_block": r["to_block"]}
                                                        for r in block_map["relationships"]]}
    bundle = {"schema_version": 1, "kind": "contract_example", "catalog": catalog_for([issue], [article]),
              "issues": [issue], "articles": [article], "media": {"schema_version": 1, "kind": "media_index", "items": media}}
    counts = validate_bundle(bundle)
    for section, topic in zip(sections, recovered["topics"]):
        require(project_section(section, {m["id"]: m for m in media}) == topic_text(topic), "Contract projection changed source text/spacing")
    for source_block, target_block in zip(block_map["blocks"], [b for s in sections for b in s["blocks"]]):
        require(source_block["id"] == target_block["id"], "Block order changed")
        require(digest(project_section({"blocks": [target_block]}, {m["id"]: m for m in media}).encode()) == source_block["content_sha256"],
                "Block content hash differs")
    provenance = {"schema_version": 1, "article_id": ARTICLE_ID, "inputs": inputs,
                  "schema_sha256": digest(SCHEMA_PATH.read_bytes()), "counts": counts,
                  "metadata_evidence": {"title": {"topic": 148, "paragraph": 2}, "byline": {"topic": 149, "paragraph": 4},
                                        "start_page": {"toc_entry_id": matched_toc["id"]}, "issue": issue_source["source"]},
                  "paragraphs": paragraph_provenance, "block_map_path": str((block_tools.OUTPUT / "blocks.json").relative_to(ROOT)),
                  "asset_bindings": bindings, "validation": {"schema_and_relationships": True, "exact_source_projection": True,
                  "assets_copied": False, "physical_magazine_compared": False}}
    files = {"pilot.example.json": json_bytes(bundle), "provenance.json": json_bytes(provenance)}
    summary = {"schema_version": 1, "article_id": ARTICLE_ID, "schema": {"path": str(SCHEMA_PATH.relative_to(ROOT)), "sha256": digest(SCHEMA_PATH.read_bytes())},
               "counts": counts, "available_media": len(bindings), "deferred_media": len(deferred_by_name),
               "caption_relationships": len(article["relationships"]), "validation": provenance["validation"],
               "outputs": [{"path": str((OUTPUT / name).relative_to(ROOT)), "bytes": len(raw), "sha256": digest(raw)} for name, raw in files.items()]}
    return summary, files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    try:
        record, files = build_example()
        if args.write_record:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_bytes(json_bytes(record))
        else:
            require(json.loads(RECORD.read_bytes()) == record, "Contract example differs from reviewed summary")
        OUTPUT.mkdir(parents=True, exist_ok=True)
        for name, raw in files.items():
            temporary = OUTPUT / (name + ".tmp")
            temporary.write_bytes(raw)
            temporary.replace(OUTPUT / name)
        print(f"Validated v1 contract example: {record['counts']}; assets are not packaged yet.")
    except (OSError, ValueError, KeyError, StopIteration, ValidationError) as error:
        print(f"Contract example failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
