"""Isolated 19a article pipeline; only exact-job, recorded policy and recovery differ."""
from copy import deepcopy
from pathlib import Path
import re

from tools import run_cd1_batch as base
from tools.run_cd1_batch import (ROOT, read_json, put, inventory, images, recovery,
    markdown, package, map_blocks, reading_sections, project_section, assemble,
    validate_bundle, BASELINE, checked_file, file_record, load_package, digest,
    require, Cache, key, write)
from tools.cd1_batch_cache import verify
from tools.batch import codec_review, oem_runs, symbol_arrow_pipeline

OUTPUT = ROOT / 'build/cd1-oem-sample'


def safe_output(output):
    output=symbol_arrow_pipeline.safe_output(output)
    for old in (symbol_arrow_pipeline.OUTPUT, ROOT/'build/cd1-symbol-pass', codec_review.OUTPUT):
        require(not output.is_relative_to(old) and not old.is_relative_to(output), 'OEM retry overlaps historical evidence')
    return output


class OemRunner(symbol_arrow_pipeline.ArrowRunner):
    def __init__(self, output=OUTPUT):
        super().__init__(safe_output(output))
        review=read_json(codec_review.RECORD)
        require(review['pipeline_identity_sha256']==key(self.identity), 'Codec review pipeline changed')
        require(review['code_sha256']==digest(Path(codec_review.__file__).read_bytes()), 'Codec review implementation changed')
        for name in ('current_record','prior_review_record'):checked_file(ROOT,review[name])
        codec_review.mapping_table()
        self.codec_review_root=ROOT/review['output_root']
        manifest=verify(self.codec_review_root,review['fingerprint'])
        require(manifest['outputs']==review['outputs'],'Codec review outputs changed')
        policy=read_json(self.codec_review_root/'policy.json')
        require(policy['source_rtf_sha256']==digest(self.rtf),'Codec review source changed')
        self.oem_policies=policy['articles']
        require(set(self.oem_policies)==codec_review.READY and not(set(self.oem_policies)&set(self.policy['article_fonts'])), 'OEM policy population changed')
        self.oem_jobs={j['source_reference']:j for j in self.data['jobs'] if j['source_reference'] in codec_review.READY}
        rows=read_json(self.codec_review_root/'runs.json')
        for ref,job in self.oem_jobs.items():
            require(self.oem_policies[ref]==codec_review.make_policy(job,[r for r in rows if r['reference']==ref]),'OEM source policy changed')
        self.identity={**self.identity,'oem_run_extension':{
            'implementation_sha256':digest(Path(__file__).read_bytes()),'adapter_sha256':digest(Path(oem_runs.__file__).read_bytes()),
            'frozen_stages_sha256':digest(Path(base.__file__).read_bytes()),'review_record_sha256':digest(codec_review.RECORD.read_bytes()),
            'policy_sha256':key(self.oem_policies)}}
        self.cache=Cache(self.output/'stages',self.identity)

    def process(self, job):
        require(job['source_reference'] in self.oem_jobs and job == self.oem_jobs[job['source_reference']], 'Article outside exact OEM jobs')
        ref = job['source_reference']
        require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', ref) is not None, 'Unsafe article identity')
        profile = self.profiles['articles'].get(ref)
        if profile:
            require(profile['source_topics'] == job['source_topics'], 'Reviewed source association changed')
        extra_fonts = self.policy['article_fonts'].get(ref)
        if extra_fonts:
            require(extra_fonts['source_topics'] == job['source_topics'], 'Additional font evidence changed')
        codecs = {int(k): v for k, v in (profile['font_codecs'] if profile else self.policy['default_font_codecs']).items()}
        if extra_fonts:
            codecs.update({int(k): v for k, v in extra_fonts['font_codecs'].items()})
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
            auxiliary_records = []
            for destination in sorted({link['target_topic_id'] for link in links} - selected):
                if destination in self.policy['auxiliaries']:
                    decision = self.policy['auxiliaries'][destination]
                    source = self.topic_lookup[destination]
                    require(source['rtf'] == decision['rtf'] and source['aliases'] == decision['aliases'] and source['links'] == decision['links'], 'Auxiliary source decision changed')
                    start, length = source['rtf']['byte_offset'], source['rtf']['byte_length']
                    raw = self.rtf[start:start + length]
                    require(digest(raw) == source['rtf']['sha256'], 'Auxiliary bytes changed')
                    path = target / 'auxiliaries' / str(source['native']['ordinal'])
                    path.mkdir(parents=True)
                    (path / 'source.rtf').write_bytes(raw)
                    evidence = {'topic_id': destination, **decision}
                    try:
                        initial = {k: v for k, v in self.states[start].items() if k != 'unknown'}
                        require(not self.states[start]['unknown'], 'Unsupported auxiliary inherited formatting')
                        report = inventory.inspect_topic(raw, start, initial['character']['font_id'])
                        report.update(ordinal=source['native']['ordinal'], role='linked_auxiliary')
                        put(path, 'inventory.json', report)
                        require(not report['issues'], 'Unsupported auxiliary controls')
                        recovered_aux = recovery.recover_topic(self.rtf, report, initial, {int(k): v for k,v in self.policy['default_font_codecs'].items()})
                        put(path, 'recovery.json', recovered_aux)
                        require(not recovered_aux['issues'], 'Undecoded auxiliary text')
                        evidence.update(recovery_status='recovered', paragraphs=len(recovered_aux['paragraphs']))
                        resources = sorted({r['object']['resource'] for p in recovered_aux['paragraphs'] for r in p['runs'] if r['kind'] == 'object'})
                        evidence['media'] = []
                        for resource in resources:
                            raw_media = images.checked_source(resource, self.media_manifest)
                            evidence['media'].append({'resource': resource, 'sha256': digest(raw_media), 'status': 'source_preserved; auxiliary_rendering_deferred'})
                    except Exception as error:
                        evidence.update(recovery_status='deferred', error_type=type(error).__name__, error=str(error))
                    put(path, 'disposition.json', evidence)
                    auxiliary_records.append(evidence)
            put(target, 'auxiliaries.json', auxiliary_records)
            for link in links:
                destination = link['target_topic_id']
                require(destination in selected or destination in self.policy['auxiliaries'] or destination in self.topic_lookup and
                        self.topic_lookup[destination]['role'] in ('navigation', 'application_resource_topic', 'formatting_separator'),
                        'Related content outside selected topics needs ownership review: ' + str(destination))
            for topic in job['source_topics']:
                span = topic['rtf']
                raw = self.rtf[span['byte_offset']:span['byte_offset'] + span['byte_length']]
                require(digest(raw) == span['sha256'], 'Topic bytes changed')
                (target / f"topic-{topic['native']['ordinal']}.rtf").write_bytes(raw)
            put(target, 'association.json', job)
        associated = stage('association', associate)
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
            put(target, 'encoding-policy.json', {'font_codecs': codecs, 'unknown_fonts': 'retain_undecoded_and_fail', 'basis': 'source_bound_reviewed_CD1_fonts', 'oem_run_policy': self.oem_policies[ref]})
            for report in read_json(inspected / 'inventory.json'):
                initial = {k: v for k, v in self.states[report['byte_offset']].items() if k != 'unknown'}
                topic = oem_runs.recover_topic(self.rtf, report, initial, codecs, self.oem_policies[ref])
                topics.append(topic)
                put(target, 'recovery.json', {'schema_version': 1, 'cd_reference': ref, 'topics': topics})
                require(not topic['issues'], 'Undecoded text retained in recovery evidence')
                require(all(p['terminated_by_par'] for p in topic['paragraphs']), 'Unterminated paragraph needs representation review')
        recovered = stage('recovery', recover)
        article = read_json(recovered / 'recovery.json')
        mapped = stage('semantics', lambda target: put(target, 'blocks.json', map_blocks(article, profile, job)))
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
                if block['type'] == 'unresolved' or not profile and block['type'] != 'spacing':
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
                                          'auxiliary_evidence': read_json(associated / 'auxiliaries.json'),
                                          'historical_evidence': self.baseline_evidence['article_evidence'][ref] if profile else None,
                                          'validation': validate_bundle(bundle)})
        packaged = stage('package', assemble_article, lambda root: load_package(root / 'content'))
        result = {'status': 'prepared', 'package': packaged.relative_to(self.output).as_posix(), 'stages': stages,
                  'counts': validate_bundle(bundle), 'deferred_media': [m['id'] for m in media if m['status'] != 'available'],
                  'semantic_review': 'reviewed_source_decisions' if profile else 'pending',
                  'auxiliaries': read_json(associated / 'auxiliaries.json')}
        write(self.output / 'articles' / (token + '.json'), recovery.json_bytes({'identity_sha256': key(self.identity), **result}))
        return result
