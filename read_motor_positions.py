from st3215 import ST3215
import time

motor_ids = {
    "left_hip_yaw": 20,
    "left_hip_roll": 21,
    "left_hip_pitch": 22,
    "left_knee": 23,
    "left_ankle": 24,
    "neck_pitch": 30,
    "head_pitch": 31,
    "right_hip_yaw": 10,
    "right_hip_roll": 11,
    "right_hip_pitch": 12,
    "right_knee": 13,
    "right_ankle": 14,
}

servo_bus = ST3215('/dev/ttyACM0')

ids = servo_bus.ListServos()

if ids:
    print("Detected servo IDs:", ids)
         
    for name, sid in motor_ids.items():
        servo_bus.StopServo(sid)
        time.sleep(0.02)
    while(True):
        for name, motor_id in motor_ids.items():
            pos = servo_bus.ReadPosition(motor_id)

            if pos is None:
                print(f"{name} (ID {motor_id}): no response")
            else:
                print(f"{name} (ID {motor_id}): position = {pos}")
        print("")
        time.sleep(5)
