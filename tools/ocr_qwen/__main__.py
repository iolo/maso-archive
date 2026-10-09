"""Opt-in Qwen3-VL OCR; run with python3 -m tools.ocr_qwen."""
import argparse
import json
from pathlib import Path

from tools.pdf_restore.inventory import write_json
from .benchmark import benchmark, prepare_trial
from .pipeline import fresh_output, ocr_image
from .inputs import package_image
from .runtime import Monitor, Server
from .workflow import workflow, review_summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='action',required=True)
    prep=sub.add_parser('prepare-trial',help='Adapt existing private three-page reviewed comparison')
    prep.add_argument('--trial',type=Path,default=Path('private/pdf-restoration/ocr-comparison'))
    prep.add_argument('--output',type=Path,required=True)
    page=sub.add_parser('page',help='Detect layout and transcribe an upright/eligible raster image')
    source=page.add_mutually_exclusive_group(required=True)
    source.add_argument('--image',type=Path)
    source.add_argument('--package',type=Path,help='Existing mapped PDF article package; preserves eligible masks')
    page.add_argument('--pdf-page',type=int)
    page.add_argument('--rotation',type=int,choices=[0,90,180,270],default=0)
    trial=sub.add_parser('benchmark',help='Recompute Qwen and two pinned Tesseract baselines')
    trial.add_argument('--manifest',type=Path,required=True)
    trial.add_argument('--repeats',type=int,default=1)
    work=sub.add_parser('workflow',help='Prepare three mapped OCR/correction arms for human review')
    work.add_argument('--manifest',type=Path,required=True)
    work.add_argument('--resume',action='store_true')
    work.add_argument('--retry-incomplete',action='store_true',help='With --resume, archive incomplete stages and retry explicitly')
    review=sub.add_parser('review-summary',help='Validate explicit human review records; no automatic acceptance')
    review.add_argument('--ledger',type=Path,required=True)
    for command in (page,trial,work):
        command.add_argument('--output',type=Path,required=True)
        command.add_argument('--server-binary',type=Path)
        command.add_argument('--model',type=Path)
        command.add_argument('--mmproj',type=Path)
        command.add_argument('--context',type=int,default=8192)
        command.add_argument('--gpu-layers',type=int,default=99)
        command.add_argument('--image-tokens',type=int,default=4096)
        command.add_argument('--max-tokens',type=int,default=4096)
        command.add_argument('--timeout',type=float,default=600)
    args=parser.parse_args()
    if args.action=='prepare-trial':
        print(prepare_trial(args.trial,args.output))
        return
    if args.action=='review-summary':
        print(json.dumps(review_summary(args.ledger),ensure_ascii=False,indent=2))
        return
    if args.context<1024 or not 1<=args.max_tokens<args.context or args.image_tokens<1 or args.timeout<=0:
        parser.error('Require context >= 1024, 0 < max-tokens < context, image-tokens > 0, timeout > 0')
    options=dict(binary=args.server_binary,model=args.model,mmproj=args.mmproj,
                 context=args.context,gpu_layers=args.gpu_layers,image_tokens=args.image_tokens)
    if args.action=='workflow':
        print(workflow(args.manifest,args.output,args.resume,options,args.max_tokens,args.timeout,args.retry_incomplete))
    elif args.action=='benchmark':
        print(benchmark(args.manifest,args.output,args.repeats,options,args.max_tokens,args.timeout))
    else:
        if args.package and (args.pdf_page is None or args.rotation):
            parser.error('--package needs --pdf-page and uses its recorded orientation (no --rotation)')
        if args.image and args.pdf_page is not None:
            parser.error('--pdf-page requires --package')
        output=fresh_output(args.output)
        image=package_image(args.package,args.pdf_page,output/'preparation') if args.package else args.image
        with Server(output/'runtime',**options) as server:
            with Monitor() as monitor:
                ocr_image(image,output/'page',server,args.rotation,args.max_tokens,args.timeout)
            write_json(output/'metrics.json',monitor.metrics)
        print(output/'page/result.json')


if __name__=='__main__':
    main()
