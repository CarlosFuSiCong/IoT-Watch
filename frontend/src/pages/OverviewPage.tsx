import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import client from '../api/client'
import type { ApiResponse, Device, AlertPage } from '../api/types'

interface Stat {
  label: string
  value: number | string
  accent?: string
}

function StatBox({ label, value, accent }: Stat) {
  return (
    <div className="stat-box" style={{ borderLeftColor: accent }}>
      <span className="stat-value">{value}</span>
      <span className="stat-label">{label}</span>
    </div>
  )
}

export default function OverviewPage() {
  const { data: devices } = useQuery({
    queryKey: ['devices'],
    queryFn: async () => {
      const res = await client.get<ApiResponse<Device[]>>('/devices')
      return res.data.data ?? []
    },
    refetchInterval: 10_000,
  })

  const { data: alertPage } = useQuery({
    queryKey: ['alerts', 'overview'],
    queryFn: async () => {
      const res = await client.get<ApiResponse<AlertPage>>('/alerts?limit=5')
      return res.data.data
    },
    refetchInterval: 15_000,
  })

  const total   = devices?.length ?? '—'
  const online  = devices?.filter(d => d.status === 'online').length ?? '—'
  const offline = devices?.filter(d => d.status === 'offline').length ?? '—'
  const alerts  = alertPage?.total ?? '—'

  const recentAlerts = alertPage?.items ?? []

  return (
    <section className="page">
      <header className="page-head">
        <h1 className="page-title">OVERVIEW</h1>
      </header>

      <div className="stat-grid">
        <StatBox label="DEVICES"      value={total}   />
        <StatBox label="ONLINE"       value={online}  accent="var(--online)" />
        <StatBox label="OFFLINE"      value={offline} accent="var(--offline)" />
        <StatBox label="TOTAL ALERTS" value={alerts}  accent="var(--warn)" />
      </div>

      {/* Recent alerts strip */}
      {recentAlerts.length > 0 && (
        <div>
          <h2 className="section-title">RECENT ALERTS</h2>
          <table className="data-table">
            <thead>
              <tr>
                {['Time', 'Device', 'Type', 'Message'].map(h => <th key={h}>{h}</th>)}
              </tr>
            </thead>
            <tbody>
              {recentAlerts.map(a => (
                <tr key={a.id}>
                  <td className="dim nowrap">
                    {new Date(a.timestamp).toLocaleString('en-GB', {
                      month: '2-digit', day: '2-digit',
                      hour: '2-digit', minute: '2-digit',
                    })}
                  </td>
                  <td className="mono dim">{a.device_id}</td>
                  <td>
                    <span className={`alert-type ${
                      a.type === 'HIGH_TEMPERATURE' ? 'alert-temp' :
                      a.type === 'LOW_BATTERY'      ? 'alert-batt' : 'alert-offline'
                    }`}>
                      {a.type === 'HIGH_TEMPERATURE' ? 'HIGH TEMP' :
                       a.type === 'LOW_BATTERY'      ? 'LOW BATT'  : 'OFFLINE'}
                    </span>
                  </td>
                  <td className="msg">{a.message}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Device quick list */}
      {(devices?.length ?? 0) > 0 && (
        <div>
          <h2 className="section-title">DEVICES</h2>
          <table className="data-table">
            <thead>
              <tr>
                {['ID', 'Name', 'Status', 'Last Seen'].map(h => <th key={h}>{h}</th>)}
              </tr>
            </thead>
            <tbody>
              {devices!.map(d => (
                <tr key={d.id} className="row-link">
                  <td className="mono dim">
                    <Link to={`/devices/${d.id}`} className="row-anchor">{d.id}</Link>
                  </td>
                  <td>{d.name}</td>
                  <td>
                    <span className={`status-dot ${d.status}`}>●</span>
                    {' '}
                    <span className={d.status === 'online' ? 'txt-online' : 'txt-offline'}>
                      {d.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="dim">
                    {new Date(d.last_seen).toLocaleString('en-GB', {
                      hour: '2-digit', minute: '2-digit', second: '2-digit',
                    })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}
