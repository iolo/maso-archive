import { describe, expect, it } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import { regionalReview, ScanText, type CorrectionDocument } from './ScanRegionReview'

describe('human scan review', () => {
  it('selects only the requested assembled region and its original notes', () => {
    const source: CorrectionDocument = {
      regional_transcription: { 'a-r1': 'first', 'b-r1': 'second' },
      records: [{ id: 'a-r1', raw_ocr: { path: 'segments/a/raw.txt' }, human_acceptance: 'pending' }],
      identity_map: [{ kind: 'region', id: 'a-r1', source_id: 'r1', source_segment: 'a' }],
      segments: [{ name: 'a', original_metadata: { source_review_notes: [{ region_id: 'r1', note: 'Source spelling retained.' }] } }, { name: 'b', original_metadata: { source_review_notes: [{ region_id: 'r1', note: 'Other note.' }] } }],
      unresolved_text: [{ region_id: 'a-r1', note: 'Check glyph.' }, { region_id: 'b-r1', note: 'Other glyph.' }],
    }
    const result = regionalReview(source, 'a-r1')
    expect(result.text).toBe('first')
    expect(result.record?.raw_ocr?.path).toBe('segments/a/raw.txt')
    expect(result.notes).toEqual(['Source spelling retained.'])
    expect(result.uncertainties).toEqual(['Check glyph.'])
    expect(result.record?.human_acceptance).toBe('pending')
    expect(regionalReview(source, 'missing').text).toBeUndefined()
  })
  it('retains blank cells and escapes table text', () => {
    const html = renderToStaticMarkup(<ScanText text={'A\t\t<x>\nB\t0\t1\n'} />)
    expect(html).toContain('<td>A</td><td></td><td>&lt;x&gt;</td>')
    expect(html.match(/<tr>/g)).toHaveLength(2)
    expect(html).not.toContain('<th>')
  })
  it('does not interpret irregular tabs as a rectangular table', () => {
    const html = renderToStaticMarkup(<ScanText text={'first\tsecond\nthird'} />)
    expect(html).not.toContain('<table>')
    expect(html).toContain('first\tsecond\nthird')
  })
})
