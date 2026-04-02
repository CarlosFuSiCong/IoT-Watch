import json
import logging
from datetime import datetime

from pydantic import BaseModel, ValidationError

from database import SessionLocal
from devices.repository import get_or_create_device
from telemetry.repository import create_sensor_data
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
        create_sensor_data(
            db,
            device_id=payload.device_id,
            temperature=payload.temperature,
            humidity=payload.humidity,
            battery=payload.battery,
            timestamp=payload.timestamp,
        )
        # check temperature and battery alerts
        check_telemetry_alerts(
            db,
            device_id=payload.device_id,
            temperature=payload.temperature,
            battery=payload.battery,
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
