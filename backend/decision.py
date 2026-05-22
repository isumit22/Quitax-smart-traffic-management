def decide_signal(lanes, ambulance=False):
    # Ensure we always return a lane id compatible with the frontend (A/B/C/D)
    if ambulance:
        # Emergency override: default to lane A (can be adjusted to suit requirements)
        return "A"

    # Find lane with max vehicles
    max_lane = max(lanes, key=lanes.get)
    return max_lane