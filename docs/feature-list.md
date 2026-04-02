# IoT Watch — Feature List

## MVP (Must Have)

| Category | Feature | Description |
|----------|---------|-------------|
| Device simulation | ≥3 devices | Simulate warehouse-01, warehouse-02, warehouse-03 |
| Device simulation | 2–5s interval | Publish telemetry every 2–5 seconds |
| Device simulation | Telemetry JSON | `device_id`, `temperature`, `humidity`, `battery`, `timestamp` (ISO8601) |
| MQTT | Mosquitto Broker | Publish and subscribe via MQTT |
| MQTT | Topic | `devices/{device_id}/telemetry` |
| Backend | Auto device registration | Create Device record when new `device_id` is received |
| Backend | SensorData storage | Persist each telemetry message |
| Status | Online/offline | 10-second threshold for offline |
| Alerts | HIGH_TEMPERATURE | Trigger when `temperature > 35` |
| Alerts | LOW_BATTERY | Trigger when `battery < 20` |
| Alerts | OFFLINE | Trigger when device goes offline |
| API | GET /devices | List all devices |
| API | GET /devices/{id} | Device detail |
| API | GET /devices/{id}/telemetry | Historical data (paginated) |
| API | GET /alerts | Alert list |
| Dashboard | Overview | Device count, online/offline, alert count |
| Dashboard | Device list | Table: Device, Status, Temp, Battery |
| Dashboard | Device detail | Real-time data, temperature/humidity/battery charts |
| Dashboard | Alert panel | Alert type, device, time, status |

## Optional (Enhancements)

| Category | Feature |
|----------|---------|
| Real-time | WebSocket push to frontend |
| AI | Simple anomaly detection |
| Management | Device CRUD (create, update, delete) |
| Deployment | Full Docker Compose (all services) |
