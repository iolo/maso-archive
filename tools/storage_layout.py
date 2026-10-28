"""Map and migrate repository storage while preserving historical artifact bytes.

Use ``python3 -m tools.storage_layout plan`` to inspect the moves, ``migrate``
to apply them, and ``verify`` to check the installed compatibility links.
Old paths remain available for hash-pinned recipes and historical scripts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
from pathlib import Path, PurePosixPath
import subprocess
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'metadata/storage-layout.json'
LOCAL_ROOTS = ('archive', 'work', 'dist')
PDF_VALIDATION_REPEATS = frozenset({
    'pilot-repeat', '6a-matchsticks-repeat', '6b-turbo-pascal-repeat',
    '6c-basic-column-repeat', '7-cd-comparison-repeat', '10-batch-repeat',
})


def pdf_issue(name):
    for prefix, issue in (
        ('11-', '1983-11'), ('12-1984-02', '1984-02'),
        ('12-1984-03', '1984-03'), ('12-1984-05', '1984-05'),
        ('12-1984-06', '1984-06'), ('12-1984-07', '1984-07'),
        ('13-', '1984-08'), ('14-', '1984-09'),
    ):
        if name.startswith(prefix):
            return issue
    return 'shared'


def destination(relative):
    """Return the canonical location of an old repository-relative path."""
    path = PurePosixPath(relative)
    if path.is_absolute() or '..' in path.parts or '\\' in str(relative):
        raise ValueError(f'Unsafe repository path: {relative}')
    parts = path.parts
    if not parts:
        raise ValueError('Empty repository path')
    if parts[0] == 'data':
        return str(PurePosixPath('metadata', *parts[1:]))
    if len(parts) < 2 or parts[0] not in ('private', 'build', 'output'):
        return str(path)
    parent, name, *tail = parts
    if name == 'pdf-restoration' and not tail:
        # This historical container spans several canonical issue directories.
        return str(path)
    if parent == 'output':
        base = f'archive/evidence/{name}'
    elif name == 'pdf-restoration' and tail:
        item, *tail = tail
        issue = pdf_issue(item)
        if parent == 'private':
            base = ('archive/toolchains/ocr' if item == 'ocr-runtime' else
                    f'archive/pdf/{issue}/restoration/{item}')
        elif parent == 'build' and item in PDF_VALIDATION_REPEATS:
            base = f'work/validation/pdf-shared/{item}'
        elif item.endswith('-reference') and issue != 'shared':
            base = f'archive/pdf/{issue}/reference'
        elif any(word in item for word in ('-repeat', '-evidence', '-draft', '-closeout', '-config', '-map', '-before-')):
            base = f'archive/pdf/{issue}/evidence/{item}'
        else:
            base = f'archive/pdf/{issue}/packages/{item}'
    elif parent == 'build' and name in ('reading-room-packages', 'reading-room-examples'):
        base = f'archive/cd1/packages/{name}'
    elif parent == 'build' and name.startswith('reading-room'):
        base = ('dist/reading-room' if name == 'reading-room-volunteer' else
                'dist/reading-room-cd' if name == 'reading-room' else f'dist/{name}')
    elif name.startswith(('cd1-', 'cd2-', 'cd3-')):
        disc = name[:3]
        if parent == 'private' and name == f'{disc}-probe':
            base = f'archive/{disc}/extraction'
        elif name == f'{disc}-reference':
            base = f'archive/{disc}/reference'
        elif name in (f'{disc}-articles', f'{disc}-issues'):
            base = f'archive/{disc}/packages/{name}'
        else:
            base = f'archive/{disc}/evidence/{name}'
    elif parent == 'build' and name == 'toc':
        base = 'archive/toc/current'
    elif parent == 'build' and name == 'toc-snapshots':
        base = 'work/cache/toc-snapshots'
    elif parent == 'build' and name == 'toc-images':
        base = 'archive/toc/images'
    elif parent == 'private' and name == 'toc-restoration':
        base = 'archive/toc/restoration'
    elif name == 'cover-inventory':
        base = 'archive/covers/inventory'
    elif name == 'cover-thumbnails':
        base = 'archive/covers/derivatives'
    elif name.startswith('cover-'):
        base = f'archive/covers/evidence/{name}'
    elif name == 'ocr-qwen3-vl':
        base = 'archive/experiments/ocr-qwen3-vl'
    elif name == 'reading-room-deploy':
        base = 'archive/operations/reading-room-deploy'
    elif name == 'preservation':
        base = 'archive/preservation'
    elif name == 'build-cleanup' or name.startswith('documentation-'):
        base = f'archive/migrations/{name}'
    elif name.endswith('.md'):
        base = f'archive/plans/{name}'
    else:
        base = f'archive/evidence/{name}'
    return str(PurePosixPath(base, *tail))


def preserved_input(root, canonical, legacy):
    """Prefer canonical inputs; support unmigrated fixtures without hiding loss."""
    root = Path(root)
    current = root / canonical
    if current.exists() or (root / MANIFEST).exists():
        return current
    previous = root / legacy
    return previous if previous.exists() else current


def is_local_output(path, root=ROOT):
    """Accept canonical local storage and existing legacy local directories."""
    path, root = Path(path).resolve(), Path(root).resolve()
    reserved = [root / name for name in LOCAL_ROOTS] + [root / 'archive/legacy-paths']
    reserved += [(root / name).resolve() for name in ('private', 'build', 'output')]
    if path in reserved:
        return False
    if any(path.is_relative_to(root / name) for name in LOCAL_ROOTS):
        return True
    # Synthetic fixtures and repositories not yet migrated retain these roots.
    return any(not (root / name).is_symlink() and path.is_relative_to(root / name)
               for name in ('private', 'build'))


def plan(root=ROOT):
    root = Path(root).resolve()
    rows = []
    for name in ('data', 'private', 'build', 'output'):
        base = root / name
        if not base.exists() or base.is_symlink():
            continue
        if name == 'data':
            candidates = [base]
        else:
            candidates = []
            for child in sorted(base.iterdir()):
                if child.name == 'pdf-restoration' and child.is_dir():
                    candidates.extend(sorted(child.iterdir()))
                else:
                    candidates.append(child)
        for source in candidates:
            old = source.relative_to(root).as_posix()
            new = destination(old)
            if old == new:
                raise ValueError(f'No destination for {old}')
            target = root / new
            if target.exists() or target.is_symlink():
                raise ValueError(f'Destination already exists: {new}')
            rows.append({'from': old, 'to': new})
    destinations = [r['to'] for r in rows]
    if len(set(destinations)) != len(destinations):
        raise ValueError('Colliding storage destinations')
    for path in destinations:
        if any(str(p) in destinations for p in PurePosixPath(path).parents):
            raise ValueError(f'Overlapping destination: {path}')
    return rows


def _link(path, target):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        if path.resolve() != target.resolve():
            raise ValueError(f'Conflicting compatibility link: {path}')
        return
    if path.exists():
        raise ValueError(f'Compatibility path already exists: {path}')
    path.symlink_to(os.path.relpath(target, path.parent), target_is_directory=target.is_dir())


def install_compatibility(root, rows):
    root = Path(root).resolve()
    legacy = root / 'archive/legacy-paths'
    for row in rows:
        old, new = row['from'], row['to']
        if old == 'data':
            continue
        _link(legacy / old, root / new)
    for name in ('private', 'build', 'output'):
        (legacy / name).mkdir(parents=True, exist_ok=True)
        old = root / name
        # All original children have been moved. Only empty containers remain.
        if old.is_dir() and not old.is_symlink():
            for base, dirs, files in os.walk(old, topdown=False):
                if files or any((Path(base) / d).is_symlink() for d in dirs):
                    raise ValueError(f'Unmoved files remain: {base}')
                Path(base).rmdir()
        _link(old, legacy / name)
    _link(root / 'data', root / 'metadata')


def verify(root=ROOT):
    root = Path(root).resolve()
    manifest = json.loads((root / MANIFEST).read_text())
    problems, regenerable_missing = [], []
    for row in manifest['moves']:
        old, new = root / row['from'], root / row['to']
        if old.resolve() != new.resolve():
            problems.append(row)
        elif not new.exists():
            (regenerable_missing if row['to'].split('/')[0] in ('work', 'dist') else problems).append(row)
    if problems:
        raise ValueError(f'Storage compatibility differs: {problems[:5]}')
    return {'moves': len(manifest['moves']), 'compatibility': 'verified',
            'regenerable_missing': regenerable_missing}


def migrate(root=ROOT):
    root = Path(root).resolve()
    if (root / MANIFEST).exists():
        manifest = json.loads((root / MANIFEST).read_text())
        install_compatibility(root, manifest['moves'])
        return verify(root)
    receipt_dir = root / 'archive/migrations/storage-2026-10-16'
    receipt_plan = receipt_dir / 'plan.json'
    identity = lambda s: [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns]
    if receipt_plan.exists():
        saved = json.loads(receipt_plan.read_text())
        rows, source_head = saved['moves'], saved['source_git_commit']
    else:
        rows = plan(root)
        if not rows or not any(r['from'] == 'data' for r in rows):
            raise ValueError('Expected the original storage layout')
        source_head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
        for row in rows:
            row['original_identity'] = identity((root / row['from']).lstat())
        for name in ('archive', 'work', 'dist'):
            (root / name).mkdir(exist_ok=True)
        receipt_dir.mkdir(parents=True, exist_ok=True)
        receipt_plan.write_text(json.dumps(dict(source_git_commit=source_head, moves=rows), indent=2) + '\n')
    journal = receipt_dir / 'moves.jsonl'
    # Cross-boundary relative symlinks would require their own reviewed migration.
    # Reject them before any move rather than changing retained evidence bytes.
    for row in rows:
        source = root / row['from']
        if not source.exists():
            source = root / row['to']
        if not source.is_dir():
            continue
        for base, dirs, files in os.walk(source, followlinks=False):
            for name in dirs + files:
                p = Path(base) / name
                if p.is_symlink():
                    target = os.readlink(p)
                    if not os.path.isabs(target) and not p.resolve().is_relative_to(source.resolve()):
                        raise ValueError(f'Relative symlink crosses moved tree: {p.relative_to(root)}')
    with journal.open('a') as log:
        for row in rows:
            old, new = root / row['from'], root / row['to']
            new.parent.mkdir(parents=True, exist_ok=True)
            if not old.exists() and new.exists():
                if identity(new.lstat()) != row['original_identity']:
                    raise ValueError(f'Resumed destination identity differs: {row}')
                continue
            before = old.lstat()
            if identity(before) != row['original_identity'] or new.exists():
                raise ValueError(f'Source or destination changed during migration: {row}')
            if before.st_dev != new.parent.stat().st_dev:
                raise ValueError(f'Cross-filesystem move refused: {row}')
            old.rename(new)
            after = new.lstat()
            if identity(before) != identity(after):
                raise ValueError(f'Move changed artifact identity: {row}')
            log.write(json.dumps(dict(row, inode=after.st_ino, device=after.st_dev,
                                      mode=after.st_mode, bytes=after.st_size, mtime_ns=after.st_mtime_ns)) + '\n')
            log.flush()
            os.fsync(log.fileno())
    manifest = dict(schema_version=1, date='2026-10-16', source_git_commit=source_head,
                    policy='Retained bytes and logical paths in historical evidence are unchanged. Old root names are compatibility links; use canonical destinations for new work.',
                    moves=[{k: row[k] for k in ('from', 'to')} for row in rows])
    (root / MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    install_compatibility(root, rows)
    return verify(root)



READER_RELEASE = 'dist/releases/reading-room-2026-10-16'


def file_inventory(directory):
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f'Expected an ordinary directory: {directory}')
    result = []
    def fail(error):
        raise error
    for base, dirs, files in os.walk(directory, onerror=fail):
        if any((Path(base) / name).is_symlink() for name in dirs + files):
            raise ValueError('Release snapshots must contain ordinary files/directories')
        for name in files:
            path = Path(base) / name
            if not stat.S_ISREG(path.stat().st_mode):
                raise ValueError(f'Expected an ordinary file: {path}')
            with path.open('rb') as stream:
                checksum = hashlib.file_digest(stream, 'sha256').hexdigest()
            result.append(dict(path=path.relative_to(directory).as_posix(),
                               bytes=path.stat().st_size, sha256=checksum))
    return sorted(result, key=lambda row: row['path'])


def release_path(root, release=None):
    name = release or Path(READER_RELEASE).name
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', name):
        raise ValueError('Release name must use letters, digits, hyphens or underscores')
    target = root / 'dist/releases' / name
    # Keep both the release tree and its receipt out of compatibility links.
    if any(p.is_symlink() for p in (root/'dist', target.parent, target, target.with_suffix('.json'))):
        raise ValueError('Release paths must not be symlinks')
    return target


def snapshot_reader(root=ROOT, release=None, source=None):
    """Copy a named optional deployment snapshot inside dist/."""
    root = Path(root).resolve()
    source = Path(source or 'dist/reading-room')
    source = (root / source).resolve()
    if not source.is_relative_to(root/'dist') or source == root/'dist':
        raise ValueError('Reader snapshot source must be a directory inside dist/')
    target = release_path(root, release)
    if source.is_relative_to(target.parent) or target.parent.is_relative_to(source):
        raise ValueError('Reader snapshot source must be outside dist/releases/')
    relative = target.relative_to(root).as_posix()
    receipt = target.with_suffix('.json')
    before = file_inventory(source)
    if not before or not (source / 'index.html').is_file() or not (source / 'data/manifest.json').is_file():
        raise ValueError('Expected the prepared reading room')
    record = dict(source=source.relative_to(root).as_posix(), files=before)
    if target.exists():
        if not receipt.exists() or file_inventory(target) != json.loads(receipt.read_text())['files']:
            raise ValueError('Existing release snapshot is incomplete or changed')
        if before != json.loads(receipt.read_text())['files']:
            raise ValueError('Reader differs from this saved release; choose a new --release name')
        return {'release': relative, 'status': 'verified'}
    if receipt.exists() and json.loads(receipt.read_text()) != record:
        raise ValueError('Existing release receipt differs; choose a new --release name')
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.snapshot-', dir=target.parent) as directory:
        stage = Path(directory) / 'reader'
        shutil.copytree(source, stage)
        if file_inventory(stage) != before:
            raise ValueError('Release copy differs from the source')
        # Install the receipt first. If interrupted before the tree rename, the
        # same inputs can resume; a different reader cannot claim that release.
        from tools.preserved_output import put
        put(target.parent, receipt.name, json.dumps(record, indent=2) + '\n')
        if target.exists():
            raise ValueError('Release destination appeared during the snapshot')
        stage.rename(target)
    return {'release': relative, 'files': len(before), 'status': 'copied and verified'}


def restore_reader(root=ROOT, output=None, release=None):
    """Copy an optional deployment snapshot without overwriting existing output."""
    root = Path(root).resolve()
    source = release_path(root, release)
    output = Path(output or root / 'dist/reading-room')
    if not output.is_absolute():
        output = root / output
    if output.is_symlink():
        raise ValueError('Reader restore output must not be a symlink')
    output = output.resolve()
    if not output.is_relative_to(root / 'dist') or output == root / 'dist':
        raise ValueError('Reader restore output must be a directory inside dist/')
    if output.is_relative_to(source.parent):
        raise ValueError('Reader restore output must be outside dist/releases/')
    if output.exists():
        raise ValueError('Reader restore output already exists; choose a new directory')
    expected = json.loads(source.with_suffix('.json').read_text())['files']
    if file_inventory(source) != expected:
        raise ValueError('Release snapshot differs from its receipt')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.restore-', dir=output.parent) as directory:
        stage = Path(directory) / 'reader'
        shutil.copytree(source, stage)
        if file_inventory(stage) != expected:
            raise ValueError('Reader restore differs from the release snapshot')
        if output.exists():
            raise ValueError('Reader restore output appeared during restore')
        stage.rename(output)
    return {'output': output.relative_to(root).as_posix(), 'release': source.relative_to(root).as_posix(),
            'files': len(expected), 'status': 'restored and verified'}



def restore_retired(name, root=ROOT):
    """Run only the preserved cleanup archive's restore action with relocated roots."""
    import importlib.util
    root = Path(root).resolve()
    path = root / 'archive/migrations/build-cleanup/2026-10-14/cleanup.py'
    if hashlib.sha256(path.read_bytes()).hexdigest() != 'd54ec7766083b775286173b0ff5c0a5e1a6b40a16fbb1ebf09b81306f487246b':
        raise ValueError('Historical cleanup restore implementation changed')
    spec = importlib.util.spec_from_file_location('retired_reader_restore', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # That script originally inferred ROOT from its depth. Leave its retained
    # source untouched and supply the real root only in this restore adapter.
    module.ROOT = root
    original_safe = module.safe
    module.safe = lambda relative: original_safe(relative).resolve()
    module.restore(name)
    return {'restored': name}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('plan', 'migrate', 'compat', 'verify', 'lookup', 'snapshot-reader', 'restore-reader', 'restore-retired'))
    parser.add_argument('path', nargs='?')
    parser.add_argument('--release', help='Named saved reader; required for snapshot-reader')
    parser.add_argument('--source', help='Snapshot source inside dist/ (default: dist/reading-room)')
    args = parser.parse_args()
    if args.release and args.action not in ('snapshot-reader', 'restore-reader'):
        parser.error('--release is only valid for snapshot-reader or restore-reader')
    if args.source and args.action != 'snapshot-reader':
        parser.error('--source is only valid for snapshot-reader')
    if args.path and args.action not in ('lookup', 'restore-reader', 'restore-retired'):
        parser.error('This action does not accept a positional path')
    if args.action == 'lookup':
        if not args.path:
            parser.error('lookup requires an old repository-relative path')
        print(destination(args.path))
    elif args.action == 'plan':
        print(json.dumps(plan(), indent=2))
    elif args.action == 'migrate':
        print(json.dumps(migrate()))
    elif args.action == 'restore-retired':
        if not args.path:
            parser.error('restore-retired requires a snapshot name')
        print(json.dumps(restore_retired(args.path)))
    elif args.action == 'snapshot-reader':
        if not args.release:
            parser.error('snapshot-reader requires --release NAME; use a new name for each release')
        print(json.dumps(snapshot_reader(release=args.release, source=args.source)))
    elif args.action == 'restore-reader':
        print(json.dumps(restore_reader(output=args.path, release=args.release)))
    elif args.action == 'compat':
        rows = json.loads((ROOT / MANIFEST).read_text())['moves']
        install_compatibility(ROOT, rows)
        print('Historical path links installed; restore missing archive data from backup before verification.')
    else:
        print(json.dumps(verify()))


if __name__ == '__main__':
    main()
