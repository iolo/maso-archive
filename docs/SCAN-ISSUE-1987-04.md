# 1987-04 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 2 |
| Source file entries checked | 989 |
| JPEG entries | 493 |
| Duplicate JPEG copies omitted | 247 |
| AppleDouble sidecars omitted | 494 |
| Donor text files retained | 2 |
| Distinct JPEG masters | 246 |
| Images in proposed reading order | 246 |
| Extras outside reading order | 0 |
| Contact sheets | 9 |
| Enlarged printed-number samples checked | 9 |

Working masters occupy 1,950,308,825 bytes (1.82 GiB).
Source filename range: 1–244.
Filename gaps: **167, 168**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 246 retained scans across
9 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover and sampled page footers identify April 1987. Four cover faces were checked separately in the shared cover preview.
- Source filenames 167-168 are absent and the donor reports a torn-out postcard at that location. The boundary scans 166 and 169 are advertisements; no additional printed-number inference is made from their text.
- Page027 has three identical source copies, including a nested copy suffix. Full hashes retain one working image with all three original locations in the manifest.
- Payment/subscription forms occupy source slots 241-242. All 246 retained images were included in the viewed overview; no additional gross ordering anomaly was apparent. Nine enlarged printed-number samples match their filenames.

Donor note summary: The donor reports the postcard at 167-168 torn out, matching the absent source filenames. The note filename uses issue 040 while the folder uses 042; cover and page footers identify April 1987. Both original text copies are retained unchanged.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 15, 16, 30, 60, 90, 120, 180, 210, 240.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1987-04/README.md)
- [Page list](../archive/scans/1987-04/page-list.csv)
- [Overview](../archive/scans/1987-04/review/overview.jpg)
- [Visual review](../archive/scans/1987-04/review.json)
- [Extraction manifest](../archive/scans/1987-04/manifest.json)
- [Fresh verification](../archive/scans/1987-04/review/verification.json)
- [Recipe](../metadata/catalog/scans/1987-04-recipe.json)
- [Result record](../metadata/catalog/scans/1987-04-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1987-04
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
