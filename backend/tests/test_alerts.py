"""Tests for GET /alerts and alert business logic (thresholds, deduplication)."""
from datetime import datetime, timedelta, timezone

import pytest

from alerts.models import Alert, AlertType
from alerts.repository import check_and_create_alert, has_recent_alert
from alerts.service import check_battery_alert, check_temperature_alert


# ---------------------------------------------------------------------------
# API: GET /alerts
# ---------------------------------------------------------------------------


def test_list_alerts_empty(client):
    resp = client.get("/alerts")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["items"] == []
    assert body["data"]["total"] == 0


def test_list_alerts_returns_all(client, make_device, make_alert):
    make_device("warehouse-01")
    make_device("warehouse-02")
    make_alert("warehouse-01", "HIGH_TEMPERATURE")
    make_alert("warehouse-02", "LOW_BATTERY")

    resp = client.get("/alerts")
    data = resp.json()["data"]
    assert data["total"] == 2
    types = {a["type"] for a in data["items"]}
    assert types == {"HIGH_TEMPERATURE", "LOW_BATTERY"}


def test_list_alerts_filter_by_device_id(client, make_device, make_alert):
    make_device("warehouse-01")
    make_device("warehouse-02")
    make_alert("warehouse-01", "HIGH_TEMPERATURE")
    make_alert("warehouse-02", "LOW_BATTERY")

    resp = client.get("/alerts?device_id=warehouse-01")
    data = resp.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["device_id"] == "warehouse-01"


def test_list_alerts_filter_by_type(client, make_device, make_alert):
    make_device("warehouse-01")
    make_alert("warehouse-01", "HIGH_TEMPERATURE")
    make_alert("warehouse-01", "LOW_BATTERY")
    make_alert("warehouse-01", "OFFLINE")

    resp = client.get("/alerts?type=LOW_BATTERY")
    data = resp.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["type"] == "LOW_BATTERY"


def test_list_alerts_filter_combined(client, make_device, make_alert):
    make_device("warehouse-01")
    make_device("warehouse-02")
    make_alert("warehouse-01", "LOW_BATTERY")
    make_alert("warehouse-02", "LOW_BATTERY")
    make_alert("warehouse-01", "HIGH_TEMPERATURE")

    resp = client.get("/alerts?device_id=warehouse-01&type=LOW_BATTERY")
    data = resp.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["device_id"] == "warehouse-01"
    assert data["items"][0]["type"] == "LOW_BATTERY"


def test_list_alerts_pagination(client, make_device, make_alert):
    make_device("warehouse-01")
    for _ in range(5):
        make_alert("warehouse-01", "HIGH_TEMPERATURE")

    resp = client.get("/alerts?page=1&limit=2")
    data = resp.json()["data"]
    assert data["total"] == 5
    assert len(data["items"]) == 2


def test_list_alerts_ordered_newest_first(client, make_device, db):
    from alerts.models import Alert, AlertType

    make_device("warehouse-01")
    now = datetime.now(timezone.utc)
    db.add(Alert(device_id="warehouse-01", type=AlertType.OFFLINE,
                 message="old", timestamp=now - timedelta(minutes=10)))
    db.add(Alert(device_id="warehouse-01", type=AlertType.HIGH_TEMPERATURE,
                 message="new", timestamp=now))
    db.commit()

    resp = client.get("/alerts")
    items = resp.json()["data"]["items"]
    assert items[0]["type"] == "HIGH_TEMPERATURE"
    assert items[1]["type"] == "OFFLINE"


def test_alert_response_fields(client, make_device, make_alert):
    make_device("warehouse-01")
    make_alert("warehouse-01", "OFFLINE", "Device went offline")

    item = client.get("/alerts").json()["data"]["items"][0]
    assert "id" in item
    assert item["device_id"] == "warehouse-01"
    assert item["type"] == "OFFLINE"
    assert item["message"] == "Device went offline"
    assert "timestamp" in item


# ---------------------------------------------------------------------------
# Business logic: alert thresholds
# ---------------------------------------------------------------------------


def test_high_temperature_alert_created(db, make_device):
    make_device("warehouse-01")
    check_temperature_alert(db, "warehouse-01", 36.0)
    db.commit()

    alerts = db.query(Alert).all()
    assert len(alerts) == 1
    assert alerts[0].type == AlertType.HIGH_TEMPERATURE


def test_no_alert_at_temperature_threshold(db, make_device):
    make_device("warehouse-01")
    check_temperature_alert(db, "warehouse-01", 35.0)  # exactly at threshold
    db.commit()

    assert db.query(Alert).count() == 0


def test_no_alert_below_temperature_threshold(db, make_device):
    make_device("warehouse-01")
    check_temperature_alert(db, "warehouse-01", 30.0)
    db.commit()

    assert db.query(Alert).count() == 0


def test_low_battery_alert_created(db, make_device):
    make_device("warehouse-01")
    check_battery_alert(db, "warehouse-01", 15.0)
    db.commit()

    alerts = db.query(Alert).all()
    assert len(alerts) == 1
    assert alerts[0].type == AlertType.LOW_BATTERY


def test_no_alert_at_battery_threshold(db, make_device):
    make_device("warehouse-01")
    check_battery_alert(db, "warehouse-01", 20.0)  # exactly at threshold
    db.commit()

    assert db.query(Alert).count() == 0


def test_no_alert_above_battery_threshold(db, make_device):
    make_device("warehouse-01")
    check_battery_alert(db, "warehouse-01", 50.0)
    db.commit()

    assert db.query(Alert).count() == 0


# ---------------------------------------------------------------------------
# Business logic: deduplication
# ---------------------------------------------------------------------------


def test_deduplication_blocks_repeat_within_window(db, make_device):
    make_device("warehouse-01")
    check_and_create_alert(db, "warehouse-01", AlertType.HIGH_TEMPERATURE, "first")
    db.commit()
    check_and_create_alert(db, "warehouse-01", AlertType.HIGH_TEMPERATURE, "second")
    db.commit()

    assert db.query(Alert).count() == 1


def test_deduplication_allows_different_type(db, make_device):
    make_device("warehouse-01")
    check_and_create_alert(db, "warehouse-01", AlertType.HIGH_TEMPERATURE, "temp alert")
    db.commit()
    check_and_create_alert(db, "warehouse-01", AlertType.LOW_BATTERY, "battery alert")
    db.commit()

    assert db.query(Alert).count() == 2


def test_deduplication_allows_different_device(db, make_device):
    make_device("warehouse-01")
    make_device("warehouse-02")
    check_and_create_alert(db, "warehouse-01", AlertType.HIGH_TEMPERATURE, "w01")
    db.commit()
    check_and_create_alert(db, "warehouse-02", AlertType.HIGH_TEMPERATURE, "w02")
    db.commit()

    assert db.query(Alert).count() == 2


def test_deduplication_allows_after_window_expires(db, make_device):
    make_device("warehouse-01")
    old_timestamp = datetime.now(timezone.utc) - timedelta(seconds=301)
    db.add(Alert(
        device_id="warehouse-01",
        type=AlertType.HIGH_TEMPERATURE,
        message="old alert",
        timestamp=old_timestamp,
    ))
    db.commit()

    # window has passed — new alert should be created
    check_and_create_alert(db, "warehouse-01", AlertType.HIGH_TEMPERATURE, "new alert")
    db.commit()

    assert db.query(Alert).count() == 2


def test_deduplication_disabled(db, make_device):
    make_device("warehouse-01")
    check_and_create_alert(db, "warehouse-01", AlertType.OFFLINE, "first", deduplicate=False)
    db.commit()
    check_and_create_alert(db, "warehouse-01", AlertType.OFFLINE, "second", deduplicate=False)
    db.commit()

    assert db.query(Alert).count() == 2


def test_has_recent_alert_true(db, make_device):
    make_device("warehouse-01")
    db.add(Alert(device_id="warehouse-01", type=AlertType.OFFLINE, message="x"))
    db.commit()

    assert has_recent_alert(db, "warehouse-01", AlertType.OFFLINE) is True


def test_has_recent_alert_false_no_alerts(db, make_device):
    make_device("warehouse-01")
    assert has_recent_alert(db, "warehouse-01", AlertType.OFFLINE) is False


def test_has_recent_alert_false_expired(db, make_device):
    make_device("warehouse-01")
    db.add(Alert(
        device_id="warehouse-01",
        type=AlertType.OFFLINE,
        message="x",
        timestamp=datetime.now(timezone.utc) - timedelta(seconds=301),
    ))
    db.commit()

    assert has_recent_alert(db, "warehouse-01", AlertType.OFFLINE) is False
