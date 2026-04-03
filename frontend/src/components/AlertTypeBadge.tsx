import type { AlertType } from '../api/types'

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

interface Props { type: AlertType }

export default function AlertTypeBadge({ type }: Props) {
  return (
    <span className={`alert-type ${TYPE_CLASS[type]}`}>
      {TYPE_LABEL[type]}
    </span>
  )
}
