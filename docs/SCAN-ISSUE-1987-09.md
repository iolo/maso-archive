# 1987-09 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 3 |
| Source file entries checked | 992 |
| JPEG entries | 496 |
| Duplicate JPEG copies omitted | 248 |
| AppleDouble sidecars omitted | 496 |
| Donor text files retained | 0 |
| Distinct JPEG masters | 248 |
| Images in proposed reading order | 248 |
| Extras outside reading order | 0 |
| Contact sheets | 9 |
| Enlarged printed-number samples checked | 9 |

Working masters occupy 2,171,236,182 bytes (2.02 GiB).
Source filename range: 1–244.
Filename gaps: **none within the observed range**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 248 retained scans across
9 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- The front cover and sampled footers identify September 1987. All four cover faces were checked in the shared cover preview.
- Source filenames run continuously from 1 through 244. No donor note is present; a continuous filename range is not proof of physical completeness.
- Source 009 is the contents page. Payment/subscription forms at source slots 241-242 remain in source order. The first numbered scan is a sideways advertisement preserved in its original orientation.
- All 248 retained images were included in the viewed overview, with no additional gross ordering anomaly apparent at that scale. Nine enlarged printed-number samples match their filenames. Source 090 is an advertisement without a verified numeral in the sampled lower corners. Full pagination remains unverified.

Donor note summary: No donor text note was present.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 15, 16, 30, 60, 120, 150, 180, 210, 240.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1987-09/README.md)
- [Page list](../archive/scans/1987-09/page-list.csv)
- [Overview](../archive/scans/1987-09/review/overview.jpg)
- [Visual review](../archive/scans/1987-09/review.json)
- [Extraction manifest](../archive/scans/1987-09/manifest.json)
- [Fresh verification](../archive/scans/1987-09/review/verification.json)
- [Recipe](../metadata/catalog/scans/1987-09-recipe.json)
- [Result record](../metadata/catalog/scans/1987-09-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1987-09
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
