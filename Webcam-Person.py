#Webcam for person detection
from ultralytics import YOLO
import cv2
import serial
import time
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

cap = cv2.VideoCapture(0)
model = YOLO("yolo11n.pt")

prev_time = 0

#Connection to Arduino (port for windows only)
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2) 

buzzer_on = False
alert_triggered = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    cv2.rectangle(frame, (180, 100), (470, 430), (255, 255, 0), 2)
    cv2.putText(frame, "ROI Zone", (180, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    for box in results[0].boxes:
        cls = int(box.cls[0])

        if cls == 0:  
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            if 180 < cx < 470 and 100 < cy < 430:
                color = (0, 0, 255)
                print("🚨 Inside ROI - Intrusion Detected")

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

    #Buzzer control
    if intrusion and not buzzer_on:
        arduino.write(b'1')  
        buzzer_on = True
        print("🚨 Buzzer ON")

    elif not intrusion and buzzer_on:
        arduino.write(b'0')  
        buzzer_on = False
        print("✅ Buzzer OFF")

    # FPS calculation
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    prev_time = curr_time

    cv2.putText(frame,
                f"FPS: {fps:.2f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2)

    cv2.imshow("Detection", frame)

    if alert_triggered:
        alert_triggered = False

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()