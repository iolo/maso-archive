# November 1984 scan restoration handoff

November's pilot restoration preserves **34 complete native article packages**
and **six non-owning headings**, covering all 40 canonical TOC identities.
The separate cover set retains all four original faces. All **246 retained
JPEGs** have explicit source outcomes: 205 used by selected articles, four
covers, and 37 other images. Nothing awaits visual disposition.

The [issue ledger](../metadata/catalog/scan-restoration/1984-11-progress.json)
is the selection authority. The
[whole-issue result](../metadata/catalog/scan-restoration/1984-11-issue.json)
records the export, audit, recipe, implementation and regression pins. Earlier
article results and frozen evidence remain intact.

The native issue is at `archive/scans/1984-11/packages/issue-r01/`:

- `issue.json`, `schema.json`, retained recipe/input files and an exact manifest;
- 34 unchanged native component directories under `articles/`;
- the four-face native package under `covers/`;
- original classification/context evidence under `headings/`;
- 37 byte-identical original scans under `other-sources/`;
- complete 246-image source accounting, retaining source groups and provenance.

There are **6,306 exact files** in the issue. All 34 selected articles were also
freshly rebuilt from their original pinned recipes: **6,237 exact native files**.
This is a separate check from copying them into the issue.

From this checkout and its retained archive, check the package with:

```sh
env PYTHONPATH=src:. python3 -m tools.pdf_restore.image_issue \
  --check --output archive/scans/1984-11/packages/issue-r01
```

Reproduce the issue into a new directory with:

```sh
env PYTHONPATH=src:. python3 -m tools.pdf_restore.image_issue \
  --recipe archive/scans/1984-11/restoration/batch-61/issue-recipe.json \
  --output work/validation/november-issue-fresh
```

The saved recipe pins the frozen construction ledger, canonical TOC, source
descriptor and complete source-accounting report. All selected component inputs
must be available. The exported directory's checker works without those original
workspace inputs. Rebuilding requires them; external evidence references do not
mean the whole working archive is embedded in the export.

The whole-issue result also lists the 34 original article recipes, their public
`tools.pdf_restore.build` or `tools.pdf_restore.assemble` entry points and saved
exact rebuild receipts. Use fresh outputs for reproduction. Reuse successful OCR;
do not execute private frozen checkpoint helper scripts.

The source fidelity review, continuity/structure checks, exclusions, original
figures, qualified folios, glyph alternatives and per-article review limitations
remain in the native components and their evidence. Original `gaps` fields also
retain local unknown glyphs/counts, unproved local associations, source example
elisions and verification limits. “Complete” records structural restoration and
artifact reproducibility; it does not mean character-perfect proofreading,
human acceptance, verified historical claims, recovered original encoded bytes
or executed programs.

The 37 other images comprise 25 advertisements, one contents/credits/colophon
page, five notices, four illustrated section dividers and two wide forms. They
retain original rasters and selected disposition labels, without full text
transcription or invented article-body ownership. Contest notices at source
filenames 60–63 form one group; the monthly invitation at 209 is distinct.
The two wide form scans remain intact and unrotated; their physical recto/verso
identity is unverified. No physical-page completeness is inferred from filenames.

The final gate passes **275 fresh tests**: 214 PDF, 48 JPEG/recognition/assembly,
seven cover and six issue tests. The three original ZIPs and all JPEG masters
are retained unchanged. The shared OCR/PDF plans and four saved reader snapshots are intact.
No reader implementation, build or deployment was part of the restoration
closeout. The reading room remains the earlier one-time visual sample.
