"""Pascal listings, mixed figures, deferred media, and a five-article package."""

from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from maso_archive.reading_room import SCHEMA_PATH, project_section
from maso_archive.reading_room_package import load_package
from tools import prepare_cd1_graphics as graphics
from tools import build_reading_room_package as package
from tools import recover_cd1_text as recovery
from tools.decode_cd1_paragraph import digest


@unittest.skipUnless((graphics.ROOT / "private/cd1-probe/raw/MASOCD.rtf").exists() and
                     (graphics.PREVIOUS / "manifest.json").exists(), "Private graphics sources unavailable")
class GraphicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record, cls.files = graphics.build_article()
        cls.article = json.loads(cls.files["recovery.json"])
        cls.mapping = json.loads(cls.files["blocks.json"])
        cls.runtime = json.loads(cls.files["single/content/articles/cd1/8802180.json"])
        cls.evidence = json.loads(cls.files["provenance.json"])

    def test_rebuild_matches_reviewed_record_and_unchanged_schema(self):
        self.assertEqual(self.record, json.loads(graphics.RECORD.read_bytes()))
        self.assertEqual((self.record, self.files), graphics.build_article())
        self.assertEqual(digest(SCHEMA_PATH.read_bytes()), "2a160d646c4a92552fcc4647216348c14ee74c357a375412f23fed54bffc6f68")
        self.assertEqual(self.record["counts"]["paragraphs"], 397)
        self.assertEqual(self.record["counts"]["blocks"], 80)

    def test_native_boundaries_and_complete_source_byte_accounting(self):
        self.assertEqual([r["native"]["ordinal"] for r in self.evidence["topic_map"]], [157, 158])
        self.assertEqual(self.evidence["topic_map"][1]["context"]["hash_hex"], "0x0e6841cb")
        self.assertEqual(sum(r["rtf"]["byte_length"] for r in self.evidence["topic_map"]), 26283)
        self.assertEqual([b["native"]["ordinal"] for b in self.evidence["boundary_separators"]], [156, 159])
        for topic in self.article["topics"]:
            cursor = topic["source_span"]["byte_offset"]
            for token in topic["accounting"]:
                self.assertEqual(token["byte_offset"], cursor)
                cursor += token["byte_length"]
            self.assertEqual(cursor, topic["source_span"]["end_exclusive"])
            self.assertFalse(topic["issues"])
        self.assertEqual(len(self.evidence["index_occurrences"]), 2)
        self.assertEqual(self.runtime["pages"], {"start": 180, "end": None})
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

    def test_listings_korean_strings_and_suspect_text_are_preserved(self):
        code = [b for b in self.mapping["blocks"] if b["kind"] == "code"]
        self.assertEqual([len(b["members"]) for b in code], [18, 1, 1, 210, 91])
        body = self.article["topics"][1]["paragraphs"]
        preview = self.files["single/content/previews/cd1/8802180/body.md"]
        for block in code:
            row = next(r for r in self.evidence["preview_content_ranges"] if r["block_id"] == block["id"])
            raw = preview[row["content_byte_offset"]:row["content_byte_offset"] + row["content_byte_length"]]
            expected = recovery.topic_text({"paragraphs": [body[m["paragraph_ordinal"] - 1] for m in block["members"]]}).encode()
            self.assertEqual(raw, b"```\n" + expected + b"```\n")
        korean = [r for p in body for r in p["runs"] if r["kind"] == "text" and r["format"]["font_id"] == 15 and
                  any(ord(c) > 127 for c in r["text"])]
        self.assertEqual(len(korean), 7)
        self.assertTrue(all(r["encoding"] == "cp949" for r in korean))
        self.assertEqual(body[319]["text"].count("\uB2AF"), 2)
        self.assertEqual(body[319]["text"].encode("cp949").count(bytes.fromhex("8874")), 2)
        review = self.evidence["text_reviews"][0]
        self.assertEqual(review["source_span"], body[319]["source_span"])
        self.assertFalse(review["corrected"])
        self.assertEqual(review["status"], "pending_physical_comparison")
        alternative = review["alternative_decoding"]
        self.assertEqual(ord(bytes.fromhex(review["encoded_pair_hex"]).decode(alternative["codec"])),
                         int(alternative["codepoint"][2:], 16))
        self.assertFalse(alternative["applied"])
        self.assertIn(b"A source string in this block needs physical-magazine review", preview)

    def test_mixed_figure_and_all_caption_relationships(self):
        blocks = {b["id"]: b for b in self.runtime["sections"][1]["blocks"]}
        for ordinal in graphics.SUBHEADINGS:
            heading = blocks[graphics.block_id(158, ordinal)]
            self.assertEqual(heading["heading_level"], 2)
            self.assertEqual(heading["parent_heading_id"], graphics.block_id(158, 11))
        figure = blocks[graphics.block_id(158, 293, 294)]
        self.assertEqual(figure["type"], "figure")
        self.assertEqual([p["id"] for p in figure["paragraphs"]], ["cd1-8802180:T158:P293", "cd1-8802180:T158:P294"])
        self.assertEqual(figure["paragraphs"][0]["runs"][0]["type"], "text")
        self.assertEqual(figure["paragraphs"][1]["runs"][0]["media_id"], "cd1:media:82181_3.dib")
        self.assertEqual(len(self.runtime["relationships"]), 6)
        for relation, (caption, target) in zip(self.runtime["relationships"], graphics.CAPTIONS):
            self.assertEqual(relation["from_block"], graphics.block_id(158, caption))
            self.assertEqual(blocks[relation["to_block"]]["paragraphs"][0]["id"], f"cd1-8802180:T158:P{target:03d}")
        row = next(r for r in self.evidence["preview_content_ranges"] if r["block_id"] == figure["id"])
        preview = self.files["single/content/" + row["path"]]
        content = preview[row["content_byte_offset"]:row["content_byte_offset"] + row["content_byte_length"]]
        self.assertTrue(content.startswith(b"&#32;" * 4))
        self.assertIn(b"\n\n", content)
        self.assertLess(content.index("A 값".encode()), content.index(b"82181"))
        self.assertIn("A 값", figure["paragraphs"][0]["runs"][0]["text"])

    def test_changed_listing_or_figure_evidence_fails_closed(self):
        article = deepcopy(self.article)
        article["topics"][1]["paragraphs"][18]["runs"][0]["format"]["font_id"] = 4
        with self.assertRaisesRegex(ValueError, "Listing font"):
            graphics.map_graphics(article)
        article = deepcopy(self.article)
        article["topics"][1]["paragraphs"][292]["text"] = "changed figure header"
        with self.assertRaisesRegex(ValueError, "Figure header"):
            graphics.map_graphics(article)

    def test_bitmap_pixels_and_every_preview_content_range(self):
        for name in graphics.RESOURCES:
            if name.endswith(".wmf"):
                continue
            with Image.open(graphics.ROOT / "private/cd1-probe/raw" / name) as source:
                expected, size = source.convert("RGBA").tobytes(), source.size
            with Image.open(io.BytesIO(self.files["single/content/media/cd1/" + name + ".png"])) as converted:
                self.assertEqual(converted.size, size)
                self.assertEqual(converted.convert("RGBA").tobytes(), expected)
        self.assertEqual(len(self.evidence["preview_content_ranges"]), 80)
        for row in self.evidence["preview_content_ranges"]:
            start = row["content_byte_offset"]
            raw = self.files["single/content/" + row["path"]]
            self.assertEqual(digest(raw[start:start + row["content_byte_length"]]), row["sha256"])

    def test_title_variant_is_matched_only_with_native_body_and_page_evidence(self):
        evidence = self.record["title_comparison"]
        self.assertEqual(evidence["toc_title"], graphics.TITLE)
        self.assertEqual(evidence["native_and_body_title"], graphics.TITLE)
        self.assertEqual(evidence["index_title"], graphics.INDEX_TITLE)
        self.assertNotEqual(evidence["index_title"], evidence["toc_title"])
        self.assertEqual(evidence["decision"], "matched")
        self.assertIn("no_global_title_normalization", evidence["scope"])
        self.assertEqual(self.runtime["toc_entry_ids"], [graphics.TOC_ID])

    def test_deferred_vectors_keep_records_and_no_runtime_assets(self):
        deferred = json.loads(self.files["deferred-media.json"])
        self.assertEqual(deferred, json.loads(graphics.DEFERRED_RECORD.read_bytes()))
        self.assertEqual([r["resource"] for r in deferred["issues"]], ["bm57.wmf", "bm58.wmf"])
        media = json.loads(self.files["single/content/media.json"])["items"]
        for problem in deferred["issues"]:
            self.assertFalse(problem["resolved"])
            item = next(m for m in media if m["source"]["resource"] == problem["resource"])
            self.assertEqual(item["status"], "deferred")
            self.assertIsNone(item["asset"])
            self.assertEqual(item["problem_ids"], [problem["id"]])
            self.assertIn("deferred-media/assets/" + problem["resource"] + ".svg", self.files)
            self.assertFalse(any(name.startswith(("single/", "combined/")) and problem["resource"] in name
                                 for name in self.files))

    def test_relocated_packages_share_media_and_preserve_previous_articles(self):
        for which in ("single", "combined"):
            with tempfile.TemporaryDirectory() as temporary:
                output = Path(temporary) / "relocated"
                prefix = which + "/"
                package.write_package(output, {p[len(prefix):]: raw for p, raw in self.files.items() if p.startswith(prefix)})
                bundle, _, counts = load_package(output / "content")
                self.assertEqual(counts["articles"], 1 if which == "single" else 5)
                self.assertEqual(counts["files"], 12 if which == "single" else 48)
                if which == "combined":
                    self.assertEqual(sum(e["link_status"] == "matched" for e in bundle["issues"][0]["toc"]), 5)
                    deferred = [m for m in bundle["media"]["items"] if m["status"] == "deferred"]
                    self.assertEqual(len(deferred), 4)
                    self.assertTrue(all(m["asset"] is None for m in deferred))
                    self.assertEqual(sum(m["id"] == "cd1:media:bm39.bmp" for m in bundle["media"]["items"]), 1)
        previous, manifest, _ = load_package(graphics.PREVIOUS)
        rows = [r for r in manifest["documents"] if r["kind"] == "article"] + manifest["previews"]
        rows += [m["asset"] for m in previous["media"]["items"] if m["asset"]]
        for row in rows:
            self.assertEqual(self.files["combined/content/" + row["path"]], (graphics.PREVIOUS / row["path"]).read_bytes())
        combined_media = json.loads(self.files["combined/content/media.json"])["items"]
        self.assertEqual(combined_media[:len(previous["media"]["items"])], previous["media"]["items"])


if __name__ == "__main__":
    unittest.main()
