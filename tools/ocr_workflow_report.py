"""Export transcription-free workflow measurements without claiming review savings."""
import argparse
import json
from pathlib import Path

from tools.pdf_restore.inventory import digest, write_json
from tools.ocr_qwen.benchmark import score
from tools.ocr_qwen.workflow import ARMS, checked_stage, review_summary


def summarize(directory):
    directory=Path(directory)
    report=json.loads((directory/'report.json').read_bytes())
    inputs=json.loads((directory/'inputs-for-evaluation.json').read_bytes())
    groups={(r['sample'],r['arm']):r for r in report['rows']}
    rows=[]
    for sample in inputs['samples']:
        stages={arm:[] for arm in ARMS}
        regressions=[]
        improvements=[]
        for region in sample['reference']:
            if region['kind']=='figure':
                continue
            results={}
            for arm in ARMS:
                result=checked_stage(directory/'stages'/sample['id']/region['id']/arm)
                if result is None:
                    raise ValueError('Missing completed stage')
                stages[arm].append(result)
                results[arm]=result
            b=score([region],[dict(region,text=results[ARMS[1]]['text'])])
            c=score([region],[dict(region,text=results[ARMS[2]]['text'])])
            delta=c['cer_no_whitespace_edits']-b['cer_no_whitespace_edits']
            if delta>0:
                regressions.append(dict(region=region['id'],extra_reference_edits=delta))
            elif delta<0:
                improvements.append(dict(region=region['id'],fewer_reference_edits=-delta))
        for arm in ARMS:
            row=groups[(sample['id'],arm)]
            dependencies=ARMS if arm==ARMS[2] else (arm,)
            consumed=[stage for name in dependencies for stage in stages[name]]
            rows.append(dict(sample=sample['id'],arm=arm,
                preparation_seconds=sum(groups[(sample['id'],name)]['stage_seconds'] for name in dependencies),
                incremental_stage_seconds=row['stage_seconds'],
                local_tokens={key:sum(groups[(sample['id'],name)]['local_tokens'][key] for name in dependencies)
                              for key in ('prompt_tokens','completion_tokens','total_tokens','calls','calls_with_usage')},
                sampled_peak_rss_mib=max(r['resources']['peak_rss_mib_sampled'] for r in consumed),
                sampled_peak_gpu_mib=max((r['resources']['peak_gpu_mib_sampled'] for r in consumed
                                         if r['resources']['peak_gpu_mib_sampled'] is not None),default=None),
                accuracy_proxy=row['accuracy_proxy'],text_regions=row['text_regions'],
                exact_draft_disagreement_regions=row['ab_disagreement_regions'],
                compact_draft_disagreement_regions=row['ab_compact_disagreement_regions'],
                correction_changed_regions=row['correction_changed_regions'] if arm==ARMS[2] else None,
                correction_uncertainty_notes=row['local_uncertainties'] if arm==ARMS[2] else None,
                correction_regressions_vs_B=regressions if arm==ARMS[2] else None,
                correction_improvements_vs_B=improvements if arm==ARMS[2] else None))
    return dict(schema_version=1,run=str(directory),report_sha256=digest(directory/'report.json'),
                reference_note=inputs.get('reference_note'),rows=rows,
                review_status=review_summary(directory/'review-ledger.json'),
                limits=report['limits']+[
                    'Preparation totals include dependencies: C=A+B+correction; B does not require A.',
                    'Times exclude model startup, common image preparation, scoring and human/capable-model correction.',
                    'Regression/improvement counts compare with existing references; they are not new human judgments.',
                    'Local Qwen token totals are local compute, not billed capable-model tokens.'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():
        parser.error('Choose a fresh summary output')
    write_json(args.output,summarize(args.run))
    print(args.output)


if __name__=='__main__':
    main()
