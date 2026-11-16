"""Portable JPEG cover sets, with reviewed roles and unchanged original rasters.

Cover faces are issue material, not invented TOC articles. Selected printed
labels are annotations; advertisement text is retained in the original raster.
This module neither selects global bookshelf covers nor generates reader output.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile

from jsonschema import Draft202012Validator
from PIL import Image

from .inventory import ROOT, pin, write_json
from .package import image_transform
from .build import safe_path

SCHEMA = ROOT / 'schemas/image-cover-set.schema.json'
ROLES = ('front', 'inside-front', 'inside-back', 'back')


def read(path):
    return json.loads(Path(path).read_bytes())


def checked(base, spec):
    path = safe_path(base, spec['path'])
    if (pin(base, spec['path'])['sha256'], path.stat().st_size) != (spec['sha256'], spec['bytes']):
        raise ValueError('Cover input hash differs: ' + spec['path'])
    return path


def inventory(folder):
    return [pin(folder, p.relative_to(folder).as_posix()) for p in sorted(folder.rglob('*'))
            if p.is_file() and p != folder / 'manifest.json']


def validate(package, source, review, schema):
    Draft202012Validator(schema).validate(package)
    if (package['id'] != 'scan-' + package['issue_id'] + '-covers' or
            source['kind'] != 'jpeg-set' or source['issue_id'] != package['issue_id']):
        raise ValueError('Cover issue/source identity differs')
    faces, missing = package['faces'], package['missing_faces']
    roles = [f['role'] for f in faces]
    absent = [f['role'] for f in missing]
    if (roles != [r for r in ROLES if r in roles] or len(set(roles)) != len(roles) or
            len(set(absent)) != len(absent) or set(roles) & set(absent) or
            set(roles + absent) != set(ROLES)):
        raise ValueError('Require distinct ordered cover roles and explicit missing outcomes')
    if package['availability'] != ('partial' if missing else 'complete'):
        raise ValueError('Cover availability differs from face coverage')
    if package['missing_faces'] != review['missing_faces'] or package['limitations'] != review['limitations']:
        raise ValueError('Cover review limitations or missing outcomes differ')
    pages = {p['source_index']: p for p in source['pages']}
    if len(pages) != len(source['pages']) or len({f['source_index'] for f in faces}) != len(faces):
        raise ValueError('Duplicate cover source identity')
    if len(review['faces']) != len(faces):
        raise ValueError('Cover review face coverage differs')
    orders = []
    for face, original in zip(faces, review['faces'], strict=True):
        if {k: v for k, v in face.items() if k not in ('asset', 'source_page')} != original:
            raise ValueError('Cover annotations differ from reviewed input')
        page = pages[face['source_index']]
        if (face['source_page'] != page or
                page['image_to_upright_normalized'] != image_transform(page) or
                face['asset']['path'] != 'faces/' + face['role'] + '.jpg' or
                any(face['asset'][k] != page['image'][k] for k in ('sha256', 'bytes'))):
            raise ValueError('Cover asset/geometry differs from original source')
        if page['reading_order'] is not None:
            orders.append(page['reading_order'])
        annotations = {a['id']: a for a in face['observations']}
        if len(annotations) != len(face['observations']):
            raise ValueError('Duplicate cover observation')
        for a in annotations.values():
            x0, y0, x1, y1 = a['bbox']
            if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1 and a['text'] in a['candidates']):
                raise ValueError('Invalid cover observation geometry or candidates')
        group_ids = [g['id'] for g in face['groups']]
        if len(set(group_ids)) != len(group_ids):
            raise ValueError('Duplicate cover annotation group')
        for group in face['groups']:
            members = group['member_observation_ids']
            if len(set(members)) != len(members) or not set(members) <= set(annotations):
                raise ValueError('Cover group references unknown or duplicate observations')
    if orders != sorted(set(orders)):
        raise ValueError('Cover roles disagree with reviewed source order')


def check_export(output):
    output = Path(output)
    manifest = read(output / 'manifest.json')
    if manifest['kind'] != 'jpeg-cover-set' or manifest['files'] != inventory(output):
        raise ValueError('Cover file inventory differs')
    package = read(output / 'cover-set.json')
    expected = {'cover-set.json', 'source.json', 'review.json', 'recipe.json', 'schema.json', 'provenance.json'}
    expected.update(f['asset']['path'] for f in package['faces'])
    if {s['path'] for s in manifest['files']} != expected:
        raise ValueError('Unexpected or missing cover package file')
    source, review = read(output / 'source.json'), read(output / 'review.json')
    provenance = read(output / 'provenance.json')
    for name in ('source', 'review', 'schema', 'recipe'):
        if provenance[name]['path'] != name + '.json':
            raise ValueError('Cover provenance path differs')
        checked(output, provenance[name])
    if (manifest['id'] != package['id'] or manifest['issue_id'] != package['issue_id'] or
            manifest['availability'] != package['availability'] or
            {k: package['source'][k] for k in ('sha256', 'bytes')} !=
            {k: provenance['source'][k] for k in ('sha256', 'bytes')}):
        raise ValueError('Cover manifest or retained source descriptor differs')
    recipe = read(output / 'recipe.json')
    if (recipe['issue_id'] != package['issue_id'] or recipe['source'] != package['source'] or
            any(recipe['review'][k] != provenance['review'][k] for k in ('sha256', 'bytes'))):
        raise ValueError('Retained cover recipe differs')
    validate(package, source, review, read(output / 'schema.json'))
    for face in package['faces']:
        path = checked(output, face['asset'])
        with Image.open(path) as image:
            if image.format != 'JPEG' or image.size != (face['source_page']['width_px'], face['source_page']['height_px']):
                raise ValueError('Cover raster dimensions/format differ')
            image.load()
    return package


def build(recipe_path, output, root=ROOT):
    recipe_path, output, root = Path(recipe_path).resolve(), Path(output).resolve(), Path(root).resolve()
    recipe = read(recipe_path)
    source_path = checked(root, recipe['source'])
    review_path = checked(recipe_path.parent, recipe['review'])
    source, review = read(source_path), read(review_path)
    if output.exists() or any(output.is_relative_to(p.parent) or p.is_relative_to(output)
                              for p in (source_path, review_path, recipe_path)):
        raise ValueError('Use a fresh cover output outside inputs')
    pages = {p['source_index']: p for p in source['pages']}
    package = dict(schema_version=1, kind='jpeg-cover-set', id='scan-' + recipe['issue_id'] + '-covers',
                   issue_id=recipe['issue_id'], source=recipe['source'], faces=[],
                   missing_faces=review['missing_faces'], availability='partial' if review['missing_faces'] else 'complete',
                   verification='sample-reviewed', coordinates='upright-normalized-top-left',
                   scope='Original cover rasters and selected source labels;not complete advertisement transcription.',
                   limitations=review['limitations'])
    for face in review['faces']:
        page = pages[face['source_index']]
        checked(root, page['image'])
        package['faces'].append(dict(deepcopy(face), source_page=page,
            asset=dict(page['image'], path='faces/' + face['role'] + '.jpg')))
    validate(package, source, review, read(SCHEMA))
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.jpeg-covers-', dir=output.parent) as temporary:
        stage = Path(temporary) / 'covers'
        (stage / 'faces').mkdir(parents=True)
        for face in package['faces']:
            shutil.copyfile(checked(root, face['source_page']['image']), stage / face['asset']['path'])
        for path, name in ((source_path, 'source'), (review_path, 'review'), (recipe_path, 'recipe'), (SCHEMA, 'schema')):
            shutil.copyfile(path, stage / (name + '.json'))
        write_json(stage / 'cover-set.json', package)
        write_json(stage / 'provenance.json', {name: pin(stage, name + '.json')
                                             for name in ('source', 'review', 'schema', 'recipe')})
        write_json(stage / 'manifest.json', dict(kind='jpeg-cover-set', id=package['id'], issue_id=package['issue_id'],
                                               availability=package['availability'], files=inventory(stage)))
        check_export(stage)
        checked(root, recipe['source'])
        checked(recipe_path.parent, recipe['review'])
        stage.rename(output)
    return package


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        package = check_export(args.output)
    else:
        if args.recipe is None:
            parser.error('--recipe is required when building')
        package = build(args.recipe, args.output)
    print(package['id'] + ': ' + package['availability'])


if __name__ == '__main__':
    main()
