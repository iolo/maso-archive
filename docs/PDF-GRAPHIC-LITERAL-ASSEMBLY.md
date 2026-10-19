# Graphic, font and table source assembly

This explicit entrypoint preserves source tables, printed BASIC/hex literals,
font definitions and graphic candidates together. All previous implementation
files and native outputs remain unchanged. The complete native corrections stay
visible to the projector; no specialized field is removed or hidden in metadata.

Every native must opt in through
`manual_postproduction.graphic_table_source_fields_format = "v1"`.
Use fresh flag-only native revisions preserving every original correction value,
all four original metadata files, source text, images and OCR. The recipe uses
`wrapped-listing-v1`; cross-segment prose/logical joins and conflicting older
BASIC/literal/table opt-ins are rejected.

Run from the repository root with `PYTHONPATH=.:src`:

    python3 -m tools.pdf_restore.graphic_literal_assembly --recipe RECIPE --output FRESH_OUTPUT
    python3 -m tools.pdf_restore.graphic_literal_assembly --check --output EXISTING_OUTPUT

Future selected-package/index/issue-closeout operations containing this format
must use `graphic_literal_assembly.check` or its `installed()` context around the
normal operation. The context restores the previous projector even after an
exception. Its unflagged fallback supports the older explicit table/literal
format, including Crowded Speedway, without changing any historical output.
Ordinary default checking cannot certify the new correction indexes.

The common projection preserves all earlier table, blank-cell, regional, review,
prose, quote, DATA, hex-dump, listing and caption occurrence checks. Its separate
implementation starts from the pinned table/literal projector. The new indexes
are validated and projected in addition to those common indexes:

- `basic_hex_literal_index` exhausts every actual `&H` spelling in numbered
  logical source units. Physical `&`/newline/`H8000` remains split; short literals
  stay short. Repeated values retain distinct ranges and physical scan clips.
- `font_definition_index` exhausts printed `DEF CHR$` units. Every full unit,
  physical source part, clipped scan and literal field spelling remains exact.
  No character label sequence or font bitmap is inferred.
- `graphic_string_index` exhausts logical source units with Unicode/graphic
  candidates. Every editorial marker retains its exact UTF-8 occurrence and
  physical source clips. Unknown run widths/counts and encoded bytes must remain
  explicitly unverified. Visible alternative labels and unknown metadata remain
  verbatim; editorial markers are not printed source characters or runnable code.

Projected ranges address the combined downloads. `source_segment` and
`source_range` retain native coordinates; block/region IDs, physical/logical
source-part references, marker ranges and nested scan pins are rebased explicitly.
Original native ordinals remain alongside combined row ordinals. Every segment's
`original_metadata` retains all original fields, including every specialized index.

Source errors, glyph candidates, blank cells, physical wraps and Unicode visual
approximations stay literal. The projector never decodes bytes or repairs source
using syntax, hardware, address arithmetic, checksums, key layouts or graphic
patterns. Human acceptance, full proofreading, original bytes and execution remain
unverified. Tests: `tests/test_pdf_graphic_literals.py`; run `make test-pdf`.
