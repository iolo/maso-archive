"""Version 3: stage one reviewed scan package alongside unchanged CD reader data."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile

from .export import digest, read, safe, text_for, write
from tools.pdf_restore.build import check_export


def project(package, toc):
    """Pure reader projection, also used to verify every scan field against its package."""
    id = package['id']
    if toc['id'] != package['toc_entry_id']:
        raise ValueError('Scan package does not match the canonical TOC entry')
    if package['relationships']:
        raise ValueError('Version relationships need a reviewed comparison adapter; cannot infer or copy unchecked links')
    prefix = f'pdf/{id}'
    path_pin = lambda pin: {**pin, 'path': f'{prefix}/{pin["path"]}'}
    figures = {f['id']: f for f in package['figures']}
    source_blocks = {b['id']: b for b in package['blocks']}
    media = []
    for figure in figures.values():
        asset = figure['asset']
        media.append(dict(issue=package['issue_id'].removeprefix('maso-'),
                          resource=f'{id}-{figure["id"]}', status='available',
                          asset_name=Path(asset['path']).name, original_sha256=asset['sha256'],
                          originalPath=f'{prefix}/{asset["path"]}', previewPath=f'{prefix}/{asset["path"]}',
                          conversion_note='Scan-region crop; original PDF identity remains in scan provenance.'))
    blocks, paragraphs = [], []
    offset = 0
    for index, item in enumerate(package['content_order']):
        block_id = f'{id}:{item["type"]}:{item["id"]}'
        if item['type'] == 'block':
            source = source_blocks[item['id']]
            kind = {'prose': 'paragraph', 'section-label': 'heading'}.get(source['kind'], source['kind'])
            runs = [dict(type='text', text=source['text'])]
            metadata = dict(scanBlockId=source['id'], regionIds=source['region_ids'])
        else:
            source = figures[item['id']]
            kind = 'figure'
            runs = [dict(type='media', resource=f'{id}-{source["id"]}',
                         textMarker=f'[그림 {source["id"]}: 스캔 이미지 참조]')]
            metadata = dict(scanFigureId=source['id'], regionIds=source['region_ids'])
        block = dict(id=block_id, type=kind, preformatted=kind == 'code', **metadata,
                     paragraphs=[dict(id=block_id + ':p', runs=runs, terminated=False)])
        blocks.append(block)
        length = len(text_for([block]))
        paragraphs.append(dict(id=block_id + ':p', character_offset=offset, characters=length,
                               regionIds=source['region_ids']))
        offset += length
        # Keep separators outside literal code/prose blocks; article.txt is unchanged.
        separator = '\n' if index == len(package['content_order']) - 1 else '\n\n'
        blocks.append(dict(id=f'{id}:separator:{index}', type='spacing', preformatted=False,
                           paragraphs=[dict(id=f'{id}:separator:{index}:p', runs=[dict(type='text', text=separator)], terminated=False)]))
        offset += len(separator)
    downloads = {d['path']: d for d in package['downloads']}
    text = downloads.get('article.txt')
    listing = downloads.get('listing.txt')
    listings = ([dict(path='listing.txt', block_id='', sha256=listing['sha256'],
                      characters=sum(len(b['text']) for b in package['blocks'] if b['kind'] == 'code'))] if listing else [])
    summary = dict(reference=id, article_id=id, issue_id=package['issue_id'], title=package['title'],
                   byline=toc['byline'], page=toc['page'], status=package['availability'],
                   sourceKind='scan', availability=package['availability'], verification=package['verification']['status'],
                   tocEntryId=package['toc_entry_id'], path=f'{prefix}/index.html',
                   referencePath=f'{prefix}/article.json', paragraphsPath=f'pdf-adapter/{id}/paragraphs.json',
                   text=f'{prefix}/article.txt' if text else None, text_sha256=text['sha256'] if text else None,
                   paragraphs=len(paragraphs), listings=len(listings), image_occurrences=len(figures),
                   resources=[m['resource'] for m in media])
    assets = {a['region_id']: path_pin(a['asset']) for a in package['region_assets']}
    scan = dict(packagePath=f'{prefix}/article.json', source=package['source'],
                coordinates=package['coordinates'], pages=package['pages'],
                regions=[{**r, 'asset': assets.get(r['id'])} for r in package['regions']],
                excludedRegions=package['excluded_regions'], contentOrder=package['content_order'],
                figures=package['figures'], availability=package['availability'], verification=package['verification'],
                gaps=package['gaps'], relationships=[], downloads=[path_pin(d) for d in package['downloads']],
                corrections=[path_pin(d) for d in package['corrections']],
                reviewRecords=[path_pin(d) for d in package['review_records']])
    doc = dict(schemaVersion=3, article=summary, blocks=blocks, listings=listings,
               media=media, details='Scan-derived reading; see the recorded review scope and gaps.', scan=scan)
    return doc, paragraphs


def validate_scan(root, doc, toc):
    path = safe(root / 'source', doc['scan']['packagePath'])
    package = check_export(path.parent)
    expected, paragraphs = project(package, toc)
    expected['scan']['packageSha256'] = digest(path)
    if expected != doc:
        raise ValueError('Scan reader projection differs from its pinned package')
    if read(safe(root / 'source', doc['article']['paragraphsPath'])) != paragraphs:
        raise ValueError('Scan paragraph positions differ')
    if doc['article']['issue_id'] != package['issue_id']:
        raise ValueError('Scan issue identity differs')
    # Validated package inventory contains every region, raw OCR and download.
    return package


def stage(base, package_dir, output, covers=None):
    base, package_dir, output = (Path(p).resolve() for p in (base, package_dir, output))
    if output.exists() or output.is_relative_to(base) or base.is_relative_to(output):
        raise ValueError('Use a separate, fresh reader output')
    if output.is_relative_to(package_dir) or package_dir.is_relative_to(output):
        raise ValueError('Output overlaps scan input')
    from .check import check
    check(base)
    base_manifest_sha = digest(base / 'manifest.json')
    package = check_export(package_dir)
    package_manifest_sha = digest(package_dir / 'manifest.json')
    if package['availability'] != 'readable' or package['verification']['status'] == 'unreviewed':
        raise ValueError('Step 8 requires a readable, reviewed pilot')
    catalog = read(base / 'catalog.json')
    if any(a['article_id'] == package['id'] or a['reference'] == package['id'] for a in catalog['articles']):
        raise ValueError('Scan article identity already exists')
    issue_id = package['issue_id']
    issue_path = f'issues/{issue_id.removeprefix("maso-")}.json'
    issue = read(safe(base, issue_path))
    if issue['issue']['id'] != issue_id:
        raise ValueError('Canonical issue differs')
    matches = [t for t in issue['toc'] if t['id'] == package['toc_entry_id']]
    if len(matches) != 1:
        raise ValueError('Expected exactly one canonical TOC entry')
    toc = matches[0]
    doc, paragraphs = project(package, toc)
    doc['scan']['packageSha256'] = digest(package_dir / 'article.json')
    summary = doc['article']
    if text_for(doc['blocks']).encode() != (package_dir / 'article.txt').read_bytes():
        raise ValueError('Scan projection changes article text')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.scan-reader-', dir=output.parent) as temp:
        staged = Path(temp) / 'data'
        shutil.copytree(base, staged)  # Independent files: never link mutable catalog/issue docs.
        destination = staged / 'source' / 'pdf' / package['id']
        if destination.exists():
            raise ValueError('Scan source destination already exists')
        shutil.copytree(package_dir, destination)
        write(staged / 'source', summary['paragraphsPath'], paragraphs)
        write(staged, f'articles/{summary["reference"]}.json', doc)
        toc['articleIds'].append(package['id'])
        issue['articles'].append(summary)
        issue['schemaVersion'] = 3
        issue['issue']['articleCount'] += 1
        issue['issue']['textCount'] += 1
        write(staged, issue_path, issue)
        catalog['schemaVersion'] = 3
        catalog['issues'] = [issue['issue'] if i['id'] == issue_id else i for i in catalog['issues']]
        catalog['articles'].append(summary)
        write(staged, 'catalog.json', catalog)
        media_path = f'media/{issue_id.removeprefix("maso-")}.json'
        media = read(staged / media_path)
        if {m['resource'] for m in media['items']} & set(summary['resources']):
            raise ValueError('Scan media identity collision')
        media['schemaVersion'] = 3
        media['items'].extend(doc['media'])
        write(staged, media_path, media)
        search = read(staged / 'search.json')
        search['schemaVersion'] = 3
        search_matches = [r for r in search['items'] if r['kind'] == 'toc' and r['id'] == toc['id']]
        if len(search_matches) != 1:
            raise ValueError('Canonical search TOC entry missing or duplicated')
        search_matches[0]['articleIds'] = toc['articleIds']
        search_matches[0]['status'] = 'linked'
        search['items'].append(dict(kind='article', id=package['id'], issueId=issue_id, title=summary['title'],
                                    byline=summary['byline'], reference=summary['reference'], status=summary['status'],
                                    sourceKind='scan', availability=summary['availability'], verification=summary['verification']))
        write(staged, 'search.json', search)
        manifest = deepcopy(read(base / 'manifest.json'))
        cover_issue_paths = set()
        if covers is not None:
            from .covers import attach_covers
            manifest['coverInputs'] = attach_covers(staged, catalog, covers)
            cover_issue_paths = {f'issues/{i.removeprefix("maso-")}.json'
                                 for row in manifest['coverInputs'] for i in row['issueIds']}
            manifest['counts']['covers'] = sum(i['cover'] is not None for i in catalog['issues'])
            write(staged, 'catalog.json', catalog)
        manifest.update(schemaVersion=3, baseManifestSha256=base_manifest_sha,
                        scanInputs=[dict(articleId=package['id'], manifestSha256=package_manifest_sha,
                                         packagePath=doc['scan']['packagePath'])])
        for key, added in dict(articles=1, texts=1, listings=len(doc['listings']), mediaRecords=len(doc['media'])).items():
            manifest['counts'][key] += added
        manifest['files'] = [dict(path=p.relative_to(staged).as_posix(), bytes=p.stat().st_size, sha256=digest(p))
                             for p in sorted(staged.rglob('*')) if p.is_file() and p != staged / 'manifest.json']
        write(staged, 'manifest.json', manifest)
        check(staged)
        # Only these five baseline documents may differ. All CD article/source files are exact copies.
        changed = {'catalog.json', 'manifest.json', 'search.json', issue_path, media_path} | cover_issue_paths
        for record in read(base / 'manifest.json')['files']:
            if record['path'] not in changed and digest(safe(staged, record['path'])) != record['sha256']:
                raise ValueError('Existing reader file changed during scan export')
        if digest(base / 'manifest.json') != base_manifest_sha or digest(package_dir / 'manifest.json') != package_manifest_sha:
            raise ValueError('Input manifest changed during export')
        staged.rename(output)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=Path('build/reading-room/data'))
    parser.add_argument('--package', type=Path, default=Path('build/pdf-restoration/pilot'))
    parser.add_argument('--output', type=Path, default=Path('build/reading-room-pdf-pilot/data'))
    parser.add_argument('--covers', type=Path, help='Include reviewed/owner covers through the existing cover adapter')
    args = parser.parse_args()
    result = stage(args.base, args.package, args.output, args.covers)
    print(json.dumps(result['counts']))


if __name__ == '__main__':
    main()
