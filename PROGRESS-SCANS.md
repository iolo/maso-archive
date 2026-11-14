# Donated scan cleanup progress

Updated 2026-11-14. Follow the [plan](PLAN-SCANS.md); linked issue reports preserve
the findings and remaining uncertainties. Original donation ZIPs stay unchanged.

## Current status

**24 of 24 donated issues have checked working sets; 0 remain.**
The donation contains 59 ZIPs. Checked issues account for 24,316
source file entries, 6,070 distinct JPEG masters,
6,073 duplicate JPEG copies omitted, and 12,157
confirmed AppleDouble sidecars omitted from the working sets.
Retained masters occupy 49.16 GiB. All sixteen donor-note files are retained.
There are 217 contact sheets, 6,066 proposed reading-order entries and four extras
(two separately retained spines and July 1987's two damaged alternatives).

**The collection-wide completion audit passed.** All 59 original ZIPs are covered
exactly once. Every ZIP and retained master was hashed again, every source member
accounted for, and page-list/review mappings checked. Each issue has its own commit
including a progress update. See the [audit record](metadata/catalog/scans/collection-audit.json)
for totals, issue commit hashes, checks and limitations.

| Issue/report | Status | Distinct scans | Filename gaps |
| --- | --- | ---: | --- |
| [1983-12](docs/SCAN-ISSUE-1983-12.md) | Checked | 236 | None in observed range |
| [1984-02](docs/SCAN-ISSUE-1984-02.md) | Checked | 248 | 13, 14, 15, 16 |
| [1984-03](docs/SCAN-ISSUE-1984-03.md) | Checked | 273 | 11, 12 |
| [1984-04](docs/SCAN-PILOT-1984-04.md) | Checked | 257 | 13, 14 |
| [1984-11](docs/SCAN-ISSUE-1984-11.md) | Checked | 246 | None in observed range |
| [1985-01](docs/SCAN-ISSUE-1985-01.md) | Checked | 246 | None in observed range |
| [1985-04](docs/SCAN-ISSUE-1985-04.md) | Checked | 270 | None in observed range |
| [1985-05](docs/SCAN-ISSUE-1985-05.md) | Checked | 258 | None in observed range |
| [1985-06](docs/SCAN-ISSUE-1985-06.md) | Checked | 266 | None in observed range |
| [1985-07](docs/SCAN-ISSUE-1985-07.md) | Checked | 274 | None in observed range |
| [1985-08](docs/SCAN-ISSUE-1985-08.md) | Checked | 258 | None in observed range |
| [1985-09](docs/SCAN-ISSUE-1985-09.md) | Checked | 262 | None in observed range |
| [1985-12](docs/SCAN-ISSUE-1985-12.md) | Checked | 274 | 18, 20 |
| [1987-01](docs/SCAN-ISSUE-1987-01.md) | Checked | 244 | 65, 66, 67, 68 |
| [1987-02](docs/SCAN-ISSUE-1987-02.md) | Checked | 248 | None in observed range |
| [1987-03](docs/SCAN-ISSUE-1987-03.md) | Checked | 244 | 207, 208 |
| [1987-04](docs/SCAN-ISSUE-1987-04.md) | Checked | 246 | 167, 168 |
| [1987-06](docs/SCAN-ISSUE-1987-06.md) | Checked | 248 | None in observed range |
| [1987-07](docs/SCAN-ISSUE-1987-07.md) | Checked | 246 | 93, 94, 95, 96 |
| [1987-08](docs/SCAN-ISSUE-1987-08.md) | Checked | 246 | 175, 176 |
| [1987-09](docs/SCAN-ISSUE-1987-09.md) | Checked | 248 | None in observed range |
| [1987-10](docs/SCAN-ISSUE-1987-10.md) | Checked | 248 | None in observed range |
| [1987-11](docs/SCAN-ISSUE-1987-11.md) | Checked | 248 | None in observed range |
| [1987-12](docs/SCAN-ISSUE-1987-12.md) | Checked | 236 | 129, 130, 131, 132, 133, 134, 135, 136, 191, 192 |

Filename gaps are distinct from verified missing printed pages. Complete
filename numbering does not establish completeness. The first observed range
for December 1983 begins at 3; no missing 1–2 claim follows from that alone.

## What checked means

Each completed issue has a byte-preserved working collection, original ZIP/member
mappings, SHA-256 duplicate grouping, fully decoded retained JPEGs, contact sheets,
a page list, visual findings, and a fresh source-to-output verification. The four
cover faces, spines, inserts and differing alternatives are retained. Known order
uncertainties and donor-note inconsistencies stay explicit.

April 1984 was the first pilot: 257 scans, nine contact sheets and twelve enlarged
printed-number samples, with a filename gap at 13–14. Later issue overviews include
all retained images in an atlas, with separate cover/boundary views where needed.
These are cleanup reviews, not full proofreading, physical collation, or complete
printed-pagination checks. Unverified printed numbers remain blank.

The [April report](docs/SCAN-PILOT-1984-04.md) and per-issue reports above link the
private working files. Recipes and small result records live in
`metadata/catalog/scans/`; masters and evidence are Git-ignored under
`archive/scans/YYYY-MM/`. Result artifact hashes describe the files captured at
that issue's checkpoint; later shared-tool/document changes do not rewrite those
historical fingerprints. Issue source and master hashes remain pinned separately.

## Next

The donated-scan cleanup campaign is complete. Use each issue's `page-list.csv`
and `review.json` as the restoration handoff; `manifest.json` retains the received
source mappings and initial order. July 1987's reviewed page list corrects the
misordered source block 025–030 without renaming or changing its JPEG masters.
Filename gaps explained by intact foldouts remain distinguished from confirmed
absence and unknown physical pagination.

Recheck any extracted issue from the repository root:

```sh
python3 -m tools.scan_cleanup --verify archive/scans/YYYY-MM
```

To rerun the collection audit, choose a fresh output path (existing audit files
are protected from overwriting):

```sh
python3 -m tools.scan_collection_audit --output archive/scans/shared/collection-audit-recheck.json
```

March 1984's late-page order, June 1987's torn-page note despite present scans,
July 1987's reordered block and damaged alternatives, and December 1987's torn
rear cover require the issue-specific findings; do not
silently infer repair or absence from those names. OCR restoration and reading-room
integration remain separate work.
