"""Exact source scope, reversible arrow glyphs, literal spaces and package fidelity."""
from copy import deepcopy
from pathlib import Path
import unittest

from tools.batch import symbol_arrows as arrows, symbol_arrow_pipeline as pipeline, retry_symbol_arrows as sample
from tools import recover_cd1_text as recovery, inventory_cd1_rtf as inventory
from tools.run_cd1_batch import ROOT, read_json
from tools.decode_cd1_paragraph import digest
from maso_archive.reading_room_package import checked_file, load_package


def fixture():
    raw=b"\\f2  \\'ac\\'ad\\'ae  \\par "
    report=inventory.inspect_topic(raw,0,4); report.update(ordinal=1,role='reference_target_body')
    old=recovery.recover_topic(raw,report)
    run=old['paragraphs'][0]['runs'][0]
    source={'id':'topic','native':{'ordinal':1},'rtf':{'byte_offset':0,'byte_length':len(raw),'sha256':digest(raw)}}
    decision={'reference':arrows.REFERENCE,'topic_id':'topic','paragraph':1,'run':1,'source_run':deepcopy(run)}
    policy={'reference':arrows.REFERENCE,'encoding':arrows.ENCODING,'source_topics':[source],'runs':[decision],
            'mapping':{f'{b:02x}':c for b,c in arrows.GLYPHS.items()},'space_policy':'literal_RTF_20_to_U0020_without_reflow',
            'mapping_sha256':arrows.symbol_review.MAPPING_SHA256}
    return raw,report,old,policy


class ArrowPolicyTests(unittest.TestCase):
    def test_round_trip_is_exact_and_no_other_bytes_or_glyphs_are_accepted(self):
        self.assertEqual(arrows.decode(b' \xac\xad\xae  '),' ←↑→  ')
        self.assertEqual(arrows.encode(' ←↑→  '),b' \xac\xad\xae  ')
        for raw in (b'',b'PRINT',b'\xaf',b'\t',b'\x00',b'\x7f'):
            with self.assertRaises(ValueError): arrows.decode(raw)
        for text in ('','\u00a0','↓','PRINT','\t','\ufffd'):
            with self.assertRaises(ValueError): arrows.encode(text)

    def test_adapter_preserves_source_fields_and_literal_spaces_without_mutation(self):
        raw,report,old,policy=fixture(); before=deepcopy(old)
        actual=arrows.recover_topic(raw,report,None,{4:'cp949'},policy)
        self.assertEqual(actual['paragraphs'][0]['text'],' ←↑→  ')
        self.assertEqual(old,before)
        for field in ('source_span','accounting','metadata','transformations','final_state','trailing_layout_span'):
            self.assertEqual(actual[field],old[field])
        a=actual['paragraphs'][0]['runs'][0]; b=old['paragraphs'][0]['runs'][0]
        for field in ('source_spans','encoded_bytes','encoded_sha256','format','original_bytes_hex'):
            self.assertEqual(a[field],b[field])
        self.assertEqual(a['encoding'],arrows.ENCODING)
        checked=arrows.check_topic(raw,actual,policy['source_topics'][0]['rtf'],policy)
        self.assertEqual(checked['symbol_arrow_runs'],1)
        self.assertEqual(checked['symbol_glyph_counts'],{' ':3,'←':1,'↑':1,'→':1})

    def test_independent_checker_rejects_changed_glyph_spacing_format_or_byte_evidence(self):
        raw,report,old,policy=fixture(); actual=arrows.expected_topic(old,policy)
        for change in ('glyph','nbsp','space','font','hash','span','ledger','encoding','missing'):
            bad=deepcopy(actual); run=bad['paragraphs'][0]['runs'][0]
            if change=='glyph':run['text']=run['text'].replace('←','→')
            elif change=='nbsp':run['text']=run['text'].replace(' ','\u00a0',1)
            elif change=='space':run['text']=run['text'][1:]
            elif change=='font':run['format']['font_id']=4
            elif change=='hash':run['encoded_sha256']='changed'
            elif change=='span':run['source_spans'][0]['byte_offset']+=1
            elif change=='ledger':bad['accounting'][0]['byte_length']+=1
            elif change=='encoding':run['encoding']='cp949'
            else:bad['paragraphs'][0]['runs']=[]
            bad['paragraphs'][0]['text']=''.join(r['text'] for r in bad['paragraphs'][0]['runs'])
            with self.assertRaises(ValueError):arrows.check_topic(raw,bad,policy['source_topics'][0]['rtf'],policy)

    def test_wrong_article_topic_policy_source_and_unrelated_issues_fail_closed(self):
        raw,report,old,policy=fixture()
        for change in ('reference','mapping','space_policy','topic','run','issue'):
            p=deepcopy(policy); t=deepcopy(old)
            if change=='reference':p['reference']='9205400a'
            elif change=='mapping':p['mapping']['ae']='↓'
            elif change=='space_policy':p['space_policy']='nbsp'
            elif change=='topic':t['ordinal']=2
            elif change=='run':t['paragraphs'][0]['runs'][0]['original_bytes_hex']='af'
            else:t['issues'].append({'reason':'Other source error'})
            with self.assertRaises(ValueError):arrows.expected_topic(t,p)
        with self.assertRaises(ValueError):arrows.recover_topic(raw,report,None,{2:'cp949',4:'cp949'},policy)
        with self.assertRaises(ValueError):arrows.recover_topic(raw.replace(b"'ac",b"'ae"),report,None,{4:'cp949'},policy)

    def test_prior_outputs_and_non_arrow_jobs_are_protected(self):
        for name in ('cd1-batch','cd1-symbol-review','cd1-symbol-sample','cd1-font-declaration-pass'):
            for p in (ROOT/'build'/name,ROOT/'build'/name/'nested'):
                with self.assertRaises(ValueError):pipeline.safe_output(p)
        for p in (ROOT/'build',Path('/tmp/arrows')):
            with self.assertRaises(ValueError):pipeline.safe_output(p)
        runner=object.__new__(pipeline.ArrowRunner);runner.arrow_job={'source_reference':arrows.REFERENCE}
        with self.assertRaises(ValueError):runner.process({'source_reference':'9210202'})


class ArrowArtifacts(unittest.TestCase):
    def test_exact_eight_reviewed_runs_and_both_full_topics_are_preserved(self):
        if not sample.RECORD.exists():self.skipTest('18b sample unavailable')
        record=read_json(sample.RECORD);root=ROOT/record['output_root']
        if not root.exists():self.skipTest('Private 18b output unavailable')
        review=read_json(arrows.symbol_review.RECORD); reviewed=ROOT/review['output_root']
        job=read_json(root/record['jobs'][0]['result']['stages']['association']['path']/'association.json')
        evidence=[e for e in read_json(reviewed/'runs.json') if e['reference']==arrows.REFERENCE]
        policy=arrows.make_policy(job,evidence)
        self.assertEqual(len(policy['runs']),8)
        self.assertEqual(len(job['source_topics']),2)
        before=read_json(reviewed/f'articles/{arrows.REFERENCE}/recovery.json')
        actual=read_json(root/record['jobs'][0]['result']['stages']['recovery']['path']/'recovery.json')
        self.assertEqual(actual,{**before,'topics':[arrows.expected_topic(t,policy) for t in before['topics']]})
        from tools.cd1_batch_cache import key
        self.assertEqual(record['glyph_policy_sha256'],key(policy))
        for change in ('reference','missing','decision','bytes'):
            j=deepcopy(job);e=deepcopy(evidence)
            if change=='reference':j['source_reference']='9210202'
            elif change=='missing':e.pop()
            elif change=='decision':e[0]['policy_approved']=True
            else:e[0]['source_run']['original_bytes_hex']='af'
            with self.assertRaises(ValueError):arrows.make_policy(j,e)

    def test_package_previews_and_all_runtime_hashes_validate(self):
        if not sample.RECORD.exists():self.skipTest('18b sample unavailable')
        record=read_json(sample.RECORD);root=ROOT/record['output_root']
        if not root.exists():self.skipTest('Private 18b output unavailable')
        self.assertEqual(set(record['sample']),{arrows.REFERENCE});self.assertEqual(len(record['jobs']),1)
        for item in record['checkpoint_outputs']:checked_file(ROOT/record['checkpoints_root'],item)
        row=record['jobs'][0];self.assertEqual(row['result']['status'],'prepared')
        package=root/row['result']['package']/'content';bundle,manifest,_=load_package(package)
        self.assertEqual([a['source']['reference'] for a in bundle['articles']],[arrows.REFERENCE])
        actual={arrows.REFERENCE+'/'+p.relative_to(package).as_posix():digest(p.read_bytes()) for p in package.rglob('*') if p.is_file()}
        self.assertEqual(actual,record['runtime_files'])
        previews=''.join(checked_file(package,p).decode() for p in manifest['previews'])
        # Non-code Markdown preserves edge spaces as numeric entities.
        # Check the encoded sequence without dumping private article text on failure.
        self.assertTrue('&#32;'*94+'←←&#32;' in previews,
                        'Arrow annotation lost literal spaces in Markdown')
        for result in record['issues'].values():
            bundle,_,counts=load_package(root/result['package']/'content')
            self.assertEqual(counts,result['counts']);self.assertEqual(len(bundle['articles']),1)
