# 1987-07 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 2 |
| Source file entries checked | 988 |
| JPEG entries | 492 |
| Duplicate JPEG copies omitted | 246 |
| AppleDouble sidecars omitted | 494 |
| Donor text files retained | 2 |
| Distinct JPEG masters | 246 |
| Images in proposed reading order | 244 |
| Extras outside reading order | 2 |
| Contact sheets | 9 |
| Enlarged printed-number samples checked | 30 |

Working masters occupy 1,902,730,057 bytes (1.77 GiB).
Source filename range: 1–244.
Filename gaps: **93, 94, 95, 96**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 246 retained scans across
9 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover and sampled footers identify July 1987. Four cover faces were inspected in the shared cover preview.
- The early filename block is misordered: source 025,026,027,028,030 visibly carry printed numbers 27,28,29,30,26. The reviewed reading list places source files 029,030,025,026,027,028 between source 024 and 031. Source 029 is an advertisement assigned the intervening slot provisionally; no printed page 25 is asserted for it. See review/reordered-025-030.jpg and the supplementary margin crops. The immutable extraction manifest and JPEG filenames retain the received order.
- Source filenames 093-096 are absent. Each of 089-092 is a separate 10200 by 6907 two-page foldout scan, inspected enlarged: a character/code chart and retail maps/directories/advertisements. Their extra panels likely account for the filename jump; four missing physical pages are not established. Foldouts remain intact.
- The complete-looking advertisements 019-020 remain in the primary sequence. Differing cut-out scans are retained as extras outside it; review/advertisement-alternatives.jpg shows the corresponding missing lower corner on both sides. These are distinct scans, not exact duplicates.
- Payment forms occupy source slots 241-242. All 246 retained images were included in the viewed overview. Beyond the corrected early block and documented foldout span, no additional gross ordering anomaly was apparent at overview scale. Full pagination remains unverified.

Donor note summary: The note says advertisement page 19 was cut out and filled in on 2015-08-05. Its issue-number prefix is 043, while the supplied July 1987 folder is 045. Both original note copies are retained. Complete-looking scans 019-020 and visibly cut alternatives are all retained; the note does not establish how the replacement scans were made.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 23, 27, 28, 29, 30, 26, 31, 32, 33, 34, 35, 40, 50, 80, 81, 82, 83, 84, 85, 86, 87, 88, 98, 99, 100, 121, 150, 180, 210, 240.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1987-07/README.md)
- [Page list](../archive/scans/1987-07/page-list.csv)
- [Overview](../archive/scans/1987-07/review/overview.jpg)
- [Visual review](../archive/scans/1987-07/review.json)
- [Extraction manifest](../archive/scans/1987-07/manifest.json)
- [Fresh verification](../archive/scans/1987-07/review/verification.json)
- [Recipe](../metadata/catalog/scans/1987-07-recipe.json)
- [Result record](../metadata/catalog/scans/1987-07-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1987-07
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
