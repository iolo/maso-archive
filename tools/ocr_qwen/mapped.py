"""Qwen raw OCR of mapped article regions, with existing PDF evidence contracts."""
import argparse
import json
from pathlib import Path
import subprocess

from PIL import Image

from tools.pdf_restore.inventory import ROOT, digest, pin, write_json
from tools.pdf_restore.ocr import orient_image, pixel_box
from tools.pdf_restore.package import validate_package
from tools.pdf_restore.build import validate_source, checked, safe_path
from .pipeline import TEXT_PROMPT, TEXT_SCHEMA, infer
from .runtime import Server
from .workflow import checked_stage, png_bytes, run_lock, save_once, stage


MAX_PAGES=12
MAX_ARTICLES=3
CODE_ROOT=Path(__file__).resolve().parents[2]


def prepare_maps(request_path):
    request_path=Path(request_path).resolve()
    request=json.loads(request_path.read_bytes())
    if not 1<=len(request['articles'])<=MAX_ARTICLES:
        raise ValueError('Mapped checkpoint must have 1..3 articles')
    pages=set(); articles=[]; identities=set()
    for item in request['articles']:
        path=safe_path(ROOT,item['map']['path'])
        package=validate_package(json.loads(checked(ROOT,item['map'])))
        validate_source(package,ROOT)
        if package['id'] in identities or package['mapping']['status']!='mapped':
            raise ValueError('Require distinct, inspected mapped articles')
        identities.add(package['id'])
        for p in package['pages']:
            pages.add((package['source']['sha256'],p['pdf_page']))
        # Package validation owns geometric/content relationships; filenames must also be safe.
        for name in [package['id'],*[r['id'] for r in package['regions']]]:
            if not name or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in name):
                raise ValueError('Unsafe article/region ID')
        articles.append(dict(package=package,map_pin=item['map']))
    if len(pages)>MAX_PAGES:
        raise ValueError('Mapped checkpoint exceeds 12 distinct source pages')
    return request,articles


def run(request_path,output,resume=False,max_tokens=4096,timeout=600,server_options=None):
    output=Path(output).resolve()
    with run_lock(output):
        request,articles=prepare_maps(request_path)
        # Resolve and fingerprint local runtime without starting a model on a cache-only run.
        attempt=1+len(list(output.glob('runtime-*'))) if output.exists() else 1
        server=Server(output/f'runtime-{attempt:03}',**(server_options or {}))
        fingerprint=dict(engine='qwen3-vl-mapped',model_files=[dict(path=str(p),sha256=digest(p))
            for p in (server.binary,server.model,server.mmproj)],
            context=server.context,image_tokens=server.image_tokens,gpu_layers=server.gpu_layers,
            max_tokens=max_tokens,timeout=timeout,prompt=TEXT_PROMPT,schema=TEXT_SCHEMA,
            scale_to=request.get('scale_to',3000),request_sha256=digest(request_path),
            implementation={str(p.relative_to(CODE_ROOT)):digest(p) for p in [Path(__file__),
                Path(__file__).parent/'pipeline.py',Path(__file__).parent/'runtime.py',
                Path(__file__).parent/'workflow.py',CODE_ROOT/'tools/pdf_restore/ocr.py']})
        if type(fingerprint['scale_to']) is not int or not 1000<=fingerprint['scale_to']<=6000:
            raise ValueError('scale_to must be 1000..6000')
        if resume:
            if json.loads((output/'runtime-fingerprint.json').read_bytes())!=fingerprint:
                raise ValueError('Mapped inputs/runtime changed; use a fresh checkpoint')
        else:
            output.mkdir(parents=True,exist_ok=False)
            write_json(output/'runtime-fingerprint.json',fingerprint)
            write_json(output/'request.json',request)
        runtime_pin=pin(output,'runtime-fingerprint.json')
        jobs=[]; cached=0
        for article in articles:
            package=article['package'];base=output/package['id']
            save_once(base/'map.json',checked(ROOT,article['map_pin']))
            for page in package['pages']:
                folder=base/f'ocr-page{page["pdf_page"]}'
                render=output/'renders'/f'{package["source"]["sha256"]}-{page["pdf_page"]}.png'
                if not render.exists():
                    render.parent.mkdir(parents=True,exist_ok=True)
                    subprocess.run(['pdftoppm','-f',str(page['pdf_page']),'-l',str(page['pdf_page']),
                        '-singlefile','-scale-to',str(fingerprint['scale_to']),'-png',
                        str(ROOT/package['source']['path']),str(render.with_suffix(''))],check=True,capture_output=True)
                with Image.open(render) as original:
                    image=orient_image(original.convert('RGB'),page)
                for excluded in package['excluded_regions']:
                    if excluded['pdf_index']==page['pdf_index']:
                        image.paste('white',pixel_box(excluded['bbox'],image.size))
                for region in package['regions']:
                    if region['pdf_index']!=page['pdf_index']:continue
                    crop=pixel_box(region['bbox'],image.size)
                    save_once(folder/f'{region["id"]}.png',png_bytes(image.crop(crop)))
                    if region['kind']=='figure':continue
                    directory=output/'stages'/package['id']/region['id']
                    job=dict(directory=directory,region=region,page=page,folder=folder,
                             crop_pixels=list(crop),render_size=list(image.size),map_pin=article['map_pin'],
                             package=package)
                    if checked_stage(directory) is not None:cached+=1
                    else:jobs.append(job)
        if jobs:
            with server:
                for job in jobs:
                    r=job['region'];crop=job['folder']/f'{r["id"]}.png'
                    def recognize(directory):
                        with Image.open(crop) as image:
                            result,metrics=infer(server,image,TEXT_PROMPT.format(kind=r['kind']),TEXT_SCHEMA,
                                                 directory/'inference',max_tokens,timeout)
                        return dict(text=result['text'],inference=metrics)
                    result,_=stage(job['directory'],recognize)
                    print(f'{job["package"]["id"]}/{r["id"]}: {result["resources"]["wall_seconds"]:.2f}s',flush=True)
        outcomes=[]
        for article in articles:
            package=article['package'];base=output/package['id'];bundles=[]
            for page in package['pages']:
                folder=base/f'ocr-page{page["pdf_page"]}';images=[];results=[]
                for region in package['regions']:
                    if region['pdf_index']!=page['pdf_index']:continue
                    rid=region['id'];images.append(pin(folder,rid+'.png'))
                    if region['kind']=='figure':continue
                    directory=output/'stages'/package['id']/rid
                    value=checked_stage(directory)
                    with Image.open(folder/f'{rid}.png') as crop:
                        size=list(crop.size)
                    # No invented word boxes: carry exact regional coordinates plus original model evidence.
                    name=rid+'-qwen'
                    save_once(folder/f'{name}.txt',(value['text']+'\n').encode())
                    response=json.loads((directory/'inference.response.json').read_bytes())
                    positions=dict(engine='qwen3-vl',granularity='region',word_positions_available=False,
                                   region_id=rid,bbox_upright_normalized=region['bbox'],crop_size=size,
                                   native_response=response)
                    settings=dict(engine='qwen3-vl',region_ids=[rid],image=rid+'.png',
                        source_sha256=package['source']['sha256'],package=dict(sha256=article['map_pin']['sha256']),
                        pdf_page=page['pdf_page'],pdf_index=page['pdf_index'],runtime=runtime_pin,
                        **{k:page[k] for k in ('orientation_correction',) if k in page},
                        render_scale_to=fingerprint['scale_to'],
                        native_request=json.loads((directory/'inference.request.json').read_bytes()),
                        positions='Region-only JSON evidence, including raw response; no inferred word positions')
                    for suffix,data in [('positions.json',positions),('settings.json',settings)]:
                        save_once(folder/f'{name}.{suffix}',(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode())
                    results.append(dict(region_ids=[rid],text=pin(folder,name+'.txt'),
                                        positions=pin(folder,name+'.positions.json'),settings=pin(folder,name+'.settings.json')))
                evidence=dict(source_sha256=package['source']['sha256'],pdf_page=page['pdf_page'],
                              runtime=runtime_pin,images=images,results=results,
                              **{k:page[k] for k in ('orientation_correction',) if k in page})
                save_once(folder/'evidence.json',(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n').encode())
                bundles.append(dict(directory=folder.name,manifest=pin(base,folder.name+'/evidence.json')))
            save_once(base/'evidence-bundles.json',(json.dumps(dict(ocr_bundles=bundles,runtime=runtime_pin),indent=2)+'\n').encode())
            outcomes.append(dict(article_id=package['id'],ocr_complete=True,semantic_correction='pending',human_review='pending',
                                 regions=len(package['regions']),pdf_pages=[p['pdf_page'] for p in package['pages']]))
        # Detect inputs changing while a long inference run was in progress.
        prepare_maps(request_path)
        if digest(request_path)!=fingerprint['request_sha256']:raise ValueError('Request changed during OCR')
        report=dict(articles=outcomes,cache_hits=cached,new_inferences=len(jobs),runtime=runtime_pin,
                    status='raw-ocr-complete',review_required=True)
        write_json(output/'report.json',report)
        return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--max-tokens',type=int,default=4096)
    parser.add_argument('--timeout',type=float,default=600)
    args=parser.parse_args()
    print(json.dumps(run(args.request,args.output,args.resume,args.max_tokens,args.timeout),indent=2))


if __name__=='__main__':main()
