"""Opt-in regional literal indexes, uncertain graphic runs and source relationships.

Original corrections stay immutable. Active spans address assembled downloads;
source declarations, rather than expected program behavior, establish joins.
"""
from collections import Counter
from copy import deepcopy
import re

from .assemble import rebase
from .assembly_structured import checked_span, START, END

UNIT_KEYS = {'source_string_unit_id', 'parameter_source_unit_id', 'target_source_unit_id',
             'last_source_unit_id', 'first_source_unit_id', 'previous_source_unit_id',
             'open_final_source_unit_id', 'incoming_source_unit_id', 'embedded_end_source_unit_id',
             'prior_source_unit_id'}
UNIT_LISTS = {'source_unit_ids', 'loader_source_unit_ids', 'display_source_unit_ids', 'earlier_rts_source_unit_ids'}
REGION_LISTS = {'figure_region_ids', 'loader_region_ids'}
BLOCK_EXTRA = {'tagline_block_id', 'source_prose_block_id'}
LOCAL_EXTRA = {'value_label_id', 'figure_label_id'}
BLOCK_EXTRA_LISTS = {'listing_block_ids'}
LISTING_EXTRA = {'setup_listing_id'}


def need(condition, message):
    if not condition:raise ValueError(message)


def unit(context, value):
    return context.logical_aliases.get(value, context.name + ':' + value)


def reference(context, key, value):
    if key == 'boundary_evidence':return True, NotImplemented
    if value is None:return False, None
    if not context.extended_source_indexes and key in {'prior_source_unit_id','embedded_end_source_unit_id','earlier_rts_source_unit_ids','source_prose_block_id','listing_block_ids','setup_listing_id','listing_ids','labels','figure_label_id'}:
        return False, None
    if key == 'prior_source_unit_id':return True, value  # Qualified against the prior manifest after joining.
    if key in UNIT_KEYS:return True, unit(context,value)
    if key in UNIT_LISTS:return True, [unit(context,v) for v in value]
    if key in REGION_LISTS:return True, [context.identity(v,context.regions) for v in value]
    if key in BLOCK_EXTRA:return True, context.block(value)
    if key in BLOCK_EXTRA_LISTS:return True, [context.block(v) for v in value]
    if key in LISTING_EXTRA:
        context.identity(value,context.groups)
        return True, context.listing_ids[value]
    if key == 'listing_ids':
        for v in value:context.identity(v,context.groups)
        return True, [context.listing_ids[v] for v in value]
    if key == 'labels' and isinstance(value,list) and all(isinstance(v,str) for v in value):
        return True, [context.name+':'+v for v in value]
    if key == 'table_ids':return True, [context.identity(v,context.tables) for v in value]
    if key in LOCAL_EXTRA or key in ('physical_line_id','table_row_id','paragraph_id'):
        return True, context.name + ':' + value
    return False, None


def graphic_span(context, row):
    """Derive optional block coordinates from the explicit listing index base."""
    base=next(r[START] for r in context.correction['listing_index'] if r['block_id']==row['block_id'])
    a,z=row[START]-base,row[END]-base
    need(row.get('block_start_byte',a)==a and row.get('block_end_byte',z)==z,
         'Graphic listing and block coordinate systems differ')
    return a,z


def validate_source_indexes(context):
    correction=context.correction
    need(correction.get('character_perfect_code',False) is False,
         'Source indexes cannot establish character-perfect code')
    supplied=correction.get('text_index',[])
    need(len(supplied)==len(context.blocks) and {r['block_id'] for r in supplied}==set(context.blocks),
         'Source text index must cover each original block exactly once')
    for row in supplied:
        need(row.get('download')=='article.txt' and (row[START],row[END])==context.ranges[row['block_id']] and
             row['region_ids']==context.blocks[row['block_id']]['region_ids'], 'Source text index differs from complete block')
    graphics=correction.get('unresolved_graphics',[])
    need(graphics==correction.get('unresolved_text',[]), 'Graphic and unresolved-text source indexes differ')
    expected=Counter()
    for id,block in context.blocks.items():
        for match in re.finditer(r'⟦[^⟧]+⟧',block['text']):
            expected[(id,len(block['text'][:match.start()].encode()),match.group())]+=1
    labels={r['label_id']:r for r in correction.get('figure_label_index',[])}
    need(len(labels)==len(correction.get('figure_label_index',[])), 'Duplicate source figure label')
    for id,label in labels.items():
        for match in re.finditer(r'⟦[^⟧]+⟧',label.get('text',label.get('literal',''))):
            expected[('figure-label:'+id,len(label.get('text',label.get('literal',''))[:match.start()].encode()),match.group())]+=1
    observed=Counter()
    physical={r['line_id']:r for r in correction['listing_line_index']}
    logical={r['line_id']:r for r in correction['logical_listing_line_index']}
    for row in graphics:
        need(row.get('status')=='manual-correction-required' and
             all(k in row and row[k] is None for k in ('original_bytes','encoded_bytes','originalGlyphCount')) and
             all(row.get(k) is False for k in ('source_encoding_verified','machine_byte_verified')),
             'Graphic occurrence must retain unknown bytes/counts and unverified encoding')
        if 'figure_label_id' in row:
            label=labels.get(row['figure_label_id'])
            figure=next((f for f in correction.get('figure_structures',[]) if f.get('figure_id')==row.get('figure_id')),None)
            need(label is not None and figure is not None and row['figure_label_id'] in figure.get('labels',[])
                 and label['region_id']==row['region_id']==figure['figure_region_id']
                 and label['scan']==row['scan']==context.assets[row['region_id']]
                 and row['transcription_excerpt']==row['marker'] and label['text'].count(row['marker'])==1,
                 'Graphic occurrence differs from its figure label source')
            a=len(label['text'].split(row['marker'])[0].encode())
            observed[('figure-label:'+row['figure_label_id'],a,row['marker'])]+=1
            continue
        id=row['block_id'];a,z=graphic_span(context,row)
        checked_span(context.blocks[id]['text'].encode(),a,z,row['marker'])
        checked_span(context.listing,row[START],row[END],row['marker'])
        source=physical.get(row['physical_line_id'])
        owner=logical.get(row['source_unit_id'])
        need(source is not None and source['block_id']==id and source['region_id']==row['region_id'] and
             source['block_start_byte']<=a<z<=source['block_end_byte'] and row['scan']==context.assets[row['region_id']] and
             row.get('download')=='listing.txt' and row[START]==source[START]+a-source['block_start_byte'] and
             row[END]==source[START]+z-source['block_start_byte'] and owner is not None and
             row['physical_line_id'] in owner['physical_line_ids'] and
             row['transcription_excerpt']==row['marker'], 'Graphic occurrence differs from its physical source')
        observed[(id,a,row['marker'])]+=1
    need(observed==expected and all(n==1 for n in observed.values()), 'Graphic occurrences do not partition editorial markers')
    regional={r['region_id']:r for r in correction['regional_text_ranges']}
    for table in correction.get('tables',[]):
        for row in table['rows']:
            regional_parts=[]
            for cell in row['cells']:
                if 'source_segments' not in cell:continue
                cursor=cell['start_byte'];parts=[]
                for part in cell['source_segments']:
                    regional_parts.append(part['region_id'])
                    source=regional.get(part['region_id'])
                    need(source is not None and source['block_id']==table['block_id'] and
                         part['scan']==context.assets[part['region_id']] and part['start_byte']==cursor and
                         source['start_byte']<=cursor<=part['end_byte']<=source['end_byte'],
                         'Continued table cell differs from its regional source')
                    parts.append(checked_span(context.blocks[table['block_id']]['text'].encode(),
                                              cursor,part['end_byte'],part['literal']))
                    cursor=part['end_byte']
                need(cursor==cell['end_byte'] and ''.join(parts)==cell['text'],
                     'Continued table cell parts do not cover the selected literal')
            if regional_parts:
                need(row.get('region_ids',[row.get('region_id')])==list(dict.fromkeys(regional_parts)),
                     'Table row regions differ from its cell source parts')
    regions={r['id']:r for r in context.source['regions']}
    for figure in correction.get('figure_structures',[]):
        if 'labels' in figure:
            need(all(id in labels and labels[id]['region_id']==figure['figure_region_id'] for id in figure['labels']),
                 'Figure labels differ from their owning source region')
        for part in figure.get('parts',[]):
            source=regions.get(part['region_id'])
            need(source is not None and source['kind']=='figure' and part['scan']==context.assets[part['region_id']] and
                 part['source_bbox']==source['bbox'] and part['source_index']==source['source_index'],
                 'Artwork placement differs from original source coordinates')


def project_index(context,key,original,row,ranges):
    if key=='text_index':
        target,within=context.positions[context.identity(original['block_id'],context.blocks)]
        length=len(context.blocks[original['block_id']]['text'].encode())
        row.update(download='article.txt',**{START:ranges[target][0]+within,END:ranges[target][0]+within+length})
        return
    if key in ('listing_line_index','listing_caption_associations'):return
    if key in ('unresolved_graphics','unresolved_text') and 'block_id' in original:
        a,z=graphic_span(context,original)
        within=context.positions[context.identity(original['block_id'],context.blocks)][1]
        row.update(block_start_byte=a+within,block_end_byte=z+within)
    if context.extended_source_indexes and key=='logical_listing_line_index':
        physical={r['line_id']:r for r in context.correction['listing_line_index']}
        for part,target in zip(original.get('source_parts',[]),row.get('source_parts',[]),strict=True):
            source=physical.get(part['line_id'])
            need(source is not None and part['line_id'] in original['physical_line_ids']
                 and part['physical_start_byte']==source[START], 'Logical source part differs from physical listing coordinates')
            target['physical_start_byte']=part['physical_start_byte']+context.offset
    # Physical fields and caption spans have their own coordinate owners.
    owner=original.get('block_id',original.get('code_block_id'))
    if owner is None and original.get('listing_id') is not None:owner=context.code_block(original['listing_id'])
    if context.extended_source_indexes and owner is None and original.get('source_unit_id') is not None:
        matches=[r for r in context.correction['logical_listing_line_index'] if r['line_id']==original['source_unit_id']]
        need(len(matches)==1, 'Literal coordinate owner lacks one original source unit')
        owner=matches[0]['block_id']
    def walk(source,target,owner):
        if isinstance(source,list):
            for a,b in zip(source,target,strict=True):walk(a,b,owner)
        elif isinstance(source,dict):
            current=source.get('block_id',source.get('code_block_id',owner))
            if current is not None:
                within=context.positions[context.identity(current,context.blocks)][1]
                if 'start_byte' in source and 'end_byte' in source:
                    context.block_span(source,target,ranges,owner=current,
                        literal=source.get('literal',source.get('text',source.get('separator'))))
                if 'block_start_byte' in source:
                    checked_span(context.blocks[current]['text'].encode(),source['block_start_byte'],source['block_end_byte'],
                                 source.get('marker',source.get('literal')))
                    target['block_start_byte']=source['block_start_byte']+within
                    target['block_end_byte']=source['block_end_byte']+within
                if 'block_anchor_byte' in source:
                    checked_span(context.blocks[current]['text'].encode(),source['block_anchor_byte'],source['block_anchor_byte'])
                    base=next(r[START] for r in context.correction['listing_index'] if r['block_id']==current)
                    need(source['anchor_byte']==base+source['block_anchor_byte'], 'Source anchor coordinate systems differ')
                    target['block_anchor_byte']=source['block_anchor_byte']+within
                    target['anchor_byte']=source['anchor_byte']+context.offset
                elif context.extended_source_indexes and 'anchor_byte' in source:
                    need(context.blocks[current]['kind']!='code', 'Code anchor requires explicit coordinate owner')
                    checked_span(context.blocks[current]['text'].encode(),source['anchor_byte'],source['anchor_byte'])
                    target.update(block_anchor_byte=source['anchor_byte']+within,download='article.txt',
                                  anchor_byte=ranges[context.block(current)][0]+within+source['anchor_byte'])
            if source.get('download')=='listing.txt' and START in source:
                checked_span(context.listing,source[START],source[END],source.get('literal',source.get('text')))
                target[START]=source[START]+context.offset;target[END]=source[END]+context.offset
            for field,value in source.items():
                if field in target and field not in ('source_parts','boundary_evidence','evidence') and isinstance(value,(dict,list)):
                    walk(value,target[field],current)
    walk(original,row,owner)


def finish_indexes(package,correction,contexts):
    # Retain both constituent text records while exposing one complete block range.
    combined=[];by_id={}
    for row in correction['text_index']:
        id=row['block_id']
        if id not in by_id:
            result=deepcopy(row);result['source_parts']=[deepcopy(row)];by_id[id]=result;combined.append(result)
        else:
            result=by_id[id];need(row[START]==result[END], 'Joined text index is not contiguous')
            result[END]=row[END];result['region_ids']+=row['region_ids'];result['source_parts'].append(deepcopy(row))
    correction['text_index']=combined
    resolve_prior(correction,contexts)


def resolve_prior(correction,contexts):
    projected={(r['source_segment'],r['source_ref']['pointer']):r for r in correction['content_associations']}
    logical={r['line_id']:r for r in correction['logical_listing_line_index']}
    resolutions=[];used=set()
    for n,current in enumerate(contexts):
        if 'previous_package_manifest' in current.correction:
            need(n>0 and all(current.correction['previous_package_manifest'].get(k)==contexts[n-1].spec['manifest'][k]
                            for k in ('sha256','bytes')), 'Source metadata previous manifest differs')
        for index,source in enumerate(current.correction['content_associations']):
            kind=source['kind']
            if kind=='source-address-literal-match' and source.get('match_scope')=='prior-segment-monitor-row':
                need(n>0, 'Address literal match lacks its prior segment')
                prior=contexts[n-1]
                need(all(source.get('prior_package_manifest',{}).get(k)==prior.spec['manifest'][k] for k in ('sha256','bytes')),
                     'Address literal match prior manifest differs')
                matches=[r for r in prior.correction['logical_listing_line_index']
                         if r['line_id']==source.get('prior_source_unit_id') and r['listing_id']==source['listing_id']
                         and r.get('printed_address')==source.get('address_literal')]
                active=projected[(current.name,f'/content_associations/{index}')]
                need(len(matches)==1 and active['listing_id']==prior.listing_ids[matches[0]['listing_id']]
                     and source.get('printed_operand','').lstrip('$')==source['address_literal']
                     and source.get('target_source_unit_id') is None,
                     'Prior address literal does not identify one joined source row')
                target=unit(prior,matches[0]['line_id'])
                active.update(target_source_unit_id=target,prior_source_unit_id=target,
                              match_scope='assembled-monitor-row',
                              previous_segment_manifest=rebase({**prior.spec['manifest'],'path':'manifest.json'},prior.prefix))
                active.pop('prior_package_manifest',None)
                resolutions.append(dict(kind=kind,source=deepcopy(active['source_ref']),target_source_unit_id=target,
                                        source_values_changed=False,execute_verified=False))
                continue
            if not kind.startswith('source-prior-'):continue
            need(n>0,'Prior source relationship lacks its immediately preceding segment')
            prior=contexts[n-1];manifest=source.get('previous_package_manifest',{})
            need(all(manifest.get(k)==prior.spec['manifest'][k] for k in ('sha256','bytes')),
                 'Prior source relationship manifest differs')
            active=projected[(current.name,f'/content_associations/{index}')]
            prior_rows=prior.correction['content_associations']
            matches=[]
            if kind=='source-prior-program-explanation':
                matches=[(i,r) for i,r in enumerate(prior_rows) if r['kind']=='source-program-range-explanation' and
                         r['table_id']==source['previous_table_id'] and r['table_row_id']==source['previous_table_row_id'] and
                         r['printed_range']==source['printed_range']]
                need(len(matches)==1,'Prior explanation does not identify one original table row')
                _,out=matches[0];a,z=out['first_printed_row'],out['last_printed_row']
                expected=[r['line_id'] for r in current.correction['logical_listing_line_index']
                          if r['listing_id']==source['listing_id'] and a<=r['printed_line']<=z]
                need(source['source_unit_ids']==expected and expected and out['pending_source_folios'],
                     'Prior explanation source units differ from the declared range')
                active.update(table_id=prior.identity(source['previous_table_id'],prior.tables),
                              table_row_id=prior.name+':'+source['previous_table_row_id'])
            elif kind=='source-prior-key-dispatch-target':
                matches=[(i,r) for i,r in enumerate(prior_rows) if r['kind']=='source-key-dispatch-branch' and
                         r['table_row_id']==source['previous_table_row_id'] and r['branch_index']==source['branch_index'] and
                         r['printed_key']==source['printed_key'] and r['target_printed_row']==source['target_printed_row']]
                need(len(matches)==1 and active['source_unit_id'] in logical and
                     logical[active['source_unit_id']]['printed_line']==source['target_printed_row'],
                     'Prior key branch differs from its source target')
                active['table_row_id']=prior.name+':'+source['previous_table_row_id']
            elif kind=='source-prior-title-data-loader':
                matches=[(i,r) for i,r in enumerate(prior_rows) if r['kind']=='source-title-data-group' and r['group_id'] in source['previous_group_ids']]
                need([r['group_id'] for _,r in matches]==source['previous_group_ids'] and matches,
                     'Prior title loader loses or invents source data groups')
                active['group_ids']=[prior.name+':'+id for id in source['previous_group_ids']]
                need(all(id in logical for id in active['loader_source_unit_ids']), 'Prior title loader names an absent source unit')
                numbers=[logical[id]['printed_line'] for id in active['loader_source_unit_ids']]
                need(all(r['loader_printed_rows']==numbers for _,r in matches),
                     'Prior title data loader differs from its declared printed rows')
            else:raise ValueError('Unsupported prior source relationship')
            for previous_index,source_out in matches:
                occurrence=prior.name,previous_index,kind
                need(occurrence not in used,'Repeated prior source relationship');used.add(occurrence)
                out=projected[(prior.name,f'/content_associations/{previous_index}')]
                if kind=='source-prior-program-explanation':
                    selected=list(dict.fromkeys(out['source_unit_ids']+active['source_unit_ids']))
                    expected=[r['line_id'] for r in correction['logical_listing_line_index']
                              if r['listing_id']==out['listing_id'] and source_out['first_printed_row']<=r['printed_line']<=source_out['last_printed_row']]
                    need(selected==expected,'Whole explanation range loses or invents source units')
                    out.update(source_unit_ids=selected,restoration_coverage='complete in assembled article',pending_source_folios=[])
                elif kind=='source-prior-key-dispatch-target':
                    need(source_out['target_source_unit_id'] is None,'Prior key target was already restored')
                    out.update(target_source_unit_id=active['source_unit_id'],target_restoration='complete in assembled article')
                else:
                    out.update(loader_source_unit_ids=active['loader_source_unit_ids'],loader_restoration='complete in assembled article')
                out.setdefault('resolution_sources',[]).append(deepcopy(active['source_ref']))
            active['kind']='resolved-'+kind.removeprefix('source-')
            active['previous_segment_manifest']=rebase({**prior.spec['manifest'],'path':'manifest.json'},prior.prefix)
            for key in ('previous_package_manifest','previous_table_id','previous_table_row_id','previous_group_ids'):active.pop(key,None)
            resolutions.append(dict(kind=kind,source=deepcopy(active['source_ref']),
                targets=[prior.source_ref('content_associations',i) for i,_ in matches],source_values_changed=False))
    for row in correction['content_associations']:
        if row.get('pending_source_folios') or row.get('loader_restoration','').startswith('pending') or row.get('target_restoration','').startswith('pending'):
            raise ValueError('Unresolved source relationship remains after assembly')
        if row['kind']=='resolved-listing-continuation' and 'pending_folios' in row:
            row.update(pending_folios=[],logical_unit_complete=True)
    correction['resolved_source_relationships']=resolutions
