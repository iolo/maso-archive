# 1987-01 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 2 |
| Source file entries checked | 981 |
| JPEG entries | 488 |
| Duplicate JPEG copies omitted | 244 |
| AppleDouble sidecars omitted | 491 |
| Donor text files retained | 2 |
| Distinct JPEG masters | 244 |
| Images in proposed reading order | 244 |
| Extras outside reading order | 0 |
| Contact sheets | 9 |
| Enlarged printed-number samples checked | 10 |

Working masters occupy 2,066,614,813 bytes (1.92 GiB).
Source filename range: 1–244.
Filename gaps: **65, 66, 67, 68**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 244 retained scans across
9 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover and sampled page footers identify January 1987. Four cover faces were checked separately in the shared cover preview.
- Source filenames 65-68 are absent. The donor explicitly reports those pages torn out; the next available boundary sample has printed number 69. The gap remains open with no replacement pages created.
- Payment/subscription forms occupy source slots 241-242 and remain in source order. Other differently shaped advertising scans were preserved intact.
- All 244 retained images were included in the viewed overview. No additional gross ordering anomaly was apparent, including across the long similar-looking character/table pages. Ten enlarged printed numbers match their filenames.

Donor note summary: The donor reports pages 65-68 torn out. This agrees with the absent source filenames. The original text-note filename uses issue 037 while the issue folder uses 039; both copies are retained unchanged and issue identity follows the January 1987 cover and page footers.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 15, 16, 30, 60, 69, 90, 150, 180, 210, 240.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1987-01/README.md)
- [Page list](../archive/scans/1987-01/page-list.csv)
- [Overview](../archive/scans/1987-01/review/overview.jpg)
- [Visual review](../archive/scans/1987-01/review.json)
- [Extraction manifest](../archive/scans/1987-01/manifest.json)
- [Fresh verification](../archive/scans/1987-01/review/verification.json)
- [Recipe](../metadata/catalog/scans/1987-01-recipe.json)
- [Result record](../metadata/catalog/scans/1987-01-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1987-01
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
