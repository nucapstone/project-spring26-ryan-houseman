import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  base: '/project-spring26-ryan-houseman/docs/',
  build: {
    outDir: 'docs'
  },
  plugins: [react()],
})
