export type Status = 'prepared' | 'normalized' | 'reference_with_gaps' | 'blocked' | 'unavailable'
export type IssueSummary = { id: string; year: number; month: number; label: string; articleCount: number; textCount: number; tocCount: number; cover: null }
export type ArticleSummary = { reference: string; article_id: string; issue_id: string; title: string; byline: string | null; page: number | null; status: Status; path: string; text: string | null; paragraphs: number; listings: number; image_occurrences: number; resources: string[]; text_sha256: string | null }
export type TocEntry = { id: string; parentId: string | null; depth: number; title: string; byline: string | null; page: number | null; kind: string; articleIds: string[] }
export type IssueDoc = { schemaVersion: 1; issue: IssueSummary; toc: TocEntry[]; articles: ArticleSummary[] }
export type Catalog = { schemaVersion: 1; issues: IssueSummary[]; articles: ArticleSummary[] }
export type Media = { issue: string; resource: string; status: 'available' | 'deferred'; asset_name: string | null; original_sha256: string; conversion_note: string | null }
export type MediaDoc = { schemaVersion: 1; issueId: string; items: Media[] }
export type Run = { type: 'text'; text: string; marks?: string[] } | { type: 'media'; resource: string; marks?: string[]; media_id?: string; occurrence_id?: string }
export type Paragraph = { id: string; runs: Run[]; terminated?: boolean }
export type Block = { id: string; type: string; layout?: string; preformatted: boolean; heading_level?: number | null; caption_for?: string | null; paragraphs: Paragraph[] }
export type Listing = { path: string; block_id: string; sha256: string; characters: number }
export type ArticleDoc = { schemaVersion: 1; article: ArticleSummary; blocks: Block[]; listings: Listing[]; details: string; media: Media[] }
export type SearchItem = { kind: 'toc' | 'article'; id: string; issueId: string; title: string; byline: string | null; articleIds?: string[]; reference?: string; status: string }
export type SearchDoc = { schemaVersion: 1; items: SearchItem[] }

export function dataUrl(relative: string): string {
  if (relative.startsWith('/') || relative.split('/').some(part => part === '..' || part === '.')) throw new Error('Unsafe data path')
  const root = new URL(`${import.meta.env.BASE_URL}data/`, document.baseURI)
  return new URL(relative.split('/').map(encodeURIComponent).join('/'), root).toString()
}
export function sourceUrl(relative: string): string { return dataUrl(`source/${relative}`) }
export function mediaUrl(media: Media, asset = false): string {
  return sourceUrl(`issues/${media.issue}/media/${media.resource}/${asset ? media.asset_name || media.resource : media.resource}`)
}
export async function load<T>(relative: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(dataUrl(relative), { signal })
  if (!response.ok) throw new Error(`Cannot load ${relative} (${response.status})`)
  const value = await response.json() as T & { schemaVersion?: number }
  if (value.schemaVersion !== 1) throw new Error(`Unsupported data version in ${relative}`)
  return value
}
export const dateOf = (id: string) => id.replace(/^maso-/, '')
export const articlePath = (id: string) => `/articles/${encodeURIComponent(id)}`
export const issuePath = (id: string) => `/issues/${encodeURIComponent(id)}`
export const tocPath = (issueId: string, entryId: string) => `${issuePath(issueId)}/toc/${encodeURIComponent(entryId)}`
export const mediaPath = (issueId: string, resource: string) => `${issuePath(issueId)}/media/${encodeURIComponent(resource)}`
export function normalize(value: string) { return value.normalize('NFKC').toLocaleLowerCase().replace(/\s+/g, ' ').trim() }
export function search(items: SearchItem[], query: string, issueId = ''): SearchItem[] {
  const q = normalize(query)
  if (!q) return []
  const articles = new Map(items.filter(item => item.kind === 'article').map(item => [item.id, item]))
  return items.filter(item => (!issueId || item.issueId === issueId) &&
    !(item.kind === 'toc' && item.articleIds?.some(id => normalize(articles.get(id)?.title || '') === normalize(item.title))) &&
    normalize(`${item.title} ${item.byline || ''} ${item.reference || ''} ${item.issueId}`).includes(q))
    .sort((a, b) => Number(normalize(b.title).startsWith(q)) - Number(normalize(a.title).startsWith(q)) ||
      a.issueId.localeCompare(b.issueId) || a.title.localeCompare(b.title, 'ko'))
}
