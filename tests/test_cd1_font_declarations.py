"""17a declaration scope, ambiguous-byte deferral and exact preservation evidence."""
from copy import deepcopy
from pathlib import Path
import unittest

from tools.batch import font_declaration_review as review, retry_font_declarations as retry
from tools.run_cd1_batch import ROOT, read_json
from tools.decode_cd1_paragraph import digest
from maso_archive.reading_room_package import checked_file, load_package


def unsupported(font, raw):
    return {'kind': 'unsupported', 'format': {'font_id': font, 'b': True},
            'text': '[unsupported]', 'reason': f'Unsupported font {font}', 'encoding': 'cp949',
            'original_bytes_hex': raw.hex(), 'source_spans': [{'byte_offset': 0, 'byte_length': len(raw)}],
            'encoded_bytes': len(raw), 'encoded_sha256': digest(raw)}


def topic(run):
    return {'paragraphs': [{'runs': [run], 'text': run['text'], 'format': {'tab_stops': [120]}}],
            'issues': [{'source_spans': deepcopy(run['source_spans']), 'reason': run['reason']}],
            'accounting': [{'byte_offset': 0, 'byte_length': run['encoded_bytes']}],
            'ordinal': 1, 'source_span': {'byte_offset': 0, 'end_exclusive': run['encoded_bytes']},
            'final_state': {'font_id': run['format']['font_id']}, 'metadata': ['retained']}


class FontDeclarationPolicyTests(unittest.TestCase):
    def test_ascii_spacing_parenthesis_and_strict_korean_use_the_selected_codec(self):
        for ref, font, text, codec in [('8910172', 1, ' ' * 14, 'ascii'), ('9108302', 72, '(', 'ascii'),
                                       ('9010204', 64, '/* 한글 */', 'cp949'), ('9107124', 73, '| 공개부', 'cp949'),
                                       ('9304171', 7, '윤곽선 폰트', 'cp949'), ('9304171', 0, ' ', 'ascii'),
                                       ('9306300', 7, 'EMS 메모리', 'cp949')]:
            self.assertEqual(review.decode_reviewed(unsupported(font, text.encode(codec)), ref), (text, codec))

    def test_round_trip_alone_cannot_accept_the_actual_ambiguous_case(self):
        raw = b'@1. 308, 83, 833 \xa4GET vsel ;'
        self.assertEqual(raw.decode('cp949').encode('cp949'), raw)
        self.assertNotIn('GET', raw.decode('cp949'))
        with self.assertRaises((ValueError, UnicodeError)):
            review.candidate_decode(unsupported(7, raw), '9309201')
        # Even unambiguous ASCII in this article has no approved policy.
        with self.assertRaises(ValueError): review.decode_reviewed(unsupported(7, b'GET'), '9309201')
        with self.assertRaises(ValueError): review.expected_topic({'paragraphs': [], 'issues': []}, '9309201')

    def test_wrong_fonts_articles_existing_errors_controls_and_invalid_bytes_fail_closed(self):
        cases = [('other', unsupported(7, b'hello')), ('9304171', unsupported(2, b'hello')),
                 ('8910172', unsupported(1, '한글'.encode('cp949')))]
        for raw in (b'\xb0', b'\x00', b'\n', b'\x7f', b'\x81\x41'):
            cases.append(('9304171', unsupported(7, raw)))
        altered = unsupported(7, b'hello'); altered['reason'] = 'Byte round-trip mismatch'
        cases.append(('9304171', altered))
        for ref, run in cases:
            with self.assertRaises((ValueError, UnicodeError)): review.decode_reviewed(run, ref)

    def test_mixed_codecs_preserve_all_existing_fields_and_unrelated_issues_cannot_clear(self):
        source = topic(unsupported(7, '한글'.encode('cp949')))
        extra = unsupported(0, b' ')
        source['paragraphs'][0]['runs'].extend([extra, {'kind': 'object', 'text': '[object:figure]'}])
        source['issues'].append({'source_spans': extra['source_spans'], 'reason': extra['reason']})
        before = deepcopy(source); actual = review.expected_topic(source, '9304171')
        self.assertEqual(source, before)
        self.assertEqual(actual['paragraphs'][0]['text'], '한글 [object:figure]')
        self.assertEqual([r.get('encoding') for r in actual['paragraphs'][0]['runs']], ['cp949', 'ascii', None])
        for name in ('metadata', 'accounting', 'final_state', 'source_span'):
            self.assertEqual(actual[name], source[name])
        self.assertEqual(actual['paragraphs'][0]['format'], source['paragraphs'][0]['format'])
        for old, new in zip(source['paragraphs'][0]['runs'], actual['paragraphs'][0]['runs']):
            for name in ('format', 'source_spans', 'encoded_sha256', 'encoded_bytes'):
                self.assertEqual(old.get(name), new.get(name))
        source['issues'].append({'reason': 'Unrelated issue'})
        with self.assertRaises(ValueError): review.expected_topic(source, '9304171')

    def test_deferred_source_byte_check_does_not_mutate_or_approve_text(self):
        raw = b'@1. 308, 83, 833 \xa4GET vsel ;'; source = topic(unsupported(7, raw))
        before = deepcopy(source); span = {'byte_offset': 0, 'byte_length': len(raw), 'sha256': digest(raw)}
        checked = review.retained_topic_checks(raw, source, span)
        self.assertEqual(source, before)
        self.assertEqual(checked['mode'], 'retained_bytes_not_decoded_text')
        self.assertEqual(checked['accounted_bytes'], len(raw))
        with self.assertRaises(ValueError): review.retained_topic_checks(raw + b'x', source, {**span, 'byte_length': len(raw) + 1})

    def test_all_historical_and_audit_output_roots_are_protected(self):
        for name in ('cd1-batch', 'cd1-associations', 'cd1-association-sample', 'cd1-association-pass',
                     'cd1-font-review', 'cd1-font-sample', 'cd1-font-pass', 'cd1-ordinary-font-review',
                     'cd1-ordinary-font-sample', 'cd1-ordinary-font-pass', 'cd1-font-declaration-review'):
            for path in (ROOT / 'build' / name, ROOT / 'build' / name / 'nested'):
                with self.assertRaises(ValueError): retry.safe_output(path)
        for path in (ROOT, ROOT / 'build', Path('/tmp/declaration-output')):
            with self.assertRaises(ValueError): retry.safe_output(path)
        self.assertEqual(retry.safe_output(retry.OUTPUT), retry.OUTPUT)


class FontDeclarationArtifacts(unittest.TestCase):
    def test_all_seven_sources_survive_and_the_ambiguous_article_has_no_policy(self):
        if not review.RECORD.exists(): self.skipTest('17a review unavailable')
        record = read_json(review.RECORD); root = ROOT / record['output_root']
        if not root.exists(): self.skipTest('Private 17a review unavailable')
        prior = read_json(ROOT / record['prior_review_record']['path'])
        checked_file(ROOT, record['prior_review_record']); checked_file(ROOT, record['current_record'])
        for item in record['outputs']: checked_file(root, item)
        self.assertEqual((record['counts']['articles'], record['counts']['source_topics'], record['counts']['reviewed_runs']), (7, 14, 799))
        self.assertEqual((record['counts']['accepted_runs'], record['counts']['accepted_non_ASCII_runs'], record['counts']['ambiguous_runs']), (703, 222, 1))
        policy = read_json(root / 'policy.json')['article_fonts']
        self.assertEqual(set(policy), review.READY); self.assertNotIn('9309201', policy)
        for row in read_json(root / 'jobs.json'):
            ref = row['source_reference']; before = read_json(ROOT / prior['output_root'] / f'articles/{ref}/recovery.json')
            if ref in review.READY:
                self.assertEqual(policy[ref]['source_topics'], row['source_topics'])
                self.assertEqual(policy[ref]['font_codecs'], review.CASES[ref]['font_codecs'])
                expected = {**before, 'topics': [review.expected_topic(t, ref) for t in before['topics']]}
            else:
                expected = before
                self.assertEqual(row['status'], 'deferred_ambiguous_source_byte')
                self.assertTrue(all(c['mode'] == 'retained_bytes_not_decoded_text' for c in row['source_checks']))
            self.assertEqual(read_json(root / f'articles/{ref}/recovery.json'), expected)
        evidence = read_json(root / 'runs.json')
        self.assertEqual(len(evidence), 799)
        ambiguous = [r for r in evidence if r['candidate']['status'] == 'deferred_ambiguous_bytes']
        self.assertEqual(len(ambiguous), 1); self.assertEqual(ambiguous[0]['reference'], '9309201')
        self.assertFalse(any(r['policy_approved'] for r in evidence if r['reference'] == '9309201'))

    def test_five_sample_packages_and_every_recorded_runtime_file_validate(self):
        if not retry.RECORD.exists(): self.skipTest('17a sample unavailable')
        record = read_json(retry.RECORD); root = ROOT / record['output_root']
        if not root.exists(): self.skipTest('Private 17a sample unavailable')
        self.assertEqual(set(record['sample']), set(review.SAMPLE)); self.assertEqual(len(record['jobs']), 5)
        self.assertFalse({'9306300', '9309201'} & set(record['sample']))
        for item in record['checkpoint_outputs']: checked_file(ROOT / record['checkpoints_root'], item)
        runtime = {}
        for row in record['jobs']:
            self.assertEqual(row['result']['status'], 'prepared')
            package = root / row['result']['package'] / 'content'; bundle, _, _ = load_package(package)
            self.assertEqual(len(bundle['articles']), 1); ref = bundle['articles'][0]['source']['reference']
            for path in package.rglob('*'):
                if path.is_file(): runtime[ref + '/' + path.relative_to(package).as_posix()] = digest(path.read_bytes())
        self.assertEqual(runtime, record['runtime_files'])
        for issue, result in record['issues'].items():
            bundle, _, counts = load_package(root / result['package'] / 'content')
            self.assertEqual(counts, result['counts']); self.assertEqual({a['issue_id'] for a in bundle['articles']}, {issue})
