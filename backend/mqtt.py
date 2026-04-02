import logging
import os

import paho.mqtt.client as mqtt

from telemetry.service import process_message

logger = logging.getLogger(__name__)

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
TELEMETRY_TOPIC = "devices/+/telemetry"

_client: mqtt.Client | None = None


def _on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        client.subscribe(TELEMETRY_TOPIC)
        logger.info(f"MQTT connected, subscribed to {TELEMETRY_TOPIC}")
    else:
        logger.error(f"MQTT connection failed: reason_code={reason_code}")


def _on_message(client, userdata, msg):
    process_message(msg.topic, msg.payload)


def start() -> None:
    global _client
    _client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    _client.on_connect = _on_connect
    _client.on_message = _on_message
    _client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    _client.loop_start()
    logger.info(f"MQTT client started → {MQTT_HOST}:{MQTT_PORT}")


def stop() -> None:
    if _client:
        _client.loop_stop()
        _client.disconnect()
        logger.info("MQTT client stopped")
