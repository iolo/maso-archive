import { useEffect, useMemo, useRef, useState, type ReactNode } from 'react'
import { Link, Route, Routes, useLocation, useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { ArrowLeft, ArrowRight, BookOpen, ChevronDown, ExternalLink, Menu, Moon, Search, Sun, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { type ArticleDoc, type ArticleSummary, type Block, type Catalog, type IssueDoc, type IssueSummary, type Media, type MediaDoc, type Run, type SearchDoc, type TocEntry, articlePath, dataUrl, dateOf, issuePath, load, mediaPath, mediaUrl, search, sourceUrl, tocPath } from './data'

import { ScanArticle, availabilityLabel, sectionPath, verificationLabel } from './ScanArticle'
import { TocImages } from './TocImages'
import type { TocGallery } from './data'

type Theme = 'system' | 'light' | 'dark'

function useDocument<T>(path: string | null) {
  const [state, setState] = useState<{ value?: T; error?: string; loading: boolean }>({ loading: true })
  const [retry, setRetry] = useState(0)
  useEffect(() => {
    if (!path) { setState({ loading: false }); return }
    const controller = new AbortController()
    setState({ loading: true })
    load<T>(path, controller.signal).then(value => setState({ value, loading: false }), error => {
      if (!controller.signal.aborted) setState({ error: String(error), loading: false })
    })
    return () => controller.abort()
  }, [path, retry])
  return { ...state, retry: () => setRetry(n => n + 1) }
}

function DataState({ loading, error, retry }: { loading: boolean; error?: string; retry: () => void }) {
  if (loading) return <p role="status" className="state">자료를 불러오는 중…</p>
  return <div role="alert" className="state"><p>자료를 열 수 없습니다. {error}</p><Button variant="outline" onClick={retry}>다시 시도</Button></div>
}

function ThemeControl() {
  const [theme, setTheme] = useState<Theme>(() => (localStorage.getItem('reading-room-theme') as Theme) || 'system')
  useEffect(() => {
    const media = window.matchMedia('(prefers-color-scheme: dark)')
    const apply = () => document.documentElement.classList.toggle('dark', theme === 'dark' || (theme === 'system' && media.matches))
    apply(); media.addEventListener('change', apply)
    return () => media.removeEventListener('change', apply)
  }, [theme])
  const change = (value: Theme) => { setTheme(value); localStorage.setItem('reading-room-theme', value) }
  return <label className="theme-control"><span className="sr-only">색상 모드</span>{theme === 'dark' ? <Moon size={17} /> : <Sun size={17} />}
    <select aria-label="색상 모드" value={theme} onChange={event => change(event.target.value as Theme)}>
      <option value="system">시스템</option><option value="light">밝게</option><option value="dark">어둡게</option>
    </select></label>
}

function Header({ issues, articles }: { issues: IssueSummary[]; articles: ArticleSummary[] }) {
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const years = [...new Set(issues.map(i => i.year))]
  const location = useLocation()
  const selected = issues.find(i => location.pathname === issuePath(i.id) || location.pathname.startsWith(issuePath(i.id) + '/'))?.id ||
    articles.find(a => articlePath(a.article_id) === location.pathname)?.issue_id || ''
  const selectedYear = issues.find(i => i.id === selected)?.year
  const [year, setYear] = useState<number | ''>(selectedYear ?? '')
  useEffect(() => { if (selectedYear !== undefined) setYear(selectedYear) }, [selectedYear])
  return <header className="site-header"><div className="header-inner">
    <Link className="brand" to="/" aria-label="마이크로소프트웨어 읽기실 홈"><BookOpen size={21} strokeWidth={1.8} /><span>마이크로소프트웨어 <em>읽기실</em></span></Link>
    <nav className="top-links" aria-label="주 메뉴"><Link to="/">호 목록</Link><Link to="/search">제목·글쓴이 검색</Link></nav>
    <div className="header-tools"><label className="header-select"><span className="sr-only">연도</span><select aria-label="연도" value={year} onChange={e => setYear(e.target.value === '' ? '' : Number(e.target.value))}><option value="">연도</option>{years.map(y => <option key={y} value={y}>{y || '날짜 미확인'}</option>)}</select><ChevronDown size={13} /></label>
      <label className="header-select"><span className="sr-only">월</span><select aria-label="월" value={selected && selectedYear === year ? selected : ''} onChange={e => e.target.value && navigate(issuePath(e.target.value))}><option value="">월</option>{issues.filter(i => i.year === year).map(i => <option value={i.id} key={i.id}>{i.nativeGroup ? i.label : `${String(i.month).padStart(2, '0')}월`}</option>)}</select><ChevronDown size={13} /></label>
      <form className="header-search" role="search" onSubmit={e => { e.preventDefault(); navigate(`/search?q=${encodeURIComponent(query)}`) }}><label className="sr-only" htmlFor="header-query">제목·글쓴이 검색</label><Search size={15} /><input id="header-query" value={query} onChange={e => setQuery(e.target.value)} placeholder="제목·글쓴이 검색" /><button aria-label="검색" type="submit"><ArrowRight size={15} /></button></form>
      <ThemeControl />
    </div></div></header>
}

function TocList({ issue, selected }: { issue: IssueDoc; selected?: string }) {
  return <nav aria-label={`${issue.issue.label} 차례`} className="toc-list">
    <Link className="toc-home" to={issuePath(issue.issue.id)}>호 개요 <ArrowRight size={14} /></Link>
    {issue.toc.map(entry => <Link key={entry.id} className={'toc-entry' + (selected === entry.id ? ' active' : '')} style={{ paddingLeft: `${12 + Math.min(entry.depth, 5) * 14}px` }} to={tocPath(issue.issue.id, entry.id)} aria-current={selected === entry.id ? 'page' : undefined}>
      <span>{entry.title}</span>{entry.articleIds.length > 0 && <span className="toc-dot" aria-label="읽기 자료 있음" />}
    </Link>)}
    {issue.articles.length > 0 && <><div className="toc-section-label">읽기 자료</div>{issue.articles.map(article => <Link key={article.article_id} className="toc-entry" to={articlePath(article.article_id)}>{article.title}</Link>)}</>}
  </nav>
}

function Sidebar({ issue, selected }: { issue?: IssueDoc; selected?: string }) {
  const [open, setOpen] = useState(false)
  if (!issue) return null
  return <><button className="mobile-toc-toggle" aria-expanded={open} onClick={() => setOpen(!open)}><Menu size={18} /> {issue.issue.label} 차례 <ChevronDown size={15} /></button>
    <aside className={'left-sidebar' + (open ? ' mobile-open' : '')} aria-label="이 호의 차례"><div className="sidebar-title">{issue.issue.label} · 차례</div><TocList issue={issue} selected={selected} /></aside></>
}

function ContextAside({ issue, article }: { issue?: IssueDoc; article?: ArticleDoc }) {
  const [open, setOpen] = useState(() => window.innerWidth >= 1000)
  if (!issue) return null
  return <aside className={'context-aside' + (open ? ' open' : '')} aria-label="관련 자료"><Button variant="ghost" className="aside-toggle" onClick={() => setOpen(!open)} aria-expanded={open}>{open ? '관련 자료 접기' : '관련 자료 보기'} <ChevronDown size={15} /></Button>
    {open && <div className="aside-content"><h2>같은 호의 글</h2><ul>{issue.articles.filter(a => a.article_id !== article?.article.article_id).slice(0, 10).map(a => <li key={a.article_id}><Link to={articlePath(a.article_id)}>{a.title}</Link><small>{statusLabel(a.status)}</small></li>)}</ul>
      {article && (article.article.referencePath || article.article.path) && <><h2>원본 자료</h2><a href={sourceUrl(article.article.referencePath || article.article.path.replace(/index\.html$/, 'reference.json'))} target="_blank" rel="noreferrer">참조 기록 <ExternalLink size={13} /></a></>}
    </div>}
  </aside>
}

function statusLabel(status: string) { return ({ prepared: 'CD 본문', normalized: '복원된 CD 본문', reference_with_gaps: '글자 판독 공백 있음', blocked: '글 경계 확인 필요', unavailable: '본문 없음', success: 'CD 본문', partial: '일부 확인 필요', readable: '스캔 · 읽기 가능', 'image-only': '스캔만 있음', failed: '복원 시도 실패', unresolved: '복원 상태 미확인' } as Record<string, string>)[status] || status }

export function IssueCover({ issue, compact = false }: { issue: IssueSummary; compact?: boolean }) {
  const [failedPath, setFailedPath] = useState<string | null>(null)
  const cover = issue.cover
  return <div className={'cover-frame ' + (compact ? 'cover-thumb' : 'cover-full')}>
    {cover && failedPath !== cover.path ? <img src={dataUrl(cover.path)} width={cover.width} height={cover.height}
      alt={compact ? '' : `${issue.label} 표지`} loading={compact ? 'lazy' : 'eager'} decoding="async"
      onError={() => setFailedPath(cover.path)} /> : <div className="cover-empty" role="img" aria-label="표지 이미지 없음">
      <span>{issue.label}</span><strong>표지 이미지 없음</strong></div>}
  </div>
}

function Bookshelf({ catalog }: { catalog: Catalog }) {
  const groups = [...new Set(catalog.issues.map(i => i.year))]
  return <div className="bookshelf page-content"><div className="page-heading"><p className="eyebrow">월간 마이크로소프트웨어</p><h1>호 목록</h1><p>도서관 차례, CD1·CD2·CD3 전사 자료와 스캔 복원 글을 찾아보세요. CD2·CD3 묶음은 CD 날짜 표기이며 종이 잡지의 발행호와 대조 전입니다.</p></div>
    {catalog.tocGallery && <p><Link to="/toc-scans">차례 스캔 모음 <ArrowRight size={16} /></Link></p>}
    {catalog.sources && <p className="source-note">보충 글·원본 자료: {catalog.sources.filter(s => s.referencePath).map(s => <a key={s.disc} href={sourceUrl(s.referencePath!)} target="_blank" rel="noreferrer">{s.disc.toUpperCase()} 참조 자료 ↗ </a>)}</p>}
    {groups.map(year => <section key={year} className="year-section"><h2>{year || '날짜 미확인'}</h2><div className="issue-grid">{catalog.issues.filter(i => i.year === year).map(issue => <Link key={issue.id} className="issue-tile" to={issuePath(issue.id)}><IssueCover issue={issue} compact /><span className="issue-date">{issue.label}</span><strong>{issue.nativeGroup ? 'CD 날짜 묶음' : `${String(issue.month).padStart(2, '0')}월호`}</strong><span>{issue.textCount ? `읽기 자료 ${issue.textCount}편` : '차례만 있음'}</span><ArrowRight size={17} /></Link>)}</div></section>)}
  </div>
}

function IssueOverview({ issue }: { issue: IssueDoc }) {
  return <div className="page-content"><div className="page-heading"><p className="eyebrow">{issue.issue.label} · 월간 마이크로소프트웨어</p><h1>{issue.issue.nativeGroup ? issue.issue.label : `${issue.issue.year}년 ${issue.issue.month}월호`}</h1><p>차례 {issue.issue.tocCount}항목 · 읽기 자료 {issue.issue.textCount}편</p></div>
    {issue.issue.nativeGroup && <p className="notice">CD의 날짜 표기로 묶었습니다. 발행호 확인 전이며 도서관 차례 연결은 없습니다.</p>}
    <IssueCover issue={issue.issue} />
    <TocImages key={issue.issue.id} pages={issue.tocImages} label={issue.issue.label} />
    {issue.scanRestoration && <section aria-label="호 복원 및 검토 상태"><h2>호 복원 기록</h2>
      <p>본문 {issue.scanRestoration.counts.classified_articles}편 · 묶음 제목 {issue.scanRestoration.counts.group_headings} · 절 참조 {issue.scanRestoration.counts.section_references} · 분류 미해결 {issue.scanRestoration.counts.unresolved_eligibility}</p>
      <p>복원: {Object.entries(issue.scanRestoration.counts.restoration_availability).map(([state, count]) => `${availabilityLabel(state as Parameters<typeof availabilityLabel>[0])} ${count}`).join(' · ')}</p>
      <p>검토: {Object.entries(issue.scanRestoration.counts.verification).map(([state, count]) => `${verificationLabel(state as Parameters<typeof verificationLabel>[0])} ${count}`).join(' · ')}</p>
      <p>판독 불확실성과 수동 비트맵 교정 대기는 각 글의 교정 기록에 남아 있습니다.</p>
    </section>}
    <section className="article-index"><h2>읽기 자료</h2>{issue.articles.length ? <ul>{issue.articles.map(article => <li key={article.article_id}><Link to={articlePath(article.article_id)}>{article.title}</Link><span>{article.sourceKind === 'scan' && article.availability ? availabilityLabel(article.availability) : statusLabel(article.status)}{article.verification && ` · ${verificationLabel(article.verification)}`}</span></li>)}</ul> : <p>이 호의 읽기 본문은 준비되지 않았습니다. 왼쪽 차례의 제목은 볼 수 있습니다.</p>}</section>
  </div>
}

export function TocDetail({ issue, id }: { issue: IssueDoc; id: string }) {
  const entry = issue.toc.find(e => e.id === id)
  if (!entry) return <NotFound />
  return <div className="page-content"><p className="eyebrow">{issue.issue.label} · 차례 항목</p><h1>{entry.title}</h1><p className="metadata">{entry.page !== null && `${entry.page}쪽`}{entry.byline && ` · ${entry.byline}`}</p>
    {entry.sectionRef ? <><p>이 항목은 아래 글 안의 절입니다.</p><Link to={sectionPath(entry.sectionRef.articleId, entry.sectionRef.blockId)}>{entry.title} 본문으로 <ArrowRight size={16} /></Link></> : entry.restorationKind === 'group-heading' ? <><p>여러 글을 묶는 차례 제목입니다.</p><ul>{issue.toc.filter(t => t.parentId === entry.id).map(t => <li key={t.id}><Link to={tocPath(issue.issue.id, t.id)}>{t.title}</Link></li>)}</ul></> : entry.articleIds.length ? <><h2>연결된 읽기 자료</h2><ul>{entry.articleIds.map(id => { const article = issue.articles.find(a => a.article_id === id); return article && <li key={id}><Link to={articlePath(id)}>{article.title} <ArrowRight size={16} /></Link></li> })}</ul></> : <p className="notice">이 차례 항목에 확인된 읽기 자료 연결이 없습니다. 차례만으로 원문 부재를 단정할 수 없습니다.</p>}
    <p className="source-note">자료마다 출처와 검토 범위가 다릅니다. 연결된 글에서 확인 상태를 확인하세요.</p></div>
}

export function RenderRun({ run, issueId, media }: { run: Run; issueId: string; media: Media[] }) {
  if (run.type === 'media') {
    const item = media.find(m => m.resource === run.resource)
    return <Link className="inline-media" to={mediaPath(issueId, run.resource)}>{item?.asset_name ? <img src={mediaUrl(item, true)} alt={run.resource} loading="lazy" /> : `[이미지: ${run.resource}]`}</Link>
  }
  let content: ReactNode = run.text
  if (run.marks?.includes('bold')) content = <strong>{content}</strong>
  if (run.marks?.includes('italic')) content = <em>{content}</em>
  if (run.marks?.includes('underline')) content = <u>{content}</u>
  if (run.marks?.includes('strike')) content = <s>{content}</s>
  if (run.marks?.includes('small_caps')) content = <span style={{ fontVariant: 'small-caps' }}>{content}</span>
  return <>{content}</>
}

function RenderBlock({ block, doc, number }: { block: Block; doc: ArticleDoc; number: number }) {
  const issueId = doc.article.issue_id
  const listing = doc.listings.find(l => l.block_id === block.id)
  if (!['title', 'issue_label', 'byline', 'paragraph', 'heading', 'code', 'caption', 'figure', 'table', 'spacing', 'unresolved'].includes(block.type))
    return <p role="alert" className="notice">지원하지 않는 본문 형식: {block.type}</p>
  const contents = block.paragraphs.map(p => <span key={p.id} id={p.id} className="paragraph">{p.runs.map((r, n) => <RenderRun key={n} run={r} issueId={issueId} media={doc.media} />)}{p.terminated !== false && '\n'}</span>)
  if (block.preformatted || block.type === 'code') return <section className="code-section" id={block.id}>
    {listing && <a className="download-link" href={sourceUrl(doc.article.path.replace(/index\.html$/, listing.path))} download>목록 {doc.listings.indexOf(listing) + 1} · 텍스트 내려받기 <ArrowRight size={15} /></a>}
    <pre><code>{contents}</code></pre></section>
  if (block.type === 'spacing') return <div className="spacing" aria-hidden="true" />
  if (block.type === 'heading' || block.type === 'title') {
    const Heading: 'h2' | 'h3' | 'h4' = block.heading_level === 3 ? 'h4' : block.heading_level === 2 ? 'h3' : 'h2'
    return <Heading className="article-heading" id={`block-${number}`}>{contents}</Heading>
  }
  if (block.type === 'caption') return <figcaption id={`block-${number}`}>{contents}</figcaption>
  return <p className={'article-paragraph block-' + block.type} id={`block-${number}`}>{contents}</p>
}

function ArticleView({ doc }: { doc: ArticleDoc }) {
  const article = doc.article
  const first = doc.media[0]
  const [params] = useSearchParams()
  const paragraphId = params.get('p')
  const blockId = params.get('block')
  useEffect(() => {
    if (!paragraphId && !blockId) return
    const frame = requestAnimationFrame(() => document.getElementById(paragraphId || blockId!)?.scrollIntoView())
    return () => cancelAnimationFrame(frame)
  }, [paragraphId, blockId, article.article_id])
  if (doc.scan) return <ScanArticle key={article.article_id} doc={doc} />
  return <article className="article-view page-content"><div className="page-heading"><p className="eyebrow"><Link to={issuePath(article.issue_id)}>{dateOf(article.issue_id)}</Link> · {article.sourceKind === 'scan' && article.availability ? availabilityLabel(article.availability) : statusLabel(article.status)}</p><h1>{article.title}</h1><p className="metadata">{article.byline && `${article.byline} · `}{article.page !== null && `${article.page}쪽 · `}CD 참조 {article.reference} · 종이 잡지 대조 전</p></div>
    {article.status === 'reference_with_gaps' && <p className="notice">이 글에는 판독하지 못한 글자가 표시되어 있습니다. ⟦…⟧ 표시는 원문 글자가 아니므로 종이 잡지나 스캔으로 확인해 주세요.</p>}
    {article.status === 'partial' && <p className="notice">본문·이미지·첨부 또는 CD 표기에 확인이 필요한 부분이 있습니다. 아래 출처와 확인 상태를 참고해 주세요.</p>}
    {article.status === 'normalized' && <p className="notice">CD의 일반 서식을 정리해 읽기 쉽게 표시했습니다. 종이 잡지 대조는 아직 끝나지 않았습니다.</p>}
    {article.status === 'blocked' ? <p>본문의 글 경계를 확인해야 합니다. 출처 기록은 보존되어 있습니다.</p> : <>
      <div className="article-actions"><a href={sourceUrl(article.text!)} download>전체 글 UTF-8 텍스트 <ArrowRight size={15} /></a><a href={sourceUrl(article.paragraphsPath || article.path.replace(/index\.html$/, 'paragraphs.json'))} target="_blank" rel="noreferrer">문단 위치</a>{first && <Link to={mediaPath(article.issue_id, first.resource)}>첫 이미지</Link>}</div>
      {(doc.attachments?.length || doc.listings.some(l => !l.block_id)) ? <section><h2>코드·첨부 자료</h2><ul>{doc.listings.filter(l => !l.block_id).map(l => <li key={l.path}><a href={sourceUrl(article.path.replace(/index\.html$/, l.path))} download>UTF-8 · {l.path}</a></li>)}{doc.attachments?.map(a => <li key={a.path}><a href={sourceUrl(a.path)} download>{a.source_path}</a></li>)}</ul></section> : null}
      {!!doc.relatedSources?.length && <section><h2>연결된 CD 자료</h2><ul>{doc.relatedSources.map(l => <li key={l.path}><a href={sourceUrl(l.path)} target="_blank" rel="noreferrer">{l.label}</a></li>)}</ul></section>}
      <div className="article-body">{doc.blocks.map((block, index) => <RenderBlock key={block.id} block={block} doc={doc} number={index + 1} />)}</div>
      {doc.media.length > 0 && <section className="article-media"><h2>이미지 자료</h2><ul>{doc.media.map(m => <li key={m.resource}><Link to={mediaPath(article.issue_id, m.resource)}>{m.resource}</Link> <small>{m.asset_name ? '보기 가능' : m.status === 'missing' ? '원본 없음' : '미리보기 없음'}</small></li>)}</ul></section>}
    </>}
    <details className="source-note"><summary>출처와 확인 상태</summary><p>이 글은 CD의 전사 자료입니다. 차이나 빈 글자는 종이 잡지 또는 스캔으로 확인해야 합니다.</p>{doc.details && <p>{doc.details}</p>}<a href={sourceUrl(article.referencePath || article.path.replace(/index\.html$/, 'reference.json'))} target="_blank" rel="noreferrer">참조 기록 열기</a></details>
  </article>
}

function MediaView({ issueId, media }: { issueId: string; media: Media }) {
  return <div className="page-content media-view"><p className="eyebrow"><Link to={issuePath(issueId)}>{dateOf(issueId)}</Link> · 이미지 자료</p><h1>{media.resource}</h1>{media.asset_name ? <img className="large-media" src={mediaUrl(media, true)} alt={media.resource} /> : <p className="notice">{media.status === 'missing' ? 'CD 원본 이미지가 없습니다.' : '미리보기를 만들지 못했습니다. 원본 파일을 내려받아 확인할 수 있습니다.'}</p>}
    <div className="article-actions">{media.originalPath !== null && <a href={mediaUrl(media)} download>원본 내려받기 <ArrowRight size={15} /></a>}{media.asset_name && <a href={mediaUrl(media, true)} download>보기 파일 내려받기</a>}</div>
    {media.conversion_note && <details className="source-note"><summary>변환 기록</summary><p>{media.conversion_note}</p></details>}
    <p className="source-note">이미지 속 글자는 자동 전사되지 않았습니다. 종이 잡지와 비교해 주세요.</p></div>
}

function SearchView({ catalog }: { catalog: Catalog }) {
  const [params, setParams] = useSearchParams()
  const query = params.get('q') || ''
  const selectedIssue = params.get('issue') || ''
  const [draft, setDraft] = useState(query)
  useEffect(() => setDraft(query), [query])
  const result = useDocument<SearchDoc>('search.json')
  const items = useMemo(() => search(result.value?.items || [], query, selectedIssue), [result.value, query, selectedIssue])
  return <div className="page-content search-view"><div className="page-heading"><p className="eyebrow">자료 찾기</p><h1>제목·글쓴이 검색</h1><p>차례와 읽기 자료의 제목, 글쓴이, 참조 번호를 찾습니다. 본문 전체 검색은 제공하지 않습니다.</p></div>
    <form className="search-form" onSubmit={e => { e.preventDefault(); setParams({ q: draft, ...(selectedIssue ? { issue: selectedIssue } : {}) }) }}><label htmlFor="search-query">검색어</label><div><input id="search-query" value={draft} onChange={e => setDraft(e.target.value)} placeholder="제목, 글쓴이 또는 참조 번호" /><Button type="submit">검색</Button></div></form>
    <label className="search-filter">호 필터 <select value={selectedIssue} onChange={e => setParams({ q: query, ...(e.target.value ? { issue: e.target.value } : {}) })}><option value="">모든 호</option>{catalog.issues.map(i => <option key={i.id} value={i.id}>{i.label}</option>)}</select></label>
    {result.loading || result.error ? <DataState loading={result.loading} error={result.error} retry={result.retry} /> : <section aria-live="polite" className="search-results"><h2>{query ? `${items.length}건` : '검색어를 입력하세요'}</h2>{query && items.length === 0 && <p>검색 결과가 없습니다.</p>}
      <ul>{items.map(item => <li key={item.kind + item.id}><span className="result-kind">{item.kind === 'toc' ? '차례' : item.sourceKind === 'scan' ? '스캔 복원' : 'CD 글'} · {dateOf(item.issueId)} · {item.kind === 'article' ? statusLabel(item.status) : item.status === 'linked' ? '읽기 자료 연결' : '연결 미확인'}</span><Link to={item.kind === 'article' ? articlePath(item.id) : tocPath(item.issueId, item.id)}>{item.title} <ArrowRight size={16} /></Link>{item.byline && <span>{item.byline}</span>}</li>)}</ul></section>}
  </div>
}

function NotFound() { return <div className="page-content"><h1>자료를 찾을 수 없습니다</h1><p>주소를 확인하거나 호 목록으로 돌아가세요.</p><Link to="/">호 목록 <ArrowRight size={16} /></Link></div> }

function TocGalleryView({ path }: { path?: string }) {
  const gallery = useDocument<TocGallery>(path || null)
  return <div className="page-content"><h1>차례 스캔 모음</h1><p>목록에 아직 등록되지 않은 호의 인쇄 차례입니다.</p>
    {!path ? <p>준비된 차례 스캔이 없습니다.</p> : gallery.loading || gallery.error ? <DataState loading={gallery.loading} error={gallery.error} retry={gallery.retry} /> :
      gallery.value?.sets.length ? gallery.value.sets.map(group => <section key={group.date}><h2>{group.date}</h2>{group.note && <p className="notice">{group.note}</p>}<TocImages pages={group.pages} label={group.date} /></section>) : <p>추가 차례 스캔이 없습니다.</p>}
  </div>
}

function RoutedPage({ catalog }: { catalog: Catalog }) {
  const params = useParams()
  const issueId = params.issueId || (params.articleId ? catalog.articles.find(a => a.article_id === params.articleId)?.issue_id : undefined)
  const issue = useDocument<IssueDoc>(issueId ? `issues/${dateOf(issueId)}.json` : null)
  const article = useDocument<ArticleDoc>(params.articleId ? `articles/${catalog.articles.find(a => a.article_id === params.articleId)?.reference || 'missing'}.json` : null)
  const media = useDocument<MediaDoc>(params.resource && issueId ? `media/${dateOf(issueId)}.json` : null)
  const location = useLocation()
  const focus = useRef<HTMLElement>(null)
  useEffect(() => {
    if (!new URLSearchParams(location.search).has('section')) {
      focus.current?.focus()
      window.scrollTo(0, 0)
    }
  }, [location.pathname, location.search])
  if (params.articleId && !issueId) return <NotFound />
  if (issueId && !catalog.issues.some(i => i.id === issueId)) return <NotFound />
  return <div className={'workspace' + (!issueId ? ' no-issue' : '')}>
    {issueId && (issue.value ? <Sidebar issue={issue.value} selected={params.entryId} /> : <aside className="left-sidebar"><DataState loading={issue.loading} error={issue.error} retry={issue.retry} /></aside>)}
    <main id="main" tabIndex={-1} ref={focus}>
      {!issueId ? <Bookshelf catalog={catalog} /> : issue.loading || issue.error ? <DataState loading={issue.loading} error={issue.error} retry={issue.retry} /> : !issue.value ? <NotFound /> :
      params.entryId ? <TocDetail issue={issue.value} id={params.entryId} /> :
      params.articleId ? article.loading || article.error ? <DataState loading={article.loading} error={article.error} retry={article.retry} /> : article.value ? <ArticleView doc={article.value} /> : <NotFound /> :
      params.resource ? media.loading || media.error ? <DataState loading={media.loading} error={media.error} retry={media.retry} /> : media.value?.items.find(m => m.resource === params.resource) ? <MediaView issueId={issueId} media={media.value.items.find(m => m.resource === params.resource)!} /> : <NotFound /> :
      <IssueOverview issue={issue.value} />}
    </main>
    {issue.value && <ContextAside issue={issue.value} article={article.value} />}
  </div>
}

export default function App() {
  const catalog = useDocument<Catalog>('catalog.json')
  return <div className="app-shell"><a className="skip-link" href="#main" onClick={event => { event.preventDefault(); document.getElementById('main')?.focus(); document.getElementById('main')?.scrollIntoView() }}>본문으로 건너뛰기</a><Header issues={catalog.value?.issues || []} articles={catalog.value?.articles || []} />
    {catalog.loading || catalog.error ? <main id="main"><DataState loading={catalog.loading} error={catalog.error} retry={catalog.retry} /></main> : catalog.value && <Routes>
      <Route path="/" element={<RoutedPage catalog={catalog.value} />} />
      <Route path="/issues/:issueId" element={<RoutedPage catalog={catalog.value} />} />
      <Route path="/issues/:issueId/toc/:entryId" element={<RoutedPage catalog={catalog.value} />} />
      <Route path="/issues/:issueId/media/:resource" element={<RoutedPage catalog={catalog.value} />} />
      <Route path="/articles/:articleId" element={<RoutedPage catalog={catalog.value} />} />
      <Route path="/search" element={<main id="main"><SearchView catalog={catalog.value} /></main>} />
      <Route path="/toc-scans" element={<main id="main"><TocGalleryView path={catalog.value.tocGallery} /></main>} />
      <Route path="*" element={<main id="main"><NotFound /></main>} />
    </Routes>}
    <footer className="site-footer"><span>월간 마이크로소프트웨어 · 개인 열람 참고 자료</span><span>자료별 출처와 검토 범위를 확인하세요</span></footer>
  </div>
}
