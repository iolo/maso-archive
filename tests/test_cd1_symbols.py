"""Symbol glyph decisions, source ambiguity and invariant-punctuation preservation."""
from copy import deepcopy
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.batch import symbol_review as review, retry_symbol_sample as retry
from tools.run_cd1_batch import ROOT, read_json
from tools.decode_cd1_paragraph import digest
from maso_archive.reading_room_package import checked_file, load_package


def unsupported(raw, font=2):
    return {'kind': 'unsupported', 'format': {'font_id': font, 'fs': 18},
            'text': '[unsupported]', 'reason': f'Unsupported font {font}', 'encoding': 'cp949',
            'original_bytes_hex': raw.hex(), 'source_spans': [{'byte_offset': 0, 'byte_length': len(raw)}],
            'encoded_bytes': len(raw), 'encoded_sha256': digest(raw)}


def topic(run):
    return {'paragraphs': [{'runs': [run], 'text': run['text'], 'format': {'tab_stops': [120]}}],
            'issues': [{'source_spans': deepcopy(run['source_spans']), 'reason': run['reason']}],
            'accounting': [{'byte_offset': 0, 'byte_length': run['encoded_bytes']}],
            'ordinal': 1, 'source_span': {'byte_offset': 0, 'end_exclusive': run['encoded_bytes']},
            'final_state': {'font_id': 2}, 'metadata': ['retained']}


class SymbolPolicyTests(unittest.TestCase):
    def test_reference_distinguishes_ascii_letters_arrows_and_ambiguous_space(self):
        table = review.mapping_table()
        self.assertEqual({b:table[b] for b in b',123;'}, {b:[chr(b)] for b in b',123;'})
        self.assertEqual(''.join(table[b][0] for b in b'PRINT'), 'ΠΡΙΝΤ')
        self.assertEqual(table[ord('k')], ['κ'])
        self.assertEqual([table[b] for b in (0xac,0xad,0xae)], [['←'],['↑'],['→']])
        self.assertEqual(table[32], [' ', '\u00a0'])
        with patch.object(review, 'MAPPING_SHA256', 'changed'):
            with self.assertRaises(ValueError): review.mapping_table()

    def test_only_exact_invariant_repertoire_and_article_can_be_approved(self):
        for raw in (b'2,3,', b',13', b';', b'2'):
            self.assertEqual(review.decode_reviewed(unsupported(raw), '9210202'), (raw.decode(), 'ascii'))
        for raw in (b'PRINT', b'k;', b' ', b'-', b'\xae', b'\x00', b'\x7f', b''):
            with self.assertRaises(ValueError): review.decode_reviewed(unsupported(raw), '9210202')
        for ref in (*review.DEFERRED, 'other'):
            with self.assertRaises(ValueError): review.decode_reviewed(unsupported(b';'), ref)
            with self.assertRaises(ValueError): review.expected_topic({'paragraphs': [], 'issues': []}, ref)
        for run in (unsupported(b';', 4), {**unsupported(b';'), 'reason': 'Byte round-trip mismatch'}):
            with self.assertRaises(ValueError): review.decode_reviewed(run, '9210202')

    def test_approved_projection_keeps_font_source_fields_and_existing_code_errors(self):
        source = topic(unsupported(b'2'))
        source['paragraphs'][0]['runs'] = [{'kind':'text','text':'string(x'}, source['paragraphs'][0]['runs'][0], {'kind':'text','text':'x1-1)'}]
        before = deepcopy(source); actual = review.expected_topic(source, '9210202')
        self.assertEqual(source, before)
        # Preserve the missing source operator: no inferred repair to x2-x1.
        self.assertEqual(actual['paragraphs'][0]['text'], 'string(x2x1-1)')
        for field in ('metadata','accounting','final_state','source_span'):
            self.assertEqual(actual[field], before[field])
        for field in ('format','source_spans','encoded_bytes','encoded_sha256'):
            self.assertEqual(actual['paragraphs'][0]['runs'][1][field], before['paragraphs'][0]['runs'][1][field])
        source['issues'].append({'reason':'Unrelated issue'})
        with self.assertRaises(ValueError): review.expected_topic(source, '9210202')

    def test_deferred_bytes_are_checked_without_approving_glyphs(self):
        for raw in (b'PRINT', b'k;', b'  \xac\xac '):
            source = topic(unsupported(raw)); before = deepcopy(source)
            span = {'byte_offset':0,'byte_length':len(raw),'sha256':digest(raw)}
            check = review.font_declaration_review.retained_topic_checks(raw, source, span)
            self.assertEqual(source, before); self.assertEqual(check['mode'], 'retained_bytes_not_decoded_text')
            self.assertEqual(check['accounted_bytes'], len(raw))

    def test_all_previous_and_review_roots_are_protected(self):
        for name in ('cd1-batch','cd1-font-review','cd1-font-sample','cd1-font-pass',
                     'cd1-ordinary-font-review','cd1-ordinary-font-sample','cd1-ordinary-font-pass',
                     'cd1-font-declaration-review','cd1-font-declaration-sample','cd1-font-declaration-pass','cd1-symbol-review'):
            for p in (ROOT/'build'/name, ROOT/'build'/name/'nested'):
                with self.assertRaises(ValueError): retry.safe_output(p)
        for p in (ROOT/'build', Path('/tmp/symbol-output')):
            with self.assertRaises(ValueError): retry.safe_output(p)
        self.assertEqual(retry.safe_output(retry.OUTPUT), retry.OUTPUT)


class SymbolArtifacts(unittest.TestCase):
    def test_all_six_topics_and_all_fifteen_runs_keep_decisions_and_source(self):
        if not review.RECORD.exists(): self.skipTest('18a audit unavailable')
        record = read_json(review.RECORD); root = ROOT/record['output_root']
        if not root.exists(): self.skipTest('Private 18a audit unavailable')
        for item in record['outputs']: checked_file(root,item)
        checked_file(ROOT,record['mapping_reference']['file']); checked_file(ROOT,record['current_record'])
        prior = read_json(ROOT/record['prior_review_record']['path'])
        self.assertEqual((record['counts']['articles'], record['counts']['source_topics'], record['counts']['reviewed_runs']), (4,6,15))
        policy = read_json(root/'policy.json')['article_fonts']; self.assertEqual(set(policy), {'9210202'})
        for row in read_json(root/'jobs.json'):
            ref = row['source_reference']; before = read_json(ROOT/prior['output_root']/f'articles/{ref}/recovery.json')
            expected = {**before,'topics':[review.expected_topic(t,ref) for t in before['topics']]} if ref in review.READY else before
            self.assertEqual(read_json(root/f'articles/{ref}/recovery.json'), expected)
            self.assertEqual(row['status'], review.CASES[ref]['status'])
            if ref in review.DEFERRED:
                self.assertTrue(all(c['mode']=='retained_bytes_not_decoded_text' for c in row['source_checks']))
        runs = read_json(root/'runs.json'); self.assertEqual(len(runs),15)
        self.assertEqual(sum(r['policy_approved'] for r in runs),4)
        self.assertEqual({r['decision'] for r in runs}, {c['status'] for c in review.CASES.values()})

    def test_sample_package_and_runtime_hashes_preserve_the_exact_single_article(self):
        if not retry.RECORD.exists(): self.skipTest('18a sample unavailable')
        record = read_json(retry.RECORD); root=ROOT/record['output_root']
        if not root.exists(): self.skipTest('Private 18a sample unavailable')
        self.assertEqual(set(record['sample']), {'9210202'}); self.assertEqual(len(record['jobs']),1)
        for item in record['checkpoint_outputs']: checked_file(ROOT/record['checkpoints_root'],item)
        row=record['jobs'][0]; self.assertEqual(row['result']['status'],'prepared')
        package=root/row['result']['package']/'content'; bundle,_,_=load_package(package)
        self.assertEqual([a['source']['reference'] for a in bundle['articles']], ['9210202'])
        actual={'9210202/'+p.relative_to(package).as_posix():digest(p.read_bytes()) for p in package.rglob('*') if p.is_file()}
        self.assertEqual(actual,record['runtime_files'])
        for result in record['issues'].values():
            bundle,_,counts=load_package(root/result['package']/'content')
            self.assertEqual(counts,result['counts']); self.assertEqual(len(bundle['articles']),1)
