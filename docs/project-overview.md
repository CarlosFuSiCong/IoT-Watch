# IoT Watch — Project Overview

## 1. Background

In warehouse, industrial, and energy scenarios, enterprises need to monitor device status (temperature, humidity, battery, etc.) in real time and trigger alerts when anomalies occur.

This project aims to build a **lightweight IoT platform** for:

- Simulating multi-device data reporting
- Real-time collection and processing of sensor data
- A visual monitoring dashboard
- Basic alerting

## 2. Goals

### Must Have (MVP)

- Multi-device simulated data reporting (MQTT)
- Backend real-time reception and storage of data
- Device online/offline status detection
- Web Dashboard with real-time display
- Basic alerts (temperature, battery, offline)

### Optional Enhancements

- Real-time WebSocket push
- Anomaly detection (simple AI)
- Multi-device management (CRUD)
- Docker deployment

## 3. User Roles

### System User (Operator)

- View device status
- View real-time data
- View historical data
- View alerts

**Note**: No complex permission system is required; the design is simplified.

## 4. Acceptance Criteria

### Functional

- [ ] Multiple device data changes are visible
- [ ] Device online/offline can be correctly determined
- [ ] Alerts can be triggered and displayed
- [ ] Dashboard displays correctly

### Technical

- [ ] MQTT communication works correctly
- [ ] Data is stored in the database
- [ ] API responds correctly
- [ ] Web pages render and function correctly
