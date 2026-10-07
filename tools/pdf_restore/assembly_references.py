"""Opt-in projection of source tables, program guides, variables and prompts."""
from copy import deepcopy

from .assembly_indexes import START, END, span


def project_references(context, result, project_range):
    original = context.correction
    parents = {r['region_id']: r for r in original['regional_text_index']}

    def linked(row, empty=False):
        parent = parents.get(row.get('region_id'))
        if (parent is None or row.get('block_id') != parent['block_id'] or
                row.get('scan') != parent['scan'] or row.get('download') != 'article.txt' or
                type(row.get(START)) is not int or type(row.get(END)) is not int or
                not parent[START] <= row[START] <= row[END] <= parent[END]):
            raise ValueError('Reference span differs from its source region')
        if row[START] != row[END]:
            return project_range(row)
        if not empty or row.get('transcription_excerpt') != '':
            raise ValueError('Only an explicit blank table cell may have an empty span')
        projected = project_range(dict(parent,
            transcription_excerpt=original['regional_transcription'][row['region_id']]))
        revised = context.references(row)
        delta = projected[START] - parent[START]
        revised.update(block_id=projected['block_id'],
                       source_segment=context.name, source_block_id=row['block_id'],
                       source_range={START: row[START], END: row[END]},
                       **{START: row[START]+delta, END: row[END]+delta})
        return revised

    tables = {}
    for row in original.get('table_index', []):
        table = row.get('table_id')
        if not isinstance(table, str) or not table or type(row.get('row')) is not int:
            raise ValueError('Table requires an ordered source identity')
        rows = tables.setdefault(table, [])
        if row['row'] != len(rows) or row.get('row_kind') not in ('header', 'data'):
            raise ValueError('Table rows must retain consecutive source order')
        if row['row_kind'] == 'header' and rows:
            raise ValueError('A source table header must be its first row')
        cells = row.get('cells')
        if not isinstance(cells, list) or not cells or rows and len(cells) != len(rows[0]['cells']):
            raise ValueError('Table columns must retain their source count')
        text = span(row, context.article)
        if text != '\t'.join(c.get('transcription_excerpt', '') for c in cells)+'\n':
            raise ValueError('Table cells differ from the literal tab-separated source row')
        cursor = row[START]
        for column, cell in enumerate(cells, 1):
            value = cell.get('transcription_excerpt')
            if (not isinstance(value, str) or cell.get('column') != column or
                    cell.get(START) != cursor or cell.get(END) != cursor+len(value.encode()) or
                    any(cell.get(k) != row.get(k) for k in ('block_id', 'region_id', 'scan', 'download'))):
                raise ValueError('Table cell range or source identity differs')
            linked(cell, empty=True)
            cursor = cell[END]+1
        if cursor != row[END] or rows and (row['region_id'] != rows[-1]['region_id'] or row[START] != rows[-1][END]):
            raise ValueError('Table rows must be adjacent in their source region')
        revised = linked(row)
        revised.update(table_id=context.name+'-'+table, source_table_id=table,
                       cells=[linked(cell, empty=True) for cell in cells])
        result.setdefault('table_index', []).append(revised)
        rows.append(row)
    for rows in tables.values():
        parent = parents[rows[0]['region_id']]
        if (rows[0][START], rows[-1][END]) != (parent[START], parent[END]):
            raise ValueError('A searchable table must cover its complete source region')

    for field in ('program_guide_index', 'variable_definition_index'):
        counts = {}
        for row in original.get(field, []):
            rid = row.get('region_id');counts[rid] = counts.get(rid, 0)+1
            if (row.get('source_row') != counts[rid] or
                    row.get('source_encoding_verified') is not False or
                    row.get('execute_verified') is not False):
                raise ValueError('Guide rows require source order and unverified bytes/execution')
            result.setdefault(field, []).append(linked(row))


def project_prompts(context, result):
    for row in context.correction.get('prompt_index', []):
        source = next((r for r in context.correction['listing_line_index']
                       if r['line_id'] == row.get('line_id')), None)
        if (source is None or source.get('row_kind') != 'unnumbered' or
                row.get('execute_verified') is not False or
                any(row.get(k) != source.get(k) for k in source) or
                row.get('transcription_excerpt') != span(source, context.listing)):
            raise ValueError('Prompt requires an exact unnumbered source row')
        target = next(r for r in result['listing_line_index']
                      if r['source_segment'] == context.name and r['source_line_id'] == source['line_id'])
        result.setdefault('prompt_index', []).append(dict(deepcopy(target),
            transcription_excerpt=row['transcription_excerpt'], execute_verified=False))
