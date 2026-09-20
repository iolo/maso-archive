"""Step 13a: reconcile CD1 sources into a metadata-only batch input inventory.

No article recovery, semantic classification, conversion, or packaging is run.
Ready means eligible for the later runner's source checks, not extraction-verified.
"""

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import json
from pathlib import Path
import re
import sys
import tempfile

from maso_archive.cd1_index import INDEX_NAMES, group_references, parse_index
from maso_archive.reading_room_package import checked_file, file_record, load_package
from maso_archive.toc import assign_identities, finalize_entries, parse_toc, atomic_write
from tools import close_cd1_february as february
from tools import map_cd1_topic as native
from tools.decode_cd1_paragraph import digest
from tools.recover_cd1_text import json_bytes
from tools.verify_cd1_match import checked_artifact

ROOT = native.ROOT
OUTPUT = ROOT / 'build/cd1-processing-inventory'
RECORD = ROOT / 'data/catalog/processing-inventories/cd1.json'
VERSION = '1.0.0'
LINK = re.compile(rb'\{\\v ([^}]+)\}')
CONTROL = re.compile(rb'(?<!\\)\\([a-zA-Z]+)(-?\d+)? ?')
PAGE = re.compile(rb'(?<![0-9])([0-9]{2})\.\s*([0-9]{1,2})\.?\s+([0-9]+)[pP]\b')
OBJECT = re.compile(rb'\\\{(?:bmc ([A-Za-z0-9_.-]+)|ewl mvbmp2, ViewerBmp2, +!([A-Za-z0-9_.-]+))\\\}')
BLANK_CONTROLS = set('pard plain f fs b ul par li ri sa sb sl tx qc qr keepn cf tqc'.split())
# Frozen after metadata inspection, before any cross-issue article recovery.
SAMPLE_REASONS = {
    185: '1988 unindexed native identity; short bitmap-bearing topic',
    302: '1989 math-library title; font 15 and numerous vector occurrences',
    1150: '1990 long font-15 topic; bitmap/vector mix and interior context offset',
    1433: '1991 additional font 26 and vector-heavy topic',
    2182: '1992 suffixed reference and font-15 content',
    2502: '1993 short suffixed reference; opening label omits month trailing period',
    2611: '1993 additional font 95 and bitmap-heavy topic',
    2985: '1993 supplement with no numeric opening page; many bitmap occurrences',
    3049: 'December 1993 long font-15 topic and interior context offset',
}
SAMPLE_ORDINALS = list(SAMPLE_REASONS)
OUTPUT_NAMES = {'topics.jsonl': 'topics', 'contexts.jsonl': 'contexts',
                'index-references.jsonl': 'references', 'index-entries.jsonl': 'entries',
                'jobs.jsonl': 'jobs', 'toc-coverage.jsonl': 'toc',
                'issues.json': 'issues', 'review-items.json': 'review_items'}
require = native.require


def histogram(values):
    return dict(sorted(Counter(values).items()))


def topic_id(ordinal):
    return f'cd1:topic:{ordinal:04d}'


def job_id(row):
    return 'cd1:job:' + row['context']['hash_hex'][2:]


def screening(raw):
    """Lexical feature hints select a sample; they are not a semantic block map."""
    controls = list(CONTROL.finditer(raw))
    resources = [next(v for v in m.groups() if v).decode('ascii') for m in OBJECT.finditer(raw)]
    words = {m[1].decode('ascii') for m in controls}
    return {'font_ids': sorted({int(m[2]) for m in controls if m[1] == b'f' and m[2]}),
            'control_words': sorted(words), 'par_controls': sum(m[1] == b'par' for m in controls),
            'tab_controls': sum(m[1] == b'tab' for m in controls),
            'resources': sorted(set(resources)), 'object_occurrences': len(resources),
            'media_extensions': histogram(Path(p).suffix.lower() for p in resources),
            'blank_formatting_only': bool(re.fullmatch(rb'(?:\\[a-zA-Z]+-?\d* ?|\s|[{}])*', raw)) and
                                     words <= BLANK_CONTROLS}


def opening_page(raw, start):
    first = re.search(rb'(?<!\\)\\par\b', raw)
    matches = list(PAGE.finditer(raw[:first.start()] if first else raw))
    if len(matches) != 1:
        return {'status': 'missing' if not matches else 'ambiguous', 'issue': None, 'page': None}
    match = matches[0]
    return {'status': 'observed', 'issue': f'19{match[1].decode()}-{int(match[2]):02d}',
            'page': int(match[3]), 'label': match[0].decode('ascii'),
            'byte_offset': start + match.start(), 'byte_length': len(match[0])}


def context_relation(offset, start, end):
    if offset == start:
        return 'at_native_header'
    if start < offset and end is not None and offset < end:
        return 'inside_native_topic_interval'
    return 'unresolved_outside_native_interval'


def toc_relation(job, entries, prepared=None):
    if prepared:
        ids = prepared['toc_entry_ids']
        require(ids and all(any(e['id'] == key and e['issue_id'] == job['issue_id'] for e in entries) for key in ids),
                'Prepared TOC identity/issue changed')
        return {'status': 'reviewed_preparation', 'matched_ids': ids, 'candidate_ids': ids,
                'basis': 'preserved_February_preparation_evidence'}
    rows = [e for e in entries if e['issue_id'] == job['issue_id'] and e['kind_candidate'] != 'section']
    titles = {job['title'], *job['index_titles']}
    candidates = [e for e in rows if e['title_candidate'] in titles]
    page = job['opening_page']['page'] if job['opening_page']['issue'] == job['issue_id'].removeprefix('maso-') else None
    supported = [e for e in candidates if page is not None and e['start_page_candidate'] == page]
    matched = [supported[0]['id']] if len(supported) == 1 else []
    return {'status': 'supported_by_metadata' if matched else 'needs_review' if candidates else 'no_exact_title_match',
            'matched_ids': matched, 'candidate_ids': [e['id'] for e in candidates],
            'basis': 'exact_native_or_index_title_and_explicit_issue_page' if matched else 'no_fuzzy_or_reference_suffix_match',
            'candidate_evidence': [{'toc_entry_id': e['id'], 'title': e['title_candidate'],
                                    'toc_page': e['start_page_candidate'], 'opening_page': page,
                                    'page_agrees': page == e['start_page_candidate'] if page is not None else None}
                                   for e in candidates]}


def reconcile(mvb, rtf, toc, entries, references, prepared):
    _, scanned = february.scan_native(mvb, rtf)
    contexts = native.context_entries(mvb)
    rows = deepcopy(scanned)
    alias_topics = {}
    raw_topics = {}
    for row in rows:
        ordinal = row['native']['ordinal']
        span = row['rtf']
        raw = rtf[span['byte_offset']:span['byte_offset'] + span['byte_length']]
        raw_topics[ordinal] = raw
        row.update(id=topic_id(ordinal), aliases=[m[1].decode('ascii') for m in native.CONTEXT_FOOTNOTE.finditer(raw)],
                   links=[{'alias': m[1].decode('ascii'), 'byte_offset': span['byte_offset'] + m.start(),
                           'byte_length': len(m[0])} for m in LINK.finditer(raw)], features=screening(raw))
        require(len(row['aliases']) <= 1, 'Multiple topic aliases need review')
        for alias in row['aliases']:
            key = native.context_hash(alias)
            require(key not in alias_topics and key in contexts, 'Duplicate or missing native alias')
            alias_topics[key] = ordinal
    require(set(alias_topics) == set(contexts), 'Native context/alias population differs')
    context_rows = []
    for key, ordinal in sorted(alias_topics.items()):
        row = rows[ordinal - 1]
        end = rows[ordinal]['native']['topic_offset'] if ordinal < len(rows) else None
        relation = context_relation(contexts[key]['topic_offset'], row['native']['topic_offset'], end)
        row['context_relation'] = relation
        context_rows.append({**contexts[key], 'alias': row['aliases'][0], 'topic_id': row['id'],
                             'native_header_topic_offset': row['native']['topic_offset'],
                             'next_header_topic_offset': end, 'association': relation})
    incoming = defaultdict(list)
    for row in rows:
        for link in row['links']:
            ordinal = alias_topics.get(native.context_hash(link['alias']))
            link['target_topic_id'] = topic_id(ordinal) if ordinal else None
            if ordinal:
                incoming[ordinal].append(row['id'])
    by_reference = defaultdict(list)
    by_entry = {e['id']: e for e in entries}
    reference_rows = []
    for reference in references:
        ordinal = alias_topics.get(native.context_hash(reference['reference']))
        row = rows[ordinal - 1] if ordinal else None
        occurrences = [by_entry[key] for key in reference['occurrence_ids']]
        labels = sorted({o['display_issue'] for o in occurrences if o['display_issue']})
        state = ('article_topic' if row['issue'] else 'navigation_topic' if ordinal in february.NAVIGATION
                 else 'undated_topic_needs_review') if row else 'unresolved_target'
        ref = {**reference, 'topic_id': row['id'] if row else None, 'native_context': contexts.get(native.context_hash(reference['reference'])),
               'target_status': state, 'display_issues': labels,
               'issue_conflict': bool(row and row['issue'] and
                                      any(issue != row['issue'] for issue in [*labels, reference['issue_candidate']] if issue))}
        reference_rows.append(ref)
        if ordinal:
            by_reference[ordinal].append(ref)
    require(all(len(value) == 1 for value in by_reference.values()), 'Multiple index identities for one topic need explicit policy')
    review_items = []
    intro_owners = {}
    for row in rows:
        if not row['issue']:
            continue
        ordinal = row['native']['ordinal']
        if ordinal > 1 and any(link['target_topic_id'] == topic_id(ordinal - 1) for link in row['links']):
            previous = rows[ordinal - 2]
            if previous['aliases'] and not previous['title'] and not previous['issue']:
                intro_owners[ordinal - 1] = row['id']
    for row in rows:
        ordinal = row['native']['ordinal']
        row['incoming_topic_ids'] = sorted(set(incoming[ordinal]))
        row['owner_topic_id'] = None
        if row['issue']:
            row['role'] = 'dated_article_candidate'
        elif ordinal in february.NAVIGATION:
            row['role'] = 'navigation'
        elif ordinal in intro_owners:
            row['role'] = 'linked_introduction_candidate'
            row['owner_topic_id'] = intro_owners[ordinal]
        elif row['features']['blank_formatting_only']:
            row['role'] = 'formatting_separator'
        elif ordinal in (2, 5, 6) and re.search(rb'\\\{ew[cl] ', raw_topics[ordinal]):
            row['role'] = 'application_resource_topic'
        elif row['aliases'] and ordinal <= 134 and incoming[ordinal]:
            row['role'] = 'linked_auxiliary_topic'
        else:
            row['role'] = 'unattributed_content'
            review_items.append({'id': f'cd1-inventory-topic-{ordinal:04d}', 'kind': 'unattributed_content',
                                 'topic_ids': [row['id']], 'status': 'needs_review',
                                 'reason': 'Content has no reviewed owner; adjacency alone is not an article boundary.'})
    jobs = []
    for row in rows:
        if not row['issue']:
            continue
        ordinal = row['native']['ordinal']
        refs = by_reference[ordinal]
        baseline = prepared.get(ordinal)
        related = [r for r in rows[max(0, ordinal - 2):min(len(rows), ordinal + 1)]
                   if r['role'] == 'unattributed_content']
        blockers = [{'code': 'unattributed_adjacent_content', 'topic_id': r['id']} for r in related]
        if row['context_relation'].startswith('unresolved'):
            blockers.append({'code': 'native_context_outside_topic'})
        if any(ref['issue_conflict'] for ref in refs):
            blockers.append({'code': 'index_native_issue_conflict'})
        if any(link['target_topic_id'] is None for link in row['links']):
            blockers.append({'code': 'unresolved_topic_link'})
        page = opening_page(raw_topics[ordinal], row['rtf']['byte_offset'])
        if page['issue'] and page['issue'] != row['issue']:
            blockers.append({'code': 'opening_keyword_issue_conflict'})
        introduction = rows[ordinal - 2] if ordinal - 1 in intro_owners else None
        if introduction and introduction.get('context_relation', '').startswith('unresolved'):
            blockers.append({'code': 'introduction_context_outside_topic'})
        source_reference = baseline['reference'] if baseline else refs[0]['reference'] if refs else row['aliases'][0]
        identity = baseline['article_id'] if baseline else 'cd1:article:' + (refs[0]['reference'] if refs else 'native-' + row['context']['hash_hex'][2:])
        job = {'schema_version': 1, 'id': job_id(row), 'kind': 'article_candidate', 'candidate_article_id': identity,
               'identity_basis': 'reviewed_preparation' if baseline else 'indexed_native_context' if refs else 'native_context_alias',
               'source_reference': source_reference, 'native_context': row['context'], 'body_topic_id': row['id'],
               'introduction_topic_ids': [introduction['id']] if introduction else [],
               'related_links': row['links'], 'title': row['title'], 'issue_id': 'maso-' + row['issue'],
               'opening_page': page, 'index_references': [ref['reference'] for ref in refs],
               'index_titles': sorted({t for ref in refs for t in ref['title_variants']}),
               'occurrence_ids': [key for ref in refs for key in ref['occurrence_ids']],
               'state': 'already_prepared' if baseline else 'blocked' if blockers else 'ready',
               'blockers': blockers, 'features': row['features'],
               'source_topics': [{k: t[k] for k in ('id', 'native', 'rtf', 'aliases', 'context_relation')}
                                 for t in ([introduction] if introduction else []) + [row]],
               'preparation': baseline, 'toc': None,
               'limits': ['physical_verification_pending', 'known_review_exceptions_retained'] if baseline else
                         ['candidate_boundaries_require_runner_validation', 'semantic_structure_unreviewed', 'physical_verification_pending']}
        job['toc'] = toc_relation(job, toc, baseline)
        if baseline:
            require(not blockers and baseline['title'] == row['title'] and baseline['issue_id'] == job['issue_id'],
                    'Prepared article identity/status changed')
            require([t['id'] for t in job['source_topics']] == baseline['topic_ids'], 'Prepared topic ownership changed')
            require([t['rtf'] for t in job['source_topics']] == baseline['rtf_spans'], 'Prepared source spans changed')
        jobs.append(job)
    job_by_topic = {j['body_topic_id']: j for j in jobs}
    for ref in reference_rows:
        ref['job_id'] = job_by_topic.get(ref['topic_id'], {}).get('id')
    toc_rows = []
    matched, candidates = defaultdict(list), defaultdict(list)
    for job in jobs:
        for key in job['toc']['matched_ids']:
            matched[key].append(job['id'])
        for key in job['toc']['candidate_ids']:
            candidates[key].append(job['id'])
    cd_issues = sorted({j['issue_id'] for j in jobs})
    for entry in toc:
        status = ('section' if entry['kind_candidate'] == 'section' else 'outside_observed_CD1_issues' if
                  entry['issue_id'] not in cd_issues else 'matched' if matched[entry['id']] else
                  'needs_review' if candidates[entry['id']] else 'no_exact_title_match')
        toc_rows.append({'toc_entry_id': entry['id'], 'issue_id': entry['issue_id'], 'source': entry['source'],
                         'status': status, 'matched_job_ids': matched[entry['id']], 'candidate_job_ids': candidates[entry['id']]})
    issues = []
    for issue_id in cd_issues:
        selected = [j for j in jobs if j['issue_id'] == issue_id]
        toc_selected = [t for t in toc_rows if t['issue_id'] == issue_id]
        issues.append({'issue_id': issue_id, 'job_ids': [j['id'] for j in selected],
                       'counts': {'article_candidates': len(selected), 'states': histogram(j['state'] for j in selected),
                                  'unindexed_candidates': sum(not j['index_references'] for j in selected),
                                  'index_occurrences': sum(len(j['occurrence_ids']) for j in selected),
                                  'toc_entries': len(toc_selected), 'toc_status': histogram(t['status'] for t in toc_selected)}})
    return {'topics': rows, 'contexts': context_rows, 'references': reference_rows, 'entries': entries,
            'jobs': jobs, 'toc': toc_rows, 'issues': issues, 'review_items': review_items}


def validate_inventory(data):
    topics, jobs = data['topics'], data['jobs']
    topic_ids = {t['id'] for t in topics}
    by_topic = {t['id']: t for t in topics}
    require([t['native']['ordinal'] for t in topics] == list(range(1, len(topics) + 1)) and
            all(t['id'] == topic_id(t['native']['ordinal']) for t in topics), 'Topic order/identity differs')
    require(all(a['native']['next_topic_pos'] == b['native']['topic_pos'] and
                a['native']['topic_offset'] < b['native']['topic_offset'] for a, b in zip(topics, topics[1:])),
            'Native header intervals are not contiguous and ordered')
    roles = {'dated_article_candidate', 'navigation', 'linked_introduction_candidate', 'formatting_separator',
             'application_resource_topic', 'linked_auxiliary_topic', 'unattributed_content'}
    require(all(t['role'] in roles for t in topics), 'Unknown topic role')
    job_ids = {j['id'] for j in jobs}
    require(len(topic_ids) == len(topics) and len(job_ids) == len(jobs), 'Duplicate topic or job identity')
    require(len({j['candidate_article_id'] for j in jobs}) == len(jobs), 'Duplicate article candidate identity')
    dated = {t['id'] for t in topics if t['role'] == 'dated_article_candidate'}
    require({j['body_topic_id'] for j in jobs} == dated and len(jobs) == len(dated), 'Article candidate coverage differs')
    occurrences = [key for ref in data['references'] for key in ref['occurrence_ids']]
    require(len(occurrences) == len(set(occurrences)) and set(occurrences) ==
            {e['id'] for e in data['entries'] if e['kind'] == 'reference'}, 'Index occurrence coverage differs')
    require({c['topic_id'] for c in data['contexts']} == {t['id'] for t in topics if t['aliases']}, 'Context/topic coverage differs')
    context_hashes = {c['hash_hex'] for c in data['contexts']}
    require(len(context_hashes) == len(data['contexts']), 'Duplicate context hash')
    for context in data['contexts']:
        topic = by_topic[context['topic_id']]
        ordinal = topic['native']['ordinal']
        end = topics[ordinal]['native']['topic_offset'] if ordinal < len(topics) else None
        require(topic['aliases'] == [context['alias']] and
                context['hash_hex'] == f"0x{native.context_hash(context['alias']):08x}" and
                context['native_header_topic_offset'] == topic['native']['topic_offset'] and
                context['next_header_topic_offset'] == end and
                context['association'] == topic['context_relation'] ==
                context_relation(context['topic_offset'], topic['native']['topic_offset'], end),
                'Context association evidence differs')
    aliases = {c['hash_hex']: c['topic_id'] for c in data['contexts']}
    for topic in topics:
        for link in topic['links']:
            require(link['target_topic_id'] == aliases.get(f"0x{native.context_hash(link['alias']):08x}"),
                    'Topic link target differs')
    grouped = group_references(data['entries'])
    require([{k: ref[k] for k in expected} for ref, expected in zip(data['references'], grouped)] == grouped and
            len(data['references']) == len(grouped), 'Index grouping evidence differs')
    issue_jobs = [key for issue in data['issues'] for key in issue['job_ids']]
    require(len(issue_jobs) == len(jobs) and set(issue_jobs) == job_ids, 'Issue job coverage differs')
    for job in jobs:
        require(job['state'] in ('ready', 'blocked', 'already_prepared'), 'Unknown queue state')
        require(bool(job['blockers']) == (job['state'] == 'blocked'), 'Queue state ignores a blocker')
        require(bool(job['preparation']) == (job['state'] == 'already_prepared'), 'Preparation status lacks evidence')
        body = by_topic[job['body_topic_id']]
        require(job['schema_version'] == 1 and job['kind'] == 'article_candidate' and job['id'] == job_id(body) and
                job['issue_id'] == 'maso-' + body['issue'] and job['title'] == body['title'] and
                job['native_context'] == body['context'], 'Job identity or issue evidence differs')
        ordinal = body['native']['ordinal']
        related = [t['id'] for t in topics[max(0, ordinal - 2):min(len(topics), ordinal + 1)]
                   if t['role'] == 'unattributed_content']
        require(related == [b['topic_id'] for b in job['blockers'] if b['code'] == 'unattributed_adjacent_content'],
                'Adjacent content blocker lost')
        require(job['source_topics'] == [{k: by_topic[t['id']][k] for k in
                                         ('id', 'native', 'rtf', 'aliases', 'context_relation')}
                                        for t in job['source_topics']], 'Job source evidence differs')
        owned = [t['id'] for t in job['source_topics']]
        require(owned == job['introduction_topic_ids'] + [job['body_topic_id']] and set(owned) <= topic_ids,
                'Job topic ownership differs')
    claimed = [t['id'] for j in jobs for t in j['source_topics']]
    require(len(claimed) == len(set(claimed)), 'Duplicate source ownership')
    require({t['id'] for t in topics if t['role'] == 'unattributed_content'} ==
            {key for item in data['review_items'] for key in item['topic_ids']}, 'Unattributed content lost from review queue')
    for ref in data['references']:
        require(ref['topic_id'] is None or ref['topic_id'] in topic_ids, 'Dangling index target')
        require(ref['job_id'] is None or ref['job_id'] in job_ids, 'Dangling index job')
        if ref['job_id'] is not None:
            job = next(j for j in jobs if j['id'] == ref['job_id'])
            require(ref['topic_id'] == job['body_topic_id'] and ref['reference'] in job['index_references'] and
                    set(ref['occurrence_ids']) <= set(job['occurrence_ids']), 'Index/job association differs')
    for job in jobs:
        refs = [r for r in data['references'] if r['job_id'] == job['id']]
        require(job['index_references'] == [r['reference'] for r in refs] and
                job['occurrence_ids'] == [key for r in refs for key in r['occurrence_ids']],
                'Job index occurrence coverage differs')
    require(len({e['id'] for e in data['entries']}) == len(data['entries']) and
            len({r['toc_entry_id'] for r in data['toc']}) == len(data['toc']), 'Duplicate index/TOC entry')
    for row in data['toc']:
        require(set(row['matched_job_ids'] + row['candidate_job_ids']) <= job_ids, 'Dangling TOC job')
        require(row['matched_job_ids'] == [j['id'] for j in jobs if row['toc_entry_id'] in j['toc']['matched_ids']] and
                row['candidate_job_ids'] == [j['id'] for j in jobs if row['toc_entry_id'] in j['toc']['candidate_ids']],
                'TOC/job relationship differs')


def select_sample(jobs):
    by_ordinal = {j['source_topics'][-1]['native']['ordinal']: j for j in jobs}
    sample = []
    for ordinal in SAMPLE_ORDINALS:
        job = by_ordinal[ordinal]
        require(job['state'] == 'ready' and job['issue_id'] != 'maso-1988-02', 'Validation sample is not a new ready candidate')
        sample.append({'job_id': job['id'], 'body_topic_id': job['body_topic_id'], 'issue_id': job['issue_id'],
                       'title': job['title'], 'source_reference': job['source_reference'], 'features': job['features'],
                       'selection_reason': SAMPLE_REASONS[ordinal],
                       'review_concerns': ['validate_boundaries_and_inherited_RTF_state', 'inspect_semantic_structure',
                                           'validate_font_encoding_and_media'] +
                                          (['unindexed_native_identity'] if not job['index_references'] else []) +
                                          (['context_is_inside_topic_not_header'] if job['source_topics'][-1]['context_relation'] != 'at_native_header' else [])})
    require(6 <= len(sample) <= 10 and len({j['issue_id'] for j in sample}) >= 3, 'Invalid validation sample population')
    return sample


def inventory_counts(data):
    counts = {'native_topics': len(data['topics']), 'topic_roles': histogram(t['role'] for t in data['topics']),
              'native_contexts': len(data['contexts']), 'context_associations': histogram(c['association'] for c in data['contexts']),
              'index_entries': len(data['entries']), 'index_references': len(data['references']),
              'reference_kinds': histogram(r['reference_kind'] for r in data['references']),
              'index_occurrences': sum(len(r['occurrence_ids']) for r in data['references']),
              'index_targets': histogram(r['target_status'] for r in data['references']),
              'article_candidates': len(data['jobs']), 'job_states': histogram(j['state'] for j in data['jobs']),
              'unindexed_article_candidates': sum(not j['index_references'] for j in data['jobs']),
              'toc_entries': len(data['toc']), 'toc_status': histogram(t['status'] for t in data['toc']),
              'issues': len(data['issues']), 'unattributed_content_topics': len(data['review_items'])}
    return counts


def build_inventory():
    inputs = {}
    def read(path, expected=None):
        path = Path(path)
        relative = path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()
        raw = checked_file(ROOT, {**(expected or {}), 'path': relative})
        inputs[relative] = file_record(relative, raw)
        return raw

    implementation = [read(path) for path in ('tools/inventory_cd1_processing.py', 'tools/close_cd1_february.py',
                                                'tools/map_cd1_topic.py', 'src/maso_archive/cd1_index.py')]
    mvb, rtf = [read(path, {'sha256': sha}) for path, sha in native.SOURCES.items()]
    manifest = json.loads(read('build/cd1-index/manifest.json'))
    probe = json.loads(read('private/cd1-probe/manifest.json', {'sha256': manifest['extraction_manifest_sha256']}))
    entries = checked_artifact(ROOT / 'build/cd1-index', 'entries.jsonl')
    references = checked_artifact(ROOT / 'build/cd1-index', 'references.jsonl')
    rebuilt = []
    for name in INDEX_NAMES:
        source = next(s for s in manifest['sources'] if s['name'] == name)
        raw = read('private/cd1-probe/raw/' + name, source)
        preserved = next(f for f in probe['files'] if f['path'] == 'raw/' + name)
        require(digest(raw) == preserved['sha256'] and len(raw) == preserved['bytes'], 'Index probe evidence differs')
        rebuilt.extend(parse_index(name, raw)[0])
    require(rebuilt == entries and group_references(entries) == references, 'Index import does not reproduce')
    for name in ('entries.jsonl', 'references.jsonl'):
        read('build/cd1-index/' + name, manifest['outputs'][name])
    toc_manifest = json.loads(read('build/toc/manifest.json'))
    toc_raw = read('TOC.md', toc_manifest['source'])
    identities = json.loads(read('data/identities/toc.json', {'sha256': toc_manifest['identities_sha256']}))
    toc = checked_artifact(ROOT / 'build/toc', 'toc-entries.jsonl')
    read('build/toc/toc-entries.jsonl', toc_manifest['outputs']['toc-entries.jsonl'])
    _, reconstructed, errors = parse_toc(toc_raw.decode(), 'toc-sha256-' + digest(toc_raw))
    assign_identities(reconstructed, identities, {}, errors)
    finalize_entries(reconstructed)
    require(not errors and reconstructed == toc, 'Current TOC entry import does not reproduce')
    package_record = json.loads(read(february.RECORD))
    for record in package_record['outputs']:
        read(package_record['package_root'] + '/' + record['path'], record)
    bundle, _, counts = load_package(ROOT / package_record['package_root'])
    require(counts == package_record['counts'], 'February package counts changed')
    evidence = json.loads(read(package_record['provenance']['path'], package_record['provenance']))
    prepared = {}
    for article in bundle['articles']:
        source = evidence['article_evidence'][article['source']['reference']]
        maps = source.get('topic_map')
        if maps is None:  # The pilot's provenance embeds its older map layout.
            pilot_map = json.loads(read(native.RECORD))
            maps = [t for t in pilot_map['topics'] if t['native']['ordinal'] in pilot_map['recovery_scope_ordinals']]
        body = next(t for t in maps if t['role'] == 'reference_target_body')
        ordinal = body['native']['ordinal']
        require(ordinal not in prepared, 'Duplicate prepared body')
        prepared[ordinal] = {'article_id': article['id'], 'reference': article['source']['reference'],
                             'title': article['title'], 'issue_id': article['issue_id'], 'toc_entry_ids': article['toc_entry_ids'],
                             'extraction_status': article['extraction_status'], 'print_verification': article['print_verification'],
                             'topic_ids': [topic_id(t['native']['ordinal']) for t in maps],
                             'rtf_spans': [{k: t['rtf'][k] for k in ('byte_offset', 'byte_length', 'sha256')} for t in maps],
                             'package_record': str(february.RECORD.relative_to(ROOT))}
    require(len(prepared) == 6, 'February preparation population changed')
    data = reconcile(mvb, rtf, toc, entries, references, prepared)
    validate_inventory(data)
    sample = select_sample(data['jobs'])
    counts = inventory_counts(data)
    files = {name + '.jsonl': b''.join(json.dumps(row, ensure_ascii=False, separators=(',', ':')).encode() + b'\n' for row in data[key])
             for name, key in [('topics', 'topics'), ('contexts', 'contexts'), ('index-references', 'references'),
                               ('index-entries', 'entries'), ('jobs', 'jobs'), ('toc-coverage', 'toc')]}
    files.update({'issues.json': json_bytes(data['issues']), 'review-items.json': json_bytes(data['review_items']),
                  'validation-sample.json': json_bytes(sample)})
    manifest = {'schema_version': 1, 'inventory_version': VERSION, 'disc_id': 'cd1', 'checkpoint': '13a', 'scope': 'metadata_only',
                'inputs': inputs, 'implementation_sha256': digest(b''.join(implementation)), 'counts': counts, 'outputs': [file_record(p, raw) for p, raw in sorted(files.items())],
                'queue_semantics': 'ready means eligible for runner validation, not checked recovery or proven complete article boundaries',
                'limits': ['no_new_article_recovery', 'no_new_media_conversion', 'no_physical_verification',
                           'exact_title_metadata_matches_only', 'untitled_content_and_related_links_require_runner_review']}
    files['manifest.json'] = json_bytes(manifest)
    record = {**manifest, 'output_root': OUTPUT.relative_to(ROOT).as_posix(), 'issues': data['issues'],
              'unindexed_articles': [{k: j[k] for k in ('id', 'body_topic_id', 'title', 'issue_id', 'source_reference', 'state')}
                                     for j in data['jobs'] if not j['index_references']],
              'blocked_jobs': [{k: j[k] for k in ('id', 'body_topic_id', 'title', 'issue_id', 'blockers')}
                               for j in data['jobs'] if j['state'] == 'blocked'],
              'review_items': data['review_items'], 'validation_sample': sample,
              'context_offset_differences': [c for c in data['contexts'] if c['association'] != 'at_native_header'],
              'manifest': file_record('manifest.json', files['manifest.json'])}
    return record, files



def load_inventory(root):
    """Validate a relocated inventory before the future runner consumes its queue."""
    root = Path(root)
    manifest = json.loads(checked_file(root, {'path': 'manifest.json'}))
    require(manifest['schema_version'] == 1 and manifest['inventory_version'] == VERSION and
            manifest['disc_id'] == 'cd1' and manifest['scope'] == 'metadata_only', 'Unsupported inventory contract')
    records = {r['path']: r for r in manifest['outputs']}
    require(len(records) == len(manifest['outputs']) and set(records) == set(OUTPUT_NAMES) | {'validation-sample.json'},
            'Inventory output population differs')
    require({p.name for p in root.iterdir()} == set(records) | {'manifest.json'}, 'Unexpected inventory files')
    data = {}
    for name, key in OUTPUT_NAMES.items():
        raw = checked_file(root, records[name])
        data[key] = [json.loads(line) for line in raw.splitlines()] if name.endswith('.jsonl') else json.loads(raw)
    sample = json.loads(checked_file(root, records['validation-sample.json']))
    validate_inventory(data)
    require(inventory_counts(data) == manifest['counts'], 'Inventory counts differ')
    require(sample == select_sample(data['jobs']), 'Validation sample differs from frozen selection')
    return data, manifest


def write_inventory(output, files):
    """Check staged metadata before replacing a prior successful inventory."""
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    require(not output.is_symlink(), 'Refusing symlink output')
    with tempfile.TemporaryDirectory(prefix='.inventory-stage-', dir=output.parent) as temporary:
        stage = Path(temporary) / 'new'
        stage.mkdir()
        require(set(files) == set(OUTPUT_NAMES) | {'validation-sample.json', 'manifest.json'}, 'Invalid inventory file set')
        for name, raw in files.items():
            (stage / name).write_bytes(raw)
        load_inventory(stage)
        previous = Path(temporary) / 'previous'
        if output.exists():
            output.rename(previous)
        try:
            stage.rename(output)
        except OSError:
            if previous.exists():
                previous.rename(output)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-record', action='store_true')
    parser.add_argument('--verify', type=Path, help='Verify an existing inventory without reading original sources')
    parser.add_argument('--check', action='store_true', help='Rebuild in memory and verify the reviewed record without writing')
    args = parser.parse_args()
    try:
        if args.verify:
            require(not args.write_record and not args.check, '--verify cannot rebuild or write records')
            _, manifest = load_inventory(args.verify)
            print(f"Validated CD1 processing inventory: {manifest['counts']}")
            return 0
        require(not (args.write_record and args.check), 'Choose either --write-record or --check')
        record, files = build_inventory()
        if not args.write_record:
            require(record == json.loads(RECORD.read_bytes()), 'Processing inventory differs from reviewed record')
        if not args.check:
            write_inventory(OUTPUT, files)
            if args.write_record:
                atomic_write(RECORD, json_bytes(record))
        print(f"CD1 processing inventory: {record['counts']}")
    except (OSError, ValueError, KeyError, StopIteration) as exc:
        print(f'CD1 processing inventory failed: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
