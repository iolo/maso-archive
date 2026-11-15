"""Source literals survive assembly as typed spans, not inferred character bytes."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_image_fragment_assemble as fragments
from tools.pdf_restore.assemble import assemble,project,read_segment
from tools.pdf_restore.assembly_indexes import block_ranges
from tools.pdf_restore.build import build,check_export
from tools.pdf_restore.inventory import pin,write_json

S,E='utf8_byte_start','utf8_byte_end_exclusive'


class ImageSourceIndexTests(unittest.TestCase):
    def test_label_graphics_derived_code_coordinates_whole_caption_and_prose_anchor(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);recipe=json.loads(path.read_bytes())
            segments=[read_segment((root/s['manifest']['path']).parent,s['manifest']) for s in recipe['segments']]
            recipe['source_index_mode']='regional-literals-v2'
            c=segments[0][1]
            for key in ('unresolved_graphics','unresolved_text'):
                c[key][0].pop('block_start_byte');c[key][0].pop('block_end_byte')
            label=c['figure_label_index'][0];label['text']='Apple ⟦screen⟧';label.pop('literal',None)
            c['figure_structures'][0].update(figure_id='figure',labels=[label['label_id']])
            graphic=dict(figure_id='figure',figure_label_id=label['label_id'],region_id=label['region_id'],scan=label['scan'],
                marker='⟦screen⟧',transcription_excerpt='⟦screen⟧',status='manual-correction-required',
                original_bytes=None,encoded_bytes=None,originalGlyphCount=None,source_encoding_verified=False,machine_byte_verified=False)
            for key in ('unresolved_graphics','unresolved_text'):c[key].append(deepcopy(graphic))
            caption=c['listing_caption_associations'][0]
            caption.pop('start_byte');caption.pop('end_byte');caption['caption_region_id']='table-region'
            c['source_uncertainties'].append(dict(block_id='table',region_id='table-region',anchor_byte=0,literal=''))
            package,active=project(recipe,segments)
            self.assertEqual(active['unresolved_graphics'][0]['block_start_byte'],9)
            self.assertEqual(active['unresolved_graphics'][1]['figure_label_id'],'a:figure:l1')
            self.assertEqual(active['figure_structures'][0]['labels'],['a:figure:l1'])
            anchor=active['source_uncertainties'][-1]
            self.assertEqual(anchor['anchor_byte'],block_ranges(package)['a-table'][0])
            self.assertEqual(anchor['download'],'article.txt')
            for case in ('missing marker','wrong owner','invented caption','split anchor'):
                altered=deepcopy(segments);bad=altered[0][1]
                if case=='missing marker':
                    for key in ('unresolved_graphics','unresolved_text'):bad[key].pop()
                elif case=='wrong owner':bad['figure_structures'][0]['labels']=['absent']
                elif case=='invented caption':bad['listing_caption_associations'][0]['caption_literal']='inferred'
                else:bad['source_uncertainties'][-1]['anchor_byte']=1
                with self.subTest(case=case),self.assertRaises(ValueError):project(recipe,altered)

    def fixture(self,root):
        path=fragments.ImageFragmentAssemblyTests().fixture(root)
        recipe=json.loads(path.read_bytes());specs=[];selected='10 PRINT ⟦x⟧ '
        for i,name in enumerate('ab'):
            base=root/'archive/inputs'/name;c=json.loads((base/'fragment-corrections.json').read_bytes())
            r=json.loads((base/'fragment-recipe.json').read_bytes());mapped=json.loads((base/'map.json').read_bytes())
            if not i:
                code=next(b for b in c['blocks'] if b['id']=='code');code['text']=selected+'\n'
                next(v for v in c['records'] if v['id']=='code-region')['corrected_text']=code['text']
                next(v for v in c['regional_text_ranges'] if v['block_id']=='code')['text']=code['text']
                c['listing_line_index'][0]['text']=code['text'];c['logical_listing_line_index'][0]['logical_text']=selected
                token=c['basic_source_fields'][0];token.update(literal='⟦x⟧',start_byte=9,end_byte=16,**{S:9,E:16})
                c['unresolved_graphics']=[dict(marker='⟦x⟧',transcription_excerpt='⟦x⟧',listing_id='code',block_id='code',
                    source_unit_id='code:n10',physical_line_id='code:r1',region_id='code-region',scan=c['records'][2]['scan'],
                    download='listing.txt',block_start_byte=9,block_end_byte=16,**{S:9,E:16},
                    original_bytes=None,encoded_bytes=None,originalGlyphCount=None,source_encoding_verified=False,
                    machine_byte_verified=False,status='manual-correction-required')]
                # One source cell spans two original prose regions, with no invented separator.
                table=next(b for b in c['blocks'] if b['id']=='table');first=table['text']
                body=next(b for b in c['blocks'] if b['id']=='body');second=body['text'];table['text']+=second
                table['region_ids'].append('body-region');table['correction_evidence'].append('corrections.json#body-region')
                c['blocks'].remove(body);r['content_order']=[v for v in r['content_order'] if v['id']!='body']
                source_body=next(v for v in c['regional_text_ranges'] if v['region_id']=='body-region')
                source_body.update(block_id='table',start_byte=len(first.encode()),end_byte=len(table['text'].encode()))
                cell=dict(column='source',text=table['text'],start_byte=0,end_byte=len(table['text'].encode()),cell_kind='value',
                    source_segments=[dict(region_id='table-region',scan=c['records'][1]['scan'],literal=first,start_byte=0,end_byte=len(first.encode())),
                                     dict(region_id='body-region',scan=c['records'][0]['scan'],literal=second,start_byte=len(first.encode()),end_byte=len(table['text'].encode()))])
                c['tables'][0].update(columns=['source'],rows=[dict(row_id='table:r0',region_ids=['table-region','body-region'],
                    start_byte=0,end_byte=len(table['text'].encode()),cells=[cell])])
                c['content_associations'][0]['prose_block_ids']=['table']
                c['formula_occurrence_index'][0].update(block_id='table',start_byte=len(first.encode()),end_byte=len(table['text'].encode()))
                c['content_associations'] += [
                    dict(kind='source-program-range-explanation',table_id='table-region',table_row_id='table:r0',listing_id='code',
                         printed_range='10~1000',first_printed_row=10,last_printed_row=1000,source_unit_ids=['code:n10'],
                         pending_source_folios=['L'],restoration_coverage='continues in unrestored following source'),
                    dict(kind='source-title-data-group',listing_id='code',group_id='title',source_unit_ids=['code:n10'],
                         loader_printed_rows=[1000],loader_restoration='pending following source'),
                    dict(kind='source-key-dispatch-branch',table_id='table-region',table_row_id='table:r0',source_unit_id='code:n10',
                         branch_index=1,printed_key='F 1',target_printed_row=1000,target_source_unit_id=None,target_restoration='pending following source')]
                c['listing_caption_associations']=[dict(listing_id='code',code_block_id='code',caption_block_id='table',
                    caption_literal=table['text'],start_byte=0,end_byte=len(table['text'].encode()))]
            else:
                boundary=c['content_associations'][2]
                boundary.update(previous_package=dict(manifest=specs[0]['manifest']),previous_literal=selected,joined_reading=selected+', 99')
                c['content_associations'][1]['from_package']['manifest']=specs[0]['manifest']
                c['previous_package_manifest']=specs[0]['manifest']
                c['unresolved_graphics']=[]
                c['content_associations'] += [
                    dict(kind='source-prior-program-explanation',listing_id='code',previous_package_manifest=specs[0]['manifest'],
                         previous_table_id='table-region',previous_table_row_id='table:r0',printed_range='10~1000',
                         source_unit_ids=['code:n10','code:n1000']),
                    dict(kind='source-prior-title-data-loader',listing_id='code',previous_package_manifest=specs[0]['manifest'],
                         previous_group_ids=['title'],loader_source_unit_ids=['code:n1000']),
                    dict(kind='source-prior-key-dispatch-target',listing_id='code',previous_package_manifest=specs[0]['manifest'],
                         previous_table_row_id='table:r0',branch_index=1,printed_key='F 1',target_printed_row=1000,source_unit_id='code:n1000')]
            c['unresolved_text']=deepcopy(c['unresolved_graphics'])
            ranges=block_ranges(dict(blocks=c['blocks'],content_order=r['content_order']))
            c['text_index']=[dict(block_id=id,region_ids=next(b for b in c['blocks'] if b['id']==id)['region_ids'],
                                 download='article.txt',**{S:a,E:z}) for id,(a,z) in ranges.items()]
            figure=c['figure_structures'][0];region=next(v for v in mapped['regions'] if v['id']=='figure-region')
            figure.update(figure_id='figure',parts=[dict(region_id='figure-region',scan=c['records'][3]['scan'],
                source_bbox=region['bbox'],source_index=region['source_index'])],placement='Preserve the original source rectangle.')
            write_json(base/'indexed-corrections.json',c);r['corrections']=pin(base,'indexed-corrections.json')
            write_json(base/'indexed-recipe.json',r);out=root/'archive/indexed-segments'/name;build(base/'indexed-recipe.json',out,root)
            specs.append(dict(name=name,manifest=pin(root,out.relative_to(root).as_posix()+'/manifest.json')))
        recipe.update(segments=specs,source_index_mode='regional-literals-v1')
        recipe['program_links'][0]['logical_join']['joined_reading']=selected+', 99'
        write_json(path,recipe);return path

    def test_native_rebuild_retains_unknown_glyph_and_continued_cell_source_spans(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);outputs=[root/'work/one',root/'work/two']
            for out in outputs:
                p=assemble(path,out,root);self.assertEqual(check_export(out),p);c=json.loads((out/'corrections.json').read_bytes())
                glyph=c['unresolved_graphics'][0]
                self.assertNotIn('block_start_byte',c['basic_source_fields'][0])  # Frozen v1 projection vocabulary.
                self.assertEqual({k:v for k,v in glyph.items() if k!='source_ref'},
                                 {k:v for k,v in c['unresolved_text'][0].items() if k!='source_ref'})
                self.assertIsNone(glyph['original_bytes']);self.assertIsNone(glyph['originalGlyphCount'])
                self.assertEqual(glyph['physical_line_id'],'a:code:r1')
                self.assertEqual((out/'listing.txt').read_bytes()[glyph[S]:glyph[E]].decode(),'⟦x⟧')
                cell=c['tables'][0]['rows'][0]['cells'][0];parts=cell['source_segments']
                self.assertEqual([v['region_id'] for v in parts],['a-table-region','a-body-region'])
                article=(out/'article.txt').read_bytes()
                self.assertEqual(''.join(article[v[S]:v[E]].decode() for v in parts),cell['text'])
                self.assertEqual(len(c['text_index']),len(p['blocks']))
                code=next(v for v in c['text_index'] if v['block_id']=='a-code')
                self.assertEqual(len(code['source_parts']),2)
                self.assertEqual(article[code[S]:code[E]],(out/'listing.txt').read_bytes())
                self.assertEqual(len(c['resolved_source_relationships']),3)
                explanation=next(v for v in c['content_associations'] if v['kind']=='source-program-range-explanation')
                self.assertEqual(explanation['source_unit_ids'],['a:code:n10','b:code:n1000'])
                self.assertEqual(explanation['pending_source_folios'],[])
                title=next(v for v in c['content_associations'] if v['kind']=='source-title-data-group')
                self.assertEqual(title['loader_source_unit_ids'],['b:code:n1000'])
                branch=next(v for v in c['content_associations'] if v['kind']=='source-key-dispatch-branch')
                self.assertEqual(branch['target_source_unit_id'],'b:code:n1000')
                caption=c['listing_caption_associations'][0]
                self.assertEqual(article[caption[S]:caption[E]].decode(),caption['caption_literal'])
                for seg in 'ab':
                    self.assertEqual((out/f'segments/{seg}/corrections.json').read_bytes(),
                                     (root/f'archive/indexed-segments/{seg}/corrections.json').read_bytes())
            files=lambda folder:{p.relative_to(folder).as_posix():p.read_bytes() for p in folder.rglob('*') if p.is_file()}
            self.assertEqual(files(outputs[0]),files(outputs[1]))

    def test_lost_markers_cell_parts_placement_and_unscoped_references_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);recipe=json.loads(path.read_bytes())
            segments=[read_segment((root/s['manifest']['path']).parent,s['manifest']) for s in recipe['segments']]
            def glyph_change(segments,key,value):
                for field in ('unresolved_graphics','unresolved_text'):segments[0][1][field][0][key]=value
            faults={
                'missing opt-in':lambda r,s:r.pop('source_index_mode'),
                'wrong opt-in':lambda r,s:r.update(source_index_mode='unknown'),
                'missing text block':lambda r,s:s[0][1]['text_index'].pop(),
                'wrong text range':lambda r,s:s[1][1]['text_index'][0].update(**{S:1}),
                'missing mirrored marker':lambda r,s:s[0][1]['unresolved_text'].clear(),
                'missing both markers':lambda r,s:(s[0][1]['unresolved_text'].clear(),s[0][1]['unresolved_graphics'].clear()),
                'invented glyph bytes':lambda r,s:glyph_change(s,'original_bytes',[128]),
                'invented glyph count':lambda r,s:glyph_change(s,'originalGlyphCount',1),
                'encoding claimed':lambda r,s:glyph_change(s,'source_encoding_verified',True),
                'wrong physical row':lambda r,s:glyph_change(s,'physical_line_id','absent'),
                'missing cell part':lambda r,s:s[0][1]['tables'][0]['rows'][0]['cells'][0]['source_segments'].pop(),
                'cell part wrong region':lambda r,s:s[0][1]['tables'][0]['rows'][0]['cells'][0]['source_segments'][1].update(region_id='code-region'),
                'cell part wrong text':lambda r,s:s[0][1]['tables'][0]['rows'][0]['cells'][0]['source_segments'][1].update(literal='changed'),
                'artwork placement':lambda r,s:s[0][1]['figure_structures'][0]['parts'][0].update(source_bbox=[0,0,1,1]),
                'previous metadata pin':lambda r,s:s[1][1]['previous_package_manifest'].update(sha256='0'*64),
                'dangling source unit list':lambda r,s:s[0][1]['content_associations'][0].update(source_unit_ids=['absent']),
                'dangling label':lambda r,s:s[0][1]['figure_structures'][0].update(value_label_id='absent'),
                'missing prior explanation':lambda r,s:s[1][1]['content_associations'].pop(3),
                'wrong prior relationship pin':lambda r,s:s[1][1]['content_associations'][3]['previous_package_manifest'].update(sha256='0'*64),
                'changed printed range':lambda r,s:s[1][1]['content_associations'][3].update(printed_range='different'),
                'missing explanation unit':lambda r,s:s[1][1]['content_associations'][3]['source_unit_ids'].pop(),
                'missing title group':lambda r,s:s[1][1]['content_associations'][4]['previous_group_ids'].clear(),
                'invented loader':lambda r,s:s[0][1]['content_associations'][4].update(loader_printed_rows=[999]),
                'wrong key':lambda r,s:s[1][1]['content_associations'][5].update(printed_key='F 2'),
                'absent key target unit':lambda r,s:s[1][1]['content_associations'][5].update(source_unit_id='absent'),
                'absent loader unit':lambda r,s:s[1][1]['content_associations'][4].update(loader_source_unit_ids=['absent']),
                'duplicate prior occurrence':lambda r,s:s[1][1]['content_associations'].append(deepcopy(s[1][1]['content_associations'][5])),
            }
            for name,mutate in faults.items():
                r,s=deepcopy(recipe),deepcopy(segments);mutate(r,s)
                with self.subTest(fault=name),self.assertRaises(ValueError):project(r,s)


if __name__=='__main__':unittest.main()
