"""Create a byte-preserving, deduplicated scan pilot from an explicit recipe."""

import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import tempfile
from zipfile import ZipFile

from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def local_path(name):
    relative = PurePosixPath(name)
    if relative.is_absolute() or '..' in relative.parts or '\\' in name:
        raise ValueError(f'Unsafe relative path: {name}')
    path = ROOT / relative
    if any(p.is_symlink() for p in [path, *path.parents] if p != ROOT):
        raise ValueError(f'Symlink in path: {name}')
    return path


def classify(name, recipe):
    base = re.sub(r'(?:\(\d+\))+(?=\.[^.]+$)', '', name)
    if base in recipe['specialImages']:
        special = recipe['specialImages'][base]
        return dict(special, sourceFilenameNumber=None)
    match = re.fullmatch(r'Page(\d+)\.jpg', base)
    if match:
        number = int(match[1])
        return dict(path=f'pages/page-{number:03}.jpg', role='page',
                    position=number + 2, sourceFilenameNumber=number)
    return dict(path=f'extras/{base}', role='unclassified', position=None,
                sourceFilenameNumber=None)


def contact_sheets(stage, images):
    ordered = sorted(images, key=lambda row: (
        row['readingOrder'] is None, row['readingOrder'] or 0, row['path']))
    folder = stage / 'contact-sheets'
    folder.mkdir()
    records = []
    for start in range(0, len(ordered), 30):
        batch = ordered[start:start + 30]
        sheet = Image.new('RGB', (5 * 280, 6 * 425), '#eeeeee')
        draw = ImageDraw.Draw(sheet)
        for n, row in enumerate(batch):
            x, y = (n % 5) * 280, (n // 5) * 425
            with Image.open(stage / row['path']) as image:
                thumb = ImageOps.contain(image, (268, 380))
            sheet.paste(thumb, (x + (280 - thumb.width) // 2, y + 30))
            order = row['readingOrder']
            label = f'{order:03}' if order is not None else 'extra'
            draw.text((x + 6, y + 6), f'{label}  {row["path"]}', fill='black')
        relative = f'contact-sheets/sheet-{start // 30 + 1:02}.jpg'
        sheet.save(stage / relative, quality=88)
        records.append(dict(path=relative, sha256=digest(stage / relative),
                            images=[row['path'] for row in batch]))
    return records


def run(recipe_path):
    recipe = json.loads(recipe_path.read_text(encoding='utf-8'))
    if recipe['schemaVersion'] != 1:
        raise ValueError('Unsupported recipe schema')
    output = local_path(recipe['output'])
    if output.exists():
        raise FileExistsError(f'Refusing existing destination: {output}')
    archives = [(name, local_path(name)) for name in recipe['archives']]
    if not archives or len({path for _, path in archives}) != len(archives):
        raise ValueError('Recipe requires a nonempty list of distinct ZIP paths')
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f'.{recipe["issue"]}-pilot-', dir=output.parent))
    print(f'Staging in {stage.relative_to(ROOT)}', flush=True)
    images, notes, sidecars, sources = {}, [], [], []
    used_paths = set()
    counts = Counter()
    for relative, archive in archives:
        before = digest(archive)
        print(f'Reading {archive.name}', flush=True)
        with ZipFile(archive) as zipped:
            for index, entry in enumerate(zipped.infolist()):
                if entry.is_dir():
                    continue
                member = PurePosixPath(entry.filename)
                if member.parent.as_posix() != recipe['sourceFolder']:
                    raise ValueError(f'Unexpected member folder: {member}')
                data = zipped.read(entry)  # Reading to EOF verifies the ZIP CRC.
                sha = hashlib.sha256(data).hexdigest()
                origin = dict(archive=relative, member=entry.filename,
                              entryIndex=index, bytes=len(data), sha256=sha,
                              crc32=f'{entry.CRC:08x}')
                counts['entries'] += 1
                name = member.name
                if name.startswith('._'):
                    if not data.startswith(b'\x00\x05\x16\x07'):
                        raise ValueError(f'Unrecognized sidecar: {entry.filename}')
                    sidecars.append(dict(origin, kind='AppleDouble'))
                    continue
                if member.suffix.lower() == '.txt':
                    dest = f'notes/{name}'
                    if dest in used_paths:
                        raise ValueError(f'Duplicate note destination: {dest}')
                    target = stage / dest
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                    used_paths.add(dest)
                    notes.append(dict(origin, path=dest))
                    continue
                if member.suffix.lower() != '.jpg':
                    raise ValueError(f'Unexpected entry: {entry.filename}')
                counts['imageEntries'] += 1
                if sha in images:
                    images[sha]['originals'].append(origin)
                    continue
                info = classify(name, recipe)
                destination = info['path']
                if destination in used_paths:
                    old = PurePosixPath(destination)
                    destination = str(old.with_name(f'{old.stem}-variant-{sha[:12]}{old.suffix}'))
                    info.update(role='alternative', position=None)
                if destination in used_paths:
                    raise ValueError(f'Destination collision: {destination}')
                # Validate recipe-derived destinations before writing them.
                local_path(f'{recipe["output"]}/{destination}')
                with Image.open(io.BytesIO(data)) as image:
                    if image.format != 'JPEG':
                        raise ValueError(f'Expected JPEG: {entry.filename}')
                    image.load()  # Full decode; truncated JPEG loading remains disabled.
                    dimensions = list(image.size)
                target = stage / destination
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open('xb') as stream:
                    stream.write(data)
                used_paths.add(destination)
                images[sha] = dict(info, path=destination, sha256=sha, bytes=len(data),
                                   dimensions=dimensions, printedPage=None,
                                   readingOrder=None, originals=[origin])
        after = digest(archive)
        if before != after:
            raise ValueError(f'Source archive changed: {relative}')
        sources.append(dict(path=relative, bytes=archive.stat().st_size,
                            sha256=before, sha256After=after, crcRead='all-entries-passed'))
    rows = sorted(images.values(), key=lambda row: row['path'])
    numbers = {r['sourceFilenameNumber'] for r in rows if r['role'] == 'page'}
    first, last = recipe['expectedFilenameRange']
    gaps = sorted(set(range(first, last + 1)) - numbers)
    if (len(rows) != recipe['expectedUniqueImages'] or not numbers
            or (min(numbers), max(numbers)) != (first, last)
            or gaps != recipe['expectedFilenameGaps']):
        raise ValueError('Pilot image counts or filename gaps differ from the recipe')
    ordered = sorted((row for row in rows if row['position'] is not None),
                     key=lambda row: (row['position'], row['path']))
    for order, row in enumerate(ordered, 1):
        row['readingOrder'] = order
    for row in rows:
        row.pop('position')
        if digest(stage / row['path']) != row['sha256']:
            raise ValueError(f'Extracted image hash differs: {row["path"]}')
    sheets = contact_sheets(stage, rows)
    summary = dict(counts, sidecars=len(sidecars), notes=len(notes),
                   uniqueImages=len(rows), duplicateImages=counts['imageEntries'] - len(rows),
                   imageBytes=sum(row['bytes'] for row in rows),
                   orderedImages=len(ordered), extras=len(rows) - len(ordered),
                   filenameRange=[first, last], filenameGaps=gaps,
                   decodedImages=len(rows), contactSheets=len(sheets))
    manifest = dict(schemaVersion=1, issue=recipe['issue'],
                    recipe=recipe_path.relative_to(ROOT).as_posix(),
                    recipeSha256=digest(recipe_path), sources=sources,
                    summary=summary, reviewStatus='awaiting-visual-review',
                    orderBasis='Source filename numbers, with explicit cover mapping; provisional.',
                    images=rows, notes=notes, omittedSidecars=sidecars,
                    contactSheets=sheets)
    save(stage / 'manifest.json', manifest)
    save(stage / 'summary.json', summary)
    if output.exists():
        raise FileExistsError(f'Destination appeared while staging: {output}')
    stage.rename(output)
    print(json.dumps(dict(output=recipe['output'], **summary), indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--recipe')
    action.add_argument('--verify', metavar='ISSUE_DIRECTORY')
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify(local_path(args.verify)), indent=2))
    else:
        run(local_path(args.recipe))


def verify(output):
    """Re-read original entries and compare them with the finished working set."""
    manifest = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
    if digest(local_path(manifest['recipe'])) != manifest['recipeSha256']:
        raise ValueError('Recipe differs from the extraction recipe')
    origins = {}
    image_paths, hashes = set(), set()
    for row in manifest['images']:
        if digest(output / row['path']) != row['sha256']:
            raise ValueError(f'Working image changed: {row["path"]}')
        if row['sha256'] in hashes or row['path'] in image_paths:
            raise ValueError('Duplicate image content or destination in manifest')
        hashes.add(row['sha256'])
        image_paths.add(row['path'])
        for origin in row['originals']:
            if origin['sha256'] != row['sha256']:
                raise ValueError('Duplicate source does not match its retained image')
    all_origins = [origin for row in manifest['images'] for origin in row['originals']]
    all_origins += manifest['omittedSidecars'] + manifest['notes']
    for origin in all_origins:
        key = (origin['archive'], origin['entryIndex'])
        if key in origins:
            raise ValueError('Source entry accounted more than once')
        origins[key] = origin
    actual_paths = {p.relative_to(output).as_posix()
                    for folder in ('pages', 'covers', 'extras')
                    for p in (output / folder).rglob('*') if p.is_file()}
    if actual_paths != image_paths:
        raise ValueError('Working image inventory differs from the manifest')
    for row in manifest['notes'] + manifest['contactSheets']:
        if digest(output / row['path']) != row['sha256']:
            raise ValueError(f'Working note or contact sheet changed: {row["path"]}')
    seen = set()
    for source in manifest['sources']:
        archive = local_path(source['path'])
        if not source['sha256'] == source['sha256After'] == digest(archive):
            raise ValueError(f'Original ZIP changed: {source["path"]}')
        with ZipFile(archive) as zipped:
            for index, entry in enumerate(zipped.infolist()):
                if entry.is_dir():
                    continue
                key = (source['path'], index)
                origin = origins.get(key)
                data = zipped.read(entry)
                if (origin is None or origin['member'] != entry.filename
                        or origin['bytes'] != len(data)
                        or origin['sha256'] != hashlib.sha256(data).hexdigest()):
                    raise ValueError(f'Source mapping differs: {key}')
                seen.add(key)
    if seen != set(origins):
        raise ValueError('Manifest references missing ZIP entries')
    orders = sorted(row['readingOrder'] for row in manifest['images']
                    if row['readingOrder'] is not None)
    if orders != list(range(1, len(orders) + 1)):
        raise ValueError('Reading-order sequence has gaps or duplicates')
    summary = manifest['summary']
    if (len(seen) != summary['entries'] or len(image_paths) != summary['uniqueImages']
            or len(manifest['omittedSidecars']) != summary['sidecars']
            or sum(len(row['originals']) for row in manifest['images']) != summary['imageEntries']):
        raise ValueError('Summary counts differ from the source accounting')
    return dict(issue=manifest['issue'], result='passed',
                manifestSha256=digest(output / 'manifest.json'),
                sourceArchives=len(manifest['sources']), sourceEntriesChecked=len(seen),
                uniqueImageHashesChecked=len(image_paths),
                duplicateImageEntriesChecked=summary['duplicateImages'],
                sidecarsAccounted=summary['sidecars'],
                contactSheetHashesChecked=len(manifest['contactSheets']),
                originalZipHashesUnchanged=True, readingOrderContiguous=True)


if __name__ == '__main__':
    main()
