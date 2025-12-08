import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom' // Yönlendirme sistemi
import 'bootstrap/dist/css/bootstrap.min.css'    // Tasarım (Bootstrap)
import './index.css'                             // Kendi stillerimiz
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)