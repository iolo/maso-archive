"""Portable issue reference from a reconciled TOC ledger and immutable packages."""
import argparse
from copy import deepcopy
import re
from pathlib import Path
import shutil
import tempfile

from tools.reading_room.export import digest, read, safe, write
from tools.reference.export import esc, page
from .build import checked, check_export
from .inventory import ROOT
from .preview import CSS, EXTRA_CSS, render_preview


AVAILABILITY = ('readable', 'partial', 'image-only', 'failed', 'unresolved')
VERIFICATION = ('unreviewed', 'sample-reviewed', 'fully-reviewed')


def accounting(ledger, toc, packages):
    """Verify ownership against the complete canonical TOC, not a candidate list."""
    entries = ledger['entries']
    if ([r['toc_entry_id'] for r in entries] != [r['id'] for r in toc] or
            len({r['id'] for r in toc}) != len(toc)):
        raise ValueError('Issue ledger differs from complete canonical TOC')
    rows, owners = [], {}
    for entry, canonical in zip(entries, toc, strict=True):
        if entry['title'] != canonical['title'] or entry['parent_id'] != canonical['parentId']:
            raise ValueError('Canonical TOC title/parent differs')
        row = {k: deepcopy(canonical[k]) for k in ('id', 'parentId', 'depth', 'title', 'byline', 'page', 'kind')}
        kind = entry['classification']
        row.update(classification=kind, bodyOwner=entry['body_owner'])
        if kind == 'article':
            package = packages.get(entry['toc_entry_id'])
            restoration = entry['restoration']
            if (entry['body_owner'] is not True or package is None or
                    package['issue_id'] != ledger['issue_id'] or package['toc_entry_id'] != row['id'] or
                    restoration['article_id'] != package['id'] or
                    restoration['availability'] != package['availability'] or
                    restoration['verification'] != package['verification']['status']):
                raise ValueError('Article outcome differs from package')
            row.update(articleId=package['id'], availability=package['availability'],
                       verification=package['verification']['status'])
            owners[row['id']] = row
        elif kind in ('group-heading', 'section-reference'):
            if entry['body_owner'] is not False or entry.get('restoration') is not None:
                raise ValueError('Non-owning TOC entry has a duplicate body')
        else:
            raise ValueError('Unresolved issue eligibility')
        rows.append(row)
    if set(packages) != set(owners) or len({p['id'] for p in packages.values()}) != len(packages):
        raise ValueError('Duplicate or unlisted article package')
    for entry, row in zip(entries, rows, strict=True):
        if row['classification'] != 'section-reference':
            continue
        owner = owners.get(entry.get('body_owner_toc_entry_id'))
        if owner is None or row['parentId'] != owner['id']:
            raise ValueError('Section reference has no parent body')
        section = entry['section']
        package = packages[owner['id']]
        blocks = [b for b in package['blocks'] if b['id'] == section['anchor'] and b['kind'] == 'title']
        if len(blocks) != 1 or section['anchor_scope'] != 'assembled-parent':
            raise ValueError('Section anchor is not an assembled heading')
        regions = {r['id']: r for r in package['regions']}
        if not any(regions[id]['pdf_index'] + 1 == section['heading_pdf_page'] for id in blocks[0]['region_ids']):
            raise ValueError('Section heading page differs')
        row.update(articleId=owner['articleId'], sectionRef=dict(articleId=owner['articleId'], blockId=section['anchor']),
                   bodyOwnerTocEntryId=owner['id'], sectionPdfPage=section['heading_pdf_page'],
                   availability=owner['availability'], verification=owner['verification'])
    counts = dict(toc_entries=len(rows), classified_articles=len(owners),
                  group_headings=sum(r['classification'] == 'group-heading' for r in rows),
                  section_references=sum(r['classification'] == 'section-reference' for r in rows),
                  unresolved_eligibility=0,
                  restoration_availability={s: sum(r['availability'] == s for r in owners.values()) for s in AVAILABILITY},
                  verification={s: sum(r['verification'] == s for r in owners.values()) for s in VERIFICATION})
    expected = deepcopy(ledger['counts'])
    expected['verification'] = {s: expected['verification'].get(s, 0) for s in VERIFICATION}
    if expected != counts:
        raise ValueError('Issue counts differ from verified ownership/outcomes')
    return dict(issueId=ledger['issue_id'], entries=rows, counts=counts,
                reviewNote='Availability and review are separate. Scan-linked uncertainties and deferred manual bitmap corrections remain in each article; readable does not certify character-perfect or executable code.')


def load_inputs(ledger_path, base, root=ROOT):
    ledger = read(ledger_path)
    issue = read(Path(base) / f'issues/{ledger["issue_id"].removeprefix("maso-")}.json')
    packages, directories = {}, {}
    for entry in ledger['entries']:
        if entry['classification'] != 'article':
            continue
        restoration = entry['restoration']
        directory = safe(root, restoration['directory'])
        if safe(root, restoration['manifest']['path']) != directory / 'manifest.json':
            raise ValueError('Article directory differs from manifest')
        checked(root, restoration['manifest'])
        packages[entry['toc_entry_id']] = check_export(directory)
        directories[entry['toc_entry_id']] = directory
    return accounting(ledger, issue['toc'], packages), issue, packages, directories


def inventory(folder):
    return [dict(path=p.relative_to(folder).as_posix(), bytes=p.stat().st_size, sha256=digest(p))
            for p in sorted(folder.rglob('*')) if p.is_file() and p != folder / 'manifest.json']


def export(ledger_path, base, output, root=ROOT):
    output = Path(output).resolve()
    report, issue, packages, directories = load_inputs(ledger_path, base, root)
    if output.exists() or any(output.is_relative_to(d) or d.is_relative_to(output) for d in directories.values()):
        raise ValueError('Use a fresh issue output outside inputs')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.pdf-issue-', dir=output.parent) as temp:
        staged = Path(temp) / 'reference'
        staged.mkdir()
        write(staged, 'accounting.json', report)
        owners = [r for r in report['entries'] if r['bodyOwner']]
        css = CSS + EXTRA_CSS
        for number, row in enumerate(owners):
            id = row['articleId']
            shutil.copytree(directories[row['id']], staged / 'articles' / id)
            html, css = render_preview(packages[row['id']])
            html = re.sub(r'(href|src)="([^"#][^"]*)"',
                          lambda m: f'{m[1]}="../articles/{esc(id)}/{m[2]}"', html)
            links = ['<a href="../index.html">호 차례</a>']
            for index, label in ((number - 1, '이전 글'), (number + 1, '다음 글')):
                if 0 <= index < len(owners):
                    links.append(f'<a href="{esc(owners[index]["articleId"])}.html">{label}</a>')
            html = html.replace('<main>', '<main><nav aria-label="호 탐색">' + ''.join(links) + '</nav>', 1)
            target = staged / 'read' / f'{id}.html'
            target.parent.mkdir(exist_ok=True)
            target.write_text(html, encoding='utf-8')
        body = [f'<main><h1>{esc(issue["issue"]["label"])} · 마이크로소프트웨어</h1>',
                '<p>목차에 실린 글의 복원 자료입니다. 광고와 별도 미등재 자료는 포함하지 않습니다.</p>']
        cover = issue['issue'].get('cover')
        if cover:
            source = safe(Path(base), cover['path'])
            if digest(source) != cover['sha256']:
                raise ValueError('Issue cover differs')
            shutil.copyfile(source, staged / ('cover' + source.suffix))
            body.append(f'<img class="issue-cover" src="cover{esc(source.suffix)}" alt="표지">')
        counts = report['counts']
        body.extend([f'<p>차례 {counts["toc_entries"]}항목 · 본문 {counts["classified_articles"]}편 · '
                     f'묶음 제목 {counts["group_headings"]} · 절 참조 {counts["section_references"]}</p>',
                     '<section aria-label="호 복원 상태"><h2>복원 및 검토</h2>',
                     '<p>복원: ' + ' · '.join(f'{s} {n}' for s, n in counts['restoration_availability'].items()) + '</p>',
                     '<p>검토: ' + ' · '.join(f'{s} {n}' for s, n in counts['verification'].items()) + '</p>',
                     f'<p>분류 미해결 {counts["unresolved_eligibility"]}</p>',
                     '<p>읽기 가능은 문자 단위 완전 교정이나 코드 실행 검증을 뜻하지 않습니다. 판독 불확실성과 수동 비트맵 교정 대기는 각 글의 교정 기록에 남아 있습니다.</p></section>',
                     '<nav aria-label="호 차례"><h2>차례</h2><ol>'])
        for row in report['entries']:
            label = esc(row['title'])
            if row.get('articleId'):
                href = f'read/{row["articleId"]}.html'
                if row.get('sectionRef'):
                    href += '#' + row['sectionRef']['blockId']
                label = f'<a href="{esc(href)}">{label}</a> — {row["availability"]} / {row["verification"]}'
            body.append(f'<li id="{esc(row["id"])}" style="margin-left:{row["depth"]}rem">{label} '
                        f'<small>({esc(row["classification"])})</small></li>')
        body.append('</ol></nav><p><a download href="accounting.json">호 복원 기록 JSON</a></p></main>')
        (staged / 'index.html').write_text(page(issue['issue']['label'], ''.join(body), 0), encoding='utf-8')
        (staged / 'style.css').write_text(css + '\n.issue-cover{width:12rem;max-width:100%;height:auto}li{margin-block:.6rem}', encoding='utf-8')
        manifest = dict(kind='pdf-issue-reference', issueId=report['issueId'], counts=counts,
                        ledgerSha256=digest(ledger_path), files=inventory(staged))
        write(staged, 'manifest.json', manifest)
        staged.rename(output)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(export(args.ledger, args.base, args.output)['counts'])


if __name__ == '__main__':
    main()
