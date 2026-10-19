"""Opt-in source-literal indexes for wrapped BASIC; never infer encoded bytes.

The existing wrapped projector proves physical/logical rows first. This extension
checks regional/table coverage and every quote/DATA occurrence before rebasing it.
Quoted blanks, physical wraps, printed checksums and unknown metadata stay literal.
"""
from copy import deepcopy
import re

from .assembly_indexes import START, END


def need(condition, message):
    if not condition:
        raise ValueError(message)


def value(row, data, blank=False):
    a, z = row.get(START), row.get(END)
    need(type(a) is int and type(z) is int and 0 <= a <= z <= len(data) and
         (blank or a < z), 'BASIC source range leaves download')
    try:
        return data[a:z].decode('utf-8')
    except UnicodeDecodeError as error:
        raise ValueError('BASIC source range splits UTF-8') from error


def data_tokens(text):
    """Return observed field character spans, with physical newlines untouched."""
    match = re.match(r'^\d+ DATA ', text)
    if not match:
        return None
    a, quoted, spans = match.end(), False, []
    for i, ch in enumerate(text[a:], a):
        if ch == '"':
            quoted = not quoted
        elif ch == ',' and not quoted:
            spans.append((a, i))
            a = i + 1
    need(not quoted, 'BASIC DATA has an unmatched source quote')
    spans.append((a, len(text)))
    result = []
    for a, z in spans:
        while a < z and text[a].isspace():
            a += 1
        while z > a and text[z-1].isspace():
            z -= 1
        need(a < z, 'BASIC DATA has an unindexed empty source field')
        result.append((a, z, text[a:z]))
    return result


def project_basic_fields(context, result, listing, text_range, references):
    original, source = context.correction, context.source
    need(original.get('basic_source_fields_format') == 'v1', 'Unknown BASIC source field format')
    keys = ('regional_text_index', 'text_review_notes', 'tables', 'table_cell_index',
            'table_row_index', 'caption_links', 'image_preservation', 'inline_example_index',
            'regional_listing_index', 'listing_source_uncertainties', 'quoted_source_index',
            'graphic_string_index', 'music_string_index', 'basic_data_statements',
            'basic_data_field_index', 'basic_machine_data_rows', 'basic_machine_data_field_index',
            'basic_hex_data_rows', 'basic_numeric_data_rows', 'basic_panel_data_rows',
            'basic_music_data_rows')
    for key in keys:
        result.setdefault(key, [])
    result['basic_source_fields_format'] = 'v1'
    blocks = {b['id']: b for b in source['blocks']}
    regional = original.get('regional_text_index', [])
    need({r.get('block_id') for r in regional} == set(blocks), 'BASIC regional block coverage differs')
    for id, (a, z) in context.ranges.items():
        rr = [r for r in regional if r['block_id'] == id]
        need(rr and rr[0][START] == a and rr[-1][END] == z and
             [r.get('region_id') for r in rr] == blocks[id]['region_ids'] and
             all(x[END] == y[START] for x, y in zip(rr, rr[1:])),
             'BASIC regional spans must partition each source block')

    def article_range(row, blank=False):
        text = value(row, context.article, blank)
        id = row.get('block_id')
        need(row.get('download') == 'article.txt' and id in blocks,
             'BASIC article range names another block/download')
        a, z = context.ranges[id]
        need(a <= row[START] <= row[END] <= z, 'BASIC article range leaves source block')
        if row.get('region_id') is not None:
            rid = row['region_id']
            need(row.get('scan') == context.assets.get(rid) and any(
                 r['block_id'] == id and r['region_id'] == rid and
                 r[START] <= row[START] <= row[END] <= r[END] for r in regional),
                 'BASIC article scan or regional occurrence differs')
        if 'region_ids' in row:
            need(row['region_ids'] == blocks[id]['region_ids'] and
                 row.get('scans') == [context.assets[r] for r in row['region_ids']],
                 'BASIC whole-block source scans differ')
        whole = text_range(dict(block_id=id, download='article.txt',
            **{START: a, END: z}), whole=True)
        delta = whole[START] - a
        revised = references(row)
        revised.update(source_range={START: row[START], END: row[END]},
                       **{START: row[START]+delta, END: row[END]+delta})
        if row.get('table_id') is not None:
            revised['table_id'] = context.name+'-'+row['table_id']
        need(value(row, context.article, blank) == text, 'BASIC article source text differs')
        return revised

    for row in regional:
        need(value(row, context.article) == row.get('transcription_excerpt'),
             'BASIC regional excerpt differs')
        result['regional_text_index'].append(article_range(row))
    for key in ('text_review_notes', 'inline_example_index'):
        for row in original.get(key, []):
            need(value(row, context.article) == row.get('transcription_excerpt'),
                 'BASIC text review excerpt differs')
            result[key].append(article_range(row))
    # Existing wrapped projection copies these references; normalize only opted-in rows.
    result['prose_joins'] = [r for r in result['prose_joins'] if r.get('source_segment') != context.name]
    for row in original.get('prose_joins', []):
        rr = [r for r in regional if r['block_id'] == row['block_id']]
        pairs = [(a,z) for a,z in zip(rr,rr[1:]) if
                 a['region_id'] == row['from_region'] and z['region_id'] == row['to_region']]
        need(len(pairs) == 1 and pairs[0][0]['transcription_excerpt'].endswith(row['ending']) and
             pairs[0][1]['transcription_excerpt'].startswith(row['continuation']),
             'BASIC prose continuation differs from source')
        result['prose_joins'].append(references(row) | {k: context.identity(row[k], context.regions)
                                                       for k in ('from_region','to_region')})
    cells, table_rows = original.get('table_cell_index', []), original.get('table_row_index', [])
    used_cells, used_rows = [], []
    for table in original.get('tables', []):
        rows = ([table['header']] if table.get('header') else []) + table['rows']
        need(rows and all(isinstance(r,list) and r for r in rows) and
             blocks[table['block_id']]['text'] == '\n'.join('\t'.join(r) for r in rows),
             'BASIC table cells differ from source block')
        cursor = context.ranges[table['block_id']][0]
        selected_cells = [r for r in cells if r['table_id'] == table['id']]
        selected_rows = [r for r in table_rows if r['table_id'] == table['id']]
        need(len(selected_cells) == sum(map(len,rows)) and len(selected_rows) == len(rows),
             'BASIC table index coverage differs')
        ci = 0
        for ordinal, row in enumerate(rows):
            nr = ordinal if table.get('header') else ordinal+1
            start = cursor
            for nc, text in enumerate(row,1):
                r = selected_cells[ci]
                ci += 1
                end = cursor+len(text.encode())
                need(r.get('row') == nr and r.get('column') == nc and
                     r.get('block_id') == table['block_id'] and
                     r.get('region_id') == table['region_id'] and
                     (r[START],r[END]) == (cursor,end) and r.get('text') == text and
                     r.get('blank') is (text == '') and
                     r.get('header') is (bool(table.get('header')) and ordinal == 0),
                     'BASIC table cell occurrence or blank differs')
                result['table_cell_index'].append(article_range(r, blank=True))
                cursor = end+(nc<len(row))
            r = selected_rows[ordinal]
            need(r.get('row') == nr and r.get('block_id') == table['block_id'] and
                 r.get('region_id') == table['region_id'] and (r[START],r[END]) == (start,cursor) and
                 value(r,context.article) == '\t'.join(row), 'BASIC table row occurrence differs')
            result['table_row_index'].append(article_range(r));cursor += 1
        used_cells.extend(selected_cells);used_rows.extend(selected_rows)
        result['tables'].append(references(table) | {'id': context.name+'-'+table['id']})
    need(used_cells == cells and used_rows == table_rows, 'BASIC table index has extra/reordered fields')
    for row in original.get('caption_links', []):
        fig = next((f for f in source['figures'] if f['id'] == row.get('figure_id')), None)
        caption = blocks.get(row.get('caption_block_id'))
        need(fig is not None and caption is not None and caption['kind'] == 'caption' and
             fig['caption'] == caption['text'] and row['figure_region_id'] in fig['region_ids'] and
             row['caption_region_id'] in caption['region_ids'], 'BASIC figure caption differs')
        result['caption_links'].append(references(row) | {k: context.identity(row[k],context.regions)
             for k in ('figure_region_id','caption_region_id')})
    image_rows = original.get('image_preservation', [])
    image_regions = {r for f in source['figures'] for r in f['region_ids']}
    need(len(image_rows) == len(image_regions) and
         {r.get('region_id') for r in image_rows} == image_regions, 'BASIC image coverage differs')
    need([r.get('figure_id') for r in original.get('figure_sequence', [])] ==
         [r['id'] for r in source['content_order'] if r['type'] == 'figure'],
         'BASIC figure reading order differs')
    for row in image_rows:
        need(row.get('scan') == context.assets.get(row['region_id']), 'BASIC image scan differs')
        result['image_preservation'].append(references(row))

    physical = original['listing_line_index'];units = original['logical_listing_line_index']
    logical_map = {r['source_line_id']:r['line_id'] for r in result['logical_listing_line_index']
                   if r['source_segment'] == context.name}
    physical_map = {r['source_line_id']:r['line_id'] for r in result['listing_line_index']
                    if r['source_segment'] == context.name}
    code_bounds = {r['block_id']:(r[START],r[END]) for r in original['listing_index']}
    def listing_range(row, unit=None):
        text = value(row, context.listing)
        id = row.get('block_id')
        need(row.get('download') == 'listing.txt' and id in code_bounds and
             code_bounds[id][0] <= row[START] < row[END] <= code_bounds[id][1],
             'BASIC listing field leaves its source block')
        if unit is not None:
            need(row.get('printed_line') == unit['printed_line'] and
                 unit[START] <= row[START] < row[END] <= unit[END] and
                 row.get('logical_line_id',unit['line_id']) == unit['line_id'],
                 'BASIC listing field names another logical occurrence')
        if row.get('region_id') is not None:
            covered = any(
                 r['region_id'] == row['region_id'] and r[START] <= row[START] and
                 row[END] <= r[END] for r in original['regional_listing_index'])
            if 'scans' in row and unit is not None:
                scans = []
                for part in unit['segments']:
                    if part['scan'] not in scans:
                        scans.append(part['scan'])
                covered = ((row[START],row[END]) == (unit[START],unit[END]) and
                           row['region_id'] == unit['segments'][0]['region_id'] and
                           row['scans'] == scans)
            need(row.get('scan') == context.assets.get(row['region_id']) and covered,
                 'BASIC listing field scan/region differs')
        if 'scans' in row:
            need(unit is not None and row.get('region_id') is not None,
                 'BASIC multi-scan field requires a logical source row')
            revised = context.listing_range({k:v for k,v in row.items() if k != 'scans'})
            revised['scans'] = [dict(s,path=context.prefix+'/'+s['path']) for s in row['scans']]
        else:
            revised = context.listing_range(row)
        if 'logical_line_id' in row:revised['logical_line_id'] = logical_map[row['logical_line_id']]
        if 'source_parts' in row:revised['source_parts'] = [physical_map[x] for x in row['source_parts']]
        if 'segments' in row:
            need(unit is not None, 'BASIC segmented field requires a logical source row')
            expected = [dict(region_id=s['region_id'],scan=s['scan'],
                **{START:max(row[START],s[START]),END:min(row[END],s[END])}) for s in unit['segments']
                if max(row[START],s[START]) < min(row[END],s[END])]
            need(row['segments'] == expected, 'BASIC field source segments differ')
            revised['segments'] = [context.listing_range(s) for s in expected]
        need(value(revised,listing) == text, 'BASIC projected listing field bytes differ')
        return revised
    for row in original.get('regional_listing_index', []):
        rr = [r for r in physical if r['block_id'] == row['block_id'] and r['region_id'] == row['region_id']]
        need(rr and (row[START],row[END]) == (rr[0][START],rr[-1][END]) and
             value(row,context.listing) == row.get('transcription_excerpt'),
             'BASIC regional listing occurrence differs')
        result['regional_listing_index'].append(listing_range(row))
    regional_listing = original.get('regional_listing_index', [])
    for id,(a,z) in code_bounds.items():
        rr = [r for r in regional_listing if r['block_id'] == id]
        need(rr and rr[0][START] == a and rr[-1][END] == z and
             [r['region_id'] for r in rr] == blocks[id]['region_ids'] and
             all(x[END] == y[START] for x,y in zip(rr,rr[1:])),
             'BASIC regional listing must partition its code block')
    by_id = {u['line_id']:u for u in units}
    for ordinal,row in enumerate(result['listing_line_index'],1):
        if row['source_segment'] != context.name:continue
        local = next(r for r in physical if r['line_id'] == row['source_line_id'])
        need(local.get('source_bytes') == 'unverified' and local.get('execution_verified') is False and
             value(local,context.listing) == local.get('text','')+'\n' and
             local.get('tokens') == local['text'].split(), 'BASIC physical byte/execution status differs')
        row.update(source_article_physical_line=local.get('article_physical_line'),article_physical_line=ordinal)
    for row in result['logical_listing_line_index']:
        if row['source_segment'] != context.name:continue
        u = by_id[row['source_line_id']]
        need(u.get('source_bytes') == 'unverified' and u.get('execution_verified') is False and
             value(u,context.listing) == u.get('text'), 'BASIC logical byte/execution status differs')
        for key in ('block_id','text','source_bytes','execution_verified'):
            row[key] = context.identity(u[key],context.blocks) if key == 'block_id' else deepcopy(u[key])
    for row in original.get('listing_source_uncertainties', []):
        u = by_id.get(row.get('logical_line_id'));need(u is not None and
             (row[START],row[END]) == (u[START],u[END]) and
             value(row,context.listing) == row.get('transcription_excerpt'),
             'BASIC source uncertainty differs from logical row')
        result['listing_source_uncertainties'].append(listing_range(row,u))

    quotes = original.get('quoted_source_index', []);expected_quotes=[]
    for u in units:
        text = u['text'];indices=[i for i,ch in enumerate(text) if ch == '"']
        for k in range(0,len(indices),2):
            a=indices[k];closed=k+1<len(indices);z=indices[k+1]+1 if closed else len(text.rstrip('\n'))
            expected_quotes.append((u,k//2+1,u[START]+len(text[:a].encode()),
                u[START]+len(text[:z].encode()),text[a:z],closed))
    need(len(quotes) == len(expected_quotes), 'BASIC quoted source coverage differs')
    for row,(u,ordinal,a,z,text,closed) in zip(quotes,expected_quotes):
        need(row.get('literal_ordinal') == ordinal and (row[START],row[END]) == (a,z) and
             row.get('transcription_excerpt') == text and row.get('closing_quote_visible') is closed and
             row.get('contents') == (text[1:-1] if closed else text[1:]) and
             row.get('source_bytes') == 'unverified' and row.get('execution_verified') is False and
             row.get('kind') in ('graphic-source-string','music-source-string','printed-source-string'),
             'BASIC quoted source occurrence/content/status differs')
        result['quoted_source_index'].append(listing_range(row,u))
    for key,kind in [('graphic_string_index','graphic-source-string'),('music_string_index','music-source-string')]:
        selected=[r for r in quotes if r['kind'] == kind]
        need(original.get(key,[]) == selected, 'BASIC quoted subtype coverage differs')
        result[key].extend(listing_range(r,by_id[r['logical_line_id']]) for r in selected)
    statements = original.get('basic_data_statements', []);fields=original.get('basic_data_field_index', [])
    expected_data=[(u,data_tokens(u['text'])) for u in units if re.match(r'^\d+ DATA ',u['text'])]
    need(len(statements) == len(expected_data), 'BASIC DATA statement coverage differs')
    consumed=[]
    for row,(u,tokens) in zip(statements,expected_data):
        need((row[START],row[END]) == (u[START],u[END]) and row.get('transcription_excerpt') == u['text'] and
             row.get('literal_values') == [v for _,_,v in tokens] and row.get('value_count') == len(tokens),
             'BASIC DATA source values or occurrence differ')
        category=row.get('category');ff=[r for r in fields if r.get('logical_line_id') == u['line_id']]
        need(len(ff) == len(tokens), 'BASIC DATA field coverage differs')
        for ordinal,(field,(a,z,text)) in enumerate(zip(ff,tokens),1):
            lo,hi=u[START]+len(u['text'][:a].encode()),u[START]+len(u['text'][:z].encode())
            kind=('hex-literal' if category in ('machine','sprite','character','bright') and
                  not(category == 'machine' and ordinal == 9) else
                  'printed-decimal-checksum' if category == 'machine' else
                  'quoted-panel-string' if category == 'panel' else
                  'unquoted-music-source' if category == 'music' else 'printed-decimal-literal')
            need(category in ('machine','sprite','character','bright','move','color','round','panel','music') and
                 field.get('category') == category and field.get('field') == ordinal and
                 field.get('kind') == kind and field.get('text') == text and
                 (field[START],field[END]) == (lo,hi), 'BASIC DATA field literal/occurrence differs')
            if kind == 'hex-literal':need(re.fullmatch('[0-9A-F]{2}',text), 'BASIC DATA hex source spelling differs')
            if kind in ('printed-decimal-checksum','printed-decimal-literal'):
                need(re.fullmatch(r'-?\s*\d+',text), 'BASIC DATA decimal source spelling differs')
            need(field.get('source_bytes') == 'unverified' and field.get('checksum_verified') is False and
                 field.get('execution_verified') is False, 'BASIC DATA field falsely claims verification')
            result['basic_data_field_index'].append(listing_range(field,u))
        need((category != 'machine' or len(tokens) == 9) and
             (category not in ('sprite','character','bright') or len(tokens) == 8) and
             (category != 'panel' or len(tokens) == 5 and all(v.startswith('"') and v.endswith('"') for _,_,v in tokens)) and
             (category != 'music' or len(tokens) == 1 and '"' not in tokens[0][2]),
             'BASIC DATA declared source category shape differs')
        need(row.get('source_bytes') == 'unverified' and row.get('checksum_verified') is False and
             row.get('execution_verified') is False, 'BASIC DATA row falsely claims verification')
        consumed.extend(ff);result['basic_data_statements'].append(listing_range(row,u))
    need(consumed == fields, 'BASIC DATA field order has extra or reassigned values')
    for key,categories in [('basic_hex_data_rows',('sprite','character','bright')),
                           ('basic_numeric_data_rows',('move','color','round')),
                           ('basic_panel_data_rows',('panel',)),('basic_music_data_rows',('music',))]:
        selected=[r for r in statements if r['category'] in categories]
        need(original.get(key,[]) == selected, 'BASIC DATA category index differs')
        result[key].extend(listing_range(r,by_id[r['logical_line_id']]) for r in selected)
    machine=[r for r in statements if r['category'] == 'machine']
    supplied=original.get('basic_machine_data_rows',[])
    need(len(supplied) == len(machine), 'BASIC machine DATA row coverage differs')
    for row,parent in zip(supplied,machine):
        need(row.get('printed_line') == parent['printed_line'] and (row[START],row[END]) == (parent[START],parent[END]) and
             row.get('hex_literals') == parent['literal_values'][:8] and
             row.get('printed_checksum') == parent['literal_values'][8] and
             row.get('checksum_verified') is False and row.get('source_bytes') == 'unverified' and
             row.get('execution_verified') is False, 'BASIC printed checksum/hex source fields differ')
        result['basic_machine_data_rows'].append(listing_range(row,by_id[parent['logical_line_id']]))
    machine_fields=[r for r in fields if r['category'] == 'machine'];supplied=original.get('basic_machine_data_field_index',[])
    need(len(supplied) == len(machine_fields), 'BASIC machine DATA field coverage differs')
    for row,parent in zip(supplied,machine_fields):
        need(all(row.get(k) == parent[k] for k in ('printed_line','field','kind','text',START,END)) and
             row.get('checksum_verified') is False and row.get('source_bytes') == 'unverified' and
             row.get('execution_verified') is False, 'BASIC machine DATA field differs from source occurrence')
        result['basic_machine_data_field_index'].append(listing_range(row,by_id[parent['logical_line_id']]))
