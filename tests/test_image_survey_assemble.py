"""Survey identity closure, exact nested source spans and explicit dispositions."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from tests import test_image_assemble as base_fixture
from tools.pdf_restore.assemble import project, read_segment, text_bytes
from tools.pdf_restore.assembly_indexes import block_ranges
from tools.pdf_restore.assembly_survey import S, E


class SurveyAssemblyTests(unittest.TestCase):
    def fixture(self, root):
        """Build ordinary synthetic sources, then supply isolated in-memory prose indexes.

        These are projection fixtures. Real source package serialization/offline
        checking is exercised by the private restoration's independent exports.
        """
        path = base_fixture.ImageAssemblyTests().fixture(root)
        base = json.loads(path.read_bytes())
        originals = [read_segment((root / s['manifest']['path']).parent, s['manifest']) for s in base['segments']]
        for i, (p, old) in enumerate(originals):
            p['pages'][0]['printed_page'] = str(i + 1)
            for region in p['regions']:
                if region['kind'] == 'code':
                    region['kind'] = 'prose'
            for block in p['blocks']:
                block['kind'] = 'section-label' if block['id'] == 'table' else 'prose'
                if block['id'] == 'code':
                    block['text'] = 'Closing 한글.'
            p['content_order'] = [dict(type='block', id=v['id']) for v in p['blocks']] + [dict(type='figure', id='figure')]
            B = {v['id']: v for v in p['blocks']}; ranges = block_ranges(p)
            p['figures'][0]['caption'] = B['table']['text']
            c = dict(article_id=p['id'], map=old['map'], blocks=deepcopy(p['blocks']), records=deepcopy(old['records']),
                     character_perfect_code=False, regional_transcription={}, regional_text_ranges=[], prose_joins=[],
                     source_readings=[], source_readings_base='archive/synthetic', limitations=[],
                     tables=[], listing_groups=[], listing_index=[], listing_line_index=[], logical_listing_line_index=[],
                     listing_caption_associations=[], figure_label_index=[], literal_source_fields=[], source_literal_index=[],
                     source_uncertainties=[], figure_structures=[], figure_associations=[], content_associations=[])
            assets = {v['id']: v['scan'] for v in c['records']}
            for block in p['blocks']:
                rid = block['region_ids'][0]; text = block['text']; c['regional_transcription'][rid] = text
                c['regional_text_ranges'].append(dict(region_id=rid, block_id=block['id'], start_byte=0, end_byte=len(text.encode()), text=text, scan=assets[rid]))
                next(v for v in c['records'] if v['id'] == rid)['corrected_text'] = text
            def occurrence(id, text):
                start = len(B[id]['text'][:B[id]['text'].index(text)].encode()); end = start + len(text.encode()); rid = B[id]['region_ids'][0]
                return dict(block_id=id, literal=text, source_segments=[dict(region_id=rid, scan=assets[rid], regional_start_byte=start, regional_end_byte=end,
                            block_start_byte=start, block_end_byte=end, **{S: ranges[id][0] + start, E: ranges[id][0] + end})])
            rows = c['content_associations']
            rows.extend(dict(kind='source-paragraph', paragraph_id=id + ':p1', **occurrence(id, B[id]['text'])) for id in ['body', 'code'])
            rows.append(dict(kind='source-section', section_id='root' if i == 0 else 'child', parent_section_id=None if i == 0 else 'root',
                             heading_block_id='table', body_block_ids=['body', 'code'], heading_source=occurrence('table', B['table']['text'])))
            rows.append(dict(kind='source-technical-claim', claim_id='same-id', subject_id='subject', source_paragraph_id='body:p1',
                             claim_source=occurrence('body', B['body']['text']), historical_or_behavioral_verification=False))
            c['literal_source_fields'].append(dict(field_id='same-id', **occurrence('code', '한글'), encoded_bytes_verified=False))
            c['figure_associations'].append(dict(figure_id='figure', figure_region_id='figure-region', caption_block_ids=['table']))
            c['figure_structures'].append(dict(figure_id='figure', figure_region_id='figure-region', scan=assets['figure-region'], kind='source-editorial-illustration'))
            originals[i] = (p, c)
        a, ac = originals[0]; z, zc = originals[1]
        prior_raw = (json.dumps(a, ensure_ascii=False, indent=2) + '\n').encode()
        prior = dict(manifest=deepcopy(base['segments'][0]['manifest']), article=dict(path='article.json', sha256=hashlib.sha256(prior_raw).hexdigest(), bytes=len(prior_raw)))
        def occ(which, block):
            return deepcopy(next(v for v in originals[which][1]['content_associations'] if v.get('paragraph_id') == block + ':p1'))
        def span_only(value):
            return {k: v for k, v in value.items() if k in ('block_id', 'literal', 'source_segments')}
        last = span_only(occ(0, 'body')); first = span_only(occ(1, 'body'))
        ac['content_associations'].append(dict(kind='source-product-profile', product_id='p', heading_source=deepcopy(ac['content_associations'][2]['heading_source']), body_block_id='body', source_paragraph_ids=['body:p1'], complete_in_segment=False))
        ac['content_associations'].append(dict(kind='source-segment-continuation', source_section_id='root', current_last_source=last, next_literal=first['literal'], next_printed_folio=2,
                                             next_source_image=z['pages'][0]['image'], paragraph_continues=False, pending_source_folios=[2], whole_article_assembly_required=True, article_complete=False))
        ac['content_associations'].append(dict(kind='source-caption-forward-reference', figure_id='figure', caption_source=deepcopy(ac['content_associations'][2]['heading_source']),
                                             target_section_id='child', target_heading_literal=zc['content_associations'][2]['heading_source']['literal'], target_printed_folio=2,
                                             caption_assigned_to_adjacent_product=False, target_status='outside-selected-segment'))
        zc['content_associations'].append(dict(kind='source-product-profile-continuation', product_id='p', prior_package=deepcopy(prior), prior_heading_block_id='table',
                                             body_block_id='body', source_paragraph_ids=['body:p1'], profile_source_ending_in_segment=True))
        zc['content_associations'].append(dict(kind='source-segment-opening', prior_package=deepcopy(prior), prior_block_id='body', prior_last_literal=last['literal'], current_first_source=first,
                                             paragraph_continues=False, continued_section_id='root', whole_article_assembly_required=True, article_complete=False))
        zc['content_associations'].append(dict(kind='source-caption-back-reference', prior_package=deepcopy(prior), prior_figure_id='figure', prior_caption_block_id='table',
                                             prior_caption_literal=a['figures'][0]['caption'], target_section_id='child', target_heading_source=deepcopy(zc['content_associations'][2]['heading_source']),
                                             caption_assigned_to_starburst=False, caption_spelling_normalized=False))
        zc['content_associations'].append(dict(kind='source-article-ending', ending_source=span_only(occ(1, 'code')), closing_region_id='figure-region', closing_printed_folio=2,
                                             next_printed_folio=3, pending_source_folios=[], whole_article_assembly_required=True, article_complete=False))
        # The prior manifest/article pins bind the final current source object,
        # after all synthetic declarations have been added.
        raw = (json.dumps(a, ensure_ascii=False, indent=2) + '\n').encode()
        for value in zc['content_associations']:
            if 'prior_package' in value:
                value['prior_package']['article'].update(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
        ref = lambda name, index: dict(segment=name, association=index)
        binding = lambda name, kind, id: dict(segment=name, kind=kind, id=id)
        recipe = dict(index_mode='structured-regions-v1', source_index_mode='regional-survey-v1', segments=base['segments'],
                      expected_source_indices=[7, 19], inventory=base['inventory'], evidence=['Synthetic whole article source extent.'], uncertainties=[], resolved_notes=[], prose_joins=[], relationship_links=[],
                      survey_links=dict(entities=[dict(**{'from': binding('a', 'section', 'child'), 'to': binding('b', 'section', 'child')}, evidence='Forward topic.'),
                                                 dict(**{'from': binding('b', 'section', 'root'), 'to': binding('a', 'section', 'root')}, evidence='Section continuation.'),
                                                 dict(**{'from': binding('b', 'product', 'p'), 'to': binding('a', 'product', 'p')}, evidence='Product continuation.')],
                                        boundaries=[dict(left=ref('a', 5), right=ref('b', 5), evidence='New paragraph.')], captions=[dict(left=ref('a', 6), right=ref('b', 6), evidence='Source caption topic.')],
                                        products=[dict(left=ref('a', 4), right=ref('b', 4), evidence='Product profile.')], endings=[dict(source=ref('b', 7), evidence='Closing source emblem.')]))
        return recipe, originals

    def test_scoped_entities_nested_bytes_and_source_relationships(self):
        with tempfile.TemporaryDirectory() as temp:
            recipe, originals = self.fixture(Path(temp)); before = deepcopy(originals)
            p, c = project(recipe, originals); article, listing = text_bytes(p)
            self.assertEqual(originals, before)
            self.assertEqual(project(recipe, originals), (p, c))
            self.assertEqual(listing, b'')
            self.assertEqual(len(c['survey_resolutions']), 3)
            self.assertNotEqual(c['literal_source_fields'][0]['field_id'], c['literal_source_fields'][1]['field_id'])
            for row in c['literal_source_fields']:
                span = row['source_segments'][0]
                self.assertEqual(article[span[S]:span[E]].decode(), '한글')
            sections = [v for v in c['content_associations'] if v['kind'] == 'source-section']
            self.assertEqual(sections[1]['parent_section_id'], sections[0]['section_id'])
            ending = next(v for v in c['content_associations'] if v['kind'] == 'resolved-source-article-ending')
            self.assertTrue(ending['article_complete']); self.assertFalse(ending['whole_article_assembly_required'])
            boundary = c['survey_resolutions'][0]
            self.assertEqual(boundary['separator'], '\n\n'); self.assertFalse(boundary['paragraph_continues'])
            self.assertEqual(c['segments'][0]['original_metadata']['regional_transcription'], originals[0][1]['regional_transcription'])

    def test_semantic_and_source_damage_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            recipe, originals = self.fixture(Path(temp))
            row = lambda s, i: s[1][1]['content_associations'][i]
            cases = {
                'unknown metadata': lambda r, s: s[0][1].update(unmapped_index=[]),
                'unresolved entity': lambda r, s: r['survey_links']['entities'].pop(),
                'duplicate alias': lambda r, s: r['survey_links']['entities'].append(deepcopy(r['survey_links']['entities'][0])),
                'wrong alias target': lambda r, s: r['survey_links']['entities'][0]['to'].update(id='absent'),
                'duplicate field': lambda r, s: s[0][1]['literal_source_fields'].append(deepcopy(s[0][1]['literal_source_fields'][0])),
                'wrong source paragraph': lambda r, s: row(s, 3).update(source_paragraph_id='absent'),
                'borrowed existing paragraph': lambda r, s: row(s, 3).update(source_paragraph_id='code:p1'),
                'UTF8 split': lambda r, s: s[1][1]['literal_source_fields'][0]['source_segments'][0].update(block_start_byte=9),
                'wrong article offset': lambda r, s: s[1][1]['literal_source_fields'][0]['source_segments'][0].update(utf8_byte_start=0),
                'wrong regional owner': lambda r, s: s[1][1]['literal_source_fields'][0]['source_segments'][0].update(region_id='body-region'),
                'wrong crop': lambda r, s: s[1][1]['literal_source_fields'][0]['source_segments'][0]['scan'].update(sha256='0'*64),
                'wrong literal': lambda r, s: s[1][1]['literal_source_fields'][0].update(literal='한굴'),
                'duplicated span part': lambda r, s: s[1][1]['literal_source_fields'][0]['source_segments'].append(deepcopy(s[1][1]['literal_source_fields'][0]['source_segments'][0])),
                'source normalization': lambda r, s: row(s, 6).update(caption_spelling_normalized=True),
                'false verification': lambda r, s: row(s, 3).update(historical_or_behavioral_verification=True),
                'missing boundary': lambda r, s: r['survey_links']['boundaries'].clear(),
                'open paragraph': lambda r, s: row(s, 5).update(paragraph_continues=True),
                'wrong boundary literal': lambda r, s: row(s, 5).update(prior_last_literal='other'),
                'wrong prior manifest': lambda r, s: row(s, 5)['prior_package']['manifest'].update(sha256='0'*64),
                'wrong prior article': lambda r, s: row(s, 5)['prior_package']['article'].update(sha256='0'*64),
                'wrong external heading': lambda r, s: row(s, 4).update(prior_heading_block_id='absent'),
                'missing caption disposition': lambda r, s: r['survey_links']['captions'].clear(),
                'lost actual caption owner': lambda r, s: s[0][1]['figure_associations'][0].update(caption_block_ids=[]),
                'borrowed section heading': lambda r, s: (s[0][1]['content_associations'][6].update(target_heading_literal='Closing 한글.'), row(s, 6).update(target_heading_source={k: deepcopy(v) for k, v in row(s, 1).items() if k in ('block_id', 'literal', 'source_segments')})),
                'duplicate caption disposition': lambda r, s: r['survey_links']['captions'].append(deepcopy(r['survey_links']['captions'][0])),
                'wrong caption literal': lambda r, s: row(s, 6).update(prior_caption_literal='other'),
                'wrong product ending': lambda r, s: row(s, 4).update(profile_source_ending_in_segment=False),
                'missing product disposition': lambda r, s: r['survey_links']['products'].clear(),
                'wrong ending page': lambda r, s: row(s, 7).update(closing_printed_folio=9),
                'invented pending page': lambda r, s: row(s, 7)['pending_source_folios'].append(3),
                'lost closing emblem': lambda r, s: row(s, 7).update(closing_region_id='body-region'),
                'unknown mode': lambda r, s: r.update(source_index_mode='regional-survey-v99'),
            }
            for label, damage in cases.items():
                r, s = deepcopy(recipe), deepcopy(originals); damage(r, s)
                with self.subTest(case=label), self.assertRaises(ValueError):
                    project(r, s)


if __name__ == '__main__':
    unittest.main()
