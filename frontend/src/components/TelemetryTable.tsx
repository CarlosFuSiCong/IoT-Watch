import type { SensorData } from '../api/types'
import { DEG_C, fmtTime } from '../lib/utils'

interface Props {
  items: SensorData[]
}

export default function TelemetryTable({ items }: Props) {
  if (items.length === 0) return null

  return (
    <div>
      <h2 className="section-title">RAW TELEMETRY</h2>
      <table className="data-table">
        <thead>
          <tr>
            {['Time', `Temp (${DEG_C})`, 'Humidity (%)', 'Battery (%)'].map(h => (
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
  )
}
