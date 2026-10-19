"""Project printed BASIC/hex literals without interpreting machine data.

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


def project_source_literals(context, result, listing):
    original, source = context.correction, context.source
    need(not any(original.get(k) for k in (
        'tables', 'table_cell_index', 'table_row_index', 'graphic_string_index',
        'music_string_index', 'basic_machine_data_rows', 'basic_machine_data_field_index',
        'basic_hex_data_rows', 'basic_numeric_data_rows', 'basic_panel_data_rows',
        'basic_music_data_rows', 'data_statements')),
        'unsupported table/category indexes require their own projection')
    keys = ('regional_text_index', 'text_review_notes', 'inline_example_index',
            'caption_links', 'image_preservation', 'regional_listing_index',
            'listing_source_uncertainties', 'quoted_source_index', 'basic_data_statements',
            'basic_data_field_index', 'hex_dump_row_index', 'hex_dump_address_index',
            'hex_dump_field_index', 'tables', 'table_cell_index', 'table_row_index')
    for key in keys:
        result.setdefault(key, [])
    result['literal_source_fields_format'] = 'v1'
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

    def article_range(row):
        text, id = span(row, context.article), row.get('block_id')
        need(id in blocks and row.get('download') == 'article.txt',
             'article block/download differs')
        a, z = context.ranges[id]
        need(a <= row[START] < row[END] <= z, 'article range leaves block')
        if 'transcription_excerpt' in row:
            need(row['transcription_excerpt'] == text, 'article excerpt differs')
        if row.get('region_id') is not None:
            rid = row['region_id']
            need(row.get('scan') == context.assets.get(rid) and any(
                r['block_id'] == id and r['region_id'] == rid and
                r[START] <= row[START] < row[END] <= r[END] for r in regional),
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

    physical, logical = original['listing_line_index'], original['logical_listing_line_index']
    pm = {r['line_id']:r for r in physical}
    lm = {r['line_id']:r for r in logical}
    projected_physical = [r for r in result['listing_line_index'] if r['source_segment'] == context.name]
    projected_logical = [r for r in result['logical_listing_line_index'] if r['source_segment'] == context.name]
    pids = {r['source_line_id']:r['line_id'] for r in projected_physical}
    lids = {r['source_line_id']:r['line_id'] for r in projected_logical}
    first_ordinal = len(result['listing_line_index']) - len(physical)
    for ordinal, (row, out) in enumerate(zip(physical, projected_physical, strict=True), 1):
        unverified(row)
        need(row.get('article_physical_line') == ordinal and
             span(row, context.listing) == row.get('text', '') + '\n' and
             row.get('tokens') == row['text'].split(), 'physical text/ordinal/tokens differ')
        out.update(source_article_physical_line=ordinal, article_physical_line=first_ordinal+ordinal)
    first_logical = len(result['logical_listing_line_index']) - len(logical)
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
            need(row.get('scan') == context.assets.get(rid) and any(
                r['block_id'] == row['block_id'] and r['region_id'] == rid and
                r[START] <= row[START] < row[END] <= r[END] for r in regional_listing),
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
                    'printed-decimal-literal' if re.fullmatch(r'-?\s*\d+', text) else
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
