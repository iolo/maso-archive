"""Occurrence-fidelity regressions for mixed printed BASIC and hex listings."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

from tools.pdf_restore.assemble import text_bytes
from tools.pdf_restore.table_literal_assembly import project, installed
from tools.pdf_restore import assemble as base_assembly
from tools.pdf_restore.assembly_indexes import START as S, END as E, block_ranges
from tools.pdf_restore.package import page_transform


def fixture():
    template = json.loads((Path(__file__).parents[1]/'examples/pdf-article.json').read_bytes())
    pin = lambda path: dict(path=path, sha256='0'*64, bytes=0)
    sources = []
    for i in range(2):
        p = deepcopy(template)
        page = dict(pdf_index=i, pdf_page=i+1, printed_page=str(i+7), width_pt=100,
                    height_pt=200, rotation=0, MediaBox=[0,0,100,200], CropBox=[0,0,100,200])
        page['pdf_to_upright_normalized'] = page_transform(page)
        blocks = [dict(id='prose', kind='prose', text='Ω Ω', region_ids=['prose'])]
        if i == 0:
            blocks.append(dict(id='table',kind='prose',text='가\t\n가\t나',region_ids=['table']))
        blocks.append(dict(id='listing-caption',kind='caption',text='리스트 2',region_ids=['listing-caption']))
        if i == 0:
            blocks.append(dict(id='basic', kind='code',
                text='10 DATA L,L,"-",13\n  3,00\n20 PRINT "Ω","Ω"\n', region_ids=['basic']))
        blocks.extend([dict(id='hex', kind='code',
            text='7BE0- 00 01 00 00 01\n7BE0- 00 00\n' if i == 0 else '7BE0- 00\n',
            region_ids=['hex']), dict(id='caption', kind='caption', text='원본 Ω', region_ids=['caption'])])
        for b in blocks:
            b.update(correction_evidence=['corrections.json#'+b['id']], uncertainties=[])
        ids = [b['id'] for b in blocks]+['image']
        assets = {id:pin(id+'.png') for id in ids}
        p.update(pages=[page], regions=[dict(id=id, pdf_index=i,
            kind='figure' if id == 'image' else next(b['kind'] for b in blocks if b['id'] == id),
            bbox=[0,n/8,1,(n+1)/8], notes='Reviewed synthetic source') for n,id in enumerate(ids)],
            excluded_regions=[], blocks=blocks, content_order=[dict(type='block',id=b['id']) for b in blocks]+
            [dict(type='figure',id='figure')], figures=[dict(id='figure',region_ids=['image'],
            asset=assets['image'],caption='원본 Ω')], region_assets=[dict(region_id=id,asset=a) for id,a in assets.items()],
            corrections=[pin('corrections.json')], gaps=[], availability='partial',
            mapping=dict(status='mapped',evidence=['Synthetic source reviewed'],uncertainties=[]),
            verification=dict(status='sample-reviewed',reviewed_region_ids=ids,evidence=['Reviewed'],uncertainties=[]))
        keys = ('text_index','regional_text_index','text_review_items','text_review_notes','prose_joins',
                'tables','table_cell_index','table_row_index','inline_example_index','listing_index',
                'regional_listing_index','listing_line_index','logical_listing_line_index',
                'quoted_source_index','basic_data_statements','basic_data_field_index',
                'hex_dump_row_index','hex_dump_address_index','hex_dump_field_index','listing_source_uncertainties')
        c = {k:[] for k in keys}
        c.update(manual_postproduction=dict(literal_table_source_fields_format='v1'), blocks=deepcopy(blocks),
            records=[dict(id=id,scan=a,raw_ocr=None,block_ids=[b['id'] for b in blocks if id in b['region_ids']])
                     for id,a in assets.items()],
            listing_groups=[dict(listing_id=b['id'],block_ids=[b['id']],execute_verified=False,
                                 execution_verified=False,source_program_complete=False)
                            for b in blocks if b['kind']=='code'],
            figure_sequence=[dict(figure_id='figure',region_id='image',scan=assets['image'])],
            image_preservation=[dict(region_id='image',scan=assets['image'])],
            caption_links=[dict(figure_id='figure',figure_region_id='image',
                                caption_block_id='caption',caption_region_id='caption')],
            future_metadata={'opaque':['Ω',3]})
        bounds = block_ranges(p)
        for b in blocks:
            a,z = bounds[b['id']]
            row = dict(block_id=b['id'],region_id=b['id'],scan=assets[b['id']],
                       download='article.txt',**{S:a,E:z},transcription_excerpt=b['text'])
            c['regional_text_index'].append(row)
            c['text_review_items'].append(deepcopy(row))
            c['text_index'].append(dict(block_id=b['id'],region_ids=[b['id']],
                scans=[assets[b['id']]],download='article.txt',**{S:a,E:z}))
        c['inline_example_index'] = [dict(c['regional_text_index'][0],transcription_excerpt='Ω',
            source_bytes='unverified',execution_verified=False,**{S:3,E:5})]
        cap=next(r for r in c['regional_text_index'] if r['block_id']=='listing-caption')
        c['listing_caption_links']=[dict(cap,caption_block_id='listing-caption',
            caption_region_id='listing-caption',listing_id='hex',block_ids=['hex'],figure_ids=['figure'])]
        if i==0:
            c['tables']=[dict(id='source-table',block_id='table',region_id='table',header=None,
                             rows=[['가',''],['가','나']])]
            cursor=bounds['table'][0]
            for nr,values in enumerate([['가',''],['가','나']],1):
                start=cursor
                for nc,value in enumerate(values,1):
                    z=cursor+len(value.encode())
                    c['table_cell_index'].append(dict(table_id='source-table',block_id='table',
                        region_id='table',scan=assets['table'],row=nr,column=nc,header=False,
                        text=value,blank=value=='',download='article.txt',**{S:cursor,E:z}))
                    cursor=z+(nc<len(values))
                c['table_row_index'].append(dict(table_id='source-table',block_id='table',
                    region_id='table',scan=assets['table'],row=nr,header=False,
                    download='article.txt',**{S:start,E:cursor}))
                cursor+=1
        offset, article_ordinal, counts = 0, 0, Counter()
        for b in (b for b in blocks if b['kind']=='code'):
            start = offset
            logical = None
            for ordinal,line in enumerate(b['text'].splitlines(True),1):
                a,z = offset,offset+len(line.encode())
                article_ordinal += 1
                part = dict(region_id=b['id'],scan=assets[b['id']],**{S:a,E:z})
                row = dict(part,block_id=b['id'],listing_id=b['id'],physical_line=ordinal,
                    article_physical_line=article_ordinal,line_id=f'{b["id"]}:physical:{ordinal}',
                    download='listing.txt',segments=[deepcopy(part)],text=line[:-1],tokens=line.split(),
                    source_bytes='unverified',execution_verified=False)
                if b['id']=='hex':
                    address = line[:4];counts[address] += 1
                    uid = f'hex:address:{address}:{counts[address]}'
                    row.update(printed_line=None,printed_line_visible=False,row_kind='unnumbered',source_unit_id=uid)
                    common = dict(block_id='hex',listing_id='hex',region_id='hex',scan=assets['hex'],
                        source_line_id=row['line_id'],unit_id=uid,address_literal=address,
                        occurrence=counts[address],download='listing.txt',source_bytes='unverified',execution_verified=False)
                    values = line[6:].split()
                    unit = dict(common,**{S:a,E:z},text=line,source_parts=[row['line_id']],
                                segments=[deepcopy(part)],hex_literals=values,value_count=len(values))
                    c['hex_dump_row_index'].append(unit)
                    c['hex_dump_address_index'].append(dict(common,**{S:a,E:a+4},text=address,kind='printed-hex-address'))
                    for n,v in enumerate(values,1):
                        lo=a+6+(n-1)*3
                        c['hex_dump_field_index'].append(dict(common,field=n,kind='printed-hex-literal',text=v,**{S:lo,E:lo+2}))
                else:
                    number = int(line.split()[0]) if line[0].isdigit() else None
                    row.update(printed_line=number,printed_line_visible=number is not None,
                               row_kind='numbered' if number is not None else 'wrapped-continuation')
                    if number is not None:
                        logical = dict(block_id='basic',listing_id='basic',printed_line=number,
                            occurrence=1,logical_line=len(c['logical_listing_line_index'])+1,
                            line_id=f'basic:number:{number}',download='listing.txt',
                            **{S:a,E:z},source_parts=[],segments=[],text='',source_bytes='unverified',execution_verified=False)
                        c['logical_listing_line_index'].append(logical)
                    else:
                        row['continues_printed_line']=logical['printed_line']
                    row['logical_line_id']=logical['line_id']
                    logical[E]=z;logical['text']+=line;logical['source_parts'].append(row['line_id'])
                    logical['segments'].append(deepcopy(part))
                c['listing_line_index'].append(row);offset=z
            c['listing_index'].append(dict(block_id=b['id'],region_ids=[b['id']],download='listing.txt',**{S:start,E:offset}))
            c['regional_listing_index'].append(dict(block_id=b['id'],listing_id=b['id'],region_id=b['id'],
                scan=assets[b['id']],download='listing.txt',**{S:start,E:offset},transcription_excerpt=b['text']))
        def pieces(u,a,z):
            return [dict(region_id=s['region_id'],scan=s['scan'],**{S:max(a,s[S]),E:min(z,s[E])})
                    for s in u['segments'] if max(a,s[S])<min(z,s[E])]
        for u in c['logical_listing_line_index']:
            literals = ['"-"'] if u['printed_line']==10 else ['"Ω"','"Ω"']
            cursor=0
            for n,t in enumerate(literals,1):
                a=u['text'].index(t,cursor);cursor=a+len(t)
                lo=u[S]+len(u['text'][:a].encode());hi=lo+len(t.encode())
                c['quoted_source_index'].append(dict(block_id='basic',listing_id='basic',
                    logical_line_id=u['line_id'],printed_line=u['printed_line'],literal_ordinal=n,
                    download='listing.txt',**{S:lo,E:hi},transcription_excerpt=t,contents=t[1:-1],
                    closing_quote_visible=True,segments=pieces(u,lo,hi),source_bytes='unverified',
                    execution_verified=False,kind='printed-source-string'))
            if u['printed_line']!=10:
                continue
            values=['L','L','"-"','13\n  3','00']
            c['basic_data_statements'].append(dict(block_id='basic',listing_id='basic',
                logical_line_id=u['line_id'],printed_line=10,download='listing.txt',**{S:u[S],E:u[E]},
                transcription_excerpt=u['text'],literal_values=values,value_count=5,
                source_parts=deepcopy(u['source_parts']),segments=deepcopy(u['segments']),
                source_bytes='unverified',execution_verified=False))
            cursor=8
            for n,t in enumerate(values,1):
                a=u['text'].index(t,cursor);cursor=a+len(t)
                lo=u[S]+len(u['text'][:a].encode());hi=lo+len(t.encode())
                c['basic_data_field_index'].append(dict(block_id='basic',listing_id='basic',
                    logical_line_id=u['line_id'],printed_line=10,field=n,text=t,
                    kind='bare-letter-source' if n<3 else 'quoted-source-string' if n==3 else 'printed-decimal-literal',
                    download='listing.txt',**{S:lo,E:hi},segments=pieces(u,lo,hi),
                    source_bytes='unverified',execution_verified=False))
        sources.append((p,c))
    recipe=dict(index_mode='wrapped-listing-v1',segments=[dict(name=n,manifest=pin(n+'/manifest.json'))
        for n in ('opening','ending')],expected_pdf_pages=[1,2],prose_joins=[],wrapped_listing_joins=[],
        evidence=['Complete synthetic source reviewed'],uncertainties=['Bytes unverified'],resolved_notes=[])
    return recipe,sources


class TableLiteralTests(unittest.TestCase):
    def test_tables_split_digits_and_all_source_occurrences_survive(self):
        recipe,sources=fixture();before=deepcopy(sources);p,c=project(recipe,sources)
        self.assertEqual(sources,before)
        self.assertEqual(text_bytes(p)[1],b''.join(text_bytes(p)[1] for p,_ in sources))
        self.assertEqual(c['literal_table_source_fields_format'],'v1')
        self.assertEqual(c['basic_data_statements'][0]['literal_values'],['L','L','"-"','13\n  3','00'])
        self.assertEqual(c['basic_data_field_index'][3]['text'],'13\n  3')
        self.assertEqual(len(c['basic_data_field_index'][3]['segments']),2)
        self.assertEqual([r['text'] for r in c['table_cell_index']],['가','','가','나'])
        self.assertEqual([r['table_id'] for r in c['table_cell_index']],['opening-source-table']*4)
        self.assertEqual(sum(r['blank'] for r in c['table_cell_index']),1)
        self.assertEqual([r['article_physical_line'] for r in c['listing_line_index']],list(range(1,7)))
        self.assertEqual([r['logical_line'] for r in c['logical_listing_line_index']],[1,2])
        self.assertEqual(c['listing_caption_links'][1]['figure_ids'],['ending-figure'])
        self.assertEqual(c['segments'][0]['original_metadata']['future_metadata'],{'opaque':['Ω',3]})

    def test_blank_cell_cannot_move_to_another_empty_occurrence(self):
        recipe,sources=fixture();r=sources[0][1]['table_cell_index'][1];r[S]=r[E]=sources[0][1]['table_row_index'][1][E]
        with self.assertRaisesRegex(ValueError,'table cell occurrence'):project(recipe,sources)

    def test_repeated_label_cannot_reuse_first_source_occurrence(self):
        recipe,sources=fixture();rr=sources[0][1]['table_cell_index']
        rr[2][S]=rr[0][S];rr[2][E]=rr[0][E]
        with self.assertRaisesRegex(ValueError,'table cell occurrence'):project(recipe,sources)

    def test_missing_or_extra_table_fields_and_rows_rejected(self):
        for key in ('table_cell_index','table_row_index'):
            for change in ('remove','duplicate'):
                with self.subTest(key=key,change=change):
                    recipe,sources=fixture();rows=sources[0][1][key]
                    if change=='remove':rows.pop()
                    else:rows.append(deepcopy(rows[-1]))
                    with self.assertRaises(ValueError):project(recipe,sources)

    def test_split_digit_field_must_keep_actual_text_and_scan_parts(self):
        for change in ('normalize','wrong-scan','missing-span'):
            recipe,sources=fixture();r=sources[0][1]['basic_data_field_index'][3]
            if change=='normalize':r['text']='133'
            elif change=='wrong-scan':r['segments'][1]['scan']=sources[0][0]['figures'][0]['asset']
            else:r['segments'].pop()
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,sources)

    def test_caption_links_exhaust_headings_and_keep_exact_owners(self):
        for change in ('missing','block','figure','range','order'):
            recipe,sources=fixture();c=sources[0][1];r=c['listing_caption_links'][0]
            if change=='missing':c['listing_caption_links']=[]
            elif change=='block':r['block_ids']=['basic']
            elif change=='figure':r['figure_ids']=['unknown']
            elif change=='range':r[S]+=1
            else:r['figure_ids']=['figure','figure']
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,sources)

    def test_wrong_table_scan_and_false_byte_or_execution_claims_rejected(self):
        for change in ('scan','bytes','execution'):
            recipe,sources=fixture();r=sources[0][1]['table_cell_index'][0]
            if change=='scan':r['scan']=sources[0][0]['figures'][0]['asset']
            elif change=='bytes':r['encoded_bytes']=[0]
            else:r['execution_verified']=True
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,sources)

    def test_repeated_hex_fields_and_short_rows_cannot_be_repaired(self):
        for change in ('repeat','padding','byteclaim'):
            recipe,sources=fixture();c=sources[0][1]
            if change=='repeat':
                rr=c['hex_dump_field_index'];rr[2][S]=rr[0][S];rr[2][E]=rr[0][E]
            elif change=='padding':
                c['hex_dump_row_index'][1]['hex_literals']=['00']*8
                c['hex_dump_row_index'][1]['value_count']=8
            else:c['hex_dump_field_index'][0]['source_bytes']='verified'
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,sources)

    def test_uniform_opt_in_and_supported_mode_required(self):
        for change in ('mixed','version','mode','basic','old-literals'):
            recipe,sources=fixture()
            if change=='mixed':sources[1][1].pop('manual_postproduction')
            elif change=='version':sources[1][1]['manual_postproduction']['literal_table_source_fields_format']='v2'
            elif change=='mode':recipe['index_mode']='namespaced-v1'
            elif change=='basic':sources[0][1]['basic_source_fields_format']='v1'
            else:sources[0][1]['manual_postproduction']['literal_source_fields_format']='v1'
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,sources)

    def test_cross_segment_joins_rejected_before_source_projection(self):
        recipe,sources=fixture();recipe['wrapped_listing_joins']=[{'unreviewed':'join'}]
        with self.assertRaisesRegex(ValueError,'without cross-segment joins'):project(recipe,sources)

    def test_adapter_restores_baseline_projector_even_after_exception(self):
        baseline=base_assembly.project
        with self.assertRaisesRegex(RuntimeError,'probe'):
            with installed():
                self.assertIs(base_assembly.project,project)
                raise RuntimeError('probe')
        self.assertIs(base_assembly.project,baseline)

    def test_legacy_output_unchanged_without_opt_in(self):
        recipe,sources=fixture()
        for _,c in sources:c.pop('manual_postproduction')
        self.assertEqual(project(recipe,sources),base_assembly.project(recipe,sources))


if __name__ == '__main__':
    unittest.main()
