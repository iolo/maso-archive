"""News assembly must preserve source tables and reject broken ownership/spans."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_image_survey_assemble as fixtures
from tools.pdf_restore.assemble import project
from tools.pdf_restore.assembly_indexes import block_ranges
from tools.pdf_restore.assembly_image_news import S, E


class NewsAssemblyTests(unittest.TestCase):
    def fixture(self, root):
        recipe, originals = fixtures.SurveyAssemblyTests().fixture(root)
        recipe.pop('survey_links')
        recipe['source_index_mode'] = 'regional-news-v1'
        recipe['coordinate_assets'] = []
        for n, (p, c) in zip('ab', originals):
            c['content_associations'] = []
            c['literal_source_fields'] = []
            c['source_literal_index'] = []
            c['source_uncertainties'] = []
            c['figure_associations'] = []
            c['figure_structures'] = []
            c['inserted_separator_ranges'] = []
            blocks = {b['id']: b for b in p['blocks']}; ranges = block_ranges(p)
            def span(owner, text, start=None):
                b = blocks[owner]; rid = b['region_ids'][0]
                a = len(b['text'][:b['text'].index(text)].encode()) if start is None else start
                z = a + len(text.encode())
                return dict(block_id=owner, literal=text, start_byte=a, end_byte=z,
                            source_segments=[dict(region_id=rid, scan=next(r['scan'] for r in c['records'] if r['id']==rid),
                                                  regional_start_byte=a, regional_end_byte=z,
                                                  block_start_byte=a, block_end_byte=z,
                                                  **{S:ranges[owner][0]+a,E:ranges[owner][0]+z})] if text else [],
                            **{S:ranges[owner][0]+a,E:ranges[owner][0]+z})
            c['content_associations'] = [
                dict(kind='source-news-category', category_id='category', parent_category_id=None,
                     heading_source=span('table', blocks['table']['text']), item_ids=['item'], whole_article_complete=False),
                dict(kind='source-news-item', news_item_id='item', category_id='category',
                     headline_source=span('table', blocks['table']['text']), body_block_ids=['body','code'],
                     logical_region_ids=blocks['body']['region_ids']+blocks['code']['region_ids']),
                dict(kind='source-news-paragraph', paragraph_id='p', news_item_id='item',
                     source=span('body', blocks['body']['text']))]
            text = blocks['code']['text']; cells=[]
            for i, (literal, a) in enumerate([('Closing',0),('한글.',8),('',len(text.encode()))]):
                s = span('code',literal,a)
                cells.append(dict(column=i,column_name=str(i),text=literal,start_byte=a,end_byte=a+len(literal.encode()),
                                  state='source-transcription' if literal else 'observed-blank',source=s))
            rid=blocks['code']['region_ids'][0]
            c['tables']=[dict(table_id='table',block_id='code',news_item_id='item',columns=['0','1','2'],
                             rows=[dict(row_id='row',row_index=0,row_kind='data',region_id=rid,
                                        scan=next(r['scan'] for r in c['records'] if r['id']==rid),
                                        start_byte=0,end_byte=len(text.encode()),cells=cells)])]
            folio=int(p['pages'][0]['printed_page'])
            if n=='a':
                c['content_associations'].append(dict(kind='source-segment-boundary',segment_id='opening',selected_folios=[folio],
                    pending_folios=[2],next_category_literal=originals[1][0]['blocks'][0]['text'],
                    whole_article_assembly_required=True,article_complete=False))
            else:
                previous=recipe['segments'][0]['manifest']
                c['content_associations'].append(dict(kind='source-segment-opening',prior_package=dict(
                    package=previous['path'].rsplit('/',1)[0],manifest=previous,evidence=dict(path='source-only',sha256='0'*64,bytes=0),extent=[1,1],preserveExactly=True),
                    prior_category_literal=originals[0][0]['blocks'][0]['text'],current_heading_source=span('table',blocks['table']['text']),
                    paragraph_continues=False,whole_article_assembly_required=True,article_complete=False))
                c['content_associations'].append(dict(kind='source-article-ending',ending_source=span('code',text),
                    closing_region_id='figure-region',closing_printed_folio=folio,next_printed_folio=folio+1,
                    pending_source_folios=[],whole_article_assembly_required=True,article_complete=False))
        # Source fixture block order is not the category heading order.
        originals[0][1]['content_associations'][3]['next_category_literal']=originals[1][1]['content_associations'][0]['heading_source']['literal']
        ref=lambda n,i:dict(segment=n,association=i)
        recipe['news_links']=dict(boundaries=[dict(left=ref('a',3),right=ref('b',3),evidence='New category.')],
                                  endings=[dict(source=ref('b',4),evidence='Closing emblem.')])
        return recipe, originals

    def test_exact_tables_blank_cells_and_scoped_utf8(self):
        with tempfile.TemporaryDirectory() as temporary:
            recipe, originals=self.fixture(Path(temporary)); before=deepcopy(originals)
            p,c=project(recipe,originals)
            self.assertEqual(originals,before)
            self.assertEqual(project(recipe,originals),(p,c))
            self.assertEqual(len(c['tables']),2)
            self.assertNotEqual(c['tables'][0]['table_id'],c['tables'][1]['table_id'])
            for table in c['tables']:
                self.assertEqual(table['rows'][0]['cells'][2]['text'],'')
                source=table['rows'][0]['cells'][1]['source']
                from tools.pdf_restore.assemble import text_bytes
                self.assertEqual(text_bytes(p)[0][source[S]:source[E]].decode(),'한글.')
            self.assertTrue(c['coverage']['complete_article'])
            self.assertEqual(len(c['resolved_news_declarations']),2)

    def test_rejects_damaged_source_contracts(self):
        with tempfile.TemporaryDirectory() as temporary:
            recipe, originals=self.fixture(Path(temporary))
            def table(o): return o[0][1]['tables'][0]
            def paragraph(o): return o[0][1]['content_associations'][2]
            faults={
                'unknown correction':lambda r,o:o[0][1].update(future_index=[]),
                'unknown semantic kind':lambda r,o:paragraph(o).update(kind='future-kind'),
                'duplicate item':lambda r,o:o[0][1]['content_associations'].append(deepcopy(o[0][1]['content_associations'][1])),
                'wrong item':lambda r,o:paragraph(o).update(news_item_id='missing'),
                'wrong category':lambda r,o:o[0][1]['content_associations'][1].update(category_id='missing'),
                'cyclic category':lambda r,o:o[0][1]['content_associations'][0].update(parent_category_id='category'),
                'wrong paragraph owner':lambda r,o:paragraph(o)['source'].update(block_id='table'),
                'split UTF8':lambda r,o:table(o)['rows'][0]['cells'][1]['source'].update(start_byte=9),
                'wrong article span':lambda r,o:paragraph(o)['source'].__setitem__(S,1),
                'wrong regional owner':lambda r,o:paragraph(o)['source']['source_segments'][0].update(region_id='code-region'),
                'wrong regional scan':lambda r,o:paragraph(o)['source']['source_segments'][0]['scan'].update(sha256='0'*64),
                'lost source part':lambda r,o:paragraph(o)['source'].update(source_segments=[]),
                'wrong table news owner':lambda r,o:table(o).update(news_item_id='missing'),
                'lost column':lambda r,o:table(o)['rows'][0]['cells'].pop(),
                'wrong column':lambda r,o:table(o)['rows'][0]['cells'][0].update(column=1),
                'filled printed blank':lambda r,o:table(o)['rows'][0]['cells'][2].update(text='inferred'),
                'invented scope':lambda r,o:table(o)['rows'][0].update(rank_scope_from_row='row'),
                'false verification':lambda r,o:paragraph(o).update(historical_claim_verified=True),
                'false normalization':lambda r,o:paragraph(o).update(normalization_applied=True),
                'unknown identity':lambda r,o:paragraph(o).update(future_id='unbound'),
                'paragraph join':lambda r,o:o[1][1]['content_associations'][3].update(paragraph_continues=True),
                'wrong predecessor':lambda r,o:o[1][1]['content_associations'][3]['prior_package']['manifest'].update(sha256='0'*64),
                'unclosed ending':lambda r,o:r['news_links']['endings'].clear(),
                'wrong boundary':lambda r,o:r['news_links']['boundaries'][0]['right'].update(association=0),
                'missing pending page':lambda r,o:o[0][1]['content_associations'][3].update(pending_folios=[]),
                'lost source region':lambda r,o:o[0][1]['regional_transcription'].pop(next(iter(o[0][1]['regional_transcription']))),
            }
            # Independent copies avoid mutation aliases between recipe and fixture.
            for name, damage in faults.items():
                with self.subTest(name=name):
                    r=deepcopy(recipe);o=deepcopy(originals);damage(r,o)
                    with self.assertRaises((ValueError,KeyError)): project(r,o)


if __name__=='__main__': unittest.main()
