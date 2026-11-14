# 1987-06 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 2 |
| Source file entries checked | 996 |
| JPEG entries | 496 |
| Duplicate JPEG copies omitted | 248 |
| AppleDouble sidecars omitted | 498 |
| Donor text files retained | 2 |
| Distinct JPEG masters | 248 |
| Images in proposed reading order | 248 |
| Extras outside reading order | 0 |
| Contact sheets | 9 |
| Enlarged printed-number samples checked | 10 |

Working masters occupy 2,032,712,311 bytes (1.89 GiB).
Source filename range: 1–244.
Filename gaps: **none within the observed range**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 248 retained scans across
9 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover and sampled page footers identify June 1987. Four cover faces were checked separately in the shared cover preview.
- Ordinary source filenames run continuously from 1 through 244. Source slots 191-192 are present and were inspected separately in review/survey-191-192.jpg: a filled-in June reader questionnaire and its printed reverse. The donor note conflicts with current scan availability, so no missing-page placeholder is inserted there.
- Payment/subscription forms occupy source slots 241-242 and remain in source order. Survey and payment-form roles are separate from verified printed pagination.
- All 248 retained images were included in the viewed overview. No additional gross ordering anomaly was apparent; all ten enlarged printed-number samples match their filenames.

Donor note summary: The donor note says 191-192 were torn out, but the supplied set includes both scans. Both note copies are preserved. Whether these were later replacement scans is unknown; the note is retained as historical context rather than treated as a current absence.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 15, 16, 30, 60, 90, 120, 150, 180, 210, 240.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1987-06/README.md)
- [Page list](../archive/scans/1987-06/page-list.csv)
- [Overview](../archive/scans/1987-06/review/overview.jpg)
- [Visual review](../archive/scans/1987-06/review.json)
- [Extraction manifest](../archive/scans/1987-06/manifest.json)
- [Fresh verification](../archive/scans/1987-06/review/verification.json)
- [Recipe](../metadata/catalog/scans/1987-06-recipe.json)
- [Result record](../metadata/catalog/scans/1987-06-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1987-06
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
