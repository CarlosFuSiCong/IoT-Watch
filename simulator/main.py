# IoT Watch Device Simulator
# Publishes telemetry to devices/{device_id}/telemetry every 2-4 seconds.
#
# Alert coverage:
#   HIGH_TEMPERATURE  — each device has a ~25% chance per reading to spike to 36-44 °C
#   LOW_BATTERY       — battery drains 1-3% per reading; resets to 60-90% after reaching 5%
#   OFFLINE           — each device has a ~6% chance per cycle to pause 10-15 s (> 8 s threshold)
import json
import random
import time
import threading
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

MQTT_HOST = "localhost"
MQTT_PORT = 1883
DEVICE_IDS = ["warehouse-01", "warehouse-02", "warehouse-03"]

TEMP_NORMAL_RANGE  = (22.0, 34.0)   # stays below HIGH_TEMPERATURE threshold
TEMP_SPIKE_RANGE   = (36.0, 44.0)   # triggers HIGH_TEMPERATURE alert (> 35 °C)
TEMP_SPIKE_CHANCE  = 0.25           # 25 % probability of spike per reading

HUMIDITY_RANGE     = (45, 75)
INTERVAL_RANGE     = (2, 4)         # seconds between full device sweeps

BATTERY_DECAY      = (1.0, 3.0)     # % lost per reading — fast enough for demo
BATTERY_RESET_AT   = 5.0            # reset when battery falls to this level
BATTERY_RESET_TO   = (60.0, 90.0)   # random range to reset to

OFFLINE_CHANCE     = 0.06           # 6 % chance a device goes dark this cycle
OFFLINE_PAUSE_RANGE = (10, 15)      # seconds the device stays silent (> 8 s threshold)


def iso8601_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def make_payload(device_id: str, battery: float) -> dict:
    if random.random() < TEMP_SPIKE_CHANCE:
        temperature = round(random.uniform(*TEMP_SPIKE_RANGE), 1)
    else:
        temperature = round(random.uniform(*TEMP_NORMAL_RANGE), 1)

    humidity = round(random.uniform(*HUMIDITY_RANGE), 1)
    return {
        "device_id":   device_id,
        "temperature": temperature,
        "humidity":    humidity,
        "battery":     round(battery, 1),
        "timestamp":   iso8601_now(),
    }


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_HOST, MQTT_PORT, 60)

    # stagger starting batteries so not all devices hit LOW_BATTERY at the same moment
    batteries = {did: random.uniform(30, 90) for did in DEVICE_IDS}
    # track per-device "offline pause" end times
    offline_until: dict[str, float] = {did: 0.0 for did in DEVICE_IDS}

    print(f"[simulator] devices={DEVICE_IDS}")
    print(f"[simulator] temp spike chance={TEMP_SPIKE_CHANCE:.0%}  "
          f"offline chance={OFFLINE_CHANCE:.0%}")
    try:
        while True:
            now = time.time()
            for device_id in DEVICE_IDS:
                # ── Offline simulation ──────────────────────────────────
                if now < offline_until[device_id]:
                    remaining = offline_until[device_id] - now
                    print(f"[{iso8601_now()}] {device_id}: OFFLINE (silent for "
                          f"{remaining:.0f}s more)")
                    continue

                # roll for next offline pause
                if random.random() < OFFLINE_CHANCE:
                    pause = random.uniform(*OFFLINE_PAUSE_RANGE)
                    offline_until[device_id] = now + pause
                    print(f"[{iso8601_now()}] {device_id}: going offline for {pause:.0f}s")
                    continue

                # ── Battery ─────────────────────────────────────────────
                battery = max(BATTERY_RESET_AT, batteries[device_id])
                payload = make_payload(device_id, battery)

                batteries[device_id] -= random.uniform(*BATTERY_DECAY)
                if batteries[device_id] <= BATTERY_RESET_AT:
                    batteries[device_id] = random.uniform(*BATTERY_RESET_TO)

                # ── Publish ─────────────────────────────────────────────
                topic = f"devices/{device_id}/telemetry"
                client.publish(topic, json.dumps(payload))

                spike_tag = " *** TEMP SPIKE ***" if payload["temperature"] > 35 else ""
                batt_tag  = " *** LOW BATTERY ***" if payload["battery"] < 20 else ""
                print(f"[{payload['timestamp']}] {device_id}: "
                      f"{payload['temperature']}°C  "
                      f"hum={payload['humidity']}%  "
                      f"bat={payload['battery']}%"
                      f"{spike_tag}{batt_tag}")

            interval = random.uniform(*INTERVAL_RANGE)
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n[simulator] stopped")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
