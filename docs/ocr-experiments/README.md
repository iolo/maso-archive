# OCR experiment data

This directory holds the public, machine-readable evidence for the OCR benchmark,
workflow trial, June and July comparisons, and August pilot and production work.
The human-readable reports and current workflow guidance remain in the parent
`docs` directory. Start with [the OCR handoff](../../PLAN-OCR.md) for current
policy, or [the workflow reference](../OCR-WORKFLOW.md) for the optional A/B/C
experiment.

| Files | Contents |
| --- | --- |
| `ocr-qwen3-vl-benchmark.json`, `ocr-workflow-measurements.json` | Initial benchmark and A/B/C workflow measurements |
| `ocr-june-*.json` | June checkpoint ledger, comparisons, accounting and metrics |
| `ocr-july-*.json` | July checkpoint ledger, 52 comparisons, usage, accounting and metrics |
| `ocr-august-pilot-*.json` | August pilot selection, progress, correction usage and results |
| `ocr-august-*.json` | August production progress and usage |

These files moved here without changing their contents. Some historical JSON
records contain repository paths from before this move. For a `docs/ocr-*.json`
path inside those records, find the same filename in this directory; hashes and
measurements still refer to the original bytes.
