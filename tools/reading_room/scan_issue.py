"""Stage a reconciled scan issue alongside an unchanged CD reader baseline."""
import argparse
from copy import deepcopy
from pathlib import Path
import shutil
import tempfile

from tools.pdf_restore.issue import accounting, inventory, load_inputs
from tools.pdf_restore.inventory import ROOT
from .export import digest, read, safe, text_for, write
from .scan import project


def validate_issue(root, issue, report):
    """Check issue ownership and section targets against the exported packages."""
    from tools.pdf_restore.build import check_export
    packages = {}
    for summary in issue['articles']:
        if summary.get('sourceKind') == 'scan':
            packages[summary['tocEntryId']] = check_export(safe(root / 'source', summary['referencePath']).parent)
    entries = []
    for row in report['entries']:
        entry = dict(toc_entry_id=row['id'], title=row['title'], parent_id=row['parentId'],
                     classification=row['classification'], body_owner=row['bodyOwner'], restoration=None)
        if row['bodyOwner']:
            entry['restoration'] = dict(article_id=row['articleId'], availability=row['availability'], verification=row['verification'])
        if row['classification'] == 'section-reference':
            entry.update(body_owner_toc_entry_id=row['bodyOwnerTocEntryId'],
                         section=dict(anchor=row['sectionRef']['blockId'], anchor_scope='assembled-parent', heading_pdf_page=row['sectionPdfPage']))
        entries.append(entry)
    expected = accounting(dict(issue_id=issue['issue']['id'], entries=entries, counts=report['counts']), issue['toc'], packages)
    if expected != report or issue.get('scanRestoration') != report:
        raise ValueError('Scan issue accounting differs')
    for toc, row in zip(issue['toc'], report['entries'], strict=True):
        if (toc.get('restorationKind') != row['classification'] or
                toc['articleIds'] != ([row['articleId']] if row.get('articleId') else []) or
                toc.get('sectionRef') != row.get('sectionRef')):
            raise ValueError('Scan issue TOC ownership/link differs')


def stage_issue(base, ledger_path, output, root=ROOT):
    from .check import check
    base, output = Path(base).resolve(), Path(output).resolve()
    if output.exists() or output.is_relative_to(base) or base.is_relative_to(output):
        raise ValueError('Use a separate, fresh reader output')
    check(base)
    base_sha, ledger_sha = digest(base / 'manifest.json'), digest(ledger_path)
    report, issue, packages, directories = load_inputs(ledger_path, base, root)
    if any(output.is_relative_to(d) or d.is_relative_to(output) for d in directories.values()):
        raise ValueError('Output overlaps scan input')
    # A full issue replaces no existing body or matching decision implicitly.
    if issue['articles'] or any(t['articleIds'] for t in issue['toc']):
        raise ValueError('Issue already contains reading links; reconcile before staging')
    catalog, search, manifest = (deepcopy(read(base / name)) for name in ('catalog.json', 'search.json', 'manifest.json'))
    ids = {p['id'] for p in packages.values()}
    if ids & {a['article_id'] for a in catalog['articles']}:
        raise ValueError('Scan article identity already exists')
    issue_id = report['issueId']
    date = issue_id.removeprefix('maso-')
    issue_path, media_path = f'issues/{date}.json', f'media/{date}.json'
    media = deepcopy(read(base / media_path))
    report_path = f'scan-issues/{date}.json'
    input_pins = {id: digest(d / 'manifest.json') for id, d in directories.items()}
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.scan-issue-', dir=output.parent) as temp:
        staged = Path(temp) / 'data'
        shutil.copytree(base, staged)
        scan_inputs = list(manifest.get('scanInputs', []))
        for toc in issue['toc']:
            if toc['id'] not in packages:
                continue
            package, directory = packages[toc['id']], directories[toc['id']]
            doc, paragraphs = project(package, toc)
            doc['scan']['packageSha256'] = digest(directory / 'article.json')
            summary = doc['article']
            if summary['text'] and text_for(doc['blocks']).encode() != (directory / 'article.txt').read_bytes():
                raise ValueError('Scan projection changes article text')
            destination = staged / 'source' / 'pdf' / package['id']
            if destination.exists():
                raise ValueError('Scan source destination already exists')
            shutil.copytree(directory, destination)
            write(staged / 'source', summary['paragraphsPath'], paragraphs)
            write(staged, f'articles/{package["id"]}.json', doc)
            issue['articles'].append(summary)
            catalog['articles'].append(summary)
            if {m['resource'] for m in media['items']} & set(summary['resources']):
                raise ValueError('Scan media identity collision')
            media['items'].extend(doc['media'])
            search['items'].append(dict(kind='article', id=package['id'], issueId=issue_id, title=summary['title'],
                                        byline=summary['byline'], reference=summary['reference'], status=summary['status'],
                                        sourceKind='scan', availability=summary['availability'], verification=summary['verification']))
            scan_inputs.append(dict(articleId=package['id'], manifestSha256=input_pins[toc['id']], packagePath=doc['scan']['packagePath']))
            for key, added in dict(articles=1, texts=int(bool(summary['text'])), listings=len(doc['listings']), mediaRecords=len(doc['media'])).items():
                manifest['counts'][key] += added
        for toc, row in zip(issue['toc'], report['entries'], strict=True):
            toc.update(restorationKind=row['classification'], articleIds=[row['articleId']] if row.get('articleId') else [])
            if row.get('sectionRef'):
                toc['sectionRef'] = row['sectionRef']
            matches = [s for s in search['items'] if s['kind'] == 'toc' and s['id'] == toc['id']]
            if len(matches) != 1:
                raise ValueError('Canonical search TOC missing or duplicated')
            matches[0].update(articleIds=toc['articleIds'], status='linked' if toc['articleIds'] else row['classification'])
        issue.update(schemaVersion=3, scanRestoration=report)
        issue['issue'].update(articleCount=len(issue['articles']), textCount=sum(bool(a['text']) for a in issue['articles']))
        catalog.update(schemaVersion=3, issues=[issue['issue'] if i['id'] == issue_id else i for i in catalog['issues']])
        media['schemaVersion'] = search['schemaVersion'] = 3
        for name, value in [(issue_path, issue), (media_path, media), ('catalog.json', catalog), ('search.json', search), (report_path, report)]:
            write(staged, name, value)
        manifest.update(schemaVersion=3, baseManifestSha256=base_sha, scanInputs=scan_inputs,
                        scanIssues=manifest.get('scanIssues', []) + [dict(issueId=issue_id, path=report_path, sha256=digest(staged / report_path), ledgerSha256=ledger_sha)])
        manifest['files'] = inventory(staged)
        write(staged, 'manifest.json', manifest)
        check(staged)
        changed = {'catalog.json', 'manifest.json', 'search.json', issue_path, media_path}
        for record in read(base / 'manifest.json')['files']:
            if record['path'] not in changed and digest(safe(staged, record['path'])) != record['sha256']:
                raise ValueError('Existing reader file changed during issue export')
        if digest(base / 'manifest.json') != base_sha or digest(ledger_path) != ledger_sha:
            raise ValueError('Input manifest/ledger changed during export')
        for id, directory in directories.items():
            if digest(directory / 'manifest.json') != input_pins[id]:
                raise ValueError('Input package changed during export')
        staged.rename(output)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(stage_issue(args.base, args.ledger, args.output)['counts'])


if __name__ == '__main__':
    main()
