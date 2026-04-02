import { useQuery } from '@tanstack/react-query'
import client from '../api/client'
import type { ApiResponse, Device } from '../api/types'

const fmt = (iso: string) =>
  new Date(iso).toLocaleString('en-GB', {
    year: '2-digit', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  })

const COLS = ['ID', 'Name', 'Status', 'Last Seen'] as const

export default function DevicesPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['devices'],
    queryFn: async () => {
      const res = await client.get<ApiResponse<Device[]>>('/devices')
      return res.data.data ?? []
    },
    refetchInterval: 10_000,
  })

  const online = data?.filter(d => d.status === 'online').length ?? 0
  const total  = data?.length ?? 0

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

      {isError && (
        <p className="state-msg error">ERR — could not reach backend</p>
      )}

      {!isLoading && !isError && total === 0 && (
        <p className="state-msg">NO DEVICES REGISTERED</p>
      )}

      {!isLoading && !isError && total > 0 && (
        <table className="data-table">
          <thead>
            <tr>
              {COLS.map(h => <th key={h}>{h}</th>)}
            </tr>
          </thead>
          <tbody>
            {data!.map(d => (
              <tr key={d.id}>
                <td className="mono dim">{d.id}</td>
                <td>{d.name}</td>
                <td>
                  <span className={`status-dot ${d.status}`}>●</span>
                  {' '}
                  <span className={d.status === 'online' ? 'txt-online' : 'txt-offline'}>
                    {d.status.toUpperCase()}
                  </span>
                </td>
                <td className="dim">{fmt(d.last_seen)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}
