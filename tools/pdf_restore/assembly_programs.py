"""Opt-in source-declared program/group joins and scoped diagram references.

Only structured-programs-v1 uses this projection. Original segment files and
listing bytes remain exact; instruction meanings never establish a boundary.
"""
from copy import deepcopy
from collections import Counter

START, END = 'utf8_byte_start', 'utf8_byte_end_exclusive'


def validate_extensions(recipe, names):
    for key in ('program_links', 'group_links', 'example_links'):
        if not isinstance(recipe[key], list):
            raise ValueError('Program assembly requires explicit link lists')
        ids = [r.get('id') for r in recipe[key] if isinstance(r, dict)]
        if len(ids) != len(recipe[key]) or any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
            raise ValueError('Program links require unique nonblank identities')
    for link in recipe['program_links']:
        if set(link) not in ({'id', 'left', 'right'}, {'id', 'left', 'right', 'logical_join'}, {'id', 'left', 'right', 'address_join'}):
            raise ValueError('Invalid program link fields')
        if 'address_join' in link:
            from .assembly_addresses import validate_join
            validate_join(link)
            if any(link[side]['segment'] not in names for side in ('left', 'right')):
                raise ValueError('Unknown address boundary segment')
            if names.index(link['right']['segment']) != names.index(link['left']['segment']) + 1:
                raise ValueError('Address join requires consecutive segments')
        else:
            for side, boundary in [('left', 'last_printed_row'), ('right', 'first_printed_row')]:
                r = link[side]
                if (not isinstance(r, dict) or set(r) != {'segment', 'listing_id', boundary, 'association'} or
                        r['segment'] not in names or not isinstance(r['listing_id'], str) or not r['listing_id'] or
                        any(type(r[k]) is not int or r[k] < 0 for k in (boundary, 'association'))):
                    raise ValueError('Invalid source program boundary')
            if names.index(link['right']['segment']) != names.index(link['left']['segment']) + 1:
                raise ValueError('Program join requires consecutive segments')
            if 'logical_join' in link:
                from .assembly_fragments import validate_join
                validate_join(link)
            elif link['right']['first_printed_row'] != link['left']['last_printed_row'] + 1:
                raise ValueError('Program source row boundary is not consecutive')
    for link in recipe['group_links']:
        if set(link) != {'id', 'program_id', 'left', 'right'} or link['program_id'] not in {r['id'] for r in recipe['program_links']}:
            raise ValueError('Group join requires an explicit program link')
        if any(r['id']==link['program_id'] and 'address_join' in r for r in recipe['program_links']):
            raise ValueError('Numbered group joins cannot replace printed address boundaries')
        for side in ('left', 'right'):
            r = link[side]
            if (not isinstance(r, dict) or set(r) != {'segment', 'association'} or
                    r['segment'] not in names or type(r['association']) is not int or r['association'] < 0):
                raise ValueError('Invalid source group boundary')
    examples = set()
    for link in recipe['example_links']:
        if set(link) != {'id', 'source', 'listing_targets', 'note'} or not isinstance(link['note'], str) or not link['note'].strip():
            raise ValueError('Invalid source example link')
        source = link['source']
        if (not isinstance(source, dict) or set(source) != {'segment', 'association'} or source['segment'] not in names or
                type(source['association']) is not int or source['association'] < 0 or
                not isinstance(link['listing_targets'], list) or not link['listing_targets']):
            raise ValueError('Invalid source example occurrence')
        occurrence = source['segment'], source['association']
        if occurrence in examples:raise ValueError('Repeated source example occurrence')
        examples.add(occurrence)
        for target in link['listing_targets']:
            if (not isinstance(target, dict) or set(target) != {'segment', 'listing_id'} or
                    target['segment'] not in names or not isinstance(target['listing_id'], str) or not target['listing_id']):
                raise ValueError('Invalid source example target')


def association(context, index):
    try:
        return context.correction['content_associations'][index]
    except (IndexError, KeyError) as error:
        raise ValueError('Source association is absent') from error


def folio(context, region):
    source_index = next(r['source_index'] for r in context.source['regions'] if r['id'] == region)
    return next(p['printed_page'] for p in context.source['pages'] if p['source_index'] == source_index)


def join_programs(recipe, package, contexts, positions):
    by_name = {c.name: c for c in contexts};used = set();records = []
    for link in recipe['program_links']:
        a, b = (by_name[link[side]['segment']] for side in ('left', 'right'))
        left, right = link['left'], link['right']
        out, inc = association(a, left['association']), association(b, right['association'])
        if 'address_join' in link:
            from .assembly_addresses import check_boundary
            check_boundary(link, a, b, out, inc)
            for context, part in [(a, left), (b, right)]:
                key = context.name, part['association']
                if key in used:raise ValueError('Repeated source address continuation')
                used.add(key)
        else:
            for context, part, row, kind in [(a, left, out, 'listing-continuation'), (b, right, inc, 'incoming-listing-continuation')]:
                key = context.name, part['association']
                if key in used or row.get('kind') != kind or row.get('listing_id') != part['listing_id'] or row.get('code_block_id') != context.code_block(part['listing_id']):
                    raise ValueError('Program boundary differs from source association')
                used.add(key)
            n, m = left['last_printed_row'], right['first_printed_row']
            aa = [r for r in a.correction['logical_listing_line_index'] if r['listing_id'] == left['listing_id']]
            bb = [r for r in b.correction['logical_listing_line_index'] if r['listing_id'] == right['listing_id']]
            if (not aa or not bb or aa[-1]['printed_line'] != n or bb[0]['printed_line'] != m or
                    str(out.get('next_folio')) != str(folio(b, inc['source_region_id'])) or
                    str(inc.get('previous_folio')) != str(folio(a, out['source_region_id'])) or
                    any(inc.get('previous_package', {}).get('manifest', {}).get(k) != a.spec['manifest'][k] for k in ('sha256', 'bytes'))):
                raise ValueError('Program rows, folios or previous manifest differ from source')
            if 'logical_join' in link:
                from .assembly_fragments import check_boundary
                check_boundary(link, a, b, out, inc, aa, bb)
            elif (out.get('last_printed_row'), out.get('next_printed_row'), inc.get('previous_last_printed_row'), inc.get('first_printed_row')) != (n, m, n, m):
                raise ValueError('Program source row declarations differ')
            elif out.get('open_source_label') != inc.get('open_source_label'):
                raise ValueError('Open source program label differs across boundary')
        ids = [positions[c.identity(c.code_block(part['listing_id']), c.blocks)][0] for c, part in [(a, left), (b, right)]]
        blocks = {r['id']: r for r in package['blocks']}
        if ids[0] == ids[1] or any(blocks[id]['kind'] != 'code' for id in ids):
            raise ValueError('Program join requires distinct source code blocks')
        x, y = (blocks[id] for id in ids);order = package['content_order']
        i, j = (order.index(dict(type='block', id=id)) for id in ids)
        if j != i + 1:
            raise ValueError('Program parts are not adjacent in reviewed content order')
        offset = len(x['text'].encode());x['text'] += y['text']
        for key in ('region_ids', 'correction_evidence', 'uncertainties'):
            x[key] = list(dict.fromkeys(x[key] + y[key]))
        package['blocks'].remove(y);del order[j]
        for original, (target, within) in list(positions.items()):
            if target == ids[1]:positions[original] = ids[0], offset + within
        target_listing = a.listing_ids[left['listing_id']];old_listing = b.listing_ids[right['listing_id']]
        for context in contexts:
            context.listing_ids = {k: target_listing if v == old_listing else v for k, v in context.listing_ids.items()}
        record=dict(id=link['id'],listing_id=target_listing,block_id=ids[0],left=deepcopy(left),right=deepcopy(right),right_block_offset=offset,source_text_preserved=True,execute_verified=False,source_occurrences=[a.source_ref('content_associations',left['association']),b.source_ref('content_associations',right['association'])])
        for extension in ('logical_join', 'address_join'):
            if extension in link:record[extension]=deepcopy(link[extension])
        records.append(record)
    expected = {(c.name, i) for c in contexts for i, r in enumerate(c.correction.get('content_associations', [])) if r.get('kind') in ('listing-continuation', 'incoming-listing-continuation', 'source-listing-continuation', 'source-listing-continuation-from')}
    if used != expected:
        raise ValueError('Unresolved or repeated source program continuation')
    return records


def project_figure(context, source, row):
    """Scope generic figure IDs and validate specialized label/guide references."""
    labels = {r['label_id'] for r in context.correction.get('figure_label_index', [])}
    local = {}
    for key in ('curves', 'vertical_guides', 'axes', 'bars'):
        values = [r['id'] for r in source.get(key, []) if isinstance(r, dict) and 'id' in r]
        if len(set(values)) != len(values):raise ValueError('Duplicate figure component identity')
        local[key] = set(values)
    prefix = context.name + ':' + source['figure_region_id'] + ':'
    references = {'axis_id':'axes', 'guide_id':'vertical_guides', 'from_guide':'vertical_guides', 'to_guide':'vertical_guides', 'bar_ids':'bars'}
    specialized_labels = {'branch_label_id','legend_label_id','pitch_label_id','room_label_id','scale_label_ids'}
    def walk(original, projected):
        if isinstance(original, list):
            for a,b in zip(original,projected,strict=True):walk(a,b)
        elif isinstance(original, dict):
            for key,value in original.items():
                if key in ('id','edge_id') and isinstance(value,str):projected[key] = prefix + value
                elif key in references:
                    values = value if isinstance(value,list) else [value]
                    if any(v not in local[references[key]] for v in values):raise ValueError('Dangling scoped figure component')
                    projected[key] = [prefix+v for v in value] if isinstance(value,list) else prefix+value
                elif key in specialized_labels and value is not None:
                    values = value if isinstance(value,list) else [value]
                    if any(v not in labels for v in values):raise ValueError('Dangling specialized figure label')
                    projected[key] = [context.name+':'+v for v in value] if isinstance(value,list) else context.name+':'+value
                elif key in projected and isinstance(value,(dict,list)):walk(value,projected[key])
    walk(source,row)
    # Standard label/node references are scoped by Context.refs; check their source closure per figure.
    nodes = {r['node_id'] for r in source.get('nodes', [])}
    if len(nodes) != len(source.get('nodes', [])):raise ValueError('Duplicate source figure node')
    def closure(value):
        if isinstance(value,list):
            for item in value:closure(item)
        elif isinstance(value,dict):
            for key,item in value.items():
                if key=='label_id' and item is not None and item not in labels:raise ValueError('Dangling source figure label')
                if key in ('from_node','to_node') and item not in nodes:raise ValueError('Cross-figure or absent source node')
                if isinstance(item,(dict,list)):closure(item)
    closure(source)
    return row


def finish_programs(recipe, package, c, contexts, records):
    by_name = {x.name:x for x in contexts};blocks={r['id']:r for r in package['blocks']}
    from .assembly_fragments import finish_fragments
    fragment_listings = finish_fragments(c, records)
    address_listings = {r['listing_id'] for r in records if 'address_join' in r}
    # Preserve every projected source group/index as a constituent of its one unified program.
    for key in ('listing_groups','listing_index'):
        combined=[];by_id={}
        for row in c[key]:
            id=row['listing_id']
            if id not in by_id:
                result=deepcopy(row);result['source_parts']=[deepcopy(row)];by_id[id]=result;combined.append(result)
            else:
                result=by_id[id];result['source_parts'].append(deepcopy(row))
                if key=='listing_groups':
                    if row['block_ids']!=result['block_ids'] or row.get('line_kind')!=result.get('line_kind'):raise ValueError('Unified listing groups disagree')
                else:
                    if row['block_id']!=result['block_id'] or row[START]!=result[END]:raise ValueError('Unified listing ranges are not contiguous')
                    result[END]=row[END];result['region_ids']+=row['region_ids']
        c[key]=combined
    for group in c['listing_groups']:
        id=group['listing_id'];physical=[r for r in c['listing_line_index'] if r['listing_id']==id]
        if len(group['source_parts'])>1:
            for n,row in enumerate(physical,1):row['source_physical_line']=row['physical_line'];row['physical_line']=n
            numbers=[r['printed_line'] for r in c['logical_listing_line_index'] if r['listing_id']==id]
            if id in address_listings:
                from .assembly_addresses import check_partition
                check_partition(group, physical, c['logical_listing_line_index'])
            elif id in fragment_listings:
                from .assembly_fragments import check_partition
                check_partition(group, physical, c['logical_listing_line_index'])
            elif any(type(n) is not int for n in numbers) or numbers!=list(range(numbers[0],numbers[-1]+1)):raise ValueError('Unified program has duplicate/missing numbered units')
            units=[r for r in c['logical_listing_line_index'] if r['listing_id']==id]
            owned=Counter(n for r in units for n in r['physical_line_ids'])
            if id not in fragment_listings | address_listings and owned!=Counter(r['line_id'] for r in physical if r.get('printed_line') is not None):raise ValueError('Unified logical units do not partition numbered source rows')
        if ''.join(r['text'] for r in physical)!=blocks[group['block_ids'][0]]['text']:raise ValueError('Unified program rows differ from complete code block')
    for record in records:
        for side in ('left','right'):
            part=record[side];row=next(r for r in c['content_associations'] if r.get('source_segment')==part['segment'] and r['source_ref']['pointer']==f'/content_associations/{part["association"]}')
            row.update(kind='resolved-listing-continuation',status='source parts joined as one program; original bytes retained',program_link_id=record['id'])
            if 'address_join' in record:
                row.update(remaining_source_folios=[], whole_assembly_pending=False, whole_article_complete=True)
                if side == 'right':
                    prior = by_name[record['left']['segment']]
                    row['prior_source_unit_id'] = prior.name + ':' + record['address_join']['left_source_unit_id']
                    row.pop('prior_package_manifest', None)
    resolved_groups=[];used=set()
    for link in recipe['group_links']:
        program=next(r for r in records if r['id']==link['program_id'])
        if any(link[side]['segment']!=program[side]['segment'] for side in ('left','right')):raise ValueError('Group and program joins have different source segments')
        parts=[]
        for side in ('left','right'):
            part=link[side];key=part['segment'],part['association']
            if key in used:raise ValueError('Repeated source group join')
            used.add(key)
            parts.append(next(r for r in c['content_associations'] if r.get('source_segment')==part['segment'] and r['source_ref']['pointer']==f'/content_associations/{part["association"]}'))
        left,right=parts
        if (left.get('kind')!=right.get('kind') or left.get('source_label')!=right.get('source_label') or
                left.get('listing_id')!=program['listing_id'] or right.get('listing_id')!=program['listing_id'] or
                left.get('continuation_pending') is not True or right.get('incoming_continuation') is not True or
                left.get('last_printed_row')!=program['left']['last_printed_row'] or right.get('first_printed_row')!=program['right']['first_printed_row'] or
                left.get('end_byte')!=right.get('start_byte') or left.get('block_id')!=right.get('block_id')):
            raise ValueError('Group join differs from open source group and program boundary')
        original=deepcopy(parts);left.update(group_id=link['id'],end_byte=right['end_byte'],last_printed_row=right['last_printed_row'],literal=left['literal']+right['literal'],physical_line_ids=left['physical_line_ids']+right['physical_line_ids'],region_ids=list(dict.fromkeys(left['region_ids']+right['region_ids'])),continuation_pending=False,incoming_continuation=False,source_parts=original)
        # Group spans use article coordinates, while listing field spans remain separate.
        left[END]=right[END];c['content_associations'].remove(right)
        resolved_groups.append(dict(id=link['id'],listing_id=program['listing_id'],source_label=left['source_label'],source_occurrences=[p['source_ref'] for p in original],source_text_preserved=True))
    unresolved=[r for r in c['content_associations'] if r.get('continuation_pending') is True or r.get('incoming_continuation') is True]
    if unresolved:raise ValueError('Unresolved source data/routine group continuation')
    resolved_examples=[]
    for link in recipe['example_links']:
        source=link['source'];context=by_name[source['segment']];original=association(context,source['association'])
        row=next(r for r in c['content_associations'] if r.get('source_segment')==source['segment'] and r['source_ref']['pointer']==f'/content_associations/{source["association"]}')
        targets=[by_name[t['segment']].block(by_name[t['segment']].code_block(t['listing_id'])) for t in link['listing_targets']]
        if original.get('kind')!='source-example' or len(set(targets))!=len(targets) or not set(row.get('code_block_ids',[]))<=set(targets):raise ValueError('Example link loses original source program relationships')
        row.update(code_block_ids=targets,source_note=row.get('note'),note=link['note'],relationship_id=link['id'])
        resolved_examples.append(dict(id=link['id'],source_occurrence=row['source_ref'],code_block_ids=targets,source_values_changed=False))
    c.update(resolved_programs=records,resolved_groups=resolved_groups,resolved_examples=resolved_examples)
