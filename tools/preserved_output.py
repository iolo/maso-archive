"""Publish retained CD results without replacing previous restoration work."""
from pathlib import Path
import os
import tempfile

from tools.storage_layout import file_inventory


def prepare_output(path, *, verify_existing=False):
    # Resolve historical aliases before publishing; never replace the link itself.
    path = Path(path).resolve()
    if verify_existing:
        if not path.is_dir():
            raise ValueError(f'Verification requires an existing directory: {path}')
    elif path.exists():
        raise ValueError(f'Preserved output already exists: {path}; use --resume, '
                         '--verify-existing, or a fresh --output')
    return path


def publish_tree(stage, target, *, verify_existing=False):
    target = prepare_output(target, verify_existing=verify_existing)
    if verify_existing:
        if file_inventory(stage) != file_inventory(target):
            raise ValueError(f'Preserved output rebuild differs: {target}')
        return  # Compare actual bytes, including extra files; keep inodes/mtimes.
    # Callers stage on the destination filesystem. A nonempty destination that
    # appears concurrently makes rename fail; no existing tree is removed.
    Path(stage).rename(target)


def put(root, name, data, *, verify_existing=False):
    """Add an immutable file, or verify identical bytes without writing it."""
    target = Path(root) / name
    raw = data.encode('utf-8') if isinstance(data, str) else data
    if target.is_symlink():
        raise ValueError(f'Symlink in preserved output: {target}')
    if target.exists():
        if target.read_bytes() != raw:
            raise ValueError(f'Preserved file differs: {target}; choose a fresh --output')
        return
    if verify_existing:
        raise ValueError(f'Missing preserved file: {target}')
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix='.preserve-', dir=target.parent) as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
        # Atomic creation, with no overwrite if another process publishes first.
        try:
            os.link(stream.name, target)
        except FileExistsError:
            if target.is_symlink() or target.read_bytes() != raw:
                raise ValueError(f'Concurrent preserved output differs: {target}')
