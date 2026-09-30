"""Project the completed CD1 reference into static reading-room documents.

Run with --demo for a small, tracked synthetic fixture when private inputs are absent.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / 'build/cd1-reference'
TOC = ROOT / 'build/toc'
OUTPUT = ROOT / 'build/reading-room/data'
VERSION = 1


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(root, name, value):
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    return target


def safe(root, relative):
    path = Path(relative)
    if path.is_absolute() or any(part in ('.', '..') for part in path.parts) or '\\' in relative:
        raise ValueError(f'Unsafe path: {relative}')
    target = root / path
    if target.is_symlink() or not target.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Unsafe path: {relative}')
    return target


def copy(root, dest, relative):
    source = safe(root, relative)
    if not source.is_file():
        raise FileNotFoundError(source)
    target = safe(dest, relative)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or digest(target) != digest(source):
        shutil.copyfile(source, target)


def text_for(blocks):
    return ''.join(
        ''.join(r['text'] if r['type'] == 'text' else r.get('textMarker', f"[image:{r['resource']}]") for r in p['runs'])
        + ('\n' if p.get('terminated', True) else '')
        for b in blocks for p in b['paragraphs']
    )


def export(reference=REFERENCE, toc=TOC, output=OUTPUT, issue_filter=None, covers=None,
           cover_checkpoint=None, thumbnails=None, tocs=None, toc_images=None, toc_reviews=None):
    from .covers import DEFAULT_OUTPUT, separate, replace_directory
    output = Path(output)
    separate(output, reference, toc, covers, cover_checkpoint, thumbnails or DEFAULT_OUTPUT)
    separate(thumbnails or DEFAULT_OUTPUT, reference, toc, covers, cover_checkpoint, output)
    from .tocs import DEFAULT_OUTPUT as TOC_IMAGES, refresh
    separate(output, tocs, toc_images or TOC_IMAGES, toc_reviews)
    separate(toc_images or TOC_IMAGES, reference, toc, covers, cover_checkpoint, thumbnails or DEFAULT_OUTPUT, output, tocs, toc_reviews)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.cd1-reader-', dir=output.parent) as temp:
        staged = Path(temp) / 'data'
        result = _export(reference, toc, staged, issue_filter, covers, cover_checkpoint, thumbnails)
        if tocs is not None:
            refresh(staged, result, tocs, toc_images, toc_reviews)
        from .check import check
        check(staged, require_thumbnails=True)
        replace_directory(staged, output, Path(temp) / 'previous')
    return result


def _export(reference, toc, output, issue_filter, covers, cover_checkpoint, thumbnails):
    reference, toc, output = map(Path, (reference, toc, output))
    manifest = read(reference / 'manifest.json')
    if manifest.get('kind') != 'cd1-readable-reference' or manifest.get('schema_version') != 1:
        raise ValueError('Unsupported or missing CD1 reference manifest')
    for name, key in [('issues.json', 'issues_sha256'), ('toc-entries.jsonl', 'toc_sha256')]:
        if digest(toc / name) != manifest['inputs'][key]:
            raise ValueError(f'{name} differs from the pinned CD1 reference snapshot')
    issue_rows = read(toc / 'issues.json')
    toc_rows = [json.loads(line) for line in (toc / 'toc-entries.jsonl').read_text(encoding='utf-8').splitlines()]
    articles = read(reference / 'catalog.json')
    images = read(reference / 'images.json')
    if len(issue_rows) != manifest['counts']['issues'] or len(articles) != manifest['counts']['candidates']:
        raise ValueError('Catalog counts differ from the pinned CD1 reference')
    if issue_filter:
        issue_id = 'maso-' + issue_filter
        issue_rows = [row for row in issue_rows if row['id'] == issue_id]
        if not issue_rows:
            raise ValueError(f'Unknown issue: {issue_filter}')
        articles = [row for row in articles if row['issue_id'] == issue_id]
        toc_rows = [row for row in toc_rows if row['issue_id'] == issue_id]
        images = [row for row in images if row['issue'] == issue_filter]
    output.mkdir(parents=True, exist_ok=True)
    by_issue = defaultdict(list)
    toc_by_issue = defaultdict(list)
    for entry in toc_rows:
        toc_by_issue[entry['issue_id']].append(entry)
    media_by_issue = defaultdict(dict)
    for image in images:
        media_by_issue['maso-' + image['issue']][image['resource']] = image

    # Reviewed associations come from the existing prepared issue packages. The
    # current TOC snapshot provides display metadata for every issue.
    coverage = read(ROOT / 'data/catalog/batch-runs/cd1-oem-pass.json')
    reviewed = {}
    article_metadata = {}
    for record in coverage['issues']:
        if record['issue_id'] not in {row['id'] for row in issue_rows}:
            continue
        package = ROOT / coverage['output_root'] / record['package'] / 'content'
        prepared_issue = read(package / 'issues' / (record['issue_id'] + '.json'))
        for entry in prepared_issue['toc']:
            reviewed[entry['id']] = entry['article_ids']
        package_manifest = read(package / 'manifest.json')
        for entry in package_manifest['documents']:
            if entry['kind'] == 'article':
                doc = read(package / entry['path'])
                article_metadata[doc['id']] = {'byline': doc['byline'], 'page': doc['pages']['start']}
    for article in articles:
        article.update(article_metadata.get(article['article_id'], {'byline': None, 'page': None}))
        by_issue[article['issue_id']].append(article)
    article_ids = {row['article_id'] for row in articles}
    issues = []
    search = []
    files = []
    for row in issue_rows:
        issue_id, date = row['id'], row['id'].removeprefix('maso-')
        entries = []
        for entry in toc_by_issue[issue_id]:
            links = [id for id in reviewed.get(entry['id'], []) if id in article_ids]
            item = {'id': entry['id'], 'parentId': entry['parent_id'], 'depth': entry['depth'],
                    'title': entry['title_candidate'], 'byline': entry['byline_candidate'],
                    'page': entry['start_page_candidate'], 'kind': entry['kind_candidate'],
                    'articleIds': links}
            entries.append(item)
            search.append({'kind': 'toc', 'id': item['id'], 'issueId': issue_id,
                           'title': item['title'], 'byline': item['byline'],
                           'articleIds': links, 'status': 'linked' if links else 'unmatched'})
        issue_articles = by_issue[issue_id]
        summary = {'id': issue_id, 'year': row['year'], 'month': row['month'],
                   'label': row['original_label'], 'articleCount': len(issue_articles),
                   'textCount': sum(a['text'] is not None for a in issue_articles),
                   'tocCount': len(entries), 'cover': None}
        issues.append(summary)
        issue_doc = {'schemaVersion': VERSION, 'issue': summary, 'toc': entries,
                     'articles': issue_articles}
        files.append(write(output, f'issues/{date}.json', issue_doc))
        media = media_by_issue[issue_id]
        files.append(write(output, f'media/{date}.json', {'schemaVersion': VERSION,
             'issueId': issue_id, 'items': list(media.values())}))
        for image in media.values():
            directory = f'issues/{date}/media/{image["resource"]}'
            copy(reference, output / 'source', f'{directory}/{image["resource"]}')
            if image['asset_name']:
                copy(reference, output / 'source', f'{directory}/{image["asset_name"]}')
        for article in issue_articles:
            base = Path(article['path']).parent
            source = read(safe(reference, (base / 'reference.json').as_posix()))
            blocks = source['blocks']
            if article['text']:
                actual = safe(reference, article['text']).read_text(encoding='utf-8')
                if actual != text_for(blocks) or digest(safe(reference, article['text'])) != article['text_sha256']:
                    raise ValueError(f'Text mismatch: {article["article_id"]}')
                copy(reference, output / 'source', article['text'])
                copy(reference, output / 'source', (base / 'paragraphs.json').as_posix())
            for listing in source['listings']:
                relative = (base / listing['path']).as_posix()
                if digest(safe(reference, relative)) != listing['sha256']:
                    raise ValueError(f'Listing mismatch: {relative}')
                copy(reference, output / 'source', relative)
            copy(reference, output / 'source', (base / 'reference.json').as_posix())
            doc = {'schemaVersion': VERSION, 'article': article, 'blocks': blocks,
                   'listings': source['listings'], 'details': source['details'],
                   'media': [media[name] for name in article['resources']]}
            files.append(write(output, f'articles/{article["reference"]}.json', doc))
            search.append({'kind': 'article', 'id': article['article_id'],
                           'issueId': issue_id, 'title': article['title'], 'byline': article['byline'],
                           'reference': article['reference'], 'status': article['status']})
    catalog = {'schemaVersion': VERSION, 'issues': issues, 'articles': articles}
    from .covers import attach_covers
    cover_inputs = attach_covers(output, catalog, covers, cover_checkpoint, thumbnails)
    files.append(write(output, 'catalog.json', catalog))
    files.append(write(output, 'search.json', {'schemaVersion': VERSION, 'items': search}))
    # Inventory includes every generated document plus each copied source asset.
    inventory = [{'path': p.relative_to(output).as_posix(), 'bytes': p.stat().st_size,
                  'sha256': digest(p)} for p in sorted(output.rglob('*')) if p.is_file() and p.name != 'manifest.json']
    result = {'schemaVersion': VERSION, 'kind': 'reading-room-static',
              'sourceManifestSha256': digest(reference / 'manifest.json'),
              'tocSha256': manifest['inputs']['toc_sha256'], 'issuesSha256': manifest['inputs']['issues_sha256'],
              'counts': {'issues': len(issues), 'tocEntries': len(toc_rows),
                         'articles': len(articles), 'texts': sum(a['text'] is not None for a in articles),
                         'listings': sum(a['listings'] for a in articles), 'mediaRecords': len(images)},
              'files': inventory}
    from .covers import POLICY
    result['coverPolicy'] = POLICY
    result['coverInputs'] = cover_inputs
    result['counts']['covers'] = sum(i['cover'] is not None for i in issues)
    result['counts']['coverAssets'] = len(cover_inputs)
    write(output, 'manifest.json', result)
    return result


def demo(output=OUTPUT):
    """Make a small public-domain synthetic dataset for UI development."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    issue = {'id': 'maso-1988-02', 'year': 1988, 'month': 2, 'label': '88.02',
             'articleCount': 4, 'textCount': 3, 'tocCount': 5, 'cover': None}
    titles = [('demo-prepared', '예제: 컴퓨터와 글쓰기', 'prepared'),
              ('demo-normalized', '예제: 다시 읽은 글', 'normalized'),
              ('demo-gap', '예제: 판독 공백이 있는 글', 'reference_with_gaps'),
              ('demo-blocked', '예제: 글 경계 확인 중', 'blocked')]
    articles = []
    items = []
    demo_media = []
    for ref, title, status in titles:
        available = status != 'blocked'
        base = f'issues/1988-02/articles/{ref}'
        text = ('문자 <tag> & 기호를 그대로 보여 줍니다.' + ('[image:diagram.svg]' if ref == 'demo-prepared' else '') + '\n'
                + ('    PRINT "HELLO"\n\tEND\n' if available else ''))
        if status == 'reference_with_gaps': text += '확인 필요: ⟦bytes:81⟧[image:missing.wmf]\n'
        article = {'reference': ref, 'article_id': f'cd1:article:{ref}', 'issue_id': issue['id'],
                   'title': title, 'byline': None, 'page': None, 'status': status, 'path': base + '/index.html',
                   'text': base + '/article.txt' if available else None, 'paragraphs': 3 if available else 0,
                   'listings': 1 if available else 0, 'image_occurrences': 1 if ref in ('demo-prepared', 'demo-gap') else 0,
                   'resources': ['diagram.svg'] if ref == 'demo-prepared' else ['missing.wmf'] if ref == 'demo-gap' else [],
                   'text_sha256': hashlib.sha256(text.encode()).hexdigest() if available else None}
        articles.append(article)
        paragraphs = [
            {'id': ref + ':p1', 'runs': [{'type': 'text', 'text': '문자 <tag> & 기호를 그대로 보여 줍니다.', 'marks': ['bold']}], 'terminated': True},
            {'id': ref + ':p2', 'runs': [{'type': 'text', 'text': '    PRINT "HELLO"', 'marks': []}], 'terminated': True},
            {'id': ref + ':p3', 'runs': [{'type': 'text', 'text': '\tEND', 'marks': []}], 'terminated': True},
        ] if available else []
        if status == 'reference_with_gaps': paragraphs.append({'id': ref + ':p4', 'runs': [
            {'type': 'text', 'text': '확인 필요: ⟦bytes:81⟧', 'marks': []},
            {'type': 'media', 'resource': 'missing.wmf', 'marks': []}], 'terminated': True})
        if ref == 'demo-prepared': paragraphs[0]['runs'].append({'type': 'media', 'resource': 'diagram.svg', 'marks': []})
        blocks = ([{'id': ref + ':b1', 'type': 'paragraph', 'preformatted': False, 'paragraphs': [paragraphs[0]]},
                  {'id': ref + ':b2', 'type': 'code', 'preformatted': True, 'paragraphs': paragraphs[1:3]}] if available else [])
        if status == 'reference_with_gaps': blocks.append({'id': ref + ':b3', 'type': 'paragraph', 'preformatted': False, 'paragraphs': [paragraphs[3]]})
        media = ([{'issue': '1988-02', 'resource': 'diagram.svg', 'status': 'available',
                   'asset_name': 'diagram.svg', 'original_sha256': '', 'conversion_note': None}] if ref == 'demo-prepared' else
                 [{'issue': '1988-02', 'resource': 'missing.wmf', 'status': 'deferred',
                   'asset_name': None, 'original_sha256': '', 'conversion_note': 'Synthetic unavailable derivative'}] if ref == 'demo-gap' else [])
        demo_media.extend(media)
        listing_text = '    PRINT "HELLO"\n\tEND\n'
        write(output, f'articles/{ref}.json', {'schemaVersion': 1, 'article': article,
              'blocks': blocks, 'listings': [{'path': 'listings/001.txt', 'block_id': ref + ':b2',
              'sha256': hashlib.sha256(listing_text.encode()).hexdigest(), 'characters': len(listing_text)}] if available else [], 'details': '', 'media': media})
        if available:
            path = output / 'source' / base
            (path / 'listings').mkdir(parents=True, exist_ok=True)
            (path / 'article.txt').write_text(text, encoding='utf-8')
            (path / 'listings/001.txt').write_text(listing_text, encoding='utf-8')
            (path / 'paragraphs.json').write_text('[]\n', encoding='utf-8')
            (path / 'reference.json').write_text('{}\n', encoding='utf-8')
        items.append({'kind': 'article', 'id': article['article_id'], 'issueId': issue['id'],
                      'title': title, 'byline': None, 'reference': ref, 'status': status})
    toc = [{'id': f'maso-1988-02-toc-{i:04}', 'parentId': None, 'depth': 0,
            'title': title, 'byline': None, 'page': i, 'kind': 'article',
            'articleIds': [f'cd1:article:{ref}'] if i < 4 else []}
           for i, (ref, title, _) in enumerate(titles + [('missing', '예제: 차례만 있는 글', '')], 1)]
    for entry in toc:
        items.append({'kind': 'toc', 'id': entry['id'], 'issueId': issue['id'],
                      'title': entry['title'], 'byline': None, 'articleIds': entry['articleIds'],
                      'status': 'linked' if entry['articleIds'] else 'unmatched'})
    write(output, 'catalog.json', {'schemaVersion': 1, 'issues': [issue], 'articles': articles})
    write(output, 'issues/1988-02.json', {'schemaVersion': 1, 'issue': issue, 'toc': toc, 'articles': articles})
    write(output, 'media/1988-02.json', {'schemaVersion': 1, 'issueId': issue['id'], 'items': demo_media})
    write(output, 'search.json', {'schemaVersion': 1, 'items': items})
    media_dir = output / 'source/issues/1988-02/media/diagram.svg'
    media_dir.mkdir(parents=True, exist_ok=True)
    (media_dir / 'diagram.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="320" height="120"><rect width="320" height="120" fill="#eee"/><text x="20" y="65">Synthetic diagram</text></svg>\n', encoding='utf-8')
    deferred_dir = output / 'source/issues/1988-02/media/missing.wmf'
    deferred_dir.mkdir(parents=True, exist_ok=True)
    (deferred_dir / 'missing.wmf').write_bytes(b'Synthetic placeholder for an unavailable derivative\n')
    return {'issues': 1, 'articles': len(articles)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, default=REFERENCE)
    parser.add_argument('--toc', type=Path, default=TOC)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    parser.add_argument('--issue', help='Single YYYY-MM issue for a first slice')
    parser.add_argument('--demo', action='store_true', help='Generate synthetic demo without private sources')
    parser.add_argument('--covers', type=Path, default=ROOT / 'covers', help='Private donated YYMM.jpg directory')
    from .covers import DEFAULT_CHECKPOINT, DEFAULT_OUTPUT
    parser.add_argument('--pdf-cover-checkpoint', type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument('--cover-thumbnails', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--all-discs', action='store_true', help='Aggregate completed CD1, CD2 and CD3 references')
    from .tocs import DEFAULT_OUTPUT as TOC_IMAGES
    from tools.toc_restore.inventory import PRIVATE, SOURCES
    parser.add_argument('--tocs', type=Path, default=SOURCES)
    parser.add_argument('--toc-images', type=Path, default=TOC_IMAGES)
    parser.add_argument('--toc-reviews', type=Path, default=PRIVATE / 'reviews.json')
    parser.add_argument('--cd2-reference', type=Path, default=ROOT / 'build/cd2-reference')
    parser.add_argument('--cd3-reference', type=Path, default=ROOT / 'build/cd3-reference')
    args = parser.parse_args()
    if args.all_discs and (args.issue or args.demo):
        parser.error('--all-discs cannot be combined with --issue or --demo')
    if args.demo:
        target = ROOT / 'build/reading-room-demo/data' if args.output == OUTPUT else args.output
        result = demo(target)
        from .tocs import demo_images
        result.update(demo_images(target))
        print(json.dumps(result, ensure_ascii=False))
        return
    if (args.toc / 'manifest.json').exists():
        imported = read(args.toc / 'manifest.json')
        if imported.get('source', {}).get('sha256') != digest(ROOT / 'TOC.md'):
            import sys
            print('TOC.md differs from the prepared import. Preserving pinned catalog inputs; catalog migration requires separate follow-up.', file=sys.stderr)
    if args.all_discs:
        from .aggregate import aggregate
        result = aggregate(args.reference, args.toc, args.cd2_reference, args.cd3_reference, args.output, args.covers, args.pdf_cover_checkpoint, args.cover_thumbnails, args.tocs, args.toc_images, args.toc_reviews)
    else:
        result = export(args.reference, args.toc, args.output, args.issue, args.covers, args.pdf_cover_checkpoint, args.cover_thumbnails, args.tocs, args.toc_images, args.toc_reviews)
    print(json.dumps(result['counts'], ensure_ascii=False))


if __name__ == '__main__':
    main()
