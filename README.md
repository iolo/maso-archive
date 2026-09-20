# maso-archive

월간 마이크로소프트웨어의 비공식 디지털 아카이브.

Archive target: **November 1983–December 1995 (146 monthly issues)**. The reviewed
TOC import covers 122 issues through December 1993, with 5,497 entries.
Official CD holdings support
further extraction; per-disc coverage and completeness remain to be verified.

Next milestone: **the first complete CD1 extraction pass**. The approved sequence
is processing inventory → shared batch pipeline → February regression and a sample
from other issues → resumable processing across CD1. Step 13a is complete;
the shared runner in **13b is next**. Full-disc processing begins after the batch
validation checkpoint. See the plan for checks.

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
- [Pilot image map and conversion findings](docs/CD1-IMAGES-8802065.md)
- [Reading-room content contract v1](docs/READING-ROOM-CONTENT-V1.md)
- [Pilot reading-room package](docs/CD1-PACKAGE-8802065.md)
- [Second article and two-article schema check](docs/CD1-SECOND-ARTICLE-8802114.md)
- [Gary Kildall interview and three-article package](docs/CD1-INTERVIEW-8802030.md)
- [Turbo C editor and four-article package](docs/CD1-EDITOR-8802184.md)
- [Turbo Pascal graphics and five-article package](docs/CD1-GRAPHICS-8802180.md)
- [Unindexed KEYBOARD LOCK article and six-article package](docs/CD1-KEYBOARD-8802162.md)
- [February 1988 issue handoff and current coverage](docs/CD1-ISSUE-1988-02.md)
- [CD1 source inventory and backup readiness](docs/CD1-PRESERVATION.md)
- [February 1988 coverage audit](docs/CD1-COVERAGE-1988-02.md)
- [CD1 processing inventory and batch input contract](docs/CD1-PROCESSING-INVENTORY.md)
- [CD1 extraction findings](docs/CD1-EXTRACTION.md)

Run `make import-toc` to build the local TOC catalog and `make check` to validate
the importer. Requires Python 3.11+ and the dependencies in `requirements.txt`.
Generated output is in `build/toc/`; persistent identities are versioned in
`data/identities/toc.json`. Imported metadata is unreviewed and not a public-site
release. Original media, Windows files, and extracted article content stay local.

Run `make import-cd1-index` to structure the three extracted CD1 indexes into
`build/cd1-index/`. This uses the private extraction files and manifest; article
bodies are not read or published.

Run `make reading-room-example` to validate and rebuild the private CD1 pilot
against the v1 content contract, using the existing recovery/block/image maps.
First run `make restore-toc-snapshot` to restore its historical TOC inputs from
Git history; current TOC imports remain separate from prepared-article provenance.
The tracked [synthetic example](examples/reading-room-v1.json) demonstrates the
format without publisher article text.

Run `make reading-room-package` to assemble the private pilot under
`build/reading-room-packages/cd1-8802065/`. Its `content/` directory contains the
complete static handoff; adjacent provenance stays separate. See the package
documentation for standalone verification and configurable base-URL use.

Run `make check-second-article` to reproduce the second article and the combined
two-article package under `build/cd1-second-article/8802114/`. Both validate against
the unchanged v1 contract; the command uses private CD1 sources and ImageMagick.

Run `make inventory-cd1-sources` to check the original CD1 ISO, all extracted disc
files, and preserved probe outputs. Requires `7z`. The local inventory is complete;
independent backup/restore verification remains pending as a separate preservation
task and does not block extraction from the verified sources.

Run `make prepare-cd1-transfer` to stage a private archive of CD1 sources,
prepared artifacts, and committed Git history with per-file checksums. See the
[transfer instructions](docs/CD1-PRESERVATION.md#prepared-local-transfer-set).
Copying it to independent storage and verifying restoration remain separate steps.

Run `make audit-cd1-issue` for the read-only February 1988 TOC/CD coverage audit,
or `PYTHONPATH=src python3 -m tools.audit_cd1_issue --check` to verify its tracked
report without writing. It accounts for metadata and existing prepared packages.

Run `make prepare-cd1-interview` to reproduce `8802030` and the combined
three-article package under `build/cd1-articles/8802030/`. The interview preserves
bold prompts and multi-paragraph answers under the unchanged v1 schema.

Run `make prepare-cd1-editor` to reproduce `8802184` and the combined four-article
package under `build/cd1-articles/8802184/`. Code tabs, blank lines, caption links,
and three diagram bitmaps are preserved; the v1 schema remains unchanged.

Run `make prepare-cd1-graphics` to reproduce `8802180` and the combined five-article
package under `build/cd1-articles/8802180/`. It preserves Korean Pascal strings
and mixed text/image figures, with explicit deferred-media and text-review records.

Run `make prepare-cd1-issue` to reproduce the historical five-article indexed
checkpoint under `build/cd1-issues/1988-02/`.

Run `make prepare-cd1-keyboard` and `make close-cd1-february` for the current
February handoff at `build/cd1-issues/1988-02-native/`. Its 56 runtime files contain
all six articles identified by native February metadata, including the unindexed
“KEYBOARD LOCK.” Coverage accounts for four sections and 29 unmatched article
candidates; physical-magazine completeness remains unverified.
See the [base URL and search handoff](docs/CD1-ISSUE-1988-02.md#static-base-url-and-metadata-search).

Run `make inventory-cd1-processing` to reproduce the CD1 batch input inventory.
It accounts for 1,088 dated article candidates across 72 months: six prepared,
1,074 ready for runner validation, and eight blocked on topic ownership. The
shared extraction runner is the next implementation checkpoint.
