"""Explicit two-fragment split statements over immutable native source scopes.

The only added byte is a declared physical row boundary. Original indexes and
files remain unchanged; derived complete units retain every source fragment.
"""
from copy import deepcopy
import re

S, E = 'utf8_byte_start', 'utf8_byte_end_exclusive'
MODE = 'scoped-split-programs-v1'


def require(value, message):
    if not value:
        raise ValueError(message)


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def validate_splits(specs, names):
    # A deliberately narrow contract: one complete program in two source scopes.
    require(isinstance(specs, list) and len(specs) == 1 and len(names) == 2,
            'Split assembly requires one program and exactly two source scopes')
    spec = specs[0]
    require(isinstance(spec, dict) and set(spec) == {
        'program_id', 'fragments', 'boundary', 'ending', 'source_extent_complete', 'evidence'},
        'Invalid split program fields')
    require(isinstance(spec['program_id'], str) and
            re.fullmatch(r'[a-z][a-z0-9-]*', spec['program_id']) and
            spec['source_extent_complete'] is True and nonblank(spec['evidence']),
            'Split program requires identity, complete source extent and review evidence')
    parts = spec['fragments']
    require(isinstance(parts, list) and len(parts) == 2, 'Split program requires two fragments')
    for i, part in enumerate(parts):
        require(isinstance(part, dict) and set(part) == {
            'segment', 'listing_id', 'first_source_unit_id', 'last_source_unit_id'} and
            part['segment'] == names[i] and all(nonblank(v) for v in part.values()),
            'Split fragments require exact ordered source identities')
    boundary = spec['boundary']
    require(isinstance(boundary, dict) and set(boundary) == {
        'printed_label', 'left_suffix', 'right_prefix', 'separator', 'intervening', 'evidence'} and
        isinstance(boundary['printed_label'], str) and
        re.fullmatch(r'[1-9][0-9]*', boundary['printed_label']) and
        boundary['separator'] == '\n' and
        all(nonblank(boundary[k]) for k in ('left_suffix', 'right_prefix', 'evidence')),
        'Split boundary requires exact source edges and one physical newline')
    require(isinstance(boundary['intervening'], list), 'Split intervening owners must be explicit')
    for item in boundary['intervening']:
        require(isinstance(item, dict) and set(item) == {'segment', 'type', 'id'} and
                item['segment'] in names and item['type'] == 'figure' and nonblank(item['id']),
                'Split program can cross only explicitly enumerated source figures')
    ending = spec['ending']
    require(isinstance(ending, dict) and set(ending) == {
        'source_unit_id', 'printed_label', 'literal', 'evidence'} and
        all(nonblank(v) for v in ending.values()), 'Split program requires its exact final source unit')


def unit_id(unit):
    return unit.get('line_id', unit.get('source_unit_id'))


def source_fragment(context, part):
    groups = context.correction.get('listing_groups', [])
    require(len(groups) == 1 and groups[0]['listing_id'] == part['listing_id'],
            'Split scope must contain exactly the declared independent listing')
    group = groups[0]
    rows = context.correction.get('listing_line_index', [])
    units = context.correction.get('logical_listing_line_index', [])
    require(rows and units and len(group['block_ids']) == 1 and
            group.get('complete_in_segment') is False and
            group.get('execute_verified') is False and group.get('original_encoded_bytes_verified') is False and
            group.get('physical_rows') == len(rows) and group.get('logical_units') == len(units) and
            group.get(S) == 0 and group.get(E) == len(context.listing) and
            all(r['listing_id'] == part['listing_id'] for r in rows + units),
            'Split fragment differs from source counts, extent or verification limits')
    require(unit_id(units[0]) == part['first_source_unit_id'] and
            unit_id(units[-1]) == part['last_source_unit_id'],
            'Split fragment truncates original source units')
    block = context.blocks[group['block_ids'][0]]
    require(block['kind'] == 'code' and block['text'].encode() == context.listing,
            'Split listing must preserve its complete independent code block')
    require('complete_program' not in group or group['complete_program'] is False,
            'Split fragment cannot already claim a complete program')
    return group, rows, units


def join_split_programs(specs, contexts, package, positions):
    """Merge only derived reading blocks and return an auditable complete program."""
    validate_splits(specs, [c.name for c in contexts])
    spec = specs[0]
    a, b = contexts
    ga, ra, ua = source_fragment(a, spec['fragments'][0])
    gb, rb, ub = source_fragment(b, spec['fragments'][1])
    left, right = ua[-1], ub[0]
    boundary = spec['boundary']
    label = boundary['printed_label']
    require(type(left.get('printed_line')) is int and str(left['printed_line']) == label and
            left.get('printed_label', label) == label and left.get('complete_in_segment') is False and
            right.get('printed_line') is None and right.get('printed_label') is None and
            right.get('continued_printed_label') == label and
            right.get('complete_in_segment') is False and right.get('external_predecessor_required') is True,
            'Split boundary must join the printed outgoing label to its unnumbered incoming fragment')
    require(all(u.get('complete_in_segment') is True and not u.get('external_predecessor_required')
                and type(u.get('printed_line')) is int for u in ua[:-1] + ub[1:]),
            'Split assembly contains another incomplete or unnumbered source unit')
    labels = [u['printed_line'] for u in ua + ub[1:]]
    require(labels == sorted(set(labels)), 'Split source labels must remain ordered and distinct')
    require(not a.listing.endswith(b'\n') and b.listing.endswith(b'\n') and
            a.listing.decode().endswith(boundary['left_suffix']) and
            b.listing.decode().startswith(boundary['right_prefix']) and
            not b.listing.startswith(b'\n'), 'Split source edges differ from the declared physical boundary')
    # Each source row remains a physical row. A missing boundary terminator is
    # supplied separately, never represented as another row or recovered byte.
    require(all(r['text'].endswith('\n') and r['text'].count('\n') == 1 for r in ra[:-1] + rb) and
            '\n' not in ra[-1]['text'], 'Split physical source row serialization is ambiguous')
    for context, rows, units in ((a, ra, ua), (b, rb, ub)):
        by_id = {r['line_id']: r for r in rows}
        require([id for u in units for id in u['physical_line_ids']] == list(by_id),
                'Split units do not preserve exact physical source row order')
        for u in units:
            reading = ''.join(by_id[id]['text'] for id in u['physical_line_ids'])
            require(u.get('physical_reading') == reading and
                    context.listing[u[S]:u[E]] == reading.encode(),
                    'Split logical reading differs from its original source rows')
    ending = spec['ending']
    require(unit_id(ub[-1]) == ending['source_unit_id'] and
            str(ub[-1]['printed_line']) == ending['printed_label'] and
            ub[-1]['physical_reading'] == ending['literal'],
            'Split program ending differs from the complete final original source unit')
    ids = [a.name + '-' + ga['block_ids'][0], b.name + '-' + gb['block_ids'][0]]
    blocks = {v['id']: v for v in package['blocks']}
    require(all(positions[id] == (id, 0) for id in ids), 'Split code block has already been joined')
    order = package['content_order']
    i, j = [order.index(dict(type='block', id=id)) for id in ids]
    actual = [dict(segment=c.name, **v) for c in contexts for v in c.package['content_order']]
    x, z = [actual.index(dict(segment=c.name, type='block', id=g['block_ids'][0]))
            for c, g in ((a, ga), (b, gb))]
    require(i < j and actual[x + 1:z] == boundary['intervening'] and
            order[i + 1:j] == [dict(type='figure', id=v['segment'] + '-' + v['id'])
                              for v in boundary['intervening']],
            'Split program hides or invents intervening source owners')
    start = len(a.listing)
    offset = start + 1
    first, second = [blocks[id] for id in ids]
    first['text'] += '\n' + second['text']
    for key in ('region_ids', 'correction_evidence', 'uncertainties'):
        first[key] = list(dict.fromkeys(first[key] + second[key]))
    package['blocks'].remove(second)
    del order[j]
    positions[ids[1]] = (ids[0], offset)
    b.listing_offset += 1
    listing = a.listing + b'\n' + b.listing
    fragments = []
    physical = []
    source_units = []
    for context, group, rows, units in ((a, ga, ra, ua), (b, gb, rb, ub)):
        fragments.append(dict(scope=context.name,
            source_ref=context.source_ref('/listing_groups/0'),
            listing_reference=context.reference('listing', group['listing_id']),
            start_byte=context.listing_offset, end_byte=context.listing_offset + len(context.listing),
            physical_rows=len(rows), logical_units=len(units)))
        for n, row in enumerate(rows):
            suffix = '\n' if context is a and n == len(rows) - 1 else ''
            physical.append(dict(source_ref=context.source_ref('/listing_line_index/' + str(n)),
                source_reference=context.reference('physical', row['line_id']),
                start_byte=context.listing_offset + row[S],
                end_byte=context.listing_offset + row[E] + len(suffix.encode()),
                source_reading=row['text'], serialization_suffix=suffix,
                layout_gap_search_separator=not row['text'].strip()))
        for n, unit in enumerate(units):
            source_units.append(dict(printed_label=str(unit['printed_line']) if unit['printed_line'] is not None else None,
                source_fragments=[dict(source_ref=context.source_ref('/logical_listing_line_index/' + str(n)),
                    source_reference=context.reference('logical', unit_id(unit)),
                    start_byte=context.listing_offset + unit[S], end_byte=context.listing_offset + unit[E])],
                start_byte=context.listing_offset + unit[S], end_byte=context.listing_offset + unit[E],
                physical_row_references=[context.reference('physical', id) for id in unit['physical_line_ids']],
                source_complete=True))
    merged = source_units[len(ua) - 1]
    incoming = source_units.pop(len(ua))
    merged['source_fragments'] += incoming['source_fragments']
    merged['end_byte'] = incoming['end_byte']
    merged['physical_row_references'] += incoming['physical_row_references']
    merged['boundary_separator'] = dict(start_byte=start, end_byte=offset, literal='\n')
    for unit in source_units:
        unit['physical_reading'] = listing[unit['start_byte']:unit['end_byte']].decode()
    result = dict(program_id=spec['program_id'], block_id=ids[0],
        source_fragments=fragments, boundary=dict(declaration=deepcopy(boundary),
            start_byte=start, end_byte=offset, literal='\n', kind='physical-row-boundary-serialization',
            original_encoded_bytes_verified=False),
        physical_rows=physical, logical_units=source_units,
        physical_row_count=len(physical), logical_unit_count=len(source_units),
        nonempty_ink_rows=sum(not v['layout_gap_search_separator'] for v in physical),
        layout_gap_search_rows=sum(v['layout_gap_search_separator'] for v in physical),
        physical_reading=listing.decode(), ending=deepcopy(ending), source_extent_complete=True,
        original_source_records_preserved=True, execute_verified=False,
        original_encoded_bytes_verified=False, evidence=spec['evidence'])
    require(''.join(v['source_reading'] + v['serialization_suffix'] for v in physical).encode() == listing and
            ''.join(v['physical_reading'] for v in source_units).encode() == listing,
            'Derived split program does not preserve complete physical and logical partitions')
    return listing, [result]
