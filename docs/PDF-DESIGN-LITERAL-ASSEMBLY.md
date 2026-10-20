# Literal design-article assembly

`tools.pdf_restore.design_literal_assembly` adds the opt-in `design-literal-v1`
mode for disjoint reviewed native maps containing prose, BASIC, opaque assembly,
patch/data fields, tables, diagrams and original images. Other formats delegate
to the existing perspective/CP/M/graphic dispatcher. No existing pinned adapter
is modified.

Every native file is copied by the standard assembler. Full original correction
metadata is retained under `native_metadata`. Every additional top-level native
array is projected recursively, including nested and zero-length UTF-8 ranges.
`native_array_ranges` records each segment/category's exact slice. Core records,
blocks and normalization/caption/source-evidence metadata retain their established
assembly representation and complete immutable originals.

Ranges must belong to their own block and regional occurrence. Parent records'
scan identity is checked even when only their nested cells have byte endpoints.
Local scan pins are rebased; external provenance remains external. Native article
blocks and listing bytes stay exact. IDs must be disjoint, source/page scope must
match explicit coverage, the final native must defer no source pages, and pending
caption associations require review. Scoped installation restores all dispatchers
even after an exception.

Printed BASIC labels remain source labels. Physical comments, blank rows, quote
runs, opaque byte/address/port/storage fields, unknown bands and source mistakes
are not interpreted or repaired. The December design article's final END stays
on its leading-semicolon physical row. The MEMOF comment tail remains uncertain;
no completion, missing-glyph count, encoded message bytes, alias arithmetic or
execution is inferred. Human acceptance, full proofreading and source bytes remain
separate unverified claims.

```sh
PYTHONPATH=.:src python3 -m tools.pdf_restore.design_literal_assembly \
  --recipe ASSEMBLY_RECIPE.json --output FRESH_ARCHIVE_OUTPUT

PYTHONPATH=.:src python3 -m tools.pdf_restore.design_literal_assembly \
  --check --output EXISTING_EXPORT
```

Use `design_literal_assembly.check(folder)` for checks that include this format,
or `installed()` around ordinary export/issue checks. Earlier selected packages
continue through the compatibility dispatcher.

Ten focused regressions cover future nested categories and scalar retention,
blank cells/UTF-8, mixed BASIC/comment rows, incorrect source ownership/scans,
physical-byte changes, incomplete scope, pending captions, duplicate identities,
compatibility delegation and scoped restoration. The private five-native probe
reverse-compares all 279 segment/category occurrences and 29,792 UTF-8
occurrences, preserves all 440 input files and retains 1,759 physical rows.
The probe creates no readable export and does not promote the issue ledger.
