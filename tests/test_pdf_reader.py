"""Synthetic v1/v2 compatibility and v3 scan projection/preservation gates."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import test_pdf_build
from tools.pdf_restore.build import build as build_article
from tools.reading_room.export import demo, digest, read, text_for, write
from tools.reading_room.check import check
from tools.reading_room.scan import project, stage


def inventory(root):
    return [dict(path=p.relative_to(root).as_posix(), bytes=p.stat().st_size, sha256=digest(p))
            for p in sorted(root.rglob('*')) if p.is_file() and p != root / 'manifest.json']


def refresh(root):
    manifest = read(root / 'manifest.json')
    manifest['files'] = inventory(root)
    write(root, 'manifest.json', manifest)


class PDFReaderTests(unittest.TestCase):
    def fixture(self, root, version=1):
        recipe = test_pdf_build.PDFBuildTests().fixture(root)
        scan = root / 'build/scan'
        package = build_article(recipe, scan, root)
        base = root / 'build/base'
        demo(base)
        summary = dict(id=package['issue_id'], year=1900, month=1, label='Synthetic',
                       articleCount=0, textCount=0, tocCount=1, cover=None)
        toc = dict(id=package['toc_entry_id'], parentId=None, depth=0, title=package['title'],
                   byline='Synthetic author', page=2, kind='article', articleIds=[])
        write(base, 'issues/1900-01.json', dict(schemaVersion=version, issue=summary, toc=[toc], articles=[]))
        write(base, 'media/1900-01.json', dict(schemaVersion=version, issueId=summary['id'], items=[]))
        catalog = read(base / 'catalog.json')
        catalog['schemaVersion'] = version
        catalog['issues'].append(summary)
        write(base, 'catalog.json', catalog)
        search = read(base / 'search.json')
        search['items'].append(dict(kind='toc', id=toc['id'], issueId=summary['id'], title=toc['title'],
                                    byline=toc['byline'], articleIds=[], status='unmatched'))
        write(base, 'search.json', search)
        write(base, 'manifest.json', dict(kind='reading-room-static', schemaVersion=version,
              counts=dict(issues=2, articles=4, texts=3, listings=3, mediaRecords=2, tocEntries=6), files=inventory(base)))
        check(base)
        return base, scan, package

    def test_v1_v2_baselines_keep_cd_bytes_and_export_deterministically(self):
        for version in (1, 2):
            with self.subTest(version=version), TemporaryDirectory() as tmp:
                root = Path(tmp)
                base, scan, package = self.fixture(root, version)
                old = {p.relative_to(base): p.read_bytes() for p in base.rglob('*') if p.is_file()}
                one, two = root / 'build/one', root / 'build/two'
                stage(base, scan, one)
                stage(base, scan, two)
                files = lambda folder: {p.relative_to(folder): p.read_bytes() for p in folder.rglob('*') if p.is_file()}
                self.assertEqual(files(one), files(two))
                self.assertEqual(files(base), old)
                self.assertEqual(check(one)['articles'], 5)
                for path, raw in old.items():
                    if str(path).startswith(('articles/', 'source/')):
                        self.assertEqual((one / path).read_bytes(), raw)
                doc = read(one / f'articles/{package["id"]}.json')
                self.assertEqual(doc['scan']['availability'], 'readable')
                self.assertEqual(doc['scan']['verification']['status'], 'sample-reviewed')
                self.assertEqual(doc['scan']['relationships'], [])
                self.assertEqual(doc['scan']['regions'][0]['bbox'], package['regions'][0]['bbox'])
                self.assertEqual(text_for(doc['blocks']).encode(), (scan / 'article.txt').read_bytes())
                code = next(b for b in doc['blocks'] if b['type'] == 'code')
                self.assertEqual(text_for([code]), package['blocks'][1]['text'])
                self.assertEqual(doc['blocks'][2]['scanFigureId'], 'figure')
                for download in doc['scan']['downloads']:
                    self.assertEqual(digest(one / 'source' / download['path']), download['sha256'])
                toc = read(one / 'issues/1900-01.json')['toc'][0]
                self.assertEqual(toc['articleIds'], [package['id']])
                self.assertEqual(read(one / 'search.json')['items'][-1]['sourceKind'], 'scan')
                with self.assertRaisesRegex(ValueError, 'fresh'):
                    stage(base, scan, one)

    def test_checker_rejects_rehashed_projection_and_provenance_changes(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            base, scan, package = self.fixture(root)
            output = root / 'build/output'
            stage(base, scan, output)
            path = f'articles/{package["id"]}.json'
            original = read(output / path)
            mutations = [lambda d: d['scan']['regions'][0].update(bbox=[0, 0, 1, 1]),
                         lambda d: d['scan']['verification'].update(status='fully-reviewed'),
                         lambda d: d['scan']['downloads'][0].update(path='../escape'),
                         lambda d: d['blocks'][0]['paragraphs'][0]['runs'][0].update(text='silently edited')]
            for mutate in mutations:
                doc = json.loads(json.dumps(original))
                mutate(doc)
                write(output, path, doc)
                refresh(output)
                with self.assertRaisesRegex(ValueError, 'projection differs'):
                    check(output)
            write(output, path, original)
            manifest = read(output / 'manifest.json')
            manifest['scanInputs'][0]['manifestSha256'] = '0' * 64
            write(output, 'manifest.json', manifest)
            refresh(output)
            with self.assertRaisesRegex(ValueError, 'scan manifest differs'):
                check(output)

    def test_failed_input_and_unknown_toc_leave_baseline_and_output_untouched(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            base, scan, package = self.fixture(root)
            before = digest(base / 'manifest.json')
            (scan / 'article.txt').write_text('tampered')
            output = root / 'build/output'
            with self.assertRaisesRegex(ValueError, 'hash/size'):
                stage(base, scan, output)
            self.assertFalse(output.exists())
            self.assertEqual(digest(base / 'manifest.json'), before)
            toc = read(base / 'issues/1900-01.json')['toc'][0]
            with self.assertRaisesRegex(ValueError, 'canonical TOC'):
                project(package, {**toc, 'id': 'unknown'})
            package['relationships'] = [{'unreviewed': 'candidate'}]
            with self.assertRaisesRegex(ValueError, 'reviewed comparison'):
                project(package, toc)
            self.assertEqual(list(output.parent.glob('.scan-reader-*')), [])


if __name__ == '__main__':
    unittest.main()
