"""Image provenance, exact occurrence coverage, and honest conversion status."""

from copy import deepcopy
import json
from pathlib import Path
import struct
import tempfile
import unittest

from tools import map_cd1_images as images
from tools import map_cd1_blocks as blocks
from tools.decode_cd1_paragraph import digest


class ImageMappingTests(unittest.TestCase):
    def test_manifest_rejects_changed_missing_duplicate_and_unsafe_resources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = b"bitmap source"
            (root / "sample.dib").write_bytes(raw)
            entry = {"path": "raw/sample.dib", "bytes": len(raw), "sha256": digest(raw)}
            manifest = {"files": [entry]}
            self.assertEqual(images.checked_source("sample.dib", manifest, root), raw)
            for entries in ([], [entry, entry], [{**entry, "sha256": "0" * 64}]):
                with self.subTest(entries=entries), self.assertRaises(ValueError):
                    images.checked_source("sample.dib", {"files": entries}, root)
            with self.assertRaises(ValueError):
                images.checked_source("../sample.dib", manifest, root)
            (root / "sample.dib").unlink()
            with self.assertRaises(FileNotFoundError):
                images.checked_source("sample.dib", manifest, root)

    def test_svg_definitions_do_not_count_as_visible_content(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.svg"
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="2mm" height="4mm"><defs><pattern><path/></pattern></defs></svg>')
            self.assertEqual(images.inspect_svg(path)["drawing_elements"], 0)
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg"><g><text style="font-family:Times New Roman;">2</text></g></svg>')
            self.assertEqual(images.inspect_svg(path)["drawing_elements"], 1)
            self.assertEqual(images.inspect_svg(path)["font_families"], ["Times New Roman"])

    def test_failed_converter_never_yields_a_success_status(self):
        raw = bytes.fromhex("d7cdc69a") + b"\0\0" + struct.pack("<hhhhH", 0, 0, 100, 200, 1000) + bytes(24)
        with tempfile.TemporaryDirectory() as directory:
            def failed(args):
                return {"argv": args, "exit_code": 1, "stdout": "", "stderr": "unsupported"}
            item = images.convert_resource("sample.wmf", raw, Path(directory), failed)
            self.assertEqual(item["status"], "conversion_failed")
            self.assertEqual(item["derivatives"], [])
            self.assertFalse(item["viewer_compared"])


@unittest.skipUnless((images.OUTPUT / "images.json").exists() and blocks.SOURCE.exists(),
                     "Private pilot image outputs unavailable")
class PilotImageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.article = json.loads(blocks.SOURCE.read_bytes())
        cls.block_map = json.loads((blocks.OUTPUT / "blocks.json").read_bytes())
        cls.result = json.loads((images.OUTPUT / "images.json").read_bytes())

    def test_exact_occurrence_order_and_duplicate_content_are_preserved(self):
        refs = images.occurrences(self.article, self.block_map)
        self.assertEqual(refs, self.result["occurrences"])
        self.assertEqual(len(refs), 21)
        self.assertEqual(len({r["id"] for r in refs}), 21)
        self.assertEqual(self.result["counts"]["distinct_source_hashes"], 16)
        self.assertEqual(self.result["duplicate_source_groups"], [[f"bm{n}.wmf" for n in (44, 45, 47, 49, 51, 53)]])
        changed = deepcopy(self.block_map)
        next(b for b in changed["blocks"] if b["object_refs"])["object_refs"].clear()
        with self.assertRaisesRegex(ValueError, "Object coverage/order changed"):
            images.occurrences(self.article, changed)

    def test_all_sources_derivatives_and_review_summary_match_hashes(self):
        manifest = json.loads(images.MANIFEST.read_bytes())
        record = json.loads(images.RECORD.read_bytes())
        self.assertEqual(record["counts"], self.result["counts"])
        for source in self.result["sources"]:
            self.assertEqual(digest((images.ROOT / source["path"]).read_bytes()), source["sha256"])
        for item in self.result["resources"]:
            raw = images.checked_source(item["resource"], manifest)
            self.assertEqual(digest(raw), item["source"]["sha256"])
            for derivative in item["derivatives"]:
                raw = (images.OUTPUT / derivative["path"]).read_bytes()
                self.assertEqual((len(raw), digest(raw)), (derivative["bytes"], derivative["sha256"]))
        for output in record["outputs"]:
            raw = (images.ROOT / output["path"]).read_bytes()
            self.assertEqual((len(raw), digest(raw)), (output["bytes"], output["sha256"]))

    def test_all_nine_bitmaps_keep_original_dimensions_and_pixels(self):
        selected = [i for i in self.result["resources"] if i.get("pixel_equivalent")]
        self.assertEqual(len(selected), 9)
        for item in selected:
            original = images.bitmap_pixels(images.RAW / item["resource"])
            derivative = images.bitmap_pixels(images.OUTPUT / item["derivatives"][0]["path"])
            for key in ("width", "height", "rgba_sha256"):
                self.assertEqual(original[key], derivative[key])

    def test_blank_and_symbol_loss_remain_flagged_not_verified(self):
        by_name = {i["resource"]: i for i in self.result["resources"]}
        blank, equation = by_name["bm54.wmf"], by_name["bm55.wmf"]
        self.assertEqual(blank["status"], "needs_review")
        self.assertTrue(blank["preview_blank"])
        self.assertTrue(images.blank_preview(images.OUTPUT / blank["derivatives"][1]["path"]))
        self.assertEqual(blank["svg"]["drawing_elements"], 0)
        self.assertEqual(equation["status"], "needs_review")
        self.assertTrue(equation["source_format"]["contains_symbol_font_name"])
        self.assertTrue(any("mathematical_glyphs_suspect" in c for c in equation["concerns"]))
        self.assertEqual(self.result["counts"]["statuses"], {"converted_pending_viewer": 19, "needs_review": 2})
        self.assertTrue(all(not i["viewer_compared"] for i in by_name.values()))
        self.assertFalse(self.result["verification"]["image_fidelity_verified"])


if __name__ == "__main__":
    unittest.main()
