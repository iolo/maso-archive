# Printed BASIC and hexadecimal source fields

Use wrapped-listing-v1 with every segment correction opting in through
manual_postproduction.literal_source_fields_format = "v1". Retain immutable
natives; adding this metadata requires fresh revisions that preserve all four
original metadata files. Legacy wrapped output is unchanged without this flag.
Do not combine this mode with basic_source_fields_format.

The opt-in projects regional article/listing spans, text notes, inline examples,
caption associations, image preservation, literal quotes, mixed BASIC DATA,
hex rows, address labels, literal fields and source uncertainties. Existing
wrapped assembly first proves physical/logical rows and source listing groups.
The extension requires complete segment-local units; cross-segment logical joins
are rejected. Tables and specialized BASIC category indexes require another mode
and are rejected here rather than dropped.

Every DATA value remains a string. Bare letters, quoted punctuation, leading
zeroes and internal physical newlines/indentation remain source text. Quote and
DATA occurrences are checked in source order by exact UTF-8 spans and clipped
physical scan segments. No numeric conversion, key encoding or program repair
is performed.

Hex rows retain their actual field counts, including short first/final rows.
Addresses are literal labels: there is no address arithmetic, inferred gap fill,
byte decoding, opcode validation, shape reconstruction or checksum calculation.
Repeated addresses retain native occurrence counts and distinct namespaced units.
Every address and field must match the corresponding physical source occurrence.

Combined unit_id prefixes the native unit with the segment name.
source_unit_id retains the native unit identity. On hex rows and fields,
source_line_id remains the segment-local physical identity and physical_line_id
links to the combined physical row. Source parts and clipped scan spans address
the combined listing; source_range and source_segment retain original coordinates.
Physical rows gain a global article_physical_line while preserving
source_article_physical_line. Logical identifiers follow existing wrapped rules;
logical_line is global and source_logical_line preserves any native ordinal.

Unknown native metadata stays verbatim in each segment's original_metadata.
Source bytes and execution remain unverified; any encoded-byte payload or positive
verification claim is rejected. Assistant source review does not establish human
acceptance or full proofreading.

Regression coverage: tests/test_pdf_source_literals.py. Run make test-pdf.
