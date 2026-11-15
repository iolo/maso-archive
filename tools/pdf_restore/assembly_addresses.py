"""Explicit joins of printed monitor addresses, without interpreting instructions.

Addresses remain source strings and logical units remain distinct. Printed byte
fields only establish the boundary increment; they never certify machine code.
"""
from collections import Counter
import re


def need(condition, message):
    if not condition:
        raise ValueError(message)


def address(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9A-F]{4}', value) is not None


def validate_join(link):
    for side, boundary in [('left', 'last_printed_address'), ('right', 'first_printed_address')]:
        part = link[side]
        need(isinstance(part, dict) and set(part) == {'segment', 'listing_id', boundary, 'association'}
             and isinstance(part['listing_id'], str) and bool(part['listing_id'])
             and type(part['association']) is int and part['association'] >= 0
             and address(part[boundary]), 'Invalid printed address boundary')
    spec = link['address_join']
    need(isinstance(spec, dict) and set(spec) ==
         {'left_source_unit_id', 'right_source_unit_id', 'left_folio', 'right_folio'}
         and all(isinstance(v, str) and bool(v) for v in spec.values()),
         'Address join requires explicit source units and folios')


def check_partition(group, physical, logical):
    units = [r for r in logical if r['listing_id'] == group['listing_id']]
    observed = [r.get('printed_address') for r in units]
    expected = [a for part in group['source_parts'] for a in part.get('observed_printed_addresses', [])]
    need(group.get('line_kind') == 'address-disassembly' and observed and observed == expected
         and all(address(a) for a in observed) and len(set(observed)) == len(observed)
         and all(r.get('printed_line') is None for r in units + physical),
         'Address listing differs from its declared original address inventory')
    need(Counter(p for u in units for p in u['physical_line_ids']) == Counter(r['line_id'] for r in physical),
         'Address units do not partition all physical source rows')
    rows = {r['line_id']: r for r in physical}
    for unit in units:
        need(len(unit['physical_line_ids']) == 1, 'Address unit must own one complete printed row')
        row = rows[unit['physical_line_ids'][0]]
        fields = row['fields']
        addr = [f['literal'] for f in fields if f['field'] == 'printed_address']
        need(row.get('printed_address') == unit['printed_address'] and addr == [unit['printed_address']]
             and unit['logical_text'] == row['text'].removesuffix('\n'),
             'Address identity differs from physical printed fields')
        byte_fields(row)
    group.update(observed_printed_addresses=observed, first_printed_address=observed[0],
                 last_printed_address=observed[-1], observed_printed_rows=[])


def byte_fields(row):
    fields = row['fields']
    tokens = [f for f in fields if re.fullmatch(r'printed_byte_[1-9][0-9]*', f['field'])]
    groups = [f['literal'] for f in fields if f['field'] == 'printed_byte_group']
    need(tokens and [f['field'] for f in tokens] == [f'printed_byte_{n}' for n in range(1, len(tokens)+1)]
         and all(re.fullmatch(r'[0-9A-F]{2}', f['literal']) for f in tokens)
         and len(groups) == 1 and groups[0].split() == [f['literal'] for f in tokens],
         'Printed byte group differs from individual source fields')
    return tokens


def check_boundary(link, a, b, out, inc):
    from .assembly_programs import folio
    spec = link['address_join']; left, right = link['left'], link['right']
    n, m = left['last_printed_address'], right['first_printed_address']
    aa = [r for r in a.correction['logical_listing_line_index'] if r['listing_id'] == left['listing_id']]
    bb = [r for r in b.correction['logical_listing_line_index'] if r['listing_id'] == right['listing_id']]
    need(aa and bb and aa[-1]['line_id'] == spec['left_source_unit_id']
         and bb[0]['line_id'] == spec['right_source_unit_id']
         and aa[-1].get('printed_address') == n and bb[0].get('printed_address') == m,
         'Printed address join differs from original endpoint units')
    for context, part, row, kind in [(a,left,out,'source-listing-continuation'),
                                     (b,right,inc,'source-listing-continuation-from')]:
        need(row.get('kind') == kind and row.get('listing_id') == part['listing_id'],
             'Address boundary differs from source association')
        group = context.groups[part['listing_id']]
        physical = [r for r in context.correction['listing_line_index'] if r['listing_id'] == part['listing_id']]
        check_partition(dict(group, source_parts=[group]), physical, context.correction['logical_listing_line_index'])
    need((out.get('source_unit_id'), out.get('segment_last_printed_address'),
          out.get('incoming_next_printed_address'), inc.get('source_unit_id'),
          inc.get('prior_source_unit_id'), inc.get('prior_last_printed_address'),
          inc.get('first_printed_address')) ==
         (spec['left_source_unit_id'], n, m, spec['right_source_unit_id'], spec['left_source_unit_id'], n, m)
         and inc.get('logical_unit_continued') is False and inc.get('whole_assembly_pending') is True
         and out.get('whole_article_complete') is False,
         'Address continuation source declarations differ')
    need(all(inc.get('prior_package_manifest', {}).get(k) == a.spec['manifest'][k] for k in ('sha256','bytes')),
         'Address continuation previous manifest differs')
    left_row = next(r for r in a.correction['listing_line_index'] if r['line_id'] == aa[-1]['physical_line_ids'][0])
    right_row = next(r for r in b.correction['listing_line_index'] if r['line_id'] == bb[0]['physical_line_ids'][0])
    need(str(folio(a,left_row['region_id'])) == spec['left_folio']
         and str(folio(b,right_row['region_id'])) == spec['right_folio'] == str(out.get('next_source_folio'))
         and [str(n) for n in out.get('remaining_source_folios',[])] == [str(p['printed_page']) for p in b.source['pages']],
         'Address continuation folios differ from observed source')
    need(int(n,16) + len(byte_fields(left_row)) == int(m,16),
         'Address boundary increment differs from printed byte fields')
