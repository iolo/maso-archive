"""Build a resumable private CD3 HTML/text/media reference from reviewed sources."""

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

from tools.build_cd2_pilot import CSS, marked_html, put
from tools.build_cd2_reference import convert_media, file_manifest, verify_package
from tools.cd3_text import parse_cd3
from tools.inventory_cd3_sources import PROBE, RECORD, ROOT, TREE
from tools.map_cd1_topic import require
from tools.map_cd3_candidates import SUMMARY as QUEUE_RECORD, checked, digest
from tools.recover_cd1_text import json_bytes

OUTPUT = ROOT / "build/cd3-reference"


def load():
    source_record = json.loads(RECORD.read_bytes())
    source_raw = checked(ROOT / source_record["private_detail"]["path"], source_record["private_detail"])
    source = json.loads(source_raw)
    queue_record = json.loads(QUEUE_RECORD.read_bytes())
    queue_raw = checked(ROOT / queue_record["private_detail"]["path"], queue_record["private_detail"])
    queue = json.loads(queue_raw)
    require(queue["source_inventory_sha256"] == digest(source_raw), "CD3 queue source differs")
    probe_files = {row["path"]: row for row in source["probe"]["main"]["files"]}
    disc_files = {row["path"]: row for row in source["extracted"]["files"]}
    rtf = checked(PROBE / "main/raw/MASO3.rtf", probe_files["MASO3.rtf"])
    return source, queue, probe_files, disc_files, rtf, digest(queue_raw)


def check_links(stage, allow_root=False):
    from tools.build_cd2_reference import Links
    for page in stage.rglob("*.html"):
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8"))
        for target in parser.targets:
            require(not target.startswith(("/", "http:", "https:", "file:")),
                    f"Nonportable link: {page} -> {target}")
            if allow_root and page == stage / "index.html" and target == "../../index.html":
                continue
            if allow_root and page.is_relative_to(stage / "articles") and target.startswith("../../../../"):
                continue
            resolved = (page.parent / target.split("#", 1)[0]).resolve()
            require(resolved.is_relative_to(stage.resolve()) and resolved.is_file(),
                    f"Broken link: {page.relative_to(stage)} -> {target}")


def build_group(group, queue, probe_files, disc_files, rtf, queue_hash,
                *, resume=False, verify_existing=False):
    topics = [t for t in queue["topics"] if t["role"] == "article_candidate" and t["group"] == group]
    by_id = {t["identity"]: t for t in queue["topics"]}
    require(topics, f"No CD3 candidates for group {group}")
    target = OUTPUT / "groups" / group
    if resume and target.exists():
        manifest = verify_package(target)
        require(manifest["source_queue_sha256"] == queue_hash and manifest["group"] == group,
                "Resumable group source differs")
        return manifest
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".cd3-{group}-", dir=target.parent) as temporary:
        stage = Path(temporary)
        media_records = {}
        rows = []

        def media_for(item):
            source_name = item["source_name"]
            if source_name is None:
                return None
            if source_name in media_records:
                return media_records[source_name]
            original = checked(PROBE / "main/raw" / source_name, probe_files[source_name])
            put(stage, f"media/{source_name}", original)
            preview, status, note = convert_media(original, source_name)
            if preview is not None:
                put(stage, f"media/{source_name}.png", preview)
            record = {"name": source_name, "status": status, "note": note,
                      "original_sha256": digest(original),
                      "preview_sha256": digest(preview) if preview is not None else None}
            media_records[source_name] = record
            return record

        for candidate in topics:
            identity, title = candidate["identity"], candidate["title"]
            span = candidate["rtf"]
            raw = rtf[span["byte_offset"]:span["byte_offset"] + span["byte_length"]]
            require(digest(raw) == span["sha256"], f"Changed CD3 topic: {identity}")
            directory = f"articles/{identity}"
            reasons = []
            if candidate["title_basis"] != "native_title_footnote":
                reasons.append("No native title footnote; display title is a visible lead phrase")
            if group == "undated":
                reasons.append("No unique CD-native issue label; group placement remains unresolved")
            elif not group.startswith("95"):
                reasons.append("CD-native date label lies outside the apparent 1995 disc range")
            body = [f'<nav><a href="../../index.html">{html.escape(group)} native list</a></nav>',
                    f'<h1>{html.escape(title)}</h1>',
                    f'<p class="note">{identity} · CD transcription · paper review pending · native labels: {html.escape(", ".join(candidate["native_issue_labels"]) or "none")}</p>',
                    '<p><a href="article.txt">UTF-8 text and inline code</a> · <a href="blocks.json">Source blocks</a></p>']
            attachments = []
            for index, action in enumerate(candidate["cab_actions"], 1):
                path = action["path"]
                if path is None:
                    reasons.append(f"CAB action target unavailable: {action['action']}")
                    body.append(f'<p class="gap">CAB unavailable: {html.escape(action["action"])}</p>')
                    continue
                original = checked(TREE / path, disc_files[path])
                name = f"attachments/{index:02d}-{Path(path).name}"
                put(stage, f"{directory}/{name}", original)
                attachments.append({"source_path": path, "path": name, "sha256": digest(original)})
                body.append(f'<p><a href="{name}">Original attachment: {html.escape(path)}</a></p>')
            try:
                paragraphs, issues, token_count = parse_cd3(raw, span["byte_offset"])
                occurrences = [run["resource"] for paragraph in paragraphs for run in paragraph["runs"]
                               if run["type"] == "media"]
                require(occurrences == [item["name"] for item in candidate["media"]],
                        f"Media order changed: {identity}")
                plain, rendered = [], []
                media_index = 0
                for paragraph in paragraphs:
                    content = []
                    for run in paragraph["runs"]:
                        if run["type"] == "media":
                            item = candidate["media"][media_index]
                            media_index += 1
                            name = item["name"]
                            figure = item["target_media"]
                            if item["target_alias"] and figure is None:
                                plain.append(f"[figure:{item['target_alias']} · target unresolved]")
                                reasons.append(f"Figure target unresolved: {item['target_alias']}")
                                content.append(f'<span class="gap">[figure:{html.escape(item["target_alias"])} · target unresolved]</span>')
                                continue
                            shown = figure or item
                            plain.append(f"[{ 'figure' if figure else 'image' }:{shown['name']}]")
                            media = media_for(shown)
                            if media is None:
                                reasons.append(f"Media source unavailable: {shown['name']}")
                                content.append(f'<span class="gap">[image:{html.escape(shown["name"])} · source unavailable]</span>')
                            elif media["preview_sha256"]:
                                source_name = media["name"]
                                content.append(f'<a href="../../media/{source_name}"><img src="../../media/{source_name}.png" alt="{html.escape(shown["name"])}"></a>')
                            else:
                                reasons.append(f"Media preview unavailable: {shown['name']}")
                                content.append(f'<a href="../../media/{media["name"]}">[image:{html.escape(shown["name"])} · preview unavailable]</a>')
                        else:
                            plain.append(run["text"])
                            content.append(marked_html(run))
                    if paragraph["terminated"]:
                        plain.append("\n")
                    rendered.append("<p>" + "".join(content) + "</p>")
                text = "".join(plain)
                put(stage, f"{directory}/article.txt", text)
                put(stage, f"{directory}/blocks.json", json_bytes({"identity": identity, "source": span,
                    "candidate": candidate, "paragraphs": paragraphs, "issues": issues,
                    "token_count": token_count, "attachments": attachments}))
                if issues:
                    reasons.append(f"{len(issues)} localized text uncertainties; see source blocks")
                figure_topics = {m["target_topic"] for m in candidate["media"] if m["target_topic"]}
                linked = []
                for link in candidate["links"]:
                    target_id = link["target_topic"]
                    if target_id is None or target_id in figure_topics:
                        continue
                    linked_target = by_id[target_id]
                    if linked_target["role"] == "article_candidate":
                        url = f"../../../../groups/{linked_target['group']}/articles/{target_id}/index.html"
                        label = linked_target["title"]
                    else:
                        url = f"../../../../supplements/{target_id}/index.html"
                        label = f"{linked_target['role'].replace('_', ' ')} {target_id}"
                    linked.append(f'<li><a href="{url}">{html.escape(label)}</a> · source offset {link["rtf_byte_offset"]}</li>')
                if linked:
                    body.append('<section><h2>Linked CD topics</h2><ul>' + "".join(linked) + '</ul></section>')
                body.extend(rendered)
                row = {"identity": identity, "title": title, "group": group,
                       "status": "partial" if reasons else "success", "reasons": sorted(set(reasons)),
                       "paragraphs": len(paragraphs), "text_characters": len(text),
                       "text_sha256": digest(text.encode()), "media_occurrences": len(occurrences),
                       "figure_links": sum(m["target_alias"] is not None for m in candidate["media"]),
                       "resolved_figures": sum(m["target_media"] is not None for m in candidate["media"]),
                       "attachments": attachments, "issue_records": len(issues),
                       "paper_review": "pending"}
            except (ValueError, IndexError, KeyError, OSError) as error:
                row = {"identity": identity, "title": title, "group": group,
                       "status": "failed", "reasons": sorted(set(reasons + [str(error)])),
                       "paragraphs": 0, "text_characters": 0, "text_sha256": None,
                       "media_occurrences": len(candidate["media"]), "attachments": attachments,
                       "figure_links": sum(m["target_alias"] is not None for m in candidate["media"]),
                       "resolved_figures": sum(m["target_media"] is not None for m in candidate["media"]),
                       "issue_records": 0, "paper_review": "pending"}
                put(stage, f"{directory}/article.txt", "")
                put(stage, f"{directory}/blocks.json", json_bytes({"identity": identity,
                    "source": span, "candidate": candidate, "error": str(error), "attachments": attachments}))
                body.append(f'<p class="gap">Text unavailable: {html.escape(str(error))}. Source remains inventoried.</p>')
            if row["reasons"]:
                body.insert(3, '<p class="gap">' + html.escape("; ".join(row["reasons"])) + '</p>')
            put(stage, f"{directory}/index.html", '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(title) + '</title><link rel="stylesheet" href="../../style.css"><body>' + "".join(body) + '</body></html>\n')
            rows.append(row)
        items = [f'<li><a href="articles/{row["identity"]}/index.html">{html.escape(row["title"])}</a> · {row["identity"]} · {row["status"]}</li>' for row in rows]
        put(stage, "index.html", '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CD3 ' + html.escape(group) + '</title><link rel="stylesheet" href="style.css"><body><nav><a href="../../index.html">All CD3 groups</a></nav><h1>CD3 native ' + html.escape(group) + ' group</h1><p class="note">CD-native labels; paper issue identities remain unverified.</p><ol>' + "".join(items) + '</ol></body></html>\n')
        put(stage, "style.css", CSS + "\n")
        put(stage, "articles.json", json_bytes({"schema_version": 1, "group": group, "articles": rows}))
        put(stage, "media.json", json_bytes({"schema_version": 1, "group": group,
                                            "resources": list(media_records.values())}))
        check_links(stage, allow_root=True)
        manifest = {"schema_version": 1, "group": group, "source_queue_sha256": queue_hash,
                    "candidates": len(rows), "outcomes": dict(sorted(Counter(r["status"] for r in rows).items())),
                    "media_resources": len(media_records),
                    "media_occurrences": sum(r["media_occurrences"] for r in rows),
                    "files": file_manifest(stage)}
        put(stage, "manifest.json", json_bytes(manifest))
        if target.exists():
            if verify_existing:
                require(verify_package(target) == manifest, f"Group {group} rebuild differs")
            shutil.rmtree(target)
        shutil.copytree(stage, target)
    return manifest


def finalize(queue, probe_files, rtf, queue_hash):
    target = OUTPUT
    groups = sorted({t["group"] for t in queue["topics"] if t["role"] == "article_candidate"})
    manifests = {group: verify_package(target / "groups" / group) for group in groups}
    require(all(m["source_queue_sha256"] == queue_hash for m in manifests.values()),
            "Group source queue differs")
    grouped = {t["identity"] for t in queue["topics"] if t["role"] == "article_candidate"}
    rows = []
    for group in groups:
        rows.extend(json.loads((target / "groups" / group / "articles.json").read_bytes())["articles"])
    require({r["identity"] for r in rows} == grouped and len(rows) == len(grouped),
            "CD3 article candidate coverage differs")
    source_media = []
    for name in sorted(p for p in probe_files if p.lower().endswith(".bmp")):
        original = checked(PROBE / "main/raw" / name, probe_files[name])
        put(target, f"media-sources/{name}", original)
        source_media.append({"name": name, "sha256": digest(original), "bytes": len(original)})
    put(target, "media-sources.json", json_bytes({"schema_version": 1, "resources": source_media}))
    supplements = []
    for topic in queue["topics"]:
        if topic["role"] == "article_candidate":
            continue
        span = topic["rtf"]
        raw = rtf[span["byte_offset"]:span["byte_offset"] + span["byte_length"]]
        require(digest(raw) == span["sha256"], "Supplement source changed")
        directory = f"supplements/{topic['identity']}"
        parts = ['<nav><a href="../index.html">All supplemental topics</a></nav>',
                 f'<h1>{html.escape(topic["role"].replace("_", " "))} {topic["identity"]}</h1>',
                 '<p class="note">CD-native auxiliary topic · paper relationship unverified</p>',
                 '<p><a href="text.txt">UTF-8 text</a> · <a href="blocks.json">Source blocks</a></p>']
        try:
            paragraphs, issues, token_count = parse_cd3(raw, span["byte_offset"])
            text_parts, rendered = [], []
            media_index = 0
            for paragraph in paragraphs:
                content = []
                for run in paragraph["runs"]:
                    if run["type"] == "media":
                        item = topic["media"][media_index]
                        media_index += 1
                        text_parts.append(f"[image:{item['name']}]")
                        if item["source_name"]:
                            content.append(f'<a href="../../media-sources/{item["source_name"]}">[image:{html.escape(item["name"])} · original]</a>')
                        else:
                            content.append(f'<span class="gap">[image:{html.escape(item["name"])} · source unavailable]</span>')
                    else:
                        text_parts.append(run["text"])
                        content.append(marked_html(run))
                if paragraph["terminated"]:
                    text_parts.append("\n")
                rendered.append("<p>" + "".join(content) + "</p>")
            require(media_index == len(topic["media"]), "Supplement media order differs")
            text = "".join(text_parts)
            put(target, f"{directory}/text.txt", text)
            put(target, f"{directory}/blocks.json", json_bytes({"identity": topic["identity"],
                "source": span, "topic": topic, "paragraphs": paragraphs, "issues": issues,
                "token_count": token_count}))
            parts.extend(rendered)
            status = "partial" if issues or any(not m["available"] for m in topic["media"]) else "success"
            issue_count = len(issues)
            text_hash = digest(text.encode())
        except (ValueError, IndexError, KeyError, OSError) as error:
            put(target, f"{directory}/text.txt", "")
            put(target, f"{directory}/blocks.json", json_bytes({"identity": topic["identity"],
                "source": span, "topic": topic, "error": str(error)}))
            parts.append(f'<p class="gap">Text unavailable: {html.escape(str(error))}</p>')
            status, issue_count, text_hash = "failed", 0, None
        put(target, f"{directory}/index.html", '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CD3 ' + topic["identity"] + '</title><link rel="stylesheet" href="../../style.css"><body>' + "".join(parts) + '</body></html>\n')
        supplements.append({"identity": topic["identity"], "role": topic["role"],
                            "context_aliases": topic["context_aliases"], "media": topic["media"],
                            "rtf": span, "status": status, "issue_records": issue_count,
                            "text_sha256": text_hash})
    put(target, "supplements.json", json_bytes({"schema_version": 1, "topics": supplements}))
    supplement_items = [f'<li><a href="{row["identity"]}/index.html">{row["identity"]}</a> · {html.escape(row["role"].replace("_", " "))} · {row["status"]}</li>'
                        for row in supplements]
    put(target, "supplements/index.html", '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CD3 supplemental topics</title><link rel="stylesheet" href="../style.css"><body><nav><a href="../index.html">CD3 reference</a></nav><h1>Supplemental topics</h1><p class="note">Native auxiliary topics, author bios, and document tail; print relationships remain unverified.</p><ol>' + "".join(supplement_items) + '</ol></body></html>\n')
    used = {m["source_name"] for t in queue["topics"] for m in t["media"] if m["source_name"]}
    unassigned = []
    for name in sorted(p for p in probe_files if p.lower().endswith(".bmp") and p not in used):
        original = checked(PROBE / "main/raw" / name, probe_files[name])
        put(target, f"unassigned-media/{name}", original)
        unassigned.append({"name": name, "sha256": digest(original), "bytes": len(original),
                           "status": "original_unassigned"})
    put(target, "unassigned-media.json", json_bytes({"schema_version": 1, "resources": unassigned}))
    list_items = [f'<li><a href="groups/{group}/index.html">{html.escape(group)}</a> · {manifests[group]["candidates"]} candidates</li>' for group in groups]
    put(target, "style.css", CSS + "\n")
    put(target, "index.html", '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CD3 private reference</title><link rel="stylesheet" href="style.css"><body><h1>CD3 private reference</h1><p class="note">CD transcription · paper review pending · native labels are not verified magazine issue identities.</p><ol>' + "".join(list_items) + '</ol><p><a href="catalog.json">Coverage catalog</a> · <a href="supplements/index.html">Supplemental topics</a> · <a href="media-sources.json">Original media</a> · <a href="unassigned-media.json">Unassigned media</a></p></body></html>\n')
    catalog = {"schema_version": 1, "disc_id": "cd3", "source_queue_sha256": queue_hash,
               "candidates": len(rows), "outcomes": dict(sorted(Counter(r["status"] for r in rows).items())),
               "groups": {group: {k: m[k] for k in ("candidates", "outcomes", "media_resources", "media_occurrences")}
                          for group, m in manifests.items()},
               "supplemental_topics": len(supplements),
               "supplement_outcomes": dict(sorted(Counter(t["status"] for t in supplements).items())),
               "source_media": len(source_media), "unassigned_media": len(unassigned),
               "articles": rows}
    put(target, "catalog.json", json_bytes(catalog))
    check_links(target)
    files = file_manifest(target)
    files = [f for f in files if f["path"] != "manifest.json"]
    put(target, "manifest.json", json_bytes({"schema_version": 1, "disc_id": "cd3",
        "source_queue_sha256": queue_hash, "counts": {"candidates": len(rows),
        "supplemental_topics": len(supplements), "unassigned_media": len(unassigned)}, "files": files}))
    return catalog


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--group")
    scope.add_argument("--all", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--verify-existing", action="store_true")
    args = parser.parse_args()
    try:
        source, queue, probe_files, disc_files, rtf, queue_hash = load()
        groups = sorted({t["group"] for t in queue["topics"] if t["role"] == "article_candidate"})
        selected = groups if args.all else [args.group]
        for group in selected:
            manifest = build_group(group, queue, probe_files, disc_files, rtf, queue_hash,
                                   resume=args.resume, verify_existing=args.verify_existing)
            print(group, manifest["candidates"], manifest["outcomes"], flush=True)
        if args.all:
            catalog = finalize(queue, probe_files, rtf, queue_hash)
            print("CD3 reference complete:", catalog["candidates"], catalog["outcomes"])
    except (OSError, ValueError, KeyError, IndexError) as error:
        print(f"CD3 reference build failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
