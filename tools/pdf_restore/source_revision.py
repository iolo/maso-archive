"""Assemble an evidenced PDF/JPEG supplement without relabeling either source.

The revision retains both original native packages byte-for-byte. Its active
reading order, source views and byte indexes are recomputed by the standalone
checker from those packages and the retained recipe. It never runs OCR.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import re
import tempfile
import zipfile

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from tools.storage_layout import is_local_output
from .inventory import ROOT, pin, write_json

S, E = 'utf8_byte_start', 'utf8_byte_end_exclusive'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def validate_article(package):
    base = json.loads((ROOT / 'schemas/pdf-article.schema.json').read_bytes())
    image = json.loads((ROOT / 'schemas/image-article.schema.json').read_bytes())
    registry = Registry().with_resources((s['$id'], Resource.from_contents(s)) for s in (base, image))
    schema = json.loads((ROOT / 'schemas/source-revision.schema.json').read_bytes())
    Draft202012Validator(schema, registry=registry).validate(package)
    need(package['id'] == 'scan-' + package['toc_entry_id'] and
         package['toc_entry_id'].startswith(package['issue_id'] + '-toc-'), 'Revision canonical identity differs')
    components = {v['name']: v for v in package['components']}
    need(len(components) == len(package['components']) == 2, 'Revision requires two distinct source components')
    views = {v['view_id']: v for v in package['pages']}
    need(len(views) == len(package['pages']), 'Revision repeats a source view')
    for v in views.values():
        need(v['component'] in components and v['source_kind'] == components[v['component']]['source_kind'],
             'Revision view has wrong source kind or component')
        original = v['original_page']
        need(('pdf_index' in original) == (v['source_kind'] == 'pdf'), 'Revision invents source geometry')
    regions = {v['id']: v for v in package['regions']}
    need(len(regions) == len(package['regions']), 'Revision repeats a region')
    excluded = [v['id'] for v in package['excluded_regions']]
    need(len(set(excluded)) == len(excluded) and not set(excluded) & set(regions), 'Revision exclusion identity differs')
    for v in package['regions'] + package['excluded_regions']:
        need(v['view_id'] in views, 'Revision region has no source view')
        x0, y0, x1, y1 = v['bbox']
        need(0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1, 'Revision region bounds differ')
    blocks = {v['id']: v for v in package['blocks']}
    figures = {v['id']: v for v in package['figures']}
    need(len(blocks) + len(figures) == len(package['blocks']) + len(package['figures']) and
         not set(blocks) & set(figures), 'Revision content identities differ')
    order = [(v['type'], v['id']) for v in package['content_order']]
    need(len(order) == len(set(order)) and set(order) ==
         {('block', id) for id in blocks} | {('figure', id) for id in figures}, 'Revision content order differs')
    represented = set()
    for v in package['blocks'] + package['figures']:
        need(bool(v['region_ids']) and set(v['region_ids']) <= regions.keys(), 'Revision content has unknown source regions')
        represented.update(v['region_ids'])
    need(represented == set(regions), 'Revision source coverage differs')
    need(set(package['verification']['reviewed_region_ids']) == set(regions), 'Revision review coverage differs')
    need({v['region_id'] for v in package['region_assets']} == set(regions) and
         len(package['region_assets']) == len(regions), 'Revision region assets differ')
    return package


def validate_recipe(recipe):
    need(set(recipe) == {'kind', 'components', 'expected_views', 'join', 'resolved_notes', 'evidence', 'uncertainties'},
         'Unknown or missing source revision recipe fields')
    need(recipe['kind'] == 'source-supplement-assembly-v1', 'Unknown source revision mode')
    need(isinstance(recipe['components'], list) and len(recipe['components']) == 2, 'Revision requires two components')
    names = []
    for v in recipe['components']:
        need(set(v) == {'name', 'manifest', 'inventory', 'toc_snapshot'} and
             re.fullmatch(r'[a-z][a-z0-9-]*', v['name']), 'Invalid revision component')
        need(set(v['inventory']) == {'sources', 'queue'}, 'Revision component inventory missing')
        names.append(v['name'])
    need(len(set(names)) == 2, 'Repeated revision component')
    join = recipe['join']
    need(set(join) == {'from_component', 'from_block', 'to_component', 'to_block', 'separator',
                      'printed_line', 'from_suffix', 'to_prefix', 'from_printed_folio',
                      'to_printed_folio', 'next_printed_line', 'last_printed_line', 'reason'},
         'Unknown or missing source join fields')
    need([join['from_component'], join['to_component']] == names and join['separator'] in ('', '\n') and
         type(join['printed_line']) is int and type(join['next_printed_line']) is int and
         type(join['last_printed_line']) is int and join['printed_line'] < join['next_printed_line'] <= join['last_printed_line'] and
         all(isinstance(join[k], str) and join[k].strip() for k in
             ('from_block', 'to_block', 'from_suffix', 'to_prefix', 'from_printed_folio', 'to_printed_folio', 'reason')),
         'Revision join needs exact observed boundary evidence')
    for key in ('evidence', 'uncertainties'):
        need(isinstance(recipe[key], list) and bool(recipe[key]) and
             all(isinstance(v, str) and v.strip() for v in recipe[key]), 'Revision needs evidence and retained limitations')
    for v in recipe['expected_views']:
        need(set(v) == {'component', 'source_kind', 'source_index', 'printed_page'} and
             v['component'] in names and v['source_kind'] in ('pdf', 'jpeg') and
             type(v['source_index']) is int and v['source_index'] >= 0 and
             isinstance(v['printed_page'], str) and v['printed_page'].strip(), 'Invalid expected source view')
    for v in recipe['resolved_notes']:
        need(set(v) == {'component', 'field', 'note', 'reason'} and v['component'] in names and
             v['field'] in ('gaps', 'verification.uncertainties') and
             all(isinstance(v[k], str) and v[k].strip() for k in ('note', 'reason')), 'Invalid scoped note disposition')


def reading_bytes(package):
    blocks = {v['id']: v for v in package['blocks']}
    parts, code = [], []
    for item in package['content_order']:
        if item['type'] == 'figure':
            parts.append(f'[그림 {item["id"]}: 스캔 이미지 참조]')
        else:
            b = blocks[item['id']]
            parts.append(b['text'])
            if b['kind'] == 'code':
                code.append(b['text'])
    return ('\n\n'.join(parts) + '\n').encode(), ''.join(code).encode()


def rebase(record, prefix):
    return {**record, 'path': prefix + '/' + record['path']}


def project(recipe, originals):
    """Pure projection from checked, immutable native source packages."""
    validate_recipe(recipe)
    need(len(originals) == 2 and [p['schema_version'] for p, c in originals] == [1, 2],
         'Source supplement requires a PDF opening and JPEG continuation')
    first = originals[0][0]
    for p, c in originals:
        need(all(p[k] == first[k] for k in ('id', 'issue_id', 'toc_entry_id', 'title', 'coordinates')),
             'Source revision identity/title differs')
        need(p['verification']['status'] != 'unreviewed' and p['availability'] in ('partial', 'readable'),
             'Source revision requires reviewed native components')
    result = {k: deepcopy(first[k]) for k in ('id', 'issue_id', 'toc_entry_id', 'title', 'coordinates')}
    result.update(schema_version=3, kind='mixed-source-article', components=[], pages=[], regions=[],
                  excluded_regions=[], blocks=[], figures=[], content_order=[], raw_ocr=[], region_assets=[],
                  corrections=[], review_records=[], downloads=[], availability='readable', relationships=[], gaps=[])
    correction = dict(article_id=first['id'], kind='source-revision-indexes', component_records=[],
                      regional_text_ranges=[], editorial_separators=[], listing_line_index=[],
                      logical_listing_line_index=[], source_notes=[], resolved_notes=deepcopy(recipe['resolved_notes']),
                      physical_token_index=[], source_boundary_joins=[], figure_associations=[],
                      source_qualification_index=[])
    actual_views, local_blocks, regional = [], {}, []
    for spec, (p, c) in zip(recipe['components'], originals, strict=True):
        name = spec['name']; prefix = 'components/' + name
        identity = lambda id: name + '--' + id
        kind = 'pdf' if p['schema_version'] == 1 else 'jpeg'
        result['components'].append(dict(name=name, source_kind=kind, source=deepcopy(p['source']),
            toc_pin=deepcopy(p['toc_pin']), original_manifest=rebase({**spec['manifest'], 'path':'manifest.json'}, prefix),
            original_availability=p['availability'], original_verification=deepcopy(p['verification'])))
        correction['component_records'].append(dict(name=name, original_corrections=rebase(p['corrections'][0], prefix),
            original_review_records=[rebase(v, prefix) for v in p.get('review_records', [])],
            original_gap_notes=deepcopy(p['gaps']), historical_source_notes_scoped_to_component=True))
        expected_resolutions = {(v['field'], v['note']) for v in recipe['resolved_notes'] if v['component'] == name}
        all_notes = [('gaps', v) for v in p['gaps']] + [('verification.uncertainties', v) for v in p['verification']['uncertainties']]
        need(expected_resolutions <= set(all_notes), 'Scoped note disposition differs from original component')
        need(len(expected_resolutions) == sum(v['component'] == name for v in recipe['resolved_notes']), 'Repeated note disposition')
        for field, note in all_notes:
            correction['source_notes'].append(dict(component=name, field=field, original_note=note,
                status='resolved-by-this-revision' if (field, note) in expected_resolutions else 'retained-qualification'))
            if (field, note) not in expected_resolutions:
                result['gaps'].append(f'{name}: {note}')
        for page in p['pages']:
            i = page.get('source_index', page.get('pdf_index')); view = identity('view-' + str(i))
            result['pages'].append(dict(view_id=view, component=name, source_kind=kind, original_page=deepcopy(page)))
            actual_views.append(dict(component=name, source_kind=kind, source_index=i, printed_page=page['printed_page']))
        for key in ('regions', 'excluded_regions'):
            for v in p[key]:
                i = v.get('source_index', v.get('pdf_index'))
                result[key].append(dict(id=identity(v['id']), view_id=identity('view-' + str(i)),
                    source_region_id=v['id'], kind=v['kind'], bbox=v['bbox'], notes=v['notes']))
        for v in p['region_assets']:
            result['region_assets'].append(dict(region_id=identity(v['region_id']), asset=rebase(v['asset'], prefix)))
        for v in p['raw_ocr']:
            result['raw_ocr'].append({**deepcopy(v), 'region_ids':[identity(id) for id in v['region_ids']],
                                    **{k: rebase(v[k], prefix) for k in ('text', 'positions', 'settings')}})
        assets = {v['region_id']: v['asset'] for v in p['region_assets']}
        for block in p['blocks']:
            b = deepcopy(block); b['id'] = identity(block['id']); b['region_ids'] = [identity(id) for id in b['region_ids']]
            b['correction_evidence'] = [prefix + '/' + v for v in b['correction_evidence']]
            local_blocks[(name, block['id'])] = b; result['blocks'].append(b)
            cursor = 0
            for rid in block['region_ids']:
                record = next(v for v in c['records'] if v['id'] == rid)
                text = record.get('corrected_text', c.get('regional_transcription', {}).get(rid))
                need(isinstance(text, str) and bool(text), 'Revision region lacks native reading')
                start = block['text'].find(text, cursor)
                need(start >= cursor and block['text'][cursor:start] in ('', ' ', '\n', '\n\n'),
                     'Native regional reading does not partition block')
                a, z = len(block['text'][:start].encode()), len(block['text'][:start+len(text)].encode())
                if start > cursor:
                    correction['editorial_separators'].append(dict(component=name, block_id=b['id'],
                        start_byte=len(block['text'][:cursor].encode()), end_byte=a,
                        literal=block['text'][cursor:start], original_native_separator=True, printed_glyph_claim=False))
                regional.append(dict(component=name, original_block_id=block['id'], original_region_id=rid,
                    region_id=identity(rid), block_id=b['id'], start_byte=a, end_byte=z, literal=text,
                    scan=rebase(assets[rid], prefix), original_block_start_byte=a, original_block_end_byte=z))
                cursor = start + len(text)
            need(block['text'][cursor:] in ('', '\n'), 'Native regional reading leaves content')
            if cursor < len(block['text']):
                correction['editorial_separators'].append(dict(component=name, block_id=b['id'],
                    start_byte=len(block['text'][:cursor].encode()), end_byte=len(block['text'].encode()),
                    literal=block['text'][cursor:], original_native_separator=True, printed_glyph_claim=False))
        for figure in p['figures']:
            result['figures'].append({**deepcopy(figure), 'id':identity(figure['id']),
                'region_ids':[identity(id) for id in figure['region_ids']], 'asset':rebase(figure['asset'], prefix)})
            associations = [v for v in c.get('figure_sequence', []) if v['figure_id'] == figure['id']]
            need(len(associations) == 1, 'Original figure requires an explicit caption disposition')
            association = associations[0]
            caption_id = association.get('caption_block_id')
            caption = next((v for v in p['blocks'] if v['id'] == caption_id), None)
            need((caption is None and caption_id is None and figure['caption'] is None) or
                 (caption is not None and caption['kind'] == 'caption' and caption['text'] == figure['caption']),
                 'Original figure caption differs from its source block')
            correction['figure_associations'].append(dict(component=name,figure_id=identity(figure['id']),
                figure_region_ids=[identity(id) for id in figure['region_ids']],
                caption_block_id=identity(caption_id) if caption_id else None,
                literal_caption=figure['caption'],printed_number=association.get('number'),
                original_record=dict(path=prefix+'/corrections.json',field='figure_sequence',
                                     index=c['figure_sequence'].index(association))))
        result['content_order'].extend(dict(type=v['type'], id=identity(v['id'])) for v in p['content_order'])
    need(actual_views == recipe['expected_views'], 'Source revision view coverage/order differs')
    join = recipe['join']; left = local_blocks[(join['from_component'], join['from_block'])]
    right = local_blocks[(join['to_component'], join['to_block'])]
    need(left['kind'] == right['kind'] == 'code' and
         result['content_order'][-2:] == [dict(type='block', id=left['id']), dict(type='block', id=right['id'])],
         'Source join is not adjacent final program content')
    need(left['text'].endswith(join['from_suffix']) and right['text'].startswith(join['to_prefix']), 'Source join literal differs')
    from_region, to_region = left['region_ids'][-1], right['region_ids'][0]
    views = {v['view_id']:v for v in result['pages']}; regions = {v['id']:v for v in result['regions']}
    for rid, key in [(from_region, 'from_printed_folio'), (to_region, 'to_printed_folio')]:
        need(views[regions[rid]['view_id']]['original_page']['printed_page'] == join[key], 'Source join folio differs')
    left_rows = list(re.finditer(r'(?m)^(\d{4}) [A-Z]', left['text']))
    right_rows = list(re.finditer(r'(?m)^(\d{4}) [A-Z]', right['text']))
    need(left_rows and right_rows and int(left_rows[-1][1]) == join['printed_line'] and
         int(right_rows[0][1]) == join['next_printed_line'] and
         int(right_rows[-1][1]) == join['last_printed_line'], 'Observed source join statement labels differ')
    delta = len(left['text'].encode()) + len(join['separator'].encode())
    if join['separator']:
        correction['editorial_separators'].append(dict(component=None, block_id=left['id'],
            start_byte=delta-len(join['separator'].encode()), end_byte=delta,
            literal=join['separator'], original_native_separator=False, printed_glyph_claim=False))
    for v in regional + correction['editorial_separators']:
        if v['block_id'] == right['id']:
            v['block_id'] = left['id']; v['start_byte'] += delta; v['end_byte'] += delta
    correction['source_boundary_joins'].append(dict(join, block_id=left['id'], from_region=from_region,
        to_region=to_region, start_byte=delta-len(join['separator'].encode()), end_byte=delta,
        original_components_unchanged=True, recovered_encoded_bytes=False))
    left['text'] += join['separator'] + right['text']; left['region_ids'] += right['region_ids']
    left['correction_evidence'] += right['correction_evidence']; left['uncertainties'] += right['uncertainties']
    result['blocks'].remove(right); result['content_order'].pop()
    result['mapping'] = dict(status='mapped', evidence=recipe['evidence'], uncertainties=recipe['uncertainties'])
    result['verification'] = dict(status='sample-reviewed', reviewed_region_ids=list(regions),
        evidence=recipe['evidence'], uncertainties=recipe['uncertainties'])
    result['gaps'].extend(recipe['uncertainties'])
    # Every range is explicit in both the assembled download and the original block.
    blocks = {v['id']:v for v in result['blocks']}; article, listing = reading_bytes(result)
    article_offsets = {}; cursor = 0
    for item in result['content_order']:
        if item['type'] == 'block':
            article_offsets[item['id']] = cursor; text = blocks[item['id']]['text']
        else:
            text = f'[그림 {item["id"]}: 스캔 이미지 참조]'
        cursor += len(text.encode()) + 2
    code_offsets = {}; cursor = 0
    for item in result['content_order']:
        if item['type'] == 'block' and blocks[item['id']]['kind'] == 'code':
            code_offsets[item['id']] = cursor; cursor += len(blocks[item['id']]['text'].encode())
    for v in regional:
        need(blocks[v['block_id']]['text'].encode()[v['start_byte']:v['end_byte']].decode() == v['literal'],
             'Projected regional source bytes differ')
        v.update(download='article.txt', **{S:article_offsets[v['block_id']]+v['start_byte'], E:article_offsets[v['block_id']]+v['end_byte']})
        correction['regional_text_ranges'].append(v)
    # Reconstruct physical and logical source units; rows keep all print wraps.
    for id, offset in code_offsets.items():
        data = blocks[id]['text'].encode(); pos = 0; unit = None
        spans = sorted([v for v in regional if v['block_id'] == id] +
                       [v for v in correction['editorial_separators'] if v['block_id'] == id], key=lambda v:v['start_byte'])
        need(spans and spans[0]['start_byte'] == 0 and spans[-1]['end_byte'] == len(data) and
             all(x['end_byte'] == y['start_byte'] for x,y in zip(spans,spans[1:])), 'Program regional coverage is not exact')
        for ordinal, text in enumerate(blocks[id]['text'].splitlines(keepends=True), 1):
            z = pos + len(text.encode()); parts = []
            for v in spans:
                x,y = max(pos,v['start_byte']),min(z,v['end_byte'])
                if x < y:
                    part = dict(component=v['component'], literal=data[x:y].decode(), start_byte=x, end_byte=y)
                    if 'region_id' in v:
                        original_x = v['original_block_start_byte'] + x-v['start_byte']
                        part.update(region_id=v['region_id'], scan=v['scan'], original_block_id=v['original_block_id'],
                            original_block_start_byte=original_x, original_block_end_byte=original_x+y-x)
                    else:
                        part['editorial_separator'] = True; part['printed_glyph_claim'] = False
                    parts.append(part)
            need(''.join(v['literal'] for v in parts) == text, 'Physical row source fragments differ')
            match = re.match(r'^(\d{4}) [A-Z]', text); number = int(match[1]) if match else None
            row_id = id + ':row:' + str(ordinal)
            if match:
                unit = dict(source_unit_id=id+':unit:'+str(ordinal), printed_line=number, physical_line_ids=[],
                            source_parts=[], execution_verified=False)
                correction['logical_listing_line_index'].append(unit)
            need(unit is not None, 'Complete revised program starts with an unexplained fragment')
            unit['physical_line_ids'].append(row_id); unit['source_parts'].extend(deepcopy(parts))
            row = dict(line_id=row_id, source_unit_id=unit['source_unit_id'], block_id=id, physical_line=ordinal,
                printed_line=number, row_kind='numbered' if match else 'blank' if not text.strip() else 'continuation',
                text=text, source_parts=parts, download='listing.txt', **{S:offset+pos,E:offset+z})
            correction['listing_line_index'].append(row)
            for token in re.finditer(r'[A-Z]+\$?|\d+|[^\w\s]',text):
                x=pos+len(text[:token.start()].encode());y=x+len(token[0].encode())
                token_parts = []
                for v in parts:
                    a,z = max(x,v['start_byte']),min(y,v['end_byte'])
                    if a >= z:
                        continue
                    part = dict(v,literal=data[a:z].decode(),start_byte=a,end_byte=z)
                    if 'original_block_start_byte' in v:
                        original_a = v['original_block_start_byte'] + a-v['start_byte']
                        part.update(original_block_start_byte=original_a,original_block_end_byte=original_a+z-a)
                    token_parts.append(part)
                correction['physical_token_index'].append(dict(line_id=row_id,source_unit_id=unit['source_unit_id'],
                    literal=token[0],download='listing.txt',**{S:offset+x,E:offset+y},source_parts=token_parts))
            pos += len(text.encode())
    for u in correction['logical_listing_line_index']:
        u['physical_text']=''.join(v['literal'] for v in u['source_parts'])
    # Preserve occurrence-level qualifications in active download coordinates,
    # while retaining their complete original records in the native components.
    component_offset = 0
    for spec,(p,c) in zip(recipe['components'],originals,strict=True):
        original_listing = reading_bytes(p)[1]
        for key in ('listing_anomalies','source_uncertainties'):
            for index,v in enumerate(c.get(key,[])):
                if v.get('download') != 'listing.txt' or S not in v or E not in v:
                    continue
                a,z = v[S],v[E]
                need(type(a) is int and type(z) is int and 0<=a<z<=len(original_listing),
                     'Original source qualification leaves its listing')
                literal = original_listing[a:z].decode()
                need(listing[component_offset+a:component_offset+z].decode()==literal,
                     'Projected source qualification bytes differ')
                correction['source_qualification_index'].append(dict(component=spec['name'],
                    original_record=dict(path='components/'+spec['name']+'/corrections.json',field=key,index=index),
                    literal=literal,download='listing.txt',**{S:component_offset+a,E:component_offset+z},
                    original_range={S:a,E:z},normalization_applied=False))
        component_offset += len(original_listing)
        if spec['name'] == join['from_component']:
            component_offset += len(join['separator'].encode())
    correction['coverage'] = dict(complete_article=True, source_views=len(result['pages']),
        source_images=sum(v['source_kind']=='jpeg' for v in result['pages']),
        pdf_pages=sum(v['source_kind']=='pdf' for v in result['pages']), source_specific_geometry_retained=True,
        original_native_components_retained=True, historical_gap_notes_scoped=True)
    correction['character_perfect_code']=False
    return validate_article(result), correction


def check_revision(output):
    from .assemble import read_segment
    from .build import checked
    output = Path(output)
    recipe = json.loads((output / 'revision-recipe.json').read_bytes()); validate_recipe(recipe)
    manifest = json.loads((output / 'manifest.json').read_bytes())
    need(manifest['files'] == file_inventory(output), 'Revision file inventory differs')
    originals=[]
    for spec in recipe['components']:
        folder=output/'components'/spec['name']
        originals.append(read_segment(folder,{**spec['manifest'],'path':'manifest.json'}))
        checked(output,{**spec['toc_snapshot'],'path':'inputs/'+spec['name']+'/original-TOC.md'})
        for key,record in spec['inventory'].items():
            checked(output,{**record,'path':'inputs/'+spec['name']+'/'+('sources.json' if key=='sources' else 'queue.jsonl')})
        sources=json.loads((output/'inputs'/spec['name']/'sources.json').read_bytes())['sources']
        queue=[json.loads(v) for v in (output/'inputs'/spec['name']/'queue.jsonl').read_bytes().splitlines()]
        validate_component_inputs(originals[-1][0],sources,queue,spec['toc_snapshot'])
    package,correction=project(recipe,originals)
    need(json.loads((output/'corrections.json').read_bytes())==correction,'Revision source indexes differ from retained natives')
    package['corrections']=[pin(output,'corrections.json')];package['review_records']=[pin(output,'revision-recipe.json')]
    article,listing=reading_bytes(package)
    need((output/'article.txt').read_bytes()==article and (output/'listing.txt').read_bytes()==listing,
         'Revision reading downloads differ')
    raw_names=raw_members(package)
    with zipfile.ZipFile(output/'raw-ocr.zip') as z:
        need(z.namelist()==raw_names and all(z.read(n)==(output/n).read_bytes() for n in raw_names),
             'Revision raw archive differs from original native bytes')
    package['downloads']=[pin(output,n) for n in ('article.txt','listing.txt','raw-ocr.zip')]
    need(json.loads((output/'article.json').read_bytes())==package,'Revision article projection differs from retained natives')
    need(manifest['kind']=='mixed-source-article' and manifest['article_id']==package['id'],'Revision manifest identity differs')
    for v in package['region_assets']:checked(output,v['asset'])
    return package


def raw_members(package):
    names={v[k]['path'] for v in package['raw_ocr'] for k in ('text','positions','settings')}
    names|={v['asset']['path'] for v in package['region_assets']}
    return sorted(names)


def file_inventory(folder):
    return [pin(folder,p.relative_to(folder).as_posix()) for p in sorted(folder.rglob('*'))
            if p.is_file() and p!=folder/'manifest.json']


def validate_component_inputs(package, sources, queue, toc_pin):
    source = next((v for v in sources if v['id'] == package['source']['id']), None)
    need(source is not None and source['scope'] == 'toc-entries-and-cover' and
         all(source[k] == package['source'][k] for k in ('path','sha256','bytes')),
         'Revision component source inventory differs')
    need(any(v['toc_entry_id'] == package['toc_entry_id'] and v['issue_id'] == package['issue_id'] and
             v['source_id'] == package['source']['id'] for v in queue), 'Revision component canonical queue differs')
    need(all(toc_pin[k] == package['toc_pin'][k] for k in ('sha256','bytes')),
         'Revision historical TOC snapshot differs')
    for page in package['pages']:
        if package['schema_version'] == 1:
            original = source['pages'][page['pdf_index']]
            keys = ('pdf_index','pdf_page','width_pt','height_pt','rotation','MediaBox','CropBox')
        else:
            original = next(v for v in source['pages'] if v['source_index'] == page['source_index'])
            keys = ('source_index','image','width_px','height_px','reading_order','source_filename_number')
        need(all(page[k] == original[k] for k in keys), 'Revision original source geometry differs')


def export(recipe_path,output,root=ROOT):
    from .assemble import read_segment
    from .build import checked,copy_pin,safe_path
    from .image_source import validate_image_set
    root,recipe_path,output=map(lambda p:Path(p).resolve(),(root,recipe_path,output))
    need(is_local_output(output,root) and not output.exists(),'Use a fresh source revision output')
    recipe=json.loads(recipe_path.read_bytes());validate_recipe(recipe);recipe_pin=pin(recipe_path.parent,recipe_path.name)
    originals=[];folders=[]
    for spec in recipe['components']:
        checked(root,spec['manifest']);folder=safe_path(root,spec['manifest']['path']).parent
        need(not output.is_relative_to(folder) and not folder.is_relative_to(output),'Revision output overlaps original component')
        p,c=read_segment(folder,spec['manifest']);originals.append((p,c));folders.append(folder)
        checked(root,{k:p['source'][k] for k in ('path','sha256','bytes')})
        for record in spec['inventory'].values():checked(root,record)
        sources=json.loads(checked(root,spec['inventory']['sources']))['sources']
        queue=[json.loads(v) for v in checked(root,spec['inventory']['queue']).splitlines()]
        checked(root,spec['toc_snapshot'])
        validate_component_inputs(p,sources,queue,spec['toc_snapshot'])
        if p['schema_version']==2:
            source=next(v for v in sources if v['id']==p['source']['id'])
            validate_image_set(p,source,root)
    package,correction=project(recipe,originals)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent,prefix='.source-revision-') as tmp:
        stage=Path(tmp)/'export';stage.mkdir()
        for spec,folder in zip(recipe['components'],folders,strict=True):
            manifest=json.loads(checked(root,spec['manifest']));prefix='components/'+spec['name']
            for record in manifest['files']+[pin(folder,'manifest.json')]:
                copy_pin(folder,stage,record,prefix+'/'+record['path'])
            copy_pin(root,stage,spec['toc_snapshot'],'inputs/'+spec['name']+'/original-TOC.md')
            for key,record in spec['inventory'].items():
                copy_pin(root,stage,record,'inputs/'+spec['name']+'/'+('sources.json' if key=='sources' else 'queue.jsonl'))
        copy_pin(recipe_path.parent,stage,recipe_pin,'revision-recipe.json')
        write_json(stage/'corrections.json',correction)
        package['corrections']=[pin(stage,'corrections.json')];package['review_records']=[pin(stage,'revision-recipe.json')]
        article,listing=reading_bytes(package);(stage/'article.txt').write_bytes(article);(stage/'listing.txt').write_bytes(listing)
        with zipfile.ZipFile(stage/'raw-ocr.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
            for name in raw_members(package):
                info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
                z.writestr(info,(stage/name).read_bytes())
        package['downloads']=[pin(stage,n) for n in ('article.txt','listing.txt','raw-ocr.zip')]
        write_json(stage/'article.json',validate_article(package))
        write_json(stage/'manifest.json',dict(kind='mixed-source-article',article_id=package['id'],files=file_inventory(stage)))
        check_revision(stage)
        checked(recipe_path.parent,recipe_pin)
        for spec,folder in zip(recipe['components'],folders,strict=True):read_segment(folder,spec['manifest'])
        stage.rename(output)
    return package


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe',type=Path);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.check:p=check_revision(args.output)
    else:
        if args.recipe is None:parser.error('--recipe is required')
        p=export(args.recipe,args.output)
    print(f'{"Checked" if args.check else "Built"} {p["id"]}: {len(p["pages"])} source views / {p["availability"]}')


if __name__=='__main__':main()
