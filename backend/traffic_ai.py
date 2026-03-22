from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

def get_vehicle_count(video_path):
    cap = cv2.VideoCapture(video_path)
    vehicle_count = 0

    ret, frame = cap.read()
    if not ret:
        return 0

    results = model(frame)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if cls in [2, 3, 5, 7]:  # car, bike, bus, truck
                vehicle_count += 1

    cap.release()
    return vehicle_count