# Literal CP/M assembly

`tools.pdf_restore.cpm_literal_assembly` adds the explicit `cpm-literal-v1`
assembly mode for reviewed, disjoint native maps with unnumbered transcripts.
It preserves original packages and complete native correction metadata. Source
text, addresses, editor labels, opaque object strings, blank cells and graphics
are not rewritten or interpreted.

Every native array is projected into the combined coordinate system. Nested
compiler cells inherit their download coordinates; table prefixes and table
starts retain separate offsets. Zero-length blank fields are valid only at
UTF-8 boundaries. Projected excerpts must equal their original occurrences.
Source IDs remain unchanged and must be unique across native maps.

The reviewed figure-16 association connects its original opening and ending
frames to the observed ending caption. The additional opening listing link is
marked as assembly-derived, with its caption-source segment retained separately.
Original caption metadata remains in the copied native packages and metadata.
Existing multi-frame links remain intact. Uncaptioned originals stay uncaptioned.

```sh
PYTHONPATH=.:src python3 -m tools.pdf_restore.cpm_literal_assembly \
  --recipe archive/pdf/1984-12/restoration/cpm5-assembly/assembly-recipe.json \
  --output FRESH_ARCHIVE_OUTPUT

PYTHONPATH=.:src python3 -m tools.pdf_restore.cpm_literal_assembly \
  --check --output EXISTING_EXPORT
```

Use `cpm_literal_assembly.check(folder)` for checks that include this format, or
its `installed()` context around ordinary export/issue checks. That context also
installs the existing graphic dispatcher and delegates older formats to it,
including BASIC speed and Crowded Speedway. Installation is scoped and restores
both dispatch and recipe validation even after an exception. No existing pinned
projector file changes are required.

The six focused regressions cover blank fields, UTF-8 boundaries, nested ranges,
source excerpts, external evidence pins and scoped installation. The private
four-native probe additionally compares all native metadata and projected byte
occurrences against the December originals. Human acceptance, full proofreading,
source encoded bytes and execution remain separate, unverified claims.
