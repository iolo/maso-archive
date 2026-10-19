"""Occurrence-fidelity regressions for mixed printed BASIC and hex listings."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

from tools.pdf_restore.assemble import text_bytes
from tools.pdf_restore.graphic_literal_assembly import project, installed
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
        blocks.append(dict(id='basic', kind='code',
            text=('10 DATA L,L,"-",13\n  3,00\n20 PRINT "Ω","Ω"\n' if i == 0 else
                  '10 PRINT "⟦blank-run:width-unverified⟧"\n20 DEF CHR$ ( &HA0 ) = CHR$ ( &\n  H8 ) + CHR$ ( &H8 )\n'),
            region_ids=['basic']))
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
        c.update(manual_postproduction=dict(graphic_table_source_fields_format='v1'), blocks=deepcopy(blocks),
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
            marks=[m.start() for m in re.finditer('"',u['text'])]
            literals=[u['text'][marks[n]:marks[n+1]+1] for n in range(0,len(marks),2)]
            cursor=0
            for n,t in enumerate(literals,1):
                a=u['text'].index(t,cursor);cursor=a+len(t)
                lo=u[S]+len(u['text'][:a].encode());hi=lo+len(t.encode())
                c['quoted_source_index'].append(dict(block_id='basic',listing_id='basic',
                    logical_line_id=u['line_id'],printed_line=u['printed_line'],literal_ordinal=n,
                    download='listing.txt',**{S:lo,E:hi},transcription_excerpt=t,contents=t[1:-1],
                    closing_quote_visible=True,segments=pieces(u,lo,hi),source_bytes='unverified',
                    execution_verified=False,kind='printed-source-string'))
            if not u['text'].startswith('10 DATA '):
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
        c.update(basic_hex_literal_index=[],font_definition_index=[],graphic_string_index=[])
        for u in c['logical_listing_line_index']:
            fields=[]
            for ordinal,match in enumerate(re.finditer(r'&(?:\n[ \t]*)?H[0-9A-F]+',u['text']),1):
                a=u[S]+len(u['text'][:match.start()].encode());z=u[S]+len(u['text'][:match.end()].encode())
                row=dict(block_id='basic',listing_id='basic',logical_line_id=u['line_id'],printed_line=u['printed_line'],field=ordinal,kind='printed-hex-source-literal',text=match[0],download='listing.txt',**{S:a,E:z},segments=pieces(u,a,z),source_bytes='unverified',execution_verified=False)
                fields.append(row);c['basic_hex_literal_index'].append(row)
            common=dict(block_id='basic',listing_id='basic',logical_line_id=u['line_id'],printed_line=u['printed_line'],download='listing.txt',**{S:u[S],E:u[E]},transcription_excerpt=u['text'],source_parts=deepcopy(u['source_parts']),segments=deepcopy(u['segments']),source_bytes='unverified',execution_verified=False)
            if 'DEF CHR$' in u['text']:
                c['font_definition_index'].append(dict(common,kind='printed-font-definition-source',literal_hex_fields=[r['text'] for r in fields],literal_count=len(fields)))
            if any(ord(ch)>127 for ch in u['text']):
                markers=[]
                for match in re.finditer('⟦[^⟧]+⟧',u['text']):
                    a=u[S]+len(u['text'][:match.start()].encode());z=u[S]+len(u['text'][:match.end()].encode())
                    markers.append(dict(text=match[0],**{S:a,E:z},segments=pieces(u,a,z),original_encoded_bytes='unverified',length_or_width='unverified',future_marker_metadata=['Ω',3]))
                c['graphic_string_index'].append(dict(common,kind='printed-graphic-source-candidate',editorial_markers=markers,visual_candidates=['unverified glyph'],future_graphic_metadata={'opaque':True}))
        sources.append((p,c))
    recipe=dict(index_mode='wrapped-listing-v1',segments=[dict(name=n,manifest=pin(n+'/manifest.json'))
        for n in ('opening','ending')],expected_pdf_pages=[1,2],prose_joins=[],wrapped_listing_joins=[],
        evidence=['Complete synthetic source reviewed'],uncertainties=['Bytes unverified'],resolved_notes=[])
    return recipe,sources


def cross_scan_fixture():
    recipe,sources=fixture();p,c=sources[1];rid='basic-cont';asset=dict(path=rid+'.png',sha256='0'*64,bytes=0)
    old_asset=next(r['asset'] for r in p['region_assets'] if r['region_id']=='basic')
    region=deepcopy(next(r for r in p['regions'] if r['id']=='basic'));region['id']=rid;p['regions'].append(region)
    p['region_assets'].append(dict(region_id=rid,asset=asset));p['verification']['reviewed_region_ids'].append(rid)
    block=next(b for b in p['blocks'] if b['id']=='basic');block['region_ids']=['basic',rid];c['blocks']=deepcopy(p['blocks'])
    c['records'].append(dict(id=rid,scan=asset,raw_ocr=None,block_ids=['basic']))
    unit=c['logical_listing_line_index'][-1];cut=unit['segments'][-1][S]
    last=next(r for r in c['listing_line_index'] if r['line_id']==unit['source_parts'][-1])
    last.update(region_id=rid,scan=asset);last['segments'][0].update(region_id=rid,scan=asset)
    unit['segments'][-1].update(region_id=rid,scan=asset)
    for key in ('basic_hex_literal_index','font_definition_index'):
        for row in c[key]:
            for part in row['segments']:
                if part[S]>=cut:part.update(region_id=rid,scan=asset)
    for key in ('regional_text_index','text_review_items'):
        old=next(r for r in c[key] if r['block_id']=='basic');idx=c[key].index(old);lo=old[S];text=old['transcription_excerpt'];split=cut
        # Native listing basic starts atzero inthis fixture.
        left=dict(old,**{E:lo+split},transcription_excerpt=text.encode()[:split].decode())
        right=dict(old,region_id=rid,scan=asset,**{S:lo+split},transcription_excerpt=text.encode()[split:].decode())
        c[key][idx:idx+1]=[left,right]
    whole=next(r for r in c['text_index'] if r['block_id']=='basic');whole.update(region_ids=['basic',rid],scans=[old_asset,asset])
    whole=next(r for r in c['listing_index'] if r['block_id']=='basic');whole['region_ids']=['basic',rid]
    old=next(r for r in c['regional_listing_index'] if r['block_id']=='basic');idx=c['regional_listing_index'].index(old);text=old['transcription_excerpt']
    c['regional_listing_index'][idx:idx+1]=[dict(old,**{E:cut},transcription_excerpt=text.encode()[:cut].decode()),dict(old,region_id=rid,scan=asset,**{S:cut},transcription_excerpt=text.encode()[cut:].decode())]
    c['listing_source_uncertainties']=[dict(block_id='basic',listing_id='basic',logical_line_id=unit['line_id'],printed_line=unit['printed_line'],region_id='basic',scan=old_asset,scans=[old_asset,asset],download='listing.txt',**{S:unit[S],E:unit[E]},transcription_excerpt=unit['text'],note='Cross-column source record;bytes unverified.')]
    return recipe,sources


class GraphicLiteralTests(unittest.TestCase):
    def test_all_categories_and_exact_nested_ranges_survive(self):
        recipe,sources=fixture();before=deepcopy(sources);p,c=project(recipe,sources)
        self.assertEqual(sources,before)
        self.assertEqual(c['graphic_table_source_fields_format'],'v1')
        self.assertEqual(c['font_definition_index'][0]['literal_hex_fields'],['&HA0','&\n  H8','&H8'])
        self.assertEqual([r['text'] for r in c['basic_hex_literal_index']],['&HA0','&\n  H8','&H8'])
        self.assertEqual(len(c['basic_hex_literal_index'][1]['segments']),2)
        listing=text_bytes(p)[1]
        for row in c['basic_hex_literal_index']:
            self.assertEqual(listing[row[S]:row[E]].decode(),row['text'])
            self.assertEqual(row['source_segment'],'ending')
            self.assertGreater(row[S],row['source_range'][S])
        marker=c['graphic_string_index'][1]['editorial_markers'][0]
        self.assertEqual(listing[marker[S]:marker[E]].decode(),marker['text'])
        self.assertEqual(marker['future_marker_metadata'],['Ω',3])
        self.assertEqual(c['graphic_string_index'][1]['future_graphic_metadata'],{'opaque':True})
        self.assertEqual([r['text'] for r in c['table_cell_index']],['가','','가','나'])
        self.assertEqual(c['basic_data_field_index'][3]['text'],'13\n  3')
        self.assertEqual([r['article_physical_line'] for r in c['listing_line_index']],list(range(1,10)))
        self.assertEqual([r['logical_line'] for r in c['logical_listing_line_index']],[1,2,3,4])
        self.assertEqual(c['segments'][1]['original_metadata']['graphic_string_index'],sources[1][1]['graphic_string_index'])

    def test_repeated_hex_occurrence_cannot_reuse_earlier_span(self):
        recipe,sources=fixture();rows=sources[1][1]['basic_hex_literal_index']
        rows[2][S]=rows[1][S];rows[2][E]=rows[1][E]
        with self.assertRaisesRegex(ValueError,'hex literal occurrence'):project(recipe,sources)

    def test_physical_hex_wrap_cannot_be_normalized_or_lose_scan_clip(self):
        for change in ('normalize','missing','scan'):
            recipe,sources=fixture();r=sources[1][1]['basic_hex_literal_index'][1]
            if change=='normalize':r['text']='&H8'
            elif change=='missing':r['segments'].pop()
            else:r['segments'][1]['scan']=sources[1][0]['figures'][0]['asset']
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,sources)

    def test_specialized_indexes_must_exhaust_all_occurrences_in_order(self):
        for key in ('basic_hex_literal_index','font_definition_index','graphic_string_index'):
            for change in ('missing','duplicate','wrong-owner'):
                recipe,sources=fixture();rows=sources[1][1][key]
                if change=='missing':rows.pop()
                elif change=='duplicate':rows.append(deepcopy(rows[-1]))
                else:rows[0]['logical_line_id']='other-unit'
                with self.subTest(key=key,change=change),self.assertRaises(ValueError):project(recipe,sources)

    def test_font_literals_and_source_parts_cannot_be_repaired(self):
        for change in ('padding','count','parts'):
            recipe,sources=fixture();r=sources[1][1]['font_definition_index'][0]
            if change=='padding':r['literal_hex_fields'][1]='&H08'
            elif change=='count':r['literal_count']+=1
            else:r['source_parts'].pop()
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,sources)

    def test_marker_utf8_occurrence_and_scan_segments_are_exact(self):
        for change in ('range','text','missing','scan'):
            recipe,sources=fixture();r=sources[1][1]['graphic_string_index'][0]['editorial_markers'][0]
            if change=='range':r[S]+=1
            elif change=='text':r['text']='⟦repaired⟧'
            elif change=='missing':r['segments'].pop()
            else:r['segments'][0]['scan']=sources[1][0]['figures'][0]['asset']
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,sources)

    def test_unknown_marker_width_or_bytes_cannot_be_certified(self):
        for key,value in (('length_or_width',4),('original_encoded_bytes',[0]),('execution_verified',True)):
            recipe,sources=fixture();r=sources[1][1]['graphic_string_index'][0]['editorial_markers'][0];r[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):project(recipe,sources)

    def test_false_source_or_execution_claims_rejected_in_each_category(self):
        for key in ('basic_hex_literal_index','font_definition_index','graphic_string_index'):
            for field,value in (('source_bytes','verified'),('execution_verified',True),('encoded_bytes',[0])):
                recipe,sources=fixture();sources[1][1][key][0][field]=value
                with self.subTest(key=key,field=field),self.assertRaises(ValueError):project(recipe,sources)

    def test_uniform_version_mode_and_no_conflicting_opt_in_required(self):
        for change in ('mixed','version','mode','basic','table','literal','join'):
            recipe,sources=fixture()
            if change=='mixed':sources[0][1].pop('manual_postproduction')
            elif change=='version':sources[0][1]['manual_postproduction']['graphic_table_source_fields_format']='v2'
            elif change=='mode':recipe['index_mode']='namespaced-v1'
            elif change=='basic':sources[0][1]['basic_source_fields_format']='v1'
            elif change in ('table','literal'):sources[0][1]['manual_postproduction']['literal_'+('table_' if change=='table' else '')+'source_fields_format']='v1'
            else:recipe['wrapped_listing_joins']=[{'unreviewed':'join'}]
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,sources)

    def test_cross_scan_uncertainty_keeps_every_source_scan_and_rejects_missing_one(self):
        recipe,sources=cross_scan_fixture();p,c=project(recipe,sources)
        row=c['listing_source_uncertainties'][0]
        self.assertEqual([s['path'] for s in row['scans']],['segments/ending/basic.png','segments/ending/basic-cont.png'])
        self.assertEqual(row['region_id'],'ending-basic')
        for change in ('missing','first-scan','region'):
            recipe,sources=cross_scan_fixture();row=sources[1][1]['listing_source_uncertainties'][0]
            if change=='missing':row['scans'].pop()
            elif change=='first-scan':row['scan']=row['scans'][1]
            else:row['region_id']='basic-cont';row['scan']=row['scans'][1]
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,sources)

    def test_context_restores_previous_projector_after_exception(self):
        baseline=base_assembly.project
        with self.assertRaisesRegex(RuntimeError,'probe'):
            with installed():
                self.assertIs(base_assembly.project,project)
                raise RuntimeError('probe')
        self.assertIs(base_assembly.project,baseline)

    def test_unflagged_legacy_output_is_unchanged(self):
        from tools.pdf_restore.table_literal_assembly import project as previous
        recipe,sources=fixture()
        for _,c in sources:c.pop('manual_postproduction')
        self.assertEqual(project(recipe,sources),previous(recipe,sources))


if __name__ == '__main__':unittest.main()
