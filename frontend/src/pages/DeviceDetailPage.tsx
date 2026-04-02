import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from 'react-router-dom'
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
} from 'recharts'
import client from '../api/client'
import type { ApiResponse, Device, TelemetryPage } from '../api/types'

const fmtTime = (iso: string) =>
  new Date(iso).toLocaleTimeString('en-GB', {
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  })

interface MetricProps {
  label: string
  value: string
  unit: string
  warn?: boolean
}

function Metric({ label, value, unit, warn }: MetricProps) {
  return (
    <div className="metric-box">
      <span className="metric-label">{label}</span>
      <span className={`metric-value ${warn ? 'txt-offline' : ''}`}>
        {value}
        <span className="metric-unit"> {unit}</span>
      </span>
    </div>
  )
}

export default function DeviceDetailPage() {
  const { id } = useParams<{ id: string }>()

  const { data: device, isError: deviceError } = useQuery({
    queryKey: ['device', id],
    queryFn: async () => {
      const res = await client.get<ApiResponse<Device>>(`/devices/${id}`)
      return res.data.data
    },
    enabled: !!id,
    refetchInterval: 10_000,
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
    refetchInterval: 10_000,
  })

  const items = telemetryPage?.items ?? []
  const latest = items[0]

  // Chart data: oldest → newest
  const chartData = [...items].reverse().map(r => ({
    t:    fmtTime(r.timestamp),
    temp: r.temperature,
  }))

  if (deviceError) {
    return (
      <section className="page">
        <p className="state-msg error">ERR — device not found</p>
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

      {/* Latest readings */}
      {latest ? (
        <div className="metric-grid">
          <Metric
            label="TEMPERATURE"
            value={latest.temperature.toFixed(1)}
            unit="°C"
            warn={latest.temperature > 35}
          />
          <Metric
            label="HUMIDITY"
            value={latest.humidity.toFixed(1)}
            unit="%"
          />
          <Metric
            label="BATTERY"
            value={latest.battery.toFixed(0)}
            unit="%"
            warn={latest.battery < 20}
          />
        </div>
      ) : (
        !telLoading && <p className="state-msg">NO TELEMETRY YET</p>
      )}

      {/* Temperature chart */}
      {chartData.length > 1 && (
        <div className="chart-section">
          <h2 className="section-title">TEMPERATURE — LAST {chartData.length} READINGS</h2>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={chartData} margin={{ top: 8, right: 16, left: -16, bottom: 0 }}>
                <CartesianGrid
                  strokeDasharray="2 4"
                  stroke="#e0e0e0"
                  vertical={false}
                />
                <XAxis
                  dataKey="t"
                  tick={{ fontSize: 10, fontFamily: 'var(--font)', fill: '#888' }}
                  tickLine={false}
                  axisLine={{ stroke: 'var(--border)' }}
                  interval="preserveStartEnd"
                />
                <YAxis
                  domain={['auto', 'auto']}
                  tick={{ fontSize: 10, fontFamily: 'var(--font)', fill: '#888' }}
                  tickLine={false}
                  axisLine={false}
                  width={40}
                />
                <Tooltip
                  contentStyle={{
                    fontFamily: 'var(--font)',
                    fontSize: 11,
                    border: '1px solid var(--border)',
                    borderRadius: 0,
                    background: '#fff',
                  }}
                  itemStyle={{ color: 'var(--fg)' }}
                  formatter={(v: number) => [`${v.toFixed(1)} °C`, 'Temp']}
                />
                <ReferenceLine
                  y={35}
                  stroke="var(--offline)"
                  strokeDasharray="3 3"
                  label={{ value: '35°C', position: 'right', fontSize: 9, fontFamily: 'var(--font)', fill: 'var(--offline)' }}
                />
                <Line
                  type="monotone"
                  dataKey="temp"
                  stroke="var(--fg)"
                  strokeWidth={1.5}
                  dot={false}
                  activeDot={{ r: 3, fill: 'var(--fg)', strokeWidth: 0 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Raw telemetry table */}
      {items.length > 0 && (
        <div>
          <h2 className="section-title">RAW TELEMETRY</h2>
          <table className="data-table">
            <thead>
              <tr>
                {['Time', 'Temp (°C)', 'Humidity (%)', 'Battery (%)'].map(h => (
                  <th key={h}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {items.map(r => (
                <tr key={r.id}>
                  <td className="dim nowrap">{fmtTime(r.timestamp)}</td>
                  <td className={r.temperature > 35 ? 'txt-offline' : ''}>
                    {r.temperature.toFixed(1)}
                  </td>
                  <td>{r.humidity.toFixed(1)}</td>
                  <td className={r.battery < 20 ? 'txt-offline' : ''}>
                    {r.battery.toFixed(0)}
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
