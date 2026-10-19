# Table and literal source assembly

This separate entrypoint preserves printed BASIC/hex source fields together with
complete TSV tables and listing-caption associations. Existing assembly modules,
their pinned implementations and legacy outputs remain unchanged.

Every native correction must opt in through
manual_postproduction.literal_table_source_fields_format = "v1".
Use fresh flag-only native revisions that retain the original four metadata files,
all original correction key/value pairs and every source text/image/OCR byte.
The recipe uses wrapped-listing-v1. Cross-segment prose/logical joins and the other
BASIC/literal opt-ins are rejected; complete native prose joins remain preserved.

Run from the repository root with PYTHONPATH=.:src:

    python3 -m tools.pdf_restore.table_literal_assembly --recipe RECIPE --output FRESH_OUTPUT
    python3 -m tools.pdf_restore.table_literal_assembly --check --output EXISTING_OUTPUT

Offline checks, later selected-package audits and issue closeout must use this
entrypoint or tools.pdf_restore.table_literal_assembly.installed() around the
normal operation. The adapter restores the original projector on exit, including
exceptions. Ordinary check_export outside that context rejects these assemblies'
additional correction indexes; it cannot certify this format.

Every table cell has an exact source occurrence, including zero-byte blanks,
duplicate labels, headers and merged-description continuation blanks. No absent
address digits or implied labels are supplied. Tables, notes, ranges and IDs are
namespaced; source_segment/source_range preserve the native coordinates.
Listing-caption links retain their exact heading span, listing group, code blocks
and original panel identities. All source caption blocks must be accounted.

DATA values stay strings. A decimal literal may contain a physical newline inside
its digits (for example 13/newline/indentation/3). Its exact spelling and clipped
physical scan segments remain; it is never converted to 133 or an encoded byte.
Quotes, bare-letter fields, short hex rows, repeated addresses and source candidates
follow the same occurrence checks as the earlier literal projector.

Physical and logical row ordinals are global; native ordinals remain in
source_article_physical_line/source_logical_line. Hex unit_id is namespaced,
source_unit_id remains native, and physical_line_id links to the combined row.
No address arithmetic, gap filling, opcode validation, checksum calculation,
character decoding or graphic-pattern reconstruction is performed. Source bytes,
execution, human acceptance and full proofreading remain unverified.

Unknown metadata remains verbatim in each segment's original_metadata.
Tests: tests/test_pdf_table_literals.py; run make test-pdf.
