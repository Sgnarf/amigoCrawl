# This script provides an interactive way to test individual servos connected
# to a PCA9685 driver board. It allows you to select a servo channel and
# set a specific angle for that servo.

# --- Required Library Installation ---
# Ensure you have the necessary libraries installed:
# sudo pip3 install adafruit-circuitpython-pca9685
# sudo pip3 install adafruit-circuitpython-motor
# sudo pip3 install adafruit-blinka

# --- Import Libraries ---
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# --- Configuration ---
# Define a list of dictionaries, where each dictionary represents a servo
# You can now give each servo a name and specify its own min/max angle and pulse width
SERVO_CONFIG = [
    {
        "name": "Right Shoulder",
        "channel": 0,
        "min_pulse": 500,
        "max_pulse": 2500,
        "min_angle": 0,
        "max_angle": 180
    },
    {
        "name": "Left Shoulder",
        "channel": 1,
        "min_pulse": 500,
        "max_pulse": 2500,
        "min_angle": 0,
        "max_angle": 180
    },
    {
        "name": "Right Elbow",
        "channel": 2,
        "min_pulse": 500,
        "max_pulse": 2500,
        "min_angle": 0,
        "max_angle": 180
    },
    {
        "name": "Left Elbow",
        "channel": 3,
        "min_pulse": 500,
        "max_pulse": 2500,
        "min_angle": 0,
        "max_angle": 180
    },
]

# --- I2C Bus and PCA9685 Setup ---
try:
    # Initialize the I2C bus on the Raspberry Pi
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    print("I2C bus initialized successfully.")

    # Create a PCA9685 object
    pca = PCA9685(i2c_bus)
    
    # Set the PWM frequency for the servos (usually 50 Hz)
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
# Create servo objects for each channel based on the configuration list
servos = {}
for config in SERVO_CONFIG:
    try:
        # Create a servo object for the specified channel and pulse width range
        my_servo = servo.Servo(
            pca.channels[config["channel"]],
            min_pulse=config["min_pulse"],
            max_pulse=config["max_pulse"]
        )
        servos[config["name"]] = {
            "object": my_servo,
            "min_angle": config["min_angle"],
            "max_angle": config["max_angle"]
        }
        print(f"Servo '{config['name']}' on channel {config['channel']} initialized.")
    except Exception as e:
        print(f"Error initializing servo '{config['name']}' on channel {config['channel']}: {e}")
        servos[config["name"]] = None

# --- Interactive Control Loop ---
def interactive_control():
    """
    An interactive function to control a single servo at a time.
    """
    print("\nAvailable servos:")
    for name in servos.keys():
        print(f" - {name}")
    
    print("\nStarting interactive servo control. Press Ctrl+C to exit.")
    
    while True:
        try:
            # Get user input for servo name
            name_input = input("\nEnter servo name (e.g., 'Right Shoulder') or 'q' to quit: ")
            if name_input.lower() == 'q':
                break
            
            # Check if the entered servo name is valid
            if name_input not in servos:
                print("Error: Invalid servo name. Please choose from the list above.")
                continue

            # Check if the selected servo was initialized successfully
            servo_data = servos[name_input]
            if servo_data is None:
                print(f"Error: Servo '{name_input}' is not available. Please check your connections.")
                continue

            min_angle = servo_data["min_angle"]
            max_angle = servo_data["max_angle"]

            # Get user input for the angle
            angle_input = input(f"Enter desired angle for '{name_input}' ({min_angle}-{max_angle}): ")
            
            # Validate the angle input
            try:
                angle = int(angle_input)
                if not min_angle <= angle <= max_angle:
                    print(f"Error: Invalid angle. Please enter a number between {min_angle} and {max_angle}.")
                    continue
            except ValueError:
                print("Error: Invalid input. Please enter a number.")
                continue

            # Set the servo angle
            print(f"Moving servo '{name_input}' to {angle} degrees...")
            servo_data["object"].angle = angle
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nExiting interactive control.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again or restart the script.")

# Run the interactive control function
if __name__ == "__main__":
    interactive_control()
