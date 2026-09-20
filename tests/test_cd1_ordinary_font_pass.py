"""16b scope gates, inherited exception history and combined package preservation."""
from copy import deepcopy
import unittest

from tools.batch import ordinary_font_pass as batch, ordinary_font_coverage as coverage
from tools.run_cd1_batch import ROOT, read_json
from tools.decode_cd1_paragraph import digest
from maso_archive.reading_room_package import checked_file, load_package


def population():
    jobs, rows, policy, previous = [], [], {}, []
    for ref, case in batch.font_review.CASES.items():
        topics = [{'id': ref, 'rtf': {'sha256': 'synthetic-source-' + ref}}]
        jobs.append({'id': ref, 'source_reference': ref, 'source_topics': topics})
        rows.append({'job_id': ref, 'status': 'source_bound_cp949_ready', 'source_topics': topics})
        policy[ref] = {'source_topics': topics, 'font_codecs': {str(case['font']): 'cp949'}}
        previous.append({'job_id': ref, 'article_id': ref, 'issue_id': 'issue', 'source_reference': ref,
                         'result': {'status': 'failed', 'error': 'Undecoded text retained in recovery evidence'}})
    return {'jobs': jobs}, rows, policy, previous


class OrdinaryFontPassTests(unittest.TestCase):
    def test_only_exact_five_reviewed_failures_are_selected_without_mutation(self):
        args = population(); snapshot = deepcopy(args)
        self.assertEqual(batch.select_reviewed_jobs(*args), args[0]['jobs'])
        self.assertEqual(args, snapshot)
        for change in ('duplicate', 'unreviewed', 'prepared', 'unrelated_failure'):
            data, rows, policy, previous = population()
            if change == 'duplicate': rows[-1] = deepcopy(rows[0])
            elif change == 'unreviewed': rows[0]['status'] = 'deferred'
            elif change == 'prepared': previous[0]['result']['status'] = 'prepared'
            else: previous[0]['result']['error'] = 'Unsupported RTF constructs'
            with self.assertRaises(ValueError): batch.select_reviewed_jobs(data, rows, policy, previous)

    def test_source_or_codec_drift_and_extra_article_policy_are_rejected(self):
        for change in ('source', 'codec', 'extra'):
            data, rows, policy, previous = deepcopy(population())
            first = next(iter(policy))
            if change == 'source': policy[first]['source_topics'] = [{'id': 'other'}]
            elif change == 'codec': policy[first]['font_codecs'] = {'2': 'ascii'}
            else: policy['other'] = deepcopy(policy[first])
            with self.assertRaises(ValueError): batch.select_reviewed_jobs(data, rows, policy, previous)

    def test_sample_gate_requires_four_distinct_reviewed_successes_and_one_remaining(self):
        data, _, _, _ = population()
        sample = {'pipeline_identity_sha256': 'pipeline',
                  'review_record_sha256': digest(batch.font_review.RECORD.read_bytes()),
                  'sample': batch.font_review.SAMPLE,
                  'jobs': [{'job_id': ref, 'result': {'status': 'prepared'}} for ref in batch.font_review.SAMPLE],
                  'verification': {'only_reviewed_source_bound_runs_changed': True}}
        self.assertEqual(batch.sample_job_ids(sample, data['jobs'], 'pipeline'), set(batch.font_review.SAMPLE))
        for change in ('pipeline', 'review', 'duplicate', 'failed', 'scope', 'verification'):
            bad = deepcopy(sample)
            if change == 'pipeline': bad['pipeline_identity_sha256'] = 'different'
            elif change == 'review': bad['review_record_sha256'] = 'different'
            elif change == 'duplicate': bad['jobs'][-1] = deepcopy(bad['jobs'][0])
            elif change == 'failed': bad['jobs'][0]['result']['status'] = 'failed'
            elif change == 'scope': bad['jobs'][0]['job_id'] = '9207134'
            else: bad['verification']['only_reviewed_source_bound_runs_changed'] = False
            with self.assertRaises(ValueError): batch.sample_job_ids(bad, data['jobs'], 'pipeline')


@unittest.skipUnless(coverage.RECORD.exists(), '16b coverage unavailable')
class OrdinaryFontPassArtifacts(unittest.TestCase):
    def test_all_current_issue_packages_preserve_previous_payloads_and_add_exact_retries(self):
        summary = read_json(coverage.RECORD); root = ROOT / summary['coverage_root']
        if not root.exists(): self.skipTest('Private 16b coverage unavailable')
        checked_file(ROOT, summary['previous_record']); checked_file(ROOT, summary['previous_execution_manifest'])
        for item in summary['outputs']: checked_file(root, item)
        counts = summary['counts']; previous = read_json(batch.PREVIOUS)
        self.assertEqual((counts['retry_candidates'], counts['new_attempts'], counts['carried_sample'], counts['deferred_font_candidates']), (5, 1, 4, 48))
        self.assertEqual(sum(counts['current_outcomes'].values()), 1088)
        self.assertEqual(counts['current_prepared'], 977 + counts['additional_prepared_since_15b'])
        self.assertEqual(len(summary['issues']), 72)
        old = {r['issue_id']: r for r in previous['issues']}; seen = set()
        for issue in summary['issues']:
            package = ROOT / summary['output_root'] / issue['package'] / 'content'
            bundle, _, actual = load_package(package)
            ids = [a['id'] for a in bundle['articles']]
            self.assertEqual(actual, issue['counts']); self.assertEqual(ids, issue['article_ids'])
            prior = old[issue['issue_id']]
            self.assertTrue(set(prior['article_ids']) <= set(ids)); self.assertFalse(seen & set(ids)); seen.update(ids)
            # Read the verified historical manifest; compare every article and preview
            # without a second full parse of all 977 historical articles here.
            old_root = ROOT / previous['output_root'] / prior['package'] / 'content'
            old_manifest = read_json(old_root / 'manifest.json')
            for item in [r for r in old_manifest['documents'] if r['kind'] == 'article'] + old_manifest['previews']:
                self.assertEqual(checked_file(package, item), checked_file(old_root, item))
        self.assertEqual(len(seen), counts['current_prepared'])

    def test_both_earlier_retry_histories_and_unretried_exception_annotations_survive(self):
        summary = read_json(coverage.RECORD)
        if not (ROOT / summary['coverage_root']).exists(): self.skipTest('Private 16b coverage unavailable')
        previous = read_json(batch.PREVIOUS)
        self.assertEqual(batch.table(summary, 'font_retry_history'), batch.table(previous, 'retry_history'))
        self.assertEqual(batch.table(summary, 'association_retry_history'), batch.table(previous, 'association_retry_history'))
        retries = batch.table(summary, 'retry_history')
        self.assertEqual(len(retries), 5)
        self.assertEqual({r['checkpoint']['origin'] for r in retries}, {'16a', '16b'})
        retry_ids = {r['job_id'] for r in retries}
        old = {r['job_id']: r for r in batch.table(previous, 'exceptions')}
        for row in batch.table(summary, 'exceptions'):
            if row['job_id'] in retry_ids: continue
            before = old[row['job_id']]
            self.assertEqual(row['retry'], before['retry'])
            self.assertEqual(row.get('font_review_status'), before.get('font_review_status'))
