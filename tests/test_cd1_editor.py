"""Editor listings, diagrams, shared media, and a four-article v1 package."""

from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from maso_archive.reading_room import SCHEMA_PATH, project_section
from maso_archive.reading_room_package import load_package
from tools import prepare_cd1_editor as editor
from tools import build_reading_room_package as package
from tools import recover_cd1_text as recovery
from tools.decode_cd1_paragraph import digest


@unittest.skipUnless((editor.ROOT / "private/cd1-probe/raw/MASOCD.rtf").exists() and
                     (editor.PREVIOUS / "manifest.json").exists(), "Private editor sources unavailable")
class EditorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record, cls.files = editor.build_article()
        cls.article = json.loads(cls.files["recovery.json"])
        cls.mapping = json.loads(cls.files["blocks.json"])
        cls.runtime = json.loads(cls.files["single/content/articles/cd1/8802184.json"])
        cls.evidence = json.loads(cls.files["provenance.json"])

    def test_rebuild_matches_reviewed_record_and_unchanged_schema(self):
        self.assertEqual(self.record, json.loads(editor.RECORD.read_bytes()))
        self.assertEqual((self.record, self.files), editor.build_article())
        self.assertEqual(digest(SCHEMA_PATH.read_bytes()), "2a160d646c4a92552fcc4647216348c14ee74c357a375412f23fed54bffc6f68")
        self.assertEqual(self.record["counts"]["paragraphs"], 1206)
        self.assertEqual(self.record["counts"]["blocks"], 85)

    def test_native_boundaries_and_complete_source_byte_accounting(self):
        self.assertEqual([r["native"]["ordinal"] for r in self.evidence["topic_map"]], [160, 161])
        self.assertEqual(self.evidence["topic_map"][1]["context"]["hash_hex"], "0x0e6841c5")
        self.assertEqual(sum(r["rtf"]["byte_length"] for r in self.evidence["topic_map"]), 62315)
        self.assertEqual([b["native"]["ordinal"] for b in self.evidence["boundary_separators"]], [159, 162])
        for topic in self.article["topics"]:
            cursor = topic["source_span"]["byte_offset"]
            for token in topic["accounting"]:
                self.assertEqual(token["byte_offset"], cursor)
                cursor += token["byte_length"]
            self.assertEqual(cursor, topic["source_span"]["end_exclusive"])
            self.assertFalse(topic["issues"])
        self.assertEqual(len(self.evidence["index_occurrences"]), 2)
        self.assertEqual(self.runtime["pages"], {"start": 184, "end": None})
        self.assertEqual(self.runtime["print_verification"]["status"], "pending")

    def test_all_runs_marks_objects_and_source_text_survive(self):
        media = json.loads(self.files["single/content/media.json"])["items"]
        lookup = {m["id"]: m for m in media}
        for topic, section in zip(self.article["topics"], self.runtime["sections"]):
            self.assertEqual(project_section(section, lookup), recovery.topic_text(topic))
            exported = [p for b in section["blocks"] for p in b["paragraphs"]]
            self.assertEqual(len(exported), len(topic["paragraphs"]))
            for old, new in zip(topic["paragraphs"], exported):
                self.assertEqual(len(old["runs"]), len(new["runs"]))
                for source, target in zip(old["runs"], new["runs"]):
                    self.assertEqual(target["marks"], [name for key, name in (("b", "bold"), ("ul", "underline")) if source["format"][key]])
                    if source["kind"] == "text":
                        self.assertEqual(target["text"], source["text"])
                        self.assertEqual(digest(target["text"].encode(source["encoding"])), source["encoded_sha256"])
                    else:
                        self.assertEqual(target["media_id"], "cd1:media:" + source["object"]["resource"])

    def test_both_code_blocks_and_tabs_survive_markdown_exactly(self):
        code = [b for b in self.mapping["blocks"] if b["kind"] == "code"]
        self.assertEqual([len(b["members"]) for b in code], [1121, 2])
        self.assertEqual(sum(t["action"] == "emit_rtf_tab_character"
                             for topic in self.article["topics"] for t in topic["transformations"]), 30)
        body = self.article["topics"][1]["paragraphs"]
        preview = self.files["single/content/previews/cd1/8802184/body.md"]
        for block in code:
            row = next(r for r in self.evidence["preview_content_ranges"] if r["block_id"] == block["id"])
            raw = preview[row["content_byte_offset"]:row["content_byte_offset"] + row["content_byte_length"]]
            expected = recovery.topic_text({"paragraphs": [body[m["paragraph_ordinal"] - 1] for m in block["members"]]}).encode()
            self.assertEqual(raw, b"```\n" + expected + b"```\n")
        self.assertEqual(preview.count(b"\t"), 30)
        self.assertIn(b"char far *vram", preview)
        self.assertIn(b"*(varm)", preview)  # Preserve the source's inconsistent spelling.

    def test_heading_hierarchy_and_caption_targets(self):
        blocks = {b["id"]: b for b in self.runtime["sections"][1]["blocks"]}
        for ordinal in editor.SUBHEADINGS:
            heading = blocks[editor.block_id(161, ordinal)]
            self.assertEqual(heading["heading_level"], 2)
            self.assertEqual(heading["parent_heading_id"], editor.block_id(161, 1146))
        self.assertEqual(blocks[editor.block_id(161, 1199)]["heading_level"], 1)
        self.assertIsNone(blocks[editor.block_id(161, 1199)]["parent_heading_id"])
        self.assertEqual(len(self.runtime["relationships"]), 4)
        for relation, (caption, target) in zip(self.runtime["relationships"], editor.CAPTIONS):
            self.assertEqual(relation["from_block"], editor.block_id(161, caption))
            block = blocks[relation["to_block"]]
            self.assertEqual(block["paragraphs"][0]["id"], f"cd1-8802184:T161:P{target:03d}")
            self.assertEqual(block["type"], "code" if caption == 22 else "figure")

    def test_changed_listing_or_heading_evidence_fails_closed(self):
        cases = [(23, "font_id", 4, "Listing font"), (8, "fs", 18, "Heading evidence")]
        for index, field, value, message in cases:
            article = deepcopy(self.article)
            article["topics"][1]["paragraphs"][index]["runs"][0]["format"][field] = value
            with self.assertRaisesRegex(ValueError, message):
                editor.map_editor(article)
        article = deepcopy(self.article)
        article["topics"][1]["paragraphs"][68]["text"] = "spaces substituted"
        with self.assertRaisesRegex(ValueError, "Listing tab count"):
            editor.map_editor(article)

    def test_bitmap_pixels_and_every_preview_content_range(self):
        for name in editor.RESOURCES:
            with Image.open(editor.ROOT / "private/cd1-probe/raw" / name) as source:
                expected, size = source.convert("RGBA").tobytes(), source.size
            with Image.open(io.BytesIO(self.files["single/content/media/cd1/" + name + ".png"])) as converted:
                self.assertEqual(converted.size, size)
                self.assertEqual(converted.convert("RGBA").tobytes(), expected)
        self.assertEqual(len(self.evidence["preview_content_ranges"]), 85)
        for row in self.evidence["preview_content_ranges"]:
            start = row["content_byte_offset"]
            raw = self.files["single/content/" + row["path"]]
            self.assertEqual(digest(raw[start:start + row["content_byte_length"]]), row["sha256"])

    def test_relocated_packages_share_media_and_preserve_previous_articles(self):
        for which in ("single", "combined"):
            with tempfile.TemporaryDirectory() as temporary:
                output = Path(temporary) / "relocated"
                prefix = which + "/"
                package.write_package(output, {p[len(prefix):]: raw for p, raw in self.files.items() if p.startswith(prefix)})
                bundle, _, counts = load_package(output / "content")
                self.assertEqual(counts["articles"], 1 if which == "single" else 4)
                self.assertEqual(counts["files"], 12 if which == "single" else 41)
                if which == "combined":
                    self.assertEqual(sum(e["link_status"] == "matched" for e in bundle["issues"][0]["toc"]), 4)
                    deferred = [m for m in bundle["media"]["items"] if m["status"] == "deferred"]
                    self.assertEqual(len(deferred), 2)
                    self.assertTrue(all(m["asset"] is None for m in deferred))
                    self.assertEqual(sum(m["id"] == "cd1:media:bm40.bmp" for m in bundle["media"]["items"]), 1)
        previous, manifest, _ = load_package(editor.PREVIOUS)
        rows = [r for r in manifest["documents"] if r["kind"] == "article"] + manifest["previews"]
        rows += [m["asset"] for m in previous["media"]["items"] if m["asset"]]
        for row in rows:
            self.assertEqual(self.files["combined/content/" + row["path"]], (editor.PREVIOUS / row["path"]).read_bytes())
        combined_media = json.loads(self.files["combined/content/media.json"])["items"]
        self.assertEqual(combined_media[:len(previous["media"]["items"])], previous["media"]["items"])


if __name__ == "__main__":
    unittest.main()
