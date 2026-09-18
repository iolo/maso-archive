# reading-room

browser-based reading room for issues/articles in archive

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
  - logo, main nav, dark/light mode toggle
    - issue selector
      - year
      - month
    - search
    - dark/light mode toggle
  - fixed on top
  - main nav
- nav: TOC
  - left side on main
  - list/tree on desktop. dropdown on mobile.
- main
  - varying content area
  - issue index(like bookshelf)
  - selected issue cover
  - selected article
  - selected media
- aside
  - link to releated articles, recommended articles, etc.
  - right side on main
  - collapsible. open at desktop, closed at mobile by default
- footer
  - copyright, license, etc.
  - sticky on bottom

