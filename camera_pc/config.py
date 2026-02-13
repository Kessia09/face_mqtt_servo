# camera_pc/config.py
"""
Configuration for the Camera PC MQTT publisher.
Edit these values to match your deployment environment.
"""

# ─────────────────────────────────────────────────────
# MQTT Broker
# ─────────────────────────────────────────────────────
MQTT_BROKER_IP = "157.173.101.159"
MQTT_BROKER_PORT = 1883
MQTT_KEEPALIVE = 60  # seconds

# ─────────────────────────────────────────────────────
# Team Isolation
# ─────────────────────────────────────────────────────
TEAM_ID = "superstars"

MQTT_TOPIC_MOVEMENT = f"vision/{TEAM_ID}/movement"
MQTT_TOPIC_HEARTBEAT = f"vision/{TEAM_ID}/heartbeat"

# ─────────────────────────────────────────────────────
# Movement Detection
# ─────────────────────────────────────────────────────
# Face position thresholds relative to frame center.
# If the face center is within ±DEAD_ZONE_RATIO → CENTERED
# Outside → MOVE_LEFT or MOVE_RIGHT

DEAD_ZONE_RATIO = 0.12   # ← good default (stable)

# 🔥 OPTIONAL: tweak if servo too jumpy
# smaller = more sensitive
# larger = more stable

# ─────────────────────────────────────────────────────
# Anti-Flooding
# ─────────────────────────────────────────────────────
# Only publish when state changes,
# but re-publish periodically as heartbeat

MIN_PUBLISH_INTERVAL = 0.5  # seconds

# ─────────────────────────────────────────────────────
# Camera
# ─────────────────────────────────────────────────────
CAMERA_INDEX = 0  # change if multiple cameras
