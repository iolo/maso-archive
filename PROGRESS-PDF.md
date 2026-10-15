# PDF restoration progress

Updated 2026-10-16. This file is the status index; detailed records live under
[`docs/progress/`](docs/progress/README.md), grouped by **magazine issue**, not
by the calendar month in which restoration work happened.

## Current status

August 1984 JSON/assets restoration is complete. September 1984 is in progress:
the printed-page-17 editorial, printed-pages-18–19 feature introduction, and
the first three child articles on printed pages 20–37, the first six
hobby games on printed pages 40–59, the first educational article on
printed pages 64–65, the complete typing article on printed pages 66–77,
the math article on printed pages 78–84, the Logo lesson on printed pages
85–92, the menu-selection technique article on printed pages 93–96, the
Z80 machine-language lesson on printed pages 97–109, **애플 포트란** on
printed pages 110–114, and **CP/M 입문** on printed pages 115–121 are readable
and assistant sample-reviewed. The **비지니스** divider is non-owning; next
restore **자료 구조** from printed page 124;
issue accounting remains open.
Twelve eligible issues remain,
including September.
Human acceptance/full proofreading remain pending; no reading-room rebuild is
queued. Follow the [OCR handoff](PLAN-OCR.md), [PDF plan](PLAN-PDF.md) and
[successor notes](docs/SUCCESSOR-NOTES.md).

| Issue | Body articles | Availability | Detailed progress |
| --- | ---: | --- | --- |
| 1983-11 | 35 | 35 readable | [8311](docs/progress/8311.md) |
| 1984-02 | 37 | 37 readable | [8402](docs/progress/8402.md) |
| 1984-03 | 38 | 37 readable, one terminal missing-source partial | [8403](docs/progress/8403.md) |
| 1984-05 | 36 | 36 readable | [8405](docs/progress/8405.md) |
| 1984-06 | 38 | 38 readable | [8406](docs/progress/8406.md) |
| 1984-07 | 36 | 36 readable | [8407](docs/progress/8407.md) |
| 1984-08 | 37 | 37 readable | [8408](docs/progress/8408.md) |
| 1984-09 | classification pending | nineteen readable; issue in progress | [8409](docs/progress/8409.md) |

No April 1984 PDF was supplied. Completed accounting and usable coverage are
separate: March's absent printed pages 250–251 remain explicit.

## Cross-issue records

- [Foundations and contrasting pilots](docs/progress/foundation.md)
- [Catalog, scope, tooling and cost decisions](docs/progress/campaign.md)
- [OCR experiment progress](docs/progress/ocr-experiments.md)
- [Full experiment-history index](docs/history/README.md)

The reorganization preserves all **489 original sections**, their order within
each destination, evidence paths and measurements. Heading levels and relative
Markdown links were adjusted for the hierarchy. [Migration provenance and
section lookup](docs/progress/migration.json) map every old section to its new
location and record original/content hashes. No restoration output was changed.

## Updating progress

Append bounded checkpoint notes to `docs/progress/YYMM.md` for the issue being
restored. For a new issue, add a current-outcome summary and a checkpoint-records
section, then add it to the [directory index](docs/progress/README.md). Update
this status table and next step at issue milestones; do not append detailed
batch histories here. Keep measurements and package pins in their existing
machine-readable ledgers, and link them from the issue page.

Record cross-issue decisions in the appropriate shared file. Preserve historical
claims as dated observations; earlier “next” instructions are not a current queue.
A future cleanup must preserve the source records and update affected links.
