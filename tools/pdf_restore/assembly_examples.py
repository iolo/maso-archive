"""Opt-in assembly of standalone examples and scan-linked text review ranges.

Source packages and historical index modes remain immutable. Explicit prose joins
preserve source coordinates beside projected UTF-8 ranges. Interrupted modes also
require the exact intervening image/caption order. They do not infer executable
programs or original glyph bytes.
"""
from copy import deepcopy
import re

from .assemble import project_legacy, rebase, text_bytes
from .assembly_indexes import END, START, Segment, block_ranges, namespace, span
from .package import validate_package


def validate_joins(rows, regional=False):
    if not isinstance(rows, list):
        raise ValueError('Standalone assembly requires explicit prose joins')
    for row in rows:
        if (not isinstance(row, dict) or set(row) != ({'left', 'right', 'separator', 'intervening'} if regional else {'left', 'right', 'separator'}) or
                row['separator'] not in ('', ' ', '\n\n')):
            raise ValueError('Invalid prose join')
        if regional:
            from .assembly_regional import validate_intervening
            validate_intervening(row['intervening'])
        for side, edge in (('left', 'ending'), ('right', 'opening')):
            part = row[side]
            if (not isinstance(part, dict) or set(part) != {'segment', 'block_id', edge} or
                    any(not isinstance(v, str) or not v for v in part.values())):
                raise ValueError('Prose join requires explicit source text and identity')


def join_blocks(recipe, package, contexts):
    """Return original namespaced block -> final block and byte offset within it."""
    blocks = {b['id']: b for b in package['blocks']}
    positions = {id: (id, 0) for id in blocks}
    names = [c.name for c in contexts]
    used, resolved = set(), []
    for row in recipe['prose_joins']:
        left, right = row['left'], row['right']
        if (left['segment'] not in names or right['segment'] not in names or
                names.index(right['segment']) != names.index(left['segment']) + 1):
            raise ValueError('Prose join must cross consecutive source segments')
        ids = [part['segment'] + '-' + part['block_id'] for part in (left, right)]
        if any(id not in blocks or id in used for id in ids):
            raise ValueError('Unknown or reused prose join block')
        a, b = (blocks[id] for id in ids)
        order = package['content_order']
        i = order.index(dict(type='block', id=ids[0]))
        j = order.index(dict(type='block', id=ids[1]))
        if recipe.get('index_mode') in ('regional-prose-v1', 'regional-listing-v1', 'regional-table-listing-v1', 'interrupted-wrapped-listing-v1'):
            from .assembly_regional import check_intervening
            check_intervening(row['intervening'], order[i + 1:j], contexts,
                              allow_wrapped_listings=recipe.get('index_mode') == 'interrupted-wrapped-listing-v1',
                              allow_indexed_tables=recipe.get('index_mode') == 'regional-table-listing-v1')
        elif j != i + 1:
            raise ValueError('Prose join differs from adjacent reviewed text')
        if (j <= i or
                a['kind'] != 'prose' or b['kind'] != 'prose' or
                not a['text'].endswith(left['ending']) or not b['text'].startswith(right['opening'])):
            raise ValueError('Prose join differs from adjacent reviewed text')
        offset = len((a['text'] + row['separator']).encode())
        a['text'] += row['separator'] + b['text']
        for key in ('region_ids', 'correction_evidence', 'uncertainties'):
            a[key] = list(dict.fromkeys(a[key] + b[key]))
        package['blocks'].remove(b)
        del order[j]
        positions[ids[1]] = (ids[0], offset)
        used.update(ids)
        resolved.append(dict(kind='prose', status='joined-reading-blocks', block_id=ids[0],
                             source_blocks=ids, separator=row['separator'], right_utf8_offset=offset,
                             evidence=deepcopy(row), source_text_preserved=True))
    return positions, resolved


def project_examples(recipe, originals):
    # Interrupted wrapped packages use existing block/range indexes; unlike the
    # regional modes, they do not require retrofitting immutable regional indexes.
    wrapped = recipe.get('index_mode') in ('wrapped-listing-v1', 'regional-listing-v1', 'regional-table-listing-v1', 'interrupted-wrapped-listing-v1', 'wrapped-scan-notes-v1')
    scan_notes = recipe.get('index_mode') == 'wrapped-scan-notes-v1'
    regional = recipe.get('index_mode') in ('regional-prose-v1', 'regional-listing-v1', 'regional-table-listing-v1')
    if regional and not wrapped and any(b['kind'] == 'code' for source, _ in originals for b in source['blocks']):
        raise ValueError('Regional prose mode cannot assemble code listings')
    contexts, offset, normalized = [], 0, []
    for spec, (source, correction) in zip(recipe['segments'], originals, strict=True):
        if correction.get('glyph_definitions'):
            raise ValueError('Glyph byte definitions require the existing listing assembly mode')
        context = Segment(spec, source, correction, offset)
        contexts.append(context)
        offset += len(context.listing)
        # Legacy projection accepts bytecode markers, not text-range glyph notes.
        # Remove only from this temporary projection; project and verify them below.
        copy = deepcopy(correction)
        copy['unresolved_graphics'] = []
        normalized.append(namespace(Segment(spec, source, copy, context.offset)))
    package, corrections = project_legacy(recipe, normalized)
    positions, resolved = join_blocks(recipe, package, contexts)
    ranges = block_ranges(package)
    article, listing = text_bytes(package)
    fields = ('text_index', 'source_text_index', 'text_review_items', 'unresolved_text',
              'unresolved_graphics', 'figure_sequence', 'figure_review_items', 'prose_joins',
              'listing_index', 'listing_line_index', 'listing_anomalies', 'listing_groups',
              'segment_continuations')
    corrections.update({key: [] for key in fields})
    corrections.update(index_mode=recipe['index_mode'], regional_transcription={},
                       reading_replacements={}, resolved_continuations=resolved, identity_map=[])
    if wrapped:
        corrections.update(logical_listing_line_index=[], data_statements=[], source_listing_groups=[])
    if scan_notes:
        corrections['unresolved_scan_notes'] = []
    if regional:
        from .assembly_regional import FIELDS
        corrections.update({field: [] for field in FIELDS})
    for context, segment_record in zip(contexts, corrections['segments'], strict=True):
        original = context.correction
        segment_record['original_corrections'] = rebase(context.source['corrections'][0], context.prefix)
        segment_record['original_metadata'] = deepcopy({k: v for k, v in original.items()
                                                        if k not in ('records', 'blocks', 'map')})
        for kind, allowed in (('region', context.regions), ('block', context.blocks), ('figure', context.figures)):
            for id in sorted(allowed):
                projected = context.identity(id, allowed)
                target, within = positions[projected] if kind == 'block' else (projected, 0)
                corrections['identity_map'].append(dict(source_segment=context.name, kind=kind,
                    source_id=id, id=target, source_namespace_id=projected, utf8_offset_in_block=within))

        def references(row):
            result = context.references(row)
            if result.get('block_id'):
                result['block_id'] = positions[result['block_id']][0]
            if 'block_ids' in result:
                result['block_ids'] = [positions[id][0] for id in result['block_ids']]
            result['source_segment'] = context.name
            return result

        def text_range(row, whole=False):
            value = span(row, context.article)
            if row.get('download') != 'article.txt' or row.get('block_id') not in context.blocks:
                raise ValueError('Invalid source text review identity')
            start, end = context.ranges[row['block_id']]
            if (not start <= row[START] < row[END] <= end or
                    (whole and (start, end) != (row[START], row[END])) or
                    (not whole and row.get('transcription_excerpt') != value)):
                raise ValueError('Text review differs from source block')
            revised = references(row)
            target, within = positions[context.identity(row['block_id'], context.blocks)]
            delta = ranges[target][0] + within - start
            revised.update(source_block_id=row['block_id'], source_range={START: row[START], END: row[END]},
                           **{START: row[START] + delta, END: row[END] + delta})
            if span(revised, article) != value:
                raise ValueError('Projected text review differs from original bytes')
            return revised

        rows = original.get('text_index', [])
        if len(rows) != len(context.blocks) or {r['block_id'] for r in rows} != context.blocks:
            raise ValueError('Text index must cover each source block')
        corrections['source_text_index'].extend(text_range(row, whole=True) for row in rows)
        for field in ('text_review_items', 'unresolved_text', 'unresolved_graphics'):
            for row in original.get(field, []):
                if scan_notes and field == 'unresolved_text' and START not in row and END not in row:
                    # Scan observations have no download range. Keep their identity
                    # and pinned evidence without inventing searchable byte offsets.
                    if (set(row) != {'region_id', 'block_id', 'scan', 'markers', 'note'} or
                            row['block_id'] not in context.blocks or
                            row['region_id'] not in next(b['region_ids'] for b in context.source['blocks']
                                                        if b['id'] == row['block_id']) or
                            row['scan'] != context.assets.get(row['region_id']) or
                            not isinstance(row['markers'], list) or not row['markers'] or
                            any(not isinstance(v, str) or not v.strip() for v in row['markers']) or
                            not isinstance(row['note'], str) or not row['note'].strip()):
                        raise ValueError('Invalid scan-only uncertainty note')
                    corrections['unresolved_scan_notes'].append(references(row))
                    continue
                if scan_notes and field == 'unresolved_text' and (START not in row or END not in row):
                    raise ValueError('Uncertainty range requires both byte bounds')
                if field == 'unresolved_graphics' and regional and 'marker' in row:
                    marker = row['marker']
                    identity = ('block_id', 'region_id', 'scan', 'download', START, END,
                                'marker', 'transcription_excerpt')
                    if (not isinstance(marker, str) or not re.fullmatch(r'⟦[^⟦⟧\r\n]+⟧', marker) or
                            row.get('transcription_excerpt') != marker or
                            row.get('status') != 'manual-correction-required' or
                            any(row.get(key) is not None for key in ('original_bytes', 'encoded_bytes')) or
                            any(key in row and row[key] is not False for key in
                                ('machine_byte_verified', 'source_encoding_verified')) or
                            not any(all(note.get(key) == row.get(key) for key in identity)
                                    for note in original.get('unresolved_text', []))):
                        raise ValueError('Graphic marker requires matching unresolved source text and unverified bytes')
                elif field == 'unresolved_graphics' and (not row.get('rendered_glyph') or
                        row['rendered_glyph'] not in row.get('transcription_excerpt', '') or
                        row.get('machine_byte_verified') is not False):
                    raise ValueError('Text glyph note requires an unverified rendered glyph')
                corrections[field].append(text_range(row))
        if regional:
            from .assembly_regional import project_regional
            project_regional(context, corrections, text_range)
            from .assembly_news import project_news
            project_news(context, corrections, text_range, positions)
        for id, text in original.get('regional_transcription', {}).items():
            corrections['regional_transcription'][context.identity(id, context.regions)] = deepcopy(text)
        for id, replacements in original.get('reading_replacements', {}).items():
            corrections['reading_replacements'][context.identity(id, context.regions)] = deepcopy(replacements)
        for field in ('figure_sequence', 'figure_review_items', 'prose_joins'):
            for row in original.get(field, []):
                revised = references(row)
                if field == 'figure_sequence':
                    caption_fields = {'caption_region_id', 'caption_download',
                                      'caption_utf8_byte_start', 'caption_utf8_byte_end_exclusive',
                                      'caption_scan', 'caption_text'}
                    # Historical caption identities without explicit spans keep
                    # their existing projection. New spans must prove their own
                    # caption block, region, bitmap and exact UTF-8 text first.
                    if caption_fields.intersection(row):
                        block = next((b for b in context.source['blocks']
                                      if b['id'] == row.get('caption_block_id')), None)
                        if (not caption_fields.issubset(row) or block is None or
                                block['kind'] != 'caption' or
                                row['caption_region_id'] not in block['region_ids'] or
                                row['caption_scan'] != context.assets.get(row['caption_region_id']) or
                                not isinstance(row['caption_text'], str) or not row['caption_text']):
                            raise ValueError('Figure caption span requires its source caption block and scan')
                        caption = text_range(dict(block_id=block['id'],
                            region_id=row['caption_region_id'], scan=row['caption_scan'],
                            download=row['caption_download'],
                            utf8_byte_start=row['caption_utf8_byte_start'],
                            utf8_byte_end_exclusive=row['caption_utf8_byte_end_exclusive'],
                            transcription_excerpt=row['caption_text']))
                        revised.update(caption_block_id=caption['block_id'],
                            caption_region_id=caption['region_id'], caption_scan=caption['scan'],
                            caption_utf8_byte_start=caption[START],
                            caption_utf8_byte_end_exclusive=caption[END],
                            source_caption_block_id=block['id'],
                            source_caption_region_id=row['caption_region_id'],
                            source_caption_scan=deepcopy(row['caption_scan']),
                            source_caption_range=caption['source_range'])
                if 'trim_region_end' in revised:
                    revised['trim_region_end'] = {context.identity(id, context.regions): value
                                                  for id, value in row['trim_region_end'].items()}
                corrections[field].append(revised)
        corrections['segment_continuations'].extend(dict(source_segment=context.name, original=deepcopy(row))
                                                    for row in original.get('segment_continuations', []))

        if wrapped:
            from .assembly_wrapped import project_listing
            project_listing(context, corrections, listing)
            continue

        code = {b['id']: b for b in context.source['blocks'] if b['kind'] == 'code'}
        groups = original.get('listing_groups', [])
        if (len(groups) != len(code) or {r.get('id') for r in groups} != set(code) or
                any(r.get('block_ids') != [r['id']] or r.get('standalone_example') is not True or
                    r.get('execute_verified') is not False for r in groups)):
            raise ValueError('Every code block must be an independent unverified example')
        for row in groups:
            revised = references(row)
            revised.update(id=context.identity(row['id'], context.blocks), source_id=row['id'])
            corrections['listing_groups'].append(revised)
        local_code, cursor = {}, 0
        for item in context.source['content_order']:
            if item['type'] == 'block' and item['id'] in code:
                end = cursor + len(code[item['id']]['text'].encode())
                local_code[item['id']] = (cursor, end)
                cursor = end

        def listing_range(row):
            value = span(row, context.listing)
            if row.get('download') != 'listing.txt' or row.get('block_id') not in code:
                raise ValueError('Unknown standalone listing block')
            start, end = local_code[row['block_id']]
            if not start <= row[START] < row[END] <= end:
                raise ValueError('Listing range crosses independent examples')
            revised = references(row)
            revised.update(source_range={START: row[START], END: row[END]},
                           **{START: context.offset + row[START], END: context.offset + row[END]})
            if span(revised, listing) != value:
                raise ValueError('Projected listing differs from source')
            return revised

        rows = original.get('listing_index', [])
        if len(rows) != len(code) or {r['block_id'] for r in rows} != set(code):
            raise ValueError('Listing index must cover each standalone example')
        for row in rows:
            if (row[START], row[END]) != local_code[row['block_id']]:
                raise ValueError('Listing index differs from complete example')
            corrections['listing_index'].append(listing_range(row))
        expected_rows = []
        for id, (start, _) in local_code.items():
            for ordinal, line in enumerate(code[id]['text'].splitlines(keepends=True), 1):
                end = start + len(line.encode())
                expected_rows.append((id, ordinal, start, end, line))
                start = end
        rows = original.get('listing_line_index', [])
        if len(rows) != len(expected_rows):
            raise ValueError('Physical listing rows do not cover standalone examples')
        for row, (id, ordinal, start, end, line) in zip(rows, expected_rows, strict=True):
            if (row.get('listing_id') != id or row.get('block_id') != id or
                    row.get('physical_line') != ordinal or (row[START], row[END]) != (start, end) or
                    any(k in row for k in ('prior_segment', 'continuation', 'segments')) or not line.endswith('\n')):
                raise ValueError('Standalone row differs from physical source line')
            if row.get('row_kind') == 'immediate-command':
                if row.get('printed_line') is not None or row.get('printed_line_visible') is not False:
                    raise ValueError('Immediate command cannot have an inferred line number')
            elif (row.get('row_kind') != 'numbered' or row.get('printed_line_visible') is not True or
                  type(row.get('printed_line')) is not int or not line.startswith(str(row['printed_line']) + ' ')):
                raise ValueError('Printed line number differs from standalone example')
            revised = listing_range(row)
            revised.update(source_line_id=row.get('line_id'), listing_id=context.identity(id, context.blocks),
                           line_id=f'{context.name}:{id}:physical:{ordinal}')
            corrections['listing_line_index'].append(revised)
        for row in original.get('listing_anomalies', []):
            corrections['listing_anomalies'].append(listing_range(row))
    # One index per combined block, plus the individually traceable original ranges.
    assets = {r['region_id']: r['asset'] for r in package['region_assets']}
    for block in package['blocks']:
        start, end = ranges[block['id']]
        corrections['text_index'].append(dict(block_id=block['id'], region_ids=block['region_ids'],
            download='article.txt', **{START: start, END: end}, scans=[assets[id] for id in block['region_ids']]))
    for record in corrections['records']:
        if 'block_ids' in record:
            record['block_ids'] = [positions[id][0] for id in record['block_ids']]
    corrections['blocks'] = package['blocks']
    validate_package(package)
    return package, corrections
