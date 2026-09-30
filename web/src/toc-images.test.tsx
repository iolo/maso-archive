import { afterEach, describe, expect, it, vi } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import { TocImages } from './TocImages'
import type { TocImage } from './data'

describe('TOC image collection', () => {
  afterEach(() => vi.unstubAllGlobals())
  it('keeps old datasets unchanged and distinguishes an explicitly missing donation', () => {
    expect(renderToStaticMarkup(<TocImages label="91.06" />)).toBe('')
    const missing = renderToStaticMarkup(<TocImages label="91.06" pages={[]} />)
    expect(missing).toContain('기증 차례 스캔은 없습니다')
    expect(missing).not.toContain('<img')
  })
  it('renders ordered lazy previews without requesting readable images', () => {
    vi.stubGlobal('document', { baseURI: 'https://example.test/archive/' })
    const pages: TocImage[] = [1, 2].map(sequence => ({ sequence,
      preview: { path: `tocs/page-${sequence}-preview.jpg`, width: 480, height: 720, bytes: 20, sha256: 'a'.repeat(64) },
      readable: { path: `tocs/page-${sequence}-readable.jpg`, width: 1600, height: 2400, bytes: 200, sha256: 'b'.repeat(64) } }))
    const html = renderToStaticMarkup(<TocImages label="88.02" pages={pages} />)
    expect(html).toContain('88.02 인쇄 차례 1 / 2')
    expect(html).toContain('88.02 인쇄 차례 2 / 2')
    expect(html).toContain('loading="lazy"')
    expect(html).toContain('width="480" height="720"')
    expect(html).not.toContain('-readable.jpg')
    expect(html).not.toContain('tocs/8802-01.jpg')
  })
})
