"""Native evidence prevents an index gap from hiding a recoverable article."""

from collections import Counter
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import tempfile
from threading import Thread
import unittest
from urllib.parse import urljoin
from urllib.request import urlopen

from maso_archive.reading_room_package import file_record, load_package
from tools import close_cd1_february as closeout
from tools.build_reading_room_package import write_package


@unittest.skipUnless((closeout.keyboard.OUTPUT / 'combined/content/manifest.json').exists(),
                     'Private six-article sources unavailable')
class FebruaryCloseoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record, cls.coverage, cls.files = closeout.build_handoff()
        cls.evidence = json.loads(cls.files['provenance.json'])

    def test_rebuild_matches_both_records_and_accounts_for_all_native_topics(self):
        self.assertEqual(self.record, json.loads(closeout.RECORD.read_bytes()))
        self.assertEqual(self.coverage, json.loads(closeout.COVERAGE.read_bytes()))
        scan = self.coverage['native_scan']
        self.assertEqual((scan['native_topics'], scan['dated_article_topics'], scan['navigation_topics'], scan['untitled_topics']),
                         (3099, 1088, 10, 2001))
        self.assertEqual(scan['unattributed_titled_topics'], 0)
        self.assertEqual(len(self.evidence['native_metadata_inventory']), 3099)
        self.assertEqual([r['native']['ordinal'] for r in scan['february_articles']], [146, 149, 152, 155, 158, 161])
        self.assertTrue(all(r['context_at_header'] for r in scan['february_articles']))
        self.assertEqual([r['issue'] for r in scan['boundary_articles']], ['1988-01', '1988-03'])
        self.assertEqual(len(scan['other_issue_context_offset_differences']), 11)
        self.assertTrue(all(r['issue'] != '1988-02' for r in scan['other_issue_context_offset_differences']))

    def test_six_native_articles_do_not_invent_a_sixth_index_reference(self):
        self.assertEqual(self.coverage['counts']['toc_preparation'], {'prepared': 6, 'unprepared': 29, 'not_applicable_section': 4})
        self.assertEqual(Counter(r['preparation_status'] for r in self.coverage['toc_entries']), self.coverage['counts']['toc_preparation'])
        self.assertEqual(len(self.coverage['cd_references']), 5)
        self.assertEqual(sum(len(r['occurrences']) for r in self.coverage['cd_references']), 11)
        self.assertEqual(len(self.coverage['native_articles']), 6)
        unindexed = [r for r in self.coverage['native_articles'] if r['index_status'] == 'unindexed']
        self.assertEqual([r['reference'] for r in unindexed], ['8802162'])
        self.assertEqual(self.evidence['article_evidence']['8802162']['index_occurrences'], [])
        self.assertEqual(self.coverage['limits']['printed_issue_completeness'], 'unverified')
        self.assertEqual(len(self.evidence['article_evidence']), 6)
        old = json.loads(closeout.indexed.COVERAGE.read_bytes())
        self.assertEqual(old['counts']['toc_preparation']['prepared'], 5)
        self.assertEqual(old['counts']['toc_preparation']['unprepared'], 30)

    def test_issue_keyword_drift_and_missing_attribution_fail_closed(self):
        source = closeout.native.SOURCES
        mvb, rtf = [(closeout.ROOT / p).read_bytes() for p in source]
        row = next(r for r in self.coverage['native_scan']['february_articles'] if r['reference'] == '8802162')
        span = row['issue_keyword']
        start, end = span['byte_offset'], span['byte_offset'] + span['byte_length']
        changed = rtf[start:end].replace(b' 2', b' 3')
        self.assertNotEqual(changed, rtf[start:end])
        with self.assertRaisesRegex(ValueError, 'February native keyword/page populations'):
            closeout.scan_native(mvb, rtf[:start] + changed + rtf[end:])
        with self.assertRaisesRegex(ValueError, 'Unattributed titled native topic'):
            closeout.scan_native(mvb, rtf[:start] + b' ' * span['byte_length'] + rtf[end:])

    def test_all_content_and_review_exceptions_survive_relocation(self):
        predecessor = closeout.keyboard.OUTPUT / 'combined/content'
        for record in self.record['outputs']:
            self.assertEqual(self.files['content/' + record['path']], (predecessor / record['path']).read_bytes())
        self.assertEqual(self.record['counts']['files'], 56)
        self.assertEqual(self.record['counts']['paragraphs'], 2821)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'issue'
            write_package(root, self.files)
            bundle, _, counts = load_package(root / 'content')
            self.assertEqual(counts, self.record['counts'])
            reviews = self.coverage['review_records']
            closeout.indexed.check_reviews(bundle, reviews['deferred_media'], reviews['text_reviews'])
            self.assertEqual(sum(m['status'] == 'deferred' for m in bundle['media']['items']), 4)
            before = (root / 'content/manifest.json').read_bytes()
            broken = dict(self.files)
            broken['content/catalog.json'] = b'{}\n'
            with self.assertRaises(ValueError):
                write_package(root, broken)
            self.assertEqual((root / 'content/manifest.json').read_bytes(), before)

    def test_every_file_fetches_beneath_two_nested_base_urls(self):
        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prefixes = ['archive/cd1', 'reader/data/1988/02']
            for prefix in prefixes:
                write_package(root / prefix, self.files)
            server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=temporary))
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                for prefix in prefixes:
                    base = f'http://127.0.0.1:{server.server_port}/{prefix}/content/'
                    for record in self.record['outputs']:
                        with urlopen(urljoin(base, record['path']), timeout=5) as response:
                            self.assertEqual(file_record(record['path'], response.read()), record)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)


if __name__ == '__main__':
    unittest.main()
