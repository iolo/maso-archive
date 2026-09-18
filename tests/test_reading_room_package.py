"""Package validation from real files, plus private pilot preservation checks."""

from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image
from jsonschema.exceptions import ValidationError

from maso_archive.reading_room import project_section
from maso_archive.reading_room_package import check_svg, file_record, load_package
from tools import build_reading_room_package as builder
from tools import build_reading_room_example as example
from tools import render_cd1_markdown as markdown
from tools.recover_cd1_text import json_bytes

ROOT = Path(__file__).resolve().parents[1]


def synthetic_files():
    bundle = json.loads((ROOT / "examples/reading-room-v1.json").read_bytes())
    buffer = io.BytesIO()
    Image.new("RGB", (32, 25), "white").save(buffer, format="PNG")
    asset = bundle["media"]["items"][0]["asset"]
    asset.update(file_record(asset["path"], buffer.getvalue()))
    files = {"content/" + asset["path"]: buffer.getvalue()}
    documents = []
    rows = [("catalog.json", bundle["catalog"]), ("media.json", bundle["media"])]
    rows += [(f"issues/{i}.json", row) for i, row in enumerate(bundle["issues"])]
    rows += [(f"articles/{i}.json", row) for i, row in enumerate(bundle["articles"])]
    for path, row in rows:
        raw = json_bytes(row)
        files["content/" + path] = raw
        documents.append({"kind": row["kind"], "id": row.get("id"), **file_record(path, raw)})
    preview = b'<a id="target"></a>\n\n[View captioned content](#target)\n'
    files["content/previews/example.md"] = preview
    manifest = {"schema_version": 1, "kind": "package_manifest", "documents": documents,
                "previews": [{"article_id": bundle["articles"][0]["id"],
                              "section_id": bundle["articles"][0]["sections"][0]["id"],
                              **file_record("previews/example.md", preview)}]}
    files["content/manifest.json"] = json_bytes(manifest)
    files["provenance.json"] = b"{}\n"
    return bundle, files


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "package"
        self.bundle, self.files = synthetic_files()
        builder.write_package(self.output, self.files)
        self.root = self.output / "content"

    def manifest(self):
        return json.loads((self.root / "manifest.json").read_bytes())

    def save_manifest(self, manifest):
        (self.root / "manifest.json").write_bytes(json_bytes(manifest))

    def test_standalone_load_matches_logical_bundle_and_all_file_hashes(self):
        bundle, manifest, counts = load_package(self.root)
        self.assertEqual(bundle, self.bundle)
        self.assertEqual((counts["files"], counts["assets"], counts["previews"]), (8, 1, 1))
        for record in manifest["documents"] + manifest["previews"]:
            actual = file_record(record["path"], (self.root / record["path"]).read_bytes())
            self.assertEqual((record["bytes"], record["sha256"]), (actual["bytes"], actual["sha256"]))

    def test_missing_and_corrupt_assets_and_previews_fail(self):
        for path in ("media/cd1/sample.bmp.png", "previews/example.md", "articles/0.json"):
            for missing in (False, True):
                with self.subTest(path=path, missing=missing):
                    builder.write_package(self.output, self.files)
                    target = self.root / path
                    if missing:
                        target.unlink()
                    else:
                        target.write_bytes(target.read_bytes() + b"changed")
                    with self.assertRaisesRegex(ValueError, "Missing package file|mismatch"):
                        load_package(self.root)

    def test_manifest_cannot_relabel_a_document_or_escape_package(self):
        original = self.manifest()
        for path in ("../outside.json", "/tmp/outside.json", "articles/%2e%2e/a.json"):
            manifest = deepcopy(original)
            manifest["documents"][0]["path"] = path
            self.save_manifest(manifest)
            with self.assertRaises((ValidationError, ValueError)):
                load_package(self.root)
        original["documents"][-1]["id"] = "wrong:identity"
        self.save_manifest(original)
        with self.assertRaisesRegex(ValueError, "identity mismatch"):
            load_package(self.root)

    def test_extra_files_and_symlink_assets_are_rejected(self):
        extra = self.root / "media/cd1/broken.wmf.svg"
        extra.write_text("suspect derivative")
        with self.assertRaisesRegex(ValueError, "inventory differs"):
            load_package(self.root)
        extra.unlink()
        target = self.root / "media/cd1/sample.bmp.png"
        external = self.output / "external.png"
        external.write_bytes(target.read_bytes())
        target.unlink()
        target.symlink_to(external)
        with self.assertRaisesRegex(ValueError, "Symlink"):
            load_package(self.root)

    def test_failed_staging_preserves_previous_package_and_clean_rebuild_removes_stale_files(self):
        broken = dict(self.files)
        broken["content/catalog.json"] += b"corrupt"
        with self.assertRaisesRegex(ValueError, "mismatch"):
            builder.write_package(self.output, broken)
        self.assertEqual(load_package(self.root)[0], self.bundle)
        (self.root / "stale.txt").write_text("obsolete")
        builder.write_package(self.output, self.files)
        self.assertFalse((self.root / "stale.txt").exists())
        self.assertEqual(load_package(self.root)[0], self.bundle)

    def test_broken_caption_anchor_fails_even_when_preview_hash_is_updated(self):
        manifest = self.manifest()
        record = manifest["previews"][0]
        raw = b"[View captioned content](#missing)\n"
        (self.root / record["path"]).write_bytes(raw)
        record.update(file_record(record["path"], raw))
        self.save_manifest(manifest)
        with self.assertRaisesRegex(ValueError, "Dangling preview caption"):
            load_package(self.root)

    def test_svg_fragment_dependencies_resolve_without_external_files(self):
        check_svg(b'<svg xmlns="http://www.w3.org/2000/svg"><g id="x"/><use href="#x"/></svg>')
        for content in (b'<use href="other.svg#x"/>', b'<use href="#absent"/>',
                        b'<path fill="url(https://example.test/x)"/>', b'<script/>',
                        b'<style>@import "other.css";</style>'):
            with self.assertRaises(ValueError):
                check_svg(b'<svg xmlns="http://www.w3.org/2000/svg">' + content + b'</svg>')

    def test_preview_updates_never_touch_protected_article_content(self):
        phrase = next(iter(builder.NOTE_UPDATES))
        raw = phrase + b"\n" + phrase + b"\n"
        locations = [{"block_id": "sample:block", "content_byte_offset": len(phrase) + 1,
                      "content_byte_length": len(phrase) + 1}]
        preview, mapped = builder.package_preview(raw, locations)
        self.assertTrue(preview.startswith(builder.NOTE_UPDATES[phrase]))
        start = mapped[0]["content_byte_offset"]
        self.assertEqual(preview[start:], phrase + b"\n")


@unittest.skipUnless((example.OUTPUT / "pilot.example.json").exists() and
                     (markdown.OUTPUT / "provenance.json").exists(), "Private pilot sources unavailable")
class PilotPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record, cls.files = builder.build_package()

    def test_private_package_reproduces_reviewed_record_and_standalone_roundtrip(self):
        self.assertEqual(self.record, json.loads(builder.RECORD.read_bytes()))
        self.assertEqual((self.record, self.files), builder.build_package())
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "relocated"
            builder.write_package(output, self.files)
            bundle, manifest, counts = load_package(output / "content")
            self.assertEqual(bundle, json.loads((example.OUTPUT / "pilot.example.json").read_bytes()))
            self.assertEqual(counts, self.record["counts"])
            self.assertEqual((counts["files"], counts["assets"], counts["previews"]), (26, 19, 2))
            self.assertEqual(len(manifest["documents"]), 4)
            media = {m["id"]: m for m in bundle["media"]["items"]}
            for section in bundle["articles"][0]["sections"]:
                source = ROOT / "build/cd1-text/8802065" / (section["role"] + ".txt")
                self.assertEqual(project_section(section, media).encode(), source.read_bytes())

    def test_all_preview_content_ranges_are_identical_and_caption_links_still_resolve(self):
        original = json.loads((markdown.OUTPUT / "provenance.json").read_bytes())
        provenance = json.loads(self.files["provenance.json"])
        self.assertEqual(len(provenance["preview_content_ranges"]), 271)
        for source, target in zip(original["blocks"], provenance["preview_content_ranges"]):
            self.assertEqual(source["block_id"], target["block_id"])
            raw = (markdown.OUTPUT / source["path"]).read_bytes()
            old = raw[source["content_byte_offset"]:source["content_byte_offset"] + source["content_byte_length"]]
            raw = self.files["content/" + target["path"]]
            new = raw[target["content_byte_offset"]:target["content_byte_offset"] + target["content_byte_length"]]
            self.assertEqual(new, old)
            self.assertEqual(file_record("unused", new)["sha256"], target["sha256"])
        for name, raw in self.files.items():
            if name.endswith(".md"):
                self.assertNotIn(b"awaits viewer comparison", raw)
                self.assertNotIn(b"await viewer comparison", raw)
                self.assertIn(b"Physical-magazine verification is pending", raw)

    def test_only_accepted_media_are_copied_with_separate_preservation_evidence(self):
        provenance = json.loads(self.files["provenance.json"])
        bindings = provenance["contract_evidence"]["asset_bindings"]
        self.assertEqual(len(bindings), 19)
        for binding in bindings:
            self.assertEqual(self.files["content/" + binding["package_path"]], (ROOT / binding["source_path"]).read_bytes())
        media = json.loads(self.files["content/media.json"])["items"]
        deferred = [m for m in media if m["status"] == "deferred"]
        self.assertEqual([m["source"]["resource"] for m in deferred], ["bm54.wmf", "bm55.wmf"])
        self.assertTrue(all(m["asset"] is None for m in deferred))
        self.assertFalse(any("bm54" in p or "bm55" in p for p in self.files))
        for name, raw in self.files.items():
            if name.startswith("content/") and name.endswith(".json"):
                for forbidden in (b'"source_span"', b'"source_path"', b'"viewer_compared"', b"/home/"):
                    self.assertNotIn(forbidden, raw)


if __name__ == "__main__":
    unittest.main()
