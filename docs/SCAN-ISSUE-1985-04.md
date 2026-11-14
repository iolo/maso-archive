# 1985-04 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 3 |
| Source file entries checked | 1080 |
| JPEG entries | 540 |
| Duplicate JPEG copies omitted | 270 |
| AppleDouble sidecars omitted | 540 |
| Donor text files retained | 0 |
| Distinct JPEG masters | 270 |
| Images in proposed reading order | 270 |
| Extras outside reading order | 0 |
| Contact sheets | 9 |
| Enlarged printed-number samples checked | 9 |

Working masters occupy 2,468,743,060 bytes (2.30 GiB).
Source filename range: 1–266.
Filename gaps: **none within the observed range**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 270 retained scans across
9 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover visibly identifies April 1985. All four cover faces were checked separately in the shared cover preview; existing edge wear was retained unchanged.
- Ordinary source filenames run continuously from 1 through 266. Source slots 265-266 contain payment/subscription forms and remain in source order.
- All 270 retained images were included in the viewed overview, including long machine-code and program-table runs. Similar appearance alone was not used to remove any scan.
- No additional gross ordering anomaly was apparent. Nine enlarged printed numbers match their filenames; unnumbered sample crops remain unset.

Donor note summary: No donor text note was present.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 30, 60, 90, 120, 150, 180, 210, 245, 246.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1985-04/README.md)
- [Page list](../archive/scans/1985-04/page-list.csv)
- [Overview](../archive/scans/1985-04/review/overview.jpg)
- [Visual review](../archive/scans/1985-04/review.json)
- [Extraction manifest](../archive/scans/1985-04/manifest.json)
- [Fresh verification](../archive/scans/1985-04/review/verification.json)
- [Recipe](../metadata/catalog/scans/1985-04-recipe.json)
- [Result record](../metadata/catalog/scans/1985-04-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1985-04
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
