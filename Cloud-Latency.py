import cv2
import requests
import time

cap = cv2.VideoCapture(0)

SERVER_URL = "http://127.0.0.1:5000/detect"

latencies = []

print("\n🚀 CLOUD LATENCY TEST STARTING (10 TRIALS)\n")
print("=" * 60)

trial = 0
MAX_TRIALS = 10

while trial < MAX_TRIALS:

    ret, frame = cap.read()
    if not ret:
        break

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

    print(f"Trial {trial:02d} | Latency: {latency:.2f} ms | "
          f"Person: {result.get('person_count', 0)} | "
          f"Total: {result.get('total_objects', 0)}")

    # Show video
    cv2.putText(frame,
                f"Trial: {trial}/10",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2)

    cv2.putText(frame,
                f"Latency: {latency:.2f} ms",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2)

    cv2.imshow("Cloud Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# =========================
# FINAL REPORT
# =========================
print("\n" + "=" * 60)
print("📊 FINAL CLOUD LATENCY REPORT (10 TRIALS)")
print("=" * 60)

for i, t in enumerate(latencies, 1):
    print(f"Trial {i:02d}: {t:.2f} ms")

print("-" * 60)

avg = sum(latencies) / len(latencies)
min_t = min(latencies)
max_t = max(latencies)

print(f"Average Latency : {avg:.2f} ms")
print(f"Minimum Latency : {min_t:.2f} ms")
print(f"Maximum Latency : {max_t:.2f} ms")

print("=" * 60)