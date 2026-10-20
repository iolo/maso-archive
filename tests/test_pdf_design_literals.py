"""Mixed literal assembly preserves future categories and rejects false source links."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.pdf_restore import assemble as base
from tools.pdf_restore import design_literal_assembly as literal
from tools.pdf_restore.assembly_indexes import block_ranges
from tools.pdf_restore.package import page_transform

S, E = literal.START, literal.END


def fixture():
    template = json.loads((Path(__file__).parents[1] / 'examples/pdf-article.json').read_bytes())
    pin = lambda path: dict(path=path, sha256='0' * 64, bytes=0)
    originals = []
    for n, code in enumerate(('10 PRINT 1\n', '\n;               END\n'), 1):
        t, c, g = 't' + str(n), 'c' + str(n), 'g' + str(n)
        assets = {id: pin(id + '.png') for id in (t, c, g)}
        page = dict(pdf_index=n-1, pdf_page=n, printed_page=str(n+10), width_pt=100,
            height_pt=200, rotation=0, MediaBox=[0, 0, 100, 200], CropBox=[0, 0, 100, 200])
        page['pdf_to_upright_normalized'] = page_transform(page)
        blocks = [dict(id=id, kind=kind, region_ids=[id], text=text,
            correction_evidence=['corrections.json#' + id], uncertainties=[])
            for id, kind, text in ((t, 'prose', '가\n가'), (c, 'code', code))]
        p = deepcopy(template)
        p.update(pages=[page], regions=[dict(id=id, pdf_index=n-1,
            kind='figure' if id==g else 'code' if id==c else 'prose',
            bbox=[0, i/3, 1, (i+1)/3], notes='Synthetic observed source')
            for i, id in enumerate((t, c, g))], blocks=blocks,
            content_order=[dict(type='block', id=t), dict(type='block', id=c), dict(type='figure', id=g)],
            figures=[dict(id=g, region_ids=[g], asset=assets[g], caption=None)],
            region_assets=[dict(region_id=id, asset=asset) for id, asset in assets.items()],
            mapping=dict(status='mapped', evidence=['Observed source'], uncertainties=[]),
            availability='partial', gaps=[], verification=dict(status='sample-reviewed',
            reviewed_region_ids=[t, c, g], evidence=['Compared source'], uncertainties=[]))
        bounds = block_ranges(p)
        correction = dict(records=[dict(id=id, region_ids=[id], scan=assets[id], raw_ocr=None,
            block_ids=[id] if id!=g else []) for id in (t, c, g)], blocks=deepcopy(blocks),
            segment_scope=dict(boundary_pdf_span=[1, 2], current_pdf_pages=[n],
                deferred_pdf_pages=[2] if n==1 else []),
            caption_associations_pending=[], regional_text_index=[], regional_listing_index=[],
            listing_index=[dict(block_id=c, region_ids=[c], download='listing.txt', **{S: 0, E: len(code.encode())})],
            listing_line_index=[], future_scalar=dict(label='Keep literal', execution_verified=False))
        for block in blocks:
            a, z = bounds[block['id']]
            correction['regional_text_index'].append(dict(block_id=block['id'], region_id=block['id'],
                scan=assets[block['id']], download='article.txt', **{S: a, E: z}, transcription_excerpt=block['text']))
        correction['regional_listing_index'] = [dict(block_id=c, region_id=c, scan=assets[c],
            download='listing.txt', **{S: 0, E: len(code.encode())}, transcription_excerpt=code)]
        cur = 0
        for ordinal, line in enumerate(code.splitlines(True), 1):
            end = cur + len(line.encode())
            correction['listing_line_index'].append(dict(block_id=c, region_id=c, scan=assets[c],
                download='listing.txt', **{S: cur, E: end}, physical_line=ordinal,
                article_physical_line=ordinal, printed_line=10 if n==1 else None,
                printed_line_visible=n==1, text=line[:-1], source_bytes='unverified', execution_verified=False))
            cur = end
        if n==1:
            correction['future_index'] = [dict(block_id=t, region_id=t, scan=assets[t], download='article.txt',
                cells=[{S: 0, E: 3, 'transcription_excerpt': '가'},
                       {S: 3, E: 3, 'transcription_excerpt': '', 'blank': True}],
                external=pin('archive/prior.json'))]
        originals.append((p, correction))
    recipe = dict(index_mode=literal.FORMAT, segments=[dict(name=name,
        manifest=pin(name + '/manifest.json')) for name in ('one', 'two')],
        expected_pdf_pages=[1, 2], evidence=['Both source pages reviewed.'],
        uncertainties=['Source bytes and execution unverified.'], resolved_notes=[])
    return recipe, originals


class DesignLiteralTests(unittest.TestCase):
    def test_future_nested_categories_blank_cells_and_all_native_metadata_survive(self):
        recipe, sources = fixture(); before = deepcopy(sources)
        package, result = literal.project(recipe, sources)
        self.assertEqual(sources, before)
        self.assertEqual([r['original'] for r in result['native_metadata']], [c for _, c in sources])
        row = result['future_index'][0]
        self.assertEqual(row['cells'][1][S], 3)
        self.assertEqual(row['cells'][1][E], 3)
        self.assertEqual(row['scan']['path'], 'segments/one/t1.png')
        self.assertEqual(row['external']['path'], 'archive/prior.json')
        trace = [r for r in result['native_array_ranges'] if r['category']=='future_index']
        self.assertEqual([(r['first_row'], r['end_row_exclusive']) for r in trace], [(0, 1), (1, 1)])

    def test_basic_labels_comment_end_and_physical_rows_are_not_reinterpreted(self):
        recipe, sources = fixture(); package, result = literal.project(recipe, sources)
        self.assertEqual(base.text_bytes(package)[1], b'10 PRINT 1\n\n;               END\n')
        self.assertEqual(result['listing_line_index'][0]['printed_line'], 10)
        self.assertEqual(result['listing_line_index'][-1]['text'], ';               END')
        self.assertEqual([r['article_physical_line'] for r in result['listing_line_index']], [1, 2, 3])
        self.assertFalse(result['coverage']['execution_verified'])
        self.assertEqual(result['coverage']['human_acceptance'], 'pending')

    def test_repeated_text_cannot_be_assigned_to_another_block_or_region(self):
        for key in ('block_id', 'region_id'):
            recipe, sources = fixture(); sources[0][1]['future_index'][0][key] = 'c1'
            with self.assertRaises(ValueError):
                literal.project(recipe, sources)

    def test_wrong_source_scan_is_rejected(self):
        recipe, sources = fixture(); row = sources[0][1]['future_index'][0]
        row['scan'] = {**row['scan'], 'path': 'wrong.png'}
        with self.assertRaisesRegex(ValueError, 'scan differs'):
            literal.project(recipe, sources)

    def test_empty_range_inside_a_multibyte_glyph_is_rejected(self):
        recipe, sources = fixture(); cell=sources[0][1]['future_index'][0]['cells'][1]
        cell.update({S: 1, E: 1})
        with self.assertRaisesRegex(ValueError, 'UTF-8'):
            literal.project(recipe, sources)

    def test_changed_physical_row_text_is_rejected(self):
        recipe, sources = fixture(); sources[1][1]['listing_line_index'][-1]['text'] = 'END'
        with self.assertRaisesRegex(ValueError, 'Physical listing row'):
            literal.project(recipe, sources)

    def test_unreviewed_caption_link_cannot_be_silently_resolved(self):
        recipe, sources = fixture(); sources[0][1]['caption_associations_pending'] = [dict(id='future')]
        with self.assertRaisesRegex(ValueError, 'caption association'):
            literal.project(recipe, sources)

    def test_incomplete_final_scope_cannot_be_promoted(self):
        recipe, sources = fixture(); sources[-1][1]['segment_scope']['deferred_pdf_pages'] = [3]
        with self.assertRaisesRegex(ValueError, 'still defers'):
            literal.project(recipe, sources)

    def test_duplicate_native_identities_are_rejected(self):
        recipe, sources = fixture(); sources[1] = deepcopy(sources[0])
        sources[1][0]['pages'][0].update(pdf_index=1, pdf_page=2)
        for r in sources[1][0]['regions']:r['pdf_index']=1
        sources[1][1]['segment_scope'].update(current_pdf_pages=[2], deferred_pdf_pages=[])
        with self.assertRaises(ValueError):
            literal.project(recipe, sources)

    def test_other_formats_delegate_and_exception_restores_dispatchers(self):
        with patch.object(literal.perspective, 'project', return_value=('delegated', None)) as delegate:
            self.assertEqual(literal.project({'index_mode': 'older-format'}, []), ('delegated', None))
            delegate.assert_called_once()
        previous = base.project, base.validate_recipe
        with self.assertRaisesRegex(RuntimeError, 'intentional'):
            with literal.installed():
                self.assertIs(base.project, literal.project)
                raise RuntimeError('intentional')
        self.assertEqual((base.project, base.validate_recipe), previous)


if __name__ == '__main__':
    unittest.main()
