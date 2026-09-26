"""Build a private CD-native 9401 issue slice with two independent article cases."""

import argparse
import hashlib
import html
import io
import json
from pathlib import Path
import shutil
import tempfile

from PIL import Image
from tools.build_cd2_pilot import CSS, digest, marked_html, parse, put
from tools.inventory_cd2_sources import PROBE, ROOT, TREE, RECORD
from tools.map_cd1_topic import require
from tools.map_cd2_candidates import SUMMARY as CANDIDATE_RECORD
from tools.recover_cd1_text import json_bytes

OUTPUT = ROOT / "build/cd2-issue-9401"
CASES = ("940116300", "940121800")


def checked(path, expected):
    data = path.read_bytes()
    require(len(data) == expected["bytes"] and digest(data) == expected["sha256"],
            f"Source changed: {path}")
    return data


def render_article(root, row, rtf, disc_files, probe_files):
    ref = row["reference"]
    span = row["rtf"]
    raw = rtf[span["byte_offset"]:span["byte_offset"]+span["byte_length"]]
    require(digest(raw) == span["sha256"], f"RTF topic changed: {ref}")
    paragraphs, issues, token_count = parse(raw, span["byte_offset"])
    media = [run["resource"] for p in paragraphs for run in p["runs"] if run["type"] == "media"]
    require(media == [item["name"] for item in row["media"]], f"Media order changed: {ref}")
    directory = f"articles/{ref}"
    title = row["index_title"]
    body = [f'<nav><a href="../../index.html">CD-native 9401 list</a></nav><h1>{html.escape(title)}</h1>',
            f'<p class="note">{ref} · {html.escape(row["index"])} · CD text · paper verification pending</p>',
            '<p class="gap">Dynamic fields and article boundaries require paper review.</p>',
            '<p><a href="article.txt">UTF-8 text</a> · <a href="blocks.json">Source blocks</a></p>']
    plain = []
    attachment_records = []
    for action in row["actions"]:
        for path in action["paths"]:
            data = checked(TREE / path, disc_files[path])
            target = f"attachments/{Path(path).name}"
            put(root, f"{directory}/{target}", data)
            attachment_records.append({"action": action["kind"], "source_path": path,
                                       "path": target, "sha256": digest(data)})
            body.append(f'<p><a href="{target}">{html.escape(Path(path).name)} · original {html.escape(action["kind"])}</a></p>')
            if action["kind"] == "ListView":
                text = data.decode("cp949")
                put(root, f"{directory}/listing.txt", text)
                body.append('<p><a href="listing.txt">Listing as UTF-8 text</a></p>')
                body.append(f'<details><summary>CD code listing</summary><pre>{html.escape(text)}</pre></details>')
    for name in sorted(set(media)):
        source = checked(PROBE / name, probe_files[name])
        put(root, f"{directory}/media/{name}", source)
        with Image.open(io.BytesIO(source)) as picture:
            pixels = picture.convert("RGBA")
            output = io.BytesIO()
            pixels.save(output, format="PNG")
            with Image.open(io.BytesIO(output.getvalue())) as restored:
                require(restored.convert("RGBA").tobytes() == pixels.tobytes(), f"PNG differs: {name}")
        put(root, f"{directory}/media/{name}.png", output.getvalue())
    for paragraph in paragraphs:
        rendered = []
        for run in paragraph["runs"]:
            if run["type"] == "media":
                name = run["resource"]
                plain.append(f"[image:{name}]")
                rendered.append(f'<a href="media/{name}"><img src="media/{name}.png" alt="{name}"></a>')
            else:
                text = run["text"]
                plain.append(text)
                rendered.append(marked_html(run))
        if paragraph["terminated"]:
            plain.append("\n")
        body.append("<p>"+"".join(rendered)+"</p>")
    text = "".join(plain)
    put(root, f"{directory}/article.txt", text)
    put(root, f"{directory}/blocks.json", json_bytes({"reference": ref, "source": span,
                                                       "paragraphs": paragraphs, "issues": issues,
                                                       "token_count": token_count,
                                                       "attachments": attachment_records}))
    put(root, f"{directory}/index.html", '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(title) + '</title><link rel="stylesheet" href="../../style.css"><body>' + "".join(body) + '</body></html>\n')
    return {"reference": ref, "title": title, "paragraphs": len(paragraphs), "issues": len(issues),
            "media_occurrences": len(media), "attachments": len(attachment_records),
            "text_sha256": digest(text.encode())}


def build(verify_existing=False):
    reviewed = json.loads(RECORD.read_bytes())
    source_raw = checked(ROOT / reviewed["private_detail"]["path"], reviewed["private_detail"])
    source = json.loads(source_raw)
    disc_files = {row["path"]: row for row in source["extracted"]["files"]}
    probe_files = {row["path"]: row for row in source["probe"]["files"]}
    queue_record = json.loads(CANDIDATE_RECORD.read_bytes())
    queue_raw = checked(ROOT / queue_record["private_detail"]["path"], queue_record["private_detail"])
    queue = json.loads(queue_raw)
    require(queue["source_inventory_sha256"] == digest(source_raw), "Queue and source differ")
    rtf = checked(PROBE / "MASO2.rtf", probe_files["MASO2.rtf"])
    rows = [row for row in queue["candidates"] if row["issue_group"] == "9401"]
    extra = [row for row in queue["additional_article_candidates"] if row["issue_group"] == "9401"]
    require(len(rows) == 91 and len(extra) == 2, "9401 candidate population changed")
    selected = {row["reference"]: row for row in rows if row["reference"] in CASES}
    require(set(selected) == set(CASES), "Pilot cases missing")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".cd2-issue-", dir=OUTPUT.parent) as temporary:
        stage = Path(temporary)
        articles = [render_article(stage, selected[ref], rtf, disc_files, probe_files) for ref in CASES]
        available = {row["reference"] for row in articles}
        all_rows = [{"id": row["reference"], "title": row["index_title"], "index": row["index"],
                     "topic_ordinal": row["topic_ordinal"],
                     "outcome": "success" if row["reference"] in available else "pending"} for row in rows]
        all_rows += [{"id": row["identity"], "title": row["title"], "index": "unindexed RTF title",
                      "topic_ordinal": row["topic_ordinal"], "outcome": "pending"} for row in extra]
        all_rows.sort(key=lambda row: row["topic_ordinal"])
        require(len(all_rows) == 93, "Incomplete issue list")
        listing = []
        for row in all_rows:
            label = html.escape(row["title"])
            link = f'<a href="articles/{row["id"]}/index.html">{label}</a>' if row["outcome"] == "success" else label
            listing.append(f'<li>{link} · {html.escape(row["id"])} · {html.escape(row["index"])} · {row["outcome"]}</li>')
        page = '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CD2 9401</title><link rel="stylesheet" href="style.css"><body><h1>CD2 native 9401 group</h1><p class="note">CD-native grouping; independent issue metadata and paper comparison pending.</p><p>93 candidate topics. Two readable pilot cases; remaining items await extraction.</p><ol>' + "".join(listing) + '</ol></body></html>\n'
        put(stage, "index.html", page)
        put(stage, "style.css", CSS + "\n")
        put(stage, "candidates.json", json_bytes({"schema_version": 1, "issue_group": "9401",
                                                  "article_list_basis": "CD-native indexes plus two titled unindexed RTF topics",
                                                  "articles": all_rows}))
        files = [{"path": p.relative_to(stage).as_posix(), "bytes": p.stat().st_size,
                  "sha256": digest(p.read_bytes())} for p in sorted(stage.rglob("*")) if p.is_file()]
        manifest = {"schema_version": 1, "issue_group": "9401", "candidates": len(all_rows),
                    "outcomes": {"success": 2, "pending": 91}, "articles": articles, "files": files}
        put(stage, "manifest.json", json_bytes(manifest))
        if OUTPUT.exists():
            if verify_existing:
                require(json.loads((OUTPUT / "manifest.json").read_bytes()) == manifest,
                        "Issue rebuild differs")
            shutil.rmtree(OUTPUT)
        shutil.copytree(stage, OUTPUT)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-existing", action="store_true")
    args = parser.parse_args()
    result = build(args.verify_existing)
    print(result["issue_group"], result["candidates"], result["outcomes"], result["articles"])


if __name__ == "__main__":
    main()
