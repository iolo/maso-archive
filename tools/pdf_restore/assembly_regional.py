"""Opt-in prose assembly with reviewed interruptions and source-region indexes."""
from collections import defaultdict
import re

from .assembly_indexes import START, END, span

FIELDS = ('regional_text_index', 'controller_table_index', 'unicode_glyphs',
          'signal_notation_index', 'reference_index')


def validate_intervening(items):
    if not isinstance(items, list):
        raise ValueError('Intervening content must be explicitly listed')
    seen = set()
    for row in items:
        if (not isinstance(row, dict) or set(row) != {'segment', 'type', 'id'} or
                row['type'] not in ('figure', 'block') or
                any(not isinstance(v, str) or not v for v in row.values())):
            raise ValueError('Invalid intervening content identity')
        key = (row['segment'], row['type'], row['id'])
        if key in seen:
            raise ValueError('Duplicate intervening content')
        seen.add(key)


def check_intervening(items, actual, contexts, *, allow_wrapped_listings=False):
    expected = [dict(type=r['type'], id=r['segment']+'-'+r['id']) for r in items]
    if expected != actual:
        raise ValueError('Intervening content differs from reviewed order')
    sources = {c.name: c for c in contexts}
    for position, row in enumerate(items):
        context = sources.get(row['segment'])
        if context is None:
            raise ValueError('Unknown intervening segment')
        if row['type'] == 'figure':
            context.identity(row['id'], context.figures)
            continue
        blocks = {b['id']: b for b in context.source['blocks']}
        block = blocks.get(row['id'])
        if block is None:
            raise ValueError('Unknown intervening block')
        if block['kind'] == 'caption':
            continue
        if allow_wrapped_listings and block['kind'] in ('code', 'title'):
            # Listing projection subsequently checks every group, physical row
            # and byte range. Here require declared membership and, for a title,
            # its immediately following listing in both reviewed/source order.
            code = {b['id'] for b in blocks.values() if b['kind'] == 'code'}
            declared = {id for group in context.correction.get('listing_groups', [])
                        for id in group.get('block_ids', []) if id in code}
            if block['kind'] == 'code' and row['id'] in declared:
                continue
            if block['kind'] == 'title':
                order = context.source['content_order']
                index = order.index(dict(type='block', id=row['id']))
                following = order[index + 1:index + 2]
                reviewed = items[position + 1:position + 2]
                if (following and following[0]['type'] == 'block' and
                        following[0]['id'] in declared and
                        reviewed == [dict(segment=context.name, **following[0])]):
                    continue
            raise ValueError('Intervening listing requires declared code and an adjacent reviewed heading')
        table_rows = context.correction.get('controller_table_index', [])
        if (block['kind'] != 'prose' or not any(
                r.get('region_id') in block['region_ids'] for r in table_rows)):
            raise ValueError('Intervening prose requires a source-linked table index')


def project_regional(context, result, project_range):
    """Validate local spans before applying the joined block's global offsets."""
    original, source = context.correction, context.source
    blocks = {b['id']: b for b in source['blocks']}
    regions = {r['id']: r for r in source['regions']}
    regional = original.get('regional_text_index', [])
    expected = {r for b in blocks.values() for r in b['region_ids']}
    if (len(regional) != len(expected) or {r.get('region_id') for r in regional} != expected or
            set(original.get('regional_transcription', {})) != expected):
        raise ValueError('Regional index must cover each text region exactly once')
    local = {}
    intervals = defaultdict(list)
    for row in regional:
        id, block_id = row['region_id'], row.get('block_id')
        if block_id not in blocks or id not in blocks[block_id]['region_ids']:
            raise ValueError('Regional span belongs to another block')
        value = original['regional_transcription'][id]
        if span(row, context.article) != value:
            raise ValueError('Regional span differs from transcription')
        revised = project_range(dict(row, transcription_excerpt=value))
        result['regional_text_index'].append(revised)
        local[id] = row
        intervals[block_id].append((row[START], row[END]))
    for parts in intervals.values():
        ordered = sorted(parts)
        if any(a[1] > b[0] for a, b in zip(ordered, ordered[1:])):
            raise ValueError('Regional spans overlap')

    def linked(row, value):
        id = row.get('region_id')
        parent = local.get(id)
        if parent is None or not parent[START] <= row[START] < row[END] <= parent[END]:
            raise ValueError('Specialized span lies outside its source region')
        if row.get('block_id', parent['block_id']) != parent['block_id']:
            raise ValueError('Specialized span identifies another block')
        return project_range(dict(row, block_id=parent['block_id'], transcription_excerpt=value))

    glyphs = original.get('unicode_glyphs', [])
    for row in glyphs:
        if (not isinstance(row.get('glyph'), str) or not row['glyph'] or
                row.get('encoded_bytes') is not None or row.get('source_encoding_verified') is not False):
            raise ValueError('Unicode reading glyph requires unverified source bytes')
        result['unicode_glyphs'].append(linked(row, row['glyph']))
    signals = original.get('signal_notation_index', [])
    signal_keys = lambda rows: [(r.get('region_id'), r.get(START), r.get(END), r.get('glyph')) for r in rows]
    overlined = [r for r in glyphs if '\u0305' in r['glyph']]
    if signal_keys(signals) != signal_keys(overlined):
        raise ValueError('Signal notation index differs from overlined glyphs')
    for row in signals:
        if not re.fullmatch(r'(?:[A-Z0-9]\u0305)+', row['glyph']):
            raise ValueError('Signal notation must retain complete overlined letters or digits')
        result['signal_notation_index'].append(linked(row, row['glyph']))

    counts = defaultdict(int)
    for row in original.get('controller_table_index', []):
        table = row.get('table_id')
        context.identity(table, context.figures)
        counts[table] += 1
        if type(row.get('row')) is not int or row['row'] != counts[table]:
            raise ValueError('Table rows must retain consecutive source identities')
        cells = [row.get(k) for k in ('classification', 'purpose', 'series_8080', 'series_z80')]
        if (any(not isinstance(v, str) or not v for v in cells[:3]) or
                cells[3] is not None and (not isinstance(cells[3], str) or not cells[3]) or
                row.get('original_blank_cells_preserved') is not True):
            raise ValueError('Table cells require explicit text or original null')
        figure = next(f for f in source['figures'] if f['id'] == table)
        region = regions.get(row.get('region_id'))
        if region is None or not any(
                all(regions[id][k] == region[k] for k in ('pdf_index', 'bbox'))
                for id in figure['region_ids']):
            raise ValueError('Table text must reference the original figure area')
        revised = linked(row, ' | '.join(v or '' for v in cells))
        revised['table_id'] = context.identity(table, context.figures)
        result['controller_table_index'].append(revised)
    for number, row in enumerate(original.get('reference_index', []), 1):
        if type(row.get('number')) is not int or row['number'] != number or row.get('bibliographically_verified') is not False:
            raise ValueError('References require source order and unverified bibliography')
        result['reference_index'].append(linked(row, row.get('transcription_excerpt')))
