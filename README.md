# IoT Watch

Lightweight IoT platform for multi-device telemetry monitoring, real-time dashboard, and basic alerting.

## Features

- Multi-device simulated data reporting (MQTT)
- Real-time data collection and storage
- Device online/offline status detection
- Web Dashboard for monitoring
- Basic alerts (temperature, battery, offline)

## Tech Stack

| Layer | Technology |
|-------|------------|
| MQTT Broker | Mosquitto |
| Backend | FastAPI, SQLAlchemy |
| Database | PostgreSQL |
| Frontend | React + Vite |
| Device Simulator | Python (paho-mqtt) |

## Quick Start

1. Start services:
   ```bash
   docker compose -f docker/docker-compose.yml up -d
   ```

2. Run the device simulator (in a separate terminal):
   ```bash
   cd simulator && python main.py
   ```

3. Start the frontend dev server:
   ```bash
   cd frontend && pnpm dev
   ```

4. Open the Dashboard: http://localhost:3000

4. API documentation: http://localhost:8000/docs

## Project Structure

```
├── backend/           # FastAPI backend
│   ├── devices/       # device module
│   ├── telemetry/     # telemetry module
│   ├── alerts/        # alert module
│   ├── main.py
│   └── requirements.txt
├── frontend/          # React + Vite dashboard
│   ├── src/
│   └── package.json
├── simulator/         # device simulator (Python)
│   ├── main.py
│   └── requirements.txt
├── docker/            # Docker compose and config
├── docs/              # project documentation
└── README.md
```

## Documentation

- [Project Overview](docs/project-overview.md)
- [Architecture](docs/architecture.md)
- [Feature List](docs/feature-list.md)
- [Implementation Tasks](docs/tasks.md)
- [API Specification](docs/api-spec.md)

## Conventions

- **Frontend**: Use `pnpm` for package management
- **Backend**: Python 3.11+
- **Docker**: Default development environment
