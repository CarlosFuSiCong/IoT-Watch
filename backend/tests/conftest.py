import asyncio
from datetime import datetime, timezone
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import devices.models  # noqa: F401 — register with Base
import telemetry.models  # noqa: F401
import alerts.models  # noqa: F401
from alerts.models import Alert, AlertType
from database import Base, get_db
from devices.models import Device, DeviceStatus
from main import app
from telemetry.models import SensorData

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    # StaticPool ensures all checkouts share the same in-memory database
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------------
# Database fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clean_tables():
    """Delete all rows before each test (fastest isolation without drop/recreate)."""
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# ---------------------------------------------------------------------------
# HTTP client fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    async def _noop_checker():
        try:
            await asyncio.sleep(3600)
        except asyncio.CancelledError:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with patch("mqtt.start"), patch("mqtt.stop"), \
            patch("main.offline_checker", _noop_checker):
        with TestClient(app) as c:
            yield c
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Data-builder helpers (return callables so tests can pass custom args)
# ---------------------------------------------------------------------------


@pytest.fixture
def make_device(db):
    def _make(device_id: str = "warehouse-01", status: str = "online") -> Device:
        device = Device(
            id=device_id,
            name=device_id,
            status=DeviceStatus(status),
            last_seen=datetime.now(timezone.utc),
        )
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    return _make


@pytest.fixture
def make_sensor_data(db):
    def _make(
        device_id: str = "warehouse-01",
        temperature: float = 28.0,
        humidity: float = 60.0,
        battery: float = 80.0,
        timestamp: datetime | None = None,
    ) -> SensorData:
        record = SensorData(
            device_id=device_id,
            temperature=temperature,
            humidity=humidity,
            battery=battery,
            timestamp=timestamp or datetime.now(timezone.utc),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    return _make


@pytest.fixture
def make_alert(db):
    def _make(
        device_id: str = "warehouse-01",
        alert_type: str = "HIGH_TEMPERATURE",
        message: str = "test alert",
    ) -> Alert:
        alert = Alert(
            device_id=device_id,
            type=AlertType(alert_type),
            message=message,
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    return _make
