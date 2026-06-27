from ultralytics import YOLO
import cv2
import os

model = YOLO("yolov8n.pt")  # YOLO-Nano

dataset_root = "dataset_test"

splits = ["train", "valid", "test"]

image_paths = []

for split in splits:
    img_dir = os.path.join(dataset_root, split, "images")

    if os.path.exists(img_dir):
        for file in os.listdir(img_dir):
            if file.endswith((".jpg", ".png", ".jpeg")):
                image_paths.append(os.path.join(img_dir, file))

print(f"📊 Total Images Found: {len(image_paths)}")

def get_actual_count(image_path):
    label_path = image_path.replace("images", "labels").rsplit(".", 1)[0] + ".txt"

    if not os.path.exists(label_path):
        return 0

    count = 0
    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()

            if len(parts) == 0:
                continue

            class_id = int(parts[0])

            if class_id == 0:  # person class
                count += 1

    return count


correct = 0
false_detection = 0
missed_detection = 0
total_actual = 0

print("\n🚀 Running Evaluation...\n")

for img_path in image_paths:

    img = cv2.imread(img_path)
    if img is None:
        continue

    results = model(img, conf=0.25)

    detected = 0

    for box in results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        if cls == 0 and conf > 0.25:
            detected += 1

    actual = get_actual_count(img_path)

    total_actual += actual

    if detected == actual:
        correct += actual

    elif detected > actual:
        correct += actual
        false_detection += (detected - actual)

    else:
        correct += detected
        missed_detection += (actual - detected)

    print(f"{os.path.basename(img_path)} | Actual: {actual} | Detected: {detected}")


accuracy = (correct / total_actual) * 100 if total_actual else 0

print("\n================ FINAL REPORT ================\n")

print(f"Total Images Tested   : {len(image_paths)}")
print(f"Total Actual Objects  : {total_actual}")
print(f"Correct Detections    : {correct}")
print(f"False Detections      : {false_detection}")
print(f"Missed Detections     : {missed_detection}")

print("\n--------------- METRICS ----------------")
print(f"Accuracy  : {accuracy:.2f}%")

print("\n============================================")