"""Unindexed native identity, code fidelity, image tables, and package composition."""

from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from maso_archive.reading_room import SCHEMA_PATH, project_section
from maso_archive.reading_room_package import load_package
from tools import prepare_cd1_keyboard as keyboard
from tools import recover_cd1_text as recovery
from tools.build_reading_room_package import write_package
from tools.decode_cd1_paragraph import digest


@unittest.skipUnless((keyboard.ROOT / 'private/cd1-probe/raw/MASOCD.rtf').exists() and
                     (keyboard.PREVIOUS / 'manifest.json').exists(), 'Private keyboard sources unavailable')
class KeyboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record, cls.files = keyboard.build_article()
        cls.article = json.loads(cls.files['recovery.json'])
        cls.mapping = json.loads(cls.files['blocks.json'])
        cls.runtime = json.loads(cls.files['single/content/articles/cd1/8802162.json'])
        cls.evidence = json.loads(cls.files['provenance.json'])

    def test_rebuild_and_native_identity_without_index_evidence(self):
        self.assertEqual(self.record, json.loads(keyboard.RECORD.read_bytes()))
        self.assertEqual(self.evidence['index_occurrences'], [])
        self.assertEqual([r['native']['ordinal'] for r in self.evidence['topic_map']], [154, 155])
        self.assertEqual(self.evidence['topic_map'][1]['context']['hash_hex'], '0x0e68416d')
        self.assertEqual(sum(r['rtf']['byte_length'] for r in self.evidence['topic_map']), 53683)
        self.assertEqual(self.runtime['pages'], {'start': 162, 'end': None})
        self.assertEqual(self.runtime['toc_entry_ids'], ['maso-1988-02-toc-0023'])
        self.assertEqual(self.runtime['byline'], '글/ 편집부')
        self.assertEqual(self.runtime['print_verification']['status'], 'pending')
        self.assertEqual(digest(SCHEMA_PATH.read_bytes()), '2a160d646c4a92552fcc4647216348c14ee74c357a375412f23fed54bffc6f68')

    def test_all_bytes_runs_marks_and_text_survive(self):
        media = {m['id']: m for m in json.loads(self.files['single/content/media.json'])['items']}
        for topic, section in zip(self.article['topics'], self.runtime['sections']):
            cursor = topic['source_span']['byte_offset']
            for token in topic['accounting']:
                self.assertEqual(token['byte_offset'], cursor)
                cursor += token['byte_length']
            self.assertEqual(cursor, topic['source_span']['end_exclusive'])
            self.assertFalse(topic['issues'])
            self.assertEqual(project_section(section, media), recovery.topic_text(topic))
            exported = [p for b in section['blocks'] for p in b['paragraphs']]
            self.assertEqual(len(exported), len(topic['paragraphs']))
            for old, new in zip(topic['paragraphs'], exported):
                self.assertEqual(len(old['runs']), len(new['runs']))
                for source, target in zip(old['runs'], new['runs']):
                    self.assertEqual(target['marks'], [name for key, name in (('b', 'bold'), ('ul', 'underline')) if source['format'][key]])
                    if source['kind'] == 'text':
                        self.assertEqual(target['text'], source['text'])
                        self.assertEqual(digest(target['text'].encode(source['encoding'])), source['encoded_sha256'])
                    else:
                        self.assertEqual(target['media_id'], 'cd1:media:' + source['object']['resource'])

    def test_both_listings_and_blank_lines_survive_markdown(self):
        code = [b for b in self.mapping['blocks'] if b['kind'] == 'code']
        self.assertEqual([len(b['members']) for b in code], [37, 173])
        body = self.article['topics'][1]['paragraphs']
        preview = self.files['single/content/previews/cd1/8802162/body.md']
        for block in code:
            row = next(r for r in self.evidence['preview_content_ranges'] if r['block_id'] == block['id'])
            raw = preview[row['content_byte_offset']:row['content_byte_offset'] + row['content_byte_length']]
            expected = recovery.topic_text({'paragraphs': [body[m['paragraph_ordinal'] - 1] for m in block['members']]}).encode()
            self.assertEqual(raw, b'```\n' + expected + b'```\n')
        for row in self.evidence['preview_content_ranges']:
            raw = self.files['single/content/' + row['path']]
            self.assertEqual(digest(raw[row['content_byte_offset']:row['content_byte_offset'] + row['content_byte_length']]), row['sha256'])

    def test_tables_headings_and_caption_links_preserve_source(self):
        blocks = {b['id']: b for b in self.runtime['sections'][1]['blocks']}
        for ordinal, level in keyboard.HEADINGS.items():
            self.assertEqual(blocks[keyboard.block_id(155, ordinal)]['heading_level'], level)
        for ordinal in (24, 35, 49):
            block = blocks[keyboard.block_id(155, ordinal)]
            self.assertEqual(block['type'], 'table')
            self.assertEqual([r['type'] for r in block['paragraphs'][0]['runs']], ['media', 'text'])
            self.assertEqual(block['paragraphs'][0]['runs'][1]['text'], ' ')
        self.assertEqual(len(self.runtime['relationships']), 6)
        for relation, (caption, target) in zip(self.runtime['relationships'], keyboard.CAPTIONS):
            self.assertEqual(relation['from_block'], keyboard.block_id(155, caption))
            self.assertEqual(blocks[relation['to_block']]['paragraphs'][0]['id'], f'cd1-8802162:T155:P{target:03d}')
        preview = self.files['single/content/previews/cd1/8802162/body.md']
        self.assertEqual(preview.count(b'cell structure has not been reconstructed'), 3)

    def test_changed_listing_heading_or_image_attachment_is_rejected(self):
        for ordinal, field, value, message in [(86, 'font_id', 4, 'Listing font'), (10, 'fs', 18, 'Heading evidence')]:
            changed = deepcopy(self.article)
            changed['topics'][1]['paragraphs'][ordinal - 1]['runs'][0]['format'][field] = value
            with self.assertRaisesRegex(ValueError, message):
                keyboard.map_keyboard(changed)
        changed = deepcopy(self.article)
        changed['topics'][1]['paragraphs'][23]['runs'][1]['text'] = 'changed'
        with self.assertRaisesRegex(ValueError, 'Image attachment'):
            keyboard.map_keyboard(changed)

    def test_pixels_relocation_and_predecessor_bytes(self):
        for resource in keyboard.RESOURCES:
            with Image.open(keyboard.ROOT / 'private/cd1-probe/raw' / resource) as source:
                expected, size = source.convert('RGBA').tobytes(), source.size
            with Image.open(io.BytesIO(self.files['single/content/media/cd1/' + resource + '.png'])) as png:
                self.assertEqual(png.size, size)
                self.assertEqual(png.convert('RGBA').tobytes(), expected)
        for which, count, file_count in [('single', 1, 12), ('combined', 6, 56)]:
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / 'relocated'
                prefix = which + '/'
                write_package(root, {p[len(prefix):]: raw for p, raw in self.files.items() if p.startswith(prefix)})
                bundle, _, counts = load_package(root / 'content')
                self.assertEqual(counts['articles'], count)
                self.assertEqual(counts['files'], file_count)
                self.assertEqual(sum(e['link_status'] == 'matched' for e in bundle['issues'][0]['toc']), count)
        previous, manifest, _ = load_package(keyboard.PREVIOUS)
        records = [r for r in manifest['documents'] if r['kind'] == 'article'] + manifest['previews']
        records += [m['asset'] for m in previous['media']['items'] if m['asset']]
        for row in records:
            self.assertEqual(self.files['combined/content/' + row['path']], (keyboard.PREVIOUS / row['path']).read_bytes())


if __name__ == '__main__':
    unittest.main()
