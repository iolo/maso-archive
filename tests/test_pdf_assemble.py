"""Synthetic segment assembly, UTF-8 offsets, immutable provenance and tamper rejection."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
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

    def run_assembly(self, output=None):
        write_json(self.recipe_path, self.recipe)
        return assemble(self.recipe_path, output or self.output, self.root)

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

    def wrapped_segments(self, split_panel=False):
        from collections import Counter
        from tools.pdf_restore.assemble import text_bytes
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = self.standalone_segments()
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

    def regional_segments(self):
        from tools.pdf_restore.assembly_indexes import block_ranges
        segments = self.standalone_segments(prose=True)
        for i, (source, c) in enumerate(segments):
            block, prose = source['blocks']
            region = block['region_ids'][0]
            block.update(kind='prose', text='분류 | 용도 | 모델 | ' if i == 0 else '1. 인쇄 참조')
            next(r for r in source['regions'] if r['id'] == region)['kind'] = 'prose'
            prose['text'] = '한글 끝과' if i == 0 else '의 D̅S̅R̅ 설명.'
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
                c['unicode_glyphs'] = [dict(row, glyph='D̅S̅R̅', utf8_byte_start=start,
                    utf8_byte_end_exclusive=start+len('D̅S̅R̅'.encode()), encoded_bytes=None, source_encoding_verified=False)]
                c['signal_notation_index'] = deepcopy(c['unicode_glyphs'])
                row = next(r for r in c['regional_text_index'] if r['block_id'] == 'block1')
                c['reference_index'] = [dict(row, number=1, transcription_excerpt='1. 인쇄 참조', bibliographically_verified=False)]
        self.recipe.update(index_mode='regional-prose-v1', prose_joins=[dict(
            left=dict(segment='opening', block_id='prose', ending='과'),
            right=dict(segment='continuation', block_id='prose', opening='의'), separator='',
            intervening=[dict(segment='opening', type=kind, id=id) for kind, id in
                         [('figure','figure0'), ('block','caption'), ('block','block0')]])])
        return segments

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

    def test_checker_rejects_rehashed_projection_index_and_preview_changes(self):
        self.run_assembly()
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
                check_export(self.output)


if __name__ == '__main__':
    unittest.main()
