"""Check portable reference links and text/listing exports without legacy typography gates."""
import argparse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit

from tools.reference.export import OUTPUT,read
from tools.reference.text import text_for
from tools.map_cd1_topic import require
from maso_archive.reading_room_package import checked_file


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.links=[];self.ids=set();self.code=[];self.in_code=False
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:
            require(attrs['id'] not in self.ids,'Duplicate HTML anchor');self.ids.add(attrs['id'])
        self.links.extend(attrs[k] for k in ('href','src') if k in attrs)
        require(tag not in ('script','iframe','object','embed'),'Active reference content')
        if tag=='code':self.code.append('');self.in_code=True
    def handle_endtag(self,tag):
        if tag=='code':self.in_code=False
    def handle_data(self,data):
        if self.in_code:self.code[-1]+=data


def check(root=OUTPUT):
    root=Path(root).resolve();manifest=read(root/'manifest.json')
    require(manifest['kind']=='cd1-readable-reference','Not a reference export')
    expected={r['path'] for r in manifest['files']}|{'manifest.json'}
    require(len(expected)==len(manifest['files'])+1,'Duplicate export file')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(actual==expected,'Export file inventory changed')
    pages={};links=0
    for row in manifest['files']:
        raw=checked_file(root,row)
        if row['path'].endswith('.html'):
            page=Page();page.feed(raw.decode('utf-8'));page.close();pages[(root/row['path']).resolve()]=page
    for path,page in pages.items():
        for target in page.links:
            parsed=urlsplit(target)
            require(not parsed.scheme and not parsed.netloc,'Non-local reference link')
            resolved=(path.parent/unquote(parsed.path)).resolve() if parsed.path else path
            require(resolved.is_relative_to(root) and resolved.is_file(),'Missing/outside local link: '+str(path.relative_to(root))+' -> '+target)
            if parsed.fragment:require(resolved in pages and unquote(parsed.fragment) in pages[resolved].ids,'Missing local anchor')
            links+=1
    catalog=read(root/'catalog.json');listings=paragraphs=0
    for row in catalog:
        directory=(root/row['path']).parent;reference=read(directory/'reference.json')
        require(reference['reference']==row['reference'] and reference['status']==row['status'],'Reference identity changed')
        blocks=reference['blocks'];members=[p for b in blocks for p in b['paragraphs']]
        require(len(members)==row['paragraphs'],'Paragraph count changed')
        if row['text']:
            actual=(root/row['text']).read_text();require(actual==text_for(members),'Exported article text changed')
            mappings=read(directory/'paragraphs.json');require(len(mappings)==len(members),'Missing paragraph position')
            cursor=0;line=1
            for mapping,p in zip(mappings,members):
                value=text_for([p]);end=cursor+len(value)
                require(mapping['id']==p['id'] and mapping['character_offset']==cursor and mapping['characters']==len(value) and
                        mapping['first_line']==line and mapping['last_line']==line+value.count('\n')-int(value.endswith('\n')) and
                        actual[cursor:end]==value,'OCR paragraph position changed')
                cursor=end;line+=value.count('\n')
            require(cursor==len(actual),'Unmapped article text')
        else:require(not blocks and row['status'] in ('blocked','unavailable'),'Unexported readable content')
        pre=[b for b in blocks if b['preformatted']]
        require(len(pre)==len(reference['listings'])==row['listings'],'Listing count changed')
        shown=pages[(directory/'index.html').resolve()].code
        require(len(shown)==len(pre),'Missing HTML listing')
        for b,item,rendered in zip(pre,reference['listings'],shown):
            value=text_for(b['paragraphs'])
            require(item['block_id']==b['id'] and checked_file(directory,item).decode()==value==rendered,
                    'Listing characters/spacing differ across HTML and text')
        paragraphs+=len(members);listings+=len(pre)
    counts=manifest['counts']
    require(len(catalog)==counts['candidates'] and dict(Counter(r['status'] for r in catalog))==counts['article_status'],
            'Article population differs')
    require(paragraphs==counts['paragraphs'] and listings==counts['listing_files'],'Reference totals differ')
    result={'files_checked':len(expected),'html_pages':len(pages),'local_links_checked':links,
            'articles':len(catalog),'paragraphs':paragraphs,'listings':listings}
    print(result,flush=True);return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=OUTPUT)
    check(parser.parse_args().output)
