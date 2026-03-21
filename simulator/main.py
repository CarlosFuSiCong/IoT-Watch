# IoT Watch Device Simulator
# Publishes telemetry to devices/{device_id}/telemetry
import json
import paho.mqtt.client as mqtt

MQTT_HOST = "localhost"
MQTT_PORT = 1883
TOPIC = "devices/test-01/telemetry"


def main():
    payload = {
        "device_id": "test-01",
        "temperature": 28.5,
        "humidity": 60,
        "battery": 87,
        "timestamp": "2025-03-21T12:00:00Z",
    }
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.publish(TOPIC, json.dumps(payload))
    client.disconnect()
    print(f"Published to {TOPIC}: {payload}")


if __name__ == "__main__":
    main()
