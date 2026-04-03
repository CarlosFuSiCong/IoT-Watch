# IoT Watch

Lightweight IoT platform for multi-device telemetry monitoring, real-time dashboard, and automated alerting.

## Features

- Multi-device telemetry simulation via MQTT
- Real-time device online/offline detection
- Threshold-based alerting (high temperature, low battery, device offline)
- State-transition deduplication — alerts fire once per crossing, not continuously
- Interactive web dashboard with live 3-second polling
- One-click demo simulator (start/stop from the UI)
- Paginated REST API with filtering

## Tech Stack

| Layer | Technology |
|-------|------------|
| MQTT Broker | Mosquitto |
| Backend | FastAPI, SQLAlchemy, Alembic |
| Database | PostgreSQL |
| Frontend | React 19 + Vite + TanStack Query |
| Device Simulator | Python (paho-mqtt) |

## Quick Start

### Option A — Full stack with Docker (recommended)

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

| Service | URL |
|---------|-----|
| Dashboard | http://localhost |
| API | http://localhost:8000 |
| API docs | http://localhost:8000/docs |

### Option B — Local development

1. Start infrastructure (MQTT + PostgreSQL):
   ```bash
   docker compose -f docker/docker-compose.yml up -d mqtt db
   ```

2. Run database migrations and start the backend:
   ```bash
   cd backend
   alembic upgrade head
   uvicorn main:app --reload
   ```

3. Start the frontend dev server:
   ```bash
   cd frontend && pnpm dev
   ```

4. Open the dashboard: http://localhost:3000

The device simulator can be started from the **SIMULATE** button in the dashboard UI,
or run manually:
```bash
cd simulator && python main.py
```

## Project Structure

```
├── backend/           # FastAPI backend
│   ├── alerts/        # alert thresholds, deduplication, service
│   ├── devices/       # device registry, offline checker
│   ├── telemetry/     # MQTT ingestion, sensor data storage
│   ├── demo/          # simulator start/stop API
│   ├── tests/         # pytest suite (SQLite in-memory)
│   ├── alembic/       # database migrations
│   ├── main.py
│   └── requirements.txt
├── frontend/          # React + Vite dashboard
│   ├── src/
│   │   ├── api/       # axios client and TypeScript types
│   │   ├── components/ # reusable UI components
│   │   ├── lib/       # shared formatters and constants
│   │   └── pages/     # Overview, Devices, Device Detail, Alerts
│   └── package.json
├── simulator/         # device simulator (Python, paho-mqtt)
│   ├── main.py
│   └── requirements.txt
├── docker/            # Docker Compose, Dockerfiles, nginx config
├── docs/              # project documentation
└── README.md
```

## Alerting Logic

| Alert Type | Trigger | Deduplication |
|------------|---------|---------------|
| `HIGH_TEMPERATURE` | Temperature rises above 35 °C | Fires once per upward crossing |
| `LOW_BATTERY` | Battery drops below 20 % | Fires once per downward crossing |
| `OFFLINE` | No telemetry received for > 8 s | Fires once per online → offline transition |

## API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/devices` | List all devices |
| `GET` | `/devices/{id}` | Get a single device |
| `GET` | `/devices/{id}/telemetry` | Paginated telemetry history |
| `GET` | `/alerts` | Paginated alerts (filterable by device, type) |
| `POST` | `/demo/start` | Start the device simulator |
| `POST` | `/demo/stop` | Stop the device simulator |
| `GET` | `/demo/status` | Check simulator running state |
| `GET` | `/health` | Health check |

Full interactive docs: http://localhost:8000/docs

## Development

```bash
# Run backend tests
cd backend && pytest

# Lint frontend
cd frontend && pnpm lint

# Build frontend for production
cd frontend && pnpm build
```

## Conventions

- **Frontend**: `pnpm` for package management
- **Backend**: Python 3.12+
- **Docker**: used for infrastructure in both dev and production
