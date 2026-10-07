"""Synthetic segment assembly, UTF-8 offsets, immutable provenance and tamper rejection."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

from PIL import Image

from tools.pdf_restore.assemble import assemble, project, read_segment
from tools.pdf_restore.build import build, check_export
from tools.pdf_restore.inventory import pin, write_json
from tools.pdf_restore.package import page_transform

EXAMPLE = Path(__file__).resolve().parents[1] / 'examples/pdf-article.json'


class PDFAssemblyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'source.pdf').write_bytes(b'synthetic immutable source')
        (self.root / 'TOC.md').write_text('Synthetic canonical TOC')
        runtime = self.root / 'private/pdf-restoration/ocr-runtime'
        write_json(runtime / 'runtime.json', {'synthetic': True})
        template = json.loads(EXAMPLE.read_bytes())
        template['source'].update(pin(self.root, 'source.pdf'))
        template['toc_pin'] = pin(self.root, 'TOC.md')
        pages = []
        for i in range(2):
            page = dict(pdf_index=i, pdf_page=i+1, printed_page=str(i+7), width_pt=100, height_pt=200,
                        rotation=0, MediaBox=[10, 20, 110, 220], CropBox=[10, 20, 110, 220])
            page['pdf_to_upright_normalized'] = page_transform(page)
            pages.append(page)
        inventory = self.root / 'private/pdf-restoration/inventory'
        write_json(inventory / 'sources.json', {'sources': [{**template['source'], 'scope': 'toc-entries-and-cover', 'pages': pages}]})
        (inventory / 'queue.jsonl').write_text(json.dumps(dict(toc_entry_id=template['toc_entry_id'], issue_id=template['issue_id'], source_id=template['source']['id']))+'\n')
        specs = []
        for i, name in enumerate(('opening', 'continuation')):
            base = self.root / 'private' / name
            folder = base / 'ocr'
            folder.mkdir(parents=True)
            package = deepcopy(template)
            page = deepcopy(pages[i])
            if i:
                page['orientation_correction'] = dict(clockwise_degrees=180, evidence='Synthetic inverted title')
                page['pdf_to_upright_normalized'] = page_transform(page)
            code_id, figure_id = f'code{i}', f'figure{i}'
            package.update(pages=[page], regions=[dict(id=code_id, pdf_index=i, kind='code', bbox=[0, 0, 1, .5], notes='Synthetic'),
                                                 dict(id=figure_id, pdf_index=i, kind='figure', bbox=[0, .5, 1, 1], notes='Synthetic')],
                           excluded_regions=[], mapping=dict(status='mapped', evidence=['Observed segment extent'], uncertainties=[]))
            write_json(base / 'map.json', package)
            first_line = 10 + 20*i
            marker = f'⟦G{first_line}⟧'
            text = f'  {first_line} PRINT "한글{marker}"\n{first_line+10} DEF CHR$(&H80)=CHR$(1)\n'
            block = dict(id='block'+str(i), kind='code', text=text, region_ids=[code_id],
                         correction_evidence=['corrections.json#'+code_id], uncertainties=['Glyph bytes unverified.'])
            for id in (code_id, figure_id):
                Image.new('RGB', (20, 30), 'blue').save(folder / (id+'.png'))
            (folder / 'raw.txt').write_text('Unaltered OCR bytes\n')
            (folder / 'raw.tsv').write_text('Unaltered positions\n')
            orientation = {k: page[k] for k in ('orientation_correction',) if k in page}
            write_json(folder / 'raw.settings.json', dict(package={'sha256': pin(base, 'map.json')['sha256']},
                       source_sha256=package['source']['sha256'], pdf_index=i, pdf_page=i+1, region_ids=[code_id], **orientation))
            write_json(folder / 'evidence.json', dict(source_sha256=package['source']['sha256'], pdf_page=i+1,
                       runtime=pin(runtime, 'runtime.json'), **orientation,
                       images=[pin(folder, id+'.png') for id in (code_id, figure_id)],
                       results=[dict(region_ids=[code_id], text=pin(folder, 'raw.txt'), positions=pin(folder, 'raw.tsv'), settings=pin(folder, 'raw.settings.json'))]))
            scan = pin(base, 'ocr/'+code_id+'.png')
            write_json(base / 'corrections.json', dict(article_id=package['id'], map=pin(base, 'map.json'),
                       records=[dict(id=id, scan=pin(base, 'ocr/'+id+'.png'), raw_ocr=pin(base, 'ocr/raw.txt') if id==code_id else None)
                                for id in (code_id, figure_id)], blocks=[block],
                       listing_index=[dict(block_id=block['id'], region_id=code_id, download='listing.txt', utf8_byte_start=0,
                                           utf8_byte_end_exclusive=len(text.encode()), printed_line_range=[first_line,first_line+10])],
                       unresolved_graphics=[dict(id=marker[1:-1], marker=marker, printed_line=first_line, region_id=code_id,
                                                scan=scan, encoded_bytes=None, character_count=None, status='unresolved')],
                       glyph_definitions=[dict(printed_line=first_line+10, printed_code='&H80', region_id=code_id, scan=scan,
                                               download='listing.txt', utf8_byte_start=len(text.splitlines(True)[0].encode()),
                                               utf8_byte_end_exclusive=len(text.encode()), graphic_occurrence_assignment=None)]))
            recipe = dict(map=pin(base, 'map.json'), corrections=pin(base, 'corrections.json'),
                          ocr_bundles=[dict(directory='ocr', manifest=pin(base, 'ocr/evidence.json'))], runtime=pin(runtime, 'runtime.json'),
                          figures=[dict(id=figure_id, region_ids=[figure_id], region_id=figure_id, caption=None)],
                          content_order=[dict(type='figure', id=figure_id), dict(type='block', id=block['id'])],
                          availability='partial', verification=dict(status='sample-reviewed', reviewed_region_ids=[code_id, figure_id],
                          evidence=['Included regions compared'], uncertainties=['Other segment is separate.', 'Glyph bytes unverified.']),
                          gaps=['Other segment is separate.', 'Glyph bytes unverified.'])
            write_json(base / 'recipe.json', recipe)
            output = self.root / 'build' / name
            build(base / 'recipe.json', output, self.root)
            specs.append(dict(name=name, manifest=pin(self.root, output.relative_to(self.root).as_posix()+'/manifest.json')))
        self.recipe = dict(segments=specs, expected_pdf_pages=[1,2], evidence=['Complete source coverage compared with both segments.'],
                           uncertainties=['Code remains unverified.'],
                           resolved_notes=[dict(segment=name, note='Other segment is separate.', reason='Both segments are now assembled.')
                                           for name in ('opening','continuation')])
        self.recipe_path = self.root / 'private/assembly-recipe.json'
        self.output = self.root / 'build/assembled'

    def run_assembly(self, output=None, *, preview=False):
        write_json(self.recipe_path, self.recipe)
        return assemble(self.recipe_path, output or self.output, self.root, preview=preview)

    def rehash(self, folder):
        manifest = json.loads((folder / 'manifest.json').read_bytes())
        manifest['files'] = [pin(folder, row['path']) for row in manifest['files']]
        write_json(folder / 'manifest.json', manifest)
        for spec in self.recipe['segments']:
            if spec['name'] == folder.name:
                spec['manifest'] = pin(self.root, folder.relative_to(self.root).as_posix()+'/manifest.json')

    def rich_segments(self):
        """Two synthetic programs share regional IDs and a split numbered line."""
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = [read_segment(self.root/'build'/s['name'], s['manifest']) for s in self.recipe['segments']]
        texts = ['10 PRINT "한글\n', '    이어짐"\n10 END\n']
        for i, (source, correction) in enumerate(segments):
            # Deliberately repeat IDs across both segments, including the figure.
            code, figure, block = f'code{i}', f'figure{i}', f'block{i}'
            def rename(value):
                if isinstance(value, dict):
                    return {k: rename(v) for k, v in value.items()}
                if isinstance(value, list):
                    return [rename(v) for v in value]
                if isinstance(value, str):
                    return {'code'+str(i): 'code', 'figure'+str(i): 'figure',
                            'block'+str(i): 'block', 'corrections.json#'+code: 'corrections.json#code'}.get(value, value)
                return value
            source, correction = rename(source), rename(correction)
            segments[i] = source, correction
            source['blocks'][0]['text'] = texts[i]
            correction['blocks'] = deepcopy(source['blocks'])
            correction['unresolved_graphics'] = correction['glyph_definitions'] = []
            correction['listing_index'][0].update(utf8_byte_start=0, utf8_byte_end_exclusive=len(texts[i].encode()))
            scan = source['region_assets'][0]['asset']
            start, end = block_ranges(source)['block']
            correction['text_index'] = [dict(block_id='block', region_ids=['code'], scans=[scan],
                download='article.txt', utf8_byte_start=start, utf8_byte_end_exclusive=end)]
            excerpt = '한글' if i == 0 else '이어짐'
            before = texts[i].index(excerpt)
            position = start + len(texts[i][:before].encode())
            correction['text_review_items'] = [dict(block_id='block', region_id='code', scan=scan,
                transcription_excerpt=excerpt, download='article.txt', utf8_byte_start=position,
                utf8_byte_end_exclusive=position+len(excerpt.encode()), note='Faint text', status='review-needed')]
            correction['regional_transcription'] = {'code': texts[i]}
            correction['prose_joins'] = [dict(block_id='block', regions=['code'], separators=[])]
            correction['figure_sequence'] = [dict(figure_id='figure', region_id='figure', caption_block_id=None)]
            correction['image_overlap_notes'] = [dict(region_id='figure', related_regions=['code'], note='Adjacent')]
            correction['listing_groups'] = [dict(listing_id='program', complete_listing=False)]
            correction['numbering_review'] = {'note': 'Printed duplicate 10 retained.'}
            lines, cursor = [], 0
            for n, physical in enumerate(texts[i].splitlines(True)):
                end = cursor + len(physical.encode())
                part = dict(region_id='code', scan=scan, utf8_byte_start=cursor, utf8_byte_end_exclusive=end)
                lines.append(dict(**part, listing_id='program', printed_line=10, printed_line_visible=not(i and n == 0),
                    download='listing.txt', segments=[deepcopy(part)], status='unverified'))
                cursor = end
            correction['listing_line_index'] = lines
            correction['listing_anomalies'] = [dict(**deepcopy(lines[-1]), note='Preserve printing')]
        prior_source, prior_correction = segments[0]
        prior_line = prior_correction['listing_line_index'][-1]
        segments[1][1]['listing_line_index'][0]['prior_segment'] = deepcopy(dict(segment_id='opening',
            manifest=self.recipe['segments'][0]['manifest'],
            listing=next(p for p in prior_source['downloads'] if p['path'] == 'listing.txt'),
            corrections=prior_source['corrections'][0], utf8_byte_start=prior_line['utf8_byte_start'],
            utf8_byte_end_exclusive=prior_line['utf8_byte_end_exclusive'], source_segments=deepcopy(prior_line['segments'])))
        self.recipe['index_mode'] = 'namespaced-v1'
        return segments

    def test_namespaced_indexes_preserve_utf8_fragments_duplicates_and_metadata(self):
        from tools.pdf_restore.assemble import text_bytes
        segments = self.rich_segments()
        package, correction = project(self.recipe, segments)
        article, listing = text_bytes(package)
        self.assertEqual(listing, b''.join(text_bytes(s)[1] for s, _ in segments))
        self.assertEqual([b['id'] for b in package['blocks']], ['opening-block', 'continuation-block'])
        self.assertEqual(len(correction['identity_map']), 8)
        self.assertEqual(len(correction['listing_line_index']), 3)
        logical = correction['logical_listing_line_index']
        self.assertEqual([r['line_id'] for r in logical], ['program:10:1', 'program:10:2'])
        self.assertEqual(len(logical[0]['source_parts']), 2)
        self.assertEqual(listing[logical[0]['utf8_byte_start']:logical[0]['utf8_byte_end_exclusive']].decode(),
                         '10 PRINT "한글\n    이어짐"\n')
        for row in correction['text_review_items']:
            self.assertEqual(article[row['utf8_byte_start']:row['utf8_byte_end_exclusive']].decode(), row['transcription_excerpt'])
        self.assertEqual(correction['prose_joins'][1]['regions'], ['continuation-code'])
        self.assertEqual(correction['image_overlap_notes'][1]['related_regions'], ['continuation-code'])
        self.assertEqual(correction['figure_sequence'][1]['figure_id'], 'continuation-figure')
        self.assertEqual(correction['segments'][1]['original_metadata']['numbering_review'], segments[1][1]['numbering_review'])
        self.assertEqual(correction['listing_anomalies'][1]['logical_line_id'], 'program:10:2')
        self.assertEqual(project(self.recipe, segments), (package, correction))

    def test_namespaced_indexes_reject_bad_ranges_references_and_carried_evidence(self):
        original = self.rich_segments()
        for change in ('text', 'utf8', 'scan', 'region', 'gap', 'parts', 'prior-pin', 'prior-range', 'prior-scan', 'anomaly'):
            segments = deepcopy(original)
            correction = segments[1][1]
            row = correction['listing_line_index'][0]
            if change == 'text': correction['text_index'][0]['utf8_byte_start'] += 1
            if change == 'utf8': correction['text_review_items'][0]['utf8_byte_start'] += 1
            if change == 'scan': correction['text_review_items'][0]['scan']['sha256'] = '0'*64
            if change == 'region': correction['prose_joins'][0]['regions'] = ['missing']
            if change == 'gap': row['utf8_byte_start'] += 1
            if change == 'parts': row['segments'][0]['utf8_byte_end_exclusive'] -= 1
            if change == 'prior-pin': row['prior_segment']['listing']['sha256'] = '0'*64
            if change == 'prior-range': row['prior_segment']['utf8_byte_start'] += 1
            if change == 'prior-scan': row['prior_segment']['source_segments'][0]['scan']['sha256'] = '0'*64
            if change == 'anomaly': correction['listing_anomalies'][0]['printed_line'] = 999
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)

    def prose_segments(self):
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = self.rich_segments()
        for (source, correction), text in zip(segments, ['전송을 시', '작한다.'], strict=True):
            source['blocks'][0].update(kind='prose', text=text)
            source['regions'][0]['kind'] = 'prose'
            correction['blocks'] = deepcopy(source['blocks'])
            correction['regional_transcription'] = {'code': text}
            start, end = block_ranges(source)['block']
            correction['text_index'][0].update(utf8_byte_start=start, utf8_byte_end_exclusive=end)
            for key in ('text_review_items', 'listing_index', 'listing_line_index', 'listing_anomalies'):
                correction[key] = []
        segments[0][1]['segment_continuations'] = [dict(kind='prose', last_region='code',
            last_source_text='전송을 시', next_pdf_page=2, next_source_text='작한다.',
            status='deferred-to-next-segment')]
        segments[1][1]['segment_continuations'] = [dict(kind='prose', prior_segment='opening',
            prior_region='code', region_id='code', prior_text_end='전송을 시',
            text_start='작한다.', join_separator='')]
        return segments

    def test_outgoing_prose_note_matches_incoming_link_without_rewriting_originals(self):
        segments = self.prose_segments()
        original = deepcopy(segments)
        package, correction = project(self.recipe, segments)
        self.assertEqual(segments, original)
        self.assertEqual([b['text'] for b in package['blocks']], ['전송을 시', '작한다.'])
        self.assertEqual(correction['segment_continuations'][0],
                         dict(source_segment='opening', original=original[0][1]['segment_continuations'][0]))
        self.assertEqual(correction['resolved_continuations'], [dict(kind='prose',
            status='linked-reading-blocks', prior_block_id='opening-block',
            block_id='continuation-block', join_separator='', text_normalized=False)])

    def test_outgoing_prose_missing_opening_uses_reviewed_link_and_preserves_native_note(self):
        segments = self.prose_segments()
        outgoing = segments[0][1]['segment_continuations'][0]
        outgoing.pop('next_source_text')
        outgoing.update(direction='outgoing', join_separator='',
                        next_printed_page=segments[1][0]['pages'][0]['printed_page'])
        original = deepcopy(segments)
        package, correction = project(self.recipe, segments)
        self.assertEqual(segments, original)
        self.assertEqual([b['text'] for b in package['blocks']], ['전송을 시', '작한다.'])
        self.assertEqual(correction['outgoing_prose_adaptations'], [dict(
            source_segment='opening', original=outgoing,
            adapted=outgoing | {'next_source_text': '작한다.'})])
        self.assertEqual(len(correction['resolved_continuations']), 1)
        for change in ('page', 'printed-page', 'separator', 'missing', 'duplicate',
                       'prefix', 'suffix', 'direction', 'empty-opening'):
            invalid = deepcopy(original)
            note = invalid[0][1]['segment_continuations'][0]
            incoming = invalid[1][1]['segment_continuations']
            if change == 'page': note['next_pdf_page'] = 3
            if change == 'printed-page': note['next_printed_page'] = 'wrong'
            if change == 'separator': note['join_separator'] = ' '
            if change == 'missing': incoming.clear()
            if change == 'duplicate': incoming.append(deepcopy(incoming[0]))
            if change == 'prefix': incoming[0]['text_start'] = 'wrong'
            if change == 'suffix': note['last_source_text'] = incoming[0]['prior_text_end'] = 'wrong'
            if change == 'direction': note.pop('direction')
            if change == 'empty-opening': note['next_source_text'] = ''
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, invalid)

    def test_outgoing_prose_requires_matching_page_link_and_actual_text(self):
        original = self.prose_segments()
        for change in ('page', 'region', 'outgoing-text', 'incoming-text', 'missing', 'duplicate', 'dangling'):
            segments = deepcopy(original)
            outgoing = segments[0][1]['segment_continuations'][0]
            incoming = segments[1][1]['segment_continuations']
            if change == 'page': outgoing['next_pdf_page'] = 3
            if change == 'region': incoming[0]['region_id'] = 'missing'
            if change == 'outgoing-text': outgoing['last_source_text'] = 'changed'
            if change == 'incoming-text':
                outgoing['next_source_text'] = incoming[0]['text_start'] = 'changed'
            if change == 'missing': incoming.clear()
            if change == 'duplicate': incoming.append(deepcopy(incoming[0]))
            if change == 'dangling': incoming.append(deepcopy(outgoing))
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)

    def legacy_prose_segments(self):
        segments = self.prose_segments()
        segments[0][1]['segment_continuations'] = [dict(region_id='code', block_id='block',
            ending='전송을 시', next_pdf_page=2,
            next_printed_page=segments[1][0]['pages'][0]['printed_page'],
            next_scan_opening='작한다.', status='next-segment-required')]
        segments[1][1]['segment_continuations'][0]['prior_text_end'] = '시'
        return segments

    def test_regional_listing_ranges_require_exact_order_text_and_scan_coverage(self):
        from tools.pdf_restore.assembly_indexes import block_listing_index
        scan = dict(path='scan.png', sha256='synthetic', bytes=1)
        values = {'a': '0200 ; 한글', 'b': '0210 RET'}
        text = ''.join(v + '\n' for v in values.values())
        middle = len((values['a'] + '\n').encode())
        rows = [dict(block_id='code', region_id=id, scan=scan, download='listing.txt',
                     utf8_byte_start=start, utf8_byte_end_exclusive=end)
                for id, start, end in [('a', 0, middle), ('b', middle, len(text.encode()))]]
        context = SimpleNamespace(source=dict(blocks=[dict(id='code', kind='code',
            text=text, region_ids=['a', 'b'])], content_order=[dict(type='block', id='code')]),
            correction=dict(listing_index=rows, regional_transcription=values),
            listing=text.encode(), assets={'a': scan, 'b': scan})
        before = deepcopy(context)
        combined, regional = block_listing_index(context)
        self.assertTrue(regional)
        self.assertEqual(context, before)
        self.assertEqual(combined, [dict(block_id='code', region_ids=['a', 'b'],
            download='listing.txt', utf8_byte_start=0, utf8_byte_end_exclusive=len(text.encode()))])
        for change in ('gap', 'overlap', 'order', 'scan', 'text', 'region', 'block', 'tail'):
            bad = deepcopy(context)
            index = bad.correction['listing_index']
            if change == 'gap': index[1]['utf8_byte_start'] += 1
            if change == 'overlap': index[1]['utf8_byte_start'] -= 1
            if change == 'order': index.reverse()
            if change == 'scan': index[1]['scan'] = dict(scan, path='other.png')
            if change == 'text': bad.correction['regional_transcription']['b'] = 'changed'
            if change == 'region': index[1]['region_id'] = 'missing'
            if change == 'block': bad.source['blocks'][0]['text'] = 'changed'
            if change == 'tail': bad.listing += b'x'
            with self.subTest(change=change), self.assertRaises(ValueError):
                block_listing_index(bad)

    def test_legacy_prose_boundary_preserves_original_and_validates_shorter_suffix(self):
        segments = self.legacy_prose_segments()
        original = deepcopy(segments)
        package, correction = project(self.recipe, segments)
        self.assertEqual(segments, original)
        self.assertEqual([b['text'] for b in package['blocks']], ['전송을 시', '작한다.'])
        adaptation = correction['legacy_continuation_adaptations'][0]
        self.assertEqual(adaptation['original'], original[0][1]['segment_continuations'][0])
        self.assertEqual(adaptation['adapted']['last_source_text'], '시')
        self.assertEqual(len(correction['resolved_continuations']), 1)

    def test_legacy_prose_boundary_rejects_unproved_adaptations(self):
        original = self.legacy_prose_segments()
        for change in ('ending', 'block', 'region', 'page', 'folio', 'opening', 'suffix',
                       'missing', 'duplicate', 'unknown-field'):
            segments = deepcopy(original)
            row = segments[0][1]['segment_continuations'][0]
            incoming = segments[1][1]['segment_continuations']
            if change == 'ending': row['ending'] = 'changed'
            if change == 'block': row['block_id'] = 'missing'
            if change == 'region': row['region_id'] = 'missing'
            if change == 'page': row['next_pdf_page'] = 3
            if change == 'folio': row['next_printed_page'] = 'wrong'
            if change == 'opening': row['next_scan_opening'] = 'changed'
            if change == 'suffix': incoming[0]['prior_text_end'] = 'changed'
            if change == 'missing': incoming.clear()
            if change == 'duplicate': incoming.append(deepcopy(incoming[0]))
            if change == 'unknown-field': row['unrecognized'] = True
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)

    def unnumbered_segments(self):
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = self.rich_segments()
        texts = ['HGR : HCOLOR=3\n10 PRINT "한글"\n.\n', 'POKE 768, 160\n10 END\n.\n']
        for (source, correction), text in zip(segments, texts, strict=True):
            source['blocks'][0]['text'] = text
            correction['blocks'] = deepcopy(source['blocks'])
            correction['regional_transcription']['code'] = text
            correction['text_review_items'] = []
            start, end = block_ranges(source)['block']
            correction['text_index'][0].update(utf8_byte_start=start, utf8_byte_end_exclusive=end)
            correction['listing_index'][0]['utf8_byte_end_exclusive'] = len(text.encode())
            scan = source['region_assets'][0]['asset']
            rows, cursor = [], 0
            for ordinal, line in enumerate(text.splitlines(True), 1):
                end = cursor + len(line.encode())
                part = dict(region_id='code', scan=scan, utf8_byte_start=cursor, utf8_byte_end_exclusive=end)
                numbered = line.startswith('10 ')
                row = dict(**part, listing_id='program', printed_line=10 if numbered else None,
                           printed_line_visible=numbered, physical_line=ordinal,
                           segments=[deepcopy(part)], download='listing.txt')
                if not numbered:
                    row['row_kind'] = 'unnumbered'
                rows.append(row)
                cursor = end
            correction['listing_line_index'] = rows
            correction['listing_anomalies'] = [dict(**deepcopy(rows[-1]), note='Printed ellipsis')]
        return segments

    def test_unnumbered_commands_and_ellipses_stay_independent_across_segments(self):
        from tools.pdf_restore.assemble import text_bytes
        segments = self.unnumbered_segments()
        package, correction = project(self.recipe, segments)
        listing = text_bytes(package)[1]
        logical = correction['logical_listing_line_index']
        self.assertEqual(listing, b'HGR : HCOLOR=3\n10 PRINT "' + '한글'.encode() +
                         b'"\n.\nPOKE 768, 160\n10 END\n.\n')
        self.assertEqual([r['line_id'] for r in logical], [
            'program:unnumbered:1', 'program:10:1', 'program:unnumbered:2',
            'program:unnumbered:3', 'program:10:2', 'program:unnumbered:4'])
        self.assertEqual([listing[r['utf8_byte_start']:r['utf8_byte_end_exclusive']]
                          for r in logical if r.get('row_kind') == 'unnumbered'],
                         [b'HGR : HCOLOR=3\n', b'.\n', b'POKE 768, 160\n', b'.\n'])
        self.assertEqual(correction['resolved_continuations'], [])
        self.assertTrue(all(len(r['source_parts']) == 1 for r in logical))
        self.assertEqual(correction['listing_anomalies'][1]['logical_line_id'], 'program:unnumbered:4')
        self.assertEqual(project(self.recipe, segments), (package, correction))

    def test_unnumbered_rows_require_explicit_identity_without_continuation_evidence(self):
        original = self.unnumbered_segments()
        for change in ('kind', 'number', 'visibility', 'ordinal', 'prior', 'continuation'):
            segments = deepcopy(original)
            row = segments[0][1]['listing_line_index'][0]
            if change == 'kind': row.pop('row_kind')
            if change == 'number': row['printed_line'] = 10
            if change == 'visibility': row['printed_line_visible'] = True
            if change == 'ordinal': row['physical_line'] = 0
            if change == 'prior': row['prior_segment'] = {}
            if change == 'continuation': row['continuation'] = {}
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)

    def listing_block_segments(self):
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = self.rich_segments()
        for i, (source, correction) in enumerate(segments):
            text = f'{10 + i * 10} PRINT "' + ('한글' if i == 0 else '이어짐') + '"\n'
            source['blocks'][0]['text'] = text
            correction['blocks'] = deepcopy(source['blocks'])
            correction['regional_transcription'] = {'code': text}
            start, end = block_ranges(source)['block']
            correction['text_index'][0].update(utf8_byte_start=start, utf8_byte_end_exclusive=end)
            correction['text_review_items'] = correction['listing_anomalies'] = []
            correction['listing_index'][0].update(utf8_byte_start=0, utf8_byte_end_exclusive=len(text.encode()))
            part = dict(region_id='code', scan=source['region_assets'][0]['asset'],
                        utf8_byte_start=0, utf8_byte_end_exclusive=len(text.encode()))
            correction['listing_line_index'] = [dict(**part, listing_id='program', block_id='block',
                printed_line=10 + i * 10, printed_line_visible=True, physical_line=1,
                download='listing.txt', segments=[deepcopy(part)])]
        page = segments[1][0]['pages'][0]['pdf_page']
        segments[0][1]['segment_continuations'] = [dict(block_id='block', direction='outgoing',
            next_pdf_page=page, next_printed_line=20, join_separator='\n', note='Next numbered row')]
        segments[1][1]['segment_continuations'] = [dict(kind='listing-block', prior_segment='opening',
            prior_block_id='block', block_id='block', prior_printed_line=10, printed_line=20,
            join_separator='\n', note='No split physical row')]
        return segments

    def test_printed_line_numbers_preserve_leading_zeros_and_reject_mismatches(self):
        from tools.pdf_restore.assemble import text_bytes
        segments = self.listing_block_segments()
        for i, (source, correction) in enumerate(segments, 1):
            text = f'{i:02}' + source['blocks'][0]['text'][2:]
            source['blocks'][0]['text'] = text
            correction['blocks'] = deepcopy(source['blocks'])
            correction['regional_transcription'] = {'code': text}
            correction['listing_line_index'][0]['printed_line'] = i
            correction['segment_continuations'] = []
        original = deepcopy(segments)
        package, correction = project(self.recipe, segments)
        self.assertEqual(segments, original)
        self.assertEqual(text_bytes(package)[1], b''.join(text_bytes(p)[1] for p, _ in original))
        self.assertEqual([r['printed_line'] for r in correction['logical_listing_line_index']], [1, 2])
        legacy = deepcopy(original)
        for i, (_, native) in enumerate(legacy, 1):
            native['listing_line_index'][0]['printed_line'] = f'{i:02}'
        legacy_package, legacy_correction = project(self.recipe, legacy)
        self.assertEqual(text_bytes(legacy_package)[1], text_bytes(package)[1])
        self.assertEqual([r['printed_line'] for r in legacy_correction['logical_listing_line_index']], ['01', '02'])
        for prefix in ('03', '1X', '-1'):
            with self.subTest(prefix=prefix):
                invalid = deepcopy(original)
                source, native = invalid[0]
                text = prefix + source['blocks'][0]['text'][2:]
                source['blocks'][0]['text'] = text
                native['blocks'] = deepcopy(source['blocks'])
                native['regional_transcription'] = {'code': text}
                with self.assertRaisesRegex(ValueError, 'Printed line differs from indexed bytes'):
                    project(self.recipe, invalid)

    def test_listing_block_boundary_preserves_separate_rows_and_native_records(self):
        from tools.pdf_restore.assemble import text_bytes
        segments = self.listing_block_segments()
        original = deepcopy(segments)
        package, correction = project(self.recipe, segments)
        self.assertEqual(segments, original)
        self.assertEqual(text_bytes(package)[1], b''.join(text_bytes(p)[1] for p, _ in original))
        self.assertEqual([r['printed_line'] for r in correction['logical_listing_line_index']], [10, 20])
        self.assertEqual(correction['resolved_continuations'], [dict(kind='listing-block',
            status='linked-reading-blocks', prior_block_id='opening-block', block_id='continuation-block',
            prior_printed_line=10, printed_line=20, join_separator='\n', text_normalized=False)])
        self.assertEqual(correction['segment_continuations'][0]['original'],
                         original[0][1]['segment_continuations'][0])

    def test_listing_block_boundary_rejects_unproved_or_mismatched_links(self):
        original = self.listing_block_segments()
        for change in ('page', 'number', 'block', 'separator', 'missing', 'duplicate',
                       'incoming-number', 'incoming-prior', 'orphan', 'unknown', 'unnumbered'):
            segments = deepcopy(original)
            outgoing = segments[0][1]['segment_continuations'][0]
            incoming = segments[1][1]['segment_continuations']
            if change == 'page': outgoing['next_pdf_page'] += 1
            if change == 'number': outgoing['next_printed_line'] += 1
            if change == 'block': outgoing['block_id'] = 'missing'
            if change == 'separator': outgoing['join_separator'] = ''
            if change == 'missing': incoming.clear()
            if change == 'duplicate': incoming.append(deepcopy(incoming[0]))
            if change == 'incoming-number': incoming[0]['prior_printed_line'] = 99
            if change == 'incoming-prior': incoming[0]['prior_segment'] = 'missing'
            if change == 'orphan': segments[0][1]['segment_continuations'].clear()
            if change == 'unknown': outgoing['invented'] = True
            if change == 'unnumbered': segments[1][1]['listing_line_index'][0]['printed_line_visible'] = False
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)

    def test_listing_block_adapter_leaves_historical_code_fragment_declarations_unchanged(self):
        segments = self.rich_segments()
        _, expected = project(self.recipe, segments)
        for direction, (_, correction) in zip(('outgoing', 'incoming'), segments):
            correction['segment_continuations'] = [dict(kind='code', direction=direction,
                listing_id='program', printed_line=10, region_id='code', text_normalized=False)]
        _, actual = project(self.recipe, segments)
        self.assertEqual(actual['resolved_continuations'], expected['resolved_continuations'])
        for i, row in enumerate(actual['segment_continuations']):
            self.assertEqual(row['original'], segments[i][1]['segment_continuations'][0])

    def test_namespaced_export_rebuild_and_rehashed_index_tamper(self):
        from tools.pdf_restore.assembly_indexes import block_ranges
        for spec in self.recipe['segments']:
            name = spec['name']
            source, correction = read_segment(self.root/'build'/name, spec['manifest'])
            start, end = block_ranges(source)[source['blocks'][0]['id']]
            correction['text_index'] = [dict(block_id=source['blocks'][0]['id'],
                region_ids=source['blocks'][0]['region_ids'], download='article.txt',
                utf8_byte_start=start, utf8_byte_end_exclusive=end)]
            correction['listing_line_index'] = []
            cursor = 0
            for text in source['blocks'][0]['text'].splitlines(True):
                end = cursor + len(text.encode())
                part = dict(region_id=source['blocks'][0]['region_ids'][0], scan=correction['records'][0]['scan'],
                            utf8_byte_start=cursor, utf8_byte_end_exclusive=end)
                correction['listing_line_index'].append(dict(**part, listing_id='program', printed_line=int(text.split()[0]),
                                                             segments=[deepcopy(part)]))
                cursor = end
            base = self.root/'private'/name
            write_json(base/'corrections.json', correction)
            recipe = json.loads((base/'recipe.json').read_bytes())
            recipe['corrections'] = pin(base, 'corrections.json')
            write_json(base/'recipe.json', recipe)
            output = self.root/'build'/('rich-'+name)
            build(base/'recipe.json', output, self.root)
            spec['manifest'] = pin(self.root, output.relative_to(self.root).as_posix()+'/manifest.json')
        self.recipe['index_mode'] = 'namespaced-v1'
        self.run_assembly()
        repeat = self.root/'build/repeat'
        self.run_assembly(repeat)
        files = lambda d: {p.relative_to(d).as_posix(): p.read_bytes() for p in d.rglob('*') if p.is_file()}
        self.assertEqual(files(self.output), files(repeat))
        correction = json.loads((self.output/'corrections.json').read_bytes())
        correction['text_index'][1]['utf8_byte_start'] += 1
        write_json(self.output/'corrections.json', correction)
        package = json.loads((self.output/'article.json').read_bytes())
        package['corrections'] = [pin(self.output, 'corrections.json')]
        write_json(self.output/'article.json', package)
        self.rehash(self.output)
        with self.assertRaisesRegex(ValueError, 'correction projection'):
            check_export(self.output)

    def standalone_segments(self, prose=False):
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = [read_segment(self.root/'build'/s['name'], s['manifest']) for s in self.recipe['segments']]
        for i, (source, c) in enumerate(segments):
            b = source['blocks'][0]
            b['text'] = '10 PRINT "♥"\nOUT 0:0\n'
            id, region = b['id'], b['region_ids'][0]
            scan = source['region_assets'][0]['asset']
            c['unresolved_graphics'], c['glyph_definitions'] = [], []
            c['listing_index'] = [dict(block_id=id, region_id=region, scan=scan, download='listing.txt',
                utf8_byte_start=0, utf8_byte_end_exclusive=len(b['text'].encode()))]
            c['listing_groups'] = [dict(id=id, block_ids=[id], standalone_example=True, execute_verified=False)]
            c['listing_line_index'] = []
            cursor = 0
            for ordinal, line in enumerate(b['text'].splitlines(True), 1):
                end = cursor + len(line.encode())
                c['listing_line_index'].append(dict(block_id=id, region_id=region, scan=scan,
                    listing_id=id, physical_line=ordinal, row_kind='numbered' if ordinal == 1 else 'immediate-command',
                    printed_line=10 if ordinal == 1 else None, printed_line_visible=ordinal == 1,
                    download='listing.txt', utf8_byte_start=cursor, utf8_byte_end_exclusive=end))
                cursor = end
            c['listing_anomalies'] = [dict(c['listing_index'][0], note='Whole example review; not just one row.')]
            if prose:
                r = dict(source['regions'][0], id='prose', kind='prose')
                source['regions'].append(r)
                source['region_assets'].append(dict(region_id='prose', asset=scan))
                c['records'].append(dict(id='prose', region_ids=['prose'], scan=scan, raw_ocr=None, block_ids=['prose']))
                source['blocks'].append(dict(id='prose', kind='prose', text='한글 시작' if i == 0 else '과 끝',
                    region_ids=['prose'], correction_evidence=['corrections.json#prose'], uncertainties=[]))
                order = dict(type='block', id='prose')
                source['content_order'].insert(0 if i else len(source['content_order']), order)
                source['verification']['reviewed_region_ids'].append('prose')
            c['blocks'] = deepcopy(source['blocks'])
            ranges = block_ranges(source)
            c['text_index'] = [dict(block_id=b['id'], region_ids=b['region_ids'], scans=[scan],
                download='article.txt', utf8_byte_start=ranges[b['id']][0], utf8_byte_end_exclusive=ranges[b['id']][1])
                for b in source['blocks']]
            c['text_review_items'] = []
            for block in source['blocks']:
                excerpt = '♥' if block['kind'] == 'code' else block['text']
                start = ranges[block['id']][0] + len(block['text'][:block['text'].index(excerpt)].encode())
                row = dict(block_id=block['id'], region_id=block['region_ids'][0], scan=scan,
                    transcription_excerpt=excerpt, download='article.txt', utf8_byte_start=start,
                    utf8_byte_end_exclusive=start+len(excerpt.encode()), status='review-needed')
                c['text_review_items'].append(row)
                if excerpt == '♥':
                    c['unresolved_graphics'].append(dict(row, rendered_glyph='♥', machine_byte_verified=False))
            c['regional_transcription'] = {b['region_ids'][0]: b['text'] for b in source['blocks']}
            c['prose_joins'] = []
            c['figure_review_items'] = [dict(figure_id=source['figures'][0]['id'],
                region_id=source['figures'][0]['region_ids'][0], scan=source['figures'][0]['asset'], text_transcribed=False)]
            c['segment_continuations'] = [dict(boundary='end' if i == 0 else 'start', note='Historical format retained')]
        self.recipe.update(index_mode='standalone-examples-v1', prose_joins=[])
        if prose:
            self.recipe['prose_joins'] = [dict(left=dict(segment='opening', block_id='prose', ending='시작'),
                right=dict(segment='continuation', block_id='prose', opening='과 끝'), separator='')]
        return segments

    def caption_segments(self):
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = self.standalone_segments(prose=True)
        for i, (source, correction) in enumerate(segments):
            old_ranges = block_ranges(source)
            scan = source['region_assets'][0]['asset']
            source['regions'].append(dict(source['regions'][0], id='caption', kind='caption'))
            source['region_assets'].append(dict(region_id='caption', asset=scan))
            source['verification']['reviewed_region_ids'].append('caption')
            text = '그림. 한글 ♥' if i == 0 else '그림. 다음 ♠'
            source['blocks'].append(dict(id='caption', kind='caption', text=text,
                region_ids=['caption'], correction_evidence=['corrections.json#caption'], uncertainties=[]))
            # Keep the cross-segment prose join adjacent while moving the first
            # caption ahead of all other text and the second behind it.
            item = dict(type='block', id='caption')
            source['content_order'].insert(0, item) if i == 0 else source['content_order'].append(item)
            ranges = block_ranges(source)
            for key in ('text_index', 'text_review_items', 'unresolved_graphics'):
                for row in correction[key]:
                    delta = ranges[row['block_id']][0] - old_ranges[row['block_id']][0]
                    row['utf8_byte_start'] += delta
                    row['utf8_byte_end_exclusive'] += delta
            start, end = ranges['caption']
            correction['text_index'].append(dict(block_id='caption', region_ids=['caption'],
                scans=[scan], download='article.txt', utf8_byte_start=start, utf8_byte_end_exclusive=end))
            correction['blocks'] = deepcopy(source['blocks'])
            correction['records'].append(dict(id='caption', region_ids=['caption'], scan=scan,
                raw_ocr=None, block_ids=['caption']))
            correction['regional_transcription']['caption'] = text
            correction['figure_sequence'] = [dict(figure_id=source['figures'][0]['id'],
                region_id=source['figures'][0]['region_ids'][0], caption_block_id='caption',
                caption_region_id='caption', caption_download='article.txt', caption_scan=scan,
                caption_utf8_byte_start=start, caption_utf8_byte_end_exclusive=end, caption_text=text)]
        return segments

    def test_figure_caption_spans_project_utf8_ids_scans_and_preserve_originals(self):
        from tools.pdf_restore.assemble import text_bytes
        segments = self.caption_segments()
        untouched = deepcopy(segments)
        package, correction = project(self.recipe, segments)
        article, _ = text_bytes(package)
        self.assertEqual(segments, untouched)
        self.assertEqual(next(b['text'] for b in package['blocks'] if b['kind'] == 'prose'), '한글 시작과 끝')
        for name, row, (_, original) in zip(('opening', 'continuation'),
                correction['figure_sequence'], segments, strict=True):
            native = original['figure_sequence'][0]
            self.assertEqual(article[row['caption_utf8_byte_start']:row['caption_utf8_byte_end_exclusive']].decode(), row['caption_text'])
            self.assertEqual(row['caption_block_id'], name + '-caption')
            self.assertEqual(row['caption_region_id'], name + '-caption')
            self.assertEqual(row['caption_scan']['path'], 'segments/' + name + '/' + native['caption_scan']['path'])
            self.assertEqual(row['source_caption_scan'], native['caption_scan'])
            self.assertEqual(row['source_caption_range'], {k: native['caption_' + k]
                for k in ('utf8_byte_start', 'utf8_byte_end_exclusive')})
        self.assertNotEqual(correction['figure_sequence'][1]['caption_utf8_byte_start'],
            segments[1][1]['figure_sequence'][0]['caption_utf8_byte_start'])
        self.assertEqual(project(self.recipe, segments), (package, correction))

    def test_figure_caption_spans_reject_missing_fields_wrong_sources_and_bytes(self):
        original = self.caption_segments()
        for change in ('missing', 'block', 'kind', 'region', 'scan', 'download', 'bounds', 'utf8', 'text'):
            segments = deepcopy(original)
            source, correction = segments[1]
            row = correction['figure_sequence'][0]
            if change == 'missing': row.pop('caption_text')
            if change == 'block': row['caption_block_id'] = 'missing'
            if change == 'kind': next(b for b in source['blocks'] if b['id'] == 'caption')['kind'] = 'prose'
            if change == 'region': row['caption_region_id'] = 'prose'
            if change == 'scan': row['caption_scan'] = dict(row['caption_scan'], sha256='0' * 64)
            if change == 'download': row['caption_download'] = 'listing.txt'
            if change == 'bounds': row['caption_utf8_byte_end_exclusive'] += 1
            if change == 'utf8': row['caption_utf8_byte_start'] += 1
            if change == 'text': row['caption_text'] = 'wrong'
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)

    def test_standalone_examples_join_prose_and_preserve_glyph_and_listing_ranges(self):
        from tools.pdf_restore.assemble import text_bytes
        segments = self.standalone_segments(prose=True)
        untouched = deepcopy(segments)
        package, c = project(self.recipe, segments)
        self.assertEqual(segments, untouched)
        self.assertEqual(len(package['blocks']), 3)
        joined = next(b for b in package['blocks'] if b['kind'] == 'prose')
        self.assertEqual(joined['text'], '한글 시작과 끝')
        article, listing = text_bytes(package)
        self.assertEqual(listing, b''.join(text_bytes(s)[1] for s, _ in segments))
        self.assertEqual(len(c['listing_groups']), 2)
        self.assertEqual(len({r['line_id'] for r in c['listing_line_index']}), 4)
        self.assertEqual([r['printed_line'] for r in c['listing_line_index']], [10, None, 10, None])
        for r in c['text_review_items'] + c['unresolved_graphics']:
            self.assertEqual(article[r['utf8_byte_start']:r['utf8_byte_end_exclusive']].decode(), r['transcription_excerpt'])
            self.assertTrue(r['scan']['path'].startswith('segments/'))
        self.assertEqual(len(c['source_text_index']), 4)
        self.assertEqual(len(c['text_index']), 3)
        self.assertEqual(c['segments'][1]['original_metadata']['segment_continuations'],
                         segments[1][1]['segment_continuations'])
        self.assertEqual(c['figure_review_items'][1]['figure_id'], 'continuation-figure1')
        self.assertEqual(project(self.recipe, segments), (package, c))

    def test_standalone_projection_rejects_invalid_joins_and_review_evidence(self):
        original = self.standalone_segments(prose=True)
        recipe = deepcopy(self.recipe)
        for change in ('join-text', 'join-order', 'join-kind', 'utf8', 'glyph', 'scan', 'line-range',
                       'line-number', 'inferred-number', 'carried-line', 'group', 'anomaly'):
            segments = deepcopy(original)
            self.recipe = deepcopy(recipe)
            source, c = segments[1]
            if change == 'join-text': self.recipe['prose_joins'][0]['right']['opening'] = 'wrong'
            if change == 'join-order': source['content_order'].reverse()
            if change == 'join-kind': source['blocks'][-1]['kind'] = 'code'
            if change == 'utf8': c['text_review_items'][0]['utf8_byte_start'] += 1
            if change == 'glyph': c['unresolved_graphics'][0]['rendered_glyph'] = 'different'
            if change == 'scan': c['figure_review_items'][0]['scan'] = dict(c['figure_review_items'][0]['scan'], sha256='0'*64)
            if change == 'line-range': c['listing_line_index'][0]['utf8_byte_end_exclusive'] -= 1
            if change == 'line-number': c['listing_line_index'][0]['printed_line'] = 20
            if change == 'inferred-number': c['listing_line_index'][1]['printed_line'] = 20
            if change == 'carried-line': c['listing_line_index'][1]['prior_segment'] = {}
            if change == 'group': c['listing_groups'][0]['standalone_example'] = False
            if change == 'anomaly': c['listing_anomalies'][0]['utf8_byte_end_exclusive'] += 1
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)

    def test_standalone_export_rebuild_and_rehashed_glyph_tamper(self):
        segments = self.standalone_segments()
        for spec, (source, correction) in zip(self.recipe['segments'], segments):
            base = self.root/'private'/spec['name']
            write_json(base/'corrections.json', correction)
            recipe = json.loads((base/'recipe.json').read_bytes())
            recipe['corrections'] = pin(base, 'corrections.json')
            write_json(base/'recipe.json', recipe)
            output = self.root/'build'/('examples-'+spec['name'])
            build(base/'recipe.json', output, self.root)
            spec['manifest'] = pin(self.root, output.relative_to(self.root).as_posix()+'/manifest.json')
        with patch('tools.pdf_restore.ocr.page_ocr', side_effect=AssertionError('No OCR')):
            self.run_assembly()
        repeat = self.root/'build/repeat'
        self.run_assembly(repeat)
        files = lambda d: {p.relative_to(d).as_posix(): p.read_bytes() for p in d.rglob('*') if p.is_file()}
        self.assertEqual(files(self.output), files(repeat))
        c = json.loads((self.output/'corrections.json').read_bytes())
        c['unresolved_graphics'][0]['utf8_byte_start'] += 1
        write_json(self.output/'corrections.json', c)
        package = json.loads((self.output/'article.json').read_bytes())
        package['corrections'] = [pin(self.output, 'corrections.json')]
        write_json(self.output/'article.json', package)
        self.rehash(self.output)
        with self.assertRaisesRegex(ValueError, 'correction projection'):
            check_export(self.output)

    def wrapped_segments(self, split_panel=False, prose=False):
        from collections import Counter
        from tools.pdf_restore.assemble import text_bytes
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = self.standalone_segments(prose=prose)
        self.recipe['index_mode'] = 'wrapped-listing-v1'
        for i, (source, c) in enumerate(segments):
            block = source['blocks'][0]
            block['text'] = '10 PRINT "한\n글"\n10 END\n' if i == 0 else '20 DATA 1\n28,2,-1\n30 END\n'
            if split_panel and i == 0:
                following = deepcopy(block)
                block['text'], following['text'] = '10 PRINT "한\n', '글"\n10 END\n'
                following['id'] = 'second-panel'
                following['region_ids'] = ['second-region']
                following['correction_evidence'] = ['corrections.json#second-region']
                source['blocks'].append(following)
                source['regions'].append(dict(source['regions'][0], id='second-region'))
                source['region_assets'].append(dict(source['region_assets'][0], region_id='second-region'))
                source['verification']['reviewed_region_ids'].append('second-region')
                position = source['content_order'].index(dict(type='block', id=block['id']))
                source['content_order'].insert(position + 1, dict(type='block', id=following['id']))
                c['records'].append(dict(c['records'][0], id='second-region'))
            c.update(blocks=deepcopy(source['blocks']), unresolved_graphics=[],
                     listing_index=[], listing_line_index=[], logical_listing_line_index=[],
                     listing_anomalies=[], data_statements=[], text_review_items=[])
            scans = {r['region_id']: r['asset'] for r in source['region_assets']}
            code = {b['id']: b for b in source['blocks'] if b['kind'] == 'code'}
            order = [r['id'] for r in source['content_order'] if r['type'] == 'block' and r['id'] in code]
            c['listing_groups'] = [dict(listing_id='program', block_ids=order, complete_listing=False,
                                        execute_verified=False)]
            cursor, counts, logical = 0, Counter(), None
            for id in order:
                b = code[id]
                region = b['region_ids'][0]
                start = cursor
                for ordinal, text in enumerate(b['text'].splitlines(True), 1):
                    end = cursor + len(text.encode())
                    number = int(text.split()[0]) if text.split()[0] in ('10', '20', '30') else None
                    part = dict(region_id=region, scan=scans[region], utf8_byte_start=cursor,
                                utf8_byte_end_exclusive=end)
                    if number is not None:
                        counts[number] += 1
                        logical = dict(listing_id='program', printed_line=number, occurrence=counts[number],
                            line_id=f'program:{number}:{counts[number]}', download='listing.txt',
                            utf8_byte_start=cursor, utf8_byte_end_exclusive=end, source_parts=[], segments=[])
                        c['logical_listing_line_index'].append(logical)
                    logical['utf8_byte_end_exclusive'] = end
                    row = dict(**part, block_id=id, listing_id='program', line_id=f'{id}:{ordinal}',
                        physical_line=ordinal, printed_line=number, printed_line_visible=number is not None,
                        row_kind='numbered' if number is not None else 'wrapped-continuation',
                        download='listing.txt', logical_line_id=logical['line_id'], segments=[deepcopy(part)])
                    if number is None:
                        row['continues_printed_line'] = logical['printed_line']
                    logical['source_parts'].append(row['line_id'])
                    logical['segments'].append(deepcopy(part))
                    c['listing_line_index'].append(row)
                    cursor = end
                c['listing_index'].append(dict(block_id=id, region_ids=[region], scan=scans[region],
                    download='listing.txt', utf8_byte_start=start, utf8_byte_end_exclusive=cursor))
            article, listing = text_bytes(source)
            ranges = block_ranges(source)
            c['text_index'] = [dict(block_id=b['id'], region_ids=b['region_ids'],
                scans=[scans[r] for r in b['region_ids']], download='article.txt',
                utf8_byte_start=ranges[b['id']][0], utf8_byte_end_exclusive=ranges[b['id']][1])
                for b in source['blocks']]
            c['regional_transcription'] = {b['region_ids'][0]: b['text'] for b in source['blocks']}
            excerpt = '한' if i == 0 else '28'
            for download, data, destination in [('article.txt', article, c['text_review_items']),
                                                ('listing.txt', listing, c['listing_anomalies'])]:
                start = data.index(excerpt.encode())
                destination.append(dict(block_id=block['id'], region_id=block['region_ids'][0],
                    scan=scans[block['region_ids'][0]], download=download, transcription_excerpt=excerpt,
                    utf8_byte_start=start, utf8_byte_end_exclusive=start+len(excerpt.encode())))
            if i:
                row = c['logical_listing_line_index'][0]
                c['data_statements'] = [dict(printed_line=20, line_id=row['line_id'],
                    literal_values=[128, 2, -1], value_count=3, physical_rows=2,
                    scan=scans[block['region_ids'][0]], download='listing.txt',
                    utf8_byte_start=row['utf8_byte_start'], utf8_byte_end_exclusive=row['utf8_byte_end_exclusive'],
                    physical_newlines_removed_for_index_only=True, original_machine_bytes_verified=False,
                    execution_verified=False)]
        return segments

    def test_wrapped_data_keyword_case_preserves_literal_bytes_and_value_checks(self):
        from tools.pdf_restore.assemble import text_bytes
        segments = self.wrapped_segments()
        source, correction = segments[1]
        source['blocks'][0]['text'] = source['blocks'][0]['text'].replace('20 DATA', '20 dAtA')
        correction['blocks'] = deepcopy(source['blocks'])
        untouched = deepcopy(segments)
        package, projected = project(self.recipe, segments)
        self.assertEqual(segments, untouched)
        self.assertIn(b'20 dAtA 1\n28,2,-1\n', text_bytes(package)[1])
        self.assertEqual(projected['data_statements'][0]['literal_values'], [128, 2, -1])
        segments[1][1]['data_statements'][0]['literal_values'][0] = 129
        with self.assertRaisesRegex(ValueError, 'DATA numeric index'):
            project(self.recipe, segments)

    def scan_noted_wrapped_segments(self):
        segments = self.wrapped_segments(split_panel=True)
        self.recipe['index_mode'] = 'wrapped-scan-notes-v1'
        for source, correction in segments:
            block = source['blocks'][0]
            region = block['region_ids'][0]
            scan = next(r['asset'] for r in source['region_assets'] if r['region_id'] == region)
            correction['unresolved_text'] = [dict(block_id=block['id'], region_id=region,
                scan=scan, markers=['small source punctuation'], note='Original glyph remains uncertain.')]
        return segments

    def test_scan_notes_preserve_evidence_without_inventing_ranges(self):
        segments = self.scan_noted_wrapped_segments()
        segments[0][1]['unresolved_text'].append(deepcopy(segments[0][1]['text_review_items'][0]))
        untouched = deepcopy(segments)
        package, correction = project(self.recipe, segments)
        self.assertEqual(segments, untouched)
        self.assertEqual(len(correction['unresolved_scan_notes']), 2)
        self.assertEqual(len(correction['unresolved_text']), 1)
        self.assertEqual(len(correction['listing_line_index']), 6)
        self.assertEqual(len(correction['logical_listing_line_index']), 4)
        for spec, (source, original), note in zip(self.recipe['segments'], segments,
                                                correction['unresolved_scan_notes']):
            self.assertEqual(note['source_segment'], spec['name'])
            self.assertEqual(note['markers'], original['unresolved_text'][0]['markers'])
            self.assertNotIn('download', note)
            self.assertNotIn('utf8_byte_start', note)
            self.assertTrue(note['scan']['path'].startswith('segments/' + spec['name'] + '/'))
        legacy = dict(self.recipe, index_mode='wrapped-listing-v1')
        with self.assertRaises(KeyError):
            project(legacy, segments)

    def test_scan_notes_reject_wrong_evidence_and_incomplete_ranges(self):
        original = self.scan_noted_wrapped_segments()
        for change in ('block', 'region', 'scan', 'markers', 'note', 'start', 'end', 'download'):
            segments = deepcopy(original)
            row = segments[0][1]['unresolved_text'][0]
            if change == 'block': row['block_id'] = 'unknown'
            if change == 'region': row['region_id'] = 'second-region'
            if change == 'scan': row['scan'] = dict(row['scan'], sha256='0'*64)
            if change == 'markers': row['markers'] = ['']
            if change == 'note': row['note'] = ''
            if change == 'start': row['utf8_byte_start'] = 0
            if change == 'end': row['utf8_byte_end_exclusive'] = 1
            if change == 'download': row['download'] = 'listing.txt'
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)

    def test_scan_notes_export_rebuild_and_rehashed_tamper(self):
        # Use the unsplit fixture so map/OCR bindings remain the original ones.
        segments = self.wrapped_segments()
        self.recipe['index_mode'] = 'wrapped-scan-notes-v1'
        for spec, (source, correction) in zip(self.recipe['segments'], segments):
            block = source['blocks'][0]
            region = block['region_ids'][0]
            correction['unresolved_text'] = [dict(block_id=block['id'], region_id=region,
                scan=next(r['asset'] for r in source['region_assets'] if r['region_id'] == region),
                markers=['uncertain punctuation'], note='Scan remains authoritative.')]
            base = self.root/'private'/spec['name']
            write_json(base/'corrections.json', correction)
            recipe = json.loads((base/'recipe.json').read_bytes())
            recipe['corrections'] = pin(base, 'corrections.json')
            write_json(base/'recipe.json', recipe)
            output = self.root/'build'/('scan-notes-' + spec['name'])
            build(base/'recipe.json', output, self.root)
            spec['manifest'] = pin(self.root, output.relative_to(self.root).as_posix() + '/manifest.json')
        with patch('tools.pdf_restore.ocr.page_ocr', side_effect=AssertionError('No OCR')):
            self.run_assembly()
            repeat = self.root/'build/repeat'
            self.run_assembly(repeat)
        files = lambda d: {p.relative_to(d).as_posix(): p.read_bytes() for p in d.rglob('*') if p.is_file()}
        self.assertEqual(files(self.output), files(repeat))
        c = json.loads((self.output/'corrections.json').read_bytes())
        c['unresolved_scan_notes'][0]['markers'] = ['tampered']
        write_json(self.output/'corrections.json', c)
        package = json.loads((self.output/'article.json').read_bytes())
        package['corrections'] = [pin(self.output, 'corrections.json')]
        write_json(self.output/'article.json', package)
        self.rehash(self.output)
        with self.assertRaisesRegex(ValueError, 'correction projection'):
            check_export(self.output)

    def interrupted_wrapped_segments(self):
        segments = self.wrapped_segments(prose=True)
        source, correction = segments[1]
        # The second segment's opening figure separates the prose fragments.
        order = source['content_order']
        figure = next(row for row in order if row['type'] == 'figure')
        order.remove(figure)
        order.insert(0, figure)
        from tools.pdf_restore.assembly_indexes import block_ranges
        ranges = block_ranges(source)
        blocks = {b['id']: b for b in source['blocks']}
        for row in correction['text_index']:
            row['utf8_byte_start'], row['utf8_byte_end_exclusive'] = ranges[row['block_id']]
        for row in correction['text_review_items']:
            block = blocks[row['block_id']]
            row['utf8_byte_start'] = ranges[block['id']][0] + len(
                block['text'][:block['text'].index(row['transcription_excerpt'])].encode())
            row['utf8_byte_end_exclusive'] = row['utf8_byte_start'] + len(row['transcription_excerpt'].encode())
        self.recipe.update(index_mode='interrupted-wrapped-listing-v1', prose_joins=[dict(
            left=dict(segment='opening', block_id='prose', ending='시작'),
            right=dict(segment='continuation', block_id='prose', opening='과 끝'),
            separator='', intervening=[dict(segment='continuation', **figure)])])
        return segments

    def test_interrupted_wrapped_join_preserves_figures_source_packages_and_ranges(self):
        from tools.pdf_restore.assemble import text_bytes, validate_recipe
        segments = self.interrupted_wrapped_segments()
        untouched = deepcopy(segments)
        validate_recipe(self.recipe)
        package, correction = project(self.recipe, segments)
        self.assertEqual(segments, untouched)
        joined = next(b for b in package['blocks'] if b['kind'] == 'prose')
        self.assertEqual(joined['text'], '한글 시작과 끝')
        self.assertEqual(len(package['figures']), 2)
        self.assertIn(dict(type='figure', id='continuation-figure1'), package['content_order'])
        article, listing = text_bytes(package)
        self.assertEqual(listing, b''.join(text_bytes(s)[1] for s, _ in untouched))
        for row in correction['text_review_items']:
            self.assertEqual(article[row['utf8_byte_start']:row['utf8_byte_end_exclusive']].decode(),
                             row['transcription_excerpt'])
        self.assertEqual(len(correction['listing_line_index']), 6)
        self.assertEqual(len(correction['logical_listing_line_index']), 4)

    def listing_interrupted_segments(self):
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = self.interrupted_wrapped_segments()
        source, correction = segments[1]
        code = next(b for b in source['blocks'] if b['kind'] == 'code')
        title = dict(deepcopy(code), id='listing-heading', kind='title', text='리스트',
                     region_ids=['heading-region'], correction_evidence=['corrections.json#heading-region'])
        source['blocks'].append(title)
        source['regions'].append(dict(source['regions'][0], id='heading-region', kind='title'))
        source['region_assets'].append(dict(source['region_assets'][0], region_id='heading-region'))
        source['verification']['reviewed_region_ids'].append('heading-region')
        correction['records'].append(dict(correction['records'][0], id='heading-region'))
        order = source['content_order']
        order.remove(dict(type='block', id=code['id']))
        order[1:1] = [dict(type='block', id=title['id']), dict(type='block', id=code['id'])]
        correction['blocks'] = deepcopy(source['blocks'])
        correction['regional_transcription']['heading-region'] = title['text']
        ranges = block_ranges(source)
        scans = {r['region_id']: r['asset'] for r in source['region_assets']}
        correction['text_index'] = [dict(block_id=b['id'], region_ids=b['region_ids'],
            scans=[scans[r] for r in b['region_ids']], download='article.txt',
            utf8_byte_start=ranges[b['id']][0], utf8_byte_end_exclusive=ranges[b['id']][1])
            for b in source['blocks']]
        blocks = {b['id']: b for b in source['blocks']}
        for row in correction['text_review_items']:
            block = blocks[row['block_id']]
            row['utf8_byte_start'] = ranges[block['id']][0] + len(
                block['text'][:block['text'].index(row['transcription_excerpt'])].encode())
            row['utf8_byte_end_exclusive'] = row['utf8_byte_start'] + len(row['transcription_excerpt'].encode())
        self.recipe['prose_joins'][0]['intervening'] = [dict(segment='continuation', **item)
                                                      for item in order[:3]]
        return segments

    def test_interrupted_wrapped_listing_heading_preserves_sources_code_and_ranges(self):
        from tools.pdf_restore.assemble import text_bytes
        segments = self.listing_interrupted_segments()
        untouched = deepcopy(segments)
        package, correction = project(self.recipe, segments)
        self.assertEqual(segments, untouched)
        article, listing = text_bytes(package)
        self.assertEqual(listing, b''.join(text_bytes(source)[1] for source, _ in untouched))
        joined = next(b for b in package['blocks'] if b['kind'] == 'prose')
        self.assertEqual(joined['text'], '한글 시작과 끝')
        self.assertIn(dict(type='block', id='continuation-listing-heading'), package['content_order'])
        self.assertEqual(len(correction['listing_line_index']), 6)
        for row in correction['source_text_index'] + correction['text_review_items']:
            value = article[row['utf8_byte_start']:row['utf8_byte_end_exclusive']].decode()
            if 'transcription_excerpt' in row:
                self.assertEqual(value, row['transcription_excerpt'])
            else:
                source = untouched[0 if row['source_segment'] == 'opening' else 1][0]
                block = next(b for b in source['blocks'] if b['id'] == row['source_block_id'])
                self.assertEqual(value, block['text'])

    def test_interrupted_listing_rejects_unreviewed_headings_groups_rows_and_other_modes(self):
        from tools.pdf_restore.assembly_indexes import Segment
        from tools.pdf_restore.assembly_regional import check_intervening
        original = self.listing_interrupted_segments()
        recipe = deepcopy(self.recipe)
        for change in ('omitted', 'reordered', 'unknown-heading', 'undeclared-code', 'damaged-row', 'prose-heading'):
            segments = deepcopy(original)
            self.recipe = deepcopy(recipe)
            source, correction = segments[1]
            if change == 'omitted': self.recipe['prose_joins'][0]['intervening'].pop(1)
            if change == 'reordered': self.recipe['prose_joins'][0]['intervening'].reverse()
            if change == 'unknown-heading': self.recipe['prose_joins'][0]['intervening'][1]['id'] = 'unknown'
            if change == 'undeclared-code': correction['listing_groups'] = []
            if change == 'damaged-row': correction['listing_line_index'][0]['utf8_byte_end_exclusive'] -= 1
            if change == 'prose-heading': source['blocks'][-1]['kind'] = 'prose'
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)
        source, correction = original[1]
        context = Segment(recipe['segments'][1], source, correction, 0)
        items = recipe['prose_joins'][0]['intervening']
        actual = [dict(type=row['type'], id='continuation-'+row['id']) for row in items]
        with self.subTest('other modes keep rejecting listings'), self.assertRaises(ValueError):
            check_intervening(items, actual, [context])
        # A title without its adjacent declared code is not an allowed interruption.
        with self.subTest('isolated title'), self.assertRaises(ValueError):
            check_intervening(items[1:2], actual[1:2], [context], allow_wrapped_listings=True)

    def test_interrupted_wrapped_join_rejects_unreviewed_order_and_unindexed_prose(self):
        segments = self.interrupted_wrapped_segments()
        with self.subTest('missing interruption'):
            recipe = deepcopy(self.recipe)
            recipe['prose_joins'][0]['intervening'] = []
            with self.assertRaisesRegex(ValueError, 'Intervening content differs'):
                project(recipe, segments)
        with self.subTest('unindexed prose interruption'):
            from tools.pdf_restore.assembly_indexes import Segment
            from tools.pdf_restore.assembly_regional import check_intervening
            source, correction = segments[1]
            interruption = [dict(segment='continuation', type='block', id='prose')]
            context = Segment(self.recipe['segments'][1], source, correction, 0)
            with self.assertRaisesRegex(ValueError, 'Intervening prose requires'):
                check_intervening(interruption, [dict(type='block', id='continuation-prose')], [context])

    def test_wrapped_listing_preserves_panel_wraps_duplicates_and_partial_utf8_ranges(self):
        from tools.pdf_restore.assemble import text_bytes
        segments = self.wrapped_segments(split_panel=True)
        untouched = deepcopy(segments)
        p, c = project(self.recipe, segments)
        article, listing = text_bytes(p)
        self.assertEqual(segments, untouched)
        self.assertEqual(listing, b''.join(text_bytes(s)[1] for s, _ in segments))
        self.assertEqual([r['line_id'] for r in c['logical_listing_line_index']],
                         ['program:10:1', 'program:10:2', 'program:20:1', 'program:30:1'])
        first = c['logical_listing_line_index'][0]
        self.assertEqual([r['region_id'] for r in first['segments']], ['opening-code0', 'opening-second-region'])
        self.assertEqual(len(c['listing_line_index']), 6)
        self.assertEqual(len({r['line_id'] for r in c['listing_line_index']}), 6)
        self.assertEqual(c['listing_groups'][0]['numbered_entries'], 4)
        self.assertEqual(len(c['source_listing_groups']), 2)
        self.assertEqual(c['data_statements'][0]['literal_values'], [128, 2, -1])
        for field, data in [('text_review_items', article), ('listing_anomalies', listing)]:
            for r in c[field]:
                self.assertEqual(data[r['utf8_byte_start']:r['utf8_byte_end_exclusive']].decode(), r['transcription_excerpt'])
                self.assertTrue(r['scan']['path'].startswith('segments/'))
        self.assertEqual(c['segments'][1]['original_metadata']['logical_listing_line_index'],
                         segments[1][1]['logical_listing_line_index'])

    def test_wrapped_listing_rejects_tampered_physical_logical_review_and_data_evidence(self):
        original = self.wrapped_segments()
        for change in ('ordinal', 'number', 'orphan', 'logical-link', 'source-parts', 'logical-range',
                       'scan', 'part-scan', 'group', 'duplicate-group', 'utf8', 'excerpt', 'data',
                       'data-range', 'data-verified', 'duplicate-id', 'carried'):
            segments = deepcopy(original)
            c = segments[0][1]
            row = c['listing_line_index'][1]
            if change == 'ordinal': row['physical_line'] = 8
            if change == 'number': row['printed_line'] = 10
            if change == 'orphan': c['listing_line_index'][0]['row_kind'] = 'wrapped-continuation'
            if change == 'logical-link': row['logical_line_id'] = 'program:10:2'
            if change == 'source-parts': c['logical_listing_line_index'][0]['source_parts'].reverse()
            if change == 'logical-range': c['logical_listing_line_index'][0]['utf8_byte_end_exclusive'] -= 1
            if change == 'scan': row['scan']['sha256'] = '0'*64
            if change == 'part-scan': row['segments'][0]['scan']['sha256'] = '0'*64
            if change == 'group': c['listing_groups'][0]['block_ids'] = []
            if change == 'duplicate-group': c['listing_groups'].append(deepcopy(c['listing_groups'][0]))
            if change == 'utf8': c['listing_anomalies'][0]['utf8_byte_start'] += 1
            if change == 'excerpt': c['listing_anomalies'][0]['transcription_excerpt'] = 'wrong'
            if change == 'data': segments[1][1]['data_statements'][0]['literal_values'][0] = 1
            if change == 'data-range': segments[1][1]['data_statements'][0]['utf8_byte_end_exclusive'] -= 1
            if change == 'data-verified': segments[1][1]['data_statements'][0]['execution_verified'] = True
            if change == 'duplicate-id': row['line_id'] = c['listing_line_index'][0]['line_id']
            if change == 'carried': row['prior_segment'] = {}
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)

    def test_wrapped_export_rebuild_and_rehashed_data_tamper(self):
        segments = self.wrapped_segments()
        for spec, (source, correction) in zip(self.recipe['segments'], segments):
            base = self.root/'private'/spec['name']
            write_json(base/'corrections.json', correction)
            recipe = json.loads((base/'recipe.json').read_bytes())
            recipe['corrections'] = pin(base, 'corrections.json')
            write_json(base/'recipe.json', recipe)
            output = self.root/'build'/('wrapped-'+spec['name'])
            build(base/'recipe.json', output, self.root)
            spec['manifest'] = pin(self.root, output.relative_to(self.root).as_posix()+'/manifest.json')
        with patch('tools.pdf_restore.ocr.page_ocr', side_effect=AssertionError('No OCR')):
            self.run_assembly()
        repeat = self.root/'build/repeat'
        self.run_assembly(repeat)
        files = lambda d: {p.relative_to(d).as_posix():p.read_bytes() for p in d.rglob('*') if p.is_file()}
        self.assertEqual(files(self.output), files(repeat))
        c = json.loads((self.output/'corrections.json').read_bytes())
        c['data_statements'][0]['literal_values'][0] = 1
        write_json(self.output/'corrections.json', c)
        p = json.loads((self.output/'article.json').read_bytes())
        p['corrections'] = [pin(self.output, 'corrections.json')]
        write_json(self.output/'article.json', p)
        self.rehash(self.output)
        with self.assertRaisesRegex(ValueError, 'correction projection'):
            check_export(self.output)

    def regional_listing_segments(self):
        segments = self.wrapped_segments(split_panel=True)
        self.recipe.update(index_mode='regional-listing-v1', prose_joins=[])
        for source, c in segments:
            c['regional_text_index'] = [dict(row, region_id=row['region_ids'][0],
                scan=row['scans'][0]) for row in c['text_index']]
            c['unicode_glyphs'] = [dict(row, glyph=row['transcription_excerpt'],
                encoded_bytes=None, source_encoding_verified=False) for row in c['text_review_items']]
        return segments

    def test_regional_listing_projects_both_downloads_without_changing_sources(self):
        from tools.pdf_restore.assemble import text_bytes
        from tools.pdf_restore.assembly_indexes import span
        segments = self.regional_listing_segments()
        untouched = deepcopy(segments)
        p, c = project(self.recipe, segments)
        article, listing = text_bytes(p)
        self.assertEqual(segments, untouched)
        self.assertEqual(listing, b''.join(text_bytes(s)[1] for s, _ in segments))
        self.assertEqual(len(c['regional_text_index']), 3)
        self.assertEqual(len(c['unicode_glyphs']), 2)
        self.assertEqual(len(c['listing_line_index']), 6)
        self.assertEqual(len(c['logical_listing_line_index']), 4)
        for field, data in [('regional_text_index', article), ('unicode_glyphs', article),
                            ('listing_anomalies', listing)]:
            for row in c[field]:
                self.assertEqual(span(row, data), row['transcription_excerpt'])
        # Opt-in projection leaves the historical wrapped result intact.
        old_recipe = dict(self.recipe, index_mode='wrapped-listing-v1')
        _, old = project(old_recipe, segments)
        self.assertNotIn('regional_text_index', old)
        self.assertNotIn('unicode_glyphs', old)
        for key in ('listing_index', 'listing_line_index', 'logical_listing_line_index',
                    'listing_anomalies', 'data_statements', 'text_review_items'):
            self.assertEqual(c[key], old[key])
        with self.assertRaisesRegex(ValueError, 'cannot assemble code'):
            project(dict(self.recipe, index_mode='regional-prose-v1'), segments)

    def test_regional_listing_rejects_damage_to_either_coordinate_system(self):
        original = self.regional_listing_segments()
        for change in ('region', 'glyph', 'physical', 'logical', 'review'):
            segments = deepcopy(original)
            c = segments[0][1]
            if change == 'region': c['regional_text_index'].pop()
            if change == 'glyph': c['unicode_glyphs'][0]['utf8_byte_start'] += 1
            if change == 'physical': c['listing_line_index'][0]['physical_line'] += 1
            if change == 'logical': c['logical_listing_line_index'][0]['source_parts'] = []
            if change == 'review': c['listing_anomalies'][0]['transcription_excerpt'] = 'wrong'
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)

    def mixed_listing_segments(self):
        from tools.pdf_restore.assemble import text_bytes
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = self.regional_listing_segments()
        for i, (source, c) in enumerate(segments):
            block = deepcopy(source['blocks'][0])
            block.update(id='immediate', region_ids=['immediate-region'],
                         text='① POKE 103,1\n② PRINT "한"\n',
                         correction_evidence=['corrections.json#immediate-region'])
            source['blocks'].append(block)
            source['regions'].append(dict(source['regions'][0], id='immediate-region'))
            source['region_assets'].append(dict(source['region_assets'][0], region_id='immediate-region'))
            source['verification']['reviewed_region_ids'].append('immediate-region')
            source['content_order'].insert(0 if i else len(source['content_order']),
                                           dict(type='block', id='immediate'))
            c['records'].append(dict(c['records'][0], id='immediate-region'))
            c['blocks'] = deepcopy(source['blocks'])
            original_size = len(text_bytes(source)[1]) - len(block['text'].encode())
            prefix = len(block['text'].encode()) if i else 0

            def shift(value):
                if isinstance(value, list):
                    for row in value: shift(row)
                elif isinstance(value, dict):
                    for key, child in value.items():
                        if key in ('utf8_byte_start', 'utf8_byte_end_exclusive'):
                            value[key] += prefix
                        elif isinstance(child, (dict, list)):
                            shift(child)
            for key in ('listing_index', 'listing_line_index', 'logical_listing_line_index',
                        'listing_anomalies', 'data_statements'):
                shift(c[key])
            start = 0 if i else original_size
            cursor = start
            scan = source['region_assets'][-1]['asset']
            rows = []
            for ordinal, text in enumerate(block['text'].splitlines(True), 1):
                end = cursor + len(text.encode())
                part = dict(region_id='immediate-region', scan=scan,
                            utf8_byte_start=cursor, utf8_byte_end_exclusive=end)
                rows.append(dict(**part, block_id='immediate', listing_id='immediate',
                    line_id=f'immediate:{ordinal}', physical_line=ordinal, printed_line=None,
                    printed_line_visible=False, row_kind='unnumbered', download='listing.txt',
                    source_label=text[0], segments=[deepcopy(part)]))
                cursor = end
            if i:
                c['listing_line_index'] = rows + c['listing_line_index']
            else:
                c['listing_line_index'].extend(rows)
            c['listing_index'].append(dict(block_id='immediate', region_ids=['immediate-region'],
                scan=scan, download='listing.txt', utf8_byte_start=start, utf8_byte_end_exclusive=cursor))
            c['listing_groups'].append(dict(listing_id='immediate', block_ids=['immediate'],
                                           complete_example=True, execute_verified=False))
            c['listing_anomalies'].append(dict(block_id='immediate', region_id='immediate-region',
                scan=scan, download='listing.txt', transcription_excerpt='①',
                utf8_byte_start=start, utf8_byte_end_exclusive=start+len('①'.encode())))
            scans = {r['region_id']: r['asset'] for r in source['region_assets']}
            ranges = block_ranges(source)
            c['text_index'] = [dict(block_id=b['id'], region_ids=b['region_ids'],
                scans=[scans[r] for r in b['region_ids']], download='article.txt',
                utf8_byte_start=ranges[b['id']][0], utf8_byte_end_exclusive=ranges[b['id']][1])
                for b in source['blocks']]
            c['regional_text_index'] = [dict(row, region_id=row['region_ids'][0], scan=row['scans'][0])
                                        for row in c['text_index']]
            c['regional_transcription']['immediate-region'] = block['text']
            for row in c['text_review_items']:
                text = next(b['text'] for b in source['blocks'] if b['id'] == row['block_id'])
                offset = ranges[row['block_id']][0] + len(text[:text.index(row['transcription_excerpt'])].encode())
                row.update(utf8_byte_start=offset,
                           utf8_byte_end_exclusive=offset+len(row['transcription_excerpt'].encode()))
            c['unicode_glyphs'] = [dict(row, glyph=row['transcription_excerpt'],
                encoded_bytes=None, source_encoding_verified=False) for row in c['text_review_items']]
        return segments

    def test_regional_listing_mixes_unnumbered_examples_with_wrapped_numbered_lines(self):
        from tools.pdf_restore.assemble import text_bytes
        from tools.pdf_restore.assembly_indexes import span
        segments = self.mixed_listing_segments()
        original = deepcopy(segments)
        p, c = project(self.recipe, segments)
        self.assertEqual(segments, original)
        article, listing = text_bytes(p)
        self.assertEqual(listing, b''.join(text_bytes(s)[1] for s, _ in segments))
        self.assertEqual(len(c['listing_line_index']), 10)
        self.assertEqual(len(c['logical_listing_line_index']), 4)
        rows = [r for r in c['listing_line_index'] if r['row_kind'] == 'unnumbered']
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(r['printed_line'] is None and 'logical_line_id' not in r for r in rows))
        self.assertEqual([r['source_label'] for r in rows], ['①', '②', '①', '②'])
        group = next(g for g in c['listing_groups'] if g['listing_id'] == 'immediate')
        self.assertEqual((group['physical_rows'], group['unnumbered_rows'], group['numbered_entries']), (4, 4, 0))
        for field, data in [('regional_text_index', article), ('listing_anomalies', listing)]:
            for row in c[field]:
                self.assertEqual(span(row, data), row['transcription_excerpt'])
        for row in rows:
            original_listing = text_bytes(segments[0 if row['source_segment'] == 'opening' else 1][0])[1]
            self.assertEqual(span(row, listing), span(row['source_range'], original_listing))

    def test_mixed_listing_rejects_inferred_numbers_and_wraps_across_independent_rows(self):
        original = self.mixed_listing_segments()
        for change in ('number', 'missing-number', 'visible', 'logical-link', 'continuation-link', 'orphan-after-example'):
            segments = deepcopy(original)
            row = segments[1][1]['listing_line_index'][0]
            if change == 'number': row['printed_line'] = 1
            if change == 'missing-number': row.pop('printed_line')
            if change == 'visible': row['printed_line_visible'] = True
            if change == 'logical-link': row['logical_line_id'] = 'program:20:1'
            if change == 'continuation-link': row['continues_printed_line'] = 20
            if change == 'orphan-after-example':
                row = segments[1][1]['listing_line_index'][2]
                row.update(row_kind='wrapped-continuation', printed_line=None,
                           printed_line_visible=False, continues_printed_line=20)
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)

    def regional_segments(self, overlined='D̅S̅R̅'):
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = self.standalone_segments(prose=True)
        for i, (source, c) in enumerate(segments):
            block, prose = source['blocks']
            region = block['region_ids'][0]
            block.update(kind='prose', text='분류 | 용도 | 모델 | ' if i == 0 else '1. 인쇄 참조')
            next(r for r in source['regions'] if r['id'] == region)['kind'] = 'prose'
            prose['text'] = '한글 끝과' if i == 0 else f'의 {overlined} 설명.'
            scan = source['region_assets'][0]['asset']
            if i == 0:
                next(r for r in source['regions'] if r['id'] == region)['bbox'] = source['regions'][1]['bbox'][:]
                source['regions'].append(dict(source['regions'][0], id='caption', kind='caption'))
                source['region_assets'].append(dict(region_id='caption', asset=scan))
                c['records'].append(dict(id='caption', region_ids=['caption'], scan=scan, raw_ocr=None))
                source['blocks'].append(dict(id='caption', kind='caption', text='그림 설명', region_ids=['caption'],
                    correction_evidence=['corrections.json#caption'], uncertainties=[]))
                source['verification']['reviewed_region_ids'].append('caption')
                source['content_order'] = [dict(type='block', id='prose'), dict(type='figure', id='figure0'),
                                          dict(type='block', id='caption'), dict(type='block', id='block0')]
            for key in ('listing_index', 'listing_groups', 'listing_line_index', 'listing_anomalies',
                        'unresolved_graphics', 'unicode_glyphs', 'signal_notation_index',
                        'controller_table_index', 'reference_index'):
                c[key] = []
            ranges = block_ranges(source)
            c['blocks'] = deepcopy(source['blocks'])
            c['text_index'], c['regional_text_index'], c['text_review_items'] = [], [], []
            c['regional_transcription'] = {}
            for b in source['blocks']:
                start, end = ranges[b['id']]
                row = dict(block_id=b['id'], region_id=b['region_ids'][0], scan=scan, download='article.txt',
                           utf8_byte_start=start, utf8_byte_end_exclusive=end)
                c['regional_text_index'].append(row)
                c['text_index'].append(dict(row, region_ids=b['region_ids']))
                c['text_review_items'].append(dict(row, transcription_excerpt=b['text']))
                c['regional_transcription'][row['region_id']] = b['text']
            if i == 0:
                row = next(r for r in c['regional_text_index'] if r['block_id'] == 'block0')
                c['controller_table_index'] = [dict(row, table_id='figure0', row=1, classification='분류',
                    purpose='용도', series_8080='모델', series_z80=None, original_blank_cells_preserved=True)]
            else:
                row = next(r for r in c['regional_text_index'] if r['block_id'] == 'prose')
                start = row['utf8_byte_start'] + len('의 '.encode())
                c['unicode_glyphs'] = [dict(row, glyph=overlined, utf8_byte_start=start,
                    utf8_byte_end_exclusive=start+len(overlined.encode()), encoded_bytes=None, source_encoding_verified=False)]
                c['signal_notation_index'] = deepcopy(c['unicode_glyphs'])
                row = next(r for r in c['regional_text_index'] if r['block_id'] == 'block1')
                c['reference_index'] = [dict(row, number=1, transcription_excerpt='1. 인쇄 참조', bibliographically_verified=False)]
        self.recipe.update(index_mode='regional-prose-v1', prose_joins=[dict(
            left=dict(segment='opening', block_id='prose', ending='과'),
            right=dict(segment='continuation', block_id='prose', opening='의'), separator='',
            intervening=[dict(segment='opening', type=kind, id=id) for kind, id in
                         [('figure','figure0'), ('block','caption'), ('block','block0')]])])
        return segments

    def test_regional_prose_preserves_overlined_port_digits_through_a_join(self):
        from tools.pdf_restore.assemble import text_bytes
        from tools.pdf_restore.assembly_indexes import span
        segments = self.regional_segments(overlined='F̅8̅')
        before = deepcopy(segments)
        package, correction = project(self.recipe, segments)
        article, _ = text_bytes(package)
        row, = correction['signal_notation_index']
        self.assertEqual(span(row, article), 'F̅8̅')
        self.assertEqual(row['block_id'], 'opening-prose')
        self.assertEqual(row['region_id'], 'continuation-prose')
        self.assertTrue(row['scan']['path'].startswith('segments/continuation/'))
        self.assertEqual(span(row['source_range'], text_bytes(segments[1][0])[0]), 'F̅8̅')
        self.assertEqual(before, segments)

    def marker_segments(self):
        marker = '⟦TI$-HOME-1⟧'
        segments = self.regional_segments(overlined=marker)
        c = segments[1][1]
        row = deepcopy(c['unicode_glyphs'][0])
        row.pop('glyph')
        row.pop('encoded_bytes')
        row.pop('source_encoding_verified')
        row.update(marker=marker, transcription_excerpt=marker,
                   status='manual-correction-required', original_bytes=None)
        c['unicode_glyphs'], c['signal_notation_index'] = [], []
        c['unresolved_text'] = [deepcopy(row)]
        c['unresolved_graphics'] = [row]
        return segments

    def test_regional_marker_projection_preserves_source_and_joined_utf8_ranges(self):
        from tools.pdf_restore.assemble import text_bytes
        from tools.pdf_restore.assembly_indexes import span
        segments = self.marker_segments()
        before = deepcopy(segments)
        package, correction = project(self.recipe, segments)
        article, _ = text_bytes(package)
        row, = correction['unresolved_graphics']
        self.assertEqual(span(row, article), '⟦TI$-HOME-1⟧')
        self.assertEqual(span(row['source_range'], text_bytes(segments[1][0])[0]), row['marker'])
        self.assertEqual(row['block_id'], 'opening-prose')
        self.assertEqual(row['region_id'], 'continuation-prose')
        self.assertTrue(row['scan']['path'].startswith('segments/continuation/'))
        self.assertIsNone(row['original_bytes'])
        self.assertEqual(before, segments)
        self.assertEqual(project(self.recipe, segments), (package, correction))

    def test_regional_marker_rejects_tampering_and_inferred_character_bytes(self):
        original = self.marker_segments()
        for change in ('marker', 'status', 'bytes', 'encoded', 'verified', 'encoding',
                       'missing-text', 'range', 'scan', 'region', 'malformed'):
            segments = deepcopy(original)
            c = segments[1][1]
            row = c['unresolved_graphics'][0]
            if change == 'marker': row['marker'] = '⟦other⟧'
            if change == 'status': row['status'] = 'verified'
            if change == 'bytes': row['original_bytes'] = [19]
            if change == 'encoded': row['encoded_bytes'] = [19]
            if change == 'verified': row['machine_byte_verified'] = True
            if change == 'encoding': row['source_encoding_verified'] = True
            if change == 'missing-text': c['unresolved_text'] = []
            if change == 'range': row['utf8_byte_start'] += 1
            if change == 'scan': row['scan']['sha256'] = '0'*64
            if change == 'region': row['region_id'] = 'missing'
            if change == 'malformed':
                row['marker'] = row['transcription_excerpt'] = '⟦unclosed'
                c['unresolved_text'] = [deepcopy(row)]
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)

    def test_regional_prose_rejects_incomplete_or_punctuated_overlined_ports(self):
        for glyph in ('F̅8', 'F̅-̅', '\u0305'):
            with self.subTest(glyph=glyph):
                segments = self.regional_segments(overlined=glyph)
                with self.assertRaisesRegex(ValueError, 'complete overlined'):
                    project(self.recipe, segments)

    def test_regional_prose_preserves_interrupted_join_source_ranges_and_blank_cells(self):
        from tools.pdf_restore.assemble import text_bytes
        segments = self.regional_segments()
        before = deepcopy(segments)
        package, c = project(self.recipe, segments)
        self.assertEqual(before, segments)
        self.assertEqual(next(b['text'] for b in package['blocks'] if b['id'] == 'opening-prose'),
                         '한글 끝과의 D̅S̅R̅ 설명.')
        self.assertEqual([r['id'] for r in package['content_order']],
                         ['opening-prose', 'opening-figure0', 'opening-caption', 'opening-block0',
                          'continuation-figure1', 'continuation-block1'])
        data, listing = text_bytes(package)
        self.assertEqual(listing, b'')
        for key in ('regional_text_index', 'controller_table_index', 'unicode_glyphs',
                    'signal_notation_index', 'reference_index'):
            for row in c[key]:
                self.assertEqual(data[row['utf8_byte_start']:row['utf8_byte_end_exclusive']].decode(),
                                 row['transcription_excerpt'])
                self.assertTrue(row['scan']['path'].startswith('segments/'))
                self.assertIn('source_range', row)
        glyph = c['unicode_glyphs'][0]
        self.assertEqual(glyph['region_id'], 'continuation-prose')
        self.assertEqual(glyph['block_id'], 'opening-prose')
        self.assertEqual(c['controller_table_index'][0]['table_id'], 'opening-figure0')
        self.assertIsNone(c['controller_table_index'][0]['series_z80'])
        self.assertEqual(project(self.recipe, segments), (package, c))

    def test_regional_prose_rejects_unreviewed_interruption_and_keeps_legacy_strict(self):
        segments = self.regional_segments()
        recipe = deepcopy(self.recipe)
        for change in ('missing', 'reordered', 'duplicate', 'invented', 'body', 'caption-kind', 'code', 'legacy'):
            current = deepcopy(segments)
            self.recipe = deepcopy(recipe)
            items = self.recipe['prose_joins'][0]['intervening']
            if change == 'missing': items.pop()
            if change == 'reordered': items.reverse()
            if change == 'duplicate': items.append(deepcopy(items[0]))
            if change == 'invented': items[0]['id'] = 'unseen'
            if change == 'body': current[0][1]['controller_table_index'] = []
            if change == 'caption-kind': current[0][0]['blocks'][-1]['kind'] = 'prose'
            if change == 'code': current[1][0]['blocks'][0]['kind'] = 'code'
            if change == 'legacy':
                self.recipe['index_mode'] = 'standalone-examples-v1'
                del self.recipe['prose_joins'][0]['intervening']
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, current)

    def test_regional_prose_rejects_bad_region_utf8_signal_table_and_reference_evidence(self):
        segments = self.regional_segments()
        for change in ('missing-region', 'duplicate-region', 'regional-text', 'regional-block', 'utf8',
                       'glyph', 'foreign-region', 'scan', 'signal', 'signal-inference',
                       'table-cell', 'table-blank', 'table-figure', 'table-number', 'reference', 'reference-number'):
            current = deepcopy(segments)
            source, first = current[0]
            second = current[1][1]
            if change == 'missing-region': second['regional_text_index'].pop()
            if change == 'duplicate-region': second['regional_text_index'].append(second['regional_text_index'][0])
            if change == 'regional-text': second['regional_transcription']['prose'] = '다른 글'
            if change == 'regional-block': second['regional_text_index'][0]['block_id'] = 'prose'
            if change == 'utf8': second['unicode_glyphs'][0]['utf8_byte_start'] += 1
            if change == 'glyph': second['unicode_glyphs'][0]['glyph'] = 'R̅T̅S̅'
            if change == 'foreign-region': second['unicode_glyphs'][0]['region_id'] = 'code1'
            if change == 'scan': second['unicode_glyphs'][0]['scan'] = dict(second['unicode_glyphs'][0]['scan'], sha256='0'*64)
            if change == 'signal': second['signal_notation_index'] = []
            if change == 'signal-inference': second['unicode_glyphs'][0]['source_encoding_verified'] = True
            if change == 'table-cell': first['controller_table_index'][0]['series_8080'] = '교정한 모델'
            if change == 'table-blank': first['controller_table_index'][0]['series_z80'] = ''
            if change == 'table-figure': source['regions'][0]['bbox'] = [0,0,1,.4]
            if change == 'table-number': first['controller_table_index'][0]['row'] = 2
            if change == 'reference': second['reference_index'][0]['transcription_excerpt'] = '수정된 참조'
            if change == 'reference-number': second['reference_index'][0]['number'] = 2
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, current)

    def news_segments(self):
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = self.regional_segments()
        self.recipe['prose_joins'] = []
        for i, (source, c) in enumerate(segments):
            heading = 'block'+str(i)
            for block in source['blocks']:
                if block['id'] == heading:
                    block.update(kind='section-label', text='기사 제목'+str(i))
            for region in source['regions']:
                region['bbox'] = [0, 0, .8, .8]
                if region['id'] == 'code'+str(i):
                    region['kind'] = 'section-label'
            source['excluded_regions'] = [dict(id='ad', kind='advertisement', pdf_index=i,
                                               bbox=[.9, .9, 1, 1], notes='Excluded advertisement')]
            source['content_order'] = [dict(type='block', id='prose'), dict(type='block', id=heading),
                                       dict(type='figure', id='figure'+str(i))]
            if i == 0:
                source['content_order'].append(dict(type='block', id='caption'))
            for key in ('unicode_glyphs', 'signal_notation_index', 'controller_table_index', 'reference_index'):
                c[key] = []
            c['text_index'], c['regional_text_index'], c['text_review_items'] = [], [], []
            c['regional_transcription'] = {}
            ranges = block_ranges(source)
            assets = {r['region_id']: r['asset'] for r in source['region_assets']}
            for block in source['blocks']:
                start, end = ranges[block['id']]
                row = dict(block_id=block['id'], region_ids=block['region_ids'], download='article.txt',
                           scans=[assets[id] for id in block['region_ids']],
                           utf8_byte_start=start, utf8_byte_end_exclusive=end)
                c['text_index'].append(row)
                id = block['region_ids'][0]
                local = dict(block_id=block['id'], region_id=id, scan=assets[id], download='article.txt',
                             utf8_byte_start=start, utf8_byte_end_exclusive=end)
                c['regional_text_index'].append(local)
                c['text_review_items'].append(dict(local, transcription_excerpt=block['text']))
                c['regional_transcription'][id] = block['text']
            c['blocks'] = deepcopy(source['blocks'])
            c['section_header_region_ids'] = ['prose']
            ids = [r['id'] for r in source['content_order'] if r['type'] == 'block' and r['id'] != 'prose']
            c['news_item_index'] = [dict(id='same-story-id', ordinal=1, subsection='부분'+str(i),
                heading_block_id=heading, block_ids=ids, figure_ids=['figure'+str(i)],
                region_ids=[r['id'] for r in source['regions'] if r['id'] != 'prose'],
                pdf_pages=[i+1], printed_pages=[i+7],
                ranges=[deepcopy(next(r for r in c['text_index'] if r['block_id'] == id)) for id in ids],
                complete_printed_news_item=True, historically_verified=False)]
        return segments

    def test_news_items_project_independent_identities_images_headers_and_utf8_ranges(self):
        from tools.pdf_restore.assemble import text_bytes
        from tools.pdf_restore.assembly_indexes import span
        segments = self.news_segments()
        before = deepcopy(segments)
        package, c = project(self.recipe, segments)
        self.assertEqual(segments, before)
        self.assertEqual([r['id'] for r in c['news_item_index']],
                         ['opening-same-story-id', 'continuation-same-story-id'])
        self.assertEqual([r['ordinal'] for r in c['news_item_index']], [1, 2])
        self.assertEqual([r['source_ordinal'] for r in c['news_item_index']], [1, 1])
        self.assertEqual(c['section_header_region_ids'], ['opening-prose', 'continuation-prose'])
        self.assertEqual([r['id'] for r in package['excluded_regions']], ['opening-ad', 'continuation-ad'])
        article, _ = text_bytes(package)
        for i, row in enumerate(c['news_item_index']):
            name = self.recipe['segments'][i]['name']
            self.assertEqual(row['heading_block_id'], name+'-block'+str(i))
            self.assertEqual(row['figure_ids'], [name+'-figure'+str(i)])
            self.assertEqual(row['pdf_pages'], [i+1])
            self.assertEqual(row['printed_pages'], [i+7])
            self.assertEqual(c['segments'][i]['original_metadata']['news_item_index'],
                             segments[i][1]['news_item_index'])
            local, _ = text_bytes(segments[i][0])
            for r in row['ranges']:
                self.assertEqual(span(r, article), span(r['source_range'], local))
                self.assertTrue(all(s['path'].startswith('segments/'+name+'/') for s in r['scans']))
        self.assertEqual(project(self.recipe, segments), (package, c))

    def test_news_items_reject_wrong_ownership_ranges_pages_and_source_claims(self):
        segments = self.news_segments()
        for change in ('missing-header', 'header-overlap', 'excluded-header', 'missing-item', 'duplicate-item',
                       'ordinal', 'heading', 'figure', 'region', 'duplicate-region', 'pdf-page', 'folio',
                       'range', 'utf8', 'scan', 'range-regions', 'order', 'verified', 'incomplete', 'subsection'):
            current = deepcopy(segments)
            source, c = current[0]
            row = c['news_item_index'][0]
            if change == 'missing-header': del c['section_header_region_ids']
            if change == 'header-overlap': c['section_header_region_ids'].append('code0')
            if change == 'excluded-header': c['section_header_region_ids'].append('ad')
            if change == 'missing-item': c['news_item_index'] = []
            if change == 'duplicate-item': c['news_item_index'].append(deepcopy(row))
            if change == 'ordinal': row['ordinal'] = 2
            if change == 'heading': row['heading_block_id'] = 'prose'
            if change == 'figure': row['figure_ids'] = []
            if change == 'region': row['region_ids'].remove('figure0')
            if change == 'duplicate-region': row['region_ids'].append('code0')
            if change == 'pdf-page': row['pdf_pages'] = [2]
            if change == 'folio': row['printed_pages'] = [8]
            if change == 'range': row['ranges'].pop()
            if change == 'utf8': row['ranges'][0]['utf8_byte_start'] += 1
            if change == 'scan': row['ranges'][0]['scans'][0]['sha256'] = '0'*64
            if change == 'range-regions': row['ranges'][0]['region_ids'] = ['prose']
            if change == 'order': row['block_ids'].reverse()
            if change == 'verified': row['historically_verified'] = True
            if change == 'incomplete': row['complete_printed_news_item'] = False
            if change == 'subsection': row['subsection'] = ''
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, current)

    def test_news_projection_keeps_older_exports_unchanged_and_rejects_cross_item_join(self):
        segments = self.regional_segments()
        _, c = project(self.recipe, segments)
        self.assertNotIn('news_item_index', c)
        self.assertNotIn('section_header_region_ids', c)
        news = self.news_segments()
        from tools.pdf_restore.assembly_indexes import block_ranges
        source, original = news[0]
        source['content_order'].append(source['content_order'].pop(0))
        ranges = block_ranges(source)
        for key in ('text_index', 'regional_text_index', 'text_review_items'):
            for row in original[key]:
                row['utf8_byte_start'], row['utf8_byte_end_exclusive'] = ranges[row['block_id']]
        item = original['news_item_index'][0]
        item['ranges'] = [deepcopy(next(r for r in original['text_index'] if r['block_id'] == id))
                          for id in item['block_ids']]
        self.recipe['prose_joins'] = [dict(left=dict(segment='opening', block_id='prose', ending='과'),
            right=dict(segment='continuation', block_id='prose', opening='의'), separator='',
            intervening=[])]
        with self.assertRaisesRegex(ValueError, 'News items cannot use cross-segment prose joins'):
            project(self.recipe, news)

    def test_deterministic_assembly_preserves_segments_offsets_and_review(self):
        original = {name:{p.relative_to(self.root/'build'/name).as_posix():p.read_bytes()
                         for p in (self.root/'build'/name).rglob('*') if p.is_file()}
                    for name in ('opening','continuation')}
        with patch('tools.pdf_restore.ocr.page_ocr', side_effect=AssertionError('No OCR')):
            package = self.run_assembly()
        self.assertEqual(check_export(self.output), package)
        self.assertEqual(package['availability'], 'readable')
        self.assertEqual(package['verification']['status'], 'sample-reviewed')
        self.assertIn('Glyph bytes unverified.', package['gaps'])
        self.assertNotIn('Other segment is separate.', package['gaps'])
        self.assertEqual(package['pages'][1]['rotation'], 0)
        self.assertEqual(package['pages'][1]['orientation_correction']['clockwise_degrees'], 180)
        for name, files in original.items():
            for path, value in files.items():
                self.assertEqual((self.output/'segments'/name/path).read_bytes(), value)
                self.assertEqual((self.root/'build'/name/path).read_bytes(), value)
        listing = (self.output/'listing.txt').read_bytes()
        self.assertEqual(listing, original['opening']['listing.txt']+original['continuation']['listing.txt'])
        corrections = json.loads((self.output/'corrections.json').read_bytes())
        for row in corrections['glyph_definitions']:
            self.assertTrue(listing[row['utf8_byte_start']:row['utf8_byte_end_exclusive']].decode().startswith(str(row['printed_line'])+' DEF'))
        self.assertEqual(corrections['listing_index'][1]['utf8_byte_start'], len(original['opening']['listing.txt']))
        for row in corrections['unresolved_graphics']:
            self.assertTrue((self.output/row['scan']['path']).is_file())
            self.assertIsNone(row['encoded_bytes'])
        with zipfile.ZipFile(self.output/'raw-ocr.zip') as archive:
            self.assertEqual(archive.read('segments/continuation/ocr/raw.settings.json'), original['continuation']['ocr/raw.settings.json'])
            self.assertIn('segments/continuation/map.json', archive.namelist())
        repeat = self.root/'build/repeat'
        self.run_assembly(repeat)
        files = lambda d:{p.relative_to(d).as_posix():p.read_bytes() for p in d.rglob('*') if p.is_file()}
        self.assertEqual(files(self.output),files(repeat))
        with self.assertRaisesRegex(ValueError, 'fresh assembly'):
            self.run_assembly()

    def test_bad_coverage_overlap_and_note_disposition_fail_before_publication(self):
        original = deepcopy(self.recipe)
        variants = [dict(expected_pdf_pages=[1,2,3]), dict(segments=list(reversed(original['segments']))),
                    dict(segments=[original['segments'][0], {**original['segments'][0], 'name':'duplicate'}], resolved_notes=[]),
                    dict(resolved_notes=[dict(segment='opening',note='Not an existing note.',reason='Unsupported')])]
        for change in variants:
            self.recipe = {**deepcopy(original), **change}
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.run_assembly()
            self.assertFalse(self.output.exists())

    def test_segment_identity_duplicates_and_index_errors_are_rejected(self):
        segments = [read_segment(self.root/'build'/s['name'], s['manifest']) for s in self.recipe['segments']]
        for change in ('identity','block','region','range','definition','marker'):
            changed = deepcopy(segments)
            package, corrections = changed[1]
            if change=='identity':package['toc_entry_id']='maso-1983-11-toc-9999'
            if change=='block':
                package['blocks'][0]['id']='block0'
                package['content_order'][1]['id']='block0'
                corrections['listing_index'][0]['block_id']='block0'
            if change=='region':package['regions'][0]['id']='code0'
            if change=='range':corrections['listing_index'][0]['utf8_byte_end_exclusive']-=1
            if change=='definition':corrections['glyph_definitions'][0]['utf8_byte_start']+=1
            if change=='marker':corrections['unresolved_graphics'][0]['marker']='⟦G999⟧'
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe,changed)

    def test_rehashed_ocr_map_mismatch_is_rejected(self):
        folder = self.root/'build/continuation'
        settings = json.loads((folder/'ocr/raw.settings.json').read_bytes())
        settings['package']['sha256']='0'*64
        write_json(folder/'ocr/raw.settings.json',settings)
        package = json.loads((folder/'article.json').read_bytes())
        package['raw_ocr'][0]['settings']=pin(folder,'ocr/raw.settings.json')
        write_json(folder/'article.json',package)
        self.rehash(folder)
        with self.assertRaisesRegex(ValueError,'OCR provenance'):
            self.run_assembly()
        self.assertFalse(self.output.exists())

    def test_raw_tampering_unreviewed_and_unsafe_names_fail_closed(self):
        self.recipe['segments'][0]['name']='../escape'
        with self.assertRaisesRegex(ValueError,'segment name'):
            self.run_assembly()
        self.recipe['segments'][0]['name']='opening'
        folder = self.root/'build/opening'
        package = json.loads((folder/'article.json').read_bytes())
        package['verification']['status']='unreviewed'
        write_json(folder/'article.json',package)
        self.rehash(folder)
        with self.assertRaisesRegex(ValueError,'reviewed segments'):
            self.run_assembly()
        (folder/'ocr/raw.txt').write_text('changed')
        with self.assertRaisesRegex(ValueError,'hash/size'):
            self.run_assembly()
        self.assertFalse(self.output.exists())

    def test_data_assembly_needs_no_renderer_or_html(self):
        from unittest.mock import patch
        with patch('tools.pdf_restore.assemble.render_preview', side_effect=AssertionError('no renderer')):
            package = self.run_assembly()
            self.assertEqual(check_export(self.output), package)
        self.assertFalse(list(self.output.rglob('*.html')))
        self.assertFalse(list(self.output.rglob('*.css')))

    def test_checker_rejects_rehashed_projection_index_and_preview_changes(self):
        self.run_assembly(preview=True)
        originals = {name:(self.output/name).read_bytes() for name in ('article.json','corrections.json','index.html','manifest.json')}
        for target in ('text','offset','preview'):
            for name,value in originals.items():(self.output/name).write_bytes(value)
            package = json.loads(originals['article.json'])
            if target=='text':
                package['blocks'][0]['text']='Altered reading text'
                write_json(self.output/'article.json',package)
            elif target=='offset':
                correction = json.loads(originals['corrections.json'])
                correction['glyph_definitions'][1]['utf8_byte_start']-=1
                write_json(self.output/'corrections.json',correction)
                package['corrections']=[pin(self.output,'corrections.json')]
                write_json(self.output/'article.json',package)
            else:
                (self.output/'index.html').write_bytes(originals['index.html'].replace('한글'.encode(),b'changed'))
            self.rehash(self.output)
            with self.subTest(target=target),self.assertRaisesRegex(ValueError,'Assembly .* differs'):
                check_export(self.output, preview=True)

    def indexed_table_interrupted_segments(self):
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = self.interrupted_wrapped_segments()
        source, correction = segments[1]
        prose = next(b for b in source['blocks'] if b['id'] == 'prose')
        table = dict(deepcopy(prose), id='table', text='열\t값\n한글\t\n',
                     region_ids=['table-region'], correction_evidence=['corrections.json#table-region'])
        source['blocks'].append(table)
        source['regions'].append(dict(source['regions'][0], id='table-region', kind='prose'))
        scan = source['region_assets'][0]['asset']
        source['region_assets'].append(dict(region_id='table-region', asset=scan))
        source['verification']['reviewed_region_ids'].append('table-region')
        correction['records'].append(dict(correction['records'][0], id='table-region'))
        order = source['content_order']
        order.insert(order.index(dict(type='block', id='prose')), dict(type='block', id='table'))
        ranges = block_ranges(source)
        start = ranges['table'][0] + len('열\t값\n'.encode())
        correction['inline_example_index'] = [dict(block_id='table', region_id='table-region',
            scan=scan, download='article.txt', table='1', row_number=1, cells=['한글', ''],
            utf8_byte_start=start, utf8_byte_end_exclusive=ranges['table'][1],
            transcription_excerpt='한글\t\n')]
        for source, c in segments:
            ranges = block_ranges(source)
            scans = {r['region_id']: r['asset'] for r in source['region_assets']}
            c['blocks'] = deepcopy(source['blocks'])
            c['text_index'], c['regional_text_index'], c['text_review_items'] = [], [], []
            c['regional_transcription'] = {}
            for block in source['blocks']:
                rid = block['region_ids'][0]
                start, end = ranges[block['id']]
                row = dict(block_id=block['id'], region_id=rid, scan=scans[rid],
                           download='article.txt', utf8_byte_start=start, utf8_byte_end_exclusive=end)
                c['text_index'].append(dict(row, region_ids=block['region_ids'], scans=[scans[rid]]))
                c['regional_text_index'].append(row)
                c['text_review_items'].append(dict(row, transcription_excerpt=block['text']))
                c['regional_transcription'][rid] = block['text']
        self.recipe['index_mode'] = 'regional-table-listing-v1'
        self.recipe['prose_joins'][0]['intervening'].append(dict(segment='continuation', type='block', id='table'))
        return segments

    def test_indexed_table_join_preserves_blank_cells_prose_code_and_native_metadata(self):
        from tools.pdf_restore.assemble import text_bytes
        segments = self.indexed_table_interrupted_segments()
        original = deepcopy(segments)
        p, c = project(self.recipe, segments)
        self.assertEqual(segments, original)
        article, listing = text_bytes(p)
        self.assertEqual(listing, b''.join(text_bytes(s)[1] for s, _ in original))
        self.assertEqual(next(b['text'] for b in p['blocks'] if b['id'] == 'opening-prose'), '한글 시작과 끝')
        self.assertEqual(next(b['text'] for b in p['blocks'] if b['id'] == 'continuation-table'), '열\t값\n한글\t\n')
        self.assertEqual(c['segments'][1]['original_metadata']['inline_example_index'], original[1][1]['inline_example_index'])
        for row in c['regional_text_index']:
            self.assertEqual(article[row['utf8_byte_start']:row['utf8_byte_end_exclusive']].decode(), row['transcription_excerpt'])

    def test_indexed_table_join_rejects_tampered_cells_scan_ranges_and_unindexed_text(self):
        original = self.indexed_table_interrupted_segments()
        for change in ('cells', 'scan', 'number', 'download', 'range', 'table-id', 'missing', 'prefix', 'trailing'):
            segments = deepcopy(original)
            source, c = segments[1]
            row = c['inline_example_index'][0]
            if change == 'cells': row['cells'][0] = '바꾼 값'
            if change == 'scan': row['scan']['sha256'] = '0'*64
            if change == 'number': row['row_number'] = 2
            if change == 'download': row['download'] = 'listing.txt'
            if change == 'range': row['utf8_byte_start'] += 1
            if change == 'table-id': row['table'] = ''
            if change == 'missing': c['inline_example_index'] = []
            if change == 'prefix': next(b for b in source['blocks'] if b['id'] == 'table')['text'] = '서술문\n열\t값\n한글\t\n'
            if change == 'trailing': next(b for b in source['blocks'] if b['id'] == 'table')['text'] += '추가 문장'
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(self.recipe, segments)

    def test_indexed_table_join_requires_new_opt_in_mode(self):
        segments = self.indexed_table_interrupted_segments()
        for mode in ('regional-listing-v1', 'interrupted-wrapped-listing-v1'):
            with self.subTest(mode=mode), self.assertRaisesRegex(ValueError, 'Intervening prose requires'):
                project(dict(self.recipe, index_mode=mode), segments)



if __name__ == '__main__':
    unittest.main()
