# April 1984 scan cleanup pilot

Completed November 14, 2026. The clean working set is in
[`archive/scans/1984-04/`](../archive/scans/1984-04/README.md).
The original donation ZIPs remain unchanged in `maso-img/`.

## Result

| Item | Count |
| --- | ---: |
| Source ZIPs | 2 |
| ZIP file entries checked | 1,028 |
| Actual JPEG entries | 514 |
| Byte-identical duplicate JPEG copies omitted | 257 |
| Confirmed AppleDouble sidecars omitted | 514 |
| Retained JPEG masters | 257 |
| Proposed reading-order entries | 256 |
| Spine scans outside reading order | 1 |
| Contact sheets | 9 |
| Enlarged printed-number samples checked | 12 |

The retained JPEGs occupy **1,889,010,983 bytes, about 1.76 GiB**, before contact
sheets and review previews. They comprise 252 source-numbered scans, four cover
faces, and a spine. No image adjustment or recompression was applied to masters.

The cover assignments were checked visually. `AFront001.jpg` is the spine,
`AFront002.jpg` is the front cover, and `AFront003.jpg` is the inside-front
cover. `Rear001.jpg` and `Rear002.jpg` were assigned inside-back and back roles.

All nine contact sheets were viewed. Source slots 247–248 contain subscription
postcards and 249–250 contain payment slips; those scans remain in source order
and are flagged as inserts in the review/page list. Their filename numbers are
not verified printed pagination.

Printed numbers **15, 16, 17, 30, 98, 129, 160, 191, 224, 241, 245, and 246**
were checked in enlarged lower-margin crops and match their source filenames.
The front cover and TOC identify April 1984, issue 6.

## Open gap

Neither ZIP contains source filenames for **13–14**. The available scan before
the gap is an advertisement; the next is the editor note with printed page 15.
The contents and reason for the absent span remain unverified. No replacement
pages were created. No additional gross ordering anomaly was apparent at contact
sheet scale. Full pagination and physical collation have not been checked.

## Files and checks

- [Page list](../archive/scans/1984-04/page-list.csv): proposed reading order,
  reviewed roles, source numbers, and the twelve verified printed numbers.
- [Contact sheet 1](../archive/scans/1984-04/contact-sheets/sheet-01.jpg) and
  [sheet 9](../archive/scans/1984-04/contact-sheets/sheet-09.jpg): beginning,
  inserts, rear covers, and spine. Sheets 2–8 cover the middle of the issue.
- [Extraction manifest](../archive/scans/1984-04/manifest.json): original
  ZIP/member mappings, hashes, dimensions, duplicate groups, and all sidecars.
- [Visual review](../archive/scans/1984-04/review.json): findings and reviewed
  overrides. This supplements the generated manifest's initial review status;
  the manifest remains an unchanged record of extraction.
- [Verification](../archive/scans/1984-04/review/verification.json): all 1,028
  original entries re-read and matched to the manifest, all 257 working hashes
  checked, all nine contact sheets checked, and original ZIP hashes unchanged.

Every retained JPEG fully decoded during extraction. Re-running extraction
against the existing destination was also checked: it refuses before writing.
Small recipe/result records live in `metadata/catalog/scans/`; scans and
derivatives are Git-ignored under `archive/scans/`.

From the repository root:

```sh
# Repeat verification without changing the working set:
python3 -m tools.scan_cleanup --verify archive/scans/1984-04

# Extraction recipe; refuses the now-existing destination:
python3 -m tools.scan_cleanup --recipe metadata/catalog/scans/1984-04-recipe.json
```

The next step is March 1984: preserve its donor note, inspect its late-page order,
and keep postcards and the spine separate from ordinary pagination. That pilot
has not been run. See the [overall plan](../PLAN-SCANS.md).
