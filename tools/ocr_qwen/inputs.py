"""Render eligible package pages with the existing orientation and exclusion rules."""
import json
from pathlib import Path
import subprocess

from PIL import Image

from tools.pdf_restore.inventory import ROOT, digest, pin, write_json
from tools.pdf_restore.ocr import orient_image, pixel_box
from tools.pdf_restore.package import validate_package


def package_image(package_path, pdf_page, output):
    package_path=Path(package_path)
    package_hash=digest(package_path)
    package=validate_package(json.loads(package_path.read_bytes()))
    source=ROOT/package['source']['path']
    if digest(source) != package['source']['sha256']:
        raise ValueError('PDF source hash changed')
    selected=[p for p in package['pages'] if p['pdf_page']==pdf_page]
    if len(selected)!=1:
        raise ValueError('Select exactly one mapped PDF page')
    page=selected[0]
    regions=[r for r in package['regions'] if r['pdf_index']==page['pdf_index']]
    output=Path(output)
    output.mkdir(parents=True,exist_ok=False)
    render=output/'page.png'
    command=['pdftoppm','-f',str(pdf_page),'-l',str(pdf_page),'-singlefile','-scale-to','3000',
             '-png',str(source),str(render.with_suffix(''))]
    subprocess.run(command,check=True,capture_output=True)
    with Image.open(render) as original:
        original.load()
        image=orient_image(original.convert('RGB'),page)
    for excluded in package['excluded_regions']:
        if excluded['pdf_index']==page['pdf_index']:
            image.paste('white',pixel_box(excluded['bbox'],image.size))
    eligible=Image.new('RGB',image.size,'white')
    for region in regions:
        box=pixel_box(region['bbox'],image.size)
        eligible.paste(image.crop(box),box)
    path=output/'eligible-page.png'
    eligible.save(path)
    if digest(source)!=package['source']['sha256'] or digest(package_path)!=package_hash:
        raise ValueError('Input changed during preparation')
    write_json(output/'provenance.json',dict(source=package['source'],package_sha256=package_hash,
               pdf_page=pdf_page,page=page,command=command,image=pin(output,path.name),
               preprocessing='Existing package orientation and exclusions, eligible-region mask; no enhancement'))
    return path
