import { afterEach, describe, expect, it, vi } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import { MemoryRouter } from 'react-router-dom'
import { ScanArticle } from './ScanArticle'
import { scanFixture } from './scan-fixtures'

const render = (state: Parameters<typeof scanFixture>[0], route = '/') => renderToStaticMarkup(<MemoryRouter initialEntries={[route]}><ScanArticle doc={scanFixture(state)} /></MemoryRouter>)
describe('scan reading and evidence states', () => {
  afterEach(() => vi.unstubAllGlobals())
  it('shows the printed byline even when the TOC author omits its role', () => {
    vi.stubGlobal('document', { baseURI: 'http://localhost/archive/' })
    const doc = scanFixture('readable')
    doc.article.byline = 'Synthetic author'
    doc.blocks.unshift({ id: 'byline', type: 'byline', preformatted: false, paragraphs: [{ id: 'author', terminated: false, runs: [{ type: 'text', text: 'Synthetic author (printed role)' }] }] })
    const html = renderToStaticMarkup(<MemoryRouter><ScanArticle doc={doc} /></MemoryRouter>)
    expect(html).toContain('Synthetic author (printed role)')
    expect(html.match(/printed role/g)).toHaveLength(1)
  })
  it('preserves literal code and prose paragraphs without turning availability into review', () => {
    vi.stubGlobal('document', { baseURI: 'http://localhost/archive/' })
    const html = render('partial')
    expect(html).toContain('복원: 일부 복원')
    expect(html).toContain('검토: 미검토')
    expect(html).toContain('Synthetic missing passage remains marked')
    expect(html).toContain('<pre><code>  10 PRINT &quot;&lt;tag&gt;&amp;&quot;\n\t20 END  \n</code></pre>')
    expect(html).toContain('<p class="article-paragraph">Invented first paragraph.</p><p class="article-paragraph">Invented second paragraph.</p>')
    expect(html).not.toContain('CD 참조')
  })
  it('keeps image-only material accessible without inventing text downloads', () => {
    vi.stubGlobal('document', { baseURI: 'http://localhost/archive/' })
    const html = render('image-only')
    expect(html).toContain('스캔만 있음')
    expect(html).toContain('region=r1')
    expect(html).not.toContain('<pre>')
    expect(html).not.toContain('download=')
    expect(html).not.toContain('<img') // Region scans wait for an explicit selection.
  })
  it('shows failed and unresolved states without broken source or download links', () => {
    vi.stubGlobal('document', { baseURI: 'http://localhost/archive/' })
    for (const state of ['failed', 'unresolved'] as const) {
      const html = render(state)
      expect(html).toContain('확인된 스캔 영역이 없습니다')
      expect(html).not.toContain('download=')
      expect(html).not.toContain('/data/source/')
      expect(html).not.toContain('class="article-body"')
    }
  })
  it('loads only the selected evidence image and handles unknown regions', () => {
    vi.stubGlobal('document', { baseURI: 'http://localhost/archive/' })
    const html = render('image-only', '/?region=r1')
    expect(html).toContain('원본 크기로 열기')
    expect(html).toContain('인쇄 미상쪽')
    expect(html).toContain('synthetic/scan.svg')
    expect((html.match(/<img/g) || []).length).toBe(1)
    expect(render('image-only', '/?region=unknown')).toContain('스캔 영역을 찾을 수 없습니다')
  })
})
