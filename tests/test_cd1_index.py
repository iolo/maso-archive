from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from maso_archive.cd1_index import INDEX_NAMES, parse_index, reference_fields, run_import
from maso_archive.toc import ImportFailure

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / "private/cd1-probe"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class IndexTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "raw"
        self.source.mkdir()
        self.manifest = self.root / "manifest.json"
        self.output = self.root / "output"
        contents = {
            "column.lst": "분류|* \r\n  소분류|*\r\n    88.02 예제 제목|8802065\r\n    93.04 팁|9304410a\r\n  처음 화면|mscdmenu\r\n@\r\n",
            "language.lst": "언어|*\n  88.02 제목의 다른 표기|8802065\n\n@\n",
            "panecmds.lst": "도구|*\n  88.02 반복 제목|8802065\n  88.02 반복 제목|8802065\n  93.11 부록|9311000\n@",
        }
        for name, text in contents.items():
            (self.source / name).write_bytes(text.encode("cp949"))
        self.refresh_manifest()

    def refresh_manifest(self):
        self.manifest.write_text(json.dumps({
            "source_sha256": "0" * 64,
            "files": [{"path": f"raw/{name}", "bytes": (self.source / name).stat().st_size,
                       "sha256": hashlib.sha256((self.source / name).read_bytes()).hexdigest()}
                      for name in INDEX_NAMES],
        }), encoding="utf-8")

    def run_import(self):
        return run_import(self.source, self.manifest, self.output)

    def test_expanded_target_boundaries_and_unknown_dates(self):
        for reference, expected in [("8310001", False), ("8311001", True),
                                    ("9101001", True), ("9304410a", True),
                                    ("9401001", True), ("9512001", True),
                                    ("9601001", False), ("9513001", None), ("mscdmenu", None)]:
            with self.subTest(reference=reference):
                self.assertIs(reference_fields(reference)["in_target_period_candidate"], expected)

    def test_preserves_occurrences_hierarchy_native_references_and_bytes(self):
        report = self.run_import()
        entries = read_jsonl(self.output / "entries.jsonl")
        groups = {row["reference"]: row for row in read_jsonl(self.output / "references.jsonl")}
        self.assertEqual(report["counts"]["entries"], 14)
        self.assertEqual(report["counts"]["blank_lines"], 1)
        self.assertEqual(report["counts"]["by_kind"]["terminator"], 3)
        self.assertEqual(report["baseline_comparison"]["status"], "not_applicable")
        self.assertEqual(len(groups["8802065"]["occurrence_ids"]), 4)
        self.assertEqual(len(groups["8802065"]["title_variants"]), 3)
        self.assertEqual(groups["9304410a"]["reference_kind"], "suffixed")
        self.assertEqual(groups["mscdmenu"]["reference_kind"], "named")
        self.assertIsNone(groups["mscdmenu"]["issue_candidate"])
        self.assertEqual(groups["9311000"]["reference"], "9311000")
        sample = entries[2]
        self.assertEqual(sample["reference"], "8802065")
        self.assertEqual(sample["label"], "88.02 예제 제목")
        self.assertEqual(sample["title"], "예제 제목")
        self.assertEqual(sample["display_issue"], "1988-02")
        self.assertEqual([p["label"] for p in sample["category_path"]], ["분류", "소분류"])
        self.assertEqual(sample["parent_id"], entries[1]["id"])
        self.assertEqual(entries[0]["reference_raw"], "* ")
        self.assertEqual(report["counts"]["by_diagnostic"]["reference_padding"], 1)
        self.assertEqual(report["counts"]["by_diagnostic"]["zero_page_component"], 1)
        for entry in entries:
            source = entry["source"]
            raw = (self.source / source["name"]).read_bytes()
            chunk = raw[source["byte_offset"]:source["byte_offset"] + source["byte_length"]]
            self.assertEqual(chunk.rstrip(b"\r\n").decode("cp949"), entry["raw_line"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), source["sha256"])

    def test_syntax_exceptions_are_preserved_and_reported(self):
        raw = (
            "분류|*\n    구분자 없음\n  |8802065\n  둘|여럿|8802065\n"
            "  88.02 날짜 충돌|8902065\n  88.13 잘못된 달|8813065\n"
            "@\n  뒤에 오는 행|8802066\n@\n"
        ).encode("cp949")
        entries, source, diagnostics = parse_index("column.lst", raw)
        self.assertEqual(len(entries), 9)
        self.assertEqual(source["nonblank_lines"], 9)
        self.assertEqual([e["kind"] for e in entries[1:4]], ["unparsed"] * 3)
        codes = {d["code"] for d in diagnostics}
        self.assertTrue({"suspicious_indentation", "invalid_separator_count", "empty_label_or_reference",
                         "label_reference_month_mismatch", "invalid_reference_month", "invalid_label_month",
                         "content_after_terminator", "terminator_count"}.issubset(codes))

    def test_invalid_cp949_is_rejected_without_replacing_success(self):
        self.run_import()
        before = {p.name: p.read_bytes() for p in self.output.iterdir()}
        (self.source / "column.lst").write_bytes(b"\x81")
        self.refresh_manifest()  # Correct hash, deliberately invalid source encoding.
        with self.assertRaises(ImportFailure):
            self.run_import()
        report = json.loads((self.output / "failed-import-report.json").read_text())
        self.assertEqual(report["errors"][0]["code"], "invalid_cp949")
        for name, content in before.items():
            self.assertEqual((self.output / name).read_bytes(), content)

    def test_manifest_mismatch_missing_record_and_duplicate_record_reject(self):
        original = self.manifest.read_bytes()
        for change in ["hash", "size", "missing", "duplicate"]:
            with self.subTest(change=change):
                manifest = json.loads(original)
                if change == "hash":
                    manifest["files"][0]["sha256"] = "0" * 64
                elif change == "size":
                    manifest["files"][0]["bytes"] += 1
                elif change == "missing":
                    manifest["files"].pop(0)
                else:
                    manifest["files"].append(manifest["files"][0])
                self.manifest.write_text(json.dumps(manifest))
                with self.assertRaises(ImportFailure):
                    self.run_import()
                self.assertFalse((self.output / "entries.jsonl").exists())

    def test_missing_source_or_invalid_manifest_has_actionable_report(self):
        (self.source / "language.lst").unlink()
        with self.assertRaises(ImportFailure):
            self.run_import()
        self.assertEqual(json.loads((self.output / "failed-import-report.json").read_text())["errors"][0]["code"], "input_error")
        self.manifest.write_text("[]")
        with self.assertRaises(ImportFailure):
            self.run_import()
        self.assertIn("files array", json.loads((self.output / "failed-import-report.json").read_text())["errors"][0]["message"])

    def test_rerun_is_identical_and_manifest_hashes_match(self):
        self.run_import()
        before = {p.name: p.read_bytes() for p in self.output.iterdir()}
        self.run_import()
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.output.iterdir()})
        manifest = json.loads((self.output / "manifest.json").read_text())
        self.assertEqual(manifest["target_period"], {"start": "1983-11", "end": "1995-12"})
        for name, details in manifest["outputs"].items():
            raw = (self.output / name).read_bytes()
            self.assertEqual(details["sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(details["bytes"], len(raw))

    def test_cli_only_needs_index_files_and_manifest(self):
        command = [sys.executable, "-m", "maso_archive", "import-cd1-index",
                   "--source-dir", str(self.source), "--manifest", str(self.manifest), "--output", str(self.output)]
        env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
        result = subprocess.run(command, cwd=self.root, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("14 index entries", result.stdout)
        (self.source / "column.lst").write_bytes(b"changed")
        result = subprocess.run(command, cwd=self.root, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("failed-import-report.json", result.stderr)
        self.refresh_manifest()
        self.run_import()
        self.assertFalse((self.output / "failed-import-report.json").exists())

    @unittest.skipUnless((PRIVATE / "manifest.json").exists() and all((PRIVATE / "raw" / n).exists() for n in INDEX_NAMES),
                         "Private CD1 indexes are not available in this checkout")
    def test_actual_indexes_account_for_every_line_and_reference(self):
        report = run_import(PRIVATE / "raw", PRIVATE / "manifest.json", self.output)
        self.assertEqual(report["baseline_comparison"]["status"], "matched")
        self.assertEqual(report["counts"]["numeric_references"], 1038)
        self.assertEqual(report["counts"]["target_numeric_references"], 1038)
        self.assertEqual(report["target_period"], {"start": "1983-11", "end": "1995-12"})
        self.assertEqual(report["counts"]["entries"], 3032)
        entries = read_jsonl(self.output / "entries.jsonl")
        groups = read_jsonl(self.output / "references.jsonl")
        self.assertEqual(sum(g["reference_kind"] == "numeric" and "1988-01" <= g["issue_candidate"] <= "1990-12"
                             for g in groups), 360)
        self.assertEqual(Counter(i for g in groups for i in g["occurrence_ids"]),
                         Counter(e["id"] for e in entries if e["kind"] == "reference"))
        by_id = {entry["id"]: entry for entry in entries}
        for name in INDEX_NAMES:
            lines = (PRIVATE / "raw" / name).read_bytes().decode("cp949").splitlines()
            rows = [entry for entry in entries if entry["source"]["name"] == name]
            self.assertEqual([e["source"]["line"] for e in rows], [i for i, line in enumerate(lines, 1) if line.strip()])
            for entry in rows:
                self.assertEqual(entry["raw_line"], lines[entry["source"]["line"] - 1])
                if entry["parent_id"]:
                    self.assertEqual(by_id[entry["parent_id"]]["source"]["name"], name)
        sample = next(g for g in groups if g["reference"] == "8802065")
        self.assertEqual(len(sample["occurrence_ids"]), 2)
        self.assertEqual({by_id[i]["source"]["name"] for i in sample["occurrence_ids"]}, {"column.lst", "panecmds.lst"})


if __name__ == "__main__":
    unittest.main()
