"""Rebuild the volunteer reader from preserved CD references and PDF closeouts."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil

from maso_archive.storage import canonical_path
from tools.pdf_restore.inventory import ROOT, pin
from tools.pdf_restore.issue import accounting, inventory
from .export import digest, read, safe, write
from .frozen import check_package, validate_report
from .scan import project

INPUTS = ROOT / 'metadata/catalog/reading-room-volunteer.json'
DATES = ('1983-11', '1984-02', '1984-03', '1984-05', '1984-06', '1984-07',
         '1984-08', '1984-09', '1984-10', '1984-12', '1985-02', '1985-03',
         '1985-10', '1985-11', '1988-01', '1991-08', '1991-09', '1992-12', '1993-03',
         '1995-03', '1995-07')
LEGACY = {
    '1983-11': 'archive/pdf/1983-11/restoration/11-november/issue-progress.json',
    '1984-02': 'archive/pdf/1984-02/restoration/12-1984-02-closeout/issue-progress-after.json',
    '1984-06': 'archive/pdf/1984-06/restoration/12-1984-06-qwen/whole-issue-ledger.json',
    '1984-07': 'archive/pdf/1984-07/restoration/12-1984-07-comparison/whole-issue-ledger.json',
}
TITLE_CHANGES = {
    'maso-1984-09-toc-0008': {'before': '바라케이드', 'after': '바리케이드'},
    'maso-1984-09-toc-0038': {'before': '리뷰 살롱', 'after': '신간 안내'},
}


def checked(root, record):
    path = safe(root, record['path'])
    if pin(root, record['path']) != record:
        raise ValueError(f'Reader input changed: {record["path"]}')
    return path


def prepare_inputs(output=INPUTS, root=ROOT):
    """Explicit selections; never discover an arbitrary latest package revision."""
    issues = []
    for date in DATES:
        if date in LEGACY:
            ledger_path = root / LEGACY[date]
            ledger = read(ledger_path)
            packages = []
            for entry in ledger['entries']:
                if entry['classification'] != 'article':
                    continue
                restoration = entry['restoration']
                path = canonical_path(root / restoration['manifest']['path'])
                record = pin(root, path.relative_to(root).as_posix())
                if any(record[k] != restoration['manifest'][k] for k in ('sha256', 'bytes')):
                    raise ValueError('Legacy selected package changed')
                packages.append(dict(tocEntryId=entry['toc_entry_id'], articleId=restoration['article_id'], manifest=record))
            issues.append(dict(issueId=f'maso-{date}', ledger=pin(root, LEGACY[date]), packages=packages))
        else:
            path = f'archive/pdf/{date}/reference/manifest.json'
            issues.append(dict(issueId=f'maso-{date}', manifest=pin(root, path)))
    data = dict(schemaVersion=1, scope=f'All {len(DATES)} completed supplied-PDF passes and all three CD references; volunteer reader.',
                toc=pin(root, 'archive/toc/current/manifest.json'),
                discs={d: pin(root, f'archive/{d}/reference/manifest.json') for d in ('cd1', 'cd2', 'cd3')},
                canonicalTitleChanges=TITLE_CHANGES, issues=issues,
                validationScope='Frozen closeout inventories, schemas, ownership and reader projections. Original assembly reconstruction remains evidenced by issue closeouts; this build does not rerun restoration or certify human proofreading.')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return data


def load_issue(spec, issue, root):
    if 'ledger' in spec:
        ledger = read(checked(root, spec['ledger']))
        directories, packages = {}, {}
        for row in spec['packages']:
            folder = checked(root, row['manifest']).parent
            package = check_package(folder, row['manifest']['sha256'])
            if package['id'] != row['articleId'] or package['toc_entry_id'] != row['tocEntryId']:
                raise ValueError('Legacy selected package identity differs')
            directories[row['tocEntryId']] = folder
            packages[row['tocEntryId']] = package
        report = accounting(ledger, issue['toc'], packages)
        return report, packages, directories, None
    folder = checked(root, spec['manifest']).parent
    manifest = read(folder / 'manifest.json')
    if manifest['files'] != inventory(folder):
        raise ValueError('Standalone issue inventory changed')
    index = read(folder / 'issue.json')
    report = read(checked(folder, index['accounting']))
    packages, directories = {}, {}
    for row in index['articles']:
        directory = checked(folder, row['manifest']).parent
        package = check_package(directory, row['manifest']['sha256'])
        if (package['id'] != row['articleId'] or package['toc_entry_id'] != row['tocEntryId'] or
                safe(folder, row['path']) != directory / 'article.json' or row['tocEntryId'] in packages):
            raise ValueError('Standalone package identity differs')
        packages[row['tocEntryId']], directories[row['tocEntryId']] = package, directory
    return report, packages, directories, folder


def add_issue(data, spec, inputs, root=ROOT):
    issue_id = spec['issueId']
    date = issue_id.removeprefix('maso-')
    print(f'Validating and copying {issue_id}', flush=True)
    issue = read(data / f'issues/{date}.json')
    report, packages, directories, standalone = load_issue(spec, issue, root)
    if report['issueId'] != issue_id:
        raise ValueError('Selected issue identity differs')
    report = deepcopy(report)
    changes = {}
    for row in report['entries']:
        change = inputs['canonicalTitleChanges'].get(row['id'])
        if change:
            if row['title'] != change['before']:
                raise ValueError('Canonical title mapping source differs')
            changes[row['id']] = change
            row.update(sourceTitle=row['title'], title=change['after'])
    catalog, search, manifest = (read(data / name) for name in ('catalog.json', 'search.json', 'manifest.json'))
    old_ids = {a['article_id'] for a in catalog['articles']}
    media = read(data / f'media/{date}.json')
    if standalone:
        target = data / 'source' / 'pdf-issues' / date
        shutil.copytree(standalone, target)
    else:
        target = data / 'source' / 'pdf-issues' / date
        target.mkdir(parents=True)
        shutil.copyfile(checked(root, spec['ledger']), target / 'ledger.json')
    for toc, row in zip(issue['toc'], report['entries'], strict=True):
        if toc['id'] != row['id']:
            raise ValueError('Selected issue TOC order differs')
        if row['bodyOwner'] is True:
            package, folder = packages[row['id']], directories[row['id']]
            if package['id'] in old_ids:
                raise ValueError('Duplicate scan identity')
            prefix = f'pdf-issues/{date}/articles/{package["id"]}' if standalone else f'pdf/{package["id"]}'
            if not standalone:
                shutil.copytree(folder, data / 'source' / prefix)
            doc, paragraphs = project(package, toc, prefix=prefix)
            doc['scan']['packageSha256'] = digest(folder / 'article.json')
            write(data / 'source', doc['article']['paragraphsPath'], paragraphs)
            write(data, f'articles/{package["id"]}.json', doc)
            summary = doc['article']
            issue['articles'].append(summary)
            catalog['articles'].append(summary)
            resources = {m['resource'] for m in media['items']}
            if resources & set(summary['resources']):
                raise ValueError('Scan media identity collision')
            media['items'].extend(doc['media'])
            manifest.setdefault('scanInputs', []).append(dict(articleId=package['id'], manifestSha256=digest(folder / 'manifest.json'), packagePath=doc['scan']['packagePath']))
            search['items'].append(dict(kind='article', id=package['id'], issueId=issue_id, title=summary['title'],
                                        byline=summary['byline'], reference=summary['reference'], status=summary['status'],
                                        sourceKind='scan', availability=summary['availability'], verification=summary['verification']))
            for key, value in dict(articles=1, texts=int(bool(summary['text'])), listings=len(doc['listings']), mediaRecords=len(doc['media'])).items():
                manifest['counts'][key] += value
        # Prefer the restored scan; preserve all existing CD associations.
        links = [row['articleId']] if row.get('articleId') else []
        toc.update(restorationKind=row['classification'], articleIds=links + toc['articleIds'])
        if row.get('eligibility'):
            toc['restorationEligibility'] = row['eligibility']
        if row.get('sectionRef'):
            toc['sectionRef'] = row['sectionRef']
        matches = [s for s in search['items'] if s['kind'] == 'toc' and s['id'] == toc['id']]
        if len(matches) != 1:
            raise ValueError('Canonical search entry missing or duplicated')
        matches[0].update(articleIds=toc['articleIds'], status='linked' if toc['articleIds'] else row['classification'])
    issue.update(schemaVersion=3, scanRestoration=report)
    issue['issue'].update(articleCount=len(issue['articles']), textCount=sum(bool(a['text']) for a in issue['articles']))
    validate_report(issue, report, packages)
    catalog.update(schemaVersion=3, issues=[issue['issue'] if i['id'] == issue_id else i for i in catalog['issues']])
    search['schemaVersion'] = media['schemaVersion'] = manifest['schemaVersion'] = 3
    report_path = f'scan-issues/{date}.json'
    write(data, report_path, report)
    manifest.setdefault('scanIssues', []).append(dict(issueId=issue_id, path=report_path, sha256=digest(data / report_path),
                                                     ledgerSha256=spec.get('ledger', spec.get('manifest'))['sha256']))
    manifest.setdefault('frozenIssues', []).append(dict(issueId=issue_id, accountingSha256=digest(data / report_path),
                                                       input=spec, canonicalTitleChanges=changes))
    for name, value in [(f'issues/{date}.json', issue), (f'media/{date}.json', media), ('catalog.json', catalog), ('search.json', search), ('manifest.json', manifest)]:
        write(data, name, value)
    print(f'Copied {len(packages)} {date} bodies; original outcomes retained', flush=True)


def export(inputs_path, output, stages, root=ROOT):
    output, stages = Path(output).resolve(), Path(stages).resolve()
    if output.exists() or output.is_relative_to(stages) or stages.is_relative_to(output):
        raise ValueError('Use fresh, separate output and staging directories')
    inputs = read(inputs_path)
    if inputs['schemaVersion'] != 1 or [i['issueId'] for i in inputs['issues']] != [f'maso-{d}' for d in DATES]:
        raise ValueError(f'Expected all {len(DATES)} selected PDF issues in order')
    from .covers import separate
    sources = [root / f'archive/{disc}/reference' for disc in ('cd1', 'cd2', 'cd3')]
    sources += [root / 'archive/toc', root / 'archive/covers', root / 'covers', root / 'tocs', Path(inputs_path)]
    for spec in inputs['issues']:
        records = [spec['manifest']] if 'manifest' in spec else [p['manifest'] for p in spec['packages']] + [spec['ledger']]
        sources.extend(canonical_path(root / row['path']).parent for row in records)
    separate(stages, *sources)
    separate(output, *sources)
    checked(root, inputs['toc'])
    for record in inputs['discs'].values():
        checked(root, record)
    data = stages / 'data'
    from .check import check
    if data.exists() and read(data / 'manifest.json').get('frozenIssues'):
        selected = read(data / 'manifest.json')['frozenIssues']
        if [r['issueId'] for r in selected] != [r['issueId'] for r in inputs['issues']]:
            raise ValueError('Incomplete issue copy; retain this stage and use a fresh stage')
        return finish(inputs_path, data, output, root)
    required = 512 * 1024 * 1024  # Reader projections, manifests and filesystem overhead.
    for spec in inputs['issues']:
        manifests = [spec['manifest']] if 'manifest' in spec else [p['manifest'] for p in spec['packages']]
        for record in manifests:
            required += sum(r['bytes'] for r in read(checked(root, record))['files'])
    if not data.exists():
        required += sum(p.stat().st_size for disc in ('cd1', 'cd2', 'cd3')
                        for p in (root / f'archive/{disc}/reference').rglob('*') if p.is_file())
    stages.mkdir(parents=True, exist_ok=True)
    free = shutil.disk_usage(stages).free
    if free < required:
        raise ValueError(f'Insufficient staging space: need approximately {required / 1024**3:.1f} GiB free; have {free / 1024**3:.1f} GiB')
    if not data.exists():
        from .aggregate import aggregate
        from .covers import DEFAULT_CHECKPOINT, DEFAULT_OUTPUT
        from tools.toc_restore.inventory import SOURCES, PRIVATE
        aggregate(root / 'archive/cd1/reference', root / 'archive/toc/current',
                  root / 'archive/cd2/reference', root / 'archive/cd3/reference', data,
                  root / 'covers', DEFAULT_CHECKPOINT, DEFAULT_OUTPUT, SOURCES, None, PRIVATE / 'reviews.json')
    check(data, require_thumbnails=True)
    if read(data / 'manifest.json').get('scanInputs'):
        raise ValueError('Staging directory already has scan data; use a fresh stage')
    original = read(data / 'manifest.json')
    save_cd_baseline(data, data)
    for spec in inputs['issues']:
        add_issue(data, spec, inputs, root)
    return finish(inputs_path, data, output, root)


def save_cd_baseline(base, data):
    """Retain a CD-only receipt so interrupted builds can verify preservation."""
    baseline = read(base / 'manifest.json')
    if baseline.get('scanInputs'):
        raise ValueError('Expected a CD-only baseline')
    links = {}
    for issue in read(base / 'catalog.json')['issues']:
        doc = read(base / f'issues/{issue["id"].removeprefix("maso-")}.json')
        links.update({r['id']: r['articleIds'] for r in doc['toc']})
    write(data, 'cd-baseline.json', dict(manifest=baseline, tocLinks=links))


def finish(inputs_path, data, output, root=ROOT):
    """Finalize an already copied stage without another archive-sized copy."""
    from .check import check
    inputs = read(inputs_path)
    manifest = read(data / 'manifest.json')
    if [r['input'] for r in manifest['frozenIssues']] != inputs['issues']:
        raise ValueError('Staged issue selections differ from requested inputs')
    # Compatibility with the first interrupted build, which predated receipts.
    for spec in inputs['issues']:
        date = spec['issueId'].removeprefix('maso-')
        if 'ledger' in spec:
            path = data / 'source/pdf-issues' / date / 'ledger.json'
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(checked(root, spec['ledger']), path)
        issue = read(data / f'issues/{date}.json')
        for toc, row in zip(issue['toc'], issue['scanRestoration']['entries'], strict=True):
            if row.get('eligibility'):
                toc['restorationEligibility'] = row['eligibility']
        write(data, f'issues/{date}.json', issue)
    if not (data / 'cd-baseline.json').is_file():
        raise ValueError('CD preservation receipt missing; reconstruct the CD-only baseline before resuming')
    write(data, 'volunteer-inputs.json', inputs)
    manifest['volunteerInputs'] = pin(data, 'volunteer-inputs.json')
    manifest['cdBaseline'] = pin(data, 'cd-baseline.json')
    manifest['files'] = inventory(data)
    write(data, 'manifest.json', manifest)
    print('Checking complete reader inventories, projections, links and downloads', flush=True)
    counts = check(data, require_thumbnails=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    data.rename(output)
    return dict(counts=counts, pdfIssues=len(inputs['issues']), pdfArticles=len(manifest['scanInputs']),
                preservedCdArticles=read(output / 'cd-baseline.json')['manifest']['counts']['articles'], manifestSha256=digest(output / 'manifest.json'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('inventory', 'export', 'check'))
    parser.add_argument('--inputs', type=Path, default=INPUTS)
    parser.add_argument('--data', type=Path, default=ROOT / 'dist/reading-room-volunteer/data')
    parser.add_argument('--stages', type=Path, default=ROOT / 'work/reading-room/volunteer-full')
    args = parser.parse_args()
    if args.action == 'inventory':
        result = prepare_inputs(args.inputs)
    elif args.action == 'export':
        result = export(args.inputs, args.data, args.stages)
    else:
        from .check import check
        result = check(args.data, require_thumbnails=True)
    print(json.dumps(result if args.action != 'inventory' else {'issues': len(result['issues'])}, ensure_ascii=False))


if __name__ == '__main__':
    main()
