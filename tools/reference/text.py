"""Readable CD1 reference text: ordinary typography never splits encoded characters."""
from collections import Counter
from copy import deepcopy
import re

from tools import inventory_cd1_rtf as inventory
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require

# Source font declarations; these fonts can change character meaning.
SYMBOL_FONTS = {2, 14, 22, 23, 28, 30, 38, 82, 83, 91}
FIXED_FONTS = {8, 13, 15, 20, 21, 24, 27, 31, 34, 36, 40, 46, 47, 48,
               56, 57, 58, 62, 64, 65, 67, 68, 69, 73, 90}
COSMETIC = set('fi fs keepn li qr qc ql qj ri sa sb sl tx tqc tqr cf i b ul uldb '
               'intbl cellx trgaph trleft trowd'.split())


def decode_bytes(raw, font, issues, offset):
    """Decode every supported byte, leaving local, explicit markers for gaps."""
    if font in SYMBOL_FONTS:
        if raw.strip():
            issues.append({'kind':'symbol_font_ambiguous','font_id':font,'byte_offset':offset,'bytes_hex':raw.hex()})
            return f'⟦symbol font {font}: {raw.hex()}⟧'
        return raw.decode('ascii')
    parts=[];cursor=0
    while cursor < len(raw):
        try:
            parts.append(raw[cursor:].decode('cp949'));break
        except UnicodeDecodeError as error:
            start=cursor+error.start;end=cursor+error.end
            parts.append(raw[cursor:start].decode('cp949'))
            encoded=raw[start:end].hex()
            parts.append(f'⟦bytes:{encoded}⟧')
            issues.append({'kind':'undecoded_bytes','source_buffer_byte_offset':offset,
                           'decoded_buffer_byte_index':start,'bytes_hex':encoded})
            cursor=end
    text=''.join(parts)
    # Expose controls that cannot be inspected visually; keep line breaks and tabs.
    for c in text:
        if ord(c)<32 and c not in '\n\t':
            issues.append({'kind':'embedded_control','source_buffer_byte_offset':offset,'code':ord(c)})
    return ''.join(c if c in '\n\t' or ord(c)>=32 else f'⟦control:{ord(c):02x}⟧' for c in text)


def recover(rtf, source, initial_font=4):
    span=source['rtf'];base=span['byte_offset'];end=base+span['byte_length'];raw=rtf[base:end]
    require(digest(raw)==span['sha256'],'Reference source changed')
    tokens=inventory.tokenize(raw,base)
    normalizations=Counter();issues=[]
    # The last native topic includes the document's closing brace, not a new body.
    group_tokens=tokens
    if tokens and tokens[-1]['kind']=='group_close' and end==len(rtf.rstrip()):
        group_tokens=tokens[:-1];normalizations['document_closing_brace']=1
    groups=inventory.group_records(raw,group_tokens,base)
    top={g['byte_offset']:g for g in groups if g['parent_byte_offset'] is None}
    require(all(g['role'] in ('metadata_marker','metadata_footnote','hidden_context_link') for g in top.values()),
            'Unclassified destination requires an explicit reading rule')
    objects={o['byte_offset']:o for o in inventory.object_records(raw,tokens,base)}
    paragraphs=[];runs=[];buffer=bytearray();fragments=[];fonts=set();font=initial_font
    paragraph_start=base;buffer_font=font

    def flush():
        nonlocal buffer_font
        if not buffer:return
        text=decode_bytes(bytes(buffer),buffer_font,issues,fragments[0]['byte_offset'])
        runs.append({'type':'text','text':text,'source_fragments':deepcopy(fragments)})
        buffer.clear();fragments.clear();buffer_font=font

    def add(data,token):
        nonlocal buffer_font
        if not buffer:buffer_font=font
        buffer.extend(data)
        fragments.append({'byte_offset':token['byte_offset'],'byte_length':token['byte_length'],'font_id':font})
        if data.strip():fonts.add(font)

    def paragraph(stop,terminated=True):
        nonlocal runs,paragraph_start,fonts
        flush()
        paragraphs.append({'id':f"T{source['native']['ordinal']}:P{len(paragraphs)+1}",
                           'source_span':{'byte_offset':paragraph_start,'end_exclusive':stop},
                           'runs':runs,'preformatted':(bool(fonts) and fonts<=FIXED_FONTS) or
                           any('\t' in r.get('text','') for r in runs),
                           'terminated':terminated})
        runs=[];fonts=set();paragraph_start=stop

    index=0
    while index<len(tokens):
        token=tokens[index];start=token['byte_offset'];kind=token['kind'];length=token['byte_length']
        if start in top or start in objects:
            flush();item=top.get(start) or objects[start];stop=start+item['byte_length']
            if start in objects:
                runs.append({'type':'media','resource':item['resource'],'source_span':{'byte_offset':start,'end_exclusive':stop}})
            while index<len(tokens) and tokens[index]['byte_offset']<stop:index+=1
            continue
        if kind=='physical_newline':pass
        elif kind in ('text_bytes','hex_byte'):
            data=rtf[start:start+length] if kind=='text_bytes' else bytes([int(rtf[start+2:start+4],16)])
            add(data,token)
        elif kind=='control_symbol':
            symbol=token['symbol']
            if symbol in '\\{}':add(symbol.encode(),token)
            elif symbol=='-' and index and tokens[index-1].get('symbol')=='{' and tokens[index-1]['byte_offset']+tokens[index-1]['byte_length']==start:
                normalizations['helpdeco_brace_guard']+=1
            else:
                flush();runs.append({'type':'text','text':f'⟦RTF symbol:{symbol}⟧'})
                issues.append({'kind':'unknown_control_symbol','symbol':symbol,'byte_offset':start})
        elif kind=='control_word':
            word=token['word'];value=token['parameter']
            if word in ('f','plain'):
                new=4 if word=='plain' else value
                require(isinstance(new,int) and 0<=new<=99,'Unknown source font')
                if new!=font:
                    if font in SYMBOL_FONTS or new in SYMBOL_FONTS:flush()
                    normalizations['font_changes']+=1
                font=new
            elif word in ('par','row'):
                paragraph(start+length);normalizations[word]+=1
            elif word in ('tab','cell','line'):
                add(b'\n' if word=='line' else b'\t',token);normalizations[word]+=1
            elif word=='pard' or word in COSMETIC:
                normalizations[word]+=1
            else:
                flush();runs.append({'type':'text','text':f'⟦RTF control:{word}⟧'})
                issues.append({'kind':'unknown_control','word':word,'byte_offset':start})
        elif kind=='group_close' and index==len(tokens)-1 and normalizations['document_closing_brace']:
            pass
        else:
            raise ValueError('Unrepresented RTF token: '+kind)
        index+=1
    flush()
    if runs:
        paragraph(end,False);normalizations['unterminated_final_paragraph']+=1
    return {'topic_id':source['id'],'source':span,'paragraphs':paragraphs,'issues':issues,
            'normalizations':dict(sorted(normalizations.items())),
            'source_bytes':sum(t['byte_length'] for t in tokens)}


def paragraph_text(paragraph):
    return ''.join(r['text'] if r['type']=='text' else f"[image:{r['resource']}]" for r in paragraph['runs'])


def text_for(paragraphs):
    return ''.join(paragraph_text(p)+('\n' if p.get('terminated',True) else '') for p in paragraphs)
