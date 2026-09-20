"""Reversible glyph adapter and independent source checks for CD1 9208198 only."""
from collections import Counter
from copy import deepcopy

from tools.batch import symbol_review
from tools import recover_cd1_text as recovery
from tools.validate_cd1_batch import run_bytes
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require

REFERENCE = '9208198'
ENCODING = 'cd1_symbol_arrows_v1'
GLYPHS = {0x20: ' ', 0xac: '←', 0xad: '↑', 0xae: '→'}


def decode(raw):
    require(raw and all(b in GLYPHS for b in raw), 'Unreviewed Symbol arrow byte')
    return ''.join(GLYPHS[b] for b in raw)


def encode(text):
    inverse = {v:k for k,v in GLYPHS.items()}
    require(text and all(c in inverse for c in text), 'Unreviewed Symbol arrow glyph')
    return bytes(inverse[c] for c in text)


def make_policy(job, evidence):
    require(job['source_reference'] == REFERENCE, 'Article outside Symbol arrow scope')
    table = symbol_review.mapping_table()
    require(all(c in table[b] for b,c in GLYPHS.items()), 'Pinned Symbol mapping differs')
    require(len(evidence) == 8 and all(e['reference'] == REFERENCE and
            e['decision'] == 'deferred_symbol_decoder_required' and not e['policy_approved'] for e in evidence),
            'Arrow review population or prior disposition changed')
    runs = [e['source_run'] for e in evidence]
    require(len({tuple((s['byte_offset'],s['byte_length']) for s in r['source_spans']) for r in runs}) == 8, 'Duplicate arrow span')
    require(all(r['kind'] == 'unsupported' and r['reason'] == 'Unsupported font 2' and
                r['format']['font_id'] == 2 for r in runs), 'Unreviewed arrow font or error')
    counts = Counter(b for r in runs for b in bytes.fromhex(r['original_bytes_hex']))
    require(counts == {0x20:95, 0xac:2, 0xad:1, 0xae:6}, 'Arrow byte population changed')
    require({e['topic_id'] for e in evidence} <= {t['id'] for t in job['source_topics']}, 'Arrow review topic changed')
    return {'reference':REFERENCE, 'encoding':ENCODING, 'source_topics':deepcopy(job['source_topics']),
            'runs':[{k:deepcopy(e[k]) for k in ('reference','topic_id','paragraph','run','source_run')} for e in evidence], 'mapping':{f'{b:02x}':c for b,c in GLYPHS.items()},
            'space_policy':'literal_RTF_20_to_U0020_without_reflow', 'mapping_sha256':symbol_review.MAPPING_SHA256}


def source_for(topic, policy):
    require(policy['reference'] == REFERENCE and policy['encoding'] == ENCODING and
            policy['mapping'] == {f'{b:02x}':c for b,c in GLYPHS.items()} and
            policy['mapping_sha256'] == symbol_review.MAPPING_SHA256 and
            policy['space_policy'] == 'literal_RTF_20_to_U0020_without_reflow', 'Unreviewed arrow policy')
    selected = [s for s in policy['source_topics'] if s['native']['ordinal'] == topic['ordinal'] and
                topic['source_span'] == {'byte_offset':s['rtf']['byte_offset'], 'end_exclusive':s['rtf']['byte_offset']+s['rtf']['byte_length']}]
    require(len(selected) == 1, 'Topic outside exact arrow source association')
    return selected[0]


def expected_topic(original, policy):
    source = source_for(original, policy)
    decisions = [e for e in policy['runs'] if e['topic_id'] == source['id']]
    result = deepcopy(original); seen=[]; issues=[]
    for p in result['paragraphs']:
        for n,run in enumerate(p['runs'],1):
            if run['kind'] != 'unsupported': continue
            matches=[e for e in decisions if e['paragraph']==p['ordinal'] and e['run']==n and e['source_run']==run]
            require(len(matches)==1, 'Run outside exact reviewed arrow source span')
            seen.append(matches[0]); issues.append({'source_spans':deepcopy(run['source_spans']), 'reason':run['reason']})
            raw=bytes.fromhex(run['original_bytes_hex']); text=decode(raw)
            require(encode(text)==raw, 'Arrow round-trip mismatch')
            run.pop('reason')
            # Keep original bytes as well as the span/hash, and name the glyph encoding honestly.
            run.update(kind='text',text=text,encoding=ENCODING)
        p['text']=''.join(r['text'] for r in p['runs'])
    require(seen==decisions and original['issues']==issues, 'Incomplete arrow population or unrelated source issue')
    result['issues']=[]
    return result


def recover_topic(rtf, report, initial, codecs, policy):
    require(2 not in codecs, 'A byte codec must not reinterpret Symbol arrow runs')
    original=recovery.recover_topic(rtf,report,initial,codecs)
    source=source_for(original,policy); span=source['rtf']
    require(digest(rtf[span['byte_offset']:span['byte_offset']+span['byte_length']])==span['sha256'], 'Arrow source bytes changed')
    return expected_topic(original,policy)


def check_topic(rtf, topic, span, policy):
    """Reconstruct source bytes independently, then verify glyphs and reverse mapping."""
    source=source_for(topic,policy)
    require(span==source['rtf'], 'Source checker association changed')
    start,length=span['byte_offset'],span['byte_length']
    require(digest(rtf[start:start+length])==span['sha256'] and not topic['issues'], 'Changed or undecoded arrow topic')
    cursor=start; runs=objects=arrow_runs=0; fonts=Counter(); glyphs=Counter(); seen=[]
    decisions=[e for e in policy['runs'] if e['topic_id']==source['id']]
    table=symbol_review.mapping_table()
    for item in topic['accounting']:
        require(item['byte_offset']==cursor, 'Source accounting gap/overlap')
        cursor+=item['byte_length']
    require(cursor==start+length, 'Incomplete source accounting')
    for paragraph in topic['paragraphs']:
        require(paragraph['text']==''.join(r['text'] for r in paragraph['runs']), 'Paragraph projection changed')
        for n,run in enumerate(paragraph['runs'],1):
            if run['kind']=='text':
                if run['encoding']==ENCODING:
                    matches=[e for e in decisions if e['paragraph']==paragraph['ordinal'] and e['run']==n]
                    require(len(matches)==1, 'Unreviewed arrow run position')
                    old=matches[0]['source_run']
                    require({k:v for k,v in run.items() if k not in ('kind','text','encoding')} ==
                            {k:v for k,v in old.items() if k not in ('kind','text','encoding','reason')}, 'Arrow source or formatting fields changed')
                    raw=bytes.fromhex(old['original_bytes_hex'])
                    # Latin-1 is only a temporary transport for the frozen RTF-span reconstructor.
                    actual=run_bytes(rtf,{**run,'text':raw.decode('latin1'),'encoding':'latin1'})
                    require(encode(run['text'])==actual, 'Arrow glyphs do not reproduce source bytes')
                    require(len(actual)==len(run['text']) and all(
                        c in table[b] and (b!=0x20 or c==' ') for b,c in zip(actual,run['text'])), 'Glyph differs from pinned Symbol reference')
                    seen.append(matches[0]); arrow_runs+=1; glyphs.update(run['text'])
                else:
                    require(run['format']['font_id']!=2, 'Symbol run mislabeled with an ordinary codec')
                    run_bytes(rtf,run)
                runs+=1; fonts[str(run['format']['font_id'])]+=1
            else:
                require(run['kind']=='object','Unsupported run reached source validation'); objects+=1
    require(seen==decisions, 'Missing or reordered arrow runs')
    return {'ordinal':topic['ordinal'],'source':span,'accounted_bytes':length,'paragraphs':len(topic['paragraphs']),
            'text_runs':runs,'objects':objects,'font_runs':dict(sorted(fonts.items())),
            'symbol_arrow_runs':arrow_runs,'symbol_glyph_counts':dict(sorted(glyphs.items())),
            'symbol_validation':'exact_reviewed_spans_reference_glyphs_and_reverse_bytes'}
