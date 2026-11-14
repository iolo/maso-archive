# 1984-03 donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | 2 |
| Source file entries checked | 1096 |
| JPEG entries | 546 |
| Duplicate JPEG copies omitted | 273 |
| AppleDouble sidecars omitted | 548 |
| Donor text files retained | 2 |
| Distinct JPEG masters | 273 |
| Images in proposed reading order | 272 |
| Extras outside reading order | 1 |
| Contact sheets | 10 |
| Enlarged printed-number samples checked | 13 |

Working masters occupy 1,821,959,343 bytes (1.70 GiB).
Source filename range: 1–266.
Filename gaps: **11, 12**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all 273 retained scans across
10 contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

- Front cover visibly identifies March 1984. AFront000 is a spine; AFront001/AFront002 and Rear001/Rear002 are the four cover faces. Cover and insert previews were viewed separately.
- Source filenames 11-12 are absent between an advertisement and the editor note with printed page 13. The donor mentions a missing advertising sheet; its exact contents remain unidentified.
- Four extra scans anchored at 260 contain subscription-postcard address/application sides and payment-slip front/reverse sides. They are placed after source slot 260, with sourceFilenameAnchor=260 and no invented printed numbers.
- The final available numbered content reaches source slot 260, followed by advertisements in source slots 261-266. The donor explicitly doubts their order. Source filename order is retained provisionally; the inspection supplies no reliable basis to claim their physical order is repaired.
- All 273 retained images were included in the viewed overview. No further gross ordering anomaly was apparent at thumbnail scale; thirteen enlarged printed-number samples match their source filenames.

Donor note summary: The donor reports a missing advertising sheet near the front and does not guarantee order from page 261 onward. The note filename says 1984_04 although the folder, cover and scans identify March 1984; both original text-file copies are retained unchanged.
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: 13, 15, 16, 30, 60, 90, 120, 150, 180, 210, 240, 245, 246.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/1984-03/README.md)
- [Page list](../archive/scans/1984-03/page-list.csv)
- [Overview](../archive/scans/1984-03/review/overview.jpg)
- [Visual review](../archive/scans/1984-03/review.json)
- [Extraction manifest](../archive/scans/1984-03/manifest.json)
- [Fresh verification](../archive/scans/1984-03/review/verification.json)
- [Recipe](../metadata/catalog/scans/1984-03-recipe.json)
- [Result record](../metadata/catalog/scans/1984-03-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/1984-03
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
