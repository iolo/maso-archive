/** Invented display fixtures only; excluded from the application bundle. */
import type { ArticleDoc, Availability, Catalog, IssueDoc } from './data'

export const syntheticScanSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="300"><rect width="600" height="300" fill="white"/><text x="20" y="80" font-size="28">Synthetic scan evidence</text></svg>'
export function scanFixture(availability: Availability): ArticleDoc {
  const id = `scan-synthetic-${availability}`
  const readable = availability === 'readable' || availability === 'partial'
  const hasImage = readable || availability === 'image-only'
  const asset = { path: 'synthetic/scan.svg', sha256: '0'.repeat(64), bytes: syntheticScanSvg.length }
  return {
    schemaVersion: 3,
    article: { reference: id, article_id: id, issue_id: 'maso-1900-01', title: `Synthetic ${availability}`, byline: null, page: null,
      status: availability, sourceKind: 'scan', availability, verification: 'unreviewed', path: '', text: null,
      paragraphs: readable ? 2 : 0, listings: 0, image_occurrences: 0, resources: [], text_sha256: null },
    blocks: readable ? [
      { id: 'prose', scanBlockId: 'prose', type: 'paragraph', preformatted: false, regionIds: ['r1'], paragraphs: [{ id: 'p1', terminated: false, runs: [{ type: 'text', text: 'Invented first paragraph.\n\nInvented second paragraph.' }] }] },
      { id: 'code', scanBlockId: 'code', type: 'code', preformatted: true, regionIds: ['r1'], paragraphs: [{ id: 'p2', terminated: false, runs: [{ type: 'text', text: '  10 PRINT "<tag>&"\n\t20 END  \n' }] }] },
    ] : [],
    listings: [], media: [], details: 'Synthetic display case, not a restored magazine article.',
    scan: { packagePath: '', packageSha256: '', source: { id: 'synthetic', path: '', sha256: '', bytes: 0 }, coordinates: 'upright-normalized-top-left',
      pages: [{ pdf_index: 0, pdf_page: 1, printed_page: null, width_pt: 600, height_pt: 300, rotation: 0, MediaBox: [0, 0, 600, 300], CropBox: [0, 0, 600, 300], pdf_to_upright_normalized: [1 / 600, 0, 0, -1 / 300, 0, 1] }],
      regions: hasImage ? [{ id: 'r1', pdf_index: 0, kind: 'prose', bbox: [0, 0, 1, 1], notes: 'Invented fixture', asset }] : [],
      excludedRegions: [], contentOrder: [], figures: [], availability,
      verification: { status: 'unreviewed', reviewed_region_ids: [], evidence: [], uncertainties: [] },
      gaps: availability === 'partial' ? ['Synthetic missing passage remains marked ⟦…⟧.'] : [], relationships: [], downloads: [], corrections: [], reviewRecords: [] },
  }
}
export const scanFixtures = ['partial', 'image-only', 'failed'].map(s => scanFixture(s as Availability))
export const syntheticIssue = { id: 'maso-1900-01', year: 1900, month: 1, label: 'Synthetic fixtures', articleCount: 3, textCount: 1, tocCount: 0, cover: null }
export const fixtureCatalog: Catalog = { schemaVersion: 3, issues: [syntheticIssue], articles: scanFixtures.map(d => d.article) }
export const fixtureIssue: IssueDoc = { schemaVersion: 3, issue: syntheticIssue, articles: fixtureCatalog.articles, toc: [] }
