"""Execute exact-run OEM retries and integrate five articles into isolated 19b handoffs."""
from copy import copy
from pathlib import Path
import json

from tools.batch import symbol_pass as prior_pass, codec_review, oem_pipeline, retry_oem_sample
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

OUTPUT = ROOT / 'build/cd1-oem-pass'
PREVIOUS = codec_review.CURRENT
SAMPLE = retry_oem_sample.RECORD
NEW = {'8902178', '8903170'}


def runner():
    return oem_pipeline.OemRunner(OUTPUT)


def previous_records(current_runner, previous):
    historical = copy(current_runner)
    historical.identity = {k:v for k,v in current_runner.identity.items() if k != 'oem_run_extension'}
    require(previous['pipeline_identity_sha256'] == key(historical.identity), '18c pipeline changed')
    earlier = json.loads(checked_file(ROOT, previous['previous_record']))
    records, locations = prior_pass.previous_records(historical, earlier)
    jobs = prior_pass.eligible_jobs(historical.data, read_json(historical.review_root/'jobs.json'), records)
    samples = prior_pass.verified_samples(historical, jobs)
    manifest = json.loads(checked_file(ROOT, previous['execution_manifest']))
    retries = []
    for item in manifest['outputs']:
        if not item['path'].startswith('outcomes/'): continue
        pointer = json.loads(checked_file(ROOT / previous['run_root'], item))
        matches = [(job, samples[job['id']]) for job in jobs if samples[job['id']][1] == pointer]
        require(len(matches) == 1, 'Historical Symbol pointer changed')
        job, (record, _) = matches[0]
        retries.append(record); locations[job['id']] = pointer
    eligible = {j['id'] for j in jobs}
    require(len(retries) == 2 and {r['job_id'] for r in retries} == eligible, '18c retry population changed')
    current = overlay(records, retries, eligible)
    require(histogram(r['outcome'] for r in current) == previous['counts']['current_outcomes'] and
            sum(r['result']['status'] == 'prepared' for r in current) == 990, '18c current population changed')
    return current, locations


def eligible_jobs(data, rows, policies, previous):
    require(len(rows) == 37 and len({r['job_id'] for r in rows}) == 37 and
            len({r['source_reference'] for r in rows}) == 37, 'Codec review population changed')
    require(set(policies) == codec_review.READY, 'OEM policy scope changed')
    jobs = {j['id']:j for j in data['jobs']}
    for row in rows:
        ref = row['source_reference']; job = jobs[row['job_id']]
        expected = ('source_bound_oem_policy_ready' if ref in codec_review.READY else
                    'deferred_cross_font_character_representation' if ref in codec_review.SPLIT else
                    'deferred_mixed_or_ambiguous_source')
        require(row['status'] == expected and ref == job['source_reference'] and
                row['source_topics'] == job['source_topics'], 'Codec review/source decision changed')
        if ref in policies:
            require(policies[ref]['reference'] == ref and policies[ref]['source_topics'] == job['source_topics'],
                    'OEM policy source changed')
    selected = [j for j in data['jobs'] if j['source_reference'] in policies]
    eligible = {j['id'] for j in selected}; old = [r for r in previous if r['job_id'] in eligible]
    require(len(selected) == len(old) == 5 and
            {r['source_reference'] for r in rows if r['status']=='source_bound_oem_policy_ready'} == set(policies) and
            {r['source_reference'] for r in rows if r['status']=='deferred_cross_font_character_representation'} == codec_review.SPLIT,
            'OEM integration scope changed')
    overlay(previous, old, eligible)
    return selected


def sample_job_ids(sample, jobs, pipeline, policies):
    require(sample['checkpoint'] == '19a' and sample['pipeline_identity_sha256'] == pipeline and
            sample['review_record_sha256'] == digest(codec_review.RECORD.read_bytes()) and
            sample['run_policies_sha256'] == key(policies) and sample['sample'] == codec_review.SAMPLE and
            len(sample['jobs']) == 3 and all(r['result']['status']=='prepared' for r in sample['jobs']) and
            sample['verification']['only_reviewed_source_bound_runs_changed'] and
            sample['verification']['source_boundaries_and_formatting_preserved'], '19a sample gate changed')
    ids = {r['job_id'] for r in sample['jobs']}
    require(len(ids) == 3 and ids == {j['id'] for j in jobs if j['source_reference'] in codec_review.SAMPLE} and
            {j['source_reference'] for j in jobs if j['id'] not in ids} == NEW, 'Sample/new population differs')
    return ids


def verified_samples(current_runner, jobs):
    sample = read_json(SAMPLE); pipeline = key(current_runner.identity)
    ids = sample_job_ids(sample, jobs, pipeline, current_runner.oem_policies)
    result = {}; actual = {}
    for job in jobs:
        if job['id'] not in ids: continue
        ref = job['source_reference']; token = job['id'].rsplit(':',1)[1]
        expected = [r for r in sample['checkpoint_outputs'] if r['path']=='jobs/'+token+'.json']
        require(len(expected) == 1, 'Sample checkpoint missing or duplicated')
        pointer = {'origin':'19a','batch_root':sample['output_root'],
                   'checkpoint_root':sample['checkpoints_root'],'record':expected[0]}
        record = load_outcome(pointer, job, pipeline)
        require(next(r for r in sample['jobs'] if r['job_id']==job['id']) ==
                {k:record[k] for k in ('job_id','outcome','result')}, 'Sample result changed')
        package = ROOT / pointer['batch_root'] / record['result']['package'] / 'content'
        actual.update({ref+'/'+p.relative_to(package).as_posix():digest(p.read_bytes()) for p in package.rglob('*') if p.is_file()})
        result[job['id']] = (record,pointer)
    require(actual == sample['runtime_files'], 'Sample runtime inventory changed')
    return result


def execution_identity(current_runner):
    return {'pipeline_identity_sha256':key(current_runner.identity),
            'helpers':{Path(p).relative_to(ROOT).as_posix():digest(Path(p).read_bytes()) for p in
                       (__file__, prior_pass.__file__, ROOT/'tools/batch/font_pass.py',
                        ROOT/'tools/batch/association_pass.py', ROOT/'tools/batch/full_pass.py')},
            **{name:file_record(p.relative_to(ROOT).as_posix(),p.read_bytes()) for name,p in
               [('previous_record',PREVIOUS),('sample_record',SAMPLE),('review_record',codec_review.RECORD)]}}


def compose(current_runner, cache, previous, issue, additions):
    row = next(r for r in previous['issues'] if r['issue_id'] == issue)
    old_root = ROOT / previous['output_root'] / row['package']
    old_stage = verify(old_root, row['fingerprint'])
    inputs = {'previous_issue':row, 'previous_record_sha256':digest(PREVIOUS.read_bytes()), 'additions':additions}
    def produce(stage):
        if not additions:
            # The audited 18c content is copied byte for byte; the coverage audit
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
                require([a['id'] for a in bundle['articles']] == [entry['article_id']], 'Wrong OEM article')
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
    current_runner = runner(); previous = read_json(PREVIOUS); pipeline = key(current_runner.identity)
    originals, _ = previous_records(current_runner, previous)
    jobs = eligible_jobs(current_runner.data, read_json(current_runner.codec_review_root/'jobs.json'),
                         current_runner.oem_policies, originals)
    samples = verified_samples(current_runner, jobs)
    identity = execution_identity(current_runner); root = OUTPUT/'runs'/key(identity)
    if (root/'identity.json').exists(): require(read_json(root/'identity.json') == identity, 'Run identity changed')
    else: write(root/'identity.json',json_bytes(identity))
    cache = Cache(OUTPUT/'current-issues',identity); records=[]; pointers=[]; issues={}
    offsets = [t['rtf']['byte_offset'] for j in jobs if j['id'] not in samples for t in j['source_topics']]
    offsets += [a['rtf']['byte_offset'] for a in current_runner.policy['auxiliaries'].values()]
    current_runner.states = inherited_states(current_runner.rtf,offsets)
    def status():
        write(root/'status.json',json_bytes({'total':5,'new_candidates':2,'carried_sample':3,'recorded':len(records),
              'outcomes':histogram(r['outcome'] for r in records),'completed_issues':len(issues)}))
    for job in jobs:
        token = job['id'].rsplit(':',1)[1]; target = root/'outcomes'/(token+'.json')
        if job['id'] in samples:
            record,pointer = samples[job['id']]; verb='CARRIED'
            if target.exists(): require(read_json(target)==pointer, 'Resumed sample pointer changed')
            else: write(target,json_bytes(pointer))
        elif target.exists():
            pointer=read_json(target)
            require(pointer['origin']=='19b' and pointer['batch_root']==OUTPUT.relative_to(ROOT).as_posix() and
                    pointer['checkpoint_root']==root.relative_to(ROOT).as_posix(), 'Resumed retry origin changed')
            record=load_outcome(pointer,job,pipeline);verb='RESUMED'
        else:
            persisted=root/'jobs'/(token+'.json')
            if persisted.exists():
                record=verify_job(root,OUTPUT,read_json(persisted),pipeline)
                require(checked_file(root,record['source_evidence'])==json_bytes(job),'Interrupted retry source changed')
            else:
                begin=len(current_runner.cache.events);result=isolate([job],current_runner.process)[0]
                record=persist_job(root,current_runner,job,result,current_runner.cache.events[begin:])
            pointer={'origin':'19b','batch_root':OUTPUT.relative_to(ROOT).as_posix(),'checkpoint_root':root.relative_to(ROOT).as_posix(),
                     'record':file_record('jobs/'+token+'.json',persisted.read_bytes())}
            write(target,json_bytes(pointer));verb='ATTEMPTED'
        records.append(record);pointers.append(pointer);status()
        print(verb+' '+job['source_reference']+': '+record['outcome'],flush=True)
    require(len(records)==5 and {r['job_id'] for r in records}=={j['id'] for j in jobs},'Incomplete OEM retry population')
    overlay(originals, records, {j['id'] for j in jobs})
    for issue in sorted({j['issue_id'] for j in current_runner.data['jobs']}):
        additions = [entry_for(r,p['batch_root'],p['origin']) for r,p in zip(records,pointers)
                     if r['issue_id'] == issue and r['result']['status']=='prepared']
        try: row = compose(current_runner,cache,previous,issue,additions)
        except Exception as error: row = {'status':'failed','error_type':type(error).__name__,'error':str(error)}
        issues[issue]=row; write(root/'issues'/(issue+'.json'),json_bytes(row)); status()
        print('CHECKPOINT '+issue+': '+row['status'],flush=True)
    files=[file_record(p.relative_to(root).as_posix(),p.read_bytes()) for directory in ('outcomes','jobs','evidence','issues')
           for p in sorted((root/directory).rglob('*')) if p.is_file()]
    require(len(issues)==72 and all(r['status']=='prepared' for r in issues.values()), 'Issue integration incomplete')
    manifest={'schema_version':1,'checkpoint':'19b','state':'all_five_reviewed_OEM_candidates_have_subsequent_outcomes',
              'identity':file_record('identity.json',(root/'identity.json').read_bytes()),'outputs':files,
              'retry_outcomes':histogram(r['outcome'] for r in records),'origins':histogram(p['origin'] for p in pointers),
              'issues':len(issues),'issue_states':histogram(r['status'] for r in issues.values()),
              'previous_prepared':990,'additional_prepared':sum(r['result']['status']=='prepared' for r in records)}
    write(root/'manifest.json',json_bytes(manifest)); print('COMPLETE '+str(root),flush=True)
    return root


if __name__ == '__main__': run()
