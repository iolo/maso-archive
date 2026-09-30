"""Derivative privacy, source priority, migration and destructive cleanup gates."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from PIL import Image, ImageCms

from tools.reading_room.covers import (POLICY, SETTINGS, apply_cleanup, attach_covers, cleanup_report,
                                      discover, pin, prepare, validate_prepared)
from tools.reading_room.export import demo, digest, read, write
from tools.reading_room.check import check
from tools.reading_room.aggregate import aggregate
import test_pdf_reader
from test_pdf_reader import refresh, inventory


def demo_reader(root):
    demo(root)
    write(root, 'manifest.json', dict(kind='reading-room-static', schemaVersion=1,
          counts=dict(issues=1, articles=4, texts=3, listings=3, mediaRecords=2, tocEntries=5),
          files=inventory(root)))


def pdf_checkpoint(root, labels=('8802',), status='verified-front-cover'):
    reviews, records = [], []
    for label in labels:
        path = root / 'candidates' / f'{label}.jpg'
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new('RGB', (800, 1200), 'blue').save(path)
        artifact = dict(path=f'candidates/{label}.jpg', **pin(path))
        review = dict(source_id=f'pdf-{label}', status=status, visible_issue_label=label,
                      date_evidence='Synthetic visible date', upright=True, proportions_checked=True,
                      reviewed_artifact=artifact)
        reviews.append(review)
        records.append(dict(source_id=review['source_id'], filename_issue_label=label,
                            review=review, candidate=dict(artifact=artifact)))
    write(root, 'review.json', reviews)
    write(root, 'ledger.json', dict(review=dict(path='review.json', **pin(root / 'review.json')), records=records))
    return root


def reader_refresh(reader, covers, thumbnails, checkpoint=None):
    catalog = read(reader / 'catalog.json')
    manifest = read(reader / 'manifest.json')
    manifest['coverInputs'] = attach_covers(reader, catalog, covers, checkpoint, thumbnails)
    manifest['coverPolicy'] = POLICY
    manifest['counts']['covers'] = sum(i['cover'] is not None for i in catalog['issues'])
    manifest['counts']['coverAssets'] = len(manifest['coverInputs'])
    write(reader, 'catalog.json', catalog)
    write(reader, 'manifest.json', manifest)
    refresh(reader)
    check(reader, require_thumbnails=True)


class CoverTests(unittest.TestCase):
    def test_downsampling_orientation_profiles_metadata_and_no_source_copy(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            covers = root / 'covers'
            covers.mkdir()
            exif = Image.Exif()
            exif[274] = 6
            exif[270] = 'Private donor metadata'
            profile = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
            Image.new('RGB', (1200, 800), 'green').save(covers / '8802.jpg', exif=exif, icc_profile=profile)
            Image.new('RGB', (12, 16), 'red').save(covers / '8803.jpg')
            before = {p.name: digest(p) for p in covers.iterdir()}
            result = prepare(covers, root / 'thumbs')
            first, second = result['records']
            self.assertEqual((first['width'], first['height']), (427, 640))
            self.assertEqual((second['width'], second['height']), (12, 16))
            self.assertNotEqual(second['sha256'], second['source']['sha256'])
            self.assertEqual(before, {p.name: digest(p) for p in covers.iterdir()})
            validate_prepared(root / 'thumbs', sources=True)
            self.assertEqual(prepare(covers, root / 'thumbs'), result)
            with patch.dict(SETTINGS, quality=79):
                regenerated = prepare(covers, root / 'thumbs')
                self.assertNotEqual(regenerated['records'][0]['path'], first['path'])

    def test_priority_fallback_review_pins_and_corrupt_donation(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            covers = root / 'covers'
            covers.mkdir()
            checkpoint = pdf_checkpoint(root / 'checkpoint')
            output = root / 'thumbs'
            fallback = prepare(covers, output, checkpoint)['records'][0]
            self.assertEqual(fallback['source']['kind'], 'pdf')
            self.assertLessEqual(fallback['height'], 640)
            Image.new('RGB', (10, 20), 'red').save(covers / '8802.jpg')
            donated = prepare(covers, output, checkpoint)['records'][0]
            self.assertEqual(donated['source']['kind'], 'donated')
            self.assertNotEqual(fallback['path'], donated['path'])
            (covers / '8802.jpg').write_bytes(b'corrupt donation')
            before = digest(output / 'manifest.json')
            with self.assertRaises(OSError):
                prepare(covers, output, checkpoint)
            self.assertEqual(digest(output / 'manifest.json'), before)
            (covers / '8802.jpg').unlink()
            self.assertEqual(prepare(covers, output, checkpoint)['records'][0], fallback)
            (checkpoint / 'candidates/8802.jpg').write_bytes(b'changed candidate')
            with self.assertRaisesRegex(ValueError, 'bytes changed'):
                prepare(covers, output, checkpoint)
            checkpoint = pdf_checkpoint(checkpoint, status='uncertain')
            self.assertEqual(prepare(covers, output, checkpoint)['records'], [])
            (checkpoint / 'review.json').write_text('[]')
            with self.assertRaisesRegex(ValueError, 'review changed'):
                prepare(covers, output, checkpoint)

    def test_discovery_ignores_legacy_rejects_bad_dates_formats_duplicates_and_paths(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            covers = root / 'covers'
            covers.mkdir()
            (covers / 'maso9513.jpg').write_bytes(b'ignored legacy, even corrupt')
            self.assertEqual(discover(covers), {})
            self.assertEqual(prepare(root / 'absent', root / 'thumbs', root / 'absent-pdf')['records'], [])
            bad = covers / '9513.jpg'
            bad.write_bytes(b'bad')
            with self.assertRaisesRegex(ValueError, 'date/filename'):
                prepare(covers, root / 'thumbs')
            bad.unlink()
            Image.new('RGB', (10, 20)).save(covers / '9512.jpg', format='PNG')
            with self.assertRaisesRegex(ValueError, 'format'):
                prepare(covers, root / 'thumbs')
            Image.new('RGB', (10, 20)).save(covers / '9512.jpg')
            (covers / '9512.JPG').write_bytes((covers / '9512.jpg').read_bytes())
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                prepare(covers, root / 'thumbs')
            (covers / '9512.JPG').unlink()
            for output in (covers, covers / 'nested', root):
                with self.assertRaisesRegex(ValueError, 'overlap'):
                    prepare(covers, output)
            (covers / '9512.jpg').unlink()
            (covers / '9512.jpg').symlink_to('/etc/passwd')
            with self.assertRaisesRegex(ValueError, 'Unsafe'):
                prepare(covers, root / 'thumbs')
            (covers / '9512.jpg').unlink()
            checkpoint = pdf_checkpoint(root / 'checkpoint')
            (checkpoint / 'candidates/8802.jpg').unlink()
            (checkpoint / 'candidates/8802.jpg').symlink_to('/etc/passwd')
            with self.assertRaisesRegex(ValueError, 'Unsafe'):
                prepare(covers, root / 'thumbs', checkpoint)

    def test_shared_dates_refresh_and_clear_assignments_and_stale_assets(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            covers, output, thumbnails = root / 'covers', root / 'reader', root / 'thumbs'
            covers.mkdir()
            Image.new('RGB', (800, 1000), 'green').save(covers / '9409.jpg')
            issues = [dict(id=id, year=year, month=month, cover=None) for id, year, month in
                      [('cd2-9409', 1994, 9), ('cd3-9409', 1994, 9), ('cd3-others', 0, 0)]]
            catalog = dict(issues=issues)
            for issue in issues:
                write(output, f'issues/{issue["id"]}.json', dict(issue=issue))
            records = attach_covers(output, catalog, covers, thumbnails=thumbnails)
            self.assertEqual(len(records), 1)
            self.assertEqual(issues[0]['cover'], issues[1]['cover'])
            self.assertIsNone(issues[2]['cover'])
            old_path = issues[0]['cover']['path']
            Image.new('RGB', (700, 900), 'red').save(covers / '9409.jpg')
            attach_covers(output, catalog, covers, thumbnails=thumbnails)
            self.assertFalse((output / old_path).exists())
            self.assertNotEqual(issues[0]['cover']['path'], old_path)
            (covers / '9409.jpg').unlink()
            self.assertEqual(attach_covers(output, catalog, covers, thumbnails=thumbnails), [])
            self.assertTrue(all(i['cover'] is None for i in issues))
            self.assertFalse((output / 'covers').exists())
            self.assertIsNone(read(output / 'issues/cd2-9409.json')['issue']['cover'])

    def test_checker_rejects_rehashed_dimensions_metadata_and_stale_covers(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            reader, covers, thumbnails = root / 'reader', root / 'covers', root / 'thumbs'
            demo_reader(reader)
            covers.mkdir()
            Image.new('RGB', (100, 200)).save(covers / '8802.jpg')
            reader_refresh(reader, covers, thumbnails)
            cover = read(reader / 'catalog.json')['issues'][0]['cover']
            path = reader / cover['path']
            original = path.read_bytes()
            for size, metadata in [((481, 640), {}), ((100, 200), {'comment': b'private'})]:
                Image.new('RGB', size).save(path, **metadata)
                # Update every public pin: semantic validation must still reject it.
                catalog = read(reader / 'catalog.json')
                catalog['issues'][0]['cover'].update(sha256=digest(path), width=size[0], height=size[1])
                write(reader, 'catalog.json', catalog)
                issue = read(reader / 'issues/1988-02.json')
                issue['issue'] = catalog['issues'][0]
                write(reader, 'issues/1988-02.json', issue)
                manifest = read(reader / 'manifest.json')
                manifest['coverInputs'][0].update(catalog['issues'][0]['cover'])
                write(reader, 'manifest.json', manifest)
                refresh(reader)
                with self.assertRaisesRegex(ValueError, 'Thumbnail'):
                    check(reader)
            path.write_bytes(original)
            reader_refresh(reader, covers, thumbnails)
            (reader / 'covers/maso8802.jpg').write_bytes(original)
            refresh(reader)
            with self.assertRaisesRegex(ValueError, 'Unreferenced'):
                check(reader)

    def test_cleanup_requires_current_reader_and_evidence_preserves_unpaired_files(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            reader, covers, thumbnails = root / 'reader', root / 'covers', root / 'thumbs'
            demo_reader(reader)
            covers.mkdir()
            for label in ('8802', '8803'):
                Image.new('RGB', (100, 200)).save(covers / f'{label}.jpg')
                (covers / f'maso{label}.jpg').write_bytes(b'old')
            for name in ('maso8802.png', 'maso8802.jpeg', 'maso8802.webp', 'maso8804.jpg'):
                (covers / name).write_bytes(b'preserve')
            checkpoint = pdf_checkpoint(root / 'checkpoint')
            reader_refresh(reader, covers, thumbnails, checkpoint)
            report = cleanup_report(covers, thumbnails, reader)
            self.assertEqual(len(report['candidates']), 2)  # Includes prepared date outside catalog.
            report_path = write(root, 'cleanup.json', report)
            (covers / 'maso8802.jpg').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'Stale'):
                apply_cleanup(report_path)
            self.assertTrue((covers / 'maso8803.jpg').exists())
            report_path = write(root, 'cleanup.json', cleanup_report(covers, thumbnails, reader))
            donation = covers / '8802.jpg'
            old = donation.read_bytes()
            donation.write_bytes(b'changed donation')
            with self.assertRaisesRegex(ValueError, 'source changed'):
                apply_cleanup(report_path)
            donation.write_bytes(old)
            result = apply_cleanup(report_path)
            self.assertEqual(len(result['deleted']), 2)
            self.assertEqual(apply_cleanup(report_path), result)
            for name in ('8802.jpg', '8803.jpg', 'maso8802.png', 'maso8802.jpeg', 'maso8802.webp', 'maso8804.jpg'):
                self.assertTrue((covers / name).exists())
            self.assertTrue((checkpoint / 'candidates/8802.jpg').exists())

    def test_scan_migrates_legacy_baseline_and_clears_uncovered_issues(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            base, scan, _ = test_pdf_reader.PDFReaderTests().fixture(root)
            catalog = read(base / 'catalog.json')
            for issue in catalog['issues']:
                name = f'covers/maso{str(issue["year"])[2:]}{issue["month"]:02}.jpg'
                (base / 'covers').mkdir(exist_ok=True)
                Image.new('RGB', (900, 1200)).save(base / name)
                issue['cover'] = dict(path=name, width=900, height=1200, sha256=digest(base / name))
                docpath = f'issues/{issue["id"].removeprefix("maso-")}.json'
                doc = read(base / docpath)
                doc['issue'] = issue
                write(base, docpath, doc)
            write(base, 'catalog.json', catalog)
            manifest = read(base / 'manifest.json')
            manifest['counts']['covers'] = 2
            write(base, 'manifest.json', manifest)
            refresh(base)
            check(base)
            with self.assertRaisesRegex(ValueError, 'migration'):
                check(base, require_thumbnails=True)
            from tools.reading_room.scan import stage
            stage(base, scan, root / 'unchanged')
            self.assertNotIn('coverPolicy', read(root / 'unchanged/manifest.json'))
            self.assertEqual((base / catalog['issues'][0]['cover']['path']).read_bytes(),
                             (root / 'unchanged' / catalog['issues'][0]['cover']['path']).read_bytes())
            covers = root / 'covers'
            covers.mkdir()
            Image.new('RGB', (700, 1100), 'green').save(covers / '0001.jpg')
            stage(base, scan, root / 'migrated', covers, thumbnails=root / 'thumbs')
            self.assertEqual(check(root / 'migrated', require_thumbnails=True)['covers'], 1)
            migrated = read(root / 'migrated/catalog.json')
            self.assertIsNone(migrated['issues'][0]['cover'])
            self.assertEqual(len(list((root / 'migrated/covers').iterdir())), 1)
            for p in (base / 'source').rglob('*'):
                if p.is_file():
                    self.assertEqual(digest(p), digest(root / 'migrated' / p.relative_to(base)))

    def test_cd1_failed_validation_preserves_previous_reader_and_protects_inputs(self):
        from tools.reading_room.export import export
        with TemporaryDirectory() as temp:
            root = Path(temp)
            output = root / 'reader'
            output.mkdir()
            (output / 'sentinel').write_text('previous reader')
            with patch('tools.reading_room.export._export', side_effect=lambda *args: demo_reader(args[2])):
                with self.assertRaisesRegex(ValueError, 'migration'):
                    export(root / 'reference', root / 'toc', output)
            self.assertEqual((output / 'sentinel').read_text(), 'previous reader')
            with self.assertRaisesRegex(ValueError, 'overlap'):
                export(root / 'reference', root / 'toc', output, thumbnails=root / 'reference')

    def test_aggregate_uses_derivatives_and_failed_refresh_preserves_reader(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            covers = root / 'covers'
            covers.mkdir()
            Image.new('RGB', (900, 1200)).save(covers / '8802.jpg')
            def cd1(reference, toc, output):
                demo_reader(output)
                return dict(read(output / 'manifest.json'), sourceManifestSha256='synthetic')
            def disc(source, name, output, catalog, search):
                return dict(disc=name, counts={})
            # Exercise aggregate staging/cover logic, isolating unrelated private disc readers.
            with patch('tools.reading_room.aggregate.export', side_effect=cd1), \
                 patch('tools.reading_room.aggregate.add_disc', side_effect=disc), \
                 patch('tools.reading_room.check.check'):
                output = root / 'reader'
                aggregate(root / 'cd1', root / 'toc', root / 'cd2', root / 'cd3', output,
                          covers, thumbnails=root / 'thumbs')
                before = digest(output / 'manifest.json')
                cover = read(output / 'catalog.json')['issues'][0]['cover']
                self.assertLessEqual(cover['height'], 640)
                (covers / '8802.jpg').write_bytes(b'corrupt')
                with self.assertRaises(OSError):
                    aggregate(root / 'cd1', root / 'toc', root / 'cd2', root / 'cd3', output,
                              covers, thumbnails=root / 'thumbs')
                self.assertEqual(digest(output / 'manifest.json'), before)


if __name__ == '__main__':
    unittest.main()
