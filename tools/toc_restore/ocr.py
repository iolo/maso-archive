"""Cached local OCR of loose JPEGs, independent of web image resolution."""
from collections import defaultdict
import csv
from pathlib import Path
import tempfile

from PIL import Image, ImageOps

from tools.pdf_restore.ocr import RUNTIME, verify_runtime, run_region
from tools.reading_room.export import digest, read, safe
from tools.reading_room.covers import separate
from .inventory import PRIVATE, SOURCES, fingerprint, save

DEFAULT_CONFIG = dict(bounds=[3600, 5400], languages='kor+eng', psm=3,
                      rotation=0, regions=[[0, 0, 1, 1]], version=1)


def lines_from_tsv(path, origin):
    groups = defaultdict(list)
    with path.open(encoding='utf-8') as stream:
        # Tesseract TSV is not CSV-quoted; a recognized quote is literal text.
        for row in csv.DictReader(stream, delimiter='\t', quoting=csv.QUOTE_NONE):
            if row['level'] == '5' and row.get('text', '').strip():
                groups[(row['block_num'], row['par_num'], row['line_num'])].append(row)
    result = []
    for words in groups.values():
        left = min(int(w['left']) for w in words)
        top = min(int(w['top']) for w in words)
        right = max(int(w['left']) + int(w['width']) for w in words)
        bottom = max(int(w['top']) + int(w['height']) for w in words)
        result.append(dict(text=' '.join(w['text'] for w in words),
                           bbox=[left + origin[0], top + origin[1], right + origin[0], bottom + origin[1]],
                           confidence=sum(float(w['conf']) for w in words) / len(words)))
    return result


def ocr_page(row, directory=SOURCES, output=PRIVATE / 'ocr', config=None, runtime=RUNTIME):
    config = dict(DEFAULT_CONFIG, **(config or {}))
    separate(Path(output), directory, runtime)
    if config['rotation'] not in (0, 90, 180, 270):
        raise ValueError('OCR rotation must be a right angle')
    if not config['regions'] or any(len(b) != 4 or not (0 <= b[0] < b[2] <= 1 and 0 <= b[1] < b[3] <= 1) for b in config['regions']):
        raise ValueError('OCR regions must be normalized nonempty rectangles')
    verify_runtime(runtime)
    path = safe(Path(directory), row['old'])
    if digest(path) != row['sha256']:
        raise ValueError('OCR source differs from inventory')
    settings = dict(config, sourceSha256=row['sha256'], runtimeSha256=digest(runtime / 'runtime.json'))
    key = fingerprint(settings)
    destination = Path(output) / key
    if destination.exists():
        evidence = read(destination / 'evidence.json')
        if evidence['settings'] != settings:
            raise ValueError('OCR cache settings differ')
        for item in evidence['files']:
            if digest(safe(destination, item['path'])) != item['sha256']:
                raise ValueError('OCR cache bytes differ')
        if evidence.get('parserVersion') != 2:
            evidence['lines'] = [dict(line, region=task['region']) for task in evidence['tasks']
                                for line in lines_from_tsv(destination / task['positions'], task['cropPixels'])]
            evidence['parserVersion'] = 2
            save(destination / 'evidence.json', evidence)
        return evidence, destination
    Path(output).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.ocr-', dir=output) as temp:
        stage = Path(temp) / 'new'
        stage.mkdir()
        with Image.open(path) as image:
            image.load()
            image = ImageOps.exif_transpose(image).convert('RGB')
            if config['rotation']:
                image = image.rotate(-config['rotation'], expand=True)
            image.thumbnail(config['bounds'], Image.Resampling.LANCZOS)
            dimensions = list(image.size)
            tasks, lines = [], []
            for index, bbox in enumerate(config['regions']):
                box = [int(bbox[0]*image.width), int(bbox[1]*image.height),
                       int(bbox[2]*image.width), int(bbox[3]*image.height)]
                name = f'region-{index:02}'
                image.crop(box).save(stage / f'{name}.png')
                run_region(stage / f'{name}.png', stage / name, config, runtime)
                region_lines = lines_from_tsv(stage / f'{name}.tsv', box)
                lines.extend(dict(r, region=index) for r in region_lines)
                tasks.append(dict(region=index, cropPixels=box, text=f'{name}.txt', positions=f'{name}.tsv'))
        if digest(path) != row['sha256']:
            raise ValueError('OCR source changed during recognition')
        files = [dict(path=p.name, sha256=digest(p)) for p in sorted(stage.iterdir())]
        evidence = dict(settings=settings, dimensions=dimensions, tasks=tasks, lines=lines, files=files, parserVersion=2,
                        coordinates='Pixels of oriented, resized OCR image; boxes include crop origin')
        save(stage / 'evidence.json', evidence)
        stage.rename(destination)
    return evidence, destination
