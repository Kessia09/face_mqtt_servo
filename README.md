# Face MQTT Servo Tracking System

A real-time face tracking system that detects face position using Python, publishes movement data via MQTT, visualizes it on a web dashboard, and physically moves a servo motor connected to an ESP8266/ESP32 to follow the face.

---

## 🚀 Features

* 🎯 Real-time face detection with Python & OpenCV
* 📡 MQTT communication between components
* 🌐 Live movement visualization on HTML dashboard
* 🤖 Servo motor automatically follows face direction
* 🔄 WebSocket relay for browser updates
* ⚡ Lightweight and modular architecture

---

## 🏗️ System Architecture

```
Camera → Python Face Tracker → MQTT Broker → ESP8266 Servo
                                  ↓
                           WebSocket Relay
                                  ↓
                              HTML Dashboard
```

---

## 📁 Project Structure

```
face_mqtt_servo/
│
├── face_lock/              # Python face tracking code
│   └── face_tracker.py
│
├── backend/                # WebSocket relay
│   └── ws_relay.py
│
├── esp/                    # ESP8266/ESP32 servo code
│   └── servo_mqtt.ino
│
├── web/                    # Frontend dashboard
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Requirements

### 🖥️ PC

* Python 3.9+
* Webcam
* Mosquitto MQTT broker
* PowerShell / Terminal

### 📡 Hardware

* ESP8266 or ESP32
* Servo motor (SG90 recommended)
* Jumper wires
* Breadboard
* Stable power supply

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Kessia09/face_mqtt_servo.git
cd face_mqtt_servo
```

---

### 2️⃣ Install Python dependencies

```bash
pip install -r requirements.txt
```

If no requirements file exists:

```bash
pip install opencv-python paho-mqtt numpy
```

---

### 3️⃣ Start MQTT broker

Example (Mosquitto):

```bash
mosquitto -v
```

Or on VPS:

```bash
sudo systemctl start mosquitto
```

---

### 4️⃣ Run WebSocket relay

```bash
cd backend
python ws_relay.py
```

---

### 5️⃣ Run face tracker

```bash
cd face_lock
python face_tracker.py
```

---

### 6️⃣ Upload ESP code

* Open `servo_mqtt.ino` in Arduino IDE
* Select your ESP8266/ESP32 board
* Update:

```cpp
const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";
const char* mqtt_server = "YOUR_VPS_IP";
```

* Upload to board

---

### 7️⃣ Open the dashboard

Open in browser:

```
web/index.html
```

---

## 📡 MQTT Topics

| Topic            | Description              |
| ---------------- | ------------------------ |
| `face/x`         | Horizontal face position |
| `face/y`         | Vertical face position   |
| `face/direction` | Movement direction       |
| `servo/angle`    | Servo angle command      |

---

## 🔧 Configuration

Make sure these match everywhere:

* ✅ MQTT broker IP
* ✅ MQTT port (e.g., 9003 for WebSocket)
* ✅ Topic names
* ✅ WebSocket URL in frontend

---

## 🐛 Troubleshooting

### ❌ WebSocket error / reconnecting

* Check broker port (9003 for WS)
* Confirm ws_relay is running
* Verify firewall allows port
* Ensure frontend URL is correct

---

### ❌ Servo not moving

* Check power supply
* Verify ESP is connected to WiFi
* Confirm MQTT messages arriving
* Check GPIO pin wiring

---

### ❌ Face not detected

* Ensure camera works
* Check lighting
* Verify OpenCV installed

---

## 🛠️ Future Improvements

* 📱 Mobile dashboard
* 🎯 Dual-axis servo (pan/tilt)
* 🧠 Face recognition (not just tracking)
* ☁️ Cloud deployment
* 📊 Movement smoothing

---

## 👩🏽‍💻 Author

**Kessia Ndinda**

* Computer Science Student
* IoT & AI Enthusiast
* Future Tech Entrepreneur 🚀

---

## 📜 License

This project is open source and available under the MIT License.

---

⭐ If you like this project, don't forget to star the repo!
