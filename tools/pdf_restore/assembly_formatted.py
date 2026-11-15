"""Opt-in assembly of original formatter displays across multiple source blocks.

Program identities and boundary joins are declared explicitly. Printed annotations,
physical rows and logical source parts remain literal; no executable BASIC is made.
"""
from copy import deepcopy
import re

from .assembly_structured import checked_span, START, END

UNIT_KEYS = {'source_caption_unit_id','comment_source_unit_id','initialization_source_unit_id',
             'source_heading_unit_id','heading_source_unit_id','for_source_unit_id',
             'next_source_unit_id','display_source_unit_id','read_loop_source_unit_id'}
UNIT_LISTS = {'credit_source_unit_ids','qualifier_source_unit_ids','data_group_source_unit_ids'}
BLOCK_KEYS = {'header_block_id','listing_block_id','notice_block_id','report_block_id',
              'following_report_block_id','continuation_block_id'}
REGION_KEYS = {'for_region_id','next_region_id','source_figure_region_id'}
REGION_LISTS = {'overlap_region_ids','overlapping_region_ids','source_region_ids'}
LOCAL_KEYS = {'run_id','connector_id','edge_id','slot_id','from_slot_id','to_slot_id',
              'through_slot_id','group_id','junction_id','from_id','to_id','zone_id',
              'branch_label_id','from_label_id'}
LOCAL_LISTS = {'slot_ids','from_slot_ids','node_ids','annotation_label_ids','display_run_ids'}


def need(test, message):
    if not test:raise ValueError(message)


def validate_recipe(recipe):
    from .assembly_structured import validate_recipe as base_validate
    need(recipe.get('source_index_mode')=='regional-literals-v2',
         'Formatted displays require explicit v2 literal coordinates')
    base=deepcopy(recipe);programs=base.pop('formatted_programs',None)
    base.update(index_mode='structured-programs-v1',program_links=[],group_links=[],example_links=[])
    base_validate(base)
    need(not recipe['relationship_links'] and not recipe['prose_joins'],
         'Formatted program mode preserves source blocks without cross-segment block joins')
    need(isinstance(programs,list) and programs,'Formatted programs must be declared')
    names=[s['name'] for s in recipe['segments']];ids=set();used=set()
    for p in programs:
        need(set(p)=={'id','parts','joins'} and isinstance(p['id'],str) and
             re.fullmatch(r'[a-z][a-z0-9-]*',p['id']) and p['id'] not in ids,
             'Formatted program identity is missing or repeated');ids.add(p['id'])
        need(isinstance(p['parts'],list) and p['parts'] and isinstance(p['joins'],list)
             and len(p['joins'])==len(p['parts'])-1,'Each formatted program boundary requires one join')
        for part in p['parts']:
            need(set(part)=={'segment','listing_id'} and part['segment'] in names and
                 isinstance(part['listing_id'],str) and part['listing_id'], 'Unknown formatted source part')
            key=part['segment'],part['listing_id'];need(key not in used,'Repeated formatted source part');used.add(key)
        for left,right,j in zip(p['parts'][:-1],p['parts'][1:],p['joins'],strict=True):
            need(names.index(right['segment'])==names.index(left['segment'])+1,
                 'Formatted continuation requires adjacent source segments')
            need(set(j)=={'kind','left_last','right_first','outgoing_association','incoming_association','joined_reading'}
                 and j['kind'] in ('consecutive','same-number') and
                 all(type(j[k]) is int and j[k]>=0 for k in
                     ('left_last','right_first','outgoing_association','incoming_association')),
                 'Invalid formatted boundary declaration')
            need((j['right_first']==j['left_last']+1 and j['joined_reading'] is None) if j['kind']=='consecutive'
                 else j['right_first']==j['left_last'] and isinstance(j['joined_reading'],str) and j['joined_reading'],
                 'Formatted number boundary or selected joined reading differs')


def reference(context,key,value):
    if value is None:return False,None
    if key in UNIT_KEYS:return True,context.logical_aliases.get(value,context.name+':'+value)
    if key in UNIT_LISTS:return True,[context.logical_aliases.get(v,context.name+':'+v) for v in value]
    if key in BLOCK_KEYS:return True,context.block(value)
    if key in REGION_KEYS:return True,context.identity(value,context.regions)
    if key in REGION_LISTS:return True,[context.identity(v,context.regions) for v in value]
    if key=='source_figure_id':return True,context.identity(value,context.figures)
    if key in LOCAL_KEYS:return True,context.name+':'+value
    if key in LOCAL_LISTS or key=='asterisk_physical_line_ids':return True,[context.name+':'+v for v in value]
    return False,None


def check_groups(context,code_ids):
    groups=list(context.groups.values())
    need([id for g in groups for id in g['block_ids']]==code_ids,
         'Formatted source groups must partition ordered code blocks')
    need(all(g['line_kind']=='formatted-basic-numbered' for g in groups),
         'Formatted assembly cannot reinterpret a different listing grammar')
    rows=context.correction['listing_line_index'];units=context.correction['logical_listing_line_index']
    need(len({r['line_id'] for r in rows})==len(rows),'Duplicate formatted physical row')
    for g in groups:
        selected=[u for u in units if u['listing_id']==g['listing_id']]
        need([u['printed_line'] for u in selected]==g['observed_printed_rows'] and selected,
             'Formatted source group numbers differ from logical units')
        need([id for u in selected for id in u['physical_line_ids']]==
             [r['line_id'] for r in rows if r['listing_id']==g['listing_id']],
             'Formatted logical units must partition their physical rows')
        for u in selected:
            need(u['line_id']==f'{g["listing_id"]}:n{u["printed_line"]}',
                 'Formatted logical identity differs from its printed number')
            parts=[r for r in rows if r['line_id'] in u['physical_line_ids']]
            need(u['logical_text']==''.join(r['text'] for r in parts),
                 'Formatted logical text differs from original physical display')
            char=0
            for p,r in zip(u['source_parts'],parts,strict=True):
                need(p['line_id']==r['line_id'] and p['start_character']==char and
                     p['end_character']==char+len(r['text']) and p['physical_start_byte']==r[START] and p['region_id']==r['region_id'] and p.get('block_id',r['block_id'])==r['block_id'],
                     'Formatted logical character or physical byte coordinate differs')
                char=p['end_character']


def prepare(recipe,contexts):
    by_name={c.name:c for c in contexts};supplied=set();fragments=set()
    for c in contexts:
        c.formatted=True
        for row in c.correction.get('source_literal_index',[])+c.correction.get('source_uncertainties',[]):
            if row.get('kind')=='source-control-display-run':
                need(row.get('originalGlyphCount') is None and row.get('encoding_verified') is False
                     and row.get('encoded_bytes_verified',False) is False and row.get('machine_bytes') is None,
                     'Formatted control-display reading cannot establish encoded bytes/counts')
                figures=[f for f in c.source['figures'] if f['id']==row.get('source_figure_id')]
                need(len(figures)==1 and row.get('source_figure_region_id') in figures[0]['region_ids'],
                     'Formatted control-display crop differs from its original figure')
    for program in recipe['formatted_programs']:
        for part in program['parts']:
            c=by_name[part['segment']];id=part['listing_id']
            need(id in c.groups,'Formatted source listing is absent')
            supplied.add((c.name,id));c.listing_ids[id]=program['id']
            # Include referenced earlier/later numbers only within this declared program.
            for other in program['parts']:
                for u in by_name[other['segment']].correction['logical_listing_line_index']:
                    if u['listing_id']==other['listing_id']:
                        c.logical_aliases[f'{id}:n{u["printed_line"]}']=f'{program["id"]}:n{u["printed_line"]}'
        for left,right,join in zip(program['parts'][:-1],program['parts'][1:],program['joins'],strict=True):
            a,b=(by_name[p['segment']] for p in (left,right));aa=[u for u in a.correction['logical_listing_line_index'] if u['listing_id']==left['listing_id']];bb=[u for u in b.correction['logical_listing_line_index'] if u['listing_id']==right['listing_id']]
            need(aa and bb and aa[-1]['printed_line']==join['left_last'] and bb[0]['printed_line']==join['right_first'],
                 'Formatted boundary numbers differ from source units')
            try:out=a.correction['content_associations'][join['outgoing_association']];inc=b.correction['content_associations'][join['incoming_association']]
            except IndexError as error:raise ValueError('Formatted boundary association absent') from error
            need(out['kind']=='source-listing-continuation' and inc['kind']=='source-incoming-listing-boundary'
                 and out['listing_id']==left['listing_id'] and inc['listing_id']==right['listing_id']
                 and out['last_source_unit_id']==aa[-1]['line_id'] and inc['first_source_unit_id']==bb[0]['line_id']
                 and inc['previous_source_unit_id']==aa[-1]['line_id'],
                 'Formatted continuation differs from declared source associations')
            def folio(c,u,first):
                row=next(r for r in c.correction['listing_line_index'] if r['line_id']==u['physical_line_ids'][0 if first else -1])
                region=next(r for r in c.source['regions'] if r['id']==row['region_id'])
                return next(p['printed_page'] for p in c.source['pages'] if p['source_index']==region['source_index'])
            need(str(out['next_folio'])==str(folio(b,bb[0],True)) and
                 str(inc['previous_folio'])==str(folio(a,aa[-1],False)),
                 'Formatted continuation folios differ')
            if join['kind']=='same-number':
                fragments.update([(a.name,aa[-1]['line_id']),(b.name,bb[0]['line_id'])])
                need(aa[-1]['complete_in_segment'] is False and bb[0]['complete_in_segment'] is False
                     and bb[0].get('incoming_fragment') is True and inc.get('same_source_group') is True
                     and inc.get('previous_group_complete') is False and out.get('logical_group_complete') is False
                     and join['joined_reading']==aa[-1]['logical_text']+bb[0]['logical_text']
                     and bb[0]['logical_text'].startswith('['+str(join['right_first'])+']')
                     and out.get('next_printed_marker')==inc.get('incoming_marker')=='['+str(join['right_first'])+']',
                     'Formatted same-number remark boundary differs from selected source fragments')
            else:
                need(aa[-1].get('complete_in_segment',True) is True and bb[0].get('complete_in_segment',True) is True
                     and inc.get('previous_group_complete') is True and out.get('next_printed_row')==join['right_first'],
                     'Formatted consecutive boundary cannot hide an incomplete source group')
    need(fragments=={(c.name,u['line_id']) for c in contexts for u in c.correction['logical_listing_line_index'] if u.get('complete_in_segment') is False}, 'Incomplete formatted groups require explicit same-number joins')
    need(supplied=={(c.name,id) for c in contexts for id in c.groups},
         'Every formatted source context must belong to exactly one program')


def finish(recipe,package,correction,contexts):
    joins=[]
    for p in recipe['formatted_programs']:
        for left,right,j in zip(p['parts'][:-1],p['parts'][1:],p['joins'],strict=True):
            joins.append(dict(program_id=p['id'],left_segment=left['segment'],right_segment=right['segment'],**deepcopy(j)))
    allowed={(j['program_id']+':n'+str(j['left_last']),j['left_segment'],j['right_segment']):j for j in joins if j['kind']=='same-number'}
    combined=[];by_id={}
    for source in correction['logical_listing_line_index']:
        row=deepcopy(source);id=row['line_id']
        if id not in by_id:
            row['source_fragments']=[deepcopy(source)];row['complete_in_article']=True
            row.pop('complete_in_segment',None);row.pop('incoming_fragment',None)
            combined.append(row);by_id[id]=row
        else:
            left=by_id[id];key=id,left['source_fragments'][-1]['source_segment'],row['source_segment']
            need(key in allowed and left[END]==row[START], 'Duplicate formatted group lacks one explicit contiguous same-number join')
            need(left['logical_text']+row['logical_text']==allowed[key]['joined_reading'], 'Formatted joined reading changed')
            offset=len(left['logical_text']);parts=deepcopy(row['source_parts'])
            for part in parts:part['start_character']+=offset;part['end_character']+=offset
            left['source_parts']+=parts;left['physical_line_ids']+=row['physical_line_ids'];left['segments']+=row['segments'];left['block_ids']=list(dict.fromkeys(left['block_ids']+row['block_ids']));left['logical_text']+=row['logical_text'];left[END]=row[END];left['source_fragments'].append(deepcopy(source))
    correction['logical_listing_line_index']=combined
    listing=b''.join(c.listing for c in contexts)
    need([id for u in combined for id in u['physical_line_ids']]==[r['line_id'] for r in correction['listing_line_index']],
         'Assembled formatted groups lose physical source rows')
    for u in combined:checked_span(listing,u[START],u[END],u['logical_text'])
    groups=[]
    for p in recipe['formatted_programs']:
        parts=[r for r in correction['listing_groups'] if r['listing_id']==p['id']]
        units=[u for u in combined if u['listing_id']==p['id']];numbers=[u['printed_line'] for u in units]
        need(numbers==sorted(set(numbers)), 'Formatted program numbers must be unique and increasing')
        groups.append(dict(listing_id=p['id'],line_kind='formatted-basic-numbered',block_ids=[id for r in parts for id in r['block_ids']],observed_printed_rows=numbers,complete=True,execute_verified=False,source_parts=deepcopy(parts)))
    correction['listing_groups']=groups
    resolved=[];boundary_keys={(j[side+'_segment'],j['outgoing_association' if side=='left' else 'incoming_association']) for j in joins for side in ('left','right')}
    seen_boundaries=set()
    for row in correction['content_associations']:
        k=row['kind'];program=row.get('listing_id');original=deepcopy(row)
        if k in ('source-control-target','source-comment-line-reference'):
            target=f'{program}:n{row["target_printed_row"]}'
            need(target in by_id and row.get('target_source_unit_id') in (None,target), 'Formatted reference target differs from declared program source')
            row.update(target_source_unit_id=target,pending_source_folios=[],target_complete_in_article=True)
        elif k=='source-explanation-listing-reference':
            targets=[f'{program}:n{n}' for n in row['printed_rows']]
            need(all(id in by_id for id in targets) and set(row['source_unit_ids'])<=set(targets),
                 'Formatted explanation refers to absent or wrong-program source units')
            row.update(source_unit_ids=targets,pending_printed_rows=[],pending_source_folios=[],restoration_coverage='complete in assembled article')
        elif k in ('source-listing-continuation','source-incoming-listing-boundary'):
            index=int(row['source_ref']['pointer'].rsplit('/',1)[1]);key=row['source_segment'],index
            need(key in boundary_keys,'Formatted continuation lacks explicit boundary review');seen_boundaries.add(key)
            row.update(kind='resolved-'+k,pending_source_folios=[],whole_article_assembly_pending=False,logical_group_complete=True)
        elif k=='source-listing-ending':row['whole_article_assembly_pending']=False
        if row!=original:resolved.append(dict(kind=k,source=deepcopy(row['source_ref']),source_values_changed=False,execute_verified=False))
    need(seen_boundaries==boundary_keys,'Formatted boundary declaration was not used')
    correction['formatted_program_joins']=joins
    correction['formatted_reference_resolutions']=resolved
    validate_active(package,correction)


def validate_active(package,correction):
    """Close new typed references; original source records remain under source_ref."""
    units={r['line_id'] for r in correction['logical_listing_line_index']};physical={r['line_id'] for r in correction['listing_line_index']}
    blocks={b['id'] for b in package['blocks']};regions={r['id'] for r in package['regions']};figures={f['id'] for f in package['figures']}
    run_ids=[r['run_id'] for r in correction['source_literal_index'] if 'run_id' in r]
    runs=set(run_ids)
    need(len(runs)==len(run_ids),'Repeated formatted display-run identity')
    labels={r['label_id'] for r in correction['figure_label_index']}
    singles={**{k:units for k in UNIT_KEYS},**{k:blocks for k in BLOCK_KEYS},**{k:regions for k in REGION_KEYS},'source_figure_id':figures}
    lists={**{k:units for k in UNIT_LISTS},**{k:regions for k in REGION_LISTS},'display_run_ids':runs,'asterisk_physical_line_ids':physical,'annotation_label_ids':labels}
    def walk(v):
        if isinstance(v,list):
            for x in v:walk(x)
        elif isinstance(v,dict):
            for k,x in v.items():
                if k in ('source_ref','source_fragments'):continue
                if k in singles and x is not None:need(x in singles[k],'Dangling formatted reference: '+k)
                if k in lists:need(set(x)<=lists[k],'Dangling formatted reference list: '+k)
                walk(x)
    for key in ('content_associations','source_literal_index','source_uncertainties','figure_associations'):walk(correction[key])
    for f in correction['figure_structures']:
        slots={s['slot_id'] for s in f.get('byte_slots',[])};nodes={n['node_id'] for n in f.get('nodes',[])}|{n['junction_id'] for n in f.get('junctions',[])}
        def closure(v):
            if isinstance(v,list):
                for x in v:closure(x)
            elif isinstance(v,dict):
                for k,x in v.items():
                    if k in ('label_id','from_label_id','branch_label_id') and x is not None:need(x in labels,'Dangling formatted diagram label')
                    if k in ('slot_ids','from_slot_ids'):need(set(x)<=slots,'Dangling memory slots')
                    if k in ('from_slot_id','to_slot_id','through_slot_id'):need(x in slots,'Dangling memory slot')
                    if k in ('from_id','to_id'):need(x in nodes,'Dangling flow connector')
                    if k=='node_ids':need(set(x)<=nodes,'Dangling flow zone')
                    closure(x)
        closure(f)
