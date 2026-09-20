"""Audit all 86 current font failures; authorize only source-bound ASCII fonts."""
import argparse
from collections import Counter
from pathlib import Path
import json
import re

from tools.batch.retry_associations import AssociationRunner
from tools.batch import retry_associations
from tools.run_cd1_batch import ROOT, read_json, POLICY
from tools.cd1_batch_core import inherited_states
from tools.cd1_batch_cache import Cache, key, write, verify
from tools import recover_cd1_text as recovery, inventory_cd1_rtf as inventory
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from tools.validate_cd1_batch import run_bytes
from maso_archive.reading_room_package import checked_file, file_record

CURRENT = ROOT / 'data/catalog/batch-runs/cd1-association-pass.json'
RECORD = ROOT / 'data/catalog/batch-runs/cd1-font-review.json'
OUTPUT = ROOT / 'build/cd1-font-review'
# Explicitly reviewed ordinary font declarations; Symbol and every unlisted
# font remain unsupported, even when their character codes happen to be ASCII.
FONTS = {0: 'Helv', 3: 'Times New Roman', 13: 'Courier New',
         26: 'MS Sans Serif', 46: 'COURIER NEW', 48: 'LinePrinter'}
SAMPLE = {'8803110': 'Courier New ASCII layout', '8804096': 'Times New Roman space',
          '8910268': 'uppercase Courier New ASCII listing', '9012137': 'Helv ASCII text',
          '9106274': 'MS Sans Serif spaces', '9205208': 'LinePrinter tab and Times New Roman'}


def classify(run):
    raw = bytes.fromhex(run['original_bytes_hex'])
    font = run['format']['font_id']
    if run['reason'] != f'Unsupported font {font}':
        return 'existing_codec_failure'
    if font not in FONTS:
        return 'unreviewed_font_or_symbol'
    if not all(b == 9 or 32 <= b <= 126 for b in raw):
        return 'non_ascii_in_additional_font'
    return 'reviewed_ascii_font'


def audit(write_record=False):
    runner = AssociationRunner(OUTPUT)
    current = read_json(CURRENT)
    require(current['pipeline_identity_sha256'] == key(runner.identity), '14b pipeline changed')
    exception_file = next(r for r in current['outputs'] if r['path'] == 'exceptions.jsonl')
    exceptions = [json.loads(l) for l in checked_file(ROOT / current['coverage_root'], exception_file).splitlines()]
    selected = [e for e in exceptions if e['category'] == 'font_or_decoding_policy']
    require(len(selected) == 86, 'Font failure population changed')
    header = runner.rtf[:runner.rtf.index(b'\n{\\colortbl')]
    font_names = {int(m[1]): m[2].decode('cp949') for m in re.finditer(rb'\{\\f(\d+)\\[a-z]+ ([^;]+);\}', header)}
    require(all(font_names.get(f) == name for f, name in FONTS.items()), 'Reviewed font declarations changed')
    jobs = {j['id']: j for j in runner.data['jobs']}
    dependencies = {'pipeline': runner.identity, 'current_record_sha256': digest(CURRENT.read_bytes()),
                    'code_sha256': digest(Path(__file__).read_bytes()), 'sample': SAMPLE, 'fonts': FONTS}
    cache = Cache(OUTPUT / 'stages', dependencies)
    def produce(stage):
        offsets = [t['rtf']['byte_offset'] for e in selected for t in jobs[e['job_id']]['source_topics']]
        states = inherited_states(runner.rtf, offsets)
        rows, policy, run_rows = [], {}, []
        for e in selected:
            job = jobs[e['job_id']]
            require(checked_file(ROOT, e['source_evidence']) == recovery.json_bytes(job), 'Source job changed')
            for evidence in e['failure_evidence']:
                checked_file(ROOT, evidence)
            old = read_json(ROOT / next(r['path'] for r in e['failure_evidence'] if r['path'].endswith('/recovery.json')))
            codecs = {int(k): v for k,v in runner.policy['default_font_codecs'].items()}
            codecs.update({int(k): v for k,v in runner.policy['article_fonts'].get(job['source_reference'], {}).get('font_codecs', {}).items()})
            topics, bad = [], []
            for source in job['source_topics']:
                span = source['rtf']; start = span['byte_offset']; raw = runner.rtf[start:start + span['byte_length']]
                require(digest(raw) == span['sha256'], 'Topic source changed')
                state = states[start]
                require(not state['unknown'], 'Inherited state no longer matches historical inventory')
                initial = {k:v for k,v in state.items() if k != 'unknown'}
                report = inventory.inspect_topic(raw, start, initial['character']['font_id'])
                report.update(ordinal=source['native']['ordinal'], role='reference_target_body' if source['id'] == job['body_topic_id'] else 'linked_introduction')
                require(not report['issues'], 'Historical successful inventory changed')
                topic = recovery.recover_topic(runner.rtf, report, initial, codecs)
                topics.append(topic)
                cursor = start
                for item in topic['accounting']:
                    require(item['byte_offset'] == cursor, 'Source accounting gap')
                    cursor += item['byte_length']
                require(cursor == start + span['byte_length'], 'Incomplete source accounting')
                for p in topic['paragraphs']:
                    for n, run in enumerate(p['runs'], 1):
                        if run['kind'] == 'text':
                            run_bytes(runner.rtf, run)
                        elif run['kind'] == 'unsupported':
                            # Independently reconstruct bytes without interpreting glyphs.
                            raw_run = bytes.fromhex(run['original_bytes_hex'])
                            probe = {**run, 'encoding': 'latin1', 'text': raw_run.decode('latin1')}
                            require(run_bytes(runner.rtf, probe) == raw_run, 'Retained run bytes changed')
                            row = {'job_id':job['id'], 'topic_id':source['id'], 'paragraph':p['ordinal'], 'run':n,
                                   'font_id':run['format']['font_id'], 'font_name':font_names.get(run['format']['font_id']),
                                   'classification':classify(run), 'evidence':run}
                            bad.append(row); run_rows.append(row)
            require(topics[:len(old['topics'])] == old['topics'], 'Historical recovery prefix changed')
            require(bad, 'Historical font failure disappeared')
            counts = dict(sorted(Counter(r['classification'] for r in bad).items()))
            ready = set(counts) == {'reviewed_ascii_font'}
            ref = job['source_reference']
            if ready:
                policy[ref] = {'source_topics':job['source_topics'],
                               'font_codecs':{str(r['font_id']):'ascii' for r in bad},
                               'basis':'exact source topics; all additional-font runs are reviewed ordinary-font ASCII; no replacement or fallback'}
            write(stage / f'articles/{ref}/recovery.json', recovery.json_bytes({'schema_version':1, 'cd_reference':ref, 'topics':topics}))
            rows.append({'job_id':job['id'], 'article_id':job['candidate_article_id'], 'source_reference':ref,
                         'source_topics':job['source_topics'], 'status':'ascii_policy_ready' if ready else 'deferred',
                         'classifications':counts, 'topics_checked':len(topics), 'historical_topics':len(old['topics']),
                         'source_evidence':e['source_evidence'], 'failure_evidence':e['failure_evidence']})
            print(ref + ': ' + rows[-1]['status'], flush=True)
        require(set(SAMPLE) <= set(policy), 'Fixed sample includes an unreviewed decoding case')
        write(stage / 'jobs.json', recovery.json_bytes(rows))
        write(stage / 'runs.json', recovery.json_bytes(run_rows))
        write(stage / 'policy.json', recovery.json_bytes({'source_rtf_sha256':digest(runner.rtf), 'article_fonts':policy}))
    path, manifest = cache.stage('review', {'current_record':digest(CURRENT.read_bytes())}, produce)
    rows, runs = read_json(path/'jobs.json'), read_json(path/'runs.json')
    summary = {'schema_version':1, 'checkpoint':'15a', 'scope':'all_86_font_failures_source_audit',
               'current_record':file_record(CURRENT.relative_to(ROOT).as_posix(), CURRENT.read_bytes()),
               'pipeline_identity_sha256':key(runner.identity), 'code_sha256':digest(Path(__file__).read_bytes()),
               'output_root':path.relative_to(ROOT).as_posix(), 'fingerprint':manifest['fingerprint'], 'outputs':manifest['outputs'],
               'reviewed_fonts':{str(k):v for k,v in FONTS.items()}, 'fixed_sample':SAMPLE,
               'counts':{'jobs':len(rows), 'job_states':dict(sorted(Counter(r['status'] for r in rows).items())),
                         'full_source_topics':sum(r['topics_checked'] for r in rows), 'historical_topics':sum(r['historical_topics'] for r in rows),
                         'unsupported_runs':len(runs), 'run_classes':dict(sorted(Counter(r['classification'] for r in runs).items()))},
               'limits':['ASCII_only_source_bound_policy', 'non_ASCII_and_symbol_glyphs_deferred', 'full_86_retry_not_performed', 'physical_review_pending']}
    if write_record: write(RECORD, recovery.json_bytes(summary))
    else: require(read_json(RECORD) == summary, 'Font audit differs from recorded result')
    print(json.dumps(summary['counts'],indent=2),flush=True)
    return summary


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--write-record',action='store_true')
    audit(parser.parse_args().write_record)
