from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from telemetry.models import SensorData


def list_telemetry(
    db: Session,
    device_id: str,
    page: int = 1,
    limit: int = 50,
) -> tuple[list[SensorData], int]:
    base = select(SensorData).where(SensorData.device_id == device_id)
    total = db.scalar(select(func.count()).select_from(base.subquery())) or 0
    items = list(
        db.scalars(
            base.order_by(SensorData.timestamp.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        ).all()
    )
    return items, total


def create_sensor_data(
    db: Session,
    device_id: str,
    temperature: float,
    humidity: float,
    battery: float,
    timestamp: datetime,
) -> SensorData:
    record = SensorData(
        device_id=device_id,
        temperature=temperature,
        humidity=humidity,
        battery=battery,
        timestamp=timestamp,
    )
    db.add(record)
    return record
