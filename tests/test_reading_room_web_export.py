"""Checks focused on the new static reader projection and portable demo."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from tools.reading_room.export import demo, safe, text_for
from tools.reading_room.aggregate import add_disc, aggregate, checked_reference, project_blocks
from tools.reading_room.export import digest, read, write


class ReadingRoomWebExportTest(unittest.TestCase):
    def test_demo_covers_missing_and_literal_content(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            demo(root)
            issue = json.loads((root / 'issues/1988-02.json').read_text())
            self.assertEqual(len(issue['toc']), 5)
            self.assertEqual(issue['toc'][-1]['articleIds'], [])
            prepared = json.loads((root / 'articles/demo-prepared.json').read_text())
            text = (root / 'source' / prepared['article']['text']).read_text()
            self.assertEqual(text_for(prepared['blocks']), text)
            self.assertIn('<tag> &', text)
            self.assertIn('\tEND', text)
            self.assertIn('[image:diagram.svg]', text)
            gap = json.loads((root / 'articles/demo-gap.json').read_text())
            self.assertIn('⟦bytes:81⟧', text_for(gap['blocks']))
            self.assertEqual(text_for(gap['blocks']), (root / 'source' / gap['article']['text']).read_text())
            media = json.loads((root / 'media/1988-02.json').read_text())['items']
            self.assertEqual({item['status'] for item in media}, {'available', 'deferred'})
            blocked = json.loads((root / 'articles/demo-blocked.json').read_text())
            self.assertIsNone(blocked['article']['text'])
            self.assertEqual(blocked['blocks'], [])

    def test_source_paths_stay_inside_root(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            for path in ('../outside', '/etc/passwd', 'a/../../outside'):
                with self.assertRaises(ValueError):
                    safe(root, path)

    def test_native_figures_preserve_markers_and_missing_sources(self):
        candidate_media = [
            {'name': 'Click.bmp', 'target_alias': 'figure', 'target_media':
             {'name': 'figure.bmp', 'source_name': 'FIGURE.BMP', 'available': False}},
            {'name': 'Click.bmp', 'target_alias': 'unknown', 'target_media': None},
        ]
        source = {'candidate': {'media': candidate_media}, 'paragraphs': [
            {'id': 'p1', 'terminated': False, 'runs': [
                {'type': 'text', 'text': '\tif (a < b)  ⟦bytes:81⟧', 'bold': True},
                {'type': 'media', 'resource': 'Click.bmp'},
                {'type': 'media', 'resource': 'Click.bmp'}]}]}
        media = {}
        blocks, resources = project_blocks(source, 'cd3', media)
        self.assertEqual(text_for(blocks), '\tif (a < b)  ⟦bytes:81⟧[figure:figure.bmp][figure:unknown · target unresolved]')
        self.assertEqual(resources, ['FIGURE.BMP'])
        self.assertEqual(media['FIGURE.BMP']['status'], 'missing')
        self.assertIsNone(media['FIGURE.BMP']['originalPath'])
        self.assertEqual(blocks[0]['paragraphs'][0]['runs'][0]['marks'], ['bold'])
        source['paragraphs'][0]['runs'][1]['resource'] = 'wrong.bmp'
        with self.assertRaisesRegex(ValueError, 'media order'):
            project_blocks(source, 'cd3', {})

    def test_cd3_blanket_underline_is_only_normalized_for_display(self):
        from tools.build_cd2_pilot import marked_html
        from tools.cd3_display import reading_run
        from tools.cd3_text import parse_cd3
        paragraphs, issues, _ = parse_cd3(b'\\plain\\uldb body \\b bold\\b0 \\i italic\\par ', 0)
        self.assertEqual(issues, [])
        source = {'candidate': {'media': []}, 'paragraphs': paragraphs}
        cd3, _ = project_blocks(source, 'cd3', {})
        cd2, _ = project_blocks(source, 'cd2', {})
        self.assertEqual(text_for(cd3), text_for(cd2))
        self.assertTrue(all(r['underline'] for p in paragraphs for r in p['runs']))
        self.assertFalse(any('underline' in r['marks'] for b in cd3 for p in b['paragraphs'] for r in p['runs']))
        self.assertTrue(all('underline' in r['marks'] for b in cd2 for p in b['paragraphs'] for r in p['runs']))
        self.assertTrue(any('bold' in r['marks'] for b in cd3 for p in b['paragraphs'] for r in p['runs']))
        self.assertTrue(any('italic' in r['marks'] for b in cd3 for p in b['paragraphs'] for r in p['runs']))
        run = {'type': 'text', 'text': '<code>\t  ', 'underline': True, 'bold': True, 'italic': True}
        self.assertEqual(marked_html(reading_run(run)), '<strong><em>&lt;code&gt;\t  </em></strong>')
        self.assertTrue(run['underline'])
        self.assertIn('<u>', marked_html(run))

    def native_fixture(self, root, disc):
        group_dir = 'issues' if disc == 'cd2' else 'groups'
        group = '9401'
        base = f'{group_dir}/{group}'
        article_base = f'{base}/articles/shared-id'
        text = '한글\t<code>  \n'
        path = root / article_base
        path.mkdir(parents=True)
        (path / 'article.txt').write_text(text, encoding='utf-8')
        (path / 'index.html').write_text('<p>synthetic</p>')
        (root / 'index.html').write_text('<p>synthetic shelf</p>')
        write(root, f'{article_base}/blocks.json', {'candidate': {'media': [], 'links': []},
              'paragraphs': [{'id': 'p1', 'terminated': True,
                              'runs': [{'type': 'text', 'text': text[:-1]}]}]})
        (path / 'attachments').mkdir()
        (path / 'attachments/source.bin').write_bytes(b'\x00\xff\r\n')
        row = {'id' if disc == 'cd2' else 'identity': 'shared-id', 'title': 'Synthetic title',
               'group': group, 'status': 'partial', 'paragraphs': 1, 'media_occurrences': 0,
               'text_sha256': digest(path / 'article.txt'), 'reasons': ['Synthetic review note'],
               'attachments': [{'path': 'attachments/source.bin', 'source_path': 'source.bin',
                                'sha256': digest(path / 'attachments/source.bin')}]}
        write(root, f'{base}/articles.json', {'articles': [row]})
        write(root, f'{base}/media.json', {'resources': []})
        write(root, 'coverage.json' if disc == 'cd2' else 'catalog.json',
              {'articles': [row], 'candidate_count' if disc == 'cd2' else 'candidates': 1,
               'outcomes': {'partial': 1}})
        def inventory(directory):
            return [{'path': p.relative_to(directory).as_posix(), 'bytes': p.stat().st_size,
                     'sha256': digest(p)} for p in sorted(directory.rglob('*')) if p.is_file()]
        manifest = {'schema_version': 1, 'disc_id': disc}
        if disc == 'cd2':
            write(root, f'{base}/manifest.json', {'files': inventory(root / base)})
            manifest['issues'] = [{'issue_group': group, 'manifest_sha256': digest(root / base / 'manifest.json')}]
            manifest['files'] = [r for r in inventory(root) if not r['path'].startswith('issues/')]
        else:
            manifest['files'] = inventory(root)
        write(root, 'manifest.json', manifest)

    def test_native_discs_keep_colliding_identities_and_download_bytes(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            output = root / 'output'
            catalog, search = {'articles': [], 'issues': []}, {'items': []}
            for disc in ('cd2', 'cd3'):
                source = root / disc
                self.native_fixture(source, disc)
                result = add_disc(source, disc, output, catalog, search)
                self.assertEqual(result['counts']['articles'], 1)
                doc = read(output / f'articles/{disc}-shared-id.json')
                self.assertEqual(doc['article']['status'], 'partial')
                self.assertEqual(text_for(doc['blocks']), '한글\t<code>  \n')
                self.assertEqual((output / 'source' / doc['attachments'][0]['path']).read_bytes(), b'\x00\xff\r\n')
                self.assertEqual(read(output / f'issues/{disc}-9401.json')['toc'], [])
                (source / 'index.html').write_text('tampered')
                with self.assertRaisesRegex(ValueError, 'Changed'):
                    checked_reference(source, disc)
            self.assertEqual({a['article_id'] for a in catalog['articles']},
                             {'cd2:article:shared-id', 'cd3:article:shared-id'})
            self.assertEqual(len(search['items']), 2)

    def test_failed_aggregate_preserves_previous_reader(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            output = root / 'reader/data'
            output.mkdir(parents=True)
            (output / 'catalog.json').write_bytes(b'previous reader')
            def fake_cd1(reference, toc, stage):
                demo(stage)
                return {'sourceManifestSha256': 'synthetic', 'counts': {}}
            with patch('tools.reading_room.aggregate.export', side_effect=fake_cd1):
                with self.assertRaises(FileNotFoundError):
                    aggregate(root / 'cd1', root / 'toc', root / 'absent-cd2', root / 'cd3', output)
            self.assertEqual((output / 'catalog.json').read_bytes(), b'previous reader')
            self.assertEqual(list(output.parent.glob('.reading-room-*')), [])


if __name__ == '__main__':
    unittest.main()
