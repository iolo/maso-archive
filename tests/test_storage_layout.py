"""Preservation, interruption recovery and safety across the storage migration."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import storage_layout as storage


class StorageTests(unittest.TestCase):
    def fixture(self, root):
        files = {
            'data/identities/toc.json': b'{"stable": "identity"}\n',
            'private/pdf-restoration/14-1984-09/batch-1/correction.txt': b'\xed\x95\x9c\xea\xb8\x80\n',
            'private/pdf-restoration/ocr-runtime/bin/tesseract': b'original runtime',
            'build/pdf-restoration/14-1984-09-reference/issue.json': b'unchanged package',
            'build/toc-snapshots/version/catalog.json': b'reproducible cache',
            'build/reading-room-volunteer/index.html': b'<h1>Reader</h1>',
            'build/reading-room-volunteer/data/manifest.json': b'{}',
            'output/playwright/review.png': b'original review evidence',
        }
        for name, raw in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        return files

    def migrate(self, root):
        with patch.object(storage.subprocess, 'check_output', return_value='original-commit\n'):
            return storage.migrate(root)

    def test_preserves_bytes_inodes_and_historical_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = self.fixture(root)
            inodes = {name: (root/name).stat().st_ino for name in files}
            self.migrate(root)
            for name, raw in files.items():
                current = root / storage.destination(name)
                self.assertEqual(current.read_bytes(), raw)
                self.assertEqual(current.stat().st_ino, inodes[name])
                self.assertEqual((root/name).resolve(), current.resolve())
            self.assertTrue((root/'archive/toolchains/ocr/bin/tesseract').is_file())
            # An older script writing an unseen path must still write to retained storage.
            (root/'private/new-correction.txt').write_text('keep this')
            self.assertEqual((root/'archive/legacy-paths/private/new-correction.txt').read_text(), 'keep this')
            self.assertEqual(self.migrate(root)['compatibility'], 'verified')
            # Missing reproducible outputs are allowed; missing preserved inputs are not.
            (root/'work/cache/toc-snapshots/version/catalog.json').unlink()
            (root/'work/cache/toc-snapshots/version').rmdir()
            (root/'work/cache/toc-snapshots').rmdir()
            self.assertEqual(len(storage.verify(root)['regenerable_missing']), 1)
            (root/'archive/toolchains/ocr/bin/tesseract').unlink()
            (root/'archive/toolchains/ocr/bin').rmdir()
            (root/'archive/toolchains/ocr').rmdir()
            with self.assertRaisesRegex(ValueError, 'compatibility differs'):
                storage.verify(root)

    def test_resumes_interrupted_moves_without_replacing_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = self.fixture(root)
            rename = Path.rename
            calls = 0
            def interrupted(path, target):
                nonlocal calls
                calls += 1
                if calls == 3:
                    raise OSError('simulated interruption')
                return rename(path, target)
            with patch.object(Path, 'rename', interrupted):
                with self.assertRaisesRegex(OSError, 'interruption'):
                    self.migrate(root)
            self.migrate(root)
            for name, raw in files.items():
                self.assertEqual((root/name).read_bytes(), raw)

    def test_conflicts_and_cross_tree_links_are_rejected_before_moves(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = self.fixture(root)
            (root/'metadata').mkdir()
            with self.assertRaisesRegex(ValueError, 'Destination already exists'):
                self.migrate(root)
            (root/'metadata').rmdir()
            link = root/'private/pdf-restoration/ocr-runtime/outside'
            link.symlink_to('../../../data/identities/toc.json')
            with self.assertRaisesRegex(ValueError, 'symlink crosses'):
                self.migrate(root)
            for name, raw in files.items():
                self.assertEqual((root/name).read_bytes(), raw)

    def test_output_containment_resolves_links_and_rejects_roots(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            self.fixture(root)
            self.migrate(root)
            self.assertTrue(storage.is_local_output(root/'private/pdf-restoration/14-1984-09/new',root))
            self.assertTrue(storage.is_local_output(root/'archive/pdf/1984-10/restoration/batch-1',root))
            self.assertTrue(storage.is_local_output(root/'work/tmp/job',root))
            for name in ('metadata/correction.json','docs/example','archive','work','dist','private','build','output'):
                self.assertFalse(storage.is_local_output(root/name,root), name)
            (root/'archive/escape').symlink_to(outside, target_is_directory=True)
            self.assertFalse(storage.is_local_output(root/'archive/escape/result',root))
            for name in ('/etc/passwd','private/../data','private\\test'):
                with self.assertRaises(ValueError): storage.destination(name)

    def test_package_hashes_allow_only_recorded_aliases(self):
        from maso_archive import storage as reader_storage
        from maso_archive.reading_room_package import checked_file, file_record, load_package
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = self.fixture(root)
            self.migrate(root)
            original = 'data/identities/toc.json'
            record = file_record(original, files[original])
            with patch.object(reader_storage, 'REPOSITORY', root):
                self.assertEqual(checked_file(root, record), files[original])
                (root/'metadata/identities/unregistered.json').symlink_to('toc.json')
                with self.assertRaisesRegex(ValueError, 'Symlink'):
                    checked_file(root, {'path': 'data/identities/unregistered.json'})
                (root/'metadata/identities/toc.json').write_bytes(b'tampered')
                with self.assertRaisesRegex(ValueError, 'mismatch'):
                    checked_file(root, record)
                (root/'data').unlink()
                (root/'data').symlink_to('archive')
                with self.assertRaisesRegex(ValueError, 'link changed'):
                    checked_file(root, record)

    def test_release_copy_is_independent_and_restore_is_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.migrate(root)
            storage.snapshot_reader(root)
            preserved = root/storage.READER_RELEASE/'index.html'
            current = root/'dist/reading-room/index.html'
            self.assertNotEqual(current.stat().st_ino,preserved.stat().st_ino)
            current.write_text('a later UI build')
            self.assertEqual(preserved.read_bytes(), b'<h1>Reader</h1>')
            storage.restore_reader(root,'dist/restored')
            self.assertEqual((root/'dist/restored/index.html').read_bytes(),preserved.read_bytes())
            with self.assertRaisesRegex(ValueError,'already exists'):
                storage.restore_reader(root,'dist/restored')
            with self.assertRaisesRegex(ValueError,'inside dist'):
                storage.restore_reader(root,'archive/overwritten')
            preserved.write_text('damaged backup')
            with self.assertRaisesRegex(ValueError,'differs'):
                storage.restore_reader(root,'dist/bad')
            self.assertFalse((root/'dist/bad').exists())


if __name__ == '__main__':
    unittest.main()
