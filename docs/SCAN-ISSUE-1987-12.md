# 1987-12 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 2 |
| Source file entries checked | 948 |
| JPEG entries | 472 |
| Duplicate JPEG copies omitted | 236 |
| AppleDouble sidecars omitted | 474 |
| Donor text files retained | 2 |
| Distinct JPEG masters | 236 |
| Images in proposed reading order | 236 |
| Extras outside reading order | 0 |
| Contact sheets | 8 |
| Enlarged printed-number samples checked | 7 |

Working masters occupy 2,045,052,941 bytes (1.90 GiB).
Source filename range: 1–242.
Filename gaps: **129, 130, 131, 132, 133, 134, 135, 136, 191, 192**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 236 retained scans across
8 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- The front cover and sampled footers identify December 1987. Four cover faces were inspected separately. Both sides of the rear cover visibly lack the same large upper outer corner; this is physical loss in the supplied scans, retained without filling or cropping.
- Source filenames span 1-242 with gaps 129-136 and 191-192, matching the donor note. Boundary scans 128,137,190,193 are present and included in the overview and margin samples. No missing image was invented; the contents of the absent spans remain unverified.
- Source 009 is the contents page. Payment/subscription forms at 241-242 remain in source order. Sideways advertisements and code listings retain their original orientation for later restoration.
- All 236 retained images were included in the viewed overview. No additional gross ordering anomaly was apparent at that scale. Seven enlarged printed-number samples match their filenames. No numeral was confirmed in the other sampled lower corners, which remain unset; full pagination and physical collation remain unverified.

Donor note summary: Both original note copies say 129-136 and 191-192 are absent. All ten filename slots are absent from the supplied ZIPs. The note does not specify their content or why they are missing.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 15, 16, 30, 90, 120, 150, 210.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1987-12/README.md)
- [Page list](../archive/scans/1987-12/page-list.csv)
- [Overview](../archive/scans/1987-12/review/overview.jpg)
- [Visual review](../archive/scans/1987-12/review.json)
- [Extraction manifest](../archive/scans/1987-12/manifest.json)
- [Fresh verification](../archive/scans/1987-12/review/verification.json)
- [Recipe](../metadata/catalog/scans/1987-12-recipe.json)
- [Result record](../metadata/catalog/scans/1987-12-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1987-12
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
