from ultralytics import YOLO
import cv2
import serial
import time
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

model = YOLO("yolo11n.pt")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam.")
    exit()

try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
    print("Arduino Connected")
except:
    print("Arduino Not Connected (Skipping)")
    arduino = None

buzzer_on = False
alert_triggered = False

prev_time = 0

ROI_X1, ROI_Y1 = 180, 100
ROI_X2, ROI_Y2 = 470, 430

while True:
    ret, frame = cap.read()
    if not ret:
        break

    intrusion = False

    results = model(frame)

    end_time = time.time()
    latency = (end_time - start_time) * 1000
    latencies.append(latency)

    cv2.rectangle(frame, (ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2), (255, 255, 0), 2)
    cv2.putText(frame, "ROI Zone", (ROI_X1, ROI_Y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    for box in results[0].boxes:

        cls = int(box.cls[0])

        if cls == 0:  # person class

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            if ROI_X1 < cx < ROI_X2 and ROI_Y1 < cy < ROI_Y2:
                intrusion = True
                color = (0, 0, 255)

                if not alert_triggered:
                    messagebox.showwarning(
                        "WARNING",
                        "Restricted Area Intrusion!"
                    )
                    alert_triggered = True
            else:
                color = (0, 255, 0)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.circle(frame, (cx, cy), 5, color, -1)

    if intrusion:
        if arduino and not buzzer_on:
            arduino.write(b'1')
            buzzer_on = True
            print("🚨 Buzzer ON")
    else:
        if arduino and buzzer_on:
            arduino.write(b'0')
            buzzer_on = False
            print("✅ Buzzer OFF")

        alert_triggered = False

if arduino:
    arduino.write(b'0')
    arduino.close()

cap.release()
cv2.destroyAllWindows()