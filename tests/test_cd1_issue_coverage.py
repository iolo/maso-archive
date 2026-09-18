"""Coverage must retain missing/conflicting metadata, not manufacture matches."""

import json
import unittest

from maso_archive.cd1_index import parse_index
from tools import audit_cd1_issue as audit
from tools.map_cd1_topic import context_hash


def toc_row(identifier="entry-1", title="Example", order=1, kind="article"):
    return {"id": identifier, "issue_id": audit.ISSUE, "order": order,
            "title_candidate": title, "kind_candidate": kind}


def index_rows(text):
    return parse_index("column.lst", (text + "\n@\n").encode("cp949"))[0]


class CoverageTests(unittest.TestCase):
    def test_every_occurrence_and_unmatched_toc_row_survives(self):
        toc = [toc_row(), toc_row("section", "Section", 2, "section"), toc_row("missing", "Missing", 3)]
        entries = index_rows("88.02 Example|8802001\n88.02 Example|8802001")
        report = audit.audit_issue(toc, entries, {}, {})
        self.assertEqual([r["entry"] for r in report["toc_entries"]], toc)
        self.assertEqual(report["counts"]["cd_index_occurrences"], 2)
        self.assertEqual(report["cd_references"][0]["native_status"], "not_found")
        self.assertEqual(report["toc_entries"][2]["relationship_status"], "not_index_matched")
        self.assertEqual(report["toc_entries"][1]["preparation_status"], "not_applicable_section")

    def test_reference_suffix_alone_never_matches(self):
        entries = index_rows("88.02 Different|8802001")
        row = {**toc_row(), "start_page_candidate": 1}
        report = audit.audit_issue([row], entries, {}, {})
        self.assertEqual(report["cd_references"][0]["relationship"]["status"], "unmatched")
        self.assertFalse(report["cd_references"][0]["relationship"]["page_suffix_used_to_match"])

    def test_issue_label_union_includes_named_targets_and_conflicts(self):
        entries = index_rows("88.02 Example|named_target\n88.03 Example|8802001\n88.02 Example|8803001\nExample|8802002")
        report = audit.audit_issue([toc_row()], entries, {}, {})
        refs = {r["reference"]: r for r in report["cd_references"]}
        self.assertEqual(set(refs), {"named_target", "8802001", "8803001", "8802002"})
        self.assertEqual(refs["named_target"]["relationship"]["status"], "supported_by_metadata")
        for ref in ("8802001", "8803001", "8802002"):
            self.assertEqual(refs[ref]["relationship"]["status"], "ambiguous")
        self.assertTrue(refs["8803001"]["attribution"]["conflict"])

    def test_duplicate_titles_and_multiple_references_stay_ambiguous(self):
        entries = index_rows("88.02 Example|8802001")
        report = audit.audit_issue([toc_row(), toc_row("entry-2", order=2)], entries, {}, {})
        self.assertEqual(report["cd_references"][0]["relationship"]["toc_candidate_ids"], ["entry-1", "entry-2"])
        self.assertEqual(report["cd_references"][0]["relationship"]["status"], "ambiguous")
        report = audit.audit_issue([toc_row()], index_rows("88.02 Example|8802001\n88.02 Example|8802002"), {}, {})
        self.assertEqual(report["counts"]["cd_relationships"], {"ambiguous": 2})

    def test_title_variant_remains_unresolved_and_rule_is_record_specific(self):
        entries = index_rows("88.02 터보 파스칼 한글 그래픽 툴|8802180\n88.02 터보 파스칼 한글 그래픽 툴|8802181")
        report = audit.audit_issue([toc_row(title="터보 파스칼 한글 그래픽스 툴")], entries, {}, {})
        self.assertEqual([r["relationship"]["status"] for r in report["cd_references"]], ["ambiguous", "unmatched"])

    def test_prepared_status_requires_supported_identity(self):
        entries = index_rows("88.02 Example|8802001")
        prepared = {"8802001": {"toc_entry_ids": ["wrong"]}}
        with self.assertRaisesRegex(ValueError, "Prepared article disagrees"):
            audit.audit_issue([toc_row()], entries, {}, prepared)
        prepared["8802001"]["toc_entry_ids"] = ["entry-1"]
        native = {"hash_hex": "synthetic", "topic_offset": 1}
        report = audit.audit_issue([toc_row()], entries, {context_hash("8802001"): native}, prepared)
        self.assertEqual(report["toc_entries"][0]["preparation_status"], "prepared")
        self.assertEqual(report["cd_references"][0]["native_context"], native)

    def test_duplicate_identity_or_source_order_is_rejected(self):
        for rows in ([toc_row(), toc_row(order=2)], [toc_row(order=2), toc_row("second", order=1)]):
            with self.assertRaises(ValueError):
                audit.audit_issue(rows, [], {}, {})

    def test_issue_snapshot_comparison_ignores_later_additions_only(self):
        original = b"## 88.02\n- Example = 1\n\n## 88.03\n- Next = 1\n"
        self.assertEqual(audit.issue_text(original), audit.issue_text(original + b"## 91.01\n- New = 1\n"))
        self.assertNotEqual(audit.issue_text(original), audit.issue_text(original.replace(b"Example", b"Changed")))
        with self.assertRaisesRegex(ValueError, "duplicated"):
            audit.issue_text(original + b"## 88.02\n")


@unittest.skipUnless((audit.ROOT / audit.PACKAGE / "manifest.json").exists(), "Private coverage inputs unavailable")
class ActualCoverageTests(unittest.TestCase):
    def test_reviewed_report_reproduces_and_accounts_for_both_populations(self):
        report = audit.build_report()
        self.assertEqual(report, json.loads(audit.RECORD.read_bytes()))
        self.assertEqual(report["counts"]["toc_entries"], 39)
        self.assertEqual(report["counts"]["cd_index_occurrences"], 11)
        self.assertEqual(report["counts"]["cd_references"], 5)
        self.assertEqual(report["counts"]["cd_preparation"], {"prepared": 2, "unprepared": 3})
        self.assertTrue(all(r["native_status"] == "resolved_hash" for r in report["cd_references"]))
        self.assertEqual(report["counts"]["toc_relationships"], {"matched": 4, "ambiguous": 1, "not_index_matched": 34})
        self.assertEqual(report["limits"]["new_article_bodies_recovered"], 0)


if __name__ == "__main__":
    unittest.main()
