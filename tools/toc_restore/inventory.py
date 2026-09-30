"""Inventory and reversibly normalize donated TOC JPEG filenames."""
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import re

from PIL import Image

from tools.reading_room.export import ROOT, digest, read, safe
from tools.reading_room.covers import date_label, separate

PRIVATE = ROOT / 'private/toc-restoration'
SOURCES = ROOT / 'tocs'
NORMAL = re.compile(r'(\d{4})-(\d{2})\.jpg')


def save(path, value):
    """Replace a journal only after its complete contents are on disk."""
    path = Path(path)
    if path.is_symlink():
        raise ValueError('Unsafe evidence symlink')
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('w', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def inventory(directory=SOURCES):
    directory = Path(directory)
    groups = defaultdict(list)
    errors, ignored = [], []
    for path in sorted(directory.rglob('*')):
        if path.is_dir():
            continue
        relative = path.relative_to(directory).as_posix()
        if path.name == '.DS_Store':
            ignored.append(relative)
            continue
        try:
            safe(directory, relative)
            match = NORMAL.fullmatch(relative)
            if match:
                label, number = match.groups()
                number = int(number)
                normalized = True
                if not number:
                    raise ValueError('Sequence starts at 01')
            else:
                old = re.fullmatch(r'(\d{4})/[^/]*?(\d+)\.(?:jpg|jpeg)', relative, re.I)
                if not old:
                    raise ValueError('Unrecognized source filename')
                label, number = old.groups()
                number, normalized = int(number), False
            date_label(label)
            with Image.open(path) as image:
                image.load()
                if image.format != 'JPEG':
                    raise ValueError('Expected JPEG encoding')
                dimensions = list(image.size)
            groups[label].append(dict(old=relative, date=label, sourceNumber=number,
                                      normalized=normalized, dimensions=dimensions,
                                      bytes=path.stat().st_size, sha256=digest(path)))
        except (ValueError, OSError) as exc:
            errors.append(dict(path=relative, error=str(exc)))
    records = []
    for label, rows in sorted(groups.items()):
        rows.sort(key=lambda r: (r['sourceNumber'], r['old']))
        if len({r['sourceNumber'] for r in rows}) != len(rows):
            errors.append(dict(date=label, error='Ambiguous numeric order'))
        if any(r['normalized'] for r in rows) and not all(r['normalized'] for r in rows):
            errors.append(dict(date=label, error='Mixed old/new donations require an explicit reviewed mapping'))
        for sequence, row in enumerate(rows, 1):
            seq = row['sourceNumber'] if row['normalized'] else sequence
            if seq > 99:
                errors.append(dict(date=label, error='Sequence exceeds two digits'))
            records.append(dict(row, sequence=seq, new=f'{label}-{seq:02}.jpg'))
    hashes = Counter(r['sha256'] for r in records)
    missing = [f'{year:02}{month:02}' for year in range(83, 96) for month in range(1, 13)
               if '8311' <= f'{year:02}{month:02}' <= '9512' and f'{year:02}{month:02}' not in groups]
    return dict(version=1, directory=str(directory.resolve()), records=records, errors=errors,
                ignored=ignored, duplicates=[h for h, n in hashes.items() if n > 1],
                missing=missing, summary=dict(images=len(records), issues=len(groups),
                    bytes=sum(r['bytes'] for r in records), pageSets={str(k):v for k,v in Counter(map(len, groups.values())).items()}))


def verify_reviews(manifest, reviews):
    reviewed = {r['sha256']: r for r in reviews['pages']}
    for row in manifest['records']:
        review = reviewed.get(row['sha256'], {})
        if (review.get('date') != row['date'] or review.get('sequence') != row['sequence']
                or not review.get('identityEvidence') or not review.get('orderEvidence')):
            raise ValueError(f'Missing visual identity/order review: {row["old"]}')


def normalize(manifest_path, reviews_path, journal_path, rollback=False):
    manifest, reviews = read(Path(manifest_path)), read(Path(reviews_path))
    root = Path(manifest['directory'])
    separate(Path(journal_path), root)
    if manifest['errors'] or manifest['duplicates']:
        raise ValueError('Resolve inventory errors/duplicate images before normalization')
    verify_reviews(manifest, reviews)
    key = fingerprint(manifest)
    journal_path = Path(journal_path)
    journal = read(journal_path) if journal_path.exists() else dict(manifest=key, state='pending')
    if journal['manifest'] != key:
        raise ValueError('Journal belongs to another inventory')
    moves = [r for r in manifest['records'] if r['old'] != r['new']]
    # Inspect all locations before any mutation. Each source must exist exactly
    # once; this also resumes a crash between a move and its journal update.
    locations, redundant = [], []
    for i, row in enumerate(moves):
        names = [row['old'], f'.toc-rename-{key[:16]}-{i}.jpg', row['new']]
        present = [name for name in names if safe(root, name).exists()]
        if not present or any(digest(safe(root, name)) != row['sha256'] for name in present):
            raise ValueError(f'Collision, missing or changed source: {row["old"]}')
        if len(present) > 1 and not all(safe(root, present[0]).samefile(safe(root, name)) for name in present[1:]):
            raise ValueError(f'Collision at destination: {row["old"]}')
        current = present[0] if rollback else present[-1]
        redundant.extend(safe(root, name) for name in present if name != current)
        locations.append((row, names, current))
    journal['state'] = 'rolling-back' if rollback else 'applying'
    save(journal_path, journal)
    for path in redundant:
        path.unlink()  # Recover only duplicate hard links proven to be our source.
    for row, names, current in locations:
        destination = names[0] if rollback else names[2]
        if current == destination:
            continue
        if digest(safe(root, current)) != row['sha256']:
            raise ValueError('Source changed before move')
        # link/unlink gives no-overwrite semantics on this same-filesystem move.
        # A crash leaving two names is recovered by the same-inode preflight.
        intermediate = names[1]
        for target in ([intermediate, destination] if current != intermediate else [destination]):
            source, target_path = safe(root, current), safe(root, target)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            os.link(source, target_path)
            source.unlink()
            current = target
            journal['lastMove'] = dict(source=row['old'], current=current)
            save(journal_path, journal)
    after = Counter(digest(safe(root, r['old'] if rollback else r['new'])) for r in manifest['records'])
    if after != Counter(r['sha256'] for r in manifest['records']):
        raise ValueError('Source hash multiset differs after normalization')
    journal['state'] = 'rolled-back' if rollback else 'complete'
    save(journal_path, journal)
    return journal
