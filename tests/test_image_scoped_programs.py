"""Explicit native program continuity, preservation and offline tamper rejection."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_image_scoped_native as native_base
from tools.pdf_restore.assemble import assemble, project, read_segment
from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.inventory import pin, write_json


class ScopedProgramTests(unittest.TestCase):
    def fixture(self, root):
        path = native_base.ScopedNativeTests().fixture(root)
        recipe = json.loads(path.read_bytes())
        specs = []
        for name in ('a', 'b'):
            folder = root / 'archive/inputs' / name
            c = json.loads((folder / 'native-corrections.json').read_bytes())
            r = json.loads((folder / 'native-recipe.json').read_bytes())
            group = c['listing_groups'][0]
            group.update(complete_in_segment=True, complete_program=False, physical_rows=1,
                         logical_units=1, original_encoded_bytes_verified=False, source_version='synthetic')
            if name == 'a':
                c['segment']['outgoing_program'] = dict(listing_id='code', last_printed_line=10,
                    next_folio='L', next_printed_line=20, source_unit_complete=True)
            else:
                def replace(value):
                    if isinstance(value, dict):
                        return {k: replace(v) for k, v in value.items()}
                    if isinstance(value, list):
                        return [replace(v) for v in value]
                    return '20 PRINT "한글"\n' if value == '10 PRINT "한글"\n' else value
                c = replace(c)
                for field in ('listing_line_index', 'logical_listing_line_index'):
                    c[field][0]['printed_line'] = 20
                c['segment'].update(incoming_program=dict(listing_id='code', previous_folio='K',
                    last_printed_line=10, next_printed_line=20, source_unit_complete=True),
                    final_program=dict(listing_id='code', last_printed_line=20, source_unit_complete=True))
            write_json(folder / 'program-corrections.json', c)
            r['corrections'] = pin(folder, 'program-corrections.json')
            write_json(folder / 'program-recipe.json', r)
            output = root / 'archive/program-segments' / name
            build(folder / 'program-recipe.json', output, root)
            specs.append(dict(name=name, manifest=pin(root, output.relative_to(root).as_posix() + '/manifest.json')))
        recipe['segments'] = specs
        recipe['program_links'] = [dict(left=dict(segment='a', listing_id='code', last_printed_line=10),
            right=dict(segment='b', listing_id='code', first_printed_line=20),
            source_unit_complete=True, evidence='Synthetic adjacent complete source units.')]
        write_json(path, recipe)
        return path

    def load(self, root, path):
        recipe = json.loads(path.read_bytes())
        return recipe, [read_segment((root / s['manifest']['path']).parent, s['manifest'])
                        for s in recipe['segments']]

    def test_joined_program_rebuild_preserves_native_fragments_and_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); path = self.fixture(root)
            recipe, sources = self.load(root, path); original = deepcopy(sources)
            outputs = [root / 'work/one', root / 'work/two']
            for out in outputs:
                package = assemble(path, out, root)
                self.assertEqual(package, check_export(out))
                c = json.loads((out / 'corrections.json').read_bytes())
                self.assertEqual(len(c['programs']), 1)
                program = c['programs'][0]
                self.assertEqual(program['block_ids'], ['a-code', 'b-code'])
                self.assertEqual((program['physical_rows'], program['logical_units']), (2, 2))
                self.assertEqual(program['continuations'], recipe['program_links'])
                self.assertEqual([(v['scope'], v['value']) for v in c['native_indexes']['listing_groups']],
                                 [(s['name'], original[i][1]['listing_groups'][0]) for i, s in enumerate(recipe['segments'])])
                data = (out / 'listing.txt').read_bytes()
                for f in program['source_fragments']:
                    source = root / 'archive/program-segments' / f['scope']
                    self.assertEqual(data[f['start_byte']:f['end_byte']], (source / 'listing.txt').read_bytes())
                self.assertFalse(program['execute_verified'])
            files = lambda p: {f.relative_to(p).as_posix(): f.read_bytes() for f in p.rglob('*') if f.is_file()}
            self.assertEqual(files(outputs[0]), files(outputs[1]))
            self.assertEqual(sources, original)

    def test_missing_links_wrong_versions_boundaries_and_endings_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); r, s = self.load(root, self.fixture(root))
            cases = {
                'missing declared join': lambda r, s: r['program_links'].clear(),
                'duplicate join': lambda r, s: r['program_links'].append(deepcopy(r['program_links'][0])),
                'missing source evidence': lambda r, s: r['program_links'][0].update(evidence=''),
                'split source unit': lambda r, s: r['program_links'][0].update(source_unit_complete=False),
                'wrong incoming number': lambda r, s: r['program_links'][0]['right'].update(first_printed_line=30),
                'wrong listing': lambda r, s: r['program_links'][0]['right'].update(listing_id='other'),
                'reversed segments': lambda r, s: r['program_links'][0]['right'].update(segment='a'),
                'different version': lambda r, s: s[1][1]['listing_groups'][0].update(source_version='other'),
                'wrong original outgoing': lambda r, s: s[0][1]['segment']['outgoing_program'].update(next_printed_line=30),
                'wrong original incoming folio': lambda r, s: s[1][1]['segment']['incoming_program'].update(previous_folio='X'),
                'lost original incoming': lambda r, s: s[1][1]['segment'].pop('incoming_program'),
                'missing final source ending': lambda r, s: s[1][1]['segment'].pop('final_program'),
                'wrong final source unit': lambda r, s: s[1][1]['segment']['final_program'].update(last_printed_line=30),
                'wrong fragment count': lambda r, s: s[0][1]['listing_groups'][0].update(physical_rows=2),
                'premature whole fragment': lambda r, s: s[1][1]['listing_groups'][0].update(complete_program=True),
                'invented original bytes': lambda r, s: s[1][1]['listing_groups'][0].update(original_encoded_bytes_verified=True),
            }
            for name, change in cases.items():
                recipe, sources = deepcopy(r), deepcopy(s); change(recipe, sources)
                with self.subTest(case=name), self.assertRaises(ValueError):
                    project(recipe, sources)

    def test_unlinked_complete_versions_stay_independent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); r, s = self.load(root, self.fixture(root))
            r['program_links'] = []
            for _, c in s:
                c['listing_groups'][0]['complete_program'] = True
                for key in ('incoming_program', 'outgoing_program', 'final_program'):
                    c['segment'].pop(key, None)
            _, correction = project(r, s)
            self.assertEqual([p['program_id'] for p in correction['programs']], ['a-code', 'b-code'])
            self.assertTrue(all(not p['continuations'] for p in correction['programs']))

    def test_rehashed_program_projection_tampering_rejects(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); path = self.fixture(root); out = root / 'work/export'
            assemble(path, out, root)
            c = json.loads((out / 'corrections.json').read_bytes())
            c['programs'][0]['source_fragments'][1]['start_byte'] += 1
            write_json(out / 'corrections.json', c)
            p = json.loads((out / 'article.json').read_bytes()); p['corrections'] = [pin(out, 'corrections.json')]
            write_json(out / 'article.json', p)
            m = json.loads((out / 'manifest.json').read_bytes()); m['files'] = [pin(out, f['path']) for f in m['files']]
            write_json(out / 'manifest.json', m)
            with self.assertRaisesRegex(ValueError, 'correction projection'):
                check_export(out)


if __name__ == '__main__':
    unittest.main()
