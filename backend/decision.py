def decide_signal(lanes, ambulance=False):
    if ambulance:
        return "EMERGENCY"

    # Find lane with max vehicles
    max_lane = max(lanes, key=lanes.get)
    return max_lane