# reading-room

NOTE: this PRD is related PRD-local-web.md but seperated for simplicity.

## GOAL

- browser-based reading room for issues/articles in archive

## INPUT

- output of PLAN-CD1.md
  - build/cd1-reference/index.html
- output of PLAN-CD2.md
  - build/cd2-reference/index.html
- output of PLAN-CD3.md
  - build/cd3-reference/index.html
- covers: cover images of all issues, but some issues are missing(not prepared yet).

## OUTPUT

- SPA webapp for reading issues/articles in archive

## architecture

user <--> SPA webapp <--> static files

## design principles

- plain-old holygrail layout
- simple & clean
- readable typography, good line height, good contrast
- minimalistic UI
- responsive design
- dark/light mode(default: system)

## tech stack

- vite, react, typescript, shadcn/ui(default theme), react-router-dom
- vitest, playwright
- no server-side-rendering
- no server, no database, no backend.
- static, client-side only SPA. all data is pre-generated and bundled with the app.

## UI layout

- header
  - fixed on top
  - logo, main nav, dark/light mode toggle
    - issue selector
      - year
      - month
    - search
    - dark/light mode toggle
  - main nav
- nav: TOC
  - left side on main
  - list/tree on desktop. dropdown on mobile.
  - TOC of the selected issue
- main
  - varying content area
  - index of issues(like bookshelf)
  - or cover of the selected issue
  - or the selected article
  - or the selected media
- aside
  - right side on main
  - collapsible. open at desktop, closed at mobile by default
  - link to releated articles, recommended articles, etc.
- footer
  - sticky on bottom
  - copyright, legal, link, etc.

## target contents

- 83.11 to 95.12 issues, but some issues are missing(not prepared yet).
- TOC of all issues are prepared, but some articles could be missing(not prepared yet).
