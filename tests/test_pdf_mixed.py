"""Mixed printed columns and text wraps: preservation and rejection of false links."""
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

from tools.pdf_restore.assemble import project, text_bytes
from tools.pdf_restore.assembly_indexes import block_ranges
from tools.pdf_restore.package import page_transform


def fixture():
    template = json.loads((Path(__file__).parents[1]/'examples/pdf-article.json').read_bytes())
    pin = lambda path: dict(path=path, sha256='0'*64, bytes=0)
    originals = []
    for index in range(2):
        p = deepcopy(template)
        page = dict(pdf_index=index, pdf_page=index+1, printed_page=str(index+7),
                    width_pt=100, height_pt=200, rotation=0,
                    MediaBox=[0, 0, 100, 200], CropBox=[0, 0, 100, 200])
        page['pdf_to_upright_normalized'] = page_transform(page)
        if index == 0:
            declarations = [('table', 'prose', ['table'], '가\t\n가\t나', None),
                ('asm', 'code', ['code-a', 'code-b'],
                 '6000:\t00 01\t1\tDFB $80,$01,$02\t;한글\n6002:\t02\t\t\t\n\t\t\tSOURCE FILE: X\t\n',
                 [(1, 'numbered', 'numbered-source-line', 1), (None, 'wrapped-continuation', 'machine-byte-wrap', 1),
                  (None, 'unnumbered', 'source-header', 2)]),
                ('body', 'prose', ['body'], '느', None)]
        else:
            declarations = [('body', 'prose', ['body'], '껴지기 때문이다.', None),
                ('basic', 'code', ['basic'], '10 IF X>1\n  83 THEN END\n',
                 [(10, 'numbered', 'numbered-source-line', 1), (None, 'wrapped-continuation', 'basic-text-wrap', 1)]),
                ('plain', 'code', ['plain'], 'RTS\n', [(None, 'unnumbered', 'instruction', 1)])]
        ids = [r for _, _, rr, _, _ in declarations for r in rr] + ['figure-region']
        assets = {id: pin(id+'.png') for id in ids}
        blocks = [dict(id=id, kind=kind, region_ids=rr, text=text,
                       correction_evidence=['corrections.json#'+r for r in rr], uncertainties=[])
                  for id, kind, rr, text, _ in declarations]
        p.update(pages=[page], regions=[dict(id=id, pdf_index=index, kind='figure' if id=='figure-region' else 'prose',
                 bbox=[0, n/(len(ids)+1), 1, (n+1)/(len(ids)+1)], notes='Observed synthetic source')
                 for n, id in enumerate(ids)], blocks=blocks,
                 mapping=dict(status='mapped', evidence=['Observed source'], uncertainties=[]),
                 figures=[dict(id='figure', region_ids=['figure-region'], asset=assets['figure-region'], caption=None)],
                 content_order=([dict(type='figure', id='figure')] if index==0 else [])+
                   [dict(type='block', id=b['id']) for b in blocks]+
                   ([dict(type='figure', id='figure')] if index else []),
                 region_assets=[dict(region_id=id, asset=asset) for id, asset in assets.items()],
                 corrections=[pin('corrections.json')], gaps=[],
                 availability='partial', verification=dict(status='sample-reviewed',
                 reviewed_region_ids=ids, evidence=['Compared synthetic source'], uncertainties=[]))
        c = dict(records=[dict(id=id, region_ids=[id], scan=assets[id], raw_ocr=None,
                              block_ids=[b['id'] for b in blocks if id in b['region_ids']]) for id in ids],
                 blocks=deepcopy(blocks), text_index=[], regional_text_index=[], text_review_items=[],
                 text_review_notes=[], inline_example_index=[], tables=[], table_cell_index=[],
                 table_row_index=[], caption_links=[], prose_joins=[], source_anomalies=[],
                 figure_sequence=[dict(figure_id='figure', region_ids=['figure-region'], caption_block_id=None)],
                 image_preservation=[dict(region_id='figure-region', scan=assets['figure-region'])],
                 listing_groups=[], listing_index=[], regional_listing_index=[], listing_line_index=[],
                 assembly_instruction_index=[], logical_listing_line_index=[], assembly_column_index=[],
                 machine_byte_index=[], data_definition_index=[], listing_source_uncertainties=[])
        bounds = block_ranges(p)
        for block in blocks:
            id, rr, text = block['id'], block['region_ids'], block['text']
            a, z = bounds[id]
            c['text_index'].append(dict(block_id=id, region_ids=rr, scans=[assets[r] for r in rr],
                download='article.txt', utf8_byte_start=a, utf8_byte_end_exclusive=z))
            pieces = [text] if len(rr)==1 else [text.splitlines(True)[0], ''.join(text.splitlines(True)[1:])]
            for rid, piece in zip(rr, pieces):
                row = dict(block_id=id, region_id=rid, scan=assets[rid], download='article.txt',
                           utf8_byte_start=a, utf8_byte_end_exclusive=a+len(piece.encode()), transcription_excerpt=piece)
                c['regional_text_index'].append(row);c['text_review_items'].append(deepcopy(row));a=row['utf8_byte_end_exclusive']
        if index==0:
            c['tables']=[dict(id='table-data',block_id='table',region_id='table',header=None,
                             rows=[['가',''],['가','나']],header_rows=0)]
            offset=bounds['table'][0]
            for nr, cells in enumerate([['가',''],['가','나']],1):
                start=offset
                for nc, cell in enumerate(cells,1):
                    end=offset+len(cell.encode())
                    c['table_cell_index'].append(dict(table_id='table-data',block_id='table',region_id='table',
                        scan=assets['table'],row=nr,column=nc,header=False,text=cell,blank=cell=='',
                        download='article.txt',utf8_byte_start=offset,utf8_byte_end_exclusive=end))
                    offset=end+(nc<2)
                c['table_row_index'].append(dict(table_id='table-data',block_id='table',region_id='table',
                    scan=assets['table'],row=nr,header=False,download='article.txt',
                    utf8_byte_start=start,utf8_byte_end_exclusive=offset));offset+=1
        cursor=0
        for id, kind, rr, text, plan in declarations:
            if kind!='code':continue
            start=cursor;units={};number_column=2 if id=='asm' else 0 if id=='basic' else None
            for ordinal,(line,(number,rowkind,unitkind,unitno)) in enumerate(zip(text.splitlines(True),plan),1):
                rid=rr[0] if len(rr)==1 or ordinal==1 else rr[1];end=cursor+len(line.encode())
                part=dict(region_id=rid,scan=assets[rid],utf8_byte_start=cursor,utf8_byte_end_exclusive=end)
                uid=f'{id}:unit:{unitno}';lid=f'{id}:row:{ordinal}'
                row=dict(**part,block_id=id,listing_id=id,physical_line=ordinal,
                    article_physical_line=len(c['listing_line_index'])+1,printed_line=number,
                    printed_line_visible=number is not None,row_kind=rowkind,assembly_row_kind=unitkind,
                    line_id=lid,download='listing.txt',segments=[part],text=line[:-1],tokens=line.split(),
                    assembly_unit_id=uid,source_bytes='unverified',execution_verified=False)
                if number is not None:row['logical_line_id']=uid
                if rowkind=='wrapped-continuation':
                    row.update(continues_printed_line=units[uid]['printed_line'],logical_line_id=uid)
                if uid not in units:
                    units[uid]=dict(unit_id=uid,listing_id=id,block_id=id,unit_kind=unitkind,
                        download='listing.txt',utf8_byte_start=cursor,utf8_byte_end_exclusive=end,
                        source_parts=[],segments=[],text='',printed_line=number,
                        source_bytes='unverified',execution_verified=False)
                unit=units[uid];unit['source_parts'].append(lid);unit['segments'].append(part)
                unit['utf8_byte_end_exclusive']=end;unit['text']+=line
                if id=='asm':
                    row['columns']=line[:-1].split('\t');off=cursor
                    for col,cell in enumerate(row['columns'],1):
                        finish=off+len(cell.encode())
                        c['assembly_column_index'].append(dict(block_id=id,listing_id=id,region_id=rid,
                            scan=assets[rid],physical_line=ordinal,printed_line=number,column=col,
                            column_name=('address','machine_bytes','printed_number','source','comment')[col-1],
                            text=cell,blank=cell=='',download='listing.txt',utf8_byte_start=off,
                            utf8_byte_end_exclusive=finish))
                        if col==2:
                            for match in re.finditer(r'\b[0-9A-F]{2}\b',cell):
                                a=off+match.start()
                                c['machine_byte_index'].append(dict(block_id=id,listing_id=id,region_id=rid,
                                    scan=assets[rid],physical_line=ordinal,printed_line=number,literal=match[0],
                                    download='listing.txt',utf8_byte_start=a,utf8_byte_end_exclusive=a+2,
                                    source_encoded_bytes='unverified',execution_verified=False))
                        off=finish+(col<5)
                    if ordinal==1:
                        a=cursor+line.index('$80')
                        c['data_definition_index'].append(dict(block_id=id,listing_id=id,region_id=rid,
                            scan=assets[rid],physical_line=ordinal,printed_line=number,download='listing.txt',
                            utf8_byte_start=a,utf8_byte_end_exclusive=a+11,transcription_excerpt='$80,$01,$02',
                            literal_values=['$80','$01','$02'],source_encoded_bytes='unverified',execution_verified=False))
                c['listing_line_index'].append(row);cursor=end
            c['assembly_instruction_index'].extend(units.values())
            for unit in units.values():
                if unit['printed_line'] is not None:
                    c['logical_listing_line_index'].append(dict(listing_id=id,block_id=id,
                        printed_line=unit['printed_line'],occurrence=1,line_id=unit['unit_id'],
                        download='listing.txt',utf8_byte_start=unit['utf8_byte_start'],
                        utf8_byte_end_exclusive=unit['utf8_byte_end_exclusive'],
                        source_parts=unit['source_parts'],segments=unit['segments']))
            c['listing_index'].append(dict(block_id=id,region_ids=rr,scans=[assets[r] for r in rr],
                download='listing.txt',utf8_byte_start=start,utf8_byte_end_exclusive=cursor))
            for rid in rr:
                selected=[r for r in c['listing_line_index'] if r['block_id']==id and r['region_id']==rid]
                a,z=selected[0]['utf8_byte_start'],selected[-1]['utf8_byte_end_exclusive']
                c['regional_listing_index'].append(dict(block_id=id,listing_id=id,region_id=rid,
                    scan=assets[rid],download='listing.txt',utf8_byte_start=a,utf8_byte_end_exclusive=z,
                    transcription_excerpt=text_bytes(p)[1][a:z].decode()))
            c['listing_groups'].append(dict(listing_id=id,block_ids=[id],physical_lines=len(plan),
                numbered_entries=sum(u['printed_line'] is not None for u in units.values()),
                assembly_logical_units=len(units),instruction_units=sum(u['unit_kind']=='instruction' for u in units.values()),
                execute_verified=False,printed_number_column=number_column))
        originals.append((p,c))
    recipe=dict(index_mode='mixed-source-listing-v1',
        segments=[dict(name=n,manifest=pin(n+'/manifest.json')) for n in ('opening','ending')],
        expected_pdf_pages=[1,2],evidence=['Both complete synthetic pages reviewed.'],uncertainties=[],
        resolved_notes=[],prose_joins=[dict(left=dict(segment='opening',block_id='body',ending='느'),
        right=dict(segment='ending',block_id='body',opening='껴지기'),separator='')])
    return recipe,originals


class PDFMixedTests(unittest.TestCase):
    def test_mixed_columns_wraps_blank_cells_and_join_preserve_original_bytes(self):
        recipe,segments=fixture();before=deepcopy(segments)
        p,c=project(recipe,segments);article,listing=text_bytes(p)
        self.assertEqual(segments,before)
        self.assertEqual(listing,b''.join(text_bytes(s)[1] for s,_ in segments))
        self.assertIn('느껴지기 때문이다.',article.decode())
        self.assertEqual(len(c['listing_line_index']),6)
        self.assertEqual(len(c['logical_listing_line_index']),2)
        self.assertEqual(len(c['assembly_instruction_index']),4)
        self.assertEqual(len(c['assembly_column_index']),15)
        self.assertEqual(len(c['machine_byte_index']),3)
        self.assertEqual(c['machine_byte_index'][0]['literal'],'00')
        self.assertEqual(c['data_definition_index'][0]['literal_values'][0],'$80')
        self.assertEqual(len(c['table_cell_index']),4)
        self.assertTrue(c['table_cell_index'][1]['blank'])
        self.assertEqual(len(c['source_text_index']),6)
        self.assertEqual(len(c['text_index']),5)
        self.assertEqual(c['segments'][0]['original_metadata']['assembly_instruction_index'],
                         before[0][1]['assembly_instruction_index'])
        for row in c['assembly_column_index']+c['machine_byte_index']:
            text=listing[row['utf8_byte_start']:row['utf8_byte_end_exclusive']].decode()
            self.assertEqual(text,row.get('text',row.get('literal')))

    def test_rejects_wrong_number_column_scan_or_claimed_source_bytes(self):
        for change in ('number','column','scan','physical-boolean','source-bytes','execution'):
            recipe,ss=fixture();c=ss[0][1]
            if change=='number':c['listing_line_index'][0]['printed_line']=2
            if change=='column':c['listing_groups'][0]['printed_number_column']=0
            if change=='scan':c['listing_line_index'][0]['scan']=deepcopy(c['listing_line_index'][1]['scan'])
            if change=='physical-boolean':c['listing_line_index'][0]['physical_line']=True
            if change=='source-bytes':c['machine_byte_index'][0]['source_encoded_bytes']='verified'
            if change=='execution':c['assembly_instruction_index'][0]['execution_verified']=True
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,ss)

    def test_rejects_missing_or_reassigned_logical_wrap_evidence(self):
        for change in ('missing-unit','wrong-parts','wrap-number','orphan','unit-range'):
            recipe,ss=fixture();c=ss[0][1]
            if change=='missing-unit':c['assembly_instruction_index'].pop()
            if change=='wrong-parts':c['logical_listing_line_index'][0]['source_parts']=[]
            if change=='wrap-number':c['listing_line_index'][1]['continues_printed_line']=2
            if change=='orphan':c['listing_line_index'][1]['assembly_unit_id']='other'
            if change=='unit-range':c['assembly_instruction_index'][0]['utf8_byte_end_exclusive']-=1
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,ss)

    def test_rejects_missing_columns_data_or_repeated_cell_misattribution(self):
        for change in ('column','byte','data','blank','repeated-cell','missing-region'):
            recipe,ss=fixture();c=ss[0][1]
            if change=='column':c['assembly_column_index'].pop()
            if change=='byte':c['machine_byte_index'].pop()
            if change=='data':c['data_definition_index'][0]['literal_values'][0]='$FF'
            if change=='blank':c['table_cell_index'][1]['text']=' '
            if change=='repeated-cell':
                c['table_cell_index'][0]['utf8_byte_start']=c['table_cell_index'][2]['utf8_byte_start']
                c['table_cell_index'][0]['utf8_byte_end_exclusive']=c['table_cell_index'][2]['utf8_byte_end_exclusive']
            if change=='missing-region':c['regional_listing_index'].pop()
            with self.subTest(change=change),self.assertRaises(ValueError):project(recipe,ss)

    def test_rejects_join_with_unreviewed_separator_or_nonadjacent_fragments(self):
        recipe,ss=fixture();recipe['prose_joins'][0]['separator']='\\n'
        with self.assertRaises(ValueError):project(recipe,ss)
        recipe,ss=fixture();ss[1][0]['content_order'].insert(0,ss[1][0]['content_order'].pop())
        with self.assertRaises(ValueError):project(recipe,ss)


if __name__=='__main__':
    unittest.main()
