import os
import logging
import cv2
from ultralytics import YOLO

logger = logging.getLogger(__name__)

# Model will be loaded lazily on first inference to avoid heavy startup cost
MODEL_PATH = os.path.join(os.path.dirname(__file__), "yolov8n.pt")
model = None


def load_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            logger.error("Model file not found: %s", MODEL_PATH)
            return None
        try:
            model = YOLO(MODEL_PATH)
        except Exception as e:
            logger.exception("Failed to load YOLO model: %s", e)
            model = None
    return model


def get_vehicle_count(video_path, sample_frames=3):
    """Count vehicles by sampling up to `sample_frames` frames from the video.

    Returns an averaged integer count across sampled frames. Returns 0 on
    error or if model not available.
    """
    m = load_model()
    if m is None:
        return 0

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.warning("Unable to open video: %s", video_path)
        return 0

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)

    indices = []
    if frame_count <= 0:
        # fallback: read first frame only
        ret, frame = cap.read()
        if not ret:
            cap.release()
            return 0
        results = m(frame)
        count = 0
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if cls in [2, 3, 5, 7]:
                    count += 1
        cap.release()
        return count

    step = max(1, frame_count // sample_frames)
    for i in range(0, frame_count, step):
        indices.append(i)
        if len(indices) >= sample_frames:
            break

    total = 0
    valid = 0
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        valid += 1
        results = m(frame)
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if cls in [2, 3, 5, 7]:
                    total += 1

    cap.release()
    if valid == 0:
        return 0
    # average detections per sampled frame
    avg = round(total / valid)
    return avg