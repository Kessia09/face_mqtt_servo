# esp8266/config.py
"""
ESP8266 Configuration — MicroPython
Edit BEFORE uploading to the board.
"""

# ---------------- WiFi ---------------- #
WIFI_SSID     = "RCA"              # ← CHANGE THIS
WIFI_PASSWORD = "@RcaNyabihu2023"  # ← CHANGE THIS

# ---------------- MQTT Broker ---------------- #
MQTT_BROKER = "157.173.101.159"  # VPS IP (same as ws_relay)
MQTT_PORT   = 1883
TEAM_ID     = "superstars"
MQTT_TOPIC  = f"vision/{TEAM_ID}/movement"
CLIENT_ID   = f"esp8266_{TEAM_ID}"

# ---------------- Servo ---------------- #
SERVO_PIN        = 14    # GPIO14 (D5 on NodeMCU)
SERVO_MIN_ANGLE  = 0
SERVO_MAX_ANGLE  = 180
SERVO_CENTER     = 90
SERVO_STEP       = 5

# ---------------- PWM ---------------- #
SERVO_FREQ = 50   # Hz for SG90 servo
DUTY_MIN   = 40   # duty for 0°
DUTY_MAX   = 115  # duty for 180°
