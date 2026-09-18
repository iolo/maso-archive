"""Interview turn preservation and a real three-article v1 package."""

from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from maso_archive.reading_room import SCHEMA_PATH, project_section
from maso_archive.reading_room_package import load_package
from tools import prepare_cd1_interview as interview
from tools import build_reading_room_package as package
from tools import recover_cd1_text as recovery
from tools.decode_cd1_paragraph import digest


@unittest.skipUnless((interview.ROOT / "private/cd1-probe/raw/MASOCD.rtf").exists() and
                     (interview.PREVIOUS / "manifest.json").exists(), "Private interview sources unavailable")
class InterviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record, cls.files = interview.build_article()
        cls.article = json.loads(cls.files["recovery.json"])
        cls.mapping = json.loads(cls.files["blocks.json"])
        cls.runtime = json.loads(cls.files["single/content/articles/cd1/8802030.json"])
        cls.evidence = json.loads(cls.files["provenance.json"])

    def test_rebuild_matches_reviewed_record_and_unchanged_schema(self):
        self.assertEqual(self.record, json.loads(interview.RECORD.read_bytes()))
        self.assertEqual((self.record, self.files), interview.build_article())
        self.assertEqual(digest(SCHEMA_PATH.read_bytes()), "2a160d646c4a92552fcc4647216348c14ee74c357a375412f23fed54bffc6f68")
        self.assertEqual(self.record["counts"]["paragraphs"], 107)
        self.assertEqual(self.record["interview_turns"], 27)

    def test_native_boundaries_and_complete_source_byte_accounting(self):
        self.assertEqual([r["native"]["ordinal"] for r in self.evidence["topic_map"]], [145, 146])
        self.assertEqual(self.evidence["topic_map"][1]["context"]["hash_hex"], "0x0e6881f5")
        self.assertEqual(sum(r["rtf"]["byte_length"] for r in self.evidence["topic_map"]), 71443)
        self.assertEqual([b["native"]["ordinal"] for b in self.evidence["boundary_separators"]], [144, 147])
        for topic in self.article["topics"]:
            cursor = topic["source_span"]["byte_offset"]
            for token in topic["accounting"]:
                self.assertEqual(token["byte_offset"], cursor)
                cursor += token["byte_length"]
            self.assertEqual(cursor, topic["source_span"]["end_exclusive"])
            self.assertFalse(topic["issues"])
        self.assertEqual(len(self.evidence["index_occurrences"]), 2)
        self.assertEqual(self.runtime["pages"], {"start": 30, "end": None})

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
                        self.assertEqual(target["media_id"], "cd1:media:bm42.bmp")

    def test_turns_preserve_multiple_answer_paragraphs_without_inventing_headings(self):
        by_id = {b["id"]: b for b in self.runtime["sections"][1]["blocks"]}
        self.assertEqual([t["question_block_id"] for t in self.mapping["interview_turns"]],
                         [interview.block_id(146, n) for n in interview.QUESTIONS])
        answer_ids = []
        for turn in self.mapping["interview_turns"]:
            question = by_id[turn["question_block_id"]]
            self.assertEqual(question["type"], "paragraph")
            self.assertIsNone(question["heading_level"])
            self.assertTrue(all("bold" in r["marks"] for p in question["paragraphs"] for r in p["runs"]))
            answer_ids.extend(turn["answer_block_ids"])
            for key in turn["answer_block_ids"]:
                self.assertTrue(all("bold" not in r["marks"] for p in by_id[key]["paragraphs"] for r in p["runs"]))
        self.assertEqual(len(answer_ids), len(set(answer_ids)))
        self.assertEqual(self.mapping["interview_turns"][-1]["answer_block_ids"],
                         [interview.block_id(146, n) for n in (99, 100, 101, 102)])
        self.assertFalse(any(b["type"] == "heading" for b in by_id.values()))

    def test_changed_question_or_answer_style_fails_closed(self):
        article = deepcopy(self.article)
        article["topics"][1]["paragraphs"][9]["format"]["li"] = 395
        with self.assertRaisesRegex(ValueError, "Question style"):
            interview.map_interview(article)
        article = deepcopy(self.article)
        article["topics"][1]["paragraphs"][9]["runs"][0]["format"]["b"] = False
        with self.assertRaisesRegex(ValueError, "question boundaries"):
            interview.map_interview(article)
        article = deepcopy(self.article)
        article["topics"][1]["paragraphs"][10]["runs"][0]["kind"] = "unsupported"
        with self.assertRaisesRegex(ValueError, "Answer structure"):
            interview.map_interview(article)

    def test_bitmap_pixels_and_every_preview_content_range(self):
        with Image.open(interview.ROOT / "private/cd1-probe/raw/bm42.bmp") as source:
            expected = source.convert("RGBA").tobytes()
        with Image.open(io.BytesIO(self.files["single/content/media/cd1/bm42.bmp.png"])) as converted:
            self.assertEqual(converted.size, (32, 25))
            self.assertEqual(converted.convert("RGBA").tobytes(), expected)
        self.assertEqual(len(self.evidence["preview_content_ranges"]), 107)
        for row in self.evidence["preview_content_ranges"]:
            start = row["content_byte_offset"]
            raw = self.files["single/content/" + row["path"]]
            self.assertEqual(digest(raw[start:start + row["content_byte_length"]]), row["sha256"])
        preview = self.files["single/content/previews/cd1/8802030/body.md"].decode()
        self.assertIn("<strong>", preview)
        self.assertNotIn("\n## ", preview)

    def test_relocated_packages_keep_previous_articles_and_deferred_assets(self):
        for which in ("single", "combined"):
            with tempfile.TemporaryDirectory() as temporary:
                output = Path(temporary) / "relocated"
                prefix = which + "/"
                package.write_package(output, {p[len(prefix):]: raw for p, raw in self.files.items() if p.startswith(prefix)})
                bundle, _, counts = load_package(output / "content")
                self.assertEqual(counts["articles"], 1 if which == "single" else 3)
                self.assertEqual(counts["files"], 8 if which == "single" else 34)
                if which == "combined":
                    self.assertEqual(sum(e["link_status"] == "matched" for e in bundle["issues"][0]["toc"]), 3)
                    deferred = [m for m in bundle["media"]["items"] if m["status"] == "deferred"]
                    self.assertEqual(len(deferred), 2)
                    self.assertTrue(all(m["asset"] is None for m in deferred))
        previous = json.loads((interview.PREVIOUS / "manifest.json").read_bytes())
        for row in previous["documents"]:
            if row["kind"] == "article":
                self.assertEqual(self.files["combined/content/" + row["path"]], (interview.PREVIOUS / row["path"]).read_bytes())
        for row in previous["previews"]:
            self.assertEqual(self.files["combined/content/" + row["path"]], (interview.PREVIOUS / row["path"]).read_bytes())

    def test_book_attribution_is_separate_from_cd_byline_and_print_review(self):
        self.assertEqual(self.runtime["byline"], "글/ 편집부")
        self.assertEqual(self.runtime["print_verification"]["status"], "pending")
        note = self.evidence["bibliographic_note"]
        self.assertEqual(note["reported_by"], "owner")
        self.assertEqual(note["work_title"], "Programmers at Work")
        self.assertFalse(note["verified_against_book"])
        self.assertFalse(note["book_credit_observed_in_recovered_cd_text"])


if __name__ == "__main__":
    unittest.main()
