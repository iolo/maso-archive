"""Pinned local Tesseract evidence, bounded to one mapped page per invocation."""
import argparse
import json
import math
import os
from pathlib import Path
import platform
import re
import subprocess
import time

from PIL import Image

from .inventory import ROOT, digest, pin, write_json
from .package import orientation_degrees, validate_package

RUNTIME = ROOT / 'private/pdf-restoration/ocr-runtime'
DEB_HASHES = {
    'libleptonica6_1.86.0-1_amd64.deb': '02cf6d56ec1b2b906a4039e93119ba04a56098efb775ca7c5791528a41ec43f0',
    'libtesseract5_5.5.0-1build1_amd64.deb': '67a4c0589b2178ea82db69cb83d0fdcee21f3e509b52819fcc359d8461555d6d',
    'tesseract-ocr-eng_1%3a4.1.0-2build1_all.deb': 'cfd4055be0740a651c80b82dcddee67d4635510a092a2a4dc86eff54589a557e',
    'tesseract-ocr-kor_1%3a4.1.0-2build1_all.deb': 'a485563f5e1e731b4fae7de58f74845e5f55c59271486207f8a3ac2c028192bc',
    'tesseract-ocr_5.5.0-1build1_amd64.deb': 'b3c3dc68fdc96ddad655f523194bc2a84c243648cffb9dc6a734877acc31ede8',
}


def environment(runtime=RUNTIME):
    return {**os.environ, 'LC_ALL': 'C.UTF-8', 'OMP_THREAD_LIMIT': '1',
            'LD_LIBRARY_PATH': str(runtime / 'root/usr/lib/x86_64-linux-gnu'),
            'TESSDATA_PREFIX': str(runtime / 'root/usr/share/tesseract-ocr/5/tessdata')}


def setup(runtime=RUNTIME):
    packages = sorted((runtime / 'debs').glob('*.deb'))
    if {p.name for p in packages} != set(DEB_HASHES):
        raise ValueError('Expected the five pinned runtime/model packages; see PDF-RESTORATION.md')
    for package in packages:
        if digest(package) != DEB_HASHES[package.name]:
            raise ValueError('Downloaded runtime package differs from pinned SHA-256')
    if (runtime / 'runtime.json').exists():
        verify_runtime(runtime)
    for package in packages:
        subprocess.run(['dpkg-deb', '-x', str(package), str(runtime / 'root')], check=True)
    executable = runtime / 'root/usr/bin/tesseract'
    version = subprocess.run([str(executable), '--version'], env=environment(runtime),
                             capture_output=True, text=True, check=True).stdout
    files = [pin(runtime, p.relative_to(runtime).as_posix()) for p in packages]
    for name in ('root/usr/bin/tesseract', 'root/usr/lib/x86_64-linux-gnu/libtesseract.so.5',
                 'root/usr/lib/x86_64-linux-gnu/libleptonica.so.6',
                 'root/usr/share/tesseract-ocr/5/tessdata/kor.traineddata',
                 'root/usr/share/tesseract-ocr/5/tessdata/eng.traineddata'):
        files.append(pin(runtime, name))
    dependencies = subprocess.run(['ldd', str(executable)], env=environment(runtime),
                                  capture_output=True, text=True, check=True).stdout
    record = dict(version=version, files=files, host=platform.platform(),
                  dependencies=dependencies, packages=[subprocess.check_output(
                      ['dpkg-deb', '-f', str(p), 'Package', 'Version', 'Architecture']).decode() for p in packages])
    target = runtime / 'runtime.json'
    if target.exists():
        existing = json.loads(target.read_bytes())
        # ldd's ASLR load addresses vary between processes; filenames and all
        # other runtime evidence must still agree. Preserve the original bytes.
        def stable(value):
            return {**value, 'dependencies': re.sub(r'\s+\(0x[0-9a-fA-F]+\)', '', value['dependencies'])}
        if stable(existing) != stable(record):
            raise ValueError('Existing pinned OCR runtime differs; preserve it and review a new checkpoint')
        return existing
    write_json(target, record)
    return record


def verify_runtime(runtime=RUNTIME):
    record = json.loads((runtime / 'runtime.json').read_bytes())
    for item in record['files']:
        if pin(runtime, item['path']) != item:
            raise ValueError('OCR runtime/model hash differs from pin')
    return record


def pixel_box(bbox, size):
    width, height = size
    box = (math.floor(bbox[0] * width), math.floor(bbox[1] * height),
           math.ceil(bbox[2] * width), math.ceil(bbox[3] * height))
    if box[0] >= box[2] or box[1] >= box[3]:
        raise ValueError('Region has no complete pixels at this render resolution')
    return box


def orient_image(image, page):
    """Correct a Poppler-rendered image before upright masks/crops, without resampling."""
    degrees = orientation_degrees(page)
    transpose = {90: Image.Transpose.ROTATE_270, 180: Image.Transpose.ROTATE_180,
                 270: Image.Transpose.ROTATE_90}
    return image.transpose(transpose[degrees]) if degrees else image


def run_region(image, destination, config, runtime=RUNTIME):
    started = time.monotonic()
    args = [str(runtime / 'root/usr/bin/tesseract'), str(image), str(destination),
            '-l', config['languages'], '--oem', '1', '--psm', str(config['psm']),
            '--dpi', '300', '-c', 'preserve_interword_spaces=1', 'txt', 'tsv']
    result = subprocess.run(args, env=environment(runtime), capture_output=True, check=True)
    elapsed = time.monotonic() - started
    destination.with_suffix('.stderr.txt').write_bytes(result.stderr)
    return elapsed


def page_ocr(package_path, pdf_page, output, mode='compare', runtime=RUNTIME):
    package = validate_package(json.loads(package_path.read_bytes()))
    source = package['source']
    if digest(ROOT / source['path']) != source['sha256']:
        raise ValueError('PDF source hash changed')
    verify_runtime(runtime)
    selected = [p for p in package['pages'] if p['pdf_page'] == pdf_page]
    if len(selected) != 1:
        raise ValueError('Choose exactly one mapped page')
    page = selected[0]
    regions = [r for r in package['regions'] if r['pdf_index'] == page['pdf_index']]
    output = output.resolve()
    if not any(output.is_relative_to(ROOT / name) for name in ('private', 'build')):
        raise ValueError('OCR outputs must stay private')
    if output.exists():
        raise ValueError('OCR evidence already exists; choose a separate output')
    output.mkdir(parents=True)
    render = output / 'page.png'
    render_args = ['pdftoppm', '-f', str(pdf_page), '-l', str(pdf_page), '-singlefile',
                   '-scale-to', '3000', '-png', str(ROOT / source['path']), str(render.with_suffix(''))]
    subprocess.run(render_args, check=True, capture_output=True)
    with Image.open(render) as image:
        image.load()
        image = orient_image(image, page)
        # Conservative rounding can include a boundary pixel. Whiten every
        # exclusion before making either page or region OCR inputs.
        for excluded in package['excluded_regions']:
            if excluded['pdf_index'] == page['pdf_index']:
                image.paste('white', pixel_box(excluded['bbox'], image.size))
        # Only eligible regions enter page-level OCR, even if a shared page is selected.
        masked = Image.new('RGB', image.size, 'white')
        for region in regions:
            box = pixel_box(region['bbox'], image.size)
            masked.paste(image.crop(box), box)
        masked.save(output / 'eligible-page.png')
        tasks = []
        if mode == 'compare':
            tasks.append(dict(name='page-psm3', image='eligible-page.png',
                              region_ids=[r['id'] for r in regions], languages='kor+eng', psm=3,
                              crop_pixels=[0, 0, *image.size]))
        for region in regions:
            box = pixel_box(region['bbox'], image.size)
            name = region['id']
            image.crop(box).save(output / f'{name}.png')
            if region['kind'] != 'figure':
                tasks.append(dict(name=name + '-psm6', image=f'{name}.png', region_ids=[name],
                                  languages='eng' if region['kind'] == 'code' else 'kor+eng',
                                  psm=6, crop_pixels=list(box)))
        dimensions = list(image.size)
    timings = {}
    results = []
    for task in tasks:
        destination = output / task['name']
        config = {**task, 'oem': 1, 'dpi_hint': 300, 'preserve_interword_spaces': 1,
                  'threads': 1, 'preprocessing': 'upright render, exact region crop; no enhancement',
                  'positions': 'TSV pixels relative to OCR input; add crop_pixels origin for page positions',
                  'runtime': pin(runtime, 'runtime.json'), 'source_sha256': source['sha256'],
                  'package': {'sha256': digest(package_path)}, 'pdf_page': pdf_page,
                  'pdf_index': page['pdf_index'], 'render_size': dimensions, 'render_scale_to': 3000}
        if 'orientation_correction' in page:
            config['orientation_correction'] = page['orientation_correction']
        write_json(destination.with_suffix('.settings.json'), config)
        timings[task['name']] = run_region(output / task['image'], destination, task, runtime)
        results.append(dict(region_ids=task['region_ids'],
                            text=pin(output, task['name'] + '.txt'),
                            positions=pin(output, task['name'] + '.tsv'),
                            settings=pin(output, task['name'] + '.settings.json')))
    write_json(output / 'evidence.json', dict(source_sha256=source['sha256'], pdf_page=pdf_page,
               runtime=pin(runtime, 'runtime.json'), results=results,
               **{k: page[k] for k in ('orientation_correction',) if k in page},
               images=[pin(output, p.name) for p in sorted(output.glob('*.png'))]))
    write_json(output / 'timing.json', dict(seconds=timings, total_seconds=sum(timings.values()),
               volatile_fields=['timing.json; wall-clock processing time only']))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('setup')
    page = sub.add_parser('page')
    page.add_argument('--package', type=Path, required=True)
    page.add_argument('--pdf-page', type=int, required=True)
    page.add_argument('--output', type=Path, required=True)
    page.add_argument('--mode', choices=['compare', 'regions'], default='compare')
    args = parser.parse_args()
    if args.action == 'setup':
        print(setup()['version'])
    else:
        print(json.dumps(page_ocr(args.package, args.pdf_page, args.output, args.mode), indent=2))


if __name__ == '__main__':
    main()
