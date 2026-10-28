# Preserved repository metadata

This is the former top-level `data/` directory. Keep it in Git.

- `identities/`: stable IDs and allocation history; do not regenerate casually.
- `catalog/`: source inventories, decisions, provenance, package records and checkpoints.
- `overrides/`: reviewed human decisions.
- `reference/`: licensed reference and decoding tables.
- `storage-layout.json`: canonical destinations and compatibility paths.

These records describe and pin restoration work; they do not contain all restored
articles. Complete packages and ongoing work live in the separately preserved,
Git-ignored `archive/`. The `data` directory inside an assembled reader is a
separate export format. See [storage and recovery](../docs/STORAGE.md).

Session cleanup excludes `metadata/`. Catalog records about a reader build or
cleanup can remain as provenance even after the generated output is deleted.
Reader builds and release snapshots belong in `dist/`, and temporary processing
belongs in the designated `work/` locations. See
[session cleanup](../docs/STORAGE.md#session-cleanup).

Historical record contents are retained byte-for-byte, including original path
strings. The root `data` compatibility link keeps those paths usable.
