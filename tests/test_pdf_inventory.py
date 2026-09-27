"""Synthetic source metadata and TOC safety checks; no private scans required."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from tools.pdf_restore.inventory import load_toc, page_metadata, pin, queue_for, text_pages, write_json


class PDFInventoryTests(unittest.TestCase):
    def test_rotation_boxes_and_index_conventions(self):
        raw = '''Pages: 2
Page 1 size: 100 x 200 pts
Page 1 rot: 90
Page 2 size: 220 x 110 pts
Page 2 rot: 270
Page 1 MediaBox: -10.00 0.00 100.00 200.00
Page 1 CropBox: 0.00 5.00 90.00 190.00
Page 2 MediaBox: 0.00 0.00 220.00 110.00
Page 2 CropBox: 0.00 0.00 220.00 110.00
'''
        pages = page_metadata(raw, 2)
        self.assertEqual([p['pdf_index'] for p in pages], [0, 1])
        self.assertEqual([p['pdf_page'] for p in pages], [1, 2])
        self.assertEqual(pages[0]['MediaBox'], [-10, 0, 100, 200])
        self.assertEqual((pages[1]['width_pt'], pages[1]['height_pt'], pages[1]['rotation']), (220, 110, 270))
        with self.assertRaisesRegex(ValueError, 'Missing dimensions'):
            page_metadata(raw, 3)
        with self.assertRaisesRegex(ValueError, 'Missing CropBox'):
            page_metadata(raw.replace('Page 2 CropBox', 'unrelated'), 2)

    def test_text_layer_does_not_conflate_empty_pages_with_missing_pages(self):
        pages = text_pages(' \n\fannotation 397~398\f\f'.encode(), 3)
        self.assertEqual([p['extractable_text'] for p in pages], [False, True, False])
        with self.assertRaisesRegex(ValueError, 'separators'):
            text_pages(b'\f', 2)

    def test_queue_retains_pageless_parents_and_non_candidate_leaves(self):
        sources = [{'id': 'pdf-sample', 'provisional_issue_id': 'issue', 'scope': 'toc-entries-and-cover'},
                   {'id': 'pdf-cover', 'provisional_issue_id': 'cover', 'scope': 'cover-only'}]
        entries = [{'id': 'parent', 'parent_id': None, 'issue_id': 'issue', 'kind_candidate': 'section'},
                   {'id': 'child', 'parent_id': 'parent', 'issue_id': 'issue', 'kind_candidate': 'article'},
                   {'id': 'pageless', 'parent_id': None, 'issue_id': 'issue', 'kind_candidate': 'unknown'},
                   {'id': 'excluded', 'parent_id': None, 'issue_id': 'cover', 'kind_candidate': 'article'}]
        before = copy.deepcopy(entries)
        queue = queue_for(sources, entries, [{'toc_entry_id': 'child', 'id': 'existing-article'}])
        self.assertEqual([q['toc_entry_id'] for q in queue], ['parent', 'child', 'pageless'])
        self.assertEqual(queue[1]['provisional_article_id'], 'existing-article')
        self.assertTrue(all(q['classification']['status'] == 'unresolved' for q in queue))
        self.assertEqual(entries, before)
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            queue_for(sources, entries + [entries[0]], [])
        with self.assertRaisesRegex(ValueError, 'Missing parent'):
            queue_for(sources, entries[1:], [])

    def test_current_snapshot_pins_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for path, data in [('TOC.md', b'synthetic'), ('data/identities/toc.json', b'{}'),
                               ('schemas/toc-import.schema.json', b'{}'),
                               ('build/toc/issues.json', b'[]'), ('build/toc/toc-entries.jsonl', b''),
                               ('build/toc/article-candidates.jsonl', b'')]:
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            names = ('issues.json', 'toc-entries.jsonl', 'article-candidates.jsonl')
            manifest = {'source': pin(root, 'TOC.md'),
                        'identities_sha256': pin(root, 'data/identities/toc.json')['sha256'],
                        'schema_sha256': pin(root, 'schemas/toc-import.schema.json')['sha256'],
                        'outputs': {n: pin(root, 'build/toc/' + n) for n in names}}
            write_json(root / 'build/toc/manifest.json', manifest)
            self.assertEqual(load_toc(root)[1:], ([], [], []))
            (root / 'build/toc/issues.json').write_text('[{}]')
            with self.assertRaisesRegex(ValueError, 'snapshot changed'):
                load_toc(root)
            (root / 'TOC.md').write_text('changed source')
            with self.assertRaisesRegex(ValueError, 'Current TOC differs'):
                load_toc(root)


if __name__ == '__main__':
    unittest.main()
