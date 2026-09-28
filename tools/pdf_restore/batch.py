"""Bounded, resumable regional OCR; reviewed publication stays a separate step."""
import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import tempfile
import time

from PIL import Image, __version__ as pillow_version

from .build import build, checked, safe_path
from .inventory import ROOT, digest, pin, write_json
from .ocr import RUNTIME, orient_image, pixel_box, run_region, verify_runtime
from .package import validate_package

DEFAULT_CONFIG = {'scale_to': 3000, 'psm': 6}
MAX_LIMITS = {'articles': 3, 'source_pages': 12, 'lookup_pages': 20}


def key(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def private_path(path, root):
    path = Path(path).resolve()
    if not any(path.is_relative_to(root / name) for name in ('private', 'build')):
        raise ValueError('Batch outputs must remain under private/ or build/')
    return path


def verify_pin(root, record):
    safe_path(root, record['path'])
    if pin(root, record['path']) != record:
        raise ValueError(f'Input hash/size changed: {record["path"]}')


def atomic_json(path, value):
    """Commit a durable ledger before starting work and after every outcome."""
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, prefix='.ledger-', delete=False) as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
        temporary = f.name
    os.replace(temporary, path)
    sync_directory(path.parent)


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


@contextmanager
def locked(folder):
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / '.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ValueError('Another batch process holds this lock') from error
        yield


def toolchain(runtime):
    record = verify_runtime(runtime)
    renderer = Path(shutil.which('pdftoppm')).resolve()
    version = subprocess.run([str(renderer), '-v'], capture_output=True, check=True).stderr.decode()
    return {'runtime': {'version': record['version'], 'files': record['files']},
            'renderer': {'sha256': digest(renderer), 'version': version},
            'pillow': pillow_version,
            'implementation': {name: digest(Path(__file__).parent / name)
                               for name in ('batch.py', 'ocr.py', 'package.py')}}


def configuration(region, overrides):
    config = {**DEFAULT_CONFIG, 'languages': 'eng' if region['kind'] == 'code' else 'kor+eng', **overrides}
    if set(config) != {'scale_to', 'psm', 'languages'}:
        raise ValueError('Unknown processing configuration')
    if (type(config['psm']) is not int or not 3 <= config['psm'] <= 13 or
        type(config['scale_to']) is not int or not 1000 <= config['scale_to'] <= 6000 or
        config['languages'] not in ('eng', 'kor', 'kor+eng')):
        raise ValueError('Unsupported processing configuration')
    return {**config, 'oem': 1, 'dpi_hint': 300, 'preserve_interword_spaces': 1,
            'threads': 1, 'preprocessing': 'upright render; whiten exclusions; exact crop'}


def prepare(request_path, state, cache, root=ROOT, runtime=RUNTIME):
    root, runtime = Path(root).resolve(), Path(runtime).resolve()
    state, cache = private_path(state, root), private_path(cache, root)
    if state.exists():
        raise ValueError('Batch state already exists; resume it or name a new checkpoint')
    if state == cache or state.is_relative_to(cache) or cache.is_relative_to(state):
        raise ValueError('State and cache must be separate directories')
    request = json.loads(Path(request_path).read_bytes())
    limits = request['limits']
    if set(limits) != set(MAX_LIMITS) or any(type(v) is not int or not 0 < v <= MAX_LIMITS[k]
                                            for k, v in limits.items()):
        raise ValueError('Invalid batch ceilings')
    if not 0 < len(request['articles']) <= limits['articles']:
        raise ValueError('Article ceiling exceeded')
    lookups = request['lookup_pages']
    if len(lookups) > limits['lookup_pages']:
        raise ValueError('Lookup page ceiling exceeded')
    inventory = root / 'private/pdf-restoration/inventory'
    sources = json.loads((inventory / 'sources.json').read_bytes())['sources']
    for lookup in lookups:
        source = next((s for s in sources if s['id'] == lookup.get('source_id')), None)
        if source is None or type(lookup.get('pdf_page')) is not int or not 1 <= lookup['pdf_page'] <= len(source['pages']):
            raise ValueError('Lookup pages require a known source and one-based PDF page')
    queue = [json.loads(line) for line in (inventory / 'queue.jsonl').read_bytes().splitlines()]
    protected = [pin(root, (inventory / name).relative_to(root).as_posix())
                 for name in ('sources.json', 'queue.jsonl')]
    environment = toolchain(runtime)
    tasks, articles, pages, identities = [], [], set(), set()
    started = time.monotonic()
    for item in request['articles']:
        package = validate_package(json.loads(checked(root, item['map'])))
        if package['mapping']['status'] != 'mapped':
            raise ValueError('Unresolved mapping must remain a separate outcome, not an OCR job')
        if package['id'] in identities:
            raise ValueError('Duplicate article identity')
        identities.add(package['id'])
        source = next((s for s in sources if s['id'] == package['source']['id']), None)
        if source is None or source['scope'] != 'toc-entries-and-cover' or any(
                source[k] != package['source'][k] for k in ('path', 'sha256', 'bytes')):
            raise ValueError('Article source is not eligible or disagrees with inventory')
        if not any(q['toc_entry_id'] == package['toc_entry_id'] and q['issue_id'] == package['issue_id']
                   and q['source_id'] == source['id'] for q in queue):
            raise ValueError('Article is not an existing eligible TOC entry')
        protected.extend([item['map'], package['toc_pin'],
                          {k: source[k] for k in ('path', 'sha256', 'bytes')}])
        page_map = {p['pdf_index']: p for p in package['pages']}
        for page in page_map.values():
            original = source['pages'][page['pdf_index']]
            if any(page[k] != original[k] for k in ('pdf_page', 'width_pt', 'height_pt', 'rotation', 'MediaBox', 'CropBox')):
                raise ValueError('Page geometry differs from inventory')
            pages.add((source['sha256'], page['pdf_index']))
        article = {'id': package['id'], 'toc_entry_id': package['toc_entry_id'], 'map': item['map'],
                   'source_pages': [p['pdf_page'] for p in package['pages']], 'recipe': item.get('recipe')}
        if item.get('recipe'):
            recipe_path = safe_path(root, item['recipe']['path'])
            recipe = json.loads(checked(root, item['recipe']))
            base = recipe_path.parent
            if checked(base, recipe['map']) != checked(root, item['map']):
                raise ValueError('Reviewed recipe belongs to another map; retain it separately')
            corrections = json.loads(checked(base, recipe['corrections']))
            if corrections['article_id'] != package['id'] or corrections['map'] != recipe['map']:
                raise ValueError('Corrections belong to another map')
            protected.append(item['recipe'])
            for record in [recipe['map'], recipe['corrections']]:
                protected.append(pin(root, safe_path(base, record['path']).relative_to(root).as_posix()))
            for bundle in recipe['ocr_bundles']:
                evidence = json.loads(checked(base, bundle['manifest']))
                protected.append(pin(root, safe_path(base, bundle['manifest']['path']).relative_to(root).as_posix()))
                folder = safe_path(base, bundle['directory'])
                for record in evidence['images'] + [r[k] for r in evidence['results'] for k in ('text', 'positions', 'settings')]:
                    checked(folder, record)
                    protected.append(pin(root, safe_path(folder, record['path']).relative_to(root).as_posix()))
        articles.append(article)
        overrides = item.get('region_config', {})
        if not set(overrides) <= {r['id'] for r in package['regions']}:
            raise ValueError('Configuration names an unknown region')
        for region in package['regions']:
            if not re.fullmatch(r'[A-Za-z0-9_-]+', region['id']):
                raise ValueError('Region IDs must be safe filename components')
            page = page_map[region['pdf_index']]
            dependency = {
                'source_sha256': source['sha256'],
                'page': {k: v for k, v in page.items() if k != 'printed_page'},
                'region': {k: region[k] for k in ('id', 'pdf_index', 'kind', 'bbox')},
                'exclusions': [r['bbox'] for r in package['excluded_regions'] if r['pdf_index'] == region['pdf_index']],
                'toolchain': environment,
                'config': configuration(region, {**request.get('config', {}), **overrides.get(region['id'], {})})}
            tasks.append({'id': package['id'] + '/' + region['id'], 'article_id': package['id'],
                          'key': key(dependency), 'dependency': dependency,
                          'source_path': source['path'], 'map': item['map']})
    if len(pages) > limits['source_pages']:
        raise ValueError('Distinct source page ceiling exceeded')
    protected = list({r['path']: r for r in protected}.values())
    for record in protected:
        verify_pin(root, record)
    state.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=state.parent, prefix='.prepare-') as temporary:
        stage = Path(temporary) / 'state'
        stage.mkdir()
        plan = {'version': 1, 'batch_id': request['batch_id'], 'limits': limits, 'lookup_pages': lookups,
                'source_pages': len(pages), 'articles': articles, 'tasks': tasks, 'protected_inputs': protected,
                'cache': cache.relative_to(root).as_posix(), 'runtime': runtime.relative_to(root).as_posix(),
                'runtime_pin': pin(runtime, 'runtime.json'), 'toolchain': environment,
                'request_sha256': digest(Path(request_path))}
        write_json(stage / 'plan.json', plan)
        atomic_json(stage / 'ledger.json', {'plan': pin(stage, 'plan.json'),
                    'prepare_validation_seconds': time.monotonic() - started,
                    'tasks': {t['id']: {'status': 'pending', 'attempts': 0, 'failures': 0, 'interruptions': 0}
                              for t in tasks}, 'events': []})
        stage.rename(state)
    return plan


def load_state(state, root, verify_environment=True):
    state = private_path(state, root)
    ledger = json.loads((state / 'ledger.json').read_bytes())
    plan = json.loads(checked(state, ledger['plan']))
    if set(ledger['tasks']) != {t['id'] for t in plan['tasks']}:
        raise ValueError('Ledger task inventory changed')
    for task in plan['tasks']:
        if task['key'] != key(task['dependency']):
            raise ValueError('Task cache key changed')
    for record in plan['protected_inputs']:
        verify_pin(root, record)
    runtime = safe_path(root, plan['runtime'])
    verify_pin(runtime, plan['runtime_pin'])
    if verify_environment and toolchain(runtime) != plan['toolchain']:
        raise ValueError('Processing tools changed; prepare a new bounded checkpoint')
    return plan, ledger


def cache_result(cache, task):
    folder = cache / task['key']
    if not folder.exists():
        return None
    record = json.loads((folder / 'manifest.json').read_bytes())
    if record['key'] != task['key'] or record['dependency'] != task['dependency']:
        raise ValueError('Cache provenance differs')
    expected = {'region.png', 'settings.json', 'timing.json'}
    if task['dependency']['region']['kind'] != 'figure':
        expected |= {'result.txt', 'result.tsv', 'result.stderr.txt'}
    if {r['path'] for r in record['files']} != expected or len(record['files']) != len(expected):
        raise ValueError('Incomplete cache inventory')
    if {p.name for p in folder.iterdir()} != expected | {'manifest.json'}:
        raise ValueError('Unexpected cache files')
    for row in record['files']:
        verify_pin(folder, row)
    return record


def process_region(task, stage, scratch, root, runtime):
    """Cache page renders only during this invocation; never export full pages."""
    dep = task['dependency']
    page, config = dep['page'], dep['config']
    page_key = key([dep['source_sha256'], page, config['scale_to']])
    render = scratch / (page_key + '.png')
    started = time.monotonic()
    if not render.exists():
        subprocess.run(['pdftoppm', '-f', str(page['pdf_page']), '-l', str(page['pdf_page']),
                        '-singlefile', '-scale-to', str(config['scale_to']), '-png',
                        str(root / task['source_path']), str(render.with_suffix(''))],
                       check=True, capture_output=True)
    with Image.open(render) as image:
        image.load()
        image = orient_image(image, page)
        for bbox in dep['exclusions']:
            image.paste('white', pixel_box(bbox, image.size))
        crop = pixel_box(dep['region']['bbox'], image.size)
        image.crop(crop).save(stage / 'region.png')
        size = list(image.size)
    crop_seconds = time.monotonic() - started
    ocr_seconds = 0
    if dep['region']['kind'] != 'figure':
        ocr_seconds = run_region(stage / 'region.png', stage / 'result', config, runtime)
    write_json(stage / 'settings.json', {'dependency': dep, 'crop_pixels': list(crop), 'render_size': size})
    write_json(stage / 'timing.json', {'render_crop_seconds': crop_seconds, 'ocr_seconds': ocr_seconds})


def resume(state, root=ROOT, max_tasks=None, retry=(), reason=None):
    root, state = Path(root).resolve(), Path(state).resolve()
    if max_tasks is not None and (type(max_tasks) is not int or max_tasks < 1):
        raise ValueError('max-tasks must be positive')
    if retry and not reason:
        raise ValueError('A targeted retry requires a recorded reason')
    with locked(private_path(state, root)):
        plan, ledger = load_state(state, root)
        if not set(retry) <= set(ledger['tasks']):
            raise ValueError('Unknown retry region')
        for id in retry:
            row = ledger['tasks'][id]
            if row['status'] != 'failed' or row['failures'] >= 2:
                raise ValueError('Retry requires one failed attempt; further recovery needs a new checkpoint')
        cache = private_path(root / plan['cache'], root)
        runtime = root / plan['runtime']
        with locked(cache), tempfile.TemporaryDirectory(dir=cache, prefix='.renders-') as temporary:
            attempted = 0
            for task in plan['tasks']:
                row = ledger['tasks'][task['id']]
                result = cache_result(cache, task)
                if result:
                    if row['status'] != 'complete':
                        row.update(status='complete', cache_hit=True)
                        ledger['events'].append({'task': task['id'], 'event': 'cache-hit'})
                        atomic_json(state / 'ledger.json', ledger)
                    continue
                if row['status'] == 'complete':
                    raise ValueError('Completed cache result is missing; preserve ledger and investigate')
                if row['status'] == 'running':
                    row.update(status='interrupted', interruptions=row['interruptions'] + 1)
                    ledger['events'].append({'task': task['id'], 'event': 'interrupted-process'})
                    atomic_json(state / 'ledger.json', ledger)
                if row['status'] == 'failed' and task['id'] not in retry:
                    continue
                if max_tasks is not None and attempted >= max_tasks:
                    break
                row.update(status='running', attempts=row['attempts'] + 1, cache_hit=False)
                ledger['events'].append({'task': task['id'], 'event': 'started', 'attempt': row['attempts'],
                                         'retry_reason': reason if task['id'] in retry else None})
                atomic_json(state / 'ledger.json', ledger)
                started = time.monotonic()
                try:
                    with tempfile.TemporaryDirectory(dir=cache, prefix='.region-') as work:
                        stage = Path(work) / 'result'
                        stage.mkdir()
                        try:
                            process_region(task, stage, Path(temporary), root, runtime)
                        except Exception as error:
                            # Retain partial raw outputs and diagnostics outside the success cache.
                            if isinstance(error, subprocess.CalledProcessError):
                                (stage / 'process.stderr.txt').write_bytes(error.stderr or b'')
                            write_json(stage / 'failure.json', {'error': f'{type(error).__name__}: {error}',
                                       'task': task['id'], 'attempt': row['attempts'], 'key': task['key']})
                            failure = state / 'failures' / (task['key'] + '-' + str(row['attempts']))
                            failure.parent.mkdir(exist_ok=True)
                            stage.rename(failure)
                            raise
                        write_json(stage / 'manifest.json', {'key': task['key'], 'dependency': task['dependency'],
                                   'files': [pin(stage, p.name) for p in sorted(stage.iterdir())]})
                        # Flush result bytes before its atomic rename and ledger completion.
                        for path in stage.iterdir():
                            with path.open('rb') as f:
                                os.fsync(f.fileno())
                        stage.rename(cache / task['key'])
                        sync_directory(cache)
                        cache_result(cache, task)
                    row.update(status='complete')
                except KeyboardInterrupt:
                    row.update(status='interrupted', interruptions=row['interruptions'] + 1)
                    ledger['events'].append({'task': task['id'], 'event': 'interrupted'})
                    atomic_json(state / 'ledger.json', ledger)
                    raise
                except Exception as error:
                    row.update(status='failed', failures=row['failures'] + 1)
                    ledger['events'].append({'task': task['id'], 'event': 'failure',
                                             'error': f'{type(error).__name__}: {error}'})
                row['seconds'] = row.get('seconds', 0) + time.monotonic() - started
                ledger['events'].append({'task': task['id'], 'event': row['status']})
                atomic_json(state / 'ledger.json', ledger)
                attempted += 1
    return report(state, root)


def report(state, root=ROOT):
    root, state = Path(root).resolve(), Path(state).resolve()
    plan, ledger = load_state(state, root)
    cache = root / plan['cache']
    counts, articles, total_bytes, timing = {}, [], 0, {'render_crop_seconds': 0, 'ocr_seconds': 0}
    for task in plan['tasks']:
        status = ledger['tasks'][task['id']]['status']
        counts[status] = counts.get(status, 0) + 1
        if status == 'complete':
            result = cache_result(cache, task)
            if result is None:
                raise ValueError('Completed cache result is missing')
            total_bytes += sum(r['bytes'] for r in result['files'])
            measured = json.loads((cache / task['key'] / 'timing.json').read_bytes())
            for k in timing:
                timing[k] += measured[k]
    for article in plan['articles']:
        tasks = [t for t in plan['tasks'] if t['article_id'] == article['id']]
        complete = all(ledger['tasks'][t['id']]['status'] == 'complete' for t in tasks)
        articles.append({'id': article['id'], 'ocr_status': 'complete' if complete else 'incomplete',
                         'verification': 'unreviewed', 'reviewed_recipe_preserved': bool(article['recipe'])})
    return {'batch_id': plan['batch_id'], 'counts': counts, 'source_pages': plan['source_pages'],
            'articles': articles, 'cache_payload_bytes': total_bytes, 'cached_processing_seconds': timing,
            'attempts': sum(r['attempts'] for r in ledger['tasks'].values()),
            'failures': sum(r['failures'] for r in ledger['tasks'].values()),
            'note': 'OCR completion is not article availability or transcription verification.'}


def reviewed_match(article, tasks, cache, root):
    """Carry review only when every crop, raw text and position output is identical."""
    if not article['recipe']:
        return False
    path = root / article['recipe']['path']
    recipe = json.loads(path.read_bytes())
    regions, raw = {}, {}
    for bundle in recipe['ocr_bundles']:
        folder = path.parent / bundle['directory']
        evidence = json.loads(checked(path.parent, bundle['manifest']))
        for record in evidence['images']:
            regions[Path(record['path']).stem] = (folder, record)
        for row in evidence['results']:
            if len(row['region_ids']) == 1:
                raw[row['region_ids'][0]] = (folder, row)
    for task in tasks:
        id = task['dependency']['region']['id']
        folder, record = regions[id]
        cached = cache / task['key']
        if (cached / 'region.png').read_bytes() != checked(folder, record):
            return False
        if task['dependency']['region']['kind'] != 'figure':
            folder, row = raw[id]
            for filename, field in [('result.txt', 'text'), ('result.tsv', 'positions')]:
                if (cached / filename).read_bytes() != checked(folder, row[field]):
                    return False
    return True


def export(state, output, root=ROOT):
    root, state = Path(root).resolve(), Path(state).resolve()
    output = private_path(output, root)
    if output.exists():
        raise ValueError('Export exists; use a fresh output')
    with locked(state):
        plan, ledger = load_state(state, root)
        summary = report(state, root)
        cache = root / plan['cache']
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=output.parent, prefix='.batch-export-') as temporary:
            stage = Path(temporary) / 'export'
            stage.mkdir()
            outcomes = []
            for article in plan['articles']:
                tasks = [t for t in plan['tasks'] if t['article_id'] == article['id']]
                base = safe_path(stage, article['id'])
                base.mkdir()
                (base / 'map.json').write_bytes(checked(root, article['map']))
                page_map = {p['pdf_page']: p for p in json.loads((base / 'map.json').read_bytes())['pages']}
                bundles = []
                for pdf_page in article['source_pages']:
                    folder = base / f'ocr-page{pdf_page}'
                    folder.mkdir()
                    page = page_map[pdf_page]
                    images, results = [], []
                    for task in tasks:
                        dep = task['dependency']
                        if dep['page']['pdf_page'] != pdf_page or ledger['tasks'][task['id']]['status'] != 'complete':
                            continue
                        cached, id = cache / task['key'], dep['region']['id']
                        shutil.copyfile(cached / 'region.png', safe_path(folder, id + '.png'))
                        images.append(pin(folder, id + '.png'))
                        if dep['region']['kind'] == 'figure':
                            continue
                        name = id + '-psm' + str(dep['config']['psm'])
                        for suffix in ('txt', 'tsv', 'stderr.txt'):
                            shutil.copyfile(cached / ('result.' + suffix), safe_path(folder, name + '.' + suffix))
                        cached_settings = json.loads((cached / 'settings.json').read_bytes())
                        write_json(folder / (name + '.settings.json'), {**dep['config'],
                            **{k: dep['page'][k] for k in ('orientation_correction',) if k in dep['page']},
                            'region_ids': [id], 'image': id + '.png', 'package': {'sha256': article['map']['sha256']},
                            'source_sha256': dep['source_sha256'], 'pdf_page': pdf_page, 'pdf_index': pdf_page - 1,
                            'render_scale_to': dep['config']['scale_to'], 'runtime': plan['runtime_pin'],
                            'crop_pixels': cached_settings['crop_pixels'], 'render_size': cached_settings['render_size'],
                            'batch_cache_key': task['key'], 'cache_dependency': dep,
                            'positions': 'TSV pixels relative to crop; add crop_pixels origin for page positions'})
                        results.append({'region_ids': [id], 'text': pin(folder, name + '.txt'),
                                        'positions': pin(folder, name + '.tsv'), 'settings': pin(folder, name + '.settings.json')})
                    write_json(folder / 'evidence.json', {'source_sha256': tasks[0]['dependency']['source_sha256'],
                               **{k: page[k] for k in ('orientation_correction',) if k in page},
                               'pdf_page': pdf_page, 'runtime': plan['runtime_pin'], 'images': images, 'results': results})
                    bundles.append({'directory': folder.name, 'manifest': pin(base, folder.name + '/evidence.json')})
                complete = all(ledger['tasks'][t['id']]['status'] == 'complete' for t in tasks)
                matches = complete and reviewed_match(article, tasks, cache, root)
                outcome = {'id': article['id'], 'ocr_complete': complete, 'review_required': not matches,
                           'evidence_bundles': bundles, 'reviewed_export': None}
                if matches:
                    build(root / article['recipe']['path'], base / 'reviewed', root)
                    outcome['reviewed_export'] = article['id'] + '/reviewed'
                outcomes.append(outcome)
            write_json(stage / 'outcomes.json', {'summary': summary, 'articles': outcomes,
                       'plan': pin(state, 'plan.json'), 'ledger': pin(state, 'ledger.json')})
            write_json(stage / 'manifest.json', {'files': [pin(stage, p.relative_to(stage).as_posix())
                       for p in sorted(stage.rglob('*')) if p.is_file()]})
            check_export(stage)
            stage.rename(output)
    return outcomes


def check_export(output):
    manifest = json.loads((output / 'manifest.json').read_bytes())
    names = [r['path'] for r in manifest['files']]
    if len(names) != len(set(names)) or set(names) | {'manifest.json'} != {
            p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}:
        raise ValueError('Batch export inventory differs')
    for record in manifest['files']:
        verify_pin(output, record)
    return json.loads((output / 'outcomes.json').read_bytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    p = sub.add_parser('prepare')
    p.add_argument('--request', type=Path, required=True)
    p.add_argument('--state', type=Path, required=True)
    p.add_argument('--cache', type=Path, default=ROOT / 'private/pdf-restoration/batch-cache')
    p = sub.add_parser('resume')
    p.add_argument('--state', type=Path, required=True)
    p.add_argument('--max-tasks', type=int)
    p.add_argument('--retry', action='append', default=[])
    p.add_argument('--reason')
    p = sub.add_parser('export')
    p.add_argument('--state', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p = sub.add_parser('check')
    p.add_argument('--state', type=Path)
    p.add_argument('--output', type=Path)
    args = parser.parse_args()
    # SIGKILL/power loss instead leave a durable running row, recovered on resume.
    def interrupted(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, interrupted)
    if args.action == 'prepare':
        result = prepare(args.request, args.state, args.cache)
        result = {'batch_id': result['batch_id'], 'tasks': len(result['tasks']), 'source_pages': result['source_pages']}
    elif args.action == 'resume':
        result = resume(args.state, max_tasks=args.max_tasks, retry=args.retry, reason=args.reason)
    elif args.action == 'export':
        result = export(args.state, args.output)
    else:
        if bool(args.state) == bool(args.output):
            parser.error('check requires exactly one of --state or --output')
        result = report(args.state) if args.state else check_export(args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.action == 'resume' or (args.action == 'check' and args.state):
        if any(row['ocr_status'] != 'complete' for row in result['articles']):
            parser.exit(2)


if __name__ == '__main__':
    main()
