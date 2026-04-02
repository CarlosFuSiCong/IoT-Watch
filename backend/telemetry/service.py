import json
import logging
from datetime import datetime

from pydantic import BaseModel, ValidationError

from database import SessionLocal
from devices.repository import get_or_create_device
from telemetry.repository import create_sensor_data, get_previous_telemetry
from alerts.service import check_telemetry_alerts

logger = logging.getLogger(__name__)


class TelemetryPayload(BaseModel):
    device_id: str
    temperature: float
    humidity: float
    battery: float
    timestamp: datetime


def process_message(topic: str, raw: bytes) -> None:
    try:
        data = json.loads(raw)
        payload = TelemetryPayload.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as e:
        logger.warning(f"invalid message on {topic}: {e}")
        return

    db = SessionLocal()
    try:
        get_or_create_device(db, payload.device_id)
        # Fetch previous reading BEFORE inserting the new one (for threshold-crossing detection)
        prev = get_previous_telemetry(db, payload.device_id, payload.timestamp)
        create_sensor_data(
            db,
            device_id=payload.device_id,
            temperature=payload.temperature,
            humidity=payload.humidity,
            battery=payload.battery,
            timestamp=payload.timestamp,
        )
        check_telemetry_alerts(
            db,
            device_id=payload.device_id,
            temperature=payload.temperature,
            battery=payload.battery,
            prev_temperature=prev.temperature if prev else None,
            prev_battery=prev.battery if prev else None,
        )
        db.commit()
        logger.info(
            f"telemetry saved | device={payload.device_id} "
            f"temp={payload.temperature} battery={payload.battery}"
        )
    except Exception:
        db.rollback()
        logger.exception(f"db error processing message on {topic}")
    finally:
        db.close()
