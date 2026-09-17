# maso-archive

월간 마이크로소프트웨어의 비공식 디지털 아카이브.

- [Implementation plan](PLAN.md)
- [Progress](PROGRESS.md)
- [TOC import and validation](docs/TOC-IMPORT.md)
- [CD1 extraction findings](docs/CD1-EXTRACTION.md)

Run `make import-toc` to build the local TOC catalog and `make check` to validate
the importer. Requires Python 3.11+ and the dependency in `requirements.txt`.
Generated output is in `build/toc/`; persistent identities are versioned in
`data/identities/toc.json`. Imported metadata is unreviewed and not a public-site
release. Original media, Windows files, and extracted article content stay local.
