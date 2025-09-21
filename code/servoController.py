# servoController.py
import time
import board, busio
from adafruit_pca9685 import PCA9685

# -----------------------
# Servo setup
# -----------------------

# Dictionary of servo configs: channel -> (min, max)
# Adjust values depending on your specific motors
SERVOS = {
    "right_shoulder": {"channel": 0, "min": 1000, "max": 2000},  
    "left_shoulder":  {"channel": 1, "min": 1000, "max": 2000},
    "left_elbow":     {"channel": 3, "min": 1000, "max": 2000},
    "right_elbow":    {"channel": 2, "min": 1000, "max": 2000},
}

pca = None  # global handle to PCA9685


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
    # PCA9685 expects 16-bit duty cycle (0–65535)
    pca.channels[cfg["channel"]].duty_cycle = pulse << 4


def test_servos(delay=0.5):
    """Move all servos through some test positions"""
    for name in SERVOS:
        print(f"Testing {name}...")
        set_servo_angle(name, 0)
        time.sleep(delay)
        set_servo_angle(name, 90)
        time.sleep(delay)
        set_servo_angle(name, 180)
        time.sleep(delay)
        set_servo_angle(name, 90)
        time.sleep(delay)


# -----------------------
# Gait definition
# -----------------------

def stroke_cycle(delay=0.3):
    """
    Defines one breaststroke-like cycle
    """
    # Phase 1: Arms forward + elbows up
    set_servo_angle("left_shoulder", 60)
    set_servo_angle("right_shoulder", 60)
    set_servo_angle("left_elbow", 120)
    set_servo_angle("right_elbow", 120)
    time.sleep(delay)

    # Phase 2: Elbows down (grip ground)
    set_servo_angle("left_elbow", 60)
    set_servo_angle("right_elbow", 60)
    time.sleep(delay)

    # Phase 3: Shoulders pull back
    set_servo_angle("left_shoulder", 120)
    set_servo_angle("right_shoulder", 120)
    time.sleep(delay)

    # Phase 4: Elbows up (reset)
    set_servo_angle("left_elbow", 120)
    set_servo_angle("right_elbow", 120)
    time.sleep(delay)


def walk_forward(steps=5, delay=0.3):
    """Run several stroke cycles"""
    for i in range(steps):
        print(f"Step {i+1}/{steps}")
        stroke_cycle(delay)


# -----------------------
# Main
# -----------------------

if __name__ == "__main__":
    init_servos()
    test_servos()
    print("Walking forward...")
    walk_forward(steps=10, delay=0.4)
