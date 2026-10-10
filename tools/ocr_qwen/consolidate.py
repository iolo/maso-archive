"""Consolidate June diagnostics without rerunning OCR or inferring human savings.

Run from the repository root with PYTHONPATH=src:. python3 -m tools.ocr_qwen.consolidate.
Private retained responses are required for the retry/token audit. Outputs contain
metrics and hashes only, never OCR transcriptions or image data.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[2]
ENGINES = ('qwen', 'tesseract')


def read(path):
    return json.loads(path.read_bytes())


def pin(path, root=ROOT):
    data = path.read_bytes()
    return dict(path=path.relative_to(root).as_posix(), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))


def pooled(rows):
    """Micro-average edit counts; never average crop percentages or mix cell scores."""
    out = dict(crops=len(rows), engines={})
    for engine in ENGINES:
        scores = [r['engines'][engine] for r in rows]
        summary = {}
        for metric in ('cer', 'cer_no_whitespace'):
            edits = sum(s[metric + '_edits'] for s in scores)
            chars = sum(s[metric + '_reference_chars'] for s in scores)
            summary[metric] = dict(edits=edits, reference_characters=chars, rate=edits / chars if chars else None)
        out['engines'][engine] = summary
    for metric in ('cer', 'cer_no_whitespace'):
        assert out['engines']['qwen'][metric]['reference_characters'] == out['engines']['tesseract'][metric]['reference_characters']
    out['compact_crop_outcomes'] = dict(Counter(
        'qwen_lower' if r['engines']['qwen']['cer_no_whitespace'] < r['engines']['tesseract']['cer_no_whitespace'] else
        'tesseract_lower' if r['engines']['qwen']['cer_no_whitespace'] > r['engines']['tesseract']['cer_no_whitespace'] else 'tie'
        for r in rows))
    return out


def unique_responses(paths):
    """Copied caches retain completion IDs; distinct reruns retain distinct IDs."""
    unique = {}
    duplicates = 0
    for path in sorted(paths):
        response = read(path)
        key = response['id']
        if key in unique:
            if unique[key][1] != response:
                raise ValueError(f'Conflicting completion ID: {path}')
            duplicates += 1
        else:
            unique[key] = (path, response)
    return unique, duplicates


def usage(responses):
    counts = {key: sum(r['usage'][key] for r in responses) for key in ('prompt_tokens', 'completion_tokens', 'total_tokens')}
    assert counts['prompt_tokens'] + counts['completion_tokens'] == counts['total_tokens']
    return counts


def build(root=ROOT):
    docs = root / 'docs'
    private = root / 'private/pdf-restoration/12-1984-06-qwen'
    progress = read(docs / 'ocr-june-progress.json')
    files = sorted(docs.glob('ocr-june-batch*-comparison.json'))
    assert len(files) == 38
    comparisons = [(p, read(p)) for p in files]
    rows = [dict(row, batch=int(p.name.split('batch')[1].split('-')[0])) for p, doc in comparisons for row in doc['rows']]
    # Exact source PNG identity must be unique in this primary comparison cohort.
    assert len({r['image']['sha256'] for r in rows}) == len(rows)
    cer_rows = [r for r in rows if 'cer' in r['engines']['qwen']]
    body_rows = [r for r in cer_rows if r['batch'] != 41]
    accuracy = dict(
        method='Sum edits / sum reference characters (micro-average). NFC-normalized; standard CER collapses whitespace, compact CER removes it. Neither certifies executable code.',
        reference='Purposive, single-run crops with unblinded assistant-corrected Qwen-derived references fixed before Tesseract. Not independent human gold or representative whole-issue accuracy.',
        body_text=pooled(body_rows),
        by_category={kind: pooled([r for r in body_rows if r['category'] == kind]) for kind in ('prose', 'code', 'other')},
        including_index_primary=pooled(cer_rows),
        index_primary=pooled([r for r in cer_rows if r['batch'] == 41]),
        index_supplemental=pooled(comparisons[-1][1]['supplemental_leader_normalized']['rows']),
        index_policy=comparisons[-1][1]['supplemental_leader_normalized']['policy'],
    )
    cell_rows = [r for r in rows if 'matched_cells' in r['engines']['qwen']]
    accuracy['phoneme_table_cells'] = dict(crops=len(cell_rows), excluded_ambiguous_cells=sum(len(r['engines']['qwen']['excluded_candidate_cells']) for r in cell_rows), engines={
        e: dict(matched=sum(r['engines'][e]['matched_cells'] for r in cell_rows), total=sum(r['engines'][e]['compared_cells'] for r in cell_rows)) for e in ENGINES})
    accuracy['phoneme_table_cells']['tesseract_english_sensitivity'] = dict(matched=sum(r['matched_cells'] for r in comparisons[0][1]['table_language_sensitivity']), total=sum(r['compared_cells'] for r in comparisons[0][1]['table_language_sensitivity']))
    numbered = [r for r in rows if 'reference_numbered_rows' in r['engines']['qwen']]
    accuracy['literal_sensitive_numbered_rows'] = dict(crops=len(numbered), scope='Only batch05–06 assembly samples; whitespace within single-quoted literals retained. Not all June code.', engines={
        e: dict(exact=sum(r['engines'][e]['literal_sensitive_exact_numbered_rows'] for r in numbered), total=sum(r['engines'][e]['reference_numbered_rows'] for r in numbered)) for e in ENGINES})
    paired = dict(crops=len(rows), scope='Primary matched crops, including two cell-scored tables and three index crops; no extra language reruns. Qwen inference versus Tesseract engine calls, excluding common layout/rendering, Qwen startup and later correction.', engines={})
    for e in ENGINES:
        times = [r[e + '_seconds'] for r in rows]
        paired['engines'][e] = dict(seconds=sum(times), median_seconds=statistics.median(times), peak_rss_mib_sampled=max(r[e + '_resources']['peak_rss_mib_sampled'] for r in rows), peak_gpu_mib_sampled=max((r[e + '_resources']['peak_gpu_mib_sampled'] for r in rows if r[e + '_resources']['peak_gpu_mib_sampled'] is not None), default=None))
    paired['qwen_to_tesseract_time_ratio'] = paired['engines']['qwen']['seconds'] / paired['engines']['tesseract']['seconds']

    final_ids = set()
    final_stages = []
    stage_pins = []
    batches = []
    timing_files = []
    for n in range(1, 42):
        batch = private / (f'batch-{n:02}' + ('-corrected' if n in (1, 4) else ''))
        stages = []
        responses = []
        for path in sorted(batch.glob('ocr/stages/*/*/result.json')):
            response = read(path.parent / 'inference.response.json')
            assert (path.parent / 'done.json').exists() and response['choices'][0]['finish_reason'] == 'stop'
            assert response['id'] not in final_ids
            final_ids.add(response['id'])
            result = read(path)
            stage_pins.append(pin(path, root))
            assert result['inference']['usage'] == response['usage']
            stages.append(result)
            responses.append(response)
        assert stages
        final_stages.extend(stages)
        row = dict(monitored_stage_seconds=sum(s['resources']['wall_seconds'] for s in stages), batch=f'batch-{n:02}', retained_calls=len(stages), inference_seconds=sum(s['inference']['seconds'] for s in stages), tokens=usage(responses), peak_gpu_mib_sampled=max(s['resources']['peak_gpu_mib_sampled'] or 0 for s in stages), peak_rss_mib_sampled=max(s['resources']['peak_rss_mib_sampled'] for s in stages))
        timer = batch / 'raw-run-timing.json'
        row['recorded_run_seconds'] = None
        if timer.exists():
            record = read(timer)
            row.update(recorded_run_seconds=record['elapsed_seconds'], run_timer_scope=record['scope'])
            timing_files.append(timer)
        batches.append(row)
    # Independently reconcile retained calls/tokens with the recorded checkpoints.
    checkpoints = progress['checkpoints']
    expected = {1: checkpoints[0]['successful_run'],
                4: checkpoints[2]['metrics']['batch-04-corrected'],
                5: checkpoints[3]['metrics'], 6: checkpoints[4]['metrics']}
    expected.update({int(s['batch'][-2:]): s['metrics'] for s in checkpoints[1]['segments']})
    expected.update({int(c['batch'][-2:]): c['metrics'] for c in checkpoints if c.get('batch')})
    assert set(expected) == set(range(1, 42))
    for row in batches:
        record = expected[int(row['batch'][-2:])]
        assert row['retained_calls'] == record['calls']
        assert row['tokens']['prompt_tokens'] == record['local_prompt_tokens']
        assert row['tokens']['completion_tokens'] == record['local_output_tokens']
        if 'inference_wall_seconds' in record:
            row['checkpoint_reported_seconds'] = record['inference_wall_seconds']
            if math.isclose(row['inference_seconds'], record['inference_wall_seconds']):
                row['checkpoint_timer_basis'] = 'inference.seconds'
            else:
                assert math.isclose(row['monitored_stage_seconds'], record['inference_wall_seconds'])
                row['checkpoint_timer_basis'] = 'resources.wall_seconds mislabeled as inference_wall_seconds'
        else:
            assert math.isclose(row['monitored_stage_seconds'], record['preparation_seconds'])
            row['checkpoint_reported_seconds'] = record['preparation_seconds']
            row['checkpoint_timer_basis'] = 'resources.wall_seconds labeled preparation_seconds; not full preparation'
    # Original batch04 was a separate complete run. Do not also add component
    # recovery timers already included in each batch's combined raw-run-timing.
    timing_files.append(private / 'batch-04/raw-run-timing.json')
    unique, copies = unique_responses(private.glob('batch-*/ocr*/stages/*/*/inference.response.json'))
    assert final_ids <= unique.keys()
    all_responses = [r for _, r in unique.values()]
    retained = [r for _, r in unique.values() if r['id'] in final_ids]
    extra = [r for _, r in unique.values() if r['id'] not in final_ids]
    failures = [(p, r) for p, r in unique.values() if r['choices'][0]['finish_reason'] != 'stop']
    c32 = next(c for c in progress['checkpoints'] if c.get('batch') == 'batch-32')
    interruption = c32['metrics']['interrupted_server_total_tokens']
    audit_rows = [dict(source=pin(p, root), completion_id=r['id'], finish_reason=r['choices'][0]['finish_reason'], usage=r['usage'], retained=r['id'] in final_ids) for p, r in unique.values()]
    audit_bytes = json.dumps(audit_rows, sort_keys=True, ensure_ascii=False).encode()
    inference_seconds = sum(s['inference']['seconds'] for s in final_stages)
    local = dict(retained_calls=len(retained), retained_inference_seconds=inference_seconds, retained_tokens=usage(retained), unique_response_calls=len(unique), duplicate_cached_response_files_ignored=copies, all_response_tokens=usage(all_responses), additional_response_tokens=usage(extra), additional_response_calls=len(extra), interrupted_request_tokens_without_response=interruption, observed_tokens_including_interrupted_request=usage(all_responses)['total_tokens'] + interruption, token_completeness='Observed June inference responses plus separately logged interrupted request; excludes earlier pilot experiments. Unlogged/uncaptured work, if any, is not estimated.', audit_sha256=hashlib.sha256(audit_bytes).hexdigest(), retained_stage_evidence_sha256=hashlib.sha256(json.dumps(stage_pins,sort_keys=True).encode()).hexdigest(), failed_response_count=len(failures), failures=[dict(source=pin(p, root), finish_reason=r['choices'][0]['finish_reason'], tokens=r['usage']['total_tokens'], server_seconds=(r['timings']['prompt_ms'] + r['timings']['predicted_ms']) / 1000) for p, r in failures], peak_gpu_mib_sampled=max(s['resources']['peak_gpu_mib_sampled'] or 0 for s in final_stages), peak_rss_mib_sampled=max(s['resources']['peak_rss_mib_sampled'] for s in final_stages), mean_retained_inference_seconds_per_source_page=inference_seconds / progress['counts']['processed_source_pages'], mean_retained_local_tokens_per_source_page=usage(retained)['total_tokens'] / progress['counts']['processed_source_pages'], recorded_run_segments_seconds=sum(read(p)['elapsed_seconds'] for p in timing_files), recorded_run_segments=[pin(p, root) for p in timing_files], full_preparation_seconds=None, timing_gaps=['Batches01–03 have no full-run timer; batch01 preparation_seconds in the old checkpoint is summed monitored stage time, not full preparation.', 'Superseded/aborted passes in batches20 and23 are not covered by the final-run timers.', 'Batches28 and32 timers cover recovery only; earlier pass wall time is unavailable.', 'Do not add retained inference time to run timers: they overlap. Layout mapping, semantic correction, assembly and human review are outside raw-run timers.'], by_batch=batches)
    # Per-batch retry audit reveals superseded work instead of hiding it in caches.
    assert len(final_ids) + len(extra) == len(unique)
    assert usage(retained)['total_tokens'] + usage(extra)['total_tokens'] == usage(all_responses)['total_tokens']
    for row in batches:
        n=int(row['batch'][-2:]); extra_batch=[r for p,r in unique.values() if int(p.relative_to(private).parts[0][6:8])==n and r['id'] not in final_ids]
        row['additional_response_calls']=len(extra_batch)
        row['additional_response_tokens']=usage(extra_batch)
    pilot = read(docs / 'ocr-workflow-measurements.json')
    pilot_out = dict(scope='Earlier three-page A/B/C development test; separate corpus and scoring, not pooled with June.', arms={}, samples=[])
    for arm in ('A-tesseract', 'B-qwen', 'C-local-correction'):
        rs=[r for r in pilot['rows'] if r['arm']==arm]
        pilot_out['arms'][arm]=dict(preparation_seconds=sum(r['preparation_seconds'] for r in rs),local_tokens=sum(r['local_tokens']['total_tokens'] for r in rs))
    for sample in ('prose','basic','figures'):
        pilot_out['samples'].append(dict(sample=sample,compact_cer={r['arm']:r['accuracy_proxy']['cer_no_whitespace'] for r in pilot['rows'] if r['sample']==sample}))
    pilot_out['limits']=pilot['limits']
    return dict(schema_version=1, issue_id='maso-1984-06', scope=progress['counts'], inputs=[pin(docs/'ocr-june-progress.json',root),pin(docs/'ocr-workflow-measurements.json',root),*[pin(p,root) for p,_ in comparisons]], accuracy=accuracy, paired_engine_comparison=paired, local_compute=local, earlier_three_page_pilot=pilot_out, unmeasured=dict(capable_model_input_tokens=None,capable_model_cached_input_tokens=None,capable_model_output_tokens=None,capable_model_cost=None,human_active_review_seconds=None,semantic_correction_seconds=None,full_workflow_elapsed_seconds=None,energy_kwh=None,whole_issue_tesseract_runtime=None,human_gold_accuracy=None), notes=['Local Qwen tokens include image/prompt tokens and generated text, not paid assistant tokens. Tesseract itself consumes no LLM tokens; its downstream correction token use is unknown.', 'Sampled process-tree RSS includes shared mappings and is not a physical-RAM requirement. GPU peaks are sampled allocations, not energy measurements.', 'Crop selection and references are unblinded; failures, omissions and graphic placeholders outside scored crops prevent treating CER as final accuracy.', 'This report reads existing evidence only; no new inference, acceptance or pipeline-default change.'])


def markdown(report):
    a=report['accuracy']; c=report['local_compute']; t=report['paired_engine_comparison']; p=report['earlier_three_page_pilot']
    pct=lambda x:f'{100*x:.2f}%'
    rate=lambda row,e,metric='cer_no_whitespace':pct(row['engines'][e][metric]['rate'])
    lines=['# June 1984 OCR decision report', '',
        '**Recommendation: use Qwen3-VL as the preferred raw-OCR option for the next issue, retain the existing semantic correction and mandatory human review, and keep Tesseract available for fallback and selective comparisons.** The June evidence supports better raw transcription, especially code. It does not yet establish lower total project cost.', '',
        'Configuration: local Qwen3-VL-8B-Instruct UD-Q4_K_XL through llama.cpp, 8,192-token context and deterministic OCR decoding; Tesseract comparisons use pinned OEM1/PSM6, one thread, usually `eng` for code and `kor+eng` for prose. Settings and exact source crops remain pinned in each comparison.', '',
        'This is a consolidation of existing evidence, not a new benchmark. No pipeline default or acceptance state was changed. The issue contains 38 assembled article bodies across 216 source pages; all 45 contents entries are accounted for, including seven group headings. Human acceptance is still zero.', '',
        '## Accuracy: raw OCR against the assistant reference', '',
        'Lower character error rate (CER) is better. The primary table removes whitespace; rates are weighted by reference character count, not averaged across crops.', '',
        '| Content | Crops | Reference characters | Qwen compact CER | Tesseract compact CER |',
        '| --- | ---: | ---: | ---: | ---: |']
    for label,row in [*[(k.capitalize() if k!='other' else 'Tables / other text',v) for k,v in a['by_category'].items()],('Combined, excluding index',a['body_text']),('All CER crops, including index',a['including_index_primary'])]:
        lines.append(f"| {label} | {row['crops']} | {row['engines']['qwen']['cer_no_whitespace']['reference_characters']:,} | {rate(row,'qwen')} | {rate(row,'tesseract')} |")
    lines += ['',
        'The 97 non-index crops contain 423 Qwen character edits versus 4,890 Tesseract edits: **91.35% fewer reference edits in this selected sample**. Qwen has lower compact CER on 95 of these crops; Tesseract is better on two. Those exceptions are the code crop `p106r17` (65.27% vs 45.42%) and other-text crop `p181r19` (59.68% vs 54.84%). Both engines can fail badly on individual regions.', '',
        f"Whitespace-normalized CER, which retains word separators, is **{rate(a['body_text'],'qwen','cer')} vs {rate(a['body_text'],'tesseract','cer')}** across the same 97 crops. This also favors Qwen, but neither metric checks original literal spacing exactly.", '',
        '| Separate diagnostic | Qwen | Tesseract | Scope |', '| --- | ---: | ---: | --- |']
    cell=a['phoneme_table_cells']; code=a['literal_sensitive_numbered_rows']
    lines += [f"| Correct table cells | {cell['engines']['qwen']['matched']}/{cell['engines']['qwen']['total']} | {cell['engines']['tesseract']['matched']}/{cell['engines']['tesseract']['total']} | Two phoneme tables; eight ambiguous cells excluded |",
        f"| Exact numbered source rows | {code['engines']['qwen']['exact']}/{code['engines']['qwen']['total']} | {code['engines']['tesseract']['exact']}/{code['engines']['tesseract']['total']} | Five assembly crops; spaces inside quoted literals retained |", '',
        'The English-only Tesseract sensitivity run improves the table result to 265/312 cells; the primary comparison uses 260/312. These cell and row scores are not pooled with CER. This stricter code-row metric was not recorded for the other June comparison batches.', '',
        f"The three advertisement-index crops have primary compact CER **{rate(a['index_primary'],'qwen')} vs {rate(a['index_primary'],'tesseract')}** because the reference replaces decorative dotted leaders with table separators. A separately labeled, post-hoc calculation removes the same four punctuation characters from both engines and the reference: **{rate(a['index_supplemental'],'qwen')} vs {rate(a['index_supplemental'],'tesseract')}**. It leaves Tesseract's spurious letters/digits and omitted rows intact. CER can exceed 100% because insertions count. Both the original and supplemental scores are retained; the supplemental result is not substituted into the combined total.", '',
        '**Limit:** these are 102 purposively selected, single-run crops: 97 ordinary CER crops, three index crops and two cell-scored tables. References were fixed before Tesseract, but were assistant-corrected Qwen drafts and are unblinded. They are not independent human gold. Failed graphic crops and many other regions are not scored. Do not read 2.22% as the whole issue’s error rate, or subtract it from 100% to claim final transcription accuracy. Layout maps were reviewed before OCR; this does not validate unattended layout detection.', '',
        '## Time and resources', '',
        '| Same 102 primary crops | Qwen | Tesseract |', '| --- | ---: | ---: |',
        f"| Sum of engine-call time | {t['engines']['qwen']['seconds']:.2f} s | {t['engines']['tesseract']['seconds']:.2f} s |",
        f"| Median per crop | {t['engines']['qwen']['median_seconds']:.2f} s | {t['engines']['tesseract']['median_seconds']:.2f} s |",
        f"| Sampled peak process-tree RSS | {t['engines']['qwen']['peak_rss_mib_sampled']:,.0f} MiB | {t['engines']['tesseract']['peak_rss_mib_sampled']:,.0f} MiB |",
        f"| Sampled GPU allocation | {t['engines']['qwen']['peak_gpu_mib_sampled']:,.0f} MiB | CPU workflow; no sampled GPU allocation |", '',
        f"**Qwen was {t['qwen_to_tesseract_time_ratio']:.2f}× slower at raw recognition on these crops.** Its possible workflow advantage is less correction work, not faster OCR calls. That downstream advantage remains unmeasured. Timing excludes shared mapping/rendering, Qwen startup and later correction; no whole-issue Tesseract runtime was measured.", '',
        '| June Qwen work | Measured value |', '| --- | ---: |',
        f"| Retained successful OCR calls | {c['retained_calls']:,} |",
        f"| Their summed inference time | {c['retained_inference_seconds']/60:.2f} minutes |",
        f"| Mean retained inference per source page | {c['mean_retained_inference_seconds_per_source_page']:.2f} seconds |",
        f"| Sum of recorded raw-run segments | {c['recorded_run_segments_seconds']/60:.2f} minutes; incomplete |",
        f"| Retained-stage peak GPU / process-tree RSS | {c['peak_gpu_mib_sampled']:,.0f} / {c['peak_rss_mib_sampled']:,.0f} MiB |", '',
        'The run-segment total is a lower bound on recorded raw execution work, **not total project elapsed time**. Early runs and several aborted passes lack complete timers. Some timers include recovery and others cover recovery only. It includes rendering/startup/export where recorded, but excludes layout preparation, semantic correction, assembly, and human review. Do not add inference time to this total: they overlap. Per-page means hide substantial differences in content and region count.', '',
        'Early checkpoints labeled monitored stage time as inference time (batches02–06), and batch01 called it preparation time. This consolidation consistently sums underlying `inference.seconds`; per-batch JSON records both timers and the original label. Token counts and call counts reconcile with every checkpoint.', '',
        'RSS includes shared mappings and is not a physical RAM requirement. Peaks are sampled and may miss brief spikes. GPU allocation is not energy use; electricity and monetary compute costs were not measured.', '',
        '## Tokens and retry overhead', '',
        '| June local Qwen token accounting | Tokens |', '| --- | ---: |',
        f"| Retained prompt/image tokens | {c['retained_tokens']['prompt_tokens']:,} |",
        f"| Retained generated tokens | {c['retained_tokens']['completion_tokens']:,} |",
        f"| Retained total | {c['retained_tokens']['total_tokens']:,} |",
        f"| Additional failed/superseded response tokens | {c['additional_response_tokens']['total_tokens']:,} |",
        f"| Separately logged interrupted request | {c['interrupted_request_tokens_without_response']:,} |",
        f"| Observed total including retries/interruption | **{c['observed_tokens_including_interrupted_request']:,}** |", '',
        f"Observed overhead is **{(c['observed_tokens_including_interrupted_request']/c['retained_tokens']['total_tokens']-1)*100:.2f}%** above retained OCR. The audit finds {c['unique_response_calls']:,} distinct completion IDs and excludes {c['duplicate_cached_response_files_ignored']:,} copied cached responses. Real reruns remain counted even when they used the same crop. The separately interrupted request has no retained completion response. These totals exclude the earlier three-page pilot and do not estimate unlogged work.", '',
        'Five archived failed responses hit the output limit, across the information tables, design article and rebellion game. Crop revisions also caused superseded work; two process interruptions were documented. A normal stop did not guarantee completeness: source review still found omissions. Three rebellion-game regions required manual transcription, with some graphic literals still represented by explicit placeholders. Failure counts therefore do not measure total OCR defect incidence.', '',
        '**Local tokens are not paid assistant tokens.** Tesseract uses no LLM tokens for OCR, but its semantic-correction cost is unknown. No defensible paid-token saving, dollar saving, cost per accepted page, or human-time reduction can be calculated from these logs.', '',
        '## Should local Qwen also do automatic correction?', '',
        'The earlier three-page development pilot is separate from the June sample:', '',
        '| Workflow | Preparation time | Local tokens |', '| --- | ---: | ---: |']
    for label,key in [('A: Tesseract','A-tesseract'),('B: Qwen raw OCR','B-qwen'),('C: A + B + local Qwen correction','C-local-correction')]:
        r=p['arms'][key];lines.append(f"| {label} | {r['preparation_seconds']:.2f} s | {r['local_tokens']:,} |")
    lines += ['',
        'Relative to B, C increased preparation time by 2.54× and local tokens by 2.69×. Compact prose CER improved from 0.79% to 0.53%, and text on the figure page from 0.57% to 0.32%, while scored BASIC worsened from 0% to 0.13% (29 exact lines became 28). BASIC scoring excluded 41 uncertain lines, so this is a limited development result. C includes A+B dependencies; these are total preparation figures, not incremental correction alone. All times exclude startup, shared image preparation and human/capable-model work.', '',
        '**Do not add local self-correction as a mandatory pass yet.** Its extra work and occasional regressions have not shown a clear downstream benefit. Use selective trials on difficult regions while preserving the raw reading.', '',
        '## Decision and next measurement', '',
        '| Decision | Evidence / condition |', '| --- | --- |',
        '| Prefer Qwen for the next raw-OCR trial | Large, consistent sampled error reduction; local compute is feasible on the current machine |',
        '| Retain semantic correction and mandatory human review | Printed code, continuations, omissions and graphic glyphs still need judgment |',
        '| Keep Tesseract as fallback and selective diagnostic | Far lower raw runtime/RSS; occasionally a better reading; no need to run both over every page |',
        '| Continue layout-map and cache reuse | Preserve prior work; record actual retries separately |',
        '| Defer a claim of improved sustainability | Paid correction tokens and active review time are still unknown |', '',
        'For the next comparison, preselect a small balanced set of fresh prose, code, tables and graphic-heavy pages. Prepare both raw drafts on identical reviewed crops, then assign **one draft per page** to the correction/review workflow, balanced across content types. Keep the other draft hidden until review finishes to reduce familiarity bias. Record actual capable-model input/cached/output tokens, active mapping/correction/review minutes, retries, omissions and explicit human acceptance. Compare total effort per accepted page and errors after correction. Set the desired saving before inspecting the results; June supplies useful raw-OCR evidence, not that final decision metric.', '',
        'The aggregate evidence is strong enough to continue Qwen as a partial alternative now. The next experiment should spend its measurement effort on correction and review cost, rather than accumulating more favorable raw-CER examples.', '',
        '## Reproduce and inspect', '',
        '[Machine-readable consolidation](ocr-june-metrics.json) contains input hashes, weighted counts, per-batch tokens/times, failure evidence and explicit nulls for unmeasured costs. [Original progress](ocr-june-progress.json), [issue accounting](ocr-june-accounting.json), [earlier A/B/C pilot](ocr-workflow-measurements.json), and [reading-room review guide](READING-ROOM.md) remain separate.', '',
        'From the repository root, with the private June evidence present:', '',
        '```sh', 'PYTHONPATH=src:. python3 -m tools.ocr_qwen.consolidate', 'PYTHONPATH=src:. python3 -m unittest discover -s tests -p test_ocr_consolidate.py', '```', '',
        'The consolidator is read-only with respect to OCR evidence. It pools existing edit counts, validates unique source-crop identity, deduplicates only identical completion IDs, keeps retry work, and never converts a missing measurement to zero.', '']
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'docs/ocr-june-metrics.json')
    parser.add_argument('--report',type=Path,default=ROOT/'docs/OCR-JUNE-DECISION.md')
    args=parser.parse_args()
    report=build()
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    args.report.write_text(markdown(report))
    print(json.dumps({k:report[k] for k in ['scope','paired_engine_comparison']},indent=2))
    print('Retained inference seconds:',report['local_compute']['retained_inference_seconds'])
    print('Retained tokens:',report['local_compute']['retained_tokens'])
    print('Observed tokens with retries:',report['local_compute']['observed_tokens_including_interrupted_request'])


if __name__ == '__main__':
    main()
