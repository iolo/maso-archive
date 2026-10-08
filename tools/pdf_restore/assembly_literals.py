"""Opt-in indexes for literal marker excerpts and monitor token candidates.

Source records stay immutable. Projected indexes describe scan readings, never
verified character encodings, machine bytes or executable programs.
"""
from collections import Counter
from copy import deepcopy
import re

from .assembly_indexes import START, END, span

MARKER = re.compile(r'⟦G[^⟦⟧\r\n]+⟧')
HEX_ROW = re.compile(r'([0-9A-F]{4})- ((?:[0-9A-F]{2} ?)+)\n')


def unverified_hex(row):
    return (row.get('original_machine_bytes_verified') is False and
            row.get('execution_verified') is False and
            all(row.get(k) is None for k in ('original_bytes', 'encoded_bytes')) and
            all(k not in row or row[k] is False for k in
                ('machine_byte_verified', 'source_encoding_verified')))


def linked_region(context, row):
    parents = [r for r in context.correction.get('regional_text_index', [])
               if r.get('region_id') == row.get('region_id')]
    parent = parents[0] if len(parents) == 1 else None
    if (parent is None or row.get('block_id') != parent.get('block_id') or
            row.get('scan') != parent.get('scan') or
            row.get('scan') != context.assets.get(row.get('region_id')) or
            row.get('download') != 'article.txt' or
            type(row.get(START)) is not int or type(row.get(END)) is not int or
            not parent[START] <= row[START] < row[END] <= parent[END] or
            row.get('transcription_excerpt') != span(row, context.article)):
        raise ValueError('Literal excerpt differs from its source region')


def validate_markers(context):
    """Prove complete G-marker coverage before bypassing the legacy byte counter."""
    original = context.correction
    expected = Counter()
    for block in context.source['blocks']:
        start = context.ranges[block['id']][0]
        for match in MARKER.finditer(block['text']):
            a = start + len(block['text'][:match.start()].encode())
            expected[block['id'], a, a+len(match[0].encode()), match[0]] += 1
    actual = Counter()
    identity = ('block_id', 'region_id', 'scan', 'download', START, END,
                'transcription_excerpt', 'status', 'original_bytes', 'source_encoding_verified')
    for row in original.get('unresolved_graphics', []):
        marker = row.get('transcription_excerpt')
        if (not isinstance(marker, str) or not MARKER.fullmatch(marker) or
                any(k in row for k in ('marker', 'rendered_glyph')) or
                row.get('status') != 'manual-correction-required' or
                'original_bytes' not in row or row['original_bytes'] is not None or
                row.get('source_encoding_verified') is not False or
                row.get('encoded_bytes') is not None or
                any(k in row and row[k] is not False for k in
                    ('machine_byte_verified', 'execution_verified'))):
            raise ValueError('Literal marker requires explicit unverified excerpt evidence')
        linked_region(context, row)
        matches = [note for note in original.get('unresolved_text', [])
                   if all(k in note and note[k] == row[k] for k in identity)]
        if (len(matches) != 1 or matches[0].get('encoded_bytes') is not None or
                any(k in matches[0] and matches[0][k] is not False for k in
                    ('machine_byte_verified', 'execution_verified'))):
            raise ValueError('Literal marker requires one matching unresolved text record')
        actual[row['block_id'], row[START], row[END], marker] += 1
    if actual != expected:
        raise ValueError('Literal marker records must cover every source G-marker once')


def project_inline_examples(context, result, project_range):
    seen = set()
    for row in context.correction.get('inline_example_index', []):
        linked_region(context, row)
        identity = row['region_id'], row[START], row[END]
        if (identity in seen or row.get('execute_verified') is not False or
                row.get('original_bytes') is not None or row.get('encoded_bytes') is not None or
                any(k in row and row[k] is not False for k in
                    ('source_encoding_verified', 'machine_byte_verified', 'execution_verified'))):
            raise ValueError('Inline example requires distinct unverified source evidence')
        seen.add(identity)
        result.setdefault('inline_example_index', []).append(project_range(row))


def project_hex_indexes(context, result, listing):
    original = context.correction
    expected = []
    for row in original['listing_line_index']:
        if row['row_kind'] != 'unnumbered':
            continue
        text = span(row, context.listing)
        match = HEX_ROW.fullmatch(text)
        if match:
            expected.append((row, text, match))
    rows = original.get('hex_row_index', [])
    if not isinstance(rows, list) or len(rows) != len(expected):
        raise ValueError('Hex rows must cover all printed unnumbered address rows')
    targets = {r['source_line_id']: r for r in result['listing_line_index']
               if r['source_segment'] == context.name}
    expected_tokens = []
    for row, (physical, text, match) in zip(rows, expected, strict=True):
        values = list(re.finditer(r'[0-9A-F]{2}', match[2]))
        if (any(row.get(k) != v for k, v in physical.items()) or
                row.get('transcription_excerpt') != text or
                row.get('printed_address') != match[1] or
                row.get('literal_token_candidates') != [v[0] for v in values] or
                type(row.get('value_count')) is not int or row['value_count'] != len(values) or
                not unverified_hex(row)):
            raise ValueError('Hex row differs from its literal unverified physical row')
        target = targets[physical['line_id']]
        result.setdefault('hex_row_index', []).append(dict(deepcopy(target),
            transcription_excerpt=text, printed_address=match[1],
            literal_token_candidates=[v[0] for v in values], value_count=len(values),
            original_machine_bytes_verified=False, execution_verified=False))
        for value in values:
            a = physical[START] + len(text[:match.start(2)+value.start()].encode())
            expected_tokens.append(dict(block_id=physical['block_id'], region_id=physical['region_id'],
                scan=physical['scan'], download='listing.txt', **{START: a, END: a+2},
                transcription_excerpt=value[0], listing_id=physical['listing_id'],
                printed_address=match[1], physical_line_id=physical['line_id'],
                original_machine_bytes_verified=False, execution_verified=False))
    tokens = original.get('hex_token_index', [])
    if not isinstance(tokens, list) or len(tokens) != len(expected_tokens):
        raise ValueError('Hex tokens must cover all literal source byte candidates')
    for row, expected in zip(tokens, expected_tokens, strict=True):
        if any(row.get(k) != v for k, v in expected.items()) or not unverified_hex(row):
            raise ValueError('Hex token differs from its exact physical source candidate')
        target = targets[row['physical_line_id']]
        projected = context.listing_range(row)
        projected.update(source_physical_line_id=row['physical_line_id'],
                         physical_line_id=target['line_id'])
        if span(projected, listing) != row['transcription_excerpt']:
            raise ValueError('Projected hex token differs from literal source bytes')
        result.setdefault('hex_token_index', []).append(projected)
