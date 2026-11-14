# 1984-02 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 2 |
| Source file entries checked | 992 |
| JPEG entries | 496 |
| Duplicate JPEG copies omitted | 248 |
| AppleDouble sidecars omitted | 496 |
| Donor text files retained | 0 |
| Distinct JPEG masters | 248 |
| Images in proposed reading order | 248 |
| Extras outside reading order | 0 |
| Contact sheets | 9 |
| Enlarged printed-number samples checked | 8 |

Working masters occupy 1,756,108,252 bytes (1.64 GiB).
Source filename range: 1–246.
Filename gaps: **13, 14, 15, 16**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 248 retained scans across
9 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover visibly identifies February 1984. All four cover faces were checked in the shared cover preview; no separate spine scan is present.
- Source filenames 13-16 are absent. Source slots 11 and 12 are unusually wide 8541 by 7006 pixel scans, showing a multi-panel TOC and an AMD seminar advertisement. Both were inspected separately at larger scale and preserved intact; the filename gap is not treated as four proven missing physical pages.
- Source slot 242 is a sideways subscription card; two separately named payment-slip scans follow its source anchor. Their printed page numbers remain unset and rotation is deferred to derivatives.
- All 248 retained images were included in the viewed overview. Several scans show folds or fading. No additional gross ordering anomaly was apparent; eight enlarged printed-number samples match their filenames.

Donor note summary: No donor text note was present.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 17, 30, 60, 90, 150, 180, 210, 240.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1984-02/README.md)
- [Page list](../archive/scans/1984-02/page-list.csv)
- [Overview](../archive/scans/1984-02/review/overview.jpg)
- [Visual review](../archive/scans/1984-02/review.json)
- [Extraction manifest](../archive/scans/1984-02/manifest.json)
- [Fresh verification](../archive/scans/1984-02/review/verification.json)
- [Recipe](../metadata/catalog/scans/1984-02-recipe.json)
- [Result record](../metadata/catalog/scans/1984-02-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1984-02
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
