import cv2
import requests

cap = cv2.VideoCapture(0)

SERVER_URL = "http://127.0.0.1:5000/detect"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    _, img_encoded = cv2.imencode('.jpg', frame)

    files = {
        "image": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")
    }

    try:
        response = requests.post(SERVER_URL, files=files, timeout=5)
        result = response.json()
    except Exception as e:
        print("Server error:", e)
        continue

    person_count = result.get("person_count", 0)

    print("Cloud Result:", result)

    cv2.putText(frame,
                f"Persons: {person_count}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2)

    cv2.imshow("Cloud Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()