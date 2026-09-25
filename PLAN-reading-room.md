# Reading-room implementation plan

Prepared 2026-09-26 from [PRD-reading-room.md](PRD-reading-room.md), the
[predecessor handoff](docs/SUCCESSOR-NOTES.md), and inspection of the completed
[CD1 reference](docs/CD1-READABLE-REFERENCE.md). Status: **implemented**; see the
[build and use guide](docs/READING-ROOM.md). This plan owns the SPA; [PLAN-CD1.md](PLAN-CD1.md) remains the
record of completed extraction and its deferred backlog.

## Outcome and scope

Deliver a simple, responsive reading room for **November 1983–December 1993**.
Readers can browse issues, inspect each issue's TOC, read available articles,
view media, download source text/listings, and search metadata. Missing bodies,
covers, and image derivatives have useful, explicit states.

Use the requested Vite, React, TypeScript, shadcn/ui default theme,
react-router-dom, Vitest, and Playwright stack. All content is generated before
deployment and shipped with the static application. No SSR, API service,
database, accounts, or runtime extraction is involved.

The stopping point is a usable reader for the existing export, with its known
exceptions. New extraction, cosmetic RTF recovery, image repair, guessed TOC
matches, OCR/correction workflows, CD2/CD3, and public deployment are separate
work. Paper remains authoritative; successful rendering does not verify CD text
against print.

## Inspected starting point

| Existing input | What the reader can reuse |
| --- | --- |
| `build/cd1-reference/index.html` | Completed reference and fallback for comparison |
| `build/cd1-reference/catalog.json` | 1,088 candidate identities, titles, issue membership, status, paths and counts |
| Per-article `reference.json` | Ordered text/media runs, blocks, paragraph IDs, listing links, and review notes |
| Per-article `article.txt`, `paragraphs.json`, `listings/*.txt` | Literal text downloads and paragraph/image positions |
| `build/cd1-reference/images.json` and issue media folders | Available derivatives, originals, conversion notes and deferred states |
| `build/cd1-reference/manifest.json` | Source hashes, exported file inventory, and baseline counts |
| `build/toc/issues.json`, `toc-entries.jsonl` | 122 issues and 5,497 ordered TOC entries, including 50 issues without CD1 bodies |
| Issue packages located by `data/catalog/batch-runs/cd1-oem-pass.json` | Existing reviewed TOC/article associations and supported article metadata |

The current baseline has 1,080 article texts across 72 issues: 995 prepared,
52 recovered without marked gaps, and 33 with marked gaps. Eight candidates
have unresolved article boundaries. There are 3,125 listing downloads, 7,738
image occurrences, and 6,090 distinct image resources: 4,979 viewable and 1,111
deferred. `images.json` has 6,783 issue/resource records because resources can
occur in multiple issues; do not confuse that count with distinct images.

The two `build/toc/` files currently match the hashes pinned in the reference
manifest. The reference's article catalog does not itself contain the complete
issue TOC or reviewed associations. Consume the matching structured inputs at
build time instead of scraping generated HTML or matching titles heuristically.

The older [reading-room v1 contract](docs/READING-ROOM-CONTENT-V1.md) describes
the strict package pipeline, not the newer reference export. Reuse its identity,
ordering, literal-text, and missing-media principles; leave its schema and
historical packages unchanged. The SPA adapter must accommodate all 85 recovered
references as well as the 995 strict preparations.

`PRD-local-web.md`, mentioned in the PRD and handoff, is absent from this working
tree. This plan uses the present reading-room PRD and completed reference guide;
it does not infer additional requirements from that missing document. The broader
archive's 1995 target does not extend this PRD's 1993 endpoint.

## Application and data design

Place the frontend in `web/`, the build adapter in
`tools/reading_room/export.py`, and generated private data/output under
`build/reading-room/`. Track source, lockfile, documentation and synthetic test
fixtures; ignore generated publisher content, dependency folders and browser
artifacts. A checkout without private sources must still support a synthetic
demo and unit/browser tests. Archive mode must fail clearly if required inputs
are missing rather than silently substituting demo content.

Generate a small, explicitly versioned SPA data format:

- A manifest records input hashes, document paths, output hashes and counts.
- A catalog contains issue summaries and article metadata for browsing.
- One issue document contains the ordered TOC, reviewed links, and a separate CD
  article list. Preserve persistent issue, TOC and article IDs.
- One article document projects the reference blocks, exact runs and paragraph
  termination, status, downloads, and the media records needed by that article.
  Keep original reference/provenance accessible separately; avoid loading repeated
  raw recovery evidence into the reader.
- Per-issue media indexes support direct media routes. Distinguish source resource
  identity from its issue-specific file location; equal bytes do not merge identities.
- A separate metadata search index includes TOC titles, available bylines, article
  titles, dates and native references. Preserve original display strings.

Read article bodies from the completed reference only. Use matching TOC inputs
and existing issue packages solely to supplement metadata/associations. Retain
unlinked articles and unmatched TOC entries independently, including multiple
reviewed links where present. Fail with an actionable input error on mismatched
snapshots; do not regenerate extraction or invent relationships automatically.

Preserve supplied block semantics, meaningful emphasis, captions, IDs, whitespace,
tabs, newlines and gap markers. Honor each paragraph's `terminated` value. Render
run text as text nodes, with explicit markup for supported marks; do not interpret
article text as HTML or Markdown. Keep media markers/occurrences in source order,
including inside preformatted blocks, with nearby image previews and links.
Do not infer richer structure for normalized paragraphs. Unknown data versions
or unsupported blocks produce a visible error rather than silent omissions.

Copy required derivatives, originals, downloads and reference evidence into the
static output, preserving bytes and relative relationships. Do not put the
approximately 1.07 GB reference into JavaScript imports or fetch it at startup.
Load issue/article documents on navigation, search metadata when needed, and
images lazily. Do not pre-cache the entire archive or add a service worker in v1.

Use one configured deployment base for application and data URLs. Default to
hash routes so static hosts need no route-rewrite rules:

| Route | Main content |
| --- | --- |
| `#/` | Issue bookshelf, grouped by year |
| `#/issues/:issueId` | Cover or missing-cover state, issue summary and CD article list |
| `#/issues/:issueId/toc/:entryId` | Selected TOC metadata and its available links or missing-body state |
| `#/articles/:articleId` | Article reader; selected issue follows article metadata |
| `#/issues/:issueId/media/:resource` | Image viewer, original/derivative downloads and availability notes |
| `#/search?q=…&issue=…` | Shareable metadata search and optional issue filter |

Encode route parameters; resolve data paths against the deployment base, never
the current route. Keep paragraph/listing selection in a route query parameter
when a deep link needs it. Support back/forward, refresh, invalid IDs, loading
and retryable file-load errors.

Interpret “no server” as no application backend: development/preview tools and
ordinary static file hosting serve the prebuilt files. Direct `file://` loading
is not an SPA acceptance requirement; the completed HTML reference continues
to provide that capability. Document this delivery assumption clearly.

## Reading experience

Visual thesis: a quiet magazine library, using the default shadcn neutral palette,
clear Korean typography, generous line height, and minimal controls.

Content plan: issue browsing leads to an issue overview, then article or media
reading; TOC navigation stays available, with secondary context in the aside.
Use real supplied covers when available and a simple date/title placeholder when
absent. No fabricated covers, decorative hero, or marketing section is needed.

Interaction thesis: brief TOC/menu opening and aside-collapse transitions provide
orientation; focus/hover states make navigation clear. Respect reduced motion
and avoid animated article entrances that interrupt reading.

- **Header:** fixed at the top, with text logo/home link, primary navigation,
  year/month selectors, search, and one System/Light/Dark theme control. Reserve
  space so it never covers content or keyboard focus. Default to system theme;
  persist explicit choices and react to system changes while in System mode.
- **Left navigation:** ordered nested issue TOC on desktop, with current selection
  and expansion controls. On mobile, use a labeled TOC dropdown/popover that
  preserves hierarchy and keyboard access. Keep CD articles discoverable even
  where the library TOC has no reviewed match.
- **Main:** responsive bookshelf on the index; cover/issue information on the
  issue route; a comfortable reading column for prose; horizontally scrollable
  code and wide tables within the article rather than across the whole viewport.
  Preserve code characters and offer the existing UTF-8/listing downloads.
- **Right aside:** open by default on desktop, closed on mobile, collapsible in
  both. Initially show clearly labeled “More from this issue” and article media
  or available source links. Use explicit relationships if present; do not claim
  same-issue suggestions are editorial recommendations or infer author identities.
- **Footer:** copyright/source notice and useful links. Keep it at the viewport
  bottom for short pages and after content for long pages, without obscuring text.
- **Missing/review states:** distinguish TOC-only issues, unmatched TOC entries,
  blocked article boundaries, text with localized gaps, unavailable covers and
  deferred images. Show original image links where available. An unmatched TOC
  entry means no linked prepared body, not proof the article is absent from the CD.
  Keep the paper-verification notice compact and detailed evidence expandable.

Use Korean interface labels and `lang="ko"`; system sans-serif for reading and a
monospace stack for code, with no remote font dependency. Start with roughly
17–18 px prose and 1.7–1.8 line height, then check real Korean articles. Support
keyboard navigation, visible focus, landmarks, skip-to-content, labeled controls,
semantic headings, readable contrast in both themes, and 200% zoom.

Search v1 covers **metadata across all 122 issues**, including entries without
bodies. Normalize only the search copy of strings for Unicode/case/whitespace;
never modify displayed or downloaded source text. Rank title matches first,
label TOC versus CD-article results and their availability, and avoid duplicate
results where reviewed associations support grouping. Unmatched records remain
separate. Label the feature as title/author search; full-text indexing is deferred.

## Implementation sequence and completion checks

Each step ends with a usable result, relevant checks, a PROGRESS.md entry, and a
scoped commit. Keep owner PRD edits out of those commits. Do not reopen extraction
or run the full historical regression suite merely for frontend work.

### 1. Prepare the adapter and a representative fixture

- Define TypeScript data types and adapter validation for the proposed format.
  Add synthetic fixtures for prepared, recovered, gap-bearing, blocked and
  unmatched content, including inline media, code and deferred images.
- Implement a deterministic export with explicit input/output paths, safe local
  path handling, supported versions, source hashes and reference validation.
  Write only into new reading-room build output.
- Export February 1988 for the first real slice, including `8802030` (Gary Kildall),
  `8802184` (Turbo C/code/images), and unindexed `8802162` (KEYBOARD LOCK).

**Done when:** adapter tests establish exact text/listing preservation, stable
identities, correct associations and unavailable states. The February data can
be loaded without parsing RTF or invoking the historical recovery pipeline.

### 2. Deliver the first working reader

- Scaffold Vite/React/TypeScript, shadcn default styling and hash routing. Add the
  data loader, responsive holy-grail shell, theme control and issue selectors.
- Render the February issue/TOC, article blocks, media placeholders/previews and
  text/listing downloads. Include explicit loading, missing and error states.

**Done when:** a browser can navigate February → Kildall interview → another
article, read Korean comfortably, open an image and download unchanged code/text.
The flow works on desktop and mobile, with refresh/back navigation and both themes.
This is the first usable checkpoint; do not wait for search to demonstrate it.

### 3. Include the complete archive and media routes

- Export all 122 issue records, 5,497 TOC entries and 1,088 candidates. Add the
  bookshelf, TOC-only issue pages, dedicated media view and contextual aside.
- Preserve the 33 gap-bearing references and eight blocked states. Show missing
  covers honestly. Add lazy loading and avoid fetching unrelated article bodies.

**Done when:** generated counts reconcile with the pinned reference; all 1,080
  text downloads and 3,125 listings retain their original bytes. Every catalog,
  TOC, media and download link resolves or has an explicit unavailable state.
  Check distinct resources separately from issue-specific media records.

### 4. Add search and complete navigation behavior

- Implement the metadata index, search results, issue filter, URL query state and
  empty/no-results states. Add stable deep links and accessible route focus/scroll
  handling, preserving the selected issue when moving between article and media.
- Finish mobile TOC behavior, aside defaults, theme persistence and keyboard use.

**Done when:** Korean/Latin titles, supplied bylines and native references find
the expected records, including TOC-only results. Sharing or refreshing a search
URL restores its query/filter, and all primary flows work without a mouse.

### 5. Validate and package the static deliverable

- Run adapter tests, TypeScript checks, Vitest and production build. Unit tests
  target loader/version/path errors, route lookup, search, themes and literal
  rendering behavior; avoid snapshots that merely mirror component markup.
- Use Playwright against the production build for bookshelf → issue → article
  → media, download bytes, metadata search, missing states, refresh/back, mobile
  controls and keyboard operation. Cover a synthetic fixture in ordinary CI and
  a separate real-export integration run locally.
- Include real cases `8802030`, `8802184`, `8802162`, recovered `8901110` and
  `9103202`, plus an actual gap-bearing article, blocked candidate, deferred image
  and TOC-only issue selected from the catalog. Assert representative rendered
  text/code matches the reference, including tabs, operators and gap markers.
- Check 360 px mobile and desktop layouts, 200% zoom, system/light/dark modes,
  reduced motion, long article/code overflow, and image readability in dark mode.
- Serve the build at `/` and a nested base such as `/archive/`; verify routes,
  assets and downloads with no external runtime requests. Inspect startup requests
  to confirm unrelated bodies and media are not eagerly loaded. Record actual
  bundle sizes and browser results rather than inventing performance claims.
- Document exact preparation, demo, dev, build and preview commands, required
  private inputs, static-host assumptions, output path and known limitations in
  `docs/READING-ROOM.md`; link it from README. Record final counts and validation.

**Done when:** the complete static output runs independently of the source tree
and extraction tools, all focused checks pass, and the owner can browse/read the
existing archive with visible exceptions. Preserve the original CD1 reference.
No deployment, additional recovery campaign or paper-verification claim is part
of completion.

## Delivered

The adapter, synthetic demo, full archive export, responsive reader, metadata
search, static package and focused validation are complete. The production build
resides under ignored `build/reading-room/`; the synthetic demo uses
`build/reading-room-demo/`. Refer to the guide for commands and current limits.
Later changes should respond to concrete reading or paper-restoration needs.
