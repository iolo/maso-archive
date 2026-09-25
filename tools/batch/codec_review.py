"""Audit 37 existing-codec failures; authorize only exact reviewed OEM literal runs."""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import re

from tools.batch import font_review, font_declaration_review, symbol_arrow_pipeline
from tools.run_cd1_batch import ROOT, read_json
from tools.cd1_batch_core import inherited_states
from tools.cd1_batch_cache import Cache, key, verify, write
from tools import recover_cd1_text as recovery, inventory_cd1_rtf as inventory
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import require
from maso_archive.reading_room_package import checked_file, file_record

CURRENT = ROOT / 'data/catalog/batch-runs/cd1-symbol-pass.json'
RECORD = ROOT / 'data/catalog/batch-runs/cd1-codec-review.json'
OUTPUT = ROOT / 'build/cd1-codec-review'
MAPPING = ROOT / 'data/reference/microsoft-cp437.txt'
LICENSE = ROOT / 'data/reference/unicode-license-v3.txt'
MAPPING_SHA256 = '6bad4dabcdf5940227c7d81fab130dcb18a77850b5d79de28b5dc4e047b0aaac'
LICENSE_SHA256 = 'e7a93b009565cfce55919a381437ac4db883e9da2126fa28b91d12732bc53d96'
MAPPING_URL = 'https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/PC/CP437.TXT'
BOX = {0xb3:'│',0xba:'║',0xbf:'┐',0xc0:'└',0xc4:'─',0xd9:'┘',0xda:'┌'}
READY = {'8901200','8902178','8903170','8911214','9206396'}
SPLIT = {'8901110','9103202'}
SAMPLE = {'8901200':'eight Pascal frame literals', '8911214':'five assembly border literals',
          '9206396':'three horizontal box bytes in a printf marker'}


def mapping_table():
    raw=MAPPING.read_bytes()
    require(digest(raw)==MAPPING_SHA256 and digest(LICENSE.read_bytes())==LICENSE_SHA256,'Reference bytes changed')
    table={int(p[0],16):chr(int(p[1],16)) for line in raw.decode('ascii').splitlines()
           if line and line != '\x1a' and not line.startswith('#') for p in [line.split()]}
    require(len(table)==256 and all(bytes([b]).decode('cp437')==c for b,c in table.items()),'CP437 implementation differs from reference')
    require(all(table[b]==c for b,c in BOX.items()),'Reviewed box glyph differs')
    return table


def attempt(raw, codec):
    """Diagnostic candidates only; success and round-trip never authorize text."""
    try:
        text=raw.decode(codec,errors='strict')
        return {'status':'decoded_candidate','text':text,'round_trip':text.encode(codec)==raw,'approved':False}
    except UnicodeDecodeError as error:
        return {'status':'decode_error','start':error.start,'end':error.end,'bytes_hex':raw[error.start:error.end].hex(),
                'reason':error.reason,'approved':False}
    except UnicodeEncodeError:
        return {'status':'non_round_trip_candidate','text':text,'round_trip':False,'approved':False}


def boundary_candidates(paragraph):
    candidates=[]
    for n,(left,right) in enumerate(zip(paragraph['runs'],paragraph['runs'][1:]),1):
        if any(r['kind']!='unsupported' or r['encoding']!='cp949' for r in (left,right)):continue
        a,b=(bytes.fromhex(r['original_bytes_hex']) for r in (left,right))
        failure=attempt(a,'cp949');joined=attempt(a+b,'cp949')
        if (failure.get('reason')!='incomplete multibyte sequence' or failure.get('end')!=len(a) or
                joined['status']!='decoded_candidate' or not joined['round_trip']):continue
        try:
            if joined['text'].encode('euc_kr')!=a+b:continue
        except UnicodeError:continue
        candidates.append({'paragraph':paragraph['ordinal'],'runs':[n,n+1], 'joined_bytes_hex':(a+b).hex(),
            'candidate_text':joined['text'],'split_at_byte':len(a),'left_format':left['format'],'right_format':right['format'],
            'approved':False,'decision':'deferred_cross_font_character_representation'})
    return candidates


def reviewed_oem_run(run, reference):
    require(reference in READY and run['kind']=='unsupported' and run['format']['font_id']==15 and
            run['encoding']=='cp949','Run outside reviewed OEM scope')
    raw=bytes.fromhex(run['original_bytes_hex'])
    require(attempt(raw,'cp949')['status']=='decode_error','OEM policy cannot replace already decoded text')
    require(raw and any(b in BOX for b in raw) and all(32<=b<=126 or b in BOX for b in raw),'Unreviewed OEM repertoire')
    if reference in {'8901200','8902178','8903170'}:
        require(re.fullmatch(rb" *WriteStr\((?:i, y[12]|x[12], i|x[12], y[12]), '[\xb3\xbf\xc0\xc4\xd9\xda]'\);",raw) is not None,
                'Unreviewed Pascal frame literal')
    elif reference=='8911214':
        require(len(raw)==65 and raw.startswith(b"   db   '\xba") and raw.endswith(b"\xba', CR, LF") and raw.count(b'\xba')==2,
                'Unreviewed assembly border literal')
    else:
        require(raw.startswith(b'    printf("%#10ld <\xc4\xc4\xc4 %-60s') and
                raw.endswith(b'",sum_fsize,thisdir);') and sum(b>=128 for b in raw)==3,'Unreviewed printf marker')
    text=raw.decode('cp437')
    require(text.encode('cp437')==raw,'OEM run is not reversible')
    return text


def make_policy(job, rows):
    ref=job['source_reference'];require(ref in READY,'Article has no approved OEM policy')
    expected_runs=8 if ref.startswith('890') else 5 if ref=='8911214' else 1
    expected_bytes={0xc4:2,0xb3:2,0xda:1,0xc0:1,0xbf:1,0xd9:1} if ref.startswith('890') else {0xba:10} if ref=='8911214' else {0xc4:3}
    require(len(rows)==expected_runs and all(r['reference']==ref for r in rows),'OEM policy population changed')
    require(len({(r['topic_id'],r['paragraph'],r['run']) for r in rows})==len(rows),'Duplicate OEM decision')
    require({r['topic_id'] for r in rows}<={t['id'] for t in job['source_topics']},'OEM topic changed')
    counts=Counter()
    for row in rows:
        reviewed_oem_run(row['source_run'],ref)
        counts.update(b for b in bytes.fromhex(row['source_run']['original_bytes_hex']) if b>=128)
    require(counts==expected_bytes,'Reviewed OEM glyph population changed')
    return {'reference':ref,'encoding':'cp437','mapping_sha256':MAPPING_SHA256,'source_topics':deepcopy(job['source_topics']),
            'runs':[{k:deepcopy(row[k]) for k in ('reference','topic_id','paragraph','run','source_run')} for row in rows],
            'basis':'exact literal bytes and programming context; no font-wide fallback; physical verification pending'}


def audit(write_record=False):
    mapping_table();runner=symbol_arrow_pipeline.ArrowRunner(OUTPUT)
    current=read_json(CURRENT);prior=read_json(font_review.RECORD)
    require(current['pipeline_identity_sha256']==key(runner.identity),'18c pipeline changed')
    checked_file(ROOT,current['execution_manifest'])
    old_root=ROOT/prior['output_root'];manifest=verify(old_root,prior['fingerprint'])
    require(manifest['outputs']==prior['outputs'],'Original font review changed')
    selected=[j for j in read_json(old_root/'jobs.json') if 'existing_codec_failure' in j['classifications']]
    require(len(selected)==37 and len({j['job_id'] for j in selected})==37,'Existing-codec population changed')
    exception_file=next(r for r in current['outputs'] if r['path']=='exceptions.jsonl')
    exceptions={r['job_id']:r for line in checked_file(ROOT/current['coverage_root'],exception_file).splitlines() for r in [json.loads(line)]}
    require(all(exceptions[j['job_id']]['category']=='font_or_decoding_policy' for j in selected),'Reviewed case is not a current font failure')
    header=runner.rtf[:runner.rtf.index(b'\n{\\colortbl')]
    names={int(m[1]):m[2].decode('cp949') for m in re.finditer(rb'\{\\f(\d+)\\[a-z]+ ([^;]+);\}',header)}
    require({f:names[f] for f in (4,5,13,15)}=={4:'Arial',5:'굴림체',13:'Courier New',15:'Fixedsys'},'Font declarations changed')
    jobs={j['id']:j for j in runner.data['jobs']}
    dependencies={'pipeline':runner.identity,'current_record_sha256':digest(CURRENT.read_bytes()),
        'prior_review_sha256':digest(font_review.RECORD.read_bytes()),'code_sha256':digest(Path(__file__).read_bytes()),
        'retained_checker_sha256':digest(Path(font_declaration_review.__file__).read_bytes()),'mapping_sha256':MAPPING_SHA256,
        'license_sha256':LICENSE_SHA256,'ready':sorted(READY),'sample':SAMPLE}
    cache=Cache(OUTPUT/'stages',dependencies)
    def produce(stage):
        states=inherited_states(runner.rtf,[s['rtf']['byte_offset'] for row in selected for s in row['source_topics']])
        rows=[];evidence=[];boundaries=[];policies={}
        for original in selected:
            ref=original['source_reference'];job=jobs[original['job_id']]
            require(job['source_topics']==original['source_topics'] and checked_file(ROOT,original['source_evidence'])==recovery.json_bytes(job),'Source association changed')
            require(ref not in runner.policy['article_fonts'],'Review would replace an earlier policy')
            before=read_json(old_root/f'articles/{ref}/recovery.json')
            require(len(before['topics'])==len(job['source_topics']),'Incomplete original article')
            codecs={int(k):v for k,v in runner.policy['default_font_codecs'].items()}
            article_rows=[];article_boundaries=[];checks=[];recovered=[]
            for old,source in zip(before['topics'],job['source_topics']):
                span=source['rtf'];start=span['byte_offset'];raw=runner.rtf[start:start+span['byte_length']]
                require(digest(raw)==span['sha256'] and not states[start]['unknown'],'Changed source or inherited state')
                initial={k:v for k,v in states[start].items() if k!='unknown'}
                report=inventory.inspect_topic(raw,start,initial['character']['font_id'])
                report.update(ordinal=source['native']['ordinal'],role='reference_target_body' if source['id']==job['body_topic_id'] else 'linked_introduction')
                require(not report['issues'],'Source inventory changed')
                actual=recovery.recover_topic(runner.rtf,report,initial,codecs)
                require(actual==old,'Original recovery changed')
                recovered.append(actual);checks.append(font_declaration_review.retained_topic_checks(runner.rtf,actual,span))
                for i,p in enumerate(actual['paragraphs']):
                    splits=boundary_candidates(p)
                    for split in splits:article_boundaries.append({'reference':ref,'topic_id':source['id'],**split})
                    split_runs={n for split in splits for n in split['runs']}
                    for n,run in enumerate(p['runs'],1):
                        if run['kind']!='unsupported':continue
                        raw_run=bytes.fromhex(run['original_bytes_hex']);font=run['format']['font_id']
                        status=('source_bound_oem_run_ready' if ref in READY else 'deferred_cross_font_character_representation' if n in split_runs else
                                'deferred_additional_font_with_codec_failure' if font not in codecs else 'deferred_mixed_or_ambiguous_bytes')
                        row={'reference':ref,'job_id':job['id'],'topic_id':source['id'],'paragraph':p['ordinal'],'run':n,
                             'font_id':font,'font_name':names[font],'active_codec':codecs.get(font),'source_run':run,
                             'decision':status,'approved':ref in READY,'context':actual['paragraphs'][max(0,i-1):i+2],
                             'attempts':{codec:attempt(raw_run,codec) for codec in ('cp949','euc_kr','cp437','cp1252')},
                             'interpretation':'Only an exact reviewed policy authorizes text; candidate success alone is insufficient'}
                        article_rows.append(row)
            status='source_bound_oem_policy_ready' if ref in READY else 'deferred_cross_font_character_representation' if ref in SPLIT else 'deferred_mixed_or_ambiguous_source'
            if ref in READY:policies[ref]=make_policy(job,article_rows)
            if ref in SPLIT:require(len(article_boundaries)==1 and len(article_rows)==2,'Split-character population changed')
            require(ref in SPLIT or not article_boundaries,'Unreviewed split-character case')
            write(stage/f'articles/{ref}/recovery.json',recovery.json_bytes({**before,'topics':recovered}))
            evidence.extend(article_rows);boundaries.extend(article_boundaries)
            rows.append({'job_id':job['id'],'source_reference':ref,'source_topics':job['source_topics'],'status':status,
                         'source_checks':checks,'runs':len(article_rows),'bytes':sum(r['source_run']['encoded_bytes'] for r in article_rows),
                         'run_decisions':dict(sorted(Counter(r['decision'] for r in article_rows).items()))})
            print(ref+': '+status,flush=True)
        require(len(evidence)==185 and sum(r['active_codec']=='cp949' for r in evidence)==184 and
                set(policies)==READY and len(boundaries)==2,'Review population changed')
        for name,value in [('jobs',rows),('runs',evidence),('boundaries',boundaries),('policy',{'source_rtf_sha256':digest(runner.rtf),'articles':policies})]:
            write(stage/(name+'.json'),recovery.json_bytes(value))
    path,manifest=cache.stage('review',{},produce)
    rows=read_json(path/'jobs.json');runs=read_json(path/'runs.json')
    summary={'schema_version':1,'checkpoint':'19a','scope':'37_existing_codec_failures_source_review',
        'pipeline_identity_sha256':key(runner.identity),'code_sha256':dependencies['code_sha256'],
        'current_record':file_record(CURRENT.relative_to(ROOT).as_posix(),CURRENT.read_bytes()),
        'prior_review_record':file_record(font_review.RECORD.relative_to(ROOT).as_posix(),font_review.RECORD.read_bytes()),
        'mapping_reference':{'url':MAPPING_URL,'retrieved':'2026-09-25','file':file_record(MAPPING.relative_to(ROOT).as_posix(),MAPPING.read_bytes()),
                             'license':file_record(LICENSE.relative_to(ROOT).as_posix(),LICENSE.read_bytes()),
                             'applicability':'exact source literals plus programming context; physical verification pending'},
        'output_root':path.relative_to(ROOT).as_posix(),'fingerprint':manifest['fingerprint'],'outputs':manifest['outputs'],
        'approved_references':sorted(READY),'split_character_references':sorted(SPLIT),'fixed_sample':SAMPLE,
        'counts':{'articles':len(rows),'topics':sum(len(r['source_topics']) for r in rows),'runs':len(runs),
                  'encoded_bytes':sum(r['source_run']['encoded_bytes'] for r in runs),
                  'job_states':dict(sorted(Counter(r['status'] for r in rows).items())),
                  'run_decisions':dict(sorted(Counter(r['decision'] for r in runs).items())),
                  'font_runs':dict(sorted(Counter(str(r['font_id']) for r in runs).items())),
                  'codec_errors':dict(sorted(Counter(r['attempts']['cp949'].get('reason','not_a_codec_error') for r in runs).items()))},
        'limits':['exact_literal_runs_only','no_global_codec_fallback','no_replacement_or_source_repair','cross_font_character_representation_deferred',
                  'mixed_or_ambiguous_bytes_retained','18c_combined_coverage_unchanged','physical_verification_pending']}
    if write_record:write(RECORD,recovery.json_bytes(summary))
    else:require(summary==read_json(RECORD),'Codec review differs from record')
    print(json.dumps(summary['counts'],indent=2),flush=True)
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write-record',action='store_true')
    audit(parser.parse_args().write_record)
