import json
from pathlib import Path
import tempfile
import unittest

from tools.pdf_restore.usage import audit, records, summarize


class UsageTests(unittest.TestCase):
    def test_duplicate_responses_and_non_usage_text_are_not_counted(self):
        row = dict(type='token_usage_record', timestamp='2026-10-10T00:00:01Z',
                   payload=dict(response_id='one', usage=dict(input_tokens=100)))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'log.jsonl'
            path.write_text('\n'.join(map(json.dumps, [row, row, dict(type='message', text='token_usage_record')]))+'\n')
            self.assertEqual(len(records(path)), 1)
            row['payload']['usage']['input_tokens'] = 101
            with path.open('a') as stream:
                stream.write(json.dumps(row)+'\n')
            with self.assertRaises(ValueError): records(path)

    def test_boundary_subsets_and_missing_records(self):
        windows = [dict(id=str(i), start=f'2026-10-10T00:00:0{i}Z',
                        end=f'2026-10-10T00:00:0{i+1}Z') for i in range(3)]
        usage = dict(input_tokens=100, cached_input_tokens=60, cache_write_input_tokens=10,
                     output_tokens=20, reasoning_output_tokens=5, total_tokens=120)
        result = summarize([dict(timestamp=windows[1]['start'], usage=usage)], windows)['windows']
        self.assertIsNone(result[0]['tokens'])
        self.assertIsNone(result[2]['tokens'])
        self.assertEqual(result[1]['tokens']['total_tokens'], 120)
        self.assertEqual(result[1]['tokens']['uncached_nonwrite_input_tokens'], 30)
        usage.pop('cache_write_input_tokens')
        result = summarize([dict(timestamp=windows[1]['start'], usage=usage)], windows)
        self.assertIsNone(result['windows'][1]['tokens']['uncached_nonwrite_input_tokens'])

    def test_overlapping_windows_and_invalid_counts_fail(self):
        w = dict(id='a', start='2026-10-10T00:00:00Z', end='2026-10-10T00:00:02Z')
        with self.assertRaises(ValueError): summarize([], [w, dict(w, id='b')])
        with self.assertRaises(ValueError):
            summarize([dict(timestamp=w['start'], usage=dict(input_tokens=1,output_tokens=2,total_tokens=5))], [w])

    def test_gap_usage_stays_visible_without_entering_an_engine_window(self):
        windows = [dict(id='first', start='2026-10-10T00:00:00Z', end='2026-10-10T00:00:01Z'),
                   dict(id='last', start='2026-10-10T00:00:02Z', end='2026-10-10T00:00:03Z')]
        rows = [dict(timestamp='2026-10-10T00:00:01.5Z', usage=dict(input_tokens=7))]
        result = audit(rows, windows)
        self.assertEqual(result['observed_trial_span']['tokens']['input_tokens'], 7)
        self.assertEqual(result['between_window_usage']['tokens']['input_tokens'], 7)
        self.assertTrue(all(w['tokens'] is None for w in result['windows']))


if __name__ == '__main__':
    unittest.main()
