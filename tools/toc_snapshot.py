"""Explicit historical TOC inputs for the two CD1 witnesses and coverage audit.

Logical paths in their original provenance keep their original meanings/hashes.
Current imports always use build/toc; historical readers use this separate cache.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from maso_archive.reading_room_package import checked_file
from maso_archive.toc import run_import

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = "7d4386d31559383e8ddf14ca60dcaa3464aef52cf4d3ac50ca5a993ab422e34e"
RECORD = f"data/catalog/toc-snapshots/{SOURCE_SHA}.json"


class Snapshot:
    def __init__(self, root=ROOT):
        self.root = Path(root)
        self.record = json.loads((self.root / RECORD).read_bytes())
        if self.record["source_sha256"] != SOURCE_SHA:
            raise ValueError("Unexpected historical TOC source")
        self.directory = self.root / "build/toc-snapshots" / SOURCE_SHA
        self.files = {r["path"]: r for r in self.record["files"]}
        if len(self.files) != len(self.record["files"]):
            raise ValueError("Duplicate snapshot paths")

    def read(self, path):
        if not self.directory.exists():
            raise ValueError("Historical TOC cache missing; run make restore-toc-snapshot")
        return checked_file(self.directory, self.files[path])

    def artifact(self, name):
        raw = self.read("build/toc/" + name)
        return json.loads(raw) if name.endswith(".json") else [json.loads(line) for line in raw.splitlines()]

    def restore(self):
        """Reproduce data from Git; retain the recorded historical import manifest."""
        if self.directory.exists():
            for path in self.files:
                self.read(path)
            return
        self.directory.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=self.directory.parent) as temporary:
            stage = Path(temporary) / "snapshot"
            stage.mkdir()
            for path, key in (("TOC.md", "source_git_blob"), ("data/identities/toc.json", "identities_git_blob")):
                raw = subprocess.check_output(["git", "cat-file", "blob", self.record[key]], cwd=self.root)
                destination = stage / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(raw)
                checked_file(stage, self.files[path])
            manifest = self.record["import_manifest"]
            run_import(stage / "TOC.md", stage / "build/toc", stage / "data/identities/toc.json",
                       **manifest["parameters"])
            # Reproduced data must match every recorded byte. The manifest itself
            # records the historical Python/dependency versions, not this run's.
            for path, record in self.files.items():
                if path != "build/toc/manifest.json":
                    checked_file(stage, record)
            raw = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
            (stage / "build/toc/manifest.json").write_bytes(raw)
            checked_file(stage, self.files["build/toc/manifest.json"])
            if hashlib.sha256((self.root / "schemas/toc-import.schema.json").read_bytes()).hexdigest() != manifest["schema_sha256"]:
                raise ValueError("Historical TOC schema changed")
            stage.rename(self.directory)


def read_input(root, path):
    """Read pinned historical paths explicitly; all other inputs remain current."""
    path = Path(path)
    relative = path.relative_to(root).as_posix() if path.is_absolute() else path.as_posix()
    snapshot = Snapshot(root)
    return snapshot.read(relative) if relative in snapshot.files else (Path(root) / relative).read_bytes()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        Snapshot().restore()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"TOC snapshot restore failed: {exc}", file=sys.stderr)
        return 1
    print(f"Historical TOC snapshot verified: {SOURCE_SHA}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
