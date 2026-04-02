"""Tests for GET /devices/{id}/telemetry."""
from datetime import datetime, timedelta, timezone


def test_get_telemetry_device_not_found(client):
    resp = client.get("/devices/ghost/telemetry")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Device not found"


def test_get_telemetry_empty(client, make_device):
    make_device("warehouse-01")

    resp = client.get("/devices/warehouse-01/telemetry")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["items"] == []
    assert body["data"]["total"] == 0
    assert body["data"]["page"] == 1
    assert body["data"]["limit"] == 50


def test_get_telemetry_returns_data(client, make_device, make_sensor_data):
    make_device("warehouse-01")
    make_sensor_data("warehouse-01", temperature=30.0, battery=85.0)

    resp = client.get("/devices/warehouse-01/telemetry")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["total"] == 1
    item = data["items"][0]
    assert item["device_id"] == "warehouse-01"
    assert item["temperature"] == 30.0
    assert item["battery"] == 85.0


def test_get_telemetry_ordered_newest_first(client, make_device, make_sensor_data):
    make_device("warehouse-01")
    now = datetime.now(timezone.utc)
    make_sensor_data("warehouse-01", temperature=25.0, timestamp=now - timedelta(seconds=10))
    make_sensor_data("warehouse-01", temperature=35.0, timestamp=now)

    resp = client.get("/devices/warehouse-01/telemetry")
    items = resp.json()["data"]["items"]
    # newest (35.0°C) must come first
    assert items[0]["temperature"] == 35.0
    assert items[1]["temperature"] == 25.0


def test_get_telemetry_pagination(client, make_device, make_sensor_data):
    make_device("warehouse-01")
    for i in range(5):
        make_sensor_data("warehouse-01", temperature=float(20 + i))

    resp = client.get("/devices/warehouse-01/telemetry?page=1&limit=2")
    data = resp.json()["data"]
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["limit"] == 2

    resp2 = client.get("/devices/warehouse-01/telemetry?page=2&limit=2")
    data2 = resp2.json()["data"]
    assert len(data2["items"]) == 2

    resp3 = client.get("/devices/warehouse-01/telemetry?page=3&limit=2")
    data3 = resp3.json()["data"]
    assert len(data3["items"]) == 1


def test_get_telemetry_only_own_device(client, make_device, make_sensor_data):
    make_device("warehouse-01")
    make_device("warehouse-02")
    make_sensor_data("warehouse-01")
    make_sensor_data("warehouse-02")

    resp = client.get("/devices/warehouse-01/telemetry")
    items = resp.json()["data"]["items"]
    assert all(r["device_id"] == "warehouse-01" for r in items)
