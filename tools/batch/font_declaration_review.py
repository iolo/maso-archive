"""Review seven non-Symbol font declarations; retain ambiguous source bytes without a policy."""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import re

from tools.batch import font_review, retry_ordinary_fonts
from tools.run_cd1_batch import ROOT, read_json
from tools.cd1_batch_core import inherited_states
from tools.cd1_batch_cache import Cache, key, write
from tools import recover_cd1_text as recovery, inventory_cd1_rtf as inventory
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from tools.validate_cd1_batch import check_topic, run_bytes
from maso_archive.reading_room_package import checked_file, file_record

CURRENT = ROOT / 'data/catalog/batch-runs/cd1-ordinary-font-pass.json'
RECORD = ROOT / 'data/catalog/batch-runs/cd1-font-declaration-review.json'
OUTPUT = ROOT / 'build/cd1-font-declaration-review'
# Ordinary names are evidence, not permission to decode arbitrary source runs.
FONTS = {0: 'Helv', 1: 'Tms Rmn', 7: 'Helvetica', 64: 'fixedsys', 72: '@굴림체', 73: 'FIXEDSYS'}
CASES = {
    '8910172': {'font_codecs': {'1': 'ascii'}, 'runs': 1, 'non_ascii': 0, 'basis': 'fourteen spaces after a pointer-assignment illustration; no visible glyph inferred'},
    '9010204': {'font_codecs': {'64': 'cp949'}, 'runs': 205, 'non_ascii': 31, 'basis': 'C listing identifiers and Korean comments agree with surrounding source and compiler notes'},
    '9107124': {'font_codecs': {'73': 'cp949'}, 'runs': 28, 'non_ascii': 4, 'basis': 'C++ class listing has coherent Korean private/public member annotations'},
    '9108302': {'font_codecs': {'72': 'ascii'}, 'runs': 1, 'non_ascii': 0, 'basis': 'single ASCII opening parenthesis before Lock, matched by the following closing parenthesis; vertical font retained'},
    '9304171': {'font_codecs': {'7': 'cp949', '0': 'ascii'}, 'runs': 99, 'non_ascii': 85, 'basis': 'Korean outline-font introduction and body agree in title and terminology; one Helv ASCII run retained'},
    '9306300': {'font_codecs': {'7': 'cp949'}, 'runs': 369, 'non_ascii': 102, 'basis': 'Korean presentation/EMS/VGA prose and listing context support the shared byte repertoire'},
    '9309201': {'font_codecs': {'7': 'cp949'}, 'runs': 96, 'non_ascii': 36, 'basis': 'ambiguous high byte before apparent GET keyword; strict CP949 consumes ASCII G into extended Hangul'},
}
DEFERRED = {'9309201'}
READY = set(CASES) - DEFERRED
SAMPLE = {ref: CASES[ref]['basis'] for ref in ('8910172', '9010204', '9107124', '9108302', '9304171')}


def candidate_decode(run, reference):
    require(reference in CASES, 'Article outside font-declaration review')
    font = run['format']['font_id']; codecs = CASES[reference]['font_codecs']
    require(run['kind'] == 'unsupported' and str(font) in codecs and
            run['reason'] == f'Unsupported font {font}', 'Run outside reviewed unsupported-font scope')
    raw = bytes.fromhex(run['original_bytes_hex']); codec = codecs[str(font)]
    text = raw.decode(codec, errors='strict')
    require(text.encode(codec) == raw, 'Byte round-trip mismatch')
    if codec == 'cp949':
        require(text.encode('euc_kr') == raw, 'Run outside reviewed KS X 1001 byte repertoire')
    require(all(c == '\t' or 32 <= ord(c) != 127 for c in text) and '\ufffd' not in text,
            'Replacement or control in reviewed run')
    return text, codec


def decode_reviewed(run, reference):
    require(reference in READY, 'Deferred article has no approved decoding policy')
    return candidate_decode(run, reference)


def retained_topic_checks(rtf, topic, span):
    """Check every source byte in a deferred topic without interpreting its glyphs."""
    transport = deepcopy(topic); issues = []
    for paragraph in transport['paragraphs']:
        for run in paragraph['runs']:
            if run['kind'] != 'unsupported': continue
            issues.append({'source_spans': deepcopy(run['source_spans']), 'reason': run['reason']})
            raw = bytes.fromhex(run['original_bytes_hex'])
            run.update(kind='text', text=raw.decode('latin1'), encoding='latin1')
        paragraph['text'] = ''.join(r['text'] for r in paragraph['runs'])
    require(topic['issues'] == issues, 'Unexpected issue in retained source')
    transport['issues'] = []
    return {**check_topic(rtf, transport, span), 'mode': 'retained_bytes_not_decoded_text'}


def expected_topic(topic, reference):
    require(reference in READY, 'Deferred article has no approved decoding policy')
    result = deepcopy(topic)
    expected_issues = []
    for paragraph in result['paragraphs']:
        for run in paragraph['runs']:
            if run['kind'] != 'unsupported':
                continue
            text, codec = decode_reviewed(run, reference)
            expected_issues.append({'source_spans': deepcopy(run['source_spans']), 'reason': run['reason']})
            run.pop('reason'); run.pop('original_bytes_hex')
            run.update(kind='text', text=text, encoding=codec)
        paragraph['text'] = ''.join(r['text'] for r in paragraph['runs'])
    require(topic['issues'] == expected_issues, 'Unrelated source issue cannot be cleared')
    result['issues'] = []
    return result


def audit(write_record=False):
    runner = retry_ordinary_fonts.OrdinaryFontRunner(OUTPUT)
    original_root = runner.prior_review_root
    current = read_json(CURRENT)
    require(current['pipeline_identity_sha256'] == key(runner.identity), '16b pipeline changed')
    exception_file = next(r for r in current['outputs'] if r['path'] == 'exceptions.jsonl')
    exceptions = [json.loads(line) for line in checked_file(ROOT / current['coverage_root'], exception_file).splitlines()]
    previous = read_json(original_root / 'jobs.json')
    selected = [j for j in previous if j['source_reference'] in CASES]
    require({j['source_reference'] for j in selected} == set(CASES) and len(selected) == 7, 'Seven-case review population changed')
    require(all(any(e['job_id'] == j['job_id'] and e['category'] == 'font_or_decoding_policy' for e in exceptions) for j in selected), 'Reviewed job is not a current font failure')
    header = runner.rtf[:runner.rtf.index(b'\n{\\colortbl')]
    names = {int(m[1]): m[2].decode('cp949') for m in re.finditer(rb'\{\\f(\d+)\\[a-z]+ ([^;]+);\}', header)}
    require(all(names.get(f) == name for f, name in FONTS.items()), 'Font declarations changed')
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
            before = read_json(original_root / f'articles/{ref}/recovery.json')
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
                if ref in READY:
                    expected = expected_topic(old, ref)
                    extra = {int(k): v for k, v in case['font_codecs'].items()}
                    actual = recovery.recover_topic(runner.rtf, report, initial, {**codecs, **extra})
                    require(actual == expected, 'Recovery changed beyond reviewed runs')
                    checks.append(check_topic(runner.rtf, actual, span)); recovered.append(actual)
                else:
                    # Keep the whole original topic, not a partly accepted decoding.
                    expected = old
                    checks.append(retained_topic_checks(runner.rtf, old, span)); recovered.append(old)
                for i, paragraph in enumerate(old['paragraphs']):
                    for n, run in enumerate(paragraph['runs'], 1):
                        if run['kind'] != 'unsupported': continue
                        encoded = bytes.fromhex(run['original_bytes_hex'])
                        run_bytes(runner.rtf, {**run, 'text': encoded.decode('latin1'), 'encoding': 'latin1'})
                        non_ascii = any(b >= 128 for b in encoded)
                        counts['runs'] += 1; counts['non_ascii'] += int(non_ascii)
                        try:
                            text, codec = candidate_decode(run, ref)
                            interpretation = {'status': 'strict_repertoire_match', 'text': text, 'codec': codec}
                        except (ValueError, UnicodeError) as error:
                            counts['ambiguous_runs'] += 1
                            interpretation = {'status': 'deferred_ambiguous_bytes', 'reason': str(error)}
                        alternatives = {}
                        if non_ascii:
                            for codec in ('cp949', 'euc_kr', 'cp1252', 'cp437', 'johab'):
                                try: alternatives[codec] = {'text': encoded.decode(codec), 'status': 'diagnostic_only'}
                                except UnicodeError: alternatives[codec] = {'status': 'invalid_byte_sequence'}
                        evidence.append({'reference': ref, 'topic_id': source['id'], 'paragraph': paragraph['ordinal'], 'run': n,
                                         'source_run': run, 'candidate': interpretation, 'basis': case['basis'],
                                         'policy_approved': ref in READY, 'alternatives': alternatives,
                                         'context': expected['paragraphs'][max(0,i-1):i+2]})
            require({k: counts[k] for k in ('runs', 'non_ascii')} == {k:case[k] for k in ('runs', 'non_ascii')}, 'Reviewed run population changed')
            require(counts['ambiguous_runs'] == (1 if ref in DEFERRED else 0), 'Ambiguous run population changed')
            write(stage / f'articles/{ref}/recovery.json', recovery.json_bytes({**before, 'topics': recovered}))
            if ref in READY:
                policies[ref] = {'source_topics': job['source_topics'], 'font_codecs': case['font_codecs'], 'basis': case['basis']}
            rows.append({'job_id': job['id'], 'source_reference': ref, 'source_topics': job['source_topics'],
                         'status': 'source_bound_font_policy_ready' if ref in READY else 'deferred_ambiguous_source_byte',
                         'counts': dict(counts), 'source_checks': checks})
            print(ref + ': ' + rows[-1]['status'], flush=True)
        write(stage / 'jobs.json', recovery.json_bytes(rows))
        write(stage / 'runs.json', recovery.json_bytes(evidence))
        write(stage / 'policy.json', recovery.json_bytes({'source_rtf_sha256': digest(runner.rtf), 'article_fonts': policies}))

    path, manifest = cache.stage('review', {}, produce)
    rows = read_json(path / 'jobs.json')
    summary = {'schema_version': 1, 'checkpoint': '17a', 'scope': 'seven_non_Symbol_font_declarations',
               'current_record': file_record(CURRENT.relative_to(ROOT).as_posix(), CURRENT.read_bytes()),
               'prior_review_record': file_record(font_review.RECORD.relative_to(ROOT).as_posix(), font_review.RECORD.read_bytes()),
               'pipeline_identity_sha256': key(runner.identity), 'code_sha256': digest(Path(__file__).read_bytes()),
               'output_root': path.relative_to(ROOT).as_posix(), 'fingerprint': manifest['fingerprint'], 'outputs': manifest['outputs'],
               'cases': CASES, 'accepted_references': sorted(READY), 'deferred_references': sorted(DEFERRED),
               'reviewed_fonts': {str(k): v for k,v in FONTS.items()}, 'fixed_sample': SAMPLE,
               'counts': {'articles': len(rows), 'source_topics': sum(len(r['source_checks']) for r in rows),
                          'reviewed_runs': sum(r['counts']['runs'] for r in rows), 'non_ASCII_runs': sum(r['counts']['non_ascii'] for r in rows),
                          'ambiguous_runs': sum(r['counts'].get('ambiguous_runs', 0) for r in rows),
                          'accepted_runs': sum(r['counts']['runs'] for r in rows if r['source_reference'] in READY),
                          'accepted_non_ASCII_runs': sum(r['counts']['non_ascii'] for r in rows if r['source_reference'] in READY),
                          'job_states': dict(sorted(Counter(r['status'] for r in rows).items()))},
               'limits': ['six_accepted_source_associations_one_deferred', 'not_a_global_font_mapping', 'no_replacement_or_fallback',
                          'physical_review_pending', 'current_16b_combined_coverage_unchanged']}
    if write_record: write(RECORD, recovery.json_bytes(summary))
    else: require(read_json(RECORD) == summary, 'Font-declaration audit differs from recorded result')
    print(json.dumps(summary['counts'], indent=2), flush=True)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-record', action='store_true')
    audit(parser.parse_args().write_record)
