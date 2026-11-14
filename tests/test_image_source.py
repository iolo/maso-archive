"""JPEG input uses the shared OCR/export path without pretending to be PDF."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.image_source import load_image
from tools.pdf_restore.inventory import pin, write_json
from tools.pdf_restore.ocr import page_ocr
from tools.pdf_restore.package import image_transform, validate_package
from tests import test_pdf_build as pdf_fixtures

EXAMPLE = Path(__file__).resolve().parents[1] / 'examples/pdf-article.json'


def image_page(root, degrees=0):
    image = Image.new('RGB', (120, 80), 'blue')
    image.paste('red', (0, 40, 120, 80))
    if degrees:
        image = image.transpose({90: Image.Transpose.ROTATE_90, 180: Image.Transpose.ROTATE_180,
                                 270: Image.Transpose.ROTATE_270}[degrees])
    image.save(root / 'source.jpg', quality=100, subsampling=0)
    page = dict(source_index=7, image=pin(root, 'source.jpg'), width_px=image.width,
                height_px=image.height, reading_order=3, source_filename_number=29, printed_page=None)
    if degrees:
        page['orientation_correction'] = dict(clockwise_degrees=degrees, evidence='Synthetic sideways source')
    page['image_to_upright_normalized'] = image_transform(page)
    return page


def source_set(root, page):
    write_json(root / 'source-set.json', dict(kind='jpeg-set', issue_id='maso-1900-01',
                                            cleanup={}, pages=[page]))
    return dict(id='jpeg-synthetic', kind='jpeg-set', **pin(root, 'source-set.json'))


class ImageSourceTests(unittest.TestCase):
    def test_all_orientations_share_exclusions_and_keep_original_coordinates(self):
        for degrees in (0, 90, 180, 270):
            with self.subTest(degrees=degrees), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                page = image_page(root, degrees)
                original = (root / 'source.jpg').read_bytes()
                package = json.loads(EXAMPLE.read_bytes())
                package.update(schema_version=2, source=source_set(root, page), pages=[page],
                               regions=[dict(id='body', source_index=7, bbox=[0, 0, 1, .5], kind='prose', notes='')],
                               excluded_regions=[dict(id='ad', source_index=7, bbox=[0, .5, 1, 1], kind='advertisement', notes='')])
                write_json(root / 'map.json', package)
                write_json(root / 'runtime/runtime.json', {'synthetic': True})
                def engine(path, destination, config, runtime):
                    with Image.open(path) as image:
                        self.assertFalse(any(r > 200 and g < 40 and b < 40
                                             for _, (r,g,b) in image.getcolors(image.width*image.height)))
                        self.assertEqual(image.size, (120, 80) if config['name'] == 'page-psm3' else (120, 40))
                    destination.with_suffix('.txt').write_text('raw\n')
                    destination.with_suffix('.tsv').write_text('positions\n')
                    return .1
                with patch('tools.pdf_restore.ocr.ROOT', root), patch('tools.pdf_restore.ocr.verify_runtime'), \
                     patch('tools.pdf_restore.ocr.subprocess.run', side_effect=AssertionError('Must not render a PDF')), \
                     patch('tools.pdf_restore.ocr.run_region', side_effect=engine):
                    page_ocr(root / 'map.json', None, root / 'work/ocr', runtime=root / 'runtime', source_index=7)
                settings = json.loads((root / 'work/ocr/body-psm6.settings.json').read_bytes())
                self.assertEqual(settings['image'], page['image'])
                self.assertEqual(settings['source_index'], 7)
                self.assertNotIn('pdf_index', settings)
                self.assertEqual(original, (root / 'source.jpg').read_bytes())
                # Original pixel coordinates round-trip through each affine transform.
                a,b,c,d,e,f = page['image_to_upright_normalized']
                det = a*d-b*c
                for x,y in ((0,0), (page['width_px'],page['height_px']), (31,42)):
                    u,v = a*x+c*y+e, b*x+d*y+f
                    self.assertAlmostEqual((d*(u-e)-c*(v-f))/det,x)
                    self.assertAlmostEqual((-b*(u-e)+a*(v-f))/det,y)

    def fixture(self, root):
        recipe_path = pdf_fixtures.PDFBuildTests().fixture(root)
        base = recipe_path.parent
        page = image_page(root)
        source = source_set(root, page)
        package = json.loads((base / 'map.json').read_bytes())
        package.update(schema_version=2, source=source, pages=[page])
        for row in package['regions'] + package['excluded_regions']:
            row.pop('pdf_index'); row['source_index'] = 7
        write_json(base / 'map.json', package)
        inventory = root / 'private/pdf-restoration/inventory'
        write_json(inventory / 'sources.json', dict(sources=[dict(source, scope='toc-entries-and-cover', pages=[page])]))
        (inventory / 'queue.jsonl').write_text(json.dumps(dict(toc_entry_id=package['toc_entry_id'],
                issue_id=package['issue_id'], source_id=source['id']))+'\n')
        recipe = json.loads(recipe_path.read_bytes())
        recipe['inventory'] = {k: pin(root, f'private/pdf-restoration/inventory/{name}')
                               for k,name in [('sources','sources.json'),('queue','queue.jsonl')]}
        recipe['map'] = pin(base, 'map.json')
        evidence = json.loads((base / 'ocr/evidence.json').read_bytes())
        evidence.pop('pdf_page'); evidence.update(source_index=7, image=page['image'], source_sha256=source['sha256'])
        for row in evidence['results']:
            path = base / 'ocr' / row['settings']['path']
            settings = json.loads(path.read_bytes())
            settings.pop('pdf_page');settings.pop('pdf_index')
            settings.update(source_index=7, image=page['image'], source_sha256=source['sha256'], package={'sha256':recipe['map']['sha256']})
            write_json(path, settings);row['settings'] = pin(base / 'ocr', path.name)
        write_json(base / 'ocr/evidence.json', evidence)
        recipe['ocr_bundles'][0]['manifest'] = pin(base, 'ocr/evidence.json')
        corrections = json.loads((base / 'corrections.json').read_bytes());corrections['map'] = recipe['map']
        write_json(base / 'corrections.json', corrections);recipe['corrections'] = pin(base, 'corrections.json')
        write_json(recipe_path, recipe)
        return recipe_path

    def test_shared_export_rebuild_and_tampered_image_rejection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); recipe = self.fixture(root)
            for name in ['one','two']:
                build(recipe, root / 'work' / name, root)
                check_export(root / 'work' / name)
            files = lambda folder: {p.relative_to(folder).as_posix():p.read_bytes() for p in folder.rglob('*') if p.is_file()}
            self.assertEqual(files(root/'work/one'), files(root/'work/two'))
            self.assertFalse(any('pdf_index' in r for r in check_export(root/'work/one')['pages']))
            (root/'source.jpg').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'hash/size'):
                build(recipe,root/'work/tampered',root)
            self.assertFalse((root/'work/tampered').exists())

    def test_geometry_folio_and_source_identity_are_independent(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);recipe=self.fixture(root)
            package=json.loads((recipe.parent/'map.json').read_bytes())
            validate_package(package)
            bad=copy.deepcopy(package);bad['pages'][0]['image_to_upright_normalized'][0] += .01
            with self.assertRaisesRegex(ValueError,'Image transform'):validate_package(bad)
            bad=copy.deepcopy(package);bad['pages']*=2
            with self.assertRaisesRegex(ValueError,'Duplicate source'):validate_package(bad)
            bad=copy.deepcopy(package);bad['regions'][0]['bbox']=[0,0,2,1]
            with self.assertRaisesRegex(ValueError,'bounds'):validate_package(bad)
            page=copy.deepcopy(package['pages'][0]);page['width_px']+=1
            with self.assertRaisesRegex(ValueError,'dimensions'):load_image(page,root)
            page['image']['path']='../source.jpg'
            with self.assertRaisesRegex(ValueError,'Unsafe'):load_image(page,root)


if __name__ == '__main__':
    unittest.main()
