import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { Button } from './components/ui/button'
import { type ArticleDoc, type Catalog, articlePath, issuePath } from './data'
import { articleSource, emptyReviews, filterReviewArticles, noteRoute, readReviews, reviewKey, reviewLabels, reviewState, saveReview, type ReviewNote, type ReviewStatus } from './reviews'

function useReviews() {
  const [state, setState] = useState(() => {
    try { return { file: readReviews(), error: '' } } catch { return { file: emptyReviews(), error: '브라우저 검토 기록을 읽을 수 없습니다. 저장소 설정이나 기존 기록을 확인하세요.' } }
  })
  useEffect(() => {
    const update = () => { try { setState({ file: readReviews(), error: '' }) } catch { setState(s => ({ ...s, error: '브라우저 검토 기록을 읽을 수 없습니다.' })) } }
    window.addEventListener('storage', update); window.addEventListener('maso-reviews-changed', update)
    return () => { window.removeEventListener('storage', update); window.removeEventListener('maso-reviews-changed', update) }
  }, [])
  return state
}

function downloadReviews(notes: ReviewNote[]) {
  const blob = new Blob([JSON.stringify({ ...emptyReviews(), exportedAt: new Date().toISOString(), notes }, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a'); link.href = url; link.download = `maso-review-${new Date().toISOString().slice(0, 10)}.json`
  link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000)
}

export function ReviewNotebook({ doc }: { doc: ArticleDoc }) {
  const [params] = useSearchParams()
  const requested = params.get('region')
  const regionId = doc.scan?.regions.some(r => r.id === requested) ? requested : null
  return <NoteEditor key={reviewKey(doc.article.article_id, regionId)} doc={doc} regionId={regionId} />
}

function NoteEditor({ doc, regionId }: { doc: ArticleDoc; regionId: string | null }) {
  const { file, error } = useReviews()
  const article = doc.article
  const existing = file.notes.find(n => reviewKey(n.articleId, n.regionId) === reviewKey(article.article_id, regionId))
  const stale = !!existing && (existing.textSha256 !== article.text_sha256 || existing.packageSha256 !== (doc.scan?.packageSha256 || null))
  const [reviewer, setReviewer] = useState(existing?.reviewer || file.notes.at(-1)?.reviewer || '')
  const [status, setStatus] = useState<ReviewStatus>(stale ? 'in-progress' : existing?.status || 'in-progress')
  const [note, setNote] = useState(existing?.note || '')
  const [message, setMessage] = useState('')
  const [failed, setFailed] = useState(false)
  const [dirty, setDirty] = useState(false)
  useEffect(() => {
    const warn = (event: BeforeUnloadEvent) => { if (dirty) { event.preventDefault(); event.returnValue = '' } }
    window.addEventListener('beforeunload', warn)
    return () => window.removeEventListener('beforeunload', warn)
  }, [dirty])
  const record = (): ReviewNote => ({ articleId: article.article_id, issueId: article.issue_id, title: article.title, regionId,
    source: articleSource(article), textSha256: article.text_sha256, packageSha256: doc.scan?.packageSha256 || null,
    route: noteRoute(article.article_id, regionId), reviewer: reviewer.trim(), status, note, updatedAt: new Date().toISOString() })
  const persist = (patch: Partial<ReviewNote> = {}) => {
    try { saveReview({ ...record(), ...patch }); setDirty(false); setFailed(false); setMessage('이 브라우저에 저장했습니다.') }
    catch { setDirty(true); setFailed(true); setMessage('저장하지 못했습니다. 현재 메모 내려받기로 보관하세요.') }
  }
  return <details className="volunteer-notebook"><summary>검토 메모 · {regionId ? '이 스캔 영역' : '글 전체'}{existing ? ` · ${reviewLabels[existing.status]}` : ''}{dirty ? ' · 저장 전' : ''}</summary>
    <p>입력하면 이 브라우저에 자동 저장됩니다. 제출하려면 JSON을 내려받아 담당자에게 전달하세요. 원본의 검토·승인 상태는 바뀌지 않습니다.</p>
    {error && <p role="alert">{error}</p>}
    {stale && <p role="alert">저장된 메모 이후 복원 자료가 바뀌었습니다. 원문을 다시 확인하세요.</p>}
    <form onSubmit={event => { event.preventDefault(); persist() }}>
      <div className="review-fields"><label>검토자 이름 (선택)<input value={reviewer} maxLength={120} onChange={e => { setReviewer(e.target.value); persist({ reviewer: e.target.value.trim() }) }} /></label>
        <label>내 검토 상태<select value={status} onChange={e => { setStatus(e.target.value as ReviewStatus); persist({ status: e.target.value as ReviewStatus }) }}>{Object.entries(reviewLabels).map(([key, label]) => <option key={key} value={key}>{label}</option>)}</select></label></div>
      <label>발견한 문제·수정 제안<textarea rows={4} value={note} maxLength={20000} onChange={e => { setNote(e.target.value); persist({ note: e.target.value }) }} placeholder="쪽·문단·코드 줄, 현재 내용, 수정 제안과 근거를 적어 주세요." /></label>
      <div className="review-actions"><Button type="submit">메모 저장</Button><Button type="button" variant="outline" onClick={() => downloadReviews([record()])}>현재 메모 내려받기</Button><Link to="/review">검토 목록 →</Link></div>
      <p role={failed ? 'alert' : 'status'}>{message || (dirty ? '이동하기 전에 메모를 저장하세요.' : '')}</p>
    </form>
  </details>
}

export function ReviewQueue({ catalog }: { catalog: Catalog }) {
  const { file, error } = useReviews()
  const [params, setParams] = useSearchParams()
  const filters = { source: params.get('source') || '', issue: params.get('issue') || '', status: params.get('status') || '', query: params.get('q') || '' }
  const [limit, setLimit] = useState(60)
  const update = (key: string, value: string) => { const next = new URLSearchParams(params); value ? next.set(key, value) : next.delete(key); if (key === 'source') next.delete('issue'); setParams(next, { replace: true }); setLimit(60) }
  const articles = filterReviewArticles(catalog.articles, file.notes, filters)
  const issues = catalog.issues.filter(i => catalog.articles.some(a => a.issue_id === i.id && (!filters.source || articleSource(a) === filters.source)))
  const scanArticles = catalog.articles.filter(a => a.sourceKind === 'scan')
  const scanIssues = new Set(scanArticles.map(a => a.issue_id)).size
  const names = new Map(catalog.issues.map(i => [i.id, i.label]))
  return <div className="page-content review-queue"><div className="page-heading"><p className="eyebrow">월간 마이크로소프트웨어 · 자원봉사 검토</p><h1>자원봉사 검토</h1>
    <p>PDF 복원 {scanIssues}개 호 · {scanArticles.length.toLocaleString()}편 / CD1·CD2·CD3 {(catalog.articles.length - scanArticles.length).toLocaleString()}편</p></div>
    <div className="review-intro"><p>글을 열어 원문과 대조하고, <strong>검토 메모</strong>에 수정할 곳을 기록하세요. PDF는 쪽·영역별 스캔을, CD는 복원 본문과 첨부 자료를 제공합니다.</p>
      <p>메모는 이 브라우저에만 보관됩니다. 작업 후 JSON을 내려받아 담당자에게 전달하세요. ‘대조 완료’는 개인 기록이며 공식 승인이 아닙니다.</p>
      <div className="review-actions"><Button variant="outline" disabled={!file.notes.length || !!error} onClick={() => downloadReviews(file.notes)}>내 검토 기록 {file.notes.length}건 내려받기</Button><Link to="/">표지로 호 찾기 →</Link></div></div>
    {error && <p role="alert">{error}</p>}
    {!!file.notes.length && <details className="saved-review-notes"><summary>내 검토 메모 {file.notes.length}건 · 이어서 보기</summary><ul>{[...file.notes].sort((a, b) => b.updatedAt.localeCompare(a.updatedAt)).map(n => <li key={reviewKey(n.articleId, n.regionId)}><Link to={n.route}>{n.title} · {n.regionId ? `영역 ${n.regionId}` : '글 전체'}</Link><small>{reviewLabels[n.status]} · {n.reviewer || '이름 없음'} · {new Date(n.updatedAt).toLocaleDateString('ko-KR')}</small></li>)}</ul></details>}
    <div className="review-filters"><label>자료<select value={filters.source} onChange={e => update('source', e.target.value)}><option value="">PDF + 모든 CD</option>{['PDF', 'CD1', 'CD2', 'CD3'].map(s => <option key={s}>{s}</option>)}</select></label>
      <label>호 / 날짜 묶음<select value={filters.issue} onChange={e => update('issue', e.target.value)}><option value="">모든 호</option>{issues.map(i => <option key={i.id} value={i.id}>{i.label}{i.nativeGroup ? ` · ${i.disc?.toUpperCase()}` : ''}</option>)}</select></label>
      <label>내 검토 상태<select value={filters.status} onChange={e => update('status', e.target.value)}><option value="">모든 상태</option><option value="pending">시작 전</option>{Object.entries(reviewLabels).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select></label>
      <label>제목·글쓴이<input type="search" value={filters.query} onChange={e => update('q', e.target.value)} placeholder="검색어" /></label></div>
    <p role="status">{articles.length.toLocaleString()}편 · 글 전체 대조를 완료해야 ‘대조 완료’로 분류됩니다.</p>
    <ul className="review-list">{articles.slice(0, limit).map(a => { const state = reviewState(a, file.notes); return <li key={a.article_id}><div><span className="eyebrow">{articleSource(a)} · <Link to={issuePath(a.issue_id)}>{names.get(a.issue_id)}</Link>{a.page !== null ? ` · ${a.page}쪽` : ''}</span><Link className="review-title" to={articlePath(a.article_id)}>{a.title}</Link><small>{a.byline || '글쓴이 미표기'}{!a.text ? ' · 본문 없음 / 기록 확인' : ''}{['partial', 'reference_with_gaps'].includes(a.status) ? ' · 일부 확인 필요' : ''}</small></div><Link className="review-open" to={articlePath(a.article_id)}><span>{state === 'pending' ? '시작 전' : reviewLabels[state]}</span><span>검토하기 →</span></Link></li> })}</ul>
    {!articles.length && <p>조건에 맞는 글이 없습니다. <button type="button" onClick={() => { setParams({}); setLimit(60) }}>필터 초기화</button></p>}
    {articles.length > limit && <Button variant="outline" onClick={() => setLimit(n => n + 60)}>다음 60편 보기</Button>}
  </div>
}
