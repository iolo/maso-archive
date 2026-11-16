"""Build a standalone review reader from an unfinished JPEG restoration ledger.

This projects selected native packages without OCR or issue-closeout claims.
Unclassified identities keep their original status and have no invented body.
"""
import argparse
import json
from pathlib import Path
import shutil
import tempfile

from tools.pdf_restore.build import check_export
from tools.pdf_restore.inventory import ROOT
from tools.pdf_restore.issue import inventory
from .export import digest, read, safe, text_for, write
from .scan import project


def canonical(toc, issue_id):
    return [dict(id=e['id'], parentId=e['parent_id'], depth=e['depth'],
                 title=e['title_candidate'], byline=e['byline_candidate'],
                 page=e['start_page_candidate'], kind=e['kind_candidate'], articleIds=[])
            for e in toc if e['issue_id'] == issue_id]


def report(ledger, toc, packages):
    if ledger.get('source_type') != 'jpeg-set':
        raise ValueError('Pilot requires a JPEG-set progress ledger')
    entries = ledger['entries']
    if [e['toc_entry_id'] for e in entries] != [t['id'] for t in toc]:
        raise ValueError('Pilot differs from complete canonical TOC')
    if len({t['id'] for t in toc}) != len(toc):
        raise ValueError('Duplicate canonical identity')
    rows, owners = [], set()
    for entry, t in zip(entries, toc, strict=True):
        if entry['title'] != t['title'] or entry['parent_id'] != t['parentId']:
            raise ValueError('Canonical pilot title/parent differs')
        row = dict(id=t['id'], classification=entry['classification'], bodyOwner=entry['body_owner'])
        if entry['classification'] == 'article':
            p = packages.get(t['id'])
            if (p is None or p['toc_entry_id'] != t['id'] or p['issue_id'] != ledger['issue_id'] or
                    p['source'].get('kind') != 'jpeg-set' or entry['body_owner'] is not True or
                    entry['availability'] != p['availability'] or
                    entry['verification'] != p['verification']['status']):
                raise ValueError('Selected pilot outcome differs from native package')
            row.update(articleId=p['id'], availability=p['availability'], verification=p['verification']['status'])
            owners.add(t['id'])
        elif entry['classification'] in ('group-heading', 'unclassified'):
            expected_owner = False if entry['classification'] == 'group-heading' else None
            if entry['body_owner'] is not expected_owner or entry.get('package'):
                raise ValueError('Pending/group identity cannot own a restored body')
        else:
            raise ValueError('Unsupported pilot classification; reconcile explicitly')
        rows.append(row)
    if set(packages) != owners or len({p['id'] for p in packages.values()}) != len(packages):
        raise ValueError('Duplicate or unlisted selected package')
    counts = dict(toc_entries=len(rows), articles=len(owners),
                  group_headings=sum(e['classification'] == 'group-heading' for e in rows),
                  unclassified=sum(e['classification'] == 'unclassified' for e in rows),
                  complete=sum(e.get('availability') == 'readable' for e in rows),
                  partial=sum(e.get('availability') == 'partial' for e in rows))
    for key, expected in [('toc_entries', 'canonical_identities'), ('group_headings', 'group_headings'),
                          ('unclassified', 'identitiesAwaitingDisposition'),
                          ('complete', 'readable_articles'), ('partial', 'partial_articles')]:
        if counts[key] != ledger[expected]:
            raise ValueError('Pilot counts differ from progress ledger')
    return dict(kind='jpeg-restoration-pilot', issueId=ledger['issue_id'], entries=rows, counts=counts,
                note='Review preview of selected reproducible native articles. Restoration is paused; '
                     'unclassified entries, covers/source accounting and whole-issue closeout remain pending. '
                     'Sample review does not mean full proofreading or human acceptance.')


def validate_pilot(root, record):
    """Reconcile the retained ledger/TOC and every reader link with native data."""
    root = Path(root)
    ledger = read(safe(root, record['ledgerPath']))
    if digest(safe(root, record['ledgerPath'])) != record['ledgerSha256']:
        raise ValueError('Pilot ledger pin differs')
    original = read(safe(root, record['canonicalPath']))
    if digest(safe(root, record['canonicalPath'])) != record['canonicalSha256']:
        raise ValueError('Pilot canonical pin differs')
    issue = read(root / f'issues/{record["issueId"].removeprefix("maso-")}.json')
    toc = canonical(original['entries'], record['issueId'])
    packages = {}
    for entry in ledger['entries']:
        if entry['classification'] != 'article':
            continue
        id = entry['toc_entry_id']
        summaries = [a for a in issue['articles'] if a.get('tocEntryId') == id]
        if len(summaries) != 1:
            raise ValueError('Pilot selected identity missing or duplicated')
        directory = safe(root / 'source', summaries[0]['referencePath']).parent
        if digest(directory / 'manifest.json') != entry['package']['manifest']['sha256']:
            raise ValueError('Pilot native manifest differs from selection')
        packages[id] = check_export(directory)
    expected = report(ledger, toc, packages)
    if (record['issueId'] != ledger['issue_id'] or read(safe(root, record['path'])) != expected or
            digest(safe(root, record['path'])) != record['sha256'] or issue.get('scanPilot') != expected):
        raise ValueError('Pilot report differs from selected native outcomes')
    for t, row in zip(toc, expected['entries'], strict=True):
        t.update(restorationKind=row['classification'], articleIds=[row['articleId']] if row.get('articleId') else [])
    source_issue = original['issue']
    expected_summary = dict(id=source_issue['id'], year=source_issue['year'], month=source_issue['month'],
                            label=source_issue['original_label'], articleCount=len(packages),
                            textCount=sum(any(d['path'] == 'article.txt' for d in p['downloads']) for p in packages.values()),
                            tocCount=len(toc), cover=None)
    if issue['toc'] != toc or issue['issue'] != expected_summary:
        raise ValueError('Pilot navigation changes canonical identities or ownership')
    search = read(root / 'search.json')['items']
    for t in toc:
        matches = [s for s in search if s['kind'] == 'toc' and s['id'] == t['id']]
        expected_search = dict(kind='toc', id=t['id'], issueId=record['issueId'], title=t['title'],
                               byline=t['byline'], articleIds=t['articleIds'],
                               status='linked' if t['articleIds'] else t['restorationKind'])
        if matches != [expected_search]:
            raise ValueError('Pilot search changes canonical outcome')
    return expected['counts']


def export(ledger_path, toc_dir, output, root=ROOT):
    from .check import check
    root, ledger_path, toc_dir, output = map(lambda p: Path(p).resolve(), (root, ledger_path, toc_dir, output))
    if output.exists():
        raise ValueError('Use a fresh pilot output')
    ledger = read(ledger_path)
    issue_id = ledger['issue_id']
    original_issue = next(i for i in read(toc_dir / 'issues.json') if i['id'] == issue_id)
    entries = [json.loads(line) for line in (toc_dir / 'toc-entries.jsonl').read_text().splitlines()]
    entries = [e for e in entries if e['issue_id'] == issue_id]
    toc = canonical(entries, issue_id)
    packages, directories, pins = {}, {}, {}
    for entry in ledger['entries']:
        if entry['classification'] != 'article':
            continue
        directory = safe(root, entry['package']['path'])
        pin = entry['package']['manifest']
        if safe(root, pin['path']) != directory / 'manifest.json' or digest(directory / 'manifest.json') != pin['sha256']:
            raise ValueError('Selected native manifest differs')
        if (output.is_relative_to(directory) or directory.is_relative_to(output) or
                ledger_path.is_relative_to(output) or toc_dir.is_relative_to(output)):
            raise ValueError('Pilot output overlaps preserved inputs')
        id = entry['toc_entry_id']
        packages[id], directories[id], pins[id] = check_export(directory), directory, digest(directory / 'manifest.json')
    outcome = report(ledger, toc, packages)
    initial = {p: digest(p) for p in [ledger_path, toc_dir / 'issues.json', toc_dir / 'toc-entries.jsonl']}
    needed = sum(p.stat().st_size for d in directories.values() for p in d.rglob('*') if p.is_file())
    output.parent.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(output.parent).free < needed + 256 * 1024 * 1024:
        raise ValueError('Insufficient space for a separate pilot copy')
    with tempfile.TemporaryDirectory(prefix='.jpeg-pilot-', dir=output.parent) as temp:
        staged = Path(temp) / 'data'
        staged.mkdir()
        articles, media, search, scan_inputs = [], [], [], []
        for t, row in zip(toc, outcome['entries'], strict=True):
            t.update(restorationKind=row['classification'], articleIds=[row['articleId']] if row.get('articleId') else [])
            search.append(dict(kind='toc', id=t['id'], issueId=issue_id, title=t['title'], byline=t['byline'],
                               articleIds=t['articleIds'], status='linked' if t['articleIds'] else row['classification']))
            if t['id'] not in packages:
                continue
            p, directory = packages[t['id']], directories[t['id']]
            doc, paragraphs = project(p, t)
            doc['scan']['packageSha256'] = digest(directory / 'article.json')
            summary = doc['article']
            if summary['text'] and text_for(doc['blocks']).encode() != (directory / 'article.txt').read_bytes():
                raise ValueError('Pilot projection changes native article text')
            shutil.copytree(directory, staged / 'source/pdf' / p['id'])
            write(staged / 'source', summary['paragraphsPath'], paragraphs)
            write(staged, f'articles/{p["id"]}.json', doc)
            articles.append(summary)
            media.extend(doc['media'])
            search.append(dict(kind='article', id=p['id'], issueId=issue_id, title=summary['title'], byline=summary['byline'],
                               reference=summary['reference'], status=summary['status'], sourceKind='scan',
                               availability=summary['availability'], verification=summary['verification']))
            scan_inputs.append(dict(articleId=p['id'], packagePath=summary['referencePath'], manifestSha256=pins[t['id']]))
        summary = dict(id=issue_id, year=original_issue['year'], month=original_issue['month'], label=original_issue['original_label'],
                       articleCount=len(articles), textCount=sum(bool(a['text']) for a in articles), tocCount=len(toc), cover=None)
        date = issue_id.removeprefix('maso-')
        write(staged, 'catalog.json', dict(schemaVersion=3, issues=[summary], articles=articles))
        write(staged, f'issues/{date}.json', dict(schemaVersion=3, issue=summary, toc=toc, articles=articles, scanPilot=outcome))
        write(staged, f'media/{date}.json', dict(schemaVersion=3, issueId=issue_id, items=media))
        write(staged, 'search.json', dict(schemaVersion=3, items=search))
        report_path, ledger_copy, canonical_path = 'pilot/report.json', 'pilot/ledger.json', 'pilot/canonical.json'
        write(staged, report_path, outcome)
        shutil.copyfile(ledger_path, staged / ledger_copy)
        write(staged, canonical_path, dict(issue=original_issue, entries=entries))
        record = dict(issueId=issue_id, path=report_path, sha256=digest(staged / report_path),
                      ledgerPath=ledger_copy, ledgerSha256=digest(staged / ledger_copy),
                      canonicalPath=canonical_path, canonicalSha256=digest(staged / canonical_path))
        counts = dict(issues=1, articles=len(articles), texts=summary['textCount'], tocEntries=len(toc),
                      listings=sum(a['listings'] for a in articles), mediaRecords=len(media), covers=0)
        write(staged, 'manifest.json', dict(kind='reading-room-static', schemaVersion=3, counts=counts,
                                           scanInputs=scan_inputs, pilotIssues=[record], files=inventory(staged)))
        check(staged)
        if any(digest(p) != sha for p, sha in initial.items()) or any(digest(d / 'manifest.json') != pins[id] for id, d in directories.items()):
            raise ValueError('Pilot inputs changed during export')
        staged.rename(output)
    return dict(counts=counts, pilot=outcome['counts'], bytes=needed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--toc', type=Path, default=Path('archive/toc/current'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(export(args.ledger, args.toc, args.output))


if __name__ == '__main__':
    main()
