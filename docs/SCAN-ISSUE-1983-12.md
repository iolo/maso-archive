# 1983-12 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 2 |
| Source file entries checked | 944 |
| JPEG entries | 472 |
| Duplicate JPEG copies omitted | 236 |
| AppleDouble sidecars omitted | 472 |
| Donor text files retained | 0 |
| Distinct JPEG masters | 236 |
| Images in proposed reading order | 236 |
| Extras outside reading order | 0 |
| Contact sheets | 8 |
| Enlarged printed-number samples checked | 7 |

Working masters occupy 1,854,608,351 bytes (1.73 GiB).
Source filename range: 3–232.
Filename gaps: **none within the observed range**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 236 retained scans across
8 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover visibly identifies December 1983. Four cover faces were checked in the shared cover preview; no separate spine scan is present.
- Ordinary source filenames run continuously from 3 through 232. No absent 1-2 claim is made because those filenames may reflect the scanner's treatment of covers and unnumbered matter.
- Source slots 113-114 are sideways subscription-card scans; two separately named payment-slip scans are anchored after source slot 114. All four are retained, with card/slip roles separated from verified printed pagination. Rotation remains deferred to restoration derivatives.
- All 236 retained images were included in the viewed overview. No additional gross order anomaly was apparent. Some source scans have fading or tape marks; the original JPEG bytes were preserved.
- Seven enlarged printed numbers match their source filenames. Candidate crops 90 and 210 have no readable printed numeral and remain unset.

Donor note summary: No donor text note was present.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 15, 16, 30, 60, 120, 150, 180.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1983-12/README.md)
- [Page list](../archive/scans/1983-12/page-list.csv)
- [Overview](../archive/scans/1983-12/review/overview.jpg)
- [Visual review](../archive/scans/1983-12/review.json)
- [Extraction manifest](../archive/scans/1983-12/manifest.json)
- [Fresh verification](../archive/scans/1983-12/review/verification.json)
- [Recipe](../metadata/catalog/scans/1983-12-recipe.json)
- [Result record](../metadata/catalog/scans/1983-12-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1983-12
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
