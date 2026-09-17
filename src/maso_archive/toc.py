"""Lossless Markdown TOC import with conservative parsing and persistent IDs.

Imported fields are candidates, not reviewed publication data. This module does
not read magazine bodies, generate summaries, or export public-site content.
"""

from collections import Counter, defaultdict
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import re
import tempfile
import unicodedata

from jsonschema import Draft202012Validator

from . import __version__

SCHEMA_VERSION = 1
SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "toc-import.schema.json"
HEADING = re.compile(r"## (\d{2})\.(\d{2})\s*$")
BULLET = re.compile(r"( *)- (.*)$")
PAGE_SUFFIX = re.compile(r"\s+=\s*(.*?)\s*$")


class ImportFailure(ValueError):
    """Validation or identity ambiguity prevented updating the catalog."""


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def notice(code, line=None, **details):
    return {"code": code, "line": line, **details}


def month_range(start, end):
    def number(value):
        if not re.fullmatch(r"19\d{2}-(0[1-9]|1[0-2])", value):
            raise ValueError(f"Invalid 20th-century issue month: {value}")
        year, month = map(int, value.split("-"))
        return year * 12 + month - 1

    first, last = number(start), number(end)
    if first > last:
        raise ValueError("Start month must not follow end month")
    return [f"maso-{n // 12:04}-{n % 12 + 1:02}" for n in range(first, last + 1)]


def parse_fields(raw_text):
    """Parse typography conventions without assigning normalized authors/ranges."""
    text = raw_text.strip()
    flags = []
    page_raw = None
    pages = []
    if match := PAGE_SUFFIX.search(text):
        page_raw = match[1]
        text = text[:match.start()].rstrip()
        if re.fullmatch(r"[1-9]\d*", page_raw):
            pages = [int(page_raw)]
        elif re.fullmatch(r"[1-9]\d*(?:(?:\s*,\s*|\s+)[1-9]\d*)+", page_raw):
            pages = [int(p) for p in re.findall(r"\d+", page_raw)]
            flags.append("multiple_page_references")
        else:
            flags.append("unparsed_page_reference")
    else:
        flags.append("missing_page_reference")

    title = text
    byline = None
    contributors = []
    # A slash surrounded by spaces is the source's byline convention. CP/M,
    # S/W, and other embedded slashes stay intact. Multiple separators need review.
    separators = list(re.finditer(r"\s+/\s+|\s+/$", text))
    if len(separators) == 1:
        sep = separators[0]
        proposed_title = text[:sep.start()].strip()
        proposed_byline = text[sep.end():].strip()
        if proposed_title:
            title = proposed_title
            if proposed_byline:
                byline = proposed_byline
                contributors = [part.strip() for part in byline.split(";") if part.strip()]
            else:
                flags.append("empty_byline")
        else:
            flags.append("ambiguous_byline")
    elif len(separators) > 1:
        flags.append("ambiguous_byline")
    if not title:
        flags.append("empty_title")
    return {
        "title_candidate": title,
        "byline_candidate": byline,
        "contributor_candidates": contributors,
        "page_reference_raw": page_raw,
        "page_candidates": pages,
        "start_page_candidate": pages[0] if len(pages) == 1 else None,
        "end_page_candidate": None,
        "flags": flags,
    }


def parse_toc(text, source_id):
    issues, entries, errors = [], [], []
    seen_issues = set()
    issue = None
    stack = []
    sibling_counts = Counter()
    previous_page = None
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        if match := HEADING.fullmatch(line):
            year, month = 1900 + int(match[1]), int(match[2])
            if not 1 <= month <= 12:
                errors.append(notice("invalid_issue_month", line_number))
                issue = None
                continue
            issue_id = f"maso-{year:04}-{month:02}"
            if issue_id in seen_issues:
                errors.append(notice("duplicate_issue", line_number, issue_id=issue_id))
            seen_issues.add(issue_id)
            issue = {
                "schema_version": SCHEMA_VERSION,
                "id": issue_id, "year": year, "month": month,
                "original_label": f"{match[1]}.{match[2]}",
                "publication_date": None, "total_pages": None,
                "verification_status": "unreviewed",
                "coverage": {"toc": "transcribed", "body": "not_matched", "cover": "not_inspected"},
                "source": {"id": source_id, "line_start": line_number, "line_end": line_number, "raw_line": line},
            }
            issues.append(issue)
            stack = []
            sibling_counts = Counter()
            previous_page = None
            continue
        match = BULLET.fullmatch(line)
        if not match:
            errors.append(notice("unsupported_source_line", line_number, raw_line=line))
            continue
        if issue is None:
            errors.append(notice("entry_without_issue", line_number, raw_line=line))
            continue
        indent = len(match[1])
        while stack and entries[stack[-1]]["indent"] >= indent:
            stack.pop()
        parent = stack[-1] if stack else None
        fields = parse_fields(match[2])
        if indent % 2 or (parent is None and indent != 0) or (
            parent is not None and indent != entries[parent]["indent"] + 2
        ):
            fields["flags"].append("suspicious_indentation")
        page = fields["start_page_candidate"]
        if page is not None:
            if previous_page is not None and page < previous_page:
                fields["flags"].append("page_order_decrease")
            previous_page = page
        if "empty_title" in fields["flags"]:
            errors.append(notice("empty_title", line_number))
        sibling_counts[parent] += 1
        entry = {
            "schema_version": SCHEMA_VERSION, "issue_id": issue["id"],
            "_parent": parent, "_ancestors": stack.copy(),
            "order": len(entries) + 1, "sibling_order": sibling_counts[parent],
            "indent": indent, "depth": len(stack), "raw_text": match[2],
            "source": {"id": source_id, "line_start": line_number, "line_end": line_number, "raw_line": line},
            "verification_status": "unreviewed", **fields,
        }
        entries.append(entry)
        stack.append(len(entries) - 1)
    return issues, entries, errors


def assign_identities(entries, previous, decisions, errors):
    """Reuse exact identities; edits/removals require explicit review decisions.

    No positional/fuzzy guess is used for edited text. Repeated identical entries
    can reuse occurrence order only when the entire issue's text/hierarchy is
    unchanged. Otherwise they require explicit source-line-to-ID decisions.
    """
    old_entries = previous.get("entries", [])
    old_by_id = {e["id"]: e for e in old_entries}
    old_by_key = defaultdict(list)
    old_by_issue = defaultdict(list)
    current_by_issue = defaultdict(list)
    for old in old_entries:
        old_by_key[(old["issue_id"], old["raw_text"])].append(old)
        old_by_issue[old["issue_id"]].append(old)
    for index, entry in enumerate(entries):
        current_by_issue[entry["issue_id"]].append(index)

    unchanged = {}
    for issue_id, indices in current_by_issue.items():
        old = old_by_issue[issue_id]
        new_shape = [(entries[i]["raw_text"], entries[i]["depth"]) for i in indices]
        if new_shape == [(e["raw_text"], e["depth"]) for e in old]:
            unchanged.update({index: record["id"] for index, record in zip(indices, old)})

    assignments = decisions.get("assignments", {})
    current_lines = {str(e["source"]["line_start"]): i for i, e in enumerate(entries)}
    new_lines = set(decisions.get("new_lines", []))
    used = set()
    retired = set(previous.get("retired_ids", []))
    allowed_removed = set(decisions.get("removed_ids", []))
    for removed in sorted(allowed_removed - old_by_id.keys()):
        errors.append(notice("invalid_removed_identity", id=removed))
    for line in sorted(new_lines):
        if line not in current_lines or line in assignments:
            errors.append(notice("invalid_new_identity", source_line=line))
    # Explicit assignments take precedence over all automatic matches.
    for line, identifier in assignments.items():
        index = current_lines.get(line)
        old = old_by_id.get(identifier)
        if index is None or old is None or old["issue_id"] != entries[index]["issue_id"] or identifier in used:
            errors.append(notice("invalid_identity_assignment", id=identifier, source_line=line))
            continue
        entries[index]["id"] = identifier
        used.add(identifier)

    next_serial = dict(previous.get("next_serial", {}))
    for index, entry in enumerate(entries):
        if "id" in entry:
            continue
        force_new = str(entry["source"]["line_start"]) in new_lines
        matches = [] if force_new else old_by_key[(entry["issue_id"], entry["raw_text"])]
        if len(matches) == 1 and matches[0]["id"] not in used:
            identifier = matches[0]["id"]
        elif not force_new and index in unchanged and unchanged[index] not in used:
            identifier = unchanged[index]
        elif matches:
            errors.append(notice(
                "ambiguous_identity", entry["source"]["line_start"],
                issue_id=entry["issue_id"], candidate_ids=[m["id"] for m in matches],
            ))
            continue
        else:
            serial = next_serial.get(entry["issue_id"], 1)
            identifier = f"{entry['issue_id']}-toc-{serial:04}"
            next_serial[entry["issue_id"]] = serial + 1
        entry["id"] = identifier
        used.add(identifier)
    for identifier in sorted(old_by_id.keys() - used):
        if identifier in allowed_removed:
            retired.add(identifier)
        else:
            old = old_by_id[identifier]
            errors.append(notice("unresolved_previous_identity", id=identifier, raw_text=old["raw_text"]))
    for identifier in sorted(allowed_removed & used):
        errors.append(notice("removed_identity_still_present", id=identifier))
    if errors:
        return None
    return {
        "schema_version": SCHEMA_VERSION,
        "next_serial": dict(sorted(next_serial.items())),
        "retired_ids": sorted(retired),
        "entries": [
            {key: entry[key] for key in ("id", "issue_id", "raw_text", "depth")}
            for entry in entries
        ],
    }


def finalize_entries(entries):
    parents = {entry["_parent"] for entry in entries if entry["_parent"] is not None}
    candidates = []
    for index, entry in enumerate(entries):
        entry["parent_id"] = entries[entry["_parent"]]["id"] if entry["_parent"] is not None else None
        entry["section_path"] = [entries[i]["id"] for i in entry["_ancestors"]]
        if index in parents:
            if entry["page_reference_raw"] is None and entry["byline_candidate"] is None:
                entry["kind_candidate"] = "section"
            else:
                entry["kind_candidate"] = "unknown"
                entry["flags"].append("bundle_or_article")
        elif entry["byline_candidate"] or entry["page_reference_raw"] is not None:
            entry["kind_candidate"] = "article"
        else:
            entry["kind_candidate"] = "subtopic" if entry["parent_id"] else "unknown"
            entry["flags"].append("entry_kind_uncertain")
        if entry["kind_candidate"] == "article" or "bundle_or_article" in entry["flags"]:
            candidates.append({
                "schema_version": SCHEMA_VERSION,
                "id": entry["id"].replace("-toc-", "-article-"),
                "toc_entry_id": entry["id"], "issue_id": entry["issue_id"],
                **{key: entry[key] for key in (
                    "title_candidate", "byline_candidate", "contributor_candidates",
                    "page_candidates", "start_page_candidate", "end_page_candidate", "section_path",
                )},
                "verification_status": "unreviewed", "source_matches": [], "summary": None,
                "flags": entry["flags"].copy(),
            })
        del entry["_parent"], entry["_ancestors"]
    return candidates


def validate_schema(name, instance):
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator({"$ref": f"#/$defs/{name}", "$defs": schema["$defs"]})
    problems = sorted(validator.iter_errors(instance), key=lambda e: str(list(e.path)))
    if problems:
        raise ValueError(f"{name} schema: {list(problems[0].path)}: {problems[0].message}")


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(data)
            stream.flush()
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def run_import(source, output, identities_path, *, decisions_path=None, start="1983-11", end="1990-12"):
    source, output, identities_path = Path(source), Path(output), Path(identities_path)
    expected = month_range(start, end)
    raw = source.read_bytes()
    source_hash = hashlib.sha256(raw).hexdigest()
    source_id = f"toc-sha256-{source_hash}"
    errors = []
    try:
        issues, entries, errors = parse_toc(raw.decode("utf-8"), source_id)
    except UnicodeDecodeError as exc:
        issues, entries = [], []
        errors.append(notice("invalid_utf8", byte_offset=exc.start))
    actual = [issue["id"] for issue in issues]
    for issue_id in sorted(set(expected) - set(actual)):
        errors.append(notice("missing_issue", issue_id=issue_id))
    for issue_id in sorted(set(actual) - set(expected)):
        errors.append(notice("out_of_scope_issue", issue_id=issue_id))
    if actual != sorted(actual):
        errors.append(notice("issue_order_mismatch"))
    populated = {entry["issue_id"] for entry in entries}
    for issue_id in sorted(set(actual) - populated):
        errors.append(notice("empty_issue", issue_id=issue_id))

    previous = {}
    decisions = {}
    try:
        if not identities_path.exists() and (output / "manifest.json").exists():
            raise ValueError("Identity registry is missing for an existing import; restore it before reimporting")
        if identities_path.exists():
            previous = json.loads(identities_path.read_text(encoding="utf-8"))
            validate_schema("identities", previous)
            previous_ids = [entry["id"] for entry in previous["entries"]]
            if len(previous_ids) != len(set(previous_ids)):
                raise ValueError("Identity registry contains duplicate IDs")
            if set(previous_ids) & set(previous["retired_ids"]):
                raise ValueError("Identity registry reuses a retired ID")
            for entry in previous["entries"]:
                if entry["id"].rsplit("-toc-", 1)[0] != entry["issue_id"]:
                    raise ValueError(f"Identity belongs to a different issue: {entry['id']}")
            for identifier in previous_ids + previous["retired_ids"]:
                issue_id, serial = identifier.rsplit("-toc-", 1)
                if previous["next_serial"].get(issue_id, 1) <= int(serial):
                    raise ValueError(f"Identity allocator would reuse {identifier}")
        if decisions_path:
            decisions = json.loads(Path(decisions_path).read_text(encoding="utf-8"))
            validate_schema("decisions", decisions)
            if decisions["source_sha256"] != source_hash:
                raise ValueError("Identity decisions refer to a different TOC revision")
    except ValueError as exc:
        errors.append(notice("invalid_identity_input", message=str(exc)))

    registry = None if errors else assign_identities(entries, previous, decisions, errors)
    if errors:
        atomic_write(output / "failed-import-report.json", json_bytes({
            "schema_version": SCHEMA_VERSION, "source_sha256": source_hash, "errors": errors,
        }))
        raise ImportFailure(f"{len(errors)} validation/identity errors")

    candidates = finalize_entries(entries)
    for issue in issues:
        if "maso-1983-11" <= issue["id"] <= "maso-1987-12":
            issue["coverage"]["body"] = "awaiting_scan"
    diagnostics = [
        notice(flag, entry["source"]["line_start"], entry_id=entry["id"])
        for entry in entries for flag in entry["flags"]
    ]
    by_title = defaultdict(list)
    for entry in entries:
        by_title[(entry["issue_id"], entry["title_candidate"])].append(entry)
    for repeated in by_title.values():
        if len(repeated) > 1:
            diagnostics.append(notice("repeated_title", entry_ids=[e["id"] for e in repeated]))
    report = {
        "schema_version": SCHEMA_VERSION, "source_sha256": source_hash, "errors": [],
        "counts": {
            "issues": len(issues), "entries": len(entries), "article_candidates": len(candidates),
            "diagnostics": len(diagnostics),
            "entries_without_page_marker": sum(e["page_reference_raw"] is None for e in entries),
            "by_kind": dict(sorted(Counter(e["kind_candidate"] for e in entries).items())),
            "by_diagnostic": dict(sorted(Counter(d["code"] for d in diagnostics).items())),
        },
        "issues": [
            {"issue_id": issue["id"], "entries": sum(e["issue_id"] == issue["id"] for e in entries),
             "article_candidates": sum(c["issue_id"] == issue["id"] for c in candidates),
             "coverage": issue["coverage"]}
            for issue in issues
        ],
        "diagnostics": diagnostics,
    }
    # Local discovery preview, deliberately not a publication export. Every TOC
    # entry is searchable, including uncertain headings and page-less subtopics.
    search = [{
        "id": entry["id"], "issue_id": entry["issue_id"],
        "title": entry["title_candidate"], "byline": entry["byline_candidate"],
        "pages": entry["page_candidates"], "kind_candidate": entry["kind_candidate"],
        "verification_status": "unreviewed",
        "search_text": unicodedata.normalize("NFC", " ".join(filter(None, (
            entry["title_candidate"], entry["byline_candidate"], entry["issue_id"].removeprefix("maso-"),
        )))).casefold(),
    } for entry in entries]

    bundle = {"issues": issues, "entries": entries, "candidates": candidates,
              "report": report, "identities": registry, "search": search}
    validate_schema("bundle", bundle)
    issue_ids = {i["id"] for i in issues}
    entry_ids = {e["id"] for e in entries}
    if len(entry_ids) != len(entries):
        raise ValueError("Duplicate entry IDs after reconciliation")
    for entry in entries:
        if entry["issue_id"] not in issue_ids or (entry["parent_id"] and entry["parent_id"] not in entry_ids):
            raise ValueError(f"Broken relationship: {entry['id']}")

    def jsonl(records):
        return "".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in records).encode("utf-8")

    outputs = {
        "issues.json": json_bytes(issues),
        "toc-entries.jsonl": jsonl(entries),
        "article-candidates.jsonl": jsonl(candidates),
        "validation-report.json": json_bytes(report),
        "local-search.json": json_bytes(search),
    }
    manifest = {
        "schema_version": SCHEMA_VERSION, "importer_version": __version__,
        "python_version": platform.python_version(),
        "jsonschema_version": importlib.metadata.version("jsonschema"),
        "source": {"name": source.name, "sha256": source_hash, "bytes": len(raw)},
        "parameters": {"start": start, "end": end},
        "schema_sha256": hashlib.sha256(SCHEMA_PATH.read_bytes()).hexdigest(),
        "identities_sha256": hashlib.sha256(json_bytes(registry)).hexdigest(),
        "outputs": {name: {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)} for name, data in outputs.items()},
    }
    for name, data in outputs.items():
        atomic_write(output / name, data)
    atomic_write(output / "manifest.json", json_bytes(manifest))
    atomic_write(identities_path, json_bytes(registry))
    (output / "failed-import-report.json").unlink(missing_ok=True)
    return report
