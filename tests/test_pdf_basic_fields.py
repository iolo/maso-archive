"""Literal BASIC source occurrences, quoted blanks, Unicode and unverified DATA."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from tools.pdf_restore.assemble import project, text_bytes
from tools.pdf_restore.assembly_indexes import block_ranges
from tools.pdf_restore.package import page_transform


def fixture():
    template = json.loads((Path(__file__).parents[1]/'examples/pdf-article.json').read_bytes())
    pin = lambda path: dict(path=path,sha256='0'*64,bytes=0)
    originals=[]
    plans=[('10 DATA 00, FF, 00, FF, 00, FF, 00, FF, 999\n20 PRINT "Ω\n  a"\n',
            [(10,'machine',['00','FF','00','FF','00','FF','00','FF','999'])]),
           ('30 DATA "  ", "Ω", "Ω", "x",\n  "y"\n40 DATA - 1, 2\n50 DATA C8.\n  O6D8\n',
            [(30,'panel',['"  "','"Ω"','"Ω"','"x"','"y"']),
             (40,'move',['- 1','2']),(50,'music',['C8.\n  O6D8'])])]
    for i,(code,declared) in enumerate(plans):
        p=deepcopy(template);page=dict(pdf_index=i,pdf_page=i+1,printed_page=str(i+7),
            width_pt=100,height_pt=200,rotation=0,MediaBox=[0,0,100,200],CropBox=[0,0,100,200])
        page['pdf_to_upright_normalized']=page_transform(page)
        blocks=[]
        if i==0:blocks.append(dict(id='table',kind='prose',text='가\t\n가\t나',region_ids=['table'],
            correction_evidence=['corrections.json#table'],uncertainties=[]))
        blocks.append(dict(id='code',kind='code',text=code,region_ids=['code'],
            correction_evidence=['corrections.json#code'],uncertainties=[]))
        ids=[b['id'] for b in blocks]+['image'];assets={id:pin(id+'.png') for id in ids}
        p.update(pages=[page],regions=[dict(id=id,pdf_index=i,kind='figure' if id=='image' else
            'code' if id=='code' else 'prose',bbox=[0,n/4,1,(n+1)/4],notes='Observed synthetic source')
            for n,id in enumerate(ids)],excluded_regions=[],blocks=blocks,
            mapping=dict(status='mapped',evidence=['Complete synthetic source'],uncertainties=[]),
            figures=[dict(id='figure',region_ids=['image'],asset=assets['image'],caption=None)],
            content_order=[dict(type='block',id=b['id']) for b in blocks]+[dict(type='figure',id='figure')],
            region_assets=[dict(region_id=id,asset=a) for id,a in assets.items()],
            corrections=[pin('corrections.json')],gaps=[],availability='partial',
            verification=dict(status='sample-reviewed',reviewed_region_ids=ids,evidence=['Reviewed'],uncertainties=[]))
        c=dict(basic_source_fields_format='v1',blocks=deepcopy(blocks),records=[dict(id=id,scan=a,
            raw_ocr=None,block_ids=[b['id'] for b in blocks if id in b['region_ids']]) for id,a in assets.items()],
            text_index=[],regional_text_index=[],text_review_items=[],text_review_notes=[],
            prose_joins=[],tables=[],table_cell_index=[],table_row_index=[],caption_links=[],
            inline_example_index=[],figure_sequence=[dict(figure_id='figure',region_id='image',scan=assets['image'])],
            image_preservation=[dict(region_id='image',scan=assets['image'])],
            listing_groups=[dict(listing_id='program',block_ids=['code'],execute_verified=False)],
            listing_index=[dict(block_id='code',region_ids=['code'],download='listing.txt',
                utf8_byte_start=0,utf8_byte_end_exclusive=len(code.encode()))],
            listing_line_index=[],logical_listing_line_index=[],regional_listing_index=[],
            listing_source_uncertainties=[],quoted_source_index=[],graphic_string_index=[],music_string_index=[],
            basic_data_statements=[],basic_data_field_index=[],basic_machine_data_rows=[],
            basic_machine_data_field_index=[],basic_hex_data_rows=[],basic_numeric_data_rows=[],
            basic_panel_data_rows=[],basic_music_data_rows=[],future_metadata={'unknown':[1,'한글']})
        bounds=block_ranges(p)
        for b in blocks:
            a,z=bounds[b['id']];r=dict(block_id=b['id'],region_id=b['id'],scan=assets[b['id']],
                download='article.txt',utf8_byte_start=a,utf8_byte_end_exclusive=z,transcription_excerpt=b['text'])
            c['regional_text_index'].append(r);c['text_review_items'].append(deepcopy(r))
            c['text_index'].append(dict(block_id=b['id'],region_ids=[b['id']],scans=[assets[b['id']]],
                download='article.txt',utf8_byte_start=a,utf8_byte_end_exclusive=z))
        if i==0:
            c['tables']=[dict(id='t',block_id='table',region_id='table',header=None,rows=[['가',''],['가','나']])]
            cursor=0
            for nr,values in enumerate([['가',''],['가','나']],1):
                a=cursor
                for nc,v in enumerate(values,1):
                    z=cursor+len(v.encode());c['table_cell_index'].append(dict(table_id='t',block_id='table',
                        region_id='table',scan=assets['table'],row=nr,column=nc,header=False,text=v,
                        blank=v=='',download='article.txt',utf8_byte_start=cursor,utf8_byte_end_exclusive=z));cursor=z+(nc<2)
                c['table_row_index'].append(dict(table_id='t',block_id='table',region_id='table',scan=assets['table'],
                    row=nr,header=False,download='article.txt',utf8_byte_start=a,utf8_byte_end_exclusive=cursor));cursor+=1
        cursor=0;u=None
        for ordinal,line in enumerate(code.splitlines(True),1):
            n=int(line.split()[0]) if line[0].isdigit() else None;z=cursor+len(line.encode())
            part=dict(region_id='code',scan=assets['code'],utf8_byte_start=cursor,utf8_byte_end_exclusive=z)
            r=dict(**part,block_id='code',listing_id='program',physical_line=ordinal,article_physical_line=ordinal,
                printed_line=n,printed_line_visible=n is not None,row_kind='numbered' if n else 'wrapped-continuation',
                line_id=f'row:{ordinal}',download='listing.txt',segments=[deepcopy(part)],text=line[:-1],
                tokens=line.split(),source_bytes='unverified',execution_verified=False)
            if n is not None:
                u=dict(block_id='code',listing_id='program',printed_line=n,occurrence=1,line_id=f'number:{n}',
                    download='listing.txt',utf8_byte_start=cursor,utf8_byte_end_exclusive=z,source_parts=[],segments=[],
                    text='',source_bytes='unverified',execution_verified=False);c['logical_listing_line_index'].append(u)
            else:r['continues_printed_line']=u['printed_line']
            r['logical_line_id']=u['line_id'];u['utf8_byte_end_exclusive']=z;u['source_parts'].append(r['line_id']);u['segments'].append(part);u['text']+=line;c['listing_line_index'].append(r);cursor=z
        c['regional_listing_index']=[dict(block_id='code',listing_id='program',region_id='code',scan=assets['code'],
            download='listing.txt',utf8_byte_start=0,utf8_byte_end_exclusive=len(code.encode()),transcription_excerpt=code)]
        def pieces(u,a,z):return [dict(region_id=s['region_id'],scan=s['scan'],utf8_byte_start=max(a,s['utf8_byte_start']),
            utf8_byte_end_exclusive=min(z,s['utf8_byte_end_exclusive'])) for s in u['segments'] if max(a,s['utf8_byte_start'])<min(z,s['utf8_byte_end_exclusive'])]
        for u in c['logical_listing_line_index']:
            # Quotes are independently selected literal fixture occurrences.
            strings=['"Ω\n  a"'] if u['printed_line']==20 else ['"  "','"Ω"','"Ω"','"x"','"y"'] if u['printed_line']==30 else []
            cursor=0
            for ordinal,s in enumerate(strings,1):
                start=u['text'].index(s,cursor);cursor=start+len(s);a=u['utf8_byte_start']+len(u['text'][:start].encode());z=a+len(s.encode())
                c['quoted_source_index'].append(dict(block_id='code',listing_id='program',printed_line=u['printed_line'],literal_ordinal=ordinal,
                    logical_line_id=u['line_id'],download='listing.txt',utf8_byte_start=a,utf8_byte_end_exclusive=z,
                    transcription_excerpt=s,contents=s[1:-1],closing_quote_visible=True,segments=pieces(u,a,z),
                    kind='graphic-source-string' if u['printed_line']==30 else 'printed-source-string',source_bytes='unverified',execution_verified=False))
        c['graphic_string_index']=[deepcopy(r) for r in c['quoted_source_index'] if r['kind']=='graphic-source-string']
        for number,category,values in declared:
            u=next(u for u in c['logical_listing_line_index'] if u['printed_line']==number)
            common=dict(block_id='code',listing_id='program',logical_line_id=u['line_id'],printed_line=number,
                category=category,download='listing.txt',utf8_byte_start=u['utf8_byte_start'],utf8_byte_end_exclusive=u['utf8_byte_end_exclusive'],
                source_parts=u['source_parts'],segments=u['segments'],transcription_excerpt=u['text'],literal_values=values,
                value_count=len(values),source_bytes='unverified',checksum_verified=False,execution_verified=False)
            c['basic_data_statements'].append(common);cursor=u['text'].index('DATA ')+5;ff=[]
            for ordinal,v in enumerate(values,1):
                start=u['text'].index(v,cursor);cursor=start+len(v);a=u['utf8_byte_start']+len(u['text'][:start].encode());z=a+len(v.encode())
                kind='hex-literal' if category=='machine' and ordinal<=8 else 'printed-decimal-checksum' if category=='machine' else 'quoted-panel-string' if category=='panel' else 'unquoted-music-source' if category=='music' else 'printed-decimal-literal'
                r=dict(block_id='code',listing_id='program',logical_line_id=u['line_id'],printed_line=number,field=ordinal,
                    category=category,kind=kind,text=v,download='listing.txt',utf8_byte_start=a,utf8_byte_end_exclusive=z,
                    segments=pieces(u,a,z),source_bytes='unverified',checksum_verified=False,execution_verified=False)
                ff.append(r);c['basic_data_field_index'].append(r)
            if category=='machine':
                c['basic_machine_data_rows'].append(dict(common,region_id='code',scan=assets['code'],hex_literals=values[:8],printed_checksum=values[8]))
                c['basic_machine_data_field_index'].extend(deepcopy(ff))
            else:c[{'panel':'basic_panel_data_rows','music':'basic_music_data_rows','move':'basic_numeric_data_rows'}[category]].append(deepcopy(common))
        originals.append((p,c))
    recipe=dict(index_mode='wrapped-listing-v1',segments=[dict(name=n,manifest=pin(n+'/manifest.json')) for n in ('opening','ending')],
        expected_pdf_pages=[1,2],prose_joins=[],wrapped_listing_joins=[],evidence=['Complete observed source'],uncertainties=['Bytes unverified'],resolved_notes=[])
    return recipe,originals


class BasicFieldTests(unittest.TestCase):
    def test_all_source_fields_project_without_mutation_or_checksum_repair(self):
        recipe,sources=fixture();before=deepcopy(sources);p,c=project(recipe,sources)
        self.assertEqual(sources,before);self.assertEqual(text_bytes(p)[1],b''.join(text_bytes(p)[1] for p,_ in sources))
        self.assertEqual(len(c['quoted_source_index']),6);self.assertEqual(len(c['basic_data_field_index']),17)
        self.assertEqual(c['basic_machine_data_rows'][0]['printed_checksum'],'999')
        self.assertEqual(c['graphic_string_index'][0]['contents'],'  ')
        self.assertEqual(c['basic_music_data_rows'][0]['literal_values'],['C8.\n  O6D8'])
        self.assertEqual(c['segments'][0]['original_metadata']['future_metadata'],{'unknown':[1,'한글']})
        self.assertEqual(sum(r['blank'] for r in c['table_cell_index']),1)
        self.assertEqual([r['article_physical_line'] for r in c['listing_line_index']],list(range(1,9)))
    def test_repeated_quote_cannot_be_reassigned_to_an_identical_occurrence(self):
        recipe,sources=fixture();c=sources[1][1];a,z=c['quoted_source_index'][1:3]
        for key in ('utf8_byte_start','utf8_byte_end_exclusive','segments'):z[key]=deepcopy(a[key])
        with self.assertRaisesRegex(ValueError,'quoted source occurrence'):project(recipe,sources)
    def test_missing_data_field_and_false_checksum_claim_rejected(self):
        for field in ('missing','verified'):
            recipe,sources=fixture();c=sources[0][1]
            if field=='missing':c['basic_data_field_index'].pop()
            else:c['basic_data_field_index'][-1]['checksum_verified']=True
            with self.assertRaisesRegex(ValueError,'BASIC DATA'):project(recipe,sources)
    def test_wrong_scan_on_unicode_field_is_rejected(self):
        recipe,sources=fixture();sources[1][1]['quoted_source_index'][1]['segments'][0]['scan']=sources[1][0]['figures'][0]['asset']
        with self.assertRaisesRegex(ValueError,'source segments'):project(recipe,sources)
    def test_blank_table_cell_must_keep_its_actual_source_occurrence(self):
        recipe,sources=fixture();r=sources[0][1]['table_cell_index'][1];r['utf8_byte_start']=r['utf8_byte_end_exclusive']=0
        with self.assertRaisesRegex(ValueError,'table cell occurrence'):project(recipe,sources)
    def test_mixed_opt_in_rejected_and_legacy_output_unchanged(self):
        recipe,sources=fixture();sources[1][1].pop('basic_source_fields_format')
        with self.assertRaisesRegex(ValueError,'uniformly opted-in'):project(recipe,sources)
        sources[0][1].pop('basic_source_fields_format');p,c=project(recipe,sources)
        self.assertNotIn('basic_data_field_index',c);self.assertEqual(len(c['listing_line_index']),8)
    def test_field_span_cannot_split_utf8_or_change_negative_decimal(self):
        for kind in ('utf8','decimal'):
            recipe,sources=fixture();c=sources[1][1]
            if kind=='utf8':c['quoted_source_index'][1]['utf8_byte_end_exclusive']-=2
            else:next(r for r in c['basic_data_field_index'] if r['category']=='move')['text']='1'
            with self.assertRaises(ValueError):project(recipe,sources)

    def test_cross_panel_uncertainty_requires_exact_ordered_source_scans(self):
        recipe,sources=fixture();p,c=sources[0];S='utf8_byte_start';E='utf8_byte_end_exclusive'
        asset=dict(path='continuation.png',sha256='1'*64,bytes=1)
        region=deepcopy(next(r for r in p['regions'] if r['id']=='code'))
        region.update(id='continuation',bbox=[0,.375,1,.5])
        next(r for r in p['regions'] if r['id']=='code')['bbox']=[0,.25,1,.375]
        p['regions'].insert(-1,region);p['region_assets'].append(dict(region_id='continuation',asset=asset))
        p['verification']['reviewed_region_ids'].append('continuation')
        for blocks in (p['blocks'],c['blocks']):
            block=next(b for b in blocks if b['id']=='code')
            block['region_ids'].append('continuation');block['correction_evidence'].append('corrections.json#continuation')
        c['records'].append(dict(id='continuation',scan=asset,raw_ocr=None,block_ids=['code']))
        physical=c['listing_line_index'][-1];boundary=physical[S]
        physical.update(region_id='continuation',scan=asset)
        physical['segments'][0].update(region_id='continuation',scan=asset)
        unit=c['logical_listing_line_index'][-1]
        unit['segments'][-1].update(region_id='continuation',scan=asset)
        c['quoted_source_index'][0]['segments'][-1].update(region_id='continuation',scan=asset)
        for key in ('regional_text_index','text_review_items','regional_listing_index'):
            row=next(r for r in c[key] if r['block_id']=='code');a,z=row[S],row[E]
            split=a+boundary if key!='regional_listing_index' else boundary
            data=text_bytes(p)[0 if key!='regional_listing_index' else 1]
            tail=deepcopy(row);row[E]=split;row['transcription_excerpt']=data[a:split].decode()
            tail.update(region_id='continuation',scan=asset,**{S:split},transcription_excerpt=data[split:z].decode())
            c[key].append(tail)
        row=next(r for r in c['text_index'] if r['block_id']=='code')
        row['region_ids'].append('continuation');row['scans'].append(asset)
        c['listing_index'][0]['region_ids'].append('continuation')
        note=dict(block_id='code',listing_id='program',logical_line_id=unit['line_id'],printed_line=20,
            region_id='code',scan=unit['segments'][0]['scan'],scans=[s['scan'] for s in unit['segments']],
            download='listing.txt',**{S:unit[S],E:unit[E]},transcription_excerpt=unit['text'])
        c['listing_source_uncertainties']=[note]
        combined,correction=project(recipe,sources)
        self.assertEqual(correction['listing_source_uncertainties'][0]['scans'][1]['path'],
                         'segments/opening/continuation.png')
        note['scans'].reverse()
        with self.assertRaisesRegex(ValueError,'scan/region'):project(recipe,sources)


if __name__=='__main__':unittest.main()
