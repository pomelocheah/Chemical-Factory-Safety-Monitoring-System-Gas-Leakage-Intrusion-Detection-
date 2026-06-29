import cv2
import requests
import time
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam.")
    exit()

SERVER_URL = "http://127.0.0.1:5000/detect"

latencies = []
MAX_TRIALS = 10
trial = 0

print("\n🚀 CLOUD LATENCY TEST STARTING (10 TRIALS)\n")
print("=" * 60)

last_trial_time = time.time()
cooldown = 5

alert_triggered = False

ROI_X1, ROI_Y1 = 180, 100
ROI_X2, ROI_Y2 = 470, 430

# ================= MAIN LOOP =================
while True:

    ret, frame = cap.read()
    if not ret:
        break

    intrusion = False
    current_time = time.time()

    person_count = 0

    # ================= CLOUD REQUEST =================
    if trial < MAX_TRIALS and (current_time - last_trial_time >= cooldown):

        _, img_encoded = cv2.imencode('.jpg', frame)

        files = {
            "image": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")
        }

        start_time = time.time()

        try:
            response = requests.post(SERVER_URL, files=files, timeout=5)
            result = response.json()
        except Exception as e:
            print(f"Trial {trial+1}: ERROR -> {e}")
            continue

        end_time = time.time()

        latency = (end_time - start_time) * 1000
        latencies.append(latency)

        trial += 1
        last_trial_time = current_time

        person_count = result.get("person_count", 0)

        print(f"Trial {trial:02d} | Latency: {latency:.2f} ms | "
              f"Person: {person_count} | Total: {result.get('total_objects', 0)}")

    # ================= ROI ZONE =================
    cv2.rectangle(frame, (ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2), (255, 255, 0), 2)
    cv2.putText(frame, "ROI Zone", (ROI_X1, ROI_Y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    # ================= ALERT =================
    if trial > 0 and person_count > 0:
        intrusion = True

        if not alert_triggered:
            messagebox.showwarning("WARNING", "Restricted Area Intrusion!")
            alert_triggered = True
    else:
        alert_triggered = False

    # ================= UI =================
    cv2.putText(frame,
                f"Trial: {trial}/10",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2)

    if len(latencies) > 0:
        cv2.putText(frame,
                    f"Last Latency: {latencies[-1]:.2f} ms",
                    (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2)

    cv2.imshow("Cloud Latency Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if trial >= MAX_TRIALS:
        print("Completed 10 trials.")
        break

cap.release()
cv2.destroyAllWindows()

# ================= REPORT =================
print("\n" + "=" * 60)
print("📊 FINAL CLOUD LATENCY REPORT (10 TRIALS)")
print("=" * 60)

for i, t in enumerate(latencies, 1):
    print(f"Trial {i:02d}: {t:.2f} ms")

avg = sum(latencies) / len(latencies)

print("-" * 60)
print(f"Average Latency : {avg:.2f} ms")
print("=" * 60)