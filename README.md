# maso-archive

월간 마이크로소프트웨어의 비공식 디지털 아카이브.

Archive target: **November 1983–December 1995 (146 monthly issues)**. The supplied
TOC currently covers 86 issues through December 1990. Official CD holdings support
further extraction; per-disc coverage and completeness remain to be verified.

- [CD1 extraction and reading-room content plan](PLAN-CD1.md)
- [CD2 extraction plan — deferred](PLAN-CD2.md)
- [CD3 extraction plan — deferred](PLAN-CD3.md)
- [Reading-room PRD](PRD-reading-room.md)
- [Detailed design reference](docs/DESIGN-REFERENCE.md)
- [Progress](PROGRESS.md)
- [Offline tasks for the owner](docs/OFFLINE-TASKS.md)
- [TOC import and validation](docs/TOC-IMPORT.md)
- [CD1 reference-index import](docs/CD1-INDEX.md)
- [First CD1-to-TOC metadata match](docs/CD1-MATCH-8802065.md)
- [Pilot raw topic map](docs/CD1-TOPIC-8802065.md)
- [Pilot paragraph decoding](docs/CD1-PARAGRAPH-8802065.md)
- [Pilot RTF feature inventory](docs/CD1-RTF-INVENTORY-8802065.md)
- [Pilot full-text recovery](docs/CD1-TEXT-8802065.md)
- [Pilot structural review and Markdown plan](docs/CD1-BLOCK-STRUCTURE-8802065.md)
- [Pilot semantic block map](docs/CD1-BLOCK-MAP-8802065.md)
- [Pilot private Markdown preview](docs/CD1-MARKDOWN-8802065.md)
- [CD1 extraction findings](docs/CD1-EXTRACTION.md)

Run `make import-toc` to build the local TOC catalog and `make check` to validate
the importer. Requires Python 3.11+ and the dependency in `requirements.txt`.
Generated output is in `build/toc/`; persistent identities are versioned in
`data/identities/toc.json`. Imported metadata is unreviewed and not a public-site
release. Original media, Windows files, and extracted article content stay local.

Run `make import-cd1-index` to structure the three extracted CD1 indexes into
`build/cd1-index/`. This uses the private extraction files and manifest; article
bodies are not read or published.
