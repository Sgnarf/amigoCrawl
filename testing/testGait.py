# This script makes the robot "crawl" forward using a simple two-phase gait.
# It controls the four servos (shoulders and elbows) in a synchronized sequence
# to achieve forward motion.

# --- Required Library Installation ---
# Ensure you have the necessary libraries installed:
# sudo pip3 install adafruit-circuitpython-pca9685
# sudo pip3 install adafruit-circuitpython-motor
# sudo pip3 install adafruit-blinka

# --- Import Libraries ---
import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# --- Servo Configuration ---
# Define a list of dictionaries, where each dictionary represents a servo.
# This makes it easy to manage each servo's specific parameters.
SERVO_CONFIG = [
    {
        "name": "Right Shoulder",
        "channel": 0,
        "min_pulse": 500,
        "max_pulse": 2500,
        "backward_angle": 0,
        "forward_angle": 180
    },
    {
        "name": "Left Shoulder",
        "channel": 1,
        "min_pulse": 500,
        "max_pulse": 2500,
        "backward_angle": 180,
        "forward_angle": 0
    },
    {
        "name": "Right Elbow",
        "channel": 2,
        "min_pulse": 500,
        "max_pulse": 2500,
        "up_angle": 0,
        "down_angle": 180
    },
    {
        "name": "Left Elbow",
        "channel": 3,
        "min_pulse": 500,
        "max_pulse": 2500,
        "up_angle": 180,
        "down_angle": 0
    },
]

# --- I2C Bus and PCA9685 Setup ---
try:
    # Initialize the I2C bus on the Raspberry Pi
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    print("I2C bus initialized successfully.")
    pca = PCA9685(i2c_bus)
    pca.frequency = 50
    print(f"PCA9685 frequency set to {pca.frequency} Hz.")

except ValueError:
    print("Error: Could not initialize I2C bus. Is the PCA9685 connected and enabled?")
    print("Ensure I2C is enabled on your Raspberry Pi via 'sudo raspi-config'.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred during setup: {e}")
    exit()

# --- Servo Initialization ---
servos = {}
for config in SERVO_CONFIG:
    try:
        my_servo = servo.Servo(
            pca.channels[config["channel"]],
            min_pulse=config["min_pulse"],
            max_pulse=config["max_pulse"]
        )
        servos[config["name"]] = my_servo
        print(f"Servo '{config['name']}' on channel {config['channel']} initialized.")
    except Exception as e:
        print(f"Error initializing servo '{config['name']}' on channel {config['channel']}: {e}")
        servos[config["name"]] = None

# --- Gait Control Functions ---

def move_all_servos(angle_map, speed=0.01, steps=10):
    """
    Moves multiple servos to their target angles smoothly.

    Args:
        angle_map (dict): A dictionary mapping servo names to target angles.
        speed (float): Delay between each step in the movement.
        steps (int): Number of intermediate steps to move through.
    """
    current_angles = {name: servos[name].angle for name in angle_map.keys()}
    
    for i in range(steps + 1):
        for name, target_angle in angle_map.items():
            if servos[name]:
                # Calculate the intermediate angle for a smooth transition
                current_angle = current_angles.get(name)
                # If the servo has no current angle (first run), set it to the start
                if current_angle is None:
                    current_angle = 90 # Start from a neutral position
                    servos[name].angle = current_angle
                    
                new_angle = current_angle + (target_angle - current_angle) * (i / steps)
                servos[name].angle = new_angle
        time.sleep(speed)


def set_neutral_position():
    """
    Initializes all servos to a neutral, standing position (90 degrees).
    """
    print("\nSetting robot to neutral position...")
    for s in servos.values():
        if s:
            s.angle = 90
    time.sleep(1) # Wait for servos to settle

def crawling_gait():
    """
    Implements a simple crawling gait by moving one arm at a time.
    """
    # Define a delay between each major movement
    step_delay = 0.5

    while True:
        try:
            print("\n--- Starting crawl cycle ---")

            # --- Phase 1: Right arm swing ---
            print("Phase 1: Swinging right arm forward...")
            
            # Lift the right elbow to prepare for the swing
            move_all_servos({"Right Elbow": SERVO_CONFIG[2]["up_angle"]})
            time.sleep(step_delay)

            # Swing the right shoulder forward
            move_all_servos({"Right Shoulder": SERVO_CONFIG[0]["forward_angle"]})
            time.sleep(step_delay)

            # Lower the right elbow to place the arm on the ground
            move_all_servos({"Right Elbow": SERVO_CONFIG[2]["down_angle"]})
            time.sleep(step_delay)

            # --- Phase 2: Left arm swing ---
            print("Phase 2: Swinging left arm forward...")
            
            # Lift the left elbow to prepare for the swing
            move_all_servos({"Left Elbow": SERVO_CONFIG[3]["up_angle"]})
            time.sleep(step_delay)

            # Swing the left shoulder forward
            move_all_servos({"Left Shoulder": SERVO_CONFIG[1]["forward_angle"]})
            time.sleep(step_delay)

            # Lower the left elbow to place the arm on the ground
            move_all_servos({"Left Elbow": SERVO_CONFIG[3]["down_angle"]})
            time.sleep(step_delay)
            
            print("--- Crawl cycle complete ---")
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nExiting the crawling script.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again or restart the script.")

# Run the crawling gait function
if __name__ == "__main__":
    set_neutral_position()
    crawling_gait()
