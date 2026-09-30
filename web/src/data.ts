export type Availability = 'readable' | 'partial' | 'image-only' | 'failed' | 'unresolved'
export type VerificationStatus = 'unreviewed' | 'sample-reviewed' | 'fully-reviewed'
export type StaticVersion = 1 | 2 | 3
export type Status = Availability | 'prepared' | 'normalized' | 'reference_with_gaps' | 'blocked' | 'unavailable' | 'success' | 'partial'
export type Cover = { path: string; width: number; height: number; sha256: string }
export type TocImage = { sequence: number; printedPage?: number; preview: Cover & { bytes: number }; readable: Cover & { bytes: number } }
export type TocGallery = { schemaVersion: StaticVersion; sets: { date: string; pages: TocImage[]; note?: string }[] }
export type IssueSummary = { id: string; year: number; month: number; label: string; articleCount: number; textCount: number; tocCount: number; cover: Cover | null; disc?: string; nativeGroup?: boolean }
export type ArticleSummary = { reference: string; article_id: string; issue_id: string; title: string; byline: string | null; page: number | null; status: Status; path: string; text: string | null; paragraphs: number; listings: number; image_occurrences: number; resources: string[]; text_sha256: string | null; disc?: string; nativeReference?: string; referencePath?: string; paragraphsPath?: string; sourceKind?: 'scan'; tocEntryId?: string; availability?: Availability; verification?: VerificationStatus }
export type TocEntry = { id: string; parentId: string | null; depth: number; title: string; byline: string | null; page: number | null; kind: string; articleIds: string[]; restorationKind?: 'article' | 'group-heading' | 'section-reference'; sectionRef?: { articleId: string; blockId: string } }
export type IssueDoc = { schemaVersion: StaticVersion; issue: IssueSummary; toc: TocEntry[]; articles: ArticleSummary[]; tocImages?: TocImage[]; scanRestoration?: { counts: { classified_articles: number; group_headings: number; section_references: number; unresolved_eligibility: number; restoration_availability: Record<Availability, number>; verification: Record<VerificationStatus, number> } } }
export type Catalog = { schemaVersion: StaticVersion; issues: IssueSummary[]; articles: ArticleSummary[]; tocGallery?: string; sources?: { disc: string; referencePath?: string }[] }
export type Media = { issue: string; resource: string; status: 'available' | 'available_with_caveat' | 'deferred' | 'missing'; asset_name: string | null; original_sha256: string; conversion_note: string | null; originalPath?: string | null; previewPath?: string | null }
export type MediaDoc = { schemaVersion: StaticVersion; issueId: string; items: Media[] }
export type Run = { type: 'text'; text: string; marks?: string[] } | { type: 'media'; resource: string; marks?: string[]; media_id?: string; occurrence_id?: string; textMarker?: string }
export type Paragraph = { id: string; runs: Run[]; terminated?: boolean }
export type Block = { id: string; type: string; layout?: string; preformatted: boolean; heading_level?: number | null; caption_for?: string | null; paragraphs: Paragraph[]; scanBlockId?: string; scanFigureId?: string; regionIds?: string[] }
export type Listing = { path: string; block_id: string; sha256: string; characters: number }
export type ArticleDoc = { schemaVersion: StaticVersion; article: ArticleSummary; blocks: Block[]; listings: Listing[]; details: string; media: Media[]; attachments?: { path: string; source_path: string; sha256: string }[]; relatedSources?: { label: string; path: string }[]; scan?: ScanData }
export type SearchItem = { kind: 'toc' | 'article'; id: string; issueId: string; title: string; byline: string | null; articleIds?: string[]; reference?: string; status: string; sourceKind?: 'scan'; availability?: Availability; verification?: VerificationStatus }
export type SearchDoc = { schemaVersion: StaticVersion; items: SearchItem[] }

export function dataUrl(relative: string): string {
  if (relative.startsWith('/') || relative.split('/').some(part => part === '..' || part === '.')) throw new Error('Unsafe data path')
  const root = new URL(`${import.meta.env.BASE_URL}data/`, document.baseURI)
  return new URL(relative.split('/').map(encodeURIComponent).join('/'), root).toString()
}
export function sourceUrl(relative: string): string { return dataUrl(`source/${relative}`) }
export function mediaUrl(media: Media, asset = false): string {
  const path = asset ? media.previewPath : media.originalPath
  if (path === null) throw new Error('Media source unavailable')
  if (path) return sourceUrl(path)
  return sourceUrl(`issues/${media.issue}/media/${media.resource}/${asset ? media.asset_name || media.resource : media.resource}`)
}
export async function load<T>(relative: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(dataUrl(relative), { signal })
  if (!response.ok) throw new Error(`Cannot load ${relative} (${response.status})`)
  const value = await response.json() as T & { schemaVersion?: number }
  if (value.schemaVersion !== 1 && value.schemaVersion !== 2 && value.schemaVersion !== 3) throw new Error(`Unsupported data version in ${relative}`)
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

// Version 3 scan fields supplement the existing static reader contract.
// Asset/download pins are relative to data/source/. Figure pins retain package
// scope; source.path identifies the repository PDF input, not a download.
export type FilePin = { path: string; sha256: string; bytes: number }
export type ScanPage = { pdf_index: number; pdf_page: number; printed_page: string | null; width_pt: number; height_pt: number; rotation: number; MediaBox: number[]; CropBox: number[]; pdf_to_upright_normalized: number[] }
export type ScanRegion = { id: string; pdf_index: number; kind: string; bbox: number[]; notes: string; asset: FilePin | null }
export type ScanData = {
  packagePath: string; packageSha256: string; source: FilePin & { id: string }
  coordinates: 'upright-normalized-top-left'; pages: ScanPage[]; regions: ScanRegion[]
  excludedRegions: Omit<ScanRegion, 'asset'>[]
  contentOrder: { type: 'block' | 'figure'; id: string }[]
  figures: { id: string; region_ids: string[]; asset: FilePin; caption: string | null }[]
  availability: Availability
  verification: { status: VerificationStatus; reviewed_region_ids: string[]; evidence: string[]; uncertainties: string[] }
  gaps: string[]; relationships: []
  downloads: FilePin[]; corrections: FilePin[]; reviewRecords: FilePin[]
}
