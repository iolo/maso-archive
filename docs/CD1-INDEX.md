# CD1 reference-index importer

This implements step 1 of [the plan](../PLAN.md). It structures the three
extracted index files while preserving every occurrence and its provenance.
It does not read RTF, article bodies, or images, and does not match the TOC.

## Run

Use the same Python environment as the TOC importer:

```sh
make import-cd1-index
```

Explicit paths, useful for a different local extraction directory:

```sh
PYTHONPATH=src python3 -m maso_archive import-cd1-index \
  --source-dir private/cd1-probe/raw \
  --manifest private/cd1-probe/manifest.json \
  --output build/cd1-index
```

The input directory must contain `column.lst`, `language.lst`, and `panecmds.lst`.
Each input's size and SHA-256 must match its `raw/<filename>` entry in the supplied
extraction manifest. Only these three files and the manifest are read; the MVB,
RTF, and all other extracted files can be absent for this command.

## Outputs

| File under `build/cd1-index/` | Contents |
| --- | --- |
| `entries.jsonl` | One record per nonblank source line, including categories, references, terminators, and any unparsed lines. |
| `references.jsonl` | One record per distinct native reference, with every occurrence ID and all distinct title variants. |
| `validation-report.json` | Per-file and combined accounting, review notices, and comparison with the earlier numeric-reference counts. |
| `manifest.json` | Input/extraction-manifest/schema/output hashes, importer/runtime versions, and the container hash recorded by the earlier extraction. |

The container hash is inherited provenance, not a new check of the MVB file.
All outputs remain local under the Git-ignored `build/` directory. Source files
and the extraction manifest are unchanged. No permanent article IDs are allocated.

## Reading a record

An occurrence retains its full raw line, original reference string, normalized
reference (surrounding whitespace removed), label, indentation, parent occurrence,
and ordered category path. Provenance includes filename, SHA-256, CP949 encoding,
line number, and a byte offset/length into the original file. The byte span
includes any line ending; `raw_line` does not.

Occurrence IDs combine source filename, source hash, and line number. They locate
evidence in a particular source version and are **not** persistent TOC/article
identities. A category-path element includes both its label and occurrence ID,
so repeated category names remain distinguishable.

Follow a grouped reference's `occurrence_ids` back to `entries.jsonl` to recover
every category, label, and source location. Grouping does not merge or discard
individual occurrences, even when a reference repeats within the same index.

The source convention is `label|target`. `*` marks a category; a standalone `@`
is retained as a terminator. The named target `mscdmenu` is a navigation reference,
not an article. Letter-suffixed references remain distinct from seven-digit
references: `9304410a` must not become `9304410`.

A leading `YY.MM` in a label supplies a display issue and is removed from the
separate title field. The original label is retained. A `YYMMPPP`-shaped reference
supplies only an **issue candidate**, used for counting the target period. There
is no verified page mapping yet. In particular, `9311000` remains intact and its
`000` component is flagged rather than treated as a valid printed page zero.

## Validation and failure behavior

Decoding is strict CP949. Missing files, invalid encoding, invalid manifest
structure, missing/duplicate manifest entries, and checksum/size mismatches reject
the import, return a nonzero exit code, and write `failed-import-report.json`.
They leave previous successful outputs unchanged. A successful rerun removes the
obsolete failure report.

Unexpected line syntax is preserved as `unparsed` and reported. Irregular
indentation, missing/repeated terminators, content after a terminator, padded
references, date disagreement, and zero page components produce review notices.
A successful command means the sources were accounted for, not that all notices
have been resolved or article identities verified. An ambiguous line is not
silently grouped as a reference.

Entries and reference groups pass `schemas/cd1-index.schema.json`. Additional
checks confirm unique occurrence IDs, parent links, and exact accounting between
reference occurrences and groups. No timestamp is added, so identical inputs and
tool/runtime versions yield byte-identical outputs. Successful files are replaced
atomically one at a time; verify manifest hashes after an interrupted write or
rerun the command to rebuild the set.

## Results for the supplied CD1 indexes

| Input | Lines | Categories | Reference occurrences | Terminators |
| --- | ---: | ---: | ---: | ---: |
| `column.lst` | 1,311 | 234 | 1,076 | 1 |
| `language.lst` | 846 | 187 | 658 | 1 |
| `panecmds.lst` | 875 | 146 | 728 | 1 |
| Total | **3,032** | **567** | **2,462** | **3** |

There are no blank or unparsed lines in these inputs. The grouped output contains
**1,080 targets**: 1,038 seven-digit references, 41 letter-suffixed references, and
one named navigation target. The seven-digit references include **360 candidates
for 1988–1990**, matching the earlier observation. The other reference forms are
reported separately, not discarded to make the counts agree.

The 12 notices are nine category references with trailing spaces and three
occurrences of `9311000`. Their original bytes/values are retained. The baseline
comparison applies only to the three exact input hashes previously inspected;
other input revisions are labeled `not_applicable` rather than forced to match.

The provisional reference `8802065` occurs in `column.lst` at line 3 and
`panecmds.lst` at line 112, with separate category paths. Confirming its TOC
identity is **step 2**, not a result of this importer.

Run `make check` for the tests. Synthetic fixtures cover provenance, mixed line
endings, hierarchy, repeated/suffixed/named references, syntax exceptions, manifest
and encoding failures, deterministic reruns, and CLI operation without any article
files. A real-source test checks all lines and the historical counts when the
private index files are available; it is skipped in checkouts without them.
