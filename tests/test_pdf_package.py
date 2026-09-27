"""Synthetic geometry, reading order, exclusion and missing-page fixtures."""
import copy
import json
from pathlib import Path
import unittest

from tools.pdf_restore.package import page_transform, validate_package

EXAMPLE = Path(__file__).resolve().parents[1] / 'examples/pdf-article.json'


def page(index, rotation=0):
    row = dict(pdf_index=index, pdf_page=index + 1, printed_page=None,
               width_pt=100, height_pt=200, rotation=rotation,
               MediaBox=[10, 20, 110, 220], CropBox=[10, 20, 110, 220])
    row['pdf_to_upright_normalized'] = page_transform(row)
    return row


def region(name, index, box):
    return dict(id=name, pdf_index=index, bbox=box, kind='prose', notes='Synthetic')


class PDFPackageTests(unittest.TestCase):
    def package(self):
        return json.loads(EXAMPLE.read_bytes())

    def test_all_rotations_and_nonzero_origin(self):
        expected = {0: [(0, 1), (1, 0)], 90: [(0, 0), (1, 1)],
                    180: [(1, 0), (0, 1)], 270: [(1, 1), (0, 0)]}
        for rotation, corners in expected.items():
            matrix = page_transform(page(0, rotation))
            a, b, c, d, e, f = matrix
            for (x, y), (u, v) in zip([(10, 20), (110, 220)], corners):
                self.assertAlmostEqual(a*x+c*y+e, u)
                self.assertAlmostEqual(b*x+d*y+f, v)

    def test_noncontiguous_order_and_printed_numbers_are_independent(self):
        p = self.package()
        p['pages'] = [page(12), page(15)]
        p['pages'][0]['printed_page'] = 'iv'
        p['regions'] = [region('first', 15, [0, 0, .4, 1]), region('continuation', 12, [.5, 0, 1, 1])]
        before = copy.deepcopy(p)
        validate_package(p)
        self.assertEqual(p, before)  # Reading order is not silently sorted by PDF page.
        p['pages'][0]['pdf_page'] = 12
        with self.assertRaisesRegex(ValueError, 'numbering'):
            validate_package(p)

    def test_shared_page_excludes_advertisement(self):
        p = self.package()
        p['pages'] = [page(0)]
        p['regions'] = [region('body', 0, [0, 0, 1, .5])]
        p['excluded_regions'] = [region('ad', 0, [0, .5, 1, 1])]
        p['excluded_regions'][0]['kind'] = 'advertisement'
        validate_package(p)
        p['regions'][0]['bbox'][3] = .51
        with self.assertRaisesRegex(ValueError, 'excluded material'):
            validate_package(p)

    def test_missing_page_is_explicit_not_an_invented_region(self):
        p = self.package()
        validate_package(p)  # An unresolved outcome with an explicit gap is legal.
        p['regions'] = [region('missing', 2, [0, 0, 1, 1])]
        with self.assertRaisesRegex(ValueError, 'unmapped page'):
            validate_package(p)

    def test_wrong_transform_and_unsupported_review_are_rejected(self):
        p = self.package()
        p['pages'] = [page(0, 90)]
        p['regions'] = [region('body', 0, [0, 0, 1, 1])]
        p['pages'][0]['pdf_to_upright_normalized'][0] = 1
        with self.assertRaisesRegex(ValueError, 'Rotation transform'):
            validate_package(p)
        p['pages'][0] = page(0, 90)
        p['verification']['status'] = 'fully-reviewed'
        with self.assertRaisesRegex(ValueError, 'all mapped regions'):
            validate_package(p)
        p['verification']['reviewed_region_ids'] = ['body']
        validate_package(p)

    def test_id_is_independent_of_title_and_paths_are_safe(self):
        p = self.package()
        p['title'] = 'Corrected OCR title'
        validate_package(p)
        p['source']['path'] = '../secret'
        with self.assertRaisesRegex(ValueError, 'safe package-relative'):
            validate_package(p)


if __name__ == '__main__':
    unittest.main()
