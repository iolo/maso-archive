"""Regressions for literal CP/M blank fields, UTF-8 and nested source ranges."""
from copy import deepcopy
import unittest

from tools.pdf_restore import assemble as base
from tools.pdf_restore import cpm_literal_assembly as cpm


class LiteralRangeTests(unittest.TestCase):
    def project(self, value, **kwargs):
        defaults = dict(article='가\t\n나'.encode(), listing=b'0100 |  | ORG 100H\n',
            article_offset=11, listing_offset=31, prefix='segments/end',
            local_paths={'scan.png'})
        defaults.update(kwargs)
        return cpm.project_record(value, **defaults)

    def test_blank_cell_keeps_zero_width_at_its_actual_utf8_position(self):
        value = dict(download='article.txt', utf8_byte_start=4,
            utf8_byte_end_exclusive=4, transcription_excerpt='', blank=True)
        result = self.project(value)
        self.assertEqual((result[cpm.START], result[cpm.END]), (15, 15))
        self.assertEqual(result['transcription_excerpt'], '')
        self.assertEqual(value[cpm.START], 4)

    def test_empty_range_inside_multibyte_glyph_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'UTF-8'):
            self.project(dict(download='article.txt', utf8_byte_start=1,
                utf8_byte_end_exclusive=1, transcription_excerpt=''))

    def test_nested_compiler_cell_inherits_listing_coordinate_system(self):
        value = dict(download='listing.txt', cells=[dict(utf8_byte_start=7,
            utf8_byte_end_exclusive=7, transcription_excerpt='', blank=True)],
            scan=dict(path='scan.png', sha256='0'*64, bytes=1))
        original = deepcopy(value)
        result = self.project(value)
        self.assertEqual(result['cells'][0][cpm.START], 38)
        self.assertEqual(result['cells'][0][cpm.END], 38)
        self.assertEqual(result['scan']['path'], 'segments/end/scan.png')
        self.assertEqual(value, original)

    def test_wrong_occurrence_excerpt_and_unknown_download_are_rejected(self):
        for value in [dict(download='article.txt', utf8_byte_start=0,
                          utf8_byte_end_exclusive=3, transcription_excerpt='나'),
                      dict(download='source.txt', utf8_byte_start=0,
                          utf8_byte_end_exclusive=0)]:
            with self.assertRaises(ValueError):
                self.project(value)

    def test_table_position_and_external_pin_keep_distinct_coordinate_systems(self):
        value = dict(table_utf8_byte_start=3, table_utf8_byte_end_exclusive=8,
                     evidence=dict(path='archive/original.json', sha256='1'*64, bytes=8))
        result = self.project(value)
        self.assertEqual(result['table_utf8_byte_start'], 14)
        self.assertEqual(result['table_utf8_byte_end_exclusive'], 19)
        self.assertEqual(result['evidence'], value['evidence'])

    def test_scoped_installation_restores_dispatcher_after_exception(self):
        previous = (base.project, base.validate_recipe)
        with self.assertRaisesRegex(RuntimeError, 'intentional'):
            with cpm.installed():
                self.assertIs(base.project, cpm.project)
                raise RuntimeError('intentional')
        self.assertEqual((base.project, base.validate_recipe), previous)


if __name__ == '__main__':
    unittest.main()
