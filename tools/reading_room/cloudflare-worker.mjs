// Static file delivery only. The bucket must not have another public endpoint.
const commonHeaders = {
  'Cache-Control': 'private, no-store',
  'X-Robots-Tag': 'noindex, nofollow, noarchive',
  'Referrer-Policy': 'no-referrer',
  'X-Content-Type-Options': 'nosniff',
};

function reply(request, status, text, extra = {}) {
  return new Response(request.method === 'HEAD' ? null : text, {
    status, headers: { ...commonHeaders, 'Content-Type': 'text/plain; charset=utf-8', ...extra },
  });
}

// Parse one byte range; large ZIP/image downloads are streamed from R2.
export function byteRange(value, size) {
  const match = /^bytes=(\d*)-(\d*)$/.exec(value);
  if (!match || (!match[1] && !match[2]) || !size) return null;
  let start, end;
  if (!match[1]) {
    const suffix = Number(match[2]);
    if (!Number.isSafeInteger(suffix) || suffix <= 0) return null;
    start = Math.max(0, size - suffix); end = size - 1;
  } else {
    start = Number(match[1]);
    end = match[2] ? Number(match[2]) : size - 1;
    if (!Number.isSafeInteger(start) || !Number.isSafeInteger(end) || start > end || start >= size) return null;
    end = Math.min(end, size - 1);
  }
  return { offset: start, length: end - start + 1 };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/robots.txt') return reply(request, 200, 'User-agent: *\nDisallow: /\n');
    // Fail closed when the binding/secret has not been configured.
    if (!/^[A-Za-z0-9_-]{32,128}$/.test(env.SHARE_TOKEN || '')) return reply(request, 404, 'Not found');
    const prefix = `/${env.SHARE_TOKEN}`;
    if (url.pathname !== prefix && !url.pathname.startsWith(prefix + '/')) return reply(request, 404, 'Not found');
    if (!['GET', 'HEAD'].includes(request.method)) return reply(request, 405, 'Method not allowed', { Allow: 'GET, HEAD' });
    if (url.pathname === prefix) return reply(request, 308, '', { Location: prefix + '/' + url.search });
    let path;
    try { path = decodeURIComponent(url.pathname.slice(prefix.length + 1)) || 'index.html'; }
    catch { return reply(request, 400, 'Invalid path'); }
    if (/[\\\x00-\x1f\x7f]/.test(path) || path.split('/').some(p => !p || p === '.' || p === '..')) return reply(request, 404, 'Not found');
    // Expose only the exported reader tree, never bucket listings or other keys.
    if (path !== 'index.html' && !path.startsWith('assets/') && !path.startsWith('data/')) return reply(request, 404, 'Not found');
    const key = `site/${path}`;
    try {
      const object = await env.ARCHIVE.head(key);
      if (!object) return reply(request, 404, 'Not found');
      const headers = new Headers(commonHeaders);
      object.writeHttpMetadata(headers);
      // These headers take precedence over any metadata on uploaded objects.
      for (const [name, value] of Object.entries(commonHeaders)) headers.set(name, value);
      headers.set('ETag', object.httpEtag);
      headers.set('Last-Modified', object.uploaded.toUTCString());
      headers.set('Accept-Ranges', 'bytes');
      headers.set('Content-Length', String(object.size));
      const noneMatch = request.headers.get('If-None-Match');
      if (noneMatch?.split(',').some(tag => tag.trim() === '*' || tag.trim().replace(/^W\//, '') === object.httpEtag)) {
        headers.delete('Content-Length');
        return new Response(null, { status: 304, headers });
      }
      if (request.method === 'HEAD') return new Response(null, { headers });
      let range;
      const requested = request.headers.get('Range');
      const ifRange = request.headers.get('If-Range');
      if (requested && (!ifRange || ifRange === object.httpEtag || ifRange === object.uploaded.toUTCString())) {
        range = byteRange(requested, object.size);
        if (!range) return reply(request, 416, 'Range not satisfiable', { 'Content-Range': `bytes */${object.size}` });
        headers.set('Content-Range', `bytes ${range.offset}-${range.offset + range.length - 1}/${object.size}`);
        headers.set('Content-Length', String(range.length));
      }
      const result = await env.ARCHIVE.get(key, { onlyIf: { etagMatches: object.etag }, ...(range ? { range } : {}) });
      // An in-place upload may have replaced the object between head and get.
      if (!result || !('body' in result)) return reply(request, 503, 'Please retry', { 'Retry-After': '1' });
      return new Response(result.body, { status: range ? 206 : 200, headers });
    } catch {
      // Do not log request URLs: their paths contain the share token.
      return reply(request, 503, 'Storage temporarily unavailable', { 'Retry-After': '5' });
    }
  },
};
