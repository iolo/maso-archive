"""Validate a generated static reading-room data tree without private sources."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

from .export import digest, read, safe, text_for


def check(root, require_thumbnails=False):
    root = Path(root)
    manifest = read(root / 'manifest.json')
    if manifest.get('kind') != 'reading-room-static' or manifest.get('schemaVersion') not in (1, 2, 3):
        raise ValueError('Unsupported reading-room manifest')
    expected = {row['path'] for row in manifest['files']} | {'manifest.json'}
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if actual != expected:
        raise ValueError(f'File inventory differs: missing={len(expected - actual)}, extra={len(actual - expected)}')
    for row in manifest['files']:
        path = safe(root, row['path'])
        if path.stat().st_size != row['bytes'] or digest(path) != row['sha256']:
            raise ValueError(f'File bytes differ: {row["path"]}')
    from .covers import POLICY, date_label, validate_thumbnail
    strict_covers = require_thumbnails or manifest.get('coverPolicy') == POLICY
    if require_thumbnails and manifest.get('coverPolicy') != POLICY:
        raise ValueError('Reader has not completed thumbnail migration')
    catalog = read(root / 'catalog.json')
    if catalog.get('schemaVersion') not in (1, 2, 3):
        raise ValueError('Unsupported catalog version')
    issues = {row['id']: row for row in catalog['issues']}
    articles = {row['article_id']: row for row in catalog['articles']}
    if len(issues) != len(catalog['issues']) or len(articles) != len(catalog['articles']) or len({a['reference'] for a in articles.values()}) != len(articles):
        raise ValueError('Duplicate reading-room identity')
    memberships = Counter()
    counts = Counter()
    accounted_issues = set()
    for issue_id, summary in issues.items():
        date = issue_id.removeprefix('maso-')
        issue = read(root / f'issues/{date}.json')
        if 'scanRestoration' in issue:
            accounted_issues.add(issue_id)
        media = read(root / f'media/{date}.json')
        if issue['issue'] != summary or media['issueId'] != issue_id:
            raise ValueError(f'Issue identity differs: {issue_id}')
        if summary['cover']:
            cover = summary['cover']
            if cover['width'] <= 0 or cover['height'] <= 0 or digest(safe(root, cover['path'])) != cover['sha256']:
                raise ValueError(f'Cover differs: {issue_id}')
            counts['covers'] += 1
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
    cover_paths = {i['cover']['path'] for i in issues.values() if i['cover']}
    if strict_covers:
        cover_rows = manifest.get('coverInputs', [])
        if len(cover_rows) != len(cover_paths) or {r['path'] for r in cover_rows} != cover_paths:
            raise ValueError('Cover input inventory differs')
        actual_covers = {p.relative_to(root).as_posix() for p in (root / 'covers').rglob('*') if p.is_file()}
        if actual_covers != cover_paths:
            raise ValueError('Unreferenced or missing cover derivatives')
        for row in cover_rows:
            match = re.fullmatch(r'covers/(\d{4})-[0-9a-f]{24}-thumb\.jpg', row['path'])
            if not match or row['filename'] != Path(row['path']).name:
                raise ValueError('Invalid reader derivative filename')
            date = date_label(match[1])
            covered = [i for i in issues.values() if i['cover'] and i['cover']['path'] == row['path']]
            if row['issueIds'] != [i['id'] for i in covered]:
                raise ValueError('Cover issue membership differs')
            for issue in covered:
                if (issue['year'], issue['month']) != date or issue['cover'] != {k: row[k] for k in ('path', 'width', 'height', 'sha256')}:
                    raise ValueError('Cover date/assignment differs')
            path = safe(root, row['path'])
            validate_thumbnail(path, dict(row, bytes=path.stat().st_size))
        counts['coverAssets'] = len(cover_paths)
    for article_id, summary in articles.items():
        if memberships[article_id] != 1:
            raise ValueError(f'Article membership differs: {article_id}')
        doc = read(root / f'articles/{summary["reference"]}.json')
        if doc['article'] != summary:
            raise ValueError(f'Article identity differs: {article_id}')
        if summary.get('sourceKind') == 'scan':
            if manifest['schemaVersion'] != 3 or doc['schemaVersion'] != 3:
                raise ValueError('Scan articles require version 3')
            from .scan import validate_scan
            issue_doc = read(root / f'issues/{summary["issue_id"].removeprefix("maso-")}.json')
            entries = [t for t in issue_doc['toc'] if t['id'] == summary['tocEntryId'] and article_id in t['articleIds']]
            if len(entries) != 1:
                raise ValueError('Scan TOC identity/link differs')
            validate_scan(root, doc, entries[0])
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
    scan_inputs = manifest.get('scanInputs', [])
    scan_ids = {a['article_id'] for a in articles.values() if a.get('sourceKind') == 'scan'}
    if len(scan_inputs) != len(scan_ids) or {s['articleId'] for s in scan_inputs} != scan_ids:
        raise ValueError('Scan input coverage differs')
    for source in scan_inputs:
        summary = articles[source['articleId']]
        if source['packagePath'] != summary['referencePath']:
            raise ValueError('Scan input package identity differs')
        path = safe(root / 'source', source['packagePath']).parent / 'manifest.json'
        if digest(path) != source['manifestSha256']:
            raise ValueError('Copied scan manifest differs')
    scan_issues = manifest.get('scanIssues', [])
    if len({s['issueId'] for s in scan_issues}) != len(scan_issues) or {s['issueId'] for s in scan_issues} != accounted_issues:
        raise ValueError('Scan issue accounting coverage differs')
    for source in scan_issues:
        from .scan_issue import validate_issue
        path = safe(root, source['path'])
        if digest(path) != source['sha256'] or source['issueId'] not in issues:
            raise ValueError('Scan issue accounting pin differs')
        issue_doc = read(root / f'issues/{source["issueId"].removeprefix("maso-")}.json')
        validate_issue(root, issue_doc, read(path))
    search = read(root / 'search.json')['items']
    for source in scan_issues:
        for row in read(safe(root, source['path']))['entries']:
            matches = [s for s in search if s['kind'] == 'toc' and s['id'] == row['id']]
            links = [row['articleId']] if row.get('articleId') else []
            if (len(matches) != 1 or matches[0].get('articleIds') != links or
                    matches[0]['issueId'] != source['issueId'] or
                    matches[0]['status'] != ('linked' if links else row['classification'])):
                raise ValueError('Scan issue search TOC differs')
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
    parser.add_argument('--require-thumbnails', action='store_true')
    args = parser.parse_args()
    print(json.dumps(check(args.data, require_thumbnails=args.require_thumbnails)))


if __name__ == '__main__':
    main()
