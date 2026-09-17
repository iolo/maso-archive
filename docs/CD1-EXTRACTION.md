# CD1 extraction probe

Date: 2026-09-18. Direct extraction is feasible; normalized article records and
comparison against the original viewer are still pending.

## Viewer setup

The owner installed and ran CD1 in DOSBox-X and supplied `masocd-1/`, an extracted
copy of the ISO. The local configuration mounts `hwin31/` as C: and the original
ISO as D:.

The executable is `MVIEWER2.EXE`. `TITLE.MST` copies the `[System Files]` section
to the Windows system directory, registers the MVB association, and creates a
Program Manager item pointing to `MASOCD.MVB` in the source directory. The
`[Installed Title Files]` section of `TITLE.INF` is empty. Thus the viewer/runtime
is installed, while the magazine content stays on the CD. The local Windows
system directory contains `MVIEWER2.EXE`, consistent with this behavior.

## Reproduction

Source file: `masocd-1/MASOCD.MVB`, 259,490,690 bytes.

```text
SHA-256: bde731b36c6a9e37ba0f23e4fce66758417753073cb537b7cc8d6dddfcd02565
```

Decoder: [joncampbell123/helpdeco](https://github.com/joncampbell123/helpdeco),
revision `b9c187a20d83a3e738d8fe073eb924a8b7264c5c`.

Build in a separate tool checkout:

```sh
make helpdeco CFLAGS='-g3 -O0 -Wno-error=incompatible-pointer-types'
```

The current compiler rejects two legacy pointer assignments in the default
build. The compatibility flag permits this exploratory build without editing
upstream code. Numerous format warnings remain; this is not yet a production
decoder dependency.

From a fresh, empty output directory, run the built executable with a **relative**
path to the MVB and `/g`. The following assumes the output directory is
`private/cd1-probe/raw/` under the repository and the tool remains in `/tmp`:

```sh
/tmp/maso-helpdeco/helpdeco ../../../masocd-1/MASOCD.MVB /g
```

Use `/d` instead of `/g` to list the internal directory. `/g` disables context
name guessing; it does not restrict extraction to a sample. This tool interprets
leading `/` as an option, so an absolute Unix input path prints usage instead of
decoding, even with exit status zero. Validate outputs, not only the exit code.
The preserved run used an empty temporary directory and copied its results into
the private output directory afterwards. Do not rerun into these preserved files.

## Results

The decoder completed with exit code zero, reporting topics through 3099 and
2,103 loaded topic-offset/hash records. These are internal record counts, not
counts of distinct magazine articles.

| Output | Count / size |
| --- | ---: |
| `MASOCD.rtf` | 74,157,536 bytes |
| `.dib` resources | 4,992 |
| `.wmf` resources | 2,345 |
| `.bmp` resources | 25 |
| `.shg` resources | 2 |
| Korean `.lst` indexes | 3 |
| Other decoded files | Project file, table, icon, AVI |

There are 7,372 decoded files, plus two captured process logs. Their combined
size is 270,966,330 bytes. Output names, sizes, and SHA-256 hashes are recorded
in `private/cd1-probe/manifest.json`; originals are in `private/cd1-probe/raw/`.
Build diagnostics and the container directory listing are retained alongside
them. These paths are excluded from Git.

The introductory text explicitly states a collection period of **1988.1–1993.12**
and a CD publication date of **1994-12-01**. This confirms the declared period;
it does not establish completeness relative to every printed issue.

The three indexes decode strictly as CP949 and contain 1,038 distinct seven-digit
references across them:

| Reference year | Distinct references |
| --- | ---: |
| 1988 | 58 |
| 1989 | 113 |
| 1990 | 189 |
| 1991 | 183 |
| 1992 | 227 |
| 1993 | 268 |

This supplies 360 candidate references for the target years 1988–1990. References
can overlap across indexes, and the indexes may omit records: do not use these
counts as final article totals. Preserve the category paths from all indexes.

## Validation and remaining work

- Found readable Korean article text after inspecting RTF hex escapes, including
  the UNIX feature, postal-code conversion program, and the December 1990
  computer-controlled Tetris article. This is text recovery, not OCR.
- The RTF preserves title, keyword, browse, and context footnotes as well as
  references to image resources. Retain these when constructing article records.
- Pillow successfully decoded one extracted `.dib` and one `.bmp` resource.
  WMF/SHG rendering and complete image validation remain untested.
- No error/warning/unknown/unsupported/invalid/failure message was found in the
  decoder's runtime log. Compilation warnings remain, and runtime success is
  not proof of faithful extraction.
- The raw RTF bytes decode as CP949, but much of the actual text uses RTF hex
  escapes. Expanding all escapes and decoding the entire result as CP949 fails
  at a font-specific character. Production conversion must parse RTF groups,
  font/charset state, escaped bytes, and symbol runs instead of replacing errors
  or stripping markup with a regular expression. Preserve the raw RTF unchanged.
- Viewer rendering, full printed-page coverage, precise image/article
  relationships, and original context-ID recovery remain to be checked.

The next extraction step is a small RTF normalization and topic-mapping pilot,
using the three recovered indexes and original viewer for comparison. Bulk OCR
is unnecessary for the recovered article text. The existing 1983–1987 plan is
unchanged: TOC metadata now, scans supplied later.
