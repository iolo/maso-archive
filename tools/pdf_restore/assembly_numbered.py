"""Explicit joins between distinct, sparsely numbered BASIC source units.

The reviewed physical rows establish the observed sequence. Numeric gaps never
establish missing instructions, and physical wraps never add logical characters.
"""
from copy import deepcopy

from .assembly_fragments import boundary_reading, check_partition, need, observed_numbers
from .assemble import rebase


def reference(context, key, value):
    if value is None:
        return False, None
    if key in ('transcription_block_id', 'body_block_id'):
        return True, context.block(value)
    if key == 'transcription_region_id':
        return True, context.identity(value, context.regions)
    if key == 'read_loop_source_unit_id':
        need(value in {r['line_id'] for r in context.correction['logical_listing_line_index']},
             'Source DATA read loop names an absent unit')
        return True, context.name + ':' + value
    if key == 'data_group_source_unit_ids':
        need(all(v in {r['line_id'] for r in context.correction['logical_listing_line_index']} for v in value),
             'Source DATA group names an absent unit')
        return True, [context.name + ':' + v for v in value]
    return False, None


def validate_join(link):
    row = link['numbered_join']
    need(isinstance(row, dict) and set(row) == {
        'left_source_unit_id', 'right_source_unit_id', 'missing_rows_inferred'},
        'Invalid observed numbered join fields')
    need(all(isinstance(row[k], str) and row[k].strip() for k in
             ('left_source_unit_id', 'right_source_unit_id')) and
         row['missing_rows_inferred'] is False and
         link['left']['last_printed_row'] < link['right']['first_printed_row'],
         'Observed numbered join requires distinct increasing source numbers without inference')


def check_boundary(link, a, b, out, inc, aa, bb):
    join = link['numbered_join']
    need((aa[-1]['line_id'], bb[0]['line_id']) ==
         (join['left_source_unit_id'], join['right_source_unit_id']) and
         out.get('number_gap_inferred_missing_rows') is False and
         inc.get('number_gap_inferred_missing_rows') is False,
         'Observed numbered boundary differs from its source units or uncertainty')
    for context, part, units in ((a, link['left'], aa), (b, link['right'], bb)):
        physical = observed_numbers(context, part['listing_id'])
        group = dict(listing_id=part['listing_id'], source_parts=[context.groups[part['listing_id']]])
        check_partition(group, physical, units)
        need([id for unit in units for id in unit['physical_line_ids']] ==
             [row['line_id'] for row in physical],
             'Observed numbered units reorder physical source rows')
        by_id = {r['line_id']: r for r in physical}
        for unit in units:
            need(unit.get('printed_number_present', True) is True and
                 by_id[unit['physical_line_ids'][0]].get('printed_line') == unit['printed_line'] and
                 all(by_id[id].get('printed_line') is None for id in unit['physical_line_ids'][1:]),
                 'Observed numbered unit has a missing or duplicate printed number')
            boundary_reading(unit, physical)
            need(all(part['region_id'] == by_id[part['line_id']]['region_id']
                     for part in unit['source_parts']),
                 'Observed numbered source part names the wrong region')


def finish(correction, contexts, records):
    """Resolve source-owned prose references after the complete source is joined."""
    listings = {r['listing_id'] for r in records if 'numbered_join' in r}
    if not listings:
        return
    active = {(r['source_segment'], r['source_ref']['pointer']): r
              for r in correction['content_associations']}
    units = {r['line_id']: r for r in correction['logical_listing_line_index']}
    by_number = {(r['listing_id'], r['printed_line']): r for r in units.values()}
    by_name = {c.name: c for c in contexts}
    for listing in listings:
        endings = [r for r in correction['content_associations']
                   if r.get('listing_id') == listing and r['kind'] == 'source-listing-end']
        need(len(endings) == 1, 'Observed numbered program requires one declared source ending')
    linked = set()
    for context in contexts:
        for i, source in enumerate(context.correction['content_associations']):
            row = active[(context.name, f'/content_associations/{i}')]
            if source['kind'] == 'source-retrospective-entry':
                row['entry_id'] = context.name + ':' + source['entry_id']
                if source['parent_entry_id'] is not None:
                    need(any(r.get('entry_id') == source['parent_entry_id'] for r in
                             context.correction['content_associations']), 'Absent retrospective parent')
                    row['parent_entry_id'] = context.name + ':' + source['parent_entry_id']
            if row.get('listing_id') not in listings:
                continue
            if source['kind'] == 'source-explanation-unit-link':
                external = source['source_explanation']
                n = contexts.index(context)
                need(n > 0, 'External explanation lacks its preceding segment')
                prior = contexts[n-1]
                need(all(external['package']['manifest'].get(k) == prior.spec['manifest'][k]
                         for k in ('sha256', 'bytes')) and
                     all(external['corrections'].get(k) == prior.source['corrections'][0][k]
                         for k in ('sha256', 'bytes')), 'External explanation source pins differ')
                index = external['association_index']
                need(type(index) is int and 0 <= index < len(prior.correction['content_associations']),
                     'External explanation source occurrence is absent')
                original = prior.correction['content_associations'][index]
                target = active[(prior.name, f'/content_associations/{index}')]
                selected = units.get(row['source_unit_id'])
                need(original['kind'] == 'source-explanation-listing-reference' and
                     original['literal'] == external['literal'] and
                     original['printed_row'] == source['printed_row'] and selected is not None and
                     selected['printed_line'] == source['printed_row'] and
                     selected['listing_id'] == target['listing_id'] == row['listing_id'],
                     'External explanation differs from the printed prose or listing unit')
                key = prior.name, index
                need(key not in linked, 'Repeated external explanation occurrence')
                linked.add(key)
                row['source_explanation'] = dict(source_ref=deepcopy(target['source_ref']),
                    literal=external['literal'], association_index=index,
                    corrections=rebase(prior.source['corrections'][0], prior.prefix))
                target['resolution_source'] = deepcopy(row['source_ref'])
            # Preserve the external source declaration in immutable corrections,
            # and point the active relationship at the embedded source package.
            for key in ('source_prose_package', 'printed_report_package'):
                if key not in source:
                    continue
                n = contexts.index(context)
                need(n > 0 and all(source[key]['manifest'].get(k) == contexts[n-1].spec['manifest'][k]
                                   for k in ('sha256', 'bytes')), 'Related source package manifest differs')
                prior = contexts[n-1]
                row[key] = dict(path=prior.prefix,
                    manifest=rebase(dict(prior.spec['manifest'], path='manifest.json'), prior.prefix))
    for row in correction['content_associations']:
        if row.get('listing_id') not in listings:
            continue
        if row['kind'] == 'source-explanation-listing-reference':
            selected = by_number.get((row['listing_id'], row['printed_row']))
            if row.get('pending_source_folios'):
                available = {str(p['printed_page']) for c in contexts for p in c.source['pages']}
                need({str(n) for n in row['pending_source_folios']} <= available,
                     'Explanation still names unrestored source pages')
                if selected is not None:
                    need('resolution_source' in row, 'Pending explanation lacks its source-declared unit link')
                row.update(pending_source_folios=[], source_unit_id=selected['line_id'] if selected else None,
                    reference_without_selected_source_unit=selected is None,
                    reference_absent_from_complete_source=selected is None,
                    restoration_coverage='complete observed source; printed prose number retained')
        if row['kind'] == 'resolved-listing-continuation':
            available = {str(p['printed_page']) for c in contexts for p in c.source['pages']}
            need({str(n) for n in row.get('pending_source_folios', [])} <= available,
                 'Program continuation still names unrestored source pages')
            row.update(pending_source_folios=[], whole_article_assembly_pending=False)
            if 'previous_package' in row:
                record = next(r for r in records if r['id'] == row['program_link_id'])
                prior = by_name[record['left']['segment']]
                row['previous_package'] = dict(path=prior.prefix,
                    manifest=rebase(dict(prior.spec['manifest'], path='manifest.json'), prior.prefix))
        if row['kind'] == 'source-listing-end':
            selected = [r for r in units.values() if r['listing_id'] == row['listing_id']][-1]
            need(row['source_unit_id'] == selected['line_id'] and
                 row['last_printed_row'] == selected['printed_line'] and
                 row['source_segment'] == selected['source_segment'] and
                 row.get('unconditional_END_inferred') is False,
                 'Source ending differs from the final observed unit')
            row['whole_article_assembly_pending'] = False
            group = next(g for g in correction['listing_groups'] if g['listing_id'] == row['listing_id'])
            group.update(complete=True, incoming_continuation=False, execute_verified=False,
                         completeness_scope='complete observed printed listing; execution unverified')
