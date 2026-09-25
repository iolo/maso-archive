# CD2 source map and article probe

The supplied `masocd-2.iso` is 197,738,496 bytes and has SHA-256
`fc7b3047b2c6cc2555500faf43dc0b73ff877c2f5b01acdb32041615d2f31a0e`.
`python3 -m tools.inventory_cd2_sources` checks that identity, fresh ISO
extraction against the supplied tree, and the private decoder output against the
reviewed metadata record. The full path, size, and hash inventory is generated
at `build/cd2-preservation/inventory.json`; it is excluded from Git. The tracked
summary is `data/catalog/preservation/cd2-inventory.json`.

The ISO has 1,956 files and 102 directories. `DATA/MASO2.M12` is the article
book; `DATA/LIST/` has 88 CP949 text files containing code listings rather than
article indexes; `DATA/SOURCE/` has 97 attachment directories. These are
different from the M12's internal `book.lst`, `info.lst`, and `qnatip.lst`
indexes. The `SOURCE` and `LIST` file names are candidates for relationships,
not articles by themselves. `BIN/MASO2.EXE` is the disc viewer entry point. The
owner reports that setup only creates a shortcut and needs no Windows 95
installation for this extraction.

The pinned CD1 decoder, `joncampbell123/helpdeco` revision
`b9c187a20d83a3e738d8fe073eb924a8b7264c5c`, accepts CD2's M12. Build it
with `make helpdeco CFLAGS='-g3 -O0 -Wno-error=incompatible-pointer-types'`.
From an empty `private/cd2-probe/raw` directory, run the executable with
`../../../masocd-2/DATA/MASO2.M12 /g`; the input must be relative because the
decoder treats a leading slash as an option. The successful probe emitted 1 RTF,
3 internal indexes, 2,163 DIBs, 114 WMFs, 58 BMPs, and 15 other files. The RTF
contains 1,388 page-delimited topics. These are decoder topics, not necessarily
1,388 articles. CD1's container decoder works; its strict font and content
policies have not been assumed for CD2.

`book.lst` line 467 is `한글 TeX을 이용하려면^940116300`. The matching RTF topic has
the same title in its native footnote, context `3H9UTZ3`, page label `94.1 / 163p`,
and action `!SrcCopy(9401163)`. Its bytes occupy offset 406,653 through 483,901
exclusive in `MASO2.rtf`, between adjacent `\page` markers; their SHA-256 is
`c3b7063c28755b3e047e75a835f15b334f5e12f7c8ac3b2c9ff54d28346172e6`.
The corresponding attachment directory has `TEX.ZIP`. The RTF contains 22
ordered image markers, and every named resource exists in the private decoder
output. This is a source-bound text/code/image probe, with article boundaries
still subject to paper review. The issue label comes from the CD body itself;
there is no independent 1994 library TOC match.

Next: decode this one topic's text and ordered blocks, preserve the ZIP and image
sources, and make a local portable reference. Validate its text, code whitespace,
media links, and repeatability before mapping an issue or running bulk extraction.
