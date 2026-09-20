"""Two-pipeline Symbol integration, immutable history and exact runtime preservation."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import tempfile
import unittest

from tools.batch import symbol_pass as batch, symbol_coverage as coverage
from tools.run_cd1_batch import ROOT, read_json
from tools.cd1_batch_cache import key, verify
from tools.decode_cd1_paragraph import digest
from maso_archive.reading_room_package import checked_file, load_package


def population():
    jobs=[];rows=[];previous=[]
    for ref,case in batch.symbol_review.CASES.items():
        topics=[{'id':ref,'rtf':{'sha256':'synthetic-'+ref}}]
        jobs.append({'id':ref,'source_reference':ref,'source_topics':topics})
        rows.append({'job_id':ref,'source_reference':ref,'source_topics':topics,'status':case['status']})
        previous.append({'job_id':ref,'article_id':ref,'issue_id':'issue','source_reference':ref,
                         'result':{'status':'failed','error':'Undecoded text retained in recovery evidence'}})
    return {'jobs':jobs},rows,previous


def sample(ref, pipeline='pipeline'):
    return {'checkpoint':'18b' if ref=='9208198' else '18a','pipeline_identity_sha256':pipeline,
            'review_record_sha256':digest(batch.symbol_review.RECORD.read_bytes()),'sample':{ref:'reviewed'},
            'jobs':[{'job_id':'cd1:job:'+ref,'outcome':'prepared_with_review_exceptions','result':{'status':'prepared','package':'article'}}],
            'verification':{'only_reviewed_source_bound_runs_changed':True,'source_boundaries_and_formatting_preserved':True},
            'checkpoint_outputs':[{'path':'jobs/'+ref+'.json','bytes':0,'sha256':'synthetic'}],
            'output_root':'build/synthetic','checkpoints_root':'build/synthetic/checkpoints'}


def preserved(root, manifest):
    media_record=next(r for r in manifest['documents'] if r['kind']=='media_index')
    import json
    media=json.loads(checked_file(root,media_record))
    return ([r for r in manifest['documents'] if r['kind']=='article'] + manifest['previews'] +
            [m['asset'] for m in media['items'] if m['asset']])


class SymbolPassTests(unittest.TestCase):
    def test_only_two_reviewed_font_failures_can_be_selected_without_mutation(self):
        args=population();before=deepcopy(args)
        self.assertEqual({j['source_reference'] for j in batch.eligible_jobs(*args)},set(batch.SAMPLES))
        self.assertEqual(args,before)
        for change in ('duplicate','prepared','unrelated_failure','source','missing'):
            data,rows,previous=population()
            if change=='duplicate':rows[-1]=deepcopy(rows[0])
            elif change=='prepared':previous[-1]['result']['status']='prepared'
            elif change=='unrelated_failure':previous[-1]['result']['error']='Unsupported RTF constructs'
            elif change=='source':rows[-1]['source_topics']=[{'id':'different'}]
            else:data['jobs'].pop()
            with self.assertRaises((ValueError,KeyError)):batch.eligible_jobs(data,rows,previous)

    def test_both_font_context_conflicts_remain_deferred(self):
        for ref in batch.DEFERRED:
            for change in ('promote','omit','identity'):
                data,rows,previous=population();row=next(r for r in rows if r['source_reference']==ref)
                if change=='promote':row['status']='source_bound_invariant_ascii_ready'
                elif change=='omit':rows.remove(row)
                else:row['source_reference']='9208198'
                with self.assertRaises(ValueError):batch.eligible_jobs(data,rows,previous)

    def test_each_sample_requires_its_own_pipeline_source_review_and_exact_job(self):
        for ref in batch.SAMPLES:
            job={'id':'cd1:job:'+ref,'source_reference':ref};s=sample(ref)
            self.assertEqual(batch.sample_pointer(s,job,'pipeline')['origin'],s['checkpoint'])
            for change in ('pipeline','checkpoint','review','scope','job','failed','verification','missing','duplicate'):
                bad=deepcopy(s)
                if change=='pipeline':bad['pipeline_identity_sha256']='other'
                elif change=='checkpoint':bad['checkpoint']='18c'
                elif change=='review':bad['review_record_sha256']='other'
                elif change=='scope':bad['sample']={'9205403':'unreviewed'}
                elif change=='job':bad['jobs'][0]['job_id']='other'
                elif change=='failed':bad['jobs'][0]['result']['status']='failed'
                elif change=='verification':bad['verification']['source_boundaries_and_formatting_preserved']=False
                elif change=='missing':bad['checkpoint_outputs']=[]
                else:bad['checkpoint_outputs']*=2
                with self.assertRaises(ValueError):batch.sample_pointer(bad,job,'pipeline')

    def test_runtime_inventory_and_arrow_policy_must_match_sample(self):
        ref='9208198';job={'id':'cd1:job:'+ref,'source_reference':ref}
        runner=SimpleNamespace(identity={'symbol_arrow_extension':{'synthetic':True}},arrow_policy={'synthetic':'review'})
        with tempfile.TemporaryDirectory(dir=ROOT/'build') as directory:
            root=Path(directory);content=root/'article/content';content.mkdir(parents=True)
            (content/'file.json').write_bytes(b'{}')
            s=sample(ref,key(runner.identity));s.update(output_root=root.relative_to(ROOT).as_posix(),
                glyph_policy_sha256=key(runner.arrow_policy),runtime_files={ref+'/file.json':digest(b'{}')})
            record=s['jobs'][0]
            with patch.object(batch,'read_json',return_value=s),patch.object(batch,'load_outcome',return_value=record):
                self.assertEqual(set(batch.verified_samples(runner,[job])),{job['id']})
                (content/'file.json').write_bytes(b'changed')
                with self.assertRaises(ValueError):batch.verified_samples(runner,[job])
                (content/'file.json').write_bytes(b'{}');(content/'extra.json').write_bytes(b'{}')
                with self.assertRaises(ValueError):batch.verified_samples(runner,[job])
                s['glyph_policy_sha256']='wrong'
                with self.assertRaises(ValueError):batch.verified_samples(runner,[job])


@unittest.skipUnless(coverage.RECORD.exists(),'18c coverage unavailable')
class SymbolPassArtifacts(unittest.TestCase):
    def test_all_issue_handoffs_preserve_previous_files_and_add_only_both_samples(self):
        summary=read_json(coverage.RECORD)
        if not (ROOT/summary['coverage_root']).exists():self.skipTest('Private 18c coverage unavailable')
        previous=read_json(batch.PREVIOUS);prior={r['issue_id']:r for r in previous['issues']}
        checked_file(ROOT,summary['previous_record']);checked_file(ROOT,summary['previous_execution_manifest'])
        for item in summary['outputs']:checked_file(ROOT/summary['coverage_root'],item)
        self.assertEqual((summary['counts']['current_prepared'],summary['counts']['new_attempts'],summary['counts']['carried_sample']),(990,0,2))
        samples={ref:read_json(path) for ref,path in batch.SAMPLES.items()};seen=set();added=set()
        for issue in summary['issues']:
            stage=ROOT/summary['output_root']/issue['package'];verify(stage,issue['fingerprint'])
            package=stage/'content';old=prior[issue['issue_id']]
            old_root=ROOT/previous['output_root']/old['package']/'content'
            old_manifest=read_json(old_root/'manifest.json');manifest=read_json(package/'manifest.json')
            new_ids=set(issue['article_ids'])-set(old['article_ids']);added.update(new_ids)
            self.assertFalse(seen & set(issue['article_ids']));seen.update(issue['article_ids'])
            if not new_ids:
                # All bytes are verified above; identical manifests inherit the
                # unchanged package's schema checks rather than parsing it twice.
                self.assertEqual(manifest,old_manifest);self.assertEqual(issue['counts'],old['counts'])
                self.assertEqual(issue['article_ids'],old['article_ids'])
            else:
                bundle,_,counts=load_package(package)
                self.assertEqual(counts,issue['counts']);self.assertEqual([a['id'] for a in bundle['articles']],issue['article_ids'])
            for item in preserved(old_root,old_manifest):
                self.assertEqual(checked_file(package,item),checked_file(old_root,item))
            for ref,s in samples.items():
                if 'cd1:article:'+ref not in new_ids:continue
                result=s['jobs'][0]['result'];sample_root=ROOT/s['output_root']/result['package']/'content'
                m=read_json(sample_root/'manifest.json')
                for item in preserved(sample_root,m):
                    self.assertEqual(checked_file(package,item),checked_file(sample_root,item))
        self.assertEqual(len(summary['issues']),72);self.assertEqual(len(seen),990)
        self.assertEqual(added,{'cd1:article:'+ref for ref in batch.SAMPLES})

    def test_all_histories_source_audits_and_deferred_decisions_survive(self):
        summary=read_json(coverage.RECORD)
        if not (ROOT/summary['coverage_root']).exists():self.skipTest('Private 18c coverage unavailable')
        previous=read_json(batch.PREVIOUS)
        for name,old in [('declaration_font_retry_history','retry_history'),('ordinary_font_retry_history','ordinary_font_retry_history'),
                         ('font_retry_history','font_retry_history'),('association_retry_history','association_retry_history')]:
            self.assertEqual(batch.table(summary,name),batch.table(previous,old))
        retries=batch.table(summary,'retry_history');self.assertEqual(len(retries),2)
        self.assertEqual({r['checkpoint']['origin'] for r in retries},{'18a','18b'})
        prior_checks=batch.table(previous,'source_checks');current_checks=batch.table(summary,'source_checks')
        self.assertEqual(current_checks[:len(prior_checks)],prior_checks)
        self.assertEqual({r['article_id'] for r in current_checks[len(prior_checks):]}, {'cd1:article:'+r for r in batch.SAMPLES})
        old={r['job_id']:r for r in batch.table(previous,'exceptions')}
        exceptions=batch.table(summary,'exceptions');self.assertEqual(len(exceptions),98)
        conflicts=[]
        for row in exceptions:
            before=old[row['job_id']];self.assertEqual(row['retry'],before['retry'])
            self.assertEqual(row.get('font_declaration_review'),before.get('font_declaration_review'))
            if 'symbol_review' in row:
                review=row['symbol_review'];conflicts.append(review['source_reference'])
                self.assertEqual(review['status'],'deferred_font_context_conflict');self.assertFalse(review['approved_policy'])
                checked_file(ROOT,review['record'])
            else:self.assertEqual(row.get('font_review_status'),before.get('font_review_status'))
        self.assertEqual(set(conflicts),batch.DEFERRED)
        self.assertEqual(summary['counts']['current_exception_categories']['font_or_decoding_policy'],40)
