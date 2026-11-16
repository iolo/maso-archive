"""Lossless assembly of heterogeneous native indexes in explicit source scopes.

An index value keeps its original IDs and coordinates. Its envelope supplies a
checked source pointer, closed typed references and ranges in the assembled
downloads. This avoids changing historical corrections to fit a later schema.
Review-only pins remain in the immutable original correction context.
"""
from collections import Counter
from copy import deepcopy
from types import SimpleNamespace

from .assemble import rebase, text_bytes
from .assembly_examples import join_blocks
from .assembly_indexes import block_ranges
from .assembly_structured import INDEXES, METADATA, checked_span
from .package import validate_package

MODE = 'scoped-native-v1'
NATIVE_INDEXES = INDEXES + ('text_index', 'unresolved_graphics', 'unresolved_text',
    'table_source_literals', 'source_byte_qualifications', 'recognition_disagreements',
    'bibliography_entries')
SOURCE_METADATA = METADATA | {'previous_package_manifest', 'character_perfect_code'}
S, E = 'utf8_byte_start', 'utf8_byte_end_exclusive'
REFS = {
    'block_id': 'block', 'code_block_id': 'block', 'caption_block_id': 'block',
    'heading_block_id': 'block', 'region_id': 'region', 'figure_region_id': 'region',
    'caption_region_id': 'region', 'source_region_id': 'region', 'figure_id': 'figure',
    'table_id': 'table', 'source_table_id': 'table', 'listing_id': 'listing',
    'label_id': 'label', 'branch_label_id': 'label', 'bit_label_id': 'label',
    'port_label_id': 'label', 'horizontal_label': 'label', 'vertical_label': 'label',
    'node_id': 'node', 'from_node': 'node', 'to_node': 'node', 'edge_id': 'edge',
    'slot_id': 'slot', 'row_id': 'row', 'cell_id': 'cell', 'table_cell_id': 'cell',
    'line_id': 'line', 'physical_line_id': 'physical', 'source_unit_id': 'logical',
    'following_address_line_id': 'physical', 'following_type_line_id': 'physical',
    'paragraph_id': 'paragraph',
}
REF_LISTS = {'block_ids': 'block', 'region_ids': 'region', 'figure_ids': 'figure',
    'table_ids': 'table', 'physical_line_ids': 'physical', 'source_row_ids': 'row',
    'annotation_label_ids': 'label', 'program_line_ids': 'physical',
    'interaction_line_ids': 'physical', 'repeated_print_line_ids': 'physical'}


def validate_recipe(recipe):
    required = {'index_mode', 'source_index_mode', 'segments', 'expected_source_indices',
        'inventory', 'evidence', 'uncertainties', 'resolved_notes', 'prose_joins',
        'paragraph_links', 'logical_aliases'}
    if (set(recipe) != required or recipe['source_index_mode'] != MODE or
            recipe['index_mode'] != 'structured-programs-v1'):
        raise ValueError('Invalid scoped native recipe fields or mode')
    # Reuse the common strict inventory, segment, note and prose-join contract.
    from .assembly_structured import validate_recipe as validate_common
    common = {k: v for k, v in recipe.items()
              if k not in {'source_index_mode', 'paragraph_links', 'logical_aliases'}}
    common.update(relationship_links=[], program_links=[], group_links=[], example_links=[])
    validate_common(common)
    names = [r['name'] for r in recipe['segments']]
    aliases = set()
    for row in recipe['logical_aliases']:
        if (set(row) != {'segment', 'index', 'source_unit_id'} or row['segment'] not in names or
                type(row['index']) is not int or row['index'] < 0 or
                not isinstance(row['source_unit_id'], str) or not row['source_unit_id'] or
                (row['segment'], row['index']) in aliases):
            raise ValueError('Invalid explicit logical identity alias')
        aliases.add((row['segment'], row['index']))
    for row in recipe['paragraph_links']:
        if (set(row) != {'left', 'right', 'separator', 'evidence'} or
                row['separator'] not in ('', ' ', '\n\n') or
                not isinstance(row['evidence'], str) or not row['evidence'].strip()):
            raise ValueError('Invalid scoped paragraph continuity link')
        for side in ('left', 'right'):
            part = row[side]
            if (set(part) != {'segment', 'association', 'literal'} or part['segment'] not in names or
                    type(part['association']) is not int or part['association'] < 0 or
                    not isinstance(part['literal'], str) or not part['literal']):
                raise ValueError('Invalid source paragraph occurrence')
        if names.index(row['right']['segment']) != names.index(row['left']['segment']) + 1:
            raise ValueError('Paragraph link must cross consecutive segments')


def walk(value, pointer=''):
    if isinstance(value, dict):
        yield pointer, value
        for key, child in value.items():
            yield from walk(child, pointer + '/' + key.replace('~', '~0').replace('/', '~1'))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from walk(child, pointer + '/' + str(i))


class Scope:
    def __init__(self, spec, package, correction, listing_offset, aliases):
        self.name, self.prefix = spec['name'], 'segments/' + spec['name']
        self.package, self.correction = package, correction
        self.listing_offset = listing_offset
        self.blocks = {r['id']: r for r in package['blocks']}
        self.groups = {r['listing_id']: r for r in correction.get('listing_groups', [])}
        self.label_owners = {r['label_id']: r.get('figure_id')
                             for r in correction.get('figure_label_index', [])}
        self.assets = {r['region_id']: r['asset'] for r in package['region_assets']}
        self.records = {r['id']: r for r in correction['records']}
        self.article, self.listing = text_bytes(package)
        self.ranges = block_ranges(package)
        self.definitions = {}
        self.used_aliases = []
        if set(correction) - set(NATIVE_INDEXES) - SOURCE_METADATA:
            raise ValueError('Unknown scoped native index; add an explicit contract')
        for field in NATIVE_INDEXES:
            if field in correction and not isinstance(correction[field], list):
                raise ValueError('Native index must be an explicit array')
        for kind, field in [('block', 'blocks'), ('figure', 'figures'), ('region', 'regions')]:
            for i, row in enumerate(package[field]):
                self.define(kind, row['id'], f'package/{field}/{i}', active=self.name + '-' + row['id'])
        for i, row in enumerate(package['excluded_regions']):
            self.define('region', row['id'], f'package/excluded_regions/{i}', active=self.name + '-' + row['id'])
        for field, kind, key in [('tables', 'table', 'table_id'),
                ('listing_groups', 'listing', 'listing_id'), ('figure_label_index', 'label', 'label_id'),
                ('listing_line_index', 'physical', 'line_id')]:
            for i, row in enumerate(correction.get(field, [])):
                self.define(kind, row[key], f'/{field}/{i}')
        for i, row in enumerate(correction.get('logical_listing_line_index', [])):
            if 'line_id' not in row:
                alias = dict(segment=self.name, index=i, source_unit_id=row.get('source_unit_id'))
                if alias not in aliases:
                    raise ValueError('Missing explicit source-unit identity alias')
                self.used_aliases.append(alias)
            elif row.get('source_unit_id', row['line_id']) != row['line_id']:
                raise ValueError('Conflicting logical source identity')
            self.define('logical', row.get('line_id', row.get('source_unit_id')),
                        f'/logical_listing_line_index/{i}')
        for i, row in enumerate(correction.get('content_associations', [])):
            if 'paragraph_id' in row:
                self.define('paragraph', row['paragraph_id'], f'/content_associations/{i}')
        for i, table in enumerate(correction.get('tables', [])):
            for j, row in enumerate(table['rows']):
                self.define('row', row['row_id'], f'/tables/{i}/rows/{j}')
                for k, cell in enumerate(row['cells']):
                    self.define('cell', cell['cell_id'], f'/tables/{i}/rows/{j}/cells/{k}')
        for i, figure in enumerate(correction.get('figure_structures', [])):
            scope = figure.get('figure_id', '')
            for pointer, row in walk(figure, f'/figure_structures/{i}'):
                for key, kind in [('node_id', 'node'), ('edge_id', 'edge'),
                                  ('slot_id', 'slot'), ('row_id', 'row')]:
                    if key in row:
                        self.define(kind, row[key], pointer, scope=scope)
        self.validate_text()

    def define(self, kind, id, pointer, *, scope='', active=None):
        if not isinstance(id, str) or not id:
            raise ValueError('Missing native identity')
        key = (kind, scope, id)
        if key in self.definitions:
            raise ValueError('Duplicate scoped native identity: ' + str(key))
        self.definitions[key] = dict(kind=kind, scope=scope, source_id=id,
            id=active or f'{self.name}:{kind}:{scope}:{id}', pointer=pointer)

    def reference(self, kind, id, scope=''):
        if kind == 'label' and scope and self.label_owners.get(id) not in (None, scope):
            raise ValueError('Native label belongs to another source figure')
        if kind == 'line':
            candidates = [self.definitions[k] for k in [('physical', '', id), ('logical', '', id)]
                          if k in self.definitions]
        else:
            keys = [(kind, scope, id)] if kind in ('node', 'edge', 'slot') else [(kind, '', id)]
            if kind == 'row' and scope:
                keys.append((kind, scope, id))
            candidates = [self.definitions[k] for k in keys if k in self.definitions]
            if kind in ('node', 'slot') and not scope:
                candidates = [v for (k, _, i), v in self.definitions.items() if k == kind and i == id]
        if len(candidates) != 1:
            raise ValueError(f'Unknown or ambiguous scoped {kind}: {scope}/{id}')
        return candidates[0]['id']

    def validate_text(self):
        coverage = {id: Counter() for id in self.blocks}
        seen = []
        for row in self.correction.get('regional_text_ranges', []):
            block, region = row['block_id'], row['region_id']
            if region in seen or region not in self.blocks[block]['region_ids']:
                raise ValueError('Duplicate or wrong-owner native region')
            seen.append(region)
            checked_span(self.blocks[block]['text'].encode(), row['start_byte'], row['end_byte'], row['text'])
            coverage[block].update(range(row['start_byte'], row['end_byte']))
        for row in self.correction.get('prose_joins', []):
            checked_span(self.blocks[row['block_id']]['text'].encode(), row['start_byte'], row['end_byte'], row['separator'])
            coverage[row['block_id']].update(range(row['start_byte'], row['end_byte']))
        if (set(seen) != {r for b in self.blocks.values() for r in b['region_ids']} or
                any(len(c) != len(self.blocks[id]['text'].encode()) or any(v != 1 for v in c.values())
                    for id, c in coverage.items())):
            raise ValueError('Native regional text is not an exact partition')
        physical = self.correction.get('listing_line_index', [])
        by_id = {r['line_id']: r for r in physical}
        for row in physical:
            checked_span(self.listing, row[S], row[E], row['text'])
            checked_span(self.blocks[row['block_id']]['text'].encode(),
                         row['block_start_byte'], row['block_end_byte'], row['text'])
            for f in row.get('fields', []):
                checked_span(row['text'].encode(), f['start_byte'], f['end_byte'], f['literal'])
                checked_span(self.blocks[row['block_id']]['text'].encode(),
                             f['block_start_byte'], f['block_end_byte'], f['literal'])
        units = self.correction.get('logical_listing_line_index', [])
        parts = []
        for row in units:
            ids = row['physical_line_ids']
            if not ids or any(id not in by_id for id in ids):
                raise ValueError('Logical unit has unknown physical rows')
            checked_span(self.listing, row[S], row[E], ''.join(by_id[id]['text'] for id in ids))
            parts.extend(ids)
        if Counter(parts) != Counter(list(by_id)):
            raise ValueError('Logical units do not partition physical listing rows')
        code = [b for b in self.blocks.values() if b['kind'] == 'code']
        groups = self.correction.get('listing_groups', [])
        if (Counter(id for g in groups for id in g['block_ids']) != Counter(b['id'] for b in code) or
                any(len(g['block_ids']) != 1 for g in groups)):
            raise ValueError('Native listing groups do not cover independent code contexts')
        if ''.join(r['text'] for r in physical).encode() != self.listing:
            raise ValueError('Physical listing rows differ from source order')

    def source_ref(self, pointer):
        return dict(corrections=rebase(self.package['corrections'][0], self.prefix), pointer=pointer)

    def envelope(self, field, index, positions, active_ranges, active_article, active_listing):
        original = self.correction[field][index]
        refs, spans, assets = [], [], []
        # Native values are intentionally unchanged. All bindings below are explicit.
        def visit(value, pointer='', owner=None, figure='', download=None, line=None):
            if isinstance(value, list):
                for i, child in enumerate(value):
                    visit(child, pointer + '/' + str(i), owner, figure, download, line)
                return
            if not isinstance(value, dict):
                return
            owner = value.get('block_id', owner)
            if owner is None and value.get('caption_block_id'):
                owner = value['caption_block_id']
            if owner is None and value.get('listing_id') in self.groups:
                ids = self.groups[value['listing_id']]['block_ids']
                if len(ids) != 1:
                    raise ValueError('Native source field requires one code owner')
                owner = ids[0]
            figure = value.get('figure_id', figure)
            download = value.get('download', download)
            literal = value.get('literal', value.get('text', value.get('separator')))
            if literal is not None and not isinstance(literal, str):
                literal = None
            def block_range(start, end, coordinate, expected=literal):
                if owner not in self.blocks:
                    raise ValueError('Native block range requires a known owner')
                try:
                    value = checked_span(self.blocks[owner]['text'].encode(), start, end, expected)
                except ValueError as error:
                    raise ValueError(f'Native {self.name}/{field}/{index}{pointer} '
                                     f'{coordinate} in {owner}: {error}') from error
                target, within = positions[self.name + '-' + owner]
                a = active_ranges[target][0] + within + start
                z = a + end - start
                checked_span(active_article, a, z, value)
                spans.append(dict(pointer=pointer, source_coordinate=coordinate,
                    source_block_id=owner, source_start_byte=start, source_end_byte=end,
                    download='article.txt', start_byte=a, end_byte=z, literal=value))
            for key, item in value.items():
                if key in ('execute_verified', 'execution_verified', 'original_encoded_bytes_verified') and item is not False:
                    raise ValueError('Assembly cannot establish execution or original encoded bytes')
                if item is None:
                    continue
                if key in REFS:
                    refs.append(dict(pointer=pointer + '/' + key,
                        id=self.reference(REFS[key], item, figure)))
                elif key in REF_LISTS:
                    refs.extend(dict(pointer=pointer + '/' + key + '/' + str(i),
                        id=self.reference(REF_LISTS[key], id, figure)) for i, id in enumerate(item))
                elif key == 'target_id':
                    kind = value.get('target_type')
                    if kind is None and value.get('kind') == 'source-figure-reference':
                        kinds = [k for k in ('figure', 'block', 'table')
                                 if (k, '', item) in self.definitions]
                        if len(kinds) == 1:
                            kind = kinds[0]
                    if kind not in ('figure', 'block', 'table'):
                        raise ValueError('Unknown native target type')
                    refs.append(dict(pointer=pointer + '/target_id', id=self.reference(kind, item)))
                elif key.endswith('_id') or key.endswith('_ids'):
                    raise ValueError('Unknown native identity field: ' + key)
            if 'scan' in value:
                asset = value['scan']
                region = value.get('region_id', value.get('figure_region_id'))
                if asset not in self.assets.values() or region is not None and self.assets.get(region) != asset:
                    raise ValueError('Native scan differs from its exported source region')
                assets.append(dict(pointer=pointer + '/scan', asset=rebase(asset, self.prefix)))
            for start_key, end_key in [('start_byte', 'end_byte'), ('block_start_byte', 'block_end_byte')]:
                if start_key in value or end_key in value:
                    if start_key not in value or end_key not in value:
                        raise ValueError('Incomplete native source range')
                    a, z = value[start_key], value[end_key]
                    if start_key == 'start_byte' and line is not None:
                        checked_span(line['text'].encode(), a, z, literal)
                        block_range(line['block_start_byte'] + a, line['block_start_byte'] + z,
                                    'physical-row-relative')
                    else:
                        block_range(a, z, start_key)
            if 'regional_start_byte' in value or 'regional_end_byte' in value:
                region = value.get('region_id')
                record = self.records.get(region, {})
                data = record.get('corrected_text')
                if not isinstance(data, str) or 'regional_start_byte' not in value or 'regional_end_byte' not in value:
                    raise ValueError('Native regional range requires original corrected text')
                checked_span(data.encode(), value['regional_start_byte'], value['regional_end_byte'], literal)
            if S in value or E in value:
                if S not in value or E not in value or download not in ('article.txt', 'listing.txt'):
                    raise ValueError('Native range requires an explicit download coordinate system')
                data = self.listing if download == 'listing.txt' else self.article
                literal = checked_span(data, value[S], value[E], literal)
                if download == 'listing.txt':
                    a, z = value[S] + self.listing_offset, value[E] + self.listing_offset
                    checked_span(active_listing, a, z, literal)
                else:
                    if owner is None or owner not in self.ranges:
                        raise ValueError('Article range requires a known source block owner')
                    base, end = self.ranges[owner]
                    if not base <= value[S] <= value[E] <= end:
                        raise ValueError('Native article range exceeds its source block')
                    target, within = positions[self.name + '-' + owner]
                    a = active_ranges[target][0] + within + value[S] - base
                    z = a + value[E] - value[S]
                    checked_span(active_article, a, z, literal)
                spans.append(dict(pointer=pointer, source_download=self.prefix + '/' + download,
                    source_start_byte=value[S], source_end_byte=value[E], download=download,
                    start_byte=a, end_byte=z, literal=literal))
            for key, child in value.items():
                # Review aids retain original provenance, not active export paths.
                if key not in ('scan', 'review_crop', 'source_context', 'evidence'):
                    child_line = value if field == 'listing_line_index' and key == 'fields' else line
                    visit(child, pointer + '/' + key, owner, figure, download, child_line)
        visit(original, download='listing.txt' if field in ('listing_index', 'listing_line_index',
            'logical_listing_line_index', 'source_literal_index', 'inline_source_fields',
            'source_byte_qualifications') else None)
        return dict(scope=self.name, source_ref=self.source_ref(f'/{field}/{index}'),
            value=deepcopy(original), references=refs, ranges=spans, assets=assets)


def project(recipe, originals):
    validate_recipe(recipe)
    contexts, offset = [], 0
    for spec, (source, correction) in zip(recipe['segments'], originals, strict=True):
        if source['schema_version'] != 2:
            raise ValueError('Scoped native assembly requires JPEG packages')
        context = Scope(spec, source, correction, offset, recipe['logical_aliases'])
        contexts.append(context)
        offset += len(context.listing)
    if [r for c in contexts for r in c.used_aliases] != recipe['logical_aliases']:
        raise ValueError('Unused or reordered logical identity alias')
    first = contexts[0].package
    package = deepcopy(first)
    for key in ('pages', 'regions', 'excluded_regions', 'blocks', 'figures',
                'content_order', 'raw_ocr', 'region_assets'):
        package[key] = []
    package.update(downloads=[], corrections=[], review_records=[], gaps=[])
    notes, records = [], []
    for c in contexts:
        source = c.package
        if any(source[k] != first[k] for k in
                ('id', 'issue_id', 'toc_entry_id', 'title', 'source', 'toc_pin', 'coordinates')):
            raise ValueError('Native segments have different canonical/source identities')
        old_notes = source['gaps'] + source['mapping']['uncertainties'] + source['verification']['uncertainties']
        old_notes += [n for b in source['blocks'] for n in b['uncertainties']]
        resolved = {r['note'] for r in recipe['resolved_notes'] if r['segment'] == c.name}
        if not resolved <= set(old_notes):
            raise ValueError('Resolved note is not an exact original uncertainty')
        notes.extend(f'[{c.name}] {n}' for n in dict.fromkeys(old_notes) if n not in resolved)
        package['pages'].extend(deepcopy(source['pages']))
        for field, kind in [('regions', 'region'), ('excluded_regions', 'region'),
                            ('blocks', 'block'), ('figures', 'figure')]:
            for old in source[field]:
                row = deepcopy(old)
                row['id'] = c.reference(kind, old['id'])
                if 'region_ids' in row:
                    row['region_ids'] = [c.reference('region', id) for id in old['region_ids']]
                if field == 'blocks':
                    row['uncertainties'] = [n for n in old['uncertainties'] if n not in resolved]
                    row['correction_evidence'] = ['corrections.json#' + id for id in row['region_ids']]
                if field == 'figures':
                    row['asset'] = rebase(old['asset'], c.prefix)
                package[field].append(row)
        package['content_order'].extend(dict(type=r['type'], id=c.reference(r['type'], r['id']))
                                       for r in source['content_order'])
        package['region_assets'].extend(dict(region_id=c.reference('region', r['region_id']),
            asset=rebase(r['asset'], c.prefix)) for r in source['region_assets'])
        package['raw_ocr'].extend(dict(region_ids=[c.reference('region', id) for id in r['region_ids']],
            **{k: rebase(r[k], c.prefix) for k in ('text', 'positions', 'settings')}) for r in source['raw_ocr'])
        for old in c.correction['records']:
            row = deepcopy(old)
            row.update(id=c.reference('region', old['id']), source_segment=c.name,
                source_ref=c.source_ref('/records/' + str(len([r for r in records if r['source_segment'] == c.name]))),
                scan=rebase(old['scan'], c.prefix),
                raw_ocr=rebase(old['raw_ocr'], c.prefix) if old['raw_ocr'] else None)
            records.append(row)
    indices = [p['source_index'] for p in package['pages']]
    orders = [p['reading_order'] for p in package['pages']]
    if (indices != recipe['expected_source_indices'] or len(set(indices)) != len(indices) or
            any(type(n) is not int or n < 1 for n in orders) or orders != sorted(set(orders))):
        raise ValueError('Native segments differ from exact ordered source coverage')
    from .assembly_structured import validate_pending_joins
    validate_pending_joins(recipe, [SimpleNamespace(name=c.name, source=c.package,
        correction=c.correction) for c in contexts])
    for i, c in enumerate(contexts):
        segment = c.correction.get('segment', {})
        later_folios = {int(p['printed_page']) for following in contexts[i + 1:]
                        for p in following.package['pages'] if str(p['printed_page']).isdigit()}
        if not set(segment.get('continuation_pending', [])) <= later_folios:
            raise ValueError('Native segment retains an uncovered source continuation')
        outgoing = segment.get('outgoing_prose')
        if outgoing is not None:
            rows = [r for r in recipe['prose_joins'] if r['left']['segment'] == c.name]
            if (i + 1 == len(contexts) or len(rows) != 1 or
                    rows[0]['left'] != dict(segment=c.name, block_id=outgoing['block_id'], ending=outgoing['literal']) or
                    rows[0]['right']['segment'] != contexts[i + 1].name or
                    rows[0]['right']['opening'] != outgoing['next_literal'] or
                    rows[0]['separator'] != outgoing['separator'] or
                    str(contexts[i + 1].package['pages'][0]['printed_page']) != str(outgoing['next_folio'])):
                raise ValueError('Native prose join differs from original outgoing declaration')
    positions, joined = join_blocks(recipe, package, [SimpleNamespace(name=c.name) for c in contexts])
    for c in contexts:
        for (kind, _, id), binding in c.definitions.items():
            if kind == 'block':
                target, within = positions[c.name + '-' + id]
                binding.update(id=target, offset_in_block=within)
    ranges = block_ranges(package)
    article, listing = text_bytes(package)
    if listing != b''.join(c.listing for c in contexts):
        raise ValueError('Native assembly changed independent source code bytes')
    native = {field: [] for field in NATIVE_INDEXES}
    for c in contexts:
        for field in NATIVE_INDEXES:
            native[field].extend(c.envelope(field, i, positions, ranges, article, listing)
                                 for i in range(len(c.correction.get(field, []))))
    continuations = []
    used = set()
    for link in recipe['paragraph_links']:
        fragments = []
        for side in ('left', 'right'):
            part = link[side]
            c = next(c for c in contexts if c.name == part['segment'])
            key = (c.name, part['association'])
            rows = c.correction.get('content_associations', [])
            if key in used or part['association'] >= len(rows):
                raise ValueError('Unknown or reused source paragraph occurrence')
            row = rows[part['association']]
            if row.get('kind') != 'source-paragraph' or row.get('literal') != part['literal']:
                raise ValueError('Paragraph continuity differs from source occurrence')
            entry = next(v for v in native['content_associations']
                         if v['scope'] == c.name and v['source_ref']['pointer'] == f'/content_associations/{part["association"]}')
            fragments.append(dict(source_ref=entry['source_ref'], ranges=entry['ranges'], literal=row['literal']))
            used.add(key)
        continuations.append(dict(kind='source-paragraph-continuation', fragments=fragments,
            separator=link['separator'], logical_display=link['left']['literal'] + link['separator'] + link['right']['literal'],
            evidence=link['evidence'], original_blocks_preserved=True))
    required_continuations = {(c.name, i) for c in contexts
        for i, r in enumerate(c.correction.get('content_associations', []))
        if any(r.get(k) for k in ('continues_next_segment', 'incoming_previous_segment',
                                  'outgoing_continuation', 'incoming_continuation'))}
    if not required_continuations <= used:
        raise ValueError('Native source paragraph continuation lacks an explicit disposition')
    package['gaps'] = list(dict.fromkeys(recipe['uncertainties'] + notes))
    package['mapping'] = dict(status='mapped', evidence=recipe['evidence'], uncertainties=[])
    package['availability'] = 'readable'
    package['verification'] = dict(status='sample-reviewed', reviewed_region_ids=[r['id'] for r in package['regions']],
        evidence=recipe['evidence'], uncertainties=package['gaps'])
    correction = dict(article_id=package['id'], index_mode=recipe['index_mode'], source_index_mode=MODE,
        policy='Native index values retain source-local identities and coordinates. Envelopes provide typed closed references and active download ranges. No OCR, encoded-byte inference or execution claim.',
        records=records, blocks=package['blocks'], native_indexes=native,
        scopes=[dict(name=c.name, original_corrections=rebase(c.package['corrections'][0], c.prefix),
            original_metadata={k: deepcopy(v) for k, v in c.correction.items() if k in SOURCE_METADATA - {'blocks', 'records', 'map'}},
            identities=list(c.definitions.values()),
            block_bindings=[dict(source_id=id, block_id=positions[c.name + '-' + id][0],
                offset_in_block=positions[c.name + '-' + id][1]) for id in c.blocks],
            coordinate_systems=dict(article=c.prefix + '/article.txt', listing=c.prefix + '/listing.txt')) for c in contexts],
        logical_aliases=deepcopy(recipe['logical_aliases']), resolved_notes=deepcopy(recipe['resolved_notes']),
        resolved_continuations=joined, paragraph_continuations=continuations,
        coverage=dict(article_source_indices=indices, complete_article=True, assembly_pending=False,
            source_pages_missing=False), character_perfect_code=False)
    validate_package(package)
    return package, correction
