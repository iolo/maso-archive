"""Mixed command/article/code coordinates, visual graphs and reviewed references."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_image_assemble as base_tests
from tools.pdf_restore.assemble import assemble,project,read_segment,text_bytes
from tools.pdf_restore.assembly_indexes import block_ranges
from tools.pdf_restore.build import build,check_export
from tools.pdf_restore.inventory import pin,write_json

S,E='utf8_byte_start','utf8_byte_end_exclusive'


class SourceStructureAssemblyTests(unittest.TestCase):
    def fixture(self,root):
        path=base_tests.ImageAssemblyTests().fixture(root);recipe=json.loads(path.read_bytes());specs=[]
        for i,name in enumerate('ab'):
            base=root/'archive/inputs'/name;c=json.loads((base/'corrections.json').read_bytes());r=json.loads((base/'recipe.json').read_bytes())
            c.pop('segment',None);c['formula_occurrence_index']=[];c['source_literal_index']=[];c['unresolved_graphics']=[];c['unresolved_text']=[];c['character_perfect_code']=False
            body=next(v for v in c['blocks'] if v['id']=='body');body['text']=('리스팅 10에서 10; ' if not i else '')+'PRINT D$ ”OPEN FILE”'
            next(v for v in c['records'] if v['id']=='body-region')['corrected_text']=body['text']
            rr=next(v for v in c['regional_text_ranges'] if v['region_id']=='body-region');rr.update(text=body['text'],end_byte=len(body['text'].encode()))
            ranges=block_ranges(dict(blocks=c['blocks'],content_order=r['content_order']));c['text_index']=[dict(block_id=id,region_ids=next(v['region_ids'] for v in c['blocks'] if v['id']==id),download='article.txt',**{S:a,E:z}) for id,(a,z) in ranges.items()]
            scan=rr['scan']
            def at(literal,start,**extra):return dict(block_id='body',literal=literal,start_byte=start,end_byte=start+len(literal.encode()),download='article.txt',**{S:ranges['body'][0]+start,E:ranges['body'][0]+start+len(literal.encode())},**extra)
            start=len(body['text'].split('PRINT')[0].encode());literal=body['text'].encode()[start:].decode();token=at('OPEN',start+len('PRINT D$ ”'.encode()),token_id='token',command_id='command')
            token['source_region_ids']=['body-region']
            command=dict(command_id='command',logical_display=literal,source_parts=[at(literal,start)],physical_row_ids=['command-row'],tokens=[token],execute_verified=False)
            c['inline_source_fields']=[deepcopy(token)];c['content_associations']=[dict(kind='source-command-format-group',format_id='body',block_id='body',physical_rows=[at(literal,start,row_id='command-row')],commands=[command])]
            c['content_associations'][0]['format_block_id']='body'
            if not i:c['content_associations'].append(at('리스팅 1',0,kind='source-pending-listing-reference',target_native_unit_id=None,target_verified=False,target_source_folios=['L']))
            fig=c['figure_structures'][0];fig.update(figure_id='figure',nodes=[dict(node_id='paper',subareas=['paper:upper'])],file_slots=[dict(slot_id='box',interior='blank')],connectors=[dict(connector_id='arrow',from_node='paper:upper',to_node='box')],delimiters=[dict(delimiter_id='separator',literal='#')],label_ids=['figure:l1'],inspection_transform=dict(path='private-view.json',sha256='0'*64,bytes=1))
            table=c['tables'][0];table['region_id']='table-region';table['rows'][0].pop('region_id')
            asset=next(v['scan'] for v in c['records'] if v['id']=='table-region')
            for j,cell in enumerate(table['rows'][0]['cells']):
                cell['cell_id']=f'cell{j}';cell['source_segments']=[] if cell['text']=='' else [dict(region_id='table-region',scan=asset,literal=cell['text'],start_byte=cell['start_byte'],end_byte=cell['end_byte'])]
            fig['slot_ids']=['cell0','cell1']
            physical=c['listing_line_index'][0];unit=c['logical_listing_line_index'][0];unit['logical_text']=physical['text'].rstrip('\n');unit['source_parts']=[dict(line_id=physical['line_id'],region_id=physical['region_id'],start_character=0,end_character=len(unit['logical_text']),selected_text=unit['logical_text'])]
            write_json(base/'v3-corrections.json',c);r['corrections']=pin(base,'v3-corrections.json');write_json(base/'v3-recipe.json',r)
            output=root/'archive/v3-segments'/name;build(base/'v3-recipe.json',output,root);specs.append(dict(name=name,manifest=pin(root,output.relative_to(root).as_posix()+'/manifest.json')))
        source=dict(segment='a',association=1,literal='리스팅 1',context=dict(block_id='body',start_byte=0,end_byte=len('리스팅 10에서 10'.encode()),literal='리스팅 10에서 10'))
        recipe.update(index_mode='structured-programs-v1',source_index_mode='regional-literals-v3',segments=specs,prose_joins=[],relationship_links=[],program_links=[],group_links=[],example_links=[],reference_links=[dict(kind='units',source=source,target=dict(segment='b',listing_id='code',source_unit_ids=['code:n10']),evidence='Synthetic source range qualifies an intentionally partial marker.')])
        path=root/'archive/v3-assembly.json';write_json(path,recipe);return path

    def load(self,root,path):
        recipe=json.loads(path.read_bytes());return recipe,[read_segment((root/s['manifest']['path']).parent,s['manifest']) for s in recipe['segments']]

    def test_rebuild_namespaces_graphs_and_keeps_mixed_coordinate_owners(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);outputs=[root/'work/one',root/'work/two']
            for out in outputs:
                p=assemble(path,out,root);self.assertEqual(check_export(out),p);c=json.loads((out/'corrections.json').read_bytes());article,listing=text_bytes(p)
                self.assertEqual([g['listing_id'] for g in c['listing_groups']],['a-code','b-code'])
                for token in c['inline_source_fields']:
                    self.assertEqual(token['download'],'article.txt');self.assertEqual(article[token[S]:token[E]].decode(),'OPEN')
                    self.assertEqual(token['command_id'],token['source_segment']+':command')
                    self.assertEqual(token['source_region_ids'],[token['source_segment']+'-body-region'])
                for token in c['basic_source_fields']:self.assertEqual(listing[token[S]:token[E]].decode(),'한글')
                for unit in c['logical_listing_line_index']:self.assertEqual(unit['source_parts'][0]['physical_start_byte'],unit[S])
                figure=c['figure_structures'][0];self.assertEqual(figure['connectors'][0]['to_node'],'a:box');self.assertEqual(figure['connectors'][0]['from_node'],'a:paper:upper')
                self.assertEqual(figure['slot_ids'],['a:cell0','a:cell1']);self.assertEqual(figure['inspection_transform']['scope'],'original-private-review')
                self.assertEqual(figure['delimiters'][0]['delimiter_id'],'a:separator')
                group=next(v for v in c['content_associations'] if v['kind']=='source-command-format-group');self.assertEqual(group['format_block_id'],'a-body')
                self.assertFalse((out/'private-view.json').exists())
                resolved=next(v for v in c['content_associations'] if v['kind']=='resolved-source-listing-reference')
                self.assertEqual(resolved['literal'],'리스팅 1');self.assertEqual(resolved['target_source_unit_ids'],['b:code:n10'])
                context=resolved['expanded_source_reference'];self.assertEqual(article[context[S]:context[E]].decode(),'리스팅 10에서 10')
                self.assertEqual((out/'segments/a/corrections.json').read_bytes(),(root/'archive/v3-segments/a/corrections.json').read_bytes())
            files=lambda d:{p.relative_to(d).as_posix():p.read_bytes() for p in d.rglob('*') if p.is_file()}
            self.assertEqual(files(outputs[0]),files(outputs[1]))

    def test_malformed_references_graphs_and_coordinate_owners_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);recipe,segments=self.load(root,self.fixture(root))
            cases={
                'omitted reviewed reference':lambda r,s:r['reference_links'].clear(),
                'duplicate reviewed occurrence':lambda r,s:r['reference_links'].append(deepcopy(r['reference_links'][0])),
                'wrong original marker':lambda r,s:r['reference_links'][0]['source'].update(literal='리스팅 2'),
                'wrong expanded text':lambda r,s:r['reference_links'][0]['source']['context'].update(literal='리스팅 11에서 11'),
                'expanded context outside marker':lambda r,s:r['reference_links'][0]['source']['context'].update(start_byte=3),
                'wrong target row':lambda r,s:r['reference_links'][0]['target'].update(source_unit_ids=['code:n11']),
                'wrong target coverage':lambda r,s:s[0][1]['content_associations'][1].update(target_source_folios=['absent']),
                'dangling subarea':lambda r,s:s[0][1]['figure_structures'][0]['connectors'][0].update(from_node='other'),
                'duplicate graph definition':lambda r,s:s[0][1]['figure_structures'][0]['nodes'][0]['subareas'].append('paper'),
                'dangling visual cell':lambda r,s:s[0][1]['figure_structures'][0].update(slot_ids=['missing']),
                'wrong table region fallback':lambda r,s:s[0][1]['tables'][0].update(region_id='body-region'),
                'wrong logical physical address':lambda r,s:s[0][1]['logical_listing_line_index'][0]['source_parts'][0].update(physical_start_byte=1),
                'wrong logical character span':lambda r,s:s[0][1]['logical_listing_line_index'][0]['source_parts'][0].update(end_character=2),
                'article token relabeled listing':lambda r,s:s[0][1]['inline_source_fields'][0].update(download='listing.txt'),
                'wrong Unicode article offset':lambda r,s:s[0][1]['inline_source_fields'][0].update(utf8_byte_start=1),
                'wrong physical field address':lambda r,s:s[0][1]['listing_line_index'][0]['fields'][0].update(utf8_byte_start=1),
                'unknown command token':lambda r,s:s[0][1]['inline_source_fields'][0].update(command_id='missing'),
            }
            for name,mutate in cases.items():
                r,s=deepcopy(recipe),deepcopy(segments);mutate(r,s)
                with self.subTest(case=name),self.assertRaises(ValueError):project(r,s)

    def test_new_contract_is_opt_in_and_original_inputs_remain_immutable(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);recipe,segments=self.load(root,self.fixture(root));before=deepcopy(segments)
            project(recipe,segments);self.assertEqual(segments,before)
            old=deepcopy(recipe);old['source_index_mode']='regional-literals-v2'
            with self.assertRaises(ValueError):project(old,segments)
            old.pop('reference_links')
            with self.assertRaises(ValueError):project(old,segments)

    def test_source_declared_article_completion_requires_exact_folio_coverage(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);recipe,segments=self.load(root,self.fixture(root))
            for i,(source,c) in enumerate(segments):source['pages'][0]['printed_page']=str(i+1)
            segments[0][1]['content_associations'][1]['target_source_folios']=[2]
            segments[0][1]['content_associations'].append(dict(kind='article-segment-continuation',source_folios=[1],whole_source_extent=[1,2],pending_source_folios=[2],whole_article_assembly_required=True,source_absence_claim=False))
            segments[1][1]['content_associations'].append(dict(kind='article-segment-assembly-required',selected_folios=[2],whole_source_extent=[1,2],opening_segment_folios=[1],whole_article_assembly_required=True,source_absence_claim=False))
            _,c=project(recipe,segments);resolved=[v for v in c['content_associations'] if v['kind']=='resolved-article-segment']
            self.assertEqual(len(resolved),2);self.assertTrue(all(v['whole_article_complete'] and not v['whole_article_assembly_required'] for v in resolved))
            for change in [dict(whole_source_extent=[1,3]),dict(source_folios=[2]),dict(pending_source_folios=[]),dict(source_absence_claim=True)]:
                altered=deepcopy(segments);altered[0][1]['content_associations'][-1].update(change)
                with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,altered)


if __name__=='__main__':unittest.main()
