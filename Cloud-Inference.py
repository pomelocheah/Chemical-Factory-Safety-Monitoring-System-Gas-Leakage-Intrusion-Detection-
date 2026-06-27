from flask import Flask, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)

model = YOLO("yolo11n.pt")

@app.route('/', methods=['GET'])
def home():
    return "YOLO Flask Server is Running"

@app.route('/detect', methods=['POST'])
def detect():

    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']

    img_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    results = model(img)

    person_count = 0
    total_objects = len(results[0].boxes)

    for box in results[0].boxes:
        cls = int(box.cls[0])

        if cls == 0:  # person class
            person_count += 1

    return jsonify({
        "person_count": person_count,
        "total_objects": total_objects
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)