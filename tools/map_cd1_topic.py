"""Reproduce the metadata-only raw topic map for CD1 reference 8802065.

Deliberately restricted to the checksummed pilot sources and their uncompressed
MVB layout. Not a general MVB/RTF reader; no body text is decoded or exported.
The native structures follow the pinned HELPDECO source cited in the map notes.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data/catalog/topic-maps/cd1-8802065.json"
SOURCES = {
    "masocd-1/MASOCD.MVB": "bde731b36c6a9e37ba0f23e4fce66758417753073cb537b7cc8d6dddfcd02565",
    "private/cd1-probe/raw/MASOCD.rtf": "01465d52667ab798df0dcf7993b6de764f45fd55e09eec1f80f77291303d957b",
}
# FILEHEADER offsets from the preserved internal-directory listing, pinned by
# the MVB checksum. Nine-byte FILEHEADER precedes each internal file payload.
CONTEXT = 0x0DDFFFD1 + 9
SYSTEM = 0x0C06C800 + 9
TOPIC = 0x0C0707F7 + 9
CONTEXT_FOOTNOTE = re.compile(rb'\{\\up #\}\{\\footnote\\pard\\plain\{\\up #\} ([^}]+)\}')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def context_hash(name):
    """WinHelp's modulo-2**32 hash, limited to this pilot's ASCII ID alphabet."""
    value = 0
    alphabet = "1234567890"
    for char in name.upper():
        if char in alphabet:
            code = alphabet.index(char) + 1
        elif "A" <= char <= "Z":
            code = ord(char) - 48
        elif char in "._":
            code = {".": 12, "_": 13}[char]
        else:
            raise ValueError(f"Unsupported context character: {char!r}")
        value = (value * 43 + code) & 0xFFFFFFFF
    return value


def context_entries(mvb):
    magic, _, page_size = struct.unpack_from("<3H", mvb, CONTEXT)
    root, _, total_pages, levels, count = struct.unpack_from("<4hI", mvb, CONTEXT + 26)
    require(magic == 0x293B and levels == 2, "Unexpected pilot context B-tree")
    pages = CONTEXT + 38
    page = struct.unpack_from("<h", mvb, pages + root * page_size + 4)[0]
    result, seen = {}, set()
    while page != -1:
        require(0 <= page < total_pages and page not in seen, "Invalid context leaf chain")
        seen.add(page)
        start = pages + page * page_size
        _, entries, _, next_page = struct.unpack_from("<4h", mvb, start)
        require(0 <= entries <= (page_size - 8) // 8, "Invalid context entry count")
        for index in range(entries):
            offset = start + 8 + index * 8
            hash_value, topic_offset = struct.unpack_from("<2I", mvb, offset)
            require(hash_value not in result, "Duplicate native context hash")
            result[hash_value] = {"hash_hex": f"0x{hash_value:08x}",
                                  "topic_offset": topic_offset,
                                  "mvb_entry_byte_offset": offset, "byte_length": 8}
        page = next_page
    require(len(result) == count == 2103, "Incomplete context table")
    return result


def topic_read(mvb, position, length):
    """Read across uncompressed 4096-byte blocks using 16384-wide TOPICPOS.

    HELPDECO uses this logical stride even when MVB SYSTEM.Flags is zero.
    Skip the 12-byte block headers; do not confuse TOPICPOS with file offsets.
    """
    output = bytearray()
    while length:
        block, offset = divmod(position - 12, 16384)
        size = min(length, 4084 - offset)
        require(block >= 0 and size > 0, "Invalid native topic position")
        physical = TOPIC + block * 4096 + 12 + offset
        chunk = mvb[physical:physical + size]
        require(len(chunk) == size, "Truncated topic data")
        output.extend(chunk)
        length -= size
        position = (block + 1) * 16384 + 12
    return bytes(output)


def native_topics(mvb, last_ordinal=152):
    require(struct.unpack_from("<3H", mvb, SYSTEM) == (0x036C, 27, 1)
            and struct.unpack_from("<H", mvb, SYSTEM + 10)[0] == 0,
            "Only the pilot's uncompressed MVB layout is supported")
    position, topic_offset = 12, 0
    result, seen = [], set()
    while len(result) < last_ordinal:
        require(position not in seen, "Cyclic topic links")
        seen.add(position)
        size, text_len, _, next_pos, data_len, kind = struct.unpack("<5iB", topic_read(mvb, position, 21))
        require(next_pos > 0 and 21 <= data_len <= size, "Invalid native topic link")
        # Read the record as a whole: arithmetic on TOPICPOS across a block
        # boundary would otherwise fail to skip its unused logical address gap.
        raw = topic_read(mvb, position, size)
        data = raw[21:data_len]
        if kind == 2:
            _, back, forward, number, _, _, next_header = struct.unpack_from("<7i", data)
            require(number == len(result), "Unexpected native topic numbering")
            block, offset = divmod(position - 12, 16384)
            result.append({"ordinal": number + 1, "topic_number": number,
                           "topic_pos": position, "topic_offset": topic_offset,
                           "mvb_header_byte_offset": TOPIC + block * 4096 + 12 + offset,
                           "next_topic_pos": next_header,
                           "browse_back_topic_offset": back,
                           "browse_forward_topic_offset": forward})
            if number + 1 in (149, 152):
                require(text_len <= size - data_len, "Compressed pilot title is unsupported")
                result[-1]["title"] = raw[data_len:data_len + text_len].split(b"\0")[0].decode("cp949")
        elif kind in (0x20, 0x23):
            index = 4 if data[0] & 1 else 2  # skip compressed signed long
            width = 2 if data[index] & 1 else 1
            topic_offset += int.from_bytes(data[index:index + width], "little") >> 1
        else:
            raise ValueError(f"Unsupported native record type {kind}")
        if (next_pos - 12) // 16384 != (position - 12) // 16384:
            topic_offset = ((next_pos - 12) // 16384) * 32768
        position = next_pos
    return result


def build_map():
    sources, content = [], []
    for path, expected in SOURCES.items():
        raw = (ROOT / path).read_bytes()
        actual = hashlib.sha256(raw).hexdigest()
        require(actual == expected, f"Changed pilot input: {path}")
        content.append(raw)
        sources.append({"path": path, "bytes": len(raw), "sha256": actual})
    mvb, rtf = content
    contexts = context_entries(mvb)
    native = native_topics(mvb)
    # In this pinned HELPDECO output, each literal page control starts a topic.
    # The native ordinal AND context hash below independently check alignment.
    pages = list(re.finditer(rb'(?<!\\)\\page\n', rtf))
    require(len(pages) == 3098, "Unexpected RTF topic count")
    topics = []
    roles = [(148, "linked_introduction", "3M4UMD"),
             (149, "reference_target_body", "2PES_R6"),
             (150, "following_untitled_separator", None),
             (151, "next_article_introduction", "3M4LHC"),
             (152, "next_article_body", "1KN6EK")]
    for ordinal, role, alias in roles:
        start, end = pages[ordinal - 2].end(), pages[ordinal - 1].start()
        raw = rtf[start:end]
        found = [m[1].decode("ascii") for m in CONTEXT_FOOTNOTE.finditer(raw)]
        require(found == ([alias] if alias else []), "RTF/native topic alignment failed")
        topic = {"role": role, "rtf_context_alias": alias, "native": native[ordinal - 1],
                 "rtf": {"byte_offset": start, "byte_length": end - start,
                         "end_exclusive": end, "sha256": hashlib.sha256(raw).hexdigest()}}
        if alias:
            entry = contexts[context_hash(alias)]
            require(entry["topic_offset"] == topic["native"]["topic_offset"], "Context points elsewhere")
            topic["context_entry"] = entry
        else:
            require(raw == b"\\pard \\b ", "Separator has unexpected content")
        if topics:
            require(topics[-1]["native"]["next_topic_pos"] == topic["native"]["topic_pos"],
                    "Nonadjacent native topics")
        topics.append(topic)
    require(context_hash("8802065") == context_hash("2PES_R6"), "Reference hash mismatch")
    require(topics[1]["native"]["title"] == "유닉스란 무엇인가?"
            and topics[4]["native"]["title"] == "스펠링 체커", "Pilot/neighbor title mismatch")
    body = topics[1]["rtf"]
    raw_body = rtf[body["byte_offset"]:body["end_exclusive"]]
    links = list(re.finditer(rb'\{\\v ([^}]+)\}', raw_body))
    require([m[1] for m in links] == [b"3M4UMD"], "Unexpected body link targets")
    marker = b"88.2.  65p"
    require(raw_body.count(marker) == 1, "Missing/ambiguous printed-page label")
    require(topics[1]["native"]["browse_forward_topic_offset"] == topics[4]["native"]["topic_offset"],
            "Browse-next target changed")
    return {"schema_version": 1, "cd_reference": "8802065", "toc_entry_id": "maso-1988-02-toc-0035",
            "scope": "raw_topic_mapping", "sources": sources,
            "offset_convention": "File byte offsets are zero-based; ends are exclusive. Native TOPICPOS and TOPICOFFSET are logical addresses, not file byte offsets.",
            "reference_hash_hex": f"0x{context_hash('8802065'):08x}", "topics": topics,
            "body_to_introduction_link": {"target_alias": "3M4UMD",
                "rtf_byte_offset": body["byte_offset"] + links[0].start(), "byte_length": len(links[0][0])},
            "body_page_label": {"label": marker.decode("ascii"),
                "rtf_byte_offset": body["byte_offset"] + raw_body.index(marker), "byte_length": len(marker)},
            "recovery_scope_ordinals": [148, 149],
            "excluded_following_ordinals": [150, 151, 152],
            "verification": {"native_context_resolved": True, "raw_boundaries_mapped": True,
                "body_decoded": False, "viewer_compared": False, "article_completeness_verified": False},
            "limitations": ["Introduction/body roles are inferred from the linked raw records; viewer confirmation is pending.",
                "The next browse target is another article, not evidence of continuation. No continuation link was identified in the body's hidden RTF targets.",
                "This bounded map does not rule out other material reachable through viewer macros/navigation or omitted by HELPDECO.",
                "The CD body's page label supports page 65 for this pilot only; it does not establish a collection-wide reference-to-page rule."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the reproducible metadata-only map")
    args = parser.parse_args()
    try:
        result = build_map()
        if args.write:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            require(json.loads(RECORD.read_text(encoding="utf-8")) == result, "Recorded topic map differs from source evidence")
        print("CD1 8802065: context, linked introduction, body, and following boundaries verified; viewer review pending.")
    except (OSError, ValueError, KeyError, IndexError, struct.error) as error:
        print(f"Topic mapping failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
