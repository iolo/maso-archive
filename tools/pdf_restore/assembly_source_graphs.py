"""Opt-in v4: scoped source graphs, wire endpoints and non-mutating prose links.

Original segments and selected code bytes remain immutable. Explicit source
namespaces, physical observations and reviewed occurrences establish identity;
this module does not infer circuit correctness or executable program bytes.
"""
from copy import deepcopy
import re

from .assemble import rebase
from .assembly_structured import (BLOCK_KEYS, BLOCK_LISTS, REGION_KEYS, FIGURE_KEYS,
                                  LOCAL_KEYS, checked_span, START as S, END as E)
from .assembly_source_structures import project_index


def need(condition, message):
    if not condition:raise ValueError('Structured source v4: '+message)


def validate_links(recipe):
    need(all(recipe.get(k)==[] for k in ('program_links','group_links','example_links',
                                        'reference_links','prose_joins','relationship_links')),
         'scoped graph mode requires disjoint contexts and explicit non-mutating links')
    for key in ('paragraph_links','figure_links'):
        need(isinstance(recipe.get(key),list),key+' must be explicit')
    names={v['name'] for v in recipe['segments']};seen=set()
    def occurrence(value):
        need(isinstance(value,dict) and set(value)=={'segment','association','literal'} and
             value['segment'] in names and type(value['association']) is int and value['association']>=0 and
             isinstance(value['literal'],str) and value['literal'],'invalid reviewed occurrence')
    for link in recipe['paragraph_links']:
        need(isinstance(link,dict) and set(link)=={'id','left','right','declaration','separator','evidence'},'invalid paragraph link')
        need(isinstance(link['id'],str) and link['id'] and link['id'] not in seen,'duplicate paragraph link');seen.add(link['id'])
        occurrence(link['left']);occurrence(link['right']);d=link['declaration']
        need(isinstance(d,dict) and set(d)=={'segment','association'} and d['segment'] in names and
             type(d['association']) is int and d['association']>=0,'invalid paragraph declaration')
        need(link['left']['segment']!=link['right']['segment'] and link['separator']=='' and
             isinstance(link['evidence'],str) and link['evidence'].strip(),'paragraph boundary/evidence missing')
    seen=set()
    for link in recipe['figure_links']:
        need(isinstance(link,dict) and set(link)=={'source','targets','unresolved_numbers','evidence'},'invalid figure link')
        occurrence(link['source']);key=(link['source']['segment'],link['source']['association'])
        need(key not in seen,'duplicate figure occurrence');seen.add(key)
        need(isinstance(link['targets'],list) and link['targets'] and isinstance(link['unresolved_numbers'],list) and
             all(type(n) is int and n>=0 for n in link['unresolved_numbers']) and
             isinstance(link['evidence'],str) and link['evidence'].strip(),'invalid figure disposition')
        for target in link['targets']:
            need(isinstance(target,dict) and set(target)=={'printed_number','segment','figure_id','caption_block_id'} and
                 type(target['printed_number']) is int and target['printed_number']>=0 and target['segment'] in names and
                 all(isinstance(target[k],str) and target[k] for k in ('figure_id','caption_block_id')),'invalid caption target')


class Registry:
    """Canonical definitions, with graph and figure scopes retained separately."""
    def __init__(self,context):
        self.context=context;self.maps={};self.graphs={};self.figures=context.figures
        c=context.correction
        self.locals={
            'label':{v['label_id'] for v in c.get('figure_label_index',[])},
            'cell':{v['cell_id'] for t in c.get('tables',[]) for row in t['rows'] for v in row['cells'] if 'cell_id' in v},
            'row':{row['row_id'] for t in c.get('tables',[]) for row in t['rows']},
            'paragraph':{v['paragraph_id'] for v in c.get('content_associations',[]) if 'paragraph_id' in v},
            'entry':{v['entry_id'] for v in c.get('content_associations',[]) if 'entry_id' in v},
            'byline':{v['byline_id'] for v in c.get('content_associations',[]) if 'byline_id' in v},
            'format':{v['format_id'] for v in c.get('content_associations',[]) if 'format_id' in v},
            'token':set(), 'command':set(), 'footnote':set(), 'delimiter':set()}
        def define_local(kind,values):
            for value in values:
                need(value not in self.locals[kind],'duplicate '+kind+' definition');self.locals[kind].add(value)
        for v in c.get('basic_source_fields',[]):
            if 'token_id' in v:define_local('token',[v['token_id']])
        for v in c.get('content_associations',[]):
            commands=v.get('commands',[]) if v.get('kind')=='source-command-format-group' else [v] if v.get('kind')=='source-command-example' else []
            if v.get('kind')=='source-command-format-group':define_local('row',[r['row_id'] for r in v['physical_rows']])
            for command in commands:
                if 'command_id' in command:define_local('command',[command['command_id']])
                define_local('token',[t['token_id'] for t in command.get('tokens',[])])
        for table in c.get('tables',[]):define_local('footnote',[f['footnote_id'] for f in table.get('footnotes',[])])
        for figure in c.get('figure_structures',[]):
            fid=figure['figure_id'];need(fid in context.figures,'unknown source figure')
            self.add_nodes(fid,None,figure.get('nodes',[]),figure.get('subareas',[]))
            for key,kind in [('graphs','graph'),('sequences','sequence')]:
                for graph in figure.get(key,[]):
                    gid=graph[kind+'_id'];scope=(kind,gid);self.add(kind,fid,None,gid)
                    self.add_nodes(fid,scope,graph.get('nodes',[]),graph.get('subareas',[]))
                    for edge in graph.get('edges',[]):self.add('edge',fid,scope,edge['edge_id'])
            for edge in figure.get('edges',[]):self.add('edge',fid,None,edge['edge_id'])
            for key,kind,idkey in [('terminals','terminal','terminal_id'),('source_fields','field','field_id'),('fields','field','field_id'),
                                   ('wires','wire','wire_id'),('bus_elisions','bus','bus_id'),('crossings','crossing','crossing_id')]:
                for value in figure.get(key,[]):self.add(kind,fid,None,value[idkey])
            for value in figure.get('components',[]):
                self.add('component',fid,None,value['component_id'])
                for port in value['ports']:self.add('port',fid,None,port['port_id'])
            define_local('delimiter',[v['delimiter_id'] for v in figure.get('delimiters',[])])
        self.validate_definitions()

    def add(self,kind,figure,scope,value):
        need(isinstance(value,str) and value,'blank '+kind+' identity')
        values=self.maps.setdefault(kind,{});key=(figure,scope,value)
        need(key not in values,'duplicate '+kind+' definition')
        prefix=self.context.name+':'+figure+':'
        if scope:prefix+=scope[0]+':'+scope[1]+':'
        values[key]=prefix+kind+':'+value

    def add_nodes(self,figure,scope,nodes,subareas):
        for node in nodes:self.add('node',figure,scope,node['node_id'])
        for subarea in subareas:
            need(isinstance(subarea,dict) and 'subarea_id' in subarea,'invalid graph subarea')
            self.add('node',figure,scope,subarea['subarea_id'])

    def get(self,kind,value,figure=None,scope=None):
        matches=[v for (f,s,k),v in self.maps.get(kind,{}).items() if k==value and
                 (figure is None or f==figure) and s==scope]
        need(len(matches)==1,'unknown or ambiguous '+kind+' reference: '+str(value));return matches[0]

    def local(self,kind,value):
        need(value in self.locals[kind],'unknown '+kind+' reference: '+str(value));return self.context.name+':'+value

    def validate_definitions(self):
        c=self.context.correction
        need(len(self.locals['label'])==len(c.get('figure_label_index',[])),'duplicate figure label')
        for figure in c.get('figure_structures',[]):
            fields={v['field_id']:v for v in figure.get('source_fields',[])}
            for part in figure.get('components',[]):
                for port in part['ports']:
                    for key,valuekey in [('label_field_id','printed_label'),('pin_field_id','printed_pin')]:
                        if key in port:need(port[key] in fields and fields[port[key]]['literal']==port[valuekey],'printed terminal differs from its source field')
        for kind,key in [('cell','cell_id'),('row','row_id')]:
            values=[v[key] for table in c.get('tables',[]) for row in table['rows'] for v in ([row] if kind=='row' else row['cells']) if key in v]
            need(len(values)==len(set(values)),'duplicate source '+kind)


def prepare_context(context):
    context.graph_registry=Registry(context)
    context.command_physical=[];context.command_logical=[];context.command_origins={}
    physical=context.correction['listing_line_index'];logical=context.correction['logical_listing_line_index']
    for group in context.groups.values():
        if group.get('line_kind')!='unnumbered-command-example':continue
        listing=group['listing_id'];block=context.code_block(listing);text=context.blocks[block]['text'];data=text.encode()
        need(not any(v['listing_id']==listing for v in physical+logical),'command row derivation would duplicate source rows')
        matches=[(i,v) for i,v in enumerate(context.correction['content_associations']) if v.get('kind')=='source-command-example' and v.get('listing_id')==listing]
        need(len(matches)==1,'unnumbered context lacks its unique source command');index,source=matches[0]
        need(source['block_id']==block and source['literal']==text and source.get('start_byte')==0 and source.get('end_byte')==len(data) and
             text and '\n' not in text and source.get('execute_verified') is False and group.get('complete') is True,
             'command rows require one complete observed source command line')
        base=next(v[S] for v in context.correction['listing_index'] if v['listing_id']==listing)
        rid=context.blocks[block]['region_ids'];need(len(rid)==1,'command row requires one mapped source region')
        pid=listing+':derived-physical';uid=listing+':derived-command'
        row=dict(line_id=pid,source_unit_id=uid,listing_id=listing,block_id=block,region_id=rid[0],scan=context.assets[rid[0]],
                 text=text,printed_line=None,row_kind='derived-source-command-row',physical_continuation=False,
                 block_start_byte=0,block_end_byte=len(data),download='listing.txt',fields=[],**{S:base,E:base+len(data)})
        unit=dict(line_id=uid,listing_id=listing,block_id=block,printed_line=None,line_kind='derived-source-command-unit',
                  physical_line_ids=[pid],logical_text=text,execute_verified=False,download='listing.txt',
                  segments=[dict(region_id=rid[0],scan=context.assets[rid[0]],**{S:base,E:base+len(data)})],**{S:base,E:base+len(data)})
        context.command_physical.append(row);context.command_logical.append(unit);context.command_origins[listing]=index
    # Close every original typed reference before active projection.
    for key in ('figure_structures','figure_label_index','figure_associations','content_associations','source_uncertainties','inline_source_fields','basic_source_fields'):
        references(context,context.correction.get(key,[]))


def references(context,value,figure=None,scope=None):
    registry=context.graph_registry
    if isinstance(value,list):return [references(context,v,figure,scope) for v in value]
    if not isinstance(value,dict):return deepcopy(value)
    if 'figure_id' in value:
        if figure!=value['figure_id']:scope=None
        figure=value['figure_id']
    if 'graph_id' in value:scope=('graph',value['graph_id'])
    if 'sequence_id' in value:scope=('sequence',value['sequence_id'])
    result={}
    block_keys=BLOCK_KEYS|{'heading_block_id','body_block_id','transcription_block_id','format_block_id','source_last_block_id','to_block_id'}
    block_lists=BLOCK_LISTS|{'caption_block_ids','transcription_block_ids'}
    region_keys=REGION_KEYS|{'transcription_region_id','physical_geometry_source_region_id'}
    node_keys={'node_id','from_node','to_node','from_node_id','to_node_id','label_node_id','target_node_id','subarea_id'}
    fig_kinds={'component_id':'component','terminal_id':'terminal','field_id':'field','wire_id':'wire','crossing_id':'crossing','bus_id':'bus'}
    field_refs={'model_field_id','model_field_id_secondary','polarity_field_id','label_field_id','pin_field_id','source_field_id'}
    local_keys={'cell_id':'cell','owner_cell_id':'cell','parent_cell_id':'cell','row_id':'row','shared_bit_header_row_id':'row',
                'label_id':'label','from_label_id':'label','token_id':'token','command_id':'command','footnote_id':'footnote',
                'delimiter_id':'delimiter','entry_id':'entry','byline_id':'byline','paragraph_id':'paragraph'}
    local_lists={'child_cell_ids':'cell','cell_ids':'cell','source_row_ids':'row','physical_row_ids':'row','label_ids':'label',
                 'entry_ids':'entry','footnote_ids':'footnote'}
    def ports(item):
        return [ports(v) for v in item] if isinstance(item,list) else registry.get('port',item,figure)
    for key,item in value.items():
        if key in ('review_crop','source_context'):continue
        if key in ('source_ref','original_metadata','original_source_range') or key=='evidence' and isinstance(item,dict):result[key]=deepcopy(item);continue
        if item is None:result[key]=None;continue
        if key in block_keys:revised=context.block(item)
        elif key in block_lists:revised=[context.block(v) for v in item]
        elif key in region_keys:revised=context.identity(item,context.regions)
        elif key in ('region_ids','source_region_ids'):revised=[context.identity(v,context.regions) for v in item]
        elif key in FIGURE_KEYS|{'circuit_figure_id'}:revised=context.identity(item,context.figures)
        elif key=='figure_ids':revised=[context.identity(v,context.figures) for v in item]
        elif key=='table_id':revised=context.identity(item,context.tables)
        elif key=='table_ids':revised=[context.identity(v,context.tables) for v in item]
        elif key=='listing_id':context.identity(item,context.groups);revised=context.listing_ids[item]
        elif key in ('line_id','source_unit_id','physical_line_id','target_source_unit_id'):revised=context.name+':'+item
        elif key in ('physical_line_ids','source_unit_ids'):revised=[context.name+':'+v for v in item]
        elif key in node_keys:revised=registry.get('node',item,figure,scope)
        elif key in ('source_graph','target_graph'):revised=registry.get('graph',item,figure)
        elif key in ('source_node','target_node'):
            graph=value['source_graph' if key=='source_node' else 'target_graph'];revised=registry.get('node',item,figure,('graph',graph))
        elif key in ('graph_id','sequence_id'):revised=registry.get('graph' if key=='graph_id' else 'sequence',item,figure)
        elif key=='edge_id':revised=registry.get('edge',item,figure,scope)
        elif key in fig_kinds:revised=registry.get(fig_kinds[key],item,figure)
        elif key in field_refs:revised=registry.get('field',item,figure)
        elif key in ('component_ids','wire_ids'):revised=[registry.get('component' if key=='component_ids' else 'wire',v,figure) for v in item]
        elif key in ('port_id','source_endpoint','target_endpoint'):revised=registry.get('port',item,figure)
        elif key in ('endpoints','source_endpoints','target_endpoints','visible_terminal_pairs'):revised=ports(item)
        elif key in ('first_port','last_port'):revised=registry.get('port',item,figure)
        elif key in local_keys:revised=registry.local(local_keys[key],item)
        elif key in local_lists:revised=[registry.local(local_lists[key],v) for v in item]
        elif key=='format_id':revised=context.block(item) if item in context.blocks else registry.local('format',item)
        elif key=='scan':
            region=value.get('region_id',value.get('figure_region_id'));need(item in context.assets.values() and (region is None or item==context.assets.get(region)),'source scan differs from its region');revised=rebase(item,context.prefix)
        elif key=='inspection_transform':
            from .assembly_source_structures import reference
            _,revised=reference(context,key,item)
        else:
            from .assembly_source_indexes import reference
            handled,revised=reference(context,key,item)
            if handled:
                if revised is NotImplemented:continue
            else:revised=references(context,item,figure,scope)
        result[key]=revised
    return result


def append_command_rows(context,correction,ranges):
    for key,values in [('listing_line_index',context.command_physical),('logical_listing_line_index',context.command_logical)]:
        for original in values:
            row=context.refs(original);project_index(context,key,original,row,ranges)
            index=context.command_origins[original['listing_id']]
            row.update(source_segment=context.name,source_ref=context.source_ref('content_associations',index),
                       derivation=dict(kind='complete-source-command-example',source_association=index,printed_line_number_supplied=False))
            correction[key].append(row)


def finish(recipe,package,correction,contexts):
    """Qualify exact source declarations without merging or rewriting source blocks."""
    from .assembly_indexes import block_ranges
    contexts={v.name:v for v in contexts};active={(v['source_segment'],v['source_ref']['pointer']):v for v in correction['content_associations']}
    def source(spec):
        c=contexts[spec['segment']];rows=c.correction['content_associations'];i=spec['association']
        need(i<len(rows),'reviewed association is absent');row=rows[i]
        if 'literal' in spec:need(row.get('literal')==spec['literal'],'reviewed association literal differs')
        return c,row,active[(c.name,f'/content_associations/{i}')]
    def span(c,row):
        need(row.get('block_id') in c.blocks,'paragraph block is absent')
        checked_span(c.blocks[row['block_id']]['text'].encode(),row['start_byte'],row['end_byte'],row['literal'])
    expected={(c.name,i) for c in contexts.values() for i,v in enumerate(c.correction['content_associations']) if v.get('kind')=='source-prose-continuation-pending-assembly'};used=set()
    for link in recipe['paragraph_links']:
        left,l,la=source(link['left']);right,r,ra=source(link['right']);decl,d,da=source(link['declaration'])
        key=(decl.name,link['declaration']['association']);need(key in expected and key not in used,'paragraph declaration repeated or unrelated');used.add(key)
        need(l['kind']==r['kind']=='source-paragraph' and decl is right and
             (d['from_segment'],d['to_segment'])==(left.name,right.name) and d['source_absence_claim'] is False,
             'paragraph link differs from its source declaration')
        span(left,l);span(right,r)
        need(l['end_byte']==len(left.blocks[l['block_id']]['text'].encode()) and r['start_byte']==0 and
             l['literal'].endswith(d['from_literal']) and r['literal'].startswith(d['to_literal']) and
             r['block_id']==d['to_block_id'],'paragraph continuation endpoints differ')
        def folios(context,row):
            ids={v['region_id'] for v in row.get('source_segments',[]) if v.get('kind')!='editorial-continuation-separator'}
            numbers={v['source_index'] for v in context.source['regions'] if v['id'] in ids}
            return {int(v['printed_page']) for v in context.source['pages'] if v['source_index'] in numbers}
        need(d['from_folio'] in folios(left,l) and d['to_folio'] in folios(right,r) and
             d['intervening_figure_folios']==list(range(d['from_folio']+1,d['to_folio'])),
             'paragraph continuation source folios differ')
        order=package['content_order'];a=order.index(dict(type='block',id=la['block_id']));z=order.index(dict(type='block',id=ra['block_id']))
        need(a<z,'paragraph continuation runs backwards')
        aids={bid for c in contexts.values() for f in c.correction['figure_associations'] for bid in [c.block(v) for v in f.get('caption_block_ids',[])+f.get('transcription_block_ids',[])]}
        need(all(item['type']=='figure' or item['id'] in aids for item in order[a+1:z]),'paragraph continuation skips unrelated prose')
        da.update(kind='resolved-source-paragraph-continuation',logical_paragraph_id='assembly:paragraph:'+link['id'],
                  member_paragraph_ids=[la['paragraph_id'],ra['paragraph_id']],fragments=[deepcopy(la),deepcopy(ra)],
                  separator=link['separator'],logical_display=l['literal']+link['separator']+r['literal'],
                  source_blocks_unchanged=True,resolution_evidence=link['evidence'])
    need(used==expected,'paragraph links do not cover every pending source declaration')
    expected={(c.name,i) for c in contexts.values() for i,v in enumerate(c.correction['content_associations']) if v.get('kind')=='source-pending-figure-reference'};used=set()
    for link in recipe['figure_links']:
        origin,row,projected=source(link['source']);key=(origin.name,link['source']['association'])
        need(key in expected and key not in used,'figure occurrence repeated or unrelated');used.add(key)
        numbers=row['printed_figure_numbers'];need(list(map(int,re.findall(r'\d+',row['literal'])))==numbers,'figure numbers differ from the printed occurrence');selected=[v['printed_number'] for v in link['targets']];unresolved=link['unresolved_numbers']
        need(len(set(selected+unresolved))==len(selected+unresolved) and set(selected+unresolved)==set(numbers),
             'figure dispositions alter the printed numbers')
        targets=[]
        for target in link['targets']:
            c=contexts[target['segment']];fid=target['figure_id'];bid=target['caption_block_id'];c.identity(fid,c.figures);c.block(bid)
            matches=[v for v in c.correction['figure_associations'] if v['figure_id']==fid]
            need(len(matches)==1 and bid in matches[0]['caption_block_ids'],'caption is not associated with its target figure')
            text=c.blocks[bid]['text'];need(next(v for v in c.source['figures'] if v['id']==fid)['caption']==text,'figure display caption differs from its source');match=re.match(r'^그림\s*(\d+)(?:\s|[.．]|$)',text)
            need(match is not None and int(match[1])==target['printed_number'] and
                 text in matches[0]['caption_literals'],'target does not have its printed source caption')
            block=c.block(bid);base=block_ranges(package)[block][0]
            targets.append(dict(printed_number=target['printed_number'],figure_id=c.identity(fid,c.figures),caption_block_id=block,
                                caption_literal=text,download='article.txt',**{S:base,E:base+len(text.encode())},target_verified=True,meaning_verified=False))
        projected.update(kind='qualified-source-figure-reference',verified_target_figures=targets,unresolved_figure_numbers=unresolved,
                         target_verified=not unresolved,meaning_verified=False,resolution_evidence=link['evidence'],source_numbering_repaired=False)
    need(used==expected,'figure links do not cover every pending source occurrence')
    actual=[str(v['printed_page']) for v in package['pages']]
    for c in contexts.values():
        rows=[(i,v) for i,v in enumerate(c.correction['content_associations']) if v.get('kind') in ('article-segment-continuation','article-segment-assembly-required')]
        need(len(rows)==1,'each source segment needs one complete-article coverage declaration')
        i,row=rows[0];a,z=row['whole_source_extent'];local=[str(v['printed_page']) for v in c.source['pages']]
        declared=row.get('pending_source_folios',row.get('pending_folios',row.get('opening_segment_folios')))
        other={str(p['printed_page']) for context in contexts.values() if context is not c for p in context.source['pages']}
        need(actual==list(map(str,range(a,z+1))) and list(map(str,row.get('source_folios',row.get('selected_folios'))))==local and
             declared is not None and set(map(str,declared))==other and row['whole_article_assembly_required'] is True and
             row['source_absence_claim'] is False,'source whole-article coverage differs')
        updated=active[(c.name,f'/content_associations/{i}')]
        updated.update(kind='resolved-article-segment',whole_article_assembly_required=False,whole_article_complete=True)
        for key in ('pending_source_folios','pending_folios'):
            if key in updated:updated[key]=[]
    validate_active(correction,package)


def validate_active(correction,package):
    """Close scoped active references and logical continuations inside the package."""
    from .assemble import text_bytes
    blocks={v['id']:v for v in package['blocks']};regions={v['id'] for v in package['regions']+package['excluded_regions']}
    figures={v['id'] for v in package['figures']};physical={v['line_id'] for v in correction['listing_line_index']};logical={v['line_id'] for v in correction['logical_listing_line_index']}
    definitions={k:set() for k in ('node','edge','graph','sequence','component','port','field','wire','crossing','bus','terminal','cell','row','label','token','command','format','paragraph','entry','byline','footnote','delimiter')}
    def define(kind,values):
        values=list(values);need(len(values)==len(set(values)) and not definitions[kind]&set(values),'duplicate active '+kind);definitions[kind].update(values)
    define('label',[v['label_id'] for v in correction['figure_label_index']])
    for table in correction['tables']:
        define('row',[v['row_id'] for v in table['rows']]);define('cell',[v['cell_id'] for row in table['rows'] for v in row['cells'] if 'cell_id' in v]);define('footnote',[v['footnote_id'] for v in table.get('footnotes',[])])
    for value in correction['basic_source_fields']:
        if 'token_id' in value:define('token',[value['token_id']])
    for value in correction['content_associations']:
        for kind in ('paragraph','entry','byline'):
            if kind+'_id' in value:define(kind,[value[kind+'_id']])
        if 'format_id' in value:define('format',[value['format_id']])
        commands=value.get('commands',[]) if value.get('kind')=='source-command-format-group' else [value] if value.get('kind')=='source-command-example' else []
        for command in commands:
            if 'command_id' in command:define('command',[command['command_id']])
            define('token',[v['token_id'] for v in command.get('tokens',[])])
    for figure in correction['figure_structures']:
        ordinary={v['node_id'] for v in figure.get('nodes',[])}|{v['subarea_id'] for v in figure.get('subareas',[])};define('node',ordinary)
        def graph_nodes(graph):
            ids=[v['node_id'] for v in graph.get('nodes',[])]+[v['subarea_id'] for v in graph.get('subareas',[])];define('node',ids)
            for edge in graph.get('edges',[]):need(edge['from_node_id'] in ids and edge['to_node_id'] in ids,'active graph edge leaves its graph')
            define('edge',[v['edge_id'] for v in graph.get('edges',[])])
        for key,kind in [('graphs','graph'),('sequences','sequence')]:
            define(kind,[v[kind+'_id'] for v in figure.get(key,[])])
            for graph in figure.get(key,[]):graph_nodes(graph)
        for edge in figure.get('edges',[]):need(edge['from_node_id'] in ordinary and edge['to_node_id'] in ordinary,'active figure edge leaves its nodes')
        define('edge',[v['edge_id'] for v in figure.get('edges',[])])
        graphs={v['graph_id']:{n['node_id'] for n in v['nodes']} for v in figure.get('graphs',[])}
        for link in figure.get('cross_panel_connectors',[]):need(link['source_node'] in graphs.get(link['source_graph'],set()) and link['target_node'] in graphs.get(link['target_graph'],set()),'cross-panel connector leaves its graph')
        components=figure.get('components',[]);define('component',[v['component_id'] for v in components]);ports=[p['port_id'] for v in components for p in v['ports']];define('port',ports)
        for wire in figure.get('wires',[]):need(set(wire['endpoints'])<=set(ports),'active source wire leaves its figure ports')
        for key,kind,idkey in [('source_fields','field','field_id'),('fields','field','field_id'),('wires','wire','wire_id'),('crossings','crossing','crossing_id'),('bus_elisions','bus','bus_id'),('terminals','terminal','terminal_id'),('delimiters','delimiter','delimiter_id')]:define(kind,[v[idkey] for v in figure.get(key,[])])
    singles={**{k:set(blocks) for k in BLOCK_KEYS|{'heading_block_id','body_block_id','transcription_block_id','format_block_id','source_last_block_id','to_block_id'}},
             **{k:regions for k in REGION_KEYS|{'transcription_region_id','physical_geometry_source_region_id'}},
             'figure_id':figures,'circuit_figure_id':figures,'table_id':{v['table_id'] for v in correction['tables']},
             'listing_id':{v['listing_id'] for v in correction['listing_groups']},'line_id':physical|logical,'source_unit_id':logical,'physical_line_id':physical,'target_source_unit_id':logical}
    for key,kind in {'node_id':'node','from_node_id':'node','to_node_id':'node','label_node_id':'node','target_node_id':'node','subarea_id':'node','source_node':'node','target_node':'node',
                     'graph_id':'graph','source_graph':'graph','target_graph':'graph','sequence_id':'sequence','edge_id':'edge','component_id':'component','port_id':'port','source_endpoint':'port','target_endpoint':'port','first_port':'port','last_port':'port',
                     'field_id':'field','model_field_id':'field','model_field_id_secondary':'field','label_field_id':'field','pin_field_id':'field','polarity_field_id':'field','source_field_id':'field',
                     'wire_id':'wire','crossing_id':'crossing','bus_id':'bus','terminal_id':'terminal','cell_id':'cell','owner_cell_id':'cell','parent_cell_id':'cell','row_id':'row','shared_bit_header_row_id':'row',
                     'label_id':'label','token_id':'token','command_id':'command','format_id':'format','paragraph_id':'paragraph','entry_id':'entry','byline_id':'byline','footnote_id':'footnote','delimiter_id':'delimiter'}.items():singles[key]=definitions[kind]
    multiples={**{k:set(blocks) for k in BLOCK_LISTS|{'caption_block_ids','transcription_block_ids'}},'region_ids':regions,'source_region_ids':regions,'figure_ids':figures,
               'physical_line_ids':physical,'source_unit_ids':logical,'component_ids':definitions['component'],'wire_ids':definitions['wire'],'child_cell_ids':definitions['cell'],
               'source_row_ids':definitions['row'],'entry_ids':definitions['entry'],'member_paragraph_ids':definitions['paragraph'],'label_ids':definitions['label'],'footnote_ids':definitions['footnote']}
    def flat(values):
        for value in values:
            if isinstance(value,list):yield from flat(value)
            else:yield value
    def walk(value):
        if isinstance(value,list):
            for v in value:walk(v)
        elif isinstance(value,dict):
            for key,item in value.items():
                if key in ('source_ref','original_metadata','inspection_transform','original_source_range','evidence'):continue
                if key in singles and item is not None:need(item in singles[key],'dangling active '+key)
                if key in multiples:need(set(item)<=multiples[key],'dangling active '+key)
                if key in ('endpoints','source_endpoints','target_endpoints','visible_terminal_pairs'):need(set(flat(item))<=definitions['port'],'dangling active circuit endpoints')
                if isinstance(item,(dict,list)):walk(item)
    from .assembly_structured import INDEXES
    for key in INDEXES:walk(correction[key])
    article,_=text_bytes(package)
    for value in correction['content_associations']:
        if value.get('kind')=='resolved-source-paragraph-continuation':
            need(len(value['fragments'])==2 and value['source_blocks_unchanged'] is True and
                 value['logical_display']==value['separator'].join(v['literal'] for v in value['fragments']) and
                 value['member_paragraph_ids']==[v['paragraph_id'] for v in value['fragments']], 'logical paragraph loses source fragments')
            for v in value['fragments']:
                checked_span(blocks[v['block_id']]['text'].encode(),v['start_byte'],v['end_byte'],v['literal']);checked_span(article,v[S],v[E],v['literal'])
        if value.get('kind')=='qualified-source-figure-reference':
            selected=[v['printed_number'] for v in value['verified_target_figures']]
            need(len(set(selected+value['unresolved_figure_numbers']))==len(selected+value['unresolved_figure_numbers']) and
                 set(selected+value['unresolved_figure_numbers'])==set(value['printed_figure_numbers']) and
                 value['target_verified']==(not value['unresolved_figure_numbers']) and value['source_numbering_repaired'] is False,
                 'qualified figure reference changes source numbering')
            for target in value['verified_target_figures']:checked_span(article,target[S],target[E],target['caption_literal'])
