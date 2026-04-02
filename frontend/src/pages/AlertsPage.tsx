import { useQuery } from '@tanstack/react-query'
import client from '../api/client'
import type { ApiResponse, AlertPage, AlertType } from '../api/types'

const TYPE_LABEL: Record<AlertType, string> = {
  HIGH_TEMPERATURE: 'HIGH TEMP',
  LOW_BATTERY:      'LOW BATT',
  OFFLINE:          'OFFLINE',
}

const TYPE_CLASS: Record<AlertType, string> = {
  HIGH_TEMPERATURE: 'alert-temp',
  LOW_BATTERY:      'alert-batt',
  OFFLINE:          'alert-offline',
}

const fmt = (iso: string) =>
  new Date(iso).toLocaleString('en-GB', {
    year: '2-digit', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  })

const COLS = ['Time', 'Device', 'Type', 'Message'] as const

export default function AlertsPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['alerts'],
    queryFn: async () => {
      const res = await client.get<ApiResponse<AlertPage>>('/alerts?limit=100')
      return res.data.data
    },
    refetchInterval: 3_000,
  })

  const items = data?.items ?? []

  return (
    <section className="page">
      <header className="page-head">
        <h1 className="page-title">ALERTS</h1>
        <div className="page-meta">
          {isLoading ? (
            <span className="meta-chip">LOADING</span>
          ) : (
            <span className="meta-chip">{data?.total ?? 0} TOTAL</span>
          )}
        </div>
      </header>

      {isError && (
        <p className="state-msg error">ERR ? could not reach backend</p>
      )}

      {!isLoading && !isError && items.length === 0 && (
        <p className="state-msg">NO ALERTS</p>
      )}

      {!isLoading && !isError && items.length > 0 && (
        <table className="data-table">
          <thead>
            <tr>
              {COLS.map(h => <th key={h}>{h}</th>)}
            </tr>
          </thead>
          <tbody>
            {items.map(a => (
              <tr key={a.id}>
                <td className="dim nowrap">{fmt(a.timestamp)}</td>
                <td className="mono dim">{a.device_id}</td>
                <td>
                  <span className={`alert-type ${TYPE_CLASS[a.type]}`}>
                    {TYPE_LABEL[a.type]}
                  </span>
                </td>
                <td className="msg">{a.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}
