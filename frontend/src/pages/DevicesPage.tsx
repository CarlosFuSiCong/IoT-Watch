import { useQuery } from '@tanstack/react-query'
import client from '../api/client'
import type { ApiResponse, Device } from '../api/types'

function statusBadge(status: string) {
  return (
    <span style={{
      padding: '2px 10px',
      borderRadius: 12,
      fontSize: '0.8rem',
      fontWeight: 600,
      background: status === 'online' ? '#d1fae5' : '#fee2e2',
      color: status === 'online' ? '#065f46' : '#991b1b',
    }}>
      {status}
    </span>
  )
}

export default function DevicesPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['devices'],
    queryFn: async () => {
      const res = await client.get<ApiResponse<Device[]>>('/devices')
      return res.data.data ?? []
    },
    refetchInterval: 10_000,
  })

  if (isLoading) return <p>Loading devices…</p>
  if (isError) return <p style={{ color: 'red' }}>Failed to load devices.</p>
  if (!data?.length) return <p>No devices registered yet.</p>

  return (
    <section>
      <h2 style={{ marginBottom: '1rem' }}>Devices ({data.length})</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff', borderRadius: 8, overflow: 'hidden', boxShadow: '0 1px 4px rgba(0,0,0,.08)' }}>
        <thead style={{ background: '#f0f0f5' }}>
          <tr>
            {['ID', 'Name', 'Status', 'Last Seen'].map(h => (
              <th key={h} style={{ padding: '10px 14px', textAlign: 'left', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((d, i) => (
            <tr key={d.id} style={{ borderTop: i ? '1px solid #eee' : undefined }}>
              <td style={{ padding: '10px 14px', fontFamily: 'monospace' }}>{d.id}</td>
              <td style={{ padding: '10px 14px' }}>{d.name}</td>
              <td style={{ padding: '10px 14px' }}>{statusBadge(d.status)}</td>
              <td style={{ padding: '10px 14px', color: '#666', fontSize: '0.85rem' }}>{new Date(d.last_seen).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  )
}
