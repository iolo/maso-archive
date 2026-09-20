"""Run the frozen 13c sample, verify source fidelity, rebuild and serve packages."""
import argparse
from collections import Counter
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import tempfile
from threading import Thread
from urllib.parse import urljoin
from urllib.request import urlopen

from tools.run_cd1_batch import Runner, OUTPUT, ROOT, read_json
from tools.cd1_batch_cache import verify, write
from tools import inventory_cd1_rtf as inventory, map_cd1_images as images
from tools import recover_cd1_text as recovery
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from maso_archive.reading_room_package import checked_file, file_record, load_package

RECORD = ROOT / 'data/catalog/batch-runs/cd1-validation-sample.json'
SAMPLE = ROOT / 'build/cd1-processing-inventory/validation-sample.json'


def run_bytes(rtf, run):
    """Independently reconstruct encoded text from its original RTF spans."""
    result = bytearray()
    for span in run['source_spans']:
        start = span['byte_offset']
        raw = rtf[start:start + span['byte_length']]
        for token in inventory.tokenize(raw):
            source = raw[token['byte_offset']:token['byte_offset'] + token['byte_length']]
            kind = token['kind']
            if kind == 'text_bytes':
                result.extend(source)
            elif kind == 'hex_byte':
                result.append(int(source[2:4], 16))
            elif kind == 'control_symbol' and token['symbol'] in '\\{}':
                result.extend(token['symbol'].encode())
            elif kind == 'control_word' and token['word'] == 'tab':
                result.extend(b'\t')
            else:
                raise ValueError('Unexpected token in text run span: ' + kind)
    require(len(result) == run['encoded_bytes'] and digest(result) == run['encoded_sha256'], 'Encoded run differs from source')
    require(bytes(result) == run['text'].encode(run['encoding']), 'Decoded run does not reproduce source bytes')
    return bytes(result)


def check_topic(rtf, topic, span):
    start, length = span['byte_offset'], span['byte_length']
    require(topic['source_span'] == {'byte_offset': start, 'end_exclusive': start + length}, 'Topic boundary changed')
    require(digest(rtf[start:start + length]) == span['sha256'], 'Topic source changed')
    require(not topic['issues'], 'Undecoded topic')
    cursor, runs, objects = start, 0, 0
    fonts = Counter()
    for item in topic['accounting']:
        require(item['byte_offset'] == cursor, 'Source accounting has a gap or overlap')
        cursor += item['byte_length']
    require(cursor == start + length, 'Incomplete source accounting')
    for paragraph in topic['paragraphs']:
        require(paragraph['text'] == ''.join(r['text'] for r in paragraph['runs']), 'Paragraph projection changed')
        for run in paragraph['runs']:
            if run['kind'] == 'text':
                run_bytes(rtf, run)
                runs += 1
                fonts[str(run['format']['font_id'])] += 1
            else:
                require(run['kind'] == 'object', 'Unsupported run reached validation')
                objects += 1
    return {'ordinal': topic['ordinal'], 'source': span, 'accounted_bytes': length,
            'paragraphs': len(topic['paragraphs']), 'text_runs': runs, 'objects': objects, 'font_runs': dict(sorted(fonts.items()))}


def inspect_run(runner, report):
    require(all(j['status'] == 'prepared' for j in report['jobs']), 'Some selected articles did not prepare; inspect run-report.json')
    require(all(i['status'] == 'prepared' for i in report['issues'].values()), 'Issue composition failed')
    jobs = {j['id']: j for j in runner.data['jobs']}
    articles, media, bitmaps, conversions = [], {}, set(), {}
    for result in report['jobs']:
        job = jobs[result['job_id']]
        recovered = read_json(runner.output / result['stages']['recovery']['path'] / 'recovery.json')
        mapping = read_json(runner.output / result['stages']['semantics']['path'] / 'blocks.json')
        require([t['ordinal'] for t in recovered['topics']] == [s['native']['ordinal'] for s in job['source_topics']], 'Source topic population/order changed')
        topics = [check_topic(runner.rtf, topic, source['rtf']) for topic, source in zip(recovered['topics'], job['source_topics'])]
        auxiliary_topics = []
        for auxiliary in result['auxiliaries']:
            require(auxiliary['recovery_status'] == 'recovered', 'Selected auxiliary text not recovered')
            ordinal = runner.topic_lookup[auxiliary['topic_id']]['native']['ordinal']
            topic = read_json(runner.output / result['stages']['association']['path'] / f'auxiliaries/{ordinal}/recovery.json')
            auxiliary_topics.append(check_topic(runner.rtf, topic, auxiliary['rtf']))
        package = runner.output / result['package']
        verify(package, result['stages']['package']['fingerprint'])
        bundle, manifest, counts = load_package(package / 'content')
        require(bundle['articles'][0]['id'] == job['candidate_article_id'] and bundle['articles'][0]['source']['reference'] == job['source_reference'], 'Source identity changed')
        for item in bundle['media']['items']:
            name = item['source']['resource']
            require(name not in media or media[name] == item, 'Shared media differs across articles')
            media[name] = item
            if item['status'] == 'available' and name.endswith(('.bmp', '.dib')):
                source = images.bitmap_pixels(images.RAW / name)
                target = images.bitmap_pixels(package / 'content' / item['asset']['path'])
                require(all(source[k] == target[k] for k in ('width', 'height', 'rgba_sha256')), 'Bitmap pixel mismatch')
                bitmaps.add(name)
        articles.append({'job_id': job['id'], 'article_id': job['candidate_article_id'], 'source_reference': job['source_reference'],
                         'issue_id': job['issue_id'], 'body_context_relation': job['source_topics'][-1]['context_relation'],
                         'topics': topics, 'auxiliary_topics': auxiliary_topics, 'counts': counts,
                         'block_types': dict(sorted(Counter(b['kind'] for b in mapping['blocks']).items())),
                         'semantic_review': result['semantic_review'], 'deferred_media': result['deferred_media'],
                         'package': result['package'], 'manifest_sha256': digest((package / 'content/manifest.json').read_bytes())})
    # Retain diagnostics for deferred vectors without trying to repair them.
    for event in report['events']:
        if not event['stage'].startswith('media-'):
            continue
        name = event['stage'].removeprefix('media-')
        path = runner.output / 'stages' / event['stage'] / event['fingerprint']
        conversion = read_json(path / 'conversion.json')
        conversions[name] = {'status': media[name]['status'], 'concerns': conversion.get('concerns', []),
                             'policy': conversion.get('policy'), 'diagnostic_sha256': digest((path / 'conversion.json').read_bytes()),
                             'diagnostic_path': (path / 'conversion.json').relative_to(runner.output).as_posix()}
    return {'articles': articles, 'media_count': len(media), 'media_statuses': dict(sorted(Counter(m['status'] for m in media.values()).items())),
            'pixel_equivalent_bitmaps': len(bitmaps), 'conversions': conversions,
            'paragraphs': sum(t['paragraphs'] for a in articles for t in a['topics']),
            'text_runs': sum(t['text_runs'] for a in articles for t in a['topics']),
            'accounted_bytes': sum(t['accounted_bytes'] for a in articles for t in a['topics'])}


def checkpoint_outputs(root, report):
    """Compare every emitted stage, including diagnostics and non-runtime evidence."""
    result = {}
    for event in report['events']:
        path = root / 'stages' / event['stage'] / event['fingerprint']
        manifest = verify(path, event['fingerprint'])
        result[event['stage']] = {'fingerprint': event['fingerprint'], 'outputs': manifest['outputs']}
    return result


def nested_http(root, report):
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    requests = 0
    with tempfile.TemporaryDirectory(prefix='maso-sample-http-') as directory:
        staging = Path(directory)
        prefixes = ['archive/cd1/sample', 'reader/data/magazines/cd1']
        expected = []
        for issue, row in report['issues'].items():
            source = root / row['package'] / 'content'
            for prefix in prefixes:
                destination = staging / prefix / issue / 'content'
                shutil.copytree(source, destination)
                expected.extend((prefix + '/' + issue + '/content/', file_record(p.relative_to(source).as_posix(), p.read_bytes())) for p in sorted(source.rglob('*')) if p.is_file())
        server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=directory))
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for prefix, record in expected:
                base = f'http://127.0.0.1:{server.server_port}/{prefix}'
                with urlopen(urljoin(base, record['path']), timeout=10) as response:
                    require(file_record(record['path'], response.read()) == record, 'Nested static URL bytes differ')
                requests += 1
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
    return {'prefixes': prefixes, 'files_fetched_and_checked': requests}


def run(output=OUTPUT):
    runner = Runner(output)
    sample = read_json(SAMPLE)
    selected = {row['job_id'] for row in sample}
    jobs = [j for j in runner.data['jobs'] if j['id'] in selected or j['issue_id'] == 'maso-1988-02']
    require(len(selected) == 9 and len(jobs) == 15, 'Frozen validation population changed')
    original_process = runner.process
    def progress(job):
        print('Preparing ' + job['source_reference'], flush=True)
        result = original_process(job)
        print('Prepared ' + job['source_reference'], flush=True)
        return result
    runner.process = progress
    first = runner.run(jobs)
    print('Checking source spans, run bytes, identities and bitmap pixels', flush=True)
    evidence = inspect_run(runner, first)
    original = checkpoint_outputs(runner.output, first)
    # Separate output proves the pipeline can rebuild from source without cache.
    print('Rebuilding all fifteen articles in an empty private root', flush=True)
    with tempfile.TemporaryDirectory(prefix='maso-cd1-determinism-') as directory:
        fresh = Runner(Path(directory) / 'batch')
        rebuilt = fresh.run(jobs)
        inspect_run(fresh, rebuilt)
        require(original == checkpoint_outputs(fresh.output, rebuilt), 'Fresh rebuild differs; source/pipeline nondeterminism requires investigation')
    print('Checking resume and two nested static base URLs', flush=True)
    runner.cache.events.clear()
    resumed = runner.run(jobs)
    require(all(e['cache'] == 'hit' for e in resumed['events']), 'Compatible resume rebuilt stages')
    require(original == checkpoint_outputs(runner.output, resumed), 'Resume changed outputs')
    http = nested_http(runner.output, resumed)
    report = {'schema_version': 1, 'checkpoint': '13c', 'sample_sha256': digest(SAMPLE.read_bytes()),
              'pipeline_identity_sha256': first['identity_sha256'], 'output_root': runner.output.relative_to(ROOT).as_posix(),
              'scope': {'february_baseline': 6, 'additional_candidates': 9, 'issues': len(first['issues'])},
              'sample': sample, 'source_checks': evidence, 'issue_packages': first['issues'],
              'validation': {'deterministic_all_stage_outputs': True, 'compatible_resume_hits': len(resumed['events']),
                             'nested_http': http, 'february_article_and_preview_bytes_unchanged': True,
                             'print_verification': 'pending'},
              'limits': ['sample_is_finite_not_proof_of_full_disc_success', 'semantic_and_physical_review_pending',
                         'auxiliaries_recovered_separately; auxiliary_media_rendering_deferred', 'known_media_failures_not_repaired']}
    write(runner.output / 'validation-report.json', recovery.json_bytes(report))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-record', action='store_true')
    args = parser.parse_args()
    report = run()
    if args.write_record:
        write(RECORD, recovery.json_bytes(report))
    else:
        require(report == read_json(RECORD), 'Validation record differs')
    print('Validated February plus all nine frozen candidates; deterministic rebuild, resume and static loading pass', flush=True)


if __name__ == '__main__':
    main()
