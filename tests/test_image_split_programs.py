"""Split statement assembly: source preservation, exact exports and strict bounds."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_image_scoped_native as base
from tools.pdf_restore.assemble import assemble, project, read_segment
from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.inventory import pin, write_json

S, E = 'utf8_byte_start', 'utf8_byte_end_exclusive'


class SplitProgramTests(unittest.TestCase):
    def fixture(self, root):
        path = base.ScopedNativeTests().fixture(root)
        recipe = json.loads(path.read_bytes())
        recipe.update(source_index_mode='scoped-split-programs-v1', logical_aliases=[], prose_joins=[])
        specs = []
        for i, (name, text) in enumerate((('a', '10 PRINT "한글"'), ('b', ' + "계속"\n\n20 END\n'))):
            folder = root / 'archive/inputs' / name
            old = json.loads((folder / 'native-corrections.json').read_bytes())
            c = {k: deepcopy(old[k]) for k in ('article_id', 'map', 'records', 'blocks', 'regional_text_ranges', 'tables')}
            r = json.loads((folder / 'native-recipe.json').read_bytes())
            for record in c['records']:
                if record['id'] == 'code-region':
                    record['corrected_text'] = text
            for block in c['blocks']:
                if block['id'] == 'code':
                    block['text'] = text
            for region in c['regional_text_ranges']:
                if region['region_id'] == 'code-region':
                    region.update(text=text, end_byte=len(text.encode()))
            rows = []
            cursor = 0
            for j, line in enumerate(text.splitlines(keepends=True)):
                size = len(line.encode())
                rows.append(dict(line_id=f'r{j}', listing_id='code', block_id='code', region_id='code-region',
                    text=line, printed_line=10 if i == 0 else 20 if j == 2 else None,
                    block_start_byte=cursor, block_end_byte=cursor + size,
                    download='listing.txt', fields=[], **{S: cursor, E: cursor + size}))
                cursor += size
            units = []
            for label, members in ([(10, rows)] if i == 0 else [(None, rows[:2]), (20, rows[2:])]):
                units.append(dict(line_id='u' + str(label), listing_id='code', block_id='code',
                    printed_line=label, printed_label=str(label) if label is not None else None,
                    physical_line_ids=[v['line_id'] for v in members],
                    physical_reading=''.join(v['text'] for v in members),
                    complete_in_segment=label == 20,
                    external_predecessor_required=label is None,
                    continued_printed_label='10' if label is None else None,
                    download='listing.txt', **{S: members[0][S], E: members[-1][E]}))
            c.update(listing_groups=[dict(listing_id='code', block_ids=['code'], physical_rows=len(rows),
                logical_units=len(units), complete_in_segment=False, execute_verified=False,
                original_encoded_bytes_verified=False, download='listing.txt', **{S: 0, E: cursor})],
                listing_line_index=rows, logical_listing_line_index=units)
            c['coverage'] = dict(article_extent_verified=True, source_pages_missing=False,
                article_actual_folios=['K', 'L'], included_actual_folios=[['K', 'L'][i]],
                deferred_actual_folios=['L'] if i == 0 else [],
                prior_native_actual_folios=[] if i == 0 else ['K'])
            write_json(folder / 'split-corrections.json', c)
            r['corrections'] = pin(folder, 'split-corrections.json')
            r['content_order'] = [dict(type='block', id='body'), dict(type='block', id='table')]
            if i == 0:
                r['content_order'] += [dict(type='block', id='code'), dict(type='figure', id='figure')]
            else:
                r['content_order'] = [dict(type='figure', id='figure'), dict(type='block', id='code')] + r['content_order']
            write_json(folder / 'split-recipe.json', r)
            out = root / 'archive/split-segments' / name
            build(folder / 'split-recipe.json', out, root)
            specs.append(dict(name=name, manifest=pin(root, out.relative_to(root).as_posix() + '/manifest.json')))
        recipe['segments'] = specs
        recipe['split_programs'] = [dict(program_id='main',
            fragments=[dict(segment='a', listing_id='code', first_source_unit_id='u10', last_source_unit_id='u10'),
                       dict(segment='b', listing_id='code', first_source_unit_id='uNone', last_source_unit_id='u20')],
            boundary=dict(printed_label='10', left_suffix='"한글"', right_prefix=' + "계속"', separator='\n',
                intervening=[dict(segment=s, type='figure', id='figure') for s in ('a', 'b')],
                evidence='Synthetic printed statement continues onto the next original source page.'),
            ending=dict(source_unit_id='u20', printed_label='20', literal='20 END\n', evidence='Final source row.'),
            source_extent_complete=True, evidence='Synthetic complete two-page program extent.')]
        write_json(path, recipe)
        sources = [read_segment((root / s['manifest']['path']).parent, s['manifest']) for s in specs]
        return path, recipe, sources

    def test_two_exact_exports_preserve_originals_and_all_native_ranges(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path, recipe, sources = self.fixture(root)
            original = deepcopy(sources)
            outputs = [root / 'work/one', root / 'work/two']
            for out in outputs:
                package = assemble(path, out, root)
                self.assertEqual(package, check_export(out))
                correction = json.loads((out / 'corrections.json').read_bytes())
                program = correction['split_programs'][0]
                listing = (out / 'listing.txt').read_bytes()
                self.assertEqual(listing, '10 PRINT "한글"\n + "계속"\n\n20 END\n'.encode())
                self.assertEqual((program['physical_row_count'], program['logical_unit_count']), (4, 2))
                self.assertEqual((program['nonempty_ink_rows'], program['layout_gap_search_rows']), (3, 1))
                self.assertEqual(len(program['logical_units'][0]['source_fragments']), 2)
                self.assertEqual(program['logical_units'][0]['printed_label'], '10')
                self.assertFalse(program['original_encoded_bytes_verified'])
                for row in program['physical_rows']:
                    self.assertEqual(listing[row['start_byte']:row['end_byte']].decode(),
                                     row['source_reading'] + row['serialization_suffix'])
                for field, values in correction['native_indexes'].items():
                    self.assertEqual([(v['scope'], v['value']) for v in values],
                        [(s['name'], v) for s, (_, c) in zip(recipe['segments'], original)
                         for v in c.get(field, [])])
                    for value in values:
                        for span in value['ranges']:
                            data = (out / span['download']).read_bytes()
                            self.assertEqual(data[span['start_byte']:span['end_byte']].decode(), span['literal'])
                for spec in recipe['segments']:
                    source = (root / spec['manifest']['path']).parent
                    for file in source.rglob('*'):
                        if file.is_file():
                            self.assertEqual(file.read_bytes(), (out / 'segments' / spec['name'] / file.relative_to(source)).read_bytes())
            files = lambda p: {f.relative_to(p).as_posix(): f.read_bytes() for f in p.rglob('*') if f.is_file()}
            self.assertEqual(files(outputs[0]), files(outputs[1]))
            self.assertEqual(sources, original)

    def test_incomplete_contracts_false_headers_hidden_owners_and_changed_code_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            _, recipe, sources = self.fixture(Path(temp))
            cases = {
                'missing opt-in declaration': lambda r, s: r.pop('split_programs'),
                'empty declaration': lambda r, s: r['split_programs'].clear(),
                'legacy mode': lambda r, s: r.update(source_index_mode='scoped-native-v1'),
                'missing boundary newline': lambda r, s: r['split_programs'][0]['boundary'].update(separator=''),
                'invented extra newline': lambda r, s: r['split_programs'][0]['boundary'].update(separator='\n\n'),
                'wrong label': lambda r, s: r['split_programs'][0]['boundary'].update(printed_label='11'),
                'wrong incoming literal': lambda r, s: r['split_programs'][0]['boundary'].update(right_prefix='20'),
                'missing intervening figure': lambda r, s: r['split_programs'][0]['boundary']['intervening'].pop(),
                'reversed figures': lambda r, s: r['split_programs'][0]['boundary']['intervening'].reverse(),
                'invented ending': lambda r, s: r['split_programs'][0]['ending'].update(literal='20 STOP\n'),
                'truncated units': lambda r, s: r['split_programs'][0]['fragments'][1].update(last_source_unit_id='uNone'),
                'false printed header': lambda r, s: s[1][1]['logical_listing_line_index'][0].update(printed_line=10),
                'complete incoming fragment': lambda r, s: s[1][1]['logical_listing_line_index'][0].update(complete_in_segment=True),
                'another incomplete unit': lambda r, s: s[1][1]['logical_listing_line_index'][1].update(complete_in_segment=False),
                'wrong source reading': lambda r, s: s[0][1]['logical_listing_line_index'][0].update(physical_reading='repaired'),
                'wrong physical count': lambda r, s: s[1][1]['listing_groups'][0].update(physical_rows=2),
                'encoded bytes claim': lambda r, s: s[1][1]['listing_groups'][0].update(original_encoded_bytes_verified=True),
            }
            for name, mutate in cases.items():
                r, s = deepcopy(recipe), deepcopy(sources)
                mutate(r, s)
                with self.subTest(case=name), self.assertRaises(ValueError):
                    project(r, s)

    def test_rehashed_derived_join_tampering_rejects_offline(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path, _, _ = self.fixture(root)
            out = root / 'work/export'
            assemble(path, out, root)
            c = json.loads((out / 'corrections.json').read_bytes())
            c['split_programs'][0]['logical_units'][0]['source_fragments'].pop()
            write_json(out / 'corrections.json', c)
            p = json.loads((out / 'article.json').read_bytes())
            p['corrections'] = [pin(out, 'corrections.json')]
            write_json(out / 'article.json', p)
            m = json.loads((out / 'manifest.json').read_bytes())
            m['files'] = [pin(out, f['path']) for f in m['files']]
            write_json(out / 'manifest.json', m)
            with self.assertRaisesRegex(ValueError, 'correction projection'):
                check_export(out)


if __name__ == '__main__':
    unittest.main()
