import { useEffect, useRef, useState } from 'react'
import { dataUrl, type TocImage } from './data'

function ScanImage({ image, label, lazy = false }: { image: TocImage['preview']; label: string; lazy?: boolean }) {
  const [failed, setFailed] = useState(false)
  return failed ? <p role="status">차례 이미지를 불러오지 못했습니다. 목록의 차례는 계속 읽을 수 있습니다.</p> :
    <img src={dataUrl(image.path)} width={image.width} height={image.height} alt={label}
      loading={lazy ? 'lazy' : 'eager'} decoding="async" onError={() => setFailed(true)} />
}

export function TocImages({ pages, label }: { pages?: TocImage[]; label: string }) {
  const [selected, setSelected] = useState<number | null>(null)
  const [zoom, setZoom] = useState(false)
  const dialog = useRef<HTMLDialogElement>(null)
  useEffect(() => {
    if (selected !== null && !dialog.current?.open) dialog.current?.showModal()
  }, [selected])
  const close = () => { dialog.current?.close(); setSelected(null); setZoom(false) }
  const select = (index: number) => { setSelected(index); setZoom(false) }
  if (pages === undefined) return null // Older datasets have no scan collection.
  if (!pages.length) return <section className="toc-scans"><h2>인쇄 차례</h2><p>이 호의 기증 차례 스캔은 없습니다. 목록의 차례는 계속 읽을 수 있습니다.</p></section>
  const page = selected === null ? null : pages[selected]
  return <section className="toc-scans" aria-label={`${label} 인쇄 차례`}><h2>인쇄 차례</h2>
    <p>이미지를 선택하면 크게 볼 수 있습니다.</p>
    <div className="toc-scan-previews">{pages.map((p, i) => <button key={p.sequence} onClick={() => select(i)} aria-label={`${label} 차례 ${i + 1} / ${pages.length} 보기`}>
      <ScanImage key={p.preview.path} image={p.preview} label={`${label} 인쇄 차례 ${i + 1} / ${pages.length}`} lazy />
      <span>{i + 1} / {pages.length}{p.printedPage !== undefined && ` · 인쇄 ${p.printedPage}쪽`}</span>
    </button>)}</div>
    <dialog ref={dialog} className="toc-scan-dialog" aria-label={`${label} 인쇄 차례 크게 보기`}
      onCancel={close} onKeyDown={event => {
        if (event.target instanceof HTMLSelectElement) return
        if (event.key === 'ArrowLeft' && selected !== null && selected > 0) { event.preventDefault(); select(selected - 1) }
        if (event.key === 'ArrowRight' && selected !== null && selected < pages.length - 1) { event.preventDefault(); select(selected + 1) }
      }}>
      {page && <><div className="toc-scan-controls"><strong>{label} · 인쇄 차례</strong>
        <button onClick={() => select(selected! - 1)} disabled={selected === 0}>이전</button>
        <label>페이지 <select aria-label="차례 페이지" value={selected!} onChange={e => select(Number(e.target.value))}>
          {pages.map((p, i) => <option key={p.sequence} value={i}>{i + 1} / {pages.length}</option>)}
        </select></label>
        <button onClick={() => select(selected! + 1)} disabled={selected === pages.length - 1}>다음</button>
        <button aria-pressed={zoom} onClick={() => setZoom(!zoom)}>{zoom ? '화면에 맞춤' : '확대'}</button>
        <button onClick={close} autoFocus>닫기</button></div>
        <div className={`toc-scan-readable${zoom ? ' zoomed' : ''}`} tabIndex={0} aria-label="차례 이미지 스크롤 영역">
          <ScanImage key={page.readable.path} image={page.readable} label={`${label} 인쇄 차례 ${selected! + 1} / ${pages.length}`} />
        </div></>}
    </dialog>
  </section>
}
