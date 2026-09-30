"""Version 2 adapter for the completed, independently preserved disc references."""
from collections import Counter
from pathlib import Path
import tempfile

from .export import copy, digest, export, read, safe, text_for, write
from tools.cd3_display import reading_run


def checked_reference(root, disc):
    """CD2 inventories groups separately; CD3 inventories the entire tree."""
    manifest = read(root / 'manifest.json')
    if manifest.get('schema_version') != 1 or manifest.get('disc_id') != disc:
        raise ValueError(f'Unsupported {disc} reference')
    inventory = list(manifest['files'])
    if disc == 'cd2':
        for group in manifest['issues']:
            base = f'issues/{group["issue_group"]}'
            path = safe(root, f'{base}/manifest.json')
            if digest(path) != group['manifest_sha256']:
                raise ValueError(f'Changed group manifest: {base}')
            inventory.append({'path': f'{base}/manifest.json', 'bytes': path.stat().st_size,
                              'sha256': digest(path)})
            inventory.extend({**row, 'path': f'{base}/{row["path"]}'}
                             for row in read(path)['files'])
    expected = {row['path'] for row in inventory} | {'manifest.json'}
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if expected != actual:
        raise ValueError(f'{disc} reference inventory differs')
    for row in inventory:
        path = safe(root, row['path'])
        if path.stat().st_size != row['bytes'] or digest(path) != row['sha256']:
            raise ValueError(f'Changed {disc} reference file: {row["path"]}')
    return manifest


def project_blocks(source, disc, media):
    """Keep literal text and displayed CD3 figure targets in source order."""
    blocks = []
    occurrences = iter(source['candidate']['media'])
    resources = []
    for paragraph in source['paragraphs']:
        runs = []
        for run in paragraph['runs']:
            if run['type'] == 'text':
                if disc == 'cd3':
                    run = reading_run(run)
                runs.append({'type': 'text', 'text': run['text'],
                             'marks': [m for m in ('bold', 'italic', 'underline', 'strike', 'small_caps') if run.get(m)]})
                continue
            item = next(occurrences)
            if item['name'] != run['resource']:
                raise ValueError('Native media order differs')
            if disc == 'cd3' and item['target_alias'] and item['target_media'] is None:
                runs.append({'type': 'text', 'text': f"[figure:{item['target_alias']} · target unresolved]"})
                continue
            figure = item.get('target_media')
            shown = figure or item
            name = shown.get('source_name') or shown['name']
            if name not in media:
                if disc != 'cd3' or shown['available']:
                    raise ValueError(f'Unaccounted native media: {name}')
                media[name] = {'issue': '', 'resource': name, 'status': 'missing',
                               'asset_name': None, 'originalPath': None, 'previewPath': None,
                               'original_sha256': '', 'conversion_note': 'CD source image unavailable'}
            marker = f"[{'figure' if figure else 'image'}:{shown['name']}]"
            resources.append(name)
            runs.append({'type': 'media', 'resource': name, 'textMarker': marker})
        blocks.append({'id': paragraph['id'], 'type': 'paragraph', 'preformatted': False,
                       'paragraphs': [{'id': paragraph['id'], 'runs': runs,
                                       'terminated': paragraph['terminated']}]})
    if next(occurrences, None) is not None:
        raise ValueError('Unused native media occurrences')
    return blocks, list(dict.fromkeys(resources))


def add_disc(root, disc, output, catalog, search):
    checked_reference(root, disc)
    # Keep the complete portable reference, including sidebars and media shelves.
    for path in sorted(root.rglob('*')):
        if path.is_file():
            copy(root, output / 'source' / disc, path.relative_to(root).as_posix())
    group_dir = 'issues' if disc == 'cd2' else 'groups'
    native_catalog = read(root / ('coverage.json' if disc == 'cd2' else 'catalog.json'))
    native_articles = native_catalog['articles']
    cd3_targets = {a['identity']: a['group'] for a in native_articles} if disc == 'cd3' else {}
    totals = Counter()
    for group_path in sorted((root / group_dir).iterdir()):
        group = group_path.name
        issue_id = f'{disc}-{group}'
        prefix = f'{disc}/{group_dir}/{group}'
        rows = read(group_path / 'articles.json')['articles']
        media = {}
        for item in read(group_path / 'media.json')['resources']:
            name = item['name']
            media[name] = {'issue': issue_id, 'resource': name,
                           'status': item['status'], 'asset_name': name + '.png' if item['preview_sha256'] else None,
                           'originalPath': f'{prefix}/media/{name}',
                           'previewPath': f'{prefix}/media/{name}.png' if item['preview_sha256'] else None,
                           'original_sha256': item['original_sha256'], 'conversion_note': item['note']}
        articles = []
        dated = len(group) == 4 and group.isdigit() and 1 <= int(group[2:]) <= 12
        issue = {'id': issue_id, 'year': 1900 + int(group[:2]) if dated else 0,
                 'month': int(group[2:]) if dated else 0, 'label': f'{disc.upper()} · {group}',
                 'disc': disc, 'nativeGroup': True, 'articleCount': len(rows),
                 'textCount': 0, 'tocCount': 0, 'cover': None}
        for row in rows:
            identity = row['id'] if disc == 'cd2' else row['identity']
            reference = f'{disc}-{identity}'
            base = f'{prefix}/articles/{identity}'
            local_base = group_path / 'articles' / identity
            source = read(local_base / 'blocks.json')
            blocks, resources = project_blocks(source, disc, media)
            for name in resources:
                media[name]['issue'] = issue_id
            if row['status'] not in ('success', 'partial'):
                raise ValueError(f'Unsupported native outcome: {reference}')
            if digest(local_base / 'article.txt') != row['text_sha256'] or text_for(blocks).encode() != (local_base / 'article.txt').read_bytes():
                raise ValueError(f'Native text differs: {reference}')
            listings = [{'path': p.relative_to(local_base).as_posix(), 'block_id': '',
                         'sha256': digest(p), 'characters': len(p.read_text(encoding='utf-8'))}
                        for p in sorted((local_base / 'listings').glob('*.txt'))]
            article = {'reference': reference, 'nativeReference': identity, 'disc': disc,
                       'article_id': f'{disc}:article:{identity}', 'issue_id': issue_id,
                       'title': row['title'], 'byline': None, 'page': None, 'status': row['status'],
                       'path': f'{base}/index.html', 'text': f'{base}/article.txt',
                       'referencePath': f'{base}/blocks.json', 'paragraphsPath': f'{base}/blocks.json',
                       'paragraphs': row['paragraphs'], 'listings': len(listings),
                       'image_occurrences': row['media_occurrences'], 'resources': resources,
                       'text_sha256': row['text_sha256']}
            links = []
            for link in source['candidate'].get('links', []):
                target = link['target_topic']
                if target is None:
                    continue
                path = (f'{disc}/groups/{cd3_targets[target]}/articles/{target}/index.html'
                        if target in cd3_targets else f'{disc}/supplements/{target}/index.html')
                safe(output / 'source', path).stat()
                if not any(item['path'] == path for item in links):
                    links.append({'label': f"{link['alias']} · {target}", 'path': path})
            doc = {'schemaVersion': 2, 'article': article, 'blocks': blocks, 'listings': listings,
                   'details': '\n'.join(row['reasons']), 'media': [media[n] for n in resources],
                   'attachments': [{**a, 'path': f'{base}/{a["path"]}'} for a in row['attachments']],
                   'relatedSources': links}
            write(output, f'articles/{reference}.json', doc)
            articles.append(article)
            search['items'].append({'kind': 'article', 'id': article['article_id'],
                                    'issueId': issue_id, 'title': row['title'], 'byline': None,
                                    'reference': identity, 'status': row['status']})
            totals['texts'] += 1
            totals['listings'] += len(listings)
            totals['attachments'] += len(row['attachments'])
        issue['textCount'] = len(articles)
        write(output, f'issues/{issue_id}.json', {'schemaVersion': 2, 'issue': issue, 'toc': [], 'articles': articles})
        write(output, f'media/{issue_id}.json', {'schemaVersion': 2, 'issueId': issue_id, 'items': list(media.values())})
        catalog['issues'].append(issue)
        catalog['articles'].extend(articles)
        totals['issues'] += 1
        totals['articles'] += len(articles)
        totals['mediaRecords'] += len(media)
    if totals['articles'] != native_catalog.get('candidate_count', native_catalog.get('candidates')):
        raise ValueError(f'{disc} candidate count differs')
    return {'disc': disc, 'manifestSha256': digest(root / 'manifest.json'),
            'referencePath': f'{disc}/index.html', 'counts': dict(totals),
            'outcomes': native_catalog['outcomes']}


def aggregate(cd1, toc, cd2, cd3, output, covers=None, cover_checkpoint=None, thumbnails=None,
              tocs=None, toc_images=None, toc_reviews=None):
    output = Path(output)
    from .covers import DEFAULT_OUTPUT, POLICY, separate
    separate(output, cover_checkpoint, thumbnails or DEFAULT_OUTPUT)
    roots = [Path(p).resolve() for p in (cd1, toc, cd2, cd3)]
    if covers is not None:
        roots.append(Path(covers).resolve())
    separate(thumbnails or DEFAULT_OUTPUT, *roots, cover_checkpoint, output)
    from .tocs import DEFAULT_OUTPUT as TOC_IMAGES, refresh
    separate(output, tocs, toc_images or TOC_IMAGES, toc_reviews)
    separate(toc_images or TOC_IMAGES, *roots, cover_checkpoint, thumbnails or DEFAULT_OUTPUT, output, tocs, toc_reviews)
    if any(output.resolve().is_relative_to(p) or p.is_relative_to(output.resolve()) for p in roots):
        raise ValueError('Output must not overlap inputs')
    output.parent.mkdir(parents=True, exist_ok=True)
    # Validate/build in isolation so a failed export leaves the usable reader intact.
    with tempfile.TemporaryDirectory(prefix='.reading-room-', dir=output.parent) as temp:
        stage = Path(temp) / 'data'
        manifest = export(cd1, toc, stage)
        catalog, search = read(stage / 'catalog.json'), read(stage / 'search.json')
        sources = [{'disc': 'cd1', 'manifestSha256': manifest['sourceManifestSha256'],
                    'counts': dict(manifest['counts'])}]
        for disc, root in [('cd2', Path(cd2)), ('cd3', Path(cd3))]:
            sources.append(add_disc(root, disc, stage, catalog, search))
        catalog['schemaVersion'] = search['schemaVersion'] = 2
        catalog['sources'] = sources
        catalog['issues'].sort(key=lambda i: (i['year'] or 9999, i['month'], i['id']))
        from .covers import attach_covers
        manifest['coverInputs'] = attach_covers(stage, catalog, covers, cover_checkpoint, thumbnails)
        write(stage, 'catalog.json', catalog)
        write(stage, 'search.json', search)
        counts = Counter(manifest['counts'])
        for source in sources[1:]:
            counts.update({k: v for k, v in source['counts'].items() if k != 'attachments'})
        manifest['coverPolicy'] = POLICY
        counts['coverAssets'] = len(manifest['coverInputs'])
        counts['covers'] = sum(i['cover'] is not None for i in catalog['issues'])
        manifest.update(schemaVersion=2, sources=sources, counts=dict(counts))
        manifest['files'] = [{'path': p.relative_to(stage).as_posix(), 'bytes': p.stat().st_size,
                              'sha256': digest(p)} for p in sorted(stage.rglob('*'))
                             if p.is_file() and p != stage / 'manifest.json']
        write(stage, 'manifest.json', manifest)
        if tocs is not None:
            refresh(stage, manifest, tocs, toc_images, toc_reviews)
        from .check import check
        check(stage)
        backup = Path(temp) / 'previous-data'
        if output.exists():
            output.rename(backup)
        try:
            stage.rename(output)
        except OSError:
            if backup.exists():
                backup.rename(output)
            raise
    return manifest
