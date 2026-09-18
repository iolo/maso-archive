"""Second source case and real multi-article v1 composition checks."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from maso_archive.reading_room import SCHEMA_PATH, project_section
from maso_archive.reading_room_package import load_package
from tools import check_cd1_second_article as second
from tools import inventory_cd1_rtf as inventory
from tools import recover_cd1_text as recovery
from tools import build_reading_room_package as package
from tools.decode_cd1_paragraph import digest


class FontPolicyTests(unittest.TestCase):
    def test_fixedsys_is_opt_in_and_ascii_only(self):
        raw = rb"\f15  PROGRAM TEST;\par  \{\- comment\'7d  \par "
        report = inventory.inspect_topic(raw, 0, 4)
        default = recovery.recover_topic(raw, report)
        self.assertTrue(default["issues"])
        decoded = recovery.recover_topic(raw, report, font_codecs=second.FONT_CODECS)
        self.assertFalse(decoded["issues"])
        self.assertEqual(recovery.topic_text(decoded), " PROGRAM TEST;\n { comment}  \n")
        self.assertTrue(all(r["encoding"] == "ascii" for p in decoded["paragraphs"] for r in p["runs"]))
        non_ascii = rb"\f15\'b0\'a1\par "
        failed = recovery.recover_topic(non_ascii, inventory.inspect_topic(non_ascii, 0, 4), font_codecs=second.FONT_CODECS)
        self.assertEqual(failed["paragraphs"][0]["runs"][0]["original_bytes_hex"], "b0a1")
        self.assertTrue(failed["issues"])


@unittest.skipUnless((second.ROOT / "private/cd1-probe/raw/MASOCD.rtf").exists() and
                     (package.OUTPUT / "content/manifest.json").exists(), "Private second-case sources unavailable")
class SecondArticleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record, cls.files = second.build_check()
        cls.article = json.loads(cls.files["recovery.json"])
        cls.runtime = json.loads(cls.files["single/content/articles/cd1/8802114.json"])
        cls.mapping = json.loads(cls.files["blocks.json"])
        cls.evidence = json.loads(cls.files["provenance.json"])

    def test_rebuild_matches_record_and_approved_schema_hash(self):
        self.assertEqual(self.record, json.loads(second.RECORD.read_bytes()))
        self.assertEqual((self.record, self.files), second.build_check())
        self.assertEqual(digest(SCHEMA_PATH.read_bytes()), "2a160d646c4a92552fcc4647216348c14ee74c357a375412f23fed54bffc6f68")
        self.assertEqual(self.record["fixedsys_ascii_runs"], 417)
        self.assertEqual(self.record["literal_brace_guards_removed"], 34)

    def test_native_reference_boundaries_metadata_and_exact_token_accounting(self):
        mapping = self.evidence["topic_map"]
        self.assertEqual([t["native"]["ordinal"] for t in mapping], [151, 152])
        self.assertEqual(mapping[1]["context"]["hash_hex"], "0x0e684098")
        self.assertEqual(self.evidence["toc_match"]["id"], "maso-1988-02-toc-0021")
        self.assertEqual(len(self.evidence["index_occurrences"]), 3)
        for topic in self.article["topics"]:
            cursor = topic["source_span"]["byte_offset"]
            for item in topic["accounting"]:
                self.assertEqual(item["byte_offset"], cursor)
                cursor += item["byte_length"]
            self.assertEqual(cursor, topic["source_span"]["end_exclusive"])
        self.assertEqual(self.runtime["pages"], {"start": 114, "end": None})
        self.assertEqual(self.runtime["print_verification"]["status"], "pending")

    def test_every_run_format_paragraph_and_source_projection_survives(self):
        media = json.loads(self.files["single/content/media.json"])["items"][0]
        self.assertEqual(sum(len(p["runs"]) for t in self.article["topics"] for p in t["paragraphs"]), 439)
        for topic, section in zip(self.article["topics"], self.runtime["sections"]):
            paragraphs = [p for b in section["blocks"] for p in b["paragraphs"]]
            self.assertEqual(len(paragraphs), len(topic["paragraphs"]))
            for source, target in zip(topic["paragraphs"], paragraphs):
                self.assertEqual(len(source["runs"]), len(target["runs"]))
                for before, after in zip(source["runs"], target["runs"]):
                    self.assertEqual(after["marks"], [name for key, name in (("b", "bold"), ("ul", "underline")) if before["format"][key]])
                    if before["kind"] == "text":
                        self.assertEqual(before["text"], after["text"])
                        self.assertEqual(digest(before["text"].encode(before["encoding"])), before["encoded_sha256"])
                    else:
                        self.assertEqual(after["media_id"], media["id"])
            self.assertEqual(project_section(section, {media["id"]: media}).encode(), self.files[section["role"] + ".txt"])

    def test_unnumbered_headings_and_three_long_listings_keep_boundaries(self):
        body = self.runtime["sections"][1]["blocks"]
        headings = [b for b in body if b["type"] == "heading"]
        self.assertEqual([b["heading_level"] for b in headings], [1, 1])
        self.assertEqual([b["paragraphs"][0]["runs"][0]["text"] for b in headings], ["프로그램의 입력", "사용법"])
        code = [b for b in body if b["type"] == "code"]
        self.assertEqual([len(b["paragraphs"]) for b in code], [1, 317, 36, 96])
        self.assertTrue(all(b["layout"] == "preformatted" for b in code))
        self.assertTrue(any(not p["runs"] for b in code for p in b["paragraphs"]))
        self.assertEqual(len(self.runtime["relationships"]), 3)
        changed = deepcopy(self.article)
        changed["topics"][1]["paragraphs"][341]["text"] = "Not an ending"
        with self.assertRaisesRegex(ValueError, "Listing boundaries"):
            second.block_map(changed)

    def test_standalone_and_combined_packages_relocate_without_identity_collisions(self):
        first, _, _ = load_package(package.OUTPUT / "content")
        with tempfile.TemporaryDirectory() as directory:
            for name, count in (("single", 8), ("combined", 30)):
                root = Path(directory) / name
                prefix = name + "/"
                package.write_package(root, {p[len(prefix):]: raw for p, raw in self.files.items() if p.startswith(prefix)})
                bundle, _, report = load_package(root / "content")
                self.assertEqual(report["files"], count)
                if name == "combined":
                    self.assertEqual(bundle["articles"][0], first["articles"][0])
                    self.assertEqual(bundle["media"]["items"][:-1], first["media"]["items"])
                    self.assertEqual(report["paragraphs"], 808)
                    self.assertEqual(sum(e["link_status"] == "matched" for e in bundle["issues"][0]["toc"]), 2)
                    self.assertEqual(sum(m["status"] == "deferred" for m in bundle["media"]["items"]), 2)

    def test_preview_content_and_new_bitmap_match_preservation_records(self):
        originals, locations = second.markdown.render(self.article, self.mapping)
        for original, mapped in zip(locations, self.evidence["preview_content_ranges"]):
            old = originals[original["path"]][original["content_byte_offset"]:original["content_byte_offset"] + original["content_byte_length"]]
            raw = self.files["single/content/" + mapped["path"]]
            new = raw[mapped["content_byte_offset"]:mapped["content_byte_offset"] + mapped["content_byte_length"]]
            self.assertEqual(old, new)
        conversion = self.evidence["conversion"]
        for key in ("width", "height", "rgba_sha256"):
            self.assertEqual(conversion["source_format"][key], conversion["png_pixels"][key])
        for path, raw in self.files.items():
            if "/content/" in path and path.endswith(".json"):
                self.assertNotIn(b'"source_span"', raw)
                self.assertNotIn(b'"source_path"', raw)


if __name__ == "__main__":
    unittest.main()
