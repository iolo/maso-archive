"""Validate six source-bound ordinary-font ASCII retries without rewriting history."""
import argparse
from copy import deepcopy
from pathlib import Path
from collections import Counter
import json
import tempfile

from tools.batch import font_review, retry_associations, full_pass
from tools.batch.retry_associations import AssociationRunner
from tools.batch.full_pass import persist_job, verify_job
from tools.run_cd1_batch import ROOT, read_json, isolate
from tools.cd1_batch_core import inherited_states
from tools.cd1_batch_cache import Cache, key, verify, write
from tools.recover_cd1_text import json_bytes
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from tools.validate_cd1_batch import check_topic
from tools import map_cd1_images as images
from maso_archive.reading_room_package import checked_file, file_record, load_package

OUTPUT = ROOT / 'build/cd1-font-sample'
RECORD = ROOT / 'data/catalog/batch-runs/cd1-font-sample.json'


def safe_output(output):
    output = Path(output).resolve()
    require(output.is_relative_to(ROOT / 'build'), 'Font retries require a private build root')
    for name in ('cd1-batch', 'cd1-associations', 'cd1-association-sample', 'cd1-association-pass', 'cd1-font-review'):
        old = ROOT / 'build' / name
        require(not output.is_relative_to(old) and not old.is_relative_to(output), 'Font retry would overlap preserved outputs')
    return output


class FontRunner(AssociationRunner):
    def __init__(self, output=OUTPUT):
        super().__init__(safe_output(output))
        review = read_json(font_review.RECORD)
        require(review['pipeline_identity_sha256'] == key(self.identity), 'Font review pipeline changed')
        require(review['code_sha256'] == digest(Path(font_review.__file__).read_bytes()), 'Font review implementation changed')
        checked_file(ROOT, review['current_record'])
        self.review_root = ROOT / review['output_root']
        manifest = verify(self.review_root, review['fingerprint'])
        require(manifest['outputs'] == review['outputs'], 'Font audit outputs changed')
        policy = read_json(self.review_root / 'policy.json')
        require(policy['source_rtf_sha256'] == digest(self.rtf), 'Font policy source changed')
        require(not (set(policy['article_fonts']) & set(self.policy['article_fonts'])), 'Font policy replaces prior decisions')
        for row in policy['article_fonts'].values():
            require(all(int(k) in font_review.FONTS and v == 'ascii' for k,v in row['font_codecs'].items()), 'Unreviewed font codec')
        self.policy['article_fonts'].update(policy['article_fonts'])
        self.identity = {**self.identity, 'font_extension': {
            'review_record_sha256':digest(font_review.RECORD.read_bytes()),
            'implementation_sha256':digest(Path(__file__).read_bytes()),
            'checkpoint_support_sha256':digest(Path(full_pass.__file__).read_bytes())}}
        self.cache = Cache(self.output / 'stages', self.identity)


def expected_ascii_topic(topic):
    """Only reviewed unsupported ASCII runs may change; all formatting stays exact."""
    result = deepcopy(topic)
    for paragraph in result['paragraphs']:
        for run in paragraph['runs']:
            if run['kind'] != 'unsupported':
                continue
            require(font_review.classify(run) == 'reviewed_ascii_font', 'Sample contains a deferred run')
            raw = bytes.fromhex(run.pop('original_bytes_hex'))
            run.pop('reason')
            run.update(kind='text', text=raw.decode('ascii'), encoding='ascii')
        paragraph['text'] = ''.join(r['text'] for r in paragraph['runs'])
    result['issues'] = []
    return result


def run(write_record=False, output=OUTPUT, fresh=False):
    runner = FontRunner(output)
    by_ref = {j['source_reference']:j for j in runner.data['jobs']}
    jobs = [by_ref[ref] for ref in font_review.SAMPLE]
    require(all(j['source_reference'] in runner.policy['article_fonts'] for j in jobs), 'Sample policy missing')
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
        before = read_json(runner.review_root / f'articles/{job["source_reference"]}/recovery.json')
        require(decoded == {**before, 'topics':[expected_ascii_topic(t) for t in before['topics']]}, 'Retry changed more than reviewed ASCII text')
        require([t['ordinal'] for t in decoded['topics']] == [s['native']['ordinal'] for s in job['source_topics']], 'Article boundary changed')
        source_checks = [check_topic(runner.rtf,t,s['rtf']) for t,s in zip(decoded['topics'],job['source_topics'])]
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
    summary={'schema_version':1,'checkpoint':'15a','scope':'fixed_six_article_ASCII_font_sample',
             'pipeline_identity_sha256':key(runner.identity),'review_record_sha256':digest(font_review.RECORD.read_bytes()),
             'output_root':runner.output.relative_to(ROOT).as_posix(),'checkpoints_root':root.relative_to(ROOT).as_posix(),
             'sample':font_review.SAMPLE,'outcomes':dict(sorted(Counter(r['outcome'] for r in records).items())),
             'jobs':[{'job_id':r['job_id'],'outcome':r['outcome'],'result':r['result']} for r in records],
             'source_checks':checks,'issues':issues,'checkpoint_outputs':outputs,'runtime_files':runtime_files,
             'verification':{'only_reviewed_ASCII_runs_changed':True,'source_boundaries_and_formatting_preserved':True,
                             'pixel_equivalent_bitmaps':len(bitmap_checks),'physical_review':'pending'},
             'limits':['six_sample_only','14b_combined_handoffs_unchanged','other_font_failures_not_retried','non_ASCII_and_symbol_glyphs_deferred','media_repair_deferred']}
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
        with tempfile.TemporaryDirectory(prefix='cd1-font-rebuild-',dir=ROOT/'build') as directory:
            run(output=Path(directory),fresh=True)
    else: run(args.write_record)
