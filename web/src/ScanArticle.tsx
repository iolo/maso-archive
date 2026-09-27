import { useEffect, useRef } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { type ArticleDoc, type Availability, type Block, type ScanData, type VerificationStatus, articlePath, dateOf, issuePath, sourceUrl, tocPath } from './data'

export const availabilityLabel = (state: Availability) => ({ readable: '읽기 가능', partial: '일부 복원', 'image-only': '스캔만 있음', failed: '복원 시도 실패', unresolved: '복원 상태 미확인' })[state]
export const verificationLabel = (state: VerificationStatus) => ({ unreviewed: '미검토', 'sample-reviewed': '범위를 정해 검토', 'fully-reviewed': '전체 검토' })[state]
export const regionPath = (articleId: string, regionId: string) => `${articlePath(articleId)}?region=${encodeURIComponent(regionId)}`
const downloadLabel = (path: string) => ({ 'article.txt': '전체 글 · UTF-8', 'listing.txt': '코드 목록 · UTF-8', 'raw-ocr.zip': '교정 전 OCR와 스캔' })[path.split('/').pop()!] || path.split('/').pop()!
const blockText = (block: Block) => block.paragraphs.map(p => p.runs.map(r => r.type === 'text' ? r.text : '').join('') + (p.terminated ? '\n' : '')).join('')

export function ScanReview({ scan }: { scan: ScanData }) {
  return <section className="scan-review" aria-label="복원 및 검토 상태">
    <p><strong>복원: {availabilityLabel(scan.availability)}</strong><span>검토: {verificationLabel(scan.verification.status)}</span></p>
    {scan.availability === 'partial' && <p>일부 본문을 복원했습니다. 빠진 부분과 판독이 어려운 곳은 아래 기록과 스캔에서 확인하세요.</p>}
    {scan.availability === 'image-only' && <p>읽기 본문은 준비되지 않았습니다. 아래 스캔 영역을 열어 원문을 볼 수 있습니다.</p>}
    {scan.availability === 'failed' && <p>본문 복원 시도가 성공하지 못했습니다. 이 상태만으로 원문이 없다고 판단할 수 없습니다.</p>}
    {scan.availability === 'unresolved' && <p>본문 복원 상태를 아직 확인하지 못했습니다.</p>}
    {scan.gaps.length > 0 && <div className="notice"><strong>남아 있는 불확실성</strong><ul>{scan.gaps.map((gap, i) => <li key={i}>{gap}</li>)}</ul></div>}
    <details className="source-note"><summary>검토 범위와 교정 기록</summary>
      <p>검토한 스캔 영역: {scan.verification.reviewed_region_ids.join(', ') || '없음'}</p>
      {[...scan.verification.evidence, ...scan.verification.uncertainties].map((note, i) => <p key={i}>{note}</p>)}
      {scan.corrections.map(pin => <p key={pin.path}><a href={sourceUrl(pin.path)} target="_blank" rel="noreferrer">교정 기록 열기</a></p>)}
    </details>
  </section>
}

export function ScanArticle({ doc }: { doc: ArticleDoc }) {
  const scan = doc.scan!
  const article = doc.article
  const bylineBlock = doc.blocks.find(b => b.type === 'byline')
  const byline = bylineBlock ? blockText(bylineBlock) : article.byline
  const [params] = useSearchParams()
  const regionId = params.get('region')
  const region = scan.regions.find(r => r.id === regionId)
  const focus = useRef<HTMLElement>(null)
  useEffect(() => {
    if (regionId) { focus.current?.focus(); window.scrollTo(0, 0) }
  }, [regionId])
  const regionLinks = (ids: string[]) => <p className="scan-links">{ids.map(id => <Link key={id} to={regionPath(article.article_id, id)}>원문 스캔 {id}</Link>)}</p>
  if (regionId) {
    const page = scan.pages.find(p => p.pdf_index === region?.pdf_index)
    return <section className="page-content scan-evidence" tabIndex={-1} ref={focus}>
      <Link to={articlePath(article.article_id)}>← {article.title} 본문</Link>
      <h1>{region ? `원문 스캔 ${region.id}` : '스캔 영역을 찾을 수 없습니다'}</h1>
      {region && <><p>PDF {page?.pdf_page}쪽 · 인쇄 {page?.printed_page || '미상'}쪽 · {verificationLabel(scan.verification.status)}</p>
        {region.asset ? <><p><a href={sourceUrl(region.asset.path)} target="_blank" rel="noreferrer">원본 크기로 열기</a> · <a href={sourceUrl(region.asset.path)} download>스캔 내려받기</a></p>
          <div className="scan-image-scroll"><img src={sourceUrl(region.asset.path)} alt={`${article.title} 원문 영역 ${region.id}`} /></div></> : <p className="notice">이 영역의 스캔 이미지는 준비되지 않았습니다.</p>}
      </>}
    </section>
  }
  const readable = scan.availability === 'readable' || scan.availability === 'partial'
  return <article className="article-view page-content scan-article">
    <div className="page-heading"><p className="eyebrow"><Link to={issuePath(article.issue_id)}>{dateOf(article.issue_id)}</Link> · 스캔 복원</p>
      <h1>{article.title}</h1><p className="metadata">{byline}{article.page !== null && ` · ${article.page}쪽`}</p>
      {article.tocEntryId && <Link to={tocPath(article.issue_id, article.tocEntryId)}>차례 항목으로</Link>}
    </div>
    <ScanReview scan={scan} />
    <nav className="article-actions" aria-label="스캔 글 자료">
      {scan.downloads.map(pin => <a key={pin.path} href={sourceUrl(pin.path)} download>{downloadLabel(pin.path)}</a>)}
      {article.path && <a href={sourceUrl(article.path)} target="_blank" rel="noreferrer">독립형 복원본</a>}
      <a href="#scan-regions" onClick={e => { e.preventDefault(); document.getElementById('scan-regions')?.scrollIntoView() }}>스캔 영역 목록</a>
    </nav>
    {readable && <div className="article-body">{doc.blocks.map(block => {
      if (block.type === 'spacing' || block.type === 'title' || block.type === 'byline') return null
      if (block.scanFigureId) {
        const figure = scan.figures.find(f => f.id === block.scanFigureId)
        if (!figure) return null
        const image = `${scan.packagePath.replace(/article\.json$/, '')}${figure.asset.path}`
        return <figure key={block.id} id={block.id} className="scan-figure">
          <Link to={regionPath(article.article_id, figure.region_ids[0])}><img src={sourceUrl(image)} loading="lazy" alt={figure.caption || `${article.title} 원문 그림`} /></Link>
          {figure.caption && <figcaption>{figure.caption}</figcaption>}{regionLinks(figure.region_ids)}
        </figure>
      }
      const text = blockText(block)
      return <section key={block.id} id={block.id} className={block.preformatted ? 'code-section' : 'scan-text'} data-scan-block={block.scanBlockId}>
        {block.preformatted ? <pre><code>{text}</code></pre> : block.type === 'heading' ? <h2>{text}</h2> : text.split('\n\n').map((p, i) => <p key={i} className="article-paragraph">{p}</p>)}
        {regionLinks(block.regionIds || [])}
      </section>
    })}</div>}
    <section id="scan-regions" className="scan-region-list"><h2>원문 스캔 영역</h2>
      <p>영역을 선택하면 해당 스캔을 불러옵니다. 인쇄 쪽수와 PDF 쪽수는 다를 수 있습니다.</p>
      {scan.regions.length ? <ul>{scan.regions.map(r => { const p = scan.pages.find(p => p.pdf_index === r.pdf_index); return <li key={r.id}>
        <Link to={regionPath(article.article_id, r.id)}>{r.id} · 인쇄 {p?.printed_page || '미상'}쪽 / PDF {p?.pdf_page}쪽</Link>{!r.asset && ' · 이미지 없음'}
      </li> })}</ul> : <p>확인된 스캔 영역이 없습니다.</p>}
    </section>
    <details className="source-note"><summary>출처 기록</summary><p>스캔을 바탕으로 복원한 글입니다. 교정 전 OCR와 교정 내용은 별도로 보존합니다.</p>
      {scan.packagePath && <a href={sourceUrl(scan.packagePath)} target="_blank" rel="noreferrer">기사·스캔 기록 열기</a>}
    </details>
  </article>
}
