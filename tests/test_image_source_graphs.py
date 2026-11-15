"""Scoped graph/wire identities, source command derivation and prose continuity."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_image_assemble as base
from tools.pdf_restore.assemble import assemble,project,read_segment,text_bytes
from tools.pdf_restore.assembly_indexes import block_ranges
from tools.pdf_restore.build import build,check_export
from tools.pdf_restore.inventory import pin,write_json
S,E='utf8_byte_start','utf8_byte_end_exclusive'


class SourceGraphAssemblyTests(unittest.TestCase):
    def fixture(self,root):
        path=base.ImageAssemblyTests().fixture(root);recipe=json.loads(path.read_bytes());specs=[]
        for i,name in enumerate('ab'):
            folder=root/'archive/inputs'/name;load=lambda n:json.loads((folder/n).read_bytes());c=load('corrections.json');r=load('recipe.json');m=load('map.json');recognition=load('recognition-map.json')
            for value in [m,recognition]:value['pages'][0]['printed_page']=str(i+1)
            write_json(folder/'v4-recognition.json',recognition);rec=pin(folder,'v4-recognition.json');write_json(folder/'v4-map.json',m)
            evidence=load('ocr/evidence.json')
            for result in evidence['results']:
                settings=load('ocr/'+result['settings']['path']);settings['package']['sha256']=rec['sha256'];write_json(folder/'ocr'/result['settings']['path'],settings);result['settings']=pin(folder/'ocr',result['settings']['path'])
            write_json(folder/'ocr/evidence.json',evidence);r['ocr_bundles']=[dict(directory='ocr',manifest=pin(folder,'ocr/evidence.json'),recognition_map=rec)];r['map']=pin(folder,'v4-map.json')
            c.pop('segment',None);c['map']=r['map'];c['tables']=[];c['formula_occurrence_index']=[];c['source_literal_index']=[];c['inline_source_fields']=[];c['unresolved_graphics']=[];c['unresolved_text']=[];c['character_perfect_code']=False
            B={v['id']:v for v in c['blocks']};B['body']['text']='P 그림 4, 5 한글 더' if not i else '욱 P 본문.'
            if i:B['table']['text']='그림 4 흐름도'
            if not i:
                B['code']['text']='POKE X, 1';c.pop('listing_line_index');c.pop('logical_listing_line_index');c['basic_source_fields']=[]
                c['listing_groups']=[dict(listing_id='code',block_ids=['code'],line_kind='unnumbered-command-example',complete=True,execute_verified=False)]
                c['listing_index'][0][E]=len(B['code']['text'].encode())
            else:
                u=c['logical_listing_line_index'][0];u['logical_text']=B['code']['text'].rstrip('\n');u['source_parts']=[dict(line_id='code:r1',region_id='code-region',start_character=0,end_character=len(u['logical_text']),physical_start_byte=0)]
            for v in c['records']:
                id=v['id'].removesuffix('-region')
                if id in B:v['corrected_text']=B[id]['text']
            for v in c['regional_text_ranges']:
                text=B[v['block_id']]['text'];v.update(text=text,end_byte=len(text.encode()))
            r['content_order']=[dict(type='figure' if id=='figure' else 'block',id=id) for id in (['table','code','figure','body'] if not i else ['figure','table','body','code'])]
            ranges=block_ranges(dict(blocks=c['blocks'],content_order=r['content_order']))
            c['text_index']=[dict(block_id=id,region_ids=B[id]['region_ids'],download='article.txt',**{S:a,E:z}) for id,(a,z) in ranges.items()]
            def at(id,text,start,**extra):return dict(block_id=id,literal=text,start_byte=start,end_byte=start+len(text.encode()),source_segments=[dict(region_id=id+'-region',scan=next(v['scan'] for v in c['records'] if v['id']==id+'-region'),literal=text,start_byte=start,end_byte=start+len(text.encode()))],download='listing.txt' if id=='code' else 'article.txt',**{S:start if id=='code' else ranges[id][0]+start,E:start+len(text.encode()) if id=='code' else ranges[id][0]+start+len(text.encode())},**extra)
            c['content_associations']=[at('body',B['body']['text'],0,kind='source-paragraph',paragraph_id='body:p1')]
            if not i:
                token=at('code','POKE',0,listing_id='code',token_id='command:token');c['inline_source_fields']=[deepcopy(token)]
                c['content_associations'] += [at('code',B['code']['text'],0,kind='source-command-example',listing_id='code',format_id='command',tokens=[token],execute_verified=False),at('body','그림 4, 5',2,kind='source-pending-figure-reference',printed_figure_numbers=[4,5],target_verified=False,meaning_verified=False)]
            else:c['content_associations'].append(dict(kind='source-prose-continuation-pending-assembly',from_segment='a',to_segment='b',from_folio=1,to_folio=2,from_literal='더',to_literal='욱',to_block_id='body',intervening_figure_folios=[],source_absence_claim=False))
            c['content_associations'].append(dict(kind='article-segment-continuation' if not i else 'article-segment-assembly-required',selected_folios=[i+1],whole_source_extent=[1,2],**({'pending_folios':[2]} if not i else {'opening_segment_folios':[1]}),whole_article_assembly_required=True,source_absence_claim=False))
            a=len(B['body']['text'].split('P')[0].encode());field=at('body','P',a,field_id='field',region_id='body-region')
            c['figure_structures']=[dict(figure_id='figure',figure_region_id='figure-region',scan=next(v['scan'] for v in c['records'] if v['id']=='figure-region'),graphs=[dict(graph_id=g,nodes=[dict(node_id='r'),dict(node_id='idle')],edges=[dict(edge_id='edge',from_node_id='r',to_node_id='idle')]) for g in ['read','write']],cross_panel_connectors=[dict(source_graph='read',source_node='idle',target_graph='write',target_node='r',physical_line_claim=False)],source_fields=[field],components=[dict(component_id='chip',model_field_id='field',ports=[dict(port_id='chip.p',printed_label='P',printed_pin=None,label_field_id='field'),dict(port_id='chip.q',printed_label=None,printed_pin=None)])],wires=[dict(wire_id=w,endpoints=['chip.p','chip.q']) for w in ['w1','w2']],crossings=[dict(crossing_id='crossing',wire_ids=['w1','w2'],dot_present=False,source_connected=None,connectivity_verified=False)],bus_elisions=[])]
            c['figure_associations']=[dict(figure_id='figure',figure_region_id='figure-region',caption_block_ids=['table'] if i else [],caption_literals=[B['table']['text']] if i else [],transcription_block_ids=[])]
            if i:r['figures'][0]['caption']=B['table']['text']
            write_json(folder/'v4-corrections.json',c);r['corrections']=pin(folder,'v4-corrections.json');write_json(folder/'v4-recipe.json',r)
            out=root/'archive/v4-segments'/name;build(folder/'v4-recipe.json',out,root);specs.append(dict(name=name,manifest=pin(root,out.relative_to(root).as_posix()+'/manifest.json')))
        recipe.update(index_mode='structured-programs-v1',source_index_mode='regional-literals-v4',segments=specs,prose_joins=[],relationship_links=[],program_links=[],group_links=[],example_links=[],reference_links=[],paragraph_links=[dict(id='continuation',left=dict(segment='a',association=0,literal='P 그림 4, 5 한글 더'),right=dict(segment='b',association=0,literal='욱 P 본문.'),declaration=dict(segment='b',association=1),separator='',evidence='Reviewed matching source paragraph fragments across the figure.')],figure_links=[dict(source=dict(segment='a',association=2,literal='그림 4, 5'),targets=[dict(segment='b',figure_id='figure',caption_block_id='table',printed_number=4)],unresolved_numbers=[5],evidence='Only source caption4 is observed.')])
        write_json(path,recipe);return path

    def load(self,root,path):
        recipe=json.loads(path.read_bytes());return recipe,[read_segment((root/s['manifest']['path']).parent,s['manifest']) for s in recipe['segments']]

    def test_rebuild_keeps_scoped_graphs_source_contexts_and_continuation(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);outs=[root/'work/one',root/'work/two']
            for out in outs:
                p=assemble(path,out,root);self.assertEqual(check_export(out),p);c=json.loads((out/'corrections.json').read_bytes());article,listing=text_bytes(p)
                f=c['figure_structures'][0];self.assertNotEqual(f['graphs'][0]['nodes'][0]['node_id'],f['graphs'][1]['nodes'][0]['node_id']);self.assertEqual(f['graphs'][0]['edges'][0]['from_node_id'],f['graphs'][0]['nodes'][0]['node_id'])
                self.assertEqual(f['wires'][0]['endpoints'],[v['port_id'] for v in f['components'][0]['ports']]);self.assertIsNone(f['crossings'][0]['source_connected'])
                self.assertEqual([g['listing_id'] for g in c['listing_groups']],['a-code','b-code']);derived=c['listing_line_index'][0];self.assertEqual(derived['text'],'POKE X, 1');self.assertIsNone(derived['printed_line']);self.assertEqual(derived['source_ref']['pointer'],'/content_associations/1')
                self.assertNotIn('listing_line_index',json.loads((out/'segments/a/corrections.json').read_bytes()))
                for token in c['basic_source_fields']:self.assertEqual(listing[token[S]:token[E]].decode(),'한글')
                self.assertEqual(c['logical_listing_line_index'][1]['source_parts'][0]['physical_start_byte'],len(b'POKE X, 1'))
                continued=next(v for v in c['content_associations'] if v['kind']=='resolved-source-paragraph-continuation');self.assertEqual(continued['logical_display'],'P 그림 4, 5 한글 더욱 P 본문.')
                for v in continued['fragments']:self.assertEqual(article[v[S]:v[E]].decode(),v['literal'])
                self.assertEqual({v['id']:v['text'] for v in p['blocks']}['a-body'],'P 그림 4, 5 한글 더')
                ref=next(v for v in c['content_associations'] if v['kind']=='qualified-source-figure-reference');self.assertFalse(ref['target_verified']);self.assertEqual(ref['unresolved_figure_numbers'],[5])
                self.assertEqual(len([v for v in c['content_associations'] if v['kind']=='resolved-article-segment']),2)
            inventory=lambda folder:{p.relative_to(folder).as_posix():p.read_bytes() for p in folder.rglob('*') if p.is_file()};self.assertEqual(inventory(outs[0]),inventory(outs[1]))

    def test_bad_graph_definitions_occurrences_and_link_dispositions_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);r,s=self.load(root,self.fixture(root));fig=lambda s:s[0][1]['figure_structures'][0]
            cases={
                'duplicate scoped node':lambda r,s:fig(s)['graphs'][0]['nodes'].append(dict(node_id='r')),
                'dangling graph edge':lambda r,s:fig(s)['graphs'][0]['edges'][0].update(to_node_id='other'),
                'wrong cross-panel graph':lambda r,s:fig(s)['cross_panel_connectors'][0].update(target_graph='other'),
                'wrong cross-panel node':lambda r,s:fig(s)['cross_panel_connectors'][0].update(target_node='other'),
                'missing wire port':lambda r,s:fig(s)['wires'][0]['endpoints'].append('chip.absent'),
                'dangling crossing wire':lambda r,s:fig(s)['crossings'][0]['wire_ids'].append('absent'),
                'wrong field owner':lambda r,s:fig(s)['components'][0].update(model_field_id='absent'),
                'wrong printed label':lambda r,s:fig(s)['components'][0]['ports'][0].update(printed_label='Q'),
                'duplicate component':lambda r,s:fig(s)['components'].append(deepcopy(fig(s)['components'][0])),
                'missing paragraph link':lambda r,s:r['paragraph_links'].clear(),
                'duplicate paragraph declaration':lambda r,s:r['paragraph_links'].append(dict(deepcopy(r['paragraph_links'][0]),id='other')),
                'wrong paragraph occurrence':lambda r,s:r['paragraph_links'][0]['left'].update(literal='other'),
                'invented paragraph separator':lambda r,s:r['paragraph_links'][0].update(separator=' '),
                'wrong continuation folio':lambda r,s:s[1][1]['content_associations'][1].update(from_folio=0),
                'unrelated intervening prose':lambda r,s:s[1][1]['figure_associations'][0].update(caption_block_ids=[]),
                'missing figure qualification':lambda r,s:r['figure_links'].clear(),
                'invented figure5 caption':lambda r,s:r['figure_links'][0]['targets'][0].update(printed_number=5),
                'unaccounted figure number':lambda r,s:r['figure_links'][0].update(unresolved_numbers=[]),
                'repeated figure number':lambda r,s:r['figure_links'][0].update(unresolved_numbers=[4,5]),
                'wrong printed figure numbers':lambda r,s:s[0][1]['content_associations'][2].update(printed_figure_numbers=[4,6]),
            }
            for name,mutate in cases.items():
                recipe,segments=deepcopy(r),deepcopy(s);mutate(recipe,segments)
                with self.subTest(case=name),self.assertRaises(ValueError):project(recipe,segments)

    def test_command_derivation_requires_complete_source_and_mixed_offsets(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);r,s=self.load(root,self.fixture(root));cases={
                'wrong command display':lambda s:s[0][1]['content_associations'][1].update(literal='POKE X, 2'),
                'partial command':lambda s:s[0][1]['content_associations'][1].update(end_byte=8),
                'missing command declaration':lambda s:s[0][1]['content_associations'][1].update(kind='source-note'),
                'false command execution':lambda s:s[0][1]['content_associations'][1].update(execute_verified=True),
                'false group completeness':lambda s:s[0][1]['listing_groups'][0].update(complete=False),
                'wrong source field download':lambda s:s[0][1]['inline_source_fields'][0].update(download='article.txt'),
                'UTF-8 split':lambda s:s[1][1]['basic_source_fields'][0].update(utf8_byte_start=11),
                'wrong physical address':lambda s:s[1][1]['logical_listing_line_index'][0]['source_parts'][0].update(physical_start_byte=1),
            }
            for name,mutate in cases.items():
                segments=deepcopy(s);mutate(segments)
                with self.subTest(case=name),self.assertRaises(ValueError):project(r,segments)

    def test_rehashed_active_graph_and_logical_paragraph_tampering_reject(self):
        for fault in ['graph','paragraph']:
            with self.subTest(fault=fault),tempfile.TemporaryDirectory() as temp:
                root=Path(temp);path=self.fixture(root);out=root/'work/one';assemble(path,out,root);c=json.loads((out/'corrections.json').read_bytes())
                if fault=='graph':c['figure_structures'][0]['graphs'][0]['edges'][0]['to_node_id']=c['figure_structures'][0]['graphs'][1]['nodes'][0]['node_id']
                else:next(v for v in c['content_associations'] if v['kind']=='resolved-source-paragraph-continuation')['logical_display']='invented'
                write_json(out/'corrections.json',c);p=json.loads((out/'article.json').read_bytes());p['corrections']=[pin(out,'corrections.json')];write_json(out/'article.json',p);m=json.loads((out/'manifest.json').read_bytes());m['files']=[pin(out,v['path']) for v in m['files']];write_json(out/'manifest.json',m)
                with self.assertRaises(ValueError):check_export(out)

    def test_optin_exact_coverage_and_input_immutability(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);r,s=self.load(root,self.fixture(root));before=deepcopy(s);project(r,s);self.assertEqual(s,before)
            for name,change in [('wrong whole extent',dict(whole_source_extent=[1,3])),('wrong pending source',dict(pending_folios=[])),('false source absence',dict(source_absence_claim=True))]:
                changed=deepcopy(s);changed[0][1]['content_associations'][-1].update(change)
                with self.subTest(case=name),self.assertRaises(ValueError):project(r,changed)
            old=deepcopy(r);old['source_index_mode']='regional-literals-v3'
            with self.assertRaises(ValueError):project(old,s)


if __name__=='__main__':unittest.main()
