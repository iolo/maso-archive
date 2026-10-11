"""Explicit, source-checked assembly of disjoint segments sharing a PDF page."""
from collections import Counter


def validate_options(recipe):
    if not ({'shared_pdf_pages', 'resolved_exclusions'} & recipe.keys()):
        return
    pages = recipe.get('shared_pdf_pages')
    rows = recipe.get('resolved_exclusions')
    if (not isinstance(pages, list) or not pages or
        any(type(p) is not int or p not in recipe['expected_pdf_pages'] for p in pages) or
        len(set(pages)) != len(pages) or not isinstance(rows, list)):
        raise ValueError('Shared-page assembly requires explicit pages and resolved exclusions')
    names = {s['name'] for s in recipe['segments']}
    seen = set()
    for row in rows:
        if (not isinstance(row, dict) or set(row) != {'segment', 'region_id', 'restored_by', 'reason'} or
            any(not isinstance(v, str) or not v.strip() for v in row.values()) or
            row['segment'] not in names or row['restored_by'] not in names or
            row['segment'] == row['restored_by']):
            raise ValueError('Resolved exclusion requires source and restoring segments and a reason')
        key = row['segment'], row['region_id']
        if key in seen:
            raise ValueError('Duplicate resolved exclusion')
        seen.add(key)


def overlaps(a, b):
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])


def validate_shared_pages(recipe, segments):
    """Validate original segment coordinates before any identity namespacing."""
    if 'shared_pdf_pages' not in recipe:
        return
    sources = {spec['name']: source for spec, (source, _) in zip(recipe['segments'], segments, strict=True)}
    sequence = [p['pdf_page'] for source in sources.values() for p in source['pages']]
    counts = Counter(sequence)
    if {p for p, count in counts.items() if count > 1} != set(recipe['shared_pdf_pages']):
        raise ValueError('Declared shared pages differ from actual segment coverage')
    collapsed = [p for i, p in enumerate(sequence) if not i or sequence[i-1] != p]
    if collapsed != recipe['expected_pdf_pages']:
        raise ValueError('Shared segments differ from expected ordered page coverage')
    resolved = {(r['segment'], r['region_id']): r for r in recipe['resolved_exclusions']}
    for (name, id), resolution in resolved.items():
        excluded = next((r for r in sources[name]['excluded_regions'] if r['id'] == id), None)
        if excluded is None or excluded['pdf_index'] + 1 not in recipe['shared_pdf_pages']:
            raise ValueError('Resolved exclusion is not on a declared shared page')
        included = [r for r in sources[resolution['restored_by']]['regions']
                    if r['pdf_index'] == excluded['pdf_index']]
        box = excluded['bbox']
        if not included or any(not (box[0] <= r['bbox'][0] < r['bbox'][2] <= box[2] and
                                   box[1] <= r['bbox'][1] < r['bbox'][3] <= box[3]) for r in included):
            raise ValueError('Restoring regions must lie inside the resolved exclusion')
    for pg in recipe['shared_pdf_pages']:
        pages = [p for source in sources.values() for p in source['pages'] if p['pdf_page'] == pg]
        if any(p != pages[0] for p in pages[1:]):
            raise ValueError('Shared-page geometry or orientation differs')
        regions = [(name, r) for name, source in sources.items() for r in source['regions'] if r['pdf_index'] == pg-1]
        for i, (name, r) in enumerate(regions):
            if any(name != other and overlaps(r['bbox'], s['bbox']) for other, s in regions[i+1:]):
                raise ValueError('Included regions overlap across shared-page segments')
        for name, source in sources.items():
            for excluded in source['excluded_regions']:
                if excluded['pdf_index'] != pg-1 or (name, excluded['id']) in resolved:
                    continue
                if any(overlaps(excluded['bbox'], r['bbox']) for _, r in regions):
                    raise ValueError('Included shared-page region overlaps an unresolved exclusion')


def exclusion_is_resolved(recipe, segment, id):
    # All nonlegacy index modes namespace identities before legacy projection.
    prefix = segment + '-' if recipe.get('index_mode') else ''
    return any(r['segment'] == segment and prefix + r['region_id'] == id
               for r in recipe.get('resolved_exclusions', []))
