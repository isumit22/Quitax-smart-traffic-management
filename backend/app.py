from flask import Flask, jsonify, request
from traffic_ai import get_vehicle_count
from decision import decide_signal
import time
from threading import Lock

app = Flask(__name__)

last_update = 0
cached_data = {
    "lanes": {"A": 0, "B": 0, "C": 0, "D": 0},
    "green": "A",
    "emergency": False
}

lock = Lock()

@app.route("/traffic")
def traffic():
    global last_update, cached_data

    ambulance = request.args.get("ambulance") == "true"

    with lock:
        # 🚑 Emergency override (instant)
        if ambulance:
            return jsonify({
                "lanes": cached_data["lanes"],
                "green": "A",  # or change based on logic
                "emergency": True
            })

        # ⏱ Update every 5 seconds
        if time.time() - last_update > 5:
            lanes = {
                "A": get_vehicle_count("../videos/video1.mp4"),
                "B": get_vehicle_count("../videos/video2.mp4"),
                "C": get_vehicle_count("../videos/video3.mp4"),
                "D": get_vehicle_count("../videos/video4.mp4"),
            }

            signal = decide_signal(lanes, False)

            cached_data = {
                "lanes": lanes,
                "green": signal,
                "emergency": False
            }

            last_update = time.time()

    return jsonify(cached_data)


if __name__ == "__main__":
    app.run(debug=True)