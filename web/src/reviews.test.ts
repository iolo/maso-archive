import { describe, expect, it, vi, afterEach } from 'vitest'
import { articleSource, emptyReviews, filterReviewArticles, noteRoute, parseReviews, readReviews, REVIEW_KEY, reviewState, saveReview, type ReviewNote } from './reviews'
import type { ArticleSummary } from './data'

const article = { article_id: 'scan:1984-08:1', issue_id: 'maso-1984-08', title: '한글 BASIC', byline: '홍길동', sourceKind: 'scan', text_sha256: 'a'.repeat(64), reference: 'aug-01' } as ArticleSummary
const note = (patch: Partial<ReviewNote> = {}): ReviewNote => ({ articleId: article.article_id, issueId: article.issue_id, title: article.title, regionId: null, route: noteRoute(article.article_id, null), source: 'PDF', textSha256: article.text_sha256, packageSha256: null, reviewer: 'Reviewer', status: 'checked', note: 'Code line 10 checked.', updatedAt: '2026-10-14T00:00:00Z', ...patch })
afterEach(() => vi.unstubAllGlobals())

describe('volunteer review records', () => {
  it('round-trips Korean feedback and safely encoded region links', () => {
    const n = note({ regionId: 'r/1?x', route: noteRoute(article.article_id, 'r/1?x'), note: '교정 <제안>' })
    expect(parseReviews(JSON.stringify({ ...emptyReviews(), notes: [n] })).notes).toEqual([n])
    expect(n.route).toContain('region=r%2F1%3Fx')
  })
  it('rejects malformed records, external routes, duplicate notes and invalid versions', () => {
    for (const value of [{ ...emptyReviews(), schemaVersion: 2 }, { ...emptyReviews(), notes: [note({ route: 'https://example.org' })] }, { ...emptyReviews(), notes: [note(), note()] }, { ...emptyReviews(), notes: [note({ textSha256: 'invalid' })] }, { ...emptyReviews(), notes: [null] }]) expect(() => parseReviews(JSON.stringify(value))).toThrow()
  })
  it('keeps regional checks distinct from whole-article checks and ignores stale text', () => {
    expect(reviewState(article, [])).toBe('pending')
    expect(reviewState(article, [note({ regionId: 'r1' })])).toBe('in-progress')
    expect(reviewState(article, [note()])).toBe('checked')
    expect(reviewState(article, [note(), note({ regionId: 'r1', status: 'needs-fix' })])).toBe('needs-fix')
    expect(reviewState(article, [note({ textSha256: 'b'.repeat(64) })])).toBe('pending')
  })
  it('filters PDF and all CD sources by issue, status and normalized metadata', () => {
    const cd = { ...article, article_id: 'cd:1', sourceKind: undefined, disc: 'cd3', issue_id: 'cd3-9501' }
    expect(articleSource({ ...cd, disc: undefined })).toBe('CD1')
    expect(filterReviewArticles([article, cd], [note()], { source: 'PDF', issue: 'maso-1984-08', status: 'checked', query: 'ｂａｓｉｃ' })).toEqual([article])
    expect(filterReviewArticles([article, cd], [], { source: 'CD3', issue: '', status: 'pending', query: '' })).toEqual([cd])
  })
  it('preserves unrelated records on updates and refuses to overwrite corrupt storage', () => {
    const data = new Map<string, string>()
    vi.stubGlobal('localStorage', { getItem: (k: string) => data.get(k) || null, setItem: (k: string, v: string) => data.set(k, v) })
    vi.stubGlobal('window', { dispatchEvent: vi.fn() })
    saveReview(note()); saveReview(note({ regionId: 'r1', route: noteRoute(article.article_id, 'r1') })); saveReview(note({ note: 'updated' }))
    expect(readReviews().notes).toHaveLength(2)
    expect(readReviews().notes.find(n => n.regionId === null)?.note).toBe('updated')
    data.set(REVIEW_KEY, '{broken')
    expect(() => saveReview(note())).toThrow()
    expect(data.get(REVIEW_KEY)).toBe('{broken')
  })
})
