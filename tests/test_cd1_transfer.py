"""Portable transfer integrity is separate from independent storage verification."""

from copy import deepcopy
from pathlib import Path
import tarfile
import tempfile
import unittest

from tools import prepare_cd1_transfer as transfer


class TransferTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        self.source.write_bytes(b"synthetic preservation content\n")
        self.archive = self.root / "transfer.tar"

    def build(self):
        return transfer.write_archive(self.archive, {"raw/source.bin": self.source}, ["empty", "raw"], "synthetic-commit")

    def test_roundtrip_determinism_and_no_source_changes(self):
        before = self.source.read_bytes()
        manifest = self.build()
        first = self.archive.read_bytes()
        self.assertFalse(manifest["independent_backup_verified"])
        self.assertEqual(self.build(), manifest)
        self.assertEqual(self.archive.read_bytes(), first)
        self.assertEqual(self.source.read_bytes(), before)
        with tarfile.open(self.archive) as archive:
            self.assertEqual(archive.extractfile("raw/source.bin").read(), before)
            self.assertTrue(archive.getmember("empty").isdir())

    def test_payload_tampering_and_missing_members_are_rejected(self):
        manifest = self.build()
        with tarfile.open(self.archive) as archive:
            offset = archive.getmember("raw/source.bin").offset_data
        with self.archive.open("r+b") as stream:
            stream.seek(offset)
            stream.write(b"X")
        with self.assertRaisesRegex(ValueError, "content mismatch"):
            transfer.verify_archive(self.archive, manifest)
        manifest = self.build()
        changed = deepcopy(manifest)
        changed["files"].append({"path": "missing", "bytes": 0, "sha256": "0" * 64})
        with self.assertRaisesRegex(ValueError, "coverage mismatch"):
            transfer.verify_archive(self.archive, changed)

    def test_unsafe_paths_symlinks_and_duplicate_members_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            transfer.write_archive(self.archive, {"../outside": self.source}, [], "synthetic")
        link = self.root / "link"
        link.symlink_to(self.source)
        with self.assertRaisesRegex(ValueError, "regular source"):
            transfer.write_archive(self.archive, {"link": link}, [], "synthetic")
        manifest = self.build()
        with tarfile.open(self.archive, "a") as archive:
            transfer.add_bytes(archive, "raw/source.bin", b"duplicate")
        with self.assertRaisesRegex(ValueError, "Duplicate archive"):
            transfer.verify_archive(self.archive, manifest)

    def test_manifest_tampering_and_archive_links_are_rejected(self):
        manifest = self.build()
        with tarfile.open(self.archive) as archive:
            offset = archive.getmember("MANIFEST.json").offset_data
        with self.archive.open("r+b") as stream:
            stream.seek(offset)
            stream.write(b"X")
        with self.assertRaisesRegex(ValueError, "manifest mismatch"):
            transfer.verify_archive(self.archive, manifest)
        with tarfile.open(self.archive, "w") as archive:
            for name in manifest["directories"]:
                info = tarfile.TarInfo(name)
                info.type = tarfile.DIRTYPE
                archive.addfile(info)
            info = tarfile.TarInfo("raw/source.bin")
            info.type, info.linkname = tarfile.SYMTYPE, "/outside"
            archive.addfile(info)
            transfer.add_bytes(archive, "MANIFEST.json", transfer.json_bytes(manifest))
            transfer.add_bytes(archive, "RESTORE.txt", transfer.INSTRUCTIONS)
        with self.assertRaisesRegex(ValueError, "regular file"):
            transfer.verify_archive(self.archive, manifest)


if __name__ == "__main__":
    unittest.main()
