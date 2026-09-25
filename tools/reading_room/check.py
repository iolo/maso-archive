"""Validate a generated static reading-room data tree without private sources."""
import argparse
from collections import Counter
import json
from pathlib import Path

from .export import digest, read, safe


def check(root):
    root = Path(root)
    manifest = read(root / 'manifest.json')
    if manifest.get('kind') != 'reading-room-static' or manifest.get('schemaVersion') != 1:
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
        for item in issue['toc']:
            if any(id not in articles or articles[id]['issue_id'] != issue_id for id in item['articleIds']):
                raise ValueError(f'Broken TOC article link: {item["id"]}')
        for item in media['items']:
            directory = f'issues/{date}/media/{item["resource"]}'
            safe(root / 'source', f'{directory}/{item["resource"]}').stat()
            if item['asset_name']:
                safe(root / 'source', f'{directory}/{item["asset_name"]}').stat()
            elif item['status'] != 'deferred':
                raise ValueError(f'Unaccounted media state: {item["resource"]}')
    for article_id, summary in articles.items():
        doc = read(root / f'articles/{summary["reference"]}.json')
        if doc['article'] != summary:
            raise ValueError(f'Article identity differs: {article_id}')
        if summary['text']:
            text = safe(root / 'source', summary['text'])
            if digest(text) != summary['text_sha256']:
                raise ValueError(f'Text differs: {article_id}')
            counts['texts'] += 1
        for listing in doc['listings']:
            relative = str(Path(summary['path']).parent / listing['path'])
            if digest(safe(root / 'source', relative)) != listing['sha256']:
                raise ValueError(f'Listing differs: {relative}')
            counts['listings'] += 1
        counts['articles'] += 1
    counts['issues'] = len(issues)
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
