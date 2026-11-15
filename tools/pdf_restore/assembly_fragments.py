"""Explicitly evidenced joins of physical fragments of one BASIC source unit.

This opt-in extension preserves code bytes, including physical line breaks.
Logical characters and sparse numbers come only from reviewed source records.
"""
from collections import Counter
from copy import deepcopy

START, END = 'utf8_byte_start', 'utf8_byte_end_exclusive'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def validate_join(link):
    row = link['logical_join']
    need(isinstance(row, dict) and set(row) == {
        'left_source_unit_id', 'right_source_unit_id', 'separator', 'joined_reading'},
        'Invalid logical fragment join fields')
    need(all(isinstance(row[k], str) and row[k].strip() for k in
             ('left_source_unit_id', 'right_source_unit_id', 'joined_reading')) and
         row['separator'] == '', 'Logical fragment join requires exact source text and no inserted characters')
    need(link['left']['last_printed_row'] == link['right']['first_printed_row'],
         'Logical fragment join requires the same contextual printed number')


def observed_numbers(context, listing_id):
    """Validate sparse source numbers, without imposing or inventing a step size."""
    group = context.groups[listing_id]
    physical = [r for r in context.correction['listing_line_index'] if r['listing_id'] == listing_id]
    units = [r for r in context.correction['logical_listing_line_index'] if r['listing_id'] == listing_id]
    numbers = [r['printed_line'] for r in physical if r.get('printed_line') is not None]
    selected = [r['printed_line'] for r in units if r.get('printed_number_present', True)]
    need(group.get('line_kind') == 'basic-numbered' and numbers and
         all(type(n) is int for n in numbers) and numbers == sorted(set(numbers)) and
         numbers == group.get('observed_printed_rows') == selected,
         'Sparse program numbers differ from explicit physical and logical source rows')
    need(group.get('first_printed_row') == numbers[0] and group.get('last_printed_row') == numbers[-1],
         'Sparse program endpoints differ from source numbers')
    return physical


def boundary_reading(unit, physical):
    """Prove that logical character ranges select the actual physical fragments."""
    by_id = {r['line_id']: r for r in physical}
    parts = unit.get('source_parts', [])
    need([p['line_id'] for p in parts] == unit['physical_line_ids'] and parts,
         'Logical boundary parts differ from physical source rows')
    cursor = 0
    for part in parts:
        row = by_id.get(part['line_id'])
        need(row is not None, 'Logical boundary refers to an absent physical row')
        text = row['text'].removesuffix('\n')
        end = cursor + len(text)
        need((part['start_character'], part['end_character'], part['physical_start_byte']) ==
             (cursor, end, row['block_start_byte']), 'Logical boundary character coordinates differ')
        cursor = end
    reading = ''.join(by_id[id]['text'].removesuffix('\n') for id in unit['physical_line_ids'])
    need(reading == unit.get('logical_text'), 'Logical boundary reading differs from source fragments')
    return reading


def check_boundary(link, a, b, out, inc, aa, bb):
    join = link['logical_join']; n = link['left']['last_printed_row']
    left_id, right_id = join['left_source_unit_id'], join['right_source_unit_id']
    pa = observed_numbers(a, link['left']['listing_id'])
    pb = observed_numbers(b, link['right']['listing_id'])
    left, right = aa[-1], bb[0]
    need((left['line_id'], right['line_id']) == (left_id, right_id) and
         out.get('last_source_unit_id') == inc.get('previous_source_unit_id') == left_id and
         inc.get('first_source_unit_id') == right_id and
         out.get('last_printed_row') == inc.get('previous_last_printed_row') ==
         inc.get('first_contextual_printed_row') == n and
         out.get('logical_unit_complete') is False and
         inc.get('printed_number_present') is False and right.get('printed_number_present') is False and
         left.get('printed_number_present', True) is True,
         'Logical fragment boundary differs from source declarations')
    need(len(bb) > 1 and out.get('next_numbered_row') == inc.get('next_numbered_row') == bb[1]['printed_line'] and
         bb[1].get('printed_number_present', True) is True and bb[1]['printed_line'] > n and
         pa[-1]['line_id'] == left['physical_line_ids'][-1] and
         pb[0]['line_id'] == right['physical_line_ids'][0] and
         pb[0].get('printed_line') is None and pb[0].get('row_kind') == 'incoming-physical-continuation',
         'Logical fragments are not at the original source boundary')
    x, y = boundary_reading(left, pa), boundary_reading(right, pb)
    need(inc.get('previous_literal') == x and inc.get('literal') == out.get('following_physical_fragment') == y and
         join['joined_reading'] == inc.get('joined_reading') == x + y and
         isinstance(out.get('open_source_label'), str) and out['open_source_label'] and
         x.startswith(out['open_source_label']), 'Logical fragment literals differ from original source')
    target = a.name + ':' + left_id
    need(right_id not in b.logical_aliases, 'Repeated logical source fragment join')
    b.logical_aliases[right_id] = target


def finish_fragments(correction, records):
    listings = set()
    for record in records:
        if 'logical_join' not in record:
            continue
        listings.add(record['listing_id']); join = record['logical_join']
        candidates = [r for r in correction['logical_listing_line_index']
                      if r['listing_id'] == record['listing_id'] and
                      r['line_id'] == record['left']['segment'] + ':' + join['left_source_unit_id']]
        need(len(candidates) == 2, 'Logical fragment projection lacks its two source occurrences')
        left, right = candidates
        need((left['source_segment'], right['source_segment']) ==
             (record['left']['segment'], record['right']['segment']) and left[END] == right[START] and
             left['logical_text'] + right['logical_text'] == join['joined_reading'],
             'Projected logical fragments differ or are not contiguous')
        original = deepcopy(candidates)
        logical_offset = len(left['logical_text'])
        for part in right['source_parts']:
            part['start_character'] += logical_offset
            part['end_character'] += logical_offset
        left.update(logical_text=join['joined_reading'],logical_status='complete selected reading; source fragments joined',
                    printed_number_present=True,source_occurrences=original,logical_join_id=record['id'])
        for key in ('physical_line_ids', 'segments', 'source_parts'):
            left[key] += right[key]
        left[END] = right[END]
        correction['logical_listing_line_index'].remove(right)
    return listings


def check_partition(group, physical, all_units):
    units = [r for r in all_units if r['listing_id'] == group['listing_id']]
    numbers = [r['printed_line'] for r in units]
    expected = [n for part in group['source_parts'] for n in part['observed_printed_rows']]
    need(numbers == expected == sorted(set(numbers)), 'Unified sparse numbers differ from original source occurrences')
    owned = Counter(id for row in units for id in row['physical_line_ids'])
    need(owned == Counter(r['line_id'] for r in physical),
         'Logical units do not partition physical source rows, including visual blanks')
    group.update(first_printed_row=numbers[0],last_printed_row=numbers[-1],observed_printed_rows=numbers)
    group.pop('open_final_source_unit_id', None)
