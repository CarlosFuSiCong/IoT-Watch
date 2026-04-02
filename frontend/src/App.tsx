import { Routes, Route, NavLink } from 'react-router-dom'
import DevicesPage from './pages/DevicesPage'
import AlertsPage from './pages/AlertsPage'
import './App.css'

export default function App() {
  return (
    <div className="app">
      <header className="app-header">
        <span className="app-logo">IoT Watch</span>
        <nav>
          <NavLink to="/" end>Devices</NavLink>
          <NavLink to="/alerts">Alerts</NavLink>
        </nav>
      </header>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<DevicesPage />} />
          <Route path="/alerts" element={<AlertsPage />} />
        </Routes>
      </main>
    </div>
  )
}
