from datetime import datetime

from sqlalchemy.orm import Session

from telemetry.models import SensorData


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
