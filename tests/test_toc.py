import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from maso_archive.toc import ImportFailure, parse_fields, run_import, validate_schema

ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class ImportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "TOC.md"
        self.output = self.root / "output"
        self.ids = self.root / "identities.json"

    def run_import(self, text=None, **kwargs):
        if text is not None:
            self.source.write_text(text, encoding="utf-8")
        return run_import(self.source, self.output, self.ids, start="1988-01", end="1988-01", **kwargs)

    def entries(self):
        return read_jsonl(self.output / "toc-entries.jsonl")

    def decisions(self, assignments=None, removed_ids=None, source_hash=None, new_lines=None):
        path = self.root / "decisions.json"
        path.write_text(json.dumps({
            "source_sha256": source_hash or hashlib.sha256(self.source.read_bytes()).hexdigest(),
            "assignments": assignments or {}, "removed_ids": removed_ids or [],
            "new_lines": new_lines or [],
        }), encoding="utf-8")
        return path

    def test_hierarchy_raw_evidence_and_uncertainty(self):
        source = ROOT / "tests/fixtures/toc.md"
        run_import(source, self.output, self.ids, start="1988-01", end="1988-02")
        entries = self.entries()
        lines = source.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(entries), 14)
        self.assertEqual(entries[0]["kind_candidate"], "unknown")
        self.assertIn("bundle_or_article", entries[0]["flags"])
        self.assertEqual(entries[1]["parent_id"], entries[0]["id"])
        self.assertIsNone(entries[1]["start_page_candidate"])
        self.assertEqual(entries[1]["page_candidates"], [])
        self.assertEqual(entries[2]["contributor_candidates"], ["김연구", "삼성 S/W 개발실"])
        self.assertEqual(entries[3]["section_path"], [entries[0]["id"], entries[2]["id"]])
        self.assertEqual(entries[4]["kind_candidate"], "section")
        self.assertIn("page_order_decrease", entries[5]["flags"])
        self.assertEqual(entries[6]["page_candidates"], [36, 63])
        self.assertIsNone(entries[6]["start_page_candidate"])
        self.assertEqual(entries[7]["page_candidates"], [89, 105, 112])
        self.assertIn("empty_byline", entries[8]["flags"])
        self.assertIsNone(entries[8]["byline_candidate"])
        self.assertEqual(entries[9]["title_candidate"], "CP/M / DOS / OS/2")
        self.assertIn("ambiguous_byline", entries[9]["flags"])
        self.assertNotEqual(entries[10]["id"], entries[11]["id"])
        self.assertEqual(entries[12]["kind_candidate"], "unknown")
        for entry in entries:
            self.assertEqual(entry["source"]["raw_line"], lines[entry["source"]["line_start"] - 1])
            self.assertIsNone(entry["end_page_candidate"])
        search = json.loads((self.output / "local-search.json").read_text())
        self.assertEqual(len(search), len(entries))
        self.assertTrue(any("cp/m" in row["search_text"] for row in search))
        self.assertTrue(all("source" not in row and "raw_text" not in row for row in search))

    def test_rerun_is_byte_identical(self):
        text = "## 88.01\n\n- 제목 / 저자 = 10\n- 다음 = 20\n"
        self.run_import(text)
        before = {p.name: p.read_bytes() for p in self.output.iterdir()}
        old_ids = self.ids.read_bytes()
        self.run_import()
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.output.iterdir()})
        self.assertEqual(old_ids, self.ids.read_bytes())

    def test_insertion_and_blank_lines_do_not_renumber(self):
        self.run_import("## 88.01\n- 기존 = 10\n- 다음 = 20\n")
        before = {e["raw_text"]: e["id"] for e in self.entries()}
        self.run_import("\n## 88.01\n\n- 새 글 = 5\n- 기존 = 10\n\n- 다음 = 20\n")
        after = {e["raw_text"]: e["id"] for e in self.entries()}
        for text, identifier in before.items():
            self.assertEqual(after[text], identifier)
        self.assertTrue(after["새 글 = 5"].endswith("0003"))

    def test_edited_title_requires_mapping_and_preserves_id(self):
        self.run_import("## 88.01\n- 오타 = 10\n")
        identifier = self.entries()[0]["id"]
        before = (self.output / "toc-entries.jsonl").read_bytes()
        old_ids = self.ids.read_bytes()
        with self.assertRaises(ImportFailure):
            self.run_import("## 88.01\n- 수정 = 10\n")
        self.assertEqual(before, (self.output / "toc-entries.jsonl").read_bytes())
        self.assertEqual(old_ids, self.ids.read_bytes())
        self.run_import(decisions_path=self.decisions({"2": identifier}))
        self.assertEqual(self.entries()[0]["id"], identifier)
        self.assertFalse((self.output / "failed-import-report.json").exists())

    def test_retired_identity_is_never_reallocated(self):
        self.run_import("## 88.01\n- 기존 = 10\n- 삭제 = 20\n")
        deleted = self.entries()[1]["id"]
        self.source.write_text("## 88.01\n- 기존 = 10\n", encoding="utf-8")
        self.run_import(decisions_path=self.decisions(removed_ids=[deleted]))
        self.run_import("## 88.01\n- 기존 = 10\n- 새 글 = 30\n")
        self.assertTrue(self.entries()[1]["id"].endswith("0003"))
        self.assertIn(deleted, json.loads(self.ids.read_text())["retired_ids"])

    def test_duplicate_entries_are_not_guessed_after_an_edit(self):
        self.run_import("## 88.01\n- 동일 = 10\n- 동일 = 10\n")
        identifiers = [e["id"] for e in self.entries()]
        self.run_import()  # Unchanged duplicate sequence is safe.
        self.assertEqual(identifiers, [e["id"] for e in self.entries()])
        with self.assertRaises(ImportFailure):
            self.run_import("## 88.01\n- 앞 = 5\n- 동일 = 10\n- 동일 = 10\n")
        self.run_import(decisions_path=self.decisions({"3": identifiers[0], "4": identifiers[1]}))
        self.assertEqual(identifiers, [e["id"] for e in self.entries()[1:]])

    def test_stale_identity_decisions_are_rejected(self):
        self.run_import("## 88.01\n- 글 = 10\n")
        with self.assertRaises(ImportFailure):
            self.run_import(decisions_path=self.decisions(source_hash="0" * 64))

    def test_explicit_new_duplicate_can_be_added(self):
        self.run_import("## 88.01\n- 동일 = 10\n")
        original = self.entries()[0]["id"]
        self.source.write_text("## 88.01\n- 동일 = 10\n- 동일 = 10\n", encoding="utf-8")
        self.run_import(decisions_path=self.decisions({"3": original}, new_lines=["2"]))
        self.assertEqual(self.entries()[1]["id"], original)
        self.assertTrue(self.entries()[0]["id"].endswith("0002"))

    def test_missing_registry_does_not_reset_identities(self):
        self.run_import("## 88.01\n- 글 = 10\n")
        self.ids.unlink()
        with self.assertRaises(ImportFailure):
            self.run_import()

    def test_corrupt_identity_allocator_is_rejected(self):
        self.run_import("## 88.01\n- 글 = 10\n")
        registry = json.loads(self.ids.read_text())
        registry["next_serial"]["maso-1988-01"] = 1
        self.ids.write_text(json.dumps(registry))
        with self.assertRaises(ImportFailure):
            self.run_import()

    def test_invalid_source_never_overwrites_successful_outputs(self):
        self.run_import("## 88.01\n- 정상 = 10\n")
        expected = (self.output / "toc-entries.jsonl").read_bytes()
        samples = [
            "## 88.01\n- 글 = 10\n## 88.01\n- 중복 = 20\n",
            "## 88.02\n- 글 = 10\n", "## 88.13\n- 글 = 10\n",
            "## 88.01\n설명으로 보이는 줄\n- 글 = 10\n",
            "## 88.01\n", "- 고아 = 10\n## 88.01\n- 글 = 10\n",
            "## 88.01\n-  = 10\n",
        ]
        for text in samples:
            with self.subTest(text=text), self.assertRaises(ImportFailure):
                self.run_import(text)
            self.assertEqual(expected, (self.output / "toc-entries.jsonl").read_bytes())

    def test_indentation_is_preserved_and_flagged(self):
        self.run_import("## 88.01\n- 부모\n    - 건너뜀 = 10\n - 이상 = 20\n")
        entries = self.entries()
        self.assertEqual(entries[1]["indent"], 4)
        self.assertEqual(entries[2]["indent"], 1)
        self.assertIn("suspicious_indentation", entries[1]["flags"])
        self.assertIn("suspicious_indentation", entries[2]["flags"])

    def test_page_ranges_and_literal_slashes_are_not_invented(self):
        self.assertEqual(parse_fields("CP/M과 S/W = 10")["title_candidate"], "CP/M과 S/W")
        fields = parse_fields("글 / 저자 = 10-15")
        self.assertEqual(fields["page_reference_raw"], "10-15")
        self.assertEqual(fields["page_candidates"], [])
        self.assertIn("unparsed_page_reference", fields["flags"])
        self.assertIsNone(fields["end_page_candidate"])

    def test_schema_rejects_unexpected_publication_fields(self):
        self.run_import("## 88.01\n- 글 = 10\n")
        entry = self.entries()[0]
        entry["full_text"] = "Must not be accepted by the TOC contract"
        with self.assertRaises(ValueError):
            validate_schema("entry", entry)

    def test_actual_toc_complete_and_traceable(self):
        source = ROOT / "TOC.md"
        report = run_import(source, self.output, self.ids)
        self.assertEqual(report["counts"]["issues"], 86)
        self.assertEqual(report["counts"]["entries"], 3811)
        self.assertEqual(report["errors"], [])
        lines = source.read_text(encoding="utf-8").splitlines()
        entries = self.entries()
        self.assertEqual(len({entry["id"] for entry in entries}), 3811)
        self.assertEqual(
            {entry["source"]["line_start"] for entry in entries},
            {i for i, line in enumerate(lines, 1) if line.lstrip().startswith("- ")},
        )
        by_id = {entry["id"]: entry for entry in entries}
        for entry in entries:
            self.assertEqual(entry["source"]["raw_line"], lines[entry["source"]["line_start"] - 1])
            if entry["parent_id"]:
                self.assertEqual(by_id[entry["parent_id"]]["issue_id"], entry["issue_id"])
        manifest = json.loads((self.output / "manifest.json").read_text())
        for name, details in manifest["outputs"].items():
            self.assertEqual(hashlib.sha256((self.output / name).read_bytes()).hexdigest(), details["sha256"])


if __name__ == "__main__":
    unittest.main()
