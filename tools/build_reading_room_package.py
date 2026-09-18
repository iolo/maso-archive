"""Assemble and verify the private CD1 pilot package from reviewed step 8 outputs."""

import argparse
import json
from pathlib import Path
import sys
import tempfile
import xml.etree.ElementTree as ET

from jsonschema.exceptions import ValidationError

from maso_archive.reading_room import SCHEMA_PATH, require, validate_bundle, validate_manifest
from maso_archive.reading_room_package import checked_file, file_record, load_package
from tools import build_reading_room_example as example
from tools import render_cd1_markdown as markdown
from tools.map_cd1_topic import ROOT
from tools.recover_cd1_text import json_bytes
from tools.toc_snapshot import Snapshot

OUTPUT = ROOT / "build/reading-room-packages/cd1-8802065"
RECORD = ROOT / "data/catalog/reading-room-packages/cd1-8802065.json"
NOTE_UPDATES = {
    b"Images are unresolved placeholders. Structure and completeness await viewer comparison.":
        b"This Markdown preview retains source image placeholders; use the structured article and media index for images. Physical-magazine verification is pending.",
    b"Image resources unresolved; image mapping/conversion is pending.":
        b"Source image placeholders are retained here. The media index records available derivatives and deferred conversions.",
    b"Title object may be a navigation icon; role awaits viewer comparison.":
        b"Title object may be a navigation icon; its source-internal role remains unresolved.",
}


def package_preview(raw, locations):
    """Change generated notes only; copy every protected block-content byte."""
    output = bytearray()
    position = 0
    mapped = []

    def notes(segment):
        for old, new in NOTE_UPDATES.items():
            segment = segment.replace(old, new)
        return segment

    for location in locations:
        start = location["content_byte_offset"]
        end = start + location["content_byte_length"]
        require(position <= start <= end <= len(raw), "Invalid Markdown content range")
        output.extend(notes(raw[position:start]))
        mapped.append({"block_id": location["block_id"], "content_byte_offset": len(output),
                       "content_byte_length": end - start,
                       "sha256": file_record("unused", raw[start:end])["sha256"]})
        output.extend(raw[start:end])
        position = end
    output.extend(notes(raw[position:]))
    return bytes(output), mapped


def build_package():
    inputs = {}

    def read(path, expected=None):
        relative = Path(path).relative_to(ROOT).as_posix()
        snapshot = Snapshot(ROOT)
        source_root = snapshot.directory if relative in snapshot.files else ROOT
        if relative in snapshot.files:
            snapshot.read(relative)
        raw = checked_file(source_root, {"path": relative, **(expected or {})})
        inputs[relative] = file_record(relative, raw)
        return raw

    example_record = json.loads(read(example.RECORD))
    require(example_record["schema"]["sha256"] == file_record("schema", read(SCHEMA_PATH))["sha256"], "Contract schema changed")
    sources = {Path(r["path"]).name: read(ROOT / r["path"], {k: r[k] for k in ("bytes", "sha256")})
               for r in example_record["outputs"]}
    bundle = json.loads(sources["pilot.example.json"])
    evidence = json.loads(sources["provenance.json"])
    counts = validate_bundle(bundle)
    require(counts == example_record["counts"], "Contract example counts differ")
    for path, expected in evidence["inputs"].items():
        read(ROOT / path, expected)

    files, documents, previews = {}, [], []

    def add_document(document, path):
        raw = json_bytes(document)
        require(path not in files, "Duplicate output path")
        files[path] = raw
        documents.append({"kind": document["kind"], "id": document.get("id"), **file_record(path, raw)})

    add_document(bundle["catalog"], "catalog.json")
    add_document(bundle["media"], "media.json")
    for issue in bundle["issues"]:
        add_document(issue, f"issues/{issue['id']}.json")
    for article in bundle["articles"]:
        add_document(article, f"articles/{article['source']['disc_id']}/{article['source']['reference']}.json")
    available = {m["id"]: m["asset"] for m in bundle["media"]["items"] if m["asset"]}
    bindings = evidence["asset_bindings"]
    require(len(bindings) == len(available) and {b["media_id"] for b in bindings} == set(available), "Asset bindings differ")
    for binding in bindings:
        asset = available[binding["media_id"]]
        require(asset["path"] == binding["package_path"] and
                all(asset[k] == binding[k] for k in ("bytes", "sha256")), "Asset binding metadata differs")
        raw = read(ROOT / binding["source_path"], {k: binding[k] for k in ("bytes", "sha256")})
        require(asset["path"] not in files or files[asset["path"]] == raw, "Asset path collision")
        files[asset["path"]] = raw

    md_record = json.loads(read(markdown.RECORD))
    md_evidence = json.loads(read(ROOT / md_record["provenance"]["path"],
                                  {k: md_record["provenance"][k] for k in ("bytes", "sha256")}))
    for source in md_record["sources"]:
        require(source["sha256"] == evidence["inputs"][source["path"]]["sha256"], "Markdown and contract sources differ")
    require(md_evidence["outputs"] == md_record["outputs"], "Markdown output records differ")
    preview_locations = []
    article = bundle["articles"][0]
    require(len(bundle["articles"]) == 1 and article["id"] == example.ARTICLE_ID, "Expected the CD1 pilot")
    require([s["role"] for s in article["sections"]] == ["introduction", "body"], "Unexpected pilot sections")
    for section in article["sections"]:
        name = section["role"] + ".md"
        record = next(r for r in md_record["outputs"] if Path(r["path"]).name == name)
        raw = read(ROOT / record["path"], {k: record[k] for k in ("bytes", "sha256")})
        locations = [b for b in md_evidence["blocks"] if b["path"] == name]
        require([b["block_id"] for b in locations] == [b["id"] for b in section["blocks"]], "Preview block order differs")
        path = "previews/cd1/8802065/" + name
        files[path], mapped = package_preview(raw, locations)
        previews.append({"article_id": article["id"], "section_id": section["id"], **file_record(path, files[path])})
        preview_locations.extend({"path": path, **m} for m in mapped)
    manifest = {"schema_version": 1, "kind": "package_manifest", "documents": documents, "previews": previews}
    validate_manifest(manifest, bundle)
    files["manifest.json"] = json_bytes(manifest)
    package_files = [file_record(path, raw) for path, raw in sorted(files.items())]
    provenance = {"schema_version": 1, "article_id": example.ARTICLE_ID, "inputs": inputs,
                  "contract_evidence": evidence, "preview_content_ranges": preview_locations,
                  "preview_policy": "Original block content bytes; generated status notes updated; ordered image placeholders retained.",
                  "runtime_root": "content", "outputs": package_files,
                  "validation": {"schema_and_relationships": True, "file_hashes_checked": True,
                                 "assets_copied": True, "exact_preview_content": True, "physical_magazine_compared": False}}
    provenance_raw = json_bytes(provenance)
    record = {"schema_version": 1, "article_id": example.ARTICLE_ID, "package_root": str((OUTPUT / 'content').relative_to(ROOT)),
              "counts": {**counts, "files": len(files), "assets": len({m['path'] for m in available.values()}), "previews": len(previews)},
              "deferred_media": [m["id"] for m in bundle["media"]["items"] if m["status"] == "deferred"],
              "outputs": package_files, "provenance": file_record(str((OUTPUT / 'provenance.json').relative_to(ROOT)), provenance_raw),
              "validation": provenance["validation"]}
    return record, {**{"content/" + path: raw for path, raw in files.items()}, "provenance.json": provenance_raw}


def write_package(output, files):
    """Validate staging before replacing the prior generated directory."""
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    require(not output.is_symlink(), "Refusing symlink output")
    with tempfile.TemporaryDirectory(prefix=".package-stage-", dir=output.parent) as directory:
        stage = Path(directory) / "new"
        for relative, raw in files.items():
            require(relative == "provenance.json" or relative.startswith("content/"), "Invalid package output")
            require(all(p not in ("", ".", "..") for p in relative.split("/")), "Unsafe output path")
            path = stage / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        load_package(stage / "content")
        previous = Path(directory) / "previous"
        if output.exists():
            output.rename(previous)
        try:
            stage.rename(output)
        except OSError:
            if previous.exists():
                previous.rename(output)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    parser.add_argument("--verify", type=Path, help="Validate an existing content directory without extraction inputs")
    args = parser.parse_args()
    try:
        if args.verify:
            require(not args.write_record, "--verify cannot update the reviewed record")
            _, _, counts = load_package(args.verify)
        else:
            record, files = build_package()
            if not args.write_record:
                require(json.loads(RECORD.read_bytes()) == record, "Package differs from reviewed summary")
            write_package(OUTPUT, files)
            if args.write_record:
                RECORD.parent.mkdir(parents=True, exist_ok=True)
                RECORD.write_bytes(json_bytes(record))
            counts = record["counts"]
        print(f"Validated reading-room package: {counts}")
    except (OSError, ValueError, KeyError, StopIteration, ValidationError, ET.ParseError) as error:
        print(f"Reading-room package failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
