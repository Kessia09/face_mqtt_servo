# Face-MQTT-Servo - superstars

Face recognition and locking with **ArcFace ONNX** and **5-point alignment**, plus **MQTT-driven servo tracking**: the PC tracks an enrolled face and publishes movement commands; an ESP8266 subscribes and drives a pan servo to follow the face.

- **CPU-only** â€” runs on laptops without GPU  
- **Face locking** â€” lock onto one enrolled identity, track movement, log actions  
- **MQTT + WebSocket** â€” vision publishes to MQTT; optional relay + dashboard in the browser  
- **ESP8266 + MicroPython** â€” subscribes to MQTT and controls a servo


---

## Quick links

| What you need | Where to go |
|---------------|-------------|
| **Setup, deployment, and full walkthrough** | [GUIDE.md](GUIDE.md) |
| **Phase 1: local face-tracking servo** | [GUIDE.md](GUIDE.md) (same guide) |
| **Face locking details** | [FACE_LOCKING_GUIDE.md](FACE_LOCKING_GUIDE.md) (if present) |

---

## Whatâ€™s in this repo

```
face-mqtt-servo/
â”œâ”€â”€ src/                    # Face recognition & locking
â”‚   â”œâ”€â”€ face_lock.py        # Face locking + action detection
â”‚   â”œâ”€â”€ enroll.py, recognize.py, embed.py, ...
â”‚   â””â”€â”€ face_history_logger.py
â”œâ”€â”€ camera_pc/              # MQTT publisher (face position â†’ movement)
â”œâ”€â”€ server/                # WebSocket relay (MQTT â†’ dashboard)
â”œâ”€â”€ esp8266/                # MicroPython: MQTT subscriber + servo
â”œâ”€â”€ dashboard/              # Browser UI (WebSocket)
â”œâ”€â”€ data/                   # Enrolled faces, DB, histories (create via enroll)
â”œâ”€â”€ models/                 # ArcFace ONNX (see GUIDE for download)
â””â”€â”€ GUIDE.md                # Full setup & deployment
```

---

## Dependencies

| Component | Requirements |
|-----------|--------------|
| **PC / Vision** | Python 3.9+, webcam, `pip install -r requirements.txt` (includes OpenCV, MediaPipe, ONNX Runtime, **paho-mqtt** for MQTT). See [GUIDE.md](GUIDE.md) for ArcFace model download. |
| **Backend (VPS)** | Python 3.x, `pip install -r server/requirements.txt` (paho-mqtt, websockets). Mosquitto broker on same host (port 1883). |
| **ESP8266** | MicroPython, WiFi. On device: `mip.install('umqtt.simple')`. |
| **Dashboard** | Modern browser; no extra deps. When served over HTTP(S), connects to WebSocket on same host; for local file use it defaults to `ws://157.173.101.159:9002`. |

---

## How to run each component

1. **Broker (VPS or local):** Start Mosquitto on port 1883 (see [GUIDE.md](GUIDE.md) or [docs/SETUP_COMMANDS.md](docs/SETUP_COMMANDS.md)).
2. **Backend relay (VPS):** `python server/ws_relay.py` â€” listens on port 9002, subscribes to `vision/<TEAM_ID>/movement`.
3. **PC Vision:** Enroll faces first (`python -m src.enroll`), then `python -m camera_pc.main`; set broker IP and `TEAM_ID` in `camera_pc/config.py`.
4. **Dashboard:** Open `dashboard/index.html` in a browser (file or served). For submission: host the dashboard (e.g. serve `dashboard/` on the VPS or another host); it will connect to the relay on that host, or edit the WebSocket URL in the file to `ws://YOUR_VPS_IP:9002`. Submit that dashboard URL in the form.
5. **ESP8266:** Upload `config.py`, `boot.py`, `main.py`; set WiFi, broker IP, and `TEAM_ID` in `config.py`. Power on; it subscribes and drives the servo.

---

## Evaluation focus / Submission checklist

- **MQTT & WebSocket:** PC and ESP use MQTT only; dashboard uses WebSocket only; backend relays MQTT â†’ WebSocket (no polling).
- **Topic isolation:** Unique `TEAM_ID` in all three configs; no generic topics or wildcard subscriptions.
- **End-to-end:** Vision â†’ MQTT â†’ broker â†’ ESP (servo) and broker â†’ relay â†’ dashboard (real-time).
- **Real-time:** Anti-flooding (publish on state change + min interval); no noticeable delay or message flooding.
- **Servo:** Smooth step movement; `NO_FACE` holds position; no uncontrolled jitter.
- **Repo:** Public, structured, README with architecture, topics, setup, dependencies, and run instructions.

---

## One-minute start

1. Clone the repo and open **[GUIDE.md](GUIDE.md)**.
2. Follow **Part 1** (environment, dependencies, model, enrollment).
3. For servo tracking, follow **Phase 1** in the same guide (Mosquitto, ESP8266, relay, dashboard).

All installation, deployment, and run instructions are in **GUIDE.md**.

---

## Phase 1: Distributed visionâ€“control (face-locked servo)

*Distributed Vision-Control System (Face-Locked Servo).* Golden rule: *Vision computes. Devices speak MQTT. Browsers speak WebSocket. The backend relays in real time.*

Phase 1 is **open-loop**: the PC publishes face movement (left/right/centered) over MQTT; the ESP8266 subscribes and drives a pan servo. Optionally a WebSocket relay pushes the same stream to a browser dashboard.

### Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   MQTT publish    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   WebSocket push   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  PC      â”‚ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â†’ â”‚  Broker (local or VPS)      â”‚ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â†’ â”‚ Dashboard â”‚
â”‚  Vision  â”‚                   â”‚  Mosquitto :1883 â†’ ws_relayâ”‚                    â”‚ (Browser) â”‚
â”‚  Node    â”‚                   â”‚  :9002                      â”‚                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                            â”‚ MQTT
                                            â–¼
                                      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                                      â”‚ ESP8266  â”‚
                                      â”‚ + Servo  â”‚
                                      â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Component roles

| Component   | Speaks           | Forbidden                          |
|------------|------------------|------------------------------------|
| PC Vision  | MQTT only        | WebSocket, HTTP, direct ESP        |
| ESP8266    | MQTT only        | WebSocket, HTTP, browser           |
| Backend    | MQTT + WebSocket | Business logic                     |
| Dashboard  | WebSocket only   | MQTT, polling                     |

### MQTT topic

| Topic                     | Publisher | Subscribers   | Payload example |
|---------------------------|----------|---------------|------------------|
| `vision/superstars/movement` | PC Vision| ESP8266, relay| `{"status":"MOVE_LEFT","confidence":0.87,"timestamp":1730000000}` |

Movement states: `MOVE_LEFT`, `MOVE_RIGHT`, `CENTERED`, `NO_FACE`.

**Topic isolation (required on shared broker):** Each team must use a **unique** `TEAM_ID` (this repo uses `superstars`; e.g. `team01`, `alpha`, `y3_grp2`) in `camera_pc/config.py`, `server/ws_relay.py`, and `esp8266/config.py`. Do **not** use generic topics (`vision/movement`, `movement`, `servo`) or wildcard subscriptions (`vision/#`, `#`). Do not publish or subscribe to another teamâ€™s namespace.

### How it works

1. PC captures frame â†’ face detection/recognition â†’ lock onto target face.
2. **MovementDetector** compares face center vs frame center â†’ publishes state only on change (anti-flooding).
3. ESP8266 receives command â†’ steps servo left/right/center.
4. Relay (if used) forwards MQTT to WebSocket â†’ dashboard shows status in real time.

The camera does not move with the servo; the servo points in the direction the face moved.

### Setup (summary)

- **Broker:** Mosquitto on PC or VPS, listener on `0.0.0.0:1883`.
- **PC:** `python -m camera_pc.main` (after enrollment); set `TEAM_ID` in `camera_pc/config.py`.
- **Backend:** `python server/ws_relay.py`; same `TEAM_ID` in `server/ws_relay.py`.
- **ESP8266:** MicroPython, WiFi + MQTT in `esp8266/config.py`, upload `config.py`, `boot.py`, `main.py`; same `TEAM_ID`.
- **Dashboard:** Open `dashboard/index.html`; it connects to `ws://<host>:9002`.

Full step-by-step: **[GUIDE.md](GUIDE.md)** Part 7 (Phase 1).

### Testing MQTT

```bash
# Subscribe
mosquitto_sub -h 127.0.0.1 -t "vision/superstars/movement" -v

# Publish (other terminal)
mosquitto_pub -h 127.0.0.1 -t "vision/superstars/movement" \
  -m '{"status":"MOVE_LEFT","confidence":0.87,"timestamp":1730000000}'
```

(Use your broker host instead of `127.0.0.1` if testing from another machine.)

### Phase 2 (future)

Phase 2 adds **closed-loop feedback**: camera on the servo, system adjusts until face is centered (e.g. PID). Same MQTT architecture; ESP feedback topic and updated servo logic.

### Common issues

| Issue | Fix |
|-------|-----|
| MQTT connection refused | Start Mosquitto; ensure listener on 1883 (and 0.0.0.0 if ESP is on WiFi). |
| ESP8266 WiFi fails | Check SSID/password in `esp8266/config.py`. |
| Dashboard "Connecting" | Run `python server/ws_relay.py`; allow port 9002 if on VPS. |
| No face detected | Enroll first: `python -m src.enroll`. |
| Camera not found | Set `CAMERA_INDEX` in `camera_pc/config.py` (0, 1, 2). |
| ESP `umqtt` import error | On ESP: `mip.install('umqtt.simple')` (see GUIDE Step 7). |

---

## References

- Deng et al. (2019). ArcFace: Additive Angular Margin Loss for Deep Face Recognition. CVPR 2019.
- [InsightFace](https://github.com/deepinsight/insightface) Â· [MediaPipe](https://mediapipe.dev/) Â· [ONNX Runtime](https://onnxruntime.ai/)

---

## License

Educational use.




