"""Pure-engine paired OCR from frozen, source-only crops; no semantic correction.

Both arms consume identical PNG bytes. Failed Qwen output stays verbatim and is
marked failed; it is never silently replaced by the other engine or an answer.
"""
import argparse
from contextlib import nullcontext
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import time

from PIL import Image
from jsonschema import ValidationError

from tools.pdf_restore.build import checked, validate_source
from tools.pdf_restore.inventory import ROOT, digest, pin, write_json
from tools.pdf_restore.ocr import RUNTIME, run_region, verify_runtime
from tools.pdf_restore.package import validate_package
from .pipeline import infer, TEXT_PROMPT, TEXT_SCHEMA
from .runtime import Server
from .workflow import run_lock


def now():
    return datetime.now(timezone.utc).isoformat()


def read(path):
    return json.loads(path.read_bytes())


def freeze(shared):
    shared = Path(shared).resolve()
    if not shared.is_relative_to(ROOT / 'private'):
        raise ValueError('Paired inputs must remain private')
    package = validate_package(read(shared / 'map.json'))
    if package['mapping']['status'] != 'mapped':
        raise ValueError('Require source-inspected mapped regions')
    validate_source(package, ROOT)
    verify_runtime()
    server = Server(shared / 'unused-runtime')
    record = dict(schema_version=1, frozen_at=now(), scale_to=4000,
        map=pin(ROOT, (shared / 'map.json').relative_to(ROOT).as_posix()),
        crops={r['id']: pin(shared, r['id'] + '.png') for r in package['regions']},
        tesseract=dict(runtime=pin(ROOT, (RUNTIME / 'runtime.json').relative_to(ROOT).as_posix()),
                       oem=1, psm=6, dpi_hint=300, preserve_interword_spaces=1, threads=1,
                       languages={'code': 'eng', 'other': 'kor+eng'}),
        qwen=dict(files={role: dict(path=str(p), sha256=digest(p), bytes=p.stat().st_size)
                         for role, p in [('binary', server.binary), ('model', server.model), ('mmproj', server.mmproj)]},
                  context=8192, image_tokens=4096, gpu_layers=99, timeout=600,
                  max_tokens=2048, region_max_tokens={'p38r10': 512} if any(r['id'] == 'p38r10' for r in package['regions']) else {},
                  temperature=0, top_p=.8, top_k=20, min_p=0, presence_penalty=0,
                  seed=42, cache_prompt=False, prompt=TEXT_PROMPT, schema=TEXT_SCHEMA),
        implementation=[pin(ROOT, f) for f in ('tools/ocr_qwen/paired.py', 'tools/ocr_qwen/pipeline.py',
                          'tools/ocr_qwen/runtime.py', 'tools/pdf_restore/ocr.py')],
        failure_policy='One bounded primary attempt per region. Preserve verbatim failed response, continue other regions, no fallback. Any later retry is separately recorded.')
    target = shared / 'frozen-inputs.json'
    if target.exists():
        raise ValueError('Frozen inputs already exist; never overwrite an experiment baseline')
    write_json(target, record)
    return record


def verify_inputs(shared):
    shared = Path(shared)
    frozen = read(shared / 'frozen-inputs.json')
    package = validate_package(json.loads(checked(ROOT, frozen['map'])))
    validate_source(package, ROOT)
    if set(frozen['crops']) != {r['id'] for r in package['regions']}:
        raise ValueError('Frozen crop inventory differs from map')
    for crop in frozen['crops'].values():
        checked(shared, crop)
    for source in frozen['implementation']:
        checked(ROOT, source)
    checked(ROOT, frozen['tesseract']['runtime'])
    verify_runtime()
    for record in frozen['qwen']['files'].values():
        p = Path(record['path'])
        if p.stat().st_size != record['bytes'] or digest(p) != record['sha256']:
            raise ValueError('Frozen Qwen runtime/model changed')
    return frozen, package


def run(shared, engine, output):
    if engine not in ('qwen', 'tesseract'):
        raise ValueError('Choose one pure OCR engine')
    shared, output = Path(shared).resolve(), Path(output).resolve()
    if not output.is_relative_to(ROOT / 'private'):
        raise ValueError('Raw paired outputs must remain private')
    with run_lock(output):
        output.mkdir(parents=True, exist_ok=False)
        started, clock = now(), time.monotonic()
        attempts = []
        write_json(output / 'started.json', dict(started_at=started, engine=engine))
        try:
            frozen, package = verify_inputs(shared)
            write_json(output / 'runtime-fingerprint.json', dict(engine=engine, frozen_inputs=pin(shared, 'frozen-inputs.json'), settings=frozen[engine]))
            runtime_pin = pin(output, 'runtime-fingerprint.json')
            base = output / package['id']; base.mkdir()
            shutil.copyfile(shared / 'map.json', base / 'map.json')
            q = frozen['qwen']
            server = Server(output / 'qwen-runtime', **{k: v['path'] for k, v in q['files'].items()},
                            context=q['context'], image_tokens=q['image_tokens'], gpu_layers=q['gpu_layers']) if engine == 'qwen' else None
            bundles = []
            with server if server else nullcontext():
                for page in package['pages']:
                    folder = base / f'ocr-page{page["pdf_page"]}'; folder.mkdir()
                    images, results = [], []
                    for region in [r for r in package['regions'] if r['pdf_index'] == page['pdf_index']]:
                        rid = region['id']; crop = folder / (rid + '.png')
                        crop.write_bytes(checked(shared, frozen['crops'][rid])); images.append(pin(folder, crop.name))
                        if region['kind'] == 'figure':
                            continue
                        name = rid + ('-qwen' if engine == 'qwen' else '-psm6')
                        entry = dict(region_id=rid, started_at=now(), status='complete', image_sha256=digest(crop))
                        tick = time.monotonic()
                        settings = dict(engine=engine, region_ids=[rid], image=crop.name,
                            source_sha256=package['source']['sha256'], package={'sha256': frozen['map']['sha256']},
                            pdf_page=page['pdf_page'], pdf_index=page['pdf_index'], render_scale_to=4000, runtime=runtime_pin)
                        if engine == 'tesseract':
                            config = dict(languages='eng' if region['kind'] == 'code' else 'kor+eng', psm=6)
                            try:
                                entry['recognition_seconds'] = run_region(crop, folder / name, config)
                            except subprocess.CalledProcessError as exc:
                                entry.update(status='failed', error_type=type(exc).__name__, returncode=exc.returncode,
                                             recognition_seconds=time.monotonic() - tick)
                                (folder / (name + '.stderr.txt')).write_bytes(exc.stderr or b'')
                                (folder / (name + '.stdout.txt')).write_bytes(exc.stdout or b'')
                                for suffix in ('.txt', '.tsv'):
                                    path = folder / (name + suffix)
                                    if not path.exists():
                                        path.write_bytes(b'')
                            settings.update(config, oem=1, dpi_hint=300, preserve_interword_spaces=1, threads=1)
                            positions = name + '.tsv'
                        else:
                            stage = output / 'stages' / rid; stage.mkdir(parents=True)
                            try:
                                with Image.open(crop) as im:
                                    result, metrics = infer(server, im, q['prompt'].format(kind=region['kind']), q['schema'],
                                        stage / 'inference', q['region_max_tokens'].get(rid, q['max_tokens']), q['timeout'])
                                value = result['text']; entry.update(recognition_seconds=metrics['seconds'], usage=metrics['usage'])
                            except (ValueError, ValidationError, TimeoutError, OSError) as exc:
                                entry.update(status='failed', error_type=type(exc).__name__, error=str(exc))
                                response_path = stage / 'inference.response.json'
                                response = read(response_path) if response_path.exists() else None
                                value = response['choices'][0]['message']['content'] if response else ''
                                entry['usage'] = response.get('usage') if response else None
                                entry['recognition_seconds'] = time.monotonic() - tick
                            response_path = stage / 'inference.response.json'
                            response = read(response_path) if response_path.exists() else None
                            (folder / (name + '.txt')).write_text(value + '\n', encoding='utf-8')
                            positions = name + '.positions.json'
                            write_json(folder / positions, dict(engine='qwen3-vl', granularity='region', word_positions_available=False,
                                region_id=rid, bbox_upright_normalized=region['bbox'], native_response=response, status=entry['status']))
                            native_request = read(stage / 'inference.request.json')
                            if native_request['image_sha256'] != digest(crop):
                                raise ValueError('Qwen received different crop bytes')
                            settings.update(engine='qwen3-vl', native_request=native_request, raw_status=entry['status'])
                        entry.update(finished_at=now(), elapsed_seconds=time.monotonic() - tick)
                        attempts.append(entry); write_json(output / 'attempts.json', attempts)
                        settings['raw_status'] = entry['status']
                        write_json(folder / (name + '.settings.json'), settings)
                        results.append(dict(region_ids=[rid], text=pin(folder, name + '.txt'), positions=pin(folder, positions), settings=pin(folder, name + '.settings.json')))
                        print(f'{engine} {rid}: {entry["status"]}', flush=True)
                    write_json(folder / 'evidence.json', dict(source_sha256=package['source']['sha256'], pdf_page=page['pdf_page'], runtime=runtime_pin, images=images, results=results))
                    bundles.append(dict(directory=folder.name, manifest=pin(base, folder.name + '/evidence.json')))
            write_json(base / 'evidence-bundles.json', dict(ocr_bundles=bundles, runtime=runtime_pin))
            verify_inputs(shared)
            report = dict(engine=engine, status='raw-complete-with-failures' if any(a['status'] != 'complete' for a in attempts) else 'raw-complete',
                          regions=len(attempts), failed_regions=[a['region_id'] for a in attempts if a['status'] != 'complete'],
                          started_at=started, finished_at=now(), worker_seconds=time.monotonic() - clock,
                          recognition_seconds=sum(a['recognition_seconds'] for a in attempts), semantic_correction='not-started', human_acceptance='pending')
            write_json(output / 'report.json', report)
            return report
        finally:
            write_json(output / 'worker-lifespan.json', dict(started_at=started, finished_at=now(), seconds=time.monotonic() - clock,
                       complete_report=(output / 'report.json').exists(), scope='Runtime verification, crop copy, model startup if applicable, inference and evidence export. Shared source rendering/mapping excluded.'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('freeze', 'run'))
    parser.add_argument('--shared', type=Path, required=True)
    parser.add_argument('--engine', choices=('qwen', 'tesseract'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.action == 'run' and (not args.engine or not args.output):
        parser.error('run requires --engine and --output')
    print(json.dumps(freeze(args.shared) if args.action == 'freeze' else run(args.shared, args.engine, args.output), ensure_ascii=False, indent=2))
