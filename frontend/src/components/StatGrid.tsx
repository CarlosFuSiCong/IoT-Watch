interface StatBoxProps {
  label: string
  value: number | string
  accent?: string
}

function StatBox({ label, value, accent }: StatBoxProps) {
  return (
    <div className="stat-box" style={{ borderLeftColor: accent }}>
      <span className="stat-value">{value}</span>
      <span className="stat-label">{label}</span>
    </div>
  )
}

interface Props {
  total:   number | string
  online:  number | string
  offline: number | string
  alerts:  number | string
}

export default function StatGrid({ total, online, offline, alerts }: Props) {
  return (
    <div className="stat-grid">
      <StatBox label="DEVICES"      value={total}   />
      <StatBox label="ONLINE"       value={online}  accent="var(--online)" />
      <StatBox label="OFFLINE"      value={offline} accent="var(--offline)" />
      <StatBox label="TOTAL ALERTS" value={alerts}  accent="var(--warn)" />
    </div>
  )
}
