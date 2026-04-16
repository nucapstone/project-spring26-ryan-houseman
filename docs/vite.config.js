import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default {
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:5000'
    }
  },
  plugins: [react()],
}
