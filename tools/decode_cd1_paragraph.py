"""Decode only the pinned first body paragraph of CD1 reference 8802065.

Run from the repository root with python3 -m tools.decode_cd1_paragraph.
This intentionally rejects RTF features outside the selected sample's subset.
"""

import argparse
import hashlib
import json
import re
import sys

from tools.map_cd1_topic import ROOT, SOURCES, require

RECORD = ROOT / "data/catalog/paragraph-samples/cd1-8802065.json"
OUTPUT = ROOT / "build/cd1-paragraph/8802065"
RTF = "private/cd1-probe/raw/MASOCD.rtf"
MAP = "data/catalog/topic-maps/cd1-8802065.json"
MAP_SHA256 = "20a88a591b59a862aea5c9a6e613773a1e04ac5eb7a19b32e7490df74a0b0ea2"
START, END = 378665, 379785
SAMPLE_SHA256 = "322b6a9cb5da8354a1dd5858b38ee006bbd770a87ecbc73df9cbd2a1f0e2d9e2"
PREFIX = rb"\pard\sl285\li395\ri395 \plain\fs18 "
TERMINATOR = rb"\par "


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def decode_sample(raw):
    """Return strict CP949 text and unescaped bytes, without guessing controls.

    The exact prologue resets character state; no inherited font is needed.
    All remaining backslashes must be byte escapes or escaped literal syntax.
    Decode after tokenization so an escaped byte cannot become an RTF command.
    """
    require(raw.startswith(PREFIX) and raw.endswith(TERMINATOR),
            "Expected the sample's formatting reset and one paragraph terminator")
    payload = raw[len(PREFIX):-len(TERMINATOR)]
    output = bytearray()
    index = 0
    while index < len(payload):
        byte = payload[index]
        if byte == 92:
            token = re.match(rb"\\'([0-9a-fA-F]{2})", payload[index:])
            if token:
                output.append(int(token[1], 16))
                index += 4
                continue
            if payload[index:index + 2] in (rb"\\", rb"\{", rb"\}"):
                output.append(payload[index + 1])
                index += 2
                continue
            raise ValueError(f"Unsupported/malformed RTF control at sample byte {len(PREFIX) + index}")
        require(byte not in (123, 125), "RTF groups/destinations are unsupported in this sample")
        if byte not in (10, 13):  # Physical RTF line endings are not paragraph breaks.
            require(32 <= byte <= 126, "Unescaped non-ASCII/control byte is unsupported")
            output.append(byte)
        index += 1
    encoded = bytes(output)
    text = encoded.decode("cp949", errors="strict")
    require(text and "\ufffd" not in text and all(ord(c) >= 32 for c in text),
            "Empty text, replacement character, or embedded control in sample")
    require(text.encode("cp949", errors="strict") == encoded, "CP949 round-trip mismatch")
    return text, encoded


def build_sample():
    rtf = (ROOT / RTF).read_bytes()
    require(digest(rtf) == SOURCES[RTF], "Changed raw RTF snapshot")
    map_bytes = (ROOT / MAP).read_bytes()
    require(digest(map_bytes) == MAP_SHA256, "Changed topic map; review sample boundaries")
    topic_map = json.loads(map_bytes)
    body = next(t for t in topic_map["topics"] if t["role"] == "reference_target_body")
    require(body["rtf"]["byte_offset"] <= START < END <= body["rtf"]["end_exclusive"],
            "Sample falls outside the mapped body")
    require(rtf[START - 5:START] == TERMINATOR, "Sample does not begin at a paragraph boundary")
    require(rtf[11:17] == rb"\deff4" and rtf[115:134] == rb"{\f4\fswiss Arial;}",
            "Unexpected default font declaration")
    font_table_end = rtf.index(b"\n{\\colortbl")
    header = rtf[:font_table_end]
    require(not re.search(rb"\\(?:ansicpg|fcharset|cpg)\d+", header),
            "Explicit encoding declaration now requires review")
    raw = rtf[START:END]
    require(digest(raw) == SAMPLE_SHA256, "Changed paragraph bytes")
    text, encoded = decode_sample(raw)
    require(encoded.decode("euc_kr", errors="strict") == text, "EUC-KR/CP949 disagreement")
    # Plain text keeps punctuation and spacing; one LF represents the final \par.
    utf8 = (text + "\n").encode("utf-8")
    artifacts = {"paragraph.raw.rtf": raw, "paragraph.cp949": encoded, "paragraph.txt": utf8}
    record = {
        "schema_version": 1, "cd_reference": "8802065", "toc_entry_id": "maso-1988-02-toc-0035",
        "scope": "one_body_paragraph", "selection": "First prose paragraph under section I",
        "source": {"path": RTF, "sha256": digest(rtf)},
        "topic_map": {"path": MAP, "sha256": digest(map_bytes), "body_ordinal": 149},
        "raw_span": {"byte_offset": START, "end_exclusive": END, "byte_length": END - START,
                     "sha256": digest(raw), "includes_terminal_par": True},
        "font": {"default_id": 4, "name": "Arial", "default_declaration_span": [11, 17],
                 "font_entry_span": [115, 134], "reset_control": "plain", "font_changes_in_sample": 0,
                 "font_size_half_points": 18, "explicit_code_page_or_charset": None},
        "encoding": {"codec": "cp949", "errors": "strict", "round_trip_equal": True,
                     "euc_kr_text_equal": True,
                     "decision": "Source-specific Korean byte interpretation, not inferred from Arial or the ansi keyword; viewer glyph comparison pending."},
        "text": {"characters_excluding_terminal_lf": len(text), "cp949_bytes": len(encoded),
                 "hangul_syllables": sum("\uac00" <= c <= "\ud7a3" for c in text),
                 "ascii_characters": sum(ord(c) < 128 for c in text), "replacement_characters": 0,
                 "punctuation": sorted(set(c for c in text if c.isascii() and not c.isalnum() and c != " ")),
                 "normalization": "None; control delimiters and physical CR/LF removed, terminal par represented by one LF."},
        "outputs": {name: {"bytes": len(data), "sha256": digest(data)} for name, data in artifacts.items()},
        "unsupported": ["Nested groups, hidden text, footnotes, fields and destinations",
                        "Font changes and symbol-font glyph mapping",
                        "Unicode escapes, special-character control words/symbols other than escaped braces/backslash",
                        "Tables, images, embedded objects, tabs and explicit line-break controls",
                        "Other paragraph prologues and unescaped non-ASCII input"],
        "verification": {"strict_decode_passed": True, "viewer_compared": False,
                         "article_completeness_verified": False},
    }
    return record, artifacts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true", help="write reviewed metadata as well as private outputs")
    args = parser.parse_args()
    try:
        record, artifacts = build_sample()
        metadata = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        if args.write_record:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_bytes(metadata)
        else:
            require(json.loads(RECORD.read_bytes()) == record, "Paragraph evidence differs from reviewed record")
        OUTPUT.mkdir(parents=True, exist_ok=True)
        for name, raw in {**artifacts, "provenance.json": metadata}.items():
            temporary = OUTPUT / (name + ".tmp")
            temporary.write_bytes(raw)
            temporary.replace(OUTPUT / name)
        print(f"Decoded one paragraph ({record['text']['characters_excluding_terminal_lf']} characters); outputs: {OUTPUT.relative_to(ROOT)}; viewer comparison pending.")
    except (OSError, ValueError, KeyError, StopIteration) as error:
        print(f"Paragraph decoding failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
