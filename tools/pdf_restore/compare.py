"""Export a bounded, manually reviewed scan/CD comparison without editing either source."""
import argparse
from difflib import SequenceMatcher
import json
from pathlib import Path
import tempfile

from .build import checked, check_export, copy_pin
from .inventory import ROOT, pin, write_json


def differences(cd_text, scan_text):
    """Exact Unicode offsets in the two displayed excerpts; never an automatic patch."""
    return [dict(operation=tag, cd_range=[a, b], scan_range=[c, d],
                 cd_text=cd_text[a:b], scan_text=scan_text[c:d])
            for tag, a, b, c, d in SequenceMatcher(None, cd_text, scan_text, autojunk=False).get_opcodes()
            if tag != 'equal']


def review(recipe, root):
    inputs = recipe['inputs']
    source_bytes = {name: checked(root, record) for name, record in inputs.items()}
    package = check_export(root / inputs['scan_package']['path'].rsplit('/', 1)[0])
    if package != json.loads(source_bytes['scan_package']):
        raise ValueError('Scan package differs from pinned input')
    if package['availability'] != 'readable' or package['verification']['status'] == 'unreviewed':
        raise ValueError('Comparison requires a successful reviewed scan sample')
    cd = json.loads(source_bytes['cd_reference'])
    text = source_bytes['cd_text'].decode('utf-8')
    paragraphs = json.loads(source_bytes['cd_paragraphs'])
    paras = {p['id']: p for p in paragraphs}
    if len(paras) != len(paragraphs):
        raise ValueError('Duplicate CD paragraph identity')
    cursor = 0
    for p in paragraphs:
        if p['character_offset'] != cursor or p['characters'] < 1:
            raise ValueError('CD paragraph offsets do not partition its text')
        cursor += p['characters']
    if cursor != len(text):
        raise ValueError('CD paragraph offsets do not cover its text')
    pages = set(recipe['pdf_pages'])
    if not 1 <= len(pages) <= 2 or len(pages) != len(recipe['pdf_pages']):
        raise ValueError('Comparison must select one or two distinct mapped pages')
    page_numbers = {p['pdf_index']: p['pdf_page'] for p in package['pages']}
    if not pages <= set(page_numbers.values()):
        raise ValueError('Comparison page is not mapped')
    regions = {r['id']: r for r in package['regions'] if page_numbers[r['pdf_index']] in pages}
    blocks = {b['id']: b for b in package['blocks']}
    eligible = {b['id'] for b in blocks.values() if set(b['region_ids']) <= regions.keys()}

    def cd_span(span):
        p = paras[span['paragraph_id']]
        start, end = span['range']
        if type(start) is not int or type(end) is not int or not 0 <= start < end <= p['characters']:
            raise ValueError('CD span exceeds paragraph bounds')
        offset = p['character_offset']
        return dict(**span, article_range=[offset + start, offset + end], text=text[offset + start:offset + end])

    association = recipe['association']
    if cd['issue_id'] != package['issue_id'] or cd['reference'] != association['cd_reference']:
        raise ValueError('CD identity/issue does not match reviewed association')
    label = cd_span(association['issue_page']['cd_span'])
    if label['text'] != association['issue_page']['observed_cd_label']:
        raise ValueError('Issue/page label differs from reviewed evidence')
    first = next(p for p in package['pages'] if p['pdf_page'] == association['issue_page']['pdf_page'])
    if first['pdf_page'] not in pages or first['printed_page'] != association['issue_page']['printed_page']:
        raise ValueError('Issue/page evidence differs from selected scan page')
    kinds = set()
    for anchor in association['anchors']:
        block = blocks[anchor['scan_block']]
        span = cd_span(anchor['cd_span'])
        value = anchor['shared_text']
        if block['id'] not in eligible or value not in block['text'] or value not in span['text']:
            raise ValueError('Association anchor is not present in both selected sources')
        if anchor['kind'] == 'body' and len(value) < 60:
            raise ValueError('Body association needs substantial shared text')
        if anchor['kind'] == 'byline' and (block['kind'] != 'byline' or len(value) < 2):
            raise ValueError('Byline association needs an observed author')
        kinds.add(anchor['kind'])
    if not {'byline', 'body'} <= kinds:
        raise ValueError('Title alone cannot establish association; require byline and body evidence')

    units, seen = [], set()
    for item in recipe['units']:
        id = item['scan_block']
        if id in seen or id not in eligible:
            raise ValueError('Duplicate or out-of-scope comparison block')
        seen.add(id)
        if not item['review_note'].strip() or not item['classification'].strip():
            raise ValueError('Comparison needs a recorded review decision')
        block = blocks[id]
        spans = [cd_span(span) for span in item['cd_spans']]
        cd_text = ''.join(span['text'] for span in spans)
        for finding in item.get('findings', []):
            if (not finding['cd_excerpt'] or finding['cd_excerpt'] not in cd_text
                    or not finding['scan_excerpt'] or finding['scan_excerpt'] not in block['text']
                    or not set(finding['scan_region_ids']) <= set(block['region_ids'])
                    or not finding['scan_region_ids']):
                raise ValueError('Reviewed finding must point to both excerpts and scan regions')
        units.append(dict(item, scan_text=block['text'], scan_range=[0, len(block['text'])],
                          scan_region_ids=block['region_ids'], correction_evidence=block['correction_evidence'],
                          cd_spans=spans, cd_text=cd_text, differences=differences(cd_text, block['text']),
                          decision='retain_scan_reading; preserve CD separately; no automatic edits'))
    if seen != eligible:
        raise ValueError('Every complete block within selected pages needs a disposition')
    figures = [f for f in package['figures'] if set(f['region_ids']) <= regions.keys()]
    if {f['id'] for f in figures} != {f['scan_figure'] for f in recipe['figure_reviews']}:
        raise ValueError('Selected figures need explicit comparison dispositions')
    for figure in recipe['figure_reviews']:
        expected = next(f for f in figures if f['id'] == figure['scan_figure'])
        if figure['scan_region_ids'] != expected['region_ids'] or not figure['review_note'].strip():
            raise ValueError('Figure review must identify its scan regions')
    result = dict(schema_version=1, scan_article_id=package['id'], toc_entry_id=package['toc_entry_id'],
                  cd_reference=cd['reference'], issue_id=package['issue_id'], inputs=inputs,
                  relationship=dict(type='reviewed-correspondence', verification='sample-reviewed',
                                    whole_cd_article_verified=False, pdf_pages=sorted(pages),
                                    evidence=association),
                  offset_convention='Zero-based, end-exclusive Unicode character offsets; CD unit text concatenates exact spans without normalization.',
                  units=units, figure_reviews=recipe['figure_reviews'],
                  excluded_blocks=[b['id'] for b in blocks.values() if b['id'] not in eligible],
                  limits=recipe['limits'])
    return result, package, regions


def check_comparison(output):
    output = Path(output)
    manifest = json.loads((output / 'manifest.json').read_bytes())
    names = [p['path'] for p in manifest['files']]
    actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
    if len(names) != len(set(names)) or actual != set(names) | {'manifest.json'}:
        raise ValueError('Comparison file inventory differs from manifest')
    for record in manifest['files']:
        checked(output, record)
    return json.loads((output / 'comparison.json').read_bytes())


def build(recipe_path, output, root=ROOT):
    root, recipe_path, output = Path(root).resolve(), Path(recipe_path).resolve(), Path(output).resolve()
    if not any(output.is_relative_to(root / name) for name in ('build', 'private')):
        raise ValueError('Comparison export must remain under build/ or private/')
    if output.exists():
        raise ValueError('Comparison export already exists; use a fresh output')
    recipe = json.loads(recipe_path.read_bytes())
    recipe_pin = pin(recipe_path.parent, recipe_path.name)
    result, package, regions = review(recipe, root)
    source = (root / recipe['inputs']['scan_package']['path']).parent
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as temporary:
        stage = Path(temporary) / 'comparison'
        stage.mkdir()
        for name, record in recipe['inputs'].items():
            copy_pin(root, stage, record, 'inputs/' + name + Path(record['path']).suffix)
        copy_pin(recipe_path.parent, stage, recipe_pin, 'inputs/recipe.json')
        for name in ('map.json', 'runtime.json'):
            copy_pin(source, stage, pin(source, name), 'scan/' + name)
        for record in package['corrections']:
            copy_pin(source, stage, record, 'scan/' + record['path'])
        for row in package['region_assets']:
            if row['region_id'] in regions:
                copy_pin(source, stage, row['asset'], 'scan/' + row['asset']['path'])
        for row in package['raw_ocr']:
            if set(row['region_ids']) <= regions.keys():
                for key in ('text', 'positions', 'settings'):
                    record = row[key]
                    copy_pin(source, stage, record, 'scan/' + record['path'])
        for record in recipe.get('cd_assets', []):
            copy_pin(root, stage, record, 'cd/' + Path(record['path']).name)
        result['recipe'] = recipe_pin
        result['scan_assets'] = [dict(region_id=r['region_id'], path='scan/' + r['asset']['path'])
                                 for r in package['region_assets'] if r['region_id'] in regions]
        write_json(stage / 'comparison.json', result)
        lines = ['# Reviewed scan/CD comparison', '',
                 f"{result['scan_article_id']} ↔ CD1 {result['cd_reference']}", '',
                 'Sample-reviewed correspondence; the complete CD article is not verified.', '',
                 'Exact offsets and edit operations: [comparison.json](comparison.json).', '',
                 'Unchanged [CD text](inputs/cd_text.txt), [paragraph index](inputs/cd_paragraphs.json), '
                 '[CD reference](inputs/cd_reference.json), [scan corrections](scan/corrections.json).', '',
                 '## Limits', '', *['- ' + note for note in result['limits']], '']
        assets = {r['region_id']: r['path'] for r in result['scan_assets']}
        for unit in result['units']:
            lines.extend([f"## {unit['scan_block']}", '', unit['classification'], '', unit['review_note'], '',
                          ' · '.join(f'[{id}]({assets[id]})' for id in unit['scan_region_ids']), '',
                          'CD excerpt (exact spans, no normalization):', '', '```text', unit['cd_text'], '```', '',
                          'Scan-supported reading:', '', '```text', unit['scan_text'], '```', ''])
        for figure in result['figure_reviews']:
            lines.extend([f"## Figure: {figure['scan_figure']}", '', figure['review_note'], ''])
        (stage / 'comparison.md').write_text('\n'.join(lines), encoding='utf-8')
        # Check the inputs again before publishing; no original package is modified.
        for record in recipe['inputs'].values():
            checked(root, record)
        checked(recipe_path.parent, recipe_pin)
        check_export(source)
        write_json(stage / 'manifest.json', dict(files=[pin(stage, p.relative_to(stage).as_posix())
                   for p in sorted(stage.rglob('*')) if p.is_file()]))
        check_comparison(stage)
        stage.rename(output)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        result = check_comparison(args.output)
    else:
        if args.recipe is None:
            parser.error('--recipe is required for a build')
        result = build(args.recipe, args.output)
    print(f"Compared {len(result['units'])} blocks: {result['scan_article_id']} ↔ {result['cd_reference']} (sample only)")


if __name__ == '__main__':
    main()
