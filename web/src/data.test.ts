import { afterEach, describe, expect, it, vi } from 'vitest'
import { createElement } from 'react'
import { renderToStaticMarkup } from 'react-dom/server'
import { RenderRun } from './App'
import { dataUrl, load, mediaUrl, normalize, search, type SearchItem } from './data'

describe('archive data lookup', () => {
  afterEach(() => vi.unstubAllGlobals())
  it('loads all three supported static versions and rejects unknown versions', async () => {
    vi.stubGlobal('document', { baseURI: 'http://localhost/archive/' })
    for (const version of [1, 2, 3, 4]) {
      vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => ({ schemaVersion: version }) }))
      if (version <= 3) expect(await load('catalog.json')).toEqual({ schemaVersion: version })
      else await expect(load('catalog.json')).rejects.toThrow('Unsupported data version')
    }
  })
  it('uses disc-specific media paths and refuses unavailable originals', () => {
    vi.stubGlobal('document', { baseURI: 'http://localhost/' })
    const media = { issue: 'cd3-9501', resource: 'FIGURE.BMP', status: 'available' as const,
      asset_name: 'FIGURE.BMP.png', original_sha256: '', conversion_note: null,
      originalPath: 'cd3/groups/9501/media/FIGURE.BMP', previewPath: 'cd3/groups/9501/media/FIGURE.BMP.png' }
    expect(mediaUrl(media, true)).toContain('/data/source/cd3/groups/9501/media/FIGURE.BMP.png')
    expect(() => mediaUrl({ ...media, status: 'missing', originalPath: null })).toThrow('Media source unavailable')
  })
  it('renders recovered text without an optional marks field as literal text', () => {
    const html = renderToStaticMarkup(createElement(RenderRun, {
      run: { type: 'text', text: '<tag> & ⟦bytes:81⟧' }, issueId: 'maso-1988-02', media: [],
    }))
    expect(html).toContain('&lt;tag&gt; &amp; ⟦bytes:81⟧')
  })
  it('rejects paths that could escape the static data root', () => {
    expect(() => dataUrl('../private.json')).toThrow('Unsafe data path')
    expect(() => dataUrl('/private.json')).toThrow('Unsafe data path')
  })
  it('searches Korean display metadata without rewriting it', () => {
    const items: SearchItem[] = [
      { kind: 'article', id: 'a', issueId: 'maso-1988-02', title: '터보 C 에디터', byline: null, reference: '8802184', status: 'prepared' },
      { kind: 'toc', id: 't', issueId: 'maso-1988-02', title: '터보 C 에디터', byline: '홍길동', articleIds: ['a'], status: 'linked' },
      { kind: 'toc', id: 'u', issueId: 'maso-1983-11', title: '터보 C 복습', byline: null, articleIds: [], status: 'unmatched' },
    ]
    expect(normalize('  Ｃ  ')).toBe('c')
    expect(search(items, '터보')).toEqual([items[2], items[0]])
    expect(search(items, '8802184')[0]).toBe(items[0])
    expect(search(items, '터보', 'maso-1983-11')).toEqual([items[2]])
    expect(items[0].title).toBe('터보 C 에디터')
  })
  it('keeps overlapping native dates and article references distinct in search', () => {
    const items: SearchItem[] = ['cd2', 'cd3'].map(disc => ({
      kind: 'article', id: `${disc}:article:shared`, issueId: `${disc}-9401`,
      title: '같은 제목', byline: null, reference: 'shared', status: 'partial',
    }))
    expect(search(items, 'shared')).toHaveLength(2)
    expect(search(items, 'shared', 'cd3-9401')).toEqual([items[1]])
  })
})
