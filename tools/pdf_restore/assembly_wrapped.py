"""Project reviewed physical wraps without joining or repairing printed code.

Numbered listings may coexist with explicitly unnumbered examples. Wraps may
cross code panels; cross-segment carried fragments use the historical namespaced mode.
Source logical indexes are checked against physical rows before offsets change.
"""
from collections import Counter
import re

from .assembly_indexes import END, START, span


def project_listing(context, corrections, listing):
    original = context.correction
    code = {b['id']: b for b in context.source['blocks'] if b['kind'] == 'code'}
    groups = original.get('listing_groups', [])
    membership, group_ids = {}, set()
    for group in groups:
        id = group.get('listing_id')
        if (not isinstance(id, str) or not id or id in group_ids or not group.get('block_ids') or
                group.get('execute_verified') is not False):
            raise ValueError('Wrapped listing requires explicit unverified groups')
        group_ids.add(id)
        for block in group['block_ids']:
            if block not in code or block in membership:
                raise ValueError('Wrapped listing group has unknown or repeated blocks')
            membership[block] = id
        corrections['source_listing_groups'].append(context.references(group) |
                                                     {'source_segment': context.name})
    if set(membership) != set(code):
        raise ValueError('Wrapped listing groups must cover all code blocks')

    bounds, expected_rows, cursor = {}, [], 0
    for item in context.source['content_order']:
        if item['type'] != 'block' or item['id'] not in code:
            continue
        id = item['id']
        start = cursor
        for ordinal, line in enumerate(code[id]['text'].splitlines(keepends=True), 1):
            end = cursor + len(line.encode())
            if not line.endswith('\n'):
                raise ValueError('Wrapped physical rows must end with a newline')
            expected_rows.append((id, ordinal, cursor, end, line))
            cursor = end
        bounds[id] = start, cursor

    def project_range(row, block=True):
        value = span(row, context.listing)
        if row.get('download') != 'listing.txt':
            raise ValueError('Wrapped listing range names another download')
        if block:
            id = row.get('block_id')
            if id not in bounds or not bounds[id][0] <= row[START] < row[END] <= bounds[id][1]:
                raise ValueError('Wrapped listing range leaves its code block')
            if row.get('region_id') is not None and row['region_id'] not in code[id]['region_ids']:
                raise ValueError('Wrapped listing range names another region')
        revised = context.listing_range(row)
        if span(revised, listing) != value:
            raise ValueError('Projected wrapped listing bytes differ')
        return revised

    indexes = original.get('listing_index', [])
    if len(indexes) != len(code) or {r['block_id'] for r in indexes} != set(code):
        raise ValueError('Wrapped listing index must cover every code block')
    for row in indexes:
        if (row[START], row[END]) != bounds[row['block_id']]:
            raise ValueError('Wrapped listing block range differs')
        corrections['listing_index'].append(project_range(row))

    rows = original.get('listing_line_index', [])
    if len(rows) != len(expected_rows):
        raise ValueError('Wrapped physical row count differs')
    local_counts, global_counts = Counter(), Counter()
    for row in corrections['logical_listing_line_index']:
        global_counts[row['listing_id'], row['printed_line']] += 1
    logicals, physical, seen, current = [], [], set(), None
    for row, (id, ordinal, start, end, text) in zip(rows, expected_rows, strict=True):
        if (row.get('block_id') != id or row.get('listing_id') != membership[id] or
                row.get('physical_line') != ordinal or (row[START], row[END]) != (start, end) or
                not isinstance(row.get('line_id'), str) or not row['line_id'] or row['line_id'] in seen or
                row.get('region_id') not in code[id]['region_ids'] or
                any(k in row for k in ('prior_segment', 'continuation'))):
            raise ValueError('Wrapped row differs from physical source identity')
        seen.add(row['line_id'])
        part = {k: row[k] for k in ('region_id', 'scan', START, END)}
        if row.get('segments') != [part]:
            raise ValueError('Wrapped physical row must retain its exact scan span')
        project_range(row)  # Validate region/scan/download even before constructing indexes.
        number = row.get('printed_line')
        if row.get('row_kind') == 'unnumbered':
            if ('printed_line' not in row or number is not None or row.get('printed_line_visible') is not False or
                    any(k in row for k in ('logical_line_id', 'continues_printed_line'))):
                raise ValueError('Unnumbered row cannot infer a numbered logical line')
            physical.append(row)
            current = None  # A subsequent wrap cannot jump across this independent row.
            continue
        if row.get('row_kind') == 'numbered':
            number_token = re.match(r'([0-9]+)(?=\s|;)', text)
            if (type(number) is not int or row.get('printed_line_visible') is not True or
                    not number_token or int(number_token[1]) != number):
                raise ValueError('Wrapped printed number differs from source text')
            key = row['listing_id'], number
            local_counts[key] += 1
            current = dict(listing_id=key[0], printed_line=number, occurrence=local_counts[key],
                           line_id=row.get('logical_line_id'), download='listing.txt',
                           **{START: start, END: end}, source_parts=[], segments=[])
            if not isinstance(current['line_id'], str) or not current['line_id']:
                raise ValueError('Wrapped logical row requires a source identity')
            logicals.append(current)
        elif (row.get('row_kind') != 'wrapped-continuation' or number is not None or
              row.get('printed_line_visible') is not False or current is None or
              row.get('continues_printed_line') != current['printed_line'] or
              row['listing_id'] != current['listing_id'] or current[END] != start):
            raise ValueError('Wrapped continuation has no adjacent numbered row')
        if row.get('logical_line_id') != current['line_id']:
            raise ValueError('Wrapped physical row names another logical line')
        current[END] = end
        current['source_parts'].append(row['line_id'])
        current['segments'].append(part)
        physical.append(row)

    supplied = original.get('logical_listing_line_index', [])
    if (len(supplied) != len(logicals) or
            len({r['line_id'] for r in logicals}) != len(logicals)):
        raise ValueError('Wrapped logical line coverage or identity differs')
    for row, expected in zip(supplied, logicals, strict=True):
        if any(row.get(k) != v for k, v in expected.items()):
            raise ValueError('Wrapped logical index differs from physical source rows')

    line_ids = {r['line_id']: f'{context.name}:physical:{i}' for i, r in enumerate(physical, 1)}
    logical_ids = {}
    for row in logicals:
        key = row['listing_id'], row['printed_line']
        global_counts[key] += 1
        id = f'{key[0]}:{key[1]}:{global_counts[key]}'
        logical_ids[row['line_id']] = id
        revised = project_range(row, block=False)
        revised.update(line_id=id, occurrence=global_counts[key], source_line_id=row['line_id'],
                       source_occurrence=row['occurrence'],
                       source_parts=[line_ids[p] for p in row['source_parts']],
                       segments=[context.listing_range(p) for p in row['segments']])
        corrections['logical_listing_line_index'].append(revised)
    for row in physical:
        revised = project_range(row)
        revised.update(line_id=line_ids[row['line_id']], source_line_id=row['line_id'],
                       segments=[context.listing_range(p) for p in row['segments']])
        if row.get('row_kind') != 'unnumbered':
            revised['logical_line_id'] = logical_ids[row['logical_line_id']]
        corrections['listing_line_index'].append(revised)
    for row in original.get('listing_anomalies', []):
        if span(row, context.listing) != row.get('transcription_excerpt'):
            raise ValueError('Wrapped listing review excerpt differs from source bytes')
        corrections['listing_anomalies'].append(project_range(row))

    by_id = {r['line_id']: r for r in logicals}
    for row in original.get('data_statements', []):
        logical = by_id.get(row.get('line_id'))
        if (logical is None or any(row.get(k) != logical[k] for k in (START, END, 'printed_line')) or
                row.get('physical_rows') != len(logical['source_parts']) or
                row.get('physical_newlines_removed_for_index_only') is not True or
                row.get('original_machine_bytes_verified') is not False or
                row.get('execution_verified') is not False or
                row.get('scan') not in [p['scan'] for p in logical['segments']]):
            raise ValueError('DATA index differs from its unverified logical source line')
        text = span(row, context.listing).replace('\n', '')
        match = re.fullmatch(r'\d+ DATA\s+(-?\d+(?:\s*,\s*-?\d+)*)\s*', text, flags=re.IGNORECASE)
        values = [int(v) for v in match[1].split(',')] if match else None
        if (values is None or row.get('literal_values') != values or row.get('value_count') != len(values) or
                any(type(v) is not int for v in row['literal_values'])):
            raise ValueError('DATA numeric index differs from literal printed values')
        revised = project_range(row, block=False)
        revised.update(line_id=logical_ids[row['line_id']], source_line_id=row['line_id'])
        corrections['data_statements'].append(revised)

    # Original per-segment completeness declarations stay in source_listing_groups.
    # Aggregation reports included blocks and rows without inferring executability.
    for group in groups:
        id = group['listing_id']
        target = next((g for g in corrections['listing_groups'] if g['listing_id'] == id), None)
        if target is None:
            target = dict(listing_id=id, block_ids=[], source_segments=[], execute_verified=False,
                          coverage='all-declared-segment-blocks', numbered_entries=0, physical_rows=0)
            corrections['listing_groups'].append(target)
        target['block_ids'].extend(context.identity(b, context.blocks) for b in group['block_ids'])
        if context.name not in target['source_segments']:
            target['source_segments'].append(context.name)
        target['numbered_entries'] += sum(r['listing_id'] == id for r in logicals)
        target['physical_rows'] += sum(r['listing_id'] == id for r in physical)
        unnumbered = sum(r['listing_id'] == id and r['row_kind'] == 'unnumbered' for r in physical)
        if unnumbered:
            target['unnumbered_rows'] = target.get('unnumbered_rows', 0) + unnumbered
