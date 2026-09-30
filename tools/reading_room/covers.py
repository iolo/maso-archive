"""Prepare private cover thumbnails; attach derivatives and explicitly retire legacy JPEGs."""
import argparse
from collections import Counter
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
import shutil
import tempfile

from PIL import Image, ImageCms, ImageOps, __version__ as pillow_version, features

from .export import ROOT, copy, digest, read, safe, write

POLICY = 'thumbnail-v1'
DEFAULT_OUTPUT = ROOT / 'build/cover-thumbnails'
DEFAULT_CHECKPOINT = ROOT / 'private/pdf-restoration/covers'
SETTINGS = dict(bounds=[480, 640], quality=80, optimize=True, mode='RGB',
                orientation='exif-transpose', color='embedded-profile-to-sRGB',
                resample='LANCZOS', metadata='stripped', pillow=pillow_version,
                jpeg=features.version('jpg'), lcms=features.version('littlecms2'))


def separate(output, *inputs):
    output = Path(output)
    if output.is_symlink():
        raise ValueError('Unsafe output symlink')
    for source in inputs:
        if source is None:
            continue
        a, b = output.resolve(), Path(source).resolve()
        if a.is_relative_to(b) or b.is_relative_to(a):
            raise ValueError('Output must not overlap cover inputs or private derivatives')


def date_label(label):
    if not re.fullmatch(r'\d{4}', label) or not 1 <= int(label[2:]) <= 12:
        raise ValueError(f'Invalid cover date/filename: {label}')
    return 1900 + int(label[:2]), int(label[2:])


def pin(path):
    return dict(sha256=digest(path), bytes=path.stat().st_size)


def discover(directory, checkpoint=None):
    selected = {}
    if directory is not None and Path(directory).exists():
        directory = Path(directory)
        for path in sorted(directory.iterdir()):
            if path.name.lower().startswith('maso') or path.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.webp'):
                continue
            if not re.fullmatch(r'\d{4}\.jpg', path.name, re.I):
                raise ValueError(f'Donated cover filename must be YYMM.jpg: {path.name}')
            label = path.stem
            date_label(label)
            if label in selected:
                raise ValueError(f'Duplicate donated cover: {label}')
            path = safe(directory, path.name)
            selected[label] = dict(kind='donated', path=str(path.resolve()), **pin(path))
    if checkpoint is None or not Path(checkpoint).exists():
        return selected
    checkpoint = Path(checkpoint)
    # Read the review itself, pinned by the installed checkpoint, rather than
    # inferring trust from maso filenames or merely rendered candidate records.
    ledger = read(safe(checkpoint, 'ledger.json'))
    review_pin = ledger['review']
    reviews_path = safe(checkpoint, review_pin['path'])
    if pin(reviews_path) != {k: review_pin[k] for k in ('sha256', 'bytes')}:
        raise ValueError('PDF cover review changed')
    reviews = read(reviews_path)
    by_id = {r['source_id']: r for r in reviews}
    if len(by_id) != len(reviews):
        raise ValueError('Duplicate PDF cover reviews')
    pdf_dates = set()
    for record in ledger['records']:
        review = by_id.get(record['source_id'])
        if review != record['review']:
            raise ValueError('PDF cover ledger/review differs')
        if review['status'] != 'verified-front-cover':
            continue
        label = review['visible_issue_label']
        date_label(label)
        if (label != record['filename_issue_label'] or not review.get('date_evidence') or
                not review.get('upright') or not review.get('proportions_checked')):
            raise ValueError('PDF cover date/orientation/proportion gate failed')
        if label in pdf_dates:
            raise ValueError(f'Duplicate verified PDF cover: {label}')
        pdf_dates.add(label)
        artifact = record['candidate']['artifact']
        if review['reviewed_artifact'] != artifact:
            raise ValueError('PDF cover review does not identify candidate bytes')
        if label in selected:
            continue  # Priority is resolved before opening/transforming the PDF image.
        path = safe(checkpoint, artifact['path'])
        if pin(path) != {k: artifact[k] for k in ('sha256', 'bytes')}:
            raise ValueError('Reviewed PDF cover bytes changed')
        selected[label] = dict(kind='pdf', path=str(path.resolve()), **pin(path),
                               evidence=dict(ledgerSha256=digest(checkpoint / 'ledger.json'),
                                             review=review, sourceId=record['source_id']))
    return selected


def validate_thumbnail(path, record):
    if pin(path) != {k: record[k] for k in ('sha256', 'bytes')}:
        raise ValueError(f'Thumbnail bytes differ: {path.name}')
    with Image.open(path) as image:
        image.load()
        if (image.format != 'JPEG' or image.mode != 'RGB' or
                image.size != (record['width'], record['height']) or
                not 0 < image.width <= 480 or not 0 < image.height <= 640):
            raise ValueError(f'Thumbnail format/dimensions differ: {path.name}')
        if image.getexif() or set(image.info) - {'jfif', 'jfif_version', 'jfif_unit', 'jfif_density'}:
            raise ValueError(f'Thumbnail contains source metadata: {path.name}')


def transform(source, target):
    path = Path(source['path'])
    with Image.open(path) as image:
        if image.format != 'JPEG':
            raise ValueError(f'Cover format disagrees with JPEG filename: {path.name}')
        image.load()
        image = ImageOps.exif_transpose(image)
        profile = image.info.get('icc_profile')
        if profile:
            image = ImageCms.profileToProfile(image, ImageCms.ImageCmsProfile(BytesIO(profile)),
                                              ImageCms.createProfile('sRGB'), outputMode='RGB')
        else:
            image = image.convert('RGB')
        image.thumbnail(SETTINGS['bounds'], Image.Resampling.LANCZOS)
        # A fresh pixel-only image cannot inherit EXIF, comments, ICC or embedded previews.
        clean = Image.new('RGB', image.size)
        clean.paste(image)
        clean.save(target, format='JPEG', quality=SETTINGS['quality'], optimize=True)
        result = dict(width=clean.width, height=clean.height, **pin(target))
    if pin(path) != {k: source[k] for k in ('sha256', 'bytes')}:
        raise ValueError(f'Cover source changed during preparation: {path.name}')
    return result


def validate_prepared(root, sources=False):
    root = Path(root)
    manifest = read(safe(root, 'manifest.json'))
    if manifest['policy'] != POLICY or manifest['settings'] != SETTINGS:
        raise ValueError('Thumbnail preparation settings differ; regenerate')
    labels, paths = set(), set()
    for record in manifest['records']:
        label = record['date']
        date_label(label)
        if label in labels or record['path'] in paths:
            raise ValueError('Duplicate prepared thumbnail')
        labels.add(label)
        paths.add(record['path'])
        if not re.fullmatch(rf'{label}-[0-9a-f]{{24}}-thumb\.jpg', record['path']):
            raise ValueError('Invalid derivative filename')
        validate_thumbnail(safe(root, record['path']), record)
        if sources and pin(Path(record['source']['path'])) != {k: record['source'][k] for k in ('sha256', 'bytes')}:
            raise ValueError('Prepared thumbnail source changed')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if actual != paths | {'manifest.json'}:
        raise ValueError('Prepared thumbnail inventory differs')
    return manifest


def replace_directory(staged, output, backup):
    if output.exists():
        output.rename(backup)
    try:
        staged.rename(output)
    except OSError:
        if backup.exists():
            backup.rename(output)
        raise


def prepare(directory=ROOT / 'covers', output=DEFAULT_OUTPUT, checkpoint=None):
    output = Path(output)
    separate(output, directory, checkpoint)
    selected = discover(directory, checkpoint)
    previous = {}
    if (output / 'manifest.json').exists():
        old = read(output / 'manifest.json')
        if old.get('settings') == SETTINGS and old.get('policy') == POLICY:
            previous = {r['date']: r for r in old['records']}
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.cover-thumbnails-', dir=output.parent) as temp:
        staged = Path(temp) / 'new'
        staged.mkdir()
        records = []
        for label, source in sorted(selected.items()):
            key = hashlib.sha256(json.dumps([source['sha256'], SETTINGS], sort_keys=True).encode()).hexdigest()[:24]
            name = f'{label}-{key}-thumb.jpg'
            old = previous.get(label)
            if old and old['source'] == source and old['path'] == name:
                validate_thumbnail(safe(output, name), old)
                shutil.copyfile(output / name, staged / name)
                record = old
            else:
                record = dict(date=label, source=source, path=name, **transform(source, staged / name))
            records.append(record)
        manifest = dict(policy=POLICY, settings=SETTINGS, records=records,
                        summary=dict(thumbnails=len(records), sourceKinds=dict(Counter(r['source']['kind'] for r in records)),
                                     bytes=sum(r['bytes'] for r in records), dates=[r['date'] for r in records],
                                     donatedGap9106='9106' not in selected or selected['9106']['kind'] != 'donated',
                                     coverGap9106='9106' not in selected))
        write(staged, 'manifest.json', manifest)
        validate_prepared(staged, sources=True)
        replace_directory(staged, output, Path(temp) / 'previous')
    return manifest


def attach_covers(output, catalog, directory, checkpoint=None, thumbnails=None):
    output = Path(output)
    thumbnails = Path(thumbnails) if thumbnails is not None else DEFAULT_OUTPUT
    separate(output, directory, checkpoint, thumbnails)
    prepared = prepare(directory, thumbnails, checkpoint) if directory is not None or checkpoint is not None else {'records': []}
    records = []
    by_date = {}
    # Transform and validate everything before touching the reader. Exporters call
    # this on a staged tree so any later error also preserves the published tree.
    for record in prepared['records']:
        date = date_label(record['date'])
        issues = [i for i in catalog['issues'] if (i['year'], i['month']) == date]
        if issues:
            cover = dict(path=f'covers/{record["path"]}', width=record['width'],
                         height=record['height'], sha256=record['sha256'])
            by_date[date] = cover
            records.append(dict(filename=record['path'], **cover, issueIds=[i['id'] for i in issues]))
    if (output / 'covers').exists():
        if (output / 'covers').is_symlink():
            raise ValueError('Unsafe reader cover directory')
        shutil.rmtree(output / 'covers')
    for record in records:
        copy(thumbnails, output / 'covers', record['filename'])
    for issue in catalog['issues']:
        issue['cover'] = by_date.get((issue['year'], issue['month']))
        name = f'issues/{issue["id"].removeprefix("maso-")}.json'
        doc = read(safe(output, name))
        doc['issue'] = issue
        write(output, name, doc)
    return records


def identity(path):
    stat = path.stat()
    return dict(device=stat.st_dev, inode=stat.st_ino, mtimeNs=stat.st_mtime_ns, **pin(path))


def cleanup_report(directory, thumbnails, reader):
    from .check import check
    directory, thumbnails, reader = map(Path, (directory, thumbnails, reader))
    separate(reader, directory, thumbnails)
    check(reader, require_thumbnails=True)
    prepared = validate_prepared(thumbnails, sources=True)
    catalog = read(reader / 'catalog.json')
    records = {r['date']: r for r in prepared['records'] if r['source']['kind'] == 'donated'}
    candidates = []
    for legacy in sorted(directory.glob('maso[0-9][0-9][0-9][0-9].jpg')):
        safe(directory, legacy.name)
        label = legacy.stem[4:]
        donation = directory / f'{label}.jpg'
        if not donation.exists():
            continue
        safe(directory, donation.name)
        record = records.get(label)
        if record is None or Path(record['source']['path']) != donation.resolve():
            raise ValueError(f'Missing donated replacement evidence: {legacy.name}')
        for issue in catalog['issues']:
            if (issue['year'], issue['month']) == date_label(label):
                expected = dict(path=f'covers/{record["path"]}', width=record['width'],
                                height=record['height'], sha256=record['sha256'])
                if issue['cover'] != expected:
                    raise ValueError(f'Reader does not use donated replacement: {label}')
        candidates.append(dict(filename=legacy.name, identity=identity(legacy), date=label))
    return dict(directory=str(directory.resolve()), thumbnails=str(thumbnails.resolve()), reader=str(reader.resolve()),
                readerManifestSha256=digest(reader / 'manifest.json'),
                thumbnailManifestSha256=digest(thumbnails / 'manifest.json'), candidates=candidates)


def apply_cleanup(report_path):
    report_path = Path(report_path)
    report = read(report_path)
    directory, thumbnails, reader = (Path(report[k]) for k in ('directory', 'thumbnails', 'reader'))
    report_hash = digest(report_path)
    log_path = report_path.with_name(f'{report_path.stem}.{report_hash[:16]}.applied.json')
    if log_path.is_symlink():
        raise ValueError('Unsafe cleanup log symlink')
    log = read(log_path) if log_path.exists() else dict(reportSha256=digest(report_path), deleted=[])
    if log['reportSha256'] != digest(report_path):
        raise ValueError('Cleanup log/report differs')
    fresh = cleanup_report(directory, thumbnails, reader)
    for key in ('readerManifestSha256', 'thumbnailManifestSha256'):
        if fresh[key] != report[key]:
            raise ValueError('Stale cleanup report: validation evidence changed')
    remaining = [c for c in report['candidates'] if c['filename'] not in log['deleted']]
    if fresh['candidates'] != remaining:
        raise ValueError('Stale cleanup report: legacy files changed')
    prepared = {r['date']: r for r in read(thumbnails / 'manifest.json')['records']}
    for candidate in remaining:
        path = safe(directory, candidate['filename'])
        if identity(path) != candidate['identity']:
            raise ValueError('Legacy file changed before deletion')
        record = prepared[candidate['date']]
        source = safe(directory, f'{candidate["date"]}.jpg')
        if pin(source) != {k: record['source'][k] for k in ('sha256', 'bytes')}:
            raise ValueError('Donated source changed before deletion')
        validate_thumbnail(safe(thumbnails, record['path']), record)
        path.unlink()
        log['deleted'].append(candidate['filename'])
        temporary = write(log_path.parent, log_path.name + '.tmp', log)
        temporary.replace(log_path)
    return log


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'cleanup'])
    parser.add_argument('--covers', type=Path, default=ROOT / 'covers', help='Private donated YYMM.jpg directory')
    parser.add_argument('--thumbnails', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--pdf-cover-checkpoint', type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument('--reader', type=Path, default=ROOT / 'build/reading-room/data')
    parser.add_argument('--report', type=Path, default=ROOT / 'build/cover-cleanup.json')
    parser.add_argument('--apply', action='store_true', help='Apply an existing, unchanged cleanup report')
    args = parser.parse_args()
    if args.action == 'prepare':
        if args.apply:
            parser.error('--apply is only for cleanup')
        result = prepare(args.covers, args.thumbnails, args.pdf_cover_checkpoint)['summary']
    elif args.apply:
        result = apply_cleanup(args.report)
    else:
        result = cleanup_report(args.covers, args.thumbnails, args.reader)
        separate(args.report, args.covers, args.thumbnails, args.reader, args.pdf_cover_checkpoint)
        write(args.report.parent, args.report.name, result)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
