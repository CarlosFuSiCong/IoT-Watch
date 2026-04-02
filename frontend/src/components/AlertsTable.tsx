import type { AlertItem } from '../api/types'
import AlertTypeBadge from './AlertTypeBadge'
import { fmtDateTimeFull } from '../lib/utils'

interface Props {
  items: AlertItem[]
  /** Show the device_id column (default true). Hide when already in device context. */
  showDevice?: boolean
}

export default function AlertsTable({ items, showDevice = true }: Props) {
  const cols = showDevice
    ? ['Time', 'Device', 'Type', 'Message']
    : ['Time', 'Type', 'Message']

  return (
    <table className="data-table">
      <thead>
        <tr>{cols.map(h => <th key={h}>{h}</th>)}</tr>
      </thead>
      <tbody>
        {items.map(a => (
          <tr key={a.id}>
            <td className="dim nowrap">{fmtDateTimeFull(a.timestamp)}</td>
            {showDevice && <td className="mono dim">{a.device_id}</td>}
            <td><AlertTypeBadge type={a.type} /></td>
            <td className="msg">{a.message}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
