"""Mapped Qwen evidence remains compatible, honest about positions, and resumable."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from PIL import Image

from tools.pdf_restore.inventory import pin, write_json
from tools.ocr_qwen.mapped import run


class MappedQwenTests(unittest.TestCase):
    def test_masked_raw_ocr_contract_figures_and_cache_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'source.pdf').write_bytes(b'source')
            (root/'model').write_bytes(b'model')
            p=dict(id='article',source=pin(root,'source.pdf'),pages=[dict(pdf_page=1,pdf_index=0)],
                   regions=[dict(id='body',pdf_index=0,kind='prose',bbox=[0,0,1,.5]),
                            dict(id='figure',pdf_index=0,kind='figure',bbox=[0,.6,1,1])],
                   excluded_regions=[dict(pdf_index=0,bbox=[0,.5,1,1])],mapping=dict(status='mapped'))
            write_json(root/'map.json',p)
            write_json(root/'request.json',dict(articles=[dict(map=pin(root,'map.json'))]))
            server=SimpleNamespace(binary=root/'model',model=root/'model',mmproj=root/'model',
                                   context=8192,image_tokens=4096,gpu_layers=99,url='http://localhost')
            def render(args,**kwargs):
                image=Image.new('RGB',(100,101),'blue');image.paste('red',(0,50,100,101))
                image.save(args[-1]+'.png')
            response=dict(choices=[dict(finish_reason='stop',message=dict(content='{"text":"draft"}'))],usage={})
            with patch('tools.ocr_qwen.mapped.ROOT',root), patch('tools.ocr_qwen.workflow.ROOT',root), \
                 patch('tools.ocr_qwen.mapped.validate_package',side_effect=lambda x:x), \
                 patch('tools.ocr_qwen.mapped.validate_source'), \
                 patch('tools.ocr_qwen.mapped.orient_image',side_effect=lambda x,p:x), \
                 patch('tools.ocr_qwen.mapped.subprocess.run',side_effect=render), \
                 patch('tools.ocr_qwen.mapped.Server') as cls, \
                 patch('tools.ocr_qwen.workflow.Monitor') as monitor, \
                 patch('tools.ocr_qwen.pipeline.request',return_value=response) as api:
                monitor.return_value.__enter__.return_value.metrics={'wall_seconds':0.1}
                instance=cls.return_value
                for k,v in vars(server).items():setattr(instance,k,v)
                instance.__enter__.return_value=instance
                out=root/'private/run'
                result=run(root/'request.json',out)
                self.assertEqual(result['new_inferences'],1)
                self.assertEqual(api.call_count,1)
                folder=out/'article/ocr-page1'
                with Image.open(folder/'body.png') as image:
                    self.assertNotIn((255,0,0),[c for _,c in image.getcolors(10100)])
                evidence=json.loads((folder/'evidence.json').read_bytes())
                self.assertEqual(len(evidence['images']),2)
                self.assertEqual(len(evidence['results']),1)
                positions=json.loads((folder/'body-qwen.positions.json').read_bytes())
                self.assertFalse(positions['word_positions_available'])
                self.assertEqual(positions['native_response'],response)
                self.assertEqual((folder/'body-qwen.txt').read_text(),'draft\n')
                again=run(root/'request.json',out,resume=True)
                self.assertEqual(again['cache_hits'],1)
                self.assertEqual(again['new_inferences'],0)
                self.assertEqual(api.call_count,1)


if __name__=='__main__':unittest.main()
