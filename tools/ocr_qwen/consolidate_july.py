"""Reconcile July diagnostics, native local usage and observed paid work windows.

Run with PYTHONPATH=src:. python3 -m tools.ocr_qwen.consolidate_july.
Private inputs are required; outputs contain only metrics and evidence pins.
"""
from collections import Counter, defaultdict
import json
import statistics

from .consolidate import ROOT, ENGINES, pin, pooled, read, unique_responses, usage


def paired_times(rows):
    paired = [r for r in rows if all(r.get(e + '_seconds') is not None for e in ENGINES)]
    engines = {e: dict(seconds=sum(r[e + '_seconds'] for r in paired),
                       median_seconds=statistics.median(r[e + '_seconds'] for r in paired))
               for e in ENGINES}
    return dict(crops=len(paired), omitted=[dict(batch=r['batch'], region_id=r['region_id'])
                                          for r in rows if r not in paired], engines=engines,
                qwen_to_tesseract_time_ratio=engines['qwen']['seconds'] / engines['tesseract']['seconds'],
                scope='Matched crop calls, excluding startup, rendering, preparation and correction. Missing either timer excludes both engines from the pair.')


def window_totals(windows):
    keys = ('input_tokens', 'cached_input_tokens', 'cache_write_input_tokens',
            'uncached_nonwrite_input_tokens', 'output_tokens', 'reasoning_output_tokens', 'total_tokens')
    return dict(windows=len(windows), elapsed_seconds=sum(w['elapsed_seconds'] for w in windows),
                observed_responses=sum(w['observed_responses'] for w in windows),
                windows_without_observed_usage=[w['id'] for w in windows if not w['tokens']],
                observed_tokens={k: sum((w['tokens'] or {}).get(k) or 0 for w in windows) for k in keys})


def build(root=ROOT):
    docs = root / 'docs'
    private = root / 'private/pdf-restoration/12-1984-07-comparison'
    progress, paid = (read(docs / f'ocr-july-{name}.json') for name in ('progress', 'usage'))
    assert progress['completed_article_bodies'] == 36 and progress['remaining_article_bodies'] == 0
    files = sorted(docs.glob('ocr-july-comparison-*.json'))
    assert len(files) == 52
    comparisons = [(p, read(p)) for p in files]
    body = [r for p, d in comparisons if p.name != 'ocr-july-comparison-52.json' for r in d['rows']]
    index = comparisons[-1][1]['rows']
    rows = body + index
    assert len(rows) == len({r['image']['sha256'] for r in rows}) == 210
    accuracy = dict(body_text=pooled(body),
                    by_category={k: pooled([r for r in body if r['category'] == k]) for k in sorted({r['category'] for r in body})},
                    index_leader_normalized=pooled(index),
                    tesseract_lower_crops=[dict(batch=r['batch'], region_id=r['region_id'], category=r['category']) for r in body
                                           if r['engines']['tesseract']['cer_no_whitespace'] < r['engines']['qwen']['cer_no_whitespace']],
                    method='Micro-average: summed edits / summed reference characters. Compact CER removes whitespace. Index52 normalizes decorative leaders and is separate.',
                    limitation='Purposive single-run crops; unblinded assistant source references, not independent human gold or whole-issue accuracy. No post-correction error-rate or executable-code claim.')
    checkpoints = progress['checkpoints']
    responses, copies = unique_responses(p for d in private.glob('batch-*') for p in d.rglob('inference.response.json'))
    local_batches = []
    for c in checkpoints:
        captured = [r for p, r in responses.values() if p.relative_to(private).parts[0] == 'batch-' + c['batch']]
        expected = c.get('local_qwen_tokens') or c.get('local_qwen_tokens_completed_responses_lower_bound')
        if c['engine'] == 'tesseract':
            assert expected is None and not captured
            expected = dict.fromkeys(('prompt_tokens', 'completion_tokens', 'total_tokens'), 0)
        assert expected is not None and usage(captured) == {k: expected[k] for k in usage(captured)}
        local_batches.append(dict(batch=c['batch'], engine=c['engine'], captured_calls=len(captured),
                                  tokens=usage(captured), completeness='exact-recorded-attempts' if c.get('local_qwen_tokens') or c['engine'] == 'tesseract' else 'lower-bound-interrupted-work',
                                  raw_run_seconds=c['raw_run_seconds'],
                                  raw_lower_bound=c.get('raw_run_seconds_lower_bound'), raw_upper_bound=c.get('raw_run_seconds_upper_bound'),
                                  contaminated_raw_wall_seconds=c.get('contaminated_raw_wall_seconds'),
                                  limitation=c.get('recognition_limitation')))
    exact = [c for c in checkpoints if c['raw_run_seconds'] is not None]
    bounded = [c for c in checkpoints if c.get('raw_run_seconds_lower_bound') is not None]
    local = dict(unique_response_calls=len(responses), copied_response_files_ignored=copies,
                 captured_tokens_lower_bound=usage([r for _, r in responses.values()]),
                 finish_reasons=dict(Counter(r['choices'][0]['finish_reason'] for _, r in responses.values())),
                 by_batch=local_batches,
                 scope='Primary batch responses, including failed and superseded attempts; copied completion IDs counted once. Alternate-engine evaluation excluded. Uncaptured interrupted generation is unknown, so aggregate is a lower bound.')
    alternates, alternate_copies = unique_responses(p for d in private.glob('comparison-*') for p in d.rglob('*.response.json'))
    assert not (responses.keys() & alternates.keys())
    local['alternate_evaluation'] = dict(captured_calls=len(alternates), copied_files_ignored=alternate_copies,
        tokens=usage([r for _, r in alternates.values()]),
        finish_reasons=dict(Counter(r['choices'][0]['finish_reason'] for _, r in alternates.values())),
        scope='Separately captured alternate Qwen calls; not part of primary restoration tokens.')
    timing = dict(exact_recorded_batches=len(exact), exact_recorded_seconds=sum(c['raw_run_seconds'] for c in exact),
                  bounded_batches=len(bounded), bounded_seconds_lower=sum(c['raw_run_seconds_lower_bound'] for c in bounded),
                  bounded_seconds_upper=sum(c['raw_run_seconds_upper_bound'] for c in bounded),
                  contaminated_batches=[dict(batch=c['batch'], seconds=c['contaminated_raw_wall_seconds']) for c in checkpoints if c.get('contaminated_raw_wall_seconds')],
                  known_raw_correction_overlap_seconds=sum(c.get('correction_raw_overlap', {}).get('raw_overlap_seconds', 0) for c in checkpoints),
                  scope='Worker timers include startup/rendering/validation/export; recognition is nested. Bounds include recovery uncertainty. Batch24 competing-model contamination excluded from clean timing. Raw and work windows overlap; never add these totals.')
    stages = defaultdict(list)
    for w in paid['windows']:
        stages[w['stage']].append(w)
    paid_summary = dict(observed_span=paid['observed_trial_span'], between_windows=paid['between_window_usage'],
                        all_named_windows=window_totals(paid['windows']), by_stage={k: window_totals(v) for k, v in stages.items()},
                        correction_labeled_windows=window_totals([w for w in paid['windows'] if 'correction' in w['stage']]),
                        evaluation_labeled_windows=window_totals([w for w in paid['windows'] if 'evaluation' in w['stage'] or w['stage'] in ('paired-diagnostics', 'fixed-crop-comparison')]),
                        limitation='Response-completion timestamps allocate whole responses to nonoverlapping work windows. Elapsed windows include tool waits, transcription and helper work; source reading also occurs in preparation. No-observation windows are unknown, not free. Reasoning is a subset of output. Span and gaps include idle time. Not a bill, or a causal engine comparison; June paid usage and human review time are unknown.')
    snapshot_path = private / 'restoration-usage-snapshot.json'
    snapshot = read(snapshot_path)
    paid_summary['restoration_cutoff_snapshot'] = dict(evidence=pin(snapshot_path, root),
        observed_span=snapshot['observed_trial_span'], between_windows=snapshot['between_window_usage'],
        all_named_windows=window_totals(snapshot['windows']),
        scope='Frozen restoration cutoff before consolidation and reading-room delivery; decision document quotes this scope.')
    for k, v in paid_summary['all_named_windows']['observed_tokens'].items():
        assert v + paid['between_window_usage']['tokens'][k] == paid['observed_trial_span']['tokens'][k]
    packages = [read(root / e['restoration']['path']) for e in progress['entries'] if e.get('restoration')]
    counts = dict(articles=len(packages), checkpoints=len(checkpoints), toc_entries=progress['canonical_toc_entries'],
                  group_headings=progress['section_heading_entries'], human_accepted=0,
                  unique_source_pages=len({p['pdf_index'] for a in packages for p in a['pages']}),
                  regions=sum(len(a['regions']) for a in packages), figures=sum(len(a['figures']) for a in packages),
                  engine_checkpoints=dict(Counter(c['engine'] for c in checkpoints)))
    return dict(schema_version=1, issue_id='maso-1984-07', counts=counts, accuracy=accuracy,
                paired_raw_timing=paired_times(rows), local_primary=local, raw_timing=timing, paid_work=paid_summary,
                evidence=[pin(p, root) for p in [docs / 'ocr-july-progress.json', docs / 'ocr-july-usage.json', *files]],
                decision='Continue provisional content routing, source correction and human review. Favor Qwen for dense Korean, code and structured content; retain cheap Tesseract probes for simple text and judge observed failures. Raw accuracy advantage is supported; reduced paid correction cost is not causally established.')


if __name__ == '__main__':
    result = build()
    destination = ROOT / 'docs/ocr-july-metrics.json'
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('counts', 'paired_raw_timing', 'raw_timing')}, indent=2))
