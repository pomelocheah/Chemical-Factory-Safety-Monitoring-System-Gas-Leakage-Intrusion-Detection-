## Chemical-Factory-Safety-Monitoring-System-Gas-Leakage-Intrusion-Detection-


## Project Overview
This project implements an intelligent safety monitoring system for chemical workshops, focusing on flammable gas leakage detection and unauthorized human intrusion detection. The system uses ESP32 as the IoT sensing node and a laptop as the edge AI host.

## Key Features
- ESP32 developed with **Arduino IDE**
- Multi-sensor monitoring: DHT11, MQ-2 gas sensor, HC-SR04 ultrasonic
- I2C OLED display for real-time local data visualization
- MQTT wireless communication for data transmission
- Laptop built-in camera + YOLO-Nano for human intrusion detection
- Dual intrusion detection (ultrasonic + vision)
- Graded linkage alarm system

## Hardware Components
- ESP32-WROOM-32
- DHT11 Temperature & Humidity Sensor
- MQ-2 Combustible Gas Sensor
- HC-SR04 Ultrasonic Sensor
- 0.96" I2C OLED Display
- Laptop (Built-in Webcam)

## Software & Tools
- **Arduino IDE** (for ESP32 firmware)
- Python (for MQTT client & AI detection)
- MQTT Broker (broker.emqx.io)
- YOLO-Nano (edge AI model)

## Repository Structure