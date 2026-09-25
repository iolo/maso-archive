"""Build the private CD2 940116300 article probe from checksummed raw sources."""

import argparse
import hashlib
import html
import io
import json
from pathlib import Path
import re
import shutil
import tempfile

from PIL import Image
from tools.inventory_cd1_rtf import tokenize
from tools.inventory_cd2_sources import PROBE, ROOT, RECORD, TREE
from tools.map_cd1_topic import require
from tools.recover_cd1_text import json_bytes

OUTPUT = ROOT / "build/cd2-reference-pilot"
TOPIC = "940116300"
CSS = """body{font:17px/1.65 system-ui,sans-serif;max-width:72rem;margin:2rem auto;padding:0 1rem;color:#222}a{color:#1455a0}.note{color:#555}.gap{border-left:4px solid #a60;padding-left:1rem}p{white-space:pre-wrap;tab-size:8;overflow-wrap:anywhere}img{max-width:100%;height:auto}figure{margin:1.5rem 0}figcaption{color:#555}"""
OBJECT = re.compile(rb"\\\{(?:bmc|ewl) ([^}]+)\\\}")
SKIP = re.compile(rb"\{\\up [+#$K]\}\{\\footnote\\pard\\plain\{\\up [+#$K]\}[^}]*\}|\{\\up [+#$K]\}|\{\\v [^}]+\}")
COSMETIC = set("pard plain fs keepn li qr qc ql qj ri sa sb sl tx cf ul uldb".split())


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def decode(data, source_offset, issues):
    parts = []
    cursor = 0
    while cursor < len(data):
        try:
            parts.append(data[cursor:].decode("cp949"))
            break
        except UnicodeDecodeError as error:
            start, end = cursor + error.start, cursor + error.end
            parts.append(data[cursor:start].decode("cp949"))
            parts.append(f"⟦bytes:{data[start:end].hex()}⟧")
            issues.append({"type": "undecodable_bytes", "source_byte_offset": source_offset,
                           "decoded_run_byte_index": start, "bytes_hex": data[start:end].hex()})
            cursor = end
    text = "".join(parts)
    for match in re.finditer(r"\{vfld\d*\}", text):
        issues.append({"type": "unresolved_dynamic_field", "source_run_byte_offset": source_offset,
                       "field": match.group()})
    return re.sub(r"\{(vfld\d*)\}", r"⟦field:\1⟧", text)


def parse(raw, base):
    tokens = tokenize(raw, base)
    require(sum(t["byte_length"] for t in tokens) == len(raw), "RTF byte coverage failed")
    spans = []
    for pattern, role in ((SKIP, "metadata"), (OBJECT, "object")):
        spans.extend((base + m.start(), base + m.end(), role, m) for m in pattern.finditer(raw))
    spans.sort()
    require(all(a[1] <= b[0] for a, b in zip(spans, spans[1:])), "Overlapping RTF spans")
    paragraphs, runs, buffer, fragments, issues = [], [], bytearray(), [], []
    bold = False

    def flush():
        if buffer:
            runs.append({"type": "text", "text": decode(bytes(buffer), fragments[0]["byte_offset"], issues),
                         "bold": bold, "source_fragments": fragments.copy()})
            buffer.clear()
            fragments.clear()

    def paragraph(terminated=True):
        flush()
        paragraphs.append({"id": f"p{len(paragraphs)+1}", "runs": runs.copy(), "terminated": terminated})
        runs.clear()

    def add(data, token):
        buffer.extend(data)
        fragments.append({"byte_offset": token["byte_offset"], "byte_length": token["byte_length"]})

    position = 0
    index = 0
    while index < len(tokens):
        token = tokens[index]
        start = token["byte_offset"]
        while position < len(spans) and spans[position][1] <= start:
            position += 1
        if position < len(spans) and start == spans[position][0]:
            stop, role, match = spans[position][1:]
            flush()
            if role == "object":
                command = match[1].decode("ascii")
                name = command.split("!")[-1].strip() if "!" in command else command.strip()
                require(re.fullmatch(r"[A-Za-z0-9_.]+", name), "Unsafe media resource")
                runs.append({"type": "media", "resource": name,
                             "source_span": {"byte_offset": start, "end_exclusive": stop}})
            while index < len(tokens) and tokens[index]["byte_offset"] < stop:
                index += 1
            continue
        kind = token["kind"]
        if kind == "text_bytes":
            add(raw[start-base:start-base+token["byte_length"]], token)
        elif kind == "hex_byte":
            add(bytes([int(raw[start-base+2:start-base+4], 16)]), token)
        elif kind == "control_symbol":
            symbol = token["symbol"]
            if symbol in "\\{}":
                add(symbol.encode(), token)
            elif symbol == "-" and index and tokens[index-1].get("symbol") == "{":
                pass  # HELPDECO literal-brace guard, not printed content.
            else:
                flush()
                marker = f"⟦RTF symbol:{symbol}⟧"
                runs.append({"type": "text", "text": marker, "bold": False, "source_fragments": []})
                issues.append({"type": "unsupported_symbol", "byte_offset": start, "symbol": symbol})
        elif kind == "control_word":
            word, value = token["word"], token["parameter"]
            if word == "par":
                paragraph()
            elif word == "line":
                add(b"\n", token)
            elif word == "tab":
                add(b"\t", token)
            elif word == "b":
                flush()
                bold = value != 0
            elif word == "plain":
                flush()
                bold = False
            elif word in COSMETIC:
                pass
            else:
                flush()
                marker = f"⟦RTF control:{word}⟧"
                runs.append({"type": "text", "text": marker, "bold": False, "source_fragments": []})
                issues.append({"type": "unsupported_control", "byte_offset": start, "word": word})
        elif kind != "physical_newline":
            raise ValueError(f"Unrepresented RTF token at {start}: {kind}")
        index += 1
    if runs or buffer:
        paragraph(False)
    return paragraphs, issues, len(tokens)


def put(root, name, data):
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data.encode("utf-8") if isinstance(data, str) else data)


def build(destination=OUTPUT, verify_existing=False):
    record = json.loads(RECORD.read_bytes())
    detail_path = ROOT / record["private_detail"]["path"]
    detail_raw = detail_path.read_bytes()
    require(len(detail_raw) == record["private_detail"]["bytes"] and
            digest(detail_raw) == record["private_detail"]["sha256"], "CD2 private inventory changed")
    detail = json.loads(detail_raw)
    raw_files = {row["path"]: row for row in detail["probe"]["files"]}
    disc_files = {row["path"]: row for row in detail["extracted"]["files"]}
    source = record["candidate"]["rtf"]
    rtf = (PROBE / "MASO2.rtf").read_bytes()
    require(digest(rtf) == raw_files["MASO2.rtf"]["sha256"], "Changed CD2 decoder RTF")
    raw = rtf[source["byte_offset"]:source["byte_offset"] + source["byte_length"]]
    require(digest(raw) == source["sha256"], "Changed CD2 article RTF")
    paragraphs, issues, token_count = parse(raw, source["byte_offset"])
    resources = [run["resource"] for p in paragraphs for run in p["runs"] if run["type"] == "media"]
    require(len(resources) == record["candidate_media"]["markers"], "Media markers changed")
    title = record["candidate"]["index"]["entry"].split("^")[0]
    rendered = []
    plain = []
    for p in paragraphs:
        content = []
        for run in p["runs"]:
            if run["type"] == "media":
                name = run["resource"]
                plain.append(f"[image:{name}]")
                content.append(f'<a href="media/{name}"><img src="media/{name}.png" alt="{name}" title="Original image: {name}"></a>')
            else:
                value = run["text"]
                plain.append(value)
                escaped = html.escape(value)
                content.append(f"<strong>{escaped}</strong>" if run["bold"] else escaped)
        if p["terminated"]:
            plain.append("\n")
        rendered.append("<p>" + "".join(content) + "</p>")
    text = "".join(plain)
    with tempfile.TemporaryDirectory(prefix=".cd2-pilot-", dir=destination.parent) as tmp:
        stage = Path(tmp)
        for name in sorted(set(resources)):
            original = (PROBE / name).read_bytes()
            require(len(original) == raw_files[name]["bytes"] and
                    digest(original) == raw_files[name]["sha256"], f"Changed media source: {name}")
            put(stage, f"media/{name}", original)
            with Image.open(io.BytesIO(original)) as picture:
                picture.load()
                pixels = picture.convert("RGBA")
                output = io.BytesIO()
                pixels.save(output, format="PNG")
                with Image.open(io.BytesIO(output.getvalue())) as restored:
                    require(restored.convert("RGBA").tobytes() == pixels.tobytes(),
                            f"Converted image pixels differ: {name}")
            put(stage, f"media/{name}.png", output.getvalue())
        for path in record["candidate_attachment_paths"]:
            file = TREE / path
            original = file.read_bytes()
            require(len(original) == disc_files[path]["bytes"] and
                    digest(original) == disc_files[path]["sha256"], f"Changed attachment: {path}")
            put(stage, "attachments/" + file.name, original)
        put(stage, "article.txt", text)
        put(stage, "blocks.json", json_bytes({"reference": TOPIC, "source": source,
                                                "token_count": token_count, "paragraphs": paragraphs,
                                                "issues": issues}))
        body = f'<h1>{html.escape(title)}</h1><p class="note">CD text · paper verification pending · native reference {TOPIC}</p>'
        body += '<p><a href="article.txt">UTF-8 text</a> · <a href="blocks.json">Source blocks</a> · <a href="attachments/TEX.ZIP">Original source ZIP</a></p>'
        body += '<p class="gap">Article boundaries and transcription remain subject to paper review.</p>'
        body += "".join(rendered)
        put(stage, "index.html", '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(title) + '</title><link rel="stylesheet" href="style.css"><body>' + body + '</body></html>\n')
        put(stage, "style.css", CSS + "\n")
        files = [{"path": p.relative_to(stage).as_posix(), "bytes": p.stat().st_size,
                  "sha256": digest(p.read_bytes())} for p in sorted(stage.rglob("*")) if p.is_file()]
        put(stage, "manifest.json", json_bytes({"schema_version": 1, "reference": TOPIC,
                                                 "title": title, "paragraphs": len(paragraphs),
                                                 "issues": len(issues), "media_occurrences": len(resources),
                                                 "files": files}))
        if destination.exists():
            if verify_existing:
                existing = json.loads((destination / "manifest.json").read_bytes())
                require(existing == json.loads((stage / "manifest.json").read_bytes()), "Pilot rebuild differs")
            shutil.rmtree(destination)
        shutil.copytree(stage, destination)
    return {"paragraphs": len(paragraphs), "issues": len(issues), "media": len(resources),
            "text_characters": len(text), "text_sha256": digest(text.encode())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-existing", action="store_true")
    args = parser.parse_args()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    print(build(verify_existing=args.verify_existing))


if __name__ == "__main__":
    main()
