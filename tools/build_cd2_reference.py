"""Build resumable private CD2 issue batches and a complete coverage report."""

import argparse
from collections import Counter
import html
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from PIL import Image
from tools.build_cd2_pilot import CSS, digest, marked_html, parse, put
from tools.inventory_cd2_sources import PROBE, ROOT, TREE, RECORD
from tools.map_cd1_topic import require
from tools.map_cd2_candidates import SUMMARY as QUEUE_RECORD
from tools.recover_cd1_text import json_bytes

OUTPUT = ROOT / "build/cd2-reference"
ISSUES = tuple(f"94{month:02d}" for month in range(1, 13))


def checked(path, record):
    raw = path.read_bytes()
    require(len(raw) == record["bytes"] and digest(raw) == record["sha256"],
            f"Source fingerprint changed: {path}")
    return raw


def load():
    source_record = json.loads(RECORD.read_bytes())
    source_raw = checked(ROOT / source_record["private_detail"]["path"], source_record["private_detail"])
    source = json.loads(source_raw)
    queue_record = json.loads(QUEUE_RECORD.read_bytes())
    queue_raw = checked(ROOT / queue_record["private_detail"]["path"], queue_record["private_detail"])
    queue = json.loads(queue_raw)
    require(queue["source_inventory_sha256"] == digest(source_raw), "CD2 queue source differs")
    probe_files = {row["path"]: row for row in source["probe"]["files"]}
    disc_files = {row["path"]: row for row in source["extracted"]["files"]}
    rtf = checked(PROBE / "MASO2.rtf", probe_files["MASO2.rtf"])
    return queue, probe_files, disc_files, rtf


def file_manifest(stage):
    return [{"path": p.relative_to(stage).as_posix(), "bytes": p.stat().st_size,
             "sha256": digest(p.read_bytes())} for p in sorted(stage.rglob("*")) if p.is_file()]


def verify_package(path):
    manifest = json.loads((path / "manifest.json").read_bytes())
    listed = {row["path"] for row in manifest["files"]}
    actual = {p.relative_to(path).as_posix() for p in path.rglob("*") if p.is_file()} - {"manifest.json"}
    require(listed == actual, f"Package paths differ: {path}")
    for row in manifest["files"]:
        checked(path / row["path"], row)
    return manifest


def convert_media(source, name):
    """Return (PNG bytes, status, note); original bytes are always retained."""
    try:
        with Image.open(io.BytesIO(source)) as picture:
            picture.load()
            pixels = picture.convert("RGBA")
            stream = io.BytesIO()
            pixels.save(stream, format="PNG")
            with Image.open(io.BytesIO(stream.getvalue())) as restored:
                require(restored.convert("RGBA").tobytes() == pixels.tobytes(),
                        f"PNG pixels differ: {name}")
            return stream.getvalue(), "available", "PNG pixels match the decoded source bitmap"
    except (OSError, ValueError):
        pass
    if name.lower().endswith((".wmf", ".dib", ".bmp")):
        with tempfile.TemporaryDirectory(prefix="cd2-image-") as temporary:
            input_path, output_path = Path(temporary) / name, Path(temporary) / "render.png"
            input_path.write_bytes(source)
            try:
                result = subprocess.run(["convert", str(input_path), "-strip", "-define",
                                         "png:exclude-chunks=date,time", str(output_path)],
                                        capture_output=True, timeout=30)
                if result.returncode == 0 and output_path.is_file():
                    raw = output_path.read_bytes()
                    with Image.open(io.BytesIO(raw)) as picture:
                        picture.load()
                    return raw, "available_with_caveat", "ImageMagick fallback render; appearance needs paper review"
                diagnostic = result.stderr.decode(errors="replace")
                diagnostic = diagnostic.replace(str(input_path), "<source>").replace(str(output_path), "<preview>")
                return None, "deferred", diagnostic[:300]
            except (OSError, ValueError, subprocess.TimeoutExpired) as error:
                return None, "deferred", str(error)[:300]
    return None, "deferred", "No validated preview conversion; original available"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("href", "src") and value and not value.startswith("#"):
                self.targets.append(value)


def check_html_links(stage):
    for page in stage.rglob("*.html"):
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8"))
        for target in parser.targets:
            if page == stage / "index.html" and target == "../../index.html":
                # The root index is written after all independent issue batches.
                continue
            require(not target.startswith(("/", "http:", "https:", "file:")), "Nonportable HTML link")
            resolved = (page.parent / target.split("#", 1)[0]).resolve()
            require(resolved.is_relative_to(stage.resolve()) and resolved.is_file(),
                    f"Broken HTML link: {page.relative_to(stage)} -> {target}")


def build_issue(issue, queue, probe_files, disc_files, rtf, resume=False, verify_existing=False):
    require(issue in ISSUES, "Unknown CD-native group")
    target = OUTPUT / "issues" / issue
    if resume and target.exists():
        manifest = verify_package(target)
        require(manifest["issue_group"] == issue, "Wrong resumable issue package")
        return manifest
    candidates = [row for row in queue["candidates"] if row["issue_group"] == issue]
    candidates += [row for row in queue["additional_article_candidates"] if row["issue_group"] == issue]
    candidates.sort(key=lambda row: row["topic_ordinal"])
    require(len(candidates) == sum(1 for row in queue["candidates"] if row["issue_group"] == issue) +
            sum(1 for row in queue["additional_article_candidates"] if row["issue_group"] == issue),
            "Issue candidate set changed")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".cd2-{issue}-", dir=target.parent) as temporary:
        stage = Path(temporary)
        media_records = {}
        rows = []

        def media_for(name):
            if name in media_records:
                return media_records[name]
            require(re.fullmatch(r"[A-Za-z0-9_.]+", name) and name in probe_files,
                    f"Uninventoried media resource: {name}")
            source = checked(PROBE / name, probe_files[name])
            put(stage, f"media/{name}", source)
            preview, status, note = convert_media(source, name)
            if preview is not None:
                put(stage, f"media/{name}.png", preview)
            record = {"name": name, "status": status, "note": note,
                      "original_sha256": digest(source),
                      "preview_sha256": digest(preview) if preview is not None else None}
            media_records[name] = record
            return record

        for candidate in candidates:
            identity = candidate.get("reference") or candidate["identity"]
            title = candidate.get("index_title") or candidate["title"]
            span = candidate["rtf"]
            raw = rtf[span["byte_offset"]:span["byte_offset"]+span["byte_length"]]
            require(digest(raw) == span["sha256"], f"Changed RTF topic: {identity}")
            directory = f"articles/{identity}"
            body = [f'<nav><a href="../../index.html">{issue} CD-native list</a></nav>',
                    f'<h1>{html.escape(title)}</h1>',
                    f'<p class="note">{identity} · CD transcription · paper review pending</p>',
                    '<p><a href="article.txt">UTF-8 text</a> · <a href="blocks.json">Source blocks</a></p>']
            reasons = []
            if "reference" not in candidate:
                reasons.append("Titled RTF topic has no native index row; boundary/issue assignment is provisional")
            elif not candidate["title_agrees"]:
                reasons.append("CD index and RTF title differ; both are retained in the source record")
            attachments = []
            for action in candidate["actions"]:
                if not action["available"]:
                    reasons.append(f"{action['kind']}({action['argument']}) target unavailable")
                    body.append(f'<p class="gap">{html.escape(action["kind"])}({action["argument"]}) target unavailable</p>')
                for path in action["paths"]:
                    require(path in disc_files, f"Uninventoried attachment: {path}")
                    source = checked(TREE / path, disc_files[path])
                    link = f"attachments/{Path(path).name}"
                    put(stage, f"{directory}/{link}", source)
                    attachments.append({"kind": action["kind"], "source_path": path,
                                        "path": link, "sha256": digest(source)})
                    body.append(f'<p><a href="{link}">{html.escape(Path(path).name)} · original {action["kind"]}</a></p>')
                    if action["kind"] == "ListView":
                        try:
                            listing = source.decode("cp949")
                            listing_path = f"listings/{Path(path).stem}.txt"
                            put(stage, f"{directory}/{listing_path}", listing)
                            body.append(f'<p><a href="{listing_path}">UTF-8 code listing</a></p>')
                            body.append(f'<details><summary>Code listing</summary><pre>{html.escape(listing)}</pre></details>')
                        except UnicodeDecodeError:
                            reasons.append(f"Listing {path} has undecodable CP949 bytes; original retained")
            try:
                paragraphs, issues, token_count = parse(raw, span["byte_offset"])
                occurrences = [run["resource"] for p in paragraphs for run in p["runs"] if run["type"] == "media"]
                require(occurrences == [item["name"] for item in candidate["media"]],
                        f"Media order changed: {identity}")
                content = []
                plain = []
                for paragraph in paragraphs:
                    rendered = []
                    for run in paragraph["runs"]:
                        if run["type"] == "media":
                            name = run["resource"]
                            plain.append(f"[image:{name}]")
                            media = media_for(name)
                            if media["preview_sha256"]:
                                rendered.append(f'<a href="../../media/{name}"><img src="../../media/{name}.png" alt="{name}"></a>')
                            else:
                                rendered.append(f'<a href="../../media/{name}">[image:{name} · preview unavailable]</a>')
                                reasons.append(f"Media preview unavailable: {name}")
                        else:
                            text = run["text"]
                            plain.append(text)
                            rendered.append(marked_html(run))
                    if paragraph["terminated"]:
                        plain.append("\n")
                    content.append("<p>" + "".join(rendered) + "</p>")
                text = "".join(plain)
                put(stage, f"{directory}/article.txt", text)
                put(stage, f"{directory}/blocks.json", json_bytes({"identity": identity, "source": span,
                                                                    "candidate": candidate, "paragraphs": paragraphs,
                                                                    "issues": issues, "token_count": token_count,
                                                                    "attachments": attachments}))
                if issues:
                    reasons.append(f"{len(issues)} localized text/control uncertainties; see blocks.json")
                status = "partial" if reasons else "success"
                body.extend(content)
                row = {"id": identity, "title": title, "status": status, "issue_group": issue,
                       "index": candidate.get("index"), "topic_ordinal": candidate["topic_ordinal"],
                       "paragraphs": len(paragraphs), "text_sha256": digest(text.encode()),
                       "text_characters": len(text), "issues": len(issues), "media_occurrences": len(occurrences),
                       "resources": list(dict.fromkeys(occurrences)), "attachments": attachments,
                       "reasons": sorted(set(reasons)), "paper_review": "pending"}
            except (ValueError, IndexError, KeyError, OSError) as error:
                status = "failed"
                row = {"id": identity, "title": title, "status": status, "issue_group": issue,
                       "index": candidate.get("index"), "topic_ordinal": candidate["topic_ordinal"],
                       "paragraphs": 0, "text_sha256": None, "text_characters": 0, "issues": 0,
                       "media_occurrences": len(candidate["media"]),
                       "resources": [item["name"] for item in candidate["media"]],
                       "attachments": attachments, "reasons": sorted(set(reasons + [str(error)])),
                       "paper_review": "pending"}
                body.append(f'<p class="gap">Text unavailable: {html.escape(str(error))}. Source RTF remains inventoried.</p>')
                put(stage, f"{directory}/blocks.json", json_bytes({"identity": identity, "source": span,
                                                                    "candidate": candidate, "error": str(error),
                                                                    "attachments": attachments}))
                put(stage, f"{directory}/article.txt", "")
            if row["reasons"]:
                body.insert(3, '<p class="gap">' + html.escape("; ".join(row["reasons"])) + '</p>')
            put(stage, f"{directory}/index.html", '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(title) + '</title><link rel="stylesheet" href="../../style.css"><body>' + "".join(body) + '</body></html>\n')
            rows.append(row)
        list_items = []
        for row in rows:
            url = f"articles/{row['id']}/index.html"
            list_items.append(f'<li><a href="{url}">{html.escape(row["title"])}</a> · {row["id"]} · {row["status"]}</li>')
        issue_html = f'<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CD2 {issue}</title><link rel="stylesheet" href="style.css"><body><nav><a href="../../index.html">All CD2 groups</a></nav><h1>CD2 native {issue} group</h1><p class="note">CD-native grouping; independent issue metadata and paper review pending.</p><ol>' + "".join(list_items) + '</ol></body></html>\n'
        put(stage, "index.html", issue_html)
        put(stage, "style.css", CSS + "\n")
        put(stage, "articles.json", json_bytes({"schema_version": 1, "issue_group": issue, "articles": rows}))
        put(stage, "media.json", json_bytes({"schema_version": 1, "issue_group": issue,
                                              "resources": list(media_records.values())}))
        check_html_links(stage)
        manifest = {"schema_version": 1, "issue_group": issue, "candidates": len(rows),
                    "outcomes": dict(sorted(Counter(row["status"] for row in rows).items())),
                    "media_resources": len(media_records),
                    "media_occurrences": sum(row["media_occurrences"] for row in rows),
                    "files": file_manifest(stage)}
        put(stage, "manifest.json", json_bytes(manifest))
        if target.exists():
            if verify_existing:
                require(verify_package(target) == manifest, f"Issue {issue} rebuild differs")
            shutil.rmtree(target)
        shutil.copytree(stage, target)
    return manifest


def classify_supplements(queue, rtf, stage):
    records = []
    for topic in queue["unindexed_topics"]:
        if topic["title_footnotes"]:
            continue
        ordinal = topic["ordinal"]
        span = topic["rtf"]
        raw = rtf[span["byte_offset"]:span["byte_offset"]+span["byte_length"]]
        require(digest(raw) == span["sha256"], "Supplement source changed")
        aliases = topic["context_aliases"]
        if ordinal == 1388 and raw.endswith(b"}"):
            kind, text, issues = "document_tail", "", []
        else:
            paragraphs, issues, _ = parse(raw, span["byte_offset"])
            text = "".join("".join(r["text"] if r["type"] == "text" else f"[image:{r['resource']}]" for r in p["runs"]) +
                           ("\n" if p["terminated"] else "") for p in paragraphs)
            if aliases and aliases[0].startswith("MM"):
                kind = "multimedia_supplement"
            elif aliases and aliases[0].startswith("6HY"):
                kind = "navigation_link_list"
            else:
                kind = "untitled_topic"
        put(stage, f"supplements/{ordinal}.txt", text)
        records.append({"ordinal": ordinal, "kind": kind, "context_aliases": aliases,
                        "source": span, "text_sha256": digest(text.encode()), "issues": issues})
    require(len(records) == 58, "Untitled topic classification incomplete")
    put(stage, "supplements.json", json_bytes({"schema_version": 1, "topics": records}))
    return records


def export_unassigned_media(queue, probe_files, stage):
    referenced = {item["name"] for row in queue["candidates"] + queue["additional_article_candidates"]
                  for item in row["media"]}
    all_media = {name for name in probe_files if name.lower().endswith((".dib", ".wmf", ".bmp"))}
    require(referenced <= all_media, "Article media missing from decoder probe")
    records = []
    gallery = []
    for name in sorted(all_media - referenced):
        source = checked(PROBE / name, probe_files[name])
        put(stage, f"unassigned-media/{name}", source)
        preview, status, note = convert_media(source, name)
        if preview is not None:
            put(stage, f"unassigned-media/{name}.png", preview)
            picture = f'<img src="{name}.png" alt="{name}" loading="lazy">'
        else:
            picture = '[preview unavailable]'
        gallery.append(f'<li><a href="{name}">{picture} {name}</a> · {status}</li>')
        records.append({"name": name, "status": status, "note": note,
                        "original_sha256": digest(source),
                        "preview_sha256": digest(preview) if preview is not None else None})
    put(stage, "unassigned-media/index.html", '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CD2 unassigned media</title><link rel="stylesheet" href="../style.css"><body><nav><a href="../index.html">CD2 reference</a></nav><h1>Unassigned decoder media</h1><p>These files have no article RTF image marker. Their original source identity is retained; article placement is unknown.</p><ol>' + "".join(gallery) + '</ol></body></html>\n')
    put(stage, "unassigned-media.json", json_bytes({"schema_version": 1, "resources": records}))
    return records


def finalize(queue, rtf, probe_files):
    reports = []
    all_articles = []
    media_statuses = Counter()
    media_records_total = 0
    media_occurrences_total = 0
    for issue in ISSUES:
        package = OUTPUT / "issues" / issue
        manifest = verify_package(package)
        require(manifest["issue_group"] == issue, "Issue manifest group mismatch")
        articles = json.loads((package / "articles.json").read_bytes())["articles"]
        resources = json.loads((package / "media.json").read_bytes())["resources"]
        require(len(articles) == manifest["candidates"], "Issue article coverage mismatch")
        require(len(resources) == manifest["media_resources"], "Issue media coverage mismatch")
        require(sum(row["media_occurrences"] for row in articles) == manifest["media_occurrences"],
                "Issue media occurrence count differs")
        referenced = {name for row in articles for name in row["resources"]}
        require(referenced == {row["name"] for row in resources}, "Issue media associations differ")
        local_status = Counter(row["status"] for row in resources)
        media_statuses.update(local_status)
        media_records_total += len(resources)
        media_occurrences_total += manifest["media_occurrences"]
        all_articles.extend(articles)
        reports.append({"issue_group": issue, "candidates": manifest["candidates"],
                        "outcomes": manifest["outcomes"],
                        "media_resources": len(resources), "media_occurrences": manifest["media_occurrences"],
                        "media_statuses": dict(sorted(local_status.items())),
                        "manifest_sha256": digest((package / "manifest.json").read_bytes())})
    expected = {row["reference"] for row in queue["candidates"]} | {row["identity"] for row in queue["additional_article_candidates"]}
    require({row["id"] for row in all_articles} == expected and len(all_articles) == len(expected),
            "Full CD2 article population not accounted for")
    require(media_occurrences_total == sum(len(row["media"]) for row in queue["candidates"] +
                                           queue["additional_article_candidates"]),
            "CD2 media occurrence inventory differs")
    stage = OUTPUT
    supplements = classify_supplements(queue, rtf, stage)
    unassigned_media = export_unassigned_media(queue, probe_files, stage)
    outcomes = Counter(row["status"] for row in all_articles)
    coverage = {"schema_version": 1, "disc_id": "cd2", "scope": "private_cd2_reference",
                "candidate_basis": queue["candidate_basis"], "candidate_count": len(expected),
                "outcomes": dict(sorted(outcomes.items())), "issues": reports,
                "media_occurrences": media_occurrences_total, "media_resource_records": media_records_total,
                "media_statuses": dict(sorted(media_statuses.items())),
                "unassigned_media_resources": len(unassigned_media),
                "unassigned_media_statuses": dict(sorted(Counter(row["status"] for row in unassigned_media).items())),
                "articles": all_articles, "untitled_topics": len(supplements),
                "supplement_classes": dict(sorted(Counter(row["kind"] for row in supplements).items())),
                "paper_review": "pending for all CD-derived text and media"}
    put(stage, "coverage.json", json_bytes(coverage))
    groups = [f'<li><a href="issues/{row["issue_group"]}/index.html">{row["issue_group"]}</a> · {row["candidates"]} candidates · {html.escape(str(row["outcomes"]))}</li>' for row in reports]
    page = '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CD2 private reference</title><link rel="stylesheet" href="style.css"><body><h1>CD2 private reference</h1><p>CD-native groups and secondary transcription for paper review. Issue identities and text remain unverified against print.</p><p><a href="coverage.json">Coverage and remaining gaps</a> · <a href="supplements.json">Untitled topic classifications</a> · <a href="unassigned-media/index.html">Unassigned media</a></p><ol>' + "".join(groups) + '</ol></body></html>\n'
    put(stage, "index.html", page)
    put(stage, "style.css", CSS + "\n")
    check_html_links(stage)
    root_files = (["index.html", "style.css", "coverage.json", "supplements.json",
                   "unassigned-media.json", "unassigned-media/index.html"] +
                  [f"supplements/{row['ordinal']}.txt" for row in supplements] +
                  [f"unassigned-media/{row['name']}" for row in unassigned_media] +
                  [f"unassigned-media/{row['name']}.png" for row in unassigned_media if row["preview_sha256"]])
    manifest = {"schema_version": 1, "disc_id": "cd2", "issues": reports,
                "coverage_sha256": digest((stage / "coverage.json").read_bytes()),
                "files": [{"path": name, "bytes": (stage / name).stat().st_size,
                           "sha256": digest((stage / name).read_bytes())} for name in root_files]}
    put(stage, "manifest.json", json_bytes(manifest))
    return coverage, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--issue", choices=ISSUES)
    group.add_argument("--all", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--verify-existing", action="store_true")
    args = parser.parse_args()
    require(not (args.resume and args.verify_existing), "Choose resume or verify-existing")
    queue, probe_files, disc_files, rtf = load()
    if args.issue:
        manifest = build_issue(args.issue, queue, probe_files, disc_files, rtf,
                               resume=args.resume, verify_existing=args.verify_existing)
        print(args.issue, manifest["candidates"], manifest["outcomes"], manifest["media_resources"])
    else:
        for issue in ISSUES:
            manifest = build_issue(issue, queue, probe_files, disc_files, rtf,
                                   resume=args.resume, verify_existing=args.verify_existing)
            print(issue, manifest["candidates"], manifest["outcomes"], manifest["media_resources"], flush=True)
        coverage, _ = finalize(queue, rtf, probe_files)
        print("CD2 coverage", coverage["candidate_count"], coverage["outcomes"], coverage["supplement_classes"])


if __name__ == "__main__":
    main()
