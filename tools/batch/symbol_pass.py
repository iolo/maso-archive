"""Integrate the two immutable Symbol samples into isolated 18c issue handoffs."""
from copy import copy
from pathlib import Path
import json

from tools.batch import font_declaration_pass as prior_pass, symbol_review
from tools.batch import retry_symbol_sample, retry_symbol_arrows, symbol_arrow_pipeline
from tools.batch.font_pass import table, overlay, merge_packages
from tools.batch.association_pass import histogram, entry_for, load_outcome
from tools.run_cd1_batch import ROOT, read_json
from tools.cd1_batch_cache import Cache, key, verify, write
from tools.decode_cd1_paragraph import digest
from tools.recover_cd1_text import json_bytes
from tools.map_cd1_topic import require
from tools.check_cd1_second_article import assemble
from maso_archive.reading_room_package import checked_file, file_record, load_package

OUTPUT = ROOT / 'build/cd1-symbol-pass'
PREVIOUS = symbol_review.CURRENT
SAMPLES = {'9210202': retry_symbol_sample.RECORD, '9208198': retry_symbol_arrows.RECORD}
DEFERRED = {'9205400a', '9205403'}


def runner():
    # No recovery is executed here. This loads and verifies the complete policy chain.
    return symbol_arrow_pipeline.ArrowRunner(OUTPUT)


def previous_records(current_runner, previous):
    historical = copy(current_runner)
    historical.identity = {k:v for k,v in current_runner.identity.items()
                           if k not in ('symbol_extension', 'symbol_arrow_extension')}
    require(previous['pipeline_identity_sha256'] == key(historical.identity), '17b pipeline changed')
    earlier = json.loads(checked_file(ROOT, previous['previous_record']))
    records, locations = prior_pass.previous_records(historical, earlier)
    manifest = json.loads(checked_file(ROOT, previous['execution_manifest']))
    jobs = {j['id']:j for j in current_runner.data['jobs']}
    retries = []
    for item in manifest['outputs']:
        if not item['path'].startswith('outcomes/'): continue
        pointer = json.loads(checked_file(ROOT / previous['run_root'], item))
        record = json.loads(checked_file(ROOT / pointer['checkpoint_root'], pointer['record']))
        job = jobs[record['job_id']]
        require(record['pipeline_identity_sha256'] == previous['pipeline_identity_sha256'], 'Historical retry pipeline changed')
        require(record['article_id'] == job['candidate_article_id'] and record['issue_id'] == job['issue_id'] and
                record['source_reference'] == job['source_reference'], 'Historical retry identity changed')
        require(checked_file(ROOT / pointer['checkpoint_root'], record['source_evidence']) == json_bytes(job), 'Historical source changed')
        retries.append(record); locations[record['job_id']] = pointer
    review = read_json(prior_pass.font_review.RECORD)
    review_root = ROOT / review['output_root']
    selected = prior_pass.select_reviewed_jobs(current_runner.data, read_json(review_root / 'jobs.json'),
                                              read_json(review_root / 'policy.json')['article_fonts'], records)
    eligible = {j['id'] for j in selected}
    require(len(retries) == len(eligible) == 6 and {r['job_id'] for r in retries} == eligible, '17b retry population changed')
    current = overlay(records, retries, eligible)
    require(histogram(r['outcome'] for r in current) == previous['counts']['current_outcomes'] and
            sum(r['result']['status'] == 'prepared' for r in current) == 988, '17b current population changed')
    return current, locations


def eligible_jobs(data, rows, previous):
    require(len(rows) == 4 and len({r['job_id'] for r in rows}) == 4 and
            {r['source_reference'] for r in rows} == set(symbol_review.CASES), 'Four-case Symbol review changed')
    jobs = {j['id']:j for j in data['jobs']}
    for row in rows:
        job = jobs[row['job_id']]
        require(row['source_reference'] == job['source_reference'] and row['source_topics'] == job['source_topics'] and
                row['status'] == symbol_review.CASES[row['source_reference']]['status'], 'Symbol review/source decision changed')
    selected = [j for j in data['jobs'] if j['source_reference'] in SAMPLES]
    eligible = {j['id'] for j in selected}
    old = [r for r in previous if r['job_id'] in eligible]
    require(len(selected) == len(old) == 2 and {j['source_reference'] for j in selected} == set(SAMPLES), 'Symbol integration scope changed')
    overlay(previous, old, eligible)
    return selected


def sample_pointer(sample, job, pipeline):
    ref = job['source_reference']; require(ref in SAMPLES, 'Unreviewed Symbol sample')
    checkpoint = '18a' if ref == '9210202' else '18b'
    require(sample['checkpoint'] == checkpoint and sample['pipeline_identity_sha256'] == pipeline and
            sample['review_record_sha256'] == digest(symbol_review.RECORD.read_bytes()) and
            set(sample['sample']) == {ref} and len(sample['jobs']) == 1 and
            sample['jobs'][0]['job_id'] == job['id'] and sample['jobs'][0]['result']['status'] == 'prepared' and
            sample['verification']['only_reviewed_source_bound_runs_changed'] and
            sample['verification']['source_boundaries_and_formatting_preserved'], 'Symbol sample gate changed')
    expected = [r for r in sample['checkpoint_outputs'] if r['path'] == 'jobs/' + job['id'].rsplit(':',1)[1] + '.json']
    require(len(expected) == 1, 'Sample checkpoint missing or duplicated')
    return {'origin':checkpoint, 'batch_root':sample['output_root'], 'checkpoint_root':sample['checkpoints_root'],
            'record':expected[0]}


def verified_samples(current_runner, jobs):
    pipelines = {'9208198':key(current_runner.identity), '9210202':key({k:v for k,v in current_runner.identity.items()
                                                                    if k != 'symbol_arrow_extension'})}
    result = {}
    for job in jobs:
        ref = job['source_reference']; sample = read_json(SAMPLES[ref])
        pointer = sample_pointer(sample, job, pipelines[ref])
        if ref == '9208198': require(sample['glyph_policy_sha256'] == key(current_runner.arrow_policy), 'Arrow policy changed')
        record = load_outcome(pointer, job, pipelines[ref])
        require(sample['jobs'][0] == {k:record[k] for k in ('job_id','outcome','result')}, 'Sample result changed')
        package = ROOT / pointer['batch_root'] / record['result']['package'] / 'content'
        actual = {ref+'/'+p.relative_to(package).as_posix():digest(p.read_bytes()) for p in package.rglob('*') if p.is_file()}
        require(actual == sample['runtime_files'], 'Sample runtime inventory changed')
        result[job['id']] = (record, pointer)
    return result


def execution_identity(current_runner):
    return {'pipeline_identity_sha256':key(current_runner.identity),
            'helpers':{Path(p).relative_to(ROOT).as_posix():digest(Path(p).read_bytes()) for p in
                       (__file__, prior_pass.__file__, ROOT/'tools/batch/font_pass.py', ROOT/'tools/batch/association_pass.py')},
            **{name:file_record(p.relative_to(ROOT).as_posix(),p.read_bytes()) for name,p in
               [('previous_record',PREVIOUS),('punctuation_sample',SAMPLES['9210202']),
                ('arrow_sample',SAMPLES['9208198']),('review_record',symbol_review.RECORD)]}}


def compose(current_runner, cache, previous, issue, additions):
    row = next(r for r in previous['issues'] if r['issue_id'] == issue)
    old_root = ROOT / previous['output_root'] / row['package']
    old_stage = verify(old_root, row['fingerprint'])
    inputs = {'previous_issue':row, 'previous_record_sha256':digest(PREVIOUS.read_bytes()), 'additions':additions}
    def produce(stage):
        if not additions:
            # The audited 17b content is copied byte for byte; the coverage audit
            # validates every old/new package independently before counting it.
            for item in old_stage['outputs']:
                if item['path'].startswith('content/'): write(stage/item['path'], checked_file(old_root,item))
            metadata = {'counts':row['counts'], 'article_ids':row['article_ids']}
        else:
            old, manifest, counts = load_package(old_root/'content')
            require(counts == row['counts'] and [a['id'] for a in old['articles']] == row['article_ids'], 'Historical issue changed')
            packages = [(old, manifest, old_root/'content')]
            for entry in additions:
                require(entry['result']['status'] == 'prepared' and entry['issue_id'] == issue, 'Unavailable or misplaced addition')
                root = ROOT / entry['batch_root'] / entry['result']['package']
                verify(root, entry['result']['stages']['package']['fingerprint'])
                bundle, manifest, _ = load_package(root/'content')
                require([a['id'] for a in bundle['articles']] == [entry['article_id']], 'Wrong Symbol article')
                packages.append((bundle,manifest,root/'content'))
            articles, media, assets, previews = merge_packages(packages, issue)
            bundle = current_runner.bundle(issue, articles, media)
            for name, raw in assemble(bundle, assets, previews).items(): write(stage/'content'/name,raw)
            actual, _, counts = load_package(stage/'content')
            require(actual['articles'] == articles, 'Composition changed article text')
            metadata = {'counts':counts, 'article_ids':[a['id'] for a in articles]}
        write(stage/'package-row.json',json_bytes(metadata))
        write(stage/'provenance.json',json_bytes(inputs))
    path, manifest = cache.stage('issue-'+issue,inputs,produce)
    return {'status':'prepared', 'package':path.relative_to(current_runner.output).as_posix(),
            'fingerprint':manifest['fingerprint'], **read_json(path/'package-row.json')}


def run():
    current_runner = runner(); previous = read_json(PREVIOUS)
    originals, _ = previous_records(current_runner, previous)
    jobs = eligible_jobs(current_runner.data, read_json(current_runner.review_root/'jobs.json'), originals)
    samples = verified_samples(current_runner, jobs)
    identity = execution_identity(current_runner); root = OUTPUT/'runs'/key(identity)
    if (root/'identity.json').exists(): require(read_json(root/'identity.json') == identity, 'Run identity changed')
    else: write(root/'identity.json',json_bytes(identity))
    cache = Cache(OUTPUT/'current-issues',identity); records=[]; pointers=[]; issues={}
    for job in jobs:
        record, pointer = samples[job['id']]; target = root/'outcomes'/(job['id'].rsplit(':',1)[1]+'.json')
        if target.exists(): require(read_json(target) == pointer, 'Resumed sample pointer changed')
        else: write(target,json_bytes(pointer))
        records.append(record); pointers.append(pointer)
        print('CARRIED '+job['source_reference']+': '+record['outcome'],flush=True)
    overlay(originals, records, {j['id'] for j in jobs})
    for issue in sorted({j['issue_id'] for j in current_runner.data['jobs']}):
        additions = [entry_for(r,p['batch_root'],p['origin']) for r,p in zip(records,pointers) if r['issue_id'] == issue]
        try: row = compose(current_runner,cache,previous,issue,additions)
        except Exception as error: row = {'status':'failed','error_type':type(error).__name__,'error':str(error)}
        issues[issue]=row; write(root/'issues'/(issue+'.json'),json_bytes(row))
        write(root/'status.json',json_bytes({'total':2,'new_candidates':0,'carried_sample':2,'recorded':len(records),
              'outcomes':histogram(r['outcome'] for r in records),'completed_issues':len(issues)}))
        print('CHECKPOINT '+issue+': '+row['status'],flush=True)
    files=[file_record(p.relative_to(root).as_posix(),p.read_bytes()) for directory in ('outcomes','issues')
           for p in sorted((root/directory).rglob('*')) if p.is_file()]
    require(len(issues) == 72 and all(r['status']=='prepared' for r in issues.values()), 'Issue integration incomplete')
    manifest={'schema_version':1,'checkpoint':'18c','state':'both_validated_Symbol_samples_carried',
              'identity':file_record('identity.json',(root/'identity.json').read_bytes()),'outputs':files,
              'retry_outcomes':histogram(r['outcome'] for r in records),'origins':histogram(p['origin'] for p in pointers),
              'issues':len(issues),'issue_states':histogram(r['status'] for r in issues.values()),
              'previous_prepared':988,'additional_prepared':2}
    write(root/'manifest.json',json_bytes(manifest)); print('COMPLETE '+str(root),flush=True)
    return root


if __name__ == '__main__': run()
