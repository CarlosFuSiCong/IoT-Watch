import asyncio
import logging

from database import SessionLocal
from devices.repository import mark_offline_devices
from alerts.service import create_offline_alerts

logger = logging.getLogger(__name__)

CHECK_INTERVAL_SECONDS = 5


async def offline_checker() -> None:
    """Background task: periodically mark devices offline when last_seen exceeds threshold."""
    logger.info("offline checker started")
    while True:
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)
        db = SessionLocal()
        try:
            stale = mark_offline_devices(db)
            if stale:
                # create offline alerts for newly stale devices
                device_ids = [device.id for device in stale]
                create_offline_alerts(db, device_ids)
                db.commit()
        except Exception:
            db.rollback()
            logger.exception("error during offline check")
        finally:
            db.close()
