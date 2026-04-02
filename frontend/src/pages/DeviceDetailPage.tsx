import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from 'react-router-dom'
import client from '../api/client'
import type { ApiResponse, Device, TelemetryPage, AlertPage } from '../api/types'
import MetricGrid from '../components/MetricGrid'
import TelemetryChart from '../components/TelemetryChart'
import TelemetryTable from '../components/TelemetryTable'
import AlertsTable from '../components/AlertsTable'

export default function DeviceDetailPage() {
  const { id } = useParams<{ id: string }>()

  const { data: device, isError: deviceError } = useQuery({
    queryKey: ['device', id],
    queryFn: async () => {
      const res = await client.get<ApiResponse<Device>>(`/devices/${id}`)
      return res.data.data
    },
    enabled: !!id,
    refetchInterval: 3_000,
  })

  const { data: telemetryPage, isLoading: telLoading } = useQuery({
    queryKey: ['telemetry', id, 'history'],
    queryFn: async () => {
      const res = await client.get<ApiResponse<TelemetryPage>>(
        `/devices/${id}/telemetry?limit=30`
      )
      return res.data.data
    },
    enabled: !!id,
    refetchInterval: 3_000,
  })

  const { data: alertPage } = useQuery({
    queryKey: ['alerts', 'device', id],
    queryFn: async () => {
      const res = await client.get<ApiResponse<AlertPage>>(
        `/alerts?device_id=${id}&limit=20`
      )
      return res.data.data
    },
    enabled: !!id,
    refetchInterval: 3_000,
  })

  const items = telemetryPage?.items ?? []
  const latest = items[0]
  const deviceAlerts = alertPage?.items ?? []

  if (deviceError) {
    return (
      <section className="page">
        <p className="state-msg error">ERR -- device not found</p>
      </section>
    )
  }

  return (
    <section className="page">
      <header className="page-head">
        <h1 className="page-title">
          <Link to="/devices" className="breadcrumb">DEVICES</Link>
          <span className="breadcrumb-sep"> / </span>
          {id}
        </h1>
        {device && (
          <span className={`meta-chip ${device.status}`}>
            {device.status.toUpperCase()}
          </span>
        )}
      </header>

      {latest ? (
        <MetricGrid data={latest} />
      ) : (
        !telLoading && <p className="state-msg">NO TELEMETRY YET</p>
      )}

      <TelemetryChart items={items} />

      <TelemetryTable items={items} />

      <div>
        <h2 className="section-title">
          ALERTS
          {alertPage && alertPage.total > 0 && (
            <span className="section-count">{alertPage.total} TOTAL</span>
          )}
        </h2>
        {deviceAlerts.length === 0 ? (
          <p className="state-msg">NO ALERTS</p>
        ) : (
          <AlertsTable items={deviceAlerts} showDevice={false} />
        )}
      </div>
    </section>
  )
}
