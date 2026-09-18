"""Full-topic recovery checks using synthetic text and the private pilot."""

import json
import unittest

from tools import inventory_cd1_rtf as inventory
from tools import recover_cd1_text as recovery


class TextRecoveryTests(unittest.TestCase):
    def recover(self, raw):
        report = inventory.inspect_topic(raw, 0, initial_font=4)
        return recovery.recover_topic(raw, report)

    def test_metadata_is_separate_and_does_not_leak_font_state(self):
        raw = rb"\f5\fs18 A{\footnote\pard\plain{\up #} SECRET}B{\v LINK}C\par "
        topic = self.recover(raw)
        self.assertEqual(recovery.topic_text(topic), "ABC\n")
        self.assertEqual(len(topic["metadata"]), 2)
        self.assertTrue(all(r["format"]["font_id"] == 5 for r in topic["paragraphs"][0]["runs"]))
        self.assertIn("SECRET", topic["metadata"][0]["raw_rtf"])

    def test_spacing_format_resets_and_empty_paragraphs_survive(self):
        raw = rb"\pard\li100\f5\b\fs24 Head\par \pard\plain\fs18  code  x\par \par "
        topic = self.recover(raw)
        self.assertEqual(recovery.topic_text(topic), "Head\n code  x\n\n")
        first, second, empty = topic["paragraphs"]
        self.assertEqual(first["format"], {"li": 100})
        self.assertTrue(first["runs"][0]["format"]["b"])
        self.assertEqual(second["format"], {})
        self.assertFalse(second["runs"][0]["format"]["b"])
        self.assertEqual(second["runs"][0]["format"]["font_id"], 4)
        self.assertEqual(empty["runs"], [])

    def test_multibyte_text_literal_braces_and_objects_keep_order(self):
        raw = rb"\f4\'b0" + b"\n" + rb"\'a1 \{\-x\'7d\{bmc bm1.wmf\}tail\par "
        topic = self.recover(raw)
        self.assertEqual(recovery.topic_text(topic), "가 {x}[object:bm1.wmf]tail\n")
        self.assertEqual(len(topic["transformations"]), 1)
        self.assertEqual(sum(r["kind"] == "object" for r in topic["paragraphs"][0]["runs"]), 1)
        self.assertEqual(sum(x["byte_length"] for x in topic["accounting"]), len(raw))

    def test_undecodable_run_is_retained_with_explicit_issue(self):
        topic = self.recover(rb"\f4\'b0\par recovered\par ")
        self.assertEqual(len(topic["issues"]), 1)
        failed = topic["paragraphs"][0]["runs"][0]
        self.assertEqual(failed["kind"], "unsupported")
        self.assertEqual(failed["original_bytes_hex"], "b0")
        self.assertIn("byte", failed["text"])
        self.assertEqual(topic["paragraphs"][1]["text"], "recovered")
        with self.assertRaises(ValueError):
            self.recover(rb"\f4\unknown X")

    @unittest.skipUnless((inventory.ROOT / inventory.RTF).exists(), "Private RTF unavailable")
    def test_real_text_matches_reviewed_outputs_and_excludes_neighbors(self):
        record, artifacts = recovery.build_recovery()
        self.assertEqual(record, json.loads(recovery.RECORD.read_bytes()))
        article = json.loads(artifacts["article.json"])
        self.assertEqual([t["ordinal"] for t in article["topics"]], [148, 149])
        self.assertEqual([len(t["paragraphs"]) for t in article["topics"]], [4, 319])
        self.assertEqual(record["object_placeholders"], 21)
        self.assertTrue(record["verification"]["all_available_text_decoded"])
        self.assertFalse(record["verification"]["article_completeness_verified"])
        self.assertNotIn(b"BROWSE0001", artifacts["body.txt"])
        self.assertNotIn(b"2PES_R6", artifacts["body.txt"])


if __name__ == "__main__":
    unittest.main()
