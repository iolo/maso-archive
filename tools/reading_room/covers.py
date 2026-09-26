"""Attach optional owner-supplied covers by date without changing source references."""
from pathlib import Path
import re

from PIL import Image

from .export import copy, digest, read, safe, write


def attach_covers(output, catalog, directory):
    if directory is None or not Path(directory).exists():
        return []
    directory = Path(directory)
    by_date = {}
    for path in sorted(directory.iterdir()):
        if path.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.webp'):
            continue
        match = re.fullmatch(r'maso(\d{2})(\d{2})\.(jpg|jpeg|png|webp)', path.name, re.I)
        if not match or not 1 <= int(match[2]) <= 12:
            raise ValueError(f'Cover filename must be masoYYMM.jpg/png/webp: {path.name}')
        date = (1900 + int(match[1]), int(match[2]))
        if date in by_date:
            raise ValueError(f'Duplicate cover for {date[0]}-{date[1]:02}: {path.name}')
        safe(directory, path.name)
        with Image.open(path) as picture:
            expected = {'.jpg': 'JPEG', '.jpeg': 'JPEG', '.png': 'PNG', '.webp': 'WEBP'}[path.suffix.lower()]
            if picture.format != expected:
                raise ValueError(f'Cover format disagrees with filename: {path.name}')
            width, height = picture.size
            picture.verify()
        by_date[date] = (path, width, height)
    records = []
    for date, (path, width, height) in by_date.items():
        issues = [i for i in catalog['issues'] if (i['year'], i['month']) == date]
        if not issues:
            continue  # The supplied cover may be outside this export's issue slice.
        copy(directory, output / 'covers', path.name)
        cover = {'path': f'covers/{path.name}', 'width': width, 'height': height,
                 'sha256': digest(path)}
        for issue in issues:
            issue['cover'] = cover
            name = f'issues/{issue["id"].removeprefix("maso-")}.json'
            doc = read(output / name)
            doc['issue'] = issue
            write(output, name, doc)
        records.append({'filename': path.name, **cover, 'issueIds': [i['id'] for i in issues]})
    return records
