"""TOC sources, catalog preservation, and public derivative guarantees."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from PIL import Image

from tools.reading_room.export import digest, read, write
from tools.reading_room.tocs import attach_tocs, check_tocs, prepare, validate_prepared
from tools.toc_restore.inventory import inventory, normalize, save
from tools.toc_restore.compare import compare


def donations(root):
    source = root / 'donations'
    for name, color in [('8802/Page003.jpg', 'red'), ('8802/Page002.jpg', 'blue'), ('9401/Page001.jpg', 'green')]:
        path = source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new('RGB', (900, 1300), color).save(path, exif=Image.Exif(), comment=b'private metadata')
    manifest = inventory(source)
    path = root / 'inventory.json'
    save(path, manifest)
    reviews = root / 'reviews.json'
    save(reviews, dict(pages=[dict(sha256=r['sha256'], date=r['date'], sequence=r['sequence'],
                                identityEvidence='Synthetic issue label', orderEvidence='Synthetic ordered pages')
                             for r in manifest['records']]))
    return source, path, reviews


def catalog_fixture(root):
    issues = [dict(id='maso-1988-02', year=1988, month=2),
              dict(id='maso-1991-06', year=1991, month=6),
              dict(id='cd2-9401', year=1994, month=1, nativeGroup=True)]
    catalog = dict(issues=issues, articles=[])
    for issue in issues:
        write(root, f'issues/{issue["id"].removeprefix("maso-")}.json', dict(issue=issue, toc=['authoritative text'], articles=[]))
    return catalog


class TocImagesTests(unittest.TestCase):
    def test_tesseract_quotes_are_literal_and_do_not_swallow_later_lines(self):
        from tools.toc_restore.ocr import lines_from_tsv
        with TemporaryDirectory() as temp:
            path = Path(temp) / 'text.tsv'
            path.write_text('level\tblock_num\tpar_num\tline_num\tleft\ttop\twidth\theight\tconf\ttext\n'
                            '5\t1\t1\t1\t0\t0\t5\t5\t90\t"\n'
                            '5\t1\t1\t2\t0\t10\t5\t5\t90\tTitle\n')
            self.assertEqual([r['text'] for r in lines_from_tsv(path, [0, 0])], ['"', 'Title'])

    def test_inventory_normalization_rerun_and_rollback_preserve_bytes(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source, manifest_path, reviews = donations(root)
            original = read(manifest_path)
            self.assertEqual([r['old'] for r in original['records'][:2]], ['8802/Page002.jpg', '8802/Page003.jpg'])
            journal = root / 'journal.json'
            normalize(manifest_path, reviews, journal)
            self.assertEqual(normalize(manifest_path, reviews, journal)['state'], 'complete')
            current = inventory(source)
            self.assertEqual([r['old'] for r in current['records']], ['8802-01.jpg', '8802-02.jpg', '9401-01.jpg'])
            self.assertEqual([r['sha256'] for r in current['records']], [r['sha256'] for r in original['records']])
            normalize(manifest_path, reviews, journal, rollback=True)
            self.assertEqual(inventory(source), original)

    def test_collision_stale_review_and_corruption_leave_sources_intact(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source, manifest, reviews = donations(root)
            (source / '8802-01.jpg').write_bytes(b'occupied')
            with self.assertRaisesRegex(ValueError, 'Collision'):
                normalize(manifest, reviews, root / 'journal')
            self.assertTrue((source / '8802/Page002.jpg').exists())
            (source / '8802-01.jpg').unlink()
            save(reviews, dict(pages=[]))
            with self.assertRaisesRegex(ValueError, 'review'):
                normalize(manifest, reviews, root / 'journal')
            (source / '9401/Page001.jpg').write_bytes(b'corrupt')
            self.assertTrue(inventory(source)['errors'])

    def test_interrupted_link_move_recovers_without_overwrite(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source, manifest, reviews = donations(root)
            original_unlink = Path.unlink
            def fail_once(path, *args, **kwargs):
                if path.name == 'Page002.jpg':
                    raise OSError('interrupted after link')
                return original_unlink(path, *args, **kwargs)
            with patch.object(Path, 'unlink', fail_once), self.assertRaises(OSError):
                normalize(manifest, reviews, root / 'journal')
            normalize(manifest, reviews, root / 'journal')
            self.assertEqual(len(inventory(source)['records']), 3)
            self.assertFalse(inventory(source)['errors'])

    def test_unreviewed_sources_cannot_be_served_and_overlap_is_rejected(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source, _, reviews = donations(root)
            with self.assertRaisesRegex(ValueError, 'overlap'):
                prepare(source, source / 'images', reviews)
            save(reviews, dict(pages=[]))
            with self.assertRaisesRegex(ValueError, 'review'):
                prepare(source, root / 'images', reviews)

    def test_attachment_keeps_catalog_and_native_groups_separate(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source, _, reviews = donations(root)
            output = root / 'reader'
            catalog = catalog_fixture(output)
            original = deepcopy(catalog)
            manifest = attach_tocs(output, catalog, source, root / 'images', reviews)
            self.assertEqual({k:v for k,v in catalog.items() if k != 'tocGallery'}, original)
            issue = read(output / 'issues/1988-02.json')
            self.assertEqual(issue['toc'], ['authoritative text'])
            self.assertEqual([r['sequence'] for r in issue['tocImages']], [1, 2])
            self.assertEqual(read(output / 'issues/1991-06.json')['tocImages'], [])
            self.assertNotIn('tocImages', read(output / 'issues/cd2-9401.json'))
            self.assertEqual(read(output / 'toc-gallery.json')['sets'][0]['date'], '1994-01')
            check_tocs(output, catalog, manifest)
            prepared = validate_prepared(root / 'images', sources=True)
            self.assertEqual(len(prepared['records']), 3)
            # No private source path or OCR text is exposed through reader documents.
            self.assertNotIn(str(source), (output / 'toc-gallery.json').read_text())
            first_path = issue['tocImages'][0]['preview']['path']
            (source / '8802/Page002.jpg').unlink()
            # Removal changes numbering of unnormalized sources and must require review.
            with self.assertRaisesRegex(ValueError, 'review'):
                attach_tocs(output, catalog, source, root / 'images', reviews)
            self.assertTrue((output / first_path).exists())

    def test_removal_drops_stale_assets_and_checker_rejects_metadata(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source, mapping, reviews = donations(root)
            normalize(mapping, reviews, root / 'journal')
            output = root / 'reader'
            catalog = catalog_fixture(output)
            manifest = attach_tocs(output, catalog, source, root / 'images', reviews)
            record = read(output / 'issues/1988-02.json')['tocImages'][0]['preview']
            path = output / record['path']
            Image.new('RGB', (record['width'], record['height'])).save(path, comment=b'private')
            issue = read(output / 'issues/1988-02.json')
            issue['tocImages'][0]['preview'].update(sha256=digest(path), bytes=path.stat().st_size)
            write(output, 'issues/1988-02.json', issue)
            with self.assertRaisesRegex(ValueError, 'metadata'):
                check_tocs(output, catalog, manifest)
            (source / '8802-01.jpg').unlink()
            manifest = attach_tocs(output, catalog, source, root / 'images', reviews)
            self.assertFalse(path.exists())
            self.assertEqual(read(output / 'issues/1988-02.json')['tocImages'][0]['sequence'], 2)
            check_tocs(output, catalog, manifest)

    def test_ocr_cache_pins_runtime_configuration_and_output(self):
        from tools.toc_restore.ocr import ocr_page
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source, mapping, _ = donations(root)
            row = read(mapping)['records'][0]
            runtime = root / 'runtime'
            save(runtime / 'runtime.json', dict(synthetic=True))
            def recognize(image, destination, config, runtime):
                destination.with_suffix('.txt').write_text('Synthetic OCR\n')
                destination.with_suffix('.tsv').write_text('level\tblock_num\tpar_num\tline_num\tleft\ttop\twidth\theight\tconf\ttext\n5\t1\t1\t1\t1\t2\t3\t4\t90\tSynthetic\n')
            with patch('tools.toc_restore.ocr.verify_runtime'), patch('tools.toc_restore.ocr.run_region', side_effect=recognize) as run:
                first, directory = ocr_page(row, source, root / 'ocr', runtime=runtime)
                self.assertEqual(ocr_page(row, source, root / 'ocr', runtime=runtime), (first, directory))
                self.assertEqual(run.call_count, 1)
                _, changed = ocr_page(row, source, root / 'ocr', dict(psm=6), runtime)
                self.assertNotEqual(directory, changed)
                (directory / 'region-00.txt').write_text('corrupt')
                with self.assertRaisesRegex(ValueError, 'cache bytes'):
                    ocr_page(row, source, root / 'ocr', runtime=runtime)

    def test_prepared_failure_preserves_previous_derivatives(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source, _, reviews = donations(root)
            prepare(source, root / 'images', reviews)
            before = digest(root / 'images/manifest.json')
            (source / '8802/Page002.jpg').write_bytes(b'invalid')
            with self.assertRaises(ValueError):
                prepare(source, root / 'images', reviews)
            self.assertEqual(digest(root / 'images/manifest.json'), before)

    def test_replacement_applies_orientation_bounds_and_removes_old_derivatives(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source, mapping, reviews = donations(root)
            normalize(mapping, reviews, root / 'journal')
            first = prepare(source, root / 'images', reviews)
            old = next(r for r in first['records'] if r['name'] == '8802-01.jpg')
            replacement = source / old['name']
            exif = Image.Exif()
            exif[274] = 6  # Upright dimensions are 300 x 600, not 600 x 300.
            Image.new('L', (600, 300), 90).save(replacement, exif=exif, comment=b'private')
            replacement_hash = digest(replacement)
            data = read(reviews)
            next(r for r in data['pages'] if r['sha256'] == old['source']['sha256'])['sha256'] = replacement_hash
            save(reviews, data)
            second = prepare(source, root / 'images', reviews)
            new = next(r for r in second['records'] if r['name'] == old['name'])
            for variant in ('preview', 'readable'):
                self.assertEqual((new[variant]['width'], new[variant]['height']), (300, 600))
                self.assertNotEqual(new[variant]['path'], old[variant]['path'])
                self.assertFalse((root / 'images' / old[variant]['path']).exists())
                with Image.open(root / 'images' / new[variant]['path']) as image:
                    self.assertEqual(image.mode, 'RGB')
                    self.assertFalse(image.getexif())
                    self.assertNotIn('comment', image.info)
            self.assertEqual(digest(replacement), replacement_hash)
            validate_prepared(root / 'images', sources=True)

    def test_non_toc_donation_is_accounted_for_but_never_served(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source, mapping, reviews = donations(root)
            data = read(reviews)
            data['pages'][0].update(kind='advertisement', note='Synthetic advertisement, no TOC')
            data['pages'][2]['publicNote'] = 'Only one donated page; remaining contents unavailable.'
            save(reviews, data)
            prepared = prepare(source, root / 'images', reviews)
            self.assertEqual(len(prepared['records']), 2)
            self.assertEqual(prepared['excluded'][0]['name'], '8802-01.jpg')
            output = root / 'reader'
            catalog = catalog_fixture(output)
            manifest = attach_tocs(output, catalog, source, root / 'images', reviews)
            check_tocs(output, catalog, manifest)
            self.assertEqual(len(read(output / 'issues/1988-02.json')['tocImages']), 1)
            self.assertFalse(list((output / 'tocs').glob('8802-01*')))
            self.assertIn('Only one donated page', read(output / 'toc-gallery.json')['sets'][0]['note'])

    def test_missing_directory_and_legacy_catalog(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            output = root / 'reader'
            catalog = catalog_fixture(output)
            check_tocs(output, catalog, {})
            manifest = attach_tocs(output, catalog, root / 'missing', root / 'images')
            check_tocs(output, catalog, manifest)
            self.assertEqual(manifest['tocImageCounts']['pages'], 0)

    def test_comparison_is_versioned_and_never_writes_catalog(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'TOC.md'
            source.write_text('## 88.02\n- Original title / Author = 7\n')
            before = source.read_bytes()
            evidence = root / 'ocr.json'
            save(evidence, dict(settings=dict(sourceSha256='a'*64), dimensions=[100, 100],
                                lines=[dict(text='Different title Author 8', region=0, confidence=90, bbox=[0, 0, 99, 20])]))
            index = root / 'index.json'
            save(index, dict(pages=[dict(name='8802-01.jpg', date='8802', sequence=1,
                                       sha256='a'*64, evidence=str(evidence))]))
            report = compare(index, source, root / 'reports', root / 'reviews', root / 'no-catalog')
            self.assertEqual(source.read_bytes(), before)
            item = read(report / 'report.json')['issues'][0]['entries'][0]
            self.assertEqual(item['line'], 2)
            self.assertEqual(item['page'], 7)
            self.assertEqual(item['contributor'], 'Author')
            self.assertEqual(item['status'], 'possible-difference')
            reviews = root / 'reviews'
            review = dict(status='reviewed-differences', note='Visible page is 8',
                          sourceSha256=digest(source), evidenceSha256=digest(evidence),
                          findings=[dict(sourceLine=2, printedText='Different title Author 8')])
            save(reviews, dict(pages=[dict(sha256='a'*64, comparison=review)]))
            reviewed_report = compare(index, source, root / 'reports', reviews, root / 'no-catalog')
            self.assertEqual(read(reviewed_report / 'report.json')['summary']['reviews'],
                             {'reviewed-differences': 1})
            self.assertIn('Visible page is 8', (reviewed_report / 'report.md').read_text())
            self.assertIn('Different title Author 8', (reviewed_report / 'report.md').read_text())
            source.write_text('## 88.02\n- User correction = 9\n')
            new_report = compare(index, source, root / 'reports', root / 'reviews', root / 'no-catalog')
            self.assertNotEqual(report, new_report)
            self.assertTrue((report / 'report.json').exists())
            stale = read(new_report / 'report.json')['issues'][0]['pages'][0]['review']
            self.assertEqual(stale['status'], 'stale')
            self.assertEqual(stale['previous'], review)
            self.assertEqual(source.read_text(), '## 88.02\n- User correction = 9\n')
            # A new OCR result also invalidates a review even with unchanged catalog text.
            review['sourceSha256'] = digest(source)
            save(reviews, dict(pages=[dict(sha256='a'*64, comparison=review)]))
            changed_evidence = read(evidence)
            changed_evidence['lines'][0]['text'] = 'New recognition'
            save(evidence, changed_evidence)
            ocr_report = compare(index, source, root / 'reports', reviews, root / 'no-catalog')
            self.assertEqual(read(ocr_report / 'report.json')['summary']['reviews'], {'stale': 1})
            self.assertEqual(read(reviewed_report / 'report.json')['summary']['reviews'],
                             {'reviewed-differences': 1})

    def test_pdf_scan_refresh_preserves_existing_article_bytes_and_toc_text(self):
        import test_pdf_reader
        from tools.reading_room.scan import stage
        from tools.reading_room.check import check
        with TemporaryDirectory() as temp:
            root = Path(temp)
            base, scan, _ = test_pdf_reader.PDFReaderTests().fixture(root)
            source, _, reviews = donations(root)
            before = read(base / 'issues/1988-02.json')
            output = root / 'with-tocs'
            stage(base, scan, output, tocs=source, toc_images=root / 'images', toc_reviews=reviews)
            check(output)
            after = read(output / 'issues/1988-02.json')
            self.assertEqual({k:v for k,v in after.items() if k != 'tocImages'}, before)
            for p in (base / 'source').rglob('*'):
                if p.is_file():
                    self.assertEqual(digest(p), digest(output / p.relative_to(base)))
            self.assertEqual(len(after['tocImages']), 2)

    def test_staged_cd1_refresh_failure_preserves_previous_output(self):
        from tools.reading_room.export import export
        from test_reading_room_covers import demo_reader, reader_refresh
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source, _, reviews = donations(root)
            output = root / 'reader'
            output.mkdir()
            (output / 'sentinel').write_text('previous reader')
            def fixture(reference, toc, staged, *args):
                demo_reader(staged)
                reader_refresh(staged, root / 'no-covers', root / 'thumbs')
                return read(staged / 'manifest.json')
            with patch('tools.reading_room.export._export', side_effect=fixture):
                save(reviews, dict(pages=[]))
                with self.assertRaisesRegex(ValueError, 'review'):
                    export(root / 'reference', root / 'toc', output, tocs=source,
                           toc_images=root / 'images', toc_reviews=reviews)
            self.assertEqual((output / 'sentinel').read_text(), 'previous reader')

    def test_full_pdf_issue_export_preserves_inherited_toc_collection(self):
        from test_pdf_issue import PDFIssueTests
        from tools.reading_room.scan_issue import stage_issue
        from tools.reading_room.tocs import refresh
        from tools.reading_room.check import check
        with TemporaryDirectory() as temp:
            root = Path(temp)
            base, ledger, _, _ = PDFIssueTests().fixture(root)
            source, _, reviews = donations(root)
            # Include the actual issue being staged, another canonical issue,
            # and a gallery-only date so all inherited locations are exercised.
            Image.new('RGB', (900, 1300), 'yellow').save(source / '0001-01.jpg')
            rows = inventory(source)['records']
            save(reviews, dict(pages=[dict(sha256=r['sha256'], date=r['date'], sequence=r['sequence'],
                identityEvidence='Synthetic issue label', orderEvidence='Synthetic order') for r in rows]))
            refresh(base, read(base / 'manifest.json'), source, root / 'images', reviews)
            before = {p.relative_to(base): p.read_bytes() for p in (base / 'tocs').iterdir()}
            images = read(base / 'issues/1900-01.json')['tocImages']
            gallery = (base / 'toc-gallery.json').read_bytes()
            output = root / 'full-issue-reader'
            stage_issue(base, ledger, output, root)
            check(output)
            self.assertEqual(read(output / 'issues/1900-01.json')['tocImages'], images)
            self.assertEqual((output / 'toc-gallery.json').read_bytes(), gallery)
            self.assertEqual(read(output / 'manifest.json')['tocImageCounts'],
                             read(base / 'manifest.json')['tocImageCounts'])
            for path, data in before.items():
                self.assertEqual((output / path).read_bytes(), data)


if __name__ == '__main__':
    unittest.main()
