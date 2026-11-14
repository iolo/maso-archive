# 1984-11 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 3 |
| Source file entries checked | 984 |
| JPEG entries | 492 |
| Duplicate JPEG copies omitted | 246 |
| AppleDouble sidecars omitted | 492 |
| Donor text files retained | 0 |
| Distinct JPEG masters | 246 |
| Images in proposed reading order | 246 |
| Extras outside reading order | 0 |
| Contact sheets | 9 |
| Enlarged printed-number samples checked | 7 |

Working masters occupy 2,137,622,259 bytes (1.99 GiB).
Source filename range: 1–242.
Filename gaps: **none within the observed range**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 246 retained scans across
9 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover and sampled page footers visibly identify November 1984. Four cover faces were checked separately in the shared cover preview.
- Ordinary source filenames run continuously from 1 through 242. No internal filename gap was found; full printed pagination and collation remain unverified.
- Source slots 241-242 contain payment/subscription form material. Both sides are retained in source order and classified separately from ordinary article pages.
- All 246 retained images were included in the viewed overview. No additional gross ordering anomaly was apparent; seven enlarged printed-number samples match their filenames. Unnumbered TOC, advertisement and contest-page sample crops remain unset.

Donor note summary: No donor text note was present.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 30, 90, 120, 150, 180, 210, 240.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1984-11/README.md)
- [Page list](../archive/scans/1984-11/page-list.csv)
- [Overview](../archive/scans/1984-11/review/overview.jpg)
- [Visual review](../archive/scans/1984-11/review.json)
- [Extraction manifest](../archive/scans/1984-11/manifest.json)
- [Fresh verification](../archive/scans/1984-11/review/verification.json)
- [Recipe](../metadata/catalog/scans/1984-11-recipe.json)
- [Result record](../metadata/catalog/scans/1984-11-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1984-11
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
