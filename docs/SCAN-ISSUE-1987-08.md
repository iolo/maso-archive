# 1987-08 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 3 |
| Source file entries checked | 988 |
| JPEG entries | 492 |
| Duplicate JPEG copies omitted | 246 |
| AppleDouble sidecars omitted | 494 |
| Donor text files retained | 2 |
| Distinct JPEG masters | 246 |
| Images in proposed reading order | 246 |
| Extras outside reading order | 0 |
| Contact sheets | 9 |
| Enlarged printed-number samples checked | 10 |

Working masters occupy 2,345,001,156 bytes (2.18 GiB).
Source filename range: 1–244.
Filename gaps: **175, 176**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 246 retained scans across
9 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- The front cover and sampled footers identify August 1987. All four cover faces were checked in the shared cover preview.
- Source filenames run from 1 through 244, with 175-176 absent. This agrees with the donor note about a torn-out postcard. The available boundary scans are 174 and 177; no replacement or blank image has been manufactured.
- Payment/subscription forms at source slots 241-242 are retained in source order. The contents page is source 009. Source 016 and 177 are advertisements without a confirmed printed numeral in the sampled lower corners.
- All 246 retained images were included in the viewed overview. No additional gross ordering anomaly was apparent at that scale. Ten enlarged printed-number samples match their source filenames; full pagination and physical collation remain unverified.

Donor note summary: Both original note copies say the postcard at 175-176 was torn out. These two filename slots are absent from the supplied scans.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 15, 30, 60, 90, 120, 150, 174, 180, 210, 240.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1987-08/README.md)
- [Page list](../archive/scans/1987-08/page-list.csv)
- [Overview](../archive/scans/1987-08/review/overview.jpg)
- [Visual review](../archive/scans/1987-08/review.json)
- [Extraction manifest](../archive/scans/1987-08/manifest.json)
- [Fresh verification](../archive/scans/1987-08/review/verification.json)
- [Recipe](../metadata/catalog/scans/1987-08-recipe.json)
- [Result record](../metadata/catalog/scans/1987-08-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1987-08
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
