import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select, and_
from sqlalchemy.orm import Session

from alerts.models import Alert, AlertType

logger = logging.getLogger(__name__)

ALERT_DEDUPLICATION_SECONDS = 300


class AlertThresholds:
    HIGH_TEMPERATURE = 35.0
    LOW_BATTERY = 20.0


def list_alerts(
    db: Session,
    device_id: str | None = None,
    alert_type: AlertType | None = None,
    page: int = 1,
    limit: int = 50,
) -> tuple[list[Alert], int]:
    filters = []
    if device_id is not None:
        filters.append(Alert.device_id == device_id)
    if alert_type is not None:
        filters.append(Alert.type == alert_type)

    base = select(Alert).where(and_(True, *filters))
    total = db.scalar(select(func.count()).select_from(base.subquery())) or 0
    items = list(
        db.scalars(
            base.order_by(Alert.timestamp.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        ).all()
    )
    return items, total


def create_alert(
    db: Session,
    device_id: str,
    alert_type: AlertType,
    message: str,
) -> Alert:
    alert = Alert(
        device_id=device_id,
        type=alert_type,
        message=message,
    )
    db.add(alert)
    logger.info(f"alert created | device={device_id} type={alert_type.value} msg={message}")
    return alert


def has_recent_alert(
    db: Session,
    device_id: str,
    alert_type: AlertType,
    seconds: int = ALERT_DEDUPLICATION_SECONDS,
) -> bool:
    """Return True if a same-type alert exists for this device within the time window."""
    cutoff = datetime.now(timezone.utc) - timedelta(seconds=seconds)
    stmt = select(Alert).where(
        and_(
            Alert.device_id == device_id,
            Alert.type == alert_type,
            Alert.timestamp >= cutoff,
        )
    )
    result = db.execute(stmt).first()
    return result is not None


def check_and_create_alert(
    db: Session,
    device_id: str,
    alert_type: AlertType,
    message: str,
    deduplicate: bool = True,
) -> Alert | None:
    """
    Create an alert, skipping creation if a duplicate exists within the deduplication window.
    Returns the created Alert or None if deduplicated.
    """
    if deduplicate and has_recent_alert(db, device_id, alert_type):
        logger.debug(f"alert deduplicated | device={device_id} type={alert_type.value}")
        return None

    return create_alert(db, device_id, alert_type, message)
