"""Local source integrity and safe restore mechanics; fixtures are not backup evidence."""

from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools import inventory_cd1_sources as preservation
from tools.recover_cd1_text import json_bytes


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_exact_inventory_detects_modified_missing_extra_and_empty_directories(self):
        (self.root / "a").mkdir()
        (self.root / "a/file").write_bytes(b"source")
        (self.root / "a.txt").write_bytes(b"other")
        (self.root / "empty").mkdir()
        expected = preservation.tree_inventory(self.root)
        self.assertEqual([r["path"] for r in expected["files"]], ["a.txt", "a/file"])
        self.assertEqual(expected["directories"], ["a", "empty"])
        for mutation in (lambda: (self.root / "a/file").write_bytes(b"changed"),
                         lambda: (self.root / "a/file").unlink(),
                         lambda: (self.root / "extra").write_bytes(b"extra"),
                         lambda: (self.root / "empty").rmdir()):
            for child in self.root.iterdir():
                shutil.rmtree(child) if child.is_dir() else child.unlink()
            for directory in expected["directories"]:
                (self.root / directory).mkdir(parents=True)
            (self.root / "a/file").write_bytes(b"source")
            (self.root / "a.txt").write_bytes(b"other")
            mutation()
            with self.assertRaisesRegex(ValueError, "Source tree differs"):
                preservation.compare_trees(expected, preservation.tree_inventory(self.root))

    def test_symlinks_and_unsafe_manifest_paths_are_rejected(self):
        (self.root / "target").write_bytes(b"bytes")
        (self.root / "link").symlink_to(self.root / "target")
        with self.assertRaisesRegex(ValueError, "Symlink"):
            preservation.tree_inventory(self.root)
        for path in ("../escape", "/absolute", "raw/../outside", "raw//empty", "raw\\file", "./file"):
            with self.assertRaises(ValueError):
                preservation.safe_relative(path)

    def probe(self):
        (self.root / "raw").mkdir()
        (self.root / "raw/file.rtf").write_bytes(b"preserved")
        manifest = {"files": [{"path": "raw/file.rtf", **preservation.fingerprint(self.root / "raw/file.rtf")}]}
        (self.root / "manifest.json").write_bytes(json_bytes(manifest))
        for name in ("build.log", "internal-directory.txt"):
            (self.root / name).write_bytes(b"evidence")
        return manifest

    def test_probe_manifest_hashes_and_supporting_file_coverage(self):
        manifest = self.probe()
        preservation.checked_probe(self.root, preservation.tree_inventory(self.root))
        (self.root / "raw/file.rtf").write_bytes(b"modified")
        with self.assertRaisesRegex(ValueError, "Probe size/hash mismatch"):
            preservation.checked_probe(self.root, preservation.tree_inventory(self.root))
        (self.root / "raw/file.rtf").write_bytes(b"preserved")
        (self.root / "extra.log").write_bytes(b"unrecorded")
        with self.assertRaisesRegex(ValueError, "Probe file inventory differs"):
            preservation.checked_probe(self.root, preservation.tree_inventory(self.root))
        (self.root / "extra.log").unlink()
        manifest["files"].append(deepcopy(manifest["files"][0]))
        (self.root / "manifest.json").write_bytes(json_bytes(manifest))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            preservation.checked_probe(self.root, preservation.tree_inventory(self.root))

    def test_archive_listing_rejects_paths_before_extraction(self):
        for name in ("../escape", "/absolute", "a/../../escape"):
            listing = f"7-Zip test\nType = Iso\n----------\nPath = {name}\nFolder = -\nSize = 1\n"
            with patch.object(preservation, "run_7z", return_value=listing), self.assertRaises(ValueError):
                preservation.iso_listing(self.root / "disc.iso")
        result = subprocess.CompletedProcess([], 2, b"partial output", b"failed")
        with patch.object(preservation.subprocess, "run", return_value=result), self.assertRaisesRegex(ValueError, "7z failed"):
            preservation.run_7z(["l", "disc.iso"])


class RestoreMechanicsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        self.iso = self.workspace / "disc.iso"
        self.iso.write_bytes(b"synthetic ISO bytes")
        self.backup = self.root / "backup.iso"
        self.backup.write_bytes(self.iso.read_bytes())
        self.inventory = {"iso": preservation.fingerprint(self.iso), "iso_entries": [],
                          "extracted": {"files": [], "directories": []}}
        for name, value in (("ROOT", self.workspace), ("ISO", self.iso)):
            patcher = patch.object(preservation, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_working_copy_and_missing_independence_description_are_rejected(self):
        for path, note in ((self.iso, "fixture"), (self.backup, "")):
            with self.assertRaises(ValueError):
                preservation.restore_backup(path, self.inventory, note)
        self.backup.unlink()
        self.backup.hardlink_to(self.iso)
        with self.assertRaises(ValueError):
            preservation.restore_backup(self.backup, self.inventory, "fixture")

    def test_wrong_backup_fails_before_extraction(self):
        self.backup.write_bytes(b"corrupt backup")
        with patch.object(preservation, "iso_listing") as listing, self.assertRaisesRegex(ValueError, "Backup ISO does not match"):
            preservation.restore_backup(self.backup, self.inventory, "synthetic fixture, not actual storage evidence")
        listing.assert_not_called()
        self.assertEqual(self.iso.read_bytes(), b"synthetic ISO bytes")

    def test_restore_reads_new_copy_cleans_temporary_files_and_preserves_sources(self):
        restored_paths = []
        def extract(iso, listing, root):
            self.assertNotEqual(iso, self.backup)
            self.assertEqual(iso.read_bytes(), self.backup.read_bytes())
            restored_paths.append(iso)
            return {"files": [], "directories": []}
        with patch.object(preservation, "iso_listing", return_value=([], "fixture")), patch.object(preservation, "extract_inventory", side_effect=extract):
            report = preservation.restore_backup(self.backup, self.inventory, "synthetic fixture, not actual storage evidence")
        self.assertTrue(report["verification"]["restored_iso_hash_matches"])
        self.assertEqual(report["storage_independence"]["basis"], "owner_supplied_description")
        self.assertTrue(all(not p.exists() for p in restored_paths))
        self.assertEqual(self.iso.read_bytes(), self.backup.read_bytes())

    def test_restore_tree_mismatch_is_not_success(self):
        with patch.object(preservation, "iso_listing", return_value=([], "fixture")), patch.object(preservation, "extract_inventory", return_value={"files": [], "directories": ["unexpected"]}):
            with self.assertRaisesRegex(ValueError, "Source tree differs"):
                preservation.restore_backup(self.backup, self.inventory, "synthetic fixture")


@unittest.skipUnless(preservation.ISO.exists() and preservation.PROBE.exists() and shutil.which("7z"), "Private CD1 sources or 7z unavailable")
class RealInventoryTests(unittest.TestCase):
    def test_all_cd1_sources_match_reviewed_inventory_without_claiming_backup(self):
        record, raw = preservation.build_inventory()
        self.assertEqual(record, json.loads(preservation.RECORD.read_bytes()))
        self.assertEqual(raw, (preservation.OUTPUT / "inventory.json").read_bytes())
        self.assertEqual(record["counts"]["disc_files"], 5828)
        self.assertEqual(record["counts"]["probe_manifest_files"], 7374)
        self.assertEqual(record["counts"]["probe_files"], 7377)
        self.assertFalse(record["validation"]["independent_backup_assessed"])
        self.assertFalse(record["validation"]["restore_from_backup_assessed"])


if __name__ == "__main__":
    unittest.main()
