"""Structured JPEG assembly: independent page identity, typed spans and offline evidence."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from PIL import Image

from tools.pdf_restore.assemble import assemble, project, read_segment
from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.inventory import pin, write_json
from tools.pdf_restore.package import image_transform

EXAMPLE=Path(__file__).resolve().parents[1]/'examples/pdf-article.json'
START,END='utf8_byte_start','utf8_byte_end_exclusive'


class ImageAssemblyTests(unittest.TestCase):
    def fixture(self,root):
        template=json.loads(EXAMPLE.read_bytes());pages=[]
        for i,(index,folio) in enumerate([(7,'K'),(19,'L')]):
            Image.new('RGB',(120,160),['blue','green'][i]).save(root/f'page-{i}.jpg')
            page=dict(source_index=index,image=pin(root,f'page-{i}.jpg'),width_px=120,height_px=160,
                      reading_order=i+1,source_filename_number=100+i*100,printed_page=folio)
            page['image_to_upright_normalized']=image_transform(page);pages.append(page)
        write_json(root/'source-set.json',dict(kind='jpeg-set',issue_id=template['issue_id'],cleanup={},pages=pages))
        source=dict(id='jpeg-synthetic',kind='jpeg-set',**pin(root,'source-set.json'))
        write_json(root/'TOC.md',dict(synthetic=True));template.update(schema_version=2,source=source,toc_pin=pin(root,'TOC.md'))
        inventory=root/'archive/inventory'
        write_json(inventory/'sources.json',dict(sources=[dict(source,scope='toc-entries-and-cover',pages=pages)]))
        (inventory/'queue.jsonl').write_text(json.dumps(dict(toc_entry_id=template['toc_entry_id'],issue_id=template['issue_id'],source_id=source['id']))+'\n')
        inv={k:pin(root,'archive/inventory/'+name) for k,name in [('sources','sources.json'),('queue','queue.jsonl')]}
        runtime=root/'archive/toolchains/ocr';write_json(runtime/'runtime.json',{'synthetic':True})
        specs=[]
        for i,name in enumerate(['a','b']):
            base=root/'archive/inputs'/name;folder=base/'ocr';folder.mkdir(parents=True)
            page=pages[i];mapped=deepcopy(template)
            mapped.update(pages=[page],excluded_regions=[],mapping=dict(status='mapped',evidence=['Synthetic geometry'],uncertainties=[]),regions=[dict(id=id,source_index=page['source_index'],kind=kind,bbox=box,notes='Synthetic') for id,kind,box in [('body-region','prose',[0,0,.5,.25]),('table-region','prose',[.5,0,1,.25]),('code-region','code',[0,.25,1,.5]),('figure-region','figure',[0,.55,1,1])]])
            write_json(base/'recognition-map.json',mapped);recognition=pin(base,'recognition-map.json')
            mapped['regions'][3]['bbox'][1]=.5;write_json(base/'map.json',mapped)
            values=['한글',''] if i==0 else ['2','값'];table='\t'.join(values)+'\n'
            texts={'body':'An opening split' if i==0 else 'word follows.','table':table,'code':'10 PRINT "한글"\n'}
            blocks=[dict(id=id,kind='code' if id=='code' else 'prose',text=text,region_ids=[id+'-region'],correction_evidence=['corrections.json#'+id+'-region'],uncertainties=[]) for id,text in texts.items()]
            records=[];results=[];images=[]
            for region in mapped['regions']:
                id=region['id'];Image.new('RGB',(20,20),'blue').save(folder/(id+'.png'));images.append(pin(folder,id+'.png'))
                raw=None
                if region['kind']!='figure':
                    for suffix,value in [('txt','raw OCR\n'),('tsv','raw positions\n')]: (folder/(id+'.'+suffix)).write_text(value)
                    write_json(folder/(id+'.settings.json'),dict(package={'sha256':recognition['sha256']},source_sha256=source['sha256'],source_index=page['source_index'],image=page['image'],region_ids=[id]))
                    results.append(dict(region_ids=[id],**{key:pin(folder,id+'.'+suffix) for key,suffix in [('text','txt'),('positions','tsv'),('settings','settings.json')]}));raw=pin(base,'ocr/'+id+'.txt')
                records.append(dict(id=id,scan=pin(base,'ocr/'+id+'.png'),raw_ocr=raw,corrected_text=texts.get(id.removesuffix('-region'))))
            write_json(folder/'evidence.json',dict(source_sha256=source['sha256'],source_index=page['source_index'],image=page['image'],runtime=pin(runtime,'runtime.json'),images=images,results=results))
            assets={r['id']:r['scan'] for r in records};code=texts['code'];length=len(code.encode());token=code.index('한글');token_end=token+len('한글'.encode())
            field=dict(field='opcode',literal='PRINT',value='PRINT',start_byte=3,end_byte=8,block_start_byte=3,block_end_byte=8,**{START:3,END:8})
            cells=[];cursor=0
            for col,value in enumerate(values):
                end=cursor+len(value.encode());cells.append(dict(column=str(col),text=value,start_byte=cursor,end_byte=end,cell_kind='blank' if value=='' else 'value'));cursor=end+1
            regional=[dict(region_id=id+'-region',block_id=id,start_byte=0,end_byte=len(text.encode()),text=text,scan=assets[id+'-region']) for id,text in texts.items()]
            common=dict(kind='source-example',figure_id='figure',table_id='table-region',code_block_ids=['code'],prose_block_ids=['body'])
            association=(dict(kind='pending-source-example',figure_id='figure',next_folio='L') if i==0 else dict(kind='cross-segment-source-example',from_segment='a',from_figure_id='figure',from_package=dict(path='archive/segments/a',manifest=specs[0]['manifest']),to_segment='b',to_folio='L',to_table_id='table-region',prose_block_ids=['body'],note='Independent source values preserved.'))
            c=dict(article_id=mapped['id'],map=pin(base,'map.json'),records=records,blocks=blocks,regional_text_ranges=regional,prose_joins=[],tables=[dict(table_id='table-region',block_id='table',columns=['0','1'],header_rows=0,rows=[dict(row_id='table:r0',region_id='table-region',scan=assets['table-region'],start_byte=0,end_byte=len(table.encode()),cells=cells)])],listing_groups=[dict(listing_id='code',block_ids=['code'],execute_verified=False)],listing_index=[dict(listing_id='code',block_id='code',region_ids=['code-region'],download='listing.txt',**{START:0,END:length})],listing_line_index=[dict(line_id='code:r1',listing_id='code',block_id='code',region_id='code-region',text=code,row_kind='numbered',printed_line=10,physical_line=1,block_start_byte=0,block_end_byte=length,scan=assets['code-region'],download='listing.txt',fields=[field],**{START:0,END:length})],logical_listing_line_index=[dict(line_id='code:n10',listing_id='code',block_id='code',printed_line=10,physical_line_ids=['code:r1'],segments=[dict(region_id='code-region',scan=assets['code-region'],**{START:0,END:length})],execute_verified=False,download='listing.txt',**{START:0,END:length})],basic_source_fields=[dict(listing_id='code',source_unit_id='code:n10',region_id='code-region',field='literal',literal='한글',start_byte=token,end_byte=token_end,scan=assets['code-region'],download='listing.txt',**{START:token,END:token_end})],source_uncertainties=[],figure_label_index=[dict(label_id='figure:l1',region_id='figure-region',literal='한글',scan=assets['figure-region'],review_crop=assets['figure-region'])],figure_structures=[dict(figure_region_id='figure-region',kind='two-cell',rows=[dict(cells=[dict(column=0,mark='small-dot'),dict(column=1,mark='empty-cell')])],scan=assets['figure-region'])],content_associations=[common,association],formula_occurrence_index=[dict(occurrence_id='formula-1',block_id='body',region_id='body-region',literal=texts['body'],start_byte=0,end_byte=len(texts['body'].encode()),scan=assets['body-region'])],segment=dict(pending_prose_join=dict(from_block='body',left_literal='split',right_literal='word',next_folio='L',separator=' ')) if i==0 else dict(incoming_prose_join=dict(to_block='body',left_literal='split',right_literal='word',separator=' ')))
            write_json(base/'corrections.json',c)
            order=['table','code','@figure','body'] if i==0 else ['body','table','code','@figure']
            recipe=dict(map=pin(base,'map.json'),corrections=pin(base,'corrections.json'),inventory=inv,runtime_directory='archive/toolchains/ocr',runtime=pin(runtime,'runtime.json'),ocr_bundles=[dict(directory='ocr',manifest=pin(base,'ocr/evidence.json'),recognition_map=recognition)],figures=[dict(id='figure',region_ids=['figure-region'],region_id='figure-region',caption=None)],content_order=[dict(type='figure' if id.startswith('@') else 'block',id=id.removeprefix('@')) for id in order],availability='partial',verification=dict(status='sample-reviewed',reviewed_region_ids=list(assets),evidence=['Synthetic complete region comparison'],uncertainties=[]),gaps=['Assembly pending.'])
            write_json(base/'recipe.json',recipe);output=root/'archive/segments'/name;build(base/'recipe.json',output,root);specs.append(dict(name=name,manifest=pin(root,output.relative_to(root).as_posix()+'/manifest.json')))
        recipe=dict(index_mode='structured-regions-v1',segments=specs,expected_source_indices=[7,19],inventory=inv,evidence=['Both synthetic source views and boundary reviewed.'],uncertainties=[],resolved_notes=[dict(segment=s,note='Assembly pending.',reason='Both views assembled.') for s in ['a','b']],prose_joins=[dict(left=dict(segment='a',block_id='body',ending='split'),right=dict(segment='b',block_id='body',opening='word'),separator=' ')],relationship_links=[dict(id='source-example',from_segment='a',from_figure_id='figure',to_segment='b',to_table_id='table-region',outgoing_association=1,incoming_association=1)])
        path=root/'archive/assembly-recipe.json';write_json(path,recipe);return path

    def test_full_rebuild_projects_typed_ranges_and_original_recognition_maps(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root)
            outputs=[root/'work/one',root/'work/two']
            for output in outputs:
                p=assemble(path,output,root);self.assertEqual(check_export(output),p)
                c=json.loads((output/'corrections.json').read_bytes());blocks={b['id']:b for b in p['blocks']}
                self.assertEqual([p['source_index'] for p in p['pages']],[7,19]);self.assertEqual([p['printed_page'] for p in p['pages']],['K','L'])
                self.assertEqual(blocks['a-body']['text'],'An opening split word follows.');self.assertNotIn('b-body',blocks)
                right=next(r for r in c['regional_text_ranges'] if r['source_segment']=='b' and r['region_id']=='b-body-region')
                self.assertEqual(right['block_id'],'a-body');self.assertEqual(right['start_byte'],len('An opening split '.encode()))
                self.assertEqual(c['tables'][0]['rows'][0]['cells'][1]['text'],'')
                self.assertEqual(c['tables'][0]['rows'][0]['cells'][1]['start_byte'],c['tables'][0]['rows'][0]['cells'][1]['end_byte'])
                token=c['basic_source_fields'][1];self.assertEqual((output/'listing.txt').read_bytes()[token[START]:token[END]].decode(),'한글')
                self.assertEqual(token['source_unit_id'],'b:code:n10');self.assertNotIn('review_crop',c['figure_label_index'][0])
                self.assertEqual(c['resolved_relationships'][0]['figure_id'],'a-figure');self.assertEqual(c['resolved_relationships'][0]['table_id'],'b-table-region')
                for s in ['a','b']:
                    self.assertEqual((output/f'segments/{s}/ocr/recognition-map.json').read_bytes(),(root/f'archive/segments/{s}/ocr/recognition-map.json').read_bytes())
                    self.assertEqual((output/f'segments/{s}/corrections.json').read_bytes(),(root/f'archive/segments/{s}/corrections.json').read_bytes())
                with zipfile.ZipFile(output/'raw-ocr.zip') as z:self.assertIn('segments/a/ocr/recognition-map.json',z.namelist())
            files=lambda folder:{p.relative_to(folder).as_posix():p.read_bytes() for p in folder.rglob('*') if p.is_file()}
            self.assertEqual(files(outputs[0]),files(outputs[1]))

    def test_boundary_coverage_relationship_and_unknown_index_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);recipe=json.loads(path.read_bytes());segments=[read_segment(root/s['manifest']['path'].removesuffix('/manifest.json'),s['manifest']) for s in recipe['segments']]
            for fault in ['coverage','join','relationship','literal','unknown index','UTF-8 split','physical unit','blank','execution group']:
                r=deepcopy(recipe);s=deepcopy(segments)
                if fault=='coverage':r['expected_source_indices'].reverse()
                elif fault=='join':r['prose_joins']=[]
                elif fault=='relationship':r['relationship_links']=[]
                elif fault=='literal':s[0][1]['basic_source_fields'][0]['literal']='다른'
                elif fault=='unknown index':s[0][1]['unprojected_data']=[{'critical':True}]
                elif fault=='UTF-8 split':s[0][1]['basic_source_fields'][0][START]+=1
                elif fault=='physical unit':s[0][1]['logical_listing_line_index'][0]['physical_line_ids']=['missing']
                elif fault=='execution group':s[0][1]['listing_groups'][0]['execute_verified']=True
                else:s[0][1]['tables'][0]['rows'][0]['cells'][1]['text']='invented'
                with self.subTest(fault=fault),self.assertRaises(ValueError):project(r,s)

    def test_inventory_and_outer_projection_tampering_reject(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=self.fixture(root);recipe=json.loads(path.read_bytes())
            bad=deepcopy(recipe);bad['inventory']['queue']['sha256']='0'*64;write_json(path,bad)
            with self.assertRaisesRegex(ValueError,'inventory'):assemble(path,root/'work/bad',root)
            write_json(path,recipe);out=root/'work/valid';assemble(path,out,root)
            c=json.loads((out/'corrections.json').read_bytes());c['tables'][0]['rows'][0]['cells'][0]['text']='tampered';write_json(out/'corrections.json',c)
            # Rehash every outer reference: retained source projection still rejects.
            p=json.loads((out/'article.json').read_bytes());p['corrections']=[pin(out,'corrections.json')];write_json(out/'article.json',p)
            manifest=json.loads((out/'manifest.json').read_bytes());manifest['files']=[pin(out,r['path']) for r in manifest['files']];write_json(out/'manifest.json',manifest)
            with self.assertRaisesRegex(ValueError,'correction projection'):check_export(out)

    def test_rehashed_segment_still_checks_image_and_original_ocr_map_binding(self):
        for fault in ['image','recognition map']:
            with self.subTest(fault=fault),tempfile.TemporaryDirectory() as temp:
                root=Path(temp);path=self.fixture(root);recipe=json.loads(path.read_bytes())
                folder=root/'archive/segments/a';p=json.loads((folder/'article.json').read_bytes())
                raw=next(r for r in p['raw_ocr'] if r['region_ids']==['code-region'])
                settings=json.loads((folder/raw['settings']['path']).read_bytes())
                if fault=='image':settings['image']['sha256']='0'*64
                else:settings['package']['sha256']=pin(folder,'map.json')['sha256']
                write_json(folder/raw['settings']['path'],settings)
                raw['settings']=pin(folder,raw['settings']['path']);write_json(folder/'article.json',p)
                manifest=json.loads((folder/'manifest.json').read_bytes())
                manifest['files']=[pin(folder,r['path']) for r in manifest['files']];write_json(folder/'manifest.json',manifest)
                with self.assertRaises(ValueError):read_segment(folder,pin(root,'archive/segments/a/manifest.json'))


if __name__=='__main__':unittest.main()
