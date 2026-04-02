import { useQuery } from '@tanstack/react-query'
import client from '../api/client'
import type { ApiResponse, AlertPage, AlertType } from '../api/types'

const TYPE_COLORS: Record<AlertType, { bg: string; fg: string }> = {
  HIGH_TEMPERATURE: { bg: '#fff3cd', fg: '#856404' },
  LOW_BATTERY:      { bg: '#fce4ec', fg: '#880e4f' },
  OFFLINE:          { bg: '#ede7f6', fg: '#4527a0' },
}

function typeBadge(type: AlertType) {
  const { bg, fg } = TYPE_COLORS[type] ?? { bg: '#eee', fg: '#333' }
  return (
    <span style={{ padding: '2px 10px', borderRadius: 12, fontSize: '0.8rem', fontWeight: 600, background: bg, color: fg }}>
      {type.replace('_', ' ')}
    </span>
  )
}

export default function AlertsPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['alerts'],
    queryFn: async () => {
      const res = await client.get<ApiResponse<AlertPage>>('/alerts?limit=100')
      return res.data.data
    },
    refetchInterval: 15_000,
  })

  if (isLoading) return <p>Loading alerts…</p>
  if (isError) return <p style={{ color: 'red' }}>Failed to load alerts.</p>

  const items = data?.items ?? []

  return (
    <section>
      <h2 style={{ marginBottom: '1rem' }}>Alerts ({data?.total ?? 0})</h2>
      {!items.length ? (
        <p>No alerts yet.</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff', borderRadius: 8, overflow: 'hidden', boxShadow: '0 1px 4px rgba(0,0,0,.08)' }}>
          <thead style={{ background: '#f0f0f5' }}>
            <tr>
              {['Time', 'Device', 'Type', 'Message'].map(h => (
                <th key={h} style={{ padding: '10px 14px', textAlign: 'left', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {items.map((a, i) => (
              <tr key={a.id} style={{ borderTop: i ? '1px solid #eee' : undefined }}>
                <td style={{ padding: '10px 14px', color: '#666', fontSize: '0.85rem', whiteSpace: 'nowrap' }}>{new Date(a.timestamp).toLocaleString()}</td>
                <td style={{ padding: '10px 14px', fontFamily: 'monospace' }}>{a.device_id}</td>
                <td style={{ padding: '10px 14px' }}>{typeBadge(a.type)}</td>
                <td style={{ padding: '10px 14px', color: '#444' }}>{a.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}
