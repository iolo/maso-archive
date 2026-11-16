"""Cover identity, source preservation, missing outcomes and portable rebuild gates."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from tools.pdf_restore.image_covers import build, check_export, inventory, read, validate, SCHEMA
from tools.pdf_restore.inventory import pin, write_json
from tools.pdf_restore.package import image_transform


class ImageCoversTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.inputs = self.root / 'inputs'
        self.inputs.mkdir()
        pages, faces = [], []
        for i, role in enumerate(('front', 'inside-front', 'inside-back', 'back')):
            image = self.inputs / (role + '.jpg')
            Image.new('RGB', (100, 140), (40 * i, 80, 90)).save(image)
            page = dict(source_index=i, image=pin(self.root, 'inputs/' + image.name),
                        width_px=100, height_px=140, reading_order=i+1)
            page['image_to_upright_normalized'] = image_transform(page)
            pages.append(page)
            faces.append(dict(role=role, source_index=i,
                material_kind='cover-artwork' if i == 0 else 'advertisement',
                role_basis='Synthetic reviewed collation and visible face labels.',
                condition=['Synthetic complete raster;no cosmetic changes.'],
                observations=[dict(id='label', kind='issue-label', text='84.11', bbox=[.1, .1, .3, .2],
                    candidates=['84.11'], qualifier='Synthetic label.', original_encoding_verified=False)],
                groups=[dict(id='labels', role='selected labels', member_observation_ids=['label'],
                             canonical_article_targets_inferred=False)],
                full_text_transcription=False, cosmetic_reconstruction_applied=False))
        write_json(self.inputs / 'source.json', dict(kind='jpeg-set', issue_id='maso-1984-11', pages=pages))
        self.review = dict(faces=faces, missing_faces=[], limitations=['Selected labels only;original raster retained.'])
        self.save_review()

    def save_review(self):
        write_json(self.inputs / 'review.json', self.review)
        source = dict(pin(self.root, 'inputs/source.json'), id='jpeg-1984-11', kind='jpeg-set')
        write_json(self.inputs / 'recipe.json', dict(issue_id='maso-1984-11', source=source,
                                                   review=pin(self.inputs, 'review.json')))

    def export(self, name='out'):
        output = self.root / name
        build(self.inputs / 'recipe.json', output, self.root)
        return output

    def reseal(self, output):
        manifest = read(output / 'manifest.json')
        manifest['files'] = inventory(output)
        write_json(output / 'manifest.json', manifest)

    def test_byte_exact_rebuild_and_no_global_cover_selection(self):
        sentinel = self.root / 'covers/8411.jpg'
        sentinel.parent.mkdir()
        sentinel.write_bytes(b'Existing global donation remains untouched')
        before = {p.name: p.read_bytes() for p in self.inputs.glob('*')}
        a, b = self.export('a'), self.export('b')
        files = sorted(p.relative_to(a) for p in a.rglob('*') if p.is_file())
        self.assertEqual(len(files), 11)
        for p in files:
            self.assertEqual((a / p).read_bytes(), (b / p).read_bytes())
        self.assertEqual(check_export(a)['availability'], 'complete')
        for role in ('front', 'inside-front', 'inside-back', 'back'):
            self.assertEqual((a / 'faces' / (role + '.jpg')).read_bytes(), (self.inputs / (role + '.jpg')).read_bytes())
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.inputs.glob('*')})
        self.assertEqual(sentinel.read_bytes(), b'Existing global donation remains untouched')
        self.assertFalse((a / 'index.html').exists())
        with self.assertRaises(ValueError):
            self.export('a')

    def test_partial_cover_set_requires_explicit_missing_outcome(self):
        self.review['faces'].pop()
        self.review['missing_faces'] = [dict(role='back', reason='Not supplied in synthetic fixture.')]
        self.save_review()
        self.assertEqual(check_export(self.export())['availability'], 'partial')
        self.review['missing_faces'] = []
        self.save_review()
        with self.assertRaises(ValueError):
            self.export('incomplete')
        self.assertFalse((self.root / 'incomplete').exists())

    def test_changed_source_and_review_pins_rejected(self):
        (self.inputs / 'front.jpg').write_bytes(b'changed')
        with self.assertRaises(ValueError):
            self.export('changed-source')
        self.assertFalse((self.root / 'changed-source').exists())
        self.review['limitations'].append('changed')
        write_json(self.inputs / 'review.json', self.review)
        with self.assertRaises(ValueError):
            self.export('changed-review')

    def test_duplicate_sources_roles_and_order_rejected(self):
        for mutation in ('role', 'source', 'order'):
            review = deepcopy(self.review)
            if mutation == 'role': review['faces'][1]['role'] = 'front'
            if mutation == 'source': review['faces'][1]['source_index'] = 0
            if mutation == 'order': review['faces'].reverse()
            write_json(self.inputs / 'review.json', review)
            recipe = read(self.inputs / 'recipe.json')
            recipe['review'] = pin(self.inputs, 'review.json')
            write_json(self.inputs / 'recipe.json', recipe)
            with self.assertRaises(ValueError):
                self.export(mutation)

    def test_annotation_bounds_and_dangling_group_rejected(self):
        out = self.export()
        package, source, review = read(out / 'cover-set.json'), read(out / 'source.json'), read(out / 'review.json')
        for mutation in ('bounds', 'group', 'candidate', 'transform'):
            p, r = deepcopy(package), deepcopy(review)
            if mutation == 'bounds': p['faces'][0]['observations'][0]['bbox'] = [.4, .1, .2, .2]
            if mutation == 'group': p['faces'][0]['groups'][0]['member_observation_ids'] = ['missing']
            if mutation == 'candidate': p['faces'][0]['observations'][0]['candidates'] = ['different']
            if mutation == 'transform': p['faces'][0]['source_page']['image_to_upright_normalized'][0] = 1
            r['faces'][0] = {k: v for k, v in p['faces'][0].items() if k not in ('asset', 'source_page')}
            with self.assertRaises(ValueError):
                validate(p, source, r, read(SCHEMA))

    def test_changed_assets_and_extra_files_rejected_after_manifest_reseal(self):
        out = self.export()
        (out / 'faces/front.jpg').write_bytes((out / 'faces/back.jpg').read_bytes())
        self.reseal(out)
        with self.assertRaises(ValueError):
            check_export(out)
        good = self.export('good')
        (good / 'unreferenced.jpg').write_bytes(b'extra')
        self.reseal(good)
        with self.assertRaises(ValueError):
            check_export(good)

    def test_unsafe_source_paths_rejected(self):
        recipe = read(self.inputs / 'recipe.json')
        recipe['source']['path'] = '../outside.json'
        write_json(self.inputs / 'recipe.json', recipe)
        with self.assertRaises(ValueError):
            self.export()
        self.assertFalse((self.root / 'out').exists())


if __name__ == '__main__':
    unittest.main()
