import type { SensorData } from '../api/types'
import { DEG_C } from '../lib/utils'

interface MetricBoxProps {
  label: string
  value: string
  unit: string
  warn?: boolean
}

function MetricBox({ label, value, unit, warn }: MetricBoxProps) {
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

interface Props {
  data: SensorData
}

export default function MetricGrid({ data }: Props) {
  return (
    <div className="metric-grid">
      <MetricBox
        label="TEMPERATURE"
        value={data.temperature.toFixed(1)}
        unit={DEG_C}
        warn={data.temperature > 35}
      />
      <MetricBox
        label="HUMIDITY"
        value={data.humidity.toFixed(1)}
        unit="%"
      />
      <MetricBox
        label="BATTERY"
        value={data.battery.toFixed(0)}
        unit="%"
        warn={data.battery < 20}
      />
    </div>
  )
}
