# Face MQTT Servo Tracking System

A real-time IoT system that detects a user's face using Python and OpenCV, publishes movement data via MQTT, visualizes the movement on a live web dashboard, and physically moves a servo motor connected to an ESP8266/ESP32 to follow the face direction.

---

## 🧠 System Description

This project implements an end-to-end face tracking pipeline:

1. **Face Detection (PC)**
   The Python script captures webcam frames, detects the face, and computes its position (left, right, center).

2. **MQTT Messaging**
   The detected movement data is published to an MQTT broker.

3. **WebSocket Relay (VPS)**
   The backend relay subscribes to MQTT topics and pushes real-time updates to the browser via WebSocket.

4. **Live Dashboard (Browser)**
   The HTML dashboard displays the face movement in real time.

5. **Servo Control (ESP8266/ESP32)**
   The ESP subscribes to MQTT messages and rotates the servo to follow the face.

---

## 🚀 Features

* 🎯 Real-time face detection with OpenCV
* 📡 MQTT-based communication
* 🌐 Live browser dashboard
* 🤖 Servo motor follows face direction
* 🔄 WebSocket live updates
* ⚡ Lightweight and modular

---

## 🏗️ System Architecture

```
Webcam → Python Face Tracker → MQTT Broker → ESP8266 Servo
                                   ↓
                            WebSocket Relay
                                   ↓
                             Live HTML Dashboard
```

---

## 📁 Project Structure

```
face_mqtt_servo/
│
├── face_lock/
│   └── face_tracker.py
│
├── backend/
│   └── ws_relay.py
│
├── esp/
│   └── servo_mqtt.ino
│
├── web/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── requirements.txt
└── README.md
```

---

## 📡 MQTT Topics Used

| Topic                        | Purpose                      |
| ---------------------------- | ---------------------------- |
| `vision/superstars/movement` | Main face movement direction |
| `face/x`                     | Horizontal face position     |
| `face/y`                     | Vertical face position       |
| `servo/angle`                | Servo angle command          |

✅ **Important:** All components must use the same topic names.

---

## 🌐 Live Dashboard URL

**WebSocket endpoint (example):**

```
ws://YOUR_VPS_IP:9003
```

**Local dashboard:**

```
web/index.html
```

👉 Replace `YOUR_VPS_IP` with your actual VPS address.

---

## ⚙️ Requirements

### PC

* Python 3.9+
* Webcam
* MQTT broker (Mosquitto recommended)

### Hardware

* ESP8266 or ESP32
* SG90 Servo motor
* Jumper wires
* Breadboard
* Stable 5V power supply

---

## 📦 Installation

### 1️⃣ Clone repository

```bash
git clone https://github.com/Kessia09/face_mqtt_servo.git
cd face_mqtt_servo
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If missing:

```bash
pip install opencv-python paho-mqtt numpy websockets
```

---

### 3️⃣ Start MQTT broker

**Linux/VPS**

```bash
sudo systemctl start mosquitto
```

**Local**

```bash
mosquitto -v
```

---

### 4️⃣ Run WebSocket relay

```bash
cd backend
python ws_relay.py
```

Make sure it shows:

```
Ready — MQTT → WebSocket relay active
```

---

### 5️⃣ Run face tracker

```bash
cd face_lock
python face_tracker.py
```

---

### 6️⃣ Upload ESP firmware

1. Open `servo_mqtt.ino` in Arduino IDE
2. Update WiFi and broker settings:

```cpp
const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";
const char* mqtt_server = "YOUR_VPS_IP";
```

3. Upload to ESP8266/ESP32

---

### 7️⃣ Open the dashboard

Open in your browser:

```
web/index.html
```

You should see live movement updates.

---

## 🐛 Troubleshooting

### WebSocket reconnect loop

* Ensure ws_relay is running
* Verify port (9003) is open
* Check frontend WebSocket URL
* Confirm MQTT broker is active

---

### Servo not moving

* Check power supply (very common issue ⚠️)
* Verify ESP WiFi connection
* Confirm MQTT messages received
* Check GPIO wiring

---

### Face not detected

* Check webcam access
* Improve lighting
* Verify OpenCV installation

---

## 🛠️ Future Improvements

* 📱 Mobile-friendly dashboard
* 🎯 Pan-tilt dual servo
* 🧠 Face recognition
* ☁️ Cloud deployment
* 📊 Motion smoothing

---

## 👩🏽‍💻 Author

**Kessia Ndinda**
Computer Science Student | IoT & AI Enthusiast

---

## 📜 License

MIT License

---

⭐ Star the repo if you like this project!
