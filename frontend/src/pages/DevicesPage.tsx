import { useQueries, useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import client from '../api/client'
import type { ApiResponse, Device, SensorData, TelemetryPage } from '../api/types'
import DeviceStatus from '../components/DeviceStatus'
import { DEG_C, fmtDateTimeFull } from '../lib/utils'

const COLS = ['ID', 'Status', `Temp (${DEG_C})`, 'Battery (%)', 'Last Seen'] as const

export default function DevicesPage() {
  const { data: devices, isLoading, isError } = useQuery({
    queryKey: ['devices'],
    queryFn: async () => {
      const res = await client.get<ApiResponse<Device[]>>('/devices')
      return res.data.data ?? []
    },
    refetchInterval: 3_000,
  })

  const telemetryQueries = useQueries({
    queries: (devices ?? []).map(d => ({
      queryKey: ['telemetry', d.id, 'latest'],
      queryFn: async (): Promise<SensorData | null> => {
        const res = await client.get<ApiResponse<TelemetryPage>>(
          `/devices/${d.id}/telemetry?limit=1`
        )
        return res.data.data?.items[0] ?? null
      },
      refetchInterval: 3_000,
      enabled: !!devices,
    })),
  })

  const latestByDevice: Record<string, SensorData | null> = {}
  ;(devices ?? []).forEach((d, i) => {
    latestByDevice[d.id] = telemetryQueries[i]?.data ?? null
  })

  const online = devices?.filter(d => d.status === 'online').length ?? 0
  const total  = devices?.length ?? 0

  return (
    <section className="page">
      <header className="page-head">
        <h1 className="page-title">DEVICES</h1>
        <div className="page-meta">
          {isLoading ? (
            <span className="meta-chip">LOADING</span>
          ) : (
            <>
              <span className="meta-chip online">{online} ONLINE</span>
              <span className="meta-chip offline">{total - online} OFFLINE</span>
            </>
          )}
        </div>
      </header>

      {isError && <p className="state-msg error">ERR -- could not reach backend</p>}

      {!isLoading && !isError && total === 0 && (
        <p className="state-msg">NO DEVICES REGISTERED</p>
      )}

      {!isLoading && !isError && total > 0 && (
        <table className="data-table">
          <thead>
            <tr>{COLS.map(h => <th key={h}>{h}</th>)}</tr>
          </thead>
          <tbody>
            {devices!.map(d => {
              const latest = latestByDevice[d.id]
              return (
                <tr key={d.id} className="row-link">
                  <td className="mono dim">
                    <Link to={`/devices/${d.id}`} className="row-anchor">{d.id}</Link>
                  </td>
                  <td><DeviceStatus status={d.status} /></td>
                  <td className={latest && latest.temperature > 35 ? 'txt-offline' : ''}>
                    {latest ? latest.temperature.toFixed(1) : '--'}
                  </td>
                  <td className={latest && latest.battery < 20 ? 'txt-offline' : ''}>
                    {latest ? latest.battery.toFixed(0) : '--'}
                  </td>
                  <td className="dim">{fmtDateTimeFull(d.last_seen)}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      )}
    </section>
  )
}
