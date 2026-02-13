# camera_pc/mqtt_publisher.py
"""
MQTT client for the Camera PC Node.

Connects to the VPS Mosquitto broker and publishes movement events.
Architecture rule enforced:
    ✅ MQTT only
    ❌ No WebSocket, HTTP, or direct ESP communication from PC.
"""

from __future__ import annotations
import json
import time
from typing import Dict

import paho.mqtt.client as mqtt

from .config import (
    MQTT_BROKER_IP,
    MQTT_BROKER_PORT,
    MQTT_KEEPALIVE,
    MQTT_TOPIC_MOVEMENT,
    TEAM_ID,
)


class CameraPCPublisher:
    """Manages MQTT connection and sends movement events from the Camera PC."""

    def __init__(self):
        self._mqtt_client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"camera_pc_{TEAM_ID}",
            protocol=mqtt.MQTTv311,
        )
        self._mqtt_client.on_connect = self._handle_connect
        self._mqtt_client.on_disconnect = self._handle_disconnect
        self._is_connected = False

    # ── Internal callbacks ──────────────────────────────────────────

    def _handle_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0 or rc == mqtt.CONNACK_ACCEPTED:
            self._is_connected = True
            print(f"[MQTT] Connected to {MQTT_BROKER_IP}:{MQTT_BROKER_PORT}")
        else:
            print(f"[MQTT] Failed to connect (rc={rc})")

    def _handle_disconnect(self, client, userdata, flags=None, rc=None, properties=None):
        self._is_connected = False
        if rc != 0:
            print(f"[MQTT] Unexpected disconnect (rc={rc}). Reconnection may be required.")

    # ── Public API ──────────────────────────────────────────────────

    def connect(self, timeout: float = 15) -> None:
        """
        Connect to the MQTT broker.

        Args:
            timeout: Maximum seconds to wait for connection
        """
        print(f"[MQTT] Connecting to {MQTT_BROKER_IP}:{MQTT_BROKER_PORT} ...")
        self._mqtt_client.connect(MQTT_BROKER_IP, MQTT_BROKER_PORT, keepalive=MQTT_KEEPALIVE)
        self._mqtt_client.loop_start()

        # Wait until connected or timeout
        start_time = time.time()
        while not self._is_connected and (time.time() - start_time) < timeout:
            time.sleep(0.1)

        if not self._is_connected:
            raise ConnectionError(
                f"Unable to connect to MQTT broker at {MQTT_BROKER_IP}:{MQTT_BROKER_PORT} within {timeout}s"
            )

    def send_movement(self, payload: Dict) -> None:
        """
        Publish a movement message to the MQTT broker.

        Args:
            payload: dict containing "status", "confidence", and "timestamp"
        """
        required_keys = {"status", "confidence", "timestamp"}
        missing = required_keys - payload.keys()
        if missing:
            raise ValueError(f"Payload missing required keys: {missing}")

        message = json.dumps(payload)
        self._mqtt_client.publish(MQTT_TOPIC_MOVEMENT, message, qos=1)

    def disconnect(self) -> None:
        """Disconnect cleanly from the broker."""
        self._mqtt_client.loop_stop()
        self._mqtt_client.disconnect()
        print("[MQTT] Disconnected from broker")

    @property
    def is_connected(self) -> bool:
        return self._is_connected
