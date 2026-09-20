"""Disc-wide source accounting, conservative matches, and safe queue consumption."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tools import inventory_cd1_processing as inventory


class InventoryPolicyTests(unittest.TestCase):
    def test_blank_detection_does_not_discard_text_or_objects(self):
        for raw in (b'\\pard \\b\\cf1 ', b'\\pard\\tqc\\tx8995 \n\\par '):
            self.assertTrue(inventory.screening(raw)['blank_formatting_only'])
        for raw in (b'\\pard hello\\par ', b"\\pard \\'b0\\'a1", b'\\pard \\{bmc example.dib\\}', b'\\pict '):
            self.assertFalse(inventory.screening(raw)['blank_formatting_only'])
        hints = inventory.screening(b'\\f15\\tab \\{bmc example.dib\\} \\{bmc example.wmf\\}')
        self.assertEqual(hints['font_ids'], [15])
        self.assertEqual(hints['media_extensions'], {'.dib': 1, '.wmf': 1})
        self.assertEqual(hints['tab_controls'], 1)

    def test_opening_page_is_explicit_and_not_inferred_from_reference(self):
        label = inventory.opening_page(b'\\pard 93.2  402p\n\\par text', 100)
        self.assertEqual((label['issue'], label['page'], label['byte_offset']), ('1993-02', 402, 106))
        self.assertEqual(inventory.opening_page(b'\\pard 93.11. supplement\\par ', 0)['status'], 'missing')
        self.assertEqual(inventory.opening_page(b'\\pard title\\par later 88.2. 30p', 0)['status'], 'missing')
        self.assertEqual(inventory.opening_page(b'88.2. 30p 88.2. 65p\\par ', 0)['status'], 'ambiguous')

    def test_context_offsets_must_stay_inside_the_native_interval(self):
        self.assertEqual(inventory.context_relation(100, 100, 200), 'at_native_header')
        self.assertEqual(inventory.context_relation(101, 100, 200), 'inside_native_topic_interval')
        for offset in (99, 200, 201):
            self.assertEqual(inventory.context_relation(offset, 100, 200), 'unresolved_outside_native_interval')
        self.assertEqual(inventory.context_relation(101, 100, None), 'unresolved_outside_native_interval')

    def test_toc_matching_requires_exact_title_issue_and_observed_page(self):
        job = {'issue_id': 'maso-1990-01', 'title': 'Exact title', 'index_titles': [],
               'opening_page': {'page': 12, 'issue': '1990-01'}, 'source_reference': '9001012'}
        entry = {'id': 'toc-1', 'issue_id': job['issue_id'], 'kind_candidate': 'article',
                 'title_candidate': 'Exact title', 'start_page_candidate': 12}
        self.assertEqual(inventory.toc_relation(job, [entry])['matched_ids'], ['toc-1'])
        for field, value in [('start_page_candidate', 13), ('title_candidate', 'Exact title!'), ('issue_id', 'maso-1990-02')]:
            changed = {**entry, field: value}
            self.assertEqual(inventory.toc_relation(job, [changed])['matched_ids'], [])
        self.assertEqual(inventory.toc_relation(job, [entry, {**entry, 'id': 'toc-2'}])['matched_ids'], [])
        job['opening_page']['page'] = None
        self.assertEqual(inventory.toc_relation(job, [entry])['matched_ids'], [])  # No suffix fallback.


@unittest.skipUnless((inventory.ROOT / 'private/cd1-probe/raw/MASOCD.rtf').exists() and
                     (inventory.february.OUTPUT / 'content/manifest.json').exists(), 'Private CD1 inventory inputs unavailable')
class ProcessingInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record, cls.files = inventory.build_inventory()
        cls.data = {key: [json.loads(line) for line in cls.files[name].splitlines()] if name.endswith('.jsonl')
                    else json.loads(cls.files[name]) for name, key in inventory.OUTPUT_NAMES.items()}

    def test_reproducible_record_and_complete_source_populations(self):
        self.assertEqual(self.record, json.loads(inventory.RECORD.read_bytes()))
        counts = self.record['counts']
        self.assertEqual((counts['native_topics'], counts['native_contexts'], counts['index_entries'],
                          counts['index_references'], counts['index_occurrences']), (3099, 2103, 3032, 1080, 2462))
        self.assertEqual(sum(counts['topic_roles'].values()), 3099)
        self.assertEqual(counts['job_states'], {'already_prepared': 6, 'blocked': 8, 'ready': 1074})
        self.assertEqual(counts['issues'], 72)
        self.assertEqual(self.record['scope'], 'metadata_only')
        self.assertEqual(set(self.files), set(inventory.OUTPUT_NAMES) | {'manifest.json', 'validation-sample.json'})

    def test_unindexed_and_suffixed_identities_are_not_lost_or_invented(self):
        jobs = self.data['jobs']
        unindexed = [j for j in jobs if not j['index_references']]
        self.assertEqual(len(unindexed), 9)
        keyboard = next(j for j in unindexed if j['body_topic_id'] == 'cd1:topic:0155')
        self.assertEqual(keyboard['candidate_article_id'], 'cd1:article:8802162')
        self.assertEqual(keyboard['state'], 'already_prepared')
        self.assertEqual(keyboard['occurrence_ids'], [])
        self.assertTrue(all(j['identity_basis'] == 'native_context_alias' and ':native-' in j['candidate_article_id']
                            for j in unindexed if j is not keyboard))
        suffixed = [r for r in self.data['references'] if r['reference_kind'] == 'suffixed']
        self.assertEqual(len(suffixed), 41)
        self.assertTrue(all(r['job_id'] for r in suffixed))
        menu = next(r for r in self.data['references'] if r['reference'] == 'mscdmenu')
        self.assertEqual(menu['target_status'], 'navigation_topic')
        self.assertIsNone(menu['job_id'])
        supplement = next(j for j in jobs if j['source_reference'] == '9311000')
        self.assertIsNone(supplement['opening_page']['page'])

    def test_context_differences_are_supported_by_alias_and_native_interval(self):
        differences = self.record['context_offset_differences']
        self.assertEqual(len(differences), 31)
        dated = {j['body_topic_id'] for j in self.data['jobs']}
        self.assertEqual(sum(c['topic_id'] in dated for c in differences), 11)
        for context in differences:
            self.assertEqual(context['association'], 'inside_native_topic_interval')
            self.assertLess(context['native_header_topic_offset'], context['topic_offset'])
            self.assertLess(context['topic_offset'], context['next_header_topic_offset'])

    def test_unattributed_introductions_and_continuations_block_only_affected_jobs(self):
        unknown = {t['id'] for t in self.data['topics'] if t['role'] == 'unattributed_content'}
        self.assertEqual(unknown, {f'cd1:topic:{n:04d}' for n in (1437, 1453, 1733, 2133, 2367, 2436, 2703, 2749)})
        blocked = [j for j in self.data['jobs'] if j['state'] == 'blocked']
        self.assertEqual({b['topic_id'] for j in blocked for b in j['blockers']}, unknown)
        topics = {t['id']: t for t in self.data['topics']}
        for n in (1437, 2133, 2367):
            self.assertEqual(topics[f'cd1:topic:{n:04d}']['aliases'], [])
            self.assertFalse(topics[f'cd1:topic:{n:04d}']['features']['blank_formatting_only'])
        self.assertEqual(len(self.data['review_items']), 8)

    def test_six_prepared_articles_keep_original_identity_spans_and_toc_links(self):
        prepared = [j for j in self.data['jobs'] if j['state'] == 'already_prepared']
        self.assertEqual({j['source_reference'] for j in prepared}, {'8802030', '8802065', '8802114', '8802162', '8802180', '8802184'})
        for job in prepared:
            baseline = job['preparation']
            self.assertEqual(job['candidate_article_id'], baseline['article_id'])
            self.assertEqual(job['toc']['matched_ids'], baseline['toc_entry_ids'])
            self.assertEqual([t['rtf'] for t in job['source_topics']], baseline['rtf_spans'])
            self.assertEqual(baseline['print_verification']['status'], 'pending')
            self.assertEqual(baseline['extraction_status'], 'checked')
        feb = next(i for i in self.data['issues'] if i['issue_id'] == 'maso-1988-02')
        self.assertEqual(feb['counts']['states'], {'already_prepared': 6})
        self.assertEqual(feb['counts']['toc_status'], {'matched': 6, 'no_exact_title_match': 29, 'section': 4})

    def test_fixed_sample_spans_years_and_preservation_concerns(self):
        sample = json.loads(self.files['validation-sample.json'])
        self.assertEqual(len(sample), 9)
        self.assertEqual({s['issue_id'][5:9] for s in sample}, {str(y) for y in range(1988, 1994)})
        self.assertEqual([s['body_topic_id'] for s in sample], [inventory.topic_id(n) for n in inventory.SAMPLE_ORDINALS])
        self.assertTrue(any('unindexed_native_identity' in s['review_concerns'] for s in sample))
        self.assertTrue(any('context_is_inside_topic_not_header' in s['review_concerns'] for s in sample))
        self.assertTrue(any(95 in s['features']['font_ids'] for s in sample))
        self.assertTrue(any(s['source_reference'] == '9311000' for s in sample))
        self.assertTrue(all(s['selection_reason'] for s in sample))

    def test_duplicate_missing_or_falsely_ready_jobs_are_rejected(self):
        changed = deepcopy(self.data)
        changed['jobs'].pop()
        with self.assertRaisesRegex(ValueError, 'Article candidate coverage'):
            inventory.validate_inventory(changed)
        changed = deepcopy(self.data)
        changed['references'][0]['occurrence_ids'].pop()
        with self.assertRaisesRegex(ValueError, 'Index occurrence coverage'):
            inventory.validate_inventory(changed)
        changed = deepcopy(self.data)
        blocked = next(j for j in changed['jobs'] if j['state'] == 'blocked')
        blocked.update(state='ready', blockers=[])
        with self.assertRaisesRegex(ValueError, 'Adjacent content blocker lost'):
            inventory.validate_inventory(changed)
        changed = deepcopy(self.data)
        changed['contexts'].append(changed['contexts'][0])
        with self.assertRaisesRegex(ValueError, 'Duplicate context hash'):
            inventory.validate_inventory(changed)

    def test_relocated_queue_and_failed_staging_preserve_previous_inventory(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'nested' / 'inventory'
            inventory.write_inventory(output, self.files)
            data, manifest = inventory.load_inventory(output)
            self.assertEqual(data, self.data)
            self.assertEqual(manifest['counts'], self.record['counts'])
            before = (output / 'manifest.json').read_bytes()
            broken = dict(self.files)
            broken['jobs.jsonl'] = b'{}\n'
            with self.assertRaisesRegex(ValueError, 'Package bytes mismatch'):
                inventory.write_inventory(output, broken)
            self.assertEqual((output / 'manifest.json').read_bytes(), before)
            self.assertEqual(inventory.load_inventory(output)[0], self.data)
            (output / 'extra.json').write_bytes(b'{}')
            with self.assertRaisesRegex(ValueError, 'Unexpected inventory files'):
                inventory.load_inventory(output)


if __name__ == '__main__':
    unittest.main()
