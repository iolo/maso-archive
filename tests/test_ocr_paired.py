"""A failed raw draft must remain visible without contaminating the paired arm."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

from tools.ocr_qwen import paired
from tools.pdf_restore.inventory import digest, pin, write_json


class FakeServer:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class PairedFailureTests(unittest.TestCase):
    def test_failed_response_is_preserved_and_next_region_runs_without_fallback(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); shared = root / 'private/shared'; shared.mkdir(parents=True)
            regions = [dict(id=id, pdf_index=0, kind='code', bbox=[0, 0, 1, 1]) for id in ('a', 'b')]
            package = dict(id='article', source={'sha256': 'source'}, pages=[dict(pdf_index=0, pdf_page=1)], regions=regions)
            write_json(shared / 'map.json', package)
            for r in regions:
                Image.new('RGB', (10, 10), 'white').save(shared / (r['id'] + '.png'))
            qwen = dict(files={}, context=8192, image_tokens=4096, gpu_layers=99, prompt='{kind}',
                        schema={}, region_max_tokens={}, max_tokens=2048, timeout=600)
            frozen = dict(qwen=qwen, map=pin(shared, 'map.json'), crops={r['id']: pin(shared, r['id'] + '.png') for r in regions})
            write_json(shared / 'frozen-inputs.json', frozen)
            calls = []
            def fake_infer(server, image, prompt, schema, destination, max_tokens, timeout):
                rid = destination.parent.name; calls.append(rid)
                write_json(destination.with_suffix('.request.json'), {'image_sha256': digest(shared / (rid + '.png'))})
                response = {'choices': [{'finish_reason': 'length' if rid == 'a' else 'stop',
                                        'message': {'content': '{"text":"unfinished' if rid == 'a' else '{"text":"second"}'}}],
                            'usage': {'prompt_tokens': 10, 'completion_tokens': 2, 'total_tokens': 12}}
                write_json(destination.with_suffix('.response.json'), response)
                if rid == 'a':
                    raise ValueError('Incomplete model response (length)')
                return {'text': 'second'}, {'seconds': .01, 'usage': response['usage']}
            output = root / 'private/output'
            with patch.object(paired, 'ROOT', root), patch.object(paired, 'verify_inputs', return_value=(frozen, package)), \
                 patch('tools.ocr_qwen.workflow.ROOT', root), \
                 patch.object(paired, 'Server', FakeServer), patch.object(paired, 'infer', side_effect=fake_infer), \
                 patch.object(paired, 'run_region') as tesseract:
                report = paired.run(shared, 'qwen', output)
                self.assertEqual(calls, ['a', 'b'])
                self.assertEqual(report['failed_regions'], ['a'])
                self.assertEqual(report['status'], 'raw-complete-with-failures')
                tesseract.assert_not_called()
                folder = output / 'article/ocr-page1'
                self.assertEqual((folder / 'a-qwen.txt').read_text(), '{"text":"unfinished\n')
                self.assertEqual((folder / 'b-qwen.txt').read_text(), 'second\n')
                self.assertEqual((folder / 'a.png').read_bytes(), (shared / 'a.png').read_bytes())
                attempts = json.loads((output / 'attempts.json').read_bytes())
                self.assertEqual(sum(a['usage']['total_tokens'] for a in attempts), 24)
                with self.assertRaises(FileExistsError):
                    paired.run(shared, 'qwen', output)
                self.assertEqual((folder / 'a-qwen.txt').read_text(), '{"text":"unfinished\n')


if __name__ == '__main__':
    unittest.main()
