"""Translate only registered repository aliases; package symlinks stay forbidden."""
from functools import lru_cache
import json
from pathlib import Path, PurePosixPath

REPOSITORY = Path(__file__).resolve().parents[2]


@lru_cache(maxsize=4)
def _moves(manifest):
    rows = json.loads(manifest.read_text())['moves']
    result = {}
    for row in rows:
        old, new = row['from'], row['to']
        parts = PurePosixPath(new).parts
        if not parts or parts[0] not in ('metadata', 'archive', 'work', 'dist') or '..' in parts:
            raise ValueError('Unsafe canonical storage path')
        result[old] = new
    return result


def canonical_path(path):
    """Resolve a recorded old prefix without allowing arbitrary package symlinks."""
    path = Path(path).absolute()
    try:
        relative = path.relative_to(REPOSITORY)
    except ValueError:
        return path
    if '..' in relative.parts:
        raise ValueError('Unsafe repository path')
    if not relative.parts or relative.parts[0] not in ('data', 'private', 'build', 'output'):
        return path
    manifest = REPOSITORY / 'metadata/storage-layout.json'
    if not manifest.is_file():
        return path  # Unmigrated checkout or synthetic package fixture.
    moves = _moves(manifest)
    parts = relative.parts
    for length in range(min(3, len(parts)), 0, -1):
        prefix = '/'.join(parts[:length])
        if prefix not in moves:
            continue
        target = REPOSITORY / moves[prefix]
        if (REPOSITORY / prefix).resolve() != target.resolve():
            raise ValueError('Storage compatibility link changed: ' + prefix)
        # Every component in canonical preserved storage must remain ordinary.
        current = REPOSITORY
        for component in Path(moves[prefix]).parts:
            current /= component
            if current.is_symlink():
                raise ValueError('Symlink in canonical storage: ' + moves[prefix])
        return target.joinpath(*parts[length:])
    return path
