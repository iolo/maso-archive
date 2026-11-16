"""Opt-in typed source observations over immutable native segment scopes.

Literal arithmetic, conversion groups, tables and bit drawings are observations,
never evaluated values. Legacy scoped-native-v1 accepts exactly its old fields.
"""
from collections import Counter
from .assembly_scoped_native import Scope, NATIVE_INDEXES, SOURCE_METADATA, REFS, REF_LISTS, walk

EXTRA_INDEXES = (
    'source_section_index', 'source_regional_line_index', 'source_paragraph_index',
    'source_table_cell_index', 'source_table_row_index', 'source_division_example_index',
    'source_division_row_index', 'source_division_field_index', 'source_grouped_conversion_index',
    'source_conversion_group_field_index', 'source_group_alignment_index', 'source_conversion_bit_index',
    'source_figure_structure_index', 'source_figure_row_index', 'source_figure_field_index',
    'source_figure_label_index', 'source_figure_connector_index', 'source_arithmetic_phase_index',
    'source_arithmetic_row_index', 'source_arithmetic_field_index', 'source_arithmetic_glyph_index',
    'source_caption_association_index', 'source_illustration_text_association_index',
    'source_prose_claim_index', 'source_inline_bit_expression_index', 'source_inline_bit_index',
    'source_range_claim_index', 'source_figure_context_index', 'source_byte_panel_association_index',
    'source_figure_bit_index', 'source_closing_mark_index', 'segment_continuations')
DEFINITIONS = {
    'source_section_index': ('section', 'section_id'),
    'source_paragraph_index': ('paragraph', 'paragraph_id'),
    'source_table_cell_index': ('cell', 'cell_id'),
    'source_table_row_index': ('row', 'row_id'),
    'source_division_example_index': ('example', 'example_id'),
    'source_division_row_index': ('row', 'row_id'),
    'source_division_field_index': ('field', 'field_id'),
    'source_grouped_conversion_index': ('example', 'example_id'),
    'source_conversion_group_field_index': ('field', 'field_id'),
    'source_group_alignment_index': ('alignment', 'alignment_id'),
    'source_conversion_bit_index': ('bit', 'bit_id'),
    'source_figure_structure_index': ('structure', 'structure_id'),
    'source_figure_row_index': ('row', 'row_id'),
    'source_figure_field_index': ('field', 'field_id'),
    'source_figure_label_index': ('label', 'label_id'),
    'source_figure_connector_index': ('connector', 'connector_id'),
    'source_arithmetic_phase_index': ('phase', 'phase_id'),
    'source_arithmetic_row_index': ('row', 'row_id'),
    'source_arithmetic_field_index': ('field', 'field_id'),
    'source_arithmetic_glyph_index': ('slot', 'slot_id'),
    'source_inline_bit_expression_index': ('expression', 'expression_id'),
    'source_inline_bit_index': ('bit', 'bit_id'),
    'source_range_claim_index': ('range', 'range_id'),
    'source_figure_bit_index': ('bit', 'bit_id'),
}


def require(value, message):
    if not value:
        raise ValueError(message)


class ObservationScope(Scope):
    native_indexes = NATIVE_INDEXES + EXTRA_INDEXES
    source_metadata = SOURCE_METADATA | {'coverage'}
    refs = {**REFS, 'from_block': 'block', 'to_block_id': 'block',
        'from_region': 'region', 'to_region': 'region', 'to_region_id': 'region',
        'prior_region_id': 'prior-region', 'text_region_id': 'region',
        'separate_text_region_id': 'region', 'section_id': 'section',
        'field_id': 'field', 'figure_field_id': 'field', 'upper_field_id': 'field',
        'lower_field_id': 'field', 'power_field_id': 'field', 'group_field_id': 'field',
        'example_id': 'example', 'structure_id': 'structure', 'phase_id': 'phase',
        'expression_id': 'expression', 'range_id': 'range', 'alignment_id': 'alignment',
        'column_id': 'column', 'connector_id': 'connector', 'bit_id': 'bit',
        'sign_bit_id': 'bit', 'lsb_bit_id': 'bit'}
    ref_lists = {**REF_LISTS, 'field_ids': 'field', 'row_field_ids': 'field',
        'row_ids': 'row', 'label_ids': 'label', 'connector_ids': 'connector',
        'phase_ids': 'phase', 'source_phase_order': 'phase', 'bit_ids': 'bit',
        'source_alignment_ids': 'alignment', 'cell_ids': 'source-cell',
        'source_order': 'column'}

    def define_additional(self):
        for field, (kind, key) in DEFINITIONS.items():
            for i, row in enumerate(self.correction.get(field, [])):
                if field == 'source_figure_structure_index' and row.get('kind') == 'original-photograph' and key not in row:
                    continue  # A captionless source image need not invent a separate structure ID.
                self.define(kind, row[key], f'/{field}/{i}')
        for i, struct in enumerate(self.correction.get('source_figure_structure_index', [])):
            for j, col in enumerate(struct.get('columns', [])):
                self.define('column', col['column_id'], f'/source_figure_structure_index/{i}/columns/{j}')
            for j, row in enumerate(struct.get('rows', [])):
                self.define('row', row['row_id'], f'/source_figure_structure_index/{i}/rows/{j}')
        for field in EXTRA_INDEXES:
            for _, value in walk(self.correction.get(field, [])):
                box = value.get('source_bbox_in_region')
                if box is not None:
                    require(isinstance(box, list) and len(box) == 4 and
                            all(type(v) in (int, float) for v in box) and
                            0 <= box[0] < box[2] <= 1 and 0 <= box[1] < box[3] <= 1,
                            'Observation context is outside its source region')
                path = value.get('source_path_in_region')
                if path is not None:
                    require(isinstance(path, list) and len(path) >= 2 and
                            all(isinstance(p, list) and len(p) == 2 and
                                all(type(v) in (int, float) and 0 <= v <= 1 for v in p) for p in path),
                            'Observation connector is outside its source region')
                for key in ('encoded_bytes', 'encoded_value', 'encoded_bit', 'evaluated_value',
                            'evaluated_bounds', 'computed_result', 'calculated_result', 'calculated_value'):
                    require(value.get(key) is None, 'Observation cannot establish computed or encoded values')
        validate_byte_strips(self.correction)

    def reference(self, kind, id, scope=''):
        if kind == 'prior-region':
            require(hasattr(self, 'prior'), 'Incoming observation lacks preceding source scope')
            return self.prior.reference('region', id)
        if kind == 'source-cell':
            matches = [k for k in ('cell', 'field') if (k, '', id) in self.definitions]
            require(len(matches) == 1, 'Unknown or ambiguous source cell identity')
            kind = matches[0]
        return super().reference(kind, id, scope)

    def reference_list(self, kind, items, pointer, figure):
        require(isinstance(items, list), 'Observation references require an explicit array')
        result = []
        for i, item in enumerate(items):
            location = pointer + '/' + str(i)
            if isinstance(item, list):
                result.extend(self.reference_list(kind, item, location, figure))
            else:
                result.append(dict(pointer=location, id=self.reference(kind, item, figure)))
        return result


def validate_continuations(recipe, contexts):
    """Close original deferred/incoming declarations without rewriting either."""
    def folios(values):
        require(isinstance(values, list) and all(type(v) in (str, int) and str(v) for v in values),
                'Observation coverage requires explicit source folios')
        return [str(v) for v in values]
    all_folios = folios([p['printed_page'] for c in contexts for p in c.package['pages']])
    matched, used = set(), set()
    for i, c in enumerate(contexts):
        coverage = c.correction.get('coverage', {})
        own = folios([p['printed_page'] for p in c.package['pages']])
        require(coverage.get('article_extent_verified') is True and
                folios(coverage.get('article_actual_folios')) == all_folios and
                folios(coverage.get('included_actual_folios')) == own and
                coverage.get('source_pages_missing') is False,
                'Observation source extent differs from complete ordered article coverage')
        later = folios([p['printed_page'] for following in contexts[i + 1:] for p in following.package['pages']])
        earlier = folios([p['printed_page'] for prior in contexts[:i] for p in prior.package['pages']])
        require(set(folios(coverage.get('deferred_actual_folios', []))) <= set(later) and
                set(folios(coverage.get('prior_native_actual_folios', []))) <= set(earlier),
                'Observation coverage retains unrepresented source pages')
        for j, outgoing in enumerate(c.correction.get('segment_continuations', [])):
            kind = outgoing.get('kind')
            if kind == 'incoming-source-prose-continuation':
                continue
            require(kind == 'deferred-source-prose-continuation' and i + 1 < len(contexts),
                    'Unknown or unrepresented observation continuation')
            following = contexts[i + 1]
            rows = [r for r in recipe['prose_joins'] if r['left']['segment'] == c.name and
                    r['left']['block_id'] == outgoing['from_block']]
            require(len(rows) == 1, 'Deferred observation requires one explicit prose join')
            join = rows[0]
            require(join['left']['ending'] == outgoing['last_source_text'] and
                    join['right']['segment'] == following.name and
                    join['right']['opening'] == outgoing['next_source_text'] and
                    join['separator'] == outgoing['separator'] and
                    str(following.package['pages'][0]['printed_page']) == str(outgoing['next_source_folio']) and
                    set(folios(outgoing['final_source_folios_required'])) <= set(later),
                    'Observation prose join differs from deferred source declaration')
            require(outgoing['from_region'] in c.blocks[outgoing['from_block']]['region_ids'],
                    'Deferred observation names the wrong source region')
            incoming = [(k, v) for k, v in enumerate(following.correction.get('segment_continuations', []))
                        if v.get('kind') == 'incoming-source-prose-continuation' and
                        v.get('to_block_id') == join['right']['block_id']]
            require(len(incoming) == 1, 'Deferred observation lacks its unique incoming declaration')
            k, inc = incoming[0]
            require((i + 1, k) not in used and inc['prior_native_manifest'] == c.spec['manifest'] and
                    inc['prior_region_id'] == outgoing['from_region'] and
                    inc['prior_text_end'] == outgoing['last_source_text'] and
                    inc['first_source_text'] == outgoing['next_source_text'] and
                    inc['separator'] == outgoing['separator'] and
                    str(inc['from_source_folio']) == own[-1] and
                    inc['to_region_id'] in following.blocks[inc['to_block_id']]['region_ids'] and
                    c.records[outgoing['from_region']]['corrected_text'].endswith(inc['prior_text_end']) and
                    following.records[inc['to_region_id']]['corrected_text'].startswith(inc['first_source_text']),
                    'Incoming observation differs from pinned preceding source declaration')
            following.prior = c
            matched.add((i, j));used.add((i + 1, k))
    declared = {(i, j) for i, c in enumerate(contexts)
                for j, _ in enumerate(c.correction.get('segment_continuations', []))}
    require(declared == matched | used, 'Observation continuation lacks an explicit disposition')


def check_intervening(items, actual, contexts):
    """Keep a source illustration and its independently indexed text in place."""
    require(actual == [dict(type=v['type'], id=v['segment'] + '-' + v['id']) for v in items],
            'Observation interruption differs from explicit reviewed content order')
    sources = {c.name: c for c in contexts}
    for i, item in enumerate(items):
        require(item['segment'] in sources, 'Unknown observation interruption scope')
        c = sources[item['segment']]
        if item['type'] == 'figure':
            c.reference('figure', item['id'])
            continue
        require(item['id'] in c.blocks, 'Unknown observation interruption block')
        block = c.blocks[item['id']]
        if block['kind'] == 'caption':
            continue
        preceding = items[i - 1] if i else {}
        associations = [v for v in c.correction.get('source_illustration_text_association_index', [])
                        if v.get('block_id') == item['id'] and v.get('literal') == block['text'] and
                        preceding == dict(segment=c.name, type='figure', id=v.get('figure_id'))]
        require(block['kind'] == 'prose' and len(associations) == 1,
                'Observation interruption requires its exact original illustration-text association')


def validate_byte_strips(correction):
    """Each drawn byte position owns one original cell outline in the same region."""
    bits = {v['bit_id']: v for v in correction.get('source_figure_bit_index', [])}
    for struct in correction.get('source_figure_structure_index', []):
        if struct.get('kind') != 'source-signed-byte-strips':
            continue
        ordered = []
        for row in struct['rows']:
            ids = row['bit_ids']
            require(len(ids) == len(set(ids)) == 8 and row['sign_bit_id'] == ids[0] and
                    row['lsb_bit_id'] == ids[-1], 'Source byte row requires eight ordered sign-to-LSB positions')
            for column, id in enumerate(ids, 1):
                bit = bits.get(id, {})
                require(bit.get('region_id') == struct['region_id'] and bit.get('column') == column and
                        bit.get('row') == row['ordinal'], 'Source byte position differs from its row and column')
            ordered.extend(ids)
        outlines = [v for v in correction.get('source_figure_connector_index', [])
                    if v.get('kind') == 'source-byte-cell-outline' and v.get('region_id') == struct['region_id']]
        require(Counter(v.get('bit_id') for v in outlines) == Counter(ordered),
                'Source byte positions and cell outlines must correspond exactly once')
        for outline in outlines:
            a, y, z, t = bits[outline['bit_id']]['source_bbox_in_region']
            require(outline['source_path_in_region'] == [[a, y], [z, y], [z, t], [a, t], [a, y]],
                    'Source byte outline differs from its original bit-cell context')
