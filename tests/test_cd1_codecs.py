"""Exact OEM literal recovery, retained alternatives and cross-font byte boundaries."""
from copy import deepcopy
from pathlib import Path
import unittest

from tools.batch import codec_review as review, oem_runs, oem_pipeline, retry_oem_sample as sample
from tools import inventory_cd1_rtf as inventory, recover_cd1_text as recovery
from tools.run_cd1_batch import ROOT, read_json
from tools.decode_cd1_paragraph import digest
from tools.cd1_batch_cache import key
from maso_archive.reading_room_package import checked_file, load_package


def fixture():
    raw=rb'''\f15     printf("%#10ld <\'c4\'c4\'c4 %-60s\\n",sum_fsize,thisdir);\par '''
    report=inventory.inspect_topic(raw,0,4);report.update(ordinal=1,role='reference_target_body')
    old=recovery.recover_topic(raw,report,None,{4:'cp949',15:'cp949'})
    source={'id':'topic','native':{'ordinal':1},'rtf':{'byte_offset':0,'byte_length':len(raw),'sha256':digest(raw)}}
    job={'source_reference':'9206396','source_topics':[source]}
    row={'reference':'9206396','topic_id':'topic','paragraph':1,'run':1,'source_run':deepcopy(old['paragraphs'][0]['runs'][0])}
    return raw,report,old,job,row


class CodecPolicyTests(unittest.TestCase):
    def test_pinned_mapping_matches_python_and_exact_box_subset(self):
        table=review.mapping_table();self.assertEqual(len(table),256)
        self.assertEqual({b:table[b] for b in review.BOX},review.BOX)
        self.assertEqual(table[0xc4],'─');self.assertNotEqual(table[0xc4],bytes([0xc4]).decode('cp1252'))
        self.assertEqual(digest(review.LICENSE.read_bytes()),review.LICENSE_SHA256)

    def test_candidate_round_trip_never_approves_ambiguous_source(self):
        for codec in ('cp437','cp1252'):
            candidate=review.attempt(b'\xc4',codec)
            self.assertTrue(candidate['round_trip']);self.assertFalse(candidate['approved'])
        error=review.attempt(b'x\xc4','cp949')
        self.assertEqual((error['status'],error['start'],error['end'],error['bytes_hex']),('decode_error',1,2,'c4'))
        self.assertFalse(error['approved'])

    def test_cross_font_character_is_recorded_without_merging_or_changing_runs(self):
        raw=rb"\f4 \'b8\f15 \'a6\par "
        report=inventory.inspect_topic(raw,0,4);report.update(ordinal=1,role='reference_target_body')
        topic=recovery.recover_topic(raw,report,None,{4:'cp949',15:'cp949'});before=deepcopy(topic)
        candidates=review.boundary_candidates(topic['paragraphs'][0])
        self.assertEqual(len(candidates),1);self.assertEqual(candidates[0]['candidate_text'],'를')
        self.assertEqual(candidates[0]['runs'],[1,2]);self.assertFalse(candidates[0]['approved'])
        self.assertEqual(topic,before)
        topic['paragraphs'][0]['runs'][1]['original_bytes_hex']='ff'
        self.assertEqual(review.boundary_candidates(topic['paragraphs'][0]),[])

    def test_only_reviewed_literal_changes_and_source_fields_remain_exact(self):
        raw,report,old,job,row=fixture();before=deepcopy(old);policy=review.make_policy(job,[row])
        actual=oem_runs.recover_topic(raw,report,None,{4:'cp949',15:'cp949'},policy)
        self.assertEqual(old,before)
        run=actual['paragraphs'][0]['runs'][0];self.assertIn('<─── ',run['text']);self.assertEqual(run['encoding'],'cp437')
        for field in ('source_spans','encoded_bytes','encoded_sha256','format','original_bytes_hex'):
            self.assertEqual(run[field],row['source_run'][field])
        for field in ('source_span','accounting','metadata','transformations','final_state','trailing_layout_span'):
            self.assertEqual(actual[field],old[field])
        checked=oem_runs.check_topic(raw,actual,job['source_topics'][0]['rtf'],policy)
        self.assertEqual(checked['oem_runs'],1);self.assertEqual(checked['oem_glyph_counts'],{'─':3})

    def test_policy_rejects_wrong_article_font_repertoire_count_and_source(self):
        raw,report,old,job,row=fixture()
        for change in ('article','font','bytes','duplicate','literal','topic'):
            j=deepcopy(job);r=deepcopy(row)
            if change=='article':j['source_reference']='8807052'
            elif change=='font':r['source_run']['format']['font_id']=4
            elif change=='bytes':r['source_run']['original_bytes_hex']='a4'
            elif change=='literal':r['source_run']['original_bytes_hex']=b"unreviewed '\xc4\xc4\xc4'".hex()
            elif change=='topic':r['topic_id']='other'
            with self.assertRaises(ValueError):review.make_policy(j,[r,r] if change=='duplicate' else [r])
        policy=review.make_policy(job,[row])
        changed=deepcopy(old);changed['issues'].append({'reason':'unrelated'})
        with self.assertRaises(ValueError):oem_runs.expected_topic(changed,policy)
        with self.assertRaises(ValueError):oem_runs.recover_topic(raw.replace(b"'c4",b"'b3",1),report,None,{4:'cp949',15:'cp949'},policy)
        with self.assertRaises(ValueError):oem_runs.recover_topic(raw,report,None,{4:'cp949',15:'ascii'},policy)

    def test_independent_checker_rejects_glyph_space_format_hash_and_ledger_changes(self):
        raw,_,old,job,row=fixture();policy=review.make_policy(job,[row]);actual=oem_runs.expected_topic(old,policy)
        for change in ('glyph','space','font','hash','span','ledger','codec','missing'):
            bad=deepcopy(actual);run=bad['paragraphs'][0]['runs'][0]
            if change=='glyph':run['text']=run['text'].replace('─','│',1)
            elif change=='space':run['text']=run['text'][1:]
            elif change=='font':run['format']['font_id']=4
            elif change=='hash':run['encoded_sha256']='changed'
            elif change=='span':run['source_spans'][0]['byte_offset']+=1
            elif change=='ledger':bad['accounting'][0]['byte_length']+=1
            elif change=='codec':run['encoding']='cp1252'
            else:bad['paragraphs'][0]['runs']=[]
            bad['paragraphs'][0]['text']=''.join(r['text'] for r in bad['paragraphs'][0]['runs'])
            with self.assertRaises((ValueError,UnicodeError)):oem_runs.check_topic(raw,bad,job['source_topics'][0]['rtf'],policy)

    def test_historical_roots_and_unreviewed_jobs_are_protected(self):
        for name in ('cd1-batch','cd1-font-review','cd1-symbol-pass','cd1-symbol-arrow-sample','cd1-codec-review'):
            for p in (ROOT/'build'/name,ROOT/'build'/name/'nested'):
                with self.assertRaises(ValueError):oem_pipeline.safe_output(p)
        with self.assertRaises(ValueError):oem_pipeline.safe_output(Path('/tmp/oem'))
        runner=object.__new__(oem_pipeline.OemRunner);runner.oem_jobs={}
        with self.assertRaises(ValueError):runner.process({'source_reference':'9103202'})


class CodecArtifacts(unittest.TestCase):
    def test_complete_review_preserves_all_sources_and_never_approves_deferred_candidates(self):
        if not review.RECORD.exists():self.skipTest('19a review unavailable')
        record=read_json(review.RECORD);root=ROOT/record['output_root']
        if not root.exists():self.skipTest('Private codec review unavailable')
        for item in record['outputs']:checked_file(root,item)
        old=read_json(review.font_review.RECORD);old_root=ROOT/old['output_root']
        rows=read_json(root/'jobs.json');runs=read_json(root/'runs.json');policies=read_json(root/'policy.json')['articles']
        self.assertEqual((len(rows),sum(len(r['source_topics']) for r in rows),len(runs)),(37,70,185))
        self.assertEqual(set(policies),review.READY)
        for row in rows:
            ref=row['source_reference'];name=f'articles/{ref}/recovery.json'
            self.assertEqual((root/name).read_bytes(),(old_root/name).read_bytes())
            relevant=[r for r in runs if r['reference']==ref]
            self.assertEqual(sum(r['approved'] for r in relevant),len(relevant) if ref in review.READY else 0)
            for r in relevant:self.assertTrue(all(not a['approved'] for a in r['attempts'].values()))
        self.assertEqual(sum(r['approved'] for r in runs),30)
        boundaries=read_json(root/'boundaries.json');self.assertEqual({r['reference'] for r in boundaries},review.SPLIT)
        self.assertTrue(all(not r['approved'] for r in boundaries))

    def test_all_sample_bytes_topics_packages_and_markdown_literals_validate(self):
        if not sample.RECORD.exists():self.skipTest('19a samples unavailable')
        record=read_json(sample.RECORD);root=ROOT/record['output_root']
        if not root.exists():self.skipTest('Private OEM samples unavailable')
        review_root=ROOT/read_json(review.RECORD)['output_root'];policies=read_json(review_root/'policy.json')['articles']
        self.assertEqual(set(record['sample']),set(review.SAMPLE));self.assertEqual(record['run_policies_sha256'],key(policies))
        runtime={};rtf=(ROOT/'private/cd1-probe/raw/MASOCD.rtf').read_bytes()
        for row in record['jobs']:
            result=row['result'];package=root/result['package']/'content';bundle,manifest,_=load_package(package)
            ref=bundle['articles'][0]['source']['reference'];self.assertIn(ref,review.SAMPLE)
            actual=read_json(root/result['stages']['recovery']['path']/'recovery.json')
            old=read_json(review_root/f'articles/{ref}/recovery.json')
            expected={**old,'topics':[oem_runs.expected_topic(t,policies[ref]) for t in old['topics']]}
            self.assertTrue(actual==expected,'Recovery changed outside approved OEM spans')
            checks=[oem_runs.check_topic(rtf,t,s['rtf'],policies[ref]) for t,s in zip(actual['topics'],policies[ref]['source_topics'])]
            self.assertEqual(checks,next(r['source_checks'] for r in record['source_checks'] if r['article_id']==row['result'].get('article_id','cd1:article:'+ref)))
            previews=''.join(checked_file(package,p).decode() for p in manifest['previews'])
            for t in actual['topics']:
                for p in t['paragraphs']:
                    for run in p['runs']:
                        if run.get('encoding')=='cp437':self.assertTrue(run['text'] in previews,'OEM literal or spaces changed in Markdown')
            runtime.update({ref+'/'+p.relative_to(package).as_posix():digest(p.read_bytes()) for p in package.rglob('*') if p.is_file()})
        self.assertEqual(runtime,record['runtime_files'])
        for result in record['issues'].values():
            _,_,counts=load_package(root/result['package']/'content');self.assertEqual(counts,result['counts'])
