"""Sample-driven RTF preservation and generic semantic rules."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from tools import inventory_cd1_rtf as inventory, recover_cd1_text as recovery
from tools.cd1_batch_core import inherited_states, map_blocks
from tools.render_cd1_markdown import render
from tools.validate_cd1_batch import check_topic, run_bytes, RECORD
from tools.run_cd1_batch import ROOT
from tools.decode_cd1_paragraph import digest
from maso_archive.reading_room_package import load_package, checked_file


def recover(raw, reference='9209394a'):
    report = inventory.inspect_topic(raw, 0, 4)
    assert not report['issues'], report['issues']
    report.update(ordinal=1, role='reference_target_body')
    topic = recovery.recover_topic(raw, report, font_codecs={4: 'cp949', 5: 'cp949', 15: 'cp949'})
    return {'schema_version': 1, 'cd_reference': reference, 'topics': [topic]}


class SampleRulesTests(unittest.TestCase):
    def test_first_indent_tab_stops_double_underline_and_resets(self):
        raw = b'\\f4\\fi120\\tx425\\tx850\\uldb A\\tab B\\par\\pard\\plain C\\par '
        topic = recover(raw)['topics'][0]
        first, second = topic['paragraphs']
        self.assertEqual(first['format'], {'fi': 120, 'tab_stops': [425, 850]})
        self.assertTrue(first['runs'][0]['format']['ul'])
        self.assertEqual(first['runs'][0]['format']['underline_style'], 'double')
        self.assertEqual(second['format'], {})
        self.assertNotIn('underline_style', second['runs'][0]['format'])
        check_topic(raw, topic, {'byte_offset': 0, 'byte_length': len(raw), 'sha256': digest(raw)})

    def test_plain_underline_overrides_double_style(self):
        raw = b'\\f4\\uldb A\\ul B\\ul0 C\\par '
        runs = recover(raw)['topics'][0]['paragraphs'][0]['runs']
        self.assertEqual([r['format'].get('underline_style') for r in runs], ['double', 'single', 'none'])

    def test_new_control_inheritance_keeps_paragraph_values(self):
        prefix = b'{\\rtf1\\fi-200\\tx400\\uldb\\page\n'
        state = inherited_states(prefix + b'body}', [len(prefix)])[len(prefix)]
        self.assertEqual(state['unknown'], [])
        self.assertEqual(state['paragraph'], {'fi': -200, 'tab_stops': [400]})
        self.assertEqual(state['character']['underline_style'], 'double')

    def test_fixed_pitch_runs_keep_tabs_internal_blanks_and_unknown_semantics(self):
        raw = b'\\f15 begin\\par   x\\tab := 1;\\par\\par end;\\par\\f4 prose\\par '
        article = recover(raw)
        mapping = map_blocks(article)
        self.assertEqual([b['kind'] for b in mapping['blocks']], ['code', 'unresolved'])
        self.assertEqual(len(mapping['blocks'][0]['members']), 4)
        self.assertIn('semantic_review_pending', mapping['blocks'][0]['decision']['review_concerns'])
        preview, _ = render(article, mapping)
        self.assertIn(b'begin\n  x\t:= 1;\n\nend;\n', preview['body.md'])
        self.assertIn(b'interpretation awaits review', preview['body.md'])

    def test_heading_pattern_does_not_invent_missing_parent_levels(self):
        article = recover(b'\\f4\\b\\fs20\\li215 1. Orphan second level\\par\\fs24 I. Top level\\par\\fs20 2. Child\\par ')
        mapping = map_blocks(article)
        self.assertEqual([b['kind'] for b in mapping['blocks']], ['unresolved', 'heading', 'heading'])
        self.assertEqual([b.get('heading_level') for b in mapping['blocks']], [None, 1, 2])

    def test_source_byte_audit_rejects_changes_and_ledger_gaps(self):
        raw = b"\\f5 \\'b0\\'a1\\f4\\tab end\\par "
        topic = recover(raw)['topics'][0]
        check_topic(raw, topic, {'byte_offset': 0, 'byte_length': len(raw), 'sha256': digest(raw)})
        changed = deepcopy(topic['paragraphs'][0]['runs'][0])
        changed['text'] = 'changed'
        with self.assertRaisesRegex(ValueError, 'Decoded run'):
            run_bytes(raw, changed)
        changed_topic = deepcopy(topic)
        changed_topic['accounting'][1]['byte_offset'] += 1
        with self.assertRaisesRegex(ValueError, 'gap or overlap'):
            check_topic(raw, changed_topic, {'byte_offset': 0, 'byte_length': len(raw), 'sha256': digest(raw)})


@unittest.skipUnless(RECORD.exists(), 'Private frozen-sample validation has not run')
class SampleArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(RECORD.read_bytes())
        cls.root = ROOT / cls.record['output_root']
        if not (cls.root / 'validation-report.json').exists():
            raise unittest.SkipTest('Private sample artifacts unavailable')

    def test_frozen_population_source_audit_and_preserved_identities(self):
        record = self.record
        self.assertEqual(record['scope'], {'february_baseline': 6, 'additional_candidates': 9, 'issues': 10})
        self.assertTrue(record['validation']['deterministic_all_stage_outputs'])
        self.assertGreater(record['validation']['nested_http']['files_fetched_and_checked'], 100)
        articles = record['source_checks']['articles']
        unindexed = next(a for a in articles if a['source_reference'] == '1KP6JK')
        self.assertEqual(unindexed['article_id'], 'cd1:article:native-0e6aae95')
        supplement = next(a for a in articles if a['source_reference'] == '9311000')
        bundle, _, _ = load_package(self.root / supplement['package'] / 'content')
        self.assertIsNone(bundle['articles'][0]['pages']['start'])
        self.assertEqual(sum(len(a['auxiliary_topics']) for a in articles), 3)

    def test_every_issue_and_media_disposition_still_validates(self):
        for issue, row in self.record['issue_packages'].items():
            bundle, _, counts = load_package(self.root / row['package'] / 'content')
            self.assertEqual(counts, row['counts'])
            self.assertEqual(bundle['issues'][0]['id'], issue)
        for resource, row in self.record['source_checks']['conversions'].items():
            raw = checked_file(self.root, {'path': row['diagnostic_path'], 'sha256': row['diagnostic_sha256']})
            diagnostic = json.loads(raw)
            if row['status'] == 'deferred':
                self.assertTrue(diagnostic.get('policy') or diagnostic.get('concerns') or diagnostic.get('error'))
