"""Tests for GET /devices and GET /devices/{id}."""


def test_list_devices_empty(client):
    resp = client.get("/devices")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"] == []


def test_list_devices_returns_all(client, make_device):
    make_device("warehouse-01")
    make_device("warehouse-02")

    resp = client.get("/devices")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    ids = [d["id"] for d in body["data"]]
    assert "warehouse-01" in ids
    assert "warehouse-02" in ids


def test_list_devices_fields(client, make_device):
    make_device("warehouse-01", status="online")

    resp = client.get("/devices")
    device = resp.json()["data"][0]
    assert device["id"] == "warehouse-01"
    assert device["status"] == "online"
    assert "last_seen" in device
    assert "created_at" in device


def test_get_device_found(client, make_device):
    make_device("warehouse-01", status="offline")

    resp = client.get("/devices/warehouse-01")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["id"] == "warehouse-01"
    assert body["data"]["status"] == "offline"


def test_get_device_not_found(client):
    resp = client.get("/devices/does-not-exist")
    assert resp.status_code == 404
    body = resp.json()
    assert body["detail"] == "Device not found"
