# 1987-02 donated scan cleanup

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
| Enlarged printed-number samples checked | 7 |

Working masters occupy 2,043,922,461 bytes (1.90 GiB).
Source filename range: 1–244.
Filename gaps: **none within the observed range**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 248 retained scans across
9 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover and sampled page footers identify February 1987. Four cover faces were checked separately in the shared cover preview.
- Ordinary source filenames run continuously from 1 through 244. Source slot 170 is a reader-survey form; 241-242 contain payment/subscription forms. All remain in source order, with form numbers separate from printed pagination.
- All 248 retained images were included in the viewed overview. Long graph/listing sequences remain intact. No additional gross ordering anomaly was apparent.
- Seven enlarged printed numbers match their filenames. Unnumbered advertisement/front-matter crops and the final imprint crop remain unset.

Donor note summary: No donor text note was present.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 30, 60, 90, 120, 150, 180, 210.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1987-02/README.md)
- [Page list](../archive/scans/1987-02/page-list.csv)
- [Overview](../archive/scans/1987-02/review/overview.jpg)
- [Visual review](../archive/scans/1987-02/review.json)
- [Extraction manifest](../archive/scans/1987-02/manifest.json)
- [Fresh verification](../archive/scans/1987-02/review/verification.json)
- [Recipe](../metadata/catalog/scans/1987-02-recipe.json)
- [Result record](../metadata/catalog/scans/1987-02-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1987-02
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
