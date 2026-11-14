"""Project structured JPEG segments with explicit identities and byte coordinates.

Immutable segment corrections retain their original metadata and review-aid pins.
Active indexes name assembled blocks/assets and link back to their source record.
"""
from collections import Counter
from copy import deepcopy
import re

from .assemble import rebase, text_bytes
from .assembly_examples import join_blocks, validate_joins
from .assembly_indexes import block_ranges
from .package import validate_package

START, END = 'utf8_byte_start', 'utf8_byte_end_exclusive'
INDEXES = ('regional_text_ranges', 'prose_joins', 'tables', 'listing_groups', 'listing_index',
           'listing_line_index', 'logical_listing_line_index', 'listing_caption_associations',
           'source_literal_index', 'source_uncertainties', 'figure_label_index', 'figure_structures',
           'figure_associations', 'content_associations', 'inline_source_fields', 'basic_source_fields',
           'monitor_source_fields', 'formula_occurrence_index', 'source_ellipsis_groups', 'end_mark_index')
METADATA = {'article_id', 'map', 'records', 'blocks', 'segment', 'source_readings', 'figure_repair',
            'reading_policy', 'source_notes', 'limitations', 'logical_order_note', 'crop_repair'}
BLOCK_KEYS = {'block_id', 'code_block_id', 'caption_block_id', 'from_block', 'to_block'}
BLOCK_LISTS = {'block_ids', 'code_block_ids', 'prose_block_ids'}
REGION_KEYS = {'region_id', 'figure_region_id', 'caption_region_id', 'source_region_id', 'from_region', 'to_region'}
FIGURE_KEYS = {'figure_id'}
LOCAL_KEYS = {'line_id', 'source_unit_id', 'label_id', 'occurrence_id', 'row_id', 'node_id', 'from_node', 'to_node'}


def validate_recipe(recipe):
    required = {'index_mode', 'segments', 'expected_source_indices', 'inventory', 'evidence',
                'uncertainties', 'resolved_notes', 'prose_joins', 'relationship_links'}
    if set(recipe) != required:
        raise ValueError('Unknown or missing structured assembly recipe field')
    if not isinstance(recipe['segments'], list) or not 2 <= len(recipe['segments']) <= 12:
        raise ValueError('Structured assembly requires two to twelve segments')
    names = []
    for spec in recipe['segments']:
        if set(spec) != {'name', 'manifest'} or not re.fullmatch(r'[a-z][a-z0-9-]*', spec['name']):
            raise ValueError('Invalid structured segment identity')
        names.append(spec['name'])
    if len(set(names)) != len(names):
        raise ValueError('Duplicate structured segment identity')
    pages = recipe['expected_source_indices']
    if (not isinstance(pages, list) or not pages or
            any(type(i) is not int or i < 0 for i in pages) or len(set(pages)) != len(pages)):
        raise ValueError('Expected source indices must be explicit, unique integers')
    if not isinstance(recipe['inventory'], dict) or set(recipe['inventory']) != {'sources', 'queue'}:
        raise ValueError('Structured JPEG assembly requires explicit inventory pins')
    for key in ('evidence', 'uncertainties'):
        if not isinstance(recipe[key], list) or any(not isinstance(s, str) or not s.strip() for s in recipe[key]):
            raise ValueError('Structured assembly notes must be nonblank strings')
    if not recipe['evidence']:
        raise ValueError('Structured assembly requires reviewed coverage evidence')
    validate_joins(recipe['prose_joins'])
    seen = set()
    for note in recipe['resolved_notes']:
        if (set(note) != {'segment', 'note', 'reason'} or note['segment'] not in names or
                any(not isinstance(v, str) or not v.strip() for v in note.values()) or
                (note['segment'], note['note']) in seen):
            raise ValueError('Resolved notes require unique exact source text and a reason')
        seen.add((note['segment'], note['note']))
    if not isinstance(recipe['relationship_links'], list):
        raise ValueError('Structured relationships require an explicit list')
    seen = set()
    for link in recipe['relationship_links']:
        if (set(link) != {'id', 'from_segment', 'from_figure_id', 'to_segment', 'to_table_id',
                         'outgoing_association', 'incoming_association'} or
                any(not isinstance(link[k], str) or not link[k] for k in
                    ('id', 'from_segment', 'from_figure_id', 'to_segment', 'to_table_id')) or
                link['id'] in seen or link['from_segment'] not in names or link['to_segment'] not in names or
                names.index(link['to_segment']) != names.index(link['from_segment']) + 1 or
                any(type(link[k]) is not int or link[k] < 0 for k in ('outgoing_association', 'incoming_association'))):
            raise ValueError('Invalid cross-segment relationship link')
        seen.add(link['id'])


def checked_span(data, start, end, literal=None):
    if type(start) is not int or type(end) is not int or not 0 <= start <= end <= len(data):
        raise ValueError('Structured byte span lies outside its coordinate system')
    try:
        value = data[start:end].decode('utf-8')
    except UnicodeDecodeError as error:
        raise ValueError('Structured byte span splits a UTF-8 character') from error
    if literal is not None and value != literal:
        raise ValueError('Structured span differs from its literal source bytes')
    return value


class Context:
    def __init__(self, spec, source, correction, offset):
        self.spec, self.source, self.correction, self.offset = spec, source, correction, offset
        self.name, self.prefix = spec['name'], 'segments/' + spec['name']
        self.regions = {r['id'] for r in source['regions'] + source['excluded_regions']}
        self.blocks = {b['id']: b for b in source['blocks']}
        self.figures = {f['id'] for f in source['figures']}
        self.tables = {t['table_id'] for t in correction.get('tables', [])}
        self.groups = {g['listing_id']: g for g in correction.get('listing_groups', [])}
        self.assets = {r['region_id']: r['asset'] for r in source['region_assets']}
        self.positions = {self.name + '-' + id: (self.name + '-' + id, 0) for id in self.blocks}
        self.article, self.listing = text_bytes(source)
        if set(correction) - set(INDEXES) - METADATA:
            raise ValueError('Unrecognized structured correction index; add an explicit projection')

    def identity(self, value, allowed):
        if value not in allowed:
            raise ValueError('Unknown structured reference: ' + str(value))
        return self.name + '-' + value

    def block(self, value):
        return self.positions[self.identity(value, self.blocks)][0]

    def refs(self, value):
        if isinstance(value, list):
            return [self.refs(v) for v in value]
        if not isinstance(value, dict):
            return deepcopy(value)
        result = {}
        for key, item in value.items():
            # Derived review views remain in their original correction context.
            # Every active occurrence still names its exported source-region scan.
            if key in ('review_crop', 'source_context') or key == 'evidence' and isinstance(item, dict):
                continue
            if item is None:
                result[key] = None
            elif key in BLOCK_KEYS:
                result[key] = self.block(item)
            elif key in BLOCK_LISTS:
                result[key] = [self.block(v) for v in item]
            elif key in REGION_KEYS:
                result[key] = self.identity(item, self.regions)
            elif key == 'region_ids':
                result[key] = [self.identity(v, self.regions) for v in item]
            elif key in FIGURE_KEYS:
                result[key] = self.identity(item, self.figures)
            elif key == 'figure_ids':
                result[key] = [self.identity(v, self.figures) for v in item]
            elif key == 'table_id':
                result[key] = self.identity(item, self.tables)
            elif key == 'listing_id':
                result[key] = self.identity(item, self.groups)
            elif key in LOCAL_KEYS:
                result[key] = self.name + ':' + item
            elif key == 'physical_line_ids':
                result[key] = [self.name + ':' + v for v in item]
            elif key == 'scan':
                region = value.get('region_id', value.get('figure_region_id'))
                if item not in self.assets.values() or region is not None and item != self.assets.get(region):
                    raise ValueError('Structured source scan differs from its mapped region')
                result[key] = rebase(item, self.prefix)
            else:
                result[key] = self.refs(item)
        return result

    def source_ref(self, field, index):
        return dict(corrections=rebase(self.source['corrections'][0], self.prefix), pointer=f'/{field}/{index}')

    def row(self, field, index):
        return self.refs(self.correction[field][index]) | dict(source_segment=self.name,
            source_ref=self.source_ref(field, index))

    def block_span(self, row, projected, ranges, *, owner=None, literal=None):
        owner = owner or row.get('block_id') or self.code_block(row['listing_id'])
        data = self.blocks[owner]['text'].encode()
        checked_span(data, row['start_byte'], row['end_byte'], literal)
        target, within = self.positions[self.identity(owner, self.blocks)]
        a, z = within + row['start_byte'], within + row['end_byte']
        projected.update(start_byte=a, end_byte=z)
        if row.get('download') != 'listing.txt':
            projected.update(download='article.txt', **{START:ranges[target][0]+a, END:ranges[target][0]+z})
        return projected

    def code_block(self, listing_id):
        group = self.groups.get(listing_id)
        if group is None or len(group['block_ids']) != 1:
            raise ValueError('Structured listing groups require one complete logical code block')
        return group['block_ids'][0]

    def listing_spans(self, original, projected):
        if isinstance(original, list):
            for a,z in zip(original,projected,strict=True):self.listing_spans(a,z)
        elif isinstance(original, dict):
            if START in original or END in original:
                if START not in original or END not in original:
                    raise ValueError('Incomplete structured listing span')
                literal = original.get('literal', original.get('text'))
                checked_span(self.listing, original[START], original[END], literal)
                projected[START],projected[END] = self.offset+original[START],self.offset+original[END]
            for key,item in original.items():
                if key in projected and isinstance(item,(dict,list)):
                    self.listing_spans(item,projected[key])


def project_structured(recipe, originals):
    validate_recipe(recipe)
    contexts=[];offset=0
    for spec,(source,correction) in zip(recipe['segments'],originals,strict=True):
        if source['schema_version'] != 2:
            raise ValueError('Structured JPEG mode requires explicit image-source packages')
        context=Context(spec,source,correction,offset);contexts.append(context);offset+=len(context.listing)
    first=contexts[0].source;package=deepcopy(first)
    for key in ('pages','regions','excluded_regions','blocks','figures','content_order','raw_ocr','region_assets'):
        package[key]=[]
    package.update(downloads=[],corrections=[],review_records=[],gaps=[])
    notes=[];resolved=[]
    for context in contexts:
        source=context.source
        if any(source[k]!=first[k] for k in ('id','issue_id','toc_entry_id','title','source','toc_pin','coordinates')):
            raise ValueError('Structured segments have different canonical/source/TOC identities')
        source_notes=source['gaps']+source['mapping']['uncertainties']+source['verification']['uncertainties']
        source_notes += [n for b in source['blocks'] for n in b['uncertainties']]
        resolve={r['note'] for r in recipe['resolved_notes'] if r['segment']==context.name}
        if not resolve <= set(source_notes):raise ValueError('Resolved structured note is not exact source text')
        notes.extend(f'[{context.name}] {n}' for n in dict.fromkeys(source_notes) if n not in resolve)
        package['pages'].extend(deepcopy(source['pages']))
        for key,allowed in [('regions',context.regions),('excluded_regions',context.regions),('blocks',context.blocks),('figures',context.figures)]:
            for original in source[key]:
                row=context.refs(original);row['id']=context.identity(original['id'],allowed)
                if key=='blocks':
                    row['uncertainties']=[n for n in original['uncertainties'] if n not in resolve]
                    row['correction_evidence']=['corrections.json#'+context.identity(id,context.regions) for id in original['region_ids']]
                if key=='figures':row['asset']=rebase(original['asset'],context.prefix)
                package[key].append(row)
        package['content_order'].extend(dict(type=r['type'],id=context.identity(r['id'],context.blocks if r['type']=='block' else context.figures)) for r in source['content_order'])
        package['region_assets'].extend(dict(region_id=context.identity(r['region_id'],context.regions),asset=rebase(r['asset'],context.prefix)) for r in source['region_assets'])
        package['raw_ocr'].extend(dict(region_ids=[context.identity(id,context.regions) for id in r['region_ids']],**{k:rebase(r[k],context.prefix) for k in ('text','positions','settings')}) for r in source['raw_ocr'])
    indices=[p['source_index'] for p in package['pages']]
    if indices != recipe['expected_source_indices'] or len(set(indices))!=len(indices):
        raise ValueError('Structured segments overlap or differ from ordered source coverage')
    orders=[p['reading_order'] for p in package['pages']]
    if any(type(n) is not int or n < 1 for n in orders) or orders != sorted(set(orders)):
        raise ValueError('Structured source views differ from reviewed reading order')
    validate_pending_joins(recipe, contexts)
    positions,resolved=join_blocks(recipe,package,contexts)
    for context in contexts:context.positions=positions
    ranges=block_ranges(package);article,listing=text_bytes(package)
    if listing != b''.join(c.listing for c in contexts):raise ValueError('Assembly changed original code bytes/order')
    package['gaps']=list(dict.fromkeys(recipe['uncertainties']+notes))
    package['mapping']=dict(status='mapped',evidence=recipe['evidence'],uncertainties=[])
    package['availability']='readable'
    package['verification']=dict(status='sample-reviewed',reviewed_region_ids=[r['id'] for r in package['regions']],evidence=recipe['evidence'],uncertainties=package['gaps'])
    correction=dict(article_id=package['id'],index_mode=recipe['index_mode'],policy='Projection of immutable structured JPEG segments. No OCR, source-byte inference or execution repair.',records=[],blocks=package['blocks'],segments=[],resolved_notes=deepcopy(recipe['resolved_notes']),resolved_continuations=resolved,identity_map=[],resolved_relationships=[],coverage=dict(article_source_indices=indices,included_source_indices=indices,included_printed_pages=[p['printed_page'] for p in package['pages']],complete_article=True,assembly_pending=False,source_pages_missing=False),character_perfect_code=False,**{k:[] for k in INDEXES})
    for context in contexts:
        correction['segments'].append(dict(name=context.name,directory=context.prefix,manifest=rebase({**context.spec['manifest'],'path':'manifest.json'},context.prefix),original_corrections=rebase(context.source['corrections'][0],context.prefix),original_metadata={k:deepcopy(v) for k,v in context.correction.items() if k not in INDEXES and k not in {'records','blocks','map'}}))
        for kind,allowed in [('region',context.regions),('block',context.blocks),('figure',context.figures)]:
            for id in sorted(allowed):
                target,within=positions[context.identity(id,allowed)] if kind=='block' else (context.identity(id,allowed),0)
                correction['identity_map'].append(dict(source_segment=context.name,kind=kind,source_id=id,id=target,block_start_byte=within if kind=='block' else None))
        for row in context.correction['records']:
            updated=context.refs({k:v for k,v in row.items() if k!='raw_ocr'});updated.update(id=context.identity(row['id'],context.regions),source_id=row['id'],source_segment=context.name,raw_ocr=rebase(row['raw_ocr'],context.prefix) if row['raw_ocr'] else None);correction['records'].append(updated)
        # Every text region is partitioned once; joins occupy only reviewed separators.
        coverage={id:Counter() for id in context.blocks};seen=[]
        for row in context.correction['regional_text_ranges']:
            id=row['region_id'];owner=row['block_id']
            if id not in context.blocks[owner]['region_ids'] or id in seen:raise ValueError('Duplicate or wrong-owner regional text')
            seen.append(id);checked_span(context.blocks[owner]['text'].encode(),row['start_byte'],row['end_byte'],row['text']);coverage[owner].update(range(row['start_byte'],row['end_byte']))
        for row in context.correction['prose_joins']:
            checked_span(context.blocks[row['block_id']]['text'].encode(),row['start_byte'],row['end_byte'],row['separator']);coverage[row['block_id']].update(range(row['start_byte'],row['end_byte']))
        if (set(seen)!={id for b in context.blocks.values() for id in b['region_ids']} or
            any(len(v)!=len(context.blocks[id]['text'].encode()) or any(n!=1 for n in v.values())
                for id,v in coverage.items())):
            raise ValueError('Structured regional ranges do not cover source text')
        code_ids=[r['id'] for r in context.source['content_order'] if r['type']=='block' and context.blocks[r['id']]['kind']=='code']
        if {context.code_block(id) for id in context.groups} != set(code_ids) or len(context.groups)!=len(code_ids):raise ValueError('Structured listing groups differ from code blocks')
        if any(group.get('execute_verified') is not False for group in context.groups.values()):
            raise ValueError('Structured listing groups cannot establish execution')
        supplied=context.correction.get('listing_index',[]);cursor=0
        if len(supplied)!=len(code_ids):raise ValueError('Structured listing index must cover code blocks')
        for id,row in zip(code_ids,supplied,strict=True):
            end=cursor+len(context.blocks[id]['text'].encode())
            if row['block_id']!=id or row['region_ids']!=context.blocks[id]['region_ids'] or row[START]!=cursor or row[END]!=end:
                raise ValueError('Structured listing index differs from complete code blocks')
            cursor=end
        physical=context.correction.get('listing_line_index',[])
        if ''.join(r['text'] for r in physical).encode()!=context.listing:raise ValueError('Physical rows differ from complete source listing')
        for row in physical:
            checked_span(context.listing,row[START],row[END],row['text'])
            checked_span(context.blocks[row['block_id']]['text'].encode(),row['block_start_byte'],row['block_end_byte'],row['text'])
            for field in row.get('fields',[]):
                checked_span(row['text'].encode(),field['start_byte'],field['end_byte'],field['literal'])
                checked_span(context.blocks[row['block_id']]['text'].encode(),field['block_start_byte'],field['block_end_byte'],field['literal'])
        physical_by_id={r['line_id']:r for r in physical}
        if len(physical_by_id)!=len(physical):raise ValueError('Duplicate physical listing row')
        units=context.correction.get('logical_listing_line_index',[]);unit_ids={r['line_id'] for r in units}
        if len(unit_ids)!=len(units):raise ValueError('Duplicate logical listing unit')
        for row in units:
            parts=[physical_by_id.get(id) for id in row['physical_line_ids']]
            if not parts or any(p is None for p in parts) or checked_span(context.listing,row[START],row[END])!=''.join(p['text'] for p in parts):raise ValueError('Logical listing unit differs from physical source rows')
            if row.get('execute_verified',False) is not False:raise ValueError('Assembly cannot establish execution')
        for key in ('inline_source_fields','basic_source_fields','monitor_source_fields'):
            if any(row.get('source_unit_id') is not None and row['source_unit_id'] not in unit_ids for row in context.correction.get(key,[])):
                raise ValueError('Source field refers to an unknown logical unit')
        for row in context.correction.get('source_ellipsis_groups',[]):
            if any(id not in physical_by_id for id in row['physical_line_ids']):raise ValueError('Ellipsis refers to an unknown physical row')
        for key in INDEXES:
            for i,original in enumerate(context.correction.get(key,[])):
                if key=='content_associations' and original.get('kind') in ('pending-source-example','cross-segment-source-example'):
                    continue  # Explicitly resolved below; every occurrence must match one link.
                row=context.row(key,i)
                if key=='tables':
                    owner=original['block_id'];rows=[]
                    for source_row,target_row in zip(original['rows'],row['rows'],strict=True):
                        context.block_span(source_row,target_row,ranges,owner=owner)
                        for source_cell,target_cell in zip(source_row['cells'],target_row['cells'],strict=True):context.block_span(source_cell,target_cell,ranges,owner=owner,literal=source_cell['text'])
                        rows.append(target_row)
                    row['rows']=rows
                elif key=='listing_caption_associations':
                    context.block_span(original,row,ranges,owner=original['caption_block_id'],literal=original['literal'])
                elif 'start_byte' in original and 'end_byte' in original:
                    literal=original.get('marker',original.get('literal',original.get('text',original.get('separator'))))
                    context.block_span(original,row,ranges,literal=literal)
                if key in ('listing_index','listing_line_index','logical_listing_line_index','source_literal_index','inline_source_fields','basic_source_fields','monitor_source_fields') or original.get('download')=='listing.txt':context.listing_spans(original,row)
                correction[key].append(row)
    # The new separator has an active occurrence as well as original segment joins.
    for row in resolved:
        target=row['block_id'];end=row['right_utf8_offset'];start=end-len(row['separator'].encode())
        correction['prose_joins'].append(dict(kind='cross-segment',block_id=target,start_byte=start,end_byte=end,separator=row['separator'],download='article.txt',**{START:ranges[target][0]+start,END:ranges[target][0]+end},source_blocks=row['source_blocks'],evidence=deepcopy(row['evidence'])))
    resolve_relationships(recipe,contexts,correction)
    validate_references(package, correction)
    validate_package(package)
    return package,correction


def validate_references(package,correction):
    """Every active reference closes inside the assembled typed structures."""
    blocks={b['id'] for b in package['blocks']}
    regions={r['id'] for r in package['regions']+package['excluded_regions']}
    figures={f['id'] for f in package['figures']}
    tables={t['table_id'] for t in correction['tables']}
    listings={g['listing_id'] for g in correction['listing_groups']}
    physical={r['line_id'] for r in correction['listing_line_index']}
    logical={r['line_id'] for r in correction['logical_listing_line_index']}
    nodes=set()
    def collect(value):
        if isinstance(value,list):
            for row in value:collect(row)
        elif isinstance(value,dict):
            if 'node_id' in value:nodes.add(value['node_id'])
            for child in value.values():collect(child)
    collect(correction['figure_structures'])
    singles={**{k:blocks for k in BLOCK_KEYS},**{k:regions for k in REGION_KEYS},
             'figure_id':figures,'table_id':tables,'listing_id':listings,
             'source_unit_id':logical,'from_node':nodes,'to_node':nodes}
    multiples={**{k:blocks for k in BLOCK_LISTS},'region_ids':regions,'figure_ids':figures,'physical_line_ids':physical}
    def walk(value):
        if isinstance(value,list):
            for row in value:walk(row)
        elif isinstance(value,dict):
            for key,item in value.items():
                # Boundary evidence contains explicitly segment-local source IDs;
                # the enclosing active row already names the assembled block.
                if key in ('source_ref', 'evidence'):continue
                if key in singles and item is not None and item not in singles[key]:
                    raise ValueError('Dangling structured reference: '+key)
                if key in multiples and not set(item)<=multiples[key]:
                    raise ValueError('Dangling structured reference list: '+key)
                walk(item)
    for key in INDEXES:walk(correction[key])


def validate_pending_joins(recipe,contexts):
    for index,context in enumerate(contexts):
        pending=context.correction.get('segment',{}).get('pending_prose_join')
        if pending is None:continue
        if index+1==len(contexts):raise ValueError('Pending prose join lacks its following segment')
        following=contexts[index+1]
        rows=[r for r in recipe['prose_joins'] if r['left']['segment']==context.name]
        incoming=following.correction.get('segment',{}).get('incoming_prose_join')
        if (len(rows)!=1 or rows[0]['left']['block_id']!=pending['from_block'] or
            rows[0]['left']['ending']!=pending['left_literal'] or rows[0]['right']['segment']!=following.name or
            rows[0]['right']['opening']!=pending['right_literal'] or rows[0]['separator']!=pending['separator'] or
            str(following.source['pages'][0]['printed_page'])!=str(pending['next_folio']) or
            incoming is None or incoming['left_literal']!=pending['left_literal'] or
            incoming['right_literal']!=pending['right_literal'] or incoming['separator']!=pending['separator'] or
            incoming['to_block']!=rows[0]['right']['block_id']):
            raise ValueError('Assembly prose join differs from original boundary declarations')


def resolve_relationships(recipe,contexts,correction):
    by_name={c.name:c for c in contexts};used=set()
    for link in recipe['relationship_links']:
        left,right=by_name[link['from_segment']],by_name[link['to_segment']]
        try:
            outgoing=left.correction['content_associations'][link['outgoing_association']]
            incoming=right.correction['content_associations'][link['incoming_association']]
        except IndexError as error:raise ValueError('Relationship source occurrence is absent') from error
        left.identity(link['from_figure_id'],left.figures);right.identity(link['to_table_id'],right.tables)
        if (outgoing.get('kind')!='pending-source-example' or outgoing.get('figure_id')!=link['from_figure_id'] or
            incoming.get('kind')!='cross-segment-source-example' or
            any(incoming.get(k)!=link[k] for k in ('from_segment','from_figure_id','to_segment','to_table_id')) or
            incoming.get('to_folio')!=outgoing.get('next_folio') or
            any(incoming.get('from_package',{}).get('manifest',{}).get(k)!=left.spec['manifest'][k] for k in ('sha256','bytes'))):
            raise ValueError('Cross-segment relationship differs from original source declarations')
        target_region=next(t for t in right.correction['tables'] if t['table_id']==link['to_table_id'])['rows'][0]['region_id']
        target_view=next(p for p in right.source['pages'] if p['source_index']==next(r for r in right.source['regions'] if r['id']==target_region)['source_index'])
        if str(target_view['printed_page'])!=str(incoming['to_folio']):raise ValueError('Relationship points to another source folio')
        occurrences=[]
        for context,index in [(left,link['outgoing_association']),(right,link['incoming_association'])]:
            key=context.name,index
            if key in used:raise ValueError('Repeated relationship source occurrence')
            used.add(key);ref=context.source_ref('content_associations',index);occurrences.append(ref)
            correction['content_associations'].append(dict(kind='resolved-cross-segment-source-example',relationship_id=link['id'],figure_id=left.identity(link['from_figure_id'],left.figures),table_id=right.identity(link['to_table_id'],right.tables),prose_block_ids=[right.block(id) for id in incoming['prose_block_ids']],source_segment=context.name,source_ref=ref,status='source-compared; independent representations retained',note=incoming['note']))
        correction['resolved_relationships'].append(dict(id=link['id'],figure_id=left.identity(link['from_figure_id'],left.figures),table_id=right.identity(link['to_table_id'],right.tables),source_occurrences=occurrences,source_values_changed=False))
    expected={(c.name,i) for c in contexts for i,r in enumerate(c.correction.get('content_associations',[])) if r.get('kind') in ('pending-source-example','cross-segment-source-example')}
    if used!=expected:raise ValueError('Unresolved structured cross-segment source relationship')
