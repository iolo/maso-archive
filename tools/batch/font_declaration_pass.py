"""Execute 17b font-declaration retries and combine immutable 16b issue handoffs."""
from pathlib import Path
from copy import copy
import json

from tools.batch import font_declaration_review as font_review, retry_font_declarations as retry_fonts
from tools.batch import ordinary_font_pass as prior_pass, association_pass, association_coverage
from tools.batch.font_pass import table, overlay, merge_packages
from tools.batch.association_pass import histogram, entry_for, load_outcome
from tools.batch.full_pass import persist_job, verify_job
from tools.run_cd1_batch import ROOT, read_json, isolate
from tools.cd1_batch_cache import Cache, key, verify, write
from tools.cd1_batch_core import inherited_states
from tools.decode_cd1_paragraph import digest
from tools.recover_cd1_text import json_bytes
from tools.map_cd1_topic import require
from tools.check_cd1_second_article import assemble
from maso_archive.reading_room_package import checked_file, file_record, load_package

OUTPUT = ROOT / 'build/cd1-font-declaration-pass'
PREVIOUS = font_review.CURRENT


def previous_records(runner, previous):
    """Carry verified outcomes through 16b without changing historical identities."""
    historical = copy(runner)
    historical.identity = {k: v for k, v in runner.identity.items() if k != 'font_declaration_extension'}
    require(previous['pipeline_identity_sha256'] == key(historical.identity), '16b pipeline changed')
    earlier = json.loads(checked_file(ROOT, previous['previous_record']))
    records, locations = prior_pass.previous_records(historical, earlier)
    manifest = json.loads(checked_file(ROOT, previous['execution_manifest']))
    jobs = {j['id']: j for j in runner.data['jobs']}
    retries = []
    for item in manifest['outputs']:
        if not item['path'].startswith('outcomes/'): continue
        pointer = json.loads(checked_file(ROOT / previous['run_root'], item))
        record = json.loads(checked_file(ROOT / pointer['checkpoint_root'], pointer['record']))
        job = jobs[record['job_id']]
        require(record['pipeline_identity_sha256'] == previous['pipeline_identity_sha256'], 'Historical retry pipeline changed')
        require(record['article_id'] == job['candidate_article_id'] and record['issue_id'] == job['issue_id'] and
                record['source_reference'] == job['source_reference'], 'Historical retry identity changed')
        require(checked_file(ROOT / pointer['checkpoint_root'], record['source_evidence']) == json_bytes(job), 'Historical retry source changed')
        retries.append(record); locations[record['job_id']] = pointer
    review = read_json(prior_pass.font_review.RECORD)
    review_root = ROOT / review['output_root']
    selected = prior_pass.select_reviewed_jobs(runner.data, read_json(review_root / 'jobs.json'),
                                              read_json(review_root / 'policy.json')['article_fonts'], records)
    eligible = {j['id'] for j in selected}
    require(len(retries) == len(eligible) == 5 and {r['job_id'] for r in retries} == eligible, 'Historical ordinary-font retry population changed')
    current = overlay(records, retries, eligible)
    require(histogram(r['outcome'] for r in current) == previous['counts']['current_outcomes'] and
            sum(r['result']['status'] == 'prepared' for r in current) == 982, '16b current population changed')
    return current, locations


def select_reviewed_jobs(data, rows, policy, previous):
    require(len(rows) == 7 and len({r['job_id'] for r in rows}) == 7 and
            {r['source_reference'] for r in rows} == set(font_review.CASES), 'Seven-case review population changed')
    for row in rows:
        expected = 'source_bound_font_policy_ready' if row['source_reference'] in font_review.READY else 'deferred_ambiguous_source_byte'
        require(row['status'] == expected, 'Reviewed declaration decision changed')
    eligible = {r['job_id'] for r in rows if r['source_reference'] in font_review.READY}
    jobs = [j for j in data['jobs'] if j['id'] in eligible]
    selected = [r for r in previous if r['job_id'] in eligible]
    overlay(previous, selected, eligible)
    require(len(eligible) == len(jobs) == len(selected) == 6 and
            {j['source_reference'] for j in jobs} == set(policy) == font_review.READY, 'Declaration policy/job population differs')
    for job in jobs:
        row = next(r for r in rows if r['job_id'] == job['id'])
        extra = policy[job['source_reference']]
        require(row['source_reference'] == job['source_reference'] and
                row['source_topics'] == extra['source_topics'] == job['source_topics'], 'Reviewed source association changed')
        require(extra['font_codecs'] == font_review.CASES[job['source_reference']]['font_codecs'], 'Unreviewed declaration codec')
    return jobs


def eligible_jobs(runner, previous):
    return select_reviewed_jobs(runner.data, read_json(runner.review_root / 'jobs.json'),
                                read_json(runner.review_root / 'policy.json')['article_fonts'], previous)


def sample_job_ids(sample, jobs, pipeline):
    require(sample['pipeline_identity_sha256'] == pipeline and
            sample['review_record_sha256'] == digest(font_review.RECORD.read_bytes()) and
            sample['sample'] == font_review.SAMPLE and len(sample['jobs']) == 5 and
            all(r['result']['status'] == 'prepared' for r in sample['jobs']) and
            sample['verification']['only_reviewed_source_bound_runs_changed'], '17a gate does not cover this run')
    ids = {r['job_id'] for r in sample['jobs']}
    require(len(ids) == 5 and ids == {j['id'] for j in jobs if j['source_reference'] in font_review.SAMPLE} and
            {j['source_reference'] for j in jobs if j['id'] not in ids} == {'9306300'}, 'Sample/new population differs')
    return ids


def compose(runner, cache, previous, issue, additions):
    row = next(r for r in previous['issues'] if r['issue_id']==issue)
    old_root = ROOT / previous['output_root'] / row['package']
    verify(old_root, row['fingerprint'])
    old, manifest, counts = load_package(old_root / 'content')
    require(counts==row['counts'] and [a['id'] for a in old['articles']]==row['article_ids'], 'Historical issue changed')
    packages = [(old,manifest,old_root/'content')]
    inputs = {'previous_issue':row, 'previous_record_sha256':digest(PREVIOUS.read_bytes()), 'additions':additions}
    for entry in additions:
        require(entry['result']['status']=='prepared' and entry['issue_id']==issue, 'Unavailable or misplaced addition')
        root = ROOT / entry['batch_root'] / entry['result']['package']
        verify(root,entry['result']['stages']['package']['fingerprint'])
        bundle,manifest,_ = load_package(root/'content')
        require([a['id'] for a in bundle['articles']]==[entry['article_id']], 'Wrong retry article')
        packages.append((bundle,manifest,root/'content'))
    articles,media,assets,previews = merge_packages(packages,issue)
    bundle = runner.bundle(issue,articles,media)
    def produce(stage):
        for name,raw in assemble(bundle,assets,previews).items(): write(stage/'content'/name,raw)
        write(stage/'provenance.json',json_bytes(inputs))
    path,manifest = cache.stage('issue-'+issue,inputs,produce,lambda p:load_package(p/'content'))
    actual,_,counts = load_package(path/'content')
    require(actual['articles']==articles, 'Composition changed article content')
    return {'status':'prepared','package':path.relative_to(runner.output).as_posix(), 'fingerprint':manifest['fingerprint'],
            'counts':counts,'article_ids':[a['id'] for a in articles]}


def run():
    runner = retry_fonts.DeclarationFontRunner(OUTPUT)
    previous, sample = read_json(PREVIOUS), read_json(retry_fonts.RECORD)
    pipeline = key(runner.identity)
    originals,_ = previous_records(runner,previous)
    jobs = eligible_jobs(runner,originals)
    sample_ids = sample_job_ids(sample, jobs, pipeline)
    identity = {'pipeline_identity_sha256':pipeline,'orchestrator_sha256':digest(Path(__file__).read_bytes()),
                'historical_helper_sha256':digest(Path(association_coverage.__file__).read_bytes()),
                'checkpoint_helper_sha256':digest(Path(association_pass.__file__).read_bytes()),
                'prior_pass_helper_sha256':digest(Path(prior_pass.__file__).read_bytes()),
                **{k:file_record(p.relative_to(ROOT).as_posix(),p.read_bytes()) for k,p in
                   [('previous_record',PREVIOUS),('sample_record',retry_fonts.RECORD),('review_record',font_review.RECORD)]}}
    root = OUTPUT/'runs'/key(identity)
    if (root/'identity.json').exists(): require(read_json(root/'identity.json')==identity, 'Run identity changed')
    else: write(root/'identity.json',json_bytes(identity))
    cache = Cache(OUTPUT/'current-issues',identity)
    offsets = [t['rtf']['byte_offset'] for j in jobs for t in j['source_topics']]
    offsets += [a['rtf']['byte_offset'] for a in runner.policy['auxiliaries'].values()]
    runner.states = inherited_states(runner.rtf,offsets)
    records,pointers,issues = [],[],{}
    def status():
        write(root/'status.json',json_bytes({'total':6,'new_candidates':1,'carried_sample':5,'recorded':len(records),
              'outcomes':histogram(r['outcome'] for r in records),'completed_issues':len(issues)}))
    for issue in sorted({j['issue_id'] for j in runner.data['jobs']}):
        for job in [j for j in jobs if j['issue_id']==issue]:
            token = job['id'].rsplit(':',1)[1]; target = root/'outcomes'/(token+'.json')
            if target.exists():
                pointer = read_json(target); record = load_outcome(pointer,job,pipeline); verb='RESUMED'
            elif job['id'] in sample_ids:
                expected = next(r for r in sample['checkpoint_outputs'] if r['path']=='jobs/'+token+'.json')
                pointer = {'origin':'17a','batch_root':sample['output_root'],'checkpoint_root':sample['checkpoints_root'],'record':expected}
                record = load_outcome(pointer,job,pipeline); write(target,json_bytes(pointer)); verb='CARRIED'
            else:
                persisted = root/'jobs'/(token+'.json')
                if persisted.exists():
                    record = verify_job(root,OUTPUT,read_json(persisted),pipeline)
                    require(checked_file(root,record['source_evidence'])==json_bytes(job),'Interrupted retry source changed')
                else:
                    begin=len(runner.cache.events);result=isolate([job],runner.process)[0]
                    record=persist_job(root,runner,job,result,runner.cache.events[begin:])
                pointer={'origin':'17b','batch_root':OUTPUT.relative_to(ROOT).as_posix(),'checkpoint_root':root.relative_to(ROOT).as_posix(),
                         'record':file_record('jobs/'+token+'.json',persisted.read_bytes())}
                write(target,json_bytes(pointer));verb='ATTEMPTED'
            records.append(record);pointers.append(pointer);status()
            print(f'{verb} {job["source_reference"]}: {record["outcome"]}; {len(records)}/6',flush=True)
        additions=[entry_for(r,p['batch_root'],p['origin']) for r,p in zip(records,pointers) if r['issue_id']==issue and r['result']['status']=='prepared']
        try: row=compose(runner,cache,previous,issue,additions)
        except Exception as error: row={'status':'failed','error_type':type(error).__name__,'error':str(error)}
        issues[issue]=row;write(root/'issues'/(issue+'.json'),json_bytes(row));status()
        print('CHECKPOINT '+issue+': '+row['status'],flush=True)
    require(len(records)==6 and {r['job_id'] for r in records}=={j['id'] for j in jobs},'Incomplete font retry population')
    overlay(originals,records,{j['id'] for j in jobs})
    files=[file_record(p.relative_to(root).as_posix(),p.read_bytes()) for directory in ('outcomes','jobs','evidence','issues')
           for p in sorted((root/directory).rglob('*')) if p.is_file()]
    manifest={'schema_version':1,'checkpoint':'17b','state':'all_eligible_font_candidates_have_subsequent_outcomes',
              'identity':file_record('identity.json',(root/'identity.json').read_bytes()),'outputs':files,
              'retry_outcomes':histogram(r['outcome'] for r in records),'origins':histogram(p['origin'] for p in pointers),
              'issues':len(issues),'issue_states':histogram(r['status'] for r in issues.values()),'previous_prepared':982,
              'additional_prepared':sum(r['result']['status']=='prepared' for r in records)}
    write(root/'manifest.json',json_bytes(manifest));print('COMPLETE '+str(root),flush=True)
    return root


if __name__=='__main__': run()
