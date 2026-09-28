"""Synthetic segment assembly, UTF-8 offsets, immutable provenance and tamper rejection."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from PIL import Image

from tools.pdf_restore.assemble import assemble, project, read_segment
from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.inventory import pin, write_json
from tools.pdf_restore.package import page_transform

EXAMPLE = Path(__file__).resolve().parents[1] / 'examples/pdf-article.json'


class PDFAssemblyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'source.pdf').write_bytes(b'synthetic immutable source')
        (self.root / 'TOC.md').write_text('Synthetic canonical TOC')
        runtime = self.root / 'private/pdf-restoration/ocr-runtime'
        write_json(runtime / 'runtime.json', {'synthetic': True})
        template = json.loads(EXAMPLE.read_bytes())
        template['source'].update(pin(self.root, 'source.pdf'))
        template['toc_pin'] = pin(self.root, 'TOC.md')
        pages = []
        for i in range(2):
            page = dict(pdf_index=i, pdf_page=i+1, printed_page=str(i+7), width_pt=100, height_pt=200,
                        rotation=0, MediaBox=[10, 20, 110, 220], CropBox=[10, 20, 110, 220])
            page['pdf_to_upright_normalized'] = page_transform(page)
            pages.append(page)
        inventory = self.root / 'private/pdf-restoration/inventory'
        write_json(inventory / 'sources.json', {'sources': [{**template['source'], 'scope': 'toc-entries-and-cover', 'pages': pages}]})
        (inventory / 'queue.jsonl').write_text(json.dumps(dict(toc_entry_id=template['toc_entry_id'], issue_id=template['issue_id'], source_id=template['source']['id']))+'\n')
        specs = []
        for i, name in enumerate(('opening', 'continuation')):
            base = self.root / 'private' / name
            folder = base / 'ocr'
            folder.mkdir(parents=True)
            package = deepcopy(template)
            page = deepcopy(pages[i])
            if i:
                page['orientation_correction'] = dict(clockwise_degrees=180, evidence='Synthetic inverted title')
                page['pdf_to_upright_normalized'] = page_transform(page)
            code_id, figure_id = f'code{i}', f'figure{i}'
            package.update(pages=[page], regions=[dict(id=code_id, pdf_index=i, kind='code', bbox=[0, 0, 1, .5], notes='Synthetic'),
                                                 dict(id=figure_id, pdf_index=i, kind='figure', bbox=[0, .5, 1, 1], notes='Synthetic')],
                           excluded_regions=[], mapping=dict(status='mapped', evidence=['Observed segment extent'], uncertainties=[]))
            write_json(base / 'map.json', package)
            first_line = 10 + 20*i
            marker = f'⟦G{first_line}⟧'
            text = f'  {first_line} PRINT "한글{marker}"\n{first_line+10} DEF CHR$(&H80)=CHR$(1)\n'
            block = dict(id='block'+str(i), kind='code', text=text, region_ids=[code_id],
                         correction_evidence=['corrections.json#'+code_id], uncertainties=['Glyph bytes unverified.'])
            for id in (code_id, figure_id):
                Image.new('RGB', (20, 30), 'blue').save(folder / (id+'.png'))
            (folder / 'raw.txt').write_text('Unaltered OCR bytes\n')
            (folder / 'raw.tsv').write_text('Unaltered positions\n')
            orientation = {k: page[k] for k in ('orientation_correction',) if k in page}
            write_json(folder / 'raw.settings.json', dict(package={'sha256': pin(base, 'map.json')['sha256']},
                       source_sha256=package['source']['sha256'], pdf_index=i, pdf_page=i+1, region_ids=[code_id], **orientation))
            write_json(folder / 'evidence.json', dict(source_sha256=package['source']['sha256'], pdf_page=i+1,
                       runtime=pin(runtime, 'runtime.json'), **orientation,
                       images=[pin(folder, id+'.png') for id in (code_id, figure_id)],
                       results=[dict(region_ids=[code_id], text=pin(folder, 'raw.txt'), positions=pin(folder, 'raw.tsv'), settings=pin(folder, 'raw.settings.json'))]))
            scan = pin(base, 'ocr/'+code_id+'.png')
            write_json(base / 'corrections.json', dict(article_id=package['id'], map=pin(base, 'map.json'),
                       records=[dict(id=id, scan=pin(base, 'ocr/'+id+'.png'), raw_ocr=pin(base, 'ocr/raw.txt') if id==code_id else None)
                                for id in (code_id, figure_id)], blocks=[block],
                       listing_index=[dict(block_id=block['id'], region_id=code_id, download='listing.txt', utf8_byte_start=0,
                                           utf8_byte_end_exclusive=len(text.encode()), printed_line_range=[first_line,first_line+10])],
                       unresolved_graphics=[dict(id=marker[1:-1], marker=marker, printed_line=first_line, region_id=code_id,
                                                scan=scan, encoded_bytes=None, character_count=None, status='unresolved')],
                       glyph_definitions=[dict(printed_line=first_line+10, printed_code='&H80', region_id=code_id, scan=scan,
                                               download='listing.txt', utf8_byte_start=len(text.splitlines(True)[0].encode()),
                                               utf8_byte_end_exclusive=len(text.encode()), graphic_occurrence_assignment=None)]))
            recipe = dict(map=pin(base, 'map.json'), corrections=pin(base, 'corrections.json'),
                          ocr_bundles=[dict(directory='ocr', manifest=pin(base, 'ocr/evidence.json'))], runtime=pin(runtime, 'runtime.json'),
                          figures=[dict(id=figure_id, region_ids=[figure_id], region_id=figure_id, caption=None)],
                          content_order=[dict(type='figure', id=figure_id), dict(type='block', id=block['id'])],
                          availability='partial', verification=dict(status='sample-reviewed', reviewed_region_ids=[code_id, figure_id],
                          evidence=['Included regions compared'], uncertainties=['Other segment is separate.', 'Glyph bytes unverified.']),
                          gaps=['Other segment is separate.', 'Glyph bytes unverified.'])
            write_json(base / 'recipe.json', recipe)
            output = self.root / 'build' / name
            build(base / 'recipe.json', output, self.root)
            specs.append(dict(name=name, manifest=pin(self.root, output.relative_to(self.root).as_posix()+'/manifest.json')))
        self.recipe = dict(segments=specs, expected_pdf_pages=[1,2], evidence=['Complete source coverage compared with both segments.'],
                           uncertainties=['Code remains unverified.'],
                           resolved_notes=[dict(segment=name, note='Other segment is separate.', reason='Both segments are now assembled.')
                                           for name in ('opening','continuation')])
        self.recipe_path = self.root / 'private/assembly-recipe.json'
        self.output = self.root / 'build/assembled'

    def run_assembly(self, output=None):
        write_json(self.recipe_path, self.recipe)
        return assemble(self.recipe_path, output or self.output, self.root)

    def rehash(self, folder):
        manifest = json.loads((folder / 'manifest.json').read_bytes())
        manifest['files'] = [pin(folder, row['path']) for row in manifest['files']]
        write_json(folder / 'manifest.json', manifest)
        for spec in self.recipe['segments']:
            if spec['name'] == folder.name:
                spec['manifest'] = pin(self.root, folder.relative_to(self.root).as_posix()+'/manifest.json')

    def test_deterministic_assembly_preserves_segments_offsets_and_review(self):
        original = {name:{p.relative_to(self.root/'build'/name).as_posix():p.read_bytes()
                         for p in (self.root/'build'/name).rglob('*') if p.is_file()}
                    for name in ('opening','continuation')}
        with patch('tools.pdf_restore.ocr.page_ocr', side_effect=AssertionError('No OCR')):
            package = self.run_assembly()
        self.assertEqual(check_export(self.output), package)
        self.assertEqual(package['availability'], 'readable')
        self.assertEqual(package['verification']['status'], 'sample-reviewed')
        self.assertIn('Glyph bytes unverified.', package['gaps'])
        self.assertNotIn('Other segment is separate.', package['gaps'])
        self.assertEqual(package['pages'][1]['rotation'], 0)
        self.assertEqual(package['pages'][1]['orientation_correction']['clockwise_degrees'], 180)
        for name, files in original.items():
            for path, value in files.items():
                self.assertEqual((self.output/'segments'/name/path).read_bytes(), value)
                self.assertEqual((self.root/'build'/name/path).read_bytes(), value)
        listing = (self.output/'listing.txt').read_bytes()
        self.assertEqual(listing, original['opening']['listing.txt']+original['continuation']['listing.txt'])
        corrections = json.loads((self.output/'corrections.json').read_bytes())
        for row in corrections['glyph_definitions']:
            self.assertTrue(listing[row['utf8_byte_start']:row['utf8_byte_end_exclusive']].decode().startswith(str(row['printed_line'])+' DEF'))
        self.assertEqual(corrections['listing_index'][1]['utf8_byte_start'], len(original['opening']['listing.txt']))
        for row in corrections['unresolved_graphics']:
            self.assertTrue((self.output/row['scan']['path']).is_file())
            self.assertIsNone(row['encoded_bytes'])
        with zipfile.ZipFile(self.output/'raw-ocr.zip') as archive:
            self.assertEqual(archive.read('segments/continuation/ocr/raw.settings.json'), original['continuation']['ocr/raw.settings.json'])
            self.assertIn('segments/continuation/map.json', archive.namelist())
        repeat = self.root/'build/repeat'
        self.run_assembly(repeat)
        files = lambda d:{p.relative_to(d).as_posix():p.read_bytes() for p in d.rglob('*') if p.is_file()}
        self.assertEqual(files(self.output),files(repeat))
        with self.assertRaisesRegex(ValueError, 'fresh assembly'):
            self.run_assembly()

    def test_bad_coverage_overlap_and_note_disposition_fail_before_publication(self):
        original = deepcopy(self.recipe)
        variants = [dict(expected_pdf_pages=[1,2,3]), dict(segments=list(reversed(original['segments']))),
                    dict(segments=[original['segments'][0], {**original['segments'][0], 'name':'duplicate'}], resolved_notes=[]),
                    dict(resolved_notes=[dict(segment='opening',note='Not an existing note.',reason='Unsupported')])]
        for change in variants:
            self.recipe = {**deepcopy(original), **change}
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.run_assembly()
            self.assertFalse(self.output.exists())

    def test_segment_identity_duplicates_and_index_errors_are_rejected(self):
        segments = [read_segment(self.root/'build'/s['name'], s['manifest']) for s in self.recipe['segments']]
        for change in ('identity','block','region','range','definition','marker'):
            changed = deepcopy(segments)
            package, corrections = changed[1]
            if change=='identity':package['toc_entry_id']='maso-1983-11-toc-9999'
            if change=='block':
                package['blocks'][0]['id']='block0'
                package['content_order'][1]['id']='block0'
                corrections['listing_index'][0]['block_id']='block0'
            if change=='region':package['regions'][0]['id']='code0'
            if change=='range':corrections['listing_index'][0]['utf8_byte_end_exclusive']-=1
            if change=='definition':corrections['glyph_definitions'][0]['utf8_byte_start']+=1
            if change=='marker':corrections['unresolved_graphics'][0]['marker']='⟦G999⟧'
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe,changed)

    def test_rehashed_ocr_map_mismatch_is_rejected(self):
        folder = self.root/'build/continuation'
        settings = json.loads((folder/'ocr/raw.settings.json').read_bytes())
        settings['package']['sha256']='0'*64
        write_json(folder/'ocr/raw.settings.json',settings)
        package = json.loads((folder/'article.json').read_bytes())
        package['raw_ocr'][0]['settings']=pin(folder,'ocr/raw.settings.json')
        write_json(folder/'article.json',package)
        self.rehash(folder)
        with self.assertRaisesRegex(ValueError,'OCR provenance'):
            self.run_assembly()
        self.assertFalse(self.output.exists())

    def test_raw_tampering_unreviewed_and_unsafe_names_fail_closed(self):
        self.recipe['segments'][0]['name']='../escape'
        with self.assertRaisesRegex(ValueError,'segment name'):
            self.run_assembly()
        self.recipe['segments'][0]['name']='opening'
        folder = self.root/'build/opening'
        package = json.loads((folder/'article.json').read_bytes())
        package['verification']['status']='unreviewed'
        write_json(folder/'article.json',package)
        self.rehash(folder)
        with self.assertRaisesRegex(ValueError,'reviewed segments'):
            self.run_assembly()
        (folder/'ocr/raw.txt').write_text('changed')
        with self.assertRaisesRegex(ValueError,'hash/size'):
            self.run_assembly()
        self.assertFalse(self.output.exists())

    def test_checker_rejects_rehashed_projection_index_and_preview_changes(self):
        self.run_assembly()
        originals = {name:(self.output/name).read_bytes() for name in ('article.json','corrections.json','index.html','manifest.json')}
        for target in ('text','offset','preview'):
            for name,value in originals.items():(self.output/name).write_bytes(value)
            package = json.loads(originals['article.json'])
            if target=='text':
                package['blocks'][0]['text']='Altered reading text'
                write_json(self.output/'article.json',package)
            elif target=='offset':
                correction = json.loads(originals['corrections.json'])
                correction['glyph_definitions'][1]['utf8_byte_start']-=1
                write_json(self.output/'corrections.json',correction)
                package['corrections']=[pin(self.output,'corrections.json')]
                write_json(self.output/'article.json',package)
            else:
                (self.output/'index.html').write_bytes(originals['index.html'].replace('한글'.encode(),b'changed'))
            self.rehash(self.output)
            with self.subTest(target=target),self.assertRaisesRegex(ValueError,'Assembly .* differs'):
                check_export(self.output)


if __name__ == '__main__':
    unittest.main()
