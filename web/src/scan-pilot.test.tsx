import { afterEach, describe, expect, it, vi } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import { MemoryRouter } from 'react-router-dom'
import { IssueOverview, TocDetail } from './App'
import { ScanArticle } from './ScanArticle'
import { pageForRegion, type IssueDoc } from './data'
import { articleSource, filterReviewArticles } from './reviews'
import { scanFixture } from './scan-fixtures'

describe('JPEG pilot review', () => {
  afterEach(() => vi.unstubAllGlobals())
  const jpeg = () => {
    const doc = scanFixture('readable')
    doc.article.scanSourceKind = 'jpeg-set'
    doc.scan!.source.kind = 'jpeg-set'
    doc.scan!.pages = [201, 207].map((index, i) => ({ source_index: index, source_filename_number: 198 + i * 6,
      printed_page: String(198 + i * 6), image: { path: `page-${index}.jpg`, bytes: 1, sha256: 'a'.repeat(64) },
      width_px: 100, height_px: 200, reading_order: i, image_to_upright_normalized: [.01, 0, 0, .005, 0, 0] }))
    const asset = doc.scan!.regions[0].asset
    doc.scan!.regions = [201, 207].map((index, i) => ({ id: `jpeg-${i}`, source_index: index,
      kind: 'prose', bbox: [0, 0, 1, 1], notes: '', asset }))
    return doc
  }
  it('matches the actual JPEG source index across nonconsecutive pages', () => {
    vi.stubGlobal('document', { baseURI: 'http://localhost/pilot/' })
    const doc = jpeg()
    expect(pageForRegion(doc.scan!.pages, doc.scan!.regions[1])?.printed_page).toBe('204')
    expect(pageForRegion(doc.scan!.pages, { ...doc.scan!.regions[1], source_index: 999 })).toBeUndefined()
    const html = renderToStaticMarkup(<MemoryRouter initialEntries={['/?region=jpeg-1']}><ScanArticle doc={doc} /></MemoryRouter>)
    expect(html).toContain('204쪽 원문 대조')
    expect(html).toContain('JPEG image 204')
    expect(html).not.toContain('PDF ')
    expect(html).toContain('204쪽 · 2/2')
  })
  it('labels JPEG review records and filters them independently of PDFs', () => {
    const jpg = jpeg().article, pdf = scanFixture('readable').article
    expect(articleSource(jpg)).toBe('JPEG scans')
    expect(articleSource(pdf)).toBe('PDF')
    expect(filterReviewArticles([jpg, pdf], [], { source: 'JPEG scans', issue: '', status: '', query: '' })).toEqual([jpg])
  })
  it('shows unfinished pilot accounting and leaves unclassified identities pending', () => {
    const doc = jpeg()
    const issue: IssueDoc = { schemaVersion: 3, issue: { id: doc.article.issue_id, year: 1900, month: 1,
      label: 'Synthetic', articleCount: 1, textCount: 1, tocCount: 1, cover: null }, articles: [doc.article],
      scanPilot: { note: 'Restoration is paused.', counts: { articles: 1, complete: 1, partial: 0, group_headings: 0, unclassified: 1 } },
      toc: [{ id: 'pending', parentId: null, depth: 0, title: 'Pending identity', byline: null, page: null,
        kind: 'unknown', articleIds: [], restorationKind: 'unclassified' }] }
    const overview = renderToStaticMarkup(<MemoryRouter><IssueOverview issue={issue} /></MemoryRouter>)
    expect(overview).toContain('1 complete native articles')
    expect(overview).toContain('1 unclassified entries')
    expect(overview).toContain('Restoration is paused.')
    const detail = renderToStaticMarkup(<MemoryRouter><TocDetail issue={issue} id="pending" /></MemoryRouter>)
    expect(detail).toContain('Restoration pending:')
    expect(detail).toContain('does not mean its source pages are missing')
  })
})
