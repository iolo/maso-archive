#!/usr/bin/env python3
"""Deploy the prepared static reader to R2 + an existing Worker. Dry-run by default."""
from __future__ import annotations

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import re
import secrets
import stat
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
NAME = 'maso-archive-reading-room-volunteer'
ORIGIN = f'https://{NAME}.iolo.workers.dev'
TOKEN_FILE = ROOT / 'private/reading-room-deploy/share-token'
WORKER_FILE = Path(__file__).with_name('cloudflare-worker.mjs')
CACHE = 'private, no-store'


@dataclass(frozen=True)
class File:
    path: Path
    key: str
    size: int
    sha256: str
    md5: str
    content_type: str
    signature: tuple


def signature(path):
    s = path.stat()
    return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)


def safe_file(root, relative):
    if not isinstance(relative, str) or '\\' in relative or any(ord(c) < 32 for c in relative):
        raise ValueError('Invalid export path')
    if any(p in ('', '.', '..') for p in relative.split('/')):
        raise ValueError(f'Unsafe export path: {relative!r}')
    path = root / relative
    if path.resolve() != path or not path.is_file():
        raise ValueError(f'Missing file or symlink in export: {relative!r}')
    return path


def content_type(path):
    fixed = {'.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
             '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
             '.json': 'application/json; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
             '.svg': 'image/svg+xml', '.zip': 'application/zip'}
    return fixed.get(path.suffix.lower()) or mimetypes.guess_type(path.name)[0] or 'application/octet-stream'


def inspect_file(root, relative, expected=None):
    path = safe_file(root, relative)
    before = signature(path)
    if before[2] > 5 * 1024**3:
        raise ValueError('This uploader supports single-part objects up to 5 GiB')
    sha = hashlib.sha256()
    md5 = hashlib.md5(usedforsecurity=False)
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024**2), b''):
            sha.update(block); md5.update(block)
    if signature(path) != before:
        raise ValueError(f'File changed during inspection: {relative}')
    if expected and (expected['bytes'] != before[2] or expected['sha256'] != sha.hexdigest()):
        raise ValueError(f'Export manifest mismatch: {relative}')
    return File(path, 'site/' + relative, before[2], sha.hexdigest(),
                base64.b64encode(md5.digest()).decode(), content_type(path), before)


def inventory(root):
    """Allow only manifest-pinned data, frontend assets, and the entry point."""
    root = root.resolve()
    index = inspect_file(root, 'index.html')
    html = index.path.read_text(encoding='utf-8')
    asset_refs = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', html)
    asset_refs = [ref for ref in asset_refs if not ref.startswith('data:')]
    if not asset_refs or any(not ref.startswith('./assets/') for ref in asset_refs):
        raise ValueError('Build with relative paths first: make build-volunteer-reading-room VOLUNTEER_BASE=./')
    for ref in asset_refs:
        safe_file(root, ref[2:])
    manifest_file = inspect_file(root, 'data/manifest.json')
    manifest = json.loads(manifest_file.path.read_text(encoding='utf-8'))
    if manifest.get('kind') != 'reading-room-static' or not isinstance(manifest.get('files'), list):
        raise ValueError('Not a reading-room export manifest')
    files = []
    seen = {'site/data/manifest.json', 'site/index.html'}
    for item in manifest['files']:
        relative = 'data/' + item['path']
        if 'site/' + relative in seen:
            raise ValueError(f'Duplicate export entry: {relative}')
        seen.add('site/' + relative)
        files.append(inspect_file(root, relative, item))
        if len(files) % 10000 == 0:
            print(f'Validated {len(files):,} data files...', flush=True)
    for path in sorted((root / 'assets').rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlinks are not deployment inputs')
        if path.is_file():
            files.append(inspect_file(root, path.relative_to(root).as_posix()))
    if 'site/data/catalog.json' not in seen:
        raise ValueError('Catalog missing from export manifest')
    # Publish these last. All other files must succeed first.
    files.extend([manifest_file, index])
    return files


def credentials():
    names = ('CLOUDFLARE_ACCOUNT_ID', 'CLOUDFLARE_API_TOKEN', 'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY')
    missing = [name for name in names if not os.environ.get(name)]
    if missing:
        raise ValueError('Set environment variables: ' + ', '.join(missing))
    values = {name: os.environ[name] for name in names}
    if not re.fullmatch(r'[a-fA-F0-9]{32}', values['CLOUDFLARE_ACCOUNT_ID']):
        raise ValueError('CLOUDFLARE_ACCOUNT_ID must be the 32-character account ID')
    return values


def s3_client(creds, jobs):
    try:
        import boto3
        from botocore.config import Config
    except ImportError:
        raise ValueError('Install tools/reading_room/requirements-deploy.txt in a virtual environment') from None
    return boto3.client('s3',
        endpoint_url=f"https://{creds['CLOUDFLARE_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        region_name='auto', aws_access_key_id=creds['R2_ACCESS_KEY_ID'],
        aws_secret_access_key=creds['R2_SECRET_ACCESS_KEY'],
        config=Config(signature_version='s3v4', max_pool_connections=jobs,
                      retries={'mode': 'standard', 'max_attempts': 8},
                      request_checksum_calculation='when_required', response_checksum_validation='when_required'))


def head(client, bucket, key):
    try:
        return client.head_object(Bucket=bucket, Key=key)
    except Exception as error:
        if getattr(error, 'response', {}).get('ResponseMetadata', {}).get('HTTPStatusCode') == 404:
            return None
        raise


def matches(remote, file):
    return bool(remote and remote.get('ContentLength') == file.size
                and remote.get('Metadata', {}).get('sha256') == file.sha256
                and remote.get('ContentType') == file.content_type
                and remote.get('CacheControl') == CACHE)


def upload_one(client, bucket, file):
    if signature(file.path) != file.signature:
        raise ValueError(f'Export changed; stop rebuilding while deploying: {file.key}')
    if matches(head(client, bucket, file.key), file):
        return False
    with file.path.open('rb') as stream:
        client.put_object(Bucket=bucket, Key=file.key, Body=stream, ContentLength=file.size,
                          ContentMD5=file.md5, ContentType=file.content_type,
                          CacheControl=CACHE, Metadata={'sha256': file.sha256})
    if signature(file.path) != file.signature or not matches(head(client, bucket, file.key), file):
        raise ValueError(f'Upload verification failed: {file.key}')
    return True


def upload_files(client, bucket, files, jobs):
    uploaded = skipped = 0
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        # Bound the queue so a failure does not leave 119,000 uploads pending.
        for offset in range(0, len(files) - 2, jobs * 4):
            batch = files[offset:min(offset + jobs * 4, len(files) - 2)]
            for changed in pool.map(lambda f: upload_one(client, bucket, f), batch):
                uploaded += changed; skipped += not changed
            if (offset // (jobs * 4)) % 32 == 0:
                print(f'Uploaded {uploaded:,}; unchanged {skipped:,}', flush=True)
    for file in files[-2:]:
        changed = upload_one(client, bucket, file)
        uploaded += changed; skipped += not changed
    print(f'Upload complete: {uploaded:,} uploaded; {skipped:,} unchanged. No objects deleted.')


def cloudflare(creds, method, suffix, body=None, content_type='application/json'):
    account = creds['CLOUDFLARE_ACCOUNT_ID']
    request = Request(f'https://api.cloudflare.com/client/v4/accounts/{account}/workers/scripts/{NAME}{suffix}',
                      data=body, method=method, headers={
                          'Authorization': 'Bearer ' + creds['CLOUDFLARE_API_TOKEN'],
                          'Content-Type': content_type})
    try:
        with urlopen(request, timeout=90) as response:
            result = json.load(response)
    except HTTPError as error:
        # Avoid API response echoes containing a secret or the upload payload.
        raise ValueError(f'Cloudflare {method} {suffix or "/script"}: HTTP {error.code}; check account, token permissions, and Worker name') from None
    except URLError:
        raise ValueError('Cloudflare API connection failed; rerun to resume') from None
    if not result.get('success'):
        codes = [str(e.get('code', 'unknown')) for e in result.get('errors', [])]
        raise ValueError('Cloudflare rejected the operation; error codes: ' + ', '.join(codes))
    return result.get('result')


def worker_payload(bucket, token):
    metadata = {
        'main_module': 'worker.mjs', 'compatibility_date': '2026-10-01',
        'bindings': [{'type': 'r2_bucket', 'name': 'ARCHIVE', 'bucket_name': bucket},
                     {'type': 'secret_text', 'name': 'SHARE_TOKEN', 'text': token}],
        'observability': {'enabled': False},
    }
    boundary = 'maso-' + secrets.token_hex(16)
    parts = []
    for name, filename, mime, data in [
        ('metadata', None, 'application/json', json.dumps(metadata).encode()),
        ('worker.mjs', 'worker.mjs', 'application/javascript+module', WORKER_FILE.read_bytes()),
    ]:
        disposition = f'Content-Disposition: form-data; name="{name}"'
        if filename:
            disposition += f'; filename="{filename}"'
        parts.append(f'--{boundary}\r\n{disposition}\r\nContent-Type: {mime}\r\n\r\n'.encode() + data + b'\r\n')
    return b''.join(parts) + f'--{boundary}--\r\n'.encode(), f'multipart/form-data; boundary={boundary}'


def read_token():
    if TOKEN_FILE.is_symlink():
        raise ValueError('Share-token file must not be a symlink')
    if not TOKEN_FILE.exists():
        return None
    if stat.S_IMODE(TOKEN_FILE.stat().st_mode) & 0o077:
        raise ValueError(f'Run chmod 600 {TOKEN_FILE}')
    token = TOKEN_FILE.read_text().strip()
    if not re.fullmatch(r'[A-Za-z0-9_-]{32,128}', token):
        raise ValueError('Invalid saved share token')
    return token


def save_token(token, path=TOKEN_FILE):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    # The pending file preserves the proposed link even if the API times out.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as stream:
        os.fchmod(stream.fileno(), 0o600)
        stream.write(token + '\n')


def verify_site(token, files):
    by_key = {file.key: file for file in files}
    for attempt in range(6):
        try:
            for relative in ('index.html', 'data/catalog.json'):
                with urlopen(ORIGIN + '/' + token + '/' + relative, timeout=60) as response:
                    digest = hashlib.sha256(response.read()).hexdigest()
                    if digest != by_key['site/' + relative].sha256:
                        raise ValueError('Hosted file checksum mismatch')
                    if response.headers.get('X-Robots-Tag') != 'noindex, nofollow, noarchive':
                        raise ValueError('Expected Worker headers missing')
            try:
                with urlopen(ORIGIN + '/data/catalog.json', timeout=30):
                    raise ValueError('Unlisted path unexpectedly accessible')
            except HTTPError as error:
                if error.code != 404:
                    raise ValueError('Expected 404 for unlisted path') from None
            print('Live checks passed: index/catalog checksums, response headers, and missing-token 404.')
            return
        except (URLError, ValueError):
            if attempt == 5:
                raise ValueError('Worker was published, but live checks did not pass. Check its bindings and retry; the share token is saved locally.') from None
            time.sleep(3)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'build/reading-room-volunteer')
    parser.add_argument('--apply', action='store_true', help='upload and publish; otherwise validate locally only')
    parser.add_argument('--worker-only', action='store_true', help='publish Worker only; require matching remote index and manifest')
    parser.add_argument('--rotate-link', action='store_true', help='generate a new share token; requires --apply')
    parser.add_argument('--show-link', action='store_true', help='print the saved share URL; no network access')
    parser.add_argument('--jobs', type=int, default=8)
    args = parser.parse_args(argv)
    if args.show_link:
        token = read_token()
        if not token:
            raise ValueError('No saved share token; deploy first')
        print(ORIGIN + '/' + token + '/#/review')
        return
    if args.rotate_link and not args.apply:
        raise ValueError('--rotate-link requires --apply')
    if not 1 <= args.jobs <= 32:
        raise ValueError('--jobs must be between 1 and 32')
    creds = credentials() if args.apply else None
    print('Checking local export and every manifest-pinned SHA-256...', flush=True)
    files = inventory(args.output)
    print(f'{len(files):,} files; {sum(f.size for f in files) / 10**9:.2f} GB; bucket/Worker: {NAME}')
    if not args.apply:
        print('DRY RUN: no network access, uploads, deployment, or secret creation. Use --apply to publish.')
        return
    old_token = read_token()
    pending = TOKEN_FILE.with_suffix('.pending')
    if pending.exists():
        raise ValueError('A pending deployment token exists. Follow the recovery instructions in docs/DEPLOY-READING-ROOM.md before retrying.')
    client = s3_client(creds, args.jobs)
    # Authenticate both services before uploading anything; never create resources.
    cloudflare(creds, 'GET', '/settings')
    client.head_bucket(Bucket=NAME)
    if args.worker_only:
        for file in files[-2:]:
            if not matches(head(client, NAME, file.key), file):
                raise ValueError('--worker-only requires an already uploaded, matching export; run --apply first')
    else:
        upload_files(client, NAME, files, args.jobs)
    token = secrets.token_urlsafe(32) if args.rotate_link or not old_token else old_token
    save_token(token, pending)
    body, mime = worker_payload(NAME, token)
    print('Publishing Worker code, R2 binding, and share secret...', flush=True)
    cloudflare(creds, 'PUT', '', body, mime)
    os.replace(pending, TOKEN_FILE)
    cloudflare(creds, 'POST', '/subdomain', json.dumps({'enabled': True, 'previews_enabled': False}).encode())
    verify_site(token, files)
    print('Deployment complete. Print the share URL with --show-link (it is intentionally omitted from logs).')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted. Rerun to resume uploads; no remote objects were deleted.', file=sys.stderr)
        sys.exit(130)
    except Exception as error:
        # SDK errors may include request details; display only known local messages.
        print(str(error) if isinstance(error, ValueError) else f'{type(error).__name__}: deployment failed; check credentials/network and rerun. No remote objects were deleted.', file=sys.stderr)
        sys.exit(1)
