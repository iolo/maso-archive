"""Current issue merging, retry-history reconciliation and 14b artifact checks."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from tools.batch.association_pass import merge_bundles
from tools.batch.association_coverage import current_records, qualify, RECORD
from tools.run_cd1_batch import ROOT, read_json
from maso_archive.reading_room_package import file_record, checked_file, load_package


def preparation(job, article, status='prepared'):
    return {'job_id': job, 'article_id': article, 'issue_id': 'issue', 'source_reference': article,
            'result': {'status': status}, 'outcome': status}


def package(entry, root, media=None):
    return (entry, {'articles': [{'id': entry['article_id'], 'issue_id': entry['issue_id'], 'preserved': {'text': 'synthetic source'}}],
                    'media': {'items': media or []}}, {'previews': []}, root)


class CurrentPackageTests(unittest.TestCase):
    def test_combines_distinct_histories_without_changing_article_content(self):
        before = [package(preparation('job-b', 'b'), Path('/unused')), package(preparation('job-a', 'a'), Path('/unused'))]
        snapshot = deepcopy(before)
        articles, media, assets, previews = merge_bundles(before, 'issue')
        self.assertEqual([a['id'] for a in articles], ['a', 'b'])
        self.assertEqual(before, snapshot)
        self.assertEqual(articles, [snapshot[1][1]['articles'][0], snapshot[0][1]['articles'][0]])
        self.assertEqual((media, assets, previews), ([], {}, []))

    def test_duplicates_wrong_issue_and_unavailable_articles_cannot_enter_package(self):
        original = package(preparation('job', 'article'), Path('/unused'))
        for other in [package(preparation('job', 'different'), Path('/unused')),
                      package(preparation('different', 'article'), Path('/unused')),
                      package(preparation('failed', 'failed', 'failed'), Path('/unused'))]:
            with self.assertRaises(ValueError):
                merge_bundles([original, other], 'issue')
        with self.assertRaises(ValueError):
            merge_bundles([original], 'other-issue')

    def test_shared_media_and_asset_collisions_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            roots = [Path(directory) / n for n in ('a', 'b')]
            for root, raw in zip(roots, (b'one', b'two')):
                root.mkdir()
                (root / 'asset.bin').write_bytes(raw)
            a = {'id': 'media', 'asset': file_record('asset.bin', b'one')}
            b = {'id': 'media', 'asset': file_record('asset.bin', b'two')}
            entries = [package(preparation('a', 'a'), roots[0], [a]), package(preparation('b', 'b'), roots[1], [b])]
            with self.assertRaises(ValueError):
                merge_bundles(entries, 'issue')
            # Distinct media IDs still cannot assign different bytes to one path.
            entries[1][1]['media']['items'][0]['id'] = 'different-media'
            with self.assertRaises(ValueError):
                merge_bundles(entries, 'issue')
            (roots[1] / 'asset.bin').write_bytes(b'one')
            entries[1][1]['media']['items'][0] = deepcopy(a)
            articles, media, assets, _ = merge_bundles(entries, 'issue')
            self.assertEqual(len(articles), 2)
            self.assertEqual(len(media), 1)
            self.assertEqual(assets, {'asset.bin': b'one'})


class CurrentCoverageTests(unittest.TestCase):
    def test_only_intended_failures_can_be_replaced_and_history_is_immutable(self):
        old = preparation('old', 'old')
        failed = preparation('retry', 'retry', 'failed')
        failed['result']['error'] = 'Related content outside selected topics needs ownership review'
        originals = [old, failed]
        snapshot = deepcopy(originals)
        retry = preparation('retry', 'retry')
        self.assertEqual(current_records(originals, [retry]), [old, retry])
        self.assertEqual(originals, snapshot)
        for bad in ([retry, retry], [preparation('old', 'old')], [preparation('unknown', 'unknown')], [preparation('retry', 'wrong-identity')]):
            with self.assertRaises(ValueError):
                current_records(originals, bad)
        unrelated = deepcopy(failed)
        unrelated['result']['error'] = 'Undecoded text'
        with self.assertRaises(ValueError):
            current_records([old, unrelated], [retry])

    def test_provenance_paths_keep_their_source_roots_without_mutating_history(self):
        record = {**preparation('j', 'a'), 'source_evidence': {'path': 'evidence/job.json', 'sha256': 'source'},
                  'failure_evidence': [{'path': 'evidence/failure.json', 'sha256': 'error'}]}
        record['result']['package'] = 'stages/package'
        snapshot = deepcopy(record)
        result = qualify(record, 'build/batch', 'build/checkpoint')
        self.assertEqual(result['result']['package'], 'build/batch/stages/package')
        self.assertEqual(result['source_evidence']['path'], 'build/checkpoint/evidence/job.json')
        self.assertEqual(result['failure_evidence'][0]['path'], 'build/checkpoint/evidence/failure.json')
        self.assertEqual(record, snapshot)


@unittest.skipUnless(RECORD.exists(), '14b complete-pass record unavailable')
class AssociationPassArtifactTests(unittest.TestCase):
    def test_complete_retry_population_and_all_combined_issue_packages(self):
        record = read_json(RECORD)
        root = ROOT / record['coverage_root']
        if not root.exists():
            self.skipTest('Private current coverage unavailable')
        counts = record['counts']
        self.assertEqual((counts['retry_candidates'], counts['new_attempts'], counts['carried_sample']), (470, 464, 6))
        self.assertEqual(sum(counts['current_outcomes'].values()), 1088)
        self.assertEqual(counts['current_prepared'], 537 + counts['additional_prepared_since_13d'])
        checked_file(ROOT, record['first_pass_record'])
        checked_file(ROOT, record['first_pass_execution_manifest'])
        for item in record['outputs']:
            checked_file(root, item)
        articles = set()
        for issue in record['issues']:
            bundle, _, actual = load_package(ROOT / record['output_root'] / issue['package'] / 'content')
            self.assertEqual(actual, issue['counts'])
            ids = [a['id'] for a in bundle['articles']]
            self.assertEqual(ids, issue['article_ids'])
            self.assertFalse(articles & set(ids))
            articles.update(ids)
        self.assertEqual(len(articles), counts['current_prepared'])
        self.assertEqual(len(record['issues']), 72)
