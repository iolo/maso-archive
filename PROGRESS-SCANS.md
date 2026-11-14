# Donated scan cleanup progress

Updated 2026-11-14. The [cleanup plan](PLAN-SCANS.md) describes the workflow;
issue reports record what was checked and what still looks odd.

## Current status

The initial inspection covers **24 issues in 59 ZIPs** under `maso-img/`.
The **April 1984 pilot is complete**, with an open filename gap at 13–14.
The other 23 issues have not been extracted by this workflow.

| Issue | Status | Working set | Notes |
| --- | --- | --- | --- |
| 1984-04 | Pilot checked | `archive/scans/1984-04/` | 257 unchanged scans; filename gap 13–14 |
| 1984-03 | Next pilot, not started | — | Donor note flags a missing advertising sheet and uncertain late-page order |
| Other 22 donated issues | Initial ZIP-listing inspection only | — | Duplicate candidates and filename gaps await extraction and visual review |

## April 1984 — first pilot

The two original ZIPs contain 514 JPEG entries and 514 AppleDouble sidecars.
Full SHA-256 comparison found **257 byte-identical image pairs**. The separate
working collection keeps one image from each pair, about **1.76 GiB**, with
252 source-numbered scans, four cover faces, and one spine. The ZIPs remain
unchanged; working masters were not cropped, rotated, or recompressed.

All nine contact sheets were viewed. Cover roles were assigned visually, with
the spine outside reading order. Source slots 247–248 are subscription postcards
and 249–250 are payment slips; the page list flags these as inserts. Twelve
printed page numbers were checked in enlarged crops and match their filenames.
Other printed numbers remain unset.

Neither ZIP contains source filenames for **13–14**. The preceding scan is an
advertisement; the next is the editor note with printed page 15. The absent
span's contents and reason remain unknown. No additional gross ordering anomaly
was apparent in the contact sheets. Full pagination and physical collation
remain unchecked.

Validation passed: all **1,028 source entries** were re-read and accounted for,
all 257 extracted image hashes and nine contact-sheet hashes matched, and both
original ZIP hashes stayed unchanged. Extraction also refused an existing issue
directory before writing. The page list and review mappings agree with the
extraction manifest.

- [Pilot report](docs/SCAN-PILOT-1984-04.md)
- [Working-set README](archive/scans/1984-04/README.md)
- [Page list](archive/scans/1984-04/page-list.csv)
- [Recipe](metadata/catalog/scans/1984-04-recipe.json) and
  [result record](metadata/catalog/scans/1984-04-result.json)
- [Cleanup and verification tool](tools/scan_cleanup.py)

Repeat the read-only verification from the repository root:

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1984-04
```

## Next

Try **March 1984** with its donor note, spine, postcards, and uncertain order
from page 261 onward. Preserve differing scans as alternatives and keep filename
numbers separate from verified printed numbers. Review that pilot before
batching the remaining issues.

Scans and private evidence stay under Git-ignored `archive/scans/`; the original
ZIPs stay under `maso-img/`. Git keeps the plan, progress, reports, recipes,
small result records, and tool. OCR restoration and reading-room integration
remain separate work.
