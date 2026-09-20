"""Validate the source-bound reversible arrow recovery for CD1 9208198."""
import argparse
from pathlib import Path
from collections import Counter
import json
import tempfile

from tools.batch import symbol_arrows, symbol_arrow_pipeline, retry_associations
from tools.batch import symbol_review as font_review
from tools.batch.full_pass import persist_job, verify_job
from tools.run_cd1_batch import ROOT, read_json, isolate
from tools.cd1_batch_core import inherited_states
from tools.cd1_batch_cache import Cache, key, verify, write
from tools.recover_cd1_text import json_bytes
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from tools import map_cd1_images as images
from maso_archive.reading_room_package import checked_file, file_record, load_package

OUTPUT = symbol_arrow_pipeline.OUTPUT
RECORD = ROOT / 'data/catalog/batch-runs/cd1-symbol-arrow-sample.json'




def run(write_record=False, output=OUTPUT, fresh=False):
    runner = symbol_arrow_pipeline.ArrowRunner(output)
    by_ref = {j['source_reference']:j for j in runner.data['jobs']}
    jobs = [by_ref[symbol_arrows.REFERENCE]]
    offsets = [t['rtf']['byte_offset'] for j in jobs for t in j['source_topics']]
    offsets += [a['rtf']['byte_offset'] for a in runner.policy['auxiliaries'].values()]
    runner.states = inherited_states(runner.rtf, offsets)
    root = runner.output / 'checkpoints' / key(runner.identity)
    records, checks, bitmap_checks, runtime_files = [], [], set(), {}
    # Auxiliary decisions remain those of 14a; adding article fonts cannot alter them.
    auxiliary_root = ROOT / read_json(retry_associations.associations.RECORD)['output_root']
    aux_rows = {r['topic_id']:r for r in read_json(auxiliary_root / 'recoveries.json')}
    for job in jobs:
        target = root / 'jobs' / (job['id'].rsplit(':',1)[1]+'.json')
        if target.exists():
            record = verify_job(root, runner.output, read_json(target), key(runner.identity))
            require(checked_file(root, record['source_evidence']) == json_bytes(job), 'Sample source job changed')
        else:
            begin = len(runner.cache.events)
            result = isolate([job], runner.process)[0]
            record = persist_job(root, runner, job, result, runner.cache.events[begin:])
        records.append(record)
        result = record['result']
        print(job['source_reference']+': '+record['outcome'],flush=True)
        require(result['status'] == 'prepared', 'Fixed font sample failed; preserve evidence and review: '+str(result.get('error')))
        decoded = read_json(runner.output / result['stages']['recovery']['path'] / 'recovery.json')
        before = read_json(runner.prior_review_root / f'articles/{job["source_reference"]}/recovery.json')
        require(decoded == {**before, 'topics':[symbol_arrows.expected_topic(t, runner.arrow_policy) for t in before['topics']]}, 'Retry changed more than reviewed source-bound text')
        require([t['ordinal'] for t in decoded['topics']] == [s['native']['ordinal'] for s in job['source_topics']], 'Article boundary changed')
        source_checks = [symbol_arrows.check_topic(runner.rtf,t,s['rtf'],runner.arrow_policy) for t,s in zip(decoded['topics'],job['source_topics'])]
        for aux in result['auxiliaries']:
            if aux['topic_id'] in aux_rows:
                expected = aux_rows[aux['topic_id']]
                require(aux['recovery_status'] == expected['status'], 'Auxiliary disposition changed')
                if aux['recovery_status'] == 'recovered':
                    n=runner.topic_lookup[aux['topic_id']]['native']['ordinal']
                    actual=read_json(runner.output/result['stages']['association']['path']/f'auxiliaries/{n}/recovery.json')
                    require(actual == read_json(auxiliary_root/f'topics/{n}/recovery.json'), 'Auxiliary text changed')
        package = runner.output / result['package'] / 'content'
        bundle, manifest, counts = load_package(package)
        require([a['id'] for a in bundle['articles']] == [job['candidate_article_id']], 'Wrong sample article')
        for path in sorted(package.rglob('*')):
            if path.is_file():
                runtime_files[job['source_reference']+'/'+path.relative_to(package).as_posix()] = digest(path.read_bytes())
        for item in bundle['media']['items']:
            name=item['source']['resource']
            if item['status']=='available' and name.endswith(('.bmp','.dib')):
                source=images.bitmap_pixels(images.RAW/name); converted=images.bitmap_pixels(package/item['asset']['path'])
                require(all(source[k]==converted[k] for k in ('width','height','rgba_sha256')), 'Bitmap pixels changed')
                bitmap_checks.add(name)
        checks.append({'article_id':job['candidate_article_id'], 'source_checks':source_checks, 'counts':counts})
    issues={issue:runner.compose(issue) for issue in sorted({j['issue_id'] for j in jobs})}
    for issue,result in issues.items():
        require(result['status']=='prepared','Sample issue composition failed')
        bundle,_,counts=load_package(runner.output/result['package']/'content')
        require({a['id'] for a in bundle['articles']} == {j['candidate_article_id'] for j in jobs if j['issue_id']==issue} and counts==result['counts'], 'Wrong sample issue population')
    outputs=[file_record(p.relative_to(root).as_posix(),p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file()]
    summary={'schema_version':1,'checkpoint':'18b','scope':'one_reversible_Symbol_arrow_article',
             'pipeline_identity_sha256':key(runner.identity),'review_record_sha256':digest(font_review.RECORD.read_bytes()),
             'output_root':runner.output.relative_to(ROOT).as_posix(),'checkpoints_root':root.relative_to(ROOT).as_posix(),
             'sample':{symbol_arrows.REFERENCE:'exact reviewed arrow runs and literal spaces'},'glyph_policy_sha256':key(runner.arrow_policy),'outcomes':dict(sorted(Counter(r['outcome'] for r in records).items())),
             'jobs':[{'job_id':r['job_id'],'outcome':r['outcome'],'result':r['result']} for r in records],
             'source_checks':checks,'issues':issues,'checkpoint_outputs':outputs,'runtime_files':runtime_files,
             'verification':{'only_reviewed_source_bound_runs_changed':True,'source_boundaries_and_formatting_preserved':True,
                             'pixel_equivalent_bitmaps':len(bitmap_checks),'physical_review':'pending'},
             'limits':['one_sample_only','17b_combined_handoffs_unchanged','two_Symbol_font_context_conflicts_deferred','18a_punctuation_sample_preserved','other_font_failures_not_retried','media_repair_deferred']}
    if fresh:
        expected=read_json(RECORD)
        require(summary['pipeline_identity_sha256']==expected['pipeline_identity_sha256'] and runtime_files==expected['runtime_files'], 'Fresh sample runtime differs')
        require(checks==expected['source_checks'] and summary['outcomes']==expected['outcomes'], 'Fresh sample audit differs')
        print('Fresh rebuild reproduces all '+str(len(runtime_files))+' runtime files',flush=True)
    elif write_record: write(RECORD,json_bytes(summary))
    else: require(summary==read_json(RECORD),'Font sample differs from recorded result')
    print(json.dumps(summary['outcomes']),flush=True)
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group();group.add_argument('--write-record',action='store_true');group.add_argument('--verify-fresh',action='store_true')
    args=parser.parse_args()
    if args.verify_fresh:
        with tempfile.TemporaryDirectory(prefix='cd1-symbol-arrow-rebuild-',dir=ROOT/'build') as directory:
            run(output=Path(directory),fresh=True)
    else: run(args.write_record)
