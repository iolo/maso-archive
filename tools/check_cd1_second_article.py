"""Bounded second-case recovery and v1 package check: CD1 8802114."""

import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
import sys
import tempfile

from jsonschema.exceptions import ValidationError

from maso_archive.reading_room import SCHEMA_PATH, catalog_for, project_section, validate_bundle
from maso_archive.reading_room_package import file_record, load_package
from tools import inventory_cd1_rtf as inventory
from tools import map_cd1_blocks as blocks
from tools import map_cd1_images as images
from tools import map_cd1_topic as native
from tools import recover_cd1_text as recovery
from tools import render_cd1_markdown as markdown
from tools import build_reading_room_package as package
from tools.decode_cd1_paragraph import digest
from tools.verify_cd1_match import checked_artifact
from tools.toc_snapshot import Snapshot, read_input

ROOT = native.ROOT
REFERENCE = "8802114"
ARTICLE_ID = "cd1:article:" + REFERENCE
TOC_ID = "maso-1988-02-toc-0021"
OUTPUT = ROOT / "build/cd1-second-article/8802114"
RECORD = ROOT / "data/catalog/second-article-checks/cd1-8802114.json"
FONT_CODECS = {4: "cp949", 5: "cp949", 6: "cp949", 15: "ascii"}
LISTINGS = [(26, 342), (346, 381), (385, 480)]
CAPTIONS = [(24, 26), (344, 346), (383, 385)]
require = native.require


def block_map(article):
    result = {"schema_version": 1, "cd_reference": REFERENCE, "blocks": [], "relationships": [],
              "verification": {"semantic_structure_verified": False}}
    for topic in article["topics"]:
        ordinal, paragraphs = topic["ordinal"], topic["paragraphs"]
        declarations = {2: (2, "title", "source_title")}
        if ordinal == 152:
            declarations.update({1: (1, "issue_label", "explicit_issue_page_label"),
                                 4: (4, "byline", "explicit_editorial_byline"),
                                 10: (10, "heading", "unnumbered_bold_24_half_points_indent_215"),
                                 14: (14, "heading", "unnumbered_bold_24_half_points_indent_215"),
                                 18: (18, "code", "isolated_command_between_usage_instructions")})
            for number, ((start, end), (caption, target)) in enumerate(zip(LISTINGS, CAPTIONS), 1):
                require(start == target and paragraphs[caption - 1]["text"].startswith(f"<리스트 {number}> "), "Listing caption changed")
                require(paragraphs[start - 1]["text"].lower().startswith("program ") and
                        paragraphs[end - 1]["text"].lower() == "end.", "Listing boundaries changed")
                require(all(r["format"]["font_id"] == 15 for p in paragraphs[start - 1:end] for r in p["runs"]), "Listing font changed")
                require(not paragraphs[start - 2]["text"] and not paragraphs[end]["text"], "Listing separator changed")
                declarations[start] = (end, "code", "caption_program_end_and_Fixedsys_runs")
                declarations[caption] = (caption, "caption", "numbered_listing_label")
        index, parent = 1, None
        while index <= len(paragraphs):
            paragraph = paragraphs[index - 1]
            end, kind, basis = declarations.get(index, (index, "paragraph" if paragraph["text"].strip() else "spacing", "source_paragraph"))
            if kind == "heading":
                require(paragraph["format"].get("li") == 215 and all(r["format"]["b"] and r["format"]["fs"] == 24 for r in paragraph["runs"]), "Heading evidence changed")
            members = paragraphs[index - 1:end]
            block = {"id": f"cd1-{REFERENCE}:T{ordinal}:P{index:03d}-{end:03d}", "topic_ordinal": ordinal,
                     "kind": kind, "parent_heading_id": None if kind == "heading" else parent,
                     "decision": {"basis": basis, "review_concerns": []},
                     "members": [{"paragraph_ordinal": p["ordinal"], "run_ordinals": list(range(1, len(p["runs"]) + 1)), "source_span": p["source_span"]} for p in members],
                     "source_span": {"byte_offset": members[0]["source_span"]["byte_offset"], "end_exclusive": members[-1]["source_span"]["end_exclusive"]},
                     "content_sha256": digest(recovery.topic_text({"paragraphs": members}).encode()),
                     "object_refs": [{"paragraph_ordinal": p["ordinal"], "run_ordinal": n, "resource": r["object"]["resource"], "rtf_byte_offset": r["object"]["byte_offset"]}
                                     for p in members for n, r in enumerate(p["runs"], 1) if r["kind"] == "object"]}
            if kind == "heading":
                block["heading_level"] = 1
                parent = block["id"]
            result["blocks"].append(block)
            index = end + 1
    by_start = {b["members"][0]["paragraph_ordinal"]: b["id"] for b in result["blocks"] if b["topic_ordinal"] == 152}
    result["relationships"] = [{"kind": "caption_for", "from_block": by_start[c], "to_block": by_start[t]} for c, t in CAPTIONS]
    blocks.validate_map(article, result)
    return result


def reading_sections(article, mapping):
    sections = []
    for topic in article["topics"]:
        section = {"id": f"cd1:topic:{topic['ordinal']}", "role": "introduction" if topic["ordinal"] == 151 else "body", "blocks": []}
        for block in mapping["blocks"]:
            if block["topic_ordinal"] != topic["ordinal"]:
                continue
            paragraphs = []
            for member in block["members"]:
                source = topic["paragraphs"][member["paragraph_ordinal"] - 1]
                identifier = f"cd1-{REFERENCE}:T{topic['ordinal']}:P{source['ordinal']:03d}"
                runs = []
                for n, run in enumerate(source["runs"], 1):
                    require(run["kind"] in ("text", "object"), "Unresolved decoding cannot become reading text")
                    marks = [name for key, name in (("b", "bold"), ("ul", "underline")) if run["format"][key]]
                    runs.append({"type": "text", "text": run["text"], "marks": marks} if run["kind"] == "text" else
                                {"type": "media", "media_id": "cd1:media:" + run["object"]["resource"], "occurrence_id": identifier + f":R{n}", "marks": marks})
                paragraphs.append({"id": identifier, "runs": runs})
            section["blocks"].append({"id": block["id"], "type": block["kind"],
                                      "layout": "preformatted" if block["kind"] == "code" else "spacing" if block["kind"] == "spacing" else "flow",
                                      "heading_level": block.get("heading_level"), "parent_heading_id": block["parent_heading_id"],
                                      "interpretation": "source_supported", "paragraphs": paragraphs})
        sections.append(section)
    return sections


def assemble(bundle, assets, previews):
    """Split a validated logical bundle without inventing IDs from filenames."""
    validate_bundle(bundle)
    files = dict(assets)
    documents = []
    rows = [("catalog.json", bundle["catalog"]), ("media.json", bundle["media"])]
    rows += [(f"issues/{i['id']}.json", i) for i in bundle["issues"]]
    rows += [(f"articles/{a['source']['disc_id']}/{a['source']['reference']}.json", a) for a in bundle["articles"]]
    for path, document in rows:
        require(path not in files, "Duplicate runtime path")
        files[path] = recovery.json_bytes(document)
        documents.append({"kind": document["kind"], "id": document.get("id"), **file_record(path, files[path])})
    records = []
    for article_id, section_id, path, raw in previews:
        require(path not in files, "Duplicate preview path")
        files[path] = raw
        records.append({"article_id": article_id, "section_id": section_id, **file_record(path, raw)})
    files["manifest.json"] = recovery.json_bytes({"schema_version": 1, "kind": "package_manifest", "documents": documents, "previews": records})
    return files


def build_check():
    inputs = {}
    def read(path, expected=None):
        path = ROOT / path
        raw = read_input(ROOT, path)
        require(expected is None or digest(raw) == expected, f"Changed source: {path.relative_to(ROOT)}")
        inputs[str(path.relative_to(ROOT))] = file_record(str(path.relative_to(ROOT)), raw)
        return raw

    mvb, rtf = [read(path, checksum) for path, checksum in native.SOURCES.items()]
    previous_map = json.loads(read(native.RECORD))
    native_topics = native.native_topics(mvb, 155)
    contexts = native.context_entries(mvb)
    pages = list(re.finditer(rb"(?<!\\)\\page\n", rtf))
    require(len(pages) == 3098, "RTF topic count changed")
    topic_map, reports, topics, state = [], [], [], None
    for ordinal, alias, role in ((151, "3M4LHC", "linked_introduction"), (152, "1KN6EK", "reference_target_body")):
        start, end = pages[ordinal - 2].end(), pages[ordinal - 1].start()
        raw = rtf[start:end]
        span = {"byte_offset": start, "byte_length": end - start, "end_exclusive": end, "sha256": digest(raw)}
        prior = next(t for t in previous_map["topics"] if t["native"]["ordinal"] == ordinal)
        require(span == prior["rtf"] and native_topics[ordinal - 1] == prior["native"], "Neighbor mapping changed")
        require([m[1].decode() for m in native.CONTEXT_FOOTNOTE.finditer(raw)] == [alias], "RTF context mismatch")
        require(contexts[native.context_hash(alias)]["topic_offset"] == native_topics[ordinal - 1]["topic_offset"], "Native alias mismatch")
        report = inventory.inspect_topic(raw, start, None if state is None else state["character"]["font_id"])
        require(not report["issues"], "New RTF construct requires a separate investigation")
        report.update(ordinal=ordinal, role=role)
        topic = recovery.recover_topic(rtf, report, state, FONT_CODECS)
        require(not topic["issues"] and all(p["terminated_by_par"] for p in topic["paragraphs"]), "Unsupported text/paragraph ending requires explicit contract review")
        state = topic["final_state"]
        topic_map.append({"role": role, "rtf": span, "native": native_topics[ordinal - 1], "alias": alias, "context": contexts[native.context_hash(alias)]})
        reports.append(report)
        topics.append(topic)
    require(native.context_hash(REFERENCE) == native.context_hash("1KN6EK"), "Reference hash mismatch")
    require(native_topics[151]["browse_forward_topic_offset"] == native_topics[154]["topic_offset"], "Next browse boundary changed")
    require(native_topics[151]["next_topic_pos"] == native_topics[152]["topic_pos"], "Following boundary changed")
    following = rtf[pages[151].end():pages[152].start()]
    require(following == b"\\pard \\b\\fs18 ", "Unexpected following separator")
    links = re.findall(rb"\{\\v ([^}]+)\}", rtf[topic_map[1]["rtf"]["byte_offset"]:topic_map[1]["rtf"]["end_exclusive"]])
    require(links == [b"3M4LHC"], "Unexpected hidden link requires boundary review")
    font = re.search(rb"\{\\f15\\froman Fixedsys;\}", rtf[:rtf.index(b"\n{\\colortbl")])
    require(font is not None, "Font 15 definition changed")
    fonts = {str(n): re.search(rb"\{\\f" + str(n).encode() + rb"\\[a-z]+ ([^{};]+);\}", rtf[:rtf.index(b"\n{\\colortbl")])[1].decode("cp949") for n in FONT_CODECS}

    entries = Snapshot(ROOT).artifact("toc-entries.jsonl")
    cd_entries = checked_artifact(ROOT / "build/cd1-index", "entries.jsonl")
    for path in ("build/toc/manifest.json", "build/toc/toc-entries.jsonl", "build/cd1-index/manifest.json", "build/cd1-index/entries.jsonl", "data/identities/toc.json", "TOC.md", SCHEMA_PATH):
        read(path)
    toc = next(e for e in entries if e["id"] == TOC_ID)
    occurrences = [e for e in cd_entries if e["reference"] == REFERENCE]
    require(len(occurrences) == 3 and all(e["title"] == "스펠링 체커" and e["display_issue"] == "1988-02" for e in occurrences), "Index evidence changed")
    require([e["id"] for e in entries if e["issue_id"] == "maso-1988-02" and e["title_candidate"] == "스펠링 체커"] == [TOC_ID], "Ambiguous TOC match")
    require(toc["start_page_candidate"] == 114 and topics[1]["paragraphs"][0]["text"] == "88.2.  114p", "Page evidence differs")
    for occurrence in occurrences:
        source = occurrence["source"]
        raw = read("private/cd1-probe/raw/" + source["name"], source["sha256"])
        require(raw[source["byte_offset"]:source["byte_offset"] + source["byte_length"]].rstrip(b"\r\n").decode("cp949") == occurrence["raw_line"], "Index byte span differs")
    article = {"schema_version": 1, "cd_reference": REFERENCE, "topics": topics}
    mapping = block_map(article)
    objects = [r["object"]["resource"] for t in topics for p in t["paragraphs"] for r in p["runs"] if r["kind"] == "object"]
    require(objects == ["bm40.bmp"], "Unexpected media requires inspection")
    manifest = json.loads(read(images.MANIFEST))
    bitmap = images.checked_source("bm40.bmp", manifest)
    read(images.RAW / "bm40.bmp", digest(bitmap))
    with tempfile.TemporaryDirectory() as directory:
        stage = Path(directory)
        (stage / "assets").mkdir()
        conversion = images.convert_resource("bm40.bmp", bitmap, stage)
        require(conversion["status"] == "converted_pending_viewer" and conversion["pixel_equivalent"], "Bitmap conversion needs a recorded disposition")
        png = (stage / "assets/bm40.bmp.png").read_bytes()
        for command in conversion["commands"]:
            command["argv"] = [a.replace(directory, "<conversion-stage>") for a in command["argv"]]
    conversion["tool_version"] = images.command(["convert", "-version"])["stdout"].splitlines()[0]
    media = {"id": "cd1:media:bm40.bmp", "source": {"disc_id": "cd1", "resource": "bm40.bmp"},
             "status": "available", "reason": None, "problem_ids": [], "rendering_notes": [],
             "asset": {**file_record("media/cd1/bm40.bmp.png", png), "mime_type": "image/png",
                       "dimensions": {"width": conversion["png_pixels"]["width"], "height": conversion["png_pixels"]["height"], "unit": "px"}}}
    runtime = {"schema_version": 1, "kind": "article", "id": ARTICLE_ID, "issue_id": "maso-1988-02",
               "title": topics[0]["paragraphs"][1]["text"], "byline": topics[1]["paragraphs"][3]["text"],
               "pages": {"start": 114, "end": None}, "source": {"disc_id": "cd1", "reference": REFERENCE}, "toc_entry_ids": [TOC_ID],
               "content_status": "available", "extraction_status": "checked", "print_verification": {"status": "pending", "report_id": None, "pages_compared": []},
               "sections": reading_sections(article, mapping),
               "relationships": [{"type": "caption_for", "from_block": r["from_block"], "to_block": r["to_block"]} for r in mapping["relationships"]]}

    first, first_manifest, _ = load_package(package.OUTPUT / "content")
    first_record = json.loads(read(package.RECORD))
    first_files = {r["path"]: read(package.OUTPUT / "content" / r["path"], r["sha256"]) for r in first_record["outputs"]}
    issue = deepcopy(first["issues"][0])
    for entry in issue["toc"]:
        entry.update(article_ids=[ARTICLE_ID] if entry["id"] == TOC_ID else [], link_status="matched" if entry["id"] == TOC_ID else "unmatched")
    bundle = {"schema_version": 1, "kind": "contract_example", "issues": [issue], "articles": [runtime],
              "catalog": catalog_for([issue], [runtime]), "media": {"schema_version": 1, "kind": "media_index", "items": [media]}}
    counts = validate_bundle(bundle)
    for section, topic in zip(runtime["sections"], topics):
        require(project_section(section, {media["id"]: media}) == recovery.topic_text(topic), "Source text/whitespace changed")
    original_previews, locations = markdown.render(article, mapping)
    previews, preview_ranges = [], []
    for section in runtime["sections"]:
        name = section["role"] + ".md"
        raw, ranges = package.package_preview(original_previews[name], [r for r in locations if r["path"] == name])
        path = f"previews/cd1/{REFERENCE}/{name}"
        previews.append((ARTICLE_ID, section["id"], path, raw))
        preview_ranges.extend({"path": path, **r} for r in ranges)
    assets = {media["asset"]["path"]: png}
    solo_files = assemble(bundle, assets, previews)
    combined = deepcopy(first)
    combined["articles"].append(runtime)
    combined["media"]["items"].append(media)
    entry = next(e for e in combined["issues"][0]["toc"] if e["id"] == TOC_ID)
    entry.update(article_ids=[ARTICLE_ID], link_status="matched")
    combined["catalog"] = catalog_for(combined["issues"], combined["articles"])
    combined_counts = validate_bundle(combined)
    combined_assets = {m["asset"]["path"]: first_files[m["asset"]["path"]] for m in first["media"]["items"] if m["asset"]}
    combined_previews = [(r["article_id"], r["section_id"], r["path"], first_files[r["path"]]) for r in first_manifest["previews"]]
    combined_files = assemble(combined, {**combined_assets, **assets}, combined_previews + previews)
    files = {**{"single/content/" + p: raw for p, raw in solo_files.items()},
             **{"combined/content/" + p: raw for p, raw in combined_files.items()},
             "recovery.json": recovery.json_bytes(article), "inventory.json": recovery.json_bytes(reports),
             "blocks.json": recovery.json_bytes(mapping), "introduction.txt": recovery.topic_text(topics[0]).encode(),
             "body.txt": recovery.topic_text(topics[1]).encode()}
    evidence = {"schema_version": 1, "article_id": ARTICLE_ID, "inputs": inputs, "topic_map": topic_map,
                "following_boundary": native_topics[152:155], "toc_match": toc, "index_occurrences": occurrences,
                "font_policy": FONT_CODECS, "font_names": fonts, "conversion": conversion, "preview_content_ranges": preview_ranges,
                "validation": {"all_source_bytes_accounted_for": True, "source_projection_equal": True, "bitmap_pixels_equal": True,
                               "schema_version": 1, "schema_changed": False, "physical_magazine_compared": False},
                "outputs": [file_record(p, raw) for p, raw in sorted(files.items())]}
    files["provenance.json"] = recovery.json_bytes(evidence)
    record = {"schema_version": 1, "article_id": ARTICLE_ID, "toc_entry_id": TOC_ID,
              "schema_sha256": digest(SCHEMA_PATH.read_bytes()), "counts": counts, "combined_counts": combined_counts,
              "single_runtime_files": len(solo_files), "combined_runtime_files": len(combined_files),
              "block_types": dict(sorted(Counter(b["kind"] for b in mapping["blocks"]).items())), "listing_paragraph_ranges": LISTINGS,
              "fixedsys_ascii_runs": sum(r["format"]["font_id"] == 15 for t in topics for p in t["paragraphs"] for r in p["runs"]),
              "literal_brace_guards_removed": sum(len(t["transformations"]) for t in topics), "validation": evidence["validation"],
              "outputs": [file_record(str((OUTPUT / p).relative_to(ROOT)), raw) for p, raw in sorted(files.items())]}
    # JSON arrays, not Python tuples, for stable comparisons to the tracked record.
    return json.loads(recovery.json_bytes(record)), files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    try:
        record, files = build_check()
        if not args.write_record:
            require(record == json.loads(RECORD.read_bytes()), "Second-article result differs from reviewed record")
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
        print(f"Second article and two-article package validate against unchanged v1: {record['counts']}; combined={record['combined_counts']}")
    except (OSError, ValueError, KeyError, StopIteration, ValidationError) as error:
        print(f"Second-article check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
