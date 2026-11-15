"""Distinct sparse BASIC units retain wrapped Unicode rows and byte ownership."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_image_program_assemble as programs
from tools.pdf_restore.assemble import assemble, project, read_segment
from tools.pdf_restore.assembly_indexes import block_ranges
from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.inventory import pin, write_json

S, E = 'utf8_byte_start', 'utf8_byte_end_exclusive'


class ImageNumberedAssemblyTests(unittest.TestCase):
    def fixture(self, root):
        path = programs.ImageProgramAssemblyTests().fixture(root)
        recipe = json.loads(path.read_bytes()); specs = []
        for i, name in enumerate('ab'):
            base = root/'archive/inputs'/name
            c = json.loads((base/'program-corrections.json').read_bytes())
            r = json.loads((base/'program-recipe.json').read_bytes())
            number = (21010, 21520)[i]
            values = [f'{number} PRINT "한\n', '글"\n']
            text = ''.join(values); length = len(text.encode())
            next(v for v in c['blocks'] if v['id']=='code')['text'] = text
            next(v for v in c['records'] if v['id']=='code-region')['corrected_text'] = text
            regional = next(v for v in c['regional_text_ranges'] if v['block_id']=='code')
            regional.update(text=text, end_byte=length)
            physical = []; parts = []; segments = []; cursor = chars = 0
            for j, value in enumerate(values):
                end = cursor + len(value.encode()); id = f'code:r{j+1}'
                physical.append(dict(line_id=id, listing_id='code', block_id='code', region_id='code-region',
                    scan=regional['scan'], text=value, physical_line=j+1, printed_line=number if j==0 else None,
                    row_kind='numbered' if j==0 else 'wrapped', download='listing.txt',
                    block_start_byte=cursor, block_end_byte=end, fields=[], **{S:cursor,E:end}))
                parts.append(dict(line_id=id, region_id='code-region', start_character=chars,
                    end_character=chars+len(value)-1, physical_start_byte=cursor))
                segments.append(dict(region_id='code-region',scan=regional['scan'],**{S:cursor,E:end}))
                cursor=end; chars+=len(value)-1
            c['listing_line_index']=physical
            c['logical_listing_line_index']=[dict(line_id=f'code:n{number}', listing_id='code',block_id='code',
                printed_line=number,physical_line_ids=[v['line_id'] for v in physical],
                logical_text=''.join(v.removesuffix('\n') for v in values),source_parts=parts,
                segments=segments,download='listing.txt',execute_verified=False,**{S:0,E:length})]
            c['listing_index'][0][E]=length
            c['listing_groups']=[dict(listing_id='code',block_ids=['code'],line_kind='basic-numbered',
                first_printed_row=number,last_printed_row=number,observed_printed_rows=[number],execute_verified=False)]
            # Select the second fragment, after a multibyte first fragment.
            a=len(values[0].encode())
            c['basic_source_fields']=[dict(listing_id='code',block_id='code',source_unit_id=f'code:n{number}',
                literal='글',start_byte=a,end_byte=a+3,download='listing.txt',**{S:a,E:a+3})]
            boundary=c['content_associations'][3]
            boundary.update(number_gap_inferred_missing_rows=False)
            if i:
                boundary.update(previous_last_printed_row=21010,first_printed_row=21520,
                    previous_package=dict(manifest=specs[0]['manifest']))
                c['content_associations'][1]['from_package']['manifest']=specs[0]['manifest']
            else:boundary.update(last_printed_row=21010,next_printed_row=21520)
            c['content_associations']=c['content_associations'][:2]+[boundary]
            if not i:
                body=next(v for v in c['blocks'] if v['id']=='body')
                for target in (21520,22000):
                    c['content_associations'].append(dict(kind='source-explanation-listing-reference',
                        block_id='body',literal=body['text'],start_byte=0,end_byte=len(body['text'].encode()),
                        listing_id='code',printed_row=target,source_unit_id=None,pending_source_folios=['L'],
                        reference_without_selected_source_unit=True,meaning_verified=False))
                c['content_associations'].append(dict(kind='source-retrospective-entry',entry_id='I',parent_entry_id=None))
                c['content_associations'].append(dict(kind='source-retrospective-entry',entry_id='I:1',parent_entry_id='I'))
                c['figure_structures'][0].update(transcription_region_id='table-region',transcription_block_id='table')
            else:
                prior=(root/specs[0]['manifest']['path']).parent
                c['content_associations'].append(dict(kind='source-explanation-unit-link',listing_id='code',
                    source_unit_id='code:n21520',printed_row=21520,meaning_verified=False,
                    source_explanation=dict(package=dict(manifest=specs[0]['manifest']),
                        corrections=pin(prior,'corrections.json'),association_index=3,
                        literal=json.loads((prior/'corrections.json').read_bytes())['content_associations'][3]['literal'])))
                c['content_associations'].append(dict(kind='source-listing-end',listing_id='code',
                    source_unit_id='code:n21520',last_printed_row=21520,unconditional_END_inferred=False,
                    whole_article_assembly_pending=True))
                c['content_associations'].append(dict(kind='source-numeric-data-group',listing_id='code',
                    read_loop_source_unit_id='code:n21520',data_group_source_unit_ids=['code:n21520']))
            ranges=block_ranges(dict(blocks=c['blocks'],content_order=r['content_order']))
            c['text_index']=[dict(block_id=id,region_ids=next(b for b in c['blocks'] if b['id']==id)['region_ids'],
                download='article.txt',**{S:a,E:z}) for id,(a,z) in ranges.items()]
            c['unresolved_graphics']=[];c['unresolved_text']=[]
            write_json(base/'numbered-corrections.json',c)
            r['corrections']=pin(base,'numbered-corrections.json');write_json(base/'numbered-recipe.json',r)
            out=root/'archive/numbered-segments'/name;build(base/'numbered-recipe.json',out,root)
            specs.append(dict(name=name,manifest=pin(root,out.relative_to(root).as_posix()+'/manifest.json')))
        recipe.update(segments=specs,source_index_mode='regional-literals-v2',group_links=[],
            program_links=[dict(id='sparse-program',left=dict(segment='a',listing_id='code',last_printed_row=21010,association=2),
                right=dict(segment='b',listing_id='code',first_printed_row=21520,association=2),
                numbered_join=dict(left_source_unit_id='code:n21010',right_source_unit_id='code:n21520',missing_rows_inferred=False))])
        write_json(path,recipe);return path

    def test_independent_rebuild_preserves_sparse_numbers_wraps_and_utf8_coordinates(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);outputs=[root/'work/one',root/'work/two']
            for out in outputs:
                p=assemble(path,out,root);self.assertEqual(check_export(out),p)
                c=json.loads((out/'corrections.json').read_bytes())
                self.assertEqual(c['listing_groups'][0]['observed_printed_rows'],[21010,21520])
                self.assertTrue(c['listing_groups'][0]['complete'])
                refs=[v for v in c['content_associations'] if v['kind']=='source-explanation-listing-reference']
                self.assertEqual(refs[0]['source_unit_id'],'b:code:n21520')
                self.assertFalse(refs[0]['reference_without_selected_source_unit'])
                self.assertIsNone(refs[1]['source_unit_id'])
                self.assertTrue(refs[1]['reference_absent_from_complete_source'])
                self.assertEqual(refs[1]['pending_source_folios'],[])
                entries=[v for v in c['content_associations'] if v['kind']=='source-retrospective-entry']
                self.assertEqual(entries[1]['parent_entry_id'],entries[0]['entry_id'])
                self.assertEqual(c['figure_structures'][0]['transcription_block_id'],'a-table')
                self.assertEqual(c['figure_structures'][0]['transcription_region_id'],'a-table-region')
                loop=next(v for v in c['content_associations'] if v['kind']=='source-numeric-data-group')
                self.assertEqual(loop['read_loop_source_unit_id'],'b:code:n21520')
                self.assertEqual(loop['data_group_source_unit_ids'],['b:code:n21520'])
                self.assertEqual([r['physical_line'] for r in c['listing_line_index']],[1,2,3,4])
                self.assertEqual([r['logical_text'] for r in c['logical_listing_line_index']],
                    ['21010 PRINT "한글"','21520 PRINT "한글"'])
                data=(out/'listing.txt').read_bytes();offset=len('21010 PRINT "한\n글"\n'.encode())
                self.assertEqual(c['logical_listing_line_index'][1]['source_parts'][0]['physical_start_byte'],offset)
                self.assertEqual(c['logical_listing_line_index'][1]['source_parts'][1]['start_character'],len('21520 PRINT "한'))
                for field in c['basic_source_fields']:
                    self.assertEqual(data[field[S]:field[E]].decode(),'글')
                    block=next(b for b in p['blocks'] if b['id']==field['block_id'])
                    self.assertEqual(block['text'].encode()[field['block_start_byte']:field['block_end_byte']].decode(),'글')
            files=lambda p:{f.relative_to(p).as_posix():f.read_bytes() for f in p.rglob('*') if f.is_file()}
            self.assertEqual(files(outputs[0]),files(outputs[1]))

    def test_false_boundaries_lost_wraps_and_character_byte_confusion_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);recipe=json.loads(path.read_bytes())
            segments=[read_segment((root/s['manifest']['path']).parent,s['manifest']) for s in recipe['segments']]
            faults={
                'no opt-in':lambda r,s:r['program_links'][0].pop('numbered_join'),
                'wrong source unit':lambda r,s:r['program_links'][0]['numbered_join'].update(right_source_unit_id='absent'),
                'missing inference policy':lambda r,s:r['program_links'][0]['numbered_join'].pop('missing_rows_inferred'),
                'inferred rows':lambda r,s:r['program_links'][0]['numbered_join'].update(missing_rows_inferred=True),
                'legacy mode':lambda r,s:r.pop('source_index_mode'),
                'wrong manifest':lambda r,s:s[1][1]['content_associations'][2]['previous_package']['manifest'].update(sha256='0'*64),
                'wrong number':lambda r,s:s[1][1]['logical_listing_line_index'][0].update(printed_line=21010),
                'wrong observed rows':lambda r,s:s[1][1]['listing_groups'][0].update(observed_printed_rows=[21521]),
                'lost wrap':lambda r,s:s[1][1]['logical_listing_line_index'][0]['physical_line_ids'].pop(),
                'duplicate wrap':lambda r,s:s[1][1]['logical_listing_line_index'][0]['physical_line_ids'].append('code:r2'),
                'byte as character':lambda r,s:s[1][1]['logical_listing_line_index'][0]['source_parts'][0].update(end_character=len('21520 PRINT "한'.encode())),
                'wrong physical byte':lambda r,s:s[1][1]['logical_listing_line_index'][0]['source_parts'][1].update(physical_start_byte=14),
                'normalized logical text':lambda r,s:s[1][1]['logical_listing_line_index'][0].update(logical_text='21520 PRINT "Hangul"'),
                'wrong prose source pin':lambda r,s:s[1][1]['content_associations'][3]['source_explanation']['corrections'].update(sha256='0'*64),
                'wrong prose occurrence':lambda r,s:s[1][1]['content_associations'][3]['source_explanation'].update(association_index=4),
                'wrong prose literal':lambda r,s:s[1][1]['content_associations'][3]['source_explanation'].update(literal='inferred'),
                'lost declared link':lambda r,s:s[1][1]['content_associations'].pop(3),
                'false final row':lambda r,s:s[1][1]['content_associations'][4].update(last_printed_row=22000),
                'invented END':lambda r,s:s[1][1]['content_associations'][4].update(unconditional_END_inferred=True),
                'missing read loop':lambda r,s:s[1][1]['content_associations'][5].update(read_loop_source_unit_id='absent'),
                'missing DATA unit':lambda r,s:s[1][1]['content_associations'][5].update(data_group_source_unit_ids=['absent']),
                'missing ending':lambda r,s:s[1][1]['content_associations'].pop(4),
                'absent parent':lambda r,s:s[0][1]['content_associations'][6].update(parent_entry_id='absent'),
            }
            for name,mutate in faults.items():
                r,s=deepcopy(recipe),deepcopy(segments);mutate(r,s)
                with self.subTest(fault=name),self.assertRaises(ValueError):project(r,s)


if __name__=='__main__':unittest.main()
