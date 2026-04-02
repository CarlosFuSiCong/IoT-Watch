import logging
from typing import List

from sqlalchemy.orm import Session

from alerts.models import AlertType
from alerts.repository import (
    check_and_create_alert,
    AlertThresholds,
)

logger = logging.getLogger(__name__)


def check_temperature_alert(db: Session, device_id: str, temperature: float) -> None:
    """Create a HIGH_TEMPERATURE alert if temperature exceeds the threshold."""
    if temperature > AlertThresholds.HIGH_TEMPERATURE:
        message = (
            f"Device {device_id} temperature too high: "
            f"{temperature:.1f}°C (threshold: {AlertThresholds.HIGH_TEMPERATURE}°C)"
        )
        check_and_create_alert(
            db,
            device_id=device_id,
            alert_type=AlertType.HIGH_TEMPERATURE,
            message=message,
        )


def check_battery_alert(db: Session, device_id: str, battery: float) -> None:
    """Create a LOW_BATTERY alert if battery level is below the threshold."""
    if battery < AlertThresholds.LOW_BATTERY:
        message = (
            f"Device {device_id} battery low: "
            f"{battery:.1f}% (threshold: {AlertThresholds.LOW_BATTERY}%)"
        )
        check_and_create_alert(
            db,
            device_id=device_id,
            alert_type=AlertType.LOW_BATTERY,
            message=message,
        )


def check_telemetry_alerts(
    db: Session,
    device_id: str,
    temperature: float,
    battery: float,
) -> None:
    """Run all telemetry-based alert checks (temperature, battery) for an incoming message."""
    check_temperature_alert(db, device_id, temperature)
    check_battery_alert(db, device_id, battery)


def create_offline_alerts(db: Session, device_ids: List[str]) -> None:
    """Create OFFLINE alerts for devices that just transitioned online → offline."""
    for device_id in device_ids:
        message = f"Device {device_id} went offline"
        check_and_create_alert(
            db,
            device_id=device_id,
            alert_type=AlertType.OFFLINE,
            message=message,
        )
