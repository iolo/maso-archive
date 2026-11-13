"""Closed snapshots, mixed-source links and unlocated outcomes stay explicit."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import test_pdf_issue
from tools.pdf_restore.inventory import pin
from tools.pdf_restore.issue import export, inventory
from tools.reading_room.check import check
from tools.reading_room.export import digest, read, write
from tools.reading_room.frozen import check_package, validate_report
from tools.reading_room.rebuild import add_issue, export as export_reader, finish, save_cd_baseline


class RebuildTests(unittest.TestCase):
    def test_source_overlap_is_rejected_before_copying(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            spec = dict(issueId='maso-1900-01', manifest=dict(path='reference/manifest.json', sha256='0' * 64, bytes=0))
            inputs = write(root, 'inputs.json', dict(schemaVersion=1, issues=[spec]))
            with patch('tools.reading_room.rebuild.DATES', ('1900-01',)):
                with self.assertRaisesRegex(ValueError, 'overlap'):
                    export_reader(inputs, root / 'reference/reader', root / 'work', root)
            self.assertFalse((root / 'reference').exists())

    def test_low_space_is_rejected_before_creating_a_reader_copy(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            base = self.fixture(root, standalone=True)
            inputs = read(base / 'volunteer-inputs.json')
            inputs.update(schemaVersion=1, toc=pin(root, 'TOC.md'),
                          discs={d: pin(root, 'source.pdf') for d in ('cd1', 'cd2', 'cd3')})
            path = write(root, 'inputs.json', inputs)
            with patch('tools.reading_room.rebuild.DATES', ('1900-01',)), \
                    patch('tools.reading_room.rebuild.shutil.disk_usage', return_value=SimpleNamespace(free=0)):
                with self.assertRaisesRegex(ValueError, 'Insufficient staging space'):
                    export_reader(path, root / 'output/data', root / 'work', root)
            self.assertFalse((root / 'output').exists())
            self.assertFalse((root / 'work/data').exists())

    def fixture(self, root, standalone=False):
        base, ledger, _, _ = test_pdf_issue.PDFIssueTests().fixture(root)
        manifest = read(base / 'manifest.json')
        manifest.update(coverPolicy='thumbnail-v1', coverInputs=[])
        manifest['counts']['coverAssets'] = 0
        write(base, 'manifest.json', manifest)
        if standalone:
            reference = root / 'reference'
            export(ledger, base, reference, root)
            spec = dict(issueId='maso-1900-01', manifest=pin(root, 'reference/manifest.json'))
        else:
            selected = read(ledger)
            spec = dict(issueId=selected['issue_id'], ledger=pin(root, ledger.name),
                        packages=[dict(tocEntryId=r['toc_entry_id'], articleId=r['restoration']['article_id'],
                                       manifest=r['restoration']['manifest']) for r in selected['entries'] if r['body_owner']])
        inputs = dict(issues=[spec], canonicalTitleChanges={})
        save_cd_baseline(base, base)
        add_issue(base, spec, inputs, root)
        write(base, 'volunteer-inputs.json', inputs)
        manifest = read(base / 'manifest.json')
        manifest['volunteerInputs'] = pin(base, 'volunteer-inputs.json')
        manifest['cdBaseline'] = pin(base, 'cd-baseline.json')
        manifest['files'] = inventory(base)
        write(base, 'manifest.json', manifest)
        return base

    def test_finish_resumes_copied_data_and_preserves_cd_receipt(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            base = self.fixture(root)
            inputs = write(root, 'inputs.json', read(base / 'volunteer-inputs.json'))
            # The first interrupted export had not yet copied this tiny receipt.
            (base / 'source/pdf-issues/1900-01/ledger.json').unlink()
            output = root / 'reader/data'
            result = finish(inputs, base, output, root)
            self.assertFalse(base.exists())
            self.assertEqual(result['pdfArticles'], 2)
            self.assertEqual(result['preservedCdArticles'], 4)
            self.assertEqual(check(output)['articles'], 6)

    def test_rebuild_from_legacy_and_standalone_inputs_without_private_adapters(self):
        for standalone in (False, True):
            with self.subTest(standalone=standalone), TemporaryDirectory() as temp:
                base = self.fixture(Path(temp), standalone)
                self.assertEqual(check(base)['articles'], 6)
                self.assertEqual(len(read(base / 'manifest.json')['frozenIssues']), 1)

    def test_rehashed_package_manifest_cannot_replace_the_selected_snapshot(self):
        with TemporaryDirectory() as temp:
            base = self.fixture(Path(temp))
            source = read(base / 'manifest.json')['scanInputs'][0]
            folder = (base / 'source' / source['packagePath']).parent
            (folder / 'article.txt').write_text('Changed source')
            manifest = read(folder / 'manifest.json')
            manifest['files'] = inventory(folder)
            write(folder, 'manifest.json', manifest)
            with self.assertRaisesRegex(ValueError, 'selected closeout'):
                check_package(folder, source['manifestSha256'])

    def test_rehashed_outcome_and_projection_tampering_are_rejected(self):
        with TemporaryDirectory() as temp:
            base = self.fixture(Path(temp), True)
            original = read(base / 'scan-issues/1900-01.json')
            altered = deepcopy(original)
            altered['reviewNote'] = 'Invented full human acceptance'
            issue = read(base / 'issues/1900-01.json')
            issue['scanRestoration'] = altered
            write(base, 'issues/1900-01.json', issue)
            write(base, 'scan-issues/1900-01.json', altered)
            manifest = read(base / 'manifest.json')
            sha = digest(base / 'scan-issues/1900-01.json')
            manifest['scanIssues'][0]['sha256'] = sha
            manifest['frozenIssues'][0]['accountingSha256'] = sha
            manifest['files'] = inventory(base)
            write(base, 'manifest.json', manifest)
            with self.assertRaisesRegex(ValueError, 'original selected closeout'):
                check(base)

    def test_cd_links_survive_and_unlocated_leaf_cannot_gain_a_scan_body(self):
        with TemporaryDirectory() as temp:
            base = self.fixture(Path(temp))
            issue = read(base / 'issues/1900-01.json')
            report = issue['scanRestoration']
            packages = {}
            for source in read(base / 'manifest.json')['scanInputs']:
                p = check_package((base / 'source' / source['packagePath']).parent, source['manifestSha256'])
                packages[p['toc_entry_id']] = p
            issue['toc'][0]['articleIds'].append('cd1:article:existing')
            validate_report(issue, report, packages)
            row = dict(issue['toc'][0], id='maso-1900-01-toc-0005', title='Unlocated', articleIds=[], parentId=None)
            row.update(restorationKind='unresolved', restorationEligibility='eligible-canonical-toc-leaf')
            issue['toc'].append(row)
            outcome = {k: row[k] for k in ('id', 'parentId', 'depth', 'title', 'byline', 'page', 'kind')}
            outcome.update(classification='unresolved', bodyOwner=None, eligibility='eligible-canonical-toc-leaf', availability='unresolved')
            report['entries'].append(outcome)
            report['counts']['toc_entries'] += 1
            report['counts']['unresolved_body_locations'] = 1
            validate_report(issue, report, packages)
            # An announced supplement has resolved eligibility but its media and
            # printed body remain unrecovered, with no invented article link.
            row['restorationEligibility'] = outcome['eligibility'] = 'canonical-announced-media-supplement'
            report['counts']['unrecovered_announced_media'] = 1
            validate_report(issue, report, packages)
            report['counts']['unrecovered_announced_media'] = 0
            with self.assertRaisesRegex(ValueError, 'unrecovered-media count'):
                validate_report(issue, report, packages)
            report['counts']['unrecovered_announced_media'] = 1
            row['articleIds'] = [next(iter(packages.values()))['id']]
            with self.assertRaisesRegex(ValueError, 'ownership/link'):
                validate_report(issue, report, packages)


if __name__ == '__main__':
    unittest.main()
