"""Private extensions must be checked before any adapter code is executed."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools.reading_room import volunteer


class VolunteerAdaptersTest(unittest.TestCase):
    def test_missing_or_modified_adapter_stops_before_execution(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(volunteer, 'run_path') as run:
            root = Path(temp)
            for name, _ in volunteer.ADAPTERS:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('raise AssertionError("must never execute")')
            with self.assertRaisesRegex(ValueError, 'Missing or changed'):
                volunteer.install_adapters(root)
            run.assert_not_called()

    def test_all_pins_checked_before_install_and_closeout_order_retained(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name, _ in volunteer.ADAPTERS:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('fixture')
            calls = []
            def digest(path):
                calls.append(('check', path.relative_to(root).as_posix()))
                return dict(volunteer.ADAPTERS)[path.relative_to(root).as_posix()]
            def run(path):
                return {'install': lambda: calls.append(('install', Path(path).relative_to(root).as_posix()))}
            with patch.object(volunteer, 'digest', side_effect=digest), patch.object(volunteer, 'run_path', side_effect=run):
                volunteer.install_adapters(root)
            self.assertEqual(calls, [('check', p) for p, _ in volunteer.ADAPTERS] + [('install', p) for p, _ in volunteer.ADAPTERS])


if __name__ == '__main__':
    unittest.main()
