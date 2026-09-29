"""Opt-in projection of regional, prose and physical listing indexes for assemblies.

Original corrections stay in their segment directories. Projected ranges address
combined downloads; source ranges and segment-local identities remain explicit.
"""
from collections import Counter
from copy import deepcopy

from .assemble import project_legacy, rebase, text_bytes

START, END = 'utf8_byte_start', 'utf8_byte_end_exclusive'


def block_ranges(package):
    blocks = {b['id']: b for b in package['blocks']}
    result, offset = {}, 0
    for item in package['content_order']:
        if item['type'] == 'figure':
            value = f'[그림 {item["id"]}: 스캔 이미지 참조]'
        else:
            value = blocks[item['id']]['text']
            result[item['id']] = (offset, offset + len(value.encode()))
        offset += len(value.encode()) + 2
    return result


def span(row, data):
    start, end = row[START], row[END]
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(data):
        raise ValueError('Correction byte range outside download')
    try:
        return data[start:end].decode('utf-8')
    except UnicodeDecodeError as error:
        raise ValueError('Correction range splits UTF-8 character') from error


class Segment:
    def __init__(self, spec, source, correction, offset):
        self.spec, self.source, self.correction = spec, source, correction
        self.name, self.prefix = spec['name'], 'segments/' + spec['name']
        self.offset = offset
        self.article, self.listing = text_bytes(source)
        self.ranges = block_ranges(source)
        self.regions = {r['id'] for r in source['regions'] + source['excluded_regions']}
        self.blocks = {b['id'] for b in source['blocks']}
        self.figures = {f['id'] for f in source['figures']}
        self.assets = {r['region_id']: r['asset'] for r in source['region_assets']}

    def identity(self, value, allowed):
        if value not in allowed:
            raise ValueError('Unknown correction identity: ' + str(value))
        return self.name + '-' + value

    def references(self, row):
        """Known local references only; never reinterpret original nested evidence."""
        result = deepcopy(row)
        for key, allowed in [('region_id', self.regions), ('block_id', self.blocks),
                             ('caption_block_id', self.blocks), ('figure_id', self.figures)]:
            if result.get(key) is not None:
                result[key] = self.identity(result[key], allowed)
        for key, allowed in [('region_ids', self.regions), ('regions', self.regions),
                             ('related_regions', self.regions), ('block_ids', self.blocks)]:
            if key in result:
                result[key] = [self.identity(v, allowed) for v in result[key]]
        for key in ('scan', 'scans'):
            if key not in result:
                continue
            pins = [result[key]] if key == 'scan' else result[key]
            allowed = [self.assets[r] for r in row.get('region_ids', [row.get('region_id')]) if r in self.assets]
            if not allowed:
                allowed = list(self.assets.values())
            if any(p not in allowed for p in pins):
                raise ValueError('Correction scan differs from mapped region')
            values = [rebase(p, self.prefix) for p in pins]
            result[key] = values[0] if key == 'scan' else values
        return result

    def listing_range(self, row):
        span(row, self.listing)
        result = self.references(row)
        result.update(source_segment=self.name, source_range={START: row[START], END: row[END]},
                      download='listing.txt', **{START: self.offset + row[START], END: self.offset + row[END]})
        return result

    def local_line(self, row, number):
        result = self.listing_range(row)
        result['source_line_id'] = row.get('line_id')
        result['line_id'] = f'{self.name}:row:{number}'
        result['segments'] = [self.listing_range(part) for part in row['segments']]
        cursor = row[START]
        for part in row['segments']:
            if part[START] != cursor:
                raise ValueError('Line source segments do not partition its byte range')
            cursor = part[END]
        if cursor != row[END] or not row['segments']:
            raise ValueError('Line source segments do not cover its byte range')
        # Historical links keep their original local coordinate system and paths.
        for key in ('prior_segment', 'continuation'):
            if key in result:
                result['original_' + key] = result.pop(key)
        return result


def namespace(segment):
    source, correction = deepcopy(segment.source), deepcopy(segment.correction)
    for key, allowed in [('regions', segment.regions), ('excluded_regions', segment.regions),
                         ('blocks', segment.blocks), ('figures', segment.figures)]:
        source[key] = [segment.references(row) for row in source[key]]
        for row in source[key]:
            original_id = row['id']
            row['id'] = segment.identity(original_id, allowed)
            if 'correction_evidence' in row:
                row['correction_evidence'] = [
                    'corrections.json#' + segment.identity(v.split('#', 1)[1], segment.regions)
                    if v.startswith('corrections.json#') else v for v in row['correction_evidence']]
    source['content_order'] = [dict(type=r['type'], id=segment.identity(
        r['id'], segment.blocks if r['type'] == 'block' else segment.figures)) for r in source['content_order']]
    for key in ('raw_ocr', 'region_assets'):
        source[key] = [segment.references(row) for row in source[key]]
    source['verification']['reviewed_region_ids'] = [segment.identity(v, segment.regions)
                                                     for v in source['verification']['reviewed_region_ids']]
    # Legacy projection rebases asset and raw paths itself.
    correction['records'] = []
    for row in segment.correction['records']:
        revised = segment.references({k: v for k, v in row.items() if k != 'scan'})
        revised.update(id=segment.identity(row['id'], segment.regions), source_id=row['id'], scan=row['scan'])
        correction['records'].append(revised)
    for key in ('listing_index', 'glyph_definitions', 'unresolved_graphics'):
        correction[key] = [segment.references({k: v for k, v in row.items() if k != 'scan'}) |
                           ({'scan': row['scan']} if 'scan' in row else {}) for row in correction.get(key, [])]
    return source, correction


def verify_prior(current, prior, row, previous_row):
    if previous_row.get('row_kind') == 'unnumbered':
        raise ValueError('Carried line requires a preceding numbered row')
    reference = row.get('prior_segment')
    if not isinstance(reference, dict) or reference.get('segment_id') != prior.name:
        raise ValueError('Carried line requires the immediately prior segment')
    expected = dict(manifest=prior.spec['manifest'],
                    listing=next(p for p in prior.source['downloads'] if p['path'] == 'listing.txt'),
                    corrections=prior.source['corrections'][0])
    for key, value in expected.items():
        if any(reference[key][field] != value[field] for field in ('sha256', 'bytes')):
            raise ValueError('Carried line prior evidence pin differs')
    if (reference[START] != previous_row[START] or reference[END] != previous_row[END] or
        reference['source_segments'] != previous_row['segments'] or reference[END] != len(prior.listing) or
        row[START] != 0 or row['listing_id'] != previous_row['listing_id'] or
        row['printed_line'] != previous_row['printed_line']):
        raise ValueError('Carried line differs from prior indexed bytes')
    return {key: rebase(value, prior.prefix) if key != 'manifest' else
            {**value, 'path': prior.prefix + '/manifest.json'} for key, value in expected.items()}


def project_indexes(recipe, originals):
    contexts, offset = [], 0
    for spec, (source, correction) in zip(recipe['segments'], originals, strict=True):
        context = Segment(spec, source, correction, offset)
        contexts.append(context)
        offset += len(context.listing)
    package, corrections = project_legacy(recipe, [namespace(c) for c in contexts])
    scoped_notes = list(recipe['uncertainties'])
    for context in contexts:
        source = context.source
        resolved = {r['note'] for r in recipe['resolved_notes'] if r['segment'] == context.name}
        notes = source['gaps'] + source['verification']['uncertainties'] + source['mapping']['uncertainties']
        notes += [n for b in source['blocks'] for n in b['uncertainties']]
        scoped_notes.extend(f'[{context.name}] {n}' for n in dict.fromkeys(notes) if n not in resolved)
    package['gaps'] = scoped_notes
    package['verification']['uncertainties'] = scoped_notes
    corrections['normalizations'] = scoped_notes
    combined_ranges = block_ranges(package)
    fields = ('text_index', 'text_review_items', 'figure_sequence', 'prose_joins', 'image_overlap_notes',
              'listing_line_index', 'listing_anomalies', 'listing_groups', 'segment_continuations',
              'logical_listing_line_index', 'resolved_continuations')
    corrections.update({key: [] for key in fields})
    corrections.update(index_mode='namespaced-v1', regional_transcription={})
    corrections['identity_map'] = [dict(source_segment=c.name, kind=kind, source_id=id,
        id=c.identity(id, allowed)) for c in contexts for kind, allowed in
        [('region', c.regions), ('block', c.blocks), ('figure', c.figures)] for id in sorted(allowed)]
    occurrences, local_rows = Counter(), {}
    for index, context in enumerate(contexts):
        original = context.correction
        for key in ('text_index', 'text_review_items'):
            rows = original.get(key, [])
            if key == 'text_index' and (len(rows) != len(context.blocks) or
                                       {r['block_id'] for r in rows} != context.blocks):
                raise ValueError('Text index must cover every block exactly once')
            for row in rows:
                value = span(row, context.article)
                start, end = context.ranges[row['block_id']]
                if (not start <= row[START] < row[END] <= end or
                    (key == 'text_index' and (start, end) != (row[START], row[END])) or
                    (key == 'text_review_items' and value != row['transcription_excerpt'])):
                    raise ValueError('Text correction range differs from reviewed block')
                revised = context.references(row)
                delta = combined_ranges[revised['block_id']][0] - start
                revised.update(source_segment=context.name, source_range={START: row[START], END: row[END]},
                               **{START: row[START] + delta, END: row[END] + delta})
                corrections[key].append(revised)
        for id, value in original.get('regional_transcription', {}).items():
            corrections['regional_transcription'][context.identity(id, context.regions)] = deepcopy(value)
        for key in ('figure_sequence', 'prose_joins', 'image_overlap_notes', 'listing_groups'):
            corrections[key].extend(context.references(row) | {'source_segment': context.name}
                                    for row in original.get(key, []))
        # Original declarations, numbering reviews and any future metadata remain
        # inspectable without accidentally presenting local offsets as global ones.
        corrections['segment_continuations'].extend(
            dict(source_segment=context.name, original=deepcopy(row)) for row in original.get('segment_continuations', []))
        corrections['segments'][index]['original_corrections'] = rebase(context.source['corrections'][0], context.prefix)
        corrections['segments'][index]['original_metadata'] = deepcopy({k: v for k, v in original.items()
            if k not in ('records', 'blocks', 'map', 'regional_transcription') and k not in fields and
            k not in ('listing_index', 'unresolved_graphics', 'glyph_definitions')})
        cursor = 0
        source_lines = original.get('listing_line_index', [])
        for number, row in enumerate(source_lines, 1):
            if row[START] != cursor:
                raise ValueError('Listing line index has a gap or overlap')
            cursor = row[END]
            local = context.local_line(row, number)
            key = (row['listing_id'], row['printed_line'])
            if row.get('row_kind') == 'unnumbered':
                if (row['printed_line'] is not None or row.get('printed_line_visible') is not False or
                    type(row.get('physical_line')) is not int or row['physical_line'] < 1 or
                    'prior_segment' in row or 'continuation' in row):
                    raise ValueError('Unnumbered row must have an explicit physical identity and no carried evidence')
                occurrences[key] += 1
                logical = dict(listing_id=key[0], printed_line=None, printed_line_visible=False,
                               row_kind='unnumbered', occurrence=occurrences[key],
                               line_id=f'{key[0]}:unnumbered:{occurrences[key]}', download='listing.txt',
                               **{START: local[START], END: local[END]}, source_parts=[], segments=[])
                corrections['logical_listing_line_index'].append(logical)
            elif row.get('printed_line_visible', True):
                value = span(row, context.listing).lstrip()
                if not value.startswith(str(row['printed_line']) + ' '):
                    raise ValueError('Printed line differs from indexed bytes')
                occurrences[key] += 1
                logical = dict(listing_id=key[0], printed_line=key[1], occurrence=occurrences[key],
                               line_id=f'{key[0]}:{key[1]}:{occurrences[key]}', download='listing.txt',
                               **{START: local[START], END: local[END]}, source_parts=[], segments=[])
                corrections['logical_listing_line_index'].append(logical)
            else:
                if index == 0 or number != 1 or not corrections['logical_listing_line_index']:
                    raise ValueError('Carried line has no preceding numbered row')
                prior = contexts[index - 1]
                prior_row = prior.correction['listing_line_index'][-1]
                evidence = verify_prior(context, prior, row, prior_row)
                logical = corrections['logical_listing_line_index'][-1]
                if logical[END] != local[START] or (logical['listing_id'], logical['printed_line']) != key:
                    raise ValueError('Carried line is not adjacent to its numbered row')
                logical[END] = local[END]
                corrections['resolved_continuations'].append(dict(kind='code', line_id=logical['line_id'],
                    prior_segment=prior.name, source_segment=context.name, evidence=evidence,
                    status='assembled-physical-fragments', text_normalized=False))
            logical['source_parts'].append(local['line_id'])
            logical['segments'].extend(deepcopy(local['segments']))
            local['logical_line_id'] = logical['line_id']
            corrections['listing_line_index'].append(local)
            local_rows[(context.name, row[START], row[END])] = (row, local)
        if cursor != len(context.listing):
            raise ValueError('Listing line index does not cover download')
        for row in original.get('listing_anomalies', []):
            pair = local_rows.get((context.name, row[START], row[END]))
            if pair is None or any(row.get(k) != v for k, v in pair[0].items()):
                raise ValueError('Listing anomaly differs from source line index')
            corrections['listing_anomalies'].append(deepcopy(pair[1]) |
                                                    {k: deepcopy(v) for k, v in row.items() if k not in pair[0]})
        for row in original.get('segment_continuations', []):
            if row['kind'] != 'prose':
                continue
            if index == 0 or row['prior_segment'] != contexts[index - 1].name:
                raise ValueError('Prose continuation has no prior segment')
            prior = contexts[index - 1]
            left = [b for b in prior.source['blocks'] if row['prior_region'] in b['region_ids']]
            right = [b for b in context.source['blocks'] if row['region_id'] in b['region_ids']]
            if (len(left) != 1 or len(right) != 1 or not left[0]['text'].endswith(row['prior_text_end']) or
                not right[0]['text'].startswith(row['text_start'])):
                raise ValueError('Prose continuation differs from reviewed text')
            corrections['resolved_continuations'].append(dict(kind='prose', status='linked-reading-blocks',
                prior_block_id=prior.identity(left[0]['id'], prior.blocks),
                block_id=context.identity(right[0]['id'], context.blocks), join_separator=row['join_separator'],
                text_normalized=False))
    return package, corrections
