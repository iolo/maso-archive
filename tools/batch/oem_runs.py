"""Reversible CP437 only at reviewed CD1 literal spans; ordinary runs stay unchanged."""
from copy import deepcopy

from tools.batch import codec_review
from tools import recover_cd1_text as recovery
from tools.validate_cd1_batch import check_topic as check_source, run_bytes
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require


def source_for(topic, policy):
    require(policy['reference'] in codec_review.READY and policy['encoding']=='cp437' and
            policy['mapping_sha256']==codec_review.MAPPING_SHA256,'Unreviewed OEM policy')
    selected=[s for s in policy['source_topics'] if s['native']['ordinal']==topic['ordinal'] and
              topic['source_span']=={'byte_offset':s['rtf']['byte_offset'],'end_exclusive':s['rtf']['byte_offset']+s['rtf']['byte_length']}]
    require(len(selected)==1,'Topic outside exact OEM source association')
    return selected[0]


def expected_topic(original, policy):
    source=source_for(original,policy);table=codec_review.mapping_table()
    decisions=[r for r in policy['runs'] if r['topic_id']==source['id']]
    result=deepcopy(original);seen=[];issues=[]
    for p in result['paragraphs']:
        for n,run in enumerate(p['runs'],1):
            if run['kind']!='unsupported':continue
            matches=[r for r in decisions if r['paragraph']==p['ordinal'] and r['run']==n and r['source_run']==run]
            require(len(matches)==1,'Run outside exact reviewed OEM source span')
            text=codec_review.reviewed_oem_run(run,policy['reference']);raw=bytes.fromhex(run['original_bytes_hex'])
            require(text==''.join(table[b] for b in raw),'OEM glyph differs from reference')
            seen.append(matches[0]);issues.append({'source_spans':deepcopy(run['source_spans']),'reason':run['reason']})
            run.pop('reason');run.update(kind='text',text=text,encoding='cp437')
        p['text']=''.join(r['text'] for r in p['runs'])
    require(seen==decisions and original['issues']==issues,'Missing OEM decision or unrelated source issue')
    result['issues']=[]
    return result


def recover_topic(rtf, report, initial, codecs, policy):
    require(codecs.get(15)=='cp949','OEM adapter requires the original Fixedsys policy')
    original=recovery.recover_topic(rtf,report,initial,codecs)
    source=source_for(original,policy);span=source['rtf']
    require(digest(rtf[span['byte_offset']:span['byte_offset']+span['byte_length']])==span['sha256'],'OEM source changed')
    return expected_topic(original,policy)


def check_topic(rtf, topic, span, policy):
    source=source_for(topic,policy);require(source['rtf']==span,'OEM source association changed')
    checked=check_source(rtf,topic,span)
    decisions=[r for r in policy['runs'] if r['topic_id']==source['id']];seen=[]
    table=codec_review.mapping_table();glyphs={}
    for p in topic['paragraphs']:
        for n,run in enumerate(p['runs'],1):
            matches=[r for r in decisions if r['paragraph']==p['ordinal'] and r['run']==n]
            if not matches:
                require(run.get('encoding')!='cp437','Unreviewed OEM decoding outside policy')
                continue
            require(len(matches)==1 and run['kind']=='text' and run['encoding']=='cp437','Missing or mislabeled OEM run')
            old=matches[0]['source_run']
            require({k:v for k,v in run.items() if k not in ('kind','text','encoding')}==
                    {k:v for k,v in old.items() if k not in ('kind','text','encoding','reason')},'OEM source or formatting changed')
            raw=run_bytes(rtf,run)
            require(raw==bytes.fromhex(old['original_bytes_hex']) and run['text']==''.join(table[b] for b in raw),
                    'OEM source bytes or glyph mapping changed')
            require(run['text']==codec_review.reviewed_oem_run(old,policy['reference']),'Unreviewed OEM literal')
            for b in raw:
                if b>=128:glyphs[table[b]]=glyphs.get(table[b],0)+1
            seen.append(matches[0])
    require(seen==decisions,'Missing or reordered OEM runs')
    return {**checked,'oem_runs':len(seen),'oem_glyph_counts':dict(sorted(glyphs.items())),
            'oem_validation':'exact_literal_spans_reference_glyphs_and_reverse_bytes'}
