"""Independent contract checks, using synthetic public data and a private pilot."""

from copy import deepcopy
import json
from pathlib import Path
import unittest
from urllib.parse import urljoin

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from maso_archive.reading_room import SCHEMA_PATH, catalog_for, validate_bundle, validate_manifest
from tools import build_reading_room_example as builder
from tools import map_cd1_blocks as block_tools
from tools.decode_cd1_paragraph import digest

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.bundle = json.loads((ROOT / "examples/reading-room-v1.json").read_bytes())

    def recatalog(self):
        self.bundle["catalog"] = catalog_for(self.bundle["issues"], self.bundle["articles"])

    def reject(self):
        with self.assertRaises((ValueError, ValidationError)):
            validate_bundle(self.bundle)

    def test_synthetic_example_supports_tree_mixed_content_and_unmatched_source(self):
        counts = validate_bundle(self.bundle)
        self.assertEqual(counts, {"issues": 1, "toc_entries": 2, "articles": 2, "media": 2,
                                  "sections": 2, "blocks": 5, "paragraphs": 7, "media_occurrences": 3})
        code = self.bundle["articles"][0]["sections"][1]["blocks"][2]
        self.assertEqual(code["paragraphs"][1]["runs"], [])
        self.assertEqual(code["paragraphs"][2]["runs"][-1]["text"], "  trailing  ")
        self.assertIsNone(self.bundle["articles"][1]["issue_id"])

    def test_each_runtime_document_validates_independently(self):
        schema = json.loads(SCHEMA_PATH.read_bytes())
        for kind, rows in (("catalog", [self.bundle["catalog"]]), ("issue", self.bundle["issues"]),
                           ("article", self.bundle["articles"]), ("media_index", [self.bundle["media"]])):
            validator = Draft202012Validator({**schema, "$ref": "#/$defs/" + kind})
            for row in rows:
                validator.validate(row)

    def test_unsupported_version_and_unknown_fields_are_rejected(self):
        original = deepcopy(self.bundle)
        self.bundle["schema_version"] = 2
        self.reject()
        self.bundle = deepcopy(original)
        self.bundle["articles"][0]["raw_rtf"] = "not runtime data"
        self.reject()
        self.bundle = deepcopy(original)
        self.bundle["articles"][0]["sections"][1]["blocks"][2]["table_cells"] = []
        self.reject()

    def test_unavailable_and_deferred_media_cannot_expose_display_assets(self):
        item = self.bundle["media"]["items"][1]
        item["asset"] = deepcopy(self.bundle["media"]["items"][0]["asset"])
        self.reject()
        item["asset"] = None
        item["problem_ids"] = []
        self.reject()
        for status in ("missing", "unsupported"):
            item.update(status=status, reason="source_not_available")
            validate_bundle(self.bundle)
        self.bundle["media"]["items"][0]["asset"] = None
        self.reject()

    def test_package_paths_work_under_a_base_url_and_reject_escapes(self):
        asset = self.bundle["media"]["items"][0]["asset"]
        self.assertEqual(urljoin("https://example.test/archive/data/", asset["path"]),
                         "https://example.test/archive/data/media/cd1/sample.bmp.png")
        for bad in ("/media/a.png", "../a.png", "media/../a.png", "media/cd1/../../a.png",
                    "https://example.test/a.png", "media/cd1/%2e%2e/a.png", "private/a.png",
                    "media/cd1/a.png?x=1", "media/cd1/a.png#fragment", "media/cd1\\a.png", "media/a.png\n"):
            with self.subTest(path=bad):
                asset["path"] = bad
                self.reject()

    def test_dangling_links_bad_tree_order_and_duplicate_identities_fail(self):
        original = deepcopy(self.bundle)
        self.bundle["issues"][0]["toc"][1]["parent_id"] = "absent"
        self.reject()
        self.bundle = deepcopy(original)
        self.bundle["articles"][0]["toc_entry_ids"] = []
        self.reject()
        self.bundle = deepcopy(original)
        self.bundle["articles"][0]["relationships"][0]["to_block"] = "absent"
        self.reject()
        self.bundle = deepcopy(original)
        self.bundle["articles"][0]["sections"][1]["blocks"][2]["paragraphs"][0]["runs"][1]["media_id"] = "absent"
        self.reject()
        self.bundle = deepcopy(original)
        self.bundle["articles"][0]["sections"][1]["blocks"][2]["paragraphs"][0]["runs"][1]["occurrence_id"] = "synthetic:occ3"
        self.reject()
        self.bundle = deepcopy(original)
        self.bundle["media"]["items"].append(deepcopy(self.bundle["media"]["items"][0]))
        self.reject()

    def test_heading_parent_and_spacing_semantics_are_checked(self):
        block = self.bundle["articles"][0]["sections"][1]["blocks"][0]
        block["heading_level"] = 2
        self.reject()
        block["heading_level"] = 1
        code = self.bundle["articles"][0]["sections"][1]["blocks"][2]
        code["parent_heading_id"] = None
        self.reject()
        code["parent_heading_id"] = block["id"]
        prose = self.bundle["articles"][0]["sections"][1]["blocks"][3]
        prose.update(type="spacing", layout="spacing")
        self.reject()

    def test_many_to_many_toc_links_and_metadata_only_articles(self):
        second = self.bundle["articles"][1]
        second["issue_id"] = self.bundle["issues"][0]["id"]
        entry = self.bundle["issues"][0]["toc"][1]
        entry["article_ids"].append(second["id"])
        second["toc_entry_ids"] = [entry["id"]]
        extra = deepcopy(entry)
        extra["id"] = self.bundle["issues"][0]["id"] + "-toc-0003"
        self.bundle["issues"][0]["toc"].append(extra)
        for article in self.bundle["articles"]:
            article["toc_entry_ids"].append(extra["id"])
        self.recatalog()
        validate_bundle(self.bundle)
        second["content_status"] = "available"
        self.recatalog()
        self.reject()  # An available article cannot silently have zero sections.

    def test_print_verification_is_independent_and_needs_report_metadata(self):
        article = self.bundle["articles"][0]
        article["extraction_status"] = "checked"
        validate_bundle(self.bundle)
        self.assertEqual(article["print_verification"]["status"], "pending")
        article["print_verification"]["status"] = "matched"
        self.reject()
        article["print_verification"].update(report_id="synthetic:print-review", pages_compared=[10])
        validate_bundle(self.bundle)  # Shape validation is not proof the review occurred.

    def test_manifest_inventory_paths_and_preview_ownership(self):
        documents = [{"kind": "catalog", "id": None, "path": "catalog.json"},
                     {"kind": "media_index", "id": None, "path": "media.json"}]
        for kind in ("issue", "article"):
            for n, row in enumerate(self.bundle[kind + "s"]):
                documents.append({"kind": kind, "id": row["id"], "path": f"{kind}s/{n}.json"})
        for document in documents:
            document.update(bytes=1, sha256="0" * 64)
        article = self.bundle["articles"][0]
        manifest = {"schema_version": 1, "kind": "package_manifest", "documents": documents,
                    "previews": [{"article_id": article["id"], "section_id": article["sections"][0]["id"],
                                  "path": "previews/intro.md", "bytes": 1, "sha256": "0" * 64}]}
        validate_manifest(manifest, self.bundle)
        for mutation in (lambda m: m["documents"].pop(),
                         lambda m: m["documents"].append(deepcopy(m["documents"][0])),
                         lambda m: m["documents"][0].update(path="../catalog.json"),
                         lambda m: m["documents"][0].update(path="other.json"),
                         lambda m: m["documents"][3].update(path="issues/0.json"),
                         lambda m: m["previews"][0].update(article_id=self.bundle["articles"][1]["id"]),
                         lambda m: m["previews"].append(deepcopy(m["previews"][0])),
                         lambda m: m["previews"][0].update(path="previews/a.md\n")):
            changed = deepcopy(manifest)
            mutation(changed)
            with self.assertRaises((ValueError, ValidationError)):
                validate_manifest(changed, self.bundle)

    def test_catalog_drift_page_ranges_and_asset_collisions_fail(self):
        original = deepcopy(self.bundle)
        self.bundle["catalog"]["articles"][0]["title"] = "Stale catalog title"
        self.reject()
        self.bundle = deepcopy(original)
        self.bundle["articles"][0]["pages"] = {"start": 10, "end": 9}
        self.recatalog()
        self.reject()
        self.bundle = deepcopy(original)
        extra = deepcopy(self.bundle["media"]["items"][0])
        extra["id"] = "synthetic:collision"
        extra["asset"]["sha256"] = "f" * 64
        self.bundle["media"]["items"].append(extra)
        self.reject()


@unittest.skipUnless(block_tools.SOURCE.exists() and (ROOT / "build/cd1-images/8802065/images.json").exists(),
                     "Private pilot sources unavailable")
class PilotContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record, cls.files = builder.build_example()
        cls.bundle = json.loads(cls.files["pilot.example.json"])
        cls.provenance = json.loads(cls.files["provenance.json"])
        cls.recovery = json.loads(block_tools.SOURCE.read_bytes())

    def test_private_example_matches_summary_and_reproduces(self):
        self.assertEqual(self.record, json.loads(builder.RECORD.read_bytes()))
        self.assertEqual((self.record, self.files), builder.build_example())
        self.assertEqual(self.record["counts"], {"issues": 1, "toc_entries": 39, "articles": 1, "media": 21,
                                               "sections": 2, "blocks": 271, "paragraphs": 323, "media_occurrences": 21})
        self.assertEqual(len(self.bundle["articles"][0]["relationships"]), 13)

    def test_every_source_run_paragraph_and_format_survives(self):
        media = {m["id"]: m for m in self.bundle["media"]["items"]}
        for topic, section in zip(self.recovery["topics"], self.bundle["articles"][0]["sections"]):
            exported = [p for b in section["blocks"] for p in b["paragraphs"]]
            self.assertEqual(len(exported), len(topic["paragraphs"]))
            reconstructed = []
            for original, paragraph in zip(topic["paragraphs"], exported):
                self.assertEqual(len(original["runs"]), len(paragraph["runs"]))
                plain = []
                for source, run in zip(original["runs"], paragraph["runs"]):
                    self.assertEqual(run["marks"], [label for key, label in (("b", "bold"), ("ul", "underline")) if source["format"][key]])
                    value = run["text"] if run["type"] == "text" else "[object:" + media[run["media_id"]]["source"]["resource"] + "]"
                    self.assertEqual(value, source["text"])
                    plain.append(value)
                self.assertEqual("".join(plain), original["text"])
                reconstructed.append("".join(plain) + "\n")
            filename = "introduction.txt" if topic["ordinal"] == 148 else "body.txt"
            self.assertEqual("".join(reconstructed).encode(), (ROOT / "build/cd1-text/8802065" / filename).read_bytes())

    def test_deferred_images_have_no_paths_and_available_assets_are_bound(self):
        media = self.bundle["media"]["items"]
        self.assertEqual([m["source"]["resource"] for m in media if m["status"] == "deferred"], ["bm54.wmf", "bm55.wmf"])
        self.assertTrue(all(m["asset"] is None for m in media if m["status"] == "deferred"))
        bindings = self.provenance["asset_bindings"]
        self.assertEqual(len(bindings), 19)
        for binding in bindings:
            raw = (ROOT / binding["source_path"]).read_bytes()
            self.assertEqual((len(raw), digest(raw)), (binding["bytes"], binding["sha256"]))
            self.assertEqual(next(m for m in media if m["id"] == binding["media_id"])["asset"]["path"], binding["package_path"])
        serialized = json.dumps(self.bundle)
        for path in ("private/", "build/", "/home/", "source_span", "viewer_compared", "rtf_byte_offset"):
            self.assertNotIn(path, serialized)
        article = self.bundle["articles"][0]
        self.assertEqual(article["print_verification"], {"status": "pending", "report_id": None, "pages_compared": []})
        self.assertIsNone(article["pages"]["end"])
        self.assertIsNone(self.bundle["issues"][0]["cover_media_id"])
        self.assertEqual(sum(e["link_status"] == "matched" for e in self.bundle["issues"][0]["toc"]), 1)


if __name__ == "__main__":
    unittest.main()
