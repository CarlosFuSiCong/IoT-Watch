import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from devices.models import Device, DeviceStatus

logger = logging.getLogger(__name__)

OFFLINE_THRESHOLD_SECONDS = 10


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


def mark_offline_devices(db: Session) -> list[Device]:
    """Mark devices as offline if last_seen exceeded the threshold. Returns affected devices."""
    cutoff = datetime.now(timezone.utc) - timedelta(seconds=OFFLINE_THRESHOLD_SECONDS)
    stmt = select(Device).where(
        Device.status == DeviceStatus.online,
        Device.last_seen < cutoff,
    )
    stale = db.scalars(stmt).all()
    for device in stale:
        device.status = DeviceStatus.offline
        logger.info(f"device offline: {device.id} (last_seen={device.last_seen})")
    return list(stale)
