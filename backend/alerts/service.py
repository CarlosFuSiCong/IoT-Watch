import logging
from typing import List

from sqlalchemy.orm import Session

from alerts.models import AlertType
from alerts.repository import (
    check_and_create_alert,
    AlertThresholds,
)

logger = logging.getLogger(__name__)


def check_temperature_alert(
    db: Session,
    device_id: str,
    temperature: float,
    prev_temperature: float | None = None,
) -> None:
    """Create a HIGH_TEMPERATURE alert only when temperature crosses the threshold upward."""
    if temperature <= AlertThresholds.HIGH_TEMPERATURE:
        return
    # Skip if the previous reading was already above threshold (continuous high-temp state)
    if prev_temperature is not None and prev_temperature > AlertThresholds.HIGH_TEMPERATURE:
        return
    message = (
        f"Device {device_id} temperature too high: "
        f"{temperature:.1f}\u00b0C (threshold: {AlertThresholds.HIGH_TEMPERATURE}\u00b0C)"
    )
    check_and_create_alert(
        db,
        device_id=device_id,
        alert_type=AlertType.HIGH_TEMPERATURE,
        message=message,
        deduplicate=False,
    )


def check_battery_alert(
    db: Session,
    device_id: str,
    battery: float,
    prev_battery: float | None = None,
) -> None:
    """Create a LOW_BATTERY alert only when battery crosses the threshold downward."""
    if battery >= AlertThresholds.LOW_BATTERY:
        return
    # Skip if the previous reading was already below threshold (continuous low-battery state)
    if prev_battery is not None and prev_battery < AlertThresholds.LOW_BATTERY:
        return
    message = (
        f"Device {device_id} battery low: "
        f"{battery:.1f}% (threshold: {AlertThresholds.LOW_BATTERY}%)"
    )
    check_and_create_alert(
        db,
        device_id=device_id,
        alert_type=AlertType.LOW_BATTERY,
        message=message,
        deduplicate=False,
    )


def check_telemetry_alerts(
    db: Session,
    device_id: str,
    temperature: float,
    battery: float,
    prev_temperature: float | None = None,
    prev_battery: float | None = None,
) -> None:
    """Run all telemetry-based alert checks for an incoming message."""
    check_temperature_alert(db, device_id, temperature, prev_temperature)
    check_battery_alert(db, device_id, battery, prev_battery)


def create_offline_alerts(db: Session, device_ids: List[str]) -> None:
    """Create OFFLINE alerts for devices that just transitioned online -> offline.

    No deduplication needed: mark_offline_devices already guarantees each device
    appears here at most once per online->offline transition.
    """
    for device_id in device_ids:
        message = f"Device {device_id} went offline"
        check_and_create_alert(
            db,
            device_id=device_id,
            alert_type=AlertType.OFFLINE,
            message=message,
            deduplicate=False,
        )
