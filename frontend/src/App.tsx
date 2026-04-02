import { Routes, Route, NavLink } from 'react-router-dom'
import OverviewPage      from './pages/OverviewPage'
import DevicesPage       from './pages/DevicesPage'
import DeviceDetailPage  from './pages/DeviceDetailPage'
import AlertsPage        from './pages/AlertsPage'
import './App.css'

export default function App() {
  return (
    <div className="app">
      <header className="app-header">
        <span className="app-logo">IOT WATCH</span>
        <nav>
          <NavLink to="/" end>Overview</NavLink>
          <NavLink to="/devices">Devices</NavLink>
          <NavLink to="/alerts">Alerts</NavLink>
        </nav>
      </header>
      <main className="app-main">
        <Routes>
          <Route path="/"            element={<OverviewPage />} />
          <Route path="/devices"     element={<DevicesPage />} />
          <Route path="/devices/:id" element={<DeviceDetailPage />} />
          <Route path="/alerts"      element={<AlertsPage />} />
        </Routes>
      </main>
    </div>
  )
}
