"""Synthetic evidence boundaries and preservation for scan/CD comparisons."""
import json
from pathlib import Path
import tempfile
import unittest

import test_pdf_build
from tools.pdf_restore.build import build as build_article
from tools.pdf_restore.compare import build, check_comparison, review
from tools.pdf_restore.inventory import pin, write_json


class PDFCompareTests(unittest.TestCase):
    def fixture(self, root):
        recipe_path = test_pdf_build.PDFBuildTests().fixture(root, with_code=False)
        corrections_path = recipe_path.parent / 'corrections.json'
        corrections = json.loads(corrections_path.read_bytes())
        body = ('This synthetic paragraph supplies substantial shared body evidence for a reviewed association. '
                'The scan retains its original ending.')
        corrections['blocks'][0]['text'] = body
        corrections['blocks'][1].update(kind='byline', text='Writer A')
        write_json(corrections_path, corrections)
        recipe = json.loads(recipe_path.read_bytes())
        recipe['corrections'] = pin(recipe_path.parent, 'corrections.json')
        write_json(recipe_path, recipe)
        scan = root / 'build/scan'
        package = build_article(recipe_path, scan, root)
        cd = root / 'private/cd'
        cd.mkdir()
        texts = ['issue 2\n', 'Writer A\n', body.replace('original ending', 'CD wording') + '\n']
        (cd / 'article.txt').write_text(''.join(texts))
        offset, paragraphs = 0, []
        for i, text in enumerate(texts):
            paragraphs.append(dict(id=f'p{i}', character_offset=offset, characters=len(text)))
            offset += len(text)
        write_json(cd / 'paragraphs.json', paragraphs)
        write_json(cd / 'reference.json', dict(reference='synthetic', issue_id=package['issue_id']))
        span = lambda i: dict(paragraph_id=f'p{i}', range=[0, len(texts[i])])
        recipe = dict(inputs=dict(scan_package=pin(root, 'build/scan/article.json'),
                      cd_text=pin(root, 'private/cd/article.txt'), cd_reference=pin(root, 'private/cd/reference.json'),
                      cd_paragraphs=pin(root, 'private/cd/paragraphs.json')), pdf_pages=[1],
                      association=dict(cd_reference='synthetic', issue_page=dict(cd_span=span(0), observed_cd_label=texts[0],
                      pdf_page=1, printed_page='2'), anchors=[dict(kind='byline', scan_block='r3-block', shared_text='Writer A', cd_span=span(1)),
                      dict(kind='body', scan_block='r1-block', shared_text=body[:90], cd_span=span(2))]),
                      units=[dict(scan_block=id, cd_spans=[span(i)], classification='Observed variant', review_note='Compared synthetic evidence.')
                             for id, i in [('r1-block', 2), ('r3-block', 1)]],
                      figure_reviews=[dict(scan_figure='figure', scan_region_ids=['r2'], review_note='Scan-only synthetic figure.')],
                      limits=['Only selected sample evidence; no complete CD verification.'])
        path = root / 'private/recipe.json'
        write_json(path, recipe)
        return path, recipe

    def test_reproducible_exact_offsets_separate_sources_and_tamper_check(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path, recipe = self.fixture(root)
            before = {p: p.read_bytes() for directory in ('private/cd', 'build/scan')
                      for p in (root / directory).rglob('*') if p.is_file()}
            one, two = root / 'build/one', root / 'build/two'
            result = build(path, one, root)
            build(path, two, root)
            files = lambda d: {p.relative_to(d): p.read_bytes() for p in d.rglob('*') if p.is_file()}
            self.assertEqual(files(one), files(two))
            self.assertEqual(check_comparison(one), result)
            self.assertTrue(all(p.read_bytes() == raw for p, raw in before.items()))
            self.assertEqual((one / 'inputs/cd_text.txt').read_bytes(), (root / 'private/cd/article.txt').read_bytes())
            text = (one / 'inputs/cd_text.txt').read_text()
            for unit in result['units']:
                self.assertEqual(unit['cd_text'], ''.join(text[s['article_range'][0]:s['article_range'][1]] for s in unit['cd_spans']))
                patched = unit['cd_text']
                for d in reversed(unit['differences']):
                    a, b = d['cd_range']
                    self.assertEqual(unit['cd_text'][a:b], d['cd_text'])
                    patched = patched[:a] + d['scan_text'] + patched[b:]
                self.assertEqual(patched, unit['scan_text'])
            self.assertFalse(result['relationship']['whole_cd_article_verified'])
            self.assertTrue((one / 'scan/ocr/r1.txt').is_file())
            self.assertTrue((one / 'scan/corrections.json').is_file())
            with self.assertRaisesRegex(ValueError, 'already exists'):
                build(path, one, root)
            (one / 'inputs/cd_text.txt').write_text('tampered')
            with self.assertRaisesRegex(ValueError, 'hash/size'):
                check_comparison(one)

    def test_title_only_wrong_offsets_and_missing_dispositions_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path, original = self.fixture(root)
            mutations = [
                (lambda r: r['association'].update(anchors=[]), 'Title alone'),
                (lambda r: r['units'][0]['cd_spans'][0].update(range=[0, 99999]), 'bounds'),
                (lambda r: r['units'].pop(), 'Every complete block'),
                (lambda r: r.update(pdf_pages=[1, 2, 3]), 'one or two'),
                (lambda r: r['association']['anchors'][1].update(shared_text='Invented words'), 'both selected sources'),
                (lambda r: r['units'][0].update(findings=[dict(cd_excerpt='Invented', scan_excerpt='Invented', scan_region_ids=['r1'])]), 'both excerpts'),
            ]
            for mutate, message in mutations:
                with self.subTest(message=message):
                    recipe = json.loads(json.dumps(original))
                    mutate(recipe)
                    with self.assertRaisesRegex(ValueError, message):
                        review(recipe, root)

    def test_modified_cd_is_rejected_before_export(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path, recipe = self.fixture(root)
            (root / recipe['inputs']['cd_text']['path']).write_text('changed')
            with self.assertRaisesRegex(ValueError, 'hash/size'):
                build(path, root / 'build/output', root)
            self.assertFalse((root / 'build/output').exists())


if __name__ == '__main__':
    unittest.main()
