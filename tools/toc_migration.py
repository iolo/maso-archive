"""Validate an explicit owner-reviewed TOC migration without rewriting witnesses."""
import json
from pathlib import Path
import tempfile

from maso_archive.toc import run_import
from tools.reading_room.export import digest, read, safe
from tools.toc_snapshot import ROOT, Snapshot


def checked(root, record):
    path = safe(Path(root), record['path'])
    if path.stat().st_size != record['bytes'] or digest(path) != record['sha256']:
        raise ValueError('TOC migration input differs: ' + record['path'])
    return path


def load_migration(toc, reference_inputs, root=ROOT):
    """A changed catalog requires pinned history, decisions and exact replay."""
    root, toc = Path(root), Path(toc)
    manifest = read(toc / 'manifest.json')
    source_sha = manifest['source']['sha256']
    if len(source_sha) != 64 or any(c not in '0123456789abcdef' for c in source_sha):
        raise ValueError('Invalid TOC source fingerprint')
    record_path = root / 'data/catalog/toc-migrations' / (source_sha + '.json')
    if not record_path.exists():
        raise ValueError('TOC differs from pinned CD1 reference; reviewed migration required')
    record = read(record_path)
    if record.get('kind') != 'reviewed-toc-migration' or record.get('schema_version') != 1:
        raise ValueError('Unsupported TOC migration')
    for name, key in [('issues.json', 'issues_sha256'), ('toc-entries.jsonl', 'toc_sha256')]:
        if reference_inputs[key] != record['before']['outputs'][name]['sha256']:
            raise ValueError('Migration does not start at this CD1 reference')
    if record['after']['source'] != manifest['source'] or digest(root / 'TOC.md') != source_sha:
        raise ValueError('Migration source differs from current TOC')
    if manifest['outputs'] != record['after']['outputs']:
        raise ValueError('Migration output coverage differs')
    for name, pin in record['after']['outputs'].items():
        if manifest['outputs'].get(name) != pin:
            raise ValueError('Migration output declaration differs')
        checked(toc, dict(pin, path=name))
    if record['after']['identities_sha256'] != manifest['identities_sha256']:
        raise ValueError('Migration identity declaration differs')
    if digest(root / 'data/identities/toc.json') != manifest['identities_sha256']:
        raise ValueError('Migration identity registry differs')
    checked(root, record['previous_snapshot'])
    decisions_path = checked(root, record['decisions'])
    snapshot = Snapshot(root, record['previous_snapshot']['path'])
    snapshot.restore()
    if (snapshot.record['import_manifest']['source'] != record['before']['source'] or
            snapshot.record['import_manifest']['outputs'] != record['before']['outputs']):
        raise ValueError('Migration historical snapshot differs')
    # Replay reviewed decisions from the old allocator; no fuzzy matching here.
    with tempfile.TemporaryDirectory(prefix='toc-migration-') as temp:
        stage = Path(temp)
        identities = stage / 'identities.json'
        identities.write_bytes(snapshot.read('data/identities/toc.json'))
        run_import(root / 'TOC.md', stage / 'toc', identities,
                   decisions_path=decisions_path, **manifest['parameters'])
        if digest(identities) != manifest['identities_sha256']:
            raise ValueError('Migration identities do not reproduce')
        for name, pin in record['after']['outputs'].items():
            if digest(stage / 'toc' / name) != pin['sha256']:
                raise ValueError('Migration catalog does not reproduce')
    old = {e['id']: e for e in snapshot.artifact('toc-entries.jsonl')}
    new = {e['id']: e for e in (json.loads(l) for l in (toc / 'toc-entries.jsonl').read_text().splitlines())}
    retired = record['retired']
    if len({r['id'] for r in retired}) != len(retired) or {r['id'] for r in retired} != old.keys() - new.keys():
        raise ValueError('Migration retirement coverage differs')
    for row in retired:
        if row['before'] != old[row['id']]['raw_text']:
            raise ValueError('Retired TOC text differs')
        target = new.get(row['successor'])
        if row['successor'] is not None and (target is None or
                target['issue_id'] != old[row['id']]['issue_id'] or target['raw_text'] != row['after']):
            raise ValueError('Invalid TOC successor')
    counts = dict(previous_entries=len(old), current_entries=len(new),
                  preserved_ids=len(old.keys() & new.keys()), new_ids=len(new.keys() - old.keys()),
                  retired_ids=len(old.keys() - new.keys()))
    if counts != record['counts']:
        raise ValueError('Migration identity counts differ')
    return record, dict(path=record_path.relative_to(root).as_posix(), sha256=digest(record_path),
                        sourceSha256=source_sha, previousSourceSha256=record['before']['source']['sha256'],
                        counts=counts)


def migrate_links(reviewed, record):
    """Only carry prior reviewed links through explicit same-issue successors."""
    result = {id: list(links) for id, links in reviewed.items()}
    for row in record['retired']:
        previous = result.pop(row['id'], [])
        if row['successor']:
            links = result.setdefault(row['successor'], [])
            links.extend(id for id in previous if id not in links)
    return result
