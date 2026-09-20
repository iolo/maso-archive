"""Export metadata-only decisions from the six reviewed February block maps."""
import json
from pathlib import Path
from tools.map_cd1_topic import ROOT, require
from tools.recover_cd1_text import json_bytes
from tools.decode_cd1_paragraph import digest
from maso_archive.reading_room_package import load_package, file_record, checked_file

OUTPUT = ROOT / 'data/catalog/batch-profiles/cd1-february.json'
BASELINE = ROOT / 'build/cd1-issues/1988-02-native/content'


def build():
    record = json.loads((ROOT / 'data/catalog/issue-packages/cd1-1988-02-native.json').read_bytes())
    for item in record['outputs']:
        checked_file(BASELINE, item)
    provenance = json.loads(checked_file(ROOT, record['provenance']))
    bundle, manifest, _ = load_package(BASELINE)
    jobs = [json.loads(line) for line in (ROOT / 'build/cd1-processing-inventory/jobs.jsonl').read_bytes().splitlines()]
    profiles, inputs = {}, {}
    for runtime in bundle['articles']:
        ref = runtime['source']['reference']
        path = ROOT / ('build/cd1-blocks/8802065/blocks.json' if ref == '8802065' else
                       'build/cd1-second-article/8802114/blocks.json' if ref == '8802114' else f'build/cd1-articles/{ref}/blocks.json')
        raw = path.read_bytes()
        mapping = json.loads(raw)
        inputs[str(path.relative_to(ROOT))] = file_record(str(path.relative_to(ROOT)), raw)
        job = next(j for j in jobs if j['candidate_article_id'] == runtime['id'])
        # Default paragraph/spacing blocks need no override. Parent hierarchy is
        # included for exceptions; ordinary children inherit their previous heading.
        decisions = []
        for block in mapping['blocks']:
            members = block['members']
            if (len(members) == 1 and block['kind'] in ('paragraph', 'spacing') and
                    not block['decision']['review_concerns'] and not block.get('representation')):
                continue
            properties = {k: v for k, v in block.items() if k not in ('id', 'topic_ordinal', 'members', 'source_span', 'content_sha256', 'object_refs')}
            decisions.append({'topic': block['topic_ordinal'], 'first': members[0]['paragraph_ordinal'],
                              'last': members[-1]['paragraph_ordinal'], 'properties': properties,
                              'content_sha256': block['content_sha256']})
        evidence = provenance['article_evidence'][ref]
        profiles[ref] = {'article_id': runtime['id'], 'source_topics': job['source_topics'],
                         'font_codecs': evidence.get('font_policy', {'4': 'cp949', '5': 'cp949', '6': 'cp949'}),
                         'decisions': decisions, 'relationships': mapping['relationships'],
                         'runtime_metadata': {k: v for k, v in runtime.items() if k not in ('sections', 'relationships')},
                         'article_sha256': digest(json_bytes(runtime))}
    return {'version': 1, 'baseline_record': 'data/catalog/issue-packages/cd1-1988-02-native.json',
            'baseline_record_sha256': digest(json_bytes(record)), 'inputs': inputs, 'articles': profiles}


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    raw = json_bytes(build())
    if args.write:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(raw)
    else:
        require(OUTPUT.read_bytes() == raw, 'Batch profiles differ from reviewed maps')
    print('Verified six source-bound February profiles')


if __name__ == '__main__':
    main()
