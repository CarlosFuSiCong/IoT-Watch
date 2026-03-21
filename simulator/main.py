# IoT Watch Device Simulator
# Publishes telemetry to devices/{device_id}/telemetry every 2-5 seconds
import json
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

MQTT_HOST = "localhost"
MQTT_PORT = 1883
DEVICE_IDS = ["warehouse-01", "warehouse-02", "warehouse-03"]
TEMP_RANGE = (25, 35)
HUMIDITY_RANGE = (50, 70)
INTERVAL_RANGE = (2, 5)
BATTERY_DECAY = (0.3, 1.5)
BATTERY_FLOOR = 15


def iso8601_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def make_payload(device_id: str, battery: float) -> dict:
    temperature = round(random.uniform(*TEMP_RANGE), 1)
    humidity = round(random.uniform(*HUMIDITY_RANGE), 1)
    return {
        "device_id": device_id,
        "temperature": temperature,
        "humidity": humidity,
        "battery": round(battery, 1),
        "timestamp": iso8601_now(),
    }


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    batteries = {did: random.uniform(80, 100) for did in DEVICE_IDS}

    print(f"Simulating {DEVICE_IDS}, interval {INTERVAL_RANGE}s, Ctrl+C to stop")
    try:
        while True:
            for device_id in DEVICE_IDS:
                topic = f"devices/{device_id}/telemetry"
                battery = max(BATTERY_FLOOR, batteries[device_id])
                payload = make_payload(device_id, battery)
                batteries[device_id] -= random.uniform(*BATTERY_DECAY)
                if batteries[device_id] < BATTERY_FLOOR:
                    batteries[device_id] = random.uniform(75, 95)

                client.publish(topic, json.dumps(payload))
                print(f"[{payload['timestamp']}] {device_id}: {payload['temperature']}°C {payload['humidity']}% {payload['battery']}%")

            interval = random.uniform(*INTERVAL_RANGE)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
