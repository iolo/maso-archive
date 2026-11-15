"""Printed addresses, blank fields and independent contexts survive native assembly."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_image_program_assemble as program_tests
from tools.pdf_restore.assemble import assemble, project, read_segment
from tools.pdf_restore.assembly_indexes import block_ranges
from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.inventory import pin, write_json

S,E='utf8_byte_start','utf8_byte_end_exclusive'


class ImageAddressAssemblyTests(unittest.TestCase):
    def fixture(self,root):
        path=program_tests.ImageProgramAssemblyTests().fixture(root)
        recipe=json.loads(path.read_bytes());specs=[]
        for i,name in enumerate('ab'):
            base=root/'archive/inputs'/name
            c=json.loads((base/'program-corrections.json').read_bytes())
            r=json.loads((base/'program-recipe.json').read_bytes())
            c['content_associations']=[]
            c['basic_source_fields']=[];c['formula_occurrence_index']=[]
            code=next(b for b in c['blocks'] if b['id']=='code')
            text='0C60- BD 10 03 LDA $0310,X\n' if not i else '0C63- 60 RTS \n0C64- FF ??? \n'
            code['text']=text
            next(v for v in c['records'] if v['id']=='code-region')['corrected_text']=text
            regional=next(v for v in c['regional_text_ranges'] if v['block_id']=='code')
            regional.update(text=text,end_byte=len(text.encode()))
            prefix='PRINT "한글"\n' if not i else ''
            order=r['content_order']
            if not i:
                setup=deepcopy(code);setup.update(id='setup',text=prefix)
                # Distinct text regions are required for independent code contexts.
                body=next(b for b in c['blocks'] if b['id']=='body')
                setup.update(region_ids=body['region_ids'],correction_evidence=body['correction_evidence'])
                c['blocks'].remove(body);c['blocks'].insert(0,setup)
                next(v for v in c['records'] if v['id']=='body-region')['corrected_text']=prefix
                region=next(v for v in c['regional_text_ranges'] if v['block_id']=='body')
                region.update(block_id='setup',text=prefix,start_byte=0,end_byte=len(prefix.encode()))
                order=[dict(type='block',id='setup') if v['id']=='body' else v for v in order]
            c['listing_line_index']=[];c['logical_listing_line_index']=[];c['listing_groups']=[];c['listing_index']=[]
            for listing,value,region_id in ([('setup',prefix,'body-region')] if not i else [])+[('code',text,'code-region')]:
                offset=0 if listing=='setup' else len(prefix.encode())
                scan=next(v['scan'] for v in c['regional_text_ranges'] if v['region_id']==region_id)
                cursor=0;addresses=[]
                for n,line in enumerate(value.splitlines(keepends=True),1):
                    end=cursor+len(line.encode());id=f'{listing}:r{n}'
                    addr=line[:4] if listing=='code' else None
                    common=dict(listing_id=listing,block_id=listing,download='listing.txt',**{S:offset+cursor,E:offset+end})
                    fields=[]
                    if addr:
                        addresses.append(addr)
                        parts=[('printed_address',addr),('printed_byte_group','BD 10 03' if not i else line[6:8]),
                               ('printed_mnemonic','LDA' if not i else line[9:12]),('printed_operand','$0310,X' if not i else '')]
                        parts += [(f'printed_byte_{j}',b) for j,b in enumerate(parts[1][1].split(),1)]
                        for field,literal in parts:
                            start=6+3*(int(field.rsplit('_',1)[1])-1) if field.startswith('printed_byte_') and field!='printed_byte_group' else (12 if not literal else line.index(literal))
                            z=start+len(literal)
                            fields.append(dict(field=field,literal=literal,value=literal,blank=not literal,start_byte=start,end_byte=z,
                                               block_start_byte=cursor+start,block_end_byte=cursor+z,**{S:offset+cursor+start,E:offset+cursor+z}))
                    c['listing_line_index'].append(dict(common,line_id=id,physical_line=n,region_id=region_id,scan=scan,text=line,
                        printed_line=None,printed_address=addr,block_start_byte=cursor,block_end_byte=end,fields=fields))
                    c['logical_listing_line_index'].append(dict(common,line_id=f'{listing}:a{addr}' if addr else 'setup:command',
                        printed_line=None,printed_address=addr,physical_line_ids=[id],logical_text=line.removesuffix('\n'),execute_verified=False,
                        source_parts=[dict(line_id=id,region_id=region_id,start_character=0,end_character=len(line)-1,physical_start_byte=offset+cursor)]))
                    cursor=end
                c['listing_groups'].append(dict(listing_id=listing,block_ids=[listing],line_kind='address-disassembly' if addresses else 'unnumbered-command',
                                               observed_printed_addresses=addresses,observed_printed_rows=[],execute_verified=False))
                c['listing_index'].append(dict(listing_id=listing,block_id=listing,region_ids=[region_id],download='listing.txt',**{S:offset,E:offset+cursor}))
            if not i:
                boundary=dict(kind='source-listing-continuation',listing_id='code',source_unit_id='code:a0C60',
                              segment_last_printed_address='0C60',incoming_next_printed_address='0C63',next_source_folio='L',
                              remaining_source_folios=['L'],whole_article_complete=False)
                # A literal with both listing and block coordinate systems, after multibyte setup text.
                c['source_literal_index']=[dict(listing_id='code',block_id='code',source_unit_id='code:a0C60',literal='BD',source_segments=[
                    dict(region_id='code-region',scan=scan,physical_line_id='code:r1',literal='BD',start_byte=len(prefix.encode())+6,
                         end_byte=len(prefix.encode())+8,block_start_byte=6,block_end_byte=8,download='listing.txt',
                         **{S:len(prefix.encode())+6,E:len(prefix.encode())+8})])]
                c['content_associations'].append(dict(kind='source-programs-required-together',listing_ids=['setup','code'],setup_listing_id='setup',source_prose_block_id='table'))
                c['content_associations'].append(dict(kind='source-literal-evidence',source_unit_id='code:a0C60',literal='BD',
                    source_segments=deepcopy(c['source_literal_index'][0]['source_segments'])))
            else:
                boundary=dict(kind='source-listing-continuation-from',listing_id='code',source_unit_id='code:a0C63',
                              first_printed_address='0C63',prior_last_printed_address='0C60',prior_source_unit_id='code:a0C60',
                              prior_package_manifest=specs[0]['manifest'],logical_unit_continued=False,whole_assembly_pending=True)
            c['content_associations'].insert(0,boundary)
            c.update(character_perfect_code=False,unresolved_graphics=[],unresolved_text=[])
            r['content_order']=order
            ranges=block_ranges(dict(blocks=c['blocks'],content_order=order))
            c['text_index']=[dict(block_id=id,region_ids=next(b for b in c['blocks'] if b['id']==id)['region_ids'],download='article.txt',**{S:a,E:z}) for id,(a,z) in ranges.items()]
            write_json(base/'address-corrections.json',c);r['corrections']=pin(base,'address-corrections.json')
            write_json(base/'address-recipe.json',r);out=root/'archive/address-segments'/name
            build(base/'address-recipe.json',out,root)
            specs.append(dict(name=name,manifest=pin(root,out.relative_to(root).as_posix()+'/manifest.json')))
        recipe.update(segments=specs,relationship_links=[],group_links=[],example_links=[],source_index_mode='regional-literals-v2',
            program_links=[dict(id='monitor',left=dict(segment='a',listing_id='code',last_printed_address='0C60',association=0),
                right=dict(segment='b',listing_id='code',first_printed_address='0C63',association=0),
                address_join=dict(left_source_unit_id='code:a0C60',right_source_unit_id='code:a0C63',left_folio='K',right_folio='L'))])
        write_json(path,recipe);return path

    def test_native_rebuild_preserves_addresses_contexts_blank_operands_and_utf8_coordinates(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);outputs=[root/'work/one',root/'work/two']
            for out in outputs:
                package=assemble(path,out,root);self.assertEqual(check_export(out),package)
                c=json.loads((out/'corrections.json').read_bytes())
                self.assertEqual([r['listing_id'] for r in c['listing_groups']],['a-setup','a-code'])
                self.assertEqual(c['listing_groups'][1]['observed_printed_addresses'],['0C60','0C63','0C64'])
                self.assertEqual([u['printed_line'] for u in c['logical_listing_line_index']],[None]*4)
                self.assertEqual([r['physical_line'] for r in c['listing_line_index'] if r['listing_id']=='a-code'],[1,2,3])
                field=c['source_literal_index'][0]['source_segments'][0];listing=(out/'listing.txt').read_bytes()
                self.assertEqual(listing[field[S]:field[E]],b'BD')
                self.assertEqual(field['block_start_byte'],6)
                evidence=next(r for r in c['content_associations'] if r['kind']=='source-literal-evidence')
                self.assertEqual(evidence['source_segments'][0]['block_id'],'a-code')
                blanks=[f for r in c['listing_line_index'] for f in r['fields'] if f.get('blank')]
                self.assertEqual(len(blanks),2)
                self.assertTrue(all(f[S]==f[E] for f in blanks))
                for n in 'ab':
                    self.assertEqual((out/f'segments/{n}/corrections.json').read_bytes(),(root/f'archive/address-segments/{n}/corrections.json').read_bytes())
            files=lambda folder:{p.relative_to(folder).as_posix():p.read_bytes() for p in folder.rglob('*') if p.is_file()}
            self.assertEqual(files(outputs[0]),files(outputs[1]))

    def test_false_address_boundaries_and_coordinate_confusion_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);recipe=json.loads(path.read_bytes())
            segments=[read_segment((root/s['manifest']['path']).parent,s['manifest']) for s in recipe['segments']]
            cases={
                'legacy coordinate mode':lambda r,s:r.update(source_index_mode='regional-literals-v1'),
                'missing join':lambda r,s:r['program_links'].clear(),
                'invented ordinal':lambda r,s:r['program_links'][0]['right'].update(first_printed_address=2),
                'different address':lambda r,s:r['program_links'][0]['right'].update(first_printed_address='0C64'),
                'wrong unit':lambda r,s:r['program_links'][0]['address_join'].update(right_source_unit_id='absent'),
                'wrong folio':lambda r,s:r['program_links'][0]['address_join'].update(right_folio='wrong'),
                'wrong manifest':lambda r,s:s[1][1]['content_associations'][0]['prior_package_manifest'].update(sha256='0'*64),
                'lost address':lambda r,s:s[1][1]['listing_groups'][0]['observed_printed_addresses'].pop(),
                'double ownership':lambda r,s:s[1][1]['logical_listing_line_index'][1]['physical_line_ids'].append('code:r1'),
                'wrong byte count':lambda r,s:s[0][1]['listing_line_index'][-1]['fields'].pop(),
                'wrong coordinate owner':lambda r,s:s[0][1]['source_literal_index'][0]['source_segments'][0].update(block_start_byte=7),
                'execution claim':lambda r,s:s[0][1].update(character_perfect_code=True),
                'already assembled':lambda r,s:s[1][1]['content_associations'][0].update(whole_assembly_pending=False),
            }
            for name,mutate in cases.items():
                r,s=deepcopy(recipe),deepcopy(segments);mutate(r,s)
                with self.subTest(case=name),self.assertRaises(ValueError):project(r,s)


if __name__=='__main__':unittest.main()
