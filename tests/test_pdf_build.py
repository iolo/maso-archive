"""Synthetic package publication, preservation, rendering and integrity gates."""
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from PIL import Image

from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.inventory import pin, write_json
from tools.pdf_restore.package import page_transform

EXAMPLE = Path(__file__).resolve().parents[1] / 'examples/pdf-article.json'


class PDFBuildTests(unittest.TestCase):
    def fixture(self, root, with_code=True, first_kind='prose', toc_number='0001'):
        last_kind = 'code' if with_code else 'prose'
        base = root / 'private/pilot'
        folder = base / 'ocr'
        folder.mkdir(parents=True)
        (root / 'source.pdf').write_bytes(b'synthetic source; never exported')
        (root / 'TOC.md').write_text('Synthetic TOC')
        runtime = root / 'private/pdf-restoration/ocr-runtime'
        write_json(runtime / 'runtime.json', {'synthetic': True})
        package = json.loads(EXAMPLE.read_bytes())
        package['id'] = 'scan-maso-1900-01-toc-' + toc_number
        package['toc_entry_id'] = 'maso-1900-01-toc-' + toc_number
        package['source'].update(pin(root, 'source.pdf'))
        package['toc_pin'] = pin(root, 'TOC.md')
        page = dict(pdf_index=0, pdf_page=1, printed_page='2', width_pt=100, height_pt=100,
                    MediaBox=[0, 0, 100, 100], CropBox=[0, 0, 100, 100], rotation=0)
        page['pdf_to_upright_normalized'] = page_transform(page)
        package['pages'] = [page]
        package['regions'] = [dict(id=id, pdf_index=0, kind=kind, bbox=box, notes='Synthetic') for id, kind, box in
                              [('r1', first_kind, [0, 0, .5, .4]), ('r2', 'figure', [.5, 0, 1, .4]),
                               ('r3', last_kind, [0, .4, 1, .6])]]
        package['excluded_regions'] = [dict(id='ad', pdf_index=0, kind='advertisement', bbox=[0, .6, 1, 1], notes='Excluded')]
        package['mapping'] = dict(status='mapped', evidence=['Synthetic complete extent'], uncertainties=[])
        write_json(base / 'map.json', package)
        inventory = root / 'private/pdf-restoration/inventory'
        write_json(inventory / 'sources.json', {'sources': [{**package['source'], 'scope': 'toc-entries-and-cover', 'pages': [page]}]})
        (inventory / 'queue.jsonl').write_text(json.dumps(dict(toc_entry_id=package['toc_entry_id'], issue_id=package['issue_id'], source_id=package['source']['id'])) + '\n')
        results, records, images, blocks = [], [], [], []
        for id, kind in [('r1', first_kind), ('r2', 'figure'), ('r3', last_kind)]:
            Image.new('RGB', (20, 20), 'blue').save(folder / f'{id}.png')
            images.append(pin(folder, f'{id}.png'))
            raw = None
            if kind != 'figure':
                (folder / f'{id}.txt').write_text('raw OCR remains unchanged\n')
                (folder / f'{id}.tsv').write_text('positions\n')
                write_json(folder / f'{id}.settings.json', dict(package={'sha256': pin(base, 'map.json')['sha256']},
                           source_sha256=package['source']['sha256'], pdf_index=0, pdf_page=1, region_ids=[id]))
                results.append(dict(region_ids=[id], text=pin(folder, f'{id}.txt'), positions=pin(folder, f'{id}.tsv'),
                                    settings=pin(folder, f'{id}.settings.json')))
                raw = pin(base, f'ocr/{id}.txt')
                text = ('  10 PRINT "<tag>&"\n\n\t20 END  \n' if kind == 'code' else
                        'Synthetic corrected prose.\n\nSecond paragraph with <literal> & text.')
                blocks.append(dict(id=id + '-block', kind=kind, text=text, region_ids=[id],
                                   correction_evidence=[f'corrections.json#{id}'], uncertainties=[]))
            records.append(dict(id=id, scan=pin(base, f'ocr/{id}.png'), raw_ocr=raw))
        Image.new('RGB', (100, 100), 'red').save(folder / 'page.png')
        images.append(pin(folder, 'page.png'))  # Contains advertising; cannot enter export.
        write_json(folder / 'evidence.json', dict(source_sha256=package['source']['sha256'], pdf_page=1,
                   runtime=pin(runtime, 'runtime.json'), results=results, images=images))
        write_json(base / 'corrections.json', dict(article_id=package['id'], map=pin(base, 'map.json'), records=records, blocks=blocks))
        recipe = dict(map=pin(base, 'map.json'), corrections=pin(base, 'corrections.json'),
                      ocr_bundles=[dict(directory='ocr', manifest=pin(base, 'ocr/evidence.json'))], runtime=pin(runtime, 'runtime.json'),
                      figures=[dict(id='figure', region_ids=['r2'], region_id='r2', caption=None)],
                      content_order=[dict(type='block', id='r1-block'), dict(type='figure', id='figure'), dict(type='block', id='r3-block')],
                      availability='readable', verification=dict(status='sample-reviewed', reviewed_region_ids=['r1', 'r2', 'r3'],
                      evidence=['Synthetic comparison'], uncertainties=[]), gaps=[])
        write_json(base / 'recipe.json', recipe)
        return base / 'recipe.json'

    def test_deterministic_portable_export_preserves_raw_code_and_excludes_ad(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            recipe = self.fixture(root)
            raw_before = (recipe.parent / 'ocr/r3.txt').read_bytes()
            output, repeat = root / 'build/one', root / 'build/two'
            package = build(recipe, output, root)
            build(recipe, repeat, root)
            files = lambda d: {p.relative_to(d).as_posix(): p.read_bytes() for p in d.rglob('*') if p.is_file()}
            self.assertEqual(files(output), files(repeat))
            self.assertEqual(check_export(output), package)
            self.assertEqual((recipe.parent / 'ocr/r3.txt').read_bytes(), raw_before)
            self.assertEqual((output / 'listing.txt').read_text(), package['blocks'][1]['text'])
            html = (output / 'index.html').read_text()
            self.assertIn('  10 PRINT &quot;&lt;tag&gt;&amp;&quot;\n\n\t20 END  \n', html)
            self.assertNotIn('<tag>', html)
            self.assertIn('<p class="text prose">Synthetic corrected prose.</p>'
                          '<p class="text prose">Second paragraph with &lt;literal&gt; &amp; text.</p>', html)
            self.assertIn(package['blocks'][0]['text'], (output / 'article.txt').read_text())
            self.assertLess(html.index('r1-block'), html.index('id="figure"'))
            self.assertLess(html.index('id="figure"'), html.index('r3-block'))
            self.assertFalse((output / 'ocr/page.png').exists())
            self.assertFalse((output / 'source.pdf').exists())
            with zipfile.ZipFile(output / 'raw-ocr.zip') as archive:
                self.assertNotIn('ocr/page.png', archive.namelist())
                self.assertEqual(archive.read('ocr/r3.txt'), raw_before)
            with self.assertRaisesRegex(ValueError, 'already exists'):
                build(recipe, output, root)

    def test_oriented_page_requires_matching_image_and_ocr_provenance(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            recipe_path = self.fixture(root)
            base = recipe_path.parent
            correction = dict(clockwise_degrees=180, evidence='Synthetic inverted title')
            package = json.loads((base / 'map.json').read_bytes())
            package['pages'][0]['orientation_correction'] = correction
            package['pages'][0]['pdf_to_upright_normalized'] = page_transform(package['pages'][0])
            write_json(base / 'map.json', package)
            recipe = json.loads(recipe_path.read_bytes())
            recipe['map'] = pin(base, 'map.json')
            corrections = json.loads((base / 'corrections.json').read_bytes())
            corrections['map'] = recipe['map']
            write_json(base / 'corrections.json', corrections)
            recipe['corrections'] = pin(base, 'corrections.json')
            evidence = json.loads((base / 'ocr/evidence.json').read_bytes())
            for row in evidence['results']:
                path = base / 'ocr' / row['settings']['path']
                settings = json.loads(path.read_bytes())
                settings['package']['sha256'] = recipe['map']['sha256']
                write_json(path, settings)
                row['settings'] = pin(base / 'ocr', path.name)

            def save_evidence():
                write_json(base / 'ocr/evidence.json', evidence)
                recipe['ocr_bundles'][0]['manifest'] = pin(base, 'ocr/evidence.json')
                write_json(recipe_path, recipe)

            save_evidence()
            with self.assertRaisesRegex(ValueError, 'evidence orientation'):
                build(recipe_path, root / 'build/missing-image-provenance', root)
            evidence['orientation_correction'] = correction
            save_evidence()
            with self.assertRaisesRegex(ValueError, 'orientation correction'):
                build(recipe_path, root / 'build/missing-ocr-provenance', root)
            for row in evidence['results']:
                path = base / 'ocr' / row['settings']['path']
                settings = json.loads(path.read_bytes())
                settings['orientation_correction'] = correction
                write_json(path, settings)
                row['settings'] = pin(base / 'ocr', path.name)
            save_evidence()
            output = root / 'build/oriented'
            built = build(recipe_path, output, root)
            self.assertEqual(built['pages'][0]['rotation'], 0)
            self.assertEqual(built['pages'][0]['orientation_correction'], correction)
            self.assertEqual(check_export(output), built)

    def test_prose_only_article_omits_listing_download(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            recipe = self.fixture(root, with_code=False)
            output = root / 'build/output'
            package = build(recipe, output, root)
            self.assertEqual(check_export(output), package)
            self.assertEqual([item['path'] for item in package['downloads']], ['article.txt', 'raw-ocr.zip'])
            self.assertFalse((output / 'listing.txt').exists())
            self.assertNotIn('listing.txt', (output / 'index.html').read_text())
            text = (output / 'article.txt').read_text()
            self.assertEqual(text.count('Synthetic corrected prose.'), 2)
            self.assertIn('[그림 figure: 스캔 이미지 참조]', text)

    def test_modified_raw_ocr_is_rejected_before_publication(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            recipe = self.fixture(root)
            (recipe.parent / 'ocr/r1.txt').write_text('tampered')
            with self.assertRaisesRegex(ValueError, 'hash/size'):
                build(recipe, root / 'build/output', root)
            self.assertFalse((root / 'build/output').exists())

    def test_readable_cannot_silently_drop_a_region(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            recipe_path = self.fixture(root)
            base = recipe_path.parent
            correction = json.loads((base / 'corrections.json').read_bytes())
            correction['blocks'].pop()
            write_json(base / 'corrections.json', correction)
            recipe = json.loads(recipe_path.read_bytes())
            recipe['corrections'] = pin(base, 'corrections.json')
            recipe['content_order'].pop()
            write_json(recipe_path, recipe)
            with self.assertRaisesRegex(ValueError, 'every mapped region'):
                build(recipe_path, root / 'build/output', root)
            self.assertFalse((root / 'build/output').exists())

    def test_unknown_toc_and_unsafe_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            recipe = self.fixture(root)
            (root / 'private/pdf-restoration/inventory/queue.jsonl').write_text('')
            with self.assertRaisesRegex(ValueError, 'existing eligible TOC'):
                build(recipe, root / 'build/output', root)
            data = json.loads(recipe.read_bytes())
            data['map']['path'] = '../map.json'
            write_json(recipe, data)
            with self.assertRaisesRegex(ValueError, 'Unsafe artifact path'):
                build(recipe, root / 'build/output', root)

    def test_export_check_rejects_missing_asset_and_bad_anchor(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            recipe = self.fixture(root)
            output = root / 'build/output'
            build(recipe, output, root)
            original = (output / 'index.html').read_text()
            (output / 'index.html').write_text(original + '<a href="#missing">Broken</a>')
            with self.assertRaisesRegex(ValueError, 'Broken preview fragment'):
                check_export(output)
            (output / 'index.html').write_text(original)
            (output / 'ocr/r2.png').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'hash/size'):
                check_export(output)


if __name__ == '__main__':
    unittest.main()
