"""Audit collection coverage, checkpoint provenance and current scan bytes.

Run from the repository root: python3 -m tools.scan_collection_audit
Per-issue cleanup already reads every ZIP entry and fully decodes each master.
This closeout pass checks the collection together and hashes every ZIP and master
again. It writes a new audit record and refuses an existing destination.
"""

import argparse
from collections import Counter
import csv
import hashlib
import json
import re
import subprocess
from zipfile import ZipFile

from tools.scan_cleanup import ROOT, digest, local_path, save


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def audit(destination):
    require(not destination.exists(), f'Refusing existing audit: {destination}')
    archives = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'maso-img').glob('*.zip')}
    issues = set()
    for name in archives:
        match = re.search(r'_(\d{4})_(\d{2})', name)
        require(match is not None, f'Unrecognized archive date: {name}')
        issues.add(f'{match[1]}-{match[2]}')
    catalog = ROOT / 'metadata/catalog/scans'
    records = {r['issue']: (p, r) for p in catalog.glob('*-result.json') for r in [read(p)]}
    require(set(records) == issues, 'Result issues do not match donated issues')
    require({p.name[:-12] for p in catalog.glob('*-recipe.json')} == issues,
            'Recipe issues do not match donated issues')
    seen_archives, global_images, totals, checkpoints = set(), set(), Counter(), []
    historical = []
    for issue in sorted(issues):
        print(f'Auditing {issue}: ZIPs, masters, metadata and commit', flush=True)
        result_path, record = records[issue]
        relative_result = result_path.relative_to(ROOT).as_posix()
        commit = git('log', '--diff-filter=A', '--format=%H', '--', relative_result).decode().strip()
        require(len(commit) == 40, f'Missing unique issue checkpoint: {issue}')
        committed_paths = git('diff-tree', '--root', '--no-commit-id', '--name-only', '-r', commit).decode().splitlines()
        require('PROGRESS-SCANS.md' in committed_paths, f'No progress update in {issue} commit')
        root = local_path(record['output'])
        manifest = read(root / 'manifest.json')
        review = read(root / 'review.json')
        validation = record['validation']
        summary = manifest['summary']
        require(record['issue'] == manifest['issue'] == review['issue'] == issue,
                f'Issue identity mismatch: {issue}')
        require(record['summary'] == summary, f'Result summary mismatch: {issue}')
        require(validation['result'] == 'passed' and validation['originalZipHashesUnchanged'],
                f'Issue verification did not pass: {issue}')
        require(digest(root / 'manifest.json') == validation['manifestSha256'] == review['manifestSha256'],
                f'Manifest fingerprint mismatch: {issue}')
        require(read(root / 'review/verification.json') == validation, f'Verification record mismatch: {issue}')
        require(digest(local_path(manifest['recipe'])) == manifest['recipeSha256'],
                f'Recipe fingerprint mismatch: {issue}')
        require(manifest['sources'] == record['sourceArchives'], f'Source mapping mismatch: {issue}')
        expected_entries = set()
        for source in manifest['sources']:
            name = source['path']
            require(name in archives and name not in seen_archives, f'Archive coverage overlap: {name}')
            seen_archives.add(name)
            path = local_path(name)
            require(path.stat().st_size == source['bytes'], f'ZIP size changed: {name}')
            require(digest(path) == source['sha256'] == source['sha256After'], f'ZIP bytes changed: {name}')
            totals['sourceArchiveBytes'] += source['bytes']
            with ZipFile(path) as zipped:
                for index, entry in enumerate(zipped.infolist()):
                    if not entry.is_dir():
                        expected_entries.add((name, index, entry.filename, entry.file_size, f'{entry.CRC:08x}'))
        origins = [o for image in manifest['images'] for o in image['originals']]
        origins += manifest['notes'] + manifest['omittedSidecars']
        recorded_entries = [(o['archive'], o['entryIndex'], o['member'], o['bytes'], o['crc32']) for o in origins]
        require(len(recorded_entries) == len(set(recorded_entries)) == summary['entries'],
                f'Duplicate or missing provenance entry: {issue}')
        require(set(recorded_entries) == expected_entries, f'ZIP entry inventory mismatch: {issue}')
        images = {r['path']: r for r in manifest['images']}
        actual_images = {p.relative_to(root).as_posix() for folder in ['pages', 'covers', 'extras']
                         for p in (root / folder).rglob('*') if p.is_file()}
        require(actual_images == set(images), f'Working image inventory mismatch: {issue}')
        hashes = {r['sha256'] for r in images.values()}
        require(len(hashes) == len(images) == summary['decodedImages'] == summary['uniqueImages'],
                f'Image deduplication/decode accounting mismatch: {issue}')
        require(not hashes & global_images, f'Unexpected image shared between issues: {issue}')
        global_images.update(hashes)
        for row in images.values():
            path = root / row['path']
            require(path.stat().st_size == row['bytes'] and digest(path) == row['sha256'],
                    f'Master bytes changed: {issue}/{row["path"]}')
            require(all(o['sha256'] == row['sha256'] for o in row['originals']),
                    f'Image/source hash mismatch: {issue}/{row["path"]}')
        for row in manifest['notes'] + manifest['contactSheets']:
            require(digest(root / row['path']) == row['sha256'], f'Note/preview bytes changed: {issue}')
        require(Counter(p for sheet in manifest['contactSheets'] for p in sheet['images']) == Counter(images.keys()),
                f'Contact sheet coverage mismatch: {issue}')
        for row in review['printedPageSamples'] + review['roleOverrides'] + review.get('readingOrderOverrides', []):
            require(row['sha256'] == images[row['path']]['sha256'], f'Review image fingerprint mismatch: {issue}')
            if 'evidence' in row:
                require((root / row['evidence']).is_file(), f'Missing review evidence: {issue}')
        printed = {r['path']: r['printedPage'] for r in review['printedPageSamples']}
        roles = {r['path']: r['role'] for r in review['roleOverrides']}
        orders = {r['path']: r['readingOrder'] for r in review.get('readingOrderOverrides', [])}
        rows = list(csv.DictReader((root / 'page-list.csv').open(encoding='utf-8', newline='')))
        require(len(rows) == len(images) and {r['working_file'] for r in rows} == set(images),
                f'Page list inventory mismatch: {issue}')
        for row in rows:
            original = images[row['working_file']]
            require(row['sha256'] == original['sha256']
                    and row['reading_order'] == str(orders.get(original['path'], original['readingOrder']) or '')
                    and row['verified_printed_page'] == str(printed.get(original['path'], ''))
                    and row['role'] == roles.get(original['path'], original['role']),
                    f'Page/review mapping mismatch: {issue}/{original["path"]}')
        require(sorted(int(r['reading_order']) for r in rows if r['reading_order']) ==
                list(range(1, summary['orderedImages'] + 1)), f'Reading order loses/repeats a slot: {issue}')
        for artifact in record['artifacts']:
            path = local_path(artifact['path'])
            if digest(path) != artifact['sha256']:
                blob = git('show', f'{commit}:{artifact["path"]}')
                require(hashlib.sha256(blob).hexdigest() == artifact['sha256'],
                        f'Artifact differs from current and checkpoint bytes: {artifact["path"]}')
                historical.append(dict(issue=issue, path=artifact['path'], checkpoint=commit))
        totals.update({key: value for key, value in summary.items() if isinstance(value, int)})
        checkpoints.append(dict(issue=issue, commit=commit, result=relative_result,
                                resultSha256=digest(result_path), manifestSha256=validation['manifestSha256']))
    require(seen_archives == archives, 'Donation archives remain unaccounted for')
    # Only numeric counters are accumulated; filename ranges/gaps are issue-specific.
    result = dict(schemaVersion=1, completedOn='2026-11-14', result='passed',
                  checks=['Every donated issue has a committed recipe, result and progress update.',
                          'Every source ZIP is covered exactly once; current ZIP SHA-256 matches extraction.',
                          'Every non-directory ZIP member has exactly one provenance mapping.',
                          'Every retained master, note, contact sheet and issue artifact has checked hashes.',
                          'Historical shared-tool/document hashes match the relevant issue commit.',
                          'Every page-list row agrees with the extraction and visual review mappings.',
                          'Each reviewed reading order retains every ordered slot exactly once.'],
                  totals=dict(issues=len(issues), archives=len(archives), **totals),
                  checkpoints=checkpoints, historicalSharedArtifacts=historical,
                  limitations=['Visual review covered all contact-sheet images plus selected enlarged views.',
                               'Full printed pagination and physical completeness remain unverified.',
                               'ZIP-entry CRC/SHA checks and full JPEG decoding were performed per issue; '
                               'this collection pass rehashes the ZIPs and masters without repeating decoding.'])
    save(destination, result)
    print(json.dumps(dict(result='passed', totals=result['totals']), indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='metadata/catalog/scans/collection-audit.json')
    args = parser.parse_args()
    audit(local_path(args.output))


if __name__ == '__main__':
    main()
