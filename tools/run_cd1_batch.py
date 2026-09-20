"""Prepare independent private CD1 articles and compose issues from checked stages.

Examples: --issue 1988-02; --article 8802030; --all. Full-disc execution follows
PLAN-CD1 13c validation. Output never changes the original reviewed packages.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import platform
from importlib.metadata import version as distribution_version
import re
import sys

from PIL import __version__ as pillow_version
from maso_archive.reading_room import SCHEMA_PATH, catalog_for, project_section, validate_bundle
from maso_archive.reading_room_package import checked_file, check_svg, file_record, load_package
from tools import inventory_cd1_processing as queue
from tools import inventory_cd1_rtf as inventory
from tools import map_cd1_images as images
from tools import recover_cd1_text as recovery
from tools import render_cd1_markdown as markdown
from tools import build_reading_room_package as package
from tools.check_cd1_second_article import assemble, reading_sections
from tools.cd1_batch_core import inherited_states, map_blocks
from tools.cd1_batch_cache import Cache, key, write, verify
from tools.build_cd1_batch_profiles import OUTPUT as PROFILES, BASELINE
from tools.decode_cd1_paragraph import digest
from tools.map_cd1_topic import ROOT, require

OUTPUT = ROOT / 'build/cd1-batch'
VERSION = '1.0.0'


def read_json(path):
    return json.loads(Path(path).read_bytes())


def put(root, name, value):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(recovery.json_bytes(value))


def select(jobs, article=None, issue=None, all_jobs=False):
    require(sum((article is not None, issue is not None, all_jobs)) == 1, 'Select one scope')
    selected = [j for j in jobs if all_jobs or issue and j['issue_id'] == 'maso-' + issue or
                article and article in (j['id'], j['candidate_article_id'], j['source_reference'])]
    require(bool(selected), 'No jobs match selection')
    require(not article or len(selected) == 1, 'Ambiguous article selector; use job ID')
    return selected


def isolate(jobs, process):
    """A content failure cannot abort unrelated jobs; user interruption still stops."""
    results = []
    for job in jobs:
        try:
            if job['state'] == 'blocked':
                result = {'status': 'blocked', 'blockers': job['blockers']}
            else:
                result = process(job)
        except Exception as error:
            result = {'status': 'failed', 'error_type': type(error).__name__, 'error': str(error)}
        results.append({'job_id': job['id'], 'article_id': job['candidate_article_id'], 'issue_id': job['issue_id'], **result})
    return results


class Runner:
    def __init__(self, output=OUTPUT):
        self.output = Path(output).resolve()
        require(self.output.is_relative_to(ROOT / 'build') or self.output.is_relative_to(Path('/tmp')), 'Output must be private build/ or /tmp')
        self.data, manifest = queue.load_inventory(queue.OUTPUT)
        # Do not trust a checksum-valid queue if its source files changed afterwards.
        for record in manifest['inputs'].values():
            checked_file(ROOT, record)
        self.profiles = read_json(PROFILES)
        baseline_record = checked_file(ROOT, {'path': self.profiles['baseline_record'],
                                             'bytes': (ROOT / self.profiles['baseline_record']).stat().st_size,
                                             'sha256': self.profiles['baseline_record_sha256']})
        record = json.loads(baseline_record)
        for item in record['outputs']:
            checked_file(BASELINE, item)
        self.baseline, self.baseline_manifest, _ = load_package(BASELINE)
        self.baseline_evidence = json.loads(checked_file(ROOT, record['provenance']))
        self.baseline_articles = {a['source']['reference']: a for a in self.baseline['articles']}
        self.baseline_media = {m['source']['resource']: m for m in self.baseline['media']['items']}
        self.rtf = (images.RAW / 'MASOCD.rtf').read_bytes()
        self.media_manifest = read_json(images.MANIFEST)
        self.toc = [json.loads(line) for line in (ROOT / 'build/toc/toc-entries.jsonl').read_bytes().splitlines()]
        self.tools = {}
        for name, command in [('convert', ['convert', '-version']), ('inkscape', ['inkscape', '--version']), ('fontconfig', ['fc-match', '--version'])]:
            try:
                result = images.command(command)
                self.tools[name] = {k: result[k] for k in ('exit_code', 'stdout', 'stderr')}
            except OSError as error:
                self.tools[name] = {'unavailable': str(error)}
        try:
            font_listing = images.command(['fc-list', '--format=%{file}\n'])
            self.tools['font_files'] = {path: digest(Path(path).read_bytes()) for path in sorted(set(font_listing['stdout'].splitlines()))}
        except OSError as error:
            self.tools['font_files'] = {'unavailable': str(error)}
        # Include all Python dependencies, schema and policies; conservative
        # invalidation is preferable to reusing an obsolete preservation decision.
        code = {p.relative_to(ROOT).as_posix(): digest(p.read_bytes()) for parent in ('tools', 'src/maso_archive')
                for p in sorted((ROOT / parent).glob('*.py'))}
        self.identity = {'version': VERSION, 'code': code, 'python': platform.python_version(), 'pillow': pillow_version,
                         'jsonschema': distribution_version('jsonschema'),
                         'schema': digest((ROOT / SCHEMA_PATH).read_bytes()), 'profiles': digest(PROFILES.read_bytes()),
                         'queue': digest((queue.OUTPUT / 'manifest.json').read_bytes()), 'tools': self.tools}
        self.cache = Cache(self.output / 'stages', self.identity)
        self.states = {}
        self.topic_lookup = {t['id']: t for t in self.data['topics']}

    def issue(self, issue_id, articles):
        if issue_id == 'maso-1988-02':
            issue = deepcopy(self.baseline['issues'][0])
        else:
            year, month = map(int, issue_id.removeprefix('maso-').split('-'))
            issue = {'schema_version': 1, 'kind': 'issue', 'id': issue_id, 'year': year, 'month': month,
                     'label': f'{year % 100:02d}.{month:02d}', 'toc_status': 'available', 'cover_media_id': None,
                     'toc': [{'id': e['id'], 'parent_id': e['parent_id'], 'kind': e['kind_candidate'],
                              'title': e['title_candidate'], 'byline': e['byline_candidate'],
                              'pages': {'start': e['start_page_candidate'], 'end': e['end_page_candidate']},
                              'article_ids': [], 'link_status': 'unmatched'} for e in self.toc if e['issue_id'] == issue_id]}
        for entry in issue['toc']:
            ids = [a['id'] for a in articles if entry['id'] in a['toc_entry_ids']]
            entry.update(article_ids=ids, link_status='matched' if ids else 'unmatched')
        return issue

    def bundle(self, issue_id, articles, media):
        issue = self.issue(issue_id, articles)
        return {'schema_version': 1, 'kind': 'contract_example', 'issues': [issue], 'articles': articles,
                'catalog': catalog_for([issue], articles), 'media': {'schema_version': 1, 'kind': 'media_index', 'items': media}}

    def media(self, name):
        source = images.checked_source(name, self.media_manifest)
        def produce(stage):
            if name in self.baseline_media:
                media = deepcopy(self.baseline_media[name])
                if media['asset']:
                    asset = media['asset']
                    target = stage / asset['path']
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(checked_file(BASELINE, asset))
                put(stage, 'conversion.json', {'policy': 'reuse_reviewed_derivative_or_deferred_disposition',
                                             'source_sha256': digest(source), 'baseline_record': self.profiles['baseline_record']})
            else:
                media = {'id': 'cd1:media:' + name, 'source': {'disc_id': 'cd1', 'resource': name},
                         'status': 'deferred', 'asset': None, 'reason': 'conversion_deferred',
                         'problem_ids': ['cd1-batch-' + name], 'rendering_notes': []}
                (stage / 'assets').mkdir()
                (stage / 'previews').mkdir()
                try:
                    converted = images.convert_resource(name, source, stage)
                    if converted['status'] == 'converted_pending_viewer':
                        derivative = converted['derivatives'][0]['path']
                        raw = (stage / derivative).read_bytes()
                        vector = name.endswith('.wmf')
                        if vector:
                            check_svg(raw)
                        dimensions = ({'width': converted['source_format']['width_inches'], 'height': converted['source_format']['height_inches'], 'unit': 'in'} if vector else
                                      {'width': converted['png_pixels']['width'], 'height': converted['png_pixels']['height'], 'unit': 'px'})
                        path = 'media/cd1/' + Path(derivative).name
                        (stage / path).parent.mkdir(parents=True, exist_ok=True)
                        (stage / path).write_bytes(raw)
                        media.update(status='available', reason=None, problem_ids=[], rendering_notes=converted['concerns'],
                                     asset={**file_record(path, raw), 'mime_type': 'image/svg+xml' if vector else 'image/png', 'dimensions': dimensions})
                except Exception as error:
                    converted = {'status': 'conversion_failed', 'error_type': type(error).__name__, 'error': str(error)}
                # Temporary output paths are not stable provenance.
                converted = json.loads(json.dumps(converted).replace(str(stage), '<conversion-stage>'))
                put(stage, 'conversion.json', converted)
            put(stage, 'media.json', media)
        path, manifest = self.cache.stage('media-' + name, {'source_sha256': digest(source)}, produce)
        return read_json(path / 'media.json'), path, manifest

    def process(self, job):
        ref = job['source_reference']
        require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', ref) is not None, 'Unsafe article identity')
        profile = self.profiles['articles'].get(ref)
        if profile:
            require(profile['source_topics'] == job['source_topics'], 'Reviewed source association changed')
        token = job['id'].rsplit(':', 1)[1]
        chain = {'job': job, 'profile': profile}
        stages = {}
        def stage(name, producer, validator=None):
            nonlocal chain
            path, manifest = self.cache.stage(token + '-' + name, chain, producer, validator)
            stages[name] = {'path': path.relative_to(self.output).as_posix(), 'fingerprint': manifest['fingerprint']}
            chain = {'previous': manifest['fingerprint'], 'outputs': manifest['outputs']}
            return path
        def associate(target):
            require(len(job['introduction_topic_ids']) <= 1, 'Multiple introductions need ownership review')
            require(not job['blockers'], 'Unresolved topic ownership')
            selected = {t['id'] for t in job['source_topics']}
            links = [link for t in job['source_topics'] for link in self.topic_lookup[t['id']]['links']]
            put(target, 'related-links.json', links)
            put(target, 'association.json', job)
            for link in links:
                destination = link['target_topic_id']
                require(destination in selected or destination in self.topic_lookup and
                        self.topic_lookup[destination]['role'] in ('navigation', 'application_resource_topic', 'formatting_separator'),
                        'Related content outside selected topics needs ownership review: ' + str(destination))
            for topic in job['source_topics']:
                span = topic['rtf']
                raw = self.rtf[span['byte_offset']:span['byte_offset'] + span['byte_length']]
                require(digest(raw) == span['sha256'], 'Topic bytes changed')
                (target / f"topic-{topic['native']['ordinal']}.rtf").write_bytes(raw)
            put(target, 'association.json', job)
        stage('association', associate)
        def inspect(target):
            reports = []
            for topic in job['source_topics']:
                start, length = topic['rtf']['byte_offset'], topic['rtf']['byte_length']
                state = self.states[start]
                put(target, 'inherited-states.json', {str(t['rtf']['byte_offset']): self.states[t['rtf']['byte_offset']] for t in job['source_topics']})
                require(not state['unknown'], 'Unsupported inherited formatting: ' + ','.join(state['unknown']))
                report = inventory.inspect_topic(self.rtf[start:start + length], start, state['character']['font_id'])
                report.update(ordinal=topic['native']['ordinal'], role='reference_target_body' if topic['id'] == job['body_topic_id'] else 'linked_introduction')
                reports.append(report)
                put(target, 'inventory.json', reports)
                require(not report['issues'], 'Unsupported RTF constructs; see inventory evidence')
        inspected = stage('inventory', inspect)
        def recover(target):
            topics = []
            codecs = {int(k): v for k, v in profile['font_codecs'].items()} if profile else {4: 'cp949', 5: 'cp949', 6: 'cp949'}
            put(target, 'encoding-policy.json', {'font_codecs': codecs, 'unknown_fonts': 'retain_undecoded_and_fail', 'basis': 'source_bound_reviewed_CD1_fonts'})
            for report in read_json(inspected / 'inventory.json'):
                initial = {k: v for k, v in self.states[report['byte_offset']].items() if k != 'unknown'}
                topic = recovery.recover_topic(self.rtf, report, initial, codecs)
                topics.append(topic)
                put(target, 'recovery.json', {'schema_version': 1, 'cd_reference': ref, 'topics': topics})
                require(not topic['issues'], 'Undecoded text retained in recovery evidence')
                require(all(p['terminated_by_par'] for p in topic['paragraphs']), 'Unterminated paragraph needs representation review')
        recovered = stage('recovery', recover)
        article = read_json(recovered / 'recovery.json')
        mapped = stage('semantics', lambda target: put(target, 'blocks.json', map_blocks(article, profile)))
        mapping = read_json(mapped / 'blocks.json')
        names = sorted({r['object']['resource'] for t in article['topics'] for p in t['paragraphs'] for r in p['runs'] if r['kind'] == 'object'})
        media, assets, media_stages = [], {}, []
        for name in names:
            item, path, manifest = self.media(name)
            media.append(item)
            media_stages.append({'resource': name, 'fingerprint': manifest['fingerprint'], 'outputs': manifest['outputs']})
            if item['asset']:
                assets[item['asset']['path']] = checked_file(path, item['asset'])
        chain['media'] = media_stages
        stage('media', lambda target: put(target, 'media.json', {'items': media, 'stages': media_stages}))
        runtime = deepcopy(profile['runtime_metadata']) if profile else {
            'schema_version': 1, 'kind': 'article', 'id': job['candidate_article_id'], 'issue_id': job['issue_id'],
            'title': job['title'], 'byline': None, 'pages': {'start': job['opening_page']['page'], 'end': None},
            'source': {'disc_id': 'cd1', 'reference': ref}, 'toc_entry_ids': job['toc']['matched_ids'],
            'content_status': 'available', 'extraction_status': 'checked',
            'print_verification': {'status': 'pending', 'report_id': None, 'pages_compared': []}}
        intro = next((t['ordinal'] for t in article['topics'] if t['role'] == 'linked_introduction'), None)
        runtime['sections'] = reading_sections(article, mapping, ref, intro)
        for section in runtime['sections']:
            for block in section['blocks']:
                if block['type'] == 'unresolved':
                    block['interpretation'] = 'unresolved'
        runtime['relationships'] = [{'type': 'caption_for', 'from_block': r['from_block'], 'to_block': r['to_block']} for r in mapping['relationships']]
        for section, topic in zip(runtime['sections'], article['topics']):
            require(project_section(section, {m['id']: m for m in media}) == recovery.topic_text(topic), 'Source text projection changed')
        if profile:
            require(runtime == self.baseline_articles[ref] and digest(recovery.json_bytes(runtime)) == profile['article_sha256'],
                    'February runtime regression: ' + ref)
        def preview(target):
            files, locations = markdown.render(article, mapping)
            records = []
            for section in runtime['sections']:
                name = section['role'] + '.md'
                raw, ranges = package.package_preview(files[name], [r for r in locations if r['path'] == name])
                path = f'previews/cd1/{ref}/{name}'
                if profile:
                    require(raw == (BASELINE / path).read_bytes(), 'February preview regression: ' + path)
                (target / path).parent.mkdir(parents=True, exist_ok=True)
                (target / path).write_bytes(raw)
                records.append({'article_id': runtime['id'], 'section_id': section['id'], **file_record(path, raw), 'content_ranges': ranges})
            put(target, 'previews.json', records)
        previewed = stage('markdown', preview)
        bundle = self.bundle(job['issue_id'], [runtime], media)
        def assemble_article(target):
            previews = [(r['article_id'], r['section_id'], r['path'], checked_file(previewed, r)) for r in read_json(previewed / 'previews.json')]
            for name, raw in assemble(bundle, assets, previews).items():
                destination = target / 'content' / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(raw)
            put(target, 'provenance.json', {'job': job, 'stages': deepcopy(stages), 'semantic_review': 'reviewed_source_decisions' if profile else 'pending',
                                          'historical_evidence': self.baseline_evidence['article_evidence'][ref] if profile else None,
                                          'validation': validate_bundle(bundle)})
        packaged = stage('package', assemble_article, lambda root: load_package(root / 'content'))
        result = {'status': 'prepared', 'package': packaged.relative_to(self.output).as_posix(), 'stages': stages,
                  'counts': validate_bundle(bundle), 'deferred_media': [m['id'] for m in media if m['status'] != 'available'],
                  'semantic_review': 'reviewed_source_decisions' if profile else 'pending'}
        write(self.output / 'articles' / (token + '.json'), recovery.json_bytes({'identity_sha256': key(self.identity), **result}))
        return result

    def compose(self, issue_id):
        packages = []
        for job in self.data['jobs']:
            if job['issue_id'] != issue_id:
                continue
            pointer = self.output / 'articles' / (job['id'].rsplit(':', 1)[1] + '.json')
            if not pointer.exists():
                continue
            record = read_json(pointer)
            if record['identity_sha256'] != key(self.identity):
                continue
            path = self.output / record['package']
            verify(path, record['stages']['package']['fingerprint'])
            packages.append((path, record))
        if not packages:
            return {'status': 'no_prepared_articles'}
        inputs = [record['stages']['package']['fingerprint'] for _, record in packages]
        def compose(target):
            articles, media, assets, previews = [], {}, {}, []
            for path, _ in packages:
                bundle, manifest, _ = load_package(path / 'content')
                articles.extend(bundle['articles'])
                for item in bundle['media']['items']:
                    require(item['id'] not in media or media[item['id']] == item, 'Conflicting shared media')
                    media[item['id']] = item
                    if item['asset']:
                        assets[item['asset']['path']] = checked_file(path / 'content', item['asset'])
                previews.extend((r['article_id'], r['section_id'], r['path'], checked_file(path / 'content', r)) for r in manifest['previews'])
            articles.sort(key=lambda a: a['id'])
            bundle = self.bundle(issue_id, articles, sorted(media.values(), key=lambda m: m['id']))
            for name, raw in assemble(bundle, assets, previews).items():
                destination = target / 'content' / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(raw)
            put(target, 'provenance.json', {'article_packages': inputs, 'counts': validate_bundle(bundle),
                                          'coverage': self.baseline_evidence['coverage'] if issue_id == 'maso-1988-02' and len(articles) == 6 else
                                          {'prepared_article_ids': [a['id'] for a in articles], 'completeness': 'not_verified'}})
        path, manifest = self.cache.stage('issue-' + issue_id, inputs, compose, lambda root: load_package(root / 'content'))
        result = {'status': 'prepared', 'package': path.relative_to(self.output).as_posix(), 'fingerprint': manifest['fingerprint'],
                  'counts': load_package(path / 'content')[2]}
        write(self.output / 'issues' / (issue_id + '.json'), recovery.json_bytes(result))
        return result

    def run(self, jobs):
        self.states = inherited_states(self.rtf, [t['rtf']['byte_offset'] for j in jobs if j['state'] != 'blocked' for t in j['source_topics']])
        results = isolate(jobs, self.process)
        issues = {}
        for issue_id in sorted({j['issue_id'] for j in jobs}):
            try:
                issues[issue_id] = self.compose(issue_id)
            except Exception as error:
                issues[issue_id] = {'status': 'failed', 'error_type': type(error).__name__, 'error': str(error)}
        report = {'version': VERSION, 'identity_sha256': key(self.identity), 'jobs': results, 'issues': issues, 'events': self.cache.events}
        write(self.output / 'run-report.json', recovery.json_bytes(report))
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument('--article')
    scope.add_argument('--issue')
    scope.add_argument('--all', action='store_true')
    parser.add_argument('--output', type=Path, default=OUTPUT)
    parser.add_argument('--write-record', action='store_true', help='Record the successful six-article February checkpoint')
    args = parser.parse_args()
    try:
        runner = Runner(args.output)
        jobs = select(runner.data['jobs'], args.article, args.issue, args.all)
        report = runner.run(jobs)
        if args.write_record:
            require(args.issue == '1988-02' and all(j['status'] == 'prepared' for j in report['jobs']) and
                    len(report['jobs']) == 6 and report['issues']['maso-1988-02']['status'] == 'prepared', 'Record requires successful full February scope')
            require(runner.output.is_relative_to(ROOT / 'build'), 'Tracked record requires repo-private output')
            record = {k: v for k, v in report.items() if k != 'events'}
            record.update(checkpoint='13b', output_root=runner.output.relative_to(ROOT).as_posix(),
                          baseline_record=runner.profiles['baseline_record'], baseline_equivalence='article_JSON_and_Markdown_byte_exact; media_records_and_assets_unchanged',
                          print_verification='pending', limits=['no_new_sample_articles', 'full_disc_run_follows_13c', 'unknown_fonts_and_controls_fail_with_private_evidence'])
            root = runner.output / report['issues']['maso-1988-02']['package']
            record['outputs'] = [file_record(p.relative_to(runner.output).as_posix(), p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file()]
            write(ROOT / 'data/catalog/batch-runs/cd1-february.json', recovery.json_bytes(record))
        for job in report['jobs']:
            print(job['article_id'] + ': ' + job['status'] + (' — ' + job['error'] if 'error' in job else ''))
        print('Report: ' + str(runner.output / 'run-report.json'))
        return int(any(j['status'] != 'prepared' for j in report['jobs']) or any(i['status'] == 'failed' for i in report['issues'].values()))
    except (OSError, ValueError, KeyError) as error:
        print('Batch failed: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
