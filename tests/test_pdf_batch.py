"""Synthetic interruption, failure isolation, invalidation and review preservation."""
from copy import deepcopy
import json
import multiprocessing
import os
from pathlib import Path
import signal
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

from tools.pdf_restore import batch
from tools.pdf_restore.inventory import pin, write_json
import test_pdf_build as build_fixtures


class PDFBatchTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.recipe = build_fixtures.PDFBuildTests().fixture(self.root)
        self.runtime = self.root / 'private/pdf-restoration/ocr-runtime'
        self.state = self.root / 'private/batch'
        self.cache = self.root / 'private/cache'
        self.request = self.root / 'private/request.json'
        self.data = {'batch_id': 'synthetic', 'limits': batch.MAX_LIMITS, 'lookup_pages': [],
                     'articles': [{'map': pin(self.root, 'private/pilot/map.json'),
                                   'recipe': pin(self.root, 'private/pilot/recipe.json')}]}
        self.environment = {'engine': 'synthetic-1', 'model': 'synthetic-hash'}
        self.patcher = patch.object(batch, 'toolchain', side_effect=lambda runtime: deepcopy(self.environment))
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.calls = []

    def prepare(self, state=None):
        write_json(self.request, self.data)
        return batch.prepare(self.request, state or self.state, self.cache, self.root, self.runtime)

    def worker(self, task, stage, scratch, root, runtime):
        self.calls.append(task['id'])
        Image.new('RGB', (20, 20), 'blue').save(stage / 'region.png')
        if task['dependency']['region']['kind'] != 'figure':
            text = ('changed OCR\n' if task['dependency']['config']['psm'] == 7 else 'raw OCR remains unchanged\n')
            (stage / 'result.txt').write_text(text)
            (stage / 'result.tsv').write_text('positions\n')
            (stage / 'result.stderr.txt').write_text('')
        write_json(stage / 'settings.json', {'crop_pixels': [0, 0, 20, 20], 'render_size': [100, 100]})
        write_json(stage / 'timing.json', {'render_crop_seconds': .1, 'ocr_seconds': .2})

    def test_interrupt_resume_and_cache_publication_crash_do_not_repeat_success(self):
        plan = self.prepare()
        def interrupt(task, *args):
            if task == plan['tasks'][1]:
                raise KeyboardInterrupt
            self.worker(task, *args)
        with patch.object(batch, 'process_region', side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt):
                batch.resume(self.state, self.root)
        ledger = json.loads((self.state / 'ledger.json').read_bytes())
        self.assertEqual([r['status'] for r in ledger['tasks'].values()], ['complete', 'interrupted', 'pending'])
        with patch.object(batch, 'process_region', side_effect=self.worker):
            self.assertEqual(batch.resume(self.state, self.root)['counts'], {'complete': 3})
        self.assertEqual(self.calls, [t['id'] for t in plan['tasks']])
        # Simulate a crash between atomic cache publication and ledger completion.
        ledger = json.loads((self.state / 'ledger.json').read_bytes())
        ledger['tasks'][plan['tasks'][0]['id']]['status'] = 'running'
        batch.atomic_json(self.state / 'ledger.json', ledger)
        with patch.object(batch, 'process_region', side_effect=AssertionError('must reuse cache')):
            self.assertEqual(batch.resume(self.state, self.root)['counts'], {'complete': 3})

    def test_failure_isolated_and_retry_is_explicit_bounded_and_durable(self):
        plan = self.prepare()
        failed = plan['tasks'][0]['id']
        def fail(task, *args):
            if task['id'] == failed:
                raise RuntimeError('Synthetic isolated failure')
            self.worker(task, *args)
        with patch.object(batch, 'process_region', side_effect=fail):
            result = batch.resume(self.state, self.root)
            self.assertEqual(result['counts'], {'failed': 1, 'complete': 2})
            self.assertEqual(batch.resume(self.state, self.root)['attempts'], 3)
            with self.assertRaisesRegex(ValueError, 'reason'):
                batch.resume(self.state, self.root, retry=[failed])
            result = batch.resume(self.state, self.root, retry=[failed], reason='one targeted fixture retry')
            self.assertEqual(result['failures'], 2)
            with self.assertRaisesRegex(ValueError, 'further recovery'):
                batch.resume(self.state, self.root, retry=[failed], reason='over budget')
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(len(list((self.state / 'failures').glob('*/failure.json'))), 2)
        outcome = batch.export(self.state, self.root / 'build/partial', self.root)
        self.assertFalse(outcome[0]['ocr_complete'])
        self.assertTrue(outcome[0]['review_required'])
        self.assertIsNone(outcome[0]['reviewed_export'])
        self.assertEqual(batch.check_export(self.root / 'build/partial')['summary']['counts'], result['counts'])

    def test_successful_retry_only_runs_failed_region(self):
        plan = self.prepare()
        failed = plan['tasks'][0]['id']
        def fail(task, *args):
            if task['id'] == failed:
                raise OSError('synthetic transient failure')
            self.worker(task, *args)
        with patch.object(batch, 'process_region', side_effect=fail):
            batch.resume(self.state, self.root)
        self.calls.clear()
        with patch.object(batch, 'process_region', side_effect=self.worker):
            result = batch.resume(self.state, self.root, retry=[failed], reason='fixture fault removed')
        self.assertEqual(self.calls, [failed])
        self.assertEqual(result['counts'], {'complete': 3})

    def test_killed_process_leaves_durable_running_row_and_resumes(self):
        plan = self.prepare()
        context = multiprocessing.get_context('fork')
        started = context.Event()
        def pause(task, stage, *args):
            (stage / 'result.txt').write_text('incomplete bytes must not be cached')
            started.set()
            context.Event().wait(10)
        def child():
            with patch.object(batch, 'process_region', side_effect=pause):
                batch.resume(self.state, self.root)
        process = context.Process(target=child)
        process.start()
        try:
            self.assertTrue(started.wait(5))
            os.kill(process.pid, signal.SIGKILL)
            process.join(5)
            self.assertFalse(process.is_alive())
        finally:
            if process.is_alive():
                process.kill()
                process.join(5)
        ledger = json.loads((self.state / 'ledger.json').read_bytes())
        self.assertEqual(ledger['tasks'][plan['tasks'][0]['id']]['status'], 'running')
        with patch.object(batch, 'process_region', side_effect=self.worker):
            self.assertEqual(batch.resume(self.state, self.root)['counts'], {'complete': 3})
        ledger = json.loads((self.state / 'ledger.json').read_bytes())
        self.assertEqual(ledger['tasks'][plan['tasks'][0]['id']]['interruptions'], 1)
        self.assertEqual(ledger['tasks'][plan['tasks'][0]['id']]['failures'], 0)

    def test_config_map_and_toolchain_keys_invalidate_only_dependencies(self):
        plan = self.prepare()
        with patch.object(batch, 'process_region', side_effect=self.worker):
            batch.resume(self.state, self.root)
        self.data['articles'][0]['region_config'] = {'r1': {'psm': 7}}
        changed = self.prepare(self.root / 'private/config-change')
        self.assertNotEqual(plan['tasks'][0]['key'], changed['tasks'][0]['key'])
        self.assertEqual([t['key'] for t in plan['tasks'][1:]], [t['key'] for t in changed['tasks'][1:]])
        self.calls.clear()
        with patch.object(batch, 'process_region', side_effect=self.worker):
            result = batch.resume(self.root / 'private/config-change', self.root)
        self.assertEqual(result['attempts'], 1)
        self.assertEqual(self.calls, [plan['tasks'][0]['id']])
        outcome = batch.export(self.root / 'private/config-change', self.root / 'build/changed', self.root)
        self.assertTrue(outcome[0]['review_required'])
        self.assertIsNone(outcome[0]['reviewed_export'])
        self.data['articles'][0].pop('region_config')
        self.data['articles'][0].pop('recipe')
        package = json.loads((self.root / 'private/pilot/map.json').read_bytes())
        package['regions'][0]['bbox'][0] = .01
        write_json(self.root / 'private/revised-map.json', package)
        self.data['articles'][0]['map'] = pin(self.root, 'private/revised-map.json')
        mapped = self.prepare(self.root / 'private/map-change')
        self.assertNotEqual(plan['tasks'][0]['key'], mapped['tasks'][0]['key'])
        self.assertEqual([t['key'] for t in plan['tasks'][1:]], [t['key'] for t in mapped['tasks'][1:]])
        self.calls.clear()
        with patch.object(batch, 'process_region', side_effect=self.worker):
            self.assertEqual(batch.resume(self.root / 'private/map-change', self.root)['attempts'], 1)
        self.assertEqual(self.calls, [plan['tasks'][0]['id']])
        self.environment['model'] = 'new-model-hash'
        with self.assertRaisesRegex(ValueError, 'tools changed'):
            batch.resume(self.state, self.root)
        new_runtime = self.prepare(self.root / 'private/model-change')
        self.assertTrue(all(a['key'] != b['key'] for a, b in zip(mapped['tasks'], new_runtime['tasks'])))

    def test_page_ceiling_and_source_changes(self):
        plan = self.prepare()
        self.data['articles'][0].pop('recipe')
        package = json.loads((self.root / 'private/pilot/map.json').read_bytes())
        (self.root / 'source.pdf').write_bytes(b'changed synthetic source')
        package['source'].update(pin(self.root, 'source.pdf'))
        write_json(self.root / 'private/new-map.json', package)
        self.data['articles'][0]['map'] = pin(self.root, 'private/new-map.json')
        inventory_path = self.root / 'private/pdf-restoration/inventory/sources.json'
        inventory = json.loads(inventory_path.read_bytes())
        inventory['sources'][0].update(package['source'])
        write_json(inventory_path, inventory)
        changed = self.prepare(self.root / 'private/source-change')
        self.assertTrue(all(a['key'] != b['key'] for a, b in zip(plan['tasks'], changed['tasks'])))
        second = {**package['pages'][0], 'pdf_index': 1, 'pdf_page': 2}
        package['pages'].append(second)
        inventory['sources'][0]['pages'].append(second)
        write_json(inventory_path, inventory)
        write_json(self.root / 'private/new-map.json', package)
        self.data['articles'][0]['map'] = pin(self.root, 'private/new-map.json')
        self.data['limits'] = {**batch.MAX_LIMITS, 'source_pages': 1}
        with self.assertRaisesRegex(ValueError, 'Distinct source page ceiling'):
            self.prepare(self.root / 'private/too-many-pages')

    def test_reviewed_export_is_identical_and_originals_are_preserved(self):
        originals = {p: p.read_bytes() for p in self.recipe.parent.rglob('*') if p.is_file()}
        self.prepare()
        with patch.object(batch, 'process_region', side_effect=self.worker):
            result = batch.resume(self.state, self.root, max_tasks=1)
            self.assertEqual(result['counts'], {'complete': 1, 'pending': 2})
            batch.resume(self.state, self.root)
        one, two = self.root / 'build/export', self.root / 'build/repeat'
        outcomes = batch.export(self.state, one, self.root)
        self.assertFalse(outcomes[0]['review_required'])
        self.assertIsNotNone(outcomes[0]['reviewed_export'])
        batch.export(self.state, two, self.root)
        files = lambda d: {p.relative_to(d): p.read_bytes() for p in d.rglob('*') if p.is_file()}
        self.assertEqual(files(one), files(two))
        self.assertEqual(originals, {p: p.read_bytes() for p in originals})
        self.assertFalse(any(p.name == 'page.png' for p in one.rglob('*')))
        (one / outcomes[0]['id'] / 'map.json').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'hash/size'):
            batch.check_export(one)

    def test_limits_identity_input_pins_and_cache_corruption_fail_closed(self):
        self.data['articles'] *= 4
        with self.assertRaisesRegex(ValueError, 'Article ceiling'):
            self.prepare()
        self.data['articles'] = self.data['articles'][:2]
        with self.assertRaisesRegex(ValueError, 'Duplicate article'):
            self.prepare()
        self.data['articles'] = self.data['articles'][:1]
        self.data['lookup_pages'] = list(range(21))
        with self.assertRaisesRegex(ValueError, 'Lookup page'):
            self.prepare()
        self.data['lookup_pages'] = []
        plan = self.prepare()
        with batch.locked(self.state), self.assertRaisesRegex(ValueError, 'holds this lock'):
            batch.resume(self.state, self.root)
        with patch.object(batch, 'process_region', side_effect=self.worker):
            batch.resume(self.state, self.root)
        cached = self.cache / plan['tasks'][0]['key'] / 'result.txt'
        cached.write_text('corrupt')
        with self.assertRaisesRegex(ValueError, 'hash/size'):
            batch.resume(self.state, self.root)
        correction = self.recipe.parent / 'corrections.json'
        correction.write_text('changed correction')
        with self.assertRaisesRegex(ValueError, 'Input hash/size'):
            batch.report(self.state, self.root)

    def test_real_worker_masks_exclusions_and_reuses_page_render(self):
        plan = self.prepare()
        scratch, output = self.root / 'private/scratch', self.root / 'private/worker'
        scratch.mkdir()
        output.mkdir()
        def render(args, **kwargs):
            image = Image.new('RGB', (100, 101), 'blue')
            image.paste('red', (0, 60, 100, 101))
            image.save(args[-1] + '.png')
        def engine(image, destination, config, runtime):
            with Image.open(image) as crop:
                self.assertNotIn((255, 0, 0), [c for _, c in crop.getcolors(crop.width * crop.height)])
            self.assertEqual(config['psm'], 6)
            return .1
        with patch.object(batch.subprocess, 'run', side_effect=render) as renderer, \
             patch.object(batch, 'run_region', side_effect=engine):
            batch.process_region(plan['tasks'][0], output, scratch, self.root, self.runtime)
            batch.process_region(plan['tasks'][2], output, scratch, self.root, self.runtime)
        self.assertEqual(renderer.call_count, 1)


if __name__ == '__main__':
    unittest.main()
