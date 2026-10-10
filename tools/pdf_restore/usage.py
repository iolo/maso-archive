"""Attribute observed assistant usage to explicit, non-overlapping work windows.

Reads only token_usage_record rows from a supplied local session log. Does not
export transcript text, infer billing, or confuse local OCR tokens with paid work.
"""
import argparse
from datetime import datetime
import json
from pathlib import Path


FIELDS = ('input_tokens', 'cached_input_tokens', 'cache_write_input_tokens',
          'output_tokens', 'reasoning_output_tokens', 'total_tokens')


def epoch(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Usage windows require timezone-aware timestamps')
    return parsed.timestamp()


def records(path):
    seen = {}
    with Path(path).open('rb') as stream:
        for line in stream:
            if b'"token_usage_record"' not in line:
                continue
            row = json.loads(line)
            if row.get('type') != 'token_usage_record':
                continue
            payload = row['payload']
            key = payload['response_id']
            value = dict(timestamp=row['timestamp'], usage=payload['usage'])
            if key in seen and seen[key]['usage'] != value['usage']:
                raise ValueError('Conflicting usage records for the same response')
            seen.setdefault(key, value)
    return list(seen.values())


def summarize(rows, windows):
    ordered = sorted(windows, key=lambda w: epoch(w['start']))
    ids = [w['id'] for w in ordered]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate work-window ID')
    previous_end = None
    result = []
    for window in ordered:
        start, end = epoch(window['start']), epoch(window['end'])
        if end <= start or (previous_end is not None and start < previous_end):
            raise ValueError('Work windows must be positive and non-overlapping')
        previous_end = end
        selected = [r['usage'] for r in rows if start <= epoch(r['timestamp']) < end]
        totals = None
        if selected:
            # An absent field is unknown, never silently zero.
            totals = {k: sum(u[k] for u in selected) if all(k in u for u in selected)
                      else None for k in FIELDS}
            for usage in selected:
                if any(v < 0 for k, v in usage.items() if k in FIELDS):
                    raise ValueError('Negative token count')
                if all(k in usage for k in ('input_tokens', 'output_tokens', 'total_tokens')):
                    if usage['input_tokens'] + usage['output_tokens'] != usage['total_tokens']:
                        raise ValueError('Token totals do not reconcile')
                if all(k in usage for k in FIELDS[:3]):
                    if usage['cached_input_tokens'] + usage['cache_write_input_tokens'] > usage['input_tokens']:
                        raise ValueError('Input subsets exceed input tokens')
                if all(k in usage for k in ('reasoning_output_tokens', 'output_tokens')):
                    if usage['reasoning_output_tokens'] > usage['output_tokens']:
                        raise ValueError('Reasoning subset exceeds output tokens')
            totals['uncached_nonwrite_input_tokens'] = (
                totals['input_tokens'] - totals['cached_input_tokens'] - totals['cache_write_input_tokens']
                if all(totals[k] is not None for k in FIELDS[:3]) else None)
        result.append(dict(**window, elapsed_seconds=end-start,
                           observed_responses=len(selected), tokens=totals))
    return dict(schema_version=1, windows=result, money_cost=None,
                policy='Observed usage by response completion timestamp in [start,end). '
                       'A boundary-straddling response is attributed wholly to its completion window. '
                       'Cached/write input and reasoning output are subsets; do not add them twice. '
                       'No observed records means unknown, not free work. Missing or delayed usage '
                       'may require a later audit. Elapsed windows include tool waits. '
                       'These observations are not a bill or causal engine savings estimate.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session-log', type=Path, required=True)
    parser.add_argument('--windows', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = audit(records(args.session_log), json.loads(args.windows.read_bytes()))
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')


def audit(rows, windows):
    report = summarize(rows, windows)
    if not report['windows']:
        return report
    first, last = report['windows'][0], report['windows'][-1]
    span = dict(id='observed-trial-span', start=first['start'], end=last['end'])
    whole = summarize(rows, [span])['windows'][0]
    unallocated = [r for r in rows if not any(
        epoch(w['start']) <= epoch(r['timestamp']) < epoch(w['end']) for w in windows)]
    remainder = summarize(unallocated, [span])['windows'][0]
    report['observed_trial_span'] = whole
    report['between_window_usage'] = remainder
    report['coverage_note'] = ('Between-window records remain visible as unattributed overhead. '
        'Span elapsed includes gaps and is not active correction time. Records outside the span '
        'are excluded. The last report/commit response may need the next audit.')
    return report


if __name__ == '__main__':
    main()
