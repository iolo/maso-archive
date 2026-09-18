# Initial source inspection

Inspected 2026-09-18. This is a planning-time observation record, not a completed
preservation or extraction pipeline. Original inputs were not modified.

Follow-up: CD1 has since been run by the owner and directly decompiled in a
host-side probe. See [CD1 extraction findings](CD1-EXTRACTION.md) for confirmed
declared coverage, recovered files, and remaining encoding/validation work.
The observations below describe the initial inspection before that probe.

Step 11a now provides the [complete CD1 source inventory](CD1-PRESERVATION.md):
5,828 ISO/extracted files, 375 directories, and 7,377 probe/support files checked.
Independent backup/restore verification remains pending; the owner confirmed that
no independent backup exists yet. CD2/CD3 observations below remain preliminary.

## TOC

`TOC.md` is 153,894 bytes and contains 86 unique monthly headings from `83.11`
through `90.12`, with no missing or duplicate issue headings. It contains 3,811
bullets across multiple nesting levels. Of these, 1,129 do not end in an explicit
`= number` page marker. These counts include sections and subtopics; they are
not counts of articles or missing article pages.

Examples requiring careful import:

- `83.11`: a feature heading has a page while its subtopics do not.
- `83.12`: apparent hierarchy and transcription anomalies should be flagged,
  not silently corrected.
- `90.05`: a feature contains another level of nested topic bullets.
- Throughout: corporate authors, translators/editors, multiple authors, article
  series, and TOC order that does not necessarily follow printed page order.

## Disc inventory

Counts exclude directory entries and come from `7z l -slt`.

| Image | Bytes | ISO volume label | Files | Main content container |
| --- | ---: | --- | ---: | --- |
| `masocd-1.iso` | 351,090,688 | `MASOCD` | 5,828 | `MASOCD.MVB` — 259,490,690 bytes |
| `masocd-2.iso` | 197,738,496 | `MASOCD_2` | 1,956 | `DATA/MASO2.M12` — 125,394,639 bytes |
| `masocd-3.iso` | 327,081,984 | `MASO3` | 137 | `MASO3.M14` — 299,619,070 bytes; `LIST.M14` — 10,067 bytes |

SHA-256 of complete supplied images:

```text
dabd54e6a516ba9e3a2c348b8d1eebddd8bd45d8be3c81c84855102a269d9a17  masocd-1.iso
fc7b3047b2c6cc2555500faf43dc0b73ff877c2f5b01acdb32041615d2f31a0e  masocd-2.iso
7c269df8479c72919863f27b68dceb6fe8b567a18f27eb9481655e15e4ae17d0  masocd-3.iso
```

These hashes identify the current copies. They do not establish that the original
discs were error-free or that another backup exists.

## Format and coverage evidence

All four inspected `.MVB` / `.M12` / `.M14` containers begin with bytes
`3f 5f 03 00`. Their names, accompanying viewer libraries, and readable content
suggest related WinHelp/Multimedia Viewer container formats. Exact dialect and
decoder compatibility remain untested. HELPDECO documents MVB extraction and
internal-directory inspection for `.M??` files in its
[README](https://github.com/pmachapman/helpdeco/blob/master/README).

CD1 includes `MVIEWER2.EXE`, `MVAPI2.DLL`, `MVFS2.DLL`, and `SETUP.EXE`.
`TITLE.INF` contains Korean installation text that decodes readably with CP949.
The container has directly readable Korean index entries, including:

```text
88.02 유닉스란 무엇인가|8802065
88.03 우편번호 변환 프로그램|8803016
88.04 터보 파스칼 4.0|8804096
```

A byte-pattern scan for `|YYMMPPP`-like references found years 1988–1993.
The `SOURCE/PYYMMPPP` directories contain 321 distinct candidate identifiers,
from `8801112` through `9312446`. These observations suggest CD1 contains
1988–1993 material. They do not prove an absence of earlier material in compressed
or otherwise uninspected records, nor complete coverage of those six years.

CD2 includes `BIN/MASO2.EXE`, `BIN/MASO2.INI`, and viewer DLLs named `MV*12.DLL`.
Its `DATA/SOURCE/` identifiers and `DATA/LIST/` filenames indicate 1994 material.
The INI names Windows Notepad as a text editor. Article-body decoding has not
been attempted, and directory names alone do not establish full coverage.

CD3 has `MASO3.EXE`, viewer DLLs named `MV*14N.DLL`, and 105 `.CAB` files.
Its attachment directories span `FILES/9501` through `FILES/9512`.
`MASO3.CNT` decodes readably with CP949 and describes a 32-bit application.
Its main article container has not been decoded. The attachment dates suggest
1995 coverage, pending verification in the application or container records.

CD3 reports an ISO creation timestamp in 1994 while many executable and
attachment timestamps are in 1996. Preserve these values as observations;
do not treat filesystem timestamps as reliable magazine or CD publication dates.

## Reproduction and limitations

Inspection used 7-Zip 26.00 for listings and selective extraction into `/tmp`,
and Python for TOC counts, byte inspection, CP949 samples, and SHA-256 hashing.
Complete inventories should be generated into durable machine-readable manifests
in Milestone 1. Temporary inspection files are not project deliverables.

No application was executed, no full container was decompiled, no OCR or AI
summary was generated, and no image was published. Full scans, covers, text
completeness, accurate printed-page mappings, and 1983–1987 source availability
remain to be established. The owner confirmed that scans for 1983–1987 can be
arranged later; those 50 issues start with TOC metadata only. The CD
operating-system requirements are supplied by
the owner: Windows 3.1 for CD1, Windows 95 for CD2/CD3.
