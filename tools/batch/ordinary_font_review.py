"""Review five exact ordinary-font non-ASCII cases against preserved source evidence."""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json

from tools.batch import font_review, retry_fonts
from tools.run_cd1_batch import ROOT, read_json
from tools.cd1_batch_core import inherited_states
from tools.cd1_batch_cache import Cache, key, write
from tools import recover_cd1_text as recovery, inventory_cd1_rtf as inventory
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from tools.validate_cd1_batch import check_topic, run_bytes
from maso_archive.reading_room_package import checked_file, file_record

CURRENT = ROOT / 'data/catalog/batch-runs/cd1-font-pass.json'
RECORD = ROOT / 'data/catalog/batch-runs/cd1-ordinary-font-review.json'
OUTPUT = ROOT / 'build/cd1-ordinary-font-review'
# These are reviewed source cases, not a detector or a global font-codec mapping.
# Contextual evidence and competing interpretations are documented in the report.
CASES = {
    '8905226': {'font': 13, 'runs': 3353, 'non_ascii': 8, 'basis': 'eight contiguous assembly string rows form a box under KS X 1001 decoding'},
    '9201260': {'font': 26, 'runs': 8, 'non_ascii': 4, 'basis': 'Korean spline prose and captions agree with adjacent font-5 headings and figure objects'},
    '9202208': {'font': 0, 'runs': 3, 'non_ascii': 1, 'basis': 'Korean SMM paragraph agrees with the adjacent mixed font-4/font-5 heading'},
    '9203182': {'font': 13, 'runs': 60, 'non_ascii': 4, 'basis': 'Korean C comments and banner text fit the enclosing ASCII listing and object positions'},
    '9207134': {'font': 26, 'runs': 1, 'non_ascii': 1, 'basis': 'Korean listing caption names the isAT function in the following listing'},
}
SAMPLE = {ref: CASES[ref]['basis'] for ref in ('8905226', '9201260', '9202208', '9203182')}


def decode_reviewed(run, reference):
    """Strictly interpret a reviewed case; a font name or round-trip alone is insufficient."""
    require(reference in CASES, 'Article outside ordinary-font review')
    font = CASES[reference]['font']
    require(run['kind'] == 'unsupported' and run['format']['font_id'] == font and
            run['reason'] == f'Unsupported font {font}', 'Run outside reviewed unsupported-font scope')
    raw = bytes.fromhex(run['original_bytes_hex'])
    text = raw.decode('cp949', errors='strict')
    require(text.encode('cp949') == raw and text.encode('euc_kr') == raw,
            'Run outside reviewed KS X 1001 byte repertoire')
    require(all(c == '\t' or 32 <= ord(c) != 127 for c in text) and '\ufffd' not in text,
            'Replacement or control in reviewed run')
    return text


def expected_topic(topic, reference):
    result = deepcopy(topic)
    expected_issues = []
    for paragraph in result['paragraphs']:
        for run in paragraph['runs']:
            if run['kind'] != 'unsupported':
                continue
            text = decode_reviewed(run, reference)
            expected_issues.append({'source_spans': deepcopy(run['source_spans']), 'reason': run['reason']})
            run.pop('reason'); run.pop('original_bytes_hex')
            run.update(kind='text', text=text, encoding='cp949')
        paragraph['text'] = ''.join(r['text'] for r in paragraph['runs'])
    require(topic['issues'] == expected_issues, 'Unrelated source issue cannot be cleared')
    result['issues'] = []
    return result


def audit(write_record=False):
    runner = retry_fonts.FontRunner(OUTPUT)
    current = read_json(CURRENT)
    require(current['pipeline_identity_sha256'] == key(runner.identity), '15b pipeline changed')
    exception_file = next(r for r in current['outputs'] if r['path'] == 'exceptions.jsonl')
    exceptions = [json.loads(line) for line in checked_file(ROOT / current['coverage_root'], exception_file).splitlines()]
    previous = read_json(runner.review_root / 'jobs.json')
    selected = [j for j in previous if set(j['classifications']) - {'reviewed_ascii_font'} == {'non_ascii_in_additional_font'}]
    require({j['source_reference'] for j in selected} == set(CASES) and len(selected) == 5, 'Five-case review population changed')
    require(all(any(e['job_id'] == j['job_id'] and e['category'] == 'font_or_decoding_policy' for e in exceptions) for j in selected), 'Reviewed job is not a current font failure')
    jobs = {j['id']: j for j in runner.data['jobs']}
    dependencies = {'pipeline': runner.identity, 'current_record_sha256': digest(CURRENT.read_bytes()),
                    'code_sha256': digest(Path(__file__).read_bytes()), 'cases': CASES, 'sample': SAMPLE}
    cache = Cache(OUTPUT / 'stages', dependencies)

    def produce(stage):
        states = inherited_states(runner.rtf, [s['rtf']['byte_offset'] for j in selected for s in j['source_topics']])
        rows, evidence, policies = [], [], {}
        for row in selected:
            ref = row['source_reference']; case = CASES[ref]; job = jobs[row['job_id']]
            require(checked_file(ROOT, row['source_evidence']) == recovery.json_bytes(job), 'Reviewed source job changed')
            require(job['source_topics'] == row['source_topics'], 'Source associations changed')
            before = read_json(runner.review_root / f'articles/{ref}/recovery.json')
            require(len(before['topics']) == len(job['source_topics']), 'Incomplete historical source coverage')
            codecs = {int(k): v for k, v in runner.policy['default_font_codecs'].items()}
            require(ref not in runner.policy['article_fonts'], 'Review would replace a prior article policy')
            recovered, checks, counts = [], [], Counter()
            for old, source in zip(before['topics'], job['source_topics']):
                span = source['rtf']; start = span['byte_offset']; raw = runner.rtf[start:start + span['byte_length']]
                require(digest(raw) == span['sha256'], 'Source topic changed')
                require(not states[start]['unknown'], 'Unknown inherited state')
                initial = {k:v for k,v in states[start].items() if k != 'unknown'}
                report = inventory.inspect_topic(raw, start, initial['character']['font_id'])
                report.update(ordinal=source['native']['ordinal'], role='reference_target_body' if source['id'] == job['body_topic_id'] else 'linked_introduction')
                require(not report['issues'], 'Unsupported source construct')
                require(recovery.recover_topic(runner.rtf, report, initial, codecs) == old, 'Historical recovery changed')
                expected = expected_topic(old, ref)
                actual = recovery.recover_topic(runner.rtf, report, initial, {**codecs, case['font']: 'cp949'})
                require(actual == expected, 'Recovery changed beyond reviewed runs')
                checks.append(check_topic(runner.rtf, actual, span)); recovered.append(actual)
                for i, paragraph in enumerate(old['paragraphs']):
                    for n, run in enumerate(paragraph['runs'], 1):
                        if run['kind'] != 'unsupported': continue
                        text = decode_reviewed(run, ref)
                        encoded = run_bytes(runner.rtf, {**run, 'text': text, 'encoding': 'cp949'})
                        non_ascii = any(b >= 128 for b in encoded)
                        counts['runs'] += 1; counts['non_ascii'] += int(non_ascii)
                        if not non_ascii: continue
                        alternatives = {}
                        for codec in ('cp1252', 'cp437', 'johab'):
                            try: alternatives[codec] = {'text': encoded.decode(codec), 'status': 'decodes_without_contextual_approval'}
                            except UnicodeError: alternatives[codec] = {'status': 'invalid_byte_sequence'}
                        evidence.append({'reference': ref, 'topic_id': source['id'], 'paragraph': paragraph['ordinal'], 'run': n,
                                         'source_run': run, 'decoded_text': text, 'codec': 'cp949', 'euc_kr_identical': True,
                                         'basis': case['basis'], 'alternatives': alternatives,
                                         'context': expected['paragraphs'][max(0,i-1):i+2]})
            require(dict(counts) == {k:case[k] for k in ('runs', 'non_ascii')}, 'Reviewed run population changed')
            write(stage / f'articles/{ref}/recovery.json', recovery.json_bytes({**before, 'topics': recovered}))
            policies[ref] = {'source_topics': job['source_topics'], 'font_codecs': {str(case['font']): 'cp949'}, 'basis': case['basis']}
            rows.append({'job_id': job['id'], 'source_reference': ref, 'source_topics': job['source_topics'],
                         'status': 'source_bound_cp949_ready', 'counts': dict(counts), 'source_checks': checks})
            print(ref + ': reviewed CP949, all source runs preserved', flush=True)
        write(stage / 'jobs.json', recovery.json_bytes(rows))
        write(stage / 'runs.json', recovery.json_bytes(evidence))
        write(stage / 'policy.json', recovery.json_bytes({'source_rtf_sha256': digest(runner.rtf), 'article_fonts': policies}))

    path, manifest = cache.stage('review', {}, produce)
    rows = read_json(path / 'jobs.json')
    summary = {'schema_version': 1, 'checkpoint': '16a', 'scope': 'five_ordinary_font_non_ASCII_cases',
               'current_record': file_record(CURRENT.relative_to(ROOT).as_posix(), CURRENT.read_bytes()),
               'prior_review_record': file_record(font_review.RECORD.relative_to(ROOT).as_posix(), font_review.RECORD.read_bytes()),
               'pipeline_identity_sha256': key(runner.identity), 'code_sha256': digest(Path(__file__).read_bytes()),
               'output_root': path.relative_to(ROOT).as_posix(), 'fingerprint': manifest['fingerprint'], 'outputs': manifest['outputs'],
               'cases': CASES, 'fixed_sample': SAMPLE,
               'counts': {'articles': len(rows), 'source_topics': sum(len(r['source_checks']) for r in rows),
                          'reviewed_runs': sum(r['counts']['runs'] for r in rows), 'non_ASCII_runs': sum(r['counts']['non_ascii'] for r in rows)},
               'limits': ['exact_five_source_associations_only', 'not_a_global_font_mapping', 'no_replacement_or_fallback',
                          'physical_review_pending', 'current_15b_combined_coverage_unchanged']}
    if write_record: write(RECORD, recovery.json_bytes(summary))
    else: require(read_json(RECORD) == summary, 'Ordinary-font audit differs from recorded result')
    print(json.dumps(summary['counts'], indent=2), flush=True)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-record', action='store_true')
    audit(parser.parse_args().write_record)
