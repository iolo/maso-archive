import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'node:path'
import fs from 'node:fs'

const project = path.resolve(import.meta.dirname, '..')
const output = process.env.READING_ROOM_OUTPUT ? path.resolve(project, process.env.READING_ROOM_OUTPUT) : path.join(project, 'build/reading-room')
const base = process.env.READING_ROOM_BASE || '/'

export default defineConfig({
  base,
  plugins: [
    react(),
    tailwindcss(),
    {
      name: 'private-reading-room-data',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          const pathname = decodeURIComponent((req.url || '').split('?')[0])
          const dataPrefix = `${base.replace(/\/$/, '')}/data/`
          if (!pathname.startsWith(dataPrefix)) return next()
          const relative = pathname.slice(dataPrefix.length)
          const root = path.join(output, 'data')
          const file = path.resolve(root, relative)
          if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) return next()
          res.setHeader('Content-Type', file.endsWith('.html') ? 'text/html; charset=utf-8' :
            file.endsWith('.css') ? 'text/css; charset=utf-8' :
            file.endsWith('.json') ? 'application/json; charset=utf-8' :
            file.endsWith('.txt') ? 'text/plain; charset=utf-8' : file.endsWith('.svg') ? 'image/svg+xml' :
            /\.png$/i.test(file) ? 'image/png' : /\.jpe?g$/i.test(file) ? 'image/jpeg' :
            /\.webp$/i.test(file) ? 'image/webp' : 'application/octet-stream')
          fs.createReadStream(file).pipe(res)
        })
      },
    },
  ],
  resolve: { alias: { '@': path.resolve(import.meta.dirname, './src') } },
  build: { outDir: output, emptyOutDir: false },
})
