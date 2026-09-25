"""Build a private, portable CD1 reading/OCR reference from prepared and retained text."""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import html
import io
import json
from pathlib import Path
import re
import subprocess
import tempfile

from PIL import Image
from tools import inventory_cd1_processing as queue, map_cd1_images as images
from tools.cd1_batch_core import inherited_states
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import ROOT, require
from tools.reference import text as recovery
from maso_archive.reading_room_package import checked_file, check_svg, file_record

CURRENT=ROOT/'data/catalog/batch-runs/cd1-oem-pass.json'
OUTPUT=ROOT/'build/cd1-reference'
RECORD=ROOT/'data/catalog/batch-runs/cd1-readable-reference.json'
CSS='''body{font:17px/1.65 system-ui,sans-serif;max-width:76rem;margin:2rem auto;padding:0 1rem;color:#222;background:#fff}
a{color:#1455a0}h1,h2{line-height:1.3}nav a{margin-right:1rem}.text{white-space:pre-wrap;overflow-wrap:anywhere;margin:.35rem 0}pre{overflow:auto;padding:1rem;background:#f5f5f5;tab-size:8;line-height:1.45}code{font-family:ui-monospace,monospace}img{max-width:100%;height:auto;background:white}figure{margin:1rem 0}figcaption,.note{color:#555}.gap{border-left:4px solid #aa6500;padding-left:1rem}li{margin:.35rem 0}table{border-collapse:collapse}td,th{padding:.3rem .7rem;border-bottom:1px solid #ddd;text-align:left}.section{font-weight:bold}details{margin:1rem 0}summary{cursor:pointer}'''
LABELS={'prepared':'Prepared CD text','normalized':'Recovered CD reference',
        'reference_with_gaps':'Reference with marked text gaps','blocked':'Article boundaries unresolved',
        'unavailable':'Text unavailable'}


def read(path):return json.loads(Path(path).read_bytes())
def json_bytes(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
def esc(value):return html.escape(str(value),quote=True)


def put(root,name,raw):
    path=root/name;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(raw.encode() if isinstance(raw,str) else raw)


def page(title,body,depth):
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(title)}</title><link rel="stylesheet" href="{"../"*depth}style.css">'
            f'</head><body>{body}</body></html>\n')


def table(record,name):
    item=next(r for r in record['outputs'] if r['path']==name+'.jsonl')
    return [json.loads(line) for line in checked_file(ROOT/record['coverage_root'],item).splitlines()]


def prepared_blocks(article,media):
    blocks=[]
    for section in article['sections']:
        for original in section['blocks']:
            block=deepcopy(original)
            block['preformatted']=block['layout']=='preformatted'
            for paragraph in block['paragraphs']:
                paragraph['terminated']=True
                for run in paragraph['runs']:
                    if run['type']=='media':run['resource']=media[run['media_id']]['source']['resource']
            blocks.append(block)
    return blocks


def normalized_blocks(topics):
    blocks=[]
    for topic in topics:
        for p in topic['paragraphs']:
            pre=p['preformatted']
            if blocks and (pre and blocks[-1]['preformatted'] or not p['runs'] and blocks[-1]['preformatted']):
                blocks[-1]['paragraphs'].append(p)
            else:
                blocks.append({'id':p['id'],'type':'code' if pre else 'paragraph',
                               'preformatted':pre,'paragraphs':[p]})
    return blocks


def render_runs(runs):
    parts=[]
    for r in runs:
        if r['type']=='media':
            parts.append(f'<a href="../../media/{esc(r["resource"])}/index.html">[image:{esc(r["resource"])}]</a>')
        else:
            value=esc(r['text'])
            for mark in r.get('marks',[]):
                if mark in ('bold','italic','underline'):
                    tag={'bold':'strong','italic':'em','underline':'u'}[mark];value=f'<{tag}>{value}</{tag}>'
            parts.append(value)
    return ''.join(parts)


def export_article(root,job,blocks,status,details,media_for,source_record):
    ref=job['source_reference'];require(re.fullmatch(r'[A-Za-z0-9_.-]+',ref),'Unsafe CD reference')
    issue=job['issue_id'].removeprefix('maso-');directory=f'issues/{issue}/articles/{ref}'
    paragraphs=[p for b in blocks for p in b['paragraphs']]
    plain=recovery.text_for(paragraphs)
    text_path=directory+'/article.txt'
    mappings=[];line=1;position=0
    for p in paragraphs:
        content=recovery.paragraph_text(p)+('\n' if p.get('terminated',True) else '')
        count=content.count('\n')
        mappings.append({'id':p['id'],'first_line':line,'last_line':line+count-int(content.endswith('\n')),
                         'character_offset':position,'characters':len(content),
                         'resources':[r['resource'] for r in p['runs'] if r['type']=='media']})
        line+=count;position+=len(content)
    require(position==len(plain),'Plain text paragraph mapping differs')
    resources=list(dict.fromkeys(r['resource'] for p in paragraphs for r in p['runs'] if r['type']=='media'))
    body=[f'<nav><a href="../../index.html">{esc(issue)}</a><a href="../../../../index.html">All issues</a></nav>',
          f'<h1>{esc(job["title"])}</h1><p>{esc(ref)} · {esc(LABELS[status])} · Paper verification pending</p>']
    if status in ('blocked','unavailable'):
        body.append('<p class="gap">Article text is not assigned here. The source and review record are retained.</p>')
    else:
        body.append('<nav><a href="article.txt">UTF-8 text for OCR comparison</a><a href="paragraphs.json">Paragraph and image positions</a><a href="#listings">Listings</a><a href="#images">Images</a></nav>')
        put(root,text_path,plain);put(root,directory+'/paragraphs.json',json_bytes(mappings))
    if details:
        body.append(f'<p class="gap">{esc(details)}</p>')
    body.append('<p class="note">CD text is a secondary reference. Check differences against the paper magazine or scan.</p>')
    listings=[];content=[];pindex=0
    for b in blocks:
        block_text=recovery.text_for(b['paragraphs'])
        if b['preformatted']:
            number=len(listings)+1;filename=f'listings/{number:03d}.txt'
            put(root,directory+'/'+filename,block_text)
            listings.append({'path':filename,'block_id':b['id'],'sha256':digest(block_text.encode()),'characters':len(block_text)})
            content.append(f'<section id="listing-{number}"><p><a href="{filename}">Listing {number} — text</a></p><pre><code>{esc(block_text)}</code></pre></section>')
            pindex+=len(b['paragraphs'])
        else:
            for p in b['paragraphs']:
                pindex+=1;rendered=render_runs(p['runs'])
                tag='h2' if b['type'] in ('title','heading') else 'p'
                content.append(f'<{tag} class="text" id="p-{pindex}">{rendered if rendered else "<br>"}</{tag}>')
        # Display figures near their source block, including images inside listings.
        for p in b['paragraphs']:
            for run in p['runs']:
                if run['type']!='media':continue
                name=run['resource'];m=media_for(name,issue);url=f'../../media/{name}/'
                picture=f'<img src="{url}{m["asset_name"]}" alt="{esc(name)}" loading="lazy">' if m['asset_name'] else '<p>Image conversion deferred; original file available.</p>'
                content.append(f'<figure><a href="{url}index.html">{picture}</a><figcaption>{esc(name)}</figcaption></figure>')
    body.append('<h2 id="listings">Listings and preformatted text</h2><p class="note">Includes source-code candidates and fixed-width tables. No code corrections are inferred.</p>')
    body.append('<ul>'+''.join(f'<li><a href="#listing-{n}">Listing {n}</a> · <a href="{r["path"]}">Download text</a></li>' for n,r in enumerate(listings,1))+'</ul>' if listings else '<p>No separate listing identified; any code remains in the complete text below.</p>')
    body.extend(content)
    body.append('<h2 id="images">Images</h2><ul>'+''.join(f'<li><a href="../../media/{esc(n)}/index.html">{esc(n)}</a></li>' for n in resources)+'</ul>')
    body.append('<details><summary>Source and review notes</summary><a href="reference.json">Reference record</a></details>')
    reference={'reference':ref,'issue_id':job['issue_id'],'status':status,'print_verification':'pending',
               'source':source_record,'details':details,'blocks':blocks,'listings':listings,'resources':resources}
    put(root,directory+'/reference.json',json_bytes(reference))
    put(root,directory+'/index.html',page(job['title'],''.join(body),4))
    return {'reference':ref,'article_id':job['candidate_article_id'],'issue_id':job['issue_id'],'title':job['title'],
            'status':status,'path':directory+'/index.html','text':text_path if paragraphs else None,
            'paragraphs':len(paragraphs),'listings':len(listings),'image_occurrences':sum(len(m['resources']) for m in mappings),
            'resources':resources,'text_sha256':digest(plain.encode()) if paragraphs else None}


def build(output=OUTPUT,write_record=False):
    output=Path(output).resolve()
    require(output.parent==ROOT/'build' and output.name.startswith('cd1-reference') and not output.is_symlink(),
            'Reference output must be a dedicated build/cd1-reference* directory')
    current=read(CURRENT);data,inventory_manifest=queue.load_inventory(queue.OUTPUT)
    jobs={j['id']:j for j in data['jobs']};catalog=table(current,'catalog');exceptions={r['job_id']:r for r in table(current,'exceptions')}
    require(len(jobs)==len(catalog)==1088,'Reference candidate population changed')
    media_rows={r['resource']:r for r in table(current,'media')}
    source_images={r['path'].removeprefix('raw/'):r for r in read(images.MANIFEST)['files'] if r['path'].startswith('raw/')}
    rtf=(images.RAW/'MASOCD.rtf').read_bytes();policy=read(ROOT/'data/catalog/batch-profiles/cd1-shared-policy.json')
    require(digest(rtf)==policy['source_rtf_sha256'],'RTF source changed')
    fallback=[jobs[r['job_id']] for r in catalog if r['outcome']=='failed']
    states=inherited_states(rtf,[s['rtf']['byte_offset'] for j in fallback for s in j['source_topics']])
    prepared={};asset_sources={};issue_records={}
    for row in current['issues']:
        package=ROOT/current['output_root']/row['package']/'content'
        manifest=read(package/'manifest.json')
        documents={}
        for entry in manifest['documents']:
            doc=json.loads(checked_file(package,entry));documents.setdefault(entry['kind'],[]).append(doc)
        issue_records[row['issue_id']]=documents['issue'][0]
        media={m['id']:m for m in documents['media_index'][0]['items']}
        for item in media.values():
            if item['asset']:asset_sources[item['source']['resource']]=(package,item['asset'])
        for article in documents.get('article',[]):
            require(article['id'] not in prepared,'Duplicate prepared article')
            prepared[article['id']]=(article,media,package,manifest)
    require(len(prepared)==995,'Prepared reference population changed')
    toc_path=ROOT/'build/toc/toc-entries.jsonl';issue_path=ROOT/'build/toc/issues.json'
    toc=[json.loads(l) for l in toc_path.read_bytes().splitlines()];all_issues=read(issue_path)
    require(len(toc)==5497 and len(all_issues)==122,'TOC population changed')
    # Current metadata is kept separate from older package TOC snapshots.
    matched={r['toc_entry_id']:r['article_ids'] for r in table(current,'toc')}
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.cd1-reference-',dir=output.parent) as temporary:
        stage=Path(temporary);copied={};articles=[];fallback_records=[]
        def media_for(name,issue):
            key=(issue,name)
            if key in copied:return copied[key]
            require(name in media_rows,'Uninventoried image reference')
            require(name in source_images,'Missing image source record')
            original=checked_file(images.RAW,{**source_images[name],'path':name});directory=f'issues/{issue}/media/{name}'
            put(stage,directory+'/'+name,original);asset_name=None;status='deferred'
            conversion_note=None
            if name in asset_sources:
                package,record=asset_sources[name];converted=checked_file(package,record)
                if record['mime_type']=='image/svg+xml':check_svg(converted)
                asset_name=Path(record['path']).name;put(stage,directory+'/'+asset_name,converted);status='available'
            elif name.endswith(('.bmp','.dib')):
                try:
                    with Image.open(io.BytesIO(original)) as image:
                        image.load();pixels=image.convert('RGBA');stream=io.BytesIO();pixels.save(stream,format='PNG')
                        converted=stream.getvalue()
                        with Image.open(io.BytesIO(converted)) as restored:require(restored.convert('RGBA').tobytes()==pixels.tobytes(),'Converted image differs')
                    asset_name=name+'.png';put(stage,directory+'/'+asset_name,converted);status='available'
                except (OSError,ValueError) as error:
                    conversion_note='Pillow could not decode the source bitmap: '+str(error)
                    candidate=stage/directory/(name+'.png')
                    try:
                        result=subprocess.run(['convert',str(images.RAW/name),'-strip','-define',
                            'png:exclude-chunks=date,time',str(candidate)],capture_output=True,timeout=60)
                        if result.returncode==0 and candidate.exists():
                            with Image.open(candidate) as rendered:rendered.load()
                            asset_name=candidate.name;status='available'
                            conversion_note+='; ImageMagick produced a readable PNG; compare with paper.'
                        else:
                            conversion_note+='; ImageMagick conversion deferred.'
                            if candidate.exists():candidate.unlink()
                    except (OSError,ValueError,subprocess.TimeoutExpired) as fallback_error:
                        conversion_note+='; '+str(fallback_error)
                        if candidate.exists():candidate.unlink()
            picture=f'<a href="{asset_name}"><img src="{asset_name}" alt="{esc(name)}"></a>' if asset_name else '<p>Conversion deferred. The original image remains available below.</p>'
            body=f'<nav><a href="../../index.html">{esc(issue)}</a></nav><h1>{esc(name)}</h1>{picture}<p><a href="{esc(name)}">Original image file</a></p><p>Compare diagrams, tables and image-based listings with the paper/scan.</p>'
            if conversion_note:body+=f'<details><summary>Conversion note</summary>{esc(conversion_note)}</details>'
            put(stage,directory+'/index.html',page(name,body,4))
            copied[key]={'resource':name,'issue':issue,'status':status,'asset_name':asset_name,'original_sha256':digest(original),'conversion_note':conversion_note}
            return copied[key]
        for number,row in enumerate(catalog,1):
            job=jobs[row['job_id']];ref=job['source_reference'];details='';blocks=[]
            source_record={'source_topics':job['source_topics'],'prior_outcome':row['outcome']}
            if job['candidate_article_id'] in prepared:
                article,media,package,manifest=prepared[job['candidate_article_id']]
                blocks=prepared_blocks(article,media);status='prepared'
                source_record['package']=package.relative_to(ROOT).as_posix()
            elif row['outcome']=='blocked':
                status='blocked';details='Source topic ownership needs review; no article boundaries are guessed.'
                source_record['blockers']=exceptions[job['id']]['blockers']
            else:
                topics=[recovery.recover(rtf,s,states[s['rtf']['byte_offset']]['character']['font_id']) for s in job['source_topics']]
                gaps=[x for t in topics for x in t['issues']]
                status='reference_with_gaps' if gaps else 'normalized';blocks=normalized_blocks(topics)
                details=(f'{len(gaps)} marked text gaps. Symbols or bytes inside ⟦…⟧ need paper/scan review.' if gaps else
                         'Recovered with ordinary formatting normalized. Text has not been checked against paper.')
                source_record.update(topics=topics,prior_failure=exceptions[job['id']]['category'])
                fallback_records.append({'reference':ref,'status':status,'topics':len(topics),'gaps':len(gaps),
                                         'source_bytes':sum(t['source_bytes'] for t in topics),
                                         'normalizations':dict(sum((Counter(t['normalizations']) for t in topics),Counter()))})
            articles.append(export_article(stage,job,blocks,status,details,media_for,source_record))
            if number%100==0:print(f'Exported {number}/1088 article references',flush=True)
        by_id={a['article_id']:a for a in articles}
        for issue in all_issues:
            date=issue['id'].removeprefix('maso-');rows=[a for a in articles if a['issue_id']==issue['id']]
            body=[f'<nav><a href="../../index.html">All issues</a></nav><h1>{esc(date)}</h1><p>Cover scan not supplied.</p>',
                  '<h2>CD articles</h2><p>Browse these directly even when the library TOC uses a different title.</p><ul>']
            for a in rows:body.append(f'<li><a href="articles/{esc(a["reference"])}/index.html">{esc(a["title"])}</a> — {esc(a["reference"])} · {esc(LABELS[a["status"]])}</li>')
            body.append('</ul>' if rows else '</ul><p>No CD1 article source for this issue; paper/scan needed.</p>')
            body.append('<h2>Library table of contents</h2><p>Transcribed metadata may vary. Unmatched entries remain unlinked; they do not hide CD articles above.</p><ol>')
            for t in (t for t in toc if t['issue_id']==issue['id']):
                links=[by_id[a] for a in matched.get(t['id'],[]) if a in by_id]
                title=esc(t['title_candidate']);pages=esc(t.get('page_reference_raw') or '')
                body.append(f'<li class="{"section" if t["kind_candidate"]=="section" else "entry"}" style="margin-left:{min(t["depth"],8)}rem">{title} {pages} '+
                            ''.join(f'<a href="articles/{a["reference"]}/index.html">CD text</a>' for a in links)+'</li>')
            body.append('</ol>');put(stage,f'issues/{date}/index.html',page(date,''.join(body),2))
        counts={'issues':len(all_issues),'issues_with_cd_articles':len({a['issue_id'] for a in articles}),
                'candidates':len(articles),'article_status':dict(sorted(Counter(a['status'] for a in articles).items())),
                'readable_articles':sum(a['status'] in ('prepared','normalized') for a in articles),
                'articles_with_text':sum(a['text'] is not None for a in articles),
                'paragraphs':sum(a['paragraphs'] for a in articles),'listing_files':sum(a['listings'] for a in articles),
                'image_occurrences':sum(a['image_occurrences'] for a in articles),'distinct_images':len({k[1] for k in copied}),
                'image_status':dict(sorted(Counter(m['status'] for m in {m['resource']:m for m in copied.values()}.values()).items())),
                'toc_entries':len(toc),'text_gaps':sum(r['gaps'] for r in fallback_records)}
        put(stage,'style.css',CSS+'\n');put(stage,'catalog.json',json_bytes(articles));put(stage,'recovery-summary.json',json_bytes(fallback_records))
        put(stage,'images.json',json_bytes(list(copied.values())))
        body=f'<h1>마이크로소프트웨어 · CD1 reference</h1><p>{counts["readable_articles"]} readable articles; {counts["article_status"].get("reference_with_gaps",0)} with marked text gaps; {counts["article_status"].get("blocked",0)} unresolved article boundaries.</p><p>For personal reading and comparison with OCR and paper scans. All CD text awaits paper verification.</p><p><a href="catalog.json">Article catalog</a> · <a href="README.txt">How to use this reference</a></p><ul>'
        with_text=[];metadata_only=[]
        for issue in all_issues:
            date=issue['id'].removeprefix('maso-');n=sum(a['issue_id']==issue['id'] and a['text'] is not None for a in articles)
            link=f'<li><a href="issues/{date}/index.html">{date}</a> — {n} CD article texts</li>'
            (with_text if n else metadata_only).append(link)
        body+=''.join(with_text)+'</ul><details><summary>Earlier issues: table of contents only; scans needed</summary><ul>'+''.join(metadata_only)+'</ul></details>'
        put(stage,'index.html',page('CD1 readable reference',body,0))
        put(stage,'README.txt','Open index.html directly in a browser. No server or framework is required.\n'
            'Each article has UTF-8 article.txt and paragraph/image positions for OCR comparison.\n'
            'Listings have separate text downloads; original image files accompany viewable derivatives.\n'
            'All text is a secondary CD reference, pending paper verification. Marked gaps must not be treated as code.\n'
            'Do not automatically overwrite OCR with CD text. Inspect disagreements against paper/scans.\n'
            'Library TOC matching is incomplete; use the separate CD article list in each issue.\n')
        inputs={'coverage':file_record(CURRENT.relative_to(ROOT).as_posix(),CURRENT.read_bytes()),
                'rtf_sha256':digest(rtf),'toc_sha256':digest(toc_path.read_bytes()),'issues_sha256':digest(issue_path.read_bytes()),
                'implementation':{p.relative_to(ROOT).as_posix():digest(p.read_bytes()) for p in (Path(__file__),Path(recovery.__file__))}}
        files=[file_record(p.relative_to(stage).as_posix(),p.read_bytes()) for p in sorted(stage.rglob('*')) if p.is_file()]
        manifest={'kind':'cd1-readable-reference','schema_version':1,'inputs':inputs,'counts':counts,'files':files}
        put(stage,'manifest.json',json_bytes(manifest))
        # Build in isolation. Existing exports are immutable; same-input reruns verify exact output.
        if output.exists():
            require(read(output/'manifest.json')==manifest,'Existing reference differs; retain it and use a new --output build/cd1-reference-* path')
            require({p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}=={r['path'] for r in files}|{'manifest.json'},'Reference inventory changed')
            for item in files:checked_file(output,item)
        else:stage.rename(output)
    summary={'schema_version':1,'checkpoint':'20','scope':'human_readable_CD1_text_code_and_images_for_OCR_reference',
             'output_root':output.relative_to(ROOT).as_posix(),'counts':counts,'inputs':inputs,
             'manifest':file_record((output/'manifest.json').relative_to(ROOT).as_posix(),(output/'manifest.json').read_bytes()),
             'limits':['paper_verification_pending','marked_gaps_are_not_inferred_text','eight_ownership_blockers_retained',
                       'deferred_vectors_not_repaired','TOC_links_not_guessed','historical_19b_records_unchanged']}
    if write_record:put(ROOT,RECORD.relative_to(ROOT),json_bytes(summary))
    elif output==OUTPUT:require(read(RECORD)==summary,'Reference summary differs from recorded result')
    print(json.dumps(counts,indent=2),flush=True)
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=OUTPUT)
    parser.add_argument('--write-record',action='store_true');args=parser.parse_args();build(args.output,args.write_record)


if __name__=='__main__':main()
