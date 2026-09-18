"""Trace and convert the pilot's images privately; preserve fidelity exceptions.

Run python3 -m tools.map_cd1_images. Requires convert, inkscape, fc-match, Pillow.
"""

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops, __version__ as PILLOW_VERSION

from tools import map_cd1_blocks as blocks
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import ROOT, require
from tools.recover_cd1_text import json_bytes

MANIFEST = ROOT / "private/cd1-probe/manifest.json"
RAW = MANIFEST.parent / "raw"
OUTPUT = ROOT / "build/cd1-images/8802065"
RECORD = ROOT / "data/catalog/image-maps/cd1-8802065.json"
SVG = "{http://www.w3.org/2000/svg}"


def command(args):
    result = subprocess.run(args, cwd=ROOT, capture_output=True, timeout=60)
    return {"argv": args, "exit_code": result.returncode,
            "stdout": result.stdout.decode("utf-8", errors="replace"),
            "stderr": result.stderr.decode("utf-8", errors="replace")}


def checked_source(name, manifest, directory=RAW):
    require(re.fullmatch(r"[A-Za-z0-9_]+\.(bmp|dib|wmf)", name) is not None, "Unsafe resource name")
    entries = [f for f in manifest["files"] if f["path"] == "raw/" + name]
    require(len(entries) == 1, f"Missing/duplicate manifest entry: {name}")
    source = directory / name
    raw = source.read_bytes()
    require(len(raw) == entries[0]["bytes"] and digest(raw) == entries[0]["sha256"],
            f"Source manifest mismatch: {name}")
    return raw


def bitmap_pixels(path):
    with Image.open(path) as image:
        image.load()
        pixels = image.convert("RGBA")
        return {"format": image.format, "width": image.width, "height": image.height,
                "rgba_sha256": digest(pixels.tobytes())}


def wmf_header(raw):
    require(len(raw) >= 40 and raw[:4] == bytes.fromhex("d7cdc69a"), "Unsupported WMF header")
    left, top, right, bottom, units = struct.unpack_from("<hhhhH", raw, 6)
    require(units > 0 and right > left and bottom > top, "Invalid WMF bounds")
    return {"format": "placeable_WMF", "bounds": [left, top, right, bottom],
            "units_per_inch": units, "width_inches": (right - left) / units,
            "height_inches": (bottom - top) / units,
            "contains_symbol_font_name": b"Symbol\x00" in raw}


def inspect_svg(path):
    root = ET.fromstring(path.read_bytes())
    require(root.tag == SVG + "svg", "Not an SVG document")
    # Inspect drawing elements outside definitions; empty defs/patterns aren't art.
    drawable = {SVG + n for n in ("path", "text", "rect", "line", "polyline", "polygon", "circle", "ellipse", "image", "use")}
    def shapes(node):
        if node.tag == SVG + "defs":
            return 0
        return int(node.tag in drawable) + sum(shapes(child) for child in node)
    fonts = set()
    for node in root.iter():
        fonts.update(re.findall(r"font-family:([^;]+)", node.get("style", "")))
        if node.get("font-family"):
            fonts.add(node.get("font-family"))
    return {"width": root.get("width"), "height": root.get("height"),
            "viewBox": root.get("viewBox"), "drawing_elements": shapes(root),
            "font_families": sorted(fonts)}


def blank_preview(path):
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        return ImageChops.difference(rgb, Image.new("RGB", rgb.size, "white")).getbbox() is None


def convert_resource(name, source_raw, output, runner=command):
    """Nonzero exit, blank drawings, and symbol loss must never imply fidelity."""
    source = RAW / name
    item = {"resource": name, "source": {"path": str(source.relative_to(ROOT)),
            "bytes": len(source_raw), "sha256": digest(source_raw)}, "commands": [],
            "derivatives": [], "concerns": [], "viewer_compared": False}
    vector = name.endswith(".wmf")
    item["source_format"] = wmf_header(source_raw) if vector else bitmap_pixels(source)
    target = output / "assets" / (name + (".svg" if vector else ".png"))
    args = (["inkscape", str(source.relative_to(ROOT)), "--export-type=svg", "--export-plain-svg",
             f"--export-filename={target}"] if vector else
            ["convert", str(source.relative_to(ROOT)), "-strip", "-define", "png:exclude-chunks=date,time", str(target)])
    result = runner(args)
    item["commands"].append(result)
    if result["exit_code"] != 0 or not target.exists():
        item.update(status="conversion_failed")
        item["concerns"].append("converter_failed_or_produced_no_file")
        return item
    if result["stderr"]:
        item["concerns"].append("converter_stderr_requires_review")
    if vector:
        item["svg"] = inspect_svg(target)
        if item["svg"]["drawing_elements"] == 0:
            item["concerns"].append("svg_has_no_drawing_elements")
        if item["source_format"]["contains_symbol_font_name"] and not any(
                "symbol" in f.lower() for f in item["svg"]["font_families"]):
            item["concerns"].append("source_Symbol_font_not_retained_in_svg; mathematical_glyphs_suspect")
        if item["svg"]["font_families"]:
            item["concerns"].append("live_svg_text_depends_on_available_fonts")
        preview = output / "previews" / (name + ".png")
        result = runner(["inkscape", str(target), "--export-type=png", "--export-dpi=384",
                         "--export-background=white", "--export-background-opacity=1", f"--export-filename={preview}"])
        item["commands"].append(result)
        if result["exit_code"] != 0 or not preview.exists():
            item["concerns"].append("svg_raster_preview_failed")
        else:
            item["preview_pixels"] = bitmap_pixels(preview)
            item["preview_blank"] = blank_preview(preview)
            if item["preview_blank"]:
                item["concerns"].append("raster_preview_is_blank")
            if result["stderr"]:
                item["concerns"].append("preview_stderr_requires_review")
            # Strip generated PNG metadata for repeatable checksums.
            stripped = preview.with_suffix(".stripped.png")
            result = runner(["convert", str(preview), "-strip", "-define", "png:exclude-chunks=date,time", str(stripped)])
            item["commands"].append(result)
            require(result["exit_code"] == 0 and stripped.exists(), "Preview normalization failed")
            require(bitmap_pixels(stripped) == item["preview_pixels"], "Preview normalization changed pixels")
            stripped.replace(preview)
            item["derivatives"].append({"path": "previews/" + preview.name, "role": "inspection_preview_384dpi"})
        item["status"] = "needs_review" if any(c != "live_svg_text_depends_on_available_fonts" for c in item["concerns"]) else "converted_pending_viewer"
    else:
        item["png_pixels"] = bitmap_pixels(target)
        require(all(item["source_format"][k] == item["png_pixels"][k] for k in ("width", "height", "rgba_sha256")),
                f"Bitmap conversion changed decoded pixels: {name}")
        item["pixel_equivalent"] = True
        item["status"] = "needs_review" if item["concerns"] else "converted_pending_viewer"
    item["derivatives"].insert(0, {"path": "assets/" + target.name, "role": "converted_svg" if vector else "converted_png"})
    return item


def occurrences(article, block_map):
    blocks.validate_map(article, block_map)
    captions = {}
    for link in block_map["relationships"]:
        captions.setdefault(link["to_block"], []).append(link["from_block"])
    result = [{"id": f"cd1-8802065:T{b['topic_ordinal']}:P{o['paragraph_ordinal']:03d}:R{o['run_ordinal']}",
               "topic_ordinal": b["topic_ordinal"], "block_id": b["id"], "block_kind": b["kind"],
               "caption_block_ids": captions.get(b["id"], []), **o}
              for b in block_map["blocks"] for o in b["object_refs"]]
    expected = [(t["ordinal"], p["ordinal"], n, r["object"]["resource"], r["object"]["byte_offset"])
                for t in article["topics"] for p in t["paragraphs"] for n, r in enumerate(p["runs"], 1) if r["kind"] == "object"]
    require([(o["topic_ordinal"], o["paragraph_ordinal"], o["run_ordinal"], o["resource"], o["rtf_byte_offset"]) for o in result] == expected,
            "Image occurrence coverage/order changed")
    return result


def gallery(items, refs):
    lookup = {i["resource"]: i for i in items}
    parts = ['<!doctype html><html lang="en"><meta charset="utf-8"><title>CD1 pilot image review</title>',
             '<style>body{font:16px sans-serif;max-width:1000px;margin:2rem auto;padding:1rem}section{border-top:1px solid #aaa;padding:1rem 0}img{max-width:100%;background:white;border:1px solid #ccc}code{overflow-wrap:anywhere}</style>',
             '<h1>CD1 8802065: private image review</h1><p>Source order; no original-viewer comparison yet. SVG text depends on fonts. Suspect and blank conversions remain flagged.</p>']
    for ref in refs:
        item = lookup[ref["resource"]]
        parts += [f'<section id="image-{ref["rtf_byte_offset"]}"><h2>{html.escape(ref["resource"])}</h2>',
                  f'<p>{html.escape(ref["block_id"])} / run {ref["run_ordinal"]} / {item["status"]}</p>',
                  f'<p>{html.escape("; ".join(item["concerns"]))}</p>']
        for asset in item["derivatives"]:
            path = html.escape(asset["path"], quote=True)
            parts.append(f'<p><a href="{path}">{asset["role"]}</a><br><img src="{path}" alt="{html.escape(ref["resource"])}"></p>')
        parts.append('</section>')
    return ("\n".join(parts) + "\n</html>\n").encode("utf-8")


def build_images():
    article_raw, map_raw, manifest_raw = blocks.SOURCE.read_bytes(), (blocks.OUTPUT / "blocks.json").read_bytes(), MANIFEST.read_bytes()
    require(digest(article_raw) == blocks.SOURCE_SHA256, "Changed structured recovery")
    require(digest(map_raw) == json.loads(blocks.RECORD.read_bytes())["output"]["sha256"], "Changed block map")
    article, block_map, manifest = json.loads(article_raw), json.loads(map_raw), json.loads(manifest_raw)
    refs = occurrences(article, block_map)
    names = list(dict.fromkeys(o["resource"] for o in refs))
    # Verify every input before invoking a converter or replacing a previous result.
    sources = {name: checked_source(name, manifest) for name in names}
    versions = {name: command(args) for name, args in (("convert", ["convert", "-version"]),
                ("inkscape", ["inkscape", "--version"]), ("fontconfig", ["fc-match", "--version"]))}
    require(all(v["exit_code"] == 0 for v in versions.values()), "Required conversion tool unavailable")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".image-stage-", dir=OUTPUT.parent) as directory:
        staging = Path(directory)
        for sub in ("assets", "previews"):
            (staging / sub).mkdir()
        items = [convert_resource(name, sources[name], staging) for name in names]
        fonts = sorted({f for i in items for f in i.get("svg", {}).get("font_families", [])})
        font_resolution = {font: command(["fc-match", "-f", "%{family}|%{file}\\n", font]) for font in fonts}
        # Commands use canonical output paths in the manifest, not random staging paths.
        for item in items:
            for call in item["commands"]:
                call["argv"] = [a.replace(str(staging), str(OUTPUT.relative_to(ROOT))) for a in call["argv"]]
                for key in ("stdout", "stderr"):
                    call[key] = call[key].replace(str(staging), str(OUTPUT.relative_to(ROOT)))
            for asset in item["derivatives"]:
                raw = (staging / asset["path"]).read_bytes()
                asset.update(bytes=len(raw), sha256=digest(raw))
        hashes = Counter(i["source"]["sha256"] for i in items)
        result = {"schema_version": 1, "cd_reference": "8802065",
                  "sources": [{"path": str(path.relative_to(ROOT)), "sha256": digest(raw)} for path, raw in
                              ((blocks.SOURCE, article_raw), (blocks.OUTPUT / "blocks.json", map_raw), (MANIFEST, manifest_raw))],
                  "tools": versions, "pillow_version": PILLOW_VERSION, "font_resolution": font_resolution,
                  "counts": {"occurrences": len(refs), "resources": len(items), "distinct_source_hashes": len(hashes),
                             "formats": dict(sorted(Counter(Path(n).suffix for n in names).items())),
                             "statuses": dict(sorted(Counter(i["status"] for i in items).items())),
                             "pixel_equivalent_bitmaps": sum(i.get("pixel_equivalent", False) for i in items)},
                  "duplicate_source_groups": [[i["resource"] for i in items if i["source"]["sha256"] == h] for h, count in hashes.items() if count > 1],
                  "occurrences": refs, "resources": items,
                  "verification": {"source_manifest_checked": True, "exact_occurrence_coverage": True,
                                   "viewer_compared": False, "image_fidelity_verified": False}}
        (staging / "images.json").write_bytes(json_bytes(result))
        (staging / "review.html").write_bytes(gallery(items, refs))
        summary = {k: result[k] for k in ("schema_version", "cd_reference", "sources", "counts", "duplicate_source_groups", "verification")}
        summary["review_items"] = [{"resource": i["resource"], "status": i["status"], "concerns": i["concerns"]} for i in items if i["concerns"]]
        summary["outputs"] = [{"path": str((OUTPUT / name).relative_to(ROOT)), "bytes": (staging / name).stat().st_size,
                               "sha256": digest((staging / name).read_bytes())} for name in ("images.json", "review.html")]
        files = {str(p.relative_to(staging)): p.read_bytes() for p in sorted(staging.rglob("*")) if p.is_file()}
    return summary, files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-record", action="store_true")
    args = parser.parse_args()
    try:
        record, files = build_images()
        if args.write_record:
            RECORD.parent.mkdir(parents=True, exist_ok=True)
            RECORD.write_bytes(json_bytes(record))
        else:
            require(json.loads(RECORD.read_bytes()) == record, "Image outputs differ from reviewed summary; inspect tool/font changes")
        files["provenance.json"] = json_bytes(record)
        for name, raw in files.items():
            path = OUTPUT / name
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_name(path.name + ".tmp")
            temporary.write_bytes(raw)
            temporary.replace(path)
        print(f"Mapped {record['counts']['occurrences']} image occurrences: {record['counts']['statuses']}. "
              f"Viewer fidelity pending. Output: {OUTPUT.relative_to(ROOT)}")
    except (OSError, ValueError, KeyError, struct.error, ET.ParseError, subprocess.TimeoutExpired) as error:
        print(f"Image mapping failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
