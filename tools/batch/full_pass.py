"""Run the validated CD1 pipeline issue by issue with durable per-job outcomes."""
import argparse
from collections import Counter
from pathlib import Path
import shutil

from tools.run_cd1_batch import Runner, ROOT, OUTPUT, read_json, isolate, put
from tools.cd1_batch_core import inherited_states
from tools.cd1_batch_cache import key, verify, write
from tools.recover_cd1_text import json_bytes
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from tools.check_cd1_second_article import assemble
from maso_archive.reading_room_package import checked_file, file_record, load_package

SAMPLE_RECORD = ROOT / 'data/catalog/batch-runs/cd1-validation-sample.json'


def outcome(result):
    if result['status'] != 'prepared':
        require(result['status'] in ('blocked', 'failed'), 'Unknown job status')
        return result['status']
    review = (result.get('semantic_review') == 'pending' or result.get('deferred_media') or
              any(a.get('recovery_status') != 'recovered' or a.get('media') for a in result.get('auxiliaries', [])))
    return 'prepared_with_review_exceptions' if review else 'prepared'


def verify_job(root, batch_root, record, identity):
    require(record['pipeline_identity_sha256'] == identity, 'Stale job checkpoint')
    require(record['outcome'] == outcome(record['result']), 'Job outcome mismatch')
    checked_file(root, record['source_evidence'])
    for evidence in record['failure_evidence']:
        checked_file(root, evidence)
    for evidence in record['stage_evidence']:
        path = batch_root / evidence['path']
        require(path.is_relative_to(batch_root), 'Stage outside batch root')
        manifest = verify(path, evidence['fingerprint'])
        require(digest((path / 'checkpoint.json').read_bytes()) == evidence['checkpoint_sha256'], 'Stage checkpoint changed')
    if record['result']['status'] == 'prepared':
        bundle, _, _ = load_package(batch_root / record['result']['package'] / 'content')
        require([a['id'] for a in bundle['articles']] == [record['article_id']], 'Wrong article package')
    return record


def persist_job(root, runner, job, result, events):
    token = job['id'].rsplit(':', 1)[1]
    source_path = f'evidence/{token}/source-job.json'
    write(root / source_path, json_bytes(job))
    stages, failures = {}, []
    for event in events:
        if event['cache'] == 'failed':
            source = Path(event['evidence'])
            require(source.is_relative_to(runner.output), 'Failure evidence outside private batch output')
            for path in sorted(source.rglob('*')):
                if not path.is_file():
                    continue
                require(not path.is_symlink(), 'Symlink failure evidence')
                relative = f'evidence/{token}/{event["stage"]}/{path.relative_to(source).as_posix()}'
                raw = path.read_bytes()
                write(root / relative, raw)
                failures.append(file_record(relative, raw))
        else:
            path = runner.output / 'stages' / event['stage'] / event['fingerprint']
            verify(path, event['fingerprint'])
            stages[event['stage']] = {'path': path.relative_to(runner.output).as_posix(),
                                      'fingerprint': event['fingerprint'],
                                      'checkpoint_sha256': digest((path / 'checkpoint.json').read_bytes())}
    record = {'schema_version': 1, 'job_id': job['id'], 'article_id': job['candidate_article_id'],
              'source_reference': job['source_reference'], 'issue_id': job['issue_id'],
              'pipeline_identity_sha256': key(runner.identity), 'outcome': outcome(result), 'result': result,
              'source_evidence': file_record(source_path, json_bytes(job)),
              'stage_evidence': list(stages.values()), 'failure_evidence': failures,
              'stage_cache': dict(sorted(Counter(e['cache'] for e in events).items())),
              'retry': None if result['status'] == 'prepared' else
                       {'module': 'tools.run_cd1_batch', 'arguments': ['--article', job['id']],
                        'policy': 'retry in subsequent bounded work; preserve this first-pass outcome'}}
    verify_job(root, runner.output, record, key(runner.identity))
    write(root / 'jobs' / (token + '.json'), json_bytes(record))
    return record


def metadata_issue(runner, issue_id, jobs):
    bundle = runner.bundle(issue_id, [], [])
    def produce(stage):
        for name, raw in assemble(bundle, {}, []).items():
            write(stage / 'content' / name, raw)
        put(stage, 'provenance.json', {'issue_id': issue_id, 'availability': 'metadata_only',
                                    'candidate_job_ids': [j['id'] for j in jobs]})
    path, manifest = runner.cache.stage('issue-' + issue_id + '-metadata', {'jobs': jobs}, produce,
                                        lambda root: load_package(root / 'content'))
    return {'status': 'metadata_only', 'package': path.relative_to(runner.output).as_posix(),
            'fingerprint': manifest['fingerprint'], 'counts': load_package(path / 'content')[2]}


def run(output=OUTPUT):
    runner = Runner(output)
    identity = key(runner.identity)
    sample = read_json(SAMPLE_RECORD)
    require(sample['pipeline_identity_sha256'] == identity and sample['validation']['deterministic_all_stage_outputs'] and
            sample['validation']['nested_http']['files_fetched_and_checked'] > 0, '13c gate does not cover current extraction pipeline')
    root = runner.output / 'full-pass' / identity
    root.mkdir(parents=True, exist_ok=True)
    run_identity = {'schema_version': 1, 'pipeline_identity_sha256': identity, 'pipeline_identity': runner.identity,
                    'queue_manifest_sha256': digest((ROOT / 'build/cd1-processing-inventory/manifest.json').read_bytes()),
                    'sample_record': file_record(str(SAMPLE_RECORD.relative_to(ROOT)), SAMPLE_RECORD.read_bytes()),
                    'orchestrator': file_record(str(Path(__file__).resolve().relative_to(ROOT)), Path(__file__).read_bytes()),
                    'batch_root': runner.output.relative_to(ROOT).as_posix(), 'scope': 'all_cd1_candidates'}
    if (root / 'identity.json').exists():
        require(read_json(root / 'identity.json') == run_identity, 'First-pass orchestration changed; retain earlier run and review before resuming')
    else:
        write(root / 'identity.json', json_bytes(run_identity))
    jobs = runner.data['jobs']
    offsets = [t['rtf']['byte_offset'] for j in jobs if j['state'] != 'blocked' for t in j['source_topics']]
    offsets += [a['rtf']['byte_offset'] for a in runner.policy['auxiliaries'].values()]
    runner.states = inherited_states(runner.rtf, offsets)
    results, issues = [], {}
    def status(current=None):
        write(root / 'status.json', json_bytes({'total_jobs': len(jobs), 'recorded_jobs': len(results),
              'outcomes': dict(sorted(Counter(r['outcome'] for r in results).items())), 'current_job': current,
              'completed_issues': len(issues), 'total_issues': len({j['issue_id'] for j in jobs})}))
    for issue_id in sorted({j['issue_id'] for j in jobs}):
        issue_jobs = [j for j in jobs if j['issue_id'] == issue_id]
        print(f'ISSUE {issue_id}: {len(issue_jobs)} candidates', flush=True)
        for job in issue_jobs:
            path = root / 'jobs' / (job['id'].rsplit(':', 1)[1] + '.json')
            if path.exists():
                record = verify_job(root, runner.output, read_json(path), identity)
                require(json_bytes(job) == checked_file(root, record['source_evidence']), 'Job source evidence changed')
                print(f'RESUMED {job["source_reference"]}: {record["outcome"]}', flush=True)
            else:
                status(job['id'])
                begin = len(runner.cache.events)
                result = isolate([job], runner.process)[0]
                record = persist_job(root, runner, job, result, runner.cache.events[begin:])
                print(f'{len(results) + 1}/{len(jobs)} {job["source_reference"]}: {record["outcome"]}' +
                      (f' ({result["error"]})' if 'error' in result else ''), flush=True)
            results.append(record)
            status()
        try:
            issue = runner.compose(issue_id)
            if issue['status'] == 'no_prepared_articles':
                issue = metadata_issue(runner, issue_id, issue_jobs)
            bundle, _, counts = load_package(runner.output / issue['package'] / 'content')
            expected = {r['article_id'] for r in results if r['issue_id'] == issue_id and r['result']['status'] == 'prepared'}
            require({a['id'] for a in bundle['articles']} == expected, 'Issue composition does not match successful first-pass jobs')
            require(counts == issue['counts'], 'Issue counts changed')
        except Exception as error:
            issue = {'status': 'failed', 'error_type': type(error).__name__, 'error': str(error)}
        issues[issue_id] = issue
        write(root / 'issues' / (issue_id + '.json'), json_bytes(issue))
        status()
        print(f'CHECKPOINT {issue_id}: {issue["status"]}; {len(results)}/{len(jobs)} jobs recorded', flush=True)
    require({r['job_id'] for r in results} == {j['id'] for j in jobs} and len(results) == len(jobs), 'Incomplete/duplicate first-pass population')
    records = [file_record(p.relative_to(root).as_posix(), p.read_bytes()) for directory in ('jobs', 'issues', 'evidence')
               for p in sorted((root / directory).rglob('*')) if p.is_file()]
    manifest = {'schema_version': 1, 'checkpoint': '13d', 'state': 'all_candidates_attempted',
                'identity': file_record('identity.json', (root / 'identity.json').read_bytes()),
                'outcomes': dict(sorted(Counter(r['outcome'] for r in results).items())),
                'issue_states': dict(sorted(Counter(i['status'] for i in issues.values()).items())),
                'jobs': len(results), 'issues': len(issues), 'outputs': records}
    write(root / 'manifest.json', json_bytes(manifest))
    print('COMPLETE first-pass execution: ' + str(root), flush=True)
    return root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    run(args.output)


if __name__ == '__main__':
    main()
