"""Opt-in assembly of source-owned prose survey indexes.

The ordinary structured adapter handles page, text and asset coverage. This
extension projects explicitly scoped semantic identities and nested UTF-8 spans,
then resolves reviewed cross-segment declarations. Original packages are retained
verbatim by the assembly writer; their historical declarations stay in source_ref.
"""
from copy import deepcopy
import hashlib
import json

from .assemble import rebase, text_bytes
from .assembly_indexes import block_ranges

S, E = 'utf8_byte_start', 'utf8_byte_end_exclusive'
DOMAIN = ('literal_source_fields', 'source_literal_index', 'source_uncertainties',
          'figure_structures', 'figure_associations', 'content_associations')
BLOCKS = {'block_id', 'body_block_id', 'heading_block_id'}
BLOCK_LISTS = {'body_block_ids', 'caption_block_ids', 'transcription_block_ids'}
REGIONS = {'region_id', 'figure_region_id', 'closing_region_id'}
DEFINITIONS = {'field_id': 'field', 'literal_id': 'literal', 'paragraph_id': 'paragraph',
               'claim_id': 'claim', 'command_id': 'command', 'component_id': 'component',
               'quotation_id': 'quotation', 'group_id': 'group', 'requirement_id': 'requirement',
               'program_id': 'program', 'attribution_id': 'attribution', 'stage_id': 'stage',
               'alternative_id': 'alternative'}
REFERENCES = {**DEFINITIONS, 'product_id': 'product', 'subject_product_id': 'product',
              'continued_product_id': 'product', 'section_id': 'section',
              'parent_section_id': 'section', 'source_section_id': 'section',
              'continued_section_id': 'section', 'target_section_id': 'section',
              'source_paragraph_id': 'paragraph', 'shared_claim_id': 'claim',
              'channel_claim_id': 'claim', 'subject_id': 'subject'}
REFERENCE_LISTS = {'source_paragraph_ids': 'paragraph', 'comparison_product_ids': 'product',
                   'stage_order': 'stage'}
METADATA = {'article_id', 'blocks', 'map', 'records', 'source_readings', 'source_readings_base',
            'reading_policy', 'limitations', 'character_perfect_code', 'regional_transcription'}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def base_recipe(recipe):
    return {k: deepcopy(v) for k, v in recipe.items() if k not in ('source_index_mode', 'survey_links')}


def validate_recipe(recipe):
    from .assembly_structured import validate_recipe as validate_base
    need(recipe.get('index_mode') == 'structured-regions-v1', 'Survey requires structured regions mode')
    need(recipe.get('source_index_mode') == 'regional-survey-v1', 'Unknown survey index mode')
    need(not recipe.get('prose_joins') and not recipe.get('relationship_links'),
         'Survey retains immutable source blocks; use explicit semantic links')
    validate_base(base_recipe(recipe))
    links = recipe.get('survey_links')
    need(isinstance(links, dict) and set(links) == {'entities', 'boundaries', 'captions', 'products', 'endings'},
         'Survey requires explicit entity/boundary/caption/product/ending dispositions')
    names = [v['name'] for v in recipe['segments']]
    for key, rows in links.items():
        need(isinstance(rows, list), 'Survey dispositions must be lists')
        for row in rows:
            fields = {'from', 'to', 'evidence'} if key == 'entities' else {'left', 'right', 'evidence'} if key != 'endings' else {'source', 'evidence'}
            need(isinstance(row, dict) and set(row) == fields and
                 isinstance(row['evidence'], str) and row['evidence'].strip(), 'Invalid survey disposition')
            for name, spec in row.items():
                if name == 'evidence':
                    continue
                expected = {'segment', 'kind', 'id'} if key == 'entities' else {'segment', 'association'}
                need(isinstance(spec, dict) and set(spec) == expected and spec['segment'] in names,
                     'Invalid survey occurrence owner')
                if key == 'entities':
                    need(spec['kind'] in ('section', 'product') and isinstance(spec['id'], str) and spec['id'],
                         'Invalid survey entity reference')
                else:
                    need(type(spec['association']) is int and spec['association'] >= 0,
                         'Invalid survey association occurrence')
    need(len(links['boundaries']) == len(names) - 1 and len(links['endings']) == 1,
         'Survey must close every boundary and exactly one ending')


class Scope:
    def __init__(self, spec, source, correction):
        self.name, self.spec, self.source, self.c = spec['name'], spec, source, correction
        self.prefix = 'segments/' + self.name
        self.blocks = {v['id']: v for v in source['blocks']}
        self.regions = {v['id']: v for v in source['regions']}
        self.figures = {v['id']: v for v in source['figures']}
        self.assets = {v['region_id']: v['asset'] for v in source['region_assets']}
        self.ranges = block_ranges(source)
        self.defs = set()
        need(correction.get('character_perfect_code') is False, 'Survey cannot establish original encoded bytes')
        need(not any(v['kind'] == 'code' for v in source['blocks']), 'Survey mode does not infer code contexts')
        need(set(correction) <= set(DOMAIN) | METADATA | {
            'regional_text_ranges', 'prose_joins', 'tables', 'listing_groups', 'listing_index',
            'listing_line_index', 'logical_listing_line_index', 'listing_caption_associations', 'figure_label_index'},
             'Unknown survey correction field; add an explicit projection')
        for key in ('tables', 'listing_groups', 'listing_index', 'listing_line_index',
                    'logical_listing_line_index', 'listing_caption_associations', 'figure_label_index'):
            need(correction.get(key) == [], 'Survey mode requires prose and original illustrations')
        self.readings = correction['regional_transcription']
        text_regions = {v for block in self.blocks.values() for v in block['region_ids']}
        need(set(self.readings) == text_regions, 'Survey regional transcription differs from text coverage')
        for block in self.blocks.values():
            need(''.join(self.readings[v] for v in block['region_ids']) == block['text'],
                 'Survey regional transcription changes source blocks')
        for row in correction['content_associations']:
            if row['kind'] == 'source-section':
                self.define('section', row['section_id'])
            if row['kind'] == 'source-product-profile':
                self.define('product', row['product_id'])
        def collect(value):
            if isinstance(value, list):
                for item in value:
                    collect(item)
            elif isinstance(value, dict):
                for key, item in value.items():
                    if key.endswith('_verified') or key in ('historical_or_behavioral_verification', 'system_tested', 'normalization_applied', 'renumbering_applied', 'caption_spelling_normalized'):
                        need(item is False, 'Survey assembly cannot establish verification or normalize source readings')
                    if key in DEFINITIONS:
                        self.define(DEFINITIONS[key], item)
                    if key == 'subject_id':
                        self.defs.add(('subject', item))
                    collect(item)
        for key in DOMAIN:
            collect(correction[key])
        paragraphs = {v['paragraph_id']: v for v in correction['content_associations'] if v['kind'] == 'source-paragraph'}
        for row in correction['content_associations']:
            if 'source_paragraph_id' not in row:
                continue
            parent = paragraphs.get(row['source_paragraph_id']); source = row.get('claim_source')
            need(parent is not None and source is not None and parent['block_id'] == source['block_id'] and
                 parent['source_segments'][0]['block_start_byte'] <= source['source_segments'][0]['block_start_byte'] and
                 source['source_segments'][-1]['block_end_byte'] <= parent['source_segments'][-1]['block_end_byte'],
                 'Survey claim belongs to another source paragraph')

    def define(self, kind, value):
        need(isinstance(value, str) and value and (kind, value) not in self.defs,
             'Duplicate or blank survey definition: ' + kind)
        self.defs.add((kind, value))

    def block(self, value):
        need(value in self.blocks, 'Unknown survey block: ' + str(value))
        return self.name + '-' + value

    def source_ref(self, key, index):
        return dict(corrections=rebase(self.source['corrections'][0], self.prefix), pointer=f'/{key}/{index}')


def project_survey(recipe, originals):
    from .assembly_structured import INDEXES, project_structured
    validate_recipe(recipe)
    scopes = [Scope(spec, *original) for spec, original in zip(recipe['segments'], originals, strict=True)]
    by_name = {v.name: v for v in scopes}
    definitions = {(s.name, kind, value): s.name + ':' + kind + ':' + value for s in scopes for kind, value in s.defs}
    aliases = {}
    for row in recipe['survey_links']['entities']:
        left, right = row['from'], row['to']
        a = (left['segment'], left['kind'], left['id']); z = (right['segment'], right['kind'], right['id'])
        need(a not in definitions and a not in aliases and z in definitions and a[1] == z[1],
             'Entity binding must resolve one external reference to one declared same-kind entity')
        aliases[a] = z
    used_aliases = set()
    def entity(scope, kind, value):
        key = (scope.name, kind, value)
        if key in aliases:
            used_aliases.add(key); key = aliases[key]
        need(key in definitions, 'Unresolved survey ' + kind + ': ' + str(value))
        return definitions[key]
    prepared = []
    for scope in scopes:
        c = {k: deepcopy(scope.c[k]) for k in METADATA - {'regional_transcription', 'source_readings_base', 'character_perfect_code'} if k in scope.c}
        c.update({key: deepcopy(scope.c.get(key, [])) if key in ('regional_text_ranges', 'prose_joins') else [] for key in INDEXES})
        prepared.append((scope.source, c))
    package, correction = project_structured(base_recipe(recipe), prepared)
    ranges = block_ranges(package); article, _ = text_bytes(package)
    projected = {}

    def prior_scope(value):
        need(set(value) == {'manifest', 'article'}, 'Unknown prior survey package pin')
        manifest = value['manifest']
        matches = [s for s in scopes if all(s.spec['manifest'][k] == manifest[k] for k in ('sha256', 'bytes'))]
        need(len(matches) == 1, 'Prior survey package is not an included immutable segment')
        target = matches[0]
        raw = (json.dumps(target.source, ensure_ascii=False, indent=2) + '\n').encode()
        need(value['article']['sha256'] == hashlib.sha256(raw).hexdigest() and value['article']['bytes'] == len(raw),
             'Prior survey article differs from its pinned package')
        return target

    def revise(scope, value, owner=None):
        if isinstance(value, list):
            return [revise(scope, v, owner) for v in value]
        if not isinstance(value, dict):
            return deepcopy(value)
        current = value.get('block_id', owner)
        result = {}
        external = prior_scope(value['prior_package']) if 'prior_package' in value else None
        for key, item in value.items():
            if item is None:
                result[key] = None
            elif key in BLOCKS:
                result[key] = scope.block(item)
            elif key in BLOCK_LISTS:
                result[key] = [scope.block(v) for v in item]
            elif key in REGIONS:
                need(item in scope.regions, 'Unknown survey region')
                result[key] = scope.name + '-' + item
            elif key == 'figure_id':
                need(item in scope.figures, 'Unknown survey figure')
                result[key] = scope.name + '-' + item
            elif key in REFERENCES:
                result[key] = entity(scope, REFERENCES[key], item)
            elif key in REFERENCE_LISTS:
                result[key] = [entity(scope, REFERENCE_LISTS[key], v) for v in item]
            elif key == 'scan':
                rid = value.get('region_id', value.get('figure_region_id'))
                need(item in scope.assets.values() and (rid is None or item == scope.assets.get(rid)),
                     'Survey scan differs from its owning region')
                result[key] = rebase(item, scope.prefix)
            elif key == 'prior_package':
                result[key] = {k: dict(v, path=external.prefix + '/' + ('manifest.json' if k == 'manifest' else 'article.json')) for k, v in item.items()}
            elif key in ('prior_block_id', 'prior_heading_block_id', 'prior_caption_block_id'):
                need(external is not None, 'Prior survey block lacks its pinned package')
                result[key] = external.block(item)
            elif key == 'prior_figure_id':
                need(external is not None and item in external.figures, 'Prior figure lacks its pinned package')
                result[key] = external.name + '-' + item
            else:
                result[key] = revise(scope, item, current)
        if 'block_start_byte' in value or S in value:
            need(current in scope.blocks and 'block_start_byte' in value and 'block_end_byte' in value and S in value and E in value,
                 'Nested survey span requires explicit block and article coordinates')
            a, z = value['block_start_byte'], value['block_end_byte']
            data = scope.blocks[current]['text'].encode()
            need(type(a) is int and type(z) is int and 0 <= a <= z <= len(data), 'Survey block span outside source')
            raw = data[a:z]
            try:
                raw.decode(); data[:a].decode(); data[:z].decode()
            except UnicodeDecodeError as error:
                raise ValueError('Survey span splits UTF-8') from error
            need(value[S] == scope.ranges[current][0] + a and value[E] == scope.ranges[current][0] + z,
                 'Survey article span differs from source block coordinates')
            if 'regional_start_byte' in value:
                rid = value['region_id']; local = next((v for v in scope.c['regional_text_ranges'] if v['region_id'] == rid), None)
                need(local is not None and local['block_id'] == current and
                     a == local['start_byte'] + value['regional_start_byte'] and z == local['start_byte'] + value['regional_end_byte'] and
                     scope.readings[rid].encode()[value['regional_start_byte']:value['regional_end_byte']] == raw,
                     'Survey occurrence differs from its exact source region')
            result[S] = ranges[scope.block(current)][0] + a; result[E] = ranges[scope.block(current)][0] + z
            need(article[result[S]:result[E]] == raw, 'Survey projection changed source bytes')
        if 'source_segments' in value:
            parts = value['source_segments']; text = value.get('literal')
            need(isinstance(text, str) and current in scope.blocks and parts, 'Survey literal requires owned source parts')
            starts = [v['block_start_byte'] for v in parts]; ends = [v['block_end_byte'] for v in parts]
            need(all(z == a for z, a in zip(ends, starts[1:])) and
                 b''.join(scope.blocks[current]['text'].encode()[a:z] for a, z in zip(starts, ends)) == text.encode(),
                 'Survey literal omits, duplicates or changes source parts')
        return result

    for key in DOMAIN:
        correction[key] = []
        for scope in scopes:
            for i, original in enumerate(scope.c[key]):
                row = revise(scope, original)
                row.update(source_segment=scope.name, source_ref=scope.source_ref(key, i))
                correction[key].append(row)
                if key == 'content_associations':
                    projected[(scope.name, i)] = row
    need(used_aliases == set(aliases), 'Unused survey entity disposition')
    for segment, scope in zip(correction['segments'], scopes, strict=True):
        segment['original_metadata'] = {k: deepcopy(v) for k, v in scope.c.items() if k not in DOMAIN and k not in INDEXES and k not in {'records', 'blocks', 'map'}}
        segment['original_metadata_scope'] = 'immutable-segment-corrections'
    correction['source_index_mode'] = 'regional-survey-v1'
    correction['survey_entities'] = [dict(id=id, kind=kind, source_segment=name, source_id=value)
                                     for (name, kind, value), id in sorted(definitions.items())]
    correction['survey_entity_links'] = [dict(source=dict(row['from']), target=definitions[(row['to']['segment'], row['to']['kind'], row['to']['id'])], evidence=row['evidence']) for row in recipe['survey_links']['entities']]
    correction['text_index'] = [dict(block_id=block['id'], region_ids=block['region_ids'], download='article.txt', **{S: ranges[block['id']][0], E: ranges[block['id']][1]}) for block in package['blocks']]
    correction['survey_resolutions'] = []

    def occurrence(spec, kind):
        scope = by_name[spec['segment']]; i = spec['association']
        rows = scope.c['content_associations']
        need(i < len(rows) and rows[i]['kind'] == kind, 'Wrong survey declaration occurrence')
        return scope, rows[i], projected[(scope.name, i)]
    used = set()
    def consume(spec, kind):
        key = (spec['segment'], spec['association'])
        need(key not in used, 'Repeated survey declaration disposition')
        used.add(key)
        return occurrence(spec, kind)
    def resolved(active, kind, original):
        active['kind'] = kind
        active['original_declaration'] = dict(scope='immutable-segment-corrections', value=deepcopy(original))
        return active
    resolve_links(recipe, scopes, correction, consume, resolved, entity)
    expected = {(s.name, i) for s in scopes for i, v in enumerate(s.c['content_associations']) if v['kind'] in {
        'source-segment-continuation', 'source-segment-opening', 'source-article-ending',
        'source-caption-forward-reference', 'source-caption-back-reference', 'source-product-profile-continuation'}}
    # Product roots are also explicitly consumed, but are ordinary profile records.
    ordinary_roots = {(v['left']['segment'], v['left']['association']) for v in recipe['survey_links']['products']}
    need(used == expected | ordinary_roots, 'Survey declarations are not completely and uniquely resolved')
    return package, correction


def resolve_links(recipe, scopes, correction, consume, resolved, entity):
    names = [v.name for v in scopes]
    for link in recipe['survey_links']['boundaries']:
        left, a, aa = consume(link['left'], 'source-segment-continuation')
        right, z, zz = consume(link['right'], 'source-segment-opening')
        need(names.index(right.name) == names.index(left.name) + 1 and
             a['current_last_source']['literal'] == z['prior_last_literal'] and
             a['next_literal'] == z['current_first_source']['literal'] and
             a['paragraph_continues'] is False and z['paragraph_continues'] is False and
             a['next_printed_folio'] == int(right.source['pages'][0]['printed_page']) and
             a['next_source_image'] == right.source['pages'][0]['image'] and
             a['pending_source_folios'] == [int(v['printed_page']) for s in scopes[names.index(right.name):] for v in s.source['pages']] and
             z['prior_block_id'] in left.blocks and left.blocks[z['prior_block_id']]['text'].endswith(z['prior_last_literal']) and
             right.blocks[z['current_first_source']['block_id']]['text'].startswith(a['next_literal']),
             'Survey boundary differs from source declarations or paragraph ownership')
        need(z['prior_package']['manifest']['sha256'] == left.spec['manifest']['sha256'], 'Boundary points to another opening package')
        for active, original, kind in [(aa, a, 'resolved-source-segment-boundary'), (zz, z, 'resolved-source-segment-opening')]:
            resolved(active, kind, original)
            active.update(article_complete=True, whole_article_assembly_required=False, pending_source_folios=[])
        aa.update(next_source=deepcopy(zz['current_first_source'])); aa.pop('next_literal')
        correction['survey_resolutions'].append(dict(kind='source-paragraph-boundary', left_source=deepcopy(aa['current_last_source']), right_source=deepcopy(zz['current_first_source']), separator='\n\n', paragraph_continues=False, source_blocks_unchanged=True, evidence=link['evidence']))
    for link in recipe['survey_links']['captions']:
        left, a, aa = consume(link['left'], 'source-caption-forward-reference')
        right, z, zz = consume(link['right'], 'source-caption-back-reference')
        need(a['caption_source']['literal'] == z['prior_caption_literal'] and
             a['target_heading_literal'] == z['target_heading_source']['literal'] and
             a['target_printed_folio'] == int(right.source['pages'][0]['printed_page']) and
             a['figure_id'] == z['prior_figure_id'] and a['caption_source']['block_id'] == z['prior_caption_block_id'] and
             a['caption_assigned_to_adjacent_product'] is False and z['caption_assigned_to_starburst'] is False and
             z['caption_spelling_normalized'] is False and aa['target_section_id'] == zz['target_section_id'],
             'Survey caption references disagree with actual caption or target heading')
        need(a['caption_source']['literal'] == left.figures[a['figure_id']]['caption'] and
             any(v['figure_id'] == a['figure_id'] and a['caption_source']['block_id'] in v['caption_block_ids']
                 for v in left.c['figure_associations']), 'Survey caption does not belong to the named original illustration')
        target = next((v for v in right.c['content_associations'] if v['kind'] == 'source-section' and v['section_id'] == z['target_section_id']), None)
        need(target is not None and target['heading_source'] == z['target_heading_source'] and
             z['prior_package']['manifest']['sha256'] == left.spec['manifest']['sha256'],
             'Survey caption target differs from its declared section or prior package')
        resolved(aa, 'resolved-source-caption-reference', a); resolved(zz, 'resolved-source-caption-back-reference', z)
        aa.update(target_status='inside-assembled-article', target_heading_source=deepcopy(zz['target_heading_source']))
        zz.update(caption_source=deepcopy(aa['caption_source']))
        correction['survey_resolutions'].append(dict(kind='source-caption-topic', figure_id=aa['figure_id'], caption_source=deepcopy(aa['caption_source']), target_heading_source=deepcopy(zz['target_heading_source']), target_section_id=aa['target_section_id'], source_spelling_normalized=False, evidence=link['evidence']))
    for link in recipe['survey_links']['products']:
        left, a, aa = consume(link['left'], 'source-product-profile')
        right, z, zz = consume(link['right'], 'source-product-profile-continuation')
        need(aa['product_id'] == zz['product_id'] and z['prior_heading_block_id'] == a['heading_source']['block_id'] and
             a['complete_in_segment'] is False and z['profile_source_ending_in_segment'] is True and
             z['prior_package']['manifest']['sha256'] == left.spec['manifest']['sha256'],
             'Survey product continuation differs from its heading/profile')
        resolved(zz, 'resolved-source-product-profile-continuation', z)
        correction['survey_resolutions'].append(dict(kind='source-product-profile', product_id=aa['product_id'], heading_source=deepcopy(aa['heading_source']), body_block_ids=[aa['body_block_id'], zz['body_block_id']], source_paragraph_ids=aa['source_paragraph_ids'] + zz['source_paragraph_ids'], complete_article_profile=True, source_blocks_unchanged=True, evidence=link['evidence']))
    for link in recipe['survey_links']['endings']:
        scope, original, active = consume(link['source'], 'source-article-ending')
        need(scope.name == names[-1] and original['closing_printed_folio'] == int(scope.source['pages'][-1]['printed_page']) and
             original['pending_source_folios'] == [] and original['next_printed_folio'] > original['closing_printed_folio'] and
             scope.blocks[original['ending_source']['block_id']]['text'].endswith(original['ending_source']['literal']) and
             original['closing_region_id'] in scope.regions and scope.regions[original['closing_region_id']]['kind'] == 'figure' and
             scope.source['content_order'][-1]['type'] == 'figure' and
             original['closing_region_id'] in scope.figures[scope.source['content_order'][-1]['id']]['region_ids'],
             'Survey ending or original closing emblem is not accounted')
        resolved(active, 'resolved-source-article-ending', original)
        active.update(article_complete=True, whole_article_assembly_required=False)
