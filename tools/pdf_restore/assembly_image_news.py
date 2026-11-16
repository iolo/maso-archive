"""Opt-in news assembly: source-owned tables, news identities and nested spans.

Source blocks and embedded packages remain immutable. Active coordinates refer
to article.txt; manually observed graph geometry retains its own pinned raster.
"""
from copy import deepcopy
import math

from .assemble import rebase
from .assembly_indexes import block_ranges
from .assembly_survey import need

S, E = 'utf8_byte_start', 'utf8_byte_end_exclusive'
DOMAIN = ('literal_source_fields', 'source_literal_index', 'source_uncertainties',
          'figure_structures', 'figure_associations', 'content_associations', 'tables',
          'inserted_separator_ranges')
METADATA = {'article_id', 'map', 'records', 'blocks', 'source_readings',
            'source_readings_base', 'reading_policy', 'limitations',
            'regional_transcription', 'character_perfect_code'}
EMPTY = ('listing_groups', 'listing_index', 'listing_line_index',
         'logical_listing_line_index', 'listing_caption_associations', 'figure_label_index')
BLOCKS = {'block_id', 'body_block_id'}
BLOCK_LISTS = {'body_block_ids', 'caption_block_ids'}
REGIONS = {'region_id', 'source_region_id', 'figure_region_id', 'closing_region_id',
           'left_region_id', 'right_region_id', 'from_region', 'to_region'}
REGION_LISTS = {'logical_region_ids', 'logical_region_sequence'}
REFS = {'news_item_id': 'item', 'category_id': 'category', 'parent_category_id': 'category',
        'paragraph_id': 'paragraph', 'section_id': 'section', 'table_id': 'table',
        'row_id': 'row', 'rank_scope_from_row': 'row', 'school_ditto_from_row': 'row',
        'role_scope_from_row': 'row', 'panel_id': 'panel', 'specification_group_id': 'specification',
        'sequence_id': 'sequence', 'formula_id': 'formula', 'attribution_id': 'attribution',
        'stage_id': 'stage', 'field_id': 'field', 'literal_id': 'literal',
        'qualification_id': 'qualification', 'segment_id': 'declaration', 'owner': 'item'}
LIST_REFS = {'item_ids': 'item', 'repeated_winner_row_ids': 'row'}
DEFINING = {'source-news-item': ('item', 'news_item_id'),
            'source-news-category': ('category', 'category_id'),
            'source-news-paragraph': ('paragraph', 'paragraph_id'),
            'source-news-subsection': ('section', 'section_id'),
            'source-news-specification-group': ('specification', 'specification_group_id'),
            'source-output-panel': ('panel', 'panel_id'),
            'source-numbered-news-sequence': ('sequence', 'sequence_id'),
            'source-prose-processing-sequence': ('sequence', 'sequence_id'),
            'source-literal-ratio-range': ('formula', 'formula_id'),
            'source-attributed-news-claim': ('attribution', 'attribution_id'),
            'source-segment-boundary': ('declaration', 'segment_id')}
KINDS = set(DEFINING) | {
    'source-delimited-literal', 'source-local-reading-qualification',
    'source-output-reading-qualification', 'printed-character-bar-report',
    'original-news-figure', 'source-award-category', 'source-print-specimen',
    'source-displaced-continuation', 'source-article-closing-emblem',
    'source-translation-semantic-roles', 'source-translation-direction-comparison',
    'source-news-disagreement', 'source-speech-device-report', 'source-bicmos-cell-roles',
    'source-fmb-input-and-unit-disagreement', 'source-unclosed-delimiter',
    'source-segment-opening', 'source-article-ending'}
FALSE = {'verification', 'historical_verification', 'modernized', 'normalization_applied',
         'renumbering_applied', 'chronological_reordering_applied', 'numeric_normalization_applied',
         'mathematical_or_codec_verification', 'external_identity_verification',
         'deduplication_applied', 'exact_vector_reconstruction', 'amount_to_bar_rule_inferred',
         'source_claims_resolved', 'device_tested', 'durability_tested', 'rate_units_unified',
         'input_method_executed', 'numerical_derivation_applied', 'closing_boundary_inferred',
         'program_behavior_used_to_repair', 'original_bytes_recovered'}


def base_recipe(recipe):
    return {k: deepcopy(v) for k, v in recipe.items()
            if k not in ('source_index_mode', 'news_links', 'coordinate_assets')}


def validate_recipe(recipe):
    from .assembly_structured import validate_recipe as validate_base
    need(recipe.get('index_mode') == 'structured-regions-v1' and
         recipe.get('source_index_mode') == 'regional-news-v1', 'Unknown news assembly mode')
    need(not recipe.get('prose_joins') and not recipe.get('relationship_links'),
         'News assembly retains separate source blocks')
    validate_base(base_recipe(recipe))
    links = recipe.get('news_links')
    names = [s['name'] for s in recipe['segments']]
    need(isinstance(links, dict) and set(links) == {'boundaries', 'endings'},
         'News requires explicit boundary and ending dispositions')
    for key, rows in links.items():
        need(isinstance(rows, list), 'News dispositions must be lists')
        for row in rows:
            fields = {'left', 'right', 'evidence'} if key == 'boundaries' else {'source', 'evidence'}
            need(isinstance(row, dict) and set(row) == fields and
                 isinstance(row['evidence'], str) and row['evidence'].strip(), 'Invalid news disposition')
            for k, ref in row.items():
                if k != 'evidence':
                    need(isinstance(ref, dict) and set(ref) == {'segment', 'association'} and
                         ref['segment'] in names and type(ref['association']) is int and
                         ref['association'] >= 0, 'Invalid news occurrence')
    need(len(links['boundaries']) == len(names)-1 and len(links['endings']) == 1,
         'Close every news boundary and exactly one ending')
    assets = recipe.get('coordinate_assets')
    need(isinstance(assets, list), 'Explicit coordinate assets required, even if empty')
    seen = set()
    for row in assets:
        need(set(row) == {'segment', 'figure_structure', 'asset', 'destination', 'width', 'height',
                         'source_index', 'bbox', 'scale_to', 'page_size', 'pixel_bounds'} and
             row['segment'] in names and type(row['figure_structure']) is int and
             row['figure_structure'] >= 0 and row['destination'].startswith('assembly-assets/') and
             '..' not in row['destination'].split('/') and '\\' not in row['destination'] and
             row['destination'] not in seen, 'Invalid graph coordinate asset')
        need(all(type(row[k]) is int and row[k] > 0 for k in ('width', 'height', 'scale_to')),
             'Invalid graph dimensions')
        seen.add(row['destination'])


class Scope:
    def __init__(self, spec, source, correction):
        self.spec, self.name, self.p, self.c = spec, spec['name'], source, correction
        self.prefix = 'segments/' + self.name
        self.blocks = {b['id']: b for b in source['blocks']}
        self.regions = {r['id']: r for r in source['regions']}
        self.assets = {r['region_id']: r['asset'] for r in source['region_assets']}
        self.figures = {f['id'] for f in source['figures']}
        self.ranges = block_ranges(source)
        self.defs = set()
        need(correction.get('character_perfect_code') is False and
             not any(b['kind'] == 'code' for b in source['blocks']), 'News cannot infer encoded code')
        need(set(correction) <= set(DOMAIN) | METADATA | set(EMPTY) | {'regional_text_ranges', 'prose_joins'},
             'Unknown news correction field; add an explicit projection')
        need(all(correction.get(k) == [] for k in EMPTY), 'Unsupported news listing/label structures')
        need(correction['blocks'] == source['blocks'], 'News correction blocks differ from source')
        self.regional = {v['region_id']: v for v in correction['regional_text_ranges']}
        need(len(self.regional) == len(correction['regional_text_ranges']) and
             set(self.regional) == set(correction['regional_transcription']), 'News regional coverage differs')
        for rid, row in self.regional.items():
            need(row['text'] == correction['regional_transcription'][rid] and
                 row['scan'] == self.assets.get(rid), 'News regional reading or scan changed')
        for key in DOMAIN:
            for row in correction.get(key, []):
                kind = row.get('kind')
                if kind in DEFINING:
                    entity_kind, field = DEFINING[kind]
                    self.define(entity_kind, row[field])
                if key == 'tables':
                    self.define('table', row['table_id'])
                    for r in row['rows']: self.define('row', r['row_id'])
                    for category in row.get('source_categories', []): self.define('award-category', category)
                if key in ('literal_source_fields', 'source_literal_index', 'source_uncertainties'):
                    for name in ('field_id', 'literal_id', 'qualification_id'):
                        if name in row: self.define(REFS[name], row[name])
                if kind == 'source-print-specimen': self.define('specimen', row['id'])
                if kind == 'source-prose-processing-sequence':
                    for stage in row['stages']: self.define('stage', stage['stage_id'])

    def define(self, kind, value):
        need(isinstance(value, str) and value and (kind, value) not in self.defs,
             'Duplicate or blank news identity: ' + kind)
        self.defs.add((kind, value))

    def entity(self, kind, value):
        need((kind, value) in self.defs, 'Unknown news '+kind+': '+str(value))
        return self.name + ':' + kind + ':' + value

    def identity(self, value, allowed):
        need(value in allowed, 'Unknown news source reference: '+str(value))
        return self.name + '-' + value

    def ref(self, key, index):
        return dict(corrections=rebase(self.p['corrections'][0], self.prefix), pointer=f'/{key}/{index}')

    def revise(self, value, ranges, owner=None):
        from .assembly_structured import checked_span
        if isinstance(value, list): return [self.revise(v, ranges, owner) for v in value]
        if not isinstance(value, dict): return deepcopy(value)
        owner = value.get('block_id', owner)
        if owner is not None: self.identity(owner, self.blocks)
        if 'kind' in value: need(value['kind'] in KINDS, 'Unknown news semantic kind')
        result = {}
        for key, item in value.items():
            if key.endswith(('_verified', '_applied', '_expanded')) or key in FALSE:
                need(item is False, 'News assembly cannot establish verification or repair source values')
            if item is None: result[key] = None
            elif key in BLOCKS: result[key] = self.identity(item, self.blocks)
            elif key in BLOCK_LISTS: result[key] = [self.identity(v, self.blocks) for v in item]
            elif key in REGIONS: result[key] = self.identity(item, self.regions)
            elif key in REGION_LISTS: result[key] = [self.identity(v, self.regions) for v in item]
            elif key == 'figure_id': result[key] = self.identity(item, self.figures)
            elif key == 'category_id' and value.get('row_kind') == 'award':
                result[key] = self.entity('award-category', item)
            elif key == 'source_categories':
                result[key] = [self.entity('award-category', v) for v in item]
            elif key in REFS: result[key] = self.entity(REFS[key], item)
            elif key in LIST_REFS: result[key] = [self.entity(LIST_REFS[key], v) for v in item]
            elif key == 'id' and value.get('kind') == 'source-print-specimen':
                result[key] = self.entity('specimen', item)
            elif key == 'parent_article_id':
                need(item == self.p['id'], 'Wrong news parent article'); result[key] = item
            elif key == 'scan':
                rid = next((value[k] for k in ('region_id', 'figure_region_id', 'source_region_id') if k in value), None)
                need(item in self.assets.values() and (rid is None or item == self.assets.get(rid)),
                     'News scan differs from its source region')
                result[key] = rebase(item, self.prefix)
            elif key == 'prior_package':
                # Historical pins are retained under a named source scope. Their
                # relation to the included predecessor is verified at resolution.
                result['prior_source_declaration'] = deepcopy(item)
            else:
                need(not key.endswith(('_id', '_ids')), 'Unknown news identity field: '+key)
                result[key] = self.revise(item, ranges, owner)
        if 'start_byte' in value or 'end_byte' in value:
            need(owner is not None and 'start_byte' in value and 'end_byte' in value,
                 'Incomplete news block span')
            a, z = value['start_byte'], value['end_byte']
            literal = value.get('literal', value.get('text', value.get('separator')))
            checked_span(self.blocks[owner]['text'].encode(), a, z, literal)
            if S in value or E in value:
                need((value.get(S), value.get(E)) == (self.ranges[owner][0]+a, self.ranges[owner][0]+z),
                     'News original article/block coordinates differ')
            result.update({S: ranges[self.name+'-'+owner][0]+a, E: ranges[self.name+'-'+owner][0]+z})
            if 'source_segments' in value:
                cursor = a
                for part in value['source_segments']:
                    need(part['block_start_byte'] == cursor and part['block_end_byte'] >= cursor,
                         'News source parts have a gap or overlap')
                    cursor = part['block_end_byte']
                need(cursor == z, 'News source parts do not cover literal')
        if 'regional_start_byte' in value:
            need(owner is not None, 'News source part has no block owner')
            region = self.regional.get(value.get('region_id'))
            need(region is not None and region['block_id'] == owner, 'News part has wrong regional owner')
            a, z = value['regional_start_byte'], value['regional_end_byte']
            checked_span(region['text'].encode(), a, z)
            need((value['block_start_byte'], value['block_end_byte']) == (region['start_byte']+a, region['start_byte']+z)
                 and (value[S], value[E]) == (self.ranges[owner][0]+region['start_byte']+a,
                                             self.ranges[owner][0]+region['start_byte']+z),
                 'News regional/block/article coordinates differ')
            result[S] = ranges[self.name+'-'+owner][0]+value['block_start_byte']
            result[E] = ranges[self.name+'-'+owner][0]+value['block_end_byte']
        return result


def project_news(recipe, originals):
    from .assembly_structured import INDEXES, project_structured
    validate_recipe(recipe)
    scopes = [Scope(spec, *source) for spec, source in zip(recipe['segments'], originals, strict=True)]
    prepared = []
    for scope in scopes:
        c = {k: deepcopy(scope.c[k]) for k in METADATA -
             {'regional_transcription', 'source_readings_base', 'character_perfect_code'} if k in scope.c}
        c.update({k: deepcopy(scope.c.get(k, [])) if k in ('regional_text_ranges', 'prose_joins') else [] for k in INDEXES})
        prepared.append((scope.p, c))
    package, correction = project_structured(base_recipe(recipe), prepared)
    ranges = block_ranges(package)
    for key in DOMAIN: correction[key] = []
    projected = {}
    for scope in scopes:
        for key in DOMAIN:
            for i, row in enumerate(scope.c.get(key, [])):
                revised = scope.revise(row, ranges)
                revised.update(source_segment=scope.name, source_ref=scope.ref(key, i))
                projected[(scope.name, key, i)] = revised
                correction[key].append(revised)
        # Retain the complete unprojected source declarations in immutable scope.
        segment = next(v for v in correction['segments'] if v['name'] == scope.name)
        segment['original_metadata'] = {k: deepcopy(v) for k, v in scope.c.items()
                                       if k not in DOMAIN and k not in INDEXES and k not in {'records', 'blocks', 'map'}}
        check_ownership(scope)
    resolve(recipe, scopes, projected, correction)
    bound = set()
    for asset in recipe['coordinate_assets']:
        scope = next(s for s in scopes if s.name == asset['segment'])
        key = (scope.name, 'figure_structures', asset['figure_structure'])
        need(key in projected and key not in bound, 'Duplicate or missing graph coordinate binding')
        row = projected[key]; source = scope.c['figure_structures'][asset['figure_structure']]
        need(source['kind'] == 'printed-character-bar-report', 'Coordinate asset needs a bar report')
        region = scope.regions[source['source_region_id']]
        need(asset['source_index'] == region['source_index'] and asset['bbox'] == region['bbox'],
             'Graph crop differs from the observed source region')
        box = asset['pixel_bounds']; w, h = asset['page_size']
        need(box == [math.floor(region['bbox'][0]*w), math.floor(region['bbox'][1]*h),
                     math.ceil(region['bbox'][2]*w), math.ceil(region['bbox'][3]*h)] and
             (asset['width'], asset['height']) == (box[2]-box[0], box[3]-box[1]),
             'Graph coordinate transform differs from review crop dimensions')
        for observation in source['rows']:
            a, b, c, d = observation['observed_bar_box']
            need(0 <= a < c <= asset['width'] and 0 <= b < d <= asset['height'] and
                 observation['exact_repetition_count'] is None, 'Invalid or invented bar geometry')
        panels = [p for p in scope.c['content_associations'] if p['kind'] == 'source-output-panel'
                  and p['panel_id'] == source['panel_id'] and p['figure_id'] == source['figure_id']]
        need(len(panels) == 1, 'Bar report needs one owned output panel')
        table = next(t for t in scope.c['tables'] if t['table_id'] == panels[0]['table_id'])
        rows = {r['row_id']: r for r in table['rows'] if r['row_kind'] != 'header'}
        need([r['row_id'] for r in source['rows']] == list(rows), 'Bar rows differ from output table')
        for observation in source['rows']:
            cells = rows[observation['row_id']]['cells']
            need(observation['date_source'] == cells[0]['source'] and
                 observation['amount_source'] == cells[1]['source'], 'Bar labels have wrong table ownership')
        row['coordinate_asset'] = dict(asset['asset'], path=asset['destination'])
        row['coordinate_transform'] = {k: deepcopy(asset[k]) for k in
                                      ('width', 'height', 'source_index', 'bbox', 'scale_to', 'page_size', 'pixel_bounds')}
        row['native_scan_uses_coordinate_basis'] = False
        bound.add(key)
    need(bound == {key for key, row in projected.items() if row.get('kind') == 'printed-character-bar-report'},
         'Every manually observed bar report requires its exact coordinate raster')
    correction['source_index_mode'] = 'regional-news-v1'
    correction['character_perfect_code'] = False
    return package, correction


def check_ownership(scope):
    """Typed item/category/table ownership, including source blanks and ditto scope."""
    c = scope.c
    items = {r['news_item_id']: r for r in c['content_associations'] if r['kind'] == 'source-news-item'}
    categories = {r['category_id']: r for r in c['content_associations'] if r['kind'] == 'source-news-category'}
    def ancestors(name):
        seen = set()
        while name is not None:
            need(name in categories and name not in seen, 'Unknown or cyclic news category parent')
            seen.add(name)
            name = categories[name]['parent_category_id']
        return seen
    for name, item in items.items():
        need(item['category_id'] in categories and name in categories[item['category_id']]['item_ids'],
             'News item has wrong category owner')
        bodies = item.get('body_block_ids', [item.get('body_block_id')])
        need(all(b in scope.blocks for b in bodies) and item['logical_region_ids'] ==
             [rid for b in bodies for rid in scope.blocks[b]['region_ids']], 'News logical body ownership differs')
    for category in categories.values():
        need(len(set(category['item_ids'])) == len(category['item_ids']) and
             all(i in items and category['category_id'] in ancestors(items[i]['category_id']) for i in category['item_ids']),
             'News category membership differs')
    for row in c['content_associations']:
        if row['kind'] == 'source-news-paragraph':
            item = items.get(row['news_item_id']); owner = row['source']['block_id']
            need(item is not None and owner in item.get('body_block_ids', [item.get('body_block_id')]),
                 'News paragraph has wrong item owner')
    for table in c.get('tables', []):
        need(table['news_item_id'] in items, 'Table has unknown news owner')
        prior = set()
        for row in table['rows']:
            need(row['region_id'] in scope.blocks[table['block_id']]['region_ids'] and
                 len(row['cells']) == len(table['columns']), 'Table row ownership or columns differ')
            for i, cell in enumerate(row['cells']):
                need(cell['column'] == i and cell['column_name'] == table['columns'][i] and
                     cell['source']['block_id'] == table['block_id'] and cell['source']['literal'] == cell['text'] and
                     (cell['start_byte'], cell['end_byte']) == (cell['source']['start_byte'], cell['source']['end_byte']) and
                     row['start_byte'] <= cell['start_byte'] <= cell['end_byte'] <= row['end_byte'],
                     'Table cell columns, literal or source owner differ')
                need((cell['text'] == '') == (cell['state'] == 'observed-blank'), 'Printed blank was filled or erased')
            for key in ('rank_scope_from_row', 'school_ditto_from_row', 'role_scope_from_row'):
                if row.get(key) is not None:
                    need(row[key] in prior, 'Table scope must refer to an earlier row in this table')
            prior.add(row['row_id'])


def resolve(recipe, scopes, projected, correction):
    by_name = {s.name: s for s in scopes}
    used = set(); records = []
    def occurrence(ref, kind):
        key = (ref['segment'], 'content_associations', ref['association'])
        need(key in projected and key not in used and projected[key]['kind'] == kind,
             'Wrong, missing or reused news declaration')
        used.add(key)
        return by_name[ref['segment']], projected[key], by_name[ref['segment']].c['content_associations'][ref['association']]
    for i, link in enumerate(recipe['news_links']['boundaries']):
        left, outgoing, a = occurrence(link['left'], 'source-segment-boundary')
        right, incoming, z = occurrence(link['right'], 'source-segment-opening')
        need(left is scopes[i] and right is scopes[i+1] and
             a['selected_folios'] == [int(p['printed_page']) for p in left.p['pages']] and
             a['pending_folios'] == [int(p['printed_page']) for s in scopes[i+1:] for p in s.p['pages']] and
             a['next_category_literal'] == z['current_heading_source']['literal'] and
             z['paragraph_continues'] is False, 'News category boundary differs from source coverage')
        prior = z['prior_package']
        need(set(prior) == {'package', 'manifest', 'evidence', 'extent', 'preserveExactly'} and
             prior['manifest'] == left.spec['manifest'] and prior['package'] == str(left.spec['manifest']['path']).rsplit('/',1)[0] and
             prior['extent'] == [int(left.p['pages'][0]['printed_page']), int(left.p['pages'][-1]['printed_page'])] and
             prior['preserveExactly'] is True, 'News opening does not pin its included predecessor')
        for row in (outgoing, incoming):
            need(row['article_complete'] is False and row['whole_article_assembly_required'] is True,
                 'News boundary declaration is already resolved')
            row.update(article_complete=True, whole_article_assembly_required=False, status='resolved-category-boundary')
        outgoing['pending_folios'] = []
        incoming['prior_segment'] = left.name
        records.append(dict(kind='category-boundary', left=outgoing['source_ref'], right=incoming['source_ref'],
                            paragraph_continues=False, evidence=link['evidence']))
    link = recipe['news_links']['endings'][0]
    scope, ending, original = occurrence(link['source'], 'source-article-ending')
    need(scope is scopes[-1] and not original['pending_source_folios'] and
         original['closing_printed_folio'] == int(scope.p['pages'][-1]['printed_page']) and
         original['closing_region_id'] in scope.regions and
         scope.regions[original['closing_region_id']]['kind'] == 'figure' and
         original['next_printed_folio'] == original['closing_printed_folio']+1 and
         original['article_complete'] is False and original['whole_article_assembly_required'] is True,
         'News ending differs from final source view')
    ending.update(article_complete=True, whole_article_assembly_required=False, status='resolved-article-ending')
    records.append(dict(kind='article-ending', source=ending['source_ref'], evidence=link['evidence']))
    expected = {key for key, row in projected.items() if row.get('kind') in
                ('source-segment-boundary', 'source-segment-opening', 'source-article-ending')}
    need(used == expected, 'Unresolved news segment declarations')
    for row in correction['content_associations']:
        if row['kind'] == 'source-news-category':
            need(row.get('whole_article_complete', False) is False, 'Source category is already assembled')
            row['whole_article_complete'] = True
    correction['resolved_news_declarations'] = records


def copy_assets(root, stage, recipe):
    from .build import copy_pin
    for row in recipe['coordinate_assets']:
        copy_pin(root, stage, row['asset'], row['destination'])
    check_assets(stage, recipe)


def check_assets(folder, recipe):
    from PIL import Image
    from .build import checked
    for row in recipe['coordinate_assets']:
        checked(folder, dict(row['asset'], path=row['destination']))
        with Image.open(folder / row['destination']) as image:
            need(image.size == (row['width'], row['height']), 'Graph coordinate raster dimensions differ')
