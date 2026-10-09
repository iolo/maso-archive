"""Human-review boundaries, evidence reuse, and source-only local preparation."""
import json
from pathlib import Path
import tempfile
import unittest
import jsonschema
from unittest.mock import patch

from PIL import Image
from tools.ocr_workflow_report import summarize

from tools.ocr_qwen.workflow import (
    ARMS, checked_stage, comparison, geometry_only, local_call, review_ledger,
    review_summary, save_once, stage, token_totals, write_packet,
    CORRECTION_SCHEMA,
    run_lock,
)


class OCRWorkflowTests(unittest.TestCase):
    def test_live_worker_lock_blocks_resume_and_releases_on_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with patch('tools.ocr_qwen.workflow.ROOT',root):
                with run_lock(root/'private/run'):
                    with self.assertRaisesRegex(ValueError,'Another worker'):
                        with run_lock(root/'private/run'):
                            self.fail('concurrent writer')
                with self.assertRaisesRegex(RuntimeError,'interrupted'):
                    with run_lock(root/'private/run'):
                        raise RuntimeError('interrupted')
                with run_lock(root/'private/run'):
                    pass

    def test_reference_answers_are_removed_before_inference(self):
        sample={'reference':[dict(id='r1',kind='prose',bbox=[0,0,1,1],
                                  text='GOLD ANSWER',uncertainties=['SECRET'])]}
        regions=geometry_only(sample)
        self.assertEqual(regions,[dict(id='r1',kind='prose',bbox=[0,0,1,1])])
        sample['reference']*=2
        with self.assertRaisesRegex(ValueError,'duplicate'):
            geometry_only(sample)

    def test_local_ocr_is_independent_and_correction_receives_only_drafts(self):
        with tempfile.TemporaryDirectory() as tmp:
            crop=Path(tmp)/'crop.png';Image.new('RGB',(10,10)).save(crop)
            with patch('tools.ocr_qwen.workflow.infer',return_value=({'text':'OCR'},{})) as call:
                local_call(object(),crop,Path(tmp),'prose',100,10)
                self.assertNotIn('DRAFT-A',call.call_args.args[2])
                local_call(object(),crop,Path(tmp),'prose',100,10,{'A':'DRAFT-A','B':'DRAFT-B'})
                prompt=call.call_args.args[2]
                self.assertIn('DRAFT-A',prompt)
                self.assertIn('DRAFT-B',prompt)
                self.assertIn('never claim human verification',prompt.lower())

    def test_completed_stage_reused_and_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)/'stage'
            with patch('tools.ocr_qwen.workflow.Monitor') as monitor:
                monitor.return_value.__enter__.return_value.metrics={'wall_seconds':1}
                result,hit=stage(directory,lambda path:{'text':'raw'})
            self.assertFalse(hit)
            with patch('tools.ocr_qwen.workflow.Monitor',side_effect=AssertionError('must reuse')):
                again,hit=stage(directory,lambda path:self.fail('inference repeated'))
            self.assertTrue(hit)
            self.assertEqual(result,again)
            (directory/'result.json').write_text('{"text":"changed"}')
            with self.assertRaisesRegex(ValueError,'hash differs'):
                checked_stage(directory)

    def test_incomplete_stage_never_silently_retried(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)/'stage';directory.mkdir()
            (directory/'raw.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'Incomplete'):
                stage(directory,lambda path:self.fail('must not retry'))

    def test_review_agreement_is_not_acceptance(self):
        sample=dict(id='sample',reference=[dict(id='r1',kind='prose')])
        ledger=review_ledger([sample])
        self.assertEqual(len(ledger['pages']),3)
        self.assertTrue(all(p['accepted'] is False for p in ledger['pages']))
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'review.json';path.write_text(json.dumps(ledger))
            summary=review_summary(path)
            self.assertEqual(summary['accepted_pages'],0)
            self.assertIsNone(summary['savings_claim'])
            ledger['pages'][0]['accepted']=True
            path.write_text(json.dumps(ledger))
            with self.assertRaisesRegex(ValueError,'human'):
                review_summary(path)

    def test_unknown_usage_is_not_zero_and_invalid_usage_rejected(self):
        sample=dict(id='sample',reference=[dict(id='r1',kind='prose')])
        ledger=review_ledger([sample])
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'review.json';path.write_text(json.dumps(ledger))
            self.assertIsNone(review_summary(path)['pages'][0]['capable_model_usage'])
            ledger['pages'][0]['capable_model_usage']={'input_tokens':1}
            path.write_text(json.dumps(ledger))
            with self.assertRaisesRegex(ValueError,'Usage'):
                review_summary(path)

    def test_differences_keep_unicode_offsets_and_whitespace_distinction(self):
        diff=comparison('가 나','가나')
        self.assertFalse(diff['exact_agreement'])
        self.assertTrue(diff['compact_agreement'])
        self.assertEqual(diff['spans'][0]['before_range'],[1,2])
        self.assertEqual(diff['spans'][0]['before'],' ')

    def test_preserve_existing_crop_and_measured_local_tokens(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'evidence';save_once(path,b'original');save_once(path,b'original')
            with self.assertRaisesRegex(ValueError,'differs'):
                save_once(path,b'changed')
        totals=token_totals([{'inference':{'usage':{'prompt_tokens':20,'completion_tokens':5,'total_tokens':25}}}])
        self.assertEqual(totals['total_tokens'],25)

    def test_packet_includes_agreement_regions_and_excludes_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            geometry=[dict(id='r1',kind='prose',bbox=[0,0,1,1])]
            records={('sample','r1',arm):dict(text='same',uncertainties=[]) for arm in ARMS}
            diffs=write_packet(root,{'id':'sample','reference':'DO NOT DISPLAY'},geometry,records)
            packet=(root/'sample-review.md').read_text()
            self.assertIn('r1 (prose)',packet)
            self.assertNotIn('DO NOT DISPLAY',packet)
            self.assertTrue(diffs[0]['requires_human_review'])
            self.assertTrue(diffs[0]['ab']['exact_agreement'])

    def test_explanations_are_bounded_by_correction_schema(self):
        for uncertainty in (['x'*161], ['x']*9):
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate({'text':'draft','uncertainties':uncertainty},CORRECTION_SCHEMA)

    def test_review_cannot_drop_pages_or_disguise_text_as_figures(self):
        sample=dict(id='sample',reference=[dict(id='r1',kind='prose')])
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'inputs-for-evaluation.json').write_text(json.dumps({'samples':[sample]}))
            ledger=review_ledger([sample]);path=root/'review-ledger.json'
            ledger['pages'].pop();path.write_text(json.dumps(ledger))
            with self.assertRaisesRegex(ValueError,'Every prepared'):
                review_summary(path)
            ledger=review_ledger([sample])
            ledger['pages'][0]['regions'][0]['disposition']='figure-reviewed'
            path.write_text(json.dumps(ledger))
            with self.assertRaisesRegex(ValueError,'Text regions'):
                review_summary(path)

    def test_human_acceptance_requires_final_text_and_preserves_unknown_usage(self):
        sample=dict(id='sample',reference=[dict(id='r1',kind='prose')])
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);ledger=review_ledger([sample]);page=ledger['pages'][0]
            page.update(reviewer='Synthetic test reviewer',reviewer_type='human',
                        page_coverage_checked=True,accepted=True,active_review_seconds=12.5)
            page['regions'][0].update(disposition='corrected',final_text='final.txt')
            path=root/'review.json';path.write_text(json.dumps(ledger))
            with self.assertRaisesRegex(ValueError,'final_text'):
                review_summary(path)
            (root/'final.txt').write_text('synthetic reviewed text')
            summary=review_summary(path)
            self.assertEqual(summary['accepted_pages'],1)
            self.assertIsNone(summary['pages'][0]['capable_model_usage'])

    def test_report_counts_c_dependencies_and_regressions_without_inventing_savings(self):
        sample=dict(id='sample',reference=[dict(id='r1',kind='prose',bbox=[0,0,1,1],text='AB')])
        tokens=dict(prompt_tokens=2,completion_tokens=1,total_tokens=3,calls=1,calls_with_usage=1)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'inputs-for-evaluation.json').write_text(json.dumps({'samples':[sample]}))
            (root/'review-ledger.json').write_text(json.dumps(review_ledger([sample])))
            rows=[dict(sample='sample',arm=arm,stage_seconds=i+1,local_tokens=tokens,
                       accuracy_proxy={},text_regions=1,ab_disagreement_regions=1,
                       ab_compact_disagreement_regions=1,correction_changed_regions=1,
                       local_uncertainties=0) for i,arm in enumerate(ARMS)]
            (root/'report.json').write_text(json.dumps({'rows':rows,'limits':[]}))
            def stage_result(path):
                return dict(text='AX' if path.name==ARMS[2] else 'AB',
                            resources=dict(peak_rss_mib_sampled=10,peak_gpu_mib_sampled=None))
            with patch('tools.ocr_workflow_report.checked_stage',side_effect=stage_result):
                result=summarize(root)
            self.assertEqual(result['rows'][1]['preparation_seconds'],2)
            self.assertEqual(result['rows'][2]['preparation_seconds'],6)
            self.assertEqual(result['rows'][2]['local_tokens']['total_tokens'],9)
            self.assertEqual(result['rows'][2]['correction_regressions_vs_B'],[
                {'region':'r1','extra_reference_edits':1}])
            self.assertIsNone(result['review_status']['savings_claim'])


if __name__=='__main__':
    unittest.main()
