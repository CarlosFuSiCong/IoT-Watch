export interface ApiResponse<T> {
  success: boolean
  data: T | null
  message: string | null
}

export interface Device {
  id: string
  name: string
  status: 'online' | 'offline'
  last_seen: string
  created_at: string
}

export interface SensorData {
  id: number
  device_id: string
  temperature: number
  humidity: number
  battery: number
  timestamp: string
}

export interface TelemetryPage {
  items: SensorData[]
  total: number
  page: number
  limit: number
}

export type AlertType = 'HIGH_TEMPERATURE' | 'LOW_BATTERY' | 'OFFLINE'

export interface AlertItem {
  id: number
  device_id: string
  type: AlertType
  message: string
  timestamp: string
}

export interface AlertPage {
  items: AlertItem[]
  total: number
  page: number
  limit: number
}
