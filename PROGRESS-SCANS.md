# Donated scan cleanup progress

Updated 2026-11-14. Follow the [plan](PLAN-SCANS.md); linked issue reports preserve
the findings and remaining uncertainties. Original donation ZIPs stay unchanged.

## Current status

**9 of 24 donated issues have checked working sets; 15 remain.**
The donation contains 59 ZIPs. Checked issues account for 9,204
source file entries, 2,300 distinct JPEG masters,
2,300 duplicate JPEG copies omitted, and 4,602
confirmed AppleDouble sidecars omitted from the working sets.
Retained masters occupy 17.77 GiB.

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
| 1985-07 | Awaiting cleanup | — | — |
| 1985-08 | Awaiting cleanup | — | — |
| 1985-09 | Awaiting cleanup | — | — |
| 1985-12 | Awaiting cleanup | — | — |
| 1987-01 | Awaiting cleanup | — | — |
| 1987-02 | Awaiting cleanup | — | — |
| 1987-03 | Awaiting cleanup | — | — |
| 1987-04 | Awaiting cleanup | — | — |
| 1987-06 | Awaiting cleanup | — | — |
| 1987-07 | Awaiting cleanup | — | — |
| 1987-08 | Awaiting cleanup | — | — |
| 1987-09 | Awaiting cleanup | — | — |
| 1987-10 | Awaiting cleanup | — | — |
| 1987-11 | Awaiting cleanup | — | — |
| 1987-12 | Awaiting cleanup | — | — |

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

Next: **1985-07**. Continue one issue at a time, record the visual findings,
update this index, and commit that issue before closing out the next.

Recheck any extracted issue from the repository root:

```sh
python3 -m tools.scan_cleanup --verify archive/scans/YYYY-MM
```

March 1984's late-page order, June 1987's torn-page note despite present scans,
and July 1987's damaged alternatives require the issue-specific findings; do not
silently infer repair or absence from those names. OCR restoration and reading-room
integration remain separate work.
