# servoController.py
import time
import board, busio
from adafruit_pca9685 import PCA9685

# -----------------------
# Servo setup
# -----------------------

SERVOS = {
    "right_shoulder": {"channel": 0, "min": 100, "max": 500},
    "left_shoulder":  {"channel": 1, "min": 100, "max": 500},
    "right_elbow":    {"channel": 2, "min": 100, "max": 500},
    "left_elbow":     {"channel": 3, "min": 100, "max": 500},
}

pca = None  # global PCA9685 handle


def init_servos(address=0x40, freq=50):
    """Initialize I2C and PCA9685"""
    global pca
    i2c = busio.I2C(board.SCL, board.SDA)
    pca = PCA9685(i2c, address=address)
    pca.frequency = freq
    print("PCA9685 initialized at I2C address", hex(address))


def angle_to_pwm(angle, servo_name):
    """Convert 0–180° to pulse length for a given servo"""
    cfg = SERVOS[servo_name]
    pulse = cfg["min"] + (angle / 180.0) * (cfg["max"] - cfg["min"])
    return int(pulse)


def set_servo_angle(servo_name, angle):
    """Move a servo to a given angle"""
    cfg = SERVOS[servo_name]
    pulse = angle_to_pwm(angle, servo_name)
    pca.channels[cfg["channel"]].duty_cycle = pulse << 4  # 12-bit value shifted


def release_servo(servo_name):
    """Stop sending PWM to one servo (relaxes it)"""
    cfg = SERVOS[servo_name]
    pca.channels[cfg["channel"]].duty_cycle = 0


def release_all_servos():
    """Stop all servos"""
    for name in SERVOS:
        release_servo(name)
    print("All servos released.")


def cleanup():
    """Release all servos and turn off PCA9685"""
    release_all_servos()
    pca.deinit()
    print("PCA9685 deinitialized.")


# -----------------------
# Servo testing
# -----------------------

def test_servos(delay):
    """Move all servos through some test positions"""
    for name in SERVOS:
        print(f"Testing {name}...")
        set_servo_angle(name, 0)
        print("Testing at 0°")
        time.sleep(delay)
        set_servo_angle(name, 90)
        print("Testing at 90°")
        time.sleep(delay)
        set_servo_angle(name, 180)
        print("Testing at 180°")
        time.sleep(delay)
        set_servo_angle(name, 90)
        print("Testing at 90°")
        time.sleep(delay)


# -----------------------
# Gait definition
# -----------------------

def stroke_cycle(delay):
    """One breaststroke-like cycle"""

    # Phase 1: Arms forward + elbows up
    set_servo_angle("left_shoulder", 40)
    set_servo_angle("right_shoulder", 140)
    set_servo_angle("left_elbow", 90)
    set_servo_angle("right_elbow", 90)
    time.sleep(delay)

    # Phase 2: Elbows down (grip ground)
    set_servo_angle("left_elbow", 20)
    set_servo_angle("right_elbow", 160)
    time.sleep(delay)

    # Phase 3: Shoulders pull back
    set_servo_angle("left_shoulder", 140)
    set_servo_angle("right_shoulder", 40)
    time.sleep(delay)

    # Phase 4: Elbows up (reset)
    set_servo_angle("left_elbow", 90)
    set_servo_angle("right_elbow", 90)
    time.sleep(delay)


def walk_forward(steps, delay):
    """Run several stroke cycles"""
    for i in range(steps):
        print(f"Step {i+1}/{steps}")
        stroke_cycle(delay)

def turn_right_cycle(delay):
    """Pin the right arm and use the left to turn"""

    # Phase 1: Arms forward + elbows up
    set_servo_angle("left_shoulder", 40)
    set_servo_angle("right_shoulder", 140)
    set_servo_angle("left_elbow", 90)
    set_servo_angle("right_elbow", 90)
    time.sleep(delay)

    # Phase 2: Elbows down (grip ground)
    set_servo_angle("left_elbow", 20)
    set_servo_angle("right_elbow", 160)
    time.sleep(delay)

    # Phase 3: Shoulders pull back
    set_servo_angle("left_shoulder", 140)
    time.sleep(delay)

    # Phase 4: Elbows up (reset)
    set_servo_angle("left_elbow", 90)
    set_servo_angle("right_elbow", 90)
    time.sleep(delay)

def turn_right(steps, delay):
    """Run several turn rigth cycles cycles"""
    for i in range(steps):
        print(f"Step {i+1}/{steps}")
        turn_right_cycle(delay)


# -----------------------
# Main
# -----------------------

if __name__ == "__main__":
    try:
        init_servos()
        #test_servos(delay = 1)
        print("Walking forward...")
        #walk_forward(steps=3, delay=0.8)
        turn_right(steps = 3, delay = 1)
    finally:
        # Always release motors on exit
        cleanup()
