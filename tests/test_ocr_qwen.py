"""Offline tests for truncation, geometry, scoring and evidence contracts."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

from PIL import Image
import jsonschema

from tools.ocr_qwen.benchmark import distance, rates, score, validate_manifest
from tools.ocr_qwen.pipeline import infer, validate_layout, TEXT_SCHEMA, ocr_image, fresh_output
from tools.pdf_restore.inventory import digest
from tools.ocr_qwen.inputs import package_image


class QwenOCRTests(unittest.TestCase):
    def test_layout_rejects_invalid_geometry_and_unknown_kind(self):
        for bbox in ([100,0,50,100], [0,50,100,50]):
            with self.assertRaises(ValueError):
                validate_layout({'regions':[{'kind':'prose','bbox':bbox}]})
        with self.assertRaises(jsonschema.ValidationError):
            validate_layout({'regions':[{'kind':'made-up','bbox':[0,0,1000,1000]}]})
        with self.assertRaises(jsonschema.ValidationError):
            validate_layout({'regions':[{'kind':'prose','bbox':[0,0,1001,1000]}]})

    def test_truncation_keeps_raw_response_and_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'request'
            response={'choices':[{'finish_reason':'length','message':{'content':'{"text":"truncated"}'}}]}
            with patch('tools.ocr_qwen.pipeline.request',return_value=response):
                with self.assertRaisesRegex(ValueError,'Incomplete'):
                    infer(SimpleNamespace(url='http://127.0.0.1:1'),Image.new('RGB',(20,20)),'read',TEXT_SCHEMA,dest)
            self.assertEqual(json.loads(dest.with_suffix('.response.json').read_text()),response)
            settings=json.loads(dest.with_suffix('.request.json').read_text())
            self.assertFalse(settings['settings']['cache_prompt'])
            self.assertEqual(settings['settings']['presence_penalty'],0)
            self.assertEqual(settings['settings']['response_format']['json_schema']['schema'],TEXT_SCHEMA)

    def test_pipeline_keeps_native_order_and_figures_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); image=root/'source.png'; output=root/'out'
            Image.new('RGB',(100,200),'white').save(image)
            layout={'regions':[{'kind':'figure','bbox':[0,0,500,300]},
                               {'kind':'prose','bbox':[500,0,1000,1000]}]}
            calls=[]
            def fake(server,img,prompt,schema,dest,*args,**kwargs):
                calls.append(img.size)
                return (layout if len(calls)==1 else {'text':'한글\nEnglish'}, {'seconds':.1})
            with patch('tools.ocr_qwen.pipeline.infer',side_effect=fake):
                result=ocr_image(image,output,object())
            self.assertEqual(len(calls),2)  # Figure kept as image, not invented transcription.
            self.assertEqual(result['regions'][1]['crop_pixels'],[48,0,100,200])
            self.assertEqual(result['regions'][1]['text'],'한글\nEnglish')
            self.assertTrue((output/'r001.png').exists())
            self.assertEqual(result['status'],'unreviewed')
            manifest=json.loads((output/'manifest.json').read_text())
            for f in manifest['files']:
                self.assertEqual(digest(output/f['path']),f['sha256'])
            with self.assertRaises(FileExistsError):
                ocr_image(image,output,object())

    def test_failed_layout_never_creates_success_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); image=root/'image.png'
            Image.new('RGB',(10,10)).save(image)
            with patch('tools.ocr_qwen.pipeline.infer',side_effect=TimeoutError('timeout')):
                with self.assertRaises(TimeoutError):
                    ocr_image(image,root/'out',object())
            self.assertTrue((root/'out/failure.json').exists())
            self.assertFalse((root/'out/result.json').exists())

    def test_edit_distance_and_unicode_normalization(self):
        self.assertEqual(distance('kitten','sitting'),3)
        self.assertEqual(distance('','abc'),3)
        self.assertEqual(rates('가 나','가\n나')['cer'],0)
        self.assertEqual(rates('가 나','가나')['cer_no_whitespace'],0)
        self.assertGreater(rates('a','aaaa')['cer'],1)

    def test_order_errors_and_omissions_are_counted(self):
        refs=[dict(kind='prose',text='AB',bbox=[0,0,.4,1]),dict(kind='prose',text='CD',bbox=[.6,0,1,1])]
        self.assertEqual(score(refs,refs)['cer'],0)
        self.assertGreater(score(refs,list(reversed(refs)))['cer'],0)
        self.assertEqual(score(refs,[])['cer'],1)

    def test_uncertain_code_lines_excluded_but_missing_known_lines_penalized(self):
        ref=[dict(kind='code',bbox=[0,0,1,1],text='100 PRINT "[BITMAP-100]"\n110 END\n120 STOP')]
        pred=[dict(kind='code',bbox=[0,0,1,1],text='100 PRINT "X"\n110 END\n130 NEW')]
        result=score(ref,pred)
        self.assertEqual(result['scored_lines'],2)
        self.assertEqual(result['excluded_uncertain_lines'],1)
        self.assertEqual(result['missing_line_numbers'],[120])
        self.assertEqual(result['extra_line_numbers'],[130])
        self.assertGreater(result['cer'],0)

    def test_manifest_rejects_tampering_and_unsafe_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); image=root/'image.png'; image.write_bytes(b'original')
            sample=dict(id='../escape',image='image.png',sha256=digest(image),reference=[])
            manifest=root/'manifest.json'
            manifest.write_text(json.dumps(dict(schema_version=1,samples=[sample])))
            with self.assertRaisesRegex(ValueError,'sample ID'):
                validate_manifest(manifest)
            sample['id']='sample'
            manifest.write_text(json.dumps(dict(schema_version=1,samples=[sample])))
            image.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'hash differs'):
                validate_manifest(manifest)

    def test_public_output_rejected(self):
        with self.assertRaisesRegex(ValueError,'archive/'):
            fresh_output('/tmp/qwen-public-output')

    def test_package_input_masks_exclusions_before_padding_or_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'source.pdf').write_bytes(b'source')
            package=dict(source=dict(path='source.pdf',sha256=digest(root/'source.pdf')),
                         pages=[dict(pdf_page=1,pdf_index=0)],
                         regions=[dict(pdf_index=0,bbox=[0,0,1,.5])],
                         excluded_regions=[dict(pdf_index=0,bbox=[0,.5,1,1])])
            (root/'package.json').write_text(json.dumps(package))
            def render(command,**kwargs):
                image=Image.new('RGB',(100,101),'blue')
                image.paste('red',(0,50,100,101))
                image.save(command[-1]+'.png')
            with patch('tools.ocr_qwen.inputs.ROOT',root), \
                 patch('tools.ocr_qwen.inputs.validate_package',side_effect=lambda x:x), \
                 patch('tools.ocr_qwen.inputs.orient_image',side_effect=lambda image,page:image), \
                 patch('tools.ocr_qwen.inputs.subprocess.run',side_effect=render):
                path=package_image(root/'package.json',1,root/'prepared')
            with Image.open(path) as image:
                self.assertNotIn((255,0,0),[c for _,c in image.getcolors(10100)])
                self.assertEqual(image.getpixel((25,50)),(255,255,255))


if __name__=='__main__':
    unittest.main()
