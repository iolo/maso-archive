"""Opt-in v3 projection for command formats, visual slots and reviewed references.

Original source metadata is immutable. Coordinates declare their download owner;
physical field offsets remain row-local. No source/program byte inference occurs.
"""
from copy import deepcopy
import re

from .assemble import rebase
from .assembly_structured import checked_span, START as S, END as E

BLOCKS={'heading_block_id','body_block_id','transcription_block_id','format_block_id','format_id'}
BLOCK_LISTS={'caption_block_ids','transcription_block_ids'}
REGIONS={'transcription_region_id'}
LOCAL={'cell_id','slot_id','terminator_cell_id','field_id','command_id','token_id','connector_id','delimiter_id','footnote_id','from_label_id'}
LOCAL_LISTS={'cell_ids','slot_ids','stacked_control_slot_ids','zero_slot_ids','label_ids','footnote_ids','physical_row_ids','subareas'}


def need(condition,message):
    if not condition:raise ValueError('Structured source v3: '+message)


def validate_links(recipe):
    need(not any(recipe.get(k) for k in ('program_links','group_links','example_links')),
         'v3 projects disjoint program contexts; use existing modes for program joins')
    links=recipe.get('reference_links');need(isinstance(links,list),'reference_links must be explicit')
    names={s['name'] for s in recipe['segments']};seen=set()
    for link in links:
        need(isinstance(link,dict) and set(link)=={'kind','source','target','evidence'},'invalid reviewed reference link')
        need(link['kind'] in ('listing','units','sections') and isinstance(link['evidence'],str) and link['evidence'].strip(),'reference kind/evidence missing')
        source,target=link['source'],link['target']
        need(isinstance(source,dict) and set(source) in ({'segment','association','literal'},{'segment','association','literal','context'}) and source['segment'] in names and
             type(source['association']) is int and source['association']>=0 and isinstance(source['literal'],str) and source['literal'],
             'invalid source reference occurrence')
        if 'context' in source:
            c=source['context'];need(isinstance(c,dict) and set(c)=={'block_id','start_byte','end_byte','literal'} and
                isinstance(c['block_id'],str) and isinstance(c['literal'],str) and c['literal'] and
                type(c['start_byte']) is int and type(c['end_byte']) is int and 0<=c['start_byte']<c['end_byte'],
                'invalid expanded source reference context')
        key=(source['segment'],source['association']);need(key not in seen,'repeated reference occurrence');seen.add(key)
        extra={'units':'source_unit_ids','sections':'section_labels'}.get(link['kind'])
        need(isinstance(target,dict) and set(target)==({'segment','listing_id'}|({extra} if extra else set())) and target['segment'] in names and
             isinstance(target['listing_id'],str) and target['listing_id'],'invalid reference target')
        if extra:need(isinstance(target[extra],list) and target[extra] and all(isinstance(v,str) and v for v in target[extra]) and
                      len(set(target[extra]))==len(target[extra]),'invalid reference target members')


def reference(context,key,value):
    if value is None:return False,None
    if key in BLOCKS:return True,context.block(value)
    if key in BLOCK_LISTS:return True,[context.block(v) for v in value]
    if key in REGIONS:return True,context.identity(value,context.regions)
    if key=='source_region_ids':return True,[context.identity(v,context.regions) for v in value]
    if key in LOCAL:return True,context.name+':'+value
    if key in LOCAL_LISTS:return True,[context.name+':'+v for v in value]
    if key=='strip_id':return True,context.identity(value,context.tables)
    if key=='inspection_transform':
        need(isinstance(value,dict) and set(value)=={'path','sha256','bytes'},'invalid original review pin')
        return True,dict(scope='original-private-review',source_segment=context.name,original_pin=deepcopy(value),
                         corrections=rebase(context.source['corrections'][0],context.prefix))
    return False,None


def figure_nodes(figure):
    nodes={v['node_id'] for v in figure.get('nodes',[])}
    nodes.update(v['slot_id'] for v in figure.get('file_slots',[]))
    for node in figure.get('nodes',[]):nodes.update(node.get('subareas',[]))
    return nodes


def validate_source(context):
    """Validate graph endpoints in their owning figure before adding namespaces."""
    labels={v['label_id'] for v in context.correction.get('figure_label_index',[])}
    all_nodes=set()
    for figure in context.correction.get('figure_structures',[]):
        declared=[v['node_id'] for v in figure.get('nodes',[])]+[v['slot_id'] for v in figure.get('file_slots',[])]
        declared += [s for v in figure.get('nodes',[]) for s in v.get('subareas',[])]
        need(len(declared)==len(set(declared)),'duplicate figure node/slot/subarea')
        nodes=set(declared)
        need(not nodes & all_nodes,'figure node identities collide within a source segment');all_nodes.update(nodes)
        def walk(value):
            if isinstance(value,list):
                for v in value:walk(v)
            elif isinstance(value,dict):
                for key,item in value.items():
                    if key in ('from_node','to_node'):need(item in nodes,'figure connector leaves its declared nodes/slots/subareas')
                    if key in ('label_id','from_label_id') and item is not None:need(item in labels,'figure label is absent')
                    if key=='label_ids':need(set(item)<=labels,'figure label list is absent')
                    if isinstance(item,(dict,list)):walk(item)
        walk(figure)


def project_index(context,key,source,target,ranges):
    """Project each explicit coordinate system independently, including nested spans."""
    physical={v['line_id']:v for v in context.correction.get('listing_line_index',[])}
    logical={v['line_id']:v for v in context.correction.get('logical_listing_line_index',[])}
    if key=='listing_caption_associations':
        caption=source['caption_block_id'];block=context.blocks[caption]
        need(source['caption_literal']==block['text'] and source.get('caption_region_id') in block['region_ids'],
             'whole listing caption differs from its actual source block')
        target['block_id']=context.block(caption)
    def owner_of(value,owner):
        current=value.get('block_id',value.get('code_block_id',owner))
        if current is None and value.get('listing_id') is not None:current=context.code_block(value['listing_id'])
        if current is None and value.get('source_unit_id') is not None:
            unit=logical.get(value['source_unit_id']);need(unit is not None,'coordinate owner has no source unit');current=unit['block_id']
        return current
    def walk(original,revised,owner=None,path=(),inherited_download=None):
        if isinstance(original,list):
            need(len(original)==len(revised),'projection changed list membership')
            for a,z in zip(original,revised,strict=True):walk(a,z,owner,path,inherited_download)
            return
        if not isinstance(original,dict):return
        current=owner_of(original,owner)
        selected_download=original.get('download',inherited_download)
        if key=='listing_caption_associations' and not path:current=source['caption_block_id']
        if path and path[-1]=='source_parts' and key=='logical_listing_line_index':
            row=physical.get(original.get('line_id'))
            need(row is not None and original['line_id'] in source['physical_line_ids'] and original.get('region_id',row['region_id'])==row['region_id'],
                 'logical source part has a wrong physical owner')
            a,z=original['start_character'],original['end_character'];value=row['text'].removesuffix('\n')
            need(type(a) is int and type(z) is int and source['logical_text'][a:z]==value and z-a==len(value),
                 'logical source character positions differ from physical text')
            need(original.get('physical_start_byte',row[S])==row[S],'logical physical byte address differs')
            revised['physical_start_byte']=row[S]+context.offset
        row_field=key=='listing_line_index' and path and path[-1]=='fields'
        literal=original.get('literal',original.get('text',original.get('separator')))
        has_span='start_byte' in original or 'end_byte' in original
        has_download=S in original or E in original
        if row_field:
            need(current in context.blocks,'physical field lacks its code block')
            a,z=original['start_byte'],original['end_byte'];checked_span(source['text'].encode(),a,z,literal)
            need((original['block_start_byte'],original['block_end_byte'])==(source['block_start_byte']+a,source['block_start_byte']+z),
                 'physical field row/block coordinates disagree')
            need((original[S],original[E])==(source[S]+a,source[S]+z),'physical field row/listing coordinates disagree')
            within=context.positions[context.identity(current,context.blocks)][1]
            revised.update(download='listing.txt',block_start_byte=original['block_start_byte']+within,
                           block_end_byte=original['block_end_byte']+within,**{S:original[S]+context.offset,E:original[E]+context.offset})
        elif has_span or has_download:
            need(current in context.blocks,'span lacks an explicit source block owner')
            data=context.blocks[current]['text'].encode();kind=context.blocks[current]['kind']
            download=selected_download or 'article.txt'
            need(download in ('article.txt','listing.txt'),'unknown span download owner')
            need(not has_span or 'start_byte' in original and 'end_byte' in original,'incomplete local span')
            need(not has_download or S in original and E in original,'incomplete download span')
            code_base=next((v[S] for v in context.correction['listing_index'] if v['block_id']==current),None)
            if download=='listing.txt':
                need(kind=='code' and code_base is not None,'listing span owned by prose')
                a=original.get('block_start_byte',original.get('start_byte',original.get(S))-code_base)
                z=original.get('block_end_byte',original.get('end_byte',original.get(E))-code_base)
                need(not has_span or (original['start_byte'],original['end_byte'])==(code_base+a,code_base+z),
                     'listing local span and code-block coordinates disagree')
                need(not has_download or (original[S],original[E])==(code_base+a,code_base+z),'listing span coordinates disagree')
                checked_span(data,a,z,literal)
                target_block,within=context.positions[context.identity(current,context.blocks)]
                revised.update(download=download,block_id=target_block,block_start_byte=a+within,block_end_byte=z+within,
                               **{S:code_base+a+context.offset,E:code_base+z+context.offset})
                if has_span:revised.update(start_byte=code_base+a+context.offset,end_byte=code_base+z+context.offset)
            else:
                base=context.ranges[current][0]
                a=original['start_byte'] if has_span else original[S]-base
                z=original['end_byte'] if has_span else original[E]-base
                need(not has_download or (original[S],original[E])==(base+a,base+z),'article span coordinates disagree')
                checked_span(data,a,z,literal);target_block,within=context.positions[context.identity(current,context.blocks)]
                revised.update(download=download,block_id=target_block,start_byte=a+within,end_byte=z+within,
                               **{S:ranges[target_block][0]+within+a,E:ranges[target_block][0]+within+z})
        for field,value in original.items():
            if field not in revised or field in ('source_ref','evidence','inspection_transform'):continue
            if isinstance(value,(dict,list)):
                child_owner=source['caption_block_id'] if key=='listing_caption_associations' and field=='caption_source_segments' else current
                walk(value,revised[field],child_owner,path+(field,),selected_download)
    walk(source,target)


def finish(recipe,package,correction,contexts):
    """Resolve only reviewed reference occurrences and source-declared article scope."""
    by_name={c.name:c for c in contexts}
    projected={(v['source_segment'],v['source_ref']['pointer']):v for v in correction['content_associations']}
    expected={(c.name,i) for c in contexts for i,v in enumerate(c.correction['content_associations']) if v.get('kind')=='source-pending-listing-reference'}
    supplied={(v['source']['segment'],v['source']['association']) for v in recipe['reference_links']}
    need(expected==supplied,'reviewed links must cover every pending listing occurrence once')
    for link in recipe['reference_links']:
        s,t=link['source'],link['target'];context=by_name[t['segment']]
        source=by_name[s['segment']].correction['content_associations'][s['association']]
        need(source['literal']==s['literal'] and source['target_native_unit_id'] is None and source['target_verified'] is False,
             'reviewed link differs from its immutable pending occurrence')
        reference_literal=s['literal'];expanded=None
        if 'context' in s:
            expanded=s['context'];origin=by_name[s['segment']]
            need(expanded['block_id']==source['block_id'] and expanded['start_byte']<=source['start_byte']<source['end_byte']<=expanded['end_byte'],
                 'expanded reference does not contain its original occurrence')
            checked_span(origin.blocks[expanded['block_id']]['text'].encode(),expanded['start_byte'],expanded['end_byte'],expanded['literal'])
            reference_literal=expanded['literal']
        need(t['listing_id'] in context.groups,'reference targets an absent listing')
        folios={str(v['printed_page']) for v in context.source['pages']}
        need(set(map(str,source['target_source_folios']))<=folios,'listing reference target source folios not covered')
        units={v['line_id']:v for v in context.correction['logical_listing_line_index'] if v['listing_id']==t['listing_id']}
        sections={v['section_label']:v for v in context.correction['content_associations'] if v.get('kind')=='source-program-section' and v['listing_id']==t['listing_id']}
        ids=[];labels=[]
        if link['kind']=='units':
            ids=t['source_unit_ids'];need(set(ids)<=units.keys(),'reference targets an absent source unit')
            numbers=[units[id]['printed_line'] for id in ids];printed=list(map(int,re.findall(r'\d+',reference_literal)))
            if len(printed)==1:need(numbers==printed,'unit link changes the printed row reference')
            else:need(len(printed)==2 and numbers==[v['printed_line'] for v in units.values() if printed[0]<=v['printed_line']<=printed[1]],'range link changes source endpoints/membership')
        elif link['kind']=='sections':
            labels=t['section_labels'];need(set(labels)<=sections.keys(),'reference targets an absent source section')
            printed=re.fullmatch(r'리스팅\s*(\d+)',reference_literal)
            need(printed and len(labels)==1 and re.search(r'(?:^|-)'+printed[1]+r'$',labels[0]),'section link differs from printed example number')
            ids=sections[labels[0]]['source_unit_ids']
        else:need(re.fullmatch(r'리스트\s*1',reference_literal) is not None,'whole-listing reference lacks its source declaration')
        active=projected[(s['segment'],f'/content_associations/{s["association"]}')]
        active.update(kind='resolved-source-listing-reference',target_listing_id=context.listing_ids[t['listing_id']],
                      target_source_unit_ids=[context.name+':'+v for v in ids],target_section_labels=labels,
                      target_verified=True,meaning_verified=False,resolution_evidence=link['evidence'])
        if expanded:
            origin=by_name[s['segment']];block=origin.block(expanded['block_id']);a,z=expanded['start_byte'],expanded['end_byte']
            from .assembly_indexes import block_ranges
            base=block_ranges(package)[block][0]
            active['expanded_source_reference']=dict(block_id=block,literal=expanded['literal'],start_byte=a,end_byte=z,
                download='article.txt',**{S:base+a,E:base+z},source_segment=s['segment'],
                original_source_range=dict(source_block_id=expanded['block_id'],source_start_byte=a,source_end_byte=z,source_literal=expanded['literal']),
                reason='Reviewed context qualifies a partial original marker; frozen marker and source text remain unchanged.')
        # Keep the original null field as history; the plural active field owns every selected target.
    actual=[str(v['printed_page']) for v in package['pages']]
    for context in contexts:
        for i,source in enumerate(context.correction['content_associations']):
            if source.get('kind') not in ('article-segment-continuation','article-segment-assembly-required'):continue
            a,z=source['whole_source_extent'];need(actual==list(map(str,range(a,z+1))),'article completion differs from source-declared whole extent')
            local=[str(v['printed_page']) for v in context.source['pages']]
            need(list(map(str,source.get('source_folios',source.get('selected_folios'))))==local,'segment completion differs from local source coverage')
            other={str(p['printed_page']) for c in contexts if c.name!=context.name for p in c.source['pages']}
            declared=source.get('pending_source_folios',source.get('opening_segment_folios'))
            need(set(map(str,declared))==other and source['whole_article_assembly_required'] is True and source['source_absence_claim'] is False,
                 'segment completion has inconsistent pending source coverage')
            active=projected[(context.name,f'/content_associations/{i}')]
            active.update(kind='resolved-article-segment',whole_article_assembly_required=False,whole_article_complete=True)
            if 'pending_source_folios' in active:active['pending_source_folios']=[]
    validate_active(correction,package)


def validate_active(correction,package):
    """Close the v3 vocabulary against real active definitions, not ID-like strings."""
    blocks={v['id'] for v in package['blocks']};regions={v['id'] for v in package['regions']}
    labels={v['label_id'] for v in correction['figure_label_index']};cells=set();slots=set();fields=set();footnotes=set();rows=set();commands=set();tokens=set();delimiters=set()
    def define(values,items,kind):
        items=list(items);need(len(items)==len(set(items)) and not values & set(items),'duplicate '+kind+' definition');values.update(items)
    for table in correction['tables']:
        for row in table['rows']:
            define(rows,[row['row_id']],'row');define(cells,(v['cell_id'] for v in row['cells'] if 'cell_id' in v),'cell')
        define(footnotes,(v['footnote_id'] for v in table.get('footnotes',[])),'footnote')
    for figure in correction['figure_structures']:
        slots.update(v['slot_id'] for v in figure.get('file_slots',[]));fields.update(v['field_id'] for v in figure.get('fields',[]))
        define(delimiters,(v['delimiter_id'] for v in figure.get('delimiters',[])),'delimiter')
    for group in correction['content_associations']:
        if group.get('kind')!='source-command-format-group':continue
        define(rows,(v['row_id'] for v in group['physical_rows']),'command row')
        define(commands,(v['command_id'] for v in group['commands']),'command')
        define(tokens,(v['token_id'] for v in group['commands'] for v in v['tokens']),'command token')
    singles={**{k:blocks for k in BLOCKS},**{k:regions for k in REGIONS},'cell_id':cells,'slot_id':slots,
             'terminator_cell_id':cells,'field_id':fields,'command_id':commands,'token_id':tokens,
             'footnote_id':footnotes,'from_label_id':labels,'row_id':rows,'delimiter_id':delimiters,
             'strip_id':{v['table_id'] for v in correction['tables']},'target_listing_id':{v['listing_id'] for v in correction['listing_groups']}}
    lists={**{k:blocks for k in BLOCK_LISTS},'source_region_ids':regions,'cell_ids':cells,'slot_ids':cells,'stacked_control_slot_ids':cells,'zero_slot_ids':cells,
           'label_ids':labels,'footnote_ids':footnotes,'physical_row_ids':rows,
           'target_source_unit_ids':{v['line_id'] for v in correction['logical_listing_line_index']}}
    def walk(value):
        if isinstance(value,list):
            for v in value:walk(v)
        elif isinstance(value,dict):
            for key,item in value.items():
                if key in ('source_ref','original_metadata','inspection_transform','evidence'):continue
                if key in singles and item is not None:need(item in singles[key],'dangling active '+key)
                if key in lists:need(set(item)<=lists[key],'dangling active '+key)
                if isinstance(item,(dict,list)):walk(item)
    from .assembly_structured import INDEXES
    for key in INDEXES:walk(correction[key])
