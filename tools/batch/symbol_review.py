"""Audit four Symbol-font cases; approve only source-bound invariant punctuation."""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json

from tools.batch import font_review, font_declaration_review, retry_font_declarations
from tools.run_cd1_batch import ROOT, read_json
from tools.cd1_batch_core import inherited_states
from tools.cd1_batch_cache import Cache, key, write
from tools import recover_cd1_text as recovery, inventory_cd1_rtf as inventory
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from tools.validate_cd1_batch import check_topic, run_bytes
from maso_archive.reading_room_package import checked_file, file_record

CURRENT = ROOT / 'data/catalog/batch-runs/cd1-font-declaration-pass.json'
RECORD = ROOT / 'data/catalog/batch-runs/cd1-symbol-review.json'
OUTPUT = ROOT / 'build/cd1-symbol-review'
MAPPING = ROOT / 'data/reference/adobe-symbol.txt'
MAPPING_SHA256 = 'deb78ca840a429311939b9d165890873f71fb23ef223ceeb144a6c6d641a7e52'
MAPPING_URL = 'https://www.unicode.org/Public/MAPPINGS/VENDORS/ADOBE/symbol.txt'
CASES = {
    '9205400a': {'runs': 2, 'status': 'deferred_font_context_conflict', 'basis': 'Two apparent BASIC PRINT keywords conflict with Greek capitals in the declared Symbol font'},
    '9205403': {'runs': 1, 'status': 'deferred_font_context_conflict', 'basis': 'Apparent Pascal identifier suffix k conflicts with Greek kappa in the declared Symbol font'},
    '9208198': {'runs': 8, 'status': 'deferred_symbol_decoder_required', 'basis': 'Left/up/right arrows agree with annotation context; frozen ASCII/CP949 decoder cannot preserve their byte-to-glyph mapping'},
    '9210202': {'runs': 4, 'status': 'source_bound_invariant_ascii_ready', 'font_codecs': {'2': 'ascii'}, 'basis': 'Only digits 1/2/3, comma and semicolon; Symbol and ASCII mappings agree and source code context supports them'},
}
READY = {'9210202'}
DEFERRED = set(CASES) - READY
SAMPLE = {ref: CASES[ref]['basis'] for ref in sorted(READY)}
INVARIANT_BYTES = frozenset(b',123;')


def mapping_table():
    raw = MAPPING.read_bytes()
    require(digest(raw) == MAPPING_SHA256, 'Symbol mapping reference changed')
    table = {}
    for line in raw.decode('ascii').splitlines():
        if not line or line.startswith('#'): continue
        unicode, encoded = line.split()[:2]
        table.setdefault(int(encoded, 16), []).append(chr(int(unicode, 16)))
    require(all(table[b] == [chr(b)] for b in INVARIANT_BYTES), 'Invariant Symbol subset changed')
    require({b: table[b] for b in (0xac, 0xad, 0xae)} == {0xac: ['←'], 0xad: ['↑'], 0xae: ['→']}, 'Arrow mapping changed')
    return table


def decode_reviewed(run, reference):
    require(reference in READY, 'Article has no approved Symbol decoding policy')
    require(run['kind'] == 'unsupported' and run['format']['font_id'] == 2 and
            run['reason'] == 'Unsupported font 2', 'Run outside reviewed Symbol scope')
    raw = bytes.fromhex(run['original_bytes_hex'])
    require(raw and set(raw) <= INVARIANT_BYTES, 'Run outside reviewed invariant Symbol repertoire')
    return raw.decode('ascii'), 'ascii'


def expected_topic(topic, reference):
    require(reference in READY, 'Article has no approved Symbol decoding policy')
    result = deepcopy(topic); issues = []
    for paragraph in result['paragraphs']:
        for run in paragraph['runs']:
            if run['kind'] != 'unsupported': continue
            text, codec = decode_reviewed(run, reference)
            issues.append({'source_spans': deepcopy(run['source_spans']), 'reason': run['reason']})
            run.pop('reason'); run.pop('original_bytes_hex')
            run.update(kind='text', text=text, encoding=codec)
        paragraph['text'] = ''.join(r['text'] for r in paragraph['runs'])
    require(topic['issues'] == issues, 'Unrelated source issue cannot be cleared')
    result['issues'] = []
    return result


def audit(write_record=False):
    table = mapping_table()
    runner = retry_font_declarations.DeclarationFontRunner(OUTPUT)
    original_root = runner.prior_review_root
    current = read_json(CURRENT)
    require(current['pipeline_identity_sha256'] == key(runner.identity), '17b pipeline changed')
    exception_file = next(r for r in current['outputs'] if r['path'] == 'exceptions.jsonl')
    exceptions = [json.loads(line) for line in checked_file(ROOT / current['coverage_root'], exception_file).splitlines()]
    selected = [j for j in read_json(original_root / 'jobs.json') if j['source_reference'] in CASES]
    require(len(selected) == 4 and {j['source_reference'] for j in selected} == set(CASES), 'Four-case population changed')
    require(all(any(e['job_id'] == j['job_id'] and e['category'] == 'font_or_decoding_policy' for e in exceptions) for j in selected), 'Reviewed job is not a current font failure')
    header = runner.rtf[:runner.rtf.index(b'\n{\\colortbl')]
    require(header.count(rb'{\f2\froman Symbol;}') == 1, 'Symbol declaration changed')
    jobs = {j['id']: j for j in runner.data['jobs']}
    dependencies = {'pipeline': runner.identity, 'current_record_sha256': digest(CURRENT.read_bytes()),
                    'code_sha256': digest(Path(__file__).read_bytes()), 'mapping_sha256': MAPPING_SHA256,
                    'retained_check_sha256': digest(Path(font_declaration_review.__file__).read_bytes()), 'cases': CASES}
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
            require(ref not in runner.policy['article_fonts'] and 2 not in codecs, 'Review would replace a prior font policy')
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
                    actual = recovery.recover_topic(runner.rtf, report, initial, {**codecs, 2: 'ascii'})
                    require(actual == expected_topic(old, ref), 'Recovery changed beyond reviewed invariant runs')
                    checks.append(check_topic(runner.rtf, actual, span)); recovered.append(actual)
                else:
                    checks.append(font_declaration_review.retained_topic_checks(runner.rtf, old, span)); recovered.append(old)
                for i, paragraph in enumerate(old['paragraphs']):
                    for n, run in enumerate(paragraph['runs'], 1):
                        if run['kind'] != 'unsupported': continue
                        require(run['format']['font_id'] == 2 and run['reason'] == 'Unsupported font 2', 'Unexpected unsupported run')
                        encoded = bytes.fromhex(run['original_bytes_hex'])
                        run_bytes(runner.rtf, {**run, 'text': encoded.decode('latin1'), 'encoding': 'latin1'})
                        require(all(b in table for b in encoded), 'Unknown Symbol byte')
                        counts['runs'] += 1; counts['bytes'] += len(encoded)
                        counts['non_ascii_runs'] += int(any(b >= 128 for b in encoded))
                        # Reference candidates stay diagnostic in all deferred articles.
                        evidence.append({'reference': ref, 'topic_id': source['id'], 'paragraph': paragraph['ordinal'], 'run': n,
                            'source_run': run, 'symbol_candidates': {f'{b:02x}': table[b] for b in sorted(set(encoded))},
                            'ascii_candidate': encoded.decode('ascii') if encoded.isascii() else None,
                            'symbol_candidate_space_as_U0020': ''.join(table[b][0] for b in encoded),
                            'decision': case['status'], 'policy_approved': ref in READY,
                            'basis': case['basis'], 'context': old['paragraphs'][max(0,i-1):i+2]})
            require(counts['runs'] == case['runs'], 'Reviewed run population changed')
            write(stage / f'articles/{ref}/recovery.json', recovery.json_bytes({**before, 'topics': recovered}))
            if ref in READY:
                policies[ref] = {'source_topics': job['source_topics'], 'font_codecs': case['font_codecs'],
                                 'allowed_bytes_hex': [f'{b:02x}' for b in sorted(INVARIANT_BYTES)], 'basis': case['basis']}
            rows.append({'job_id': job['id'], 'source_reference': ref, 'source_topics': job['source_topics'],
                         'status': case['status'], 'counts': dict(counts), 'source_checks': checks})
            print(ref + ': ' + case['status'], flush=True)
        write(stage / 'jobs.json', recovery.json_bytes(rows))
        write(stage / 'runs.json', recovery.json_bytes(evidence))
        write(stage / 'policy.json', recovery.json_bytes({'source_rtf_sha256': digest(runner.rtf), 'article_fonts': policies}))

    path, manifest = cache.stage('review', {}, produce)
    rows = read_json(path / 'jobs.json')
    summary = {'schema_version': 1, 'checkpoint': '18a', 'scope': 'four_Symbol_font_cases',
        'current_record': file_record(CURRENT.relative_to(ROOT).as_posix(), CURRENT.read_bytes()),
        'prior_review_record': file_record(font_review.RECORD.relative_to(ROOT).as_posix(), font_review.RECORD.read_bytes()),
        'mapping_reference': {'url': MAPPING_URL, 'retrieved': '2026-09-20', 'file': file_record(MAPPING.relative_to(ROOT).as_posix(), MAPPING.read_bytes()),
                              'applicability': 'reference mapping plus exact declaration and context; not physical glyph verification'},
        'pipeline_identity_sha256': key(runner.identity), 'code_sha256': digest(Path(__file__).read_bytes()),
        'retained_check_sha256': dependencies['retained_check_sha256'],
        'output_root': path.relative_to(ROOT).as_posix(), 'fingerprint': manifest['fingerprint'], 'outputs': manifest['outputs'],
        'cases': CASES, 'accepted_references': sorted(READY), 'deferred_references': sorted(DEFERRED), 'fixed_sample': SAMPLE,
        'counts': {'articles': len(rows), 'source_topics': sum(len(r['source_checks']) for r in rows),
                   'reviewed_runs': sum(r['counts']['runs'] for r in rows), 'reviewed_bytes': sum(r['counts']['bytes'] for r in rows),
                   'accepted_runs': sum(r['counts']['runs'] for r in rows if r['source_reference'] in READY),
                   'job_states': dict(sorted(Counter(r['status'] for r in rows).items()))},
        'limits': ['one_invariant_ascii_policy_only', 'two_font_context_conflicts_retained', 'arrow_decoder_extension_pending',
                   'no_global_Symbol_mapping', 'no_code_repair', 'physical_review_pending', 'current_17b_combined_coverage_unchanged']}
    if write_record: write(RECORD, recovery.json_bytes(summary))
    else: require(read_json(RECORD) == summary, 'Symbol audit differs from recorded result')
    print(json.dumps(summary['counts'], indent=2), flush=True)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-record', action='store_true')
    audit(parser.parse_args().write_record)
