"""Explicit complete-unit program continuations over unchanged native scopes."""
from copy import deepcopy

S, E = 'utf8_byte_start', 'utf8_byte_end_exclusive'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def validate_links(links, names):
    require(isinstance(links, list), 'Scoped program links must be an array')
    for link in links:
        require(isinstance(link, dict) and set(link) ==
                {'left', 'right', 'source_unit_complete', 'evidence'}, 'Invalid scoped program link')
        require(link['source_unit_complete'] is True and isinstance(link['evidence'], str) and
                bool(link['evidence'].strip()), 'Program link requires complete source units and evidence')
        for side, edge in [('left', 'last_printed_line'), ('right', 'first_printed_line')]:
            part = link[side]
            require(isinstance(part, dict) and set(part) == {'segment', 'listing_id', edge} and
                    part['segment'] in names and isinstance(part['listing_id'], str) and
                    bool(part['listing_id']) and type(part[edge]) is int,
                    'Program link requires explicit source listing and printed boundary')
        require(names.index(link['right']['segment']) == names.index(link['left']['segment']) + 1,
                'Program link must cross consecutive segments')


def project_programs(links, contexts, listing):
    """Bind all source groups exactly once; links resolve only declared boundaries.

    This opt-in contract covers complete numbered units, not a split statement.
    Original groups, logical units and physical rows remain in native_indexes.
    """
    names = [c.name for c in contexts]
    validate_links(links, names)
    fragments, owners = {}, {}
    for c in contexts:
        for i, group in enumerate(c.correction.get('listing_groups', [])):
            id = group['listing_id']
            rows = [r for r in c.correction.get('listing_line_index', []) if r['listing_id'] == id]
            units = [r for r in c.correction.get('logical_listing_line_index', []) if r['listing_id'] == id]
            require(rows and units and group.get('complete_in_segment') is True and
                    type(group.get('complete_program')) is bool and
                    group.get('physical_rows') == len(rows) and group.get('logical_units') == len(units),
                    'Program fragment differs from complete native source rows')
            require(all(type(u['printed_line']) is int for u in units),
                    'Scoped program links require numbered source units')
            require(group.get('execute_verified') is False and
                    group.get('original_encoded_bytes_verified') is False,
                    'Program assembly cannot establish execution or encoded bytes')
            require(all(r['block_id'] in group['block_ids'] for r in rows + units) and
                    {r['line_id'] for r in rows} ==
                    {id for u in units for id in u['physical_line_ids']},
                    'Program fragment has wrong-owner physical or logical rows')
            start, end = rows[0][S], rows[-1][E]
            data = ''.join(r['text'] for r in rows).encode()
            require(c.listing[start:end] == data and
                    listing[start + c.listing_offset:end + c.listing_offset] == data,
                    'Program fragment differs from contiguous source download bytes')
            key = (c.name, id)
            fragments[key] = dict(scope=c.name, listing_id=id,
                listing_reference=c.reference('listing', id),
                source_ref=c.source_ref(f'/listing_groups/{i}'),
                block_ids=[c.reference('block', b) for b in group['block_ids']],
                physical_line_ids=[c.reference('physical', r['line_id']) for r in rows],
                logical_unit_ids=[c.reference('logical', u.get('line_id', u.get('source_unit_id'))) for u in units],
                download='listing.txt', start_byte=start + c.listing_offset,
                end_byte=end + c.listing_offset, physical_rows=len(rows), logical_units=len(units),
                first_printed_line=units[0]['printed_line'], last_printed_line=units[-1]['printed_line'])
            owners[key] = (c, group)
    outgoing, incoming = {}, {}
    for link in links:
        left, right = link['left'], link['right']
        a, b = (left['segment'], left['listing_id']), (right['segment'], right['listing_id'])
        require(a in fragments and b in fragments and a not in outgoing and b not in incoming,
                'Unknown or reused scoped program fragment')
        ca, ga = owners[a]; cb, gb = owners[b]
        fa, fb = fragments[a], fragments[b]
        first, last = right['first_printed_line'], left['last_printed_line']
        require(ga['complete_program'] is False and gb['complete_program'] is False and
                ga['source_version'] == gb['source_version'] and ga['listing_id'] == gb['listing_id'] and
                fa['last_printed_line'] == last and fb['first_printed_line'] == first and first > last and
                fa['end_byte'] == fb['start_byte'],
                'Program link differs from source version, units or adjacent code bytes')
        old = ca.correction.get('segment', {}).get('outgoing_program')
        new = cb.correction.get('segment', {}).get('incoming_program')
        require(isinstance(old, dict) and isinstance(new, dict) and
                set(old) == {'listing_id', 'last_printed_line', 'next_folio',
                             'next_printed_line', 'source_unit_complete'} and
                set(new) == {'listing_id', 'previous_folio', 'last_printed_line',
                             'next_printed_line', 'source_unit_complete'} and
                old['listing_id'] == left['listing_id'] and new['listing_id'] == right['listing_id'] and
                old['last_printed_line'] == new['last_printed_line'] == last and
                old['next_printed_line'] == new['next_printed_line'] == first and
                old['source_unit_complete'] is True and new['source_unit_complete'] is True and
                str(old['next_folio']) == str(cb.package['pages'][0]['printed_page']) and
                str(new['previous_folio']) == str(ca.package['pages'][-1]['printed_page']),
                'Program link differs from original incoming/outgoing declarations')
        outgoing[a] = (b, deepcopy(link)); incoming[b] = a
    for c in contexts:
        segment = c.correction.get('segment', {})
        for field, bound in [('outgoing_program', outgoing), ('incoming_program', incoming)]:
            if field in segment:
                require((c.name, segment[field]['listing_id']) in bound,
                        'Unresolved declared scoped program continuation')
    programs, used = [], set()
    for key, fragment in fragments.items():
        if key in incoming:
            continue
        chain, boundaries, cursor = [], [], key
        while True:
            require(cursor not in used, 'Reused or cyclic scoped program')
            used.add(cursor); chain.append(deepcopy(fragments[cursor]))
            if cursor not in outgoing:
                break
            cursor, boundary = outgoing[cursor]; boundaries.append(boundary)
        _, first_group = owners[key]
        final_context, _ = owners[cursor]
        if boundaries:
            final = final_context.correction.get('segment', {}).get('final_program')
            require(final == dict(listing_id=cursor[1], last_printed_line=chain[-1]['last_printed_line'],
                                  source_unit_complete=True), 'Joined program lacks an explicit source ending')
        else:
            require(first_group['complete_program'] is True, 'Incomplete native program lacks a continuation')
        programs.append(dict(program_id=key[0] + '-' + key[1],
            source_version=first_group['source_version'], source_fragments=chain,
            block_ids=[b for f in chain for b in f['block_ids']],
            physical_rows=sum(f['physical_rows'] for f in chain),
            logical_units=sum(f['logical_units'] for f in chain), continuations=boundaries,
            complete_program=True, execute_verified=False, original_encoded_bytes_verified=False))
    require(used == set(fragments), 'Unowned scoped native program fragment')
    return programs
