"""Import the three extracted CD1 indexes without reading article bodies."""

from collections import Counter, defaultdict
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import re

from jsonschema import Draft202012Validator

from .toc import ImportFailure, atomic_write, json_bytes

VERSION = "0.1.0"
INDEX_NAMES = ("column.lst", "language.lst", "panecmds.lst")
SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas/cd1-index.schema.json"
REFERENCE = re.compile(r"([0-9]{2})([0-9]{2})([0-9]{3})([A-Za-z]*)\Z")
LABEL_DATE = re.compile(r"^([0-9]{2})\.([0-9]{2})\s+(.*)$")
BASELINE_HASHES = {
    "column.lst": "ac8b1885fdc19b8db1fcf8a85983b6dc1c082c4fda12df3b84d1ea3470220a60",
    "language.lst": "a89d2541e32e3cec89fa1ec9c84403ffcb95e937279b64a33c110d28b48471dc",
    "panecmds.lst": "3396b2504d528c359ff51a8cd6c9306854d526d5ea1e26a7742960e45df694b8",
}


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def reference_fields(reference):
    """Keep native targets intact; a YYMMPPP interpretation is only a candidate."""
    match = REFERENCE.fullmatch(reference)
    if not match:
        return {"reference_kind": "named", "issue_candidate": None,
                "in_target_period_candidate": None}
    issue = f"19{match[1]}-{match[2]}" if 1 <= int(match[2]) <= 12 else None
    return {
        "reference_kind": "suffixed" if match[4] else "numeric",
        "issue_candidate": issue,
        "in_target_period_candidate": "1983-11" <= issue <= "1990-12" if issue else None,
    }


def parse_index(name, raw):
    raw.decode("cp949", errors="strict")
    digest = sha256(raw)
    entries, diagnostics, stack = [], [], []
    offset = 0
    blanks = 0
    terminators = []
    lines = raw.splitlines(keepends=True)

    def warn(code, line, **details):
        diagnostics.append({"code": code, "source_name": name, "line": line, **details})

    for line_number, encoded_line in enumerate(lines, 1):
        raw_line = encoded_line.rstrip(b"\r\n").decode("cp949")
        location = {"name": name, "sha256": digest, "encoding": "cp949",
                    "line": line_number, "byte_offset": offset, "byte_length": len(encoded_line)}
        offset += len(encoded_line)
        if not raw_line.strip():
            blanks += 1
            continue
        content = raw_line.lstrip(" \t")
        prefix = raw_line[:len(raw_line) - len(content)]
        indent = len(prefix.expandtabs(8))
        row = {
            "schema_version": 1, "id": f"cd1-index:{name}:{digest}:L{line_number}",
            "source": location, "raw_line": raw_line, "indent": indent,
            "kind": "unparsed", "parent_id": None, "category_path": [],
            "label": None, "title": None, "display_issue": None,
            "reference_raw": None, "reference": None,
        }
        if content.strip() == "@":
            row["kind"] = "terminator"
            terminators.append(line_number)
            entries.append(row)
            stack = []
            continue
        if terminators:
            warn("content_after_terminator", line_number)
        while stack and stack[-1]["indent"] >= indent:
            stack.pop()
        if "\t" in prefix:
            warn("tab_indentation", line_number)
        expected_indent = stack[-1]["indent"] + 2 if stack else 0
        if indent != expected_indent:
            warn("suspicious_indentation", line_number, indent=indent, expected_indent=expected_indent)
        if stack:
            row["parent_id"] = stack[-1]["id"]
            if stack[-1]["kind"] != "category":
                warn("non_category_parent", line_number)
        row["category_path"] = [
            {"entry_id": parent["id"], "label": parent["label"]}
            for parent in stack if parent["kind"] == "category"
        ]
        if content.count("|") != 1:
            warn("invalid_separator_count", line_number, count=content.count("|"))
        else:
            label, target = content.split("|")
            row.update(label=label.strip(), title=label.strip(), reference_raw=target)
            if not label.strip() or not target.strip():
                warn("empty_label_or_reference", line_number)
            else:
                row["reference"] = target.strip()
                row["kind"] = "category" if row["reference"] == "*" else "reference"
                if target != target.strip():
                    warn("reference_padding", line_number)
                if match := LABEL_DATE.fullmatch(row["label"]):
                    if 1 <= int(match[2]) <= 12:
                        row["display_issue"] = f"19{match[1]}-{match[2]}"
                        row["title"] = match[3]
                    else:
                        warn("invalid_label_month", line_number)
                if row["kind"] == "reference" and (match := REFERENCE.fullmatch(row["reference"])):
                    inferred = reference_fields(row["reference"])["issue_candidate"]
                    if inferred is None:
                        warn("invalid_reference_month", line_number)
                    elif row["display_issue"] and row["display_issue"] != inferred:
                        warn("label_reference_month_mismatch", line_number)
                    if match[3] == "000":
                        warn("zero_page_component", line_number)
        entries.append(row)
        stack.append(row)

    if len(terminators) != 1:
        warn("terminator_count", None, count=len(terminators))
    metadata = {
        "name": name, "sha256": digest, "bytes": len(raw), "encoding": "cp949",
        "lines": len(lines), "blank_lines": blanks, "nonblank_lines": len(entries),
        "kinds": dict(sorted(Counter(row["kind"] for row in entries).items())),
    }
    return entries, metadata, diagnostics


def group_references(entries):
    grouped = defaultdict(list)
    for entry in entries:
        if entry["kind"] == "reference":
            grouped[entry["reference"]].append(entry)
    return [{
        "schema_version": 1, "reference": reference, **reference_fields(reference),
        "occurrence_ids": [entry["id"] for entry in rows],
        "title_variants": sorted({entry["title"] for entry in rows}),
    } for reference, rows in sorted(grouped.items())]


def run_import(source_dir, manifest_path, output):
    source_dir, manifest_path, output = Path(source_dir), Path(manifest_path), Path(output)
    entries, sources, diagnostics, errors = [], [], [], []
    manifest_raw = b""
    manifest = {}
    try:
        manifest_raw = manifest_path.read_bytes()
        manifest = json.loads(manifest_raw)
        if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), list):
            raise ValueError("Extraction manifest must contain a files array")
        for name in INDEX_NAMES:
            raw = (source_dir / name).read_bytes()
            records = [record for record in manifest["files"]
                       if isinstance(record, dict) and record.get("path") == f"raw/{name}"]
            if len(records) != 1:
                errors.append({"code": "manifest_entry_count", "source_name": name, "count": len(records)})
                continue
            expected = records[0]
            if expected.get("sha256") != sha256(raw) or expected.get("bytes") != len(raw):
                errors.append({"code": "source_manifest_mismatch", "source_name": name,
                               "actual_sha256": sha256(raw), "actual_bytes": len(raw)})
                continue
            try:
                rows, metadata, notices = parse_index(name, raw)
            except UnicodeDecodeError as exc:
                errors.append({"code": "invalid_cp949", "source_name": name, "byte_offset": exc.start})
                continue
            if not rows:
                errors.append({"code": "empty_index", "source_name": name})
            entries.extend(rows)
            sources.append(metadata)
            diagnostics.extend(notices)
    except (OSError, ValueError) as exc:
        errors.append({"code": "input_error", "message": str(exc)})
    if errors:
        atomic_write(output / "failed-import-report.json", json_bytes({"schema_version": 1, "errors": errors}))
        raise ImportFailure(f"{len(errors)} CD1 index input errors")

    references = group_references(entries)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate({"entries": entries, "references": references})
    ids = {entry["id"] for entry in entries}
    if len(ids) != len(entries) or len(entries) != sum(s["nonblank_lines"] for s in sources):
        raise ValueError("Index occurrence accounting failed")
    for entry in entries:
        if entry["parent_id"] is not None and entry["parent_id"] not in ids:
            raise ValueError("Unresolved index parent")
    grouped_ids = [identifier for group in references for identifier in group["occurrence_ids"]]
    if Counter(grouped_ids) != Counter(e["id"] for e in entries if e["kind"] == "reference"):
        raise ValueError("Grouped reference accounting failed")

    numeric = [group for group in references if group["reference_kind"] == "numeric"]
    observed = {"numeric_references": len(numeric),
                "target_numeric_references": sum(g["in_target_period_candidate"] is True for g in numeric)}
    known_inputs = {source["name"]: source["sha256"] for source in sources} == BASELINE_HASHES
    expected = {"numeric_references": 1038, "target_numeric_references": 360}
    baseline_status = ("matched" if observed == expected else "different") if known_inputs else "not_applicable"
    if baseline_status == "different":
        diagnostics.append({"code": "baseline_count_difference", "source_name": None, "line": None})
    report = {
        "schema_version": 1, "errors": [], "sources": sources,
        "counts": {
            "source_files": len(sources), "lines": sum(s["lines"] for s in sources),
            "blank_lines": sum(s["blank_lines"] for s in sources), "entries": len(entries),
            "by_kind": dict(sorted(Counter(e["kind"] for e in entries).items())),
            "reference_occurrences": len(grouped_ids), "distinct_references": len(references),
            "by_reference_kind": dict(sorted(Counter(g["reference_kind"] for g in references).items())),
            "numeric_references_by_year": dict(sorted(Counter(g["reference"][:2] for g in numeric).items())),
            **observed,
            "diagnostics": len(diagnostics),
            "by_diagnostic": dict(sorted(Counter(d["code"] for d in diagnostics).items())),
        },
        "baseline_comparison": {"status": baseline_status, "expected": expected, "observed": observed},
        "diagnostics": diagnostics,
    }

    def jsonl(rows):
        return "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows).encode("utf-8")

    outputs = {"entries.jsonl": jsonl(entries), "references.jsonl": jsonl(references),
               "validation-report.json": json_bytes(report)}
    run_manifest = {
        "schema_version": 1, "importer_version": VERSION, "encoding": "cp949",
        "python_version": platform.python_version(),
        "jsonschema_version": importlib.metadata.version("jsonschema"),
        "extraction_manifest_sha256": sha256(manifest_raw),
        "container_sha256_recorded": manifest.get("source_sha256"),
        "schema_sha256": sha256(SCHEMA_PATH.read_bytes()),
        "sources": [{key: source[key] for key in ("name", "bytes", "sha256")} for source in sources],
        "outputs": {name: {"sha256": sha256(raw), "bytes": len(raw)} for name, raw in outputs.items()},
    }
    for name, raw in outputs.items():
        atomic_write(output / name, raw)
    atomic_write(output / "manifest.json", json_bytes(run_manifest))
    (output / "failed-import-report.json").unlink(missing_ok=True)
    return report
