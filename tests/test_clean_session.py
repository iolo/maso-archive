"""Exercise cleanup boundaries against real directories, links and Git records."""
from pathlib import Path
import subprocess
import tempfile
import unittest

from tools.clean_session import clean


class SessionCleanupTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        subprocess.run(['git', 'init', '--quiet', str(self.root)], check=True)
        self.files = (
            'archive/pdf/1988-01/restoration/raw-ocr.txt',
            'metadata/identities/toc.json', 'maso-pdf/source.pdf',
            'work/tmp/render.png', 'work/validation/rebuild/article.json',
            'work/reading-room/stages/data/manifest.json',
            'work/cache/toc-snapshots/history/catalog.json',
            'work/unclassified/review.txt',
            'dist/reading-room/data/manifest.json',
            'dist/releases/review/index.html', 'dist/releases/review.json',
            'dist/README.md',
        )
        for name in self.files:
            path = self.root/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(name)

    def assert_kept(self, *names):
        for name in names:
            self.assertEqual((self.root/name).read_text(), name)

    def test_preview_is_read_only_and_default_delete_keeps_readers_and_caches(self):
        preview = clean(self.root)
        self.assertEqual(len(preview), 3)
        self.assert_kept(*self.files)
        deleted = clean(self.root, apply=True)
        self.assertEqual(deleted, preview)
        self.assertTrue(all(not (self.root/row['path']).exists() for row in deleted))
        self.assert_kept(*(name for name in self.files if name.split('/')[1] not in
                           {'tmp', 'validation', 'reading-room'} or not name.startswith('work/')))
        self.assertEqual(clean(self.root, apply=True), [])

    def test_optional_reader_and_cache_cleanup_keeps_preserved_storage(self):
        rows = clean(self.root, apply=True, include_dist=True, include_caches=True)
        removed = {row['path'] for row in rows}
        self.assertIn('dist/reading-room', removed)
        self.assertIn('dist/releases', removed)
        self.assertIn('work/cache/toc-snapshots', removed)
        self.assert_kept(self.files[0], self.files[1], self.files[2],
                         'work/unclassified/review.txt', 'dist/README.md')

    def test_symlinked_parent_is_rejected_before_any_deletion(self):
        (self.root/'work').rename(self.root/'saved-work')
        (self.root/'work').symlink_to('archive', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            clean(self.root, apply=True, include_dist=True)
        self.assert_kept(self.files[0], self.files[1], 'dist/reading-room/data/manifest.json')

    def test_symlinked_dist_target_prevents_partial_cleanup(self):
        (self.root/'dist/archive-link').symlink_to('../archive', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            clean(self.root, apply=True, include_dist=True)
        self.assert_kept('work/tmp/render.png', self.files[0])

    def test_nested_links_are_unlinked_without_following_their_targets(self):
        (self.root/'work/tmp/archive-link').symlink_to('../../archive', target_is_directory=True)
        (self.root/'work/validation/metadata-link').symlink_to('../../metadata', target_is_directory=True)
        clean(self.root, apply=True)
        self.assert_kept(self.files[0], self.files[1], self.files[2])

    def test_tracked_file_prevents_partial_cleanup(self):
        subprocess.run(['git', 'add', 'work/validation/rebuild/article.json'], cwd=self.root, check=True)
        with self.assertRaisesRegex(ValueError, 'Git-tracked'):
            clean(self.root, apply=True)
        self.assert_kept(*self.files)


if __name__ == '__main__':
    unittest.main()
