"""Issue ownership, batch staging, section targets and CD preservation gates."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import test_pdf_build
import test_pdf_reader
from test_pdf_reader import inventory, refresh
from tools.pdf_restore.build import build
from tools.pdf_restore.inventory import pin
from tools.pdf_restore.issue import AVAILABILITY, export
from tools.reading_room.check import check
from tools.reading_room.export import digest, read, write
from tools.reading_room.scan_issue import stage_issue


class PDFIssueTests(unittest.TestCase):
    def fixture(self, root):
        base, first, one = test_pdf_reader.PDFReaderTests().fixture(root, first_kind='title')
        other = root / 'second'
        recipe = test_pdf_build.PDFBuildTests().fixture(other, first_kind='title', toc_number='0002')
        second = other / 'build/scan'
        two = build(recipe, second, other)
        issue = read(base / 'issues/1900-01.json')
        first_toc = issue['toc'][0]
        section = dict(first_toc, id='maso-1900-01-toc-0003', parentId=first_toc['id'], depth=1, title='Internal section', kind='subtopic', page=None)
        group = dict(first_toc, id='maso-1900-01-toc-0004', title='Group', kind='heading', page=None)
        second_toc = dict(first_toc, id=two['toc_entry_id'], parentId=group['id'], depth=1)
        issue['toc'] = [first_toc, section, group, second_toc]
        issue['issue']['tocCount'] = 4
        write(base, 'issues/1900-01.json', issue)
        catalog = read(base / 'catalog.json')
        catalog['issues'][-1] = issue['issue']
        write(base, 'catalog.json', catalog)
        search = read(base / 'search.json')
        for t in (section, group, second_toc):
            search['items'].append(dict(kind='toc', id=t['id'], issueId=one['issue_id'], title=t['title'], byline=t['byline'], articleIds=[], status='unmatched'))
        write(base, 'search.json', search)
        manifest = read(base / 'manifest.json')
        manifest['counts']['tocEntries'] += 3
        manifest['files'] = inventory(base)
        write(base, 'manifest.json', manifest)
        entries = []
        for t, kind, p, folder in [(first_toc, 'article', one, first), (section, 'section-reference', None, None),
                                    (group, 'group-heading', None, None), (second_toc, 'article', two, second)]:
            row = dict(toc_entry_id=t['id'], title=t['title'], parent_id=t['parentId'], classification=kind, body_owner=kind == 'article', restoration=None)
            if p:
                row['restoration'] = dict(article_id=p['id'], availability='readable', verification='sample-reviewed',
                                          directory=folder.relative_to(root).as_posix(), manifest=pin(root, (folder / 'manifest.json').relative_to(root).as_posix()))
            if kind == 'section-reference':
                row.update(body_owner_toc_entry_id=first_toc['id'], section=dict(anchor='r1-block', anchor_scope='assembled-parent', heading_pdf_page=1))
            entries.append(row)
        ledger = dict(issue_id=one['issue_id'], entries=entries, counts=dict(toc_entries=4, classified_articles=2, group_headings=1,
                        section_references=1, unresolved_eligibility=0, restoration_availability={s: 2 if s == 'readable' else 0 for s in AVAILABILITY},
                        verification={'sample-reviewed': 2}))
        path = write(root, 'ledger.json', ledger)
        return base, path, one, two

    def test_issue_export_and_staging_preserve_bodies_and_cd_bytes(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            base, ledger, one, two = self.fixture(root)
            old = {p.relative_to(base): p.read_bytes() for p in base.rglob('*') if p.is_file()}
            reference, repeat = root / 'reference', root / 'repeat'
            export(ledger, base, reference, root)
            export(ledger, base, repeat, root)
            self.assertEqual(inventory(reference), inventory(repeat))
            self.assertEqual(len(list((reference / 'read').glob('*.html'))), 2)
            html = (reference / 'index.html').read_text()
            self.assertIn(f'read/{one["id"]}.html#r1-block', html)
            self.assertIn('group-heading', html)
            article_html = (reference / f'read/{one["id"]}.html').read_text()
            self.assertIn('href="../index.html"', article_html)
            self.assertIn(f'href="{two["id"]}.html"', article_html)
            self.assertIn(f'../articles/{one["id"]}/ocr/r1.png', article_html)
            output, again = root / 'reader', root / 'reader-repeat'
            stage_issue(base, ledger, output, root)
            stage_issue(base, ledger, again, root)
            self.assertEqual(inventory(output), inventory(again))
            self.assertEqual(check(output)['articles'], 6)
            issue = read(output / 'issues/1900-01.json')
            self.assertEqual(len(issue['articles']), 2)
            self.assertEqual(issue['toc'][1]['articleIds'], [one['id']])
            self.assertEqual(issue['toc'][1]['sectionRef'], dict(articleId=one['id'], blockId='r1-block'))
            self.assertEqual(issue['toc'][2]['articleIds'], [])
            for path, raw in old.items():
                self.assertEqual((base / path).read_bytes(), raw)
                if str(path).startswith(('articles/', 'source/')):
                    self.assertEqual((output / path).read_bytes(), raw)

    def test_bad_ownership_anchor_and_omissions_fail_before_publication(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            base, path, _, _ = self.fixture(root)
            original = read(path)
            mutations = [lambda l: l['entries'].pop(),
                         lambda l: l['entries'][1]['section'].update(anchor='r3-block'),
                         lambda l: l['entries'][1].update(body_owner_toc_entry_id=l['entries'][2]['toc_entry_id']),
                         lambda l: l['entries'][2].update(body_owner=True),
                         lambda l: l['counts']['restoration_availability'].update(readable=3)]
            for mutate in mutations:
                ledger = deepcopy(original)
                mutate(ledger)
                write(root, path.name, ledger)
                with self.assertRaises(ValueError):
                    stage_issue(base, path, root / 'output', root)
                self.assertFalse((root / 'output').exists())

    def test_rehashed_toc_link_and_section_target_tampering_is_rejected(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            base, ledger, _, two = self.fixture(root)
            output = root / 'reader'
            stage_issue(base, ledger, output, root)
            original = read(output / 'issues/1900-01.json')
            issue = deepcopy(original)
            issue['toc'][1]['articleIds'] = [two['id']]
            write(output, 'issues/1900-01.json', issue)
            refresh(output)
            with self.assertRaisesRegex(ValueError, 'ownership/link'):
                check(output)
            issue = deepcopy(original)
            report = read(output / 'scan-issues/1900-01.json')
            report['entries'][1]['sectionRef']['blockId'] = 'r3-block'
            issue['scanRestoration'] = report
            issue['toc'][1]['sectionRef']['blockId'] = 'r3-block'
            write(output, 'issues/1900-01.json', issue)
            write(output, 'scan-issues/1900-01.json', report)
            manifest = read(output / 'manifest.json')
            manifest['scanIssues'][0]['sha256'] = digest(output / 'scan-issues/1900-01.json')
            write(output, 'manifest.json', manifest)
            refresh(output)
            with self.assertRaisesRegex(ValueError, 'assembled heading'):
                check(output)


if __name__ == '__main__':
    unittest.main()
