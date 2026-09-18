"""Block map coverage and evidence checks; publisher text stays private."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import map_cd1_blocks as mapper


class HeadingEvidenceTests(unittest.TestCase):
    def test_heading_needs_both_numbered_label_and_formatting(self):
        paragraph = {"text": "II. Example", "format": {"li": 215},
                     "runs": [{"kind": "text", "format": {"b": True, "fs": 24}}]}
        self.assertEqual(mapper.heading_level(paragraph), 1)
        paragraph["text"] = "ordinary sentence"
        self.assertIsNone(mapper.heading_level(paragraph))
        paragraph["text"] = "II. Example"
        paragraph["runs"][0]["format"]["b"] = False
        self.assertIsNone(mapper.heading_level(paragraph))

    def test_changed_recovery_rejected_before_classification(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "article.json"
            path.write_text("{}", encoding="utf-8")
            with patch.object(mapper, "SOURCE", path), self.assertRaisesRegex(ValueError, "Changed structured recovery"):
                mapper.build_map()


@unittest.skipUnless(mapper.SOURCE.exists(), "Private structured recovery unavailable")
class PilotBlockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.article = json.loads(mapper.SOURCE.read_bytes())
        cls.record, encoded = mapper.build_map()
        cls.block_map = json.loads(encoded)

    def test_reviewed_map_preserves_code_blanks_and_inline_objects(self):
        self.assertEqual(self.record, json.loads(mapper.RECORD.read_bytes()))
        blocks = self.block_map["blocks"]
        code = [b for b in blocks if b["kind"] == "code"]
        self.assertEqual(len(code), 17)
        tbl = next(b for b in code if b["subtype"] == "roff_tbl_example")
        self.assertEqual(tbl["representation"], "mixed_text_objects")
        self.assertEqual(len(tbl["object_refs"]), 10)
        self.assertEqual([m["paragraph_ordinal"] for m in tbl["members"]], list(range(156, 174)))
        pic = next(b for b in code if b["subtype"] == "pic_example")
        self.assertIn(193, [m["paragraph_ordinal"] for m in pic["members"]])
        unresolved = [b for b in blocks if b["kind"] == "unresolved"]
        self.assertEqual([o["resource"] for b in unresolved for o in b["object_refs"]], ["bm54.wmf"])
        by_id = {b["id"]: b for b in blocks}
        example_caption = next(r for r in self.block_map["relationships"] if r["label_kind"] == "figure" and r["label_number"] == 8)
        self.assertEqual(by_id[example_caption["to_block"]]["kind"], "code")
        self.assertEqual(self.record["counts"]["paragraphs"], 323)
        self.assertEqual(self.record["counts"]["objects"], 21)

    def test_omissions_duplicates_and_invalid_relationships_rejected(self):
        variants = []
        missing = deepcopy(self.block_map)
        missing["blocks"].pop(0)
        variants.append(missing)
        duplicate = deepcopy(self.block_map)
        duplicate["blocks"][0]["members"].append(duplicate["blocks"][0]["members"][0])
        variants.append(duplicate)
        run = deepcopy(self.block_map)
        next(m for b in run["blocks"] for m in b["members"] if m["run_ordinals"])["run_ordinals"].pop()
        variants.append(run)
        obj = deepcopy(self.block_map)
        next(b for b in obj["blocks"] if b["object_refs"])["object_refs"].pop()
        variants.append(obj)
        relation = deepcopy(self.block_map)
        relation["relationships"][0]["to_block"] = "missing"
        variants.append(relation)
        for number, variant in enumerate(variants):
            with self.subTest(number=number), self.assertRaises(ValueError):
                mapper.validate_map(self.article, variant)

    def test_text_spacing_change_rejected_by_projection_hash(self):
        changed = deepcopy(self.article)
        changed["topics"][1]["paragraphs"][187]["text"] = changed["topics"][1]["paragraphs"][187]["text"].lstrip()
        with self.assertRaisesRegex(ValueError, "Block text/spacing changed"):
            mapper.validate_map(changed, self.block_map)


if __name__ == "__main__":
    unittest.main()
