"""Immutable, hash-checked stage generations; atomic publication and crash recovery."""
import json
import os
from pathlib import Path
import tempfile
import uuid

from maso_archive.reading_room_package import checked_file, file_record
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from tools.recover_cd1_text import json_bytes


def key(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


def write(path, raw):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.write-', delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def verify(root, fingerprint):
    root = Path(root)
    require(not root.is_symlink(), 'Symlink stage root')
    manifest = json.loads((root / 'checkpoint.json').read_bytes())
    require(manifest['fingerprint'] == fingerprint, 'Stale checkpoint')
    paths = [r['path'] for r in manifest['outputs']]
    require(len(paths) == len(set(paths)), 'Duplicate checkpoint output')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(not any(p.is_symlink() for p in root.rglob('*')), 'Symlink checkpoint output')
    require(actual == set(paths) | {'checkpoint.json'}, 'Checkpoint population differs')
    for record in manifest['outputs']:
        checked_file(root, record)
    return manifest


class Cache:
    def __init__(self, root, identity):
        self.root, self.identity = Path(root), identity
        self.events = []

    def stage(self, name, inputs, produce, validate=None):
        require(all(c.isalnum() or c in '-_.' for c in name) and name not in ('.', '..'), 'Unsafe stage name')
        fingerprint = key({'identity': self.identity, 'stage': name, 'inputs': inputs})
        parent = self.root / name
        final = parent / fingerprint
        parent.mkdir(parents=True, exist_ok=True)
        try:
            manifest = verify(final, fingerprint)
            if validate:
                validate(final)
            self.events.append({'stage': name, 'fingerprint': fingerprint, 'cache': 'hit'})
            return final, manifest
        except (OSError, ValueError, KeyError):
            pass
        # An interrupted process leaves .stage-* evidence; only a validated final
        # generation is reusable. Prior successful generations are never deleted.
        stage = Path(tempfile.mkdtemp(prefix='.stage-', dir=parent))
        try:
            produce(stage)
            require(not (stage / 'checkpoint.json').exists(), 'Producer owns reserved checkpoint path')
            records = [file_record(p.relative_to(stage).as_posix(), p.read_bytes())
                       for p in sorted(stage.rglob('*')) if p.is_file()]
            manifest = {'version': 1, 'fingerprint': fingerprint, 'identity': self.identity, 'inputs': inputs, 'outputs': records}
            (stage / 'checkpoint.json').write_bytes(json_bytes(manifest))
            verify(stage, fingerprint)
            if validate:
                validate(stage)
            if final.exists():
                final.rename(parent / ('.invalid-' + uuid.uuid4().hex))
            stage.rename(final)
        except Exception as error:
            write(stage / 'failure.json', json_bytes({'stage': name, 'fingerprint': fingerprint,
                                                    'error_type': type(error).__name__, 'error': str(error)}))
            self.events.append({'stage': name, 'fingerprint': fingerprint, 'cache': 'failed', 'evidence': str(stage)})
            raise
        self.events.append({'stage': name, 'fingerprint': fingerprint, 'cache': 'built'})
        return final, manifest
