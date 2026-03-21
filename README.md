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
| Frontend | Next.js |
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

3. Open the Dashboard: http://localhost:8000

4. API documentation: http://localhost:8000/docs

## Project Structure

```
├── backend/           # FastAPI 后端
│   ├── devices/       # 设备模块
│   ├── telemetry/     # 遥测模块
│   ├── alerts/        # 告警模块
│   ├── main.py
│   └── requirements.txt
├── frontend/          # Next.js Dashboard
│   ├── app/
│   └── package.json
├── simulator/         # 设备模拟器 (Python)
│   ├── main.py
│   └── requirements.txt
├── docker/            # Docker 编排与配置
├── docs/              # 项目文档
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
