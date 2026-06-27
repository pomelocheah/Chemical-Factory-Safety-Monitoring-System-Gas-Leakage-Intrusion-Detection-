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

ROI_X1, ROI_Y1 = 180, 100
ROI_X2, ROI_Y2 = 470, 430

latencies = []
MAX_TRIALS = 10
trial = 0

while True:

    ret, frame = cap.read()
    if not ret:
        break

    intrusion = False

    if trial < MAX_TRIALS:

        start_time = time.time()

        results = model(frame)

        end_time = time.time()

        latency = (end_time - start_time) * 1000
        latencies.append(latency)

        trial += 1

        print(f"Trial {trial}: {latency:.2f} ms")

    else:
        break

    cv2.rectangle(frame, (ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2), (255, 255, 0), 2)
    cv2.putText(frame, "ROI Zone", (ROI_X1, ROI_Y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    for box in results[0].boxes:

        cls = int(box.cls[0])

        if cls == 0:

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
    else:
        if arduino and buzzer_on:
            arduino.write(b'0')
            buzzer_on = False
        alert_triggered = False

    # Show frame
    cv2.imshow("Latency Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("\n================ TABLE 4.1 RESULTS ================\n")

for i, val in enumerate(latencies):
    print(f"Trial {i+1}: {val:.2f} ms")

avg_latency = sum(latencies) / len(latencies)

print("\n---------------------------------------------------")
print(f"Average Local Inference Latency: {avg_latency:.2f} ms")
print("---------------------------------------------------")

messagebox.showinfo(
    "Latency Result",
    f"Average Latency: {avg_latency:.2f} ms"
)

if arduino:
    arduino.write(b'0')
    arduino.close()

cap.release()
cv2.destroyAllWindows()