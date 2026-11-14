# 1985-07 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 3 |
| Source file entries checked | 1096 |
| JPEG entries | 548 |
| Duplicate JPEG copies omitted | 274 |
| AppleDouble sidecars omitted | 548 |
| Donor text files retained | 0 |
| Distinct JPEG masters | 274 |
| Images in proposed reading order | 274 |
| Extras outside reading order | 0 |
| Contact sheets | 10 |
| Enlarged printed-number samples checked | 7 |

Working masters occupy 2,402,855,260 bytes (2.24 GiB).
Source filename range: 1–270.
Filename gaps: **none within the observed range**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 274 retained scans across
10 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover visibly identifies July 1985. Four cover faces were checked separately in the shared cover preview.
- Ordinary source filenames run continuously from 1 through 270. TOC scans occupy source slots 18-19; payment/subscription forms occupy 269-270 and remain in source order.
- All 274 retained images were included in the viewed overview. No additional gross ordering anomaly was apparent, including across extended code and keyboard/table sequences.
- Seven enlarged printed numbers match their filenames. Other sample crops have no readable printed numeral and remain unset; article references and advertising text are not used as pagination.

Donor note summary: No donor text note was present.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 30, 90, 120, 150, 180, 210, 246.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1985-07/README.md)
- [Page list](../archive/scans/1985-07/page-list.csv)
- [Overview](../archive/scans/1985-07/review/overview.jpg)
- [Visual review](../archive/scans/1985-07/review.json)
- [Extraction manifest](../archive/scans/1985-07/manifest.json)
- [Fresh verification](../archive/scans/1985-07/review/verification.json)
- [Recipe](../metadata/catalog/scans/1985-07-recipe.json)
- [Result record](../metadata/catalog/scans/1985-07-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1985-07
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
