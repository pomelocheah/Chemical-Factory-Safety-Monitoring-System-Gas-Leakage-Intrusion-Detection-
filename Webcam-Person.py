from ultralytics import YOLO
import cv2
import paho.mqtt.client as mqtt

# ================= MQTT =================
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

# ================= YOLO =================
model = YOLO("yolo11n.pt")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam.")
    exit()

# ================= ROI =================
ROI_X1, ROI_Y1 = 180, 100
roi_w, roi_h = 290, 330

# ================= STATE =================
last_state = -1  # IMPORTANT: ensures first publish always happens

cv2.namedWindow("YOLO ROI Intrusion", cv2.WINDOW_NORMAL)

while True:

    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    intrusion = False

    # ================= KEY CONTROL =================
    key = cv2.waitKey(1) & 0xFF

    if key == ord('w'):
        ROI_Y1 -= 10
    elif key == ord('s'):
        ROI_Y1 += 10
    elif key == ord('a'):
        ROI_X1 -= 10
    elif key == ord('d'):
        ROI_X1 += 10
    elif key == ord('+'):
        roi_w += 20
        roi_h += 20
    elif key == ord('-'):
        roi_w -= 20
        roi_h -= 20

    ROI_X2 = ROI_X1 + roi_w
    ROI_Y2 = ROI_Y1 + roi_h

    # ================= DRAW ROI =================
    cv2.rectangle(frame, (ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2), (255, 255, 0), 2)
    cv2.putText(frame, "ROI ZONE", (ROI_X1, ROI_Y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    # ================= YOLO DETECTION =================
    for box in results[0].boxes:

        cls = int(box.cls[0])
        conf = float(box.conf[0])

        if cls == 0 and conf > 0.5:  # person class

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            # ROI check
            if ROI_X1 < cx < ROI_X2 and ROI_Y1 < cy < ROI_Y2:
                intrusion = True
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.circle(frame, (cx, cy), 5, color, -1)

    if intrusion:
        # print intrusion message in red color (ANSI escape)
        print("\033[91m⚠️ Intrusion detected!\033[0m")
    # ================= FINAL STATE =================
    yoloPerson = 1 if intrusion else 0

    # ================= MQTT (ONLY ON CHANGE) =================
    if yoloPerson != last_state:
        client.publish("ai/person", str(yoloPerson))
        print("📡 MQTT Published:", yoloPerson)
        last_state = yoloPerson

    # ================= DISPLAY =================
    status_text = "INTRUSION" if yoloPerson == 1 else "SAFE"

    cv2.putText(frame, f"STATE: {status_text}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("YOLO ROI Intrusion", frame)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
client.loop_stop()
client.disconnect()