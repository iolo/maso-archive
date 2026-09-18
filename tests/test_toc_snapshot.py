"""Historical provenance must survive a growing current TOC and identity map."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools.toc_snapshot import ROOT, RECORD, SOURCE_SHA, Snapshot, read_input
from maso_archive.toc import run_import


class SnapshotTests(unittest.TestCase):
    def test_restore_reproduces_history_without_overwriting_current_inputs(self):
        descriptor = json.loads((ROOT / RECORD).read_bytes())
        blobs = {descriptor[key]: subprocess.check_output(["git", "cat-file", "blob", descriptor[key]], cwd=ROOT)
                 for key in ("source_git_blob", "identities_git_blob")}
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in (RECORD, "schemas/toc-import.schema.json"):
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
            (root / "data/identities").mkdir(parents=True)
            (root / "TOC.md").write_bytes(b"current source must survive\n")
            (root / "data/identities/toc.json").write_bytes(b"current identities must survive\n")
            snapshot = Snapshot(root)
            with patch("tools.toc_snapshot.subprocess.check_output", side_effect=lambda command, **kw: blobs[command[-1]]):
                snapshot.restore()
            for record in descriptor["files"]:
                self.assertEqual(hashlib.sha256(snapshot.read(record["path"])).hexdigest(), record["sha256"])
            snapshot.restore()  # Valid existing cache is checked, not rewritten.
            self.assertEqual((root / "TOC.md").read_bytes(), b"current source must survive\n")
            self.assertEqual((root / "data/identities/toc.json").read_bytes(), b"current identities must survive\n")
            self.assertEqual(hashlib.sha256(read_input(root, "TOC.md")).hexdigest(), SOURCE_SHA)
            (snapshot.directory / "TOC.md").write_bytes(b"tampered")
            with self.assertRaisesRegex(ValueError, "mismatch"):
                snapshot.restore()
            with self.assertRaisesRegex(ValueError, "mismatch"):
                read_input(root, "TOC.md")

    def test_missing_cache_never_falls_back_to_current_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / RECORD).parent.mkdir(parents=True)
            shutil.copy2(ROOT / RECORD, root / RECORD)
            (root / "TOC.md").write_bytes(b"current\n")
            with self.assertRaisesRegex(ValueError, "restore-toc-snapshot"):
                read_input(root, "TOC.md")
            (root / "unrelated.txt").write_bytes(b"live input")
            self.assertEqual(read_input(root, "unrelated.txt"), b"live input")

    def test_expansion_preserves_every_old_identity_and_entry_field(self):
        descriptor = json.loads((ROOT / RECORD).read_bytes())
        old_ids = subprocess.check_output(["git", "cat-file", "blob", descriptor["identities_git_blob"]], cwd=ROOT)
        old_source = subprocess.check_output(["git", "cat-file", "blob", descriptor["source_git_blob"]], cwd=ROOT)
        old_registry = json.loads(old_ids)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            identities = root / "identities.json"
            identities.write_bytes(old_ids)
            (root / "TOC.md").write_bytes(old_source)
            output = root / "output"
            run_import(root / "TOC.md", output, identities, **descriptor["import_manifest"]["parameters"])
            old_entries = [json.loads(line) for line in (output / "toc-entries.jsonl").read_bytes().splitlines()]
            result = run_import(ROOT / "TOC.md", output, identities)
            entries = [json.loads(line) for line in (output / "toc-entries.jsonl").read_bytes().splitlines()]
            registry = json.loads(identities.read_bytes())
            self.assertEqual(registry["entries"][:3811], old_registry["entries"])
            self.assertEqual(registry["retired_ids"], old_registry["retired_ids"])
            for issue, serial in old_registry["next_serial"].items():
                self.assertEqual(registry["next_serial"][issue], serial)
            self.assertEqual(len(entries) - len(old_entries), 1686)
            for old, new in zip(old_entries, entries):
                self.assertNotEqual(old["source"]["id"], new["source"]["id"])
                new["source"]["id"] = old["source"]["id"]
                self.assertEqual(old, new)
            self.assertEqual(result["errors"], [])
            before = {p.name: p.read_bytes() for p in output.iterdir()}
            before_ids = identities.read_bytes()
            run_import(ROOT / "TOC.md", output, identities)
            self.assertEqual(before, {p.name: p.read_bytes() for p in output.iterdir()})
            self.assertEqual(before_ids, identities.read_bytes())


if __name__ == "__main__":
    unittest.main()
