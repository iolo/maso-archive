import { useEffect, useState } from 'react'
import { sourceUrl, type ArticleDoc } from './data'

export type CorrectionDocument = {
  regional_transcription?: Record<string, string>
  records?: { id: string; raw_ocr?: { path: string } | null; human_acceptance?: string }[]
  source_review_notes?: { region_id: string; note: string }[]
  text_review_items?: { region_id?: string; note?: string }[]
  unresolved_text?: { region_id?: string; note?: string }[]
  identity_map?: { kind: string; id: string; source_id: string; source_segment: string }[]
  segments?: { name: string; original_metadata?: { source_review_notes?: { region_id: string; note: string }[] } }[]
}

export function regionalReview(data: CorrectionDocument, regionId: string) {
  const identity = data.identity_map?.find(r => r.kind === 'region' && r.id === regionId)
  const original = identity && data.segments?.find(s => s.name === identity.source_segment)?.original_metadata
  const notes = [
    ...(data.source_review_notes || []).filter(r => r.region_id === regionId).map(r => r.note),
    ...(original?.source_review_notes || []).filter(r => r.region_id === identity?.source_id).map(r => r.note),
    ...(data.text_review_items || []).filter(r => r.region_id === regionId).map(r => r.note),
  ].filter((n): n is string => typeof n === 'string')
  return {
    text: data.regional_transcription?.[regionId],
    record: data.records?.find(r => r.id === regionId),
    notes: [...new Set(notes)],
    uncertainties: [...new Set((data.unresolved_text || []).filter(r => r.region_id === regionId).map(r => r.note).filter((n): n is string => typeof n === 'string'))],
  }
}

type Review = ReturnType<typeof regionalReview> & { raw?: string; rawError?: boolean }
export function ScanRegionReview({ doc, regionId }: { doc: ArticleDoc; regionId: string }) {
  const pin = doc.scan!.corrections.find(p => p.path.endsWith('/corrections.json') || p.path === 'corrections.json')
  const key = `${pin?.path || ''}:${regionId}`
  const [state, setState] = useState<{ key: string; data?: Review; error?: string }>()
  const region = doc.scan!.regions.find(r => r.id === regionId)!
  useEffect(() => {
    if (!pin) return
    const controller = new AbortController()
    const read = async () => {
      try {
        const response = await fetch(sourceUrl(pin.path), { signal: controller.signal })
        if (!response.ok) throw new Error('교정 기록을 불러오지 못했습니다.')
        const data = regionalReview(await response.json(), regionId)
        const rawPath = data.record?.raw_ocr?.path
        let raw: string | undefined, rawError = false
        if (rawPath) {
          try {
            const prefix = pin.path.slice(0, pin.path.lastIndexOf('/') + 1)
            const result = await fetch(sourceUrl(prefix + rawPath), { signal: controller.signal })
            if (!result.ok) throw new Error('Raw OCR unavailable')
            raw = await result.text()
          } catch { rawError = true }
        }
        if (!controller.signal.aborted) setState({ key, data: { ...data, raw, rawError } })
      } catch {
        if (!controller.signal.aborted) setState({ key, error: '교정 기록을 불러오지 못했습니다. 원문 스캔과 본문은 계속 볼 수 있습니다.' })
      }
    }
    void read()
    return () => controller.abort()
  }, [pin?.path, regionId, key])
  const current = state?.key === key ? state : undefined
  const data = current?.data
  const fallback = doc.blocks.filter(b => b.regionIds?.includes(regionId) && !b.scanFigureId)
  return <section className="region-reading" aria-label="교정문과 검토 기록">
    <h2>교정문</h2>
    {data?.record?.human_acceptance === 'pending' && <p className="notice">사람 검토 대기 · 아래 교정문을 원문과 대조해 주세요.</p>}
    {pin && !current && <p role="status">교정문을 불러오는 중…</p>}
    {current?.error && <p role="alert">{current.error}</p>}
    {data?.text !== undefined ? <pre className={region.kind === 'code' ? 'region-code' : 'region-prose'}>{data.text}</pre> :
      region.kind === 'figure' ? <p>그림과 표의 원본 이미지입니다. 내부 글자도 스캔에서 확인해 주세요.</p> :
      (!pin || current) && <><p>이 영역에 연결된 본문입니다. 여러 스캔의 내용이 이어질 수 있습니다.</p>{fallback.map(b => <pre key={b.id} className={b.preformatted ? 'region-code' : 'region-prose'}>{b.paragraphs.flatMap(p => p.runs.filter(r => r.type === 'text').map(r => r.text)).join('')}</pre>)}</>}
    {!!data?.uncertainties.length && <section className="notice"><h3>확인이 필요한 부분</h3><ul>{data.uncertainties.map(n => <li key={n}>{n}</li>)}</ul></section>}
    {!!data?.notes.length && <details open><summary>교정 메모 · {data.notes.length}건</summary><ul>{data.notes.map(n => <li key={n}>{n}</li>)}</ul></details>}
    {data?.raw !== undefined && <details><summary>교정 전 OCR 보기</summary><pre className="region-prose">{data.raw}</pre></details>}
    {data?.rawError && <p role="status">교정 전 OCR를 불러오지 못했습니다.</p>}
  </section>
}

export function ScanText({ text }: { text: string }) {
  const rows = text.replace(/\n$/, '').split('\n').map(line => line.split('\t'))
  if (rows.length && rows[0].length > 1 && rows.every(r => r.length === rows[0].length)) {
    return <div className="scan-table-scroll" tabIndex={0} role="region" aria-label="원문 표"><table><tbody>{rows.map((r, i) => <tr key={i}>{r.map((cell, j) => <td key={j}>{cell}</td>)}</tr>)}</tbody></table></div>
  }
  return <>{text.split('\n\n').map((p, i) => <p key={i} className="article-paragraph">{p}</p>)}</>
}
