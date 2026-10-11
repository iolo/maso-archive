"""Explicit segment-boundary links preserve bytes, scans and local identities."""
from copy import deepcopy
import unittest

from tools.pdf_restore.assembly_wrapped import join_boundaries, validate_boundary_joins
from tools.pdf_restore.assembly_indexes import START, END, span


class WrappedBoundaryTests(unittest.TestCase):
    def fixture(self):
        texts = ['270 PRINT "한\n', '글":A=\n', '1\n', '280 END\n']
        data = ''.join(texts).encode()
        rows, cursor = [], 0
        for i, text in enumerate(texts):
            end = cursor + len(text.encode())
            part = dict(region_id=f'r{i}', scan={'path': f'scan-{i}.png'}, **{START: cursor, END: end})
            rows.append(dict(part, source_segment='first' if i == 0 else 'second',
                source_line_id=f'p{i}', line_id=f'physical:{i}', listing_id='program',
                row_kind='numbered' if i in (0, 3) else 'unnumbered',
                source_range={START: 0 if i in (0, 1) else cursor-len(texts[0].encode()),
                              END: end if i == 0 else end-len(texts[0].encode())},
                printed_line=270 if i == 0 else 280 if i == 3 else None,
                printed_line_visible=i in (0, 3), segments=[part]))
            cursor = end
        rows[0]['logical_line_id'] = 'program:270:1'
        logical = dict(listing_id='program', source_segment='first', source_line_id='local:270',
                       line_id='program:270:1', printed_line=270, **{START: 0, END: rows[0][END]},
                       source_parts=['physical:0'], segments=deepcopy(rows[0]['segments']))
        c = dict(listing_line_index=rows, logical_listing_line_index=[logical], data_statements=[],
                 listing_groups=[dict(listing_id='program', unnumbered_rows=2)], resolved_continuations=[])
        recipe = dict(segments=[dict(name='first'), dict(name='second')], wrapped_listing_joins=[dict(
            left=dict(segment='first', logical_line_id='local:270', ending='한\n'),
            right=dict(segment='second', physical_line_ids=['p1', 'p2'], opening='글'))])
        return recipe, c, data

    def test_utf8_two_row_boundary_preserves_physical_evidence(self):
        recipe, c, data = self.fixture()
        before = deepcopy(c['listing_line_index'])
        join_boundaries(recipe, c, data)
        logical = c['logical_listing_line_index'][0]
        self.assertEqual(span(logical, data), '270 PRINT "한\n글":A=\n1\n')
        self.assertEqual(logical['source_parts'], ['physical:0', 'physical:1', 'physical:2'])
        self.assertEqual(len(logical['segments']), 3)
        for old, row in zip(before, c['listing_line_index']):
            for field in (START, END, 'scan', 'segments', 'source_range', 'source_line_id', 'printed_line'):
                self.assertEqual(row[field], old[field])
        self.assertEqual(c['listing_line_index'][1]['source_row_kind'], 'unnumbered')
        self.assertEqual(c['listing_line_index'][1]['continues_printed_line'], 270)
        self.assertEqual(c['listing_groups'][0]['unnumbered_rows'], 0)
        self.assertFalse(c['resolved_continuations'][0]['bytes_changed'])

    def test_rejects_partial_reordered_nonadjacent_and_wrong_evidence(self):
        for change in ('partial', 'reversed', 'wrong-text', 'wrong-target', 'gap', 'other-listing', 'data', 'duplicate'):
            recipe, c, data = self.fixture()
            right = recipe['wrapped_listing_joins'][0]['right']
            if change == 'partial': right['physical_line_ids'].pop()
            if change == 'reversed': right['physical_line_ids'].reverse()
            if change == 'wrong-text': right['opening'] = '다'
            if change == 'wrong-target': recipe['wrapped_listing_joins'][0]['left']['logical_line_id'] = 'missing'
            if change == 'gap': c['listing_line_index'][1][START] += 1
            if change == 'other-listing': c['listing_line_index'][2]['listing_id'] = 'other'
            if change == 'data': c['data_statements'] = [dict(line_id='program:270:1')]
            if change == 'duplicate': recipe['wrapped_listing_joins'] *= 2
            with self.subTest(change=change), self.assertRaises(ValueError):
                join_boundaries(recipe, c, data)

    def test_recipe_rejects_nonadjacent_segments(self):
        recipe, _, _ = self.fixture()
        recipe['segments'].insert(1, dict(name='intervening'))
        with self.assertRaises(ValueError):
            validate_boundary_joins(recipe)
