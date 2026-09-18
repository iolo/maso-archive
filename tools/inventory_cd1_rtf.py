"""Inventory the pilot's two mapped RTF topics without decoding their text.

Run python3 -m tools.inventory_cd1_rtf. Full token locations stay under build/;
only the compact metadata summary is tracked. This is not a general RTF reader.
"""

import argparse
from collections import Counter, defaultdict
import json
import re
import sys

from tools.decode_cd1_paragraph import MAP, MAP_SHA256, RTF, digest
from tools.map_cd1_topic import ROOT, SOURCES, require

OUTPUT = ROOT / "build/cd1-rtf-inventory/8802065"
RECORD = ROOT / "data/catalog/rtf-inventories/cd1-8802065.json"
KNOWN = set("b f fs footnote keepn li par pard plain qr ri sa sb sl ul up v".split())
WORD = re.compile(rb"\\([a-zA-Z]+)(-?\d+)? ?")


def tokenize(raw, base=0):
    """Cover every byte, retaining unknown controls and opaque binary payloads."""
    tokens = []
    i = 0
    while i < len(raw):
        start = i
        extra = {}
        if raw[i] in (123, 125):
            kind = "group_open" if raw[i] == 123 else "group_close"
            i += 1
        elif raw[i] == 92:
            require(i + 1 < len(raw), f"Truncated escape at {base + i}")
            if raw[i + 1] == 39:
                require(re.fullmatch(rb"[0-9a-fA-F]{2}", raw[i + 2:i + 4]) is not None,
                        f"Malformed hex escape at {base + i}")
                kind, i = "hex_byte", i + 4
            else:
                match = WORD.match(raw, i)
                if match:
                    kind, i = "control_word", match.end()
                    extra = {"word": match[1].decode("ascii"),
                             "parameter": int(match[2]) if match[2] else None}
                else:
                    kind, i = "control_symbol", i + 2
                    extra = {"symbol": chr(raw[start + 1])}
        elif raw[i] in (10, 13):
            kind = "physical_newline"
            while i < len(raw) and raw[i] in (10, 13):
                i += 1
        else:
            kind = "text_bytes"
            while i < len(raw) and raw[i] not in (10, 13, 92, 123, 125):
                i += 1
        tokens.append({"kind": kind, "byte_offset": base + start, "byte_length": i - start, **extra})
        if extra.get("word") == "bin":
            size = extra["parameter"]
            require(size is not None and 0 <= size <= len(raw) - i,
                    f"Invalid binary length at {base + start}")
            if size:
                tokens.append({"kind": "binary_bytes", "byte_offset": base + i, "byte_length": size})
            i += size
    require(sum(t["byte_length"] for t in tokens) == len(raw), "Incomplete token coverage")
    return tokens


def group_records(raw, tokens, base):
    stack, groups = [], []
    for token in tokens:
        if token["kind"] == "group_open":
            group = {"byte_offset": token["byte_offset"], "depth": len(stack) + 1,
                     "parent_byte_offset": stack[-1]["byte_offset"] if stack else None}
            stack.append(group)
            groups.append(group)
        elif token["kind"] == "group_close":
            require(stack, f"Unmatched closing brace at {token['byte_offset']}")
            group = stack.pop()
            end = token["byte_offset"] + 1
            group["byte_length"] = end - group["byte_offset"]
            fragment = raw[group["byte_offset"] - base:end - base]
            marker = re.fullmatch(rb"\{\\up ([+#$K])\}", fragment)
            footnote = re.match(rb"\{\\footnote\\pard\\plain\{\\up ([+#$K])\}", fragment)
            if marker:
                group.update(role="metadata_marker", marker=marker[1].decode())
            elif footnote:
                group.update(role="metadata_footnote", marker=footnote[1].decode())
            elif re.fullmatch(rb"\{\\v [A-Z0-9_.]+\}", fragment):
                group.update(role="hidden_context_link")
            else:
                group.update(role="unclassified")
    require(not stack, "Unclosed RTF group")
    return groups


def object_records(raw, tokens, base):
    """Identify literal HELPDECO object commands, not RTF destination groups."""
    objects = []
    for index, token in enumerate(tokens[:-2]):
        if token.get("symbol") != "{":
            continue
        middle, closing = tokens[index + 1:index + 3]
        if middle["kind"] != "text_bytes" or closing.get("symbol") != "}":
            continue
        a = middle["byte_offset"] - base
        value = raw[a:a + middle["byte_length"]]
        match = re.fullmatch(rb"bmc ([A-Za-z0-9_.]+)|ewl mvbmp2, ViewerBmp2, +!([A-Za-z0-9_.]+)", value)
        if match:
            objects.append({"byte_offset": token["byte_offset"],
                            "byte_length": closing["byte_offset"] + closing["byte_length"] - token["byte_offset"],
                            "command": "bmc" if match[1] else "ewl",
                            "resource": (match[1] or match[2]).decode("ascii")})
    return objects


def inspect_topic(raw, base, initial_font=None):
    tokens = tokenize(raw, base)
    groups = group_records(raw, tokens, base)
    objects = object_records(raw, tokens, base)
    group_by_start = {g["byte_offset"]: g for g in groups}
    words, fonts = defaultdict(list), defaultdict(list)
    state = {"font": initial_font, "category": "visible"}
    stack, issues, guards = [], [], []
    for index, token in enumerate(tokens):
        kind = token["kind"]
        if kind == "group_open":
            stack.append(state.copy())
            state["category"] = group_by_start[token["byte_offset"]]["role"]
        elif kind == "group_close":
            state = stack.pop()
        elif kind == "control_word":
            word, parameter = token["word"], token["parameter"]
            words[word].append({"byte_offset": token["byte_offset"], "parameter": parameter})
            if word == "plain":
                state["font"] = 4  # pinned document default; scoped by groups
            elif word == "f":
                require(parameter is not None and parameter >= 0, "Invalid font selector")
                state["font"] = parameter
            if word not in KNOWN:
                issues.append({"byte_offset": token["byte_offset"], "reason": "unclassified_control", "word": word})
        token["font_id"] = state["font"]
        token["category"] = state["category"]
        if any(o["byte_offset"] <= token["byte_offset"] < o["byte_offset"] + o["byte_length"] for o in objects):
            token["category"] = "object_marker"
        if kind in ("text_bytes", "hex_byte", "control_symbol"):
            if token["category"] == "visible":
                fonts[str(state["font"])].append(token["byte_offset"])
                if state["font"] is None and kind != "physical_newline":
                    # Whitespace alone before the first font selector is harmless.
                    a = token["byte_offset"] - base
                    if raw[a:a + token["byte_length"]].strip():
                        issues.append({"byte_offset": token["byte_offset"], "reason": "inherited_font_unknown"})
        if kind == "control_symbol" and token["symbol"] not in "\\{}":
            previous = tokens[index - 1] if index else {}
            if (token["symbol"] == "-" and previous.get("symbol") == "{"
                    and previous["byte_offset"] + previous["byte_length"] == token["byte_offset"]):
                guards.append({"byte_offset": token["byte_offset"], "byte_length": token["byte_length"],
                               "role": "helpdeco_literal_brace_guard"})
            else:
                issues.append({"byte_offset": token["byte_offset"], "reason": "unsupported_control_symbol"})
    for group in groups:
        if group["role"] == "unclassified":
            issues.append({"byte_offset": group["byte_offset"], "reason": "unclassified_group"})
    return {"byte_offset": base, "byte_length": len(raw), "sha256": digest(raw),
            "accounted_bytes": sum(t["byte_length"] for t in tokens),
            "token_counts": dict(sorted(Counter(t["kind"] for t in tokens).items())),
            "controls": dict(sorted(words.items())), "groups": groups, "objects": objects,
            "visible_font_token_offsets": dict(sorted(fonts.items())),
            "initial_font_id": initial_font, "final_font_id": state["font"],
            "literal_brace_guards": guards, "issues": issues, "tokens": tokens}


def build_inventory():
    rtf = (ROOT / RTF).read_bytes()
    require(digest(rtf) == SOURCES[RTF], "Changed RTF snapshot")
    map_bytes = (ROOT / MAP).read_bytes()
    require(digest(map_bytes) == MAP_SHA256, "Changed topic map")
    topic_map = json.loads(map_bytes)
    reports, initial_font = [], None
    for topic in topic_map["topics"][:2]:
        span = topic["rtf"]
        raw = rtf[span["byte_offset"]:span["end_exclusive"]]
        require(digest(raw) == span["sha256"], "Topic slice mismatch")
        report = inspect_topic(raw, span["byte_offset"], initial_font)
        report.update(ordinal=topic["native"]["ordinal"], role=topic["role"])
        initial_font = report["final_font_id"]
        reports.append(report)
    used = {int(font) for r in reports for font in r["visible_font_token_offsets"] if font != "None"}
    used.update(e["parameter"] for r in reports for e in r["controls"].get("f", []))
    header_end = rtf.index(b"\n{\\colortbl")
    font_definitions = []
    for number in sorted(used):
        match = re.search(rb"\{\\f" + str(number).encode() + rb"\\[a-z]+ ([^{};]+);\}", rtf[:header_end])
        require(match is not None, f"Missing font definition {number}")
        font_definitions.append({"font_id": number, "name": match[1].decode("cp949", errors="strict"),
                                 "byte_offset": match.start(), "byte_length": len(match[0])})
    summaries = []
    for report in reports:
        summary = {k: report[k] for k in ("ordinal", "role", "byte_offset", "byte_length", "sha256",
                                         "accounted_bytes", "token_counts", "initial_font_id", "final_font_id", "issues")}
        summary["controls"] = {word: {"count": len(entries), "first_byte_offset": entries[0]["byte_offset"],
                                      "parameters": sorted({e["parameter"] for e in entries}, key=lambda p: (p is not None, p or 0))}
                               for word, entries in report["controls"].items()}
        summary["group_roles"] = dict(sorted(Counter(g["role"] for g in report["groups"]).items()))
        summary["metadata_markers"] = dict(sorted(Counter(g["marker"] for g in report["groups"] if g["role"] == "metadata_footnote").items()))
        summary["visible_fonts"] = {font: {"token_count": len(offsets), "first_byte_offset": offsets[0]}
                                    for font, offsets in report["visible_font_token_offsets"].items()}
        summary["objects"] = report["objects"]
        summary["literal_brace_guards"] = report["literal_brace_guards"]
        summaries.append(summary)
    record = {"schema_version": 1, "cd_reference": "8802065", "scope": "rtf_feature_inventory",
              "source": {"path": RTF, "sha256": digest(rtf)},
              "topic_map": {"path": MAP, "sha256": digest(map_bytes)},
              "font_definitions": font_definitions,
              "explicit_encoding_declarations": [m.decode("ascii") for m in re.findall(rb"\\(?:ansicpg|fcharset|cpg)\d+", rtf[:header_end])],
              "topics": summaries,
              "limitations": ["Lexical coverage is not decoded text or verified completeness.",
                              "CP949 remains a source-specific decoding choice; symbol/glyph fidelity awaits viewer review.",
                              "Object markers are located only; resources are not converted or checked here.",
                              "No table controls were observed; tables or code may still be represented by images or formatted text."],
              "verification": {"full_text_decoded": False, "viewer_compared": False}}
    return record, reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    try:
        record, reports = build_inventory()
        metadata = json.dumps(record, ensure_ascii=False, indent=2) + "\n"
        if args.write_record:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_text(metadata, encoding="utf-8")
        else:
            require(json.loads(RECORD.read_bytes()) == record, "Inventory differs from reviewed metadata")
        OUTPUT.mkdir(parents=True, exist_ok=True)
        for name, data in [("summary.json", metadata), ("inventory.json", json.dumps(reports, ensure_ascii=False, indent=2) + "\n")]:
            temporary = OUTPUT / (name + ".tmp")
            temporary.write_text(data, encoding="utf-8")
            temporary.replace(OUTPUT / name)
        print(f"Inventoried {sum(r['accounted_bytes'] for r in reports)} bytes in two topics; "
              f"{sum(len(r['objects']) for r in reports)} object markers; "
              f"{sum(len(r['issues']) for r in reports)} review issues. Outputs: {OUTPUT.relative_to(ROOT)}")
    except (OSError, ValueError, KeyError) as error:
        print(f"Inventory failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
