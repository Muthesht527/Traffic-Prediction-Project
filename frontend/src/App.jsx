import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import ForecastPage from './pages/ForecastPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/forecast" element={<ForecastPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
