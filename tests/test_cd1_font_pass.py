"""15b scope, combined payload preservation and actual current handoff checks."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from tools.batch import font_pass, font_coverage
from tools.run_cd1_batch import ROOT, read_json
from maso_archive.reading_room_package import file_record, checked_file, load_package


def record(job, status='failed', error='Undecoded text retained in recovery evidence'):
    return {'job_id':job,'article_id':job,'issue_id':'issue','source_reference':job,
            'result':{'status':status,'error':error},'outcome':status}


def package(ids, root=Path('/unused'), media=None):
    return ({'articles':[{'id':i,'issue_id':'issue','text':'synthetic'} for i in ids],
             'media':{'items':media or []}}, {'previews':[]}, root)


class FontPassTests(unittest.TestCase):
    def test_overlay_only_replaces_eligible_font_failures_without_mutating_history(self):
        original=[record('old','prepared'),record('retry'),record('deferred')]
        snapshot=deepcopy(original);new=record('retry','prepared')
        self.assertEqual(font_pass.overlay(original,[new],{'retry'}),[original[0],new,original[2]])
        self.assertEqual(original,snapshot)
        for bad in ([record('deferred','prepared')],[record('old','prepared')],[new,new],[record('missing','prepared')]):
            with self.assertRaises(ValueError):font_pass.overlay(original,bad,{'retry'})
        changed=deepcopy(new);changed['source_reference']='changed'
        with self.assertRaises(ValueError):font_pass.overlay(original,[changed],{'retry'})
        with self.assertRaises(ValueError):font_pass.overlay([record('retry',error='Unsupported RTF constructs')],[new],{'retry'})

    def test_merge_carries_multi_article_issue_and_adds_standalone_without_mutation(self):
        packages=[package(['b','a']),package(['c'])];snapshot=deepcopy(packages)
        articles,media,assets,previews=font_pass.merge_packages(packages,'issue')
        self.assertEqual([a['id'] for a in articles],['a','b','c'])
        self.assertEqual(packages,snapshot)
        self.assertEqual((media,assets,previews),([],{},[]))
        self.assertEqual(articles[0],snapshot[0][0]['articles'][1])

    def test_merge_rejects_duplicate_and_wrong_issue_articles(self):
        for packages,issue in (([package(['a','b']),package(['b'])],'issue'),([package(['a'])],'other')):
            with self.assertRaises(ValueError):font_pass.merge_packages(packages,issue)

    def test_conflicting_shared_media_or_asset_bytes_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            a=Path(directory)/'a';b=Path(directory)/'b';a.mkdir();b.mkdir()
            (a/'asset').write_bytes(b'first');(b/'asset').write_bytes(b'second')
            first={'id':'media','asset':file_record('asset',b'first')}
            second={'id':'media','asset':file_record('asset',b'second')}
            packages=[package(['old'],a,[first]),package(['new'],b,[second])]
            with self.assertRaises(ValueError):font_pass.merge_packages(packages,'issue')
            second['id']='different'
            with self.assertRaises(ValueError):font_pass.merge_packages(packages,'issue')
            (b/'asset').write_bytes(b'first');packages[1][0]['media']['items']=[deepcopy(first)]
            articles,media,assets,_=font_pass.merge_packages(packages,'issue')
            self.assertEqual(len(articles),2);self.assertEqual(len(media),1);self.assertEqual(assets,{'asset':b'first'})

    def test_preservation_covers_article_preview_and_assets_but_allows_new_indexes(self):
        article={'kind':'article','path':'article.json'};preview={'path':'preview.md'};asset={'path':'image.png'}
        manifest={'documents':[{'kind':'catalog'},{'kind':'issue'},article,{'kind':'media_index'}],'previews':[preview]}
        bundle={'media':{'items':[{'asset':asset},{'asset':None}]}}
        self.assertEqual(font_coverage.preserved_files(bundle,manifest),[article,preview,asset])


@unittest.skipUnless(font_coverage.RECORD.exists(),'15b report unavailable')
class FontPassArtifacts(unittest.TestCase):
    def test_complete_scope_history_and_all_current_issue_packages(self):
        summary=read_json(font_coverage.RECORD);root=ROOT/summary['coverage_root']
        if not root.exists():self.skipTest('Private 15b coverage unavailable')
        checked_file(ROOT,summary['previous_record']);checked_file(ROOT,summary['previous_execution_manifest'])
        for item in summary['outputs']:checked_file(root,item)
        counts=summary['counts']
        self.assertEqual((counts['retry_candidates'],counts['new_attempts'],counts['carried_sample'],counts['deferred_font_candidates']),(33,27,6,53))
        self.assertEqual(sum(counts['current_outcomes'].values()),1088)
        self.assertEqual(counts['current_prepared'],944+counts['additional_prepared_since_14b'])
        self.assertEqual(len(summary['issues']),72)
        previous=read_json(font_pass.PREVIOUS)
        old={r['issue_id']:set(r['article_ids']) for r in previous['issues']};seen=set()
        for issue in summary['issues']:
            bundle,_,actual=load_package(ROOT/summary['output_root']/issue['package']/'content')
            ids=[a['id'] for a in bundle['articles']]
            self.assertEqual(actual,issue['counts']);self.assertEqual(ids,issue['article_ids'])
            self.assertTrue(old[issue['issue_id']]<=set(ids));self.assertFalse(seen & set(ids));seen.update(ids)
        self.assertEqual(len(seen),counts['current_prepared'])
        self.assertEqual(len(font_pass.table(summary,'retry_history')),33)
        self.assertEqual(font_pass.table(summary,'association_retry_history'),font_pass.table(previous,'retry_history'))
