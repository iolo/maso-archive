"""Project source-linked news items without merging independent stories."""
def project_news(context, result, project_range, positions):
    """Only segments declaring news metadata opt in; older exports stay identical."""
    original, source = context.correction, context.source
    if not {'news_item_index', 'section_header_region_ids'} & original.keys():
        return
    items = original.get('news_item_index')
    headers = original.get('section_header_region_ids')
    if headers is None and isinstance(items, list) and items and all(
            isinstance(row, dict) and 'news_item_id' in row for row in items):
        project_news_candidates(context, result, project_range, positions, items)
        return
    regions = {r['id']: r for r in source['regions']}
    blocks = {b['id']: b for b in source['blocks']}
    figures = {f['id']: f for f in source['figures']}

    def identities(values, allowed, nonempty=False):
        if (not isinstance(values, list) or nonempty and not values or
                any(not isinstance(v, str) or v not in allowed for v in values) or
                len(set(values)) != len(values)):
            raise ValueError('News identities must be unique mapped source identities')
        return set(values)

    seen = identities(headers, regions)
    if not isinstance(items, list) or not items:
        raise ValueError('News index requires source items and explicit header regions')
    # Joining a story or header into another segment loses the independent item
    # boundary. Supporting continued stories would need explicit item-level joins.
    if any(positions[context.identity(id, context.blocks)] !=
           (context.identity(id, context.blocks), 0) for id in blocks):
        raise ValueError('News items cannot use cross-segment prose joins')
    ids = set()
    projected = []
    pages = {p['pdf_page']: p['printed_page'] for p in source['pages']}
    text_indexes = {r['block_id']: r for r in original['text_index']}
    for ordinal, row in enumerate(items, 1):
        if not isinstance(row, dict):
            raise ValueError('News item must be a source record')
        id = row.get('id')
        if (not isinstance(id, str) or not id or id in ids or
                type(row.get('ordinal')) is not int or row['ordinal'] != ordinal or
                not isinstance(row.get('subsection'), str) or not row['subsection'].strip() or
                row.get('complete_printed_news_item') is not True or
                row.get('historically_verified') is not False):
            raise ValueError('News item requires ordered identity and unverified source claims')
        ids.add(id)
        owned = identities(row.get('region_ids'), regions, nonempty=True)
        block_ids = identities(row.get('block_ids'), blocks, nonempty=True)
        figure_ids = identities(row.get('figure_ids'), figures)
        heading = row.get('heading_block_id')
        if heading not in block_ids or blocks[heading]['kind'] != 'section-label':
            raise ValueError('News heading must identify its source section label')
        if seen & owned:
            raise ValueError('News regions overlap another item or section header')
        seen |= owned
        expected = {r for id in block_ids for r in blocks[id]['region_ids']}
        expected |= {r for id in figure_ids for r in figures[id]['region_ids']}
        if owned != expected:
            raise ValueError('News regions differ from their blocks and figures')
        for kind, key, allowed in [('block', 'block_ids', block_ids), ('figure', 'figure_ids', figure_ids)]:
            if row[key] != [r['id'] for r in source['content_order'] if r['type'] == kind and r['id'] in allowed]:
                raise ValueError('News content differs from source reading order')
        pdf_pages = sorted({regions[id]['pdf_index'] + 1 for id in owned})
        # Segment indexes use integer printed folios; source packages use strings.
        if (row.get('pdf_pages') != pdf_pages or
                not isinstance(row.get('printed_pages'), list) or
                list(map(str, row['printed_pages'])) != [pages[n] for n in pdf_pages]):
            raise ValueError('News pages differ from mapped source regions')
        ranges = row.get('ranges')
        if not isinstance(ranges, list) or ranges != [text_indexes[id] for id in row['block_ids']]:
            raise ValueError('News ranges must match complete source text indexes')
        for r in ranges:
            if (r.get('region_ids') != blocks[r['block_id']]['region_ids'] or
                    r.get('scans') != [context.assets[id] for id in r['region_ids']]):
                raise ValueError('News text range has unrelated region or scan evidence')
        revised = context.references(row)
        revised.update(id=context.name+'-'+id, source_id=id, source_segment=context.name,
                       source_ordinal=ordinal, ordinal=len(result.get('news_item_index', []))+len(projected)+1,
                       heading_block_id=context.identity(heading, context.blocks),
                       figure_ids=[context.identity(id, context.figures) for id in row['figure_ids']],
                       ranges=[project_range(r, whole=True) for r in ranges])
        projected.append(revised)
    if seen != set(regions):
        raise ValueError('News items and section headers must cover every included region')
    result.setdefault('news_item_index', []).extend(projected)
    result.setdefault('section_header_region_ids', []).extend(context.identity(id, regions) for id in headers)


def project_news_candidates(context, result, project_range, positions, items):
    """Preserve regional candidate indexes without inventing full item ownership."""
    originals = context.correction['regional_text_index']
    regions = {r['id']: r for r in context.source['regions']}
    projected = []
    ids, numbers, owned = set(), set(), set()
    previous = 0
    for row in items:
        id, number = row.get('news_item_id'), row.get('number')
        if (not isinstance(id, str) or not id.strip() or id in ids or
                type(number) is not int or number <= previous or number in numbers or
                row.get('section') not in ('domestic', 'foreign') or
                row.get('source_claims_verified') is not False):
            raise ValueError('News candidate requires ordered identity and unverified claims')
        ids.add(id); numbers.add(number); previous = number
        headline, spans, body = row.get('headline'), row.get('source_spans'), row.get('source_regions')
        if (not isinstance(headline, dict) or not isinstance(spans, list) or not spans or
                not isinstance(body, list) or body != [r.get('region_id') for r in spans] or
                any(not isinstance(r, str) or r not in regions for r in body) or
                len(set(body)) != len(body)):
            raise ValueError('News candidate requires ordered mapped regional spans')
        all_spans = [headline] + spans
        local = {r.get('region_id') for r in all_spans}
        if len(local) != len(all_spans) or owned & local:
            raise ValueError('News candidate regions overlap another source item')
        owned |= local
        revised_spans = []
        for span in all_spans:
            if not any(all(span.get(k) == parent.get(k) for k in
                    ('block_id', 'region_id', 'scan', 'download', 'utf8_byte_start',
                     'utf8_byte_end_exclusive')) for parent in originals):
                raise ValueError('News candidate differs from its complete regional source range')
            block = span['block_id']
            if positions[context.identity(block, context.blocks)] != (context.identity(block, context.blocks), 0):
                raise ValueError('News candidates cannot use cross-segment prose joins')
            revised_spans.append(project_range(span))
        revised = dict(row, news_item_id=context.name+'-'+id, source_news_item_id=id,
                       source_segment=context.name, headline=revised_spans[0],
                       source_regions=[context.identity(id, regions) for id in body],
                       source_spans=revised_spans[1:])
        projected.append(revised)
    prior = result.get('news_item_index', [])
    if any(r.get('number') in numbers for r in prior):
        raise ValueError('News candidate numbers overlap a previous segment')
    result.setdefault('news_item_index', []).extend(projected)
