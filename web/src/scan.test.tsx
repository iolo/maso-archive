import { afterEach, describe, expect, it, vi } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import { MemoryRouter } from 'react-router-dom'
import { ScanArticle, sectionPath } from './ScanArticle'
import { TocDetail } from './App'
import type { IssueDoc } from './data'
import { scanFixture } from './scan-fixtures'

const render = (state: Parameters<typeof scanFixture>[0], route = '/') => renderToStaticMarkup(<MemoryRouter initialEntries={[route]}><ScanArticle doc={scanFixture(state)} /></MemoryRouter>)
describe('scan reading and evidence states', () => {
  afterEach(() => vi.unstubAllGlobals())
  it('retains internal titles as section targets and reports unknown targets', () => {
    vi.stubGlobal('document', { baseURI: 'http://localhost/archive/' })
    const doc = scanFixture('readable')
    doc.blocks.unshift({ id: 'internal-title', scanBlockId: 'section-2', type: 'title', preformatted: false,
      paragraphs: [{ id: 'heading', terminated: false, runs: [{ type: 'text', text: '2. Internal heading' }] }] })
    const html = renderToStaticMarkup(<MemoryRouter initialEntries={['/?section=section-2']}><ScanArticle doc={doc} /></MemoryRouter>)
    expect(html).toContain('id="internal-title" tabindex="-1"')
    expect(html).toContain('<h2>2. Internal heading</h2>')
    expect(html).not.toContain('요청한 절을 찾을 수 없습니다')
    expect(render('readable', '/?section=unknown')).toContain('요청한 절을 찾을 수 없습니다')
  })
  it('links section entries to one parent body and treats group headings as groups', () => {
    const article = scanFixture('readable').article
    const issue: IssueDoc = { schemaVersion: 3, issue: { id: article.issue_id, year: 1900, month: 1, label: 'Synthetic', articleCount: 1, textCount: 1, tocCount: 3, cover: null },
      articles: [article], toc: [
        { id: 'group', parentId: null, depth: 0, title: 'Group', byline: null, page: null, kind: 'heading', articleIds: [], restorationKind: 'group-heading' },
        { id: 'parent', parentId: 'group', depth: 1, title: 'Parent', byline: null, page: 1, kind: 'article', articleIds: [article.article_id], restorationKind: 'article' },
        { id: 'child', parentId: 'parent', depth: 2, title: 'Internal section', byline: null, page: null, kind: 'subtopic', articleIds: [article.article_id], restorationKind: 'section-reference', sectionRef: { articleId: article.article_id, blockId: 'section-2' } },
      ] }
    const html = renderToStaticMarkup(<MemoryRouter><TocDetail issue={issue} id="child" /></MemoryRouter>)
    expect(html).toContain(sectionPath(article.article_id, 'section-2'))
    expect(html).toContain('이 항목은 아래 글 안의 절입니다')
    const group = renderToStaticMarkup(<MemoryRouter><TocDetail issue={issue} id="group" /></MemoryRouter>)
    expect(group).toContain('여러 글을 묶는 차례 제목')
    expect(group).toContain('Parent')
    expect(group).not.toContain('읽기 자료 연결이 없습니다')
  })
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
