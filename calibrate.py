import time
import numpy as np
from st3215 import ST3215

motor_ids = {
    "right_hip_yaw":   10, 
    "right_hip_roll":  11, 
    "right_hip_pitch": 12, 
    "right_knee":      13, 
    "right_ankle":     14,
    "left_hip_yaw":    20, 
    "left_hip_roll":   21, 
    "left_hip_pitch":  22, 
    "left_knee":       23, 
    "left_ankle":      24,
}

servo_bus = ST3215("/dev/ttyACM0")

def center_joint(name):
    sid = motor_ids[name]
    servo_bus.MoveTo(sid, 2048, speed=500, acc=10)

def relax_all():
    for name, sid in motor_ids.items():
        servo_bus.StopServo(sid)

print("------------------------------------------------")
print("CALIBRATING")
print("1. Robot will go to CENTER.")
print("2. Robot should be assembled so legs are STRAIGHT (or as close as possible) at each joint's center.")
print("------------------------------------------------")


tests = [ "left_ankle", 
         "right_ankle", 
         "left_knee", 
         "right_knee", 
         "left_hip_pitch", 
         "right_hip_pitch", 
         "left_hip_roll", 
         "right_hip_roll"
        ]

for joint in tests:
    print(f"\nCentering: {joint.upper()}...")
    center_joint(joint)
    time.sleep(1.5)
    
    print("Joint is centered)
    input("Press Enter for next joint...")
    
    time.sleep(1)

relax_all()
print("\nDone.")
