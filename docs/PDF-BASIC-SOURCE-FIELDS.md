# Wrapped BASIC source fields

`wrapped-listing-v1` accepts the optional correction metadata flag
`basic_source_fields_format: "v1"`. Every segment must opt in together. Existing
assemblies without the flag retain their previous projection.

The extension validates each native physical and logical listing occurrence before
projecting regional text, review notes, table cells (including blanks), caption
links, quoted strings and DATA fields into the combined UTF-8 downloads. Repeated
strings retain separate source occurrences. Fields crossing physical rows retain
their exact newline, indentation and clipped scan segments. Original correction
metadata remains available in each assembly segment record.

DATA categories distinguish printed machine hex/checksum pairs, sprite and
character hex, decimal values, quoted panel strings and unquoted music source.
Values remain source literals. The projector does not calculate checksums, infer
encoded bytes, repair syntax, normalize graphic glyphs or certify execution.

Older natives can receive a fresh metadata-only compatibility revision. Preserve
the original package, every original metadata file and the revision procedure;
prove that restored text, images, maps and raw OCR bytes are unchanged. Assemble
the revision alongside the original source evidence, then independently check
the combined ranges and a byte-identical rebuild.

Validation: `make test-pdf`. The source-field tests exercise Unicode wraps,
repeated strings, blank cells, negative decimal spacing, scan attribution,
incomplete coverage and false checksum verification claims.
