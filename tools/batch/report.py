"""Reconcile all CD1 first-pass jobs, sources, TOC links, packages and exceptions."""
import argparse
from collections import Counter, defaultdict
from pathlib import Path
import json

from tools.batch.full_pass import verify_job, outcome
from tools.run_cd1_batch import Runner, ROOT, OUTPUT, read_json
from tools.cd1_batch_cache import key, verify, write, Cache
from tools.recover_cd1_text import json_bytes
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from tools import inventory_cd1_processing as queue
from tools import map_cd1_images as images
from tools.validate_cd1_batch import check_topic
from maso_archive.reading_room_package import checked_file, file_record, load_package

RECORD = ROOT / 'data/catalog/batch-runs/cd1-full-pass.json'


def histogram(values):
    return dict(sorted(Counter(values).items()))


def verify_generated_coverage(path, manifest, files):
    outputs = {item['path']: item for item in manifest['outputs']}
    require(len(outputs) == len(manifest['outputs']) and set(outputs) == set(files), 'Coverage report population changed')
    for name, raw in files.items():
        require(checked_file(path, outputs[name]) == raw, 'Regenerated coverage differs: ' + name)


def exception_category(result):
    if result['status'] == 'blocked':
        return 'source_topic_ownership'
    error = result.get('error', '')
    for text, category in [('Related content', 'unreviewed_linked_content'), ('Unsupported inherited', 'unsupported_inherited_formatting'),
                           ('Unsupported RTF', 'unsupported_rtf_construct'), ('Undecoded text', 'font_or_decoding_policy'),
                           ('Unterminated paragraph', 'unterminated_paragraph'), ('Skipped heading', 'semantic_structure'),
                           ('Unsupported visible', 'unsupported_visible_control'), ('Unmatched closing brace', 'rtf_document_envelope'), ('Missing/duplicate manifest', 'missing_media_source'),
                           ('No such file', 'missing_source_file')]:
        if text in error:
            return category
    return 'other_retained_failure'


def reconcile(data, records, prepared, auxiliary_ids, media):
    """Pure population reconciliation; failed jobs never imply extracted content."""
    jobs = {j['id']: j for j in data['jobs']}
    require(len(records) == len(jobs) and {r['job_id'] for r in records} == set(jobs), 'Missing/duplicate candidate outcomes')
    by_job = {r['job_id']: r for r in records}
    require(set(prepared) == {r['article_id'] for r in records if r['result']['status'] == 'prepared'}, 'Prepared population differs from successful jobs')
    owners = defaultdict(list)
    for job in jobs.values():
        for source in job['source_topics']:
            owners[source['id']].append(job['id'])
    topics = []
    for topic in data['topics']:
        linked = owners[topic['id']]
        require(len(linked) <= 1, 'Topic owned by multiple candidates')
        if linked:
            result = by_job[linked[0]]
            state = 'prepared_article_content' if result['result']['status'] == 'prepared' else result['outcome']
        elif topic['id'] in auxiliary_ids:
            state = 'auxiliary_text_recovered'
        else:
            state = {'formatting_separator': 'formatting_source_retained', 'unattributed_content': 'unattributed_source_retained',
                     'linked_auxiliary_topic': 'auxiliary_source_retained'}.get(topic['role'], 'non_article_source_retained')
        topics.append({'id': topic['id'], 'role': topic['role'], 'state': state, 'job_ids': linked,
                       'native': topic['native'], 'rtf': topic['rtf'], 'aliases': topic['aliases'], 'links': topic['links']})
    topic_by_id = {t['id']: t for t in topics}
    require(len(topic_by_id) == len(data['topics']), 'Duplicate native topic')
    contexts = [{**c, 'content_state': topic_by_id[c['topic_id']]['state']} for c in data['contexts']]
    references, occurrences = [], {}
    for reference in data['references']:
        job_id = reference['job_id']
        state = by_job[job_id]['outcome'] if job_id else 'non_article_target'
        row = {**reference, 'outcome': state, 'article_id': jobs[job_id]['candidate_article_id'] if job_id else None,
               'content_available': bool(job_id and by_job[job_id]['result']['status'] == 'prepared')}
        references.append(row)
        for occurrence in reference['occurrence_ids']:
            require(occurrence not in occurrences, 'Duplicate index occurrence')
            occurrences[occurrence] = {'reference': reference['reference'], 'topic_id': reference['topic_id'],
                                       'job_id': job_id, 'outcome': state, 'content_available': row['content_available']}
    entries = [{**entry, 'target': occurrences.get(entry['id']),
                'availability': 'available' if occurrences.get(entry['id'], {}).get('content_available') else 'source_metadata_retained'}
               for entry in data['entries']]
    require(set(occurrences) <= {e['id'] for e in entries}, 'Index occurrence missing source row')
    toc = []
    for source in data['toc']:
        available = [jobs[j]['candidate_article_id'] for j in source['matched_job_ids'] if by_job[j]['result']['status'] == 'prepared']
        for article_id in available:
            require(source['toc_entry_id'] in prepared[article_id]['toc_entry_ids'], 'Runtime TOC match differs from inventory')
        toc.append({**source, 'article_ids': available, 'content_status': 'available' if available else 'unavailable',
                    'matched_job_outcomes': {j: by_job[j]['outcome'] for j in source['matched_job_ids']}})
    expected_links = {(t['toc_entry_id'], a) for t in toc for a in t['article_ids']}
    actual_links = {(t, a['id']) for a in prepared.values() for t in a['toc_entry_ids']}
    require(expected_links == actual_links, 'Prepared TOC links missing or invented')
    catalog = [{'job_id': j['id'], 'article_id': j['candidate_article_id'], 'source_reference': j['source_reference'],
                'issue_id': j['issue_id'], 'title': j['title'], 'outcome': by_job[j['id']]['outcome'],
                'content_status': 'available' if j['candidate_article_id'] in prepared else 'unavailable',
                'toc_entry_ids': j['toc']['matched_ids'], 'index_occurrence_ids': j['occurrence_ids'],
                'package': by_job[j['id']]['result'].get('package'), 'print_verification': 'pending'} for j in jobs.values()]
    exceptions = [{'job_id': r['job_id'], 'article_id': r['article_id'], 'issue_id': r['issue_id'], 'outcome': r['outcome'],
                   'category': exception_category(r['result']), 'error': r['result'].get('error'), 'blockers': r['result'].get('blockers', []),
                   'source_evidence': r['source_evidence'], 'failure_evidence': r['failure_evidence'], 'retry': r['retry']}
                  for r in records if r['result']['status'] != 'prepared']
    return {'topics': topics, 'contexts': contexts, 'references': references, 'entries': entries, 'toc': toc,
            'catalog': catalog, 'exceptions': exceptions, 'media': media, 'unattributed': data['review_items']}


def build(runner, root):
    manifest = read_json(root / 'manifest.json')
    require(manifest['state'] == 'all_candidates_attempted', 'Execution not complete')
    checked_file(root, manifest['identity'])
    identity_record = read_json(root / 'identity.json')
    require(identity_record['pipeline_identity_sha256'] == key(runner.identity), 'Extraction pipeline changed since first pass')
    records_by_path = {r['path']: r for r in manifest['outputs']}
    require(len(records_by_path) == len(manifest['outputs']), 'Duplicate run manifest output')
    actual = {p.relative_to(root).as_posix() for directory in ('jobs', 'issues', 'evidence') for p in (root / directory).rglob('*') if p.is_file()}
    require(actual == set(records_by_path), 'First-pass artifact population changed')
    print(f'Verifying {len(manifest["outputs"])} execution evidence files', flush=True)
    for item in manifest['outputs']:
        checked_file(root, item)
    records = [verify_job(root, runner.output, read_json(root / 'jobs' / (j['id'].rsplit(':', 1)[1] + '.json')), key(runner.identity))
               for j in runner.data['jobs']]
    for expected, record in zip(runner.data['jobs'], records):
        require(all(record[k] == expected[source] for k, source in [('job_id', 'id'), ('article_id', 'candidate_article_id'),
                    ('source_reference', 'source_reference'), ('issue_id', 'issue_id')]), 'Outcome identity differs from source queue')
        require(checked_file(root, record['source_evidence']) == json_bytes(expected), 'Recorded source job differs from frozen queue')
    require(manifest['outcomes'] == histogram(r['outcome'] for r in records), 'Manifest outcome counts changed')
    print('Auditing every successful article against source bytes', flush=True)
    prepared, runtime_media, media_assets, auxiliary_ids, source_checks = {}, {}, {}, set(), []
    attempted_media = {}
    for record in records:
        result = record['result']
        for event in record['stage_evidence']:
            path = runner.output / event['path']
            if path.parent.name.startswith('media-'):
                name = path.parent.name.removeprefix('media-')
                item = read_json(path / 'media.json')
                conversion = read_json(path / 'conversion.json')
                attempted_media[name] = {'status': item['status'], 'concerns': conversion.get('concerns', []),
                                         'error': conversion.get('error'), 'policy': conversion.get('policy'),
                                         'diagnostics': file_record((path / 'conversion.json').relative_to(runner.output).as_posix(), (path / 'conversion.json').read_bytes())}
        if result['status'] != 'prepared':
            continue
        bundle, _, counts = load_package(runner.output / result['package'] / 'content')
        article = bundle['articles'][0]
        require(article['id'] == record['article_id'] and article['source']['reference'] == record['source_reference'] and
                article['issue_id'] == record['issue_id'], 'Prepared identity differs from source job')
        require(counts == {**result['counts'], 'files': counts['files'], 'assets': counts['assets'], 'previews': counts['previews']}, 'Article counts changed')
        prepared[article['id']] = article
        for item in bundle['media']['items']:
            name = item['source']['resource']
            require(name not in runtime_media or runtime_media[name] == item, 'Shared runtime media differs')
            runtime_media[name] = item
            if item["asset"]:
                media_assets[name] = runner.output / result["package"] / "content" / item["asset"]["path"]
        job = json.loads(checked_file(root, record['source_evidence']))
        recovered = read_json(runner.output / result['stages']['recovery']['path'] / 'recovery.json')
        require([t['ordinal'] for t in recovered['topics']] == [s['native']['ordinal'] for s in job['source_topics']],
                'Recovery topic population/order changed')
        checks = [check_topic(runner.rtf, t, s['rtf']) for t, s in zip(recovered['topics'], job['source_topics'])]
        for auxiliary in result.get('auxiliaries', []):
            if auxiliary['recovery_status'] == 'recovered':
                ordinal = runner.topic_lookup[auxiliary['topic_id']]['native']['ordinal']
                recovered_aux = read_json(runner.output / result['stages']['association']['path'] / f'auxiliaries/{ordinal}/recovery.json')
                check_topic(runner.rtf, recovered_aux, auxiliary['rtf'])
                auxiliary_ids.add(auxiliary['topic_id'])
        source_checks.append({'article_id': article['id'], 'topics': checks})
        if len(source_checks) % 50 == 0:
            print(f'Audited {len(source_checks)} successful articles', flush=True)
    print('Validating all issue packages and exact article populations', flush=True)
    issues = []
    for issue_id in sorted({j['issue_id'] for j in runner.data['jobs']}):
        row = read_json(root / 'issues' / (issue_id + '.json'))
        require(row['status'] in ('prepared', 'metadata_only'), 'Unresolved issue composition failure: ' + issue_id)
        path = runner.output / row['package']
        verify(path, row['fingerprint'])
        bundle, _, counts = load_package(path / 'content')
        require(counts == row['counts'], 'Issue package counts differ')
        require({a['id'] for a in bundle['articles']} == {a['id'] for a in prepared.values() if a['issue_id'] == issue_id}, 'Issue/package outcome reconciliation failed')
        for article in bundle['articles']:
            require(article == prepared[article['id']], 'Issue altered standalone article')
        issues.append({'issue_id': issue_id, **row, 'candidate_outcomes': histogram(r['outcome'] for r in records if r['issue_id'] == issue_id)})
    require(manifest['jobs'] == len(records) and manifest['issues'] == len(issues), 'Execution manifest population differs')
    require(manifest['issue_states'] == histogram(i['status'] for i in issues), 'Execution issue outcomes differ')
    resource_topics = defaultdict(list)
    resource_jobs = defaultdict(list)
    for topic in runner.data['topics']:
        for name in topic['features']['resources']:
            resource_topics[name].append(topic['id'])
    for job in runner.data['jobs']:
        for name in job['features']['resources']:
            resource_jobs[name].append(job['id'])
    print(f'Checking {len(resource_topics)} referenced source resources and available bitmap pixels', flush=True)
    media, pixel_checks = [], 0
    for name in sorted(resource_topics):
        try:
            raw = images.checked_source(name, runner.media_manifest)
            source = {'status': 'verified', 'bytes': len(raw), 'sha256': digest(raw)}
        except (OSError, ValueError) as error:
            source = {'status': 'missing_or_invalid', 'error': str(error)}
        item = runtime_media.get(name)
        if item and item['status'] == 'available' and name.endswith(('.bmp', '.dib')):
            original, converted = images.bitmap_pixels(images.RAW / name), images.bitmap_pixels(media_assets[name])
            require(all(original[k] == converted[k] for k in ('width', 'height', 'rgba_sha256')), 'Prepared bitmap pixels differ: ' + name)
            pixel_checks += 1
        media.append({'resource': name, 'topic_ids': resource_topics[name], 'job_ids': resource_jobs[name], 'source': source,
                      'runtime_status': item['status'] if item else 'not_packaged', 'runtime_record': item,
                      'conversion': attempted_media.get(name)})
    data = reconcile(runner.data, records, prepared, auxiliary_ids, media)
    data['issues'], data['source_checks'] = issues, source_checks
    counts = {'candidates': len(records), 'outcomes': histogram(r['outcome'] for r in records), 'prepared_articles': len(prepared),
              'issues': len(issues), 'issue_states': histogram(i['status'] for i in issues),
              'native_topics': len(data['topics']), 'topic_states': histogram(t['state'] for t in data['topics']),
              'native_contexts': len(data['contexts']), 'index_references': len(data['references']), 'index_entries': len(data['entries']),
              'index_occurrences': sum(len(r['occurrence_ids']) for r in data['references']),
              'index_occurrence_outcomes': histogram(r['outcome'] for r in data['references'] for _ in r['occurrence_ids']),
              'toc_entries': len(data['toc']), 'toc_content_status': histogram(t['content_status'] for t in data['toc']),
              'toc_metadata_status': histogram(t['status'] for t in data['toc']),
              'prepared_without_toc_link': sum(not a['toc_entry_ids'] for a in prepared.values()),
              'unindexed_candidates': histogram(r['outcome'] for r in records if not next(j for j in runner.data['jobs'] if j['id'] == r['job_id'])['index_references']),
              'unattributed_topics': len(data['unattributed']), 'exception_categories': histogram(e['category'] for e in data['exceptions']),
              'pixel_equivalent_bitmaps': pixel_checks, 'source_media': len(media), 'source_media_status': histogram(m['source']['status'] for m in media),
              'runtime_media': histogram(m['runtime_status'] for m in media), 'attempted_media': len(attempted_media),
              'paragraphs': sum(len(s['paragraphs']) if 'paragraphs' in s else sum(len(b['paragraphs']) for b in s['blocks']) for a in prepared.values() for s in a['sections']),
              'blocks': sum(len(s['blocks']) for a in prepared.values() for s in a['sections']),
              'source_bytes_checked': sum(t['accounted_bytes'] for a in source_checks for t in a['topics']),
              'text_runs_checked': sum(t['text_runs'] for a in source_checks for t in a['topics'])}
    require((counts['candidates'], counts['issues'], counts['native_topics'], counts['native_contexts'], counts['index_occurrences'], counts['toc_entries']) ==
            (1088, 72, 3099, 2103, 2462, 5497), 'Frozen first-pass source population differs')
    sample = read_json(ROOT / 'data/catalog/batch-runs/cd1-validation-sample.json')
    sample_ids = {a['article_id'] for a in sample['source_checks']['articles']}
    reused = [r for r in records if r['article_id'] in sample_ids]
    require(len(reused) == 15 and all(r['result']['status'] == 'prepared' and set(r['stage_cache']) == {'hit'} for r in reused), 'Validated sample stages were not carried forward unchanged')
    files = {name + '.jsonl': b''.join(json.dumps(row, ensure_ascii=False, separators=(',', ':')).encode() + b'\n' for row in rows)
             for name, rows in data.items()}
    summary = {'schema_version': 1, 'checkpoint': '13d', 'scope': 'first_complete_CD1_pass', 'pipeline_identity_sha256': key(runner.identity),
               'run_root': root.relative_to(ROOT).as_posix(), 'counts': counts,
               'source_inventory_record': 'data/catalog/processing-inventories/cd1.json',
               'execution_manifest': file_record((root / 'manifest.json').relative_to(ROOT).as_posix(), (root / 'manifest.json').read_bytes()),
               'reporter': file_record(Path(__file__).resolve().relative_to(ROOT).as_posix(), Path(__file__).read_bytes()),
               'verification': {'all_1088_candidates_have_outcomes': len(records) == 1088, 'all_successful_article_and_issue_packages_checked': True,
                                'all_prepared_source_runs_and_topic_accounting_checked': True, 'sample_articles_carried_forward_from_cache': len(reused),
                                'all_native_topics_contexts_and_index_occurrences_reconciled': True, 'physical_verification': 'pending'},
               'issues': issues, 'limits': ['failed_and_blocked_jobs_are_not_extracted', 'semantic_review_pending_for_generic_preparations',
                                        'first_pass_does_not_establish_complete_printed_issue_coverage', 'deferred_media_not_repaired',
                                        'individual_exceptions_remain_subsequent_bounded_work']}
    return summary, files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-record', action='store_true')
    args = parser.parse_args()
    runner = Runner()
    root = runner.output / 'full-pass' / key(runner.identity)
    summary, files = build(runner, root)
    cache = Cache(root / 'reports', {'reporter_sha256': digest(Path(__file__).read_bytes())})
    def produce(stage):
        for name, raw in files.items():
            write(stage / name, raw)
    path, manifest = cache.stage('coverage', {'execution_manifest': summary['execution_manifest']}, produce)
    verify_generated_coverage(path, manifest, files)
    summary['coverage_root'] = path.relative_to(ROOT).as_posix()
    summary['outputs'] = manifest['outputs']
    if args.write_record:
        write(RECORD, json_bytes(summary))
    else:
        require(read_json(RECORD) == summary, 'Full-pass report differs from reviewed record')
    print(json.dumps(summary['counts'], ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
