"""Inventory PDF metadata and preserve the complete provisional TOC queue."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
ISSUES = ('8311 8402 8403 8405 8406 8407 8408 8409 8410 8412 '
          '8502 8503 8510 8511 8801 9108 9109 9212 9303 9503 9507').split()
EXPECTED = dict(sources=21, pages=6615, bytes=2664455314,
                toc_issues=19, toc_entries=839, article_candidates=684)


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def pin(root, path):
    return {'path': path, 'sha256': digest(root / path),
            'bytes': (root / path).stat().st_size}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def command(args):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env={**os.environ, 'LC_ALL': 'C'}).stdout


def page_metadata(raw, count):
    """Poppler reports unrotated boxes in PDF points, bottom-left origin."""
    pages = []
    for index in range(count):
        number = index + 1
        size = re.search(rf'^Page\s+{number} size:\s+([\d.]+) x ([\d.]+) pts', raw, re.M)
        rotation = re.search(rf'^Page\s+{number} rot:\s+(-?\d+)', raw, re.M)
        if not size or not rotation:
            raise ValueError(f'Missing dimensions/rotation for PDF page {number}')
        page = dict(pdf_index=index, pdf_page=number,
                    width_pt=float(size[1]), height_pt=float(size[2]), rotation=int(rotation[1]))
        if page['rotation'] not in (0, 90, 180, 270):
            raise ValueError(f'Unsupported rotation: {page}')
        for box in ('MediaBox', 'CropBox'):
            match = re.search(rf'^Page\s+{number} {box}:\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)', raw, re.M)
            if not match:
                raise ValueError(f'Missing {box} for PDF page {number}')
            page[box] = [float(v) for v in match.groups()]
        pages.append(page)
    return pages


def text_pages(raw, count):
    parts = raw.decode('utf-8').split('\f')
    if len(parts) != count + 1 or parts[-1].strip():
        raise ValueError('pdftotext page separators do not reconcile')
    return [{'pdf_index': i, 'characters': len(text.strip()),
             'extractable_text': bool(text.strip())} for i, text in enumerate(parts[:-1])]


def load_toc(root):
    manifest_path = 'build/toc/manifest.json'
    manifest = json.loads((root / manifest_path).read_bytes())
    inputs = [pin(root, path) for path in
              ('TOC.md', 'data/identities/toc.json', manifest_path, 'schemas/toc-import.schema.json')]
    if inputs[0]['sha256'] != manifest['source']['sha256']:
        raise ValueError('Current TOC differs from structured snapshot; run make import-toc')
    if inputs[1]['sha256'] != manifest['identities_sha256']:
        raise ValueError('TOC identity ledger differs from snapshot')
    if inputs[3]['sha256'] != manifest['schema_sha256']:
        raise ValueError('TOC schema differs from snapshot')
    for name, expected in sorted(manifest['outputs'].items()):
        actual = pin(root, f'build/toc/{name}')
        if any(actual[key] != expected[key] for key in ('sha256', 'bytes')):
            raise ValueError(f'TOC snapshot changed: {name}')
        inputs.append(actual)
    issues = json.loads((root / 'build/toc/issues.json').read_bytes())
    entries = [json.loads(line) for line in (root / 'build/toc/toc-entries.jsonl').read_bytes().splitlines()]
    candidates = [json.loads(line) for line in (root / 'build/toc/article-candidates.jsonl').read_bytes().splitlines()]
    return inputs, issues, entries, candidates


def queue_for(sources, entries, candidates):
    by_issue = {s['provisional_issue_id']: s for s in sources if s['scope'] == 'toc-entries-and-cover'}
    candidate_ids = {c['toc_entry_id']: c['id'] for c in candidates}
    eligible = [e for e in entries if e['issue_id'] in by_issue]
    ids = [e['id'] for e in eligible]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate TOC identity')
    id_set = set(ids)
    queue = []
    for entry in eligible:
        if entry['parent_id'] and entry['parent_id'] not in id_set:
            raise ValueError(f'Missing parent: {entry["id"]}')
        source = by_issue[entry['issue_id']]
        queue.append(dict(toc_entry_id=entry['id'], source_id=source['id'],
                          issue_id=entry['issue_id'], toc_entry=entry,
                          provisional_article_id=candidate_ids.get(entry['id']),
                          classification={'status': 'unresolved', 'decision': None, 'evidence': []},
                          location={'status': 'not-mapped', 'regions': []}))
    return queue


def inventory(root=ROOT, output=None):
    root = Path(root).resolve()
    output = Path(output or root / 'private/pdf-restoration/inventory').resolve()
    if not output.is_relative_to(root / 'private') and not output.is_relative_to(root / 'build'):
        raise ValueError('Generated evidence must live under private/ or build/')
    if output.exists():
        raise ValueError(f'Output already exists; use a separate --output to verify reproducibility: {output}')
    paths = sorted((root / 'maso-pdf').glob('*.pdf'))
    if [p.name for p in paths] != [f'maso-{label}.pdf' for label in ISSUES]:
        raise ValueError('Supplied PDF set differs from PLAN-PDF.md; review inputs before proceeding')
    inputs, issues, entries, candidates = load_toc(root)
    issue_ids = {issue['id'] for issue in issues}
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent, prefix='.inventory-') as temporary:
        stage = Path(temporary) / 'inventory'
        stage.mkdir()
        versions = {}
        for tool in ('pdfinfo', 'pdftotext'):
            result = subprocess.run([tool, '-v'], capture_output=True, check=True)
            versions[tool] = (result.stdout + result.stderr).decode().splitlines()[0]
        sources = []
        for path in paths:
            label = path.stem.removeprefix('maso-')
            identifier = f'pdf-maso-{label}'
            issue_id = f'maso-19{label[:2]}-{label[2:]}'
            before = pin(root, path.relative_to(root).as_posix())
            summary = command(['pdfinfo', str(path)]).decode()
            count = int(re.search(r'^Pages:\s+(\d+)', summary, re.M)[1])
            info = command(['pdfinfo', '-box', '-f', '1', '-l', str(count), str(path)])
            raw_text = command(['pdftotext', '-layout', '-enc', 'UTF-8', str(path), '-'])
            pages = page_metadata(info.decode(), count)
            text = text_pages(raw_text, count)
            for page, layer in zip(pages, text):
                page['text_layer'] = layer
            if before != pin(root, path.relative_to(root).as_posix()):
                raise ValueError(f'Source changed while reading: {path.name}')
            evidence = stage / 'evidence' / identifier
            evidence.mkdir(parents=True)
            (evidence / 'pdfinfo.txt').write_bytes(info)
            (evidence / 'text-layer.txt').write_bytes(raw_text)
            sources.append(dict(id=identifier, **before, filename_issue_label=label,
                                provisional_issue_id=issue_id if issue_id in issue_ids else None,
                                identity_status='filename-only-unverified',
                                identity_conflicts=[] if issue_id in issue_ids or label in ('9503', '9507')
                                else ['filename-has-no-toc-issue'],
                                scope='cover-only' if label in ('9503', '9507') else 'toc-entries-and-cover',
                                page_count=count, pages=pages,
                                text_layer_status='some-extractable-text' if any(t['extractable_text'] for t in text)
                                else 'no-extractable-text',
                                evidence=[pin(stage, f'evidence/{identifier}/{name}')
                                          for name in ('pdfinfo.txt', 'text-layer.txt')]))
            print(f'{identifier}: {count} pages; {sources[-1]["text_layer_status"]}', flush=True)
        queue = queue_for(sources, entries, candidates)
        totals = dict(sources=len(sources), pages=sum(s['page_count'] for s in sources),
                      bytes=sum(s['bytes'] for s in sources), toc_issues=len({q['issue_id'] for q in queue}),
                      toc_entries=len(queue), article_candidates=sum(q['provisional_article_id'] is not None for q in queue))
        if totals != EXPECTED:
            raise ValueError(f'Plan counts differ; review input correction: {totals}')
        november = [q for q in queue if q['issue_id'] == 'maso-1983-11']
        if len(november) != 47 or sum(q['provisional_article_id'] is not None for q in november) != 35:
            raise ValueError('November queue does not reconcile')
        write_json(stage / 'sources.json', dict(schema_version=1, inputs=inputs, tools=versions,
                   coordinate_convention={'pdf_index': 'zero-based', 'pdf_page': 'one-based',
                                          'printed_page': 'not inferred', 'box_units': 'PDF points',
                                          'box_origin': 'bottom-left, before page rotation'}, sources=sources))
        (stage / 'queue.jsonl').write_text(''.join(json.dumps(q, ensure_ascii=False, sort_keys=True) + '\n'
                                                for q in queue), encoding='utf-8')
        per_issue = []
        for issue_id in sorted({q['issue_id'] for q in queue}):
            rows = [q for q in queue if q['issue_id'] == issue_id]
            per_issue.append(dict(issue_id=issue_id, entries=len(rows),
                                  article_candidates=sum(q['provisional_article_id'] is not None for q in rows),
                                  provisional_kinds=dict(Counter(q['toc_entry']['kind_candidate'] for q in rows)),
                                  page_less=sum(not q['toc_entry']['page_candidates'] for q in rows)))
        write_json(stage / 'report.json', dict(checkpoint='1', status='complete', totals=totals,
                   issues=per_issue, covers_only=[s['id'] for s in sources if s['scope'] == 'cover-only'],
                   artifacts=[pin(stage, name) for name in ('sources.json', 'queue.jsonl')],
                   limits=['No article boundaries investigated.', 'All source identities require visual verification.',
                           'All article/heading decisions remain unresolved.',
                           'Extractable text is metadata evidence, not OCR quality or restoration coverage.']))
        # Recheck small upstream inputs before publishing the complete checkpoint.
        for record in inputs:
            if pin(root, record['path']) != record:
                raise ValueError('TOC inputs changed during inventory')
        stage.rename(output)
    return totals


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    print(json.dumps(inventory(output=args.output), indent=2))


if __name__ == '__main__':
    main()
