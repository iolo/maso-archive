"""Opt-in literal source assembly with explicit, retained region supersession.

Every immutable native file is copied by the standard assembler. Active indexes
replace a revised region once; full original metadata remains separately retained.
Other formats delegate to the CP/M/graphic compatibility dispatcher.
"""
import argparse
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path

from . import assemble as assembly
from . import cpm_literal_assembly as cpm
from .assembly_indexes import block_ranges
from .build import check_export
from .package import validate_package

FORMAT = 'perspective-literal-v1'
START, END = 'utf8_byte_start', 'utf8_byte_end_exclusive'
_VALIDATE = assembly.validate_recipe
EXTRA = {'region_revisions', 'prose_continuations'}


def validate_recipe(recipe):
    if recipe.get('index_mode') != FORMAT:
        return cpm.validate_recipe(recipe)
    compatible = deepcopy(recipe)
    for key in EXTRA:
        compatible.pop(key, None)
    compatible['index_mode'] = 'namespaced-v1'
    _VALIDATE(compatible)
    names = {s['name'] for s in recipe['segments']}
    required = {'target_segment', 'revision_segment', 'region_id', 'block_id'}
    revisions = recipe.get('region_revisions')
    if not isinstance(revisions, list) or len(revisions) != 1:
        raise ValueError('One explicit retained region revision is required')
    row = revisions[0]
    if (set(row) != required or any(not isinstance(v, str) or not v for v in row.values())
            or row['target_segment'] not in names or row['revision_segment'] not in names
            or row['target_segment'] == row['revision_segment']):
        raise ValueError('Invalid region revision identity')
    joins = recipe.get('prose_continuations')
    fields = {'left_segment', 'left_block_id', 'right_segment', 'right_block_id', 'reason'}
    if not isinstance(joins, list):
        raise ValueError('Explicit prose continuation list is required')
    for row in joins:
        if (set(row) != fields or any(not isinstance(v, str) or not v for v in row.values())
                or row['left_segment'] not in names or row['right_segment'] not in names):
            raise ValueError('Invalid prose continuation identity')
    if recipe.get('shared_pdf_pages') or recipe.get('prose_joins'):
        raise ValueError('Region supersession uses its own explicit contract')


def project_record(value, *, article, listing, ranges, targets, listing_offset,
                   prefix, local_paths, inherited_download=None, inherited_block=None):
    """Project every nested occurrence by its actual source block, never text search."""
    args = dict(article=article, listing=listing, ranges=ranges, targets=targets,
                listing_offset=listing_offset, prefix=prefix, local_paths=local_paths)
    if isinstance(value, list):
        return [project_record(v, **args, inherited_download=inherited_download,
                               inherited_block=inherited_block) for v in value]
    if not isinstance(value, dict):
        return deepcopy(value)
    if {'path', 'sha256', 'bytes'} <= value.keys():
        return assembly.rebase(value, prefix) if value['path'] in local_paths else deepcopy(value)
    download = value.get('download', inherited_download)
    block = value.get('block_id', inherited_block)
    result = {k: project_record(v, **args, inherited_download=download,
                               inherited_block=block) for k, v in value.items()}
    if START in value or END in value:
        if START not in value or END not in value or download not in ('article.txt', 'listing.txt'):
            raise ValueError('Source range needs endpoints and a known download')
        start, end = value[START], value[END]
        data = article if download == 'article.txt' else listing
        if type(start) is not int or type(end) is not int or not 0 <= start <= end <= len(data):
            raise ValueError('Source range outside native download')
        try:
            data[:start].decode()
            text = data[start:end].decode()
        except UnicodeDecodeError as error:
            raise ValueError('Source range splits UTF-8') from error
        if 'transcription_excerpt' in value and text != value['transcription_excerpt']:
            raise ValueError('Source occurrence excerpt differs')
        if download == 'article.txt':
            if block not in ranges or block not in targets or not ranges[block][0] <= start <= end <= ranges[block][1]:
                raise ValueError('Source article occurrence outside its own active block')
            offset = targets[block][0] - ranges[block][0]
        else:
            offset = listing_offset
        result.update({START: start + offset, END: end + offset})
    if 'join_utf8_byte' in value:
        point = value['join_utf8_byte']
        if block not in ranges or not ranges[block][0] <= point <= ranges[block][1]:
            raise ValueError('Native prose boundary outside source block')
        article[:point].decode()
        result['join_utf8_byte'] = point + targets[block][0] - ranges[block][0]
    return result


def _one(rows, key, value):
    result = [r for r in rows if r[key] == value]
    if len(result) != 1:
        raise ValueError('Expected one source identity: ' + str(value))
    return result[0]


def validate_revision(spec, sources, specifications):
    target, old = sources[spec['target_segment']]
    revised, correction = sources[spec['revision_segment']]
    contract = correction.get('source_revision', {})
    region, block = spec['region_id'], spec['block_id']
    if (len(revised['regions']) != 1 or len(revised['blocks']) != 1 or revised['figures']
            or revised['regions'][0]['id'] != region or revised['blocks'][0]['id'] != block
            or revised['content_order'] != [dict(type='block', id=block)]):
        raise ValueError('Revision must contain exactly its one region and block')
    if any(target[k] != revised[k] for k in ('id', 'issue_id', 'toc_entry_id', 'source', 'toc_pin', 'title', 'coordinates')):
        raise ValueError('Revision article/source identity differs')
    if (contract.get('prior_pins', {}).get('manifest') != specifications[spec['target_segment']]['manifest']
            or contract.get('superseded_region_id') != region or contract.get('superseded_block_id') != block):
        raise ValueError('Revision does not bind its exact immutable target')
    prior_block = _one(target['blocks'], 'id', block)
    if prior_block['region_ids'] != [region] or revised['blocks'][0]['region_ids'] != [region]:
        raise ValueError('Revision may not replace part of a multi-region block')
    prior_region = _one(target['regions'], 'id', region)
    if (prior_region['pdf_index'] != revised['regions'][0]['pdf_index']
            or contract.get('prior_bbox') != prior_region['bbox']
            or contract.get('selected_bbox') != revised['regions'][0]['bbox']
            or revised['pages'] != [p for p in target['pages'] if p['pdf_index'] == prior_region['pdf_index']]):
        raise ValueError('Revision geometry/page metadata differs from contract')
    before, after = prior_block['text'].encode(), revised['blocks'][0]['text'].encode()
    at, inserted = contract.get('local_insertion_utf8_byte'), contract.get('inserted_text')
    if (type(at) is not int or not 0 <= at <= len(before) or inserted != ')'
            or after != before[:at] + inserted.encode() + before[at:]
            or contract.get('prior_text') != prior_block['text'] or contract.get('revised_text') != revised['blocks'][0]['text']):
        raise ValueError('Revision changes more than its observed parenthesis insertion')
    before[:at].decode()
    return contract


def project(recipe, originals):
    if recipe.get('index_mode') != FORMAT:
        return cpm.project(recipe, originals)
    validate_recipe(recipe)
    specs = {s['name']: s for s in recipe['segments']}
    sources = {s['name']: native for s, native in zip(recipe['segments'], originals, strict=True)}
    revision_spec = recipe['region_revisions'][0]
    contract = validate_revision(revision_spec, sources, specs)
    revision_name, target_name = revision_spec['revision_segment'], revision_spec['target_segment']
    rid, bid = revision_spec['region_id'], revision_spec['block_id']
    base_recipe = {k: deepcopy(v) for k, v in recipe.items() if k not in EXTRA}
    base_recipe['index_mode'] = 'namespaced-v1'
    base_recipe['segments'] = [s for s in recipe['segments'] if s['name'] != revision_name]
    base_recipe['resolved_notes'] = [r for r in recipe['resolved_notes'] if r['segment'] != revision_name]
    base_originals = [sources[s['name']] for s in base_recipe['segments']]
    package, combined = assembly.project_legacy(base_recipe, base_originals, check_listing_markers=False)
    revised, revision_correction = sources[revision_name]
    prefix = 'segments/' + revision_name
    package['regions'] = [deepcopy(revised['regions'][0]) if r['id'] == rid else r for r in package['regions']]
    package['blocks'] = [deepcopy(revised['blocks'][0]) if r['id'] == bid else r for r in package['blocks']]
    package['region_assets'] = [dict(region_id=rid, asset=assembly.rebase(revised['region_assets'][0]['asset'], prefix))
                                 if r['region_id'] == rid else r for r in package['region_assets']]
    replacement = {**deepcopy(revised['raw_ocr'][0]), **{k: assembly.rebase(revised['raw_ocr'][0][k], prefix) for k in ('text', 'positions', 'settings')}}
    package['raw_ocr'] = [deepcopy(replacement) if r['region_ids'] == [rid] else r for r in package['raw_ocr']]
    package['gaps'] = list(dict.fromkeys(package['gaps'] + revised['blocks'][0]['uncertainties']))
    package['verification']['uncertainties'] = package['gaps']
    for key in ('regions', 'blocks', 'figures'):
        if len({r['id'] for r in package[key]}) != len(package[key]):
            raise ValueError('Overlapping active native identities')
    reserved = {'records', 'blocks', 'normalizations', 'regional_transcription_sources', 'caption_associations_pending'}
    arrays = sorted({k for _, c in originals for k, v in c.items() if isinstance(v, list) and k not in reserved})
    for key in arrays:
        combined[key] = []
    combined.update(records=[], blocks=deepcopy(package['blocks']), literal_source_format=FORMAT,
        native_metadata=[], regional_transcription_sources=[], original_caption_associations=[],
        caption_associations_pending=[], source_revision=deepcopy(contract),
        resolved_source_revisions=[dict(**deepcopy(revision_spec), contract=deepcopy(contract),
            status='applied-once-at-original-reading-order', superseded_native_files_retained=True)])
    targets = block_ranges(package)
    combined_listing = assembly.text_bytes(package)[1]
    listing_offset = physical_offset = 0
    for spec, (source, correction) in zip(recipe['segments'], originals, strict=True):
        name, prefix = spec['name'], 'segments/' + spec['name']
        article, listing = assembly.text_bytes(source)
        ranges = block_ranges(source)
        active_ranges = {k: v for k, v in ranges.items() if not (name == target_name and k == bid)}
        for id, (start, end) in active_ranges.items():
            a, z = targets[id]
            if article[start:end] != assembly.text_bytes(package)[0][a:z]:
                raise ValueError('Active source block changed during assembly')
        if combined_listing[listing_offset:listing_offset + len(listing)] != listing:
            raise ValueError('Physical listing bytes changed during assembly')
        local_paths = {r['asset']['path'] for r in source['region_assets']}
        local_paths |= {r[k]['path'] for r in source['raw_ocr'] for k in ('text', 'positions', 'settings')}
        local_paths |= {'map.json', 'corrections.json', 'runtime.json', 'provenance.json', 'manifest.json'}
        args = dict(article=article, listing=listing, ranges=ranges, targets=targets,
                    listing_offset=listing_offset, prefix=prefix, local_paths=local_paths)
        combined['native_metadata'].append(dict(source_segment=name, directory=prefix,
            role='revision' if name == revision_name else 'base', original=deepcopy(correction),
            superseded_region_ids=[rid] if name == target_name else []))
        combined['regional_transcription_sources'].append(dict(source_segment=name,
            original_source_pins=deepcopy(correction.get('regional_transcription_sources', []))))
        combined['original_caption_associations'].append(dict(source_segment=name,
            original=deepcopy(correction.get('caption_associations_pending', []))))
        def superseded(row):
            return name == target_name and (row.get('region_id') == rid or row.get('block_id') == bid or row.get('id') == rid)
        for key in ['records'] + arrays:
            for row in correction.get(key, []):
                if isinstance(row, dict) and superseded(row):
                    continue
                result = project_record(row, **args)
                if isinstance(result, dict):
                    result['source_segment'] = name
                    if 'article_physical_line' in result:
                        result['article_physical_line'] += physical_offset
                combined[key].append(result)
        listing_offset += len(listing)
        physical_offset += len(correction.get('listing_line_index', []))
    if len({r['id'] for r in combined['records']}) != len(package['regions']):
        raise ValueError('Active correction record coverage differs')
    _resolve_captions(recipe, sources, package, combined)
    _connect_sources(recipe, sources, package, combined)
    combined['normalizations'] = deepcopy(package['gaps'])
    combined['resolved_notes'] = deepcopy(recipe['resolved_notes'])
    combined['segments'].append(dict(name=revision_name, directory='segments/' + revision_name, role='superseding-region-revision'))
    combined['coverage'].update(source_bytes='unverified', execution_verified=False,
        revision_applied=True, duplicate_revision_page=False)
    validate_package(package)
    return package, combined


def _resolve_captions(recipe, sources, package, combined):
    specs = {s['name']: s for s in recipe['segments']}
    combined['resolved_caption_associations'] = []
    for spec in recipe['segments']:
        for pending in sources[spec['name']][1].get('caption_associations_pending', []):
            native = sources[spec['name']][0]
            _one([r for r in native['blocks'] if r['kind'] == 'code'], 'id', pending['listing_id'])
            if not pending['figure_ids'] or len(set(pending['figure_ids'])) != len(pending['figure_ids']):
                raise ValueError('Pending caption needs distinct local source frames')
            for id in pending['figure_ids']:
                _one(native['figures'], 'id', id)
            ext = pending['external_caption']
            owners = [name for name, row in specs.items() if row['manifest'] == ext['source_package_manifest']]
            if len(owners) != 1:
                raise ValueError('External caption has no exact immutable owner')
            owner = owners[0]
            source, correction = sources[owner]
            caption = _one(source['blocks'], 'id', ext['source_caption_block_id'])
            region = ext['source_caption_region_id']
            article = assembly.text_bytes(source)[0]
            start, end = ext['external_utf8_byte_start'], ext['external_utf8_byte_end_exclusive']
            row = _one([r for r in correction['regional_text_index'] if r['region_id'] == region], 'block_id', caption['id'])
            if (region not in caption['region_ids'] or (start, end) != (row[START], row[END])
                    or article[start:end].decode() != ext['caption_text'] or caption['text'] != ext['caption_text']):
                raise ValueError('External caption occurrence differs')
            parent = specs[owner]['manifest']['path'].rsplit('/', 1)[0]
            expected = dict(source_corrections=source['corrections'][0],
                source_download=_one(source['downloads'], 'path', 'article.txt'),
                source_scan=_one(source['region_assets'], 'region_id', region)['asset'])
            for key, pin in expected.items():
                if ext[key] != {**pin, 'path': parent + '/' + pin['path']}:
                    raise ValueError('External caption source pin differs')
            projected = _one([r for r in combined['regional_text_index'] if r['source_segment'] == owner and r['region_id'] == region], 'block_id', caption['id'])
            combined['listing_caption_links'].append(dict(block_id=caption['id'],
                caption_block_id=caption['id'], caption_region_id=region, listing_id=pending['listing_id'],
                block_ids=[pending['listing_id']], figure_ids=deepcopy(pending['figure_ids']),
                download='article.txt', scan=deepcopy(projected['scan']),
                **{START: projected[START], END: projected[END]}, transcription_excerpt=caption['text'],
                assembly_derived=True, source_segment=spec['name'], caption_source_segment=owner))
            for id in pending['figure_ids']:
                figure = _one(package['figures'], 'id', id)
                if figure['caption'] is not None:
                    raise ValueError('Pending caption frame already has a different owner')
                figure['caption'] = caption['text']
                combined['caption_links'].append(dict(figure_id=id, figure_region_id=id,
                    caption_block_id=caption['id'], caption_region_id=region,
                    internal_text_transcribed=True, assembly_derived=True, caption_source_segment=owner))
                combined['caption_part_index'].append({**deepcopy(projected), 'figure_id': id,
                    'caption_block_id': caption['id'], 'caption_part_index': 1,
                    'kind': 'resolved-known-external-listing-heading', 'assembly_derived': True})
            combined['resolved_caption_associations'].append(dict(source_segment=spec['name'],
                original=deepcopy(pending), caption_source_segment=owner, status='resolved-from-exact-native-occurrence'))
    resolved = {id for r in combined['resolved_caption_associations'] for id in r['original']['figure_ids']}
    combined['uncaptioned_figure_index'] = [r for r in combined['uncaptioned_figure_index'] if r['figure_id'] not in resolved]


def _connect_sources(recipe, sources, package, combined):
    combined['cross_native_prose_boundaries'] = []
    for row in recipe['prose_continuations']:
        left, right = [], []
        for name, id, out in [(row['left_segment'], row['left_block_id'], left),
                              (row['right_segment'], row['right_block_id'], right)]:
            out.extend(r for r in combined['regional_text_index'] if r['source_segment'] == name and r['block_id'] == id)
        if not left or not right:
            raise ValueError('Missing explicit prose continuation occurrence')
        order = [x['id'] for x in package['content_order'] if x['type'] == 'block']
        if order.index(row['left_block_id']) >= order.index(row['right_block_id']):
            raise ValueError('Prose continuation reverses source order')
        combined['cross_native_prose_boundaries'].append(dict(**deepcopy(row),
            left=deepcopy(left[-1]), right=deepcopy(right[0]),
            policy='Source blocks and original image anchors retained; association adds no text or source glyphs.'))
    combined['connected_listing_groups'] = []
    for row in combined['source_code_connections']:
        if 'incoming_listing_id' not in row:
            continue
        current, incoming = row['listing_id'], row['incoming_listing_id']
        owners = [spec for spec in recipe['segments'] if incoming in {b['id'] for b in sources[spec['name']][0]['blocks']}]
        if len(owners) != 1 or row.get('incoming_package') != owners[0]['manifest']:
            raise ValueError('Listing connection differs from exact incoming native')
        first = [r for r in combined['logical_listing_line_index'] if r['listing_id'] == current]
        previous = [r for r in combined['logical_listing_line_index'] if r['listing_id'] == incoming]
        if not first or not previous or previous[-1][END] != first[0][START]:
            raise ValueError('Listing continuation does not preserve adjacent physical bytes')
        combined['connected_listing_groups'].append(dict(listing_ids=[incoming, current],
            last_incoming_printed_line=previous[-1]['printed_line'], first_continuation_printed_line=first[0]['printed_line'],
            source_connection=deepcopy(row), physical_bytes_preserved=True,
            policy='Independent source versions;physical wraps and native listing IDs retained without executable flattening.'))
    for row in combined['source_code_connections']:
        row['assembly_resolution'] = 'Complete source connection;original native requirement fields retained as provenance.'
    combined['flowchart_connections'] = [deepcopy(row) for _, correction in sources.values()
        for row in correction.get('segment_scope', {}).get('flowchart_connections', [])]
    active_regions = {r['id'] for r in package['regions']}
    for row in combined['flowchart_connections']:
        if not {row['opening_region'], row['continuation_region']} <= active_regions:
            raise ValueError('Flowchart continuation lacks an original frame')


@contextmanager
def installed():
    with cpm.installed():
        previous = assembly.project, assembly.validate_recipe
        assembly.project, assembly.validate_recipe = project, validate_recipe
        try:
            yield
        finally:
            assembly.project, assembly.validate_recipe = previous


def assemble(recipe, output, root=assembly.ROOT):
    with installed():
        return assembly.assemble(recipe, output, root=root)


def check(output):
    with installed():
        return check_export(Path(output))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if not args.check and args.recipe is None:
        parser.error('--recipe is required')
    package = check(args.output) if args.check else assemble(args.recipe, args.output)
    print(f"Perspective literal assembly: {package['id']} / {package['availability']}")


if __name__ == '__main__':
    main()
