"""Validate a fixed six-article retry sample against separately preserved auxiliaries."""
import argparse
from collections import Counter
from pathlib import Path
import json

from tools.batch import associations, full_pass
from tools.batch.full_pass import persist_job, verify_job, metadata_issue
from tools.run_cd1_batch import Runner, OUTPUT as FIRST_OUTPUT, ROOT, read_json, isolate
from tools.cd1_batch_core import inherited_states
from tools.cd1_batch_cache import Cache, key, verify, write
from tools.recover_cd1_text import json_bytes
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from tools.validate_cd1_batch import check_topic
from tools import map_cd1_images as images
from maso_archive.reading_room_package import checked_file, file_record, load_package

OUTPUT = ROOT / 'build/cd1-association-sample'
RECORD = ROOT / 'data/catalog/batch-runs/cd1-association-sample.json'
SAMPLE = {'9308449': 'leaf auxiliary', '9103252': 'auxiliary with outgoing series links',
          '9010234': 'mixed leaf and series auxiliaries', '9201335': 'deferred auxiliary 18',
          '9008224': 'deferred auxiliary 19 with series links', '9004200': 'shared auxiliary linked by 49 candidates'}


class AssociationRunner(Runner):
    def __init__(self, output=OUTPUT):
        require(not Path(output).resolve().is_relative_to(FIRST_OUTPUT), 'Retry output must be separate from first pass')
        super().__init__(output)
        first = read_json(associations.FIRST_PASS)
        require(key(self.identity) == first['pipeline_identity_sha256'], 'Original extraction pipeline changed')
        self.review = read_json(associations.RECORD)
        require(checked_file(ROOT, self.review['inputs']['first_pass']) == associations.FIRST_PASS.read_bytes(), 'First-pass record changed')
        require(self.review['inputs']['code_sha256'] == digest(Path(associations.__file__).read_bytes()), 'Association review implementation changed')
        self.review_root = ROOT / self.review['output_root']
        manifest = verify(self.review_root, self.review['fingerprint'])
        require(manifest['outputs'] == self.review['outputs'], 'Association review outputs changed')
        policy = read_json(self.review_root / 'policy.json')
        require(policy['source_rtf_sha256'] == digest(self.rtf), 'Auxiliary policy source changed')
        require(not (set(policy['auxiliaries']) & set(self.policy['auxiliaries'])), 'Policy attempts to replace a reviewed auxiliary')
        self.policy['auxiliaries'].update(policy['auxiliaries'])
        self.identity = {**self.identity, 'association_extension': {
            'review_record_sha256': digest(associations.RECORD.read_bytes()),
            'checkpoint_support_sha256': digest(Path(full_pass.__file__).read_bytes()),
            'implementation_sha256': digest(Path(__file__).read_bytes())}}
        self.cache = Cache(self.output / 'stages', self.identity)


def sample_jobs(data, retries):
    by_ref = {j['source_reference']: j for j in data['jobs']}
    ready = {r['job_id'] for r in retries if r['status'] == 'association_policy_ready'}
    jobs = [by_ref[ref] for ref in SAMPLE]
    require(all(j['id'] in ready for j in jobs), 'Sample includes a candidate outside reviewed association failures')
    return jobs


def run(write_record=False):
    runner = AssociationRunner()
    jobs = sample_jobs(runner.data, read_json(runner.review_root / 'retry-queue.json'))
    offsets = [t['rtf']['byte_offset'] for j in jobs for t in j['source_topics']]
    offsets += [a['rtf']['byte_offset'] for a in runner.policy['auxiliaries'].values()]
    runner.states = inherited_states(runner.rtf, offsets)
    root = runner.output / 'checkpoints' / key(runner.identity)
    records, checks, pixel_checks = [], [], set()
    by_aux = {r['topic_id']: r for r in read_json(runner.review_root / 'recoveries.json')}
    for job in jobs:
        path = root / 'jobs' / (job['id'].rsplit(':', 1)[1] + '.json')
        if path.exists():
            record = verify_job(root, runner.output, read_json(path), key(runner.identity))
            require(checked_file(root, record['source_evidence']) == json_bytes(job), 'Retry source job changed')
        else:
            begin = len(runner.cache.events)
            result = isolate([job], runner.process)[0]
            record = persist_job(root, runner, job, result, runner.cache.events[begin:])
        records.append(record)
        # Every candidate must pass the association stage even if a later source
        # construct prevents body preparation. Such failures remain explicit.
        associated = next((e for e in record['stage_evidence'] if e['path'].split('/')[-2].endswith('-association')), None)
        require(associated is not None, 'Reviewed association still fails: ' + job['source_reference'])
        require(read_json(runner.output / associated['path'] / 'association.json') == job, 'Association altered article boundaries')
        result = record['result']
        if result['status'] == 'prepared':
            recovered = read_json(runner.output / result['stages']['recovery']['path'] / 'recovery.json')
            require([t['ordinal'] for t in recovered['topics']] == [t['native']['ordinal'] for t in job['source_topics']], 'Auxiliary merged into article body')
            source_checks = [check_topic(runner.rtf, t, source['rtf']) for t, source in zip(recovered['topics'], job['source_topics'])]
            for aux in result['auxiliaries']:
                if aux['topic_id'] not in by_aux:
                    continue
                expected = by_aux[aux['topic_id']]
                require(aux['recovery_status'] == expected['status'], 'Auxiliary recovery disposition changed')
                if aux['recovery_status'] == 'recovered':
                    ordinal = runner.topic_lookup[aux['topic_id']]['native']['ordinal']
                    actual = read_json(runner.output / associated['path'] / f'auxiliaries/{ordinal}/recovery.json')
                    require(actual == read_json(runner.review_root / f'topics/{ordinal}/recovery.json'), 'Auxiliary decoded differently in retry')
                    check_topic(runner.rtf, actual, aux['rtf'])
            bundle, _, counts = load_package(runner.output / result['package'] / 'content')
            require([a['id'] for a in bundle['articles']] == [job['candidate_article_id']], 'Wrong retry article identity')
            for media in bundle['media']['items']:
                name = media['source']['resource']
                if media['status'] == 'available' and name.endswith(('.bmp', '.dib')):
                    original = images.bitmap_pixels(images.RAW / name)
                    converted = images.bitmap_pixels(runner.output / result['package'] / 'content' / media['asset']['path'])
                    require(all(original[k] == converted[k] for k in ('width', 'height', 'rgba_sha256')), 'Retry bitmap differs: ' + name)
                    pixel_checks.add(name)
            checks.append({'article_id': job['candidate_article_id'], 'source_checks': source_checks, 'counts': counts})
        print(job['source_reference'] + ': ' + record['outcome'], flush=True)
    issues = {issue: runner.compose(issue) for issue in sorted({j['issue_id'] for j in jobs})}
    for issue, result in issues.items():
        if result['status'] == 'no_prepared_articles':
            result = issues[issue] = metadata_issue(runner, issue, [j for j in jobs if j['issue_id'] == issue])
        require(result['status'] in ('prepared', 'metadata_only'), 'Sample issue did not compose: ' + issue)
        bundle, _, counts = load_package(runner.output / result['package'] / 'content')
        expected = {r['article_id'] for r in records if r['issue_id'] == issue and r['result']['status'] == 'prepared'}
        require({a['id'] for a in bundle['articles']} == expected and counts == result['counts'], 'Sample issue population changed')
    metadata = [file_record(p.relative_to(root).as_posix(), p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file()]
    summary = {'schema_version': 1, 'checkpoint': '14a', 'scope': 'fixed_association_retry_sample',
               'pipeline_identity_sha256': key(runner.identity), 'review_record_sha256': digest(associations.RECORD.read_bytes()),
               'output_root': runner.output.relative_to(ROOT).as_posix(), 'checkpoints_root': root.relative_to(ROOT).as_posix(),
               'sample': SAMPLE, 'outcomes': dict(sorted(Counter(r['outcome'] for r in records).items())),
               'jobs': [{'job_id': r['job_id'], 'outcome': r['outcome'], 'result': r['result']} for r in records],
               'source_checks': checks, 'issues': issues, 'checkpoint_outputs': metadata,
               'verification': {'all_selected_associations_passed': True, 'article_boundaries_unchanged': True,
                                'auxiliary_recovery_matches_separate_audit': True, 'pixel_equivalent_bitmaps': len(pixel_checks),
                                'physical_review': 'pending'},
               'limits': ['sample_only_issue_packages_do_not_replace_full_pass_handoffs', 'first_pass_history_unchanged',
                          'remaining_464_association_candidates_not_retried_here', 'deferred_media_not_repaired']}
    if write_record:
        write(RECORD, json_bytes(summary))
    else:
        require(read_json(RECORD) == summary, 'Retry sample differs from recorded result')
    print(json.dumps(summary['outcomes'], indent=2), flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-record', action='store_true')
    args = parser.parse_args()
    run(args.write_record)


if __name__ == '__main__':
    main()
