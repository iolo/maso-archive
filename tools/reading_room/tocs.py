"""Reduced TOC images and a gallery independent of catalog transcription."""
from collections import defaultdict
from io import BytesIO
from pathlib import Path
import re
import shutil
import tempfile

from PIL import Image, ImageCms, ImageOps, __version__ as pillow_version, features

from .export import ROOT, digest, read, safe, write
from .covers import date_label, pin, replace_directory, separate
from tools.toc_restore.inventory import PRIVATE, SOURCES, fingerprint, inventory, verify_reviews

POLICY = 'toc-images-v1'
DEFAULT_OUTPUT = ROOT / 'build/toc-images'
SETTINGS = dict(preview=dict(bounds=[480, 720], quality=80),
                readable=dict(bounds=[1600, 2400], quality=85),
                orientation='exif-transpose', mode='RGB', color='sRGB',
                resample='LANCZOS', metadata='stripped', pillow=pillow_version,
                jpeg=features.version('jpg'), lcms=features.version('littlecms2'))


def validate_image(path, record, variant):
    if pin(path) != {k: record[k] for k in ('sha256', 'bytes')}:
        raise ValueError('TOC derivative bytes differ')
    with Image.open(path) as image:
        image.load()
        bounds = SETTINGS[variant]['bounds']
        if (image.format != 'JPEG' or image.mode != 'RGB' or
                image.size != (record['width'], record['height']) or
                not 0 < image.width <= bounds[0] or not 0 < image.height <= bounds[1]):
            raise ValueError('TOC derivative encoding or dimensions differ')
        if image.getexif() or set(image.info) - {'jfif', 'jfif_version', 'jfif_unit', 'jfif_density'}:
            raise ValueError('TOC derivative contains source metadata')


def transform(source, target, variant):
    before = pin(source)
    with Image.open(source) as image:
        if image.format != 'JPEG':
            raise ValueError('Expected donated JPEG')
        image.load()
        image = ImageOps.exif_transpose(image)
        profile = image.info.get('icc_profile')
        image = (ImageCms.profileToProfile(image, ImageCms.ImageCmsProfile(BytesIO(profile)),
                 ImageCms.createProfile('sRGB'), outputMode='RGB') if profile else image.convert('RGB'))
        image.thumbnail(SETTINGS[variant]['bounds'], Image.Resampling.LANCZOS)
        clean = Image.new('RGB', image.size)
        clean.paste(image)
        clean.save(target, format='JPEG', quality=SETTINGS[variant]['quality'], optimize=True)
        result = dict(width=clean.width, height=clean.height, **pin(target))
    if before != pin(source) or result['sha256'] == before['sha256']:
        raise ValueError('Source changed or original bytes used as derivative')
    validate_image(target, result, variant)
    return result


def prepare(directory=SOURCES, output=DEFAULT_OUTPUT, reviews=PRIVATE / 'reviews.json'):
    directory, output = Path(directory), Path(output)
    separate(output, directory, reviews)
    source = inventory(directory)
    if source['errors'] or source['duplicates']:
        raise ValueError('Resolve TOC inventory before preparation')
    if source['records']:
        review_data = read(Path(reviews))
        verify_reviews(source, review_data)
    else:
        review_data = dict(pages=[])
    by_hash = {r['sha256']: r for r in review_data['pages']}
    old = {}
    if (output / 'manifest.json').exists():
        previous = read(output / 'manifest.json')
        if previous.get('settings') == SETTINGS:
            old = {r['name']: r for r in previous['records']}
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.toc-images-', dir=output.parent) as temp:
        staged = Path(temp) / 'new'
        staged.mkdir()
        records, excluded = [], []
        for row in source['records']:
            review = by_hash[row['sha256']]
            if review.get('kind', 'toc') != 'toc':
                if review['kind'] != 'advertisement' or not review.get('note'):
                    raise ValueError('Unresolved TOC page classification')
                excluded.append(dict(name=row['new'], reason=review['note'], kind=review['kind'],
                                     source=dict(path=str((directory / row['old']).resolve()), sha256=row['sha256'], bytes=row['bytes'])))
                continue
            key = fingerprint([row['sha256'], SETTINGS])[:24]
            record = dict(name=row['new'], date=row['date'], sequence=row['sequence'],
                          source=dict(path=str((directory / row['old']).resolve()),
                                      sha256=row['sha256'], bytes=row['bytes']))
            if review.get('publicNote'):
                record['publicNote'] = review['publicNote']
            for variant in ('preview', 'readable'):
                filename = f'{Path(row["new"]).stem}-{key}-{variant}.jpg'
                prior = old.get(row['new'], {})
                if (prior.get('source', {}).get('sha256') == record['source']['sha256']
                        and prior.get(variant, {}).get('path') == filename):
                    item = prior[variant]
                    validate_image(safe(output, filename), item, variant)
                    shutil.copyfile(output / filename, staged / filename)
                else:
                    item = dict(path=filename, **transform(directory / row['old'], staged / filename, variant))
                record[variant] = item
            records.append(record)
        manifest = dict(policy=POLICY, settings=SETTINGS, records=records, excluded=excluded)
        write(staged, 'manifest.json', manifest)
        validate_prepared(staged, sources=True)
        replace_directory(staged, output, Path(temp) / 'previous')
    return manifest


def validate_prepared(root, sources=False):
    root = Path(root)
    manifest = read(safe(root, 'manifest.json'))
    if manifest.get('policy') != POLICY or manifest.get('settings') != SETTINGS:
        raise ValueError('TOC image settings differ; regenerate')
    paths, names = {'manifest.json'}, set()
    for row in manifest['records']:
        if row['name'] in names or row['name'] != f'{row["date"]}-{row["sequence"]:02}.jpg':
            raise ValueError('Duplicate or invalid TOC image identity')
        date_label(row['date'])
        names.add(row['name'])
        for variant in ('preview', 'readable'):
            record = row[variant]
            expected = f'{Path(row["name"]).stem}-{fingerprint([row["source"]["sha256"], SETTINGS])[:24]}-{variant}.jpg'
            if record['path'] != expected or record['path'] in paths:
                raise ValueError('Invalid prepared TOC filename')
            paths.add(record['path'])
            validate_image(safe(root, record['path']), record, variant)
            if record['sha256'] == row['source']['sha256']:
                raise ValueError('Original TOC bytes in prepared images')
        if sources and pin(Path(row['source']['path'])) != {k: row['source'][k] for k in ('sha256', 'bytes')}:
            raise ValueError('TOC source changed')
    for row in manifest.get('excluded', []):
        if row['name'] in names or row['kind'] != 'advertisement' or not row['reason']:
            raise ValueError('Invalid excluded donated image')
        names.add(row['name'])
        if sources and pin(Path(row['source']['path'])) != {k: row['source'][k] for k in ('sha256', 'bytes')}:
            raise ValueError('Excluded source changed')
    if {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()} != paths:
        raise ValueError('Prepared TOC inventory differs')
    return manifest


def attach_tocs(output, catalog, directory, prepared=None, reviews=None):
    output = Path(output)
    prepared = Path(prepared) if prepared is not None else DEFAULT_OUTPUT
    separate(output, directory, prepared, reviews)
    records = (prepare(directory, prepared, reviews or PRIVATE / 'reviews.json')['records']
               if directory is not None else [])
    groups = defaultdict(list)
    if (output / 'tocs').exists():
        if (output / 'tocs').is_symlink():
            raise ValueError('Unsafe TOC asset directory')
        shutil.rmtree(output / 'tocs')
    for row in records:
        page = dict(sequence=row['sequence'])
        for variant in ('preview', 'readable'):
            item = row[variant]
            relative = f'tocs/{item["path"]}'
            safe(output, relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(safe(prepared, item['path']), safe(output, relative))
            page[variant] = dict(item, path=relative)
        groups[row['date']].append(page)
    canonical = {f'{i["year"] % 100:02}{i["month"]:02}': i for i in catalog['issues']
                 if not i.get('nativeGroup') and i['id'] == f'maso-{i["year"]:04}-{i["month"]:02}'}
    for label, issue in canonical.items():
        path = f'issues/{issue["id"].removeprefix("maso-")}.json'
        doc = read(safe(output, path))
        doc['tocImages'] = groups.get(label, [])
        write(output, path, doc)
    gallery = [dict(date=f'{date_label(label)[0]:04}-{date_label(label)[1]:02}', pages=pages)
               for label, pages in sorted(groups.items()) if label not in canonical]
    for group in gallery:
        notes = sorted({r['publicNote'] for r in records if r['date'] == group['date'][2:4] + group['date'][5:]
                        and r.get('publicNote')})
        if notes:
            group['note'] = ' '.join(notes)
    write(output, 'toc-gallery.json', dict(schemaVersion=1, sets=gallery))
    catalog['tocGallery'] = 'toc-gallery.json'
    return dict(tocImagePolicy=POLICY, tocImageCounts=dict(pages=len(records),
                assets=len(records) * 2, gallerySets=len(gallery)))


def check_tocs(root, catalog, manifest):
    """Public-only checks: no private paths or source images are needed."""
    root = Path(root)
    if 'tocImagePolicy' not in manifest:
        if (catalog.get('tocGallery') or any((root / 'tocs').glob('*')) or
                any('tocImages' in read(root / f'issues/{i["id"].removeprefix("maso-")}.json') for i in catalog['issues'])):
            raise ValueError('TOC assets without a declared policy')
        return
    if manifest['tocImagePolicy'] != POLICY or catalog.get('tocGallery') != 'toc-gallery.json':
        raise ValueError('Invalid TOC image policy/gallery')
    pages, paths, dates = 0, set(), set()

    def check_set(date, rows):
        nonlocal pages
        if date in dates or (rows and not re.fullmatch(r'19\d{2}-(0[1-9]|1[0-2])', date)):
            raise ValueError('Duplicate/invalid TOC scan date')
        dates.add(date)
        sequences = [r['sequence'] for r in rows]
        if sequences != sorted(set(sequences)) or any(not 1 <= n <= 99 for n in sequences):
            raise ValueError('TOC page order differs')
        for page in rows:
            if set(page) - {'sequence', 'printedPage', 'preview', 'readable'}:
                raise ValueError('Unexpected public TOC evidence')
            pages += 1
            for variant in ('preview', 'readable'):
                record = page[variant]
                if set(record) != {'path', 'sha256', 'bytes', 'width', 'height'}:
                    raise ValueError('Unexpected public TOC derivative fields')
                pattern = rf'tocs/{date[2:4]}{date[5:]}-{page["sequence"]:02}-[0-9a-f]{{24}}-{variant}\.jpg'
                if not re.fullmatch(pattern, record['path']) or record['path'] in paths:
                    raise ValueError('Invalid/duplicate TOC derivative path')
                paths.add(record['path'])
                validate_image(safe(root, record['path']), record, variant)
    for issue in catalog['issues']:
        doc = read(root / f'issues/{issue["id"].removeprefix("maso-")}.json')
        rows = doc.get('tocImages', [])
        if issue.get('nativeGroup') and rows:
            raise ValueError('TOC scans attached to unverified native group')
        if not issue.get('nativeGroup'):
            check_set(issue['id'].removeprefix('maso-'), rows)
    gallery = read(safe(root, catalog['tocGallery']))
    if gallery.get('schemaVersion') != 1:
        raise ValueError('Invalid TOC gallery version')
    for group in gallery['sets']:
        if set(group) - {'date', 'pages', 'note'} or not group['pages'] or ('note' in group and not isinstance(group['note'], str)):
            raise ValueError('Invalid TOC gallery set')
        check_set(group['date'], group['pages'])
    actual = {p.relative_to(root).as_posix() for p in (root / 'tocs').rglob('*') if p.is_file()}
    if actual != paths or manifest['tocImageCounts'] != dict(pages=pages, assets=len(paths), gallerySets=len(gallery['sets'])):
        raise ValueError('Missing/stale TOC assets or counts')


def refresh(output, manifest, directory, prepared=None, reviews=None):
    """Call only inside an exporter's staging tree, before its final check."""
    catalog = read(Path(output) / 'catalog.json')
    manifest.update(attach_tocs(output, catalog, directory, prepared, reviews))
    write(Path(output), 'catalog.json', catalog)
    manifest['files'] = [dict(path=p.relative_to(output).as_posix(), bytes=p.stat().st_size, sha256=digest(p))
                         for p in sorted(Path(output).rglob('*')) if p.is_file() and p != Path(output) / 'manifest.json']
    write(Path(output), 'manifest.json', manifest)


def demo_images(output):
    """Draw public synthetic pages without opening any private donation."""
    from PIL import ImageDraw
    from tools.toc_restore.inventory import save
    output = Path(output)
    with tempfile.TemporaryDirectory(prefix='toc-demo-') as temp:
        temp = Path(temp)
        sources = temp / 'sources'
        sources.mkdir()
        for name, color in [('8802-01.jpg', '#ebe6d8'), ('8802-02.jpg', '#dde8e5'), ('9401-01.jpg', '#e6dfe9')]:
            image = Image.new('RGB', (900, 1300), color)
            draw = ImageDraw.Draw(image)
            draw.text((70, 90), f'SYNTHETIC CONTENTS / {name[:7]}', fill='#263c38', font_size=32)
            for n in range(8):
                draw.text((70, 220 + n * 95), f'Sample article {n + 1}  . . . . . . .  {10 + n * 8}', fill='#263c38', font_size=24)
            image.save(sources / name)
        rows = inventory(sources)['records']
        reviews = temp / 'reviews.json'
        save(reviews, dict(pages=[dict(sha256=r['sha256'], date=r['date'], sequence=r['sequence'],
              identityEvidence='Generated synthetic issue label', orderEvidence='Generated synthetic sequence') for r in rows]))
        catalog = read(output / 'catalog.json')
        result = attach_tocs(output, catalog, sources, temp / 'images', reviews)
        write(output, 'catalog.json', catalog)
        return result
