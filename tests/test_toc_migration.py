"""Owner corrections must preserve identity and cannot bypass historical pins."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from maso_archive.toc import run_import
from tools.reading_room.export import digest, read
from tools.toc_migration import load_migration, migrate_links


class TocMigrationTests(unittest.TestCase):
    def fixture(self, root):
        def write(path, value):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
        def pin(path):
            return dict(path=path.relative_to(root).as_posix(), bytes=path.stat().st_size, sha256=digest(path))
        source, ids, toc = root / 'TOC.md', root / 'data/identities/toc.json', root / 'build/toc'
        source.write_text('## 88.01\n- Category: Old title = 10\n- News\n  - Local\n  - Abroad\n')
        run_import(source, toc, ids, start='1988-01', end='1988-01')
        old = read(toc / 'manifest.json')
        cache = root / 'work/cache/toc-snapshots' / old['source']['sha256']
        (cache / 'build').mkdir(parents=True)
        shutil.copytree(toc, cache / 'build/toc')
        (cache / 'data/identities').mkdir(parents=True)
        shutil.copyfile(ids, cache / 'data/identities/toc.json')
        shutil.copyfile(source, cache / 'TOC.md')
        files = [dict(path=p.relative_to(cache).as_posix(), bytes=p.stat().st_size, sha256=digest(p)) for p in cache.rglob('*') if p.is_file()]
        descriptor = root / 'data/catalog/toc-snapshots/old.json'
        write(descriptor, dict(source_sha256=old['source']['sha256'], import_manifest=old, files=files))
        source.write_text('## 88.01\n- Category\n  - New title = 10\n- News\n  - Local; Abroad\n')
        decisions = root / 'data/overrides/review.json'
        write(decisions, dict(source_sha256=digest(source), assignments={'3': 'maso-1988-01-toc-0001'},
                              removed_ids=['maso-1988-01-toc-0003', 'maso-1988-01-toc-0004'], new_lines=[]))
        run_import(source, toc, ids, decisions_path=decisions, start='1988-01', end='1988-01')
        new = read(toc / 'manifest.json')
        record = dict(schema_version=1, kind='reviewed-toc-migration', previous_snapshot=pin(descriptor), decisions=pin(decisions),
                      before=dict(source=old['source'], outputs=old['outputs']),
                      after=dict(source=new['source'], outputs=new['outputs'], identities_sha256=new['identities_sha256']),
                      counts=dict(previous_entries=4, current_entries=4, preserved_ids=2, new_ids=2, retired_ids=2),
                      retired=[dict(id='maso-1988-01-toc-'+n, before=t, successor='maso-1988-01-toc-0006', after='Local; Abroad')
                               for n,t in [('0003','Local'), ('0004','Abroad')]])
        path = root / 'data/catalog/toc-migrations' / (digest(source) + '.json')
        write(path, record)
        reference = dict(issues_sha256=old['outputs']['issues.json']['sha256'], toc_sha256=old['outputs']['toc-entries.jsonl']['sha256'])
        return toc, path, reference

    def test_replays_corrections_and_carries_only_explicit_links(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            toc, path, reference = self.fixture(root)
            before = {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
            record, receipt = load_migration(toc, reference, root)
            self.assertEqual(receipt['counts']['preserved_ids'], 2)
            original = {'maso-1988-01-toc-0001':['body'], 'maso-1988-01-toc-0003':['news'], 'maso-1988-01-toc-0004':['news','other']}
            projected = migrate_links(original, record)
            self.assertEqual(projected, {'maso-1988-01-toc-0001':['body'], 'maso-1988-01-toc-0006':['news','other']})
            self.assertNotIn('maso-1988-01-toc-0005', projected)  # New category has no invented body.
            self.assertEqual(before, {p: p.read_bytes() for p in before})
            self.assertEqual(original['maso-1988-01-toc-0004'], ['news','other'])

    def test_rejects_stale_history_decisions_catalog_and_successors(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            toc, path, reference = self.fixture(root)
            original = read(path)
            for mutate in [lambda r:r['before']['outputs']['toc-entries.jsonl'].update(sha256='0'*64),
                           lambda r:r['after']['outputs'].pop('toc-entries.jsonl'),
                           lambda r:r['retired'][0].update(successor='unknown'),
                           lambda r:r['retired'].pop(),
                           lambda r:r['counts'].update(preserved_ids=9),
                           lambda r:r['decisions'].update(sha256='0'*64)]:
                record = deepcopy(original);mutate(record);path.write_text(json.dumps(record))
                with self.assertRaises(ValueError):
                    load_migration(toc, reference, root)
            path.write_text(json.dumps(original))
            (toc / 'toc-entries.jsonl').write_text('tampered\n')
            with self.assertRaisesRegex(ValueError, 'input differs'):
                load_migration(toc, reference, root)

    def test_repository_migration_retains_completed_scan_identities(self):
        from tools.toc_snapshot import ROOT
        root = ROOT
        old = read(root / 'data/catalog/toc-imports/1993-12.json')['manifest']
        # Do not require private article or reader exports.
        reference = dict(issues_sha256=old['outputs']['issues.json']['sha256'], toc_sha256=old['outputs']['toc-entries.jsonl']['sha256'])
        # The real reviewed metadata reproduces from tracked source/history.
        with TemporaryDirectory() as tmp:
            stage = Path(tmp)
            for name in ['TOC.md', 'data/identities/toc.json']:
                dest=stage/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/name,dest)
            for directory in ['data/catalog/toc-migrations','data/catalog/toc-snapshots','data/overrides']:
                shutil.copytree(root/directory,stage/directory)
            source_sha = old['source']['sha256']
            from tools.toc_snapshot import Snapshot
            snapshot=Snapshot(root,'data/catalog/toc-snapshots/'+source_sha+'.json')
            snapshot.restore()
            shutil.copytree(snapshot.directory,stage/'work/cache/toc-snapshots'/source_sha)
            run_import(stage/'TOC.md',stage/'build/toc',stage/'data/identities/toc.json')
            record, _ = load_migration(stage/'build/toc',reference,stage)
            old_entries=snapshot.artifact('toc-entries.jsonl')
            new_entries=[json.loads(l) for l in (stage/'build/toc/toc-entries.jsonl').read_text().splitlines()]
            for issue in ['maso-1983-11','maso-1984-02']:
                strip=lambda rows:[{k:v for k,v in e.items() if k!='source'} for e in rows if e['issue_id']==issue]
                self.assertEqual(strip(old_entries),strip(new_entries))
            self.assertEqual(record['counts'],dict(previous_entries=5497,current_entries=5299,preserved_ids=5032,new_ids=267,retired_ids=465))


if __name__ == '__main__':
    unittest.main()
