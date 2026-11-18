"""Figure crop review can reuse pinned OCR without rebinding its settings."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

from tools.pdf_restore.build import build, check_export, validate_recognition_map
from tools.pdf_restore.assemble import read_segment
from tools.pdf_restore.inventory import pin, write_json
from tools.pdf_restore.ocr import page_ocr, pixel_box
from tests import test_image_source, test_pdf_build


class RecognitionMapTests(unittest.TestCase):
    def added_figure_fixture(self, root, jpeg):
        fixture = test_image_source.ImageSourceTests() if jpeg else test_pdf_build.PDFBuildTests()
        path = fixture.fixture(root)
        base = path.parent
        recipe = json.loads(path.read_bytes())
        original = (base / 'map.json').read_bytes()
        (base / 'recognition-map.json').write_bytes(original)
        current = json.loads(original)
        region = dict(current['regions'][1], id='r4', bbox=[.05, .39, .95, .59],
                      notes='Additional original listing-frame context; no new recognition.')
        current['regions'].append(region)
        write_json(base / 'map.json', current)
        recipe['map'] = pin(base, 'map.json')
        recipe['ocr_bundles'][0].update(region_ids=['r1', 'r2', 'r3'],
            recognition_map=pin(base, 'recognition-map.json'), added_figure_regions=['r4'])
        assets = base / 'frame-assets'
        assets.mkdir()
        if jpeg:
            with Image.open(root / current['pages'][0]['image']['path']) as image:
                image.crop(pixel_box(region['bbox'], image.size)).save(assets / 'r4.png')
        else:
            Image.new('RGB', (30, 12), 'green').save(assets / 'r4.png')
        evidence = json.loads((base / 'ocr/evidence.json').read_bytes())
        evidence.update(results=[], images=[pin(assets, 'r4.png')])
        write_json(assets / 'evidence.json', evidence)
        recipe['ocr_bundles'].append(dict(directory='frame-assets', region_ids=['r4'],
            manifest=pin(base, 'frame-assets/evidence.json')))
        corrections = json.loads((base / 'corrections.json').read_bytes())
        corrections['map'] = recipe['map']
        corrections['records'].append(dict(id='r4', scan=pin(base, 'frame-assets/r4.png'), raw_ocr=None))
        write_json(base / 'corrections.json', corrections)
        recipe['corrections'] = pin(base, 'corrections.json')
        recipe['figures'].append(dict(id='frame', region_id='r4', region_ids=['r4'], caption=None))
        recipe['content_order'].append(dict(type='figure', id='frame'))
        recipe['verification']['reviewed_region_ids'].append('r4')
        write_json(path, recipe)
        return path

    def test_added_original_figures_rebuild_without_changing_recognition(self):
        for jpeg in (False, True):
            with self.subTest(jpeg=jpeg), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                path = self.added_figure_fixture(root, jpeg)
                base = path.parent
                old_evidence = (base / 'ocr/evidence.json').read_bytes()
                old_files = {p.name: p.read_bytes() for p in (base / 'ocr').iterdir() if p.is_file()}
                outputs = [root / 'work' / name for name in ('one', 'two')]
                with patch('tools.pdf_restore.ocr.run_region', side_effect=AssertionError('No recognition')):
                    for output in outputs:
                        package = build(path, output, root)
                        self.assertEqual(check_export(output), package)
                        self.assertEqual(read_segment(output, pin(output, 'manifest.json'))[0], package)
                        self.assertEqual(len(package['raw_ocr']), 2)
                        self.assertEqual(len(package['region_assets']), 4)
                        self.assertEqual(len(package['figures']), 2)
                        for name, data in old_files.items():
                            if name not in ('evidence.json', 'page.png'):
                                self.assertEqual((output / 'ocr' / name).read_bytes(), data)
                        self.assertEqual((output / 'frame-assets/r4.png').read_bytes(),
                                         (base / 'frame-assets/r4.png').read_bytes())
                        self.assertEqual((output / 'ocr/recognition-map.json').read_bytes(),
                                         (base / 'recognition-map.json').read_bytes())
                self.assertEqual((base / 'ocr/evidence.json').read_bytes(), old_evidence)
                files = lambda folder: {p.relative_to(folder).as_posix(): p.read_bytes()
                                        for p in folder.rglob('*') if p.is_file()}
                self.assertEqual(files(outputs[0]), files(outputs[1]))

    def test_added_figure_declarations_keep_all_original_map_gates(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = self.added_figure_fixture(Path(temporary), True)
            original = json.loads((path.parent / 'recognition-map.json').read_bytes())
            current = json.loads((path.parent / 'map.json').read_bytes())
            before, after = copy.deepcopy(original), copy.deepcopy(current)
            validate_recognition_map(original, current, region_ids={'r1', 'r2', 'r3'},
                                     added_figure_regions=['r4'])
            self.assertEqual(original, before)
            self.assertEqual(current, after)
            for additions in (None, [], ['r4', 'r4'], ['unknown'], ['r2'], 'r4', [4], [['r4']]):
                with self.subTest(additions=additions), self.assertRaises(ValueError):
                    validate_recognition_map(original, current, region_ids={'r1', 'r2', 'r3'},
                                             added_figure_regions=additions)
            for scope in (None, {'r1', 'r2', 'r3', 'r4'}):
                with self.subTest(scope=scope), self.assertRaises(ValueError):
                    validate_recognition_map(original, current, region_ids=scope, added_figure_regions=['r4'])
            mutations = {
                'new text region': lambda p: p['regions'][-1].update(kind='prose'),
                'undeclared extra figure': lambda p: p['regions'].append(dict(p['regions'][-1], id='r5')),
                'changed selected bounds': lambda p: p['regions'][0].update(bbox=[.01, 0, .5, .4]),
                'changed original note': lambda p: p['regions'][1].update(notes='changed'),
                'removed original figure': lambda p: p['regions'].pop(1),
                'reordered original regions': lambda p: p['regions'].reverse(),
                'changed source': lambda p: p['source'].update(sha256='0' * 64),
                'changed page': lambda p: p['pages'][0].update(printed_page='different'),
                'changed exclusion': lambda p: p['excluded_regions'][0].update(bbox=[0, .61, 1, 1]),
            }
            for name, mutate in mutations.items():
                bad = copy.deepcopy(current)
                mutate(bad)
                with self.subTest(name=name), self.assertRaises(ValueError):
                    validate_recognition_map(original, bad, region_ids={'r1', 'r2', 'r3'},
                                             added_figure_regions=['r4'])

    def test_added_figure_bundle_requires_explicit_old_map_scope_and_asset_review(self):
        for fault in ('no original map', 'no scope', 'no declaration', 'no asset', 'no review', 'wrong asset pin'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                path = self.added_figure_fixture(root, True)
                base = path.parent
                recipe = json.loads(path.read_bytes())
                if fault == 'no original map':
                    del recipe['ocr_bundles'][0]['recognition_map']
                elif fault == 'no scope':
                    del recipe['ocr_bundles'][0]['region_ids']
                elif fault == 'no declaration':
                    del recipe['ocr_bundles'][0]['added_figure_regions']
                elif fault == 'no asset':
                    recipe['ocr_bundles'].pop()
                elif fault == 'no review':
                    corrections = json.loads((base / 'corrections.json').read_bytes())
                    corrections['records'].pop()
                    write_json(base / 'corrections.json', corrections)
                    recipe['corrections'] = pin(base, 'corrections.json')
                else:
                    (base / 'frame-assets/r4.png').write_bytes(b'changed')
                write_json(path, recipe)
                output = root / 'work/rejected'
                with self.assertRaises(ValueError):
                    build(path, output, root)
                self.assertFalse(output.exists())

    def test_targeted_recognition_calls_engine_only_for_selected_region(self):
        for jpeg in (False, True):
            with self.subTest(jpeg=jpeg), tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary)
                fixture=test_image_source.ImageSourceTests() if jpeg else test_pdf_build.PDFBuildTests()
                path=fixture.fixture(root);map_path=path.parent/'map.json'
                calls=[]
                def render(args,**kwargs):Image.new('RGB',(120,80),'blue').save(args[-1]+'.png')
                def engine(image,destination,config,runtime):
                    calls.append(config['region_ids'])
                    destination.with_suffix('.txt').write_text('targeted raw\n')
                    destination.with_suffix('.tsv').write_text('targeted positions\n')
                    return .1
                with patch('tools.pdf_restore.ocr.ROOT',root), patch('tools.pdf_restore.ocr.verify_runtime'), \
                     patch('tools.pdf_restore.ocr.subprocess.run',side_effect=render), \
                     patch('tools.pdf_restore.ocr.run_region',side_effect=engine):
                    selection=dict(source_index=7) if jpeg else {}
                    rows=page_ocr(map_path,None if jpeg else 1,root/'work/targeted',mode='regions',
                        runtime=root/'private/pdf-restoration/ocr-runtime',region_ids=['r3'],**selection)
                    self.assertEqual(calls,[['r3']]);self.assertEqual(len(rows),1)
                    self.assertTrue((root/'work/targeted/r3.png').exists())
                    self.assertFalse((root/'work/targeted/r1.png').exists())
                    for scope in [[],['r3','r3'],['unknown'],'r3']:
                        with self.subTest(scope=scope), self.assertRaises(ValueError):
                            page_ocr(map_path,None if jpeg else 1,root/'work/invalid',mode='regions',
                                runtime=root/'private/pdf-restoration/ocr-runtime',region_ids=scope,**selection)
                        self.assertFalse((root/'work/invalid').exists())

    def test_targeted_text_repair_reuses_unchanged_pdf_and_jpeg_regions(self):
        for jpeg, revised_note in ((False,False),(True,False),(False,True),(True,True)):
            with self.subTest(jpeg=jpeg,revised_note=revised_note), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                fixture = test_image_source.ImageSourceTests() if jpeg else test_pdf_build.PDFBuildTests()
                path = fixture.fixture(root); base = path.parent
                recipe = json.loads(path.read_bytes())
                original = (base / 'map.json').read_bytes()
                (base / 'recognition-map.json').write_bytes(original)
                current = json.loads(original)
                current['regions'][2]['bbox'][1] = .39
                if revised_note:
                    current['regions'][2]['notes'] += ' Reviewed expanded crop.'
                write_json(base / 'map.json', current)
                recipe['map'] = pin(base, 'map.json')
                repair = base / 'repair'; repair.mkdir()
                for suffix in ('txt', 'tsv', 'settings.json'):
                    shutil.copy2(base / 'ocr' / ('r3.' + suffix), repair / ('r3.' + suffix))
                (repair / 'r3.txt').write_text('New crop recognition\n')
                settings = json.loads((repair / 'r3.settings.json').read_bytes())
                settings['package']['sha256'] = recipe['map']['sha256']
                write_json(repair / 'r3.settings.json', settings)
                Image.new('RGB', (20, 21), 'green').save(repair / 'r3.png')
                evidence = json.loads((base / 'ocr/evidence.json').read_bytes())
                evidence['results'] = [dict(region_ids=['r3'], **{key:pin(repair, name) for key,name in
                    [('text','r3.txt'),('positions','r3.tsv'),('settings','r3.settings.json')]})]
                evidence['images'] = [pin(repair, 'r3.png')]
                write_json(repair / 'evidence.json', evidence)
                recipe['ocr_bundles'][0].update(region_ids=['r1','r2'],
                    recognition_map=pin(base, 'recognition-map.json'))
                if revised_note:
                    recipe['ocr_bundles'][0]['unselected_note_revisions']=[dict(region_id='r3',
                        before=json.loads(original)['regions'][2]['notes'],after=current['regions'][2]['notes'],
                        reason='The separately recognized repaired region carries its reviewed crop annotation.')]
                recipe['ocr_bundles'].append(dict(directory='repair', region_ids=['r3'],
                    manifest=pin(base, 'repair/evidence.json')))
                corrections = json.loads((base / 'corrections.json').read_bytes())
                corrections['map'] = recipe['map']
                corrections['records'][2].update(scan=pin(base,'repair/r3.png'), raw_ocr=pin(base,'repair/r3.txt'))
                write_json(base / 'corrections.json', corrections)
                recipe['corrections'] = pin(base, 'corrections.json'); write_json(path, recipe)
                outputs = [root / 'work' / name for name in ('one','two')]
                for output in outputs:
                    package = build(path, output, root)
                    self.assertEqual(check_export(output), package)
                    # The immutable segment reader must accept the same scoped
                    # note dispositions as export, for both PDF and JPEG input.
                    self.assertEqual(read_segment(output, pin(output, 'manifest.json'))[0], package)
                    self.assertEqual(len(package['raw_ocr']), 2)
                    self.assertEqual(len(package['region_assets']), 3)
                    self.assertEqual((output/'ocr/r1.settings.json').read_bytes(),
                                     (base/'ocr/r1.settings.json').read_bytes())
                    self.assertEqual((output/'repair/r3.settings.json').read_bytes(),
                                     (repair/'r3.settings.json').read_bytes())
                    self.assertFalse((output/'ocr/r3.png').exists())
                files = lambda folder: {p.relative_to(folder).as_posix():p.read_bytes()
                                       for p in folder.rglob('*') if p.is_file()}
                self.assertEqual(files(outputs[0]), files(outputs[1]))

    def test_scoped_reuse_still_rejects_selected_crop_metadata_and_invalid_scope(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = test_image_source.ImageSourceTests().fixture(Path(temporary))
            original = json.loads((path.parent/'map.json').read_bytes())
            current = copy.deepcopy(original); current['regions'][2]['bbox'][1] = .39
            validate_recognition_map(original,current,region_ids={'r1','r2'})
            for scope in [set(), {'unknown'}, {'r3'}]:
                with self.subTest(scope=scope), self.assertRaises(ValueError):
                    validate_recognition_map(original,current,region_ids=scope)
            for key,value in [('notes','different'),('kind','prose')]:
                bad = copy.deepcopy(current); bad['regions'][2][key] = value
                with self.subTest(key=key), self.assertRaises(ValueError):
                    validate_recognition_map(original,bad,region_ids={'r1','r2'})

    def test_unselected_note_dispositions_cannot_change_recognized_content_or_other_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=test_image_source.ImageSourceTests().fixture(Path(temporary))
            original=json.loads((path.parent/'map.json').read_bytes());current=copy.deepcopy(original)
            before=current['regions'][2]['notes'];current['regions'][2].update(notes=before+' Expanded crop reviewed.')
            revisions=[dict(region_id='r3',before=before,after=current['regions'][2]['notes'],reason='Separate crop repair.')]
            validate_recognition_map(original,current,region_ids={'r1','r2'},unselected_note_revisions=revisions)
            recipe=json.loads(path.read_bytes());recipe['ocr_bundles'][0]['unselected_note_revisions']=revisions
            write_json(path,recipe)
            with self.assertRaisesRegex(ValueError,'require an original recognition map'):
                build(path,Path(temporary)/'work/rejected-note',Path(temporary))
            for field,value in [('before','invented'),('after','invented'),('reason',''),('region_id','r1')]:
                changed=copy.deepcopy(revisions);changed[0][field]=value
                with self.subTest(field=field),self.assertRaises(ValueError):
                    validate_recognition_map(original,current,region_ids={'r1','r2'},unselected_note_revisions=changed)
            for scope,notes in [(None,revisions),({'r1','r2','r3'},revisions),({'r1','r2'},[]),({'r1','r2'},revisions*2)]:
                with self.subTest(scope=scope,notes=notes),self.assertRaises(ValueError):
                    validate_recognition_map(original,current,region_ids=scope,unselected_note_revisions=notes)
            for key,value in [('kind','code'),('bbox',[.1,.1,.2,.2])]:
                changed=copy.deepcopy(current);changed['regions'][0][key]=value
                with self.subTest(key=key),self.assertRaises(ValueError):
                    validate_recognition_map(original,changed,region_ids={'r1','r2'},unselected_note_revisions=revisions)

    def test_invalid_bundle_scopes_and_unknown_results_reject(self):
        for scope in [[],['r1','r1'],['unknown'],'r1']:
            with self.subTest(scope=scope), tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary); path=test_image_source.ImageSourceTests().fixture(root)
                recipe=json.loads(path.read_bytes());recipe['ocr_bundles'][0]['region_ids']=scope
                write_json(path,recipe)
                with self.assertRaises(ValueError):build(path,root/'work/rejected',root)
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);path=test_image_source.ImageSourceTests().fixture(root);base=path.parent
            evidence=json.loads((base/'ocr/evidence.json').read_bytes())
            evidence['results'][0]['region_ids']=['unknown'];write_json(base/'ocr/evidence.json',evidence)
            recipe=json.loads(path.read_bytes());recipe['ocr_bundles'][0]['manifest']=pin(base,'ocr/evidence.json')
            write_json(path,recipe)
            with self.assertRaises(ValueError):build(path,root/'work/rejected',root)

    def test_missing_and_overlapping_figure_asset_scopes_reject(self):
        for overlap in (False,True):
            with self.subTest(overlap=overlap), tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary);path=test_image_source.ImageSourceTests().fixture(root)
                recipe=json.loads(path.read_bytes());bundle=recipe['ocr_bundles'][0]
                bundle['region_ids']=['r1','r2','r3'] if overlap else ['r1','r3']
                if overlap:recipe['ocr_bundles'].append(dict(bundle,region_ids=['r2']))
                write_json(path,recipe)
                with self.assertRaisesRegex(ValueError,'exactly one scan asset'):
                    build(path,root/'work/rejected',root)

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
