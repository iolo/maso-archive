"""Render the reviewed pilot block map as a private, derived Markdown preview.

Run python3 -m tools.render_cd1_markdown. Preservation inputs remain unchanged.
"""

import argparse
import html
import json
import re
import string
import sys

from tools import map_cd1_blocks as mapper
from tools.recover_cd1_text import json_bytes, topic_text
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import ROOT, require

OUTPUT = ROOT / "build/cd1-markdown/8802065"
RECORD = ROOT / "data/catalog/markdown-previews/cd1-8802065.json"
BLOCKS = mapper.OUTPUT / "blocks.json"


def escape_text(text):
    """Escape source syntax before adding our own Markdown/inline HTML markup."""
    escaped = "".join(html.escape(c, quote=False) if c in "&<>" else
                      "\\" + c if c in string.punctuation else c for c in text)
    # Prevent indented code and Markdown's trimming/hard-break interpretation.
    return re.sub(r"^ +| +$", lambda m: "&#32;" * len(m[0]), escaped)


def inline(paragraph):
    pieces = []
    for run in paragraph["runs"]:
        require(run["kind"] in ("text", "object"), "Unsupported run kind")
        text = run["text"]
        require("\n" not in text and "\r" not in text, "Unexpected inline line break")
        value = escape_text(text)
        # HTML avoids emphasis delimiter ambiguity at Korean/Latin font boundaries
        # and preserves underline, which has no standard Markdown delimiter.
        if run["format"].get("ul"):
            value = f"<u>{value}</u>"
        if run["format"].get("b"):
            value = f"<strong>{value}</strong>"
        pieces.append(value)
    return "".join(pieces)


def fenced(text):
    require(text.endswith("\n"), "Code projection needs its source paragraph terminator")
    fence = "`" * max(3, 1 + max((len(m[0]) for m in re.finditer(r"`+", text)), default=0))
    return fence + "\n" + text + fence + "\n"


def anchor(block_id):
    require(re.fullmatch(r"cd1-[A-Za-z0-9][A-Za-z0-9_.-]*:T\d+:P\d+-\d+", block_id) is not None, "Unsafe block ID")
    return block_id.replace(":", "-")


def render(article, block_map):
    reference = article["cd_reference"]
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", reference) is not None, "Unsafe article reference")
    mapper.validate_map(article, block_map)
    for topic in article["topics"]:
        for paragraph in topic["paragraphs"]:
            require(paragraph["text"] == "".join(r["text"] for r in paragraph["runs"]),
                    "Paragraph/run text mismatch")
    links = {}
    for relation in block_map["relationships"]:
        require(relation["kind"] == "caption_for", "Unsupported relationship")
        links.setdefault(relation["from_block"], []).append(relation["to_block"])
    files, locations = {}, []
    for topic in article["topics"]:
        roles = {"linked_introduction": "introduction", "reference_target_body": "body"}
        require(topic["role"] in roles, "Unexpected topic role")
        filename = roles[topic["role"]] + ".md"
        require(filename not in files, "Duplicate topic output")
        data = bytearray((
            f"> Private reading preview — CD1 {reference}, {topic['role']} (topic {topic['ordinal']}).\n>\n"
            "> Images are unresolved placeholders. Structure and completeness await viewer comparison.\n>\n"
            "> Layout, fonts, and blank-paragraph spacing are not reproduced; preservation data remains separate.\n\n"
        ).encode("utf-8"))
        for block in block_map["blocks"]:
            if block["topic_ordinal"] != topic["ordinal"]:
                continue
            paragraphs = [topic["paragraphs"][m["paragraph_ordinal"] - 1] for m in block["members"]]
            projection = topic_text({"paragraphs": paragraphs})
            kind = block["kind"]
            if kind == "code":
                content = fenced(projection)
            elif kind == "spacing":
                content = projection
            else:
                require(kind in ("title", "heading", "paragraph", "caption", "figure", "table",
                                 "unresolved", "issue_label", "byline"), "Unknown block kind")
                require(len(paragraphs) == 1 or kind == "figure",
                        "Unexpected multi-paragraph prose block")
                prefix = "# " if kind == "title" else ""
                if kind == "heading":
                    require(block["heading_level"] in (1, 2, 3), "Invalid heading level")
                    prefix = "#" * (block["heading_level"] + 1) + " "
                content = prefix + "\n\n".join(inline(p) for p in paragraphs) + "\n"
            start = len(data)
            data.extend(f'<a id="{anchor(block["id"])}"></a>\n\n'.encode("utf-8"))
            if kind == "spacing":
                data.extend(f'<!-- Source spacing: {len(paragraphs)} paragraph(s); exact layout in recovery. -->\n'.encode("utf-8"))
            content_start = len(data)
            encoded = content.encode("utf-8")
            data.extend(encoded)
            data.extend(b"\n")
            notes = []
            if block.get("representation") == "mixed_text_objects":
                notes.append("Mixed text/object example: placeholders inside the code fence preserve object order; images cannot render there.")
            if block["object_refs"]:
                notes.append("Image resources unresolved; image mapping/conversion is pending.")
            if kind == "unresolved":
                notes.append("Source paragraph structure awaits review; text, formatting, and object order are retained in preservation data."
                             if "semantic_review_pending" in block["decision"]["review_concerns"] else
                             "Unresolved attachment: this object has not been assigned to either neighboring figure/example.")
            if "navigation_icon_role_pending_viewer" in block["decision"]["review_concerns"]:
                notes.append("Title object may be a navigation icon; role awaits viewer comparison.")
            if "table_cells_not_reconstructed" in block["decision"]["review_concerns"]:
                notes.append("Image-backed table/layout: cell structure has not been reconstructed.")
            if "suspect_decoded_text" in block["decision"]["review_concerns"]:
                notes.append("A source string in this block needs physical-magazine review; its decoded characters are preserved without correction.")
            for note in notes:
                data.extend(f"> Preview note: {note}\n\n".encode("utf-8"))
            for target in links.get(block["id"], []):
                data.extend(f"[View captioned content](#{anchor(target)})\n\n".encode("utf-8"))
            locations.append({"block_id": block["id"], "kind": kind, "path": filename,
                              "byte_offset": start, "byte_length": len(data) - start,
                              "content_byte_offset": content_start, "content_byte_length": len(encoded),
                              "source_content_sha256": block["content_sha256"],
                              "object_refs": block["object_refs"]})
        files[filename] = bytes(data)
    require([loc["block_id"] for loc in locations] == [b["id"] for b in block_map["blocks"]],
            "Export block coverage/order mismatch")
    return files, locations


def build_preview():
    article_raw = mapper.SOURCE.read_bytes()
    require(digest(article_raw) == mapper.SOURCE_SHA256, "Changed structured recovery")
    map_record = json.loads(mapper.RECORD.read_bytes())
    map_raw = BLOCKS.read_bytes()
    require(digest(map_raw) == map_record["output"]["sha256"], "Changed block map; re-review decisions")
    block_map = json.loads(map_raw)
    require(block_map["source"] == map_record["source"] and
            block_map["source"]["sha256"] == digest(article_raw), "Block map source mismatch")
    files, locations = render(json.loads(article_raw), block_map)
    provenance = {"schema_version": 1, "cd_reference": "8802065",
                  "sources": [{"path": str(path.relative_to(ROOT)), "sha256": digest(raw)}
                              for path, raw in ((mapper.SOURCE, article_raw), (BLOCKS, map_raw))],
                  "policy": {"format": "Markdown with inline HTML anchors/strong/underline",
                             "heading_levels": "title H1; source levels 1/2/3 map to H2/H3/H4",
                             "code": "verbatim source projection; collision-safe unlabeled fences",
                             "spacing": "explicit source-spacing comments; original layout not reproduced",
                             "images": "ordered source placeholders; no converted assets yet"},
                  "counts": {**map_record["counts"], "markdown_files": len(files)},
                  "outputs": [{"path": str((OUTPUT / name).relative_to(ROOT)), "bytes": len(raw), "sha256": digest(raw)}
                              for name, raw in files.items()],
                  "verification": {"source_hashes_checked": True, "exact_block_coverage": True,
                                   "viewer_compared": False, "semantic_structure_verified": False},
                  "blocks": locations}
    files["provenance.json"] = json_bytes(provenance)
    record = {k: v for k, v in provenance.items() if k != "blocks"}
    record["provenance"] = {"path": str((OUTPUT / "provenance.json").relative_to(ROOT)),
                            "bytes": len(files["provenance.json"]), "sha256": digest(files["provenance.json"])}
    return record, files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    try:
        record, files = build_preview()
        if args.write_record:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_bytes(json_bytes(record))
        else:
            require(json.loads(RECORD.read_bytes()) == record, "Preview differs from reviewed summary")
        OUTPUT.mkdir(parents=True, exist_ok=True)
        for name, data in files.items():
            temporary = OUTPUT / (name + ".tmp")
            temporary.write_bytes(data)
            temporary.replace(OUTPUT / name)
        print(f"Rendered {record['counts']['blocks']} blocks into two private Markdown files. "
              f"Images/viewer comparison pending. Output: {OUTPUT.relative_to(ROOT)}")
    except (OSError, ValueError, KeyError, IndexError) as error:
        print(f"Markdown preview failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
