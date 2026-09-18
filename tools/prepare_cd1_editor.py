"""Bounded CD1 step 12b.2: preserve and package the Turbo C editor article."""

import argparse
from collections import Counter
from copy import deepcopy
import json
import re
import struct
import sys
import tempfile
from pathlib import Path

from jsonschema.exceptions import ValidationError

from maso_archive.reading_room import SCHEMA_PATH, catalog_for, project_section, validate_bundle
from maso_archive.reading_room_package import checked_file, file_record, load_package
from tools import check_cd1_second_article as second
from tools import prepare_cd1_interview as interview
from tools import inventory_cd1_rtf as inventory
from tools import map_cd1_blocks as blocks
from tools import map_cd1_images as images
from tools import map_cd1_topic as native
from tools import recover_cd1_text as recovery
from tools import render_cd1_markdown as markdown
from tools import build_reading_room_package as package
from tools.decode_cd1_paragraph import digest
from tools.toc_snapshot import Snapshot, read_input
from tools.verify_cd1_match import checked_artifact

ROOT = native.ROOT
REFERENCE = "8802184"
ARTICLE_ID = "cd1:article:" + REFERENCE
TOC_ID = "maso-1988-02-toc-0027"
OUTPUT = ROOT / "build/cd1-articles/8802184"
RECORD = ROOT / "data/catalog/article-preparations/cd1-8802184.json"
PREVIOUS = interview.OUTPUT / "combined/content"
FONT_CODECS = {4: "cp949", 5: "cp949", 15: "ascii"}
LISTING = (24, 1144)
SUBHEADINGS = [1147, 1153, 1158, 1167, 1173, 1177, 1180, 1183, 1189, 1192]
CAPTIONS = [(22, 24), (1150, 1151), (1170, 1171), (1186, 1187)]
RESOURCES = ["bm39.bmp", "bm40.bmp", "p8021851.dib", "82185_2.dib", "82186_3.dib"]
require = native.require


def block_id(topic, start, end=None):
    return f"cd1-{REFERENCE}:T{topic}:P{start:03d}-{end if end is not None else start:03d}"


def map_editor(article):
    """Classify reviewed source spans; keep code characters and all blank lines."""
    require([t["ordinal"] for t in article["topics"]] == [160, 161], "Unexpected editor topics")
    body = article["topics"][1]["paragraphs"]
    start, end = LISTING
    require(body[start - 1]["text"] == " #include <stdio.h>" and body[end - 1]["text"] == "}",
            "Listing boundaries changed")
    require(not body[start - 2]["text"] and not body[end]["text"], "Listing separator changed")
    require(all(r["kind"] == "text" and r["format"]["font_id"] == 15 and r["format"]["fs"] == 20
                for p in body[start - 1:end] for r in p["runs"]), "Listing font changed")
    require(sum(p["text"].count("\t") for p in body[start - 1:end]) == 30, "Listing tab count changed")
    require([p["ordinal"] for p in body if any(r["format"]["font_id"] == 15 for r in p["runs"])] ==
            [p["ordinal"] for p in body[start - 1:end] if p["runs"]], "Code font outside reviewed listing")
    require(body[1161]["text"] == "char far *vram = 0xB8000000;" and
            body[1162]["text"] == "*(varm) = 'A';", "Short code example changed")
    require(not body[1160]["text"] and not body[1163]["text"], "Short example separator changed")
    result = {"schema_version": 1, "cd_reference": REFERENCE, "blocks": [], "relationships": [],
              "verification": {"semantic_structure_verified": False}}
    for topic in article["topics"]:
        ordinal, paragraphs = topic["ordinal"], topic["paragraphs"]
        declarations = {2: (2, "title", "source_title")}
        if ordinal == 161:
            declarations.update({1: (1, "issue_label", "explicit_issue_page_label_with_object"),
                                 4: (4, "byline", "explicit_author_byline"),
                                 start: (end, "code", "listing_caption_Fixedsys_runs_and_C_boundaries"),
                                 1162: (1163, "code", "isolated_C_example_between_explanatory_paragraphs")})
            for n in [9, 1146, 1195, 1199] + SUBHEADINGS:
                declarations[n] = (n, "heading", "bold_indented_source_heading")
            for number, n in enumerate(SUBHEADINGS, 1):
                require(body[n - 1]["text"].startswith(f"{number}."), "Subheading numbering changed")
            for number, (caption, target) in enumerate(CAPTIONS):
                prefix = "<리스트 1> " if number == 0 else f"<그림 {number}> "
                require(body[caption - 1]["text"].startswith(prefix), "Caption changed")
                declarations[caption] = (caption, "caption", "numbered_source_caption")
                if number:
                    require(len(body[target - 1]["runs"]) == 1 and
                            body[target - 1]["runs"][0]["kind"] == "object", "Figure attachment changed")
                    declarations[target] = (target, "figure", "single_bitmap_after_numbered_caption")
        index, parents = 1, {}
        while index <= len(paragraphs):
            p = paragraphs[index - 1]
            stop, kind, basis = declarations.get(index, (index, "paragraph" if p["text"].strip() else "spacing", "source_paragraph"))
            level = None
            if kind == "heading":
                level = 2 if index in SUBHEADINGS else 1
                size = 24 if index in (9, 1146, 1195) else 20
                require(p["format"].get("li") == 215 and p["runs"] and
                        all(r["format"]["b"] and r["format"]["fs"] == size for r in p["runs"]),
                        "Heading evidence changed")
                parents = {k: v for k, v in parents.items() if k < level}
            members = paragraphs[index - 1:stop]
            block = {"id": block_id(ordinal, index, stop), "topic_ordinal": ordinal, "kind": kind,
                     "parent_heading_id": parents[max(parents)] if parents else None,
                     "decision": {"basis": basis, "review_concerns":
                                  ["unnumbered_closing_heading_level_inferred"] if ordinal == 161 and index == 1199 else []},
                     "members": [{"paragraph_ordinal": p["ordinal"], "run_ordinals": list(range(1, len(p["runs"]) + 1)),
                                  "source_span": p["source_span"]} for p in members],
                     "source_span": {"byte_offset": members[0]["source_span"]["byte_offset"],
                                     "end_exclusive": members[-1]["source_span"]["end_exclusive"]},
                     "content_sha256": digest(recovery.topic_text({"paragraphs": members}).encode()),
                     "object_refs": [{"paragraph_ordinal": p["ordinal"], "run_ordinal": n,
                                      "resource": r["object"]["resource"], "rtf_byte_offset": r["object"]["byte_offset"]}
                                     for p in members for n, r in enumerate(p["runs"], 1) if r["kind"] == "object"]}
            if level is not None:
                block["heading_level"] = level
                parents[level] = block["id"]
            result["blocks"].append(block)
            index = stop + 1
    by_start = {b["members"][0]["paragraph_ordinal"]: b["id"] for b in result["blocks"] if b["topic_ordinal"] == 161}
    result["relationships"] = [{"kind": "caption_for", "from_block": by_start[c], "to_block": by_start[t]} for c, t in CAPTIONS]
    blocks.validate_map(article, result)
    return result


def recover_editor(mvb, rtf):
    topics = native.native_topics(mvb, 164)
    contexts = native.context_entries(mvb)
    require(contexts[native.context_hash(REFERENCE)]["topic_offset"] == topics[160]["topic_offset"], "Native target changed")
    pages = list(re.finditer(rb"(?<!\\)\\page\n", rtf))
    require(len(pages) == 3098, "RTF topic population changed")
    boundaries = []
    for ordinal in (159, 162):
        start, end = pages[ordinal - 2].end(), pages[ordinal - 1].start()
        require(rtf[start:end] == b"\\pard \\b ", "Neighbor separator changed")
        boundaries.append({"native": topics[ordinal - 1], "rtf": {"byte_offset": start, "byte_length": end - start,
                           "sha256": digest(rtf[start:end])}})
    mapping, reports, recovered, state = [], [], [], None
    for ordinal, alias, role in ((160, "3M4LOC", "linked_introduction"), (161, "1KN6LK", "reference_target_body")):
        start, end = pages[ordinal - 2].end(), pages[ordinal - 1].start()
        raw = rtf[start:end]
        require([m[1].decode() for m in native.CONTEXT_FOOTNOTE.finditer(raw)] == [alias], "RTF alias changed")
        context = contexts[native.context_hash(alias)]
        require(context["topic_offset"] == topics[ordinal - 1]["topic_offset"], "RTF/native mapping differs")
        links = re.findall(rb"\{\\v ([^}]+)\}", raw)
        require(links == ([] if ordinal == 160 else [b"3M4LOC"]), "Unaccounted linked topic")
        report = inventory.inspect_topic(raw, start, None if state is None else state["character"]["font_id"])
        require(not report["issues"], "Unsupported RTF construct needs review")
        report.update(ordinal=ordinal, role=role)
        topic = recovery.recover_topic(rtf, report, state, FONT_CODECS)
        require(not topic["issues"] and all(p["terminated_by_par"] for p in topic["paragraphs"]), "Incomplete editor decoding")
        state = topic["final_state"]
        mapping.append({"role": role, "alias": alias, "native": topics[ordinal - 1], "context": context,
                        "rtf": {"byte_offset": start, "byte_length": end - start, "end_exclusive": end, "sha256": digest(raw)}})
        reports.append(report)
        recovered.append(topic)
    require(native.context_hash(REFERENCE) == native.context_hash("1KN6LK"), "Reference/alias mismatch")
    require(topics[159]["next_topic_pos"] == topics[160]["topic_pos"] and
            topics[160]["next_topic_pos"] == topics[161]["topic_pos"] and
            topics[160]["browse_back_topic_offset"] == topics[157]["topic_offset"] and
            topics[160]["browse_forward_topic_offset"] == topics[163]["topic_offset"], "Article boundary chain changed")
    position = topics[160]["topic_pos"]
    size, length, _, _, data_length, kind = struct.unpack("<5iB", native.topic_read(mvb, position, 21))
    require(kind == 2 and length <= size - data_length, "Unsupported native title")
    title = native.topic_read(mvb, position, size)[data_length:data_length + length].split(b"\0")[0].decode("cp949")
    require(title == recovered[0]["paragraphs"][1]["text"] == "터보 C로 작성한 에디터", "Native/introductory title differs")
    require([len(t["paragraphs"]) for t in recovered] == [4, 1202], "Paragraph population changed")
    require(re.search(rb"\{\\f15\\froman Fixedsys;\}", rtf[:rtf.index(b"\n{\\colortbl")]) is not None,
            "Font 15 definition changed")
    require(sum(len(r["controls"].get("tab", [])) for r in reports) == 30, "Source tab count changed")
    return {"schema_version": 1, "cd_reference": REFERENCE, "topics": recovered}, reports, mapping, boundaries


def build_article():
    inputs = {}
    def read(path, expected=None):
        path = ROOT / path
        raw = read_input(ROOT, path)
        require(expected is None or digest(raw) == expected, f"Changed source: {path.relative_to(ROOT)}")
        inputs[str(path.relative_to(ROOT))] = file_record(str(path.relative_to(ROOT)), raw)
        return raw

    mvb, rtf = [read(p, sha) for p, sha in native.SOURCES.items()]
    article, reports, topic_map, boundaries = recover_editor(mvb, rtf)
    mapping = map_editor(article)
    toc_entries = Snapshot(ROOT).artifact("toc-entries.jsonl")
    toc = next(e for e in toc_entries if e["id"] == TOC_ID)
    cd_entries = checked_artifact(ROOT / "build/cd1-index", "entries.jsonl")
    for path in ("TOC.md", "data/identities/toc.json", "build/toc/manifest.json", "build/toc/toc-entries.jsonl",
                 "build/cd1-index/manifest.json", "build/cd1-index/entries.jsonl", SCHEMA_PATH):
        read(path)
    title = article["topics"][0]["paragraphs"][1]["text"]
    require(toc["title_candidate"] == title and toc["start_page_candidate"] == 184, "TOC match changed")
    require([e["id"] for e in toc_entries if e["issue_id"] == "maso-1988-02" and
             e["title_candidate"] == title] == [TOC_ID], "Ambiguous editor TOC match")
    occurrences = [e for e in cd_entries if e["reference"] == REFERENCE]
    require(len(occurrences) == 2 and all(e["title"] == title and e["display_issue"] == "1988-02" for e in occurrences), "CD label mismatch")
    for e in occurrences:
        source = e["source"]
        raw = read("private/cd1-probe/raw/" + source["name"], source["sha256"])
        require(raw[source["byte_offset"]:source["byte_offset"] + source["byte_length"]].rstrip(b"\r\n").decode("cp949") == e["raw_line"], "CD occurrence changed")
    body = article["topics"][1]["paragraphs"]
    require(body[0]["text"] == "[object:bm39.bmp] 88.2.  184p" and body[3]["text"] == "글/ 우원식", "Opening metadata changed")
    objects = [r["object"]["resource"] for t in article["topics"] for p in t["paragraphs"] for r in p["runs"] if r["kind"] == "object"]
    require(objects == RESOURCES, "Unexpected editor media")
    manifest = json.loads(read(images.MANIFEST))
    media, assets, conversions = [], {}, []
    version = images.command(["convert", "-version"])["stdout"].splitlines()[0]
    for resource in RESOURCES:
        bitmap = images.checked_source(resource, manifest)
        read(images.RAW / resource, digest(bitmap))
        with tempfile.TemporaryDirectory() as temporary:
            stage = Path(temporary)
            (stage / "assets").mkdir()
            conversion = images.convert_resource(resource, bitmap, stage)
            require(conversion["status"] == "converted_pending_viewer" and conversion["pixel_equivalent"],
                    "Bitmap needs explicit disposition")
            png = (stage / ("assets/" + resource + ".png")).read_bytes()
            for command in conversion["commands"]:
                command["argv"] = [a.replace(temporary, "<conversion-stage>") for a in command["argv"]]
        conversion["tool_version"] = version
        conversions.append(conversion)
        path = "media/cd1/" + resource + ".png"
        assets[path] = png
        media.append({"id": "cd1:media:" + resource, "source": {"disc_id": "cd1", "resource": resource},
                      "status": "available", "reason": None, "problem_ids": [], "rendering_notes": [],
                      "asset": {**file_record(path, png), "mime_type": "image/png",
                                "dimensions": {"width": conversion["png_pixels"]["width"],
                                               "height": conversion["png_pixels"]["height"], "unit": "px"}}})
    runtime = {"schema_version": 1, "kind": "article", "id": ARTICLE_ID, "issue_id": "maso-1988-02",
               "title": title, "byline": body[3]["text"], "pages": {"start": 184, "end": None},
               "source": {"disc_id": "cd1", "reference": REFERENCE}, "toc_entry_ids": [TOC_ID],
               "content_status": "available", "extraction_status": "checked",
               "print_verification": {"status": "pending", "report_id": None, "pages_compared": []},
               "sections": second.reading_sections(article, mapping, REFERENCE, 160), "relationships": [{"type": "caption_for", "from_block": r["from_block"], "to_block": r["to_block"]}
                                 for r in mapping["relationships"]]}
    previous_record = json.loads(read(interview.RECORD))
    previous_files = {}
    for record in previous_record["outputs"]:
        path = Path(record["path"])
        if path.is_relative_to(PREVIOUS.relative_to(ROOT)):
            raw = checked_file(ROOT, record)
            previous_files[path.relative_to(PREVIOUS.relative_to(ROOT)).as_posix()] = raw
    require(len(previous_files) == previous_record["combined_runtime_files"], "Incomplete predecessor package")
    previous, previous_manifest, _ = load_package(PREVIOUS)
    issue = deepcopy(previous["issues"][0])
    for entry in issue["toc"]:
        entry.update(article_ids=[ARTICLE_ID] if entry["id"] == TOC_ID else [],
                     link_status="matched" if entry["id"] == TOC_ID else "unmatched")
    bundle = {"schema_version": 1, "kind": "contract_example", "issues": [issue], "articles": [runtime],
              "catalog": catalog_for([issue], [runtime]), "media": {"schema_version": 1, "kind": "media_index", "items": media}}
    counts = validate_bundle(bundle)
    for section, topic in zip(runtime["sections"], article["topics"]):
        require(project_section(section, {m["id"]: m for m in media}) == recovery.topic_text(topic), "Editor projection changed")
    rendered, locations = markdown.render(article, mapping)
    previews, ranges = [], []
    for section in runtime["sections"]:
        name = section["role"] + ".md"
        raw, selected = package.package_preview(rendered[name], [r for r in locations if r["path"] == name])
        path = f"previews/cd1/{REFERENCE}/{name}"
        previews.append((ARTICLE_ID, section["id"], path, raw))
        ranges.extend({"path": path, **r} for r in selected)
    single_files = second.assemble(bundle, assets, previews)
    # Validate a relocated standalone package before composing the next package.
    with tempfile.TemporaryDirectory() as temporary:
        stage = Path(temporary)
        for path, raw in single_files.items():
            target = stage / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        load_package(stage)
    combined = deepcopy(previous)
    combined["articles"].append(runtime)
    existing_media = {m["id"]: m for m in combined["media"]["items"]}
    for item in media:
        if item["id"] in existing_media:
            require(item == existing_media[item["id"]], "Shared media record changed")
            require(assets[item["asset"]["path"]] == previous_files[item["asset"]["path"]], "Shared media bytes changed")
        else:
            combined["media"]["items"].append(item)
    entry = next(e for e in combined["issues"][0]["toc"] if e["id"] == TOC_ID)
    entry.update(article_ids=[ARTICLE_ID], link_status="matched")
    combined["catalog"] = catalog_for(combined["issues"], combined["articles"])
    combined_counts = validate_bundle(combined)
    combined_assets = {m["asset"]["path"]: previous_files[m["asset"]["path"]] for m in previous["media"]["items"] if m["asset"]}
    old_previews = [(r["article_id"], r["section_id"], r["path"], previous_files[r["path"]]) for r in previous_manifest["previews"]]
    combined_files = second.assemble(combined, {**combined_assets, **assets}, old_previews + previews)
    files = {**{"single/content/" + p: raw for p, raw in single_files.items()},
             **{"combined/content/" + p: raw for p, raw in combined_files.items()},
             "recovery.json": recovery.json_bytes(article), "inventory.json": recovery.json_bytes(reports),
             "blocks.json": recovery.json_bytes(mapping),
             "introduction.txt": recovery.topic_text(article["topics"][0]).encode(),
             "body.txt": recovery.topic_text(article["topics"][1]).encode()}
    validation = {"all_source_bytes_accounted_for": True, "source_projection_equal": True,
                  "bitmap_pixels_equal": True, "standalone_package_checked_before_composition": True,
                  "schema_version": 1, "schema_changed": False, "physical_magazine_compared": False}
    evidence = {"schema_version": 1, "article_id": ARTICLE_ID, "inputs": inputs, "topic_map": topic_map,
                "boundary_separators": boundaries, "toc_match": toc, "index_occurrences": occurrences,
                "font_policy": FONT_CODECS, "conversions": conversions,
                "tab_policy": {"source_controls": 30, "output_character": "U+0009", "expanded_to_spaces": False},
                "code_policy": "Preserve all listing text, tabs, blank lines, and source spelling; no compilation or correction.",
                "preview_content_ranges": ranges, "validation": validation,
                "outputs": [file_record(p, raw) for p, raw in sorted(files.items())]}
    files["provenance.json"] = recovery.json_bytes(evidence)
    record = {"schema_version": 1, "article_id": ARTICLE_ID, "toc_entry_id": TOC_ID,
              "schema_sha256": digest(SCHEMA_PATH.read_bytes()), "counts": counts, "combined_counts": combined_counts,
              "single_runtime_files": len(single_files), "combined_runtime_files": len(combined_files),
              "topic_map": topic_map, "listing_paragraphs": LISTING[1] - LISTING[0] + 1, "tab_characters": 30,
              "block_types": dict(sorted(Counter(b["kind"] for b in mapping["blocks"]).items())),
              "runs": sum(len(p["runs"]) for t in article["topics"] for p in t["paragraphs"]),
              "validation": validation,
              "outputs": [file_record(str((OUTPUT / p).relative_to(ROOT)), raw) for p, raw in sorted(files.items())]}
    return json.loads(recovery.json_bytes(record)), files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    try:
        record, files = build_article()
        if not args.write_record:
            require(record == json.loads(RECORD.read_bytes()), "Editor article differs from reviewed record")
        OUTPUT.mkdir(parents=True, exist_ok=True)
        for name in ("single", "combined"):
            prefix = name + "/"
            package.write_package(OUTPUT / name, {p[len(prefix):]: raw for p, raw in files.items() if p.startswith(prefix)})
        for path, raw in files.items():
            if not path.startswith(("single/", "combined/")):
                temporary = OUTPUT / (path + ".tmp")
                temporary.write_bytes(raw)
                temporary.replace(OUTPUT / path)
        if args.write_record:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_bytes(recovery.json_bytes(record))
        print(f"Editor article prepared: {record['counts']}; combined={record['combined_counts']}")
    except (OSError, ValueError, KeyError, StopIteration, ValidationError) as exc:
        print(f"Editor preparation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
