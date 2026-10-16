import assert from 'node:assert/strict';
import { test } from 'node:test';
import worker from './cloudflare-worker.mjs';

const token = 'a'.repeat(43);
const base = `https://example.workers.dev/${token}/`;
function fixture() {
  const calls = [];
  const stored = new Map([
    ['site/index.html', ['<h1>Reader</h1>', 'text/html; charset=utf-8']],
    ['site/data/한글 #?.txt', ['0123456789', 'text/plain; charset=utf-8']],
    ['site/assets/app.js', ['export default 1;', 'text/javascript; charset=utf-8']],
  ]);
  const meta = (key) => {
    const value = stored.get(key);
    if (!value) return null;
    return { size: Buffer.byteLength(value[0]), etag: 'digest', httpEtag: '"digest"', uploaded: new Date('2026-10-01T00:00:00Z'),
      writeHttpMetadata(headers) { headers.set('Content-Type', value[1]); headers.set('Cache-Control', 'public'); } };
  };
  const env = { SHARE_TOKEN: token, ARCHIVE: {
    async head(key) { calls.push(['head', key]); return meta(key); },
    async get(key, options) {
      calls.push(['get', key, options]);
      const object = meta(key);
      if (!object) return null;
      assert.equal(options.onlyIf.etagMatches, object.etag);
      let body = Buffer.from(stored.get(key)[0]);
      if (options.range) body = body.subarray(options.range.offset, options.range.offset + options.range.length);
      return { ...object, body };
    },
  } };
  return { env, calls, fetch: (path = '', options) => worker.fetch(new Request(base + path, options), env) };
}

test('missing, incorrect and unconfigured tokens never query R2', async () => {
  const { env, calls } = fixture();
  for (const path of ['/', '/data/catalog.json', '/wrong/index.html', `/${token}extra/index.html`]) {
    assert.equal((await worker.fetch(new Request('https://example.workers.dev' + path), env)).status, 404);
  }
  assert.equal((await worker.fetch(new Request(base), { ...env, SHARE_TOKEN: '' })).status, 404);
  assert.equal(calls.length, 0);
});

test('root redirects to trailing slash then serves index with privacy headers', async () => {
  const { env, fetch } = fixture();
  const redirect = await worker.fetch(new Request(base.slice(0, -1)), env);
  assert.equal(redirect.status, 308);
  assert.equal(redirect.headers.get('location'), `/${token}/`);
  const response = await fetch();
  assert.equal(await response.text(), '<h1>Reader</h1>');
  assert.equal(response.headers.get('Content-Type'), 'text/html; charset=utf-8');
  assert.equal(response.headers.get('Cache-Control'), 'private, no-store');
  assert.equal(response.headers.get('X-Robots-Tag'), 'noindex, nofollow, noarchive');
  assert.equal(response.headers.get('Referrer-Policy'), 'no-referrer');
});

test('Unicode and reserved filename characters decode exactly once', async () => {
  const { fetch, calls } = fixture();
  const response = await fetch('data/' + encodeURIComponent('한글 #?.txt'));
  assert.equal(await response.text(), '0123456789');
  assert.equal(calls[0][1], 'site/data/한글 #?.txt');
});

test('traversal, unsupported paths, directory requests and bad encodings cannot list the bucket', async () => {
  const { fetch, calls } = fixture();
  for (const path of ['data/%2e%2e%2fsecret', 'data/%00x', 'data/%5csecret', 'data/', 'data//x', 'private/key']) {
    assert.equal((await fetch(path)).status, 404);
  }
  assert.equal((await fetch('data/%zz')).status, 400);
  assert.equal(calls.length, 0);
});

test('missing objects are 404 and writes are rejected', async () => {
  const { fetch } = fixture();
  assert.equal((await fetch('data/missing')).status, 404);
  const response = await fetch('index.html', { method: 'PUT', body: 'overwrite' });
  assert.equal(response.status, 405);
  assert.equal(response.headers.get('Allow'), 'GET, HEAD');
});

test('HEAD and conditional requests do not read object bodies', async () => {
  const { fetch, calls } = fixture();
  const response = await fetch('', { method: 'HEAD' });
  assert.equal(response.headers.get('Content-Length'), '15');
  assert.equal(await response.text(), '');
  for (const tag of ['"digest"', 'W/"digest"', '"old", "digest"', '*']) {
    const cached = await fetch('', { headers: { 'If-None-Match': tag } });
    assert.equal(cached.status, 304);
    assert.equal(cached.headers.has('Content-Length'), false);
  }
  assert.equal(calls.filter(c => c[0] === 'get').length, 0);
});

test('range and suffix downloads have correct lengths and content', async () => {
  const { fetch } = fixture();
  const path = 'data/' + encodeURIComponent('한글 #?.txt');
  for (const [range, expected, header] of [['bytes=2-5', '2345', 'bytes 2-5/10'], ['bytes=-3', '789', 'bytes 7-9/10'], ['bytes=8-', '89', 'bytes 8-9/10']]) {
    const response = await fetch(path, { headers: { Range: range } });
    assert.equal(response.status, 206);
    assert.equal(response.headers.get('Content-Range'), header);
    assert.equal(response.headers.get('Content-Length'), String(expected.length));
    assert.equal(await response.text(), expected);
  }
  for (const range of ['bytes=20-', 'bytes=3-1', 'bytes=-0', 'bytes=1-2,4-5', 'bytes=9007199254740992-']) {
    const response = await fetch(path, { headers: { Range: range } });
    assert.equal(response.status, 416);
    assert.equal(response.headers.get('Content-Range'), 'bytes */10');
  }
  const response = await fetch(path, { headers: { Range: 'bytes=1-2', 'If-Range': '"old"' } });
  assert.equal(response.status, 200);
  assert.equal(await response.text(), '0123456789');
});

test('concurrent replacement and storage failure return retryable responses', async () => {
  const { env, fetch } = fixture();
  env.ARCHIVE.get = async () => ({ etag: 'changed' });
  assert.equal((await fetch()).status, 503);
  env.ARCHIVE.head = async () => { throw Error('private internal details'); };
  const response = await fetch();
  assert.equal(response.status, 503);
  assert.equal((await response.text()).includes('private internal details'), false);
});

test('robots discourages indexing without disclosing a share path', async () => {
  const { env } = fixture();
  const response = await worker.fetch(new Request('https://example.workers.dev/robots.txt'), env);
  assert.equal(await response.text(), 'User-agent: *\nDisallow: /\n');
});
