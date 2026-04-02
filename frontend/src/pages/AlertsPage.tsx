import { useQuery } from '@tanstack/react-query'
import client from '../api/client'
import type { ApiResponse, AlertPage } from '../api/types'
import AlertsTable from '../components/AlertsTable'

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

      {isError && <p className="state-msg error">ERR -- could not reach backend</p>}

      {!isLoading && !isError && items.length === 0 && (
        <p className="state-msg">NO ALERTS</p>
      )}

      {!isLoading && !isError && items.length > 0 && (
        <AlertsTable items={items} showDevice />
      )}
    </section>
  )
}
