"""OCR input exclusions and evidence retention without a real engine or scans."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

from tools.pdf_restore.inventory import pin, write_json
from tools.pdf_restore.ocr import page_ocr
from tools.pdf_restore.package import page_transform

EXAMPLE = Path(__file__).resolve().parents[1] / 'examples/pdf-article.json'


class PDFOCRTests(unittest.TestCase):
    def test_shared_page_masks_boundary_pixels_and_keeps_raw_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'source.pdf').write_bytes(b'synthetic source')
            write_json(root / 'runtime/runtime.json', {'synthetic': True})
            package = json.loads(EXAMPLE.read_bytes())
            package['source'].update(pin(root, 'source.pdf'))
            page = dict(pdf_index=0, pdf_page=1, printed_page='7', width_pt=100, height_pt=101,
                        MediaBox=[0, 0, 100, 101], CropBox=[0, 0, 100, 101], rotation=0)
            page['pdf_to_upright_normalized'] = page_transform(page)
            package['pages'] = [page]
            package['regions'] = [dict(id='body', pdf_index=0, kind='prose', bbox=[0, 0, 1, .5], notes='')]
            package['excluded_regions'] = [dict(id='ad', pdf_index=0, kind='advertisement', bbox=[0, .5, 1, 1], notes='')]
            write_json(root / 'package.json', package)
            def render(args, **kwargs):
                image = Image.new('RGB', (100, 101), 'blue')
                image.paste('red', (0, 50, 100, 101))  # Excluded advertisement sentinel.
                image.save(args[-1] + '.png')
            def engine(image, destination, config, runtime):
                with Image.open(image) as rendered:
                    colors = rendered.getcolors(rendered.width * rendered.height)
                    self.assertNotIn((255, 0, 0), [color for _, color in colors])
                destination.with_suffix('.txt').write_text('unchanged raw\n')
                destination.with_suffix('.tsv').write_text('positional evidence\n')
                return .1
            output = root / 'private/ocr'
            with patch('tools.pdf_restore.ocr.ROOT', root), patch('tools.pdf_restore.ocr.verify_runtime'), \
                 patch('tools.pdf_restore.ocr.subprocess.run', side_effect=render), \
                 patch('tools.pdf_restore.ocr.run_region', side_effect=engine):
                result = page_ocr(root / 'package.json', 1, output, runtime=root / 'runtime')
                self.assertEqual(len(result), 2)
                for row in result:
                    for field in ('text', 'positions', 'settings'):
                        self.assertEqual(row[field], pin(output, row[field]['path']))
                with self.assertRaisesRegex(ValueError, 'already exists'):
                    page_ocr(root / 'package.json', 1, output, runtime=root / 'runtime')
                self.assertEqual((output / 'body-psm6.txt').read_text(), 'unchanged raw\n')


if __name__ == '__main__':
    unittest.main()
