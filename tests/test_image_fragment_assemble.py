"""One source statement across exports, sparse numbering and exact physical bytes."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_image_program_assemble as program_tests
from tools.pdf_restore.assemble import assemble, project, read_segment
from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.inventory import pin, write_json
from tools.pdf_restore.assembly_fragments import boundary_reading

S, E = 'utf8_byte_start', 'utf8_byte_end_exclusive'


class ImageFragmentAssemblyTests(unittest.TestCase):
    def fixture(self, root):
        path = program_tests.ImageProgramAssemblyTests().fixture(root)
        recipe = json.loads(path.read_bytes()); specs = []
        texts = ['10 PRINT "한글"\n', ', 99\n1000 END\n']
        for i, name in enumerate('ab'):
            base = root / 'archive/inputs' / name
            c = json.loads((base / 'program-corrections.json').read_bytes())
            text = texts[i]; length = len(text.encode())
            code = next(b for b in c['blocks'] if b['id'] == 'code'); code['text'] = text
            next(r for r in c['records'] if r['id'] == 'code-region')['corrected_text'] = text
            regional = next(r for r in c['regional_text_ranges'] if r['block_id'] == 'code')
            regional.update(text=text, end_byte=length)
            scan = regional['scan']; physical = []; units = []; cursor = 0
            for j, value in enumerate(text.splitlines(keepends=True)):
                number = 10 if not i or not j else 1000
                incoming = i == 1 and j == 0
                end = cursor + len(value.encode()); row_id = f'code:r{j+1}'
                common = dict(listing_id='code',block_id='code',download='listing.txt',**{S:cursor,E:end})
                physical.append(dict(common,line_id=row_id,region_id='code-region',scan=scan,
                                     text=value,physical_line=j+1,printed_line=None if incoming else number,
                                     row_kind='incoming-physical-continuation' if incoming else 'numbered',
                                     block_start_byte=cursor,block_end_byte=end,fields=[]))
                units.append(dict(common,line_id=f'code:n{number}',printed_line=number,
                                  printed_number_present=not incoming,physical_line_ids=[row_id],
                                  logical_text=value.removesuffix('\n'),execute_verified=False,
                                  source_parts=[dict(line_id=row_id,region_id='code-region',start_character=0,
                                                     end_character=len(value)-1,physical_start_byte=cursor)],
                                  segments=[dict(region_id='code-region',scan=scan,**{S:cursor,E:end})]))
                cursor = end
            c['listing_line_index'] = physical; c['logical_listing_line_index'] = units
            c['listing_index'][0][E] = length
            numbers = [r['printed_line'] for r in physical if r['printed_line'] is not None]
            c['listing_groups'] = [dict(listing_id='code',block_ids=['code'],line_kind='basic-numbered',
                                        first_printed_row=numbers[0],last_printed_row=numbers[-1],
                                        observed_printed_rows=numbers,execute_verified=False)]
            if i:
                c['basic_source_fields'][0].update(source_unit_id='code:n10',literal=',',start_byte=0,end_byte=1,**{S:0,E:1})
                boundary = dict(kind='incoming-listing-continuation',listing_id='code',code_block_id='code',
                                source_region_id='code-region',previous_folio='K',previous_package=dict(manifest=specs[0]['manifest']),
                                first_source_unit_id='code:n10',previous_source_unit_id='code:n10',
                                previous_last_printed_row=10,first_contextual_printed_row=10,printed_number_present=False,
                                previous_literal=texts[0].strip(),literal=', 99',joined_reading=texts[0].strip()+', 99',
                                next_numbered_row=1000)
                c['content_associations'][1]['from_package']['manifest'] = specs[0]['manifest']
            else:
                c['listing_groups'][0]['open_final_source_unit_id'] = 'code:n10'
                boundary = dict(kind='listing-continuation',listing_id='code',code_block_id='code',
                                source_region_id='code-region',last_printed_row=10,last_source_unit_id='code:n10',
                                logical_unit_complete=False,next_folio='L',following_physical_fragment=', 99',
                                next_numbered_row=1000,open_source_label='10 PRINT')
            c['content_associations'] = c['content_associations'][:2] + [boundary]
            write_json(base/'fragment-corrections.json', c)
            source_recipe = json.loads((base/'program-recipe.json').read_bytes())
            source_recipe['corrections'] = pin(base, 'fragment-corrections.json')
            write_json(base/'fragment-recipe.json', source_recipe)
            output = root/'archive/fragment-segments'/name
            build(base/'fragment-recipe.json',output,root)
            specs.append(dict(name=name,manifest=pin(root,output.relative_to(root).as_posix()+'/manifest.json')))
        recipe.update(segments=specs,group_links=[],program_links=[dict(id='fragment-program',
                      left=dict(segment='a',listing_id='code',last_printed_row=10,association=2),
                      right=dict(segment='b',listing_id='code',first_printed_row=10,association=2),
                      logical_join=dict(left_source_unit_id='code:n10',right_source_unit_id='code:n10',
                                        separator='',joined_reading=texts[0].strip()+', 99'))])
        write_json(path,recipe)
        return path

    def test_offline_rebuild_preserves_physical_bytes_and_one_logical_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); path=self.fixture(root); outputs=[root/'work/one',root/'work/two']
            for out in outputs:
                package=assemble(path,out,root);self.assertEqual(check_export(out),package)
                c=json.loads((out/'corrections.json').read_bytes());units=c['logical_listing_line_index']
                self.assertEqual((out/'listing.txt').read_text(),'10 PRINT "한글"\n, 99\n1000 END\n')
                self.assertEqual([u['printed_line'] for u in units],[10,1000])
                self.assertEqual(units[0]['logical_text'],'10 PRINT "한글", 99')
                self.assertEqual(units[0]['physical_line_ids'],['a:code:r1','b:code:r1'])
                self.assertEqual(len(units[0]['source_occurrences']),2)
                self.assertEqual(units[0]['source_parts'][1]['start_character'],len('10 PRINT "한글"'))
                self.assertEqual(units[0]['source_parts'][1]['physical_start_byte'],len('10 PRINT "한글"\n'.encode()))
                self.assertEqual(units[1]['source_parts'][0]['physical_start_byte'],len('10 PRINT "한글"\n, 99\n'.encode()))
                self.assertEqual(c['basic_source_fields'][1]['source_unit_id'],'a:code:n10')
                self.assertEqual(c['listing_groups'][0]['observed_printed_rows'],[10,1000])
                self.assertNotIn('open_final_source_unit_id',c['listing_groups'][0])
                self.assertEqual([r['printed_line'] for r in c['listing_line_index']],[10,None,1000])
                for seg in 'ab':
                    self.assertEqual((out/f'segments/{seg}/corrections.json').read_bytes(),
                                     (root/f'archive/fragment-segments/{seg}/corrections.json').read_bytes())
            files=lambda folder:{f.relative_to(folder).as_posix():f.read_bytes() for f in folder.rglob('*') if f.is_file()}
            self.assertEqual(files(outputs[0]),files(outputs[1]))

    def test_false_fragment_joins_and_lost_source_rows_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);recipe=json.loads(path.read_bytes())
            segments=[read_segment((root/s['manifest']['path']).parent,s['manifest']) for s in recipe['segments']]
            faults={
                'missing opt-in':lambda r,s:r['program_links'][0].pop('logical_join'),
                'invented separator':lambda r,s:r['program_links'][0]['logical_join'].update(separator=' '),
                'wrong contextual number':lambda r,s:r['program_links'][0]['right'].update(first_printed_row=11),
                'wrong source unit':lambda r,s:r['program_links'][0]['logical_join'].update(right_source_unit_id='absent'),
                'invented reading':lambda r,s:r['program_links'][0]['logical_join'].update(joined_reading='repaired'),
                'wrong manifest':lambda r,s:s[1][1]['content_associations'][2]['previous_package']['manifest'].update(sha256='0'*64),
                'wrong folio':lambda r,s:s[0][1]['content_associations'][2].update(next_folio='wrong'),
                'already complete':lambda r,s:s[0][1]['content_associations'][2].update(logical_unit_complete=True),
                'incoming number invented':lambda r,s:s[1][1]['logical_listing_line_index'][0].update(printed_number_present=True),
                'wrong prior text':lambda r,s:s[1][1]['content_associations'][2].update(previous_literal='other'),
                'wrong incoming text':lambda r,s:s[0][1]['content_associations'][2].update(following_physical_fragment=', 98'),
                'wrong next number':lambda r,s:s[1][1]['content_associations'][2].update(next_numbered_row=20),
                'lost sparse number':lambda r,s:s[1][1]['listing_groups'][0].update(observed_printed_rows=[999]),
                'wrong logical character range':lambda r,s:s[0][1]['logical_listing_line_index'][0]['source_parts'][0].update(end_character=11),
                'byte versus character confusion':lambda r,s:s[0][1]['logical_listing_line_index'][0]['source_parts'][0].update(end_character=len('10 PRINT "한글"'.encode())),
                'wrong physical start':lambda r,s:s[1][1]['logical_listing_line_index'][0]['source_parts'][0].update(physical_start_byte=1),
                'duplicate physical ownership':lambda r,s:s[1][1]['logical_listing_line_index'][1]['physical_line_ids'].append('code:r1'),
            }
            for name,mutate in faults.items():
                r,s=deepcopy(recipe),deepcopy(segments);mutate(r,s)
                with self.subTest(fault=name),self.assertRaises(ValueError):project(r,s)

    def test_wrapped_boundary_uses_logical_characters_and_physical_byte_positions(self):
        physical=[dict(line_id='first',text='10 PRINT "한\n',block_start_byte=0),
                  dict(line_id='wrap',text='글"\n',block_start_byte=len('10 PRINT "한\n'.encode()))]
        unit=dict(physical_line_ids=['first','wrap'],logical_text='10 PRINT "한글"',source_parts=[
            dict(line_id='first',start_character=0,end_character=11,physical_start_byte=0),
            dict(line_id='wrap',start_character=11,end_character=13,
                 physical_start_byte=len('10 PRINT "한\n'.encode()))])
        self.assertEqual(boundary_reading(unit,physical),'10 PRINT "한글"')
        bad=deepcopy(unit);bad['source_parts'][1]['physical_start_byte']=len('10 PRINT "한\n')
        with self.assertRaises(ValueError):boundary_reading(bad,physical)

    def test_rehashed_outer_logical_repair_is_rejected_against_original_fragments(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);out=root/'work/one';assemble(path,out,root)
            c=json.loads((out/'corrections.json').read_bytes())
            c['logical_listing_line_index'][0]['logical_text']='10 PRINT "repaired", 99'
            write_json(out/'corrections.json',c)
            p=json.loads((out/'article.json').read_bytes());p['corrections']=[pin(out,'corrections.json')]
            write_json(out/'article.json',p)
            manifest=json.loads((out/'manifest.json').read_bytes())
            manifest['files']=[pin(out,r['path']) for r in manifest['files']]
            write_json(out/'manifest.json',manifest)
            with self.assertRaisesRegex(ValueError,'correction projection'):check_export(out)


if __name__=='__main__':unittest.main()
