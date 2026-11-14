# Donated scan cleanup

Keep this a practical tidy-up: make the scans easy to browse and restore, while
keeping the original donation available if a decision needs revisiting.

## First look — November 14, 2026

`maso-img/` currently contains 59 ZIP files for 24 issues, about 98.36 GiB.
The issue directories are inside the ZIPs. Together they contain 12,143 JPEG
entries, 12,157 Mac `._` sidecars, and sixteen ordinary text-note entries.

ZIP CRC/size comparisons suggest 6,070 distinct images within the issue sets,
about 49.16 GiB. Most images have an ordinary copy and a `(1)` copy. Five sampled
pairs also matched by SHA-256; a complete content-hash pass is still needed.
No JPEG CRC/size matches were found between different issues.

Useful extras include spines, payment slips, postcards, and alternate scans of
damaged pages. Preserve those. Cover names are inconsistent: April 1984's
`AFront001.jpg` is the spine and `AFront002.jpg` is the front cover.

Filename gaps found in the first look:

| Issue | Missing filename numbers within the observed range |
| --- | --- |
| 1984-02 | 13–16 |
| 1984-03 | 11–12 |
| 1984-04 | 13–14 |
| 1985-12 | 18, 20 |
| 1987-01 | 65–68 |
| 1987-03 | 207–208 |
| 1987-04 | 167–168 |
| 1987-07 | 93–96 |
| 1987-08 | 175–176 |
| 1987-12 | 129–136, 191–192 |

These are filename gaps, not yet a verified inventory of missing printed pages.
December 1983's ordinary sequence begins at 3; that alone does not establish
missing pages 1–2. Complete filename numbering does not establish completeness.

The donor's notes add useful context but occasionally have inconsistent issue
numbers or dates. March 1984's note mentions a missing advertising sheet and
uncertain ordering from page 261 onward. June 1987's note says 191–192 were torn
out, although scans named for both pages exist. July 1987 includes damaged and
complete-looking alternatives for pages 19–20. Check these visually.

## Working plan

1. Leave the ZIPs in `maso-img/` unchanged. Group all ZIP parts for each issue
   before sorting; ZIP member order is not reading order.
2. Read every entry and verify ZIP CRCs. Hash image bytes with SHA-256 and keep
   one working copy of each identical image. Omit confirmed Mac sidecars from
   the working image set; record their source locations. Keep donor text notes.
   Different images with similar names remain separate alternatives.
3. Build one issue directory under `archive/scans/YYYY-MM/`, with `pages/`,
   `covers/`, `extras/`, a manifest, and small contact sheets. Preserve original
   JPEG bytes. Do not crop, rotate, recolour, or recompress the working masters.
4. Use contact sheets and selected larger views to identify cover faces, spines,
   inserts, damaged alternatives, and suspicious boundaries. Keep reading order,
   source filename numbers, and verified printed page numbers as separate fields.
   Leave uncertain printed numbers unset. Do not create replacement pages.
5. Record each working file's hash, original ZIP/member names, dimensions, role,
   and proposed reading order. Keep a short issue report describing gaps and
   decisions. Store small recipes and summaries in `metadata/catalog/scans/`;
   private scans and image derivatives stay outside Git under `archive/scans/`.
6. Independently check extracted hashes, duplicate accounting, output inventory,
   and ZIP preservation. Try April 1984 first, then March 1984's awkward cases.
   Review the pilots before processing the rest of the donation.

No OCR restoration or reading-room integration is part of this cleanup pass.

## April 1984 pilot

The pilot recipe is `metadata/catalog/scans/1984-04-recipe.json`.
Run it from the repository root with:

```sh
python3 -m tools.scan_cleanup --recipe metadata/catalog/scans/1984-04-recipe.json
```

The command creates a new issue directory and refuses an existing destination.
It retains a partial staging directory on failure for inspection. The resulting
manifest and contact sheets are under `archive/scans/1984-04/`.

The [April pilot report](docs/SCAN-PILOT-1984-04.md) records the completed first
pass: 257 byte-preserved scans, nine contact sheets, verified duplicate and
sidecar accounting, and twelve checked printed page numbers. The only filename
gap is 13–14. This was the first checkpoint; subsequent issue status is maintained
in [PROGRESS-SCANS.md](PROGRESS-SCANS.md).

## Continuing the campaign

The user authorized cleanup of all donated issues, with a progress update and a
separate commit for each issue. March 1984's second pilot is checked; its
[report](docs/SCAN-ISSUE-1984-03.md) retains the uncertain late-page order.

`tools.scan_campaign` prepares candidate recipes and review previews, then records
explicitly supplied visual findings. Inspect the overview, covers, boundaries,
inserts and enlarged printed-number samples before supplying review decisions.
Recipe numbering is provisional; source filenames do not prove printed numbers.

```sh
python3 -m tools.scan_campaign --prepare YYYY-MM
python3 -m tools.scan_cleanup --recipe metadata/catalog/scans/YYYY-MM-recipe.json
python3 -m tools.scan_campaign --assets YYYY-MM
# Save the actual visual findings in the issue's review/decisions.json, then:
python3 -m tools.scan_campaign --finish YYYY-MM --decisions archive/scans/YYYY-MM/review/decisions.json
```

The finish step rechecks all ZIP entries and output hashes, records the review,
exports a page list, writes an issue report/result record, and updates progress.
Commit only that issue's tracked recipe, result and report plus the progress
update and any shared-tool changes. Original scans and previews stay outside Git.
