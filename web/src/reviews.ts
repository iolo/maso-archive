import { type ArticleSummary, articlePath, normalize } from './data'

export const REVIEW_KEY = 'maso-volunteer-reviews-v1'
export const reviewLabels = { 'in-progress': '검토 중', 'needs-fix': '수정 제안', checked: '대조 완료' } as const
export type ReviewStatus = keyof typeof reviewLabels
export type ReviewNote = {
  articleId: string; issueId: string; title: string; regionId: string | null
  source: string; textSha256: string | null; packageSha256: string | null
  route: string; reviewer: string; status: ReviewStatus; note: string; updatedAt: string
}
export type ReviewFile = { schemaVersion: 1; kind: 'maso-volunteer-reviews'; notes: ReviewNote[] }
export const reviewKey = (articleId: string, regionId: string | null) => JSON.stringify([articleId, regionId])
export const articleSource = (a: ArticleSummary) => a.sourceKind === 'scan' ? 'PDF' : (a.disc || 'cd1').toUpperCase()
export const noteRoute = (articleId: string, regionId: string | null) => articlePath(articleId) + (regionId ? `?region=${encodeURIComponent(regionId)}` : '')

export function parseReviews(text: string): ReviewFile {
  const value = JSON.parse(text)
  if (value?.schemaVersion !== 1 || value.kind !== 'maso-volunteer-reviews' || !Array.isArray(value.notes)) throw new Error('지원하지 않는 검토 파일입니다.')
  const keys = new Set<string>()
  for (const n of value.notes) {
    if (!n || !['articleId', 'issueId', 'title', 'source', 'route', 'reviewer', 'note', 'updatedAt'].every(k => typeof n[k] === 'string') ||
        !n.articleId || !(n.regionId === null || typeof n.regionId === 'string') ||
        ![n.textSha256, n.packageSha256].every(v => v === null || (typeof v === 'string' && /^[a-f0-9]{64}$/.test(v))) ||
        !Object.hasOwn(reviewLabels, n.status) || !Number.isFinite(Date.parse(n.updatedAt)) || n.route !== noteRoute(n.articleId, n.regionId)) throw new Error('검토 기록의 형식이 올바르지 않습니다.')
    const key = reviewKey(n.articleId, n.regionId)
    if (keys.has(key)) throw new Error('중복 검토 기록이 있습니다.')
    keys.add(key)
  }
  return value
}
export const emptyReviews = (): ReviewFile => ({ schemaVersion: 1, kind: 'maso-volunteer-reviews', notes: [] })
export function readReviews(): ReviewFile {
  const text = localStorage.getItem(REVIEW_KEY)
  return text ? parseReviews(text) : emptyReviews()
}
export function saveReview(note: ReviewNote): void {
  // Re-read before writing so notes saved by another tab are retained.
  const file = readReviews()
  file.notes = file.notes.filter(n => reviewKey(n.articleId, n.regionId) !== reviewKey(note.articleId, note.regionId))
  file.notes.push(note)
  localStorage.setItem(REVIEW_KEY, JSON.stringify(file))
  window.dispatchEvent(new Event('maso-reviews-changed'))
}
export function reviewState(article: ArticleSummary, notes: ReviewNote[]): ReviewStatus | 'pending' {
  const current = notes.filter(n => n.articleId === article.article_id && n.textSha256 === article.text_sha256)
  if (current.some(n => n.status === 'needs-fix')) return 'needs-fix'
  if (current.some(n => n.regionId === null && n.status === 'checked')) return 'checked'
  return current.length ? 'in-progress' : 'pending'
}
export function filterReviewArticles(articles: ArticleSummary[], notes: ReviewNote[], filters: { source: string; issue: string; status: string; query: string }) {
  const q = normalize(filters.query)
  return articles.filter(a => (!filters.source || articleSource(a) === filters.source) && (!filters.issue || a.issue_id === filters.issue) &&
    (!filters.status || reviewState(a, notes) === filters.status) && (!q || normalize(`${a.title} ${a.byline || ''} ${a.reference} ${a.issue_id}`).includes(q)))
}
