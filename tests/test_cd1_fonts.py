"""ASCII policy boundaries, source-preserving replacement and private artifacts."""
from copy import deepcopy
from pathlib import Path
import unittest

from tools.batch import font_review, retry_fonts
from tools.run_cd1_batch import ROOT, read_json
from maso_archive.reading_room_package import checked_file, load_package


def unsupported(font, raw, reason=None):
    return {'kind':'unsupported', 'format':{'font_id':font,'b':True},
            'text':'[unsupported]', 'reason':reason or f'Unsupported font {font}',
            'encoding':'cp949','original_bytes_hex':raw.hex(), 'source_spans':[{'byte_offset':9,'byte_length':len(raw)}]}


class FontPolicyTests(unittest.TestCase):
    def test_ordinary_ascii_layout_spaces_and_tabs_are_allowed(self):
        for font in font_review.FONTS:
            for raw in (b' ',b'\t',b'0123 / text',b'  ..   ..'):
                self.assertEqual(font_review.classify(unsupported(font,raw)),'reviewed_ascii_font')

    def test_non_ascii_controls_and_existing_codec_errors_stay_deferred(self):
        for raw in (b'\xb0\xa1',b'\x80',b'\x00',b'\n',b'\x7f'):
            self.assertEqual(font_review.classify(unsupported(13,raw)),'non_ascii_in_additional_font')
        self.assertEqual(font_review.classify(unsupported(4,b'\xc4', 'invalid cp949')),'existing_codec_failure')
        self.assertEqual(font_review.classify(unsupported(13,b'A', 'Byte round-trip mismatch')),'existing_codec_failure')

    def test_ascii_codes_do_not_authorize_symbol_or_unreviewed_fonts(self):
        for font in (2,14,30,64,72,99,1000):
            self.assertEqual(font_review.classify(unsupported(font,b'PRINT')),'unreviewed_font_or_symbol')

    def test_replacement_preserves_all_other_text_formatting_and_source_fields(self):
        source={'paragraphs':[{'runs':[{'kind':'text','text':'existing','format':{'font_id':4}},unsupported(13,b' \tA')],
                               'text':'existing[unsupported]','format':{'tab_stops':[120]},'terminated_by_par':True}],
                'issues':[{'reason':'Unsupported font 13'}],'accounting':[{'byte_offset':5}], 'final_state':{'font':13}}
        before=deepcopy(source)
        actual=retry_fonts.expected_ascii_topic(source)
        self.assertEqual(source,before)
        self.assertEqual(actual['paragraphs'][0]['text'],'existing \tA')
        self.assertEqual(actual['paragraphs'][0]['runs'][0],source['paragraphs'][0]['runs'][0])
        self.assertEqual(actual['paragraphs'][0]['runs'][1]['format'],source['paragraphs'][0]['runs'][1]['format'])
        self.assertEqual(actual['accounting'],source['accounting'])
        self.assertEqual(actual['final_state'],source['final_state'])
        self.assertEqual(actual['issues'],[])
        source['paragraphs'][0]['runs'][1]=unsupported(2,b'A')
        with self.assertRaises(ValueError):retry_fonts.expected_ascii_topic(source)

    def test_private_output_cannot_overlap_prior_handoffs_or_audit(self):
        for name in ('cd1-batch','cd1-associations','cd1-association-sample','cd1-association-pass','cd1-font-review'):
            for path in (ROOT/'build'/name,ROOT/'build'/name/'nested'):
                with self.assertRaises(ValueError):retry_fonts.safe_output(path)
        for path in (ROOT/'build',ROOT,Path('/tmp/font-output')):
            with self.assertRaises(ValueError):retry_fonts.safe_output(path)
        self.assertEqual(retry_fonts.safe_output(ROOT/'build/cd1-font-sample'),ROOT/'build/cd1-font-sample')


class FontArtifactTests(unittest.TestCase):
    def test_all_failure_sources_and_source_bound_policy_are_accounted_for(self):
        if not font_review.RECORD.exists():self.skipTest('Font review unavailable')
        record=read_json(font_review.RECORD);root=ROOT/record['output_root']
        if not root.exists():self.skipTest('Private font audit unavailable')
        checked_file(ROOT,record['current_record'])
        for item in record['outputs']:checked_file(root,item)
        rows=read_json(root/'jobs.json');policy=read_json(root/'policy.json')['article_fonts']
        self.assertEqual(len(rows),86)
        self.assertEqual(sum(row['topics_checked'] for row in rows),record['counts']['full_source_topics'])
        self.assertGreater(record['counts']['full_source_topics'],record['counts']['historical_topics'])
        self.assertEqual(set(policy),{r['source_reference'] for r in rows if r['status']=='ascii_policy_ready'})
        self.assertTrue(set(font_review.SAMPLE)<=set(policy))
        for row in rows:
            checked_file(ROOT,row['source_evidence'])
            if row['source_reference'] in policy:
                extra=policy[row['source_reference']]
                self.assertEqual(extra['source_topics'],row['source_topics'])
                self.assertTrue(all(int(k) in font_review.FONTS and v=='ascii' for k,v in extra['font_codecs'].items()))

    def test_all_six_sample_packages_and_checkpoints_validate(self):
        if not retry_fonts.RECORD.exists():self.skipTest('Font sample unavailable')
        record=read_json(retry_fonts.RECORD);root=ROOT/record['output_root']
        if not root.exists():self.skipTest('Private font sample unavailable')
        self.assertEqual(set(record['sample']),set(font_review.SAMPLE))
        self.assertEqual(len(record['jobs']),6)
        for item in record['checkpoint_outputs']:checked_file(ROOT/record['checkpoints_root'],item)
        for row in record['jobs']:
            self.assertEqual(row['result']['status'],'prepared')
            bundle,_,_=load_package(root/row['result']['package']/'content')
            self.assertEqual(len(bundle['articles']),1)
        for issue,result in record['issues'].items():
            bundle,_,counts=load_package(root/result['package']/'content')
            self.assertEqual(counts,result['counts'])
            self.assertEqual({a['issue_id'] for a in bundle['articles']},{issue})
