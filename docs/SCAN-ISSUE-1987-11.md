# 1987-11 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 2 |
| Source file entries checked | 993 |
| JPEG entries | 497 |
| Duplicate JPEG copies omitted | 249 |
| AppleDouble sidecars omitted | 496 |
| Donor text files retained | 0 |
| Distinct JPEG masters | 248 |
| Images in proposed reading order | 248 |
| Extras outside reading order | 0 |
| Contact sheets | 9 |
| Enlarged printed-number samples checked | 8 |

Working masters occupy 2,111,438,957 bytes (1.97 GiB).
Source filename range: 1–244.
Filename gaps: **none within the observed range**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 248 retained scans across
9 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- The front cover and sampled footers identify November 1987. All four cover faces were checked in the shared cover preview.
- Source filenames run continuously from 1 through 244. No donor note is present. Continuous numbering does not establish physical completeness.
- Source Page054 has three byte-identical copies named Page054.jpg, Page054(1).jpg and Page054(2).jpg. One unchanged working master is retained with all three original members recorded. All other retained images have two exact source copies.
- Source 009 is the contents page. Payment/subscription forms at 241-242 remain in source order. Sideways code listings and existing folds/shadows are preserved for later restoration.
- All 248 retained images were included in the viewed overview. No additional gross ordering anomaly was apparent at that scale. Eight enlarged printed-number samples match their filenames. No numeral was confirmed in the source 015 and 240 crops, so those fields remain unset. Full pagination remains unverified.

Donor note summary: No donor text note was present.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 16, 30, 60, 90, 120, 150, 180, 210.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1987-11/README.md)
- [Page list](../archive/scans/1987-11/page-list.csv)
- [Overview](../archive/scans/1987-11/review/overview.jpg)
- [Visual review](../archive/scans/1987-11/review.json)
- [Extraction manifest](../archive/scans/1987-11/manifest.json)
- [Fresh verification](../archive/scans/1987-11/review/verification.json)
- [Recipe](../metadata/catalog/scans/1987-11-recipe.json)
- [Result record](../metadata/catalog/scans/1987-11-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1987-11
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
