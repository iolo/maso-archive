"""Bounded CD1 step 12b.1: preserve and package the Gary Kildall interview."""

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
REFERENCE = "8802030"
ARTICLE_ID = "cd1:article:" + REFERENCE
TOC_ID = "maso-1988-02-toc-0031"
OUTPUT = ROOT / "build/cd1-articles/8802030"
RECORD = ROOT / "data/catalog/article-preparations/cd1-8802030.json"
PREVIOUS = second.OUTPUT / "combined/content"
QUESTIONS = [10, 13, 16, 19, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51,
             54, 57, 60, 63, 69, 72, 75, 79, 83, 87, 92, 95, 98]
FONT_CODECS = {4: "cp949", 5: "cp949"}
require = native.require


def block_id(topic, paragraph):
    return f"cd1-{REFERENCE}:T{topic}:P{paragraph:03d}-{paragraph:03d}"


def map_interview(article):
    """Preserve questions as bold paragraphs, with explicit private turn evidence."""
    require([t["ordinal"] for t in article["topics"]] == [145, 146], "Unexpected interview topics")
    body = article["topics"][1]["paragraphs"]
    questions = [p["ordinal"] for p in body if p["ordinal"] > 4 and p["runs"] and
                 all(r["kind"] == "text" and r["format"]["b"] for r in p["runs"])]
    require(questions == QUESTIONS, "Interview question boundaries changed")
    turns, answer_ids = [], set()
    for number, start in enumerate(questions):
        p = body[start - 1]
        require(p["format"].get("li") == 215 and p["format"].get("sa") == 95 and
                all(r["format"]["fs"] == 18 for r in p["runs"]), "Question style changed")
        stop = questions[number + 1] if number + 1 < len(questions) else len(body) + 1
        answers = [p for p in body[start:stop - 1] if p["text"].strip()]
        require(answers and all(all(r["kind"] == "text" and not r["format"]["b"] for r in p["runs"])
                               for p in answers), "Answer structure changed")
        answer_ids.update(p["ordinal"] for p in answers)
        turns.append({"question_block_id": block_id(146, start),
                      "answer_block_ids": [block_id(146, p["ordinal"]) for p in answers],
                      "basis": "bold_prompt_and_following_plain_paragraphs_before_next_prompt"})
    result = {"schema_version": 1, "cd_reference": REFERENCE, "blocks": [], "relationships": [],
              "interview_turns": turns, "verification": {"semantic_structure_verified": False}}
    for topic in article["topics"]:
        ordinal = topic["ordinal"]
        for p in topic["paragraphs"]:
            index = p["ordinal"]
            kind = "paragraph" if p["text"].strip() else "spacing"
            if index == 2:
                kind = "title"
            elif ordinal == 146 and index in (1, 4):
                kind = {1: "issue_label", 4: "byline"}[index]
            subtype = "interview_question" if ordinal == 146 and index in questions else (
                "interview_answer" if ordinal == 146 and index in answer_ids else None)
            result["blocks"].append({
                "id": block_id(ordinal, index), "topic_ordinal": ordinal, "kind": kind, "subtype": subtype,
                "parent_heading_id": None,
                "decision": {"basis": "interview_turn_evidence" if subtype else "source_paragraph_and_opening_metadata",
                             "review_concerns": []},
                "members": [{"paragraph_ordinal": index, "run_ordinals": list(range(1, len(p["runs"]) + 1)),
                             "source_span": p["source_span"]}],
                "source_span": p["source_span"],
                "content_sha256": digest(recovery.topic_text({"paragraphs": [p]}).encode()),
                "object_refs": [{"paragraph_ordinal": index, "run_ordinal": n, "resource": r["object"]["resource"],
                                 "rtf_byte_offset": r["object"]["byte_offset"]}
                                for n, r in enumerate(p["runs"], 1) if r["kind"] == "object"],
            })
    blocks.validate_map(article, result)
    return result


def recover_interview(mvb, rtf):
    topics = native.native_topics(mvb, 149)
    contexts = native.context_entries(mvb)
    require(contexts[native.context_hash(REFERENCE)]["topic_offset"] == topics[145]["topic_offset"], "Native target changed")
    pages = list(re.finditer(rb"(?<!\\)\\page\n", rtf))
    require(len(pages) == 3098, "RTF topic population changed")
    boundaries = []
    for ordinal in (144, 147):
        start, end = pages[ordinal - 2].end(), pages[ordinal - 1].start()
        require(rtf[start:end] == b"\\pard \\b ", "Neighbor separator changed")
        boundaries.append({"native": topics[ordinal - 1], "rtf": {"byte_offset": start, "byte_length": end - start,
                           "sha256": digest(rtf[start:end])}})
    mapping, reports, recovered, state = [], [], [], None
    for ordinal, alias, role in ((145, "3M4UJI", "linked_introduction"), (146, "6SRE0ZE", "reference_target_body")):
        start, end = pages[ordinal - 2].end(), pages[ordinal - 1].start()
        raw = rtf[start:end]
        require([m[1].decode() for m in native.CONTEXT_FOOTNOTE.finditer(raw)] == [alias], "RTF alias changed")
        context = contexts[native.context_hash(alias)]
        require(context["topic_offset"] == topics[ordinal - 1]["topic_offset"], "RTF/native mapping differs")
        links = re.findall(rb"\{\\v ([^}]+)\}", raw)
        require(links == ([] if ordinal == 145 else [b"3M4UJI"]), "Unaccounted linked topic")
        report = inventory.inspect_topic(raw, start, None if state is None else state["character"]["font_id"])
        require(not report["issues"], "Unsupported RTF construct needs review")
        report.update(ordinal=ordinal, role=role)
        topic = recovery.recover_topic(rtf, report, state, FONT_CODECS)
        require(not topic["issues"] and all(p["terminated_by_par"] for p in topic["paragraphs"]), "Incomplete interview decoding")
        state = topic["final_state"]
        mapping.append({"role": role, "alias": alias, "native": topics[ordinal - 1], "context": context,
                        "rtf": {"byte_offset": start, "byte_length": end - start, "end_exclusive": end, "sha256": digest(raw)}})
        reports.append(report)
        recovered.append(topic)
    require(native.context_hash(REFERENCE) == native.context_hash("6SRE0ZE"), "Reference/alias mismatch")
    require(topics[144]["next_topic_pos"] == topics[145]["topic_pos"] and
            topics[145]["next_topic_pos"] == topics[146]["topic_pos"] and
            topics[145]["browse_back_topic_offset"] == topics[142]["topic_offset"] and
            topics[145]["browse_forward_topic_offset"] == topics[148]["topic_offset"], "Article boundary chain changed")
    position = topics[145]["topic_pos"]
    size, length, _, _, data_length, kind = struct.unpack("<5iB", native.topic_read(mvb, position, 21))
    require(kind == 2 and length <= size - data_length, "Unsupported native title")
    title = native.topic_read(mvb, position, size)[data_length:data_length + length].split(b"\0")[0].decode("cp949")
    require(title == recovered[0]["paragraphs"][1]["text"] == "CP/M의 게리 킬달", "Native/introductory title differs")
    require([len(t["paragraphs"]) for t in recovered] == [4, 103], "Paragraph population changed")
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
    article, reports, topic_map, boundaries = recover_interview(mvb, rtf)
    mapping = map_interview(article)
    toc_entries = Snapshot(ROOT).artifact("toc-entries.jsonl")
    toc = next(e for e in toc_entries if e["id"] == TOC_ID)
    cd_entries = checked_artifact(ROOT / "build/cd1-index", "entries.jsonl")
    for path in ("TOC.md", "data/identities/toc.json", "build/toc/manifest.json", "build/toc/toc-entries.jsonl",
                 "build/cd1-index/manifest.json", "build/cd1-index/entries.jsonl", SCHEMA_PATH):
        read(path)
    title = article["topics"][0]["paragraphs"][1]["text"]
    prefix = "유명한 프로그래머를 만났읍니다(5) : "
    require(toc["title_candidate"] == prefix + title and toc["start_page_candidate"] == 30, "TOC match changed")
    require([e["id"] for e in toc_entries if e["issue_id"] == "maso-1988-02" and
             e["title_candidate"].removeprefix(prefix) == title] == [TOC_ID], "Ambiguous interview TOC match")
    occurrences = [e for e in cd_entries if e["reference"] == REFERENCE]
    require(len(occurrences) == 2 and all(e["title"] == title and e["display_issue"] == "1988-02" for e in occurrences), "CD label mismatch")
    for e in occurrences:
        source = e["source"]
        raw = read("private/cd1-probe/raw/" + source["name"], source["sha256"])
        require(raw[source["byte_offset"]:source["byte_offset"] + source["byte_length"]].rstrip(b"\r\n").decode("cp949") == e["raw_line"], "CD occurrence changed")
    body = article["topics"][1]["paragraphs"]
    require(body[0]["text"] == "88.2.  30p" and body[3]["text"] == "글/ 편집부", "Opening metadata changed")
    objects = [r["object"]["resource"] for t in article["topics"] for p in t["paragraphs"] for r in p["runs"] if r["kind"] == "object"]
    require(objects == ["bm42.bmp"], "Unexpected interview media")
    manifest = json.loads(read(images.MANIFEST))
    bitmap = images.checked_source("bm42.bmp", manifest)
    read(images.RAW / "bm42.bmp", digest(bitmap))
    with tempfile.TemporaryDirectory() as temporary:
        stage = Path(temporary)
        (stage / "assets").mkdir()
        conversion = images.convert_resource("bm42.bmp", bitmap, stage)
        require(conversion["status"] == "converted_pending_viewer" and conversion["pixel_equivalent"], "Bitmap needs explicit disposition")
        png = (stage / "assets/bm42.bmp.png").read_bytes()
        for command in conversion["commands"]:
            command["argv"] = [a.replace(temporary, "<conversion-stage>") for a in command["argv"]]
    conversion["tool_version"] = images.command(["convert", "-version"])["stdout"].splitlines()[0]
    media = {"id": "cd1:media:bm42.bmp", "source": {"disc_id": "cd1", "resource": "bm42.bmp"},
             "status": "available", "reason": None, "problem_ids": [], "rendering_notes": [],
             "asset": {**file_record("media/cd1/bm42.bmp.png", png), "mime_type": "image/png",
                       "dimensions": {"width": 32, "height": 25, "unit": "px"}}}
    require((conversion["png_pixels"]["width"], conversion["png_pixels"]["height"]) == (32, 25), "Bitmap dimensions changed")
    runtime = {"schema_version": 1, "kind": "article", "id": ARTICLE_ID, "issue_id": "maso-1988-02",
               "title": title, "byline": body[3]["text"], "pages": {"start": 30, "end": None},
               "source": {"disc_id": "cd1", "reference": REFERENCE}, "toc_entry_ids": [TOC_ID],
               "content_status": "available", "extraction_status": "checked",
               "print_verification": {"status": "pending", "report_id": None, "pages_compared": []},
               "sections": second.reading_sections(article, mapping, REFERENCE, 145), "relationships": []}
    previous_record = json.loads(read(second.RECORD))
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
              "catalog": catalog_for([issue], [runtime]), "media": {"schema_version": 1, "kind": "media_index", "items": [media]}}
    counts = validate_bundle(bundle)
    for section, topic in zip(runtime["sections"], article["topics"]):
        require(project_section(section, {media["id"]: media}) == recovery.topic_text(topic), "Interview projection changed")
    rendered, locations = markdown.render(article, mapping)
    previews, ranges = [], []
    for section in runtime["sections"]:
        name = section["role"] + ".md"
        raw, selected = package.package_preview(rendered[name], [r for r in locations if r["path"] == name])
        path = f"previews/cd1/{REFERENCE}/{name}"
        previews.append((ARTICLE_ID, section["id"], path, raw))
        ranges.extend({"path": path, **r} for r in selected)
    assets = {media["asset"]["path"]: png}
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
    combined["media"]["items"].append(media)
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
    bibliographic_note = {"reported_by": "owner", "work_title": "Programmers at Work",
                          "relationship": "translated_interview", "verified_against_book": False,
                          "book_credit_observed_in_recovered_cd_text": False}
    evidence = {"schema_version": 1, "article_id": ARTICLE_ID, "inputs": inputs, "topic_map": topic_map,
                "boundary_separators": boundaries, "toc_match": toc, "index_occurrences": occurrences,
                "title_comparison": {"toc_prefix_removed": prefix, "application": "this_record_only"},
                "font_policy": FONT_CODECS, "conversion": conversion, "interview_turns": mapping["interview_turns"],
                "bibliographic_note": bibliographic_note,
                "numbering_note": "TOC series label (5) and introduction's fourth programmer retained without harmonization",
                "preview_content_ranges": ranges, "validation": validation,
                "outputs": [file_record(p, raw) for p, raw in sorted(files.items())]}
    files["provenance.json"] = recovery.json_bytes(evidence)
    record = {"schema_version": 1, "article_id": ARTICLE_ID, "toc_entry_id": TOC_ID,
              "schema_sha256": digest(SCHEMA_PATH.read_bytes()), "counts": counts, "combined_counts": combined_counts,
              "single_runtime_files": len(single_files), "combined_runtime_files": len(combined_files),
              "topic_map": topic_map, "interview_turns": len(mapping["interview_turns"]),
              "block_types": dict(sorted(Counter(b["kind"] for b in mapping["blocks"]).items())),
              "runs": sum(len(p["runs"]) for t in article["topics"] for p in t["paragraphs"]),
              "bibliographic_note": bibliographic_note, "validation": validation,
              "outputs": [file_record(str((OUTPUT / p).relative_to(ROOT)), raw) for p, raw in sorted(files.items())]}
    return json.loads(recovery.json_bytes(record)), files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    try:
        record, files = build_article()
        if not args.write_record:
            require(record == json.loads(RECORD.read_bytes()), "Interview differs from reviewed record")
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
        print(f"Interview prepared: {record['counts']}; turns={record['interview_turns']}; combined={record['combined_counts']}")
    except (OSError, ValueError, KeyError, StopIteration, ValidationError) as exc:
        print(f"Interview preparation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
