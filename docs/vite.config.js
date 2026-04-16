import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: '/project-spring26-ryan-houseman/docs/',
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:5000'
    }
  },
  plugins: [react()],
})
