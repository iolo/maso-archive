"""Data-only JPEG issue export: native articles, covers and all source dispositions.

This complete-issue gate never performs OCR or builds a reading room. Original
article packages remain intact; unlisted source rasters are copied unchanged.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import shutil
import tempfile

from jsonschema import Draft202012Validator
from PIL import Image

from .build import check_export as check_article, safe_path
from .image_covers import check_export as check_covers, checked, inventory, read
from .inventory import ROOT, pin, write_json

SCHEMA = ROOT / 'schemas/image-issue.schema.json'
OTHER = {'advertisement', 'table-of-contents', 'unlisted-notice', 'section-divider', 'unlisted-form'}
LIMITATIONS = [
    'Complete means structural article/source accounting and reproducible native artifacts;human acceptance and character-perfect proofreading are not claimed.',
    'Article packages retain their own source ranges,exclusions,glyph alternatives,gaps and verification limits;original encoded bytes and execution remain unverified.',
    'Unlisted material retains full original rasters and selected visual-disposition labels;complete unlisted-text transcription is not claimed.',
    'Source-image coverage does not claim every printed region was transcribed or that every physical page was supplied.',
    'External repository-relative evidence and reconstruction-input pins remain provenance references;the issue contains native component artifacts and unlisted rasters,not the entire working archive.',
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def same_bytes(a, b):
    return all(a[k] == b[k] for k in ('sha256', 'bytes'))


def slug(value):
    require(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', value),
            'Unsafe issue/component identity')
    return value


def toc_rows(path, issue_id):
    return [row for line in Path(path).read_text().splitlines() if line.strip()
            for row in [json.loads(line)] if row['issue_id'] == issue_id]


def validate_accounting(ledger, toc, source, accounting, articles, covers):
    """Cross-check actual native ownership against canonical identities and sources."""
    issue_id = ledger['issue_id']
    require(source['kind'] == 'jpeg-set' and source['issue_id'] == accounting['issue_id'] == issue_id,
            'Issue/source identity differs')
    entries = ledger['entries']
    ids = [t['id'] for t in toc]
    require(ids and len(ids) == len(set(ids)) and [e['toc_entry_id'] for e in entries] == ids,
            'Canonical TOC coverage/order differs')
    require(all(t['issue_id'] == issue_id for t in toc), 'Foreign canonical TOC entry')
    article_ids, headings = [], []
    owners = {}
    pages = source['pages']
    by_index = {p['source_index']:p for p in pages}
    require(len(by_index) == len(pages) and len({p['image']['path'] for p in pages}) == len(pages),
            'Duplicate source identity')
    orders = [p['reading_order'] for p in pages]
    require(all(isinstance(n, int) and n > 0 for n in orders) and len(set(orders)) == len(orders),
            'Missing/duplicate source order')
    for e, t in zip(entries, toc, strict=True):
        require(e['title'] == t['title_candidate'] and e['parent_id'] == t['parent_id'],
                'Canonical title/parent differs')
        require(e['parent_id'] is None or e['parent_id'] in ids, 'Unknown canonical parent')
        if e['classification'] == 'group-heading':
            require(e['body_owner'] is False and e['availability'] == 'not-applicable' and
                    e.get('restoration') is None and 'package' not in e and
                    e['group_reference']['owns_standalone_body'] is False,
                    'Heading acquired article ownership')
            require(e['child_toc_entry_ids'] == [t2['id'] for t2 in toc if t2['parent_id'] == t['id']],
                    'Heading child context differs')
            headings.append(e['toc_entry_id'])
            continue
        require(e['classification'] == 'article' and e['body_owner'] is True,
                'Unresolved or unsupported canonical disposition')
        a = articles[e['toc_entry_id']]
        require(a['issue_id'] == issue_id and a['toc_entry_id'] == e['toc_entry_id'] and
                a['availability'] == e['availability'] == 'readable' and
                a['verification']['status'] == e['verification'], 'Native article identity/outcome differs')
        slug(a['id']); article_ids.append(a['id'])
        require(a['source']['kind'] == 'jpeg-set' and same_bytes(a['source'], accounting['source_descriptor']),
                'Article source descriptor differs')
        require(len({p['source_index'] for p in a['pages']}) == len(a['pages']), 'Duplicate article source')
        for p in a['pages']:
            original = by_index[p['source_index']]
            for key in ('image', 'width_px', 'height_px', 'reading_order', 'source_filename_number'):
                require(p.get(key) == original.get(key), 'Article source geometry/identity differs')
            regions = [r['id'] for r in a['regions'] if r['source_index'] == p['source_index']]
            require(regions, 'Article source has no mapped ownership')
            owners.setdefault(p['source_index'], []).append(dict(toc_entry_id=e['toc_entry_id'],
                article_id=a['id'], package_manifest=e['package']['manifest'], region_ids=regions))
    require(set(articles) == {e['toc_entry_id'] for e in entries if e['classification'] == 'article'} and
            len(article_ids) == len(set(article_ids)), 'Duplicate/unaccounted native article')
    require(ledger['canonical_identities'] == len(toc) and ledger['readable_articles'] == len(article_ids) and
            ledger['group_headings'] == len(headings) and ledger['partial_articles'] == 0 and
            ledger['identitiesAwaitingDisposition'] == 0, 'Canonical outcome counts differ')
    require(covers['issue_id'] == issue_id and covers['availability'] == 'complete' and
            same_bytes(covers['source'], accounting['source_descriptor']) and
            ledger['cover_set']['manifest'] == accounting['cover_package_manifest'],
            'Incomplete/foreign cover set or differing manifest')
    cover_faces = {f['source_index']:f for f in covers['faces']}
    require(not set(owners) & set(cover_faces), 'Cover acquired canonical article ownership')
    rows = accounting['records']
    ordered = sorted(pages, key=lambda p:p['reading_order'])
    require(accounting['kind'] == 'jpeg-issue-source-accounting' and
            accounting['total_source_images'] == len(rows) == len(pages) and
            accounting['all_source_images_visually_disposed'] is True and
            accounting['remaining_visual_dispositions'] == 0, 'Incomplete source accounting')
    require([r['source_index'] for r in rows] == [p['source_index'] for p in ordered],
            'Lost/duplicated/reordered source disposition')
    others = []
    for row, original in zip(rows, ordered, strict=True):
        for key in ('source_index', 'width_px', 'height_px', 'reading_order', 'source_filename_number'):
            require(row.get(key) == original.get(key), 'Disposition source geometry/identity differs')
        require(row['source_image'] == original['image'], 'Disposition source pin differs')
        i, kind = row['source_index'], row['classification']
        if i in owners:
            require(kind == 'selected-article-source' and row['article_owners'] == owners[i] and
                    'visual_disposition' not in row, 'Native article source ownership differs')
        elif i in cover_faces:
            require(kind == 'cover' and row['face'] == cover_faces[i]['role'] and
                    row['cover_package_manifest'] == accounting['cover_package_manifest'] and
                    'article_owners' not in row, 'Cover source ownership differs')
        else:
            require(kind in OTHER and 'article_owners' not in row, 'Unclassified/unowned source image')
            d = row['visual_disposition']
            require(d['source_index'] == i and d['source_image'] == row['source_image'] and
                    d['source_filename_number'] == row.get('source_filename_number') and
                    d['reading_order'] == row['reading_order'] and d['classification'] == kind and
                    d['body_owner_toc_entry_id'] is None and d['complete_text_transcription'] is False and
                    d['printed_folio_observed'] is None and d['observed_label'] and d['notes'],
                    'Unlisted disposition/claim differs')
            require(set(d.get('related_nonowning_heading_ids', [])) <= set(headings),
                    'Divider references unknown/non-heading identity')
            others.append(row)
    require(accounting['counts'] == dict(Counter(r['classification'] for r in rows)),
            'Source classification counts differ')
    expected_groups = {g: [r['source_index'] for r in others if r['visual_disposition']['group_id'] == g]
                       for g in {r['visual_disposition']['group_id'] for r in others} if g}
    require(len({g['id'] for g in accounting['groups']}) == len(accounting['groups']) and
            {g['id']:g['source_indices'] for g in accounting['groups']} == expected_groups and
            all(g['relationship'] for g in accounting['groups']), 'Source grouping differs')
    return dict(canonical_identities=len(toc), article_packages=len(article_ids), group_headings=len(headings),
                source_images=len(pages), selected_article_source_images=len(owners), cover_faces=len(cover_faces),
                other_source_images=len(others), source_classifications=accounting['counts'])


def projection(ledger, accounting, articles, counts):
    issue_id = ledger['issue_id']
    result = dict(schema_version=1, kind='jpeg-issue', id='scan-' + issue_id + '-issue', issue_id=issue_id,
                  availability='complete', verification='sample-reviewed', counts=counts,
                  articles=[], headings=[], covers={}, other_sources=[], limitations=LIMITATIONS)
    for e in ledger['entries']:
        id = slug(e['toc_entry_id'])
        if e['classification'] == 'article':
            a = articles[id]
            result['articles'].append(dict(toc_entry_id=id, article_id=a['id'],
                path='articles/' + id + '/article.json', original_manifest=e['package']['manifest']))
        else:
            result['headings'].append(dict(toc_entry_id=id,body_owner=False,
                evidence='headings/' + id + '.json', validation='headings/' + id + '-validation.json',
                original_evidence=e['group_reference']['evidence'],original_validation=e['group_reference']['validation']))
    result['covers'] = dict(path='covers/cover-set.json',original_manifest=ledger['cover_set']['manifest'])
    for row in accounting['records']:
        if row['classification'] in OTHER:
            result['other_sources'].append(dict(source_index=row['source_index'],
                classification=row['classification'], original=row['source_image'],
                asset=dict(row['source_image'],path='other-sources/source-' + str(row['source_index']) + '.jpg')))
    return result


def check_export(output):
    output = Path(output)
    manifest = read(output/'manifest.json')
    require(manifest['kind'] == 'jpeg-issue' and manifest['files'] == inventory(output), 'Issue file inventory differs')
    package = read(output/'issue.json')
    Draft202012Validator(read(output/'schema.json')).validate(package)
    recipe, provenance = read(output/'recipe.json'), read(output/'provenance.json')
    expected = {'issue.json','schema.json','recipe.json','provenance.json','source.json','ledger.json','toc.jsonl','source-accounting.json'}
    for key,name in [('source','source.json'),('ledger','ledger.json'),('toc','toc.jsonl'),('accounting','source-accounting.json')]:
        require(provenance[key]['path'] == name and same_bytes(recipe[key],provenance[key]), 'Issue retained input binding differs')
        checked(output,provenance[key])
    for key in ('recipe','schema'):
        require(provenance[key]['path'] == key + '.json', 'Issue provenance path differs')
        checked(output,provenance[key])
    ledger, source, accounting = read(output/'ledger.json'), read(output/'source.json'), read(output/'source-accounting.json')
    require(recipe['issue_id'] == ledger['issue_id'] == package['issue_id'] and
            same_bytes(accounting['source_descriptor'],recipe['source']) and
            ledger['source_accounting']['status'] == 'complete' and
            ledger['source_accounting']['accounting'] == recipe['accounting'] and
            recipe['toc'] in source['toc_inputs'], 'Issue recipe/ledger/source binding differs')
    articles = {}
    for item in package['articles']:
        id = slug(item['toc_entry_id']); path = 'articles/' + id
        require(item['path'] == path + '/article.json' and id not in articles, 'Duplicate/unsafe article path')
        folder = safe_path(output,path)
        require(same_bytes(pin(folder,'manifest.json'),item['original_manifest']), 'Copied article manifest differs')
        articles[id] = check_article(folder)
        expected.update(path + '/' + r['path'] for r in read(folder/'manifest.json')['files'])
        expected.add(path + '/manifest.json')
    cover_folder = output/'covers'
    require(package['covers']['path'] == 'covers/cover-set.json' and
            same_bytes(pin(cover_folder,'manifest.json'),package['covers']['original_manifest']), 'Copied cover manifest differs')
    covers = check_covers(cover_folder)
    expected.update('covers/' + r['path'] for r in read(cover_folder/'manifest.json')['files'])
    expected.add('covers/manifest.json')
    toc = toc_rows(output/'toc.jsonl',package['issue_id'])
    counts = validate_accounting(ledger,toc,source,accounting,articles,covers)
    require(package == projection(ledger,accounting,articles,counts), 'Issue component projection differs')
    for item in package['headings']:
        for key in ('evidence','validation'):
            p = safe_path(output,item[key]); require(same_bytes(pin(output,item[key]),item['original_' + key]), 'Heading evidence differs')
            expected.add(item[key])
        outcome = read(output/item['evidence'])
        entry = next(e for e in ledger['entries'] if e['toc_entry_id']==item['toc_entry_id'])
        require(outcome['issue_id']==package['issue_id'] and outcome['toc_entry_id']==item['toc_entry_id'] and
                outcome['body_owner'] is False and outcome['restoration'] is None and
                outcome['title']==entry['title'] and outcome['parent_id']==entry['parent_id'] and
                outcome['child_toc_entry_ids']==entry['child_toc_entry_ids'], 'Heading outcome/context differs')
    page_lookup = {p['source_index']:p for p in source['pages']}
    for item in package['other_sources']:
        path = checked(output,item['asset']); expected.add(item['asset']['path'])
        require(same_bytes(item['asset'],item['original']), 'Unlisted original bytes differ')
        page = page_lookup[item['source_index']]
        with Image.open(path) as im:
            require(im.format=='JPEG' and im.size==(page['width_px'],page['height_px']), 'Unlisted raster geometry/format differs')
            im.load()
    require({r['path'] for r in manifest['files']} == expected, 'Unexpected/missing issue files')
    require(manifest['id']==package['id'] and manifest['issue_id']==package['issue_id'] and
            manifest['availability']==package['availability'], 'Issue manifest identity/outcome differs')
    return package


def build(recipe_path, output, root=ROOT):
    recipe_path, output, root = (Path(p).resolve() for p in (recipe_path,output,root))
    require(not output.exists(), 'Use a fresh issue output')
    recipe = read(recipe_path); slug(recipe['issue_id'])
    inputs = {k:checked(root,recipe[k]) for k in ('source','ledger','toc','accounting')}
    ledger, source, accounting = (read(inputs[k]) for k in ('ledger','source','accounting'))
    require(ledger['issue_id']==recipe['issue_id'] and ledger['source_accounting']['status']=='complete' and
            ledger['source_accounting']['accounting']==recipe['accounting'] and
            recipe['toc'] in source['toc_inputs'] and same_bytes(recipe['source'],accounting['source_descriptor']),
            'Issue recipe input bindings differ')
    folders, articles = {}, {}
    extra_inputs = [recipe_path, SCHEMA, *inputs.values()]
    for e in ledger['entries']:
        slug(e['toc_entry_id'])
        if e['classification'] != 'article': continue
        folder = safe_path(root,e['package']['path'])
        require(e['package']['manifest']['path'] == e['package']['path'] + '/manifest.json', 'Article manifest path differs')
        checked(root,e['package']['manifest']); extra_inputs.append(folder)
        require(e['toc_entry_id'] not in articles, 'Duplicate selected article')
        folders[e['toc_entry_id']] = folder
        articles[e['toc_entry_id']] = check_article(folder)
    cover_folder = safe_path(root,ledger['cover_set']['path'])
    require(ledger['cover_set']['manifest']['path']==ledger['cover_set']['path']+'/manifest.json' and
            ledger['cover_set']['manifest']==accounting['cover_package_manifest'], 'Cover manifest binding differs')
    checked(root,ledger['cover_set']['manifest']);extra_inputs.append(cover_folder)
    covers = check_covers(cover_folder)
    counts = validate_accounting(ledger,toc_rows(inputs['toc'],recipe['issue_id']),source,accounting,articles,covers)
    package = projection(ledger,accounting,articles,counts)
    Draft202012Validator(read(SCHEMA)).validate(package)
    for p in source['pages']:
        extra_inputs.append(checked(root,p['image']))
    for item in package['headings']:
        for key in ('evidence','validation'):extra_inputs.append(checked(root,item['original_'+key]))
    require(not any(output == p or (p.is_dir() and output.is_relative_to(p)) or p.is_relative_to(output)
                    for p in extra_inputs), 'Issue output overlaps inputs')
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent,prefix='.jpeg-issue-') as temporary:
        stage = Path(temporary)/'issue';stage.mkdir()
        for id,folder in folders.items():shutil.copytree(folder,stage/'articles'/id)
        shutil.copytree(cover_folder,stage/'covers')
        for item in package['headings']:
            for key in ('evidence','validation'):
                target=stage/item[key];target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(checked(root,item['original_'+key]),target)
        for item in package['other_sources']:
            target=stage/item['asset']['path'];target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(checked(root,item['original']),target)
        for key,name in [('source','source.json'),('ledger','ledger.json'),('toc','toc.jsonl'),('accounting','source-accounting.json')]:
            shutil.copyfile(inputs[key],stage/name)
        shutil.copyfile(recipe_path,stage/'recipe.json');shutil.copyfile(SCHEMA,stage/'schema.json')
        write_json(stage/'issue.json',package)
        write_json(stage/'provenance.json',{k:pin(stage,n) for k,n in [('source','source.json'),('ledger','ledger.json'),
            ('toc','toc.jsonl'),('accounting','source-accounting.json'),('recipe','recipe.json'),('schema','schema.json')]})
        write_json(stage/'manifest.json',dict(kind='jpeg-issue',id=package['id'],issue_id=package['issue_id'],
            availability=package['availability'],files=inventory(stage)))
        check_export(stage)
        for k,p in inputs.items():checked(root,recipe[k])
        stage.rename(output)
    return package


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.check:package=check_export(args.output)
    else:
        if args.recipe is None:parser.error('--recipe is required when building')
        package=build(args.recipe,args.output)
    print(package['id'] + ': ' + package['availability'])


if __name__=='__main__':main()
