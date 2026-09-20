"""Separate auxiliary ownership, source fidelity and bounded retry regressions."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from tools.batch.associations import review_links, recover_auxiliary, RECORD
from tools.batch.retry_associations import AssociationRunner, RECORD as SAMPLE_RECORD
from tools.run_cd1_batch import read_json, ROOT, OUTPUT as FIRST_OUTPUT
from tools.decode_cd1_paragraph import digest
from tools.cd1_batch_cache import verify
from tools.batch.full_pass import verify_job
from maso_archive.reading_room_package import checked_file, load_package


def fixture():
    span = {'byte_offset': 0, 'byte_length': 1, 'sha256': 'source-hash'}
    article = {'id': 'article-topic', 'native': {'ordinal': 2}, 'rtf': span, 'aliases': ['body'],
               'links': [{'alias': 'aux', 'target_topic_id': 'aux-topic', 'byte_offset': 0, 'byte_length': 1}]}
    aux = {'id': 'aux-topic', 'native': {'ordinal': 1}, 'role': 'linked_auxiliary_topic', 'rtf': span,
           'aliases': ['aux'], 'links': [], 'issue': None, 'owner_topic_id': None,
           'context_relation': 'at_native_header', 'incoming_topic_ids': ['article-topic']}
    job = {'id': 'job', 'source_reference': 'ref', 'candidate_article_id': 'article', 'issue_id': 'issue',
           'source_topics': [{k: article[k] for k in ('id', 'native', 'rtf', 'aliases')}]}
    return {'topics': [article, aux], 'jobs': [job]}, [{'category': 'unreviewed_linked_content', 'job_id': 'job'}]


class AssociationPolicyTests(unittest.TestCase):
    def test_linked_auxiliary_keeps_separate_identity_and_outgoing_links(self):
        data, exceptions = fixture()
        data['topics'][1]['links'] = [{'target_topic_id': 'unvisited-other-article'}]
        edges, destinations, retries = review_links(data, exceptions, {})
        self.assertEqual(edges[0]['action'], 'preserve_separate_auxiliary')
        self.assertEqual(set(destinations), {'aux-topic'})
        self.assertEqual(destinations['aux-topic']['links'], data['topics'][1]['links'])
        self.assertEqual(retries[0]['article_preparation'], 'not_retried')
        self.assertEqual(retries[0]['status'], 'association_policy_ready')
        self.assertEqual(len(data['jobs'][0]['source_topics']), 1)

    def test_owned_or_ambiguous_topics_are_not_silently_approved(self):
        data, exceptions = fixture()
        variants = []
        owned = deepcopy(data)
        owned['jobs'].append({'id': 'other-job', 'source_topics': [{'id': 'aux-topic'}]})
        variants.append(owned)
        for change in ({'role': 'dated_article_candidate'}, {'context_relation': 'unresolved_offset'},
                       {'incoming_topic_ids': []}, {'aliases': []}, {'owner_topic_id': 'other-topic'}):
            changed = deepcopy(data)
            changed['topics'][1].update(change)
            variants.append(changed)
        missing = deepcopy(data)
        missing['topics'].pop()
        variants.append(missing)
        for changed in variants:
            with self.subTest(changed=changed['topics'][-1]['id']):
                edges, destinations, retries = review_links(changed, exceptions, {})
                self.assertFalse(destinations)
                self.assertEqual(retries[0]['status'], 'blocked')
                self.assertEqual(edges[0]['action'], 'needs_ownership_review')

    def test_stale_source_and_duplicate_or_disappeared_failures_are_rejected(self):
        data, exceptions = fixture()
        changed = deepcopy(data)
        changed['jobs'][0]['source_topics'][0]['rtf'] = {**changed['topics'][0]['rtf'], 'sha256': 'changed'}
        with self.assertRaises(ValueError):
            review_links(changed, exceptions, {})
        with self.assertRaises(ValueError):
            review_links(data, exceptions * 2, {})
        with self.assertRaises(ValueError):
            review_links(data, exceptions, {'aux-topic': {}})

    def test_full_text_and_deferred_formatting_keep_original_bytes(self):
        raw = b'\\f4 Sample auxiliary\\par '
        topic = {'id': 'aux', 'native': {'ordinal': 1},
                 'rtf': {'byte_offset': 0, 'byte_length': len(raw), 'sha256': digest(raw)}}
        state = {'character': {'font_id': 4, 'fs': None, 'b': False, 'ul': False}, 'paragraph': {}, 'unknown': []}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = recover_auxiliary(root / 'ok', topic, raw, state, {4: 'cp949'}, {})
            self.assertEqual(result['status'], 'recovered')
            self.assertEqual(result['source_check']['accounted_bytes'], len(raw))
            self.assertEqual(read_json(root / 'ok/recovery.json')['paragraphs'][0]['text'], 'Sample auxiliary')
            unknown = {**state, 'unknown': ['unsupported-format']}
            result = recover_auxiliary(root / 'deferred', topic, raw, unknown, {4: 'cp949'}, {})
            self.assertEqual(result['status'], 'deferred')
            self.assertNotIn('source_check', result)
            self.assertEqual((root / 'deferred/source.rtf').read_bytes(), raw)
            self.assertEqual(read_json(root / 'deferred/inherited-state.json'), unknown)
            with self.assertRaises(ValueError):
                recover_auxiliary(root / 'changed', topic, b'!' + raw[1:], state, {4: 'cp949'}, {})

    def test_retry_cannot_write_inside_original_first_pass(self):
        with self.assertRaises(ValueError):
            AssociationRunner(FIRST_OUTPUT / 'accidental-retry')


@unittest.skipUnless(RECORD.exists() and SAMPLE_RECORD.exists(), 'Association review/sample unavailable')
class AssociationArtifactTests(unittest.TestCase):
    def test_complete_review_and_sample_preserve_first_pass_and_article_boundaries(self):
        review, sample = read_json(RECORD), read_json(SAMPLE_RECORD)
        root = ROOT / review['output_root']
        if not root.exists():
            self.skipTest('Private association artifacts unavailable')
        checked_file(ROOT, review['first_pass_unchanged'])
        manifest = verify(root, review['fingerprint'])
        self.assertEqual(manifest['outputs'], review['outputs'])
        self.assertEqual(review['counts']['affected_candidates'], 470)
        self.assertEqual(review['counts']['auxiliary_topics'], 111)
        self.assertEqual(sum(review['counts']['recovery_states'].values()), 111)
        self.assertEqual(len(sample['jobs']), 6)
        self.assertTrue(sample['verification']['all_selected_associations_passed'])
        checkpoint_root = ROOT / sample['checkpoints_root']
        for output in sample['checkpoint_outputs']:
            checked_file(checkpoint_root, output)
        for path in (checkpoint_root / 'jobs').glob('*.json'):
            result = verify_job(checkpoint_root, ROOT / sample['output_root'], read_json(path), sample['pipeline_identity_sha256'])
            if result['result']['status'] == 'prepared':
                bundle, _, _ = load_package(ROOT / sample['output_root'] / result['result']['package'] / 'content')
                self.assertEqual([a['id'] for a in bundle['articles']], [result['article_id']])
