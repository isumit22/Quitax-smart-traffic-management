import os
import time
import logging
from threading import Lock
from flask import Flask, jsonify, request

from traffic_ai import get_vehicle_count
from decision import decide_signal

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return response


last_update = 0
cached_data = {
    "lanes": {"A": 0, "B": 0, "C": 0, "D": 0},
    "green": "A",
    "emergency": False,
}

lock = Lock()


def video_path(name):
    # Resolve videos folder relative to repository root
    backend_dir = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(backend_dir, os.pardir))
    return os.path.join(repo_root, "videos", name)


@app.route("/health")
def health():
    # lightweight health endpoint
    model_loaded = False
    try:
        # check if model is loaded without forcing heavy load
        import traffic_ai
        model_loaded = getattr(traffic_ai, "model", None) is not None
    except Exception:
        model_loaded = False
    return jsonify({"status": "ok", "model_loaded": model_loaded})


@app.route("/traffic")
def traffic():
    global last_update, cached_data

    ambulance = request.args.get("ambulance") == "true"

    with lock:
        # ⏱ Update every 5 seconds
        if time.time() - last_update > 5:
            lanes = {
                "A": get_vehicle_count(video_path("video1.mp4")),
                "B": get_vehicle_count(video_path("video2.mp4")),
                "C": get_vehicle_count(video_path("video3.mp4")),
                "D": get_vehicle_count(video_path("video4.mp4")),
            }

            signal = decide_signal(lanes, ambulance)

            cached_data = {
                "lanes": lanes,
                "green": signal,
                "emergency": bool(ambulance),
            }

            last_update = time.time()

    return jsonify(cached_data)


if __name__ == "__main__":
    app.run(debug=True)