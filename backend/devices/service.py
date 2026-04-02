import asyncio
import logging

from database import SessionLocal
from devices.repository import mark_offline_devices
from alerts.service import create_offline_alerts

logger = logging.getLogger(__name__)

CHECK_INTERVAL_SECONDS = 5


def _run_mark_offline() -> list[str]:
    """Runs in a thread: marks stale devices offline and returns their IDs."""
    db = SessionLocal()
    try:
        stale = mark_offline_devices(db)
        db.commit()
        return [d.id for d in stale]
    except Exception:
        db.rollback()
        logger.exception("error marking devices offline")
        return []
    finally:
        db.close()


def _run_create_alerts(device_ids: list[str]) -> None:
    """Runs in a thread: creates offline alerts for the given device IDs."""
    db = SessionLocal()
    try:
        create_offline_alerts(db, device_ids)
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("error creating offline alerts")
    finally:
        db.close()


async def offline_checker() -> None:
    """Background task: periodically mark devices offline when last_seen exceeds threshold."""
    logger.info("offline checker started")
    while True:
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

        # Run blocking DB work in a thread so the event loop stays responsive
        device_ids = await asyncio.to_thread(_run_mark_offline)

        if not device_ids:
            continue

        # Separate transaction: alert failures must not roll back device status changes
        await asyncio.to_thread(_run_create_alerts, device_ids)
