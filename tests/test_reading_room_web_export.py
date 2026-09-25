"""Checks focused on the new static reader projection and portable demo."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.reading_room.export import demo, safe, text_for


class ReadingRoomWebExportTest(unittest.TestCase):
    def test_demo_covers_missing_and_literal_content(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            demo(root)
            issue = json.loads((root / 'issues/1988-02.json').read_text())
            self.assertEqual(len(issue['toc']), 5)
            self.assertEqual(issue['toc'][-1]['articleIds'], [])
            prepared = json.loads((root / 'articles/demo-prepared.json').read_text())
            text = (root / 'source' / prepared['article']['text']).read_text()
            self.assertEqual(text_for(prepared['blocks']), text)
            self.assertIn('<tag> &', text)
            self.assertIn('\tEND', text)
            self.assertIn('[image:diagram.svg]', text)
            gap = json.loads((root / 'articles/demo-gap.json').read_text())
            self.assertIn('⟦bytes:81⟧', text_for(gap['blocks']))
            self.assertEqual(text_for(gap['blocks']), (root / 'source' / gap['article']['text']).read_text())
            media = json.loads((root / 'media/1988-02.json').read_text())['items']
            self.assertEqual({item['status'] for item in media}, {'available', 'deferred'})
            blocked = json.loads((root / 'articles/demo-blocked.json').read_text())
            self.assertIsNone(blocked['article']['text'])
            self.assertEqual(blocked['blocks'], [])

    def test_source_paths_stay_inside_root(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            for path in ('../outside', '/etc/passwd', 'a/../../outside'):
                with self.assertRaises(ValueError):
                    safe(root, path)


if __name__ == '__main__':
    unittest.main()
