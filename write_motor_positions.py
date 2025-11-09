import time
from st3215 import ST3215

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

def emergency_stop(servo_bus):
    print("EMERGENCY STOP: disabling torque on all servos")
    for sid in motor_ids.values():
        servo_bus.StopServo(sid)

def safe_move_small(servo_bus, joint_name, delta_deg=5.0, speed=300, acc=10):
    """
    Safely move one joint by a small angle, then back.
    Uses ST3215.MoveTo with low speed/acceleration.
    """
    if joint_name not in motor_ids:
        raise ValueError(f"Unknown joint name: {joint_name}")

    sid = motor_ids[joint_name]
    print(f"\nTesting joint: {joint_name} (ID {sid})")

    if not servo_bus.PingServo(sid):
        print(f"Servo {sid} not responding. Aborting.")
        return

    status = servo_bus.ReadStatus(sid)
    if status is None:
        print("Could not read status. Aborting.")
        return
    if not all(status.values()):
        print("Warning: some status flags are bad:")
        print(status)

    curr_pos = servo_bus.ReadPosition(sid)
    if curr_pos is None:
        print("Could not read position. Aborting.")
        return
    print(f"Current position (ticks): {curr_pos}")

    TICKS_PER_REV = 4096
    delta_ticks = int(delta_deg / 360.0 * TICKS_PER_REV)
    target = curr_pos + delta_ticks
    target = max(0, min(4095, target))
    print(f"Target position (ticks): {target} (~{delta_deg:.2f} deg change)")

    try:
        print("Enabling torque...")
        comm, error = servo_bus.StartServo(sid)
        if comm != 0 or error != 0:
            print(f"Failed to enable torque: comm={comm}, error={error}")
            return

        time.sleep(0.1)

        print(f"Moving to target with speed={speed}, acc={acc} ...")
        res = servo_bus.MoveTo(sid, target, speed=speed, acc=acc, wait=True)
        if res is None:
            print("MoveTo to target failed. Aborting.")
            return

        time.sleep(0.3)

        print("Returning to original position...")
        res = servo_bus.MoveTo(sid, curr_pos, speed=speed, acc=acc, wait=True)
        if res is None:
            print("MoveTo back to original failed.")
            return

        time.sleep(0.3)
        print("Test movement completed safely.")

    finally:
        print("Disabling torque on this servo.")
        servo_bus.StopServo(sid)


if __name__ == "__main__":
    print("Opening servo bus...")
    servo_bus = ST3215('/dev/ttyACM0')

    try:
        print("Scanning for servos...")
        ids = servo_bus.ListServos()
        print("Detected servo IDs:", ids)

        safe_move_small(servo_bus, "left_ankle") # try with all motors

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected.")
        emergency_stop(servo_bus)
    except Exception as e:
        print(f"Exception: {e}")
        emergency_stop(servo_bus)

