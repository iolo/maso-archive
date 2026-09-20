"""Audit both Symbol samples and 18c combined coverage against immutable 17b handoffs."""
import argparse
from pathlib import Path
import json

from tools.batch import symbol_pass as font_pass, symbol_review as font_review, symbol_arrows
from tools.batch import associations, report as first_report
from tools.batch.font_coverage import preserved_files
from tools.batch.association_coverage import qualify
from tools.batch.association_pass import histogram, load_outcome
from tools.run_cd1_batch import ROOT, read_json
from tools.cd1_batch_cache import Cache, key, verify, write
from tools.decode_cd1_paragraph import digest
from tools.recover_cd1_text import json_bytes
from tools.map_cd1_topic import require
from tools.validate_cd1_batch import check_topic
from tools import map_cd1_images as images
from maso_archive.reading_room_package import checked_file, file_record, load_package

RECORD = ROOT / 'data/catalog/batch-runs/cd1-symbol-pass.json'


def find_run(runner):
    identity = font_pass.execution_identity(runner)
    root = runner.output / 'runs' / key(identity)
    manifest = read_json(root/'manifest.json')
    require(json.loads(checked_file(root,manifest['identity'])) == identity, 'Symbol integration identity changed')
    return root


def build():
    runner=font_pass.runner();root=find_run(runner)
    manifest=read_json(root/'manifest.json')
    require(manifest['state']=='both_validated_Symbol_samples_carried','Font execution incomplete')
    outputs={r['path']:r for r in manifest['outputs']}
    actual={p.relative_to(root).as_posix() for d in ('outcomes','jobs','evidence','issues') for p in (root/d).rglob('*') if p.is_file()}
    require(len(outputs)==len(manifest['outputs']) and actual==set(outputs),'Font execution population changed')
    for item in manifest['outputs']:checked_file(root,item)
    previous=read_json(font_pass.PREVIOUS)
    originals,locations=font_pass.previous_records(runner,previous)
    jobs=font_pass.eligible_jobs(runner.data,read_json(runner.review_root/'jobs.json'),originals);eligible={j['id'] for j in jobs}
    samples=font_pass.verified_samples(runner,jobs)
    by_job={j['id']:j for j in runner.data['jobs']}
    retries,pointers=[],{}
    print('Verifying both Symbol samples and their distinct pipeline identities',flush=True)
    for job in jobs:
        pointer=read_json(root/'outcomes'/(job['id'].rsplit(':',1)[1]+'.json'))
        record,expected_pointer=samples[job['id']]
        require(pointer==expected_pointer,'Carried sample pointer differs')
        association=next(e for e in record['stage_evidence'] if e['path'].split('/')[-2].endswith('-association'))
        require(read_json(ROOT/pointer['batch_root']/association['path']/'association.json')==job,'Font retry changed association')
        retries.append(record);pointers[job['id']]=pointer
    require(manifest['retry_outcomes']==histogram(r['outcome'] for r in retries) and
            manifest['origins']==histogram(p['origin'] for p in pointers.values())=={'18a':1,'18b':1},'Font outcome/origin totals differ')
    current=font_pass.overlay(originals,retries,eligible);locations.update(pointers)
    source_checks=font_pass.table(previous,'source_checks')
    require(len(source_checks)==988,'Historical source audit population changed')
    prepared,media,assets,required_files,required_media={}, {}, {}, {}, {}
    def consume(package,bundle,manifest):
        for article in bundle['articles']:
            require(article['id'] not in prepared,'Duplicate prepared article')
            prepared[article['id']]=article
        for item in bundle['media']['items']:
            name=item['source']['resource']
            require(name not in media or media[name]==item,'Conflicting shared current media')
            media[name]=item
            if item['asset']:assets[name]=package/item['asset']['path']
        issue=bundle['issues'][0]['id']
        required_files.setdefault(issue,[]).extend(preserved_files(bundle,manifest))
        required_media.setdefault(issue,{}).update({m['id']:m for m in bundle['media']['items']})
    print('Validating all 72 previous handoffs and preserving their article payloads',flush=True)
    for n,row in enumerate(previous['issues'],1):
        path=ROOT/previous['output_root']/row['package'];verify(path,row['fingerprint'])
        bundle,old_manifest,counts=load_package(path/'content')
        require(counts==row['counts'] and [a['id'] for a in bundle['articles']]==row['article_ids'],'Historical handoff changed')
        require({a['issue_id'] for a in bundle['articles']}=={row['issue_id']},'Historical issue mismatch')
        consume(path/'content',bundle,old_manifest)
        if n%12==0:print(f'Verified {n}/72 historical issues',flush=True)
    require(len(prepared)==988,'Historical package article population differs')
    previous_topics=font_pass.table(previous,'topics')
    auxiliary_ids={r['id'] for r in previous_topics if r['state']=='auxiliary_text_recovered'}
    aux_root=ROOT/read_json(associations.RECORD)['output_root']
    aux_review={r['topic_id']:r for r in read_json(aux_root/'recoveries.json')}
    previous_media=font_pass.table(previous,'media')
    conversions={r['resource']:r['conversion'] for r in previous_media}
    print('Auditing invariant punctuation and reversible arrows against source bytes',flush=True)
    for record in retries:
        location=pointers[record['job_id']];batch=ROOT/location['batch_root'];result=record['result']
        for event in record['stage_evidence']:
            path=batch/event['path']
            if path.parent.name.startswith('media-'):
                resource=path.parent.name.removeprefix('media-');converted=read_json(path/'conversion.json')
                conversions[resource]={'status':read_json(path/'media.json')['status'],'concerns':converted.get('concerns',[]),
                    'error':converted.get('error'),'policy':converted.get('policy'),
                    'diagnostics':file_record((path/'conversion.json').relative_to(ROOT).as_posix(),(path/'conversion.json').read_bytes())}
        if result['status']!='prepared':continue
        job=by_job[record['job_id']]
        decoded=read_json(batch/result['stages']['recovery']['path']/'recovery.json')
        before=read_json(runner.prior_review_root/f'articles/{job["source_reference"]}/recovery.json')
        expected_topics=([symbol_arrows.expected_topic(t,runner.arrow_policy) for t in before['topics']]
                         if job['source_reference']=='9208198' else
                         [font_review.expected_topic(t,job['source_reference']) for t in before['topics']])
        require(decoded=={**before,'topics':expected_topics},'Retry changed more than reviewed source-bound runs')
        require([t['ordinal'] for t in decoded['topics']]==[s['native']['ordinal'] for s in job['source_topics']],'Retry topic population changed')
        checks=[(symbol_arrows.check_topic(runner.rtf,t,s['rtf'],runner.arrow_policy)
                 if job['source_reference']=='9208198' else check_topic(runner.rtf,t,s['rtf']))
                for t,s in zip(decoded['topics'],job['source_topics'])]
        sample=read_json(font_pass.SAMPLES[job['source_reference']])
        require(checks==sample['source_checks'][0]['source_checks'],'Carried source checks differ from sample')
        source_checks.append({'article_id':record['article_id'],'topics':checks})
        for aux in result['auxiliaries']:
            if aux['topic_id'] in aux_review:require(aux['recovery_status']==aux_review[aux['topic_id']]['status'],'Auxiliary disposition changed')
            if aux['recovery_status']=='recovered':
                ordinal=runner.topic_lookup[aux['topic_id']]['native']['ordinal']
                decoded_aux=read_json(batch/result['stages']['association']['path']/f'auxiliaries/{ordinal}/recovery.json')
                check_topic(runner.rtf,decoded_aux,aux['rtf'])
                if aux['topic_id'] in aux_review:require(decoded_aux==read_json(aux_root/f'topics/{ordinal}/recovery.json'),'Auxiliary text changed')
        path=batch/result['package'];verify(path,result['stages']['package']['fingerprint'])
        bundle,new_manifest,counts=load_package(path/'content')
        require(counts=={**result['counts'],'files':counts['files'],'assets':counts['assets'],'previews':counts['previews']},'Font standalone counts changed')
        require([a['id'] for a in bundle['articles']]==[record['article_id']] and bundle['articles'][0]['issue_id']==record['issue_id'] and bundle['articles'][0]['source']['reference']==job['source_reference'],'Wrong font article package')
        consume(path/'content',bundle,new_manifest)
    print('Validating all 72 current packages and exact preserved files',flush=True)
    issues=[]
    for n,issue in enumerate(sorted({j['issue_id'] for j in runner.data['jobs']}),1):
        row=read_json(root/'issues'/(issue+'.json'))
        require(row['status']=='prepared','Unresolved issue composition: '+issue)
        path=runner.output/row['package'];verify(path,row['fingerprint'])
        bundle,_,counts=load_package(path/'content')
        expected={a['id']:a for a in prepared.values() if a['issue_id']==issue}
        require({a['id']:a for a in bundle['articles']}==expected and len(bundle['articles'])==len(expected),'Current issue lost, duplicated or changed content')
        require(row['article_ids']==[a['id'] for a in bundle['articles']] and counts==row['counts'],'Current issue counts/order changed')
        for item in required_files[issue]:checked_file(path/'content',item)
        require({m['id']:m for m in bundle['media']['items']}==required_media[issue] and len(bundle['media']['items'])==len(required_media[issue]), 'Current issue media population changed')
        issues.append({'issue_id':issue,**row})
        if n%12==0:print(f'Verified {n}/72 current issues',flush=True)
    require(len(issues)==manifest['issues']==72 and manifest['issue_states']=={'prepared':72},'Current issue population differs')
    print('Checking all referenced media and available bitmap pixels',flush=True)
    media_rows=[];pixels=0
    for original in previous_media:
        name=original['resource'];raw=images.checked_source(name,runner.media_manifest);item=media.get(name)
        if item and item['status']=='available' and name.endswith(('.bmp','.dib')):
            source,converted=images.bitmap_pixels(images.RAW/name),images.bitmap_pixels(assets[name])
            require(all(source[k]==converted[k] for k in ('width','height','rgba_sha256')),'Bitmap differs: '+name);pixels+=1
        media_rows.append({'resource':name,'topic_ids':original['topic_ids'],'job_ids':original['job_ids'],
            'source':{'status':'verified','bytes':len(raw),'sha256':digest(raw)},'runtime_status':item['status'] if item else 'not_packaged',
            'runtime_record':item,'conversion':conversions.get(name)})
    qualified=[qualify(r,locations[r['job_id']]['batch_root'],locations[r['job_id']]['checkpoint_root']) for r in current]
    for record in qualified:
        checked_file(ROOT,record['source_evidence'])
        for item in record['failure_evidence']:checked_file(ROOT,item)
    data=first_report.reconcile(runner.data,qualified,prepared,auxiliary_ids,media_rows)
    historical_exceptions={e['job_id']:e for e in font_pass.table(previous,'exceptions')}
    font_rows={r['job_id']:r for r in read_json(runner.review_root/'jobs.json')}
    for e in data['exceptions']:
        require(e['job_id'] not in pointers,'Successful Symbol sample remained an exception')
        old=historical_exceptions[e['job_id']]
        for name in ('retry','font_review_status','font_declaration_review'):
            if name in old:e[name]=old[name]
        if e['job_id'] in font_rows:
            row=font_rows[e['job_id']]
            require(row['source_reference'] in font_pass.DEFERRED,'Unexpected Symbol exception')
            e['font_review_status']=row['status']
            e['symbol_review']={'status':row['status'],'source_reference':row['source_reference'],
                'record':file_record(font_review.RECORD.relative_to(ROOT).as_posix(),font_review.RECORD.read_bytes()),
                'approved_policy':False}
    deferred_ids={r['job_id'] for r in font_rows.values() if r['source_reference'] in font_pass.DEFERRED}
    require(len(deferred_ids)==2 and not (deferred_ids & eligible) and
            deferred_ids <= {e['job_id'] for e in data['exceptions']},'Symbol conflicts were retried or lost')
    issue_lookup={r['issue_id']:r for r in issues}
    for row in data['catalog']:
        row['origin']=locations[row['job_id']]['origin']
        row['current_issue_package']=(runner.output/issue_lookup[row['issue_id']]['package']).relative_to(ROOT).as_posix()
    before={r['job_id']:r for r in originals}
    data['retry_history']=[{'job_id':r['job_id'],'article_id':r['article_id'],'issue_id':r['issue_id'],
        'previous_outcome':before[r['job_id']]['outcome'],'previous_error':before[r['job_id']]['result'].get('error'),
        'subsequent_outcome':r['outcome'],'subsequent_error':r['result'].get('error'),
        'subsequent_category':first_report.exception_category(r['result']) if r['result']['status']!='prepared' else None,
        'checkpoint':pointers[r['job_id']]} for r in retries]
    data['declaration_font_retry_history']=font_pass.table(previous,'retry_history')
    data['ordinary_font_retry_history']=font_pass.table(previous,'ordinary_font_retry_history')
    data['font_retry_history']=font_pass.table(previous,'font_retry_history')
    data['association_retry_history']=font_pass.table(previous,'association_retry_history')
    data['issues'],data['source_checks']=issues,source_checks
    prior_topic={r['id']:r for r in previous_topics}
    for row in data['topics']:
        if 'auxiliary_recovery_status' in prior_topic[row['id']]:row['auxiliary_recovery_status']=prior_topic[row['id']]['auxiliary_recovery_status']
    new=[r for r in retries if pointers[r['job_id']]['origin']=='18c']
    counts={'candidates':len(current),'retry_candidates':len(retries),'new_attempts':len(new),'carried_sample':2,'deferred_font_candidates':40,
        'retry_outcomes':histogram(r['outcome'] for r in retries),'new_attempt_outcomes':histogram(r['outcome'] for r in new),
        'current_outcomes':histogram(r['outcome'] for r in current),'previous_prepared':988,
        'additional_prepared_since_17b':sum(r['result']['status']=='prepared' for r in retries),
        'new_prepared_in_18c':sum(r['result']['status']=='prepared' for r in new),'current_prepared':len(prepared),
        'issues':len(issues),'native_topics':len(data['topics']),'topic_states':histogram(r['state'] for r in data['topics']),
        'native_contexts':len(data['contexts']),'index_references':len(data['references']),'index_entries':len(data['entries']),
        'index_occurrences':sum(len(r['occurrence_ids']) for r in data['references']),'toc_entries':len(data['toc']),
        'toc_content_status':histogram(r['content_status'] for r in data['toc']),'toc_metadata_status':histogram(r['status'] for r in data['toc']),
        'prepared_without_toc_link':sum(not a['toc_entry_ids'] for a in prepared.values()),
        'unindexed_candidates':histogram(r['outcome'] for r in current if not by_job[r['job_id']]['index_references']),
        'unattributed_topics':len(data['unattributed']),'current_exception_categories':histogram(e['category'] for e in data['exceptions']),
        'retry_exception_categories':histogram(first_report.exception_category(r['result']) for r in retries if r['result']['status']!='prepared'),
        'source_media':len(media_rows),'runtime_media':histogram(r['runtime_status'] for r in media_rows),'pixel_equivalent_bitmaps':pixels,
        'paragraphs':sum(len(b['paragraphs']) for a in prepared.values() for s in a['sections'] for b in s['blocks']),
        'blocks':sum(len(s['blocks']) for a in prepared.values() for s in a['sections']),
        'source_bytes_accounted':sum(t['accounted_bytes'] for a in source_checks for t in a['topics']),
        'text_runs_accounted':sum(t['text_runs'] for a in source_checks for t in a['topics'])}
    require(len(source_checks)==len(prepared) and {a['article_id'] for a in source_checks}==set(prepared),'Source audit population differs')
    require(counts['current_prepared']==988+manifest['additional_prepared']==988+counts['additional_prepared_since_17b'],'Preparation gains differ')
    require((counts['candidates'],counts['retry_candidates'],counts['new_attempts'],counts['native_topics'],counts['native_contexts'],counts['toc_entries'],counts['source_media'])==
            (1088,2,0,3099,2103,5497,6165),'Source population differs')
    files={name+'.jsonl':b''.join(json.dumps(row,ensure_ascii=False,separators=(',',':')).encode()+b'\n' for row in rows) for name,rows in data.items()}
    summary={'schema_version':1,'checkpoint':'18c','scope':'both_validated_Symbol_samples_and_current_CD1_coverage',
        'pipeline_identity_sha256':key(runner.identity),'run_root':root.relative_to(ROOT).as_posix(),'output_root':runner.output.relative_to(ROOT).as_posix(),
        'counts':counts,'issues':issues,'previous_record':file_record(font_pass.PREVIOUS.relative_to(ROOT).as_posix(),font_pass.PREVIOUS.read_bytes()),
        'previous_execution_manifest':previous['execution_manifest'],
        'sample_records':{ref:file_record(p.relative_to(ROOT).as_posix(),p.read_bytes()) for ref,p in font_pass.SAMPLES.items()},
        'execution_manifest':file_record((root/'manifest.json').relative_to(ROOT).as_posix(),(root/'manifest.json').read_bytes()),
        'report_dependencies':{Path(p).relative_to(ROOT).as_posix():digest(Path(p).read_bytes()) for p in (__file__,font_pass.__file__,first_report.__file__,ROOT/'tools/batch/font_coverage.py',symbol_arrows.__file__,font_review.__file__)},
        'verification':{'both_sample_outcomes_and_runtime_inventories_verified':True,'all_72_previous_and_current_issue_packages_validated':True,
                        'new_standalone_packages_and_source_runs_checked':True,'only_reviewed_source_bound_runs_changed':True,
                        'article_preview_and_media_bytes_preserved':True,'unchanged_17b_source_audits_carried_forward':988,
                        'all_source_populations_reconciled':True,'physical_review':'pending'},
        'limits':['historical_handoffs_and_records_preserved','40_other_font_cases_deferred','remaining_failures_and_blockers_not_extracted',
                  'historical_intermediate_stage_audits_carried_forward','semantic_and_physical_review_pending','deferred_media_not_repaired']}
    return root,summary,files


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write-record',action='store_true');args=parser.parse_args()
    root,summary,files=build();cache=Cache(root/'reports',summary['report_dependencies'])
    def produce(stage):
        for name,raw in files.items():write(stage/name,raw)
    path,manifest=cache.stage('current-coverage',{'execution_manifest':summary['execution_manifest']},produce)
    first_report.verify_generated_coverage(path,manifest,files)
    summary.update(coverage_root=path.relative_to(ROOT).as_posix(),outputs=manifest['outputs'])
    if args.write_record:write(RECORD,json_bytes(summary))
    else:require(read_json(RECORD)==summary,'Current Symbol coverage differs from recorded result')
    print(json.dumps(summary['counts'],indent=2),flush=True)


if __name__=='__main__':main()
