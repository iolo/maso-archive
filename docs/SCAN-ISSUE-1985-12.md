# 1985-12 donated scan cleanup

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
| Enlarged printed-number samples checked | 10 |

Working masters occupy 3,172,366,726 bytes (2.95 GiB).
Source filename range: 1–272.
Filename gaps: **18, 20**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 274 retained scans across
10 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover visibly identifies December 1985. Four cover faces were checked separately in the shared cover preview.
- Source filenames 18 and 20 are absent. The immediately preceding source slots 17 and 19 are intact two-page spreads, each 9828 by 6907 pixels: a TOC spread and an advertisement spread. Both were inspected separately at larger scale. These paired scans likely explain the skipped even filename slots; their exact printed-page spans remain unverified and the gaps are not called proven missing physical pages.
- Source slots 269-270 show Christmas greeting-card front/reverse material; 271-272 contain payment/subscription forms. All sides are retained in source order without invented printed numbers.
- All 274 retained images were included in the viewed overview. No additional gross ordering anomaly was apparent; ten enlarged printed-number samples match their filenames.

Donor note summary: No donor text note was present.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 30, 60, 90, 120, 150, 180, 210, 240, 245, 246.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1985-12/README.md)
- [Page list](../archive/scans/1985-12/page-list.csv)
- [Overview](../archive/scans/1985-12/review/overview.jpg)
- [Visual review](../archive/scans/1985-12/review.json)
- [Extraction manifest](../archive/scans/1985-12/manifest.json)
- [Fresh verification](../archive/scans/1985-12/review/verification.json)
- [Recipe](../metadata/catalog/scans/1985-12-recipe.json)
- [Result record](../metadata/catalog/scans/1985-12-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1985-12
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
