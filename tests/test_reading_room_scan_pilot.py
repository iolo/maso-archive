"""Pilot export keeps unfinished eligibility separate from completed issue data."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from tests import test_image_assemble as image_fixtures
from tools.pdf_restore.inventory import pin
from tools.reading_room.check import check
from tools.reading_room.export import digest, read, write
from tools.reading_room.scan_pilot import canonical, export, report
from tools.pdf_restore.issue import inventory


class ScanPilotTests(unittest.TestCase):
    def fixture(self, root):
        recipe = read(image_fixtures.ImageAssemblyTests().fixture(root))
        directory = root / Path(recipe['segments'][0]['manifest']['path']).parent
        package = read(directory / 'article.json')
        issue_id, id = package['issue_id'], package['toc_entry_id']
        rows = [dict(id=id, issue_id=issue_id, title_candidate=package['title'], parent_id=None,
                     depth=0, byline_candidate=None, start_page_candidate=None, kind_candidate='unknown')]
        rows += [dict(rows[0], id=id+'-'+kind, title_candidate=kind) for kind in ['group', 'pending']]
        toc = root / 'toc'
        write(toc, 'issues.json', [dict(id=issue_id, year=1900, month=1, original_label='Synthetic')])
        (toc / 'toc-entries.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
        entries = [dict(toc_entry_id=id, title=package['title'], parent_id=None,
                        classification='article', body_owner=True, availability=package['availability'],
                        verification=package['verification']['status'],
                        package=dict(path=directory.relative_to(root).as_posix(),
                                     manifest=pin(root, (directory/'manifest.json').relative_to(root).as_posix())))]
        entries += [dict(toc_entry_id=r['id'], title=r['title_candidate'], parent_id=None,
                         classification=kind, body_owner=owner)
                    for r, kind, owner in [(rows[1], 'group-heading', False), (rows[2], 'unclassified', None)]]
        ledger = dict(issue_id=issue_id, source_type='jpeg-set', canonical_identities=3,
                      readable_articles=int(package['availability']=='readable'),
                      partial_articles=int(package['availability']=='partial'),
                      identitiesAwaitingDisposition=1, group_headings=1, entries=entries)
        path = write(root, 'ledger.json', ledger)
        return path, toc, directory, package

    def test_offline_export_preserves_selected_package_and_pending_identities(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            ledger, toc, directory, package = self.fixture(root)
            before = inventory(directory)
            output = root / 'reader/data'
            result = export(ledger, toc, output, root)
            self.assertEqual(result['pilot']['unclassified'], 1)
            self.assertEqual(check(output)['articles'], 1)
            self.assertEqual(inventory(directory), before)
            copied = output/'source/pdf'/package['id']
            self.assertEqual(inventory(copied), before)
            issue = read(output / f'issues/{package["issue_id"].removeprefix("maso-")}.json')
            self.assertNotIn('scanRestoration', issue)
            self.assertEqual(issue['toc'][2]['restorationKind'], 'unclassified')
            self.assertEqual(issue['toc'][2]['articleIds'], [])
            doc = read(output / f'articles/{package["id"]}.json')
            self.assertEqual(doc['scan']['pages'], package['pages'])
            self.assertEqual(doc['article']['scanSourceKind'], 'jpeg-set')
            self.assertIn('JPEG', doc['media'][0]['conversion_note'])
            with self.assertRaisesRegex(ValueError, 'fresh'):
                export(ledger, toc, output, root)

    def test_rehashed_reader_link_search_and_accounting_tampering_reject(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            ledger, toc, _, package = self.fixture(root)
            output = root / 'reader/data'
            export(ledger, toc, output, root)
            manifest = read(output / 'manifest.json')
            issue_path = f'issues/{package["issue_id"].removeprefix("maso-")}.json'
            for name, mutate in [
                (issue_path, lambda d: d['toc'][2].update(restorationKind='group-heading')),
                (issue_path, lambda d: d['issue'].update(year=1999)),
                ('search.json', lambda d: d['items'][0].update(title='invented')),
                ('pilot/report.json', lambda d: d['counts'].update(unclassified=0)),
                ('manifest.json', lambda d: d.update(pilotIssues=[])),
            ]:
                path = output / name
                original = path.read_bytes()
                data = read(path); mutate(data); write(output, name, data)
                if name != 'manifest.json':
                    updated = deepcopy(manifest); updated['files'] = inventory(output)
                    write(output, 'manifest.json', updated)
                with self.subTest(name=name), self.assertRaises(ValueError):
                    check(output)
                path.write_bytes(original); write(output, 'manifest.json', manifest)
            # Removing both report declarations must not bypass JPEG accounting.
            original_issue = (output / issue_path).read_bytes()
            issue = read(output / issue_path); issue.pop('scanPilot')
            write(output, issue_path, issue)
            stripped = deepcopy(manifest); stripped['pilotIssues'] = []; stripped['files'] = inventory(output)
            write(output, 'manifest.json', stripped)
            with self.assertRaisesRegex(ValueError, 'Pilot issue accounting coverage'):
                check(output)
            (output / issue_path).write_bytes(original_issue); write(output, 'manifest.json', manifest)
            copied = output/'source/pdf'/package['id']/'article.txt'
            copied.write_bytes(b'corrupt')
            changed = deepcopy(manifest); changed['files'] = inventory(output)
            write(output, 'manifest.json', changed)
            with self.assertRaises(ValueError):
                check(output)

    def test_unknown_ownership_counts_and_wrong_selection_reject(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            path, toc, _, package = self.fixture(root)
            ledger = read(path)
            rows = [json.loads(line) for line in (toc/'toc-entries.jsonl').read_text().splitlines()]
            canonical_rows = canonical(rows, package['issue_id'])
            for fault in ['pending-owner', 'counts', 'source-kind', 'missing-package']:
                changed = deepcopy(ledger); packages = {package['toc_entry_id']: deepcopy(package)}
                if fault == 'pending-owner': changed['entries'][2]['body_owner'] = False
                elif fault == 'counts': changed['identitiesAwaitingDisposition'] = 0
                elif fault == 'source-kind': packages[package['toc_entry_id']]['source']['kind'] = 'pdf'
                else: packages = {}
                with self.subTest(fault=fault), self.assertRaises(ValueError):
                    report(changed, canonical_rows, packages)


if __name__ == '__main__':
    unittest.main()
