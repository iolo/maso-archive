"""Project printed literals, tables, font definitions and graphic source candidates.

This opt-in schema retains physical whitespace, incomplete hex rows, bare-letter
DATA, source glyph candidates and occurrence identities. It never decodes bytes.
Existing wrapped assembly establishes the physical and logical source units first.
"""
from collections import Counter
from copy import deepcopy
import re

from .assembly_indexes import START, END, span
from .assembly_basic_fields import data_tokens


def need(condition, message):
    if not condition:
        raise ValueError('Literal source fields: ' + message)


def unverified(row, required=True):
    if required:
        need(row.get('source_bytes') == 'unverified' and
             row.get('execution_verified') is False, 'source/execution status differs')
    for key in ('encoded_bytes', 'original_bytes', 'machine_bytes', 'decoded_bytes'):
        need(row.get(key) is None, 'encoded bytes are not source literals')
    for key in ('source_encoding_verified', 'machine_byte_verified',
                'original_machine_bytes_verified', 'checksum_verified', 'execution_verified', 'execute_verified'):
        need(key not in row or row[key] is False, 'false verification claim')


def project_graphic_literals(context, result, listing):
    original, source = context.correction, context.source
    need(not any(original.get(k) for k in (
        'music_string_index', 'basic_machine_data_rows', 'basic_machine_data_field_index',
        'basic_hex_data_rows', 'basic_numeric_data_rows', 'basic_panel_data_rows',
        'basic_music_data_rows', 'data_statements')),
        'unsupported specialized category indexes require their own projection')
    keys = ('regional_text_index', 'text_review_notes', 'inline_example_index',
            'caption_links', 'image_preservation', 'regional_listing_index',
            'listing_source_uncertainties', 'quoted_source_index', 'basic_data_statements',
            'basic_data_field_index', 'hex_dump_row_index', 'hex_dump_address_index',
            'hex_dump_field_index', 'tables', 'table_cell_index', 'table_row_index', 'listing_caption_links')
    for key in keys:
        result.setdefault(key, [])
    result['graphic_table_source_fields_format'] = 'v1'
    blocks = {b['id']: b for b in source['blocks']}
    regional = original.get('regional_text_index', [])
    need({r.get('block_id') for r in regional} == set(blocks),
         'regional block coverage differs')
    for id, (a, z) in context.ranges.items():
        rows = [r for r in regional if r['block_id'] == id]
        need(rows and (rows[0][START], rows[-1][END]) == (a, z) and
             [r.get('region_id') for r in rows] == blocks[id]['region_ids'] and
             all(x[END] == y[START] for x, y in zip(rows, rows[1:])),
             'regional spans must partition each block')

    def references(row):
        revised = context.references(row)
        revised['source_segment'] = context.name
        return revised

    def article_range(row, blank=False):
        a, z = row.get(START), row.get(END)
        need(type(a) is int and type(z) is int and 0 <= a <= z <= len(context.article)
             and (blank or a < z), 'article range leaves download')
        try:
            text = context.article[a:z].decode('utf-8')
        except UnicodeDecodeError as error:
            raise ValueError('Table literal range splits UTF-8') from error
        id = row.get('block_id')
        need(id in blocks and row.get('download') == 'article.txt',
             'article block/download differs')
        a, z = context.ranges[id]
        need(a <= row[START] <= row[END] <= z and (blank or row[START] < row[END]), 'article range leaves block')
        if 'transcription_excerpt' in row:
            need(row['transcription_excerpt'] == text, 'article excerpt differs')
        if row.get('region_id') is not None:
            rid = row['region_id']
            need(row.get('scan') == context.assets.get(rid) and any(
                r['block_id'] == id and r['region_id'] == rid and
                r[START] <= row[START] <= row[END] <= r[END] and (blank or row[START] < row[END]) for r in regional),
                'article regional occurrence or scan differs')
        if 'region_ids' in row:
            need(row['region_ids'] == blocks[id]['region_ids'] and
                 row.get('scans') == [context.assets[r] for r in row['region_ids']],
                 'article whole-block scans differ')
        targets = [r for r in result['source_text_index'] if
                   r['source_segment'] == context.name and r['source_block_id'] == id]
        need(len(targets) == 1 and targets[0]['source_range'] == {START:a, END:z},
             'missing source-block projection')
        target = targets[0]
        delta = target[START] - a
        revised = references(row)
        revised.update(block_id=target['block_id'], source_block_id=id,
                       source_range={START:row[START], END:row[END]},
                       **{START:row[START]+delta, END:row[END]+delta})
        return revised

    for key in ('regional_text_index', 'text_review_notes', 'inline_example_index'):
        for row in original.get(key, []):
            need('transcription_excerpt' in row, 'article field requires exact excerpt')
            if key == 'inline_example_index':
                unverified(row)
            result[key].append(article_range(row))
    for key in ('text_index', 'text_review_items'):
        for row in original.get(key, []):
            article_range(row)  # Existing wrapped projection supplies these indexes.
    result['prose_joins'] = [r for r in result['prose_joins']
                            if r.get('source_segment') != context.name]
    for row in original.get('prose_joins', []):
        rows = [r for r in regional if r['block_id'] == row['block_id']]
        pairs = [(a, z) for a, z in zip(rows, rows[1:]) if
                 a['region_id'] == row['from_region'] and z['region_id'] == row['to_region']]
        need(len(pairs) == 1 and pairs[0][0]['transcription_excerpt'].endswith(row['ending']) and
             pairs[0][1]['transcription_excerpt'].startswith(row['continuation']),
             'prose boundary differs')
        result['prose_joins'].append(references(row) | {
            k:context.identity(row[k], context.regions) for k in ('from_region', 'to_region')})

    figures = {f['id']:f for f in source['figures']}
    sequence = original.get('figure_sequence', [])
    need([r.get('figure_id') for r in sequence] ==
         [r['id'] for r in source['content_order'] if r['type'] == 'figure'],
         'figure reading order differs')
    for row in sequence:
        need(row.get('region_id') in figures[row['figure_id']]['region_ids'] and
             row.get('scan') == context.assets.get(row['region_id']),
             'figure source region/scan differs')
    images = original.get('image_preservation', [])
    regions = {r for f in figures.values() for r in f['region_ids']}
    need(len(images) == len(regions) and {r.get('region_id') for r in images} == regions,
         'image preservation coverage differs')
    for row in images:
        need(row.get('scan') == context.assets.get(row['region_id']), 'image scan differs')
        result['image_preservation'].append(references(row))
    captions = original.get('caption_links', [])
    need([r.get('figure_id') for r in captions] ==
         [r['figure_id'] for r in sequence if figures[r['figure_id']].get('caption') is not None],
         'caption association coverage differs')
    for row in captions:
        figure, caption = figures.get(row.get('figure_id')), blocks.get(row.get('caption_block_id'))
        need(figure is not None and caption is not None and caption['kind'] == 'caption' and
             figure['caption'] == caption['text'] and row['figure_region_id'] in figure['region_ids'] and
             row['caption_region_id'] in caption['region_ids'], 'caption source association differs')
        result['caption_links'].append(references(row) | {
            k:context.identity(row[k], context.regions)
            for k in ('figure_region_id', 'caption_region_id')})

    # A table is a complete TSV source block, with exact occurrence ranges for
    # every cell, including zero-byte blanks and duplicate labels.
    cells, table_rows = original.get('table_cell_index', []), original.get('table_row_index', [])
    used_cells, used_rows, seen_tables = [], [], set()
    for table in original.get('tables', []):
        id = table.get('id')
        need(isinstance(id, str) and id and id not in seen_tables, 'table identity differs')
        seen_tables.add(id)
        unverified(table, required=False)
        bid, rid = table.get('block_id'), table.get('region_id')
        need(bid in blocks and blocks[bid]['kind'] == 'prose' and
             rid in blocks[bid]['region_ids'], 'table source block/region differs')
        rows = ([table['header']] if table.get('header') is not None else []) + table['rows']
        need(rows and all(isinstance(r, list) and r and all(isinstance(v, str) for v in r)
                         for r in rows) and len({len(r) for r in rows}) == 1 and
             blocks[bid]['text'] == '\n'.join('\t'.join(r) for r in rows),
             'table values differ from complete source block')
        selected_cells = [r for r in cells if r.get('table_id') == id]
        selected_rows = [r for r in table_rows if r.get('table_id') == id]
        need(len(selected_cells) == sum(map(len, rows)) and len(selected_rows) == len(rows),
             'table cell/row coverage differs')
        cursor, ci = context.ranges[bid][0], 0
        for ordinal, values in enumerate(rows):
            nr = ordinal if table.get('header') is not None else ordinal+1
            header = table.get('header') is not None and ordinal == 0
            start = cursor
            for nc, text in enumerate(values, 1):
                row = selected_cells[ci]
                ci += 1
                end = cursor+len(text.encode())
                need(row.get('block_id') == bid and row.get('region_id') == rid and
                     (row.get(START), row.get(END)) == (cursor, end) and
                     row.get('row') == nr and row.get('column') == nc and
                     row.get('header') is header and row.get('blank') is (text == '') and
                     row.get('text') == text, 'table cell occurrence/blank differs')
                unverified(row, required=False)
                revised = article_range(row, blank=True)
                revised['table_id'] = context.name+'-'+id
                result['table_cell_index'].append(revised)
                cursor = end+(nc < len(values))
            row = selected_rows[ordinal]
            need(row.get('block_id') == bid and row.get('region_id') == rid and
                 (row.get(START), row.get(END)) == (start, cursor) and
                 row.get('row') == nr and row.get('header') is header and
                 context.article[start:cursor].decode() == '\t'.join(values),
                 'table row occurrence differs')
            unverified(row, required=False)
            revised = article_range(row)
            revised['table_id'] = context.name+'-'+id
            result['table_row_index'].append(revised)
            cursor += 1
        need(cursor-1 == context.ranges[bid][1], 'table leaves source block')
        result['tables'].append(references(table) | {'id':context.name+'-'+id})
        used_cells.extend(selected_cells)
        used_rows.extend(selected_rows)
    need(used_cells == cells and used_rows == table_rows, 'extra/reordered table indexes')

    linked_captions = {r['caption_block_id'] for r in captions}
    for row in original.get('listing_caption_links', []):
        unverified(row, required=False)
        cap = blocks.get(row.get('caption_block_id'))
        groups = [g for g in original['listing_groups'] if g['listing_id'] == row.get('listing_id')]
        fids = row.get('figure_ids')
        need(cap is not None and cap['kind'] == 'caption' and
             row.get('block_id') == cap['id'] and
             row.get('caption_region_id') == row.get('region_id') and
             row['region_id'] in cap['region_ids'] and
             (row.get(START), row.get(END)) == context.ranges[cap['id']] and
             row.get('transcription_excerpt') == cap['text'] and
             len(groups) == 1 and row.get('block_ids') == groups[0]['block_ids'] and
             isinstance(fids, list) and fids and len(fids) == len(set(fids)) and
             fids == [r['figure_id'] for r in sequence if r['figure_id'] in fids],
             'listing caption association/occurrence differs')
        revised = article_range(row)
        revised['caption_region_id'] = context.identity(row['caption_region_id'], context.regions)
        revised['figure_ids'] = [context.identity(id, context.figures) for id in fids]
        result['listing_caption_links'].append(revised)
        linked_captions.add(cap['id'])
    need(linked_captions == {id for id, block in blocks.items() if block['kind'] == 'caption'},
         'source caption coverage differs')

    physical, logical = original['listing_line_index'], original['logical_listing_line_index']
    pm = {r['line_id']:r for r in physical}
    lm = {r['line_id']:r for r in logical}
    projected_physical = [r for r in result['listing_line_index'] if r['source_segment'] == context.name]
    projected_logical = [r for r in result['logical_listing_line_index'] if r['source_segment'] == context.name]
    pids = {r['source_line_id']:r['line_id'] for r in projected_physical}
    lids = {r['source_line_id']:r['line_id'] for r in projected_logical}
    first_ordinal = (result['listing_line_index'].index(projected_physical[0])
                     if projected_physical else 0)
    for ordinal, (row, out) in enumerate(zip(physical, projected_physical, strict=True), 1):
        unverified(row)
        need(row.get('article_physical_line') == ordinal and
             span(row, context.listing) == row.get('text', '') + '\n' and
             row.get('tokens') == row['text'].split(), 'physical text/ordinal/tokens differ')
        out.update(source_article_physical_line=ordinal, article_physical_line=first_ordinal+ordinal)
    first_logical = (result['logical_listing_line_index'].index(projected_logical[0])
                     if projected_logical else 0)
    for ordinal, (row, out) in enumerate(zip(logical, projected_logical, strict=True), 1):
        unverified(row)
        need(row.get('text') == span(row, context.listing) and
             ('logical_line' not in row or row['logical_line'] == ordinal),
             'logical source text/ordinal differs')
        out.update(block_id=context.identity(row['block_id'], context.blocks),
                   text=row['text'], source_bytes='unverified', execution_verified=False,
                   logical_line=first_logical+ordinal)
        if 'logical_line' in row:
            out['source_logical_line'] = row['logical_line']
    for group in original['listing_groups']:
        unverified(group, required=False)
    regional_listing = original.get('regional_listing_index', [])
    for block in (b for b in blocks.values() if b['kind'] == 'code'):
        rows = [r for r in regional_listing if r['block_id'] == block['id']]
        pp = [r for r in physical if r['block_id'] == block['id']]
        need(rows and pp and (rows[0][START], rows[-1][END]) == (pp[0][START], pp[-1][END]) and
             [r['region_id'] for r in rows] == block['region_ids'] and
             all(a[END] == z[START] for a, z in zip(rows, rows[1:])),
             'regional listing must partition its block')
        for row in rows:
            selected = [r for r in pp if r['region_id'] == row['region_id']]
            aa = [r for r in regional if r['block_id'] == block['id'] and
                  r['region_id'] == row['region_id']]
            need(selected and len(aa) == 1 and
                 (row[START], row[END]) == (selected[0][START], selected[-1][END]) and
                 span(row, context.listing) == span(aa[0], context.article),
                 'regional listing differs from physical/article spans')
    need({r.get('block_id') for r in regional_listing} ==
         {b['id'] for b in blocks.values() if b['kind'] == 'code'},
         'regional listing block coverage differs')

    def listing_range(row, unit=None):
        text = span(row, context.listing)
        need(row.get('download') == 'listing.txt', 'listing download differs')
        if unit is not None:
            need(row.get('block_id') == unit['block_id'] and
                 row.get('listing_id') == unit['listing_id'] and
                 unit[START] <= row[START] < row[END] <= unit[END],
                 'listing field leaves its source unit')
            if 'logical_line_id' in row:
                need(row['logical_line_id'] == unit['line_id'] and
                     row.get('printed_line') == unit['printed_line'], 'logical source identity differs')
        if row.get('region_id') is not None:
            rid = row['region_id']
            need(row.get('scan') == context.assets.get(rid) and ('scans' in row or any(
                r['block_id'] == row['block_id'] and r['region_id'] == rid and
                r[START] <= row[START] < row[END] <= r[END] for r in regional_listing)),
                'listing regional occurrence or scan differs')
        if 'scans' in row:
            need(unit is not None, 'multi-scan field requires a source unit')
            scans = []
            for s in unit['segments']:
                if s['scan'] not in scans:
                    scans.append(s['scan'])
            need(row['scans'] == scans and row.get('region_id') == unit['segments'][0]['region_id'],
                 'unit scan sequence differs')
        revised = context.listing_range({k:v for k,v in row.items() if k != 'scans'})
        if 'scans' in row:
            revised['scans'] = [dict(s, path=context.prefix+'/'+s['path']) for s in row['scans']]
        if 'logical_line_id' in row:
            need(row['logical_line_id'] in lids, 'unknown logical source reference')
            revised['logical_line_id'] = lids[row['logical_line_id']]
        if 'source_parts' in row:
            need(unit is not None and row['source_parts'] == unit['source_parts'],
                 'unit physical source parts differ')
            revised['source_parts'] = [pids[p] for p in row['source_parts']]
        if 'segments' in row:
            need(unit is not None, 'source spans require a source unit')
            expected = [dict(region_id=s['region_id'], scan=s['scan'],
                **{START:max(row[START], s[START]), END:min(row[END], s[END])})
                for s in unit['segments']
                if max(row[START], s[START]) < min(row[END], s[END])]
            need(row['segments'] == expected, 'field source spans differ')
            revised['segments'] = [context.listing_range(s) for s in expected]
        need(span(revised, listing) == text, 'projected listing bytes differ')
        return revised

    for row in regional_listing:
        need(row.get('transcription_excerpt') == span(row, context.listing), 'regional listing excerpt differs')
        result['regional_listing_index'].append(listing_range(row))

    expected_quotes = []
    for unit in logical:
        text = unit['text']
        indices = [i for i, ch in enumerate(text) if ch == '"']
        for i in range(0, len(indices), 2):
            a = indices[i]
            closed = i+1 < len(indices)
            z = indices[i+1]+1 if closed else len(text.rstrip('\n'))
            expected_quotes.append((unit, i//2+1, unit[START]+len(text[:a].encode()),
                                    unit[START]+len(text[:z].encode()), text[a:z], closed))
    quotes = original.get('quoted_source_index', [])
    need(len(quotes) == len(expected_quotes), 'quoted source coverage differs')
    for row, (unit, ordinal, a, z, text, closed) in zip(quotes, expected_quotes, strict=True):
        unverified(row)
        need('segments' in row and row.get('literal_ordinal') == ordinal and (row[START], row[END]) == (a, z) and
             row.get('transcription_excerpt') == text and row.get('closing_quote_visible') is closed and
             row.get('contents') == (text[1:-1] if closed else text[1:]) and
             row.get('kind') == 'printed-source-string', 'quote occurrence/content differs')
        result['quoted_source_index'].append(listing_range(row, unit))

    expected_data = [(u, data_tokens(u['text'])) for u in logical if re.match(r'^\d+ DATA ', u['text'])]
    statements, fields = original.get('basic_data_statements', []), original.get('basic_data_field_index', [])
    need(len(statements) == len(expected_data), 'DATA statement coverage differs')
    consumed = []
    for row, (unit, tokens) in zip(statements, expected_data, strict=True):
        unverified(row)
        need('segments' in row and 'source_parts' in row and
             (row[START], row[END]) == (unit[START], unit[END]) and
             row.get('transcription_excerpt') == unit['text'] and
             row.get('literal_values') == [t for _, _, t in tokens] and
             row.get('value_count') == len(tokens), 'DATA literal values differ')
        selected = [r for r in fields if r.get('logical_line_id') == unit['line_id']]
        need(len(selected) == len(tokens), 'DATA field coverage differs')
        for ordinal, (field, (a, z, text)) in enumerate(zip(selected, tokens, strict=True), 1):
            unverified(field)
            kind = ('quoted-source-string' if re.fullmatch(r'"[^"]*"', text, re.S) else
                    'printed-decimal-literal' if re.fullmatch(r'-?\s*\d+(?:\n[ \t]+\d+)*', text) else
                    'bare-letter-source' if re.fullmatch('[A-Za-z]+', text) else None)
            need('segments' in field and kind is not None and field.get('kind') == kind and field.get('field') == ordinal and
                 field.get('text') == text and (field[START], field[END]) ==
                 (unit[START]+len(unit['text'][:a].encode()), unit[START]+len(unit['text'][:z].encode())),
                 'DATA field occurrence/literal differs')
            result['basic_data_field_index'].append(listing_range(field, unit))
        consumed.extend(selected)
        result['basic_data_statements'].append(listing_range(row, unit))
    need(consumed == fields, 'extra/reordered DATA fields')

    hex_rows = original.get('hex_dump_row_index', [])
    expected_hex = [r for r in physical if r['row_kind'] == 'unnumbered']
    need(len(hex_rows) == len(expected_hex), 'hex row coverage differs')
    addresses, fields = original.get('hex_dump_address_index', []), original.get('hex_dump_field_index', [])
    need(len(addresses) == len(hex_rows), 'hex address coverage differs')
    counts, units, consumed = Counter(), {}, []
    for row, physical_row, address in zip(hex_rows, expected_hex, addresses, strict=True):
        text = span(physical_row, context.listing)
        match = re.fullmatch(r'([0-9A-F]{4})- ((?:[0-9A-F]{2} )*[0-9A-F]{2})\n', text)
        need(match is not None, 'unnumbered row is not a declared printed hex row')
        addr, values = match[1], match[2].split(' ')
        counts[physical_row['listing_id'], addr] += 1
        occurrence = counts[physical_row['listing_id'], addr]
        id = row.get('unit_id')
        need('segments' in row and 'source_parts' in row and
             isinstance(id, str) and id and id not in units and
             physical_row.get('source_unit_id') == id and
             row.get('source_line_id') == physical_row['line_id'] and
             row.get('address_literal') == addr and row.get('occurrence') == occurrence and
             (row[START], row[END]) == (physical_row[START], physical_row[END]) and
             row.get('region_id') == physical_row['region_id'] and row.get('scan') == physical_row['scan'] and
             row.get('text') == text and row.get('hex_literals') == values and
             row.get('value_count') == len(values), 'hex unit identity/values differ')
        unit = dict(physical_row, source_parts=[physical_row['line_id']])
        units[id] = unit

        def hex_range(field):
            unverified(field)
            need(all(field.get(k) == row[k] for k in
                 ('unit_id', 'source_line_id', 'address_literal', 'occurrence', 'region_id', 'scan')),
                 'hex field source identity differs')
            revised = listing_range(field, unit)
            revised.update(unit_id=context.name+'-'+id, source_unit_id=id,
                           physical_line_id=pids[physical_row['line_id']])
            return revised

        result['hex_dump_row_index'].append(hex_range(row))
        need(address.get('kind') == 'printed-hex-address' and address.get('text') == addr and
             (address[START], address[END]) == (row[START], row[START]+4),
             'hex address occurrence differs')
        result['hex_dump_address_index'].append(hex_range(address))
        selected = [r for r in fields if r.get('unit_id') == id]
        need(len(selected) == len(values), 'hex literal field coverage differs')
        for ordinal, (field, token) in enumerate(zip(selected, values, strict=True), 1):
            a = row[START]+6+(ordinal-1)*3
            need(field.get('field') == ordinal and field.get('kind') == 'printed-hex-literal' and
                 field.get('text') == token and (field[START], field[END]) == (a, a+2),
                 'hex literal occurrence differs')
            result['hex_dump_field_index'].append(hex_range(field))
        consumed.extend(selected)
        out = next(r for r in projected_physical if r['source_line_id'] == physical_row['line_id'])
        out['unit_id'] = context.name+'-'+id
    need(consumed == fields, 'extra/reordered hex literal fields')
    for row in original.get('listing_source_uncertainties', []):
        unit = lm.get(row.get('logical_line_id')) if 'logical_line_id' in row else units.get(row.get('unit_id'))
        need(unit is not None and (row[START], row[END]) == (unit[START], unit[END]) and
             row.get('transcription_excerpt') == span(row, context.listing),
             'source uncertainty unit/excerpt differs')
        unverified(row, required=False)
        revised = listing_range(row, unit)
        if 'unit_id' in row:
            need(row.get('address_literal') == span(unit, context.listing)[:4],
                 'uncertainty printed address differs')
            revised.update(unit_id=context.name+'-'+row['unit_id'], source_unit_id=row['unit_id'])
        result['listing_source_uncertainties'].append(revised)

    # Specialized fields stay visible in the original correction throughout the
    # projection. No filtered correction view or metadata-only preservation path.
    for key in ('basic_hex_literal_index', 'font_definition_index', 'graphic_string_index'):
        result.setdefault(key, [])
    hex_fields = original.get('basic_hex_literal_index', [])
    expected_hex_fields = []
    for unit in logical:
        for ordinal, match in enumerate(re.finditer(r'&(?:\n[ \t]*)?H[0-9A-F]+', unit['text']), 1):
            a = unit[START] + len(unit['text'][:match.start()].encode())
            z = unit[START] + len(unit['text'][:match.end()].encode())
            expected_hex_fields.append((unit, ordinal, a, z, match[0]))
    need(len(hex_fields) == len(expected_hex_fields), 'BASIC hex literal coverage differs')
    for row, (unit, ordinal, a, z, text) in zip(hex_fields, expected_hex_fields, strict=True):
        unverified(row)
        need(row.get('kind') == 'printed-hex-source-literal' and
             row.get('logical_line_id') == unit['line_id'] and
             row.get('printed_line') == unit['printed_line'] and
             row.get('field') == ordinal and row.get('text') == text and
             (row.get(START), row.get(END)) == (a, z) and 'segments' in row,
             'BASIC hex literal occurrence differs')
        result['basic_hex_literal_index'].append(listing_range(row, unit))

    def whole_source_unit(row, unit, kind):
        unverified(row)
        need(row.get('kind') == kind and row.get('logical_line_id') == unit['line_id'] and
             row.get('printed_line') == unit['printed_line'] and
             (row.get(START), row.get(END)) == (unit[START], unit[END]) and
             row.get('transcription_excerpt') == unit['text'] and
             'source_parts' in row and 'segments' in row,
             'specialized source unit identity/text differs')
        return listing_range(row, unit)

    expected_fonts = [u for u in logical if re.match(r'^\d+ DEF CHR\$', u['text'])]
    fonts = original.get('font_definition_index', [])
    need(len(fonts) == len(expected_fonts), 'font definition coverage differs')
    for row, unit in zip(fonts, expected_fonts, strict=True):
        fields = [r for r in hex_fields if r['logical_line_id'] == unit['line_id']]
        need(row.get('literal_hex_fields') == [r['text'] for r in fields] and
             row.get('literal_count') == len(fields), 'font source literals differ')
        revised = whole_source_unit(row, unit, 'printed-font-definition-source')
        result['font_definition_index'].append(revised)

    expected_graphics = [u for u in logical if any(ord(ch) > 127 for ch in u['text'])]
    graphics = original.get('graphic_string_index', [])
    need(len(graphics) == len(expected_graphics), 'graphic source coverage differs')
    for row, unit in zip(graphics, expected_graphics, strict=True):
        revised = whole_source_unit(row, unit, 'printed-graphic-source-candidate')
        matches = list(re.finditer('⟦[^⟧]+⟧', unit['text']))
        markers = row.get('editorial_markers')
        need(isinstance(markers, list) and len(markers) == len(matches),
             'editorial marker coverage differs')
        projected_markers = []
        for marker, match in zip(markers, matches, strict=True):
            a = unit[START] + len(unit['text'][:match.start()].encode())
            z = unit[START] + len(unit['text'][:match.end()].encode())
            expected_parts = [dict(region_id=s['region_id'], scan=s['scan'],
                **{START:max(a, s[START]), END:min(z, s[END])})
                for s in unit['segments'] if max(a, s[START]) < min(z, s[END])]
            need((marker.get(START), marker.get(END)) == (a, z) and
                 marker.get('text') == match[0] and marker.get('segments') == expected_parts,
                 'editorial marker occurrence or scan differs')
            unverified(marker, required=False)
            need(marker.get('original_encoded_bytes') == 'unverified' and
                 marker.get('length_or_width') == 'unverified',
                 'editorial marker byte/length claim differs')
            out = context.listing_range({k:v for k,v in marker.items() if k != 'segments'})
            out['segments'] = [context.listing_range(s) for s in expected_parts]
            need(span(out, listing) == match[0], 'projected editorial marker bytes differ')
            projected_markers.append(out)
        revised['editorial_markers'] = projected_markers
        result['graphic_string_index'].append(revised)
