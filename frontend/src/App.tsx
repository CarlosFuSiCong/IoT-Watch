import { useState } from 'react'
import { Routes, Route, NavLink } from 'react-router-dom'
import { useQueryClient } from '@tanstack/react-query'
import OverviewPage     from './pages/OverviewPage'
import DevicesPage      from './pages/DevicesPage'
import DeviceDetailPage from './pages/DeviceDetailPage'
import AlertsPage       from './pages/AlertsPage'
import client           from './api/client'
import './App.css'

type SimState = 'idle' | 'running' | 'error'

export default function App() {
  const queryClient = useQueryClient()
  const [simState, setSimState] = useState<SimState>('idle')

  async function handleSimulate() {
    if (simState === 'running') {
      try {
        await client.post('/demo/stop')
      } catch (err) {
        console.error('[sim stop]', err)
      }
      queryClient.invalidateQueries()
      setSimState('idle')
      return
    }

    if (simState === 'idle') {
      setSimState('running')
      try {
        await client.post('/demo/start')
        queryClient.invalidateQueries()
      } catch (err) {
        console.error('[sim start]', err)
        setSimState('error')
        setTimeout(() => setSimState('idle'), 2_000)
      }
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header-left">
          <span className="app-logo">
            IOT WATCH
            <span className="logo-demo">DEMO</span>
          </span>
          <button
            className={`btn-simulate${simState !== 'idle' ? ` ${simState}` : ''}`}
            onClick={handleSimulate}
            disabled={simState === 'error'}
          >
            {simState === 'running' ? '■ STOP' : simState === 'error' ? 'ERR — backend?' : 'SIMULATE'}
          </button>
        </div>
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
