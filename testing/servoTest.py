# This script controls four servo motors connected to a PCA9685 driver
# board via a Raspberry Pi Zero W. It sweeps each servo from 0 to 180
# degrees to allow for easy debugging and testing of motor movement.

# --- Required Library Installation ---
# Before running, make sure you have the necessary libraries installed:
# sudo pip3 install adafruit-circuitpython-pca9685
# sudo pip3 install adafruit-circuitpython-motor
# sudo pip3 install adafruit-blinka

# --- Import Libraries ---
import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# --- Configuration ---
# The number of servos to control
NUM_SERVOS = 4

# The channels on the PCA9685 where the servos are connected
SERVO_CHANNELS = [0, 1, 2, 3]

# The pulse width range for the servos (in microseconds)
# These values may need to be adjusted for your specific servos.
# A common range for 180-degree servos is 500us to 2500us.
SERVO_PULSE_WIDTHS = (500, 2500)

# --- I2C Bus and PCA9685 Setup ---
try:
    # Initialize the I2C bus on the Raspberry Pi
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    print("I2C bus initialized successfully.")

    # Create a PCA9685 object
    pca = PCA9685(i2c_bus)
    
    # Set the PWM frequency for the servos (usually 50 Hz for most standard servos)
    pca.frequency = 50
    print(f"PCA9685 frequency set to {pca.frequency} Hz.")

except ValueError:
    print("Error: Could not initialize I2C bus. Is the PCA9685 connected correctly?")
    print("Also, ensure I2C is enabled on your Raspberry Pi via 'sudo raspi-config'.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred during setup: {e}")
    exit()


# --- Servo Initialization ---
# Create servo objects for each channel
# The min_pulse and max_pulse parameters define the 0 and 180-degree positions
servos = []
for i, channel in enumerate(SERVO_CHANNELS):
    try:
        # Create a servo object using the specified channel and pulse width range
        my_servo = servo.Servo(
            pca.channels[channel],
            min_pulse=SERVO_PULSE_WIDTHS[0],
            max_pulse=SERVO_PULSE_WIDTHS[1]
        )
        servos.append(my_servo)
        print(f"Servo on channel {channel} initialized.")
    except Exception as e:
        print(f"Error initializing servo on channel {channel}: {e}")
        servos.append(None) # Append None to maintain list structure


# --- Servo Control Loop ---
def debug_servos():
    """
    Sweeps all connected servos from 0 to 180 degrees and back.
    This function runs indefinitely until the script is manually stopped.
    """
    print("\nStarting servo debug cycle. Press Ctrl+C to exit.")
    
    while True:
        try:
            # Sweep servos from 0 to 180 degrees
            print("Sweeping servos from 0 to 180 degrees...")
            for i in range(181):
                for s in servos:
                    if s is not None:
                        s.angle = i
                time.sleep(0.01) # Small delay for smooth movement

            # Sweep servos from 180 to 0 degrees
            print("Sweeping servos from 180 to 0 degrees...")
            for i in range(180, -1, -1):
                for s in servos:
                    if s is not None:
                        s.angle = i
                time.sleep(0.01)

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nExiting servo debugger.")
            break
        except Exception as e:
            print(f"An error occurred during the servo movement loop: {e}")
            break

# Run the debugging function
if __name__ == "__main__":
    debug_servos()
