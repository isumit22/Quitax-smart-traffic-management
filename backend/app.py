from flask import Flask, jsonify, request
from traffic_ai import get_vehicle_count
from decision import decide_signal

app = Flask(__name__)

@app.route("/traffic")
def traffic():
    lanes = {
        "A": get_vehicle_count("../videos/traffic.mp4"),
        "B": get_vehicle_count("../videos/traffic.mp4"),
        "C": get_vehicle_count("../videos/traffic.mp4"),
        "D": get_vehicle_count("../videos/traffic.mp4"),
    }

    ambulance = request.args.get("ambulance") == "true"
    signal = decide_signal(lanes, ambulance)

    return jsonify({
        "lanes": lanes,
        "green": signal
    })

if __name__ == "__main__":
    app.run(debug=True)