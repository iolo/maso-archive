"""Typed literal observations, unchanged native scopes and declared prose boundaries."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from tests import test_image_scoped_native as native_tests
from tools.pdf_restore.assemble import assemble, project, read_segment
from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.inventory import pin, write_json


class ObservationAssemblyTests(unittest.TestCase):
    def figure_links_fixture(self, root):
        path, recipe, originals = self.fixture(root)
        recipe['prose_joins'] = []
        specs = []
        for i, (name, (_, original)) in enumerate(zip(('a', 'b'), originals)):
            folder = root / 'archive/inputs' / name
            c = deepcopy(original)
            r = json.loads((folder / 'observation-recipe.json').read_bytes())
            body = next(b for b in c['blocks'] if b['id'] == 'body')
            prior_text = body['text']
            caption = '그림1. Native target'
            literal = '그림 1'
            body['text'] += '\n' + caption + '\n' + literal
            next(v for v in c['records'] if v['id'] == 'body-region')['corrected_text'] = body['text']
            next(v for v in c['regional_text_ranges'] if v['region_id'] == 'body-region').update(
                text=body['text'], end_byte=len(body['text'].encode()))
            c['segment_continuations'] = []
            c['segment'] = {}
            start = len((prior_text + '\n' + caption + '\n').encode())
            occurrence = dict(block_id='body', literal=literal, start_byte=start,
                              end_byte=start + len(literal.encode()), printed_number='1')
            if i == 0:
                occurrence.update(kind='original-source-reference-to-deferred-figure',
                                  target_native_pending=True, target_actual_folio='L')
            else:
                occurrence.update(kind='original-source-reference-to-pinned-prior-figure',
                                  prior_native_manifest=specs[0]['manifest'], prior_figure_name='figure')
            c['source_literal_index'] = [occurrence]
            capstart = len((prior_text + '\n').encode())
            capocc = dict(block_id='body', literal=caption, start_byte=capstart,
                          end_byte=capstart + len(caption.encode()))
            c['source_caption_association_index'] = [dict(figure_id='figure',
                figure_region_id='figure-region', caption_occurrence=capocc)]
            if i:
                c['source_literal_index'].append(dict(capocc,
                    kind='original-located-target-for-prior-figure-reference',
                    prior_region_name='body-region', prior_native_manifest=specs[0]['manifest']))
            r['figures'][0]['caption'] = caption
            write_json(folder / 'figure-link-corrections.json', c)
            r['corrections'] = pin(folder, 'figure-link-corrections.json')
            write_json(folder / 'figure-link-recipe.json', r)
            output = root / 'archive/figure-link-segments' / name
            build(folder / 'figure-link-recipe.json', output, root)
            specs.append(dict(name=name, manifest=pin(root, str(output.relative_to(root) / 'manifest.json'))))
        recipe['segments'] = specs
        recipe['figure_reference_links'] = [dict(source=dict(segment=a, index=0, literal='그림 1'),
            target=dict(segment=b, figure_id='figure'), printed_number='1',
            evidence='Original source reference and numbered target caption were compared.')
            for a, b in [('a', 'b'), ('b', 'a')]]
        write_json(path, recipe)
        sources = [read_segment((root / s['manifest']['path']).parent, s['manifest']) for s in specs]
        return path, recipe, sources

    def test_figure_reference_links_rebuild_both_directions_without_prose_join(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path, recipe, sources = self.figure_links_fixture(root)
            before = deepcopy(sources)
            outputs = [root / 'work/one', root / 'work/two']
            for output in outputs:
                p = assemble(path, output, root)
                self.assertEqual(check_export(output), p)
                c = json.loads((output / 'corrections.json').read_bytes())
                self.assertFalse(c['resolved_continuations'])
                links = c['figure_reference_resolutions']
                self.assertEqual([v['target']['figure_id'] for v in links], ['b-figure', 'a-figure'])
                self.assertTrue(all(v['original_record_preserved'] for v in links))
                for link in links:
                    self.assertEqual(link['target']['caption_literal'], '그림1. Native target')
                    for span in link['source']['ranges']:
                        self.assertEqual((output / span['download']).read_bytes()[
                            span['start_byte']:span['end_byte']].decode(), span['literal'])
                for field, entries in c['native_indexes'].items():
                    self.assertEqual([(v['scope'], v['value']) for v in entries],
                        [(spec['name'], row) for spec, (_, original) in zip(recipe['segments'], sources)
                         for row in original.get(field, [])])
                locator = c['native_indexes']['source_literal_index'][-1]
                self.assertIn(dict(pointer='/prior_region_name', id='a-body-region'), locator['references'])
            files = lambda d: {p.relative_to(d).as_posix(): p.read_bytes()
                               for p in d.rglob('*') if p.is_file()}
            self.assertEqual(files(outputs[0]), files(outputs[1]))
            self.assertEqual(sources, before)

    def test_figure_reference_links_reject_missing_wrong_or_unpinned_targets(self):
        with tempfile.TemporaryDirectory() as temp:
            _, recipe, sources = self.figure_links_fixture(Path(temp))
            cases = {
                'legacy mode': lambda r, s: r.update(source_index_mode='scoped-native-v1'),
                'missing disposition': lambda r, s: r['figure_reference_links'].pop(),
                'duplicate source': lambda r, s: r['figure_reference_links'].append(deepcopy(r['figure_reference_links'][0])),
                'boolean index': lambda r, s: r['figure_reference_links'][0]['source'].update(index=True),
                'unknown occurrence': lambda r, s: r['figure_reference_links'][0]['source'].update(index=99),
                'same scope target': lambda r, s: r['figure_reference_links'][0]['target'].update(segment='a'),
                'unknown figure': lambda r, s: r['figure_reference_links'][0]['target'].update(figure_id='missing'),
                'wrong number': lambda r, s: r['figure_reference_links'][0].update(printed_number='2'),
                'wrong literal': lambda r, s: r['figure_reference_links'][0]['source'].update(literal='그림\n1'),
                'wrong caption': lambda r, s: s[1][0]['figures'][0].update(caption='그림2. Other'),
                'caption number prefix': lambda r, s: s[1][0]['figures'][0].update(caption='그림12. Other'),
                'missing caption association': lambda r, s: s[1][1]['source_caption_association_index'].clear(),
                'wrong deferred folio': lambda r, s: s[0][1]['source_literal_index'][0].update(target_actual_folio='K'),
                'wrong prior manifest': lambda r, s: s[1][1]['source_literal_index'][0]['prior_native_manifest'].update(sha256='0'*64),
                'wrong prior figure': lambda r, s: s[1][1]['source_literal_index'][0].update(prior_figure_name='other'),
                'unpinned prior locator': lambda r, s: s[1][1]['source_literal_index'][1].pop('prior_native_manifest'),
                'wrong prior locator region': lambda r, s: s[1][1]['source_literal_index'][1].update(prior_region_name='missing'),
            }
            for label, mutate in cases.items():
                r, s = deepcopy(recipe), deepcopy(sources)
                mutate(r, s)
                with self.subTest(case=label), self.assertRaises((ValueError, KeyError)):
                    project(r, s)

    def test_rehashed_figure_resolution_tampering_rejects(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path, _, _ = self.figure_links_fixture(root)
            output = root / 'work/one'
            assemble(path, output, root)
            c = json.loads((output / 'corrections.json').read_bytes())
            c['figure_reference_resolutions'][0]['target']['figure_id'] = 'a-figure'
            write_json(output / 'corrections.json', c)
            p = json.loads((output / 'article.json').read_bytes())
            p['corrections'] = [pin(output, 'corrections.json')]
            write_json(output / 'article.json', p)
            m = json.loads((output / 'manifest.json').read_bytes())
            m['files'] = [pin(output, row['path']) for row in m['files']]
            write_json(output / 'manifest.json', m)
            with self.assertRaisesRegex(ValueError, 'correction projection'):
                check_export(output)

    def test_each_byte_position_requires_one_matching_outline(self):
        from tools.pdf_restore.assembly_scoped_observations import validate_byte_strips
        ids = [f'b{i}' for i in range(1, 9)]
        value = dict(source_figure_structure_index=[dict(kind='source-signed-byte-strips',
            region_id='byte', rows=[dict(ordinal=1, bit_ids=ids, sign_bit_id=ids[0], lsb_bit_id=ids[-1])])],
            source_figure_bit_index=[dict(bit_id=id, region_id='byte', row=1, column=i,
                source_bbox_in_region=[(i-1)/8, 0, i/8, 1]) for i, id in enumerate(ids, 1)],
            source_figure_connector_index=[dict(kind='source-byte-cell-outline', region_id='byte',
                bit_id=id, source_path_in_region=[[(i-1)/8,0],[i/8,0],[i/8,1],[(i-1)/8,1],[(i-1)/8,0]])
                for i, id in enumerate(ids, 1)])
        validate_byte_strips(value)
        for fault in ('lost', 'duplicate', 'column', 'bounds', 'LSB'):
            c = deepcopy(value)
            if fault == 'lost':c['source_figure_connector_index'].pop()
            elif fault == 'duplicate':c['source_figure_connector_index'].append(deepcopy(c['source_figure_connector_index'][0]))
            elif fault == 'column':c['source_figure_bit_index'][-1]['column'] = 7
            elif fault == 'bounds':c['source_figure_connector_index'][-1]['source_path_in_region'][0][0] = 0
            else:c['source_figure_structure_index'][0]['rows'][0]['lsb_bit_id'] = ids[0]
            with self.subTest(fault=fault), self.assertRaises(ValueError):validate_byte_strips(c)

    def test_illustration_interruption_requires_exact_order_and_source_text_association(self):
        from tools.pdf_restore.assembly_scoped_observations import check_intervening
        items = [dict(segment='a', type='figure', id='picture'),
                 dict(segment='a', type='block', id='callout')]
        actual = [dict(type=v['type'], id='a-' + v['id']) for v in items]
        context = SimpleNamespace(name='a', blocks={'callout': dict(kind='prose', text='원문')},
            correction={'source_illustration_text_association_index': [
                dict(block_id='callout', figure_id='picture', literal='원문')]},
            reference=lambda kind, id: self.assertEqual((kind, id), ('figure', 'picture')))
        check_intervening(items, actual, [context])
        for fault in ('order', 'omitted', 'literal', 'figure', 'association'):
            scope, ordered, observed = deepcopy(context), deepcopy(items), deepcopy(actual)
            if fault == 'order':ordered.reverse()
            elif fault == 'omitted':ordered.pop()
            elif fault == 'literal':scope.correction['source_illustration_text_association_index'][0]['literal'] = '다름'
            elif fault == 'figure':scope.correction['source_illustration_text_association_index'][0]['figure_id'] = 'other'
            else:scope.correction['source_illustration_text_association_index'].clear()
            with self.subTest(fault=fault), self.assertRaises(ValueError):
                check_intervening(ordered, observed, [scope])

    def test_multiple_original_label_owners_require_same_figure_and_exact_region_text(self):
        from tools.pdf_restore.assembly_scoped_observations import check_intervening
        items = [dict(segment='a', type='figure', id='picture'),
                 dict(segment='a', type='block', id='left'),
                 dict(segment='a', type='block', id='right')]
        actual = [dict(type=v['type'], id='a-' + v['id']) for v in items]
        context = SimpleNamespace(name='a',
            blocks={n: dict(kind='prose', text=t, region_ids=[n + '-region'])
                    for n, t in [('left', '왼쪽'), ('right', '오른쪽')]},
            records={n + '-region': dict(corrected_text=t)
                     for n, t in [('left', '왼쪽'), ('right', '오른쪽')]},
            package={'figures': [dict(id='picture', region_ids=['figure-region'])]},
            correction={'source_illustration_text_association_index': [
                dict(block_id=n, text_region_id=n + '-region',
                     figure_id='picture', figure_region_id='figure-region') for n in ('left', 'right')]},
            reference=lambda kind, id: self.assertEqual((kind, id), ('figure', 'picture')))
        check_intervening(items, actual, [context])
        for fault in ('record-text', 'text-owner', 'figure-owner', 'association', 'intervening-caption'):
            c = deepcopy(context)
            if fault == 'record-text':c.records['right-region']['corrected_text'] = '다름'
            elif fault == 'text-owner':c.blocks['right']['region_ids'] = ['left-region']
            elif fault == 'figure-owner':c.package['figures'][0]['region_ids'] = ['other-region']
            elif fault == 'association':c.correction['source_illustration_text_association_index'].pop()
            else:c.blocks['left']['kind'] = 'caption'
            with self.subTest(fault=fault), self.assertRaises(ValueError):
                check_intervening(items, actual, [c])

    def fixture(self, root, pinned_names=False):
        path = native_tests.ScopedNativeTests().fixture(root)
        recipe = json.loads(path.read_bytes())
        recipe['source_index_mode'] = 'scoped-observations-v1'
        for join in recipe['prose_joins']:
            join['intervening'] = []
        specs = []
        for i, name in enumerate(('a', 'b')):
            folder = root / 'archive/inputs' / name
            c = json.loads((folder / 'native-corrections.json').read_bytes())
            r = json.loads((folder / 'native-recipe.json').read_bytes())
            c['coverage'] = dict(article_extent_verified=True, source_pages_missing=False,
                article_actual_folios=['K', 'L'], included_actual_folios=[['K', 'L'][i]],
                deferred_actual_folios=['L'] if i == 0 else [],
                prior_native_actual_folios=[] if i == 0 else ['K'])
            c['segment_continuations'] = [dict(kind='deferred-source-prose-continuation',
                from_region='body-region', from_block='body', last_source_text='split',
                next_source_folio='L', next_source_text='word', separator=' ',
                final_source_folios_required=['L'], assembly_required=True)] if i == 0 else [dict(
                kind='incoming-source-prose-continuation', prior_native_manifest=specs[0]['manifest'],
                prior_region_id='body-region', prior_text_end='split', from_source_folio='K',
                to_region_id='body-region', to_block_id='body', first_source_text='word',
                separator=' ', assembly_required=True)]
            if pinned_names:
                boundary = c['segment_continuations'][0]
                if i == 0:
                    boundary['region_id'] = boundary.pop('from_region')
                    boundary['next_actual_folio'] = boundary.pop('next_source_folio')
                    boundary.pop('final_source_folios_required')
                    boundary['source_occurrence'] = dict(block_id='body', literal='split')
                else:
                    boundary['kind'] = 'incoming-pinned-source-prose-continuation'
                    boundary['prior_region_name'] = boundary.pop('prior_region_id')
                    boundary['source_occurrence'] = dict(block_id='body', literal='word')
            scan = next(v['scan'] for v in c['records'] if v['id'] == 'figure-region')
            source = dict(region_id='figure-region', scan=scan, source_bbox_in_region=[0, 0, 1, 1])
            c['source_arithmetic_phase_index'] = [dict(phase_id='phase', row_ids=['row'])]
            c['source_arithmetic_row_index'] = [dict(row_id='row', phase_id='phase',
                literal='−01', field_ids=['operator', 'number'])]
            c['source_arithmetic_field_index'] = [dict(source, field_id=id, row_id='row',
                literal=text, encoded_bytes=None, evaluated_value=None)
                for id, text in [('operator', '−'), ('number', '01')]]
            c['source_arithmetic_glyph_index'] = [dict(source, slot_id='glyph:' + str(j),
                field_id='number', literal=ch, position=j, encoded_value=None)
                for j, ch in enumerate('01', 1)]
            c['source_figure_bit_index'] = [dict(source, bit_id='bit:' + str(j),
                field_id='number', literal=ch, position=j, encoded_bit=None)
                for j, ch in enumerate('01', 1)]
            c['source_figure_connector_index'] = [dict(connector_id='rule',
                region_id='figure-region', source_path_in_region=[[0, .5], [1, .5]])]
            c['source_figure_structure_index'] = [dict(structure_id='arithmetic',
                region_id='figure-region', phase_ids=['phase'], source_phase_order=['phase'],
                row_ids=['row'], field_ids=['operator', 'number'], connector_ids=['rule'],
                rows=[dict(row_id='strip-row', bit_ids=['bit:1', 'bit:2'],
                           sign_bit_id='bit:1', lsb_bit_id='bit:2')])]
            c['source_grouped_conversion_index'] = [dict(example_id='group',
                row_field_ids=[['operator', 'number']], source_alignment_ids=[])]
            c['source_regional_line_index'] = [deepcopy(c['content_associations'][0])]
            write_json(folder / 'observation-corrections.json', c)
            r['corrections'] = pin(folder, 'observation-corrections.json')
            write_json(folder / 'observation-recipe.json', r)
            output = root / 'archive/observation-segments' / name
            build(folder / 'observation-recipe.json', output, root)
            specs.append(dict(name=name, manifest=pin(root, output.relative_to(root).as_posix() + '/manifest.json')))
        recipe['segments'] = specs
        write_json(path, recipe)
        segments = [read_segment((root / s['manifest']['path']).parent, s['manifest']) for s in specs]
        return path, recipe, segments

    def test_compact_pinned_boundary_rebuild_preserves_both_original_declarations(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path, recipe, segments = self.fixture(root, pinned_names=True)
            before = deepcopy(segments)
            outputs = [root / 'work/one', root / 'work/two']
            for output in outputs:
                p = assemble(path, output, root)
                self.assertEqual(check_export(output), p)
                self.assertEqual(next(b['text'] for b in p['blocks'] if b['id'] == 'a-body'),
                                 'An opening split word follows.')
                c = json.loads((output / 'corrections.json').read_bytes())
                boundaries = c['native_indexes']['segment_continuations']
                self.assertEqual([b['value'] for b in boundaries],
                                 [s[1]['segment_continuations'][0] for s in segments])
                self.assertIn(dict(pointer='/prior_region_name', id='a-body-region'),
                              boundaries[1]['references'])
            files = lambda folder: {p.relative_to(folder).as_posix(): p.read_bytes()
                                    for p in folder.rglob('*') if p.is_file()}
            self.assertEqual(files(outputs[0]), files(outputs[1]))
            self.assertEqual(segments, before)

    def test_compact_pinned_boundary_rejects_ambiguous_unbound_or_changed_source(self):
        with tempfile.TemporaryDirectory() as temp:
            _, recipe, sources = self.fixture(Path(temp), pinned_names=True)
            cases = {
                'ambiguous outgoing region': lambda r, s: s[0][1]['segment_continuations'][0].update(from_region='body-region'),
                'ambiguous outgoing folio': lambda r, s: s[0][1]['segment_continuations'][0].update(next_source_folio='L'),
                'missing deferred extent': lambda r, s: s[0][1]['coverage'].update(deferred_actual_folios=[]),
                'wrong outgoing occurrence': lambda r, s: s[0][1]['segment_continuations'][0]['source_occurrence'].update(literal='wrong'),
                'wrong next folio': lambda r, s: s[0][1]['segment_continuations'][0].update(next_actual_folio='M'),
                'ambiguous incoming region': lambda r, s: s[1][1]['segment_continuations'][0].update(prior_region_id='body-region'),
                'wrong prior owner': lambda r, s: s[1][1]['segment_continuations'][0].update(prior_region_name='table-region'),
                'wrong incoming occurrence': lambda r, s: s[1][1]['segment_continuations'][0]['source_occurrence'].update(block_id='other'),
                'wrong manifest': lambda r, s: s[1][1]['segment_continuations'][0]['prior_native_manifest'].update(sha256='0' * 64),
                'changed word separator': lambda r, s: s[1][1]['segment_continuations'][0].update(separator=''),
                'missing explicit join': lambda r, s: r['prose_joins'].clear(),
            }
            for label, mutate in cases.items():
                r, s = deepcopy(recipe), deepcopy(sources)
                mutate(r, s)
                with self.subTest(case=label), self.assertRaises((ValueError, KeyError)):
                    project(r, s)

    def test_complete_rebuild_preserves_observations_and_binds_cross_scope_region(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path, recipe, segments = self.fixture(root)
            before = deepcopy(segments)
            outputs = [root / 'work/one', root / 'work/two']
            for output in outputs:
                p = assemble(path, output, root)
                self.assertEqual(check_export(output), p)
                self.assertEqual(next(b['text'] for b in p['blocks'] if b['id'] == 'a-body'),
                                 'An opening split word follows.')
                c = json.loads((output / 'corrections.json').read_bytes())
                self.assertEqual(c['source_index_mode'], 'scoped-observations-v1')
                identities = {v['id'] for scope in c['scopes'] for v in scope['identities']}
                for field, entries in c['native_indexes'].items():
                    self.assertEqual([(v['scope'], v['value']) for v in entries],
                        [(s['name'], row) for s, (_, source) in zip(recipe['segments'], segments)
                         for row in source.get(field, [])])
                    for entry in entries:
                        self.assertTrue(all(v['id'] in identities for v in entry['references']))
                        for span in entry['ranges']:
                            self.assertEqual((output / span['download']).read_bytes()[
                                span['start_byte']:span['end_byte']].decode(), span['literal'])
                incoming = c['native_indexes']['segment_continuations'][1]
                self.assertIn(dict(pointer='/prior_region_id', id='a-body-region'), incoming['references'])
            files = lambda folder: {p.relative_to(folder).as_posix(): p.read_bytes()
                                    for p in folder.rglob('*') if p.is_file()}
            self.assertEqual(files(outputs[0]), files(outputs[1]))
            self.assertEqual(segments, before)

    def test_dangling_typed_records_invalid_geometry_and_boundary_changes_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, recipe, sources = self.fixture(root)
            cases = {
                'legacy mode rejects new records': lambda r, s: r.update(source_index_mode='scoped-native-v1'),
                'unknown array': lambda r, s: s[0][1].update(source_unknown_index=[]),
                'missing field': lambda r, s: s[0][1]['source_arithmetic_field_index'].pop(),
                'duplicate identity': lambda r, s: s[0][1]['source_arithmetic_field_index'].append(deepcopy(s[0][1]['source_arithmetic_field_index'][0])),
                'wrong nested group': lambda r, s: s[0][1]['source_grouped_conversion_index'][0]['row_field_ids'][0].append('missing'),
                'unknown phase': lambda r, s: s[0][1]['source_figure_structure_index'][0]['source_phase_order'].append('missing'),
                'unknown bit': lambda r, s: s[0][1]['source_figure_structure_index'][0]['rows'][0].update(lsb_bit_id='missing'),
                'computed value': lambda r, s: s[0][1]['source_arithmetic_field_index'][0].update(evaluated_value=1),
                'inferred encoding': lambda r, s: s[0][1]['source_figure_bit_index'][0].update(encoded_bit=0),
                'geometry outside image': lambda r, s: s[0][1]['source_arithmetic_field_index'][0].update(source_bbox_in_region=[0, 0, 2, 1]),
                'connector outside image': lambda r, s: s[0][1]['source_figure_connector_index'][0].update(source_path_in_region=[[0, 0], [2, 1]]),
                'wrong source extent': lambda r, s: s[0][1]['coverage']['article_actual_folios'].append('M'),
                'missing source page': lambda r, s: s[0][1]['coverage'].update(source_pages_missing=True),
                'unknown deferred page': lambda r, s: s[0][1]['coverage']['deferred_actual_folios'].append('M'),
                'missing outgoing': lambda r, s: s[0][1]['segment_continuations'].clear(),
                'missing incoming': lambda r, s: s[1][1]['segment_continuations'].clear(),
                'wrong incoming pin': lambda r, s: s[1][1]['segment_continuations'][0]['prior_native_manifest'].update(sha256='0' * 64),
                'wrong incoming region': lambda r, s: s[1][1]['segment_continuations'][0].update(prior_region_id='table-region'),
                'wrong outgoing region': lambda r, s: s[0][1]['segment_continuations'][0].update(from_region='table-region'),
                'wrong separator': lambda r, s: s[1][1]['segment_continuations'][0].update(separator=''),
                'missing join': lambda r, s: r['prose_joins'].clear(),
            }
            for label, mutate in cases.items():
                r, s = deepcopy(recipe), deepcopy(sources)
                mutate(r, s)
                with self.subTest(case=label), self.assertRaises((ValueError, KeyError)):
                    project(r, s)

    def test_rehashed_outer_observation_tampering_rejects(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path, _, _ = self.fixture(root)
            output = root / 'work/one'
            assemble(path, output, root)
            c = json.loads((output / 'corrections.json').read_bytes())
            c['native_indexes']['source_figure_bit_index'][0]['value']['literal'] = '1'
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
