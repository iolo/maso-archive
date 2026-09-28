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
        for degrees in (0, 90, 180, 270):
            with self.subTest(degrees=degrees):
                self.check_shared_page(degrees)

    def check_shared_page(self, degrees):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'source.pdf').write_bytes(b'synthetic source')
            write_json(root / 'runtime/runtime.json', {'synthetic': True})
            package = json.loads(EXAMPLE.read_bytes())
            package['source'].update(pin(root, 'source.pdf'))
            page = dict(pdf_index=0, pdf_page=1, printed_page='7', width_pt=100, height_pt=101,
                        MediaBox=[0, 0, 100, 101], CropBox=[0, 0, 100, 101], rotation=0)
            if degrees:
                page['orientation_correction'] = dict(clockwise_degrees=degrees, evidence='Synthetic sideways page')
            page['pdf_to_upright_normalized'] = page_transform(page)
            package['pages'] = [page]
            package['regions'] = [dict(id='body', pdf_index=0, kind='prose', bbox=[0, 0, 1, .5], notes='')]
            package['excluded_regions'] = [dict(id='ad', pdf_index=0, kind='advertisement', bbox=[0, .5, 1, 1], notes='')]
            write_json(root / 'package.json', package)
            def render(args, **kwargs):
                image = Image.new('RGB', (100, 101), 'blue')
                image.paste('red', (0, 50, 100, 101))  # Excluded advertisement sentinel.
                if degrees:
                    image = image.transpose({90: Image.Transpose.ROTATE_90, 180: Image.Transpose.ROTATE_180,
                                             270: Image.Transpose.ROTATE_270}[degrees])
                image.save(args[-1] + '.png')
            def engine(image, destination, config, runtime):
                with Image.open(image) as rendered:
                    colors = rendered.getcolors(rendered.width * rendered.height)
                    self.assertNotIn((255, 0, 0), [color for _, color in colors])
                    self.assertIn((0, 0, 255), [color for _, color in colors])
                    self.assertEqual(rendered.size, (100, 101) if config['name'] == 'page-psm3' else (100, 51))
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
                settings = json.loads((output / 'body-psm6.settings.json').read_bytes())
                evidence = json.loads((output / 'evidence.json').read_bytes())
                for record in (settings, evidence):
                    self.assertEqual(record.get('orientation_correction'), page.get('orientation_correction'))
                self.assertEqual(settings['render_size'], [100, 101])
                self.assertEqual(settings['crop_pixels'], [0, 0, 100, 51])


if __name__ == '__main__':
    unittest.main()
