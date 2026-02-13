🎯 Face-Tracking MQTT Servo System










Real-time face tracking system that detects head movement on a camera PC and physically moves a servo motor via MQTT and WebSocket relay.

✨ Features

🎥 Real-time face detection & locking

🧭 Movement direction analysis

☁️ MQTT-based distributed architecture

🔁 VPS WebSocket relay for dashboards

🤖 ESP8266 servo control

⚡ Anti-flood intelligent publishing

🖥 Live visual debugging overlay

🧠 System Architecture
Camera PC
   ↓
Face Lock System
   ↓
Movement Analyzer
   ↓
MQTT Publisher
   ↓
🌐 VPS Mosquitto Broker
   ↓
WebSocket Relay
   ↓
ESP8266 Subscriber
   ↓
🎯 Servo Motor

📁 Project Structure
face-mqtt-servo/
│
├── camera_pc/
│   ├── main.py
│   ├── config.py
│   ├── movement_analyzer.py
│   └── mqtt_publisher.py
│
├── esp8266/
│   ├── main.py
│   └── config.py
│
├── server/
│   └── ws_relay.py
│
├── src/
│   ├── face_lock.py
│   ├── camera_display.py
│   └── enroll.py
│
└── data/
    └── enroll/

⚙️ Requirements
🖥 Camera PC

Python 3.10+

Webcam

Windows/Linux/macOS

Install dependencies:

pip install opencv-python paho-mqtt numpy

🌐 VPS

Ubuntu/Debian server

Mosquitto broker

Python 3.10+

Install:

sudo apt update
sudo apt install -y mosquitto mosquitto-clients
pip install websockets paho-mqtt

📡 ESP8266

MicroPython firmware

SG90 (or similar) servo

External 5V power supply ⚠️ recommended

🔧 Configuration
1️⃣ Camera PC

Edit:

camera_pc/config.py


Important fields:

TEAM_ID = "superstars"
MQTT_BROKER_IP = "YOUR_VPS_IP"

2️⃣ ESP8266

Edit:

esp8266/config.py


Set your:

WiFi credentials

VPS IP

TEAM_ID (must match PC)

3️⃣ VPS Relay

Edit:

server/ws_relay.py


Verify:

TEAM_ID = "superstars"
MQTT_BROKER = "127.0.0.1"

▶️ Running the System
✅ Step 1 — Start Mosquitto (VPS)
sudo systemctl start mosquitto
sudo systemctl status mosquitto

✅ Step 2 — Start WebSocket Relay (VPS)
cd ~/backend
python3 ws_relay.py


Expected output:

[MQTT] Connected and subscribed
[WS] Listening on ws://0.0.0.0:9002

✅ Step 3 — Flash & Run ESP8266

Upload:

esp8266/main.py

esp8266/config.py

Serial monitor should show:

WiFi connected
MQTT connected

✅ Step 4 — Enroll Face (Camera PC)
python -m src.enroll

✅ Step 5 — Run Camera Node
python -m camera_pc.main


Controls:

Key	Action
r	Release lock
q	Quit
🎮 Movement States

Published via MQTT:

MOVE_LEFT

MOVE_RIGHT

CENTERED

NO_FACE

ESP8266 converts these into servo angles.

🔌 Servo Wiring (VERY IMPORTANT)
Servo Red   → External 5V
Servo Brown → GND (shared with ESP8266)
Servo Orange → GPIO14 (D5)


⚠️ Do NOT power servo from ESP8266 3.3V

🐛 Troubleshooting
❌ WebSocket keeps reconnecting

Check:

relay is running

correct WS port

VPS firewall open

browser console

❌ Servo not moving

Check:

TEAM_ID matches everywhere

MQTT connected on ESP

servo has external 5V

correct GPIO pin

❌ MQTT not connecting

Verify broker:

sudo systemctl status mosquitto

🚀 Future Improvements

⬆️ Vertical tracking (pan-tilt)

👥 Multi-face support

🎯 Motion smoothing

📱 Mobile dashboard

🔐 TLS security

🧠 AI face prediction

🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first.

📜 License

MIT License — feel free to use and modify.

👩‍💻 Author

Team: Superstars
Project: Face-Tracking MQTT Servo System
Built with: Python • MQTT • MicroPython • OpenCV
