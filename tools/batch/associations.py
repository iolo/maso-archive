"""Review first-pass linked-topic failures and preserve auxiliary text separately."""
import argparse
from collections import Counter, defaultdict
from pathlib import Path
import json

from tools import inventory_cd1_processing as queue, inventory_cd1_rtf as inventory
from tools import recover_cd1_text as recovery, map_cd1_images as images
from tools.cd1_batch_core import inherited_states
from tools.cd1_batch_cache import Cache, key, write, verify
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import ROOT, require
from tools.validate_cd1_batch import check_topic
from tools.run_cd1_batch import read_json, POLICY
from maso_archive.reading_room_package import checked_file, file_record

FIRST_PASS = ROOT / 'data/catalog/batch-runs/cd1-full-pass.json'
RECORD = ROOT / 'data/catalog/batch-runs/cd1-association-review.json'
OUTPUT = ROOT / 'build/cd1-associations'
DISPOSITION = 'recover_separately; preserve source links; do not merge into article body or traverse related articles'


def review_links(data, exceptions, approved):
    topics = {t['id']: t for t in data['topics']}
    jobs = {j['id']: j for j in data['jobs']}
    owners = defaultdict(list)
    for job in jobs.values():
        for topic in job['source_topics']:
            owners[topic['id']].append(job['id'])
    selected = [e['job_id'] for e in exceptions if e['category'] == 'unreviewed_linked_content']
    require(len(selected) == len(set(selected)), 'Duplicate association retry candidate')
    edges, destinations, retries = [], {}, []
    for job_id in sorted(selected):
        job = jobs[job_id]
        owned = {s['id'] for s in job['source_topics']}
        targets, unresolved = set(), []
        for source in job['source_topics']:
            topic = topics[source['id']]
            require(all(source[k] == topic[k] for k in ('native', 'rtf', 'aliases')), 'Article source binding changed')
            for link in topic['links']:
                target = link['target_topic_id']
                if target in owned or target in approved or topics.get(target, {}).get('role') in ('navigation', 'application_resource_topic', 'formatting_separator'):
                    continue
                dest = topics.get(target)
                # Inventory labels alone are insufficient: reject any article owner,
                # unresolved context, missing alias or inconsistent incoming edge.
                safe = bool(dest and dest['role'] == 'linked_auxiliary_topic' and not owners[target]
                            and not dest['issue'] and not dest['owner_topic_id'] and len(dest['aliases']) == 1
                            and not dest['context_relation'].startswith('unresolved')
                            and topic['id'] in dest['incoming_topic_ids'])
                action = 'preserve_separate_auxiliary' if safe else 'needs_ownership_review'
                edge = {'job_id': job_id, 'source_topic_id': topic['id'], **link, 'action': action}
                edges.append(edge)
                if safe:
                    targets.add(target)
                    destinations[target] = dest
                else:
                    unresolved.append(edge)
        require(targets or unresolved, 'Recorded association failure has no unexplained links')
        retries.append({'job_id': job_id, 'article_id': job['candidate_article_id'], 'source_reference': job['source_reference'],
                        'issue_id': job['issue_id'], 'auxiliary_topic_ids': sorted(targets),
                        'unresolved_links': unresolved, 'status': 'association_policy_ready' if not unresolved else 'blocked',
                        'article_preparation': 'not_retried'})
    return edges, destinations, retries


def recover_auxiliary(stage, topic, rtf, state, codecs, media_manifest):
    span = topic['rtf']
    start, length = span['byte_offset'], span['byte_length']
    raw = rtf[start:start + length]
    require(len(raw) == length and digest(raw) == span['sha256'], 'Auxiliary source bytes changed')
    write(stage / 'source.rtf', raw)
    write(stage / 'source-topic.json', recovery.json_bytes(topic))
    write(stage / 'inherited-state.json', recovery.json_bytes(state))
    result = {'topic_id': topic['id'], 'rtf': span, 'media': [], 'disposition': DISPOSITION}
    try:
        require(not state['unknown'], 'Unsupported auxiliary inherited formatting')
        initial = {k: v for k, v in state.items() if k != 'unknown'}
        report = inventory.inspect_topic(raw, start, initial['character']['font_id'])
        report.update(ordinal=topic['native']['ordinal'], role='linked_auxiliary')
        write(stage / 'inventory.json', recovery.json_bytes(report))
        require(not report['issues'], 'Unsupported auxiliary controls')
        decoded = recovery.recover_topic(rtf, report, initial, codecs)
        write(stage / 'recovery.json', recovery.json_bytes(decoded))
        require(not decoded['issues'], 'Undecoded auxiliary text retained')
        require(all(p['terminated_by_par'] for p in decoded['paragraphs']), 'Unterminated auxiliary paragraph')
        result['source_check'] = check_topic(rtf, decoded, span)
        resources = sorted({r['object']['resource'] for p in decoded['paragraphs'] for r in p['runs'] if r['kind'] == 'object'})
        for name in resources:
            raw_media = images.checked_source(name, media_manifest)
            result['media'].append({'resource': name, 'sha256': digest(raw_media), 'status': 'source_preserved; auxiliary_rendering_deferred'})
        result.update(status='recovered', paragraphs=len(decoded['paragraphs']))
    except (ValueError, OSError, KeyError) as error:
        result.update(status='deferred', error_type=type(error).__name__, error=str(error))
    write(stage / 'disposition.json', recovery.json_bytes(result))
    return result


def build(write_record=False):
    data, manifest = queue.load_inventory(queue.OUTPUT)
    for record in manifest['inputs'].values():
        checked_file(ROOT, record)
    first = read_json(FIRST_PASS)
    execution = json.loads(checked_file(ROOT, first['execution_manifest']))
    run_root = ROOT / first['run_root']
    identity = json.loads(checked_file(run_root, execution['identity']))
    # Leave the first-pass pipeline and its reproduction commands intact.
    for path, sha in identity['pipeline_identity']['code'].items():
        require(digest((ROOT / path).read_bytes()) == sha, 'First-pass dependency changed: ' + path)
    coverage = ROOT / first['coverage_root']
    exception_file = next(r for r in first['outputs'] if r['path'] == 'exceptions.jsonl')
    exceptions = [json.loads(line) for line in checked_file(coverage, exception_file).splitlines()]
    policy = read_json(POLICY)
    edges, destinations, retries = review_links(data, exceptions, policy['auxiliaries'])
    rtf = (images.RAW / 'MASOCD.rtf').read_bytes()
    require(digest(rtf) == policy['source_rtf_sha256'], 'Original RTF changed')
    inputs = {'first_pass': file_record(FIRST_PASS.relative_to(ROOT).as_posix(), FIRST_PASS.read_bytes()),
              'queue_sha256': digest((queue.OUTPUT / 'manifest.json').read_bytes()),
              'shared_policy_sha256': digest(POLICY.read_bytes()), 'source_rtf_sha256': digest(rtf),
              'code_sha256': digest(Path(__file__).read_bytes())}
    cache = Cache(OUTPUT / 'stages', inputs)
    def produce(stage):
        states = inherited_states(rtf, [t['rtf']['byte_offset'] for t in destinations.values()])
        media_manifest = read_json(images.MANIFEST)
        results, decisions = [], {}
        for topic_id, topic in sorted(destinations.items()):
            result = recover_auxiliary(stage / 'topics' / str(topic['native']['ordinal']), topic, rtf,
                                       states[topic['rtf']['byte_offset']], {int(k): v for k,v in policy['default_font_codecs'].items()}, media_manifest)
            results.append(result)
            decisions[topic_id] = {'rtf': topic['rtf'], 'role': 'linked_auxiliary', 'aliases': topic['aliases'],
                                   'links': topic['links'], 'disposition': DISPOSITION}
        write(stage / 'policy.json', recovery.json_bytes({'version': 1, 'source_rtf_sha256': digest(rtf), 'auxiliaries': decisions}))
        write(stage / 'links.json', recovery.json_bytes(edges))
        write(stage / 'recoveries.json', recovery.json_bytes(results))
        write(stage / 'retry-queue.json', recovery.json_bytes(retries))
    path, checkpoint = cache.stage('review', inputs, produce)
    verify(path, checkpoint['fingerprint'])
    require(read_json(path / 'links.json') == edges and read_json(path / 'retry-queue.json') == retries, 'Cached associations differ')
    results = read_json(path / 'recoveries.json')
    require({r['topic_id'] for r in results} == set(destinations) and len(results) == len(destinations), 'Auxiliary population changed')
    for result in results:
        if result['status'] == 'recovered':
            topic = destinations[result['topic_id']]
            decoded = read_json(path / 'topics' / str(topic['native']['ordinal']) / 'recovery.json')
            require(check_topic(rtf, decoded, topic['rtf']) == result['source_check'], 'Auxiliary source audit changed')
    counts = {'affected_candidates': len(retries), 'blocking_link_occurrences': len(edges), 'auxiliary_topics': len(destinations),
              'leaf_topics': sum(not t['links'] for t in destinations.values()), 'topics_with_links': sum(bool(t['links']) for t in destinations.values()),
              'outgoing_links_preserved': sum(len(t['links']) for t in destinations.values()),
              'retry_states': dict(sorted(Counter(r['status'] for r in retries).items())),
              'recovery_states': dict(sorted(Counter(r['status'] for r in results).items())),
              'paragraphs': sum(r.get('paragraphs', 0) for r in results),
              'source_bytes_checked': sum(r.get('source_check', {}).get('accounted_bytes', 0) for r in results),
              'text_runs_checked': sum(r.get('source_check', {}).get('text_runs', 0) for r in results),
              'media_resources': len({m['resource'] for r in results for m in r['media']})}
    require((counts['affected_candidates'], counts['blocking_link_occurrences'], counts['auxiliary_topics']) == (470, 587, 111), 'First-pass association population changed')
    summary = {'schema_version': 1, 'checkpoint': '14a', 'inputs': inputs, 'first_pass_unchanged': first['execution_manifest'],
               'output_root': path.relative_to(ROOT).as_posix(), 'fingerprint': checkpoint['fingerprint'], 'counts': counts,
               'outputs': checkpoint['outputs'], 'limits': ['auxiliaries_remain_separate_from_article_bodies', 'outgoing_links_not_followed_recursively',
                'article_retries_have_separate_results', 'physical_and_semantic_review_pending', 'auxiliary_media_rendering_deferred']}
    if write_record:
        write(RECORD, recovery.json_bytes(summary))
    else:
        require(read_json(RECORD) == summary, 'Association audit differs from recorded result')
    print(json.dumps(counts, indent=2), flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-record', action='store_true')
    args = parser.parse_args()
    build(args.write_record)


if __name__ == '__main__':
    main()
