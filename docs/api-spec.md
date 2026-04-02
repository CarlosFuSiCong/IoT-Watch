# IoT Watch — API Specification

Base URL: `http://localhost:8000`

## Response Format

All endpoints return a consistent structure:

**Success:**
```json
{
  "success": true,
  "data": { ... }
}
```

**Error:**
```json
{
  "success": false,
  "message": "Error description",
  "errors": []
}
```

---

## Devices

### GET /devices

List all devices.

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "warehouse-01",
      "name": "warehouse-01",
      "status": "online",
      "last_seen": "2025-03-21T10:30:00Z",
      "created_at": "2025-03-21T08:00:00Z"
    }
  ]
}
```

### GET /devices/{id}

Get device detail.

**Parameters:**
- `id` (path): Device ID

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "warehouse-01",
    "name": "warehouse-01",
    "status": "online",
    "last_seen": "2025-03-21T10:30:00Z",
    "created_at": "2025-03-21T08:00:00Z"
  }
}
```

**Response (404):**
```json
{
  "success": false,
  "message": "Device not found"
}
```

---

## Telemetry

### GET /devices/{id}/telemetry

Get device historical telemetry data (paginated).

**Parameters:**
- `id` (path): Device ID
- `page` (query, optional): Page number, default 1
- `limit` (query, optional): Items per page, default 50

**Response (200):**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "device_id": "warehouse-01",
        "temperature": 28.4,
        "humidity": 60.2,
        "battery": 87,
        "timestamp": "2025-03-21T10:30:00Z"
      }
    ],
    "total": 100,
    "page": 1,
    "limit": 50
  }
}
```

---

## Alerts

### GET /alerts

List alerts with optional filters.

**Parameters:**
- `device_id` (query, optional): Filter by device
- `type` (query, optional): Filter by alert type (HIGH_TEMPERATURE, LOW_BATTERY, OFFLINE)
- `page` (query, optional): Page number
- `limit` (query, optional): Items per page

**Response (200):**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "device_id": "warehouse-01",
        "type": "HIGH_TEMPERATURE",
        "message": "Temperature exceeds threshold",
        "timestamp": "2025-03-21T10:30:00Z"
      }
    ],
    "total": 10,
    "page": 1,
    "limit": 50
  }
}
```

---

## Health Check

### GET /health

Optional health check for Docker.

**Response (200):**
```json
{
  "status": "ok"
}
```
