"""Regressions for exact nested occurrences and immutable source supersession."""
from copy import deepcopy
import unittest

from tools.pdf_restore import assemble as base
from tools.pdf_restore import perspective_literal_assembly as literal

S, E = literal.START, literal.END


class PerspectiveRangeTests(unittest.TestCase):
    def project(self, value):
        return literal.project_record(value, article='가\n나'.encode(), listing=b'10 X\n',
            ranges={'one': (0, 3), 'two': (4, 7)}, targets={'one': (10, 13), 'two': (31, 34)},
            listing_offset=20, prefix='segments/base', local_paths={'scan.png'})

    def test_repeated_content_uses_its_own_block_position(self):
        row = dict(block_id='two', download='article.txt', **{S: 4, E: 7}, transcription_excerpt='나')
        self.assertEqual((self.project(row)[S], self.project(row)[E]), (31, 34))
        with self.assertRaisesRegex(ValueError, 'own active block'):
            self.project({**row, 'block_id': 'one'})

    def test_nested_ranges_inherit_download_and_block(self):
        row = dict(block_id='two', download='article.txt', cells=[{S: 4, E: 7, 'transcription_excerpt': '나'}])
        self.assertEqual(self.project(row)['cells'][0][S], 31)
        self.assertEqual(row['cells'][0][S], 4)

    def test_utf8_boundaries_and_wrong_excerpts_are_rejected(self):
        for start, end, text in [(1, 2, ''), (4, 7, '가')]:
            with self.assertRaises(ValueError):
                self.project(dict(block_id='two', download='article.txt', **{S: start, E: end}, transcription_excerpt=text))

    def test_listing_and_zero_width_positions_keep_literal_bytes(self):
        row = dict(download='listing.txt', **{S: 3, E: 3}, transcription_excerpt='')
        self.assertEqual((self.project(row)[S], self.project(row)[E]), (23, 23))

    def test_local_scan_and_external_provenance_are_distinct(self):
        local = dict(path='scan.png', sha256='0'*64, bytes=1)
        external = dict(path='archive/prior.json', sha256='1'*64, bytes=2)
        result = self.project(dict(scan=local, external=external))
        self.assertEqual(result['scan']['path'], 'segments/base/scan.png')
        self.assertEqual(result['external'], external)

    def test_native_prose_boundary_uses_its_own_block_offset(self):
        row = dict(block_id='two', download='article.txt', join_utf8_byte=7)
        self.assertEqual(self.project(row)['join_utf8_byte'], 34)

    def test_exception_restores_nested_dispatchers(self):
        previous = base.project, base.validate_recipe
        with self.assertRaises(RuntimeError):
            with literal.installed():
                self.assertIs(base.project, literal.project)
                raise RuntimeError('intentional')
        self.assertEqual((base.project, base.validate_recipe), previous)


class SourceRevisionTests(unittest.TestCase):
    def fixture(self):
        spec = dict(target_segment='base', revision_segment='repair', region_id='r', block_id='b')
        pin = dict(path='base/manifest.json', sha256='0'*64, bytes=1)
        original = dict(id='same', issue_id='issue', toc_entry_id='toc', source={}, toc_pin={}, title='title', coordinates='upright',
            pages=[dict(pdf_index=0)], regions=[dict(id='r', pdf_index=0, bbox=[0, 0, .9, 1])],
            blocks=[dict(id='b', region_ids=['r'], text='음수(−1이면')], figures=[], content_order=[dict(type='block', id='b')])
        repaired = deepcopy(original);repaired['regions'][0]['bbox']=[0, 0, 1, 1];repaired['blocks'][0]['text']='음수(−1)이면'
        contract = dict(prior_pins=dict(manifest=pin), superseded_region_id='r', superseded_block_id='b',
            prior_bbox=[0, 0, .9, 1], selected_bbox=[0, 0, 1, 1],
            local_insertion_utf8_byte=len('음수(−1'.encode()), inserted_text=')',
            prior_text=original['blocks'][0]['text'], revised_text=repaired['blocks'][0]['text'])
        return spec, {'base': (original, {}), 'repair': (repaired, {'source_revision': contract})}, {'base': {'manifest': pin}}

    def test_one_observed_insertion_is_accepted_without_mutating_inputs(self):
        spec, sources, specs = self.fixture();snapshot=deepcopy(sources)
        self.assertEqual(literal.validate_revision(spec, sources, specs)['inserted_text'], ')')
        self.assertEqual(sources, snapshot)

    def test_semantic_changes_and_wrong_manifest_are_rejected(self):
        for change in ('text', 'pin'):
            spec, sources, specs = self.fixture()
            if change == 'text':sources['repair'][0]['blocks'][0]['text']='corrected math'
            else:specs['base']['manifest']={}
            with self.assertRaises(ValueError):literal.validate_revision(spec, sources, specs)

    def test_revision_cannot_duplicate_a_section_or_change_page_geometry(self):
        for change in ('block', 'page'):
            spec, sources, specs = self.fixture()
            if change == 'block':sources['repair'][0]['blocks'].append(deepcopy(sources['repair'][0]['blocks'][0]))
            else:sources['repair'][0]['pages']=[dict(pdf_index=1)]
            with self.assertRaises(ValueError):literal.validate_revision(spec, sources, specs)


if __name__ == '__main__':
    unittest.main()
