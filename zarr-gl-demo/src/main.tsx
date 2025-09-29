import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import 'mapbox-gl/dist/mapbox-gl.css'
import './index.css'
import App from './App.tsx'
import { Buffer } from 'buffer'

if (!window.Buffer) {
  window.Buffer = Buffer
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
)
