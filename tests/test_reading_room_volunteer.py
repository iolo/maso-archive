"""Private extensions must be checked before any adapter code is executed."""
import tempfile
import unittest
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from tools.reading_room import volunteer


class VolunteerAdaptersTest(unittest.TestCase):
    def test_changed_february_dispatcher_is_not_executed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            relative, _ = volunteer.FEBRUARY_DISPATCHER
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_text('raise AssertionError("must never execute")')
            with patch.object(volunteer.importlib.util, 'spec_from_file_location') as spec:
                with self.assertRaisesRegex(ValueError, 'Missing or changed February'):
                    volunteer.load_february_dispatcher(root)
                spec.assert_not_called()

    def test_private_formats_route_without_displacing_existing_formats(self):
        from tools.pdf_restore import assemble, design_literal_assembly
        private = SimpleNamespace(project=lambda recipe, segments: 'private', validate_recipe=lambda recipe: 'private validation')
        dispatcher = SimpleNamespace(MODULES={'private-v1': private})
        common_project = lambda recipe, segments: 'existing'
        common_validate = lambda recipe: 'existing validation'
        with patch.object(volunteer, 'load_february_dispatcher', return_value=dispatcher), \
                patch.object(volunteer, 'install_adapters'), \
                patch.object(design_literal_assembly, 'installed', return_value=nullcontext()), \
                patch.object(assemble, 'project', common_project), \
                patch.object(assemble, 'validate_recipe', common_validate):
            with self.assertRaisesRegex(RuntimeError, 'operation failed'):
                with volunteer.installed_adapters():
                    self.assertEqual(assemble.project({'index_mode': 'private-v1'}, []), 'private')
                    self.assertEqual(assemble.validate_recipe({'index_mode': 'private-v1'}), 'private validation')
                    self.assertEqual(assemble.project({'index_mode': 'existing'}, []), 'existing')
                    self.assertEqual(assemble.validate_recipe({'index_mode': 'existing'}), 'existing validation')
                    raise RuntimeError('operation failed')
            self.assertIs(assemble.project, common_project)
            self.assertIs(assemble.validate_recipe, common_validate)

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
