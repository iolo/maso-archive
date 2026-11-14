# 1987-03 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 2 |
| Source file entries checked | 980 |
| JPEG entries | 488 |
| Duplicate JPEG copies omitted | 244 |
| AppleDouble sidecars omitted | 490 |
| Donor text files retained | 2 |
| Distinct JPEG masters | 244 |
| Images in proposed reading order | 244 |
| Extras outside reading order | 0 |
| Contact sheets | 9 |
| Enlarged printed-number samples checked | 6 |

Working masters occupy 2,085,574,307 bytes (1.94 GiB).
Source filename range: 1–242.
Filename gaps: **207, 208**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 244 retained scans across
9 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover and sampled page footers identify March 1987. Four cover faces were checked separately in the shared cover preview.
- Source filenames 207-208 are absent, consistent with the donor note about a damaged postcard at that location. The next available boundary scan has printed number 209. No missing postcard sides were fabricated.
- All 244 retained images were included in the viewed overview. The contest illustration in the body resembles the cover design but remains a separate image; all nonidentical scans were retained.
- No additional gross ordering anomaly was apparent. Six enlarged printed numbers match their filenames; advertising and title-page crops without confirmed numerals remain unset.

Donor note summary: The donor reports damage to the postcard at 207-208. Neither numbered source file is present. Both copies of the original note are retained unchanged.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 30, 60, 90, 180, 209, 210.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1987-03/README.md)
- [Page list](../archive/scans/1987-03/page-list.csv)
- [Overview](../archive/scans/1987-03/review/overview.jpg)
- [Visual review](../archive/scans/1987-03/review.json)
- [Extraction manifest](../archive/scans/1987-03/manifest.json)
- [Fresh verification](../archive/scans/1987-03/review/verification.json)
- [Recipe](../metadata/catalog/scans/1987-03-recipe.json)
- [Result record](../metadata/catalog/scans/1987-03-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1987-03
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
