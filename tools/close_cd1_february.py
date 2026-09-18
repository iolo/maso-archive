"""Step 12d: audit native February metadata and hand off six prepared articles.

The indexed five-article checkpoint remains reproducible at its original path.
This checkpoint adds the unindexed article without inventing index occurrences.
"""

import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
import struct
import sys

from jsonschema.exceptions import ValidationError

from maso_archive.reading_room_package import checked_file, file_record, load_package
from tools import map_cd1_topic as native
from tools import prepare_cd1_issue as indexed
from tools import prepare_cd1_keyboard as keyboard
from tools.build_reading_room_package import write_package
from tools.decode_cd1_paragraph import digest
from tools.recover_cd1_text import json_bytes

ROOT = native.ROOT
OUTPUT = ROOT / 'build/cd1-issues/1988-02-native'
RECORD = ROOT / 'data/catalog/issue-packages/cd1-1988-02-native.json'
COVERAGE = ROOT / 'data/catalog/issue-coverage/cd1-1988-02-native.json'
KEYWORD = re.compile(rb'\{\\up K\}\{\\footnote\\pard\\plain\{\\up K\} 4:([^}]+)\}')
PAGE_LABEL = re.compile(rb'(?<![0-9])(?:19)?88\.\s*0?2\.\s*([0-9]+)p')
FEBRUARY = {146: ('8802030', 30), 149: ('8802065', 65), 152: ('8802114', 114),
            155: ('8802162', 162), 158: ('8802180', 180), 161: ('8802184', 184)}
NAVIGATION = {1, 7, 8, 9, 10, 11, 12, 13, 14, 15}
require = native.require


def scan_native(mvb, rtf):
    """Read all topic headers and issue keywords, without decoding article bodies."""
    pages = list(re.finditer(rb'(?<!\\)\\page\n', rtf))
    require(len(pages) == 3098, 'RTF topic population changed')
    topics = native.native_topics(mvb, len(pages) + 1)
    contexts = native.context_entries(mvb)
    rows, february, page_topics, navigation = [], [], [], []
    for topic in topics:
        ordinal = topic['ordinal']
        size, length, _, _, data, kind = struct.unpack('<5iB', native.topic_read(mvb, topic['topic_pos'], 21))
        require(kind == 2 and 0 <= length <= size - data, 'Unsupported native header title')
        title = native.topic_read(mvb, topic['topic_pos'], size)[data:data + length].split(b'\0')[0].decode('cp949')
        start = pages[ordinal - 2].end() if ordinal > 1 else 0
        end = pages[ordinal - 1].start() if ordinal <= len(pages) else len(rtf)
        raw = rtf[start:end]
        matches = list(KEYWORD.finditer(raw))
        require(len(matches) <= 1, 'Ambiguous issue keyword')
        row = {'native': topic, 'title': title, 'issue': None,
               'rtf': {'byte_offset': start, 'byte_length': end - start, 'sha256': digest(raw)}}
        if matches:
            match = matches[0]
            decoded = re.sub(rb"\\'([0-9a-fA-F]{2})", lambda m: bytes.fromhex(m[1].decode()), match[1]).decode('cp949')
            date = re.fullmatch(r'(\d{2})년\s*(\d{1,2})월', decoded)
            require(date is not None and 1 <= int(date[2]) <= 12, 'Unsupported issue keyword')
            require(title and ordinal not in NAVIGATION, 'Issue keyword outside titled article')
            aliases = [m[1].decode('ascii') for m in native.CONTEXT_FOOTNOTE.finditer(raw)]
            require(len(aliases) == 1, 'Dated topic alias population changed')
            context = contexts[native.context_hash(aliases[0])]
            # Some other issues point inside a topic rather than at its header.
            # Keep those offsets visible; only February requires exact agreement.
            row['context_at_header'] = context['topic_offset'] == topic['topic_offset']
            title_note = re.search(rb'\{\\up \$\}\{\\footnote\\pard\\plain\{\\up \$\} ([^}]+)\}', raw)
            require(title_note is not None, 'Dated topic title footnote missing')
            rtf_title = re.sub(rb"\\'([0-9a-fA-F]{2})", lambda m: bytes.fromhex(m[1].decode()), title_note[1]).decode('cp949')
            require(rtf_title == title, 'Native/RTF title association changed')
            row.update(issue=f'19{date[1]}-{int(date[2]):02d}', alias=aliases[0], context=context,
                       issue_keyword={'label': decoded, 'byte_offset': start + match.start(),
                                      'byte_length': match.end() - match.start(), 'sha256': digest(match[0])})
            if row['issue'] == '1988-02':
                february.append(row)
        elif title:
            require(ordinal in NAVIGATION, 'Unattributed titled native topic needs review')
            navigation.append(row)
        for match in PAGE_LABEL.finditer(raw):
            # The explicit date/page must be in the opening paragraph, not a later citation.
            first_par = re.search(rb'(?<!\\)\\par\b', raw)
            require(first_par is not None and match.end() <= first_par.start(), 'February label outside opening paragraph')
            page_topics.append(ordinal)
            row['opening_page_label'] = {'page': int(match[1]), 'label': match[0].decode(),
                                         'byte_offset': start + match.start(), 'byte_length': len(match[0])}
        rows.append(row)
    require([r['native']['ordinal'] for r in february] == page_topics == list(FEBRUARY),
            'February native keyword/page populations disagree with reviewed six articles')
    require({r['native']['ordinal'] for r in navigation} == NAVIGATION, 'Navigation metadata population changed')
    require(Counter('article' if r['issue'] else 'navigation' if r['title'] else 'untitled' for r in rows) ==
            {'article': 1088, 'navigation': 10, 'untitled': 2001}, 'Native metadata population changed')
    for row in february:
        ordinal = row['native']['ordinal']
        reference, page = FEBRUARY[ordinal]
        context = contexts[native.context_hash(reference)]
        require(row['context_at_header'] and context == row['context'] and row['opening_page_label']['page'] == page,
                'Numeric context, native alias, or explicit page changed')
        row.update(reference=reference, numeric_context=context)
        previous, following = topics[ordinal - 4], topics[ordinal + 2]
        require(row['native']['browse_back_topic_offset'] == previous['topic_offset'] and
                row['native']['browse_forward_topic_offset'] == following['topic_offset'], 'February browse chain changed')
    neighbors = [rows[142], rows[163]]
    require([r['issue'] for r in neighbors] == ['1988-01', '1988-03'], 'February issue boundaries changed')
    summary = {'native_topics': len(rows), 'dated_article_topics': 1088, 'navigation_topics': 10,
               'untitled_topics': 2001, 'unattributed_titled_topics': 0,
               'other_issue_context_offset_differences': [
                   {'ordinal': r['native']['ordinal'], 'issue': r['issue'],
                    'header_topic_offset': r['native']['topic_offset'], 'context': r['context'],
                    'status': 'outside_February_scope_not_resolved'}
                   for r in rows if r.get('context_at_header') is False],
               'february_body_topics': len(february), 'february_page_labels': len(page_topics),
               'february_articles': february, 'boundary_articles': neighbors,
               'undated_navigation': navigation,
               'method': 'All native titles and all RTF issue-keyword footnotes; independent opening February page-label scan; alias/context and browse-chain checks.'}
    return summary, rows


def build_handoff():
    old_record, old_coverage, old_files = indexed.build_handoff()
    require(old_record == json.loads(indexed.RECORD.read_bytes()) and
            old_coverage == json.loads(indexed.COVERAGE.read_bytes()), 'Indexed checkpoint changed')
    inputs = {}

    def read(path, expected=None):
        path = Path(path)
        relative = path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()
        raw = checked_file(ROOT, {**(expected or {}), 'path': relative})
        inputs[relative] = file_record(relative, raw)
        return raw

    for path in (indexed.RECORD, indexed.COVERAGE):
        read(path)
    mvb, rtf = [read(p, {'sha256': sha}) for p, sha in native.SOURCES.items()]
    scan, rows = scan_native(mvb, rtf)
    summary = json.loads(read(keyboard.RECORD))
    records = {r['path']: r for r in summary['outputs']}
    base = keyboard.OUTPUT.relative_to(ROOT).as_posix()
    evidence_path = base + '/provenance.json'
    evidence = json.loads(read(evidence_path, records[evidence_path]))
    require(evidence['index_occurrences'] == [] and summary['index_status'] == 'absent_from_all_three_indexes',
            'Unexpected keyboard index evidence')
    prefix = base + '/combined/content/'
    runtime = {path[len(prefix):]: read(path, record) for path, record in records.items() if path.startswith(prefix)}
    bundle, _, counts = load_package(keyboard.OUTPUT / 'combined/content')
    require(len(runtime) == counts['files'] == summary['combined_runtime_files'], 'Incomplete six-article package')
    single_prefix = base + '/single/content/'
    single, _, single_counts = load_package(keyboard.OUTPUT / 'single/content')
    single_files = {path[len(single_prefix):]: read(path, record) for path, record in records.items()
                    if path.startswith(single_prefix)}
    require(single_counts['articles'] == 1 and len(single_files) == single_counts['files'] == summary['single_runtime_files'],
            'Incomplete keyboard standalone')
    for files, prefix in ((old_files, 'content/'), (single_files, '')):
        for path, raw in files.items():
            if path.startswith(tuple(prefix + p for p in ('articles/', 'previews/', 'media/'))):
                require(runtime.get(path[len(prefix):]) == raw, 'Prior or standalone content changed')
    old_media = json.loads(old_files['content/media.json'])['items']
    require(bundle['media']['items'] == old_media + single['media']['items'], 'Six-article media changed')
    by_reference = {a['source']['reference']: a for a in bundle['articles']}
    require(set(by_reference) == {r for r, _ in FEBRUARY.values()}, 'Unaccounted prepared article')
    native_articles = []
    for row in scan['february_articles']:
        reference = row['reference']
        article = by_reference[reference]
        require(article['title'] == row['title'] and article['pages']['start'] == row['opening_page_label']['page'] and
                article['print_verification']['status'] == 'pending' and article['pages']['end'] is None,
                'Prepared article and native evidence disagree')
        body = next(s for s in article['sections'] if s['role'] == 'body')
        require(body['blocks'][0]['paragraphs'][0]['id'] == f"cd1-{reference}:T{row['native']['ordinal']}:P001",
                'Prepared body identity differs from native topic')
        native_articles.append({**row, 'article_id': article['id'], 'toc_entry_ids': article['toc_entry_ids'],
                                'preparation_status': 'prepared',
                                'index_status': 'unindexed' if reference == keyboard.REFERENCE else 'indexed'})
    reviews = old_coverage['review_records']
    indexed.check_reviews(bundle, reviews['deferred_media'], reviews['text_reviews'])
    coverage = deepcopy(old_coverage)
    coverage.update(checkpoint='12d', scope='all_observed_native_February_articles_and_complete_TOC_accounting',
                    indexed_checkpoint=inputs[indexed.COVERAGE.relative_to(ROOT).as_posix()],
                    native_scan=scan, native_articles=native_articles, runtime_counts=counts)
    matched = {toc: a for a in bundle['articles'] for toc in a['toc_entry_ids']}
    expected_issue = json.loads(old_files['content/issues/maso-1988-02.json'])
    new_entry = next(e for e in expected_issue['toc'] if e['id'] == keyboard.TOC_ID)
    new_entry.update(article_ids=[keyboard.ARTICLE_ID], link_status='matched')
    require(bundle['issues'] == [expected_issue], 'Existing issue metadata changed')
    runtime_toc = bundle['issues'][0]['toc']
    require(len(runtime_toc) == len(coverage['toc_entries']) == 39, 'Issue TOC population changed')
    for row, entry in zip(coverage['toc_entries'], runtime_toc):
        require(row['entry']['id'] == entry['id'], 'Issue TOC identity/order changed')
        article = matched.get(entry['id'])
        refs = [article['source']['reference']] if article else []
        require(entry['article_ids'] == ([article['id']] if article else []) and
                entry['link_status'] == ('matched' if article else 'unmatched'), 'Runtime TOC link changed')
        row['matched_references'] = refs
        if article:
            row.update(preparation_status='prepared', content_availability='prepared', relationship_status='matched')
            row['match_basis'] = ('exact_TOC_native_intro_title_and_explicit_body_page_with_native_context' if
                                  article['id'] == keyboard.ARTICLE_ID else 'reviewed_indexed_article_evidence')
        elif row['entry']['kind_candidate'] == 'section':
            row['relationship_status'] = 'not_applicable_section'
        else:
            row.update(content_availability='no_match_in_reviewed_native_February_metadata',
                       relationship_status='no_observed_native_match')
    coverage['counts'].update(native_articles=6, unindexed_native_articles=1,
                              toc_relationships=dict(sorted(Counter(r['relationship_status'] for r in coverage['toc_entries']).items())),
                              toc_preparation={'not_applicable_section': 4, 'prepared': 6, 'unprepared': 29})
    require(Counter(r['preparation_status'] for r in coverage['toc_entries']) == coverage['counts']['toc_preparation'],
            'Coverage preparation accounting differs')
    coverage['limits'].update(unindexed_native_targets='one_February_body_attributed_and_prepared',
                             new_topics_recovered=2, new_media_conversions=5,
                             native_metadata_completeness='all_observed_February_issue_keywords_and_opening_labels_accounted_for',
                             remaining_29='No matching February native body observed; obtain scans or another source. Absence of mislabeled content is not proven.')
    old_evidence = json.loads(old_files['provenance.json'])
    article_evidence = {**old_evidence['article_evidence'], keyboard.REFERENCE: evidence}
    outputs = [file_record(p, raw) for p, raw in sorted(runtime.items())]
    validation = {'schema_changed': False, 'all_six_standalones_checked': True,
                  'previous_article_preview_and_asset_bytes_preserved': True,
                  'all_observed_native_February_bodies_prepared': True, 'physical_magazine_compared': False}
    provenance = {'schema_version': 1, 'issue_id': indexed.ISSUE, 'inputs': inputs,
                  'indexed_checkpoint_evidence': old_evidence, 'article_evidence': article_evidence,
                  'coverage': coverage, 'native_metadata_inventory': rows,
                  'runtime_root': 'content', 'outputs': outputs, 'handoff': old_evidence['handoff'], 'validation': validation}
    files = {**{'content/' + p: raw for p, raw in runtime.items()}, 'provenance.json': json_bytes(provenance)}
    record = {'schema_version': 1, 'issue_id': indexed.ISSUE, 'package_root': (OUTPUT / 'content').relative_to(ROOT).as_posix(),
              'schema': old_record['schema'], 'coverage': file_record(COVERAGE.relative_to(ROOT).as_posix(), json_bytes(coverage)),
              'counts': counts, 'coverage_counts': coverage['counts'], 'outputs': outputs,
              'deferred_media': 4, 'text_reviews': 1, 'validation': validation,
              'provenance': file_record((OUTPUT / 'provenance.json').relative_to(ROOT).as_posix(), files['provenance.json'])}
    return record, coverage, files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-record', action='store_true')
    args = parser.parse_args()
    try:
        record, coverage, files = build_handoff()
        if not args.write_record:
            require(record == json.loads(RECORD.read_bytes()), 'Native issue handoff differs from reviewed record')
            require(coverage == json.loads(COVERAGE.read_bytes()), 'Native issue coverage differs from reviewed record')
        write_package(OUTPUT, files)
        if args.write_record:
            for path, value in ((RECORD, record), (COVERAGE, coverage)):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(json_bytes(value))
        print(f"February native handoff prepared: {record['counts']}; six prepared, 29 unmatched article candidates")
    except (OSError, ValueError, KeyError, StopIteration, ValidationError) as exc:
        print(f'February native handoff failed: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
