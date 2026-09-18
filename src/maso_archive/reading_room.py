"""Reading-room v1 shape and relationship validation; no source decoding or UI."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas/reading-room-v1.schema.json"
ISSUE_FIELDS = ("id", "year", "month", "label", "toc_status", "cover_media_id")
ARTICLE_FIELDS = ("id", "issue_id", "title", "byline", "pages", "content_status")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def catalog_for(issues, articles):
    """Small, deterministic metadata index; source order is never page-sorted."""
    return {"schema_version": 1, "kind": "catalog",
            "issues": [{k: row[k] for k in ISSUE_FIELDS} for row in issues],
            "articles": [{k: row[k] for k in ARTICLE_FIELDS} for row in articles],
            "search_fields": ["title", "byline", "issue_id"]}


def project_section(section, media):
    """Preservation check only: recreate source placeholder text, including LFs."""
    return "".join("".join(r["text"] if r["type"] == "text" else
                           f"[object:{media[r['media_id']]['source']['resource']}]"
                           for r in p["runs"]) + "\n"
                   for b in section["blocks"] for p in b["paragraphs"])


def validate_bundle(bundle):
    schema = json.loads(SCHEMA_PATH.read_bytes())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(bundle)
    identities = set()

    def register(identifier):
        require(identifier not in identities, f"Duplicate identity: {identifier}")
        identities.add(identifier)

    def indexed(rows):
        for row in rows:
            register(row["id"])
        return {row["id"]: row for row in rows}

    def pages(value):
        start, end = value["start"], value["end"]
        require(end is None or (start is not None and start <= end), "Invalid page range")

    issues = indexed(bundle["issues"])
    articles = indexed(bundle["articles"])
    media = indexed(bundle["media"]["items"])
    require(bundle["catalog"] == catalog_for(bundle["issues"], bundle["articles"]), "Catalog projection differs")
    paths = {}
    for item in media.values():
        if item["status"] == "deferred":
            require(item["problem_ids"], "Deferred media needs a tracked issue ID")
        if item["asset"]:
            asset = item["asset"]
            extension = {"image/png": (".png",), "image/svg+xml": (".svg",),
                         "image/jpeg": (".jpg", ".jpeg"), "image/webp": (".webp",)}[asset["mime_type"]]
            require(asset["path"].endswith(extension), "Asset MIME/extension mismatch")
            require(asset["path"] not in paths or paths[asset["path"]] == asset, "Conflicting asset path")
            paths[asset["path"]] = asset
    toc = {}
    article_links = {identifier: [] for identifier in articles}
    for issue in issues.values():
        require(issue["id"] == f"maso-{issue['year']:04d}-{issue['month']:02d}", "Issue date/identity mismatch")
        if issue["toc_status"] == "missing":
            require(not issue["toc"], "Missing TOC contains entries")
        if issue["toc_status"] == "available":
            require(issue["toc"], "Available TOC is empty")
        if issue["cover_media_id"] is not None:
            require(issue["cover_media_id"] in media, "Dangling cover media")
        ancestors = []
        for entry in issue["toc"]:
            register(entry["id"])
            require(entry["id"].startswith(issue["id"] + "-toc-"), "TOC identity belongs to another issue")
            parent = entry["parent_id"]
            if parent is None:
                ancestors = []
            else:
                require(parent in ancestors, "TOC is not in parent-before-child tree order")
                ancestors = ancestors[:ancestors.index(parent) + 1]
            ancestors.append(entry["id"])
            pages(entry["pages"])
            toc[entry["id"]] = (issue["id"], entry)
            for article_id in entry["article_ids"]:
                require(article_id in articles, "Dangling TOC article link")
                require(articles[article_id]["issue_id"] == issue["id"], "Cross-issue TOC article link")
                article_links[article_id].append(entry["id"])
    native_refs = set()
    for article in articles.values():
        require(article["issue_id"] is None or article["issue_id"] in issues, "Unknown article issue")
        require(article["toc_entry_ids"] == article_links[article["id"]], "TOC/article backlinks differ")
        native = (article["source"]["disc_id"], article["source"]["reference"])
        require(native not in native_refs, "Duplicate native article reference")
        native_refs.add(native)
        pages(article["pages"])
        compared = article["print_verification"]["pages_compared"]
        require(compared == sorted(compared), "Print evidence pages must be ordered")
        article_blocks = {}
        for section in article["sections"]:
            register(section["id"])
            headings = []
            for block in section["blocks"]:
                register(block["id"])
                article_blocks[block["id"]] = block
                if block["type"] == "heading":
                    level = block["heading_level"]
                    while headings and headings[-1][0] >= level:
                        headings.pop()
                    require(level == 1 or (headings and headings[-1][0] == level - 1), "Skipped heading level")
                require(block["parent_heading_id"] == (headings[-1][1] if headings else None), "Invalid heading parent/order")
                if block["type"] == "heading":
                    headings.append((block["heading_level"], block["id"]))
                media_count = 0
                for paragraph in block["paragraphs"]:
                    register(paragraph["id"])
                    for run in paragraph["runs"]:
                        if run["type"] == "media":
                            register(run["occurrence_id"])
                            require(run["media_id"] in media, "Dangling inline media")
                            media_count += 1
                        else:
                            require("\r" not in run["text"] and "\n" not in run["text"], "Inline text contains a paragraph break")
                            require(block["type"] != "spacing" or not run["text"].strip(), "Spacing block contains visible text")
                require(block["type"] != "spacing" or media_count == 0, "Spacing block contains media")
                if block["type"] in ("figure", "table"):
                    require(media_count > 0, "Image-backed figure/table has no media")
                if block["type"] == "unresolved":
                    require(block["interpretation"] == "unresolved", "Unresolved block needs explicit interpretation status")
        captions = set()
        for relation in article["relationships"]:
            source, target = relation["from_block"], relation["to_block"]
            require(source in article_blocks and target in article_blocks, "Dangling caption relationship")
            require(article_blocks[source]["type"] == "caption", "Caption relationship source is not a caption")
            require(article_blocks[target]["type"] in ("code", "figure", "table", "unresolved"), "Invalid caption target")
            captions.add(source)
        require(captions == {b["id"] for b in article_blocks.values() if b["type"] == "caption"}, "Unlinked caption block")
    return {"issues": len(issues), "toc_entries": len(toc), "articles": len(articles), "media": len(media),
            "sections": sum(len(a["sections"]) for a in articles.values()),
            "blocks": sum(len(s["blocks"]) for a in articles.values() for s in a["sections"]),
            "paragraphs": sum(len(b["paragraphs"]) for a in articles.values() for s in a["sections"] for b in s["blocks"]),
            "media_occurrences": sum(r["type"] == "media" for a in articles.values() for s in a["sections"] for b in s["blocks"] for p in b["paragraphs"] for r in p["runs"])}


def validate_manifest(manifest, bundle):
    """Validate the transport index; step 9 additionally checks actual file bytes."""
    schema = json.loads(SCHEMA_PATH.read_bytes())
    Draft202012Validator({**schema, "$ref": "#/$defs/package_manifest"}).validate(manifest)
    validate_bundle(bundle)
    expected = {("catalog", None), ("media_index", None)}
    expected.update(("issue", i["id"]) for i in bundle["issues"])
    expected.update(("article", a["id"]) for a in bundle["articles"])
    documents = [(f["kind"], f["id"]) for f in manifest["documents"]]
    require(len(documents) == len(set(documents)) and set(documents) == expected, "Manifest document inventory differs")
    paths = set()
    for document in manifest["documents"]:
        path, kind = document["path"], document["kind"]
        if kind in ("catalog", "media_index"):
            require(path == ("catalog.json" if kind == "catalog" else "media.json"), "Invalid index path")
        else:
            require(path.startswith("issues/" if kind == "issue" else "articles/") and path.endswith(".json"), "Invalid document path")
        require(path not in paths, "Duplicate package path")
        paths.add(path)
    sections = {(a["id"], s["id"]) for a in bundle["articles"] for s in a["sections"]}
    previews = set()
    for preview in manifest["previews"]:
        key = (preview["article_id"], preview["section_id"])
        require(key in sections and key not in previews, "Invalid/duplicate preview section")
        previews.add(key)
        require(preview["path"].startswith("previews/") and preview["path"].endswith(".md"), "Invalid preview path")
        require(preview["path"] not in paths, "Duplicate package path")
        paths.add(preview["path"])
