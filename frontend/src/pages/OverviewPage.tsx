import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import client from '../api/client'
import type { ApiResponse, Device, AlertPage } from '../api/types'
import StatGrid from '../components/StatGrid'
import AlertsTable from '../components/AlertsTable'
import DeviceStatus from '../components/DeviceStatus'
import { fmtTime } from '../lib/utils'

export default function OverviewPage() {
  const { data: devices } = useQuery({
    queryKey: ['devices'],
    queryFn: async () => {
      const res = await client.get<ApiResponse<Device[]>>('/devices')
      return res.data.data ?? []
    },
    refetchInterval: 3_000,
  })

  const { data: alertPage } = useQuery({
    queryKey: ['alerts', 'overview'],
    queryFn: async () => {
      const res = await client.get<ApiResponse<AlertPage>>('/alerts?limit=5')
      return res.data.data
    },
    refetchInterval: 3_000,
  })

  const total   = devices?.length ?? '--'
  const online  = devices?.filter(d => d.status === 'online').length ?? '--'
  const offline = devices?.filter(d => d.status === 'offline').length ?? '--'
  const alerts  = alertPage?.total ?? '--'

  const recentAlerts = alertPage?.items ?? []

  return (
    <section className="page">
      <header className="page-head">
        <h1 className="page-title">OVERVIEW</h1>
      </header>

      <StatGrid total={total} online={online} offline={offline} alerts={alerts} />

      {recentAlerts.length > 0 && (
        <div>
          <h2 className="section-title">RECENT ALERTS</h2>
          <AlertsTable items={recentAlerts} showDevice />
        </div>
      )}

      {(devices?.length ?? 0) > 0 && (
        <div>
          <h2 className="section-title">DEVICES</h2>
          <table className="data-table">
            <thead>
              <tr>
                {['ID', 'Status', 'Last Seen'].map(h => <th key={h}>{h}</th>)}
              </tr>
            </thead>
            <tbody>
              {devices!.map(d => (
                <tr key={d.id} className="row-link">
                  <td className="mono dim">
                    <Link to={`/devices/${d.id}`} className="row-anchor">{d.id}</Link>
                  </td>
                  <td><DeviceStatus status={d.status} /></td>
                  <td className="dim">{fmtTime(d.last_seen)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}
