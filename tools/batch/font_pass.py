"""Execute 15b font retries and combine them with the immutable 14b issue handoffs."""
from pathlib import Path
import json

from tools.batch import font_review, retry_fonts, associations, association_pass, association_coverage
from tools.batch.association_pass import histogram, entry_for, load_outcome, first_records
from tools.batch.full_pass import persist_job, verify_job
from tools.batch.report import exception_category
from tools.run_cd1_batch import ROOT, read_json, isolate
from tools.cd1_batch_cache import Cache, key, verify, write
from tools.cd1_batch_core import inherited_states
from tools.decode_cd1_paragraph import digest
from tools.recover_cd1_text import json_bytes
from tools.map_cd1_topic import require
from tools.check_cd1_second_article import assemble
from maso_archive.reading_room_package import checked_file, file_record, load_package

OUTPUT = ROOT / 'build/cd1-font-pass'
PREVIOUS = font_review.CURRENT


def table(summary, name):
    record = next(r for r in summary['outputs'] if r['path'] == name + '.jsonl')
    return [json.loads(line) for line in checked_file(ROOT / summary['coverage_root'], record).splitlines()]


def previous_records(runner, previous):
    """Read source-bound historical checkpoints; detailed source audits carry forward."""
    first = json.loads(checked_file(ROOT, previous['first_pass_record']))
    originals = first_records(runner, first)
    locations = {r['job_id']: {'origin':'13d', 'batch_root':'build/cd1-batch', 'checkpoint_root':first['run_root']} for r in originals}
    manifest = json.loads(checked_file(ROOT, previous['execution_manifest']))
    files = {r['path']:r for r in manifest['outputs']}
    jobs = {j['id']:j for j in runner.data['jobs']}
    retries = []
    for path in sorted(p for p in files if p.startswith('outcomes/')):
        pointer = json.loads(checked_file(ROOT / previous['run_root'], files[path]))
        record = json.loads(checked_file(ROOT / pointer['checkpoint_root'], pointer['record']))
        require(checked_file(ROOT / pointer['checkpoint_root'], record['source_evidence']) == json_bytes(jobs[record['job_id']]), 'Historical source job changed')
        retries.append(record); locations[record['job_id']] = pointer
    require(len(retries) == 470, 'Historical association population changed')
    records = association_coverage.current_records(originals, retries)
    require(histogram(r['outcome'] for r in records) == previous['counts']['current_outcomes'] and
            sum(r['result']['status']=='prepared' for r in records) == 944, 'Historical current population changed')
    return records, locations


def overlay(previous, retries, eligible):
    records = {r['job_id']:r for r in previous}
    require(len(records) == len(previous), 'Duplicate previous job')
    require(len({r['job_id'] for r in retries}) == len(retries), 'Duplicate font retry')
    for r in retries:
        require(r['job_id'] in eligible and r['job_id'] in records, 'Retry outside reviewed font scope')
        old = records[r['job_id']]
        require(old['result']['status']=='failed' and exception_category(old['result'])=='font_or_decoding_policy', 'Font retry replaces unrelated outcome')
        require(all(old[k]==r[k] for k in ('article_id','issue_id','source_reference')), 'Font retry identity changed')
        records[r['job_id']] = r
    return [records[r['job_id']] for r in previous]


def eligible_jobs(runner, previous):
    rows = read_json(runner.review_root / 'jobs.json')
    eligible = {r['job_id'] for r in rows if r['status']=='ascii_policy_ready'}
    require(len(rows)==86 and len(eligible)==33 and sum(r['status']=='deferred' for r in rows)==53, 'Reviewed font scope changed')
    jobs = [j for j in runner.data['jobs'] if j['id'] in eligible]
    selected = [r for r in previous if r['job_id'] in eligible]
    overlay(previous, selected, eligible)
    require(len(jobs)==len(selected)==33 and {j['source_reference'] for j in jobs} == set(read_json(runner.review_root/'policy.json')['article_fonts']), 'Font policy/job population differs')
    return jobs


def merge_packages(packages, issue_id):
    articles, media, assets, previews = {}, {}, {}, []
    for bundle, manifest, root in packages:
        for article in bundle['articles']:
            require(article['issue_id']==issue_id and article['id'] not in articles, 'Duplicate or wrong-issue article')
            articles[article['id']] = article
        for item in bundle['media']['items']:
            require(item['id'] not in media or media[item['id']]==item, 'Conflicting shared media')
            media[item['id']] = item
            if item['asset']:
                name = item['asset']['path']; raw = checked_file(root, item['asset'])
                require(name not in assets or assets[name]==raw, 'Conflicting asset bytes')
                assets[name] = raw
        previews.extend((p['article_id'],p['section_id'],p['path'],checked_file(root,p)) for p in manifest['previews'])
    return [articles[k] for k in sorted(articles)], [media[k] for k in sorted(media)], assets, previews


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
    runner = retry_fonts.FontRunner(OUTPUT)
    previous, sample = read_json(PREVIOUS), read_json(retry_fonts.RECORD)
    pipeline = key(runner.identity)
    require(sample['pipeline_identity_sha256']==pipeline and sample['review_record_sha256']==digest(font_review.RECORD.read_bytes()) and
            len(sample['jobs'])==6 and all(r['result']['status']=='prepared' for r in sample['jobs']) and sample['verification']['only_reviewed_ASCII_runs_changed'], '15a gate does not cover this run')
    originals,_ = previous_records(runner,previous)
    jobs = eligible_jobs(runner,originals)
    sample_ids = {r['job_id'] for r in sample['jobs']}
    require(sample_ids <= {j['id'] for j in jobs} and len(jobs)-len(sample_ids)==27, 'Sample/new population differs')
    identity = {'pipeline_identity_sha256':pipeline,'orchestrator_sha256':digest(Path(__file__).read_bytes()),
                'historical_helper_sha256':digest(Path(association_coverage.__file__).read_bytes()),
                'checkpoint_helper_sha256':digest(Path(association_pass.__file__).read_bytes()),
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
        write(root/'status.json',json_bytes({'total':33,'new_candidates':27,'carried_sample':6,'recorded':len(records),
              'outcomes':histogram(r['outcome'] for r in records),'completed_issues':len(issues)}))
    for issue in sorted({j['issue_id'] for j in runner.data['jobs']}):
        for job in [j for j in jobs if j['issue_id']==issue]:
            token = job['id'].rsplit(':',1)[1]; target = root/'outcomes'/(token+'.json')
            if target.exists():
                pointer = read_json(target); record = load_outcome(pointer,job,pipeline); verb='RESUMED'
            elif job['id'] in sample_ids:
                expected = next(r for r in sample['checkpoint_outputs'] if r['path']=='jobs/'+token+'.json')
                pointer = {'origin':'15a','batch_root':sample['output_root'],'checkpoint_root':sample['checkpoints_root'],'record':expected}
                record = load_outcome(pointer,job,pipeline); write(target,json_bytes(pointer)); verb='CARRIED'
            else:
                persisted = root/'jobs'/(token+'.json')
                if persisted.exists():
                    record = verify_job(root,OUTPUT,read_json(persisted),pipeline)
                    require(checked_file(root,record['source_evidence'])==json_bytes(job),'Interrupted retry source changed')
                else:
                    begin=len(runner.cache.events);result=isolate([job],runner.process)[0]
                    record=persist_job(root,runner,job,result,runner.cache.events[begin:])
                pointer={'origin':'15b','batch_root':OUTPUT.relative_to(ROOT).as_posix(),'checkpoint_root':root.relative_to(ROOT).as_posix(),
                         'record':file_record('jobs/'+token+'.json',persisted.read_bytes())}
                write(target,json_bytes(pointer));verb='ATTEMPTED'
            records.append(record);pointers.append(pointer);status()
            print(f'{verb} {job["source_reference"]}: {record["outcome"]}; {len(records)}/33',flush=True)
        additions=[entry_for(r,p['batch_root'],p['origin']) for r,p in zip(records,pointers) if r['issue_id']==issue and r['result']['status']=='prepared']
        try: row=compose(runner,cache,previous,issue,additions)
        except Exception as error: row={'status':'failed','error_type':type(error).__name__,'error':str(error)}
        issues[issue]=row;write(root/'issues'/(issue+'.json'),json_bytes(row));status()
        print('CHECKPOINT '+issue+': '+row['status'],flush=True)
    require(len(records)==33 and {r['job_id'] for r in records}=={j['id'] for j in jobs},'Incomplete font retry population')
    overlay(originals,records,{j['id'] for j in jobs})
    files=[file_record(p.relative_to(root).as_posix(),p.read_bytes()) for directory in ('outcomes','jobs','evidence','issues')
           for p in sorted((root/directory).rglob('*')) if p.is_file()]
    manifest={'schema_version':1,'checkpoint':'15b','state':'all_eligible_font_candidates_have_subsequent_outcomes',
              'identity':file_record('identity.json',(root/'identity.json').read_bytes()),'outputs':files,
              'retry_outcomes':histogram(r['outcome'] for r in records),'origins':histogram(p['origin'] for p in pointers),
              'issues':len(issues),'issue_states':histogram(r['status'] for r in issues.values()),'previous_prepared':944,
              'additional_prepared':sum(r['result']['status']=='prepared' for r in records)}
    write(root/'manifest.json',json_bytes(manifest));print('COMPLETE '+str(root),flush=True)
    return root


if __name__=='__main__': run()
