"""Audit 14b retries and reconcile current CD1 coverage while preserving 13d history."""
import argparse
from copy import deepcopy
from pathlib import Path
import json

from tools.batch import associations, retry_associations, association_pass, report as first_report
from tools.batch.association_pass import histogram, first_records, load_outcome
from tools.run_cd1_batch import ROOT, read_json
from tools.cd1_batch_cache import Cache, key, verify, write
from tools.recover_cd1_text import json_bytes
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from tools.validate_cd1_batch import check_topic
from tools import map_cd1_images as images
from maso_archive.reading_room_package import checked_file, file_record, load_package

RECORD = ROOT / 'data/catalog/batch-runs/cd1-association-pass.json'


def current_records(originals, retries):
    """Overlay only the intended failures; never replace a first-pass success."""
    original = {r['job_id']: r for r in originals}
    require(len(original) == len(originals), 'Duplicate first-pass job')
    require(len({r['job_id'] for r in retries}) == len(retries), 'Duplicate retry job')
    for record in retries:
        require(record['job_id'] in original, 'Retry outside first-pass population')
        before = original[record['job_id']]
        require(first_report.exception_category(before['result']) == 'unreviewed_linked_content' and before['result']['status'] == 'failed', 'Retry replaces an unrelated outcome')
        require(all(record[k] == before[k] for k in ('article_id', 'issue_id', 'source_reference')), 'Retry changed source identity')
        original[record['job_id']] = record
    return [original[r['job_id']] for r in originals]


def qualify(record, batch_root, checkpoint_root):
    result = deepcopy(record)
    result['source_evidence']['path'] = checkpoint_root + '/' + result['source_evidence']['path']
    for item in result['failure_evidence']:
        item['path'] = checkpoint_root + '/' + item['path']
    if result['result'].get('package'):
        result['result']['package'] = batch_root + '/' + result['result']['package']
    result['batch_root'], result['checkpoint_root'] = batch_root, checkpoint_root
    return result


def find_run(runner):
    roots = []
    for path in (runner.output / 'runs').glob('*/manifest.json'):
        manifest = read_json(path)
        identity = json.loads(checked_file(path.parent, manifest['identity']))
        if identity['pipeline_identity_sha256'] == key(runner.identity) and identity['orchestrator_sha256'] == digest(Path(association_pass.__file__).read_bytes()):
            for name in ('first_pass_record', 'sample_record', 'review_record'):
                checked_file(ROOT, identity[name])
            roots.append(path.parent)
    require(len(roots) == 1, 'Expected exactly one completed run for current 14b inputs')
    return roots[0]


def build():
    runner = retry_associations.AssociationRunner(association_pass.OUTPUT)
    root = find_run(runner)
    manifest = read_json(root / 'manifest.json')
    require(manifest['state'] == 'all_association_candidates_have_subsequent_outcomes', 'Retry execution incomplete')
    expected = {r['path']: r for r in manifest['outputs']}
    require(len(expected) == len(manifest['outputs']), 'Duplicate retry manifest output')
    actual = {p.relative_to(root).as_posix() for directory in ('outcomes', 'jobs', 'evidence', 'issues') for p in (root / directory).rglob('*') if p.is_file()}
    require(actual == set(expected), 'Retry execution artifact population differs')
    for item in manifest['outputs']:
        checked_file(root, item)
    first = read_json(associations.FIRST_PASS)
    originals = first_records(runner, first)
    by_job = {j['id']: j for j in runner.data['jobs']}
    retry_queue = read_json(runner.review_root / 'retry-queue.json')
    pointers, retries = {}, []
    print('Verifying all 470 subsequent outcomes and their evidence', flush=True)
    for row in retry_queue:
        job = by_job[row['job_id']]
        pointer = read_json(root / 'outcomes' / (job['id'].rsplit(':', 1)[1] + '.json'))
        record = load_outcome(pointer, job, key(runner.identity))
        association = next((e for e in record['stage_evidence'] if e['path'].split('/')[-2].endswith('-association')), None)
        require(association is not None, 'Retry did not pass reviewed association')
        require(read_json(ROOT / pointer['batch_root'] / association['path'] / 'association.json') == job, 'Retry changed article boundaries')
        pointers[job['id']] = pointer
        retries.append(record)
    require(len(retries) == 470 and manifest['retry_outcomes'] == histogram(r['outcome'] for r in retries), 'Retry outcome totals differ')
    require(manifest['origins'] == histogram(p['origin'] for p in pointers.values()) == {'14a': 6, '14b': 464}, 'Sample carry-forward population differs')
    current = current_records(originals, retries)
    locations = {r['job_id']: {'batch_root': 'build/cd1-batch', 'checkpoint_root': first['run_root'], 'origin': '13d'} for r in originals}
    locations.update(pointers)
    def first_table(name):
        item = next(r for r in first['outputs'] if r['path'] == name + '.jsonl')
        return [json.loads(line) for line in checked_file(ROOT / first['coverage_root'], item).splitlines()]
    source_checks = first_table('source_checks')
    require(len(source_checks) == 537, 'First-pass successful source audit population changed')
    auxiliary_ids = {t['id'] for t in first_table('topics') if t['state'] == 'auxiliary_text_recovered'}
    aux_review = {r['topic_id']: r for r in read_json(runner.review_root / 'recoveries.json')}
    auxiliary_ids.update(k for k, r in aux_review.items() if r['status'] == 'recovered')
    prepared, media, assets, conversions, verified_historical_stages = {}, {}, {}, {}, set()
    standalone_files = {}
    print('Validating every current standalone and auditing newly prepared source runs', flush=True)
    for record in current:
        location = locations[record['job_id']]
        batch_root = ROOT / location['batch_root']
        if location['origin'] == '13d':
            for item in record['failure_evidence']:
                checked_file(ROOT / location['checkpoint_root'], item)
        # Keep attempted media diagnostics even when later article preparation failed.
        for event in record['stage_evidence']:
            path = batch_root / event['path']
            if location['origin'] == '13d' and event['path'] not in verified_historical_stages:
                verify(path, event['fingerprint'])
                require(digest((path / 'checkpoint.json').read_bytes()) == event['checkpoint_sha256'], 'Historical stage checkpoint changed')
                verified_historical_stages.add(event['path'])
            if path.parent.name.startswith('media-'):
                resource = path.parent.name.removeprefix('media-')
                converted = read_json(path / 'conversion.json')
                conversions[resource] = {'status': read_json(path / 'media.json')['status'],
                    'concerns': converted.get('concerns', []), 'error': converted.get('error'), 'policy': converted.get('policy'),
                    'diagnostics': file_record((path / 'conversion.json').relative_to(ROOT).as_posix(), (path / 'conversion.json').read_bytes())}
        result = record['result']
        if result['status'] != 'prepared':
            continue
        package_root = batch_root / result['package']
        verify(package_root, result['stages']['package']['fingerprint'])
        bundle, package_manifest, counts = load_package(package_root / 'content')
        require(counts == {**result['counts'], 'files': counts['files'], 'assets': counts['assets'], 'previews': counts['previews']}, 'Standalone counts changed')
        require(len(bundle['articles']) == 1, 'Current standalone article population changed')
        article = bundle['articles'][0]
        require(article['id'] == record['article_id'] and article['issue_id'] == record['issue_id'] and article['source']['reference'] == record['source_reference'], 'Current article identity changed')
        require(article['id'] not in prepared, 'Duplicate current article')
        prepared[article['id']] = article
        article_path = f"articles/{article['source']['disc_id']}/{article['source']['reference']}.json"
        standalone_files[article['id']] = [file_record(article_path, (package_root / 'content' / article_path).read_bytes()),
            *package_manifest['previews'], *[m['asset'] for m in bundle['media']['items'] if m['asset']]]
        for item in bundle['media']['items']:
            name = item['source']['resource']
            require(name not in media or media[name] == item, 'Shared current media differs')
            media[name] = item
            if item['asset']:
                assets[name] = package_root / 'content' / item['asset']['path']
        if location['origin'] != '13d':
            job = by_job[record['job_id']]
            recovered = read_json(batch_root / result['stages']['recovery']['path'] / 'recovery.json')
            require([t['ordinal'] for t in recovered['topics']] == [t['native']['ordinal'] for t in job['source_topics']], 'Retry merged or omitted source topics')
            checks = [check_topic(runner.rtf, t, s['rtf']) for t, s in zip(recovered['topics'], job['source_topics'])]
            source_checks.append({'article_id': article['id'], 'topics': checks})
            for aux in result['auxiliaries']:
                if aux['topic_id'] in aux_review:
                    require(aux['recovery_status'] == aux_review[aux['topic_id']]['status'], 'Auxiliary recovery disposition changed')
                if aux['recovery_status'] == 'recovered':
                    ordinal = runner.topic_lookup[aux['topic_id']]['native']['ordinal']
                    decoded = read_json(batch_root / result['stages']['association']['path'] / f'auxiliaries/{ordinal}/recovery.json')
                    check_topic(runner.rtf, decoded, aux['rtf'])
                    if aux['topic_id'] in aux_review:
                        require(decoded == read_json(runner.review_root / f'topics/{ordinal}/recovery.json'), 'Retry auxiliary differs from independent audit')
        if len(prepared) % 100 == 0:
            print(f'Validated {len(prepared)} current articles', flush=True)
    print('Validating all combined issue packages and exact standalone content', flush=True)
    issues = []
    for issue_id in sorted({j['issue_id'] for j in runner.data['jobs']}):
        row = read_json(root / 'issues' / (issue_id + '.json'))
        require(row['status'] == 'prepared', 'Unresolved current issue composition failure: ' + issue_id)
        path = runner.output / row['package']
        verify(path, row['fingerprint'])
        bundle, _, counts = load_package(path / 'content')
        require(counts == row['counts'], 'Combined issue counts changed')
        expected_articles = {a['id']: a for a in prepared.values() if a['issue_id'] == issue_id}
        require({a['id']: a for a in bundle['articles']} == expected_articles, 'Combined issue omitted, duplicated or changed an article')
        require(len(bundle['articles']) == len(expected_articles) and row['article_ids'] == [a['id'] for a in bundle['articles']], 'Combined issue duplicate/order mismatch')
        for article_id in expected_articles:
            for item in standalone_files[article_id]:
                checked_file(path / 'content', item)
        issues.append({'issue_id': issue_id, **row})
    require(len(issues) == manifest['issues'] == 72 and manifest['issue_states'] == {'prepared': 72}, 'Combined issue population differs')
    print('Checking current media resources and bitmap pixels', flush=True)
    media_rows, pixel_checks = [], 0
    for original in first_table('media'):
        name = original['resource']
        raw = images.checked_source(name, runner.media_manifest)
        item = media.get(name)
        if item and item['status'] == 'available' and name.endswith(('.bmp', '.dib')):
            source, derivative = images.bitmap_pixels(images.RAW / name), images.bitmap_pixels(assets[name])
            require(all(source[k] == derivative[k] for k in ('width', 'height', 'rgba_sha256')), 'Current bitmap differs from source: ' + name)
            pixel_checks += 1
        media_rows.append({'resource': name, 'topic_ids': original['topic_ids'], 'job_ids': original['job_ids'],
            'source': {'status': 'verified', 'bytes': len(raw), 'sha256': digest(raw)},
            'runtime_status': item['status'] if item else 'not_packaged', 'runtime_record': item, 'conversion': conversions.get(name)})
    qualified = [qualify(r, locations[r['job_id']]['batch_root'], locations[r['job_id']]['checkpoint_root']) for r in current]
    data = first_report.reconcile(runner.data, qualified, prepared, auxiliary_ids, media_rows)
    for exception in data['exceptions']:
        if locations[exception['job_id']]['origin'] != '13d':
            # The shared checkpoint helper retains the historical base-runner
            # command. A later source-policy fix must use the auxiliary extension.
            historical = exception['retry']
            exception['retry'] = {'status': 'requires_bounded_source_policy_follow_up',
                'job_id': exception['job_id'], 'pipeline_class': 'tools.batch.retry_associations.AssociationRunner',
                'output_policy': 'use a new private output root; preserve recorded outcomes',
                'historical_base_runner_command': historical}
    issue_lookup = {r['issue_id']: r for r in issues}
    for row in data['catalog']:
        row['origin'] = locations[row['job_id']]['origin']
        row['current_issue_package'] = (runner.output / issue_lookup[row['issue_id']]['package']).relative_to(ROOT).as_posix()
    before = {r['job_id']: r for r in originals}
    data['retry_history'] = [{'job_id': r['job_id'], 'article_id': r['article_id'], 'issue_id': r['issue_id'],
        'previous_outcome': before[r['job_id']]['outcome'], 'previous_error': before[r['job_id']]['result'].get('error'),
        'subsequent_outcome': r['outcome'], 'subsequent_error': r['result'].get('error'),
        'subsequent_category': first_report.exception_category(r['result']) if r['result']['status'] != 'prepared' else None,
        'checkpoint': pointers[r['job_id']]} for r in retries]
    data['issues'], data['source_checks'] = issues, source_checks
    for row in data['topics']:
        if row['id'] in aux_review:
            row['auxiliary_recovery_status'] = aux_review[row['id']]['status']
    new = [r for r in retries if pointers[r['job_id']]['origin'] == '14b']
    counts = {'candidates': len(current), 'retry_candidates': len(retries), 'new_attempts': len(new), 'carried_sample': 6,
        'retry_outcomes': histogram(r['outcome'] for r in retries), 'new_attempt_outcomes': histogram(r['outcome'] for r in new),
        'current_outcomes': histogram(r['outcome'] for r in current), 'previous_prepared': 537,
        'additional_prepared_since_13d': sum(r['result']['status'] == 'prepared' for r in retries),
        'new_prepared_in_14b': sum(r['result']['status'] == 'prepared' for r in new), 'current_prepared': len(prepared),
        'issues': len(issues), 'native_topics': len(data['topics']), 'topic_states': histogram(t['state'] for t in data['topics']),
        'native_contexts': len(data['contexts']), 'index_references': len(data['references']), 'index_entries': len(data['entries']),
        'index_occurrences': sum(len(r['occurrence_ids']) for r in data['references']), 'toc_entries': len(data['toc']),
        'toc_content_status': histogram(t['content_status'] for t in data['toc']), 'toc_metadata_status': histogram(t['status'] for t in data['toc']),
        'prepared_without_toc_link': sum(not a['toc_entry_ids'] for a in prepared.values()),
        'unindexed_candidates': histogram(r['outcome'] for r in current if not by_job[r['job_id']]['index_references']),
        'unattributed_topics': len(data['unattributed']), 'current_exception_categories': histogram(e['category'] for e in data['exceptions']),
        'retry_exception_categories': histogram(first_report.exception_category(r['result']) for r in retries if r['result']['status'] != 'prepared'),
        'source_media': len(media_rows), 'runtime_media': histogram(m['runtime_status'] for m in media_rows), 'pixel_equivalent_bitmaps': pixel_checks,
        'paragraphs': sum(len(b['paragraphs']) for a in prepared.values() for s in a['sections'] for b in s['blocks']),
        'blocks': sum(len(s['blocks']) for a in prepared.values() for s in a['sections']),
        'source_bytes_accounted': sum(t['accounted_bytes'] for a in source_checks for t in a['topics']),
        'text_runs_accounted': sum(t['text_runs'] for a in source_checks for t in a['topics'])}
    require(counts['current_prepared'] == 537 + manifest['additional_prepared'] == 537 + counts['additional_prepared_since_13d'], 'Preparation gains differ')
    require((counts['candidates'], counts['retry_candidates'], counts['new_attempts'], counts['native_topics'], counts['native_contexts'], counts['toc_entries'], counts['source_media']) ==
            (1088, 470, 464, 3099, 2103, 5497, 6165), 'Current source population differs')
    require(len(source_checks) == len(prepared) and {a['article_id'] for a in source_checks} == set(prepared), 'Current source audit coverage differs')
    files = {name + '.jsonl': b''.join(json.dumps(row, ensure_ascii=False, separators=(',', ':')).encode() + b'\n' for row in rows) for name, rows in data.items()}
    summary = {'schema_version': 1, 'checkpoint': '14b', 'scope': 'all_association_retries_and_current_CD1_coverage',
        'pipeline_identity_sha256': key(runner.identity), 'run_root': root.relative_to(ROOT).as_posix(),
        'output_root': runner.output.relative_to(ROOT).as_posix(), 'counts': counts, 'issues': issues,
        'execution_manifest': file_record((root / 'manifest.json').relative_to(ROOT).as_posix(), (root / 'manifest.json').read_bytes()),
        'first_pass_record': file_record(associations.FIRST_PASS.relative_to(ROOT).as_posix(), associations.FIRST_PASS.read_bytes()),
        'first_pass_execution_manifest': first['execution_manifest'],
        'report_dependencies': {Path(p).relative_to(ROOT).as_posix(): digest(Path(p).read_bytes()) for p in (__file__, first_report.__file__, association_pass.__file__)},
        'verification': {'all_470_subsequent_outcomes_verified': True, 'all_current_standalone_and_combined_packages_validated': True,
                        'all_retry_associations_preserve_article_boundaries': True, 'all_retry_success_source_runs_checked': True,
                        'standalone_article_preview_and_media_bytes_preserved_in_combined_issues': True,
                        'unchanged_first_pass_source_audits_carried_forward': 537, 'all_source_populations_reconciled': True,
                        'physical_review': 'pending'},
        'limits': ['first_pass_history_preserved', 'remaining_failures_and_blockers_not_extracted', 'generic_semantic_review_pending',
                   'auxiliary_topics_18_and_19_and_auxiliary_rendering_deferred', 'printed_issue_completeness_not_established', 'deferred_media_not_repaired']}
    return root, summary, files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-record', action='store_true')
    args = parser.parse_args()
    root, summary, files = build()
    cache = Cache(root / 'reports', summary['report_dependencies'])
    def produce(stage):
        for name, raw in files.items():
            write(stage / name, raw)
    path, manifest = cache.stage('current-coverage', {'execution_manifest': summary['execution_manifest']}, produce)
    first_report.verify_generated_coverage(path, manifest, files)
    summary.update(coverage_root=path.relative_to(ROOT).as_posix(), outputs=manifest['outputs'])
    if args.write_record:
        write(RECORD, json_bytes(summary))
    else:
        require(read_json(RECORD) == summary, 'Current coverage differs from recorded result')
    print(json.dumps(summary['counts'], indent=2), flush=True)


if __name__ == '__main__':
    main()
