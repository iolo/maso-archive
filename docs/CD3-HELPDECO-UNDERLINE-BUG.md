# CD3 HELPDECO character-set / underline bug

Recorded 2026-09-26. **Diagnosis: decoder bug. Current mitigation: display-only
normalization. The decoder itself has not been corrected or reported upstream.**
This is a retained limitation of the completed restoration, not an active
extraction task.

## Symptom and source of the error

The owner reported widespread underlining in the CD3 reading room and confirmed
that the same text looks normal, without underlining, in the Windows viewer.
The generated RTF sets underline on 4,463,116 of 4,478,600 article characters
(99.65%), affecting all 968 candidates.

The problem begins in HELPDECO's interpretation of the M14 font records. It is
not introduced by React or the reading-room aggregator:

```text
M14 font character-set byte 0x81 (Hangul)
  → HELPDECO reads it as DoubleUnderline, tests it for nonzero
  → generated RTF contains \uldb
  → our RTF parser records underline: true
  → HTML / React render the text with <u>
```

The examined decoder is the unchanged source at revision
`b9c187a20d83a3e738d8fe073eb924a8b7264c5c` of
[joncampbell123/helpdeco](https://github.com/joncampbell123/helpdeco/tree/b9c187a20d83a3e738d8fe073eb924a8b7264c5c).
Its [`MVBFONT` structure](https://github.com/joncampbell123/helpdeco/blob/b9c187a20d83a3e738d8fe073eb924a8b7264c5c/helpdeco.h#L280)
names the byte after `StrikeOut` as `DoubleUnderline`.
[`FontLoad`](https://github.com/joncampbell123/helpdeco/blob/b9c187a20d83a3e738d8fe073eb924a8b7264c5c/helpdeco.c#L2153)
converts any nonzero value to a true double-underline flag, and
[`ChangeFont`](https://github.com/joncampbell123/helpdeco/blob/b9c187a20d83a3e738d8fe073eb924a8b7264c5c/helpdeco.c#L3089)
emits `\uldb`.

In the Windows [LOGFONT layout](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-logfonta),
the corresponding byte after italic, underline and strikeout is `lfCharSet`.
Microsoft identifies [129 (`0x81`) as HANGUL/HANGEUL_CHARSET and 2 as SYMBOL_CHARSET](https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.inputlanguagechangedeventargs.charset).
The CD3 bytes match these character sets and their font names, including Korean
fonts with the genuine underline byte set to zero. Together with the decoder
code and the owner's Windows observation, this identifies the misinterpreted
field as the source of the blanket underlining. We did not reverse-engineer the
Windows viewer or compare all styling with printed magazines.

## Byte-level evidence

The `|FONT` stream extracted from the unchanged `masocd-3/MASO3.M14` has:

- Length: 5,292 bytes.
- SHA-256: `9335dacc3a7fde79b14c3cd89f2879bc7532a4e69788ff181a1e9db65d880bbc`.
- Header (`<8H`): `(70, 64, 40, 2280, 2, 4968, 1, 5260)`.
- 70 face names, 64 descriptors, 42 bytes per descriptor, descriptors at byte 2280.

Offsets below are relative to each descriptor:

| Offset | Actual role in the font layout | Observed values across 64 records |
| --- | --- | --- |
| 32 | Italic | 60 zero, 4 one |
| 33 | Underline | 53 zero, 11 one |
| 34 | Strikeout | 64 zero |
| 35 | Character set, misnamed `DoubleUnderline` by HELPDECO | 53 `0x81`, 7 `0x00`, 4 `0x02` |

Descriptor 1, face `돋움,0`, has height -10 and bytes 32–39
`00 00 00 81 00 00 00 30`. Its actual underline flag is off; HELPDECO enables
double underline from the Hangul byte. The symbol-font value `0x02` is also
nonzero and follows the same erroneous path. Do not interpret either value as
an editorial request to underline text.

To reproduce the inspection with the pinned binary, from the repository root:

```sh
mkdir -p private/cd3-font-audit
/path/to/helpdeco ./masocd-3/MASO3.M14 '|FONT' private/cd3-font-audit/FONT.bin
python3 - <<'PY'
from collections import Counter
from pathlib import Path
import hashlib
import struct

raw = Path('private/cd3-font-audit/FONT.bin').read_bytes()
header = struct.unpack_from('<8H', raw)
_, count, _, start, _, end, _, _ = header
stride = (end - start) // count
print(len(raw), hashlib.sha256(raw).hexdigest(), header, stride)
for offset in (32, 33, 34, 35):
    print(offset, Counter(raw[start + i * stride + offset] for i in range(count)))
PY
```

The extracted stream and source bodies stay private; this record contains only
format evidence, counts and hashes. See [the source map](CD3-SOURCE-MAP.md) for
the ISO hash and decoder preparation.

## Current workaround and limits

[`tools/cd3_display.py`](../tools/cd3_display.py) suppresses the CD3 underline flag
when rendering the standalone article/supplement HTML and when projecting
reading-room runs. It does not modify the ISO, M14, generated RTF, parsed source
blocks, literal text, code whitespace, attachments or other emphasis. Six focused
adapter tests pass, and browser checks show normal text with bold retained.
All 8,971 non-page/non-manifest reference file hashes stayed unchanged during the
display rebuild; the combined export retains its coverage counts.

The generated RTF and its parsed flags are **decoder output**, not authoritative
original typography. Earlier descriptions of these flags as "original formatting
evidence" were too strong. They remain useful evidence of what this decoder
produced, with this known defect attached.

The current workaround suppresses all CD3 underline marks, including any genuine
ones. The parser currently collapses `\ul` and `\uldb` into one boolean, so the
workaround cannot distinguish genuine underlining or viewer-link styling from
the bogus character-set interpretation. CD1/CD2 display handling is unchanged;
the shared decoder's applicability to their font variants has not been audited
as part of this diagnosis.

## Deferred correction

A future decoder correction should read character-set and underline fields
separately, preserve hyperlink control behavior and genuine emphasis, and check
the other font fields against the relevant MVB variants. Validate it against
the raw font records and the Windows viewer before replacing the pinned probe.
Version the corrected decoder/probe evidence, compare text/code/media outcomes,
regenerate dependent records and references, and remove the blanket suppression
once corrected formatting reaches the reader. No such correction, probe migration,
upstream report or new extraction campaign is part of this implementation wrap-up.
