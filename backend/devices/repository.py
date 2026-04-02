import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from devices.models import Device, DeviceStatus

logger = logging.getLogger(__name__)


def get_or_create_device(db: Session, device_id: str) -> Device:
    device = db.get(Device, device_id)
    now = datetime.now(timezone.utc)

    if device is None:
        device = Device(
            id=device_id,
            name=device_id,
            status=DeviceStatus.online,
            last_seen=now,
        )
        db.add(device)
        logger.info(f"registered new device: {device_id}")
    else:
        device.status = DeviceStatus.online
        device.last_seen = now

    return device
