import json
import time
import numpy as np
from st3215 import ST3215

motor_ids = {
    "left_hip_yaw":    20,
    "left_hip_roll":   21,
    "left_hip_pitch":  22,
    "left_knee":       23,
    "left_ankle":      24,
    "right_hip_yaw":   10,
    "right_hip_roll":  11,
    "right_hip_pitch": 12,
    "right_knee":      13,
    "right_ankle":     14,
}

# The Generator saves 3 Root Pos + 4 Root Rot = 7 items before joints start
JSON_JOINT_START_INDEX = 7 

home_ticks = {
    "left_hip_yaw":    2921,
    "left_hip_roll":   2594,
    "left_hip_pitch":  1674,
    "left_knee":       2363,
    "left_ankle":      2047,
    "right_hip_yaw":   3624,
    "right_hip_roll":  3100,
    "right_hip_pitch": 1757,
    "right_knee":      2044,
    "right_ankle":     2082,
}

RAD_TO_TICKS = 4096 / (2 * np.pi)

def angle_to_ticks(joint_name, angle_rad):
    ticks = int(home_ticks[joint_name] + (angle_rad * RAD_TO_TICKS))
    
    return max(200, min(3900, ticks)) # clamp

with open("gaits/0.01-0.01.json", "r") as f:
    traj = json.load(f)

#FPS = traj.get("FPS", 60) # originally read from file, need to alter for testing
FPS = 45
dt = 1.0 / FPS
frames = traj["Frames"]

servo_bus = ST3215("/dev/ttyACM0")

print("Initializing Servos...")
for name, sid in motor_ids.items():
    servo_bus.StartServo(sid)
    servo_bus.MoveTo(sid, home_ticks[name], 500)
time.sleep(3)

print(f"Starting Replay: {len(frames)} frames at {FPS} FPS")

start_time = time.time()

for i, frame in enumerate(frames):
    # slice the list to get just the joints
    # grab 10 items starting from index 7
    joint_angles = frame[JSON_JOINT_START_INDEX : JSON_JOINT_START_INDEX + 10]
    
    ordered_names = [
        "left_hip_yaw", "left_hip_roll", "left_hip_pitch", "left_knee", "left_ankle",
        "right_hip_yaw", "right_hip_roll", "right_hip_pitch", "right_knee", "right_ankle"
    ]

    halt = [ "left_hip_yaw", "left_hip_roll", "right_hip_yaw", "right_hip_roll" ] # test without these joints
    
    for j, name in enumerate(ordered_names):
        target_rad = joint_angles[j]
        sid = motor_ids[name]
        target_ticks = angle_to_ticks(name, target_rad)
        if (target_ticks == 200 or target_ticks == 3900):
            # means command was farther than motor range
            print(name)
            for name, sid in motor_ids.items():
                servo_bus.StopServo(sid)
                time.sleep(0.02)

        if(name not in halt):
            servo_bus.MoveTo(sid, target_ticks, speed=3400, acc=254)

    expected_time = (i + 1) * dt
    actual_time = time.time() - start_time
    sleep_time = expected_time - actual_time
    
    if sleep_time > 0:
        time.sleep(sleep_time)

for name, sid in motor_ids.items():
                servo_bus.StopServo(sid)
                time.sleep(0.02)

print("Replay finished.")
