"""Preservation and evidence gates for cover installation."""
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from tools.pdf_restore.covers import existing_covers, install
from tools.pdf_restore.inventory import pin, write_json


class PDFCoverTests(unittest.TestCase):
    def fixture(self, root):
        output = root / 'private/pdf-restoration/covers'
        output.mkdir(parents=True)
        (root / 'covers').mkdir()
        (root / 'covers/maso8311.png').write_bytes(b'owner-supplied untouched bytes')
        write_json(output / 'existing-before.json', existing_covers(root))
        sources, records, reviews = [], [], []
        for label in ('8311', '8402'):
            path = root / f'maso-{label}.pdf'
            path.write_bytes(b'synthetic source ' + label.encode())
            source = dict(id=f'pdf-{label}', filename_issue_label=label, **pin(root, path.name))
            sources.append(source)
            Image.new('RGB', (10, 20), 'blue').save(output / f'{label}.jpg')
            artifact = pin(output, f'{label}.jpg')
            records.append(dict(source_id=source['id'], candidate={'artifact': artifact}))
            reviews.append(dict(source_id=source['id'], status='verified-front-cover', visible_issue_label=label,
                                date_evidence='visible date', upright=True, proportions_checked=True,
                                reviewed_artifact=artifact))
        inventory = root / 'private/inventory.json'
        write_json(inventory, {'sources': sources})
        write_json(output / 'candidates.json', dict(inventory=pin(root, 'private/inventory.json'),
                                                   records=records, renderer_version='synthetic'))
        write_json(output / 'review.json', reviews)
        return output, reviews

    def test_preserves_existing_alternative_and_installs_missing_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output, _ = self.fixture(root)
            before = (root / 'covers/maso8311.png').read_bytes()
            install(root, output)
            self.assertEqual((root / 'covers/maso8311.png').read_bytes(), before)
            self.assertFalse((root / 'covers/maso8311.jpg').exists())
            self.assertEqual((root / 'covers/maso8402.jpg').read_bytes(), (output / '8402.jpg').read_bytes())
            ledger = json.loads((output / 'ledger.json').read_bytes())
            self.assertEqual(len(ledger['records']), 2)
            with self.assertRaisesRegex(ValueError, 'already installed'):
                install(root, output)

    def test_conflicting_date_prevents_any_installation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output, reviews = self.fixture(root)
            reviews[1]['visible_issue_label'] = '8403'
            write_json(output / 'review.json', reviews)
            with self.assertRaisesRegex(ValueError, 'gate failed'):
                install(root, output)
            self.assertFalse((root / 'covers/maso8402.jpg').exists())

    def test_changed_owner_bytes_and_changed_review_asset_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output, _ = self.fixture(root)
            owner = root / 'covers/maso8311.png'
            original = owner.read_bytes()
            owner.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'existing cover changed'):
                install(root, output)
            owner.write_bytes(original)
            (output / '8402.jpg').write_bytes(b'changed derivative')
            with self.assertRaisesRegex(ValueError, 'cover bytes changed'):
                install(root, output)
            self.assertFalse((root / 'covers/maso8402.jpg').exists())

    def test_uncertain_outcome_has_no_association_or_installed_image(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output, reviews = self.fixture(root)
            reviews[1] = {'source_id': reviews[1]['source_id'], 'status': 'uncertain'}
            write_json(output / 'review.json', reviews)
            install(root, output)
            ledger = json.loads((output / 'ledger.json').read_bytes())
            self.assertEqual(ledger['records'][1]['disposition'], 'deferred-no-association')
            self.assertIsNone(ledger['records'][1]['installed'])
            self.assertFalse((root / 'covers/maso8402.jpg').exists())


if __name__ == '__main__':
    unittest.main()
