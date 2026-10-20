# Perspective literal assembly

`tools.pdf_restore.perspective_literal_assembly` is an opt-in dispatcher for
`perspective-literal-v1`. Other formats delegate to the existing CP/M and graphic
adapters. The earlier implementation files remain unchanged.

Recipes name immutable native manifests, ordered expected PDF pages, one explicit
`region_revisions` contract and `prose_continuations`. The revision binds an exact
target manifest, region, block, geometry and one observed parenthesis insertion.
It cannot add a page, duplicate a section, alter other text or replace part of a
multi-region block. All native files, including superseded evidence, are copied
unchanged into the output's `segments/` directories.

The active region, block, crop, OCR and occurrence indexes use the revision once
at the original reading position. All original correction fields and arrays remain
in `native_metadata`; superseded regional indexes and the incorrect absence claim
remain archival provenance there. Original source values are never repaired from
mathematical, program or firmware expectations.

Every native array category is projected recursively, including nested UTF-8
ranges, zero-width fields, physical/logical code rows, matrix cells, ellipses,
flow labels, DATA, output values, quotes, comments, numeric and punctuation indexes.
Article positions use their own block occurrence; listing positions use exact
concatenated physical bytes. External evidence pins keep their original roots.
Source blocks, physical wraps and image anchors remain unchanged. Cross-native
prose and listing continuation records connect the source without executable
flattening or relocating the original images.

Pending listing captions resolve only when the exact native manifest, caption
block/region, download bytes and scan pins agree. Original caption provenance is
retained separately. Uncaptioned source drawings remain uncaptioned.

Run from the repository root, always with fresh output/report destinations:

```sh
PYTHONPATH=.:src python3 -m tools.pdf_restore.perspective_literal_assembly \
  --recipe RECIPE.json --output archive/pdf/YYYY-MM/packages/FRESH
PYTHONPATH=.:src python3 -m tools.pdf_restore.perspective_literal_assembly \
  --output archive/pdf/YYYY-MM/packages/FRESH --check
```

Use `perspective_literal_assembly.check()` or `installed()` for all-selected issue
checks after promoting a perspective assembly. The wrapper delegates older formats;
calling an older dispatcher directly cannot validate this new format. The normal
assembler provides immutable native copying, deterministic ZIP creation, independent
reproduction and offline re-projection checks. No reader or frontend rebuild is part
of this workflow.
