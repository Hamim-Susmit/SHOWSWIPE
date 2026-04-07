import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import SetupPage from './pages/SetupPage'
import SwipePage from './pages/SwipePage'
import MatchesPage from './pages/MatchesPage'
import { useAppStore } from './store/useAppStore'

function Guard({ children }) {
  const circleId = useAppStore((s) => s.circleId)
  return circleId ? children : <Navigate to="/setup" replace />
}

export default function App() {
  const circleId = useAppStore((s) => s.circleId)
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to={circleId ? '/swipe' : '/setup'} replace />} />
        <Route path="/setup" element={<SetupPage />} />
        <Route path="/swipe" element={<Guard><SwipePage /></Guard>} />
        <Route path="/matches" element={<Guard><MatchesPage /></Guard>} />
      </Routes>
    </BrowserRouter>
  )
}
