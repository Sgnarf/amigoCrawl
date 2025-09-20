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
# The channels on the PCA9685 where the servos are connected
SERVO_CHANNELS = [0, 1, 2, 3]

# The pulse width range for the servos (in microseconds)
# Adjust these values as needed for your specific servos.
SERVO_PULSE_WIDTHS = (500, 2500)

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
# Create servo objects for each channel
servos = {}
for channel in SERVO_CHANNELS:
    try:
        # Create a servo object for the specified channel and pulse width range
        my_servo = servo.Servo(
            pca.channels[channel],
            min_pulse=SERVO_PULSE_WIDTHS[0],
            max_pulse=SERVO_PULSE_WIDTHS[1]
        )
        servos[channel] = my_servo
        print(f"Servo on channel {channel} initialized.")
    except Exception as e:
        print(f"Error initializing servo on channel {channel}: {e}")
        servos[channel] = None

# --- Interactive Control Loop ---
def interactive_control():
    """
    An interactive function to control a single servo at a time.
    """
    print("\nStarting interactive servo control. Press Ctrl+C to exit.")
    
    while True:
        try:
            # Get user input for servo channel
            channel_input = input("\nEnter servo channel (0-3) or 'q' to quit: ")
            if channel_input.lower() == 'q':
                break
            
            # Validate the channel input
            try:
                channel = int(channel_input)
                if channel not in SERVO_CHANNELS:
                    print(f"Error: Invalid channel. Please enter a number between 0 and {len(SERVO_CHANNELS) - 1}.")
                    continue
            except ValueError:
                print("Error: Invalid input. Please enter a number.")
                continue

            # Check if the selected servo was initialized successfully
            if servos[channel] is None:
                print(f"Error: Servo on channel {channel} is not available. Please check your connections.")
                continue

            # Get user input for the angle
            angle_input = input(f"Enter desired angle for servo {channel} (0-180): ")
            
            # Validate the angle input
            try:
                angle = int(angle_input)
                if not 0 <= angle <= 180:
                    print("Error: Invalid angle. Please enter a number between 0 and 180.")
                    continue
            except ValueError:
                print("Error: Invalid input. Please enter a number.")
                continue

            # Set the servo angle
            print(f"Moving servo on channel {channel} to {angle} degrees...")
            servos[channel].angle = angle
            
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
