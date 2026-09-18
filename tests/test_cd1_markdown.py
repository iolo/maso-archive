"""Markdown content preservation, syntax safety, and private pilot regression."""

from copy import deepcopy
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

try:
    from markdown_it import MarkdownIt
except ImportError:
    MarkdownIt = None

from tools import render_cd1_markdown as renderer
from tools import map_cd1_blocks as mapper
from tools.recover_cd1_text import topic_text


class VisibleText(HTMLParser):
    """Collect source content inside rendered paragraphs, headings, or code."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.inside = False
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag in ("p", "pre", "h1", "h2", "h3", "h4"):
            self.inside = True

    def handle_endtag(self, tag):
        if tag in ("p", "pre", "h1", "h2", "h3", "h4"):
            self.inside = False

    def handle_data(self, data):
        if self.inside:
            self.text.append(data)


class MarkdownSafetyTests(unittest.TestCase):
    def test_fences_exceed_every_source_backtick_run(self):
        text = "  code\n\n```\n````` literal\n trailing  \n"
        rendered = renderer.fenced(text)
        self.assertEqual(rendered, "``````\n" + text + "``````\n")

    def test_inline_markup_escapes_source_and_retains_styles(self):
        paragraph = {"runs": [{"kind": "text", "text": "  *a* <x> & _b_",
                               "format": {"b": True, "ul": True}}]}
        self.assertEqual(renderer.inline(paragraph),
                         "<strong><u>&#32;&#32;\\*a\\* &lt;x&gt; &amp; \\_b\\_</u></strong>")

    def test_changed_sources_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.json"
            source.write_text("{}", encoding="utf-8")
            with patch.object(mapper, "SOURCE", source), self.assertRaisesRegex(ValueError, "Changed structured recovery"):
                renderer.build_preview()
            if mapper.SOURCE.exists():
                with patch.object(renderer, "BLOCKS", source), self.assertRaisesRegex(ValueError, "Changed block map"):
                    renderer.build_preview()

    @unittest.skipUnless(MarkdownIt, "Optional markdown-it-py renderer unavailable")
    def test_adversarial_source_renders_as_literal_text(self):
        md = MarkdownIt("commonmark", {"html": True})
        samples = ["# heading", "1. item", "> quote", "---", "[x](https://example.org)",
                   "<script>alert('x')</script>", "&copy; &#32;", "    indent", "a_b **c** `d`",
                   "|a|b|", "한글*English", "<a id=\"injected\">", "\\backslash!  "]
        for text in samples:
            with self.subTest(text=text):
                for bold in (False, True):
                    fragment = renderer.inline({"runs": [{"kind": "text", "text": text,
                                                          "format": {"b": bold, "ul": bold}}]})
                    rendered = md.render(fragment)
                    parsed = VisibleText()
                    parsed.feed(rendered)
                    self.assertEqual("".join(parsed.text), text)
                    self.assertNotIn("<script>", rendered)
                    self.assertNotIn("<a ", rendered)


@unittest.skipUnless(mapper.SOURCE.exists() and renderer.BLOCKS.exists(), "Private pilot inputs unavailable")
class PilotMarkdownTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.article = json.loads(mapper.SOURCE.read_bytes())
        cls.block_map = json.loads(renderer.BLOCKS.read_bytes())
        cls.record, cls.files = renderer.build_preview()
        cls.locations = json.loads(cls.files["provenance.json"])["blocks"]

    def test_reviewed_outputs_are_deterministic_and_complete(self):
        self.assertEqual(self.record, json.loads(renderer.RECORD.read_bytes()))
        self.assertEqual((self.record, self.files), renderer.build_preview())
        self.assertEqual(len(self.locations), 271)
        self.assertEqual([l["block_id"] for l in self.locations], [b["id"] for b in self.block_map["blocks"]])
        objects = [o["resource"] for l in self.locations for o in l["object_refs"]]
        self.assertEqual(len(objects), 21)
        for filename in ("introduction.md", "body.md"):
            raw = self.files[filename]
            actual_objects = []
            for loc in (l for l in self.locations if l["path"] == filename):
                self.assertIn(f'id="{renderer.anchor(loc["block_id"])}"'.encode(),
                              raw[loc["byte_offset"]:loc["byte_offset"] + loc["byte_length"]])
                content = raw[loc["content_byte_offset"]:loc["content_byte_offset"] + loc["content_byte_length"]].decode()
                # Outside fences, object marker punctuation is escaped as prose.
                actual_objects.extend(re.findall(r"\[object:([^\]]+)\]", content.replace("\\", "")))
            expected = [o["resource"] for l in self.locations if l["path"] == filename for o in l["object_refs"]]
            self.assertEqual(actual_objects, expected)

    def test_code_spacing_caption_links_and_unresolved_content(self):
        topics = {t["ordinal"]: t for t in self.article["topics"]}
        for block, loc in zip(self.block_map["blocks"], self.locations):
            fragment = self.files[loc["path"]][loc["content_byte_offset"]:loc["content_byte_offset"] + loc["content_byte_length"]].decode()
            if block["kind"] == "code":
                ps = [topics[block["topic_ordinal"]]["paragraphs"][m["paragraph_ordinal"] - 1] for m in block["members"]]
                lines = fragment.splitlines(keepends=True)
                self.assertEqual("".join(lines[1:-1]), topic_text({"paragraphs": ps}))
                self.assertEqual(lines[0], lines[-1])
            if block["kind"] == "heading":
                self.assertTrue(fragment.startswith("#" * (block["heading_level"] + 1) + " "))
        body = self.files["body.md"].decode()
        for relation in self.block_map["relationships"]:
            self.assertEqual(body.count(f'[View captioned content](#{renderer.anchor(relation["to_block"])})'), 1)
        self.assertIn("Mixed text/object example", body)
        self.assertIn("Unresolved attachment", body)
        self.assertIn("cell structure has not been reconstructed", body)
        self.assertNotIn("![", body)

    def test_inconsistent_runs_or_missing_blocks_fail_before_rendering(self):
        changed = deepcopy(self.article)
        changed["topics"][1]["paragraphs"][187]["runs"][0]["text"] += " changed"
        with self.assertRaisesRegex(ValueError, "Paragraph/run text mismatch"):
            renderer.render(changed, self.block_map)
        changed_map = deepcopy(self.block_map)
        changed_map["blocks"].pop()
        with self.assertRaisesRegex(ValueError, "Missing, duplicated, or reordered paragraph"):
            renderer.render(self.article, changed_map)

    @unittest.skipUnless(MarkdownIt, "Optional markdown-it-py renderer unavailable")
    def test_independent_markdown_parser_preserves_all_block_text(self):
        md = MarkdownIt("commonmark", {"html": True})
        topics = {t["ordinal"]: t for t in self.article["topics"]}
        documents = "\n".join(self.files[name].decode() for name in ("introduction.md", "body.md"))
        tokens = md.parse(documents)
        self.assertEqual(sum(t.type == "fence" for t in tokens), 17)
        self.assertEqual([t.tag for t in tokens if t.type == "heading_open"].count("h1"), 2)
        for level, count in (("h2", 3), ("h3", 7), ("h4", 18)):
            self.assertEqual([t.tag for t in tokens if t.type == "heading_open"].count(level), count)
        rendered = md.render(documents)
        ids = re.findall(r'<a id="([^"]+)"', rendered)
        targets = re.findall(r'<a href="#([^"]+)"', rendered)
        self.assertEqual(len(ids), 271)
        self.assertEqual(len(set(ids)), 271)
        self.assertEqual(len(targets), 13)
        self.assertTrue(set(targets) <= set(ids))
        for block, loc in zip(self.block_map["blocks"], self.locations):
            with self.subTest(block=block["id"]):
                ps = [topics[block["topic_ordinal"]]["paragraphs"][m["paragraph_ordinal"] - 1] for m in block["members"]]
                projection = topic_text({"paragraphs": ps})
                fragment = self.files[loc["path"]][loc["content_byte_offset"]:loc["content_byte_offset"] + loc["content_byte_length"]].decode()
                if block["kind"] == "spacing":
                    self.assertEqual(fragment, projection)
                    continue
                parsed = VisibleText()
                parsed.feed(md.render(fragment))
                expected = projection if block["kind"] == "code" else projection[:-1]
                self.assertEqual("".join(parsed.text), expected)


if __name__ == "__main__":
    unittest.main()
