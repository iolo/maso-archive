"""Small synthetic text fixtures; publisher paragraph stays outside Git."""

import json
import unittest

from tools import decode_cd1_paragraph as sample


class ParagraphTests(unittest.TestCase):
    def decode(self, payload):
        return sample.decode_sample(sample.PREFIX + payload + sample.TERMINATOR)

    def test_korean_bytes_ascii_punctuation_and_spacing(self):
        text, encoded = self.decode(rb"PC \'b0\'a1(UNIX)?  \'b3\'aa." + b"\r\n")
        self.assertEqual(text, "PC 가(UNIX)?  나.")
        self.assertEqual(encoded, text.encode("cp949"))

    def test_escaped_syntax_is_text_not_reparsed_as_controls(self):
        text, _ = self.decode(rb"\{x\} \\ \'5cpar")
        self.assertEqual(text, "{x} \\ \\par")

    def test_incomplete_or_invalid_multibyte_sequences_fail(self):
        for payload in (rb"\'b0", rb"\'ff\'ff", rb"\'b0 A"):
            with self.subTest(payload=payload), self.assertRaises(UnicodeError):
                self.decode(payload)

    def test_unsupported_controls_and_groups_are_not_silently_dropped(self):
        for payload in (rb"\'zz", rb"\'a", rb"\f2 x", rb"{\v hidden}",
                        rb"\u44032?", rb"\tab x", rb"\~", rb"\par second", b"\x81"):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                self.decode(payload)
        with self.assertRaises(ValueError):
            sample.decode_sample(b"inherited font text\\par ")

    @unittest.skipUnless((sample.ROOT / sample.RTF).exists(), "Private RTF unavailable")
    def test_real_sample_reproduces_metadata_without_neighbor_content(self):
        record, artifacts = sample.build_sample()
        self.assertEqual(record, json.loads(sample.RECORD.read_bytes()))
        self.assertEqual(record["text"]["characters_excluding_terminal_lf"], 182)
        self.assertEqual(artifacts["paragraph.txt"].count(b"\n"), 1)
        self.assertFalse(record["verification"]["viewer_compared"])


if __name__ == "__main__":
    unittest.main()
