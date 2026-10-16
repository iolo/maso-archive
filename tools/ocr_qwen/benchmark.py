"""Paired uncached OCR trials with pinned inputs and explicitly limited accuracy metrics."""
from tools.storage_layout import is_local_output
from collections import defaultdict
import json
import platform
from pathlib import Path
import re
import statistics
import subprocess
import time
import unicodedata

from PIL import Image

from tools.pdf_restore.inventory import ROOT, digest, pin, write_json
from tools.pdf_restore.ocr import RUNTIME, run_region, verify_runtime, pixel_box
from tools.toc_restore.ocr import lines_from_tsv
from .pipeline import fresh_output, ocr_image
from .runtime import Monitor, Server


def normalize(text, compact=False):
    text = unicodedata.normalize('NFC', text)
    return ''.join(text.split()) if compact else ' '.join(text.split())


def distance(a, b):
    """Exact Levenshtein distance with O(min(len(a),len(b))) space."""
    if len(a) < len(b):
        a, b = b, a
    row = list(range(len(b)+1))
    for i, x in enumerate(a, 1):
        nxt = [i]
        for j, y in enumerate(b, 1):
            nxt.append(min(nxt[-1]+1, row[j]+1, row[j-1]+(x != y)))
        row = nxt
    return row[-1]


def rates(reference, hypothesis):
    result = {}
    for name, compact in [('cer', False), ('cer_no_whitespace', True)]:
        ref, hyp = normalize(reference, compact), normalize(hypothesis, compact)
        errors = distance(ref, hyp)
        result[name] = errors/len(ref) if ref else None
        result[name+'_edits'] = errors
        result[name+'_reference_chars'] = len(ref)
    ref, hyp = normalize(reference).split(), normalize(hypothesis).split()
    result['wer'] = distance(ref, hyp)/len(ref) if ref else None
    return result


def intersection(a, b):
    return max(0, min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))


def area(a):
    return (a[2]-a[0])*(a[3]-a[1])


def iou(a, b):
    inter = intersection(a,b)
    return inter/(area(a)+area(b)-inter) if inter else 0


def eligible(region, references):
    # Include a predicted unit if >= half its area falls in one eligible reference
    # or its centre lies in one. Keep native order, never reorder using truth.
    a = region['bbox']
    x,y = (a[0]+a[2])/2, (a[1]+a[3])/2
    return any(intersection(a,r['bbox']) >= .5*area(a) or
               (r['bbox'][0] <= x <= r['bbox'][2] and r['bbox'][1] <= y <= r['bbox'][3])
               for r in references)


def numbered_lines(text):
    result = defaultdict(list)
    for line in text.splitlines():
        match = re.match(r'^\s*(\d{2,5})\s+(.*)', line)
        if match:
            result[int(match[1])].append(match[2])
    return result


def score(reference, prediction):
    refs = [r for r in reference if r['kind'] != 'figure']
    selected = [r for r in prediction if r.get('text') and eligible(r, refs)]
    text = '\n'.join(r['text'] for r in selected)
    if refs and all(r['kind'] == 'code' for r in refs):
        truth = numbered_lines('\n'.join(r['text'] for r in refs))
        actual = numbered_lines(text)
        # Overlapping reference crops repeat physical lines. Score each line once.
        known = {k:v[0] for k,v in truth.items() if not any('[BITMAP-' in s or '[BLANK-' in s or '[ILLEGIBLE]' in s for s in v)}
        ref = '\n'.join(f'{k} {v}' for k,v in sorted(known.items()))
        hyp = '\n'.join(f'{k} {actual[k][0]}' if k in actual else '' for k in sorted(known))
        accuracy = dict(scope='Resolved numbered BASIC lines only; first hypothesis per line number, unknown-glyph lines excluded; not whole-page CER',
                        **rates(ref,hyp), reference_lines=len(truth), scored_lines=len(known),
                        excluded_uncertain_lines=len(truth)-len(known),
                        missing_line_numbers=sorted(set(truth)-set(actual)),
                        extra_line_numbers=sorted(set(actual)-set(truth)),
                        duplicate_line_numbers=sorted(k for k,v in actual.items() if len(v)>1),
                        exact_resolved_lines=sum(k in actual and v == actual[k][0] for k,v in known.items()))
    else:
        accuracy = dict(scope='Eligible page text in native engine order; NFC and whitespace-normalized; includes order/omission errors',
                        **rates('\n'.join(r['text'] for r in refs), text))
    # A transparent coarse geometry metric, independent from text scoring.
    best = [max((iou(r['bbox'],p['bbox']) for p in prediction if p.get('text')),default=0) for r in refs]
    figures = [r for r in reference if r['kind']=='figure']
    accuracy['layout'] = dict(text_regions=len(refs), text_regions_iou_50=sum(v>=.5 for v in best),
                              mean_best_text_iou=statistics.mean(best) if best else None,
                              figures=len(figures), figures_iou_50=sum(
                                  max((iou(r['bbox'],p['bbox']) for p in prediction if p['kind']=='figure'), default=0)>=.5
                                  for r in figures),
                              note='Best-box IoU >= .5; sensitive to segmentation granularity. Tesseract page units are lines; mapped regions are supplied, not detected.')
    return accuracy


def prepare_trial(trial, destination):
    """Adapt the prior reviewed three-page trial without passing truth to the model."""
    trial = Path(trial).resolve()
    samples_path = trial/'samples.json'
    samples = json.loads(samples_path.read_bytes())['samples']
    entries=[]
    for sample in samples:
        image=trial/sample['input']['path']
        if pin(trial,sample['input']['path']) != sample['input']:
            raise ValueError('Prior trial input hash changed')
        reviewed_path=trial/'reviews/tesseract'/sample['id']/'reviewed-text.json'
        reviewed=json.loads(reviewed_path.read_bytes())
        regions=reviewed['regions']
        regions += [dict(r,text='') for r in sample['review_regions'] if r['kind']=='figure']
        entries.append(dict(id=sample['id'], image=str(image), sha256=digest(image),
                            reference=regions, reference_source=dict(path=str(reviewed_path),sha256=digest(reviewed_path)),
                            source=sample['source'], pdf_page=sample['page']['pdf_page']))
    if Path(destination).exists():
        raise ValueError('Manifest already exists')
    destination = Path(destination).resolve()
    if not is_local_output(destination, ROOT):
        raise ValueError('References must remain private')
    write_json(destination, dict(schema_version=1,samples=entries,
        reference_note='Prior scan-reviewed, assistant-corrected Tesseract drafts, crosschecked in earlier trial. Not an independent human gold corpus. BASIC has unresolved bitmap/blank glyphs. Three purposive pages, no generalization claim.',
        source_manifest=dict(path=str(samples_path),sha256=digest(samples_path))))
    return destination


def tesseract(image_path, output, references, mapped=False, runtime=RUNTIME):
    output.mkdir(parents=True,exist_ok=False)
    with Image.open(image_path) as img:
        image=img.convert('RGB')
    tasks = [r for r in references if r['kind']!='figure'] if mapped else [dict(id='page',kind='prose',bbox=[0,0,1,1])]
    regions=[]
    for index, task in enumerate(tasks):
        name=f'r{index:03}'
        box=pixel_box(task['bbox'],image.size)
        crop=image.crop(box)
        crop.save(output/f'{name}.png')
        config=dict(languages='eng' if task['kind']=='code' else 'kor+eng',psm=6 if mapped else 3)
        run_region(output/f'{name}.png',output/name,config,runtime)
        write_json(output/f'{name}.settings.json',config)
        if mapped:
            regions.append(dict(task,text=(output/f'{name}.txt').read_text(encoding='utf-8')))
        else:
            for line in lines_from_tsv(output/f'{name}.tsv', [0,0]):
                regions.append(dict(kind='prose', text=line['text'],bbox=[line['bbox'][0]/image.width,line['bbox'][1]/image.height,
                                                                       line['bbox'][2]/image.width,line['bbox'][3]/image.height]))
    write_json(output/'result.json',dict(regions=regions))
    return regions


def validate_manifest(path):
    manifest=json.loads(path.read_bytes())
    if manifest.get('schema_version') != 1 or not manifest.get('samples'):
        raise ValueError('Expected schema_version 1 and nonempty samples')
    ids=set()
    for sample in manifest['samples']:
        if not re.fullmatch(r'[A-Za-z0-9_-]+',sample['id']) or sample['id'] in ids:
            raise ValueError('Invalid or duplicate sample ID')
        ids.add(sample['id'])
        image=Path(sample['image'])
        if not image.is_absolute():
            image=path.parent/image
        sample['image']=str(image.resolve())
        if digest(image) != sample['sha256']:
            raise ValueError('Benchmark input hash differs')
        for r in sample['reference']:
            b=r['bbox']
            if len(b)!=4 or not (0<=b[0]<b[2]<=1 and 0<=b[1]<b[3]<=1) or not isinstance(r['text'],str):
                raise ValueError('Invalid reference region')
        source=sample.get('reference_source')
        if source and digest(Path(source['path'])) != source['sha256']:
            raise ValueError('Reference source hash differs')
    return manifest


def benchmark(manifest_path, output, repeats=1, server_options=None, max_tokens=4096, timeout=600):
    if repeats<1:
        raise ValueError('Repeats must be positive')
    manifest_path=Path(manifest_path).resolve()
    manifest_hash=digest(manifest_path)
    manifest=validate_manifest(manifest_path)
    runtime=verify_runtime()
    output=fresh_output(output)
    write_json(output/'inputs.json',manifest)
    write_json(output/'tesseract-runtime.json',runtime)
    write_json(output/'run.json',dict(manifest=dict(path=str(manifest_path),sha256=manifest_hash),
        repeats=repeats,max_tokens=max_tokens,timeout=timeout,
        implementation=[dict(path=str(p.relative_to(ROOT)),sha256=digest(p))
                        for p in sorted(Path(__file__).parent.glob('*.py'))]))
    rows=[]
    hardware=dict(platform=platform.platform(),cpu=platform.processor(),logical_cpus=__import__('os').cpu_count())
    try:
        hardware['gpu']=subprocess.check_output(['nvidia-smi','--query-gpu=name,driver_version,memory.total','--format=csv'],text=True).strip()
    except (OSError, subprocess.SubprocessError):
        hardware['gpu']=None
    def record(sample,engine,repeat,regions,metrics,error=None):
        row=dict(sample=sample['id'],engine=engine,repeat=repeat,metrics=metrics,status='failed' if error else 'ok')
        if error:
            row['error']=error
        else:
            row['accuracy']=score(sample['reference'],regions)
        rows.append(row)
        write_json(output/'results.json',dict(hardware=hardware,reference_note=manifest.get('reference_note'),rows=rows))
        print(f"{sample['id']} {engine} repeat {repeat}: {row['status']} {metrics['wall_seconds']:.2f}s",flush=True)
    for repeat in range(1,repeats+1):
        for sample in manifest['samples']:
            for engine,mapped in [('tesseract-page',False),('tesseract-mapped',True)]:
                with Monitor() as monitor:
                    regions=tesseract(Path(sample['image']),output/f'{sample["id"]}-{engine}-{repeat}',sample['reference'],mapped)
                record(sample,engine,repeat,regions,monitor.metrics)
    with Server(output/'runtime',**(server_options or {})) as server:
        for repeat in range(1,repeats+1):
            for sample in manifest['samples']:
                error=None
                with Monitor() as monitor:
                    try:
                        result=ocr_image(Path(sample['image']),output/f'{sample["id"]}-qwen-{repeat}',server,max_tokens=max_tokens,timeout=timeout)
                    except Exception as exc:
                        error=f'{type(exc).__name__}: {exc}'
                record(sample,'qwen',repeat,None if error else result['regions'],monitor.metrics,error)
                if server.process.poll() is not None:
                    raise RuntimeError('Owned llama-server exited during benchmark')
        write_json(output/'summary.json',summarize(rows,server.metadata['startup'],hardware,manifest))
    validate_manifest(manifest_path)
    if digest(manifest_path)!=manifest_hash:
        raise ValueError('Benchmark manifest changed during processing')
    write_json(output/'manifest.json',{'files':[pin(output,p.relative_to(output).as_posix())
        for p in sorted(output.rglob('*')) if p.is_file()]})
    return output


def summarize(rows,startup,hardware,manifest):
    groups=defaultdict(list)
    for row in rows:
        groups[(row['sample'],row['engine'])].append(row)
    summary=[]
    for (sample,engine),items in groups.items():
        good=[r for r in items if r['status']=='ok']
        summary.append(dict(sample=sample,engine=engine,runs=len(items),failures=len(items)-len(good),
            median_seconds=statistics.median(r['metrics']['wall_seconds'] for r in good) if good else None,
            peak_rss_mib_sampled=max((r['metrics']['peak_rss_mib_sampled'] for r in items),default=None),
            peak_gpu_mib_sampled=max((r['metrics']['peak_gpu_mib_sampled'] for r in items if r['metrics']['peak_gpu_mib_sampled'] is not None),default=None),
            accuracy=[r.get('accuracy') for r in items]))
    return dict(hardware=hardware,reference_note=manifest.get('reference_note'),startup=startup,summary=summary,
                limits=['Inference pipeline timing includes crop I/O and model HTTP requests; excludes common pre-rendered input and model startup.',
                        'All runs recompute OCR; Qwen cache_prompt=false. GPU allocator and OS file caches remain warm.',
                        'Tesseract mapped mode uses reviewed boxes; Qwen and Tesseract page modes do not receive reference boxes.',
                        'Sampled process-tree RSS is not PSS; summed shared mappings can overcount physical memory.',
                        'Greedy sampling with seed 42, no presence penalty; cross-hardware determinism is not guaranteed.',
                        'CER can exceed 100%; whitespace-free CER does not measure code indentation accuracy.'])
