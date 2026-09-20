"""Recover the mapped CD1 pilot's full available text into private build output.

Run python3 -m tools.recover_cd1_text. The reusable decoder supports the reviewed
CD1 RTF subset. Unknown/undecodable content stays explicitly flagged with source spans.
"""

import argparse
from collections import Counter
from copy import deepcopy
import json
import sys

from tools import inventory_cd1_rtf as inventory
from tools import decode_cd1_paragraph as sample
from tools.map_cd1_topic import ROOT, require

OUTPUT = ROOT / "build/cd1-text/8802065"
RECORD = ROOT / "data/catalog/text-recoveries/cd1-8802065.json"


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def reset_character():
    # None means no explicit size since the reset, not a guessed rendering size.
    return {"font_id": 4, "fs": None, "b": False, "ul": False}


def recover_topic(rtf, report, initial_state=None, font_codecs=None):
    """Interpret visible tokens; retain metadata and account for every byte."""
    # Callers must establish additional font/encoding mappings from source evidence.
    font_codecs = {4: "cp949", 5: "cp949", 6: "cp949"} if font_codecs is None else dict(font_codecs)
    require(all(codec in ("ascii", "cp949") for codec in font_codecs.values()), "Unsupported decoding policy")
    state = deepcopy(initial_state) if initial_state else {"character": reset_character(), "paragraph": {}}
    if initial_state is None:
        state["character"]["font_id"] = report["initial_font_id"]
    tokens = report["tokens"]
    groups = {g["byte_offset"]: g for g in report["groups"] if g["parent_byte_offset"] is None}
    objects = {o["byte_offset"]: o for o in report["objects"]}
    guards = {g["byte_offset"] for g in report["literal_brace_guards"]}
    paragraphs, metadata, ledger, issues, transformations = [], [], [], [], []
    runs, buffer, spans = [], bytearray(), []
    paragraph_start = report["byte_offset"]

    def add_bytes(data, token):
        buffer.extend(data)
        start, length = token["byte_offset"], token["byte_length"]
        if spans and spans[-1]["byte_offset"] + spans[-1]["byte_length"] == start:
            spans[-1]["byte_length"] += length
        else:
            spans.append({"byte_offset": start, "byte_length": length})

    def flush():
        if not buffer:
            return
        encoded = bytes(buffer)
        font = state["character"]["font_id"]
        run = {"kind": "text", "format": state["character"].copy(),
               "source_spans": deepcopy(spans), "encoded_bytes": len(encoded),
               "encoded_sha256": sample.digest(encoded), "encoding": "cp949"}
        try:
            require(font in font_codecs, f"Unsupported font {font}")
            codec = font_codecs[font]
            run["encoding"] = codec
            text = encoded.decode(codec, errors="strict")
            require("\ufffd" not in text and all(c == "\t" or ord(c) >= 32 for c in text),
                    "Replacement/embedded control character")
            require(text.encode(codec, errors="strict") == encoded, "Byte round-trip mismatch")
            run["text"] = text
        except (ValueError, UnicodeError) as error:
            run.update(kind="unsupported", text=f"[unsupported text at byte {spans[0]['byte_offset']}]",
                       reason=str(error), original_bytes_hex=encoded.hex())
            issues.append({"source_spans": deepcopy(spans), "reason": str(error)})
        runs.append(run)
        buffer.clear()
        spans.clear()

    def account(token, category):
        ledger.append({"byte_offset": token["byte_offset"], "byte_length": token["byte_length"],
                       "token_kind": token["kind"], "disposition": category})

    index = 0
    while index < len(tokens):
        token = tokens[index]
        start, length = token["byte_offset"], token["byte_length"]
        kind = token["kind"]
        if start in groups or start in objects:
            flush()
            item = groups.get(start) or objects[start]
            end = start + item["byte_length"]
            if start in groups:
                require(item["role"] in ("metadata_marker", "metadata_footnote", "hidden_context_link"),
                        "Unreviewed group in pilot")
                category = "metadata"
                metadata.append({**item, "raw_rtf": rtf[start:end].decode("ascii")})
            else:
                category = "object_reference"
                runs.append({"kind": "object", "text": f"[object:{item['resource']}]",
                             "format": state["character"].copy(), "object": item,
                             "source_spans": [{"byte_offset": start, "byte_length": item["byte_length"]}]})
            while index < len(tokens) and tokens[index]["byte_offset"] < end:
                account(tokens[index], category)
                index += 1
            require(ledger[-1]["byte_offset"] + ledger[-1]["byte_length"] == end, "Group/object cuts a token")
            continue
        if start in guards:
            account(token, "decompiler_guard")
            transformations.append({"byte_offset": start, "byte_length": length,
                                    "action": "omit_helpdeco_literal_brace_guard"})
        elif kind == "physical_newline":
            account(token, "rtf_layout")
        elif kind in ("text_bytes", "hex_byte", "control_symbol"):
            raw = rtf[start:start + length]
            if kind == "hex_byte":
                data = bytes([int(raw[2:4], 16)])
            elif kind == "control_symbol":
                require(token["symbol"] in "\\{}", "Unsupported visible control symbol")
                data = token["symbol"].encode("ascii")
            else:
                data = raw
            add_bytes(data, token)
            account(token, "text")
        elif kind == "control_word":
            flush()
            word, value = token["word"], token["parameter"]
            if word == "tab":
                require(value is None, "Unexpected tab parameter")
                # Keep the character, not a guessed tab width; spans still point
                # to the original control token and the ledger records its use.
                add_bytes(b"\t", token)
                account(token, "text_control")
                transformations.append({"byte_offset": start, "byte_length": length,
                                        "action": "emit_rtf_tab_character"})
            elif word == "par":
                paragraphs.append({"ordinal": len(paragraphs) + 1,
                                   "source_span": {"byte_offset": paragraph_start, "end_exclusive": start + length},
                                   "format": state["paragraph"].copy(), "runs": runs,
                                   "text": "".join(r["text"] for r in runs), "terminated_by_par": True})
                runs = []
                paragraph_start = start + length
                account(token, "paragraph_boundary")
            else:
                if word == "plain":
                    state["character"] = reset_character()
                elif word == "pard":
                    state["paragraph"] = {}
                elif word in ("f", "fs"):
                    require(value is not None, "Missing font/size parameter")
                    state["character"]["font_id" if word == "f" else "fs"] = value
                elif word in ("b", "ul"):
                    state["character"][word] = value != 0
                    if word == "ul" and "underline_style" in state["character"]:
                        state["character"]["underline_style"] = "single" if value != 0 else "none"
                elif word == "uldb":
                    state["character"]["ul"] = value != 0
                    state["character"]["underline_style"] = "double" if value != 0 else "none"
                elif word == "tx":
                    require(value is not None, "Missing tab stop parameter")
                    state["paragraph"].setdefault("tab_stops", []).append(value)
                elif word in ("sl", "li", "ri", "sa", "sb", "fi"):
                    require(value is not None, "Missing paragraph format parameter")
                    state["paragraph"][word] = value
                elif word in ("qr", "keepn"):
                    state["paragraph"][word] = value != 0
                else:
                    raise ValueError(f"Unsupported visible control {word} at byte {start}")
                account(token, "formatting")
        else:
            raise ValueError(f"Unsupported token {kind} at byte {start}")
        index += 1
    flush()
    end = report["byte_offset"] + report["byte_length"]
    if runs:
        paragraphs.append({"ordinal": len(paragraphs) + 1,
                           "source_span": {"byte_offset": paragraph_start, "end_exclusive": end},
                           "format": state["paragraph"].copy(), "runs": runs,
                           "text": "".join(r["text"] for r in runs), "terminated_by_par": False})
        paragraph_start = end
    cursor = report["byte_offset"]
    for entry in ledger:
        require(entry["byte_offset"] == cursor, "Gap/overlap in byte accounting")
        cursor += entry["byte_length"]
    require(cursor == end and len(ledger) == len(tokens), "Incomplete byte/token accounting")
    return {"ordinal": report.get("ordinal"), "role": report.get("role"),
            "source_span": {"byte_offset": report["byte_offset"], "end_exclusive": end},
            "paragraphs": paragraphs, "metadata": metadata, "accounting": ledger,
            "transformations": transformations, "issues": issues, "final_state": state,
            "trailing_layout_span": {"byte_offset": paragraph_start, "end_exclusive": end}}


def topic_text(topic):
    return "".join(p["text"] + ("\n" if p["terminated_by_par"] else "") for p in topic["paragraphs"])


def build_recovery():
    summary, reports = inventory.build_inventory()
    require(summary == json.loads(inventory.RECORD.read_bytes()), "Inventory changed; review before recovery")
    require(not any(r["issues"] for r in reports), "Inventory has unresolved constructs")
    rtf = (ROOT / sample.RTF).read_bytes()
    require(sample.digest(rtf) == summary["source"]["sha256"], "Source changed after inventory")
    topics, state = [], None
    for report in reports:
        topic = recover_topic(rtf, report, state)
        topics.append(topic)
        state = topic["final_state"]
    sample_record, sample_artifacts = sample.build_sample()
    require(sample_record == json.loads(sample.RECORD.read_bytes()), "Reviewed paragraph record changed")
    matches = [p for t in topics for p in t["paragraphs"]
               if p["source_span"] == {"byte_offset": sample.START, "end_exclusive": sample.END}]
    require(len(matches) == 1 and (matches[0]["text"] + "\n").encode("utf-8") == sample_artifacts["paragraph.txt"],
            "Earlier paragraph is not reproduced exactly")
    actual_objects = [r["object"] for t in topics for p in t["paragraphs"] for r in p["runs"] if r["kind"] == "object"]
    require(actual_objects == [o for r in reports for o in r["objects"]], "Missing/reordered object marker")
    require(sum(len(t["transformations"]) for t in topics) == 5, "Unexpected brace guard count")
    artifacts = {"introduction.txt": topic_text(topics[0]).encode("utf-8"),
                 "body.txt": topic_text(topics[1]).encode("utf-8"),
                 "article.json": json_bytes({"schema_version": 1, "cd_reference": "8802065", "topics": topics})}
    topic_summaries = []
    for topic in topics:
        accounting = Counter()
        for item in topic["accounting"]:
            accounting[item["disposition"]] += item["byte_length"]
        topic_summaries.append({"ordinal": topic["ordinal"], "role": topic["role"],
                               "paragraphs": len(topic["paragraphs"]),
                               "nonempty_paragraphs": sum(bool(p["text"]) for p in topic["paragraphs"]),
                               "text_characters_with_placeholders_and_newlines": len(topic_text(topic)),
                               "metadata_groups": len(topic["metadata"]), "bytes_by_disposition": dict(sorted(accounting.items())),
                               "accounted_tokens": len(topic["accounting"]),
                               "brace_guards_removed": len(topic["transformations"]), "issues": topic["issues"]})
    record = {"schema_version": 1, "cd_reference": "8802065", "scope": "private_full_available_topic_text",
              "source": summary["source"], "topic_map": summary["topic_map"],
              "inventory_sha256": sample.digest(inventory.RECORD.read_bytes()),
              "encoding": {"codec": "cp949", "errors": "strict", "policy": "Source-specific for observed fonts 4, 5, 6; each text run must round-trip exactly."},
              "topics": topic_summaries, "object_placeholders": len(actual_objects),
              "sample_paragraph_sha256": sample_record["outputs"]["paragraph.txt"]["sha256"],
              "outputs": {name: {"bytes": len(raw), "sha256": sample.digest(raw)} for name, raw in artifacts.items()},
              "verification": {"all_source_tokens_accounted_for": True,
                               "all_available_text_decoded": not any(t["issues"] for t in topics),
                               "pilot_paragraph_matches": True, "viewer_compared": False,
                               "article_completeness_verified": False},
              "limitations": ["Text embedded inside image resources is not transcribed; all object positions remain placeholders for step 6.",
                              "Paragraph/run formatting is retained as observed RTF properties, without inferred heading, table, or code semantics.",
                              "Recovered topic text is private preparation, not publication or an access-control decision.",
                              "Completeness and rendering fidelity still require original-viewer comparison."]}
    return record, artifacts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    try:
        record, artifacts = build_recovery()
        metadata = json_bytes(record)
        if args.write_record:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_bytes(metadata)
        else:
            require(json.loads(RECORD.read_bytes()) == record, "Recovery differs from reviewed metadata")
        OUTPUT.mkdir(parents=True, exist_ok=True)
        for name, raw in {**artifacts, "provenance.json": metadata}.items():
            temporary = OUTPUT / (name + ".tmp")
            temporary.write_bytes(raw)
            temporary.replace(OUTPUT / name)
        print(f"Recovered both topics with {record['object_placeholders']} object placeholders; "
              f"{sum(len(t['issues']) for t in record['topics'])} undecoded runs. Output: {OUTPUT.relative_to(ROOT)}")
    except (OSError, ValueError, KeyError) as error:
        print(f"Text recovery failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
