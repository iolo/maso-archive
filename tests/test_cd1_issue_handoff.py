"""Issue coverage reconciliation, preserved evidence, and static-base relocation."""

from copy import deepcopy
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import tempfile
from threading import Thread
import unittest
from urllib.parse import urljoin
from urllib.request import urlopen

from maso_archive.reading_room_package import file_record, load_package
from tools import prepare_cd1_issue as issue
from tools.build_reading_room_package import write_package


class MetadataComparisonTests(unittest.TestCase):
    def test_only_source_identifier_may_change(self):
        old = [{"id": "entry-1", "issue_id": issue.ISSUE, "title": "Example", "pages": [12],
                "source": {"id": "old-document", "line_start": 5}}]
        new = deepcopy(old)
        new[0]["source"]["id"] = "expanded-document"
        self.assertEqual(issue.compare_toc(old, new), [{"toc_entry_id": "entry-1", "field": "source.id",
                                                      "before": "old-document", "after": "expanded-document"}])
        for key, value in (("title", "Changed"), ("pages", [13]), ("id", "entry-2")):
            changed = deepcopy(new)
            changed[0][key] = value
            with self.assertRaises(ValueError):
                issue.compare_toc(old, changed)
        new[0]["source"]["line_start"] = 6
        with self.assertRaises(ValueError):
            issue.compare_toc(old, new)


@unittest.skipUnless((issue.PREVIOUS / "manifest.json").exists(), "Private prepared issue inputs unavailable")
class IssueHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record, cls.coverage, cls.files = issue.build_handoff()
        cls.provenance = json.loads(cls.files["provenance.json"])
        cls.bundle, _, _ = load_package(issue.PREVIOUS)

    def test_reviewed_records_and_rebuild_are_identical(self):
        self.assertEqual(self.record, json.loads(issue.RECORD.read_bytes()))
        self.assertEqual(self.coverage, json.loads(issue.COVERAGE.read_bytes()))
        self.assertEqual((self.record, self.coverage, self.files), issue.build_handoff())
        self.assertEqual(self.record["schema"]["sha256"], "2a160d646c4a92552fcc4647216348c14ee74c357a375412f23fed54bffc6f68")

    def test_every_toc_entry_and_index_occurrence_has_an_explicit_status(self):
        counts = self.coverage["counts"]
        self.assertEqual(counts["toc_preparation"], {"not_applicable_section": 4, "prepared": 5, "unprepared": 30})
        self.assertEqual(counts["cd_preparation"], {"prepared": 5})
        refs = self.coverage["cd_references"]
        self.assertEqual(len(refs), 5)
        occurrences = [o["id"] for r in refs for o in r["occurrences"]]
        self.assertEqual(len(occurrences), 11)
        self.assertEqual(len(set(occurrences)), 11)
        for row in self.coverage["toc_entries"]:
            if row["entry"]["kind_candidate"] == "section":
                self.assertEqual(row["content_availability"], "not_applicable_section")
            elif row["matched_references"]:
                self.assertEqual(row["content_availability"], "prepared")
            else:
                self.assertEqual(row["content_availability"], "not_prepared_no_index_match")
        self.assertEqual(self.coverage["limits"]["unindexed_native_targets"], "not_attributed")
        self.assertEqual(self.coverage["limits"]["printed_issue_completeness"], "unverified")

    def test_historical_audit_survives_and_new_match_has_later_evidence(self):
        old = json.loads(issue.audit.RECORD.read_bytes())
        self.assertEqual(old["counts"]["cd_preparation"], {"prepared": 2, "unprepared": 3})
        before = next(r for r in old["cd_references"] if r["reference"] == "8802180")
        after = next(r for r in self.coverage["cd_references"] if r["reference"] == "8802180")
        self.assertEqual(before["relationship"]["status"], "ambiguous")
        self.assertEqual(after["relationship"]["basis"], "reviewed_native_body_title_and_page_agreement")
        self.assertEqual(after["relationship"]["status"], "supported_by_metadata")
        self.assertFalse(after["relationship"]["page_suffix_used_to_match"])
        comparison = self.coverage["metadata_comparison"]
        self.assertEqual(len(comparison["entry_differences"]), 39)
        self.assertTrue(all(d["field"] == "source.id" for d in comparison["entry_differences"]))
        self.assertEqual(comparison["runtime_metadata_changes"], [])

    def test_all_runtime_bytes_and_five_article_evidence_documents_are_preserved(self):
        for record in self.record["outputs"]:
            self.assertEqual(self.files["content/" + record["path"]], (issue.PREVIOUS / record["path"]).read_bytes())
        for ref, _, base in issue.PREPARATIONS:
            self.assertEqual(self.provenance["article_evidence"][ref], json.loads((issue.ROOT / base / "provenance.json").read_bytes()))
        self.assertEqual(self.record["counts"]["files"], 48)
        self.assertEqual(self.record["counts"]["assets"], 29)
        self.assertEqual(self.record["counts"]["paragraphs"], 2518)
        self.assertEqual(self.coverage["catalog_search_fields"], ["title", "byline", "issue_id"])

    def test_missing_resolved_or_misplaced_review_evidence_is_rejected(self):
        reviews = self.coverage["review_records"]
        self.assertEqual(sum(len(r["issues"]) for r in reviews["deferred_media"]), 4)
        self.assertEqual(len(reviews["text_reviews"]), 1)
        issue.check_reviews(self.bundle, reviews["deferred_media"], reviews["text_reviews"])
        with self.assertRaisesRegex(ValueError, "text review record missing"):
            issue.check_reviews(self.bundle, reviews["deferred_media"], [])
        missing = deepcopy(reviews["deferred_media"])
        missing[0]["issues"].pop()
        with self.assertRaisesRegex(ValueError, "lacks a review"):
            issue.check_reviews(self.bundle, missing, reviews["text_reviews"])
        resolved = deepcopy(reviews["deferred_media"])
        resolved[0]["issues"][0]["resolved"] = True
        with self.assertRaisesRegex(ValueError, "disposition changed"):
            issue.check_reviews(self.bundle, resolved, reviews["text_reviews"])
        changed = deepcopy(reviews["text_reviews"])
        changed[0]["paragraph_ordinal"] = 9999
        with self.assertRaisesRegex(ValueError, "target/status changed"):
            issue.check_reviews(self.bundle, reviews["deferred_media"], changed)

    def test_failed_staging_preserves_previous_handoff(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "issue"
            write_package(root, self.files)
            before = (root / "content/manifest.json").read_bytes()
            broken = dict(self.files)
            broken["content/catalog.json"] = b"{}\n"
            with self.assertRaisesRegex(ValueError, "Package bytes mismatch"):
                write_package(root, broken)
            self.assertEqual((root / "content/manifest.json").read_bytes(), before)
            self.assertEqual(load_package(root / "content")[2], self.record["counts"])

    def test_every_runtime_file_loads_under_two_nested_http_base_urls(self):
        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for prefix in ("archive/data", "reading-room/cd1/1988-02"):
                write_package(root / prefix, self.files)
                self.assertEqual(load_package(root / prefix / "content")[2], self.record["counts"])
            server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=temporary))
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                for prefix in ("archive/data", "reading-room/cd1/1988-02"):
                    base = f"http://127.0.0.1:{server.server_port}/{prefix}/content/"
                    for record in self.record["outputs"]:
                        with urlopen(urljoin(base, record["path"]), timeout=5) as response:
                            self.assertEqual(file_record(record["path"], response.read()), record)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
