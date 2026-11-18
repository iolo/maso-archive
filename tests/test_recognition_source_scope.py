"""Complete JPEG exports retain exact, disjoint original recognition maps."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from tests import test_image_source
from tools.pdf_restore.assemble import read_segment
from tools.pdf_restore.build import build, validate_recognition_map
from tools.pdf_restore.inventory import pin, write_json


class RecognitionSourceScopeTests(unittest.TestCase):
    def fixture(self, root):
        recipe_path = test_image_source.ImageSourceTests().fixture(root)
        base = recipe_path.parent
        recipe = json.loads(recipe_path.read_bytes())
        template = json.loads((base / 'map.json').read_bytes())
        page = deepcopy(template['pages'][0])
        shutil.copyfile(root / 'source.jpg', root / 'second.jpg')
        page.update(source_index=11, reading_order=4, source_filename_number=30,
                    image=pin(root, 'second.jpg'))
        pages = [template['pages'][0], page]
        source_set = json.loads((root / 'source-set.json').read_bytes())
        source_set['pages'] = pages
        write_json(root / 'source-set.json', source_set)
        template['source'].update(pin(root, 'source-set.json'))
        inventory = root / 'private/pdf-restoration/inventory'
        write_json(inventory / 'sources.json', {'sources': [dict(template['source'],
                   scope='toc-entries-and-cover', pages=pages)]})
        recipe['inventory']['sources'] = pin(root, 'private/pdf-restoration/inventory/sources.json')
        combined = deepcopy(template)
        for key in ('pages', 'regions', 'excluded_regions'):
            combined[key] = []
        records, blocks, bundles, figures, order, originals = [], [], [], [], [], []
        old_records = json.loads((base / 'corrections.json').read_bytes())['records']
        for i, page in enumerate(pages):
            mapped = deepcopy(template)
            mapped['pages'] = [page]
            prefix, directory = f'p{i}-', f'ocr-{i}'
            for row in mapped['regions'] + mapped['excluded_regions']:
                row.update(id=prefix + row['id'], source_index=page['source_index'])
            mapped['mapping']['evidence'] = [f'Original segment {i}']
            name = f'original-{i}.json'
            write_json(base / name, mapped)
            recognition = pin(base, name)
            originals.append(mapped)
            evidence = json.loads((base / 'ocr/evidence.json').read_bytes())
            evidence.update(source_index=page['source_index'], image=page['image'],
                            source_sha256=mapped['source']['sha256'])
            evidence['images'], evidence['results'] = [], []
            folder = base / directory
            folder.mkdir()
            for original, region in zip(old_records, mapped['regions']):
                rid, old_id = region['id'], original['id']
                shutil.copyfile(base / 'ocr' / (old_id + '.png'), folder / (rid + '.png'))
                evidence['images'].append(pin(folder, rid + '.png'))
                raw = None
                if region['kind'] != 'figure':
                    for suffix in ('txt', 'tsv'):
                        shutil.copyfile(base / 'ocr' / (old_id + '.' + suffix), folder / (rid + '.' + suffix))
                    settings = json.loads((base / 'ocr' / (old_id + '.settings.json')).read_bytes())
                    settings.update(package={'sha256': recognition['sha256']}, region_ids=[rid],
                                    image=page['image'], source_index=page['source_index'],
                                    source_sha256=mapped['source']['sha256'])
                    write_json(folder / (rid + '.settings.json'), settings)
                    evidence['results'].append(dict(region_ids=[rid], **{k: pin(folder, rid + '.' + s)
                        for k, s in [('text', 'txt'), ('positions', 'tsv'), ('settings', 'settings.json')]}))
                    raw = pin(base, directory + '/' + rid + '.txt')
                    blocks.append(dict(id=rid, kind=region['kind'], text='한글 source ' + rid,
                        region_ids=[rid], correction_evidence=['corrections.json#' + rid], uncertainties=[]))
                    order.append(dict(type='block', id=rid))
                else:
                    figures.append(dict(id=rid, region_id=rid, region_ids=[rid], caption=None))
                    order.append(dict(type='figure', id=rid))
                records.append(dict(id=rid, scan=pin(base, directory + '/' + rid + '.png'), raw_ocr=raw))
            write_json(folder / 'evidence.json', evidence)
            bundles.append(dict(directory=directory, manifest=pin(base, directory + '/evidence.json'),
                recognition_map=recognition, recognition_source_indices=[page['source_index']]))
            for key in ('pages', 'regions', 'excluded_regions'):
                combined[key].extend(mapped[key])
        combined['mapping']['evidence'] = ['Complete article assembled from both unchanged maps']
        write_json(base / 'combined.json', combined)
        write_json(base / 'combined-corrections.json', dict(article_id=combined['id'],
            map=pin(base, 'combined.json'), records=records, blocks=blocks))
        recipe.update(map=pin(base, 'combined.json'), corrections=pin(base, 'combined-corrections.json'),
                      ocr_bundles=bundles, figures=figures, content_order=order)
        recipe['verification']['reviewed_region_ids'] = [r['id'] for r in combined['regions']]
        write_json(recipe_path, recipe)
        return recipe_path, originals, combined

    def test_two_exports_preserve_original_recognition_and_validate_for_later_assembly(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path, originals, combined = self.fixture(root)
            before = {p.relative_to(path.parent): p.read_bytes() for p in path.parent.rglob('*') if p.is_file()}
            outputs = [root / 'work' / n for n in ('one', 'two')]
            with patch('tools.pdf_restore.ocr.run_region', side_effect=AssertionError('No OCR')):
                for output in outputs:
                    package = build(path, output, root)
                    self.assertEqual(read_segment(output, pin(output, 'manifest.json'))[0], package)
                    self.assertEqual(len(package['raw_ocr']), 4)
                    for i in range(2):
                        self.assertEqual((output / f'ocr-{i}/recognition-map.json').read_bytes(),
                                         (path.parent / f'original-{i}.json').read_bytes())
            files = lambda d: {p.relative_to(d): p.read_bytes() for p in d.rglob('*') if p.is_file()}
            self.assertEqual(files(outputs[0]), files(outputs[1]))
            self.assertEqual(files(path.parent), before)

    def test_scope_cannot_hide_changed_source_regions_exclusions_or_identity(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, originals, current = self.fixture(Path(temporary))
            original = originals[0]
            scope = dict(region_ids={'p0-r1'}, recognition_source_indices=[7])
            validate_recognition_map(original, current, **scope)
            for fault in ('crop', 'unselected crop', 'figure crop', 'exclusion', 'page', 'source', 'title', 'region note'):
                bad = deepcopy(current)
                if fault in ('crop', 'unselected crop', 'figure crop'):
                    bad['regions'][{'crop': 0, 'unselected crop': 2, 'figure crop': 1}[fault]]['bbox'][2] -= .01
                elif fault == 'exclusion': bad['excluded_regions'][0]['bbox'][1] += .01
                elif fault == 'page': bad['pages'][0]['printed_page'] = 'changed'
                elif fault == 'source': bad['source']['sha256'] = '0' * 64
                elif fault == 'title': bad['title'] = 'changed'
                else: bad['regions'][0]['notes'] = 'changed'
                with self.subTest(fault=fault), self.assertRaises(ValueError):
                    validate_recognition_map(original, bad, **scope)
            for indices in ([], [7, 7], [True], [11], [7, 11]):
                with self.subTest(indices=indices), self.assertRaises(ValueError):
                    validate_recognition_map(original, current, region_ids={'p0-r1'}, recognition_source_indices=indices)
            with self.assertRaises(ValueError):
                validate_recognition_map(original, current, **scope, added_figure_regions=['p1-r2'])

    def test_scope_requires_pinned_original_map_and_unchanged_settings(self):
        for fault in ('missing map', 'rebound settings'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                path, _, _ = self.fixture(root)
                recipe = json.loads(path.read_bytes())
                if fault == 'missing map':
                    del recipe['ocr_bundles'][0]['recognition_map']
                else:
                    folder = path.parent / 'ocr-0'
                    settings = json.loads((folder / 'p0-r1.settings.json').read_bytes())
                    settings['package']['sha256'] = recipe['map']['sha256']
                    write_json(folder / 'p0-r1.settings.json', settings)
                    evidence = json.loads((folder / 'evidence.json').read_bytes())
                    evidence['results'][0]['settings'] = pin(folder, 'p0-r1.settings.json')
                    write_json(folder / 'evidence.json', evidence)
                    recipe['ocr_bundles'][0]['manifest'] = pin(path.parent, 'ocr-0/evidence.json')
                write_json(path, recipe)
                with self.assertRaises(ValueError):
                    build(path, root / 'work/rejected', root)


if __name__ == '__main__':
    unittest.main()
