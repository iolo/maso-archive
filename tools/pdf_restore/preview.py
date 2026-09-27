"""Portable scan article HTML, reused by article and later issue references."""
from tools.reference.export import CSS, esc, page

EXTRA_CSS = '''
body{max-width:64rem}main{max-width:48rem;margin:auto}.text{margin:1rem 0}
.review{padding:1rem 0;border-block:1px solid #ddd}.evidence-links{font-size:.85rem}
pre{max-width:100%;white-space:pre;overflow-x:auto}.byline,.section-label{color:#555}
figcaption{font-size:.9rem}summary{overflow-wrap:anywhere}.download-list{overflow-wrap:anywhere}
'''


def render_preview(package):
    regions = {r['id']: r for r in package['regions']}
    pages = {p['pdf_index']: p for p in package['pages']}
    assets = {r['region_id']: r['asset'] for r in package.get('region_assets', [])}
    blocks = {b['id']: b for b in package['blocks']}
    figures = {f['id']: f for f in package['figures']}
    def evidence_links(ids):
        return '<p class="evidence-links">' + ' · '.join(
            f'<a href="{esc(assets[id]["path"])}">스캔 {esc(id)} · 인쇄 {esc(pages[regions[id]["pdf_index"]]["printed_page"] or "미상")}쪽</a>'
            for id in ids if id in assets) + '</p>'
    availability = {'readable': '읽기 가능', 'partial': '일부 복원', 'image-only': '이미지만 있음',
                    'failed': '복원 시도 실패', 'unresolved': '미해결'}[package['availability']]
    verification = {'unreviewed': '검토 전', 'sample-reviewed': '범위를 명시한 검토',
                    'fully-reviewed': '전체 검토'}[package['verification']['status']]
    body = [f'<main><nav><a href="#reading">본문</a><a href="#evidence">스캔 근거</a><a href="#downloads">다운로드</a></nav>',
            f'<p>{esc(package["issue_id"])} · {esc(package["toc_entry_id"])}</p>',
            f'<section class="review" aria-label="복원 및 검토 상태"><p>복원: <strong>{esc(availability)}</strong> '
            f'({esc(package["availability"])}) · 검토: <strong>{esc(verification)}</strong> '
            f'({esc(package["verification"]["status"])})</p>']
    for note in package['verification']['evidence'] + package['verification']['uncertainties']:
        body.append(f'<p>{esc(note)}</p>')
    if package['gaps']:
        body.append('<p>⟦…⟧는 원문이 아닌 판독 불확실 표시입니다.</p><ul class="gap">' +
                    ''.join(f'<li>{esc(gap)}</li>' for gap in package['gaps']) + '</ul>')
    body.append('</section><article id="reading">')
    if not package.get('content_order'):
        body.append(f'<h1>{esc(package["title"])}</h1><p>읽기 본문이 아직 준비되지 않았습니다.</p>')
    for item in package.get('content_order', []):
        if item['type'] == 'figure':
            figure = figures[item['id']]
            body.append(f'<figure id="{esc(figure["id"])}"><a href="{esc(figure["asset"]["path"])}">'
                        f'<img src="{esc(figure["asset"]["path"])}" loading="lazy" alt="원문 그림 — {esc(package["title"])}"></a>')
            if figure['caption'] is not None:
                body.append(f'<figcaption>{esc(figure["caption"])}</figcaption>')
            body.append('</figure>' + evidence_links(figure['region_ids']))
        else:
            block = blocks[item['id']]
            body.append(f'<section id="{esc(block["id"])}">')
            if block['kind'] == 'code':
                body.append(f'<pre><code>{esc(block["text"])}</code></pre>')
            else:
                tag = 'h1' if block['kind'] == 'title' else 'p'
                paragraphs = block['text'].split('\n\n') if block['kind'] == 'prose' else [block['text']]
                for paragraph in paragraphs:
                    body.append(f'<{tag} class="text {esc(block["kind"])}">{esc(paragraph)}</{tag}>')
            body.append(evidence_links(block['region_ids']))
            for note in block['uncertainties']:
                body.append(f'<p class="gap">{esc(note)}</p>')
            body.append('</section>')
    body.append('</article><section id="evidence"><h2>스캔 근거</h2><ul>')
    for region in package['regions']:
        page_record = pages[region['pdf_index']]
        label = f'{region["id"]} · PDF {page_record["pdf_page"]} / 인쇄 {page_record["printed_page"] or "미상"} · {region["kind"]}'
        if region['id'] in assets:
            body.append(f'<li><a href="{esc(assets[region["id"]]["path"])}">{esc(label)}</a></li>')
        else:
            body.append(f'<li>{esc(label)} — 스캔 자산 없음</li>')
    body.append('</ul></section><section id="downloads"><h2>다운로드</h2><ul class="download-list">')
    for record in package['downloads']:
        body.append(f'<li><a download href="{esc(record["path"])}">{esc(record["path"])}</a> ({record["bytes"]:,} bytes)</li>')
    body.append('</ul><p><a href="article.json">기사 기록</a> · <a href="corrections.json">교정 및 검토 근거</a></p></section></main>')
    return page(package['title'], ''.join(body), 0), CSS + EXTRA_CSS
