"""Occurrence-fidelity regressions for mixed printed BASIC and hex listings."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

from tools.pdf_restore.assemble import project, text_bytes
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
            blocks.append(dict(id='basic', kind='code',
                text='10 DATA L,L,"-",-\n  1,00\n20 PRINT "Ω","Ω"\n', region_ids=['basic']))
        blocks.extend([dict(id='hex', kind='code',
            text='7BE0- 00 01 00 00 01\n7BE0- 00 00\n' if i == 0 else '7BE0- 00\n',
            region_ids=['hex']), dict(id='caption', kind='caption', text='원본 Ω', region_ids=['caption'])])
        for b in blocks:
            b.update(correction_evidence=['corrections.json#'+b['id']], uncertainties=[])
        ids = [b['id'] for b in blocks]+['image']
        assets = {id:pin(id+'.png') for id in ids}
        p.update(pages=[page], regions=[dict(id=id, pdf_index=i,
            kind='figure' if id == 'image' else next(b['kind'] for b in blocks if b['id'] == id),
            bbox=[0,n/6,1,(n+1)/6], notes='Reviewed synthetic source') for n,id in enumerate(ids)],
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
        c.update(manual_postproduction=dict(literal_source_fields_format='v1'), blocks=deepcopy(blocks),
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
            values=['L','L','"-"','-\n  1','00']
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


class SourceLiteralTests(unittest.TestCase):
    def test_source_occurrences_and_short_rows_survive_without_interpretation(self):
        recipe,sources=fixture();before=deepcopy(sources);p,c=project(recipe,sources)
        self.assertEqual(sources,before)
        self.assertEqual(text_bytes(p)[1],b''.join(text_bytes(p)[1] for p,_ in sources))
        self.assertEqual([r['literal_values'] for r in c['basic_data_statements']],[['L','L','"-"','-\n  1','00']])
        self.assertEqual([r['hex_literals'] for r in c['hex_dump_row_index']],
                         [['00','01','00','00','01'],['00','00'],['00']])
        self.assertEqual([r['occurrence'] for r in c['hex_dump_row_index']],[1,2,1])
        self.assertEqual([r['contents'] for r in c['quoted_source_index']],['-','Ω','Ω'])
        self.assertEqual([r['article_physical_line'] for r in c['listing_line_index']],list(range(1,7)))
        self.assertEqual(c['inline_example_index'][0]['source_range'],{S:3,E:5})
        self.assertEqual(c['segments'][0]['original_metadata']['future_metadata'],{'opaque':['Ω',3]})
        self.assertEqual(c['caption_links'][1]['caption_region_id'],'ending-caption')
        self.assertEqual(c['hex_dump_row_index'][1]['physical_line_id'],'opening:physical:5')
        self.assertEqual(c['listing_line_index'][4]['unit_id'],'opening-hex:address:7BE0:2')
        self.assertEqual([r['logical_line'] for r in c['logical_listing_line_index']],[1,2])
        self.assertEqual([r['source_logical_line'] for r in c['logical_listing_line_index']],[1,2])

    def test_identical_hex_fields_cannot_reuse_another_occurrence(self):
        recipe,sources=fixture();ff=sources[0][1]['hex_dump_field_index'];ff[2][S]=ff[0][S];ff[2][E]=ff[0][E]
        with self.assertRaisesRegex(ValueError,'hex literal occurrence'):project(recipe,sources)

    def test_repeated_address_cannot_name_another_physical_row(self):
        recipe,sources=fixture();aa=sources[0][1]['hex_dump_address_index'];aa[1][S]=aa[0][S];aa[1][E]=aa[0][E]
        with self.assertRaisesRegex(ValueError,'hex address occurrence'):project(recipe,sources)

    def test_repeated_quotes_and_bare_letter_fields_keep_positions(self):
        for key,first,last in [('quoted_source_index',1,2),('basic_data_field_index',0,1)]:
            with self.subTest(key=key):
                recipe,sources=fixture();rr=sources[0][1][key]
                for k in (S,E,'segments'):rr[last][k]=deepcopy(rr[first][k])
                with self.assertRaises(ValueError):project(recipe,sources)

    def test_missing_rows_addresses_values_and_segments_rejected(self):
        for key in ('hex_dump_row_index','hex_dump_address_index','hex_dump_field_index',
                    'quoted_source_index','basic_data_field_index'):
            with self.subTest(key=key):
                recipe,sources=fixture();sources[0][1][key].pop()
                with self.assertRaises(ValueError):project(recipe,sources)
        recipe,sources=fixture();sources[0][1]['basic_data_field_index'][0].pop('segments')
        with self.assertRaises(ValueError):project(recipe,sources)

    def test_wrong_native_logical_ordinal_rejected(self):
        recipe,sources=fixture();sources[0][1]['logical_listing_line_index'][1]['logical_line']=1
        with self.assertRaisesRegex(ValueError,'logical source text/ordinal'):project(recipe,sources)

    def test_short_final_row_cannot_be_padded(self):
        recipe,sources=fixture();r=sources[1][1]['hex_dump_row_index'][0]
        r['hex_literals']=['00']*8;r['value_count']=8
        with self.assertRaisesRegex(ValueError,'hex unit identity/values'):project(recipe,sources)

    def test_source_status_and_encoded_byte_claims_rejected(self):
        for key,value in [('source_bytes','verified'),('execution_verified',True),('execute_verified',True),
                          ('checksum_verified',True),('encoded_bytes',[0])]:
            with self.subTest(key=key):
                recipe,sources=fixture();sources[0][1]['hex_dump_field_index'][0][key]=value
                with self.assertRaises(ValueError):project(recipe,sources)

    def test_physical_negative_wrap_must_not_be_normalized_in_data_index(self):
        recipe,sources=fixture();sources[0][1]['basic_data_field_index'][3]['text']='-1'
        with self.assertRaisesRegex(ValueError,'DATA field occurrence'):project(recipe,sources)

    def test_wrong_scan_and_split_utf8_quote_rejected(self):
        recipe,sources=fixture();sources[0][1]['quoted_source_index'][1]['segments'][0]['scan']=sources[0][0]['figures'][0]['asset']
        with self.assertRaises(ValueError):project(recipe,sources)
        recipe,sources=fixture();sources[0][1]['quoted_source_index'][1][S]+=2
        with self.assertRaises(ValueError):project(recipe,sources)

    def test_inline_repeated_text_cannot_move_to_another_region(self):
        recipe,sources=fixture();sources[0][1]['inline_example_index'][0]['region_id']='caption'
        with self.assertRaisesRegex(ValueError,'regional occurrence'):project(recipe,sources)

    def test_opt_in_uniformity_version_mode_and_legacy_behavior(self):
        for change in ('mixed','version','mode','basic'):
            with self.subTest(change=change):
                recipe,sources=fixture()
                if change=='mixed':sources[1][1].pop('manual_postproduction')
                elif change=='version':sources[1][1]['manual_postproduction']['literal_source_fields_format']='v2'
                elif change=='mode':recipe['index_mode']='aligned-assembly-listing-v1'
                else:sources[0][1]['basic_source_fields_format']='v1'
                with self.assertRaises(ValueError):project(recipe,sources)
        recipe,sources=fixture()
        for _,c in sources:c.pop('manual_postproduction')
        _,c=project(recipe,sources)
        self.assertNotIn('literal_source_fields_format',c)

    def test_cross_segment_logical_joins_rejected(self):
        recipe,sources=fixture()
        recipe['wrapped_listing_joins']=[dict(left=dict(segment='opening',logical_line_id='basic:number:20',ending='"Ω"\n'),
            right=dict(segment='ending',physical_line_ids=['hex:physical:1'],opening='7BE0'))]
        with self.assertRaisesRegex(ValueError,'complete segment-local units'):project(recipe,sources)

    def test_unsupported_tables_are_rejected_instead_of_silently_dropped(self):
        recipe,sources=fixture();sources[0][1]['table_row_index']=[{'future':'table'}]
        with self.assertRaisesRegex(ValueError,'unsupported table/category'):project(recipe,sources)

    def test_image_order_caption_and_source_unit_references_rejected(self):
        for change in ('image','caption','unit'):
            recipe,sources=fixture();c=sources[0][1]
            if change=='image':c['image_preservation']=[]
            elif change=='caption':c['caption_links'][0]['caption_region_id']='prose'
            else:c['hex_dump_row_index'][0]['source_line_id']='hex:physical:2'
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,sources)


if __name__ == '__main__':
    unittest.main()
