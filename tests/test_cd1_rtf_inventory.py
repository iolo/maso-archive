"""RTF inventory tests with synthetic syntax and private-source integration."""

import json
import unittest

from tools import inventory_cd1_rtf as inventory


class RtfInventoryTests(unittest.TestCase):
    def test_every_byte_covered_with_escapes_delimiters_and_binary(self):
        raw = rb"{\f5 A\'b0\'a1 \{literal\}\\}" + b"\r\n" + rb"\bin4 " + b"{\\}\x00"
        tokens = inventory.tokenize(raw, 100)
        offset = 100
        rebuilt = bytearray()
        for token in tokens:
            self.assertEqual(token["byte_offset"], offset)
            rebuilt.extend(raw[offset - 100:offset - 100 + token["byte_length"]])
            offset += token["byte_length"]
        self.assertEqual(bytes(rebuilt), raw)
        self.assertEqual(tokens[-1]["kind"], "binary_bytes")
        self.assertEqual(sum(t["kind"] == "group_open" for t in tokens), 1)

    def test_group_font_state_restored_and_metadata_separated(self):
        raw = rb"\f5 A{\footnote\pard\plain{\up #} ID}B\plain C"
        result = inventory.inspect_topic(raw, 0)
        visible = [t for t in result["tokens"] if t["kind"] == "text_bytes" and t["category"] == "visible"]
        self.assertEqual([t["font_id"] for t in visible], [5, 5, 4])
        self.assertEqual(result["issues"], [])
        self.assertEqual(result["groups"][0]["role"], "metadata_footnote")

    def test_literal_braces_and_object_commands_are_distinct(self):
        raw = rb"\f4 \{bmc bm1.wmf\} \{\-x\'7d \-"
        result = inventory.inspect_topic(raw, 50)
        self.assertEqual([o["resource"] for o in result["objects"]], ["bm1.wmf"])
        self.assertEqual(len(result["literal_brace_guards"]), 1)
        self.assertEqual(len(result["issues"]), 1)  # lone optional hyphen needs review
        self.assertEqual(result["groups"], [])

    def test_unknown_controls_retained_and_malformed_input_rejected(self):
        result = inventory.inspect_topic(rb"\mystery9 X", 0)
        self.assertIn("mystery", result["controls"])
        self.assertIn("unclassified_control", [i["reason"] for i in result["issues"]])
        self.assertIn("inherited_font_unknown", [i["reason"] for i in result["issues"]])
        for raw in (b"\\", rb"\'xz", rb"\bin9 abc", b"{x", b"x}"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                inventory.inspect_topic(raw, 0)

    @unittest.skipUnless((inventory.ROOT / inventory.RTF).exists(), "Private RTF unavailable")
    def test_private_inventory_reproduces_reviewed_summary(self):
        record, reports = inventory.build_inventory()
        self.assertEqual(record, json.loads(inventory.RECORD.read_bytes()))
        self.assertEqual(sum(r["accounted_bytes"] for r in reports), 149579)
        self.assertEqual(sum(len(r["objects"]) for r in reports), 21)
        self.assertEqual(sum(len(r["literal_brace_guards"]) for r in reports), 5)
        self.assertEqual([r["issues"] for r in reports], [[], []])
        self.assertFalse(record["verification"]["full_text_decoded"])


if __name__ == "__main__":
    unittest.main()
