"""19b selection gates, sample provenance and complete integration preservation."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import tempfile
import unittest

from tools.batch import oem_pass as batch, oem_coverage as coverage, oem_runs
from tools.run_cd1_batch import ROOT, read_json
from tools.cd1_batch_cache import key, verify
from tools.decode_cd1_paragraph import digest
from maso_archive.reading_room_package import checked_file, load_package


def population():
    jobs=[];rows=[];previous=[];policies={}
    refs=sorted(batch.codec_review.READY | batch.codec_review.SPLIT) + [f'other-{i}' for i in range(30)]
    for ref in refs:
        topics=[{'id':ref,'rtf':{'sha256':'synthetic-'+ref}}]
        jobs.append({'id':'cd1:job:'+ref,'source_reference':ref,'source_topics':topics})
        status=('source_bound_oem_policy_ready' if ref in batch.codec_review.READY else
                'deferred_cross_font_character_representation' if ref in batch.codec_review.SPLIT else
                'deferred_mixed_or_ambiguous_source')
        rows.append({'job_id':jobs[-1]['id'],'source_reference':ref,'source_topics':topics,'status':status})
        if ref in batch.codec_review.READY:policies[ref]={'reference':ref,'source_topics':topics}
        previous.append({'job_id':jobs[-1]['id'],'article_id':ref,'issue_id':'issue','source_reference':ref,
                         'result':{'status':'failed','error':'Undecoded text retained in recovery evidence'}})
    return {'jobs':jobs},rows,policies,previous


def sample(jobs,policies,pipeline='pipeline'):
    selected=[j for j in jobs if j['source_reference'] in batch.codec_review.SAMPLE]
    return {'checkpoint':'19a','pipeline_identity_sha256':pipeline,
            'review_record_sha256':digest(batch.codec_review.RECORD.read_bytes()),'sample':batch.codec_review.SAMPLE,
            'run_policies_sha256':key(policies),
            'jobs':[{'job_id':j['id'],'outcome':'prepared_with_review_exceptions',
                     'result':{'status':'prepared','package':j['source_reference']}} for j in selected],
            'verification':{'only_reviewed_source_bound_runs_changed':True,'source_boundaries_and_formatting_preserved':True},
            'checkpoint_outputs':[{'path':'jobs/'+j['source_reference']+'.json','bytes':0,'sha256':'synthetic'} for j in selected],
            'output_root':'build/synthetic','checkpoints_root':'build/synthetic/checkpoints'}


def preserved(root,manifest):
    import json
    media=json.loads(checked_file(root,next(r for r in manifest['documents'] if r['kind']=='media_index')))
    return ([r for r in manifest['documents'] if r['kind']=='article']+manifest['previews']+
            [m['asset'] for m in media['items'] if m['asset']])


class OemPassTests(unittest.TestCase):
    def test_only_exact_five_reviewed_failures_can_be_selected_without_mutation(self):
        args=population();before=deepcopy(args)
        self.assertEqual({j['source_reference'] for j in batch.eligible_jobs(*args)},batch.codec_review.READY)
        self.assertEqual(args,before)
        for change in ('duplicate','source','policy','scope','prepared','unrelated_failure','missing'):
            data,rows,policies,previous=population();ref=sorted(batch.codec_review.READY)[0]
            row=next(r for r in rows if r['source_reference']==ref)
            old=next(r for r in previous if r['source_reference']==ref)
            if change=='duplicate':rows[-1]=deepcopy(row)
            elif change=='source':row['source_topics']=[{'id':'wrong'}]
            elif change=='policy':policies[ref]['reference']='wrong'
            elif change=='scope':policies['unreviewed']={}
            elif change=='prepared':old['result']['status']='prepared'
            elif change=='unrelated_failure':old['result']['error']='Unsupported RTF constructs'
            else:data['jobs']=[j for j in data['jobs'] if j['source_reference']!=ref]
            with self.assertRaises((ValueError,KeyError)):batch.eligible_jobs(data,rows,policies,previous)

    def test_split_and_ambiguous_cases_cannot_be_promoted_or_omitted(self):
        for ref in [*batch.codec_review.SPLIT,'other-0']:
            for change in ('promote','omit','source'):
                data,rows,policies,previous=population();row=next(r for r in rows if r['source_reference']==ref)
                if change=='promote':row['status']='source_bound_oem_policy_ready'
                elif change=='omit':rows.remove(row)
                else:row['source_topics']=[{'id':'changed'}]
                with self.assertRaises(ValueError):batch.eligible_jobs(data,rows,policies,previous)

    def test_three_samples_bind_exact_pipeline_policies_and_two_new_jobs(self):
        data,rows,policies,previous=population();jobs=batch.eligible_jobs(data,rows,policies,previous)
        good=sample(jobs,policies)
        self.assertEqual(len(batch.sample_job_ids(good,jobs,'pipeline',policies)),3)
        for change in ('pipeline','checkpoint','review','policy','scope','duplicate','failed','formatting','missing'):
            bad=deepcopy(good)
            if change=='pipeline':bad['pipeline_identity_sha256']='other'
            elif change=='checkpoint':bad['checkpoint']='19b'
            elif change=='review':bad['review_record_sha256']='other'
            elif change=='policy':bad['run_policies_sha256']='other'
            elif change=='scope':bad['sample']={'8902178':'not a sample'}
            elif change=='duplicate':bad['jobs'][-1]=deepcopy(bad['jobs'][0])
            elif change=='failed':bad['jobs'][0]['result']['status']='failed'
            elif change=='formatting':bad['verification']['source_boundaries_and_formatting_preserved']=False
            else:bad['jobs'].pop()
            with self.assertRaises(ValueError):batch.sample_job_ids(bad,jobs,'pipeline',policies)
        with self.assertRaises(ValueError):batch.sample_job_ids(good,jobs[:-1],'pipeline',policies)

    def test_carried_samples_require_exact_checkpoint_and_runtime_inventory(self):
        data,rows,policies,previous=population();jobs=batch.eligible_jobs(data,rows,policies,previous)
        runner=SimpleNamespace(identity={'synthetic':True},oem_policies=policies)
        with tempfile.TemporaryDirectory(dir=ROOT/'build') as directory:
            root=Path(directory);s=sample(jobs,policies,key(runner.identity));s['output_root']=root.relative_to(ROOT).as_posix()
            s['runtime_files']={}
            for r in s['jobs']:
                ref=r['result']['package'];content=root/ref/'content';content.mkdir(parents=True)
                (content/'file.json').write_bytes(b'{}');s['runtime_files'][ref+'/file.json']=digest(b'{}')
            def record(pointer,job,pipeline):return next(r for r in s['jobs'] if r['job_id']==job['id'])
            with patch.object(batch,'read_json',return_value=s),patch.object(batch,'load_outcome',side_effect=record):
                self.assertEqual(len(batch.verified_samples(runner,jobs)),3)
                last=content/'file.json';last.write_bytes(b'changed')
                with self.assertRaises(ValueError):batch.verified_samples(runner,jobs)
                last.write_bytes(b'{}');extra=content/'extra.json';extra.write_bytes(b'{}')
                with self.assertRaises(ValueError):batch.verified_samples(runner,jobs)
                extra.unlink();s['checkpoint_outputs'].append(deepcopy(s['checkpoint_outputs'][0]))
                with self.assertRaises(ValueError):batch.verified_samples(runner,jobs)


@unittest.skipUnless(coverage.RECORD.exists(),'19b coverage unavailable')
class OemPassArtifacts(unittest.TestCase):
    def setUp(self):
        self.summary=read_json(coverage.RECORD)
        if not (ROOT/self.summary['coverage_root']).exists():self.skipTest('Private 19b coverage unavailable')

    def test_all_72_handoffs_preserve_old_payloads_and_add_exactly_five_articles(self):
        summary=self.summary;previous=read_json(batch.PREVIOUS);prior={r['issue_id']:r for r in previous['issues']}
        for name in ('previous_record','previous_execution_manifest','sample_record','execution_manifest'):checked_file(ROOT,summary[name])
        for item in summary['outputs']:checked_file(ROOT/summary['coverage_root'],item)
        self.assertEqual((summary['counts']['current_prepared'],summary['counts']['new_attempts'],summary['counts']['carried_sample']),(995,2,3))
        manifest=read_json(ROOT/summary['execution_manifest']['path']);self.assertEqual(manifest['origins'],{'19a':3,'19b':2})
        for item in manifest['outputs']:checked_file(ROOT/summary['run_root'],item)
        retries=batch.table(summary,'retry_history');seen=set();added=set()
        for issue in summary['issues']:
            stage=ROOT/summary['output_root']/issue['package'];verify(stage,issue['fingerprint']);package=stage/'content'
            old=prior[issue['issue_id']];old_root=ROOT/previous['output_root']/old['package']/'content'
            old_manifest=read_json(old_root/'manifest.json');current_manifest=read_json(package/'manifest.json')
            new_ids=set(issue['article_ids'])-set(old['article_ids']);added.update(new_ids)
            self.assertFalse(seen & set(issue['article_ids']));seen.update(issue['article_ids'])
            if new_ids:
                bundle,_,counts=load_package(package);self.assertEqual(counts,issue['counts'])
                self.assertEqual([a['id'] for a in bundle['articles']],issue['article_ids'])
            else:
                self.assertEqual(current_manifest,old_manifest);self.assertEqual(issue['counts'],old['counts'])
                self.assertEqual(issue['article_ids'],old['article_ids'])
            for item in preserved(old_root,old_manifest):self.assertEqual(checked_file(package,item),checked_file(old_root,item))
            for row in retries:
                if row['article_id'] not in new_ids:continue
                p=row['checkpoint'];record=read_json(ROOT/p['checkpoint_root']/p['record']['path'])
                standalone=ROOT/p['batch_root']/record['result']['package']/'content'
                for item in preserved(standalone,read_json(standalone/'manifest.json')):
                    self.assertEqual(checked_file(package,item),checked_file(standalone,item))
        self.assertEqual(len(summary['issues']),72);self.assertEqual(len(seen),995)
        self.assertEqual(added,{'cd1:article:'+ref for ref in batch.codec_review.READY})

    def test_all_histories_and_deferred_source_decisions_survive(self):
        summary=self.summary;previous=read_json(batch.PREVIOUS)
        for name,old in [('symbol_retry_history','retry_history'),('declaration_font_retry_history','declaration_font_retry_history'),
                         ('ordinary_font_retry_history','ordinary_font_retry_history'),('font_retry_history','font_retry_history'),
                         ('association_retry_history','association_retry_history')]:
            self.assertEqual(batch.table(summary,name),batch.table(previous,old))
        retries=batch.table(summary,'retry_history');self.assertEqual(len(retries),5)
        self.assertEqual(batch.histogram(r['checkpoint']['origin'] for r in retries),{'19a':3,'19b':2})
        before=batch.table(previous,'source_checks');after=batch.table(summary,'source_checks')
        self.assertEqual(after[:len(before)],before);self.assertEqual(len(after),995)
        old={e['job_id']:e for e in batch.table(previous,'exceptions')};exceptions=batch.table(summary,'exceptions')
        self.assertEqual(len(exceptions),93);decisions=[]
        for row in exceptions:
            for name in ('retry','font_review_status','font_declaration_review','symbol_review'):
                self.assertEqual(row.get(name),old[row['job_id']].get(name))
            if 'codec_review' in row:
                decision=row['codec_review'];decisions.append(decision)
                self.assertFalse(decision['approved_policy']);checked_file(ROOT,decision['record'])
        self.assertEqual(batch.histogram(r['status'] for r in decisions),
                         {'deferred_cross_font_character_representation':2,'deferred_mixed_or_ambiguous_source':30})
        self.assertEqual(summary['counts']['current_exception_categories']['font_or_decoding_policy'],35)

    def test_all_five_recoveries_inverse_bytes_and_oem_markdown_literals(self):
        summary=self.summary;runner=batch.runner();checks={r['article_id']:r['topics'] for r in batch.table(summary,'source_checks')}
        for row in batch.table(summary,'retry_history'):
            p=row['checkpoint'];record=read_json(ROOT/p['checkpoint_root']/p['record']['path']);result=record['result']
            job=runner.oem_jobs[record['source_reference']];policy=runner.oem_policies[record['source_reference']]
            decoded=read_json(ROOT/p['batch_root']/result['stages']['recovery']['path']/'recovery.json')
            before=read_json(runner.prior_review_root/f'articles/{record["source_reference"]}/recovery.json')
            self.assertEqual(decoded,{**before,'topics':[oem_runs.expected_topic(t,policy) for t in before['topics']]})
            self.assertEqual([oem_runs.check_topic(runner.rtf,t,s['rtf'],policy) for t,s in zip(decoded['topics'],job['source_topics'])],checks[row['article_id']])
            content=ROOT/p['batch_root']/result['package']/'content';manifest=read_json(content/'manifest.json')
            preview='\n'.join(checked_file(content,item).decode() for item in manifest['previews'])
            for t in decoded['topics']:
                for paragraph in t['paragraphs']:
                    for run in paragraph['runs']:
                        if run.get('encoding')=='cp437':self.assertIn(run['text'],preview)
