"""Shared runner preservation, cache recovery and independent failure tests."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.cd1_batch_cache import Cache, key, verify
from tools.cd1_batch_core import inherited_states, map_blocks
from tools import inventory_cd1_rtf as inventory
from tools import recover_cd1_text as recovery
from tools import render_cd1_markdown as markdown
from tools.run_cd1_batch import Runner, select, isolate
from tools.build_cd1_batch_profiles import build, OUTPUT as PROFILES, BASELINE
from tools.map_cd1_topic import ROOT
from maso_archive.reading_room_package import load_package


class CacheTests(unittest.TestCase):
    def test_interruption_resume_and_corrupt_or_extra_output_rejection(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Cache(directory, {'pipeline': 1})
            calls = []
            def interrupted(root):
                (root / 'partial').write_text('source evidence')
                raise KeyboardInterrupt()
            with self.assertRaises(KeyboardInterrupt):
                cache.stage('decode', {}, interrupted)
            self.assertEqual(len(list(Path(directory).rglob('partial'))), 1)
            def produce(root):
                calls.append(1)
                (root / 'result').write_text('verified')
            first, manifest = cache.stage('decode', {}, produce)
            self.assertEqual(cache.stage('decode', {}, produce)[0], first)
            self.assertEqual(len(calls), 1)
            (first / 'result').write_text('damaged')
            cache.stage('decode', {}, produce)
            self.assertEqual(len(calls), 2)
            (first / 'unexpected').write_text('extra')
            cache.stage('decode', {}, produce)
            self.assertEqual(len(calls), 3)
            verify(first, manifest['fingerprint'])

    def test_source_config_version_invalidate_and_failed_validation_preserves_prior(self):
        with tempfile.TemporaryDirectory() as directory:
            def produce(root):
                (root / 'result').write_text('good')
            cache = Cache(directory, {'pipeline': 1})
            first, _ = cache.stage('package', {'source': 'a', 'config': 1}, produce)
            second, _ = cache.stage('package', {'source': 'b', 'config': 1}, produce)
            third, _ = cache.stage('package', {'source': 'b', 'config': 2}, produce)
            fourth, _ = Cache(directory, {'pipeline': 2}).stage('package', {'source': 'b', 'config': 2}, produce)
            self.assertEqual(len({first, second, third, fourth}), 4)
            def reject(root):
                raise ValueError('invalid package')
            with self.assertRaises(ValueError):
                cache.stage('package', {'source': 'c'}, produce, reject)
            self.assertEqual((first / 'result').read_text(), 'good')
            self.assertEqual(len(list(Path(directory).rglob('failure.json'))), 1)

    def test_symlink_outputs_are_not_reusable(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Cache(directory, {})
            def produce(root):
                (root / 'unsafe').symlink_to('/etc/hostname')
            with self.assertRaisesRegex(ValueError, 'Symlink'):
                cache.stage('stage', {}, produce)


class SharedRecoveryTests(unittest.TestCase):
    def test_scoped_inheritance_across_topic_boundaries_and_binary(self):
        prefix = b'{\\rtf1\\ansi\\deff4\\f5\\b\\fs24 {\\f15 ignored}\\page\n'
        raw = prefix + b'body\\par {\\bin5 \\f99}\\page\nend}'
        offsets = [len(prefix), raw.index(b'end}')]
        snapshots = inherited_states(raw, offsets)
        for state in snapshots.values():
            self.assertEqual(state['character'], {'font_id': 5, 'fs': 24, 'b': True, 'ul': False})
            self.assertEqual(state['unknown'], [])

    def test_unknown_inherited_formatting_is_retained(self):
        prefix = b'{\\rtf1\\cf7\\page\n'
        state = inherited_states(prefix + b'body}', [len(prefix)])[len(prefix)]
        self.assertEqual(state['unknown'], ['cf'])

    def test_new_unknown_formatting_after_plain_is_not_cleared_by_pard(self):
        prefix = b'{\\rtf1\\cf1\\plain\\cf2\\pard\\page\n'
        state = inherited_states(prefix + b'body}', [len(prefix)])[len(prefix)]
        self.assertEqual(state['unknown'], ['cf'])

    def test_generic_recovery_preserves_tabs_objects_and_unknown_structure(self):
        raw = b'\\pard\\f4\\b Title\\par\\b0  spaces\\tab x\\par \\{bmc test.bmp\\}\\par '
        report = inventory.inspect_topic(raw, 0, 4)
        report.update(ordinal=9, role='reference_target_body')
        topic = recovery.recover_topic(raw, report)
        article = {'schema_version': 1, 'cd_reference': '9302402a', 'topics': [topic]}
        mapping = map_blocks(article)
        self.assertEqual(mapping['blocks'][0]['kind'], 'unresolved')
        self.assertEqual(topic['paragraphs'][1]['text'], ' spaces\tx')
        self.assertEqual(mapping['blocks'][2]['object_refs'][0]['resource'], 'test.bmp')
        files, _ = markdown.render(article, mapping)
        self.assertIn(b'&#32;spaces', files['body.md'])
        self.assertEqual(sum(a['byte_length'] for a in topic['accounting']), len(raw))

    def test_unknown_font_retains_encoded_evidence(self):
        raw = b"\\f95 \\'b0\\'a1\\par "
        report = inventory.inspect_topic(raw, 0, 4)
        report.update(ordinal=9, role='reference_target_body')
        topic = recovery.recover_topic(raw, report)
        self.assertTrue(topic['issues'])
        self.assertEqual(topic['paragraphs'][0]['runs'][0]['kind'], 'unsupported')
        with self.assertRaises(ValueError):
            markdown.render({'schema_version': 1, 'cd_reference': 'native-abcdef', 'topics': [topic]}, map_blocks({'schema_version': 1, 'cd_reference': 'native-abcdef', 'topics': [topic]}))

    def test_unsupported_visible_control_cannot_recover_successfully(self):
        raw = b'\\f4 text\\cf2 more\\par '
        report = inventory.inspect_topic(raw, 0, 4)
        report.update(ordinal=9, role='reference_target_body')
        with self.assertRaisesRegex(ValueError, 'Unsupported visible control'):
            recovery.recover_topic(raw, report)

    def test_selectors_and_failure_isolation(self):
        jobs = [{'id': 'job-a', 'candidate_article_id': 'cd1:article:a', 'source_reference': 'a', 'issue_id': 'maso-1988-02', 'state': 'ready'},
                {'id': 'job-b', 'candidate_article_id': 'cd1:article:b', 'source_reference': 'b', 'issue_id': 'maso-1988-03', 'state': 'ready'},
                {'id': 'job-c', 'candidate_article_id': 'cd1:article:c', 'source_reference': 'c', 'issue_id': 'maso-1988-03', 'state': 'blocked', 'blockers': ['ownership']}]
        self.assertEqual(select(jobs, article='a'), jobs[:1])
        self.assertEqual(select(jobs, issue='1988-03'), jobs[1:])
        self.assertEqual(select(jobs, all_jobs=True), jobs)
        def process(job):
            if job['id'] == 'job-a':
                raise ValueError('broken article')
            return {'status': 'prepared'}
        self.assertEqual([r['status'] for r in isolate(jobs, process)], ['failed', 'prepared', 'blocked'])
        with self.assertRaises(ValueError):
            select(jobs, article='a', all_jobs=True)


@unittest.skipUnless(BASELINE.exists() and (ROOT / 'build/cd1-processing-inventory/manifest.json').exists(), 'Private CD1 sources unavailable')
class FebruaryBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.runner = Runner(Path(cls.temporary.name) / 'batch')
        cls.jobs = select(cls.runner.data['jobs'], issue='1988-02')
        cls.report = cls.runner.run(cls.jobs)

    def test_profiles_reproduce_without_publisher_text(self):
        self.assertEqual(json.loads(PROFILES.read_bytes()), build())
        self.assertEqual(len(build()['articles']), 6)

    def test_february_content_assets_links_and_review_evidence_preserved(self):
        self.assertTrue(all(j['status'] == 'prepared' for j in self.report['jobs']), self.report['jobs'])
        issue = self.report['issues']['maso-1988-02']
        self.assertEqual(issue['status'], 'prepared', issue)
        root = self.runner.output / issue['package']
        actual, manifest, counts = load_package(root / 'content')
        expected, previous_manifest, previous_counts = load_package(BASELINE)
        self.assertEqual(counts, previous_counts)
        self.assertEqual(sorted(actual['articles'], key=lambda a: a['id']), sorted(expected['articles'], key=lambda a: a['id']))
        self.assertEqual(sorted(actual['media']['items'], key=lambda m: m['id']), sorted(expected['media']['items'], key=lambda m: m['id']))
        self.assertEqual(actual['issues'], expected['issues'])
        for item in actual['media']['items']:
            if item['asset']:
                path = item['asset']['path']
                self.assertEqual((root / 'content' / path).read_bytes(), (BASELINE / path).read_bytes())
        provenance = json.loads((root / 'provenance.json').read_bytes())
        self.assertEqual(provenance['coverage'], self.runner.baseline_evidence['coverage'])
        self.assertEqual(counts['paragraphs'], 2821)
        self.assertEqual(counts['blocks'], 677)

    def test_resume_reuses_all_stages_and_single_article_keeps_independent_issue_members(self):
        self.runner.cache.events.clear()
        report = self.runner.run(self.jobs[:1])
        self.assertTrue(all(e['cache'] == 'hit' for e in report['events']), report['events'])
        self.assertEqual(report['issues']['maso-1988-02']['counts']['articles'], 6)

    def test_reviewed_decisions_reject_changed_text(self):
        row = self.report['jobs'][0]
        path = self.runner.output / row['stages']['recovery']['path'] / 'recovery.json'
        article = json.loads(path.read_bytes())
        profile = self.runner.profiles['articles'][article['cd_reference']]
        declaration = profile['decisions'][0]
        paragraph = next(t for t in article['topics'] if t['ordinal'] == declaration['topic'])['paragraphs'][declaration['first'] - 1]
        paragraph['text'] += 'changed'
        with self.assertRaisesRegex(ValueError, 'Source-bound decision text changed'):
            map_blocks(article, profile)

    def test_actual_runner_interruption_resume_and_decoder_failure_isolation(self):
        runner = Runner(Path(self.temporary.name) / 'fault-injection')
        first_two = select(runner.data['jobs'], issue='1988-02')[:2]
        original = recovery.recover_topic
        calls = []
        def interrupt_second_topic(*args, **kwargs):
            calls.append(1)
            if len(calls) == 2:
                raise KeyboardInterrupt()
            return original(*args, **kwargs)
        with patch('tools.run_cd1_batch.recovery.recover_topic', side_effect=interrupt_second_topic):
            with self.assertRaises(KeyboardInterrupt):
                runner.run(first_two[:1])
        partials = list(runner.output.rglob('.stage-*/recovery.json'))
        self.assertEqual(len(partials), 1)
        self.assertEqual(len(json.loads(partials[0].read_bytes())['topics']), 1)
        runner.cache.events.clear()
        resumed = runner.run(first_two[:1])
        self.assertEqual(resumed['jobs'][0]['status'], 'prepared')
        self.assertTrue(any(e['cache'] == 'hit' and e['stage'].endswith('-inventory') for e in resumed['events']))
        # A new pipeline configuration forces recovery again, allowing the same
        # run to demonstrate one failed article followed by one valid package.
        runner.cache = Cache(runner.output / 'stages', {**runner.identity, 'fault_probe': True})
        first_ordinal = first_two[0]['source_topics'][0]['native']['ordinal']
        def fail_first_article(rtf, report, *args, **kwargs):
            if report['ordinal'] == first_ordinal:
                raise ValueError('injected decoder failure')
            return original(rtf, report, *args, **kwargs)
        with patch('tools.run_cd1_batch.recovery.recover_topic', side_effect=fail_first_article):
            report = runner.run(first_two)
        self.assertEqual([j['status'] for j in report['jobs']], ['failed', 'prepared'])
        self.assertTrue(list(runner.output.rglob('failure.json')))
