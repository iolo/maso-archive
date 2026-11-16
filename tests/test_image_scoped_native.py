"""Lossless native index scopes, typed bindings and offline assembly checks."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_image_assemble as base
from tools.pdf_restore.assemble import assemble, project, read_segment, text_bytes
from tools.pdf_restore.assembly_indexes import block_ranges
from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.inventory import pin, write_json

S, E = 'utf8_byte_start', 'utf8_byte_end_exclusive'


class ScopedNativeTests(unittest.TestCase):
    def fixture(self, root):
        path = base.ImageAssemblyTests().fixture(root)
        recipe = json.loads(path.read_bytes())
        recipe.update(index_mode='structured-programs-v1', source_index_mode='scoped-native-v1',
                      logical_aliases=[], paragraph_links=[])
        recipe.pop('relationship_links')
        specs = []
        for n in ('a', 'b'):
            folder = root / 'archive/inputs' / n
            c = json.loads((folder / 'corrections.json').read_bytes())
            r = json.loads((folder / 'recipe.json').read_bytes())
            for row in c['tables'][0]['rows']:
                for i, cell in enumerate(row['cells']):
                    cell['cell_id'] = f'table:r0:c{i}'
            c['formula_occurrence_index'] = []
            body = next(b for b in c['blocks'] if b['id'] == 'body')
            p = dict(kind='source-paragraph', paragraph_id='body:p1', block_id='body',
                     literal=body['text'], start_byte=0, end_byte=len(body['text'].encode()),
                     download='article.txt')
            ranges = block_ranges(dict(blocks=c['blocks'], content_order=r['content_order']))
            p.update({S: ranges['body'][0], E: ranges['body'][1]})
            c['content_associations'] = [p]
            c['figure_label_index'][0]['figure_id'] = 'figure'
            c['figure_structures'] = [dict(figure_id='figure', region_id='figure-region',
                kind='source-flow-graph', nodes=[dict(node_id='ret', label_id='figure:l1')],
                edges=[dict(edge_id='edge', from_node='ret', to_node='ret', branch_label_id=None)],
                inspection_transform=dict(clockwise_degrees=90,
                    inspection_normalized_to_source_normalized=[0, -1, 1, 0, 0, 1],
                    changes_source_raster=False))]
            c['source_byte_qualifications'] = [deepcopy(c['basic_source_fields'][0])]
            c['table_source_literals'] = []
            c['recognition_disagreements'] = [dict(physical_line_id='code:r1',
                region_id='code-region', scan=next(v['scan'] for v in c['records'] if v['id'] == 'code-region'),
                prior_pdf='different', disposition='Retained comparison.')]
            c['bibliography_entries'] = [deepcopy(p)]
            if n == 'a':
                c['logical_listing_line_index'][0]['source_unit_id'] = 'code:n10'
                c['logical_listing_line_index'][0].pop('line_id')
                recipe['logical_aliases'].append(dict(segment=n, index=0, source_unit_id='code:n10'))
            write_json(folder / 'native-corrections.json', c)
            r['corrections'] = pin(folder, 'native-corrections.json')
            write_json(folder / 'native-recipe.json', r)
            output = root / 'archive/native-segments' / n
            build(folder / 'native-recipe.json', output, root)
            specs.append(dict(name=n, manifest=pin(root, output.relative_to(root).as_posix() + '/manifest.json')))
        recipe['segments'] = specs
        write_json(path, recipe)
        return path

    def load(self, root, path):
        recipe = json.loads(path.read_bytes())
        segments = [read_segment((root / s['manifest']['path']).parent, s['manifest'])
                    for s in recipe['segments']]
        return recipe, segments

    def test_exact_rebuild_preserves_all_native_values_and_binds_downloads(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.fixture(root)
            recipe, segments = self.load(root, path)
            before = deepcopy(segments)
            outputs = [root / 'work/one', root / 'work/two']
            for output in outputs:
                package = assemble(path, output, root)
                self.assertEqual(check_export(output), package)
                c = json.loads((output / 'corrections.json').read_bytes())
                self.assertEqual(next(b['text'] for b in package['blocks'] if b['id'] == 'a-body'),
                                 'An opening split word follows.')
                for field, entries in c['native_indexes'].items():
                    expected = [(spec['name'], value) for spec, (_, source) in zip(recipe['segments'], segments)
                                for value in source.get(field, [])]
                    self.assertEqual([(v['scope'], v['value']) for v in entries], expected)
                    for entry in entries:
                        for span in entry['ranges']:
                            data = (output / span['download']).read_bytes()
                            self.assertEqual(data[span['start_byte']:span['end_byte']].decode(), span['literal'])
                graphs = c['native_indexes']['figure_structures']
                ids = [next(r['id'] for r in g['references'] if r['pointer'] == '/nodes/0/node_id') for g in graphs]
                self.assertNotEqual(ids[0], ids[1])
                self.assertIn('inspection_transform', graphs[0]['value'])
                self.assertNotIn('line_id', c['native_indexes']['logical_listing_line_index'][0]['value'])
                self.assertEqual(c['logical_aliases'], recipe['logical_aliases'])
                blocks = {b['id'] for b in package['blocks']}
                for scope in c['scopes']:
                    self.assertTrue(all(v['id'] in blocks for v in scope['identities'] if v['kind'] == 'block'))
            files = lambda folder: {p.relative_to(folder).as_posix(): p.read_bytes()
                                    for p in folder.rglob('*') if p.is_file()}
            self.assertEqual(files(outputs[0]), files(outputs[1]))
            self.assertEqual(segments, before)

    def test_bad_native_references_ranges_aliases_and_coverage_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            recipe, segments = self.load(root, self.fixture(root))
            cases = {
                'unknown index': lambda r, s: s[0][1].update(unhandled_native_data=[]),
                'unknown field': lambda r, s: s[0][1]['figure_structures'][0].update(unhandled_id='ret'),
                'dangling node': lambda r, s: s[0][1]['figure_structures'][0]['edges'][0].update(to_node='other'),
                'duplicate node': lambda r, s: s[0][1]['figure_structures'][0]['nodes'].append(dict(node_id='ret')),
                'missing alias': lambda r, s: r['logical_aliases'].clear(),
                'wrong alias': lambda r, s: r['logical_aliases'][0].update(source_unit_id='other'),
                'missing physical': lambda r, s: s[0][1]['logical_listing_line_index'][0].update(physical_line_ids=['absent']),
                'double physical': lambda r, s: s[0][1]['logical_listing_line_index'].append(deepcopy(s[0][1]['logical_listing_line_index'][0])),
                'unknown row': lambda r, s: s[0][1]['recognition_disagreements'][0].update(physical_line_id='absent'),
                'split UTF8': lambda r, s: s[0][1]['basic_source_fields'][0].update(utf8_byte_start=11),
                'outside owner': lambda r, s: s[0][1]['bibliography_entries'][0].update(utf8_byte_end_exclusive=999),
                'wrong source order': lambda r, s: r['expected_source_indices'].reverse(),
                'wrong join': lambda r, s: r['prose_joins'][0]['right'].update(opening='different'),
                'missing declared join': lambda r, s: r['prose_joins'].clear(),
                'wrong scan': lambda r, s: s[0][1]['recognition_disagreements'][0]['scan'].update(sha256='0' * 64),
                'wrong literal': lambda r, s: s[0][1]['basic_source_fields'][0].update(literal='다른'),
                'wrong cell': lambda r, s: s[0][1]['tables'][0]['rows'][0]['cells'][0].update(text='invented'),
                'invented execution': lambda r, s: s[0][1]['listing_groups'][0].update(execute_verified=True),
            }
            for name, change in cases.items():
                r, s = deepcopy(recipe), deepcopy(segments)
                change(r, s)
                with self.subTest(case=name), self.assertRaises(ValueError):
                    project(r, s)

    def test_repeated_nodes_are_scoped_by_figure_and_label_ownership_is_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            r, s = self.load(root, self.fixture(root))
            package, correction = s[1]
            figure = deepcopy(package['figures'][0])
            figure['id'] = 'other'
            package['figures'].append(figure)
            package['content_order'].append(dict(type='figure', id='other'))
            label = deepcopy(correction['figure_label_index'][0])
            label.update(label_id='other:l1', figure_id='other')
            correction['figure_label_index'].append(label)
            graph = deepcopy(correction['figure_structures'][0])
            graph.update(figure_id='other')
            graph['nodes'][0]['label_id'] = 'other:l1'
            correction['figure_structures'].append(graph)
            _, c = project(r, s)
            graphs = [v for v in c['native_indexes']['figure_structures'] if v['scope'] == 'b']
            ids = [next(v['id'] for v in g['references'] if v['pointer'] == '/nodes/0/node_id') for g in graphs]
            self.assertNotEqual(*ids)
            graph['nodes'][0]['label_id'] = 'figure:l1'
            with self.assertRaisesRegex(ValueError, 'another source figure'):
                project(r, s)

    def test_rehashed_native_binding_and_value_tampering_reject(self):
        for fault in ('binding', 'value'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                path = self.fixture(root)
                output = root / 'work/one'
                assemble(path, output, root)
                c = json.loads((output / 'corrections.json').read_bytes())
                entry = c['native_indexes']['figure_structures'][0]
                if fault == 'binding':
                    entry['references'][0]['id'] = 'invented'
                else:
                    entry['value']['nodes'][0]['node_id'] = 'invented'
                write_json(output / 'corrections.json', c)
                p = json.loads((output / 'article.json').read_bytes())
                p['corrections'] = [pin(output, 'corrections.json')]
                write_json(output / 'article.json', p)
                m = json.loads((output / 'manifest.json').read_bytes())
                m['files'] = [pin(output, v['path']) for v in m['files']]
                write_json(output / 'manifest.json', m)
                with self.assertRaisesRegex(ValueError, 'correction projection'):
                    check_export(output)


if __name__ == '__main__':
    unittest.main()
