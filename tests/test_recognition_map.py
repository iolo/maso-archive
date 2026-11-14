"""Figure crop review can reuse pinned OCR without rebinding its settings."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from tools.pdf_restore.build import build, check_export, validate_recognition_map
from tools.pdf_restore.inventory import pin, write_json
from tests import test_image_source, test_pdf_build


class RecognitionMapTests(unittest.TestCase):
    def fixture(self, root, jpeg):
        fixture = test_image_source.ImageSourceTests() if jpeg else test_pdf_build.PDFBuildTests()
        path = fixture.fixture(root)
        base = path.parent
        recipe = json.loads(path.read_bytes())
        old = (base / 'map.json').read_bytes()
        (base / 'recognition-map.json').write_bytes(old)
        current = json.loads(old)
        current['regions'][1]['bbox'][1] = .01
        write_json(base / 'map.json', current)
        recipe['map'] = pin(base, 'map.json')
        recipe['ocr_bundles'][0]['recognition_map'] = pin(base, 'recognition-map.json')
        # A new reviewed figure asset; recognition results/settings stay exact.
        Image.new('RGB', (20, 19), 'green').save(base / 'ocr/r2.png')
        evidence = json.loads((base / 'ocr/evidence.json').read_bytes())
        evidence['images'] = [pin(base / 'ocr', r['path']) for r in evidence['images']]
        write_json(base / 'ocr/evidence.json', evidence)
        recipe['ocr_bundles'][0]['manifest'] = pin(base, 'ocr/evidence.json')
        corrections = json.loads((base / 'corrections.json').read_bytes())
        corrections['map'] = recipe['map']
        corrections['records'][1]['scan'] = pin(base, 'ocr/r2.png')
        write_json(base / 'corrections.json', corrections)
        recipe['corrections'] = pin(base, 'corrections.json')
        write_json(path, recipe)
        return path

    def test_pdf_and_jpeg_rebuild_preserve_original_settings_and_both_maps(self):
        for jpeg in (False, True):
            with self.subTest(jpeg=jpeg), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                path = self.fixture(root, jpeg)
                base = path.parent
                raw = {p.name:p.read_bytes() for p in (base / 'ocr').glob('*')
                       if p.suffix in ('.txt', '.tsv', '.json')}
                outputs = [root / 'work' / name for name in ('one', 'two')]
                for output in outputs:
                    package = build(path, output, root)
                    self.assertEqual(check_export(output), package)
                    self.assertEqual((output / 'ocr/recognition-map.json').read_bytes(),
                                     (base / 'recognition-map.json').read_bytes())
                    self.assertEqual((output / 'map.json').read_bytes(), (base / 'map.json').read_bytes())
                    for name, data in raw.items():
                        if name != 'evidence.json':
                            self.assertEqual((output / 'ocr' / name).read_bytes(), data)
                    with Image.open(output / 'ocr/r2.png') as image:
                        self.assertEqual(image.size, (20, 19))
                files = lambda folder: {p.relative_to(folder).as_posix():p.read_bytes()
                                        for p in folder.rglob('*') if p.is_file()}
                self.assertEqual(files(outputs[0]), files(outputs[1]))

    def test_reuse_rejects_every_other_map_change(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = self.fixture(root, True)
            original = json.loads((path.parent / 'recognition-map.json').read_bytes())
            current = json.loads((path.parent / 'map.json').read_bytes())
            mutations = {
                'text crop': lambda p: p['regions'][0]['bbox'].__setitem__(0, .01),
                'text role': lambda p: p['regions'][0].__setitem__('kind', 'code'),
                'exclusion': lambda p: p['excluded_regions'][0]['bbox'].__setitem__(1, .61),
                'source': lambda p: p['source'].__setitem__('sha256', '0' * 64),
                'page': lambda p: p['pages'][0].__setitem__('printed_page', '3'),
                'identity': lambda p: p.__setitem__('title', 'different'),
                'figure note': lambda p: p['regions'][1].__setitem__('notes', 'different'),
                'figure addition': lambda p: p['regions'].append(dict(p['regions'][1], id='extra')),
                'figure removal': lambda p: p['regions'].pop(1),
                'region order': lambda p: p['regions'].reverse(),
            }
            validate_recognition_map(original, current)
            for name, mutate in mutations.items():
                with self.subTest(name=name):
                    changed = copy.deepcopy(current)
                    mutate(changed)
                    with self.assertRaises(ValueError):
                        validate_recognition_map(original, changed)

    def test_old_map_pin_settings_binding_and_opt_in_are_required(self):
        for fault in ('tampered map', 'wrong binding', 'no opt in', 'unsafe pin'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                path = self.fixture(root, True)
                recipe = json.loads(path.read_bytes())
                bundle = recipe['ocr_bundles'][0]
                if fault == 'tampered map':
                    (path.parent / 'recognition-map.json').write_text('{}')
                elif fault == 'wrong binding':
                    bundle['recognition_map'] = recipe['map']
                elif fault == 'no opt in':
                    del bundle['recognition_map']
                else:
                    bundle['recognition_map']['path'] = '../recognition-map.json'
                write_json(path, recipe)
                output = root / 'work/rejected'
                with self.assertRaises(ValueError):
                    build(path, output, root)
                self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
