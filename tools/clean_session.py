"""Preview or remove disposable session outputs; preserved storage is never scanned."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import stat
import subprocess

from tools.storage_layout import ROOT


SESSION_PATHS = ('work/tmp', 'work/validation', 'work/reading-room')
CACHE_PATH = 'work/cache/toc-snapshots'


def ordinary_path(root, relative):
    """Reject symlinks in a deletion target or its parents, including dangling links."""
    path = root
    for part in Path(relative).parts:
        path /= part
        if path.is_symlink():
            raise ValueError(f'Cleanup path must not be a symlink: {path.relative_to(root)}')
    return path


def allocated_bytes(path):
    """Estimate allocated space without following links or crossing mount points."""
    info = path.lstat()
    total = info.st_blocks * 512
    if stat.S_ISDIR(info.st_mode):
        if path.is_mount():
            raise ValueError(f'Cleanup will not cross a mount point: {path}')
        with os.scandir(path) as entries:
            for entry in entries:
                total += allocated_bytes(Path(entry.path))
    elif not (stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode)):
        raise ValueError(f'Cleanup encountered a special file: {path}')
    return total


def plan(root=ROOT, *, include_dist=False, include_caches=False):
    root = Path(root).resolve()
    selected = list(SESSION_PATHS)
    if include_caches:
        selected.append(CACHE_PATH)
    if include_dist:
        directory = ordinary_path(root, 'dist')
        if directory.exists():
            selected.extend(p.relative_to(root).as_posix() for p in sorted(directory.iterdir())
                            if p.name != 'README.md')
    tracked = [Path(os.fsdecode(name)) for name in subprocess.check_output(
        ['git', 'ls-files', '-z', '--', 'work', 'dist'], cwd=root).split(b'\0') if name]
    result = []
    for relative in selected:
        path = ordinary_path(root, relative)
        if not path.exists():
            continue
        if any(name == Path(relative) or name.is_relative_to(relative) for name in tracked):
            raise ValueError(f'Cleanup target contains Git-tracked files: {relative}')
        result.append(dict(path=relative, allocated_bytes=allocated_bytes(path)))
    return result


def clean(root=ROOT, *, apply=False, include_dist=False, include_caches=False):
    root = Path(root).resolve()
    # Finish every target's checks before deleting anything.
    candidates = plan(root, include_dist=include_dist, include_caches=include_caches)
    if apply:
        for row in candidates:
            path = ordinary_path(root, row['path'])
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    return candidates


def size(value):
    for unit in ('B', 'KiB', 'MiB', 'GiB', 'TiB'):
        if value < 1024 or unit == 'TiB':
            return f'{value:.1f} {unit}'
        value /= 1024


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Delete the listed outputs; default is preview only')
    parser.add_argument('--include-dist', action='store_true', help='Also remove generated readers and release snapshots')
    parser.add_argument('--include-caches', action='store_true', help='Also remove reproducible historical TOC snapshots')
    args = parser.parse_args()
    try:
        rows = clean(apply=args.apply, include_dist=args.include_dist, include_caches=args.include_caches)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'Cleanup stopped: {error}\n')
    action = 'Removed' if args.apply else 'Would remove'
    if not rows:
        print('No disposable outputs found in the selected locations.')
    for row in rows:
        print(f'{action} {row["path"]} ({size(row["allocated_bytes"])})')
    if rows:
        print(f'Estimated allocated space: {size(sum(row["allocated_bytes"] for row in rows))}')
        if not args.apply:
            print('Preview only. Add --apply to delete these outputs.')


if __name__ == '__main__':
    main()
