"""Read and verify a v1 static package without its extraction environment."""

import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from jsonschema import Draft202012Validator

from .reading_room import SCHEMA_PATH, require, validate_bundle, validate_manifest


def file_record(path, raw):
    return {"path": path, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def checked_file(root, record):
    """Read only regular files below the package root, never symlink targets."""
    relative = record["path"]
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*(/[A-Za-z0-9][A-Za-z0-9._-]*)*", relative),
            f"Unsafe package path: {relative!r}")
    path = Path(root)
    require(path.is_dir() and not path.is_symlink(), "Package root must be a real directory")
    for segment in relative.split("/"):
        path = path / segment
        require(not path.is_symlink(), f"Symlink in package: {relative}")
    require(path.is_file(), f"Missing package file: {relative}")
    raw = path.read_bytes()
    actual = file_record(relative, raw)
    for key in ("bytes", "sha256"):
        require(key not in record or actual[key] == record[key], f"Package {key} mismatch: {relative}")
    return raw


def check_svg(raw):
    """The copied pilot SVGs must not need external image/style documents."""
    require(b"<!DOCTYPE" not in raw.upper() and b"<?xml-stylesheet" not in raw.lower(),
            "SVG has an external-document mechanism")
    root = ET.fromstring(raw)
    require(root.tag == "{http://www.w3.org/2000/svg}svg", "Invalid SVG root")
    identifiers = {e.attrib["id"] for e in root.iter() if "id" in e.attrib}
    for element in root.iter():
        require(element.tag.rsplit("}", 1)[-1] not in ("script", "foreignObject"), "Unsupported active SVG element")
        for key, value in element.attrib.items():
            require(not key.lower().startswith("on"), "Unsupported SVG event handler")
            if key.rsplit("}", 1)[-1] == "href":
                require(value.startswith("#") and value[1:] in identifiers, "External/dangling SVG reference")
        styles = list(element.attrib.values()) + [element.text or ""]
        for style in styles:
            require("@import" not in style.lower(), "External SVG stylesheet")
            for target in re.findall(r"url\((.*?)\)", style, re.IGNORECASE):
                target = target.strip(" \t\r\n\"'")
                require(target.startswith("#") and target[1:] in identifiers, "External/dangling SVG URL")


def load_package(root):
    """Check schema, file hashes, references, and exact on-disk inventory."""
    root = Path(root)
    schema = json.loads(SCHEMA_PATH.read_bytes())
    manifest = json.loads(checked_file(root, {"path": "manifest.json"}))
    Draft202012Validator({**schema, "$ref": "#/$defs/package_manifest"}).validate(manifest)
    groups = {kind: [] for kind in ("catalog", "media_index", "issue", "article")}
    expected = {"manifest.json"}
    for record in manifest["documents"]:
        document = json.loads(checked_file(root, record))
        Draft202012Validator({**schema, "$ref": "#/$defs/" + record["kind"]}).validate(document)
        require(document.get("id") == record["id"], "Manifest/document identity mismatch")
        groups[record["kind"]].append(document)
        expected.add(record["path"])
    require(len(groups["catalog"]) == len(groups["media_index"]) == 1, "Package needs exactly one catalog and media index")
    bundle = {"schema_version": 1, "kind": "contract_example", "catalog": groups["catalog"][0],
              "issues": groups["issue"], "articles": groups["article"], "media": groups["media_index"][0]}
    validate_manifest(manifest, bundle)
    for item in bundle["media"]["items"]:
        if item["asset"] is not None:
            raw = checked_file(root, item["asset"])
            if item["asset"]["mime_type"] == "image/svg+xml":
                check_svg(raw)
            expected.add(item["asset"]["path"])
    for preview in manifest["previews"]:
        text = checked_file(root, preview).decode("utf-8")
        anchors = re.findall(r'^<a id="([^"]+)"></a>$', text, re.MULTILINE)
        require(len(anchors) == len(set(anchors)), "Duplicate preview anchor")
        for target in re.findall(r"^\[View captioned content\]\(#([^)]+)\)$", text, re.MULTILINE):
            require(target in anchors, "Dangling preview caption link")
        expected.add(preview["path"])
    actual = set()
    for path in root.rglob("*"):
        require(not path.is_symlink(), "Package contains a symlink")
        if not path.is_dir():
            require(path.is_file(), "Package contains a non-regular file")
            actual.add(path.relative_to(root).as_posix())
    require(actual == expected, f"Package inventory differs: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")
    return bundle, manifest, {**validate_bundle(bundle), "files": len(actual),
                              "assets": len({m['asset']['path'] for m in bundle['media']['items'] if m['asset']}),
                              "previews": len(manifest["previews"])}
