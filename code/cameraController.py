from picamera2 import Picamera2
from time import sleep

# --- Configuration ---
OUTPUT_FILENAME = "rotated_image.jpg"
ROTATION_ANGLE = 180  # We want a 180 degree rotation
WARMUP_TIME = 2       # Seconds to wait for the camera to adjust

# --- Script ---
try:
    print("Starting Picamera2...")
    picam2 = Picamera2()

    # Get the default configuration for still images
    config = picam2.create_still_configuration()

    # Apply the rotation to the configuration.
    # The 'transform' parameter controls image manipulation,
    # and 'vflip' (Vertical Flip) and 'hflip' (Horizontal Flip) together
    # achieve a 180 degree rotation.
    config["transform"] = picam2.Transform(vflip=True, hflip=True)
    
    # Start the camera with the specified configuration
    picam2.configure(config)
    picam2.start()

    print(f"Camera started. Waiting {WARMUP_TIME} seconds for sensor warm-up...")
    sleep(WARMUP_TIME)

    print(f"Capturing image and saving to {OUTPUT_FILENAME} with {ROTATION_ANGLE} degree rotation...")
    
    # Capture the image. Since the rotation is applied in the config, 
    # the saved file will already be oriented correctly.
    picam2.capture_file(OUTPUT_FILENAME)

    print(f"Successfully captured and saved {OUTPUT_FILENAME}.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Always ensure the camera is stopped
    if 'picam2' in locals() and picam2.started:
        print("Stopping camera...")
        picam2.stop()
