# 1985-08 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 3 |
| Source file entries checked | 1032 |
| JPEG entries | 516 |
| Duplicate JPEG copies omitted | 258 |
| AppleDouble sidecars omitted | 516 |
| Donor text files retained | 0 |
| Distinct JPEG masters | 258 |
| Images in proposed reading order | 258 |
| Extras outside reading order | 0 |
| Contact sheets | 9 |
| Enlarged printed-number samples checked | 9 |

Working masters occupy 2,523,971,550 bytes (2.35 GiB).
Source filename range: 1–254.
Filename gaps: **none within the observed range**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 258 retained scans across
9 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover visibly identifies August 1985. Four cover faces were checked separately in the shared cover preview.
- Ordinary source filenames run continuously from 1 through 254. TOC material occupies source slots 18-19; payment/subscription forms occupy source slots 253-254 and remain in source order.
- All 258 retained images were included in the viewed overview. No additional gross ordering anomaly was apparent across the blue, grey and brown section transitions or the long listing runs.
- Nine enlarged printed numbers match their filenames. Advertisement/front-matter crops and candidate 246 contain no confirmed page numeral and remain unset.

Donor note summary: No donor text note was present.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 30, 60, 90, 120, 150, 180, 210, 240, 245.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1985-08/README.md)
- [Page list](../archive/scans/1985-08/page-list.csv)
- [Overview](../archive/scans/1985-08/review/overview.jpg)
- [Visual review](../archive/scans/1985-08/review.json)
- [Extraction manifest](../archive/scans/1985-08/manifest.json)
- [Fresh verification](../archive/scans/1985-08/review/verification.json)
- [Recipe](../metadata/catalog/scans/1985-08-recipe.json)
- [Result record](../metadata/catalog/scans/1985-08-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1985-08
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
