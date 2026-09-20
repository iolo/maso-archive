"""Source-bound non-ASCII policy limits and complete 16a preservation evidence."""
from copy import deepcopy
from pathlib import Path
import unittest

from tools.batch import ordinary_font_review as review, retry_ordinary_fonts as retry
from tools.run_cd1_batch import ROOT, read_json
from tools.decode_cd1_paragraph import digest
from maso_archive.reading_room_package import checked_file, load_package


def unsupported(font, raw, reason=None):
    return {'kind': 'unsupported', 'format': {'font_id': font, 'b': True},
            'text': '[unsupported]', 'reason': reason or f'Unsupported font {font}',
            'encoding': 'cp949', 'original_bytes_hex': raw.hex(),
            'source_spans': [{'byte_offset': 9, 'byte_length': len(raw)}],
            'encoded_bytes': len(raw), 'encoded_sha256': digest(raw)}


class OrdinaryFontPolicyTests(unittest.TestCase):
    def test_korean_comments_box_drawing_and_ascii_round_trip(self):
        for ref, case in review.CASES.items():
            for text in (' \tASCII', '/* 한글 */', '┏━━┳━━┓'):
                raw = text.encode('euc_kr')
                self.assertEqual(review.decode_reviewed(unsupported(case['font'], raw), ref), text)

    def test_other_articles_fonts_and_existing_decode_errors_are_rejected(self):
        for ref, run in [('other', unsupported(13, b'abc')),
                         ('9202208', unsupported(13, b'abc')),
                         ('8905226', unsupported(2, b'abc')),
                         ('8905226', unsupported(13, b'abc', 'Byte round-trip mismatch'))]:
            with self.assertRaises(ValueError): review.decode_reviewed(run, ref)

    def test_malformed_bytes_controls_and_unreviewed_extended_repertoire_are_rejected(self):
        for raw in (b'\xb0', b'\x80', b'\x81\x41', b'\x00', b'\n', b'\x7f'):
            with self.assertRaises((ValueError, UnicodeError)):
                review.decode_reviewed(unsupported(13, raw), '8905226')

    def test_replacement_preserves_existing_runs_objects_and_every_source_field(self):
        run = unsupported(13, '/* 한글 */'.encode('cp949'))
        source = {'paragraphs': [{'runs': [{'kind': 'text', 'text': 'prefix', 'encoding': 'ascii'}, run,
                                         {'kind': 'object', 'text': '[object:figure]', 'source_spans': []}],
                                  'text': 'old projection', 'format': {'tab_stops': [120]}}],
                  'issues': [{'source_spans': run['source_spans'], 'reason': run['reason']}],
                  'accounting': [{'byte_offset': 5}], 'final_state': {'font': 13}, 'metadata': ['retained']}
        before = deepcopy(source)
        actual = review.expected_topic(source, '9203182')
        self.assertEqual(source, before)
        self.assertEqual(actual['paragraphs'][0]['text'], 'prefix/* 한글 */[object:figure]')
        expected = deepcopy(source)
        new_run = expected['paragraphs'][0]['runs'][1]
        new_run.pop('reason'); new_run.pop('original_bytes_hex')
        new_run.update(kind='text', text='/* 한글 */', encoding='cp949')
        expected['paragraphs'][0]['text'] = 'prefix/* 한글 */[object:figure]'
        expected['issues'] = []
        self.assertEqual(actual, expected)
        source['issues'].append({'reason': 'Unrelated source error'})
        with self.assertRaises(ValueError): review.expected_topic(source, '9203182')

    def test_historical_and_review_output_roots_are_protected(self):
        for name in ('cd1-batch', 'cd1-associations', 'cd1-association-sample', 'cd1-association-pass',
                     'cd1-font-review', 'cd1-font-sample', 'cd1-font-pass', 'cd1-ordinary-font-review'):
            for path in (ROOT / 'build' / name, ROOT / 'build' / name / 'nested'):
                with self.assertRaises(ValueError): retry.safe_output(path)
        for path in (ROOT / 'build', ROOT, Path('/tmp/ordinary-font-output')):
            with self.assertRaises(ValueError): retry.safe_output(path)
        self.assertEqual(retry.safe_output(retry.OUTPUT), retry.OUTPUT)


class OrdinaryFontArtifacts(unittest.TestCase):
    def test_review_preserves_all_ten_topics_and_binds_exact_five_source_jobs(self):
        if not review.RECORD.exists(): self.skipTest('16a audit unavailable')
        record = read_json(review.RECORD); root = ROOT / record['output_root']
        if not root.exists(): self.skipTest('Private 16a audit unavailable')
        checked_file(ROOT, record['current_record'])
        prior = read_json(ROOT / record['prior_review_record']['path'])
        checked_file(ROOT, record['prior_review_record'])
        for item in record['outputs']: checked_file(root, item)
        self.assertEqual(record['counts'], {'articles': 5, 'source_topics': 10, 'reviewed_runs': 3425, 'non_ASCII_runs': 18})
        policy = read_json(root / 'policy.json')['article_fonts']
        rows = read_json(root / 'jobs.json'); evidence = read_json(root / 'runs.json')
        self.assertEqual(set(policy), set(review.CASES))
        self.assertEqual(len(evidence), 18)
        for row in rows:
            ref = row['source_reference']
            self.assertEqual(policy[ref]['source_topics'], row['source_topics'])
            self.assertEqual(policy[ref]['font_codecs'], {str(review.CASES[ref]['font']): 'cp949'})
            before = read_json(ROOT / prior['output_root'] / f'articles/{ref}/recovery.json')
            self.assertEqual(read_json(root / f'articles/{ref}/recovery.json'),
                             {**before, 'topics': [review.expected_topic(t, ref) for t in before['topics']]})

    def test_sample_packages_checkpoints_and_runtime_hashes_validate(self):
        if not retry.RECORD.exists(): self.skipTest('16a sample unavailable')
        record = read_json(retry.RECORD); root = ROOT / record['output_root']
        if not root.exists(): self.skipTest('Private 16a sample unavailable')
        self.assertEqual(set(record['sample']), set(review.SAMPLE))
        self.assertEqual(len(record['jobs']), 4)
        self.assertNotIn('9207134', record['sample'])
        for item in record['checkpoint_outputs']: checked_file(ROOT / record['checkpoints_root'], item)
        runtime = {}
        for row in record['jobs']:
            self.assertEqual(row['result']['status'], 'prepared')
            package = root / row['result']['package'] / 'content'
            bundle, _, _ = load_package(package)
            self.assertEqual(len(bundle['articles']), 1)
            ref = bundle['articles'][0]['source']['reference']
            for path in package.rglob('*'):
                if path.is_file(): runtime[ref + '/' + path.relative_to(package).as_posix()] = digest(path.read_bytes())
        self.assertEqual(runtime, record['runtime_files'])
        for issue, result in record['issues'].items():
            bundle, _, counts = load_package(root / result['package'] / 'content')
            self.assertEqual(counts, result['counts'])
            self.assertEqual({a['issue_id'] for a in bundle['articles']}, {issue})
