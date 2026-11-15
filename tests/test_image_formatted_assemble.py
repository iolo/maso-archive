"""Formatter displays preserve multi-block programs, remarks and nested byte owners."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_image_assemble as assembly_fixture
from tools.pdf_restore.assemble import assemble, project, read_segment
from tools.pdf_restore.assembly_indexes import block_ranges
from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.inventory import pin, write_json

S,E='utf8_byte_start','utf8_byte_end_exclusive'


class ImageFormattedAssemblyTests(unittest.TestCase):
    def fixture(self,root,consecutive=False):
        path=assembly_fixture.ImageAssemblyTests().fixture(root);recipe=json.loads(path.read_bytes());specs=[]
        for i,name in enumerate('ab'):
            base=root/'archive/inputs'/name;c=json.loads((base/'corrections.json').read_bytes());r=json.loads((base/'recipe.json').read_bytes())
            text={'table':'5 END\n','code':'10 PRINT "한글"\n'} if not i else {'table':('11' if consecutive else '[10]')+' * |I| |G| |I|\n','code':'20 * B 한글\n'}
            for block in c['blocks']:
                if block['id'] in text:
                    block.update(kind='code',text=text[block['id']]);rid=block['region_ids'][0]
                    next(v for v in c['records'] if v['id']==rid)['corrected_text']=block['text']
                    next(v for v in c['regional_text_ranges'] if v['region_id']==rid).update(text=block['text'],end_byte=len(block['text'].encode()))
            c.pop('segment',None);c['tables']=[];c['listing_groups']=[];c['listing_index']=[];c['listing_line_index']=[];c['logical_listing_line_index']=[];c['basic_source_fields']=[];c['source_literal_index']=[];c['unresolved_graphics']=[];c['unresolved_text']=[]
            cursor=0
            for j,id in enumerate(['table','code']):
                value=text[id];number=5 if not i and not j else 11 if i and not j and consecutive else 10 if not i or not j else 20;listing='setup' if not i and not j else 'formatter';rid=id+'-region';scan=next(v for v in c['records'] if v['id']==rid)['scan'];end=cursor+len(value.encode());rowid=listing+':r'+str(j);unitid=listing+':n'+str(number)
                common=dict(listing_id=listing,block_id=id,download='listing.txt',**{S:cursor,E:end})
                c['listing_index'].append(dict(common,region_ids=[rid]))
                c['listing_line_index'].append(dict(common,line_id=rowid,physical_line=j+1,region_id=rid,scan=scan,text=value,printed_line=None if i and not j and not consecutive else number,row_kind='bracketed-continuation' if i and not j and not consecutive else 'numbered',block_start_byte=0,block_end_byte=len(value.encode()),fields=[]))
                c['logical_listing_line_index'].append(dict(common,line_id=unitid,printed_line=number,logical_text=value,physical_line_ids=[rowid],block_ids=[id],source_parts=[dict(line_id=rowid,region_id=rid,start_character=0,end_character=len(value),physical_start_byte=cursor)],segments=[dict(region_id=rid,block_id=id,scan=scan,**{S:cursor,E:end})],execute_verified=False,complete_in_segment=consecutive or number!=10,incoming_fragment=bool(i and not j and not consecutive)))
                if not i:c['listing_groups'].append(dict(listing_id=listing,block_ids=[id],line_kind='formatted-basic-numbered',observed_printed_rows=[number],complete=number!=10,execute_verified=False))
                else:
                    if not j:c['listing_groups'].append(dict(listing_id=listing,block_ids=['table','code'],line_kind='formatted-basic-numbered',observed_printed_rows=[11 if consecutive else 10,20],complete=False,execute_verified=False))
                    if not j:
                        for ordinal,letter in enumerate('IGI',1):
                            a=value.index('|')+(ordinal-1)*4;literal='|'+letter+'|';part=dict(region_id=rid,block_id=id,physical_line_id=rowid,scan=scan,literal=literal,block_start_byte=a,block_end_byte=a+3,download='listing.txt',**{S:cursor+a,E:cursor+a+3})
                            c['source_literal_index'].append(dict(kind='source-control-display-run',listing_id=listing,block_id=id,source_unit_id=unitid,run_id='run'+str(ordinal),source_figure_id='figure',source_figure_region_id='figure-region',originalGlyphCount=None,encoding_verified=False,literal=literal,source_segments=[part]))
                    else:
                        a=value.encode().index('한글'.encode());part=dict(region_id=rid,block_id=id,physical_line_id=rowid,scan=scan,literal='한글',block_start_byte=a,block_end_byte=a+6,download='listing.txt',**{S:cursor+a,E:cursor+a+6})
                        c['basic_source_fields'].append(dict(part,listing_id=listing,source_unit_id=unitid,start_byte=cursor+a,end_byte=cursor+a+6))
                        definition=dict(kind='source-variable-definition',listing_id=listing,source_unit_id=unitid,heading_source_unit_id=f'formatter:n{11 if consecutive else 10}',qualifier_source_unit_ids=[f'formatter:n{11 if consecutive else 10}'],description_parts=[part])
                cursor=end
            if not i:
                boundary=dict(kind='source-listing-continuation',listing_id='formatter',last_source_unit_id='formatter:n10',logical_group_complete=False,next_folio='L',next_printed_marker='[10]',pending_source_folios=['L'],whole_article_assembly_pending=True)
                if consecutive:boundary.update(next_printed_row=11)
                c['content_associations']=[boundary]
            else:
                boundary=dict(kind='source-incoming-listing-boundary',listing_id='formatter',first_source_unit_id='formatter:n10',previous_source_unit_id='formatter:n10',previous_folio='K',previous_group_complete=consecutive,same_source_group=not consecutive,incoming_marker='[10]')
                if consecutive:boundary.update(first_source_unit_id='formatter:n11')
                c['content_associations']=[boundary,definition,dict(kind='source-control-display-comment',listing_id='formatter',display_source_unit_id=f'formatter:n{11 if consecutive else 10}',comment_source_unit_id='formatter:n20',source_figure_id='figure',display_run_ids=['run1','run2','run3'])]
            if i:
                body=next(v for v in c['blocks'] if v['id']=='body');start=block_ranges(dict(blocks=c['blocks'],content_order=r['content_order']))['body'][0]
                c['content_associations'].append(dict(kind='source-formatter-statistics',block_id='body',literal=body['text'],download='article.txt',**{S:start,E:start+len(body['text'].encode())}))
            ranges=block_ranges(dict(blocks=c['blocks'],content_order=r['content_order']));c['text_index']=[dict(block_id=id,region_ids=next(b for b in c['blocks'] if b['id']==id)['region_ids'],download='article.txt',**{S:a,E:z}) for id,(a,z) in ranges.items()]
            write_json(base/'formatted-corrections.json',c);r['corrections']=pin(base,'formatted-corrections.json');write_json(base/'formatted-recipe.json',r);out=root/'archive/formatted-segments'/name;build(base/'formatted-recipe.json',out,root);specs.append(dict(name=name,manifest=pin(root,out.relative_to(root).as_posix()+'/manifest.json')))
        recipe.update(index_mode='structured-formatted-v1',source_index_mode='regional-literals-v2',segments=specs,prose_joins=[],relationship_links=[],formatted_programs=[dict(id='setup',parts=[dict(segment='a',listing_id='setup')],joins=[]),dict(id='formatted',parts=[dict(segment=n,listing_id='formatter') for n in 'ab'],joins=[dict(kind='consecutive' if consecutive else 'same-number',left_last=10,right_first=11 if consecutive else 10,outgoing_association=0,incoming_association=0,joined_reading=None if consecutive else '10 PRINT "한글"\n[10] * |I| |G| |I|\n')])]);write_json(path,recipe);return path

    def test_native_rebuild_keeps_programs_blocks_original_rows_and_nested_utf8(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);outputs=[root/'work/one',root/'work/two']
            for out in outputs:
                p=assemble(path,out,root);self.assertEqual(check_export(out),p);c=json.loads((out/'corrections.json').read_bytes());listing=(out/'listing.txt').read_bytes()
                self.assertEqual([g['listing_id'] for g in c['listing_groups']],['setup','formatted'])
                self.assertEqual(c['listing_groups'][1]['block_ids'],['a-code','b-table','b-code'])
                self.assertEqual([u['line_id'] for u in c['logical_listing_line_index']],['setup:n5','formatted:n10','formatted:n20'])
                u=c['logical_listing_line_index'][1];self.assertEqual(u['logical_text'],'10 PRINT "한글"\n[10] * |I| |G| |I|\n');self.assertEqual(len(u['source_fragments']),2);self.assertTrue(u['complete_in_article'])
                self.assertEqual(u['source_parts'][1]['start_character'],len('10 PRINT "한글"\n'))
                self.assertEqual(u['source_parts'][1]['physical_start_byte'],len('5 END\n10 PRINT "한글"\n'.encode()))
                definition=next(v for v in c['content_associations'] if v['kind']=='source-variable-definition');part=definition['description_parts'][0]
                self.assertEqual((definition['heading_source_unit_id'],definition['qualifier_source_unit_ids']),('formatted:n10',['formatted:n10']))
                self.assertEqual((part['block_id'],listing[part[S]:part[E]].decode()),('b-code','한글'))
                report=next(v for v in c['content_associations'] if v['kind']=='source-formatter-statistics');self.assertEqual((out/'article.txt').read_bytes()[report[S]:report[E]].decode(),report['literal']);self.assertEqual(report[S],block_ranges(p)['b-body'][0])
                runs=[v for v in c['source_literal_index'] if v['kind']=='source-control-display-run'];self.assertEqual([v['run_id'] for v in runs],['b:run1','b:run2','b:run3']);self.assertEqual([v['literal'] for v in runs],['|I|','|G|','|I|']);self.assertTrue(all(v['originalGlyphCount'] is None and v['encoding_verified'] is False for v in runs))
                self.assertEqual([v['source_figure_id'] for v in runs],['b-figure']*3)
                for name in 'ab':self.assertEqual((out/f'segments/{name}/corrections.json').read_bytes(),(root/f'archive/formatted-segments/{name}/corrections.json').read_bytes())
            files=lambda p:{f.relative_to(p).as_posix():f.read_bytes() for f in p.rglob('*') if f.is_file()};self.assertEqual(files(outputs[0]),files(outputs[1]))

    def test_false_boundaries_unknown_references_and_changed_source_coordinates_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);r=json.loads(path.read_bytes());s=[read_segment((root/v['manifest']['path']).parent,v['manifest']) for v in r['segments']]
            faults={
                'no formatted opt-in':lambda r,s:r.update(index_mode='structured-regions-v1'),
                'missing source context':lambda r,s:r['formatted_programs'].pop(0),
                'duplicate program':lambda r,s:r['formatted_programs'].append(deepcopy(r['formatted_programs'][0])),
                'changed joined reading':lambda r,s:r['formatted_programs'][1]['joins'][0].update(joined_reading='repaired'),
                'wrong bracket number':lambda r,s:r['formatted_programs'][1]['joins'][0].update(right_first=11),
                'wrong association':lambda r,s:r['formatted_programs'][1]['joins'][0].update(incoming_association=1),
                'wrong previous folio':lambda r,s:s[1][1]['content_associations'][0].update(previous_folio='absent'),
                'false same-group declaration':lambda r,s:s[1][1]['content_associations'][0].update(same_source_group=False),
                'false complete fragment':lambda r,s:s[0][1]['logical_listing_line_index'][-1].update(complete_in_segment=True),
                'lost physical row':lambda r,s:s[1][1]['listing_line_index'].pop(),
                'wrong character offset':lambda r,s:s[1][1]['logical_listing_line_index'][0]['source_parts'][0].update(end_character=1),
                'wrong nested block coordinate':lambda r,s:s[1][1]['content_associations'][1]['description_parts'][0].update(block_start_byte=0),
                'split UTF8 source token':lambda r,s:s[1][1]['basic_source_fields'][0].update(start_byte=s[1][1]['basic_source_fields'][0]['start_byte']+1),
                'wrong source part region':lambda r,s:s[1][1]['logical_listing_line_index'][0]['source_parts'][0].update(region_id='code-region'),
                'claimed glyph encoding':lambda r,s:s[1][1]['source_literal_index'][0].update(encoding_verified=True),
                'dangling qualifier':lambda r,s:s[1][1]['content_associations'][1].update(qualifier_source_unit_ids=['formatter:n99']),
                'dangling glyph identity':lambda r,s:s[1][1]['content_associations'][2]['display_run_ids'].append('absent'),
                'wrong known glyph crop':lambda r,s:s[1][1]['source_literal_index'][0].update(source_figure_region_id='code-region'),
                'unknown glyph crop':lambda r,s:s[1][1]['source_literal_index'][0].update(source_figure_region_id='absent'),
            }
            for name,mutate in faults.items():
                rr,ss=deepcopy(r),deepcopy(s);mutate(rr,ss)
                with self.subTest(case=name),self.assertRaises(ValueError):project(rr,ss)

    def test_consecutive_join_preserves_separate_numbers_across_multi_block_context(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root,consecutive=True);out=root/'work/one';assemble(path,out,root);c=json.loads((out/'corrections.json').read_bytes())
            self.assertEqual(c['listing_groups'][1]['observed_printed_rows'],[10,11,20])
            self.assertEqual(len(c['logical_listing_line_index']),4)
            self.assertTrue(all(len(u['source_fragments'])==1 for u in c['logical_listing_line_index']))
            self.assertEqual(c['formatted_program_joins'][0]['kind'],'consecutive')

    def test_rehashed_outer_indexes_cannot_change_nested_source_ownership(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);out=root/'work/one';assemble(path,out,root);c=json.loads((out/'corrections.json').read_bytes());c['logical_listing_line_index'][1]['source_parts'][1]['physical_start_byte']=0;write_json(out/'corrections.json',c);p=json.loads((out/'article.json').read_bytes());p['corrections']=[pin(out,'corrections.json')];write_json(out/'article.json',p);manifest=json.loads((out/'manifest.json').read_bytes());manifest['files']=[pin(out,v['path']) for v in manifest['files']];write_json(out/'manifest.json',manifest)
            with self.assertRaisesRegex(ValueError,'correction projection'):check_export(out)


if __name__=='__main__':unittest.main()
