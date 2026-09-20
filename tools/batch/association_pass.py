"""Run all 14b association retries and compose current issues without rewriting history."""
from collections import Counter
from pathlib import Path
import json

from tools.batch import associations, retry_associations
from tools.batch.full_pass import persist_job, verify_job
from tools.run_cd1_batch import ROOT, read_json, isolate
from tools.cd1_batch_core import inherited_states
from tools.cd1_batch_cache import Cache, key, write, verify
from tools.recover_cd1_text import json_bytes
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from tools.check_cd1_second_article import assemble
from maso_archive.reading_room_package import checked_file, file_record, load_package

OUTPUT = ROOT / 'build/cd1-association-pass'


def histogram(values):
    return dict(sorted(Counter(values).items()))


def load_outcome(pointer, job, identity):
    batch_root, checkpoint_root = (ROOT / pointer[k] for k in ('batch_root', 'checkpoint_root'))
    require(all(p.resolve().is_relative_to(ROOT / 'build') for p in (batch_root, checkpoint_root)), 'Outcome outside private build roots')
    record = json.loads(checked_file(checkpoint_root, pointer['record']))
    verify_job(checkpoint_root, batch_root, record, identity)
    require(record['job_id'] == job['id'] and record['article_id'] == job['candidate_article_id'] and
            record['source_reference'] == job['source_reference'] and record['issue_id'] == job['issue_id'], 'Retry identity changed')
    require(checked_file(checkpoint_root, record['source_evidence']) == json_bytes(job), 'Retry source job changed')
    return record


def entry_for(record, batch_root, origin):
    return {'job_id': record['job_id'], 'article_id': record['article_id'], 'issue_id': record['issue_id'],
            'origin': origin, 'batch_root': batch_root, 'result': record['result']}


def merge_bundles(packages, issue_id):
    """Merge already-validated standalone packages, rejecting identity/media collisions."""
    articles, media, assets, previews, seen_jobs = [], {}, {}, [], set()
    for entry, bundle, manifest, root in packages:
        require(entry['result']['status'] == 'prepared', 'Unavailable article cannot enter current package')
        require(entry['job_id'] not in seen_jobs, 'Duplicate current job')
        seen_jobs.add(entry['job_id'])
        require(len(bundle['articles']) == 1, 'Expected standalone article package')
        article = bundle['articles'][0]
        require(article['id'] == entry['article_id'] and article['issue_id'] == issue_id == entry['issue_id'], 'Current article identity mismatch')
        require(article['id'] not in {a['id'] for a in articles}, 'Duplicate current article')
        articles.append(article)
        for item in bundle['media']['items']:
            require(item['id'] not in media or media[item['id']] == item, 'Conflicting shared media')
            media[item['id']] = item
            if item['asset']:
                path = item['asset']['path']
                raw = checked_file(root, item['asset'])
                require(path not in assets or assets[path] == raw, 'Conflicting asset bytes')
                assets[path] = raw
        previews.extend((r['article_id'], r['section_id'], r['path'], checked_file(root, r)) for r in manifest['previews'])
    return sorted(articles, key=lambda a: a['id']), sorted(media.values(), key=lambda m: m['id']), assets, previews


def compose_current(runner, cache, issue_id, entries):
    selected = sorted([e for e in entries if e['issue_id'] == issue_id and e['result']['status'] == 'prepared'], key=lambda e: e['article_id'])
    require(selected, 'Current issue lost all previously prepared articles')
    inputs, packages = [], []
    for entry in selected:
        root = ROOT / entry['batch_root'] / entry['result']['package']
        verify(root, entry['result']['stages']['package']['fingerprint'])
        bundle, manifest, _ = load_package(root / 'content')
        packages.append((entry, bundle, manifest, root / 'content'))
        inputs.append({k: entry[k] for k in ('job_id', 'article_id', 'origin', 'batch_root')} |
                      {'package': entry['result']['package'], 'manifest_sha256': digest((root / 'content/manifest.json').read_bytes())})
    articles, media, assets, previews = merge_bundles(packages, issue_id)
    bundle = runner.bundle(issue_id, articles, media)
    def produce(stage):
        for name, raw in assemble(bundle, assets, previews).items():
            write(stage / 'content' / name, raw)
        write(stage / 'provenance.json', json_bytes({'issue_id': issue_id, 'standalone_packages': inputs,
              'coverage': 'prepared_content_only; printed_completeness_and_physical_review_pending'}))
    path, manifest = cache.stage('issue-' + issue_id, inputs, produce, lambda p: load_package(p / 'content'))
    actual, _, counts = load_package(path / 'content')
    require(actual['articles'] == articles, 'Composition changed standalone article content')
    require(counts['articles'] == len(selected), 'Current issue article population differs')
    return {'status': 'prepared', 'package': path.relative_to(runner.output).as_posix(),
            'fingerprint': manifest['fingerprint'], 'counts': counts, 'article_ids': [a['id'] for a in articles]}


def first_records(runner, first):
    manifest = json.loads(checked_file(ROOT, first['execution_manifest']))
    files = {r['path']: r for r in manifest['outputs']}
    root = ROOT / first['run_root']
    records = []
    for job in runner.data['jobs']:
        path = 'jobs/' + job['id'].rsplit(':', 1)[1] + '.json'
        record = json.loads(checked_file(root, files[path]))
        require(record['job_id'] == job['id'] and record['article_id'] == job['candidate_article_id'] and record['issue_id'] == job['issue_id'], 'First-pass identity changed')
        require(checked_file(root, record['source_evidence']) == json_bytes(job), 'First-pass source evidence changed')
        records.append(record)
    require(len(records) == 1088 and sum(r['result']['status'] == 'prepared' for r in records) == 537, 'First-pass population changed')
    return records


def run():
    runner = retry_associations.AssociationRunner(OUTPUT)
    first, sample = read_json(associations.FIRST_PASS), read_json(retry_associations.RECORD)
    pipeline = key(runner.identity)
    require(sample['pipeline_identity_sha256'] == pipeline and sample['review_record_sha256'] == digest(associations.RECORD.read_bytes()), '14a gate does not cover current pipeline')
    require(len(sample['jobs']) == 6 and all(j['result']['status'] == 'prepared' for j in sample['jobs']) and
            sample['verification']['all_selected_associations_passed'], '14a retry sample is incomplete')
    retry_queue = read_json(runner.review_root / 'retry-queue.json')
    require(len(retry_queue) == 470 and all(r['status'] == 'association_policy_ready' for r in retry_queue), 'Reviewed retry scope changed')
    retry_ids = {r['job_id'] for r in retry_queue}
    sample_ids = {j['job_id'] for j in sample['jobs']}
    require(sample_ids <= retry_ids and len(retry_ids - sample_ids) == 464, 'Retry/sample populations differ')
    jobs = [j for j in runner.data['jobs'] if j['id'] in retry_ids]
    originals = first_records(runner, first)
    require(all(r['result']['status'] == 'failed' for r in originals if r['job_id'] in retry_ids), 'Retry would replace an earlier success')
    original_entries = [entry_for(r, 'build/cd1-batch', '13d') for r in originals if r['result']['status'] == 'prepared']
    identity = {'pipeline_identity_sha256': pipeline, 'orchestrator_sha256': digest(Path(__file__).read_bytes()),
                'first_pass_record': file_record(associations.FIRST_PASS.relative_to(ROOT).as_posix(), associations.FIRST_PASS.read_bytes()),
                'sample_record': file_record(retry_associations.RECORD.relative_to(ROOT).as_posix(), retry_associations.RECORD.read_bytes()),
                'review_record': file_record(associations.RECORD.relative_to(ROOT).as_posix(), associations.RECORD.read_bytes())}
    root = runner.output / 'runs' / key(identity)
    if (root / 'identity.json').exists():
        require(read_json(root / 'identity.json') == identity, 'Retry execution identity changed')
    else:
        write(root / 'identity.json', json_bytes(identity))
    cache = Cache(runner.output / 'current-issues', identity)
    offsets = [s['rtf']['byte_offset'] for j in jobs for s in j['source_topics']]
    offsets += [a['rtf']['byte_offset'] for a in runner.policy['auxiliaries'].values()]
    runner.states = inherited_states(runner.rtf, offsets)
    records, pointers, issues = [], [], {}
    def status(current=None):
        write(root / 'status.json', json_bytes({'total_retries': 470, 'new_candidates': 464, 'sample_carried_forward': 6,
              'recorded_retries': len(records), 'outcomes': histogram(r['outcome'] for r in records),
              'completed_issues': len(issues), 'current_job': current}))
    for issue in sorted({j['issue_id'] for j in runner.data['jobs']}):
        print('ISSUE ' + issue, flush=True)
        for job in [j for j in jobs if j['issue_id'] == issue]:
            token = job['id'].rsplit(':', 1)[1]
            target = root / 'outcomes' / (token + '.json')
            if target.exists():
                pointer = read_json(target)
                record = load_outcome(pointer, job, pipeline)
                verb = 'RESUMED'
            elif job['id'] in sample_ids:
                relative = 'jobs/' + token + '.json'
                source = ROOT / sample['checkpoints_root'] / relative
                expected = next(r for r in sample['checkpoint_outputs'] if r['path'] == relative)
                checked_file(ROOT / sample['checkpoints_root'], expected)
                pointer = {'origin': '14a', 'batch_root': sample['output_root'], 'checkpoint_root': sample['checkpoints_root'], 'record': expected}
                record = load_outcome(pointer, job, pipeline)
                write(target, json_bytes(pointer))
                verb = 'CARRIED'
            else:
                status(job['id'])
                persisted = root / 'jobs' / (token + '.json')
                if persisted.exists():
                    record = verify_job(root, runner.output, read_json(persisted), pipeline)
                    require(checked_file(root, record['source_evidence']) == json_bytes(job), 'Interrupted retry source changed')
                else:
                    begin = len(runner.cache.events)
                    result = isolate([job], runner.process)[0]
                    record = persist_job(root, runner, job, result, runner.cache.events[begin:])
                pointer = {'origin': '14b', 'batch_root': runner.output.relative_to(ROOT).as_posix(),
                           'checkpoint_root': root.relative_to(ROOT).as_posix(), 'record': file_record('jobs/' + token + '.json', persisted.read_bytes())}
                write(target, json_bytes(pointer))
                verb = 'ATTEMPTED'
            records.append(record)
            pointers.append(pointer)
            status()
            print(f'{verb} {job["source_reference"]}: {record["outcome"]}; {len(records)}/470' +
                  (' — ' + record['result']['error'] if 'error' in record['result'] else ''), flush=True)
        entries = original_entries + [entry_for(r, p['batch_root'], p['origin']) for r, p in zip(records, pointers) if r['result']['status'] == 'prepared']
        try:
            result = compose_current(runner, cache, issue, entries)
        except Exception as error:
            result = {'status': 'failed', 'error_type': type(error).__name__, 'error': str(error)}
        issues[issue] = result
        write(root / 'issues' / (issue + '.json'), json_bytes(result))
        status()
        print('CHECKPOINT ' + issue + ': ' + result['status'], flush=True)
    require(len(records) == 470 and {r['job_id'] for r in records} == retry_ids, 'Incomplete retry population')
    files = [file_record(p.relative_to(root).as_posix(), p.read_bytes()) for directory in ('outcomes', 'jobs', 'evidence', 'issues')
             for p in sorted((root / directory).rglob('*')) if p.is_file()]
    manifest = {'schema_version': 1, 'checkpoint': '14b', 'state': 'all_association_candidates_have_subsequent_outcomes',
                'identity': file_record('identity.json', (root / 'identity.json').read_bytes()), 'outputs': files,
                'retry_outcomes': histogram(r['outcome'] for r in records), 'origins': histogram(p['origin'] for p in pointers),
                'issue_states': histogram(i['status'] for i in issues.values()), 'issues': len(issues),
                'previous_prepared': 537, 'additional_prepared': sum(r['result']['status'] == 'prepared' for r in records)}
    write(root / 'manifest.json', json_bytes(manifest))
    print('COMPLETE execution: ' + str(root), flush=True)
    return root


if __name__ == '__main__':
    run()
