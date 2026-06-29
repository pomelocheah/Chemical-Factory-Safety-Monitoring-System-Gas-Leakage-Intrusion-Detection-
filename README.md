# 🏭 Chemical Factory Safety Monitoring System

### Gas Leakage & Human Intrusion Detection using ESP32, MQTT and YOLO-Nano

---

## 📖 Project Overview

This project presents an intelligent safety monitoring system designed for chemical factory workshops. The system continuously monitors combustible gas concentration, environmental conditions, and unauthorized human intrusion by combining IoT sensing with edge AI vision.

The ESP32 collects data from multiple sensors and publishes them through MQTT, while a laptop running YOLO-Nano performs real-time human detection using the built-in webcam. The system integrates sensor fusion and a graded alarm mechanism to improve industrial safety.

---

## ✨ Features

* 🌡 Real-time temperature and humidity monitoring (DHT11)
* 🔥 Combustible gas leakage detection (MQ-2)
* 📏 Ultrasonic distance sensing (HC-SR04)
* 👤 AI-based human intrusion detection using YOLO-Nano
* 📡 MQTT communication between ESP32 and AI edge device
* 🖥 OLED real-time monitoring display
* 🚨 Three-level warning system

  * Safe (Green)
  * Warning (Yellow)
  * Danger (Red + Buzzer)
* ⚡ Edge AI inference with low latency

---

# System Architecture

```
                +----------------------+
                |    Laptop Webcam     |
                +----------+-----------+
                           |
                           |
                    YOLO-Nano Detection
                           |
                      Person = 0 / 1
                           |
                    MQTT (ai/person)
                           |
        ------------------------------------------
                           |
                    HiveMQ Broker
                           |
        ------------------------------------------
                           |
                        ESP32
     +---------+----------+----------+
     |         |          |          |
    MQ-2      DHT11    HC-SR04    OLED
     |         |          |          |
     +---------+----------+----------+
                           |
                     Decision Logic
                           |
              Safe / Warning / Danger
                           |
                LEDs + Buzzer Alarm
```

---

# Hardware Components

| Component      | Purpose                |
| -------------- | ---------------------- |
| ESP32-WROOM-32 | Main controller        |
| DHT11          | Temperature & Humidity |
| MQ-2           | Gas leakage detection  |
| HC-SR04        | Distance measurement   |
| OLED Display   | Local monitoring       |
| Active Buzzer  | Alarm                  |
| LEDs           | Status indication      |
| Laptop Webcam  | Human detection        |

---

# Software Stack

| Software         | Usage                  |
| ---------------- | ---------------------- |
| Arduino IDE      | ESP32 firmware         |
| Python           | AI & MQTT              |
| OpenCV           | Webcam processing      |
| Ultralytics YOLO | Human detection        |
| MQTT             | Wireless communication |
| HiveMQ Broker    | Message broker         |

---

# Detection Logic

```
Gas Normal
        |
        v
Person?
      /    \
    No      Yes
    |         |
 SAFE      WARNING

Gas Leak?
      |
      v
Person?
      /     \
    No       Yes
    |          |
 WARNING    DANGER
```

---

# Alarm Levels

| Condition            | LED | Buzzer | Status  |
| -------------------- | --- | ------ | ------- |
| Normal               | 🟢  | Off    | Safe    |
| Gas Leak Only        | 🟡  | On     | Warning |
| Human Intrusion Only | 🟡  | On     | Warning |
| Gas Leak + Intrusion | 🔴  | On     | Danger  |

---

# Repository Structure

```
Chemical-Factory-Safety-Monitoring-System/
│
├── Arduino/
│   └── ESP32.ino
│
├── Python/
│   ├── Webcam-Person.py
│   ├── FPS-Calculate.py
│   ├── Latency-testing.py
│   ├── detection-accuracy.py
│   ├── Cloud-Inference.py
    ├── Connection-mqtt.py
│   ├── Cloud-client.py
│   └── Cloud-Latency.py
│
├── Models/
│   └── yolo11n.pt
    └── yolov8n.pt
│
├── Stage1.ino/
│
├── requirements.txt
└── README.md

```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourname/Chemical-Factory-Safety-Monitoring-System.git
cd Chemical-Factory-Safety-Monitoring-System
```

## 2. Install Python Packages

```bash
pip install -r requirements.txt
```

## 3. Configure ESP32

Update the following information inside the Arduino code:

```cpp
const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";
const char* mqtt_server = "broker.hivemq.com";
```

Upload the firmware using Arduino IDE.

---

# Running the System

## Step 1

Run the ESP32 firmware.

## Step 2

Start the YOLO detection and MQTT

```
py Webcam-Person.py
py Connection-mqtt.py
```

## Step 3

Observe:

* OLED display
* MQTT messages
* LEDs
* Alarm status

---

# Performance Evaluation

The repository also includes:

* FPS measurement
* Detection accuracy evaluation
* Edge inference latency
* Cloud inference latency comparison

---

# Future Improvements

* ESP32-CAM integration
* SMS / Telegram notification
* Cloud dashboard
* Historical database logging
* Multi-camera monitoring
* Mobile application

---

# License

This project is developed for academic and research purposes.