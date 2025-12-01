import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5177,
    proxy: {
      // Proxy API requests to FastAPI backend, so frontend and backend
      // appear under one origin (http://localhost:5177) in the browser.
      '/upload': 'http://localhost:8000',
      '/scenes': 'http://localhost:8000',
      '/projects': 'http://localhost:8000',
    },
  },
})
