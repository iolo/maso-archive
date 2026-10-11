"""Guard against misleading metric pooling and counting cache copies as work."""
import json
from pathlib import Path
import tempfile
import unittest

from tools.ocr_qwen.consolidate import pooled, unique_responses, usage
from tools.ocr_qwen.consolidate_july import paired_times, window_totals


def row(errors, chars):
    return {'engines': {e: {'cer': errors/chars, 'cer_edits': errors,
                            'cer_reference_chars': chars,
                            'cer_no_whitespace': errors/chars,
                            'cer_no_whitespace_edits': errors,
                            'cer_no_whitespace_reference_chars': chars}
                        for e in ('qwen', 'tesseract')}}


class ConsolidationTests(unittest.TestCase):
    def test_missing_timer_excludes_both_sides(self):
        rows = [dict(batch='01', region_id='a', qwen_seconds=10, tesseract_seconds=2),
                dict(batch='02', region_id='b', qwen_seconds=100, tesseract_seconds=None)]
        result = paired_times(rows)
        self.assertEqual(result['crops'], 1)
        self.assertEqual(result['qwen_to_tesseract_time_ratio'], 5)
        self.assertEqual(result['omitted'], [dict(batch='02', region_id='b')])

    def test_unobserved_window_retained_as_unknown(self):
        result = window_totals([dict(id='empty', elapsed_seconds=3, observed_responses=0, tokens=None)])
        self.assertEqual(result['elapsed_seconds'], 3)
        self.assertEqual(result['windows_without_observed_usage'], ['empty'])

    def test_pool_weights_characters_not_crop_percentages(self):
        result = pooled([row(1, 1), row(0, 99)])
        self.assertEqual(result['engines']['qwen']['cer']['rate'], .01)
        self.assertEqual(result['compact_crop_outcomes'], {'tie': 2})

    def test_mismatched_reference_denominators_fail(self):
        r = row(1, 10)
        r['engines']['tesseract']['cer_reference_chars'] = 11
        with self.assertRaises(AssertionError):
            pooled([r])

    def test_empty_cohort_is_unknown_not_perfect(self):
        self.assertIsNone(pooled([])['engines']['qwen']['cer']['rate'])

    def test_cache_copy_excluded_but_true_retry_counted(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for n, id in enumerate(['first', 'first', 'retry']):
                p = Path(tmp)/f'{n}.json'
                p.write_text(json.dumps({'id': id, 'usage': {'prompt_tokens': 10, 'completion_tokens': 2, 'total_tokens': 12}, 'text': 'identical content'}))
                paths.append(p)
            unique, duplicates = unique_responses(paths)
            self.assertEqual(duplicates, 1)
            self.assertEqual(len(unique), 2)
            self.assertEqual(usage([r for _, r in unique.values()])['total_tokens'], 24)
            paths[-1].write_text(json.dumps({'id': 'first', 'text': 'conflict'}))
            with self.assertRaisesRegex(ValueError, 'Conflicting completion'):
                unique_responses(paths)

    def test_usage_totals_must_reconcile(self):
        with self.assertRaises(AssertionError):
            usage([{'usage': {'prompt_tokens': 1, 'completion_tokens': 2, 'total_tokens': 10}}])


if __name__ == '__main__':
    unittest.main()
