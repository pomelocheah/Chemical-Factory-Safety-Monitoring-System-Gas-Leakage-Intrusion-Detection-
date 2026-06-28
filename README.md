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

## How to Setup?
- Replace the default Wi-Fi SSID and password with your own network information.
- Complete the MQTT broker configuration on your side.
- This application is built to work with the HiveMQ MQTT broker. Please set the corresponding broker address, port and other related parameters as required.

---

## YOLO-Nano Object Detection Setup Guide
This project explains how to set up and run YOLO-Nano for real-time object detection using PyTorch. YOLO-Nano is a lightweight deep learning model designed for edge devices and low-power systems while still maintaining good detection accuracy.

## Project Overview
YOLO-Nano is a compact object detection model optimized for:

- Real-time detection
- Low computational power devices (CPU / low-end GPU)
- Embedded systems (e.g., Jetson Nano, laptops)

It detects objects in images or video streams efficiently using a single forward pass.

## Required Software and Downloads
Before running YOLO-Nano, install the following:

1. Python
Download Python:
https://www.python.org/downloads/
** Make sure to check:
✔ “Add Python to PATH”

2. PyTorch (IMPORTANT)
Install based on your system:
CPU version:
pip install torch torchvision torchaudio

CUDA (GPU version):
Use official selector:
https://pytorch.org/get-started/locally/
3. Install Dependencies
pip install -r requirements.txt
**Verify Installation

Confirm that the required packages are installed successfully:
python -c "import torch; print(torch.__version__)"
python -c "import ultralytics; print('Ultralytics installed successfully')"

4. Run YOLO-Nano (Inference)
Run detection on webcam:
py Webcam-Person.py

5. Run FPS-Calculate
Run calculate FPS for the system :
py FPS-Calculate.py

6. Run detection accuracy
Run to test the detection accuracy for dataset : 
py detection-accuracy.py

7. Edge Inference Latency Test
Measure the latency of edge YOLO inference:
py Latency-testing.py

The program will:
- Open the webcam
- Perform 10 latency measurements
- Display detected persons
- Highlight the Restricted Area (ROI)
- Generate an average latency report

8. Cloud Inference Model
Start the Flask server:
py Cloud-Inference.py

Open another terminal and run:
py Cloud-client.py

9. Cloud Inference Latency Test
Start the Flask server:
py Cloud-Inference.py

Open another terminal and run:
py Cloud-Latency.py

The client will:
-Capture webcam frames
-Send frames to the server
-Receive detection results
-Measure latency over 10 trials
-Display a latency summary

## Repository Structure
