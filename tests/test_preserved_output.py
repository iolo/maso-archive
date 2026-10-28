"""Regression checks for retained results across successive restoration runs."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import preserved_output as saved
from tools import storage_layout as storage


def identities(root):
    return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_ino, p.stat().st_mtime_ns)
            for p in root.rglob('*') if p.is_file()}


class PreservationTests(unittest.TestCase):
    def test_tree_verification_checks_bytes_and_never_replaces_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stage, target = root/'stage', root/'retained'
            saved.put(stage, 'result.txt', b'original')
            saved.put(stage, 'manifest.json', b'{"unchanged": true}')
            saved.publish_tree(stage, target)
            self.assertFalse(stage.exists())
            saved.put(stage, 'result.txt', b'original')
            saved.put(stage, 'manifest.json', b'{"unchanged": true}')
            before = identities(target)
            with self.assertRaisesRegex(ValueError, 'already exists'):
                saved.publish_tree(stage, target)
            saved.publish_tree(stage, target, verify_existing=True)
            self.assertEqual(identities(target), before)
            (target/'result.txt').write_text('tampered; manifest unchanged')
            with self.assertRaisesRegex(ValueError, 'rebuild differs'):
                saved.publish_tree(stage, target, verify_existing=True)
            (target/'result.txt').write_text('original')
            (target/'unlisted.txt').write_text('retained note')
            with self.assertRaisesRegex(ValueError, 'rebuild differs'):
                saved.publish_tree(stage, target, verify_existing=True)
            with self.assertRaisesRegex(ValueError, 'existing directory'):
                saved.publish_tree(stage, root/'absent', verify_existing=True)
            self.assertFalse((root/'absent').exists())

    def test_file_writes_preserve_previous_bytes_and_verification_is_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            saved.put(root, 'record.json', b'kept')
            before = identities(root)
            saved.put(root, 'record.json', b'kept')
            saved.put(root, 'record.json', b'kept', verify_existing=True)
            self.assertEqual(identities(root), before)
            with self.assertRaisesRegex(ValueError, 'Preserved file differs'):
                saved.put(root, 'record.json', b'replacement')
            with self.assertRaisesRegex(ValueError, 'Missing preserved file'):
                saved.put(root, 'absent.json', b'new', verify_existing=True)
            self.assertEqual(identities(root), before)
            (root/'alias.json').symlink_to('record.json')
            with self.assertRaisesRegex(ValueError, 'Symlink'):
                saved.put(root, 'alias.json', b'kept')

    def test_cd_builders_refuse_existing_results_before_processing_sources(self):
        from tools import build_cd2_pilot as pilot, build_cd2_issue as issue
        from tools import build_cd2_reference as cd2, build_cd3_reference as cd3
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'issues/9401').mkdir(parents=True)
            (root/'groups/9501').mkdir(parents=True)
            for module, call in (
                (pilot, lambda: pilot.build()),
                (issue, lambda: issue.build()),
                (cd2, lambda: cd2.build_issue('9401', {}, {}, {}, b'')),
                (cd3, lambda: cd3.build_group('9501', {'topics': [
                    {'identity':'one', 'role':'article_candidate', 'group':'9501'}]}, {}, {}, b'', 'hash')),
            ):
                with self.subTest(tool=module.__name__), patch.object(module, 'OUTPUT', root):
                    with self.assertRaisesRegex(ValueError, 'already exists'):
                        call()

    def test_cd_finalizers_verify_without_writing_or_repairing_missing_files(self):
        from tools import build_cd2_reference as cd2, build_cd3_reference as cd3
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            queue2 = dict(candidates=[], additional_article_candidates=[], unindexed_topics=[], candidate_basis='fixture')
            queue3 = dict(topics=[])
            def supplements(queue, rtf, stage, *, write):
                write(stage, 'supplements.json', b'{"topics": []}')
                return []
            with patch.object(cd2, 'ISSUES', ()), patch.object(cd2, 'classify_supplements', supplements):
                cd2.finalize(queue2, b'', {}, output=root/'cd2')
                cd3.finalize(queue3, {}, b'', 'queue-hash', output=root/'cd3')
                before = identities(root)
                cd2.finalize(queue2, b'', {}, output=root/'cd2', verify_existing=True)
                cd3.finalize(queue3, {}, b'', 'queue-hash', output=root/'cd3', verify_existing=True)
                self.assertEqual(identities(root), before)
                for name, call in (
                    ('cd2', lambda: cd2.finalize(queue2, b'', {}, output=root/'cd2', verify_existing=True)),
                    ('cd3', lambda: cd3.finalize(queue3, {}, b'', 'queue-hash', output=root/'cd3', verify_existing=True)),
                ):
                    with self.subTest(tool=name):
                        missing = root/name/'style.css'
                        missing.unlink()
                        remaining = identities(root)
                        with self.assertRaisesRegex(ValueError, 'Missing preserved file'):
                            call()
                        self.assertFalse(missing.exists())
                        self.assertEqual(identities(root), remaining)

    def test_new_pdf_checkpoint_uses_canonical_inputs_without_legacy_aliases(self):
        from tests.test_pdf_build import PDFBuildTests
        from tools.pdf_restore.build import build, check_export
        from tools.pdf_restore import batch
        from tools.pdf_restore.inventory import pin, write_json
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            old_recipe = PDFBuildTests().fixture(root)
            base = root/'archive/pdf/1984-10/restoration/batch-01'
            base.parent.mkdir(parents=True)
            old_recipe.parent.rename(base)
            for old, new in (
                ('private/pdf-restoration/inventory', 'archive/pdf/shared/restoration/inventory'),
                ('private/pdf-restoration/ocr-runtime', 'archive/toolchains/ocr'),
            ):
                target = root/new
                target.parent.mkdir(parents=True, exist_ok=True)
                (root/old).rename(target)
            inputs = identities(root/'archive')
            output = root/'archive/pdf/1984-10/packages/batch-01-r01'
            package = build(base/'recipe.json', output, root)
            self.assertEqual(check_export(output), package)
            with self.assertRaisesRegex(ValueError, 'already exists'):
                build(base/'recipe.json', output, root)
            before = identities(output)
            repeat = root/'archive/pdf/1984-10/evidence/batch-01-repeat'
            build(base/'recipe.json', repeat, root)
            self.assertEqual(storage.file_inventory(output), storage.file_inventory(repeat))
            self.assertEqual(identities(output), before)
            after = identities(root/'archive')
            self.assertTrue(all(after[name] == value for name, value in inputs.items()))
            request = base/'request.json'
            relative = base.relative_to(root).as_posix()
            write_json(request, dict(batch_id='next-issue', limits=batch.MAX_LIMITS,
                lookup_pages=[], articles=[dict(map=pin(root, relative+'/map.json'),
                                               recipe=pin(root, relative+'/recipe.json'))]))
            with patch.object(batch, 'toolchain', return_value={'engine': 'synthetic'}):
                state = base/'ocr-state'
                batch.prepare(request, state, root/'archive/pdf/shared/restoration/batch-cache',
                              root, root/'archive/toolchains/ocr')
            self.assertTrue((state/'ledger.json').is_file())
            self.assertFalse((root/'private/pdf-restoration/inventory').exists())
            self.assertFalse((root/'private/pdf-restoration/ocr-runtime').exists())

    def reader(self, root):
        source = root/'dist/reading-room'
        saved.put(source, 'index.html', b'first reader')
        saved.put(source, 'data/manifest.json', b'{}')
        return source

    def test_successive_releases_are_independent_and_selectable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = self.reader(root)
            storage.snapshot_reader(root, release='first')
            before = identities(root/'dist/releases')
            storage.snapshot_reader(root, release='first')
            self.assertEqual(identities(root/'dist/releases'), before)
            (source/'index.html').write_bytes(b'second reader')
            with self.assertRaisesRegex(ValueError, 'choose a new --release'):
                storage.snapshot_reader(root, release='first')
            storage.snapshot_reader(root, release='second')
            storage.restore_reader(root, 'dist/first-restored', release='first')
            storage.restore_reader(root, 'dist/second-restored', release='second')
            self.assertEqual((root/'dist/first-restored/index.html').read_bytes(), b'first reader')
            self.assertEqual((root/'dist/second-restored/index.html').read_bytes(), b'second reader')
            for bad in ('../escape', '/absolute', 'same.name', ''):
                if not bad: continue
                with self.assertRaisesRegex(ValueError, 'Release name'):
                    storage.snapshot_reader(root, release=bad)
            (root/'dist/releases/linked').symlink_to('first')
            with self.assertRaisesRegex(ValueError, 'symlinks'):
                storage.restore_reader(root, 'dist/linked', release='linked')

    def test_interrupted_snapshot_resumes_only_with_the_same_reader(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = self.reader(root)
            original = Path.rename
            def interrupted(path, target):
                if path.name == 'reader': raise OSError('simulated interruption')
                return original(path, target)
            with patch.object(Path, 'rename', interrupted):
                with self.assertRaisesRegex(OSError, 'interruption'):
                    storage.snapshot_reader(root, release='interrupted')
            self.assertTrue((root/'dist/releases/interrupted.json').is_file())
            self.assertFalse((root/'dist/releases/interrupted').exists())
            (source/'index.html').write_bytes(b'changed reader')
            with self.assertRaisesRegex(ValueError, 'receipt differs'):
                storage.snapshot_reader(root, release='interrupted')
            (source/'index.html').write_bytes(b'first reader')
            storage.snapshot_reader(root, release='interrupted')
            storage.restore_reader(root, 'dist/restored', release='interrupted')
            self.assertEqual((root/'dist/restored/index.html').read_bytes(), b'first reader')


if __name__ == '__main__':
    unittest.main()
