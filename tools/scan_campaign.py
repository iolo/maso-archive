"""Prepare donated issue recipes and record explicitly supplied visual reviews."""

import argparse
import csv
import json
from pathlib import Path
import re
from zipfile import ZipFile

from PIL import Image, ImageDraw, ImageOps

from tools.scan_cleanup import ROOT, digest, local_path, save, verify


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def prepare(issue):
    if not re.fullmatch(r'\d{4}-\d{2}', issue):
        raise ValueError('Expected YYYY-MM')
    paths = sorted((ROOT / 'maso-img').glob(f'*_{issue.replace("-", "_")}*.zip'))
    if not paths:
        raise ValueError(f'No donated ZIPs for {issue}')
    names, signatures, folders, numbers = set(), set(), set(), set()
    for path in paths:
        with ZipFile(path) as zipped:
            for entry in zipped.infolist():
                p = Path(entry.filename)
                if entry.is_dir() or p.name.startswith('._') or p.suffix.lower() != '.jpg':
                    continue
                base = re.sub(r'(?:\(\d+\))+(?=\.jpg$)', '', p.name)
                names.add(base)
                signatures.add((entry.CRC, entry.file_size))
                folders.add(p.parent.as_posix())
                match = re.fullmatch(r'Page(\d+)\.jpg', base)
                if match:
                    numbers.add(int(match[1]))
    if len(folders) != 1:
        raise ValueError('Expected a single source issue folder')
    special = {
        'AFront001.jpg': dict(path='covers/front.jpg', role='front-cover', position=0),
        'AFront002.jpg': dict(path='covers/inside-front.jpg', role='inside-front-cover', position=1),
        'Rear001.jpg': dict(path='covers/inside-back.jpg', role='inside-back-cover', position=10000),
        'Rear002.jpg': dict(path='covers/back.jpg', role='back-cover', position=10001),
    }
    if 'AFront000.jpg' in names:
        special['AFront000.jpg'] = dict(path='extras/spine.jpg', role='spine', position=None)
    if 'AFront003.jpg' in names:
        special.update({
            'AFront001.jpg': dict(path='extras/spine.jpg', role='spine', position=None),
            'AFront002.jpg': dict(path='covers/front.jpg', role='front-cover', position=0),
            'AFront003.jpg': dict(path='covers/inside-front.jpg', role='inside-front-cover', position=1),
        })
    for name in sorted(names):
        match = re.fullmatch(r'Page(\d+)_(jiro|postcard)_([A-D])\.jpg', name)
        if match:
            anchor, kind, side = match.groups()
            role = 'payment-slip' if kind == 'jiro' or side in 'CD' else 'subscription-postcard'
            special[name] = dict(path=f'extras/{name.lower()}', role=role,
                                 position=int(anchor) + 2 + (ord(side) - ord('A') + 1) / 10,
                                 sourceFilenameAnchor=int(anchor))
        if re.fullmatch(r'Page\d+_cut\.jpg', name):
            special[name] = dict(path=f'extras/{name.lower()}', role='damaged-alternative',
                                 position=None, sourceFilenameAnchor=int(name[4:7]))
    first, last = min(numbers), max(numbers)
    recipe = dict(schemaVersion=1, issue=issue, sourceFolder=folders.pop(),
                  archives=[p.relative_to(ROOT).as_posix() for p in paths],
                  output=f'archive/scans/{issue}', expectedUniqueImages=len(signatures),
                  expectedFilenameRange=[first, last],
                  expectedFilenameGaps=sorted(set(range(first, last + 1)) - numbers),
                  specialImages=special,
                  reviewStatus='Candidate roles and source order; visual review required before closeout.')
    destination = ROOT / f'metadata/catalog/scans/{issue}-recipe.json'
    save(destination, recipe)
    print(json.dumps(recipe, ensure_ascii=False, indent=2))


def assets(issue):
    root = local_path(f'archive/scans/{issue}')
    manifest = read(root / 'manifest.json')
    folder = root / 'review'
    folder.mkdir(exist_ok=True)
    sheets = manifest['contactSheets']
    atlas = Image.new('RGB', (2100, 1275 * ((len(sheets) + 2) // 3)), '#dddddd')
    for index, row in enumerate(sheets):
        with Image.open(root / row['path']) as image:
            image = image.resize((700, 1275))
            atlas.paste(image, ((index % 3) * 700, (index // 3) * 1275))
    final_group = ((len(sheets) - 1) // 3) * 3
    final_height = max(((len(row['images']) + 4) // 5) * 425 for row in sheets[final_group:])
    atlas = atlas.crop((0, 0, 2100, (final_group // 3) * 1275 + (final_height + 1) // 2))
    atlas.save(folder / 'overview.jpg', quality=94)
    # Include source-numbered pages spread through the issue, and gap boundaries.
    available = {r['sourceFilenameNumber']: r for r in manifest['images']
                 if r['sourceFilenameNumber'] is not None}
    sample = {n for n in (15, 16, 30, 60, 90, 120, 150, 180, 210, 240, 245, 246)
              if n in available}
    for gap in manifest['summary']['filenameGaps']:
        for n in (gap - 1, gap + 1):
            if n in available:
                sample.add(n)
    sample = sorted(sample)
    atlas = Image.new('RGB', (1400, 190 * ((len(sample) + 1) // 2)), '#eeeeee')
    crops = []
    for index, number in enumerate(sample):
        row = available[number]
        with Image.open(root / row['path']) as image:
            width, height = image.size
            boxes = [(0, height - 550, 1300, height),
                     (width - 1300, height - 550, width, height)]
            x, y = (index % 2) * 700, (index // 2) * 190
            ImageDraw.Draw(atlas).text((x + 5, y + 3), row['path'], fill='black')
            for side, box in enumerate(boxes):
                thumb = ImageOps.contain(image.crop(box), (340, 160))
                atlas.paste(thumb, (x + side * 350, y + 25))
            crops.append(dict(path=row['path'], number=number, boxes=boxes, sha256=row['sha256']))
    atlas.save(folder / 'pagination-samples.jpg', quality=94)
    save(folder / 'pagination-crops.json', crops)
    print('Pagination sample candidates:', sample)
    for note in manifest['notes']:
        data = (root / note['path']).read_bytes()
        for encoding in ('utf-8-sig', 'cp949', 'utf-16'):
            try:
                text = data.decode(encoding)
                break
            except UnicodeError:
                continue
        else:
            text = repr(data)
        print('DONOR NOTE', note['path'], repr(text))


def finish(issue, decision_path):
    root = local_path(f'archive/scans/{issue}')
    manifest = read(root / 'manifest.json')
    decisions = read(decision_path)
    if not decisions.get('overviewReviewed') or not decisions.get('coversReviewed'):
        raise ValueError('Explicit visual overview and cover review required')
    images = {row['path']: row for row in manifest['images']}
    samples = []
    candidates = {row['number']: row for row in read(root / 'review/pagination-crops.json')}
    for number in decisions['confirmedPrintedNumbers']:
        candidate = candidates[number]
        samples.append(dict(path=candidate['path'], printedPage=number,
                            sha256=candidate['sha256'], evidence='review/pagination-samples.jpg'))
    overrides = []
    for path, role in decisions.get('roleOverrides', {}).items():
        overrides.append(dict(path=path, role=role, sha256=images[path]['sha256']))
    review = dict(schemaVersion=1, issue=issue, reviewedOn='2026-11-14',
                  status='overview-reviewed-pagination-sampled', reviewer='assistant visual review',
                  manifestSha256=digest(root / 'manifest.json'),
                  coverage=dict(contactSheetAtlasViewed='review/overview.jpg',
                                contactSheetsIncluded=[row['path'] for row in manifest['contactSheets']],
                                imagesShown=len(images), printedPageSamples=len(samples),
                                fullResolutionPageByPageReview=False),
                  printedPageSamples=samples, roleOverrides=overrides,
                  findings=decisions['findings'], donorNoteSummary=decisions.get('donorNoteSummary'),
                  limitations=['Full pagination and physical collation remain unverified.',
                               'Insert placement follows source order unless an explicit finding says otherwise.'])
    save(root / 'review.json', review)
    numbers = {row['path']: row['printedPage'] for row in samples}
    roles = {row['path']: row['role'] for row in overrides}
    ordered = sorted(images.values(), key=lambda row: (
        row['readingOrder'] is None, row['readingOrder'] or 0, row['path']))
    with (root / 'page-list.csv').open('x', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(['reading_order', 'source_filename_number', 'source_filename_anchor',
                         'verified_printed_page', 'role', 'working_file', 'width', 'height',
                         'bytes', 'sha256', 'source_entries'])
        for row in ordered:
            writer.writerow([row['readingOrder'], row['sourceFilenameNumber'],
                             row.get('sourceFilenameAnchor'), numbers.get(row['path']),
                             roles.get(row['path'], row['role']), row['path'], *row['dimensions'],
                             row['bytes'], row['sha256'], len(row['originals'])])
    with (root / 'page-list.csv').open(newline='', encoding='utf-8') as stream:
        exported = list(csv.DictReader(stream))
    if len(exported) != len(images) or {r['working_file'] for r in exported} != set(images):
        raise ValueError('Page list does not account for every retained image')
    for row in exported:
        original = images[row['working_file']]
        if (row['sha256'] != original['sha256']
                or row['reading_order'] != str(original['readingOrder'] or '')
                or row['verified_printed_page'] != str(numbers.get(original['path'], ''))
                or row['role'] != roles.get(original['path'], original['role'])):
            raise ValueError('Page list differs from extraction or review mappings')
    print('Re-reading all source entries and checking working files.', flush=True)
    verification = verify(root)
    verification.update(pageListRows=len(ordered), reviewMappingsChecked=True)
    save(root / 'review/verification.json', verification)
    summary = manifest['summary']
    gaps = ', '.join(map(str, summary['filenameGaps'])) or 'none within the observed range'
    findings = '\n'.join(f'- {finding}' for finding in decisions['findings'])
    note_summary = decisions.get('donorNoteSummary') or 'No donor text note was present.'
    report = f'''# {issue} donated scan cleanup

Completed 2026-11-14. Original ZIPs remain unchanged. Working JPEG masters retain
their original bytes; only previews are resized.

| Item | Count |
| --- | ---: |
| Original ZIPs | {len(manifest['sources'])} |
| Source file entries checked | {summary['entries']} |
| JPEG entries | {summary['imageEntries']} |
| Duplicate JPEG copies omitted | {summary['duplicateImages']} |
| AppleDouble sidecars omitted | {summary['sidecars']} |
| Donor text files retained | {summary['notes']} |
| Distinct JPEG masters | {summary['uniqueImages']} |
| Images in proposed reading order | {summary['orderedImages']} |
| Extras outside reading order | {summary['extras']} |
| Contact sheets | {summary['contactSheets']} |
| Enlarged printed-number samples checked | {len(samples)} |

Working masters occupy {summary['imageBytes']:,} bytes ({summary['imageBytes'] / 2**30:.2f} GiB).
Source filename range: {summary['filenameRange'][0]}–{summary['filenameRange'][1]}.
Filename gaps: **{gaps}**. These do not establish the contents or reason for an
absent span; a continuous filename range does not prove completeness.

## Visual findings

The overview atlas includes all {summary['uniqueImages']} retained scans across
{summary['contactSheets']} contact sheets. Covers and selected boundaries/inserts
were inspected separately where described below. Full pagination and physical
collation remain unverified.

{findings}

Donor note summary: {note_summary}
Original note bytes and filenames are retained under the issue's `notes/` when present.
Printed numbers confirmed in enlarged margin crops: {', '.join(str(r['printedPage']) for r in samples) or 'none'}.
Other printed-number fields remain unset.

## Files and verification

- [Working-set README](../archive/scans/{issue}/README.md)
- [Page list](../archive/scans/{issue}/page-list.csv)
- [Overview](../archive/scans/{issue}/review/overview.jpg)
- [Visual review](../archive/scans/{issue}/review.json)
- [Extraction manifest](../archive/scans/{issue}/manifest.json)
- [Fresh verification](../archive/scans/{issue}/review/verification.json)
- [Recipe](../metadata/catalog/scans/{issue}-recipe.json)
- [Result record](../metadata/catalog/scans/{issue}-result.json)

All source entries were re-read and matched with their recorded hashes, working
image and contact-sheet hashes checked, and original ZIP hashes confirmed unchanged.
Every retained JPEG fully decoded during extraction. Extraction refuses an existing
destination. The generated manifest's initial review status is supplemented by
the separate `review.json` and page list.

```sh
python3 -m tools.scan_cleanup --verify archive/scans/{issue}
```

See [progress](../PROGRESS-SCANS.md) and the [plan](../PLAN-SCANS.md).
'''
    report_path = ROOT / f'docs/SCAN-ISSUE-{issue}.md'
    with report_path.open('x', encoding='utf-8') as stream:
        stream.write(report)
    with (root / 'README.md').open('x', encoding='utf-8') as stream:
        stream.write(f'''# {issue} clean scan working set

Start with `review/overview.jpg` or the larger `contact-sheets/sheet-01.jpg` and
subsequent sheets. `page-list.csv` contains proposed order and reviewed roles;
blank printed-page fields are unverified. JPEG masters are byte-preserved.

There are {summary['uniqueImages']} distinct scans, {summary['orderedImages']} proposed reading-order entries,
and {summary['extras']} extras outside that sequence. Filename gaps: {gaps}.

{findings}

Donor note summary: {note_summary}

`manifest.json` preserves extraction mappings and source hashes. `review.json`
supplements it with visual findings. `review/verification.json` records the fresh
source-to-output check. Full pagination and physical collation remain unverified.

Project report: `docs/SCAN-ISSUE-{issue}.md` from the repository root.
Verify again with `python3 -m tools.scan_cleanup --verify archive/scans/{issue}`.
''')
    artifact_paths = [report_path, ROOT / f'metadata/catalog/scans/{issue}-recipe.json',
                      Path(__file__), ROOT / 'tools/scan_cleanup.py',
                      *[p for p in sorted(root.rglob('*')) if p.is_file() and
                        (p.suffix != '.jpg' or p.parent.name == 'review')]]
    artifacts = [dict(path=p.relative_to(ROOT).as_posix(), bytes=p.stat().st_size,
                      sha256=digest(p)) for p in artifact_paths]
    result = dict(schemaVersion=1, issue=issue, completedOn='2026-11-14',
                  status='cleanup-checked-with-recorded-uncertainties',
                  output=root.relative_to(ROOT).as_posix(), summary=summary,
                  sourceArchives=manifest['sources'], validation=verification,
                  visualReview=dict(overviewViewed=True, printedPageSamplesChecked=len(samples),
                                    fullPaginationVerified=False, findings=decisions['findings']),
                  artifacts=artifacts)
    save(ROOT / f'metadata/catalog/scans/{issue}-result.json', result)
    update_progress()
    print(json.dumps(dict(issue=issue, result='passed', **summary), indent=2))


def update_progress():
    """Rebuild the status index only from completed, verified result records."""
    issues = set()
    for path in (ROOT / 'maso-img').glob('*.zip'):
        match = re.search(r'_(\d{4})_(\d{2})', path.name)
        if match:
            issues.add(f'{match[1]}-{match[2]}')
    records = {record['issue']: record for record in
               (read(p) for p in (ROOT / 'metadata/catalog/scans').glob('*-result.json'))}
    completed = set(records) & issues
    pending = sorted(issues - completed)
    totals = {key: sum(records[issue]['summary'][key] for issue in completed)
              for key in ('uniqueImages', 'duplicateImages', 'sidecars', 'entries', 'imageBytes')}
    table = []
    for issue in sorted(issues):
        if issue not in completed:
            table.append(f'| {issue} | Awaiting cleanup | — | — |')
            continue
        record = records[issue]
        report = f'docs/SCAN-PILOT-{issue}.md' if issue == '1984-04' else f'docs/SCAN-ISSUE-{issue}.md'
        gaps = ', '.join(map(str, record['summary']['filenameGaps'])) or 'None in observed range'
        table.append(f'| [{issue}]({report}) | Checked | {record["summary"]["uniqueImages"]} | {gaps} |')
    next_issue = '1984-03' if '1984-03' in pending else (pending[0] if pending else None)
    next_text = (f'Next: **{next_issue}**. Continue one issue at a time, record the visual findings,\n'
                 'update this index, and commit that issue before closing out the next.'
                 if next_issue else
                 'All donated issues have checked cleanup results. The collection-wide completion\n'
                 'audit is the remaining gate before marking the campaign complete.')
    text = f'''# Donated scan cleanup progress

Updated 2026-11-14. Follow the [plan](PLAN-SCANS.md); linked issue reports preserve
the findings and remaining uncertainties. Original donation ZIPs stay unchanged.

## Current status

**{len(completed)} of {len(issues)} donated issues have checked working sets; {len(pending)} remain.**
The donation contains 59 ZIPs. Checked issues account for {totals['entries']:,}
source file entries, {totals['uniqueImages']:,} distinct JPEG masters,
{totals['duplicateImages']:,} duplicate JPEG copies omitted, and {totals['sidecars']:,}
confirmed AppleDouble sidecars omitted from the working sets.
Retained masters occupy {totals['imageBytes'] / 2**30:.2f} GiB.

| Issue/report | Status | Distinct scans | Filename gaps |
| --- | --- | ---: | --- |
{chr(10).join(table)}

Filename gaps are distinct from verified missing printed pages. Complete
filename numbering does not establish completeness. The first observed range
for December 1983 begins at 3; no missing 1–2 claim follows from that alone.

## What checked means

Each completed issue has a byte-preserved working collection, original ZIP/member
mappings, SHA-256 duplicate grouping, fully decoded retained JPEGs, contact sheets,
a page list, visual findings, and a fresh source-to-output verification. The four
cover faces, spines, inserts and differing alternatives are retained. Known order
uncertainties and donor-note inconsistencies stay explicit.

April 1984 was the first pilot: 257 scans, nine contact sheets and twelve enlarged
printed-number samples, with a filename gap at 13–14. Later issue overviews include
all retained images in an atlas, with separate cover/boundary views where needed.
These are cleanup reviews, not full proofreading, physical collation, or complete
printed-pagination checks. Unverified printed numbers remain blank.

The [April report](docs/SCAN-PILOT-1984-04.md) and per-issue reports above link the
private working files. Recipes and small result records live in
`metadata/catalog/scans/`; masters and evidence are Git-ignored under
`archive/scans/YYYY-MM/`. Result artifact hashes describe the files captured at
that issue's checkpoint; later shared-tool/document changes do not rewrite those
historical fingerprints. Issue source and master hashes remain pinned separately.

## Next

{next_text}

Recheck any extracted issue from the repository root:

```sh
python3 -m tools.scan_cleanup --verify archive/scans/YYYY-MM
```

March 1984's late-page order, June 1987's torn-page note despite present scans,
and July 1987's damaged alternatives require the issue-specific findings; do not
silently infer repair or absence from those names. OCR restoration and reading-room
integration remain separate work.
'''
    (ROOT / 'PROGRESS-SCANS.md').write_text(text, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--prepare', metavar='ISSUE')
    action.add_argument('--assets', metavar='ISSUE')
    action.add_argument('--finish', metavar='ISSUE')
    parser.add_argument('--decisions')
    args = parser.parse_args()
    if args.prepare:
        prepare(args.prepare)
    elif args.assets:
        assets(args.assets)
    elif args.decisions:
        finish(args.finish, local_path(args.decisions))
    else:
        parser.error('--finish requires --decisions')


if __name__ == '__main__':
    main()
