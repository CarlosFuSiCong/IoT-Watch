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
import type { SensorData } from '../api/types'
import { DEG_C, fmtTime } from '../lib/utils'

interface Props {
  items: SensorData[]
}

export default function TelemetryChart({ items }: Props) {
  const chartData = [...items].reverse().map(r => ({
    t:    fmtTime(r.timestamp),
    temp: r.temperature,
  }))

  if (chartData.length < 2) return null

  return (
    <div className="chart-section">
      <h2 className="section-title">TEMPERATURE -- LAST {chartData.length} READINGS</h2>
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={chartData} margin={{ top: 8, right: 16, left: -16, bottom: 0 }}>
            <CartesianGrid strokeDasharray="2 4" stroke="#e0e0e0" vertical={false} />
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
              formatter={(v) => {
                const n = typeof v === 'number' ? v : Number(Array.isArray(v) ? v[0] : v)
                return [`${n.toFixed(1)} ${DEG_C}`, 'Temp'] as [string, string]
              }}
            />
            <ReferenceLine
              y={35}
              stroke="var(--offline)"
              strokeDasharray="3 3"
              label={{
                value: `35 ${DEG_C}`,
                position: 'right',
                fontSize: 9,
                fontFamily: 'var(--font)',
                fill: 'var(--offline)',
              }}
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
  )
}
