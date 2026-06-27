from ultralytics import YOLO
import cv2
import serial
import time
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

#Load YOLO-Nano Model
model = YOLO("yolo11n.pt")

# Open Webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam.")
    exit()

# Connect Arduino
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
    print("Arduino Connected")
except:
    print("Arduino Not Connected (Skipping)")
    arduino = None

ROI_X1 = 180
ROI_Y1 = 100
ROI_X2 = 470
ROI_Y2 = 430

buzzer_on = False
alert_triggered = False

prev_time = 0
fps_sum = 0
fps_count = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    intrusion = False

    results = model(frame)

    cv2.rectangle(frame,
                  (ROI_X1, ROI_Y1),
                  (ROI_X2, ROI_Y2),
                  (255, 255, 0),
                  2)

    cv2.putText(frame,
                "Restricted Area",
                (ROI_X1, ROI_Y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2)

    for box in results[0].boxes:

        cls = int(box.cls[0])

        if cls == 0:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            if ROI_X1 < cx < ROI_X2 and ROI_Y1 < cy < ROI_Y2:

                intrusion = True
                color = (0, 0, 255)

                # Popup only once per intrusion event
                if not alert_triggered:
                    messagebox.showwarning(
                        "WARNING",
                        "Restricted Area Intrusion!"
                    )
                    alert_triggered = True

            else:
                color = (0, 255, 0)

            cv2.rectangle(frame,
                          (x1, y1),
                          (x2, y2),
                          color,
                          2)

            cv2.circle(frame,
                       (cx, cy),
                       5,
                       color,
                       -1)

            cv2.putText(frame,
                        f"Person {confidence:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2)

    # Arduino Buzzer
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

        # Allow popup next time
        alert_triggered = False

    # FPS Calculation
    current_time = time.time()

    if prev_time != 0:

        fps = 1 / (current_time - prev_time)

        fps_sum += fps
        fps_count += 1

    else:
        fps = 0

    prev_time = current_time

    cv2.putText(frame,
                f"FPS: {fps:.2f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2)

    cv2.imshow("Chemical Factory Safety Monitoring", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Calculate average FPS
if fps_count > 0:
    average_fps = fps_sum / fps_count
else:
    average_fps = 0

print("\n==============================")
print(f"Average FPS: {average_fps:.2f}")
print("==============================")

# Show average FPS popup when the program ends
messagebox.showinfo(
    "Performance Result",
    f"Average FPS: {average_fps:.2f}"
)

if arduino:
    arduino.write(b'0')
    arduino.close()

cap.release()
cv2.destroyAllWindows()