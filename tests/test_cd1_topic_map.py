"""Focused native-address and real-source checks for the bounded pilot map."""

import json
import unittest

from tools import map_cd1_topic as topic_map


class PilotTopicMapTests(unittest.TestCase):
    def test_reference_and_generated_alias_share_native_hash(self):
        # Published record bytes in |CONTEXT are 71 82 68 0e (little endian).
        self.assertEqual(topic_map.context_hash("8802065"), 0x0E688271)
        self.assertEqual(topic_map.context_hash("2pes_r6"), 0x0E688271)
        self.assertNotEqual(topic_map.context_hash("8802066"), 0x0E688271)
        with self.assertRaises(ValueError):
            topic_map.context_hash("한글")

    def test_native_read_crosses_physical_header_and_logical_gap(self):
        # Keep the large real container base out of the synthetic fixture.
        from unittest.mock import patch

        raw = b"H" * 12 + b"a" * 4082 + b"BC" + b"H" * 12 + b"DE" + b"z" * 4082
        with patch.object(topic_map, "TOPIC", 0):
            self.assertEqual(topic_map.topic_read(raw, 12 + 4082, 4), b"BCDE")
            with self.assertRaisesRegex(ValueError, "Invalid native topic position"):
                topic_map.topic_read(raw, 12 + 4090, 1)
            with self.assertRaisesRegex(ValueError, "Truncated topic data"):
                topic_map.topic_read(raw[:4096], 12 + 4082, 4)

    def test_unsupported_layout_rejected(self):
        from unittest.mock import patch

        with patch.object(topic_map, "SYSTEM", 0):
            with self.assertRaisesRegex(ValueError, "uncompressed MVB"):
                topic_map.native_topics(bytes(12))

    @unittest.skipUnless(all((topic_map.ROOT / p).exists() for p in topic_map.SOURCES),
                         "Private pilot MVB/RTF are unavailable")
    def test_real_sources_reproduce_reviewed_map(self):
        actual = topic_map.build_map()
        self.assertEqual(actual, json.loads(topic_map.RECORD.read_text(encoding="utf-8")))
        # The empty native topic must survive mapping, without accidentally
        # merging the following article into the pilot's recovery scope.
        self.assertEqual(actual["recovery_scope_ordinals"], [148, 149])
        self.assertEqual(actual["topics"][2]["rtf"]["byte_length"], 9)
        self.assertFalse(actual["verification"]["article_completeness_verified"])


if __name__ == "__main__":
    unittest.main()
