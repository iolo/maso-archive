"""Consume hash-pinned, closed restoration snapshots without rerunning restoration.

The closeout already checked native/assembly reconstruction. Reader builds verify
the complete frozen inventory, package schema, resource pins and ownership, then
check every reader projection against those bytes. No private adapter is executed.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path

from tools.pdf_restore.build import package_pins
from tools.pdf_restore.package import validate_package
from .export import digest, read, safe


def check_inputs(root, manifest):
    """Bind published outcomes/packages to the selected original closeout inputs."""
    source = manifest.get('volunteerInputs')
    if source is None:
        raise ValueError('Frozen reader has no selected-input receipt')
    path = safe(root, source['path'])
    if path.stat().st_size != source['bytes'] or digest(path) != source['sha256']:
        raise ValueError('Frozen selected-input receipt changed')
    inputs = read(path)
    specs = {s['issueId']: s for s in inputs['issues']}
    rows = manifest['frozenIssues']
    if len(specs) != len(inputs['issues']) or set(specs) != {r['issueId'] for r in rows}:
        raise ValueError('Frozen issue selection differs')
    files = {r['path']: r for r in manifest['files']}
    scan_inputs = {r['articleId']: r for r in manifest['scanInputs']}
    reports, expected_scan_ids = {}, set()
    for row in rows:
        spec = specs[row['issueId']]
        if row['input'] != spec:
            raise ValueError('Frozen issue input differs from selection')
        date = row['issueId'].removeprefix('maso-')
        prefix = f'source/pdf-issues/{date}'
        if 'manifest' in spec:
            original_path = root / prefix / 'manifest.json'
            if digest(original_path) != spec['manifest']['sha256']:
                raise ValueError('Frozen standalone manifest differs')
            original = read(original_path)
            for file in original['files']:
                expected = dict(file, path=f'{prefix}/{file["path"]}')
                if files.get(expected['path']) != expected:
                    raise ValueError('Frozen standalone file differs from selected inventory')
            reports[row['issueId']] = read(root / prefix / 'accounting.json')
            selected = read(root / prefix / 'issue.json')['articles']
            packages = [(r['articleId'], r['manifest']['sha256'], f'pdf-issues/{date}/{r["path"]}') for r in selected]
        else:
            ledger_path = root / prefix / 'ledger.json'
            if digest(ledger_path) != spec['ledger']['sha256']:
                raise ValueError('Frozen legacy ledger differs')
            packages = [(r['articleId'], r['manifest']['sha256'], f'pdf/{r["articleId"]}/article.json') for r in spec['packages']]
            # The report is recomputed after package validation in the checker.
            reports[row['issueId']] = read(ledger_path)
        for article, sha, package_path in packages:
            if article in expected_scan_ids or scan_inputs.get(article) != dict(articleId=article, manifestSha256=sha, packagePath=package_path):
                raise ValueError('Frozen selected article input differs')
            expected_scan_ids.add(article)
        changes = {k: v for k, v in inputs['canonicalTitleChanges'].items() if k.startswith(row['issueId'] + '-toc-')}
        if row['canonicalTitleChanges'] != changes:
            raise ValueError('Frozen canonical title mappings differ')
    if expected_scan_ids != set(scan_inputs):
        raise ValueError('Frozen selected article coverage differs')
    baseline = manifest.get('cdBaseline')
    if baseline:
        path = safe(root, baseline['path'])
        if path.stat().st_size != baseline['bytes'] or digest(path) != baseline['sha256']:
            raise ValueError('CD baseline receipt differs')
        cd = read(path)
        mutable = {'catalog.json', 'search.json', 'manifest.json'} | {
            f'{kind}/{id.removeprefix("maso-")}.json' for id in specs for kind in ('issues', 'media')}
        for row in cd['manifest']['files']:
            if row['path'] not in mutable and files.get(row['path']) != row:
                raise ValueError('Existing CD reader file changed')
        links = {}
        for issue in read(root / 'catalog.json')['issues']:
            doc = read(root / f'issues/{issue["id"].removeprefix("maso-")}.json')
            links.update({r['id']: [id for id in r['articleIds'] if not id.startswith('scan-')] for r in doc['toc']})
        if links != cd['tocLinks']:
            raise ValueError('Existing CD TOC associations changed')
    return reports


def expected_report(original, issue, packages, title_changes):
    if 'issue_id' in original:
        from tools.pdf_restore.issue import accounting
        original = accounting(original, issue['toc'], packages)
    report = deepcopy(original)
    for row in report['entries']:
        change = title_changes.get(row['id'])
        if change:
            if row['title'] != change['before']:
                raise ValueError('Frozen canonical title source differs')
            row.update(sourceTitle=row['title'], title=change['after'])
    return report


def check_package(folder, expected_sha256):
    folder = Path(folder)
    if digest(folder / 'manifest.json') != expected_sha256:
        raise ValueError('Frozen package manifest differs from selected closeout')
    records = read(folder / 'manifest.json')['files']
    expected = {r['path'] for r in records}
    actual = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
    if len(expected) != len(records) or actual != expected | {'manifest.json'}:
        raise ValueError('Frozen package inventory differs')
    for row in records:
        path = safe(folder, row['path'])
        if path.stat().st_size != row['bytes'] or digest(path) != row['sha256']:
            raise ValueError(f'Frozen package bytes differ: {row["path"]}')
    package = validate_package(read(folder / 'article.json'))
    by_path = {r['path']: r for r in records}
    for row in package_pins(package):
        if by_path.get(row['path']) != row:
            raise ValueError('Frozen package resource differs from inventory')
    return package


def validate_report(issue, report, packages):
    """Preserve original outcome notes while independently checking reader ownership."""
    if report['issueId'] != issue['issue']['id'] or len(report['entries']) != len(issue['toc']):
        raise ValueError('Frozen issue identity/count differs')
    owners, groups, sections, unresolved = {}, [], [], []
    for toc, row in zip(issue['toc'], report['entries'], strict=True):
        if any(toc[k] != row[k] for k in ('id', 'parentId', 'depth', 'title', 'byline', 'page', 'kind')):
            raise ValueError(f'Frozen canonical TOC differs: {row["id"]}')
        kind = row['classification']
        if kind == 'article':
            package = packages.get(row['id'])
            if (row['bodyOwner'] is not True or package is None or
                    package['id'] != row['articleId'] or package['toc_entry_id'] != row['id'] or
                    package['issue_id'] != report['issueId'] or
                    package['availability'] != row['availability'] or
                    package['verification']['status'] != row['verification']):
                raise ValueError('Frozen article ownership/outcome differs')
            owners[row['id']] = row
        elif kind in ('group-heading', 'section-reference'):
            if row['bodyOwner'] is not False:
                raise ValueError('Frozen non-owning entry owns a body')
            (groups if kind == 'group-heading' else sections).append(row)
        elif kind == 'unresolved':
            if row['bodyOwner'] is not None or row.get('articleId') or row.get('restoration'):
                raise ValueError('Frozen unresolved entry has an invented body')
            unresolved.append(row)
        else:
            raise ValueError('Unsupported frozen classification')
        links = [row['articleId']] if row.get('articleId') else []
        scan_links = [id for id in toc['articleIds'] if id.startswith('scan-')]
        if (toc.get('restorationKind') != kind or scan_links != links or
                toc.get('sectionRef') != row.get('sectionRef') or
                toc.get('restorationEligibility') != row.get('eligibility')):
            raise ValueError('Frozen TOC ownership/link differs')
    if set(packages) != set(owners) or len({p['id'] for p in packages.values()}) != len(packages):
        raise ValueError('Duplicate or unlisted frozen body')
    for row in sections:
        owner = owners.get(row['bodyOwnerTocEntryId'])
        if owner is None or row['parentId'] != owner['id'] or row['articleId'] != owner['articleId']:
            raise ValueError('Frozen section owner differs')
        package = packages[owner['id']]
        blocks = [b for b in package['blocks'] if b['id'] == row['sectionRef']['blockId']]
        regions = {r['id']: r for r in package['regions']}
        if (row['sectionRef']['articleId'] != owner['articleId'] or len(blocks) != 1 or
                not any(regions[r]['pdf_index'] + 1 == row['sectionPdfPage'] for r in blocks[0]['region_ids'])):
            raise ValueError('Frozen section anchor/page differs')
    counts = report['counts']
    expected = dict(toc_entries=len(issue['toc']), classified_articles=len(owners),
                    group_headings=len(groups), section_references=len(sections),
                    unresolved_eligibility=sum(r.get('eligibility') != 'eligible-canonical-toc-leaf' for r in unresolved))
    for key, value in expected.items():
        if counts[key] != value:
            raise ValueError(f'Frozen outcome count differs: {key}')
    if counts.get('unresolved_body_locations', 0) != sum(r.get('eligibility') == 'eligible-canonical-toc-leaf' for r in unresolved):
        raise ValueError('Frozen unlocated-body count differs')
    for key, field in [('restoration_availability', 'availability'), ('verification', 'verification')]:
        actual = Counter(r[field] for r in owners.values())
        if +Counter(counts[key]) != actual:
            raise ValueError(f'Frozen {key} counts differ')
    if issue.get('scanRestoration') != report:
        raise ValueError('Frozen issue report differs')
