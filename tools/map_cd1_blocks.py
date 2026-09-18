"""Map semantic blocks for the reviewed CD1 pilot; no Markdown rendering yet.

Run python3 -m tools.map_cd1_blocks. Explicit pilot decisions are scoped to the
checksummed recovery, not presented as a collection-wide classification engine.
"""

import argparse
from collections import Counter
import json
import re
import sys

from tools import recover_cd1_text as recovery
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import ROOT, require

SOURCE = ROOT / "build/cd1-text/8802065/article.json"
SOURCE_SHA256 = "d92a4231df2dce3d81bbf709e8191bde741397a77218cc5e61aaa6a130b0b1a1"
OUTPUT = ROOT / "build/cd1-blocks/8802065"
RECORD = ROOT / "data/catalog/block-maps/cd1-8802065.json"

# Paragraph ranges inspected in the source, including context on both sides.
# Each tuple is (start, end, subtype, evidence, review concerns).
EXAMPLES = [
    *[(n, n, "command_example", "isolated_prompt_and_explanatory_context", [])
      for n in (59, 67, 71, 76, 80, 85, 90, 100, 105, 109, 113, 261)],
    (255, 257, "terminal_transcript", "prompt_usage_output_prompt_sequence", []),
    (137, 145, "roff_mm_example", "figure_4_caption_and_macro_sequence", []),
    (156, 173, "roff_tbl_example", "figure_6_caption_and_DS_TS_TE_DE_delimiters",
     ["ten_inline_objects_require_image_inspection; example_is_not_text_only"]),
    (182, 202, "pic_example", "figure_8_caption_and_PS_PE_delimiters", []),
    (212, 217, "eqn_example", "figure_10_caption_and_EQ_EN_delimiters", []),
]
# Caption -> content references are relationships; they do not re-own paragraphs.
CAPTIONS = [(20, 21, "figure", 1), (37, 38, "figure", 2), (128, 129, "figure", 3),
            (136, 137, "figure", 4), (147, 148, "figure", 5), (154, 156, "figure", 6),
            (175, 176, "figure", 7), (180, 182, "figure", 8), (207, 208, "figure", 9),
            (210, 212, "figure", 10), (229, 230, "figure", 11), (244, 245, "figure", 12),
            (282, 283, "table", 1)]
DELIMITERS = {137: (".TL", ".MT 4"), 156: (".DS", ".DE"),
              182: (".PS", ".PE"), 212: (".EQ", ".EN")}


def heading_level(paragraph):
    """Require both observed heading formatting and a matching numbered label."""
    runs = paragraph["runs"]
    if not runs or not all(r["kind"] == "text" and r["format"]["b"] for r in runs):
        return None
    sizes = {r["format"]["fs"] for r in runs}
    if len(sizes) != 1 or paragraph["format"].get("li") != 215:
        return None
    level = {24: 1, 20: 2, 18: 3}.get(next(iter(sizes)))
    pattern = {1: r"^[IVX]+\. ", 2: r"^\d+\. ", 3: r"^\(\d+\) "}.get(level)
    return level if pattern and re.match(pattern, paragraph["text"]) else None


def map_article(article):
    blocks, relationships = [], []
    for topic in article["topics"]:
        ordinal, paragraphs = topic["ordinal"], topic["paragraphs"]
        require(ordinal in (148, 149), "Unexpected topic")
        declarations = {}
        if ordinal == 148:
            declarations[2] = (2, "title", "introductory_title", "linked_topic_title", [])
        else:
            declarations.update({1: (1, "issue_label", None, "explicit_issue_page_label", []),
                                 2: (2, "title", "with_navigation_icon", "native_title_and_large_bold_runs",
                                     ["navigation_icon_role_pending_viewer"]),
                                 4: (4, "byline", None, "byline_prefix_at_article_opening", []),
                                 174: (174, "unresolved", "adjacent_object", "object_between_example_end_and_next_caption",
                                       ["bm54.wmf_attachment_unknown_until_image_inspection"])})
            for start, end, subtype, evidence, concerns in EXAMPLES:
                require(start not in declarations, "Overlapping declared start")
                declarations[start] = (end, "code", subtype, evidence, concerns)
                first, last = paragraphs[start - 1]["text"], paragraphs[end - 1]["text"]
                if start in DELIMITERS:
                    require((first, last) == DELIMITERS[start], "Example boundary changed")
                else:
                    require(first.startswith("%"), "Missing command prompt")
                    require(not paragraphs[start - 2]["text"].strip() and not paragraphs[end]["text"].strip(),
                            "Command block context changed")
                if subtype == "terminal_transcript":
                    require(paragraphs[start]["text"].startswith("usage:") and last == "%", "Transcript changed")
            for caption, target, kind, number in CAPTIONS:
                label = "그림" if kind == "figure" else "표"
                require(paragraphs[caption - 1]["text"].startswith(f"<{label} {number}> "), "Caption label changed")
                declarations[caption] = (caption, "caption", kind, "label_and_reviewed_content_context", [])
                if target not in declarations:
                    concerns = ["image_contents_pending_inspection"]
                    if kind == "table" or number == 7:
                        concerns.append("table_cells_not_reconstructed")
                    declarations[target] = (target, "table" if kind == "table" else "figure",
                                            "image_backed", "caption_link_and_object_run", concerns)
        index, heading_stack = 1, []
        while index <= len(paragraphs):
            paragraph = paragraphs[index - 1]
            level = heading_level(paragraph) if ordinal == 149 else None
            if index in declarations:
                end, kind, subtype, evidence, concerns = declarations[index]
            elif level:
                end, kind, subtype, evidence, concerns = index, "heading", None, "numbered_label_bold_size_and_indent", []
            elif not paragraph["text"].strip():
                end, kind, subtype, evidence, concerns = index, "spacing", None, "blank_or_whitespace_only_paragraph", []
            else:
                end, kind, subtype, evidence, concerns = index, "paragraph", None, "preserved_paragraph_without_stronger_block_evidence", []
            require(not any(n in declarations for n in range(index + 1, end + 1)), "Overlapping block declarations")
            members = paragraphs[index - 1:end]
            block = {"id": f"cd1-8802065:T{ordinal}:P{index:03d}-{end:03d}",
                     "topic_ordinal": ordinal, "kind": kind, "subtype": subtype,
                     "decision": {"status": "source_supported_pending_viewer" if kind != "unresolved" else "unresolved",
                                  "basis": evidence, "review_concerns": concerns},
                     "members": [{"paragraph_ordinal": p["ordinal"], "run_ordinals": list(range(1, len(p["runs"]) + 1)),
                                  "source_span": p["source_span"]} for p in members],
                     "source_span": {"byte_offset": members[0]["source_span"]["byte_offset"],
                                     "end_exclusive": members[-1]["source_span"]["end_exclusive"]},
                     "content_sha256": digest(recovery.topic_text({"paragraphs": members}).encode("utf-8")),
                     "object_refs": [{"paragraph_ordinal": p["ordinal"], "run_ordinal": n,
                                      "resource": run["object"]["resource"],
                                      "rtf_byte_offset": run["object"]["byte_offset"],
                                      "role": "navigation_icon_candidate" if ordinal == 149 and index == 2 else "content_or_layout_pending_inspection"}
                                     for p in members for n, run in enumerate(p["runs"], 1) if run["kind"] == "object"]}
            if kind == "heading":
                while heading_stack and heading_stack[-1][0] >= level:
                    heading_stack.pop()
                require(level == 1 or (heading_stack and heading_stack[-1][0] == level - 1), "Heading level skipped")
                block["heading_level"] = level
                block["parent_heading_id"] = heading_stack[-1][1] if heading_stack else None
                heading_stack.append((level, block["id"]))
            else:
                block["parent_heading_id"] = heading_stack[-1][1] if heading_stack else None
            if kind == "code":
                block["representation"] = "mixed_text_objects" if block["object_refs"] else "preformatted_text"
                block["language"] = None  # no speculative Markdown highlighter label
            blocks.append(block)
            index = end + 1
    body_lookup = {b["members"][0]["paragraph_ordinal"]: b for b in blocks if b["topic_ordinal"] == 149}
    for caption, target, kind, number in CAPTIONS:
        relationships.append({"kind": "caption_for", "label_kind": kind, "label_number": number,
                              "from_block": body_lookup[caption]["id"], "to_block": body_lookup[target]["id"],
                              "status": "source_supported_pending_viewer"})
    result = {"schema_version": 1, "cd_reference": "8802065", "blocks": blocks, "relationships": relationships,
              "verification": {"viewer_compared": False, "semantic_structure_verified": False}}
    validate_map(article, result)
    return result


def validate_map(article, block_map):
    """Prove exact paragraph/run/object coverage and byte-identical projection."""
    ids = [b["id"] for b in block_map["blocks"]]
    require(len(ids) == len(set(ids)), "Duplicate block ID")
    expected_topics = [t["ordinal"] for t in article["topics"]]
    require(all(b["topic_ordinal"] in expected_topics for b in block_map["blocks"]), "Unexpected block topic")
    actual_order = [b["topic_ordinal"] for b in block_map["blocks"]]
    require(actual_order == sorted(actual_order, key=expected_topics.index), "Reordered topics")
    for topic in article["topics"]:
        selected = [b for b in block_map["blocks"] if b["topic_ordinal"] == topic["ordinal"]]
        members = [m for b in selected for m in b["members"]]
        require([m["paragraph_ordinal"] for m in members] == [p["ordinal"] for p in topic["paragraphs"]],
                "Missing, duplicated, or reordered paragraph")
        for member, paragraph in zip(members, topic["paragraphs"]):
            require(member["run_ordinals"] == list(range(1, len(paragraph["runs"]) + 1)), "Run coverage changed")
            require(member["source_span"] == paragraph["source_span"], "Paragraph source span changed")
        for block in selected:
            ps = [topic["paragraphs"][m["paragraph_ordinal"] - 1] for m in block["members"]]
            require(block["content_sha256"] == digest(recovery.topic_text({"paragraphs": ps}).encode("utf-8")),
                    "Block text/spacing changed")
            objects = [(p["ordinal"], n, r["object"]["resource"], r["object"]["byte_offset"])
                       for p in ps for n, r in enumerate(p["runs"], 1) if r["kind"] == "object"]
            require(objects == [(o["paragraph_ordinal"], o["run_ordinal"], o["resource"], o["rtf_byte_offset"])
                                for o in block["object_refs"]], "Object coverage/order changed")
            require(block["source_span"] == {"byte_offset": ps[0]["source_span"]["byte_offset"],
                                             "end_exclusive": ps[-1]["source_span"]["end_exclusive"]}, "Block span changed")
    by_id = {b["id"]: b for b in block_map["blocks"]}
    for link in block_map["relationships"]:
        require(link["from_block"] in by_id and link["to_block"] in by_id, "Dangling caption relation")
        require(by_id[link["from_block"]]["kind"] == "caption", "Relationship source is not a caption")
        require(by_id[link["to_block"]]["kind"] in ("code", "figure", "table"), "Invalid caption content target")
    for block in block_map["blocks"]:
        parent = block["parent_heading_id"]
        if parent is not None:
            require(parent in by_id and by_id[parent]["kind"] == "heading"
                    and by_id[parent]["topic_ordinal"] == block["topic_ordinal"]
                    and ids.index(parent) < ids.index(block["id"]), "Invalid heading parent")
    require(not block_map["verification"]["semantic_structure_verified"], "Viewer review is still pending")


def build_map():
    raw = SOURCE.read_bytes()
    require(digest(raw) == SOURCE_SHA256, "Changed structured recovery; re-review pilot decisions")
    article = json.loads(raw)
    block_map = map_article(article)
    block_map["source"] = {"path": str(SOURCE.relative_to(ROOT)), "sha256": SOURCE_SHA256}
    encoded = recovery.json_bytes(block_map)
    blocks = block_map["blocks"]
    record = {"schema_version": 1, "cd_reference": "8802065", "source": block_map["source"],
              "counts": {"blocks": len(blocks), "paragraphs": sum(len(b["members"]) for b in blocks),
                         "runs": sum(len(m["run_ordinals"]) for b in blocks for m in b["members"]),
                         "objects": sum(len(b["object_refs"]) for b in blocks),
                         "block_types": dict(sorted(Counter(b["kind"] for b in blocks).items())),
                         "heading_levels": dict(sorted(Counter(str(b["heading_level"]) for b in blocks if b["kind"] == "heading").items())),
                         "caption_relationships": len(block_map["relationships"])},
              "code_ranges": [{"topic": b["topic_ordinal"], "start_paragraph": b["members"][0]["paragraph_ordinal"],
                               "end_paragraph": b["members"][-1]["paragraph_ordinal"], "subtype": b["subtype"],
                               "representation": b["representation"], "objects": len(b["object_refs"])} for b in blocks if b["kind"] == "code"],
              "review_items": [{"block_id": b["id"], "concerns": b["decision"]["review_concerns"]}
                               for b in blocks if b["decision"]["review_concerns"]],
              "output": {"path": str((OUTPUT / "blocks.json").relative_to(ROOT)), "bytes": len(encoded), "sha256": digest(encoded)},
              "verification": {"exact_paragraph_run_object_coverage": True, "text_projection_unchanged": True,
                               "viewer_compared": False, "semantic_structure_verified": False}}
    return record, encoded


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    try:
        record, encoded = build_map()
        metadata = recovery.json_bytes(record)
        if args.write_record:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_bytes(metadata)
        else:
            require(json.loads(RECORD.read_bytes()) == record, "Block map differs from reviewed summary")
        OUTPUT.mkdir(parents=True, exist_ok=True)
        for name, data in [("blocks.json", encoded), ("provenance.json", metadata)]:
            temporary = OUTPUT / (name + ".tmp")
            temporary.write_bytes(data)
            temporary.replace(OUTPUT / name)
        print(f"Mapped {record['counts']['blocks']} blocks covering {record['counts']['paragraphs']} paragraphs and "
              f"{record['counts']['objects']} objects. Semantic/viewer review pending. Output: {OUTPUT.relative_to(ROOT)}")
    except (OSError, ValueError, KeyError, IndexError) as error:
        print(f"Block mapping failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
