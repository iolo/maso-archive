"""Versioned mismatch evidence; no catalog mutation or automatic corrections."""
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
import re
import unicodedata

from maso_archive.toc import parse_toc
from tools.reading_room.export import ROOT, digest, read
from .inventory import PRIVATE, fingerprint, save


def normalized(text):
    return re.sub(r'\s+', '', unicodedata.normalize('NFC', text))


def compare(index_path=PRIVATE / 'ocr-index.json', source=ROOT / 'TOC.md',
            output=PRIVATE / 'reports', reviews_path=PRIVATE / 'reviews.json',
            catalog=ROOT / 'build/toc'):
    source = Path(source)
    source_hash = digest(source)
    raw = source.read_text(encoding='utf-8')
    issues, entries, errors = parse_toc(raw, 'toc-sha256-' + source_hash)
    if errors:
        raise ValueError('TOC source cannot be compared without resolving parse errors')
    index = read(Path(index_path))
    reviews = read(Path(reviews_path)) if Path(reviews_path).exists() else dict(pages=[])
    reviewed = {r['sha256']: r for r in reviews['pages']}
    # Stable IDs are usable only when the generated import describes these bytes.
    ids, catalog_status = {}, 'missing-import'
    if (Path(catalog) / 'manifest.json').exists():
        manifest = read(Path(catalog) / 'manifest.json')
        catalog_status = 'current' if manifest['source']['sha256'] == source_hash else 'stale-import'
        if manifest['source']['sha256'] == source_hash:
            import json
            for line in (Path(catalog) / 'toc-entries.jsonl').read_text().splitlines():
                entry = json.loads(line)
                ids[entry['source']['line_start']] = entry['id']
    by_issue = defaultdict(list)
    for entry in entries:
        by_issue[entry['issue_id']].append(entry)
    scans = defaultdict(list)
    for row in index['pages']:
        evidence = read(Path(row['evidence']))
        if evidence['settings']['sourceSha256'] != row['sha256']:
            raise ValueError('OCR index/evidence source differs')
        scans[row['date']].append((dict(row, evidenceSha256=digest(Path(row['evidence']))), evidence))
    reports = []
    for date in sorted(set(scans) | {i['id'][7:9] + i['id'][10:12] for i in issues}):
        issue_id = f'maso-19{date[:2]}-{date[2:]}'
        pages = sorted(scans.get(date, []), key=lambda pair: pair[0]['sequence'])
        candidates = []
        for row, evidence in pages:
            for n, line in enumerate(evidence['lines']):
                # Adjacent line candidates handle titles wrapped by OCR. These
                # remain suggestions, never identity or association decisions.
                for count in range(1, 4):
                    selected = evidence['lines'][n:n+count]
                    if len(selected) != count or len({l['region'] for l in selected}) != 1:
                        continue
                    candidates.append(dict(image=row['name'], region=selected[0]['region'],
                        bbox=[min(l['bbox'][0] for l in selected), min(l['bbox'][1] for l in selected),
                              max(l['bbox'][2] for l in selected), max(l['bbox'][3] for l in selected)],
                        text=' '.join(l['text'] for l in selected), confidence=min(l['confidence'] for l in selected)))
        differences = []
        for entry in by_issue[issue_id]:
            title = normalized(entry['title_candidate'])
            def score(candidate):
                text = normalized(candidate['text'])
                return 1.0 if title and title in text else SequenceMatcher(None, title, text).ratio()
            match = max(candidates, key=score) if candidates else None
            exact = bool(match and title and title in normalized(match['text']))
            differences.append(dict(line=entry['source']['line_start'], id=ids.get(entry['source']['line_start']),
                catalogText=entry['raw_text'], title=entry['title_candidate'],
                contributor=entry.get('byline_candidate'), page=entry.get('start_page_candidate'),
                parentLine=entries[entry['_parent']]['source']['line_start'] if entry['_parent'] is not None else None,
                depth=entry.get('depth'),
                status='title-located-fields-need-review' if exact else 'possible-difference' if match else 'no-scan-evidence',
                suggestion=match, similarity=round(score(match), 3) if match else None))
        page_reports = []
        for row, evidence in pages:
            review = reviewed.get(row['sha256'], {}).get('comparison')
            if not review:
                review = dict(status='pending', note='Visual comparison not yet recorded')
            elif review.get('sourceSha256') != source_hash or review.get('evidenceSha256') != row['evidenceSha256']:
                review = dict(status='stale', note='Catalog or OCR evidence changed since visual comparison', previous=review)
            page_reports.append(dict(row, dimensions=evidence['dimensions'], lines=evidence['lines'], review=review))
        reports.append(dict(date=f'19{date[:2]}-{date[2:]}', issueId=issue_id,
            coverage='catalog-and-images' if differences and pages else 'image-only' if pages else 'catalog-only',
            entries=differences, pages=page_reports))
    result = dict(source=dict(path='TOC.md', sha256=source_hash), catalogStatus=catalog_status, issues=reports,
                  note='OCR suggestions are not corrections. All lines retained for omission, hierarchy and order review.')
    result['summary'] = dict(pages=sum(len(i['pages']) for i in reports),
                             coverage=dict(Counter(i['coverage'] for i in reports)),
                             entries=dict(Counter(e['status'] for i in reports for e in i['entries'])),
                             reviews=dict(Counter(p['review']['status'] for i in reports for p in i['pages'])))
    key = fingerprint([source_hash, index, reviews, [p['evidenceSha256'] for issue in reports for p in issue['pages']]])
    destination = Path(output) / key
    destination.mkdir(parents=True, exist_ok=True)
    save(destination / 'report.json', result)
    text = ['# Donated TOC comparison', '', f'TOC.md SHA-256: `{source_hash}`', '',
            'Catalog text is authoritative. OCR candidates require visual review; no catalog files were changed.', '',
            f'Imported catalog status: {catalog_status}. A stale import needs separate manual catalog migration; this command never reimports.', '']
    text += [f'Summary: {result["summary"]}', '']
    for issue in reports:
        text += [f'## {issue["date"]} — {issue["coverage"]}', '']
        for page in issue['pages']:
            text += [f'- {page["name"]}: {page["review"]["status"]} — {page["review"]["note"]}']
            for finding in page['review'].get('findings', []):
                text += [f'  - Visual finding: {finding}']
        for entry in issue['entries']:
            candidate = entry['suggestion']
            text += ['', f'### TOC.md:{entry["line"]} ({entry["id"] or "ID unavailable for this source version"})',
                     f'Catalog: {entry["catalogText"]}', f'Status: {entry["status"]}']
            if candidate:
                text += [f'OCR: {candidate["text"]}', f'Evidence: {candidate["image"]}, region {candidate["region"]}, OCR pixel box {candidate["bbox"]}']
        text += ['', '### Complete OCR (including unassigned/image-only text)', '']
        for page in issue['pages']:
            text += [f'#### {page["name"]}', '```text', *[l['text'] for l in page['lines']], '```', '']
    (destination / 'report.md').write_text('\n'.join(text), encoding='utf-8')
    if digest(source) != source_hash:
        raise ValueError('TOC.md changed during comparison; previous report preserved, rerun against new source')
    save(Path(output) / 'latest.json', dict(path=str(destination), sourceSha256=source_hash))
    return destination
