"""Source-reviewed program continuity over immutable heterogeneous native groups.

The reading joins physical source rows, including damaged labels. It is separate
from the byte-preserved listing download and makes no executable-byte claim.
"""
from copy import deepcopy
import re

S, E = 'utf8_byte_start', 'utf8_byte_end_exclusive'


def require(value, message):
    if not value:
        raise ValueError(message)


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def validate_observations(specs, names):
    require(isinstance(specs, list) and specs, 'Observed programs require an explicit nonempty array')
    ids, used = set(), set()
    for spec in specs:
        require(isinstance(spec, dict) and set(spec) == {
            'program_id', 'fragments', 'boundaries', 'ending', 'source_extent_complete', 'evidence'},
            'Invalid observed program declaration')
        id = spec['program_id']
        require(isinstance(id, str) and re.fullmatch(r'[a-z][a-z0-9-]*', id) and id not in ids,
                'Invalid or duplicate observed program identity')
        ids.add(id)
        require(spec['source_extent_complete'] is True and nonblank(spec['evidence']),
                'Observed program requires reviewed complete source extent')
        fragments = spec['fragments']
        require(isinstance(fragments, list) and 2 <= len(fragments) <= len(names),
                'Observed continuation requires two or more source fragments')
        previous = None
        for part in fragments:
            require(isinstance(part, dict) and set(part) == {
                'segment', 'listing_id', 'first_source_unit_id', 'last_source_unit_id'} and
                part['segment'] in names and all(nonblank(v) for v in part.values()),
                'Observed fragment requires explicit listing and source unit identities')
            pos = names.index(part['segment'])
            require(previous is None or pos == previous + 1,
                    'Observed fragments must follow consecutive source scopes')
            previous = pos
            key = (part['segment'], part['listing_id'])
            require(key not in used, 'Reused observed source fragment')
            used.add(key)
        boundaries = spec['boundaries']
        require(isinstance(boundaries, list) and len(boundaries) == len(fragments) - 1,
                'Observed program requires every fragment boundary')
        for boundary in boundaries:
            require(isinstance(boundary, dict) and set(boundary) == {
                'left_printed_label', 'right_printed_label', 'separator',
                'source_unit_complete', 'intervening', 'evidence'} and
                boundary['separator'] in ('', '\n') and boundary['source_unit_complete'] is True and
                all(nonblank(boundary[k]) for k in ('left_printed_label', 'right_printed_label', 'evidence')),
                'Observed boundary requires literal complete source units and evidence')
            require(isinstance(boundary['intervening'], list), 'Observed intervening owners must be explicit')
            for item in boundary['intervening']:
                require(isinstance(item, dict) and set(item) == {'segment', 'type', 'id'} and
                        item['segment'] in names and item['type'] in ('block', 'figure') and nonblank(item['id']),
                        'Invalid observed intervening source owner')
        ending = spec['ending']
        require(isinstance(ending, dict) and set(ending) == {
            'source_unit_id', 'printed_label', 'source_unit_complete', 'evidence'} and
            ending['source_unit_complete'] is True and
            all(nonblank(ending[k]) for k in ('source_unit_id', 'printed_label', 'evidence')),
            'Observed program requires an explicit original ending')


def source_unit_id(unit):
    return unit.get('line_id', unit.get('source_unit_id'))


def printed_label(unit):
    label = unit.get('printed_label')
    return label if label is not None else str(unit['printed_line']) if type(unit.get('printed_line')) is int else None


def project_observations(specs, contexts, listing):
    names = [c.name for c in contexts]
    validate_observations(specs, names)
    by_name = {c.name: c for c in contexts}
    order = [dict(segment=c.name, **item) for c in contexts for item in c.package['content_order']]
    results = []
    for spec in specs:
        fragments, sources = [], []
        for part in spec['fragments']:
            c = by_name[part['segment']]
            groups = c.correction.get('listing_groups', [])
            matches = [(i, v) for i, v in enumerate(groups) if v['listing_id'] == part['listing_id']]
            require(len(matches) == 1, 'Observed fragment has no unique original listing group')
            index, group = matches[0]
            id = part['listing_id']
            rows = [r for r in c.correction.get('listing_line_index', []) if r['listing_id'] == id]
            units = [u for u in c.correction.get('logical_listing_line_index', []) if u['listing_id'] == id]
            require(rows and units and group.get('physical_rows') == len(rows) and
                    group.get('logical_units') == len(units) and
                    group.get('execute_verified') is False and group.get('original_encoded_bytes_verified') is False,
                    'Observed fragment differs from original source counts or verification limits')
            require(source_unit_id(units[0]) == part['first_source_unit_id'] and
                    source_unit_id(units[-1]) == part['last_source_unit_id'],
                    'Observed fragment truncates its original logical source units')
            ids = [r['line_id'] for r in rows]
            require(len(set(ids)) == len(ids) and
                    [r for u in units for r in u['physical_line_ids']] == ids and
                    all(r['block_id'] in group['block_ids'] for r in rows + units),
                    'Observed source rows require exact ordered unit and block ownership')
            by_id = {r['line_id']: r for r in rows}
            start, end = rows[0][S], rows[-1][E]
            cursor = start
            for row in rows:
                require(row[S] == cursor and row[E] == cursor + len(row['text'].encode()),
                        'Observed physical source byte partition is not contiguous')
                cursor = row[E]
            data = ''.join(r['text'] for r in rows).encode()
            require(c.listing[start:end] == data and
                    listing[start+c.listing_offset:end+c.listing_offset] == data and
                    (group.get(S), group.get(E)) == (start, end),
                    'Observed program fragment differs from original listing bytes')
            require(all(c.blocks[b]['kind'] == 'code' for b in group['block_ids']) and
                    ''.join(c.blocks[b]['text'] for b in group['block_ids']).encode() == data,
                    'Observed fragment must own its complete original code blocks')
            damaged = []
            for unit in units:
                members = [by_id[id] for id in unit['physical_line_ids']]
                require(unit.get('physical_reading') == ''.join(r['text'] for r in members) and
                        (unit[S], unit[E]) == (members[0][S], members[-1][E]) and
                        unit['printed_line'] == members[0]['printed_line'],
                        'Observed unit differs from its original physical source members')
                if unit['printed_line'] is None:
                    require(nonblank(unit.get('printed_label')) and unit.get('line_number_certified') is False and
                            isinstance(unit.get('line_label_candidates'), list) and unit['line_label_candidates'],
                            'Damaged source label requires its literal uncertainty')
                    damaged.append(dict(source_unit_reference=c.reference('logical', source_unit_id(unit)),
                        printed_label=unit['printed_label'], candidates=deepcopy(unit['line_label_candidates']),
                        line_number_certified=False))
            fragment = dict(scope=c.name, listing_id=id,
                listing_reference=c.reference('listing', id), source_ref=c.source_ref(f'/listing_groups/{index}'),
                block_ids=[c.reference('block', b) for b in group['block_ids']],
                physical_line_references=[c.reference('physical', r['line_id']) for r in rows],
                logical_unit_references=[c.reference('logical', source_unit_id(u)) for u in units],
                source_download='listing.txt', source_start_byte=start+c.listing_offset,
                source_end_byte=end+c.listing_offset, source_reading=data.decode(),
                physical_rows=len(rows), logical_units=len(units),
                first_printed_label=printed_label(units[0]), last_printed_label=printed_label(units[-1]),
                damaged_source_units=damaged)
            fragments.append(fragment);sources.append((c,group,rows,units))
        boundaries, reading, offset = [], '', 0
        for i, fragment in enumerate(fragments):
            if i:
                boundary = spec['boundaries'][i-1];left = fragments[i-1]
                ca, ga, ra, ua = sources[i-1];cb, gb, rb, ub = sources[i]
                require(type(ua[-1]['printed_line']) is int and type(ub[0]['printed_line']) is int and
                        left['last_printed_label'] == boundary['left_printed_label'] and
                        fragment['first_printed_label'] == boundary['right_printed_label'],
                        'Observed fragment boundary differs from literal numbered source units')
                require(left['source_end_byte'] == fragment['source_start_byte'],
                        'Observed fragments have intervening independent code bytes')
                expected_separator = '' if left['source_reading'].endswith('\n') else '\n'
                require(boundary['separator'] == expected_separator,
                        'Observed separator must preserve exactly one physical row boundary')
                a = order.index(dict(segment=ca.name, type='block', id=ga['block_ids'][-1]))
                z = order.index(dict(segment=cb.name, type='block', id=gb['block_ids'][0]))
                require(a < z and order[a+1:z] == boundary['intervening'],
                        'Observed program hides or invents intervening source owners')
                for item in boundary['intervening']:
                    if item['type'] == 'block':
                        require(by_name[item['segment']].blocks[item['id']]['kind'] != 'code',
                                'Observed program cannot skip another source listing')
                separator = boundary['separator']
                boundaries.append(dict(declaration=deepcopy(boundary), reading_start_byte=offset,
                    reading_end_byte=offset+len(separator.encode()),
                    left_unit_reference=ca.reference('logical', source_unit_id(ua[-1])),
                    right_unit_reference=cb.reference('logical', source_unit_id(ub[0])),
                    intervening_references=[by_name[v['segment']].reference(v['type'], v['id'])
                                            for v in boundary['intervening']]))
                reading += separator;offset += len(separator.encode())
            fragment['reading_start_byte'] = offset
            reading += fragment['source_reading'];offset += len(fragment['source_reading'].encode())
            fragment['reading_end_byte'] = offset
        ending = spec['ending'];c, group, rows, units = sources[-1]
        require(ending['source_unit_id'] == source_unit_id(units[-1]) and
                ending['printed_label'] == printed_label(units[-1]) and type(units[-1]['printed_line']) is int,
                'Observed ending differs from the final original source unit')
        results.append(dict(program_id=spec['program_id'],source_fragments=fragments,
            boundaries=boundaries,ending=dict(declaration=deepcopy(ending),
                source_unit_reference=c.reference('logical', source_unit_id(units[-1]))),
            physical_reading=reading,physical_rows=sum(v['physical_rows'] for v in fragments),
            logical_units=sum(v['logical_units'] for v in fragments),
            source_extent_complete=True,original_listing_download_unchanged=True,
            execute_verified=False,original_encoded_bytes_verified=False,evidence=spec['evidence']))
    return results
