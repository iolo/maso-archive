"""Opt-in assembly of source columns, unnumbered examples and numbered text wraps.

Printed columns and physical bytes are never reformatted. Logical source units
are explicit evidence, not inferred instructions or executable machine code.
"""
from collections import Counter
from copy import deepcopy
import re

from .assemble import project_legacy, text_bytes
from .assembly_examples import join_blocks
from .assembly_indexes import START, END, Segment, block_ranges, namespace
from .package import validate_package


def need(condition, message):
    if not condition:
        raise ValueError(message)


def value(row, data, *, blank=False):
    a, z = row.get(START), row.get(END)
    need(type(a) is int and type(z) is int and
         0 <= a <= z <= len(data) and (blank or a < z), 'Mixed source span leaves download')
    try:
        return data[a:z].decode('utf-8')
    except UnicodeDecodeError as error:
        raise ValueError('Mixed source span splits UTF-8') from error


def project_mixed(recipe, originals):
    contexts, normalized, cursor = [], [], 0
    for spec, (source, correction) in zip(recipe['segments'], originals, strict=True):
        need(not correction.get('glyph_definitions') and not correction.get('unresolved_graphics'),
             'Mixed source mode requires text/scan reading notes, not encoded glyph definitions')
        context = Segment(spec, source, correction, cursor)
        contexts.append(context)
        normalized.append(namespace(context))
        cursor += len(context.listing)
    package, result = project_legacy(recipe, normalized)
    positions, resolved = join_blocks(recipe, package, contexts)
    bounds = block_ranges(package)
    article, listing = text_bytes(package)
    fields = ('text_index', 'source_text_index', 'regional_text_index', 'text_review_items',
              'text_review_notes', 'inline_example_index', 'tables', 'table_cell_index',
              'table_row_index', 'caption_links', 'figure_sequence', 'image_preservation',
              'prose_joins', 'source_anomalies', 'listing_groups', 'listing_index',
              'regional_listing_index', 'listing_line_index', 'logical_listing_line_index',
              'assembly_instruction_index', 'assembly_column_index', 'data_definition_index',
              'machine_byte_index', 'listing_source_uncertainties')
    result.update({key: [] for key in fields})
    result.update(index_mode='mixed-source-listing-v1', resolved_continuations=resolved,
                  identity_map=[], regional_transcription={})
    for context, record in zip(contexts, result['segments'], strict=True):
        original, source = context.correction, context.source
        record['original_corrections'] = dict(source['corrections'][0],
            path=context.prefix+'/'+source['corrections'][0]['path'])
        record['original_metadata'] = deepcopy({k: v for k, v in original.items()
                                               if k not in ('records', 'blocks', 'map')})
        for kind, allowed in (('region', context.regions), ('block', context.blocks),
                              ('figure', context.figures)):
            for id in sorted(allowed):
                namespaced = context.identity(id, allowed)
                target, within = positions[namespaced] if kind == 'block' else (namespaced, 0)
                result['identity_map'].append(dict(source_segment=context.name, kind=kind,
                    source_id=id, id=target, source_namespace_id=namespaced,
                    utf8_offset_in_block=within))

        def ident(id):
            need(isinstance(id, str) and bool(id), 'Mixed source identity is empty')
            return context.name+'-'+id

        def references(row):
            revised = context.references(row)
            if revised.get('block_id'):
                revised['block_id'] = positions[revised['block_id']][0]
            if 'block_ids' in revised:
                revised['block_ids'] = [positions[id][0] for id in revised['block_ids']]
            if revised.get('caption_block_id'):
                revised['caption_block_id'] = positions[revised['caption_block_id']][0]
            for key in ('from_region', 'to_region', 'caption_region_id', 'figure_region_id'):
                if row.get(key) is not None:
                    revised[key] = context.identity(row[key], context.regions)
            for key in ('table_id', 'listing_id', 'unit_id', 'line_id',
                        'assembly_unit_id', 'logical_line_id'):
                if row.get(key) is not None:
                    revised[key] = ident(row[key])
            if 'source_parts' in row:
                revised['source_parts'] = [ident(id) for id in row['source_parts']]
            revised['source_segment'] = context.name
            return revised

        local_bounds = context.ranges
        regional = original.get('regional_text_index', [])
        need(len(original.get('text_index', [])) == len(context.blocks) and
             {r['block_id'] for r in original['text_index']} == context.blocks,
             'Mixed text index must cover every source block once')
        for id, (a, z) in local_bounds.items():
            rr = [r for r in regional if r.get('block_id') == id]
            need(bool(rr) and rr[0][START] == a and rr[-1][END] == z and
                 all(x[END] == y[START] for x, y in zip(rr, rr[1:])),
                 'Mixed regional spans must partition each source block')
        need({r.get('block_id') for r in regional} == context.blocks,
             'Mixed regional span identifies an unknown block')

        def text_range(row, *, blank=False, whole=False):
            text = value(row, context.article, blank=blank)
            id = row.get('block_id')
            need(row.get('download') == 'article.txt' and id in local_bounds,
                 'Mixed text span has unknown source block')
            a, z = local_bounds[id]
            block_regions = next(b['region_ids'] for b in source['blocks'] if b['id'] == id)
            need(a <= row[START] <= row[END] <= z and
                 (not whole or (a, z) == (row[START], row[END])),
                 'Mixed text span leaves source block')
            if 'region_ids' in row:
                need(set(row['region_ids']) <= set(block_regions) and
                     (not whole or row['region_ids'] == block_regions),
                     'Mixed text region membership differs')
            if whole:
                need(row.get('scans') == [context.assets[r] for r in block_regions],
                     'Mixed whole-block scans differ')
            if row.get('region_id') is not None:
                rid = row['region_id']
                need(rid in next(b['region_ids'] for b in source['blocks'] if b['id'] == id) and
                     row.get('scan') == context.assets.get(rid) and any(
                         r['block_id'] == id and r['region_id'] == rid and
                         r[START] <= row[START] <= row[END] <= r[END] for r in regional),
                     'Mixed text span leaves its named region')
            revised = references(row)
            target, within = positions[context.identity(id, context.blocks)]
            delta = bounds[target][0] + within - a
            revised.update(source_block_id=id, source_range={START: row[START], END: row[END]},
                           **{START: row[START]+delta, END: row[END]+delta})
            need(value(revised, article, blank=blank) == text, 'Projected mixed text bytes differ')
            return revised

        for row in original['text_index']:
            result['source_text_index'].append(text_range(row, whole=True))
        for key in ('regional_text_index', 'text_review_items', 'text_review_notes',
                    'inline_example_index'):
            for row in original.get(key, []):
                need(value(row, context.article) == row.get('transcription_excerpt'),
                     'Mixed text review excerpt differs')
                result[key].append(text_range(row))
        table_cells, table_rows = [], []
        for table in original.get('tables', []):
            id, rid, tid = table['block_id'], table['region_id'], table['id']
            header = table.get('header')
            need(type(table.get('header_rows')) is int and
                 table['header_rows'] == (1 if header else 0), 'Mixed table header count differs')
            rows = ([header] if header else []) + table['rows']
            text = '\n'.join('\t'.join(row) for row in rows)
            need(id in context.blocks and text == context.article[slice(*local_bounds[id])].decode(),
                 'Mixed table differs from printed row bytes')
            cells = [r for r in original.get('table_cell_index', []) if r.get('table_id') == tid]
            indexed_rows = [r for r in original.get('table_row_index', []) if r.get('table_id') == tid]
            need(len(cells) == sum(map(len, rows)) and len(indexed_rows) == len(rows),
                 'Mixed table cell/row coverage differs')
            offset, index = local_bounds[id][0], 0
            for ordinal, row in enumerate(rows):
                number, start = (ordinal if header else ordinal+1), offset
                for column, cell in enumerate(row, 1):
                    expected = cells[index]
                    end = offset+len(cell.encode())
                    need(all(expected.get(k) == v for k, v in dict(
                        table_id=tid, block_id=id, region_id=rid, row=number, column=column,
                        header=bool(header) and ordinal == 0, text=cell, blank=cell == '',
                        utf8_byte_start=offset, utf8_byte_end_exclusive=end).items()),
                        'Mixed table cell identity/bytes differ')
                    table_cells.append(expected)
                    result['table_cell_index'].append(text_range(expected, blank=True))
                    offset, index = end+(column < len(row)), index+1
                expected = indexed_rows[ordinal]
                need(all(expected.get(k) == v for k, v in dict(block_id=id, region_id=rid,
                    row=number, header=bool(header) and ordinal == 0,
                    utf8_byte_start=start, utf8_byte_end_exclusive=offset).items()),
                    'Mixed table row identity/bytes differ')
                table_rows.append(expected)
                result['table_row_index'].append(text_range(expected))
                offset += 1
            need(offset-1 == local_bounds[id][1], 'Mixed table leaves unindexed text')
            revised = references(table)
            revised['id'] = ident(tid)
            if table.get('axis_label_source_region'):
                revised['axis_label_source_region'] = context.identity(
                    table['axis_label_source_region'], context.regions)
            result['tables'].append(revised)
        need(table_cells == original.get('table_cell_index', []) and
             table_rows == original.get('table_row_index', []), 'Mixed table order differs')
        for join in original.get('prose_joins', []):
            rr = [r for r in regional if r['block_id'] == join['block_id']]
            pairs = [(x, y) for x, y in zip(rr, rr[1:]) if
                     x['region_id'] == join['from_region'] and y['region_id'] == join['to_region']]
            need(len(pairs) == 1 and
                 value(pairs[0][0], context.article).endswith(join['ending']) and
                 value(pairs[0][1], context.article).startswith(join['continuation']),
                 'Mixed native prose join differs from source fragments')
            result['prose_joins'].append(references(join))
        for link in original.get('caption_links', []):
            figure = next((r for r in source['figures'] if r['id'] == link['figure_id']), None)
            caption = next((r for r in source['blocks'] if r['id'] == link['caption_block_id']), None)
            need(figure is not None and caption is not None and caption['kind'] == 'caption' and
                 figure['caption'] == caption['text'] and link['figure_region_id'] in figure['region_ids'] and
                 link['caption_region_id'] in caption['region_ids'], 'Mixed caption association differs')
            result['caption_links'].append(references(link))
        sequence = original.get('figure_sequence', [])
        need([r.get('figure_id') for r in sequence] ==
             [r['id'] for r in source['content_order'] if r['type'] == 'figure'],
             'Mixed figure order differs')
        for key in ('figure_sequence', 'image_preservation', 'source_anomalies'):
            result[key].extend(references(row) for row in original.get(key, []))
        need({r.get('region_id') for r in original.get('image_preservation', [])} ==
             {r for figure in source['figures'] for r in figure['region_ids']},
             'Mixed image preservation must cover every figure region')
        project_listings(context, result, listing, references)
    assets = {r['region_id']: r['asset'] for r in package['region_assets']}
    for block in package['blocks']:
        a, z = bounds[block['id']]
        result['text_index'].append(dict(block_id=block['id'], region_ids=block['region_ids'],
            scans=[assets[r] for r in block['region_ids']], download='article.txt',
            **{START: a, END: z}))
    for row in result['records']:
        if 'block_ids' in row:
            row['block_ids'] = [positions[id][0] for id in row['block_ids']]
    result['blocks'] = package['blocks']
    validate_package(package)
    return package, result


def project_listings(context, result, combined, references):
    original, source = context.correction, context.source
    code = {b['id']: b for b in source['blocks'] if b['kind'] == 'code'}
    groups, membership = {}, {}
    for group in original.get('listing_groups', []):
        id = group.get('listing_id')
        need(isinstance(id, str) and id not in groups and group.get('execute_verified') is False,
             'Mixed listing group identity or execution status differs')
        groups[id] = group
        for block in group['block_ids']:
            need(block in code and block not in membership, 'Mixed listing block membership differs')
            membership[block] = id
    need(set(membership) == set(code), 'Mixed groups must cover all code blocks')
    bounds, expected, cursor = {}, [], 0
    for item in source['content_order']:
        id = item['id']
        if item['type'] != 'block' or id not in code:
            continue
        start = cursor
        for ordinal, line in enumerate(code[id]['text'].splitlines(keepends=True), 1):
            end = cursor+len(line.encode())
            need(line.endswith('\n'), 'Mixed physical row must end with LF')
            expected.append((id, ordinal, cursor, end, line))
            cursor = end
        bounds[id] = start, cursor

    def listing_range(row, *, blank=False):
        text = value(row, context.listing, blank=blank)
        id = row.get('block_id')
        need(row.get('download') == 'listing.txt' and id in bounds and
             bounds[id][0] <= row[START] <= row[END] <= bounds[id][1],
             'Mixed listing span leaves code block')
        if row.get('region_id') is not None:
            need(row['region_id'] in code[id]['region_ids'] and
                 row.get('scan') == context.assets.get(row['region_id']),
                 'Mixed listing scan differs from named region')
        revised = references(row)
        revised.update(source_range={START: row[START], END: row[END]},
                       **{START: context.offset+row[START], END: context.offset+row[END]})
        need(value(revised, combined, blank=blank) == text, 'Projected mixed listing bytes differ')
        return revised

    supplied = original.get('listing_index', [])
    need(len(supplied) == len(code) and {r['block_id'] for r in supplied} == set(code),
         'Mixed listing index must cover every code block')
    for row in supplied:
        need((row[START], row[END]) == bounds[row['block_id']], 'Mixed block listing range differs')
        regions = code[row['block_id']]['region_ids']
        need(row.get('region_ids') == regions and
             row.get('scans') == [context.assets[r] for r in regions],
             'Mixed listing block region/scans differ')
        result['listing_index'].append(listing_range(row))
    physical, by_id, aligned, counts = original.get('listing_line_index', []), {}, [], Counter()
    need(len(physical) == len(expected), 'Mixed physical row coverage differs')
    for source_ordinal, (row, (id, ordinal, a, z, line)) in enumerate(zip(physical, expected), 1):
        need(row.get('block_id') == id and row.get('listing_id') == membership[id] and
             type(row.get('physical_line')) is int and
             type(row.get('article_physical_line')) is int and
             row.get('physical_line') == ordinal and (row[START], row[END]) == (a, z) and
             row.get('article_physical_line') == source_ordinal and
             row.get('text') == line[:-1] and row.get('tokens') == line.split() and
             isinstance(row.get('line_id'), str) and row['line_id'] not in by_id,
             'Mixed physical row identity/text differs')
        need(row.get('source_bytes') == 'unverified' and row.get('execution_verified') is False,
             'Mixed physical source-byte/execution status differs')
        part = dict(region_id=row['region_id'], scan=row['scan'], **{START: a, END: z})
        need(row.get('segments') == [part], 'Mixed physical row region span differs')
        column = groups[membership[id]].get('printed_number_column')
        number, kind = row.get('printed_line'), row.get('row_kind')
        need(row.get('printed_line_visible') is (number is not None), 'Mixed number visibility differs')
        if column == 2:
            need(type(column) is int, 'Mixed number column must be integer')
            cols = line[:-1].split('\t')
            need(len(cols) == 5 and row.get('columns') == cols, 'Mixed five source columns differ')
            need(not cols[0] or re.fullmatch(r'[0-9A-F]{4}:', cols[0]), 'Mixed address spelling differs')
            need(not cols[1] or re.fullmatch(r'[0-9A-F]{2}(?: [0-9A-F]{2})*', cols[1]),
                 'Mixed machine-byte spelling differs')
            if kind == 'numbered':
                need(type(number) is int and cols[2] == str(number), 'Mixed printed column number differs')
            elif kind == 'wrapped-continuation':
                need(number is None and cols[0] and cols[1] and not any(cols[2:]),
                     'Mixed byte continuation must retain only its address and bytes')
            else:
                need(kind == 'unnumbered' and number is None and not any(cols[:3]),
                     'Mixed source header has an inferred address or number')
            aligned.append(row)
        elif kind == 'numbered':
            need(column == 0 and type(column) is int and type(number) is int and
                 line.startswith(str(number)+' '), 'Mixed text number differs from source')
        else:
            need(column is None or column == 0 and type(column) is int, 'Mixed number column differs')
            need(kind in ('unnumbered', 'wrapped-continuation') and number is None,
                 'Mixed unnumbered row carries an inferred number')
        counts[membership[id]] += 1
        by_id[row['line_id']] = row
    units, seen, numbered = original.get('assembly_instruction_index', []), [], []
    for unit in units:
        parts = unit.get('source_parts', [])
        need(parts and all(id in by_id for id in parts), 'Mixed logical unit has missing physical rows')
        rr = [by_id[id] for id in parts]
        need(rr[0]['assembly_row_kind'] == unit.get('unit_kind') and
             all(r['assembly_row_kind'] in ('comment-wrap', 'machine-byte-wrap', 'basic-text-wrap')
                 for r in rr[1:]) and
             all(r['assembly_unit_id'] == unit.get('unit_id') and
                 r['listing_id'] == unit.get('listing_id') and
                 r['block_id'] == unit.get('block_id') for r in rr),
             'Mixed logical unit membership differs')
        need((unit[START], unit[END]) == (rr[0][START], rr[-1][END]) and
             all(x[END] == y[START] for x, y in zip(rr, rr[1:])) and
             unit.get('segments') == [r['segments'][0] for r in rr] and
             value(unit, context.listing) == unit.get('text') and
             unit.get('source_bytes') == 'unverified' and unit.get('execution_verified') is False,
             'Mixed logical unit coverage or byte status differs')
        if unit.get('printed_line') is not None:
            need(rr[0]['row_kind'] == 'numbered' and rr[0]['printed_line'] == unit['printed_line'] and
                 rr[0].get('logical_line_id') == unit['unit_id'] and all(
                     r['row_kind'] == 'wrapped-continuation' and
                     r.get('logical_line_id') == unit['unit_id'] and
                     r.get('continues_printed_line') == unit['printed_line'] for r in rr[1:]),
                 'Mixed numbered unit continuation differs')
            numbered.append(unit)
        else:
            need(all(r['row_kind'] == 'unnumbered' for r in rr),
                 'Mixed plain unit hides a printed number')
        seen.extend(parts)
    need(seen == [r['line_id'] for r in physical] and
         len({u['unit_id'] for u in units}) == len(units), 'Mixed units must partition all physical rows')
    logical = original.get('logical_listing_line_index', [])
    need(len(logical) == len(numbered), 'Mixed numbered logical coverage differs')
    for row, unit in zip(logical, numbered):
        need(row.get('line_id') == unit['unit_id'] and row.get('occurrence') == 1 and
             all(row.get(k) == unit.get(k) for k in ('listing_id', 'block_id', 'printed_line',
                                                   START, END, 'source_parts', 'segments')),
             'Mixed numbered logical source parts differ')
    for group in groups.values():
        uu = [u for u in units if u['listing_id'] == group['listing_id']]
        need(all(type(group.get(k)) is int for k in
                 ('physical_lines', 'assembly_logical_units', 'numbered_entries', 'instruction_units')) and
             group.get('physical_lines') == counts[group['listing_id']] and
             group.get('assembly_logical_units') == len(uu) and
             group.get('numbered_entries') == sum(u['printed_line'] is not None for u in uu) and
             group.get('instruction_units') == sum(u['unit_kind'] == 'instruction' for u in uu),
             'Mixed listing group counts differ')
        result['listing_groups'].append(references(group))
    for key, rows in (('listing_line_index', physical), ('assembly_instruction_index', units),
                      ('logical_listing_line_index', logical)):
        for row in rows:
            revised = listing_range(row)
            revised['segments'] = [listing_range(dict(p, block_id=row['block_id'], download='listing.txt'))
                                   for p in row['segments']]
            if key == 'listing_line_index':
                revised['source_article_physical_line'] = row['article_physical_line']
                revised['article_physical_line'] = len(result[key])+1
            result[key].append(revised)
    regional = original.get('regional_listing_index', [])
    for id, (a, z) in bounds.items():
        rr = [r for r in regional if r['block_id'] == id]
        need(rr and rr[0][START] == a and rr[-1][END] == z and
             [r['region_id'] for r in rr] == code[id]['region_ids'] and
             all(x[END] == y[START] for x, y in zip(rr, rr[1:])),
             'Mixed regional listing must partition its block')
        for row in rr:
            pp = [r for r in physical if r['block_id'] == id and r['region_id'] == row['region_id']]
            need(pp and (row[START], row[END]) == (pp[0][START], pp[-1][END]) and
                 value(row, context.listing) == row.get('transcription_excerpt'),
                 'Mixed regional listing differs from physical rows')
    need({r['block_id'] for r in regional} == set(code), 'Mixed regional listing has unknown block')
    result['regional_listing_index'].extend(listing_range(r) for r in regional)
    cells = original.get('assembly_column_index', [])
    need(len(cells) == len(aligned)*5, 'Mixed source column coverage differs')
    machine_expected, i = [], 0
    for row in aligned:
        offset = row[START]
        for column, text in enumerate(row['columns'], 1):
            end, cell = offset+len(text.encode()), cells[i]
            need(all(cell.get(k) == v for k, v in dict(block_id=row['block_id'],
                listing_id=row['listing_id'], region_id=row['region_id'], scan=row['scan'],
                physical_line=row['physical_line'], printed_line=row['printed_line'], column=column,
                column_name=('address', 'machine_bytes', 'printed_number', 'source', 'comment')[column-1],
                text=text, blank=text == '', utf8_byte_start=offset, utf8_byte_end_exclusive=end).items()),
                'Mixed source column identity or bytes differ')
            result['assembly_column_index'].append(listing_range(cell, blank=True))
            if column == 2:
                for match in re.finditer(r'\b[0-9A-F]{2}\b', text):
                    a = offset+len(text[:match.start()].encode())
                    machine_expected.append((row, a, a+2, match[0]))
            offset, i = end+(column < 5), i+1
        need(offset == row[END]-1, 'Mixed source columns leave unindexed text')
    machine = original.get('machine_byte_index', [])
    need(len(machine) == len(machine_expected), 'Mixed machine-byte coverage differs')
    for row, (parent, a, z, literal) in zip(machine, machine_expected):
        need(all(row.get(k) == v for k, v in dict(block_id=parent['block_id'],
            listing_id=parent['listing_id'], region_id=parent['region_id'], scan=parent['scan'],
            physical_line=parent['physical_line'], printed_line=parent['printed_line'],
            literal=literal, utf8_byte_start=a, utf8_byte_end_exclusive=z,
            source_encoded_bytes='unverified', execution_verified=False).items()),
            'Mixed machine-byte source span or verification status differs')
        result['machine_byte_index'].append(listing_range(row))
    definitions = []
    for row in physical:
        match = re.search(r'DFB\s+((?:\$[0-9A-F]{2})(?:\s*,\s*\$[0-9A-F]{2})*)', row['text'])
        if match:
            a = row[START]+len(row['text'][:match.start(1)].encode())
            definitions.append((row, a, a+len(match[1].encode()), match[1]))
    supplied = original.get('data_definition_index', [])
    need(len(supplied) == len(definitions), 'Mixed DFB source coverage differs')
    for row, (parent, a, z, text) in zip(supplied, definitions):
        need(all(row.get(k) == v for k, v in dict(block_id=parent['block_id'],
            listing_id=parent['listing_id'], region_id=parent['region_id'], scan=parent['scan'],
            physical_line=parent['physical_line'], printed_line=parent['printed_line'],
            transcription_excerpt=text, literal_values=re.findall(r'\$[0-9A-F]{2}', text),
            utf8_byte_start=a, utf8_byte_end_exclusive=z, source_encoded_bytes='unverified',
            execution_verified=False).items()), 'Mixed DFB values/span or verification status differs')
        result['data_definition_index'].append(listing_range(row))
    for row in original.get('listing_source_uncertainties', []):
        need(value(row, context.listing) == row.get('transcription_excerpt'),
             'Mixed listing uncertainty excerpt differs')
        result['listing_source_uncertainties'].append(listing_range(row))
