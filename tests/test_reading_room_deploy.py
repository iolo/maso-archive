import base64
from contextlib import redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.reading_room import deploy_cloudflare as deploy


class FakeS3:
    def __init__(self):
        self.objects = {}
        self.puts = []
        self.fail = None

    def head_object(self, Bucket, Key):
        if Key not in self.objects:
            error = RuntimeError('not found')
            error.response = {'ResponseMetadata': {'HTTPStatusCode': 404}}
            raise error
        return self.objects[Key]

    def put_object(self, **kwargs):
        key = kwargs['Key']
        if key == self.fail:
            raise RuntimeError('upload interrupted')
        data = kwargs['Body'].read()
        self.puts.append(key)
        assert base64.b64encode(hashlib.md5(data, usedforsecurity=False).digest()).decode() == kwargs['ContentMD5']
        self.objects[key] = {**kwargs, 'ContentLength': len(data)}


class DeployTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / 'assets').mkdir()
        (self.root / 'data').mkdir()
        (self.root / 'assets/main.js').write_text('console.log("fixture")')
        (self.root / 'index.html').write_text('<script src="./assets/main.js"></script>')
        data = b'{"schemaVersion":3,"articles":[]}'
        (self.root / 'data/catalog.json').write_bytes(data)
        manifest = {'kind': 'reading-room-static', 'files': [{'path': 'catalog.json', 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}]}
        (self.root / 'data/manifest.json').write_text(json.dumps(manifest))

    def test_dry_run_has_no_network_or_secret_side_effects(self):
        with patch.object(deploy, 'cloudflare') as api, patch.object(deploy, 's3_client') as s3, patch.object(deploy, 'save_token') as save, redirect_stdout(io.StringIO()):
            deploy.main(['--output', str(self.root)])
        api.assert_not_called(); s3.assert_not_called(); save.assert_not_called()

    def test_only_export_files_are_selected_and_entry_points_are_last(self):
        (self.root / 'private-key').write_text('not for upload')
        (self.root / 'data/unlisted.pdf').write_text('not for upload')
        files = deploy.inventory(self.root)
        self.assertEqual([f.key for f in files], ['site/data/catalog.json', 'site/assets/main.js', 'site/data/manifest.json', 'site/index.html'])

    def test_bad_hash_absolute_base_and_symlink_are_rejected(self):
        (self.root / 'data/catalog.json').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'manifest mismatch'):
            deploy.inventory(self.root)
        (self.root / 'index.html').write_text('<script src="/archive/assets/main.js"></script>')
        with self.assertRaisesRegex(ValueError, 'relative paths'):
            deploy.inventory(self.root)
        (self.root / 'assets/link.js').symlink_to(self.root / 'assets/main.js')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            deploy.safe_file(self.root, 'assets/link.js')
        for path in ('../secret', '/secret', 'data/../secret', 'data//file', 'data/\\file'):
            with self.assertRaises(ValueError):
                deploy.safe_file(self.root, path)

    def test_upload_resumes_by_hash_and_corrects_wrong_mime(self):
        files = deploy.inventory(self.root)
        s3 = FakeS3()
        with redirect_stdout(io.StringIO()):
            deploy.upload_files(s3, 'bucket', files, 2)
        self.assertEqual(s3.puts[-2:], ['site/data/manifest.json', 'site/index.html'])
        s3.puts.clear()
        with redirect_stdout(io.StringIO()):
            deploy.upload_files(s3, 'bucket', files, 2)
        self.assertEqual(s3.puts, [])
        s3.objects[files[0].key]['ContentType'] = 'application/octet-stream'
        self.assertTrue(deploy.upload_one(s3, 'bucket', files[0]))

    def test_failed_upload_never_publishes_manifest_or_index(self):
        files = deploy.inventory(self.root)
        s3 = FakeS3(); s3.fail = files[0].key
        with self.assertRaises(RuntimeError), redirect_stdout(io.StringIO()):
            deploy.upload_files(s3, 'bucket', files, 2)
        self.assertNotIn('site/index.html', s3.puts)
        self.assertNotIn('site/data/manifest.json', s3.puts)

    def test_changed_local_file_stops_before_upload(self):
        file = deploy.inventory(self.root)[0]
        file.path.write_text('changed during deploy')
        s3 = FakeS3()
        with self.assertRaisesRegex(ValueError, 'Export changed'):
            deploy.upload_one(s3, 'bucket', file)
        self.assertEqual(s3.puts, [])

    def test_non_404_storage_error_is_not_treated_as_missing(self):
        with patch.object(FakeS3, 'head_object', side_effect=RuntimeError('403')):
            with self.assertRaises(RuntimeError):
                deploy.head(FakeS3(), 'bucket', 'key')

    def test_worker_payload_binds_existing_bucket_and_secret_without_public_vars(self):
        body, mime = deploy.worker_payload('test-bucket', 'a' * 43)
        self.assertIn(b'"bucket_name": "test-bucket"', body)
        self.assertIn(b'"type": "secret_text"', body)
        self.assertIn(b'"observability": {"enabled": false}', body)
        self.assertIn(b'name="worker.mjs"; filename="worker.mjs"', body)
        self.assertTrue(mime.startswith('multipart/form-data; boundary='))

    def test_secret_file_permissions_validation_and_reuse(self):
        path = self.root / 'private/share-token'
        with patch.object(deploy, 'TOKEN_FILE', path):
            self.assertIsNone(deploy.read_token())
            deploy.save_token('a' * 43, path)
            self.assertEqual(deploy.read_token(), 'a' * 43)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            path.chmod(0o644)
            with self.assertRaisesRegex(ValueError, 'chmod 600'):
                deploy.read_token()

    def test_missing_credentials_show_names_not_values(self):
        with patch.dict(os.environ, {'CLOUDFLARE_API_TOKEN': 'do-not-print-me'}, clear=True):
            with self.assertRaises(ValueError) as caught:
                deploy.credentials()
        self.assertIn('CLOUDFLARE_ACCOUNT_ID', str(caught.exception))
        self.assertNotIn('do-not-print-me', str(caught.exception))

    def test_apply_uploads_before_publishing_and_keeps_token_out_of_logs(self):
        calls = []
        client = FakeS3()
        client.head_bucket = lambda **kw: calls.append('head-bucket')
        path = self.root / 'private/share-token'
        def api(creds, method, suffix, *args):
            calls.append((method, suffix))
            if method == 'PUT':
                self.assertIn('site/index.html', client.objects)
                self.assertTrue(path.with_suffix('.pending').exists())
        output = io.StringIO()
        with patch.object(deploy, 'TOKEN_FILE', path), patch.object(deploy, 'credentials', return_value={}), patch.object(deploy, 's3_client', return_value=client), patch.object(deploy, 'cloudflare', side_effect=api), patch.object(deploy, 'verify_site') as verify, redirect_stdout(output):
            deploy.main(['--output', str(self.root), '--apply'])
            token = deploy.read_token()
            self.assertEqual(len(token), 43)
            self.assertNotIn(token, output.getvalue())
            self.assertFalse(path.with_suffix('.pending').exists())
            verify.assert_called_once()
            self.assertLess(calls.index(('GET', '/settings')), calls.index(('PUT', '')))
            deploy.main(['--output', str(self.root), '--apply', '--worker-only'])
            self.assertEqual(deploy.read_token(), token)
            deploy.main(['--output', str(self.root), '--apply', '--worker-only', '--rotate-link'])
            self.assertNotEqual(deploy.read_token(), token)

    def test_worker_failure_preserves_pending_token_and_blocks_silent_retry(self):
        client = FakeS3(); client.head_bucket = lambda **kw: None
        path = self.root / 'private/share-token'
        def api(creds, method, suffix, *args):
            if method == 'PUT':
                raise ValueError('connection failed')
        with patch.object(deploy, 'TOKEN_FILE', path), patch.object(deploy, 'credentials', return_value={}), patch.object(deploy, 's3_client', return_value=client), patch.object(deploy, 'cloudflare', side_effect=api), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'connection failed'):
                deploy.main(['--output', str(self.root), '--apply'])
            self.assertTrue(path.with_suffix('.pending').exists())
            self.assertFalse(path.exists())
            with self.assertRaisesRegex(ValueError, 'pending deployment token'):
                deploy.main(['--output', str(self.root), '--apply'])

    def test_worker_only_refuses_missing_remote_export(self):
        client = FakeS3(); client.head_bucket = lambda **kw: None
        with patch.object(deploy, 'TOKEN_FILE', self.root / 'private/share-token'), patch.object(deploy, 'credentials', return_value={}), patch.object(deploy, 's3_client', return_value=client), patch.object(deploy, 'cloudflare') as api, redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'matching export'):
                deploy.main(['--output', str(self.root), '--apply', '--worker-only'])
        api.assert_called_once_with({}, 'GET', '/settings')


if __name__ == '__main__':
    unittest.main()
