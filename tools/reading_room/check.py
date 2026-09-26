"""Validate a generated static reading-room data tree without private sources."""
import argparse
from collections import Counter
import json
from pathlib import Path

from .export import digest, read, safe, text_for


def check(root):
    root = Path(root)
    manifest = read(root / 'manifest.json')
    if manifest.get('kind') != 'reading-room-static' or manifest.get('schemaVersion') not in (1, 2):
        raise ValueError('Unsupported reading-room manifest')
    expected = {row['path'] for row in manifest['files']} | {'manifest.json'}
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if actual != expected:
        raise ValueError(f'File inventory differs: missing={len(expected - actual)}, extra={len(actual - expected)}')
    for row in manifest['files']:
        path = safe(root, row['path'])
        if path.stat().st_size != row['bytes'] or digest(path) != row['sha256']:
            raise ValueError(f'File bytes differ: {row["path"]}')
    catalog = read(root / 'catalog.json')
    issues = {row['id']: row for row in catalog['issues']}
    articles = {row['article_id']: row for row in catalog['articles']}
    if len(issues) != len(catalog['issues']) or len(articles) != len(catalog['articles']) or len({a['reference'] for a in articles.values()}) != len(articles):
        raise ValueError('Duplicate reading-room identity')
    memberships = Counter()
    counts = Counter()
    for issue_id, summary in issues.items():
        date = issue_id.removeprefix('maso-')
        issue = read(root / f'issues/{date}.json')
        media = read(root / f'media/{date}.json')
        if issue['issue'] != summary or media['issueId'] != issue_id:
            raise ValueError(f'Issue identity differs: {issue_id}')
        if len(issue['toc']) != summary['tocCount'] or len(issue['articles']) != summary['articleCount']:
            raise ValueError(f'Issue count differs: {issue_id}')
        counts['tocEntries'] += len(issue['toc'])
        counts['mediaRecords'] += len(media['items'])
        for article in issue['articles']:
            if articles.get(article['article_id']) != article or article['issue_id'] != issue_id:
                raise ValueError(f'Broken issue article: {issue_id}')
            memberships[article['article_id']] += 1
        for item in issue['toc']:
            if any(id not in articles or articles[id]['issue_id'] != issue_id for id in item['articleIds']):
                raise ValueError(f'Broken TOC article link: {item["id"]}')
        for item in media['items']:
            directory = f'issues/{date}/media/{item["resource"]}'
            original = item.get('originalPath', f'{directory}/{item["resource"]}')
            if original:
                safe(root / 'source', original).stat()
            elif item['status'] != 'missing':
                raise ValueError(f'Unaccounted original: {item["resource"]}')
            if item['asset_name']:
                safe(root / 'source', item.get('previewPath', f'{directory}/{item["asset_name"]}')).stat()
            elif item['status'] not in ('deferred', 'missing'):
                raise ValueError(f'Unaccounted media state: {item["resource"]}')
    for article_id, summary in articles.items():
        if memberships[article_id] != 1:
            raise ValueError(f'Article membership differs: {article_id}')
        doc = read(root / f'articles/{summary["reference"]}.json')
        if doc['article'] != summary:
            raise ValueError(f'Article identity differs: {article_id}')
        if summary['text']:
            text = safe(root / 'source', summary['text'])
            if digest(text) != summary['text_sha256'] or text_for(doc['blocks']).encode() != text.read_bytes():
                raise ValueError(f'Text differs: {article_id}')
            counts['texts'] += 1
        for listing in doc['listings']:
            relative = str(Path(summary['path']).parent / listing['path'])
            if digest(safe(root / 'source', relative)) != listing['sha256']:
                raise ValueError(f'Listing differs: {relative}')
            counts['listings'] += 1
        for attachment in doc.get('attachments', []):
            if digest(safe(root / 'source', attachment['path'])) != attachment['sha256']:
                raise ValueError(f'Attachment differs: {attachment["path"]}')
        for link in doc.get('relatedSources', []):
            safe(root / 'source', link['path']).stat()
        media = read(root / f'media/{summary["issue_id"].removeprefix("maso-")}.json')['items']
        by_resource = {m['resource']: m for m in media}
        if doc['media'] != [by_resource[r] for r in summary['resources']]:
            raise ValueError(f'Article media differs: {article_id}')
        counts['articles'] += 1
    counts['issues'] = len(issues)
    search = read(root / 'search.json')['items']
    if Counter(s['id'] for s in search if s['kind'] == 'article') != Counter({id: 1 for id in articles}):
        raise ValueError('Search article coverage differs')
    for source in manifest.get('sources', [])[1:]:
        if digest(safe(root / 'source', f'{source["disc"]}/manifest.json')) != source['manifestSha256']:
            raise ValueError('Copied reference manifest differs')
        if sum(a.get('disc') == source['disc'] for a in articles.values()) != source['counts']['articles']:
            raise ValueError('Disc article count differs')
    for key, value in manifest['counts'].items():
        if counts[key] != value:
            raise ValueError(f'{key}: expected {value}, found {counts[key]}')
    return dict(counts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path('build/reading-room/data'))
    args = parser.parse_args()
    print(json.dumps(check(args.data)))


if __name__ == '__main__':
    main()
