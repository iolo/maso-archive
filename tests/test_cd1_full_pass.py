"""First-pass outcomes, durable failure evidence and complete source reconciliation."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from tools.batch.full_pass import outcome, persist_job, verify_job, metadata_issue
from tools.batch.report import reconcile, exception_category, verify_generated_coverage, RECORD
from tools.cd1_batch_cache import Cache, key
from maso_archive.reading_room_package import checked_file, load_package
from maso_archive.reading_room import catalog_for
from tools.map_cd1_topic import ROOT


class OutcomeTests(unittest.TestCase):
    def test_unavailable_jobs_never_count_as_extracted(self):
        self.assertEqual(outcome({'status': 'failed'}), 'failed')
        self.assertEqual(outcome({'status': 'blocked'}), 'blocked')
        self.assertEqual(outcome({'status': 'prepared', 'semantic_review': 'reviewed_source_decisions'}), 'prepared')
        for extra in ({'semantic_review': 'pending'}, {'deferred_media': ['image']},
                      {'auxiliaries': [{'recovery_status': 'recovered', 'media': ['unrendered']}]}):
            self.assertEqual(outcome({'status': 'prepared', **extra}), 'prepared_with_review_exceptions')
        with self.assertRaises(ValueError):
            outcome({'status': 'silently_skipped'})

    def test_failure_evidence_survives_resume_and_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            runner = SimpleNamespace(output=base / 'batch', identity={'pipeline': 'test'})
            cache = Cache(runner.output / 'stages', runner.identity)
            def fail(stage):
                (stage / 'source.rtf').write_bytes(b'original undecoded source')
                raise ValueError('unsupported source')
            with self.assertRaises(ValueError):
                cache.stage('job-recovery', {}, fail)
            job = {'id': 'cd1:job:one', 'candidate_article_id': 'cd1:article:one', 'source_reference': 'one', 'issue_id': 'maso-1988-01'}
            root = base / 'pass'
            record = persist_job(root, runner, job, {'status': 'failed', 'error': 'unsupported source'}, cache.events)
            self.assertTrue(record['retry'])
            self.assertEqual(len(record['failure_evidence']), 2)
            self.assertEqual(verify_job(root, runner.output, record, key(runner.identity)), record)
            evidence = next(e for e in record['failure_evidence'] if e['path'].endswith('source.rtf'))
            (root / evidence['path']).write_bytes(b'damaged')
            with self.assertRaises(ValueError):
                verify_job(root, runner.output, record, key(runner.identity))

    def test_issue_without_successful_articles_retains_a_valid_metadata_package(self):
        bundle = json.loads((ROOT / 'examples/reading-room-v1.json').read_bytes())
        bundle['articles'] = []
        bundle['media']['items'] = []
        for issue in bundle['issues']:
            issue['cover_media_id'] = None
            for entry in issue['toc']:
                entry.update(article_ids=[], link_status='unmatched')
        bundle['catalog'] = catalog_for(bundle['issues'], [])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runner = SimpleNamespace(output=root, cache=Cache(root / 'stages', {}), bundle=lambda *args: bundle)
            result = metadata_issue(runner, bundle['issues'][0]['id'], [{'id': 'blocked-job'}])
            self.assertEqual(result['status'], 'metadata_only')
            loaded, _, counts = load_package(root / result['package'] / 'content')
            self.assertEqual(counts['articles'], 0)
            self.assertEqual(counts['toc_entries'], 2)
            self.assertTrue(all(not t['article_ids'] for t in loaded['issues'][0]['toc']))

    def test_exception_categories_preserve_unsupported_source_distinctions(self):
        self.assertEqual(exception_category({'status': 'blocked'}), 'source_topic_ownership')
        self.assertEqual(exception_category({'status': 'failed', 'error': 'Undecoded text retained in recovery evidence'}), 'font_or_decoding_policy')
        self.assertEqual(exception_category({'status': 'failed', 'error': 'Related content outside selected topics'}), 'unreviewed_linked_content')


def populations():
    jobs = [{'id': 'j' + str(n), 'candidate_article_id': 'a' + str(n), 'source_reference': 'r' + str(n),
             'issue_id': 'issue', 'title': 'metadata', 'source_topics': [{'id': 't' + str(n)}],
             'toc': {'matched_ids': ['toc' + str(n)]}, 'occurrence_ids': ['e' + str(n)] if n < 3 else []} for n in range(1, 4)]
    topics = [{'id': 't' + str(n), 'role': role, 'native': {'ordinal': n}, 'rtf': {'sha256': str(n)}, 'aliases': [], 'links': []}
              for n, role in enumerate(['dated_article_candidate', 'dated_article_candidate', 'dated_article_candidate',
                                        'unattributed_content', 'navigation', 'formatting_separator', 'linked_auxiliary_topic'], 1)]
    references = [{'reference': 'r' + str(n), 'job_id': 'j' + str(n), 'topic_id': 't' + str(n), 'occurrence_ids': ['e' + str(n)]} for n in (1, 2)]
    references.append({'reference': 'menu', 'job_id': None, 'topic_id': 't5', 'occurrence_ids': ['e4']})
    toc = [{'toc_entry_id': 'toc' + str(n), 'matched_job_ids': ['j' + str(n)] if n < 4 else [],
            'candidate_job_ids': [], 'status': 'metadata_match' if n < 4 else 'no_match'} for n in range(1, 5)]
    data = {'jobs': jobs, 'topics': topics, 'contexts': [{'topic_id': 't1'}, {'topic_id': 't5'}],
            'references': references, 'entries': [{'id': 'e' + str(n)} for n in range(1, 5)], 'toc': toc,
            'review_items': [{'topic_ids': ['t4']} ]}
    records = [{'job_id': 'j' + str(n), 'article_id': 'a' + str(n), 'issue_id': 'issue', 'outcome': status,
                'result': {'status': status, 'package': 'package' if status == 'prepared' else None},
                'source_evidence': {}, 'failure_evidence': [], 'retry': {'job_id': 'j' + str(n)}}
               for n, status in enumerate(['prepared', 'failed', 'blocked'], 1)]
    prepared = {'a1': {'id': 'a1', 'toc_entry_ids': ['toc1']}}
    return data, records, prepared


class PopulationTests(unittest.TestCase):
    def test_cached_report_cannot_hide_changed_regenerated_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Cache(Path(directory), {})
            def produce(stage):
                (stage / 'catalog.jsonl').write_bytes(b'original report\n')
            path, manifest = cache.stage('coverage', {}, produce)
            verify_generated_coverage(path, manifest, {'catalog.jsonl': b'original report\n'})
            # The stored report is checksum-valid, but freshly computed output differs.
            with self.assertRaises(ValueError):
                verify_generated_coverage(path, manifest, {'catalog.jsonl': b'changed report\n'})
            with self.assertRaises(ValueError):
                verify_generated_coverage(path, manifest, {})

    def test_every_source_population_and_unavailable_toc_link_remains_explicit(self):
        data, records, prepared = populations()
        result = reconcile(data, records, prepared, {'t7'}, [])
        self.assertEqual(len(result['topics']), 7)
        self.assertEqual([t['state'] for t in result['topics']], ['prepared_article_content', 'failed', 'blocked',
                         'unattributed_source_retained', 'non_article_source_retained', 'formatting_source_retained', 'auxiliary_text_recovered'])
        self.assertEqual([t['article_ids'] for t in result['toc']], [['a1'], [], [], []])
        self.assertEqual([e['content_available'] for e in result['references']], [True, False, False])
        self.assertEqual(len(result['entries']), 4)
        self.assertEqual(len(result['exceptions']), 2)
        self.assertEqual([c['content_status'] for c in result['catalog']], ['available', 'unavailable', 'unavailable'])

    def test_omitted_duplicated_and_falsely_prepared_jobs_fail_reconciliation(self):
        data, records, prepared = populations()
        for bad in (records[:-1], [records[0], records[0], records[2]]):
            with self.assertRaises(ValueError):
                reconcile(data, bad, prepared, set(), [])
        with self.assertRaises(ValueError):
            reconcile(data, records, {**prepared, 'a2': {'id': 'a2', 'toc_entry_ids': ['toc2']}}, set(), [])

    def test_omitted_or_invented_toc_links_are_rejected(self):
        data, records, prepared = populations()
        for ids in ([], ['toc1', 'invented']):
            changed = deepcopy(prepared)
            changed['a1']['toc_entry_ids'] = ids
            with self.assertRaises(ValueError):
                reconcile(data, records, changed, set(), [])


@unittest.skipUnless(RECORD.exists(), 'Complete CD1 first-pass artifacts not yet available')
class FullPassArtifactTests(unittest.TestCase):
    def test_complete_population_counts_and_all_runtime_packages(self):
        record = json.loads(RECORD.read_bytes())
        if not (ROOT / record['coverage_root']).exists():
            self.skipTest('Private first-pass report unavailable')
        counts = record['counts']
        self.assertEqual(counts['candidates'], 1088)
        self.assertEqual(sum(counts['outcomes'].values()), 1088)
        self.assertEqual((counts['native_topics'], counts['native_contexts'], counts['index_occurrences']), (3099, 2103, 2462))
        self.assertEqual(counts['issues'], 72)
        for output in record['outputs']:
            checked_file(ROOT / record['coverage_root'], output)
        for issue in record['issues']:
            bundle, _, actual = load_package(ROOT / 'build/cd1-batch' / issue['package'] / 'content')
            self.assertEqual(actual, issue['counts'])
            self.assertEqual(bundle['issues'][0]['id'], issue['issue_id'])
